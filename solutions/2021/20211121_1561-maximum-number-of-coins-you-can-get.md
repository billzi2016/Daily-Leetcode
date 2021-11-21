# #1561. **你能获得的最大硬币数** / Maximum Number of Coins You Can Get

> 难度：中等 · 标签：Array、Math、Greedy、Sorting、Game Theory · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-coins-you-can-get/)

---

## 题目（英文原版）

**Description**

There are 3n piles of coins of varying size, you and your friends will take piles of coins as follows:
Given an array of integers piles where piles[i] is the number of coins in the ith pile.
Return the maximum number of coins that you can have.

**Examples**

**Example 1:**

```
Input: piles = [2,4,1,2,7,8]
Output: 9
Explanation: Choose the triplet (2, 7, 8), Alice Pick the pile with 8 coins, you the pile with 7 coins and Bob the last one.
Choose the triplet (1, 2, 4), Alice Pick the pile with 4 coins, you the pile with 2 coins and Bob the last one.
The maximum number of coins which you can have are: 7 + 2 = 9.
On the other hand if we choose this arrangement (1, 2, 8), (2, 4, 7) you only get 2 + 4 = 6 coins which is not optimal.
```

**Example 2:**

```
Input: piles = [2,4,5]
Output: 4
```

**Example 3:**

```
Input: piles = [9,8,7,6,5,1,2,3,4]
Output: 18
```

**Constraints**

- 3 <= piles.length <= 105
- piles.length % 3 == 0
- 1 <= piles[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `piles`，其中 `piles[i]` 表示第 `i` 堆硬币的数量。共有 `3n` 堆硬币，你和你的两位朋友（Alice 和 Bob）将按照以下规则依次挑选每组三堆中的一堆：

1. 将剩余的堆分成若干个三元组（triplet），每个三元组包含 3 堆硬币。  
2. 在每个三元组中，Alice 先挑选硬币数量最多的那堆，随后你挑选剩下的两堆中硬币数量较多的那堆，最后 Bob 只能得到剩下的那堆。

返回在所有可能的挑选方式中，你能够获得的硬币总数的最大值。

---

### 示例

**示例 1**  
```text
Input: piles = [2,4,1,2,7,8]
Output: 9
Explanation: 先选择三元组 (2, 7, 8)，Alice 选取 8 枚硬币的堆，你得到 7 枚，Bob 拿到剩下的 2 枚。  
再选择三元组 (1, 2, 4)，Alice 选取 4 枚硬币的堆，你得到 2 枚，Bob 拿到剩下的 1 枚。  
你能够得到的硬币总数最大为 7 + 2 = 9。  
如果改为选择 (1, 2, 8) 等其他组合，则得到的总数会更少。  
```

**示例 2**  
```text
Input: piles = [2,4,5]
Output: 4
```

**示例 3**  
```text
Input: piles = [9,8,7,6,5,1,2,3,4]
Output: 18
```

---

### 约束条件

- `3 <= piles.length <= 10^5`
- `piles.length % 3 == 0`
- `1 <= piles[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `3n` 堆硬币全部分成 `n` 组，每组恰好 3 堆。  
每一组里，**Alice** 必然会拿走最大的那堆，**你** 拿走第二大的那堆，**Bob** 拿走最小的那堆。  

于是，只要枚举所有可能的分组方式，计算每种分组下「你」得到的硬币总数，取最大值即可。

> **数据结构类比**：  
> 把所有堆想成一本厚厚的词典，每页上写着一个数字（硬币数）。  
> 暴力解相当于把这本词典的每一页随意组合成三页一组，尝试所有可能的排版方式。

**为什么正确**：  
因为题目已经规定了每组的取法（最大→Alice，次大→你，最小→Bob），只要遍历所有合法的分组，必然会覆盖最优的那一种。

**复杂度分析（大白话）**：

- **时间**：要把 `3n` 堆全部分成 `n` 组，组合的数量是  
  \[
  \frac{(3n)!}{(3!)^n \, n!}
  \]
  也就是“阶乘级别”，随着 `n` 增大瞬间爆炸（比如 `n=10` 时已经超过 10^20 种）。可以说 **时间复杂度是 O((3n)!)**，几乎不可能在一分钟内跑完。
- **空间**：递归/回溯时需要保存当前已经分好的组，最坏需要 O(3n) 的栈空间。

#### 代码（Python）

```python
from itertools import permutations
from math import factorial

def brute_max_coins(piles):
    """
    暴力解：枚举所有可能的 3 堆一组的分法，计算你能得到的最大硬币数。
    仅用于解释思路，实际在 n>3 时根本跑不完。
    """
    n = len(piles) // 3
    best = 0

    # 把所有堆的排列列举出来（这里用 permutations，仅作示例）
    # 实际上每一种排列对应一种分组方式：第 0、1、2 为第一组，3、4、5 为第二组，...
    for perm in permutations(piles):
        cur = 0
        for i in range(n):
            triplet = sorted(perm[3*i:3*i+3])   # 从小到大排序
            # Alice 取最大，Bob 取最小，你取中间
            cur += triplet[1]                  # 你得到的硬币数
        best = max(best, cur)

    return best

# 示例（仅能跑极小规模）
print(brute_max_coins([2, 4, 1, 2, 7, 8]))   # 9
```

> **注意**：上面的 `permutations` 会在 `len(piles)=6` 时产生 720 种排列，已经很慢；`len=9` 时就有 362880 种，几乎不可接受。

#### 复杂度

- **时间复杂度**：`O((3n)!)` —— 随着 `n` 增大，计算量呈阶乘级增长，实际不可用。
- **空间复杂度**：`O(3n)` —— 递归栈或临时列表的大小。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们把所有堆都随意组合，这导致枚举次数爆炸。  
实际上，题目只要求我们**最大化**自己拿到的硬币数，而 **Alice** 总是抢走每组三堆里最大的，**Bob** 必然会得到最小的那一堆（因为他只能拿剩下的唯一一堆）。  

这启示我们：**把最小的堆留给 Bob，把最大的堆让 Alice，剩下的“第二大”就是我们想要的**。只要把所有堆排好序，就可以直接挑出这些“第二大”。

**关键观察**：

1. 把所有堆从小到大排序：`piles[0] ≤ piles[1] ≤ … ≤ piles[3n‑1]`。  
2. 为了让 Bob 拿到最小的堆，我们把 **最左边的 n 堆**（最小的 n 堆）全部交给 Bob。  
3. 剩下的 `2n` 堆中，最大的 `n` 堆会被 Alice 抢走。  
4. 于是，剩下的 **中间的 n 堆**（既不是最小也不是最大的）正好是我们能得到的每组的第二大堆。  

把这个过程用**双指针**或**一步步跳**的方式写出来：

- 排序后，从右往左遍历，**每隔两个取一次**（因为每组三堆：左边最小 → Bob，右边最大 → Alice，中间的就是我们）。
- 具体而言，设 `m = len(piles)`，我们从 `m‑2` 开始，每次往左走两步，取 `n` 次。

> **类比**：把硬币堆排成一排，左边是最弱的士兵（Bob），右边是最强的骑士（Alice），我们站在两者之间的“中间骑士”，只要把队形排好，就自然知道我们该站在哪。

#### 代码（Python）

```python
def maxCoins(piles):
    """
    贪心+排序：先把所有堆从小到大排好序，
    再从右往左每隔两个取一次，恰好是我们能得到的最大硬币数。
    时间 O(n log n)（排序），空间 O(1)（原地排序）。
    """
    piles.sort()                     # 从小到大排好序
    n = len(piles) // 3               # 组数
    ans = 0
    # 从倒数第二个元素开始，每隔两个取一次，取 n 次
    # 例如 len=6: 索引顺序 4, 2   -> 对应 piles[4] + piles[2]
    for i in range(n):
        idx = len(piles) - 2 - 2*i   # 计算当前要拿的元素下标
        ans += piles[idx]            # 累加到答案
    return ans

# ----------------- 测试 -----------------
print(maxCoins([2,4,1,2,7,8]))                     # 9
print(maxCoins([2,4,5]))                           # 4
print(maxCoins([9,8,7,6,5,1,2,3,4]))               # 18
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `n` 这里指的是 `len(piles)`，排序需要 `O(3n log (3n))`，后面的遍历只要 `O(n)`，整体 dominated by 排序。  
  - **含义**：如果堆的数量是 300,000，排序大约需要几千万次比较，仍然能在一秒左右跑完（Python 的 Timsort 很快）。

- **空间复杂度**：`O(1)`（不计排序时 Python 列表内部的临时空间）  
  - 我们只用了几个整数变量来记录下标和累计答案。

- **对比**：暴力解的 `O((3n)!)` 完全不可接受，最优解把时间从“天文级”压到了“几百万次比较”，瞬间变得可用。

---

## 心得

- **核心技巧**：**先排序，再贪心挑选“第二大”**。本题的本质是把 “谁拿最大、谁拿最小” 固定下来后，剩下的就是我们能得到的最大值。
- **适用场景**：
  1. **分组取最大/最小** 的游戏类题目（如 LeetCode 1561 “Maximum Number of Coins You Can Get” 本题）。
  2. **“你总是拿第二好”** 的策略题（如 “Stone Game VI”）。
  3. **在已排序序列中每隔固定步长取值** 的贪心题（如 “Array Partition I”）。
- **一句话总结**：  
  *把最小的交给 Bob，最大的让 Alice，剩下的就是你最大的收益——排序后每隔两个取一次即可。*

---

## 反思

- **第一反应**：把所有堆随意组合，枚举所有可能的三堆分组。  
- **最容易踩的坑**：
  - **忽视 Bob 必然拿到最小的那堆**：如果不把 Bob 的堆固定为最小，可能会误以为需要复杂的动态规划。  
  - **边界条件**：`len(piles) % 3 == 0` 保证可以完整分组，若忘记这一点会导致下标越界。  
  - **索引计算错误**：从右往左每隔两个取一次时，`len(piles) - 2 - 2*i` 必须写对，否则会漏掉或重复取元素。
- **下次遇到同类题**：第一步先**思考谁必然拿走最大/最小**，把这些固定角色对应的堆“锁定”，剩下的自然就是我们要最大化的部分；随后**排序+贪心**往往是最直接的路径。