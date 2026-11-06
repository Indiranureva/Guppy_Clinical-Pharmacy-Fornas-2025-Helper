"""Primary Action Cards Component for Beranda.

Displays 4 distinct pastel-accented interactive action cards:
- Cek Fornas (Mint)
- Cek Diagnosa (Blue)
- Buat Justifikasi (Peach)
- Simulasi Klaim (Lavender)
"""

import streamlit as st


def render_four_action_cards():
    """Render the 4 primary action cards with one-click navigation."""
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div class="action-card action-card-mint">
                <div class="action-icon-box" style="background: #E8F8F0; color: #0F9F93;">
                    💊
                </div>
                <div class="action-card-title">Cek Fornas</div>
                <div class="action-card-desc">
                    Lihat ketersediaan obat, restriksi, indikasi, dan ketentuan penulisan.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Buka Cek Fornas →", key="btn_act_fornas", use_container_width=True):
            st.session_state["nav_selection"] = "Cek Fornas"
            st.rerun()

    with c2:
        st.markdown(
            """
            <div class="action-card action-card-blue">
                <div class="action-icon-box" style="background: #EBF3FE; color: #2563EB;">
                    🩺
                </div>
                <div class="action-card-title">Cek Diagnosa</div>
                <div class="action-card-desc">
                    Cocokkan kode ICD-10 dengan ketentuan Fornas & diagnosa yang sesuai.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Buka Cek Diagnosa →", key="btn_act_diag", use_container_width=True):
            st.session_state["nav_selection"] = "Cek Diagnosa"
            st.rerun()

    with c3:
        st.markdown(
            """
            <div class="action-card action-card-peach">
                <div class="action-icon-box" style="background: #FFF0E5; color: #EA580C;">
                    📄
                </div>
                <div class="action-card-title">Buat Justifikasi</div>
                <div class="action-card-desc">
                    Template alasan sah (LINI_1_GAGAL, KONTRAINDIKASI, dll).
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Buka Justifikasi →", key="btn_act_just", use_container_width=True):
            st.session_state["nav_selection"] = "Justifikasi Klinis"
            st.rerun()

    with c4:
        st.markdown(
            """
            <div class="action-card action-card-lavender">
                <div class="action-icon-box" style="background: #F3EEFF; color: #7C3AED;">
                    🧮
                </div>
                <div class="action-card-title">Simulasi Klaim</div>
                <div class="action-card-desc">
                    Cek potensi penolakan dan estimasi kesesuaian klaim BPJS Kesehatan.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Buka Simulasi Klaim →", key="btn_act_klaim", use_container_width=True):
            st.session_state["nav_selection"] = "Simulasi Klaim"
            st.rerun()
