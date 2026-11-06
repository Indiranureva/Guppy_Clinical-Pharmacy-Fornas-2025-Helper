"""UI Card Components and Dashboard Layout Widgets.

Matches the healthcare design system inspired by the GUPPY mockup:
- Top bar with global search, notifications & profile
- Welcome banner with Mascot speech bubble
- Usage statistics metric cards
- Daily clinical tips with working pagination
- Quick regulatory references
- 6 Core clinical values of GUPPY
"""

import streamlit as st
from guppy.frontend.components.render_utils import render_html
from guppy.frontend.components.mascot import (
    get_welcome_banner_mascot_html,
)


def render_top_bar(
    user_name: str = "dr. Andini",
    facility: str = "Fasilitas Kesehatan",
    unread_notifications: int = 1,
):
    """Render top bar with search, notification bell, and user profile."""
    col_search, col_actions = st.columns([2.5, 1.2])

    with col_search:
        search_query = st.text_input(
            "Cari obat, diagnosa, atau kata kunci...",
            placeholder="🔍 Cari obat, diagnosa, atau kata kunci... (Ctrl + K)",
            key="top_global_search",
            label_visibility="collapsed",
        )
        if search_query:
            # If user entered search query, allow quick jumping
            st.session_state["page_drug_search"] = search_query
            st.session_state["nav_selection"] = "Cek Fornas"

    with col_actions:
        notif_badge = (
            f'<span style="position: absolute; top: -3px; right: -3px; background: #EF4444; color: #FFFFFF; border-radius: 50%; width: 16px; height: 16px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 700;">{unread_notifications}</span>'
            if unread_notifications > 0
            else ""
        )
        render_html(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 14px;">
                <div style="position: relative; background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 50%; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; box-shadow: 0 1px 3px rgba(18, 52, 90, 0.04);">
                    <span style="font-size: 1.05rem;">🔔</span>
                    {notif_badge}
                </div>
                <div style="display: flex; align-items: center; gap: 10px; background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 9999px; padding: 4px 14px 4px 6px; box-shadow: 0 1px 3px rgba(18, 52, 90, 0.04);">
                    <div style="width: 28px; height: 28px; border-radius: 50%; background: #E0F2FE; color: #0284C7; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem;">
                        👤
                    </div>
                    <div style="line-height: 1.2;">
                        <div style="font-size: 0.84rem; font-weight: 700; color: #12345A;">{user_name}</div>
                        <div style="font-size: 0.7rem; color: #64748B;">{facility}</div>
                    </div>
                </div>
            </div>
            """
        )


def render_welcome_banner(user_name: str = "dr. Andini"):
    """Render the pastel cream welcome banner with the Guppy mascot."""
    mascot_speech = get_welcome_banner_mascot_html()
    render_html(
        f"""
        <div class="welcome-banner">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                <div style="flex: 1; min-width: 280px;">
                    <div class="welcome-title">Halo, {user_name}!</div>
                    <div class="welcome-subtitle">
                        GUPPY siap membantu memeriksa kesesuaian resep dengan Fornas 2025, restriksi, diagnosa, dan justifikasi klinis.
                    </div>
                    <div class="welcome-meta-pill">
                        <span>🏛️ Acuan: KMK No. HK.01.07/MENKES/1199/2025</span>
                        <span>•</span>
                        <span>💊 775+ Zat Aktif</span>
                        <span>•</span>
                        <span>⚖️ Logika Tiga Nilai (CDSS)</span>
                    </div>
                </div>
                <div style="flex-shrink: 0;">
                    {mascot_speech}
                </div>
            </div>
        </div>
        """
    )


def render_stats_panel(
    searches: int = 152,
    diagnoses: int = 98,
    justifications: int = 67,
    simulations: int = 24,
):
    """Render the 4 pastel metric cards matching the mockup."""
    with st.container(border=True):
        render_html(
            f"""
            <div>
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-size: 0.95rem; font-weight: 700; color: #12345A;">Statistik Penggunaan</span>
                    <span style="font-size: 0.74rem; color: #64748B; background: #F8FAFC; border: 1px solid #CBD5E1; padding: 2px 8px; border-radius: 6px; font-weight: 500;">Bulan ini ▼</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;">
                    <div style="background: #E8F8F0; border: 1px solid #A7F3D0; border-radius: 10px; padding: 10px 6px; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 800; color: #065F46; line-height: 1;">{searches}</div>
                        <div style="font-size: 0.72rem; font-weight: 600; color: #047857; margin-top: 4px;">Pencarian Fornas</div>
                    </div>
                    <div style="background: #EBF3FE; border: 1px solid #BFDBFE; border-radius: 10px; padding: 10px 6px; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 800; color: #1E40AF; line-height: 1;">{diagnoses}</div>
                        <div style="font-size: 0.72rem; font-weight: 600; color: #1D4ED8; margin-top: 4px;">Cek Diagnosa</div>
                    </div>
                    <div style="background: #FFF0E5; border: 1px solid #FED7AA; border-radius: 10px; padding: 10px 6px; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 800; color: #9A3412; line-height: 1;">{justifications}</div>
                        <div style="font-size: 0.72rem; font-weight: 600; color: #C2410C; margin-top: 4px;">Justifikasi Dibuat</div>
                    </div>
                    <div style="background: #F3EEFF; border: 1px solid #DDD6FE; border-radius: 10px; padding: 10px 6px; text-align: center;">
                        <div style="font-size: 1.4rem; font-weight: 800; color: #5B21B6; line-height: 1;">{simulations}</div>
                        <div style="font-size: 0.72rem; font-weight: 600; color: #6D28D9; margin-top: 4px;">Simulasi Klaim</div>
                    </div>
                </div>
            </div>
            """
        )


def render_tips_card(tip_index: int = 1, total_tips: int = 5):
    """Render the clinical tip card with lightbulb and working pagination buttons."""
    tips = [
        "Gunakan kode ICD-10 yang paling spesifik untuk mengurangi risiko penolakan klaim BPJS Kesehatan.",
        "Data yang belum tersedia (TIDAK_DIKETAHUI) tidak boleh otomatis dianggap pelanggaran restriksi.",
        "Sesuai Diktum KELIMA KMK 1199/2025, obat di luar Fornas dapat digunakan dengan persetujuan Komite Medis/KFT.",
        "Pemantauan fungsi ginjal (eGFR) wajib dilakukan berkala pada penggunaan Metformin kronis.",
        "Peresepan PRB (Rujuk Balik) dibatasi maksimal 30 hari untuk menjaga kontinuitas terapi di FKTP.",
    ]
    cur_idx = st.session_state.get("tips_idx", 1)
    current_tip = tips[(cur_idx - 1) % len(tips)]

    with st.container(border=True):
        col_t_title, col_t_prev, col_t_count, col_t_next = st.columns([5, 1, 1.2, 1])
        with col_t_title:
            render_html(
                """
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 1.1rem;">💡</span>
                    <b style="color: #92400E; font-size: 0.88rem;">Tips Hari Ini</b>
                </div>
                """
            )
        with col_t_prev:
            if st.button("◀", key="btn_tip_prev", help="Tips sebelumnya"):
                st.session_state["tips_idx"] = ((cur_idx - 2) % len(tips)) + 1
                st.rerun()
        with col_t_count:
            render_html(
                f"""<div style="text-align: center; font-size: 0.75rem; font-weight: 700; color: #B45309; padding-top: 6px;">{cur_idx}/{total_tips}</div>"""
            )
        with col_t_next:
            if st.button("▶", key="btn_tip_next", help="Tips berikutnya"):
                st.session_state["tips_idx"] = (cur_idx % len(tips)) + 1
                st.rerun()

        render_html(
            f"""
            <div style="font-size: 0.82rem; color: #475569; line-height: 1.45; margin-top: 4px; padding-top: 6px; border-top: 1px solid #FEF3C7;">
                {current_tip}
            </div>
            """
        )


def render_quick_references():
    """Render the quick reference regulatory links."""
    with st.container(border=True):
        render_html(
            """
            <div>
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #EDF2F7;">
                    <span style="font-size: 0.92rem; font-weight: 700; color: #12345A;">Regulasi & Referensi Cepat</span>
                    <span style="color: #0F9F93; font-size: 0.76rem; font-weight: 600;">Lihat Semua ↗</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.82rem;">
                    <div style="display: flex; align-items: center; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #F1F5F9;">
                        <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                            <span>📘</span> <b>KMK No. 1199 Tahun 2025</b>
                        </span>
                        <span style="color: #64748B; font-size: 0.75rem;">↗</span>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #F1F5F9;">
                        <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                            <span>🩺</span> <b>Panduan Koding ICD-10</b>
                        </span>
                        <span style="color: #64748B; font-size: 0.75rem;">↗</span>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #F1F5F9;">
                        <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                            <span>🏛️</span> <b>Diktum KELIMA (Obat di Luar Fornas)</b>
                        </span>
                        <span style="color: #64748B; font-size: 0.75rem;">↗</span>
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between; padding: 4px 0;">
                        <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                            <span>🏷️</span> <b>Ketentuan Simbol dan Tanda Khusus</b>
                        </span>
                        <span style="color: #64748B; font-size: 0.75rem;">↗</span>
                    </div>
                </div>
            </div>
            """
        )


def render_guppy_core_values():
    """Render the 6 Core Values of GUPPY as shown on the far right of the mockup."""
    with st.container(border=True):
        render_html(
            """
            <div>
                <div style="font-size: 0.95rem; font-weight: 800; color: #12345A; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #EDF2F7;">
                    Nilai Utama GUPPY
                </div>
                
                <!-- Value 1 -->
                <div class="value-card-item">
                    <div class="value-icon-badge" style="background: #E8F8F0; color: #065F46;">✓</div>
                    <div>
                        <div class="value-title">Akurat & Terstruktur</div>
                        <div class="value-desc">Mengindeks seluruh tabel Fornas 2025 (Hal. 9–224) secara sistematis.</div>
                    </div>
                </div>

                <!-- Value 2 -->
                <div class="value-card-item">
                    <div class="value-icon-badge" style="background: #EBF3FE; color: #1E40AF;">⚖️</div>
                    <div>
                        <div class="value-title">Logika Tiga Nilai</div>
                        <div class="value-desc">Menilai kriteria peresepan sebagai TERPENUHI, TIDAK_TERPENUHI, atau TIDAK_DIKETAHUI.</div>
                    </div>
                </div>

                <!-- Value 3 -->
                <div class="value-card-item">
                    <div class="value-icon-badge" style="background: #FFF0E5; color: #9A3412;">📋</div>
                    <div>
                        <div class="value-title">Katalog Justifikasi Klinis</div>
                        <div class="value-desc">Kode alasan sah yang dapat diaudit tim KFT/BPJS Kesehatan.</div>
                    </div>
                </div>

                <!-- Value 4 -->
                <div class="value-card-item">
                    <div class="value-icon-badge" style="background: #FFE7EC; color: #9F1239;">🛡️</div>
                    <div>
                        <div class="value-title">Peringatan Keselamatan</div>
                        <div class="value-desc">Restriksi keselamatan (usia, kehamilan, fungsi organ) diprioritaskan di atas kendali biaya.</div>
                    </div>
                </div>

                <!-- Value 5 -->
                <div class="value-card-item">
                    <div class="value-icon-badge" style="background: #F3EEFF; color: #5B21B6;">📖</div>
                    <div>
                        <div class="value-title">Dukungan Bukti Ilmiah</div>
                        <div class="value-desc">Terintegrasi dengan jurnal internasional (Q1–Q3) untuk telaah klinis rasional.</div>
                    </div>
                </div>

                <!-- Value 6 -->
                <div class="value-card-item">
                    <div class="value-icon-badge" style="background: #E0F2FE; color: #0369A1;">👥</div>
                    <div>
                        <div class="value-title">Dirancang untuk Praktisi Klinis</div>
                        <div class="value-desc">Sederhana, adaptif, dan mudah digunakan dokter & apoteker setiap hari.</div>
                    </div>
                </div>
            </div>
            """
        )
