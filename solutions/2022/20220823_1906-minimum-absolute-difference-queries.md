# #1906. 最小绝对差查询 / Minimum Absolute Difference Queries

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/minimum-absolute-difference-queries/)

---

## 题目（英文原版）

**Description**

The minimum absolute difference of an array a is defined as the minimum value of |a[i] - a[j]|, where 0 <= i < j < a.length and a[i] != a[j]. If all elements of a are the same, the minimum absolute difference is -1.
You are given an integer array nums and the array queries where queries[i] = [li, ri]. For each query i, compute the minimum absolute difference of the subarray nums[li...ri] containing the elements of nums between the 0-based indices li and ri (inclusive).
Return an array ans where ans[i] is the answer to the ith query.
A subarray is a contiguous sequence of elements in an array.
The value of |x| is defined as:

**Examples**

**Example 1:**

```
Input: nums = [1,3,4,8], queries = [[0,1],[1,2],[2,3],[0,3]]
Output: [2,1,4,1]
Explanation: The queries are processed as follows:
- queries[0] = [0,1]: The subarray is [1,3] and the minimum absolute difference is |1-3| = 2.
- queries[1] = [1,2]: The subarray is [3,4] and the minimum absolute difference is |3-4| = 1.
- queries[2] = [2,3]: The subarray is [4,8] and the minimum absolute difference is |4-8| = 4.
- queries[3] = [0,3]: The subarray is [1,3,4,8] and the minimum absolute difference is |3-4| = 1.
```

**Example 2:**

```
Input: nums = [4,5,2,2,7,10], queries = [[2,3],[0,2],[0,5],[3,5]]
Output: [-1,1,1,3]
Explanation: The queries are processed as follows:
- queries[0] = [2,3]: The subarray is [2,2] and the minimum absolute difference is -1 because all the
  elements are the same.
- queries[1] = [0,2]: The subarray is [4,5,2] and the minimum absolute difference is |4-5| = 1.
- queries[2] = [0,5]: The subarray is [4,5,2,2,7,10] and the minimum absolute difference is |4-5| = 1.
- queries[3] = [3,5]: The subarray is [2,7,10] and the minimum absolute difference is |7-10| = 3.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i] <= 100
- 1 <= queries.length <= 2 * 104
- 0 <= li < ri < nums.length

---

## 题目（中文翻译）

The minimum absolute difference of an array `a` is defined as the minimum value of `|a[i] - a[j]|`, where `0 ≤ i < j < a.length` and `a[i] != a[j]`. If all elements of `a` are the same, the minimum absolute difference is `-1`。  

You are given an integer array `nums` and the array `queries` where `queries[i] = [li, ri]`. For each query `i`, compute the minimum absolute difference of the **subarray**（子数组）`nums[li...ri]` containing the elements of `nums` between the 0‑based indices `li` and `ri` (inclusive).  
Return an array `ans` where `ans[i]` is the answer to the `i`‑th query.  

A **subarray**（子数组）is a contiguous sequence of elements in an array.  

The value of `|x|` is defined as the absolute value of `x` (the non‑negative value of `x`).  

---

### 示例

#### 示例 1
**Input:**  
```text
nums = [1,3,4,8], queries = [[0,1],[1,2],[2,3],[0,3]]
```
**Output:**  
```text
[2,1,4,1]
```
**Explanation:**  
The queries are processed as follows:
- `queries[0] = [0,1]`：子数组为 `[1,3]`，最小绝对差为 `|1-3| = 2`。  
- `queries[1] = [1,2]`：子数组为 `[3,4]`，最小绝对差为 `|3-4| = 1`。  
- `queries[2] = [2,3]`：子数组为 `[4,8]`，最小绝对差为 `|4-8| = 4`。  
- `queries[3] = [0,3]`：子数组为 `[1,3,4,8]`，最小绝对差为 `|3-4| = 1`。  
... (已截断)

#### 示例 2
**Input:**  
```text
nums = [4,5,2,2,7,10], queries = [[2,3],[0,2],[0,5],[3,5]]
```
**Output:**  
```text
[-1,1,1,3]
```
**Explanation:**  
The queries are processed as follows:
- `queries[0] = [2,3]`：子数组为 `[2,2]`，所有元素相同，最小绝对差为 `-1`。  
- `queries[1] = [0,2]`：子数组为 `[4,5,2]`，最小绝对差为 `|4-5| = 1`。  
- `queries[2] = [0,5]`：子数组为 `[4,5,2,2,7,10]`，最小绝对差为 `|4-5| = 1`。  
- `queries[3] = [3,5]`：子数组为 `[2,7,10]`，最小绝对差为 `|7-10| = 3`。  
... (已截断)

---

### 约束条件
- `2 ≤ nums.length ≤ 10^5`  
- `1 ≤ nums[i] ≤ 100`  
- `1 ≤ queries.length ≤ 2·10^4`  
- `0 ≤ li < ri < nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每个查询的子数组完整取出来，逐个比较**，找出所有不同元素之间的绝对差的最小值。

- **取子数组**：把 `nums[l..r]` 用切片 `nums[l:r+1]` 复制出来。  
- **两两比较**：对子数组中的每一对不同下标 `(i, j)`，计算 `abs(nums[i] - nums[j])`，记录最小的那个。  
- **全部相同**：如果遍历完后发现所有元素都相等（即最小差一直是“无穷大”），答案应该返回 `-1`。

> **类比**：想象你在超市里挑选两件商品，想知道价钱差最小的两件。暴力做法就是把所有商品都搬到桌子上，两两比较价钱，最慢但最可靠。

**为什么正确**：因为我们穷举了所有合法的 `(i, j)` 对，必然能够得到真实的最小差值。  

**复杂度分析**（大白话）：

- 对每个查询，我们要遍历子数组的长度 `m = r - l + 1`。  
- 两两比较的次数是 `C(m, 2) = m·(m-1)/2`，大约是 `m²/2`，所以时间随子数组长度的平方增长。  
- 空间上我们只需要保存子数组本身，最多 `O(m)`。

> **O(m²)** 的意思就是：如果子数组有 1000 个元素，比较次数大约是 1,000,000 次；如果有 10,000 个元素，就会涨到 100,000,000 次，显然会超时。

#### 代码（Python）

```python
def min_abs_diff_bruteforce(nums, queries):
    ans = []
    for l, r in queries:                     # 逐个处理查询
        sub = nums[l:r + 1]                  # 取出子数组（复制了一份）
        best = float('inf')                  # 用无穷大表示“还没找到”
        n = len(sub)
        for i in range(n):
            for j in range(i + 1, n):        # 两两比较，只比较一次
                if sub[i] != sub[j]:        # 只关心不同的数
                    diff = abs(sub[i] - sub[j])
                    if diff < best:
                        best = diff
        ans.append(-1 if best == float('inf') else best)
    return ans
```

#### 复杂度

- **时间复杂度**：`O( Σ (ri‑li+1)² )`，最坏情况下每个查询的子数组几乎是整个数组，等价于 `O(q·n²)`。  
  > 实际上会因为 `n` 可达 `10⁵`、`q` 可达 `2·10⁴` 而彻底炸掉。

- **空间复杂度**：`O(max length of a subarray)`，即 `O(n)`，因为我们会把子数组复制一份。

---

### 2. 最优解

#### 思路  

观察题目约束可以发现两个关键点：

1. **数组元素值的范围很小**：`1 ≤ nums[i] ≤ 100`。  
   这意味着在任意子数组里，最多只有 100 种不同的数。  
2. **查询很多**，而 **子数组长度可能很大**，所以我们必须把“每次都遍历子数组”这一步省掉。

**利用小值域**：如果我们能够在 **O(1)** 时间内知道某个数在 `[l, r]` 区间出现了多少次，就可以只检查这 100 种数，而不必遍历子数组的每个位置。

**前缀计数**（Prefix Count）正好满足需求：

- 对每一个可能的数 `v (1 … 100)`，建立一个长度为 `n+1` 的前缀和数组 `pref[v][i]`，表示 **前 i 个元素中** 数字 `v` 出现的次数。  
- `pref[v][i]` 的递推式非常简单：  
  `pref[v][i] = pref[v][i-1] + (nums[i-1] == v)`。

有了前缀计数后，**区间 `[l, r]` 内数字 `v` 的出现次数** 可以在 **O(1)** 通过  
`cnt = pref[v][r+1] - pref[v][l]` 直接算出。

**求最小绝对差**：

1. 先遍历 `v = 1 … 100`，统计该区间内每个数的出现次数 `cnt`。  
2. 如果发现某个 `cnt ≥ 2`，说明该区间里有相同的数，答案直接是 `-1`（因为题目规定全部相同才返回 `-1`，但出现重复数 **不一定** 全部相同；这里我们要进一步判断）。  
   实际上，**只有当所有出现的数的总数等于 1**（即只有一种数出现）时才返回 `-1`，否则继续寻找最小差。  
3. 把出现过的数收集到一个有序列表 `present`（因为我们是从小到大遍历的，直接记录即可）。  
4. 在 `present` 中，两两相邻的数的差就是**所有可能差值**的候选，因为相邻的两个数差最小。遍历一次取最小即可。

> **类比**：把 `[l, r]` 看成一本书的某一章节，前缀计数相当于在书的每一页前都贴了一张“本章节已经出现了哪些单词”的小卡片。查询时，只要看两张卡片的差异，就能立刻知道本章节里出现了哪些单词，而不必把整本书翻一遍。

**时间/空间分析**：

- **预处理**：对每个位置遍历 100 次，复杂度 `O(100·n)`，约 `1e7` 步，完全可以接受。  
- **单次查询**：遍历 100 种数，做 O(1) 的计数差，随后一次线性扫描（最多 100 次）求最小相邻差，整体 `O(100)`。  
- **总复杂度**：`O(100·n + 100·q)` ≈ `O(n + q)`（常数 100 可以忽略）。  
- **空间**：`(n+1)·101` 个整数，大约 `1e5·101 ≈ 1e7`，在 Python 中约占 80 MB，仍在多数平台的内存上限之内。

#### 代码（Python）

```python
from typing import List

def minAbsDifference(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)
    MAXV = 100                     # 题目给出的最大数值

    # ---------- 1. 构建前缀计数矩阵 ----------
    # pref[v][i] 表示前 i 个元素（下标 0..i-1）中数值 v 出现的次数
    pref = [[0] * (n + 1) for _ in range(MAXV + 1)]

    for i in range(1, n + 1):
        x = nums[i - 1]            # 第 i-1 个元素的真实数值
        for v in range(1, MAXV + 1):
            # 前缀计数的递推：拷贝上一步的计数，再加上当前位置是否等于 v
            pref[v][i] = pref[v][i - 1] + (1 if v == x else 0)

    # ---------- 2. 处理每个查询 ----------
    ans = []
    for l, r in queries:
        present = []               # 本区间出现过的数（从小到大）
        duplicate = False         # 是否出现了相同的数两次以上

        # 遍历所有可能的数值 1..100，利用前缀计数快速得到出现次数
        for v in range(1, MAXV + 1):
            cnt = pref[v][r + 1] - pref[v][l]   # 区间[l, r]内 v 的出现次数
            if cnt:
                present.append(v)
                if cnt >= 2:
                    duplicate = True

        # ① 所有数都相同（只有一种数且出现次数 >= 2） → -1
        if len(present) == 1 and duplicate:
            ans.append(-1)
            continue

        # ② 计算相邻数的最小差
        best = float('inf')
        for i in range(1, len(present)):
            diff = present[i] - present[i - 1]   # 因为已经有序，只需要相邻差
            if diff < best:
                best = diff

        # 如果区间里只有一个不同的数且没有重复（即长度为 1），
        # 题目保证 li < ri，所以不会出现这种情况，安全返回 best。
        ans.append(best if best != float('inf') else -1)

    return ans
```

> **代码要点解释**  
> - 第 7‑12 行：`pref` 的维度是 `[101][n+1]`，下标 0 不使用，只是为了让数值对应下标更直观。  
> - 第 16‑20 行：遍历数组一次，同时对 **每个可能的数值** 更新前缀计数。虽然看起来是 `100·n` 次循环，但每次只做一次加法，运行非常快。  
> - 第 28‑38 行：对单个查询，仅遍历 1..100，利用前缀差得到出现次数 `cnt`。  
> - 第 41‑44 行：如果只有一种数且出现次数 ≥2，直接返回 `-1`（全部相同的特例）。  
> - 第 48‑53 行：因为 `present` 已经是升序的，只需要比较相邻两个数的差，得到最小绝对差。

#### 复杂度

- **时间复杂度**：`O(100·n + 100·q)` → 实际上是线性的 `O(n + q)`，因为常数 100 很小。  
  - 与暴力解相比，**从每个查询的 `O(m²)` 降到 `O(100)`**，提升数千倍甚至上万倍。

- **空间复杂度**：`O(100·(n+1))` → 大约 `1e7` 个整数，约 80 MB。  
  - 相比暴力解的 `O(m)`（临时子数组），这里的空间是预先一次性分配的，但仍在题目限制内。

---

## 心得

- **核心技巧**：**利用值域小（≤100）做前缀计数**，把“在区间里是否出现”变成 O(1) 查询。  
- **适用的题型**  
  1. “区间内出现次数 / 是否出现”类问题（例如 *Range Frequency Queries*、*Range Majority Query*）。  
  2. “区间内求最小/最大差值”且数值范围受限的题目（如本题）。  
- **一句话总结解题钥匙**：*当数组元素的取值范围远小于数组长度时，用前缀计数把“遍历子数组”压缩到常数时间*。

---

## 反思

- **第一反应**：看到“子数组最小绝对差”，本能想到两层循环暴力比较。  
- **最容易踩的坑**  
  - **全部相同的情况**：只有当子数组里只出现一种数且出现次数≥2 时返回 `-1`，不能把出现一次的子数组误判。  
  - **前缀计数的下标**：`pref[v][i]` 表示前 `i` 个元素（即下标 `0..i-1`），查询时要用 `r+1` 与 `l` 的差。  
  - **内存**：直接用 `list` 保存 `(n+1)×101` 的二维数组会占用约 80 MB，需确认平台内存足够。  
- **下次类似题的第一步**：检查**数值范围**是否足够小，如果是，就先考虑**离线预处理（前缀计数 / 位图）**，把区间查询转化为 O(常数) 操作。这样往往可以把看似 O(n·q) 的暴力直接降到 O(n + q)。