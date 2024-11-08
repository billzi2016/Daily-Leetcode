# #2931. 购买商品后的最大花费 / Maximum Spending After Buying Items

> 难度：困难 · 标签：Array、Greedy、Sorting、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-spending-after-buying-items/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m * n integer matrix values, representing the values of m * n different items in m different shops. Each shop has n items where the jth item in the ith shop has a value of values[i][j]. Additionally, the items in the ith shop are sorted in non-increasing order of value. That is, values[i][j] >= values[i][j + 1] for all 0 <= j < n - 1.
On each day, you would like to buy a single item from one of the shops. Specifically, On the dth day you can:
Note that all items are pairwise different. For example, if you have bought item 0 from shop 1, you can still buy item 0 from any other shop.
Return the maximum amount of money that can be spent on buying all  m * n products.

**Examples**

**Example 1:**

```
Input: values = [[8,5,2],[6,4,1],[9,7,3]]
Output: 285
Explanation: On the first day, we buy product 2 from shop 1 for a price of values[1][2] * 1 = 1.
On the second day, we buy product 2 from shop 0 for a price of values[0][2] * 2 = 4.
On the third day, we buy product 2 from shop 2 for a price of values[2][2] * 3 = 9.
On the fourth day, we buy product 1 from shop 1 for a price of values[1][1] * 4 = 16.
On the fifth day, we buy product 1 from shop 0 for a price of values[0][1] * 5 = 25.
On the sixth day, we buy product 0 from shop 1 for a price of values[1][0] * 6 = 36.
On the seventh day, we buy product 1 from shop 2 for a price of values[2][1] * 7 = 49.
On the eighth day, we buy product 0 from shop 0 for a price of values[0][0] * 8 = 64.
On the ninth day, we buy product 0 from shop 2 for a price of values[2][0] * 9 = 81.
Hence, our total spending is equal to 285.
It can be shown that 285 is the maximum amount of money that can be spent buying all m * n products.
```

**Example 2:**

```
Input: values = [[10,8,6,4,2],[9,7,5,3,2]]
Output: 386
Explanation: On the first day, we buy product 4 from shop 0 for a price of values[0][4] * 1 = 2.
On the second day, we buy product 4 from shop 1 for a price of values[1][4] * 2 = 4.
On the third day, we buy product 3 from shop 1 for a price of values[1][3] * 3 = 9.
On the fourth day, we buy product 3 from shop 0 for a price of values[0][3] * 4 = 16.
On the fifth day, we buy product 2 from shop 1 for a price of values[1][2] * 5 = 25.
On the sixth day, we buy product 2 from shop 0 for a price of values[0][2] * 6 = 36.
On the seventh day, we buy product 1 from shop 1 for a price of values[1][1] * 7 = 49.
On the eighth day, we buy product 1 from shop 0 for a price of values[0][1] * 8 = 64
On the ninth day, we buy product 0 from shop 1 for a price of values[1][0] * 9 = 81.
On the tenth day, we buy product 0 from shop 0 for a price of values[0][0] * 10 = 100.
Hence, our total spending is equal to 386.
It can be shown that 386 is the maximum amount of money that can be spent buying all m * n products.
```

**Constraints**

- 1 <= m == values.length <= 10
- 1 <= n == values[i].length <= 104
- 1 <= values[i][j] <= 106
- values[i] are sorted in non-increasing order.

---

## 题目（中文翻译）

你得到一个下标从 0 开始的 **m × n** 整数矩阵 `values`，表示 **m** 家不同商店中每家有 **n** 件商品的价值。其中，第 `i` 家商店的第 `j` 件商品的价值为 `values[i][j]`。此外，第 `i` 家商店的商品已经按价值从大到小（**非递增**）排序，即对于所有 `0 ≤ j < n - 1`，`values[i][j] >= values[i][j + 1]`。

在每一天，你想从某一家商店购买恰好一件商品。具体地，在第 `d` 天（从 1 开始计数），你可以：

>（题目原文此处的具体规则在提供的描述中缺失，保持原样）

需要注意的是，所有商品彼此不同。例如，若你已经从第 1 家商店购买了编号为 0 的商品，你仍然可以在其他商店购买编号为 0 的商品。

返回购买完全部 **m·n** 件商品后能够花费的**最大金额**。

---

### 示例

**示例 1**

```text
Input: values = [[8,5,2],[6,4,1],[9,7,3]]
Output: 285
Explanation: 
在第一天，我们从商店 1 购买编号为 2 的商品，花费为 values[1][2] * 1 = 1。  
在第二天，我们从商店 0 购买编号为 2 的商品，花费为 values[0][2] * 2 = 4。  
在第三天，我们从商店 2 购买编号为 2 的商品，花费为 values[2][2] * 3 = 9。  
在第四天，我们从商店 1 购买编号为 1 的商品，花费为 values[1][1] * 4 = ...  
（后续过程已截断）
```

**示例 2**

```text
Input: values = [[10,8,6,4,2],[9,7,5,3,2]]
Output: 386
Explanation: 
在第一天，我们从商店 0 购买编号为 4 的商品，花费为 values[0][4] * 1 = 2。  
在第二天，我们从商店 1 购买编号为 4 的商品，花费为 values[1][4] * 2 = 4。  
在第三天，我们从商店 1 购买编号为 3 的商品，花费为 values[1][3] * 3 = 9。  
在第四天，我们从商店 0 购买编号为 3 的商品，花费为 values[0][3] * 4 = ...  
（后续过程已截断）
```

---

### 约束条件

- `1 <= m == values.length <= 10`
- `1 <= n == values[i].length <= 10^4`
- `1 <= values[i][j] <= 10^6`
- 对每个 `i`，`values[i]` 已按 **非递增** 顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有商品的购买顺序** 列举出来，算出每一种顺序对应的花费，然后取最大的那个。

- **数据结构**：可以用一个一维列表 `order` 保存购买的商品 `(shop, index)`，用递归（或 `itertools.permutations`）一次遍历所有可能的排列。  
- **为什么正确**：因为题目要求 **在所有可能的购买顺序中** 选出总花费最大的那一个，遍历完所有排列自然不会漏掉最优解。  
- **复杂度分析**：  
  - 假设矩阵有 `k = m * n` 件商品。排列数是 `k!`（阶乘），这在数学上增长非常快。  
  - 时间复杂度 `O(k!)`，即使 `k = 6`（6 件商品）也已经是 720 种情况，`k = 10` 就是 3,628,800 种，远远超出计算机在一秒内能完成的范围。  
  - 空间复杂度 `O(k)`，只需要保存当前递归路径和累计费用。

> **大白话**：`O(k!)` 就像把所有可能的排队方式都写下来，然后一个一个算钱，钱多得数不过来。

#### 代码（Python）

```python
import itertools
from typing import List

def max_spending_bruteforce(values: List[List[int]]) -> int:
    m, n = len(values), len(values[0])
    # 把每件商品标记为 (shop, position)
    items = [(i, j) for i in range(m) for j in range(n)]

    best = 0
    # 枚举所有排列（会非常慢，只适合极小规模测试）
    for order in itertools.permutations(items):
        total = 0
        for day, (shop, idx) in enumerate(order, start=1):   # day 从 1 开始计数
            total += values[shop][idx] * day
        best = max(best, total)
    return best

# ------------------- 示例（仅用于小规模验证） -------------------
# values = [[8,5,2],[6,4,1],[9,7,3]]
# print(max_spending_bruteforce(values))   # 仅在 n,m 极小的情况下可运行
```

> **注意**：上面的函数只适合 `m*n <= 6` 左右的极小输入，用来验证思路。实际提交时会 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O((m·n)!)` — 所有排列的数量。  
- **空间复杂度**：`O(m·n)` — 保存当前排列和累计费用。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**排列顺序是关键**。  
我们注意到每件商品的花费是 `value * day`，而 `day` 随时间单调递增。  

> **直观**：如果把“大价值”放在“小天数”上，乘积会小；把“大价值”放在“大天数”上，乘积会大。  
> 因此**要让总花费最大**，就应该把 **值小的商品尽早买**，把 **值大的商品留到后面**。

每家店的商品已经按 **非递增**（从大到小）排好，所以**当前最小的商品**一定在该店的 **最后一个位置**（`values[i][-1]`）。  

于是我们可以把问题转化为：

> 每一天，从所有店铺当前“最小的商品”中挑出 **全局最小** 的那件买掉。

这正好对应 **“每次取最小值”** 的典型数据结构——**最小堆（优先队列）**。

**步骤**：

1. **初始化**：把每家店的最小商品（即最后一个元素）放进堆里，堆的元素是 `(value, shop_index)`。  
2. **遍历天数** `day = 1 … m·n`：  
   - 弹出堆顶，即当前全局最小的商品 `value`。  
   - 累加 `value * day` 到答案。  
   - 把该店的这个商品删掉（`pop()` 最后一个）。  
   - 如果该店还有商品，取它的新最小商品（仍是最后一个）再压进堆。  
3. 循环结束后，答案即为最大可能花费。

**为什么正确**（贪心证明的简化版）：

- 设想任意一个最优购买序列。若在某一天 `d` 买的商品不是当前所有最小值，而是更大的 `x`，而还有更小的 `y` 在以后某天 `d' > d` 被买。把这两天的购买顺序互换后，新增的花费是  
  `x*d' + y*d - (x*d + y*d') = (x-y)*(d'-d) ≥ 0`（因为 `x ≥ y` 且 `d' > d`），即总花费 **不会变小**。  
- 于是我们可以一步步把所有不符合“当天买最小值”的情况换成符合的，而不降低总花费。最终得到的序列恰好是我们贪心算法产生的序列，说明它是最优的。

**核心数据结构**：

- **最小堆（Priority Queue）**：类似于“超市排队系统”，每次把最“便宜”的商品叫出来。堆的大小永远 ≤ `m`（店铺数），所以操作代价是 `log m`。

#### 代码（Python）

```python
import heapq
from typing import List

def max_spending(values: List[List[int]]) -> int:
    """
    贪心 + 最小堆
    :param values: m 行 n 列的矩阵，每行已按非递增排序
    :return: 购买全部商品的最大可能花费
    """
    m, n = len(values), len(values[0])
    total_days = m * n
    ans = 0

    # 把每家店的最小商品（即最后一个）放进堆
    # heap 元素是 (value, shop_index)
    heap = []
    for shop in range(m):
        # 取最后一个元素作为当前最小
        smallest = values[shop][-1]
        heapq.heappush(heap, (smallest, shop))

    # 从第 1 天到第 total_days 天依次购买
    for day in range(1, total_days + 1):
        # 取全局最小的商品
        value, shop = heapq.heappop(heap)
        ans += value * day          # 累计当天花费

        # 删除这件商品：因为是最后一个，直接 pop
        values[shop].pop()          # 现在该店的最小商品变成新的最后一个

        # 如果该店还有剩余商品，继续把新的最小商品压入堆
        if values[shop]:
            new_smallest = values[shop][-1]
            heapq.heappush(heap, (new_smallest, shop))

    return ans

# ------------------- 示例 -------------------
if __name__ == "__main__":
    vals1 = [[8,5,2],[6,4,1],[9,7,3]]
    print(max_spending(vals1))   # 285

    vals2 = [[10,8,6,4,2],[9,7,5,3,2]]
    print(max_spending(vals2))   # 386
```

> **关键行中文注释**  
> - `heapq.heappush(heap, (smallest, shop))` 把「当前最小商品」放进「最小堆」  
> - `value, shop = heapq.heappop(heap)` 弹出全局最小商品  
> - `ans += value * day` 把「商品价值 × 当天编号」加入答案  
> - `values[shop].pop()` 把已经买掉的商品从对应店铺列表中删除  
> - `if values[shop]: …` 如果该店还有商品，继续把新「最小」压入堆

#### 复杂度  

- **时间复杂度**：`O(m·n log m)`  
  - 共 `m·n` 天，每天一次堆弹出 `O(log m)`，以及（若有）一次压入 `O(log m)`。  
  - 与暴力 `O((m·n)!)` 相比，几乎是线性的提升。  
- **空间复杂度**：`O(m + m·n)`（原矩阵本身占 `O(m·n)`，堆最多存 `m` 条目）。  
  - 额外的辅助空间只有堆，大小 ≤ 店铺数 `m ≤ 10`，可以忽略不计。

---

## 心得

- **核心技巧**：**贪心 + 最小堆** —— 把「把小的先买」转化为「每天取全局最小」的调度问题。  
- **适用场景**：  
  1. **加权排序**：需要把较大的基数（这里是商品价值）配给较大的权重（这里是天数），常见于「最大化 Σ a_i·b_i」的题目。  
  2. **多队列合并**：每个队列内部有顺序（这里是非递增），需要一次挑出全局最小/最大，如「合并 k 条有序链表」或「K 组任务的最早完成时间」等。  
- **一句话总结**：**把最小的商品先买，最大化乘以天数的收益**。

---

## 反思

- **第一反应**：看到「价值 × 天数」的乘积，立刻想到「把大的价值放到大的天数」——这暗示了排序或贪心。  
- **最容易踩的坑**：  
  - **误把每家店的最大商品先买**（与题意相反），导致总花费最小而不是最大。  
  - **忘记把已买商品从对应店的列表中删除**，导致同一件商品被多次计入。  
  - **天数从 0 开始计数**（乘以 0 会把商品价值全部抹掉），应从 1 开始。  
- **下次类似题**：  
  1. 首先确认 **权重（天数、位置）是递增还是递减**。  
  2. 判断是 **「把大配大」还是「把小配小」**，进而决定是取最大堆还是最小堆。  
  3. 用 **堆** 快速维护多组有序序列的「当前最小/最大」元素，做到 O(log k) 的更新。