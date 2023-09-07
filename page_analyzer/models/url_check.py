from page_analyzer.db import Database


class UrlCheck:
    def __init__(self, id, url_id,
                 status_code, created_at,
                 title, h1, description,
                 load_time=None, semantic_tags=None,
                 robots_and_sitemap=None, links_statuses=None,
                 alt_texts=None, custom_404=None):
        self.id = id
        self.url_id = url_id
        self.status_code = status_code
        self.created_at = created_at
        self.title = title
        self.h1 = h1
        self.description = description
        self.load_time = load_time
        self.semantic_tags = semantic_tags
        self.robots_and_sitemap = robots_and_sitemap
        self.links_statuses = links_statuses
        self.alt_texts = alt_texts
        self.custom_404 = custom_404

    @staticmethod
    def get_by_url_id(url_id):
        with Database() as cursor:
            query = """
                    SELECT * FROM url_checks
                    WHERE url_id = %s ORDER BY id DESC
                    """
            cursor.execute(query, (url_id,))
            rows = cursor.fetchall()
            return rows

    @staticmethod
    def create(url_id, status_code, created_at, title, h1, description,
               load_time=None, semantic_tags=None,
               robots_and_sitemap=None, links_statuses=None,
               alt_texts=None, custom_404=None):
        with Database() as cursor:
            query = """
                    INSERT INTO url_checks (
                                url_id, status_code,
                                created_at, title,
                                h1, description,
                                load_time, semantic_tags,
                                robots_and_sitemap, links_statuses,
                                alt_texts, custom_404
                                )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (url_id, status_code,
                                   created_at, title, h1,
                                   description, load_time,
                                   semantic_tags, robots_and_sitemap,
                                   links_statuses, alt_texts,
                                   custom_404))
