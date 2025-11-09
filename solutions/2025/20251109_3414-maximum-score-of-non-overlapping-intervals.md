# #3414. 最大不重叠区间的得分 / Maximum Score of Non-overlapping Intervals

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-score-of-non-overlapping-intervals/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array intervals, where intervals[i] = [li, ri, weighti]. Interval i starts at position li and ends at ri, and has a weight of weighti. You can choose up to 4 non-overlapping intervals. The score of the chosen intervals is defined as the total sum of their weights.
Return the lexicographically smallest array of at most 4 indices from intervals with maximum score, representing your choice of non-overlapping intervals.
Two intervals are said to be non-overlapping if they do not share any points. In particular, intervals sharing a left or right boundary are considered overlapping.

**Examples**

**Example 1:**

```
Input: intervals = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]
Output: [2,3]
Explanation:
You can choose the intervals with indices 2, and 3 with respective weights of 5, and 3.
```

**Example 2:**

```
Input: intervals = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]
Output: [1,3,5,6]
Explanation:
You can choose the intervals with indices 1, 3, 5, and 6 with respective weights of 7, 6, 3, and 5.
```

**Constraints**

- 1 <= intevals.length <= 5 * 104
- intervals[i].length == 3
- intervals[i] = [li, ri, weighti]
- 1 <= li <= ri <= 109
- 1 <= weighti <= 109

---

## 题目（中文翻译）

给定一个二维整数数组 `intervals`，其中 `intervals[i] = [l_i, r_i, weight_i]`。区间 `i` 的左端点为 `l_i`，右端点为 `r_i`，权重为 `weight_i`。你可以选择至多 4 个互不重叠的区间（non-overlapping intervals）。所选区间的得分定义为它们权重的总和。

返回一个长度不超过 4 的索引数组（indices），该数组在得分最大时按字典序（lexicographically）最小，表示你选择的互不重叠区间。

**区间的非重叠定义**：两个区间若没有任何公共点则视为非重叠。特别地，若两个区间共享左端点或右端点，则视为重叠。

---

## 示例

### 示例 1
**输入**  
`intervals = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]`

**输出**  
`[2,3]`

**解释**  
可以选择索引为 2 和 3 的区间，它们的权重分别为 5 和 3，得到的总得分为 8。

### 示例 2
**输入**  
`intervals = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]`

**输出**  
`[1,3,5,6]`

**解释**  
可以选择索引为 1、3、5、6 的区间，它们的权重分别为 7、6、3、5，得到的总得分为 21。

---

## 约束条件

- `1 <= intervals.length <= 5 * 10^4`
- `intervals[i].length == 3`
- `intervals[i] = [l_i, r_i, weight_i]`
- `1 <= l_i <= r_i <= 10^9`
- `1 <= weight_i <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的「最多 4 条不重叠区间」的组合枚举一遍，算出每种组合的权重和，挑出最大值，再在最大值相同的组合里挑字典序最小的那一个。

- **枚举组合**：可以把 `intervals` 看成一本“区间目录”。我们要从这本目录里挑出 1、2、3 或 4 本书，使得它们的页码区间互不相交（左端点和右端点都不能碰到）。这相当于在所有区间集合中遍历子集，子集大小不超过 4。
- **检验不重叠**：把两个区间的左、右端点拿出来比较，如果 `a.r < b.l` 并且 `b.r < a.l`（因为左边界相等也算重叠），则它们不冲突。可以把「是否冲突」想象成两个人的约会时间是否有交叉，交叉就算冲突。
- **记录最佳**：遍历完所有合法组合后，比较它们的总权重，挑出最大的；若有多个组合权重相同，则比较它们的索引序列（字典序），取最小的。

> **为什么暴力一定能得到正确答案？**  
> 因为我们把「所有可能」都列举出来，真正的最优解一定在其中。只要检验条件（不重叠）写对，结果必然正确。

> **时间/空间复杂度**  
> - 枚举所有子集的时间是指数级的。设区间数为 `n`，最多挑 4 条，则组合数为 `C(n,1)+C(n,2)+C(n,3)+C(n,4) = O(n^4)`。当 `n` 达到几千甚至上万时，这根本不可行。  
> - 需要的额外空间只有保存当前组合的索引和最大解，都是 `O(1)`。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def max_score_bruteforce(intervals: List[List[int]]) -> List[int]:
    n = len(intervals)
    best_score = -1          # 记录最高权重和
    best_idx = []            # 记录对应的索引序列（字典序最小）

    # 枚举选取 1~4 条区间的所有组合
    for k in range(1, 5):
        for combo in combinations(range(n), k):
            # 检查组合中的区间是否两两不重叠
            ok = True
            for i in range(k):
                li, ri, _ = intervals[combo[i]]
                for j in range(i + 1, k):
                    lj, rj, _ = intervals[combo[j]]
                    # 只要有一点相同或交叉就算重叠
                    if not (ri < lj or rj < li):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue

            # 计算当前组合的总权重
            cur_score = sum(intervals[idx][2] for idx in combo)

            # 更新答案：先比权重，大则更新；权重相同则比字典序，小则更新
            if (cur_score > best_score) or (cur_score == best_score and list(combo) < best_idx):
                best_score = cur_score
                best_idx = list(combo)

    return best_idx
```

> 关键行注释已在代码中给出，直接运行即可（但仅适用于 `n` 很小的测试）。

#### 复杂度

- **时间复杂度**：`O(n^4)`  
  这表示如果 `n=100`，大约需要 `100^4 = 10^8` 次遍历，已经非常慢；而题目允许 `n` 达到 `5·10⁴`，根本不可能跑完。
- **空间复杂度**：`O(1)`（不计输入本身）  
  只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于「每次都要遍历所有组合」以及「每次都要线性检查是否冲突」。我们需要把「找不冲突的前一个区间」这一步变得快速，同时利用「最多只能选 4 条」的限制做动态规划。

1. **先把区间按右端点排序**  
   - 想象把所有约会按结束时间排成一列，早结束的约会先安排，这样在考虑第 `i` 条约会时，所有可能的「前一个不冲突的约会」必然出现在它左边。  
   - 排序后，`intervals[i]` 的右端点一定 **≥** `intervals[i-1]` 的右端点。

2. **二分查找前一个不冲突的区间**  
   - 对于排好序的第 `i` 条区间，我们想找最大的下标 `j < i` 使得 `intervals[j].right < intervals[i].left`（左边界严格小于右边界）。  
   - 因为右端点已经是递增的，`j` 可以通过二分搜索在 `O(log n)` 时间得到。  
   - 这一步相当于在「字典」里找「最近的、且不冲突的」条目，二分搜索就像快速翻页查找。

3. **动态规划 (DP) 设状态**  
   - 设 `dp[k][i]` 为「在前 `i`（含）个区间中，最多选 `k` 条不重叠区间能得到的最大权重和」以及对应的「最小字典序索引序列」。  
   - `k` 取值为 `0~4`，`i` 取值为 `1~n`（为方便起见把下标从 1 开始）。

4. **状态转移**  
   - **不选第 i 条**：`dp[k][i] = dp[k][i-1]`（保持之前的最优）。
   - **选第 i 条**：需要把它的权重加到「选 `k-1` 条且不冲突的」最优上。  
     - 前一个不冲突的下标记作 `pre = prev[i]`（二分得到）。  
     - 那么「选第 i 条」得到的总权重是 `intervals[i].weight + dp[k-1][pre]`。  
   - 取两者的更大者；若相等则比较对应的索引序列，保留字典序更小的那一个。

5. **实现细节**  
   - 为了同时保存「权重」和「索引序列」，我们让 `dp[k][i]` 存储一个二元组 `(score, idx_list)`。  
   - `idx_list` 用 Python 的 `list` 保存索引（已是升序），比较时直接使用列表的字典序特性。  
   - `dp[0][*]` 的分数始终为 `0`，索引列表为空。  
   - 最终答案是 `dp[4][n]`（最多 4 条），但也要考虑实际选的条数可能少于 4 条——只要 `score` 最大即可。

6. **复杂度分析**  
   - 排序 `O(n log n)`。  
   - 预处理 `prev`（二分）对每个 `i` `O(log n)`，共 `O(n log n)`。  
   - DP 循环 `k=1..4`、`i=1..n`，每次只做常数次比较，`O(4·n) = O(n)`。  
   - 总时间 `O(n log n)`，空间 `O(4·n)`（约 `4n` 个二元组），在本题的 `5·10⁴` 规模下完全可行。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List, Tuple

def max_score_intervals(intervals: List[List[int]]) -> List[int]:
    """
    返回字典序最小、权重和最大的至多 4 条不重叠区间的索引列表（原始下标）。
    """
    n = len(intervals)

    # 1. 记录原始下标，方便最后返回答案
    intervals = [(l, r, w, idx) for idx, (l, r, w) in enumerate(intervals)]

    # 2. 按右端点升序排序（若右端点相同，左端点升序，保证唯一顺序）
    intervals.sort(key=lambda x: (x[1], x[0]))

    # 3. 提取左端点、右端点、权重、原始下标的独立列表，方便二分
    L = [it[0] for it in intervals]
    R = [it[1] for it in intervals]
    W = [it[2] for it in intervals]
    IDX = [it[3] for it in intervals]

    # 4. 预处理 prev[i]：i 之前最大的下标 j，使得 R[j] < L[i]
    #    使用二分在 R 中查找第一个 >= L[i] 的位置，然后向左移动一位
    prev = [-1] * n          # -1 表示不存在不冲突的前区间
    for i in range(n):
        # 在 R[0..i-1] 中找第一个右端点 >= L[i]
        pos = bisect_left(R, L[i], 0, i)   # 只在左侧范围内搜索
        prev[i] = pos - 1                  # 前一个不冲突的下标（可能为 -1）

    # 5. DP 表：dp[k][i] = (max_score, best_index_list)
    #    为了节省空间，使用二维列表，其中 i 从 0~n（0 表示“空前缀”）
    dp: List[List[Tuple[int, List[int]]]] = [
        [(0, []) for _ in range(n + 1)]   # k = 0 时，分数 0，索引为空
        for _ in range(5)                 # k = 0~4
    ]

    # 6. 动态规划
    for k in range(1, 5):          # 选 1~4 条
        for i in range(1, n + 1):  # 处理第 i-1 个区间（因为 dp 下标比 intervals 多 1）
            # 不选第 i-1 条
            not_pick = dp[k][i - 1]

            # 选第 i-1 条
            j = prev[i - 1]                     # 前一个不冲突的下标
            pick_score = W[i - 1] + dp[k - 1][j + 1][0]   # j+1 把下标映射到 dp 表
            pick_idx = dp[k - 1][j + 1][1] + [IDX[i - 1]]  # 追加当前原始下标

            # 取更大的分数；若相等则取字典序更小的索引列表
            if pick_score > not_pick[0]:
                dp[k][i] = (pick_score, pick_idx)
            elif pick_score < not_pick[0]:
                dp[k][i] = not_pick
            else:   # 分数相等，比较字典序
                dp[k][i] = not_pick if not_pick[1] <= pick_idx else (pick_score, pick_idx)

    # 7. 在 dp[1..4][n] 中挑出分数最高且字典序最小的答案
    best_score = -1
    best_idx = []
    for k in range(1, 5):
        cur_score, cur_idx = dp[k][n]
        if cur_score > best_score:
            best_score, best_idx = cur_score, cur_idx
        elif cur_score == best_score and cur_idx < best_idx:
            best_idx = cur_idx

    # 结果已经是原始下标的升序列表（因为我们始终保持升序添加），直接返回
    return best_idx
```

**代码要点解释**

| 行号 | 作用 | 类比/解释 |
|------|------|-----------|
| 4‑7  | 把每个区间记上原始下标 | 像给每本约会日记贴上标签，后面要把标签找回来 |
| 9‑10 | 按右端点排序 | 把约会按结束时间排队，先结束的先考虑 |
| 14‑19| 二分找 `prev[i]` | 在已排好的队伍里快速定位「最近的、结束时间早于当前约会开始时间」的那个人 |
| 23‑26| 初始化 DP 表（k=0） | 选 0 条时，得分 0，索引列表为空 |
| 30‑42| DP 主循环 | 对每个「可选数量」和「当前考虑的区间」进行状态转移 |
| 35‑37| 计算「选当前区间」的得分和索引列表 | 把当前约会的权重加到「前一个不冲突」的最优上 |
| 39‑44| 取最大并在相等时比较字典序 | 好像在挑选「更高分」的方案，若分数相同则挑「字典序更小」的方案 |
| 48‑55| 从 `dp[1..4][n]` 中找全局最优 | 最终答案可能是选了 1、2、3 或 4 条，统一比较 |

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`  
  - 二分预处理 `O(n log n)`（每个区间一次二分）  
  - DP 主循环 `O(4·n) = O(n)`  
  综合下来仍是 `O(n log n)`，在 `n ≤ 5·10⁴` 时几毫秒即可完成。

- **空间复杂度**：`O(n)`  
  - `prev`、排序后的数组各占 `O(n)`  
  - DP 表保存 `5·(n+1)` 个二元组，整体也是线性空间。  
  相比暴力的指数空间，这已经是可以接受的。

---

## 心得

- **核心技巧**：**先排序 + 二分 + 动态规划**。  
  通过把区间按右端点排序，把「找前一个不冲突的区间」转化为二分查找，随后用 DP 记录「选了多少条」的最优解。

- **适用的题型**  
  1. **“最多 K 条不重叠区间”**（如 LeetCode 1235、1326）  
  2. **“带权区间调度”**（如 经典的 Weighted Interval Scheduling）  
  3. **“选若干不冲突任务以最大化收益”**（如工作安排、会议室调度等）

- **一句话总结**：**把区间按结束时间排好，用二分快速定位前一个可兼容区间，再用 DP 按选的数量累加权重，最后在同分数下挑字典序最小的组合。**

---

## 反思

- **第一反应**：看到“最多 4 条不重叠区间”，立刻想到「枚举」或「回溯」——因为 4 这个数字很小，似乎可以直接遍历所有组合。  
- **最容易踩的坑**  
  1. **区间的重叠定义**：左端点相等或右端点相等也算重叠，二分时必须使用严格小于 (`<`) 而不是 `≤`。  
  2. **字典序比较**：仅比较分数不足以得到唯一答案，需要在分数相等时手动比较索引列表的字典序。  
  3. **下标映射**：在 `prev` 为 `-1` 时，需要把它映射到 DP 表的第 `0` 行，否则会越界。  
  4. **保持索引升序**：在 DP 里把新加入的原始下标直接 `append`，因为我们遍历的顺序已经是原始下标的升序，保证最终列表自然有序。

- **下次遇到同类题**：  
  1. **先检查是否可以排序**（通常右端点排序是关键）。  
  2. **寻找“前一个可兼容状态”**，若能用二分或指针实现，就可以把状态转移从 `O(n)` 降到 `O(log n)`。  
  3. **确定 DP 维度**：这里是「选了多少条」+「处理到哪条」，类似的思路可以迁移到「最多 K 条」或「最多 K 次切割」等问题。