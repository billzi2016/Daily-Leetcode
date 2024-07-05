# #2765. 最长交替子数组 / Longest Alternating Subarray

> 难度：简单 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/longest-alternating-subarray/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. A subarray s of length m is called alternating if:
Return the maximum length of all alternating subarrays present in nums or -1 if no such subarray exists.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [2,3,4,3,4]
Output: 4
Explanation:
The alternating subarrays are [2, 3] , [3,4] , [3,4,3] , and [3,4,3,4] . The longest of these is [3,4,3,4] , which is of length 4.
```

**Example 2:**

```
Input: nums = [4,5,6]
Output: 2
Explanation:
[4,5] and [5,6] are the only two alternating subarrays. They are both of length 2.
```

**Constraints**

- 2 <= nums.length <= 100
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个 **0** 起始索引的整数数组 `nums`。长度为 `m` 的子数组 `s` 若满足以下条件，则称为 **交替子数组**（alternating subarray）：

- 对所有 `1 ≤ i < m`，都有 `|s[i] - s[i-1]| = 1`（相邻元素的差的绝对值恰好为 1）；
- 对所有 `2 ≤ i < m`，相邻差的符号交替，即 `(s[i] - s[i-1]) * (s[i-1] - s[i-2]) = -1`。

返回 `nums` 中所有交替子数组的 **最大长度**，如果不存在满足条件的子数组则返回 `-1`。

> 子数组（subarray）是数组中连续且非空的一段元素序列。

## 示例

### 示例 1
**输入**：`nums = [2,3,4,3,4]`  
**输出**：`4`  
**解释**：交替子数组有 `[2, 3]`、`[3,4]`、`[3,4,3]` 和 `[3,4,3,4]`。其中最长的是 `[3,4,3,4]`，长度为 4。

### 示例 2
**输入**：`nums = [4,5,6]`  
**输出**：`2`  
**解释**：唯一的交替子数组是 `[4,5]` 和 `[5,6]`，它们的长度都是 2。

## 约束条件
- `2 ≤ nums.length ≤ 100`
- `1 ≤ nums[i] ≤ 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把**所有可能的子数组**都枚举出来，逐个检查它们是否满足“交替子数组”的定义。  

- **枚举子数组**：用两个循环，外层 `i` 标记子数组的起点，内层 `j` 标记子数组的终点（`j ≥ i`），这样就能得到所有连续的非空子序列。  
- **检查交替**：遍历子数组中的相邻元素，判断  
  1. 相邻两个数的差的绝对值是否恰好为 `1`（比如 `3 → 4` 或 `4 → 3`），  
  2. 相邻两次的差的符号是否相反（先增后减，再增……）。  
  这两个条件一起就等价于“交替”。  

如果子数组满足条件，就更新答案 `max_len` 为它的长度。遍历结束后，若 `max_len` 仍为 `0`（说明没有任何交替子数组），返回 `-1`；否则返回 `max_len`。

> **类比**：把数组想成一本书的章节，暴力解相当于把每一页都翻一遍，检查从第 `i` 页到第 `j` 页的内容是否满足“前后页数只相差 1 并且增减交替”。虽然最稳妥，但显然效率很低。

#### 代码（Python）  

```python
from typing import List

def longestAlternatingSubarray_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    max_len = 0                     # 记录目前找到的最长交替子数组长度

    # 枚举所有子数组的起点 i
    for i in range(n):
        # 子数组的终点 j（必须大于等于 i）
        for j in range(i, n):
            # 长度为 1 的子数组不算（题目要求长度 ≥ 2）
            if j - i + 1 < 2:
                continue

            ok = True                # 用来标记当前子数组是否满足交替条件
            # 检查子数组 nums[i..j] 的相邻元素
            for k in range(i, j):
                diff = nums[k + 1] - nums[k]
                # 1) 必须恰好相差 1
                if abs(diff) != 1:
                    ok = False
                    break
                # 2) 若不是子数组的第一个差值，需要和前一个差值符号相反
                if k > i:
                    prev_diff = nums[k] - nums[k - 1]
                    if diff * prev_diff >= 0:   # 同号或为 0 都不行
                        ok = False
                        break
            # 若全部检查通过，更新答案
            if ok:
                max_len = max(max_len, j - i + 1)

    return max_len if max_len != 0 else -1
```

#### 复杂度  

- **时间复杂度：** `O(n³)`  
  - 外层两层循环枚举子数组是 `O(n²)`，  
  - 每个子数组内部再遍历一次检查相邻元素是 `O(n)`，于是最坏情况是 `n² * n = n³`。  
  - 用大白话说：如果数组有 100 个数，暴力解大概要做 1,000,000 次“检查”，对初学者来说已经够慢的了。  

- **空间复杂度：** `O(1)`  
  - 只用了常数个额外变量（`max_len、ok、diff` 等），不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的主要瓶颈在于**重复检查**：相邻子数组的大部分元素会被一次又一次地重新遍历。我们可以把检查过程**合并到一次遍历**里，只要在遍历时维护当前符合交替要求的子数组的长度即可。

关键观察：

1. **交替子数组只能从相邻两个满足条件的元素开始**。如果 `|nums[i] - nums[i-1]| != 1`，那么以 `i` 为结尾的任何交替子数组都不可能超过长度 `1`（即不存在）。  
2. **当我们已经知道以 `i-1` 结尾的最长交替子数组长度 `cur_len` 时**，只要 `nums[i]` 与 `nums[i-1]` 的差为 `±1` 且符号与前一次差相反，就可以把 `cur_len` 加 `1`，否则重新从 `i-1` 开始计数（即 `cur_len = 2`）。  

于是我们只需要一次线性扫描：

- 用变量 `cur_len` 保存**以当前元素结尾的交替子数组的最长长度**。  
- 用变量 `prev_diff` 记录**上一次相邻差值的符号**（`+1` 或 `-1`），方便判断是否交替。  
- 每次检查 `diff = nums[i] - nums[i-1]`：  
  - 若 `abs(diff) != 1` → 不能继续，`cur_len = 1`（因为单个元素本身不算），`prev_diff` 失效。  
  - 若 `abs(diff) == 1` 且 `prev_diff` 与 `diff` 符号相反 → `cur_len += 1`。  
  - 否则（差为 1 但符号相同） → 重新从这两个元素开始计数，`cur_len = 2`。  
- 同时维护全局最大值 `max_len`（只在 `cur_len ≥ 2` 时更新）。  

> **类比**：把数组想成一条路，每走一步都要看前后坡度（上坡或下坡）是否恰好为 1 且交替。如果坡度符合，就继续往前走；不符合，就重新找新的起点。这样我们只需“一路走到底”，不必回头检查已经走过的路段。

#### 代码（Python）  

```python
from typing import List

def longestAlternatingSubarray(nums: List[int]) -> int:
    n = len(nums)
    max_len = -1          # 题目要求若不存在交替子数组返回 -1
    cur_len = 1           # 当前以 nums[i] 结尾的交替子数组长度（至少包含自身）
    prev_diff = 0         # 前一次相邻差值的符号，0 表示还没有有效差值

    for i in range(1, n):
        diff = nums[i] - nums[i - 1]

        # 必须恰好相差 1，才可能是交替子数组的一部分
        if abs(diff) != 1:
            cur_len = 1           # 只能重新从当前位置开始计数
            prev_diff = 0
            continue

        # 此时 |diff| == 1，检查符号是否交替
        if prev_diff != 0 and diff * prev_diff < 0:
            # 符号相反 → 继续扩展
            cur_len += 1
        else:
            # 符号相同（或之前没有有效 diff） → 以这两个元素重新开始
            cur_len = 2

        # 更新 prev_diff 为本次的差值符号
        prev_diff = diff

        # 只在长度 ≥ 2 时才算合法的交替子数组
        if cur_len >= 2:
            max_len = max(max_len, cur_len)

    return max_len
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次数组，每一步做常数次计算。  
  - 用大白话说：如果有 100 个数，只需要检查 99 次相邻差值，几乎瞬间就能得到答案。  

- **空间复杂度：** `O(1)`  
  - 只用了固定的几个变量 (`max_len、cur_len、prev_diff`) ，不随输入规模增长。  

---  

## 心得  

- **核心技巧**：**一次遍历 + 状态维护**（记录当前子数组长度和上一次差值的符号），把原本的“枚举 + 检查”压缩成线性扫描。  
- **适用的题型**：  
  1. “最长递增子数组” / “最长递减子数组” —— 只需要判断相邻元素是否满足单调关系。  
  2. “最长平衡子数组” （如 0 与 1 数量相等）—— 通过前缀和转化为“一次遍历 + 哈希表”。  
  3. “最长连续子序列” —— 需要记录连续性，常用滑动窗口或单指针。  
- **一句话总结解题钥匙**：**把局部合法性转化为“状态转移”，用一次遍历把所有可能的子数组合并在一起。**  

## 反思  

- **第一反应**：看到“交替子数组”，立刻想到枚举所有子数组检查——这是一种最安全的直觉。  
- **最容易踩的坑**：  
  - 忘记判断 **差的绝对值必须为 1**，只检查符号交替会导致错误。  
  - 边界条件：数组长度只有 2 时，需要直接返回 `2`（如果满足）或 `-1`。  
  - 当出现 `abs(diff) != 1` 时，必须把 `prev_diff` 重置为 `0`，否则后面的比较会受到污染。  
- **下次类似题目第一步**：**先思考“相邻元素之间的约束是什么”，能否用一个变量记录上一次的约束（比如差值、方向、和等）来做状态转移**，如果能，就直接走“一次遍历”路线；如果不能，再考虑枚举或更高级的数据结构。