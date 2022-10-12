# #1969. 数组元素的最小非零乘积 / Minimum Non-Zero Product of the Array Elements

> 难度：中等 · 标签：Math、Greedy、Recursion · [LeetCode 链接](https://leetcode.com/problems/minimum-non-zero-product-of-the-array-elements/)

---

## 题目（英文原版）

**Description**

You are given a positive integer p. Consider an array nums (1-indexed) that consists of the integers in the inclusive range [1, 2p - 1] in their binary representations. You are allowed to do the following operation any number of times:
For example, if x = 1101 and y = 0011, after swapping the 2nd bit from the right, we have x = 1111 and y = 0001.
Find the minimum non-zero product of nums after performing the above operation any number of times. Return this product modulo 109 + 7.
Note: The answer should be the minimum product before the modulo operation is done.

**Examples**

**Example 1:**

```
Input: p = 1
Output: 1
Explanation: nums = [1].
There is only one element, so the product equals that element.
```

**Example 2:**

```
Input: p = 2
Output: 6
Explanation: nums = [01, 10, 11].
Any swap would either make the product 0 or stay the same.
Thus, the array product of 1 * 2 * 3 = 6 is already minimized.
```

**Example 3:**

```
Input: p = 3
Output: 1512
Explanation: nums = [001, 010, 011, 100, 101, 110, 111]
- In the first operation we can swap the leftmost bit of the second and fifth elements.
    - The resulting array is [001, 110, 011, 100, 001, 110, 111].
- In the second operation we can swap the middle bit of the third and fourth elements.
    - The resulting array is [001, 110, 001, 110, 001, 110, 111].
The array product is 1 * 6 * 1 * 6 * 1 * 6 * 7 = 1512, which is the minimum possible product.
```

**Constraints**

- 1 <= p <= 60

---

## 题目（中文翻译）

给定一个正整数 `p`。构造一个 **1-indexed** 数组 `nums`，其元素为区间 `[1, 2^p - 1]` 内的所有整数的二进制表示（不足 `p` 位的前面补零）。  
你可以任意多次执行以下操作：

- 任选两个元素 `x` 和 `y`，以及二进制的任意一个位位置，将该位上的比特（bit）在 `x` 与 `y` 之间交换。  
  例如，若 `x = 1101`、`y = 0011`，交换 **从右数第 2 位** 后得到 `x = 1111`、`y = 0001`。

在进行任意次数的上述操作后，求 `nums` 的 **最小非零乘积**（即所有元素相乘的结果不为零且最小）。返回该乘积对 `10^9 + 7` 取模后的值。  

> **注意**：返回的答案应为取模前的最小乘积，然后再对 `10^9 + 7` 取模。

## 示例

### 示例 1
```
Input: p = 1
Output: 1
Explanation: nums = [1]。数组只有一个元素，乘积即为该元素本身。
```

### 示例 2
```
Input: p = 2
Output: 6
Explanation: nums = [01, 10, 11]。任意一次交换要么使乘积变为 0，要么保持不变。因此 1 * 2 * 3 = 6 已经是最小的非零乘积。
```

### 示例 3
```
Input: p = 3
Output: 1512
Explanation: nums = [001, 010, 011, 100, 101, 110, 111]。
- 第一次操作：交换第二个元素 (010) 与第五个元素 (101) 的最高位，得到 [001, 110, 011, 100, 001, 110, 111]。
- 第二次操作：交换第三个元素 (011) 与第四个元素 (100) 的中间位，得到 [001, 110, 001, 110, 001, 110, 111]。
此时数组的乘积为 1512，已是最小的非零乘积。
```

## 约束

- `1 <= p <= 60`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出的数组 `nums` 包含所有长度为 `p` 的二进制数（去掉全 0 的那一个），即  
```
[1, 2, 3, … , 2^p‑1]
```
我们可以把数组里任意两个数的同一位 **互换**，次数不限。  
最直接的想法是：

1. 把所有可能的位交换都枚举出来。  
2. 每一次交换后把数组所有元素相乘，记下最小的非零乘积。

> **类比**：把每个数想成一本字典的单词，字典里每一列（即同一位）都是同一字母。暴力做法就是把每列的字母随意换位，尝试所有可能的排法，再算出每本书的“价值”（乘积），找最小的非零价值。

这种做法**一定能得到正确答案**（因为我们穷举了所有合法的状态），但：

- `p ≤ 60`，数组长度是 `2^p‑1`，即最多约 `10^18` 个元素，根本不可能真的列出来。  
- 每一次交换只会改变两位，状态空间呈指数级增长，连一秒都撑不住。

#### 代码（Python）

下面的代码只是演示思路，**不适用于真实输入**，仅用于说明暴力法的实现方式。

```python
def brute_min_product(p: int) -> int:
    # 1. 生成原始数组
    nums = list(range(1, (1 << p)))          # [1, 2, … , 2^p‑1]

    # 2. 暴力枚举所有位交换（这里仅示意，实际不可行）
    #    为了让代码能跑，我们只尝试一次随机交换
    import random
    for _ in range(1000):                    # 随机尝试 1000 次
        i, j = random.sample(range(len(nums)), 2)
        # 随机挑选一个位进行交换
        bit = random.randint(0, p - 1)
        mask = 1 << bit
        # 取出该位
        bi = (nums[i] >> bit) & 1
        bj = (nums[j] >> bit) & 1
        # 交换
        if bi != bj:
            nums[i] ^= mask
            nums[j] ^= mask

    # 3. 计算乘积（可能会非常大，实际要取模）
    prod = 1
    for v in nums:
        prod *= v
    return prod
```

> **注意**：这段代码只用于演示“把每列的 0/1 随意换位”，并不保证得到最小值，更不适用于 `p` 较大的情况。

#### 复杂度  

- 时间复杂度：`O(尝试次数 × 交换代价)`，在真正的全枚举情况下是 `O(2^{p·p})`（天文数字），这里用随机尝试把它压到 `O(1000·p)`，但仍然 **不可接受**。  
- 空间复杂度：`O(2^p)` 用于存放数组，同样在 `p=60` 时根本装不下。

> **大白话**：`O(2^p)` 就相当于“把地球上的每粒沙子都装进电脑里”，显然不现实。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点不是位交换本身，而是如何在满足每一列 1 的个数不变的前提下，让整体乘积尽可能小**。  
下面一步步推导出最优策略。

1. **每一列 1 的数量是不变的**  
   初始数组是 `1 … 2^p‑1`，对每一位（从最低位到最高位）来看，`1` 出现的次数恰好是 `2^{p‑1}`。  
   这相当于我们有 `p` 列，每列都有固定的 `2^{p‑1}` 张 “1” 卡片，交换只能把卡片在行之间搬动，**不能增减**。

2. **要让乘积最小，应该把 0 “集中” 到尽可能少的行**  
   - 乘积是所有行值的乘积。  
   - 如果某行里出现很多 `0`，该行的数值就会变小（甚至为 0）。  
   - 但是**出现 0 的行数越多，乘积越可能为 0**，而题目要求 **非零** 最小乘积。  
   - 因此我们只能让 **唯一** 一行出现最少的 `1`（只保留最高位），其余行尽可能全是 `1`。

3. **构造最优的排列**  
   - 把所有 `2^{p‑1}` 张最高位的 `1` 卡片放进同一行，这行的二进制就是 `100…0`，数值为 `2^{p‑1}`。  
   - 其余的 `2^{p‑1}` 张最高位 `1` 分别放进 **其余** `2^{p‑1}` 行，使这些行的最高位也为 `1`。  
   - 对于每一列（除最高位外），我们同样把它的 `2^{p‑1}` 张 `1` 全部放进这 `2^{p‑1}` 行。于是这 `2^{p‑1}` 行的每一位都是 `1`，它们的二进制全部是 `111…1`，数值为 `2^p‑1`。  
   - 这样 **恰好** 使用完所有 `1` 卡片，且没有出现全 0 的行。  

   最终得到的数组（不要求顺序）：

   ```
   [ 2^{p‑1} ]                # 只保留最高位的那一行
   [ 2^p‑1 , 2^p‑1 , … , 2^p‑1 ]   # 共 2^{p‑1} 行
   ```

   注意：我们只需要 **一个** `2^{p‑1}`，其余全部是 `2^p‑1`，因为其余的 `2^{p‑1}‑1` 行已经被 “全 1” 行覆盖了（每列的 1 已经全部用完）。

4. **最小乘积的公式**  

   \[
   \text{minProd}=2^{p-1}\times (2^{p}-1)^{\,2^{p-1}}
   \]

   - 第一个因子是唯一的最小数 `2^{p‑1}`。  
   - 指数 `2^{p‑1}` 表示有多少个 “全 1” 行（即 `2^p‑1`）。  

5. **取模**  

   题目要求先算出真实的最小乘积，再对 `10^9+7` 取模。  
   直接使用 Python 内置的 `pow(base, exp, mod)` 可以在 `O(log exp)` 时间完成 **快速幂**，避免大数溢出。

#### 代码（Python）

```python
MOD = 10**9 + 7

def min_non_zero_product(p: int) -> int:
    """
    返回在进行任意次位交换后，数组的最小非零乘积（模 1e9+7）。
    思路：最小乘积 = 2^{p-1} * (2^p - 1)^{2^{p-1}}，使用快速幂取模。
    """
    # 2^p % MOD
    pow2_p = pow(2, p, MOD)                     # 计算 2^p (模 MOD)
    # 2^{p-1} % MOD
    pow2_half = pow(2, p - 1, MOD)               # 计算 2^{p-1} (模 MOD)

    # (2^p - 1) % MOD，先算 2^p 再减 1，防止负数
    max_val = (pow2_p - 1) % MOD

    # (2^p - 1)^{2^{p-1}} % MOD，使用内置 pow 实现快速幂
    part = pow(max_val, pow2_half, MOD)

    # 最终答案 = 2^{p-1} * part % MOD
    ans = (pow2_half * part) % MOD
    return ans
```

**代码要点说明**  

| 行号 | 关键操作 | 中文注释 |
|------|----------|----------|
| 5    | `pow(2, p, MOD)` | 计算 `2^p` 并直接取模，防止中间值爆炸 |
| 7    | `pow(2, p-1, MOD)` | 计算 `2^{p-1}`（也是指数） |
| 10   | `(pow2_p - 1) % MOD` | 得到 `2^p - 1`（全 1 的数） |
| 13   | `pow(max_val, pow2_half, MOD)` | 快速幂：`(2^p - 1)^{2^{p-1}}` 取模 |
| 16   | `(pow2_half * part) % MOD` | 最终乘积再取模 |

#### 复杂度  

- **时间复杂度**：`O(log p)`（快速幂的对数复杂度），因为 `pow` 的时间是 `O(log exponent)`，这里 exponent 为 `2^{p-1}`，但 `pow` 实际上使用 **模指数** 的二进制展开，复杂度是 `O(log 2^{p-1}) = O(p)`，而 `p ≤ 60`，几乎可以视作常数。  
- **空间复杂度**：`O(1)`，只用了若干整数变量。

> **对比**：暴力解需要指数级时间和空间，而最优解只用几次整数运算，瞬间就能得到答案。

---

## 心得

- **核心技巧**：**位计数不变 + 把 0 集中到最少的行**，从而把多数行变成最大值 `2^p‑1`，唯一一行保留最小非零值 `2^{p‑1}`。  
- **适用题型**：  
  1. 需要在“每一位的 1 数量固定”前提下最小化/最大化整体乘积或和的题目（如 “Maximum Product of the Array After Swaps”）。  
  2. 类似 “把 0/1 卡片重新分配，使得某种代价最小” 的组合优化题。  
- **解题钥匙**：**先统计每一列的 1 的总数，再思考如何把这些 1 “集中”或“分散”，找出让乘积最小的极端分布**。

---

## 反思

- **第一反应**：立刻想到“枚举所有交换”，因为位交换听起来像是可以随意调换的自由操作。  
- **最容易踩的坑**：  
  - 忽视每一列 `1` 的总数是固定的，导致误以为可以让所有数都变成 `1`。  
  - 没有注意到“非零”限制，随意把所有 `1` 收集到一行会导致其它行全为 `0`，乘积为 `0`（不符合要求）。  
- **下次类似题的第一步**：**先写出每一位（或每一列）的统计信息**，弄清哪些量是守恒的，再在这些守恒约束下寻找极端（最小或最大）分布。这样往往能直接导出数学公式，避免暴力搜索的陷阱。