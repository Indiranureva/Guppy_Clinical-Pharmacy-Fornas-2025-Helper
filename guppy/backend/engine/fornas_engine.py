"""[USANG - lihat fornas_matcher.py] Engine lama berbasis data 11 obat Fornas 2022; datanya tidak sesuai KMK 1199/2025.
Gunakan guppy/backend/engine/fornas_matcher.py. File ini dipertahankan sementara agar frontend lama tetap berjalan.

Formularium Nasional (Fornas) Restriction Engine.

Provides clinical restriction lookup, diagnosis-based drug matching,
and dosage guidance aligned with Fornas 2022 (JKN Program).
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Resolve path relative to this file
_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
_FORNAS_DB_PATH = _KNOWLEDGE_DIR / "fornas_db.json"


def _load_fornas_db() -> Dict[str, Any]:
    """Load and cache the Fornas knowledge base."""
    try:
        with open(_FORNAS_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"drugs": [], "icd10_index": {}, "metadata": {}}


# Module-level cache
_FORNAS_DB: Optional[Dict[str, Any]] = None


def get_fornas_db() -> Dict[str, Any]:
    global _FORNAS_DB
    if _FORNAS_DB is None:
        _FORNAS_DB = _load_fornas_db()
    return _FORNAS_DB


# ─────────────────────────────────────────────
# FEATURE 1: Drug Restriction Lookup by Name
# ─────────────────────────────────────────────

class FornasDrugLookup:
    """Lookup Fornas restriction data by drug name (INN or brand)."""

    @staticmethod
    def search(query: str) -> List[Dict[str, Any]]:
        """Search drugs by INN name, brand name, or ATC code.
        Returns a list of matching drug records.
        """
        db = get_fornas_db()
        q = query.strip().lower()
        results = []

        for drug in db.get("drugs", []):
            # Match on INN
            if q in drug.get("inn", "").lower():
                results.append(drug)
                continue
            # Match on brand names
            if any(q in brand.lower() for brand in drug.get("brand_examples", [])):
                results.append(drug)
                continue
            # Match on ATC code
            if q in drug.get("atc_code", "").lower():
                results.append(drug)
                continue
            # Match on therapeutic class
            if q in drug.get("therapeutic_class", "").lower():
                results.append(drug)
                continue

        return results

    @staticmethod
    def get_all_drugs() -> List[Dict[str, Any]]:
        """Return all drugs in the Fornas database."""
        return get_fornas_db().get("drugs", [])

    @staticmethod
    def get_drug_names() -> List[str]:
        """Return a sorted list of all INN drug names for UI dropdowns."""
        return sorted([d["inn"] for d in get_fornas_db().get("drugs", [])])

    @staticmethod
    def format_restriction_verdict(drug: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a drug record into a structured restriction verdict for display.
        Returns a dict with keys: summary, restrictions, warnings.
        """
        warnings = []
        restriction_list = drug.get("restrictions", [])
        facility = drug.get("facility_level", "Tidak diketahui")
        prescriber = drug.get("prescriber_restriction", "Tidak diketahui")

        # Detect high-restriction drugs
        for r in restriction_list:
            code = r.get("restriction_code", "")
            if code == "R-FKRTL":
                warnings.append("⚠️ Obat ini hanya boleh diresepkan di FKRTL (Rumah Sakit atau Klinik Utama).")
            if prescriber.startswith("SP"):
                warnings.append("⚠️ Peresepan terbatas untuk Dokter Spesialis — tidak untuk Dokter Umum.")
            if "narkotika" in drug.get("fornas_status", "").lower():
                warnings.append("🔴 NARKOTIKA: Memerlukan resep khusus (Blanko N-1 / e-Narkotika BPOM).")
            # Check prescribing notes for embedded warnings
            notes = r.get("prescribing_notes", "")
            if "HATI-HATI" in notes or "PERINGATAN" in notes:
                warnings.append(f"⚠️ {notes[:200]}..." if len(notes) > 200 else f"⚠️ {notes}")

        return {
            "drug_id": drug.get("drug_id"),
            "inn": drug.get("inn"),
            "atc_code": drug.get("atc_code"),
            "therapeutic_class": drug.get("therapeutic_class"),
            "facility_level": facility,
            "prescriber_restriction": prescriber,
            "fornas_status": drug.get("fornas_status"),
            "dosage_forms": drug.get("dosage_forms", []),
            "restrictions": restriction_list,
            "warnings": warnings,
        }


# ─────────────────────────────────────────────
# FEATURE 2: Diagnosis → Drug Restriction Matching
# ─────────────────────────────────────────────

class FornasDiagnosisMatch:
    """Match patient diagnoses (ICD-10) to Fornas drug restrictions."""

    @staticmethod
    def find_drugs_for_icd10(icd10_code: str) -> List[Dict[str, Any]]:
        """Find all Fornas drugs indicated for a given ICD-10 code.
        
        Args:
            icd10_code: e.g. 'E11', 'I10', 'K21.0'
        
        Returns:
            List of drug records (full objects) matching this ICD-10.
        """
        db = get_fornas_db()
        code_upper = icd10_code.strip().upper()
        index = db.get("icd10_index", {})

        # Try exact match first
        matched_ids = index.get(code_upper, [])

        # If no exact match, try prefix matching (e.g. 'E11' matches 'E11.9')
        if not matched_ids:
            for key, ids in index.items():
                if key.startswith(code_upper) or code_upper.startswith(key):
                    for mid in ids:
                        if mid not in matched_ids:
                            matched_ids.append(mid)

        # Retrieve full drug records
        all_drugs = {d["drug_id"]: d for d in db.get("drugs", [])}
        results = []
        for mid in matched_ids:
            if mid in all_drugs:
                drug = all_drugs[mid]
                # Filter restrictions to only those matching this ICD-10
                relevant_restrictions = [
                    r for r in drug.get("restrictions", [])
                    if any(
                        code_upper == rc.strip().upper() or
                        rc.strip().upper().startswith(code_upper) or
                        code_upper.startswith(rc.strip().upper())
                        for rc in r.get("icd10_codes", [])
                    )
                ]
                drug_copy = dict(drug)
                drug_copy["matched_restrictions"] = relevant_restrictions
                results.append(drug_copy)

        return results

    @staticmethod
    def assess_appropriateness(
        drug: Dict[str, Any],
        patient_diagnosis_icd10: str,
        patient_facility: str = "FKTP",
        prescriber_type: str = "DU",
    ) -> Dict[str, Any]:
        """
        Assess whether prescribing a specific drug for a patient's diagnosis
        is appropriate according to Fornas restrictions.

        Args:
            drug: Full drug record from Fornas DB.
            patient_diagnosis_icd10: Patient's ICD-10 diagnosis code.
            patient_facility: 'FKTP' or 'FKRTL'
            prescriber_type: 'DU' (Dokter Umum) or 'SP' (Spesialis)

        Returns:
            Dict with 'verdict', 'status', 'issues', 'recommendations'
        """
        issues = []
        recommendations = []
        code_upper = patient_diagnosis_icd10.strip().upper()
        status = "SESUAI"  # default

        restrictions = drug.get("restrictions", [])
        if not restrictions:
            return {
                "verdict": "TIDAK DAPAT DINILAI",
                "status": "UNKNOWN",
                "issues": ["Tidak ada data restriksi Fornas untuk obat ini."],
                "recommendations": [],
            }

        # Check if diagnosis matches any restriction indication
        indication_matched = False
        for r in restrictions:
            icd10s = r.get("icd10_codes", [])
            for rc in icd10s:
                rc_upper = rc.strip().upper()
                if rc_upper == code_upper or code_upper.startswith(rc_upper) or rc_upper.startswith(code_upper):
                    indication_matched = True
                    break

        if not indication_matched:
            issues.append(
                f"⚠️ Diagnosis pasien ({patient_diagnosis_icd10}) tidak terdaftar sebagai indikasi "
                f"yang disetujui untuk {drug['inn']} dalam Fornas 2022."
            )
            recommendations.append(
                "Tinjau ulang indikasi klinis. Jika penggunaan di luar indikasi Fornas (off-label), "
                "pertimbangkan justifikasi ilmiah dan persetujuan komite farmasi."
            )
            status = "TIDAK SESUAI INDIKASI"

        # Check facility appropriateness
        r_code = restrictions[0].get("restriction_code", "R")
        if r_code == "R-FKRTL" and patient_facility == "FKTP":
            issues.append(
                f"🏥 Obat '{drug['inn']}' dengan kode restriksi R-FKRTL hanya boleh diresepkan di "
                f"FKRTL (Rumah Sakit / Klinik Utama). Fasilitas pasien saat ini: {patient_facility}."
            )
            recommendations.append(
                "Rujuk pasien ke FKRTL untuk inisiasi terapi. Kelanjutan terapi di FKTP hanya setelah "
                "mendapat instruksi tertulis dari dokter FKRTL."
            )
            status = "TIDAK SESUAI FASILITAS"

        # Check prescriber appropriateness
        drug_prescriber = drug.get("prescriber_restriction", "DU")
        if drug_prescriber.startswith("SP") and prescriber_type == "DU":
            issues.append(
                f"👨‍⚕️ Obat '{drug['inn']}' hanya boleh diresepkan oleh Dokter Spesialis "
                f"({drug_prescriber}). Peresep saat ini: {prescriber_type}."
            )
            recommendations.append(
                "Konsultasikan ke dokter spesialis yang sesuai untuk inisiasi terapi ini. "
                "Dokter Umum tidak diperbolehkan meresepkan obat ini di fasilitas JKN."
            )
            status = "TIDAK SESUAI PERESEP"

        # Overall verdict
        if status == "SESUAI":
            verdict = f"✅ SESUAI — {drug['inn']} dapat diberikan untuk diagnosis {patient_diagnosis_icd10} sesuai Fornas 2022."
        else:
            verdict = f"❌ {status} — Terdapat {len(issues)} masalah restriksi Fornas yang perlu ditindaklanjuti."

        return {
            "verdict": verdict,
            "status": status,
            "issues": issues,
            "recommendations": recommendations,
            "legal_basis": restrictions[0].get("legal_basis", "Fornas 2022"),
        }

    @staticmethod
    def get_icd10_options() -> List[Tuple[str, str]]:
        """Return all ICD-10 codes in the Fornas index as (code, label) tuples."""
        db = get_fornas_db()
        index = db.get("icd10_index", {})
        options = sorted(index.keys())
        return options


# ─────────────────────────────────────────────
# FEATURE 3: Dosage Guidance
# ─────────────────────────────────────────────

class FornasDosageAdvisor:
    """Provide structured dosage guidance from Fornas for a specific drug."""

    @staticmethod
    def get_dosage(drug: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract structured dosage information from a Fornas drug record."""
        results = []
        for restriction in drug.get("restrictions", []):
            dg = restriction.get("dose_guidance", {})
            if dg:
                results.append({
                    "indication": restriction.get("indication_required", ""),
                    "icd10_codes": restriction.get("icd10_codes", []),
                    "dose_guidance": dg,
                    "monitoring": restriction.get("monitoring_required", []),
                    "notes": restriction.get("prescribing_notes", ""),
                    "legal_basis": restriction.get("legal_basis", ""),
                    "guideline_ref": restriction.get("clinical_guidelines_ref", ""),
                })
        return results

    @staticmethod
    def format_dosage_card(drug: Dict[str, Any]) -> str:
        """Format dosage guidance as a readable Markdown card."""
        lines = [f"### 💊 Panduan Dosis Fornas: **{drug['inn']}**\n"]
        lines.append(f"**Kelas Terapi**: {drug.get('therapeutic_class', '-')}")
        lines.append(f"**Sediaan Tersedia**: {', '.join(drug.get('dosage_forms', []))}")
        lines.append(f"**Level Fasilitas**: {drug.get('facility_level', '-')}")
        lines.append(f"**Peresep yang Diizinkan**: {drug.get('prescriber_restriction', '-')}")
        lines.append("")

        for restriction in drug.get("restrictions", []):
            dg = restriction.get("dose_guidance", {})
            lines.append(f"#### Indikasi: {restriction.get('indication_required', '-')}")
            lines.append(f"**ICD-10**: {', '.join(restriction.get('icd10_codes', []))}")
            lines.append("")

            if dg:
                lines.append("**Panduan Dosis:**")
                for key, val in dg.items():
                    key_label = key.replace("_", " ").title()
                    lines.append(f"- **{key_label}**: {val}")
            lines.append("")

            monitoring = restriction.get("monitoring_required", [])
            if monitoring:
                lines.append("**Parameter Monitoring Wajib:**")
                for m in monitoring:
                    lines.append(f"- {m}")
            lines.append("")

            notes = restriction.get("prescribing_notes", "")
            if notes:
                lines.append(f"**Catatan Klinis Fornas**: {notes}")
            lines.append("")
            lines.append(f"> *{restriction.get('legal_basis', '')}*")
            lines.append(f"> *Panduan Klinis: {restriction.get('clinical_guidelines_ref', '')}*")
            lines.append("---")

        return "\n".join(lines)
