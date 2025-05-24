from invoice_generator import generate_pdf, save_invoice_to_db
from input_collect import get_invoice_data  # From Step 3B

def main():
    customer, items, subtotal, discount, tax, gross, notes = get_invoice_data()
    pdf_path = generate_pdf(customer, items, subtotal, discount, tax, gross, notes)
    save_invoice_to_db(customer, items, subtotal, discount, tax, gross, notes, pdf_path)
    print(f"Invoice saved to {pdf_path} and recorded in database.")

if __name__ == "__main__":
    main()

