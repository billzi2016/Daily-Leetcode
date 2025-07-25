# #3281. 最大化区间内数字的得分 / Maximize Score of Numbers in Ranges

> 难度：中等 · 标签：Array、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-score-of-numbers-in-ranges/)

---

## 题目（英文原版）

**Description**

You are given an array of integers start and an integer d, representing n intervals [start[i], start[i] + d].
You are asked to choose n integers where the ith integer must belong to the ith interval. The score of the chosen integers is defined as the minimum absolute difference between any two integers that have been chosen.
Return the maximum possible score of the chosen integers.

**Examples**

**Example 1:**

```
Input: start = [6,0,3], d = 2
Output: 4
Explanation:
The maximum possible score can be obtained by choosing integers: 8, 0, and 4. The score of these chosen integers is min(|8 - 0|, |8 - 4|, |0 - 4|) which equals 4.
```

**Example 2:**

```
Input: start = [2,6,13,13], d = 5
Output: 5
Explanation:
The maximum possible score can be obtained by choosing integers: 2, 7, 13, and 18. The score of these chosen integers is min(|2 - 7|, |2 - 13|, |2 - 18|, |7 - 13|, |7 - 18|, |13 - 18|) which equals 5.
```

**Constraints**

- 2 <= start.length <= 105
- 0 <= start[i] <= 109
- 0 <= d <= 109

---

## 题目（中文翻译）

你得到一个整数数组 `start` 和一个整数 `d`，它们表示 `n` 个区间 `[start[i], start[i] + d]`。  
你需要为每个区间选择一个整数，第 `i` 个整数必须位于第 `i` 个区间内。选取的整数的**得分**定义为任意两个已选整数之间的绝对差的最小值。  
返回可以获得的最大可能得分。

**示例 1**  
**输入**: `start = [6,0,3]`, `d = 2`  
**输出**: `4`  
**解释**:  
可以通过选择整数 `8, 0, 4` 来得到最大得分。这些整数的得分为  
`min(|8 - 0|, |8 - 4|, |0 - 4|) = 4`。

**示例 2**  
**输入**: `start = [2,6,13,13]`, `d = 5`  
**输出**: `5`  
**解释**:  
可以通过选择整数 `2, 7, 13, 18` 来得到最大得分。这些整数的得分为  
`min(|2 - 7|, |2 - 13|, |2 - 18|, |7 - 13|, |7 - 18|, |13 - 18|) = 5`。

**约束条件**  
- `2 <= start.length <= 10^5`  
- `0 <= start[i] <= 10^9`  
- `0 <= d <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每个区间都枚举一遍**，把所有可能的取值组合都列出来，随后算出每种组合的「得分」——即所有已选整数两两之间的最小绝对差，最后取最大的得分。  

- **数据结构**：我们可以把每个区间 `[start[i], start[i] + d]` 看成一本小字典，键是「可以选的整数」，值可以随意设（这里不需要），相当于把所有合法的整数「列在纸上」再去组合。  
- **为什么正确**：因为我们把**所有**合法的取法都遍历了一遍，答案一定在这些取法里出现。  
- **时间/空间复杂度**：  
  - 每个区间的合法整数个数是 `d + 1`（因为区间是闭区间），如果 `d` 很大，这个数可能达到 `10^9`，根本不可能枚举。即使 `d` 很小，枚举所有组合的时间也是指数级的：`(d+1)^n`。这在日常生活里相当于「把每个人的所有可能坐标都列出来，然后把所有人排成一列，尝试每一种排法」，根本不可行。  
  - 用大白话讲，**O((d+1)^n)** 就像把一只鸡的每根羽毛都拆下来再重新组合，羽毛越多，组合方式就会呈指数增长，几分钟内根本算不完。  

#### 代码（Python）

```python
from itertools import product
from math import inf

def maxScore_bruteforce(start, d):
    # 1. 把每个区间所有合法整数列成列表
    intervals = [list(range(s, s + d + 1)) for s in start]   # 这里会非常慢

    best = -inf
    # 2. 逐个枚举所有组合（笛卡尔积）
    for comb in product(*intervals):
        # 计算当前组合的得分：所有两两差的最小值
        min_diff = inf
        n = len(comb)
        for i in range(n):
            for j in range(i + 1, n):
                min_diff = min(min_diff, abs(comb[i] - comb[j]))
        best = max(best, min_diff)
    return best
```

> **注意**：上述代码仅用于说明「暴力」思路，实际提交会因为时间超限而直接 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O((d+1)^n * n^2)`  
  - `(d+1)^n` 来自所有取值的组合数，`n^2` 来自每次组合内部计算两两差。  
  - 用生活化的比喻：如果把每个区间看成“一篮子水果”，篮子里有 `d+1` 个水果，`n` 个人每人挑一个水果，所有可能的挑选方式是 `篮子数的乘积`，再把每种挑选方式里的人两两比较一次，工作量就会爆炸。  

- **空间复杂度**：`O(n * d)`（存放每个区间的所有合法整数）  
  - 这已经是「把所有水果先全部摆在桌子上」的代价，显然不可取。  



---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举所有取值是最慢的环节**。我们需要**在不枚举的前提下，快速判断是否可以让最小差距 ≥ 某个值 `x`**，再通过二分搜索找到最大的 `x`。  

**核心观察**  

1. **把区间按左端点 `start[i]` 排序**（如果不排序，后面贪心选数会出现交叉，导致判断错误）。  
2. 假设我们已经决定「最小差距」要 **不小于 `x`**，则  
   - 第一个数可以直接取该区间的最左端 `start[0]`（因为没有左边的数约束）。  
   - 对于后面的每个区间 `i`，我们必须选一个数 `val`，满足两个条件：  
     1. `val` 落在它自己的合法范围 `[start[i], start[i] + d]`。  
     2. 为了保证与前一个已选数的差距 ≥ `x`，必须有 `val ≥ last_chosen + x`。  
   - 因此**我们只需要在区间里取最小的满足条件的数**，即 `val = max(start[i], last_chosen + x)`。如果这个 `val` 超出了上界 `start[i] + d`，说明在保证差距 ≥ `x` 的前提下，这个区间已经无解，整个 `x` 不可行。  

3. 以上检查过程只遍历一次数组，**时间是 O(n)**，空间只用了常数。  

**二分搜索**  

- `x` 的取值范围显然在 `[0, max_possible]` 之间。  
  - `0` 永远可行（把所有数都选成区间左端点），  
  - 最大可能的最小差距不会超过 `max(start) + d - min(start)`（把最左的数选在最左，最右的数选在最右）。  
- 使用**二分**在这个闭区间里搜索**最大的**可行 `x`。每一次二分都会调用上面的**可行性检查**（贪心）来判断。  

**为什么贪心是对的？**  

因为我们总是把每个区间的数选得**尽可能小**（满足约束的最小值），这样后面的区间拥有**最大的可选空间**，从而最有可能成功。如果我们在某一步选了更大的数，只会让后面的区间更难满足 `last_chosen + x` 的要求，反而降低成功概率。  

#### 代码（Python）

```python
from typing import List

def maxScore(start: List[int], d: int) -> int:
    """
    返回能够取得的最大 “最小差距” 分数
    """
    n = len(start)
    # 1. 按左端点排序，保持对应的区间一起移动
    start.sort()                     # 哈希表查字典的思路：这里相当于把所有“水果篮子”排成一行，左边的先处理

    # 2. 二分搜索答案
    lo, hi = 0, max(start) + d - min(start)   # 可能的最小差距范围
    while lo < hi:
        mid = (lo + hi + 1) // 2               # 取上中位数，防止死循环
        if feasible(start, d, mid):
            lo = mid                           # mid 可行，尝试更大
        else:
            hi = mid - 1                       # mid 不可行，缩小范围
    return lo

def feasible(start: List[int], d: int, x: int) -> bool:
    """
    判断是否能在每个区间里选数，使得任意相邻已选数的差距 >= x
    这里不必比较所有两两，只要相邻的满足即可（相邻差 >= x 已经能保证所有差 >= x）。
    """
    last = start[0]                 # 第一个区间直接选最左端
    # 只要在自己的合法范围内就行，已经满足 x=0 的情况
    for i in range(1, len(start)):
        # 必须至少比上一个选的数大 x
        need = last + x
        # 该区间能选的最小合法数
        cur = max(start[i], need)
        # 检查是否越界
        if cur > start[i] + d:
            return False            # 该区间已经没有合法数，x 不可行
        last = cur                  # 更新已选的最后一个数
    return True
```

> **关键注释**  
> - `start.sort()`：把所有区间按左端点从小到大排好，就像把「水果篮子」按大小顺序排队，后面的篮子只能往右挑。  
> - `mid = (lo + hi + 1) // 2`：二分取上中位数，防止在 `lo = hi - 1` 时死循环。  
> - `feasible` 中的 `need = last + x`：相当于「上一个小朋友已经拿了一个糖果，下一位小朋友至少要间隔 x 才能再拿」。  
> - `cur = max(start[i], need)`：在当前区间里挑最左的、还能满足间隔的糖果。  

#### 复杂度  

- **时间复杂度**：`O(n log R)`  
  - `n` 是数组长度（最多 `10^5`），遍历一次做可行性检查。  
  - `log R` 是二分的次数，其中 `R = max(start) + d - min(start)`，其值不超过 `2·10^9`，`log2(2·10^9) ≈ 31`，所以最多 31 次检查。  
  - 用生活化的说法：我们只需要「一次排队检查」每次「把所有小朋友的糖果分配」的过程，然后把「检查的次数」控制在 30 次左右，整个过程就像「把 10 万个人排成一列，走 30 趟」一样快。

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个整数变量 `last、need、cur、lo、hi、mid`，不随 `n` 增长。  

---  

## 心得  

- **核心技巧**：**二分答案 + 贪心可行性检查**。  
- **适用题型**：  
  1. “在区间里选数，使得最小差距最大” 类似题（如 LeetCode 1552 “两个城市的最小距离”）。  
  2. “在若干资源上分配，使得每个人的最小满意度最大” （如分配糖果、分配任务的最大最小值）。  
  3. “在数组中挑选 k 项，使得相邻差距≥x” 这类的“最大化最小值”问题。  
- **一句话总结解题钥匙**：**把“能否做到”转化为单调判定，然后用二分把最大可行值找出来**。  



## 反思  

- **第一反应**：看到“最大化最小差距”，立刻想到“二分答案”。因为这类“最大化最小值”往往满足单调性——如果某个差距 `x` 可行，那么所有更小的差距必然也可行。  
- **最容易踩的坑**：  
  1. **忘记先排序**——如果不把区间左端点排好序，贪心检查会出现“前面选的大，后面选的不够大”导致误判。  
  2. **相邻检查 vs 任意两两**——只检查相邻已选数的差距即可，因为已经保证相邻差 ≥ x，累加后自然保证任意两两差 ≥ x。  
  3. **二分区间取值**——要使用上取整的中点 `(lo+hi+1)//2`，否则在 `lo` 与 `hi` 相差 1 时可能陷入死循环。  
- **下次遇到同类题的第一步**：先判断“可行性”是否具备单调性（`x` 越大越难实现），如果是，就立刻写出 **“检查函数”**（通常是贪心或 DP），再套二分搜索求最大可行 `x`。