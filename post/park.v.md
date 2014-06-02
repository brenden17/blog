scikit-learning, natural language processing
박근혜 대통령 연설의 가벼운 분석
pandas, pyhannanum
2014년 박근혜 대통령이 신년 연설을 했다. 

* 2013년 대통령 취임 연설
* 2013년 국회 연설
* 2014년 신년 연설

다른 대통령보다 연설이나 대화가 적었기 때문에 총 3번의 연설을 기반으로 가볍게 분석해 보았다.

다음과 같이 실시한다.

1. 3회 연설에서 형태소 분석을 통해 명사만 구한다.
1. 명사의 빈도를 구한다. 
1. 각 연설의 빈도를 모두 더하고 비교한다.

다음 함수로 명사의 빈도를 구한다.

    def file2df(filename):
        with open(get_fullpath(filename), 'r') as f:
            rawdata = f.read()
    
        data = rawdata.split('\n')
        countvector = CountVectorizer(min_df=1)
        words = countvector.fit_transform(data).toarray()
        features = np.array(countvector.get_feature_names())
        np.clip(words, 0, 1, out=words)
        dist = np.sum(words, axis=0)
        return pd.DataFrame(zip(features, dist), columns=['term', 'count'])
    
    
다음 함수로 각 연설의 빈도를 더하고 비교한다.

    def compare_all():
        address201302 = file2df('20130215_noun.txt')
        address201311 = file2df('20131118_noun.txt')
        address201401 = file2df('20140106_noun.txt')
        address = pd.merge(address201302, address201311, on='term',
                        how='outer',
                        suffixes=('_201302', '_201311')).fillna(0)
    
        address = pd.merge(address, address201401, on='term',
                        how='outer').fillna(0)
        address.rename(columns={'count':'count_201401'}, inplace=True)
    
        address['total'] = address['count_201302'] + address['count_201311'] + address['count_201401']
        address = address.sort([('total')], ascending=True)
        for row in address.itertuples():
            print "['%s', %d, %d, %d, %d]," % (row[1], row[2], row[3], row[4], row[5])

결과는 다음과 같다.

    ['창출', 0, 6, 3, 9],
    ['생각', 2, 6, 2, 10],
    ['노력', 2, 8, 0, 10],
    ['발전', 7, 2, 1, 10],
    ['산업', 3, 5, 2, 10],
    ['내년', 0, 9, 1, 10],
    ['모두', 7, 3, 0, 10],
    ['올해', 0, 1, 9, 10],
    ['적극', 2, 5, 3, 10],
    ['강화', 0, 8, 3, 11],
    ['활성화', 0, 9, 2, 11],
    ['투자', 0, 6, 5, 11],
    ['국회', 0, 11, 0, 11],
    ['대통령', 3, 7, 1, 11],
    ['신뢰', 8, 2, 2, 12],
    ['희망', 9, 2, 1, 12],
    ['중소기업', 2, 4, 6, 12],
    ['미래', 7, 3, 3, 13],
    ['일자리', 2, 9, 3, 14],
    ['북한', 5, 3, 6, 14],
    ['국가', 6, 5, 3, 14],
    ['확대', 1, 8, 6, 15],
    ['존경', 5, 6, 5, 16],
    ['사회', 11, 3, 4, 18],
    ['추진', 1, 8, 9, 18],
    ['지원', 3, 9, 6, 18],
    ['세계', 8, 6, 6, 20],
    ['대한', 12, 5, 4, 21],
    ['민국', 12, 5, 4, 21],
    ['문화', 15, 5, 1, 21],
    ['창조', 8, 8, 7, 23],
    ['시대', 19, 3, 3, 25],
    ['여러', 10, 9, 9, 28],
    ['행복', 19, 9, 4, 32],
    ['정부', 8, 21, 9, 38],
    ['우리', 20, 16, 8, 44],
    ['경제', 11, 20, 15, 46],
    ['국민', 44, 26, 18, 88],

좀 더 구체적인 분석을 위해 일부 단어를 처리해야 하겠다. 이 부분에 대해서는 좀 더 찾아 봐야 할 듯 하다.

**'경제'**라는 단어는 2013년 취임 연설에서는 11회, 국회에선 20회, 신년 연설은 15회,총 46회 사용했다.

역시 **'경제'**, **'창조'**, **'일자리'**등이 많이 사용되었고 2013년 연설은 취임식이였기 때문에 좀 더 관용적 단어인 행복, 희망, 신뢰등을 더 많이 사용하였다.

차후 stop word보다 높은 개념인 삭제 가능한 단어를 찾는 방법을 알아봐야 할 듯 하다.
   
  
