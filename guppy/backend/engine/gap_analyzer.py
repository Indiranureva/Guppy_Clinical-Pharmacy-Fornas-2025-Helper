"""ACTD Dossier Gap Analysis and Compliance Scoring Engine."""

import json
from typing import List
from guppy.backend.config import ACTD_RULES_PATH
from guppy.backend.models.product import ProductCase
from guppy.backend.models.dossier import (
    GapSeverity, EvaluationStatus, GapFinding, DossierScorecard
)


class DossierGapAnalyzer:
    """Evaluates product cases and submission dossiers against Indonesian BPOM requirements."""

    def __init__(self, rules_path=ACTD_RULES_PATH):
        self.rules_path = rules_path
        self._load_rules()

    def _load_rules(self):
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.rules = data.get("rules", [])
        except Exception:
            self.rules = []

    def evaluate(self, case: ProductCase) -> DossierScorecard:
        findings: List[GapFinding] = []

        # 1. Evaluate GMP Certificate (Part I.C)
        if not case.manufacturing.gmp_certificate_valid:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-I-GMP",
                actd_part="Part_I",
                section="I.C",
                title="Sertifikat CPOB / GMP Aktif",
                status=EvaluationStatus.FAIL,
                severity=GapSeverity.CRITICAL,
                observation=f"Sertifikat CPOB produsen {case.manufacturing.manufacturer_name} tidak valid atau kedaluwarsa.",
                legal_citation="UU No. 17/2023 Pasal 146 jo. PerBPOM No. 24/2017",
                remediation_steps=[
                    "Segera ajukan resertifikasi inspeksi CPOB ke BPOM.",
                    "Jangan mengajukan berkas pra-registrasi sebelum dokumen CPOB dinyatakan aktif di sistem ASROT."
                ]
            ))
        else:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-I-GMP",
                actd_part="Part_I",
                section="I.C",
                title="Sertifikat CPOB / GMP Aktif",
                status=EvaluationStatus.PASS,
                severity=GapSeverity.COMPLIANT,
                observation="Fasilitas manufaktur memiliki sertifikat CPOB / GMP yang masih berlaku.",
                legal_citation="UU No. 17/2023 Pasal 146",
                remediation_steps=[]
            ))

        # 2. Evaluate 2D Barcode (Part I.G)
        if not case.barcode_2d_present:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-I-BARCODE",
                actd_part="Part_I",
                section="I.G",
                title="2D Barcode (QR Code) Penandaan BPOM",
                status=EvaluationStatus.FAIL,
                severity=GapSeverity.MODERATE,
                observation="Rancangan kemasan etiket/dus belum menyediakan alokasi pencetakan 2D Barcode otentikasi BPOM.",
                legal_citation="PerBPOM No. 31/2018 jo. PerBPOM No. 22/2022",
                remediation_steps=[
                    "Tambahkan ruang cetak matriks 2D QR Code pada mock-up kemasan primer dan sekunder.",
                    "Pastikan font dan bahasa Indonesia pada brosur informasi pasien (PIL) telah memenuhi ketentuan."
                ]
            ))
        else:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-I-BARCODE",
                actd_part="Part_I",
                section="I.G",
                title="2D Barcode Penandaan BPOM",
                status=EvaluationStatus.PASS,
                severity=GapSeverity.COMPLIANT,
                observation="Penandaan kemasan telah mencakup spesifikasi 2D Barcode BPOM.",
                legal_citation="PerBPOM No. 31/2018",
                remediation_steps=[]
            ))

        # 3. Evaluate Climatic Zone Stability (Part II.C.11)
        stab = case.stability
        is_zone_ivb = ("ivb" in stab.climatic_zone.lower()) or ("30" in stab.real_time_temp_rh and "75" in stab.real_time_temp_rh)
        if not is_zone_ivb:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-II-STABILITY-ZONE",
                actd_part="Part_II",
                section="II.C.11",
                title="Stabilitas Zona Iklim Tropis IVb",
                status=EvaluationStatus.FAIL,
                severity=GapSeverity.CRITICAL,
                observation=f"Data stabilitas jangka panjang diuji pada {stab.climatic_zone} ({stab.real_time_temp_rh}). BPOM Indonesia mewajibkan Zona IVb (30°C ± 2°C / 75% ± 5% RH).",
                legal_citation="PerBPOM No. 24/2017 Lampiran 3 & ASEAN Stability Guidelines",
                remediation_steps=[
                    "SHOWSTOPPER GAP: BPOM menolak registrasi baru yang hanya mengandalkan data Zona II (25°C/60% RH).",
                    "Segera tempatkan bets pada climatic chamber Zona IVb (30°C/75% RH) dan uji dipercepat (40°C/75% RH).",
                    "Kumpulkan data real-time minimal 12 bulan dan dipercepat 6 bulan sebelum mengajukan berkas."
                ]
            ))
        elif stab.real_time_months < 12:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-II-STABILITY-DURATION",
                actd_part="Part_II",
                section="II.C.11",
                title="Durasi Data Stabilitas Real-Time Zona IVb",
                status=EvaluationStatus.FAIL,
                severity=GapSeverity.MAJOR,
                observation=f"Durasi data stabilitas riil baru {stab.real_time_months} bulan (minimal yang dipersyaratkan adalah 12 bulan).",
                legal_citation="Pedoman Stabilitas ASEAN BPOM",
                remediation_steps=[
                    "Tunggu hingga pengujian stabilitas bulan ke-12 selesai sebelum submit registrasi untuk menghindari penolakan atau PTD panjang."
                ]
            ))
        else:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-II-STABILITY-ZONE",
                actd_part="Part_II",
                section="II.C.11",
                title="Stabilitas Zona Iklim Tropis IVb",
                status=EvaluationStatus.PASS,
                severity=GapSeverity.COMPLIANT,
                observation=f"Data stabilitas memenuhi Zona IVb ({stab.real_time_temp_rh}) selama {stab.real_time_months} bulan.",
                legal_citation="PerBPOM No. 24/2017 Lampiran 3",
                remediation_steps=[]
            ))

        # 4. Evaluate Process Validation Batches (Part II.C.6)
        if case.manufacturing.validation_batches_count < 3:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-II-VALIDATION-BATCHES",
                actd_part="Part_II",
                section="II.C.6",
                title="Validasi Proses Manufaktur (Minimal 3 Bets)",
                status=EvaluationStatus.FAIL,
                severity=GapSeverity.MAJOR,
                observation=f"Laporan validasi proses baru mencakup {case.manufacturing.validation_batches_count} bets.",
                legal_citation="Pedoman CPOB 2018 Aneks 8",
                remediation_steps=[
                    "Lengkapi laporan validasi prospektif pada 3 bets komersial berturut-turut beserta protokol dan kriteria penerimaan."
                ]
            ))
        else:
            findings.append(GapFinding(
                rule_id="RULE-ACTD-II-VALIDATION-BATCHES",
                actd_part="Part_II",
                section="II.C.6",
                title="Validasi Proses Manufaktur (Minimal 3 Bets)",
                status=EvaluationStatus.PASS,
                severity=GapSeverity.COMPLIANT,
                observation=f"Telah melampirkan validasi proses pada {case.manufacturing.validation_batches_count} bets berturut-turut.",
                legal_citation="Pedoman CPOB 2018",
                remediation_steps=[]
            ))

        # 5. Evaluate Bioequivalence / Biowaiver (Part IV.C)
        is_oral_solid = any(term in case.dosage_form.lower() for term in ["tablet", "kapsul", "kaplet"])
        if is_oral_solid and case.is_generic_copy:
            if not case.be_study_completed and not (case.biowaiver_claimed and case.biowaiver_dissolution_f2_valid):
                findings.append(GapFinding(
                    rule_id="RULE-ACTD-IV-BE-STUDY",
                    actd_part="Part_IV",
                    section="IV.C",
                    title="Uji Bioekivalensi (BE) In Vivo / Biowaiver Valid",
                    status=EvaluationStatus.FAIL,
                    severity=GapSeverity.CRITICAL,
                    observation="Sediaan oral padat lepas cepat belum memiliki laporan Uji BE in vivo maupun Uji Disolusi Terbanding (UDT) biowaiver yang memenuhi syarat f2 >= 50.",
                    legal_citation="SK KaBPOM No. HK.00.05.3.1818 jo. Pedoman BE BPOM 2022",
                    remediation_steps=[
                        "Jika mengajukan Biowaiver (BCS Kelas I atau III): Lakukan Uji Disolusi Terbanding pada 3 media (pH 1.2, 4.5, 6.8) terhadap produk inovator resmi dengan f2 >= 50 atau disolusi >85% dalam 15 menit.",
                        "Jika tidak memenuhi kriteria biowaiver: Wajib menyelenggarakan uji Bioekivalensi in vivo di sentra uji BE terdaftar BPOM."
                    ]
                ))
            elif case.biowaiver_claimed and case.biowaiver_dissolution_f2_valid:
                findings.append(GapFinding(
                    rule_id="RULE-ACTD-IV-BE-STUDY",
                    actd_part="Part_IV",
                    section="IV.C",
                    title="BCS Biowaiver Uji Disolusi Terbanding",
                    status=EvaluationStatus.PASS,
                    severity=GapSeverity.COMPLIANT,
                    observation="Kriteria Biowaiver terpenuhi dengan justifikasi kelarutan tinggi dan profil disolusi terbanding f2 valid terhadap komparator.",
                    legal_citation="Pedoman BE BPOM 2022 & ICH M9",
                    remediation_steps=[]
                ))
            else:
                findings.append(GapFinding(
                    rule_id="RULE-ACTD-IV-BE-STUDY",
                    actd_part="Part_IV",
                    section="IV.C",
                    title="Uji Bioekivalensi In Vivo",
                    status=EvaluationStatus.PASS,
                    severity=GapSeverity.COMPLIANT,
                    observation="Laporan Uji Bioekivalensi in vivo lengkap memenuhi 90% CI (80.00% - 125.00%).",
                    legal_citation="SK KaBPOM HK.00.05.3.1818",
                    remediation_steps=[]
                ))

        # Calculate Scores
        total = len(findings)
        passed = sum(1 for f in findings if f.status == EvaluationStatus.PASS)
        failed = total - passed
        score = (passed / total) * 100.0 if total > 0 else 0.0

        crit_count = sum(1 for f in findings if f.severity == GapSeverity.CRITICAL and f.status != EvaluationStatus.PASS)
        maj_count = sum(1 for f in findings if f.severity == GapSeverity.MAJOR and f.status != EvaluationStatus.PASS)
        mod_count = sum(1 for f in findings if f.severity == GapSeverity.MODERATE and f.status != EvaluationStatus.PASS)

        if crit_count > 0:
            verdict = "TIDAK LAYAK SUBMIT (SHOWSTOPPER REJECTION RISK)"
            msg = f"Ditemukan {crit_count} gap kritikal (misal kestabilan bukan Zona IVb atau tiadanya BE). Registrasi dijamin ditolak jika diajukan saat ini."
        elif maj_count > 0:
            verdict = "RISIKO PTD TINGGI (MAJOR GAPS)"
            msg = f"Ditemukan {maj_count} gap mayor. Berkas akan memicu surat Permintaan Tambahan Data (PTD) dan risiko clock-stop."
        elif mod_count > 0:
            verdict = "PERBAIKAN MINOR (PTD RENDAH)"
            msg = f"Hanya terdapat {mod_count} catatan administratif minor yang dapat diperbaiki sebelum submission."
        else:
            verdict = "SIAP SUBMIT (COMPLIANT)"
            msg = "Berkas memenuhi seluruh parameter evaluasi teknis dasar BPOM."

        return DossierScorecard(
            product_name=case.product_name,
            total_checks=total,
            passed_checks=passed,
            failed_checks=failed,
            compliance_score_percent=round(score, 1),
            critical_count=crit_count,
            major_count=maj_count,
            moderate_count=mod_count,
            findings=findings,
            readiness_verdict=verdict,
            summary_message=msg
        )
