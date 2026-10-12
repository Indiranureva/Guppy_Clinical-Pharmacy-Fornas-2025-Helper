"""Cross-Jurisdiction Regulatory Comparison Engine."""

from typing import Dict, List, Any


class JurisdictionComparator:
    """Benchmarks pharmaceutical requirements across BPOM (Indonesia), US FDA, EMA, and ICH."""

    TOPICS = {
        "stability": {
            "title": "Stabilitas Sediaan Obat Jadi (Finished Product Stability)",
            "rows": [
                {"param": "Zonasi Iklim (Climatic Zone)", "bpom": "Zona IVb (Hot & very humid)", "fda": "Zona I / II (Temperate)", "ema": "Zona I / II (Temperate)", "ich": "ICH Q1A(R2) harmonized"},
                {"param": "Kondisi Real-Time Long Term", "bpom": "30°C ± 2°C / 75% ± 5% RH", "fda": "25°C ± 2°C / 60% ± 5% RH (atau 30°C/65% RH)", "ema": "25°C ± 2°C / 60% ± 5% RH", "ich": "25°C/60% RH (Z-I/II) atau 30°C/75% RH (Z-IVb)"},
                {"param": "Kondisi Dipercepat (Accelerated)", "bpom": "40°C ± 2°C / 75% ± 5% RH", "fda": "40°C ± 2°C / 75% ± 5% RH", "ema": "40°C ± 2°C / 75% ± 5% RH", "ich": "40°C ± 2°C / 75% ± 5% RH"},
                {"param": "Minimal Data Riil Saat Filing", "bpom": "12 Bulan (Wajib Zona IVb)", "fda": "12 Bulan (Zona I/II)", "ema": "6 - 12 Bulan (Zona I/II)", "ich": "12 Bulan"},
                {"param": "Format Dossier", "bpom": "ACTD Part II.C.11", "fda": "eCTD Module 3 (3.2.P.8)", "ema": "eCTD Module 3 (3.2.P.8)", "ich": "CTD M4Q 3.2.P.8"}
            ],
            "impact_analysis": "Data stabilitas global Zona II tidak dapat digunakan untuk registrasi BPOM. Industri multinasional wajib menjalankan pengujian Zona IVb terpisah untuk pasar Indonesia."
        },
        "nitrosamines": {
            "title": "Pengendalian Cemaran Nitrosamin (Mutagenic Impurities)",
            "rows": [
                {"param": "Regulasi Rujukan", "bpom": "Surat Edaran BPOM No. PW.01.07.3.34.05.21.32", "fda": "FDA Guidance: Control of Nitrosamine Impurities in Human Drugs", "ema": "EMA/409815/2020 Q&A on Nitrosamines", "ich": "ICH M7(R2) Mutagenic Impurities"},
                {"param": "Default Acceptable Intake (AI)", "bpom": "26.5 ng/hari (TTC group-specific)", "fda": "26.5 ng/hari (TTC limit)", "ema": "26.5 ng/hari (TTC limit)", "ich": "1.5 mcg/hari umum; 26.5 ng/hari cohort of concern"},
                {"param": "Kewajiban Pengkajian Risiko", "bpom": "Wajib untuk semua API sintetis pada registrasi baru", "fda": "Step 1 Risk Assessment + Step 2 Confirmatory Testing", "ema": "Step 1, 2, 3 Call for Review", "ich": "Prinsip risk assessment terintegrasi di CMC"}
            ],
            "impact_analysis": "BPOM mengadopsi ambang batas nitrosamin yang harmonis dengan FDA dan EMA, namun memerlukan pernyataan komitmen pengujian rutin yang diunggah pada Bagian II.B dan II.C ACTD."
        },
        "bioequivalence": {
            "title": "Bioekivalensi (BE) & BCS Biowaiver",
            "rows": [
                {"param": "Rentang Kriteria BE", "bpom": "90% CI: 80.00% - 125.00% (AUC & Cmax)", "fda": "90% CI: 80.00% - 125.00%", "ema": "90% CI: 80.00% - 125.00% (NTI: 90.00% - 111.11%)", "ich": "ICH M13A (Harmonisasi 80-125%)"},
                {"param": "Kelayakan Biowaiver", "bpom": "BCS Kelas I dan Kelas III (Disolusi sangat cepat >85% 15 mnt)", "fda": "BCS Kelas I dan Kelas III", "ema": "BCS Kelas I dan Kelas III (ekspien ketat)", "ich": "ICH M9 Biopharmaceutics Classification"},
                {"param": "Media Disolusi Terbanding", "bpom": "pH 1.2, pH 4.5, pH 6.8 (37°C)", "fda": "pH 1.2, pH 4.5, pH 6.8", "ema": "pH 1.2, pH 4.5, pH 6.8", "ich": "pH 1.2, pH 4.5, pH 6.8"}
            ],
            "impact_analysis": "Ketentuan Biowaiver BPOM selaras dengan ICH M9. Untuk BCS Kelas III, eksipien tidak boleh mempengaruhi motilitas saluran cerna."
        },
        "dossier_format": {
            "title": "Format Dossier & Struktur Pengajuan",
            "rows": [
                {"param": "Struktur Dokumen", "bpom": "ACTD (4 Parts)", "fda": "ICH eCTD (5 Modules)", "ema": "ICH eCTD (5 Modules)", "ich": "ICH CTD (5 Modules)"},
                {"param": "Sistem Portal Pendaftaran", "bpom": "ASROT (e-Registration BPOM)", "fda": "ESG (Electronic Submissions Gateway)", "ema": "CESP / IRIS Gateway", "ich": "Electronic Common Technical Document specs"},
                {"param": "Bahasa Penandaan & PIL", "bpom": "Bahasa Indonesia Resmi", "fda": "English (USPI)", "ema": "Official Member State Languages (SmPC/PIL)", "ich": "Regional competence"}
            ],
            "impact_analysis": "Dossier global CTD Module 2 harus didekonstruksi dan dipindahkan ke dalam masing-masing Part ACTD (misal Module 2.3 QOS dipindahkan ke Part II.A)."
        }
    }

    @classmethod
    def get_comparison(cls, topic_key: str) -> Dict[str, Any]:
        """Retrieve structured comparison data for a given regulatory domain."""
        return cls.TOPICS.get(topic_key, cls.TOPICS["stability"])

    @classmethod
    def list_available_topics(cls) -> List[Dict[str, str]]:
        return [
            {"key": k, "title": v["title"]}
            for k, v in cls.TOPICS.items()
        ]
