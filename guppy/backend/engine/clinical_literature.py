"""Clinical Literature Scout — Evidence Justification for Fornas Restriction Adaptation.

Provides peer-reviewed scientific justification when a patient's clinical condition
requires consideration beyond standard Fornas restrictions (e.g., off-label use,
renal dose adjustment, geriatrics, or line-of-therapy adaptation).

Features:
- Routine curated article repository (Scopus Q1–Q3, PubMed, Lancet, NEJM, JAMA, KDIGO, ESC).
- Deep search engine across topic metadata, synonyms, and article body texts.
- Bilingual Indonesian-English drug name synonym mapping.
- Multi-article selection per clinical topic (Guppy Primary Recommendation + Supporting Studies).
- Interactive selection by user (pharmacist/clinician).
- Automated Clinical Justification Memo generator for Hospital Pharmacy & Therapeutics Committee (KFT) / BPJS.
- Smart Universal Justification Fallback for any drug in the national formulary.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class ClinicalLiteratureScout:
    """Clinical evidence repository and justification memo engine for Fornas adaptations."""

    CURATION_VERSION = "Kurasi Rutin Guppy Q4-2026 (Update Berkala Terverifikasi)"

    # Kamus sinonim bilingual (Indonesia <-> INN/Inggris & nama dagang umum)
    DRUG_SYNONYMS: Dict[str, List[str]] = {
        "seftriakson": ["ceftriaxone", "rocephin"],
        "ceftriaxone": ["seftriakson", "rocephin"],
        "amoksisilin": ["amoxicillin", "amoxil"],
        "amoxicillin": ["amoksisilin", "amoxil"],
        "parasetamol": ["paracetamol", "acetaminophen", "sanmol", "panadol"],
        "paracetamol": ["parasetamol", "acetaminophen"],
        "lansoprazol": ["lansoprazole", "prosogan"],
        "lansoprazole": ["lansoprazol"],
        "omeprazol": ["omeprazole", "losec"],
        "omeprazole": ["omeprazol"],
        "esomeprazol": ["esomeprazole", "nexium"],
        "esomeprazole": ["esomeprazol"],
        "kandesartan": ["candesartan", "blopress"],
        "candesartan": ["kandesartan"],
        "valsartan": ["diovan"],
        "ramipril": ["triatec"],
        "kaptopril": ["captopril"],
        "captopril": ["kaptopril"],
        "deksametason": ["dexamethasone", "kalmethasone"],
        "dexamethasone": ["deksametason"],
        "metilprednisolon": ["methylprednisolone", "medixon", "urbason"],
        "methylprednisolone": ["metilprednisolon"],
        "prednison": ["prednisone"],
        "prednisone": ["prednison"],
        "gliklazid": ["gliclazide", "diamicron"],
        "gliclazide": ["gliklazid"],
        "glimepirid": ["glimepiride", "amaryl"],
        "glimepiride": ["glimepirid"],
        "glibenklamid": ["glibenclamide", "daonil"],
        "glibenclamide": ["glibenklamid"],
        "spironolakton": ["spironolactone", "aldactone"],
        "spironolactone": ["spironolakton"],
        "furosemid": ["furosemide", "lasix"],
        "furosemide": ["furosemid"],
        "klopidogrel": ["clopidogrel", "plavix"],
        "clopidogrel": ["klopidogrel"],
        "aspirin": ["asetosal", "aspilets", "thrombo"],
        "asetosal": ["aspirin", "aspilets"],
        "simvastatin": ["simvastatin", "zocor"],
        "atorvastatin": ["atorvastatin", "lipitor"],
        "rosuvastatin": ["crestor"],
        "siprofloksasin": ["ciprofloxacin", "baquinor"],
        "ciprofloxacin": ["siprofloksasin"],
        "levofloksasin": ["levofloxacin", "cravit"],
        "levofloxacin": ["levofloksasin"],
        "azitromisin": ["azithromycin", "zithromax"],
        "azithromycin": ["azitromisin"],
        "gentamisin": ["gentamicin"],
        "gentamicin": ["gentamisin"],
        "sefiksim": ["cefixime", "cepanat"],
        "cefixime": ["sefiksim"],
        "warfarin": ["simarc", "coumadin"],
        "ketorolak": ["ketorolac"],
        "ketorolac": ["ketorolak"],
        "tramadol": ["tramadol", "centrasic"],
        "metformin": ["glucophage"],
        "amlodipin": ["amlodipine", "norvask"],
        "amlodipine": ["amlodipin", "norvask"],
        "setirizin": ["cetirizine", "incidal"],
        "cetirizine": ["setirizin", "incidal"],
        "ibuprofen": ["proris"],
        "asam mefenamat": ["mefenamic acid", "ponstan"],
        "mefenamic acid": ["asam mefenamat", "ponstan"],
        "metoklopramid": ["metoclopramide", "primperan"],
        "ondansetron": ["narfoz", "cedantron"],
        "ranitidin": ["ranitidine", "zantac"],
        "salbutamol": ["ventolin"],
        "budesonid": ["budesonide", "pulmicort"],
        "tiotropium": ["spiriva"],
        "gabapentin": ["neurontin"],
        "pregabalin": ["lyrica"],
        "digoksin": ["digoxin", "fargoxin"],
        "allopurinol": ["alopurinol", "zyloric"],
        "alopurinol": ["allopurinol", "zyloric"],
    }

    CURATED_TOPICS: List[Dict[str, Any]] = [
        {
            "topic_id": "metformin_ckd_egfr",
            "title": "Keamanan Metformin pada DMT2 dengan Penurunan Fungsi Ginjal (CKD)",
            "category": "Endokrinologi & Nefrologi",
            "drug_inn": "Metformin",
            "clinical_problem": (
                "Pasien DMT2 dengan penurunan fungsi ginjal (eGFR 30–60 mL/mnt/1.73m² / CKD Derajat 3) "
                "membutuhkan kontrol glikemik, namun sering kali dihentikan prematur karena kekhawatiran "
                "laktat asidosis atau restriksi baku Fornas."
            ),
            "fornas_rule": "Fornas membatasi metformin pada gagal ginjal (kontraindikasi mutlak eGFR < 30 mL/menit).",
            "keywords": ["metformin", "ckd", "ginjal", "egfr", "creatinine", "renal", "lactic acidosis", "diabetes", "glucophage"],
            "articles": [
                {
                    "article_id": "metformin_lipska_2011",
                    "is_primary": True,
                    "citation": {
                        "authors": "Lipska, K. J., Bailey, C. J., Inzucchi, S. E.",
                        "year": 2011,
                        "title": "Use of Metformin in the Setting of Mild-to-Moderate Renal Insufficiency",
                        "journal": "Diabetes Care",
                        "volume_issue": "Vol. 34(6), pp. 1431–1437",
                        "quartile": "Scopus Q1 / IF ~17",
                        "study_type": "Systematic Review & Clinical Cohort",
                        "doi": "10.2337/dc10-2361",
                        "pmid": "21617112",
                    },
                    "clinical_finding": (
                        "Metformin dapat digunakan dengan aman pada pasien DMT2 dengan eGFR 30–60 mL/mnt/1.73m² "
                        "(CKD Derajat 3a-3b) dengan penyesuaian dosis (maksimal 1000 mg/hari) dan pemantauan "
                        "fungsi ginjal berkala setiap 3–6 bulan. Insiden laktat asidosis sangat rendah (< 10 per "
                        "100.000 pasien-tahun) dan sebanding dengan terapi antidiabetik oral lainnya."
                    ),
                    "fornas_implication": (
                        "Mendukung justifikasi kelanjutan terapi metformin pada CKD 3a-3b dengan reduksi dosis 50%, "
                        "mencegah hiperglikemia akibat penghentian mendadak obat lini pertama."
                    ),
                },
                {
                    "article_id": "metformin_inzucchi_2014",
                    "is_primary": False,
                    "citation": {
                        "authors": "Inzucchi, S. E., Lipska, K. J., Mayo, H., et al.",
                        "year": 2014,
                        "title": "Metformin in Patients With Type 2 Diabetes and Kidney Disease: A Systematic Review",
                        "journal": "JAMA",
                        "volume_issue": "Vol. 312(24), pp. 2668–2675",
                        "quartile": "Scopus Q1 / IF ~157",
                        "study_type": "Systematic Review & Meta-Analysis (65 Studi)",
                        "doi": "10.1001/jama.2014.15298",
                        "pmid": "25536168",
                    },
                    "clinical_finding": (
                        "Telaah sistematis 65 studi membuktikan bahwa metformin berhubungan dengan penurunan "
                        "mortalitas semua penyebab pada pasien DMT2 dengan gangguan ginjal ringan hingga sedang "
                        "tanpa peningkatan bermakna kejadian laktat asidosis fatal."
                    ),
                    "fornas_implication": (
                        "Bukti level meta-analisis bagi Komite Farmasi & Terapi (KFT) bahwa proteksi kardiovaskular "
                        "metformin tetap bermanfaat pada eGFR > 30 mL/menit bila dipantau dengan tepat."
                    ),
                },
                {
                    "article_id": "metformin_kdigo_2022",
                    "is_primary": False,
                    "citation": {
                        "authors": "de Boer, I. H., Khunti, K., Sadusky, T., et al. (KDIGO Work Group)",
                        "year": 2022,
                        "title": "Executive summary of the KDIGO 2022 Clinical Practice Guideline for Diabetes Management in CKD",
                        "journal": "Kidney International",
                        "volume_issue": "Vol. 102(5), pp. 974–989",
                        "quartile": "Scopus Q1 / IF ~19.6",
                        "study_type": "International Clinical Practice Guideline",
                        "doi": "10.1016/j.kint.2022.06.013",
                        "pmid": "36272753",
                    },
                    "clinical_finding": (
                        "Rekomendasi 1.3 KDIGO: Lini pertama terapi glikemik pasien DMT2 dengan CKD adalah kombinasi "
                        "Metformin + SGLT2i. Dosis metformin dititrasi: eGFR 45–59 mL/mnt maks 2000 mg/hari; "
                        "eGFR 30–44 mL/mnt maks 1000 mg/hari; hentikan hanya bila eGFR < 30 mL/mnt."
                    ),
                    "fornas_implication": (
                        "Pedoman konsensus global terkini yang selaras dengan adaptasi restriksi Fornas: aman dipakai "
                        "pada eGFR 30–60 dengan protokol penyesuaian dosis terdokumentasi."
                    ),
                },
            ],
        },
        {
            "topic_id": "statin_elderly",
            "title": "Manfaat & Keamanan Statin pada Geriatri (>75 Tahun) dengan Dislipidemia",
            "category": "Kardiovaskular & Geriatri",
            "drug_inn": "Simvastatin / Atorvastatin",
            "clinical_problem": (
                "Kekhawatiran efek samping miopati atau rabdomiolisis sering memicu penghentian statin pada pasien lanjut usia "
                "(>75 tahun), atau sebaliknya peresepan dosis tinggi simvastatin (80 mg) yang berisiko tinggi."
            ),
            "fornas_rule": "Fornas membatasi simvastatin pada dosis maksimal 40 mg/hari dan atorvastatin pada indikasi risiko tinggi.",
            "keywords": ["statin", "elderly", "lansia", "atorvastatin", "simvastatin", "myopathy", "rhabdomyolysis", "cardiovascular", "lipitor", "zocor"],
            "articles": [
                {
                    "article_id": "statin_ctt_lancet_2019",
                    "is_primary": True,
                    "citation": {
                        "authors": "Cholesterol Treatment Trialists' (CTT) Collaboration",
                        "year": 2019,
                        "title": "Efficacy and safety of statin therapy in older people: a meta-analysis of individual participant data",
                        "journal": "The Lancet",
                        "volume_issue": "Vol. 393(10170), pp. 407–415",
                        "quartile": "Scopus Q1 / IF ~202",
                        "study_type": "Individual Participant Data Meta-Analysis (28 RCT, 186.854 pasien)",
                        "doi": "10.1016/S0140-6736(18)31942-1",
                        "pmid": "30712900",
                    },
                    "clinical_finding": (
                        "Statin secara signifikan mengurangi risiko kejadian kardiovaskular mayor (MACE) pada lansia >75 tahun "
                        "(RR 0.82 per 1 mmol/L penurunan LDL-C) dengan tolerabilitas tinggi. Risiko miopati atau rabdomiolisis "
                        "sangat jarang pada dosis standar. Namun, Simvastatin 80 mg tidak disarankan karena lonjakan risiko toksisitas otot."
                    ),
                    "fornas_implication": (
                        "Mendukung restriksi Fornas yang membatasi Simvastatin maksimal 40 mg/hari. Pada lansia risiko tinggi yang gagal "
                        "mencapai target dengan simvastatin 40 mg, alih ke Atorvastatin 20 mg didukung kuat secara ilmiah."
                    ),
                },
                {
                    "article_id": "statin_esc_eas_2020",
                    "is_primary": False,
                    "citation": {
                        "authors": "Mach, F., Baigent, C., Catapano, A. L., et al. (ESC/EAS Task Force)",
                        "year": 2020,
                        "title": "2019 ESC/EAS Guidelines for the management of dyslipidaemias: lipid modification to reduce cardiovascular risk",
                        "journal": "European Heart Journal",
                        "volume_issue": "Vol. 41(1), pp. 111–188",
                        "quartile": "Scopus Q1 / IF ~39.3",
                        "study_type": "International Consensus Guideline",
                        "doi": "10.1093/eurheartj/ehz455",
                        "pmid": "31504418",
                    },
                    "clinical_finding": (
                        "Rekomendasi Kelas I: Terapi statin diindikasikan untuk lansia dengan ASCVD (pencegahan sekunder) sama seperti "
                        "pasien yang lebih muda. Memulai dosis rendah dan titrasi bertahap direkomendasikan pada gangguan fungsi ginjal atau potensi interaksi obat."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi peresepan Atorvastatin untuk pasien lansia pasca-stroke/infark miokard di FKRTL sebagai pencegahan sekunder."
                    ),
                },
                {
                    "article_id": "statin_orkaby_jama_2020",
                    "is_primary": False,
                    "citation": {
                        "authors": "Orkaby, A. R., Driver, J. A., Ho, Y. L., et al.",
                        "year": 2020,
                        "title": "Association of Statin Therapy With Mortality in Older Veterans Without Prior Cardiovascular Events",
                        "journal": "JAMA",
                        "volume_issue": "Vol. 324(1), pp. 68–78",
                        "quartile": "Scopus Q1 / IF ~157",
                        "study_type": "Retrospective Cohort Study (>120.000 lansia)",
                        "doi": "10.1001/jama.2020.7848",
                        "pmid": "32634248",
                    },
                    "clinical_finding": (
                        "Penggunaan statin pada lansia usia ≥ 75 tahun berhubungan bermakna dengan penurunan 25% risiko mortalitas semua "
                        "penyebab (HR 0.75, 95% CI 0.74–0.76) dan 20% penurunan mortalitas kardiovaskular."
                    ),
                    "fornas_implication": (
                        "Menegaskan keselamatan jangka panjang statin pada geriatri dan mencegah under-prescribing pada kelompok lansia."
                    ),
                },
            ],
        },
        {
            "topic_id": "ppi_deprescribing",
            "title": "Deprescribing PPI Jangka Panjang & Evaluasi Rasionalitas Terapi Gastrointestinal",
            "category": "Gastroenterologi",
            "drug_inn": "Omeprazole / Lansoprazole / Esomeprazole",
            "clinical_problem": (
                "Penggunaan Proton Pump Inhibitor (PPI) berkepanjangan tanpa indikasi objektif atau tanpa batas waktu evaluasi "
                "meningkatkan risiko infeksi C. difficile, hipomagnesemia, fraktur tulang, dan inefisiensi biaya klaim JKN."
            ),
            "fornas_rule": "Fornas membatasi durasi peresepan maksimal PPI (maksimal 4-8 minggu berturut-turut pada GERD/dispepsia tanpa komplikasi).",
            "keywords": ["omeprazole", "lansoprazole", "esomeprazole", "omeprazol", "lansoprazol", "esomeprazol", "ppi", "deprescribing", "gerd", "long-term", "proton pump inhibitor", "withdrawal", "losec", "nexium", "prosogan"],
            "articles": [
                {
                    "article_id": "ppi_farrell_2017",
                    "is_primary": True,
                    "citation": {
                        "authors": "Farrell, B., Pottie, K., Thompson, W., et al.",
                        "year": 2017,
                        "title": "Deprescribing proton pump inhibitors: Evidence-based clinical practice guideline",
                        "journal": "Canadian Family Physician",
                        "volume_issue": "Vol. 63(5), pp. 354–364",
                        "quartile": "Scopus Q2 / MEDLINE Indexed",
                        "study_type": "Evidence-Based Clinical Practice Guideline",
                        "doi": "PMC5429073",
                        "pmid": "28500294",
                    },
                    "clinical_finding": (
                        "Pada pasien dewasa yang telah menjalani terapi PPI selama minimal 4-8 minggu untuk GERD atau esofagitis ringan "
                        "dan gejalanya telah terkontrol, deprescribing (penurunan dosis, beralih ke PRN, atau penghentian bertahap) "
                        "berhasil pada 70–80% pasien tanpa rebound gejala yang merugikan."
                    ),
                    "fornas_implication": (
                        "Mendukung audit restriksi Fornas 2025: PPI wajib dievaluasi setiap 4-8 minggu. Mengarahkan pasien non-komplikasi "
                        "ke antasida atau H2-blocker untuk terapi pemeliharaan rasional."
                    ),
                },
                {
                    "article_id": "ppi_moayyedi_2019",
                    "is_primary": False,
                    "citation": {
                        "authors": "Moayyedi, P., Eikelboom, J. W., Bosch, J., et al. (COMPASS Trial Investigators)",
                        "year": 2019,
                        "title": "Safety of Proton Pump Inhibitors Based on a Large, Multi-Year, Randomized Trial (COMPASS Trial)",
                        "journal": "Gastroenterology",
                        "volume_issue": "Vol. 157(3), pp. 682–691",
                        "quartile": "Scopus Q1 / IF ~29.4",
                        "study_type": "Large Double-Blind Randomized Controlled Trial (17.598 Pasien)",
                        "doi": "10.1053/j.gastro.2019.05.056",
                        "pmid": "31163151",
                    },
                    "clinical_finding": (
                        "Uji klinis acak berskala besar menunjukkan pantoprazole aman digunakan jangka panjang bila ada indikasi kuat "
                        "(seperti pencegahan perdarahan GI pada antikoagulan), namun infeksi enterik (C. difficile) tetap meningkat signifikan "
                        "(OR 1.84, p=0.015). Penggunaan tanpa indikasi kuat tidak dapat dibenarkan."
                    ),
                    "fornas_implication": (
                        "Sebagai acuan pemilah: PPI jangka panjang hanya dijustifikasi jika ada komedikasi antitrombotik/NSAID risiko tinggi."
                    ),
                },
                {
                    "article_id": "ppi_aga_guideline_2023",
                    "is_primary": False,
                    "citation": {
                        "authors": "Targownik, L. E., Fisher, D. A., Saini, S. D. (AGA Institute)",
                        "year": 2022,
                        "title": "AGA Clinical Practice Update on De-Prescribing of Proton Pump Inhibitors: Best Practice Advice",
                        "journal": "Gastroenterology",
                        "volume_issue": "Vol. 162(4), pp. 1334–1342",
                        "quartile": "Scopus Q1 / IF ~29.4",
                        "study_type": "Clinical Practice Expert Consensus",
                        "doi": "10.1053/j.gastro.2021.12.247",
                        "pmid": "35183361",
                    },
                    "clinical_finding": (
                        "Seluruh pasien yang menggunakan PPI jangka panjang harus memiliki dokumentasi indikasi medis yang jelas. "
                        "Percobaan de-prescribing harus ditawarkan secara rutin setahun sekali bagi pasien GERD tanpa esofagitis erosif berat (Los Angeles C/D) atau Barrett's Esophagus."
                    ),
                    "fornas_implication": (
                        "Dasar penyusunan SOP audit obat PPI di instalasi farmasi RS untuk menolak klaim berulang yang tidak rasional."
                    ),
                },
            ],
        },
        {
            "topic_id": "clopidogrel_dapt_post_pci",
            "title": "Dual Antiplatelet Therapy (DAPT): Clopidogrel + Aspirin Pasca-PCI & Sindrom Koroner Akut",
            "category": "Kardiologi & Hemostatis",
            "drug_inn": "Clopidogrel / Aspirin",
            "clinical_problem": (
                "Peresepan DAPT (Clopidogrel + Aspirin/Asetosal) memerlukan justifikasi klinis tertulis ketika durasi peresepan "
                "melebihi batas baku 12 bulan pada pasien dengan risiko trombosis stent tinggi, atau bila terjadi resistensi/alergi aspirin."
            ),
            "fornas_rule": "Fornas membatasi klopidogrel maksimal 12 bulan pasca-PCI/ACS, kecuali ada rekomendasi tertulis Sp.JP.",
            "keywords": ["clopidogrel", "klopidogrel", "aspirin", "asetosal", "plavix", "aspilets", "thrombo", "pci", "stent", "dapt", "acs", "infark"],
            "articles": [
                {
                    "article_id": "clopidogrel_cure_trial_2001",
                    "is_primary": True,
                    "citation": {
                        "authors": "Yusuf, S., Zhao, F., Mehta, S. R., et al. (CURE Trial Investigators)",
                        "year": 2001,
                        "title": "Effects of clopidogrel in addition to aspirin in patients with acute coronary syndromes without ST-segment elevation",
                        "journal": "New England Journal of Medicine",
                        "volume_issue": "Vol. 345(7), pp. 494–502",
                        "quartile": "Scopus Q1 / IF ~176",
                        "study_type": "Randomized Double-Blind Placebo-Controlled Trial (12.562 Pasien)",
                        "doi": "10.1056/NEJMoa010746",
                        "pmid": "11519503",
                    },
                    "clinical_finding": (
                        "Penambahan clopidogrel pada aspirin menurunkan kejadian kematian kardiovaskular, infark miokard, atau stroke "
                        "sebesar 20% (9.3% vs 11.4%, RR 0.80, p<0.001) pada pasien ACS, menetapkan DAPT sebagai pilar proteksi antitrombotik."
                    ),
                    "fornas_implication": (
                        "Mendukung ketentuan Fornas mengenai jaminan penuh klopidogrel 75 mg/hari pasca-ACS hingga 12 bulan."
                    ),
                },
                {
                    "article_id": "clopidogrel_esc_dapt_2018",
                    "is_primary": False,
                    "citation": {
                        "authors": "Valgimigli, M., Bueno, H., Byrne, R. A., et al. (ESC Scientific Document Group)",
                        "year": 2018,
                        "title": "2017 ESC focused update on dual antiplatelet therapy in coronary artery disease",
                        "journal": "European Heart Journal",
                        "volume_issue": "Vol. 39(3), pp. 213–260",
                        "quartile": "Scopus Q1 / IF ~39.3",
                        "study_type": "International Consensus Practice Guideline",
                        "doi": "10.1093/eurheartj/ehx419",
                        "pmid": "28854649",
                    },
                    "clinical_finding": (
                        "Pada pasien risiko iskemik tinggi (bifurkasi stent, riwayat trombosis stent, DM) dengan risiko perdarahan rendah "
                        "(PRECISE-DAPT score < 25), perpanjangan DAPT > 12 bulan menghasilkan reduksi infark berulang yang bermakna."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi resmi KFT untuk memperpanjang klopidogrel melampaui 12 bulan bila dinilai Sp.JP berisiko tinggi."
                    ),
                },
            ],
        },
        {
            "topic_id": "corticosteroid_tapering_safety",
            "title": "Protokol Penggunaan & Tapering Off Kortikosteroid Sistemik (Metilprednisolon / Deksametason)",
            "category": "Imunologi & Pulmonologi",
            "drug_inn": "Methylprednisolone / Dexamethasone",
            "clinical_problem": (
                "Penggunaan kortikosteroid sistemik jangka panjang tanpa jadwal tapering-off yang jelas memicu supresi aksis HPA "
                "(insufisiensi adrenal akut saat dihentikan), sindrom Cushing iatrogenik, osteoporosis, dan lonjakan gula darah berat."
            ),
            "fornas_rule": "Fornas membatasi durasi peresepan kortikosteroid oral dan mensyaratkan peresepan oleh spesialis untuk penyakit autoimun.",
            "keywords": ["methylprednisolone", "metilprednisolon", "dexamethasone", "deksametason", "prednisone", "prednison", "steroid", "corticosteroid", "tapering", "autoimun", "medixon", "kalmethasone"],
            "articles": [
                {
                    "article_id": "steroid_recovery_nejm_2021",
                    "is_primary": True,
                    "citation": {
                        "authors": "RECOVERY Collaborative Group (Horby, P., et al.)",
                        "year": 2021,
                        "title": "Dexamethasone in Hospitalized Patients with Covid-19 and Severe Respiratory Failure",
                        "journal": "New England Journal of Medicine",
                        "volume_issue": "Vol. 384(8), pp. 693–704",
                        "quartile": "Scopus Q1 / IF ~176",
                        "study_type": "Pragmatic Randomized Controlled Trial (6.425 Pasien)",
                        "doi": "10.1056/NEJMoa2021436",
                        "pmid": "32678530",
                    },
                    "clinical_finding": (
                        "Pemberian deksametason dosis sedang (6 mg/hari selama maksimal 10 hari) secara signifikan memangkas mortalitas 28 hari "
                        "pada pasien dengan gagal napas yang membutuhkan suplementasi oksigen, tanpa komplikasi supresi adrenal berkepanjangan."
                    ),
                    "fornas_implication": (
                        "Mendukung pembatasan durasi kortikosteroid dosis tinggi maksimal 7-10 hari pada fase inflamasi akut berat."
                    ),
                },
                {
                    "article_id": "steroid_adrenal_endotext_2020",
                    "is_primary": False,
                    "citation": {
                        "authors": "Diri, H., Karaca, Z., Tanriverdi, F., Unluhizarci, K., Kelestimur, F.",
                        "year": 2020,
                        "title": "Recovery of Hypothalamic-Pituitary-Adrenal Axis After Glucocorticoid Withdrawal",
                        "journal": "The Journal of Clinical Endocrinology & Metabolism",
                        "volume_issue": "Vol. 105(6), pp. 1902–1914",
                        "quartile": "Scopus Q1 / IF ~5.8",
                        "study_type": "Systematic Review & Clinical Protocol",
                        "doi": "10.1210/clinem/dgaa124",
                        "pmid": "32168340",
                    },
                    "clinical_finding": (
                        "Penggunaan glukokortikoid ekuivalen prednison ≥ 20 mg/hari selama > 3 minggu wajib melalui protokol penurunan dosis "
                        "bertahap (tapering off 10-20% setiap 1-2 minggu) untuk memungkinkan pemulihan aksis HPA dan mencegah krisis adrenal."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi farmasis menyusun jadwal tapering off tertulis pada resep metilprednisolon rawat jalan."
                    ),
                },
            ],
        },
        {
            "topic_id": "candesartan_arb_acei_cough",
            "title": "Substitusi Terapi ARB (Kandesartan / Valsartan) pada Kasus Intoleransi Batuk Kering ACE-Inhibitor",
            "category": "Kardiologi & Hipertensi",
            "drug_inn": "Candesartan / Valsartan",
            "clinical_problem": (
                "Sebanyak 10-20% pasien hipertensi atau gagal jantung yang menerima kaptopril/ramipril mengalami batuk kering persisten "
                "(bradikinin-induced cough) yang menurunkan kepatuhan, sehingga membutuhkan alih terapi ke golongan ARB."
            ),
            "fornas_rule": "Fornas menjamin ARB (Kandesartan) untuk hipertensi dan gagal jantung bila pasien intoleran terhadap ACEI.",
            "keywords": ["candesartan", "kandesartan", "valsartan", "captopril", "kaptopril", "ramipril", "arb", "acei", "batuk", "cough", "intolerance", "blopress", "diovan"],
            "articles": [
                {
                    "article_id": "candesartan_charm_lancet_2003",
                    "is_primary": True,
                    "citation": {
                        "authors": "Granger, C. B., McMurray, J. J., Yusuf, S., et al. (CHARM Investigators)",
                        "year": 2003,
                        "title": "Effects of candesartan in patients with chronic heart failure and reduced left-ventricular systolic function intolerant to ACE inhibitors: the CHARM-Alternative trial",
                        "journal": "The Lancet",
                        "volume_issue": "Vol. 362(9386), pp. 772–776",
                        "quartile": "Scopus Q1 / IF ~202",
                        "study_type": "Double-Blind Randomized Controlled Trial (2.028 Pasien)",
                        "doi": "10.1016/S0140-6736(03)14284-5",
                        "pmid": "13678870",
                    },
                    "clinical_finding": (
                        "Pada pasien gagal jantung/hipertensi yang intoleran ACE-inhibitor karena batuk, pemberian kandesartan (titrasi target 32 mg/hari) "
                        "menurunkan mortalitas kardiovaskular atau rawat inap gagal jantung sebesar 23% (p<0.001) dengan tingkat rekurensi batuk sangat rendah (<1%)."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi utama peresepan Kandesartan di FKTP dan FKRTL: bukti bahwa batuk intoleran ACEI merupakan indikasi sah pengalihan ke ARB."
                    ),
                },
                {
                    "article_id": "candesartan_pnpk_kemenkes_2020",
                    "is_primary": False,
                    "citation": {
                        "authors": "Komite Nasional Pedoman Pelayanan Kedokteran (Kemenkes RI)",
                        "year": 2020,
                        "title": "Pedoman Nasional Pelayanan Kedokteran Tata Laksana Hipertensi Dewasa",
                        "journal": "Kepmenkes RI HK.01.07/MENKES/4634/2020",
                        "volume_issue": "Pedoman Resmi Kemenkes",
                        "quartile": "Pedoman Nasional PNPK",
                        "doi": "KMK_4634_2020",
                        "pmid": "PNPK_HIPERTENSI",
                    },
                    "clinical_finding": (
                        "Golongan ARB direkomendasikan sebagai alternatif lini pertama setara ACE-inhibitor bagi pasien yang mengalami efek samping batuk kering. "
                        "Kombinasi dengan CCB (Amlodipin) dianjurkan bila target < 140/90 mmHg belum tercapai dengan monoterapi."
                    ),
                    "fornas_implication": (
                        "Dasar verifikasi klaim BPJS Kesehatan: resep Kandesartan tidak boleh ditolak jika rekam medis mencatat efek samping batuk pada kaptopril/ramipril."
                    ),
                },
            ],
        },
        {
            "topic_id": "insulin_basal_initiation",
            "title": "Protokol Inisiasi & Titrasi Insulin Basal Pasca Kegagalan Terapi OAD pada DMT2",
            "category": "Endokrinologi",
            "drug_inn": "Insulin Glargine / NPH",
            "clinical_problem": (
                "Keterlambatan inisiasi insulin (clinical inertia) pada pasien DMT2 dengan HbA1c > 9% meski sudah mendapat "
                "kombinasi 2-3 obat antidiabetik oral (OAD)."
            ),
            "fornas_rule": "Fornas mensyaratkan peresepan awal analog insulin di FKRTL oleh Sp.PD/Sp.PD-KEMD dengan target titrasi ketat.",
            "keywords": ["insulin", "glargine", "basal", "diabetes", "hba1c", "oad", "failure", "initiation", "lantus"],
            "articles": [
                {
                    "article_id": "insulin_riddle_2003",
                    "is_primary": True,
                    "citation": {
                        "authors": "Riddle, M. C., Rosenstock, J., Gerich, J. (Treat-to-Target Trial)",
                        "year": 2003,
                        "title": "The Treat-to-Target Trial: randomized addition of glargine or human NPH insulin to oral therapy",
                        "journal": "Diabetes Care",
                        "volume_issue": "Vol. 26(11), pp. 3080–3086",
                        "quartile": "Scopus Q1 / IF ~17",
                        "study_type": "Multicenter Randomized Controlled Trial",
                        "doi": "10.2337/diacare.26.11.3080",
                        "pmid": "14578243",
                    },
                    "clinical_finding": (
                        "Penambahan insulin glargine dosis awal 10 IU/hari bedtime dengan titrasi mandiri 2 IU setiap 3 hari berhasil "
                        "mencapai target HbA1c < 7.0% pada 58% pasien yang gagal OAD, dengan tingkat kejadian hipoglikemia nokturnal "
                        "jauh lebih rendah dibanding NPH (1.3 vs 4.0 kejadian/pasien-tahun, p<0.001)."
                    ),
                    "fornas_implication": (
                        "Mendukung panduan dosis dan restriksi Fornas 2025 untuk insulin glargine (0.1–0.2 IU/kg bedtime, titrasi 2 IU). "
                        "Memastikan inisiasi aman dan terstandar."
                    ),
                },
                {
                    "article_id": "insulin_ada_standards_2024",
                    "is_primary": False,
                    "citation": {
                        "authors": "American Diabetes Association Professional Practice Committee",
                        "year": 2024,
                        "title": "Pharmacologic Approaches to Glycemic Treatment: Standards of Care in Diabetes—2024",
                        "journal": "Diabetes Care",
                        "volume_issue": "Vol. 47(Suppl. 1), pp. S158–S178",
                        "quartile": "Scopus Q1 / IF ~17",
                        "study_type": "Evidence-Based Clinical Practice Guidelines",
                        "doi": "10.2337/dc24-S009",
                        "pmid": "38078590",
                    },
                    "clinical_finding": (
                        "Jika target HbA1c tidak tercapai dalam 3 bulan dengan terapi oral kombinasi, inisiasi insulin basal tidak boleh ditunda. "
                        "Analog basal generasi panjang (Glargine U-100) direkomendasikan untuk meminimalkan risiko hipoglikemia."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi peralihan dari OAD ke insulin di FKRTL saat HbA1c tetap tidak terkontrol sesuai PNPK DMT2 Kemenkes."
                    ),
                },
            ],
        },
        {
            "topic_id": "tramadol_serotonin_syndrome",
            "title": "Pencegahan Sindrom Serotonin: Interaksi Tramadol dengan Antidepresan SSRI/SNRI",
            "category": "Neurologi & Manajemen Nyeri",
            "drug_inn": "Tramadol",
            "clinical_problem": (
                "Peresepan tramadol bersamaan dengan antidepresan (fluoxetine, sertraline, venlafaxine) yang meningkatkan "
                "risiko toksisitas serotonergik akut dan kejang."
            ),
            "fornas_rule": "Fornas memberi peringatan tegas restriksi tramadol: kontraindikasi bersama MAOI dan perhatian ketat dengan serotonergik.",
            "keywords": ["tramadol", "ssri", "snri", "serotonin syndrome", "interaction", "antidepressant", "opioid", "centrasic"],
            "articles": [
                {
                    "article_id": "tramadol_beakley_2015",
                    "is_primary": True,
                    "citation": {
                        "authors": "Beakley, B. D., Kaye, A. M., Kaye, A. D.",
                        "year": 2015,
                        "title": "Tramadol, Pharmacology, Side Effects, and Serotonin Syndrome: A Review",
                        "journal": "Pain Physician",
                        "volume_issue": "Vol. 18(4), pp. 395–400",
                        "quartile": "Scopus Q2 / Peer Reviewed",
                        "study_type": "Narrative Pharmacological Review",
                        "doi": "PMID_26218949",
                        "pmid": "26218949",
                    },
                    "clinical_finding": (
                        "Tramadol memiliki mekanisme ganda: agonis reseptor mu-opioid dan inhibitor reuptake serotonin/norepinefrin. "
                        "Kombinasi dengan SSRI/SNRI melipatgandakan risiko sindrom serotonin (klonus, hipertermia, delirium) dan menurunkan ambang kejang."
                    ),
                    "fornas_implication": (
                        "Mendukung validasi farmasi klinis: bila pasien mengonsumsi antidepresan, apoteker berhak merekomendasikan penggantian "
                        "analgetik ke parasetamol/NSAID atau opioid murni non-serotonergik."
                    ),
                },
                {
                    "article_id": "serotonin_boyer_nejm_2005",
                    "is_primary": False,
                    "citation": {
                        "authors": "Boyer, E. W., Shannon, M.",
                        "year": 2005,
                        "title": "The Serotonin Syndrome",
                        "journal": "New England Journal of Medicine",
                        "volume_issue": "Vol. 352(11), pp. 1112–1120",
                        "quartile": "Scopus Q1 / IF ~176",
                        "study_type": "Comprehensive Clinical Review",
                        "doi": "10.1056/NEJMra041867",
                        "pmid": "15784664",
                    },
                    "clinical_finding": (
                        "Kriteria Hunter Toxicity Criteria merupakan alat diagnostik paling akurat untuk sindrom serotonin. Mayoritas kasus "
                        "terjadi karena interaksi polifarmasi 2 atau lebih obat yang meningkatkan transmisi serotonin secara simultan."
                    ),
                    "fornas_implication": (
                        "Lampiran referensi edukatif resmi bagi tim KFT RS dalam mengaudit keselamatan resep analgesik dan psikotropika."
                    ),
                },
            ],
        },
        {
            "topic_id": "glibenclamide_elderly_hypoglycemia",
            "title": "Penghindaran Glibenklamid pada Pasien Geriatri (Beers Criteria)",
            "category": "Geriatri & Endokrinologi",
            "drug_inn": "Glibenclamide",
            "clinical_problem": (
                "Peresepan glibenklamid pada lansia berisiko tinggi menyebabkan hipoglikemia berkepanjangan yang fatal karena metabolit aktif dan waktu paruh panjang."
            ),
            "fornas_rule": "Fornas memberi penandaan khusus agar penggunaan pada lansia dihindari bila sulfonilurea alternatif tersedia.",
            "keywords": ["glibenclamide", "glibenklamid", "gliclazide", "gliklazid", "glimepiride", "glimepirid", "sulfonilurea", "hipoglikemia", "lansia", "elderly", "hypoglycemia", "diabetes", "daonil", "diamicron", "amaryl"],
            "articles": [
                {
                    "article_id": "glibenclamide_shorr_1997",
                    "is_primary": True,
                    "citation": {
                        "authors": "Shorr, R. I., Ray, W. A., Daugherty, J. R., Griffin, M. R.",
                        "year": 1997,
                        "title": "Individual sulfonylureas and serious hypoglycemia in older people",
                        "journal": "Journal of the American Geriatrics Society",
                        "volume_issue": "Vol. 45(7), pp. 816–820",
                        "quartile": "Scopus Q1 / IF ~7.5",
                        "study_type": "Epidemiological Cohort Study",
                        "doi": "10.1111/j.1532-5415.1997.tb01506.x",
                        "pmid": "9215334",
                    },
                    "clinical_finding": (
                        "Glibenklamid meningkatkan risiko hipoglikemia berat pada usia >65 tahun sebesar 3.2 kali lipat dibanding sulfonilurea lain "
                        "akibat akumulasi metabolit aktif pada penurunan fungsi ginjal fisiologis lansia."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi peralihan resep dari glibenklamid ke gliklazid MR atau glimepirid dalam formularium faskes."
                    ),
                },
                {
                    "article_id": "glibenclamide_guide_study_2004",
                    "is_primary": False,
                    "citation": {
                        "authors": "Schernthaner, G., Grimaldi, A., Di Mario, U., et al. (GUIDE Study)",
                        "year": 2004,
                        "title": "GUIDE study: double-blind comparison of once-daily gliclazide MR and glimepiride in type 2 diabetic patients",
                        "journal": "European Journal of Clinical Investigation",
                        "volume_issue": "Vol. 34(8), pp. 535–542",
                        "quartile": "Scopus Q1 / IF ~5.5",
                        "study_type": "Randomized Double-Blind Parallel Trial (845 Pasien)",
                        "doi": "10.1111/j.1365-2362.2004.01381.x",
                        "pmid": "15305898",
                    },
                    "clinical_finding": (
                        "Gliklazid MR 30–120 mg/hari menunjukkan efikasi kontrol HbA1c setara dengan glimepirid namun dengan insiden hipoglikemia "
                        "50% lebih rendah (3.7% vs 8.9%, p=0.003), menjadikannya pilihan sulfonilurea paling aman untuk lansia."
                    ),
                    "fornas_implication": (
                        "Mendukung ketersediaan Gliklazid MR dalam katalog Fornas untuk populasi pasien rentan hipoglikemia."
                    ),
                },
            ],
        },
        {
            "topic_id": "furosemide_electrolyte_monitoring",
            "title": "Pemantauan Kalium & Proteksi Hipokalemia pada Penggunaan Loop Diuretik (Furosemid)",
            "category": "Kardiologi & Nefrologi",
            "drug_inn": "Furosemide / Spironolactone",
            "clinical_problem": (
                "Penggunaan furosemid dosis tinggi tanpa pemantauan elektrolit memicu aritmia fatal akibat hipokalemia dan hipomagnesemia."
            ),
            "fornas_rule": "Fornas mensyaratkan pemantauan kadar elektrolit serum berkala pada pasien gagal jantung yang mendapat diuretik loop.",
            "keywords": ["furosemide", "furosemid", "spironolactone", "spironolakton", "diuretik", "kalium", "hipokalemia", "monitoring", "electrolyte", "heart failure", "lasix", "aldactone"],
            "articles": [
                {
                    "article_id": "furosemide_rales_1999",
                    "is_primary": True,
                    "citation": {
                        "authors": "Pitt, B., Zannad, F., Remme, W. J., et al. (RALES Investigators)",
                        "year": 1999,
                        "title": "The effect of spironolactone on morbidity and mortality in patients with severe heart failure",
                        "journal": "New England Journal of Medicine",
                        "volume_issue": "Vol. 341(10), pp. 709–717",
                        "quartile": "Scopus Q1 / IF ~176",
                        "study_type": "Double-Blind Randomized Controlled Trial (1.663 Pasien)",
                        "doi": "10.1056/NEJM199909023411001",
                        "pmid": "10471456",
                    },
                    "clinical_finding": (
                        "Kombinasi spironolakton (25 mg/hari) pada pasien gagal jantung yang menerima loop diuretik menurunkan risiko mortalitas "
                        "sebesar 30% (RR 0.70, p<0.001) dan mencegah penurunan kalium serum drastis."
                    ),
                    "fornas_implication": (
                        "Mendukung peresepan kombinasi furosemid + spironolakton pada gagal jantung HFrEF sesuai kelas terapi Fornas."
                    ),
                },
                {
                    "article_id": "furosemide_esc_hf_2021",
                    "is_primary": False,
                    "citation": {
                        "authors": "McDonagh, T. A., Metra, M., Adamo, M., et al. (ESC Task Force)",
                        "year": 2021,
                        "title": "2021 ESC Guidelines for the diagnosis and treatment of acute and chronic heart failure",
                        "journal": "European Heart Journal",
                        "volume_issue": "Vol. 42(36), pp. 3599–3726",
                        "quartile": "Scopus Q1 / IF ~39.3",
                        "study_type": "European Society of Cardiology Clinical Practice Guidelines",
                        "doi": "10.1093/eurheartj/ehab368",
                        "pmid": "34447992",
                    },
                    "clinical_finding": (
                        "Diuretik loop digunakan pada dosis efektif terendah yang mampu menjaga euvolemia. Fungsi ginjal dan elektrolit "
                        "(Na, K, kreatinin) wajib diperiksa pada 1-2 minggu setelah inisiasi atau kenaikan dosis."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi protokol skrining laboratorium kalium berkala pada klaim rawat jalan BPJS."
                    ),
                },
            ],
        },
        {
            "topic_id": "antibiotic_stewardship_amoxicillin",
            "title": "Program Pengendalian Resistensi Antimikroba (PPRA): Pemilihan Amoksisilin vs Sefalosporin",
            "category": "Penyakit Infeksi & PPAB",
            "drug_inn": "Amoxicillin / Ceftriaxone",
            "clinical_problem": (
                "Kecenderungan penggunaan sefalosporin generasi 3 (ceftriaxone/cefixime) secara berlebihan pada infeksi saluran pernapasan atas atau CAP ringan di faskes primer."
            ),
            "fornas_rule": "Fornas menetapkan amoksisilin sebagai lini pertama FKTP; sefalosporin generasi 3 dibatasi untuk indikasi rawat inap/kultur.",
            "keywords": ["amoxicillin", "amoksisilin", "ceftriaxone", "seftriakson", "cefixime", "sefiksim", "antibiotik", "stewardship", "ppab", "ppra", "resistensi", "community", "pneumonia", "isk", "rocephin"],
            "articles": [
                {
                    "article_id": "antibiotic_bts_cap_2009",
                    "is_primary": True,
                    "citation": {
                        "authors": "Lim, W. S., Baudouin, S. V., George, R. C., et al. (BTS Guideline Group)",
                        "year": 2009,
                        "title": "BTS guidelines for the management of community acquired pneumonia in adults",
                        "journal": "Thorax",
                        "volume_issue": "Vol. 64(Suppl 3), pp. iii1–55",
                        "quartile": "Scopus Q1 / IF ~9.3",
                        "study_type": "Evidence-Based National Clinical Guideline",
                        "doi": "10.1136/thx.2009.121434",
                        "pmid": "19783532",
                    },
                    "clinical_finding": (
                        "Amoksisilin oral 500 mg 3x sehari selama 5 hari merupakan terapi lini pertama definitif untuk CAP ringan (skor CURB-65 = 0-1) "
                        "dengan tingkat kesembuhan klinis > 90% tanpa memicu resistensi bakteri gram-negatif."
                    ),
                    "fornas_implication": (
                        "Mendukung restriksi Fornas yang membatasi antibiotik spektrum luas di FKTP dan menjaga lini pertama amoksisilin."
                    ),
                },
                {
                    "article_id": "antibiotic_ats_idsa_2019",
                    "is_primary": False,
                    "citation": {
                        "authors": "Metlay, J. P., Waterer, G. W., Long, A. C., et al. (ATS/IDSA Committee)",
                        "year": 2019,
                        "title": "Diagnosis and Treatment of Adults with Community-acquired Pneumonia: An Official Clinical Practice Guideline",
                        "journal": "American Journal of Respiratory and Critical Care Medicine",
                        "volume_issue": "Vol. 200(7), pp. e45–e67",
                        "quartile": "Scopus Q1 / IF ~30.5",
                        "study_type": "Official ATS/IDSA Consensus Guideline",
                        "doi": "10.1164/rccm.201908-1581ST",
                        "pmid": "31573350",
                    },
                    "clinical_finding": (
                        "Penggunaan antibiotik durasi singkat (5 hari) dengan kriteria stabilitas klinis terbukti seefektif terapi 7-10 hari "
                        "dan secara bermakna memangkas risiko resistensi antimikroba (AMR)."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi pembatasan peresepan maksimal antibiotik oral di Fornas 2025 menjadi 5-7 hari."
                    ),
                },
            ],
        },
        {
            "topic_id": "amlodipine_jnc8",
            "title": "Pemilihan CCB (Amlodipin) pada Hipertensi dengan Komorbiditas DM atau Ginjal",
            "category": "Kardiologi & Hipertensi",
            "drug_inn": "Amlodipine",
            "clinical_problem": (
                "Penetapan target tekanan darah <130/80 mmHg pada pasien DM/CKD dan perdebatan kombinasi antihipertensi lini pertama di FKTP."
            ),
            "fornas_rule": "Fornas menetapkan amlodipin sebagai antihipertensi lini pertama yang dapat diresepkan di FKTP hingga FKRTL.",
            "keywords": ["amlodipine", "amlodipin", "hipertensi", "ccb", "calcium channel blocker", "diabetes", "ckd", "target tekanan darah", "norvask"],
            "articles": [
                {
                    "article_id": "amlodipine_jnc8_jama",
                    "is_primary": True,
                    "citation": {
                        "authors": "James, P. A., Oparil, S., Carter, B. L., et al. (JNC 8 Panel)",
                        "year": 2014,
                        "title": "2014 Evidence-Based Guideline for the Management of High Blood Pressure in Adults: Report From JNC 8",
                        "journal": "JAMA",
                        "volume_issue": "Vol. 311(5), pp. 507–520",
                        "quartile": "Scopus Q1 / IF ~157",
                        "study_type": "Systematic Evidence-Based Guideline",
                        "doi": "10.1001/jama.2013.284427",
                        "pmid": "24352797",
                    },
                    "clinical_finding": (
                        "CCB (termasuk amlodipin) terbukti setara dengan thiazid, ACE-i, dan ARB dalam mencegah stroke dan komplikasi kardiovaskular. "
                        "Sangat efektif pada populasi geriatri dan pasien dengan kekakuan arteri (isolated systolic hypertension)."
                    ),
                    "fornas_implication": (
                        "Mendukung penempatan amlodipin sebagai obat antihipertensi esensial lini pertama dengan ketersediaan penuh di FKTP."
                    ),
                },
                {
                    "article_id": "amlodipine_ish_2020",
                    "is_primary": False,
                    "citation": {
                        "authors": "Unger, T., Borghi, C., Charchar, F., et al. (International Society of Hypertension)",
                        "year": 2020,
                        "title": "2020 International Society of Hypertension Global Hypertension Practice Guidelines",
                        "journal": "Hypertension",
                        "volume_issue": "Vol. 75(6), pp. 1334–1357",
                        "quartile": "Scopus Q1 / IF ~8.3",
                        "study_type": "Global Clinical Practice Guidelines",
                        "doi": "10.1161/HYPERTENSIONAHA.120.15026",
                        "pmid": "32370772",
                    },
                    "clinical_finding": (
                        "Strategi kombinasi dua obat dosis rendah (A+C: ACEi/ARB + CCB) direkomendasikan sebagai langkah awal untuk sebagian besar pasien hipertensi "
                        "derajat 2 atau pasien dengan komorbiditas, menghasilkan kontrol tensi lebih cepat dan proteksi organ target optimal."
                    ),
                    "fornas_implication": (
                        "Dasar justifikasi peresepan kombinasi amlodipin + kandesartan/ramipril pada resep rujuk balik (PRB)."
                    ),
                },
            ],
        },
    ]

    # Backward compatibility flat evidence list
    EVIDENCE_REPOSITORY: List[Dict[str, Any]] = []

    @classmethod
    def _init_flat_evidence(cls):
        """Populate the legacy flat EVIDENCE_REPOSITORY from CURATED_TOPICS for compatibility."""
        items = []
        for t in cls.CURATED_TOPICS:
            for art in t["articles"]:
                items.append({
                    "topic_id": t["topic_id"],
                    "article_id": art["article_id"],
                    "drug_inn": t["drug_inn"],
                    "clinical_question": t["title"],
                    "keywords": t["keywords"],
                    "citation": art["citation"],
                    "clinical_finding": art["clinical_finding"],
                    "fornas_implication": art["fornas_implication"],
                    "is_primary": art["is_primary"],
                })
        cls.EVIDENCE_REPOSITORY = items

    @classmethod
    def get_all_topics(cls) -> List[Dict[str, Any]]:
        """Return all curated clinical justification topics."""
        return cls.CURATED_TOPICS

    @classmethod
    def get_topic_by_id(cls, topic_id: str) -> Optional[Dict[str, Any]]:
        """Find a specific topic by topic_id."""
        for t in cls.CURATED_TOPICS:
            if t["topic_id"] == topic_id:
                return t
        return None

    @classmethod
    def expand_query_with_synonyms(cls, query: str) -> List[str]:
        """Expand user query tokens with drug synonyms and spelling variants."""
        clean = re.sub(r"[^\w\s-]", " ", query.lower()).strip()
        tokens = clean.split()
        expanded = set(tokens)

        for tok in tokens:
            # Check exact match in synonyms
            if tok in cls.DRUG_SYNONYMS:
                for syn in cls.DRUG_SYNONYMS[tok]:
                    expanded.add(syn)
            # Check partial match
            for k, syns in cls.DRUG_SYNONYMS.items():
                if tok in k or k in tok:
                    expanded.add(k)
                    for s in syns:
                        expanded.add(s)

        return list(expanded)

    @classmethod
    def search_curated_topics(cls, query: str = "") -> List[Dict[str, Any]]:
        """Deep Search across topics, metadata, synonyms, and article body texts."""
        if not query or not query.strip():
            return cls.CURATED_TOPICS

        expanded_tokens = cls.expand_query_with_synonyms(query)
        scored_topics = []

        for t in cls.CURATED_TOPICS:
            score = 0
            drug_lower = t["drug_inn"].lower()
            title_lower = t["title"].lower()
            category_lower = t.get("category", "").lower()
            problem_lower = t.get("clinical_problem", "").lower()
            rule_lower = t.get("fornas_rule", "").lower()

            for tok in expanded_tokens:
                # 1. Drug INN match (highest priority)
                if tok in drug_lower or drug_lower in tok:
                    score += 12
                # 2. Title match
                if tok in title_lower:
                    score += 8
                # 3. Category match
                if tok in category_lower:
                    score += 4
                # 4. Keyword match
                for kw in t.get("keywords", []):
                    if tok in kw.lower() or kw.lower() in tok:
                        score += 5
                # 5. Clinical problem or Fornas rule match
                if tok in problem_lower:
                    score += 3
                if tok in rule_lower:
                    score += 3

            # 6. Deep Search into Articles (citations, findings, and implications)
            for art in t.get("articles", []):
                c = art.get("citation", {})
                art_text = f"{c.get('title', '')} {c.get('authors', '')} {c.get('journal', '')} {art.get('clinical_finding', '')} {art.get('fornas_implication', '')}".lower()
                for tok in expanded_tokens:
                    if tok in art_text:
                        score += 3

            if score > 0:
                scored_topics.append((score, t))

        scored_topics.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in scored_topics]

    @classmethod
    def search_clinical_evidence(
        cls, drug_inn: str = "", clinical_question: str = ""
    ) -> List[Dict[str, Any]]:
        """Legacy flat evidence search for backward compatibility."""
        if not cls.EVIDENCE_REPOSITORY:
            cls._init_flat_evidence()

        query_tokens = []
        if drug_inn:
            query_tokens.extend(cls.expand_query_with_synonyms(drug_inn))
        if clinical_question:
            query_tokens.extend(cls.expand_query_with_synonyms(clinical_question))

        matches = []
        for item in cls.EVIDENCE_REPOSITORY:
            score = 0
            if drug_inn and any(tok in item["drug_inn"].lower() for tok in query_tokens):
                score += 5
            for kw in item.get("keywords", []):
                if any(token in kw or kw in token for token in query_tokens):
                    score += 2
            if clinical_question:
                for token in query_tokens:
                    if token in item["clinical_question"].lower():
                        score += 2
            if score > 0:
                matches.append((score, item))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in matches]

    @classmethod
    def format_evidence_card(cls, item: Dict[str, Any]) -> str:
        """Format a single clinical evidence item as a structured Markdown card."""
        c = item["citation"]
        lines = [
            f"### 📖 Bukti Klinis: *{item['clinical_question']}*",
            "",
            f"**Obat Terkait**: {item['drug_inn']}",
            "",
            "**Sumber Literatur:**",
            f"- **Penulis**: {c['authors']} ({c['year']})",
            f"- **Judul**: *\"{c['title']}\"*",
            f"- **Jurnal**: {c['journal']}, {c['volume_issue']} (**{c['quartile']}**)",
            f"- **Identifikasi**: DOI: {c.get('doi', '-')} | PMID: {c.get('pmid', '-')}",
            "",
            "**Temuan Klinis:**",
            f"> {item['clinical_finding']}",
            "",
            "**Implikasi terhadap Restriksi Fornas:**",
            f"> {item['fornas_implication']}",
            "---",
        ]
        return "\n".join(lines)

    @classmethod
    def generate_justification_memo(
        cls,
        topic: Dict[str, Any],
        selected_articles: List[Dict[str, Any]],
        patient_info: Optional[Dict[str, str]] = None,
        pharmacist_notes: str = "",
        pharmacist_name: str = "Apoteker Farmasi Klinis",
        sipa_number: str = "SIPA.XXXXXXXXXXXX",
    ) -> str:
        """Generate a complete, audit-ready Clinical Justification Memo for KFT & BPJS."""
        now_str = datetime.now().strftime("%d %B %Y, %H:%M WIB")
        p = patient_info or {}

        patient_name = p.get("nama_pasien", "[Nama Pasien]")
        no_rm = p.get("no_rm", "[No. Rekam Medis]")
        diagnosis = p.get("diagnosis", "[Diagnosis Klinis]")
        dpjp = p.get("dpjp", "[Dokter Penanggung Jawab Pelayanan]")
        ruangan = p.get("ruangan", "[Instalasi / Bangsal Rawat]")

        lines = [
            "# 📋 MEMO JUSTIFIKASI KLINIS KEPADA KOMITE FARMASI & TERAPI (KFT)",
            "**Lampiran Telaah Bukti Ilmiah (Q1–Q3) & Adaptasi Restriksi Formularium Nasional**",
            f"*Dibuat melalui Guppy Clinical Pharmacy & Fornas 2025 Helper — {now_str}*",
            "",
            "---",
            "### BAGIAN I: DATA PASIEN & MASALAH REGULASI RESEP",
            f"- **Nama Pasien**: {patient_name}",
            f"- **No. Rekam Medis**: {no_rm}",
            f"- **Diagnosis Kerja / ICD-10**: {diagnosis}",
            f"- **DPJP (Dokter Penulis Resep)**: {dpjp}",
            f"- **Unit / Ruang Perawatan**: {ruangan}",
            f"- **Obat yang Dimintakan Justifikasi**: **{topic.get('drug_inn', '-')}**",
            f"- **Kasus / Masalah Klinis**: {topic.get('clinical_problem', '-')}",
            f"- **Ketentuan Baku Fornas 2025**: {topic.get('fornas_rule', '-')}",
            "",
            "---",
            "### BAGIAN II: TELAAH BUKTI ILMIAH TERAKREDITASI (PILIHAN APOTEKER)",
            f"*Sumber referensi terindeks Scopus Q1–Q3 tervalidasi ({cls.CURATION_VERSION})*",
            "",
        ]

        if not selected_articles:
            lines.append("*(Tidak ada artikel spesifik yang dipilih. Mengacu pada pedoman standar Kemenkes/Fornas)*\n")
        else:
            for idx, art in enumerate(selected_articles, 1):
                c = art["citation"]
                badge = "⭐ [REKOMENDASI UTAMA GUPPY]" if art.get("is_primary") else "📑 [STUDI PENDUKUNG/PEMBANDING]"
                lines.extend([
                    f"#### {idx}. {badge} {c['title']}",
                    f"- **Penulis & Tahun**: {c['authors']} ({c['year']})",
                    f"- **Jurnal & Reputasi**: *{c['journal']}*, {c['volume_issue']} — **`{c['quartile']}`**",
                    f"- **Jenis Studi**: {c.get('study_type', 'Clinical Evidence')}",
                    f"- **DOI / Pengenal**: `{c.get('doi', '-')}` | PMID: `{c.get('pmid', '-')}`",
                    "",
                    "**Ringkasan Temuan Klinis Ilmiah:**",
                    f"> {art['clinical_finding']}",
                    "",
                    "**Implikasi Klinis terhadap Restriksi Fornas:**",
                    f"> {art['fornas_implication']}",
                    "",
                ])

        lines.extend([
            "---",
            "### BAGIAN III: REKOMENDASI & SINTESIS APOTEKER KLINIS",
        ])

        if pharmacist_notes and pharmacist_notes.strip():
            lines.append(f"> {pharmacist_notes.strip()}\n")
        else:
            lines.append(
                "> Berdasarkan telaah bukti ilmiah di atas, pasien memenuhi kriteria adaptasi restriksi "
                "dengan mempertimbangkan rasio manfaat klinis yang melampaui risiko (risk-benefit balance). "
                "Disarankan pemberian terapi dapat dilanjutkan dengan pemantauan parameter keamanan secara berkala.\n"
            )

        lines.extend([
            "**Rencana Pemantauan Keamanan Terapi Obat (PTO):**",
            "- Pemantauan tanda vital dan respon terapeutik secara berkala.",
            "- Pemeriksaan parameter laboratorium keamanan (fungsi ginjal / hati / elektrolit) sesuai indikasi.",
            "- Pelaporan segera jika timbul Kejadian Tidak Diinginkan (KTD) / Efek Samping Obat (MESO).",
            "",
            "---",
            "### BAGIAN IV: LEMBAR PENGESAHAN & PERSETUJUAN KFT",
            "",
            "| Diajukan oleh (Apoteker Pengkaji) | Diverifikasi oleh (DPJP Pasien) | Disetujui oleh (Ketua KFT / Direktur RS) |",
            "| :---: | :---: | :---: |",
            "| <br><br><br> | <br><br><br> | <br><br><br> |",
            f"| **({pharmacist_name})**<br>No. SIPA: {sipa_number} | **({dpjp})**<br>Dokter Spesialis / DPJP | **(.......................................)**<br>Komite Farmasi & Terapi |",
            "",
            "---",
            "*Catatan Audit: Dokumen ini sah sebagai lampiran verifikasi klaim BPJS Kesehatan / audit internal RS sesuai PMK Standar Pelayanan Kefarmasian di RS.*",
        ])

        return "\n".join(lines)

    @classmethod
    def generate_universal_justification_memo(
        cls,
        drug_name: str,
        justification_reason: str,
        clinical_rationale: str,
        patient_info: Optional[Dict[str, str]] = None,
        fornas_info: Optional[Dict[str, Any]] = None,
        pharmacist_name: str = "Apoteker Farmasi Klinis",
        sipa_number: str = "SIPA.XXXXXXXXXXXX",
    ) -> str:
        """Generate a Universal Justification Memo for any drug in the national formulary.

        Used when a drug does not yet have a dedicated curated literature article card.
        """
        now_str = datetime.now().strftime("%d %B %Y, %H:%M WIB")
        p = patient_info or {}
        f_info = fornas_info or {}

        patient_name = p.get("nama_pasien", "[Nama Pasien]")
        no_rm = p.get("no_rm", "[No. Rekam Medis]")
        diagnosis = p.get("diagnosis", "[Diagnosis Klinis / ICD-10]")
        dpjp = p.get("dpjp", "[Dokter Penanggung Jawab Pelayanan]")
        ruangan = p.get("ruangan", "[Instalasi / Bangsal Rawat]")

        lines = [
            "# 📋 MEMO JUSTIFIKASI KLINIS KEPADA KOMITE FARMASI & TERAPI (KFT)",
            "**Formulir Pengajuan Adaptasi Khusus Terapi Obat / Verifikasi Klaim Rumah Sakit**",
            f"*Dibuat melalui Guppy Clinical Pharmacy & Fornas 2025 Helper — {now_str}*",
            "",
            "---",
            "### BAGIAN I: DATA PASIEN & IDENTITAS TERAPI",
            f"- **Nama Pasien**: {patient_name}",
            f"- **No. Rekam Medis**: {no_rm}",
            f"- **Diagnosis Kerja / ICD-10**: {diagnosis}",
            f"- **Dokter Penulis Resep (DPJP)**: {dpjp}",
            f"- **Ruangan / Poliklinik**: {ruangan}",
            f"- **Nama Obat yang Diajukan**: **{drug_name.upper()}**",
        ]

        if f_info.get("kelas_terapi"):
            lines.append(f"- **Kelas Terapi Fornas**: {f_info.get('kelas_terapi')}")
        if f_info.get("fasilitas"):
            lines.append(f"- **Tingkat Fasilitas Penjaminan**: {f_info.get('fasilitas')}")
        if f_info.get("peresepan_maksimal"):
            lines.append(f"- **Peresepan Maksimal Standar**: {f_info.get('peresepan_maksimal')}")

        lines.extend([
            "",
            "---",
            "### BAGIAN II: ALASAN & KATEGORI JUSTIFIKASI KLINIS (KFT)",
            f"- **Kategori Justifikasi**: **`[{justification_reason}]`**",
            "",
            "**Uraian Klinis & Dasar Kebutuhan Pasien:**",
            f"> {clinical_rationale if clinical_rationale.strip() else 'Pasien memerlukan terapi ini dengan pertimbangan kondisi klinis individual yang mendesak dan tidak dapat digantikan oleh regimen standar lini pertama.'}",
            "",
            "---",
            "### BAGIAN III: TELAAH REGULASI & STANDAR KESELAMATAN (PTO)",
            "- **Regulasi Acuan**: Kepmenkes RI No. HK.01.07/MENKES/1199/2025 tentang Formularium Nasional & UU No. 17/2023 tentang Kesehatan.",
            "- **Analisis Manfaat vs Risiko (Risk-Benefit)**: Manfaat terapeutik yang diharapkan lebih besar daripada potensi risiko efek samping.",
            "- **Protokol Pemantauan Terapi Obat (PTO)**: Apoteker dan DPJP akan memantau respon klinis dan laboratorium keamanan (fungsi hati/ginjal/tanda vital) secara berkala selama terapi berlangsung.",
            "",
            "---",
            "### BAGIAN IV: LEMBAR PENGESAHAN DOKUMEN KFT",
            "",
            "| Diajukan oleh (Apoteker Pengkaji) | Diverifikasi oleh (DPJP Pasien) | Disetujui oleh (Ketua KFT / Direktur RS) |",
            "| :---: | :---: | :---: |",
            "| <br><br><br> | <br><br><br> | <br><br><br> |",
            f"| **({pharmacist_name})**<br>No. SIPA: {sipa_number} | **({dpjp})**<br>Dokter Spesialis / DPJP | **(.......................................)**<br>Komite Farmasi & Terapi |",
            "",
            "---",
            "*Catatan: Dokumen ini disimpan di Rekam Medis Pasien dan sah dilampirkan pada berkas pertanggungjawaban verifikasi klaim BPJS Kesehatan.*",
        ])

        return "\n".join(lines)

    @classmethod
    def generate_justification_memo_docx(
        cls,
        topic: Dict[str, Any],
        selected_articles: List[Dict[str, Any]],
        patient_info: Optional[Dict[str, str]] = None,
        pharmacist_notes: str = "",
        pharmacist_name: str = "Apoteker Farmasi Klinis",
        sipa_number: str = "SIPA.XXXXXXXXXXXX",
    ) -> bytes:
        """Generate Word (.docx) document bytes for Curated Topic Justification Memo."""
        from guppy.backend.engine.docx_generator import create_justification_memo_docx
        return create_justification_memo_docx(
            topic=topic,
            selected_articles=selected_articles,
            patient_info=patient_info,
            pharmacist_notes=pharmacist_notes,
            pharmacist_name=pharmacist_name,
            sipa_number=sipa_number,
        )

    @classmethod
    def generate_universal_justification_memo_docx(
        cls,
        drug_name: str,
        justification_reason: str,
        clinical_rationale: str,
        patient_info: Optional[Dict[str, str]] = None,
        fornas_info: Optional[Dict[str, Any]] = None,
        pharmacist_name: str = "Apoteker Farmasi Klinis",
        sipa_number: str = "SIPA.XXXXXXXXXXXX",
    ) -> bytes:
        """Generate Word (.docx) document bytes for Universal Justification Memo."""
        from guppy.backend.engine.docx_generator import create_universal_justification_memo_docx
        return create_universal_justification_memo_docx(
            drug_name=drug_name,
            justification_reason=justification_reason,
            clinical_rationale=clinical_rationale,
            patient_info=patient_info,
            fornas_info=fornas_info,
            pharmacist_name=pharmacist_name,
            sipa_number=sipa_number,
        )


# Initialize flat evidence repository on module import
ClinicalLiteratureScout._init_flat_evidence()
