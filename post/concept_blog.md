work, blog
블로그 구성
gae, python, flask, blog, aws
블로그는 다음과 같이 되어있다.

* [Google App Engine](https://developers.google.com/appengine/)
* [Flask](http://flask.pocoo.org/)

Google App Engine을 선택한 이유는 이용도가 낮으면 무료라는 점이다. 거의 나만 사용하니 무료임은 틀림없고 맘대로 개발만 하면 된다. 다른 조건은 다 구글에서 해 주니 다른 걱정을 하지 않아도 된다.
더 큰 이유는 최근에 AWS 사용하다 요금 폭탄을 맞았다. 가입 1년동안 무료이기 때문에 잘못 관리했다가는 완전 폭탄 맞는다.

[Flask](https://developers.google.com/appengine/?hl=da)를 선택한 이유는 요즘에 Django를 잘 지원하기 때문에 별 문제 없이 장고를 사용할 수 있을 것 같으나 중요한 부분이 데이터베이스 부분인데 아무리 장고를 사용한다고 해도 data store를 사용해야 한다는 점이다.
그래서 가벼운 Flask를 선택했는데 대만족이다. Jinja2를 사용하기 때문에 template쪽은 똑같이 사용할 수 있다.
이전에 말한대로 웹에서 직접 포스트를 입력하는 방식이 아니라 form도 사용하지 않고 로그인 기능도 필요가 없기 때문에 제격이다.
그럼 포스트는 어떻게 입력하는가?
[Remote API](https://developers.google.com/appengine/docs/python/tools/remoteapi)를 사용하여 로컬 문서를 직접 서버에 입력하는 방식이 된다.
markdown형식 문서를 직접 서버에 저장하여 서버에서 html로 출력하도록 되어있다.
