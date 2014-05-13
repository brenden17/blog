from string import strip

from google.appengine.api import search
from google.appengine.ext import ndb

from models import Post

POSTBASEDIR = './post/'
POSTBIFILE = POSTBASEDIR + 'blog.ini'

def get_postid(filename):
    with open(POSTBIFILE) as f:
        lines = f.readlines()
        for line in lines:
            savedfilename, postid = line.split(',')
            if savedfilename.strip() == filename.strip():
                return postid.strip()
        return None

def set_postid(filename, postid):
    with open(POSTBIFILE, 'a') as f:
        f.write('{0},{1}\n'.format(filename.strip(), postid))

def create_post(filename):
    filename = POSTBASEDIR + filename
    with open(filename) as f:
        txt = f.readlines()
        category = txt[0].strip()
        title = txt[1].strip()
        tags = map(strip, txt[2].strip().split(','))
        content = ''.join(txt[3:])

    postid = get_postid(filename)
    print 'postid...', postid
    if not postid:
        key = Post(category=category,
                    title=title,
                    tags=tags,
                    content=content).put()
        print 'key...', key.id()
        set_postid(filename, key.id())
        print 'New post saved'
    else:
        post = Post.get_by_id(int(postid))
        post.category = category
        post.title = title
        post.tags = tags
        post.content = content
        post.put()
        print 'Existed post saved'

