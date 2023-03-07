from urllib.parse import urlparse
import validators


def normalize_url(url):
    """
    Функция принимает строку URL и возвращает
    отформатированный URL без дублирования слешей и других лишних символов.

    >>> normalize_url('https://www.example.com/')
    'https://www.example.com'
    >>> normalize_url('http://www.example.com/path/?key=value')
    'http://www.example.com'
    """
    result = urlparse(url)
    new_result = result._replace(path='', params='', query='', fragment='')
    return new_result.geturl()


def is_valid(url):
    """
    Функция проверяет, является ли строка URL допустимой.

    >>> is_valid('https://www.example.com')
    True
    >>> is_valid('invalid url')
    False
    >>> is_valid(None)
    False
    >>> is_valid('https://' + 'a' * 243 + '.com')
    True
    >>> is_valid('https://' + 'a' * 244 + '.com')
    False
    >>> is_valid('httpsss://abcabca@test.ru')
    False
    """

    if url is None:
        return False
    if len(url) > 255:
        return False
    if url.startswith('http://') or url.startswith('https://'):
        return validators.url(url)
    else:
        return False
