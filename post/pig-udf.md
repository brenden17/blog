work
python으로 pig의 UDF 만들기
hadoop, pig, udf
pig을 가지고 놀다 보면 어떻게 데이터를 처리할 수 있을까하는 생각이 든다.
물론, 다양한 기본 함수를 제공하고 있지만 부족하다. 이럴 경우을 대비해 pig는 사용자가 만들어 사용할 수 있는 기능인 [User Defined Function](http://pig.apache.org/docs/r0.12.0/udf.html)을 제공한다.
당연히 자바로 만들어야 하겠지라고 생각했지만 다양한 언어로 구현할 수 있다. 파이썬도 예외가 아니다.
사용법도 너무나 간단하다. 하지만 jython을 사용하고 있기 때문에 3.x는 지원이 안되고 웹에서 보니 특히 json을 사용할 때 문제가 되는 듯 하다.

먼저, udf로 사용할 파이썬 코드를 만든다. 여기서는 util.py으로 한다.
get_length함수로 제목의 글자수를 반환한다. 반환할 때 반환되는 타입을 명시해야한다.


    @outputSchema('num:long')
    def get_length(name):
        return len(name) 

그리고 실제 사용할 pig 코드에서 REGISTER만 해 주고 함수를 호출하면 된다.

    REGISTER 'util.py' USING jython as util
    movies = LOAD '/input/movie/movies_with_duplicates.csv' USING PigStorage(',') as (id:int, name:chararray, year:int, rating:double, duration:int);
    count_movie_name = FOREACH movies GENERATE util.get_length(name);
    DUMP count_movie_name;

매우 간단하지만 강력한 기능을 제공한다.

    https://github.com/brenden17/pig-farmer/tree/master/python-udf
