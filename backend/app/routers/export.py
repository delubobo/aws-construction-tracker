"""
Export router — GET /api/export/csv and /api/export/pdf
"""
import csv
import io
from datetime import date
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rfi import RFI
from app.models.submittal import Submittal
from app.models.change_order import ChangeOrder
from app.models.ofm import OFMItem
from app.models.vendor import Vendor

router = APIRouter(prefix="/api/export", tags=["export"])

PROJECT = "AWS Data Center Expansion — Lubbock Region, Phase 2"
GENERATED = date.today().isoformat()


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def _row(obj, fields):
    return [str(getattr(obj, f, '') or '') for f in fields]


@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    buf = io.StringIO()
    w = csv.writer(buf)

    # --- RFIs ---
    w.writerow(["=== RFI REGISTER ==="])
    w.writerow(["Number", "Title", "Status", "Priority", "GC", "Submitted", "Due Date", "Spec Section"])
    for r in db.query(RFI).order_by(RFI.rfi_number).all():
        w.writerow(_row(r, ["rfi_number", "title", "status", "priority", "assigned_gc",
                            "submitted_date", "due_date", "spec_section"]))
    w.writerow([])

    # --- Submittals ---
    w.writerow(["=== SUBMITTAL REGISTER ==="])
    w.writerow(["Number", "Description", "Spec", "GC", "Rev", "Status", "Response Due", "Returned"])
    for s in db.query(Submittal).order_by(Submittal.submittal_number).all():
        w.writerow(_row(s, ["submittal_number", "description", "spec_section", "assigned_gc",
                            "revision", "status", "response_due", "returned_date"]))
    w.writerow([])

    # --- Change Orders ---
    w.writerow(["=== CHANGE ORDER LOG ==="])
    w.writerow(["Number", "Title", "GC", "Cost Impact ($)", "Schedule (days)", "Status", "Submitted"])
    for c in db.query(ChangeOrder).order_by(ChangeOrder.co_number).all():
        w.writerow(_row(c, ["co_number", "title", "assigned_gc", "cost_impact",
                            "schedule_impact", "status", "submitted_date"]))
    w.writerow([])

    # --- OFM ---
    w.writerow(["=== OFM TRACKER ==="])
    w.writerow(["Tag", "Description", "Supplier", "Expected", "Actual", "Variance (days)", "Status"])
    for o in db.query(OFMItem).order_by(OFMItem.equipment_tag).all():
        w.writerow(_row(o, ["equipment_tag", "description", "supplier", "expected_delivery",
                            "actual_delivery", "variance_days", "rag_status"]))
    w.writerow([])

    # --- Vendors ---
    w.writerow(["=== VENDOR ONBOARDING ==="])
    w.writerow(["Company", "Trade", "Contact", "Email", "NDA", "Orientation", "Badge", "Site Access"])
    for v in db.query(Vendor).order_by(Vendor.company_name).all():
        w.writerow([
            v.company_name, v.trade or '', v.contact_name or '', v.contact_email or '',
            'Yes' if v.nda_signed else 'No',
            'Yes' if v.orientation_complete else 'No',
            'Yes' if v.badge_issued else 'No',
            'Yes' if v.site_access_approved else 'No',
        ])

    buf.seek(0)
    filename = f"tracker-export-{GENERATED}.csv"
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ---------------------------------------------------------------------------
# PDF export
# ---------------------------------------------------------------------------

def _build_pdf(db: Session) -> bytes:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, spaceAfter=4,
                        textColor=colors.HexColor("#1d4ed8"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, spaceAfter=4,
                        textColor=colors.HexColor("#1e293b"))
    small = ParagraphStyle("Small", parent=styles["Normal"], fontSize=8, textColor=colors.HexColor("#64748b"))
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9)

    BRAND = colors.HexColor("#1d4ed8")
    HEADER_BG = colors.HexColor("#dbeafe")
    ALT_ROW = colors.HexColor("#f8fafc")
    RED_ROW = colors.HexColor("#fef2f2")

    def section_table(headers, rows, col_widths, red_rows=None):
        data = [headers] + rows
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), BRAND),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, ALT_ROW]),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
        if red_rows:
            for row_idx in red_rows:
                ts.add("BACKGROUND", (0, row_idx + 1), (-1, row_idx + 1), RED_ROW)
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(ts)
        return t

    def fmt(v):
        return str(v) if v is not None else "—"

    W = 7.0 * inch  # usable width

    story = []

    # --- Cover header ---
    story.append(Paragraph("RFI &amp; Change Order Tracker", h1))
    story.append(Paragraph(PROJECT, h2))
    story.append(Paragraph(f"Generated: {GENERATED} &nbsp;|&nbsp; Confidential — AWS Project Controls", small))
    story.append(HRFlowable(width="100%", thickness=1, color=BRAND, spaceAfter=12))

    # --- RFIs ---
    rfis = db.query(RFI).order_by(RFI.rfi_number).all()
    story.append(Paragraph(f"RFI Register ({len(rfis)} records)", h2))
    rfi_rows = [
        [r.rfi_number, r.title[:55] + "…" if len(r.title) > 55 else r.title,
         r.status, r.priority, r.assigned_gc or "—", fmt(r.due_date)]
        for r in rfis
    ]
    red_rfis = [i for i, r in enumerate(rfis) if r.status != "Closed" and r.due_date and r.due_date < date.today()]
    story.append(section_table(
        ["Number", "Title", "Status", "Priority", "GC", "Due Date"],
        rfi_rows,
        [0.7*inch, 2.6*inch, 0.8*inch, 0.7*inch, 1.6*inch, 0.9*inch],
        red_rows=red_rfis,
    ))
    story.append(Spacer(1, 16))

    # --- Change Orders ---
    cos = db.query(ChangeOrder).order_by(ChangeOrder.co_number).all()
    pending_total = sum(c.cost_impact for c in cos if c.status == "Pending Approval")
    story.append(Paragraph(
        f"Change Order Log ({len(cos)} records — <font color='#1d4ed8'>${pending_total:,.0f} pending approval</font>)",
        h2,
    ))
    co_rows = [
        [c.co_number, c.title[:50] + "…" if len(c.title) > 50 else c.title,
         c.assigned_gc or "—", f"${c.cost_impact:,.0f}", f"{c.schedule_impact}d", c.status]
        for c in cos
    ]
    story.append(section_table(
        ["Number", "Title", "GC", "Cost", "Sched", "Status"],
        co_rows,
        [0.7*inch, 2.5*inch, 1.5*inch, 0.8*inch, 0.55*inch, 1.25*inch],
    ))
    story.append(Spacer(1, 16))

    # --- Submittals ---
    subs = db.query(Submittal).order_by(Submittal.submittal_number).all()
    story.append(Paragraph(f"Submittal Register ({len(subs)} records)", h2))
    sub_rows = [
        [s.submittal_number, s.description[:55] + "…" if len(s.description) > 55 else s.description,
         s.spec_section or "—", s.assigned_gc or "—", str(s.revision), s.status]
        for s in subs
    ]
    story.append(section_table(
        ["Number", "Description", "Spec", "GC", "Rev", "Status"],
        sub_rows,
        [0.7*inch, 2.5*inch, 0.75*inch, 1.5*inch, 0.35*inch, 1.5*inch],
    ))
    story.append(Spacer(1, 16))

    # --- OFM ---
    ofm_items = db.query(OFMItem).order_by(OFMItem.rag_status, OFMItem.equipment_tag).all()
    story.append(Paragraph(f"OFM Tracker ({len(ofm_items)} items)", h2))
    ofm_rows = [
        [o.equipment_tag, o.description[:45] + "…" if len(o.description) > 45 else o.description,
         o.supplier or "—", fmt(o.expected_delivery),
         fmt(o.actual_delivery) if o.actual_delivery else "Pending",
         f"+{o.variance_days}d" if o.variance_days and o.variance_days > 0 else (fmt(o.variance_days) if o.variance_days is not None else "—"),
         o.rag_status]
        for o in ofm_items
    ]
    red_ofm = [i for i, o in enumerate(ofm_items) if o.rag_status == "Red"]
    story.append(section_table(
        ["Tag", "Description", "Supplier", "Expected", "Actual", "Variance", "RAG"],
        ofm_rows,
        [0.7*inch, 2.0*inch, 1.3*inch, 0.85*inch, 0.85*inch, 0.7*inch, 0.55*inch],
        red_rows=red_ofm,
    ))
    story.append(Spacer(1, 16))

    # --- Vendor Onboarding ---
    vendors = db.query(Vendor).order_by(Vendor.company_name).all()
    story.append(Paragraph(f"Vendor Onboarding ({len(vendors)} vendors)", h2))
    vendor_rows = [
        [v.company_name, v.trade or "—", v.contact_name or "—",
         "✓" if v.nda_signed else "✗",
         "✓" if v.orientation_complete else "✗",
         "✓" if v.badge_issued else "✗",
         "✓" if v.site_access_approved else "✗"]
        for v in vendors
    ]
    story.append(section_table(
        ["Company", "Trade", "Contact", "NDA", "Orientation", "Badge", "Site Access"],
        vendor_rows,
        [1.8*inch, 1.2*inch, 1.2*inch, 0.55*inch, 0.85*inch, 0.55*inch, 0.85*inch],
    ))

    # --- Signature block ---
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=8))
    story.append(Paragraph(
        "Prepared by: Project Engineer &nbsp; | &nbsp; "
        "AWS Data Center Expansion, Lubbock Region, Phase 2 &nbsp; | &nbsp; "
        f"Report Date: {GENERATED}",
        small,
    ))

    doc.build(story)
    return buf.getvalue()


@router.get("/pdf")
def export_pdf(db: Session = Depends(get_db)):
    pdf_bytes = _build_pdf(db)
    filename = f"tracker-report-{GENERATED}.pdf"
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
