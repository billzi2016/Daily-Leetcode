# #2121. **相同元素之间的区间** / Intervals Between Identical Elements

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/intervals-between-identical-elements/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of n integers arr.
The interval between two elements in arr is defined as the absolute difference between their indices. More formally, the interval between arr[i] and arr[j] is |i - j|.
Return an array intervals of length n where intervals[i] is the sum of intervals between arr[i] and each element in arr with the same value as arr[i].
Note: |x| is the absolute value of x.
Note: This question is the same as  2615: Sum of Distances.

**Examples**

**Example 1:**

```
Input: arr = [2,1,3,1,2,3,3]
Output: [4,2,7,2,4,4,5]
Explanation:
- Index 0: Another 2 is found at index 4. |0 - 4| = 4
- Index 1: Another 1 is found at index 3. |1 - 3| = 2
- Index 2: Two more 3s are found at indices 5 and 6. |2 - 5| + |2 - 6| = 7
- Index 3: Another 1 is found at index 1. |3 - 1| = 2
- Index 4: Another 2 is found at index 0. |4 - 0| = 4
- Index 5: Two more 3s are found at indices 2 and 6. |5 - 2| + |5 - 6| = 4
- Index 6: Two more 3s are found at indices 2 and 5. |6 - 2| + |6 - 5| = 5
```

**Example 2:**

```
Input: arr = [10,5,10,10]
Output: [5,0,3,4]
Explanation:
- Index 0: Two more 10s are found at indices 2 and 3. |0 - 2| + |0 - 3| = 5
- Index 1: There is only one 5 in the array, so its sum of intervals to identical elements is 0.
- Index 2: Two more 10s are found at indices 0 and 3. |2 - 0| + |2 - 3| = 3
- Index 3: Two more 10s are found at indices 0 and 2. |3 - 0| + |3 - 2| = 4
```

**Constraints**

- n == arr.length
- 1 <= n <= 105
- 1 <= arr[i] <= 105

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组（array）`arr`，长度为 `n`。  
数组中任意两个元素的 **区间（interval）** 定义为它们下标的绝对差，即 `|i - j|`。  
返回一个长度为 `n` 的数组 `intervals`，其中 `intervals[i]` 等于 `arr[i]` 与数组中所有值与 `arr[i]` 相同的元素之间 **区间（interval）** 的和。  
注意，`|x|` 表示 `x` 的绝对值。

---

### 示例

**示例 1**  
```text
Input: arr = [2,1,3,1,2,3,3]
Output: [4,2,7,2,4,4,5]
Explanation:
- 下标 0: 另一个 2 位于下标 4，|0 - 4| = 4
- 下标 1: 另一个 1 位于下标 3，|1 - 3| = 2
- 下标 2: 还有两个 3 位于下标 5 和 6，|2 - 5| + |2 - 6| = 7
- 下标 3: 另一个 1 位于下标 1，|3 - 1| = 2
- 下标 4: 另一个 2 位于下标 0，|4 - 0| = 4
- 下标 5: 还有两个 3 位于下标 2 和 6，|5 - 2| + |5 - 6| = 4
- 下标 6: 还有两个 3 位于下标 2 和 5，|6 - 2| + |6 - 5| = 5
```

**示例 2**  
```text
Input: arr = [10,5,10,10]
Output: [5,0,3,4]
Explanation:
- 下标 0: 另外两个 10 位于下标 2 和 3，|0 - 2| + |0 - 3| = 5
- 下标 1: 数组中只有一个 5，故与相同元素的区间和为 0
- 下标 2: 另外两个 10 位于下标 0 和 3，|2 - 0| + |2 - 3| = 3
- 下标 3: 另外两个 10 位于下标 0 和 2，|3 - 0| + |3 - 2| = 4
```

---

### 约束条件

- `n == arr.length`
- `1 <= n <= 10^5`
- `1 <= arr[i] <= 10^5`

> 本题等同于 2615: Sum of Distances。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个位置 i，遍历整个数组，找出所有与 `arr[i]` 相同的元素 j，累加 `|i-j|`**。  
这里用到的唯一数据结构就是**数组**本身——我们把数组看成一排座位，`i` 和 `j` 就是座位号，`|i-j|` 就是两个人之间的步数。

为什么这样一定能得到正确答案？  
- 对每个 i，我们把 **所有** 与 `arr[i]` 相同的下标都枚举了一遍，且每一次都加上它们之间的距离。  
- 题目要求的正是“所有相同值的下标之间的距离之和”，所以遍历一次就能完整收集。

#### 代码（Python）

```python
from typing import List

def sum_of_intervals_bruteforce(arr: List[int]) -> List[int]:
    n = len(arr)
    ans = [0] * n                      # 用来存放答案
    for i in range(n):                 # 枚举每个位置 i
        total = 0
        for j in range(n):             # 再遍历所有位置 j
            if i != j and arr[i] == arr[j]:
                total += abs(i - j)    # 累加距离
        ans[i] = total                  # 把结果写进答案数组
    return ans
```

> **关键行注释**  
> - `for i in range(n)`: “站在第 i 位的同学”。  
> - `if i != j and arr[i] == arr[j]`: 只把 **相同值且不是自己** 的同学算进去。  
> - `abs(i - j)`: “从 i 走到 j 需要的步数”。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们有两个嵌套的 `for` 循环，外层遍历 `n` 次，内层每次也要遍历 `n` 次，整体是 `n × n` 次操作。  
  在实际意义上，如果 `n = 10⁴`，则需要约 `10⁸` 次比较，已经很慢了。

- **空间复杂度**：`O(1)`（不计答案数组）  
  只用了常数个额外变量（`total`、循环计数器），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于对每个位置都要遍历整条数组**。  
其实，同一个数的所有下标是 **有序的**（因为我们是按下标从左到右扫描），我们可以把它们先收集起来，然后利用**前缀和**一次性算出每个位置的距离和。

具体步骤：

1. **把相同数的下标收集到哈希表**  
   - 哈希表（`dict`）的键是数组里的数值，值是该数值出现的下标列表（自然是递增的）。  
   - 类比：哈希表像一本“电话簿”，名字是键，电话号码列表是值。

2. **对每个值的下标列表分别计算答案**  
   对于下标列表 `idx = [p₀, p₁, …, pₖ]`（已排好序）：
   - 设 `pref[i] = p₀ + p₁ + … + pᵢ` 为前缀和。  
   - 对于列表中的第 `i` 个下标 `pᵢ`，它左边有 `i` 个元素，右边有 `k-i` 个元素。  
   - 与左边元素的距离之和 = `pᵢ * i - pref[i-1]`（因为每个左边元素都比 `pᵢ` 小，距离是 `pᵢ - pⱼ`）  
   - 与右边元素的距离之和 = `(pref[k] - pref[i]) - pᵢ * (k-i)`（因为每个右边元素都比 `pᵢ` 大，距离是 `pⱼ - pᵢ`）  
   - 两者相加即为 `ans[pᵢ]`。

3. **把每个列表的结果写回答案数组**  
   最终得到所有位置的距离和。

这整个过程只遍历了两遍数组：一次收集下标，第二次对每个列表做线性计算，**时间是 `O(n)`**。  
前缀和的额外空间也只需要保存每个列表的前缀和，**总空间是 `O(n)`**（答案数组本身必然占 `O(n)`）。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def sum_of_intervals(arr: List[int]) -> List[int]:
    n = len(arr)
    ans = [0] * n                     # 最终答案

    # 1️⃣ 收集相同数值的下标列表
    pos = defaultdict(list)           # 哈希表：value -> [indices]
    for i, v in enumerate(arr):
        pos[v].append(i)               # 把下标 i 加入对应的列表

    # 2️⃣ 对每个数值的下标列表分别计算前缀和并求答案
    for indices in pos.values():      # 逐个列表处理
        k = len(indices)
        if k == 1:                     # 只出现一次，答案自然是 0
            continue

        # 计算前缀和 pref[i] = indices[0] + ... + indices[i]
        pref = [0] * k
        pref[0] = indices[0]
        for i in range(1, k):
            pref[i] = pref[i-1] + indices[i]

        total_sum = pref[-1]           # 整个列表的下标和，方便后面计算

        # 逐个下标求它的距离和
        for i, idx in enumerate(indices):
            # 左边元素的贡献：idx * i - pref[i-1]
            left_cnt = i                # 左边有 i 个元素
            left_sum = pref[i-1] if i > 0 else 0
            left = idx * left_cnt - left_sum

            # 右边元素的贡献： (total_sum - pref[i]) - idx * (k-i-1)
            right_cnt = k - i - 1       # 右边有多少个元素
            right_sum = total_sum - pref[i]
            right = right_sum - idx * right_cnt

            ans[idx] = left + right     # 合并左右贡献

    return ans
```

> **关键行中文注释**  
> - `pos = defaultdict(list)`: “电话簿”，键是数值，值是出现位置的列表。  
> - `pref[i] = pref[i-1] + indices[i]`: 前缀和，记录从最左到当前位置的下标总和。  
> - `left = idx * left_cnt - left_sum`: 左边距离之和 = “当前位置乘以左边人数” 减去 “左边下标之和”。  
> - `right = right_sum - idx * right_cnt`: 右边距离之和的对称公式。  

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次遍历收集下标：`O(n)`。  
  - 对每个唯一值的下标列表做一次线性遍历（计算前缀和 + 计算答案），所有列表的长度之和仍是 `n`，所以整体仍是 `O(n)`。  
  - 与暴力的 `O(n²)` 相比，速度提升了 **近 n 倍**。

- **空间复杂度**：`O(n)`  
  - 需要额外存储哈希表 `pos`（总共保存 `n` 个下标）和前缀和数组（同样最多 `n` 长）。  
  - 加上答案数组本身，总体是线性空间。

---

## 心得

- **核心技巧**：**同值下标的前缀和**。把相同数值的下标视为一个有序序列，利用前缀和把“左边所有距离”和“右边所有距离”一次性算出来。  
- **适用场景**：  
  1. **“相同元素之间的距离求和”**（本题）。  
  2. **“相同字符出现位置的距离和”**（如字符串版的相同问题）。  
  3. **“分组后对每组做前缀和/后缀和”**的各种统计题（如统计每组元素的累计费用、累计次数等）。  
- **一句话总结**：**把相同值的下标收集好，用前缀和把左/右距离一次算完，省掉所有重复遍历**。

---

## 反思

- **拿到题目第一反应**：直接双层循环枚举每对相同元素，写出最朴素的实现。  
- **最容易踩的坑**：  
  - **下标列表的顺序**：如果不保证下标是递增的，前缀和公式会失效。  
  - **单个出现的元素**：需要单独判断，否则会出现除零或索引越界。  
  - **大数范围**：`n` 可达 `10⁵`，暴力 `O(n²)` 会超时，需要立刻想到分组+前缀和的线性思路。  
- **下次遇到同类题**：第一步先 **“把相同值的下标分组”，再思考如何在每个组内部一次遍历完成所有统计**（常用工具：前缀和、后缀和、滑动窗口等）。