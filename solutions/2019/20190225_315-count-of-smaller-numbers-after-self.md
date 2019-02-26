# #315. 统计自身右侧的更小数字个数 / Count of Smaller Numbers After Self

> 难度：困难 · 标签：Array、Binary Search、Divide and Conquer、Binary Indexed Tree、Segment Tree、Merge Sort、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return an integer array counts where counts[i] is the number of smaller elements to the right of nums[i].

**Examples**

**Example 1:**

```
Input: nums = [5,2,6,1]
Output: [2,1,1,0]
Explanation:
To the right of 5 there are 2 smaller elements (2 and 1).
To the right of 2 there is only 1 smaller element (1).
To the right of 6 there is 1 smaller element (1).
To the right of 1 there is 0 smaller element.
```

**Example 2:**

```
Input: nums = [-1]
Output: [0]
```

**Example 3:**

```
Input: nums = [-1,-1]
Output: [0,0]
```

**Constraints**

- 1 <= nums.length <= 105
- -104 <= nums[i] <= 104

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`，返回一个整数数组 `counts`，其中 `counts[i]` 表示在 `nums[i]` 右侧（即下标大于 `i` 的位置）比 `nums[i]` 更小的元素个数。

**约束**  
- `1 <= nums.length <= 10^5`  
- `-10^4 <= nums[i] <= 10^4`

**示例**

**示例 1**  
```
Input: nums = [5,2,6,1]
Output: [2,1,1,0]
Explanation:
在 5 的右侧有 2 个更小的元素（2 和 1）。
在 2 的右侧只有 1 个更小的元素（1）。
在 6 的右侧有 1 个更小的元素（1）。
在 1 的右侧没有更小的元素。
```

**示例 2**  
```
Input: nums = [-1]
Output: [0]
Explanation:
唯一的元素左侧没有其他元素，所以更小的元素个数为 0。
```

**示例 3**  
```
Input: nums = [-1,-1]
Output: [0,0]
Explanation:
两个相同的元素互相之间不构成“更小”，因此每个位置右侧的更小元素个数均为 0。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**对每一个位置 i，往右扫描所有元素，统计比 `nums[i]` 小的个数**。  
这和我们平时数数的方式一样：把左边的数字想成“我”，右边的数字想成“一堆小伙伴”，逐个比较谁更小。

- **用到的数据结构**：只需要一个普通的 Python 列表 `counts` 来保存答案，遍历时再用 `for` 循环访问 `nums`。不需要任何高级结构。
- **为什么正确**：因为我们真的把每个元素右边的所有数都检查了一遍，只要比它小就计数，结果自然就是题目要求的“右侧更小的个数”。  
- **复杂度分析**：  
  - 外层循环遍历 `n` 次，内层循环对每个位置最多再遍历 `n‑1` 次，时间大约是 `n × n`，记作 **O(n²)**。这里的 “O” 表示“数量级”，也就是说当 `n` 翻倍，时间大约会增加四倍。  
  - 只用了一个长度为 `n` 的额外数组 `counts`，空间是 **O(n)**。

#### 代码（Python）

```python
def count_smaller_bruteforce(nums):
    n = len(nums)
    counts = [0] * n                     # 用来存放答案，初始全为 0
    for i in range(n):                   # 对每个位置 i
        cnt = 0
        for j in range(i + 1, n):        # 看看它右边的每个位置 j
            if nums[j] < nums[i]:        # 如果右边的数更小，就计数
                cnt += 1
        counts[i] = cnt                   # 把计数结果写进答案数组
    return counts
```

#### 复杂度

- **时间复杂度**：O(n²)  
  > 例如 `n = 10⁴` 时，大约需要 10⁸ 次比较，计算机会明显卡顿。
- **空间复杂度**：O(n)  
  > 只多开了一个和原数组等长的列表来保存结果。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每次都把右边的全部元素重新遍历一遍”**，这导致二次方的时间。  
如果我们能够在 **一次遍历**（或 **log 次遍历**）中就知道右侧有多少更小的数，时间就可以大幅下降。

一种常用的技巧是 **“归并排序 + 计数”**（也叫 **逆序对计数** 的变形）：

1. **归并排序的核心**：把数组不断拆成左右两半，递归排序后再把两段合并。合并时把较小的数先放到结果里，这保证了合并后的序列是有序的。  
2. **计数的关键**：在合并的过程中，左段的某个元素 `L` 要放进结果时，如果右段的指针已经提前把若干个更小的数 `R` 放进来了，说明这 `R` 个数在原数组里 **都在 `L` 的右侧且比 `L` 小**。于是我们可以把这 `R` 的数量加到 `L` 对应位置的答案里。  
3. 为了在合并后仍然能把答案对应回原来的下标，我们在递归时 **把每个元素包装成 `(value, index)`**，这样即使排序后位置改变，也能通过 `index` 把计数写回正确的答案位置。

> **类比**：想象有两排学生站好，左排是“原来的顺序”，右排是“已经排好序的顺序”。我们把左排的学生逐个让位给右排更矮的学生。每当左排的学生让位时，记下右排已经让位的学生数，这就是他右侧更小的同学数。

**步骤概览**  

| 步骤 | 说明 |
|------|------|
| ① 将 `nums` 转成 `enum = [(val, idx)]` | 保存原始下标 |
| ② 调用 `merge_sort(enum, 0, n‑1)` | 递归排序并计数 |
| ③ 在 `merge` 时统计右侧更小的数量并写入 `result[idx]` | 关键计数步骤 |
| ④ 最终返回 `result` | 完成 |

#### 代码（Python）

```python
def count_smaller(nums):
    """
    使用归并排序的思路，在 O(n log n) 时间内求每个位置右侧比自己小的元素个数。
    """
    n = len(nums)
    # result[i] 最终保存答案
    result = [0] * n

    # 把每个元素和它原来的下标打包，方便在排序后仍能找到对应位置
    enum = [(num, i) for i, num in enumerate(nums)]

    def merge_sort(arr):
        """对 arr 进行归并排序，同时更新 result 中的计数"""
        mid = len(arr) // 2
        if mid:
            left = merge_sort(arr[:mid])   # 排序左半边
            right = merge_sort(arr[mid:])  # 排序右半边
            # 合并过程，同时统计右侧更小的数
            i = j = 0
            merged = []
            # 当左侧元素小于等于右侧元素时，左侧元素先出列
            while i < len(left) and j < len(right):
                if left[i][0] <= right[j][0]:
                    # left[i] 前面已经有 j 个右侧更小的元素
                    result[left[i][1]] += j
                    merged.append(left[i])
                    i += 1
                else:
                    # right[j] 更小，直接放进结果，不影响左侧计数
                    merged.append(right[j])
                    j += 1
            # 处理剩余的左侧元素
            while i < len(left):
                result[left[i][1]] += j   # 此时右侧已经全部合并完，j 就是右侧更小的总数
                merged.append(left[i])
                i += 1
            # 处理剩余的右侧元素（不需要计数）
            merged.extend(right[j:])
            return merged
        else:
            # 长度为 1 的子数组本身已经有序
            return arr

    merge_sort(enum)
    return result
```

> **代码要点解释**  
> - `enum = [(num, i) for i, num in enumerate(nums)]`：把值和原下标配对，类似把每本书的标题和它在原书架上的位置记下来。  
> - `result[left[i][1]] += j`：`j` 表示已经从右侧取走、且比当前左侧元素小的数的个数，正好是我们要加的“右侧更小的元素”。  
> - 递归的基线是子数组长度为 1（`if mid:`），此时不需要再拆分，直接返回。

#### 复杂度

- **时间复杂度**：O(n log n)  
  > 归并排序本身就是 `n log n`，在合并时我们只做了常数次的额外操作（加计数），所以整体仍保持 `n log n`。相较于暴力的 O(n²)，当 `n = 10⁵` 时运行时间会从几分钟降到几百毫秒。
- **空间复杂度**：O(n)  
  > 归并排序需要额外的临时数组来存放合并后的结果，这里用了和原数组等长的列表 `enum`（以及递归栈的深度 `log n`），整体是线性空间。

---

## 心得

- **核心技巧**：在排序的过程中**同步计数**（归并排序计数）或使用**树状数组 / 有序集合**。本题用归并排序实现，思路清晰且易于手写。
- **适用的题型**  
  1. **逆序对计数**（LeetCode 493 Reverse Pairs）  
  2. **求区间中位数/第 k 大元素**（需要有序结构的题目）  
  3. **统计区间中小于/大于某值的个数**（如“数组中出现次数大于 K 的元素”）
- **一句话总结**：把“右侧更小的数”看作“在归并时被右边抢先放走的元素”，合并的瞬间就能把答案记下来。

---

## 反思

- **第一反应**：直接想到两层循环遍历右侧，写出暴力解。  
- **最容易踩的坑**  
  - **边界条件**：空数组或长度为 1 时直接返回 `[0]`（归并实现自然兼容）。  
  - **相等元素的处理**：题目要求“更小”，所以在合并时 `<=` 放左侧，确保相等的元素不计入“更小”。  
  - **下标混乱**：排序后元素位置变化，若不保存原下标会把计数写到错误的位置。  
- **下次遇到同类题的第一步**：先思考“能不能在已有的 O(n log n) 排序/树结构里把计数顺带做了”，如果答案是“可以”，就尝试把计数嵌入到排序或查询过程，而不是再套一层遍历。