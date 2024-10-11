# #2897. 对数组进行操作以最大化平方和 / Apply Operations on Array to Maximize Sum of Squares

> 难度：困难 · 标签：Array、Hash Table、Greedy、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/apply-operations-on-array-to-maximize-sum-of-squares/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and a positive integer k.
You can do the following operation on the array any number of times:
You have to choose k elements from the final array and calculate the sum of their squares.
Return the maximum sum of squares you can achieve.
Since the answer can be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [2,6,5,8], k = 2
Output: 261
Explanation: We can do the following operations on the array:
- Choose i = 0 and j = 3, then change nums[0] to (2 AND 8) = 0 and nums[3] to (2 OR 8) = 10. The resulting array is nums = [0,6,5,10].
- Choose i = 2 and j = 3, then change nums[2] to (5 AND 10) = 0 and nums[3] to (5 OR 10) = 15. The resulting array is nums = [0,6,0,15].
We can choose the elements 15 and 6 from the final array. The sum of squares is 152 + 62 = 261.
It can be shown that this is the maximum value we can get.
```

**Example 2:**

```
Input: nums = [4,5,4,7], k = 3
Output: 90
Explanation: We do not need to apply any operations.
We can choose the elements 7, 5, and 4 with a sum of squares: 72 + 52 + 42 = 90.
It can be shown that this is the maximum value we can get.
```

**Constraints**

- 1 <= k <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组（integer array）`nums` 和一个正整数 `k`。  
你可以对数组执行以下操作任意次数：

- 任选两个不同下标 `i`、`j`（`i ≠ j`），将 `nums[i]` 改为 `nums[i] AND nums[j]`，将 `nums[j]` 改为 `nums[i] OR nums[j]`。其中 **AND** 表示按位与（bitwise AND），**OR** 表示按位或（bitwise OR）。

在完成任意次数的操作后，你需要从最终数组中选择 `k` 个元素，计算它们的平方和（sum of squares），并返回能够得到的最大平方和。由于答案可能非常大，请返回 **模** `10^9 + 7`（即 `109 + 7`）后的结果。

### 示例

#### 示例 1
```
Input: nums = [2,6,5,8], k = 2
Output: 261
Explanation: 我们可以对数组执行以下操作：
- 选择 i = 0, j = 3，将 nums[0] 改为 (2 AND 8) = 0，nums[3] 改为 (2 OR 8) = 10，得到数组 [0,6,5,10]。
- 再选择 i = 2, j = 3，将 nums[2] 改为 (5 AND 10) = 0，nums[3] 改为 (5 OR 10) = 15，得到数组 [0,6,0,15]。
此时选取最大的两个元素 15 与 6，平方和为 15² + 6² = 225 + 36 = 261。
```

#### 示例 2
```
Input: nums = [4,5,4,7], k = 3
Output: 90
Explanation: 不需要进行任何操作。直接选取元素 7、5、4，平方和为 7² + 5² + 4² = 49 + 25 + 16 = 90，这是能够得到的最大值。
```

### 约束条件
- `1 <= k <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把**所有可能的操作**都枚举一遍，然后在每一次得到的数组里挑出 `k` 个元素，算它们的平方和，取最大值。  

- **枚举操作**：每一次操作要从数组中任选两个下标 `i`、`j`（`i ≠ j`），把  
  ```text
  nums[i] = nums[i] & nums[j]
  nums[j] = nums[i] | nums[j]          （这里的 “nums[i]” 指的是 **原来的** nums[i]）
  ```  
  这样就得到一个新的数组。  
- **挑选 k 个元素**：把数组的所有 `C(n, k)` 种子集都遍历一遍，计算每个子集的平方和。  

**为什么这个方法能得到正确答案**  
因为我们把**所有**合法的操作序列都穷举完了，最后再把**所有**可能的 `k` 元素组合都算了一遍，必然会覆盖得到最大平方和的那一种情况。

**时间/空间复杂度分析**  
- 枚举一次操作有 `O(n²)` 种（任选两下标）。  
- 再把每一种操作后的数组里挑 `k` 个的组合数是 `C(n, k)`，在最坏情况下接近 `O(n^k)`（指数级）。  
- 甚至只考虑一次操作已经是 `O(n²)`，而我们还要把操作次数 **任意次**（可以是 0、1、2…），所以整体的时间复杂度是 **指数级**，根本不可接受。  

大白话解释：  
- `O(n²)` 就像让你把班里每两个人都拍一张合照，人数多的话照片数会爆炸。  
- `O(n^k)` 更糟，等于是让你把班里每 `k` 个人都排成一队排队，队形数会多到天文数字。  

#### 代码（Python）  

```python
# 暴力解（仅作思路演示，实际会超时）
import itertools
from copy import deepcopy

def brute(nums, k):
    n = len(nums)
    best = 0
    # 为了演示，这里只枚举 **一次** 操作的所有可能（实际题目可以操作任意次）
    for i in range(n):
        for j in range(i + 1, n):
            a, b = nums[i], nums[j]               # 记住原来的值
            new_nums = deepcopy(nums)
            new_nums[i] = a & b                    # AND
            new_nums[j] = a | b                    # OR

            # 枚举所有挑 k 个元素的方式
            for combo in itertools.combinations(new_nums, k):
                s = sum(x * x for x in combo)      # 平方和
                best = max(best, s)

    # 也要考虑“什么都不做”的情况
    for combo in itertools.combinations(nums, k):
        best = max(best, sum(x * x for x in combo))

    return best % (10**9 + 7)

# 示例（仅用于验证思路，实际大数据会直接卡死）
print(brute([2, 6, 5, 8], 2))
```

> **注意**：上述代码只能跑极小规模的数据（比如 `n ≤ 6`），在正式测试里会因为时间爆炸而 **超时**。

#### 复杂度  

- **时间复杂度**：`O(n² * C(n, k))` → 甚至更糟，因为我们可以进行多次操作，实际是指数级。  
  - **含义**：随着数组长度稍微大一点，运行时间就会从几秒飙升到几天、几年不等。  
- **空间复杂度**：`O(n)`（复制数组需要的临时空间），相对较小。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的难点不是挑 `k` 个数，而是如何把位（bit）搬到合适的数上**。  
观察一次操作的本质：

| 原来 `i` | 原来 `j` | `i` 变成 | `j` 变成 |
|----------|----------|----------|----------|
| 0 / 1    | 0 / 1    | `i & j`  | `i | j`  |

- 对于某一位 `b`（比如第 3 位），如果 **只有一个** 数的该位是 `1`，操作后 `1` 会 **移动** 到另一个数上（`i` 失去 `1`，`j` 获得 `1`）。  
- 如果两个数的该位都是 `1`，两个数都保留 `1`，位数不变。  
- **结论**：**每一位的 `1` 的总个数是保持不变的**，只会在不同的元素之间转移。  

这意味着我们可以把每一位的 `1` 随意分配到数组的任意位置，只要不超过该位原本的出现次数。  
于是问题可以转化为：

> 给定每一位 `b` 的出现次数 `cnt[b]`（`0 ≤ b ≤ 30`），把这些位分配到 `k` 个数里，使这 `k` 个数的平方和最大。

---

#### 为什么要“把位集中到少数几个数”  

平方函数是 **凸函数**，即数越大，增加同样的值会带来更大的增量。  
把位 `v = 2^b` 加到已经很大的数 `x` 上，增量是  
```
(x + v)² - x² = 2·x·v + v²
```
其中 `2·x·v` 与 `x` 成正比，`x` 越大，增量越大。  
因此，为了让总增量最大，我们应当 **把位尽可能多地塞进已经大的数里**，而不是平均分配。  

换句话说，**把位集中到前 few（最多 k）个数**，其余数可以全部变成 `0`（不影响平方和），就能得到最大值。

---

#### 构造最优数组的步骤  

1. **统计每一位的出现次数**  
   - 对每个 `num`，遍历二进制的每一位（最多到第 30 位，因为 `num ≤ 10⁹ < 2³⁰`），如果该位是 `1`，`cnt[b] += 1`。  
   - 这一步相当于把“位的分布表”记在一本“小字典”里，`cnt` 就像字典的 **key**（位）对应的 **value**（出现次数）。  

2. **把位分配给前 k 个数**  
   - 创建一个长度为 `k` 的数组 `big = [0] * k`。  
   - 对每一位 `b`（从低位到高位都可以，顺序不影响结果），把它的 `cnt[b]` 次出现分别加到 `big[0]、big[1] … big[cnt[b]-1]` 上。  
   - 也就是说，**出现次数越多的位，会出现在前面更多的数里**，自然把位“堆”到前几个数。  

3. **计算答案**  
   - 对 `big` 中的每个数 `x`，累加 `x²`，并在每一步取模 `MOD = 10⁹ + 7` 防止溢出。  

---

#### 代码（Python）  

```python
MOD = 10**9 + 7
MAX_BIT = 31                 # 因为 2^30 > 1e9，遍历到 30 位即可

def maxSumSquare(nums, k):
    # 1️⃣ 统计每一位的出现次数
    cnt = [0] * MAX_BIT
    for num in nums:
        b = 0
        while num:
            if num & 1:          # 当前最低位是 1
                cnt[b] += 1
            num >>= 1
            b += 1

    # 2️⃣ 把位尽可能集中到前 k 个数
    big = [0] * k               # 前 k 个“超级大数”，其余可以视作 0
    for b in range(MAX_BIT):
        bit_val = 1 << b        # 该位对应的数值，例如第 3 位是 8
        for i in range(cnt[b]):    # 把这 cnt[b] 个 1 分配给前 cnt[b] 个数
            if i >= k:              # 超过 k 个的位只能给 0（不影响最大值）
                break
            big[i] += bit_val

    # 3️⃣ 计算平方和并取模
    ans = 0
    for x in big:
        ans = (ans + (x * x) % MOD) % MOD
    return ans
```

**代码解释（每行中文注释）**  

| 行号 | 代码 | 中文说明 |
|------|------|----------|
| 1    | `MOD = 10**9 + 7` | 题目要求的取模常数 |
| 2    | `MAX_BIT = 31` | 因为 `nums[i] ≤ 10⁹`，最高只会到第 30 位（从 0 开始） |
| 5‑10 | 统计每一位出现次数 | 用 `cnt[b]` 记录第 `b` 位上 `1` 的总个数，遍历每个数的二进制位 |
| 13   | `big = [0] * k` | 初始化前 `k` 个要“收集位”的大数，初始都是 0 |
| 14‑19| 把位分配到 `big` | 对每一位 `b`，把它的 `cnt[b]` 个 `1` 加到 `big[0] … big[cnt[b]-1]` 上；如果 `cnt[b] > k`，只需要前 `k` 个，因为其余的 `1` 放在不选的数里也不会提升答案 |
| 22‑26| 计算平方和并取模 | 逐个把 `big[i]²` 加到答案里，途中取模防止整数爆炸 |

#### 复杂度  

- **时间复杂度**：`O(n * MAX_BIT + k * MAX_BIT)`  
  - 统计位：`n` 个数 × 最多 31 位 → `≈ 3·10⁶` 次操作（对 `10⁵` 长度的数组完全可以接受）。  
  - 位分配：每个位最多遍历 `cnt[b] ≤ n` 次，总次数等于所有 `1` 的总数，同样是 `O(n * MAX_BIT)`。  
  - **含义**：即使 `n = 100,000`，程序也只会跑几百万次基本运算，毫秒级完成。  

- **空间复杂度**：`O(k + MAX_BIT)`  
  - `big` 数组需要 `k` 个整数，`cnt` 只需要 31 个计数。  
  - **含义**：使用的额外内存与输入规模线性相关，最多约 `100,000` 个整数（≈ 0.8 MB），非常小。  

与暴力解相比：  
- 暴力解是指数级（根本不可用），最优解是线性/准线性，能轻松跑满 10⁵ 规模的测试数据。

---

## 心得  

- **核心技巧**：把位（bit）视作可自由搬运的“资源”，统计每一位出现的次数，然后把这些资源**尽可能集中**到少数几个数上，以利用平方函数的凸性。  
- **适用的题型**  
  1. “把位或数值重新分配，使某个函数值最大”——如 *Maximum Sum of Squares After Bit Operations*（本题）。  
  2. “把数组元素合并后求最大乘积/平方和”——如 *Maximum Sum of Products After Merging*。  
  3. “位计数后贪心分配”——如 *Maximum XOR Sum of Two Numbers*（位计数后配对）。  
- **一句话总结解题钥匙**：**位计数 + 把位集中到前 k 个数**，利用平方的凸性获得最大和。

---

## 反思  

- **第一反应**：看到 “AND / OR” 操作，就想直接模拟所有可能的交换，结果发现搜索空间太大。  
- **最容易踩的坑**  
  1. **误以为必须模拟操作顺序**——其实位的总数不变，只要懂位的转移本质，就能直接构造最优数组。  
  2. **忘记取模**——平方和可能超过 64 位整数范围，必须在累加时及时 `% MOD`。  
  3. **位数上限写错**——`nums[i] ≤ 10⁹`，最高位是第 30 位（0‑based），所以循环要到 31（包括 0）。  
- **下次遇到同类题**：第一步立刻检查“操作是否保持某种不变量（如位计数、总和、奇偶性）”，再围绕不变量设计 **贪心/计数** 的构造方案，而不是盲目搜索。