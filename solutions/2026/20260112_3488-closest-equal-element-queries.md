# #3488. **Closest Equal Element Queries** / Closest Equal Element Queries

> 难度：中等 · 标签：Array、Hash Table、Binary Search · [LeetCode 链接](https://leetcode.com/problems/closest-equal-element-queries/)

---

## 题目（英文原版）

**Description**

You are given a circular array nums and an array queries.
For each query i, you have to find the following:
Return an array answer of the same size as queries, where answer[i] represents the result for query i.

**Examples**

**Example 1:**

```
Input: nums = [1,3,1,4,1,3,2], queries = [0,3,5]
Output: [2,-1,3]
Explanation:
```

**Example 2:**

```
Input: nums = [1,2,3,4], queries = [0,1,2,3]
Output: [-1,-1,-1,-1]
Explanation:
Each value in nums is unique, so no index shares the same value as the queried element. This results in -1 for all queries.
```

**Constraints**

- 1 <= queries.length <= nums.length <= 105
- 1 <= nums[i] <= 106
- 0 <= queries[i] < nums.length

---

## 题目（中文翻译）

给定一个循环数组 `nums` 和一个查询数组 `queries`。  
对于每个查询 `queries[i]`（它是 `nums` 中的下标），需要找到与该下标 **值相同** 的最近的另一个下标，并返回它们之间的最小循环距离。如果不存在值相同的其他下标，则返回 `-1`。

- 循环数组（circular array）指的是首尾相连的数组，数组长度记为 `n = nums.length`。  
- 两个下标 `i` 与 `j` 的循环距离定义为 `min(|i - j|, n - |i - j|)`，即在顺时针或逆时针移动时的最少步数。

返回一个大小与 `queries` 相同的数组 `answer`，其中 `answer[i]` 为第 `i` 个查询的结果。

---

### 示例

**示例 1**

```text
输入: nums = [1,3,1,4,1,3,2], queries = [0,3,5]
输出: [2,-1,3]
解释:
- 查询下标 0，nums[0] = 1。相同的值出现在下标 2 和 4，最近的距离为 min(2, 7-2) = 2。
- 查询下标 3，nums[3] = 4。数组中只有一个 4，返回 -1。
- 查询下标 5，nums[5] = 3。相同的值出现在下标 1，距离为 min(|5-1|, 7-|5-1|) = min(4,3) = 3。
```

**示例 2**

```text
输入: nums = [1,2,3,4], queries = [0,1,2,3]
输出: [-1,-1,-1,-1]
解释:
每个值在数组中都唯一，没有其他下标与查询下标的值相同，所有查询返回 -1。
```

---

### 约束条件

- `1 <= queries.length <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`
- `0 <= queries[i] < nums.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个查询下标 `i`，把整个数组 `nums` 再遍历一遍**，找出所有与 `nums[i]` 相同的下标 `j`，然后计算它们在环形数组里的距离，取最小的那个。如果没有其它相同的元素，就返回 `-1`。

> **数据结构**  
> - 这里我们只用到 **数组**（list），因为直接把 `nums` 从头到尾走一遍最简单。  
> - “环形数组”可以想象成一条闭合的跑道，跑一圈后又回到起点。两个下标之间的最短距离就是 **正向跑的步数** 与 **反向跑的步数** 里较小的那个。

> **为什么这个方法一定能得到答案**  
> - 我们把所有可能的 `j` 都检查了一遍，最小的距离自然不会漏掉。  
> - 只要把环形的距离公式写对（`min(diff, n - diff)`），答案就一定正确。

#### 代码（Python）

```python
def closest_equal_brute(nums, queries):
    n = len(nums)                     # 环形数组的长度
    ans = []

    for q in queries:                 # 对每一个查询下标 q
        target = nums[q]              # 目标值
        best = float('inf')           # 当前找到的最小距离，先设为无限大

        # 暴力遍历整个数组，找相同的元素
        for idx, val in enumerate(nums):
            if idx == q:              # 不能和自己比
                continue
            if val == target:         # 找到相同的值
                diff = abs(idx - q)               # 正向的步数
                dist = min(diff, n - diff)         # 环形最短距离
                best = min(best, dist)             # 维护最小值

        ans.append(-1 if best == float('inf') else best)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * m)`（`n` 为数组长度，`m` 为查询个数）。可以把 `O(n * m)` 想象成「每个查询都要把整条跑道跑一遍」。
- **空间复杂度**：`O(1)`（只用了常数级别的额外变量），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个查询都要遍历整个数组**，这在 `n`、`queries` 都达到 10⁵ 时会非常慢。  
我们可以把「相同数值的下标」提前准备好，这样查询时只在**相同数值的下标集合**里找最近的下标，而不是在全数组里找。

**步骤拆解**  

1. **预处理**：遍历一遍 `nums`，用 **哈希表（字典）** 把每个数值映射到它出现的所有下标，**并保持下标有序**。  
   - 哈希表就像一本**词典**，`key` 是单词（这里是数组里的数值），`value` 是页码列表（这里是出现的下标）。查找 `key` 的时间几乎是 `O(1)`，非常快。  

2. **查询**：对于每个 `queries[i] = q`，  
   - 先取出 `target = nums[q]` 在字典里对应的下标列表 `pos_list`（已经排好序）。  
   - 如果列表长度只有 1，说明 `q` 是唯一出现的，下一个答案是 `-1`。  
   - 否则，需要在这个有序列表里**找到离 `q` 最近的左边和右边的下标**。这一步可以用 **二分查找** 完成，时间是 `O(log k)`（`k` 为该数值出现的次数）。  
   - 计算这两个候选下标与 `q` 的环形距离 `min(diff, n - diff)`，取最小值即为答案。

**为什么二分查找能帮我们**  
因为列表是有序的，二分查找相当于在一本**有目录的书**里快速定位到某一页码所在的章节，只需要看几页就能定位，而不需要从头到尾翻。

#### 代码（Python）

```python
import bisect

def closest_equal_opt(nums, queries):
    n = len(nums)

    # 1. 预处理：构建 value -> sorted list of indices 的映射
    idx_map = {}                     # dict[int, List[int]]
    for i, v in enumerate(nums):
        if v not in idx_map:
            idx_map[v] = []
        idx_map[v].append(i)        # 追加下标，遍历顺序本身就是递增的

    # 2. 对每个查询做二分查找
    ans = []
    for q in queries:
        target = nums[q]
        pos_list = idx_map[target]   # 已排好序的下标列表

        if len(pos_list) == 1:       # 只有自己一个出现
            ans.append(-1)
            continue

        # 在有序列表中找到 q 应该插入的位置（左侧的元素全 <= q）
        insert = bisect.bisect_left(pos_list, q)

        # 考虑左侧最近的下标（循环到列表最后）
        left_idx = pos_list[insert - 1] if insert > 0 else pos_list[-1]
        # 考虑右侧最近的下标（循环到列表开头）
        right_idx = pos_list[insert] if insert < len(pos_list) else pos_list[0]

        # 计算环形距离
        def circ_dist(a, b):
            diff = abs(a - b)
            return min(diff, n - diff)

        best = min(circ_dist(q, left_idx), circ_dist(q, right_idx))
        ans.append(best)

    return ans
```

> **代码要点解释**  
> - `bisect_left`：在有序列表里找 **第一个不小于** `q` 的位置。相当于在目录里找 **最近的章节起始页**。  
> - `left_idx`、`right_idx`：分别是左侧和右侧最近的同值下标，利用列表的循环特性（如果左侧已经没有元素，就取列表最后一个；右侧如果已经到末尾，就取第一个）。  
> - `circ_dist`：计算环形数组的最短步数，`min(diff, n - diff)` 就是「顺时针」和「逆时针」两条路里取更短的一条。

#### 复杂度

- **时间复杂度**：  
  - 预处理遍历一次 `nums`：`O(n)`。  
  - 每个查询二分查找：`O(log k)`，最坏情况下 `k ≤ n`，所以整体是 `O(m log n)`（`m` 为查询数）。  
  - 与暴力解的 `O(n·m)` 相比，**把每次遍历整条跑道的工作换成了在小范围内的快速定位**，快得多。  

- **空间复杂度**：`O(n)`，因为要保存每个数值对应的下标列表，最多和数组长度等价。相当于在跑道旁边放了一张**每个数字出现位置的表格**。

---

## 心得

- **核心技巧**：**利用哈希表把相同数值的下标收集起来，再用二分查找在有序列表中快速定位最近的下标**。  
- **适用的题型**  
  1. “查询最近相同元素” 类题目（如 *Find Nearest Duplicate*）。  
  2. “区间内最近相同值” 的变种（如 LeetCode 2202 *Maximize the Topmost Element After K Moves* 中的相同思路）。  
  3. “循环/环形数组” 里求最短距离的题目（如 *Circular Array Loop*）。  
- **一句话总结解题钥匙**：**先把“相同值的下标”组织好，再用二分定位最近的下标**。

---

## 反思

- **第一反应**：看到“环形数组”和“相同元素”，我立刻想到遍历全数组找最近的相同值——这就是暴力解。  
- **最容易踩的坑**  
  - **环形距离的计算**：忘记取 `min(diff, n - diff)`，会把顺时针距离当成唯一答案。  
  - **下标列表的循环取值**：左侧没有元素时要取列表最后一个，右侧没有时要取第一个，否则会出现越界错误。  
  - **单值数组**：如果某个数只出现一次，必须返回 `-1`，不能把自己当作最近的相同元素。  
- **下次遇到同类题**，第一步应该想到：**“把相同数值的下标预先收集并排序”，这样查询就能在对数时间完成**。这样就能把原本的 `O(n·m)` 直接降到 `O(n + m log n)`。