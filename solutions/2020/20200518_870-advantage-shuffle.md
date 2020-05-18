# #870. 优势洗牌 / Advantage Shuffle

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/advantage-shuffle/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2 both of the same length. The advantage of nums1 with respect to nums2 is the number of indices i for which nums1[i] > nums2[i].
Return any permutation of nums1 that maximizes its advantage with respect to nums2.

**Examples**

**Example 1:**

```
Input: nums1 = [2,7,11,15], nums2 = [1,10,4,11]
Output: [2,11,7,15]
```

**Example 2:**

```
Input: nums1 = [12,24,8,32], nums2 = [13,25,32,11]
Output: [24,32,8,12]
```

**Constraints**

- 1 <= nums1.length <= 105
- nums2.length == nums1.length
- 0 <= nums1[i], nums2[i] <= 109

---

## 题目（中文翻译）

给定两个整数数组（integer array）`nums1` 和 `nums2`，二者长度相同。**相对于** `nums2`，`nums1` 的优势（advantage）定义为满足 `nums1[i] > nums2[i]` 的下标 `i` 的数量。  
返回 `nums1` 的任意一种排列（permutation），使其相对于 `nums2` 的优势最大化。

**示例 1**  
输入: `nums1 = [2,7,11,15]`, `nums2 = [1,10,4,11]`  
输出: `[2,11,7,15]`  

**示例 2**  
输入: `nums1 = [12,24,8,32]`, `nums2 = [13,25,32,11]`  
输出: `[24,32,8,12]`  

**约束条件**  
- `1 <= nums1.length <= 10^5`  
- `nums2.length == nums1.length`  
- `0 <= nums1[i], nums2[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 `nums1` 的所有排列都枚举一遍，然后统计每一种排列与 `nums2` 的“优势”——即满足 `nums1[i] > nums2[i]` 的下标个数，取优势最大的那一个。  

- **数据结构**：我们只需要普通的 Python 列表来保存两个数组。枚举排列时会用到 `itertools.permutations`，它相当于“把所有可能的排队顺序全部列出来”。可以把它想象成把一副牌的所有洗牌方式全部展示出来。  
- **正确性**：因为我们遍历了 **所有** 可能的排列，必然能找到最优的那一个。  

显然，这种方法在理论上是对的，但会非常慢。  

#### 代码（Python）  
```python
from itertools import permutations
from typing import List

def advantage_shuffle_bruteforce(nums1: List[int], nums2: List[int]) -> List[int]:
    best_perm = None          # 用来记录当前优势最大的排列
    best_score = -1           # 记录对应的优势分数

    # 把 nums1 的所有排列枚举出来
    for perm in permutations(nums1):
        # 计算当前排列的优势分数
        score = sum(p > q for p, q in zip(perm, nums2))
        # 如果比之前的更好，就更新记录
        if score > best_score:
            best_score = score
            best_perm = perm

    # 返回列表形式的答案
    return list(best_perm)

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    print(advantage_shuffle_bruteforce([2,7,11,15], [1,10,4,11]))   # 可能得到 [2,11,7,15]
```

#### 复杂度  
- **时间复杂度**：`O(n! * n)`  
  - `n!` 是 `nums1` 所有排列的个数（比如 4! = 24），每个排列要遍历 `n` 个元素去统计优势。  
  - 用大白话说，就是“随着数组长度稍微长一点，计算量就会像炸弹一样爆炸”。  
- **空间复杂度**：`O(n)`  
  - 只需要保存当前的排列（`perm`）和几个计数器，额外空间随 `n` 线性增长。

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **“枚举所有排列”**。我们需要找到一种只遍历一次或几次数组就能得到最优排列的方法。  

观察题目：  
- 对于每一个 `nums2[i]`，我们只关心 **是否能找一个更大的 `nums1` 元素** 来“赢”它。  
- 如果我们把 `nums2` 按从小到大的顺序排好，并且同样把 `nums1` 排序，**贪心** 的想法是：**用最小的能够赢的 `nums1` 去匹配 `nums2`，否则把最小的 `nums1` “牺牲” 给最大的 `nums2`**。  

这就是经典的 “优势洗牌” 贪心策略，思路可以拆成以下几步：

1. **把 `nums2` 的下标按对应值从小到大排序**。  
   - 类比：把每个对手的实力从弱到强排好，记住他们原来的位置（下标），因为最终答案要放回原来的顺序。  
2. **把 `nums1` 从小到大排序**。  
3. 使用 **双指针**（或叫“左指针 / 右指针”）在 `nums1` 上操作：  
   - `left` 指向当前最小的未使用元素，`right` 指向当前最大的未使用元素。  
   - 从 `nums2` 的 **最小** 元素开始检查：  
     - 如果 `nums1[left] > nums2_small`，说明我们有一个能赢的牌，直接把它放到对应的下标上，`left++`。  
     - 否则，说明手里最小的牌根本赢不了这个 `nums2`，我们把 **最小的牌**（`nums1[left]`）“献祭”给 **最大的 `nums2`**（用 `right` 指向的最大 `nums1` 去对付），并把它放到最大的 `nums2` 的下标上，`right--`，`left++`（把这张最小牌标记为已用）。  
4. 这样遍历完所有 `nums2`（从小到大），就得到一个最大化优势的排列。  

**为什么贪心有效？**  
- 对于当前最小的 `nums2`，如果我们有任何能够赢的 `nums1`，把**最小的那张**用来赢是最省力的选择，留给后面的更大的 `nums2` 更大的牌。  
- 如果连最小的 `nums1` 都赢不了，那这张牌注定在任何位置都不能赢，最聪明的做法是把它丢给最大的 `nums2`（因为它本来就不可能赢），这样把“无用”牌的损失控制在最不重要的对手身上。  

#### 代码（Python）  
```python
from typing import List

def advantage_shuffle(nums1: List[int], nums2: List[int]) -> List[int]:
    n = len(nums1)

    # 1. 把 nums2 的下标按照对应的值从小到大排序
    #   idx[i] 表示第 i 小的 nums2 在原数组中的位置
    idx = sorted(range(n), key=lambda i: nums2[i])

    # 2. 把 nums1 从小到大排序
    nums1_sorted = sorted(nums1)

    # 3. 准备答案数组，先全部填 0（占位）
    answer = [0] * n

    # 双指针：左指针指向最小未使用元素，右指针指向最大未使用元素
    left, right = 0, n - 1

    # 4. 从最小的 nums2 开始遍历
    for i in idx:                     # i 是原位置
        if nums1_sorted[left] > nums2[i]:
            # 能赢：用最小的能够赢的牌
            answer[i] = nums1_sorted[left]
            left += 1                 # 这张牌已经使用
        else:
            # 赢不了：把最小的牌献祭给最大的 nums2（此时 i 是当前最小的 nums2）
            answer[i] = nums1_sorted[right]
            right -= 1                # 使用最大的牌
            left += 1                 # 同时把这张最小的牌标记为已用

    return answer

# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    print(advantage_shuffle([2,7,11,15], [1,10,4,11]))   # [2,11,7,15]（可能的最优解）
    print(advantage_shuffle([12,24,8,32], [13,25,32,11]))# [24,32,8,12]
```

#### 复杂度  
- **时间复杂度**：`O(n log n)`  
  - 对 `nums1`、`nums2` 各自排序各需要 `O(n log n)`，其余遍历是线性的 `O(n)`。  
  - 用通俗的话说，就是“先花点时间把东西排好序，然后一次快速扫描就能得到答案”。  
- **空间复杂度**：`O(n)`  
  - 需要额外的数组保存排序后的下标 `idx`、排好序的 `nums1_sorted`，以及答案 `answer`，总共和原数组等长。  

---

## 心得  

- **核心技巧**：**贪心 + 双指针 + 排序**（把问题转化为“最小能赢的配最小的对手，不能赢的牺牲给最强的对手”）。  
- **适用题型**：  
  1. “最大化匹配”类，如 **“Assign Cookies”**（分配饼干）  
  2. “相对大小比较”类，如 **“Maximum Number of Events That Can Be Attended”**（最大可参加活动数）  
  3. “排列对抗”类，如 **“Permute Array to Maximize Score”**（排列数组以最大化得分）  
- **一句话总结**：把两边都排好序，用最小能赢的牌去赢最弱的对手，剩下的牌统统丢给最强的对手，优势自然最大。

---

## 反思  

- **第一反应**：看到“优势”两个数组，就想到**逐个比较**，于是想到暴力枚举所有排列。  
- **最容易踩的坑**：  
  - 忘记把 `nums2` 的原始下标记下来，导致答案顺序错误。  
  - 在“献祭”时只用了最大牌，却忘了把最小牌也标记为已用，导致重复使用。  
  - 边界条件：数组长度为 1 时仍需正常工作。  
- **下次类似题的第一步**：**先把两个数组排序并记录原位置信息**，再思考“最小能赢的配最小的，不能赢的丢给最大的”这种贪心配对策略。