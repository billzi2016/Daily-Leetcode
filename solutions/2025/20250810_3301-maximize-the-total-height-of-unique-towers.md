# #3301. 最大化唯一塔的总高度 / Maximize the Total Height of Unique Towers

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-the-total-height-of-unique-towers/)

---

## 题目（英文原版）

**Description**

You are given an array maximumHeight, where maximumHeight[i] denotes the maximum height the ith tower can be assigned.
Your task is to assign a height to each tower so that:
Return the maximum possible total sum of the tower heights. If it's not possible to assign heights, return -1.

**Examples**

**Example 1:**

```
Input: maximumHeight = [2,3,4,3]
Output: 10
Explanation:
We can assign heights in the following way: [1, 2, 4, 3] .
```

**Example 2:**

```
Input: maximumHeight = [15,10]
Output: 25
Explanation:
We can assign heights in the following way: [15, 10] .
```

**Example 3:**

```
Input: maximumHeight = [2,2,1]
Output: -1
Explanation:
It's impossible to assign positive heights to each index so that no two towers have the same height.
```

**Constraints**

- 1 <= maximumHeight.length <= 105
- 1 <= maximumHeight[i] <= 109

---

## 题目（中文翻译）

给定一个数组 `maximumHeight`，其中 `maximumHeight[i]` 表示第 *i* 座塔可以被分配的最大高度。  
你的任务是为每座塔分配一个高度，使得：

- 每座塔的高度为正整数，且不超过对应的 `maximumHeight[i]`；
- 所有塔的高度互不相同（unique）。

返回塔高度之和的最大可能值。如果不存在满足条件的分配方案，返回 `-1`。

## 示例

### 示例 1
**输入:** `maximumHeight = [2,3,4,3]`  
**输出:** `10`  
**解释:**  
我们可以按如下方式分配高度: `[1, 2, 4, 3]` 。

### 示例 2
**输入:** `maximumHeight = [15,10]`  
**输出:** `25`  
**解释:**  
我们可以按如下方式分配高度: `[15, 10]` 。

### 示例 3
**输入:** `maximumHeight = [2,2,1]`  
**输出:** `-1`  
**解释:**  
无法为每个下标分配正整数高度，使得没有两座塔的高度相同。

## 约束条件
- `1 <= maximumHeight.length <= 10^5`
- `1 <= maximumHeight[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一座塔的高度都枚举出来**，然后检查是否满足：

1. 第 `i` 座塔的高度 `h[i]` 必须是正整数且 `h[i] ≤ maximumHeight[i]`。  
2. 所有塔的高度必须互不相同（即集合 `h` 中没有重复值）。

可以把这件事想象成**给每座塔发放编号牌**，每张牌上写着一个正整数，高度不能超过它的上限，而且每张牌的号码必须唯一。  
暴力做法就是**把所有可能的号码组合都列举一遍**，挑出合法的组合并求出总和的最大值。

为什么这个方法一定能得到答案？因为它遍历了**全部**合法的高度分配方式，最大值必然在其中出现。  

但显然，这种“全排列”式的搜索会非常慢。假设第 `i` 座塔的上限是 `M_i`，则它可能的取值有 `M_i` 种（从 1 到 `M_i`），全部组合的数量是 `M_1 × M_2 × … × M_n`，即 **指数级**（随着塔的数量指数增长），在最坏情况下根本不可接受。

#### 代码（Python）

```python
from itertools import product

def max_total_height_bruteforce(maximumHeight):
    n = len(maximumHeight)
    # 1. 生成每座塔所有可能的取值（1 ~ maximumHeight[i]）
    candidates = [range(1, h + 1) for h in maximumHeight]

    best = -1                     # 记录当前找到的最大合法总和
    # 2. 枚举所有组合（暴力遍历）
    for heights in product(*candidates):
        # 3. 判断是否所有高度互不相同
        if len(set(heights)) == n:          # set 去重后长度仍是 n，说明没有重复
            total = sum(heights)            # 计算总和
            best = max(best, total)         # 更新最大值
    return best
```

> **注意**：上述代码仅用于说明思路，实际运行在 `n` 较大（如 10⁵）时会 **超时**，甚至根本无法在有限时间内结束。

#### 复杂度  

- **时间复杂度**：`O(Π M_i)`（每座塔的取值数相乘），相当于指数级增长。可以把 `O(2ⁿ)`、`O(10ⁿ)` 等大写的 **O** 看作“**随着 n 增长，耗时会像翻倍/十倍那样爆炸**”。  
- **空间复杂度**：`O(n)`，主要是存放递归/遍历时的当前组合 `heights`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们一次性考虑了所有可能的高度组合，而实际上只需要**一个合理的构造**就能得到最大总和。  

观察题目：

- 每座塔的高度必须唯一且不超过自己的上限 `maximumHeight[i]`。  
- 如果把所有塔的上限从大到小排好序（降序），则**越靠前的塔拥有的“自由度”越大**，它可以取到更高的值。  
- 为了让总和最大，我们希望**前面的塔取尽可能大的值，后面的塔则在前面塔已经占用了某些高度后，取下一个可用的最大值**。

这正好对应一种**贪心**策略：

1. **先把上限数组降序排列**。  
   类比：把一堆不同长度的木棍按从长到短排好，先把长的木棍安排好位置，短的再去找空位。  
2. **从左到右遍历**（即从最高的上限开始）。  
   - 第 `i` 座塔（0‑based）能够取的最大高度应该是  
     `allowed = min(maximumHeight[i], previous_height - 1)`  
     其中 `previous_height` 是前一座塔实际分配的高度。  
   - 解释：如果前一座塔已经占用了高度 `h_prev`，为了保证唯一性，当前塔的高度必须 **严格小于** `h_prev`，而且不能超过自己的上限 `maximumHeight[i]`，于是取两者的较小值。  
   - 特殊情况：对于第一座塔，没有前驱限制，只能取 `maximumHeight[0]`（因为已经是最大的上限）。  
3. **如果在某一步得到的 `allowed ≤ 0`，说明已经没有正整数可以分配**，此时题目要求返回 `-1`。  

这样遍历一次数组，就得到了一组合法且 **总和最大的** 高度分配。

#### 代码（Python）

```python
def max_total_height_greedy(maximumHeight):
    # 1. 降序排序，让大的上限先处理
    maximumHeight.sort(reverse=True)

    total = 0                # 累计总和
    prev = float('inf')      # 前一座塔的高度，初始设为无穷大（保证第一座可以直接取上限）

    for idx, limit in enumerate(maximumHeight):
        # 2. 当前塔能取的最大高度 = min(自己的上限, 前一座塔高度-1)
        cur = min(limit, prev - 1)

        # 3. 如果 cur 已经 <= 0，说明无法再分配正整数高度，直接返回 -1
        if cur <= 0:
            return -1

        total += cur          # 累加到答案
        prev = cur            # 更新前一座塔的高度供下次使用

    return total
```

**代码要点注释**：

- `maximumHeight.sort(reverse=True)`：把上限从大到小排，好比把“最高的山峰先登”，后面的山峰只能往下走一步步。  
- `prev = float('inf')`：把第一座塔的前驱高度设为无限大，这样 `min(limit, inf-1) = limit`，自然满足第一座塔可以直接取自己的上限。  
- `cur = min(limit, prev - 1)`：核心贪心公式，确保唯一性（比前一个小）且不超上限。  
- `if cur <= 0: return -1`：一旦出现非正数，说明已经没有合法正整数可以分配，题目要求返回 `-1`。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`，主要来自排序（`n` 为塔的数量）。排序是 `n log n`，遍历一次是 `O(n)`，两者相加仍是 `O(n log n)`。  
  - **含义**：如果塔的数量翻倍，运行时间大约会增加 `log₂(2) = 1` 倍的对数因子，即 **略微变慢**，但远远好于指数级的暴力。  
- **空间复杂度**：`O(1)`（不计输入数组本身），只用了常数级的额外变量 `total、prev、cur`。  

---

## 心得

- **核心技巧**：**贪心 + 降序排序**，把“最大的资源先分配”，后面的资源在前面的约束下取最大的可能值。  
- **适用的题型**  
  1. “**唯一且不超过上限**”的分配类问题，如 *Maximum Sum of Unique Numbers*。  
  2. “**递减序列**”约束的安排问题，如 *Maximum Number of Dishes*（每道菜的份数必须递减）。  
  3. “**限制递减**”的排队或排班问题，例如 *Maximum Profit in Job Scheduling* 的简化版。  
- **一句话总结解题钥匙**：**先把“大”安排好，再让“小”在剩余空间里尽可能“大”。**

---

## 反思

- **第一反应**：看到“唯一高度”和“上限”，自然想到**枚举**或**回溯**，于是想了暴力搜索。  
- **最容易踩的坑**  
  - 忘记**严格小于**前一个高度（`prev - 1`），导致出现相同高度的非法解。  
  - 没有处理 **`cur ≤ 0`** 的情况，直接返回错误的总和。  
  - 在排序时用了升序，导致贪心公式失效（需要降序）。  
- **下次遇到同类题**：第一步先**思考能否把约束转化为“从大到小依次取最大可行值”**，如果可以，立刻尝试 **排序 + 逐步递减** 的贪心构造。这样往往能把指数级的搜索直接压缩到 `O(n log n)`。