"""Tes engine Fornas 1199/2025 (logika tiga nilai). Jalankan: python -m pytest tests -q"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from guppy.backend.engine import fornas_matcher as fm  # noqa: E402


def hasil(res, cid):
    return {k["id"]: k["hasil"] for k in res["evaluasi"][0]["kriteria"]}[cid]


def test_metformin_850_fpktp_dalam_batas_sesuai():
    r = fm.evaluate("metformin", "tab 850 mg", "FKTP", quantity={"jumlah": 60, "satuan": "tab", "per": "bulan"})
    assert r["status"] == "SESUAI"
    assert hasil(r, "K-FASILITAS") == "TERPENUHI" and hasil(r, "K-MAKSIMAL") == "TERPENUHI"


def test_metformin_1000_mg_tidak_tercantum():
    r = fm.evaluate("metformin", "tab 1000 mg", "FKTP")
    assert r["status"] == "PERLU_JUSTIFIKASI"
    assert "OBAT_LUAR_FORNAS" in r["evaluasi"][0]["justifikasi"]


def test_melebihi_peresepan_maksimal():
    r = fm.evaluate("metformin", "tab 850 mg", "FPKTP", quantity={"jumlah": 90, "satuan": "tab", "per": "bulan"})
    assert hasil(r, "K-MAKSIMAL") == "TIDAK_TERPENUHI"
    assert "PERESEPAN_MAKS_LEBIH" in r["evaluasi"][0]["justifikasi"]


def test_data_kosong_bukan_gagal():
    r = fm.evaluate("metformin", "tab 850 mg")
    assert hasil(r, "K-FASILITAS") == "TIDAK_DIKETAHUI"
    assert r["status"] == "DATA_KURANG"


def test_fentanil_fpktp_tidak_terpenuhi():
    r = fm.evaluate("fentanil", "patch 25 mcg/jam", "FPKTP")
    assert hasil(r, "K-FASILITAS") == "TIDAK_TERPENUHI"


def test_atorvastatin_restriksi_teks_tidak_dinilai_mesin():
    r = fm.evaluate("atorvastatin", "tab sal selaput 20 mg", "FPKTP", patient={"diagnosis_icd10": ["I25"]})
    assert hasil(r, "K-RESTRIKSI") == "TIDAK_DIKETAHUI"
    assert r["status"] in ("DATA_KURANG", "PERLU_JUSTIFIKASI")
    assert r["evaluasi"][0]["kriteria"][-1]["restriksi"]            # teks restriksi ditampilkan apa adanya


def test_obat_di_luar_fornas():
    r = fm.evaluate("obatfiktifxyz")
    assert r["status"] == "PERLU_JUSTIFIKASI"
    assert "kepala/direktur" in r["evaluasi"][0]["peringatan"][0]


def test_tidak_ada_rujukan_fornas_2022():
    r = fm.evaluate("metformin", "tab 500 mg", "FPKTP")
    teks = json.dumps(r, ensure_ascii=False)
    assert "2022" not in teks and "1199/2025" in teks


def test_status_sesuai_tidak_memicu_notifikasi():
    r = fm.evaluate("metformin", "tab 500 mg", "FPKTP", quantity={"jumlah": 100, "satuan": "tab", "per": "bulan"})
    assert r["status"] == "SESUAI" and r["notifikasi"] == []
