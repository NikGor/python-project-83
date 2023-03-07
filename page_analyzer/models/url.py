from page_analyzer.db import Database


class Url:
    def __init__(self, id, name=None, created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at

    def get(self):
        with Database() as cursor:
            query = "SELECT * FROM urls WHERE id = %s LIMIT 1"
            cursor.execute(query, (self.id,))
            row = cursor.fetchone()
            if row:
                self.name = row[1]
                self.created_at = row[2]
                return self
            return None

    def get_by_name(name):
        with Database() as cursor:
            query = "SELECT * FROM urls WHERE name = %s LIMIT 1"
            cursor.execute(query, (name,))
            row = cursor.fetchone()
            if row:
                return Url(*row)
            return None

    def get_all():
        with Database() as cursor:
            query = """
                SELECT urls.id, urls.name,
                url_checks.created_at,
                url_checks.status_code
                FROM urls
                LEFT OUTER JOIN url_checks
                ON urls.id = url_checks.url_id
                AND url_checks.id = (
                    SELECT MAX(id)
                    FROM url_checks
                    WHERE url_checks.url_id = urls.id
                )
                ORDER BY urls.id DESC
                """
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    def create(name, created_at):
        with Database() as cursor:
            query = """
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id
                    """
            cursor.execute(query, (name, created_at))
            id = cursor.fetchone()[0]
            return Url(id, name, created_at)
