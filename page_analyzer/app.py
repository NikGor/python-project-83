import psycopg2
from flask import Flask, render_template, flash, redirect, url_for, request
from datetime import datetime

from page_analyzer.utils import is_valid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
DATABASE_URL = "postgresql://niko:123456@localhost:5432/page_analyzer_test"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if is_valid(url):
            with psycopg2.connect(dsn=DATABASE_URL) as conn:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO urls (name, created_at) '
                                   'VALUES (%s, %s)', (url, now))
                    conn.commit()
                    cursor.execute('SELECT * FROM urls '
                                   'ORDER BY created_at '
                                   'DESC LIMIT 1')
                    url = cursor.fetchone()
            flash('URL submitted successfully!', 'success')
            return redirect(url_for('url', url_id=url[0]))
        else:
            flash('Invalid URL!', 'danger')
            return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/urls')
def urls():
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM urls '
                           'ORDER BY created_at DESC')
            urls = cursor.fetchall()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def url(url_id):
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM urls '
                           'WHERE id = %s', (url_id,))
            url = cursor.fetchone()
            cursor.execute('SELECT * FROM url_checks '
                           'WHERE url_id = %s '
                           'ORDER BY created_at DESC', (url_id,))
            url_checks = cursor.fetchall()
    return render_template('url.html', url=url, url_checks=url_checks)


@app.route('/url/<id>/checks', methods=['POST'])
def url_checks(id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with psycopg2.connect(dsn=DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO url_checks (url_id, created_at) '
                           'VALUES (%s, %s)', (id, now))
            conn.commit()
            flash('URL checked!', 'success')
    return redirect(url_for('url', url_id=id))


if __name__ == '__main__':
    app.run(debug=True)
