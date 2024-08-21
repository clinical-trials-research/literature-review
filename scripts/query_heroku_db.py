import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

with psycopg.connect(DATABASE_URL) as connection:
    with connection.cursor() as cursor:
        data = cursor.execute("SELECT * FROM Study")
        print(list(data))
