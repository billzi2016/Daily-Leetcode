# #2155. 二进制数组的最高得分划分 / All Divisions With the Highest Score of a Binary Array

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/all-divisions-with-the-highest-score-of-a-binary-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed binary array nums of length n. nums can be divided at index i (where 0 <= i <= n) into two arrays (possibly empty) numsleft and numsright:
The division score of an index i is the sum of the number of 0's in numsleft and the number of 1's in numsright.
Return all distinct indices that have the highest possible division score. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: nums = [0,0,1,0]
Output: [2,4]
Explanation: Division at index
- 0: numsleft is []. numsright is [0,0,1,0]. The score is 0 + 1 = 1.
- 1: numsleft is [0]. numsright is [0,1,0]. The score is 1 + 1 = 2.
- 2: numsleft is [0,0]. numsright is [1,0]. The score is 2 + 1 = 3.
- 3: numsleft is [0,0,1]. numsright is [0]. The score is 2 + 0 = 2.
- 4: numsleft is [0,0,1,0]. numsright is []. The score is 3 + 0 = 3.
Indices 2 and 4 both have the highest possible division score 3.
Note the answer [4,2] would also be accepted.
```

**Example 2:**

```
Input: nums = [0,0,0]
Output: [3]
Explanation: Division at index
- 0: numsleft is []. numsright is [0,0,0]. The score is 0 + 0 = 0.
- 1: numsleft is [0]. numsright is [0,0]. The score is 1 + 0 = 1.
- 2: numsleft is [0,0]. numsright is [0]. The score is 2 + 0 = 2.
- 3: numsleft is [0,0,0]. numsright is []. The score is 3 + 0 = 3.
Only index 3 has the highest possible division score 3.
```

**Example 3:**

```
Input: nums = [1,1]
Output: [0]
Explanation: Division at index
- 0: numsleft is []. numsright is [1,1]. The score is 0 + 2 = 2.
- 1: numsleft is [1]. numsright is [1]. The score is 0 + 1 = 1.
- 2: numsleft is [1,1]. numsright is []. The score is 0 + 0 = 0.
Only index 0 has the highest possible division score 2.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- nums[i] is either 0 or 1.

---

## 题目（中文翻译）

给定一个下标从 0 开始的二进制数组 `nums`，长度为 `n`。可以在索引 `i`（其中 `0 <= i <= n`）处将数组划分为两个（可能为空的）子数组 `numsleft` 和 `numsright`：  
- `numsleft` 包含 `nums[0]` 到 `nums[i‑1]`（若 `i = 0` 则为空）。  
- `numsright` 包含 `nums[i]` 到 `nums[n‑1]`（若 `i = n` 则为空）。  

索引 `i` 的**划分得分 (division score)** 定义为 `numsleft` 中 `0` 的个数加上 `numsright` 中 `1` 的个数之和。  

返回所有拥有最高可能划分得分的不同索引。答案的顺序不限。

**示例 1**  
```text
Input: nums = [0,0,1,0]
Output: [2,4]
Explanation: 在各个索引处的划分如下：
- 0: numsleft = []，numsright = [0,0,1,0]，得分 = 0 + 1 = 1。
- 1: numsleft = [0]，numsright = [0,1,0]，得分 = 1 + 1 = 2。
- 2: numsleft = [0,0]，numsright = [1,0]，得分 = 2 + 1 = 3。
- 3: numsleft = [0,0,1]，numsright = [0]，得分 = 2 + 0 = 2。
- 4: numsleft = [0,0,1,0]，numsright = []，得分 = 3 + 0 = 3。

最高得分为 3，对应的索引为 2 和 4。
```

**示例 2**  
```text
Input: nums = [0,0,0]
Output: [3]
Explanation: 在各个索引处的划分如下：
- 0: numsleft = []，numsright = [0,0,0]，得分 = 0 + 0 = 0。
- 1: numsleft = [0]，numsright = [0,0]，得分 = 1 + 0 = 1。
- 2: numsleft = [0,0]，numsright = [0]，得分 = 2 + 0 = 2。
- 3: numsleft = [0,0,0]，numsright = []，得分 = 3 + 0 = 3。

只有索引 3 的得分最高，为 3。
```

**示例 3**  
```text
Input: nums = [1,1]
Output: [0]
Explanation: 在各个索引处的划分如下：
- 0: numsleft = []，numsright = [1,1]，得分 = 0 + 2 = 2。
- 1: numsleft = [1]，numsright = [1]，得分 = 0 + 1 = 1。
- 2: numsleft = [1,1]，numsright = []，得分 = 0 + 0 = 0。

只有索引 0 的得分最高，为 2。
```

**约束条件**  
- `n == nums.length`  
- `1 <= n <= 10^5`  
- `nums[i]` 仅为 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历所有可能的分割点 `i`**（`0 ≤ i ≤ n`），  
- 把左边的子数组 `numsleft = nums[0:i]`（左闭右开）  
- 把右边的子数组 `numsright = nums[i:n]`  

然后分别统计  
- `left_zero`：左边 0 的个数  
- `right_one`：右边 1 的个数  

分数 = `left_zero + right_one`。把每个分数记下来，最后找出最大的分数对应的所有下标即可。

> **类比**：把 `nums` 想象成一本书的章节，`i` 是“分卷线”。左边的 0 就像是左卷里出现的“错误页”，右边的 1 像是右卷里出现的“成功章节”。我们要把“错误页数 + 成功章节数”最大化。

**为什么正确**  
- 我们枚举了 **所有** 合法的分割位置，且对每个位置都算出了准确的分数。最大分数必然出现在这 `n+1` 种情况中，所以返回的下标必然是答案。

**时间/空间复杂度**  
- 对每个 `i` 都要遍历一次左子数组计 0，遍历一次右子数组计 1，时间复杂度是 `O(n^2)`。  
  - **大白话**：如果 `n=10⁴`，相当于要做 10⁴ × 10⁴ ≈ 1 亿次计数，显然太慢。  
- 只用了常数级别的额外空间（几个计数器），空间复杂度是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def maxScoreIndices_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    best_score = -1               # 记录最高分数
    ans = []                      # 记录对应的下标

    # i 表示分割点，左闭右开 [0, i) 为左侧， [i, n) 为右侧
    for i in range(n + 1):
        left_zero = 0
        right_one = 0

        # 统计左侧 0 的个数
        for j in range(i):
            if nums[j] == 0:
                left_zero += 1

        # 统计右侧 1 的个数
        for j in range(i, n):
            if nums[j] == 1:
                right_one += 1

        score = left_zero + right_one

        # 更新最高分数和答案列表
        if score > best_score:
            best_score = score
            ans = [i]               # 重新开始记录
        elif score == best_score:
            ans.append(i)           # 同分数，继续收集

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 每个分割点都要遍历一次左子数组和右子数组。  
- **空间复杂度**：`O(1)` —— 只用了固定数量的计数变量（不随 `n` 增长）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历左侧和右侧**，导致二次循环。  
实际上，**从左往右一次遍历**就能把所需的计数全部维护好：

1. **预先统计**整个数组中 `1` 的总数 `total_one`。  
2. 再次从左到右遍历，维护两个变量  
   - `left_zero`：当前左侧（`0 ~ i-1`）的 0 的个数  
   - `left_one`：当前左侧的 1 的个数（可以直接从 `total_one` 减去右侧的 1）  
3. 对于分割点 `i`（左侧是前 `i` 个元素），右侧的 `1` 个数等于  
   `right_one = total_one - left_one`。  
   分数公式简化为  
   `score(i) = left_zero + (total_one - left_one)`。  
4. 在遍历过程中 **实时更新**最高分数 `best_score`，并把对应的下标收集进列表。  
5. 注意：分割点可以在最左（`i = 0`）和最右（`i = n`），因此遍历结束后还要处理 `i = n`（此时左侧是整个数组，右侧为空）。

> **类比**：把 `total_one` 看成一本完整的“成功章节”总数，左侧已经读过的章节用 `left_one` 表示，剩下的就是右侧还有多少“成功章节”。只要一次遍历，就能知道每个分割点的左侧错误页数和右侧成功章节数。

**关键技巧**：**前缀计数**（prefix count）  
- 与前缀和相似，只是我们记录的是 “到当前位置为止的 0 的个数”和 “1 的个数”。  
- 这样每次移动分割点时，只需要 **增量更新**（加 1 或不变），不必重新遍历。

#### 代码（Python）

```python
from typing import List

def maxScoreIndices(nums: List[int]) -> List[int]:
    n = len(nums)

    # 1️⃣ 统计整个数组里 1 的总数
    total_one = sum(nums)          # O(n) 一次遍历

    left_zero = 0                  # 左侧 0 的个数（初始为 0，因为左侧为空）
    left_one = 0                   # 左侧 1 的个数
    best_score = -1                # 当前最高分数
    ans = []                       # 保存所有最高分数对应的下标

    # 2️⃣ 枚举分割点 i = 0, 1, ..., n
    #    注意：在循环开始时，左侧已经是前 i 个元素
    for i in range(n + 1):
        # 右侧 1 的个数 = 总 1 减去左侧已出现的 1
        right_one = total_one - left_one
        score = left_zero + right_one

        # 更新最高分数和答案列表
        if score > best_score:
            best_score = score
            ans = [i]               # 重新开始收集
        elif score == best_score:
            ans.append(i)

        # 3️⃣ 为下一个分割点准备计数（i -> i+1）
        #    只有在 i < n 时才会有第 i 个元素可以加入左侧
        if i < n:
            if nums[i] == 0:
                left_zero += 1      # 左侧多了一个 0
            else:                    # nums[i] == 1
                left_one += 1       # 左侧多了一个 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历数组两遍（一次求 `total_one`，一次维护前缀计数），每个元素处理常数次。  
  - **对比**：相较于暴力的 `O(n²)`，大幅提升，`n=10⁵` 时也能轻松跑完。  
- **空间复杂度**：`O(1)` —— 只用了若干整数变量和返回列表（返回列表大小最多 `n+1`，不计入额外空间）。

---

## 心得  

- **核心技巧**：利用**前缀计数**（或前缀和）一次遍历即可得到每个分割点的左侧 0 与右侧 1 的数量。  
- **适用题型**：  
  1. “分割数组求最大/最小某种组合分数”——如 LeetCode 1689 *Partitioning Into Minimum Number Of Subsets*。  
  2. “统计前缀/后缀满足条件的子数组数目”——如 LeetCode 1248 *Count Number of Nice Subarrays*。  
  3. “求每个位置的左侧/右侧累计信息”——如 LeetCode 2130 *Maximum Twin Sum of a Linked List*（思路类似的前缀/后缀）。  
- **一句话总结**：**把全局信息（总 1 的个数）与动态维护的前缀计数结合，就能在 O(n) 内算出所有分割点的分数**。

---

## 反思  

- **第一反应**：看到“左侧 0 + 右侧 1”，立刻想到遍历每个切分点并分别计数——也就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记考虑 `i = 0`（左侧空）和 `i = n`（右侧空）的情况。  
  - 计数时把右侧的 1 错误地写成 `total_one - left_zero`（其实是减左侧的 1）。  
  - 对于大数组忘记使用 O(1) 额外空间的前缀计数，导致超时。  
- **下次类似题的第一步**：先问自己“**是否可以用一次遍历把左/右信息累计起来**”，如果答案是“可以”，就立即考虑前缀和/前缀计数的方案。