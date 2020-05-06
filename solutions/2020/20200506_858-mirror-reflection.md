# #858. 镜面反射 / Mirror Reflection

> 难度：中等 · 标签：Math、Geometry、Number Theory · [LeetCode 链接](https://leetcode.com/problems/mirror-reflection/)

---

## 题目（英文原版）

**Description**

There is a special square room with mirrors on each of the four walls. Except for the southwest corner, there are receptors on each of the remaining corners, numbered 0, 1, and 2.
The square room has walls of length p and a laser ray from the southwest corner first meets the east wall at a distance q from the 0th receptor.
Given the two integers p and q, return the number of the receptor that the ray meets first.
The test cases are guaranteed so that the ray will meet a receptor eventually.

**Examples**

**Example 1:**

```
Input: p = 2, q = 1
Output: 2
Explanation: The ray meets receptor 2 the first time it gets reflected back to the left wall.
```

**Example 2:**

```
Input: p = 3, q = 1
Output: 1
```

**Constraints**

- 1 <= q <= p <= 1000

---

## 题目（中文翻译）

有一个特殊的正方形房间，四面墙上都装有镜子。除西南角之外，剩余三个角各放置一个接收器（receptor），编号为 0、1、2。  
正方形房间的边长为 `p`，激光光线从西南角发出，第一次碰到东墙时，距编号为 0 的接收器的距离为 `q`。  
给定整数 `p` 和 `q`，返回光线首次碰到的接收器编号。  
题目保证光线最终一定会碰到某个接收器。

**示例 1**  
```text
Input: p = 2, q = 1
Output: 2
Explanation: 光线在第一次被反射回左墙时碰到接收器 2。
```

**示例 2**  
```text
Input: p = 3, q = 1
Output: 1
```

**约束条件**  
- `1 <= q <= p <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**模拟光线的运动**，每次碰到墙就按照“入射角等于反射角”把方向改成相反的。  
- 用坐标 `(x, y)` 表示光点的位置，`dx, dy` 表示水平、垂直方向的步长。  
- 房间是一个边长为 `p` 的正方形，左下角是激光发射点 `(0,0)`，右上角是 `(p,p)`。  
- 当光线到达右墙（`x = p`）或上墙（`y = p`）时，需要把对应的方向反向（`dx = -dx` 或 `dy = -dy`）。  
- 每次光线恰好落在某个角点时，就检查该角点对应的 receptor 编号：  
  - `(p,0)` → 0  
  - `(p,p)` → 1  
  - `(0,p)` → 2  

这个过程像在玩“弹弹球”游戏，**每一步都用最直观的几何规则**来推进，最终一定会撞到一个角点（题目保证）。

#### 代码（Python）
```python
def mirrorReflection_bruteforce(p: int, q: int) -> int:
    # 初始位置在左下角 (0, 0)
    x, y = 0, 0
    # 每次向右上方前进，水平走 p，垂直走 q
    # 为了统一步长，使用最小公倍数的倍数来一次性跨过多次反射
    # 这里采用最朴素的“每次走到最近的墙”模拟
    dx, dy = p, q          # 正向的水平/垂直位移

    while True:
        # 计算下一次会先撞到哪面墙
        # 由于房间是正方形，只需要比较 x+dx 与 y+dy 哪个先到达 p
        # 这里把 dx, dy 视为“相对距离”，不真正移动，只判断比例
        # 当比例相等时，光线恰好撞到左上角 (p, p)
        # 当水平比例更小，先撞到右墙；垂直比例更小，先撞到上墙
        if (x + dx) % p == 0 and (y + dy) % p == 0:
            # 同时到达右墙和上墙，说明撞到 (p, p)
            return 1
        elif (x + dx) % p == 0:
            # 先到达右墙 (p, y')
            x = p
            y = (y + dy) % (2 * p)   # 取模实现上下墙的镜像效果
            # 碰到右墙后水平方向反向
            dx = -dx
        else:
            # 先到达上墙 (x', p)
            x = (x + dx) % (2 * p)
            y = p
            # 碰到上墙后垂直方向反向
            dy = -dy

        # 处理完反射后，检查是否正好落在某个 receptor 位置
        if x == p and y == 0:   # 右下角
            return 0
        if x == p and y == p:   # 右上角
            return 1
        if x == 0 and y == p:   # 左上角
            return 2
```

> **注意**：上述代码写得比较“笨拙”，只为说明思路。实际运行时会出现无限循环，因为我们没有把 `dx, dy` 正确归一化。这里的重点是让读者感受到“每次碰墙都改方向”的直觉。

#### 复杂度
- **时间复杂度**：`O(k)`，其中 `k` 是光线碰墙的次数。最坏情况下 `k` 可能非常大（比如 `p=1000, q=1`），相当于“慢到像 O(p)`”。  
- **空间复杂度**：`O(1)`，只用了常数个变量来记录坐标和方向。

---

### 2. 最优解

#### 思路  
从暴力模拟可以看出，**光线的路径其实是有规律的**：每一次碰墙都相当于在“平面上”把房间复制成镜像，光线在这些复制的房间里是一条直线，**不再折返**。  

我们可以把四面镜子想象成把房间无限复制成网格（像棋盘），光线就像在这张无限大纸上直线前进。  
- 每次光线到达右墙的距离是 `p` 的整数倍；每次到达上墙的距离是 `q` 的整数倍。  
- 当光线第一次恰好落在某条竖直或水平镜像的交点时，就对应原房间的某个角点。  

因此，只要找最小的正整数 `m` 使得 `m * q` 同时是 `p` 的整数倍，即  
```
m * q = LCM(p, q)
```
其中 `LCM` 为最小公倍数。  
- `m` 表示光线在 **垂直方向**（上墙）走了多少次 `q` 的距离。  
- 同时，光线在 **水平方向**走了 `n = LCM(p, q) / p` 次 `p` 的距离。

现在只要判断 `m`（上墙次数）和 `n`（右墙次数）的奇偶性：

| n (右墙次数) | m (上墙次数) | 落点 | receptor |
|-------------|--------------|------|----------|
| 偶数        | 奇数         | 左上角 `(0, p)` | 2 |
| 奇数        | 偶数         | 右下角 `(p, 0)` | 0 |
| 奇数        | 奇数         | 右上角 `(p, p)` | 1 |

解释：  
- 每次碰到右墙会把水平坐标从 `0 → p → 0 → p …`，所以 **奇偶** 决定最终是左墙还是右墙。  
- 同理，上墙的奇偶决定是下墙还是上墙。  
- 只有三种组合会出现 receptor（左下角没有 receptor），对应上表。

**关键点**：只需要用**数学公式**求最小公倍数，然后检查奇偶性，整个过程是 **O(1)**。

> **最小公倍数的求法**  
> `LCM(a, b) = a // gcd(a, b) * b`，其中 `gcd` 是最大公约数。Python 标准库 `math.gcd` 可以直接使用。

#### 代码（Python）
```python
import math

def mirrorReflection(p: int, q: int) -> int:
    """
    返回光线第一次遇到的 receptor 编号（0、1、2）
    思路：把镜子房间想象成无限平铺的网格，光线在网格中是一条直线。
    当光线第一次在网格交点处落在原房间的角落时，即为答案。
    """
    # 计算最小公倍数 L = LCM(p, q)
    lcm = p // math.gcd(p, q) * q   # 先除后乘，防止整数溢出（这里 p,q <= 1000，安全）

    # 右墙被碰撞的次数 = L / p
    times_right = lcm // p
    # 上墙被碰撞的次数 = L / q
    times_up = lcm // q

    # 根据奇偶性判断落在的角点
    if times_right % 2 == 1 and times_up % 2 == 1:
        # 右墙奇数、上墙奇数 → (p, p) → receptor 1
        return 1
    elif times_right % 2 == 1 and times_up % 2 == 0:
        # 右墙奇数、上墙偶数 → (p, 0) → receptor 0
        return 0
    else:
        # 右墙偶数、上墙奇数 → (0, p) → receptor 2
        return 2
```

#### 复杂度
- **时间复杂度**：`O(1)`。只用了求最大公约数（欧几里得算法）和几次整数运算，跟 `p、q` 的大小无关。  
- **空间复杂度**：`O(1)`。只用了常数个变量。

---

## 心得

- **核心技巧**：把“镜子反射”转化为“平面镜像的无限复制”，进而用**最小公倍数**和**奇偶性**直接求解。  
- **适用的题型**：  
  1. 需要判断光线或球在镜面/弹性碰撞后落点的几何题（如 “反弹球”）。  
  2. 需要在周期性运动中找第一次满足某条件的情形（如 “循环数组中的最小公倍数”）。  
- **一句话总结**：**把折射的路径“拉直”，在整数格子里找最小公倍数，再看奇偶就能直接得到答案。**

---

## 反思

- **第一反应**：看到镜子和反射，就想到“模拟每一次碰撞”。这会导致代码冗长且效率低下。  
- **最容易踩的坑**：  
  - 忘记考虑左下角没有 receptor，导致错误返回 `0`。  
  - 直接使用 `lcm = p * q` 而不除以 `gcd`，会产生整数溢出（虽然本题范围小，但是坏习惯）。  
  - 在判断奇偶时写反了 `times_right % 2` 与 `times_up % 2` 的对应关系。  
- **下次类似题的第一步**：先问自己“如果把镜子去掉，光线会在怎样的平面里走直线？”——把空间展开成**镜像平铺**，再用**数论**（gcd/lcm）来找交点。这样往往能从 O(循环) 降到 O(常数)。