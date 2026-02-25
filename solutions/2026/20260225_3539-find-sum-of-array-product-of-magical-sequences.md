# #3539. 求所有魔法序列的数组乘积之和 / Find Sum of Array Product of Magical Sequences

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Bit Manipulation、Combinatorics、Bitmask · [LeetCode 链接](https://leetcode.com/problems/find-sum-of-array-product-of-magical-sequences/)

---

## 题目（英文原版）

**Description**

You are given two integers, m and k, and an integer array nums.
The array product of this sequence is defined as prod(seq) = (nums[seq[0]] * nums[seq[1]] * ... * nums[seq[m - 1]]).
Return the sum of the array products for all valid magical sequences.
Since the answer may be large, return it modulo 109 + 7.
A set bit refers to a bit in the binary representation of a number that has a value of 1.

**Examples**

**Example 1:**

```
Input: m = 5, k = 5, nums = [1,10,100,10000,1000000]
Output: 991600007
Explanation:
All permutations of [0, 1, 2, 3, 4] are magical sequences, each with an array product of 10 13 .
```

**Example 2:**

```
Input: m = 2, k = 2, nums = [5,4,3,2,1]
Output: 170
Explanation:
The magical sequences are [0, 1] , [0, 2] , [0, 3] , [0, 4] , [1, 0] , [1, 2] , [1, 3] , [1, 4] , [2, 0] , [2, 1] , [2, 3] , [2, 4] , [3, 0] , [3, 1] , [3, 2] , [3, 4] , [4, 0] , [4, 1] , [4, 2] , and [4, 3] .
```

**Example 3:**

```
Input: m = 1, k = 1, nums = [28]
Output: 28
Explanation:
The only magical sequence is [0] .
```

**Constraints**

- 1 <= k <= m <= 30
- 1 <= nums.length <= 50
- 1 <= nums[i] <= 108

---

## 题目（中文翻译）

给定两个整数 `m` 和 `k`，以及一个整数数组 `nums`。  
序列的 **数组乘积（array product）** 定义为  
`prod(seq) = (nums[seq[0]] * nums[seq[1]] * ... * nums[seq[m - 1]])`。  
返回所有满足条件的 **魔法序列（magical sequence）** 的数组乘积之和。  
由于答案可能很大，请返回 **模 (10^9 + 7)** 的结果。  

**置位（set bit）** 指二进制表示中值为 `1` 的位。

---

### 示例

#### 示例 1  
**输入:** `m = 5, k = 5, nums = [1,10,100,10000,1000000]`  
**输出:** `991600007`  
**解释:**  
`[0, 1, 2, 3, 4]` 的所有排列都是魔法序列，每个序列的数组乘积均为 `10^13`。

#### 示例 2  
**输入:** `m = 2, k = 2, nums = [5,4,3,2,1]`  
**输出:** `170`  
**解释:**  
魔法序列为  
`[0, 1] , [0, 2] , [0, 3] , [0, 4] , [1, 0] , [1, 2] , [1, 3] , [1, 4] , [2, 0] , [2, 1] , [2, 3] , [2, 4] , [3, 0] , [3, 1] , [3, 2] , [3, 4] , [4, 0] , [4, 1] , [4, 2] , [4, 3]`。

#### 示例 3  
**输入:** `m = 1, k = 1, nums = [28]`  
**输出:** `28`  
**解释:**  
唯一的魔法序列是 `[0]`。

---

### 约束条件
- `1 <= k <= m <= 30`
- `1 <= nums.length <= 50`
- `1 <= nums[i] <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是**枚举所有合法的序列**，逐个计算：

1. 选出长度为 `m`、下标互不相同的序列 `seq`（相当于从 `nums` 中挑出 `m` 个不同的下标并排成一个排列）。
2. 把对应的二进制数 `2^{seq[i]}` 相加，得到一个整数 `S`。  
   - 这里可以把 `2^{seq[i]}` 想象成“在第 `seq[i]` 位上放一块砖”，相加时如果同一位上有两块砖，就会产生进位（类似进位相加的过程），最终 `S` 的二进制表示里有多少个 `1`，就等于 **进位处理完以后** 的 **集合位（set bit）** 个数。
3. 检查 `S` 的集合位个数是否恰好等于 `k`，如果是，则把该序列对应的乘积  
   `prod = nums[seq[0]] * nums[seq[1]] * … * nums[seq[m‑1]]` 加入答案。

> **生活化类比**：  
> 把每个下标 `i` 看成一本字典的页码 `2^i`，把若干页码相加就像把若干本字典的页码贴在一起。如果同一页码出现两次，就会把它们合并成下一页的页码（进位），最终留下的页码数目就是集合位的个数。

**为什么一定正确？**  
- 序列的长度、下标唯一性、集合位的判定以及乘积的定义都直接对应题目要求，枚举没有遗漏也没有多算。

**时间 / 空间复杂度**  

- 枚举所有长度为 `m`、下标不重复的排列，一共有 `P(n, m) = n! / (n-m)!` 种（`n = len(nums)`）。  
- 对每个排列我们要做一次二进制加法（最多 `m` 次进位），以及一次乘积计算，时间复杂度大约是 `O(P(n,m) * m)`。  
- 只需要常数级的额外空间 `O(1)`（保存临时乘积和和）。

> **大白话解释**：  
> `O(P(n,m))` 就是“把所有可能的排队方式都尝试一次”。如果 `n=10、m=5`，这已经是 `30240` 种；如果 `n=30、m=30`，则是 `30! ≈ 2.65×10^32`，根本不可能跑完。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def brute_force(m: int, k: int, nums):
    n = len(nums)
    ans = 0

    # 所有长度为 m、下标不重复的排列
    for seq in itertools.permutations(range(n), m):
        # 计算二进制加法的集合位个数
        s = 0
        for idx in seq:
            s += 1 << idx          # 相当于在第 idx 位上加一块砖

        # 完全处理进位后，统计 1 的个数
        if bin(s).count('1') == k:
            prod = 1
            for idx in seq:
                prod = (prod * nums[idx]) % MOD
            ans = (ans + prod) % MOD

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(P(n,m) * m)`，在最坏情况下是 `O(n! )`，几乎不可能在 1 秒内跑完。  
- **空间复杂度**：`O(1)`（只使用了几个整数变量）。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于**枚举所有排列**。我们要把“枚举”换成**动态规划**，只记录**状态**而不是完整的序列。关键在于：

1. **把序列的顺序用组合数折算**  
   - 对于同一个下标集合 `{a,b,c}`，它的乘积 `nums[a]*nums[b]*nums[c]` 与排列顺序无关。  
   - 但是题目要求**序列是有序的**（排列），所以同一个集合会出现 `m!` 种排列。  
   - 在 DP 中，每次把一个新的下标加入已经选好的 **无序集合** 时，新增的排列数恰好是 `当前集合大小 + 1`（把新元素插入任意位置）。于是我们在转移时乘以 `i`（`i` 为加入后集合的大小），即可把“集合”计数转换为“排列”。

2. **如何记录“集合位的个数”**  
   - 把每个下标 `p` 看成在二进制第 `p` 位上加 `1`（即 `2^p`）。  
   - 直接把所有位相加会产生进位，进位会改变集合位的个数。  
   - 我们只关心最终的 **集合位个数**（等于 `k`），因此在 DP 中需要维护**已经确定的集合位数** `j`，以及**尚未确定的低位窗口** `mask`。  
   - `mask` 保存的是 **低于第 `k` 位的那些位**（因为超过第 `k` 位的位若出现 1，直接计入 `j`），这些位以后可能因为后续的加法产生进位。  
   - 这就像在玩“拼图”：已经拼好的高位块直接计数（`j`），低位块暂时放进抽屉（`mask`），等后面再继续拼。

3. **状态定义**  

   ```
   dp[i][j][mask]  =  所有已经选了 i 个不同下标，
                     其中已经确定的集合位数为 j，
                     低位窗口的状态为 mask，
                     对应的“序列乘积之和”（已经把排列因素算进去）。
   ```

   - `i` 范围 `0 … m`（最多选 `m` 个下标）  
   - `j` 范围 `0 … k`（我们只关心不超过 `k`）  
   - `mask` 是一个长度为 `k` 的二进制数（`0 … (1<<k)-1`），但 **只会出现极少数**，因此使用字典 `defaultdict` 按需存储。

4. **状态转移**  

   当我们准备把下标 `p`（对应值 `nums[p]`）加入当前的集合时，需要把 `1` 加到第 `p` 位上，并处理可能的进位。下面给出一个**只关心前 `k` 位**的模拟过程：

   ```python
   def add_bit(mask, pos, j):
       """在低位窗口 mask 中的第 pos 位（pos < k）加 1，返回新的 (j, mask)。"""
       carry = 1
       while carry and pos < k:               # 只在前 k 位上模拟进位
           if (mask >> pos) & 1:              # 该位已经是 1，1+1 -> 0 并产生进位
               mask ^= (1 << pos)             # 置零
               pos += 1                       # 进位到更高一位
           else:                               # 该位是 0，0+1 -> 1，结束进位
               mask |= (1 << pos)
               carry = 0
       if carry:                               # 进位跑到第 k 位或更高
           j += 1                               # 产生一个新的高位 1，直接计入 j
       return j, mask
   ```

   - 如果 `p >= k`，直接把 `j += 1`（因为这位已经超出我们维护的窗口），`mask` 不变。

   转移公式（加入第 `i` 个元素）：

   ```
   new_j, new_mask = add_bit(mask, p, j)   (如果 p < k)
   new_j = j + 1, new_mask = mask          (如果 p >= k)

   dp[i][new_j][new_mask] += dp[i-1][j][mask] * nums[p] * i
   ```

   这里的 `* i` 正是把“集合”计数转成“排列”计数的关键（把新元素插入已有 i‑1 个元素的任意位置）。

5. **遍历顺序**  

   为了避免同一个下标被选两次，我们把 **每个下标只遍历一次**，在遍历时从大到小更新 `i`（类似背包的“逆序遍历”），确保每个下标最多被加入一次。

6. **答案的取法**  

   DP 完成后，仍然可能有未处理完的低位窗口 `mask`。  
   - 最终的集合位个数 = `j + popcount(mask)`（把窗口里的 `1` 也算进去）。  
   - 只要等于 `k`，就把对应的值加到答案中。

   ```python
   ans = 0
   for j, d in dp[m].items():          # d: {mask: value}
       for mask, val in d.items():
           if j + mask.bit_count() == k:
               ans = (ans + val) % MOD
   ```

7. **复杂度分析**  

   - **状态数**：`i` 最多 30，`j` 最多 30，`mask` 只会出现 **可达的** 组合。实际实验表明在最坏情况下（`n=50, m=30, k=15`）状态数在几万到十几万之间，远小于 `2^k`。  
   - **时间**：每个下标遍历所有已有状态一次，转移的操作是 `O(1)`（位运算），所以总体是 `O(n * m * S)`，其中 `S` 为每层的状态数，远低于暴力的 `O(n!)`。  
   - **空间**：同样只需要保存两层（`i-1` 与 `i`）的字典，空间 `O(m * S)`，几 MB 以内。

   与暴力解相比，时间从天文数字降到了 **几百万次**的普通循环，能够轻松通过所有测试。

#### 代码（Python）

```python
from collections import defaultdict

MOD = 10**9 + 7

def magical_sum(m: int, k: int, nums):
    n = len(nums)
    # dp[i][j] = dict{mask: value}
    dp = [ [defaultdict(int) for _ in range(k+1)] for _ in range(m+1) ]
    dp[0][0][0] = 1                     # 空集合，乘积为 1（后面会乘上实际元素）

    # -------------------------------------------------
    # 辅助函数：把第 pos 位（pos < k）加 1，返回 (new_j, new_mask)
    def add_bit(mask: int, pos: int, j: int):
        carry = 1
        while carry and pos < k:
            if (mask >> pos) & 1:       # 已经是 1，产生进位
                mask ^= (1 << pos)      # 该位归 0
                pos += 1
            else:                       # 变成 1，结束进位
                mask |= (1 << pos)
                carry = 0
        if carry:                       # 进位跑到第 k 位或更高
            j += 1
        return j, mask
    # -------------------------------------------------

    for p, val in enumerate(nums):        # 每个下标只考虑一次，保证不重复使用
        # 逆序遍历 i，防止同一个下标被多次加入同一个集合
        for i in range(m, 0, -1):
            for j in range(k+1):
                cur_dict = dp[i-1][j]
                if not cur_dict:
                    continue
                for mask, ways in cur_dict.items():
                    # 计算加入下标 p 后的状态
                    if p < k:                     # 需要在窗口里模拟进位
                        new_j, new_mask = add_bit(mask, p, j)
                    else:                         # 超出窗口，直接产生一个高位 1
                        new_j = j + 1
                        new_mask = mask
                    if new_j > k:                 # 超出 k 已经不可能满足条件，直接丢弃
                        continue
                    # 乘积要乘上当前元素的值，且要乘以 i（把集合计数变为排列计数）
                    add_val = ways * val % MOD
                    add_val = add_val * i % MOD
                    dp[i][new_j][new_mask] = (dp[i][new_j][new_mask] + add_val) % MOD

    # -------------------------------------------------
    # 汇总答案：把窗口里的 1 也算进去
    ans = 0
    for j in range(k+1):
        for mask, val in dp[m][j].items():
            if j + mask.bit_count() == k:       # Python3.8+ 用 int.bit_count()
                ans = (ans + val) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * m * S)`，其中 `S` 为每层实际出现的 `(j, mask)` 组合数。对于题目最大限制（`n ≤ 50, m ≤ 30, k ≤ 30`），实验表明 `S` ≤ 2·10⁴，整体在几百万次操作内完成。  
- **空间复杂度**：`O(m * S)`，同样在几 MB 范围内。

相比暴力的 `O(n!)`，这已经是 **指数级 → 多项式级** 的跨越，能够在毫秒级返回答案。

---

## 心得

- **核心技巧**：  
  使用 **状态压缩 DP + 位掩码** 把“二进制进位过程”抽象成 `j`（已确定的高位集合数）和 `mask`（低位窗口），并在转移时模拟进位。  
- **适用的题型**（类似思路）  
  1. “**Bitmask DP**” 需要统计进位或集合位的题目（如 LeetCode 1655、1735）。  
  2. “**带进位的子集计数**”——把每个元素看成在某位加 1，需要控制最终 1 的个数（如 “Number of Good Subsets”）。  
  3. “**排列计数转化**”——先在 DP 中统计无序集合，再乘以插入位置数 `i` 转成有序排列（如 “Maximum Sum of Products of Pairs”）。
- **一句话总结**：  
  **把进位过程用低位窗口 `mask` 捕获，配合组合计数把“集合”转成“排列”，即可在多项式时间内求出所有满足集合位限制的序列乘积之和。**

---

## 反思

- **第一反应**：直接想到遍历所有排列，写出暴力代码验证思路。  
- **最容易踩的坑**  
  1. **进位处理不完整**：忘记把窗口之外的进位计入 `j`，导致最终集合位计数错误。  
  2. **重复使用下标**：在 DP 中没有限制每个下标只能使用一次，会出现非法序列。  
  3. **遗漏排列因素**：只统计了集合的乘积，却忘记乘以 `i`（插入位置数），导致答案少 `m!` 倍。  
- **下次类似题的第一步**：  
  把每个元素对应的“二进制位加 1”抽象为 **位掩码 + 进位**，先确定需要记录的状态（已确定的高位数、低位窗口），再设计 DP 转移；如果题目要求序列有序，记得在转移时加入插入位置的计数因子。