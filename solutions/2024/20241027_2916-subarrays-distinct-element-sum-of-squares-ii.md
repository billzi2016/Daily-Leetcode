# #2916. 子数组不同元素计数的平方和 II / Subarrays Distinct Element Sum of Squares II

> 难度：困难 · 标签：Array、Dynamic Programming、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/subarrays-distinct-element-sum-of-squares-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
The distinct count of a subarray of nums is defined as:
Return the sum of the squares of distinct counts of all subarrays of nums.
Since the answer may be very large, return it modulo 109 + 7.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1]
Output: 15
Explanation: Six possible subarrays are:
[1]: 1 distinct value
[2]: 1 distinct value
[1]: 1 distinct value
[1,2]: 2 distinct values
[2,1]: 2 distinct values
[1,2,1]: 2 distinct values
The sum of the squares of the distinct counts in all subarrays is equal to 12 + 12 + 12 + 22 + 22 + 22 = 15.
```

**Example 2:**

```
Input: nums = [2,2]
Output: 3
Explanation: Three possible subarrays are:
[2]: 1 distinct value
[2]: 1 distinct value
[2,2]: 1 distinct value
The sum of the squares of the distinct counts in all subarrays is equal to 12 + 12 + 12 = 3.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个 **0 起始索引** 的整数数组 `nums`。  
子数组（subarray）的 **不同元素计数** 定义为该子数组中不重复的元素个数。  

返回 `nums` 所有子数组的不同元素计数的平方和。由于答案可能非常大，请返回 **10^9 + 7** 取模后的结果。  

子数组是数组中连续且非空的元素序列。

**示例 1**  
```text
Input: nums = [1,2,1]
Output: 15
Explanation: 一共有六个子数组：
[1]：1 个不同的值
[2]：1 个不同的值
[1]：1 个不同的值
[1,2]：2 个不同的值
[2,1]：2 个不同的值
[1,2,1]：2 个不同的值
所有子数组的不同元素计数的平方和为 1^2 + 1^2 + 1^2 + 2^2 + 2^2 + 2^2 = 15。
```

**示例 2**  
```text
Input: nums = [2,2]
Output: 3
Explanation: 一共有三个子数组：
[2]：1 个不同的值
[2]：1 个不同的值
[2,2]：1 个不同的值
所有子数组的不同元素计数的平方和为 1^2 + 1^2 + 1^2 = 3。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是把所有子数组枚举出来，逐个统计子数组里不同元素的个数 `cnt`，再把 `cnt²` 累加得到答案。

- **枚举子数组**：  
  对每个左端点 `l`（从 `0` 到 `n‑1`），再枚举右端点 `r`（从 `l` 到 `n‑1`），子数组就是 `nums[l … r]`。  
- **统计不同元素**：  
  用一个 `set`（集合）把子数组里出现的数字收集起来，集合的大小就是不同元素的个数。  
  > `set` 在生活中可以类比为“字典”，把每个单词（这里是数组元素）记下来，只要出现过一次就算进集合，重复的就不再计数。

- **累加平方**：把每个子数组得到的 `cnt` 先平方再加到答案中。

> **为什么暴力法一定能对**  
> 我们把题目要求的“所有子数组”全部列举出来，且对每个子数组都完整地算出了 “不同元素个数的平方”。没有遗漏，也没有多算，故答案必然正确。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

def subarraysDistinctElementSumOfSquares_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    # 枚举左端点
    for l in range(n):
        seen = set()          # 记录当前子数组出现过的元素
        # 右端点向右移动
        for r in range(l, n):
            seen.add(nums[r]) # 把新加入的元素放进集合，重复的自动被忽略
            cnt = len(seen)   # 不同元素的个数
            ans = (ans + cnt * cnt) % MOD   # 累加平方，取模防溢出
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环分别遍历左端点和右端点，最坏情况下要检查 `n·(n+1)/2 ≈ n²/2` 个子数组。  
  大白话：如果 `n = 10⁵`，`n²` 大约是 `10¹⁰`，远远超出一秒能跑完的量级。

- **空间复杂度**：`O(n)`（集合的大小）  
  最坏情况下子数组里全部不同元素，需要把 `n` 个数装进集合。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有子数组**，这一步是 `O(n²)`。  
我们要把“子数组的不同元素个数”以及它的 **平方**，在 **一次遍历** 中累计出来。  

关键观察：

1. **从左到右依次加入元素**  
   设我们已经处理到下标 `i‑1`，并且维护了所有以 `i‑1` 结尾的子数组的 **不同元素个数**（记作 `dist[s]`，`s` 为子数组的左端点）。  
   当把第 `i` 个元素 `x = nums[i]` 加入时，只有左端点 `s` 大于 `x` 上一次出现位置 `prev` 的子数组会把 `x` 当作 **新元素**，其 `dist` 要 **+1**；其它子数组的 `dist` 保持不变。

2. **平方的增量**  
   对于一个子数组，原来的不同元素个数是 `d`，加上新元素后变成 `d+1`，平方的变化是  
   \[
   (d+1)^2 - d^2 = 2d + 1
   \]
   因此 **每个左端点在 `prev+1 … i` 区间内**，答案要增加 `2·d + 1`。  
   这里的 `d` 正是我们之前维护的 `dist[s]`。

3. **我们需要快速得到**  
   - 区间 `[L, R]`（即 `prev+1 … i`）内 **所有 `dist[s]` 的和**（记作 `sumDist`），用于计算 `2·sumDist`。  
   - 区间长度 `len = R-L+1`，用于加上 `+1` 的部分。

   这两件事都可以用 **支持区间加、区间求和** 的数据结构实现——**树状数组（Fenwick）** 或 **线段树**。这里用更轻量的 Fenwick（两棵树实现区间加+区间和）。

4. **数据结构的工作原理（零基础解释）**  
   - **树状数组**：把数组的前缀和拆成若干段，利用二进制特性可以在 `log n` 时间内完成“单点修改+前缀求和”。  
   - **区间加**：把“在 `[L,R]` 区间里每个位置都加 `v`”拆成两次“单点修改”。  
   - **区间求和**：通过维护两棵树 `bit1、bit2`，可以在 `log n` 时间得到任意区间的和。  
   > 类比：想象有一本厚厚的电话簿（数组），我们要在某一段页码里批量写上同一个号码（区间加），而后随时查询某几页的总和（区间和）。树状数组就像是帮我们在每一层索引快速定位到对应的页码段。

5. **整体流程**  

   | 步骤 | 说明 |
   |------|------|
   | 初始化 | `last` 哈希表记录每个数上一次出现的下标；两棵 Fenwick 树 `bit1、bit2` 全部 0；答案 `ans = 0` |
   | 循环 i=0…n‑1 | 1️⃣ 取 `prev = last.get(nums[i], -1)` <br>2️⃣ 计算区间 `[L,R] = [prev+2, i+1]`（Fenwick 用 1‑based 索引）<br>3️⃣ 若 `L ≤ R`：<br> a. `oldSum = range_sum(L,R)`（这就是所有 `dist[s]` 的和）<br> b. `ans += 2·oldSum + (R-L+1)`（对应 `2d+1` 的累计）<br> c. `range_add(L,R,1)` 把这些子数组的 `dist` 加 1，供后面使用<br>4️⃣ 更新 `last[nums[i]] = i` |
   | 最后 | 返回 `ans % MOD` |

   这样只遍历一次数组，每一步只做 `O(log n)` 的树状数组操作，总体是 `O(n log n)`。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7

# ---------- Fenwick（树状数组） ----------
class Fenwick:
    """支持区间加 + 区间求和（两棵树实现）"""
    def __init__(self, n: int):
        self.n = n
        self.bit1 = [0] * (n + 2)   # 1‑based
        self.bit2 = [0] * (n + 2)

    def _add(self, bit: List[int], idx: int, delta: int) -> None:
        """单点加 delta 到 bit[idx]，向上维护"""
        while idx <= self.n:
            bit[idx] = (bit[idx] + delta) % MOD
            idx += idx & -idx

    def range_add(self, l: int, r: int, delta: int) -> None:
        """把 [l, r]（均为 1‑based）每个位置都加 delta"""
        # 对 bit1、bit2 分别做差分更新
        self._add(self.bit1, l, delta)
        self._add(self.bit1, r + 1, -delta)
        self._add(self.bit2, l, delta * (l - 1))
        self._add(self.bit2, r + 1, -delta * r)

    def _prefix(self, bit: List[int], idx: int) -> int:
        """返回 bit 前缀和"""
        s = 0
        while idx > 0:
            s = (s + bit[idx]) % MOD
            idx -= idx & -idx
        return s

    def prefix_sum(self, idx: int) -> int:
        """返回原数组前缀和 sum[1..idx]"""
        # 公式：sum = query(bit1, idx) * idx - query(bit2, idx)
        return (self._prefix(self.bit1, idx) * idx - self._prefix(self.bit2, idx)) % MOD

    def range_sum(self, l: int, r: int) -> int:
        """返回区间 [l, r] 的和"""
        return (self.prefix_sum(r) - self.prefix_sum(l - 1)) % MOD


# ---------- 主函数 ----------
def subarraysDistinctElementSumOfSquares(nums: List[int]) -> int:
    n = len(nums)
    bit = Fenwick(n)               # 只需要大小 n，1‑based 索引
    last = dict()                  # 记录每个数上一次出现的位置
    ans = 0

    for i, x in enumerate(nums):
        prev = last.get(x, -1)                 # -1 表示之前没出现过
        # 计算需要更新的左端点区间，转成 1‑based
        L = prev + 2            # prev+1 (0‑based) -> +1 for 1‑based
        R = i + 1               # i (0‑based) -> +1 for 1‑based

        if L <= R:                         # 说明有子数组会把 x 计为新元素
            old_sum = bit.range_sum(L, R)   # 这些子数组原来的 distinct 个数之和
            inc = (2 * old_sum + (R - L + 1)) % MOD   # 2d + 1 的累计
            ans = (ans + inc) % MOD

            # 把这些子数组的 distinct 数量都加 1，供后面使用
            bit.range_add(L, R, 1)

        last[x] = i                         # 更新最近出现位置

    return ans % MOD
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  循环 `n` 次，每次进行常数次 Fenwick 操作（`range_add`、`range_sum`），每个操作的时间是 `O(log n)`。  
  > 与暴力的 `O(n²)` 相比，`log n` 只在 `10⁵` 时约为 17，几乎可以视作线性。

- **空间复杂度**：`O(n)`  
  两棵 Fenwick 树各需要 `n+2` 的整数数组（约 `2n`），再加上哈希表 `last`（最多保存不同元素的下标），总体是线性空间。

---

## 心得

- **核心技巧**：**从子数组右端点逐步递推 + 区间加/区间和的 Fenwick（或线段树）**。  
  把“子数组的不同元素个数”视作一种随左端点变化的 **状态**，当加入新元素时，只在 **左端点大于上一次出现位置** 的区间里统一更新。

- **适用的题型**  
  1. “所有子数组的某种累计值”需要在 **右端点递推**（如子数组最小值之和、最大值之和）。  
  2. “出现次数/是否出现”随左端点变化的题目（如子数组中不同元素个数、出现次数的平方、子数组中出现次数恰好为 1 的元素个数等）。  
  3. 需要 **区间加 + 区间求和** 的场景，常用 Fenwick/线段树实现。

- **一句话总结解题钥匙**：**把“是否为新元素”转化为左端点的区间更新，用树状数组在对数时间内维护子数组的 distinct 计数，进而快速累计平方增量**。

---

## 反思

- **第一反应**：看到“所有子数组”，本能想到双层循环枚举，随后意识到 `n` 高达 `10⁵`，暴力肯定超时，需要寻找 **累计/递推** 的思路。

- **最容易踩的坑**  
  1. **下标转换**：题目使用 0‑based，Fenwick 必须 1‑based，容易忘记 `+1` 或 `+2` 导致区间错位。  
  2. **模运算**：增量 `2·oldSum + len` 以及 Fenwick 的内部更新都要取模，防止负数或溢出。  
  3. **区间长度**：`+1` 的贡献是每个受影响子数组一次，必须用区间长度 `R-L+1` 而不是 `i-prev`（两者等价，但要保持一致）。  

- **下次遇到同类题，第一步该想到**：**把“新出现的元素”映射为左端点的连续区间**，然后思考使用 **区间加 + 区间和** 的数据结构来维护随右端点扩展的状态。这样可以把原本指数级的枚举压缩到 `O(n log n)`。