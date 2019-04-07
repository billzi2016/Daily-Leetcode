# #376. 摆动子序列 / Wiggle Subsequence

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/wiggle-subsequence/)

---

## 题目（英文原版）

**Description**

A wiggle sequence is a sequence where the differences between successive numbers strictly alternate between positive and negative. The first difference (if one exists) may be either positive or negative. A sequence with one element and a sequence with two non-equal elements are trivially wiggle sequences.
A subsequence is obtained by deleting some elements (possibly zero) from the original sequence, leaving the remaining elements in their original order.
Given an integer array nums, return the length of the longest wiggle subsequence of nums.
Follow up: Could you solve this in O(n) time?

**Examples**

**Example 1:**

```
Input: nums = [1,7,4,9,2,5]
Output: 6
Explanation: The entire sequence is a wiggle sequence with differences (6, -3, 5, -7, 3).
```

**Example 2:**

```
Input: nums = [1,17,5,10,13,15,10,5,16,8]
Output: 7
Explanation: There are several subsequences that achieve this length.
One is [1, 17, 10, 13, 10, 16, 8] with differences (16, -7, 3, -3, 6, -8).
```

**Example 3:**

```
Input: nums = [1,2,3,4,5,6,7,8,9]
Output: 2
```

**Constraints**

- 1 <= nums.length <= 1000
- 0 <= nums[i] <= 1000

---

## 题目（中文翻译）

摆动序列是指相邻数字之间的差值严格在正数和负数之间交替出现的序列。若存在第一组差值，它可以是正的也可以是负的。仅包含一个元素的序列以及包含两个不相等元素的序列天然满足摆动序列的定义。

子序列（subsequence）是通过从原始序列中删除若干元素（也可以不删）而得到的，剩余元素保持原来的相对顺序。

给定整数数组 `nums`，返回其最长摆动子序列（wiggle subsequence）的长度。

**示例 1**  
```
Input: nums = [1,7,4,9,2,5]
Output: 6
Explanation: 整个序列本身就是摆动序列，其差值分别为 (6, -3, 5, -7, 3)。
```

**示例 2**  
```
Input: nums = [1,17,5,10,13,15,10,5,16,8]
Output: 7
Explanation: 存在多种子序列可以达到该长度，其中一种是 [1, 17, 10, 13, 10, 16, 8]，其差值为 (16, -7, 3, -3, 6, -8)。
```

**示例 3**  
```
Input: nums = [1,2,3,4,5,6,7,8,9]
Output: 2
```

**约束条件**  
- `1 <= nums.length <= 1000`  
- `0 <= nums[i] <= 1000`

**进阶**  
你能在 `O(n)` 时间复杂度内完成此题吗？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有可能的「子序列」都枚举一遍，检查每一个子序列是否满足「摆动」的条件，记录最长的长度。

- **子序列**：可以把原数组想象成一串珠子，挑选出若干颗（顺序不变）组成新的一串。枚举子序列相当于遍历所有挑选/不挑选的组合。  
- **摆动序列**：相邻两个数的差值要交替出现正负。比如 `1,7,4,9` 的差是 `+6, -3, +5`，正负交替就符合要求。  
- **数据结构**：我们只需要用 **列表**（list）来保存当前枚举出来的子序列，用 **递归**（或二进制掩码）来遍历所有组合。这里没有哈希表之类的高级结构，只是最朴素的「全遍历」。

为什么暴力方法一定能得到正确答案？因为我们检查了**所有**合法子序列，最长的自然就是答案。

> **时间复杂度的直观解释**  
> 假设数组长度为 `n`，每个位置可以「选」或「不选」，所以一共有 `2^n` 种子序列。对每一种我们都要遍历一次子序列检查摆动，最坏情况下相当于「把所有可能的组合都试一遍」——这就是指数级的时间消耗，用 `O(2^n)` 表示。

#### 代码（Python）

```python
from typing import List

def longest_wiggle_brute(nums: List[int]) -> int:
    n = len(nums)
    best = 0                     # 记录当前找到的最长长度

    # 用二进制掩码遍历所有子序列，mask 的第 i 位为 1 表示保留 nums[i]
    for mask in range(1, 1 << n):            # 0 代表空子序列，直接跳过
        seq = []                              # 当前子序列
        for i in range(n):
            if mask & (1 << i):               # 第 i 位为 1，选取该元素
                seq.append(nums[i])

        # 判断 seq 是否是摆动序列
        if is_wiggle(seq):
            best = max(best, len(seq))

    return best


def is_wiggle(seq: List[int]) -> bool:
    """检查一个序列是否满足摆动条件"""
    if len(seq) < 2:          # 长度 0、1 都算摆动序列
        return True
    # 计算相邻差值的符号（正为 +1，负为 -1，零不算摆动）
    diff_signs = []
    for i in range(1, len(seq)):
        diff = seq[i] - seq[i - 1]
        if diff > 0:
            diff_signs.append(1)
        elif diff < 0:
            diff_signs.append(-1)
        else:                 # 差为 0，直接返回 False
            return False

    # 检查符号是否交替出现
    for i in range(1, len(diff_signs)):
        if diff_signs[i] == diff_signs[i - 1]:   # 连续两个符号相同
            return False
    return True
```

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  解释：我们遍历 `2^n` 种子序列，每一种最多要遍历 `n` 次元素来构造序列并检查摆动，等价于「把所有可能的组合都试一次」。
- **空间复杂度**：`O(n)`  
  解释：主要是递归/循环中保存当前子序列 `seq` 所需的额外空间，最坏情况下长度为 `n`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于「枚举所有子序列」这一步。其实我们并不需要真的把所有组合列出来，只要知道「最长摆动子序列」的长度可以通过**局部最优**来递推得到。

**关键观察**：

1. **只关心“方向”**（上升或下降），而不是具体的数值。  
2. 对于一个位置 `i`，如果 `nums[i]` 与前一个保留的元素形成了 **不同方向** 的差，就一定可以把 `nums[i]` 加入到当前摆动序列，长度加 1。  
3. 如果方向相同，则保留「更有利」的那个元素：  
   - 当我们在上升阶段（上一次差为正）时，**更大的数** 更容易在后面再下降；  
   - 当我们在下降阶段（上一次差为负）时，**更小的数** 更容易在后面再上升。  
   这就意味着我们可以用 **贪心** 的方式，只记录最近一次「有效」的上升或下降值，而不必保留全部历史。

基于上述想法，我们只需要一次遍历：

- 用两个变量 `up`、`down` 表示「以当前位置结尾且最后一次差为正」和「为负」的最长摆动子序列长度。  
- 当 `nums[i] > nums[i-1]` 时，说明出现了上升，`up = down + 1`（因为可以在之前的下降后接上这一次上升）。  
- 当 `nums[i] < nums[i-1]` 时，说明出现了下降，`down = up + 1`。  
- 相等时不做任何改变，因为差为 0 既不是上升也不是下降，不能帮助摆动。

最终答案是 `max(up, down)`，因为序列可以以正差或负差结束。

> **为什么贪心是对的？**  
> 每一次「方向改变」都必然能让序列长度加 1，而「方向不变」时我们只保留最有利的端点（更大或更小），这不会影响后面能够继续摆动的可能性。换句话说，**只要方向交替，就一定是最优的**，所以一次线性扫描就能得到最优解。

#### 代码（Python）

```python
from typing import List

def longest_wiggle(nums: List[int]) -> int:
    """
    O(n) 贪心解法
    up   : 以当前位置结尾，且最后一次差为正（上升）的最长摆动子序列长度
    down : 以当前位置结尾，且最后一次差为负（下降）的最长摆动子序列长度
    """
    n = len(nums)
    if n < 2:
        return n                     # 长度 0、1 本身就是摆动序列

    up = down = 1                    # 第一个元素单独成序列，长度为 1

    for i in range(1, n):
        if nums[i] > nums[i - 1]:
            up = down + 1            # 形成上升，长度 = 之前的下降长度 + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1            # 形成下降，长度 = 之前的上升长度 + 1
        # else: nums[i] == nums[i-1]，不改变 up/down

    return max(up, down)             # 可能以正差或负差结束
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，`n` 表示元素个数。相当于「一次走完所有珠子」的速度，远快于指数级的暴力。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（`up`, `down`），不随 `n` 增长。

---

## 心得

- 这道题的核心技巧是 **贪心 + 方向记忆**（用两个计数器记录上升/下降的最长长度）。  
- 该技巧常用于**需要交替出现两种状态**的题目，例如：  
  1. **最长交替子序列**（类似本题的变体）  
  2. **山脉数组**（先上升后下降）  
  3. **股票买卖最多一次**（寻找上升/下降的转折点）  
- **一句话总结**：只要抓住“方向变化”，每次变化都让长度+1，保持最有利的端点即可。

## 反思

- **第一反应**：先想到「枚举所有子序列」检查摆动，属于直觉的暴力思路。  
- **最容易踩的坑**：  
  - 忽略相等元素的处理，`0` 的差既不是正也不是负，会导致错误计数。  
  - 只关注局部「最大/最小」而忘记更新 `up`、`down` 同时进行，导致遗漏某些交替。  
- **下次遇到同类题**：第一步先思考「状态转移」——用几个变量记录当前的“方向”和“长度”，看能否用一次遍历完成。这样就能迅速从暴力走向线性解。