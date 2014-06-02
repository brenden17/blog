scikit-learn, outlier, machine learning
Detecting Outlier-2
pandas, elliptic envelop, one class svm

[Detecting Outlier-1](/page/Detecting Outlier-1)에서 구별한 novelty와 outlier를 간략하게 다시 보면
novelty deteciton는 unsupervised 학습 방법이며, 훈련 데이터에 이상치는 없는 반면, 
outlier detecion은 훈련 데이터에 이상치가 포함되어 있다.
novelty deteciton의 대표적인 방법은 [One class SVM](http://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html)이다.
outlier detecion의 대표적인 방법은 [Elliptic evnvelop](http://scikit-learn.org/stable/modules/generated/sklearn.covariance.EllipticEnvelope.html)이다.

sklearn에서는 novelty와 outlier을 검출하는 기계 학습 도구를 제공한다.
공통적으로 다음과 같이 사용한다.

    estimator.fix(x_train)
    estimator.precit(x_test)

우선, 데이터의 특성을 살펴보아야 한다. 데이터가 정규 분포를 따른다면 One Class SVM을 사용하고 정규 분포가 아니라면,
robust esitmator 방법인 Elliptic envelop을 사용한다.

* 일변량 - 표준 점수(z-score)를 사용하여 표본을 찾는다.
* 이변량 - 독립 변수와 종속 변수의 관계성 테스트하여 특정 신뢰구간에 포함하지 않은 표본을 찾는다.
* 다변량 - 마할로노비스을 사용하여 표본을 찾는다.

One Class SVM은 classification, regression에 사용하는 SVM의 한 분야이다. 다른 SVM 기법과 마찬가지로,
커널 함수와 마진(margin)을 매개 변수로 정의 할 수 있다.
