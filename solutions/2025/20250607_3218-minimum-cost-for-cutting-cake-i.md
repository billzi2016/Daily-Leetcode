# #3218. **切蛋糕的最小成本 I** / Minimum Cost for Cutting Cake I

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-for-cutting-cake-i/)

---

## 题目（英文原版）

**Description**

There is an m x n cake that needs to be cut into 1 x 1 pieces.
You are given integers m, n, and two arrays:
In one operation, you can choose any piece of cake that is not yet a 1 x 1 square and perform one of the following cuts:
After the cut, the piece of cake is divided into two distinct pieces.
The cost of a cut depends only on the initial cost of the line and does not change.
Return the minimum total cost to cut the entire cake into 1 x 1 pieces.

**Examples**

**Example 1:**

```
Input: m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5]
Output: 13
Explanation:

The total cost is 5 + 1 + 1 + 3 + 3 = 13 .
```

**Example 2:**

```
Input: m = 2, n = 2, horizontalCut = [7], verticalCut = [4]
Output: 15
Explanation:
The total cost is 7 + 4 + 4 = 15 .
```

**Constraints**

- 1 <= m, n <= 20
- horizontalCut.length == m - 1
- verticalCut.length == n - 1
- 1 <= horizontalCut[i], verticalCut[i] <= 103

---

## 题目（中文翻译）

给定一个 **m × n** 的蛋糕，需要将其切割成全部 **1 × 1** 的小块。  
你会得到整数 `m`、`n`，以及两个数组：

- `horizontalCut`：长度为 `m‑1`，表示所有水平切割线的初始费用（cost）。
- `verticalCut`：长度为 `n‑1`，表示所有垂直切割线的初始费用（cost）。

在一次操作中，你可以选择任意尚未成为 **1 × 1** 正方形的蛋糕块，并执行以下两种切割方式之一：

1. 沿一条水平切割线切开，使该块蛋糕分成两个不相交的子块。
2. 沿一条垂直切割线切开，同样得到两个不相交的子块。

切割的费用仅取决于所选切割线的初始费用，切割次数不会影响费用本身。  
返回将整个蛋糕切割成全部 **1 × 1** 小块的 **最小总费用**（total cost）。

---

### 示例

**示例 1**

```text
Input: m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5]
Output: 13
Explanation:
总费用为 5 + 1 + 1 + 3 + 3 = 13。
```

**示例 2**

```text
Input: m = 2, n = 2, horizontalCut = [7], verticalCut = [4]
Output: 15
Explanation:
总费用为 7 + 4 + 4 = 15。
```

---

### 约束条件

- `1 <= m, n <= 20`
- `horizontalCut.length == m - 1`
- `verticalCut.length == n - 1`
- `1 <= horizontalCut[i], verticalCut[i] <= 10^3`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有切割的顺序都枚举一遍**，算出每一种顺序的总花费，最后取最小值。  
- **数据结构**：我们用两个列表 `h`、`v` 分别保存水平切线和垂直切线的费用。  
- **生活化类比**：把蛋糕想象成一本厚厚的书，每一条切线就像一本书的页码（费用），我们要把书拆成每页单独的纸。  
- **为什么正确**：只要把所有合法的切割顺序都尝试一遍，必然会碰到最优的那一种，所以答案一定会被找到。  
- **时间/空间复杂度**：  
  - 每一次切割都要在剩余的水平切线和垂直切线中任选一条，切完后递归处理得到的两个子矩形。  
  - 对于 `m` 行、`n` 列的蛋糕，需要切 `m‑1` 条水平线和 `n‑1` 条垂直线，总共 `m+n‑2` 步。所有可能的切割顺序数是 `(m+n‑2)!`（阶乘），随 `m,n` 增大非常快。  
  - 因此时间复杂度约为 **O((m+n)!)**，在最坏情况下几乎是指数级别。空间上只需要递归栈和记忆化表，最多 `O(m·n)`。  

> **大白话**：`O((m+n)!)` 就像你要把 10 本书排成所有可能的顺序，可能的排列数是 10! = 3,628,800，想象一下要跑多少遍！  

#### 代码（Python）  

```python
from functools import lru_cache
from typing import List

def minCost_bruteforce(m: int, n: int,
                       horizontalCut: List[int],
                       verticalCut: List[int]) -> int:
    # 为了方便，把切线费用从大到小排序（不影响暴力枚举，只是让递归顺序更统一）
    h = sorted(horizontalCut, reverse=True)
    v = sorted(verticalCut, reverse=True)

    @lru_cache(None)
    def dfs(h_idx: int, v_idx: int, h_seg: int, v_seg: int) -> int:
        """
        :param h_idx: 已经使用的水平切线数量（从左到右使用的下标）
        :param v_idx: 已经使用的垂直切线数量（从上到下使用的下标）
        :param h_seg: 当前矩形在水平方向被分成了多少段
        :param v_seg: 当前矩形在垂直方向被分成了多少段
        :return: 从当前状态把所有剩余切线全部切完的最小费用
        """
        # 所有切线都用完，说明已经是 1x1 小块了
        if h_idx == len(h) and v_idx == len(v):
            return 0

        best = float('inf')

        # 选一条水平切线（如果还有剩余）
        if h_idx < len(h):
            # 切这条线的费用会被当前的垂直段数 v_seg 放大
            cost = h[h_idx] * v_seg + dfs(h_idx + 1, v_idx, h_seg + 1, v_seg)
            best = min(best, cost)

        # 选一条垂直切线（如果还有剩余）
        if v_idx < len(v):
            # 切这条线的费用会被当前的水平段数 h_seg 放大
            cost = v[v_idx] * h_seg + dfs(h_idx, v_idx + 1, h_seg, v_seg + 1)
            best = min(best, cost)

        return best

    # 初始时只有 1 段水平、1 段垂直
    return dfs(0, 0, 1, 1)
```

**代码要点解释**  

- `@lru_cache(None)`：记忆化搜索，避免对相同子状态重复计算。相当于给每个“子问题”装上了标签（键），以后再来直接查表。  
- `h_seg`、`v_seg`：当前矩形在水平方向/垂直方向已经被切成了多少段。切一条水平线时，它会影响 **所有当前的垂直段**，所以费用要乘以 `v_seg`（同理垂直线乘以 `h_seg`）。  
- 递归的终止条件是所有切线都用完，说明已经得到 1×1 小块，费用为 0。  

#### 复杂度  

- **时间复杂度**：`O((m+n)!)`（所有切割顺序的枚举）。  
  - 这里的 `!` 表示阶乘，随着 `m,n` 增大，计算量会爆炸。  
- **空间复杂度**：`O(m·n)`（记忆化表的大小）+ 递归栈深度 `O(m+n)`。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**每一次切割的费用都会被“已有的段数”放大**。  
- 当我们切一条水平线时，费用会乘以当前的 **垂直段数**（因为这条线要把每一列都切开）。  
- 当我们切一条垂直线时，费用会乘以当前的 **水平段数**。  

这暗示了一个关键点：**把“贵的”切线尽早切**，这样它们乘上的段数会更小，从而整体费用更低。  

**优化步骤**  

1. **把所有水平切线和垂直切线分别按费用从大到小排序**。  
2. 维护两个计数器：  
   - `h_parts`：已经得到的水平段数（初始为 1）。  
   - `v_parts`：已经得到的垂直段数（初始为 1）。  
3. **贪心地从费用最大的切线开始**：  
   - 若当前最大的水平切线费用 ≥ 最大的垂直切线费用，先切这条水平线，费用 `horizontal[i] * v_parts`，然后 `h_parts += 1`。  
   - 否则切垂直线，费用 `vertical[j] * h_parts`，然后 `v_parts += 1`。  
4. 重复步骤 3，直到所有切线都用完。  

为什么这一步是最优的？  
- **局部最优等价全局最优**：在任意时刻，如果我们把一条费用更大的切线推迟到后面，它的乘数（另一方向的段数）只会变得 **不小于** 当前的乘数，因为段数是单调递增的。于是推迟只会让费用不降反升。  
- 这正是“**交换论证**”的核心：把两条切线的顺序调换，如果把费用大的那条提前，整体费用不会增加，反而可能降低。通过不断把费用大的切线提前，最终得到的顺序必然是最优的。  

**类比**：想象你在超市买东西，打折券的折扣力度不同。若你先用折扣最大的券，后面再用折扣小的券，总价会更低。这里的 “段数” 就相当于 “买的商品数量”，越早用大折扣，乘上的商品数量越少，省钱更多。  

#### 代码（Python）  

```python
from typing import List

def minCost_greedy(m: int, n: int,
                   horizontalCut: List[int],
                   verticalCut: List[int]) -> int:
    # 1. 按费用从大到小排序
    horizontal = sorted(horizontalCut, reverse=True)
    vertical   = sorted(verticalCut, reverse=True)

    # 2. 计数器，表示当前已经有多少段
    h_parts = 1          # 水平方向的段数
    v_parts = 1          # 垂直方向的段数

    i = j = 0            # 分别指向水平、垂直切线的当前位置
    total = 0

    # 3. 贪心取最大费用的切线
    while i < len(horizontal) and j < len(vertical):
        if horizontal[i] >= vertical[j]:
            # 先切水平线，费用乘以当前的垂直段数
            total += horizontal[i] * v_parts
            h_parts += 1
            i += 1
        else:
            # 先切垂直线，费用乘以当前的水平段数
            total += vertical[j] * h_parts
            v_parts += 1
            j += 1

    # 4. 处理剩余的切线（只能是一种方向了）
    while i < len(horizontal):
        total += horizontal[i] * v_parts
        i += 1
        h_parts += 1

    while j < len(vertical):
        total += vertical[j] * h_parts
        j += 1
        v_parts += 1

    return total
```

**代码要点解释**  

- `sorted(..., reverse=True)` 把费用最大的切线排在最前面，方便“一眼看出最大”。  
- `h_parts`、`v_parts` 初始为 1，表示整个蛋糕本身就是一段。每切一次对应方向的段数就加 1。  
- `while i < len(horizontal) and j < len(vertical)` 同时遍历两条列表，比较当前最大的两条费用，决定切哪条。  
- 当一种方向的切线全部用完后，剩下的只能按顺序全部切完。  

#### 复杂度  

- **时间复杂度**：`O(m log m + n log n)`  
  - 主要是对水平切线和垂直切线各自排序，需要 `log` 级的比较。排序之后的遍历都是线性的。  
  - 与暴力解的指数级时间相比，这几乎是瞬间完成的。  
- **空间复杂度**：`O(1)`（只用了若干计数器和临时变量），不需要额外的递归栈或记忆化表。  

---

## 心得  

- **核心技巧**：**贪心 + 乘数递增的思想**。  
  - 把费用大的切线尽早切，让它乘上的段数最小。  
- **适用的题型**：  
  1. “切木板”类问题（LeetCode 1547 Minimum Cost to Cut a Board into Squares）。  
  2. “拼图/合并”类的费用乘以已有块数的情形（如合并石子游戏的变种）。  
  3. “分割/拆分”费用随已分段数线性增长的调度问题。  
- **一句话总结解题钥匙**：**把最大的费用先付出，因段数只会增不减，能保证最小的累计乘积。**  

---

## 反思  

- **第一反应**：看到“费用乘以已有段数”，立刻想到“先切贵的”。  
- **最容易踩的坑**：  
  - 忘记把费用乘以 **另一方向的段数**（水平切线乘以垂直段数，反之亦然）。  
  - 忽略了可能出现的 **空列表**（比如 `m=1` 或 `n=1`），导致下标越界。  
  - 在实现时把排序顺序写反，导致小费用先被使用，结果不正确。  
- **下次遇到同类题**：第一步就检查“费用是否会被已有块数放大”，如果是，立刻考虑 **降序贪心**（把大费用提前），再验证是否满足交换论证。