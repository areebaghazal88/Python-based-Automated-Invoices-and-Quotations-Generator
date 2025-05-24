import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='areeba_126356',
        database='invoice_system'
    )








