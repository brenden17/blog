a
If you ask, inspect module can answer
python
When you get an object, you might wonder what it is. First off, you can ask whether isfunction or isclass. If it is function, what are arguments? 

    #target function
    def read(arg1, arg2='math'):
        print(arg1, arg2)
    import inspect
    if inspect.isfunction(read):
        arg_spec = inspect.getargspec(read)
        print('name    :', arg_spec[0])
        print('*       :', arg_spec[1])
        print('**      :', arg_spec[2])
        print('defaults:', arg_spec[3])
        
Also, you can check Class Hierachies with getclasstree() and getmro().
When I create new class, I wonder what is different between using type function and declare class. I assume that one of then has less method.

    from inspect from getmembers
    class X(object):
        """declare X class"""
        x = 1
    
    y = type('Y', (objects,'), {'__doc__':"created by type", 'x':1})
    
    print(getmembers(X))
    print(getmembers(y))

Both of them are exactly the same. Two class objects have the same methods.
However, I know the process of creation is a little bit different. Which means, when you declare class and then create, X class calls type.__new__(), type.__init__(). On the other hand, type function does not calls type.__init__().

Inspect module is like an oracle.