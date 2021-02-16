from flask import render_template

from packages import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='ABOUT SHOP!!!!', body='ABOUT OUR SHOP!!!')