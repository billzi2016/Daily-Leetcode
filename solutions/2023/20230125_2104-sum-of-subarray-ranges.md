# #2104. 子数组范围之和 / Sum of Subarray Ranges

> 难度：中等 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/sum-of-subarray-ranges/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. The range of a subarray of nums is the difference between the largest and smallest element in the subarray.
Return the sum of all subarray ranges of nums.
A subarray is a contiguous non-empty sequence of elements within an array.
Follow-up: Could you find a solution with O(n) time complexity?

**Examples**

**Example 1:**

```
Input: nums = [1,2,3]
Output: 4
Explanation: The 6 subarrays of nums are the following:
[1], range = largest - smallest = 1 - 1 = 0 
[2], range = 2 - 2 = 0
[3], range = 3 - 3 = 0
[1,2], range = 2 - 1 = 1
[2,3], range = 3 - 2 = 1
[1,2,3], range = 3 - 1 = 2
So the sum of all ranges is 0 + 0 + 0 + 1 + 1 + 2 = 4.
```

**Example 2:**

```
Input: nums = [1,3,3]
Output: 4
Explanation: The 6 subarrays of nums are the following:
[1], range = largest - smallest = 1 - 1 = 0
[3], range = 3 - 3 = 0
[3], range = 3 - 3 = 0
[1,3], range = 3 - 1 = 2
[3,3], range = 3 - 3 = 0
[1,3,3], range = 3 - 1 = 2
So the sum of all ranges is 0 + 0 + 0 + 2 + 0 + 2 = 4.
```

**Example 3:**

```
Input: nums = [4,-2,-3,4,1]
Output: 59
Explanation: The sum of all subarray ranges of nums is 59.
```

**Constraints**

- 1 <= nums.length <= 1000
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个整数数组 `nums`。数组中任意子数组（subarray）的 **范围** 定义为该子数组中最大元素与最小元素的差值。  
返回 `nums` 所有子数组范围的 **总和**。  
子数组是数组中连续且非空的元素序列。

### 示例

#### 示例 1
**输入**: `nums = [1,2,3]`  
**输出**: `4`  
**解释**: `nums` 的 6 个子数组如下：
- `[1]`，范围 = 最大值 - 最小值 = `1 - 1 = 0`  
- `[2]`，范围 = `2 - 2 = 0`  
- `[3]`，范围 = `3 - 3 = 0`  
- `[1,2]`，范围 = `2 - 1 = 1`  
- `[2,3]`，范围 = `3 - 2 = 1`  
- `[1,2,3]`，范围 = `3 - 1 = 2`  

所有范围之和为 `0 + 0 + 0 + 1 + 1 + 2 = 4`。

#### 示例 2
**输入**: `nums = [1,3,3]`  
**输出**: `4`  
**解释**: `nums` 的 6 个子数组如下：
- `[1]`，范围 = `1 - 1 = 0`  
- `[3]`，范围 = `3 - 3 = 0`  
- `[3]`，范围 = `3 - 3 = 0`  
- `[1,3]`，范围 = `3 - 1 = 2`  
- `[3,3]`，范围 = `3 - 3 = 0`  
- `[1,3,3]`，范围 = `3 - 1 = 2`  

所有范围之和为 `0 + 0 + 0 + 2 + 0 + 2 = 4`。

#### 示例 3
**输入**: `nums = [4,-2,-3,4,1]`  
**输出**: `59`  
**解释**: 所有子数组范围的总和为 `59`。

### 约束条件
- `1 <= nums.length <= 1000`
- `-10^9 <= nums[i] <= 10^9`

### 进阶
能否找到时间复杂度为 `O(n)` 的解法？

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有连续子数组** 都枚举出来，分别算出它们的最大值和最小值，再求差值累加。  

- **枚举子数组**：对每个起始位置 `i`，把右边的元素一个一个往后加，形成子数组 `nums[i…j]`（`j >= i`）。  
- **求最大/最小**：在把 `j` 向右移动的过程中，可以把当前子数组的最大值和最小值用两个变量 `cur_max`、`cur_min` 维护，只要把 `nums[j]` 和这两个变量比较一次即可。  
- **累加贡献**：`range = cur_max - cur_min`，把它加到答案里。

> **类比**：把数组想成一排排的盒子，暴力做法就是把每个盒子当作起点，往右一直打开盒子，看到里面的最大和最小是什么，然后记下来。  

因为我们只用了两个变量来记录当前子数组的最大/最小，所以虽然枚举了 `O(n²)` 个子数组，**每个子数组的最大/最小是 `O(1)` 时间得到的**，整体时间仍是 `O(n²)`。

#### 代码（Python）  

```python
def subArrayRanges(nums):
    n = len(nums)
    ans = 0
    # 枚举左端点 i
    for i in range(n):
        cur_max = cur_min = nums[i]          # 子数组只有一个元素时的最大最小
        # 枚举右端点 j（>= i）
        for j in range(i, n):
            # 更新当前子数组的最大值和最小值
            cur_max = max(cur_max, nums[j])
            cur_min = min(cur_min, nums[j])
            ans += cur_max - cur_min          # 累加该子数组的范围
    return ans
```

> 关键行解释  
> - `cur_max = cur_min = nums[i]`：子数组刚开始只有 `nums[i]`，最大最小都是它自己。  
> - `cur_max = max(cur_max, nums[j])` / `cur_min = min(cur_min, nums[j])`：把新加入的元素 `nums[j]` 与当前最大/最小比较，及时更新。  

#### 复杂度  

- **时间复杂度**：`O(n²)`。想象有 `n` 行 `n` 列的格子，每个格子对应一次子数组的遍历，整体就是平方级别。  
- **空间复杂度**：`O(1)`。只用了常数个额外变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举所有子数组**，即使每个子数组的最大/最小是 `O(1)`，子数组的数量仍是 `n·(n+1)/2 ≈ O(n²)`。  
要做到 `O(n)`，必须 **不显式枚举子数组**，而是把每个元素对答案的贡献直接算出来。

**核心观察**：  
- 对于任意子数组，它的范围 `max - min` 可以拆成两部分：  
  - 该子数组中最大元素的 **贡献**（加上它的值）  
  - 该子数组中最小元素的 **贡献**（减去它的值）  
- 所以答案 = (所有子数组中最大元素的贡献之和) - (所有子数组中最小元素的贡献之和)。

于是任务变成：**统计每个位置的元素在多少个子数组里是最大值（或最小值）**。  
如果能求出 `cnt_max[i]`（第 `i` 个元素是子数组最大值的个数）和 `cnt_min[i]`，答案就等于  

```
ans = Σ nums[i] * cnt_max[i]  -  Σ nums[i] * cnt_min[i]
```

**如何求 cnt_max / cnt_min？**  
考虑第 `i` 个元素 `nums[i]`，它在子数组 `[L … R]` 中是最大值的充要条件是：

- 左边没有比它更大的元素（左边第一个比它大的下标记为 `leftGreater`），于是左端点 `L` 必须在 `(leftGreater, i]` 之间。  
- 右边没有**不小于**它的元素（右边第一个大于等于它的下标记为 `rightGreaterOrEqual`），于是右端点 `R` 必须在 `[i, rightGreaterOrEqual)` 之间。  

于是 **可以取的左端点有 `i - leftGreater` 种**，**右端点有 `rightGreaterOrEqual - i` 种**，两者独立组合得到  

```
cnt_max[i] = (i - leftGreater) * (rightGreaterOrEqual - i)
```

同理，最小值的计数使用 **单调递增栈**（找左侧第一个更小，右侧第一个小于等于的下标）得到 `cnt_min[i]`。

**单调栈是什么？**  
想象一条只能“递增”或“递减”的栈（栈顶永远保持某种顺序），当我们从左到右遍历数组时，栈里存的是 **下标**，而不是元素本身。  
- 对 **最大值**，我们维护 **严格递减** 的栈（栈顶对应的数比新来的数大），这样当新数出现时，就能一次性弹出所有 **不再可能成为更大元素左侧界限** 的下标，得到它们的右界限。  
- 对 **最小值**，维护 **严格递增** 的栈，原理类似。

整个过程只遍历一次数组，栈的每个元素最多进出一次，故是 `O(n)`。

#### 代码（Python）  

```python
def subArrayRanges(nums):
    n = len(nums)
    # ---------- 计算每个元素作为最大值的贡献 ----------
    # left[i]  : 距离最近的、严格大于 nums[i] 的左侧下标（若不存在为 -1）
    # right[i] : 距离最近的、> = nums[i] 的右侧下标（若不存在为 n）
    left = [-1] * n
    right = [n] * n
    stack = []                     # 单调递减栈，保存下标

    # 求左侧严格大于的下标
    for i in range(n):
        while stack and nums[stack[-1]] <= nums[i]:   # 栈顶 <= 当前，弹出
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # 清空栈，重新求右侧大于等于的下标
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] < nums[i]:    # 栈顶 < 当前，弹出
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    max_contrib = 0
    for i in range(n):
        # (i - left) * (right - i) 是 nums[i] 作为最大值出现的子数组个数
        cnt = (i - left[i]) * (right[i] - i)
        max_contrib += nums[i] * cnt

    # ---------- 计算每个元素作为最小值的贡献 ----------
    left = [-1] * n
    right = [n] * n
    stack.clear()                  # 单调递增栈，保存下标

    # 求左侧严格小于的下标
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:   # 栈顶 >= 当前，弹出
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # 求右侧小于等于的下标
    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] > nums[i]:    # 栈顶 > 当前，弹出
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    min_contrib = 0
    for i in range(n):
        cnt = (i - left[i]) * (right[i] - i)
        min_contrib += nums[i] * cnt

    # ---------- 最终答案 ----------
    return max_contrib - min_contrib
```

> 关键行解释  
> - `while stack and nums[stack[-1]] <= nums[i]: stack.pop()`：保持栈从下到上严格递减（对应最大值），遇到不再满足的元素就弹出，它们的右界限就在当前位置 `i`。  
> - `left[i] = stack[-1] if stack else -1`：栈顶是最近的左侧更大的元素下标；若栈空说明左边没有更大的，用 `-1` 代表“左边界在数组外”。  
> - `cnt = (i - left[i]) * (right[i] - i)`：左端点可以选 `i-left[i]` 种，右端点可以选 `right[i]-i` 种，组合即子数组个数。  

#### 复杂度  

- **时间复杂度**：`O(n)`。每个元素进栈、出栈各最多一次，两个方向各遍历一次数组。  
- **空间复杂度**：`O(n)`。需要额外的 `left`、`right` 数组以及栈，都是线性大小。  

---

## 心得  

- **核心技巧**：**单调栈 + 贡献计数**。把“每个子数组的最大/最小”转化为“每个元素在多少子数组里是最大/最小”。  
- **适用题型**  
  1. “子数组的最值贡献”类，如 *Sum of Subarray Minimums*、*Sum of Subarray Maximums*。  
  2. “直方图面积”或 “矩形最大面积”类，需要快速找左/右第一个更大或更小的元素。  
- **一句话总结解题钥匙**：**把全局求和拆成每个元素的局部贡献，再用单调栈一次性算出每个元素的贡献次数**。  

---

## 反思  

- **第一反应**：直接枚举所有子数组，写两层循环，算最大最小——对初学者最自然的思路。  
- **最容易踩的坑**  
  - **等号处理**：在求最大值右边界时需要 `>=`（防止重复计数），左边界用 `>`；最小值相反。否则相同元素会被多算或漏算。  
  - **负数和大数**：答案可能很大，使用 Python 的大整数没问题，但在某些语言要注意溢出。  
  - **下标越界**：左边界不存在时用 `-1`，右边界不存在时用 `n`，乘法公式才能正常工作。  
- **下次类似题的第一步**：先思考 **“每个元素的贡献”** 能否把全局问题拆解，而不是直接遍历子结构。这样往往能把时间从 `O(n²)` 降到 `O(n)`。