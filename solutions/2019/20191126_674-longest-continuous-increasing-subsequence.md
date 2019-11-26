# #674. 最长连续递增子序列 / Longest Continuous Increasing Subsequence

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/longest-continuous-increasing-subsequence/)

---

## 题目（英文原版）

**Description**

Given an unsorted array of integers nums, return the length of the longest continuous increasing subsequence (i.e. subarray). The subsequence must be strictly increasing.
A continuous increasing subsequence is defined by two indices l and r (l < r) such that it is [nums[l], nums[l + 1], ..., nums[r - 1], nums[r]] and for each l <= i < r, nums[i] < nums[i + 1].

**Examples**

**Example 1:**

```
Input: nums = [1,3,5,4,7]
Output: 3
Explanation: The longest continuous increasing subsequence is [1,3,5] with length 3.
Even though [1,3,5,7] is an increasing subsequence, it is not continuous as elements 5 and 7 are separated by element
4.
```

**Example 2:**

```
Input: nums = [2,2,2,2,2]
Output: 1
Explanation: The longest continuous increasing subsequence is [2] with length 1. Note that it must be strictly
increasing.
```

**Constraints**

- 1 <= nums.length <= 104
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个无序的整数数组 `nums`，返回最长连续递增子序列（subarray）的长度。子序列必须严格递增。

连续递增子序列由两个索引 `l` 和 `r`（`l < r`）定义，其形式为 `[nums[l], nums[l + 1], ..., nums[r - 1], nums[r]]`，并且对于所有 `l ≤ i < r`，都有 `nums[i] < nums[i + 1]`。

## 示例

### 示例 1
**输入**  
`nums = [1,3,5,4,7]`

**输出**  
`3`

**解释**  
最长的连续递增子序列是 `[1,3,5]`，长度为 3。虽然 `[1,3,5,7]` 也是递增的，但它不是连续的，因为元素 5 与 7 之间被元素 4 隔开。

### 示例 2
**输入**  
`nums = [2,2,2,2,2]`

**输出**  
`1`

**解释**  
最长的连续递增子序列是 `[2]`，长度为 1。需要注意的是，子序列必须严格递增。

## 约束条件
- `1 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的连续子数组**，检查每个子数组是否严格递增，若是则记录它的长度，最后取最大值。

- **数据结构**：只需要原始的 `list`（数组）本身。我们把数组想象成一排排的书，暴力解就是把每一本书当作起点，往后一直翻，直到发现后面的书不比前一本厚（即不再递增），然后把这段连续的书的数量记下来。  
- **正确性**：因为我们遍历了所有可能的起点 `l`，并且对每个起点尝试所有可能的结束位置 `r (l ≤ r)`，只要子数组满足递增条件，就会被计入比较。所有合法的连续递增子数组都被检查到了，所以最大长度一定被找到。  
- **复杂度直观解释**：  
  - **时间复杂度 O(n²)**：想象有 `n` 本书，每本书都要当一次起点，然后往后检查最多 `n` 本书是否递增。第一本检查 `n` 次，第二本检查 `n‑1` 次，……，总次数大约是 `n + (n‑1) + … + 1 ≈ n²/2`，这就是 O(n²)。  
  - **空间复杂度 O(1)**：只用几个计数变量，不会随输入规模增长而占用更多内存。

#### 代码（Python）

```python
from typing import List

class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        """暴力解：枚举所有连续子数组，返回最长递增子数组的长度"""
        n = len(nums)
        if n == 0:
            return 0

        max_len = 1                     # 当前找到的最长长度，最小就是 1（单个元素）
        for start in range(n):          # 把每个位置当作子数组的左端点
            cur_len = 1                 # 子数组至少包含 start 本身
            # 从 start 往后逐个检查是否递增
            for end in range(start + 1, n):
                if nums[end] > nums[end - 1]:
                    cur_len += 1       # 仍然递增，长度加 1
                else:
                    break              # 一旦不递增，就不能再往后扩展了
            max_len = max(max_len, cur_len)  # 更新全局最大值
        return max_len
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 由于两层循环，最坏情况下每个起点都要遍历到数组末尾，操作次数随 `n` 的平方增长。  
- **空间复杂度**：`O(1)` — 只用了常数个整型变量 (`max_len、cur_len、start、end`)。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都从头重新遍历**，实际上我们只需要一次线性扫描就能得到答案。关键观察是：

- 如果 `nums[i] > nums[i‑1]`，说明以 `i` 结尾的递增子数组可以把前面的长度直接延伸 1。
- 否则，递增序列被打断，需要从 `i` 重新开始计数。

于是我们可以用 **两个变量**：

1. `cur_len` – 当前正在统计的递增子数组的长度（以当前位置为结尾）。
2. `max_len` – 全局最大长度。

遍历数组一次（相当于把书一排排往后翻），每次检查相邻两本书的厚度关系，决定是继续延伸还是重新计数。这个过程就是 **滑动窗口 / 双指针** 的最简形式——左指针隐式地随 `cur_len` 归零而移动。

**为什么只需要一次遍历？**  
因为递增性是“传递的”：只要前面的序列是递增的，加入一个更大的元素后仍然递增；一旦出现不递增的情况，之前的所有信息都不再有用，只需要从当前元素重新开始。这正好对应 O(n) 的线性扫描。

**类比**：想象在跑步比赛中，你记录每一步是否比前一步快。如果快，就把当前连续加速的距离累加；如果慢，就把计数器归零，从这一步重新开始。最终的最大计数器就是最长加速段的长度。

#### 代码（Python）

```python
from typing import List

class Solution:
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        """最优解：一次遍历，维护当前递增段长度和全局最大长度"""
        n = len(nums)
        if n == 0:
            return 0

        max_len = 1          # 至少有一个元素
        cur_len = 1          # 当前递增段的长度

        for i in range(1, n):               # 从第二个元素开始检查
            if nums[i] > nums[i - 1]:        # 递增，当前段可以延伸
                cur_len += 1                # 长度加一
            else:                            # 不递增，重新从当前元素开始计数
                cur_len = 1                 # 重新计数，长度恢复为 1（只有自己）
            max_len = max(max_len, cur_len) # 更新全局最大值

        return max_len
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，操作次数随 `n` 成线性增长。相比暴力解的 `n²`，快了很多。  
- **空间复杂度**：`O(1)` — 只用了常数个变量 (`max_len、cur_len、i`)。

---

## 心得

- **核心技巧**：**一次遍历维护递增段长度**（滑动窗口/双指针的极简版）。  
- **适用的类似题目**  
  1. *Longest Continuous Decreasing Subsequence*（最长连续递减子序列）  
  2. *Maximum Consecutive Ones*（最大连续 1 的个数）  
  3. *Longest Subarray With Absolute Diff Less Than or Equal to Limit*（满足差值限制的最长子数组）  
- **一句话总结解题钥匙**：**把“是否递增”转化为“是否可以把当前计数器加 1”，一旦断裂就把计数器归零**。

---

## 反思

- **第一反应**：看到“连续子数组”，自然想到枚举所有子数组——也就是暴力解。  
- **最容易踩的坑**  
  - 输入只有一个元素时，答案应为 1，需要提前处理空数组或单元素的情况。  
  - 元素相等不算递增，必须使用严格的 “>” 而不是 “>=”。  
  - 在遍历时忘记在不递增时把 `cur_len` 重新设为 1（而不是 0），否则会把单个元素的长度漏掉。  
- **下次遇到同类题的第一步**：先问自己“这个属性（递增、递减、满足某种条件）能否在一次扫描中维护？”如果能，就立刻尝试用“当前段长度 + 全局最大值”这种滑动窗口思路来实现。