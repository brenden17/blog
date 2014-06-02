python, natural language processing
파이썬 한국어 형태소 분석기
pyhannanum, pos, tagger
자연어 처리를 하고자 할 때, 때때로 형태소 분석기가 필요하다.

몇몇 공개된 형태소 분석기가 있지만 막상 파이썬으로 작업하려면 만만치 않다.
그래서 파이썬에서 작업할 수 있도록 [한나눔](http://kldp.net/projects/hannanum/)을 바인딩하였다.
자바 클래스를 파이썬에서 접근하려면 Jython을 사용하는 방법이 있는데 Jython은 생각보다 무겁고 이 작업만을 위해 사용하기도 영 석연치 않다.
그래서 [Pyjninus](http://pyjnius.readthedocs.org/en/latest/)를 사용했다.
완성도 높은 패키지 같지는 않지만 사용하기엔 충분하다.
다음 git 저장소을 참고한다. 완성도는 높지 않지만 약간씩 변경해서 하면된다.

    https://github.com/brenden17/pyHannanum



자바 클래스를 사용해야 하기 때문에 jar, data와 같은 레벨에서 실행한다.
pyHannanum/convert.py을 적절히 변경한다.