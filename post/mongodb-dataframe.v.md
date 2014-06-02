mongodb, pandas, data
mongodb 데이터를 pandas 데이터로 변환하기
python
mongodb를 사용하다 보면 pandas로 바로 가져와 작업해 보고 싶다는 생각이 가끔 들때가 있다.
아무리 데이터베이스가 좋다하더라도 메모리에 올려 작업하는 것보다 쉽지는 않기 때문이다.
데이터를 그때 그때 변환하는 방법도 좋지만 아예 처음부터 파이썬에서 mongodb 클래스를 선언할 때 관련 메쏘드를 넣으면 어떨까?

가장 먼저 고려할 사항은 클래스 이름과 실제 데이터베이스의 collection 이름의 차이이다. 보통 파이썬에서 클래스 이름은 다음과 같은 낙타명명법이다. 

    class MyFriendName:
        pass

하지만 mongodb에서 collection 이름은 my_friend_name으로 사용된다.
변환 함수를 우선 만든다.

    def convertname(name):
        newname = [name[0].lower()]
        A, Z = ord('A')-1, ord('Z')-1
        for c in name[1:]:
            if A < ord(c) < Z:
                c = '_' + c.lower()
            newname.append(c)
        return ''.join(newname)

그리고 메타 클래스 하나를 정의하여 클래스에 자동으로 관련 메쏘드가 생기도록 한다.


    class MetaMongoBase(type):
        def __new__(meta, classname, supers, classdict):
            if 'mongometa'in classdict:
                mongometa = classdict['mongometa']
                dbname = mongometa.get('dbname', None)
                o = mongometa.get('option', {})
                collection = convertname(classname)
                classdict['get_dataframe'] = lambda self:MongoHelper.get_dataframe(dbname, collection, o)
            return type.__new__(meta, classname, supers, classdict)

    class MongoBase(object):
        __metaclass__ = MetaMongoBase
        def __init__(self):
            pass

    class Year(MongoBase):
        mongometa = {'dbname':'yearlybalancedb', 'option':{'field':['dayat']}}
        #mongometa = {'dbname':'yearlybalancedb'}
        def __init__(self):
            pass

이렇게 하면 자동으로 선언한 클래스의 mongometa정보로 관련 메쏘드를 만든다.
그런데 사실, get_dataframe 메쏘드는 MongoHelper.get_dataframe 메쏘드이다.

    @staticmethod
    def get_collection(dbname, collection_name):
       try:
           conn = Connection()
           db = database.Database(conn, dbname)
           return db[collection_name]
       except Exception as e:
           print(str(e))

    @staticmethod
    def get_dataframe(dbname, collection_name, option={}):
       try:
           c = MongoHelper.get_collection(dbname, collection_name)
           return pd.DataFrame(list(c.find(**option)))
       except Exception as e:
           print(str(e))

mongodb에서 pandas의 dataframe으로 변환하는 핵심은 위 코드이다. 다른 코드는 좀 편한게 하는 코드일 뿐 변환하는 부분은 이게 전부이다.

전체 코드는 다음에서 볼 수 있다.

    https://github.com/brenden17/infinity/blob/master/test/mongoengine/common.py


