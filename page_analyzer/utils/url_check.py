import requests
from bs4 import BeautifulSoup


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
