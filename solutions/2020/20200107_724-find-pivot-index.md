# #724. 寻找枢轴下标 / Find Pivot Index

> 难度：简单 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-pivot-index/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums, calculate the pivot index of this array.
The pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right.
If the index is on the left edge of the array, then the left sum is 0 because there are no elements to the left. This also applies to the right edge of the array.
Return the leftmost pivot index. If no such index exists, return -1.
Note: This question is the same as 1991: https://leetcode.com/problems/find-the-middle-index-in-array/

**Examples**

**Example 1:**

```
Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
The pivot index is 3.
Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
Right sum = nums[4] + nums[5] = 5 + 6 = 11
```

**Example 2:**

```
Input: nums = [1,2,3]
Output: -1
Explanation:
There is no index that satisfies the conditions in the problem statement.
```

**Example 3:**

```
Input: nums = [2,1,-1]
Output: 0
Explanation:
The pivot index is 0.
Left sum = 0 (no elements to the left of index 0)
Right sum = nums[1] + nums[2] = 1 + -1 = 0
```

**Constraints**

- 1 <= nums.length <= 104
- -1000 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个整数数组（array）`nums`，计算该数组的枢轴下标（pivot index）。  
枢轴下标是指满足 **左侧所有元素的和**（left sum）**恰好等于右侧所有元素的和**（right sum）的下标。  

- 若下标位于数组的最左侧，则左侧和为 0，因为左侧没有元素；右侧同理。
- 返回最左侧满足条件的枢轴下标。如果不存在满足条件的下标，返回 `-1`。

> **注意**：本题与 1991 题相同，链接：https://leetcode.com/problems/find-the-middle-index-in-array/

### 示例

**示例 1**  
```
Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
枢轴下标是 3。
左侧和 = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
右侧和 = nums[4] + nums[5] = 5 + 6 = 11
```

**示例 2**  
```
Input: nums = [1,2,3]
Output: -1
Explanation:
不存在满足题目条件的下标。
```

**示例 3**  
```
Input: nums = [2,1,-1]
Output: 0
Explanation:
枢轴下标是 0。
左侧和 = 0（下标 0 左侧没有元素）
右侧和 = nums[1] + nums[2] = 1 + -1 = 0
```

### 约束条件

- `1 <= nums.length <= 10^4`
- `-1000 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个位置 i，都分别算出左边所有数的和、右边所有数的和，然后比较是否相等**。  
- 为了得到左侧和，我们可以从 `0` 累加到 `i‑1`；右侧和则是从 `i+1` 累加到数组末尾。  
- 这里用到的“数组求和”就像我们在生活中数钱：把左边所有硬币放一起算总额，把右边的也一样。  

这种做法一定能找到答案，因为我们穷举了所有可能的“枢轴”。如果某个位置满足左、右和相等，我们立刻返回它；遍历完都没有找到，就返回 `-1`。

#### 代码（Python）

```python
def pivotIndex_brute(nums):
    """
    暴力解法：对每个下标 i，分别计算左侧和右侧的总和
    """
    n = len(nums)
    for i in range(n):
        # 左侧 sum：从 0 加到 i-1
        left_sum = sum(nums[:i])          # 切片会生成新列表，随后求和
        # 右侧 sum：从 i+1 加到末尾
        right_sum = sum(nums[i+1:])       
        # 如果相等，返回当前下标
        if left_sum == right_sum:
            return i
    # 没有符合条件的下标
    return -1
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 对每个 `i`（共 `n` 次）我们都要遍历一次左边和一次右边的元素，最坏情况下每次遍历约 `n/2`，于是总操作数大约是 `n × n/2 ≈ n²`。  
  - 用大白话说，就是“如果数组有 1000 个数，最坏要算 1 000 000 次加法”，这在实际运行时会慢。

- **空间复杂度：** `O(1)`（不计切片产生的临时列表）  
  - 我们只用了常数级别的额外变量 `left_sum`、`right_sum`、`i`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历左侧和右侧**。我们可以利用**前缀和（Prefix Sum）**的思想，把重复的计算“搬到”一次遍历里完成。

1. **先算出整个数组的总和** `total`。  
2. **维护一个变量 `left_sum`，记录当前下标左边所有数的和**。遍历数组时，`left_sum` 可以在 O(1) 时间内更新：  
   - 当我们站在下标 `i` 时，左侧和已经在 `left_sum` 中。  
   - 右侧和则是 `total - left_sum - nums[i]`（总和减去左侧和和当前元素，就是右侧的和）。  
3. 检查 `left_sum == right_sum`，若相等则返回 `i`。  
4. 若遍历结束仍未找到，返回 `-1`。  

**类比**：想象你在走一条路，两边都有钱袋子。你手里记着左边已经捡到的钱（`left_sum`），路上总共有多少钱（`total`），所以右边还剩多少钱只要用总额减去左边和当前手里这袋子即可。

#### 代码（Python）

```python
def pivotIndex(nums):
    """
    最优解：一次遍历 + 前缀和
    """
    total = sum(nums)      # 整个数组的总和
    left_sum = 0           # 左侧累计和，初始为 0（左边没有元素）

    for i, x in enumerate(nums):
        # 此时的 right_sum = total - left_sum - x
        if left_sum == total - left_sum - x:
            return i       # 找到最左侧的枢轴下标
        left_sum += x      # 把当前元素加入左侧和，为下一个位置做准备
    return -1               # 没有符合条件的下标
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次数组，每个元素做常数次加减操作。  
  - 用大白话说，“如果有 1000 个数，只需要算 1000 次加法”，比暴力的 1 000 000 次快很多。

- **空间复杂度：** `O(1)`  
  - 只用了 `total`、`left_sum`、`i`、`x` 四个变量，和输入规模无关。

---

## 心得

- **核心技巧**：前缀和（Prefix Sum）——把“左边的累计”和“右边的累计”通过一次遍历同时维护。  
- **适用的题型**  
  1. “子数组和等于 K” 之类的区间求和问题（常用哈希表 + 前缀和）。  
  2. “最长连续子数组满足条件”——利用前缀和转化为差值比较。  
  3. “数组分割点”或“平衡点”类题目（如本题）。  
- **一句话总结**：**把全局信息（总和）和局部信息（左侧累计）结合，右侧和自然显现**。

---

## 反思

- **第一反应**：直接遍历每个位置，分别求左、右和——也就是暴力解。  
- **最容易踩的坑**  
  - **边界条件**：当枢轴在最左侧或最右侧时，左/右和应视为 `0`，代码里 `left_sum` 初始为 `0` 已经处理。  
  - **负数**：数组中可能有负数，不能用“所有数都是正的”之类的假设。  
  - **整数溢出**：在 Python 中整数自动大数，不会溢出，但在某些语言需要注意。  
- **下次遇到同类题**：第一步先**求整体信息（总和或前缀和数组）**，再**逐步维护局部信息**，这样往往能把 O(n²) 降到 O(n)。