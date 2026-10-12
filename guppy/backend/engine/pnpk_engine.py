"""PNPK Integration Engine - Penghubung PNPK 2025 Kemenkes RI dengan Fornas dan Evaluasi Klinis."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
_PNPK_PATH = _KNOWLEDGE_DIR / "pnpk_2025_knowledge.json"
_PNPK_CACHE: Optional[List[Dict[str, Any]]] = None


def get_pnpk_db() -> List[Dict[str, Any]]:
    """Memuat dan menyimpan cache database PNPK 2025."""
    global _PNPK_CACHE
    if _PNPK_CACHE is None:
        try:
            with open(_PNPK_PATH, "r", encoding="utf-8") as f:
                _PNPK_CACHE = json.load(f)
        except Exception:
            _PNPK_CACHE = []
    return _PNPK_CACHE


def get_pnpk_by_drug(drug_name: str) -> List[Dict[str, Any]]:
    """Mencari PNPK terkait zat aktif tertentu."""
    q = drug_name.strip().lower()
    matches = []
    for item in get_pnpk_db():
        # Cek daftar obat terlibat
        if any(q in d.lower() or d.lower() in q for d in item.get("drugs_involved", [])):
            matches.append(item)
            continue
        # Cek di rekomendasi lini pertama / lini kedua
        recs = item.get("clinical_recommendations", {})
        all_recs = recs.get("first_line", []) + recs.get("second_line_or_escalation", [])
        if any(q in r.get("zat_aktif", "").lower() for r in all_recs):
            matches.append(item)
    return matches


def get_pnpk_by_icd10(icd_code: str) -> List[Dict[str, Any]]:
    """Mencari PNPK berdasarkan kode diagnosis ICD-10."""
    clean_icd = icd_code.strip().upper().split(".")[0]
    matches = []
    for item in get_pnpk_db():
        for code in item.get("icd10", []):
            if clean_icd in code.upper() or code.upper().startswith(clean_icd):
                matches.append(item)
                break
    return matches
