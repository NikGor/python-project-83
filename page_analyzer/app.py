import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for, request
from datetime import datetime
from page_analyzer.models.url import Url
from page_analyzer.models.url_check import UrlCheck
from page_analyzer.utils import is_valid, \
    analyze_url, check_website, normalize_url, get_current_date

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/urls')
def urls():
    data = Url.get_all()
    return render_template('urls.html', data=data)


@app.route('/urls/<int:url_id>')
def url(url_id):
    url_obj = Url(url_id).get()
    url_checks = UrlCheck.get_by_url_id(url_id)
    return render_template('url.html', url=url_obj, url_checks=url_checks)


@app.route('/url/<int:id>/checks', methods=['POST'])
def url_checks(id):
    url_obj = Url(id).get()
    try:
        status_code = check_website(url_obj.name)
        analysis = analyze_url(url_obj.name)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url', url_id=id))
    UrlCheck.create(
        url_id=id,
        status_code=status_code,
        created_at=datetime.now().strftime('%Y-%m-%d'),
        title=analysis['title'],
        h1=analysis['h1'],
        description=analysis['description']
    )
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url', url_id=id))


if __name__ == '__main__':
    app.run(debug=True)
