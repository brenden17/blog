a
Speed up with readlines
python
You might get the idea as you compare between readline and readlines. 
It might make your code speed up more 3 times.

    with open(filename) as f:
        while True:
            lines = f.readlines(1000) #buffer size
            if not lines:
                break
            for line in lines:
                #code