# #982. 位与为零的三元组 / Triples with Bitwise AND Equal To Zero

> 难度：困难 · 标签：Array、Hash Table、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/triples-with-bitwise-and-equal-to-zero/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the number of AND triples.
An AND triple is a triple of indices (i, j, k) such that:

**Examples**

**Example 1:**

```
Input: nums = [2,1,3]
Output: 12
Explanation: We could choose the following i, j, k triples:
(i=0, j=0, k=1) : 2 & 2 & 1
(i=0, j=1, k=0) : 2 & 1 & 2
(i=0, j=1, k=1) : 2 & 1 & 1
(i=0, j=1, k=2) : 2 & 1 & 3
(i=0, j=2, k=1) : 2 & 3 & 1
(i=1, j=0, k=0) : 1 & 2 & 2
(i=1, j=0, k=1) : 1 & 2 & 1
(i=1, j=0, k=2) : 1 & 2 & 3
(i=1, j=1, k=0) : 1 & 1 & 2
(i=1, j=2, k=0) : 1 & 3 & 2
(i=2, j=0, k=1) : 3 & 2 & 1
(i=2, j=1, k=0) : 3 & 1 & 2
```

**Example 2:**

```
Input: nums = [0,0,0]
Output: 27
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] < 216

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums`，返回满足位与（AND）结果为 0 的三元组数量。  
一个 **AND 三元组** 是一组索引 `(i, j, k)`，满足：

```
nums[i] & nums[j] & nums[k] == 0
```

其中 `&` 表示按位与（bitwise AND）运算。

---

### 示例

**示例 1**

```text
Input: nums = [2,1,3]
Output: 12
Explanation: 我们可以选择以下 (i, j, k) 三元组：
(i=0, j=0, k=1) : 2 & 2 & 1
(i=0, j=1, k=0) : 2 & 1 & 2
(i=0, j=1, k=1) : 2 & 1 & 1
(i=0, j=1, k=2) : 2 & 1 & 3
(i=0, j=2, k=1) : 2 & 3 & 1
(i=1, j=0, k=0) : 1 & 2 & 2
(i=1, j=0, k=1) : 1 & 2 & 1
(i=1, j=0, k=2) : 1 & 2 & 3
(i=1, j=1, k=0) : 1 & 1 & 2
(i=1, j=2, k=0) : 1 & 3 & 2
(i=2, j=0, k=1) : 3 & 2 & 1
(i=2, j=1, k=0) : 3 & 1 & 2
```

**示例 2**

```text
Input: nums = [0,0,0]
Output: 27
```

---

### 约束条件

- `1 <= nums.length <= 1000`
- `0 <= nums[i] < 2^16`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有下标三元组 `(i, j, k)` 都枚举一遍，逐个检查

```
nums[i] & nums[j] & nums[k] == 0
```

- **使用的数据结构**：只需要一个普通的列表 `nums`，不需要额外的结构。  
  （把它想象成一排编号的盒子，盒子里放的就是每个整数。我们只要把盒子拿出来，一个个比较就行了。）

- **为什么正确**：只要遍历到所有可能的 `(i, j, k)`，并对每个三元组都做“与”运算，满足条件的必然被统计，漏掉的不存在。

- **复杂度分析**：  
  - 外层有 `n` 个 `i`，中层有 `n` 个 `j`，里层还有 `n` 个 `k`，于是总共要做 `n³` 次“与”运算。  
  - `n` 最多是 1000，`1000³ = 10⁹`，这在一秒几千次的 Python 里根本跑不完。  
  - 空间上只用了原数组和几个计数器，都是 **O(1)**（常数级）的额外空间。

> **大白话解释**：  
> `O(n³)` 就像让 1000 个人每人去跟另外 999 个人握手、再跟每个人再握一次手——次数太多了，根本来不及完成。

#### 代码（Python）

```python
def countTriples_bruteforce(nums):
    n = len(nums)
    ans = 0
    for i in range(n):                     # 第一个下标
        for j in range(n):                 # 第二个下标
            for k in range(n):             # 第三个下标
                if (nums[i] & nums[j] & nums[k]) == 0:
                    ans += 1               # 满足条件就计数
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)` —— 随着数组长度的立方增长，运算次数会非常爆炸。  
- **空间复杂度**：`O(1)` —— 只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **三层循环**，每一次都要遍历整个数组。  
我们要把 “遍历所有三元组” 换成 “只遍历所有可能的位掩码”。  
因为题目中所有数都不大于 `2¹⁶-1`（即 16 位），所以可以把 **每个数看成 16 盏灯的开关**：

- **灯亮** → 该位为 `1`  
- **灯灭** → 该位为 `0`

如果我们知道“有多少个数的灯集合**包含**某个特定的灯组合（即某个子集）”，就可以用它来快速统计满足 `a & b & c == 0` 的三元组。

下面一步步把思路展开：

1. **统计每个数出现的次数**  
   建立大小为 `2¹⁶`（65536）的数组 `cnt[mask]`，`cnt[x]` 表示数组里等于 `x` 的元素有多少个。  
   这一步相当于把所有盒子按照“灯的开关形状”分类。

2. **求每个子集的“超集计数”**  
   对每个掩码 `mask`，我们想知道有多少个数 **至少** 包含 `mask` 中所有的 `1`（即这些数的二进制是 `mask` 的**超集**）。  
   记作 `sup[mask]`。  
   这一步可以用 **SOS DP（Subset‑On‑Superset DP）** 在 `O(位数 * 2^位数)` 完成。  
   类比：如果把每个掩码想成一本字典，`sup[mask]` 就像查“所有包含这些关键字的词条有多少”。

3. **计算“两个数的与等于某个掩码”的有序对数目**  
   设 `pair[mask]` 为 **有序** 对 `(y, z)` 满足 `nums[y] & nums[z] == mask` 的个数。  
   根据容斥原理（或 Möbius 反演），可以先把 `sup[mask]` 的平方视为 “两个数都至少包含 `mask`”，再减去更大掩码的情况：

   ```
   pair[mask] = sup[mask] * sup[mask]          # 暴力地把所有 sup[mask] 的组合算进去
   for each superset t of mask (t != mask):
       pair[mask] -= pair[t]                  # 把掩码更大的情况剔除掉
   ```

   这一步同样可以在 `O(位数 * 2^位数)` 完成，因为我们按 **从大到小的掩码** 逐个消除。

4. **最终答案**  
   对每个可能的第一个数 `x = nums[i]`（对应掩码 `x`），只要第二、第三个数的与是 `(~x) & ((1<<16)-1)`（即 `x` 的补码在 16 位范围内），整体的 AND 就会是 0。  
   所以：

   ```
   ans = Σ_{mask} cnt[mask] * pair[complement(mask)]
   ```

   这里 `complement(mask) = (~mask) & ((1<<16)-1)`，保证只保留 16 位。

> **关键点总结**  
> - 把 **位运算** 转化为 **子集/超集计数**。  
> - 用 **SOS DP** 快速得到每个子集的超集个数。  
> - 再用 **Möbius 反演** 把 “至少包含” 转成 “恰好等于”。  
> - 最后把第一个数的出现次数和对应的配对数相乘即可。

#### 代码（Python）

```python
def countTriples(nums):
    # ---------- 1. 统计每个数出现的次数 ----------
    MAX_BITS = 16                         # 题目说 nums[i] < 2^16
    SIZE = 1 << MAX_BITS                  # 2^16 = 65536
    cnt = [0] * SIZE                      # cnt[mask] = 出现次数
    for x in nums:
        cnt[x] += 1

    # ---------- 2. SOS DP：求 sup[mask]（超集计数） ----------
    sup = cnt[:]                          # 初始时 sup[mask] = cnt[mask]
    # 对每一位进行“把子集的计数加到它的子集上”
    for bit in range(MAX_BITS):
        for mask in range(SIZE):
            if (mask & (1 << bit)) == 0:   # 如果第 bit 位是 0，说明 mask 是它的子集
                sup[mask] += sup[mask | (1 << bit)]

    # ---------- 3. 计算 pair[mask] = 有序对 (y,z) 且 (y & z) == mask ----------
    pair = [0] * SIZE
    # 先把 sup[mask]^2 计入（两个数都至少包含 mask）
    for mask in range(SIZE):
        pair[mask] = sup[mask] * sup[mask]

    # Möbius 反演：从大到小消除被更大掩码覆盖的情况
    for bit in range(MAX_BITS):
        for mask in range(SIZE):
            if (mask & (1 << bit)) == 0:   # mask 是子集，mask|bit 是更大的超集
                pair[mask] -= pair[mask | (1 << bit)]

    # ---------- 4. 统计答案 ----------
    FULL = SIZE - 1                       # 16 位全 1，即 0b111...111
    ans = 0
    for mask in range(SIZE):
        complement = FULL ^ mask          # 只保留 16 位的补码
        ans += cnt[mask] * pair[complement]

    return ans
```

> **代码注释要点**  
> - `sup[mask]` 的更新过程相当于“把每个灯亮的组合的计数，往所有把这盏灯关掉的子集合并”。  
> - `pair[mask]` 先用 `sup[mask]^2` 把所有可能的有序对算进来，再用 **Möbius 反演**（即从大到小减去多算的部分）得到恰好等于 `mask` 的对数。  
> - 最后乘上 `cnt[mask]`（第一个数的出现次数）再乘以对应的配对数 `pair[~mask]`，即得到所有满足 `AND == 0` 的有序三元组。

#### 复杂度

- **时间复杂度**：`O(位数 * 2^位数)`  
  - `位数 = 16`，`2^位数 = 65536`，两层循环各遍历一次，所以大约 `16 * 65536 ≈ 1.05 * 10⁶` 次基本操作。  
  - 与暴力的 `O(n³)`（最坏 10⁹）相比，快了 **几千倍**，完全可以在毫秒级通过。

- **空间复杂度**：`O(2^位数)`  
  - 需要 `cnt、sup、pair` 三个大小为 `65536` 的整型数组，约占几百 KB，远小于题目给出的内存限制。

---

## 心得

- **核心技巧**：  
  1. **位掩码转子集计数**（SOS DP）  
  2. **Möbius 反演**（把“至少包含”转成“恰好等于”）  

- **适用的题型**（可以迁移这些技巧）：  
  - *“子集的和/乘积/位运算”等需要快速统计所有子集/超集的题目*  
  - LeetCode 1977️⃣ **Number of Ways to Separate Numbers**（子集计数）  
  - LeetCode 1915️⃣ **Number of Wonderful Substrings**（位掩码子集 DP）  

- **一句话总结解题钥匙**：  
  **把“逐个枚举三元组”换成“遍历所有位掩码”，利用 SOS DP 把 2ⁿ 个状态一次性算完**。

---

## 反思

- **第一反应**：看到 “三元组 AND 为 0”，立刻想到三层循环暴力枚举。  
- **最容易踩的坑**：  
  - 忘记对 **有序**三元组计数，直接除以 `6`（去重）会得到错误答案。  
  - 计算补码时必须限制在 16 位内，使用 `FULL ^ mask` 而不是普通的 `~mask`，否则会出现负数导致数组越界。  
  - 在 SOS DP 中遍历顺序必须是 **从低位到高位**（或相反），否则会重复累加。

- **下次遇到同类题**：第一步先检查数值范围是否足够小，能否把“值”映射到位掩码空间；如果可以，立刻考虑 **SOS DP + Möbius 反演** 这条常用路线。