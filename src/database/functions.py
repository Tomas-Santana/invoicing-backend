import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import json
import logging
import datetime


conn = psycopg2.connect("dbname=facturas user=postgres password=123456789")


def search_product(param: str):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # query with query parameters
    cur.execute("SELECT * FROM product WHERE UPPER(name) LIKE %s", (f'%{param.upper()}%',))
    
    result = cur.fetchall()
    
    cur.close()
    
    return json.loads(json.dumps(result))

def general_search(table: str, field: str, value: str) -> list[dict]:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if (field == "name" and table == "client"):
        query = "SELECT * FROM client WHERE UPPER(CONCAT(name,' ' ,  surname)) LIKE %s"
        cur.execute(query, (f"%%{value.upper()}%%",))
    else:
        query = sql.SQL("SELECT * FROM {table} WHERE UPPER(CAST({field} AS VARCHAR)) LIKE %s").format(
            table=sql.Identifier(table),
            field=sql.Identifier(field),
        )
        cur.execute(query, (f"%%{value.upper()}%%",))
        
    logging.debug(cur.query)
    result = cur.fetchall()
    cur.close()
    return json.loads(json.dumps(result))

def create_client(name: str, surname: str, dir: str, pid: str, pid_prefix: str) -> dict:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # check if client already exists (pid_prefix + pid is unique)
    cur.execute("SELECT * FROM client WHERE pid = %s", (pid, ))
    
    result = cur.fetchone()
    
    response = {}
    
    if result is not None:
        # update client
        query = sql.SQL("UPDATE client SET name = %s, surname = %s, dir = %s WHERE pid = %s AND pid_prefix = %s RETURNING *")
        
        cur.execute(query, (name, surname, dir, pid, pid_prefix))
        
        response = {"action": "update", "client_id": result['id_client']}
    else:
        # insert new client
        query = sql.SQL("INSERT INTO client (name, surname, dir, pid, pid_prefix) VALUES (%s, %s, %s, %s, %s) RETURNING *")
        cur.execute(query, (name, surname, dir, pid, pid_prefix))
        
        response = {"action": "insert", "client_id": cur.fetchone()['id_client']}
    
    result = cur.fetchone()
    # TODO: add commit after testing
    # conn.commit()
    cur.close()
    
    return response


invoice = {
    "client": {
        "name": "Juan",
        "surname": "Perez",
        "pid_prefix": "E",
        "pid": "12345678",
        "dir": "La Virginia"
    },
    "products": [
        {
            "name": "TENEDOR",
            "code": "12345",
            "photourl": "https://www.google.com",
            "price": 2,
            "quantity": 2
        },
        {
            "name": "TAZA",
            "code": "09876",
            "photourl": "https://www.google.com",
            "price": 7,
            "quantity": 1
        }
    ],
    "payments": [
        {
            "method": "EFECTIVO",
            "amount": 10
        },
        {
            "method": "TARJETA DE CREDITO",
            "bank": "BNC",
            "amount": 1.1
        }
    ]
}

def get_method_id(method: str) -> int:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT id_method FROM payment_method WHERE name = %s", (method,))
    
    result = cur.fetchone()
    cur.close()
    
    return result['id_method']

def get_bank_id(bank: str) -> int:
    if (bank == ""):
        return None
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT id_bank FROM bank WHERE name = %s", (bank,))
    
    logging.debug(cur.query)
    
    result = cur.fetchone()
    cur.close()
    
    result_str = json.dumps(result, indent=4)
    logging.debug(bank + "\n" + result_str)
    
    if result is None:
        return None
    
    return result.get('id_bank', None)

def get_client_id(pid: str, pid_prefix: str) -> int:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT id_client FROM client WHERE pid = %s AND pid_prefix = %s", (pid, pid_prefix))
    
    result = cur.fetchone()
    cur.close()
    
    if result is None:
        return None
    
    return result['id_client']

def create_invoice(invoice: dict) -> dict:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    invoice_query = sql.SQL("INSERT INTO invoice (date, id_client) VALUES (%s, %s) RETURNING id_invoice")
    
    client_id = get_client_id(invoice['client']['pid'], invoice['client']['pid_prefix'])
    
    if client_id is None:
        client_op = create_client(invoice['client']['name'], invoice['client']['surname'], invoice['client']['dir'], invoice['client']['pid'], invoice['client']['pid_prefix'])
        
        client_id = client_op['client_id']
        
    cur.execute(invoice_query, (today, client_id))
    
    invoice_id = cur.fetchone()['id_invoice']
    print(invoice_id)
    
    # insert products (product_id, invoice_id, quantity) into invoice_product
    
    products_query = sql.SQL("INSERT INTO invoice_product (code_product, id_invoice, quantity) VALUES (%s, %s, %s)")
    
    for product in invoice['products']:
        cur.execute(products_query, (product['code'], invoice_id, product['quantity']))
    
    
    payments_query = sql.SQL("INSERT INTO payment (id_invoice, id_method, id_bank, amount) VALUES (%s, %s, %s, %s)")
    payments_query_no_bank = sql.SQL("INSERT INTO payment (id_invoice, id_method, amount) VALUES (%s, %s, %s)")
    
    for payment in invoice['payments']:
        method_id = get_method_id(payment['method'])
        
        bank = payment.get('bank', "N/A")
        bank_id = get_bank_id(bank)
        if bank_id is None:
            cur.execute(payments_query_no_bank, (invoice_id, method_id, payment['amount']))
        else:
            cur.execute(payments_query, (invoice_id, method_id, bank_id, payment['amount']))
    
    total_products = sum([product['price'] * product['quantity'] for product in invoice['products']])*1.1
    total_payments = sum([payment['amount'] for payment in invoice['payments']])
    
    if total_products != total_payments:
        conn.rollback()
        return {"message": "Invalid request"}
    
    cur.close()
    # conn.commit()
    print({"message": "Invoice created successfully", "invoice_id": invoice_id})
    return {"message": "Invoice created successfully", "invoice_id": invoice_id}

def get_invoice(invoice_id: int) -> dict:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = sql.SQL("SELECT * FROM invoice WHERE id_invoice = %s")
    cur.execute(query, (invoice_id,))
    
    result = cur.fetchone()
    
    # build the invoice object
    
    invoice = {
        "invoice_id": result['id_invoice'],
        "date": result['date'].strftime('%Y-%m-%d'),
        "client": {},
        "products": [],
        "payments": []
    }
    
    # get client info
    client_query = sql.SQL("SELECT * FROM client WHERE id_client = %s")
    cur.execute(client_query, (result['id_client'],))
    
    client = cur.fetchone()
    
    invoice['client'] = {
        "name": client['name'],
        "surname": client['surname'],
        "dir": client['dir'],
        "pid": client['pid'],
        "pid_prefix": client['pid_prefix']
    }
    
    # get products info
    products_query = sql.SQL("SELECT p.name, p.code, p.price, iv.quantity, p.photourl FROM invoice i join invoice_product iv using (id_invoice) join product p on iv.code_product=p.code WHERE id_invoice=%s")
    
    cur.execute(products_query, (invoice_id,))
    
    products = cur.fetchall()
    
    for product in products:
        invoice['products'].append({
            "name": product['name'],
            "code": product['code'],
            "price": product['price'],
            "quantity": product['quantity'],
            "photourl": product['photourl']
        })
    
    # get payments info
    payments_query = sql.SQL("SELECT pm.name as method, b.name as bank, p.amount FROM payment p join payment_method pm on p.id_method=pm.id_method left join bank b on p.id_bank=b.id_bank WHERE id_invoice=%s")
    
    cur.execute(payments_query, (invoice_id,))
    
    payments = cur.fetchall()
    
    for payment in payments:
        invoice['payments'].append({
            "method": payment['method'],
            "bank": payment['bank'] if payment['bank'] else "",
            "amount": payment['amount']
        })
    
    cur.close()
    
    return json.loads(json.dumps(invoice))

def search_invoice(field: str, value: str) -> list[dict]:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if (field == "invoice_id"):
        query = sql.SQL("""
            SELECT i.id_invoice as invoice_id, i.date, c.name, c.surname, c.pid_prefix, c.pid, sum(p.amount) as total, i.void 
            FROM invoice i 
            JOIN client c ON i.id_client = c.id_client
            JOIN payment p ON i.id_invoice = p.id_invoice
            WHERE i.id_invoice = %s
            GROUP BY i.id_invoice, c.name, c.surname, c.pid_prefix, c.pid, i.date
            """)
        
        cur.execute(query, (value,))
    elif (field == "name"):
        query = sql.SQL("""
            SELECT i.id_invoice as invoice_id, i.date, c.name, c.surname, c.pid_prefix, c.pid, sum(p.amount) as total, i.void
            FROM invoice i 
            JOIN client c ON i.id_client = c.id_client
            JOIN payment p ON i.id_invoice = p.id_invoice
            WHERE UPPER(CONCAT(c.name, ' ', c.surname)) LIKE %s
            GROUP BY i.id_invoice, c.name, c.surname, c.pid_prefix, c.pid, i.date
            """)
        cur.execute(query, (f"%%{value.upper()}%%",))
    elif (field == "pid"):
        query = sql.SQL("""
            SELECT i.id_invoice as invoice_id, i.date, c.name, c.surname, c.pid_prefix, c.pid, sum(p.amount) as total, i.void
            FROM invoice i 
            JOIN client c ON i.id_client = c.id_client
            JOIN payment p ON i.id_invoice = p.id_invoice
            WHERE c.pid = %s
            GROUP BY i.id_invoice, c.name, c.surname, c.pid_prefix, c.pid, i.date
            """)
        cur.execute(query, (value,))
    elif (field == "date"):
        query = sql.SQL("""
            SELECT i.id_invoice as invoice_id, i.date, c.name, c.surname, c.pid_prefix, c.pid, sum(p.amount) as total, i.void
            FROM invoice i  
            JOIN client c ON i.id_client = c.id_client
            JOIN payment p ON i.id_invoice = p.id_invoice
            WHERE i.date = %s
            GROUP BY i.id_invoice, c.name, c.surname, c.pid_prefix, c.pid, i.date
            """)
        cur.execute(query, (value,))
    
    result = cur.fetchall()
    cur.close()
    
    for r in result:
        r['date'] = r['date'].strftime('%Y-%m-%d')
    
    return json.loads(json.dumps(result)) 

def get_closing_statement(date: str):
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # get all invoices from the date
    invoices = search_invoice("date", date)
    
    # get the day total
    day_total = sum([invoice['total'] for invoice in invoices if not invoice['void']])
    
    
    # get how much was paid by each method
    query = sql.SQL("""
        SELECT pm.name as method, sum(p.amount) as total
        FROM payment p
        JOIN payment_method pm ON p.id_method = pm.id_method
        JOIN invoice i ON p.id_invoice = i.id_invoice
        WHERE i.date = %s AND i.void = FALSE
        GROUP BY pm.name
        """)
    cur.execute(query, (date,))
    methods = cur.fetchall()
    
    # get how much was paid by each bank
    
    query = sql.SQL("""
        SELECT b.name as bank, sum(p.amount) as total
        FROM payment p
        JOIN bank b ON p.id_bank = b.id_bank
        JOIN invoice i ON p.id_invoice = i.id_invoice
        WHERE i.date = %s AND i.void = FALSE
        GROUP BY b.name
    """)
    cur.execute(query, (date,))
    banks = cur.fetchall()
    
    # get how much was paid in cash
    query = sql.SQL("""
        SELECT sum(p.amount) as total
        FROM payment p
        JOIN payment_method pm ON p.id_method = pm.id_method
        JOIN invoice i ON p.id_invoice = i.id_invoice
        WHERE i.date = %s AND pm.name = 'EFECTIVO' AND i.void = FALSE
    """)
        
    cur.execute(query, (date,))
    cash = cur.fetchone()
    if cash['total'] is not None:
        banks.append({"bank": "EFECTIVO", "total": cash['total']})
    
    # get how many units of each product were sold
    query = sql.SQL("""
        SELECT p.name, sum(ip.quantity) as sold, sum(ip.quantity * p.price) as total
        FROM invoice_product ip
        JOIN product p ON ip.code_product = p.code
        JOIN invoice i ON ip.id_invoice = i.id_invoice
        WHERE i.date = %s AND i.void = FALSE
        GROUP BY p.name
    """)
    cur.execute(query, (date,))
    products = cur.fetchall()
    
    # build the closing statement
    closing_statement = {
        "date": date,
        "day_total": day_total,
        "methods": methods,
        "banks": banks,
        "products": products
    }
    
    cur.close()
    
    return json.loads(json.dumps(closing_statement))

    
    


    
    
    
    
    



    