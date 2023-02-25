import psycopg2
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired
from datetime import datetime

from page_analyzer.utils import is_valid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
DATABASE_URL = "postgresql://niko:123456@localhost:5432/page_analyzer_test"


class URLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(),
                                         URL(message='Invalid URL')])
    submit = SubmitField('CHECK')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()

    url = form.url.data
    if is_valid(url):
        # Записываем URL в базу данных
        conn = psycopg2.connect(dsn=DATABASE_URL)
        c = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO urls (name, created_at) '
                  'VALUES (%s, %s)', (url, now))
        conn.commit()
        conn.close()
        flash('URL submitted successfully!', 'success')
    else:
        flash('Invalid URL!', 'danger')
    redirect(url_for('index'))
    return render_template('index.html', form=form)


@app.route('/urls')
def urls():
    conn = psycopg2.connect(dsn=DATABASE_URL)
    c = conn.cursor()
    c.execute('SELECT * FROM urls ORDER BY created_at DESC')
    urls = c.fetchall()
    conn.close()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def url(url_id):
    conn = psycopg2.connect(dsn=DATABASE_URL)
    c = conn.cursor()
    c.execute('SELECT * FROM urls WHERE id = %s', (url_id, ))
    url = c.fetchone()  # Fetch only one row
    conn.close()
    return render_template('url.html', url=url)


if __name__ == '__main__':
    app.run(debug=True)
