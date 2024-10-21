# #2908. 山峰三元组的最小和 I / Minimum Sum of Mountain Triplets I

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/minimum-sum-of-mountain-triplets-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of integers.
A triplet of indices (i, j, k) is a mountain if:
Return the minimum possible sum of a mountain triplet of nums. If no such triplet exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [8,6,1,5,3]
Output: 9
Explanation: Triplet (2, 3, 4) is a mountain triplet of sum 9 since: 
- 2 < 3 < 4
- nums[2] < nums[3] and nums[4] < nums[3]
And the sum of this triplet is nums[2] + nums[3] + nums[4] = 9. It can be shown that there are no mountain triplets with a sum of less than 9.
```

**Example 2:**

```
Input: nums = [5,4,8,7,10,2]
Output: 13
Explanation: Triplet (1, 3, 5) is a mountain triplet of sum 13 since: 
- 1 < 3 < 5
- nums[1] < nums[3] and nums[5] < nums[3]
And the sum of this triplet is nums[1] + nums[3] + nums[5] = 13. It can be shown that there are no mountain triplets with a sum of less than 13.
```

**Example 3:**

```
Input: nums = [6,5,4,3,4,5]
Output: -1
Explanation: It can be shown that there are no mountain triplets in nums.
```

**Constraints**

- 3 <= nums.length <= 50
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个 **0 索引**（0-indexed）的整数数组 `nums`。  
若索引三元组 `(i, j, k)` 满足以下条件，则称其为 **山峰**（mountain）三元组：

- `i < j < k`
- `nums[i] < nums[j]` 且 `nums[k] < nums[j]`

返回 `nums` 中任意山峰三元组的 **最小可能和**。如果不存在满足条件的三元组，返回 `-1`。

---

### 示例

#### 示例 1
**输入**: `nums = [8,6,1,5,3]`  
**输出**: `9`  
**解释**: 三元组 `(2, 3, 4)` 是一个山峰三元组，和为 `9`，因为  
- `2 < 3 < 4`  
- `nums[2] < nums[3]` 且 `nums[4] < nums[3]`  
其和为 `nums[2] + nums[3] + nums[4] = 9`。可以证明不存在和小于 `9` 的山峰三元组。

#### 示例 2
**输入**: `nums = [5,4,8,7,10,2]`  
**输出**: `13`  
**解释**: 三元组 `(1, 3, 5)` 是一个山峰三元组，和为 `13`，因为  
- `1 < 3 < 5`  
- `nums[1] < nums[3]` 且 `nums[5] < nums[3]`  
其和为 `nums[1] + nums[3] + nums[5] = 13`。可以证明不存在和小于 `13` 的山峰三元组。

#### 示例 3
**输入**: `nums = [6,5,4,3,4,5]`  
**输出**: `-1`  
**解释**: 可以证明 `nums` 中不存在任何山峰三元组。

---

### 约束

- `3 <= nums.length <= 50`
- `1 <= nums[i] <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有可能的三元组** 都枚举一遍，检查它们是否满足“山形”条件，再把满足条件的三元组的和取最小。  

- **枚举三元组**：遍历下标 `i、j、k`，要求 `0 ≤ i < j < k < n`。  
- **山形判定**：只要 `nums[i] < nums[j]` 且 `nums[k] < nums[j]`，这三个下标就是一座山。  
- **记录最小和**：每找到一座山，就把 `nums[i] + nums[j] + nums[k]` 与当前最小值比较，取更小的那个。  

> **类比**：把数组想象成一排小山坡，暴力解相当于把每个人手里拿的三根棍子（下标）全都试一遍，看看能不能搭成一座“山”。虽然能保证找到答案，但要试的组合很多，效率低下。

因为题目只要求返回最小的山形三元组的和，这种“全盘检查”的方法必然是正确的——只要遍历了所有合法组合，就不可能漏掉最小的那一个。

#### 代码（Python）

```python
from math import inf
from typing import List

def minimumSum(nums: List[int]) -> int:
    n = len(nums)
    ans = inf                     # 用一个很大的数表示“目前还没有找到山形”

    # 三层循环枚举所有 i < j < k
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] >= nums[j]:   # 先判断左侧是否满足 nums[i] < nums[j]，不满足直接跳过
                continue
            for k in range(j + 1, n):
                if nums[k] >= nums[j]:   # 再判断右侧是否满足 nums[k] < nums[j]
                    continue
                # 此时 (i, j, k) 是一座山，计算它的和
                cur_sum = nums[i] + nums[j] + nums[k]
                ans = min(ans, cur_sum)   # 保留更小的和

    return -1 if ans == inf else ans    # 若 ans 没被更新，说明不存在山形
```

#### 复杂度  

- **时间复杂度**：`O(n³)`。  
  - “三层循环”意味着如果数组长度是 `n`，最坏情况下要检查大约 `n³/6` 个三元组。  
  - 大白话：如果 `n = 50`，最多要尝试 20,000 多次组合，虽然在本题数据范围还能跑完，但当 `n` 更大时就会“卡死”。  

- **空间复杂度**：`O(1)`。  
  - 只用了常数级别的额外变量（`ans`、`cur_sum` 等），不随 `n` 增长。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **重复遍历**：对每一个中间下标 `j`，我们都要把左边所有元素和右边所有元素重新扫描一遍来找满足 `nums[i] < nums[j]`、`nums[k] < nums[j]` 的最小值。  

**优化目标**：对每个 `j`，直接得到  
- 左侧 **最小的**、且 **小于** `nums[j]` 的数 `left_min[j]`  
- 右侧 **最小的**、且 **小于** `nums[j]` 的数 `right_min[j]`  

有了这两个最小值，山形三元组的最小和就可以直接算：  

```
candidate = left_min[j] + nums[j] + right_min[j]
```

只要遍历所有 `j`，取最小的 `candidate` 即可。

**如何得到 left_min / right_min？**  
- 对每个 `j`，我们只需要在它左边（或右边）**一次**线性扫描，找出满足 `< nums[j]` 的最小元素。  
- 把这个过程对所有 `j` 重复一次，总体时间是 `O(n²)`（每个方向各 `n` 次遍历，每次最多检查 `n` 个元素），空间只需要保存两个长度为 `n` 的数组。

> **类比**：把数组看成一排房子。我们想在每栋房子 `j` 的左边找一间“更便宜且更小”的房子 `i`，右边同理。最优解相当于先给每栋房子贴上左边最近且最便宜的标签 `left_min`，右边同理，然后再挑出最省钱的组合。

**步骤概览**  

1. **预处理左侧最小值**  
   - 初始化 `left_min` 为 `inf`（表示不存在）。  
   - 对每个 `j`（从左到右），遍历 `i < j`，如果 `nums[i] < nums[j]`，就更新 `left_min[j]` 为更小的 `nums[i]`。  

2. **预处理右侧最小值**  
   - 同理，从右往左遍历，得到 `right_min[j]`。  

3. **求答案**  
   - 对每个 `j`，如果 `left_min[j]` 与 `right_min[j]` 都不是 `inf`，说明 `j` 能构成山形，计算 `candidate` 并取最小。  
   - 若最终没有合法 `candidate`，返回 `-1`。  

#### 代码（Python）

```python
from math import inf
from typing import List

def minimumSum(nums: List[int]) -> int:
    n = len(nums)
    left_min = [inf] * n          # left_min[j] = 最左侧满足 nums[i] < nums[j] 的最小值
    right_min = [inf] * n         # right_min[j] = 最右侧满足 nums[k] < nums[j] 的最小值

    # 计算 left_min
    for j in range(n):
        for i in range(j):        # i 遍历 j 左侧所有位置
            if nums[i] < nums[j]:
                left_min[j] = min(left_min[j], nums[i])

    # 计算 right_min（从右往左更方便）
    for j in range(n - 1, -1, -1):
        for k in range(j + 1, n): # k 遍历 j 右侧所有位置
            if nums[k] < nums[j]:
                right_min[j] = min(right_min[j], nums[k])

    ans = inf
    # 结合中间位置 j，得到山形三元组的最小和
    for j in range(n):
        if left_min[j] != inf and right_min[j] != inf:
            ans = min(ans, left_min[j] + nums[j] + right_min[j])

    return -1 if ans == inf else ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - 两次双层循环（左侧、右侧）各需要 `≈ n·(n-1)/2` 次比较，总体是二次方级别。  
  - 与暴力解的 `O(n³)` 相比，减少了一层循环，**速度提升大约是 `n` 倍**（在最坏情况下从 20,000 次下降到约 1,250 次，当 `n=50` 时）。  

- **空间复杂度**：`O(n)`。  
  - 需要额外的两个长度为 `n` 的数组 `left_min`、`right_min`，随着输入规模线性增长。  

---

## 心得  

- **核心技巧**：对每个候选中间元素，**分别维护左侧和右侧满足条件的最小值**，从而把三重循环降到双重循环。  
- **适用题型**：  
  1. “**最小/最大三元组**” 类问题（如 *Minimum Sum of Mountain Triplets II*、*Maximum Sum of Increasing Triplet*）。  
  2. “**左/右侧最近满足条件的元素**” 题目（如 *Nearest Smaller Element*、*Maximum Width Ramp*）。  
- **解题钥匙**：**先把局部最优（左/右的最小）算好，再在中间位置一次性合并**。

---

## 反思  

- **第一反应**：直接想到“三层循环遍历所有 i、j、k”。这在没有进一步思考时是最自然的做法。  
- **最容易踩的坑**：  
  - 忘记检查左、右两侧都必须存在满足 `< nums[mid]` 的元素，导致错误地把只有一侧满足的三元组计入答案。  
  - 在实现 `left_min`、`right_min` 时忘记初始化为 `inf`，导致误把未找到的情况当作合法值。  
- **下次思路**：看到“**在左侧找满足某条件的最小/最大**”或“**在右侧找满足某条件的最小/最大**”时，第一步就考虑 **预处理**（一次遍历或双层遍历）来保存这些信息，而不是每次都重新扫描。这样可以把指数级别的暴力直接压缩到二次或一次遍历的范围。