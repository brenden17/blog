import logging
import re
import json

from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, Response
from flask import Markup
from flask import Blueprint
from flask import jsonify

from jinja2 import Template

import markdown

from models import Post, Entity

app = Flask(__name__.split('.')[0])

def noTag(text, tag):
    pattern = r"(<\s*%s\s*.*?>)|(<\s*/%s\s*>)" % (tag, tag)
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    tagless = pat.sub('', text)
    return tagless
  
def md2html(content):
    md = markdown.Markdown(extensions=['toc', 'def_list','abbr', 'tables', 'smart_strong', 'fenced_code', 'footnotes'])
    html_content = Markup(md.convert(content))
    toc = Markup(md.toc)
    return html_content, toc

def post(title=None, category=None):
    if title:
        post = Post.query(Post.title==title).get()
    else:
        post = Post.get_1lastest(category=category)

    if not post:
        return redirect(url_for("notfound", title=title))
		
    pre_post = post.get_pre(category=category)
    next_post = post.get_next(category=category)
    content, toc = md2html(post.content)

    last_posts = Post.get_lastest()
    
    txt = noTag(noTag(toc, 'div'), 'ul')
    toc = toc if txt.strip() else ''

    return render_template('post.html',
                           post=post,
                           last_posts=last_posts,
                           category=category,
                           pre_post=pre_post,
                           next_post=next_post,
                           toc=toc,
                           content=content)

@app.route('/pages')
def pages():
    posts = [p.get_json() for p in Post.query().order(-Post.date)]
    # return jsonify(posts)
    return Response(json.dumps(posts), mimetype='application/json')

@app.route('/')
@app.route('/page/')
@app.route('/page/<title>')
def index(title=None):
    return post(title)

@app.route('/<noun>/')
def entity(noun=None):
    entity = Entity.query(Entity.name==noun).get()
    post = Post.query(Post.title==noun).get()
    if not post:
        return redirect(url_for("idonotknow", noun=noun))
    
    posts = Post.query().filter(Post.category.IN([noun])).order(-Post.date)
    content, toc = md2html(post.content)
    
    txt = noTag(noTag(toc, 'div'), 'ul')
    toc = toc if txt.strip() else ''

    last_posts = Post.get_lastest()
    return render_template('entity.html',
                           entity=entity,
                           post=post,
                           posts=posts,
                           last_posts=last_posts,
                           toc=toc,
                           content=content)

@app.route('/<noun>/<verb>')
def verb(noun=None, verb=None):
    return post(verb, category=noun)

@app.route('/idonotknow/<noun>')
def idonotknow(noun):
    posts = Post.query().filter(Post.category.IN([noun])).order(-Post.date)
    tagged_posts = Post.get_tagged_post(noun)
    last_posts = Post.get_lastest()
    return render_template('idonotknow.html',
                           noun=noun,
                           posts=posts,
                           last_posts=last_posts,
                           tagged_posts=tagged_posts)

@app.route('/archives')
def archives():
    entities = Entity.query().order(Entity.name)
    last_posts = Post.get_lastest()
    return render_template('archives.html',
                           last_posts=last_posts,
                           entities=entities)

@app.route('/history')
def hisotry():
    posts = Post.query().order(-Post.date)
    last_posts = Post.get_lastest()
    return render_template('archives-history.html',
                           last_posts=last_posts,
                           posts=posts)

@app.route('/network')
def network():
    entities = Entity.query().order(Entity.name)
    result = list()
    for e in entities:
        result.extend(e.get_json())
    last_posts = Post.get_lastest()
    return render_template('network.html',
                           last_posts=last_posts,
                           result=result)
    
@app.route('/about')
def about():
    last_posts = Post.get_lastest()
    return render_template('about.html',last_posts=last_posts)

@app.route('/admin')
def admin():
    last_posts = Post.get_lastest()
    return render_template('admin.html',last_posts=last_posts)

@app.route('/notfound/<title>')
def notfound(title=None):
    last_posts = Post.get_lastest()
    return render_template('notfound.html', suggest=title,
                                            last_posts=last_posts)

@app.route('/test')
def test():
    return render_template('test.html')

### Flask extension

class Graph(object):
    def __init__(self, data,
                       chart="line",
                       width=400,
                       height=350,
                       x='Word',
                       y='Awesomeness'):
        self.data = data
        self.chart = chart
        self.width = width
        self.height = height
        self.x = x
        self.y = y
    
    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)
    
    @property
    def html(self):
        return Markup(
            self.render('graph.html', graph=self)
        )

def graph(*args, **kwargs):
    graph = Graph(*args, **kwargs)
    return graph.html

class GraphTemplate(object):
    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.register_blueprint(app)
        app.add_template_global(graph)
        
    def register_blueprint(self, app):
        module = Blueprint(
            "graph",
            __name__,
            template_folder="templates"
        )
        app.register_blueprint(module)
        return module

graph_template = GraphTemplate()
graph_template.init_app(app)
