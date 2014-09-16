d3
Sankey Diagram 그리기
javascript, visualization 

# Sankey Diagram
Sankey Diagram은 흐름도(flow diagram)의 일종으로, 시스템에서 에너지나 물질의 양이 어떻게 이동하는지를 나타낸다. 화살표의 방향은 이동 방향이며, 굵기는 대상의 양이 된다. 대표적인 사용예는 1812년 나폴레옹이 러시아로 진군하면서 변화된 군사 수를 도표화한 것이다.

![Alt text](http://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Minard.png/400px-Minard.png "Sankey Diagram") 
출처 : [wikipedia](http://en.wikipedia.org/wiki/Sankey_diagram)

좀 더 다양한 sankey diagram은 http://www.sankey-diagrams.com/에서 볼 수 있다.

# D3.js로 Sankey Diagram 그리기
D3.js에 관해 무료로 볼 수 있는 책 [D3 Tips and Tricks](https://leanpub.com/D3-Tips-and-Tricks)에서 sankey diagram을 그릴 수 있는 함수를 만들어 놓아 그리 어렵지 않게 사용할 수 있다. 지금 그리고자 하는 데이터는 [지구의 물 비율](http://water.usgs.gov/edu/watercyclekoreanhi.html)이다. 지구의 물은 97%로 바닷물이 절대적 많아 그대로 그린다면 다른 물의 양은 거의 보이지 않기 때문에 다음과 같이 변경하였다.

    {
    "nodes":[
    {"node":0,"name":"지구의 물"},
    {"node":1,"name":"민물"},
    {"node":2,"name":"바닷물"},
    {"node":3,"name":"기타"},
    {"node":4,"name":"지표수"},
    {"node":5,"name":"지하수"},
    {"node":6,"name":"빙하"},
    {"node":7,"name":"강"},
    {"node":8,"name":"늪지"},
    {"node":9,"name":"호수"}
    ],
    "links":[
    {"source":0,"target":1,"value":300},
    {"source":0,"target":2,"value":670},
    {"source":1,"target":3,"value":20},
    {"source":1,"target":4,"value":110},
    {"source":1,"target":5,"value":100},
    {"source":1,"target":6,"value":180},
    {"source":4,"target":7,"value":10},
    {"source":4,"target":8,"value":10},
    {"source":4,"target":9,"value":10},
    {"source":9,"target":2,"value":10},
    {"source":8,"target":2,"value":10},
    {"source":7,"target":2,"value":10}
    ]}

http://embed.plnkr.co/J4o5pmDjYLFsTkYdQjp0/preview에서 그린 도표를 확인할 수 있으며 코드도 함께 볼 수 있다.

# 참고
 * https://gist.github.com/d3noob/c2637e28b79fb3bfea13/
 * http://en.wikipedia.org/wiki/Sankey_diagram
 * http://www.sankey-diagrams.com/
 * http://water.usgs.gov/edu/watercyclekoreanhi.html

