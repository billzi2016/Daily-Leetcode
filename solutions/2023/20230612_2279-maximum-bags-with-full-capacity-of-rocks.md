# #2279. 最大可装满的袋子数 / Maximum Bags With Full Capacity of Rocks

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-bags-with-full-capacity-of-rocks/)

---

## 题目（英文原版）

**Description**

You have n bags numbered from 0 to n - 1. You are given two 0-indexed integer arrays capacity and rocks. The ith bag can hold a maximum of capacity[i] rocks and currently contains rocks[i] rocks. You are also given an integer additionalRocks, the number of additional rocks you can place in any of the bags.
Return the maximum number of bags that could have full capacity after placing the additional rocks in some bags.

**Examples**

**Example 1:**

```
Input: capacity = [2,3,4,5], rocks = [1,2,4,4], additionalRocks = 2
Output: 3
Explanation:
Place 1 rock in bag 0 and 1 rock in bag 1.
The number of rocks in each bag are now [2,3,4,4].
Bags 0, 1, and 2 have full capacity.
There are 3 bags at full capacity, so we return 3.
It can be shown that it is not possible to have more than 3 bags at full capacity.
Note that there may be other ways of placing the rocks that result in an answer of 3.
```

**Example 2:**

```
Input: capacity = [10,2,2], rocks = [2,2,0], additionalRocks = 100
Output: 3
Explanation:
Place 8 rocks in bag 0 and 2 rocks in bag 2.
The number of rocks in each bag are now [10,2,2].
Bags 0, 1, and 2 have full capacity.
There are 3 bags at full capacity, so we return 3.
It can be shown that it is not possible to have more than 3 bags at full capacity.
Note that we did not use all of the additional rocks.
```

**Constraints**

- n == capacity.length == rocks.length
- 1 <= n <= 5 * 104
- 1 <= capacity[i] <= 109
- 0 <= rocks[i] <= capacity[i]
- 1 <= additionalRocks <= 109

---

## 题目（中文翻译）

你有 `n` 个编号为 `0` 到 `n-1` 的袋子（bag）。给定两个 **0 索引** 的整数数组 `capacity` 和 `rocks`。第 `i` 个袋子最多可以装 `capacity[i]` 颗石子（rock），当前已经装有 `rocks[i]` 颗石子。另给你一个整数 `additionalRocks`，表示你可以再向任意袋子中放入的额外石子数量。

返回在向若干袋子中放入这些额外石子后，能够达到 **满容量**（full capacity）的最大袋子数量。

### 示例

**示例 1**

```
Input: capacity = [2,3,4,5], rocks = [1,2,4,4], additionalRocks = 2
Output: 3
Explanation:
向袋子 0 中放入 1 颗石子，向袋子 1 中放入 1 颗石子。
此时每个袋子的石子数为 [2,3,4,4]。
袋子 0、1、2 已经满容量。
满容量的袋子共有 3 个，返回 3。
可以证明无法让满容量的袋子数超过 3。
```

**示例 2**

```
Input: capacity = [10,2,2], rocks = [2,2,0], additionalRocks = 100
Output: 3
Explanation:
向袋子 0 中放入 8 颗石子，向袋子 2 中放入 2 颗石子。
此时每个袋子的石子数为 [10,2,2]。
袋子 0、1、2 已经满容量。
满容量的袋子共有 3 个，返回 3。
可以证明无法让满容量的袋子数超过 3。
注意我们并没有使用完所有的额外石子。
```

### 约束条件

- `n == capacity.length == rocks.length`
- `1 <= n <= 5 * 10^4`
- `1 <= capacity[i] <= 10^9`
- `0 <= rocks[i] <= capacity[i]`
- `1 <= additionalRocks <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的放石头方式**，看哪一种能让最多的袋子恰好装满。  
- 先算出每个袋子还差多少石头才能装满，记作 `need[i] = capacity[i] - rocks[i]`。  
- 接下来我们可以把 `additionalRocks` 按任意方式分配到这些 `need` 上，只要某个袋子的需求被全部满足，它就算“满”。  
- 为了得到最大数量，需要尝试所有**子集**（即哪些袋子我们决定填满，哪些不填），并检查剩余的石头是否足够。  

这相当于在 **“背包问题”** 中把每个袋子当作一个物品，重量是 `need[i]`，价值是 1（填满一个袋子计 1 分），容量是 `additionalRocks`。求最大价值的组合。  

> **类比**：把 `need` 想成“每本书缺的页数”，我们有一定的“纸张”（额外石头），想把尽可能多的书补全。最笨的办法就是把每本书的“缺页数”全部列出来，尝试看能补全哪些组合。

这种枚举显然是 **指数级** 的：如果有 `n` 个袋子，就有 `2^n` 种子集。`n` 最多可达 `5·10⁴`，根本不可行，只能当作思考的起点，帮助我们确认**“只要能填满的袋子越多越好”**这一点是对的。

#### 代码（Python）

```python
from itertools import combinations

def maxBags_bruteforce(capacity, rocks, additionalRocks):
    n = len(capacity)
    need = [c - r for c, r in zip(capacity, rocks)]   # 每个袋子还差多少石头

    best = 0
    # 枚举要填满的袋子数量 k，从 0 到 n
    for k in range(n + 1):
        # 枚举所有恰好 k 个袋子的组合
        for idxs in combinations(range(n), k):
            total = sum(need[i] for i in idxs)        # 这 k 个袋子需要的石头总数
            if total <= additionalRocks:              # 还能满足吗？
                best = max(best, k)                  # 更新答案
    return best
```

> **注意**：上述代码仅用于说明思路，实际运行会在 `n` 超过 20 左右就超时。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`，因为要遍历所有子集（`2^n`）并在每次检查时求和（最坏 `O(n)`）。  
  - 大白话：如果袋子有 30 个，就相当于要检查 **十亿** 次，根本不可能在几秒内算完。  
- **空间复杂度**：`O(n)`，主要是存 `need` 数组和递归栈（组合生成器内部使用的临时空间）。

---

### 2. 最优解

#### 思路  

从暴力解我们知道：

1. 每个袋子要想“满”，必须投入 **恰好 `need[i]` 块石头**，多余的石头对该袋子没有帮助（只能浪费）。  
2. 为了让 **“填满的袋子数量”** 最大，我们应该**先填那些需求最小的袋子**，因为它们花费的石头最少，能让我们在同样的 `additionalRocks` 下“买到”更多的满袋子。  

这正是**贪心（Greedy）**的思路：  
- 计算所有 `need[i]`（只要 `need[i] = 0` 的袋子已经满，不需要再考虑）。  
- 把这些需求从小到大排序。  
- 按顺序遍历，**只要还有足够的 `additionalRocks`**，就把它填满并扣除对应的石头；否则停止。  

> **类比**：想象你去超市买水果，每个水果的价格是 `need[i]`，你只有 `additionalRocks` 元钱。想买到的水果种类最多，就应该先买最便宜的水果，这样钱花得最划算，买的种类也最多。

**为什么贪心是最优的？**  
- 假设我们有两个袋子 A、B，`need[A] ≤ need[B]`。如果我们先填满 B 而不是 A，花的石头不少于填满 A 所需的。如果此时石头不够再填 A，换个顺序先填 A 再填 B（如果还能填的话）**不会减少**已满的袋子数量，反而可能让我们多填一个。所以把需求最小的先填是安全的，最终得到的满袋子数是最大的。

#### 代码（Python）

```python
def maxBags(capacity, rocks, additionalRocks):
    """
    返回在放置 additionalRocks 后，最多可以有多少袋子恰好装满。
    """
    # 1. 计算每个袋子还差多少石头才能装满
    need = [c - r for c, r in zip(capacity, rocks)]

    # 2. 已经满的袋子不需要再考虑，直接计数
    full = sum(1 for x in need if x == 0)

    # 3. 把需要额外石头的袋子需求从小到大排序
    #    只保留 >0 的需求，0 的已经算进 full 了
    need = [x for x in need if x > 0]
    need.sort()                     # O(n log n)

    # 4. 贪心填充
    for cur in need:
        if additionalRocks >= cur:  # 还能填满当前袋子吗？
            additionalRocks -= cur  # 用掉相应的石头
            full += 1               # 该袋子现在满了
        else:                        # 石头不够了，后面的需求只会更大，直接结束
            break

    return full
```

> 关键行的中文注释已经写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n log n)`，主要来源于对 `need` 数组的排序。  
  - 大白话：如果有 50,000 个袋子，排序大约需要几万次比较，几乎在瞬间完成。  
- **空间复杂度**：`O(n)`，存放 `need` 列表（最坏情况所有袋子都需要石头）。  
  - 与暴力解相比，只是多了一点临时存储，完全可以接受。

---

## 心得

- **核心技巧**：**贪心 + 排序**——先把每个袋子需要的石头算出来，最小的先填。
- **适用的题型**  
  1. “尽可能多完成任务”类（如 `Maximum Number of Achievable Transfer Requests` 的贪心变形）。  
  2. “最少资源完成最多目标”类（如 `Maximum Units on a Truck`、`Boats to Save People`）。  
  3. “预算分配”类（如 `Maximum Profit With Minimum Cost`）。
- **一句话总结**：**把最“便宜”的需求先满足，才能把有限资源花得最划算。**

---

## 反思

- **第一反应**：看到“把石头放进袋子”，自然想到先算每个袋子还差多少，然后尝试把石头分配过去。  
- **最容易踩的坑**  
  - 忽略已经满的袋子（`need[i] == 0`），导致计数重复。  
  - 排序后忘记在遍历时提前退出（石头不够时仍继续循环），会产生错误的计数。  
  - `additionalRocks`、`capacity[i]` 可能很大（到 `10⁹`），一定要用 `int`（Python 自动大整数）避免溢出。  
- **下次遇到同类题**：**先把每个目标的“花费”算出来，排序后从小到大逐个消耗资源**——这就是贪心的标准套路。