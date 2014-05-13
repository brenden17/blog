from flask import Flask
from flask import render_template
from flask import request
from flask import Markup

import markdown

from models import Post

app = Flask(__name__.split('.')[0])

def md2html(content):
    return Markup(markdown.markdown(content))

@app.route('/')
def index():
    post = Post.get_1lastest()
    content = md2html(post.content)
    return render_template('index.html',
                           post=post,
                           content=content)
    
def post(post_id=None, category=None):
    if post_id:
        post = Post.get_by_id(post_id)
    else:
        post = Post.get_1lastest(category=category)

    pre_post = post.get_pre(category=category)
    next_post = post.get_next(category=category)
    content = md2html(post.content)
    return render_template('post.html',
                           post=post,
                           pre_post=pre_post,
                           next_post=next_post,
                           content=content,
                           base_url=request.base_url)

@app.route('/blog/')
@app.route('/blog/<int:post_id>')
def blog(post_id=None):
    return post(post_id, category='blog')

@app.route('/page/')
@app.route('/page/<int:post_id>')
def page(post_id=None):
    return post(post_id, category='page')

@app.route('/book/')
@app.route('/book/<int:post_id>')
def book(post_id=None):
    return post(post_id, category='book')

@app.route('/tags/<tag>')
def tags(tag):
    posts = Post.get_tagged_post(tag)
    return render_template('tags.html', posts=posts)

@app.route('/archives')
def archives():
    blogs = Post.get_lastest(count=999, category='blog')
    pages = Post.get_lastest(count=999, category='page')
    books = Post.get_lastest(count=999, category='book')
    return render_template('archives.html',
                           blogs=blogs,
                           pages=pages,
                           books=books)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')