# #2940. **寻找 Alice 与 Bob 能相遇的建筑** / Find Building Where Alice and Bob Can Meet

> 难度：困难 · 标签：Array、Binary Search、Stack、Binary Indexed Tree、Segment Tree、Heap (Priority Queue)、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/find-building-where-alice-and-bob-can-meet/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array heights of positive integers, where heights[i] represents the height of the ith building.
If a person is in building i, they can move to any other building j if and only if i < j and heights[i] < heights[j].
You are also given another array queries where queries[i] = [ai, bi]. On the ith query, Alice is in building ai while Bob is in building bi.
Return an array ans where ans[i] is the index of the leftmost building where Alice and Bob can meet on the ith query. If Alice and Bob cannot move to a common building on query i, set ans[i] to -1.

**Examples**

**Example 1:**

```
Input: heights = [6,4,8,5,2,7], queries = [[0,1],[0,3],[2,4],[3,4],[2,2]]
Output: [2,5,-1,5,2]
Explanation: In the first query, Alice and Bob can move to building 2 since heights[0] < heights[2] and heights[1] < heights[2]. 
In the second query, Alice and Bob can move to building 5 since heights[0] < heights[5] and heights[3] < heights[5]. 
In the third query, Alice cannot meet Bob since Alice cannot move to any other building.
In the fourth query, Alice and Bob can move to building 5 since heights[3] < heights[5] and heights[4] < heights[5].
In the fifth query, Alice and Bob are already in the same building.  
For ans[i] != -1, It can be shown that ans[i] is the leftmost building where Alice and Bob can meet.
For ans[i] == -1, It can be shown that there is no building where Alice and Bob can meet.
```

**Example 2:**

```
Input: heights = [5,3,8,2,6,1,4,6], queries = [[0,7],[3,5],[5,2],[3,0],[1,6]]
Output: [7,6,-1,4,6]
Explanation: In the first query, Alice can directly move to Bob's building since heights[0] < heights[7].
In the second query, Alice and Bob can move to building 6 since heights[3] < heights[6] and heights[5] < heights[6].
In the third query, Alice cannot meet Bob since Bob cannot move to any other building.
In the fourth query, Alice and Bob can move to building 4 since heights[3] < heights[4] and heights[0] < heights[4].
In the fifth query, Alice can directly move to Bob's building since heights[1] < heights[6].
For ans[i] != -1, It can be shown that ans[i] is the leftmost building where Alice and Bob can meet.
For ans[i] == -1, It can be shown that there is no building where Alice and Bob can meet.
```

**Constraints**

- 1 <= heights.length <= 5 * 104
- 1 <= heights[i] <= 109
- 1 <= queries.length <= 5 * 104
- queries[i] = [ai, bi]
- 0 <= ai, bi <= heights.length - 1

---

## 题目（中文翻译）

给定一个下标从 0 开始的正整数数组 `heights`，其中 `heights[i]` 表示第 `i` 栋建筑的高度。  
如果一个人位于建筑 `i`，当且仅当 `i < j` 且 `heights[i] < heights[j]` 时，他可以移动到任意其他建筑 `j`（满足上述条件）。

同时给定另一个数组 `queries`，其中 `queries[i] = [a_i, b_i]`。在第 `i` 条查询中，Alice 位于建筑 `a_i`，Bob 位于建筑 `b_i`。  

返回一个数组 `ans`，其中 `ans[i]` 为第 `i` 条查询中 Alice 和 Bob 能相遇的最左侧建筑的下标。如果在第 `i` 条查询中 Alice 与 Bob 无法移动到同一建筑，则 `ans[i] = -1`。

---

### 示例

**示例 1**  

```
Input: heights = [6,4,8,5,2,7], queries = [[0,1],[0,3],[2,4],[3,4],[2,2]]
Output: [2,5,-1,5,2]
Explanation: 在第一条查询中，Alice 和 Bob 可以移动到建筑 2，因为 heights[0] < heights[2] 且 heights[1] < heights[2]。  
In the second query, Alice and Bob can move to building 5 since heights[0] < heights[5] and heights[3] < heights[5].  
In the third query, Alice cannot meet Bob since Alice can
... (已截断)
```

**示例 2**  

```
Input: heights = [5,3,8,2,6,1,4,6], queries = [[0,7],[3,5],[5,2],[3,0],[1,6]]
Output: [7,6,-1,4,6]
Explanation: 在第一条查询中，Alice 可以直接移动到 Bob 所在的建筑，因为 heights[0] < heights[7]。  
In the second query, Alice and Bob can move to building 6 since heights[3] < heights[6] and heights[5] < heights[6].  
In the third query, Alice cannot meet Bob since Bob cannot move to any other b
... (已截断)
```

---

### 约束条件

- `1 <= heights.length <= 5 * 10^4`
- `1 <= heights[i] <= 10^9`
- `1 <= queries.length <= 5 * 10^4`
- `queries[i] = [a_i, b_i]`
- `0 <= a_i, b_i <= heights.length - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次查询当成一次**模拟**：  
1. 先把 `ai , bi` 按照下标从小到大排好（如果 `ai > bi` 就把它们换一下），记为 `x ≤ y`。  
2. 检查两个人能否直接到达对方的建筑：  
   * 如果 `heights[x] < heights[y]`，说明从左边的建筑 `x` 可以一步跳到右边的 `y`，答案就是 `y`。  
3. 否则两个人都只能往更高的右边建筑走。我们从 `y+1` 开始向右扫描，找到第一个高度 **严格大于** `heights[x]` 的建筑 `t`，因为  
   * `heights[x] ≥ heights[y]`，所以 `heights[t] > heights[x] ≥ heights[y]`，这座建筑既能被 `x` 也能被 `y` 到达。  
4. 如果一直找不到满足条件的 `t`，说明两人永远走不到同一座楼，答案是 `-1`。

> **类比**：把建筑想象成一排向右的楼梯，只能往更高的台阶上走。我们要找的就是“从左边的台阶 `x` 开始，往右数第一个比它更高的台阶”。  

这个思路一定能得到正确答案，因为我们把所有合法的移动路径都枚举了——只要有一座建筑同时满足 `> heights[x]` 且在 `y` 的右边，它就一定是最左边的公共可达建筑。

#### 代码（Python）

```python
from typing import List

def meetBuilding_bruteforce(heights: List[int], queries: List[List[int]]) -> List[int]:
    n = len(heights)
    ans = []

    for a, b in queries:
        # 1. 保证 x ≤ y
        x, y = (a, b) if a <= b else (b, a)

        # 2. 能直接相遇的情况
        if heights[x] < heights[y]:
            ans.append(y)
            continue

        # 3. 暴力向右找第一个更高的建筑
        meet = -1
        for t in range(y + 1, n):
            if heights[t] > heights[x]:      # 只要比左边最高的那座楼高就行
                meet = t
                break

        ans.append(meet)                     # 若找不到则为 -1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(q * n)`  
  对每个查询最坏需要遍历一次整个数组（`n`），所以总时间是查询数 `q` 乘以 `n`。  
  大白话：如果数组有 10 000 块楼，查询有 10 000 条，最坏要跑 **一亿次**循环，显然太慢了。  
- **空间复杂度**：`O(1)`（不计输出数组）  
  只用了常数级别的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要从 `y+1` 向右线性扫描**，这会导致 `O(q·n)` 的时间。  
我们要把“找第一个高度 > `heights[x]` 的位置”这一步加速。

观察可以发现：

* 对于同一个右端点 `y`，所有查询只关心 **在 `y` 右侧的建筑**。  
* 如果我们从右往左一次性把所有右侧建筑加入某个结构，并且能够**快速二分**出第一个满足 `height > H` 的下标，就能把每个查询的查找时间降到 `O(log n)`。

这正好可以用 **单调栈 + 二分搜索** 来实现。

##### 关键数据结构——单调栈  

- **栈的定义**：从右往左遍历数组时，维护一个只保存“递减高度”的下标栈 `stack`。  
- **为什么是递减？**  
  当我们把一个新下标 `i` 加入栈时，若它的高度不低于栈顶的高度（`heights[i] >= heights[stack[-1]]`），栈顶就永远不可能成为“更高建筑的左边最近位置”，于是把它弹出。  
  这样栈里保存的下标对应的高度严格递减：`heights[stack[0]] > heights[stack[1]] > …`。  
- **性质**：栈中的下标是严格递增的（因为我们是从右往左插入的），而对应的高度是严格递减的。这正好让我们可以 **对高度二分**，找到第一个高度 > 某个阈值的下标。

##### 处理查询的顺序  

- 将所有查询按右端点 `y` **从大到小** 排序。  
- 用一个指针 `i` 从数组最右侧向左移动，**一次性把所有下标 > 当前查询的 `y`** 加入单调栈。  
- 当处理完当前查询后，栈已经包含了 **所有** 位置 `> y`，且保持单调递减。此时只要在栈里二分查找第一个高度 > `heights[x]`（其中 `x` 为左侧下标），得到的下标就是答案的左边界。

##### 步骤概览  

1. **预处理**：把查询记成 `(x, y, idx)`（`idx` 为原始顺序），如果 `x > y` 先交换，使 `x ≤ y`。  
2. **排序**：按 `y` 降序排列这些查询。  
3. **遍历**：  
   - 初始化 `i = n-1`（指向最右侧建筑），`stack = []`。  
   - 对每个查询 `(x, y, idx)`（从大到小的 `y`）：  
     a. **把右侧建筑加入栈**：`while i > y:`  
        - 弹出所有高度 ≤ `heights[i]`（保持递减），然后 `stack.append(i)`，`i -= 1`。  
     b. **直接相遇的特殊情况**：如果 `heights[x] < heights[y]`，答案就是 `y`。  
     c. **二分搜索**：在 `stack` 中找第一个满足 `heights[stack[pos]] > heights[x]` 的位置 `pos`（使用 `bisect_left` 的自定义键）。如果找到，答案是 `stack[pos]`，否则为 `-1`。  
4. **恢复原顺序**：把答案写回 `ans[idx]`，最后返回。

##### 为什么正确？

* **单调栈保证**：栈中所有下标都严格大于当前查询的 `y`，且对应的高度从左到右严格递减。  
* **二分的充分性**：我们要找的建筑只需要满足 `height > heights[x]`（因为 `heights[x] ≥ heights[y]`），在递减序列中，第一次出现“大于阈值”的位置恰好是**最左边**满足条件的下标。  
* **覆盖所有可能**：若答案存在，它一定在 `y` 右侧，且高度一定大于 `heights[x]`，所以一定会出现在栈里。若栈里没有满足条件的元素，说明右侧再也没有更高的楼，答案只能是 `-1`。  

因此，算法既完整又不遗漏任何合法答案。

#### 代码（Python）

```python
from typing import List
import bisect

def meetBuilding(heights: List[int], queries: List[List[int]]) -> List[int]:
    n = len(heights)
    m = len(queries)

    # 1️⃣ 把查询统一成 (x, y, original_index)，并保证 x ≤ y
    qs = []
    for idx, (a, b) in enumerate(queries):
        x, y = (a, b) if a <= b else (b, a)
        qs.append((x, y, idx))

    # 2️⃣ 按 y 降序排序
    qs.sort(key=lambda t: -t[1])

    ans = [-1] * m          # 最终答案
    stack = []              # 单调栈，存下标，对应的 heights 递减
    i = n - 1               # 从最右侧开始往左加入栈

    for x, y, idx in qs:
        # ---------- 把所有下标 > y 加入单调栈 ----------
        while i > y:
            # 维持栈中 heights 单调递减
            while stack and heights[i] >= heights[stack[-1]]:
                stack.pop()
            stack.append(i)
            i -= 1

        # ---------- 特殊情况：直接相遇 ----------
        if heights[x] < heights[y]:
            ans[idx] = y
            continue

        # ---------- 在栈里二分找第一个 height > heights[x] ----------
        # 为了二分，我们需要一个只包含 heights 的列表（保持同序）
        # 由于 heights[stack] 递减，二分找“> target”可以转化为
        # “在递减序列中找左侧第一个 > target”，使用 bisect_left
        # 但 bisect 只能在递增序列上工作，这里我们手写二分。
        lo, hi = 0, len(stack) - 1
        pos = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if heights[stack[mid]] > heights[x]:
                pos = mid          # 可能的答案，继续左边找更左
                hi = mid - 1
            else:
                lo = mid + 1

        ans[idx] = stack[pos] if pos != -1 else -1

    return ans
```

> **代码要点注释**  
> * `while i > y:` 把所有右侧建筑一次性加入栈，保证每个下标只进出栈 **一次**，所以总的栈操作是 `O(n)`。  
> * 手写二分是因为 `heights[stack]` 是递减的，直接用 `bisect` 需要额外的“负号”技巧，这里写得更直观。  
> * 最后把答案写回原始查询下标 `idx`，保证返回顺序和输入一致。

#### 复杂度  

- **时间复杂度**：`O((n + q) log n)`  
  *加入栈* 的过程每个下标最多被弹出一次、压入一次，线性 `O(n)`。  
  对每个查询在栈上二分，`O(log n)`，共 `q` 次。整体比暴力的 `O(q·n)` 快了几个数量级。  
  大白话：如果 `n = 5·10⁴, q = 5·10⁴`，则约 `10⁵·log2·10⁵ ≈ 1.7·10⁶` 次基本运算，完全可以在一秒内跑完。

- **空间复杂度**：`O(n)`  
  主要是单调栈保存的下标（最坏会保存所有下标），以及存放答案的数组。相较于输入规模，这已经是线性的最小代价。

---

## 心得

- **核心技巧**：**单调栈 + 二分**。单调栈把“右侧更高建筑”压缩成一个递减序列，二分在其中快速定位第一个满足高度阈值的下标。  
- **适用题型**  
  1. “左/右侧最近的更大/更小元素”类问题（如 Next Greater Element、寻找左侧第一个满足条件的下标）。  
  2. 需要对 **同一方向的区间** 多次查询“第一个满足阈值的元素”时（如区间最大/最小查询的离线解法）。  
- **一句话总结**：把所有“右侧可达的更高楼”压进单调栈，二分找第一个比左侧最高楼更高的，即是两人最左的会合点。

---

## 反思

- **第一反应**：看到“只能向右走且必须更高”，马上想到 **单调栈**（常用于“下一个更高楼”），但最开始我会先尝试 **直接遍历**，导致时间超限。  
- **最容易踩的坑**  
  1. **下标顺序**：忘记先把 `ai, bi` 按下标排序，导致在 `y` 左侧错误地加入了建筑。  
  2. **高度比较**：只比较 `heights[y]` 与 `heights[x]` 不够，必须在 `heights[x] ≥ heights[y]` 时才去找更高的建筑。  
  3. **二分条件**：栈中高度是递减的，使用普通 `bisect_left`（递增）会出错，需要自行实现或把高度取负数。  
- **下次思路**：面对“只能向一个方向移动且有单调约束”的题目，第一步就把查询 **离线**（按某个方向排序），然后寻找可以 **单调维护** 的结构（栈、单调队列、线段树）来把每次查询的复杂度压到 `log` 级别。这样既能保证正确性，又能轻松突破时间限制。