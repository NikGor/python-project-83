from datetime import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import validators


def normalize_url(url):
    result = urlparse(url)
    new_result = result._replace(path='', params='', query='', fragment='')
    return new_result.geturl()


def is_valid(url):
    if not url:
        return False
    if len(url) > 255:
        return False
    return validators.url(url)


def check_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.status_code
    except Exception:
        raise Exception('Ошибка при проверке сайта')


def analyze_url(url):
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
    except requests.exceptions.RequestException as e:
        raise Exception(f'Ошибка при проверке сайта: {e}')


def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')
