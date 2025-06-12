# #3224. 最小数组修改次数使差值相等 / Minimum Array Changes to Make Differences Equal

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-array-changes-to-make-differences-equal/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of size n where n is even, and an integer k.
You can perform some changes on the array, where in one change you can replace any element in the array with any integer in the range from 0 to k.
You need to perform some changes (possibly none) such that the final array satisfies the following condition:
Return the minimum number of changes required to satisfy the above condition.

**Examples**

**Example 1:**

```
Input: nums = [1,0,1,2,4,3], k = 4
Output: 2
Explanation: We can perform the following changes:
The integer X will be 2.
```

**Example 2:**

```
Input: nums = [0,1,2,3,3,6,5,4], k = 6
Output: 2
Explanation: We can perform the following operations:
The integer X will be 4.
```

**Constraints**

- 2 <= n == nums.length <= 105
- n is even.
- 0 <= nums[i] <= k <= 105

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`（其中 `n` 为偶数）以及一个整数 `k`。  
你可以对数组进行若干次 **修改（change）**，一次修改可以将数组中的任意元素替换为 `[0, k]` 区间内的任意整数。

请在进行（可能为零次）修改后，使得最终数组满足如下条件：  
对于所有 `0 ≤ i < n/2`，`|nums[i] - nums[n‑1‑i]|` 的值都相等（记为整数 `X`），即每一对对称位置的元素差的绝对值相同。

返回满足上述条件所需的 **最少修改次数**。

### 示例

**示例 1**

```
输入: nums = [1,0,1,2,4,3], k = 4
输出: 2
解释: 我们可以进行以下两次修改，使得所有对称位置的差的绝对值均为 X = 2。
```

**示例 2**

```
输入: nums = [0,1,2,3,3,6,5,4], k = 6
输出: 2
解释: 进行两次操作后，所有对称位置的差的绝对值均为 X = 4。
```

### 约束条件

- `2 <= n == nums.length <= 10^5`
- `n` 为偶数
- `0 <= nums[i] <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **枚举目标和 X**（X 是所有配对的和，题目要求所有 `i` 与 `n-1-i` 的和相同）。  
2. 对每一对 `(nums[i], nums[n-1-i])`，判断把它们变成和 `X` 最少需要几次修改：  
   - 已经等于 `X` → 0 次  
   - 改动其中 **一个** 元素就能得到 `X` → 1 次  
   - 两个都要改动 → 2 次  
3. 把所有配对的修改次数加起来，取所有可能的 `X` 中的最小值。

> **数据结构类比**：  
> - `Hash Table（哈希表）` 可以想象成一本**词典**，`key` 是单词，`value` 是对应的页码。这里我们不需要哈希表，只需要 **遍历**（循环）和 **计数**。

> **为什么正确**：  
> 只要把所有配对的和都统一为同一个 `X`，题目就满足了。暴力遍历所有 `X` 并逐对检查，必然可以找到最少的修改次数。

> **时间/空间分析**：  
> - `X` 的取值范围是 `2 … 2k`（因为每个元素在 `[0, k]`），最多有 `2k-1` 种可能。  
> - 对每一种 `X`，我们要遍历 `n/2` 对元素，做常数次判断。  
> - 所以时间复杂度是 `O((2k) * (n/2)) ≈ O(n·k)`。如果 `k` 与 `n` 都是 `10^5`，最坏会是 `10^10`，根本跑不完。  
> - 只用到几个计数变量，空间复杂度是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def min_changes_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    half = n // 2
    ans = float('inf')

    # X 的可能取值从 2 到 2k
    for X in range(2, 2 * k + 1):
        cur = 0
        for i in range(half):
            a, b = nums[i], nums[n - 1 - i]
            s = a + b
            if s == X:               # 已经等于 X，无需修改
                continue
            # 看能否只改动一个数就得到 X
            # a 改动后要变成 X - b，范围必须在 [0, k]，同理 b
            if (0 <= X - a <= k) or (0 <= X - b <= k):
                cur += 1             # 只需要一次修改
            else:
                cur += 2             # 两个都要改
        ans = min(ans, cur)

    return ans
```

> 代码里每个关键判断都有中文注释，直接可以运行。  

#### 复杂度

- **时间复杂度**：`O(n·k)` —— 想象成“把 n 张纸和 k 本书全部配对检查”，规模太大会卡死。  
- **空间复杂度**：`O(1)` —— 只用了几个整数计数器，几乎不占内存。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **重复遍历**：对每个可能的 `X` 都要重新遍历所有配对。  
我们要做的，是 **一次遍历** 所有配对，就把每个 `X` 需要的修改次数 **累计** 好。

关键观察：

1. 对于一对数 `(a, b)`，把它们的和变成 `X` 最少需要的操作数只可能是 **0、1、2**。
2.  
   - **0 次**：当 `a + b == X` 时。  
   - **1 次**：只要 `X` 落在区间 `[min(a, b)+1, max(a, b)+k]`，就可以只改动较小的数或较大的数得到 `X`。  
   - **2 次**：其余所有 `X`（即不在上面两种情况里）必须改动两个数。

3. 设总配对数为 `m = n/2`。如果不做任何优化，所有配对默认需要 **2 次** 修改 → 初始答案是 `2·m`。  
   接下来对每一对 `(a, b)`：
   - 对于 **0 次** 的 `X = a+b`，我们可以把答案再 **-1**（从 2 降到 0）。  
   - 对于 **1 次** 的区间 `[L, R] = [min(a,b)+1, max(a,b)+k]`，我们可以把答案再 **-1**（从 2 降到 1）。

4. 如何在一次遍历中把所有区间的 “-1” 操作累计到每个 `X`？  
   使用 **差分数组 + 前缀和**（也叫“扫描线”）：

   - 创建一个长度为 `2k+2` 的数组 `diff`，全部初始化为 0。  
   - 对于区间 `[L, R]`，执行 `diff[L] += 1`，`diff[R+1] -= 1`。  
   - 最后对 `diff` 做前缀和，得到 `one_change[x]` —— 需要 **恰好 1 次** 修改的配对数量（相对于默认的 2 次）。  
   - 同理，用一个哈希表（或额外数组）记录每个具体和 `s = a+b` 出现的次数 `zero_change[s]`。

5. 计算每个可能的 `X` 的总修改次数：

```
total_changes[X] = 2*m                # 默认 2 次
                - one_change[X]      # 减去可以只改动 1 次的配对数
                - zero_change[X]     # 再减去已经满足的配对数
```

6. 只需遍历 `X = 2 … 2k`，取最小值即为答案。

> **核心数据结构解释**  
> - **差分数组**：想象成一条路上的“增减标记”。在起点 `L` 放一个“+1”，在终点的后一个位置 `R+1` 放一个 “-1”。走路时累计标记（前缀和），路上每一点的累计值就是这段路上有多少标记在起作用。这里的“标记”表示“这对数可以用 1 次改动达成的 X 区间”。  
> - **前缀和**：把差分数组的累计过程叫前缀和，就像从左到右走，手里一直装着“当前有多少标记在起作用”。  

#### 代码（Python）

```python
from typing import List

def minChanges(nums: List[int], k: int) -> int:
    n = len(nums)
    m = n // 2                      # 配对数量
    max_sum = 2 * k

    # diff 用来记录「可以只改动 1 次」的区间贡献
    diff = [0] * (max_sum + 2)      # +2 防止访问 R+1 越界
    # zero_cnt 用来统计「已经满足」的具体和出现次数
    zero_cnt = [0] * (max_sum + 1)

    for i in range(m):
        a, b = nums[i], nums[n - 1 - i]
        s = a + b
        zero_cnt[s] += 1           # 0 次修改的情况

        lo = min(a, b) + 1         # 能只改动一个数的最小目标和
        hi = max(a, b) + k         # 能只改动一个数的最大目标和

        # 把区间 [lo, hi] 用差分标记为「-1」 (从默认的 2 次降到 1 次)
        diff[lo] += 1
        diff[hi + 1] -= 1

    # 前缀和得到每个 X 需要「1 次」的配对数量
    one_change = [0] * (max_sum + 1)
    cur = 0
    for x in range(2, max_sum + 1):
        cur += diff[x]
        one_change[x] = cur

    # 计算答案
    ans = float('inf')
    for X in range(2, max_sum + 1):
        # 默认 2*m 次，减去能只改动 1 次的配对数，再减去已经满足的配对数
        changes = 2 * m - one_change[X] - zero_cnt[X]
        ans = min(ans, changes)

    return ans
```

> **代码注释** 已经写在每一行的右侧，直接复制即可运行。

#### 复杂度

- **时间复杂度**：`O(n + k)`  
  - 只遍历一次数组 (`O(n)`) 来收集区间信息。  
  - 再遍历 `2k` 次求前缀和和最小值 (`O(k)`)。  
  - 与暴力的 `O(n·k)` 相比，线性级别的算法在 `10^5` 规模下轻松跑完。  
- **空间复杂度**：`O(k)`  
  - 需要两个长度约为 `2k` 的辅助数组 `diff`、`zero_cnt`（相当于几百 KB），不随 `n` 增长。

---

## 心得

- **核心技巧**：**差分数组 + 前缀和** 用来一次性统计所有目标值的「1 次改动」区间。  
- **适用场景**：  
  1. LeetCode 1674 – *Minimum Array Changes to Make Differences Equal*（本题）。  
  2. LeetCode 1102 – *Path With Maximum Minimum Value*（需要区间统计）。  
  3. LeetCode 1657 – *Determine if Two Strings Are Close*（也涉及全局计数差分的思想）。  
- **一句话总结**：把所有配对默认视作「需要改动 2 次」，然后用差分数组一次性把「可以省 1 次」和「可以省 2 次」的情况扣除，最小值即为答案。

---

## 反思

- **第一反应**：看到“把每对数的和统一”为 X，立刻想到「枚举 X」并逐对检查——这就是暴力思路。  
- **最容易踩的坑**：  
  - 区间 `[min+1, max+k]` 的边界要写对，尤其是 `+1` 与 `+k` 的含义。  
  - 差分数组的大小必须是 `2k+2`，防止对 `hi+1` 越界。  
  - 记得 `X` 的取值从 **2**（最小和）到 **2k**（最大和），不包括 0 或 1。  
- **下次遇到同类题**：第一步先思考「默认情况」需要多少操作，再找出「可以省掉几次」的区间/条件，使用差分或前缀和一次性累计。这样可以把原本的二重循环降到线性时间。