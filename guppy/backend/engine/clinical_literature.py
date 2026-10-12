"""Clinical Literature Scout — Evidence Justification for Fornas Restriction Adaptation.

Provides peer-reviewed scientific justification when a patient's clinical condition
requires consideration beyond standard Fornas restrictions (e.g., off-label use,
dose adjustment, or special population considerations).
"""

from typing import Dict, List, Any


class ClinicalLiteratureScout:
    """Clinical evidence repository for justifying Fornas restriction adaptations.

    Evidence sourced from Q1-Q3 indexed journals relevant to Indonesian clinical practice:
    Scopus, PubMed, NEJM, Lancet, JAMA, and national PNPK references.
    """

    EVIDENCE_REPOSITORY: List[Dict[str, Any]] = [
        {
            "topic_id": "metformin_ckd_egfr",
            "drug_inn": "Metformin",
            "clinical_question": "Keamanan metformin pada pasien DMT2 dengan penurunan fungsi ginjal (CKD)",
            "keywords": ["metformin", "ckd", "ginjal", "egfr", "creatinine", "renal", "lactic acidosis", "diabetes"],
            "citation": {
                "authors": "Lipska, K. J., Bailey, C. J., Inzucchi, S. E.",
                "year": 2011,
                "title": "Use of Metformin in the Setting of Mild-to-Moderate Renal Insufficiency",
                "journal": "Diabetes Care",
                "volume_issue": "Vol. 34(6), pp. 1431–1437",
                "quartile": "Scopus Q1 / IF ~17",
                "doi": "10.2337/dc10-2361",
                "pmid": "21617112",
            },
            "clinical_finding": (
                "Metformin dapat digunakan dengan aman pada pasien DMT2 dengan eGFR 30-60 mL/mnt/1.73m² "
                "(CKD Derajat 3a-3b) dengan penyesuaian dosis (maksimal 1000 mg/hari) dan pemantauan "
                "fungsi ginjal setiap 3-6 bulan. Risiko laktat asidosis sangat rendah pada eGFR > 30 mL/mnt "
                "bila tidak ada kontraindikasi lain. Fornas melarang penggunaan pada eGFR < 30 mL/mnt."
            ),
            "fornas_implication": (
                "Mendukung tetap melanjutkan metformin pada pasien dengan CKD ringan-sedang (GFR 30-60), "
                "dengan modifikasi dosis sesuai guideline KDIGO 2022 dan PNPK DMT2 Kemenkes 2020."
            ),
        },
        {
            "topic_id": "statin_elderly",
            "drug_inn": "Simvastatin / Atorvastatin",
            "clinical_question": "Manfaat dan keamanan statin pada pasien lanjut usia (>75 tahun) dengan dislipidemia",
            "keywords": ["statin", "elderly", "lansia", "atorvastatin", "simvastatin", "myopathy", "rhabdomyolysis", "cardiovascular"],
            "citation": {
                "authors": "Cholesterol Treatment Trialists' (CTT) Collaboration",
                "year": 2019,
                "title": "Efficacy and safety of statin therapy in older people: a meta-analysis of individual participant data",
                "journal": "The Lancet",
                "volume_issue": "Vol. 393(10170), pp. 407–415",
                "quartile": "Scopus Q1 / IF ~202",
                "doi": "10.1016/S0140-6736(18)31942-1",
                "pmid": "30712900",
            },
            "clinical_finding": (
                "Meta-analisis 28 RCT (186,854 peserta) menunjukkan statin mengurangi risiko major "
                "cardiovascular events pada lansia >75 tahun sebanding dengan pasien lebih muda "
                "(RR 0.82 per 1 mmol/L LDL-C reduction). Risiko miopati/rabdomiolisis tidak meningkat "
                "signifikan. Simvastatin 80 mg tetap tidak direkomendasikan pada lansia karena risiko "
                "miopati yang jauh lebih tinggi dibanding dosis lebih rendah."
            ),
            "fornas_implication": (
                "Mendukung penggunaan Atorvastatin (bukan Simvastatin 80 mg) pada lansia dengan risiko CV tinggi. "
                "Fornas membatasi Simvastatin pada 40 mg/hari; alih ke Atorvastatin dianjurkan untuk "
                "pencegahan sekunder pada lansia sesuai ESC/EAS Guidelines 2019."
            ),
        },
        {
            "topic_id": "ppi_deprescribing",
            "drug_inn": "Omeprazole",
            "clinical_question": "Deprescribing PPI pada pasien tanpa indikasi kuat (penggunaan jangka panjang tanpa evaluasi)",
            "keywords": ["omeprazole", "ppi", "deprescribing", "gerd", "long-term", "proton pump inhibitor", "withdrawal"],
            "citation": {
                "authors": "Farrell, B., Pottie, K., Thompson, W., et al.",
                "year": 2017,
                "title": "Deprescribing proton pump inhibitors: Evidence-based clinical practice guideline",
                "journal": "Canadian Family Physician",
                "volume_issue": "Vol. 63(5), pp. 354–364",
                "quartile": "Scopus Q2 / MEDLINE Indexed",
                "doi": "PMC5429073",
                "pmid": "28500294",
            },
            "clinical_finding": (
                "Penggunaan PPI jangka panjang (>8 minggu) tanpa indikasi yang kuat dapat dihentikan secara "
                "bertahap (step-down) pada 70-80% pasien tanpa rekurensi gejala signifikan. "
                "Risiko penggunaan PPI jangka panjang: defisiensi Mg, peningkatan risiko infeksi C. difficile, "
                "dan penurunan densitas tulang. Re-evaluasi indikasi setiap kunjungan direkomendasikan."
            ),
            "fornas_implication": (
                "Mendukung kebijakan Fornas bahwa PPI harus dievaluasi ulang setiap 4-8 minggu. "
                "Untuk GERD ringan, step-down ke antasida/H2-blocker direkomendasikan setelah remisi. "
                "PPI tanpa indikasi bukti kuat tidak dijamin JKN."
            ),
        },
        {
            "topic_id": "tramadol_serotonin_syndrome",
            "drug_inn": "Tramadol",
            "clinical_question": "Risiko sindrom serotonin tramadol bila dikombinasi dengan antidepresan SSRI/SNRI",
            "keywords": ["tramadol", "ssri", "snri", "serotonin syndrome", "interaction", "antidepressant", "opioid"],
            "citation": {
                "authors": "Beakley, B. D., Kaye, A. M., Kaye, A. D.",
                "year": 2015,
                "title": "Tramadol, Pharmacology, Side Effects, and Serotonin Syndrome: A Review",
                "journal": "Pain Physician",
                "volume_issue": "Vol. 18(4), pp. 395–400",
                "quartile": "Scopus Q2",
                "doi": "PMID_26218949",
                "pmid": "26218949",
            },
            "clinical_finding": (
                "Tramadol menghambat reuptake serotonin dan norepinefrin, dan sebagai opioid agonis parsial. "
                "Kombinasi dengan SSRI/SNRI meningkatkan risiko sindrom serotonin (agitasi, hiperrefleksia, "
                "hipertermia, tremor). Kasus fatal dilaporkan. Penggunaan bersama MAO-inhibitor "
                "SANGAT DIKONTRAINDIKASIKAN. Fornas mencantumkan restriksi ini secara tegas."
            ),
            "fornas_implication": (
                "Mendukung catatan prescribing Fornas bahwa tramadol tidak boleh dikombinasi dengan "
                "MAO-inhibitor dan harus hati-hati jika dikombinasi dengan SSRI/SNRI. "
                "Klinisi wajib meninjau daftar obat pasien sebelum meresepkan tramadol."
            ),
        },
        {
            "topic_id": "insulin_basal_initiation",
            "drug_inn": "Insulin Glargine",
            "clinical_question": "Kapan waktu yang tepat untuk inisiasi insulin basal pada DMT2 yang gagal OAD",
            "keywords": ["insulin", "glargine", "basal", "diabetes", "hba1c", "oad", "failure", "initiation"],
            "citation": {
                "authors": "Riddle, M. C., Rosenstock, J., Gerich, J. (Treat-to-Target Trial)",
                "year": 2003,
                "title": "The treat-to-target trial: randomized addition of glargine or human NPH insulin to oral therapy of type 2 diabetic patients",
                "journal": "Diabetes Care",
                "volume_issue": "Vol. 26(11), pp. 3080–3086",
                "quartile": "Scopus Q1",
                "doi": "10.2337/diacare.26.11.3080",
                "pmid": "14578243",
            },
            "clinical_finding": (
                "Penambahan insulin glargine pada terapi OAD gagal menghasilkan penurunan HbA1c signifikan "
                "mencapai target < 7% pada 58% pasien vs 38% dengan NPH insulin, dengan risiko hipoglikemia "
                "nokturnal lebih rendah. Inisiasi dosis kecil (0.1-0.2 IU/kg/malam) dengan titrasi 2 IU "
                "setiap 3 hari terbukti efektif dan aman."
            ),
            "fornas_implication": (
                "Mendukung panduan dosis Fornas untuk insulin glargine (0.1-0.2 IU/kg bedtime, titrasi 2 IU "
                "setiap 3 hari). Inisiasi di FKRTL oleh Sp.PD-KEMD sesuai dengan kompleksitas titration "
                "yang memerlukan monitoring ketat. PERKENI 2021 dan ADA 2024 selaras dengan Fornas."
            ),
        },
        {
            "topic_id": "glibenclamide_elderly_hypoglycemia",
            "drug_inn": "Glibenclamide",
            "clinical_question": "Risiko hipoglikemia glibenclamide pada pasien lansia dengan DMT2",
            "keywords": ["glibenclamide", "sulfonilurea", "hipoglikemia", "lansia", "elderly", "hypoglycemia", "diabetes"],
            "citation": {
                "authors": "Shorr, R. I., Ray, W. A., Daugherty, J. R., Griffin, M. R.",
                "year": 1997,
                "title": "Individual sulfonylureas and serious hypoglycemia in older people",
                "journal": "Journal of the American Geriatrics Society",
                "volume_issue": "Vol. 45(7), pp. 816–820",
                "quartile": "Scopus Q1",
                "doi": "10.1111/j.1532-5415.1997.tb01506.x",
                "pmid": "9215334",
            },
            "clinical_finding": (
                "Glibenclamide meningkatkan risiko hipoglikemia serius pada lansia > 3 kali lipat dibanding "
                "sulfonilurea generasi baru (Gliclazide, Glimepiride) atau Glipizide. Hipoglikemia nokturnal "
                "berkepanjangan terjadi karena waktu paruh panjang (~16 jam) dan metabolit aktif yang terakumulasi "
                "pada gangguan ginjal. Mortalitas akibat hipoglikemia pada lansia secara konsisten lebih tinggi "
                "untuk glibenclamide dibanding OAD lainnya."
            ),
            "fornas_implication": (
                "Mendukung peringatan Fornas bahwa glibenclamide tidak direkomendasikan sebagai pilihan pertama "
                "pada lansia. Preferensikan Gliclazide MR atau Glimepiride yang tersedia dalam Fornas. "
                "Jika glibenclamide terpaksa digunakan, mulai dosis rendah (2.5 mg) dan monitor ketat."
            ),
        },
        {
            "topic_id": "furosemide_electrolyte_monitoring",
            "drug_inn": "Furosemide",
            "clinical_question": "Pentingnya monitoring elektrolit pada terapi furosemide jangka panjang",
            "keywords": ["furosemide", "diuretik", "kalium", "hipokalemia", "monitoring", "electrolyte", "heart failure"],
            "citation": {
                "authors": "Pitt, B., Zannad, F., Remme, W. J., et al. (RALES Trial)",
                "year": 1999,
                "title": "The effect of spironolactone on morbidity and mortality in patients with severe heart failure",
                "journal": "New England Journal of Medicine",
                "volume_issue": "Vol. 341(10), pp. 709–717",
                "quartile": "Scopus Q1 / IF ~176",
                "doi": "10.1056/NEJM199909023411001",
                "pmid": "10471456",
            },
            "clinical_finding": (
                "Penggunaan loop diuretik (furosemide) dalam jangka panjang pada gagal jantung menyebabkan "
                "hipokalemia pada 20-40% pasien, yang meningkatkan risiko aritmia dan kematian mendadak "
                "terutama pada pasien yang bersamaan menggunakan digoksin. Suplementasi kalium dan/atau "
                "spironolakton secara signifikan menurunkan mortalitas (RALES: -30% all-cause mortality)."
            ),
            "fornas_implication": (
                "Mendukung panduan monitoring Fornas bahwa elektrolit (K, Na, Mg) wajib dipantau pada "
                "terapi furosemide. Kombinasi furosemide + spironolakton tersedia dalam Fornas untuk "
                "gagal jantung — selaras dengan ESC Heart Failure Guidelines 2021."
            ),
        },
        {
            "topic_id": "antibiotic_stewardship_amoxicillin",
            "drug_inn": "Amoxicillin",
            "clinical_question": "Panduan penggunaan amoxicillin sesuai prinsip bijak antibiotik (PPAB) di FKTP",
            "keywords": ["amoxicillin", "antibiotik", "stewardship", "ppab", "resistensi", "community", "pneumonia", "isk"],
            "citation": {
                "authors": "Lim, W. S., Baudouin, S. V., George, R. C., et al. (BTS Guidelines Group)",
                "year": 2009,
                "title": "BTS guidelines for the management of community acquired pneumonia in adults",
                "journal": "Thorax",
                "volume_issue": "Vol. 64(Suppl 3), pp. iii1–55",
                "quartile": "Scopus Q1 / IF ~9.3",
                "doi": "10.1136/thx.2009.121434",
                "pmid": "19783532",
            },
            "clinical_finding": (
                "Amoxicillin oral (500 mg 3x/hari, 5-7 hari) merupakan terapi lini pertama untuk Community "
                "Acquired Pneumonia (CAP) ringan (CURB-65 skor 0-1) di FKTP, dengan efektivitas setara "
                "antibiotik spektrum lebih luas namun dengan profil resistensi lebih terbatas. "
                "Pemberian antibiotik hanya berdasarkan klinis dan/atau kultur mengurangi resistensi antimikroba."
            ),
            "fornas_implication": (
                "Mendukung penggunaan amoxicillin sebagai pilihan pertama di FKTP untuk infeksi respirasi "
                "komunitas sesuai PPAB Kemenkes 2021. Penggantian ke antibiotik broad-spectrum hanya jika "
                "ada bukti resistensi atau kondisi berat (FKRTL). Fornas mendukung stewardship antibiotik."
            ),
        },
        {
            "topic_id": "amlodipine_jnc8",
            "drug_inn": "Amlodipine",
            "clinical_question": "Pilihan antihipertensi berbasis bukti untuk pasien hipertensi dengan komorbiditas DM atau CKD",
            "keywords": ["amlodipine", "hipertensi", "ccb", "calcium channel blocker", "diabetes", "ckd", "target tekanan darah"],
            "citation": {
                "authors": "James, P. A., Oparil, S., Carter, B. L., et al.",
                "year": 2014,
                "title": "2014 Evidence-Based Guideline for the Management of High Blood Pressure in Adults: Report From JNC 8",
                "journal": "JAMA",
                "volume_issue": "Vol. 311(5), pp. 507–520",
                "quartile": "Scopus Q1 / IF ~157",
                "doi": "10.1001/jama.2013.284427",
                "pmid": "24352797",
            },
            "clinical_finding": (
                "CCB (termasuk amlodipine) merupakan salah satu dari 4 kelas antihipertensi lini pertama "
                "yang direkomendasikan (bersama thiazid, ACE-i, ARB). Untuk pasien non-Black non-DM, "
                "CCB atau thiazid direkomendasikan sebagai lini pertama. Amlodipine menunjukkan reduksi "
                "risiko stroke dan mortalitas kardiovaskular yang signifikan dalam ASCOT-BPLA trial."
            ),
            "fornas_implication": (
                "Mendukung posisi amlodipine sebagai antihipertensi lini pertama dalam Fornas untuk FKTP. "
                "Target tekanan darah < 140/90 mmHg umum, atau < 130/80 mmHg untuk pasien DM/CKD "
                "sesuai PNPK Hipertensi Kemenkes 2020 dan ISH 2020 Guidelines."
            ),
        },
    ]

    @classmethod
    def search_clinical_evidence(
        cls, drug_inn: str = "", clinical_question: str = ""
    ) -> List[Dict[str, Any]]:
        """Search for clinical evidence relevant to a drug and/or clinical question.

        Args:
            drug_inn: INN name of the drug (e.g., 'Metformin')
            clinical_question: Free-text clinical question

        Returns:
            List of matching evidence items.
        """
        query_tokens = []
        if drug_inn:
            query_tokens.extend(drug_inn.lower().split())
        if clinical_question:
            query_tokens.extend(clinical_question.lower().split())

        matches = []
        for item in cls.EVIDENCE_REPOSITORY:
            score = 0
            # Score by drug name match
            if drug_inn and drug_inn.lower() in item["drug_inn"].lower():
                score += 3
            # Score by keywords
            for kw in item.get("keywords", []):
                if any(token in kw or kw in token for token in query_tokens):
                    score += 1
            # Score by clinical question match
            if clinical_question:
                for token in query_tokens:
                    if token in item["clinical_question"].lower():
                        score += 1

            if score > 0:
                matches.append((score, item))

        matches.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in matches]

    @classmethod
    def format_evidence_card(cls, item: Dict[str, Any]) -> str:
        """Format a clinical evidence item as a structured Markdown card."""
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
            f"- **Identifikasi**: DOI/PMID: {c.get('doi', '-')} | PMID: {c.get('pmid', '-')}",
            "",
            f"**Temuan Klinis:**",
            f"> {item['clinical_finding']}",
            "",
            f"**Implikasi terhadap Restriksi Fornas:**",
            f"> {item['fornas_implication']}",
            "---",
        ]
        return "\n".join(lines)
