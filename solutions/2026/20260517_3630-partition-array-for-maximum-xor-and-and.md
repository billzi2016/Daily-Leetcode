# #3630. 划分数组以获得最大 XOR 与 AND 和 / Partition Array for Maximum XOR and AND

> 难度：困难 · 标签：Array、Math、Greedy、Enumeration · [LeetCode 链接](https://leetcode.com/problems/partition-array-for-maximum-xor-and-and/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Partition the array into three (possibly empty) subsequences A, B, and C such that every element of nums belongs to exactly one subsequence.
Your goal is to maximize the value of: XOR(A) + AND(B) + XOR(C)
where:
Return the maximum value achievable.
Note: If multiple partitions result in the same maximum sum, you can consider any one of them.

**Examples**

**Example 1:**

```
Input: nums = [2,3]
Output: 5
Explanation:
One optimal partition is:
The maximum value of: XOR(A) + AND(B) + XOR(C) = 3 + 2 + 0 = 5 . Thus, the answer is 5.
```

**Example 2:**

```
Input: nums = [1,3,2]
Output: 6
Explanation:
One optimal partition is:
The maximum value of: XOR(A) + AND(B) + XOR(C) = 1 + 2 + 3 = 6 . Thus, the answer is 6.
```

**Example 3:**

```
Input: nums = [2,3,6,7]
Output: 15
Explanation:
One optimal partition is:
The maximum value of: XOR(A) + AND(B) + XOR(C) = 7 + 2 + 6 = 15 . Thus, the answer is 15.
```

**Constraints**

- 1 <= nums.length <= 19
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
将数组划分为三个（可能为空）子序列 `A`、`B`、`C`，要求 `nums` 中的每个元素恰好属于其中的一个子序列。  
你的目标是最大化以下表达式的值：

```
XOR(A) + AND(B) + XOR(C)
```

其中 `XOR(S)` 表示子序列 `S` 中所有元素的按位异或（XOR）结果，`AND(S)` 表示子序列 `S` 中所有元素的按位与（AND）结果。  

返回可以得到的最大值。  
注意：如果有多个划分能够得到相同的最大和，你可以任选其一。

**示例 1**  
``` 
Input: nums = [2,3]
Output: 5
Explanation:
一种最优的划分方式是：
XOR(A) + AND(B) + XOR(C) = 3 + 2 + 0 = 5
因此答案为 5。
```

**示例 2**  
``` 
Input: nums = [1,3,2]
Output: 6
Explanation:
一种最优的划分方式是：
XOR(A) + AND(B) + XOR(C) = 1 + 2 + 3 = 6
因此答案为 6。
```

**示例 3**  
``` 
Input: nums = [2,3,6,7]
Output: 15
Explanation:
一种最优的划分方式是：
XOR(A) + AND(B) + XOR(C) = 7 + 2 + 6 = 15
因此答案为 15。
```

**约束条件**  
- `1 <= nums.length <= 19`  
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每个元素都放进 A、B、C 中的某一个**，枚举所有可能的分配，然后把对应的  
`XOR(A) + AND(B) + XOR(C)` 计算出来，取最大值。  

- **数据结构**：我们只需要把每个元素的所属组记录下来。最常见的做法是使用 **三进制枚举**（0 表示 A，1 表示 B，2 表示 C），相当于把数组看成一个 “三进制数”。  
- **为什么正确**：因为我们把**所有**合法的划分都遍历了一遍，答案一定会在遍历的集合里出现。  
- **复杂度分析**：  
  - 每个元素有 3 种选择，数组长度为 `n`，所以总的枚举次数是 `3ⁿ`。  
  - 对每一种划分，我们要遍历一次数组来分别求 `XOR(A)`、`AND(B)`、`XOR(C)`，这一步是 `O(n)`。  
  - 整体时间复杂度是 `O(3ⁿ · n)`。  
  - 只用了几个整数来保存临时的 XOR/AND，空间 `O(1)`。  

> **大白话**：如果你把 `n` 看成 10，`3ⁿ` 已经是 59049，已经很大了；而题目里 `n` 最多 19，`3¹⁹ ≈ 1.16 × 10⁹`，根本跑不完。  

#### 代码（Python）  

```python
from typing import List
import itertools

def max_xor_and(nums: List[int]) -> int:
    n = len(nums)
    best = 0

    # 0 -> A, 1 -> B, 2 -> C
    for assign in itertools.product(range(3), repeat=n):   # 暴力遍历 3^n 种情况
        xor_a, xor_c = 0, 0
        and_b = (1 << 31) - 1          # 初始全 1，随后与每个 B 元素做 AND

        has_b = False                  # 判断 B 是否为空，空集的 AND 按题意是 0
        for i, g in enumerate(assign):
            if g == 0:                 # 放进 A
                xor_a ^= nums[i]
            elif g == 1:               # 放进 B
                and_b &= nums[i]
                has_b = True
            else:                      # 放进 C
                xor_c ^= nums[i]

        if not has_b:                  # B 为空时，AND 的值应该是 0
            and_b = 0

        best = max(best, xor_a + and_b + xor_c)

    return best
```

> **关键行中文注释** 已在代码中标出。  

#### 复杂度  

- **时间复杂度**：`O(3ⁿ · n)` —— “3 的 n 次方乘以 n”。`3ⁿ` 表示枚举的组合数，`n` 是每次遍历数组的代价。  
- **空间复杂度**：`O(1)` —— 只用了常数个整数变量，不随 `n` 增长。  

---

### 2. 最优解  

#### 思路  

暴力的 **瓶颈** 在于对 **A、B、C 三个子序列 simultaneously** 进行枚举。  
观察题目可以把 **B** 单独枚举，剩下的元素只需要把它们分成 **两个子序列**（A 与 C），这两个子序列的贡献是  

```
XOR(A) + XOR(C)   =   x + (s XOR x)
```

其中  

- `s = XOR(所有不在 B 中的元素)`（即 A∪C 的整体 XOR）  
- `x = XOR(A)`（随意选取的一个子集的 XOR）  

所以 **核心问题** 变成：在已知 `s` 的情况下，**从剩余元素中挑出一个子集的 XOR 为 x，使 `x + (s XOR x)` 最大**。

---

##### 2.1 把目标函数化简  

```
x + (s XOR x)
= s + 2 * (x AND ~s)                （使用位运算的分配律）
```

- `~s` 表示 `s` 的位取反（只保留最高位到 0 的那部分）。  
- `x AND ~s` 只保留 **在 s 中为 0 的位**，这些位如果能被设为 1，就会让 `2 * (x AND ~s)` 更大。  

**结论**：我们只关心 **能够让这些 “s 为 0 的位” 变为 1 的子集 XOR**。  

---

##### 2.2 线性 XOR 基（XOR Basis）  

要在若干数里找出 **最大的可能的子集 XOR**，经典工具是 **线性基**（也叫高斯消元的位运算版）。  
它的工作原理类似 **把字典里每个单词的页码对应到一个唯一的 “基向量”**，任意组合这些基向量就能得到原集合里所有可能的 XOR 值。

构建基的步骤（以 31 位整数为例）：

1. **从高位到低位**，维护 `basis[i]` 表示 **第 i 位最高的基向量**（如果存在）。  
2. 对每个数 `v`：  
   - 从最高位往下找，如果 `v` 在第 `i` 位是 1：  
     - 若 `basis[i]` 为空，就把 `v` 放进去，结束。  
     - 否则，用 `v ^= basis[i]` 把第 `i` 位消掉，继续向低位检查。  
3. 完成后，`basis` 中的非空元素构成了 **线性无关** 的集合，任意子集的 XOR 都可以由它们生成。  

**最大化子集 XOR**：从高位到低位，尝试把当前的基向量 **加入答案**（即 `ans ^= basis[i]`），只要这样会让答案变大，就保留。这样得到的 `ans` 就是所有可能 XOR 中的最大值。

---

##### 2.3 应用到本题  

对于每一种 **B 的取法**（仍然用 2ⁿ 枚举，因为 `n ≤ 19`），我们得到：

- `and_b`：所有在 B 中的数的按位与（如果 B 为空，值为 0）。  
- `rem = [nums[j] for j not in B]`：剩余的元素集合。  
- `s = XOR(rem)`：所有剩余元素的整体 XOR。  

接下来要最大化 `x + (s XOR x)`，根据化简得到的等价式，只需要 **在 `rem` 中挑选若干数**，使得  

```
x_max = 最大的子集 XOR，使得 (x AND ~s) 最大
```

这正好可以通过 **线性基** 完成：

1. 把每个 `v` 替换成 `v & ~s`（只保留在 `s` 为 0 的位）。  
2. 用这些数构建 XOR 基。  
3. 从高位到低位“贪心”取基向量，得到 `best_x = 最大可能的 (x AND ~s)`。  
4. 代回公式 `cur = s + 2 * best_x`，再加上 `and_b`，得到这一次 B 取法的答案。  

遍历所有 `B`（2ⁿ 种）后取最大值，即为最终答案。

---

##### 2.4 为什么线性基是 **最优** 的  

- **完整性**：线性基能够产生 **所有** 可能的子集 XOR（因为它是原集合的线性空间的基）。  
- **最优性**：我们贪心地在高位上尽可能把 `best_x` 的位设为 1，等价于在二进制数中把最高位的 1 放进去，这正是让数值最大的自然做法。  

因此，这个过程一定能得到 `x` 使得 `x + (s XOR x)` 最大。

---

#### 代码（Python）  

```python
from typing import List

def max_xor_and(nums: List[int]) -> int:
    n = len(nums)
    best = 0
    ALL_BITS = 31                     # 1e9 < 2^30，取 31 位安全

    # 预处理：把每个数的二进制补齐到 ALL_BITS 位（python 本身支持无限位，这里仅作说明）

    # 2^n 种 B 的枚举（用整数的位表示是否属于 B）
    for mask in range(1 << n):
        # 计算 B 的 AND
        and_b = (1 << ALL_BITS) - 1   # 初始全 1
        has_b = False
        rem = []                      # 剩余元素（不在 B 中）

        for i in range(n):
            if mask >> i & 1:         # 第 i 位为 1，说明 nums[i] 属于 B
                and_b &= nums[i]
                has_b = True
            else:
                rem.append(nums[i])

        if not has_b:                 # B 为空时，AND 的定义是 0
            and_b = 0

        # s = XOR of all remaining elements
        s = 0
        for v in rem:
            s ^= v

        # ---------- 构造 XOR 基，只保留 ~s 中的位 ----------
        basis = [0] * ALL_BITS         # basis[i] 对应第 i 位的基向量
        for v in rem:
            v &= ~s                     # 只关心 s 为 0 的位
            # 插入 v 到基中
            for bit in range(ALL_BITS - 1, -1, -1):
                if not (v >> bit) & 1:   # 第 bit 位不是 1，继续
                    continue
                if basis[bit] == 0:      # 该位还没有基向量，直接存入
                    basis[bit] = v
                    break
                v ^= basis[bit]          # 消掉该位，继续尝试更低位

        # ---------- 贪心取得最大的 (x AND ~s) ----------
        max_and_part = 0
        for bit in range(ALL_BITS - 1, -1, -1):
            if basis[bit] and not (max_and_part >> bit) & 1:
                # 若把这条基向量加入，能把当前位设为 1，则加入
                if (max_and_part ^ basis[bit]) > max_and_part:
                    max_and_part ^= basis[bit]

        # 现在 max_and_part == max possible (x AND ~s)
        cur = s + 2 * max_and_part + and_b
        best = max(best, cur)

    return best
```

**代码要点解释**  

- `mask` 的每一位对应一个元素是否放进 **B**。使用位运算可以在 `O(1)` 时间判断。  
- `and_b` 初始为全 1 (`(1 << ALL_BITS) - 1`)——这相当于“空字典里所有页码都是 1”，随后逐个 `&=` 把不在 B 的位清掉。  
- `basis` 数组实现 **线性基**：`basis[i]` 保存“最高位是第 i 位的基向量”。插入过程与高斯消元相同，只是用 `^=`（异或）代替减法。  
- 贪心取最大 `max_and_part`：从高位往低位尝试加入基向量，只要加入后数值变大就保留。这样得到的就是 `x AND ~s` 的最大可能值。  
- 最终公式 `s + 2 * max_and_part + and_b` 正是从化简得到的 `x + (s XOR x) + AND(B)`。  

#### 复杂度  

- **时间复杂度**：  
  - 枚举所有 `B`：`2ⁿ`（`n ≤ 19`，约 5.2 × 10⁵）。  
  - 对每个 `mask`，遍历一次数组得到 `rem`、`s`、`and_b`，时间 `O(n)`。  
  - 构造基和贪心取值的复杂度是 `O(|rem| * ALL_BITS)`，`ALL_BITS ≤ 31`，可视为常数。  
  - 综合为 `O(2ⁿ · n · 31)` ≈ `O(2ⁿ · n)`，在约 10⁶ 次基本操作内轻松通过。  

- **空间复杂度**：`O(ALL_BITS)`（基数组）+ `O(n)`（临时的 `rem` 列表），均为线性且很小，整体 `O(n)`。  

> 与暴力的 `3ⁿ` 相比，`2ⁿ` 少了一个常数因子，而且每次只做线性基的 `O(n·logMAX)` 处理，速度提升数十倍甚至上百倍。  

---

## 心得  

- **核心技巧**：**线性 XOR 基**（又称高斯消元的位运算版）配合 **位运算化简** 能把“在若干数中挑子集最大 XOR”问题转化为线性代数求解。  
- **适用的题型**（类似思路）  
  1. *Maximum XOR Subset*（LeetCode 421）  
  2. *Maximum XOR of Two Numbers in an Array*（LeetCode 421 的变形）  
  3. *Maximum XOR Sum of Two Non‑Overlapping Subarrays*（需要在两个子数组之间取最大 XOR）  

- **一句话总结解题钥匙**：  
  > 把 “把剩下的数分成两组的 XOR 和” 化为 “在 `s 为 0` 的位上尽可能设 1”，然后用 **XOR 基** 把这些 1 按位“拼出来”。  

---

## 反思  

- **第一反应**：看到 “XOR(A) + AND(B) + XOR(C)” 直接想到“三进制暴力”，但很快发现 `n` 虽然不大，却会导致 `3ⁿ` 爆炸。  
- **最容易踩的坑**  
  - **B 为空** 时，`AND(B)` 应该是 `0`（而不是全 1），需要单独处理。  
  - **位数范围**：`nums[i] ≤ 10⁹`，最高位是第 30 位，构造基时要确保基数组足够长（取 31 位或 32 位均可）。  
  - **取最大子集 XOR 时的贪心**：必须从高位到低位判断“加入后是否变大”，不能随意把所有基向量都 `^=`。  
- **下次遇到同类题**：第一步先 **把目标函数化简**（比如拆成 `s + 2·(x AND ~s)`），再判断是否可以用 **线性基** 来最大化某个子集 XOR。这样可以快速定位到 “构造基 + 贪心取最大” 的套路。