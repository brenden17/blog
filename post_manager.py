from __future__ import division
from glob import glob
from string import strip

from models import Post, Entity

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

def update_post(filename, post_base_dir='./post/'):
    filename = post_base_dir + filename
    with open(filename) as f:
        txt = f.readlines()
        category = map(strip, txt[0].strip().split(','))
        title = txt[1].strip().replace(' ', '-')
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
        suggest = [title.replace(' ', '-') for title in post.suggest]

        print suggest
        post.category = category
        post.title = title
        post.tags = tags
        post.content = content
        post.suggest = suggest
        post.put()
        print 'Existed post saved'

def update_all_post():
    dir_name = './post/*.v.md'
    files = glob(dir_name)
    for f in files:
        print f
        update_post(f, '')

class Node(object):
    def __init__(self, entity=''):
        self.entity = entity
        self.parent = set()
        self.children = set()
        self.ref = set()

    def get_ancestor(self):
        if not self.parent:
            return []
        ancestor = list()
        for p in self.parent:
            ancestor.append(p)
            ancestor.extend(p.get_ancestor())
        return ancestor

    def get_ancestor_depth(self):
        if not self.parent:
            return 1
        ancestor_depth = list()
        for p in self.parent:
            ancestor_depth.append(p.get_ancestor_depth()+1)
        return max(ancestor_depth)

    def get_descendant(self):
        if not self.children:
            return []
        descendant = list()
        for c in self.children:
            descendant.append(c)
            descendant.extend(c.get_descendant())
        return descendant

    def get_descendant_depth(self):
        if not self.children:
            return 1
        descendant_depth = list()
        for p in self.children:
            descendant_depth.append(p.get_descendant_depth()+1)
        return max(descendant_depth)

    def display(self, indent=''):
        return '==========\n%s\n%s\n%s\n%s\n==========' % (self.parent, self.entity, self.children, self.ref)

    def __eq__(self, other):
        if other == None:
            return False
        return self.entity == other.entity

    def __str__(self):
        return self.entity

    def __repr__(self):
        return self.entity

    def get_parent(self):
        return [p.entity for p in self.parent]

    def get_children(self):
        return [c.entity for c in self.children]

    def get_ref(self):
        return [r.entity for r in self.ref]

class Tree(object):
    def __init__(self):
        self.root = None
        self.entities = dict()

    def get_or_create(self, entity):
        node = self.entities.get(entity, None)
        if not node:
            node = Node(entity)
            self.entities[entity] = node
        return node

    def insert(self, entity, f, t, r):
        node = self.get_or_create(entity)
        for f_entity in f:
            parent = self.get_or_create(f_entity)
            if parent in node.get_descendant():
                raise RuntimeError("%s is %s's children."%(parent.entity, node.entity))

            node.parent.add(parent)
            parent.children.add(node)

        for t_entity in t:
            child = self.get_or_create(t_entity)
            if child in node.get_ancestor():
                raise RuntimeError("%s is %s's parent."%(child.entity, node.entity))

            node.children.add(child)
            child.parent.add(node)

        for r_entity in r:
            ref_node = self.get_or_create(r_entity)
            node.ref.add(ref_node)
            ref_node.ref.add(node)

        return node

    def build(self, filename, debug=True):
        with open(filename) as f:
            lines = f.readlines()
            all_nodes = set()
            for line in lines[1:]:
                line = line.strip()
                sub, obj = line.split('=')[0], line.split('=')[1]
                f = map(strip, obj.split('|')[0].split(',')) if obj.split('|')[0] else []
                t = map(strip, obj.split('|')[1].split(',')) if obj.split('|')[1] else []
                r = map(strip, obj.split('|')[2].split(',')) if obj.split('|')[2] else []
                print sub, f, t, r
                all_nodes |= set([sub]) | set(f) | set(t) | set(r)
                self.insert(sub, f, t, r)
                if debug:
                    for n in all_nodes:
                        n = self.get_or_create(n)
            return all_nodes

## update entity
def update_entity():
    tree = Tree()
    all_nodes = tree.build('./post/entity.txt', False)
    for node in all_nodes:
        node = tree.get_or_create(node)
        entity = Entity.query(Entity.name==node.entity).get()
        print '-----------------------'
        print node.get_parent()
        print node.entity
        print node.get_children()
        print node.get_ref()
        if entity:
            entity.from_entity = node.get_parent()
            entity.to_entity = node.get_children()
            entity.ref_entity = node.get_ref()
            entity.put()
        else:
            Entity(name=node.entity,
                   from_entity=node.get_parent(),
                   to_entity=node.get_children(),
                   ref_entity=node.get_ref(),
                   ).put()

## check category similarity
def tanimoto(s1, s2):
    c = len(set(s1)&set(s2))
    g = len(s1) + len(s2) - c
    return c/g if g else 0 

def calculate(n1, n2, w, sf=tanimoto):
    print n1, n1.get_ancestor_depth()
    return sf(n1.get_parent(), n2.get_parent()) * w['p'] + \
            sf(n1.get_children(), n2.get_children()) * w['c'] + \
            sf(n1.get_ancestor(), n2.get_ancestor()) * (n1.get_ancestor_depth() + n2.get_ancestor_depth())/2 * w['a'] + \
            sf(n1.get_descendant(), n2.get_descendant()) * (n1.get_descendant_depth() + n2.get_descendant_depth())/2 * w['d'] +\
            sf(n1.get_ref(), n2.get_ref()) * w['r']

def check_similar_entity():
    import pandas as pd
    from itertools import combinations
    tree = Tree()
    weight = {'p':0.3,
                'c':0.3,
                'a': 0.2,
                'd': 0.2,
                'r': 0.4}

    all_nodes = tree.build('./post/entity.txt', False)
    result = list()
    for n1, n2 in combinations(all_nodes, 2):
        n1 = tree.get_or_create(n1)
        n2 = tree.get_or_create(n2)
        result.append([n1, n2, calculate(n1, n2, weight)])

    r = pd.DataFrame(result)
    print r.sort([2], ascending=[0]).head(50)
