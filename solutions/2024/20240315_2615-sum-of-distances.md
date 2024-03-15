# #2615. 距离之和 / Sum of Distances

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/sum-of-distances/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. There exists an array arr of length nums.length, where arr[i] is the sum of |i - j| over all j such that nums[j] == nums[i] and j != i. If there is no such j, set arr[i] to be 0.
Return the array arr.
Note: This question is the same as  2121: Intervals Between Identical Elements.

**Examples**

**Example 1:**

```
Input: nums = [1,3,1,1,2]
Output: [5,0,3,4,0]
Explanation: 
When i = 0, nums[0] == nums[2] and nums[0] == nums[3]. Therefore, arr[0] = |0 - 2| + |0 - 3| = 5. 
When i = 1, arr[1] = 0 because there is no other index with value 3.
When i = 2, nums[2] == nums[0] and nums[2] == nums[3]. Therefore, arr[2] = |2 - 0| + |2 - 3| = 3. 
When i = 3, nums[3] == nums[0] and nums[3] == nums[2]. Therefore, arr[3] = |3 - 0| + |3 - 2| = 4. 
When i = 4, arr[4] = 0 because there is no other index with value 2.
```

**Example 2:**

```
Input: nums = [0,5,3]
Output: [0,0,0]
Explanation: Since each element in nums is distinct, arr[i] = 0 for all i.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数数组 `nums`。存在一个长度为 `nums.length` 的数组 `arr`，其中 `arr[i]` 为所有满足 `nums[j] == nums[i]` 且 `j != i` 的下标 `j` 的 `|i - j|`（绝对差）的和。如果不存在这样的 `j`，则 `arr[i]` 设为 `0`。  
返回数组 `arr`。

> **注意**：本题与 2121: Intervals Between Identical Elements 完全相同。

## 示例

### 示例 1

> **输入**：`nums = [1,3,1,1,2]`  
> **输出**：`[5,0,3,4,0]`  
> **解释**：  
> 当 `i = 0` 时，`nums[0] == nums[2]` 且 `nums[0] == nums[3]`。因此  
> `arr[0] = |0 - 2| + |0 - 3| = 5`。  
> 当 `i = 1` 时，`arr[1] = 0`，因为没有其他下标的值为 `3`。  
> 当 `i = 2` 时，`nums[2] == nums[0]` 且 `nums[2] == nums[3]`。因此  
> `arr[2] = |2 - 0| + |2 - 3| = 3`。  
> 当 `i = 3` 时，`nums[3] == nums[0]` 且 `nums[3] == nums[2]`。因此  
> `arr[3] = |3 - 0| + |3 - 2| = 4`。  
> 当 `i = 4` 时，`arr[4] = 0`，因为没有其他下标的值为 `2`。

### 示例 2

> **输入**：`nums = [0,5,3]`  
> **输出**：`[0,0,0]`  
> **解释**：数组 `nums` 中的每个元素均不相同，故所有 `arr[i]` 均为 `0`。

## 约束

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把每个位置 i 当作中心**，把数组里所有和 `nums[i]` 相同的下标 `j`（`j ≠ i`）全部找出来，然后把 `|i - j|` 加到答案里。  

- **用到的数据结构**：  
  - `for` 循环遍历数组。  
  - 一个临时的整数变量 `total` 用来累计距离。  
  - 可以把“相同的数”想象成 **同一本书的不同章节**，我们要把章节号之间的距离全部相加。  

- **为什么正确**：  
  对每个 `i`，我们把**所有**满足 `nums[j] == nums[i]` 且 `j ≠ i` 的 `j` 都遍历一次，计算 `|i-j|`，正好等于题目要求的 `arr[i]`。  

- **时间/空间复杂度**：  
  - 外层遍历 `i` 需要 `n` 次，内层遍历 `j` 也要 `n` 次，最坏情况（所有数都相同）会执行 `n·n` 次比较和加法，记作 **O(n²)**。  
    - 大白话：如果数组长度是 10,000，暴力解要做大约 1 亿 次操作，计算机会明显卡顿。  
  - 只用了常数级别的额外空间（几个整数），记作 **O(1)**。  

#### 代码（Python）  

```python
from typing import List

def sum_of_distances_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [0] * n                      # 最终答案，初始全 0
    for i in range(n):                 # 把每个位置 i 当作中心
        total = 0
        for j in range(n):             # 扫描所有位置 j
            if i != j and nums[i] == nums[j]:
                total += abs(i - j)    # 累加距离
        ans[i] = total                  # 把结果写进 ans
    return ans
```

#### 复杂度  

- **时间复杂度**：O(n²) —— 两层循环，每层最多遍历 `n` 次。  
- **空间复杂度**：O(1) —— 只用了常数个额外变量（答案数组不算在额外空间里）。  

---  

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于每次都要把整个数组再遍历一遍，导致 `n²` 的时间。  
观察题目可以发现：  

1. **相同数的下标集合**是我们真正关心的。比如数 `1` 出现在下标 `[0, 2, 3]`，我们只需要在这三个位置之间计算距离。  
2. 对于同一组下标（已排好序），**左边的下标对当前下标的贡献**和**右边的下标对当前下标的贡献**可以用**前缀和**一次性算出。  

> 类比：想象你站在一条直线上的某个点，左边有若干座标点，右边也有若干点。左边所有点到你的距离之和 = `当前位置·左边点的个数 - 左边点坐标之和`；右边同理，只是符号相反。  

**具体步骤**  

1. **遍历一次数组**，把每个数出现的下标保存到哈希表 `pos`（字典）里。  
   - `pos[x]` = `[i1, i2, …, ik]`（下标自然是递增的，因为我们是从左到右收集的）。  
   - 哈希表就像 **词典**：键是数值，值是它出现的所有位置。  

2. 对每个键 `x`，**计算该下标列表的前缀和** `pre`：  
   - `pre[t] = i0 + i1 + … + it`。  
   - 前缀和相当于 **累加账本**，帮助我们快速求任意区间的坐标之和。  

3. 再遍历该下标列表，对每个位置 `p`（在列表中的下标），利用下面的公式算出 `arr[ ip ]`：  

   - 左侧贡献（所有左边的下标）  
     ```
     left_cnt = p                     # 左边有 p 个元素
     left_sum = pre[p-1] if p > 0 else 0
     left_part = ip * left_cnt - left_sum
     ```
   - 右侧贡献（所有右边的下标）  
     ```
     right_cnt = k - p - 1            # 右边有 k-p-1 个元素
     right_sum = pre[-1] - pre[p]    # 总和减去左侧+当前的前缀和
     right_part = right_sum - ip * right_cnt
     ```
   - 两部分相加即为答案 `arr[ip] = left_part + right_part`。  

4. 把所有组的结果写回答案数组即可。  

**为什么是 O(n)**  

- 第一步遍历一次数组，收集下标 → O(n)。  
- 对每个不同的数，我们只遍历它的下标列表两次（一次算前缀和，一次算答案）→ 所有列表的长度加起来正好是 `n`，所以仍是 O(n)。  
- 哈希表的查找、插入都是 **均摊 O(1)**。  

**空间**方面，需要保存每个数的下标列表以及对应的前缀和，整体占用 O(n) 的额外空间。  

#### 代码（Python）  

```python
from typing import List
from collections import defaultdict

def sum_of_distances(nums: List[int]) -> List[int]:
    n = len(nums)
    ans = [0] * n                      # 最终答案

    # 1️⃣ 收集每个数出现的下标，哈希表相当于“词典”
    pos = defaultdict(list)            # key: 数值，value: 该数出现的所有下标（已排好序）
    for idx, val in enumerate(nums):
        pos[val].append(idx)

    # 2️⃣ 对每个数的下标列表分别处理
    for indices in pos.values():        # indices 是一个递增的下标列表
        k = len(indices)
        if k == 1:                      # 只出现一次，答案本来就是 0，直接跳过
            continue

        # 前缀和数组 pre[t] = indices[0] + ... + indices[t]
        pre = [0] * k
        pre[0] = indices[0]
        for i in range(1, k):
            pre[i] = pre[i - 1] + indices[i]

        total_sum = pre[-1]             # 所有下标的总和，后面会用到

        # 3️⃣ 逐个下标计算距离和
        for p, cur_idx in enumerate(indices):
            # ----- 左侧贡献 -----
            left_cnt = p                         # 左边有 p 个元素
            left_sum = pre[p - 1] if p > 0 else 0
            left_part = cur_idx * left_cnt - left_sum

            # ----- 右侧贡献 -----
            right_cnt = k - p - 1                # 右边的元素个数
            right_sum = total_sum - pre[p]       # 右边所有下标的和
            right_part = right_sum - cur_idx * right_cnt

            # 合并左右两侧的距离和
            ans[cur_idx] = left_part + right_part

    return ans
```

#### 复杂度  

- **时间复杂度**：O(n) —— 只遍历了两遍数组（一次收集下标，一次计算答案），不随数值种类增多而增加。相比暴力的 O(n²)，快了几个数量级。  
- **空间复杂度**：O(n) —— 需要保存每个数的下标列表以及对应的前缀和，总共不超过 `n` 个整数。  

---  

## 心得  

- **核心技巧**：把相同数的下标分组，然后用**前缀和**一次性算出每个位置左/右侧的距离贡献。  
- **适用的题型**  
  1. “相同元素之间的距离求和”系列（本题、2121 Inter​vals Between Identical Elements）。  
  2. “每个元素与同值元素的差值之和”或“同值元素的乘积之和”。  
  3. “按值分组后需要快速区间求和的场景”，如 “按颜色统计区间长度”。  
- **一句话总结解题钥匙**：**把问题转化为“对每个分组的有序下标求前缀和”，左侧用 `i·cnt - sum`，右侧用 `sum - i·cnt`**。  

---  

## 反思  

- **第一反应**：看到“所有相同元素之间的绝对差”就想到两层循环逐个比较——这就是暴力解。  
- **最容易踩的坑**  
  - **下标列表必须是有序的**：如果在收集时不保证顺序（比如用了集合），公式就不成立。  
  - **边界条件**：当某个数只出现一次时，左/右侧计数会为 0，需要单独处理，避免出现负索引。  
  - **整数溢出**（在某些语言中）：`i * cnt` 可能超过 32 位整数范围，Python 自动大整数所以不必担心。  
- **下次遇到同类题**，**第一步**应该想到：  
  1. 按值把下标**分组**（哈希表）。  
  2. 利用**有序**的特性，用**前缀和**一次性算出左/右贡献，而不是逐个遍历。