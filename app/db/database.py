# import psycopg2 -> import for NON ORM CONNECTION
# from psycopg2.extras import RealDictCursor -> import for NON ORM CONNECTION
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

alchURL = os.getenv('DB_URL')
engine = create_engine(alchURL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def getDB():
    db = Session()
    try:
        yield db
    finally:
        db.close()


# use for NON ORM CONNECTION!
# def connect():
#     while True:
#         try:
#             conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Zeeshanh1!', cursor_factory=RealDictCursor) 
#             cursor = conn.cursor()
#             print("Database Connection was Succesfull")
#             return cursor, conn
#         except Exception as e:
#             print(f"DatabaseConnection Was Failed due to {e}")
