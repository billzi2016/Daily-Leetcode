# #3514. 唯一异或三元组计数 II / Number of Unique XOR Triplets II

> 难度：中等 · 标签：Array、Math、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/number-of-unique-xor-triplets-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
A XOR triplet is defined as the XOR of three elements nums[i] XOR nums[j] XOR nums[k] where i <= j <= k.
Return the number of unique XOR triplet values from all possible triplets (i, j, k).

**Examples**

**Example 1:**

```
Input: nums = [1,3]
Output: 2
Explanation:
The possible XOR triplet values are:
The unique XOR values are {1, 3} . Thus, the output is 2.
```

**Example 2:**

```
Input: nums = [6,7,8,9]
Output: 4
Explanation:
The possible XOR triplet values are {6, 7, 8, 9} . Thus, the output is 4.
```

**Constraints**

- 1 <= nums.length <= 1500
- 1 <= nums[i] <= 1500

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
异或三元组（XOR triplet）定义为三个元素的异或值 `nums[i] XOR nums[j] XOR nums[k]`，其中 `i <= j <= k`。  
返回所有可能的三元组 `(i, j, k)` 所产生的 **唯一** 异或三元组值的数量。

**示例 1**  
```text
Input: nums = [1,3]
Output: 2
```
**解释**：  
可能的异或三元组值为：  
唯一的异或值为 `{1, 3}`，因此答案为 `2`。

**示例 2**  
```text
Input: nums = [6,7,8,9]
Output: 4
```
**解释**：  
可能的异或三元组值为：  
唯一的异或值为 `{6, 7, 8, 9}`，因此答案为 `4`。

**约束条件**  
- `1 <= nums.length <= 1500`  
- `1 <= nums[i] <= 1500`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有合法的三元组** `(i, j, k)`，计算  

```
value = nums[i] ^ nums[j] ^ nums[k]      # ^ 表示按位异或
```  

把每一次得到的 `value` 放进一个集合（`set`），最后集合的大小就是答案。  

- **用到的数据结构**：  
  - **列表** `nums` 本身存放数组。  
  - **集合** `set`，像一本“字典”，把每个出现过的 XOR 结果记下来，重复的会自动被合并。  
- **为什么正确**：  
  - 题目要求“所有可能的三元组的 XOR 值”，只要把 **每一种可能** 都算一遍，就不会漏掉任何值。  
- **复杂度分析（大白话）**：  
  - 我们要把每一个 `i`、`j`、`k` 都遍历一遍。假设数组长度是 `n`，那么 `i`、`j`、`k` 各自可以取 `n` 种可能，**总共要做 `n × n × n = n³` 次计算**。  
  - 这就像把 1500 本书全部排成三层楼，每层楼再把每本书都挑出来检查一次，显然太慢。  
  - 空间上，只需要保存集合里出现的 XOR 值，最多也就是所有可能的 XOR（因为 `nums[i] ≤ 1500`，所以 XOR 的最大值不超过 `2¹¹‑1 = 2047`），所以空间是 **O(1)**（常数级）。


#### 代码（Python）

```python
from typing import List

def countUniqueXorTriplets_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    uniq = set()                     # 用来保存所有出现过的 XOR 值

    for i in range(n):               # 第一个下标
        for j in range(i, n):        # 第二个下标，保证 i <= j
            for k in range(j, n):    # 第三个下标，保证 j <= k
                xor_val = nums[i] ^ nums[j] ^ nums[k]   # 计算三元组的 XOR
                uniq.add(xor_val)   # 放进集合，重复的会自动去重

    return len(uniq)                 # 集合大小就是不同的 XOR 值个数
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 直观地说，就是把所有 `i、j、k` 三层循环全部跑一遍。对于 `n = 1500`，这会产生约 **3.4 × 10⁹** 次计算，远远超出合理时间。  
- **空间复杂度**：`O(1)`（实际上是 `O(2048)`，因为 XOR 结果最多只有 2048 种可能）  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举三层循环是最大的瓶颈**。我们要想办法把这层循环压掉。下面一步步推导优化思路：

1. **利用异或的性质**  
   - 异或满足**交换律**和**结合律**：`a ^ b ^ c` 与顺序无关。  
   - 同一个数异或两次会抵消：`x ^ x = 0`，所以  
     - `x ^ x ^ y = y`（两个相同的下标等价于只保留另一个）  
     - `x ^ x ^ x = x`（三个相同的仍然是 `x`）  

   这意味着只要出现**重复下标**，最终的值要么是数组里的某个元素本身，要么是 **三个互不相同** 的数的 XOR。

2. **先把所有单个元素的值记下来**  
   - 任意三元组至少能产生数组中出现的每个数（把前两个下标设成相同），所以答案一定包含所有**不同的数组元素**。

3. **关注“三个不同数的 XOR”**  
   - 设 `a、b、c` 为三种不同的数，`a ^ b ^ c` 就是我们需要额外考虑的值。  
   - 关键是 **如何快速枚举所有 `a ^ b ^ c`**。

4. **把问题转化为“两个数的 XOR 再异或第三个数”**  
   - 先算出 **所有可能的两数 XOR**（包括相同下标的情况），记为 `pair_xor = a ^ b`。  
   - 然后对每个数组元素 `c`，把 `pair_xor ^ c` 加入答案集合。  
   - 这样每个三元组的 XOR 都能被表示成 “某个两数 XOR 再 ^ 第三个数”。  

5. **利用取值范围的限制**  
   - 题目给出 `nums[i] ≤ 1500`，即所有数都在 **0~1500** 之间。  
   - 任意三个数的 XOR 最大不超过 `2¹¹‑1 = 2047`（因为 1500 < 2¹¹）。  
   - 因此所有可能的 XOR 结果只有 **2048** 种，完全可以用一个长度为 2048 的布尔数组 `seen[2048]` 来标记是否出现过。  

6. **整体算法**  
   - **步骤 1**：把所有不同的 `nums[i]` 标记为已出现。  
   - **步骤 2**：双层循环（`i ≤ j`）算出所有 `pair_xor = nums[i] ^ nums[j]`，把它们放进一个列表 `pair_list`（去重或不去重都行，后面会再次去重）。  
   - **步骤 3**：遍历 `pair_list`，对每个 `c`（遍历整个 `nums`），计算 `pair ^ c` 并在 `seen` 中标记。  
   - 由于 `pair_list` 的大小至多是 2048，步骤 3 的复杂度是 `O(2048 * n)`，远远小于 `O(n³)`，实际上接近线性。

**核心技巧**：利用 **异或的消消乐特性** + **值域小（只要 2048 种）**，把原本的三层枚举压缩成 **两层**，再用 **布尔数组** 实现 O(1) 的去重。

#### 代码（Python）

```python
from typing import List

def countUniqueXorTriplets(nums: List[int]) -> int:
    """
    最优解：O(n^2) 时间，O(2048) 额外空间
    """
    MAX_XOR = 2048                     # 2^11，因为 nums[i] <= 1500 < 2^11
    seen = [False] * MAX_XOR           # seen[v] 为 True 表示 XOR 值 v 已出现

    # 1. 单个元素本身一定是合法的 XOR 值
    for x in nums:
        seen[x] = True

    n = len(nums)
    pair_xors = []                     # 保存所有两数 XOR（包括 i==j 的情况）

    # 2. 计算所有两数 XOR，i <= j 保证不重复计数
    for i in range(n):
        for j in range(i, n):
            pair = nums[i] ^ nums[j]
            pair_xors.append(pair)    # 这里不去重，后面会统一处理

    # 3. 把两数 XOR 再和第三个数异或，得到所有三数 XOR
    #    由于 pair_xors 的取值范围也在 [0, 2047]，我们可以直接遍历
    for pair in pair_xors:
        for c in nums:
            triple = pair ^ c          # 实际上是 a ^ b ^ c
            seen[triple] = True

    # 4. 统计出现过的不同 XOR 值数量
    return sum(seen)                   # True 当作 1，统计为 1 的个数
```

**代码要点说明**  

- `MAX_XOR = 2048`：因为 1500 的二进制最高位是第 11 位（2¹⁰ = 1024），三个数异或最多会把第 11 位打开，所以取 `2^11 = 2048` 作为上界。  
- `seen` 用布尔数组代替 `set`，查询/插入都是 O(1) 并且省去哈希开销。  
- 第一步把所有单独的元素标记，确保即使所有三数都出现重复也不会遗漏。  
- 第二步的双层循环是 **O(n²)**，这是算法的主要时间消耗。  
- 第三步的两层循环本质上是 `O(|pair_xors| * n)`，但 `|pair_xors| ≤ 2048`，所以整体仍是 **≈ O(n²)**（常数很小）。

#### 复杂度  

- **时间复杂度**：`O(n² + n * U)`，其中 `U = 2048`（所有可能的 XOR 值个数），对本题而言可以简写为 **O(n²)**。  
  - 与暴力的 `O(n³)` 相比，省掉了一层循环，速度提升约 `n` 倍（1500 → 1500/1500 = 1/1500）。  
- **空间复杂度**：`O(U)` = **O(2048)**，即常数级别的额外空间。  
  - `pair_xors` 最多也只会保存 2048 条不同的两数 XOR，完全可以视为常数空间。

---

## 心得  

- **核心技巧**：利用异或的“消消乐”特性把三元组的 XOR 转化为 “两数 XOR 再异或第三个数”，并借助**值域有限**（最多 2048 种）用布尔数组快速去重。  
- **适用的题型**（类似思路可复用）：  
  1. **唯一 XOR 子集值**（如“所有子数组的 XOR 有多少种”）  
  2. **限定长度的 XOR 组合计数**（如“长度为 2 或 3 的子序列 XOR 种类数”）  
  3. **位运算 + 小范围取值** 的计数问题（如“所有两数之和在限定范围内的不同值”）  
- **一句话总结解题钥匙**：**把高维组合问题压缩到低维，再用“取值上界 + 布尔表”完成 O(1) 去重**。

---

## 反思  

- **第一反应**：直接三层循环枚举，写出最直观的实现。  
- **最容易踩的坑**：  
  - 忽视 **i ≤ j ≤ k** 允许下标相同，导致误以为只能取三种不同的数。实际上重复下标会把 XOR 结果简化为单个元素。  
  - 没注意到 **nums[i] ≤ 1500**，从而错失利用 **最大 XOR 只到 2047** 的优化空间。  
- **下次遇到同类题**，第一步应该先**分析运算的代数性质（如 XOR 的消消乐）**，并**估算结果的取值范围**，看能否用固定大小的数组/位图来做 O(1) 去重。这样往往能把指数级/立方级的暴力直接压到二次或线性量级。