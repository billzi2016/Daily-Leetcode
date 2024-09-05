# #2857. 计数距离为 k 的点对 / Count Pairs of Points With Distance k

> 难度：中等 · 标签：Array、Hash Table、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/count-pairs-of-points-with-distance-k/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array coordinates and an integer k, where coordinates[i] = [xi, yi] are the coordinates of the ith point in a 2D plane.
We define the distance between two points (x1, y1) and (x2, y2) as (x1 XOR x2) + (y1 XOR y2) where XOR is the bitwise XOR operation.
Return the number of pairs (i, j) such that i < j and the distance between points i and j is equal to k.

**Examples**

**Example 1:**

```
Input: coordinates = [[1,2],[4,2],[1,3],[5,2]], k = 5
Output: 2
Explanation: We can choose the following pairs:
- (0,1): Because we have (1 XOR 4) + (2 XOR 2) = 5.
- (2,3): Because we have (1 XOR 5) + (3 XOR 2) = 5.
```

**Example 2:**

```
Input: coordinates = [[1,3],[1,3],[1,3],[1,3],[1,3]], k = 0
Output: 10
Explanation: Any two chosen pairs will have a distance of 0. There are 10 ways to choose two pairs.
```

**Constraints**

- 2 <= coordinates.length <= 50000
- 0 <= xi, yi <= 106
- 0 <= k <= 100

---

## 题目（中文翻译）

给定一个二维整数数组 `coordinates` 和一个整数 `k`，其中 `coordinates[i] = [x_i, y_i]` 表示平面上第 `i` 个点的坐标。  
我们定义两点 `(x_1, y_1)` 与 `(x_2, y_2)` 的距离为  

\[
(x_1 \text{ XOR } x_2) + (y_1 \text{ XOR } y_2)
\]

其中 **XOR** 为按位异或（exclusive OR）运算。  

返回满足 `i < j` 且点 `i` 与点 `j` 的距离等于 `k` 的所有点对 `(i, j)` 的数量。

### 示例

#### 示例 1
**输入**  
```text
coordinates = [[1,2],[4,2],[1,3],[5,2]], k = 5
```
**输出**  
```text
2
```
**解释**  
我们可以选取以下两对点：
- `(0,1)`：因为 `(1 XOR 4) + (2 XOR 2) = 5`。
- `(2,3)`：因为 `(1 XOR 5) + (3 XOR 2) = 5`。

#### 示例 2
**输入**  
```text
coordinates = [[1,3],[1,3],[1,3],[1,3],[1,3]], k = 0
```
**输出**  
```text
10
```
**解释**  
任意两点之间的距离都是 `0`。共有 `10` 种选择两点的方式。

### 约束条件
- `2 <= coordinates.length <= 50000`
- `0 <= x_i, y_i <= 10^6`
- `0 <= k <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有点两两配对，逐个计算它们的「距离」  
\[
\text{dist}((x_1,y_1),(x_2,y_2)) = (x_1 \oplus x_2) + (y_1 \oplus y_2)
\]  
（`\oplus` 表示按位异或）。如果得到的和正好等于给定的 `k`，计数器加一。

- **用到的数据结构**：只需要一个普通的列表 `coordinates` 来存放点。  
  没有额外的结构，整个过程像在找“好朋友”——把每个人（点）和所有其他人都聊一遍，看看聊天的“距离”是否正好是 `k`。

- **为什么正确**：我们枚举了 **所有** 可能的 `(i, j)`（`i < j`），只要把每对的距离算出来并和 `k` 比较，就不可能漏掉任何符合条件的配对。

- **复杂度分析**  
  - 外层循环遍历 `n` 个点，内层循环又遍历剩下的 `n‑1、n‑2 …`，总共约 \(\frac{n(n-1)}{2}\) 次比较。  
  - 用大白话说，这就是 **\(O(n^2)\)**，即“平方级”。当 `n` 达到 5 万时，\(n^2\) 已经是 2.5 × 10⁹，几乎不可能在一秒内算完。  
  - 额外空间只用了常数级的几个变量，**\(O(1)\)**。

#### 代码（Python）

```python
from typing import List

def countPairs_bruteforce(coordinates: List[List[int]], k: int) -> int:
    n = len(coordinates)
    ans = 0
    # 两层循环枚举所有 i < j 的组合
    for i in range(n):
        x1, y1 = coordinates[i]
        for j in range(i + 1, n):
            x2, y2 = coordinates[j]
            # 计算距离 (x1 XOR x2) + (y1 XOR y2)
            dist = (x1 ^ x2) + (y1 ^ y2)
            if dist == k:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要遍历所有点对，随着点的数量呈平方增长。  
- **空间复杂度**：`O(1)` —— 只用了几个临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历所有已出现的点** 来求距离。  
我们可以把“已经出现的点”用一个**哈希表**（在 Python 中就是 `dict` 或 `Counter`）记下来，这样查询是否存在某个点只需要 **常数时间**。

关键观察（提示里已经给出）：

1. 设  
   \[
   x = x_1 \oplus x_2,\quad y = y_1 \oplus y_2
   \]  
   那么  
   \[
   x_2 = x_1 \oplus x,\quad y_2 = y_1 \oplus y
   \]  
   因为异或有 “自反” 与 “可逆” 的特性：`a ^ b ^ b == a`。

2. 题目要求 `x + y = k`。  
   因此只要枚举所有可能的 `x`（从 `0` 到 `k`），对应的 `y` 就是 `k - x`。  
   对于当前点 `(x1, y1)`，**目标点** 必须满足  
   \[
   (x_2, y_2) = (x_1 \oplus x,\; y_1 \oplus (k - x))
   \]  

3. 如果我们在遍历点的过程中，已经把之前出现过的点存进哈希表 `cnt`（键是点的坐标，值是出现次数），  
   那么对当前点只要检查 `cnt[target]` 就能得到**有多少个已经出现的点** 与它的距离恰好是 `k`。  
   这样每个点只需要 **遍历 `k+1` 次**（`x` 的所有取值），而不是遍历所有已出现的点。

因为 `k ≤ 100`，`k+1` 最多只有 101 次循环，整体复杂度是 **\(O(n·k)\)**，即 **线性**（对 `n`）且常数很小。

**类比**：  
- 哈希表就像一本“点的电话簿”，把每个坐标映射到它出现的次数。  
- 查找某个坐标是否在电话簿里，就像查字典的页码——几乎瞬间就能找到（常数时间）。

#### 代码（Python）

```python
from collections import Counter
from typing import List, Tuple

def countPairs(coordinates: List[List[int]], k: int) -> int:
    """
    使用哈希表 + 枚举 x (0..k) 的方式统计满足距离为 k 的点对数。
    """
    cnt = Counter()               # 记录已经遍历过的点出现次数，键是 (x, y) 元组
    ans = 0

    for x1, y1 in coordinates:    # 按顺序遍历每个点，保证 i < j
        # 枚举 x = (x1 XOR x2) 的所有可能取值
        for x in range(k + 1):
            y = k - x              # 对应的 y = (y1 XOR y2) 必须满足 x + y = k
            # 根据异或的可逆性，算出满足条件的“另一端”点坐标
            target = (x1 ^ x, y1 ^ y)
            # cnt 中已有的 target 点就构成合法配对
            ans += cnt[target]

        # 把当前点加入哈希表，供后面的点使用
        cnt[(x1, y1)] += 1

    return ans
```

> **代码要点解释**  
> 1. `cnt[(x1, y1)] += 1` —— 把当前点记下来，后面更靠后的点可以把它当作“左侧点”。  
> 2. `for x in range(k + 1):` —— `x` 只需要遍历 `0~k`，因为 `x` 与 `y` 都是非负整数且 `x + y = k`。  
> 3. `target = (x1 ^ x, y1 ^ y)` —— 通过异或的“可逆”特性直接算出对应的点坐标。  
> 4. `ans += cnt[target]` —— 哈希表的查询是 O(1)，所以每次只需要常数时间。

#### 复杂度

- **时间复杂度**：`O(n·(k+1))` ≈ `O(n·k)`。  
  - 对每个点我们遍历 `k+1 ≤ 101` 次，查表是常数时间。  
  - 与暴力的 `O(n²)` 相比，**快了好几个数量级**，在 5 万点的极限数据下也能轻松跑完。

- **空间复杂度**：`O(n)`。  
  - 最坏情况下所有点都不相同，需要把每个点存进哈希表。  
  - 这相当于“一本点的电话簿”，大小随输入点数线性增长。

---

## 心得

- **核心技巧**：利用 **异或的可逆性** + **哈希表**，把原本的“遍历所有已出现点”转化为 “枚举固定次数、快速查询”。  
- **适用场景**  
  1. “两数异或和等于给定值” 这类问题（如 LeetCode 1725 `Number Of Rectangles That Can Form The Largest Square` 的变形）。  
  2. 任意需要 **“已出现的元素”快速计数** 的配对问题，例如 `k` 差值配对、`k` 和配对等。  
- **一句话总结**：**把“找配对”变成“在字典里找目标”，枚举的范围只跟 `k` 有关，复杂度从平方降到线性。**

---

## 反思

- **第一反应**：直接两层循环枚举所有点对——因为这最容易写、最不容易出错。  
- **最容易踩的坑**  
  1. **忘记 `i < j` 的顺序**：如果不按顺序统计，可能会把同一对算两次。解决办法是“先查询后加入”哈希表。  
  2. **`k = 0` 的特殊情况**：此时 `x = 0, y = 0`，目标点恰好是自己，需要利用哈希表中已经出现的相同点的计数来得到组合数。  
  3. **整数范围**：异或结果仍在 `[0, 2^20)`（因为 `xi, yi ≤ 10⁶`），不会溢出，仍可安全使用 Python 的普通整数。  
- **下次遇到同类题**：第一步先**把“距离公式”用异或写成 `x = a1 ^ a2`、`y = b1 ^ b2`，再**枚举 `x`（或 `y`）的所有可能**，利用哈希表把 “已经出现的点” 快速查到。这样就能立刻把暴力的 `O(n²)` 降到 `O(n·k)`。