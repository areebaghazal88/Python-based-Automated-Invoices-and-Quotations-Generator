import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from invoice_generator import generate_pdf, save_invoice_to_db 

class InvoiceGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        self.root.geometry("950x750")


        self.items = []

        # Modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#f5f5f5')
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9), background='#4a6baf', foreground='white')
        style.configure('TEntry', font=('Segoe UI', 9))
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))
        style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        style.map('TButton', background=[('active', '#3a5a9f')])

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=(20, 10))
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_header()
        self.create_info_section()
        self.create_items_section()
        self.create_summary_section()
        self.create_buttons()

    def create_header(self):
        header = ttk.Frame(self.main_frame)
        header.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header, text="AUTOMATED INVOICE AND QUOTATION GENERATOR", font=('Segoe UI', 16, 'bold'), foreground='#2a4b8d').pack()

    def create_info_section(self):
        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(fill=tk.X, pady=5)

        self.create_client_info(info_frame)
        self.create_invoice_meta(info_frame)

    def create_client_info(self, parent):
        client = ttk.LabelFrame(parent, text=" Client Information ", padding=10)
        client.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        fields = [
            ("Customer Name*", "customer_name"),
            ("Phone Number*", "phone"),
            ("Address*", "address"),
            ("Email", "email"),
        ]

        for i, (label, attr) in enumerate(fields):
            ttk.Label(client, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(client, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            setattr(self, attr, entry)

    def create_invoice_meta(self, parent):
        meta = ttk.LabelFrame(parent, text=" Invoice Details ", padding=10)
        meta.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        meta_fields = [
            ("Invoice Number*", "invoice_number"),
            ("Date", "date", datetime.today().strftime("%Y-%m-%d")),
            ("Invoice Type", "invoice_type", ["INVOICE", "QUOTATION"]),
            ("Status", "status", ["PAID", "UNPAID"]),
        ]

        for i, (label, attr, *rest) in enumerate(meta_fields):
            ttk.Label(meta, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            if rest and isinstance(rest[0], list):
                combo = ttk.Combobox(meta, values=rest[0], state="readonly", width=27)
                combo.grid(row=i, column=1, padx=5, pady=2)
                combo.current(0)
                setattr(self, attr, combo)
            else:
                entry = ttk.Entry(meta, width=30)
                entry.grid(row=i, column=1, padx=5, pady=2)
                if rest:
                    entry.insert(0, rest[0])
                setattr(self, attr, entry)

    def create_items_section(self):
        items_frame = ttk.LabelFrame(self.main_frame, text=" Invoice Items ", padding=10)
        items_frame.pack(fill=tk.X, pady=10)  # Use fill=tk.X instead of BOTH

        # Set fixed height for the treeview (for example, 200 pixels)
        tree_height = 8  # This controls the number of visible rows

        self.tree = ttk.Treeview(items_frame, columns=('desc', 'qty', 'price', 'total'), show='headings', height=tree_height)
        self.tree.heading('desc', text='Description')
        self.tree.heading('qty', text='Qty')
        self.tree.heading('price', text='Unit Price')
        self.tree.heading('total', text='Total')
        self.tree.column('desc', width=300)
        self.tree.column('qty', width=80, anchor=tk.CENTER)
        self.tree.column('price', width=120, anchor=tk.E)
        self.tree.column('total', width=120, anchor=tk.E)
        self.tree.pack(fill=tk.X)

        # Optional: Add vertical scrollbar to the treeview
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.setup_tree_context_menu()

        controls = ttk.Frame(items_frame)
        controls.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(controls, text="Description:").pack(side=tk.LEFT, padx=2)
        self.item_desc = ttk.Entry(controls, width=30)
        self.item_desc.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls, text="Qty:").pack(side=tk.LEFT, padx=2)
        self.item_qty = ttk.Spinbox(controls, from_=1, to=999, width=5)
        self.item_qty.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls, text="Unit Price:").pack(side=tk.LEFT, padx=2)
        self.item_price = ttk.Entry(controls, width=10)
        self.item_price.pack(side=tk.LEFT, padx=5)

        ttk.Button(controls, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=10)


    def setup_tree_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Delete Item", command=self.delete_selected_item)

        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected[0])
            del self.items[index]
            self.tree.delete(selected[0])
            self.update_totals()

    def add_item(self):
        desc = self.item_desc.get().strip()
        qty = self.item_qty.get().strip()
        price = self.item_price.get().strip()

        if not desc or not qty or not price:
            messagebox.showwarning("Missing Info", "Please fill all item fields.")
            return

        try:
            qty = int(qty)
            price = float(price)
            total = qty * price
            item = {"desc": desc, "qty": qty, "unit_price": price, "total": total}
            self.items.append(item)
            self.tree.insert('', 'end', values=(desc, qty, f"Rs {price:.2f}", f"Rs {total:.2f}"))
            self.update_totals()
            self.item_desc.delete(0, tk.END)
            self.item_qty.delete(0, tk.END)
            self.item_price.delete(0, tk.END)
            self.item_desc.focus()
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be an integer and Price must be a number.")

    def create_summary_section(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(5, 10))

        ttk.Label(frame, text="Notes:").pack(side=tk.LEFT, padx=5)
        self.notes = ttk.Entry(frame, width=60)
        self.notes.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        calc = ttk.Frame(frame)
        calc.pack(side=tk.RIGHT)

        self.discount, self.tax, self.subtotal_var, self.total_var = self._create_summary_labels(calc)

    def _create_summary_labels(self, parent):
        discount = ttk.Entry(parent, width=10)
        discount.insert(0, "0")
        tax = ttk.Entry(parent, width=10)
        tax.insert(0, "0")
        subtotal_var = tk.StringVar(value="Rs 0.00")
        total_var = tk.StringVar(value="Rs 0.00")

        ttk.Label(parent, text="Discount:").grid(row=0, column=0)
        discount.grid(row=0, column=1, padx=5)
        ttk.Label(parent, text="Tax:").grid(row=0, column=2)
        tax.grid(row=0, column=3, padx=5)
        ttk.Label(parent, text="Subtotal:").grid(row=0, column=4)
        ttk.Label(parent, textvariable=subtotal_var, font=('Segoe UI', 9, 'bold')).grid(row=0, column=5, padx=5)
        ttk.Label(parent, text="Total:").grid(row=0, column=6)
        ttk.Label(parent, textvariable=total_var, font=('Segoe UI', 9, 'bold')).grid(row=0, column=7, padx=5)

        return discount, tax, subtotal_var, total_var

    def update_totals(self):
        subtotal = sum(item['total'] for item in self.items)
        try:
            discount = float(self.discount.get())
            tax = float(self.tax.get())
        except ValueError:
            discount = 0
            tax = 0

        total = (subtotal - discount) * (1 + tax / 100)
        self.subtotal_var.set(f"Rs {subtotal:.2f}")
        self.total_var.set(f"Rs {total:.2f}")

    def create_buttons(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(btn_frame, text="Generate Invoice", command=self.generate_invoice).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.RIGHT)

    def generate_invoice(self):
        # Collect client info
        customer = self.customer_name.get().strip()
        phone = self.phone.get().strip()
        address = self.address.get().strip()
        email = self.email.get().strip()

        if not customer or not phone or not address:
            messagebox.showerror("Missing Info", "Customer name, phone, and address are required.")
            return

        # Collect invoice details
        invoice_number = self.invoice_number.get().strip()
        date = self.date.get().strip()
        invoice_type = self.invoice_type.get().strip()
        status = self.status.get().strip()

        if not invoice_number:
            messagebox.showerror("Missing Info", "Invoice number is required.")
            return

        if not self.items:
            messagebox.showerror("No Items", "Please add at least one item to the invoice.")
            return

        # Summary calculations
        try:
            discount = float(self.discount.get())
            tax = float(self.tax.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Discount and tax must be numeric.")
            return

        subtotal = sum(item['total'] for item in self.items)
        total = (subtotal - discount) * (1 + tax / 100)

        # Notes
        notes = self.notes.get().strip()

        # Flattened customer data for function calls
        customer_data = {
            "name": customer,
            "phone": phone,
            "address": address,
            "email": email,
            "invoice_number": invoice_number,
            "date": date,
            "invoice_type": invoice_type,
            "status": status
        }

        try:
            # Generate PDF and save invoice
            pdf_path = generate_pdf(
                customer=customer_data,
                items=self.items,
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                gross=total,
                notes=notes
            )

            save_invoice_to_db(
                customer=customer_data,
                items=self.items,
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                gross=total,
                notes=notes,
                pdf_path=pdf_path
            )

            messagebox.showinfo("Success", f"Invoice generated successfully:\n{pdf_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the invoice:\n{str(e)}")

    def clear_all(self):
        for attr in ['customer_name', 'phone', 'address', 'email', 'invoice_number', 'date']:
            getattr(self, attr).delete(0, tk.END)
        for cb in ['invoice_type', 'status']:
            getattr(self, cb).current(0)
        self.notes.delete(0, tk.END)
        self.discount.delete(0, tk.END)
        self.tax.delete(0, tk.END)
        self.discount.insert(0, "0")
        self.tax.insert(0, "0")
        self.tree.delete(*self.tree.get_children())
        self.items.clear()
        self.update_totals()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceGenerator(root)
    root.mainloop()