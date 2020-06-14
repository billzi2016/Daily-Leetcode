# #896. 单调数组 / Monotonic Array

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/monotonic-array/)

---

## 题目（英文原版）

**Description**

An array is monotonic if it is either monotone increasing or monotone decreasing.
An array nums is monotone increasing if for all i <= j, nums[i] <= nums[j]. An array nums is monotone decreasing if for all i <= j, nums[i] >= nums[j].
Given an integer array nums, return true if the given array is monotonic, or false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,3]
Output: true
```

**Example 2:**

```
Input: nums = [6,5,4,4]
Output: true
```

**Example 3:**

```
Input: nums = [1,3,2]
Output: false
```

**Constraints**

- 1 <= nums.length <= 105
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

如果一个数组要么是单调递增（monotone increasing），要么是单调递减（monotone decreasing），则称该数组为单调（monotonic）数组。

当对所有 **i ≤ j**，满足 `nums[i] ≤ nums[j]` 时，数组 `nums` 为单调递增（monotone increasing）。  
当对所有 **i ≤ j**，满足 `nums[i] ≥ nums[j]` 时，数组 `nums` 为单调递减（monotone decreasing）。

给定整数数组 `nums`，如果该数组是单调（monotonic）的则返回 `true`，否则返回 `false`。

**示例 1**  
Input: `nums = [1,2,2,3]`  
Output: `true`

**示例 2**  
Input: `nums = [6,5,4,4]`  
Output: `true`

**示例 3**  
Input: `nums = [1,3,2]`  
Output: `false`

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `-10^5 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把数组里每一对元素都拿出来比较一次：  
- 对于 **单调递增**，要保证 `nums[i] <= nums[j]` 对所有 `i ≤ j` 成立。  
- 对于 **单调递减**，要保证 `nums[i] >= nums[j]` 对所有 `i ≤ j` 成立。  

这相当于把数组当成一本字典，**每个词（下标）都要去查它后面所有词的“大小关系”**，类似于把每本书的每一页都翻遍检查顺序。  

只要我们遍历所有可能的 `(i, j)` 对，分别判断两种单调性是否被破坏，就能得到答案。  

> **为什么正确**  
> 如果在所有 `i ≤ j` 的组合里都没有出现 “前面的数比后面的数大（递增情况）” 或 “前面的数比后面的数小（递减情况）”，说明数组满足对应的单调定义；只要其中一种成立，题目要求的“单调数组”就为 `True`。

#### 代码（Python）  
```python
def isMonotonic_brute(nums):
    n = len(nums)
    # 假设数组既可能是递增，也可能是递减
    inc = True   # 递增标记
    dec = True   # 递减标记

    # 双层循环，枚举所有 i <= j 的组合
    for i in range(n):
        for j in range(i, n):
            if nums[i] > nums[j]:      # 发现一次递增被破坏
                inc = False
            if nums[i] < nums[j]:      # 发现一次递减被破坏
                dec = False

            # 只要两种标记都已经变 False，就可以提前结束循环
            if not inc and not dec:
                return False

    # 只要还有一种标记为 True，就说明数组是单调的
    return True
```

#### 复杂度  
- **时间复杂度：** `O(n²)`  
  - “二次方”意思是如果数组长度是 `n`，我们大概要比较 `n × n` 次。比如 `n=10⁴` 时，需要检查约 `10⁸` 次，计算量会明显变慢。  
- **空间复杂度：** `O(1)`  
  - 只用了几个布尔变量，和数组大小无关，几乎不占额外空间。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于大量重复比较**。  
实际上，只要把 **相邻元素** 的大小关系检查一遍，就能判断整个数组的单调性，因为：

- 若数组是递增的，则每两个相邻数 `nums[i] ≤ nums[i+1]` 必然成立，进而所有 `i ≤ j` 的关系自然成立。  
- 若数组是递减的，则每两个相邻数 `nums[i] ≥ nums[i+1]` 必然成立，同理得到整体递减。  

所以我们只需要一次线性遍历，记录下是否出现过“上升”和“下降”这两种“方向”。  
- 初始时我们假设两种方向都可能（`inc = True, dec = True`）。  
- 遍历时，若发现 `nums[i] > nums[i+1]`，说明数组**不可能是递增**，把 `inc` 设为 `False`。  
- 若发现 `nums[i] < nums[i+1]`，说明数组**不可能是递减**，把 `dec` 设为 `False`。  
- 当两者都为 `False` 时，说明既不是递增也不是递减，直接返回 `False`，否则遍历结束后返回 `True`。

> **核心概念——双指针（相邻比较）**  
> 这里的“双指针”指的是我们用两个下标 `i` 与 `i+1` 同时前进，像走路时左脚、右脚交替着踏在地面上，只检查相邻的两步是否符合方向。

#### 代码（Python）  
```python
def isMonotonic(nums):
    """
    判断数组是否单调（递增或递减）。
    只需要一次遍历，时间 O(n)，空间 O(1)。
    """
    inc = True   # 仍有可能是递增
    dec = True   # 仍有可能是递减

    # 只需要比较相邻的元素
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:   # 出现一次下降
            inc = False            # 递增被破坏
        if nums[i] < nums[i + 1]:   # 出现一次上升
            dec = False            # 递减被破坏

        # 两种可能都被否定，直接返回 False
        if not inc and not dec:
            return False

    # 循环结束后，仍保留一种可能，则数组单调
    return True
```

#### 复杂度  
- **时间复杂度：** `O(n)` — 只遍历一次，`n` 是数组长度。对比暴力的 `n²`，相当于把“每本书的每一页都翻遍”简化为“只翻一次”。  
- **空间复杂度：** `O(1)` — 只用了常数个布尔变量，和 `n` 没有关系。

---

## 心得  

- **核心技巧**：一次遍历同时维护“是否还能是递增”和“是否还能是递减”。  
- **适用的题型**  
  1. 判断数组是否已排序（LeetCode 896）。  
  2. 判断字符串是否满足字典序单调（类似的字符数组题）。  
  3. 判断股票价格序列是否单调上涨/下跌（面试常见变体）。  
- **一句话总结解题钥匙**：**只要相邻元素的方向不冲突，整体就单调**。

## 反思  

- **第一反应**：直接想“把所有对比都算一遍”，于是写出了 O(n²) 的暴力代码。  
- **最容易踩的坑**  
  - 忘记处理 **长度为 1** 的数组——此时既是递增也是递减，直接返回 `True`。  
  - 只检查递增或只检查递减，导致遗漏了另一种可能。  
  - 在遍历时忘记 `i+1` 越界，需要遍历到 `len(nums)-2` 为止。  
- **下次类似题的第一步**：先思考“是否只需要看相邻元素的关系”，如果答案是“是”，就立刻写出一次遍历的双向标记方案。