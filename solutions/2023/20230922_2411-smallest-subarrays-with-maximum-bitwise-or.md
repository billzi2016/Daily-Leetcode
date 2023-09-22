# #2411. **最大位或的最小子数组** / Smallest Subarrays With Maximum Bitwise OR

> 难度：中等 · 标签：Array、Binary Search、Bit Manipulation、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/smallest-subarrays-with-maximum-bitwise-or/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of length n, consisting of non-negative integers. For each index i from 0 to n - 1, you must determine the size of the minimum sized non-empty subarray of nums starting at i (inclusive) that has the maximum possible bitwise OR.
The bitwise OR of an array is the bitwise OR of all the numbers in it.
Return an integer array answer of size n where answer[i] is the length of the minimum sized subarray starting at i with maximum bitwise OR.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,0,2,1,3]
Output: [3,3,2,2,1]
Explanation:
The maximum possible bitwise OR starting at any index is 3. 
- Starting at index 0, the shortest subarray that yields it is [1,0,2].
- Starting at index 1, the shortest subarray that yields the maximum bitwise OR is [0,2,1].
- Starting at index 2, the shortest subarray that yields the maximum bitwise OR is [2,1].
- Starting at index 3, the shortest subarray that yields the maximum bitwise OR is [1,3].
- Starting at index 4, the shortest subarray that yields the maximum bitwise OR is [3].
Therefore, we return [3,3,2,2,1].
```

**Example 2:**

```
Input: nums = [1,2]
Output: [2,1]
Explanation:
Starting at index 0, the shortest subarray that yields the maximum bitwise OR is of length 2.
Starting at index 1, the shortest subarray that yields the maximum bitwise OR is of length 1.
Therefore, we return [2,1].
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始、长度为 `n` 的数组 `nums`，其中元素为非负整数。对于每个下标 `i`（`0 ≤ i ≤ n‑1`），需要求出从下标 `i` 开始（含 `i`）的、满足**最大可能的位或**（bitwise OR）的**最小长度非空子数组**（subarray）的大小。

数组的位或是指数组中所有元素按位或运算的结果。

返回一个长度为 `n` 的整数数组 `answer`，其中 `answer[i]` 表示从下标 `i` 开始、能够得到最大位或的最小子数组的长度。

子数组是指数组中连续的、非空的元素序列。

---

### 示例

#### 示例 1
```text
Input: nums = [1,0,2,1,3]
Output: [3,3,2,2,1]
```
**解释**：  
从任意下标开始能够得到的最大位或都是 `3`。  
- 从下标 `0` 开始，最短的子数组是 `[1,0,2]`。  
- 从下标 `1` 开始，最短的子数组是 `[0,2,1]`。  
- 从下标 `2` 开始，最短的子数组是 `[2,1]`。  
- 从下标 `3` 开始，最短的子数组是 `[1,3]`（长度为 `2`）。  
- 从下标 `4` 开始，最短的子数组是 `[3]`（长度为 `1`）。

#### 示例 2
```text
Input: nums = [1,2]
Output: [2,1]
```
**解释**：  
- 从下标 `0` 开始，能够得到最大位或的最短子数组长度为 `2`（即 `[1,2]`）。  
- 从下标 `1` 开始，能够得到最大位或的最短子数组长度为 `1`（即 `[2]`）。  
因此返回 `[2,1]`。

---

### 约束条件
- `n == nums.length`
- `1 ≤ n ≤ 10^5`
- `0 ≤ nums[i] ≤ 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个起点 `i`，把后面的元素一个一个往右加，直到 OR 的结果不再变化（也就是已经等于从 `i` 开始所有元素的 OR）为止**。  
- **数据结构**：只需要一个整数 `cur_or` 来保存当前子数组的按位或结果。  
- **生活化类比**：把数组想成一串灯泡，每个灯泡的开关对应二进制位（0=关，1=亮）。从第 `i 颗灯开始，一颗颗往右检查，只要还能点亮新的灯（出现新的 1），就继续往右；一旦所有灯都已经亮到最高（再也没有新灯亮了），就可以停下来，这时候的子数组长度就是答案。  

**为什么正确**：  
- 对于固定的起点 `i`，子数组的 OR 随着右端点的移动只能“增加”或保持不变（因为 OR 只会把 0 变成 1），不会出现减小的情况。  
- 当我们第一次达到**全局最大 OR**（即从 `i` 开始到数组末尾的 OR），再往右也不可能得到更大的 OR，因为已经把所有能点亮的灯都点亮了。于是此时的子数组一定是 **最短** 的满足条件的子数组。  

**复杂度分析（大白话）**：  
- 对每个位置 `i`，我们最坏要遍历到数组末尾，这相当于 `n + (n-1) + (n-2) + … + 1 = n·(n+1)/2` 次操作。  
- 用大 O 记号写就是 **O(n²)**，也就是说如果数组有 10,000 个元素，最坏情况要做大约 100,000,000 次计算，可能会超时。  
- 空间上只用了几个整数，**O(1)**（常数）额外空间。  

#### 代码（Python）

```python
from typing import List

def smallestSubarrays_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    answer = [0] * n
    
    # 从左到右遍历每个起点 i
    for i in range(n):
        cur_or = 0               # 当前子数组的 OR
        # 往右扩展，直到 OR 达到从 i 开始的最大可能值
        for j in range(i, n):
            cur_or |= nums[j]    # 把 nums[j] 加进来，按位或
            # 计算从 i 到数组末尾的全部 OR（一次性算）
            # 这里用一个小技巧：在最外层循环里预先算一次 max_or[i] 会更快，
            # 但为了保持“最直觉”的写法，这里直接在内部比较。
            # 只要 cur_or 已经等于从 i 到末尾所有数的 OR，就可以停止
            #（因为 OR 只会增不减）
            # 为了不每次都遍历到末尾求 max，这里先算一次整体 OR
            #（在实际实现中可以提前预处理，但这里保持最原始思路）
            # 下面的 if 条件等价于：cur_or == OR(i, n-1)
            # 这里我们直接在内部循环结束后再判断
            # 为了让代码可运行，这里不做提前终止，等循环自然结束
        # 循环结束后，cur_or 已经是从 i 到末尾的 OR
        # 再次遍历找到最短子数组（可以在上面循环里直接返回，这里写得更清晰）
        cur_or = 0
        for j in range(i, n):
            cur_or |= nums[j]
            if cur_or == answer[i] or (j == n-1):
                # 当第一次达到最大 OR 时，记录长度
                answer[i] = j - i + 1
                break
    return answer
```

> **注**：上面的实现为“最直觉的”写法，实际运行会很慢。它展示了 **“遍历每个起点、逐个向右累加”** 的思路，便于初学者理解问题本质。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “n²” 可以想象成一个正方形的格子，横坐标是起点，纵坐标是右端点。我们把每个格子都遍历了一遍。  
- **空间复杂度**：`O(1)`（不计答案数组本身）  
  - 只用了几个整数变量，和数组大小无关。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每个起点都要向右扫描**，导致重复工作。  
观察按位或的性质可以帮助我们 **一次遍历就得到所有答案**。

**关键观察 1：**  
对于任意起点 `i`，其“最大可能的 OR”其实是从 `i` 到数组末尾所有元素的 OR（记作 `max_or[i]`）。因为再往右也只能把已有的 1 保持或增加，不能出现新的更大的位。

**关键观察 2：**  
`max_or[i]` 的每一位（bit）只要在 **某个位置** 出现过 1，就会一直保持 1 到数组末尾。也就是说，**若我们知道从 `i` 开始最近的、能够把第 `b` 位打开的元素位置**，则只要子数组长度 ≥ 那个位置与 `i` 的距离，就能把第 `b` 位包含进来。

**把这两个观察结合**：  
- 对每一位 `b (0~30)`（因为 `nums[i] ≤ 10^9 < 2^30`），记录 **下一个出现 1 的位置**。  
- 对于起点 `i`，所有位的 “最近出现 1 的位置” 取 **最大值**（最远的那个），因为只有覆盖到最远的那一位，子数组的 OR 才能等于 `max_or[i]`。  
- 那么答案长度 `answer[i] = max_distance + 1`（+1 因为长度是位置差+1）。

**如何高效得到“下一个出现 1 的位置”**？  
- 逆序遍历数组（从右往左），维护一个大小为 31 的数组 `next_one[b]`，表示**当前索引右侧最近的、在第 `b` 位为 1 的元素下标**。  
- 当我们处理位置 `i` 时，先把 `nums[i]` 的每一位为 1 的情况更新 `next_one`（因为 `i` 本身就是最近的）。  
- 然后遍历 0~30 位，计算 `next_one[b] - i`（如果该位在后面永远没有 1，则用 `inf` 表示），取最大值即为需要的最小子数组长度减 1。  

**一步步推导**：  

1. 初始化 `next_one = [inf] * 31`（`inf` 代表“没有找到”）。  
2. 从 `i = n-1` 到 `0` 逆序遍历：  
   - 对每一位 `b`：  
     - 如果 `nums[i]` 在第 `b` 位是 1，则 `next_one[b] = i`（因为当前位置已经是最近的 1）。  
   - 计算 `max_dist = 0`。  
   - 再遍历 0~30 位：  
     - `dist = next_one[b] - i`（若 `next_one[b]` 为 `inf`，说明从 `i` 起永远没有该位的 1，直接忽略，因为该位在 `max_or[i]` 中本来就是 0）。  
     - `max_dist = max(max_dist, dist)`。  
   - `answer[i] = max_dist + 1`（长度）。  

**为什么一次遍历就能得到所有答案？**  
- 逆序遍历保证在处理 `i` 时，`next_one` 已经记录了 **i 右侧** 所有元素的最近 1 位置。  
- 每次只需要检查 31 位，时间是 **O(31·n) ≈ O(n)**，空间只用了 `next_one`（31 个整数）和答案数组，**O(1)** 额外空间。  

**类比帮助理解**：  
想象 31 条“管道”，每条管道对应二进制的一个位。管道里有阀门（数组元素）会把水（1）放进去。我们从右往左走，每走一步就检查当前阀门是否打开对应管道的阀门，如果打开，就把 “最近的阀门位置” 更新为当前。这样，当我们站在位置 `i` 时，所有管道的 “最近阀门” 已经准备好，只要我们往右走到最远的那个阀门，就能让所有需要的水流进来，形成最大 OR。  

#### 代码（Python）

```python
from typing import List

def smallestSubarrays(nums: List[int]) -> List[int]:
    n = len(nums)
    INF = n               # 因为下标最大是 n-1，使用 n 代表 “不存在”
    # next_one[b] 表示在当前遍历位置的右侧，最近的、在第 b 位为 1 的下标
    next_one = [INF] * 31
    answer = [0] * n

    # 从右往左遍历
    for i in range(n - 1, -1, -1):
        x = nums[i]

        # 1) 更新最近的 1 位置（如果当前数在该位是 1）
        for b in range(31):
            if (x >> b) & 1:          # 第 b 位是 1 吗？
                next_one[b] = i       # 当前下标就是最近的

        # 2) 计算从 i 开始需要覆盖的最远距离
        max_dist = 0
        for b in range(31):
            # 如果该位在后面永远没有 1，next_one[b] == INF，dist 会很大，
            # 但其实 max_or[i] 在这位本来就是 0，直接忽略即可
            if next_one[b] != INF:    # 该位在后面至少出现一次
                dist = next_one[b] - i
                if dist > max_dist:
                    max_dist = dist

        # 3) 子数组长度 = 最远距离 + 1（因为距离是下标差）
        answer[i] = max_dist + 1

    return answer
```

> **关键行中文注释**  
> - `if (x >> b) & 1:`  # 判断第 `b` 位是否为 1（右移后与 1 做与运算）  
> - `next_one[b] = i`   # 更新最近出现 1 的位置  
> - `dist = next_one[b] - i` # 需要向右走多远才能把第 `b` 位的 1 包含进来  

#### 复杂度  

- **时间复杂度**：`O(31·n) = O(n)`  
  - 31 是常数（因为整数最多只有 30~31 位），所以整体线性增长。相比暴力的 `n²`，速度提升了几个数量级。  
- **空间复杂度**：`O(31) = O(1)`（不计答案数组）  
  - 只用了一个长度为 31 的小数组 `next_one`，与输入规模无关。  

---  

## 心得  

- **核心技巧**：**按位拆分 + 逆序维护最近出现 1 的位置**。  
- 这种“每个位单独考虑” 的思路在很多 **位运算** 题目里都非常有用，例如：  
  1. *Maximum XOR of Two Numbers in an Array*（使用 Trie 按位处理）  
  2. *Subarray Bitwise ORs*（统计所有可能的 OR）  
  3. *Number of Subarrays with Bounded Maximum*（也可以用单调栈按位思考）  
- **一句话总结**：**把每一位当成独立的“任务”，逆序记录最近能完成任务的下标，最大距离决定最短子数组长度**。  

## 反思  

- **第一反应**：直接想“从每个位置往右累加 OR”。这导致了 `O(n²)` 的暴力实现。  
- **最容易踩的坑**：  
  - 忘记 **按位** 只需要检查到最高位（30 位），否则会出现 `range(64)` 之类的多余循环。  
  - 在逆序遍历时更新 `next_one` 的顺序一定要在 **使用** 之前完成，否则会把当前下标算成“右侧”。  
  - 处理 “该位永远没有 1” 的情况时，需要用 `INF` 或 `n` 进行屏蔽，避免把无效的距离当成最大值。  
- **下次类似题**：  
  1. **先判断是否可以把问题拆成每一位独立**（如 OR、AND、XOR）。  
  2. **考虑逆序或前缀/后缀信息**，看能否一次遍历把所有“最近位置”预处理好。  
  3. **用最大距离/最小距离** 把 “需要多大范围才能满足所有位” 转化为子数组长度。