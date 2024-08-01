# #2809. 使数组和至多为 x 的最少时间 / Minimum Time to Make Array Sum At Most x

> 难度：困难 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-make-array-sum-at-most-x/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2 of equal length. Every second, for all indices 0 <= i < nums1.length, value of nums1[i] is incremented by nums2[i]. After this is done, you can do the following operation:
You are also given an integer x.
Return the minimum time in which you can make the sum of all elements of nums1 to be less than or equal to x, or -1 if this is not possible.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3], nums2 = [1,2,3], x = 4
Output: 3
Explanation: 
For the 1st second, we apply the operation on i = 0. Therefore nums1 = [0,2+2,3+3] = [0,4,6]. 
For the 2nd second, we apply the operation on i = 1. Therefore nums1 = [0+1,0,6+3] = [1,0,9]. 
For the 3rd second, we apply the operation on i = 2. Therefore nums1 = [1+1,0+2,0] = [2,2,0]. 
Now sum of nums1 = 4. It can be shown that these operations are optimal, so we return 3.
```

**Example 2:**

```
Input: nums1 = [1,2,3], nums2 = [3,3,3], x = 4
Output: -1
Explanation: It can be shown that the sum of nums1 will always be greater than x, no matter which operations are performed.
```

**Constraints**

- 1 <= nums1.length <= 103
- 1 <= nums1[i] <= 103
- 0 <= nums2[i] <= 103
- nums1.length == nums2.length
- 0 <= x <= 106

---

## 题目（中文翻译）

给定两个等长的 **0 索引** 整数数组 `nums1` 和 `nums2`。  
每秒钟，**对所有下标** `0 ≤ i < nums1.length`，执行 `nums1[i] += nums2[i]`（即 `nums1[i]` 增加 `nums2[i]`）。  
在上述增量完成后，你可以再执行一次操作：

* 选择任意下标 `i`，将 `nums1[i]` **设为 0**。

另外，给定一个整数 `x`。求最小的时间（秒数），使得 `nums1` 中所有元素的和 **不大于** `x`。如果无论怎样操作都无法使和 ≤ `x`，返回 `-1`。

---

## 示例

### 示例 1
**输入**  
```text
nums1 = [1,2,3], nums2 = [1,2,3], x = 4
```
**输出**  
```text
3
```
**解释**  
- 第 1 秒，先全部增量得到 `[2,4,6]`，随后对下标 `0` 执行操作，将其设为 `0` → `[0,4,6]`。  
- 第 2 秒，增量后得到 `[1,6,9]`，对下标 `1` 设为 `0` → `[1,0,9]`。  
- 第 3 秒，增量后得到 `[2,2,12]`，对下标 `2` 设为 `0` → `[2,2,0]`。  

此时 `nums1` 的和为 `2 + 2 + 0 = 4 ≤ x`，共用了 **3 秒**，且可以证明这是最小的时间。

### 示例 2
**输入**  
```text
nums1 = [1,2,3], nums2 = [3,3,3], x = 4
```
**输出**  
```text
-1
```
**解释**  
无论怎样选择下标进行置零操作，`nums1` 的和始终大于 `x`，因此返回 `-1`。

---

## 约束

- `1 ≤ nums1.length ≤ 10^3`
- `1 ≤ nums1[i] ≤ 10^3`
- `0 ≤ nums2[i] ≤ 10^3`
- `nums1.length == nums2.length`
- `0 ≤ x ≤ 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举所有可能的操作顺序**，然后找出第一个让 `sum(nums1) ≤ x` 的时刻。  

- 每一秒我们可以把任意下标 `i` 的 `nums1[i]` 设为 `0`（相当于“把这个位置的数清零”），随后所有 `nums1` 再统一 **加上对应的 `nums2`**。  
- 把「把第 `i` 个位置清零」看成一次「任务」，整个过程就是在 **n** 个任务中挑选若干个并安排执行顺序。  

> 类比：想象一排书架上有若干本书（`nums1`），每本书每天会自动增加若干页（`nums2`）。我们可以一次把某本书的页数归零，然后再让所有书继续每天增长。目标是让所有书的总页数在最短时间内不超过 `x`。

**为什么暴力一定能得到答案**  
因为我们穷举了 **所有** 可能的清零集合以及所有可能的执行顺序，必然能覆盖最优方案。  

**为什么会超时**  
- `n ≤ 1000`，如果我们直接枚举每本书是否被清零，就有 `2ⁿ` 种可能，已经远远超出计算能力。  
- 即使把「是否清零」固定下来，还需要考虑 **清零的顺序**（最多 `n!` 种），更是不可行。  

#### 代码（Python）  
下面的实现只是为了演示「暴力」的思路，**不适合在实际提交中使用**，因为会在最小的测试用例上就超时。

```python
from itertools import combinations, permutations

def min_time_bruteforce(nums1, nums2, x):
    n = len(nums1)
    total0 = sum(nums1)                     # 初始总和
    inc = sum(nums2)                        # 每秒整体增加的量

    # 枚举清零的个数 t（0~n）
    for t in range(n + 1):
        # 枚举要清零的下标集合（大小为 t）
        for idxs in combinations(range(n), t):
            # 只考虑按 nums2 升序的执行顺序（因为后面会证明最优一定是这样）
            order = sorted(idxs, key=lambda i: nums2[i])
            # 计算在第 t 秒结束时的总和
            cur = total0 + inc * t          # 所有元素在 t 秒后自然增长的部分
            # 逐个把被清零的元素在它们各自的清零时刻减掉对应的累计增长
            for k, i in enumerate(order, 1):   # k 是该元素被清零的秒数（1-indexed）
                cur -= nums1[i] + nums2[i] * k
            if cur <= x:
                return t
    return -1
```

> 关键行解释  
> - `combinations(range(n), t)`：挑选 `t` 本书要清零的下标。  
> - `sorted(idxs, key=lambda i: nums2[i])`：把要清零的书按增长速度 `nums2` 从小到大排好顺序（后面会证明这是最优顺序）。  
> - `cur -= nums1[i] + nums2[i] * k`：第 `k` 秒把第 `i` 本书清零时，实际上我们把它之前累计的值（初始值 + 已增长的 `k` 次）从总和中减掉。

#### 复杂度  

- **时间复杂度**：`O( Σ_{t=0}^{n} C(n,t) * t! )`，即 **指数级**（`2ⁿ` 甚至更高），在最坏情况下几乎不可计算。  
- **空间复杂度**：`O(n)`，只用了若干临时列表保存下标集合。

> 大白话：`O(2ⁿ)` 就像把所有可能的钥匙都试一遍，钥匙数量翻倍，时间也翻倍，根本不可能在几秒内把 1000 把钥匙全试完。

---

### 2. 最优解  

#### 思路  

从暴力解我们已经知道两个关键事实（提示里已经给出）：

1. **每个位置至多清零一次**。如果同一个位置被清了两次，完全可以把前一次去掉，后面的操作整体左移一秒，得到更好的或等价的方案。  
2. **清零的顺序一定是 `nums2` 从小到大**。因为增长速度大的位置越晚清零，累计的增长就越多，能够削掉更多的“额外”值。

基于这两个结论，我们可以把问题转化为：

> 在 **已经按 `nums2` 升序排好** 的序列中，挑选 `t` 个位置（`t` 为我们要尝试的时间），并决定它们各自被清零的秒数（恰好是 `1,2,…,t`），使得**被削掉的总值**最大。  

如果在 `t` 秒后削掉的总值记为 `reduce(t)`，则此时数组的总和为  

```
sum(nums1) + t * sum(nums2) - reduce(t)
```

我们只要找到最小的 `t` 使得上式 ≤ `x` 即可。

---

#### 动态规划构造  

设数组已经按照 `nums2` **非递减** 排序（如果相等，`nums1` 也一起随动）。记  

- `n = len(nums1)`  
- `a[i] = nums1[i]`（排好序后的）  
- `b[i] = nums2[i]`（排好序后的）  

我们用 `dp[i][j]` 表示：**只考虑前 `i` 个元素，恰好进行 `j` 次清零操作时，能够削掉的最大总值**。  

- **初始化**：`dp[i][0] = 0`（不做任何清零，削掉的值为 0）。  
- **状态转移**：对第 `i`（1‑based）个元素，有两种选择  
  1. **不选**它：`dp[i-1][j]`  
  2. **选**它作为第 `j` 次清零（因为已经有 `j-1` 次清零在前面），此时它在第 `j` 秒被清零，削掉的值为 `a[i-1] + b[i-1] * j`（初始值 + 经过 `j` 次增长）。  
     
     因此  
     `dp[i-1][j-1] + a[i-1] + b[i-1] * j`  

  取两者最大：

```
dp[i][j] = max( dp[i-1][j],
                dp[i-1][j-1] + a[i-1] + b[i-1] * j )
```

- **边界**：`dp[0][j] = -∞`（没有元素却要清零是不可能的），实际实现时只在 `j ≤ i` 时计算。

最终我们得到 `dp[n][t]`，即在前 `n` 个元素中恰好做 `t` 次清零能削掉的最大值。

> 为什么这个 DP 正确？  
> - 由于我们已经固定了清零顺序（`b` 从小到大），第 `j` 次清零一定对应的是 **已经选的第 `j` 小的 `b`**。  
> - DP 按照“前缀 + 选多少”逐步构造，确保每个子问题的解都是最优的，进而得到整体最优。

---

#### 求答案  

遍历所有可能的 `t = 0 … n`，检查：

```
current_sum = sum(nums1) + t * sum(nums2) - dp[n][t]
if current_sum <= x:
    answer = t   # 第一个满足条件的 t 即为最小时间
```

如果所有 `t` 都不满足，则返回 `-1`。

---

#### 代码（Python）  

```python
from typing import List

def minimum_time(nums1: List[int], nums2: List[int], x: int) -> int:
    n = len(nums1)

    # 1. 按 nums2 升序排序，nums1 随之一起移动
    paired = sorted(zip(nums2, nums1))          # (b, a) 对
    b = [p[0] for p in paired]                  # 排好序的 nums2
    a = [p[1] for p in paired]                  # 对应的 nums1

    total_a = sum(a)            # sum(nums1)（已排序但求和不变）
    total_b = sum(b)            # sum(nums2)

    # 2. DP: 只保留上一行，空间压缩到 O(n)
    # dp[j] 表示在处理到当前 i 时，恰好用了 j 次清零的最大削减值
    dp = [-10**18] * (n + 1)    # -∞ 表示不可达
    dp[0] = 0                   # 0 次清零削掉 0

    for i in range(1, n + 1):
        # 必须倒序遍历 j，防止本轮更新时被后面的状态覆盖
        for j in range(i, 0, -1):
            # 选第 i 个元素作为第 j 次清零的贡献
            take = dp[j - 1] + a[i - 1] + b[i - 1] * j
            # 不选则保持 dp[j]，取较大者
            if take > dp[j]:
                dp[j] = take
        # dp[0] 保持不变（仍为 0）

    # 3. 找最小的 t 使得 sum <= x
    for t in range(n + 1):
        # dp[t] 可能仍为 -∞（比如 t > i），此时跳过
        if dp[t] < 0:
            continue
        cur_sum = total_a + t * total_b - dp[t]
        if cur_sum <= x:
            return t
    return -1
```

> 关键行中文注释  
> - `paired = sorted(zip(nums2, nums1))`：把 `nums2` 当作“字典的关键字”，把对应的 `nums1` 搬进去一起排序，类似把词典按拼音排好顺序。  
> - `dp = [-10**18] * (n + 1)`：用一个很小的负数表示「不可达」的状态。  
> - `for j in range(i, 0, -1):`：倒序更新保证本轮的 `dp[j-1]` 仍是上一轮的值。  
> - `take = dp[j - 1] + a[i - 1] + b[i - 1] * j`：如果把第 `i` 个位置作为第 `j` 次清零，它能削掉的值等于「之前已经削掉的」加上「这一次清零能去掉的」 (`a[i-1]` 是原始值，`b[i-1]*j` 是已经增长的部分)。  
> - `cur_sum = total_a + t * total_b - dp[t]`：在第 `t` 秒结束时的总和 = 初始总和 + `t` 秒的整体增长 - 已经削掉的最大值。

---

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 排序 `O(n log n)`，在 `n ≤ 1000` 时几乎可以忽略。  
  - 双层循环：外层 `i` 遍历 `1…n`，内层 `j` 最多遍历 `i`，总次数约为 `n·(n+1)/2 ≈ n²/2`。  
  - 大白话：如果 `n = 1000`，大约要做 500 000 次简单的加减比较，电脑在毫秒级就能完成。

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n+1` 的一维 DP 数组，另外还有几个长度 `n` 的临时数组。  

> 与暴力解对比：暴力是指数级，最优解把时间从「天文数字」降到了「几千次」，是可以接受的。

---

## 心得  

- **核心技巧**：**排序 + 动态规划**。先把增长最快的元素排在后面（因为它们越晚清零越有价值），再用 DP 计算在给定次数的清零操作下能削掉的最大总值。  
- **适用的题型**  
  1. 需要在**有限次数**的操作中**最大化收益**，且每个元素的收益随操作次数呈线性（或可累加）增长，如「选择 k 项使加权和最大」类问题。  
  2. **先排序后 DP** 的典型例子还有「分割数组的最大和」或「背包问题的顺序约束」等。  
- **一句话总结解题钥匙**：*把所有元素按照增长速度从小到大排好序，利用 DP 计算在第 `t` 次清零时能削掉的最大值，随后遍历 `t` 找到最小可行时间*。

---

## 反思  

- **第一反应**：看到「每秒所有元素都会增加」以及「可以把某个元素归零」的描述，我首先想到「模拟」或「搜索所有可能的清零顺序」——这就是暴力解的思路。  
- **最容易踩的坑**  
  1. **忽略“每个位置最多清零一次”**：若不证明这点，可能会把 DP 状态写成 `dp[i][j][k]`（是否已经清零），导致状态爆炸。  
  2. **忘记排序**：若直接在原数组上做 DP，`dp[i][j]` 的转移式不再成立，因为第 `j` 次清零对应的 `nums2` 不一定是第 `j` 小的。  
  3. **边界条件**：`dp[t]` 可能为负无穷（不可达），直接使用会导致错误的 `cur_sum`。需要在判断时跳过这些状态。  
- **下次遇到类似题目**：**第一步**先思考是否可以通过排序把“顺序约束”固定下来；**第二步**考虑用 DP 记录「前 i 项、用了多少次操作」的最优值。这样往往能把指数级搜索压缩到多项式时间。