# #2200. 在数组中查找所有 K 远距离索引 / Find All K-Distant Indices in an Array

> 难度：简单 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/find-all-k-distant-indices-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and two integers key and k. A k-distant index is an index i of nums for which there exists at least one index j such that |i - j| <= k and nums[j] == key.
Return a list of all k-distant indices sorted in increasing order.

**Examples**

**Example 1:**

```
Input: nums = [3,4,9,1,3,9,5], key = 9, k = 1
Output: [1,2,3,4,5,6]
Explanation: Here, nums[2] == key and nums[5] == key.
- For index 0, |0 - 2| > k and |0 - 5| > k, so there is no j where |0 - j| <= k and nums[j] == key. Thus, 0 is not a k-distant index.
- For index 1, |1 - 2| <= k and nums[2] == key, so 1 is a k-distant index.
- For index 2, |2 - 2| <= k and nums[2] == key, so 2 is a k-distant index.
- For index 3, |3 - 2| <= k and nums[2] == key, so 3 is a k-distant index.
- For index 4, |4 - 5| <= k and nums[5] == key, so 4 is a k-distant index.
- For index 5, |5 - 5| <= k and nums[5] == key, so 5 is a k-distant index.
- For index 6, |6 - 5| <= k and nums[5] == key, so 6 is a k-distant index.
Thus, we return [1,2,3,4,5,6] which is sorted in increasing order.
```

**Example 2:**

```
Input: nums = [2,2,2,2,2], key = 2, k = 2
Output: [0,1,2,3,4]
Explanation: For all indices i in nums, there exists some index j such that |i - j| <= k and nums[j] == key, so every index is a k-distant index. 
Hence, we return [0,1,2,3,4].
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 1000
- key is an integer from the array nums.
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数数组 `nums`，以及两个整数 `key` 和 `k`。若存在至少一个索引 `j` 满足 `|i - j| <= k` 且 `nums[j] == key`，则称数组中的索引 `i` 为 **k‑distant 索引**（k‑distant index）。  
返回所有 k‑distant 索引的列表，按升序排列。

### 示例 1
**输入**  
``` 
nums = [3,4,9,1,3,9,5], key = 9, k = 1
```  
**输出**  
```
[1,2,3,4,5,6]
```  
**解释**  
这里 `nums[2] == key` 且 `nums[5] == key`。  

- 对于索引 `0`，`|0 - 2| > k` 且 `|0 - 5| > k`，不存在满足 `|0 - j| <= k` 且 `nums[j] == key` 的 `j`，因此 `0` 不是 k‑distant 索引。  
- 对于索引 `1`，`|1 - 2| <= k` 且 `nums[2] == key`，所以 `1` 是 k‑distant 索引。  
- 对于索引 `2`，`|2 - 2| <= k` 且 `nums[2] == key`，所以 `2` 是 k‑distant 索引。  
- …（后续索引同理）

### 示例 2
**输入**  
``` 
nums = [2,2,2,2,2], key = 2, k = 2
```  
**输出**  
```
[0,1,2,3,4]
```  
**解释**  
对于 `nums` 中的每个索引 `i`，都存在某个索引 `j` 使得 `|i - j| <= k` 且 `nums[j] == key`，因此所有索引都是 k‑distant 索引，返回 `[0,1,2,3,4]`。

### 约束条件
- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`
- `key` 为数组 `nums` 中的一个整数
- `1 <= k <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是 **把每个下标 i 当作“候选”，检查它左边和右边最多 k 步之内是否出现过 key**。  
- 把数组想象成一排座位，key 就是“明星”。我们要判断每个座位 i 是否离明星不超过 k 步。  
- 对每个 i，我们把它能看到的范围写出来 `[i‑k, i+k]`（记得别越界），在这个范围里遍历所有 j，看看 `nums[j] == key` 是否成立。只要找到一次，就把 i 加入答案。

这种做法一定能得到正确答案，因为我们穷举了“所有可能的 j”。  

#### 代码（Python）  

```python
from typing import List

def findKDistantIndices_bruteforce(nums: List[int], key: int, k: int) -> List[int]:
    n = len(nums)
    ans = []                       # 用来存放满足条件的下标
    for i in range(n):             # 枚举每个候选下标 i
        # 计算 i 能看到的左右边界，防止越界
        left = max(0, i - k)
        right = min(n - 1, i + k)
        # 在 [left, right] 区间里寻找是否有 key
        found = False
        for j in range(left, right + 1):
            if nums[j] == key:      # 只要出现一次就够了
                found = True
                break               # 提前退出内层循环，省点时间
        if found:
            ans.append(i)            # i 符合条件，加入答案
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`。  
  - `n` 是数组长度，外层遍历每个下标。  
  - 对每个 i，我们最多检查 `2k+1` 个位置（左、右各 k 步，加上自身），所以总体是 `n × (2k+1)`，简写成 `O(n·k)`。  
  - 当 `k` 接近 `n` 时，这相当于 `O(n²)`，也就是“把所有元素两两比较”。  

- **空间复杂度**：`O(1)`（不计返回结果的空间）。只用了常数个额外变量 `left、right、found`。  



---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每个下标都要去检查它左右 k 步的所有位置**，这会产生大量的重复劳动。  
其实我们只关心 **每个位置离最近的 key 有多远**，如果这个距离 ≤ k，答案就成立。  

可以用 **前缀+后缀遍历**（两遍线性扫描）一次性算出每个下标到最近 key 的最小距离：

1. **从左往右扫描**  
   - 用 `last` 记录最近一次出现 key 的下标（如果左边还没出现 key，`last = -inf`）。  
   - 对当前下标 `i`，如果 `last` 有效，则 `dist[i] = i - last`（这就是左侧最近 key 的距离）。  

2. **从右往左扫描**  
   - 用 `next` 记录最近一次出现 key 的下标（从右边看过去）。  
   - 同理，如果 `next` 有效，则 `dist[i] = min(dist[i], next - i)`，把右侧的距离也考虑进去。  

扫描结束后，`dist[i]` 就是 **左侧或右侧最近的 key 的距离的最小值**。只要 `dist[i] <= k`，`i` 就是答案。

> **类比**：把数组看成一条路，两边都有灯塔（key）。我们先从左边走，记录每个点离左边最近灯塔的距离；再从右边走，取两次记录的最小值，这样每个点就知道离最近灯塔有多远了。

#### 代码（Python）  

```python
from typing import List

def findKDistantIndices_optimal(nums: List[int], key: int, k: int) -> List[int]:
    n = len(nums)
    INF = n + 5                     # 一个足够大的数，表示“暂无 key”
    dist = [INF] * n                # dist[i] 保存下标 i 到最近 key 的距离

    # 1️⃣ 左到右：记录左侧最近的 key
    last = -INF                     # 初始时左侧没有 key
    for i in range(n):
        if nums[i] == key:
            last = i                # 碰到 key，更新最近位置
        if last != -INF:            # 有左侧 key 时更新距离
            dist[i] = i - last

    # 2️⃣ 右到左：记录右侧最近的 key，取最小值
    nxt = INF                       # 初始时右侧没有 key
    for i in range(n - 1, -1, -1):
        if nums[i] == key:
            nxt = i                 # 碰到 key，更新最近位置
        if nxt != INF:              # 有右侧 key 时取更小的距离
            dist[i] = min(dist[i], nxt - i)

    # 3️⃣ 收集满足条件的下标
    ans = [i for i in range(n) if dist[i] <= k]
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 只遍历了数组两遍（左→右、右→左），每次都是常数时间操作。  
  - 与暴力解的 `O(n·k)` 相比，省去了内部的 `k` 次循环，速度提升显著。  

- **空间复杂度**：`O(n)`（用于存放 `dist` 数组）。  
  - 若只想要返回结果而不保留全部距离，也可以在第二遍扫描时直接把满足 `dist <= k` 的下标加入答案，这样可以把额外空间降到 `O(1)`（不计返回列表）。  



---  

## 心得  

- **核心技巧**：**前缀/后缀扫描求最近距离**。  
  - 这是一种“从两端收敛”的思路，常用于“最近某类元素的距离”这类问题。  

- **适用题型**（类似思路可直接迁移）：  
  1. *“每个元素到最近 0 的距离”*（LeetCode 2059）  
  2. *“数组中每个位置到最近的出现的目标值的距离”*（类似 1848）  
  3. *“求每个位置最近的左/右边满足条件的元素”*（单调栈也可以实现）  

- **一句话总结解题钥匙**：  
  > 把“是否在 k 步内”转化为“最近的 key 距离 ≤ k”，用两遍线性扫描一次算出所有最近距离。  



---  

## 反思  

- **第一反应**：看到“|i‑j| ≤ k 且 nums[j] == key”，立刻想到“遍历所有 i、j”，于是写出暴力解。  

- **最容易踩的坑**：  
  - **边界处理**：`i‑k` 可能小于 0，`i+k` 可能超过数组长度，需要 `max`/`min` 防止越界。  
  - **重复下标**：如果直接对每个 key 的左右区间做标记，可能会把同一个下标加入多次，记得去重（使用集合或一次性遍历）。  
  - **k 大于数组长度**：虽然题目保证 `k ≤ len(nums)`，但写代码时仍要防止 `right` 越界。  

- **下次遇到同类题**，第一步应该先问自己：  
  - “我真的需要逐个比较吗？能否把‘距离’信息提前算好？”  
  - 如果答案是可以预处理，那么就考虑 **前缀/后缀扫描**、**前缀和**、**单调栈** 等线性时间的技巧。  



---