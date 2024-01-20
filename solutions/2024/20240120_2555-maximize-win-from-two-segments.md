# #2555. 最大化两段获奖数量 / Maximize Win From Two Segments

> 难度：中等 · 标签：Array、Binary Search、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximize-win-from-two-segments/)

---

## 题目（英文原版）

**Description**

There are some prizes on the X-axis. You are given an integer array prizePositions that is sorted in non-decreasing order, where prizePositions[i] is the position of the ith prize. There could be different prizes at the same position on the line. You are also given an integer k.
You are allowed to select two segments with integer endpoints. The length of each segment must be k. You will collect all prizes whose position falls within at least one of the two selected segments (including the endpoints of the segments). The two selected segments may intersect.
Return the maximum number of prizes you can win if you choose the two segments optimally.

**Examples**

**Example 1:**

```
Input: prizePositions = [1,1,2,2,3,3,5], k = 2
Output: 7
Explanation: In this example, you can win all 7 prizes by selecting two segments [1, 3] and [3, 5].
```

**Example 2:**

```
Input: prizePositions = [1,2,3,4], k = 0
Output: 2
Explanation: For this example, one choice for the segments is [3, 3] and [4, 4], and you will be able to get 2 prizes.
```

**Constraints**

- 1 <= prizePositions.length <= 105
- 1 <= prizePositions[i] <= 109
- 0 <= k <= 109
- prizePositions is sorted in non-decreasing order.

---

## 题目（中文翻译）

有若干奖品分布在 X 轴上。给定一个按非递减顺序排序的整数数组 `prizePositions`，其中 `prizePositions[i]` 表示第 i 个奖品的位置。同一位置上可能会有多个奖品。另给定一个整数 `k`。

你可以选择 **两个段（segments）**，每个段的端点必须为整数。每个段的 **长度（length）** 必须恰好为 `k`。你将收集所有位于至少一个所选段内的奖品（包括段的端点）。这两个段可以相交。

返回在最优选择两段的情况下，你能够获得的 **奖品（prizes）** 的最大数量。

## 示例

### 示例 1
**输入**：`prizePositions = [1,1,2,2,3,3,5]`, `k = 2`  
**输出**：`7`  
**解释**：在此示例中，选择段 `[1, 3]` 和 `[3, 5]` 即可赢得全部 7 个奖品。

### 示例 2
**输入**：`prizePositions = [1,2,3,4]`, `k = 0`  
**输出**：`2`  
**解释**：一种可行的选择是段 `[3, 3]` 和 `[4, 4]`，此时可以获得 2 个奖品。

## 约束条件
- `1 <= prizePositions.length <= 10^5`
- `1 <= prizePositions[i] <= 10^9`
- `0 <= k <= 10^9`
- `prizePositions` 已按非递减顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的两段区间** 都枚举一遍，算出每个组合能覆盖多少奖品，取最大值。

- **区间的表示**：区间长度固定为 `k`，所以只要确定左端点 `L`，右端点自然是 `L + k`。  
- **统计区间内奖品数量**：遍历奖品数组 `prizePositions`，判断每个奖品的位置 `p` 是否满足 `L ≤ p ≤ L + k`。这一步可以想象成“在一本字典里查词”，我们把每个奖品的位置当作要查的词，看它是否落在当前区间这页里。  
- **两段区间的组合**：外层循环枚举第一段左端点 `L1`，内层循环枚举第二段左端点 `L2`，分别统计它们覆盖的奖品数，然后把两段的奖品集合取并集（即去掉重复计数），得到总数。

> 为什么这种方法一定能得到正确答案？  
> 因为我们把 **所有合法的左端点**（从最左边的奖品位置到最右边的奖品位置）都尝试了一遍，必然会包含最优的那两个左端点组合。

**时间/空间复杂度的“大白话”**  
- 时间复杂度 `O(n³)`（n 为奖品数量）：  
  - 第一个 `for` 循环遍历所有可能的 `L1`（≈ n 次）  
  - 第二个 `for` 循环遍历所有可能的 `L2`（≈ n 次）  
  - 第三层遍历奖品数组统计是否在区间内（≈ n 次）  
  - 三层循环相乘，就是 `n × n × n`，如果 `n = 10⁵`，这根本不可能在合理时间内跑完。  
- 空间复杂度 `O(1)`：只用了常数个额外变量。

#### 代码（Python）

```python
from typing import List

def maxPrize_bruteforce(prizePositions: List[int], k: int) -> int:
    n = len(prizePositions)
    # 所有可能的左端点（只取出现过的奖品位置，足够了）
    candidates = prizePositions

    best = 0
    for i in range(n):                     # 第一个区间的左端点
        L1 = candidates[i]
        R1 = L1 + k
        # 统计第一个区间覆盖的奖品下标集合（用 set 去重）
        set1 = {idx for idx, p in enumerate(prizePositions) if L1 <= p <= R1}

        for j in range(n):                 # 第二个区间的左端点
            L2 = candidates[j]
            R2 = L2 + k
            set2 = {idx for idx, p in enumerate(prizePositions) if L2 <= p <= R2}
            # 并集的大小即为两段区间能收集的奖品数
            total = len(set1 | set2)       # “|” 是集合的并集
            best = max(best, total)

    return best
```

> 代码里每一行都加了中文注释，帮助你一步步对照思路。

#### 复杂度

- **时间复杂度**：`O(n³)` — 想象成“三层循环”，每层都要遍历全部奖品，所以跑得非常慢。  
- **空间复杂度**：`O(1)`（不计输入数组本身）——只用了几个临时集合，规模不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历奖品数组来统计区间内的奖品数**。如果我们能够 **一次性算出所有左端点对应的区间内奖品数量**，后面的组合就可以在 `O(1)` 时间内完成。

**核心技巧**  
1. **滑动窗口（Two‑Pointer）**：因为 `prizePositions` 已经排好序，只要左端点向右移动，右端点也只会向右不回退。我们用两个指针 `left`、`right`，保持窗口 `[prizePositions[left], prizePositions[left] + k]` 包含的奖品数 `win[left]`。  
   - 类比：想象你在看一条路，两根手指分别指在路的起点和终点，终点只能往前走，起点往前走时，手指之间的车辆数就是窗口内的奖品数。  
2. **前缀最大（Prefix Max）**：`win[i]` 表示以 `prizePositions[i]` 为左端点的区间能收集的奖品数。若我们想在 **左侧** 选一个区间，右侧再选一个区间，只需要知道左侧 **截至 i‑1** 的最佳区间有多少奖品。于是构造 `preMax[i] = max(win[0..i])`。  
   - 类比：你在跑步，每跑到第 `i` 步，就记录到目前为止跑得最远的距离，这个记录帮助你快速回答“之前跑过的最远距离是多少”。  
3. **合并两段**：遍历所有可能的左端点 `i`（作为**第二段**的左端点），答案可以是 `win[i] + preMax[i-1]`（如果 `i>0`），即“左边的最佳区间 + 以 `i` 为左端点的区间”。因为两个区间可以相交，**最优解一定可以在不相交的情况下取得**（相交只会导致重复计数而没有额外收益），所以这种划分不会错过最优答案。

**算法步骤**  

| 步骤 | 说明 |
|------|------|
| 1️⃣ 计算 `win[i]` | 使用滑动窗口，一次遍历得到每个左端点对应的奖品数量，时间 `O(n)`。 |
| 2️⃣ 计算前缀最大 `preMax` | 线性遍历 `win`，记录截至每个位置的最大值，时间 `O(n)`。 |
| 3️⃣ 求最终答案 | 再遍历一次 `win`，对每个 `i` 计算 `win[i] + preMax[i-1]`（或只取 `win[i]` 当只有一段时），取最大值。时间 `O(n)`。 |
| 总时间 | `O(n)`（只用了几次线性遍历）。 |
| 总空间 | `O(n)` 用来存 `win` 与 `preMax`（可以把 `preMax` 合并到 `win` 中进一步压缩到 `O(n)`）。 |

#### 代码（Python）

```python
from typing import List

def maxPrize(prizePositions: List[int], k: int) -> int:
    n = len(prizePositions)

    # 1️⃣ win[i] = 区间 [prizePositions[i], prizePositions[i] + k] 能收集的奖品数
    win = [0] * n
    right = 0                     # 窗口右指针
    for left in range(n):
        # 把 right 指针尽量往右推，使窗口仍然合法
        while right < n and prizePositions[right] - prizePositions[left] <= k:
            right += 1
        # 此时 [left, right) 中的奖品全在窗口内，数量就是 right - left
        win[left] = right - left

    # 2️⃣ preMax[i] = max(win[0..i])，这里直接复用 win 数组来存前缀最大
    preMax = [0] * n
    preMax[0] = win[0]
    for i in range(1, n):
        # 取前面最大的 + 当前的，保留最大值
        preMax[i] = max(preMax[i - 1], win[i])

    # 3️⃣ 合并两段区间，求最大可能的奖品数量
    ans = 0
    for i in range(n):
        # 以 i 为左端点的区间作为“第二段”
        second = win[i]
        # “第一段”必须在 i 左侧（不相交），所以取 preMax[i-1]（i>0 时）
        first = preMax[i - 1] if i > 0 else 0
        ans = max(ans, first + second)

    return ans
```

**代码要点**  

- `while` 循环实现滑动窗口，`right` 只会单调递增，整体是线性时间。  
- `win[left] = right - left` 直接给出窗口内奖品的数量（因为数组已经排序，窗口内部的元素个数就是下标差）。  
- `preMax` 用来快速获取左侧最优区间的奖品数，避免每次都遍历。  
- 最后遍历一次 `win`，把“左侧最佳 + 当前区间”做加法，取最大即为答案。

#### 复杂度

- **时间复杂度**：`O(n)` — 只用了三次线性遍历，`n` 最多是 `10⁵`，在 1 秒内轻松跑完。  
  - 大白话：想象你只需要一次“走路”把所有奖品位置走遍，每走一步都顺手记点，根本不需要回头。  
- **空间复杂度**：`O(n)` – 需要两个长度为 `n` 的数组 `win`、`preMax`（如果想进一步节省，可以把 `preMax` 写回 `win`，仍然是 `O(n)`）。  

---

## 心得

- **核心技巧**：**滑动窗口 + 前缀最大**。滑动窗口把“统计区间内元素个数”从 `O(n²)` 降到 `O(n)`；前缀最大把“在左侧挑选最佳区间”从 `O(n²)` 降到 `O(1)` 查询。  
- **适用的题型**（类似思路）  
  1. *最多的子数组/子序列长度*（如 LeetCode 3. 无重复字符的最长子串）  
  2. *两个不相交子数组的最大和*（如 “Maximum Sum of Two Non‑Overlapping Subarrays”）  
  3. *在固定长度窗口内的最大/最小值*（如 “Sliding Window Maximum”）  
- **一句话总结解题钥匙**：**把所有“区间统计”一次算完，再用前缀/后缀信息快速拼出两段的最佳组合**。

---

## 反思

- **第一反应**：看到“两个长度为 `k` 的区间”，自然想到枚举所有左端点组合，直接写暴力三层循环。  
- **最容易踩的坑**  
  - **重复计数**：如果两个区间相交，直接把两段的奖品数相加会把交叉部分算两次。实际上，最优解可以在不相交的情况下取得，记得利用这一点。  
  - **窗口边界**：`right` 指针要指向第一个不满足 `prizePositions[right] - prizePositions[left] ≤ k` 的位置，窗口大小是 `right - left`。容易把 `≤` 与 `<` 搞混。  
  - **特殊情况**：`k = 0` 时每个区间只能覆盖同一位置的奖品；此时 `win[i]` 其实是该位置出现的次数，需要保证滑动窗口仍然正确统计。  
- **下次遇到同类题的第一步**：先 **确定单段区间的最优统计方式**（滑动窗口、前缀和、二分搜索等），再思考 **如何把两段（或多段）组合**，往往可以用前缀/后缀最大或动态规划把组合过程压到线性时间。