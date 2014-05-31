import logging

from google.appengine.ext import ndb

PAGE = 'page'
BLOG = 'blog'
WORK = 'work'
BOOK = 'book'

class DisplayerMixin(object):
    def get_tags(self):
        return ', '.join(['<a href="/%s">%s</a>' % (tag, tag) for tag in self.tags])

    def get_categorys(self):
        return ', '.join(['<a href="/%s">%s</a>' % (c, c) for c in self.category])

class Post(ndb.Model, DisplayerMixin):
    category = ndb.StringProperty(repeated=True)
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)
    suggest = ndb.StringProperty(repeated=True) 

    @classmethod
    def get_lastest(cls, count=5, category=None):
        if not category:
            return cls.query().order(-cls.date).fetch(count)
        else:
            return cls.query().filter(Post.category.IN([category])).order(-cls.date).fetch(count)

    @classmethod
    def get_1lastest(cls, count=1, category=None):
        if not category:
            return cls.query().order(-cls.date).fetch(count)[0]
        else:
            return cls.query().filter(Post.category.IN([category])).order(-cls.date).fetch(count)[0]


    def get_post(self, pre=True, category=None):
        if category:
            posts = Post.query().filter(Post.category.IN([category]))
        else:
            posts = Post.query()
            
        if pre:
            posts = posts.filter(Post.date < self.date).order(-Post.date).fetch(1)
        else:
            posts = posts.filter(Post.date > self.date).order(Post.date).fetch(1)
        return posts[0] if posts else None

    def get_pre(self, category=None):
        return self.get_post(category=category)
    
    def get_next(self, category=None):
        return self.get_post(pre=False, category=category)
    
    @classmethod
    def get_tagged_post(cls, tag):
        return cls.query(Post.tags.IN([tag]))
    
    def get_addr(self, category=None):
        return '/%s/%s' % ('page', self.title)

class Entity(ndb.Model):
    name = ndb.StringProperty(required=True)
    from_entity = ndb.StringProperty(repeated=True)
    to_entity = ndb.StringProperty(repeated=True)
    ref_entity = ndb.StringProperty(repeated=True)
    
    def get_addr(self, category=None):
        return '/%s' % (self.name)
    
    def get_post(self):
        return Post.query().filter(Post.category.IN([self.name]))
