"""Word (.docx) Document Generator for Clinical Justification Memos (KFT / BPJS).

Generates hospital-grade, audit-ready Microsoft Word documents (.docx)
with standardized typography, tables, color-coded callout blocks, and signature boxes.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import io
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn


# Color Constants
COLOR_NAVY = RGBColor(26, 54, 93)       # #1A365D - Deep Navy
COLOR_BLUE = RGBColor(43, 108, 176)     # #2B6CB0 - Medium Blue
COLOR_DARK = RGBColor(45, 55, 72)       # #2D3748 - Dark Charcoal
COLOR_MUTED = RGBColor(113, 128, 150)   # #718096 - Muted Slate
COLOR_GREEN = RGBColor(22, 101, 52)     # #166534 - Forest Green
COLOR_AMBER = RGBColor(146, 64, 14)     # #92400E - Dark Amber

HEX_BG_HEADER = "EBF8FF"   # Light soft blue for table headers
HEX_BG_OK = "F0FDF4"       # Light mint for clinical findings
HEX_BG_WARN = "FFFBEB"     # Light amber for Fornas implications
HEX_BORDER = "CBD5E1"      # Border color for tables


def _set_cell_background(cell, hex_color: str):
    """Set background fill color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def _set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal padding/margins for a table cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def _set_table_borders(table, color=HEX_BORDER, sz="4", val="single"):
    """Apply clean borders to an entire table."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)


def _configure_document_styles(doc: docx.Document):
    """Configure default margins and base font settings."""
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Set normal style font to Calibri
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(10.5)
    font.color.rgb = COLOR_DARK


def _add_document_header(doc: docx.Document, subtitle: str):
    """Add standard hospital KFT letterhead and metadata block."""
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run("MEMO JUSTIFIKASI KLINIS KEPADA KOMITE FARMASI & TERAPI (KFT)")
    run_title.font.size = Pt(14)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    run_sub = p_sub.add_run(subtitle)
    run_sub.font.size = Pt(10.5)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_BLUE

    now_str = datetime.now().strftime("%d %B %Y, %H:%M WIB")
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(14)
    run_meta = p_meta.add_run(f"Dibuat melalui Guppy Clinical Pharmacy & Fornas 2025 Helper — {now_str}")
    run_meta.font.size = Pt(9)
    run_meta.font.italic = True
    run_meta.font.color.rgb = COLOR_MUTED


def _add_section_heading(doc: docx.Document, title: str):
    """Add a section heading with formal styling."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(title)
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY


def _add_signatures_table(
    doc: docx.Document,
    pharmacist_name: str,
    sipa_number: str,
    dpjp_name: str,
):
    """Add standard 3-party KFT approval & signature block."""
    _add_section_heading(doc, "BAGIAN IV: LEMBAR PENGESAHAN & PERSETUJUAN KFT")

    table = doc.add_table(rows=3, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(table)

    headers = [
        "Diajukan oleh\n(Apoteker Pengkaji)",
        "Diverifikasi oleh\n(Dokter Penulis Resep / DPJP)",
        "Disetujui oleh\n(Ketua KFT / Direktur RS)",
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        _set_cell_background(cell, HEX_BG_HEADER)
        _set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h_text)
        run.font.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = COLOR_NAVY

    # Space for physical signature / stamp
    for col_idx in range(3):
        cell = table.cell(1, col_idx)
        _set_cell_margins(cell, top=500, bottom=500, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("\n\n\n( Tanda Tangan & Cap )\n")

    # Signer details
    signers = [
        f"({pharmacist_name})\nNo. SIPA: {sipa_number}",
        f"({dpjp_name})\nDokter Spesialis / DPJP",
        "(...................................................)\nKomite Farmasi & Terapi",
    ]

    for col_idx, s_text in enumerate(signers):
        cell = table.cell(2, col_idx)
        _set_cell_margins(cell, top=100, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(s_text)
        run.font.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = COLOR_DARK

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(8)
    p_note.paragraph_format.space_after = Pt(0)
    run_note = p_note.add_run(
        "*Catatan Audit: Dokumen ini disimpan di Rekam Medis Pasien dan sah sebagai lampiran "
        "pertanggungjawaban klaim BPJS Kesehatan / audit internal sesuai PMK Standar Pelayanan Kefarmasian di RS."
    )
    run_note.font.size = Pt(8.5)
    run_note.font.italic = True
    run_note.font.color.rgb = COLOR_MUTED


def create_justification_memo_docx(
    topic: Dict[str, Any],
    selected_articles: List[Dict[str, Any]],
    patient_info: Optional[Dict[str, str]] = None,
    pharmacist_notes: str = "",
    pharmacist_name: str = "Apoteker Farmasi Klinis",
    sipa_number: str = "SIPA.XXXXXXXXXXXX",
) -> bytes:
    """Generate Word (.docx) document for Curated Topic Clinical Justification Memo."""
    doc = docx.Document()
    _configure_document_styles(doc)

    _add_document_header(
        doc,
        subtitle="Lampiran Telaah Bukti Ilmiah (Q1–Q3) & Adaptasi Restriksi Formularium Nasional"
    )

    # 1. BAGIAN I: DATA PASIEN & MASALAH REGULASI RESEP
    _add_section_heading(doc, "BAGIAN I: DATA PASIEN & MASALAH REGULASI RESEP")

    p_info = patient_info or {}
    patient_name = p_info.get("nama_pasien", "[Nama Pasien]")
    no_rm = p_info.get("no_rm", "[No. Rekam Medis]")
    diagnosis = p_info.get("diagnosis", "[Diagnosis Klinis / ICD-10]")
    dpjp = p_info.get("dpjp", "[Dokter Penanggung Jawab Pelayanan]")
    ruangan = p_info.get("ruangan", "[Instalasi / Bangsal Rawat]")

    kv_items = [
        ("Nama Pasien & Usia", patient_name),
        ("No. Rekam Medis (RM)", no_rm),
        ("Diagnosis Kerja / ICD-10", diagnosis),
        ("DPJP (Dokter Penulis Resep)", dpjp),
        ("Unit / Ruangan Rawat", ruangan),
        ("Obat yang Diajukan Justifikasi", topic.get("drug_inn", "-")),
        ("Kasus / Masalah Klinis Pasien", topic.get("clinical_problem", "-")),
        ("Ketentuan Baku Restriksi Fornas", topic.get("fornas_rule", "-")),
    ]

    table_p = doc.add_table(rows=0, cols=2)
    table_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(table_p)

    for row_idx, (k, v) in enumerate(kv_items):
        row = table_p.add_row()
        cell_k = row.cells[0]
        cell_v = row.cells[1]

        _set_cell_background(cell_k, HEX_BG_HEADER)
        _set_cell_margins(cell_k, top=80, bottom=80, left=120, right=120)
        _set_cell_margins(cell_v, top=80, bottom=80, left=120, right=120)

        cell_k.width = Inches(2.4)
        cell_v.width = Inches(4.1)

        p_k = cell_k.paragraphs[0]
        p_k.paragraph_format.space_after = Pt(0)
        run_k = p_k.add_run(k)
        run_k.font.bold = True
        run_k.font.size = Pt(9.5)
        run_k.font.color.rgb = COLOR_NAVY

        p_v = cell_v.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(0)
        run_v = p_v.add_run(v)
        run_v.font.size = Pt(9.5)
        if k in ("Obat yang Diajukan Justifikasi", "Ketentuan Baku Restriksi Fornas"):
            run_v.font.bold = True

    # 2. BAGIAN II: TELAAH BUKTI ILMIAH TERAKREDITASI
    _add_section_heading(doc, "BAGIAN II: TELAAH BUKTI ILMIAH TERAKREDITASI (PILIHAN APOTEKER)")

    if not selected_articles:
        p_empty = doc.add_paragraph()
        p_empty.add_run("*(Tidak ada artikel spesifik yang dipilih. Mengacu pada pedoman standar Kemenkes/Fornas)*").font.italic = True
    else:
        for idx, art in enumerate(selected_articles, 1):
            c = art.get("citation", {})
            badge_text = "[REKOMENDASI UTAMA GUPPY]" if art.get("is_primary") else "[STUDI PENDUKUNG / KONSENSUS]"
            
            p_art_head = doc.add_paragraph()
            p_art_head.paragraph_format.space_before = Pt(8)
            p_art_head.paragraph_format.space_after = Pt(2)
            run_num = p_art_head.add_run(f"2.{idx} {badge_text} ")
            run_num.font.bold = True
            run_num.font.size = Pt(10.5)
            run_num.font.color.rgb = COLOR_BLUE

            run_title = p_art_head.add_run(f"\"{c.get('title', '')}\"")
            run_title.font.bold = True
            run_title.font.size = Pt(10.5)
            run_title.font.color.rgb = COLOR_NAVY

            # Citation bullet points
            p_cite = doc.add_paragraph()
            p_cite.paragraph_format.left_indent = Inches(0.2)
            p_cite.paragraph_format.space_after = Pt(3)
            
            run_c1 = p_cite.add_run("• Penulis & Tahun: ")
            run_c1.font.bold = True
            p_cite.add_run(f"{c.get('authors', '-')} ({c.get('year', '-')})\n")

            run_c2 = p_cite.add_run("• Jurnal & Reputasi: ")
            run_c2.font.bold = True
            p_cite.add_run(f"{c.get('journal', '-')}, {c.get('volume_issue', '')} — ")
            run_q = p_cite.add_run(f"[{c.get('quartile', '-')}]\n")
            run_q.font.bold = True
            run_q.font.color.rgb = COLOR_BLUE

            run_c3 = p_cite.add_run("• Jenis Studi & Identifikasi: ")
            run_c3.font.bold = True
            p_cite.add_run(f"{c.get('study_type', 'Clinical Trial')} | DOI: {c.get('doi', '-')} | PMID: {c.get('pmid', '-')}")

            # Callout Box 1: Temuan Klinis Utama
            tbl_ok = doc.add_table(rows=1, cols=1)
            tbl_ok.alignment = WD_TABLE_ALIGNMENT.CENTER
            _set_table_borders(tbl_ok, color="86EFAC")
            cell_ok = tbl_ok.cell(0, 0)
            _set_cell_background(cell_ok, HEX_BG_OK)
            _set_cell_margins(cell_ok, top=80, bottom=80, left=120, right=120)
            cell_ok.width = Inches(6.5)

            p_ok = cell_ok.paragraphs[0]
            p_ok.paragraph_format.space_after = Pt(0)
            run_ok_lbl = p_ok.add_run("🔬 Temuan Klinis Utama: ")
            run_ok_lbl.font.bold = True
            run_ok_lbl.font.size = Pt(9.5)
            run_ok_lbl.font.color.rgb = COLOR_GREEN
            run_ok_txt = p_ok.add_run(art.get("clinical_finding", "-"))
            run_ok_txt.font.size = Pt(9.5)

            # Callout Box 2: Implikasi Restriksi Fornas
            tbl_warn = doc.add_table(rows=1, cols=1)
            tbl_warn.alignment = WD_TABLE_ALIGNMENT.CENTER
            _set_table_borders(tbl_warn, color="FDE68A")
            cell_warn = tbl_warn.cell(0, 0)
            _set_cell_background(cell_warn, HEX_BG_WARN)
            _set_cell_margins(cell_warn, top=80, bottom=80, left=120, right=120)
            cell_warn.width = Inches(6.5)

            p_warn = cell_warn.paragraphs[0]
            p_warn.paragraph_format.space_after = Pt(0)
            run_warn_lbl = p_warn.add_run("🩺 Implikasi terhadap Fornas & KFT: ")
            run_warn_lbl.font.bold = True
            run_warn_lbl.font.size = Pt(9.5)
            run_warn_lbl.font.color.rgb = COLOR_AMBER
            run_warn_txt = p_warn.add_run(art.get("fornas_implication", "-"))
            run_warn_txt.font.size = Pt(9.5)

    # 3. BAGIAN III: REKOMENDASI & SINTESIS APOTEKER KLINIS
    _add_section_heading(doc, "BAGIAN III: REKOMENDASI & SINTESIS APOTEKER KLINIS")

    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_after = Pt(4)
    if pharmacist_notes and pharmacist_notes.strip():
        run_rec = p_rec.add_run(pharmacist_notes.strip())
    else:
        run_rec = p_rec.add_run(
            "Berdasarkan telaah bukti ilmiah di atas, pasien memenuhi kriteria adaptasi restriksi "
            "dengan mempertimbangkan rasio manfaat klinis yang melampaui potensi risiko (favorable risk-benefit balance). "
            "Disarankan pemberian terapi dapat dilanjutkan dengan pemantauan parameter keamanan secara berkala."
        )
    run_rec.font.size = Pt(10)

    p_pto_head = doc.add_paragraph()
    p_pto_head.paragraph_format.space_before = Pt(4)
    p_pto_head.paragraph_format.space_after = Pt(2)
    run_pto = p_pto_head.add_run("Rencana Pemantauan Keamanan Terapi Obat (PTO):")
    run_pto.font.bold = True
    run_pto.font.size = Pt(10)

    pto_points = [
        "Pemantauan tanda vital dan respon terapeutik secara berkala.",
        "Pemeriksaan parameter laboratorium keamanan (fungsi ginjal / hati / elektrolit) sesuai indikasi klinis.",
        "Pelaporan segera kepada DPJP bila timbul Kejadian Tidak Diinginkan (KTD) / Efek Samping Obat (MESO).",
    ]
    for pt in pto_points:
        p_pt = doc.add_paragraph(style='List Bullet')
        p_pt.paragraph_format.space_after = Pt(1)
        run_pt = p_pt.add_run(pt)
        run_pt.font.size = Pt(9.5)

    # 4. BAGIAN IV: LEMBAR PENGESAHAN DOKUMEN KFT
    _add_signatures_table(
        doc,
        pharmacist_name=pharmacist_name,
        sipa_number=sipa_number,
        dpjp_name=dpjp,
    )

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def create_universal_justification_memo_docx(
    drug_name: str,
    justification_reason: str,
    clinical_rationale: str,
    patient_info: Optional[Dict[str, str]] = None,
    fornas_info: Optional[Dict[str, Any]] = None,
    pharmacist_name: str = "Apoteker Farmasi Klinis",
    sipa_number: str = "SIPA.XXXXXXXXXXXX",
) -> bytes:
    """Generate Word (.docx) document for Universal / Custom Clinical Justification Memo."""
    doc = docx.Document()
    _configure_document_styles(doc)

    _add_document_header(
        doc,
        subtitle="Formulir Pengajuan Adaptasi Khusus Terapi Obat / Verifikasi Klaim Rumah Sakit"
    )

    p_info = patient_info or {}
    f_info = fornas_info or {}

    patient_name = p_info.get("nama_pasien", "[Nama Pasien]")
    no_rm = p_info.get("no_rm", "[No. Rekam Medis]")
    diagnosis = p_info.get("diagnosis", f"Kebutuhan Terapi {drug_name.upper()}")
    dpjp = p_info.get("dpjp", "[Dokter Penanggung Jawab Pelayanan]")
    ruangan = p_info.get("ruangan", "[Instalasi / Bangsal Rawat]")

    # 1. BAGIAN I: DATA PASIEN & IDENTITAS TERAPI
    _add_section_heading(doc, "BAGIAN I: DATA PASIEN & IDENTITAS TERAPI OBAT")

    kv_items = [
        ("Nama Pasien & Usia", patient_name),
        ("No. Rekam Medis (RM)", no_rm),
        ("Diagnosis Kerja / ICD-10", diagnosis),
        ("Dokter Penulis Resep (DPJP)", dpjp),
        ("Ruang Rawat / Poliklinik", ruangan),
        ("Nama Obat yang Diajukan", drug_name.upper()),
    ]

    if f_info.get("kelas_terapi"):
        kv_items.append(("Kelas Terapi Fornas 2025", f_info.get("kelas_terapi")))
    if f_info.get("fasilitas"):
        kv_items.append(("Tingkat Fasilitas Penjaminan", f_info.get("fasilitas")))
    if f_info.get("peresepan_maksimal"):
        kv_items.append(("Batas Peresepan Maksimal", f_info.get("peresepan_maksimal")))

    table_p = doc.add_table(rows=0, cols=2)
    table_p.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(table_p)

    for k, v in kv_items:
        row = table_p.add_row()
        cell_k = row.cells[0]
        cell_v = row.cells[1]

        _set_cell_background(cell_k, HEX_BG_HEADER)
        _set_cell_margins(cell_k, top=80, bottom=80, left=120, right=120)
        _set_cell_margins(cell_v, top=80, bottom=80, left=120, right=120)

        cell_k.width = Inches(2.4)
        cell_v.width = Inches(4.1)

        p_k = cell_k.paragraphs[0]
        p_k.paragraph_format.space_after = Pt(0)
        run_k = p_k.add_run(k)
        run_k.font.bold = True
        run_k.font.size = Pt(9.5)
        run_k.font.color.rgb = COLOR_NAVY

        p_v = cell_v.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(0)
        run_v = p_v.add_run(v)
        run_v.font.size = Pt(9.5)
        if k == "Nama Obat yang Diajukan":
            run_v.font.bold = True
            run_v.font.color.rgb = COLOR_BLUE

    # 2. BAGIAN II: ALASAN & KATEGORI JUSTIFIKASI KLINIS (KFT)
    _add_section_heading(doc, "BAGIAN II: ALASAN & KATEGORI JUSTIFIKASI KLINIS (KFT/BPJS)")

    p_kat = doc.add_paragraph()
    p_kat.paragraph_format.space_after = Pt(4)
    run_kat_lbl = p_kat.add_run("Kategori Alasan Justifikasi: ")
    run_kat_lbl.font.bold = True
    run_kat_lbl.font.size = Pt(10)
    run_kat_val = p_kat.add_run(f"[{justification_reason}]")
    run_kat_val.font.bold = True
    run_kat_val.font.size = Pt(10.5)
    run_kat_val.font.color.rgb = COLOR_BLUE

    tbl_rat = doc.add_table(rows=1, cols=1)
    tbl_rat.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(tbl_rat, color="86EFAC")
    cell_rat = tbl_rat.cell(0, 0)
    _set_cell_background(cell_rat, HEX_BG_OK)
    _set_cell_margins(cell_rat, top=100, bottom=100, left=140, right=140)
    cell_rat.width = Inches(6.5)

    p_rat = cell_rat.paragraphs[0]
    p_rat.paragraph_format.space_after = Pt(0)
    run_rat_lbl = p_rat.add_run("Uraian Klinis & Dasar Kebutuhan Pasien:\n")
    run_rat_lbl.font.bold = True
    run_rat_lbl.font.size = Pt(9.5)
    run_rat_lbl.font.color.rgb = COLOR_GREEN

    rat_text = clinical_rationale.strip() if clinical_rationale.strip() else (
        "Pasien memerlukan terapi ini dengan pertimbangan kondisi klinis individual yang mendesak "
        "dan tidak dapat digantikan oleh regimen standar lini pertama demi keselamatan dan pemulihan pasien."
    )
    run_rat_txt = p_rat.add_run(rat_text)
    run_rat_txt.font.size = Pt(9.5)

    # 3. BAGIAN III: TELAAH REGULASI & STANDAR KESELAMATAN (PTO)
    _add_section_heading(doc, "BAGIAN III: TELAAH REGULASI & STANDAR KESELAMATAN (PTO)")

    reg_points = [
        "Regulasi Acuan: Kepmenkes RI No. HK.01.07/MENKES/1199/2025 tentang Formularium Nasional & UU No. 17/2023 tentang Kesehatan.",
        "Analisis Manfaat vs Risiko (Risk-Benefit): Manfaat terapeutik yang diharapkan secara signifikan melampaui potensi risiko efek samping.",
        "Protokol Pemantauan Terapi Obat (PTO): Apoteker dan DPJP akan memantau respon klinis dan laboratorium keamanan (fungsi hati/ginjal/tanda vital) secara berkala selama terapi berlangsung.",
    ]
    for pt in reg_points:
        p_pt = doc.add_paragraph(style='List Bullet')
        p_pt.paragraph_format.space_after = Pt(2)
        run_pt = p_pt.add_run(pt)
        run_pt.font.size = Pt(9.5)

    # 4. BAGIAN IV: LEMBAR PENGESAHAN DOKUMEN KFT
    _add_signatures_table(
        doc,
        pharmacist_name=pharmacist_name,
        sipa_number=sipa_number,
        dpjp_name=dpjp,
    )

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
