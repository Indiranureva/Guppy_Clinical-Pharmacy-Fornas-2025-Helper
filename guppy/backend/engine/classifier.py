"""Product Classification and Categorization Engine for BPOM Indonesia."""

from typing import Dict, Any, List
from guppy.backend.models.product import ProductCase


class ProductClassifier:
    """Executes deductive classification trees for pharmaceutical products,

    traditional medicines, supplements, and cosmetics according to Indonesian regulations.
    """

    KNOWN_NARCOTICS = {"morphine", "codeine", "fentanyl", "oxycodone", "pethidine", "methadone"}
    KNOWN_PSYCHOTROPICS = {"diazepam", "alprazolam", "lorazepam", "clobazam", "phenobarbital", "zolpidem"}
    KNOWN_ETHICAL_APIS = {
        "metformin", "amlodipine", "atorvastatin", "captopril", "amoxicillin", "ciprofloxacin",
        "azithromycin", "omeprazole", "lansoprazole", "losartan", "valsartan", "dexamethasone",
        "methylprednisolone", "ibuprofen 400", "ibuprofen 600", "ketoprofen"
    }

    @classmethod
    def classify(cls, case: ProductCase) -> Dict[str, Any]:
        """Classify a product into its regulatory category, symbol, legal basis, and BPOM category."""
        active_names = [ing.name.lower().strip() for ing in case.active_ingredients]
        route = case.route_of_administration.lower()
        form = case.dosage_form.lower()

        # 1. Check Narcotics & Psychotropics
        for name in active_names:
            if any(narc in name for narc in cls.KNOWN_NARCOTICS):
                return {
                    "category": "Narkotika",
                    "sub_category": "Obat Golongan Narkotika",
                    "symbol": "Palang Medali Merah",
                    "prescription_required": True,
                    "bpom_category": "Kategori 1 atau Kategori 2 (Jalur Khusus Narkotika)",
                    "legal_basis": "UU No. 35 Tahun 2009 jo. UU No. 17 Tahun 2023 tentang Kesehatan",
                    "distribution_channel": "Apotek & Rumah Sakit dengan Resep Dokter (SP Khusus)",
                    "rationale": f"Zat aktif '{name}' termasuk dalam daftar Narkotika Golongan II/III."
                }
            if any(psy in name for psy in cls.KNOWN_PSYCHOTROPICS):
                return {
                    "category": "Psikotropika",
                    "sub_category": "Obat Golongan Psikotropika",
                    "symbol": "Lingkaran Merah Huruf K (Obat Keras)",
                    "prescription_required": True,
                    "bpom_category": "Kategori 1 atau Kategori 2",
                    "legal_basis": "UU No. 5 Tahun 1997 jo. UU No. 17 Tahun 2023 tentang Kesehatan",
                    "distribution_channel": "Apotek & Fasilitas Pelayanan Kefarmasian dengan Resep Dokter",
                    "rationale": f"Zat aktif '{name}' berkhasiat psikoaktif pada susunan saraf pusat."
                }

        # 2. Check Natural Ingredients / Herbal Products (OBA)
        if any(term in name for name in active_names for term in ["extract", "ekstrak", "curcuma", "rimpang", "daun", "herba"]):
            # Differentiate Jamu vs OHT vs Fitofarmaka
            metadata = case.metadata or {}
            has_clinical = metadata.get("has_clinical_trials", False)
            has_standardized_preclinical = metadata.get("has_standardized_extract", False) and metadata.get("has_preclinical_trials", False)

            if has_clinical:
                return {
                    "category": "Obat Bahan Alam (OBA)",
                    "sub_category": "Fitofarmaka",
                    "symbol": "Kristal Salju / Jari-Jari Hijau di dalam Lingkaran",
                    "prescription_required": False,
                    "bpom_category": "Kategori Fitofarmaka (Registrasi OBA)",
                    "legal_basis": "Peraturan BPOM tentang Pendaftaran Obat Bahan Alam & Formularium Fitofarmaka Kemenkes",
                    "distribution_channel": "Dapat diresepkan dokter dan masuk Formularium Nasional",
                    "rationale": "Ekstrak terstandar yang telah dibuktikan keamanan dan khasiatnya melalui Uji Klinik pada manusia."
                }
            elif has_standardized_preclinical:
                return {
                    "category": "Obat Bahan Alam (OBA)",
                    "sub_category": "Obat Herbal Terstandar (OHT)",
                    "symbol": "Tiga Buah Bintang Hijau di dalam Lingkaran",
                    "prescription_required": False,
                    "bpom_category": "Kategori OHT (Registrasi OBA)",
                    "legal_basis": "Peraturan BPOM tentang Pendaftaran Obat Bahan Alam",
                    "distribution_channel": "Apotek, Toko Obat Berizin, Modern Market",
                    "rationale": "Ekstrak terstandar dengan dukungan data uji toksisitas dan farmakodinamik praklinik."
                }
            else:
                return {
                    "category": "Obat Bahan Alam (OBA)",
                    "sub_category": "Jamu",
                    "symbol": "Pohon / Ranting Daun Hijau di dalam Lingkaran",
                    "prescription_required": False,
                    "bpom_category": "Kategori Jamu (Registrasi OBA)",
                    "legal_basis": "Peraturan BPOM tentang Pendaftaran Obat Bahan Alam",
                    "distribution_channel": "Bebas beredar di masyarakat",
                    "rationale": "Bahan alam yang dibuktikan secara empiris turun-temurun minimal 3 generasi."
                }

        # 3. Check Health Supplements (Vitamins & Minerals threshold check)
        for ing in case.active_ingredients:
            ing_lower = ing.name.lower()
            if "vitamin c" in ing_lower or "ascorbic acid" in ing_lower:
                if ing.strength > 1000 and ing.unit.lower() == "mg":
                    return cls._build_ethical_drug_verdict(case, f"Vitamin C dengan dosis {ing.strength} mg melebihi batas suplemen kesehatan (maks 1000 mg/hari). Wajib didaftarkan sebagai Obat Keras.")
                elif route == "parenteral" or "injeksi" in form:
                    return cls._build_ethical_drug_verdict(case, "Vitamin C sediaan parenteral/injeksi diklasifikasikan sebagai Obat Keras.")
            if "vitamin d" in ing_lower or "cholecalciferol" in ing_lower:
                if ing.strength > 4000 and "iu" in ing.unit.lower():
                    return cls._build_ethical_drug_verdict(case, f"Vitamin D3 dengan dosis {ing.strength} IU melebihi batas suplemen (maks 4000 IU/hari). Wajib didaftarkan sebagai Obat Keras.")

        if "suplemen" in case.intended_indication.lower() or case.metadata.get("is_supplement_claim", False):
            return {
                "category": "Suplemen Kesehatan",
                "sub_category": "Suplemen Vitamin / Mineral / Nutrisi",
                "symbol": "Tidak menggunakan simbol lingkaran obat keras/bebas (Logo Suplemen Kesehatan)",
                "prescription_required": False,
                "bpom_category": "Registrasi Suplemen Kesehatan (Direktorat Registrasi OT, SK, dan Kosmetik)",
                "legal_basis": "Peraturan BPOM Batas Maksimum Vitamin dan Mineral dalam Suplemen Kesehatan",
                "distribution_channel": "Apotek, Toko Obat, Retail Komersial",
                "rationale": "Kandungan berada dalam rentang Angka Kecukupan Gizi / Batas Maksimum Asupan Harian BPOM."
            }

        # 4. Check Cosmetics (Topical for aesthetics)
        if route == "topikal" and any(term in case.intended_indication.lower() for term in ["mencerahkan", "melembabkan", "estetika", "kosmetik"]):
            return {
                "category": "Kosmetika",
                "sub_category": "Sediaan Perawatan Kulit (Skincare)",
                "symbol": "Nomor Notifikasi BPOM (NA + 11 digit)",
                "prescription_required": False,
                "bpom_category": "Notifikasi Kosmetika (Notifkos BPOM)",
                "legal_basis": "Peraturan BPOM tentang Persyaratan Teknis Kosmetika",
                "distribution_channel": "Bebas beredar di retail dan e-commerce",
                "rationale": "Ditujukan untuk bagian luar tubuh untuk membersihkan, merawat, dan memelihara penampilan luar tanpa klaim pengobatan sistemik."
            }

        # 5. Finished Pharmaceutical Drug (Obat Jadi)
        is_ethical = False
        for name in active_names:
            if any(eth in name for eth in cls.KNOWN_ETHICAL_APIS):
                is_ethical = True
                break

        if route in ["parenteral", "injeksi", "infus"] or is_ethical or case.is_new_chemical_entity:
            return cls._build_ethical_drug_verdict(case, "Mengandung entitas kimia aktif berpotensi tinggi atau rute parenteral yang memerlukan pengawasan medis.")

        # Default OTC check (Paracetamol standard dose, antacids)
        if any("paracetamol" in n for n in active_names):
            return {
                "category": "Obat Jadi",
                "sub_category": "Obat Bebas",
                "symbol": "Lingkaran Hijau Garis Tepi Hitam",
                "prescription_required": False,
                "bpom_category": "Kategori 2 (Obat Copy - Bebas)",
                "legal_basis": "Peraturan BPOM No. 24 Tahun 2017 jo. PerBPOM 13/2022",
                "distribution_channel": "Apotek, Toko Obat Berizin, Supermarket",
                "rationale": "Zat aktif dengan indeks terapi lebar dan rekam jejak keamanan tinggi untuk swamedikasi."
            }

        return {
            "category": "Obat Jadi",
            "sub_category": "Obat Bebas Terbatas",
            "symbol": "Lingkaran Biru Garis Tepi Hitam (Disertai Tanda Peringatan P.No. 1)",
            "prescription_required": False,
            "bpom_category": "Kategori 2 (Obat Copy Bebas Terbatas)",
            "legal_basis": "Peraturan BPOM No. 24 Tahun 2017 jo. SK Menkes Tanda Peringatan",
            "distribution_channel": "Apotek dan Toko Obat Berizin",
            "rationale": "Obat keras dengan batas kemasan tertentu yang dapat dijual bebas dengan peringatan resmi."
        }

    @classmethod
    def _build_ethical_drug_verdict(cls, case: ProductCase, rationale: str) -> Dict[str, Any]:
        bpom_cat = "Kategori 1 (Obat Baru)" if case.is_new_chemical_entity else "Kategori 2 / 3 (Obat Copy)"
        return {
            "category": "Obat Jadi",
            "sub_category": "Obat Keras (Ethical Drug)",
            "symbol": "Lingkaran Merah dengan Huruf K Hitam Menyentuh Garis Tepi",
            "prescription_required": True,
            "bpom_category": bpom_cat,
            "legal_basis": "UU No. 17 Tahun 2023 tentang Kesehatan jo. PerBPOM No. 24 Tahun 2017",
            "distribution_channel": "Hanya di Apotek, Rumah Sakit, dan Klinik dengan Resep Dokter",
            "rationale": rationale
        }
