a
Detecting Outlier-1
sklearn, pandas, outlier, DBSCAN
이상치 검출(Outlier detection)은 [imbalanced data](http://cohesive-beach-456.appspot.com/page/5144752345317376)와 매우 유사한 형태라고 할 수 있다.
이상치는 대부분 데이터와 다른 형태를 띄고 있고 매우 소수이다.
좀 더 살펴보기 전에 몇가지 정의를 보도록 하자.

Novelty Detection
> The training data is not polluted outliers, and we are interested in detecting
> anomalies in new observations

Outlier Detection
> The training data contains outliers, and we need to fit the central
> mode of the training data, ignoring the deviant obserations

결국, Novelty Detection은 훈련 데이터에 이상치가 있지 않고 새로운 데이터에서 이상치를 검출한다.
반면, Outlier Detection은 훈련 데이터에 이상치가 포함되어 있다.

[yhat](http://yhathq.com/)의 [Detecting Outlier Car Prices on the Web](http://blog.yhathq.com/posts/detecting-outlier-car-prices-on-the-web.html)을 보면 LinearRegression을 사용하여 이상치를 검출한다.

이상치는 결국 주요 데이터와 다른 데이터이기 때문에 [DBSCAN](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)을 사용하여 그룹화 되지 못한 데이터를 이상치로 간주할 수 있을 듯 하다.

다음은 DBSCAN로 그룹화하는 부분인데 가장 중요한 파라미터는 eps=param.eps, min_samples=param.min_samples이다.

    Param = namedtuple('Param', ['eps', 'min_samples'])
    param = Param(1.20, 5)
    dbscan = DBSCAN(eps=param.eps, min_samples=param.min_samples).fit(X.values)
    labels = dbscan.labels_
    unique_labels = set(labels)
    for k in unique_labels:
        for index in np.argwhere(labels == k):
            # print k, index
            col = 'r' if k == -1 else 'b'
            ax.scatter(df.mileage[index], df.trim_encode[index], df.price[index], c=col)
    ax.set_xlabel('Mileage')
    ax.set_ylabel('Transmission')
    ax.set_zlabel('Price')
    plt.show()

훈련 데이터에서 최적의 매개 변수를 찾는다면 실제 데이터에 적용하여 이상치를 검출할 수 있을 듯 하다.

    https://github.com/brenden17/detecting-outlier  

다음은 one class svm, elliptic envelope를 사용해 보도록 하겠다.