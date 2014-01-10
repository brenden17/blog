import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
from flask import Markup

import markdown
from models import Post

app = Flask(__name__.split('.')[0])


@app.route('/')
@app.route('/index')
def index():
    """ Return hello template at application root URL."""
    return render_template('index.html')

@app.route('/blog/<int:post_id>')
def post(post_id=None):
    post = Post.get_by_id(post_id)
    contents = Markup(markdown.markdown(post.contents))
    return render_template('post.html', post=post, contents=contents)

@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        category = request.form['category'] or 'b'
        title = request.form['title'] or 'No title'
        content = request.form['content'] or 'No Content'
        tags = request.form['tags']
        if tags:
            tags = map(lambda x: x.strip(), tags.split(','))
        else:
            tags = ['']
        post = Post(category=category,
                    title=title, content=content, tags=tags)
        post.put()
#         return redirect(url_for('/blog/', post_id=post.id))
        return redirect(url_for('/blog/%d' % post.id))

    return render_template('create_post.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
