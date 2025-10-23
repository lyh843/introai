import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, uniform

# ==== 1. 定义Clayton Copula采样函数 ====
def clayton_copula_sample(theta, n):
    # Step 1: 从Gamma分布采样 (根据Clayton的构造原理)
    W = np.random.gamma(shape=1/theta, scale=1, size=n)
    # Step 2: 从独立的均匀分布采样 U
    U = np.random.rand(n)
    # Step 3: 计算另一个依赖变量 V
    V = (U**(-theta/(1+theta)) * (np.random.rand(n)**(-1/theta) - 1) + 1)**(-1/theta)
    return U, V

# ==== 2. 生成Copula上的U,V ====
theta = 2.0
n = 5000
U, V = clayton_copula_sample(theta, n)

# ==== 3. 定义边缘分布 ====
# X1 ~ Exp(1), X2 ~ Uniform(0,1)
X1 = expon.ppf(U, scale=1.0)   # 反CDF变换
X2 = uniform.ppf(V, loc=0, scale=1)

# ==== 4. 可视化 ====
fig, axes = plt.subplots(1, 3, figsize=(15,4))

axes[0].scatter(U, V, s=5, color='steelblue')
axes[0].set_title('Copula space (U,V)')

axes[1].hist2d(X1, X2, bins=50, cmap='Blues')
axes[1].set_title('Joint distribution (X1, X2)')

axes[2].scatter(X1, X2, s=5, color='darkorange')
axes[2].set_title('Joint samples after transformation')

for ax in axes:
    ax.set_xlabel('X1 or U')
    ax.set_ylabel('X2 or V')

plt.tight_layout()
plt.show()
