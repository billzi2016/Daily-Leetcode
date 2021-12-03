# #1577. 数的平方等于两个数乘积的方案数 / Number of Ways Where Square of Number Is Equal to Product of Two Numbers

> 难度：中等 · 标签：Array、Hash Table、Math、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-where-square-of-number-is-equal-to-product-of-two-numbers/)

---

## 题目（英文原版）

**Description**

Given two arrays of integers nums1 and nums2, return the number of triplets formed (type 1 and type 2) under the following rules:

**Examples**

**Example 1:**

```
Input: nums1 = [7,4], nums2 = [5,2,8,9]
Output: 1
Explanation: Type 1: (1, 1, 2), nums1[1]2 = nums2[1] * nums2[2]. (42 = 2 * 8).
```

**Example 2:**

```
Input: nums1 = [1,1], nums2 = [1,1,1]
Output: 9
Explanation: All Triplets are valid, because 12 = 1 * 1.
Type 1: (0,0,1), (0,0,2), (0,1,2), (1,0,1), (1,0,2), (1,1,2).  nums1[i]2 = nums2[j] * nums2[k].
Type 2: (0,0,1), (1,0,1), (2,0,1). nums2[i]2 = nums1[j] * nums1[k].
```

**Example 3:**

```
Input: nums1 = [7,7,8,3], nums2 = [1,2,9,7]
Output: 2
Explanation: There are 2 valid triplets.
Type 1: (3,0,2).  nums1[3]2 = nums2[0] * nums2[2].
Type 2: (3,0,1).  nums2[3]2 = nums1[0] * nums1[1].
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 1000
- 1 <= nums1[i], nums2[i] <= 105

---

## 题目（中文翻译）

给定两个整数数组 `nums1` 和 `nums2`，返回满足以下规则形成的三元组（triplet）的数量（分为类型 1 和类型 2）。

**约束条件**  
- `1 <= nums1.length, nums2.length <= 1000`  
- `1 <= nums1[i], nums2[i] <= 10^5`

**示例**

**示例 1**  
```
Input: nums1 = [7,4], nums2 = [5,2,8,9]
Output: 1
```
**解释**：类型 1 的三元组为 `(1, 1, 2)`，满足 `nums1[1]^2 = nums2[1] * nums2[2]`（`4^2 = 2 * 8`）。

**示例 2**  
```
Input: nums1 = [1,1], nums2 = [1,1,1]
Output: 9
```
**解释**：所有三元组均合法，因为 `1^2 = 1 * 1`。  
- 类型 1 的三元组有 `(0,0,1)`, `(0,0,2)`, `(0,1,2)`, `(1,0,1)`, `(1,0,2)`, `(1,1,2)`，满足 `nums1[i]^2 = nums2[j] * nums2[k]`。  
- 类型 2 的三元组有 `(0,0,1)`, `(1,0,1)`, `(2,0,1)`，满足 `nums2[i]^2 = nums1[j] * nums1[k]`。

**示例 3**  
```
Input: nums1 = [7,7,8,3], nums2 = [1,2,9,7]
Output: 2
```
**解释**：共有 2 个合法三元组。  
- 类型 1：`(3,0,2)`，满足 `nums1[3]^2 = nums2[0] * nums2[2]`。  
- 类型 2：`(3,0,1)`，满足 `nums2[3]^2 = nums1[0] * nums1[1]`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求统计两类「三元组」：

* **类型 1**：`nums1[i]² = nums2[j] * nums2[k]`  
* **类型 2**：`nums2[i]² = nums1[j] * nums1[k]`

最直接的想法就是「把所有可能的下标组合都枚举一遍」：

1. 先遍历 `nums1` 中的每个元素 `i`，计算 `nums1[i]²`。  
2. 再遍历 `nums2` 中的所有 **有序** 两个下标 `(j, k)`（`j < k`），计算 `nums2[j] * nums2[k]`。  
3. 两个值相等时计数。  
4. 类型 2 同理，只是把角色互换。

> **类比**：把 `nums2` 想成一本字典，`nums2[j] * nums2[k]` 就是「把两个词的页码相乘」得到的「新页码」。我们把所有「新页码」都写下来，再去找有没有和「某个词的平方页码」相同的。

**为什么正确**  
因为我们把「所有可能的」`i、j、k` 组合都检查了一遍，凡是满足等式的必然被计数，凡是不满足的自然被过滤。

**时间/空间复杂度**  

- 枚举 `i`（`len(nums1) = n`） → `O(n)`  
- 枚举 `j,k`（`len(nums2) = m`），两层循环 → `O(m²)`  
- 所以类型 1 的时间是 `O(n * m²)`，类型 2 同理是 `O(m * n²)`。  
- 合在一起最坏情况是 `O(n·m² + m·n²)`，在 `n = m = 1000` 时约等于 `10⁹` 次运算，远超 1 秒的限制。  

空间方面，只用了常数级变量 → `O(1)`。

> **大白话**：`O(n²)` 并不是说「两百次」或「两千次」，它表示「随着 n 增大，运算次数会像 n 的平方那样快速增长」。当 n = 1000 时，`n² = 1,000,000`，已经是百万级别了；再乘以另一个 1000，立刻变成十亿级。

#### 代码（Python）

```python
def numTriplets_bruteforce(nums1, nums2):
    # ---------- 类型 1 ----------
    cnt = 0
    n, m = len(nums1), len(nums2)
    for i in range(n):                         # 遍历 nums1 的每个元素
        target = nums1[i] * nums1[i]            # 计算平方
        for j in range(m):                     # 两层循环枚举 nums2 中的两下标
            for k in range(j + 1, m):
                if target == nums2[j] * nums2[k]:
                    cnt += 1

    # ---------- 类型 2 ----------
    for i in range(m):
        target = nums2[i] * nums2[i]
        for j in range(n):
            for k in range(j + 1, n):
                if target == nums1[j] * nums1[k]:
                    cnt += 1
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n·m² + m·n²)` — 随着数组长度的平方增长，运算次数会非常大。  
- **空间复杂度**：`O(1)` — 只用了几个临时变量，不会随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**同一个「两个数的乘积」很多次。  
例如 `nums2 = [a, b, c, d]`，`a*b`、`a*c`、`a*d`… 这些乘积在不同的外层 `i` 时都会重新算一遍。

**关键优化**：把「所有可能的乘积」预先算好并记录出现次数。这样后面只要看「某个平方」是否等于「某个乘积」时，就可以 **O(1)** 地查表。

实现步骤：

1. **统计乘积频率**  
   - 对 `nums1`，遍历所有下标对 `(i, j)`（`i < j`），把 `nums1[i] * nums1[j]` 放进哈希表 `prod1`，键是乘积，值是出现次数。  
   - 同理得到 `nums2` 的乘积频率表 `prod2`。  
   - 这里的「哈希表」可以类比成「查字典」：键是「乘积这页的页码」，值是「这页在字典里出现了几次」。

2. **统计匹配的三元组**  
   - 对 `nums1` 中的每个元素 `x`，计算 `x²`。如果 `x²` 在 `prod2` 中出现过 `cnt` 次，那么就说明有 `cnt` 个 `(j, k)` 使得 `nums2[j] * nums2[k] = x²`，于是把 `cnt` 加到答案里。  
   - 同理遍历 `nums2`，用 `prod1` 统计类型 2。

3. **返回答案**。

> **为什么对**  
> - 乘积表里记录的是「所有 unordered pair 的乘积出现次数」。  
> - 每次我们只关心「某个具体的平方」是否等于「某个乘积」——这正好是「查询」哈希表能做到的事，且查询时间是常数 `O(1)`。  
> - 整体只遍历两次数组（一次算乘积，一次查平方），所以时间大幅降低。

**核心数据结构**：哈希表（Python 中的 `dict`），相当于「字典」——查找、插入、更新都是 `O(1)`。

**时间复杂度**  

- 生成乘积表：对每个数组长度为 `n`（或 `m`）的数组，需要遍历所有 unordered 对，复杂度是 `O(n²)`（或 `O(m²)`）。  
- 查找匹配：遍历两个数组各一次，`O(n + m)`。  
- 综合：`O(n² + m²)`，在最坏情况下 `1000² + 1000² = 2,000,000` 次运算，轻松在 1 秒内完成。  

**空间复杂度**  

- 两个哈希表最多各保存 `n·(n‑1)/2`（或 `m·(m‑1)/2`）个不同的乘积键。  
- 这相当于 `O(n² + m²)` 的额外空间，仍然在题目限制内（因为乘积值本身最大是 `10⁵ * 10⁵ = 10¹⁰`，Python 整数可以直接存）。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def numTriplets(nums1: List[int], nums2: List[int]) -> int:
    # ---------- 第一步：统计所有 unordered pair 的乘积 ----------
    def pair_product_counter(arr: List[int]) -> Counter:
        """返回 Counter，其中 key = 两数乘积，value = 出现次数"""
        cnt = Counter()
        n = len(arr)
        for i in range(n):
            a = arr[i]
            for j in range(i + 1, n):
                prod = a * arr[j]               # 计算乘积
                cnt[prod] += 1                  # 哈希表里计数 +1
        return cnt

    prod1 = pair_product_counter(nums1)   # nums1 两数乘积的频率表
    prod2 = pair_product_counter(nums2)   # nums2 两数乘积的频率表

    # ---------- 第二步：统计匹配的三元组 ----------
    ans = 0

    # 类型 1：nums1 中的平方等于 nums2 两数乘积
    for x in nums1:
        sq = x * x                         # 计算平方
        if sq in prod2:                    # 哈希表快速查询
            ans += prod2[sq]               # 累加对应的配对数量

    # 类型 2：nums2 中的平方等于 nums1 两数乘积
    for x in nums2:
        sq = x * x
        if sq in prod1:
            ans += prod1[sq]

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² + m²)`  
  - `n²`、`m²` 分别来自于对 `nums1`、`nums2` 所有 unordered 对的遍历。  
  - 与暴力解相比，省掉了外层的线性遍历，使得整体运算次数从「立方级」下降到「平方级」。

- **空间复杂度**：`O(n² + m²)`  
  - 两个哈希表分别存放所有可能的乘积及其出现次数。  
  - 在最坏情况下（所有乘积都不同）键的数量正好是 `n·(n‑1)/2 + m·(m‑1)/2`，仍然在可接受范围。

---

## 心得

- **核心技巧**：把「两数乘积」预先统计到哈希表，再用「平方」去查询。  
- **适用的题型**  
  1. “两个数的乘积等于第三个数的平方” 类似的计数题（如 LeetCode 1725：`Number Of Rectangles That Can Form The Largest Square` 中的面积计数思路）。  
  2. “两数之和等于目标值” 的变体，只是把求和换成求乘积（可用哈希表存出现次数）。  
- **一句话总结解题钥匙**：**把所有可能的「组合结果」先算好并放进字典，后面只需要 O(1) 查询即可**。

---

## 反思

- **第一反应**：直接写三层循环枚举所有下标，觉得能跑通但不够快。  
- **最容易踩的坑**  
  - **下标顺序**：题目要求的是「两个数的乘积」而不是「有序对」，所以 `(j, k)` 与 `(k, j)` 只算一次；使用 `i < j` 的遍历方式可以自然避免重复计数。  
  - **整数溢出**：在 Python 中不必担心，因为整数是任意精度；但如果换成 C++/Java，需要注意 `int` 可能会 overflow。  
  - **边界情况**：数组长度为 1 时没有配对，返回 0；全部元素相同时乘积会大量重复，哈希表计数必须使用 `+= 1` 而不是 `= 1`。  
- **下次遇到同类题**：第一步先思考「有没有可以一次性预处理的中间结果」——比如「所有 unordered 对的和/积/异或」等；如果能把这些中间结果放进哈希表，后面的匹配步骤往往可以降到 `O(n)`。