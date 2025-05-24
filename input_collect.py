from datetime import datetime

def get_invoice_data():
    customer = {}
    customer['name'] = input("Customer Name: ")
    customer['phone'] = input("Phone Number: ")
    customer['address'] = input("Address: ")
    customer['date'] = input("Date (YYYY-MM-DD): ")
    customer['invoice_number'] = input("Invoice/Quotation Number: ")
    customer['invoice_type'] = input("Type (INVOICE/QUOTATION): ")
    customer['status'] = input("Status (PAID/UNPAID): ")
    
    items = []
    while True:
        desc = input("Item Description: ")
        qty = int(input("Quantity: "))
        unit_price = float(input("Unit Price: "))
        total = qty * unit_price
        items.append({'desc': desc, 'qty': qty, 'unit_price': unit_price, 'total': total})
        more = input("Add another item? (y/n): ")
        if more.lower() != 'y':
            break

    subtotal = sum(item['total'] for item in items)
    discount = float(input("Discount (flat): "))
    tax = float(input("Tax amount: "))
    gross = subtotal + tax - discount
    notes = input("Notes: ")

    return customer, items, subtotal, discount, tax, gross, notes

# from datetime import datetime

# def get_valid_input(prompt, validation_func, error_msg):
#     while True:
#         value = input(prompt).strip()
#         if not value:
#             print("This field is required. Please enter a value.")
#             continue
#         try:
#             return validation_func(value)
#         except Exception:
#             print(error_msg)

# def get_invoice_data():
#     customer = {}

#     customer['name'] = get_valid_input("Customer Name: ", str, "Invalid name.")
#     customer['phone'] = get_valid_input("Phone Number: ", str, "Invalid phone number.")
#     customer['address'] = get_valid_input("Address: ", str, "Invalid address.")
#     customer['date'] = get_valid_input(
#         "Date (YYYY-MM-DD): ", 
#         lambda x: datetime.strptime(x, "%Y-%m-%d").date(), 
#         "Invalid date format. Please use YYYY-MM-DD."
#     )
#     customer['invoice_number'] = get_valid_input("Invoice/Quotation Number: ", str, "Invalid number.")
    
#     customer['invoice_type'] = get_valid_input(
#         "Type (INVOICE/QUOTATION): ", 
#         lambda x: x.upper() if x.upper() in ['INVOICE', 'QUOTATION'] else 1/0, 
#         "Must be 'INVOICE' or 'QUOTATION'."
#     )
#     customer['status'] = get_valid_input(
#         "Status (PAID/UNPAID): ", 
#         lambda x: x.upper() if x.upper() in ['PAID', 'UNPAID'] else 1/0, 
#         "Must be 'PAID' or 'UNPAID'."
#     )

#     items = []
#     while True:
#         desc = get_valid_input("Item Description: ", str, "Invalid description.")
#         qty = get_valid_input("Quantity: ", lambda x: int(x), "Quantity must be a number.")
#         unit_price = get_valid_input("Unit Price: ", lambda x: float(x), "Unit Price must be a number.")
#         total = qty * unit_price
#         items.append({'desc': desc, 'qty': qty, 'unit_price': unit_price, 'total': total})
        
#         more = input("Add another item? (y/n): ").strip().lower()
#         if more != 'y':
#             break

#     subtotal = sum(item['total'] for item in items)
#     discount = get_valid_input("Discount (flat): ", lambda x: float(x), "Discount must be a number.")
#     tax = get_valid_input("Tax amount: ", lambda x: float(x), "Tax must be a number.")
#     gross = subtotal + tax - discount
#     notes = input("Notes: ").strip()

#     return customer, items, subtotal, discount, tax, gross, notes

