work
pig 사용하기
hadoop, pig
비정형 데이터에서 간단한 정보를 얻기 위해 자바 소스를 작성하는 건 약간은 귀찮은 일이다.
그렇다고 stream을 이용할 요량으로 파이썬 코드를 작성하면 성능 저하가 생기니 고려 사항에서 벗어난다.
[pig](http://wiki.apache.org/pig/)를 사용해 보자. 
Yahoo에서도 약 20%는 pig를 사용하여 작업한다고 하니 간단한 작업에는 적당할 듯 하다.
데이터베이스 query와 비슷하여 각 operation을 비교적 쉽게 알 수 있다.

함수 정리 
 
 * [wiki](http://wiki.apache.org/pig/PigLatin)
 * [apache](http://pig.apache.org/docs/r0.12.0/func.html) 

# LOAD
데이터 로드하기

    grunt> movies = LOAD '/input/movie/movies_data.csv' USING PigStorage(',') as (id:int, name:chararray, year:int, rating:double, duration:int);

열 이름 옆에 타입을 명시하면 차후 type casting할 필요가 없다. 

# FILTER
필요한 정보만 걸러내기
    
    grunt> movies_between_50_60 = FILTER movies by year>1950 and year<1960;
    grunt> movies_between_50_60_starting_with_a = FILTER movies_between_50_60 by name matches 'A.*';

# FOREACH
각 열을 처리하기 위해 사용. 열을 걸러낼 수도 있음

    grunt> movies_duration = FOREACH movies GENERATE name, (double)(duration/60);
    
# GROUP
하나 이상 열로 그룹화 할 수 있음

    grunt> grouped_by_year = GROUP movies BY year;
    grunt> count_by_year = FOREACH grouped_by_year GENERATE group, COUNT(movies);
    
# ORDER BY
순서화하기 

    grunt> desc_movies_by_year = ORDER movies BY year DESC;
    grunt> desc_movies_by_year = ORDER movies BY year ASC;

# DISTINCT
중복 제거하기

    grunt> movies = DISTINCT movies;
    
# LIMIT
필요한 개수만 가져오기

    grunt> top_10_movies = LIMIT movies 10;

# 아주 간단한 예제
별점을 많이 받은 영화 top 10을 구해보자.
    
    grunt> raw_dep_movies = LOAD '/input/movie/movies_data.csv' USING PigStorage(',') as (id:int, name:chararray, year:int, rating:double, duration:int);
    grunt> desc_movies_by_rating = ORDER raw_movies BY rating DESC;
    grunt> top10_movies = LIMIT desc_movies_by_rating 10;
