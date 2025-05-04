# #3171. 寻找与 K 按位或（bitwise OR）最接近的子数组 / Find Subarray With Bitwise OR Closest to K

> 难度：困难 · 标签：Array、Binary Search、Bit Manipulation、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/find-subarray-with-bitwise-or-closest-to-k/)

---

## 题目（英文原版）

**Description**

You are given an array nums and an integer k. You need to find a subarray of nums such that the absolute difference between k and the bitwise OR of the subarray elements is as small as possible. In other words, select a subarray nums[l..r] such that |k - (nums[l] OR nums[l + 1] ... OR nums[r])| is minimum.
Return the minimum possible value of the absolute difference.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,4,5], k = 3
Output: 0
Explanation:
The subarray nums[0..1] has OR value 3, which gives the minimum absolute difference |3 - 3| = 0 .
```

**Example 2:**

```
Input: nums = [1,3,1,3], k = 2
Output: 1
Explanation:
The subarray nums[1..1] has OR value 3, which gives the minimum absolute difference |3 - 2| = 1 .
```

**Example 3:**

```
Input: nums = [1], k = 10
Output: 9
Explanation:
There is a single subarray with OR value 1, which gives the minimum absolute difference |10 - 1| = 9 .
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个数组 `nums` 和一个整数 `k`，请找到 `nums` 的一个子数组（subarray），使得该子数组所有元素的按位或（bitwise OR）与 `k` 之间的绝对差（absolute difference）尽可能小。换句话说，选取一个子数组 `nums[l..r]`，使得  

\[
|k - (nums[l] \text{ OR } nums[l+1] \dots \text{ OR } nums[r])|
\]

的值最小。返回该最小可能的绝对差值。

子数组（subarray）是数组中连续且非空的元素序列。

**示例 1**  
**输入**: `nums = [1,2,4,5]`, `k = 3`  
**输出**: `0`  
**解释**: 子数组 `nums[0..1]` 的按位或（OR）值为 `3`，此时的绝对差 `|3 - 3| = 0` 为最小值。

**示例 2**  
**输入**: `nums = [1,3,1,3]`, `k = 2`  
**输出**: `1`  
**解释**: 子数组 `nums[1..1]` 的按位或（OR）值为 `3`，此时的绝对差 `|3 - 2| = 1` 为最小值。

**示例 3**  
**输入**: `nums = [1]`, `k = 10`  
**输出**: `9`  
**解释**: 唯一的子数组的按位或（OR）值为 `1`，此时的绝对差 `|10 - 1| = 9` 为最小值。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `1 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有子数组**，把每个子数组的元素做按位或（OR），再和 `k` 求绝对差，取最小值。

- **枚举子数组**：可以用两层循环，外层 `l` 表示子数组的左端点，内层 `r` 从 `l` 往右移动，逐步扩展子数组。  
- **计算 OR**：在把 `r` 向右推进的过程中，用一个变量 `cur_or` 累积 `nums[l] | nums[l+1] | … | nums[r]`。  
- **更新答案**：每得到一个 `cur_or`，计算 `abs(k - cur_or)`，如果更小就保存下来。

> **类比**：把数组想成一排灯泡，每盏灯有若干个开关（对应二进制位）。子数组的 OR 就是把这段灯泡的所有开关一次性打开（只会把 0 变成 1，已经是 1 的不会再变）。我们要找的是“打开后”离目标 `k` 最近的那段灯泡。

> **为什么正确**：我们把 **所有可能的子数组** 都遍历了一遍，必然会碰到最优的那一个，所以答案一定会被找到。

#### 代码（Python）

```python
from typing import List

def min_abs_diff_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = float('inf')                 # 初始答案设为正无穷大
    for l in range(n):                 # 左端点
        cur_or = 0                     # 记录区间 [l, r] 的 OR
        for r in range(l, n):          # 右端点逐步右移
            cur_or |= nums[r]          # 把 nums[r] 加入 OR
            diff = abs(k - cur_or)     # 计算当前差值
            if diff < ans:             # 找到更小的就更新
                ans = diff
            # 早停技巧：如果 cur_or 已经 >= k 并且再加任何数只会让它更大，
            # diff 只会增大，可以直接 break（可选优化）。
    return ans
```

> **关键注释**  
> - `cur_or |= nums[r]`：`|=` 相当于 “把当前的 OR 再和新元素做一次 OR”。  
> - `abs(k - cur_or)`：计算绝对差，就是我们要最小化的目标。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环遍历所有子数组，最坏情况下要检查 `n·(n+1)/2 ≈ n²/2` 次。  
  **大白话**：如果数组长度是 10⁴，暴力解大约要做 10⁸ 次运算，通常会超时。

- **空间复杂度**：`O(1)`  
  只用了几个常数级别的变量（`cur_or、ans`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复计算**。当我们从左到右遍历数组时，子数组 `[i … j]` 与 `[i+1 … j]` 只相差左端的一个元素 `nums[i]`，但我们每次都重新算 OR，浪费了很多工作。

**关键观察**：

1. **OR 的单调性**  
   对任意两个整数 `a`、`b`，`a | b` 的二进制位只会把 `0` 变成 `1`，已经是 `1` 的位永远不会再变回 `0`。  
   换句话说，**向左扩展子数组只会让 OR 的值增大（或保持不变）**。

2. **每个位置的 OR 集合大小有限**  
   对于一个固定的右端点 `i`，考虑所有以 `i` 结尾的子数组的 OR 值集合 `dp[i]`。  
   当我们把左端点往左移动时，只有 **未被置位的位** 可能被新加入的元素置为 `1`。  
   由于 `nums[i] ≤ 10⁹`，二进制位数不超过 30（`2³⁰ ≈ 10⁹`），所以 **`dp[i]` 中的不同 OR 值至多 30 个**。  
   这就是题目提示里说的 “dp[i] 最多 30 个元素”。

**利用上述观察**，我们可以 **动态维护** `dp[i]`：

- `dp[i]` = `{ nums[i] } ∪ { x | y for x in dp[i‑1] }`  
  也就是说，所有以 `i‑1` 结尾的子数组的 OR 再和 `nums[i]` 做一次 OR，得到以 `i` 结尾的子数组的 OR；再把单独的 `nums[i]` 加进去。

- 在构造 `dp[i]` 的过程中，用 `set` 去重，保证每个 OR 只出现一次。

- 每得到一个新的 OR 值，就立刻计算 `abs(k - OR)`，更新全局最小差。

**算法步骤**：

1. 初始化答案 `ans = +∞`，`prev = set()`（表示 `dp[i‑1]`）。
2. 从左到右遍历数组 `nums[i]`：
   - `cur = { nums[i] }`，先把只包含自身的子数组加入。
   - 对 `prev` 中的每个值 `v`，计算 `v | nums[i]` 并加入 `cur`。
   - 对 `cur` 中的每个值 `v`，更新 `ans = min(ans, abs(k - v))`。
   - 将 `cur` 赋给 `prev`，进入下一个位置。
3. 循环结束后，`ans` 即为答案。

> **类比**：把每个位置想象成一条流水线，左边的“已经加工好的”子数组（它们的 OR）进入当前节点后再加上当前的原料（`nums[i]`），得到新的产品。因为每次只会往更高的位“加料”，所以同一种产品最多出现 30 种不同的形态。

#### 代码（Python）

```python
from typing import List

def min_abs_diff_opt(nums: List[int], k: int) -> int:
    ans = float('inf')          # 全局最小差
    prev = set()                # dp[i-1]，保存上一个位置的所有 OR 值

    for num in nums:            # 从左到右遍历
        cur = {num}             # 只含自身的子数组
        # 把所有以 i-1 结尾的子数组再加上当前元素
        for v in prev:
            cur.add(v | num)    # OR 后可能产生新的值

        # 立即检查所有新产生的 OR 值
        for v in cur:
            diff = abs(k - v)
            if diff < ans:
                ans = diff

        # 为下一轮准备
        prev = cur

    return ans
```

> **关键注释**  
> - `cur = {num}`：单独的 `num` 本身也是一个合法子数组。  
> - `v | num`：把上一次的 OR 再和当前元素做一次 OR，得到以当前元素结尾的更长子数组。  
> - `prev = cur`：把本轮的结果保存，供下一轮使用。

#### 复杂度

- **时间复杂度**：`O(n * B)`，其中 `B ≤ 30` 是整数的最高位数。  
  对每个位置，我们最多遍历前一次集合中的 30 个值，整体大约是 `30n`，线性级别。  
  **对比**：比暴力的 `O(n²)` 快很多，即使 `n = 10⁵` 也能轻松跑完。

- **空间复杂度**：`O(B)`，即最多保存 30 个 OR 值的集合。  
  只和数组长度无关，常数级别的额外空间。

---

## 心得

- **核心技巧**：利用 **按位或的单调性** + **每个位置的 OR 集合大小上限**（≤ 30）进行状态压缩。  
- **适用的题型**：  
  1. “所有子数组的 OR/AND/异或集合” 类问题（例如 “子数组按位与的所有可能值”）。  
  2. 需要在 **子数组上做位运算** 并求最小/最大差值的优化题。  
  3. “子数组的所有不同值” 统计（如 “子数组的不同 XOR 值”）的类似思路。  
- **一句话总结解题钥匙**：**“向左扩展只能让 OR 位增多，因而每个右端点的不同 OR 值至多 30 个，利用集合动态转移即可线性求解”。**

---

## 反思

- **第一反应**：直接枚举所有子数组（暴力），因为题目描述最直观。  
- **最容易踩的坑**：  
  - 忘记 **去重**：同一个 OR 值可能由不同左端点得到，若不去重会导致集合膨胀，破坏 `≤30` 的性质。  
  - 忽视 **整数位数上限**：若把 `30` 当成常数写死，代码仍需解释为什么不超过 30。  
  - 边界条件：数组长度为 1 时，算法仍需正确返回 `abs(k - nums[0])`。  
- **下次类似题的第一步**：先思考**“该位运算的单调性或可逆性”**，判断是否可以用**状态压缩**（如集合、位掩码）把子数组的所有可能值限制在常数个，然后做 DP/滑动窗口。