# #1848. 最小距离到目标元素 / Minimum Distance to the Target Element

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/minimum-distance-to-the-target-element/)

---

## 题目（英文原版）

**Description**

Given an integer array nums (0-indexed) and two integers target and start, find an index i such that nums[i] == target and abs(i - start) is minimized. Note that abs(x) is the absolute value of x.
Return abs(i - start).
It is guaranteed that target exists in nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], target = 5, start = 3
Output: 1
Explanation: nums[4] = 5 is the only value equal to target, so the answer is abs(4 - 3) = 1.
```

**Example 2:**

```
Input: nums = [1], target = 1, start = 0
Output: 0
Explanation: nums[0] = 1 is the only value equal to target, so the answer is abs(0 - 0) = 0.
```

**Example 3:**

```
Input: nums = [1,1,1,1,1,1,1,1,1,1], target = 1, start = 0
Output: 0
Explanation: Every value of nums is 1, but nums[0] minimizes abs(i - start), which is abs(0 - 0) = 0.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 104
- 0 <= start < nums.length
- target is in nums.

---

## 题目（中文翻译）

给定一个整数数组 `nums`（0 索引）以及两个整数 `target` 和 `start`，请找到满足 `nums[i] == target` 且 `abs(i - start)` 最小的下标 `i`。其中 `abs(x)` 表示 `x` 的绝对值。  
返回 `abs(i - start)` 的值。  
题目保证数组中一定存在 `target`。

**示例 1**  
**输入**: `nums = [1,2,3,4,5]`, `target = 5`, `start = 3`  
**输出**: `1`  
**解释**: `nums[4] = 5` 是唯一等于目标值的元素，因此答案为 `abs(4 - 3) = 1`。

**示例 2**  
**输入**: `nums = [1]`, `target = 1`, `start = 0`  
**输出**: `0`  
**解释**: `nums[0] = 1` 是唯一等于目标值的元素，答案为 `abs(0 - 0) = 0`。

**示例 3**  
**输入**: `nums = [1,1,1,1,1,1,1,1,1,1]`, `target = 1`, `start = 0`  
**输出**: `0`  
**解释**: 数组中所有元素均为 `1`，但 `nums[0]` 能最小化 `abs(i - start)`，即 `abs(0 - 0) = 0`。

**约束条件**  
- `1 <= nums.length <= 1000`  
- `1 <= nums[i] <= 10^4`  
- `0 <= start < nums.length`  
- `target` 必定出现在 `nums` 中。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组 `nums` 从头到尾全部检查一遍，遇到 `nums[i] == target` 就算出 `abs(i - start)`（即下标差的绝对值），把所有算出来的距离保存下来，最后取最小的那个。  

- **用到的数据结构**：只需要遍历数组，用一个普通的整数变量 `ans` 来保存目前找到的最小距离。可以把它想象成在找最近的便利店，走到每一家店（遍历每个下标），记下离自己家（`start`）的距离，挑最短的那条路。  
- **为什么正确**：因为我们把所有满足 `nums[i] == target` 的位置都检查了一遍，必然不会错过最近的那个。只要把每一次的距离和当前最小距离比较并更新，最终得到的就是全局最小值。  
- **时间/空间复杂度**：  
  - **时间复杂度**是 `O(n)`，其中 `n` 是数组长度。我们只遍历一次数组，遍历一次的工作量和数组长度成正比。  
  - **空间复杂度**是 `O(1)`，只用了常数个额外变量（`ans`、循环变量 `i`），和数组大小无关。

> 大白话解释：  
> - `O(n)` 可以理解为“如果数组有 10 个元素，就做大约 10 次工作；如果有 1000 个元素，就做大约 1000 次工作”。  
> - `O(1)` 表示“不管数组多大，额外占用的空间都几乎不变”，就像只带了一把钥匙，而不是整套工具箱。

#### 代码（Python）

```python
from typing import List

def get_minimum_distance(nums: List[int], target: int, start: int) -> int:
    # 初始化答案为一个很大的数，后面会被第一个符合条件的距离覆盖
    ans = float('inf')
    
    # 从左到右遍历整个数组
    for i in range(len(nums)):
        if nums[i] == target:                 # 找到目标元素
            distance = abs(i - start)         # 计算与 start 的下标距离
            ans = min(ans, distance)          # 保留最小的距离
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，工作量随数组长度线性增长。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，额外空间不随输入规模变化。

---

### 2. 最优解  

#### 思路  

对于本题，**暴力解已经是最优**，因为我们只需要一次线性扫描就能得到答案。  
如果把暴力解想象成“一次性把所有店都走一遍”，已经没有更快的办法——我们必须至少检查一次每个元素，才能确认它是否是目标 `target`。  

不过，从实现角度还有一种更简洁的写法：**双指针向左右同时扩散**。  
从 `start` 位置出发，向左、向右分别一步一步检查，谁先碰到 `target`，对应的步数就是答案。  

- **为什么快**：在最坏情况下仍然要遍历整个数组（比如 `target` 在最远端），所以时间复杂度仍是 `O(n)`。但在实际运行时，往往能提前结束，平均走的步数会比完整遍历少。  
- **核心概念**：**双指针**（Two‑Pointer）——想象你站在数组中间，左手向左伸，右手向右伸，谁先碰到目标元素，距离就是答案。  

#### 代码（Python）

```python
from typing import List

def get_minimum_distance(nums: List[int], target: int, start: int) -> int:
    n = len(nums)
    left, right = start, start          # 同时从 start 向左、向右扩散
    
    # 最多循环 n 次，因为最多检查所有下标
    for step in range(n):
        # 检查左边界是否在数组范围内且是否等于 target
        if left >= 0 and nums[left] == target:
            return step                 # 第一步就是最小距离
        # 检查右边界是否在数组范围内且是否等于 target
        if right < n and nums[right] == target:
            return step
        # 向外扩散一步
        left -= 1
        right += 1
    # 题目保证一定会找到 target，这行理论上永远不会执行
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 最坏仍需检查全部 `n` 个元素。相较于完整遍历的实现，平均情况会更早返回。  
- **空间复杂度**：`O(1)` —— 只用了常数个指针变量 `left`、`right`、`step`。

---

## 心得  

- **核心技巧**：双指针（或一次线性扫描）求最近距离。  
- **适用的题型**：  
  1. “在数组中找离指定下标最近的满足条件的元素”（如本题）。  
  2. “从中心向两侧搜索最近的目标”（如 LeetCode 1791 “Find Center of Star Graph” 的变形）。  
  3. “最近的相同字符位置”（字符串版的最近相等字符问题）。  
- **一句话总结**：**从起点向两边同步扩散，谁先碰到目标，距离就是答案**。

---

## 反思  

- **第一反应**：看到“最小的 `abs(i-start)`”，自然想到遍历全部元素计算距离。  
- **最容易踩的坑**：  
  - 忘记 `abs`（取绝对值），导致负数距离错误。  
  - 没有考虑 `target` 可能出现多次，需要取最小的那个。  
  - 边界条件：如果 `start` 本身就是目标，需要立刻返回 `0`。  
- **下次类似题的第一步**：先判断起点是否已经满足条件；如果不是，考虑从起点向左向右同步扩散（双指针）或一次完整遍历，取最小距离。