machine learning
유사도 측정
distance, similarity
# 유사도 측정
한 개체와 다른 개체가 비슷한 것을 어떻게 평가할 수 있을까?
친구들과 모여 본 영화를 이야기 할 때 나와 본 영화가 가장 겹치는 친구가 내 성향과 가장 비슷할 테고
그 친구가 추천한 영화를 보면 후회하지 않을 수 있다.
또한, 인터넷 서점에서 나와 책을 가장 비슷하게 산 사람의 책 목록을 보면 내가 좋아할 만한 책을 알 수 있을 테다.
이러한 경우가 일차원 변수를 가지는 경우이다.
하지만, 개체가 여러 특성을 가진다면 어떨까?
음식을 설탕량, 소금량, 수분량, 고추가루량등으로 나누고 각기 다른 음식과 유사한 음식을 찾을 수도 있다.
영화별로 별점을 주는 경우도 그렇다.
이러한 경우가 다차원 변수를 가지게 된다.

다음과 같이 다양한 방법으로 차원별 유사도를 측정할 수 있다.

## 1차원 변수의 유사도
1차원 변수일 경우 몇가지 방법으로 값을 얻을 수 있다. 
각 공식은 상당히 간단하기 때문에 python 코드로 대신하고자 한다.

### 타니모토 계수(Tanimoto's coefficient)
IBM 수학자인 타니모토가 세균 분류를 위해 개발되었다.

    def tanimoto(s1, s2):
        c = len(set(s1)&set(s2))
        return float(c) / (len(s1) + len(s2) - c)

### 다이스 계수(Dice's coefficient)

    def dice(s1, s2):
        c = len(set(s1)&set(s2))
        return float(2 * c) / (len(s1) + len(s2))

### 자카드 계수(Jaccard's coefficient)

    def jaccard(s1, s2):
        c = len(set(s1)&set(s2))
        return float(c) / (len(set(s1)|set(s2))
        
## 다차원 변수의 유사도
다차원 변수의 유사도는 두 개체의 거리를 통해 알 수 있다.

### 유클리디안 거리(Euclidean distance)

    def euclidean(p, q):
        dist = sum([(p(i)-q(i))**2 for i in range(len(p))])
        return dist**0.5

### 피어슨 상관계수(Pearson correlation coefficient)

    def pearson(x,y):
        vals = range(len(x))
         
        sumx = sum([float(x[i]) for i in vals])
        sumy = sum([float(y[i]) for i in vals])
         
        sumx_sq = sum([x[i]**2.0 for i in vals])
        sumy_sq = sum([y[i]**2.0 for i in vals])
         
        #sum of the products
        p_sum = sum([x[i]*y[i] for i in vals])
         
        num = p_sum - (sumx * sumy / n)
        den = ((sumx_sq - pow(sumx, 2) / n) * (sumy_sq - pow(sumy, 2)) ** 0.5
        return 1 if den == 0 else num / den

## 결론
추천 시스템이나 군집화등 다양한 영역에서 유사도는 사용되고 있다.
그만큼 다양한 측정법이 있으니 각 시스템의 특성이 맞게 사용하면 좀 더 나은 결과를 얻는다.
 