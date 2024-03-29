import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for, request
from datetime import datetime
from page_analyzer.models.url_check import UrlCheck
from page_analyzer.utils.date import get_current_date
from page_analyzer.models.url import Url
from page_analyzer.utils.url_check import (check_status, analyze_url,
                                           check_load_time, check_semantic_tags,
                                           check_robots_and_sitemap,
                                           check_links_on_page,
                                           check_alt_texts)
from page_analyzer.utils.url import is_valid, normalize_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'GET':
        data = Url.get_all()
        return render_template('urls.html', data=data)
    elif request.method == 'POST':
        url = request.form.get('url')
        if is_valid(url):
            normalized_url = normalize_url(url)
            created_at = get_current_date()
            existing_url = Url.get_by_name(normalized_url)
            if not existing_url:
                url_obj = Url.create(normalized_url, created_at)
                flash('Страница успешно добавлена', 'success')
            else:
                url_obj = existing_url
                flash('Страница уже существует', 'warning')
            return redirect(url_for('url', url_id=url_obj.id))
        flash('Некорректный URL!', 'danger')
        return render_template('index.html', input_url=url), 422


@app.route('/urls/<int:url_id>')
def url(url_id):
    url = Url(url_id).get()
    url_checks = UrlCheck.get_by_url_id(url_id)
    if not url:
        return render_template('404.html')
    return render_template('url.html', url=url, url_checks=url_checks)


@app.route('/url/<int:url_id>/checks', methods=['POST'])
def url_checks(url_id):
    url_instance = Url(url_id).get()
    if not url_instance:
        return render_template('404.html')

    url_name = url_instance.name

    try:
        status_code = check_status(url_name)
        analysis = analyze_url(url_name)
        load_time = check_load_time(url_name)
        semantic_tags = check_semantic_tags(url_name)
        robots_and_sitemap = check_robots_and_sitemap(url_name)
        links_statuses = check_links_on_page(url_name)
        alt_texts = check_alt_texts(url_name)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url', url_id=url_id))

    UrlCheck.create(
        url_id=url_id,
        status_code=status_code,
        created_at=datetime.now().strftime('%Y-%m-%d'),
        title=analysis.get('title'),
        h1=analysis.get('h1'),
        description=analysis.get('description'),
        load_time=load_time,
        semantic_tags=','.join(semantic_tags),
        robots_and_sitemap='\n '.join(robots_and_sitemap),
        links_statuses=','.join(links_statuses),
        alt_texts=','.join(alt_texts)
    )

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url', url_id=url_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
