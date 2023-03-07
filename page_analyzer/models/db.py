import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv()


class Database:
    DATABASE_URL = os.getenv('DATABASE_URL')

    def __init__(self):
        self.conn = psycopg2.connect(Database.DATABASE_URL)

    def __enter__(self):
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
