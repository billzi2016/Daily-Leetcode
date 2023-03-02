# #2148. 计数同时存在严格更小和严格更大元素的数组元素 / Count Elements With Strictly Smaller and Greater Elements 

> 难度：简单 · 标签：Array、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/count-elements-with-strictly-smaller-and-greater-elements/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return the number of elements that have both a strictly smaller and a strictly greater element appear in nums.

**Examples**

**Example 1:**

```
Input: nums = [11,7,2,15]
Output: 2
Explanation: The element 7 has the element 2 strictly smaller than it and the element 11 strictly greater than it.
Element 11 has element 7 strictly smaller than it and element 15 strictly greater than it.
In total there are 2 elements having both a strictly smaller and a strictly greater element appear in nums.
```

**Example 2:**

```
Input: nums = [-3,3,3,90]
Output: 2
Explanation: The element 3 has the element -3 strictly smaller than it and the element 90 strictly greater than it.
Since there are two elements with the value 3, in total there are 2 elements having both a strictly smaller and a strictly greater element appear in nums.
```

**Constraints**

- 1 <= nums.length <= 100
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，返回 `nums` 中满足 **同时** 存在一个 **严格更小**（strictly smaller）和一个 **严格更大**（strictly greater）元素的元素个数。

---

### 示例

#### 示例 1
**输入**：`nums = [11,7,2,15]`  
**输出**：`2`  
**解释**：元素 `7` 的左侧存在元素 `2` 严格更小，且右侧存在元素 `11` 严格更大。  
元素 `11` 的左侧存在元素 `7` 严格更小，且右侧存在元素 `15` 严格更大。  
因此，总共有 2 个元素同时满足上述条件。

#### 示例 2
**输入**：`nums = [-3,3,3,90]`  
**输出**：`2`  
**解释**：元素 `3` 的左侧存在元素 `-3` 严格更小，右侧存在元素 `90` 严格更大。  
由于数组中有两个值为 `3` 的元素，故一共计数为 2。

---

### 约束条件
- `1 <= nums.length <= 100`
- `-10^5 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对数组里的每一个元素 `x`，分别检查是否存在比 `x` 小的数和比 `x` 大的数**。  
- 我们可以用两层循环：外层遍历每个 `x`，内层把 `x` 和其它所有元素两两比较。  
- 只要在内层找到一次 `y < x`（更小的）和一次 `z > x`（更大），就把 `x` 计入答案。  

> **类比**：把数组想象成一排学生的身高，暴力做法就是让每个学生去“和全班每个人比身高”，只要找到了既比他矮也比他高的同学，就算他符合条件。

这种方法一定能得到正确答案，因为我们把所有可能的“更小”和“更大”都检查了一遍。

#### 代码（Python）

```python
def countElements(nums):
    """
    暴力解：对每个元素都遍历整个数组，检查是否存在更小和更大的元素。
    """
    n = len(nums)
    ans = 0

    for i in range(n):                     # 外层：选定当前元素 nums[i]
        has_smaller = False                # 标记是否找到更小的元素
        has_greater = False                # 标记是否找到更大的元素

        for j in range(n):                 # 内层：与所有元素比较
            if nums[j] < nums[i]:          # 找到更小的
                has_smaller = True
            if nums[j] > nums[i]:          # 找到更大的
                has_greater = True

            # 两个标记都满足时，提前结束内层循环，节省一点时间
            if has_smaller and has_greater:
                break

        if has_smaller and has_greater:    # 当前元素满足题意
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - `n` 是数组长度。外层遍历 `n` 次，内层最坏也要遍历 `n` 次，所以总共是 `n × n`。  
  - 大白话：如果数组有 100 个数，最坏情况下要比较 100 × 100 = 10 000 次。

- **空间复杂度**：`O(1)`。只用了常数个额外变量 (`ans、has_smaller、has_greater`)。

---

### 2. 最优解

#### 思路  

观察题目可以发现：**只要元素不是全局最小值，也不是全局最大值，就一定同时拥有比它更小和更大的元素**。  
换句话说，**答案等于“数组总长度”减去“最小值出现的次数”再减去“最大值出现的次数”。**  

因此我们只需要：

1. **一次遍历**找出数组的最小值 `min_val`、最大值 `max_val`，并统计它们各自出现的次数 `cnt_min`、`cnt_max`。  
2. 如果 `min_val == max_val`（所有元素相同），显然没有任何元素既有更小也有更大，答案直接返回 `0`。  
3. 否则，答案 = `len(nums) - cnt_min - cnt_max`。  

> **类比**：把数组看成一盒糖果，最小味道的糖和最大味道的糖是“特殊的”。只要不是这两种特殊糖，其他糖自然就有比它更淡也有更浓的糖存在。

这个思路把 **两层循环** 的 `O(n²)` 降到了 **一次线性扫描** 的 `O(n)`，并且只用了几个整数变量（`O(1)` 额外空间）。

> **为什么公式 `n - count(min) - count(max)` 在“全相等”时失效？**  
> 当所有元素相等时，最小值和最大值其实是同一个数。此时 `count(min) == count(max) == n`，公式会算成 `n - n - n = -n`，显然不对。我们必须先判断 `min == max`，如果相等直接返回 `0`。

#### 代码（Python）

```python
def countElements(nums):
    """
    最优解：只需一次遍历统计最小值、最大值及其出现次数。
    时间 O(n)，空间 O(1)。
    """
    n = len(nums)
    if n == 0:
        return 0

    # 第一次遍历：找出最小值和最大值
    min_val = max_val = nums[0]
    for x in nums[1:]:
        if x < min_val:
            min_val = x
        elif x > max_val:
            max_val = x

    # 如果最小值等于最大值，说明所有元素相等，没有符合条件的元素
    if min_val == max_val:
        return 0

    # 第二次遍历：统计最小值和最大值各出现了多少次
    cnt_min = cnt_max = 0
    for x in nums:
        if x == min_val:
            cnt_min += 1
        elif x == max_val:
            cnt_max += 1

    # 其余的元素全部满足题意
    return n - cnt_min - cnt_max
```

> 也可以把找最小/最大值和计数合并到一次遍历里，只要在更新 `min_val`/`max_val` 时同步重置计数即可，仍然是 `O(n)`。

#### 复杂度  

- **时间复杂度**：`O(n)`。只遍历数组常数次，`n` 是数组长度。  
  - 与暴力解相比，时间从“每两个元素都要比较一次”降到“每个元素只看一次”。  

- **空间复杂度**：`O(1)`。只用了几个整数变量 (`min_val、max_val、cnt_min、cnt_max`)。

---

## 心得

- **核心技巧**：利用全局极值（最小值、最大值）把“局部是否存在更小/更大”转化为“是否是极值”。  
- **适用的题型**  
  1. *Count Elements With Strictly Smaller and Greater Elements*（本题）  
  2. *Remove Minimum and Maximum Elements*（求去掉极值后的统计）  
  3. *Number of Elements Greater Than Minimum*（统计比最小值大的元素个数）  
- **一句话总结**：只要不是最小或最大，就一定同时拥有更小和更大的伙伴——把问题简化为“除去极值”。

---

## 反思

- **第一反应**：对每个数遍历整个数组，逐个检查是否有更小/更大的元素（暴力法）。  
- **最容易踩的坑**  
  - **全相等的数组**：最小值等于最大值，需要单独处理，否则公式会出现负数。  
  - **最小值/最大值出现多次**：不能只减去 `1`，要减去它们各自的出现次数。  
  - **空数组或长度为 1 的情况**：虽然题目保证长度 ≥ 1，但写代码时仍需防止除零或索引错误。  
- **下次遇到同类题**：第一步先思考“有没有全局信息（最值、总和、前缀和）可以一次遍历得到”，再决定是否需要排序或使用哈希表。这样往往能直接把 `O(n²)` 降到 `O(n)` 或 `O(n log n)`。