# #2334. 阈值随子数组长度变化的子数组 / Subarray With Elements Greater Than Varying Threshold

> 难度：困难 · 标签：Array、Stack、Union Find、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/subarray-with-elements-greater-than-varying-threshold/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer threshold.
Find any subarray of nums of length k such that every element in the subarray is greater than threshold / k.
Return the size of any such subarray. If there is no such subarray, return -1.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,3,4,3,1], threshold = 6
Output: 3
Explanation: The subarray [3,4,3] has a size of 3, and every element is greater than 6 / 3 = 2.
Note that this is the only valid subarray.
```

**Example 2:**

```
Input: nums = [6,5,6,5,8], threshold = 7
Output: 1
Explanation: The subarray [8] has a size of 1, and 8 > 7 / 1 = 7. So 1 is returned.
Note that the subarray [6,5] has a size of 2, and every element is greater than 7 / 2 = 3.5. 
Similarly, the subarrays [6,5,6], [6,5,6,5], [6,5,6,5,8] also satisfy the given conditions.
Therefore, 2, 3, 4, or 5 may also be returned.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i], threshold <= 109

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数 `threshold`（阈值）。  
寻找任意长度为 `k` 的子数组（subarray），要求子数组中的每个元素都大于 `threshold / k`。  
返回任意满足条件的子数组的长度。如果不存在这样的子数组，返回 `-1`。  

子数组（subarray）是数组中连续且非空的元素序列。

**示例 1**  
**输入**: `nums = [1,3,4,3,1]`, `threshold = 6`  
**输出**: `3`  
**解释**: 子数组 `[3,4,3]` 的长度为 `3`，且每个元素都大于 `6 / 3 = 2`。这是唯一满足条件的子数组。

**示例 2**  
**输入**: `nums = [6,5,6,5,8]`, `threshold = 7`  
**输出**: `1`  
**解释**: 子数组 `[8]` 的长度为 `1`，且 `8 > 7 / 1 = 7`，因此返回 `1`。  
注意子数组 `[6,5]` 的长度为 `2`，且每个元素都大于 `7 / 2 = 3.5`。同理，子数组 `[6,5,6]`、`[6,5,6,5]`、`[6,5,6,5,8]` 也都满足条件。  
因此返回 `2`、`3`、`4` 或 `5` 皆可。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i], threshold <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的**连续子数组**都枚举一遍，算出它们的长度 `k`，然后检查子数组里的每个元素是否都满足  

```
element > threshold / k
```

- **数据结构**：只需要用普通的 Python 列表来存放数组 `nums`。遍历子数组时，用两个嵌套的 `for` 循环，外层确定子数组的左端点 `left`，内层逐步扩展右端点 `right`，随时维护当前子数组的最小值（因为只要最小值满足条件，整个子数组必定满足）。
- **正确性**：我们把所有合法的子数组都检查了一遍，只要有一个满足条件，就一定会被找到。没有遗漏，也不会误判。

#### 代码（Python）

```python
from typing import List

def subarray_size_brute(nums: List[int], threshold: int) -> int:
    n = len(nums)
    # 枚举左端点
    for left in range(n):
        cur_min = float('inf')          # 当前子数组的最小值
        # 右端点不断向右扩展
        for right in range(left, n):
            cur_min = min(cur_min, nums[right])   # 更新最小值
            k = right - left + 1                 # 子数组长度
            # 判定条件：最小值 > threshold / k
            if cur_min * k > threshold:          # 为了避免浮点数，等价于 cur_min > threshold / k
                return k                         # 找到第一个合法长度直接返回
    return -1                                   # 没有合法子数组
```

- 第 9 行 `cur_min * k > threshold` 把不等式 `cur_min > threshold / k` 两边同乘 `k`（`k` 为正整数），避免使用浮点数比较。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环会检查大约 `n·(n+1)/2` 个子数组。可以把 `O(n²)` 想象成“如果数组有 10,000 个元素，最坏情况下要检查大约 100 000 000 次”。在 10⁵ 规模的数据上会超时。
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（`cur_min`、`left`、`right`、`k`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**不断重复计算子数组的最小值**。如果我们能一次性得到每个位置上“**以该位置为最小元素的最大连续区间**”，就可以直接判断是否存在合法长度，而不必枚举所有子数组。

**关键观察**  

1. 对于任意子数组，只要其中的**最小元素**满足 `min > threshold / k`，整段子数组必定合法。  
2. 对于数组中的某个下标 `i`，如果我们知道它左侧最近的**比它更小**的元素位置 `L`，以及右侧最近的**比它更小**的元素位置 `R`，那么**以 `i` 为最小元素的最大子数组**就是 `(L+1 … R-1)`，长度为 `R - L - 1`。  
3. 只要这个最大长度 `max_len` 大于 `floor(threshold / nums[i])`，就一定可以挑选出一个合法的 `k`（例如 `k = floor(threshold / nums[i]) + 1`）。

**如何快速得到 `L` 与 `R`**  

- 使用**单调递增栈**（Monotonic Stack）。  
- 扫描一次数组，栈里保持**严格递增**的元素下标。当遇到更小的元素时，就可以弹出栈顶，确定该弹出元素的**右侧最近更小**位置。  
- 同理，逆序扫描或在同一次扫描中记录**左侧最近更小**位置。

**步骤概览**  

1. 用单调递增栈得到每个下标 `i` 的 `prev_smaller[i]`（左侧最近更小的下标，若不存在记为 `-1`）。  
2. 再用单调递增栈（从左到右）得到 `next_smaller[i]`（右侧最近更小的下标，若不存在记为 `n`）。  
3. 对每个 `i` 计算  
   - `max_len = next_smaller[i] - prev_smaller[i] - 1`  
   - `need = threshold // nums[i] + 1`（因为我们要求 `k > threshold / nums[i]`，取整数最小的满足值）。  
   - 若 `need <= max_len`，返回 `need`（任意合法长度都可以，这里返回最小的）。  
4. 若遍历完所有 `i` 都找不到合法长度，返回 `-1`。

**类比**：  
想象一排房子高度不同，单调栈相当于“从左到右的巡逻队”。当巡逻队遇到比前面房子更矮的房子时，就可以立刻报告前面那栋房子“视野被挡住了”，于是得到了它左/右两侧的最近更矮房子的位置。

#### 代码（Python）

```python
from typing import List

def subarray_size_opt(nums: List[int], threshold: int) -> int:
    n = len(nums)
    # ---------- 第一步：求左侧最近更小的下标 ----------
    prev_smaller = [-1] * n          # -1 表示左侧不存在更小元素
    stack = []                       # 单调递增栈，存下标
    for i, val in enumerate(nums):
        # 栈顶元素 >= 当前值时弹出，直到栈为空或栈顶 < 当前值
        while stack and nums[stack[-1]] >= val:
            stack.pop()
        # 此时栈顶（若存在）就是左侧最近更小的元素
        prev_smaller[i] = stack[-1] if stack else -1
        stack.append(i)               # 当前下标加入栈中

    # ---------- 第二步：求右侧最近更小的下标 ----------
    next_smaller = [n] * n           # n 表示右侧不存在更小元素
    stack.clear()
    for i in range(n - 1, -1, -1):   # 逆序遍历
        val = nums[i]
        while stack and nums[stack[-1]] >= val:
            stack.pop()
        next_smaller[i] = stack[-1] if stack else n
        stack.append(i)

    # ---------- 第三步：检查每个位置是否能得到合法子数组 ----------
    for i in range(n):
        max_len = next_smaller[i] - prev_smaller[i] - 1   # 以 i 为最小元素的最大长度
        # 需要的最小长度，使得 nums[i] > threshold / k
        need = threshold // nums[i] + 1
        if need <= max_len:                               # 能在区间内取到合法 k
            return need                                   # 任意合法长度，这里返回最小的

    return -1  # 没有找到符合条件的子数组
```

- 第 5‑12 行：求左侧最近更小的位置，使用递增栈实现 `O(n)`。
- 第 15‑22 行：逆序求右侧最近更小的位置，思路相同。
- 第 25‑31 行：根据公式 `need = threshold // nums[i] + 1` 计算**最小可行长度**，只要它不超过 `max_len`，就说明存在合法子数组。

#### 复杂度

- **时间复杂度**：`O(n)`  
  单调栈的每个元素最多进栈一次、出栈一次，整体线性扫描两遍即可。相当于“即使数组有 100,000 个元素，也只需要大约 200,000 次基本操作”，远快于暴力的 `n²`。
- **空间复杂度**：`O(n)`  
  需要额外的三个长度为 `n` 的数组（`prev_smaller、next_smaller、stack`），但都是线性空间，且在实际运行中只占用几百 KB。

---

## 心得

- **核心技巧**：利用**单调栈**一次性得到每个元素左右最近更小的位置，从而快速求出“以该元素为最小值的最大区间”。  
- **适用题型**：
  1. “找每个元素左右最近更大/更小”类问题（如 **柱状图中最大的矩形**、**滑动窗口最大值**）。  
  2. “子数组的最小值/最大值决定整体性质”类问题（如 **子数组最小值的总和**、**最长的子数组满足条件**）。  
- **解题钥匙**：**把“所有子数组”转化为“每个元素对应的最大区间”，再用数学不等式快速判断**。

---

## 反思

- **第一反应**：直接枚举所有子数组，检查每个元素是否满足条件。  
- **最容易踩的坑**：
  - 忘记把不等式 `a > b / k` 转换为整数比较 `a * k > b`，导致浮点数精度问题。  
  - 在单调栈实现时，忘记使用 **严格递增**（`>=`）而导致相等元素的处理错误。  
  - 计算 `need = threshold // nums[i] + 1` 时，忽略了阈值恰好被整除的情况。  
- **下次类似题目**：第一步先思考“**最小/最大元素**是否能代表整个子数组的约束”，再尝试用 **单调栈** 或 **前缀/后缀** 信息把子数组空间压缩到 `O(n)`。