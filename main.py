import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import redirect, url_for

import markdown
from models import Post

app = Flask(__name__.split('.')[0])


@app.route('/')
@app.route('/index')
def index():
    """ Return hello template at application root URL."""
    return render_template('index.html')

@app.route('/blog')
def post():
    return render_template('post.html')

@app.route('/create-blog', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        contents = request.form['contents']
        tags = request.form['tags']
        return return redirect(url_for('post'))

    return render_template('create_post.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
