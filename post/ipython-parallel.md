a
sklearn의 GridSearch를 ipython parallel로 실행하기
ipython, sklearn
sklearn을 사용할 때, 실험 데이터가 커지거나 특히, 적용하고자 하는 파라미터가 많을 때 시간이 많이 걸린다. 이런 문제를 해결하기 [starcluster](http://star.mit.edu/cluster/)와 같은 병렬처리로 속도를 낼 수 있다.
Ipython도 병렬처리를 지원하다. cpu로 개수로 process를 관리할 수 있는 장점이 있다.
sklearn의 GridSearchCV를 BaseSearchCV를 상속받아 구현했다.
다음은 소스를 참고한다.

    https://github.com/brenden17/IPyGridSearchCV    
