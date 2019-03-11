# #334. 递增三元子序列 / Increasing Triplet Subsequence

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/increasing-triplet-subsequence/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, return true if there exists a triple of indices (i, j, k) such that i < j < k and nums[i] < nums[j] < nums[k]. If no such indices exists, return false.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: true
Explanation: Any triplet where i < j < k is valid.
```

**Example 2:**

```
Input: nums = [5,4,3,2,1]
Output: false
Explanation: No triplet exists.
```

**Example 3:**

```
Input: nums = [2,1,5,0,4,6]
Output: true
Explanation: The triplet (3, 4, 5) is valid because nums[3] == 0 < nums[4] == 4 < nums[5] == 6.
```

**Constraints**

- 1 <= nums.length <= 5 * 105
- -231 <= nums[i] <= 231 - 1

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，如果存在一组三元组（triplet）索引 `(i, j, k)` 满足 `i < j < k` 且 `nums[i] < nums[j] < nums[k]`，返回 `true`；否则返回 `false`。  

**示例**  

**示例 1**  
输入: `nums = [1,2,3,4,5]`  
输出: `true`  
解释: 任意满足 `i < j < k` 的三元组都是有效的。  

**示例 2**  
输入: `nums = [5,4,3,2,1]`  
输出: `false`  
解释: 不存在满足条件的三元组。  

**示例 3**  
输入: `nums = [2,1,5,0,4,6]`  
输出: `true`  
解释: 三元组 `(3, 4, 5)` 有效，因为 `nums[3] == 0 < nums[4] == 4 < nums[5] == 6`。  

**约束条件**  

- `1 <= nums.length <= 5 * 10^5`  
- `-2^31 <= nums[i] <= 2^31 - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里所有可能的三元组都枚举一遍，只要找到满足  

```
i < j < k 且 nums[i] < nums[j] < nums[k]
```

的组合，就返回 `True`，否则返回 `False`。  

- **使用的数据结构**：只需要原始的列表 `nums`，不需要额外的数据结构。可以把「遍历所有三元组」想象成在一本书里随意挑三页，检查这三页上的数字是否递增。  
- **为什么正确**：因为我们把所有合法的 `(i, j, k)` 都检查了一遍，只要答案是 `True`，必然会在某一次检查中被发现；如果所有组合都不满足条件，那么答案一定是 `False`。  
- **时间/空间复杂度**：  
  - 时间上要嵌套三层循环，每层最多遍历 `n` 次，整体是 `O(n³)`。把 `O(n³)` 想象成「把 n 本书每本都和其他两本书配对」的工作量，随 `n` 增大会非常快地爆炸。  
  - 空间上只使用了常数个额外变量，`O(1)`。

#### 代码（Python）

```python
from typing import List

def increasing_triplet_bruteforce(nums: List[int]) -> bool:
    n = len(nums)
    # 第一个循环找 i
    for i in range(n - 2):
        # 第二个循环找 j，必须在 i 之后
        for j in range(i + 1, n - 1):
            # 只有当 nums[i] < nums[j] 时才继续找 k，省一点点时间
            if nums[i] < nums[j]:
                # 第三个循环找 k，必须在 j 之后
                for k in range(j + 1, n):
                    if nums[j] < nums[k]:
                        # 找到递增的三元组，直接返回 True
                        return True
    # 所有可能都检查完了，仍未找到
    return False
```

#### 复杂度

- **时间复杂度**：`O(n³)` — 需要三层嵌套循环，随着数组长度 `n` 的增长，运算次数会呈立方增长，`n=1000` 时就已经是 10⁹ 次了，实际会超时。  
- **空间复杂度**：`O(1)` — 只用了常数个临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们不停地在整个数组里寻找第三个数 `k`。其实我们只需要维护两个「最小的候选」即可：

1. **first**：到目前为止看到的最小的数（可能是递增三元组的第一个元素）。  
2. **second**：在 `first` 之后，能够比 `first` 大的最小数（可能是递增三元组的第二个元素）。  

遍历数组时：
- 若当前数 `x` 小于或等于 `first`，说明我们找到了更小的第一个元素，更新 `first = x`。  
- 否则若 `x` 小于或等于 `second`，说明它可以成为更好的第二个元素（比之前的 `second` 更小），更新 `second = x`。  
- 否则 `x` 大于 `second`，说明我们已经找到了 `first < second < x`，直接返回 `True`。  

这套思路叫 **贪心（Greedy）**：每一步都尽量让 `first`、`second` 保持最小，从而为后面的数留下最大可能的空间。  

- **使用的数据结构**：只用两个变量 `first`、`second`，相当于在记一本字典里「最小的词」和「次小的词」的页码。  
- **为什么正确**：如果存在递增三元组，那么在遍历到它们的第三个元素时，`first` 与 `second` 必然已经被更新为该三元组的前两个元素（或更小的元素），因此第三个元素一定会触发 `x > second`，返回 `True`。  
- **时间复杂度**：只需要一次线性遍历，`O(n)`。  
- **空间复杂度**：仅用常数个变量，`O(1)`。

#### 代码（Python）

```python
from typing import List

def increasing_triplet(nums: List[int]) -> bool:
    # 把 first、second 初始化为正无穷，代表“还没找到”
    first = second = float('inf')

    for x in nums:
        if x <= first:
            # 找到更小的第一个元素
            first = x
        elif x <= second:
            # 找到比 first 大，但比 second 小的元素，更新 second
            second = x
        else:
            # x > second，说明已经找到了递增的三元组
            return True
    # 遍历结束仍未找到
    return False
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，`n` 增大时运算次数线性增长，`n=10⁶` 仍然可在毫秒级完成。  
- **空间复杂度**：`O(1)` — 只用了两个额外变量，和输入规模无关。

---

## 心得

- 这道题考察的核心技巧是 **贪心维护最小的两层候选**（two‑pointer / two‑variable greedy），在不需要额外结构的情况下完成线性时间判定。  
- 该技巧常见于：  
  1. **最长递增子序列长度为 3 的判定**（本题）。  
  2. **最大子数组乘积**（需要维护最大/最小两个乘积）。  
  3. **寻找四元组/五元组递增**（可以把思路推广为维护 k‑1 个变量）。  
- **解题钥匙**：用「尽可能小」的前两个数把空间留给后面的数。

## 反思

- **第一反应**：直接想遍历所有三元组，写出暴力三层循环。  
- **最容易踩的坑**：  
  - 忘记在更新 `first`、`second` 时使用 “`<=`”，导致相等的数被误当作递增。  
  - 对负数或极大/极小值没有特殊处理，使用 `float('inf')` 初始化可以避免溢出。  
- **下次遇到同类题**：第一步先思考「是否能只维护几个极值」而不是「全部枚举」，把注意力放在「把问题的搜索空间压到最小」上。