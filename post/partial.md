work
Currying에서 온 그대, partial
python, math, 
파이썬은 다중 파라다임 언어이다. 이 말은 어떤 문제를 명령형(Imperative)으로 해결할 수도 있으며,
객체지향(Objective)으로 해결할 수도 있고, 함수형(Functional)으로 해결할 수 있다는 뜻이다.
그러면 어떠한 함수와 특징이 파이썬을 함수형 언어라고 하는지 살펴보도록 한다.

## partial 함수
함수적 특징을 가진 가장 기본적인 map, reduce, filter와 같은 함수 이외에 
[partial](https://docs.python.org/2.7/library/functools.html#functools.partial) 함수가 있다.
partial 함수는 함수형 언어의 특징을 아주 잘 나타낸다.

아래의 함수는 간단하게 두 수를 더하여 반환하는 add 함수이다.
이 함수를 정의하고 partial 함수에 첫 번째 매개변수로 넣고 
두 번째 매개 변수로는 add 함수의 매개변수로 들어갈 값을 넣고 add_one으로 반환받는다.
add_one의 매개 변수에 add 함수에 들어가 나머지 매개 변수를 넣고 실행하면
add 함수가 실행한 결과와 같은 결과가 된다.

    from functools import partial
    def add(a, b):
        """Add a to b"""
        return a + b
    add_one = partial(add, 1)
    add_one(10)

이로써 단순하게는 함수를 재사용할 수 있으며 새로운 함수를 정의하여 가독성을 높일 수 있는 장점이 있을 수 있다.
그러면 partial 함수는 어디서 왔을까? 필요하기 때문에 만들었을 수도 있지만 어디서 사용되어 왔을 수도 있다.

## 종의 기원
* 기계의 메모리가 충분하고 CPU가 강력하다면 이 세상에 모든 문제를 해결할 수 있을까? 
* 기계가 계산할 수 있는 능력은 어디까지 일까?
* 계산이란 무엇일까?

이러한 문제는 수십년전 논리 수학자나 수학자들의 문제이기도 했다.
[힐베르트의 23문제](http://ko.wikipedia.org/wiki/%ED%9E%90%EB%B2%A0%EB%A5%B4%ED%8A%B8%EC%9D%98_%EB%AC%B8%EC%A0%9C%EB%93%A4)중 1, 2번 문제에 대해 
많은 수학자들이 도전하였고 증명의 문제를 넘어 계산가능의 문제로 확대하였다.  

튜링과 다른 방법으로 [처치](http://ko.wikipedia.org/wiki/%EC%95%8C%EB%A1%A0%EC%A1%B0_%EC%B2%98%EC%B9%98)는 
[람다 계산법](http://en.wikipedia.org/wiki/Lambda_calculus)(Lambda calculus)을 만들어 계산이란 문제를 연구하였다.
처치는 아래와 같은 계산 과정에서 이름없는(익명성) 함수를 만들었고 이것이 파이썬의 partial 함수의 기원이 된다.  
 
    sum(x, y) = x * x + y * y
    (x, y) -> x * x + y * y
    x -> (y -> x * x + y * y) # currying

함수형 언어의 특징인 [1차 논리](http://ko.wikipedia.org/wiki/1%EC%B0%A8_%EB%85%BC%EB%A6%AC)(first-order logic)도 잘 보여준다.
참고로, 프로그램 언어의 특징을 구별하는 [first class citizen](http://en.wikipedia.org/wiki/First-class_citizen)를 보면 재미있다.

## 진화
사실, 파이썬에서 partial 함수의 반환값은 partial 객체이다. 
그래서 partial 객체는 원함수(예제의 add 함수)의 메타정보를 가지 않는 불편함이 생긴다.
아래와 같이 이전에 정의한 add_one 함수의 메타 정보를 호출하면 오류가 뱔생한다.
   
    >>> add.__name__
    >>> add.__doc__
    >>> add_one.__name__ #오류
    >>> add_one.__doc__ #오류
    >>> add_one

이러한 문제를 해결하기 위해 파이썬은 update_wrapper 함수를 제공한다.
아래와 같이 update_wrapper 함수를 사용하면 원함수의 메타정보를 그대로 사용할 수 있다.

    from functools import update_wrapper
    update_wapper(add_one, add)
    add_one.__name__
    add_one.__doc__

사실, decorator에도 같은 문제가 있으며 wraps 함수를 사용하면 이또한 해결할 수 있다.

    def my_decorator(f):
        @wraps(f)
    	def wrapper(*args, **kwarg):
    		return f(*args, **kwarg)
    	return wrapper
    
    @my_decorator
    def example():
        """doc of example"""
    	return 1
    	
    example.__name__
    example.__doc__

## 결론
지금까지 파이썬 partial 함수로 함수형 언어의 기원과 특징은 아주 간략하게 보았다.
파이썬은 사용하기에 따라 매우 쉬운 언어이기도 하지만 매우 심도있는 언어이기도 하다(다른 언어도 그렇지만). 
같은 문제를 다양한 해결법으로 해결할 수 있는 재미있는 언어이다.