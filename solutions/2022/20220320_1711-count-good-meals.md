# #1711. 好餐计数 / Count Good Meals

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/count-good-meals/)

---

## 题目（英文原版）

**Description**

A good meal is a meal that contains exactly two different food items with a sum of deliciousness equal to a power of two.
You can pick any two different foods to make a good meal.
Given an array of integers deliciousness where deliciousness[i] is the deliciousness of the i​​​​​​th​​​​​​​​ item of food, return the number of different good meals you can make from this list modulo 109 + 7.
Note that items with different indices are considered different even if they have the same deliciousness value.

**Examples**

**Example 1:**

```
Input: deliciousness = [1,3,5,7,9]
Output: 4
Explanation: The good meals are (1,3), (1,7), (3,5) and, (7,9).
Their respective sums are 4, 8, 8, and 16, all of which are powers of 2.
```

**Example 2:**

```
Input: deliciousness = [1,1,1,3,3,3,7]
Output: 15
Explanation: The good meals are (1,1) with 3 ways, (1,3) with 9 ways, and (1,7) with 3 ways.
```

**Constraints**

- 1 <= deliciousness.length <= 105
- 0 <= deliciousness[i] <= 220

---

## 题目（中文翻译）

一个好餐点是指恰好包含两种不同食物，且它们的美味度（deliciousness）之和等于二的幂（power of two）的餐点。你可以任意挑选两种不同的食物来组成好餐点。

给定整数数组 `deliciousness`，其中 `deliciousness[i]` 表示第 *i* 件食物的美味度，返回可以从该列表中组成的不同好餐点的数量，对 `10^9 + 7` 取模。注意，即使美味度相同，只要索引不同，也视为不同的食物。

**示例 1**  
```text
Input: deliciousness = [1,3,5,7,9]
Output: 4
Explanation: 好餐点是 (1,3)、(1,7)、(3,5) 和 (7,9)。
它们的和分别是 4、8、8、16，都是二的幂。
```

**示例 2**  
```text
Input: deliciousness = [1,1,1,3,3,3,7]
Output: 15
Explanation: 好餐点是 (1,1) 有 3 种组合，(1,3) 有 9 种组合，(1,7) 有 3 种组合。
```

**约束条件**  
- `1 <= deliciousness.length <= 10^5`  
- `0 <= deliciousness[i] <= 2^20`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有可能的两道菜**，检查它们的美味度之和是否是 2 的幂。  

- **数据结构**：我们只需要遍历数组本身，用两个下标 `i`、`j`（`i < j`）表示挑选的两道菜。可以把这一步想象成**把所有菜排成一排，依次挑两个**，就像在超市里挑两件商品。  
- **正确性**：因为题目要求“任意两道不同的食物”，只要把所有 `(i, j)` 组合都检查一次，就一定不会漏掉任何合法的配对。  
- **时间/空间复杂度**：  
  - 外层循环遍历 `n` 次，内层最多遍历 `n-1、n-2 …` 次，总次数约为 `n*(n-1)/2`，这在大 O 记号下写作 **O(n²)**。用大白话说，就是如果有 10,000 道菜，需要检查大约 5,0000,000（5 亿）对，显然太慢。  
  - 只用了几个整数计数器，空间复杂度是 **O(1)**（常数级），因为不需要额外的容器。  

#### 代码（Python）  

```python
from typing import List

MOD = 10 ** 9 + 7          # 题目要求的取模数

def countGoodMeals_bruteforce(deliciousness: List[int]) -> int:
    n = len(deliciousness)
    ans = 0

    # 预先准备所有可能的 2 的幂（最多到 2^21，因为 2^21 > 2*10^6）
    powers = [1 << k for k in range(22)]   # 1,2,4,8,...,2^21

    # 枚举所有 unordered pairs (i, j)
    for i in range(n):
        for j in range(i + 1, n):
            s = deliciousness[i] + deliciousness[j]   # 两道菜的总美味度
            # 判断 s 是否是 2 的幂：只要在 powers 列表里出现就是
            if s in powers:
                ans += 1
                ans %= MOD        # 防止整数溢出，随时取模

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 随着菜的数量平方增长，实际意义是“每多 10 道菜，检查的组合数会多出约 100 倍”。  
- **空间复杂度**：`O(1)` —— 只用了常数个变量（`powers` 长度固定为 22），不随 `n` 增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **瓶颈在于枚举所有配对**。  
要提升速度，需要在 **“给定一个菜的美味度 x，快速找出已有的菜 y 使得 x + y 是 2 的幂”** 上做文章。  

1. **把“是否是 2 的幂”转化为“目标值”**  
   对于当前的 `x`，所有可能的目标和是 `2^0, 2^1, …, 2^21`（因为 `deliciousness[i] ≤ 2^20`，两道菜最大和 ≤ `2^21`）。  
   那么对应的 `y` 必须等于 `target - x`。  

2. **使用哈希表记录已经遍历过的菜的出现次数**  
   哈希表（Python 中的 `dict`）可以视作 **查字典**：键是美味度，值是已经看到的该美味度的菜的数量。  
   当我们遍历到第 `i` 道菜 `x` 时：  
   - 先检查所有 21 个 `target`，计算 `need = target - x`。  
   - 如果 `need` 已经在哈希表中出现过，则说明之前的每一道 `need` 菜都可以和当前的 `x` 组成一顿好饭，贡献 `cnt[need]` 种配对。  
   - 累加这些配对数到答案中。  
   - 最后把当前的 `x` 加入哈希表，供后面的菜使用。  

3. **为什么一次遍历就够了**  
   由于我们只在遍历 **从左到右** 的过程中统计“左边已经出现的菜”，每对 `(i, j)` 只会在 `j`（后面的那道）被处理时计数一次，避免了重复。  

4. **复杂度分析**  
   - 对每个元素，我们检查常数个（最多 22）目标和，哈希表的查询/写入都是 **O(1)** 均摊时间。  
   - 因此整体时间是 **O(n * 22) ≈ O(n)**，线性增长，能够轻松处理 `10⁵` 的数据规模。  
   - 哈希表最多保存所有不同的美味度，最坏情况下有 `n` 条记录，空间 **O(n)**。  

#### 代码（Python）  

```python
from typing import List
from collections import defaultdict

MOD = 10 ** 9 + 7

def countGoodMeals(deliciousness: List[int]) -> int:
    # 预生成所有可能的 2 的幂（2^0 ~ 2^21）
    powers = [1 << k for k in range(22)]

    freq = defaultdict(int)   # 哈希表：美味度 -> 已出现的次数
    ans = 0

    for x in deliciousness:            # 逐个遍历每道菜
        # 检查所有可能的目标和
        for p in powers:
            need = p - x               # 需要的另一道菜的美味度
            if need in freq:          # 如果之前出现过这种美味度
                ans += freq[need]      # 计入对应的配对数
                ans %= MOD             # 取模防止溢出

        # 当前菜加入哈希表，供后续菜使用
        freq[x] += 1

    return ans
```

> **关键注释**  
> - `defaultdict(int)` 自动把不存在的键当作 0 处理，省去 `if key in dict` 的写法。  
> - `1 << k` 等价于 `2 ** k`，但位运算更快且更直观地表示“左移”。  
> - `ans %= MOD` 放在内部循环里是安全的，因为答案可能在累计过程中非常大。  

#### 复杂度  

- **时间复杂度**：`O(n * 22) = O(n)` —— 只随菜的数量线性增长。相比暴力的 `O(n²)`，速度提升了 **n 倍**（比如 n=10⁵ 时，暴力需要 10¹⁰ 次操作，最优只需要约 2·10⁶ 次）。  
- **空间复杂度**：`O(n)` —— 需要存储每种美味度出现的次数，最坏情况下每道菜的美味度都不相同。  

---  

## 心得  

- **核心技巧**：利用 **哈希表** 把“是否存在配对”转化为 **计数查询**，并结合 **有限的目标集合（2 的幂）** 实现线性时间解。  
- **适用题型**：  
  1. “找出满足某种求和条件的数对”，如 *两数之和*、*数对之和为平方数* 等。  
  2. “统计满足特定差值/和的配对数”，如 *数组中有多少对差值为 k*。  
- **一句话总结**：**把“找配对”变成“查询已有元素”，哈希表让它瞬间完成**。  

---  

## 反思  

- **第一反应**：直接写双层循环枚举所有配对，感觉最安全。  
- **最容易踩的坑**：  
  - 忘记 **取模**（`10⁹+7`）会导致整数溢出。  
  - 没考虑 **目标和的上限**，导致生成了不必要的 2 的幂（实际只需要到 `2^21`）。  
  - 在统计配对时重复计数（如同时在左侧和右侧统计），会把答案翻倍。  
- **下次类似题的第一步**：先**列出所有可能的目标值**（这里是 2 的幂），然后**思考如何在一次遍历中快速判断是否已经出现过满足条件的元素**——这几乎总是哈希表的用武之地。