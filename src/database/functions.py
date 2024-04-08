import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import json
import logging


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



    