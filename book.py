#-*- coding: utf-8 -*-
import HTMLParser
import re

import simplejson, urllib

title = '온더무브'

"""
http://apis.daum.net/search/book?output=json&apikey=b62b20a07b737c1cca5b88737980adb11809762a&q=python
"""
h = HTMLParser.HTMLParser()
def clean(s):
    s = h.unescape(s)
    return re.sub('<[^<]+?>', '', s)

url='http://apis.daum.net/search/book?output=json&apikey=b62b20a07b737c1cca5b88737980adb11809762a&q=' + title

result = simplejson.load(urllib.urlopen(url))
print result
info = result['channel']
for item in info['item'][:2]:
    print clean(item['title'])
    print clean(item['cover_s_url'])
    print clean(item['cover_l_url'])
    print clean(item['author'])
    print clean(item['translator'])
    print clean(item['category'])
    print clean(item['isbn'])
