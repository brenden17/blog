import logging

from google.appengine.ext import ndb

def strip(l):
        return [] if len(l) == 1 and l[0]=='' else l

class DisplayerMixin(object):
    def get_tags(self):
        return ', '.join(['<a href="/%s">%s</a>' %
                          (t, t) for t in strip(self.tags)])

    def get_categorys(self):
        return', '.join(['<a href="/%s">%s</a>' %
                         (c, c) for c in strip(self.category)])

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

    def get_addr(self, category=None, nav=False):
    	if nav:
    		return '/%s/%s' % ('page', self.title)
    	if self.is_entity():
    		return '/%s' % (self.title,)
        return '/%s/%s' % ('page', self.title)

    def get_json(self):
        return {
            'category': ','.join(self.category),
            'title':self.title,
            'date':self.date.strftime('%m/%b/%Y'),
            'tags':','.join(self.tags)
        }
        
    def is_entity(self):
    	if self.tags == [''] and self.category == ['']:
    		return True
    	return False

class Entity(ndb.Model):
    name = ndb.StringProperty(required=True)
    from_entity = ndb.StringProperty(repeated=True)
    to_entity = ndb.StringProperty(repeated=True)
    ref_entity = ndb.StringProperty(repeated=True)

    def get_addr(self, category=None):
        return '/%s' % (self.name)

    def get_post(self):
        return Post.query().filter(ndb.OR(Post.category.IN([self.name]),
                            Post.tags.IN([self.name])))

    def get_json(self):
        entity_json = list()
        for f in self.from_entity:
            d = {'source':self.name, 'target':f, 'type':'resolved'}
            entity_json.append(d)
        for t in self.to_entity:
            d = {'source':self.name, 'target':t, 'type':'suit'}
            entity_json.append(d)
        for r in self.ref_entity:
            d = {'source':self.name, 'target':r, 'type':'licensing'}
            entity_json.append(d)

        return entity_json

