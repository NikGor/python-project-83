import requests
from bs4 import BeautifulSoup
import time


def check_status(url):
    """
    Функция проверяет статус-код сайта.

    >>> check_status('https://httpstat.us/200')
    200
    >>> check_status('https://httpstat.us/503')
    503
    >>> check_status('https://httpstat.us/404')
    404
    >>> check_status('invalid url')
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


def check_load_time(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        if response.status_code == 200:
            return round(end_time - start_time, 2)
        else:
            raise Exception("Ошибка при получении ответа от сайта")
    except Exception:
        raise Exception('Ошибка при проверке времени загрузки сайта')


def check_semantic_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = ['header', 'footer', 'nav',
                'main', 'article', 'section',
                'aside', 'details', 'figcaption',
                'figure', 'summary']
        present_tags = [tag for tag in tags if soup.find(tag)]
        return present_tags
    except Exception:
        raise Exception('Ошибка при проверке семантических тегов')


def check_robots_and_sitemap(url):
    # Проверка robots.txt
    results = []
    robots_url = f"{url}/robots.txt"
    response_robots = requests.get(robots_url)
    if response_robots.status_code == 200:
        results.append("robots.txt exists")
    else:
        results.append("robots.txt does not exist")

    # Проверка sitemap.xml
    sitemap_url = f"{url}/sitemap.xml"
    response_sitemap = requests.get(sitemap_url)
    if response_sitemap.status_code == 200:
        results.append("sitemap.xml exists")
    else:
        results.append("sitemap.xml does not exist")

    return results


def check_meta_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tags = {
            'title': soup.title.string if soup.title else None,
            'description': soup.find('meta',
                                     attrs={'name': 'description'}).get('content')
            if soup.find('meta', attrs={
                'name': 'description'}) else None,
            'keywords': soup.find('meta', attrs={'name': 'keywords'}).get('content')
            if soup.find('meta', attrs={
                'name': 'keywords'}) else None
        }
        return meta_tags
    except Exception:
        raise Exception('Ошибка при проверке мета-тегов')


def check_links_on_page(url):
    broken_links = []
    error_links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.startswith('/'):
            href = url + href
        try:
            r = requests.head(href)
            if r.status_code == 404:
                broken_links.append(href)
        except:
            error_links.append(href)

    # Преобразование списков в строки для последующего сохранения в базе данных
    return broken_links + error_links


def check_alt_texts(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img')
        alt_texts = [img.get('alt', '') for img in images]
        return alt_texts
    except Exception:
        raise Exception('Ошибка при проверке альтернативных текстов для изображений')


def seo_score(url):
    checks = [
        check_load_time,
        check_semantic_tags,
        check_robots_and_sitemap,
        check_meta_tags,
        check_links_on_page,
        check_alt_texts,
    ]

    passed_checks = 0
    for check in checks:
        try:
            result = check(url)
            if result:
                passed_checks += 1
        except Exception:
            continue

    score = round((passed_checks / len(checks)) * 10)
    return score
