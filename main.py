import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import redirect, url_for, request
from flask import Markup

import markdown

from models import Post
from decorator import login_required, admin_required

app = Flask(__name__.split('.')[0])

@app.route('/')
def index():
    posts = Post.get_lastest(5)
    current_post = posts[0]
    rest_posts = posts[1:]
    return render_template('index.html',
                           current_post=current_post,
                           rest_posts=rest_posts)

@app.route('/blog/<int:post_id>')
def post(post_id):
    post = Post.get_by_id(post_id)
    pre = post.get_pre()
    next = post.get_next()
    content = Markup(markdown.markdown(post.content))
    return render_template('post.html', post=post,
                           pre=pre,
                           next=next,
                           content=content)

@app.route('/posts/<tag>')
def tags(tag):
    posts = Post.get_tagged_post(tag)
    return render_template('posts.html', posts=posts)

@admin_required
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

@app.route('/archives')
def archives():
    return render_template('archives.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
