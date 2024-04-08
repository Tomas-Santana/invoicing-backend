import json
import sqlalchemy

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import *

# psycopg2
# connect to a pgsql database
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect("dbname=facturas user=postgres password=123456789")
cur = conn.cursor(cursor_factory=RealDictCursor)

# select all the products
cur.execute("SELECT * FROM producto")

# turn the result into a list of dictionaries
result = cur.fetchall()

print(result)





# #connect to a pgsql database

# engine = create_engine('postgresql+psycopg2://postgres:123456789@localhost:5432/facturas')

# Session = sessionmaker(bind=engine)

# session = Session()

# # select all the products
# stmt = select(Producto).where(Producto.de.like('%TE%'))

# # execute the statement

# result = session.execute(stmt)

# # iterate over the result
# for row in result:
#     print(row)

