"""Guppy - Formularium Nasional (Fornas 2025) & Clinical Pharmacy Helper.

Focused clinical pharmacy decision-support tool for healthcare professionals:
1. Penelusuran Restriksi Obat Fornas 2025 (KMK HK.01.07/MENKES/1199/2025)
2. Evaluasi Resep Pasien & Logika Tiga Nilai (SESUAI, DATA_KURANG, PERLU_JUSTIFIKASI)
3. Pencocokan Diagnosis (ICD-10) ke Terapi Fornas
4. Justifikasi Literatur Klinis Berbasis Bukti (Q1-Q3)
5. Dasar Hukum Regulasi Farmasi Klinis & Fornas
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import json
import streamlit as st

from guppy.backend.engine import fornas_matcher as fm
from guppy.backend.engine import pnpk_engine as pe
from guppy.backend.engine.clinical_literature import ClinicalLiteratureScout
from guppy.backend.security.sanitizer import InputSanitizer
from guppy.backend.security.link_guard import LinkGuard
from guppy.backend.config import (
    REGULATIONS_DB_PATH,
    FORNAS_KEPMENKES,
    FORNAS_EDITION,
    FORNAS_BERLAKU,
    FORNAS_PROGRAM,
    FACILITY_LEVELS,
    PRESCRIBER_TYPES,
    COMMON_ICD10,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Guppy — Clinical Pharmacy & Fornas 2025 Helper",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Clinical Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  .stApp {
    background: linear-gradient(135deg, #0d1117 0%, #0f1923 50%, #0d1117 100%);
    min-height: 100vh;
  }

  .guppy-hero {
    background: linear-gradient(135deg, #0a2540 0%, #1a3a5c 40%, #0d2d45 100%);
    border: 1px solid rgba(56, 182, 255, 0.2);
    border-radius: 16px;
    padding: 24px 30px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
  }
  .guppy-hero-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #e2f4ff;
    margin: 0 0 6px 0;
  }
  .guppy-hero-subtitle {
    font-size: 0.95rem;
    color: #7db8d8;
    margin: 0;
  }
  .guppy-hero-badge {
    display: inline-block;
    background: rgba(56, 182, 255, 0.15);
    border: 1px solid rgba(56, 182, 255, 0.3);
    color: #38b6ff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 10px;
    letter-spacing: 0.04em;
  }

  .badge-r {
    background: rgba(251, 191, 36, 0.15);
    border: 1px solid rgba(251, 191, 36, 0.4);
    color: #fbbf24;
    padding: 3px 10px;
    border-radius: 16px;
    font-size: 0.78rem;
    font-weight: 600;
  }
  .badge-danger {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #f87171;
    padding: 3px 10px;
    border-radius: 16px;
    font-size: 0.78rem;
    font-weight: 600;
  }
  .badge-ok {
    background: rgba(52, 211, 153, 0.15);
    border: 1px solid rgba(52, 211, 153, 0.4);
    color: #34d399;
    padding: 3px 10px;
    border-radius: 16px;
    font-size: 0.78rem;
    font-weight: 600;
  }

  .drug-card {
    background: rgba(15, 25, 40, 0.8);
    border: 1px solid rgba(56, 182, 255, 0.15);
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 14px;
  }
  .drug-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2f4ff;
    margin-bottom: 4px;
  }
  .drug-card-class {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 2px;
  }

  .verdict-ok {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.1));
    border: 1px solid rgba(16, 185, 129, 0.4);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #6ee7b7;
    font-weight: 600;
  }
  .verdict-warn {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.1));
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #fde68a;
    font-weight: 600;
  }
  .verdict-fail {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(185, 28, 28, 0.1));
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #fca5a5;
    font-weight: 600;
  }

  .clinical-warning {
    background: rgba(245, 158, 11, 0.1);
    border-left: 4px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 6px 0;
    color: #fde68a;
    font-size: 0.88rem;
  }
  .clinical-danger {
    background: rgba(239, 68, 68, 0.1);
    border-left: 4px solid #ef4444;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 6px 0;
    color: #fca5a5;
    font-size: 0.88rem;
  }
  .clinical-ok {
    background: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 6px 0;
    color: #6ee7b7;
    font-size: 0.88rem;
  }
  .section-header {
    color: #38b6ff;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 16px 0 10px 0;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(56, 182, 255, 0.2);
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🐟 Guppy")
    st.caption("Asisten Farmasi Klinis & Restriksi Fornas 2025")
    st.markdown("---")

    st.markdown("**📋 Sumber Acuan Resmi:**")
    st.markdown(f"- **{FORNAS_EDITION}**\n  *({FORNAS_KEPMENKES})*")
    st.markdown(f"- **Mulai Berlaku:** 1 April 2026")
    st.markdown(f"- {FORNAS_PROGRAM}")
    st.markdown("- UU No. 17 Tahun 2023 (Kesehatan)")
    st.markdown("- Panduan Praktik Klinis / PNPK Kemenkes")

    st.markdown("---")
    st.markdown("**🛡️ Status Proteksi Sistem & Sumber Data:**")
    sec_light = LinkGuard.get_security_light()
    if sec_light["color"] == "HIJAU":
        st.markdown(
            f"""<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
            <b style="color: #34d399;">🟢 Lampu Hijau: Aman Semua</b><br>
            <small style="color: #a7f3d0;">Seluruh akses website acuan & database dalam kondisi aman terlindungi.</small>
            </div>""",
            unsafe_allow_html=True,
        )
    elif sec_light["color"] == "ORANGE":
        st.markdown(
            f"""<div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
            <b style="color: #fbbf24;">🟠 Lampu Orange: Dibatasi Sementara</b><br>
            <small style="color: #fde68a;">Ada satu atau lebih akses website yang sedang dibatasi sementara.</small>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
            <b style="color: #f87171;">🔴 Lampu Merah: Akses Ditutup Permanen</b><br>
            <small style="color: #fca5a5;">Ada satu atau lebih website yang ditutup permanen karena ancaman keamanan.</small>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("**⚠️ Disclaimer Farmasi Klinis:**")
    st.caption(
        "Guppy adalah sistem pendukung keputusan klinis (CDSS) berbasis KMK 1199/2025 dengan logika 3-nilai. "
        "Keputusan akhir peresepan dan persetujuan klaim tetap berada pada dokter penulis resep, apoteker klinis, "
        "dan Komite Farmasi & Terapi (KFT) fasilitas setempat."
    )
    st.markdown("---")

    # Quick drug search in sidebar
    st.markdown("**🔍 Cari Cepat Obat Fornas:**")
    quick_q = st.text_input("Nama Obat / INN", placeholder="e.g. Fentanil, Metformin", label_visibility="collapsed")
    if quick_q:
        q_clean = InputSanitizer.clean_text(quick_q)
        hits = fm.search(q_clean)
        if hits:
            for h in hits[:4]:
                pen = h.get("penanda", {})
                tag = " [P]" if pen.get("P") else ""
                tag += " [Ca]" if pen.get("Ca") else ""
                tag += " *" if pen.get("PRB") else ""
                st.markdown(f"💊 **{h['zat_aktif'].title()}**{tag}")
                st.caption(f"{h['kelas_path'][-1]['nama'] if h.get('kelas_path') else '-'}")
        else:
            sugg = fm.suggest_names(q_clean, n=3)
            st.caption("Tidak ditemukan." + (f" Maksudnya: {', '.join(sugg)}?" if sugg else ""))


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="guppy-hero">
  <div class="guppy-hero-title">🐟 Guppy — Asisten Farmasi Klinis & Restriksi Fornas 2025</div>
  <div class="guppy-hero-subtitle">
    Sistem Pendukung Keputusan Klinis Berdasarkan Formularium Nasional (KMK No. HK.01.07/MENKES/1199/2025)
  </div>
  <span class="guppy-hero-badge">FORNAS 2025 (KMK 1199/2025) · JKN BPJS KESEHATAN · 775+ ZAT AKTIF · LOGIKA 3-NILAI</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# NAVIGATION TABS (5 Clinical Tabs)
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Penelusuran Obat & Restriksi",
    "⚖️ Evaluasi Resep Pasien (3-Nilai)",
    "🩺 Matching Diagnosis (ICD-10)",
    "📖 Justifikasi Literatur Klinis (Q1-Q3)",
    "📜 Basis Hukum Farmasi Klinis",
])


# ═══════════════════════════════════════════════════════════════
# TAB 1: PENELUSURAN OBAT & RESTRIKSI FORNAS 2025
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Penelusuran Zat Aktif, Sediaan, dan Restriksi Fornas 2025</div>', unsafe_allow_html=True)
    st.markdown(
        "Telusuri **775 zat aktif** dan **1.238 sediaan** resmi Fornas 2025 (KMK 1199/2025). "
        "Melihat ketentuan sediaan, peresepan maksimal, tingkat fasilitas (FPKTP/FPKTL), dan teks restriksi klinis."
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        drug_search_q = st.text_input(
            "Cari Zat Aktif / Kelas Terapi:",
            placeholder="e.g. Parasetamol, Fentanil, Atorvastatin, Morfin, Klopidogrel...",
            value="parasetamol",
        )
    with col2:
        filter_program = st.checkbox("Hanya Obat Program [P]", value=False)
        filter_cancer = st.checkbox("Hanya Obat Kanker [Ca]", value=False)
        filter_prb = st.checkbox("Hanya Rujuk Balik (*)", value=False)

    clean_q = InputSanitizer.clean_text(drug_search_q) if drug_search_q else ""

    if clean_q:
        results = fm.search(clean_q)
        if filter_program:
            results = [r for r in results if r.get("penanda", {}).get("P")]
        if filter_cancer:
            results = [r for r in results if r.get("penanda", {}).get("Ca")]
        if filter_prb:
            results = [r for r in results if r.get("penanda", {}).get("PRB")]

        if not results:
            sugg = fm.suggest_names(clean_q, n=4)
            st.warning(f"Zat aktif '{clean_q}' tidak ditemukan dalam Fornas 2025.")
            if sugg:
                st.info(f"💡 Apakah maksud Anda: **{', '.join(sugg)}**?")
        else:
            st.write(f"Ditemukan **{len(results)}** zat aktif:")
            for item in results:
                pen = item.get("penanda", {})
                badges = []
                if pen.get("P"):
                    badges.append('<span class="badge-r">Program Kemenkes/BKKBN [P]</span>')
                if pen.get("Ca"):
                    badges.append('<span class="badge-danger">Kanker [Ca]</span>')
                if pen.get("PRB"):
                    badges.append('<span class="badge-ok">Rujuk Balik (*)</span>')

                badge_str = " ".join(badges)
                kelas_str = " > ".join([k["nama"] for k in item.get("kelas_path", [])])

                with st.expander(f"💊 {item['zat_aktif'].upper()} — {item['kelas_path'][-1]['nama'] if item.get('kelas_path') else ''}", expanded=False):
                    st.markdown(
                        f"""<div class="drug-card">
                        <div class="drug-card-title">{item['zat_aktif'].title()} {badge_str}</div>
                        <div class="drug-card-class"><b>Kelas Terapi:</b> {kelas_str} (Kode: {item.get('kelas_kode', '-')})</div>
                        <div class="drug-card-class"><b>Halaman PDF:</b> Hal. {item.get('halaman_pdf', '-')}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

                    # Tampilkan Referensi PNPK 2025 jika terkait
                    matched_pnpk = pe.get_pnpk_by_drug(item["zat_aktif"])
                    if matched_pnpk:
                        st.markdown("**📚 Pedoman Terkait (PNPK 2025):**")
                        for p in matched_pnpk:
                            st.markdown(
                                f'<div class="clinical-ok">🏛️ <b>{p["title"]}</b> ({p["kmk"]})<br>'
                                f'<small>Status: Regulasi Klinis Resmi Kemenkes RI · <a href="{p["source_url"]}" target="_blank" style="color: #38b6ff; text-decoration: underline;">Buka Sumber di Portal Kemenkes ↗</a></small></div>',
                                unsafe_allow_html=True,
                            )

                    # Tampilkan Restriksi Zat Aktif jika ada
                    if item.get("restriksi_zat_aktif"):
                        st.markdown("**📋 Restriksi Tingkat Zat Aktif:**")
                        for rza in item["restriksi_zat_aktif"]:
                            st.markdown(f'<div class="clinical-warning">⚠️ {rza["teks"]}</div>', unsafe_allow_html=True)

                    # Tampilkan Sediaan
                    st.markdown("**🧪 Bentuk Sediaan & Tingkat Fasilitas:**")
                    for sed in item.get("sediaan", []):
                        f_badges = []
                        if sed.get("fpktp"):
                            f_badges.append("🟢 FPKTP")
                        if sed.get("pp"):
                            f_badges.append("🏢 Puskesmas Perawatan (PP)")
                        if sed.get("fpktl"):
                            f_badges.append("🔴 FPKTL (Rumah Sakit)")
                        if sed.get("prb"):
                            f_badges.append("⭐ PRB")
                        if sed.get("oen"):
                            f_badges.append("✅ Obat Esensial (OEN)")

                        col_s1, col_s2 = st.columns([3, 2])
                        with col_s1:
                            st.markdown(f"**{sed['no']}. {sed['sediaan']}**")
                            st.caption(f"Fasilitas: {' · '.join(f_badges) if f_badges else 'Sesuai ketentuan'}")
                        with col_s2:
                            max_presc = sed.get("peresepan_maksimal", "-")
                            st.markdown(f"**Peresepan Maks:** `{max_presc if max_presc else 'Tidak dibatasi'}`")

                        # Restriksi sediaan spesifik
                        if sed.get("restriksi_sediaan"):
                            for rs in sed["restriksi_sediaan"]:
                                st.markdown(f'<div class="clinical-danger">📌 <em>{rs["teks"]}</em></div>', unsafe_allow_html=True)
                        st.markdown("<hr style='margin: 4px 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2: EVALUASI RESEP PASIEN (LOGIKA TIGA NILAI)
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Evaluasi Kesesuaian Resep Terhadap Fornas 2025</div>', unsafe_allow_html=True)
    st.markdown(
        "Menilai kesesuaian resep dengan prinsip **Logika Tiga Nilai** (TERPENUHI | TIDAK_TERPENUHI | TIDAK_DIKETAHUI). "
        "Data kosong tidak serta-merta ditolak (`DATA_KURANG`), dan bila ada restriksi yang dilanggar, Guppy menyarankan "
        "kategori justifikasi terstruktur sesuai acuan KFT/BPJS."
    )

    col_e1, col_e2 = st.columns([1, 1])

    with col_e1:
        st.markdown("#### 📝 Input Data Resep Pasien")
        ev_drug = st.text_input("Zat Aktif Obat:", value="metformin", placeholder="e.g. metformin, atorvastatin, fentanil")
        ev_sed = st.text_input("Bentuk Sediaan & Kekuatan (opsional):", value="tab 850 mg", placeholder="e.g. tab 850 mg, patch 25 mcg/jam")
        ev_fac = st.selectbox("Tingkat Fasilitas Pelayanan:", ["FPKTP", "FPKTL", "Belum Ditentukan"])
        fac_val = None if ev_fac == "Belum Ditentukan" else ev_fac

        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            q_num = st.number_input("Jumlah:", min_value=0, value=60, step=1)
        with col_q2:
            q_unit = st.selectbox("Satuan:", ["tab", "kaps", "amp", "btl", "patch", "vial"])
        with col_q3:
            q_per = st.selectbox("Periode:", ["bulan", "hari", "kasus", "minggu"])

        q_dict = {"jumlah": q_num, "satuan": q_unit, "per": q_per} if q_num > 0 else None

        ev_icd = st.text_input("Diagnosis Pasien (Kode ICD-10):", value="E11", placeholder="e.g. E11, I10, I25")
        patient_dict = {"diagnosis_icd10": [InputSanitizer.clean_text(ev_icd).upper()]} if ev_icd else {}

        eval_btn = st.button("⚖️ Jalankan Evaluasi Resep", type="primary", use_container_width=True)

    with col_e2:
        st.markdown("#### 📊 Hasil Penilaian Resep")
        if eval_btn:
            safe_drug = InputSanitizer.clean_text(ev_drug)
            safe_sed = InputSanitizer.clean_text(ev_sed) if ev_sed else None

            res = fm.evaluate(
                drug=safe_drug,
                sediaan=safe_sed,
                facility=fac_val,
                patient=patient_dict,
                quantity=q_dict,
            )

            status = res.get("status")
            if status == "SESUAI":
                st.markdown(f'<div class="verdict-ok">✅ STATUS: {status} — Resep Memenuhi Ketentuan Fornas 2025</div>', unsafe_allow_html=True)
            elif status == "DATA_KURANG":
                st.markdown(f'<div class="verdict-warn">⚠️ STATUS: {status} — Data Pasien / Sediaan Perlu Dilengkapi</div>', unsafe_allow_html=True)
            elif status == "PERLU_JUSTIFIKASI":
                st.markdown(f'<div class="verdict-fail">⛔ STATUS: {status} — Diperlukan Justifikasi Klinis / Administratif</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="verdict-warn">🔍 STATUS: {status}</div>', unsafe_allow_html=True)

            st.caption(f"📌 {res.get('fornas', 'Fornas 2025')}")

            # Kriteria Evaluasi
            for ev in res.get("evaluasi", []):
                st.markdown("**Rincian Kriteria Penilaian:**")
                for k in ev.get("kriteria", []):
                    badge = "✅" if k["hasil"] == "TERPENUHI" else ("❌" if k["hasil"] == "TIDAK_TERPENUHI" else "❓")
                    st.markdown(f"- {badge} **[{k['id']}] {k['jenis'].title()}:** `{k['hasil']}` — {k['alasan']}")
                    if k.get("restriksi"):
                        with st.expander("Lihat Teks Restriksi Asli Fornas"):
                            for r in k["restriksi"]:
                                st.write(f"- *({r.get('tingkat', '-')})*: {r.get('teks', '')}")

                if ev.get("justifikasi"):
                    st.markdown("**💡 Kode Justifikasi yang Disarankan:**")
                    for j in ev["justifikasi"]:
                        st.markdown(f"- `[{j}]` Sesuai pedoman katalog justifikasi KFT")

                if ev.get("data_diminta"):
                    st.markdown("**📋 Data Tambahan yang Perlu Dilengkapi:**")
                    for d in ev["data_diminta"]:
                        st.markdown(f'<div class="clinical-warning">Minta: {d}</div>', unsafe_allow_html=True)

                if ev.get("peringatan"):
                    for w in ev["peringatan"]:
                        st.markdown(f'<div class="clinical-danger">⚠️ {w}</div>', unsafe_allow_html=True)

                # Referensi PNPK Terkait untuk Evaluasi Resep
                eval_pnpk = pe.get_pnpk_by_drug(safe_drug)
                if eval_pnpk:
                    st.markdown("**🏛️ Dukungan Regulasi Klinis Nasional (PNPK 2025):**")
                    for p in eval_pnpk:
                        recs = p.get("clinical_recommendations", {})
                        recs_txt = []
                        for fl in recs.get("first_line", []):
                            if safe_drug.lower() in fl.get("zat_aktif", "").lower():
                                recs_txt.append(f"<b>Lini Pertama:</b> {fl.get('keterangan', '-')}")
                        for sl in recs.get("second_line_or_escalation", []):
                            if safe_drug.lower() in sl.get("zat_aktif", "").lower():
                                recs_txt.append(f"<b>Lini Kedua / Eskalasi:</b> {sl.get('keterangan', '-')}")
                        
                        detail_rec = "<br>".join(recs_txt) if recs_txt else p.get("summary", "")
                        st.markdown(
                            f'<div class="clinical-ok">📌 <b>{p["title"]}</b> ({p["kmk"]})<br>'
                            f'{detail_rec}<br>'
                            f'<small><a href="{p["source_url"]}" target="_blank" style="color: #38b6ff; text-decoration: underline;">Tinjau Dokumen Resmi di Portal Kemenkes ↗</a></small></div>',
                            unsafe_allow_html=True,
                        )

            # Notifikasi
            notifs = res.get("notifikasi", [])
            if notifs:
                st.markdown("**🔔 Notifikasi Otomatis yang Dihasilkan:**")
                for n in notifs:
                    lvl_color = "clinical-danger" if n["tingkat"] == "KRITIS" else "clinical-warning"
                    st.markdown(
                        f"""<div class="{lvl_color}">
                        <b>[{n['tingkat']}] Kepada: {n['penerima']}</b><br>
                        <b>{n['judul']}</b>: {n['isi']}
                        </div>""",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Isi formulir resep di sebelah kiri lalu klik tombol 'Jalankan Evaluasi Resep'.")


# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
# TAB 3: MATCHING DIAGNOSIS (ICD-10)
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Pencocokan Diagnosis Pasien (ICD-10) ke Terapi Fornas & PNPK 2025</div>', unsafe_allow_html=True)
    
    # 💡 Keterangan Edukatif Fungsi Fitur (Sesuai Permintaan)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(56, 182, 255, 0.12), rgba(15, 25, 35, 0.6)); border: 1px solid rgba(56, 182, 255, 0.35); border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="font-size: 1.5rem;">💡</span>
            <b style="color: #e2f4ff; font-size: 1.05rem;">Fungsi & Manfaat Mengetahui Hasil Matching Diagnosis:</b>
        </div>
        <ul style="color: #94d8ff; margin: 0; padding-left: 20px; font-size: 0.92rem; line-height: 1.6;">
            <li><b>Validasi Rasionalitas Terapi (Evidence-Based):</b> Memastikan obat yang diresepkan dokter selaras dengan indikasi resmi yang diakui dalam Fornas 2025 dan baku emas klinis <b>PNPK Kemenkes 2025</b>.</li>
            <li><b>Mencegah Dispute / Penolakan Klaim BPJS Kesehatan:</b> BPJS mencocokkan kode diagnosis ICD-10 dengan restriksi obat. Mengetahui pasangan diagnosis-obat yang tepat mencegah klaim berstatus <i>pending</i> atau tidak dibayar.</li>
            <li><b>Panduan Pemilihan Lini Terapi (First-Line vs Escalation):</b> Mengetahui urutan terapi yang sah secara hukum dan etika medis sehingga pasien mendapatkan obat yang paling efektif sebelum naik ke terapi lini kedua.</li>
            <li><b>Penyusunan Form Justifikasi Otomatis:</b> Jika pasien membutuhkan obat di luar daftar standar, data matching ini menjadi dasar kuat apoteker menyusun memo persetujuan ke Direktur RS / Komite Farmasi & Terapi (KFT).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    icd_col1, icd_col2 = st.columns([1, 2])
    with icd_col1:
        st.markdown("#### 🎯 Pilih / Input Kode Diagnosis")
        st.caption("Pilih dari kategori klinis yang tersedia atau ketik kode ICD-10 secara bebas.")

        icd_sel = st.selectbox("Kategori Diagnosis Klinis:", list(COMMON_ICD10.keys()), index=0)
        selected_code = COMMON_ICD10[icd_sel]

        custom_icd = st.text_input("Atau Cari Kode ICD-10 / Nama Penyakit:", value="", placeholder="e.g. J18, N39, E11, M17, Asma...")
        target_code = custom_icd.strip().upper() if custom_icd.strip() else selected_code

        st.info(f"Target Diagnosis Terpilih: **{target_code}**")

        # Tampilkan apakah ada pedoman PNPK untuk kode ini
        pnpk_for_icd = pe.get_pnpk_by_icd10(target_code)
        if pnpk_for_icd:
            st.markdown(
                f"""<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 12px; margin-top: 10px;">
                <b style="color: #34d399;">🏛️ Memiliki Acuan Resmi PNPK 2025</b><br>
                <small style="color: #a7f3d0;">Tersedia <b>{len(pnpk_for_icd)}</b> Pedoman Nasional Pelayanan Kedokteran Kemenkes RI terkait diagnosis ini.</small>
                </div>""",
                unsafe_allow_html=True,
            )

    with icd_col2:
        st.markdown("#### 📋 Hasil Telaah Diagnosis & Pilihan Terapi")

        # 1. BAGIAN PNPK 2025 (JIKA TERSEDIA)
        if pnpk_for_icd:
            st.markdown("##### 🏛️ Rekomendasi Terapi Resmi (PNPK 2025 Kemenkes RI)")
            for p in pnpk_for_icd:
                with st.expander(f"🩺 {p['title']} ({p['kmk']})", expanded=True):
                    st.caption(f"Status: Standar Baku Emas Kemenkes RI · <a href='{p['source_url']}' target='_blank' style='color: #38b6ff;'>Buka Dokumen di Portal Kemenkes ↗</a>", unsafe_allow_html=True)
                    st.markdown(f'<div class="clinical-ok">{p.get("summary", "")}</div>', unsafe_allow_html=True)

                    recs = p.get("clinical_recommendations", {})
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown("**🟢 Rekomendasi Lini Pertama (First-Line):**")
                        for fl in recs.get("first_line", []):
                            st.markdown(f"- **{fl['zat_aktif']}** ({fl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em>{fl.get('keterangan', '-')}</em>", unsafe_allow_html=True)
                    with col_r2:
                        st.markdown("**🟡 Lini Kedua / Eskalasi / Alternatif:**")
                        for sl in recs.get("second_line_or_escalation", []):
                            st.markdown(f"- **{sl['zat_aktif']}** ({sl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em>{sl.get('keterangan', '-')}</em>", unsafe_allow_html=True)

                    if recs.get("safety_and_restrictions"):
                        st.markdown("**⚠️ Batasan & Keamanan Klinis:**")
                        for sr in recs["safety_and_restrictions"]:
                            st.markdown(f"- <em>{sr}</em>", unsafe_allow_html=True)

        # 2. PENCARIAN OBAT TERINTEGRASI DALAM FORNAS 2025
        all_drugs = fm.get_db()["obat"]
        matched_drugs = []
        target_clean = target_code.split(".")[0]

        # Ambil daftar obat yang terlibat dari PNPK
        pnpk_drug_names = set()
        for p in pnpk_for_icd:
            for d_name in p.get("drugs_involved", []):
                pnpk_drug_names.add(d_name.strip().lower())

        for d in all_drugs:
            is_hit = False
            # Cek kecocokan kode ICD-10 usulan
            for u in d.get("icd10_usulan", []):
                u_code = u["kode"].split("-")[0].split(".")[0]
                if target_clean in u_code or u_code in target_clean:
                    is_hit = True
                    break
            # Cek kecocokan dengan obat rekomendasi PNPK
            if not is_hit and any(d["zat_aktif"].strip().lower() == pd or pd in d["zat_aktif"].strip().lower() for pd in pnpk_drug_names):
                is_hit = True

            if is_hit:
                matched_drugs.append(d)

        # Tampilkan Obat Terkait dengan Expander Interaktif
        st.markdown("##### 💊 Obat Fornas 2025 yang Diakui untuk Diagnosis Ini")
        if matched_drugs:
            st.success(f"Ditemukan **{len(matched_drugs)}** obat dalam Fornas 2025 untuk diagnosis `{target_code}`. Klik obat untuk membuka detail sediaan & restriksi:")
            for md in matched_drugs:
                pen = md.get("penanda", {})
                badges = []
                if pen.get("P"):
                    badges.append("🏷️ Program [P]")
                if pen.get("Ca"):
                    badges.append("🎗️ Kanker [Ca]")
                if pen.get("PRB"):
                    badges.append("⭐ Rujuk Balik (*)")
                badge_text = f" ({', '.join(badges)})" if badges else ""

                kelas_nama = md["kelas_path"][-1]["nama"] if md.get("kelas_path") else "-"

                with st.expander(f"💊 {md['zat_aktif'].title()}{badge_text} — {kelas_nama}", expanded=False):
                    st.markdown(f"**Kelas Terapi:** `{' > '.join([k['nama'] for k in md.get('kelas_path', [])])}`")
                    st.markdown(f"**Halaman PDF Fornas 2025:** Hal. {md.get('halaman_pdf', '-')}")

                    if md.get("restriksi_zat_aktif"):
                        st.markdown("**📋 Restriksi Tingkat Zat Aktif:**")
                        for rza in md["restriksi_zat_aktif"]:
                            st.markdown(f'<div class="clinical-warning">⚠️ {rza["teks"]}</div>', unsafe_allow_html=True)

                    st.markdown("**🧪 Bentuk Sediaan & Tingkat Fasilitas:**")
                    for sed in md.get("sediaan", []):
                        f_badges = []
                        if sed.get("fpktp"):
                            f_badges.append("🟢 FPKTP (Primer)")
                        if sed.get("pp"):
                            f_badges.append("🏢 Puskesmas Perawatan")
                        if sed.get("fpktl"):
                            f_badges.append("🔴 FPKTL (Rumah Sakit)")
                        if sed.get("prb"):
                            f_badges.append("⭐ PRB")
                        if sed.get("oen"):
                            f_badges.append("✅ OEN")

                        st.markdown(f"- **{sed['no']}. {sed['sediaan']}**")
                        st.caption(f"Fasilitas: {' · '.join(f_badges) if f_badges else 'Sesuai ketentuan'} | Peresepan Maksimal: {sed.get('peresepan_maksimal') or 'Tidak dibatasi'}")

                        if sed.get("restriksi_sediaan"):
                            for rs in sed["restriksi_sediaan"]:
                                st.markdown(f'<div class="clinical-danger">📌 <em>{rs["teks"]}</em></div>', unsafe_allow_html=True)
        else:
            st.warning(f"Belum ada pemetaan eksplisit untuk kode `{target_code}` dalam database. Anda dapat menelusuri nama obat secara manual pada Tab 1.")


# ═══════════════════════════════════════════════════════════════
# TAB 4: JUSTIFIKASI LITERATUR KLINIS (Q1-Q3)
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Justifikasi Literatur Klinis Berbasis Bukti (Q1-Q3) & Memo KFT</div>', unsafe_allow_html=True)
    
    # 💡 Penjelasan Fitur Kurasi Rutin & Interaktif
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(56, 182, 255, 0.12), rgba(15, 25, 35, 0.6)); border: 1px solid rgba(56, 182, 255, 0.35); border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <span style="font-size: 1.5rem;">💡</span>
            <b style="color: #e2f4ff; font-size: 1.05rem;">Kurasi Rutin Guppy (Update Berkala) & Seleksi Fleksibel Pengguna:</b>
        </div>
        <p style="color: #94d8ff; margin: 0; font-size: 0.92rem; line-height: 1.6;">
            Guppy memilihkan artikel bereputasi internasional (<b>Scopus Q1–Q3</b>, PubMed, Lancet, NEJM, JAMA, dan konsensus global) untuk setiap kasus peresepan yang memerlukan adaptasi restriksi Fornas 2025. 
            Anda dapat meninjau rekomendasi utama Guppy serta studi pendukung lainnya, lalu <b>mencentang satu atau beberapa artikel terbaik</b> sesuai kondisi pasien untuk menghasilkan <b>Memo Justifikasi KFT</b> yang sah dan audit-ready.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. PENCARIAN & PEMILIHAN TOPIK KLINIS
    col_lit_s1, col_lit_s2 = st.columns([1.2, 0.8])
    with col_lit_s1:
        lit_search_query = st.text_input(
            "🔍 Saring Kasus / Nama Obat / Topik Klinis:",
            value="",
            placeholder="e.g. Metformin, Statin, Lansia, Ginjal, PPI, Antibiotik, Insulin, Hipertensi...",
        )
    with col_lit_s2:
        st.caption(f"🛡️ Versi Repositori: `{ClinicalLiteratureScout.CURATION_VERSION}`. Sumber terverifikasi bebas artikel predator.")

    filtered_topics = ClinicalLiteratureScout.search_curated_topics(lit_search_query)

    if not filtered_topics:
        st.warning("Tidak ditemukan topik klinis yang cocok dengan kata kunci pencarian. Menampilkan seluruh repositori.")
        filtered_topics = ClinicalLiteratureScout.get_all_topics()

    topic_options = {
        f"[{t['category']}] {t['title']} (Obat: {t['drug_inn']} · {len(t['articles'])} telaah Q1-Q3)": t["topic_id"]
        for t in filtered_topics
    }

    selected_topic_label = st.selectbox(
        "📌 Pilih Kasus Klinis yang Membutuhkan Justifikasi:",
        options=list(topic_options.keys()),
        index=0,
    )

    selected_topic_id = topic_options[selected_topic_label]
    curr_topic = ClinicalLiteratureScout.get_topic_by_id(selected_topic_id)

    if curr_topic:
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.65); border-left: 4px solid #38b6ff; border-radius: 8px; padding: 14px 18px; margin: 15px 0 20px 0;">
            <div style="color: #e2f4ff; font-weight: 600; font-size: 1.05rem; margin-bottom: 4px;">💊 Kasus: {curr_topic['title']}</div>
            <div style="color: #cbd5e1; font-size: 0.92rem; margin-bottom: 6px;"><b>Masalah Pasien:</b> {curr_topic['clinical_problem']}</div>
            <div style="color: #fbbf24; font-size: 0.9rem;"><b>⚠️ Restriksi Baku Fornas:</b> {curr_topic['fornas_rule']}</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. SELEKSI ARTIKEL OLEH PENGGUNA DARI PILIHAN GUPPY
        st.markdown("#### 📚 Artikel Kurasi Guppy — Silakan Pilih Artikel untuk Memo Justifikasi:")
        st.caption(
            "Artikel bertanda ⭐ adalah Rekomendasi Utama Guppy yang langsung dicentang secara default. "
            "Anda dapat mencentang artikel studi pembanding / pedoman konsensus bertanda 📑 untuk memperkuat dasar telaah."
        )

        user_selected_articles = []
        for idx, art in enumerate(curr_topic["articles"], 1):
            c = art["citation"]
            is_pri = art.get("is_primary", False)
            badge_icon = "⭐ [REKOMENDASI UTAMA GUPPY]" if is_pri else "📑 [STUDI PENDUKUNG / KONSENSUS]"
            
            # Checkbox pemilihan artikel oleh pengguna
            cb_key = f"chk_art_{curr_topic['topic_id']}_{art['article_id']}"
            is_checked = st.checkbox(
                f"{badge_icon} {c['authors']} ({c['year']}) — \"{c['title']}\" [{c['quartile']}]",
                value=is_pri,
                key=cb_key,
            )
            if is_checked:
                user_selected_articles.append(art)

            # Detail konten artikel dalam expander
            with st.expander(f"🔎 Detail Telaah #{idx}: {c['journal']} ({c['year']}) · {c['quartile']}", expanded=is_pri):
                st.markdown(f"**Judul Makalah:** *\"{c['title']}\"*")
                st.markdown(f"**Penulis:** {c['authors']} ({c['year']})")
                st.markdown(f"**Jurnal & Reputasi:** `{c['journal']}`, {c['volume_issue']} · **`{c['quartile']}`**")
                st.markdown(f"**Desain / Jenis Studi:** `{c.get('study_type', 'Clinical Trial / Guideline')}`")
                st.markdown(f"**Identifikasi Referensi:** DOI: `{c.get('doi', '-')}` | PMID: `{c.get('pmid', '-')}`")
                st.markdown("---")
                st.markdown("**🔬 Temuan Klinis Kunci:**")
                st.markdown(f'<div class="clinical-ok">{art["clinical_finding"]}</div>', unsafe_allow_html=True)
                st.markdown("**🩺 Implikasi Terhadap Justifikasi Fornas & KFT:**")
                st.markdown(f'<div class="clinical-warning">{art["fornas_implication"]}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # 3. PERSONALISASI DATA PASIEN & GENERATOR MEMO KFT
        st.markdown("#### 📝 Personalisasi & Unduh Memo Justifikasi KFT")
        
        with st.expander("✏️ Klik untuk Mengisi Identitas Pasien & Catatan Khusus Apoteker (Opsional)", expanded=False):
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                memo_pt_name = st.text_input("Nama Pasien & Usia:", value="", placeholder="e.g. Ny. Siti Rahma (68 th)", key=f"pt_n_{curr_topic['topic_id']}")
                memo_no_rm = st.text_input("No. Rekam Medis (RM):", value="", placeholder="e.g. RM-2026-44910", key=f"pt_rm_{curr_topic['topic_id']}")
                memo_diag = st.text_input("Diagnosis Klinis / ICD-10:", value=f"Terkait {curr_topic['drug_inn']}", placeholder="e.g. E11 DMT2 + N18 CKD Stage 3", key=f"pt_dx_{curr_topic['topic_id']}")
            with p_col2:
                memo_dpjp = st.text_input("DPJP (Dokter Penulis Resep):", value="", placeholder="e.g. dr. Hendra, Sp.PD-KEMD", key=f"pt_dr_{curr_topic['topic_id']}")
                memo_ruang = st.text_input("Ruang Rawat / Poliklinik:", value="", placeholder="e.g. Rawat Inap Melati 3B / Poli Penyakit Dalam", key=f"pt_rg_{curr_topic['topic_id']}")
                memo_apt = st.text_input("Nama Apoteker Pengkaji:", value="Apt. Tim Farmasi Klinis, S.Farm.", key=f"pt_apt_{curr_topic['topic_id']}")
                memo_sipa = st.text_input("Nomor SIPA:", value="SIPA.XXXXXXXXXXXX", key=f"pt_sipa_{curr_topic['topic_id']}")

            memo_notes = st.text_area(
                "Catatan Khusus Rekomendasi Apoteker (Rencana Dosis, Monitoring Lab, atau Evaluasi Efek Samping):",
                value="",
                placeholder="e.g. Dosis metformin disesuaikan menjadi 500 mg 2x sehari (1000 mg/hari). Pemantauan kadar serum kreatinin dan eGFR dijadwalkan ulang dalam 3 bulan.",
                key=f"pt_notes_{curr_topic['topic_id']}",
            )

        # Ringkasan Status Seleksi
        if user_selected_articles:
            st.success(f"✅ Sebanyak **{len(user_selected_articles)} artikel bukti ilmiah** dipilih untuk dimasukkan ke dalam draft Memo Justifikasi.")
        else:
            st.warning("⚠️ Tidak ada artikel yang dicentang. Silakan centang minimal 1 artikel di atas agar memo memiliki dasar bukti ilmiah yang kokoh.")

        patient_dict = {
            "nama_pasien": memo_pt_name or "[Nama Pasien]",
            "no_rm": memo_no_rm or "[No. Rekam Medis]",
            "diagnosis": memo_diag or f"Terkait terapi {curr_topic['drug_inn']}",
            "dpjp": memo_dpjp or "[Dokter Penanggung Jawab Pelayanan]",
            "ruangan": memo_ruang or "[Poliklinik / Rawat Inap]",
        }

        generated_memo_md = ClinicalLiteratureScout.generate_justification_memo(
            topic=curr_topic,
            selected_articles=user_selected_articles,
            patient_info=patient_dict,
            pharmacist_notes=memo_notes if 'memo_notes' in locals() else "",
            pharmacist_name=memo_apt if 'memo_apt' in locals() and memo_apt else "Apoteker Farmasi Klinis",
            sipa_number=memo_sipa if 'memo_sipa' in locals() and memo_sipa else "SIPA.XXXXXXXXXXXX",
        )

        with st.expander("👁️ Pratinjau Dokumen Memo Justifikasi KFT (Siap Cetak / Diserahkan)", expanded=False):
            st.markdown(generated_memo_md)

        clean_fn_drug = curr_topic['drug_inn'].replace('/', '_').replace(' ', '_').lower()
        st.download_button(
            label=f"⬇️ Unduh Dokumen Memo Justifikasi KFT ({curr_topic['drug_inn']})",
            data=generated_memo_md,
            file_name=f"memo_justifikasi_{clean_fn_drug}_{curr_topic['topic_id']}.md",
            mime="text/markdown",
            key=f"dl_memo_{curr_topic['topic_id']}",
        )


# ═══════════════════════════════════════════════════════════════
# TAB 5: BASIS HUKUM REGULASI FARMASI KLINIS
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Basis Hukum Regulasi & Pedoman Nasional Pelayanan Kedokteran (PNPK)</div>', unsafe_allow_html=True)
    st.markdown(
        "Akses teks hierarki perundang-undangan farmasi klinis Indonesia (**UU 17/2023**, **KMK Fornas 1199/2025**) "
        "serta integrasi **Pedoman Nasional Pelayanan Kedokteran (PNPK 2025)** resmi Kementerian Kesehatan RI."
    )

    reg_subtab1, reg_subtab2 = st.tabs([
        "🏛️ Pedoman Nasional Pelayanan Kedokteran (PNPK 2025)",
        "📜 Regulasi Pokok & Fornas 2025 (UU & Kepmenkes)",
    ])

    with reg_subtab1:
        st.markdown("#### 📚 Kompilasi PNPK Kemenkes RI 2025")
        st.caption(
            "Ringkasan klinis esensial (First-Line & Second-Line) dari Keputusan Menteri Kesehatan RI tahun 2025. "
            "Seluruh hak cipta dokumen dimiliki oleh Kementerian Kesehatan RI. Akses dokumen lengkap melalui portal resmi Kemenkes."
        )

        pnpk_list = pe.get_pnpk_db()
        pnpk_filter = st.text_input("Saring PNPK (Penyakit / Obat / KMK):", value="", placeholder="e.g. Pneumonia, ISK, Osteoartritis, Seftriakson...")
        clean_pf = pnpk_filter.strip().lower()

        filtered_pnpk = []
        for p in pnpk_list:
            if not clean_pf or (
                clean_pf in p["title"].lower()
                or clean_pf in p["kmk"].lower()
                or clean_pf in p.get("summary", "").lower()
                or any(clean_pf in d.lower() for d in p.get("drugs_involved", []))
            ):
                filtered_pnpk.append(p)

        st.write(f"Menampilkan **{len(filtered_pnpk)}** dari **{len(pnpk_list)}** dokumen PNPK 2025:")
        for p in filtered_pnpk:
            with st.expander(f"🩺 {p['title']} — {p['kmk']}", expanded=False):
                st.markdown(f"**Nomor Kepmenkes:** `{p['kmk']}`")
                st.markdown(f"**Status & Tahun:** Ditetapkan Tahun {p['year']} oleh Menteri Kesehatan RI")
                st.markdown(f'<div class="clinical-ok">{p["summary"]}</div>', unsafe_allow_html=True)

                recs = p.get("clinical_recommendations", {})
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown("**🟢 Rekomendasi Terapi Lini Pertama:**")
                    for fl in recs.get("first_line", []):
                        st.markdown(f"- **{fl['zat_aktif']}** ({fl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em>{fl.get('keterangan', '-')}</em>", unsafe_allow_html=True)
                with col_p2:
                    st.markdown("**🟡 Lini Kedua / Eskalasi:**")
                    for sl in recs.get("second_line_or_escalation", []):
                        st.markdown(f"- **{sl['zat_aktif']}** ({sl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em>{sl.get('keterangan', '-')}</em>", unsafe_allow_html=True)

                if recs.get("safety_and_restrictions"):
                    st.markdown("**⚠️ Batasan Peresepan & Keselamatan Pasien:**")
                    for sr in recs["safety_and_restrictions"]:
                        st.markdown(f"- <em>{sr}</em>", unsafe_allow_html=True)

                st.markdown("---")
                st.markdown(
                    f"🔗 **Tautan Resmi Kemenkes:** "
                    f"<a href='{p['source_url']}' target='_blank' style='display: inline-block; padding: 6px 14px; background: rgba(56, 182, 255, 0.15); border: 1px solid rgba(56, 182, 255, 0.4); border-radius: 8px; color: #38b6ff; text-decoration: none; font-weight: 500;'>"
                    f"Buka Dokumen Resmi di Portal Kemenkes RI ↗</a>",
                    unsafe_allow_html=True,
                )

    with reg_subtab2:
        reg_q = st.text_input("Cari Pasal / Diktum / Kata Kunci:", value="1199/2025", placeholder="e.g. 1199/2025, obat luar fornas, izin edar")
        clean_reg_q = InputSanitizer.clean_text(reg_q).lower() if reg_q else ""

        try:
            with open(REGULATIONS_DB_PATH, "r", encoding="utf-8") as f:
                reg_db = json.load(f)

            matched_articles = []
            for reg in reg_db.get("regulations", []):
                for art in reg.get("articles", []):
                    match = (
                        not clean_reg_q
                        or clean_reg_q in reg["title"].lower()
                        or clean_reg_q in reg["number"].lower()
                        or clean_reg_q in art["article"].lower()
                        or any(clean_reg_q in p.lower() for p in art.get("paragraphs", []))
                        or any(clean_reg_q in kw.lower() for kw in art.get("keywords", []))
                    )
                    if match:
                        matched_articles.append((reg, art))

            st.write(f"Ditemukan **{len(matched_articles)}** ketentuan regulasi:")
            for reg, art in matched_articles:
                with st.expander(f"📜 {reg['number']} — {art['article']}", expanded=False):
                    st.markdown(f"**{reg['title']}** *(Status: {reg.get('status', '-')})*")
                    st.caption(f"Hierarki: {reg.get('hierarchy', '-')} | Bab: {art.get('chapter', '-')}")
                    for p in art.get("paragraphs", []):
                        st.markdown(f'<div class="clinical-ok">📖 {p}</div>', unsafe_allow_html=True)
                    if art.get("keywords"):
                        st.caption("Kata Kunci: " + " · ".join(art["keywords"]))
        except Exception as e:
            st.error(f"Gagal memuat database regulasi: {e}")
