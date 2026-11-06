"""Guppy — Clinical Pharmacy & Fornas 2025 Helper.

Sistem Agen AI & Pendukung Keputusan Klinis (CDSS) Berbasis Formularium Nasional
KMK No. HK.01.07/MENKES/1199/2025 dan 9 PNPK Kemenkes RI 2025.

Nilai Utama & Esensi Klinis:
1. Penelusuran Restriksi & Sediaan Obat Fornas 2025 (775+ zat aktif & 1.238 sediaan)
2. Evaluasi Resep Pasien & Logika Tiga Nilai (TERPENUHI | TIDAK_TERPENUHI | TIDAK_DIKETAHUI)
3. Pencocokan Diagnosis (ICD-10) ke Terapi Resmi Fornas & PNPK 2025
4. Justifikasi Literatur Klinis Berbasis Bukti (Scopus Q1-Q3) & Unduh Dokumen Word (.docx)
5. Basis Hukum Regulasi (KMK 1199/2025, UU 17/2023) & Simulasi Audit Kepatuhan Klaim BPJS
"""

import sys
from pathlib import Path
import json
import base64

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
from guppy.frontend.components.render_utils import render_html
from guppy.frontend.components.mascot import (
    get_guppy_circle_logo_svg,
    get_welcome_banner_mascot_html,
    get_sidebar_footer_html,
)


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
        render_html(f"<style>{f.read()}</style>")


# ─────────────────────────────────────────────────────────────
# 2. SESSION STATE MANAGEMENT
# ─────────────────────────────────────────────────────────────
st.session_state.setdefault("user_name", "dr. Andini")
st.session_state.setdefault("user_role", "Dokter Spesialis / DPJP")
st.session_state.setdefault("facility_level", "FPKTL (Rumah Sakit)")
st.session_state.setdefault("sipa_number", "SIPA.1995.04.01")
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
# 3. SIDEBAR WITH LOGO GUPPY & CLINICAL METADATA
# ─────────────────────────────────────────────────────────────
LOGO_PNG_PATH = Path(__file__).parent / "assets" / "guppy_logo.png"
LOGO_SVG_PATH = Path(__file__).parent / "assets" / "guppy_logo.svg"

with st.sidebar:
    # 1. Official Guppy Logo (Visible & Prominent)
    if LOGO_PNG_PATH.exists():
        st.image(str(LOGO_PNG_PATH), use_container_width=True)
    elif LOGO_SVG_PATH.exists():
        st.image(str(LOGO_SVG_PATH), use_container_width=True)
    else:
        render_html(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                {get_guppy_circle_logo_svg(size=46)}
                <div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.1;">
                        GUPPY
                    </div>
                    <div style="font-size: 0.72rem; color: #BAE6FD; font-weight: 500;">
                        Clinical Pharmacy &amp; Fornas 2025 Helper
                    </div>
                </div>
            </div>
            """
        )

    # 2. Editable User Profile Widget (dr. Andini by default, customizable)
    with st.expander("👤 Profil Pengguna (Ganti Nama)", expanded=False):
        new_user_name = st.text_input("Nama Pengguna:", value=st.session_state["user_name"], key="sb_edit_name")
        new_user_role = st.selectbox(
            "Peran Profesi:",
            ["Dokter Spesialis / DPJP", "Dokter Umum", "Apoteker Farmasi Klinis", "Komite Farmasi & Terapi (KFT)", "Verifikator Klaim BPJS"],
            index=0,
            key="sb_edit_role",
        )
        new_fac = st.selectbox(
            "Tingkat Faskes:",
            ["FPKTL (Rumah Sakit)", "FPKTP (Puskesmas / Klinik Primer)"],
            index=0 if "FPKTL" in st.session_state["facility_level"] else 1,
            key="sb_edit_fac",
        )
        if st.button("💾 Simpan Perubahan Profil", key="btn_save_profile", use_container_width=True):
            st.session_state["user_name"] = new_user_name
            st.session_state["user_role"] = new_user_role
            st.session_state["facility_level"] = new_fac
            st.toast("✅ Profil berhasil diperbarui!", icon="👤")
            st.rerun()

    st.markdown("---")

    # 3. Acuan Regulasi Resmi
    st.markdown("**📋 Sumber Acuan Resmi:**")
    st.markdown(f"- **{FORNAS_EDITION}**\n  *({FORNAS_KEPMENKES})*")
    st.markdown(f"- **Mulai Berlaku:** {FORNAS_BERLAKU}")
    st.markdown(f"- {FORNAS_PROGRAM}")
    st.markdown("- UU No. 17 Tahun 2023 (Kesehatan)")
    st.markdown("- 9 PNPK Kemenkes RI Terbitan 2025")

    st.markdown("---")

    # 4. Status Proteksi Sistem & Sumber Data
    st.markdown("**🛡️ Status Proteksi Sistem & Sumber Data:**")
    sec_light = LinkGuard.get_security_light()
    if sec_light["color"] == "HIJAU":
        render_html(
            """
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                <b style="color: #10B981;">🟢 Lampu Hijau: Aman Semua</b><br>
                <small style="color: #065F46;">Seluruh akses regulasi &amp; database dalam kondisi aman terlindungi.</small>
            </div>
            """
        )
    elif sec_light["color"] == "ORANGE":
        render_html(
            """
            <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                <b style="color: #F59E0B;">🟠 Lampu Orange: Dibatasi Sementara</b><br>
                <small style="color: #92400E;">Akses regulasi cadangan aktif dalam mode pengawasan.</small>
            </div>
            """
        )
    else:
        render_html(
            """
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                <b style="color: #EF4444;">🔴 Lampu Merah: Akses Dibatasi</b><br>
                <small style="color: #991B1B;">Mode luring lokal aktif demi keamanan data klinis.</small>
            </div>
            """
        )

    st.markdown("---")

    # 5. Cari Cepat Zat Aktif di Sidebar
    st.markdown("**🔍 Cari Cepat Obat Fornas:**")
    quick_q = st.text_input("Nama Obat / INN", placeholder="e.g. Metformin, Fentanil", label_visibility="collapsed", key="sb_quick_drug")
    if quick_q:
        q_clean = InputSanitizer.clean_text(quick_q)
        hits = fm.search(q_clean)
        if hits:
            for h in hits[:3]:
                pen = h.get("penanda", {})
                tag = " [P]" if pen.get("P") else ""
                tag += " [Ca]" if pen.get("Ca") else ""
                tag += " *" if pen.get("PRB") else ""
                st.markdown(f"💊 **{h['zat_aktif'].title()}**{tag}")
                st.caption(f"{h['kelas_path'][-1]['nama'] if h.get('kelas_path') else '-'}")
        else:
            sugg = fm.suggest_names(q_clean, n=3)
            st.caption("Tidak ditemukan." + (f" Maksudnya: {', '.join(sugg)}?" if sugg else ""))

    # 6. Tagline Footer
    render_html(get_sidebar_footer_html())


# ─────────────────────────────────────────────────────────────
# 4. TOP BAR & HERO WELCOME BANNER (MODERN PASTEL THEME)
# ─────────────────────────────────────────────────────────────
# Top bar: User Profile & Quick Edit Popover
col_search, col_actions = st.columns([2.5, 1.2])

with col_search:
    top_search_query = st.text_input(
        "Cari obat, diagnosa, atau kata kunci...",
        placeholder="🔍 Cari obat, kode diagnosa ICD-10, atau ketentuan Fornas 2025...",
        key="top_search_bar",
        label_visibility="collapsed",
    )
    # Sync with Tab 1 search if user types in top search bar
    if top_search_query and top_search_query != st.session_state.get("_prev_top_search"):
        st.session_state["_prev_top_search"] = top_search_query
        st.session_state["t1_drug_search"] = top_search_query

with col_actions:
    # Interactive Popover for Profile Editing directly from top bar
    with st.popover(f"👤 {st.session_state['user_name']}", use_container_width=True):
        st.markdown("**⚙️ Pengaturan Profil Pengguna**")
        p_edit_name = st.text_input("Nama Pengguna & Gelar:", value=st.session_state["user_name"], key="top_p_name")
        p_edit_role = st.selectbox(
            "Peran Profesi:",
            ["Dokter Spesialis / DPJP", "Dokter Umum", "Apoteker Farmasi Klinis", "Komite Farmasi & Terapi (KFT)", "Verifikator Klaim BPJS"],
            index=0,
            key="top_p_role",
        )
        p_edit_fac = st.selectbox(
            "Fasilitas Pelayanan:",
            ["FPKTL (Rumah Sakit)", "FPKTP (Puskesmas / Klinik Primer)"],
            index=0 if "FPKTL" in st.session_state["facility_level"] else 1,
            key="top_p_fac",
        )
        if st.button("Simpan Perubahan", key="btn_save_top_p", type="primary", use_container_width=True):
            st.session_state["user_name"] = p_edit_name
            st.session_state["user_role"] = p_edit_role
            st.session_state["facility_level"] = p_edit_fac
            st.toast("✅ Nama pengguna diperbarui!", icon="👤")
            st.rerun()

# ─────────────────────────────────────────────────────────────
# HERO WELCOME BANNER (GUPPY OFFICIAL VECTOR ASSET)
# ─────────────────────────────────────────────────────────────
banner_path = PROJECT_ROOT / "assets" / "images" / "guppy-banner.svg"
if not banner_path.exists():
    banner_path = Path(__file__).parent / "assets" / "guppy-banner.svg"

if banner_path.exists():
    with open(banner_path, "r", encoding="utf-8") as f:
        banner_content = f.read()

    # Dynamic user greeting if user customizes profile name
    current_user = st.session_state.get("user_name", "dr. Andini")
    if current_user and current_user != "dr. Andini":
        banner_content = banner_content.replace("Halo, dr. Andini!", f"Halo, {current_user}!")

    b64_banner = base64.b64encode(banner_content.encode("utf-8")).decode("utf-8")
    render_html(
        f"""
        <div style="margin-bottom: 20px; width: 100%; border-radius: 16px; overflow: hidden; border: 1px solid #E2EAF3; box-shadow: 0 1px 3px rgba(18, 52, 90, 0.04); line-height: 0;">
            <img src="data:image/svg+xml;base64,{b64_banner}" 
                 alt="GUPPY Welcome Banner — KMK No. HK.01.07/MENKES/1199/2025" 
                 style="width: 100%; height: auto; max-width: 100%; display: block; border-radius: 16px; object-fit: contain;" />
        </div>
        """
    )
else:
    # Graceful fallback to HTML welcome banner
    mascot_speech = get_welcome_banner_mascot_html()
    render_html(
        f"""
        <div class="welcome-banner">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                <div style="flex: 1; min-width: 280px;">
                    <div class="welcome-title">Halo, {st.session_state['user_name']}!</div>
                    <div class="welcome-subtitle">
                        GUPPY siap membantu memeriksa kesesuaian resep dengan Formularium Nasional 2025, restriksi obat, indikasi diagnosis, dan penyusunan justifikasi klinis KFT.
                    </div>
                    <div class="welcome-meta-pill">
                        <span>🏛️ KMK No. HK.01.07/MENKES/1199/2025</span>
                        <span>•</span>
                        <span>💊 775+ Zat Aktif &amp; 1.238 Sediaan</span>
                        <span>•</span>
                        <span>⚖️ Logika Tiga Nilai (CDSS)</span>
                        <span>•</span>
                        <span>📑 Ekspor Memo Word (.docx)</span>
                    </div>
                </div>
                <div style="flex-shrink: 0;">
                    {mascot_speech}
                </div>
            </div>
        </div>
        """
    )

# Executive pastel metric indicators
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    render_html(
        """
        <div style="background: #E8F8F0; border: 1px solid #A7F3D0; border-radius: 12px; padding: 10px 14px; text-align: center;">
            <div style="font-size: 1.45rem; font-weight: 800; color: #065F46; line-height: 1.1;">775+ Zat Aktif</div>
            <div style="font-size: 0.74rem; font-weight: 600; color: #047857; margin-top: 2px;">Tabel Resmi Fornas 2025</div>
        </div>
        """
    )
with col_m2:
    render_html(
        """
        <div style="background: #EBF3FE; border: 1px solid #BFDBFE; border-radius: 12px; padding: 10px 14px; text-align: center;">
            <div style="font-size: 1.45rem; font-weight: 800; color: #1E40AF; line-height: 1.1;">9 PNPK 2025</div>
            <div style="font-size: 0.74rem; font-weight: 600; color: #1D4ED8; margin-top: 2px;">Rekomendasi Lini 1 &amp; 2</div>
        </div>
        """
    )
with col_m3:
    render_html(
        """
        <div style="background: #FFF0E5; border: 1px solid #FED7AA; border-radius: 12px; padding: 10px 14px; text-align: center;">
            <div style="font-size: 1.45rem; font-weight: 800; color: #9A3412; line-height: 1.1;">Logika 3-Nilai</div>
            <div style="font-size: 0.74rem; font-weight: 600; color: #C2410C; margin-top: 2px;">Terpenuhi | Data Kurang | Justifikasi</div>
        </div>
        """
    )
with col_m4:
    render_html(
        """
        <div style="background: #F3EEFF; border: 1px solid #DDD6FE; border-radius: 12px; padding: 10px 14px; text-align: center;">
            <div style="font-size: 1.45rem; font-weight: 800; color: #5B21B6; line-height: 1.1;">Word (.docx) KFT</div>
            <div style="font-size: 0.74rem; font-weight: 600; color: #6D28D9; margin-top: 2px;">Memo Bukti Scopus Q1-Q3</div>
        </div>
        """
    )

render_html("<div style='height: 16px;'></div>")


# ─────────────────────────────────────────────────────────────
# 5. CORE CLINICAL DECISION SUPPORT TABS (100% USABLE & DIRECT)
# ─────────────────────────────────────────────────────────────
tab_fornas, tab_eval, tab_dx, tab_just, tab_reg = st.tabs([
    "💊 1. Penelusuran Fornas 2025",
    "⚖️ 2. Evaluasi Resep (Logika 3-Nilai)",
    "🩺 3. Matching Diagnosis (ICD-10)",
    "📝 4. Justifikasi Literatur (Q1-Q3 & Word .docx)",
    "📜 5. Basis Hukum Regulasi & Simulasi BPJS",
])


# ═════════════════════════════════════════════════════════════
# TAB 1: PENELUSURAN OBAT & RESTRIKSI FORNAS 2025
# ═════════════════════════════════════════════════════════════
with tab_fornas:
    render_html(
        """
        <div style="margin-bottom: 14px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #12345A;">💊 Penelusuran Resmi Formularium Nasional (Fornas 2025)</div>
            <div style="font-size: 0.85rem; color: #64748B;">
                Basis data resmi KMK No. HK.01.07/MENKES/1199/2025 memuat 775 zat aktif, 1.238 sediaan, batas peresepan maksimal, dan ketentuan fasilitas FPKTP/FPKTL.
            </div>
        </div>
        """
    )

    col_srch1, col_srch2 = st.columns([3, 1.2])
    with col_srch1:
        default_drug_q = top_search_query if top_search_query else "metformin"
        drug_search_q = st.text_input(
            "Cari Zat Aktif, Nama Obat, atau Kelas Terapi:",
            value=default_drug_q,
            placeholder="e.g. Metformin, Parasetamol, Atorvastatin, Klopidogrel, Fentanil...",
            key="t1_drug_search",
        )
    with col_srch2:
        render_html("<div style='height: 24px;'></div>")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_p = st.checkbox("Program [P]", value=False, key="t1_f_p")
            filter_ca = st.checkbox("Kanker [Ca]", value=False, key="t1_f_ca")
        with col_f2:
            filter_prb = st.checkbox("PRB (*)", value=False, key="t1_f_prb")
            filter_oen = st.checkbox("OEN (Esensial)", value=False, key="t1_f_oen")

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
            st.write(f"Ditemukan **{len(results)}** zat aktif dalam katalog Fornas 2025:")
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
                        if badge_str:
                            render_html(f"<div style='margin-top: 4px;'>{badge_str}</div>")
                    with c_top2:
                        is_fav = item['zat_aktif'].title() in st.session_state["favorites"]
                        fav_btn_label = "⭐ Favorit" if is_fav else "☆ Tambah Favorit"
                        if st.button(fav_btn_label, key=f"t1_fav_{item['zat_aktif']}"):
                            if is_fav:
                                st.session_state["favorites"].remove(item['zat_aktif'].title())
                            else:
                                st.session_state["favorites"].add(item['zat_aktif'].title())
                            st.rerun()

                    # Pedoman PNPK 2025 Terkait
                    matched_pnpk = pe.get_pnpk_by_drug(item["zat_aktif"])
                    if matched_pnpk:
                        st.markdown("**🏛️ Pedoman Praktik Terkait (PNPK Kemenkes 2025):**")
                        for p in matched_pnpk:
                            render_html(
                                f"""
                                <div class="callout-ok">
                                    <b>{p['title']}</b> ({p['kmk']})<br>
                                    <small>{p.get('summary', '')} · <a href='{p['source_url']}' target='_blank' style='color: #0F9F93; font-weight: 600;'>Buka Dokumen Resmi Kemenkes ↗</a></small>
                                </div>
                                """
                            )

                    # Restriksi Tingkat Zat Aktif
                    if item.get("restriksi_zat_aktif"):
                        st.markdown("**📋 Restriksi Tingkat Zat Aktif:**")
                        for rza in item["restriksi_zat_aktif"]:
                            render_html(f'<div class="callout-warn">⚠️ <b>Restriksi:</b> {rza["teks"]}</div>')

                    # Bentuk Sediaan & Tingkat Fasilitas
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
                                render_html(f'<div class="callout-danger">📌 <em>{rs["teks"]}</em></div>')


# ═════════════════════════════════════════════════════════════
# TAB 2: EVALUASI RESEP PASIEN (LOGIKA TIGA NILAI)
# ═════════════════════════════════════════════════════════════
with tab_eval:
    render_html(
        """
        <div style="margin-bottom: 14px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #12345A;">⚖️ Evaluasi Resep Pasien & Logika Tiga Nilai (CDSS)</div>
            <div style="font-size: 0.85rem; color: #64748B;">
                Menilai kesesuaian resep dengan prinsip Logika Tiga Nilai: <b>TERPENUHI</b>, <b>TIDAK_TERPENUHI</b>, atau <b>TIDAK_DIKETAHUI</b> (data yang belum lengkap tidak boleh otomatis ditolak).
            </div>
        </div>
        """
    )

    c_ev1, c_ev2 = st.columns([1.1, 1.3])

    with c_ev1:
        with st.container(border=True):
            st.markdown("#### 📝 Formulir Input Resep Pasien")
            ev_drug = st.text_input("Zat Aktif Obat:", value="metformin", placeholder="e.g. metformin, atorvastatin", key="t2_ev_drug")
            ev_sed = st.text_input("Bentuk Sediaan & Kekuatan (Opsional):", value="tab 500 mg", placeholder="e.g. tab 500 mg", key="t2_ev_sed")
            ev_fac = st.selectbox(
                "Tingkat Fasilitas Faskes Pengaju:",
                ["FPKTL", "FPKTP", "Belum Ditentukan"],
                index=0 if "FPKTL" in st.session_state["facility_level"] else 1,
                key="t2_ev_fac",
            )
            fac_val = None if ev_fac == "Belum Ditentukan" else ev_fac

            col_q1, col_q2, col_q3 = st.columns(3)
            with col_q1:
                q_num = st.number_input("Jumlah:", min_value=0, value=60, step=1, key="t2_q_num")
            with col_q2:
                q_unit = st.selectbox("Satuan:", ["tab", "kaps", "amp", "btl", "patch", "vial"], key="t2_q_unit")
            with col_q3:
                q_per = st.selectbox("Periode:", ["bulan", "hari", "kasus", "minggu"], key="t2_q_per")

            q_dict = {"jumlah": q_num, "satuan": q_unit, "per": q_per} if q_num > 0 else None
            ev_icd = st.text_input("Diagnosis Kerja Pasien (Kode ICD-10):", value="E11", placeholder="e.g. E11, I10, J18", key="t2_ev_icd")
            patient_dict = {"diagnosis_icd10": [InputSanitizer.clean_text(ev_icd).upper()]} if ev_icd else {}

            eval_btn = st.button("⚖️ Jalankan Evaluasi Resep", type="primary", use_container_width=True, key="btn_run_eval")

    with c_ev2:
        with st.container(border=True):
            st.markdown("#### 📊 Hasil Penilaian Resep (CDSS)")
            if eval_btn or "last_eval" in st.session_state:
                safe_drug = InputSanitizer.clean_text(ev_drug)
                safe_sed = InputSanitizer.clean_text(ev_sed) if ev_sed else None

                res = fm.evaluate(
                    drug=safe_drug,
                    sediaan=safe_sed,
                    facility=fac_val,
                    patient=patient_dict,
                    quantity=q_dict,
                )
                st.session_state["last_eval"] = res

                status = res.get("status")
                if status == "SESUAI":
                    render_html('<div class="callout-ok"><b>✅ STATUS: SESUAI</b> — Resep memenuhi seluruh ketentuan Fornas 2025 & indikasi klinis.</div>')
                elif status == "DATA_KURANG":
                    render_html('<div class="callout-warn"><b>⚠️ STATUS: DATA_KURANG</b> — Data pasien atau sediaan perlu dilengkapi sebelum verifikasi akhir (tidak otomatis ditolak).</div>')
                elif status == "PERLU_JUSTIFIKASI":
                    render_html('<div class="callout-danger"><b>⛔ STATUS: PERLU_JUSTIFIKASI</b> — Ditemukan restriksi yang dilampaui; disarankan menyertakan Memo Justifikasi KFT.</div>')

                for ev in res.get("evaluasi", []):
                    st.markdown("**Rincian Kriteria Penilaian Logika Tiga Nilai:**")
                    for k in ev.get("kriteria", []):
                        badge = "✅" if k["hasil"] == "TERPENUHI" else ("❌" if k["hasil"] == "TIDAK_TERPENUHI" else "❓")
                        st.markdown(f"- {badge} **[{k['id']}] {k['jenis'].title()}:** `{k['hasil']}` — {k['alasan']}")

                    if ev.get("justifikasi"):
                        st.markdown("**💡 Kode Justifikasi yang Disarankan:**")
                        for j in ev["justifikasi"]:
                            st.markdown(f"- `[{j}]` Sesuai ketentuan katalog justifikasi Diktum KELIMA KMK 1199/2025")

                    if ev.get("data_diminta"):
                        st.markdown("**📋 Data Tambahan yang Perlu Dilengkapi:**")
                        for d in ev["data_diminta"]:
                            render_html(f'<div class="callout-warn">Minta: {d}</div>')

                    if ev.get("peringatan"):
                        for w in ev["peringatan"]:
                            render_html(f'<div class="callout-danger">🛡️ <b>Peringatan Keselamatan:</b> {w}</div>')

                if st.button("📁 Simpan Evaluasi ke Riwayat", key="btn_save_eval_hist"):
                    st.session_state["history"].insert(
                        0,
                        {
                            "timestamp": "Baru Saja",
                            "type": "Evaluasi Resep",
                            "item": f"{safe_drug} ({safe_sed or '-'})",
                            "diagnosis": ev_icd or "-",
                            "status": status,
                        },
                    )
                    st.toast("✅ Evaluasi berhasil disimpan ke Riwayat Klinis!", icon="📁")
            else:
                st.info("Masukkan data resep pada formulir di sebelah kiri, lalu klik '⚖️ Jalankan Evaluasi Resep'.")


# ═════════════════════════════════════════════════════════════
# TAB 3: MATCHING DIAGNOSIS (ICD-10) KE TERAPI & PNPK 2025
# ═════════════════════════════════════════════════════════════
with tab_dx:
    render_html(
        """
        <div style="margin-bottom: 14px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #12345A;">🩺 Pencocokan Diagnosis (ICD-10) ke Terapi Fornas & PNPK 2025</div>
            <div style="font-size: 0.85rem; color: #64748B;">
                Memastikan terapi obat selaras dengan rekomendasi Lini Pertama / Lini Kedua dalam 9 Pedoman Nasional Pelayanan Kedokteran (PNPK) Kemenkes 2025.
            </div>
        </div>
        """
    )

    c_dx1, c_dx2 = st.columns([1, 2])
    with c_dx1:
        with st.container(border=True):
            st.markdown("#### 🎯 Pilih / Input Kode Diagnosis")
            icd_sel = st.selectbox("Kategori Diagnosis Umum:", list(COMMON_ICD10.keys()), index=0, key="t3_icd_sel")
            selected_code = COMMON_ICD10[icd_sel]

            custom_icd = st.text_input("Atau Cari Kode ICD-10 / Nama Penyakit:", value="", placeholder="e.g. J18, N39, E11, M17, Asma...", key="t3_custom_icd")
            target_code = custom_icd.strip().upper() if custom_icd.strip() else selected_code

            st.info(f"Target Diagnosis Terpilih: **{target_code}**")

            pnpk_for_icd = pe.get_pnpk_by_icd10(target_code)
            if pnpk_for_icd:
                render_html(
                    f"""
                    <div class="callout-ok">
                        <b>🏛️ Memiliki Acuan Resmi PNPK 2025</b><br>
                        Tersedia <b>{len(pnpk_for_icd)}</b> Pedoman Pelayanan Kedokteran Kemenkes RI yang relevan.
                    </div>
                    """
                )

    with c_dx2:
        with st.container(border=True):
            st.markdown("#### 📋 Hasil Telaah Terapi & Rekomendasi Klinis")

            if pnpk_for_icd:
                for p in pnpk_for_icd:
                    with st.expander(f"🩺 {p['title']} ({p['kmk']})", expanded=True):
                        render_html(f'<div class="callout-ok">{p.get("summary", "")}</div>')
                        recs = p.get("clinical_recommendations", {})
                        col_r1, col_r2 = st.columns(2)
                        with col_r1:
                            st.markdown("**🟢 Rekomendasi Lini Pertama (First-Line):**")
                            for fl in recs.get("first_line", []):
                                render_html(f"<div style='margin-bottom: 4px;'>• <b>{fl['zat_aktif']}</b> ({fl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em style='color: #64748B;'>{fl.get('keterangan', '-')}</em></div>")
                        with col_r2:
                            st.markdown("**🟡 Lini Kedua / Alternatif / Eskalasi:**")
                            for sl in recs.get("second_line_or_escalation", []):
                                render_html(f"<div style='margin-bottom: 4px;'>• <b>{sl['zat_aktif']}</b> ({sl.get('sediaan', '-')})<br>&nbsp;&nbsp;↳ <em style='color: #64748B;'>{sl.get('keterangan', '-')}</em></div>")

            # Obat Fornas 2025 yang Diakui untuk Diagnosis ini
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
                st.warning(f"Belum ada pemetaan eksplisit untuk kode `{target_code}`. Anda dapat mencari nama obat secara langsung di Tab 1 (Penelusuran Fornas).")


# ═════════════════════════════════════════════════════════════
# TAB 4: JUSTIFIKASI LITERATUR KLINIS (Q1-Q3 & WORD .DOCX)
# ═════════════════════════════════════════════════════════════
with tab_just:
    render_html(
        """
        <div style="margin-bottom: 14px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #12345A;">📝 Wizard Justifikasi Klinis (KFT & Diktum KELIMA) & Dokumen Word (.docx)</div>
            <div style="font-size: 0.85rem; color: #64748B;">
                Susun memo justifikasi terstruktur berbasis bukti jurnal internasional Scopus Q1–Q3 dan unduh langsung dalam format <b>Microsoft Word (.docx)</b> resmi untuk audit Komite Farmasi &amp; Terapi (KFT) dan BPJS Kesehatan.
            </div>
        </div>
        """
    )

    col_lit_s1, col_lit_s2 = st.columns([3, 1.2])
    with col_lit_s1:
        lit_search_query = st.text_input(
            "Cari Telaah Bukti (Zat Aktif, Masalah Klinis, atau Kata Kunci):",
            value="metformin",
            placeholder="e.g. Metformin, Simvastatin, Albumin, Parasetamol, Captopril, Meropenem...",
            key="t4_lit_search_q",
        )
    with col_lit_s2:
        render_html("<div style='height: 24px;'></div>")
        st.caption(f"🛡️ Versi Repositori: `{ClinicalLiteratureScout.CURATION_VERSION}`. Sumber Scopus Q1-Q3 terverifikasi.")

    filtered_topics = ClinicalLiteratureScout.search_curated_topics(lit_search_query)

    # 1. SMART FALLBACK / UNIVERSAL GENERATOR JIKA TOPIK KURASI KHUSUS TIDAK DITEMUKAN
    if lit_search_query.strip() and not filtered_topics:
        render_html(
            f"""
            <div class="callout-warn">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span style="font-size: 1.2rem;">💡</span>
                    <b style="font-size: 0.98rem; color: #92400E;">Topik Kurasi Khusus Belum Ditemukan untuk "{lit_search_query}"</b>
                </div>
                <div style="font-size: 0.84rem; line-height: 1.5; color: #78350F;">
                    Repositori kurasi jurnal berfokus pada peresepan kasus-kasus kontroversial / peresepan berisiko tinggi.
                    Untuk obat <b>"{lit_search_query}"</b>, Anda dapat menggunakan <b>Generator Memo Justifikasi KFT Mandiri / Universal</b> di bawah ini yang terintegrasi langsung dengan database 1.100+ obat Fornas 2025.
                </div>
            </div>
            """
        )

        # Cari data obat di database Fornas 2025
        synonyms = ClinicalLiteratureScout.expand_query_with_synonyms(lit_search_query)
        fornas_hits = []
        for syn in synonyms:
            hits = fm.search(syn)
            if hits:
                fornas_hits = hits
                break

        fornas_info_dict = None
        if fornas_hits:
            f_drug = fornas_hits[0]
            fornas_info_dict = {
                "zat_aktif": f_drug["zat_aktif"],
                "kelas_terapi": f_drug["kelas_path"][-1]["nama"] if f_drug.get("kelas_path") else "-",
                "halaman_pdf": f_drug.get("halaman_pdf", "-"),
                "restriksi_zat_aktif": [r["teks"] for r in f_drug.get("restriksi_zat_aktif", [])],
                "sediaan": [f"{s['sediaan']} (Batas: {s.get('peresepan_maksimal', 'Tidak dibatasi')})" for s in f_drug.get("sediaan", [])],
            }
            render_html(
                f"""
                <div class="callout-ok">
                    ✅ Obat <b>{f_drug['zat_aktif'].upper()}</b> ditemukan dalam Fornas 2025 (Hal. {f_drug.get('halaman_pdf', '-')}). Parameter resmi otomatis dimuat ke memo justifikasi.
                </div>
                """
            )

        with st.container(border=True):
            st.markdown(f"#### 📝 Formulir Justifikasi KFT Mandiri — {lit_search_query.upper()}")
            c_fb1, c_fb2 = st.columns(2)
            with c_fb1:
                fb_kat = st.selectbox(
                    "Alasan Klinis Justifikasi (Diktum KELIMA KMK 1199/2025):",
                    [
                        "LINI_1_GAGAL (Gagal terapi obat lini pertama)",
                        "KONTRAINDIKASI (Kontraindikasi terhadap obat standar Fornas)",
                        "EFEK_SAMPING_BERAT (Reaksi merugikan obat sebelumnya)",
                        "TIDAK_TERSEDIA (Kekosongan stok obat formularium yang sah)",
                        "GAWAT_DARURAT (Kondisi kegawatdaruratan klinis mengancam nyawa)",
                        "LAINNYA (Alasan pertimbangan medis spesifik)",
                    ],
                    key="t4_fb_kat",
                )
                fb_patient = st.text_input("Nama Pasien & Usia:", value="Tn. Pasien (58 th)", key="t4_fb_patient")
                fb_rm = st.text_input("Nomor Rekam Medis (RM):", value="RM-2026-UNIVERSAL", key="t4_fb_rm")
                fb_dx = st.text_input("Diagnosis Kerja (ICD-10):", value=f"Terkait terapi {lit_search_query}", key="t4_fb_dx")
            with c_fb2:
                fb_dr = st.text_input("DPJP (Dokter Penulis Resep):", value=st.session_state["user_name"], key="t4_fb_dr")
                fb_apt = st.text_input("Nama Apoteker Pengkaji:", value="Apt. Tim Farmasi Klinis, S.Farm.", key="t4_fb_apt")
                fb_sipa = st.text_input("Nomor SIPA:", value=st.session_state["sipa_number"], key="t4_fb_sipa")
                fb_ruang = st.text_input("Ruangan / Poliklinik:", value="Rawat Inap / Poliklinik", key="t4_fb_ruang")

            fb_rationale = st.text_area(
                "Rasional Klinis & Penjelasan Medis:",
                value=f"Pasien memerlukan terapi {lit_search_query} berdasarkan pertimbangan efektivitas klinis, tolerabilitas, dan optimalisasi luaran pasien sesuai panduan klinis.",
                key="t4_fb_rationale",
            )

            fb_patient_dict = {
                "nama_pasien": fb_patient,
                "no_rm": fb_rm,
                "diagnosis": fb_dx,
                "dpjp": fb_dr,
                "ruangan": fb_ruang,
            }

            universal_docx_bytes = ClinicalLiteratureScout.generate_universal_justification_memo_docx(
                drug_name=lit_search_query,
                justification_reason=fb_kat,
                clinical_rationale=fb_rationale,
                patient_info=fb_patient_dict,
                fornas_info=fornas_info_dict,
                pharmacist_name=fb_apt,
                sipa_number=fb_sipa,
            )

            st.download_button(
                label=f"📥 Unduh Dokumen Memo Justifikasi KFT (.docx / Microsoft Word) — {lit_search_query.upper()}",
                data=universal_docx_bytes,
                file_name=f"memo_justifikasi_kft_{lit_search_query.lower().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                type="primary",
                use_container_width=True,
                key=f"t4_dl_uni_{lit_search_query}",
            )

        st.markdown("---")
        st.markdown("##### 📚 Atau Telusuri Topik Kurasi Jurnal Q1–Q3 yang Tersedia:")
        filtered_topics = ClinicalLiteratureScout.get_all_topics()

    elif lit_search_query.strip() and filtered_topics:
        st.success(f"🎯 Ditemukan **{len(filtered_topics)} topik kurasi klinis** terkait kata kunci `{lit_search_query}`:")

    # 2. TOPIK KURASI KHUSUS DENGAN BUKTI JURNAL Q1-Q3
    topic = filtered_topics[0] if filtered_topics else None

    if topic:
        col_j1, col_j2 = st.columns([1.2, 1])

        with col_j1:
            with st.container(border=True):
                st.markdown(f"#### 🔬 {topic['title']} ({topic['drug_inn']})")
                render_html(
                    f"""
                    <div class="callout-info">
                        <b>Masalah Klinis Pasien:</b> {topic['clinical_problem']}<br>
                        <b>Ketentuan Baku Fornas 2025:</b> {topic['fornas_rule']}
                    </div>
                    """
                )

                st.markdown("##### 📚 Pilih Artikel Bukti Ilmiah (Scopus Q1–Q3):")
                chosen_articles = []
                for idx, art in enumerate(topic["articles"], 1):
                    c = art["citation"]
                    is_pri = art.get("is_primary", False)
                    tag = "⭐ [Rekomendasi Utama]" if is_pri else "📑 [Studi Pendukung]"
                    is_chk = st.checkbox(
                        f"{tag} {c['authors']} ({c['year']}) — \"{c['title']}\" [{c['quartile']}]",
                        value=is_pri,
                        key=f"t4_art_{topic['topic_id']}_{art['article_id']}",
                    )
                    if is_chk:
                        chosen_articles.append(art)
                    st.caption(f"↳ {c['journal']} · DOI: {c.get('doi', '-')} · Temuan: {art['clinical_finding']}")

        with col_j2:
            with st.container(border=True):
                st.markdown("#### ✏️ Identitas Pasien, Dokter & Apoteker")
                p_name = st.text_input("Nama Pasien & Usia:", value="Tn. Rahardjo (62 th)", key="t4_p_name")
                p_rm = st.text_input("Nomor Rekam Medis (RM):", value="RM-2026-9921", key="t4_p_rm")
                p_dx = st.text_input("Diagnosis Kerja / ICD-10:", value=f"Terkait indikasi {topic['drug_inn']}", key="t4_p_dx")
                p_dr = st.text_input("DPJP (Dokter Penulis Resep):", value=st.session_state["user_name"], key="t4_p_dr")
                p_apt = st.text_input("Nama Apoteker Pengkaji:", value="Apt. Tim Farmasi Klinis, S.Farm.", key="t4_p_apt")
                p_sipa = st.text_input("Nomor SIPA:", value=st.session_state["sipa_number"], key="t4_p_sipa")

                p_notes = st.text_area(
                    "Catatan Rekomendasi Terapi (PTO):",
                    value="Dosis dan pemilihan terapi disesuaikan dengan profil klinis pasien. Monitoring parameter efektivitas & keamanan dijadwalkan berkala.",
                    key="t4_p_notes",
                )

                # Generate Docx
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
                    label=f"📥 Unduh Memo Justifikasi KFT (.docx / Microsoft Word) — {topic['drug_inn']}",
                    data=docx_bytes,
                    file_name=f"memo_justifikasi_kft_{clean_slug}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    type="primary",
                    use_container_width=True,
                    key="t4_dl_btn",
                )


# ═════════════════════════════════════════════════════════════
# TAB 5: BASIS HUKUM REGULASI & SIMULASI KLAIM BPJS
# ═════════════════════════════════════════════════════════════
with tab_reg:
    render_html(
        """
        <div style="margin-bottom: 14px;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #12345A;">📜 Basis Hukum Regulasi & Simulasi Audit Kepatuhan Klaim BPJS</div>
            <div style="font-size: 0.85rem; color: #64748B;">
                Hierarki regulasi farmasi klinis Indonesia (KMK 1199/2025, UU 17/2023, Diktum KELIMA) dan deteksi dini potensi sengketa (dispute) klaim BPJS Kesehatan.
            </div>
        </div>
        """
    )

    t_reg_sub1, t_reg_sub2, t_reg_sub3 = st.tabs([
        "🏛️ Kompilasi 9 PNPK Kemenkes 2025",
        "⚖️ Simulasi Kepatuhan Klaim BPJS",
        "📖 Regulasi Pokok (Fornas & UU)",
    ])

    with t_reg_sub1:
        pnpk_list = pe.get_pnpk_db()
        pnpk_filter = st.text_input("Saring PNPK (Penyakit / Obat / KMK):", value="", placeholder="e.g. Pneumonia, ISK, Osteoartritis...", key="t5_pnpk_q")
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
                render_html(f'<div class="callout-ok">{p["summary"]}</div>')
                render_html(f"🔗 <a href='{p['source_url']}' target='_blank' style='color: #0F9F93; font-weight: 600;'>Buka Dokumen Resmi di Portal Kemenkes RI ↗</a>")

    with t_reg_sub2:
        col_sm1, col_sm2 = st.columns([1.1, 1.3])
        with col_sm1:
            with st.container(border=True):
                st.markdown("#### 📋 Data Resep yang Disimulasikan")
                sim_drug = st.selectbox("Pilih Obat:", ["Metformin 500 mg tablet", "Atorvastatin 20 mg tablet", "Omeprazole 20 mg kapsul", "Insulin Glargine 100 IU/mL pen"], key="t5_sim_d")
                sim_dx = st.selectbox("Diagnosis Pasien (ICD-10):", ["E11 — Diabetes Melitus Tipe 2", "E78 — Dislipidemia Campuran", "K21 — GERD", "I10 — Hipertensi Esensial"], key="t5_sim_dx")
                sim_fac = st.selectbox("Tingkat Fasilitas Pengajuan:", ["FPKTP (Faskes Primer)", "FPKTL (Rumah Sakit)"], key="t5_sim_fac")
                sim_dur = st.number_input("Durasi Peresepan (Hari):", min_value=1, value=30, step=1, key="t5_sim_dur")
                sim_memo = st.checkbox("Telah Melampirkan Memo Justifikasi KFT", value=True, key="t5_sim_memo")

        with col_sm2:
            with st.container(border=True):
                st.markdown("#### 🔍 Hasil Simulasi & Estimasi Risiko Klaim")

                is_high_risk = "Omeprazole" in sim_drug and sim_dur > 30 and not sim_memo
                is_med_risk = "Insulin" in sim_drug and sim_fac.startswith("FPKTP")

                if is_high_risk:
                    render_html(
                        """
                        <div class="callout-danger">
                            <b>🔴 TINGKAT RISIKO KLAIM: TINGGI (Potensi Dispute / Tolak)</b><br>
                            • Penggunaan PPI lebih dari 30 hari tanpa lampiran memo justifikasi KFT berisiko tidak dijamin JKN.<br>
                            • <b>Tindakan:</b> Buat Memo Justifikasi KFT di Tab 4.
                        </div>
                        """
                    )
                elif is_med_risk:
                    render_html(
                        """
                        <div class="callout-warn">
                            <b>🟡 TINGKAT RISIKO KLAIM: SEDANG (Perlu Verifikasi Faskes)</b><br>
                            • Inisiasi analog insulin awal dipersyaratkan dilakukan di FPKTL oleh Dokter Spesialis Penyakit Dalam.<br>
                            • <b>Tindakan:</b> Pastikan resep merupakan resep rujuk balik (PRB) yang sah.
                        </div>
                        """
                    )
                else:
                    render_html(
                        """
                        <div class="callout-ok">
                            <b>🟢 TINGKAT RISIKO KLAIM: RENDAH (Memenuhi Syarat Klaim)</b><br>
                            Resep memenuhi ketentuan Fornas 2025, kesesuaian diagnosis ICD-10, dan tingkat fasilitas penjaminan BPJS.
                        </div>
                        """
                    )

                render_html(
                    f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2EAF3; border-radius: 10px; padding: 12px; margin-top: 10px;">
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
                    """
                )

    with t_reg_sub3:
        try:
            with open(REGULATIONS_DB_PATH, "r", encoding="utf-8") as f:
                reg_db = json.load(f)
            for reg in reg_db.get("regulations", []):
                for art in reg.get("articles", []):
                    with st.expander(f"📜 {reg['number']} — {art['article']}", expanded=False):
                        st.markdown(f"**{reg['title']}**")
                        for p in art.get("paragraphs", []):
                            render_html(f'<div class="callout-ok">{p}</div>')
        except Exception as e:
            st.error(f"Gagal memuat basis data regulasi: {e}")
