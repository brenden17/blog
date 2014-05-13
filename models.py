from google.appengine.ext import ndb


BLOG = 'blog'
PAGE = 'page'
BOOK = 'book'


class Post(ndb.Model):
    category = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)

    @classmethod
    def get_lastest(cls, count=5, category=None):
        if not category:
            return cls.query().order(-cls.date).fetch(count)
        else:
            return cls.query().filter(Post.category==category).order(-cls.date).fetch(count)

    @classmethod
    def get_1lastest(cls, count=1, category=None):
        if not category:
            return cls.query().order(-cls.date).fetch(count)[0]
        else:
            return cls.query().filter(Post.category==category).order(-cls.date).fetch(count)[0]


    def get_post(self, pre=True, category=None):
        posts = Post.query().filter(Post.category==category)
        if pre:
            posts = posts.filter(Post.date < self.date).order(-Post.date).fetch(1)
        else:
            posts = posts.filter(Post.date > self.date).order(Post.date).fetch(1)
        return posts[0] if posts else None

    def get_pre(self, category=None):
        return self.get_post(category=category)
    
    def get_next(self, category=None):
        return self.get_post(pre=False, category=category)
    
    def get_addr(self):
        return '/%s/%d' % (self.category, self.key.id())

    @classmethod
    def get_tagged_post(cls, tag):
        return cls.query(Post.tags.IN([tag]))

    def get_tags(self):
        return ', '.join(['<a href="/tags/%s">%s</a>' % (tag, tag) for tag in self.tags])