"""Ekstrak tabel Fornas (KMK HK.01.07/MENKES/1199/2025) dari PDF menjadi JSON terstruktur.

Pemakaian:  python tools/build_fornas_db.py <path-pdf> <path-output.json>

Prinsip:
- Teks restriksi disalin apa adanya (tidak ditafsirkan). Tingkat restriksi (kelas / zat aktif / sediaan)
  mengikuti posisi pada tabel sesuai ketentuan penulisan Fornas butir k.
- Hal yang ambigu secara tata letak ditandai di `perlu_tinjauan`, bukan ditebak.
- Pemetaan ICD-10 dan `sifat_usulan` hanya USULAN berbasis kata kunci; wajib ditinjau apoteker/KFT.
"""
import json
import re
import sys
from datetime import date

import pdfplumber

COL1_MAX = 85          # kolom kelas/no. item
MAIN_MAX = 320         # kolom nama/sediaan/restriksi
TP_RANGE = (320, 365)  # FPKTP
TL_RANGE = (365, 420)  # FPKTL
MAX_RANGE = (420, 548) # peresepan maksimal
OEN_MIN = 548
CHECK = "\uf0d6"

MARKER_RE = re.compile(r"^([a-z]\)|\d+\)|[-\u2013\u2022])$")
HEADING_NUM_RE = re.compile(r"^\d+(\.\d+)*\.?$")
ITEM_NUM_RE = re.compile(r"^\d+$")
SED_NUM_RE = re.compile(r"^\d+\.$")

# ---- usulan sifat restriksi & ICD-10 (kata kunci, konservatif; WAJIB ditinjau manusia) ----
SIFAT_KATA_KUNCI = {
    "keselamatan": ["tidak diberikan", "tidak boleh", "kontraindikasi", "hamil", "menyusui", "anak", "usia",
                    "gagal ginjal", "gangguan fungsi", "tahun", "bayi", "neonatus", "gagal jantung"],
    "kendali_biaya": ["jika setelah", "bila setelah", "tidak responsif", "tidak respons", "gagal", "lini",
                      "tidak dapat mencapai", "tidak mencapai target", "setelah pemberian", "kombinasi"],
    "administratif": ["hanya boleh diresepkan", "hanya dapat diberikan di", "tim ", "dokter spesialis",
                      "spesialis", "diresepkan oleh", "fpktl", "rumah sakit", "initial"],
}
NEGASI = ("tidak ", "bukan ", "kontraindikasi", "kecuali", "jangan ")
ICD_KATA_KUNCI = [
    ("diabetes melitus tipe 2", ["E11"]), ("diabetes melitus tipe 1", ["E10"]),
    ("diabetes melitus", ["E10-E14"]), ("hipertensi", ["I10-I15"]), ("gagal jantung", ["I50"]),
    ("angina", ["I20"]), ("infark", ["I21-I22"]), ("stroke", ["I63-I64"]),
    ("hiperlipidemia", ["E78"]), ("dislipidemia", ["E78"]), ("asma", ["J45"]), ("ppok", ["J44"]),
    ("tuberkulosis", ["A15-A19"]), ("hiv", ["B20-B24"]), ("epilepsi", ["G40"]), ("gout", ["M10"]),
    ("pirai", ["M10"]), ("malaria", ["B50-B54"]), ("pneumonia", ["J12-J18"]),
    ("infeksi saluran kemih", ["N39.0"]), ("hepatitis b", ["B16", "B18"]), ("sindrom nefrotik", ["N04"]),
    ("migrain", ["G43"]), ("skizofrenia", ["F20"]), ("depresi", ["F32-F33"]), ("parkinson", ["G20"]),
    ("hipotiroid", ["E03"]), ("hipertiroid", ["E05"]), ("glaukoma", ["H40"]), ("anemia", ["D50-D64"]),
    ("kanker", ["C00-C97"]), ("gerd", ["K21"]), ("refluks", ["K21"]), ("tukak", ["K25-K27"]),
]


def sifat_usulan(teks):
    t = teks.lower()
    return [k for k, kws in SIFAT_KATA_KUNCI.items() if any(w in t for w in kws)]


def icd_usulan(teks):
    """Usulan kode ICD-10 dari kalimat yang TIDAK mengandung negasi (hindari memetakan kontraindikasi)."""
    hasil, terlihat = [], set()
    kalimat = re.split(r"(?<=[.;:])\s+", teks)
    for k in kalimat:
        kl = k.lower()
        if any(n in kl for n in NEGASI):
            continue
        for kata, kodes in ICD_KATA_KUNCI:
            if re.search(r"\b" + re.escape(kata) + r"\b", kl):
                for kode in kodes:
                    if kode not in terlihat:
                        terlihat.add(kode)
                        hasil.append({"kode": kode, "kata_kunci": kata, "status": "USULAN_BELUM_DITINJAU"})
    return hasil


def clean_flags(name):
    flags = {"P": False, "Ca": False, "PRB": False}
    if "[P]" in name:
        flags["P"] = True
    if "[Ca]" in name:
        flags["Ca"] = True
    if re.search(r"\*+\s*$", name.strip()) or name.strip().endswith("*"):
        flags["PRB"] = True
    name = name.replace("[P]", "").replace("[Ca]", "")
    name = re.sub(r"\*+", "", name)
    return re.sub(r"\s+", " ", name).strip(), flags


def page_lines(page):
    header_bottom = None
    words = page.extract_words(extra_attrs=["size", "fontname"])
    for w in words:
        if w["text"] == "TL" and 365 < w["x0"] < 420 and w["top"] < 260:
            header_bottom = w["bottom"] + 2
    if header_bottom is None:
        return None
    keep = []
    for w in words:
        if w["top"] < header_bottom or w["top"] > 895:
            continue
        if w["size"] > 20 or w["text"].startswith("jdih"):
            continue
        if "BoldItalic" in w["fontname"] and w["size"] < 10:   # watermark KEMENTERIAN KESEHATAN
            continue
        keep.append(w)
    keep.sort(key=lambda w: (w["top"], w["x0"]))
    lines, cur, cur_top = [], [], None
    for w in keep:
        if cur_top is None or abs(w["top"] - cur_top) <= 3:
            cur.append(w)
            cur_top = w["top"] if cur_top is None else cur_top
        else:
            lines.append(sorted(cur, key=lambda x: x["x0"]))
            cur, cur_top = [w], w["top"]
    if cur:
        lines.append(sorted(cur, key=lambda x: x["x0"]))
    return lines


def split_line(ws):
    col1 = [w for w in ws if w["x0"] < COL1_MAX and w["text"] != CHECK]
    main = [w for w in ws if COL1_MAX <= w["x0"] < MAIN_MAX and w["text"] != CHECK]
    tp = any(w["text"] == CHECK and TP_RANGE[0] <= w["x0"] < TP_RANGE[1] for w in ws)
    tl = any(w["text"] == CHECK and TL_RANGE[0] <= w["x0"] < TL_RANGE[1] for w in ws)
    oen = any(w["text"] == CHECK and w["x0"] >= OEN_MIN for w in ws)
    pp = any(w["text"] == "PP" and TP_RANGE[0] <= w["x0"] < TP_RANGE[1] for w in ws)
    mx = [w for w in ws if MAX_RANGE[0] <= w["x0"] < MAX_RANGE[1] and w["text"] != CHECK]
    return col1, main, tp, tl, oen, pp, mx


def join(ws):
    return " ".join(w["text"] for w in ws).strip()


def add_restr(buf, first_tok, text):
    if MARKER_RE.match(first_tok) or not buf:
        buf.append(text)
    else:
        buf[-1] += " " + text


def build(pdf_path):
    pdf = pdfplumber.open(pdf_path)
    kelas_stack = {}          # level -> (kode, nama)
    kelas_restr = {}          # kode -> {"buf": [], "halaman": n}
    obat_list = []
    cur = None                # obat saat ini
    sed = None                # sediaan saat ini
    state = "KELAS"           # KELAS | NAME | RESTR_ZAT | SED | RESTR_SED
    heading_open = False
    cur_kelas = None
    anomali = []
    first_table_page = last_table_page = None

    for pno, page in enumerate(pdf.pages, start=1):
        lines = page_lines(page)
        if lines is None:
            continue
        first_table_page = first_table_page or pno
        last_table_page = pno
        top_of_page = True
        for ws in lines:
            col1, main, tp, tl, oen, pp, mx = split_line(ws)
            main_txt, mx_txt = join(main), join(mx)
            if not (col1 or main or tp or tl or oen or mx):
                continue
            first_main = main[0]["text"] if main else ""

            # ---------- heading kelas terapi ----------
            if col1 and col1[0]["x0"] < 45 and HEADING_NUM_RE.match(col1[0]["text"]) and (len(col1) > 1 or main):
                kode = col1[0]["text"].rstrip(".")
                nama = join(col1[1:] + main)
                level = kode.count(".") + 1
                kelas_stack = {l: v for l, v in kelas_stack.items() if l < level}
                kelas_stack[level] = (kode, nama)
                cur_kelas = kode
                kelas_restr.setdefault(kode, {"buf": [], "halaman": pno})
                cur, sed, state, heading_open = None, None, "KELAS", True
                continue
            if col1 and heading_open and not ITEM_NUM_RE.match(col1[0]["text"]):
                lv = max(kelas_stack)
                kode, nama = kelas_stack[lv]
                kelas_stack[lv] = (kode, nama + " " + join(col1 + main))
                continue
            heading_open = False

            # ---------- item zat aktif ----------
            if col1 and len(col1) == 1 and 45 <= col1[0]["x0"] < 80 and ITEM_NUM_RE.match(col1[0]["text"]) and main:
                name, flags = clean_flags(main_txt)
                cur = {
                    "no_item": int(col1[0]["text"]),
                    "kelas_kode": cur_kelas,
                    "kelas_path": [{"kode": kelas_stack[l][0], "nama": kelas_stack[l][1]} for l in sorted(kelas_stack)],
                    "zat_aktif": name, "penanda": flags, "halaman_pdf": pno,
                    "restriksi_zat_aktif_buf": [], "sediaan": [], "perlu_tinjauan": [],
                    "fasilitas_tingkat_zat": None, "raw": [main_txt],
                }
                obat_list.append(cur)
                sed, state = None, "NAME"
                if tp or tl or oen or mx_txt:
                    cur["fasilitas_tingkat_zat"] = {"fpktp": tp, "fpktl": tl, "oen": oen, "pp": pp, "peresepan_maksimal": mx_txt}
                    cur["perlu_tinjauan"].append("tanda/peresepan maksimal pada baris zat aktif")
                continue

            # ---------- sediaan bernomor ----------
            if main and 88 <= main[0]["x0"] < 135 and SED_NUM_RE.match(first_main) and len(main) > 1 and main[1]["x0"] - main[0]["x0"] >= 15 and cur is not None:
                txt = join(main[1:])
                sed = {
                    "no": int(first_main.rstrip(".")), "sediaan_raw": txt, "prb": False,
                    "fpktp": tp, "fpktl": tl, "pp": pp, "oen": oen,
                    "peresepan_maksimal": mx_txt, "restriksi_buf": [], "halaman_pdf": pno,
                    "flags_tinjauan": [],
                }
                if top_of_page and mx_txt and mx_txt[:1].islower() and cur["sediaan"]:
                    prev = cur["sediaan"][-1]
                    if prev["peresepan_maksimal"] and not prev["peresepan_maksimal"].rstrip().endswith("."):
                        prev["flags_tinjauan"].append("peresepan maksimal mungkin terpotong ke halaman berikutnya")
                        sed["flags_tinjauan"].append("peresepan maksimal diawali lanjutan teks halaman sebelumnya")
                cur["sediaan"].append(sed)
                state = "SED"
                top_of_page = False
                continue
            elif cur is None and main_txt and state == "KELAS":
                add_restr(kelas_restr.setdefault(cur_kelas, {"buf": [], "halaman": pno})["buf"], first_main, main_txt)
                top_of_page = False
                continue

            # ---------- lanjutan sel (tanda / peresepan maksimal / teks) ----------
            if (tp or tl or oen or mx_txt) and sed is not None and not (main_txt and state in ("RESTR_SED",) and not mx_txt):
                if mx_txt:
                    sed["peresepan_maksimal"] = (sed["peresepan_maksimal"] + " " + mx_txt).strip()
                sed["fpktp"] |= tp
                sed["fpktl"] |= tl
                sed["oen"] |= oen
                sed["pp"] |= pp
            elif (tp or tl or oen or mx_txt) and sed is None and cur is not None:
                anomali.append((pno, cur["zat_aktif"], "tanda/maks tanpa sediaan", main_txt[:40], mx_txt[:40]))

            if not main_txt or cur is None:
                top_of_page = False
                continue

            is_marker = bool(MARKER_RE.match(first_main))
            cur["raw"].append((main_txt + (" || " + mx_txt if mx_txt else "")).strip())
            if state == "NAME":
                if (first_main[:1].islower() or first_main[:1] in "+(") and not is_marker:
                    cur["zat_aktif"], f2 = clean_flags(cur["zat_aktif"] + " " + main_txt)
                    cur["penanda"] = {k: cur["penanda"][k] or f2[k] for k in f2}
                    cur["perlu_tinjauan"].append("nama zat aktif lebih dari satu baris")
                else:
                    state = "RESTR_ZAT"
                    add_restr(cur["restriksi_zat_aktif_buf"], first_main, main_txt)
            elif state == "RESTR_ZAT":
                add_restr(cur["restriksi_zat_aktif_buf"], first_main, main_txt)
            elif state == "SED":
                if (first_main[:1].islower() or first_main[:1].isdigit() or first_main[:1] in "(+") and not is_marker:
                    sed["sediaan_raw"] += " " + main_txt
                else:
                    state = "RESTR_SED"
                    add_restr(sed["restriksi_buf"], first_main, main_txt)
            elif state == "RESTR_SED":
                add_restr(sed["restriksi_buf"], first_main, main_txt)
            top_of_page = False

    # ---------- finalisasi ----------
    out = []
    for i, o in enumerate(obat_list, start=1):
        restr_zat = [r for r in o.pop("restriksi_zat_aktif_buf")]
        o["id"] = f"FN-{i:04d}"
        o["restriksi_zat_aktif"] = [{"teks": t, "halaman_pdf": o["halaman_pdf"]} for t in restr_zat]
        n_sed = len(o["sediaan"])
        for j, s in enumerate(o["sediaan"]):
            raw = s["sediaan_raw"]
            nm, fl = clean_flags(raw)
            s["sediaan"], s["prb"] = nm, fl["PRB"]
            s["penanda_P"], s["penanda_Ca"] = fl["P"], fl["Ca"]
            s.pop("sediaan_raw")
            buf = s.pop("restriksi_buf")
            s["restriksi_sediaan"] = []
            for t in buf:
                item = {"teks": t, "halaman_pdf": s["halaman_pdf"]}
                if j == n_sed - 1:
                    item["perlu_tinjauan_cakupan"] = True   # bisa berlaku untuk zat aktif, bukan hanya sediaan terakhir
                s["restriksi_sediaan"].append(item)
        if o["zat_aktif"].lower().endswith("*"):
            o["penanda"]["PRB"] = True
        # sel peresepan maksimal yang menyatu lintas baris/halaman: teks baris berikutnya diawali huruf kecil
        # dan teks sebelumnya belum berakhir titik -> gabungkan dan berlakukan ke semua sediaan dalam sel itu
        seds = o["sediaan"]
        k = 0
        while k < len(seds) - 1:
            grp = [k]
            while (grp[-1] + 1 < len(seds)
                   and seds[grp[-1]]["peresepan_maksimal"] and not seds[grp[-1]]["peresepan_maksimal"].rstrip().endswith(".")
                   and seds[grp[-1] + 1]["peresepan_maksimal"][:1].islower()):
                grp.append(grp[-1] + 1)
            if len(grp) > 1:
                gab = " ".join(seds[g]["peresepan_maksimal"] for g in grp)
                for g in grp:
                    seds[g]["peresepan_maksimal"] = gab
                    seds[g]["flags_tinjauan"] = [f for f in seds[g]["flags_tinjauan"] if "terpotong" not in f and "lanjutan teks" not in f]
                    seds[g]["flags_tinjauan"].append("peresepan maksimal berasal dari sel gabungan beberapa sediaan; cek PDF")
            k = grp[-1] + 1
        raw = o.pop("raw", [])
        if not o["sediaan"]:
            o["perlu_tinjauan"].append("tidak ada sediaan terbaca; tata letak tidak baku (paket/kombipak?) - cek PDF")
            o["teks_mentah"] = "\n".join(raw)[:3000]
        if MARKER_RE.match(o["zat_aktif"].split(" ")[0]) or len(o["zat_aktif"]) > 90:
            o["perlu_tinjauan"].append("nama zat aktif tampak tidak wajar (baris terpotong halaman / kombinasi panjang)")
        gabungan = " ".join(r["teks"] for r in o["restriksi_zat_aktif"] +
                            [x for s in o["sediaan"] for x in s["restriksi_sediaan"]])
        kr = []
        for lv in o["kelas_path"]:
            kr += kelas_restr.get(lv["kode"], {"buf": []})["buf"]
        gabungan_all = " ".join(kr) + " " + gabungan
        o["sifat_usulan"] = sifat_usulan(gabungan_all) if gabungan_all.strip() else []
        o["icd10_usulan"] = icd_usulan(gabungan_all) if gabungan_all.strip() else []
        out.append(o)

    kelas = []
    for kode, v in kelas_restr.items():
        kelas.append({"kode": kode, "restriksi": [{"teks": t, "halaman_pdf": v["halaman"]} for t in v["buf"]]})
    return out, kelas, anomali, (first_table_page, last_table_page)


def main(pdf_path, out_path):
    obat, kelas, anomali, (p1, p2) = build(pdf_path)
    n_sed = sum(len(o["sediaan"]) for o in obat)
    db = {
        "metadata": {
            "sumber": "Keputusan Menteri Kesehatan RI Nomor HK.01.07/MENKES/1199/2025 tentang Formularium Nasional",
            "ditetapkan": "2025-12-31", "penerapan_mulai": "2026-04-01",
            "mencabut": ["HK.01.07/MENKES/2197/2023", "HK.01.07/MENKES/1818/2024"],
            "diktum_obat_luar_fornas": "KELIMA: obat lain dapat digunakan secara terbatas berdasarkan persetujuan "
                                       "kepala/direktur fasilitas pelayanan kesehatan setempat sesuai peraturan perundang-undangan.",
            "halaman_tabel_pdf": [p1, p2],
            "dibuat_pada": date.today().isoformat(),
            "skema_versi": "2.0",
            "legenda": {
                "fpktp": "centang kolom FPKTP: dipakai di fasilitas tingkat pertama",
                "pp": "centang + 'PP' di kolom FPKTP: dipakai di Puskesmas Perawatan",
                "fpktl": "centang kolom FPKTL: dipakai di fasilitas tingkat lanjut",
                "prb": "tanda * : dapat disediakan FPKTP/apotek PRB untuk program rujuk balik",
                "P": "[P]: pengadaan oleh program Kemenkes/BKKBN", "Ca": "[Ca]: antineoplastik/imunomodulator terapi kanker",
                "oen": "centang kolom OEN: obat esensial nasional",
                "tingkat_restriksi": "kelas terapi -> berlaku untuk semua item di kelas; zat aktif -> semua kekuatan/sediaan; "
                                     "kekuatan/sediaan -> hanya sediaan itu (ketentuan penulisan butir k)",
            },
            "catatan_kualitas": "Diekstrak otomatis dari PDF. Teks restriksi disalin apa adanya. 'icd10_usulan' dan "
                                "'sifat_usulan' adalah USULAN kata kunci dan wajib ditinjau apoteker/KFT sebelum dipakai "
                                "untuk keputusan. Entri dengan 'perlu_tinjauan' wajib dicek ke PDF.",
            "statistik": {"zat_aktif": len(obat), "sediaan": n_sed,
                          "perlu_tinjauan": sum(1 for o in obat if o["perlu_tinjauan"] or any(s["flags_tinjauan"] for s in o["sediaan"]))},
        },
        "restriksi_kelas": kelas,
        "obat": obat,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=1)
    print("zat aktif:", len(obat), "| sediaan:", n_sed, "| halaman tabel:", p1, "-", p2)
    print("anomali:", len(anomali))
    for a in anomali[:15]:
        print("  ", a)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
