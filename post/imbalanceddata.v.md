scikit-learn, machine learning
imbalanced data 처리하기
pandas, undersampling, oversampling
# 개요

훈련 데이터의 불균형은 기계 학습 알고리즘을 제대로 훈련할 수 없게 한다.
사기적발이나 불균형한 단백질 구조에서 서열 규칙을 찾아내는 사례가 대표적이다.
대표적인 해결 방안으로 크게 두가지를 들 수 있다. 

* 표본 추출(sampling)
* 오분류 비용(misclassification cost)

먼저, 표본 추출을 간략하게 보자면 

* 소수 범주와 균형을 이루도록 과소 표본 추출하는 방법(undersampling)
* 소수 범주를 반복적으로 복사하여 데이터 수를 늘리는 과대 표본 추출하는 방법(oversampling)

과대 표본 추출의 경우 데이터 수가 증가하기 때문에 훈련 시간이나 복잡도는 증가한다.
뿐만 아니라 단순히 소수 범주를 복사해서 늘리는 방법은 효과가 미비하다. 
그래서 단순 반복이 아닌 KNN을 통해 주변 인공 데이터를 생성하는 **SMOTE(Synthetic Minority Oversampling TEchnique)**는 가장 기본적인 해결 방안이다.

다른 방법인 오분류 비용은 원본 데이터를 그대로 유지하면서 소수 범주 오분류에 가중치를 주어 데이터의 불균형을 해소하는 방법이다.
의사 결정 나무나 로지스틱 회귀분석에서 목표 변수에 가중치를 다르게 준다.


# 간단한 구현

간단하게 구현해 보자.
먼저, 사용할 데이터를 정해 보자. 데이터는 [http://archive.ics.uci.edu/ml/datasets/Balance+Scale](http://archive.ics.uci.edu/ml/datasets/Balance+Scale)에서 구하도록 한다.
데이터의 구성 비율을 먼저 체크해 보자.

    def read_file():
        return pd.read_csv(get_fullpath('balance-scale.data'), delimiter=',',
                       names=['class', 'lweight', 'ldist', 'rweight', 'rdist'])

    def analysis_data():
        df = read_file()
        X_outlier = df[df['class'] == 'B'] # .ix[idx]
        X_train = df[df['class'] == 'L']
    
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter(X_outlier['lweight'], X_outlier['ldist'],
                   X_outlier['rweight'], c='r')
        ax.scatter(X_train['lweight'], X_train['ldist'],
                   X_train['rweight'], c='b')
        ax.set_xlabel('left weight')
        ax.set_ylabel('left dist')
        ax.set_zlabel('right weight')
        plt.show()
    
Class B가 다른 범주보다 1/6정도 작다. 이정도면 괜찮을 듯 하다. 그리고 기본적으로 데이터는 무작위로 구성되어 있다.
3가지 방법으로 표본화 한 후, Ensemble Tree, SVM, Logistic Regression으로 평가하고자 한다.

# 과소 표본 추출(undersampling)

    def load_undersampling():
        rawdata = read_file()
        n_sample = rawdata[rawdata['class'] == 'B'].shape[0]
        B = rawdata[rawdata['class'] == 'B']
        L = rawdata[rawdata['class'] == 'L'][:n_sample]
        R = rawdata[rawdata['class'] == 'R'][:n_sample]
        d = pd. concat([B, L, R])
        le = LabelEncoder()
        X = d.icol(range(1, 5)).values
        y = le.fit_transform(d['B'].values)
        return X, y

        
## SMOTE(Synthetic Minority Oversampling TEchnique)

    def load_data_with_SMOTE():
        rawdata = read_file()
        size = 150
        small = rawdata[rawdata['class'] == 'B']
        n_sample = small.shape[0]
        idx = np.random.randint(0, n_sample, size)
        X = small.iloc[idx, range(1, 5)].values
        y = small.iloc[idx, 0].values
        knn = NearestNeighbors(n_neighbors=2)
        knn.fit(X)
        d, i = knn.kneighbors(X)
        idx2 = i[:, 1]
        diff = X - X[idx2]
        X = X + np.random.random(4) * diff
        B = np.concatenate([np.transpose(y[np.newaxis]), X], axis=1)
        B = pd.DataFrame(B)
    
        n_sample = rawdata[rawdata['class'] == 'L'].shape[0]
        idx = np.random.randint(0, n_sample, size)
        L = rawdata[rawdata['class'] == 'L'].iloc[idx]


## 과표본화 기반 앙상블

마지막으로 **[과표본화 기반 앙상블](http://bi.snu.ac.kr/Publications/Conferences/Domestic/KIISE2013f_KMKim.pdf)** 논문을 기반으로 데이터를 구성한다.
200번 복원 추출한다.

    def load_sampling():
        size = 200
        rawdata = read_file()
        n_sample = rawdata[rawdata['class'] == 'B'].shape[0]
        idx = np.random.randint(0, n_sample, size)
        B = rawdata[rawdata['class'] == 'B'].iloc[idx]
    
        n_sample = rawdata[rawdata['class'] == 'L'].shape[0]
        idx = np.random.randint(0, n_sample, size)
        L = rawdata[rawdata['class'] == 'L'].iloc[idx]
    
        n_sample = rawdata[rawdata['class'] == 'R'].shape[0]
        idx = np.random.randint(0, n_sample, size)
        R = rawdata[rawdata['class'] == 'R'].iloc[idx]
    
        df = pd.concat([B, L, R])
    
        le = LabelEncoder()
        X = df.icol(range(1, 5)).values
        y = le.fit_transform(df['class'].values)
        return X, y


## 평가 기계 학습 알고리즘
이렇게 데이터를 각각 구성한 후, 다른 3개 기계 학습 알고리즘으로 평가한다.

    def create_learners():
        return [ExtraTreesClassifier(), SVC(), LogisticRegression()]


# 평가
자, 최종 평가를 실시한다. 알고리즘의 파라미터는 기본으로 한다.

어떤 데이터가 가장 좋은 결과를 내었을까?

 **과표본화 기반 앙상블**이 가장 좋은 결과를 만든다.

전체적으로 다음 소스를 참고한다.

    https://github.com/brenden17/imbalanced-data
 
 