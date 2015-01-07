==================================
Generative vs Discriminative
==================================

生成模型(Generative Model) ：无穷样本==》概率密度模型 = 产生模型==》预测
判别模型(Discriminative Model)：有限样本==》判别函数 = 预测模型==》预测

简单的说，假设o是观察值，q是模型。
如果对P(o|q)建模，就是Generative模型。其基本思想是首先建立样本的概率密度模型，再利用模型进行推理预测。要求已知样本无穷或尽可能的大限制。
这种方法一般建立在统计力学和bayes理论的基础之上。
如果对条件概率(后验概率) P(q|o)建模，就是Discrminative模型。基本思想是有限样本条件下建立判别函数，不考虑样本的产生模型，直接研究预测模型。代表性理论为统计学习理论。
这两种方法目前交叉较多。

【判别模型Discriminative Model】
====================================

又可以称为条件模型，或条件概率模型。估计的是条件概率分布(conditional distribution)， p(class|context)。
利用正负例和分类标签，focus在判别模型的边缘分布。目标函数直接对应于分类准确率。

- 主要特点：
  寻找不同类别之间的最优分类面，反映的是异类数据之间的差异。
- 优点:
  分类边界更灵活，比使用纯概率方法或生产模型得到的更高级。
  能清晰的分辨出多类或某一类与其他类之间的差异特征
  在聚类、viewpoint changes, partial occlusion and scale variations中的效果较好
  适用于较多类别的识别
  判别模型的性能比生成模型要简单，比较容易学习
- 缺点：
  不能反映训练数据本身的特性。能力有限，可以告诉你的是1还是2，但没有办法把整个场景描述出来。
  Lack elegance of generative: Priors, 结构, 不确定性
  Alternative notions of penalty functions, regularization, 核函数
  黑盒操作: 变量间的关系不清楚，不可视

- 常见的主要有：
  logistic regression
  SVMs
  traditional neural networks
  Nearest neighbor
  Conditional random fields(CRF): 目前最新提出的热门模型，从NLP领域产生的，正在向ASR和CV上发展。

【生成模型Generative Model】
==================================

又叫产生式模型。估计的是联合概率分布（joint probability distribution），p(class, context)=p(class|context)*p(context)。

用于随机生成的观察值建模，特别是在给定某些隐藏参数情况下。在机器学习中，或用于直接对数据建模（用概率密度函数对观察到的draw建模），或作为生成条件概率密度函数的中间步骤。通过使用贝叶斯rule可以从生成模型中得到条件分布。

如果观察到的数据是完全由生成模型所生成的，那么就可以fitting生成模型的参数，从而仅可能的增加数据相似度。但数据很少能由生成模型完全得到，所以比较准确的方式是直接对条件密度函数建模，即使用分类或回归分析。

与描述模型的不同是，描述模型中所有变量都是直接测量得到。

- 主要特点：
  一般主要是对后验概率建模，从统计的角度表示数据的分布情况，能够反映同类数据本身的相似度。
  只关注自己的inclass本身（即点左下角区域内的概率），不关心到底 decision boundary在哪。
- 优点:
  实际上带的信息要比判别模型丰富，
  研究单类问题比判别模型灵活性强
  模型可以通过增量学习得到
  能用于数据不完整（missing data）情况
  modular construction of composed solutions to complex problems
  prior knowledge can be easily taken into account
  robust to partial occlusion and viewpoint changes
  can tolerate significant intra-class variation of object appearance
- 缺点：
  tend to produce a significant number of false positives. This is particularly true for object classes which share a high visual similarity such as horses and cows
  学习和计算过程比较复杂

- 常见的主要有：
  Gaussians, Naive Bayes, Mixtures of multinomials
  Mixtures of Gaussians, Mixtures of experts, HMMs
  Sigmoidal belief networks, Bayesian networks
  Markov random fields

所列举的Generative model也可以用disriminative方法来训练，比如GMM或HMM，训练的方法有EBW(Extended Baum Welch),或最近Fei Sha提出的Large         Margin方法。

- 主要应用：
  NLP:
  Traditional rule-based or Boolean logic systems (Dialog and Lexis-Nexis) are giving way to statistical approaches (Markov models and stochastic context grammars)
  Medical Diagnosis:
  QMR knowledge base, initially a heuristic expert systems for reasoning about diseases and symptoms been augmented with decision theoretic formulation Genomics and Bioinformatics
  Sequences represented as generative HMMs

【两者之间的关系】
=======================

由生成模型可以得到判别模型，但由判别模型得不到生成模型。


======================

比较三种模型：HMMs and MRF and CRF

http://blog.sina.com.cn/s/blog_4cdaefce010082rm.html

HMMs(隐马尔科夫模型):
状态序列不能直接被观测到(hidden)；
每一个观测被认为是状态序列的随机函数；
状态转移矩阵是随机函数，根据转移概率矩阵来改变状态。
HMMs与MRF的区别是只包含标号场变量，不包括观测场变量。

MRF(马尔科夫随机场)
将图像模拟成一个随机变量组成的网格。
其中的每一个变量具有明确的对由其自身之外的随机变量组成的近邻的依赖性(马尔科夫性)。

CRF(条件随机场),又称为马尔可夫随机域
一种用于标注和切分有序数据的条件概率模型。
从形式上来说CRF可以看做是一种无向图模型，考察给定输入序列的标注序列的条件概率。

在视觉问题的应用：
HMMs:图像去噪、图像纹理分割、模糊图像复原、纹理图像检索、自动目标识别等
MRF: 图像恢复、图像分割、边缘检测、纹理分析、目标匹配和识别等
CRF: 目标检测、识别、序列图像中的目标分割

P.S.
标号场为隐随机场，它描述像素的局部相关属性，采用的模型应根据人们对图像的结构与特征的认识程度，具有相当大的灵活性。
空域标号场的先验模型主要有非因果马尔可夫模型和因果马尔可夫模型。
