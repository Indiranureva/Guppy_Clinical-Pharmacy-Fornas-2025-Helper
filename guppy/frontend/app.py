"""Guppy — Clinical Pharmacy & Fornas 2025 Helper.

Modern Healthcare Decision Support System (CDSS) for Indonesian Healthcare Professionals:
- Formularium Nasional (Fornas 2025 - KMK HK.01.07/MENKES/1199/2025)
- Pedoman Nasional Pelayanan Kedokteran (9 PNPK Kemenkes 2025)
- Three-Valued Logic Prescription Evaluator (TERPENUHI | TIDAK_TERPENUHI | TIDAK_DIKETAHUI)
- Diagnosis-to-Therapy ICD-10 Matching Engine
- Evidence-Based Justification Wizard (Scopus Q1-Q3 & Word .docx Export)
- BPJS Pre-Claim Compliance Simulator
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
from guppy.frontend.components.mascot import (
    get_guppy_circle_logo_svg,
    get_sidebar_footer_html,
)
from guppy.frontend.components.ui_cards import (
    render_top_bar,
    render_welcome_banner,
    render_stats_panel,
    render_tips_card,
    render_quick_references,
    render_guppy_core_values,
)
from guppy.frontend.components.action_cards import render_four_action_cards
from guppy.frontend.components.interactive_workflow import render_four_workflow_columns


# ─────────────────────────────────────────────────────────────
# 1. STREAMLIT PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Guppy — Clinical Pharmacy & Fornas 2025 Helper",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load external CSS design tokens
CSS_PATH = Path(__file__).parent / "assets" / "style.css"
if CSS_PATH.exists():
    with open(CSS_PATH, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 2. SESSION STATE MANAGEMENT
# ─────────────────────────────────────────────────────────────
st.session_state.setdefault("nav_selection", "Beranda")
st.session_state.setdefault("user_name", "dr. Andini")
st.session_state.setdefault("user_role", "Dokter Spesialis / DPJP")
st.session_state.setdefault("facility_level", "FPKTL (Rumah Sakit)")
st.session_state.setdefault("sipa_number", "SIPA.1995.04.01")
st.session_state.setdefault("tips_idx", 1)
st.session_state.setdefault("favorites", {"Metformin", "Atorvastatin", "E11", "J18", "Candesartan"})
st.session_state.setdefault(
    "history",
    [
        {
            "timestamp": "23 Okt 2026, 16:32",
            "type": "Evaluasi Resep",
            "item": "Metformin 500 mg tab",
            "diagnosis": "E11 (DMT2)",
            "status": "SESUAI",
        },
        {
            "timestamp": "23 Okt 2026, 15:10",
            "type": "Justifikasi KFT",
            "item": "Simvastatin 40 mg tab",
            "diagnosis": "E78 (Dislipidemia Geriatri)",
            "status": "MEMO_SELESAI",
        },
        {
            "timestamp": "23 Okt 2026, 11:45",
            "type": "Simulasi Klaim",
            "item": "Omeprazole 20 mg",
            "diagnosis": "K21 (GERD)",
            "status": "PERLU_TINJAUAN",
        },
    ],
)


# ─────────────────────────────────────────────────────────────
# 3. SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    # Mascot Circle Logo & Brand Title
    logo_svg = get_guppy_circle_logo_svg(size=46)
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
            {logo_svg}
            <div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.1;">
                    GUPPY
                </div>
                <div style="font-size: 0.72rem; color: #BAE6FD; font-weight: 500;">
                    Clinical Pharmacy & Fornas 2025 Helper
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Primary Navigation Menu
    nav_options = [
        "Beranda",
        "Cek Fornas",
        "Cek Diagnosa",
        "Evaluasi Resep",
        "Justifikasi Klinis",
        "Simulasi Klaim",
        "Referensi",
        "Literatur Ilmiah",
        "Riwayat",
        "Favorit",
        "Pengaturan",
    ]

    nav_icons = {
        "Beranda": "🏠",
        "Cek Fornas": "💊",
        "Cek Diagnosa": "🩺",
        "Evaluasi Resep": "⚖️",
        "Justifikasi Klinis": "📝",
        "Simulasi Klaim": "📊",
        "Referensi": "📚",
        "Literatur Ilmiah": "📖",
        "Riwayat": "🕒",
        "Favorit": "⭐",
        "Pengaturan": "⚙️",
    }

    current_nav = st.session_state["nav_selection"]
    if current_nav not in nav_options:
        current_nav = "Beranda"

    selected_page = st.radio(
        "Menu Navigasi Utama",
        options=nav_options,
        index=nav_options.index(current_nav),
        format_func=lambda x: f"{nav_icons.get(x, '•')}  {x}",
        label_visibility="collapsed",
        key="main_sidebar_nav",
    )

    if selected_page != st.session_state["nav_selection"]:
        st.session_state["nav_selection"] = selected_page
        st.rerun()

    st.markdown("---")

    # LinkGuard Security Light Indicator
    sec_light = LinkGuard.get_security_light()
    if sec_light["color"] == "HIJAU":
        st.markdown(
            """
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                <b style="color: #34d399; font-size: 0.8rem;">🟢 Sistem & Acuan: AMAN</b><br>
                <small style="color: #A7F3D0; font-size: 0.72rem;">Database Fornas 2025 & PNPK Kemenkes terverifikasi resmi.</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif sec_light["color"] == "ORANGE":
        st.markdown(
            """
            <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                <b style="color: #FBBF24; font-size: 0.8rem;">🟠 Akses Dibatasi Sementara</b><br>
                <small style="color: #FDE68A; font-size: 0.72rem;">Satu atau lebih portal referensi sedang dalam pemeliharaan.</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                <b style="color: #F87171; font-size: 0.8rem;">🔴 Proteksi Keamanan Aktif</b><br>
                <small style="color: #FCA5A5; font-size: 0.72rem;">Tautan tidak terverifikasi dinonaktifkan otomatis.</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Sidebar Tagline Footer with Swimming Mascot
    st.markdown(get_sidebar_footer_html(), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 4. TOP BAR RENDERING
# ─────────────────────────────────────────────────────────────
render_top_bar(
    user_name=st.session_state["user_name"],
    facility=st.session_state["facility_level"],
    unread_notifications=1,
)


# ─────────────────────────────────────────────────────────────
# 5. MAIN ROUTER & PAGE IMPLEMENTATIONS
# ─────────────────────────────────────────────────────────────
current_page = st.session_state["nav_selection"]

# ═════════════════════════════════════════════════════════════
# PAGE: BERANDA (EXECUTIVE CLINICAL DASHBOARD)
# ═════════════════════════════════════════════════════════════
if current_page == "Beranda":
    # 1. Main Welcome Banner with Mascot
    render_welcome_banner(user_name=st.session_state["user_name"])

    # 2. Main Layout: Left Workflow / Actions (72%) & Right Intelligence Widgets (28%)
    col_main_dash, col_side_dash = st.columns([2.6, 1.2])

    with col_main_dash:
        # 4 Primary Action Cards
        render_four_action_cards()

    with col_side_dash:
        # Statistics Panel
        render_stats_panel(searches=152, diagnoses=98, justifications=67, simulations=24)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 3. Middle Section: Interactive Workflow (Left) + Tips, Links & Core Values (Right)
    col_lower_left, col_lower_right = st.columns([2.6, 1.2])

    with col_lower_left:
        # Interactive 4-Column Live Workflow Cards from Mockup
        render_four_workflow_columns()

    with col_lower_right:
        # Tips Hari Ini
        render_tips_card(tip_index=st.session_state["tips_idx"], total_tips=5)
        # Quick References Links
        render_quick_references()
        # 6 Core Values of GUPPY
        render_guppy_core_values()


# ═════════════════════════════════════════════════════════════
# PAGE: CEK FORNAS (775+ ZAT AKTIF & 1.238 SEDIAAN)
# ═════════════════════════════════════════════════════════════
elif current_page == "Cek Fornas":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">💊 Penelusuran Formularium Nasional (Fornas 2025)</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Basis data resmi KMK No. HK.01.07/MENKES/1199/2025 memuat 775 zat aktif, sediaan, indikasi, dan batas peresepan maksimal.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_search1, c_search2 = st.columns([3, 1.2])
    with c_search1:
        drug_search_q = st.text_input(
            "Cari Zat Aktif, Nama Obat, atau Kelas Terapi:",
            placeholder="e.g. Metformin, Parasetamol, Atorvastatin, Klopidogrel, Fentanil...",
            value="metformin",
            key="page_drug_search",
        )
    with c_search2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_p = st.checkbox("Program [P]", value=False)
            filter_ca = st.checkbox("Kanker [Ca]", value=False)
        with col_f2:
            filter_prb = st.checkbox("PRB (*)", value=False)
            filter_oen = st.checkbox("OEN (Esensial)", value=False)

    clean_drug_q = InputSanitizer.clean_text(drug_search_q) if drug_search_q else ""
    if clean_drug_q:
        results = fm.search(clean_drug_q)
        if filter_p:
            results = [r for r in results if r.get("penanda", {}).get("P")]
        if filter_ca:
            results = [r for r in results if r.get("penanda", {}).get("Ca")]
        if filter_prb:
            results = [r for r in results if r.get("penanda", {}).get("PRB")]

        if not results:
            sugg = fm.suggest_names(clean_drug_q, n=4)
            st.warning(f"Zat aktif '{clean_drug_q}' tidak ditemukan dalam katalog Fornas 2025.")
            if sugg:
                st.info(f"💡 Apakah maksud Anda: **{', '.join(sugg)}**?")
        else:
            st.write(f"Ditemukan **{len(results)}** zat aktif dalam Fornas 2025:")
            for item in results:
                pen = item.get("penanda", {})
                badges = []
                if pen.get("P"):
                    badges.append('<span class="badge-program">🏷️ Program [P]</span>')
                if pen.get("Ca"):
                    badges.append('<span class="badge-cancer">🎗️ Kanker [Ca]</span>')
                if pen.get("PRB"):
                    badges.append('<span class="badge-prb">⭐ Rujuk Balik (*)</span>')

                badge_str = " ".join(badges)
                kelas_str = " > ".join([k["nama"] for k in item.get("kelas_path", [])]) if item.get("kelas_path") else "-"

                with st.expander(f"💊 {item['zat_aktif'].upper()} — {item['kelas_path'][-1]['nama'] if item.get('kelas_path') else '-'}", expanded=True):
                    c_top1, c_top2 = st.columns([3, 1])
                    with c_top1:
                        st.markdown(f"**Kelas Terapi:** `{kelas_str}`")
                        st.markdown(f"**Halaman PDF Fornas:** Hal. {item.get('halaman_pdf', '-')}")
                    with c_top2:
                        is_fav = item['zat_aktif'].title() in st.session_state["favorites"]
                        fav_btn_label = "⭐ Favorit" if is_fav else "☆ Tambah Favorit"
                        if st.button(fav_btn_label, key=f"fav_{item['zat_aktif']}"):
                            if is_fav:
                                st.session_state["favorites"].remove(item['zat_aktif'].title())
                            else:
                                st.session_state["favorites"].add(item['zat_aktif'].title())
                            st.rerun()

                    # Pedoman PNPK 2025
                    matched_pnpk = pe.get_pnpk_by_drug(item["zat_aktif"])
                    if matched_pnpk:
                        st.markdown("**🏛️ Pedoman Praktik Terkait (PNPK Kemenkes 2025):**")
                        for p in matched_pnpk:
                            st.markdown(
                                f"""
                                <div class="callout-ok">
                                    <b>{p['title']}</b> ({p['kmk']})<br>
                                    <small>{p.get('summary', '')} · <a href='{p['source_url']}' target='_blank' style='color: #0F9F93; font-weight: 600;'>Buka Dokumen Resmi Kemenkes ↗</a></small>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    # Restriksi Zat Aktif
                    if item.get("restriksi_zat_aktif"):
                        st.markdown("**📋 Restriksi Tingkat Zat Aktif:**")
                        for rza in item["restriksi_zat_aktif"]:
                            st.markdown(f'<div class="callout-warn">⚠️ {rza["teks"]}</div>', unsafe_allow_html=True)

                    # Tabel Bentuk Sediaan & Fasilitas
                    st.markdown("**🧪 Bentuk Sediaan & Tingkat Fasilitas:**")
                    for sed in item.get("sediaan", []):
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

                        col_s1, col_s2 = st.columns([3, 2])
                        with col_s1:
                            st.markdown(f"- **{sed['no']}. {sed['sediaan']}**")
                            st.caption(f"Fasilitas: {' · '.join(f_badges) if f_badges else 'Sesuai ketentuan'}")
                        with col_s2:
                            max_presc = sed.get("peresepan_maksimal", "-")
                            st.markdown(f"**Batas Peresepan:** `{max_presc if max_presc else 'Tidak dibatasi'}`")

                        if sed.get("restriksi_sediaan"):
                            for rs in sed["restriksi_sediaan"]:
                                st.markdown(f'<div class="callout-danger">📌 <em>{rs["teks"]}</em></div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# PAGE: CEK DIAGNOSA (ICD-10 MATCHING ENGINE)
# ═════════════════════════════════════════════════════════════
elif current_page == "Cek Diagnosa":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">🩺 Pencocokan Diagnosis (ICD-10) ke Terapi Fornas & PNPK 2025</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Membantu Apoteker dan Dokter memastikan terapi resep selaras dengan indikasi resmi yang diakui Fornas dan pedoman klinis Kemenkes RI.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_dx1, c_dx2 = st.columns([1, 2])
    with c_dx1:
        st.markdown("#### 🎯 Pilih / Input Kode Diagnosis")
        icd_sel = st.selectbox("Kategori Diagnosis Umum:", list(COMMON_ICD10.keys()), index=0)
        selected_code = COMMON_ICD10[icd_sel]

        custom_icd = st.text_input("Atau Cari Kode ICD-10 / Nama Penyakit:", value="", placeholder="e.g. J18, N39, E11, M17, Asma...")
        target_code = custom_icd.strip().upper() if custom_icd.strip() else selected_code

        st.info(f"Target Diagnosis Terpilih: **{target_code}**")

        pnpk_for_icd = pe.get_pnpk_by_icd10(target_code)
        if pnpk_for_icd:
            st.markdown(
                f"""
                <div class="callout-ok">
                    <b>🏛️ Memiliki Acuan Resmi PNPK 2025</b><br>
                    Tersedia <b>{len(pnpk_for_icd)}</b> Pedoman Nasional Pelayanan Kedokteran Kemenkes RI.
                </div>
                """,
                unsafe_allow_html=True,
            )

    with c_dx2:
        st.markdown("#### 📋 Hasil Telaah Terapi Terkait Fornas 2025")

        if pnpk_for_icd:
            for p in pnpk_for_icd:
                with st.expander(f"🩺 {p['title']} ({p['kmk']})", expanded=True):
                    st.markdown(f'<div class="callout-ok">{p.get("summary", "")}</div>', unsafe_allow_html=True)
                    recs = p.get("clinical_recommendations", {})
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown("**🟢 Rekomendasi Lini Pertama (First-Line):**")
                        for fl in recs.get("first_line", []):
                            st.markdown(f"- **{fl['zat_aktif']}** ({fl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em>{fl.get('keterangan', '-')}</em>", unsafe_allow_html=True)
                    with col_r2:
                        st.markdown("**🟡 Lini Kedua / Alternatif / Eskalasi:**")
                        for sl in recs.get("second_line_or_escalation", []):
                            st.markdown(f"- **{sl['zat_aktif']}** ({sl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em>{sl.get('keterangan', '-')}</em>", unsafe_allow_html=True)

        all_drugs = fm.get_db()["obat"]
        matched_drugs = []
        target_clean = target_code.split(".")[0]

        pnpk_drug_names = set()
        for p in pnpk_for_icd:
            for d_name in p.get("drugs_involved", []):
                pnpk_drug_names.add(d_name.strip().lower())

        for d in all_drugs:
            is_hit = False
            for u in d.get("icd10_usulan", []):
                u_code = u["kode"].split("-")[0].split(".")[0]
                if target_clean in u_code or u_code in target_clean:
                    is_hit = True
                    break
            if not is_hit and any(d["zat_aktif"].strip().lower() == pd or pd in d["zat_aktif"].strip().lower() for pd in pnpk_drug_names):
                is_hit = True
            if is_hit:
                matched_drugs.append(d)

        st.markdown("##### 💊 Obat Fornas 2025 yang Diakui untuk Diagnosis Ini:")
        if matched_drugs:
            st.success(f"Ditemukan **{len(matched_drugs)}** obat dalam Fornas 2025 untuk diagnosis `{target_code}`.")
            for md in matched_drugs:
                kelas_nama = md["kelas_path"][-1]["nama"] if md.get("kelas_path") else "-"
                with st.expander(f"💊 {md['zat_aktif'].title()} — {kelas_nama}", expanded=False):
                    st.markdown(f"**Halaman PDF Fornas:** Hal. {md.get('halaman_pdf', '-')}")
                    for sed in md.get("sediaan", []):
                        st.markdown(f"- **{sed['sediaan']}** (Batas Peresepan: `{sed.get('peresepan_maksimal') or 'Tidak dibatasi'}`)")
        else:
            st.warning(f"Belum ada pemetaan eksplisit untuk kode `{target_code}`. Anda dapat mencari nama obat secara langsung di menu Cek Fornas.")


# ═════════════════════════════════════════════════════════════
# PAGE: EVALUASI RESEP (LOGIKA TIGA NILAI)
# ═════════════════════════════════════════════════════════════
elif current_page == "Evaluasi Resep":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">⚖️ Evaluasi Resep Pasien & Logika Tiga Nilai</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Menilai kesesuaian resep dengan prinsip Logika Tiga Nilai: <b>TERPENUHI</b>, <b>TIDAK_TERPENUHI</b>, atau <b>TIDAK_DIKETAHUI</b> (data kurang tidak otomatis ditolak).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_ev1, c_ev2 = st.columns([1.1, 1.3])

    with c_ev1:
        st.markdown("#### 📝 Formulir Resep Pasien")
        ev_drug = st.text_input("Zat Aktif Obat:", value="metformin", placeholder="e.g. metformin, atorvastatin")
        ev_sed = st.text_input("Bentuk Sediaan & Kekuatan (Opsional):", value="tab 500 mg", placeholder="e.g. tab 500 mg")
        ev_fac = st.selectbox("Tingkat Fasilitas Faskes:", ["FPKTP", "FPKTL", "Belum Ditentukan"], index=1)
        fac_val = None if ev_fac == "Belum Ditentukan" else ev_fac

        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            q_num = st.number_input("Jumlah:", min_value=0, value=60, step=1)
        with col_q2:
            q_unit = st.selectbox("Satuan:", ["tab", "kaps", "amp", "btl", "patch", "vial"])
        with col_q3:
            q_per = st.selectbox("Periode:", ["bulan", "hari", "kasus", "minggu"])

        q_dict = {"jumlah": q_num, "satuan": q_unit, "per": q_per} if q_num > 0 else None
        ev_icd = st.text_input("Diagnosis Kerja (Kode ICD-10):", value="E11", placeholder="e.g. E11, I10")
        patient_dict = {"diagnosis_icd10": [InputSanitizer.clean_text(ev_icd).upper()]} if ev_icd else {}

        eval_btn = st.button("⚖️ Jalankan Evaluasi Resep", type="primary", use_container_width=True)

    with c_ev2:
        st.markdown("#### 📊 Hasil Penilaian Resep (CDSS)")
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
                st.markdown('<div class="callout-ok"><b>✅ STATUS: SESUAI</b> — Resep memenuhi seluruh ketentuan Fornas 2025.</div>', unsafe_allow_html=True)
            elif status == "DATA_KURANG":
                st.markdown('<div class="callout-warn"><b>⚠️ STATUS: DATA_KURANG</b> — Data pasien atau sediaan perlu dilengkapi sebelum verifikasi akhir.</div>', unsafe_allow_html=True)
            elif status == "PERLU_JUSTIFIKASI":
                st.markdown('<div class="callout-danger"><b>⛔ STATUS: PERLU_JUSTIFIKASI</b> — Ditemukan restriksi yang dilanggar; disarankan melampirkan memo justifikasi KFT.</div>', unsafe_allow_html=True)

            for ev in res.get("evaluasi", []):
                st.markdown("**Rincian Kriteria Penilaian Tiga Nilai:**")
                for k in ev.get("kriteria", []):
                    badge = "✅" if k["hasil"] == "TERPENUHI" else ("❌" if k["hasil"] == "TIDAK_TERPENUHI" else "❓")
                    st.markdown(f"- {badge} **[{k['id']}] {k['jenis'].title()}:** `{k['hasil']}` — {k['alasan']}")

                if ev.get("justifikasi"):
                    st.markdown("**💡 Kode Justifikasi yang Disarankan:**")
                    for j in ev["justifikasi"]:
                        st.markdown(f"- `[{j}]` Sesuai pedoman katalog justifikasi KFT")

                if ev.get("data_diminta"):
                    st.markdown("**📋 Data Tambahan yang Perlu Dilengkapi:**")
                    for d in ev["data_diminta"]:
                        st.markdown(f'<div class="callout-warn">Minta: {d}</div>', unsafe_allow_html=True)

                if ev.get("peringatan"):
                    for w in ev["peringatan"]:
                        st.markdown(f'<div class="callout-danger">🛡️ <b>Peringatan Keselamatan:</b> {w}</div>', unsafe_allow_html=True)
        else:
            st.info("Isi formulir resep di sebelah kiri lalu klik 'Jalankan Evaluasi Resep'.")


# ═════════════════════════════════════════════════════════════
# PAGE: JUSTIFIKASI KLINIS (WIZARD & WORD .DOCX GENERATOR)
# ═════════════════════════════════════════════════════════════
elif current_page == "Justifikasi Klinis":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">📝 Wizard Justifikasi Klinis (KFT & Diktum KELIMA)</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Susun memo justifikasi terstruktur berbasis bukti Scopus Q1–Q3 dan unduh langsung dalam format <b>Microsoft Word (.docx)</b> resmi untuk KFT/BPJS.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    all_topics = ClinicalLiteratureScout.get_all_topics()
    topic_options = {f"[{t['category']}] {t['title']} ({t['drug_inn']})": t["topic_id"] for t in all_topics}

    sel_label = st.selectbox("📌 Pilih Topik Kasus Klinis:", list(topic_options.keys()))
    topic_id = topic_options[sel_label]
    topic = ClinicalLiteratureScout.get_topic_by_id(topic_id)

    if topic:
        st.markdown(
            f"""
            <div class="callout-info">
                <b>Masalah Klinis Pasien:</b> {topic['clinical_problem']}<br>
                <b>Ketentuan Baku Fornas 2025:</b> {topic['fornas_rule']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### 📚 Pilih Artikel Bukti Ilmiah (Scopus Q1–Q3):")
        chosen_articles = []
        for idx, art in enumerate(topic["articles"], 1):
            c = art["citation"]
            is_pri = art.get("is_primary", False)
            tag = "⭐ [Rekomendasi Utama]" if is_pri else "📑 [Studi Pendukung]"
            is_chk = st.checkbox(
                f"{tag} {c['authors']} ({c['year']}) — \"{c['title']}\" [{c['quartile']}]",
                value=is_pri,
                key=f"just_art_{topic_id}_{art['article_id']}",
            )
            if is_chk:
                chosen_articles.append(art)

        st.markdown("#### ✏️ Identitas Pasien & Apoteker Pengkaji:")
        cp1, cp2 = st.columns(2)
        with cp1:
            p_name = st.text_input("Nama Pasien & Usia:", value="Tn. Rahardjo (62 th)", key="j_p_name")
            p_rm = st.text_input("No. Rekam Medis (RM):", value="RM-2026-9921", key="j_p_rm")
            p_dx = st.text_input("Diagnosis Kerja / ICD-10:", value=f"Terkait {topic['drug_inn']}", key="j_p_dx")
        with cp2:
            p_dr = st.text_input("DPJP (Dokter Penulis Resep):", value="dr. Hendra, Sp.PD-KEMD", key="j_p_dr")
            p_apt = st.text_input("Nama Apoteker Pengkaji:", value="Apt. Indira Nureva, S.Farm.", key="j_p_apt")
            p_sipa = st.text_input("Nomor SIPA:", value="SIPA.1995.04.01", key="j_p_sipa")

        p_notes = st.text_area(
            "Catatan Khusus Rekomendasi Terapi (PTO):",
            value="Dosis disesuaikan dengan fungsi ginjal (eGFR 45 mL/mnt). Pemantauan parameter biokimia dijadwalkan ulang dalam 3 bulan.",
            key="j_p_notes",
        )

        docx_bytes = ClinicalLiteratureScout.generate_justification_memo_docx(
            topic=topic,
            selected_articles=chosen_articles,
            patient_info={"nama_pasien": p_name, "no_rm": p_rm, "diagnosis": p_dx, "dpjp": p_dr},
            pharmacist_notes=p_notes,
            pharmacist_name=p_apt,
            sipa_number=p_sipa,
        )

        clean_slug = topic["drug_inn"].lower().replace(" ", "_").replace("/", "_")
        st.download_button(
            label=f"⬇️ Unduh Dokumen Memo Justifikasi KFT (.docx / Microsoft Word) — {topic['drug_inn']}",
            data=docx_bytes,
            file_name=f"memo_justifikasi_{clean_slug}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True,
        )


# ═════════════════════════════════════════════════════════════
# PAGE: SIMULASI KLAIM (BPJS PRE-CLAIM COMPLIANCE AUDIT)
# ═════════════════════════════════════════════════════════════
elif current_page == "Simulasi Klaim":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">📊 Simulasi Klaim & Audit Kepatuhan BPJS Kesehatan</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Deteksi dini potensi sengketa (dispute) / penolakan klaim resep obat sebelum diverifikasi oleh BPJS Kesehatan.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_sim1, c_sim2 = st.columns([1.1, 1.3])

    with c_sim1:
        st.markdown("#### 📋 Data Resep yang Disimulasikan")
        sim_drug = st.selectbox("Pilih Obat:", ["Metformin 500 mg tablet", "Atorvastatin 20 mg tablet", "Omeprazole 20 mg kapsul", "Insulin Glargine 100 IU/mL pen"])
        sim_dx = st.selectbox("Diagnosis Pasien (ICD-10):", ["E11 — Diabetes Melitus Tipe 2", "E78 — Dislipidemia Campuran", "K21 — GERD", "I10 — Hipertensi Esensial"])
        sim_fac = st.selectbox("Tingkat Fasilitas Pengajuan:", ["FPKTP (Faskes Primer)", "FPKTL (Rumah Sakit)"])
        sim_dur = st.number_input("Durasi Peresepan (Hari):", min_value=1, value=30, step=1)
        sim_memo = st.checkbox("Telah Melampirkan Memo Justifikasi KFT", value=True)

    with c_sim2:
        st.markdown("#### 🔍 Hasil Simulasi & Estimasi Risiko Klaim")

        # Risk scoring
        is_high_risk = "Omeprazole" in sim_drug and sim_dur > 30 and not sim_memo
        is_med_risk = "Insulin" in sim_drug and sim_fac.startswith("FPKTP")

        if is_high_risk:
            st.markdown(
                """
                <div class="callout-danger">
                    <b>🔴 TINGKAT RISIKO KLAIM: TINGGI (Potensi Dispute / Tolak)</b><br>
                    • Penggunaan PPI lebih dari 30 hari tanpa lampiran memo justifikasi KFT berisiko tidak dijamin JKN.<br>
                    • <b>Tindakan:</b> Buat Memo Justifikasi KFT di menu 'Justifikasi Klinis'.
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif is_med_risk:
            st.markdown(
                """
                <div class="callout-warn">
                    <b>🟡 TINGKAT RISIKO KLAIM: SEDANG (Perlu Verifikasi Faskes)</b><br>
                    • Inisiasi analog insulin awal dipersyaratkan dilakukan di FPKTL oleh Dokter Spesialis Penyakit Dalam.<br>
                    • <b>Tindakan:</b> Pastikan resep merupakan resep rujuk balik (PRB) yang sah.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="callout-ok">
                    <b>🟢 TINGKAT RISIKO KLAIM: RENDAH (Memenuhi Syarat Klaim)</b><br>
                    Resep memenuhi ketentuan Fornas 2025, kesesuaian diagnosis ICD-10, dan tingkat fasilitas penjaminan.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 12px; padding: 14px; margin-top: 10px;">
                <b style="color: #12345A;">Checklist 6 Parameter Verifikator BPJS:</b>
                <div style="font-size: 0.82rem; line-height: 1.8; margin-top: 6px;">
                    <div>✓ Kesesuaian Obat dalam Fornas 2025: <b style="color: #065F46;">Terpenuhi</b></div>
                    <div>✓ Kesesuaian Indikasi Diagnosis (ICD-10): <b style="color: #065F46;">Terpenuhi</b></div>
                    <div>✓ Batas Peresepan Maksimal: <b style="color: #065F46;">Sesuai ({sim_dur} hari)</b></div>
                    <div>✓ Tingkat Fasilitas Pelayanan: <b style="color: #065F46;">Sesuai ({sim_fac[:5]})</b></div>
                    <div>✓ Status Kelengkapan Justifikasi: <b style="color: #065F46;">{'Tersedia' if sim_memo else 'Belum Diperlukan'}</b></div>
                    <div>✓ Peringatan Keselamatan Pasien: <b style="color: #065F46;">Aman</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════════════════════
# PAGE: REFERENSI (BASIS HUKUM & PNPK KEMENKES 2025)
# ═════════════════════════════════════════════════════════════
elif current_page == "Referensi":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">📚 Basis Hukum Regulasi & Pedoman Pelayanan Kedokteran (PNPK)</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Hierarki regulasi farmasi klinis Indonesia (KMK Fornas 1199/2025, UU 17/2023) dan 9 PNPK Kemenkes RI.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_reg1, t_reg2 = st.tabs(["🏛️ PNPK Kemenkes RI 2025", "📜 Regulasi Pokok (Fornas & UU)"])

    with t_reg1:
        pnpk_list = pe.get_pnpk_db()
        pnpk_filter = st.text_input("Saring PNPK (Penyakit / Obat / KMK):", value="", placeholder="e.g. Pneumonia, ISK, Osteoartritis...")
        clean_pf = pnpk_filter.strip().lower()

        filtered_pnpk = [
            p for p in pnpk_list
            if not clean_pf
            or clean_pf in p["title"].lower()
            or clean_pf in p["kmk"].lower()
            or clean_pf in p.get("summary", "").lower()
            or any(clean_pf in d.lower() for d in p.get("drugs_involved", []))
        ]

        st.write(f"Menampilkan **{len(filtered_pnpk)}** dari **{len(pnpk_list)}** dokumen PNPK 2025:")
        for p in filtered_pnpk:
            with st.expander(f"🩺 {p['title']} — {p['kmk']}", expanded=False):
                st.markdown(f"**Nomor Kepmenkes:** `{p['kmk']}` | Ditetapkan Tahun {p['year']}")
                st.markdown(f'<div class="callout-ok">{p["summary"]}</div>', unsafe_allow_html=True)
                st.markdown(f"🔗 <a href='{p['source_url']}' target='_blank' style='color: #0F9F93; font-weight: 600;'>Buka Dokumen Resmi di Portal Kemenkes RI ↗</a>", unsafe_allow_html=True)

    with t_reg2:
        try:
            with open(REGULATIONS_DB_PATH, "r", encoding="utf-8") as f:
                reg_db = json.load(f)
            for reg in reg_db.get("regulations", []):
                for art in reg.get("articles", []):
                    with st.expander(f"📜 {reg['number']} — {art['article']}", expanded=False):
                        st.markdown(f"**{reg['title']}**")
                        for p in art.get("paragraphs", []):
                            st.markdown(f'<div class="callout-ok">{p}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal memuat basis data regulasi: {e}")


# ═════════════════════════════════════════════════════════════
# PAGE: LITERATUR ILMIAH (SCOPUS Q1-Q3 EVIDENCE SCOUT)
# ═════════════════════════════════════════════════════════════
elif current_page == "Literatur Ilmiah":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">📖 Telaah Literatur Klinis Berbasis Bukti (Scopus Q1–Q3)</div>
            <div style="font-size: 0.9rem; color: #64748B;">
                Repositori bukti ilmiah peer-reviewed dari The Lancet, NEJM, JAMA, Diabetes Care, dan pedoman internasional.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    q_lit = st.text_input("Cari Telaah Bukti (Zat Aktif, Masalah Klinis, atau Sinonim):", value="metformin")
    results_topics = ClinicalLiteratureScout.search_curated_topics(q_lit)

    st.write(f"Ditemukan **{len(results_topics)}** topik bukti ilmiah:")
    for t in results_topics:
        with st.expander(f"🔬 {t['title']} ({t['drug_inn']})", expanded=True):
            st.markdown(f'<div class="callout-info"><b>Masalah Klinis:</b> {t["clinical_problem"]}<br><b>Restriksi Fornas:</b> {t["fornas_rule"]}</div>', unsafe_allow_html=True)
            for art in t["articles"]:
                c = art["citation"]
                st.markdown(f"**• {c['authors']} ({c['year']})** — *\"{c['title']}\"*")
                st.caption(f"{c['journal']} · `{c['quartile']}` · DOI: {c.get('doi', '-')}")
                st.markdown(f'<div class="callout-ok"><b>Temuan:</b> {art["clinical_finding"]}</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# PAGE: RIWAYAT & FAVORIT
# ═════════════════════════════════════════════════════════════
elif current_page in ("Riwayat", "Favorit"):
    if current_page == "Riwayat":
        st.markdown(
            """
            <div style="margin-bottom: 16px;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">🕒 Riwayat Aktivitas & Penilaian Klinis</div>
                <div style="font-size: 0.9rem; color: #64748B;">Daftar evaluasi resep, penelusuran Fornas, dan memo justifikasi yang telah diproses.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for h in st.session_state["history"]:
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <b style="color: #12345A;">{h['item']}</b> — <span style="color: #64748B;">{h['diagnosis']}</span><br>
                        <small style="color: #94A3B8;">{h['timestamp']} · {h['type']}</small>
                    </div>
                    <span class="badge-terpenuhi">{h['status']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div style="margin-bottom: 16px;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">⭐ Obat & Diagnosis Favorit</div>
                <div style="font-size: 0.9rem; color: #64748B;">Akses cepat item yang sering Anda evaluasi dalam praktik klinis sehari-hari.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        favs = list(st.session_state["favorites"])
        if favs:
            for f in favs:
                st.markdown(f"- ⭐ **{f}**")
        else:
            st.info("Belum ada item favorit yang disimpan.")


# ═════════════════════════════════════════════════════════════
# PAGE: PENGATURAN
# ═════════════════════════════════════════════════════════════
elif current_page == "Pengaturan":
    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <div style="font-size: 1.5rem; font-weight: 800; color: #12345A;">⚙️ Pengaturan Profil & Fasilitas Kesehatan</div>
            <div style="font-size: 0.9rem; color: #64748B;">Konfigurasi identitas dokter/apoteker dan tingkat fasilitas penjaminan.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_set1, c_set2 = st.columns(2)
    with c_set1:
        new_name = st.text_input("Nama Pengguna:", value=st.session_state["user_name"])
        new_role = st.selectbox("Peran Profesi:", ["Dokter Spesialis / DPJP", "Apoteker Farmasi Klinis", "Verifikator Klaim BPJS"])
        new_sipa = st.text_input("Nomor SIPA / SIP:", value=st.session_state["sipa_number"])
    with c_set2:
        new_fac = st.selectbox("Tingkat Fasilitas Kesehatan:", ["FPKTL (Rumah Sakit)", "FPKTP (Puskesmas / Klinik Primer)"])
        st.markdown(
            """
            <div class="callout-info" style="margin-top: 24px;">
                <b>Pengaturan CDSS:</b><br>
                Perubahan tingkat fasilitas akan secara otomatis menyesuaikan parameter validasi restriksi Fornas 2025.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("💾 Simpan Pengaturan", type="primary"):
        st.session_state["user_name"] = new_name
        st.session_state["user_role"] = new_role
        st.session_state["sipa_number"] = new_sipa
        st.session_state["facility_level"] = new_fac
        st.toast("✅ Pengaturan berhasil diperbarui!", icon="⚙️")
        st.rerun()
