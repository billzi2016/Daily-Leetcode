# #3131. 找到添加到数组 I 的整数 / Find the Integer Added to Array I

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/find-the-integer-added-to-array-i/)

---

## 题目（英文原版）

**Description**

You are given two arrays of equal length, nums1 and nums2.
Each element in nums1 has been increased (or decreased in the case of negative) by an integer, represented by the variable x.
As a result, nums1 becomes equal to nums2. Two arrays are considered equal when they contain the same integers with the same frequencies.
Return the integer x.

**Examples**

**Example 1:**

```
Input: nums1 = [2,6,4], nums2 = [9,7,5]
Output: 3
Explanation:
The integer added to each element of nums1 is 3.
```

**Example 2:**

```
Input: nums1 = [10], nums2 = [5]
Output: -5
Explanation:
The integer added to each element of nums1 is -5.
```

**Example 3:**

```
Input: nums1 = [1,1,1,1], nums2 = [1,1,1,1]
Output: 0
Explanation:
The integer added to each element of nums1 is 0.
```

**Constraints**

- 1 <= nums1.length == nums2.length <= 100
- 0 <= nums1[i], nums2[i] <= 1000
- The test cases are generated in a way that there is an integer x such that nums1 can become equal to nums2 by adding x to each element of nums1.

---

## 题目（中文翻译）

给定两个等长的数组 `nums1` 和 `nums2`。  
`nums1` 中的每个元素都被增加了同一个整数（若该整数为负则是减少），该整数用变量 `x` 表示。  
因此，`nums1` 经过此操作后会与 `nums2` 相等。当两个数组包含相同的整数且出现次数相同，即视为相等。  

返回整数 `x`。

**示例 1**

```text
输入: nums1 = [2,6,4], nums2 = [9,7,5]
输出: 3
解释:
添加到 `nums1` 每个元素的整数是 3。
```

**示例 2**

```text
输入: nums1 = [10], nums2 = [5]
输出: -5
解释:
添加到 `nums1` 每个元素的整数是 -5。
```

**示例 3**

```text
输入: nums1 = [1,1,1,1], nums2 = [1,1,1,1]
输出: 0
解释:
添加到 `nums1` 每个元素的整数是 0。
```

**约束条件**

- `1 <= nums1.length == nums2.length <= 100`
- `0 <= nums1[i], nums2[i] <= 1000`
- 测试用例保证存在一个整数 `x`，使得对 `nums1` 的每个元素加上 `x` 后可以变为 `nums2`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的整数 `x`，看哪一个可以让 `nums1` 加上 `x` 后和 `nums2` 完全一样**（顺序不重要，只要出现的数和出现次数相同即可）。

实现步骤：

1. 把 `nums2` 用一个「哈希表」保存起来。哈希表可以类比成一本字典，`key` 是数字本身，`value` 是这个数字在数组中出现的次数。这样我们可以在 **O(1)** 的时间内判断一个数字是否在 `nums2` 中以及它还剩多少次可以匹配。  
2. 对于 `nums1` 中的每个元素 `a`，尝试把它对应到 `nums2` 中的每个元素 `b`（即假设 `x = b - a`）。  
3. 计算得到 `x` 后，把 `nums1` 的每个元素都加上 `x`，再检查加完之后的集合是否和 `nums2` 完全相同（利用哈希表计数）。  
4. 只要有一次检查成功，就返回对应的 `x`。

因为题目保证一定存在唯一的 `x`，所以一定能在所有枚举中找到答案。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def find_x_brute(nums1: List[int], nums2: List[int]) -> int:
    # 统计 nums2 中每个数出现的次数，类似查字典
    cnt2 = Counter(nums2)                 # O(n) 建表

    n = len(nums1)
    # 枚举 nums1 中的每个元素 a 与 nums2 中的每个元素 b 的差值
    for a in nums1:                       # 最外层 O(n)
        for b in nums2:                   # 内层 O(n)
            x = b - a                     # 假设的整数 x
            # 用 Counter 重新计数一次 nums1 加上 x 之后的结果
            transformed = [v + x for v in nums1]   # O(n)
            if Counter(transformed) == cnt2:       # O(n) 比较两个 Counter
                return x
    # 题目保证一定有解，这行理论上不会执行
    raise ValueError("No valid x found")
```

> **关键行解释**  
> - `Counter(nums2)`：把 `nums2` 的每个数字和出现次数放进哈希表，像查字典一样快。  
> - `x = b - a`：假设 `a`（来自 `nums1`）对应到 `b`（来自 `nums2`）时需要的增量。  
> - `Counter(transformed) == cnt2`：把所有加完 `x` 的数重新统计，再和原来的统计表做一次完整比较。

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 两层循环枚举 `a`、`b` → `O(n²)`  
  - 每次都要遍历 `nums1` 生成新数组并计数 → `O(n)`  
  - 所以整体是 `n² * n = n³`。  
  - **大白话**：如果数组长度是 100，最坏情况下要做 1,000,000 次左右的基本操作，已经算是很慢了。

- **空间复杂度**：`O(n)`  
  - 需要额外的哈希表 `cnt2` 与 `transformed`，每个最多保存 `n` 个数字的计数。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于我们穷举了所有可能的 `x`**，而实际上只需要 **一次** 就能算出正确的 `x`。下面给出两种等价且更快的思路，任选其一即可：

1. **排序 + 最小值差**  
   - 把两数组都排个序。排序后，最小的数一定对应最小的数（因为所有数都平移了同一个 `x`），所以  
     `x = min(nums2) - min(nums1)`。  
   - 排序的时间是 `O(n log n)`，但我们只需要一次比较。

2. **利用总和求平均**（更快）  
   - 把 `nums1` 中所有数加上 `x` 后得到 `nums2`，于是  
     `sum(nums2) = sum(nums1) + n * x`，其中 `n` 是数组长度。  
   - 直接求得  
     `x = (sum(nums2) - sum(nums1)) // n`。  
   - 只需要一次遍历就能算出两个数组的总和，时间是 `O(n)`，空间 `O(1)`。

下面用第二种「总和」方法实现，因为它最简洁、最快。

#### 代码（Python）

```python
from typing import List

def find_x(nums1: List[int], nums2: List[int]) -> int:
    """
    只需要一次遍历统计两个数组的总和，然后利用
    sum(nums2) = sum(nums1) + n * x 求出 x。
    时间 O(n)，空间 O(1)。
    """
    n = len(nums1)               # 两数组长度相等
    sum1 = sum(nums1)            # O(n) 统计 nums1 的所有元素之和
    sum2 = sum(nums2)            # O(n) 统计 nums2 的所有元素之和
    x = (sum2 - sum1) // n       # 根据公式直接算出 x
    return x
```

> **关键行解释**  
> - `sum(nums1)` 与 `sum(nums2)`：把数组里所有数字加起来，像把一堆钱放进收银机，一次遍历即可。  
> - `x = (sum2 - sum1) // n`：先算出两总和的差，这个差其实是 `n` 个 `x` 的和，除以 `n` 就得到单个 `x`。  

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历两次数组（一次算 `sum1`，一次算 `sum2`），线性时间。  
  - **大白话**：如果数组有 100 条数据，只需要 200 次加法操作，几乎是瞬间完成。

- **空间复杂度**：`O(1)` — 只用了几个整数变量，不会随输入规模增长而占用更多内存。

---

## 心得

- **核心技巧**：利用**整体属性**（如总和、最小值）一次性求出全局平移量 `x`，而不是逐个枚举。  
- **适用的题型**  
  1. 两个数组只相差一个常数（平移）的问题。  
  2. 需要从整体统计信息（和、均值、最大最小）直接求解的题目，如「找出数组中缺失的数」的变形。  
- **一句话总结解题钥匙**：**把“每个元素都变化了同样的量”转化为“整体变化量除以元素个数”。**

---

## 反思

- **第一反应**：看到“每个元素都加了同一个整数”，立刻想到用 **差值** 或 **总和** 来推算。  
- **最容易踩的坑**  
  - 忘记检查整数除法是否会产生小数（本题保证 `x` 为整数，使用 `//` 安全）。  
  - 对负数的处理不当——这里的公式同样适用于负 `x`，只要用整数除法即可。  
- **下次遇到同类题的第一步**：**先思考是否能把局部的“每个元素的变化”升华为全局的“总和/最小值/最大值的变化”。** 若能，就可以在 O(n) 或 O(n log n) 时间内直接算出答案。