# #2611. 老鼠与奶酪 / Mice and Cheese

> 难度：中等 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/mice-and-cheese/)

---

## 题目（英文原版）

**Description**

There are two mice and n different types of cheese, each type of cheese should be eaten by exactly one mouse.
A point of the cheese with index i (0-indexed) is:
You are given a positive integer array reward1, a positive integer array reward2, and a non-negative integer k.
Return the maximum points the mice can achieve if the first mouse eats exactly k types of cheese.

**Examples**

**Example 1:**

```
Input: reward1 = [1,1,3,4], reward2 = [4,4,1,1], k = 2
Output: 15
Explanation: In this example, the first mouse eats the 2nd (0-indexed) and the 3rd types of cheese, and the second mouse eats the 0th and the 1st types of cheese.
The total points are 4 + 4 + 3 + 4 = 15.
It can be proven that 15 is the maximum total points that the mice can achieve.
```

**Example 2:**

```
Input: reward1 = [1,1], reward2 = [1,1], k = 2
Output: 2
Explanation: In this example, the first mouse eats the 0th (0-indexed) and 1st types of cheese, and the second mouse does not eat any cheese.
The total points are 1 + 1 = 2.
It can be proven that 2 is the maximum total points that the mice can achieve.
```

**Constraints**

- 1 <= n == reward1.length == reward2.length <= 105
- 1 <= reward1[i], reward2[i] <= 1000
- 0 <= k <= n

---

## 题目（中文翻译）

有两只老鼠和 `n` 种不同的奶酪，每种奶酪必须恰好被其中一只老鼠吃掉。  
第 `i` 种奶酪（**0‑indexed**）的得分（**point**）为：

- 若第一只老鼠吃第 `i` 种奶酪，则得到 `reward1[i]` 分；
- 若第二只老鼠吃第 `i` 种奶酪，则得到 `reward2[i]` 分。

给定正整数数组 `reward1`、正整数数组 `reward2`，以及非负整数 `k`。  
返回在第一只老鼠恰好吃掉 `k` 种奶酪的前提下，两只老鼠能够获得的最大总得分（**maximum points**）。

**示例 1**  
**输入**: `reward1 = [1,1,3,4]`, `reward2 = [4,4,1,1]`, `k = 2`  
**输出**: `15`  
**解释**: 在此示例中，第一只老鼠吃第 `2`（**0‑indexed**）和第 `3` 种奶酪，第二只老鼠吃第 `0` 和第 `1` 种奶酪。  
总得分为 `4 + 4 + 3 + 4 = 15`。可以证明 `15` 是能够取得的最大总得分。

**示例 2**  
**输入**: `reward1 = [1,1]`, `reward2 = [1,1]`, `k = 2`  
**输出**: `2`  
**解释**: 在此示例中，第一只老鼠吃第 `0`（**0‑indexed**）和第 `1` 种奶酪，第二只老鼠不吃任何奶酪。  
总得分为 `1 + 1 = 2`。可以证明 `2` 是能够取得的最大总得分。

**约束条件**

- `1 <= n == reward1.length == reward2.length <= 10^5`
- `1 <= reward1[i], reward2[i] <= 1000`
- `0 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的分配方式**，然后挑出满足「第一只老鼠恰好吃 k 种奶酪」且总得分最高的那一种。  

- **数据结构**：可以用一个长度为 `n` 的二进制数组 `choose`（或 `0/1` 列表）来表示每种奶酪谁吃：`choose[i]=1` 表示第一只老鼠吃第 `i` 种，`0` 表示第二只老鼠吃。  
- **生活化类比**：把 `choose` 想成「是/否」的选项卡，像我们在超市挑选商品时，决定「买」还是「不买」。  
- **正确性**：只要遍历了 **所有** 长度为 `n`、恰好有 `k` 个 `1` 的二进制序列，就一定能找到最优解，因为每一种合法分配都被检查到了。  

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def miceAndCheese_bruteforce(reward1: List[int], reward2: List[int], k: int) -> int:
    n = len(reward1)
    best = 0

    # 生成所有恰好选 k 个下标的组合，组合里的下标表示第一只老鼠吃的奶酪
    for first_idxs in combinations(range(n), k):
        total = 0
        # 把第一只老鼠吃的奶酪加上 reward1
        for i in first_idxs:
            total += reward1[i]
        # 剩下的奶酪交给第二只老鼠，加上 reward2
        for i in range(n):
            if i not in first_idxs:          # 这里可以用集合加速，省略细节
                total += reward2[i]
        best = max(best, total)

    return best
```

> 关键点  
> - `combinations(range(n), k)` 会把所有「选 `k` 个下标」的情况列举出来。  
> - 对每种组合，我们分别累加对应的 `reward1` 与 `reward2`。  

#### 复杂度  

- **时间复杂度**：`O( C(n, k) * n )`  
  - `C(n, k)` 是「从 `n` 个中选 `k` 个」的组合数，等价于 `n! / (k! (n-k)!)`。  
  - 对每个组合我们要遍历一次 `n` 长度的数组求和。  
  - 用大白话说，就是「组合数乘以一次遍历」，当 `n` 为 10⁵ 时根本不可能跑完。  
- **空间复杂度**：`O(k)`（存放当前组合的下标），这在理论上是可以接受的，但时间已经毁了这道题。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**遍历所有组合是瓶颈**。我们需要找到一种只遍历一次就能得到最优答案的办法。  

1. **先假设第二只老鼠吃掉所有奶酪**  
   - 那么初始得分为 `sum(reward2)`。  
2. **如果把第 `i` 种奶酪交给第一只老鼠**，分数会从 `reward2[i]` 变成 `reward1[i]`，**增量** 为  

\[
\text{gain}_i = reward1[i] - reward2[i]
\]

   - 当 `gain_i` 为正数时，把这块奶酪交给第一只老鼠会让总分提高；当为负数时则会降低。  
3. **我们必须恰好让第一只老鼠吃 `k` 种**，所以**挑选增量最大的 `k` 块**即可。  
   - 这一步其实是「从所有增量中挑出最大的 `k` 个」，**贪心**的经典场景。  
4. **实现方式**  
   - 计算每种奶酪的 `gain`（相当于「差值」），放进列表。  
   - 对 `gain` 降序排序，取前 `k` 项的和 `gain_sum`。  
   - 最终答案 = `sum(reward2) + gain_sum`。  

> **为什么贪心对这道题一定正确？**  
> - 每块奶酪的增量互不影响（吃不吃这块只会影响自己的那块分数），所以把「最有价值」的 `k` 块拿走必然得到最大总分。  
> - 这相当于「背包容量固定为 `k`，每件物品价值为 `gain_i`，且每件只能选或不选」的特殊情况：价值不受重量限制，直接选价值最高的 `k` 件。  

#### 代码（Python）

```python
from typing import List

def miceAndCheese(reward1: List[int], reward2: List[int], k: int) -> int:
    n = len(reward1)

    # 1. 先算出第二只老鼠吃全部奶酪的基础得分
    base = sum(reward2)                     # 相当于“所有奶酪都交给第二只老鼠”

    # 2. 计算每块奶酪交给第一只老鼠后能带来的增量
    #    gain[i] = reward1[i] - reward2[i]
    gains = [r1 - r2 for r1, r2 in zip(reward1, reward2)]

    # 3. 按增量从大到小排序，挑出最大的 k 项
    #    使用 sort 的逆序参数，时间 O(n log n)
    gains.sort(reverse=True)

    # 4. 把最大的 k 个增量加到 base 上
    #    如果 k 为 0，循环体不会执行，直接返回 base
    extra = sum(gains[:k])

    return base + extra
```

> 关键行解释  
> - `base = sum(reward2)`：把「第二只老鼠吃全部」的得分算出来。  
> - `gains = [r1 - r2 for r1, r2 in zip(reward1, reward2)]`：一次遍历得到每块奶酪的「价值差”。  
> - `gains.sort(reverse=True)`：把差值从大到小排，好像把「最贵的」奶酪排在前面。  
> - `extra = sum(gains[:k])`：把前 `k` 块最贵的奶酪的增量加起来。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 计算 `gain` 与求 `sum(reward2)` 各是 `O(n)`。  
  - 排序是 `O(n log n)`，这是主导因素。  
  - 用大白话说，就是「先把所有奶酪排个队（从最有价值到最没价值），再挑前面 `k` 个」。  
- **空间复杂度**：`O(n)`  
  - 需要一个 `gains` 列表保存每块奶酪的增量，大小跟 `n` 成正比。  
  - 这在题目限制 `n ≤ 10⁵` 的情况下完全可以接受。  

---

## 心得  

- **核心技巧**：把「两只老鼠的得分差」转化为单维度的增量（`gain`），然后用**贪心挑最大 k 项**。  
- **适用的题型**：  
  1. “两个人分配任务、要求其中一人恰好完成 k 项”——如 LeetCode 2611 *Mice and Cheese*（本题）。  
  2. “从两个数组中挑选 k 项，使总和最大”——如 “Two City Scheduling”。  
  3. “固定数量的选择，收益为两种方案的差值”——如 “Maximum Sum of Two Non-Overlapping Subarrays” 的变形。  
- **一句话总结**：**把所有收益差值排序，挑最大 k 个即可**。  

---

## 反思  

- **第一反应**：看到「两只老鼠」「恰好 k 种」就想「枚举所有组合」或「动态规划」——但这会超时。  
- **最容易踩的坑**：  
  - 忽略 `k = 0` 或 `k = n` 的边界情况，导致切片 `gains[:k]` 产生错误。  
  - 没有先把 `reward2` 的总和算进去，只算了 `gain`，会少算第二只老鼠的基础分。  
- **下次遇到同类题**，第一步应该**思考是否可以把问题转化为“选取增量最大的若干项”**，即检查是否存在「两种方案的差值」这种结构，若有则直接用贪心排序解决。