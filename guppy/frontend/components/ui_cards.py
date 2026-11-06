"""UI Card Components and Dashboard Layout Widgets.

Matches the healthcare design system inspired by the GUPPY mockup:
- Pastel cards & badges
- Metric cards
- Quick reference links
- Core value cards
- 4-workflow interactive action cards
"""

import streamlit as st
from guppy.frontend.components.mascot import (
    get_guppy_circle_logo_svg,
    get_welcome_banner_mascot_html,
    get_sidebar_footer_html,
)


def render_top_bar(
    user_name: str = "dr. Andini",
    facility: str = "Fasilitas Kesehatan (FPKTL)",
    unread_notifications: int = 1,
):
    """Render the sleek top bar with global search, notifications, and user profile."""
    col_search, col_actions = st.columns([2.5, 1.2])

    with col_search:
        st.markdown(
            """
            <div style="display: flex; align-items: center; background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 9999px; padding: 6px 16px; box-shadow: 0 1px 3px rgba(18, 52, 90, 0.04);">
                <span style="color: #64748B; font-size: 1rem; margin-right: 8px;">🔍</span>
                <span style="color: #94A3B8; font-size: 0.88rem; flex-grow: 1;">Cari obat, diagnosa, atau kata kunci...</span>
                <span style="background: #F1F5F9; border: 1px solid #CBD5E1; color: #475569; font-size: 0.72rem; font-weight: 600; padding: 2px 8px; border-radius: 6px;">Ctrl + K</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_actions:
        notif_badge = (
            f'<span style="position: absolute; top: -3px; right: -3px; background: #EF4444; color: #FFFFFF; border-radius: 50%; width: 16px; height: 16px; font-size: 0.65rem; display: flex; align-items: center; justify-content: center; font-weight: 700;">{unread_notifications}</span>'
            if unread_notifications > 0
            else ""
        )
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 14px;">
                <div style="position: relative; cursor: pointer; background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 50%; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; box-shadow: 0 1px 3px rgba(18, 52, 90, 0.04);">
                    <span style="font-size: 1.1rem;">🔔</span>
                    {notif_badge}
                </div>
                <div style="display: flex; align-items: center; gap: 10px; background: #FFFFFF; border: 1px solid #E2EAF3; border-radius: 9999px; padding: 4px 14px 4px 6px; box-shadow: 0 1px 3px rgba(18, 52, 90, 0.04);">
                    <div style="width: 30px; height: 30px; border-radius: 50%; background: #E0F2FE; color: #0284C7; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.82rem;">
                        👤
                    </div>
                    <div style="line-height: 1.2;">
                        <div style="font-size: 0.86rem; font-weight: 700; color: #12345A;">{user_name}</div>
                        <div style="font-size: 0.72rem; color: #64748B;">{facility}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_welcome_banner(user_name: str = "dr. Andini"):
    """Render the pastel cream welcome banner with the Guppy mascot."""
    mascot_speech = get_welcome_banner_mascot_html()
    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )


def render_stats_panel(
    searches: int = 152,
    diagnoses: int = 98,
    justifications: int = 67,
    simulations: int = 24,
):
    """Render the 4 pastel metric cards matching the mockup."""
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <div style="font-size: 0.95rem; font-weight: 700; color: #12345A;">Statistik Penggunaan</div>
            <div style="font-size: 0.78rem; color: #64748B; background: #FFFFFF; border: 1px solid #CBD5E1; padding: 2px 8px; border-radius: 6px; font-weight: 500;">Bulan ini ▼</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div style="background: #E8F8F0; border: 1px solid #A7F3D0; border-radius: 12px; padding: 12px; text-align: center;">
                <div style="font-size: 1.55rem; font-weight: 800; color: #065F46; line-height: 1;">{searches}</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #047857; margin-top: 4px;">Pencarian Fornas</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background: #EBF3FE; border: 1px solid #BFDBFE; border-radius: 12px; padding: 12px; text-align: center;">
                <div style="font-size: 1.55rem; font-weight: 800; color: #1E40AF; line-height: 1;">{diagnoses}</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #1D4ED8; margin-top: 4px;">Cek Diagnosa</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div style="background: #FFF0E5; border: 1px solid #FED7AA; border-radius: 12px; padding: 12px; text-align: center;">
                <div style="font-size: 1.55rem; font-weight: 800; color: #9A3412; line-height: 1;">{justifications}</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #C2410C; margin-top: 4px;">Justifikasi Dibuat</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div style="background: #F3EEFF; border: 1px solid #DDD6FE; border-radius: 12px; padding: 12px; text-align: center;">
                <div style="font-size: 1.55rem; font-weight: 800; color: #5B21B6; line-height: 1;">{simulations}</div>
                <div style="font-size: 0.75rem; font-weight: 600; color: #6D28D9; margin-top: 4px;">Simulasi Klaim</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_tips_card(tip_index: int = 1, total_tips: int = 5):
    """Render the clinical tip card with lightbulb and pagination."""
    tips = [
        "Gunakan kode ICD-10 yang paling spesifik untuk mengurangi risiko penolakan klaim BPJS Kesehatan.",
        "Data yang belum tersedia (TIDAK_DIKETAHUI) tidak boleh otomatis dianggap pelanggaran restriksi.",
        "Sesuai Diktum KELIMA KMK 1199/2025, obat di luar Fornas dapat digunakan dengan persetujuan Komite Medis/KFT.",
        "Pemantauan fungsi ginjal (eGFR) wajib dilakukan berkala pada penggunaan Metformin kronis.",
        "Peresepan PRB (Rujuk Balik) dibatasi maksimal 30 hari untuk menjaga kontinuitas terapi di FKTP.",
    ]
    current_tip = tips[(tip_index - 1) % len(tips)]

    st.markdown(
        f"""
        <div class="tips-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.15rem;">💡</span>
                    <b style="color: #92400E; font-size: 0.88rem;">Tips Hari Ini</b>
                </div>
                <div style="font-size: 0.76rem; font-weight: 600; color: #B45309;">{tip_index}/{total_tips}</div>
            </div>
            <div style="font-size: 0.84rem; color: #475569; line-height: 1.45;">
                {current_tip}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_references():
    """Render the quick reference regulatory links."""
    st.markdown(
        """
        <div class="guppy-card">
            <div class="guppy-card-header">
                <span>Regulasi & Referensi Cepat</span>
                <span style="color: #0F9F93; font-size: 0.78rem; font-weight: 600; cursor: pointer;">Lihat Semua ↗</span>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.84rem;">
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F1F5F9;">
                    <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                        <span>📘</span> <b>KMK No. 1199 Tahun 2025</b>
                    </span>
                    <span style="color: #64748B; font-size: 0.78rem;">↗</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F1F5F9;">
                    <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                        <span>🩺</span> <b>Panduan Koding ICD-10</b>
                    </span>
                    <span style="color: #64748B; font-size: 0.78rem;">↗</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F1F5F9;">
                    <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                        <span>🏛️</span> <b>Diktum KELIMA (Obat di Luar Fornas)</b>
                    </span>
                    <span style="color: #64748B; font-size: 0.78rem;">↗</span>
                </div>
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 6px 0;">
                    <span style="display: flex; align-items: center; gap: 8px; color: #1E293B;">
                        <span>🏷️</span> <b>Ketentuan Simbol [P], [Ca], (*)</b>
                    </span>
                    <span style="color: #64748B; font-size: 0.78rem;">↗</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_guppy_core_values():
    """Render the 6 Core Values of GUPPY as shown on the far right of the mockup."""
    st.markdown(
        """
        <div class="guppy-card">
            <div style="font-size: 0.98rem; font-weight: 800; color: #12345A; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid #EDF2F7;">
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
        """,
        unsafe_allow_html=True,
    )
