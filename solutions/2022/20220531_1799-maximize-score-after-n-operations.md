# #1799. 最大化 N 次操作后的得分 / Maximize Score After N Operations

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Backtracking、Bit Manipulation、Number Theory、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximize-score-after-n-operations/)

---

## 题目（英文原版）

**Description**

You are given nums, an array of positive integers of size 2 * n. You must perform n operations on this array.
In the ith operation (1-indexed), you will:
Return the maximum score you can receive after performing n operations.
The function gcd(x, y) is the greatest common divisor of x and y.

**Examples**

**Example 1:**

```
Input: nums = [1,2]
Output: 1
Explanation: The optimal choice of operations is:
(1 * gcd(1, 2)) = 1
```

**Example 2:**

```
Input: nums = [3,4,6,8]
Output: 11
Explanation: The optimal choice of operations is:
(1 * gcd(3, 6)) + (2 * gcd(4, 8)) = 3 + 8 = 11
```

**Example 3:**

```
Input: nums = [1,2,3,4,5,6]
Output: 14
Explanation: The optimal choice of operations is:
(1 * gcd(1, 5)) + (2 * gcd(2, 4)) + (3 * gcd(3, 6)) = 1 + 4 + 9 = 14
```

**Constraints**

- 1 <= n <= 7
- nums.length == 2 * n
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个长度为 `2 * n` 的正整数数组 `nums`，需要对该数组执行恰好 `n` 次操作。  

在第 `i` 次操作（**1-indexed**，即从 1 开始计数）中，你必须：

1. 从当前数组中任选 **两个** 元素 `x` 和 `y`，将它们从数组中移除；
2. 计算 `gcd(x, y)`，其中 `gcd(x, y)` 为 `x` 与 `y` 的最大公约数（**greatest common divisor**）；
3. 将 `i * gcd(x, y)` 加入总得分。

在完成所有 `n` 次操作后，返回可以获得的 **最大得分**。

---

### 示例

**示例 1**  
> **输入**: `nums = [1,2]`  
> **输出**: `1`  
> **解释**:  
> 最优的操作方式为:  
> \((1 * \text{gcd}(1, 2)) = 1\)

**示例 2**  
> **输入**: `nums = [3,4,6,8]`  
> **输出**: `11`  
> **解释**:  
> 最优的操作方式为:  
> \((1 * \text{gcd}(3, 6)) + (2 * \text{gcd}(4, 8)) = 3 + 8 = 11\)

**示例 3**  
> **输入**: `nums = [1,2,3,4,5,6]`  
> **输出**: `14`  
> **解释**:  
> 最优的操作方式为:  
> \((1 * \text{gcd}(1, 5)) + (2 * \text{gcd}(2, 4)) + (3 * \text{gcd}(3, 6)) = 1 + 4 + 9 = 14\)

---

### 约束

- `1 <= n <= 7`
- `nums.length == 2 * n`
- `1 <= nums[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求我们 **从 2·n 个数中每次挑出两两配对**，配对的顺序会影响最终得分，因为第 i 次操作要乘以系数 `i`。  
最直接的想法就是 **把所有可能的配对顺序枚举一遍**，每一种配对方式算出它的得分，取最大值。

- **用到的数据结构**  
  - **数组** `nums` 保存所有数字。  
  - **位掩码（bitmask）**：把 2·n 个位置用二进制的 0/1 标记是否已经被取走。  
    - 想象一下我们在 **查字典**，字典的每一页对应一个数，`1` 表示这页已经被“借走”，`0` 表示还在书架上。  
- **为什么正确**  
  - 我们遍历了**所有合法的配对序列**，不遗漏也不重复。只要把每一种序列算出分数，最大值必然就是答案。  
- **时间/空间复杂度（大白话解释）**  
  - 配对的总方案数等价于 **把 2·n 个人两两配对**，这叫 **完全匹配的计数**，数量是  
    \[
    \frac{(2n)!}{2^{n}\,n!}
    \]  
    举个例子，`n=7`（即 14 个数）时大约有 **135135** 种配对方式，虽然看起来很多，但在电脑里跑一遍还是可以接受的。  
  - **时间复杂度**：\(O\big(\frac{(2n)!}{2^{n}n!}\big)\)——随着 `n` 增长会指数级爆炸。  
  - **空间复杂度**：递归栈深度为 `n`，以及记录已使用元素的位掩码，都是 **\(O(n)\)**，几乎可以忽略不计。

#### 代码（Python）

```python
import math
from functools import lru_cache
from typing import List

def maxScore(nums: List[int]) -> int:
    """
    暴力递归 + 位掩码
    nums 长度为 2 * n，n ≤ 7
    """
    m = len(nums)                 # m = 2 * n
    full_mask = (1 << m) - 1      # 所有位置都被使用时的掩码

    @lru_cache(None)              # 记忆化，避免同一状态重复计算
    def dfs(mask: int, op: int) -> int:
        """
        mask : 已经被取走的下标对应的位为 1
        op   : 当前是第几次操作（从 1 开始）
        返回：从当前状态出发能够得到的最大剩余得分
        """
        if mask == full_mask:     # 所有数都已经配对完
            return 0

        best = 0
        # 找到第一个还没被使用的数 i
        for i in range(m):
            if not (mask >> i) & 1:
                # 把 i 选出来后，继续找第二个 j
                for j in range(i + 1, m):
                    if not (mask >> j) & 1:
                        new_mask = mask | (1 << i) | (1 << j)
                        cur = op * math.gcd(nums[i], nums[j]) + dfs(new_mask, op + 1)
                        best = max(best, cur)
                break   # i 已经确定为最左边的未使用位置，后面的递归会自行处理
        return best

    return dfs(0, 1)   # 初始时没有取走任何数，操作序号从 1 开始
```

- `math.gcd` 用来求两个数的最大公约数。  
- `lru_cache` 把已经算过的 `(mask, op)` 记住，避免同一个子问题重复递归。  
- `mask` 用二进制记录哪些下标已经配对，`1 << i` 表示把第 `i` 位设为 1（即“借走”这个数）。

#### 复杂度

- **时间复杂度**：\(O\big(\frac{(2n)!}{2^{n}n!}\big)\)。  
  - 用通俗的话说：当 `n=7` 时，大约要检查 135,135 种配对方式，电脑可以在几毫秒内完成。  
- **空间复杂度**：\(O(2^{2n})\)（缓存的状态数）+ \(O(n)\)（递归深度）。  
  - 实际上 `2^{2n}` 在 `n≤7` 时最多是 `2^{14}=16384`，占用的内存只有几百 KB。

---  

### 2. 最优解  

#### 思路  

暴力解已经可以跑通，但它的时间仍然是 **指数级**，如果把 `n` 放大一点就会失效。  
观察递归过程可以发现：

1. **状态只由已经使用的元素集合决定**。  
   - 也就是说，只要知道哪些下标被配对了，接下来要进行的操作次数 `op` 其实可以从 `mask` 推算出来：  
     \[
     op = \frac{\text{已使用的元素个数}}{2}+1
     \]  
     因为每一次操作恰好使用 2 个数。  
2. 对同一个 `mask`，我们会在不同的递归路径上多次计算它的最优得分。  
   - 这正是 **子问题重复** 的典型表现，适合用 **动态规划 + 记忆化**（也叫“位掩码 DP”）来一次性算出。

**核心想法**：用一个数组 `dp[mask]` 记录 **从当前已使用集合 `mask` 出发可以得到的最大剩余得分**。  
从 “所有数都已经使用” 的状态往回推（自底向上）或者用递归+记忆化（自顶向下）都可以，这里仍然采用递归+记忆化，但把 `op` 省掉，只用 `mask` 推算。

**步骤**  

1. `full_mask = (1 << (2n)) - 1` 表示所有数都已配对。  
2. `dp[full_mask] = 0`，因为没有数可以再配对，得分为 0。  
3. 对任意 `mask`（未满），找出两个未使用的下标 `i, j`，形成新状态 `new_mask = mask | (1<<i) | (1<<j)`。  
   - 当前操作的序号 `op = cnt(mask)//2 + 1`，其中 `cnt(mask)` 是 `mask` 中 `1` 的个数（即已经使用的元素数）。  
   - 计算这一步的得分 `op * gcd(nums[i], nums[j])`，再加上 `dp[new_mask]`（后面的最优得分），取最大。  
4. 递归结束后 `dp[0]`（即没有使用任何数的起始状态）即为答案。

**为什么快**  

- **状态总数**只有 `2^{2n}`（最多 16384），远小于暴力枚举的 `(2n)!/(2^n n!)`。  
- 对每个状态我们只尝试 **未使用的两两组合**，每次最多遍历 `C(2n,2) = (2n)*(2n-1)/2` 次。  
- 整体时间大约是 `O( (2n)^2 * 2^{2n} )`，在 `n ≤ 7` 的限制下几乎是瞬间完成。

#### 代码（Python）

```python
import math
from functools import lru_cache
from typing import List

def maxScore(nums: List[int]) -> int:
    """
    位掩码 DP（自顶向下记忆化搜索）
    时间：O((2n)^2 * 2^{2n})，空间：O(2^{2n})
    """
    m = len(nums)                 # = 2 * n
    full_mask = (1 << m) - 1

    # 计算 mask 中 1 的个数（已使用的元素个数）
    def bits_cnt(x: int) -> int:
        return bin(x).count('1')

    @lru_cache(None)
    def dp(mask: int) -> int:
        if mask == full_mask:     # 所有数都已配对
            return 0

        # 当前是第几次操作（从 1 开始）
        op = bits_cnt(mask) // 2 + 1
        best = 0

        # 找到第一个未使用的 i，避免重复枚举相同的配对集合
        for i in range(m):
            if not (mask >> i) & 1:
                for j in range(i + 1, m):
                    if not (mask >> j) & 1:
                        new_mask = mask | (1 << i) | (1 << j)
                        cur = op * math.gcd(nums[i], nums[j]) + dp(new_mask)
                        best = max(best, cur)
                break   # 只让 i 固定为最左侧未使用的，下层递归会自行遍历其余组合
        return best

    return dp(0)    # 从空集合开始
```

- `bits_cnt` 用来算出已经配对了多少个数，从而得到当前操作的系数 `op`。  
- `break` 只让最左边的未使用元素 `i` 进入循环，这样可以 **避免同一配对集合被不同顺序重复计数**（类似组合而非排列）。  

#### 复杂度

- **时间复杂度**：\(O((2n)^2 \cdot 2^{2n})\)。  
  - 对比暴力解，时间从 “\(\frac{(2n)!}{2^{n}n!}\)” 降到了 “\(2^{2n}\) 乘以一个多项式因子”。  
  - 当 `n=7` 时约为 `14^2 * 16384 ≈ 3.2 × 10^6` 次基本运算，毫秒级完成。  
- **空间复杂度**：\(O(2^{2n})\) 用于缓存所有 `mask` 的结果，最多 `16384` 个整数，只有几百 KB。

---  

## 心得  

- **核心技巧**：**位掩码 DP（记忆化搜索）**，把“已经选过的元素集合”抽象成二进制状态，利用子问题重叠性实现指数级的剪枝。  
- **适用题型**（类似思路可直接套用）：  
  1. **配对类最大化/最小化**：如 *1725. 最小距离对*（需要配对点），*1799. 最大奇数分数*（配对取模）。  
  2. **分割/组合类**：如 *1987. 第 N 天的最大收益*（用掩码表示已完成的任务），*1260. 递增子序列的最大和*（子集 DP）。  
- **一句话总结解题钥匙**：**把“哪些元素已经用过”用二进制掩码记录，递归/DP 只在这些状态上做一次最优计算**。

## 反思  

- **第一反应**：看到“挑两两配对，乘以操作序号”就想到“全排列/全组合”，于是直接写了暴力递归。  
- **最容易踩的坑**  
  - **忘记除以 2 计算操作序号**：`op = 已使用元素数 / 2 + 1`，否则会把系数算错。  
  - **重复计数**：若不让 `i` 固定为最左未使用的下标，会把同一配对集合按不同顺序算多次，导致时间爆炸。  
  - **位运算细节**：`mask >> i & 1` 必须加上括号防止优先级错误。  
- **下次遇到同类题**：第一步先 **判断是否可以用位掩码描述已选元素**，若可以，就立刻建立 “状态 = 已使用的集合”，再考虑 **记忆化搜索 / DP**，而不是直接遍历所有排列。这样可以把指数级的搜索压到可接受的范围。