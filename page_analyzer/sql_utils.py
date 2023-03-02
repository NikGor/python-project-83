from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')


def insert_data(table_name, **kwargs):
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            columns = ', '.join(kwargs.keys())
            values = ', '.join(['%s'] * len(kwargs))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(query, tuple(kwargs.values()))
            conn.commit()


def get_data(table_name, column_name=None, value=None, limit=None):
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            if column_name and value:
                query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
                cursor.execute(query, (value,))
            else:
                query = f"SELECT * FROM {table_name}"
                if column_name:
                    query += f" ORDER BY {column_name} DESC"
                if limit:
                    query += f" LIMIT {limit}"
                cursor.execute(query)
            if limit == 1:
                data = cursor.fetchone()
            else:
                data = cursor.fetchall()
            return data
