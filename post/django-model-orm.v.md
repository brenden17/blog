django
Django의 model를 standalone으로 사용하기
model
장고(Django)의 여러 장점중 가장 좋아하는 장점은 모델 부분이다.
조금만 보더라도(django debug toolbar를 사용해서 보면) 장고의 ORM은 얼마나 자동으로 쓸모없는 코드를 만들어 내는지 알 수 있고 좀 복잡한 query를 만들려면 그 한계가 있다는 점을 쉽게 알 수 있다. 하지만 복잡한 관계를 만들기 보다는 간단하고 단순한 데이터베이스를 만들 때 그만큼 편한 것도 없다.

데이터베이스를 사용할 기회가 있으면 잠깐 고민을 하는데 그냥 날코딩을 할건지 아니면 장고의 모델을 가져다 쓸건지...
가끔 있지만 이럴 때를 위해 좀 찾아보니 manage.py만 살짝 변경해 주면 된다.
아예 하나의 프로젝트로 만들었다.

    https://github.com/brenden17/infinity/tree/master/test/django-model-standalone

만들고 막상 사용할 기회가 있어 사용하려고 하니 아예 mongodb로 하는 것이 여러가지로 편해 mongodb를 사용했다는...

