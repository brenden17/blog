data, hdf5
HDF5로 데이터 저장하기
pandas, h5py, scikit-learn
> HDF5는 NCSA에서 개발하기 시작한 오픈 소스 라이브러리이자 대량의 수치 데이터를 저장하기 위한 파일 포맷이다. 나사의 지구 관찰 시스템에서 연구 실험과 시뮬레이션에서 생성된 데이터 저장소까지 과학 커뮤니티에서 널리 사용되고 있다.
> 
> 몇년전부터 HDF5는 대량의 수치 데이터셋을 저장하기 위해 파이썬 세계에서 사실상 표준으로 떠올랐다. h5py 패키지는 파이썬스럽고(Pythonic), 사용하기 쉽지만 HDF5의 모든 특성을 사용할 수 있다.
> 
> HDF는 "Hierachical Data Format"의 약어이다.  
> 
> **Group은 딕션너리처럼 작동하며 dataset은 Numpy의 array처럼 작동한다.** 
> 

[h5py](http://www.h5py.org/docs/intro/quick.html) 일부를 번역하였다.

기계 학습을 하다보면 많은 성능을 높일 수 있는 부분은 데이터 전처리(data preprocessing) 단계라 할 수 있다.

데이터 전처리를 하다 보면 꽤 시간이 걸리는 부분이 있다. 할 때마다 하기보다는 저장을 해 사용하는 것도 좋은 방법이다.

numpy의 save를 사용해 보면 어떨까?

물론 좋을 수도 있으나 좀 더 다양한 기능을 제공하는 HDF5를 사용하면 좋을 듯 하다. 그럼, 어떠한 기능을 제공할까?

 * 계층적으로 관리 할 수 있다.
 * 부가 정보를 저장할 수 있다.
 * 압축하여 저장할 수 있다.
 
또한, Pandas에서는 기본적으로 HDF5를 지원한다.

    store = pd.HDFStore('store.h5')
    
하지만, Pandas를 사용하기 좀 힘들다. 왜냐하면 전처리를 하고 나면 dataframe보다 numpy의 array로 처리할 경우가 많기 때문이다.
HDF5가 자연스럽게 사용할 수 있다. 이와 더불어 고려해 볼 사항은 [jug](http://pythonhosted.org/Jug/)이다.
다음에 좀 더 이부분은 다루어 보겠다.
어쨌든 다양한 전처리를 시도해 보고 각 처리된 데이터를 저장하면 다음에 처리할 때 시간을 절약할 수 있게 한다.

데이터셋은 http://archive.ics.uci.edu/ml/datasets/Letter+Recognition에서 구했다.
20000개 아이템과 16개 속성을 가지고 있기에 좀 작은 듯 하지만 간단하게 처리해 볼 수 있다.
우선 데이터를 읽어보자.

    letter_df = pd.read_csv(get_fullpath('letter-recognition.data'),
                            names=['lettr', 'x-box', 'y-box',
                                   'width', 'high', 'onpix',
                                   'x-bar', 'y-bar', 'x2bar',
                                   'y2bar', 'xybar', 'x2ybr',
                                   'xy2br', 'x-ege', 'xegvy',
                                   'y-ege', 'yegvx'],
                            delimiter=',')
    print letter_df.describe()
    le = LabelEncoder()
    letter_df['lettr_co'] = le.fit_transform(letter_df['lettr'].values)
 
    X = letter_df.icol(range(1, 17)).values
    y = letter_df['lettr_co'].values

결과적으로 테스트 해 보면(기본적인 매개변수를 사용하면) SVC와 16개 속성을 사용할 때 최상의 결과를 낸다.
하지만, 몇가지 전처리를 시도해 보자.  

 * SelectKBest
 * SelectPercentile
 * RFE

등을 사용할 수 있다.
먼저 SelectPercentile를 사용한 후 HDF5에 저장한다.

    X, y = load()
    if f.get('/letter/SelectPercentile', False):
        print '/letter/SelectPercentile exist'
        return f['/letter/SelectPercentile'], y

    selector = SelectPercentile(f_classif, percentile=90)
    X = selector.fit_transform(X, y)
    f['/letter/SelectPercentile'] = X
    f['/letter/SelectPercentile'].attrs['f_classif'] = 'f_classif'
    f['/letter/SelectPercentile'].attrs['percentile'] = 90
    return X, y

다음은, SelectKBest으로 사용해 보자.

    X, y = load()
    if f.get('/letter/selectkbest', False):
        print '/letter/selectkbest exist'
        return f['/letter/selectkbest'], y

    skb = SelectKBest(chi2, k=7)
    X = skb.fit_transform(X, y)
    f['/letter/selectkbest'] = X
    f['/letter/selectkbest'].attrs['chi2'] = 'chi2'
    f['/letter/selectkbest'].attrs['k'] = 7
    
이렇게 저장하면 차후 작업에 시간을 절약 할 수 있다.


