-- CREATE DATABASE invoice_system;
-- USE invoice_system;

CREATE TABLE invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    phone_number VARCHAR(20),
    address TEXT,
    date DATE,
    invoice_number VARCHAR(50),
    invoice_type ENUM('INVOICE', 'QUOTATION'),
    status ENUM('PAID', 'UNPAID'),
    subtotal DECIMAL(10,2),
    discount DECIMAL(10,2),
    tax DECIMAL(10,2),
    gross_amount DECIMAL(10,2),
    notes TEXT,
    pdf_path VARCHAR(255)
);

CREATE TABLE invoice_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    description TEXT,
    quantity INT,
    unit_price DECIMAL(10,2),
    total DECIMAL(10,2),
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id)
);
