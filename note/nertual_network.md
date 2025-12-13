# 神经网络与深度学习

## 一、神经元模型到前馈神经网络

### (1) M - P神经元

$$
x_i \in \{0, 1\}\  and \ y \in \{0, 1\}
$$

$$
z(x_1, x_2, \dots, x_d) = z(x) = \sum_{j=1}^d w_jx_j
$$

$$
y = g(z(x)) = 
\begin{cases}
1 & if \  z(x) \geq T\\
0 & if \  z(x) < T
\end{cases}
$$

### (2) 神经元的激活函数

- 理想激活函数是阶跃函数，0表示抑制神经元而1表示激活神经元
- 阶跃函数具有不连续、不光滑等不好的性质，常用的是 $Sigmoid$函数

$$
sgn(x) = \begin{cases} 1, & if \  x \geq 0;\\ 0, & if \  x < 0. \end{cases} \quad \quad sigmoid(x) = \frac{1}{1 + e^{-x}}
$$

### (3) 感知机（Perceptron）

$$
y = w_1 x_1 + w_2 x_2
$$

感知机能够容易实现逻辑与、或、非运算。

> 现代神经网络普遍将感知机中的显式阈值 $\theta$ 吸收到偏置项$bias$中，从而不再单独使用阈值。

当两类模式线性可分时，则感知机的学习过程一定会收敛；否则感知机的学习过程将会发生震荡。

### (4) 多层感知机（Multi-Layerd Perceptron, MLP）

#### 多层前馈神经网络

将输出层与输入层之间的一层神经元称为**隐层或隐含层**。

隐含层和输出层神经元都是具有激活函数的**功能神经元**。

**前馈网络：**层与层全连接，但不能存在同层连接和跨层连接。

**万有逼近性：** 仅需一个包含足够多神经元的隐层，多层前馈神经网络就能以任意精度逼近任意复杂度的连续函数。（并非神经网络特有）

## 二、参数优化 BP算法

### (1) 网络参数优化

给定训练集$D = \{(x_1, y_1), (x_2, y_2), \cdots, (x_m, y_m)\}, x_i \in \mathbb{R}^d, y_i \in \mathbb{R}^l$

- 输入：$d$维特征向量
- 输出：$l$个输出值
- 隐层：$q$个隐层神经元

第$h$个隐层神经元的输入：
$$
\alpha_h = \sigma(\sum_{i = 1}^d w_{ih}x_i)
$$
第$j$个输出神经元的输入：
$$
\beta_j = \sum_{h = 1}^q w_{hj}b_h
$$

- 需要通过学习确定的参数数目：$dq + ql + q + l$

### (2) 梯度下降（Gradient Descent）

- 函数$f$在$w$处的取值为$f(w)$，梯度为$\nabla f(w)$

- 参数更新方法为：
  $$
  w_i = w_{i - 1} - \eta \nabla f(w_{i - 1})
  $$
  其中$\eta$一般被称为步长（step size）或者学习率（learning rate）.

  学习率$\eta \in [0, 1]$，不能太大，不能太小。

### (3) BP（Back Propagation：误差逆传播算法）

对于训练样本$(x_k, y_k)$，假定网络的实际输出为$\hat{y}_k = (\hat{y}_1^k, \hat{y}_2^k, \cdots, \hat{y}_n^k)$，则网络在样本$(x_k, y_k)$上的均方误差为：
$$
E_k = \frac{1}{2} \sum_{j = 1}^l (\hat{y}_j^k - y^k_j)^2
$$
对误差$E_k$，当我们求
$$
\frac{\partial E_k}{\partial w_{hj}}
$$
时，注意到$w_{hj}$先影响$\beta_j$，在影响到$\hat{y}_j^k$，然后才影响到$E_k$，有：
$$
\frac{\partial E_k}{\partial w_{hj}} = \frac{\partial E_k}{\partial \hat{y}^k_j} \frac{\partial  \hat{y}^k_j}{\partial \beta_j}  \frac{\partial \beta_j}{\partial w_{hj}}
$$
这种做法称为**链式法则**。

> 对于$sigmoid(x) = \frac{1}{1 + e^{-x}}$，
> $$
> f'(x) = f(x)(1 - f(x))
> $$

#### 多种实现方式

1. **批量梯度下降(batch gradient descent)：**
   - 每次在整个训练集上计算损失误差
   - 每次需要读取完整数据，消耗内存，收敛速度较慢
2. **随机梯度下降(stochastic gradient descent)：**
   - 每次随机选一个样本计算损失误差
   - 参数更新频繁，不同样例可能抵消
3. **小批量梯度下降(mint-batch gradient descent)：**
   - 每次随机选一批样本计算损失误差读取整个训练集
   - 训练过程更稳定，如何设置`batch-size`是个难题

#### 两个名词：Epoch和Iteration

- **Epoch：**轮次，整个训练集被完整地训练一遍
- **Iteration：**迭代步，一次参数更新

```python
for epoch in range(num_epochs):	# epoch 层
    for i, (x_batch, y_batch) in enumerate(train_loader):	# iteration 层
        y_pred = model(x_batch)
        loss = criterion(y_pred, y_batch)
        loss.backward()
        optimizer.step()
```

## 三、深度学习

深度学习模型就是具有很多个隐层的神经网络。

### (1) 理解深度学习

#### 从“特征工程”到“特征学习”或“表示学习”

- 特征工程是由人类专家根据现实任务来设计，**特征提取与识别**是分开的两个阶段。
- 特征学习通过深度学习**自动产生**有益于分类的特征，是一个**端到端（end-to-end）**的学习框架。

### (2) 深度学习的挑战

#### 1. 复杂优化问题

**非凸优化（Non-Convex Optimization）**：神经网络通常是非凸的，难以找到全局最优解、鞍点（saddle point）问题。

神经网络最大的谜团之一：优化是如此困难，为什么效果还能这么好？

- **过参数化**：过参数化让许多不同参数组合都能实现相同的低损失，从而形成大量”良性平坦极小值“。
- **足够好的局部最优：**在大型、过参数化的神经网络中，大部分局部最优解可能已经足够好了
- **逃离鞍点：**$SGD$的随机性，往往可以逃出鞍点。

#### 2. 梯度消失与梯度爆炸

反向传播链式法则中的导数连乘导致梯度消失或爆炸

##### 缓解梯度消失的Tricks：

1. **新型激活函数**

   - $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$

   - $ReLU(x) = \begin{cases} x, & x \geq 0\\ 0, & x < 0 \end{cases}= \max(x, 0) $
   
   - $LeakyReLU(x) = \begin{cases} x, & x \geq 0\\ \gamma x, & x < 0 \end{cases}= \max(x, 0) + \gamma \min(x, 0)$
   
   - $ELU(x) = \begin{cases} x, & x > 0\\ \gamma (\exp(x) - 1), & x \leq 0 \end{cases} = \max(0, x) + \min(0, \gamma(\exp(x) - 1))$ 
   
   - $softplus(x) = \log(1 + exp(x))$
   
2. **残差连接**

   假设在一个深度网络中，我们期望$f(x, \theta)$去逼近目标函数$h(x)$，将目标函数拆分成两部分：**恒等函数**和**残差函数**。
   $$
   h(x) = x + (h(x) - x)
   $$
   其中$x$为恒等函数，$h(x) - x$为残差函数

3. **Batch Normalization**

   在每层网络中，都对输入特征进行归一化，让分布稳定在$\mathcal{N}(0, 1)$。

   假设输入是一个batch的样本$B$，样本$x$是这个$batch$中的样本，$\gamma$和$\beta$是可学习参数。
   $$
   BN(x) = \gamma \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} + \beta
   $$

   > 可避免进入激活函数的梯度饱和区。

#### 3. 超参数选择困难

#### 4. 过拟合

#### 5. 计算资源开销

#### 6. 可解释性

#### 7. 稳健性