=======================
HMM
=======================

生成模式
----------------

非确定性模式：状态转移具有不确定性
一种做法是假设模型的当期状态仅仅依赖于前面的几个状态，这被称为马尔科夫假设。
一个马尔科夫过程是状态间的转移仅依赖于前n个状态的过程。这个过程被称之为n阶马尔科夫模型。
最简单的马尔科夫过程是一阶模型，他的状态选择仅与前一个状态有关。这里要注意，他的下一个状态的选择是由相应的概率决定，而非确定性的

隐藏模式
-----------------

通过观察的状态预测隐藏的状态，比如通过水藻的状态变化和马尔科夫假设预测天气的变化
隐马尔科夫模型包含一个底层隐藏的随时间改变的马尔科夫过程，以及一个与隐藏状态某种程度相关的可观察到的状态集合
隐马尔科夫模型（HMM)包括两组状态集合和三组概率集合：
  隐藏状态和观察状态
  pi向量：包含了（隐）模型在时间t＝1时一个特殊的隐藏状态的概率（初始概率）
  状态转移矩阵：一个隐藏状态到另一个隐藏状态的概率
  混淆矩阵：包含给定HMM的某一个特殊的隐藏状态，观察到某个观察状态的概率

一个HMM是一个三元组(pi, A, B)
  pi：初始化向量
  A = (aij) : 状态转移矩阵 P(Xi | X i-1)
  B = (bij) : 混淆矩阵P(Yi | Xi)

三个问题：
  给定HMM求一个观察序列的概率                  前向算法(forward algorithm)
  搜索最有可能生成一个观察序列的隐藏状态序列   Viterbi algorithm
  给定观察序列生成一个HMM                      前向-后向算法(forward-backward algorithm)

前向算法
-----------------

1.穷举搜索

2.使用递归降低问题复杂度

at(j) = Pr(观察状态 | 隐藏状态j) * Pr(t时刻所有指向j状态的路径)
故我们所计算的这个概率等于相应的观察概率（亦即，t+1时在状态j所观察到的符号的概率）与该时刻到达此状态的概率总和--这来自于上一步每一个局部概率的计算结果与相应的状态转移概率乘积后再相加--的乘积

维特比算法
--------------------

寻找最可能的隐藏状态序列

1. 穷举搜索

2. 使用递归降低复杂度

前向-后向算法
--------------------------

根据观察序列生成隐马尔科夫模型


后向算法
-------------------


