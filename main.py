import logging

from flask import Flask
from flask import render_template
from flask import request
from flask import Markup

import markdown

from models import Post

app = Flask(__name__.split('.')[0])

def md2html(content):
    md = markdown.Markdown(extensions=['toc'])
    html_content = Markup(md.convert(content))
    toc = Markup(md.toc)
    return html_content, toc

def post(title=None, category=None):
    if title:
        post = Post.query(Post.title==title).get()
    else:
        post = Post.get_1lastest(category=category)

    pre_post = post.get_pre(category=category)
    next_post = post.get_next(category=category)
    content, toc = md2html(post.content)
    return render_template('post.html',
                           post=post,
                           category=category,
                           pre_post=pre_post,
                           next_post=next_post,
                           toc=toc,
                           content=content)

@app.route('/')
@app.route('/page/')
@app.route('/page/<title>')
def index(title=None):
    return post(title)

@app.route('/blog/')
@app.route('/blog/<title>')
def blog(title=None):
    return post(title, category='blog')

@app.route('/work/')
@app.route('/work/<title>')
def page(title=None):
    return post(title, category='work')

@app.route('/book/')
@app.route('/book/<title>')
def book(title=None):
    return post(title, category='book')

@app.route('/tags/<tag>')
def tags(tag):
    posts = Post.get_tagged_post(tag)
    return render_template('tags.html', posts=posts)

@app.route('/archives')
def archives():
    blogs = Post.get_lastest(count=999, category='blog')
    works = Post.get_lastest(count=999, category='work')
    books = Post.get_lastest(count=999, category='book')
    return render_template('archives.html',
                           blogs=blogs,
                           works=works,
                           books=books)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
