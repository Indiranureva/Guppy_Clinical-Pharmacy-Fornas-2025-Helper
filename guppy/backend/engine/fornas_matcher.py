"""Penilai kesesuaian resep terhadap Fornas (KMK HK.01.07/MENKES/1199/2025) dengan logika tiga nilai.

Per kriteria hasilnya salah satu dari:
    TERPENUHI | TIDAK_TERPENUHI | TIDAK_DIKETAHUI
Data yang kosong TIDAK dianggap gagal (TIDAK_DIKETAHUI). Teks restriksi klinis tidak ditafsirkan oleh
mesin; teks ditampilkan apa adanya untuk diverifikasi manusia, kecuali pemetaan diagnosis sudah berstatus
"DITINJAU" oleh apoteker/KFT. Mesin hanya merekomendasikan; keputusan akhir ada pada dokter/apoteker/KFT.

Status keseluruhan: SESUAI | DATA_KURANG | PERLU_JUSTIFIKASI | TIDAK_SESUAI | ESKALASI
"""
from __future__ import annotations

import difflib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

_DB_PATH = Path(__file__).resolve().parent.parent / "knowledge" / "fornas_2025.json"
_DB: Optional[Dict[str, Any]] = None

T, F, U = "TERPENUHI", "TIDAK_TERPENUHI", "TIDAK_DIKETAHUI"
FACILITY_ALIAS = {"FKTP": "FPKTP", "FPKTP": "FPKTP", "FKRTL": "FPKTL", "FPKTL": "FPKTL", "FKTL": "FPKTL"}
_UNITS = r"(tab|kaps|amp|btl|botol|vial|patch|tube|supp|sach|kapl|tablet|kapsul|ampul|flakon|pen|cartridge)"
_MAX_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*" + _UNITS + r"[a-z]*\s*/\s*(bulan|hari|minggu|kasus|kunjungan|resep)", re.I)


def get_db() -> Dict[str, Any]:
    global _DB
    if _DB is None:
        with open(_DB_PATH, "r", encoding="utf-8") as f:
            _DB = json.load(f)
    return _DB


def fornas_label() -> str:
    m = get_db()["metadata"]
    kmk = m["sumber"].split("Nomor ")[-1].split(" tentang")[0]
    return f"Fornas (KMK {kmk}, penerapan mulai {m['penerapan_mulai']})"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[*\[\]]", "", s.lower())).strip()


def search(query: str) -> List[Dict[str, Any]]:
    """Cari entri zat aktif. Satu zat aktif dapat muncul di beberapa kelas terapi (sesuai indikasi)."""
    q = _norm(query)
    obat = get_db()["obat"]
    exact = [o for o in obat if _norm(o["zat_aktif"]) == q]
    return exact or [o for o in obat if q and q in _norm(o["zat_aktif"])]


def suggest_names(query: str, n: int = 5) -> List[str]:
    names = sorted({_norm(o["zat_aktif"]) for o in get_db()["obat"] if len(o["zat_aktif"]) < 60})
    return difflib.get_close_matches(_norm(query), names, n=n, cutoff=0.7)


def _match_sediaan(entry: Dict[str, Any], sediaan: Optional[str]) -> Optional[Dict[str, Any]]:
    if not sediaan:
        return None
    q = _norm(sediaan)
    for s in entry["sediaan"]:
        if _norm(s["sediaan"]) == q:
            return s
    hits = [s for s in entry["sediaan"] if q in _norm(s["sediaan"])]
    return hits[0] if len(hits) == 1 else None


def _parse_max(text: str, facility: Optional[str]) -> Optional[Dict[str, Any]]:
    """Ambil batas sederhana 'N satuan/periode'. Kembalikan None bila ambigu (mis. banyak aturan)."""
    if not text:
        return None
    parts = [text]
    if "FPKTP" in text or "FPKTL" in text:
        parts = [p for p in re.split(r"(?=FPKT[PL]\s*:)", text) if facility and p.startswith(facility)] or []
    found = []
    for p in parts:
        found += _MAX_RE.findall(p)
    if len(found) != 1:
        return None
    jml, unit, per = found[0]
    return {"jumlah": float(jml.replace(",", ".")), "satuan": unit.lower()[:3], "per": per.lower()}


def _crit(cid, jenis, hasil, alasan, **extra):
    d = {"id": cid, "jenis": jenis, "hasil": hasil, "alasan": alasan}
    d.update(extra)
    return d


def _restriksi_berlaku(entry, sed) -> List[Dict[str, Any]]:
    out = []
    for kr in get_db()["restriksi_kelas"]:
        if any(kr["kode"] == lv["kode"] for lv in entry["kelas_path"]):
            out += [dict(tingkat="kelas_terapi", kelas=kr["kode"], **r) for r in kr["restriksi"]]
    out += [dict(tingkat="zat_aktif", **r) for r in entry["restriksi_zat_aktif"]]
    seds = [sed] if sed else entry["sediaan"]
    for s in seds:
        for r in s["restriksi_sediaan"]:
            out.append(dict(tingkat="sediaan", sediaan=s["sediaan"], hanya_jika_sediaan_dipilih=bool(sed), **r))
    return out


def _evaluate_entry(entry, sediaan, facility, patient, quantity, rujuk_balik) -> Dict[str, Any]:
    krit: List[Dict[str, Any]] = []
    just: List[str] = []
    minta: List[str] = []
    warn: List[str] = []
    sed = _match_sediaan(entry, sediaan)

    # 1. sediaan/kekuatan tercantum?
    if sediaan and sed is None:
        krit.append(_crit("K-SEDIAAN", "terdaftar", F,
                          f"Sediaan/kekuatan '{sediaan}' tidak tercantum untuk {entry['zat_aktif']} pada kelas {entry['kelas_kode']}.",
                          sediaan_tercantum=[s["sediaan"] for s in entry["sediaan"]]))
        just.append("OBAT_LUAR_FORNAS")
    elif not sediaan and len(entry["sediaan"]) > 1:
        minta.append("Sediaan/kekuatan yang diresepkan")
        krit.append(_crit("K-SEDIAAN", "terdaftar", U, "Sediaan/kekuatan belum disebutkan.",
                          sediaan_tercantum=[s["sediaan"] for s in entry["sediaan"]]))
    else:
        sed = sed or (entry["sediaan"][0] if entry["sediaan"] else None)
        krit.append(_crit("K-SEDIAAN", "terdaftar", T, "Zat aktif dan sediaan tercantum dalam Fornas."))

    # 2. fasilitas
    fac = FACILITY_ALIAS.get((facility or "").upper())
    if sed is not None:
        if not fac:
            minta.append("Tingkat fasilitas (FPKTP/FPKTL)")
            krit.append(_crit("K-FASILITAS", "fasilitas", U, "Tingkat fasilitas belum diberikan."))
        else:
            ok = sed["fpktp"] if fac == "FPKTP" else sed["fpktl"]
            if ok:
                krit.append(_crit("K-FASILITAS", "fasilitas", T, f"Sediaan ditandai untuk {fac}."))
            elif fac == "FPKTP" and sed.get("prb"):
                if rujuk_balik is True:
                    krit.append(_crit("K-FASILITAS", "fasilitas", T, "Tanda * (rujuk balik): dapat diberikan FPKTP/apotek PRB."))
                elif rujuk_balik is None:
                    minta.append("Apakah pasien dalam program rujuk balik (PRB)?")
                    krit.append(_crit("K-FASILITAS", "fasilitas", U, "Obat ber-tanda * hanya untuk PRB di FPKTP; status PRB belum diketahui."))
                else:
                    krit.append(_crit("K-FASILITAS", "fasilitas", F, "Tidak ditandai FPKTP dan pasien bukan PRB."))
                    just.append("RUJUK_BALIK")
            else:
                krit.append(_crit("K-FASILITAS", "fasilitas", F, f"Sediaan tidak ditandai untuk {fac}."))
                just.append("LAINNYA")
                warn.append("Pertimbangkan rujukan atau alternatif pada tingkat fasilitas ini; jangan menunda terapi yang mendesak.")

        # 3. peresepan maksimal
        mx = sed["peresepan_maksimal"].strip()
        if not mx:
            krit.append(_crit("K-MAKSIMAL", "kuantitas", T, "Tidak ada batas peresepan maksimal tertulis."))
        else:
            batas = _parse_max(mx, fac)
            if quantity and batas and quantity.get("per") == batas["per"] and (quantity.get("satuan") or "")[:3].lower() == batas["satuan"]:
                if quantity["jumlah"] <= batas["jumlah"]:
                    krit.append(_crit("K-MAKSIMAL", "kuantitas", T, f"Jumlah {quantity['jumlah']:g} dalam batas {batas['jumlah']:g}/{batas['per']}.", teks_fornas=mx))
                else:
                    krit.append(_crit("K-MAKSIMAL", "kuantitas", F, f"Jumlah {quantity['jumlah']:g} melebihi batas {batas['jumlah']:g}/{batas['per']}.", teks_fornas=mx))
                    just.append("PERESEPAN_MAKS_LEBIH")
            else:
                if not quantity:
                    minta.append("Jumlah yang diresepkan (angka, satuan, per periode)")
                krit.append(_crit("K-MAKSIMAL", "kuantitas", U, "Batas tertulis belum bisa dibandingkan otomatis; periksa teks.", teks_fornas=mx))
        if any("sel gabungan" in f or "terpotong" in f for f in sed["flags_tinjauan"]):
            warn.append("Teks peresepan maksimal berasal dari sel gabungan/terpotong halaman; cek PDF halaman %s." % sed["halaman_pdf"])

    # 4. restriksi teks klinis (kelas / zat aktif / sediaan)
    restr = _restriksi_berlaku(entry, sed)
    if not restr:
        krit.append(_crit("K-RESTRIKSI", "indikasi", T, "Tidak ada restriksi penggunaan tertulis pada kelas, zat aktif, maupun sediaan ini."))
    else:
        dx = [d.upper() for d in (patient.get("diagnosis_icd10") or [])]
        reviewed = [m for m in entry["icd10_usulan"] if m.get("status") == "DITINJAU"]
        hint = [m for m in entry["icd10_usulan"] if m.get("status") != "DITINJAU"]
        hasil, alasan = U, "Restriksi berupa teks klinis; belum dapat dinilai otomatis. Verifikasi manual terhadap teks di bawah."
        if reviewed and dx:
            cocok = any(d.startswith(m["kode"].split("-")[0]) for d in dx for m in reviewed)
            hasil, alasan = (T, "Diagnosis cocok dengan pemetaan ICD-10 yang sudah ditinjau.") if cocok else (F, "Diagnosis tidak cocok dengan pemetaan ICD-10 yang sudah ditinjau.")
        elif not dx:
            minta.append("Diagnosis (kode ICD-10) dan data klinis yang disebut pada teks restriksi")
        petunjuk = None
        if hint and dx and hasil == U:
            petunjuk = "Kemungkinan terkait diagnosis (USULAN kata kunci, belum ditinjau): " + ", ".join(m["kode"] for m in hint)
        krit.append(_crit("K-RESTRIKSI", "indikasi", hasil, alasan, restriksi=restr, sifat_usulan=entry["sifat_usulan"], petunjuk=petunjuk))
        if hasil == F:
            just.append("LAINNYA")
        if "keselamatan" in entry["sifat_usulan"] and hasil != T:
            warn.append("Restriksi tampak berkaitan dengan keselamatan (usulan kata kunci); wajib ditinjau apoteker sebelum diputuskan.")
    return {"entri": {"id": entry["id"], "zat_aktif": entry["zat_aktif"], "kelas_kode": entry["kelas_kode"],
                      "kelas": entry["kelas_path"][-1]["nama"] if entry["kelas_path"] else "", "halaman_pdf": entry["halaman_pdf"]},
            "sediaan": sed["sediaan"] if sed else None, "kriteria": krit, "justifikasi": just, "data_diminta": minta,
            "peringatan": warn, "perlu_tinjauan_ekstraksi": entry["perlu_tinjauan"]}


def _status(krit, entry_flags) -> str:
    hasil = [k["hasil"] for k in krit]
    if entry_flags and any("tidak ada sediaan terbaca" in f for f in entry_flags):
        return "ESKALASI"
    if F in hasil:
        return "PERLU_JUSTIFIKASI"
    if U in hasil:
        return "DATA_KURANG"
    return "SESUAI"


def _notifikasi(status, ev, ref) -> List[Dict[str, Any]]:
    n = []
    if status == "SESUAI":
        return n
    if any("keselamatan" in w.lower() for w in ev["peringatan"]):
        n.append({"id_rujukan": ref, "tingkat": "KRITIS", "penerima": "apoteker", "judul": "Tinjau restriksi terkait keselamatan",
                  "isi": "Restriksi Fornas tampak berkaitan dengan keselamatan dan belum bisa dinilai otomatis.",
                  "data_diminta": ev["data_diminta"], "dapat_menunda_terapi": False,
                  "asumsi": ["Tingkat dan penerima memakai default skill; sesuaikan kebijakan fasilitas"]})
    if status in ("DATA_KURANG", "PERLU_JUSTIFIKASI", "ESKALASI"):
        n.append({"id_rujukan": ref, "tingkat": "PENTING", "penerima": "penulis_resep",
                  "judul": "Lengkapi data / justifikasi resep" if status != "ESKALASI" else "Resep perlu ditinjau apoteker",
                  "isi": f"Status penilaian Fornas: {status}.", "data_diminta": ev["data_diminta"],
                  "kode_justifikasi_disarankan": ev["justifikasi"], "dapat_menunda_terapi": False,
                  "asumsi": ["Tenggat default: sebelum kunjungan berikutnya"]})
    return n


def evaluate(drug: str, sediaan: Optional[str] = None, facility: Optional[str] = None,
             patient: Optional[Dict[str, Any]] = None, quantity: Optional[Dict[str, Any]] = None,
             kelas_kode: Optional[str] = None, rujuk_balik: Optional[bool] = None,
             ref: str = "RESEP-TANPA-ID") -> Dict[str, Any]:
    """Nilai satu resep. `quantity` = {"jumlah": 60, "satuan": "tab", "per": "bulan"}."""
    patient = patient or {}
    label = fornas_label()
    entries = search(drug)
    if kelas_kode:
        entries = [e for e in entries if e["kelas_kode"] == kelas_kode] or entries
    base = {"fornas": label, "pemeriksaan_diminta": {"obat": drug, "sediaan": sediaan, "fasilitas": facility}}

    if not entries:
        k = [_crit("K-TERDAFTAR", "terdaftar", F, f"'{drug}' tidak ditemukan dalam {label}.", kemungkinan_maksud=suggest_names(drug))]
        ev = {"kriteria": k, "justifikasi": ["OBAT_LUAR_FORNAS"], "data_diminta": ["Alasan tidak ada alternatif Fornas yang memadai"],
              "peringatan": [get_db()["metadata"]["diktum_obat_luar_fornas"]], "perlu_tinjauan_ekstraksi": []}
        return {**base, "status": "PERLU_JUSTIFIKASI", "evaluasi": [ev], "notifikasi": _notifikasi("PERLU_JUSTIFIKASI", ev, ref),
                "catatan_kepastian": "Keputusan obat di luar Fornas mengikuti Diktum KELIMA dan kebijakan fasilitas; verifikasi aturan terbaru."}

    evs = [_evaluate_entry(e, sediaan, facility, patient, quantity, rujuk_balik) for e in entries]
    if len(evs) > 1 and not kelas_kode:
        status = "DATA_KURANG"
        minta = ["Indikasi/kelas terapi (zat aktif ini tercantum di beberapa kelas): " +
                 "; ".join(f"{e['entri']['kelas_kode']} {e['entri']['kelas']}" for e in evs)]
        ev0 = {"data_diminta": minta, "justifikasi": [], "peringatan": []}
        return {**base, "status": status, "evaluasi": evs, "notifikasi": _notifikasi(status, ev0, ref),
                "catatan_kepastian": "Satu zat aktif dapat tercantum di beberapa kelas sesuai indikasi (ketentuan butir c)."}
    ev = evs[0]
    status = _status(ev["kriteria"], ev["perlu_tinjauan_ekstraksi"])
    return {**base, "status": status, "evaluasi": [ev], "notifikasi": _notifikasi(status, ev, ref),
            "catatan_kepastian": "Teks restriksi diekstrak otomatis dari PDF; pemetaan ICD-10 dan sifat restriksi adalah usulan "
                                 "sampai ditinjau apoteker/KFT."}
