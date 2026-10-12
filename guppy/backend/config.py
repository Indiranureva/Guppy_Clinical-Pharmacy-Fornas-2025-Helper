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
    "E11 — Diabetes Melitus Tipe 2": "E11",
    "E10 — Diabetes Melitus Tipe 1": "E10",
    "I10 — Hipertensi Esensial (Primer)": "I10",
    "I50.9 — Gagal Jantung, tidak spesifik": "I50.9",
    "E78.5 — Hiperlipidemia Campuran": "E78.5",
    "E78.0 — Hiperkolesterolemia Murni": "E78.0",
    "K21.0 — GERD dengan Esofagitis": "K21.0",
    "K21.9 — GERD tanpa Esofagitis": "K21.9",
    "J18.9 — Pneumonia, tidak spesifik": "J18.9",
    "J06.9 — ISPA Atas Akut, tidak spesifik": "J06.9",
    "N39.0 — ISK tanpa komplikasi": "N39.0",
    "R52 — Nyeri, tidak spesifik": "R52",
    "R05 — Batuk": "R05",
    "N04 — Sindrom Nefrotik": "N04",
}
