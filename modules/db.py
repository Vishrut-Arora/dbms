import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

def connect_to_db():
    cur = psycopg2.connect(
        database = "DBMS",
        user = "postgres",
        password = os.environ.get('PASSWORD'),
        host = "localhost"
    )
    return cur.cursor()