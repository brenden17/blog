import os
import sys

from models import Post

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template

app = Flask(__name__.split('.')[0])


@app.route('/')
@app.route('/index')
def index():
    """ Return hello template at application root URL."""
    return render_template('index.html')



@app.route('/posts')
def list_posts():
    posts = Post.all()
    return render_template('list_posts.html', posts=posts)
