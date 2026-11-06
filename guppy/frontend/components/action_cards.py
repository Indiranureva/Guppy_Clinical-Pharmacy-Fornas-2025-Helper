"""Primary Action Cards Component for Beranda.

Displays 4 distinct pastel-accented interactive action cards matching the mockup:
- Cek Fornas (Mint)
- Cek Diagnosa (Blue)
- Buat Justifikasi (Peach)
- Simulasi Klaim (Lavender)
"""

import streamlit as st
from guppy.frontend.components.render_utils import render_html


def render_four_action_cards():
    """Render the 4 primary action cards with one-click navigation."""
    c1, c2, c3, c4 = st.columns(4)

    # 1. CEK FORNAS
    with c1:
        with st.container(border=True):
            render_html(
                """
                <div style="min-height: 140px; display: flex; flex-direction: column;">
                    <div style="width: 42px; height: 42px; border-radius: 10px; background: #E8F8F0; color: #0F9F93; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; margin-bottom: 12px; border: 1px solid #A7F3D0;">
                        💊
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #12345A; margin-bottom: 6px;">
                        Cek Fornas
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.4; flex-grow: 1;">
                        Lihat ketersediaan obat, restriksi, indikasi, dan ketentuan penulisan.
                    </div>
                </div>
                """
            )
            if st.button("Cek Fornas →", key="btn_act_fornas", use_container_width=True):
                st.session_state["nav_selection"] = "Cek Fornas"
                st.rerun()

    # 2. CEK DIAGNOSA
    with c2:
        with st.container(border=True):
            render_html(
                """
                <div style="min-height: 140px; display: flex; flex-direction: column;">
                    <div style="width: 42px; height: 42px; border-radius: 10px; background: #EBF3FE; color: #2563EB; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; margin-bottom: 12px; border: 1px solid #BFDBFE;">
                        🩺
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #12345A; margin-bottom: 6px;">
                        Cek Diagnosa
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.4; flex-grow: 1;">
                        Cocokkan kode ICD-10 dengan ketentuan Fornas & diagnosa yang sesuai.
                    </div>
                </div>
                """
            )
            if st.button("Cek Diagnosa →", key="btn_act_diag", use_container_width=True):
                st.session_state["nav_selection"] = "Cek Diagnosa"
                st.rerun()

    # 3. BUAT JUSTIFIKASI
    with c3:
        with st.container(border=True):
            render_html(
                """
                <div style="min-height: 140px; display: flex; flex-direction: column;">
                    <div style="width: 42px; height: 42px; border-radius: 10px; background: #FFF0E5; color: #EA580C; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; margin-bottom: 12px; border: 1px solid #FED7AA;">
                        📄
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #12345A; margin-bottom: 6px;">
                        Buat Justifikasi
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.4; flex-grow: 1;">
                        Template alasan sah (LINI_1_GAGAL, KONTRAINDIKASI, dll).
                    </div>
                </div>
                """
            )
            if st.button("Buat Justifikasi →", key="btn_act_just", use_container_width=True):
                st.session_state["nav_selection"] = "Justifikasi Klinis"
                st.rerun()

    # 4. SIMULASI KLAIM
    with c4:
        with st.container(border=True):
            render_html(
                """
                <div style="min-height: 140px; display: flex; flex-direction: column;">
                    <div style="width: 42px; height: 42px; border-radius: 10px; background: #F3EEFF; color: #7C3AED; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; margin-bottom: 12px; border: 1px solid #DDD6FE;">
                        🧮
                    </div>
                    <div style="font-size: 1.05rem; font-weight: 700; color: #12345A; margin-bottom: 6px;">
                        Simulasi Klaim
                    </div>
                    <div style="font-size: 0.8rem; color: #64748B; line-height: 1.4; flex-grow: 1;">
                        Cek potensi penolakan dan estimasi kesesuaian klaim BPJS.
                    </div>
                </div>
                """
            )
            if st.button("Simulasi Klaim →", key="btn_act_klaim", use_container_width=True):
                st.session_state["nav_selection"] = "Simulasi Klaim"
                st.rerun()
