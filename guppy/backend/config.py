"""Application configuration and constants for Guppy - Regulatory Helper (Clinical Focus)."""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
KNOWLEDGE_DIR = BACKEND_DIR / "knowledge"

# Knowledge DB Paths
REGULATIONS_DB_PATH = KNOWLEDGE_DIR / "regulations_db.json"
FORNAS_DB_PATH = KNOWLEDGE_DIR / "fornas_db.json"          # LEGACY (11 obat, Fornas 2022) - jangan dipakai untuk data baru
FORNAS_2025_DB_PATH = KNOWLEDGE_DIR / "fornas_2025.json"   # data baru, diekstrak dari KMK 1199/2025
ACTD_RULES_PATH = KNOWLEDGE_DIR / "actd_rules.json"
COMPENDIA_INDEX_PATH = KNOWLEDGE_DIR / "compendia_index.json"

# Fornas Program Info
FORNAS_EDITION = "Fornas 2025"
FORNAS_KEPMENKES = "Kepmenkes No. HK.01.07/MENKES/1199/2025"
FORNAS_BERLAKU = "Penerapan mulai 1 April 2026 (mencabut KMK 2197/2023 dan 1818/2024)"
FORNAS_PROGRAM = "Jaminan Kesehatan Nasional (JKN) – BPJS Kesehatan"

# Facility Levels (JKN)
FACILITY_LEVELS = ["FKTP (Puskesmas / Klinik Pratama)", "FKRTL (Rumah Sakit / Klinik Utama)"]
PRESCRIBER_TYPES = ["DU (Dokter Umum)", "SP (Dokter Spesialis)", "SP-Sub (Dokter Subspesialis / Konsultan)"]

# ICD-10 Common Diagnosis Codes (quick reference for UI)
COMMON_ICD10 = {
    "J18 — Pneumonia (PNPK Kemenkes 2025)": "J18",
    "N39.0 — Infeksi Saluran Kemih / ISK (PNPK Kemenkes 2025)": "N39.0",
    "M17 — Osteoartritis Lutut & Sendi (PNPK Kemenkes 2025)": "M17",
    "F20 — Skizofrenia (PNPK Kemenkes 2025)": "F20",
    "K74 — Sirosis Hati pada Dewasa (PNPK Kemenkes 2025)": "K74",
    "E66 — Obesitas Dewasa (PNPK Kemenkes 2025)": "E66",
    "C91.0 — Leukemia Limfoblastik Akut Anak (PNPK Kemenkes 2025)": "C91.0",
    "K05 — Penyakit Periodontal / Gigi & Mulut (PNPK Kemenkes 2025)": "K05",
    "H16.0 — Ulkus Kornea Bakteri (PNPK Kemenkes 2025)": "H16.0",
    "E11 — Diabetes Melitus Tipe 2 (Fornas)": "E11",
    "E10 — Diabetes Melitus Tipe 1 (Fornas)": "E10",
    "I10 — Hipertensi Esensial (Fornas)": "I10",
    "I50.9 — Gagal Jantung Kongestif (Fornas)": "I50.9",
    "E78 — Dislipidemia / Hiperkolesterolemia (Fornas)": "E78",
    "K21 — GERD / Refluks Gastroesofageal (Fornas)": "K21",
    "J45 — Asma Bronkial (Fornas)": "J45",
    "G40 — Epilepsi (Fornas)": "G40",
    "M10 — Gout / Artritis Pirai (Fornas)": "M10",
    "A15 — Tuberkulosis / TB Paru (Fornas)": "A15",
    "N04 — Sindrom Nefrotik (Fornas)": "N04",
}
