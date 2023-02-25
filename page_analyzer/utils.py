from urllib.parse import urlparse


def is_valid(url):
    try:
        result = urlparse(url)
        if len(url) > 255:
            return False
        return all([result.scheme, result.netloc])
    except (ValueError, TypeError):
        return False
