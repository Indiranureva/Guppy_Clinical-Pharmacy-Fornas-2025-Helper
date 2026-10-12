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
from guppy.backend.engine.clinical_literature import ClinicalLiteratureScout
from guppy.backend.security.sanitizer import InputSanitizer
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
# TAB 3: MATCHING DIAGNOSIS (ICD-10)
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Pencocokan Diagnosis Pasien (ICD-10) ke Terapi Fornas</div>', unsafe_allow_html=True)
    st.markdown(
        "Membantu apoteker dan klinisi mencocokkan kode diagnosis penyakit (ICD-10) dengan opsi obat "
        "yang diatur penggunaannya dalam Fornas 2025."
    )

    icd_col1, icd_col2 = st.columns([1, 1])
    with icd_col1:
        st.markdown("#### 🎯 Pilih / Input Kode Diagnosis")
        icd_sel = st.selectbox("Diagnosis Umum:", list(COMMON_ICD10.keys()))
        selected_code = COMMON_ICD10[icd_sel]

        custom_icd = st.text_input("Atau ketik kode/istilah ICD-10 lain:", value="", placeholder="e.g. E11, I10, J45, N04")
        target_code = custom_icd.strip().upper() if custom_icd.strip() else selected_code

        st.info(f"Target Diagnosis Terpilih: **{target_code}**")

    with icd_col2:
        st.markdown("#### 📋 Daftar Obat Terkait")
        all_drugs = fm.get_db()["obat"]
        matched_drugs = []
        target_clean = target_code.split(".")[0]

        for d in all_drugs:
            for u in d.get("icd10_usulan", []):
                u_code = u["kode"].split("-")[0].split(".")[0]
                if target_clean in u_code or u_code in target_clean:
                    matched_drugs.append(d)
                    break

        if matched_drugs:
            st.success(f"Ditemukan **{len(matched_drugs)}** obat dalam Fornas 2025 terkait diagnosis `{target_code}`:")
            for md in matched_drugs[:8]:
                st.markdown(f"- 💊 **{md['zat_aktif'].title()}** ({md['kelas_path'][-1]['nama'] if md.get('kelas_path') else '-'})")
                if md.get("restriksi_zat_aktif"):
                    st.caption(f"Restriksi: {md['restriksi_zat_aktif'][0]['teks'][:100]}...")
        else:
            st.warning(f"Belum ada pemetaan eksplisit untuk kode `{target_code}`. Anda dapat meninjau kelas terapi terkait secara langsung di Tab 1.")


# ═══════════════════════════════════════════════════════════════
# TAB 4: JUSTIFIKASI LITERATUR KLINIS (Q1-Q3)
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Justifikasi Literatur Klinis Berbasis Bukti (Q1-Q3)</div>', unsafe_allow_html=True)
    st.markdown(
        "Menyediakan bukti ilmiah dari jurnal terindeks Scopus (Q1–Q3) dan pedoman praktik klinis (PNPK) "
        "untuk menyusun **Memo Justifikasi Klinis** saat terapi pasien memerlukan adaptasi di luar restriksi baku."
    )

    col_lit1, col_lit2 = st.columns([1, 1])
    with col_lit1:
        lit_q = st.text_input("Cari Bukti Ilmiah (Nama Obat / Kasus):", value="", placeholder="e.g. Metformin, Statin, Lansia, Ginjal, PPI")
    with col_lit2:
        st.caption("Repositori bukti mencakup studi klinis keamanan metformin pada CKD, statin pada lansia, dan deprescribing PPI.")

    clean_lit_q = InputSanitizer.clean_text(lit_q) if lit_q else ""
    evidence_items = ClinicalLiteratureScout.search_clinical_evidence(
        drug_inn=clean_lit_q,
        clinical_question=clean_lit_q,
    )
    if not evidence_items and not clean_lit_q:
        evidence_items = ClinicalLiteratureScout.EVIDENCE_REPOSITORY

    st.write(f"Ditemukan **{len(evidence_items)}** telaah bukti ilmiah:")
    for item in evidence_items:
        c = item["citation"]
        with st.expander(f"📖 {item['drug_inn']} — {item['clinical_question']}", expanded=False):
            st.markdown(f"**Judul Studi:** *\"{c['title']}\"*")
            st.markdown(f"**Jurnal & Reputasi:** {c['journal']} ({c['year']}) · `{c['quartile']}` · DOI: {c.get('doi', '-')}")
            st.markdown("---")
            st.markdown("**🔬 Temuan Klinis Utama:**")
            st.markdown(f'<div class="clinical-ok">{item["clinical_finding"]}</div>', unsafe_allow_html=True)
            st.markdown("**🩺 Implikasi Terhadap Fornas & Justifikasi:**")
            st.markdown(f'<div class="clinical-warning">{item["fornas_implication"]}</div>', unsafe_allow_html=True)

            memo_md = ClinicalLiteratureScout.format_evidence_card(item)
            st.download_button(
                label=f"⬇️ Unduh Memo Justifikasi ({item['drug_inn']})",
                data=memo_md,
                file_name=f"memo_justifikasi_{item['drug_inn']}.md",
                mime="text/markdown",
                key=f"dl_memo_{item['topic_id']}",
            )


# ═══════════════════════════════════════════════════════════════
# TAB 5: BASIS HUKUM REGULASI FARMASI KLINIS
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Basis Hukum & Ketentuan Regulasi Farmasi Klinis Indonesia</div>', unsafe_allow_html=True)
    st.markdown(
        "Akses teks lengkap ketentuan perundang-undangan farmasi klinis Indonesia, termasuk **KMK No. HK.01.07/MENKES/1199/2025 (Fornas 2025)**, "
        "**UU No. 17 Tahun 2023 tentang Kesehatan**, dan pedoman peresepan obat esensial JKN."
    )

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
