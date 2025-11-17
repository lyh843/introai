# 监督学习（Supervised Learning）

**监督学习：**所有训练样本均有对应的标注

## 一、近邻算法

考虑一个二分类问题：

- 给定数据集$D = \{(x_1, y_1), (x_2, y_2), \cdots, (x_n, y_n)\}$
- 学习模型$f:x\rightarrow y, y = \{-1, 1\}$

**基本思路：**近朱者赤，近墨者黑（懒惰学习）

> 懒惰学习：不需要训练，直接用来测试

### k 近邻学习器（K Nearest Neighbors）

找到最近的$k$个样本，投票或者平均

**关键问题：**$k$值的选取、距离的计算

> 选择较小的$k$，相当于用较小的领域中的训练样本进行预测，训练误差会减小，泛化误差会增大。即$k$的减小意味着整体模型更为复杂，容易发生过拟合。
>
> 选择较大的$k$，相当于用较大的领域中的训练样本进行预测，会使模型更简单，一定成都可以减小泛化误差。

#### 距离度量

需要满足以下性质：

- 非负性：$\textbf{dist}(x_i, x_j) \geq 0$
- 同一性：$dist(x_i, x_j) = 0$当且仅当$x_i = x_j$
- 对称性：$\textbf{dist}(x_i, x_j) = \textbf{dist}(x_j, x_i)$
- 直递性：$\textbf{dist}(x_i, x_k) \leq \textbf{dist}(x_i, x_j) +\textbf{dist}(x_j, x_k)$，在机器学习中直递性不一定满足

常用距离形式：**闵克夫斯基距离（Minkowski distance）**

假设输入样本为$d$维向量：$x = (x_1, x_2, \cdots ,x_d)$
$$
dist_{mk}(x, x') = \left( \sum_{i=1}^d |x_i - x_i'|^p \right)^{\frac{1}{p}}
$$

## 二、决策树（Decision Tree）

决策树是一种通过树形结构来进行分类的方法

每个非叶子节点表示对样本在某个属性上的一个判断，根据判断的不同结果产生不同的分支，每个叶子节点代表一种分类结果

- **学习过程：**通过对训练样本的分析来确定“划分属性”
- **预测过程：**将测试示例从根节点开始，沿着划分属性所构成的“判定测试序列“下行，直至叶结点

> 随着划分的不断进行，我们希望决策树分支节点所包含的样本集尽可能属于同一类别，即节点的“纯度”越高越好

###  信息熵：

度量样本集合“纯度”最常用的一种指标

假定当前样本集合$D$中第$k$类样本所占的比例为$p_k$，则$D$的信息熵定义为
$$
\textbf{Ent}(D) = -\sum_{k=1}^{|y|}p_k \log_2{p_k}
$$
$\textbf{Ent}(D)$的值越小，则$D$的纯度越高。

> 其中$y$表示样本的类数。
>
> 通过比较划分前后的信息熵值，来衡量模型的好坏

### 信息增益：

以属性$a$对数据集$D$进行划分所或得的信息增益为：
$$
\textbf{Gain}(D, a) = \textbf{Ent}(D)-\sum_{v=1}^V\frac{|D^v|}{|D|}\textbf{Ent}(D^v)
$$

> 信息增益 = 划分前的信息熵 - 第$v$个分支信息熵的权重 \* 划分后的信息熵

对可取数目较多的属性有明显偏好。

### 增益率：

$$
\text{Gain_ratio}(D, a) = \frac{\text{Gain}(D, a)}{IV(a)}
$$

其中$IV(a) = -\sum_{v=1}^V \frac{|D^v|}{|D|} \log_2 \frac{|D^v|}{|D|}$

### 基尼系数（Gini Index）

$$
Gini(D) = \sum_{k=1}^{|y|}\sum_{k' \neq k} p_k p_{k'} = 1 - \sum_{k=1}^{|y|}p_k^2
$$

属性$a$的基尼指数：$Gini\_index(D, a) = \sum_{v=1}^{V}\frac{|D^v|}{|D|} Gini(D^v)$

在候选属性集合中，选取那个是划分后基尼指数最小的属性

### 停止条件：

- 结点包含的样本全属于同一类别，无需划分
- 样本在所有属性上的取值相同，无法划分
- 划分集为空，不能划分

### 规则学习（Rule Learning）：从数据到规则

一棵决策树对应于一个“规则集”

==每个从根节点到叶结点的分支路径对应于一条规则==

## 三、线性回归（linear regression）

### 1. 一元线性回归

- 模型：$f(x_i) = w x_i + b$​
- 目标：$f(x_i) \cong y_i \rightarrow (w^*, b^*) = \arg \min_{(w, b)} \sum_{i = 1}^n(y_i - f(x_i))^2$  （最小二乘法）

> 均方误差：$L(f) = \sum_{i=1}^n (y_i - f(x_i))^2$

#### 过程：

- 将$L(w, b)$分别对$w$和$b$求导；
- 令导数为$0$，得到闭式解：
  - $b = \frac{1}{n} \sum_{i=1}^n(y_i - wx_i) = \bar{y} - w \bar{x}$
  - $w = \frac{\sum_{i=1}^n x_iy_i - n \bar{x}\bar{y}}{\sum_{i=1}^n x_ix_i - n \bar{x}^2}$

### 2. 多元线性回归

- 模型：$f(x_i) = w_1 x_{i1} + w_2 x_{i2} + \cdots + w_dx_{id} + b$，向量形式：$f(x) = w^Tx + b$

#### 矩阵形式

给定数据集$D = \{X, Y\}, X \in \mathbb{R}^{n\times d}, Y \in \mathbb{R}^{n \times 1}$

#### 齐次表达

把$W$和$b$吸收入矩阵$\hat{W}$，并且在特征矩阵后添加一个全$1$列

### 3. 正则化

限制假设空间复杂度，提升泛化能力

**岭回归：**
$$
\arg \min_{w, b} \frac{1}{m} \sum_{i=1}^{m} (w^Tx_i + b - y_i)^2 + \lambda \|w\|_2
$$
**LASSO Regression：**
$$
\arg \min_{w, b} \frac{1}{m} \sum_{i = 1}^m (w^T x_i + b - y_i)^2 + \lambda \|w\|_1
$$

#### 结构风险最小化（Structural Risk Minimization, SRM）

$L(w, b)$描述的是经验风险，而$\|w\|_p$描述的是结构风险。

## 四、对数几率回归

### 1. 广义线性模型

令预测值逼近$y$的衍生物，如$\ln y = w^T x+b$

### 2. 对数几率回归

在回归模型中引入`sigmoid`函数的一种模型
$$
y = \frac{1}{1 + e^{-z}} = \frac{1}{1 + e^{-(w^Tx + b)}} \Rightarrow \ln{\frac{y}{1-y}} = w^Tx+b
$$

> 几率：$\frac{y}{1-y}$反映了$x$作为正例的相对可能性
>
> 如果输入数据$x$属于正例的概率大于其属于负例的概率，即$p(y=1|x) > 0.5$，则$x$可被判断为正例。
>
> ==此时==$\frac{p(y=1|x)}{p(y=0|x)} > 1$
>
> 对数几率：$\ln{\frac{y}{1-y}}$

## 3. 求解

- 给定数据集$D=\{(x_1, y_1), (x_2, y_2), \cdots (x_n, y_n)\}, x_i \in \mathbb{R}^d, y_i \in \{0, 1\}$

- 将$y$看作类后验概率估计，则有
  $$
  \ln \frac{p(y = 1 |x)}{p(y = 0 |x)} = w^Tx + b
  $$

- 显然有
  $$
  p(y = 1 |x) = \frac{e^{w^Tx + b}}{1 + e^{w^Tx + b}}\\
  P(y = 0 |x) = \frac{1}{1 + e^{w^Tx +b}}
  $$

- 我们希望每个样本属于其真实标记的概率越大越好
  $$
  \max \sum_{i=1}^n \ln p(y_i | x_i; w, b)
  $$
  其中$p(y_i |x_i; w, b) = \sigma(w^Tx_i + b)^{y_i} \cdot [1 - \sigma(w^Tx_i + b)]^{1- y_i}$，$\sigma(z) = \frac{1}{1 + e^{-z}}$

- 等价于最大化
  $$
  \sum_{i=1}^n y_i \ln(f(x_i)) + (1 - y_i)\ln(1 - f(x_1))
  $$

- 即最小化
  $$
  L(f) = \sum_{i=1}^n -y_i \ln(f(x_i)) - (1 - y_i) \ln (1 - f(x_1))
  $$
  

## 五、支持向量机（Support Vector Machine, SVM）

### 1. 线性分类器

在样本空间中寻找一个超平面，将不同类别的样本分开

**正中间的决策边界：**鲁棒性最好，泛化能力最强。

#### 间隔（margin）与支持向量(support vector)

对于正中间的决策边界，它的支持向量

点到超平面距离公式：
$$
r = \frac{|w^Tx + b|}{\|w\|}
$$

> 点到决策边界的距离即对这个点分类的把握，距离越远把握越大。

### 2. 支持向量机-基本型

**最大间隔：**寻找参数$w$和$b$，使得$\gamma = \frac{2}{\|w\|}$最大
$$
\begin{aligned}
\arg \max_{w, b} & \frac{2}{\|w\|}\\
\text{s.t.} & y_i(w^Tx_i + b) \geq 1, i = 1, 2, \dots, m.
\end{aligned}
$$

### 3. 支持向量机-对偶型

#### 拉格朗日乘子法

- 第一步：引入拉格朗日乘子$\alpha_i \geq 0$，得到拉格朗日函数
  $$
  L(w,b,\alpha) = \frac{1}{2}\|w\|^2 + \sum_{i=1}^m \alpha_i(1-y_i(w^Tx_i +b))
  $$
  
- 第二步：令$L(w,b, \alpha)$对$w$和$b$的偏导为零可得：
  $$
  w = \sum_{i = 1}^m \alpha_iy_ix_i, \quad 0 = \sum_{i = 1}^m \alpha_i y_i
  $$

- 第三步：回代可得：

$$
\begin{aligned}
\max_\alpha & \sum_{i=1}^m \alpha_i -\frac{1}{2} \sum_{i=1}^m\sum_{j=1}^m \alpha_i \alpha_j y_i y_j x_i^T x_j\\
\text{s.t.} & sum_{i = 1}^m \alpha_i y_i = 0, \alpha_i \geq 0, \quad i = 1, 2, \dots, m
\end{aligned}
$$

- 最终模型：$f(x) = w^Tx + b = \sum_{i=1}^m a_iy_ix_i^Tx + b$

- KKT条件：
  $$
  \begin{cases}
  \alpha_i \geq 0\\
  1 - y_i f(x_i) \leq 0\\
  \alpha_i(1 - y_if(x_i)) = 0
  \end{cases}
  \Rightarrow \alpha_i = 0 \text{或}y_if(x_i) = 1
  $$

- 

**解的稀疏性：**训练完成后，最终模型仅与支持向量有关。

### 4. 特征空间映射

若原始空间是有限维（属性数有限），那么一定存在一个高维特征空间使样本线性可分。

**Mercer定理：**若一个对称函数所对应的核矩阵半正定，则它就能作为核函数来使用。（满足距离的特性即可）

核函数的选择成为决定支持向量机性能的关键。

## 六、多分类

### 1. 拆解法

将一个多分类任务拆分成若干个二分类任务求解

`one to one`&`one to rest`

### 2. ECOC码

多对多：将若干分类作为正类，若干类作为反类

- 二元ECOC码
- 三元ECOC码

> ECOC编码对分类器有一定容忍和修正能力，编码越长、纠错能力越强

## 七、类别不平衡（Class-Imbalance）

不同类别的样本比例相差很大，“小类”有时候更重要

### 1. 基本思路

若$\frac{y}{1-y} > 1 \Rightarrow \frac{y}{1-y} > \frac{m^+}{m^-}$，则预测为正类。

**基本策略：**再缩放（rescaling）

### 2. 常见类别不平衡学习方法

- **过采样**

## 八、开发一个机器学习系统

### 1. 步骤

- #### 任务形式化

  - 判断垃圾邮件、金融欺诈检测
  - 评价指标是什么？正确率、查准率、查全率、F1

- #### 数据

  - 有多少数据？数据的形式是什么？有多少维度？有没有对应的标注？类别是否平衡？
  - 特征工程（Feature Engineering）：离散值编码、特征组合扩充、特征选择

- #### 模型选择

  - LR, Decision Tree, SVM, Neural Network?

- #### 模型训练与评估

  - 训练集 vs 验证集

- #### 模型部署