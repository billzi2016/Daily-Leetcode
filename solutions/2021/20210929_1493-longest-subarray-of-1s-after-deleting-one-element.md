# #1493. 删除一个元素后最长的全 1 子数组 / Longest Subarray of 1's After Deleting One Element

> 难度：中等 · 标签：Array、Dynamic Programming、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/)

---

## 题目（英文原版）

**Description**

Given a binary array nums, you should delete one element from it.
Return the size of the longest non-empty subarray containing only 1's in the resulting array. Return 0 if there is no such subarray.

**Examples**

**Example 1:**

```
Input: nums = [1,1,0,1]
Output: 3
Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.
```

**Example 2:**

```
Input: nums = [0,1,1,1,0,1,1,0,1]
Output: 5
Explanation: After deleting the number in position 4, [0,1,1,1,1,1,0,1] longest subarray with value of 1's is [1,1,1,1,1].
```

**Example 3:**

```
Input: nums = [1,1,1]
Output: 2
Explanation: You must delete one element.
```

**Constraints**

- 1 <= nums.length <= 105
- nums[i] is either 0 or 1.

---

## 题目（中文翻译）

**题目描述**  
给定一个二进制数组（binary array）`nums`，你必须删除其中的一个元素。  
返回删除元素后，结果数组中仅包含 `1` 的最长非空子数组（subarray）的长度。如果不存在这样的子数组，返回 `0`。

**示例**

**示例 1**  
```
输入: nums = [1,1,0,1]
输出: 3
解释: 删除下标为 2 的元素后，数组变为 [1,1,1]，其中连续的 `1` 的个数为 3。
```

**示例 2**  
```
输入: nums = [0,1,1,1,0,1,1,0,1]
输出: 5
解释: 删除下标为 4 的元素后，数组变为 [0,1,1,1,1,1,0,1]，最长的全 `1` 子数组是 [1,1,1,1,1]，长度为 5。
```

**示例 3**  
```
输入: nums = [1,1,1]
输出: 2
解释: 必须删除一个元素，删除任意一个后剩下的最长全 `1` 子数组长度为 2。
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `nums[i]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举**要删掉的那个元素的位置（可以是下标 `i`），把它从数组中“拿走”，然后在剩下的数组里找最长的只包含 `1` 的连续子数组。  

- **数据结构**：这里只需要普通的 Python 列表 `list`，相当于我们平时用的“装东西的盒子”。  
- **生活化类比**：把数组想成一排灯泡，`1` 表示灯亮，`0` 表示灯灭。我们先挑掉一盏灯（无论亮还是灭），然后在剩下的灯串中找最长的全亮段。  
- **正确性**：因为题目要求“必须删掉恰好一个元素”，枚举所有可能的删除位置就覆盖了所有合法的情况，取最大值自然就是答案。  

#### 代码（Python）

```python
from typing import List

def longest_subarray_brute(nums: List[int]) -> int:
    n = len(nums)
    best = 0                                 # 用来记录全局最长长度
    for del_idx in range(n):                 # 枚举要删掉的下标
        cur_len = 0                           # 当前连续 1 的长度
        max_len = 0                           # 删除该元素后，这段数组的最长 1 子数组长度
        for i in range(n):
            if i == del_idx:                  # 跳过被删除的元素，相当于它不存在
                continue
            if nums[i] == 1:                  # 遇到 1，长度加一
                cur_len += 1
            else:                             # 遇到 0，当前段结束，更新 max_len 并重置 cur_len
                max_len = max(max_len, cur_len)
                cur_len = 0
        # 循环结束后，还要再比较一次，因为数组可能以 1 结尾
        max_len = max(max_len, cur_len)
        best = max(best, max_len)            # 在所有删除方案中取最大
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n^2)`。外层遍历 `n` 次（每个可能的删除位置），内层又要遍历整个数组 `n` 次来统计最长 1 的段。可以把 `O(n²)` 想成“如果你把一百个人排成两行，第一行每个人都要检查第二行的所有人”，所以随 `n` 增大，耗时会快速增长。  
- **空间复杂度**：`O(1)`。只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次删除后都要重新遍历一遍数组。实际上我们并不需要真的把元素删掉，只要在遍历时“容忍”一次出现 `0`，就能模拟“已经删掉了一个零”。这正是**滑动窗口**（Sliding Window）的典型用法：

1. 用两个指针 `left`、`right` 构成一个窗口，窗口内的元素最多只能有 **一个** `0`。  
2. 当窗口里出现第二个 `0` 时，说明窗口已经违反了“最多一个零”的规则，需要把左边的指针 `left` 往右移动，直到窗口里只剩一个 `0` 为止。  
3. 此时窗口的长度 `right - left + 1` 包含了一个 `0`，而我们必须**删除**恰好一个元素，所以实际的连续 `1` 长度是 `window_length - 1`（把窗口里的那个 `0` 当作被删掉的元素）。  
4. 在遍历结束时，记录下所有窗口对应的 `window_length - 1` 的最大值，就是答案。

**关键概念解释**：

- **滑动窗口**：想象你手里有一根可以伸缩的尺子（窗口），左端和右端分别是 `left`、`right`。我们把尺子往右滑动（增大 `right`），只要尺子里满足条件（最多一个零），就继续；一旦不满足，就把左端往右收缩（增大 `left`），直到再次满足。这样每个元素最多被左指针和右指针各访问一次，时间线性。  
- **最多一个零**：相当于在灯泡串里允许出现一盏灭灯，但不能出现两盏。因为我们可以把这盏灭灯“拔掉”，剩下的全是亮灯。

#### 代码（Python）

```python
from typing import List

def longest_subarray(nums: List[int]) -> int:
    left = 0                # 窗口左边界
    zero_count = 0          # 窗口内 0 的个数
    best = 0                # 记录最长的只含 1 的子数组长度（已删除一个元素）

    for right, val in enumerate(nums):   # 右指针一次遍历数组
        if val == 0:
            zero_count += 1              # 窗口里出现了 0，计数加一

        # 如果窗口里出现了第二个 0，需要收缩左边界
        while zero_count > 1:
            if nums[left] == 0:
                zero_count -= 1          # 左边界离开了一个 0，计数减一
            left += 1                    # 左指针右移，窗口变小

        # 此时窗口内至多一个 0，窗口长度 = right - left + 1
        # 因为必须删除恰好一个元素（可以是这个 0，也可以是窗口外的 1），
        # 所以真正的连续 1 长度是窗口长度减一
        current_len = right - left      # 等价于 (right - left + 1) - 1
        best = max(best, current_len)   # 更新全局最大值

    return best
```

> **注意**：如果数组全是 `1`，窗口永远没有 `0`，此时 `current_len = right - left` 会得到 `n-1`，正好是 “必须删掉一个元素后剩下的最长 1 子数组”。这正是题目要求的行为。

#### 复杂度  

- **时间复杂度**：`O(n)`。左指针和右指针各只会向右走最多 `n` 步，整体是线性遍历。可以把它想成“你只需要一次跑完马拉松，不需要来回折返”。  
- **空间复杂度**：`O(1)`。只用了常数个变量（指针、计数、结果），不随输入规模增长。

---

## 心得

- **核心技巧**：**滑动窗口**——在满足“窗口内某种约束”（本题是“最多包含一个 0”）的前提下，动态维护一个可变长度的子数组。  
- **适用的题型**：
  1. “最长子数组/子串满足最多 K 个特定字符”——如 *最长子数组的和不超过 K*、*最长子串只包含至多两个不同字符*。  
  2. “最短子数组满足某种累计条件”——如 *最小长度子数组之和 ≥ target*。  
  3. “数组中最多允许 X 个不满足条件的元素”——如本题“删除一个元素后全是 1”。  
- **一句话总结**：**把“删掉一个 0”转化为“窗口里允许出现一个 0”，用滑动窗口一次遍历即可得到答案**。

---

## 反思

- **第一反应**：看到“删除一个元素”，立刻想到枚举删除位置，写出暴力解。  
- **最容易踩的坑**：
  - 忘记 **必须删除** 一个元素；即使数组全是 `1`，答案也不是数组长度，而是 `len-1`。  
  - 在滑动窗口实现时，窗口长度要 **减一**（因为窗口里包含了要删除的那个 `0`），否则会把删除的操作漏算。  
  - 边界情况：数组长度为 `1` 时，删除唯一元素后答案应为 `0`，代码需要能够正确返回。  
- **下次遇到同类题**：第一步想到 “把限制转化为窗口内最多出现多少个‘违规’元素”，然后用 **滑动窗口** 维持这个上限，实时更新答案。这样可以把指数级的枚举压到线性时间。