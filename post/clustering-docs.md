work
문서 군집화
sklearn, gensim, clustering, nlp, nmp
# 문서 군집화
## Non-negative matrix factorization
비음수 행렬 인수분해(NMF, Non-negative matrix factorization)는 
다변향 분석(multivariate analysis) 알고리즘으로 음수가 없는 하나의 행렬을 두 개의 음수가 없는 행렬로
분해한다. PCA(Principle Component Analysis)와 유사하지만 음수가 없다는 점이 가장 큰 차이점이다.
이 차이점으로 분해된 두 행렬 중에 기저 행렬의 원소들을 더하여 원래의 행렬과 **유사하게** 표현할 수 있다. 
NMF는 이미지 등의 패턴 학습과 패턴 인식에 우수한 성능을 보인다. 특히 다수의 입력 데이터에서 최적의
기초 패턴을 분리하여 이들의 선형 조합으로 전체 데이터를 근사할 수 있기 때문에 데이터 특징 추출에 유용하다.

## scikit-learn 라이브러리
NMF를 활용하기 위해 [scikit-learn](http://scikit-learn.org) 라이브러리를 사용하고자 한다. 
scikit-learn는 파이썬으로 구현된 기계 학습 라이브러리로 다양한 기계 학습의 알고리즘을 제공한다.
다음과 같이 라이브러리를 설치 할 수 있다.

> pip install -U scikit-learn

## 데이터 구하기
지금부터 NMF를 활용하여 전직 대통령 연설을 군집화하도록 하겠다.
NMF을 활용하여 성향이 다른 두 전현직 대통령의 연설의 특징을 찾아 군집화한 다음, 군집화 된 연설이 잘 군집화 되었는지 살펴보자.
두 대통령의 연설(데이터)은 [노무현 대통령 홈페이지](http://archives.knowhow.or.kr/archives/index.php?bId=437&speechId=747)와 [청와대 홈페이지](http://www1.president.go.kr/president/speech.php)에서 구할 수 있다.
간단히 테스트를 하기 위해 각각 3개의 연설을 먼저 해 보도록 한다(데이터가 매우 적다. 하지만 진행하는 방법으로 데이터는 계속 만들 수 있다).
웹에서 구한 연설을 txt 파일로 저장한다. 하지만 이 문서를 그대로 사용할 수 없기 때문에 다른 작업이 필요하다.

### 형태소 분석
우리가 사용하는 자연어는 다양한 품사가 사용되며 모든 품사로 분석할 수도 있지만 여기서는 가장 의미있는 명사만 추출하고자 한다.
이를 위해 [형태소 분석](http://ko.wikipedia.org/wiki/%EC%9E%90%EC%97%B0_%EC%96%B8%EC%96%B4_%EC%B2%98%EB%A6%AC)을 해야한다.
(아래 github의 /data/*.txt는 원연설 문서이고 /data/*_noun.txt는 형태소 분석한 후 명사를 추출한 문서이다.)
    
### 벡터화
문서를 행렬로 만들어 다룰 수 있도록 변환하도록 하자. 이러한 변환을 하기 위해 단어 주머니([bag-of-words model](http://en.wikipedia.org/wiki/Bag_of_words)) 접근법을 사용한다.
연설에 출현한 모든 단어를 세어 벡터로 나타낸다. 즉, 형태소 분석을 한 후 명사로 구성된 문서에서 출현된 단어를 세어 각 문서로 적는다.
이때, 각 문서에 출현된 단어는 문서마다 크게 다를 수 있기 때문에 [희소 행렬](http://ko.wikipedia.org/wiki/%ED%9D%AC%EC%86%8C%ED%96%89%EB%A0%AC)을 사용하는 것이 좋다.
이렇게 하여 문서를 우리가 다를 수 있는 행렬로 표현했다.
하지만 결론부터 말해, 이 행렬로 계산하는 것보다 좀 더 좋은 결과를 얻을 수 있게 한번 더 처리를 할 수 있다.
이 과정은 단어가 특정 문서에서 얼마나 중요한가를 측정하는 [TF-IDF](http://ko.wikipedia.org/wiki/TF-IDF)(Term Frequency - Inverse Document Frequency)이다.
이로써, 각 단어의 중요도를 행렬을 만들어 정확도를 높일 수 있다.
scikit-learn을 사용하면 상당히 간단하게 구현할 수 있다.

    vectorizer = CountVectorizer(max_df=10, min_df=2)
    counts = vectorizer.fit_transform(data)
    tfidf = TfidfTransformer().fit_transform(counts)

## 데이터에 NMF 적용하기
scikit-learn은 NMF를 지원하여 사용법도 간단하다. 
벡터화 한 데이터를 입력하고 군집화 할 개수를 n_components로 설정한다. 

    nmf = decomposition.NMF(n_components=2).fit(tfidf)
    feature_names = vectorizer.get_feature_names()

결과는 다음과 같다.

> Topic #0:
> 국민 우리 평화 동북아 북한 여러분 한반도 시대 세계 역사 정부 사회 문화 신뢰 경제 여러 민국 대한 협력 정치 대화 오늘 나라 활력 존경 도전 번영 올해 진정 과거 위대 마음 미래 남북관계 남북한 노력 저력 문제 비롯 극복 대통령 지속 국제 국가 최선 감사 원칙 지혜 자랑 타협 행복 적극 사람 지난해 안보 과제 기회 어려움 여정 내수 해결 하나 개혁 건강 발전 시작 용기 희망 실행 혼란 수립 기록 회복 고통 중국 분단 동참 로운 계기 정책 추진 청산 하기 농어민 성찰 지역구 전기 우려 바다 민주주의 정치권 안정 변화 수출 정착 성과 자리 환경 이후

> Topic #1:
> 경제 확대 우리 규제 국민 혁신 정부 투자 참여 창조 강화 추진 지원 국회 세계 fta 노력 시장 법안 한국 사업 수출 일자리 해서 투명 제도 도입 여러 민간 변화 문제 관행 해결 중심 전략 내년 통과 활성화 공공기관 전환 창업 지방 분야 확충 지역 발전 모두 청년 성장 적극 행복 문화 투명성 산업 개혁 경영 극복 생각 속도 국가 아이디어 관련 가계부채 고용 개방 기초 내수 제조업 마련 사회 북핵문제 중요 확신 중소기업 재정 규모 국내 창출 경쟁력 비정상 체제 안정 지속 기업 수준 지금 방향 시스템 구축 주택 국제 대비 사회안전 개선 대기업 회의 진행 체결 획기적


## 결과
총 6개 문서를 2개 그룹으로 군집화하면 4개 연설은 정확하게 지정하는 반면 2개 연설은 잘못 지정한다.
NMF을 하는 데이터에는 관련 정보가 없지만 우리는 처음부터 연설한 대통령을 알고 있기 때문에 결과를 비교 할 수 있다.
2개 문서가 잘못된 이유를 찾자면, 하나는 문서 즉 연설 개수가 너무 적다는 점이다.
좀 더 많은 총단어 수를 가진다면 특성을 좀 더 잘 뽑아 낼 수 있을 수 있다. 
다른 하나는 2개의 문서가 정말 다른 특성을 가질 수 있다. 왜냐하면 정치인의 연설은 특정 시기나 특정 문제에 대해 같은 목소리를 낼 수 있기 때문이다.
NMF을 활용한 문서 군집화는 점차 데이터가 많아지기 때문에 사용할 수 있는 범위도 계속 늘어나고 있다.

이와 더불어, KMeans나 [LSI](http://en.wikipedia.org/wiki/Latent_semantic_indexing)을 사용해도 재미있는 결과를 얻을 수 있다.
작동하는 코드는 다음 https://github.com/brenden17/clustring-docs에서 구할 수 있다.
