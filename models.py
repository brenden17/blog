from google.appengine.ext import ndb

class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    contents = ndb.TextProperty(required=True)
    when = ndb.DateTimeProperty(auto_now_add=True)
    tags = ndb.StringProperty(repeated=True)

