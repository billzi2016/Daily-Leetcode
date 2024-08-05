# #2813. K 长度子序列的最大优雅度 / Maximum Elegance of a K-Length Subsequence

> 难度：困难 · 标签：Array、Hash Table、Stack、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-elegance-of-a-k-length-subsequence/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array items of length n and an integer k.
items[i] = [profiti, categoryi], where profiti and categoryi denote the profit and category of the ith item respectively.
Let's define the elegance of a subsequence of items as total_profit + distinct_categories2, where total_profit is the sum of all profits in the subsequence, and distinct_categories is the number of distinct categories from all the categories in the selected subsequence.
Your task is to find the maximum elegance from all subsequences of size k in items.
Return an integer denoting the maximum elegance of a subsequence of items with size exactly k.
Note: A subsequence of an array is a new array generated from the original array by deleting some elements (possibly none) without changing the remaining elements' relative order.

**Examples**

**Example 1:**

```
Input: items = [[3,2],[5,1],[10,1]], k = 2
Output: 17
Explanation: In this example, we have to select a subsequence of size 2.
We can select items[0] = [3,2] and items[2] = [10,1].
The total profit in this subsequence is 3 + 10 = 13, and the subsequence contains 2 distinct categories [2,1].
Hence, the elegance is 13 + 22 = 17, and we can show that it is the maximum achievable elegance.
```

**Example 2:**

```
Input: items = [[3,1],[3,1],[2,2],[5,3]], k = 3
Output: 19
Explanation: In this example, we have to select a subsequence of size 3. 
We can select items[0] = [3,1], items[2] = [2,2], and items[3] = [5,3]. 
The total profit in this subsequence is 3 + 2 + 5 = 10, and the subsequence contains 3 distinct categories [1,2,3]. 
Hence, the elegance is 10 + 32 = 19, and we can show that it is the maximum achievable elegance.
```

**Example 3:**

```
Input: items = [[1,1],[2,1],[3,1]], k = 3
Output: 7
Explanation: In this example, we have to select a subsequence of size 3. 
We should select all the items. 
The total profit will be 1 + 2 + 3 = 6, and the subsequence contains 1 distinct category [1]. 
Hence, the maximum elegance is 6 + 12 = 7.
```

**Constraints**

- 1 <= items.length == n <= 105
- items[i].length == 2
- items[i][0] == profiti
- items[i][1] == categoryi
- 1 <= profiti <= 109
- 1 <= categoryi <= n
- 1 <= k <= n

---

## 题目（中文翻译）

你得到一个下标从 0 开始的二维整数数组 `items`，长度为 `n`，以及一个整数 `k`。  
`items[i] = [profiti, categoryi]`，其中 `profiti` 和 `categoryi` 分别表示第 `i` 件物品的利润和类别。

我们将一个子序列（subsequence）的 **优雅度** 定义为  

```
total_profit + distinct_categories^2
```

其中 `total_profit` 为子序列中所有利润的和，`distinct_categories` 为子序列中出现的不同类别的数量。

你的任务是从所有长度恰为 `k` 的子序列中找到最大优雅度，并返回该最大值。

> **注意**：数组的子序列是指在不改变剩余元素相对顺序的前提下，删除若干（可能为零）元素后得到的新数组。

## 示例

### 示例 1
**输入**  
```
items = [[3,2],[5,1],[10,1]], k = 2
```
**输出**  
```
17
```
**解释**  
本例需要选取大小为 2 的子序列。我们可以选择 `items[0] = [3,2]` 和 `items[2] = [10,1]`。  
子序列的 `total_profit` 为 `3 + 10 = 13`，且包含 2 种不同类别 `[2,1]`。  
因此优雅度为 `13 + 2^2 = 17`，且可以证明这是能够得到的最大优雅度。

### 示例 2
**输入**  
```
items = [[3,1],[3,1],[2,2],[5,3]], k = 3
```
**输出**  
```
19
```
**解释**  
本例需要选取大小为 3 的子序列。我们可以选择 `items[0] = [3,1]`、`items[2] = [2,2]` 和 `items[3] = [5,3]`。  
子序列的 `total_profit` 为 `3 + 2 + 5 = 10`，且包含 3 种不同类别 `[1,2,3]`。  
因此优雅度为 `10 + 3^2 = 19`，且可以证明这是最大可达的优雅度。

### 示例 3
**输入**  
```
items = [[1,1],[2,1],[3,1]], k = 3
```
**输出**  
```
7
```
**解释**  
本例需要选取大小为 3 的子序列。显然需要选取全部物品。  
`total_profit = 1 + 2 + 3 = 6`，仅有 1 种不同类别 `[1]`。  
因此最大优雅度为 `6 + 1^2 = 7`。

## 约束条件
- `1 <= items.length == n <= 10^5`
- `items[i].length == 2`
- `items[i][0] == profiti`
- `items[i][1] == categoryi`
- `1 <= profiti <= 10^9`
- `1 <= categoryi <= n`
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 长度为 `k` 的子序列都枚举一遍，分别算出  

```
elegance = (利润之和) + (不同类别数)²
```

把最大的 `elegance` 记下来就是答案。

> **数据结构类比**  
> - **列表**：像我们平时记账本，顺序保存每件商品的信息 `[profit, category]`。  
> - **集合（set）**：像一本字典，只关心出现过的单词（这里是类别），不在乎出现次数，用来快速统计 “不同类别数”。  
> - **组合生成**：把 `n` 本书挑 `k` 本的所有可能，类似把水果篮子里挑出 `k` 颗水果的所有取法。

只要把每一种取法的利润相加、统计不同的类别、算出优雅值，就能得到答案。

#### 代码（Python）

```python
from itertools import combinations

def max_elegance_bruteforce(items, k):
    """
    暴力枚举所有长度为 k 的子序列，返回最大 elegance。
    只适合 n 很小的情况（例如 n <= 20）。
    """
    best = 0
    # combinations 会保持原来的相对顺序，只是挑出下标的组合
    for idxs in combinations(range(len(items)), k):
        profit_sum = 0
        categories = set()
        for i in idxs:
            profit, cat = items[i]
            profit_sum += profit
            categories.add(cat)
        elegance = profit_sum + len(categories) ** 2
        best = max(best, elegance)
    return best
```

#### 复杂度  

- **时间复杂度**：`O( C(n, k) * k )`  
  - `C(n, k)` 是组合数，表示所有可能的子序列个数。  
  - 对每一种子序列我们要遍历 `k` 项求和并统计类别。  
  - 用大白话说，就是“先选出所有可能的 k 本书，然后每本书都要算一次”，随着 `n` 增大会指数级爆炸，根本跑不完。

- **空间复杂度**：`O(k)`（递归/迭代时保存当前组合的下标）  

> **结论**：暴力解只能用来验证思路或在极小的数据上跑通，面对 `n ≤ 10⁵` 时根本不可行。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**利润** 越大越好，**类别多** 也越好。  
如果我们先把利润最高的 `k` 件商品挑出来，利润和已经是最大的。但这一步可能会出现“重复类别”，导致 `distinct_categories` 较少，优雅值受限。

> **慢在哪里？**  
> - 暴力要枚举所有组合，根本不利用“利润高的更有价值”这一信息。  
> - 我们只需要在 **利润最高的前 k 件** 中挑出若干“可以换掉的重复品”，再用后面出现的 **新类别** 的商品去换。

#### 关键观察  

1. **先按利润降序排**，把最贵的 `k` 件放进候选集合 `selected`。  
2. 在 `selected` 中，**如果某个类别出现了多次**，其中利润最小的那件最适合被替换掉——因为换掉它对总利润的损失最小。我们把这些“可替换的重复品”放进一个 **最小堆**（`heap`），堆顶始终是当前利润最小的可换商品。  
3. 接下来遍历剩下的商品（仍然是按利润从大到小的顺序），**只关心那些类别在 `selected` 里还没有出现的商品**（称为 “新类别商品”）。  
   - 若堆非空，说明 `selected` 里有可以被换掉的重复品。  
   - 用当前新类别商品的利润 **替换** 堆顶（最小的重复品），这样：
     - 总利润 `profit_sum` 增加 `new.profit - removed.profit`（可能正，也可能负，但我们只在堆非空时尝试）。
     - 不同类别数 `distinct` 增加 `1`（因为加入了新类别）。
   - 计算新的优雅值 `profit_sum + distinct²`，更新答案。  

为什么这种贪心是最优的？  
- 我们一开始已经保证了 **利润的基线是最大的**（前 k 高利润）。  
- 每一次替换都 **以最小代价**（最小利润的重复品）换掉 **价值最高的未出现类别**（因为我们是按利润从大到小遍历的），这正是“在保证类别数尽可能多的前提下，保持利润尽可能大”。  
- 任何其他的替换方案要么换走的利润更大，要么换进的类别利润更小，都会导致优雅值不如我们这种方案。

#### 数据结构解释  

| 数据结构 | 类比 | 作用 |
|----------|------|------|
| **列表 `items`** | 商品清单 | 保存每件商品的利润和类别 |
| **集合 `used_categories`** | “已经收集的种类清单” | 快速判断一个类别是否已经出现（O(1)） |
| **最小堆 `duplicate_heap`** | “最便宜的可换商品箱子” | 随时可以弹出利润最小的重复品（O(log k)） |
| **变量 `profit_sum`、`distinct`** | “当前总利润”和“已有种类数” | 用来即时计算优雅值 |

#### 代码（Python）

```python
import heapq
from typing import List

def max_elegance(items: List[List[int]], k: int) -> int:
    """
    贪心 + 堆实现的最优解
    时间复杂度 O(n log n) ，空间复杂度 O(k)
    """
    # 1️⃣ 按利润从大到小排序
    items.sort(key=lambda x: -x[0])          # profit 降序

    profit_sum = 0               # 当前选中 k 件的利润和
    distinct = 0                 # 已有的不同类别数
    used = set()                 # 已出现的类别集合
    duplicate_heap = []          # 保存「可被替换的」重复商品的利润（最小堆）

    # 2️⃣ 先选前 k 件（利润最大的 k 件）
    for i in range(k):
        profit, cat = items[i]
        profit_sum += profit
        if cat in used:
            # 已经有同类别商品，这件可以作为以后换掉的候选
            heapq.heappush(duplicate_heap, profit)   # 只放利润，堆顶自然是最小的
        else:
            used.add(cat)
            distinct += 1

    # 初始答案：仅仅使用前 k 件的情况
    best = profit_sum + distinct * distinct

    # 3️⃣ 遍历剩余商品，尝试用「新类别」换掉「最便宜的重复品」
    for i in range(k, len(items)):
        profit, cat = items[i]
        # 只关心「新」类别，因为换入已有类别对 distinct 没帮助
        if cat in used:
            continue

        # 若堆为空，说明已经没有可以换掉的重复品了，后面也不可能再提升 distinct
        if not duplicate_heap:
            break

        # 取出当前堆中利润最小的可换商品
        removed_profit = heapq.heappop(duplicate_heap)

        # 更新累计利润和类别数
        profit_sum = profit_sum - removed_profit + profit
        distinct += 1
        used.add(cat)

        # 计算新状态下的 elegance，更新全局最大值
        best = max(best, profit_sum + distinct * distinct)

    return best
```

> **关键注释**  
> - `heapq.heappush(duplicate_heap, profit)`：把「可以被换掉的」重复商品放进最小堆，堆顶永远是当前利润最小的那件。  
> - `heapq.heappop(duplicate_heap)`：弹出最小利润的重复品，代表「以最小代价」进行一次替换。  
> - `if not duplicate_heap: break`：当没有可替换的重复品时，再也不可能增加类别数，直接结束循环，省时。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`。  
  - 维护堆的每一次 `push` / `pop` 均为 `O(log k)`，而总的堆操作次数不超过 `n`。  
  - 用大白话说，就是“先把商品排好序（像排队），然后每次换人都只需要在最前面找最便宜的那个人”。  

- **空间复杂度**：`O(k)`  
  - `used` 集合、`duplicate_heap` 堆以及前 `k` 件商品的累计信息最多保存 `k` 条记录。  
  - 与 `n` 成线性比例的额外空间几乎没有，基本只和选中的子序列大小有关。

> 与暴力解相比，时间从指数级降到了 **对数级**，能够轻松处理 `n=10⁵` 的大数据。

---

## 心得

- **核心技巧**：先按利润降序取前 `k` 件，再用最小堆把「利润最小的重复类别」换成「利润较大且类别新颖」的商品。  
- **适用的题型**  
  1. **需要在固定数量的选择中兼顾“价值最大”和“种类多”** 的问题（如 “Maximum Sum of Values with Unique Types”）。  
  2. **先选最高价值，再通过贪心换取额外属性** 的场景（如 “Maximum Score From Performing Multiplication Operations” 的变形）。  
- **一句话总结**：**“先抢利润最高的，再用最便宜的重复品换掉利润最高的新类别”** 是本题的解题钥匙。

---

## 反思

- **第一反应**：直接想遍历所有组合，写出暴力代码验证思路。  
- **最容易踩的坑**  
  - **忘记维护“重复品”堆**：如果只记录出现次数而不挑出最小利润的那件，可能会错误地换掉利润大的重复品，导致优雅值不最大。  
  - **边界条件**：当 `k` 恰好等于 `n` 时，后面的循环不应执行；当堆为空时必须提前退出，否则会尝试用不存在的商品换掉。  
  - **整数溢出**（在 Python 不会，但在其他语言要注意 `profit` 可达 `1e9`，`distinct²` 最高约 `1e10`）。  
- **下次遇到同类题**：第一步先 **排序 + 取前 k**，第二步 **用最小堆管理可替换的冗余**，然后 **遍历剩余元素尝试增种类**。这样就能把“价值最大 + 类别多”这两个目标统一起来。