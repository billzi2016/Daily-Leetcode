# #1819. 不同子序列的 GCD 数量 / Number of Different Subsequences GCDs

> 难度：困难 · 标签：Array、Math、Counting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/number-of-different-subsequences-gcds/)

---

## 题目（英文原版）

**Description**

You are given an array nums that consists of positive integers.
The GCD of a sequence of numbers is defined as the greatest integer that divides all the numbers in the sequence evenly.
A subsequence of an array is a sequence that can be formed by removing some elements (possibly none) of the array.
Return the number of different GCDs among all non-empty subsequences of nums.

**Examples**

**Example 1:**

```
Input: nums = [6,10,3]
Output: 5
Explanation: The figure shows all the non-empty subsequences and their GCDs.
The different GCDs are 6, 10, 3, 2, and 1.
```

**Example 2:**

```
Input: nums = [5,15,40,5,6]
Output: 7
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 2 * 105

---

## 题目（中文翻译）

给定一个只包含正整数的数组 `nums`。  
序列（sequence）中所有数字的最大公约数（GCD）定义为能够整除序列中所有数字的最大整数。  
数组的子序列（subsequence）是通过删除数组中的任意若干（可能为零）元素后得到的一个序列。  

返回 `nums` 所有非空子序列中 **不同的 GCD** 的数量。

**示例 1**  
**输入**: `nums = [6,10,3]`  
**输出**: `5`  
**解释**: 下图展示了所有非空子序列及其对应的 GCD。不同的 GCD 为 6、10、3、2、1。

**示例 2**  
**输入**: `nums = [5,15,40,5,6]`  
**输出**: `7`

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 2 * 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组的所有 **非空子序列** 都枚举出来，逐个算出它们的最大公约数（GCD），最后把出现过的 GCD 放进集合去重。

- **子序列**：把原数组看成一串珠子，挑走若干颗（可以不挑，也可以挑走全部），剩下的顺序不变，这就是一个子序列。  
- **GCD**：把几个数想象成“共同的伙伴”，GCD 就是它们都能整除的最大整数。  
- **集合（set）**：就像一本字典，里面的每个词（这里是 GCD）只会出现一次。

只要把所有子序列遍历完，收集到的集合大小就是答案。

> **为什么一定正确？**  
> 因为我们没有遗漏任何可能的子序列，也没有多算重复的 GCD（集合自动去重），所以最终得到的就是 **所有** 不同的 GCD。

#### 代码（Python）

```python
import math
from itertools import combinations

def brute(nums):
    n = len(nums)
    gcd_set = set()                     # 用集合记录出现过的 GCD
    # 枚举子序列的长度 1~n
    for k in range(1, n + 1):
        # 组合生成所有长度为 k 的子序列（顺序不变的组合）
        for idxs in combinations(range(n), k):
            g = nums[idxs[0]]           # 先把第一个数当作初始 GCD
            for i in idxs[1:]:
                g = math.gcd(g, nums[i])
                if g == 1:              # 已经是最小可能值，后面再算也不会更小
                    break
            gcd_set.add(g)              # 把该子序列的 GCD 放进集合
    return len(gcd_set)

# 示例
print(brute([6, 10, 3]))   # 5
```

> **关键行中文注释**  
> - `combinations` 用来产生所有不改变相对顺序的子序列（实际上是组合）。  
> - `math.gcd` 负责计算两个数的最大公约数。  
> - 当 GCD 变成 `1` 时，后面再取 GCD 也不可能更小，提前 `break` 能稍微加速。

#### 复杂度  

- **时间复杂度**：`O(2^n · log A)`  
  - 解释：数组长度为 `n`，子序列的总数是 `2^n - 1`（每个元素保留或删除），每个子序列里要算几次 GCD，GCD 的计算本身是 `log A`（`A` 为数的大小）级别的。  
  - 对于 `n = 20` 已经是几百万次，`n = 30` 就已经不可接受，更别说本题的 `n ≤ 10^5`。
- **空间复杂度**：`O(2^n)`（用于存放所有子序列的组合索引），实际上只要集合 `gcd_set`，空间是 `O(K)`，`K` 为不同 GCD 的数量，最坏也不会超过 `max(nums)`。

> **大白话**：暴力解相当于把所有可能的“吃法”都尝一遍，数量爆炸，根本跑不完。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的难点在 **“到底哪些整数可以成为某个子序列的 GCD？”**。  
我们不需要真的去枚举子序列，只要判断 **某个整数 `x` 是否可能是 GCD**，就可以把 `x` 加入答案。

**关键观察 1**  
如果一个子序列的 GCD 为 `x`，那么子序列里的每个数必定是 `x` 的倍数。  
> 把 `x` 想成“公共的钥匙”，只有能被它整除的数字才能一起打开（组成）这个子序列的大门。

**关键观察 2**  
把子序列里所有 **倍数** 都取出来（即把所有能被 `x` 整除的数全部保留下来），它们的 GCD **不会比 `x` 更大**，因为加入更多数只能让 GCD 变小或保持不变。  
如果这堆数的 GCD 正好等于 `x`，说明 **至少存在一个子序列的 GCD 为 `x`**（最小的子序列可以只取其中任意两个数）。

**关键观察 3**  
设 `cnt[v]` 为数组中数值等于 `v` 的出现次数（`v` 最大不超过 `2·10^5`），我们可以用一个 **频率数组**（类似查字典的哈希表）快速判断某个数是否在原数组里出现。  

基于以上三点，算法如下：

1. 统计 `cnt`，记下数组中出现的每个数的频率。  
2. 枚举可能的 GCD `g` 从 `1` 到 `max(nums)`（记为 `M`）。  
3. 对于每个 `g`，遍历它的所有倍数 `m = g, 2g, 3g, … ≤ M`。如果 `cnt[m] > 0`（说明原数组里有这个数），把 `m` 加入当前集合并用 `gcd` 累计。  
4. 最终得到的累计 GCD 记作 `cur_gcd`。如果 `cur_gcd == g`，说明 **存在一个子序列的 GCD 正好是 `g`**，答案计数加一。  

整个过程类似 **筛法**（埃拉托斯特尼筛），时间复杂度是所有 `g` 的倍数之和，即  

\[
\sum_{g=1}^{M} \frac{M}{g} = M \cdot (1 + \frac12 + \frac13 + …) \approx M \log M
\]

对 `M ≤ 2·10^5` 完全可以接受。

> **为什么不需要真正的子序列？**  
> 因为我们只关心“是否存在”，而不是具体是哪一个。只要所有倍数的 GCD 等于 `g`，就一定能挑选出若干个数让它们的 GCD 为 `g`（比如挑选两两个互质的倍数即可）。

#### 代码（Python）

```python
import math
from typing import List

def countDifferentGCDs(nums: List[int]) -> int:
    """
    返回所有非空子序列的不同 GCD 的数量
    """
    M = max(nums)                         # 题目保证 M <= 2 * 10^5
    cnt = [0] * (M + 1)                    # 频率数组，cnt[v] 表示 v 出现了多少次
    for v in nums:
        cnt[v] += 1

    ans = 0

    # 枚举可能的 GCD g
    for g in range(1, M + 1):
        cur_gcd = 0                        # 用来累计所有是 g 的倍数的数的 GCD
        # 遍历 g 的所有倍数 m = g, 2g, 3g, ...
        for m in range(g, M + 1, g):
            if cnt[m]:                     # 只关心原数组里出现过的数
                cur_gcd = math.gcd(cur_gcd, m)   # 逐步合并 GCD
                # 如果已经等于 g，后面再合并也不会变大，直接可以提前结束
                if cur_gcd == g:
                    break
        # 若累计的 GCD 正好等于 g，则说明 g 是某子序列的 GCD
        if cur_gcd == g:
            ans += 1

    return ans

# ------------------- 示例 -------------------
print(countDifferentGCDs([6, 10, 3]))          # 5
print(countDifferentGCDs([5, 15, 40, 5, 6]))   # 7
```

**代码要点解释（中文注释）**  

- `cnt` 相当于“字典”，`cnt[v]` 告诉我们 “第 `v` 页是否在书里”。  
- `for g in range(1, M + 1)` 是在尝试每一个可能的“钥匙”。  
- `for m in range(g, M + 1, g)` 用步长 `g` 把所有 `g` 的倍数一次性挑出来，类似 “把所有能被 `g` 整除的数字放进篮子”。  
- `cur_gcd = math.gcd(cur_gcd, m)` 把篮子里所有数字的公共钥匙逐个合并。  
- 当 `cur_gcd` 已经等于 `g` 时，后面再合并也不可能把它变大（只能保持或变小），所以可以 **提前退出**，进一步加速。  

#### 复杂度  

- **时间复杂度**：`O(M log M)`，其中 `M = max(nums) ≤ 2·10^5`。  
  - 大白话：我们相当于对每个数 `1 … M` 都跑一次“筛”，总共大约 `M` 乘以自然对数 `ln M`（约 12）次操作，几百万次，电脑一秒能搞定。  
  - 与暴力解的 `O(2^n)` 相比，下降了 **指数级**，从不可想象的天文数字降到几百万。

- **空间复杂度**：`O(M)` 用于存放频率数组 `cnt`。  
  - 只需要 200k 整数的空间，约几百 KB，极其轻量。

---

## 心得

- **核心技巧**：利用 **“所有倍数的 GCD 等于目标值”** 的逆向思考，把原问题转化为 “遍历可能的 GCD 并检查其倍数”。这是一种 **数论筛**（sieve）思路，常用于 **“能否用若干数满足某个公因数/公倍数条件”** 的题目。  
- **适用的类似题型**  
  1. *LeetCode 1979 – Find Greatest Common Divisor of Array*（求数组中任意两数的最大 GCD）  
  2. *LeetCode 2403 – Minimum Traversal Cost*（需要判断某个数能否被若干数整除）  
  3. *LeetCode 1512 – Number of Good Pairs*（通过哈希表计数的技巧）  
- **一句话总结解题钥匙**：**“把‘是否存在子序列的 GCD = x’转化为‘所有 x 的倍数的 GCD 是否等于 x’，用频率数组和筛法一次性检查所有 x”。**

---

## 反思

- **拿到题目第一反应**：直接想遍历子序列，计算 GCD，想把结果放进集合。  
- **最容易踩的坑**  
  - **时间爆炸**：`2^n` 的子序列数量根本不可遍历。  
  - **忽视空子序列**：题目要求非空子序列，别把空集合算进去。  
  - **边界值**：`nums` 中的最大值可能达到 `2·10^5`，需要预先知道上限来建数组。  
  - **提前结束**：在遍历倍数时，如果累计的 GCD 已经等于当前 `g`，可以立即 `break`，否则会不必要地继续循环。  
- **下次遇到同类题，第一步该想到**：  
  1. **先思考“是否存在”而不是“怎么构造”。**  
  2. **寻找可以把整个搜索空间压缩到‘数值范围’而不是‘子序列组合数’的属性”，比如“倍数”“因子”“前缀和”等。  

这样往往可以把指数级的暴力直接降到线性或准线性，顺利 AC。