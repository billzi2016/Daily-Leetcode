# #805. 拆分数组使平均值相等 / Split Array With Same Average

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/split-array-with-same-average/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
You should move each element of nums into one of the two arrays A and B such that A and B are non-empty, and average(A) == average(B).
Return true if it is possible to achieve that and false otherwise.
Note that for an array arr, average(arr) is the sum of all the elements of arr over the length of arr.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5,6,7,8]
Output: true
Explanation: We can split the array into [1,4,5,8] and [2,3,6,7], and both of them have an average of 4.5.
```

**Example 2:**

```
Input: nums = [3,1]
Output: false
```

**Constraints**

- 1 <= nums.length <= 30
- 0 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
你需要将 `nums` 中的每个元素分配到两个数组 **A** 和 **B** 中，使得 **A** 与 **B** 均非空，并且满足 `average(A) == average(B)`。如果能够实现返回 `true`，否则返回 `false`。  
其中，`average(arr)` 表示数组 `arr` 所有元素之和除以 `arr` 的长度。

## 示例

### 示例 1
**输入**: `nums = [1,2,3,4,5,6,7,8]`  
**输出**: `true`  
**解释**: 我们可以将数组拆分为 `[1,4,5,8]` 和 `[2,3,6,7]`，两者的平均值（average）均为 `4.5`。

### 示例 2
**输入**: `nums = [3,1]`  
**输出**: `false`

## 约束条件
- `1 <= nums.length <= 30`
- `0 <= nums[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把数组里的每个元素都**枚举**进哪一个子数组（A 或 B），  
等把所有元素都分完后，再检查两个子数组的平均值是否相等。  
在程序里，这等价于**遍历所有非空子集**（除去整个数组本身），  
因为只要找到了一个子集 `S`，把它当作 A，剩下的元素自然就是 B。

> **类比**：想象你有一堆水果，要把它们装进两个篮子，使得两个篮子里水果的“重量平均值”相同。最笨的办法就是把所有可能的装法（所有子集）都试一遍，看看有没有满足条件的。

**为什么正确**：  
若存在合法划分，则必有一个子集 `S`（对应 A）满足  

\[
\frac{\text{sum}(S)}{|S|} = \frac{\text{sum}(\text{nums})-\text{sum}(S)}{n-|S|}
\]

把等式两边同乘得到整数形式  

\[
\text{sum}(S)\times (n-|S|) = (\text{total}-\text{sum}(S))\times |S|
\]

只要我们枚举到这样一个 `S`，就可以直接返回 `True`。

**时间/空间复杂度**：  
- 枚举子集的数量是 `2^n`（每个元素有“进 A”或“进 B”两种选择），  
  其中 `n ≤ 30`，`2^30 ≈ 1.07 × 10⁹`，对计算机来说已经很慢了。  
- 对每个子集我们只需要 O(1) 的算术运算，所以总时间是 **O(2ⁿ)**。  
- 只用到常数级的额外空间 **O(1)**（不计递归栈或迭代变量）。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def splitArraySameAverage_bruteforce(nums: List[int]) -> bool:
    n = len(nums)
    total = sum(nums)

    # 子集的大小从 1 到 n-1（不能是空集，也不能是全体）
    for size in range(1, n):
        # 用 combinations 直接枚举所有 size 大小的子集
        for subset in combinations(nums, size):
            s = sum(subset)
            # 检查平均值相等的等价整数式
            #   s / size == (total - s) / (n - size)
            if s * (n - size) == (total - s) * size:
                return True
    return False
```

> **关键行注释**  
> - `for size in range(1, n):`：遍历子集的可能长度。  
> - `combinations(nums, size)`：枚举所有恰好 `size` 个元素的子集。  
> - `if s * (n - size) == (total - s) * size:`：利用上面的整数等式判断是否满足平均相等。

#### 复杂度  

- **时间复杂度**：`O(2ⁿ)`——每增加一个元素，可能的子集数翻倍。  
  用大白话说，就是如果数组有 30 个数，最坏情况下要检查 **十几亿** 种分配方式，几乎不可能在一秒内算完。  
- **空间复杂度**：`O(1)`——只用了几个整数变量和循环计数器，和输入规模无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有子集**。  
我们需要一种方式，只“记住”哪些**子集和**是可能出现的，而不是把每个子集都列出来。  

---

#### 2.1 关键数学观察  

设 `total = sum(nums)`，数组长度为 `n`。  
若存在合法划分，则一定可以找到一个非空子集 `S`，大小为 `k (1 ≤ k ≤ n‑1)`，满足  

\[
\frac{\text{sum}(S)}{k} = \frac{total}{n}
\]

即  

\[
\text{sum}(S) = \frac{total \times k}{n}
\]

右边必须是整数，否则不可能出现这样的子集。  
因此 **只要找到了某个 k 使得 total * k 能被 n 整除，并且存在大小为 k、和为 total*k/n 的子集**，答案就是 `True`。

另外，若我们已经找到了大小为 `k` 的子集 `S`，则剩下的 `n‑k` 个元素自然形成子集 B，平均值必相等。  
因为 `k` 与 `n‑k` 对称，只需要检查 `k ≤ n/2`（更小的一边），即可省掉一半的搜索。

---

#### 2.2 动态规划（DP）求“能否得到某个和”  

我们把问题转化为**“在前 i 个数中，能否恰好选出 k 个数，使它们的和为 s”**。  
这正是经典的 **子集和 DP**，不过这里还要额外记录选了多少个数。

实现方式：  
- 建立一个长度为 `n+1` 的列表 `dp`，其中 `dp[k]` 是一个 **集合**，记录所有可以由恰好 `k` 个数得到的和。  
- 初始时 `dp[0] = {0}`（选 0 个数和为 0）。  
- 遍历数组中的每个数字 `num`，从大到小更新 `dp`（防止同一个数被多次使用）：

```
for num in nums:
    for k from current_max down to 1:
        for each previous_sum in dp[k-1]:
            dp[k].add(previous_sum + num)
```

这样，遍历完所有数字后，`dp[k]` 就包含了所有可能的 `k` 元子集和。

随后，只要检查 **是否存在** `k (1 ≤ k ≤ n/2)` 满足 `total * k % n == 0`，并且目标和 `target = total * k // n` 落在 `dp[k]` 中，即可返回 `True`。

> **类比**：把 `dp[k]` 想象成一本“记账本”。  
> - 第 `k` 页记录“用 k 张卡片能凑出哪些金额”。  
> - 每加入一张新卡片（数组中的一个数），我们把它的金额加到所有已有的记账本上，形成新的可能金额。  
> - 最后只要在某一页里看到我们想要的金额，就说明可以用恰好 k 张卡片凑出它。

---

#### 2.3 复杂度分析  

- **时间**：外层遍历 `n`（最多 30）个数，内层遍历 `k`（最多 `n/2`），而每个 `dp[k]` 最多保存 **所有可能的和**。和的上限是 `total ≤ 30 × 10⁴ = 300000`。  
  实际上每加入一个数，只会把已有的和 “平移” 一次，整体操作数约为 `O(n * total)`，在本题限制下约为 `9·10⁶`，非常快。  
- **空间**：我们保存 `n+1` 个集合，所有集合里存的和总数同样不超过 `total * n` 的数量级，实际约 `O(n * total)`。对 30·300000 ≈ 9 × 10⁶ 的整数而言，内存也在可接受范围（约 70 MB 左右）。  

相比暴力的 `2ⁿ`，DP 把指数级下降到 **线性乘以和的大小**，在本题的数据范围内是最优的可行方案。

#### 代码（Python）

```python
from typing import List

def splitArraySameAverage(nums: List[int]) -> bool:
    n = len(nums)
    total = sum(nums)

    # 如果所有数相同，直接返回 True（因为任意划分平均值相等）
    # 但这里的 DP 也会得到 True，下面的代码已经涵盖这种情况。
    
    # 预处理：如果不存在满足 total * k % n == 0 的 k，直接返回 False
    possible_ks = [k for k in range(1, n // 2 + 1) if (total * k) % n == 0]
    if not possible_ks:
        return False

    # dp[k] = set of achievable sums using exactly k numbers
    dp = [set() for _ in range(n + 1)]
    dp[0].add(0)                     # 选 0 个数，和为 0

    for num in nums:
        # 必须倒序遍历 k，防止同一个元素被重复计入同一子集
        for k in range(n, 0, -1):
            # 把当前数加入到所有已有的 “k-1 个数的和” 中
            for prev_sum in dp[k - 1]:
                dp[k].add(prev_sum + num)

    # 检查每一个可能的子集大小 k
    for k in possible_ks:
        target = total * k // n      # 必须是整数，前面已经保证可整除
        if target in dp[k]:          # 如果恰好可以用 k 个数凑出 target
            return True

    return False
```

> **关键行注释**  
> - `possible_ks = [...]`：先筛掉那些根本不可能满足整数目标和的子集大小，省掉后面的 DP 检查。  
> - `for k in range(n, 0, -1):`：倒序是 DP 的常用技巧，确保每个数只使用一次。  
> - `if target in dp[k]:`：只要出现一次即可，立刻返回 `True`。

---

#### 复杂度  

- **时间复杂度**：`O(n * total)`，即 `O(30 * 300000) ≈ 9·10⁶` 步。  
  用大白话说，就是**遍历 30 次，每次把所有可能的“金额”往后推一次**，整体大约几百万次操作，几乎在一瞬间完成。  
- **空间复杂度**：`O(n * total)`，同样约几百万个整数，约 70 MB 左右，符合 LeetCode 的内存限制。  
  与暴力的 `O(1)` 空间相比略高，但时间优势巨大，实际是最优选择。

---

## 心得  

- **核心技巧**：把“平均相等”转化为“子集和等于特定值”，然后用 **按元素个数分层的子集和 DP** 判断是否可达。  
- **适用题型**：  
  1. **“分割数组使两部分和相等”**（如 Partition Equal Subset Sum）  
  2. **“找出恰好 k 个数的子集和为 target”**（如 Combination Sum IV 的变形）  
  3. **“按元素个数限定的背包问题”**（如 0/1 背包带容量限制的变体）  
- **一句话总结解题钥匙**：  
  *把平均值问题转化为整数子集和问题，利用“按选取个数分层的 DP”快速判断可行性。*

---

## 反思  

- **第一反应**：直接想到枚举所有子集，写出暴力解法验证思路。  
- **最容易踩的坑**：  
  - 忘记排除空集和完整集合（两边必须非空）。  
  - 没检查 `total * k % n == 0`，导致后面 DP 查找的目标和不是整数，浪费时间。  
  - DP 更新时正序遍历导致同一个元素被重复使用，必须倒序。  
- **下次遇到同类题**：第一步先**把等式化为整数形式**，看是否能通过 “子集和 + 选取个数” 的 DP 来降低指数爆炸。这样思路更清晰，代码也更易于调试。