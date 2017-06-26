from __future__ import division
from glob import glob
from os.path import basename
from os.path import splitext
from string import strip

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

def read_file(filename, readline=False):
    with open(filename, 'r') as f:
        return f.readlines() if readline else f.read()

def get_feature(filename):
    rawdata = read_file(filename, readline=True)
    feature = []
    i = 0
    for line in rawdata:
        i += 1
        #print line
        line = line.strip().decode('utf-8')
        if i == 1: # category
            feature.append(line)
        if i == 2: # title
            feature.append(line.replace(' ', '-'))
        if i == 3: # tag
            feature.append(line)
            break
    return feature

def init_data():
    get_filename = lambda x: splitext(basename(x))
    #dir_name = './postv0/*.*'
    dir_name = './post/*.v.md'
    files = glob(dir_name)
    dir_name2 = './post/*.v.md'
    files2 = glob(dir_name2)
    return map(read_file, files), map(get_feature, files2), files

def vectorize(data):
    vectorizer = CountVectorizer(max_df=10, min_df=2)
    counts = vectorizer.fit_transform(data)
    tfidf = TfidfTransformer().fit_transform(counts)
    return tfidf

def get_knn_score(data, target_page):
    data = vectorize(data)
    knn = NearestNeighbors(n_neighbors=30)
    knn.fit(data)
    result = knn.kneighbors(data[target_page,:])
    score = result[0][0]
    index = result[1][0]

    """
    for i in index.tolist():
        print files[i]
    for i in index.tolist():
    print map(float, score)
    print index.tolist()
    """
    return index.tolist(), score.tolist()

def convert_pd(filted_feature, score):
    refine = lambda x: (x[0][0].strip(), x[0][1].strip(), map(strip, x[0][2].split(',')), x[1])
    d = pd.DataFrame([refine(x) for x in zip(filted_feature, score)],
                        columns=['category', 'title','tag', 'knn_score'])

    #print d
    return d

def tanimoto(s1, s2):
    c = len(set(s1)&set(s2))
    de = len(s1) + len(s2) - c
    return 0 if de == 0 else float(c) / de

def dice(s1, s2):
    c = len(set(s1)&set(s2))
    de = len(s1) + len(s2)
    return 0 if de == 0 else float(2 * c) / de
    
def calculate(pd_data, target_index=0, n_suggest=7, debug=False):
    weight = {'knn':1, 'category':0.7, 'tag':0.1}
    knn_score_min, knn_score_max = pd_data['knn_score'].min(),\
                                            pd_data['knn_score'].max()
    def calculate_normalized_knn_score(row, knn_score_min, knn_score_max):
        return round(1 - (row['knn_score'] - knn_score_min) / knn_score_max, 4) * weight['knn']
    
    pd_data['knn_normalized_score'] = \
                               pd_data.apply(calculate_normalized_knn_score,
                               args=(knn_score_min, knn_score_max), axis=1)

    # CATEGORY
    target_category = pd_data['category'][target_index]
    def calculate_category(row, target_category):
        return tanimoto(target_category, row['category']) * weight['category']
#         if target_category == row['category']:
#             return 1 * weight['category']
#         else:
#             return 1
    pd_data['category_score'] = pd_data.apply(calculate_category,
                                        args=(target_category,), axis=1)
    # Tag
    target_tag = pd_data['tag'][target_index]
    def calculate_tag(row, target_tag):
        return tanimoto(target_tag, row['tag']) * weight['tag']
#         intersection = set(target_tag) & set(row['tag'])
#         return (len(intersection) / len(set(row['tag']))) * weight['tag']

    pd_data['tag_score'] = pd_data.apply(calculate_tag,
                                        args=(target_tag,), axis=1)

    pd_data['total_score'] = \
                        pd_data['category_score'] + \
                        pd_data['tag_score'] + \
                        pd_data['knn_normalized_score']
    d = pd_data.sort_values(['total_score'], ascending=[False])

    if debug:
#         print d[['title', 'total_score', 'knn_normalized_score',
#                                                 'category_score', 'tag_score']]
        print d.iloc[0:10][['title', 'total_score', 
                            'category_score', 'tag_score',
                            'knn_normalized_score']].head(10)
    return d.iloc[1:n_suggest]['title'].tolist()

def check_post(target_index=1):
    f_data, feature, files = init_data()
    #for i, fname in enumerate(files): print i, fname
    print 'total page:', len(files)
    print 'page:', files[target_index]
    # step1 - knn
    index, score = get_knn_score(f_data, target_index)
    # step2 - feature
    filted_feature = [feature[i] for i in index]
    pd_data = convert_pd(filted_feature, score)
    # calculate
    suggested_titles = calculate(pd_data, 0, 5, True)

def bulk():
    f_data, feature, files = init_data()
    result = {}
    print 'files %d' % (len(files))
    for k in range(0, len(files)):
        # step1 - knn
        index, score = get_knn_score(f_data, k)
        # step2 - feature
        filted_feature = [feature[i] for i in index]
        pd_data = convert_pd(filted_feature, score)
        # calculate
        suggested_titles = calculate(pd_data, 0, 6, True)
        result[feature[k][1].strip()] = suggested_titles
    return result

def check_suggest():
    from models import Post
    result = bulk()
    i = 0
    for post in Post.query():
        try:
            print i, post.title.strip()
            i += 1
            for t in result[post.title.strip()]:
                print '\t %s' % (t,)
        except:
            print '++++++++++++++++++++++'
            print 'No title ', post.title

def update_suggest():
    from models import Post
    result = bulk()
    for post in Post.query():
        try:
            print post.title.strip()
            post.suggest = result[post.title.strip()]
            post.put()
        except:
            print '++++++++++++++++++++++'
            print 'No title ', post.title

if __name__ == '__main__':
    check_post(65)
    # bulk()
    # update_suggest()