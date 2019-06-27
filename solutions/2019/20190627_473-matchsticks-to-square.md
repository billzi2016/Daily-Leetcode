# #473. 火柴棒组成正方形 / Matchsticks to Square

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/matchsticks-to-square/)

---

## 题目（英文原版）

**Description**

You are given an integer array matchsticks where matchsticks[i] is the length of the ith matchstick. You want to use all the matchsticks to make one square. You should not break any stick, but you can link them up, and each matchstick must be used exactly one time.
Return true if you can make this square and false otherwise.

**Examples**

**Example 1:**

```
Input: matchsticks = [1,1,2,2,2]
Output: true
Explanation: You can form a square with length 2, one side of the square came two sticks with length 1.
```

**Example 2:**

```
Input: matchsticks = [3,3,3,3,4]
Output: false
Explanation: You cannot find a way to form a square with all the matchsticks.
```

**Constraints**

- 1 <= matchsticks.length <= 15
- 1 <= matchsticks[i] <= 108

---

## 题目（中文翻译）

给定一个整数数组 **matchsticks**，其中 `matchsticks[i]` 表示第 `i` 根火柴棒的长度。你需要使用所有的火柴棒恰好组成一个正方形。**不能**折断任何火柴棒，但可以将它们首尾相连，每根火柴棒必须且只能使用一次。

如果能够组成这样的正方形返回 `true`，否则返回 `false`。

## 示例

### 示例 1
**输入**  
`matchsticks = [1,1,2,2,2]`

**输出**  
`true`

**解释**  
可以组成边长为 `2` 的正方形，其中正方形的一条边由两根长度为 `1` 的火柴棒拼接而成。

### 示例 2
**输入**  
`matchsticks = [3,3,3,3,4]`

**输出**  
`false`

**解释**  
无法使用所有火柴棒拼出一个正方形。

## 约束条件
- `1 <= matchsticks.length <= 15`
- `1 <= matchsticks[i] <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把每根火柴棒尝试放到四条边的任意一条上**，把所有可能的放置方式枚举完后，检查四条边的长度是否相等。  
- **数据结构**：用一个长度为 4 的数组 `sides` 来记录当前四条边已经累加的长度。`sides[i]` 就像是“第 i 条边的进度条”，初始都是 0。  
- **递归**：从第一根火柴棒开始，依次尝试把它放到第 0、1、2、3 条边上（如果放进去后该边的长度不超过目标边长）。递归结束的条件是所有火柴棒都已经用了，此时只要四条边长度相同（即都等于目标长度）就返回 `True`。  
- **为什么正确**：因为我们枚举了**所有**可能的分配方式，只要有一种方式能让四条边相等，递归就会找到并返回 `True`。  

**时间复杂度**  
每根火柴棒都有 4 种放置选择，最多有 `n` 根（`n ≤ 15`），所以最坏情况下要尝试 `4^n` 种情况。用大白话说，就是如果有 10 根火柴棒，最多要检查 4^10 ≈ 1,048,576 种组合。  
**空间复杂度**  
递归调用栈的深度是 `n`，每层只保存常数个变量，所以是 `O(n)`，这里最多 15 层，几乎可以忽略不计。

#### 代码（Python）

```python
from typing import List

def makesquare_bruteforce(matchsticks: List[int]) -> bool:
    # 总长度必须能被 4 整除，否则不可能组成正方形
    total = sum(matchsticks)
    if total % 4 != 0:
        return False
    target = total // 4                     # 每条边的目标长度

    # 为了加速剪枝，先把长的火柴棒放前面，容易提前发现不合法
    matchsticks.sort(reverse=True)

    # sides[i] 表示第 i 条边当前已经累加的长度
    sides = [0] * 4

    def dfs(idx: int) -> bool:
        """尝试把第 idx 根火柴棒放到四条边的某一条上"""
        if idx == len(matchsticks):          # 所有火柴棒都已放完
            # 如果每条边都正好等于 target，则成功
            return all(side == target for side in sides)

        cur = matchsticks[idx]               # 当前要放的火柴棒长度
        for i in range(4):
            # 剪枝：如果放到第 i 条边会超过目标长度，就跳过
            if sides[i] + cur > target:
                continue
            # 为了避免对称状态的重复搜索，如果当前边长度和前一条边相同，
            # 把火柴棒放到这条边没有意义（会产生相同的排列），直接跳过
            if i > 0 and sides[i] == sides[i - 1]:
                continue

            sides[i] += cur                   # 把火柴棒放到第 i 条边
            if dfs(idx + 1):                  # 递归尝试放下一根
                return True
            sides[i] -= cur                   # 回溯，撤销放置

        return False                          # 所有放置方式都不行

    return dfs(0)
```

#### 复杂度

- **时间复杂度**：`O(4^n)`——每根火柴棒有 4 种选择，指数级增长。  
- **空间复杂度**：`O(n)`——递归栈深度为火柴棒数量 `n`（最多 15），属于线性空间。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**大量重复的状态**：比如把两根相同长度的火柴棒分别放到第 0 条边和第 1 条边，与把它们调换顺序得到的状态是等价的。我们可以通过**排序+剪枝**大幅降低搜索树的宽度。

**关键优化点**：

1. **先排序（从大到小）**  
   把最长的火柴棒先放，若它已经导致某条边超长，就可以立刻剪掉整棵子树。相当于先把“大块”铺好，剩下的小块更容易填补。

2. **目标长度提前算好**  
   正方形每条边的长度 `target = sum(matchsticks) // 4`。如果总长度不是 4 的倍数，直接返回 `False`。

3. **对称剪枝**  
   当我们尝试把当前火柴棒放到某条边时，如果该边的长度和前一条边相同（`sides[i] == sides[i-1]`），则把火柴棒放到这条边不会产生新状态，直接跳过。这样可以避免把相同的火柴棒在不同的“相同长度的边”之间来回搬动。

4. **提前成功判定**  
   当前三条边都恰好填满 `target` 时，最后一条边必然也满足（因为总长度已经等于 `4 * target`），可以直接返回 `True`，不必继续递归。

整个思路仍然是**回溯**（深度优先搜索），但通过上述剪枝，实际遍历的分支数会大幅下降，在 `n ≤ 15` 的限制下可以轻松通过。

#### 代码（Python）

```python
from typing import List

def makesquare(matchsticks: List[int]) -> bool:
    total = sum(matchsticks)
    if total % 4 != 0:
        return False
    target = total // 4

    # 长的火柴棒先放，能更快触发剪枝
    matchsticks.sort(reverse=True)

    # 若最长的火柴棒已经超过目标边长，必然不可能
    if matchsticks[0] > target:
        return False

    sides = [0] * 4  # 记录四条边的当前长度

    def dfs(idx: int) -> bool:
        if idx == len(matchsticks):
            # 所有火柴棒都用了，检查四条边是否都恰好等于 target
            return all(side == target for side in sides)

        cur = matchsticks[idx]
        for i in range(4):
            if sides[i] + cur > target:      # 超过目标长度，剪枝
                continue
            if i > 0 and sides[i] == sides[i - 1]:  # 对称剪枝
                continue

            sides[i] += cur                   # 放置
            if dfs(idx + 1):                  # 继续递归
                return True
            sides[i] -= cur                   # 回溯

            # 如果当前边刚好为 0（即这根火柴棒是放进空边），
            # 那么后面的空边放同样的火柴棒也没有意义，直接跳出循环
            if sides[i] == 0:
                break

        return False

    return dfs(0)
```

#### 复杂度

- **时间复杂度**：在最坏情况下仍是指数级 `O(4^n)`，但由于排序、对称剪枝和提前失败的剪枝，实际遍历的分支数远小于暴力解。对于本题的约束（`n ≤ 15`），运行时间通常在毫秒级。可以把它理解为“原本要检查 1,000,000 种可能，现在只检查几千种”。  
- **空间复杂度**：`O(n)`——递归栈深度为火柴棒数量 `n`（最多 15），加上常数级的 `sides` 数组。

---

## 心得

- 本题核心考察**回溯 + 剪枝**的能力，尤其是如何利用**对称性**和**先排序**来大幅削减搜索空间。  
- 这类技巧在其他“分割/组合”问题中也非常常用，例如：  
  1. **分割等和子集**（Partition Equal Subset Sum）  
  2. **装箱问题**（Bin Packing）  
  3. **N 叉树的分配**（例如把数字分成 k 组，使每组和相等）  
- 一句话总结解题钥匙：**“先把大块铺好，再用对称剪枝避免重复搜索”。**

---

## 反思

- **第一反应**：看到“把所有火柴棒用完并且每条边相等”，立刻想到“把数组划分成四等份”，于是想到了枚举每根火柴棒属于哪条边的全排列。  
- **最容易踩的坑**：  
  - 忘记先判断总长度是否能被 4 整除，导致不必要的递归。  
  - 没有对相同长度的边做对称剪枝，导致大量重复状态，程序会超时。  
  - 边界条件：如果最长的火柴棒本身就大于目标边长，必须直接返回 `False`。  
- **下次遇到同类题**，第一步应该先**检查整体可行性（总和、最大值）并排序**，然后再考虑**回溯 + 剪枝**的搜索框架。这样可以把搜索空间压到最小。