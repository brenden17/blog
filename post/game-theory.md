
game theory

game theory
:    게임 이론이란 대립(conflict)과 협력(cooperation)에 대한 정형 연구다. 행위자들은 다른 행위자의 이익에 영향을 주는 결졍을 하는데 이러한 결정에 대한 연구다. 1838년 Antoine Cournot이 2개 업체의 독점에 대한 연구를 하였으며, 그 후 1944년 폰 노이만이 게임 이론 분야를 개척했다. 1950년에 존 내쉬는 유한 게임에서 모든 행위자가 가장 합리적인 행위를 하는 평형점(equilibrim point)이 있다는 것을 증명하였다. 전통적인 경매에서 벗어나 좀 더 효과적인 경매를 고안하는등 여러 분야에서 사용된다.

## 용어

* payoff - 결과의 희망치를 반영하는 값
* perfect information - 모든 정보가 공개된 상태
* dominating strategy -  상대방의 결정의 상관없이 행위자에게 더 나은 payoff를 주는 전략
* nash equilibrium - 전략적 평형으로, 모든 행위자가 각 전략에 대한 만족하여 더 이상 전략을 변경하지 않는다.

유명한 예제 "용의자 딜레마"로 시작해 보자.
용의자 2명이 잡혀왔다. 경찰은 둘을 따로 심문한다. 용의자는 두 가지가 전략 "c(협력)"과 "d(배신)"를 취할 수 있다. 각 전략에는 payoff가 있다. 

* 용의자 1이 c하고 용의자 2도 c하다면 각 각 2, 2를 얻는 반면 용의자 1이 d하고 용의자 2도 d하다면 각 각 1, 1를 얻는다.
* 용의자 1이 c하는데 용의자 2가 d한다면 각 각 0, 3를 얻고 용의자 1이 d하는데 용의자 2가 c한다면 각 각 3, 0를 얻는다.

다른 용의자의 결정에 따라 자신의 이익에 변한다. 용의자 1이 c하기로 한다면, 용의자 2의 결정에 따라, c인 경우 2나 d인 경우 0을 얻는 반면 용의자 1이 d하기로 한다면, 용의자 2의 결정에 따라 c인 경우 3나 d인 경우 1을 얻는다.
용의자 1은 d를 선택한다. 용의자 2도 같은 조건이기 때문에 용의자들은 최종적으로 모두 d를 선택한다.

이러한 게임을 표로 나타내 보자. 좀 더 이해하기 쉽다.

$$
% Please add the following required packages to your document preamble:
% \usepackage{multirow}
\begin{table}[]
\centering
\caption{My caption}
\label{my-label}
\begin{tabular}{|l|l|l|}
\hline
\textbf{}                                                            & \multicolumn{2}{l|}{c     d}                                                                  \\ \hline
\multirow{2}{*}{\begin{tabular}[c]{@{}l@{}}C\\ \\ \\ D\end{tabular}} & \begin{tabular}[c]{@{}l@{}}2\\ 2\end{tabular} & \begin{tabular}[c]{@{}l@{}}3\\ 0\end{tabular} \\ \cline{2-3} 
                                                                     & \begin{tabular}[c]{@{}l@{}}0\\ 3\end{tabular} & \begin{tabular}[c]{@{}l@{}}1\\ 1\end{tabular} \\ \hline
\end{tabular}
\end{table}
$$

