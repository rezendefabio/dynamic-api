# test_connection.py
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:25076600@localhost:5432/dynamicapi"

engine = create_engine(DATABASE_URL)
connection = engine.connect()
print("Conexão bem-sucedida!")
connection.close()