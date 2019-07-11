# #491. 非递减子序列 / Non-decreasing Subsequences

> 难度：中等 · 标签：Array、Hash Table、Backtracking、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/non-decreasing-subsequences/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return all the different possible non-decreasing subsequences of the given array with at least two elements. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: nums = [4,6,7,7]
Output: [[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]
```

**Example 2:**

```
Input: nums = [4,4,3,2,1]
Output: [[4,4]]
```

**Constraints**

- 1 <= nums.length <= 15
- -100 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个整数数组 `nums`，返回该数组中所有 **不同的**、长度 **至少为 2** 的非递减子序列（non-decreasing subsequence）。答案可以以任意顺序返回。

**示例 1**  
输入: `nums = [4,6,7,7]`  
输出: `[[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]`

**示例 2**  
输入: `nums = [4,4,3,2,1]`  
输出: `[[4,4]]`

**约束条件**  

- `1 <= nums.length <= 15`  
- `-100 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举所有子序列**，检查它们是否满足“非递减且长度≥2”。  
- **子序列**：可以把数组想成一本书，每一页上有一个数字。子序列相当于从这本书里挑出若干页，保持原来的顺序，但可以跳过中间的页。  
- **枚举**：对长度为 `n` 的数组，一共有 `2ⁿ` 种挑选方式（每个位置要么选，要么不选），这就是“幂集”。我们可以用二进制的 **位掩码** 来表示一种挑选方式：第 `i` 位是 1 表示挑第 `i` 个元素，0 表示不挑。  

枚举完每一种掩码后，把对应的元素取出来形成一个子序列，判断：
1. 长度是否 ≥ 2；
2. 是否非递减（即后一个数不小于前一个数）。

只要满足，就把它加入结果集合。因为不同的掩码有可能得到相同的子序列（比如数组里有重复数字），我们需要用 **哈希表**（在 Python 中是 `set`）去重。哈希表可以类比成一本“大词典”，把子序列（转成元组）当作单词，出现过的单词直接记下来，避免重复。

这个方法一定能得到所有合法子序列，因为我们把 **所有可能的挑选方式** 都遍历了一遍。

#### 代码（Python）

```python
from typing import List

def findSubsequences(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    res_set = set()                     # 用 set 去重，存放元组形式的子序列

    # 1 << n 表示 2 的 n 次方，即所有位掩码的上界
    for mask in range(1, 1 << n):       # 从 1 开始，排除全 0（空子序列）
        subseq = []
        for i in range(n):
            # 判断第 i 位是否为 1，若是则把 nums[i] 加入当前子序列
            if mask & (1 << i):
                subseq.append(nums[i])

        # 2 条筛选条件
        if len(subseq) >= 2:            # 长度至少为 2
            # 检查是否非递减
            ok = True
            for j in range(1, len(subseq)):
                if subseq[j] < subseq[j - 1]:
                    ok = False
                    break
            if ok:
                # 把列表转成元组放进 set，自动去重
                res_set.add(tuple(subseq))

    # 把 set 里的元组再转回列表返回
    return [list(t) for t in res_set]
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ * n)`  
  - `2ⁿ` 是所有位掩码的数量（因为每个元素有选或不选两种可能）。  
  - 对每个掩码我们要遍历一次数组收集元素，又要检查一次非递减，最多 `n` 次操作。  
  - 用大白话说，就是“当数组长度稍大时，时间会像指数一样飞快增长”。

- **空间复杂度**：`O(2ⁿ)`（最坏情况）  
  - 结果集合里可能保存所有合法子序列，数量同样受 `2ⁿ` 的上限限制。  
  - 另外还有 `O(n)` 的临时列表 `subseq`。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**遍历全部 2ⁿ 种子序列**，其中大多数都不满足非递减条件，浪费大量时间。  
我们可以**在构造子序列的过程中就提前剪枝**，只保留有希望成为合法答案的分支。  
这类“逐步构造、回溯” 的思路非常适合 **回溯（Backtracking）**：

1. **从左到右遍历数组**，维护一个“当前正在构造的子序列”。  
2. 对每个位置 `i`，有两种选择：  
   - **跳过** `nums[i]`（不放进子序列），继续递归。  
   - **加入** `nums[i]`（前提是加入后仍保持非递减），再递归。  
3. 当递归结束（遍历完所有元素）时，如果当前子序列长度 ≥ 2，就把它加入答案集合。  
4. 为了避免重复子序列（尤其是数组中出现相同数字时），**在同一层递归里使用一个局部哈希表 `used` 记录本层已经尝试过的数字**。如果本层已经尝试过 `nums[i]`，就不要再用它了。这样可以把 `[4,6,7,7]` 中的两次 `7` 产生的相同子序列过滤掉。

**核心数据结构**  
- **列表 `path`**：记录当前构造的子序列（类似一条正在走的路）。  
- **集合 `ans`**：存放所有合法子序列的 **元组**，自动去重。  
- **局部集合 `used`**：在每层递归中防止同一数字被重复尝试。

**为什么这样快？**  
- 每次加入新数字前都会检查 `num >= last`，不满足就直接 **剪枝**（不往下走），大幅降低搜索空间。  
- 由于数组长度最多 15，回溯的深度最多 15，时间复杂度大约是 `O(k * 2^k)`（k 为合法子序列的个数），远小于遍历所有 `2ⁿ` 种子序列。

#### 代码（Python）

```python
from typing import List, Set, Tuple

def findSubsequences(nums: List[int]) -> List[List[int]]:
    n = len(nums)
    ans: Set[Tuple[int, ...]] = set()   # 用 set 存放元组，自动去重

    def backtrack(start: int, path: List[int]) -> None:
        """
        start : 下一次决定是否加入的起始下标
        path  : 当前已经构造好的子序列（保持非递减）
        """
        if len(path) >= 2:               # 合法子序列直接加入答案
            ans.add(tuple(path))

        if start == n:                   # 已经遍历完所有元素，结束本层
            return

        used = set()                     # 本层已经尝试过的数字
        for i in range(start, n):
            if nums[i] in used:          # 同层去重：本层已经用了相同的数字
                continue
            if not path or nums[i] >= path[-1]:
                used.add(nums[i])        # 记录本层使用的数字
                path.append(nums[i])     # 选取 nums[i]
                backtrack(i + 1, path)   # 递归处理后面的元素
                path.pop()               # 恢复现场，回溯

    backtrack(0, [])
    return [list(t) for t in ans]         # 把元组转回列表返回
```

#### 复杂度

- **时间复杂度**：`O(k * n)`（近似）  
  - `k` 为最终合法子序列的数量（最坏情况下仍然指数级，但远小于 `2ⁿ`）。  
  - 每条合法路径在递归时最多遍历 `n` 次元素检查。  
  - 与暴力解相比，**剪枝** 极大降低了实际运行时间。

- **空间复杂度**：`O(k + n)`  
  - `k` 用于保存答案集合。  
  - 递归栈最多 `n` 层（因为数组长度 ≤ 15），属于线性空间。

---

## 心得

- **核心技巧**：回溯 + 同层去重（使用哈希表）  
- **适用题型**：  
  1. “所有子集/子序列” 类问题（如 `Subsets`, `Combination Sum`）  
  2. 需要 **保持顺序且满足单调性** 的序列问题（如 `Increasing Subsequence`, `Longest Increasing Subsequence` 的变形）  
- **一句话总结**：**在构造的过程中随时检查约束并剪枝，同层去重防止重复子序列**，就是这道题的解题钥匙。

---

## 反思

- **第一反应**：直接想到遍历所有子序列（位掩码），因为最容易实现。  
- **最容易踩的坑**：  
  - 忘记对结果去重，导致出现重复子序列。  
  - 没有在递归时检查 `num >= last`，会产生大量非法分支，导致超时。  
  - 同层去重忘记使用 `used`，在有相同数字时会重复产生相同路径。  
- **下次遇到同类题**：第一步先思考 **“是否可以在生成过程中就验证约束并剪枝”**，再决定是否需要 **同层去重**，这样往往能直接得到高效的回溯解法。