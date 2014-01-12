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
def index():
    posts = Post.get_lastest(5)
    current_post = posts[0]
    rest_posts = posts[1:]
    return render_template('index.html',
                           current_post=current_post,
                           rest_posts=rest_posts)
@app.route('/blog/')
@app.route('/blog/<int:post_id>')
def post(post_id=None):
    base_url = request.base_url
    if post_id:
        post = Post.get_by_id(post_id)
    else:
        post = Post.get_blastest()
    pre_post = post.get_bpre()
    next_post = post.get_bnext()
    content = Markup(markdown.markdown(post.content))
    return render_template('post.html', post=post,
                           pre_post=pre_post,
                           next_post=next_post,
                           content=content,
                           base_url=base_url)
@app.route('/page/')
@app.route('/page/<int:post_id>')
def page(post_id=None):
    base_url = request.base_url
    if post_id:
        post = Post.get_by_id(post_id)
    else:
        post = Post.get_alastest()
    pre_post = post.get_apre()
    next_post = post.get_anext()
    content = Markup(markdown.markdown(post.content))
    return render_template('page.html', post=post,
                           pre_post=pre_post,
                           next_post=next_post,
                           content=content,
                           base_url=base_url)

@app.route('/tags/<tag>')
def tags(tag):
    posts = Post.get_tagged_post(tag)
    return render_template('tags.html', posts=posts)

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
        return redirect(url_for('/blog/', post_id=post.key.id()))

    return render_template('create_post.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
