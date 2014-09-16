machine-learning, scikit-learn
scikit-learn을 활용한 기계 학습(2014년 7월 마이크로소프트)
iris, pca

**본 내용은 2014년 7월 마이크로소프트의 [스텝바이스텝]으로 실린 내용이기 때문에 일부 내용을 제한했습니다.**

# scikit-learn을 활용한 기계 학습

요즘 우리는 다양한 디바이스와 더불어 눈치 채기 어려운 흥미로운 기능들 속에서 살고 있다. 이를 테면, 핸드폰은 메시지 작성할 때 쓰고 있는 단어와 가장 연관성이 높은 다음 단어를 예측해 보여주고, 페이스북에서 찍은 사진을 올리면 별도의 정보 없이 내 주변 사람 중 누구인지를 인식해 태그를 붙인다. 아마존과 같은 인터넷 서점에 가면 내가 살만한 책을 추천한다. 
잠들기 전, 불현듯 어떻게 단어, 주변 사람들, 기호를 이 기계들이 알고 있을까 궁금하게 되면서 석연치 않은 의심까지도 한다. 빅데이터라는 단어를 떠올리며 넘어가려 해도 개인 정보가 유출된 것은 아닌지 영 찜찜하다. 어떻게 이러한 기술이 나타나게 됐을까? 이유는 여러 가지일 수 있지만 몇 가지 혁신적인 기술로 가능하게 되었다.

가장 먼저 말할 수 있는 점은 컴퓨팅 환경의 변화다. 인터넷이나 여러 기계상에서 하는 행위는 나 이외 다른 누구에게도 중요한 정보가 됐다. 모바일, 자동차 GPS, 서버 로그 등 우리 주변의 다양한 하드웨어에서 데이터를 쏟아내고 있다. 더욱이 저장 공간 비용은 저렴해지는 반면, 네트워크는 빨라지고 있는 형태로 데이터가 축적되고 있다. 확률과 통계학이 발전하면서 동시에 기계 학습도 발전한 이유도 하나의 주요한 요인이다. 

기계 학습이란 말 그대로 엄마가 아이를 가르치듯이 기계를 학습시키는 것이다. 엄마가 아이에게 하나 하나 가르치는 것과는 달리, 우리가 가지고 있는 데이터를 기계에 학습시킨 후 학습한 데이터와 유사한 데이터를 입력하면 기계는 우리가 알고 싶어하는 정보를 예측한다. 마치, 선생님이 학생들에게 시험 범위 안에서 학습을 시킨 후 시험을 보는 것도 비슷하다. 가장 쉽게 접할 수 있는 예는 이메일을 자동으로 분류하는 시스템이다. 이 시스템은 이전에 온 스팸 이메일 정보를 근거로 새로 온 이메일이 스팸인지 아닌지 분류한다.

이 글은 간단한 예제에 기계 학습을 적용하면서 기계 학습의 전반적인 이해를 높이도록 하는 것이 목적이다. 예제는 파이썬을 기반으로 하며 기계 학습을 쉽게 적용할 수 있도록 scikit-learn 라이브러리를 사용한다.

# 파이썬과 scikit 스택

파이썬은 비교적 배우기 쉬운 컴퓨터 언어로 구글이 초기 시스템을 구축할 때 사용했고 유튜브 추천 시스템을 만들 때도 사용한 언어로 유명하다. 다른 신생 언어보다 다양하고 적용하기 쉬운 라이브러리를 가지고 있어, 다양한 분야에서 사용되고 있다. 특히, 공학자나 과학자들에게 인기가 높다. 파이썬 라이브러리 넘피(numpy)는 매트랩(matlab)과 유사하게 매트리스 연산을 쉽게 할 수 있으며 라이브러리 scipy는 이산이나 공학에서 자주 사용하는 계산이나 함수를 모아 최적화해 쉽고 빠르게 문제에 적용할 수 있다. 이와 더불어 pandas는 R의 데이터프레임과 유사하게 구현돼 있어 데이터를 손쉽게 처리할 수 있다. 하지만 이 예제에서는 사용하지 않겠다. 이러한 라이브러리는 모두 넘피를 기반으로 되어 있기 때문에 이를 사용하는 다른 라이브러리와 호환이 잘되며, 기능 확장을 하거나 통합하는데 문제가 되지 않는다. 

# 기계 학습(Machine Learning) 소개

기계 학습은 기존 데이터를 사용하여 새로운 데이터의 정보를 유추할 수 있도록 한다. 이러한 기계 학습은 일반적으로 크게 몇 단계로 나눌 수 있다. 여기에서는 크게 3 단계로 나누어 보겠다.

 1. 데이터 정리 및 이해
 1. 모델의 학습
 1. 모델의 평가

가장 먼저 할 일은 데이터를 충분한 이해하는 것이다. 데이터를 이해해 유효한 데이터와 유효하지 않은 데이터를 판단한다. 이를 기반으로 데이터를 추상할 기법을 선택한다. 하지만 너무 부담을 가질 필요는 없다. 잘못된 판단이지만 나중에 좀 더 나은 결과를 얻게 하는 계기가 될 수 있다. 파이썬은 빠르고 쉽게 데이터를 처리할 수 있기 때문에 큰 문제가 되지 않는다. 이러한 특징 때문에 파이썬을 선택하기도 한다.

다음은 데이터에 대해 모델을 학습하는 단계다. 데이터를 가장 잘 추상화 할 수 있는 기법을 선택하여 기계를 학습한다. 신경망(neural network), 서포트 벡터 머신(support vector machine), K평균(KMeans)등 다양한 모델을 생성한다. 모델에는 다른 매개 변수(parameter)가 있다. 입력 데이터와 모델이 같더라도 매개 변수를 변경해 다른 결과를 얻을 수도 있다.

마지막으로 학습한 모델의 평가가 필요하다. 다양한 모델과 각 모델의 여러 조건으로 데이터를 예측할 수 있고, 이 예측이 얼마나 정확한지 평가해야 더 나은 모델이나 기법을 선택할 수 있다.

기계 학습 알고리즘을 학습하는 방법에 따라 크게 두 가지로 나눌 수 있다. 지도 학습(supervised learning)은 데이터에 예측하고자 하는 목적 속성(target feature)이 있어 예측 모델(predictive model)을 구축한다. 하지만 비지도 학습(unsupervised learning)은 목적 속성 없이 기술 모델(descriptive model)을 구축한다. 전자의 대표적인 예는 스팸 메일 분류다. 스팸 메일과 햄 메일(정상 메일)로 구분할 수 있는 목적 속성을 가진 데이터를 가지고 학습한 후 스팸 메일을 분류한다. 후자의 예는 영화 추천과 같이 나와 기호가 같은 사용자가 본 영화를 찾아 추천해 주는 시스템이다. 

# scikit-learn 소개

scikit-learn은 2007년 구글 썸머 코드에서 처음 구현됐으며 현재 파이썬으로 구현된 가장 유명한 기계 학습 오픈 소스 라이브러리다. scikit-learn의 장점은 라이브러리 외적으로는 scikit 스택을 사용하고 있기 때문에 다른 라이브러리와의 호환성이 좋다. 내적으로는 통일된 인터페이스를 가지고 있기 때문에 매우 간단하게 여러 기법을 적용할 수 있어 쉽고 빠르게 최상의 결과를 얻을 수 있다.

라이브러리의 구성은 크게 지도 학습, 비지도 학습, 모델 선택 및 평가, 데이터 변환으로 나눌 수 있다(scikit-learn 사용자 가이드 참조, http://scikit-learn.org/stable/user_guide.html). 지도 학습에는 서포트 벡터 머신, 나이브 베이즈(Naïve Bayes), 결정 트리(Decision Tree)등이 있으며 비지도 학습에는 군집화, 이상치 검출 등이 있다. 모델 선택 및 평가에는 교차 검증(cross-validation), 파이프라인(pipeline)등 있으며 마지막으로 데이터 변환에는 속성 추출(Feature Extraction), 전처리(Preprocessing)등이 있다.

클래스별로 보자면, 각 기법들이 공통으로 가지고 있어야 하는 기본 BaseEstimator가 있으며 기법의 공통적인 부분을 모은 ClassifierMixin, RegressorMixin, ClusterMixin들이 있어 기법들은 각각의 기법의 클래스를 상속 받아 구현할 수 있다. 대부분의 클래스는 입력 데이터를 적합화하는 fit 메소드와 새로운 데이터를 예측하는 predict 메소드를 가지고 있다.

간단한 예제로 기계 학습을 어떻게 적용할 수 있는지를 알아본다. 기계 학습에서 자주 사용하는 1936년에 만들어진 피셔경(http://ko.wikipedia.org/wiki/로널드_피셔)의 붓꽃(iris) 데이터를 사용한다. 이 데이터를 사용하는 이유는 구하기가 쉽고 데이터 크기와 속성이 적기 때문에 빠르게 실험 결과를 볼 수 있다. scikit 스택과 scikit-learn(코드에서는 라이브러리 명은 sklearn으로 사용)을 설치한다.

윈도우(http://sourceforge.net/projects/numpy/,  http://sourceforge.net/projects/scikit-learn/, http://sourceforge.net/projects/scipy/)
에서 각각의 라이브러리 설치자를 내려 받아 설치하고 다음과 같이 파이썬 쉘(shell)에서 코드를 실행한다. 잘 설치되었다면 아무 메시지가 나오지 않고 버전을 확인 할 수 있다.

<리스트 1> scikit-learn 설치 후 코드 실행

    import numpy as np
    import scipy
    import sklearn

    np.__version__
    1.8.1'
    sklearn.__version__
    '0.14.1'
    scipy.__version__
    '0.13.3'


scikit-learn을 설치하면 기본적으로 포함되어 있는 데이터가 있다. 이를테면, 숫자 데이터, 보스턴 주택 가격, 그리고 그 중 하나가 iris 데이터이다.

![alt text](http://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Iris_sanguinea_2007-05-13_361.jpg/180px-Iris_sanguinea_2007-05-13_361.jpg "iris")

붓꽃(출처 - http://ko.wikipedia.org/wiki/붓꽃속)

<리스트 2> iris 데이터 출력 코드 

    from sklearn import datasets

    iris = datasets.load_iris()
    print(iris.DESCR)
    print(iris.target_names)


iris 데이터의 기본 정보를 보고자 iris.DESCR을 실행하면 <리스트 3>과 같은 정보가 나온다. 

<리스트 3> iris.DESCR 실행 결과

    Data Set Characteristics:
        :Number of Instances: 150 (50 in each of three classes)
        :Number of Attributes: 4 numeric, predictive attributes and the class
        :Attribute Information:
            - sepal length in cm
            - sepal width in cm
            - petal length in cm
            - petal width in cm
            - class:
                    - Iris-Setosa
                    - Iris-Versicolour
                    - Iris-Virginica
        :Summary Statistics:
        ============== ==== ==== ======= ===== ====================
                        Min  Max   Mean    SD   Class Correlation
        ============== ==== ==== ======= ===== ====================
        sepal length:   4.3  7.9   5.84   0.83    0.7826
        sepal width:    2.0  4.4   3.05   0.43   -0.4194
        petal length:   1.0  6.9   3.76   1.76    0.9490  (high!)
        petal width:    0.1  2.5   1.20  0.76     0.9565  (high!)
        ============== ==== ==== ======= ===== ====================


150개의 데이터와 4개의 속성인 꽃받침 길이, 꽃받침 너비, 꽃잎 길이, 꽃잎 너비가 있으며 각 속성의 최소값, 최대값, 평균 등을 볼 수 있다. 목적 속성은 0, 1, 2이며 iris.target_names으로 볼 수 있으며 Setosa, Versicolour, Virginica다
iris 객체는 data와 target 속성을 가지고 있으며 data는 iris 데이터의 속성들이며, target은 목적 속성이다. 데이터와 목적 속성을 편의상 X, y로 지정하도록 하자.

<리스트 4> 데이터와 목적 속성 지정 및 결과

    X, y = iris.data, iris.target
    print('Size of data : %s' % (X.shape, )) 
    print('Target value : %s' % np.unique(y))

    Size of data : (150, 4)
    Target value : [0 1 2]


가장 위에 있는 10개의 데이터를 살펴보면 다음과 같다. 150개 각각에 대해 꽃의 꽃받침 길이, 꽃받침 너비, 꽃잎 길이, 꽃잎 너비를 측정하여 속성으로 만들었음을 볼 수 있다.

<리스트 5> 10개의 데이터 

    print(X[0:10, :])

    [[ 5.1  3.5  1.4  0.2]
     [ 4.9  3.   1.4  0.2]
     [ 4.7  3.2  1.3  0.2]
     [ 4.6  3.1  1.5  0.2]
     [ 5.   3.6  1.4  0.2]
     [ 5.4  3.9  1.7  0.4]
     [ 4.6  3.4  1.4  0.3]
     [ 5.   3.4  1.5  0.2]
     [ 4.4  2.9  1.4  0.2]
     [ 4.9  3.1  1.5  0.1]]


데이터를 준비하였고 가볍게 살펴봤다. 이 데이터로 기계 학습 기법 중 하나를 훈련시켜 sample이라는 임의에 데이터가 어떤 꽃에 속하는지 예측한다.  이를 위해 기계 학습 기법을 선택할 차례다. 

    sample = [[6, 4, 6, 2],]

## k 최근접 이웃(kNN) 알고리즘 소개

다양한 학습 기법이 있지만 간단하고 데이터 특성만 잘 맞는다면 좋은 결과를 얻을 수 있는  k 최근접 이웃 알고리즘(kNN, k-Nearest Neighbors algorithm, http://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)을 사용하겠다. kNN은 매우 단순하여 예측하고자 하는 데이터에 가까이 있는 k개의 데이터의 목적 속성을 보고 데이터를 예측하는 방법이다. 

k가 3이라면 예측하고자 하는 데이터에 가까이 있는 3개 데이터의 목적 속성에서 가장 많이 있는 것에 따라 예측한다. 이 알고리즘에는 k뿐만 아니라 몇 가지 매개 변수(parameter)가 있는데 주변 데이터에 따른 가중치와 주변 데이터를 계산할 알고리즘 등이 있다. scikit-learn에 있는 KNeighborsClassifier 클래스를 사용한다. 초기 k값인 n_neighbors를 1로 설정한다. 가장 가까운 하나의 데이터를 보고 그 속성으로 예측하겠다는 의미다. fit메쏘드에 X, y를 입력하여 적합화하고 predict 메소드에 샘플을 넣고 예측값을 확인한다.

<리스트 6> predict 메소드에 샘플 입력

    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X, y)
    predicted_value = knn.predict(sample)
    print(iris.target_names[predicted_value])
    print(knn.predict_proba(sample))


결과는 다음과 같다.

    ['virginica']
    [[ 0.  0.  1.]]

virginica로 예측했다. 확률도 k가 1이기 없기 때문에 100%가 된다. 다음 코드 조각과 같이 k를 10으로, weight를 가중치가 같았던 기본 매개 변수인 'uniform'에서 거리에 따라 가중치를 더 부여하는 'distance'로 변경하고 실행해 보자.

<리스트 7> weight 변경 후 실행

    knn = KNeighborsClassifier(n_neighbors=10, weights='distance')
    knn.fit(X, y)
    predicted_value = knn.predict(sample)
    print(knn.predict_proba(sample))
    print(iris.target_names[predicted_value])


결과는 같지만 확률값이 다르다.

    ['virginica']
    [[ 0.          0.08888682  0.91111318]]

이번에도 virginica로 예측했고 확률적으로 versicolor는 약 9%이고, virginica는 약 91%가 되었다. versicolor보다 virginica 확률적으로 높기 때문에 virginica로 예측한다. 여기서는 예측값에 대한 정확도를 측정하지 않겠다(cross validation을 참고하자. 사실 정확도 측정은 매우 중요하지만 여기서 다루기가 쉽지 않다. 하지만 꼭 한번 살펴 보길 바란다). 

앞서 언급했듯이 기계 학습 알고리즘도 중요하지만 알고리즘의 매개 변수의 선택도 매우 중요하다. 매번 다른 매개 변수를 변경해서 넣어주기는 상당히 귀찮은 일이며, 데이터 클 경우 매번 오랜 시간을 기다려 다시 실행해 주기는 좀 부담스럽다. scikit-learn 라이브러리는 이 부분을 자동화 할 수 있도록 GridSearchCV 클래스를 제공한다. GridSearchCV의 매개 변수는 알고리즘과 알고리즘의 들어가는 매개 변수들이다. 다음 코드 조각은 k인 n_neighbors을 1, 3, 10로 설정하고 weights를 uniform, distance로 설정해 각각의 매개 변수 조합으로 최적의 매개 변수의 조건을 찾도록 한다.

<리스트 8> n_neighbors을 1,3,10으로 weight를 uniform, distance로 설정

    parameters = {'n_neighbors':(1, 3, 10), 'weights':('uniform', 'distance')}
    knn_base = KNeighborsClassifier()
    grid_search = GridSearchCV(knn_base, parameters)
    grid_search.fit(X, y)
    print(grid_search)
    print(grid_search.best_params_)
    print(grid_search.grid_scores_)


결과는 <리스트 9>와 같다.

<리스트 9> 결과

    {'n_neighbors': 3, 'weights': 'uniform'}
    [mean: 0.96000, std: 0.00000, params: {'n_neighbors': 1, 'weights': 'uniform'}, 
    mean: 0.96000, std: 0.00000, params: {'n_neighbors': 1, 'weights': 'distance'},
    mean: 0.96667, std: 0.01886, params: {'n_neighbors': 3, 'weights': 'uniform'},
    mean: 0.96667, std: 0.01886, params: {'n_neighbors': 3, 'weights': 'distance'},
    mean: 0.95333, std: 0.00943, params: {'n_neighbors': 10, 'weights': 'uniform'}, 
    mean: 0.96667, std: 0.02494, params: {'n_neighbors': 10, 'weights': 'distance'}]


n_neighbors가 3, weights가 'uniform'일 때 주어진 매개 변수 중에서 최적의 조건이 된다. 다른 조건에서 같은 결과가 나온다면 복잡도가 적은 매개 변수를 선택한다. {'n_neighbors': 3, 'weights': 'uniform'}과 {'n_neighbors': 3, 'weights': 'distance'} 조건일 때 같은 결과이지만 복잡도가 적은 전자로 최적의 조건을 찾았다. 

sample에 따라 예측값이 다르다. k가 1일때, k가 3, 10일때 각각 예측값이 다를 수 있으며, 알고리즘마다 예측값이 다를 수 있다. 그러므로 최적의 예측값을 얻기 위해서는 반드시 평가 단계를 거쳐야 한다.

# 더 읽어보기
scikit-learn의 좀 더 생산적인 기능은 pipeline과 라이브러리의 공통적인 인터페이스이다. pipeline은 기계 학습 알고리즘을 적용하기 전에 전처리와 같은 처리와 알고리즘이 수행하는 부분을 한번에 연결해서 구현할 수 있도록 한다. 예를 들어, iris 데이터의 차원을 줄여 기계 학습 알고리즘에 적용할 수도 있다. 차원의 저주라는 말이 있듯이 높은 차원은 좋은 결과를 주지 못하는 경우가 많다. pipeline을 사용하면 PCA(Principal Component Analysis, http://en.wikipedia.org/wiki/Principal_component_analysis)를 먼저 적용한 후 기계 학습 알고리즘을 바로 적용할 수 있다.

**내용을 제한합니다.**

# 결론
지금까지 기계학습과 파이썬으로 구현된 scikit-learn을 간략하게 살펴봤고 붓꽃 예제에 적용했다. 기계 학습에는 다양한 기법이 있고 여기에서 다루지 않은 적용된 기법에 대한 평가에 문제가 있다. scikit-learn은 문서화가 매우 잘 돼있어 기계 학습 기법을 학습한 후 scikit-learn 문서를 찾아 보면 그리 어렵지 않게 실제 문제에 적용할 수 있다. 마지막으로 실행 가능한 소스는 https://github.com/brenden17/iris에서 볼 수 있다.

# 참고자료
 * http://scikit-learn.org/stable/
 * http://www.scipy.org/
 * http://www.acornpub.co.kr/book/machine-learning-python
 * https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/neighbors/classification.py
 * http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
 * http://ko.wikipedia.org/wiki/주성분_분석

