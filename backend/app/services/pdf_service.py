from datetime import datetime
from decimal import Decimal
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.config import get_settings
from app.models.auth import User
from app.models.commerce import Order


def _ensure_dir(subfolder: str) -> Path:
    settings = get_settings()
    path = Path(settings.upload_dir) / subfolder
    path.mkdir(parents=True, exist_ok=True)
    return path


def _format_money(value: Decimal | float) -> str:
    return f"${float(value):,.2f}"


def generate_invoice_pdf(order: Order, user: User, numero: str) -> str:
    output_dir = _ensure_dir("invoices")
    filename = f"{numero.replace('-', '_')}.pdf"
    filepath = output_dir / filename

    doc = SimpleDocTemplate(str(filepath), pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>FACTURA</b>", styles["Title"]))
    elements.append(Paragraph(f"Número: {numero}", styles["Normal"]))
    elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>Cliente</b>", styles["Heading2"]))
    elements.append(Paragraph(f"{user.nombres} {user.apellidos}", styles["Normal"]))
    elements.append(Paragraph(f"Email: {user.email}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Pedido #{order.id}</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    data = [["Producto", "Cant.", "Precio", "Subtotal"]]
    for item in order.items:
        data.append([
            item.product_nombre,
            str(item.cantidad),
            _format_money(item.precio_unitario),
            _format_money(item.subtotal),
        ])
    data.append(["", "", "TOTAL", _format_money(order.total)])

    table = Table(data, colWidths=[220, 50, 80, 80])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -2), 0.5, colors.grey),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f0f0f0")),
        ])
    )
    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Gracias por su compra - FastFood Platform", styles["Normal"]))

    doc.build(elements)
    return f"/uploads/invoices/{filename}"


def generate_ticket_pdf(order: Order, user: User, numero: str) -> str:
    output_dir = _ensure_dir("tickets")
    filename = f"{numero.replace('-', '_')}.pdf"
    filepath = output_dir / filename

    doc = SimpleDocTemplate(str(filepath), pagesize=(80 * mm, 200 * mm), rightMargin=5 * mm, leftMargin=5 * mm)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>FASTFOOD</b>", styles["Title"]))
    elements.append(Paragraph(f"Ticket: {numero}", styles["Normal"]))
    elements.append(Paragraph(f"Pedido #{order.id}", styles["Normal"]))
    elements.append(Paragraph(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    elements.append(Paragraph(f"Cliente: {user.nombres} {user.apellidos}", styles["Normal"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("-" * 32, styles["Normal"]))

    for item in order.items:
        line = f"{item.product_nombre} x{item.cantidad}"
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Paragraph(f"  {_format_money(item.subtotal)}", styles["Normal"]))

    elements.append(Paragraph("-" * 32, styles["Normal"]))
    elements.append(Paragraph(f"<b>TOTAL: {_format_money(order.total)}</b>", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("¡Buen provecho!", styles["Normal"]))

    doc.build(elements)
    return f"/uploads/tickets/{filename}"
