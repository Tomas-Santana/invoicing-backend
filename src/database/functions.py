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
        
        response = {"action": "update"}
    else:
        # insert new client
        query = sql.SQL("INSERT INTO client (name, surname, dir, pid, pid_prefix) VALUES (%s, %s, %s, %s, %s) RETURNING *")
        cur.execute(query, (name, surname, dir, pid, pid_prefix))
        
        response = {"action": "insert"}
    
    result = cur.fetchone()
    # TODO: add commit after testing
    # conn.commit()
    cur.close()
    
    return response

# export type Payment = {
#   method: string;
#   bank?: string;
#   amount: number;
# };

# export type ProductEntry = {
#   name: string;
#   code: string;
#   photourl: string;
#   price: number;
#   quantity: number;
# };

# export type Client = {
#   name: string;
#   surname: string;
#   pid_prefix: string;
#   pid: string;
#   dir: string;
# };

# export type Invoice = {
#   client: Client;
#   products: ProductEntry[];
#   payments: Payment[];
# };

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
    if (bank == "N/A"):
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

def create_invoice(invoice: dict) -> dict:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    invoice_query = sql.SQL("INSERT INTO invoice (date, id_client) VALUES (%s, %s) RETURNING id_invoice")
    
    cur.execute(invoice_query, (today, 1))
    
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
    print({"message": "Invoice created successfully", "invoice_id": invoice_id})
    return {"message": "Invoice created successfully", "invoice_id": invoice_id}



create_invoice(invoice)
    
    
    
    
    
    



    