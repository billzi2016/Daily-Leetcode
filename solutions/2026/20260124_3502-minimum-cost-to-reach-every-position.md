# #3502. 到达每个位置的最小费用 / Minimum Cost to Reach Every Position

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-reach-every-position/)

---

## 题目（英文原版）

**Description**

You are given an integer array cost of size n. You are currently at position n (at the end of the line) in a line of n + 1 people (numbered from 0 to n).
You wish to move forward in the line, but each person in front of you charges a specific amount to swap places. The cost to swap with person i is given by cost[i].
You are allowed to swap places with people as follows:
Return an array answer of size n, where answer[i] is the minimum total cost to reach each position i in the line.

**Examples**

**Example 1:**

```
Input: cost = [5,3,4,1,3,2]
Output: [5,3,3,1,1,1]
Explanation:
We can get to each position in the following way:
```

**Example 2:**

```
Input: cost = [1,2,4,6,7]
Output: [1,1,1,1,1]
Explanation:
We can swap with person 0 for a cost of 1, then we will be able to reach any position i for free.
```

**Constraints**

- 1 <= n == cost.length <= 100
- 1 <= cost[i] <= 100

---

## 题目（中文翻译）

你得到一个长度为 `n` 的整数数组 `cost`。在一条由 `n + 1` 个人组成的队列中（编号从 `0` 到 `n`），你最初站在位置 `n`（即队列的末尾）。  
你希望向前移动到队列中的其他位置，但队列前面的每个人都会收取一定费用来与你交换位置。与编号为 `i` 的人交换位置的费用为 `cost[i]`。

你可以按以下方式与前面的人交换位置：

（题目原文中此处应给出具体的交换规则，保持原样）

返回一个长度为 `n` 的数组 `answer`，其中 `answer[i]` 表示达到队列中位置 `i` 所需的最小总费用。

**示例 1**  
**输入**: `cost = [5,3,4,1,3,2]`  
**输出**: `[5,3,3,1,1,1]`  
**解释**:  
我们可以通过如下方式到达每个位置：

**示例 2**  
**输入**: `cost = [1,2,4,6,7]`  
**输出**: `[1,1,1,1,1]`  
**解释**:  
我们先以费用 `1` 与编号 `0` 的人交换位置，此后即可免费到达任意位置 `i`。

**约束条件**  
- `1 <= n == cost.length <= 100`  
- `1 <= cost[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

- **题目再说一遍**：我们站在队伍的最后（下标 `n`），想要搬到前面的任意位置 `i`（`0 ≤ i < n`）。  
  与下标为 `i` 的人换位要付 `cost[i]` 元。  
  关键是：**只要先换到一个费用更低的人的位置，之后再往前换位就不需要再付钱**（因为已经“买到了”更低的费用）。

- **最直接的想法**：对每一个目标位置 `i`，把所有可能先换到的前面位置 `j (0 ≤ j ≤ i)` 都枚举一遍，取其中费用最小的那个。  
  也就是说  
  `answer[i] = min(cost[0], cost[1], … , cost[i])`  
  只不过我们不提前知道要怎么算最小值，于是把这个最小过程写成两层循环：

  1. 外层遍历每个目标 `i`（共 `n` 次）。
  2. 内层在 `[0, i]` 区间里找最小的 `cost`（最坏要遍历 `i+1` 次）。

- **为什么它是对的**：  
  - 对于位置 `i`，如果我们直接和 `i` 换位，花 `cost[i]`。  
  - 如果我们先和更前面的 `j`（`j < i`）换位，只要 `cost[j] ≤ cost[i]`，后面再往前走就可以免费。  
  - 所以在 `[0, i]` 中找最小的 `cost` 就一定是到达 `i` 的最小总费用。

- **复杂度大白话**：  
  - **时间**：外层 `n` 次，内层最多 `n` 次（当 `i = n‑1` 时要遍历 `n` 个数），于是总共大约要做 `n × n / 2` 次比较，记作 **O(n²)**。  
    “O(n²)” 可以想象成 **一个正方形的格子**，如果 `n = 100`，大约要检查 10,000 次。  
  - **空间**：只用了一个长度为 `n` 的答案数组和几个临时变量，**O(n)**，即随输入大小线性增长的空间。

#### 代码（Python）

```python
from typing import List

def minCostBrute(cost: List[int]) -> List[int]:
    n = len(cost)                # 队伍里前面的人有 n 个
    answer = [0] * n             # 用来存放每个位置的最小费用

    # 外层：枚举每一个想要到达的位置 i
    for i in range(n):
        cur_min = float('inf')   # 先设一个很大的数，后面会不断取更小的

        # 内层：在区间 [0, i] 里找最小的 cost
        for j in range(i + 1):
            if cost[j] < cur_min:
                cur_min = cost[j]   # 更新当前找到的最小费用

        answer[i] = cur_min      # i 位置的答案就是区间最小值

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要两层循环，外层 `n` 次，内层最多 `n` 次。  
  想象成在一个 `n × n` 的棋盘上检查每一个格子。
- **空间复杂度**：`O(n)` — 只用了长度为 `n` 的 `answer` 数组，其他都是常数级别的临时变量。

---

### 2. 最优解

#### 思路  

- **慢在哪儿**：暴力解的瓶颈在于每次都要重新遍历 `[0, i]` 找最小值，导致 **重复劳动**。  
  实际上，当我们已经算出了 `answer[i‑1]`（即 `cost[0..i‑1]` 的最小值），再算 `answer[i]` 只需要把 `cost[i]` 和之前的最小值比较一下，就可以得到新的最小值。  
  这就是“**前缀最小**”的思想。

- **一步步推导**  
  1. **定义**：`pre_min[i]` 表示 `cost[0..i]` 中的最小值。  
  2. **递推公式**：`pre_min[i] = min(pre_min[i‑1], cost[i])`。  
     - 当我们已经知道了前面 `i‑1` 个数的最小值 `pre_min[i‑1]`，只要再把第 `i` 个数拿来比较，就能得到新的最小值。  
  3. **答案**：因为 `answer[i]` 正好等于 `pre_min[i]`，所以只要在一次遍历中维护这个前缀最小，就能直接写入答案。

- **核心数据结构**：**前缀最小数组**（其实可以不额外开数组，直接在答案数组里滚动更新）。  
  前缀最小就像 **一本日记本**，每天记录到目前为止的最低温度，只要记住最近的最低值，后面每天只需要和今天的温度比一次，就能得到新的最低温度。

- **实现细节**：  
  - 初始化 `cur_min` 为一个很大的数（或直接把 `cost[0]` 赋给 `answer[0]`）。  
  - 从左到右遍历 `cost`，每一步 `cur_min = min(cur_min, cost[i])`，然后把 `cur_min` 写入 `answer[i]`。  
  - 只需要 **O(1)** 的额外空间（除了返回的答案数组），时间是 **O(n)**。

#### 代码（Python）

```python
from typing import List

def minCostOptimal(cost: List[int]) -> List[int]:
    n = len(cost)
    answer = [0] * n          # 用来直接存放前缀最小

    cur_min = float('inf')    # 当前看到的最小费用，初始设为无穷大

    for i in range(n):
        # 与当前元素比较，保留更小的那个
        if cost[i] < cur_min:
            cur_min = cost[i]   # 更新前缀最小

        answer[i] = cur_min      # 直接把前缀最小写进答案

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，每个元素做常数次比较。  
  与暴力的 `O(n²)` 相比，**快了大约 `n` 倍**（比如 `n=100` 时，从 10,000 次降到 100 次）。
- **空间复杂度**：`O(n)` — 只需要返回的答案数组。额外的临时变量 `cur_min` 是 **O(1)** 的。

---

## 心得

- **核心技巧**：**前缀最小（前缀最小值）**。  
  当问题要求“区间 `[0, i]` 的最小/最大/和”等，往往可以用一次遍历维护一个滚动的状态，避免重复遍历。
- **适用的题型**  
  1. “Running Minimum/Maximum” 系列，如 LeetCode 1446 *Consecutive Characters*（需要前缀计数）。  
  2. “区间最小值查询” 的简化版，如 “Maximum Subarray Sum After One Deletion”。  
  3. “前缀和” 类问题，如 “Running Sum of 1d Array”。
- **一句话总结**：**只要把“已经算好的信息”保留下来，后面的计算就可以一步到位**。

---

## 反思

- **第一反应**：看到“每个人都有费用，想要最小费用到达每个位置”，立刻想到 “在前面找费用最小的那个人”。  
- **最容易踩的坑**  
  - **忘记“前缀”概念**：直接对每个 `i` 再遍历会导致 `O(n²)` 超时。  
  - **边界条件**：`cost` 只有一个元素时，答案就是它本身。  
  - **初始化**：如果把 `cur_min` 初始化为 `0`，会把所有答案错误地变成 `0`，所以要用无穷大或直接用 `cost[0]` 初始化。
- **下次遇到同类题**：第一步先问自己“答案是否只和前面某个最优值有关”，如果答案是“是”，就立刻考虑维护**前缀最小/最大/和**，把时间复杂度从平方降到线性。