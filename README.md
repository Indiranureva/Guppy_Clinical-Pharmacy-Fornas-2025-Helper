# Guppy - Pharmaceutical Regulatory Helper

**Guppy** is an AI agent-based application engineered to help pharmacists, regulatory affairs (RA) professionals, and pharmaceutical researchers search for, understand, compare, and apply pharmaceutical regulations to specific cases or products.

Built for the Master's Program course: *Aplikasi AI dalam Industri Farmasi*.

---

## Key Features

1. **Product Classification Wizard**:
   - Deductive classification tree for Indonesian market: Sediaan Obat Jadi (Obat Keras, Bebas Terbatas, Bebas), Obat Bahan Alam (Jamu, OHT, Fitofarmaka), Suplemen Kesehatan, and Kosmetika.
   - Evaluates dosing thresholds (e.g., Vitamin C 1000 mg limit, Vitamin D3 4000 IU limit), routes of administration, and preclinical/clinical evidence status.
2. **ACTD Dossier Compliance & Gap Analysis Engine**:
   - Evaluates submission readiness across ACTD Parts I to IV.
   - Enforces Indonesian Climatic Zone IVb stability testing ($30^\circ\text{C} \pm 2^\circ\text{C} / 75\% \pm 5\% \text{RH}$ real-time $\ge 12$ months, $40^\circ\text{C} / 75\% \text{RH}$ accelerated $\ge 6$ months).
   - Flags Critical showstoppers, Major PTD risks, and Moderate labeling gaps.
3. **Cross-Jurisdiction Regulatory Comparator**:
   - Side-by-side benchmarking: BPOM (Indonesia) vs. US FDA vs. EMA vs. ICH.
   - Stability testing zones, Nitrosamine limits (ICH M7 vs. BPOM SE), Bioequivalence criteria, and ACTD vs. eCTD formats.
4. **Regulatory Clause Explorer**:
   - Instant search across indexed articles from UU No. 17/2023 tentang Kesehatan, PerBPOM No. 24/2017, PerBPOM No. 31/2018 (Penandaan & 2D Barcode), and Farmakope Indonesia VI.
5. **BPOM Submission Roadmap & NIE Decoder**:
   - SLA calculator for Jalur 100, 150, 300 hari kerja including PTD buffer estimation.
   - 15-digit NIE decoder (Golongan obat, status impor/lokal, tahun persetujuan, kode bentuk sediaan).
6. **Q1–Q3 Scientific Evidence Scout**:
   - Synthesizes peer-reviewed open-source literature (Scopus Q1–Q3 / PubMed) to justify biowaivers, novel excipient safety, and biomarker standardization when statutory clauses require empirical proof.

---

## Quick Start

### 1. Launch the Application
Double-click `run_guppy.bat` or run in PowerShell:
```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m streamlit run guppy\frontend\app.py
```
Then open your browser at `http://localhost:8501`.

### 2. Run the Automated Tests
Double-click `run_tests.bat` or run:
```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m pytest tests/ -v
```

---

## Project Structure

```text
.
├── .agents/skills/pharma-regulatory-helper/  # Antigravity skill & reference runbooks
├── guppy/
│   ├── backend/
│   │   ├── config.py                         # App configuration and paths
│   │   ├── models/
│   │   │   ├── product.py                    # ProductCase, Stability, and Manufacturing models
│   │   │   └── dossier.py                    # Scorecard and GapFinding models
│   │   ├── engine/
│   │   │   ├── classifier.py                 # Product classification decision trees
│   │   │   ├── gap_analyzer.py               # ACTD rule-based gap checker
│   │   │   ├── jurisdiction_comparator.py    # Multi-agency benchmarking (BPOM/FDA/EMA/ICH)
│   │   │   ├── literature_scout.py           # Q1-Q3 open-access evidence retrieval
│   │   │   └── roadmap_calculator.py         # BPOM SLAs, timeline calculator, NIE decoder
│   │   └── knowledge/
│   │       ├── regulations_db.json           # Indexed statutes and PerBPOM articles
│   │       ├── compendia_index.json          # Farmakope Indonesia VI monographs
│   │       └── actd_rules.json               # Full ACTD Parts I-IV regulatory rules
│   └── frontend/
│       ├── app.py                            # Streamlit interactive application
│       └── assets/
│           └── style.css                     # Custom styling
├── tests/
│   ├── test_classifier.py                    # Tests for product classification
│   ├── test_gap_analyzer.py                  # Tests for gap analysis & scoring
│   └── test_roadmap.py                       # Tests for timeline & NIE decoding
├── requirements.txt                          # Dependencies
├── run_guppy.bat                             # One-click app launcher
└── run_tests.bat                             # One-click test runner
```

## Pembaruan data Fornas (KMK HK.01.07/MENKES/1199/2025)
- Data baru: `guppy/backend/knowledge/fornas_2025.json` (diekstrak dari PDF dengan `tools/build_fornas_db.py`).
- Engine baru (logika tiga nilai): `guppy/backend/engine/fornas_matcher.py`. Engine lama `fornas_engine.py` dan `fornas_db.json` (11 obat, Fornas 2022) USANG dan hanya dipertahankan sementara.
- Pemetaan ICD-10 (`icd10_usulan`) dan `sifat_usulan` hanyalah usulan kata kunci; wajib ditinjau apoteker/KFT. Entri `perlu_tinjauan` harus dicek ke PDF.
- Regenerasi: `python tools/build_fornas_db.py <pdf> guppy/backend/knowledge/fornas_2025.json`
