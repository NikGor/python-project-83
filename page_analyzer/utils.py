from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup
from datetime import datetime


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


def check_website(url):
    """
    Функция проверяет статус-код сайта.

    >>> check_website('https://httpstat.us/200')
    200
    >>> check_website('https://httpstat.us/503')
    503
    >>> check_website('https://httpstat.us/404')
    404
    >>> check_website('invalid url')
    Traceback (most recent call last):
        ...
    Exception: Ошибка при проверке сайта
    """
    try:
        response = requests.get(url)
        # response.raise_for_status()
        return response.status_code
    except Exception:
        raise Exception('Ошибка при проверке сайта')


def analyze_url(url):
    """
    Функция анализирует метаданные страницы.

    >>> analyze_url('https://www.example.com')
    {'title': 'Example Domain', 'h1': 'Example Domain', 'description': None}
    >>> analyze_url('not url')
    Traceback (most recent call last):
        ...
    Exception: Ошибка при проверке сайта
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title')
        h1 = soup.find('h1')
        description = soup.find('meta', attrs={'name': 'description'})
        return {'title': title.text if title else None,
                'h1': h1.text if h1 else None,
                'description': description['content']
                if description and 'content' in description.attrs else None}
    except Exception:
        raise Exception('Ошибка при проверке сайта')


def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')
