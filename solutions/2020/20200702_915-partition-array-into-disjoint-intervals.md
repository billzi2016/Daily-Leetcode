# #915. 划分数组为不相交区间 / Partition Array into Disjoint Intervals

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/partition-array-into-disjoint-intervals/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, partition it into two (contiguous) subarrays left and right so that:
Return the length of left after such a partitioning.
Test cases are generated such that partitioning exists.

**Examples**

**Example 1:**

```
Input: nums = [5,0,3,8,6]
Output: 3
Explanation: left = [5,0,3], right = [8,6]
```

**Example 2:**

```
Input: nums = [1,1,1,0,6,12]
Output: 4
Explanation: left = [1,1,1,0], right = [6,12]
```

**Constraints**

- 2 <= nums.length <= 105
- 0 <= nums[i] <= 106
- There is at least one valid answer for the given input.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，将其划分为两个（连续的）子数组 `left` 和 `right`，满足题目要求。返回划分后 `left` 的长度。题目保证一定存在合法的划分。

示例 1:
```
Input: nums = [5,0,3,8,6]
Output: 3
Explanation: left = [5,0,3], right = [8,6]
```
解释：左子数组 = [5,0,3]，右子数组 = [8,6]

示例 2:
```
Input: nums = [1,1,1,0,6,12]
Output: 4
Explanation: left = [1,1,1,0], right = [6,12]
```
解释：左子数组 = [1,1,1,0]，右子数组 = [6,12]

约束条件：
- 2 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^6
- 至少存在一个有效的答案。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的切分位置**，然后检查切分后左边子数组的最大值是否不大于右边子数组的最小值。  
- **数据结构**：我们只需要普通的 Python 列表 `nums`。在检验每一个切分点时，需要遍历左子数组求最大值，遍历右子数组求最小值。可以把“求最大值”想象成在一堆水果里挑出最大的一颗，“求最小值”则像在另一堆水果里挑出最小的一颗。
- **正确性**：如果左子数组的最大值 `max_left` ≤ 右子数组的最小值 `min_right`，则左子数组的所有元素都不大于右子数组的任何元素，满足题目要求。我们只要找到最左边的满足条件的切分点，返回左子数组的长度即可。

#### 代码（Python）

```python
def partition_disjoint_bruteforce(nums):
    n = len(nums)
    # i 表示左子数组的最后一个下标，切分点在 i+1
    for i in range(1, n):                 # 至少保留一个元素在右边
        max_left = max(nums[:i])          # 左边最大值（遍历左子数组）
        min_right = min(nums[i:])         # 右边最小值（遍历右子数组）
        if max_left <= min_right:         # 条件满足，返回左子数组长度
            return i
    # 题目保证一定有解，这里永远不会到达
    return n
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环遍历 `n‑1` 个切分点；每一次循环里要分别遍历左子数组和右子数组求最大/最小，最坏情况下需要遍历 `O(n)` 次。因此总体是 `O(n·n) = O(n²)`。  
  - 用大白话说，就是“每次都要把所有水果重新挑一遍”，随着水果数量增加，工作量会呈平方增长，稍大点的数据会很慢。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`max_left`、`min_right`、循环计数器），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次切分都要重新遍历子数组**。我们可以把这些遍历的结果提前算好，省掉重复劳动。

1. **前缀最大**  
   - 对每个下标 `i`，记录从数组开头到 `i` 的最大值。  
   - 类比：把从左往右的水果装进一个盒子，盒子里始终保留到目前为止最大的水果。这样我们随时能在 **O(1)** 时间得到左边子数组的最大值。

2. **后缀最小**  
   - 对每个下标 `i`，记录从 `i` 到数组末尾的最小值。  
   - 类比：把从右往左的水果装进另一个盒子，盒子里始终保留到目前为止最小的水果。这样我们随时能在 **O(1)** 时间得到右边子数组的最小值。

3. **一次遍历找切点**  
   - 从左到右检查第一个满足 `prefix_max[i] ≤ suffix_min[i+1]` 的位置 `i`。  
   - 此时左子数组是 `nums[0…i]`，右子数组是 `nums[i+1…]`，恰好满足题目要求，且 `i` 是最左的合法切点，返回 `i+1`（左子数组长度）。

**实现细节**  
- 可以一次遍历计算 `prefix_max`（直接在原数组上累积），再一次逆向遍历计算 `suffix_min`（存进额外数组 `right_min`），最后一次遍历找切点。  
- 也可以进一步把 `suffix_min` 的存储压缩到 **O(1)** 空间：在遍历时维护一个变量 `min_right`，从左到右更新 `max_left`，并在每一步判断 `max_left ≤ min_right` 是否成立。这里的 `min_right` 实际上是所有 **右边** 元素的最小值的滚动记录。

下面给出两种实现：**O(n) 时间 + O(n) 额外空间**（更直观）和 **O(n) 时间 + O(1) 额外空间**（最省内存）。

#### 代码（Python）

**方案一：前缀最大 + 后缀最小（O(n) 额外空间）**

```python
def partition_disjoint(nums):
    n = len(nums)

    # 1) 前缀最大数组：pre_max[i] = max(nums[0..i])
    pre_max = [0] * n
    cur_max = nums[0]
    for i in range(n):
        cur_max = max(cur_max, nums[i])
        pre_max[i] = cur_max          # 记录到 i 为止的最大值

    # 2) 后缀最小数组：suf_min[i] = min(nums[i..n-1])
    suf_min = [0] * n
    cur_min = nums[-1]
    for i in range(n - 1, -1, -1):
        cur_min = min(cur_min, nums[i])
        suf_min[i] = cur_min          # 记录从 i 开始的最小值

    # 3) 找到最左的切点，使 pre_max[i] <= suf_min[i+1]
    for i in range(n - 1):            # 切点左边至少有一个元素
        if pre_max[i] <= suf_min[i + 1]:
            return i + 1              # 左子数组长度
    return n                          # 题目保证一定能找到，这行不会执行
```

**方案二：一次遍历 O(1) 空间（更高效）**

```python
def partition_disjoint_opt(nums):
    # max_left: 当前左边子数组的最大值（从左往右累积）
    # max_sofar: 全局最大值，用来决定左子数组需要扩展到哪里
    # ans: 当前左子数组的长度（最左合法切点+1）
    max_left = nums[0]
    max_sofar = nums[0]
    ans = 1

    for i in range(1, len(nums)):
        max_sofar = max(max_sofar, nums[i])   # 到 i 为止的全局最大值
        if nums[i] < max_left:                # 当前元素比左边最大值小，说明左子数组必须扩展到 i
            max_left = max_sofar              # 把左子数组的最大值更新为全局最大值
            ans = i + 1                       # 左子数组长度随之扩大
        # else: nums[i] >= max_left，切点仍然可以保持在 ans-1 位置
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了数组常数次（一次或两次），每一步都是常数操作。用大白话说，就是“每个水果只检查一次”，即使有 10⁵ 个水果也能在毫秒级完成。

- **空间复杂度**：  
  - **方案一**：`O(n)` 额外空间，用来存 `pre_max`、`suf_min` 两个长度为 `n` 的数组。  
  - **方案二**：`O(1)` 额外空间，只用了几个整型变量。相比暴力解省掉了大量内存，尤其在 `n` 很大时优势明显。

---

## 心得

- **核心技巧**：利用**前缀最大**和**后缀最小**的预处理（或单遍滚动维护）把“每次都重新遍历子数组”转化为“一次遍历即可得到答案”。这是一类“**单调性**”题目的常用手法。
- **适用的题型**  
  1. **划分数组，使左边所有元素 ≤ 右边所有元素**（本题）。  
  2. **寻找最长的子数组，使其内部满足某种单调关系**（如 LeetCode 1004 “最长连续递增序列”）。  
  3. **前缀和 / 前缀最大与后缀最小结合的区间划分**（如 “分割数组的最大子数组和”）。
- **一句话总结**：**“把局部信息（左侧最大、右侧最小）提前算好或滚动维护，就能一次遍历找出合法切点。”**

---

## 反思

- **第一反应**：看到“把数组分成两段，左边所有数不大于右边所有数”，立刻想到枚举切点并逐段比较——这就是暴力解的雏形。
- **最容易踩的坑**  
  1. **切点的边界**：左子数组必须至少有一个元素，右子数组也必须至少有一个元素，切记循环范围 `i in range(1, n)`（或 `i in range(n-1)`）。  
  2. **全局最大值的更新**：在 O(1) 空间方案中，需要维护一个 `max_sofar`，否则在左子数组扩展时会遗漏之前出现的更大数。  
  3. **返回左子数组长度**：返回的是切点左侧的元素个数，即 `i+1`，不要把下标误写成长度。
- **下次遇到同类题的第一步**：先判断**单调性**（是否可以用“最大/最小随位置单调变化”），然后考虑**前缀/后缀预处理**或**滚动维护**，把重复遍历的成本降到 `O(1)`。这样往往能直接得到 `O(n)` 的最优解。