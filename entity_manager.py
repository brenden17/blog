from glob import glob
from string import strip
import unittest
import sys

    
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
    
    def get_descendant(self):
        if not self.children:
            return []
        descendant = list()
        for c in self.children:
            descendant.append(c)
            descendant.extend(c.get_descendant())
        return descendant
    
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
    
class Tree(object):
    def __init__(self):
        self.root = None
        self.entities = dict()
    
    def get_or_create(self, entity):
        node = self.entities.get(entity, False)
        if not node:
            node = Node(entity)
            self.entities[entity] = node
        return node
        
    def insert(self, entity, f, t, r):
        node = self.get_or_create(entity)
        node.display()
        print entity, node.entity
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
        
        node.display()
        return node
    
    def display(self, indent=''):
        if not self.root:
            print 'No root'
        
        for child in self.root.children:
            child.display(indent)
    
    def build(self, filename):
        with open(filename) as f:
            lines = f.readlines()
            all_node = set()
            for line in lines[1:]:
                sub, obj = line.split('=')[0], line.split('=')[1]
                f = obj.split('|')[0].split(',') if obj.split('|')[0] else []
                t = obj.split('|')[1].split(',') if obj.split('|')[1] else []
                r = obj.split('|')[2].split(',') if obj.split('|')[2] else []
                print sub, f, t, r
                all_node |= set([sub]) | set(f) | set(t) | set(r)
                self.insert(sub, f, t, r)
            print all_node
            
            for n in all_node:
                n = self.get_or_create(n)
                print n.display()
        return all_node

        
class Test(unittest.TestCase):
    def test_tree(self):
        s = """
        a=b,c,d|e,f|g
        b=e,f|c,b|
        c=|e|f
        """
        s1 = """book=||\namazon=book,company|aws,kindle|google\naws=tech||gae\ngoogle=company|gae|amazon"""
        tree = Tree() 
        lines = s1.split('\n')
        all_node = set()
        for l in lines:
#            print l
            sub, obj = l.split('=')[0], l.split('=')[1]
            f = obj.split('|')[0].split(',') if obj.split('|')[0] else []
            t = obj.split('|')[1].split(',') if obj.split('|')[1] else []
            r = obj.split('|')[2].split(',') if obj.split('|')[2] else []
            print sub, f, t, r
            all_node |= set([sub]) | set(f) | set(t) | set(r)
            tree.insert(sub, f, t, r)
        print all_node
        
        for n in all_node:
            n = tree.get_or_create(n)
            print n.display()

def test():
    tree = Tree()
    tree.build('./post/entity.txt')

if __name__ == "__main__":
#    unittest.main()
    test()

        