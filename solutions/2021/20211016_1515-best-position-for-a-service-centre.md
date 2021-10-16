# #1515. **最佳服务中心位置** / Best Position for a Service Centre

> 难度：困难 · 标签：Array、Math、Geometry、Randomized · [LeetCode 链接](https://leetcode.com/problems/best-position-for-a-service-centre/)

---

## 题目（英文原版）

**Description**

A delivery company wants to build a new service center in a new city. The company knows the positions of all the customers in this city on a 2D-Map and wants to build the new center in a position such that the sum of the euclidean distances to all customers is minimum.
Given an array positions where positions[i] = [xi, yi] is the position of the ith customer on the map, return the minimum sum of the euclidean distances to all customers.
In other words, you need to choose the position of the service center [xcentre, ycentre] such that the following formula is minimized:
Answers within 10-5 of the actual value will be accepted.

**Examples**

**Example 1:**

```
Input: positions = [[0,1],[1,0],[1,2],[2,1]]
Output: 4.00000
Explanation: As shown, you can see that choosing [xcentre, ycentre] = [1, 1] will make the distance to each customer = 1, the sum of all distances is 4 which is the minimum possible we can achieve.
```

**Example 2:**

```
Input: positions = [[1,1],[3,3]]
Output: 2.82843
Explanation: The minimum possible sum of distances = sqrt(2) + sqrt(2) = 2.82843
```

**Constraints**

- 1 <= positions.length <= 50
- positions[i].length == 2
- 0 <= xi, yi <= 100

---

## 题目（中文翻译）

一个快递公司计划在新城市建立一个服务中心。公司已经知道该城市中所有客户在二维平面（2D-Map）上的坐标，想要把服务中心建在一个位置，使得到所有客户的欧几里得距离（euclidean distance）之和最小。

给定数组 `positions`，其中 `positions[i] = [xi, yi]` 表示第 `i` 位客户在地图上的位置，返回使所有客户的欧几里得距离之和最小的值。

换句话说，你需要选择服务中心的位置 `[xcentre, ycentre]`，使得下面的公式取得最小值：

```
∑ sqrt( (xi - xcentre)^2 + (yi - ycentre)^2 )
```

答案只要在实际值的 `10^-5` 以内即可接受。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

**示例 1**  
输入: `positions = [[0,1],[1,0],[1,2],[2,1]]`  
输出: `4.00000`  
解释: 如图所示，选择 `[xcentre, ycentre] = [1, 1]` 时，每位客户到中心的距离均为 1，所有距离之和为 4，这是能够达到的最小值。

**示例 2**  
输入: `positions = [[1,1],[3,3]]`  
输出: `2.82843`  
解释: 最小的距离和为 `sqrt(2) + sqrt(2) = 2.82843`

### 约束条件

- `1 <= positions.length <= 50`
- `positions[i].length == 2`
- `0 <= xi, yi <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的建中心位置都尝试一遍**，然后挑出距离和最小的那个。  
因为我们只会在**二维平面**上放点，最容易想到的“所有可能的位置”就是**把每个顾客的位置都当作候选点**，甚至可以把两点连线上的所有点都枚举（把坐标离散化成很细的网格），只要把每个候选点和所有顾客算一次欧氏距离的和，就能得到答案。

- **用到的数据结构**：  
  - `list` 保存所有候选点（这里直接使用 `positions` 本身）。  
  - `float` 用来累计距离和。  
  - **哈希表**（字典）在本解法里其实不需要，但如果我们想把“网格点 → 已算过的距离和”缓存起来，哈希表就像一本**查字典**：键是坐标，值是对应的距离和，避免重复计算。

- **为什么它一定能得到正确答案**：  
  - 只要我们把**所有可能的建中心位置**都列出来，遍历一次必然会找到最优的那个。  
  - 把每个顾客的位置本身当作候选点是合法的（因为答案可以恰好落在某个顾客处），所以最差情况下我们也能得到一个可行解。  

- **时间/空间复杂度**（大白话版）：  
  - 假设我们只枚举 `n`（顾客数）个候选点，每次都要把 **所有 `n` 位顾客** 的距离算一遍。  
  - 这相当于 **“一遍遍历 n，另一遍再遍历 n”**，所以总共要做 `n × n = n²` 次距离计算。  
  - 用数学符号写就是 **O(n²)**，也就是“随顾客数量的平方增长”。如果 `n = 50`，最多只要算 2500 次，算力足够。  
  - 空间上我们只保存原始的 `positions`，所以是 **O(1)**（常数级）额外空间。

#### 代码（Python）

```python
import math
from typing import List

def min_total_distance_bruteforce(positions: List[List[int]]) -> float:
    """
    暴力枚举每个顾客的位置作为服务中心候选点，计算所有顾客到该点的欧氏距离之和，
    取最小值返回。时间复杂度 O(n²)，空间复杂度 O(1)。
    """
    n = len(positions)
    best = float('inf')                     # 当前找到的最小距离和

    for cx, cy in positions:                # 把每个顾客的坐标 (cx,cy) 当作候选中心
        total = 0.0
        for x, y in positions:              # 计算所有顾客到 (cx,cy) 的距离并累加
            dx = x - cx
            dy = y - cy
            total += math.hypot(dx, dy)      # math.hypot(dx,dy) = sqrt(dx²+dy²)
        best = min(best, total)              # 保留最小的距离和

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - **含义**：如果顾客数量翻倍，计算量会变成原来的四倍（因为要比较的对数是 n²）。
- **空间复杂度**：`O(1)`（不计输入数组）  
  - **含义**：除了存放几个临时变量外，几乎不需要额外的内存。

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于我们只考虑了离散的候选点（顾客本身），但**几何中位点（Geometric Median）**——使所有点到它的欧氏距离之和最小的点——往往不在任何一个顾客的位置上。  
所以我们需要一种**可以在连续平面上搜索最优点**的方法，而不是穷举离散点。

**核心思路：Weiszfeld 算法**（也叫**加权质心迭代**）  
- 把几何中位点看作一种“加权平均”。  
- 每一次迭代，根据当前的中心 `(x, y)`，把每个顾客的坐标按 **距离的倒数** 加权求和，得到新的中心。  
- 公式如下（假设第 `i` 个顾客坐标为 `(xi, yi)`，`d_i` 为它到当前中心的距离）：

\[
x_{new} = \frac{\sum_{i=1}^{n} \frac{x_i}{d_i}}{\sum_{i=1}^{n} \frac{1}{d_i}}, \quad
y_{new} = \frac{\sum_{i=1}^{n} \frac{y_i}{d_i}}{\sum_{i=1}^{n} \frac{1}{d_i}}
\]

- 直观类比：**把每个人的力量“靠近”中心的程度（距离越近力量越大）加起来，重新找一个“力量平衡点”。**  
- 只要 **当前中心不恰好和某个顾客重合**（如果相等，距离为 0，倒数会炸），该迭代会快速收敛到全局最优的几何中位点。  
- 为防止除以 0 的情况，如果迭代点恰好落在某个顾客位置，直接返回该点即可——它必然是局部最优且满足题目要求。

**为什么它比暴力更快**  
- 每一次迭代只需要 **一次遍历所有点**（O(n)），而迭代次数通常在 50~200 次以内即可满足 `1e-5` 的精度要求。  
- 总体时间复杂度 **O(iterations × n)**，在本题的约束 `n ≤ 50` 下几乎是瞬间完成。  

**实现细节**（从零解释）  
1. **初始化**：可以随意选一个点做起点，常用 **所有点的算术平均**（即普通均值）因为它已经在点云的“中心”。  
2. **迭代**：按照上面的公式计算新坐标。  
3. **收敛判定**：如果新旧坐标的欧氏距离小于 `1e-7`（一个非常小的阈值），说明已经足够接近最优解，直接退出。  
4. **返回答案**：遍历完所有顾客，算一次 **总距离** 并返回。  

#### 代码（Python）

```python
import math
from typing import List

def geometric_median(positions: List[List[int]]) -> float:
    """
    Weiszfeld 算法求几何中位点（使欧氏距离和最小的点）。
    时间复杂度 O(iterations * n)，空间复杂度 O(1)。
    """
    # 1️⃣ 初始点：所有点的算术平均（普通均值），相当于“质心”
    x = sum(p[0] for p in positions) / len(positions)
    y = sum(p[1] for p in positions) / len(positions)

    eps = 1e-7               # 收敛阈值：坐标变化小于这个值就认为已经收敛
    max_iter = 10000         # 防止万一不收敛，最多迭代这么多次

    for _ in range(max_iter):
        num_x = 0.0          # 分子 Σ (xi / di)
        num_y = 0.0
        den = 0.0            # 分母 Σ (1 / di)

        # 2️⃣ 对每个顾客累加权重
        for xi, yi in positions:
            dx = xi - x
            dy = yi - y
            dist = math.hypot(dx, dy)

            # 如果当前点恰好落在某个顾客位置，直接返回该点
            if dist < eps:          # 防止除以 0
                x, y = xi, yi
                break

            weight = 1.0 / dist
            num_x += xi * weight
            num_y += yi * weight
            den   += weight

        # 3️⃣ 计算新中心
        new_x = num_x / den
        new_y = num_y / den

        # 4️⃣ 判断是否收敛
        if math.hypot(new_x - x, new_y - y) < eps:
            x, y = new_x, new_y
            break

        x, y = new_x, new_y

    # 5️⃣ 计算最小的距离和并返回
    total = sum(math.hypot(px - x, py - y) for px, py in positions)
    return total
```

#### 复杂度  

- **时间复杂度**：`O(iterations * n)`，通常 `iterations` 在 50~200 之间。  
  - **含义**：如果顾客数翻倍，计算量大约也会翻倍；但相比暴力的 `O(n²)`，这里是 **线性** 增长，明显更快。  
- **空间复杂度**：`O(1)`（只用常数个临时变量），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**Weiszfeld 迭代（几何中位点）**——把距离的倒数当作权重，反复求加权平均，直到坐标不再明显变化。  
- **适用的题型**（类似技巧）  
  1. **Geometric Median / Weber Problem**（本题）  
  2. **最小化 Manhattan 距离和的点**（可用一维中位数）  
  3. **求最小化欧氏距离平方和的点**（即普通均值，直接算均值即可）  
- **一句话总结解题钥匙**：**把每个点的“影响力”设为离它越近影响越大（1 / 距离），不断让中心向“影响力加权的平均”靠拢，就会收敛到全局最优的几何中位点。**

---

## 反思  

- **拿到题目第一反应**：把所有点的坐标直接枚举（暴力），因为题目只要求“最小距离和”。  
- **最容易踩的坑**  
  - **除以 0**：在迭代过程中若中心恰好与某个顾客重合，距离为 0，倒数会炸。必须检测并直接返回该点。  
  - **收敛阈值选取**：题目要求 `1e-5` 的误差，实际迭代时要使用更小的阈值（如 `1e-7`）确保最终误差在容忍范围内。  
  - **边界条件**：只有一个顾客时，答案就是 0；代码需要能正常处理 `n = 1` 的情况。  
- **下次遇到同类题，第一步该想到**：**是否可以把目标函数写成“加权平均”形式？**如果可以，用 **Weiszfeld** 或 **梯度下降** 之类的迭代方法直接在连续空间搜索，而不是离散枚举。这样既能保证精度，又能在大规模数据下保持高效。