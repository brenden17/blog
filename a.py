from models import Post

def create_post(filename):
    with open(filename) as f:
        txt = f.readlines()
        category = txt[0]
        title = txt[1]
        tags = txt[2].split(',')
        content = '\n'.join(txt[3:])

        post = Post(category=category,
                title=title,
                content=content,
                tags=tags)
        return post.put()
