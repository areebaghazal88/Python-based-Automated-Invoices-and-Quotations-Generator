import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='your_password123',
        database='invoice_system'
    )








