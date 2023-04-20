# #2212. 射箭比赛中的最大得分 / Maximum Points in an Archery Competition

> 难度：中等 · 标签：Array、Backtracking、Bit Manipulation、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-points-in-an-archery-competition/)

---

## 题目（英文原版）

**Description**

Alice and Bob are opponents in an archery competition. The competition has set the following rules:
You are given the integer numArrows and an integer array aliceArrows of size 12, which represents the number of arrows Alice shot on each scoring section from 0 to 11. Now, Bob wants to maximize the total number of points he can obtain.
Return the array bobArrows which represents the number of arrows Bob shot on each scoring section from 0 to 11. The sum of the values in bobArrows should equal numArrows.
If there are multiple ways for Bob to earn the maximum total points, return any one of them.

**Examples**

**Example 1:**

```
Input: numArrows = 9, aliceArrows = [1,1,0,1,0,0,2,1,0,1,2,0]
Output: [0,0,0,0,1,1,0,0,1,2,3,1]
Explanation: The table above shows how the competition is scored. 
Bob earns a total point of 4 + 5 + 8 + 9 + 10 + 11 = 47.
It can be shown that Bob cannot obtain a score higher than 47 points.
```

**Example 2:**

```
Input: numArrows = 3, aliceArrows = [0,0,1,0,0,0,0,0,0,0,0,2]
Output: [0,0,0,0,0,0,0,0,1,1,1,0]
Explanation: The table above shows how the competition is scored.
Bob earns a total point of 8 + 9 + 10 = 27.
It can be shown that Bob cannot obtain a score higher than 27 points.
```

**Constraints**

- 1 <= numArrows <= 105
- aliceArrows.length == bobArrows.length == 12
- 0 <= aliceArrows[i], bobArrows[i] <= numArrows
- sum(aliceArrows[i]) == numArrows

---

## 题目（中文翻译）

**题目描述**  
Alice 和 Bob 是射箭比赛的对手。比赛规则如下：

给定整数 `numArrows` 和长度为 12 的整数数组 `aliceArrows`，其中 `aliceArrows[i]` 表示 Alice 在得分区间 `i`（从 0 到 11）射中的箭的数量。  
Bob 希望在使用恰好 `numArrows` 支箭的前提下，使自己获得的总得分最大化。

返回长度为 12 的整数数组 `bobArrows`，其中 `bobArrows[i]` 表示 Bob 在得分区间 `i` 射中的箭的数量，且 `bobArrows` 中所有元素的和必须等于 `numArrows`。  
如果存在多种方式可以使 Bob 获得最大总得分，返回任意一种即可。

**示例**  

*示例 1*  
```text
Input: numArrows = 9, aliceArrows = [1,1,0,1,0,0,2,1,0,1,2,0]
Output: [0,0,0,0,1,1,0,0,1,2,3,1]
Explanation: 上表展示了比赛的计分方式。  
Bob 获得的总得分为 4 + 5 + 8 + 9 + 10 + 11 = 47。  
可以证明，Bob 不可能得到高于 47 分的成绩。
```

*示例 2*  
```text
Input: numArrows = 3, aliceArrows = [0,0,1,0,0,0,0,0,0,0,0,2]
Output: [0,0,0,0,0,0,0,0,1,1,1,0]
Explanation: 上表展示了比赛的计分方式。  
Bob 获得的总得分为 8 + 9 + 10 = 27。  
可以证明，Bob 不可能得到高于 27 分的成绩。
```

**约束条件**  

- `1 <= numArrows <= 10^5`  
- `aliceArrows.length == bobArrows.length == 12`  
- `0 <= aliceArrows[i], bobArrows[i] <= numArrows`  
- `sum(aliceArrows[i]) == numArrows`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出 12 个得分区间（从 0 分到 11 分），每个区间的得分等于它的下标。  
- **要想得到第 `i` 分**，Bob 必须在该区间投 **`aliceArrows[i] + 1`** 支箭，才能超过 Alice 的数量并占领该分数。  
- 只要 **投够了** 这条最小要求，后面再多投多少支都不影响这块分数的归属（多投的箭只会浪费）。

因为区间只有 12 个，**枚举** Bob 想要“赢”的区间集合是可行的。  
- 把每个区间看成一个“开关”，打开表示 Bob 决定要抢这个分数，关闭表示不抢。  
- 12 个开关的所有状态正好是 **2 的 12 次方 = 4096** 种（就像把 12 本书的《是否阅读》做二进制枚举），这在计算机里可以一次遍历完。

遍历每一种状态（用 **位运算** 把 12 位二进制数当作子集）时：

1. 计算 **需要的最少箭数**：对每个被选中的区间 `i` 加上 `aliceArrows[i] + 1`。  
2. 如果这总数 **不超过** `numArrows`，说明这套选区是可行的。  
3. 计算 **能得到的总分**：把所有被选中的区间下标相加（因为每个区间的得分就是它的下标）。  
4. 记录下得分最高的那套选区，同时把多余的箭全部放到第 0 区（或者任意一个不影响得分的区间），保证 `bobArrows` 的和恰好等于 `numArrows`。

这样就能得到“最大可能得分”。  
因为我们枚举的是所有可能的抢分组合，**一定不会漏掉最优解**。

**为什么会对**  
- 只要满足每个抢到的区间的最小要求，Bob 就一定可以得到该区间的分数。  
- 剩余的箭再投到任何不抢的区间都不会改变已经得到的分数。  

**复杂度**  
- 枚举 2<sup>12</sup> ≈ 4096 种子集。  
- 对每个子集遍历最多 12 个区间，做加法比较。  

时间复杂度大约是 **O(2^12 · 12) ≈ O(5 × 10³)**，在任何机器上都跑得飞快。  
空间只需要保存当前的 `bobArrows` 数组和若干临时变量，**O(12) = O(1)**（常数级）。

#### 代码（Python）

```python
from typing import List

def maximumBobArrows(numArrows: int, aliceArrows: List[int]) -> List[int]:
    n = 12                         # 只会有 12 个区间
    best_score = -1                # 记录最高分
    best_mask = 0                  # 记录对应的子集（用二进制掩码保存）

    # 0 ~ (1<<12)-1 表示所有可能的子集
    for mask in range(1 << n):
        need = 0       # 这套子集需要的最少箭数
        score = 0      # 能得到的总分

        for i in range(n):
            if mask >> i & 1:          # 第 i 位为 1，表示要抢第 i 分
                need += aliceArrows[i] + 1   # 必须比 Alice 多投 1 支
                score += i                    # 抢到 i 分

        # 如果需要的箭数超过了可用的，就直接丢弃这套方案
        if need > numArrows:
            continue

        # 记录更好的方案（如果得分相同，随便保存一个即可）
        if score > best_score:
            best_score = score
            best_mask = mask

    # 根据最佳子集构造答案数组
    bob = [0] * n
    arrows_used = 0
    for i in range(n):
        if best_mask >> i & 1:               # 这块要抢
            bob[i] = aliceArrows[i] + 1
            arrows_used += bob[i]

    # 把剩余的箭全部放到第 0 区（不会影响得分，因为第 0 分价值为 0）
    bob[0] += numArrows - arrows_used
    return bob


# ------------------- 下面是示例测试 -------------------
if __name__ == "__main__":
    # 示例 1
    numArrows = 9
    alice = [1,1,0,1,0,0,2,1,0,1,2,0]
    print(maximumBobArrows(numArrows, alice))
    # 示例 2
    numArrows = 3
    alice = [0,0,1,0,0,0,0,0,0,0,0,2]
    print(maximumBobArrows(numArrows, alice))
```

> **代码要点注释**  
> - `mask >> i & 1`：把 `mask` 右移 `i` 位后与 `1` 做与运算，判断第 `i` 位是否为 1（即是否要抢该分）。  
> - `aliceArrows[i] + 1`：要比 Alice 多投 1 支才能占领。  
> - 最后把剩余的箭塞到第 0 区，因为 0 分不影响总得分。

#### 复杂度

- **时间复杂度**：`O(2^12 * 12) ≈ O(5 × 10³)`。  
  - 2<sup>12</sup> 是所有子集的数量，12 是每次遍历区间的上限。  
  - 用大白话讲，就是**几千次**的循环，几乎可以在眨眼之间算完。

- **空间复杂度**：`O(1)`（常数级）。  
  - 只用了长度为 12 的数组和若干整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

在本题中，**暴力枚举已经是最优的**。  
- 由于区间数目固定为 12（极小），枚举所有子集的时间已经是常数级（≈ 4 k 次），不可能再进一步降低数量级。  
- 任何想要“更快”地搜索，都需要把搜索空间压缩到 **子集数 < 2<sup>12</sup>**，这只能在 **已知某些区间必然不取** 的情况下实现。但题目没有提供这类先验信息。

因此我们把 **暴力枚举 + 位运算** 视作**最优解**。  
下面的实现与上面的“直觉解”几乎相同，只是把关键步骤抽成函数，代码更简洁，且在记录答案时采用**贪心**把多余箭放到最低得分的区间（第 0 区），保证答案合法。

#### 代码（Python）

```python
from typing import List

def maximumBobArrows_opt(numArrows: int, aliceArrows: List[int]) -> List[int]:
    n = 12
    best_score = -1
    best_mask = 0

    # -------- 枚举所有子集 --------
    for mask in range(1 << n):
        need = 0
        score = 0
        # 计算该子集所需最少箭数和能得到的分数
        for i in range(n):
            if mask & (1 << i):
                need += aliceArrows[i] + 1
                score += i
        if need <= numArrows and score > best_score:
            best_score, best_mask = score, mask

    # -------- 根据最佳子集恢复 Bob 的出箭方案 --------
    bob = [0] * n
    used = 0
    for i in range(n):
        if best_mask & (1 << i):
            bob[i] = aliceArrows[i] + 1
            used += bob[i]

    # 剩余的箭全部放到第 0 区（得分为 0，不影响最优解）
    bob[0] += numArrows - used
    return bob
```

#### 复杂度

- **时间复杂度**：`O(2^12 * 12)`，与暴力解相同，已是理论下界。  
  - “最优”体现在 **不需要额外的递归、回溯或记忆化**，仅一次遍历即可完成。

- **空间复杂度**：`O(1)`，只用常数个额外变量。

---

## 心得

- **核心技巧**：**位运算枚举子集**（Subset Enumeration）+ **最小需求**（用 `aliceArrows[i] + 1` 表示抢分的最低箭数）。  
- 该技巧适用于 **区间/物品数量很小（≤20）**，需要在每个子集上做一次线性计算的题目。常见类似题目有：  
  1. LeetCode 1686 *Maximum Points in an Archery Competition*（本题）。  
  2. LeetCode 1985 *Find the Kth Smallest Sum of a Matrix With Sorted Rows*（行数 ≤ 12，使用子集/位运算）。  
  3. LeetCode 1631 *Path With Minimum Effort*（在状态压缩 DP 中也会用到子集枚举）。  

- **一句话总结**：  
  > “当可选项极少时，用二进制掩码枚举所有可能的组合，配合最小需求计算，即可在常数时间内找到全局最优。”

---

## 反思

- **第一反应**：看到“12 个区间”和“要比 Alice 多投 1 支才能得分”，立刻想到 **枚举哪些区间要抢**，因为 12 很小，穷举不会超时。  
- **最容易踩的坑**  
  1. **剩余箭的分配**：忘记把剩余的箭全部填满导致 `sum(bobArrows) != numArrows`。解决办法是把多余箭全部放到分值最小的区间（这里是第 0 区）。  
  2. **位运算细节**：写错 `mask >> i & 1` 与 `mask & (1 << i)` 的顺序，导致判断错误。  
  3. **边界情况**：如果 `numArrows` 正好等于所有必需最小箭数的和，剩余箭为 0，也要正确处理（即不再额外加箭）。  

- **下次遇到同类题**：  
  - **第一步**：先判断可选项的数量是否足够小（≤20），如果是，就立刻想到 **子集枚举 + 位掩码**。  
  - **第二步**：明确每个选项的“最小代价”（本题是 `alice[i] + 1`），以及选中后得到的“收益”（本题是 `i` 分）。  
  - **第三步**：遍历所有子集，比较代价是否在预算内，记录最大收益即可。