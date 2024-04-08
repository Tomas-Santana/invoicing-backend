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
    return json.loads(json.dumps(result))



    