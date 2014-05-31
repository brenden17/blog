work
MathJax
math
# MathJax
[MathJax](http://www.mathjax.org/)
:   MathJax는 모든 브라우저에서 수학식을 출력할 수 있는 자바스크립트 오픈 소스이다.
  
MathJax는 매우 **아름답다**.

## 설치
head에 한줄 추가하면 된다.

> <script type="text/javascript"  src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>

## 기본 사항
### 인라인과 단락
    $...$ (인라인)
    $$...$$ (단락)

### 그리스 문자

$$
\alpha, \beta, \omega
$$

### 어깨 글자(superscripts), 첨자(subscripts)
$$
x_i^2
$$

### 그룹 만들기
$$
x_i^2 \qquad x_i^{2+y}
$$

### 작은 괄호, 큰 괄호
$$
(\frac12) \qquad \left(\frac12\right)
$$

### 합과 적분
$$
\sum_{i=0}^\infty i^2 \qquad \int \qquad \iint \qquad \prod
$$

### 분수
$$
\frac{a+1}{b+1} \qquad {a+1\over b+1}
$$

### 근
$$
\sqrt[3]{\frac xy}
$$

### 기호
$$
\lim_{x\to 0}
$$
$$
\sin x 
$$
$$
\lt  \qquad \gt  \qquad \le  \qquad \ge  \qquad \neq
$$
$$
\times  \qquad \div  \qquad \pm  \qquad \mp 
$$
$$
\binom{n+1}{2k}
$$
$$
\cup \qquad \cap \qquad \setminus \qquad \subset \qquad \subseteq 
$$
$$
\subsetneq  \qquad \supset  \qquad \in  \qquad \notin  \qquad \emptyset  \qquad \varnothing
$$
$$
\to  \qquad \rightarrow  \qquad \leftarrow  \qquad \Rightarrow  \qquad \Leftarrow  \qquad \mapsto
$$
$$
\land  \qquad \lor \qquad \lnot \qquad \forall \qquad \exists \qquad \top \qquad \bot \qquad \vdash \qquad \vDash
$$
$$
\Im  \qquad \Re
$$
$$
\nabla \qquad \partial 
$$
$$
\infty \qquad \aleph_0
$$
$$
\ldots \qquad \cdots
$$
$$
\text{…}
\vec x
$$
$$
\overrightarrow xy 
$$


## 예제
* *Gamma function*
$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

---------

from [mathjax](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)