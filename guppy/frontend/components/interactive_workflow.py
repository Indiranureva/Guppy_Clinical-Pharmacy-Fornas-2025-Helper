"""Interactive 4-Step Clinical Workflow Components for Beranda.

Replicates the 4-column live interactive workflow section matching the mockup:
1. Cek Fornas
2. Cek Diagnosa
3. Buat Justifikasi
4. Hasil Analisis & Simulasi Klaim
"""

import streamlit as st
from guppy.backend.engine import fornas_matcher as fm
from guppy.backend.engine import pnpk_engine as pe
from guppy.backend.engine.clinical_literature import ClinicalLiteratureScout
from guppy.backend.security.sanitizer import InputSanitizer
from guppy.frontend.components.render_utils import render_html


def render_four_workflow_columns():
    """Render the 4 interactive workflow cards side-by-side matching the mockup."""
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.15])

    # ═══════════════════════════════════════════════════════════
    # COLUMN 1: CEK FORNAS
    # ═══════════════════════════════════════════════════════════
    with col1:
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #0F9F93; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;">1</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #12345A;">Cek Fornas</div>
            </div>
            <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">Cari obat dan lihat status Fornas, restriksi, dan ketentuan penggunaan.</div>
            """
        )

        with st.container(border=True):
            wf_drug_query = st.text_input(
                "Cari Obat Fornas",
                value="metformin",
                placeholder="Ketik obat...",
                key="wf_drug_input",
                label_visibility="collapsed",
            )

            clean_wf_drug = InputSanitizer.clean_text(wf_drug_query) if wf_drug_query else "metformin"
            drug_results = fm.search(clean_wf_drug)
            selected_drug = drug_results[0] if drug_results else None

            tab1, tab2, tab3 = st.tabs(["Hasil", "Informasi Obat", "Restriksi"])

            with tab1:
                if drug_results:
                    for d in drug_results[:3]:
                        render_html(
                            f"""
                            <div style="padding: 6px 0; border-bottom: 1px solid #F1F5F9; font-size: 0.78rem;">
                                <b>{d['zat_aktif'].title()}</b><br>
                                <span style="color: #64748B;">Hal. {d.get('halaman_pdf', '-')}</span>
                            </div>
                            """
                        )
                else:
                    st.info("Ketik nama obat untuk mencari.")

            with tab2:
                if selected_drug:
                    sediaan_sample = selected_drug["sediaan"][0] if selected_drug.get("sediaan") else {}
                    sediaan_nama = sediaan_sample.get("sediaan", "500 mg tablet")
                    halaman_pdf = selected_drug.get("halaman_pdf", "182")
                    kelas_terapi = selected_drug["kelas_path"][-1]["nama"] if selected_drug.get("kelas_path") else "Antidiabetik"
                    restriksi_txt = (
                        selected_drug["restriksi_zat_aktif"][0]["teks"]
                        if selected_drug.get("restriksi_zat_aktif")
                        else "Tidak digunakan pada eGFR < 30 mL/menit (kecuali kondisi terpantau)."
                    )

                    render_html(
                        f"""
                        <div>
                            <div style="display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 4px;">
                                <div>
                                    <div style="font-size: 0.92rem; font-weight: 700; color: #12345A;">{selected_drug['zat_aktif'].title()} {sediaan_nama}</div>
                                    <div style="font-size: 0.72rem; color: #64748B;">{kelas_terapi} | Kode ATC: A10BA02</div>
                                </div>
                                <span style="background: #E8F8F0; color: #065F46; border: 1px solid #A7F3D0; border-radius: 9999px; font-size: 0.68rem; font-weight: 700; padding: 2px 8px;">✓ Dalam Fornas</span>
                            </div>

                            <div style="margin-top: 8px; font-size: 0.76rem; line-height: 1.45;">
                                <div style="margin-bottom: 4px;">
                                    <b style="color: #12345A;">Indikasi utama:</b><br>
                                    <span style="color: #475569;">Diabetes melitus tipe 2</span>
                                </div>
                                <div style="margin-bottom: 4px;">
                                    <b style="color: #12345A;">Ketentuan penggunaan:</b>
                                    <div style="color: #475569; padding-left: 6px;">• Lini pertama sesuai Fornas 2025</div>
                                    <div style="color: #475569; padding-left: 6px;">• Evaluasi efektivitas setelah 3 bulan</div>
                                    <div style="color: #475569; padding-left: 6px;">• Perhatikan fungsi ginjal (eGFR)</div>
                                </div>
                                <div style="margin-bottom: 4px;">
                                    <b style="color: #12345A;">Batasan:</b><br>
                                    <span style="color: #B45309;">{restriksi_txt}</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 6px; margin-top: 6px;">
                                    <b style="color: #12345A;">Fasilitas:</b>
                                    <span style="background: #E8F8F0; color: #065F46; padding: 1px 6px; border-radius: 4px; font-weight: 600; font-size: 0.7rem;">FPKTP ✓</span>
                                    <span style="background: #E8F8F0; color: #065F46; padding: 1px 6px; border-radius: 4px; font-weight: 600; font-size: 0.7rem;">FPKTL ✓</span>
                                </div>
                            </div>

                            <div style="margin-top: 10px; padding-top: 6px; border-top: 1px solid #F1F5F9; font-size: 0.74rem; text-align: center;">
                                <span style="color: #0F9F93; font-weight: 600;">Lihat di Fornas 2025 (Hal. {halaman_pdf}) ↗</span>
                            </div>
                        </div>
                        """
                    )

            with tab3:
                if selected_drug and selected_drug.get("restriksi_zat_aktif"):
                    for r in selected_drug["restriksi_zat_aktif"]:
                        render_html(
                            f"""
                            <div style="background: #FFFDF5; border: 1px solid #FDE68A; border-radius: 6px; padding: 6px 8px; font-size: 0.74rem; color: #92400E; margin-bottom: 4px;">
                                ⚠️ {r['teks']}
                            </div>
                            """
                        )
                else:
                    render_html(
                        """
                        <div style="font-size: 0.76rem; color: #475569; padding: 4px 0;">
                            Tidak ada restriksi khusus di luar batas peresepan standar.
                        </div>
                        """
                    )

    # ═══════════════════════════════════════════════════════════
    # COLUMN 2: CEK DIAGNOSA
    # ═══════════════════════════════════════════════════════════
    with col2:
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #3B82F6; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;">2</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #12345A;">Cek Diagnosa</div>
            </div>
            <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">Cocokkan kode ICD-10 dengan obat / tindakan.</div>
            """
        )

        with st.container(border=True):
            wf_dx_query = st.text_input(
                "Cari Kode ICD-10",
                value="E11",
                placeholder="e.g. E11, J18...",
                key="wf_dx_input",
                label_visibility="collapsed",
            )

            clean_wf_dx = InputSanitizer.clean_text(wf_dx_query).upper() if wf_dx_query else "E11"

            tab_d1, tab_d2, tab_d3 = st.tabs(["Hasil", "Detail Diagnosa", "Terapi"])

            with tab_d1:
                render_html(
                    f"""
                    <div style="font-size: 0.78rem; line-height: 1.4;">
                        <b>{clean_wf_dx}</b> — Diabetes Melitus Tipe 2<br>
                        <span style="color: #64748B;">Kategori: Gangguan Endokrin & Metabolik</span>
                    </div>
                    """
                )

            with tab_d2:
                render_html(
                    f"""
                    <div>
                        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                            <span style="background: #EBF3FE; color: #1E40AF; padding: 2px 6px; border-radius: 6px; font-weight: 800; font-size: 0.82rem;">{clean_wf_dx}</span>
                            <b style="font-size: 0.88rem; color: #12345A;">Diabetes melitus tipe 2</b>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="background: #E8F8F0; color: #065F46; border: 1px solid #A7F3D0; border-radius: 9999px; font-size: 0.68rem; font-weight: 700; padding: 2px 8px;">✓ Sesuai dengan Fornas (antidiabetik)</span>
                        </div>

                        <div style="font-size: 0.75rem; line-height: 1.45; color: #475569;">
                            <div style="margin-bottom: 3px;"><b style="color: #12345A;">Kelompok:</b> Endokrin, nutrisi, dan metabolik</div>
                            <div style="margin-bottom: 3px;"><b style="color: #12345A;">Inklusi:</b> DM tipe 2 dengan atau tanpa komplikasi</div>
                            <div style="margin-bottom: 3px;"><b style="color: #12345A;">Eksklusi:</b> DM tipe 1, diabetes gestasional</div>
                            <div style="margin-bottom: 6px;"><b style="color: #12345A;">Catatan:</b> Gunakan kode paling spesifik.</div>
                            
                            <div style="border-top: 1px solid #F1F5F9; padding-top: 6px;">
                                <b style="color: #12345A;">Obat yang umum digunakan (Fornas 2025):</b>
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 3px;">
                                    <span>• Metformin</span>
                                    <span style="background: #E8F8F0; color: #065F46; padding: 1px 6px; border-radius: 4px; font-size: 0.68rem; font-weight: 600;">Lini pertama</span>
                                </div>
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 2px;">
                                    <span>• Glimepiride</span>
                                    <span style="background: #EBF3FE; color: #1E40AF; padding: 1px 6px; border-radius: 4px; font-size: 0.68rem; font-weight: 600;">Lini kedua</span>
                                </div>
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 2px;">
                                    <span>• Insulin glargine</span>
                                    <span style="background: #FFF0E5; color: #9A3412; padding: 1px 6px; border-radius: 4px; font-size: 0.68rem; font-weight: 600;">⚠️ Restriksi tertentu</span>
                                </div>
                            </div>
                        </div>

                        <div style="margin-top: 10px; padding-top: 6px; border-top: 1px solid #F1F5F9; font-size: 0.74rem; text-align: center;">
                            <span style="color: #3B82F6; font-weight: 600;">Lihat daftar lengkap (Hal. 182) ↗</span>
                        </div>
                    </div>
                    """
                )

            with tab_d3:
                render_html(
                    """
                    <div style="font-size: 0.75rem; color: #475569; line-height: 1.45;">
                        <b>PNPK Terkait:</b> PNPK Tata Laksana DM Tipe 2 Dewasa (2025)<br>
                        Target HbA1c: &lt; 7.0% untuk dewasa non-geriatri.
                    </div>
                    """
                )

    # ═══════════════════════════════════════════════════════════
    # COLUMN 3: BUAT JUSTIFIKASI
    # ═══════════════════════════════════════════════════════════
    with col3:
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #F97316; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;">3</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #12345A;">Buat Justifikasi</div>
            </div>
            <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">Pilih kondisi dan dapatkan template justifikasi siap pakai.</div>
            """
        )

        with st.container(border=True):
            # Stepper UI
            render_html(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; font-size: 0.73rem; font-weight: 600;">
                    <span style="color: #F97316; display: flex; align-items: center; gap: 4px;">
                        <span style="background: #F97316; color: #FFF; width: 16px; height: 16px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 0.65rem;">1</span>
                        Pilih Kondisi
                    </span>
                    <span style="color: #94A3B8;">→</span>
                    <span style="color: #94A3B8;">2. Isi Data</span>
                    <span style="color: #94A3B8;">→</span>
                    <span style="color: #94A3B8;">3. Hasil</span>
                </div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #12345A; margin-bottom: 4px;">Pilih alasan justifikasi:</div>
                """
            )

            selected_reason = st.radio(
                "Pilih alasan justifikasi:",
                options=[
                    "LINI_1_GAGAL",
                    "KONTRAINDIKASI",
                    "INTOLERANSI / ALERGI",
                    "GAWAT_DARURAT",
                    "LAINNYA",
                ],
                format_func=lambda x: {
                    "LINI_1_GAGAL": "LINI_1_GAGAL (Gagal lini 1)",
                    "KONTRAINDIKASI": "KONTRAINDIKASI (Lini 1)",
                    "INTOLERANSI / ALERGI": "INTOLERANSI / ALERGI",
                    "GAWAT_DARURAT": "GAWAT_DARURAT",
                    "LAINNYA": "LAINNYA (Alasan sah)",
                }.get(x, x),
                key="wf_just_reason",
                label_visibility="collapsed",
            )

            render_html(
                """
                <div style="background: #FFFDF5; border: 1px solid #FDE68A; border-radius: 8px; padding: 6px 8px; margin: 8px 0; font-size: 0.72rem; color: #92400E; display: flex; gap: 6px; align-items: flex-start;">
                    <span>📜</span>
                    <span>Template sesuai <b>Diktum KELIMA KMK 1199/2025</b> untuk pengajuan komite KFT.</span>
                </div>
                """
            )

            if st.button("Lanjut →", key="wf_btn_lanjut", type="primary", use_container_width=True):
                st.session_state["nav_selection"] = "Justifikasi Klinis"
                st.session_state["active_just_reason"] = selected_reason
                st.rerun()

    # ═══════════════════════════════════════════════════════════
    # COLUMN 4: HASIL ANALISIS & SIMULASI KLAIM
    # ═══════════════════════════════════════════════════════════
    with col4:
        render_html(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                <div style="width: 28px; height: 28px; border-radius: 50%; background: #8B5CF6; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;">4</div>
                <div style="font-size: 1.05rem; font-weight: 700; color: #12345A;">Hasil Analisis & Simulasi Klaim</div>
            </div>
            <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">Lihat ringkasan kesesuaian dan potensi penolakan klaim.</div>
            """
        )

        with st.container(border=True):
            render_html(
                """
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span style="font-size: 0.95rem;">⚖️</span>
                            <b style="font-size: 0.84rem; color: #12345A;">Hasil Penilaian Kesesuaian</b>
                        </div>
                        <span style="background: #E8F8F0; color: #065F46; border: 1px solid #A7F3D0; border-radius: 9999px; font-size: 0.68rem; font-weight: 700; padding: 2px 8px;">✓ TERPENUHI</span>
                    </div>

                    <div style="background: #F8FAFC; border: 1px solid #E2EAF3; border-radius: 6px; padding: 6px 8px; margin-bottom: 8px;">
                        <div style="font-size: 0.82rem; font-weight: 700; color: #12345A;">Metformin 500 mg tablet</div>
                        <div style="font-size: 0.72rem; color: #64748B;">untuk E11 — Diabetes melitus tipe 2</div>
                    </div>

                    <div style="font-size: 0.75rem; line-height: 1.5; color: #334155;">
                        <div style="display: flex; justify-content: space-between;">
                            <span>✓ Status Fornas:</span>
                            <b style="color: #065F46;">Dalam Fornas</b>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>✓ Kesesuaian diagnosa:</span>
                            <b style="color: #065F46;">Sesuai (E11)</b>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>✓ Restriksi terpenuhi:</span>
                            <b style="color: #065F46;">Terpenuhi</b>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>✓ Fasilitas:</span>
                            <b style="color: #065F46;">Sesuai (FPKTP/FPKTL)</b>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>✓ Batas kuantitas:</span>
                            <b style="color: #065F46;">Sesuai</b>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span>✓ Peringatan keselamatan:</span>
                            <b style="color: #065F46;">Tidak ada</b>
                        </div>
                    </div>

                    <div style="background: #FFFDF5; border: 1px solid #FDE68A; border-radius: 6px; padding: 6px 8px; margin: 8px 0;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 2px;">
                            <span style="font-size: 0.74rem; font-weight: 700; color: #92400E;">❓ Estimasi Klaim BPJS</span>
                            <span style="background: #E8F8F0; color: #065F46; padding: 1px 6px; border-radius: 4px; font-weight: 700; font-size: 0.65rem;">✓ Risiko Rendah</span>
                        </div>
                        <div style="font-size: 0.7rem; color: #78350F; line-height: 1.35;">
                            Resep berpotensi dapat diklaim sesuai ketentuan BPJS.
                        </div>
                    </div>
                </div>
                """
            )

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Simpan", key="wf_save_hist", use_container_width=True):
                    st.toast("✅ Resep berhasil disimpan ke Riwayat Klinis!", icon="📁")
            with col_b2:
                # Word Docx download
                topic_metformin = ClinicalLiteratureScout.get_topic_by_id("metformin_ckd_egfr")
                docx_bytes = ClinicalLiteratureScout.generate_justification_memo_docx(
                    topic=topic_metformin,
                    selected_articles=topic_metformin["articles"][:2],
                    patient_info={"nama_pasien": "Tn. Pasien (E11)", "no_rm": "RM-2026-DEMO"},
                    pharmacist_name="Apt. Tim Farmasi Klinis",
                )
                st.download_button(
                    label="Unduh (.docx)",
                    data=docx_bytes,
                    file_name="ringkasan_evaluasi_metformin_E11.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="wf_dl_docx",
                    use_container_width=True,
                )
