import os
from fpdf import FPDF
from datetime import datetime
from db_connect import connect_db

def save_invoice_to_db(customer, items, subtotal, discount, tax, gross, notes, pdf_path):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (customer_name, phone_number, address, date, invoice_number,
        invoice_type, status, subtotal, discount, tax, gross_amount, notes, pdf_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        customer['name'], customer['phone'], customer['address'], customer['date'],
        customer['invoice_number'], customer['invoice_type'], customer['status'],
        subtotal, discount, tax, gross, notes, pdf_path
    ))
    invoice_id = cursor.lastrowid
    for item in items:
        cursor.execute("""
            INSERT INTO invoice_items (invoice_id, description, quantity, unit_price, total)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            invoice_id, item['desc'], item['qty'], item['unit_price'], item['total']
        ))

    conn.commit()
    conn.close()


def generate_pdf(customer, items, subtotal, discount, tax, gross, notes):
    if not os.path.exists("invoices"):
        os.makedirs("invoices")
    

    file_name = f"invoice_{customer['invoice_number']}.pdf"
    file_path = f"invoices/{file_name}"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)


    #logo
    if os.path.exists("Dummy_logo.png"):
        pdf.image("Dummy_logo.png", x=5, y=7, w=45)

    # Company Header
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "Company XYZ", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 6, "Company Address Line 1", ln=1, align='C')
    pdf.cell(0, 6, "Company Address Line 2", ln=1, align='C')
    pdf.cell(0, 6, "Phone: +92 3456789012 | Email: contact@company.com", ln=1, align='C')
    pdf.ln(10)

    #Invoice Title
    pdf.set_font("Arial", 'B', 16)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(185, 10, f"{customer['invoice_type'].upper()}", ln=1, align='C', fill=True)
    pdf.ln(5)

    # Customer Info
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 8, f"Customer Name: {customer['name']}")
    pdf.cell(0, 8, f"Date: {customer['date']}", ln=1)
    pdf.cell(100, 8, f"Phone: {customer['phone']}")
    pdf.cell(0, 8, f"Invoice #: {customer['invoice_number']}", ln=1)
    pdf.cell(0, 8, f"Address: {customer['address']}", ln=1)
    pdf.ln(5)

    #table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(230, 230, 230)  # light gray
    pdf.set_text_color(0, 0, 0)
    pdf.cell(15, 10, "#", 0, 0, 'C', True)
    pdf.cell(55, 10, "Description", 0, 0, 'L', True)
    pdf.cell(25, 10, "Qty", 0, 0, 'C', True)
    pdf.cell(45, 10, "Unit Price", 0, 0, 'R', True)
    pdf.cell(45, 10, "Total", 0, 1, 'R', True)


    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(245, 245, 245)
    pdf.set_text_color(0, 0, 0)

    for idx, item in enumerate(items, start=1):
        fill = (idx % 2 == 0)  # alternate row fill
        pdf.cell(15, 10, str(idx), border=0, ln=0, align='C', fill=fill)
        pdf.cell(55, 10, item['desc'], border=0, ln=0, align='L', fill=fill)
        pdf.cell(25, 10, str(item['qty']), border=0, ln=0, align='C', fill=fill)
        pdf.cell(45, 10, f"Rs {item['unit_price']:.2f}", border=0, ln=0, align='R', fill=fill)
        pdf.cell(45, 10, f"Rs {item['total']:.2f}", border=0, ln=1, align='R', fill=fill)
    
    pdf.ln(4)

    def totals_row(label, amount, fill_color=(245, 245, 245), bold=False, is_percent=False):
        font_style = 'B' if bold else ''
        pdf.set_fill_color(*fill_color)
        pdf.set_font("Arial", font_style, 12)
        pdf.cell(140, 10, label, 0, 0, 'R', True)
        if is_percent:
            pdf.cell(45, 10, f"{amount:.2f}%", 0, 1, 'R', True)
        else:
            pdf.cell(45, 10, f"Rs {amount:.2f}", 0, 1, 'R', True)

    totals_row("Subtotal:", subtotal)
    totals_row("Discount:", discount)
    totals_row("Tax:", tax, is_percent=True)
    totals_row("Gross Amount:", gross, fill_color=(220, 220, 220), bold=True)


    #notes
    if notes:
        pdf.ln(6)
        pdf.set_font("Arial", 'I', 11)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 10, f"Notes: {notes}")
        pdf.set_text_color(0, 0, 0)

    pdf.ln(6)

    #header with underline
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 12, "Account Details:", ln=1)
    pdf.set_draw_color(100, 100, 100)  # gray underline
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 184, pdf.get_y())  # underline
    pdf.ln(4)

    #light gray
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Arial", 'B', 11)

    account_items = [
        ("UBL Account #:", "xxxxxxxxxx-xxx"),
        ("ABL Account #:", "xxxxxxxxxx-xxx"),
        ("EasyPaisa #:", "xxxxxxxxxx-xxx"),
        ("JazzCash #:", "xxxxxxxxxx-xxx"),
    ]

    for label, value in account_items:
        pdf.cell(50, 8, label, border=0, ln=0, align='L', fill=True)
        pdf.set_font("Arial", '', 11)
        pdf.cell(135, 8, value, border=0, ln=1, align='L', fill=True)  # Fixed width
        pdf.set_font("Arial", 'B', 11)


    pdf.ln(6)


    #Watermark
    pdf.set_text_color(225, 225, 225)
    pdf.set_font("Arial", 'B', 50)
    pdf.set_xy(30, 110)
    pdf.cell(150, 20, customer['invoice_type'].upper(), 0, 0, 'C')

    # Status
    pdf.set_text_color(255, 0, 0)
    pdf.set_font("Arial", 'B', 18)
    pdf.set_xy(160, 10)
    pdf.cell(30, 10, customer['status'].upper(), 0, 1)

    #Footer with logo and company info
    pdf.set_y(-30)

    #logo
    if os.path.exists("Dummy_logo.png"):
        pdf.image("Dummy_logo.png", x=10, y=pdf.get_y()+2, w=15)

    #footer text
    pdf.set_y(pdf.get_y() + 2)  # slight padding
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(0)
    pdf.cell(0, 10, "Company XYZ | Company Address | Phone: +92 3456789012", ln=1, align='C')


    pdf.output(file_path)
    return file_path