# #1798. 最大连续整数数量 / Maximum Number of Consecutive Values You Can Make

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-consecutive-values-you-can-make/)

---

## 题目（英文原版）

**Description**

You are given an integer array coins of length n which represents the n coins that you own. The value of the ith coin is coins[i]. You can make some value x if you can choose some of your n coins such that their values sum up to x.
Return the maximum number of consecutive integer values that you can make with your coins starting from and including 0.
Note that you may have multiple coins of the same value.

**Examples**

**Example 1:**

```
Input: coins = [1,3]
Output: 2
Explanation: You can make the following values:
- 0: take []
- 1: take [1]
You can make 2 consecutive integer values starting from 0.
```

**Example 2:**

```
Input: coins = [1,1,1,4]
Output: 8
Explanation: You can make the following values:
- 0: take []
- 1: take [1]
- 2: take [1,1]
- 3: take [1,1,1]
- 4: take [4]
- 5: take [4,1]
- 6: take [4,1,1]
- 7: take [4,1,1,1]
You can make 8 consecutive integer values starting from 0.
```

**Example 3:**

```
Input: coins = [1,4,10,3,1]
Output: 20
```

**Constraints**

- coins.length == n
- 1 <= n <= 4 * 104
- 1 <= coins[i] <= 4 * 104

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `coins`，其中第 `i` 个元素 `coins[i]` 表示你拥有的第 `i` 枚硬币的面值。若你可以挑选若干枚硬币，使它们的面值之和等于 `x`，则称你能够组成值 `x`。  
返回从 `0` 开始（包括 `0`）你能够连续组成的整数值的最大数量。  

> 注意：数组中可能出现相同面值的硬币多次。

## 示例

### 示例 1
**输入**: `coins = [1,3]`  
**输出**: `2`  
**解释**: 你可以组成以下数值：
- `0`：不取任何硬币 `[]`
- `1`：取硬币 `[1]`  

从 `0` 开始你可以连续组成 `2` 个整数。

### 示例 2
**输入**: `coins = [1,1,1,4]`  
**输出**: `8`  
**解释**: 你可以组成以下数值：
- `0`：`[]`
- `1`：`[1]`
- `2`：`[1,1]`
- `3`：`[1,1,1]`
- `4`：`[4]`
- `5`：`[4,1]`
- `6`：`[4,1,1]`
- `7`：`[4,1,1,1]`  

从 `0` 开始你可以连续组成 `8` 个整数。

### 示例 3
**输入**: `coins = [1,4,10,3,1]`  
**输出**: `20`

## 约束条件
- `coins.length == n`
- `1 <= n <= 4 * 10^4`
- `1 <= coins[i] <= 4 * 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有子集**，把每个子集的硬币价值相加，得到所有可以凑出的数值，然后找出从 0 开始连续的最长区间。  

- **使用的数据结构**：  
  - `set`（集合）可以看成一本“词典”，把每一次算出的和记下来，像查字典一样判断某个值是否已经出现。  
- **正确性解释**：  
  - 每一种取硬币的方式对应唯一的子集，而我们把所有子集的和都收集进集合中，所以集合里恰好包含了**所有**可以凑出的数值。遍历从 0 开始的整数，遇到第一个不在集合里的数，就是连续区间的终点。  
- **复杂度分析（大白话）**：  
  - 枚举子集的数量是 `2^n`（每个硬币“要”或“不要”），这相当于 **指数级**增长。  
  - 把每个子集的和加入集合需要 O(1)（均摊）时间，但总的时间仍然是 `O(2^n)`。  
  - 集合最多会存 `2^n` 条记录，空间同样是 `O(2^n)`。  
  - 用大白话说：如果硬币有 20 枚，`2^20 ≈ 1,000,000`；如果是 30 枚，已经是 **十亿** 级别，根本跑不完。  

#### 代码（Python）  

```python
from itertools import combinations

def max_consecutive_bruteforce(coins):
    """
    暴力枚举所有子集的和，返回从 0 开始连续的最大个数
    """
    n = len(coins)
    reachable = set([0])                     # 0 总是可以凑到
    # 枚举子集大小 1~n
    for r in range(1, n + 1):
        for combo in combinations(coins, r):
            reachable.add(sum(combo))        # 把子集的和放进集合

    # 从 0 开始找连续的最大区间
    ans = 0
    while ans in reachable:                  # 一直往后找，直到缺口
        ans += 1
    return ans                                # ans 正好是连续个数
```

> **提示**：上面的实现只适合演示概念，`itertools.combinations` 本身已经是指数级的，实际 LeetCode 数据会直接 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 每个硬币都有“选”或“不选”两种可能，组合数呈指数增长。  
- **空间复杂度**：`O(2^n)` —— 最坏情况下需要保存所有子集的和。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举所有子集是最慢的环节**。我们需要找到一种只**线性**（或接近线性）遍历硬币的方法。关键观察来自题目提示：

> 如果已经能够凑出 `[0, x]`（即从 0 到 x 的所有整数），并且手里还有一枚面值为 `v` 的硬币，**只要 `v ≤ x + 1`，我们就可以把可凑区间扩展到 `[0, x + v]`**。

**为什么？**  
- 已经可以凑出 `0 … x`。  
- 加上一枚面值 `v`，我们可以把 `v` 加到已有的每一个数上，得到 `v … v + x`。  
- 两个区间 `[0, x]` 与 `[v, v + x]` 相邻或重叠（因为 `v ≤ x + 1`），于是它们合在一起正好是连续的 `[0, x + v]`。  

所以，只要我们**从小到大**处理硬币，并且每一次都满足 `coin ≤ current_reachable + 1`，就可以不断延伸可凑的上界。  
一旦出现 `coin > current_reachable + 1`，说明出现了“缺口”，无法再继续向右扩展，答案就在这里确定。

**实现步骤**  

1. **排序**：把硬币从小到大排好序。排序相当于把硬币按“从最容易填补缺口”到“最难填补缺口”的顺序摆好。  
2. **维护变量 `reach`**：当前已经可以凑出的最大连续值（即 `[0, reach]` 区间的右端点）。初始 `reach = 0`（只会凑出 0）。  
3. **遍历硬币**：  
   - 若 `coin ≤ reach + 1` → 可以把区间扩大到 `reach += coin`。  
   - 否则 → 直接退出循环，因为后面的硬币更大，只会让缺口更大。  
4. **答案**：区间 `[0, reach]` 包含 `reach + 1` 个整数（因为包括 0），直接返回 `reach + 1`。  

**类比**：把 `reach` 想成一根绳子可以覆盖的长度，硬币的面值是可以往右继续拉伸的“木棍”。只要木棍的长度不超过“绳子末端 + 1”，我们就能把绳子顺利拉长；一旦木棍太长，绳子就拉不动了。

#### 代码（Python）  

```python
def max_consecutive(coins):
    """
    贪心 + 排序：返回从 0 开始连续可凑的整数个数
    """
    coins.sort()                 # 从小到大排列，像排队买东西，先处理最便宜的
    reach = 0                    # 当前能够连续凑出的最大值，初始只能凑到 0
    for c in coins:
        if c > reach + 1:        # 这枚硬币太大，产生缺口，后面的更不行，直接结束
            break
        reach += c               # 能够把区间扩展到更大的值
    return reach + 1             # 包含 0 在内的连续整数个数
```

#### 复杂度  

- **时间复杂度**：`O(n log n)` —— 主要花在对 `coins` 的排序上，遍历本身是线性 `O(n)`。  
  - 与暴力解的 `O(2^n)` 相比，**从指数级降到对数级+线性**，即使 `n = 4·10⁴` 也能在毫秒级完成。  
- **空间复杂度**：`O(1)` —— 只用了常数级的额外变量 `reach`，不随 `n` 增长。  

---

## 心得  

- **核心技巧**：**贪心 + 前缀可达区间**。只要当前可达区间的右端点 `reach` 已经覆盖到 `coin-1`，这枚硬币就一定可以把区间继续往右拉。  
- **适用的题型**  
  1. “最小不可达金额”类问题（LeetCode 1665/1671 等）。  
  2. “用最少硬币拼成连续区间”或“从若干数字构造最长连续子序列”。  
- **一句话总结**：**把硬币从小到大排，遇到比“已能凑的最大值+1”更大的硬币就停，下一个答案就是当前最大可达值+1。**  

---

## 反思  

- **第一反应**：看到“连续整数”“从 0 开始”，自然会想到**前缀和**或**动态规划**，于是先想到了暴力枚举所有子集。  
- **最容易踩的坑**：  
  - 忘记 **包括 0** 本身，导致返回值少 1。  
  - 把答案写成 `reach` 而不是 `reach + 1`（因为区间是闭区间）。  
  - 对硬币不排序直接使用贪心，会出现错误例子，如 `[2,1]`。  
- **下次第一步**：看到“从 0 开始的连续区间”，立刻检查**是否可以用已知的连续区间 + 当前元素**的方式扩展；如果可以，说明可以采用**贪心 + 排序**的思路。