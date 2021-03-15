# #1253. **重构二行二进制矩阵** / Reconstruct a 2-Row Binary Matrix

> 难度：中等 · 标签：Array、Greedy、Matrix · [LeetCode 链接](https://leetcode.com/problems/reconstruct-a-2-row-binary-matrix/)

---

## 题目（英文原版）

**Description**

Given the following details of a matrix with n columns and 2 rows :
Your task is to reconstruct the matrix with upper, lower and colsum.
Return it as a 2-D integer array.
If there are more than one valid solution, any of them will be accepted.
If no valid solution exists, return an empty 2-D array.

**Examples**

**Example 1:**

```
Input: upper = 2, lower = 1, colsum = [1,1,1]
Output: [[1,1,0],[0,0,1]]
Explanation: [[1,0,1],[0,1,0]], and [[0,1,1],[1,0,0]] are also correct answers.
```

**Example 2:**

```
Input: upper = 2, lower = 3, colsum = [2,2,1,1]
Output: []
```

**Example 3:**

```
Input: upper = 5, lower = 5, colsum = [2,1,2,0,1,0,1,2,0,1]
Output: [[1,1,1,0,1,0,0,1,0,0],[1,0,1,0,0,0,1,1,0,1]]
```

**Constraints**

- 1 <= colsum.length <= 10^5
- 0 <= upper, lower <= colsum.length
- 0 <= colsum[i] <= 2

---

## 题目（中文翻译）

给定一个有 `n` 列、2 行的二进制矩阵的以下信息：

- `upper`：第一行（上层）中 1 的个数  
- `lower`：第二行（下层）中 1 的个数  
- `colsum`：长度为 `n` 的数组，其中 `colsum[i]` 表示第 `i` 列中 1 的总数（即该列上、下两行的和）

请根据上述信息重新构造该矩阵，并以 **二维整数数组** 的形式返回。  
- 若存在多个满足条件的矩阵，返回任意一个即可。  
- 若不存在合法的矩阵，返回空的二维数组。

**示例 1**  
输入: `upper = 2, lower = 1, colsum = [1,1,1]`  
输出: `[[1,1,0],[0,0,1]]`  
解释: `[[1,0,1],[0,1,0]]` 和 `[[0,1,1],[1,0,0]]` 也是合法答案。

**示例 2**  
输入: `upper = 2, lower = 3, colsum = [2,2,1,1]`  
输出: `[]`

**示例 3**  
输入: `upper = 5, lower = 5, colsum = [2,1,2,0,1,0,1,2,0,1]`  
输出: `[[1,1,1,0,1,0,0,1,0,0],[1,0,1,0,0,0,1,1,0,1]]`

**约束条件**  

- `1 <= colsum.length <= 10^5`  
- `0 <= upper, lower <= colsum.length`  
- `0 <= colsum[i] <= 2`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一列的 `colsum[i]` 按照 **所有可能的组合** 逐一尝试，然后检查是否满足 `upper` 与 `lower` 的总和要求。

- `colsum[i] = 0` 时，这一列只能是 `[0,0]`（上、下都放 0）。  
- `colsum[i] = 2` 时，只能是 `[1,1]`（上下各放 1）。  
- `colsum[i] = 1` 时，有两种选择：`[1,0]`（上放 1，下放 0）或 `[0,1]`（上放 0，下放 1）。

把所有 `colsum[i] = 1` 的列视为“待决定”的位置。  
我们可以用**回溯（DFS）**遍历每一种可能的填法：

1. 从左到右依次处理列。  
2. 对于 `colsum[i] = 1`，尝试把 1 放到上面或下面。  
3. 每次放置后更新已使用的 `upper_used`、`lower_used`。  
4. 若某一步已经超出 `upper` 或 `lower`，立刻回溯剪枝。  
5. 当遍历完所有列且 `upper_used == upper`、`lower_used == lower` 时，得到合法矩阵。

> **类比**：把每一列想象成一本字典的页码，`colsum[i] = 1` 的页码可以写在上面的目录或下面的目录，就像在查字典时，你可以先翻到上面的页码或下面的页码。我们要把所有“只能写在上面或只能写在下面”的页码先确定，再在“可以任选”的页码里试不同的组合。

**为什么这个方法正确**  
因为我们穷举了 **所有** 可能的填法，只要存在合法解，回溯一定能找到；若不存在合法解，遍历结束后返回空矩阵。

#### 代码（Python）

```python
from typing import List

def reconstructMatrix_bruteforce(upper: int, lower: int, colsum: List[int]) -> List[List[int]]:
    n = len(colsum)
    # 初始化答案矩阵
    upper_row = [0] * n
    lower_row = [0] * n

    # 深度优先搜索
    def dfs(idx: int, up_used: int, low_used: int) -> bool:
        # 已经处理完所有列
        if idx == n:
            # 检查是否恰好用了指定的 1 的个数
            return up_used == upper and low_used == lower

        # 处理当前列的三种情况
        if colsum[idx] == 0:          # 必须都是 0
            return dfs(idx + 1, up_used, low_used)

        if colsum[idx] == 2:          # 必须都是 1
            # 若放进去会超出上/下的上限，直接剪枝
            if up_used + 1 > upper or low_used + 1 > lower:
                return False
            upper_row[idx] = lower_row[idx] = 1
            return dfs(idx + 1, up_used + 1, low_used + 1)

        # colsum[idx] == 1，分两种尝试
        # 1）上放 1，下放 0
        if up_used + 1 <= upper:
            upper_row[idx] = 1
            lower_row[idx] = 0
            if dfs(idx + 1, up_used + 1, low_used):
                return True
            # 回溯
            upper_row[idx] = 0

        # 2）上放 0，下放 1
        if low_used + 1 <= lower:
            upper_row[idx] = 0
            lower_row[idx] = 1
            if dfs(idx + 1, up_used, low_used + 1):
                return True
            # 回溯
            lower_row[idx] = 0

        # 两条路都走不通，返回 False
        return False

    # 开始搜索
    if dfs(0, 0, 0):
        return [upper_row, lower_row]
    else:
        return []          # 无解
```

> **关键注释**  
> - `dfs` 的三个参数分别是当前处理的列下标、已用的上行 `1` 的个数、已用的下行 `1` 的个数。  
> - 当 `colsum[i] = 2` 时，如果放进去会让 `up_used` 或 `low_used` 超过上限，直接返回 `False`（剪枝）。  
> - 对 `colsum[i] = 1` 的两种选择分别递归尝试，找到第一条合法路径即返回。

#### 复杂度

- **时间复杂度**：最坏情况下，所有 `colsum[i] = 1`，我们需要尝试 2 种放法，遍历深度为 `n`，所以是 `O(2^k)`（`k` 为 `colsum` 中等于 1 的个数）。在最坏的 `k = n = 10^5` 时根本不可接受。  
  > 大白话：如果每一列都有“我要放 1 在上面还是下面”的选择，就像在十万道二选一的题目里逐个尝试，可能要尝遍全部组合，指数级增长，速度会非常慢。

- **空间复杂度**：递归栈深度为 `n`，需要 `O(n)` 的额外空间（存放 `upper_row`、`lower_row` 以及递归调用栈）。

---

### 2. 最优解

#### 思路  

暴力解慢的根源是 **盲目枚举** `colsum[i] = 1` 的每一种放置方式。实际上，这类列只有两种合法状态（`[1,0]` 或 `[0,1]`），我们可以**贪心**地决定把 1 放在哪一行，而不需要回溯。

观察：

1. **`colsum[i] = 2`** 必须同时占用上、下两行的 1。  
   - 所以我们先把所有 `2` 的列固定为 `[1,1]`，并直接从 `upper`、`lower` 中各减去 1。  
   - 如果此时 `upper` 或 `lower` 已经变成负数，说明要求的 1 太少，直接返回空矩阵。

2. **`colsum[i] = 0`** 必须是 `[0,0]`，不影响 `upper`、`lower`，直接跳过。

3. 剩下的全部是 **`colsum[i] = 1`**。此时我们只需要在上、下两行中**分配**这些 1，使得上行恰好用掉 `upper`（已经扣除掉所有 `2`）个，下面恰好用掉 `lower`（同理）个。  
   - 把 `upper` 视为“上面还能放多少个 1”。我们可以 **先把 1 放到上面**，直到上面的配额用完；剩余的 1 自动放到底下。  
   - 这一步是 **贪心**：把尽可能多的 `1` 放到上面，确保不超出 `upper`。因为上面的配额是固定的，任意把一个 `1` 放到底下，都会让上面的配额更难达标。  

   只要 `upper + lower` 正好等于 `colsum` 中 `1` 的个数（因为 `2` 的列已经占掉了各自的 1），上述分配一定可行。否则说明配额不匹配，返回空矩阵。

> **类比**：把每一列看成一只装有 0、1、2 块糖果的盒子。`2` 的盒子里必须把两块糖分别放进上、下两只碗；`0` 的盒子什么也不放；剩下的 `1` 的盒子只剩下一块糖，我们先把糖倒进“上碗”，直到上碗装满；剩余的糖自然倒进“下碗”。只要两碗的容量恰好匹配所有糖的总量，就一定能装完。

#### 代码（Python）

```python
from typing import List

def reconstructMatrix(upper: int, lower: int, colsum: List[int]) -> List[List[int]]:
    n = len(colsum)
    upper_row = [0] * n
    lower_row = [0] * n

    # 第一步：处理 2 和 0
    for i, v in enumerate(colsum):
        if v == 2:
            # 必须同时放 1
            upper_row[i] = lower_row[i] = 1
            upper -= 1
            lower -= 1
        elif v == 0:
            # 直接保持 0，什么也不做
            continue

    # 如果因为 2 的列已经把上/下的配额用光了（出现负数），直接返回空
    if upper < 0 or lower < 0:
        return []

    # 第二步：处理所有 1
    for i, v in enumerate(colsum):
        if v != 1:
            continue
        # 贪心：优先把 1 放到上面，只要还有上面的配额
        if upper > 0:
            upper_row[i] = 1
            upper -= 1
        else:
            # 上面配额已经用完，只能放到底下
            lower_row[i] = 1
            lower -= 1

    # 最后检查配额是否全部用完
    if upper == 0 and lower == 0:
        return [upper_row, lower_row]
    else:
        # 配额不匹配，说明无解
        return []
```

> **关键注释**  
> - 第一次遍历把所有 `2` 的列固定为 `[1,1]`，并同步扣除 `upper`、`lower`。  
> - 第二次遍历只看 `colsum[i] == 1` 的列：如果 `upper` 还有剩余，就把 1 放到上面；否则放到底下。  
> - 最后检查 `upper` 与 `lower` 是否恰好归零，确保所有需求都被满足。

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历两次数组（`n` 为列数），每一步都是常数时间。  
  > 大白话：我们只需要顺序看一遍所有列，两遍也算一次线性扫描，处理 10 万列只要几毫秒，完全可以接受。

- **空间复杂度**：`O(n)` 用于存放结果矩阵（两行 `n` 列）。除了输出之外，只用了若干个整数变量，额外空间是常数级 `O(1)`。

---

## 心得

- **核心技巧**：**贪心分配 + 预处理固定情况**  
  先把只能唯一决定的列（`0` 与 `2`）固定下来，再对唯一可变的 `1` 列采用“先填上、后填下”的贪心策略，使得配额恰好匹配。

- **适用的题型**  
  1. “两行二进制矩阵重建” 类问题（如本题）。  
  2. “分配资源到两个人” 的配额题，例如 `Split Array Largest Sum` 的简化版。  
  3. “按要求填充 0/1/2 的矩阵/数组”，需要先处理确定项，再贪心处理可选项。

- **一句话总结解题钥匙**  
  **先确定唯一解的部分，再用配额贪心把剩余的 1 分配到上、下两行**。

---

## 反思

- **第一反应**：看到 `colsum` 里只有 0、1、2 三种值，立刻想到可以把 `2` 固定为 `[1,1]`，`0` 固定为 `[0,0]`，只剩下 `1` 需要分配。  
- **最容易踩的坑**  
  - 忽视 `upper`、`lower` 在处理完 `2` 后可能已经变负的情况。  
  - 没有检查 `upper + lower` 是否恰好等于 `colsum` 中 `1` 的数量，导致最后配额不匹配却仍返回错误矩阵。  
  - 边界条件：当所有列都是 `0` 或 `2` 时，需要确保直接返回正确的全零或全一矩阵，而不是误判为无解。  

- **下次遇到同类题**：第一步 **先把“只能唯一决定”的位置固定下来**（这里是 `0` 与 `2`），再检查剩余配额是否还能满足 **“可自由选择”** 的位置（这里是 `1`），用贪心或简单计数完成分配。这样可以把复杂度控制在 `O(n)`。