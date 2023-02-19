from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


class URLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL(message='Invalid URL')])
    submit = SubmitField('CHECK')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.url.data
        try:
            response = requests.get(url)
            if response.status_code == 200:
                flash('Site is reachable', category='success')
            else:
                flash(f'Site returned status code {response.status_code}', category='danger')
        except:
            flash('Could not reach site', category='danger')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
