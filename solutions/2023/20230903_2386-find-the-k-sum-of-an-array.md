# #2386. 求数组的 K 和 / Find the K-Sum of an Array

> 难度：困难 · 标签：Array、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-the-k-sum-of-an-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and a positive integer k. You can choose any subsequence of the array and sum all of its elements together.
We define the K-Sum of the array as the kth largest subsequence sum that can be obtained (not necessarily distinct).
Return the K-Sum of the array.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.
Note that the empty subsequence is considered to have a sum of 0.

**Examples**

**Example 1:**

```
Input: nums = [2,4,-2], k = 5
Output: 2
Explanation: All the possible subsequence sums that we can obtain are the following sorted in decreasing order:
- 6, 4, 4, 2, 2, 0, 0, -2.
The 5-Sum of the array is 2.
```

**Example 2:**

```
Input: nums = [1,-2,3,4,-10,12], k = 16
Output: 10
Explanation: The 16-Sum of the array is 10.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- -109 <= nums[i] <= 109
- 1 <= k <= min(2000, 2n)

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个正整数 `k`。你可以选择数组的任意子序列（subsequence），并将其所有元素求和。  
我们将数组的 **K-和**（K-Sum）定义为所有可能的子序列和中第 `k` 大的值（不要求不同）。返回该数组的 K-和。  

子序列是指可以通过删除若干（也可以不删除）元素得到的数组，**不改变**剩余元素的相对顺序。  
注意，空子序列的和被视为 `0`。

**示例**  

*示例 1*  
```text
Input: nums = [2,4,-2], k = 5
Output: 2
Explanation: 所有可以得到的子序列和按从大到小排序为：
6, 4, 4, 2, 2, 0, 0, -2。第 5 大的和为 2。
```

*示例 2*  
```text
Input: nums = [1,-2,3,4,-10,12], k = 16
Output: 10
Explanation: 第 16 大的子序列和为 10。
```

**约束条件**  

- `n == nums.length`
- `1 <= n <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `1 <= k <= min(2000, 2^n)`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有可能的子序列** 都枚举出来，算出它们的和，然后把所有和排个序，取第 k 大的那个。

- **子序列**：可以把数组看成一串字符，挑选或不挑选每个字符，就得到一个子序列。  
  比如 `[2,4,-2]`，挑选第 1、2 位得到子序列 `[2,4]`，不挑选任何位得到空子序列 `[]`（和为 0）。
- **枚举方式**：对每个位置决定 “取” 还是 “不取”。这相当于二进制的 `0/1` 选择，总共有 `2ⁿ` 种组合（`n` 为数组长度）。  
  这就像把一本字典的每一页都翻一遍，找出所有可能的页码——显然不切实际，但思路最清晰。

> **为什么一定能得到正确答案？**  
> 因为我们把 *所有* 子序列的和都算出来了，排好序后第 k 大的就是题目要求的 **K‑Sum**。

#### 代码（Python）

```python
from itertools import combinations

def kth_sum_bruteforce(nums, k):
    n = len(nums)
    all_sums = []

    # 对每一种可能的子序列长度进行枚举
    for r in range(n + 1):                     # 包含空子序列 r = 0
        for comb in combinations(nums, r):    # 取出长度为 r 的所有组合
            all_sums.append(sum(comb))        # 计算子序列和

    # 从大到小排序
    all_sums.sort(reverse=True)
    return all_sums[k - 1]                     # 第 k 大（下标从 0 开始）

# 示例
print(kth_sum_bruteforce([2, 4, -2], 5))   # 输出 2
```

> **关键行中文注释**  
> - `for r in range(n + 1)`: 依次枚举子序列的长度，从 0（空子序列）到 `n`（全部元素）。  
> - `combinations(nums, r)`: Python 标准库提供的“取 r 个不重复元素的所有组合”。  
> - `all_sums.sort(reverse=True)`: 降序排列，最大值排在最前面。

#### 复杂度  

- **时间复杂度**：`O(2ⁿ)`  
  每个元素都有 “取 / 不取” 两种选择，全部组合数是 `2ⁿ`，对每个组合都要计算一次和。  
  对初学者来说，`2ⁿ` 可以想象成“指数增长”，比如 `n=20` 时已经有 `1,048,576` 种情况，远远超出计算机在几毫秒内能处理的范围。
- **空间复杂度**：`O(2ⁿ)`  
  我们把所有子序列的和都存进列表，数量同样是 `2ⁿ`。

> **结论**：暴力解只能用来验证思路或在极小的输入（比如 `n ≤ 20`）上测试，面对题目给出的 `n ≤ 10⁵` 完全不可行。

---

### 2. 最优解

#### 思路  

从暴力解出发，**慢的根源** 是我们一次性枚举了全部 `2ⁿ` 种子序列。  
实际上，**我们只需要前 k 大的和**（k 最多 2000），根本不必遍历所有组合。  

下面一步步推导出一种只产生 “下一个最大和” 的方法：

1. **把问题转成“在一堆正数里挑子集”**  
   - 把所有正数 **一定要取**，因为取了它们可以让和更大。  
   - 把所有负数 **不取**，因为不取负数可以让和更大。  
   - 设 `base = sum(positive numbers)`，这就是 **最大的子序列和**（即第 1 大）。
   - 对每个正数 `p`，如果我们**不取**它，和会 **减去 `p`**。  
   - 对每个负数 `-n`（`n>0`），如果我们**取**它，和会 **加上 `n`**（即把负数变成正数）。  

   因此，每一次“改变”都相当于 **在 `base` 上减去一个正数的绝对值**。  
   把所有元素的 **绝对值** 放进一个数组 `abs_vals`，我们的问题等价于：

   > 从 `base` 开始，每次可以选择 **减去** `abs_vals[i]`（对应“去掉一个正数”或“加上一个负数”），  
   > 求第 k 大的结果。

2. **把 `abs_vals` 按从大到小排序**  
   - 大的绝对值对和的影响更大，先考虑它们更容易得到大的结果。  
   - 类比：如果你有若干块重量不同的砖头，想让总重量尽可能大，就先决定是否放下最大的那块。

3. **使用最大堆（Priority Queue）逐步产生 “下一个最大和”**  
   - 初始状态：`cur_sum = base`（什么都不减），对应第 1 大。把它放进堆。
   - 每次从堆里弹出当前最大的和 `s`，记住它是第 `cnt` 大的答案。
   - **如何产生后继？**  
     假设弹出的是“已经决定了前 `i` 个绝对值的取舍，且第 `i` 个已经 **被减去**”。  
     那么我们有两种新情况可以继续往下走（对应经典的 “K 大子集和” 推导）：

     1. **再减去第 `i+1` 个**：`s - abs_vals[i+1]`  
        （继续不取后面的元素，和更小）  
     2. **把已经减去的第 `i` 个 “换成” 第 `i+1` 个**：`s + abs_vals[i] - abs_vals[i+1]`  
        （相当于把较大的 `abs_vals[i]` 替换成稍小的 `abs_vals[i+1]`，得到的和会比情况 1 大一点）  

   - 为了避免重复产生相同的状态，用 `visited` 集合记录已经入堆的 `(index, sum)`。

4. **循环 k 次**  
   - 第 `k` 次弹出的 `s` 就是答案。  
   - 因为每次只产生最多两个新状态，堆的大小始终保持在 `O(k)`，而 `k ≤ 2000`，非常小。

5. **特殊情况：空子序列**  
   - 空子序列的和是 `0`。在上面的转化里，如果 `base` 本身就是 `0`（没有正数），堆的初始元素已经是 `0`，自然会被计入。  
   - 如果 `base > 0`，`0` 会在后面的某一步被生成（把所有正数都减掉），同样不需要额外处理。

> **核心技巧**：  
> - 把“取子序列”转化为“在一组正数里挑子集”，把负数的取与正数的舍统一为“减去绝对值”。  
> - 用 **最大堆** 按顺序生成 **K 大子集和**，只保留前 k 个，不会遍历全部 `2ⁿ` 种可能。

#### 代码（Python）

```python
import heapq

def kth_sum(nums, k):
    """
    返回数组 nums 的第 k 大子序列和（K‑Sum）。
    思路：把问题转化为在正数数组的子集上求第 k 大的和，
          使用最大堆按序生成。
    """
    # 1️⃣ 计算最大可能的和（把所有正数都取）
    base = sum(x for x in nums if x > 0)

    # 2️⃣ 把每个元素的绝对值放进列表，并从大到小排序
    abs_vals = [abs(x) for x in nums]
    abs_vals.sort(reverse=True)          # 大 → 小

    # 3️⃣ 最大堆（Python 的 heapq 是最小堆，用负数模拟最大堆）
    max_heap = []
    # 初始状态：不减任何数，和为 base，当前考虑的下标为 -1（表示还未选任何）
    heapq.heappush(max_heap, (-base, -1))   # (负的和, 已处理的最后一个下标)

    visited = set()                         # 防止同一个状态被重复加入
    visited.add((-base, -1))

    cnt = 0                                 # 已弹出的次数
    answer = None

    while max_heap:
        cur_neg, idx = heapq.heappop(max_heap)
        cur = -cur_neg                       # 恢复为正数，即当前的子序列和
        cnt += 1
        if cnt == k:                         # 第 k 大的就是答案
            answer = cur
            break

        # 下一步要处理的下标是 idx + 1
        nxt = idx + 1
        if nxt < len(abs_vals):
            # 方案 1：继续减去下一个绝对值
            s1 = cur - abs_vals[nxt]
            state1 = (-s1, nxt)
            if state1 not in visited:
                heapq.heappush(max_heap, state1)
                visited.add(state1)

            # 方案 2：把已经减去的 abs_vals[idx]（如果 idx >= 0）换成 nxt
            if idx >= 0:
                s2 = cur + abs_vals[idx] - abs_vals[nxt]
                state2 = (-s2, nxt)
                if state2 not in visited:
                    heapq.heappush(max_heap, state2)
                    visited.add(state2)

    return answer

# ----------------- 示例 -----------------
print(kth_sum([2, 4, -2], 5))               # 输出 2
print(kth_sum([1, -2, 3, 4, -10, 12], 16)) # 输出 10
```

**代码要点解释**  

| 行号 | 作用（中文） |
|------|--------------|
| `base = sum(x for x in nums if x > 0)` | 把所有正数都取，得到最大的子序列和 |
| `abs_vals = [abs(x) for x in nums]` | 把每个元素转成“绝对值”，因为之后只会“减去”它们 |
| `abs_vals.sort(reverse=True)` | 从大到小排，好让先处理影响最大的数 |
| `heapq.heappush(max_heap, (-base, -1))` | 把初始状态（最大和）放进最大堆（用负数模拟） |
| `while max_heap:` | 循环弹出当前最大的和 |
| `cur = -cur_neg` | 把负数转回正数，得到真实的子序列和 |
| `if cnt == k:` | 第 k 次弹出即为答案 |
| `s1 = cur - abs_vals[nxt]` | 方案 1：继续把下一个绝对值减去 |
| `s2 = cur + abs_vals[idx] - abs_vals[nxt]` | 方案 2：把已经减去的 `idx` 换成更小的 `nxt` |
| `visited` | 记录已经加入堆的状态，防止重复 |

#### 复杂度  

- **时间复杂度**：`O(n log n + k log k)`  
  - `n log n` 来自对 `abs_vals` 的排序（`n ≤ 10⁵`）。  
  - 堆里最多会出现 `2k` 条记录（每弹出一次最多产生两条新记录），每次弹入/弹出是 `log(k)`，所以总共是 `O(k log k)`。  
  - 对比暴力解的 `2ⁿ`，这里的 `k` 最多只有 2000，几乎可以忽略不计。

- **空间复杂度**：`O(n + k)`  
  - `abs_vals` 需要 `O(n)` 的存储。  
  - 堆和 `visited` 最多保存 `O(k)` 条状态。  

> **直观解释**：排序像把书排好序，只要一次翻页就能找到“大致最大的”。堆则像一个“随时可以看到当前最大值的宝箱”，我们每次只拿走最大的宝物，然后再往里放进两件稍小的宝物，最多只会放进几千件，根本不用把所有 `2ⁿ` 件宝物都搬进来。

---

## 心得

- **核心技巧**：把“子序列和”问题转化为“在一组正数里挑子集”，再用 **最大堆** 按序生成 K 大子集和。
- **适用的题型**（类似思路）  
  1. **K 大子数组和**（LeetCode 2386）  
  2. **K 大子集和**（LeetCode 1918）  
  3. **前 K 小/大的路径和**（图论中的 K 条最短路）  
- **一句话总结解题钥匙**：**先把所有正数全取（得到最大），再把“去掉正数 / 加上负数”统一为“减去绝对值”，利用堆一次产生下一个最大和**。

---

## 反思

- **拿到题目第一反应**：想到“枚举所有子序列”，因为子序列概念直观，最自然的实现是暴力搜索。
- **最容易踩的坑**  
  - **忽略负数的作用**：负数不取会让和更大，取负数会让和更小，必须在转化时统一处理。  
  - **重复状态**：堆的两条生成规则会产生相同的 `(sum, index)`，如果不去重会导致无限循环或错误答案。  
  - **空子序列**：空子序列的和是 0，需确保算法在 `base > 0` 时也能产生 0（通过把所有正数都减掉实现）。  
- **下次遇到同类题的第一步**：  
  **“先找出最大可能的答案（贪心全取），再把问题转化为‘在正数集合里挑子集’”，然后考虑用堆或 DP 按序生成前 K 大/小的结果。**