# #2382. 移除元素后的最大子段和 / Maximum Segment Sum After Removals

> 难度：困难 · 标签：Array、Union Find、Prefix Sum、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/maximum-segment-sum-after-removals/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums and removeQueries, both of length n. For the ith query, the element in nums at the index removeQueries[i] is removed, splitting nums into different segments.
A segment is a contiguous sequence of positive integers in nums. A segment sum is the sum of every element in a segment.
Return an integer array answer, of length n, where answer[i] is the maximum segment sum after applying the ith removal.
Note: The same index will not be removed more than once.

**Examples**

**Example 1:**

```
Input: nums = [1,2,5,6,1], removeQueries = [0,3,2,4,1]
Output: [14,7,2,2,0]
Explanation: Using 0 to indicate a removed element, the answer is as follows:
Query 1: Remove the 0th element, nums becomes [0,2,5,6,1] and the maximum segment sum is 14 for segment [2,5,6,1].
Query 2: Remove the 3rd element, nums becomes [0,2,5,0,1] and the maximum segment sum is 7 for segment [2,5].
Query 3: Remove the 2nd element, nums becomes [0,2,0,0,1] and the maximum segment sum is 2 for segment [2]. 
Query 4: Remove the 4th element, nums becomes [0,2,0,0,0] and the maximum segment sum is 2 for segment [2]. 
Query 5: Remove the 1st element, nums becomes [0,0,0,0,0] and the maximum segment sum is 0, since there are no segments.
Finally, we return [14,7,2,2,0].
```

**Example 2:**

```
Input: nums = [3,2,11,1], removeQueries = [3,2,1,0]
Output: [16,5,3,0]
Explanation: Using 0 to indicate a removed element, the answer is as follows:
Query 1: Remove the 3rd element, nums becomes [3,2,11,0] and the maximum segment sum is 16 for segment [3,2,11].
Query 2: Remove the 2nd element, nums becomes [3,2,0,0] and the maximum segment sum is 5 for segment [3,2].
Query 3: Remove the 1st element, nums becomes [3,0,0,0] and the maximum segment sum is 3 for segment [3].
Query 4: Remove the 0th element, nums becomes [0,0,0,0] and the maximum segment sum is 0, since there are no segments.
Finally, we return [16,5,3,0].
```

**Constraints**

- n == nums.length == removeQueries.length
- 1 <= n <= 105
- 1 <= nums[i] <= 109
- 0 <= removeQueries[i] < n
- All the values of removeQueries are unique.

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的整数数组 `nums` 和 `removeQueries`，它们的长度均为 `n`。第 `i` 次查询会删除 `nums` 中下标为 `removeQueries[i]` 的元素，导致 `nums` 被划分成若干不相交的 **子段（segment）**。  
**子段** 是 `nums` 中连续的正整数序列。**子段和** 是子段中所有元素的和。  

返回一个长度为 `n` 的整数数组 `answer`，其中 `answer[i]` 为执行第 `i` 次删除后所有子段的 **最大子段和（maximum segment sum）**。  
> 注意：同一个下标不会被删除多次。

---

## 示例

### 示例 1

**输入**  
```text
nums = [1,2,5,6,1], removeQueries = [0,3,2,4,1]
```

**输出**  
```text
[14,7,2,2,0]
```

**解释**  
用 `0` 表示已删除的元素，过程如下：

- 查询 1：删除下标 `0` 的元素，`nums` 变为 `[0,2,5,6,1]`，最大子段和为 `14`（子段 `[2,5,6,1]`）。
- 查询 2：删除下标 `3` 的元素，`nums` 变为 `[0,2,5,0,1]`，最大子段和为 `7`（子段 `[2,5]`）。
- 查询 3：删除下标 `2` 的元素，`nums` 变为 `[0,2,0,0,1]`，最大子段和为 `2`（子段 `[2]` 或 `[1]`）。
- 查询 4：删除下标 `4` 的元素，`nums` 变为 `[0,2,0,0,0]`，最大子段和为 `2`（子段 `[2]`）。
- 查询 5：删除下标 `1` 的元素，`nums` 变为 `[0,0,0,0,0]`，最大子段和为 `0`（不存在正整数子段）。

### 示例 2

**输入**  
```text
nums = [3,2,11,1], removeQueries = [3,2,1,0]
```

**输出**  
```text
[16,5,3,0]
```

**解释**  
用 `0` 表示已删除的元素，过程如下：

- 查询 1：删除下标 `3` 的元素，`nums` 变为 `[3,2,11,0]`，最大子段和为 `16`（子段 `[3,2,11]`）。
- 查询 2：删除下标 `2` 的元素，`nums` 变为 `[3,2,0,0]`，最大子段和为 `5`（子段 `[3,2]`）。
- 查询 3：删除下标 `1` 的元素，`nums` 变为 `[3,0,0,0]`，最大子段和为 `3`（子段 `[3]`）。
- 查询 4：删除下标 `0` 的元素，`nums` 变为 `[0,0,0,0]`，最大子段和为 `0`（不存在正整数子段）。

---

## 约束条件

- `n == nums.length == removeQueries.length`
- `1 <= n <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= removeQueries[i] < n`
- `removeQueries` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步一步模拟** 题目描述的过程：

1. 先把 `nums` 原封不动放在一个列表里。  
2. 按照 `removeQueries` 的顺序，把对应下标的元素设为 **0**（相当于“被移除”）。  
3. 每一次移除后，从左到右遍历整个数组，找出所有 **连续的正整数**（即不为 0 的子数组），把每个子数组的元素相加得到该段的 **segment sum**。  
4. 记录这些段的最大和，就是本次查询的答案。

> **类比**：把数组想象成一条街道，街道上每栋房子里都有钱（`nums[i]`），移除操作就是把房子炸掉，炸掉的房子里钱变成 0。我们每次都要走一遍街道，看看哪些房子还连在一起，算出它们的钱总和，找出最多的钱。

**为什么正确**：  
因为我们没有漏掉任何一步——每一次都完整地把“炸掉”后的街道重新检查一遍，必然能得到真实的最大段和。

**时间/空间复杂度**（大白话）：

- **时间**：  
  - 第 `i` 次查询要遍历整个数组 `n` 次（`n` ≤ 10⁵），  
  - 一共要做 `n` 次查询 → 大约是 `n × n` 次操作。  
  - 用 **O(n²)** 来表示，就是“把 n × n 次小事儿都做完”。对 10⁵ 的规模来说，已经太慢了（≈ 10¹⁰ 次）。
- **空间**：  
  - 只用了原数组和几个临时变量 → **O(1)** 额外空间。

#### 代码（Python）

```python
from typing import List

def maximumSegmentSum_bruteforce(nums: List[int], removeQueries: List[int]) -> List[int]:
    n = len(nums)
    # 用一个拷贝来模拟“被移除后置为 0”
    cur = nums[:]
    ans = []

    for idx in removeQueries:
        # 1) 把该位置设为 0（相当于被删除）
        cur[idx] = 0

        # 2) 扫描整个数组，计算每个连续正数段的和，取最大
        max_seg = 0          # 当前查询的最大段和
        cur_sum = 0          # 正在累加的段的和
        for v in cur:
            if v > 0:        # 仍然在同一段里
                cur_sum += v
                max_seg = max(max_seg, cur_sum)
            else:            # 遇到 0，段结束
                cur_sum = 0

        ans.append(max_seg)

    return ans
```

> 关键行注释已经用中文写明。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：如果 `n = 1000`，大约需要做 1,000,000 次基本操作；`n = 10⁵` 时就会爆炸。
- **空间复杂度**：`O(1)`（不计答案数组）  
  - 只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次查询都要完整遍历数组**。我们需要一种办法，让每一次“移除”只影响局部，而不必重新扫描全部。

**逆向思考**：  
- 题目让我们 **逐步删除** 元素，得到每一步的最大段和。  
- 如果把过程 **倒过来**：从全部元素都已经被删除的状态（全是 0）开始，**逐步恢复** 被删除的元素。  
- 当我们把一个元素 **恢复**（把 0 改回原来的正数）时，它只会和左边、右边已经恢复的相邻段**合并**，形成一个更大的段。  

这样，每一步只涉及 **最多两个相邻段的合并**，时间就可以降到线性。

要实现逆向恢复，需要两件事：

1. **快速合并相邻段**  
   - 使用 **并查集（Union‑Find）** 来记录每个位置所属的 “连通块”。  
   - 每个连通块维护 **该块所有元素的和**（即段和）。  
   - 合并时把两个块的和相加，更新根节点的和。

2. **随时得到当前所有块的最大段和**  
   - 维护一个全局变量 `cur_max`，每次合并后只需要比较新块的和与 `cur_max`，取较大者。  
   - 由于我们是**逆向**处理，答案数组需要在最后再 **反转** 回去。

> **类比**：把数组想象成一条被砍掉的树枝，最开始所有枝桠都被锯断（全是 0）。我们从树根往外“重新拼接”枝桠，每拼一次，只会把左边的枝桠、右边的枝桠和自己这段拼在一起，得到一根更长的枝桠。最长的枝桠长度（段和）随时可以用一个变量记录。

**并查集基础**（给零基础的同学）：

- 每个位置有一个 **父指针** `parent[i]`，指向它所在集合的代表（根）。  
- `find(i)`：沿着父指针一直往上找，直到找到根。  
- `union(a, b)`：把 `a` 所在集合和 `b` 所在集合合并，让一个根指向另一个根。  
- 为了加速，我们常用 **路径压缩**（在 `find` 过程中把沿途的节点直接挂到根上）和 **按大小合并**（把小集合挂到大集合下），这样几乎可以认为每次操作都是 `O(1)`，整体是 `O(n α(n))`（α 为极慢增长的反 Ackermann 函数）。

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集，带有每个集合的和"""
    def __init__(self, n: int, vals: List[int]):
        self.parent = list(range(n))      # 父指针
        self.size   = [1] * n             # 集合大小（用于按大小合并）
        self.sum    = vals[:]             # 当前根节点对应的段和

    def find(self, x: int) -> int:
        """路径压缩"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> int:
        """把 a、b 所在集合合并，返回合并后根节点的段和"""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:                      # 已经在同一个集合里
            return self.sum[ra]

        # 按大小合并：把小集合挂到大集合下
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.sum[ra] += self.sum[rb]       # 更新根的段和
        return self.sum[ra]                # 返回新的段和


def maximumSegmentSum(nums: List[int], removeQueries: List[int]) -> List[int]:
    n = len(nums)
    # 逆向思考：一开始全部删除，用 0 表示
    alive = [False] * n          # 标记哪些位置已经“恢复”
    dsu = DSU(n, [0] * n)        # 初始所有段和为 0
    ans = [0] * n                # 逆序答案
    cur_max = 0                  # 当前所有已恢复段的最大和

    # 从最后一次查询倒着往前恢复
    for step in range(n - 1, -1, -1):
        idx = removeQueries[step]        # 这一步要恢复的位置
        alive[idx] = True
        dsu.sum[idx] = nums[idx]         # 把该位置的真实值写进并查集

        # 检查左、右邻居是否已经恢复，若是则合并
        if idx - 1 >= 0 and alive[idx - 1]:
            cur_max = max(cur_max, dsu.union(idx, idx - 1))
        if idx + 1 < n and alive[idx + 1]:
            cur_max = max(cur_max, dsu.union(idx, idx + 1))

        # 合并完后，自己所在块的和也要和 cur_max 比较
        cur_max = max(cur_max, dsu.sum[dsu.find(idx)])

        ans[step] = cur_max               # 记录此时的最大段和

    return ans
```

> **代码要点解释**  
> - `alive` 用来判断相邻位置是否已经恢复，防止错误合并。  
> - `dsu.sum` 在恢复时从 `0` 变成真实的 `nums[idx]`，随后通过 `union` 把相邻块的和累加。  
> - `cur_max` 只会 **单调不减**（因为恢复只会让段和变大或保持不变），所以直接取最大即可。  
> - 最后返回的 `ans` 已经是正序的，因为我们在逆向循环时把答案写进对应的下标。

#### 复杂度

- **时间复杂度**：`O(n α(n)) ≈ O(n)`  
  - 解释：每个位置只会被 **恢复一次**，并查集的 `find / union` 操作几乎是常数时间，整体随 `n` 线性增长。对 10⁵ 的数据量完全可以在毫秒级完成。  
- **空间复杂度**：`O(n)`  
  - 需要额外的 `parent、size、sum、alive、ans` 五个长度为 `n` 的数组。

---

## 心得

- **核心技巧**：**逆向思考 + 并查集**。把“删除”转成“恢复”，利用并查集快速合并相邻段并维护段和。
- **适用的题型**  
  1. “在数组上动态删除/添加，要求维护某种区间属性”（如 **Maximum Segment Sum After Removals**、**Maximum Consecutive Ones After Deletions**）。  
  2. “在离线查询中，需要快速合并相邻区间”——典型的 **Union‑Find + Offline** 思路（如 **LeetCode 1202. Smallest String With Swaps** 的变体）。  
  3. “动态连通性” 类问题（如 **Number of Islands II**）。
- **一句话总结解题钥匙**：**把难以增量维护的“删除”逆向为“添加”，并用并查集把相邻块快速合并**。

---

## 反思

- **拿到题目第一反应**：直接模拟删除，逐次遍历求最大段和——这是最自然的暴力思路。  
- **最容易踩的坑**  
  1. **时间限制**：直接遍历会导致 `O(n²)`，在 `n=10⁵` 时必超时。  
  2. **边界条件**：恢复第一个或最后一个元素时，左/右邻居可能不存在，需要额外判断。  
  3. **并查集的初始化**：一开始所有段和为 0，恢复时要记得把 `sum[idx]` 设回真实值，否则合并后得到的和会错误。  
- **下次遇到同类题，第一步该想到**：**能否把操作倒着做**（逆向思考），并检查是否能用 **Union‑Find** 或 **线段树** 等结构在 **局部** 完成合并/更新，而不是全局遍历。这样往往能把 `O(n²)` 降到 `O(n log n)` 或 `O(n)`。