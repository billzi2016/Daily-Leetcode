# #3145. 大数组元素乘积查询 / Find Products of Elements of Big Array

> 难度：困难 · 标签：Array、Binary Search、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/find-products-of-elements-of-big-array/)

---

## 题目（英文原版）

**Description**

The powerful array of a non-negative integer x is defined as the shortest sorted array of powers of two that sum up to x. The table below illustrates examples of how the powerful array is determined. It can be proven that the powerful array of x is unique.
The array big_nums is created by concatenating the powerful arrays for every positive integer i in ascending order: 1, 2, 3, and so on. Thus, big_nums begins as [1, 2, 1, 2, 4, 1, 4, 2, 4, 1, 2, 4, 8, ...].
You are given a 2D integer matrix queries, where for queries[i] = [fromi, toi, modi] you should calculate (big_nums[fromi] * big_nums[fromi + 1] * ... * big_nums[toi]) % modi.
Return an integer array answer such that answer[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: queries = [[1,3,7]]
Output: [4]
Explanation:
There is one query.
big_nums[1..3] = [2,1,2] . The product of them is 4. The result is 4 % 7 = 4.
```

**Example 2:**

```
Input: queries = [[2,5,3],[7,7,4]]
Output: [2,2]
Explanation:
There are two queries.
First query: big_nums[2..5] = [1,2,4,1] . The product of them is 8. The result is 8 % 3 = 2 .
Second query: big_nums[7] = 2 . The result is 2 % 4 = 2 .
```

**Constraints**

- 1 <= queries.length <= 500
- queries[i].length == 3
- 0 <= queries[i][0] <= queries[i][1] <= 1015
- 1 <= queries[i][2] <= 105

---

## 题目（中文翻译）

**描述**  
非负整数 `x` 的 *强大数组*（powerful array）定义为：将 `x` 表示为若干个 2 的幂之和，并且这些幂的集合按升序排列后得到的最短数组。下表展示了如何确定强大数组。可以证明，任意 `x` 的强大数组是唯一的。  

数组 `big_nums` 通过按升序依次拼接每个正整数 `i`（从 1, 2, 3 …）的强大数组得到。因此，`big_nums` 的开头为 `[1, 2, 1, 2, 4, 1, 4, 2, 4, 1, 2, 4, 8, ...]`。

给定一个二维整数矩阵 `queries`，其中 `queries[i] = [from_i, to_i, mod_i]`，需要计算  

\[
(big\_nums[from_i] \times big\_nums[from_i + 1] \times \dots \times big\_nums[to_i]) \bmod mod_i
\]

返回一个整数数组 `answer`，使得 `answer[i]` 为第 `i` 条查询的答案。

---

**示例 1**  
```text
Input: queries = [[1,3,7]]
Output: [4]
Explanation:
There is one query.
big_nums[1..3] = [2,1,2] . The product of them is 4. The result is 4 % 7 = 4.
```

**示例 2**  
```text
Input: queries = [[2,5,3],[7,7,4]]
Output: [2,2]
Explanation:
There are two queries.
First query: big_nums[2..5] = [1,2,4,1] . The product of them is 8. The result is 8 % 3 = 2 .
Second query: big_nums[7] = 2 . The result is 2 % 4 = 2 .
```

---

**约束条件**

- `1 <= queries.length <= 500`
- `queries[i].length == 3`
- `0 <= queries[i][0] <= queries[i][1] <= 10^15`
- `1 <= queries[i][2] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把 big_nums 整个列出来**，然后把查询区间的元素相乘取模。

1. 从 `i = 1` 开始遍历每个正整数。  
2. 把 `i` 的二进制中为 `1` 的位取出来（比如 `13 = 1101₂ → [1,4,8]`），这些就是 `i` 的 *powerful array*。  
3. 把得到的数组按顺序接到 `big_nums` 末尾。  
4. 当 `big_nums` 的长度已经超过所有查询的右端点 `toi` 时，停止生成。  
5. 对每个查询 `[from, to, mod]`，把 `big_nums[from..to]` 中的数逐个相乘，最后取 `% mod`。

> **类比**：把 `big_nums` 想象成一本书的章节目录，**暴力解** 就是把整本书打印出来再去翻页查找。  
> 对于本题，`to` 最多可以是 `10¹⁵`，相当于要打印 **一千兆页**的书，显然不可行。

#### 代码（Python）

```python
def brute_force(queries):
    # 1. 先找出所有查询需要的最大右端点
    max_right = max(q[1] for q in queries)

    big = []                     # 用来存放 big_nums
    i = 1
    while len(big) <= max_right:
        # 把 i 的二进制中为 1 的位取出来，升序存放
        bits = []
        bit = 0
        x = i
        while x:
            if x & 1:            # 当前位是 1 → 这是一条“2 的幂”
                bits.append(1 << bit)   # 2^bit
            x >>= 1
            bit += 1
        big.extend(bits)         # 连接到 big_nums
        i += 1

    # 2. 直接遍历区间求乘积
    ans = []
    for l, r, mod in queries:
        prod = 1
        for v in big[l: r + 1]:   # Python 列表切片是左闭右开，这里手动 +1
            prod = (prod * v) % mod
        ans.append(prod)
    return ans
```

> 代码里每一行都有中文注释，帮助你对照思路。

#### 复杂度

- **时间复杂度**：`O(max_right)`  
  需要把 `big_nums` 生成到最大右端点。因为 `max_right` 可以高达 `10¹⁵`，这相当于**每秒只能处理几千万次**的机器根本跑不完。

- **空间复杂度**：`O(max_right)`  
  需要把全部的 `big_nums` 存在内存里，同样会爆掉。

> **大白话**：`O(n)` 就像是“把 n 件事儿一个一个做”。当 `n = 10¹⁵` 时，想象排队买 1 万亿 张彩票，根本等不到。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于**逐个展开 big_nums**。观察题目可以发现：

1. **big_nums 的每个元素都是 2 的幂**，比如 `1, 2, 4, 8 …`。  
   把这些数相乘等价于把指数相加：  

   \[
   \prod 2^{e_i}=2^{\sum e_i}
   \]

   于是**只要知道区间内所有元素对应的指数之和**，最后再用 `pow(2, sum, mod)` 求模即可。

2. **指数就是二进制中“第几位是 1”**。  
   例如 `13 = 1101₂` → `[1,4,8]` → 指数分别是 `[0,2,3]`。  
   因此我们把问题转化为：**在 `big_nums` 前缀中，所有出现的位号（0‑based）之和是多少**？

3. 对于任意正整数 `n`，我们可以**在 O(log n) 时间**算出：

   - `len(n)`：`1 … n` 的二进制中**1 的总个数**，也就是 `big_nums` 前缀的长度。  
   - `exp(n)`：`1 … n` 的二进制中**所有 1 的位号之和**（即指数之和）。

   这两个公式都是对每一位 `k (0,1,2,…)` 单独统计的。

   > **位计数公式**（把它想成“查字典”）  
   > 对第 `k` 位（值 `2^k`），在 `0 … n` 中出现的次数 =  
   > \[
   > \text{full} = \left\lfloor\frac{n+1}{2^{k+1}}\right\rfloor \times 2^{k}
   > \]  
   > \[
   > \text{rem} = \max\big(0,\;(n+1) \bmod 2^{k+1} - 2^{k}\big)
   > \]  
   > **出现次数** = `full + rem`。  
   > 对应的**指数贡献**就是 `k * (full + rem)`。

4. 现在我们可以得到 **前缀函数**：

   - `pref_len(x)` = `len(x)`（1 … x 的位数总和）  
   - `pref_exp(x)` = `exp(x)`（1 … x 的位号总和）

   这两个函数都在 `O(log x)` 时间完成。

5. 对于查询的右端点 `pos`（比如 `r`），我们需要**前缀到第 `pos` 个元素**的指数和。  
   直接使用 `pref_exp(x)` 会得到 **完整** 到数字 `x` 的贡献，但 `pos` 可能落在某个数字的 **内部**（只取了它的前几位）。

   解决办法：

   - 用二分搜索找最小的整数 `num` 使得 `pref_len(num) >= pos`。  
     此时 `num` 包含了第 `pos` 个元素。  
   - `prev_len = pref_len(num-1)`，`need = pos - prev_len` 表示在 `num` 中需要取多少个最小的 1 位。  
   - 把 `num` 的二进制位号升序列出（最多 60 位，因为 `10¹⁵ < 2⁵⁰`），取前 `need` 个求和。  
   - 最终 `prefix_exp(pos) = pref_exp(num-1) + partial_sum`。

6. 对于查询 `[l, r, mod]`：

   ```text
   total_exp = prefix_exp(r) - prefix_exp(l-1)
   answer    = pow(2, total_exp, mod)
   ```

   只用了 **两次二分 + O(log n) 的位计数**，时间复杂度约为 `O(log² maxPos)`，空间几乎为 `O(1)`。

#### 代码（Python）

```python
import math
from typing import List

# ---------- 1. 统计 1 的个数和位号之和（O(log n)） ----------
def pref_len_and_exp(n: int):
    """
    返回 (len, exp)：
    - len : 1..n 二进制中 1 的总个数   (big_nums 前缀长度)
    - exp : 1..n 所有 1 的位号之和   (指数前缀和)
    """
    total_len = 0          # 位数总和
    total_exp = 0          # 位号之和
    k = 0
    while (1 << k) <= n:   # 只遍历到最高位
        block = 1 << (k + 1)          # 2^{k+1}
        full_cycles = (n + 1) // block
        ones_in_full = full_cycles * (1 << k)   # 每个完整周期里有 2^k 个 1
        rem = (n + 1) % block
        ones_in_rem = max(0, rem - (1 << k))
        cnt = ones_in_full + ones_in_rem        # 第 k 位出现的次数

        total_len += cnt
        total_exp += cnt * k                     # 每出现一次贡献 k
        k += 1
    return total_len, total_exp


# ---------- 2. 前缀指数和，支持任意位置 pos（1-indexed） ----------
def prefix_exp(pos: int) -> int:
    """
    返回 big_nums 前 pos 个元素的指数之和（即 2 的幂的指数之和）。
    若 pos == 0，直接返回 0。
    """
    if pos == 0:
        return 0

    # 先二分找到包含第 pos 个元素的数字 num
    lo, hi = 1, 10**16          # 足够大的上界
    while lo < hi:
        mid = (lo + hi) // 2
        length_mid, _ = pref_len_and_exp(mid)
        if length_mid >= pos:
            hi = mid
        else:
            lo = mid + 1
    num = lo

    # 前面完整的数字贡献
    len_before, exp_before = pref_len_and_exp(num - 1)

    # 这一次我们只需要取 num 的前 need 位
    need = pos - len_before          # 1 ≤ need ≤ popcount(num)

    # 取出 num 的所有 1 位的位号（升序）
    bits = []
    k = 0
    x = num
    while x:
        if x & 1:
            bits.append(k)          # 该位对应的指数是 k
        x >>= 1
        k += 1

    # 只取最小的 need 个（因为 powerful array 要升序）
    partial = sum(bits[:need])

    return exp_before + partial


# ---------- 3. 主函数 ----------
def productQueries(queries: List[List[int]]) -> List[int]:
    """
    对每个查询 [l, r, mod]，计算
        (big_nums[l] * ... * big_nums[r]) % mod
    """
    ans = []
    for l, r, mod in queries:
        # 题目中的下标是 0‑based，prefix_exp 采用 1‑based，
        # 所以把区间左端点 +1 再求前缀差
        total_exp = prefix_exp(r + 1) - prefix_exp(l)
        ans.append(pow(2, total_exp, mod))
    return ans
```

**代码要点解释**

| 行号 | 关键操作 | 中文注释 |
|------|----------|----------|
| 7‑19 | 统计每一位 `k` 在 `1..n` 中出现的次数 `cnt` | 把“查字典”过程写成公式 |
| 21‑22| 把出现次数累加到总长度 `total_len` 与指数和 `total_exp` | 前缀长度与前缀指数 |
| 30‑44| 二分搜索找出包含第 `pos` 个元素的整数 `num` | 把“大书的第 pos 页”定位到哪本章节 |
| 49‑55| 计算 `need`（在 `num` 中需要取多少个最小的 1 位）并把对应的位号相加 | “只读章节的前 need 行” |
| 62‑66| `pow(2, total_exp, mod)` 完成取模幂运算 | Python 自带快速模幂 |

#### 复杂度

- **时间复杂度**：  
  对每个查询：

  1. 两次二分搜索，每次 `O(log X)`（`X`≈`10¹⁵`），每步内部调用 `pref_len_and_exp`，其本身是 `O(log X)`。  
  2. 其余操作（位号提取、求和）最多遍历 60 位。

  综合为 `O(log² X)`，这里 `log X ≤ 60`，所以每个查询最多几千次基本运算，**非常快**。

- **空间复杂度**：`O(1)`（只使用常数个整数变量），不需要存储整个 `big_nums`。

> 与暴力解对比：  
> - 暴力是 `O(max_right)`（线性）并且需要 `O(max_right)` 的内存。  
> - 最优解是 `O(log² max_right)`（对数的对数）并且只用常数空间，能够轻松处理 `10¹⁵` 级别的下标。

---

## 心得

- **核心技巧**：把“乘积”转化为“指数之和”，再利用**位计数公式**快速求前缀统计。  
- **适用的题型**  
  1. 需要对只包含 2 的幂的序列做乘积或求和（例如 “Power of Two Queries”）。  
  2. 统计 **1 的出现次数**或 **位号之和** 的区间查询（如 “Count Total Set Bits”）。  
- **解题钥匙**：**把问题映射到二进制位上**，利用“每一位独立出现次数可直接算”这一性质。

---

## 反思

- **第一反应**：看到“big_nums 是所有正整数的 1 位按升序拼接”，自然会想到直接生成序列。  
- **最容易踩的坑**  
  - 忽视 **下标是 0‑based**，而前缀统计往往写成 **1‑based**，导致 off‑by‑one 错误。  
  - 在二分搜索后忘记处理 **“只取了某个数的部分位”**，导致前缀指数计算不准确。  
  - `mod` 可以是任意正整数（不一定是质数），所以必须使用 **Python 的 `pow(base, exp, mod)`**，而不是欧拉定理等特殊技巧。  
- **下次思路**：  
  1. 先判断序列元素是否都有**共同的数学形式**（本题都是 2 的幂）。  
  2. 把乘积转化为指数求和，检查是否可以用 **前缀统计**。  
  3. 若前缀统计涉及“部分出现”，记得 **二分定位 + 局部补偿**。  

这样一步步抽象，往往能把看似“巨大的”序列问题化简为 **对数级别** 的计算。祝你玩得开心！