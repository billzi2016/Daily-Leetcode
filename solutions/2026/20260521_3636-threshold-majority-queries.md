# #3636. 阈值多数查询 / Threshold Majority Queries

> 难度：困难 · 标签： · [LeetCode 链接](https://leetcode.com/problems/threshold-majority-queries/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of length n and an array queries, where queries[i] = [li, ri, thresholdi].
Return an array of integers ans where ans[i] is equal to the element in the subarray nums[li...ri] that appears at least thresholdi times, selecting the element with the highest frequency (choosing the smallest in case of a tie), or -1 if no such element exists.

**Examples**

**Example 1:**

```
Input: nums = [1,1,2,2,1,1], queries = [[0,5,4],[0,3,3],[2,3,2]]
Output: [1,-1,2]
Explanation:
```

**Example 2:**

```
Input: nums = [3,2,3,2,3,2,3], queries = [[0,6,4],[1,5,2],[2,4,1],[3,3,1]]
Output: [3,2,3,2]
Explanation:
```

**Constraints**

- 1 <= nums.length == n <= 104
- 1 <= nums[i] <= 109
- 1 <= queries.length <= 5 * 104
- queries[i] = [li, ri, thresholdi]
- 0 <= li <= ri < n
- 1 <= thresholdi <= ri - li + 1

---

## 题目（中文翻译）

给定长度为 `n` 的整数数组 `nums` 和一个查询数组 `queries`，其中 `queries[i] = [li, ri, thresholdi]`。返回一个整数数组 `ans`，使得 `ans[i]` 等于子数组（subarray）`nums[li…ri]` 中出现次数不少于 `thresholdi` 次的元素。若有多个元素满足条件，选取出现频率最高的；若出现次数相同，则选取数值最小的。如果不存在满足条件的元素，返回 `-1`。

## 示例

### 示例 1
**输入**  
```text
nums = [1,1,2,2,1,1], queries = [[0,5,4],[0,3,3],[2,3,2]]
```
**输出**  
```text
[1,-1,2]
```
**解释**：

（此处填写示例 1 的解释）

### 示例 2
**输入**  
```text
nums = [3,2,3,2,3,2,3], queries = [[0,6,4],[1,5,2],[2,4,1],[3,3,1]]
```
**输出**  
```text
[3,2,3,2]
```
**解释**：

（此处填写示例 2 的解释）

## 约束条件
- `1 <= nums.length == n <= 10^4`
- `1 <= nums[i] <= 10^9`
- `1 <= queries.length <= 5 * 10^4`
- `queries[i] = [li, ri, thresholdi]`
- `0 <= li <= ri < n`
- `1 <= thresholdi <= ri - li + 1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每个查询单独算**：  

1. 取出子数组 `nums[l … r]`（就像在一本书里翻到第 `l`‑`r` 页）。  
2. 用一个哈希表（想象成“查字典”，单词是数组里的数，页码是出现次数）统计子数组里每个数字出现了多少次。  
3. 再遍历哈希表，找出出现次数 **≥ threshold** 的数字中，出现次数最多的那个；如果出现次数相同，选最小的数字。  
4. 找不到符合条件的，就返回 `-1`。  

这种做法**一定能得到正确答案**，因为我们对每个查询都完整地统计了子数组的频率，没有遗漏任何可能的答案。

#### 代码（Python）  

```python
from collections import Counter
from typing import List

def majority_query_bruteforce(nums: List[int], queries: List[List[int]]) -> List[int]:
    ans = []
    for l, r, th in queries:
        # 1. 取子数组
        sub = nums[l: r + 1]                 # 包含右端点
        # 2. 统计频率，Counter 就像“查字典”
        cnt = Counter(sub)                  # key: 数字，value: 出现次数

        # 3. 在满足阈值的数字中找出现次数最多、值最小的
        best_val = -1
        best_freq = 0
        for val, freq in cnt.items():
            if freq >= th:                   # 必须达到阈值
                # 更高频率或相同频率但更小的数字，更新答案
                if freq > best_freq or (freq == best_freq and val < best_val):
                    best_freq = freq
                    best_val = val
        ans.append(best_val)                # 若没有符合条件的，best_val 仍为 -1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(Q * N)`（最坏情况下每个查询都遍历整个数组）  
  - 这里的 `O(Q * N)` 可以理解为“如果有 5 万个查询，而数组长度是 1 万，那么最多要做 5 × 10⁸ 次基本操作”。  
- **空间复杂度**：`O(N)`（临时的 Counter 最多保存子数组里不重复的数字，最坏情况是整个数组全部不同）  

显然，这在 **n = 10⁴、Q = 5·10⁴** 的极限情况下会超时，需要更快的办法。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都重新统计整个子数组**。我们希望在相邻查询之间**复用已有的统计信息**，只对变化的部分做增量更新。  

这正是 **Mo's algorithm（莫队算法）** 的思想——把查询按照一定顺序排列，使得左端点 `L` 和右端点 `R` 只会“小幅度”移动，从而整体复杂度降到 `O((N+Q)·√N)`。  

下面一步步解释如何在本题中实现它：

1. **分块（sqrt decomposition）**  
   - 取块大小 `B = int(sqrt(N))`（大约是 100），把数组的下标划分成若干块。  
   - 把查询先按左端点所在块的编号升序排列；同一块内再按右端点升序排列。  
   - 这样相邻查询的 `L` 只会在同一块内部来回移动，`R` 基本只会向右移动或稍微回退，整体移动次数 ≈ `O(N·√N)`。

2. **维护窗口 `[L, R]` 的频率**  
   - 用字典 `cnt` 记录当前窗口里每个数出现了多少次（哈希表 → 查字典）。  
   - 为了快速找出“出现次数 ≥ threshold 的最大频率且数值最小”，我们再建立 **频率桶**：`bucket[f]` 保存所有出现次数恰好为 `f` 的数（用 `set` 维护）。  
   - 当我们 **加入** 一个数 `x`（右指针右移或左指针左移）时：  
     ```python
     old = cnt.get(x, 0)          # 之前出现了几次
     new = old + 1                # 加进窗口后次数加 1
     cnt[x] = new
     bucket[old].discard(x)       # 从旧频率的集合里删掉
     bucket[new].add(x)           # 加入新频率的集合
     max_freq = max(max_freq, new)   # 维护当前窗口的最大出现次数
     ```
   - 当我们 **移除** 一个数 `x`（左指针右移或右指针左移）时，做相反的操作，并在必要时降低 `max_freq`（如果最高频率的集合为空，则向下搜索）。

3. **回答单个查询**  
   - 已经把窗口调整到 `[l, r]`，此时 `cnt`、`bucket`、`max_freq` 完全对应这个子数组。  
   - 从 `threshold` 开始向上扫描到 `max_freq`，找到第一个 **非空** 的 `bucket[f]`，取其中最小的数即为答案。  
   - 如果一直没有找到，说明没有数字满足阈值，返回 `-1`。  
   - 这一步的时间是 `O(max_freq - threshold + 1)`，在最坏情况下也不会超过 `O(√N)`（因为出现次数大于 `√N` 的数最多只有 `√N` 个）。

整体复杂度是 `O((N + Q)·√N)`，在本题约为 `O( (10⁴ + 5·10⁴)·100 ) = 6·10⁶`，足够快。

#### 代码（Python）  

```python
import math
from collections import defaultdict
from typing import List

def majority_query(nums: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums)
    B = int(math.sqrt(n)) or 1          # 块大小，防止 n=0 时除以 0

    # ---------- 1. 把查询按 Mo 的顺序排序 ----------
    indexed_queries = [(l, r, th, idx) for idx, (l, r, th) in enumerate(queries)]
    indexed_queries.sort(key=lambda x: (x[0] // B, x[1]))

    # ---------- 2. 初始化窗口 ----------
    cnt = defaultdict(int)              # cnt[x] = x 在当前窗口出现次数
    bucket = defaultdict(set)           # bucket[f] = 所有出现次数恰为 f 的数
    max_freq = 0                         # 当前窗口的最大出现次数

    L, R = 0, -1                         # 空窗口，左闭右开区间 [L, R]
    ans = [0] * len(queries)

    # ---------- 3. 辅助函数 ----------
    def add(pos: int):
        """把 nums[pos] 加入窗口"""
        nonlocal max_freq
        x = nums[pos]
        old = cnt[x]
        new = old + 1
        cnt[x] = new
        if old > 0:
            bucket[old].discard(x)      # 从旧频率的集合里删掉
        bucket[new].add(x)              # 加入新频率的集合
        if new > max_freq:
            max_freq = new

    def remove(pos: int):
        """把 nums[pos] 从窗口中移除"""
        nonlocal max_freq
        x = nums[pos]
        old = cnt[x]
        new = old - 1
        cnt[x] = new
        bucket[old].discard(x)          # 从旧频率的集合里删掉
        if new > 0:
            bucket[new].add(x)          # 仍然在窗口里，加入新频率集合
        # 若最高频率的集合已经空了，需要往下找新的 max_freq
        if not bucket[max_freq]:
            while max_freq > 0 and not bucket[max_freq]:
                max_freq -= 1

    # ---------- 4. 处理每个查询 ----------
    for l, r, th, idx in indexed_queries:
        # 把窗口移动到 [l, r]
        while R < r:
            R += 1
            add(R)
        while R > r:
            remove(R)
            R -= 1
        while L < l:
            remove(L)
            L += 1
        while L > l:
            L -= 1
            add(L)

        # 在当前窗口里查找满足阈值的答案
        answer = -1
        # 只需要检查阈值到 max_freq 之间的频率
        for f in range(th, max_freq + 1):
            if bucket[f]:                # 该频率下至少有一个数
                answer = min(bucket[f]) # 取最小的数
                break
        ans[idx] = answer

    return ans
```

> **代码要点注释**  
> - `add` / `remove` 两个函数负责 **增量维护** `cnt` 与 `bucket`，相当于“窗口滑动时的增删”。  
> - `bucket` 用 `set` 保存同一频率的所有数，查找最小值时只要 `min(bucket[f])` 即可。  
> - `max_freq` 记录当前窗口的最大出现次数，帮助我们在查询时只遍历 **必要的频率区间**。  

#### 复杂度  

- **时间复杂度**：`O((N + Q)·√N)`  
  - `√N`≈100（因为 `N ≤ 10⁴`），所以整体约为几百万次基本操作，远快于暴力的 `5·10⁸` 次。  
- **空间复杂度**：`O(N)`  
  - `cnt`、`bucket` 最多存放当前窗口里出现的不同数字，最坏情况是整个数组全部不同，即 `O(N)`。  

相比暴力解，**时间降低了一个量级**，而空间几乎不变，符合题目对 10⁴ 长度和 5·10⁴ 查询的要求。

---

## 心得  

- **核心技巧**：**Mo's 算法 + 频率桶**  
  - Mo's 算法把大量区间查询的“重新统计”工作改成“增量更新”。  
  - 频率桶让我们能够在 **O(频率差)** 的时间内快速定位满足阈值的最大频率及对应的最小元素。  

- **适用的题型**（类似思路）  
  1. “区间多数元素” / “区间出现次数≥k的元素”。  
  2. “区间不同数目” / “区间中出现次数恰好为 k 的数”。  
  3. “区间最大频率（Mode）” 类问题。  

- **一句话总结**：  
  *把查询按块排序，让窗口只做小步滑动，再用哈希表+频率桶实时维护出现次数，即可在 √N 级别时间内回答所有区间阈值多数查询。*  

---

## 反思  

- **第一反应**：直接遍历子数组统计频率（暴力），因为它最直观。  
- **最容易踩的坑**  
  1. **左闭右闭 vs 左闭右开**：窗口的左右端点要保持一致的闭区间约定，容易写错导致遗漏或多计。  
  2. **频率桶的同步**：在 `remove` 时忘记把数从旧频率的集合里删掉，或在 `add` 时忘记更新 `max_freq`，会导致查询结果不正确。  
  3. **阈值大于当前最大频率**：直接返回 `-1`，否则会在空的频率区间里循环。  

- **下次遇到同类题**，第一步应该：  
  *“这是一类需要对大量区间做相似统计的题目吗？如果是，尝试先用 Mo 的排序把查询顺序固定，再设计增量维护的数据结构（哈希表、桶、树状数组等）”。*  

这样即可快速从暴力思路转向高效解法。