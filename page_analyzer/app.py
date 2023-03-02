import os
import psycopg2
from flask import Flask, render_template, flash, redirect, url_for, request
from datetime import datetime
from page_analyzer.sql_utils import insert_data, get_data
from page_analyzer.utils import is_valid, \
    analyze_url, check_website, normalize_url
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if is_valid(url):
            normalized_url = normalize_url(url)
            created_at = datetime.now().strftime('%Y-%m-%d')
            if not get_data('urls', column_name='name', value=normalized_url):
                insert_data('urls',
                            name=normalized_url,
                            created_at=created_at)
                flash('Страница успешно добавлена', 'success')
                id = get_data('urls', column_name='id')[0][0]
                return redirect(url_for('url', url_id=id))
            else:
                flash('Страница уже существует', 'warning')
                id = get_data('urls', column_name='name',
                              value=normalized_url)[0][0]
                return redirect(url_for('url', url_id=id))
        flash('Некорректный URL!', 'danger')
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/urls')
def urls():
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
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
            data = cursor.fetchall()
    return render_template('urls.html', data=data)


@app.route('/urls/<int:url_id>')
def url(url_id):
    url = get_data('urls',
                   column_name='id',
                   value=url_id,
                   limit=1)
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM url_checks "\
                    "WHERE url_id = %s ORDER BY id DESC"
            cursor.execute(query, (url_id,))
            url_checks = cursor.fetchall()
    return render_template('url.html', url=url, url_checks=url_checks)


@app.route('/url/<id>/checks', methods=['POST'])
def url_checks(id):
    url = get_data('urls',
                   column_name='id',
                   value=id,
                   limit=1)[1]
    try:
        status_code = check_website(url)
        analysis = analyze_url(url)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url', url_id=id))
    insert_data('url_checks',
                url_id=id,
                status_code=status_code,
                created_at=datetime.now().strftime('%Y-%m-%d'),
                title=analysis['title'],
                h1=analysis['h1'],
                description=analysis['description'])
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url', url_id=id))


if __name__ == '__main__':
    app.run(debug=True)
