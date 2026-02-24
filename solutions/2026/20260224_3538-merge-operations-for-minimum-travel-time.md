# #3538. 合并操作以最小化行驶时间 / Merge Operations for Minimum Travel Time

> 难度：困难 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/merge-operations-for-minimum-travel-time/)

---

## 题目（英文原版）

**Description**

You are given a straight road of length l km, an integer n, an integer k, and two integer arrays, position and time, each of length n.
The array position lists the positions (in km) of signs in strictly increasing order (with position[0] = 0 and position[n - 1] = l).
Each time[i] represents the time (in minutes) required to travel 1 km between position[i] and position[i + 1].
You must perform exactly k merge operations. In one merge, you can choose any two adjacent signs at indices i and i + 1 (with i > 0 and i + 1 < n) and:
Return the minimum total travel time (in minutes) to travel from 0 to l after exactly k merges.

**Examples**

**Example 1:**

```
Input: l = 10, n = 4, k = 1, position = [0,3,8,10], time = [5,8,3,6]
Output: 62
Explanation:
Merge the signs at indices 1 and 2. Remove the sign at index 1, and change the time at index 2 to 8 + 3 = 11 .
```

**Example 2:**

```
Input: l = 5, n = 5, k = 1, position = [0,1,2,3,5], time = [8,3,9,3,3]
Output: 34
Explanation:
```

**Constraints**

- 1 <= l <= 105
- 2 <= n <= min(l + 1, 50)
- 0 <= k <= min(n - 2, 10)
- position.length == n
- position[0] = 0 and position[n - 1] = l
- position is sorted in strictly increasing order.
- time.length == n
- 1 <= time[i] <= 100​
- 1 <= sum(time) <= 100​​​​​​

---

## 题目（中文翻译）

**题目描述**  
给定一条长度为 `l` 公里的直线道路，一个整数 `n`，一个整数 `k`，以及两个长度均为 `n` 的整数数组 `position` 和 `time`。  

- 数组 `position` 按严格递增顺序列出路标的位置（单位：km），其中 `position[0] = 0` 且 `position[n - 1] = l`。  
- 每个 `time[i]` 表示在 `position[i]` 与 `position[i + 1]` 之间每公里所需的时间（单位：分钟）。  

你必须恰好执行 `k` 次合并操作。一次合并，你可以选择任意两个相邻的路标，索引为 `i` 和 `i + 1`（`i > 0` 且 `i + 1 < n`），然后：

1. 删除索引 `i` 处的路标。  
2. 将索引 `i + 1` 处的 `time` 更新为 `time[i] + time[i + 1]`。  

返回恰好进行 `k` 次合并后，从 `0` 行驶到 `l` 的最小总时间（单位：分钟）。

---

### 示例

**示例 1**  
```
Input: l = 10, n = 4, k = 1, position = [0,3,8,10], time = [5,8,3,6]
Output: 62
Explanation:
合并索引为 1 和 2 的路标。删除索引 1 的路标，并将索引 2 的 time 更新为 8 + 3 = 11。
```

**示例 2**  
```
Input: l = 5, n = 5, k = 1, position = [0,1,2,3,5], time = [8,3,9,3,3]
Output: 34
Explanation:
（此示例的具体合并过程与结果如上所示）
```

---

### 约束条件

- `1 <= l <= 10^5`
- `2 <= n <= min(l + 1, 50)`
- `0 <= k <= min(n - 2, 10)`
- `position.length == n`
- `position[0] = 0` 且 `position[n - 1] = l`
- `position` 按严格递增顺序排序
- `time.length == n`
- `1 <= time[i] <= 100`
- `1 <= sum(time) <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**要合并（也就是删除）的 `k` 个相邻标志位。  
- 先把所有可以删除的下标（`1 … n‑2`，因为第 0、`n‑1` 位置不能删）列出来；
- 从中挑出恰好 `k` 个下标的所有组合（相当于在一副牌里抽 `k` 张），每一种组合对应一次**具体的合并方案**；
- 按照这个方案把相邻的标志位合并：相邻的若被合并，则它们之间的时间系数 `time` 相加，形成一个更长的路段；
- 最后遍历得到的每段路程，算 `长度 × 时间系数` 的和，取最小值。

> **类比**：把标志位想成一本书的章节目录，`time[i]` 是第 `i` 章节的阅读速度。暴力做法就是把 **任意 `k` 个相邻章节合并**，算出整本书的总阅读时间，挑出最省时的合并方式。

**为什么能得到正确答案**  
因为我们把 **所有可能的合并方式** 都遍历了一遍，答案必然在其中。只要计算过程没有错误，最小的总时间就是题目要求的答案。

**复杂度分析（大白话）**  

- 组合数 `C(n‑2, k)`：从 `n‑2`（最多 48）个位置挑 `k`（最多 10）个。即使最坏的 `C(48,10) ≈ 3.2e9`，也远远超出可接受范围。  
- 对每一种组合我们要遍历一次所有路段（`O(n)`）来累加时间。  

所以整体时间是 **指数级**（指数增长），在实际测试里会 **超时**。  
空间上只需要保存原数组和临时的合并结果，`O(n)`。

#### 代码（Python）

```python
import itertools
from math import inf

def brute_merge(l, n, k, position, time):
    # 前缀和，方便后面快速算区间时间系数之和
    pref_time = [0] * (n + 1)
    for i in range(n):
        pref_time[i + 1] = pref_time[i] + time[i]

    best = inf                     # 当前找到的最小时间
    # 可删除的下标（不能删 0 与 n-1）
    deletable = list(range(1, n - 1))

    # 枚举所有恰好 k 个下标的组合
    for del_idx in itertools.combinations(deletable, k):
        del_set = set(del_idx)     # 为了 O(1) 判断是否被删

        total = 0
        last_keep = 0              # 上一次保留下来的标志位下标
        i = 1
        while i < n:
            if i in del_set:       # 需要合并，直接跳到下一个
                i += 1
                continue

            # i 是下一个被保留下来的标志位
            length = position[i] - position[last_keep]
            # 这段路的时间系数是 time[last_keep] … time[i-1] 的和
            t_sum = pref_time[i] - pref_time[last_keep]
            total += length * t_sum

            last_keep = i
            i += 1

        best = min(best, total)

    return best
```

> 代码里每一行都有中文注释，直接跑即可。只要 `n`、`k` 很小，这个暴力解能得到正确答案，帮助我们验证后面的动态规划实现是否正确。

#### 复杂度

- **时间复杂度**：`O( C(n‑2, k) * n )`  
  大白话：先从 `n‑2`（最多 48）个位置里挑 `k`（最多 10）个，组合数会非常大，随后每种组合再遍历一次所有路段（最多 50）。因此整体是 **指数级**，实际会超时。
- **空间复杂度**：`O(n)`  
  只用了原数组和前缀和，和输入规模成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**合并的本质**是把若干相邻的标志位“打包”，形成一个更长的路段。  
每个打包后的路段只需要两件信息：

1. **左端点的下标**（即该段的起点是哪个原始标志位）  
2. **右端点的下标**（该段的终点是哪个原始标志位）

一旦左、右端点确定，**该段的费用**可以直接算出：

```
长度 = position[right] - position[left]
时间系数之和 = sum(time[left … right-1])
费用 = 长度 * 时间系数之和
```

于是问题可以转化为：

> 在原序列中挑选 `n‑k`（包括首尾）个下标作为 **保留点**，使相邻保留点之间的费用和最小。

这正是典型的**区间划分 + 动态规划**。  
我们用 **前缀和** 来快速求出任意区间的 `time` 累加和，随后用 DP 枚举左端点、右端点的配对。

---

##### DP 状态  

`dp[i][c]`：**走到第 `i` 个标志位（必须保留），并且已经保留了 `c` 个标志位**（包括第 `i`）时的最小总费用。

- `i` 范围：`0 … n-1`  
- `c` 范围：`1 … n‑k`（因为最终要保留 `n‑k` 个）

##### 初始化  

- `dp[0][1] = 0`：起点在 0，已经保留 1 个标志位，费用为 0。  
- 其它状态先设为 **正无穷**（`inf`），表示不可达。

##### 转移  

设上一个保留下来的标志位是 `p`（`p < i`），此时已经保留了 `c‑1` 个标志位。  
把 `p` 与 `i` 之间的所有标志位全部合并（即删除），形成一个新路段。

```
segment_cost = (position[i] - position[p]) * (pref_time[i] - pref_time[p])
dp[i][c] = min( dp[i][c],
                dp[p][c-1] + segment_cost )
```

其中  

- `pref_time[t] = sum_{x=0}^{t-1} time[x]`（前缀和），用来 **O(1)** 求区间 `time` 之和。  
- `segment_cost` 正是该段的旅行时间。

##### 最终答案  

`dp[n-1][n-k]` —— 必须保留最后一个标志位（下标 `n-1`），且总共保留 `n‑k` 个标志位。

##### 为什么快  

- 外层循环遍历 `i`（`O(n)`），  
- 内层遍历可能的前驱 `p`（最坏 `O(n)`），  
- 再遍历保留数量 `c`（最多 `n‑k ≤ n`），  
- 总体时间 `O(n³)`，在本题的限制下（`n ≤ 50`）约 `125,000` 次运算，**毫秒级**即可完成。  
- 空间只需要 `dp` 表（`n × (n‑k+1)`）和前缀和，**`O(n²)`**，也很小。

> **类比**：把标志位想成城市，合并相当于在城市之间建一条**直达高速**。我们要在所有城市中挑出若干“停靠站”，让每段高速的“路程 × 速度”之和最小。DP 就像在地图上一步步画出最短的“站点序列”。

---

#### 代码（Python）

```python
from math import inf

def min_travel_time(l, n, k, position, time):
    """
    动态规划求解最小旅行时间
    参数含义与题目一致
    """
    # ---------- 前缀和，帮助 O(1) 取区间时间系数之和 ----------
    pref_time = [0] * (n + 1)          # pref_time[i] = sum(time[0..i-1])
    for i in range(n):
        pref_time[i + 1] = pref_time[i] + time[i]

    keep_cnt = n - k                    # 最终需要保留的标志位数量
    # dp[i][c]：到达 i 并保留了 c 个标志位时的最小费用
    dp = [[inf] * (keep_cnt + 1) for _ in range(n)]
    dp[0][1] = 0                        # 起点

    # ---------- 动态规划主循环 ----------
    for i in range(1, n):               # 当前保留下来的标志位
        for c in range(2, keep_cnt + 1):   # 必须保留至少两个（包括起点）
            # 枚举上一个保留下来的标志位 p
            best = inf
            for p in range(i):              # p < i
                if dp[p][c - 1] == inf:
                    continue                # 之前不可达，跳过
                # 计算 p -> i 这段合并后的费用
                length = position[i] - position[p]
                time_sum = pref_time[i] - pref_time[p]   # sum(time[p .. i-1])
                seg_cost = length * time_sum
                cand = dp[p][c - 1] + seg_cost
                if cand < best:
                    best = cand
            dp[i][c] = best

    # 必须以最后一个标志位结束，且保留 exactly keep_cnt 个
    return dp[n - 1][keep_cnt]
```

> - 每一行都写了中文注释，帮助理解每一步的意义。  
> - 代码只依赖标准库，直接复制粘贴即可运行。  

#### 复杂度

- **时间复杂度**：`O(n³)`  
  大白话：我们把所有标志位 (`n ≤ 50`) 两两配对，再遍历一次可能的保留数量，总共不超过 `50³ = 125,000` 次基本运算，跑得非常快。相比暴力的指数级，这已经是 **线性多项式**，在实际中几乎是瞬间完成。

- **空间复杂度**：`O(n²)`  
  需要存 `dp` 表（`n × (n‑k+1) ≤ 50 × 50`）和前缀和，都是和输入规模线性相关，几乎可以忽略不计。

---

## 心得

- **核心技巧**：把“合并相邻标志位”抽象为**区间划分**，然后用**动态规划**在所有可能的左端点、右端点配对中求最小费用。  
- **适用场景**：  
  1. **分段函数最小化**（如把数组划分为若干段，每段代价由端点决定）。  
  2. **路径压缩类问题**（如把若干连续道路合并，费用为长度×系数）。  
  3. **“保留若干元素”类 DP**（如保留 `m` 个石子、站点等，使相邻代价最小）。  
- **一句话总结解题钥匙**：**“把合并视为在原序列上挑选保留点，转化为区间代价的最小划分，用 DP 枚举前驱点”**。

---

## 反思

- **第一反应**：看到“合并相邻标志位”，马上想到“枚举所有合并方式”。这是一种**暴力思考**，对小数据能验证思路，却忽视了指数级组合的爆炸。  
- **最容易踩的坑**  
  1. **忽略首尾必须保留**：若把首尾也当作可删除，会产生非法的区间长度计算。  
  2. **时间系数的求法错误**：合并后该段的时间系数是 **被合并的所有 `time` 之和**，不是平均或最大。使用前缀和可以避免手动循环出错。  
  3. **边界条件**：`k = 0`（不合并）时答案应等于原始总时间；`k = n-2`（只保留首尾）时只剩一段，需要确保 DP 能覆盖 `c = 2` 的情况。  
- **下次遇到同类题的第一步**：先**写出“保留点”模型**，确认每段费用的公式，然后决定是用**枚举+前缀和**（小规模）还是**DP**（规模稍大）来求最小总费用。这样可以迅速摆脱暴力思维的束缚，直奔最优解。