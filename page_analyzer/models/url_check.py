from page_analyzer.models.db import Database


class UrlCheck:
    def __init__(self, id, url_id,
                 status_code, created_at,
                 title, h1, description):
        self.id = id
        self.url_id = url_id
        self.status_code = status_code
        self.created_at = created_at
        self.title = title
        self.h1 = h1
        self.description = description

    def get_by_url_id(url_id):
        with Database() as cursor:
            query = """
                    SELECT * FROM url_checks
                    WHERE url_id = %s ORDER BY id DESC
                    """
            cursor.execute(query, (url_id,))
            rows = cursor.fetchall()
            return rows

    def create(url_id, status_code, created_at, title, h1, description):
        with Database() as cursor:
            query = """
                    INSERT INTO url_checks (
                                url_id, status_code,
                                created_at, title,
                                h1, description
                                )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (url_id, status_code,
                                   created_at, title, h1,
                                   description))
