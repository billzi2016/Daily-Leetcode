# #1595. 连接两组点的最小成本 / Minimum Cost to Connect Two Groups of Points

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Matrix、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-connect-two-groups-of-points/)

---

## 题目（英文原版）

**Description**

You are given two groups of points where the first group has size1 points, the second group has size2 points, and size1 >= size2.
The cost of the connection between any two points are given in an size1 x size2 matrix where cost[i][j] is the cost of connecting point i of the first group and point j of the second group. The groups are connected if each point in both groups is connected to one or more points in the opposite group. In other words, each point in the first group must be connected to at least one point in the second group, and each point in the second group must be connected to at least one point in the first group.
Return the minimum cost it takes to connect the two groups.

**Examples**

**Example 1:**

```
Input: cost = [[15, 96], [36, 2]]
Output: 17
Explanation: The optimal way of connecting the groups is:
1--A
2--B
This results in a total cost of 17.
```

**Example 2:**

```
Input: cost = [[1, 3, 5], [4, 1, 1], [1, 5, 3]]
Output: 4
Explanation: The optimal way of connecting the groups is:
1--A
2--B
2--C
3--A
This results in a total cost of 4.
Note that there are multiple points connected to point 2 in the first group and point A in the second group. This does not matter as there is no limit to the number of points that can be connected. We only care about the minimum total cost.
```

**Example 3:**

```
Input: cost = [[2, 5, 1], [3, 4, 7], [8, 1, 2], [6, 2, 4], [3, 8, 8]]
Output: 10
```

**Constraints**

- size1 == cost.length
- size2 == cost[i].length
- 1 <= size1, size2 <= 12
- size1 >= size2
- 0 <= cost[i][j] <= 100

---

## 题目（中文翻译）

**描述**  
给定两组点，其中第一组有 `size1` 个点，第二组有 `size2` 个点，且满足 `size1 >= size2`。任意两个点之间的连接成本由一个 `size1 × size2` 的矩阵 `cost` 给出，`cost[i][j]` 表示将第一组的第 `i` 个点与第二组的第 `j` 个点相连的费用。若每个点在两组之间至少与一个对方组的点相连，则称这两组是**已连接 (connected)** 的——即第一组的每个点必须至少连接到第二组的一个点，第二组的每个点也必须至少连接到第一组的一个点。  
返回使两组点全部相连的最小总成本。

**示例**  

### 示例 1  
**输入**  
```text
cost = [[15, 96], [36, 2]]
```  
**输出**  
```text
17
```  
**解释**  
一种最优的连接方式是：  
- 第 1 个点 ↔ 第 A 个点  
- 第 2 个点 ↔ 第 B 个点  

这样总费用为 `15 + 2 = 17`。

### 示例 2  
**输入**  
```text
cost = [[1, 3, 5], [4, 1, 1], [1, 5, 3]]
```  
**输出**  
```text
4
```  
**解释**  
一种最优的连接方式是：  
- 第 1 个点 ↔ 第 A 个点  
- 第 2 个点 ↔ 第 B 个点  
- 第 2 个点 ↔ 第 C 个点  
- 第 3 个点 ↔ 第 A 个点  

总费用为 `1 + 1 + 1 + 1 = 4`。  
注意，点 2 可以同时连接到多个第二组的点，点 A 也可以同时连接到多个第一组的点。连接数量没有上限，我们只关注最小总费用。

### 示例 3  
**输入**  
```text
cost = [[2, 5, 1], [3, 4, 7], [8, 1, 2], [6, 2, 4], [3, 8, 8]]
```  
**输出**  
```text
10
```  

**约束条件**  

- `size1 == cost.length`  
- `size2 == cost[i].length`  
- `1 <= size1, size2 <= 12`  
- `size1 >= size2`  
- `0 <= cost[i][j] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把**所有可能的连线方式**都列举出来，找出满足“左组每个点至少连到右组一个点、右组每个点也至少连到左组一个点”且费用最小的方案。

- **数据结构**：我们可以用一个二维数组 `connections[i][j]`（即题目给出的 `cost[i][j]`）来记录左侧第 `i` 个点和右侧第 `j` 个点之间的连线费用。  
  类比：这就像一本**价格表**，行是左边的商品，列是右边的商品，格子里写的是买这两件商品一起的折扣价。

- **枚举方式**：对左侧的每一个点，任选它要连的右侧点的**子集**（子集可以是空集、单个点、两个点…），所有左侧点的子集组合起来就是一种完整的连线方案。  
  这里的“子集”可以用二进制掩码（bitmask）来表示：`mask` 的第 `j` 位为 1 表示左点 `i` 与右点 `j` 之间建立了连线。

- **为什么一定能得到答案**：因为我们把**所有**合法的连线方式都遍历了一遍，最小费用自然会在其中出现。

- **时间/空间分析**：  
  - 左侧有 `size1` 个点，右侧有 `size2` 个点。  
  - 对每个左点，要遍历 `2^{size2}` 种子集。  
  - 所以总的遍历次数是 `(2^{size2})^{size1} = 2^{size1·size2}`。  
  - 这在最坏情况下是 `2^{12·12}=2^{144}`，天文数字，根本跑不完。  
  - 空间上只需要保存当前方案的费用，总共 `O(size1·size2)`。

> **大白话**：如果你把每一次选择想象成一次“掷硬币”，左侧每点掷 `size2` 次硬币（每次决定连不连），所有左点一起掷完相当于掷了 `size1·size2` 次硬币，总共会有 `2^{size1·size2}` 种可能的硬币组合——这远远超过我们电脑能在一秒钟算完的次数。

#### 代码（Python）

```python
import math
from itertools import product

def minCost_bruteforce(cost):
    n, m = len(cost), len(cost[0])          # n = size1, m = size2
    best = math.inf                         # 记录全局最小费用

    # 对每个左点 i，遍历它可以连的右点子集（用 0/1 表示是否连）
    # product 会生成 n 个长度为 m 的二进制序列的笛卡尔积，即所有可能的连线方案
    for masks in product(range(1 << m), repeat=n):
        # 检查是否合法：每个左点必须至少连一个右点
        if any(mask == 0 for mask in masks):
            continue

        # 统计每个右点是否被连过
        right_covered = 0
        total = 0
        for i, mask in enumerate(masks):
            # 计算左点 i 与它选中的右点的费用之和
            j = 0
            cur = 0
            while mask:
                if mask & 1:
                    cur += cost[i][j]
                    right_covered |= 1 << j
                mask >>= 1
                j += 1
            total += cur

        # 每个右点也必须至少被连一次
        if right_covered != (1 << m) - 1:
            continue

        best = min(best, total)

    return best
```

> 关键行解释  
> - `product(range(1 << m), repeat=n)`：把每个左点的“连线子集”全部组合起来。  
> - `right_covered |= 1 << j`：把已经被连到的右点记下来，类似“在字典里标记页码”。  
> - `if right_covered != (1 << m) - 1`：检查右侧是否全部被覆盖。

#### 复杂度

- **时间复杂度**：`O( 2^{size1·size2} )` —— 这里的指数代表“每一次选择都要尝试所有可能”，在实际中根本不可行。  
- **空间复杂度**：`O(size1·size2)` —— 只保存输入矩阵和少量临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们把**所有**子集都枚举了。其实我们不需要一次性决定所有左点的连线，只要逐步处理左点，同时记录**右点哪些已经被覆盖**，就可以大幅剪枝。

核心思路：

1. **状态压缩**  
   - 用一个 `mask`（二进制整数）记录右侧哪些点已经至少被连过一次。  
   - 第 `j` 位为 1 表示右点 `j` 已经有至少一条连线。  
   - 这相当于在“查字典”，`key` 是右点的编号，`value` 是是否已经被覆盖。

2. **动态规划**  
   - `dp[i][mask]`：处理完前 `i` 个左点后，右侧已覆盖的集合为 `mask` 时的最小费用。  
   - 初始状态：`dp[0][0] = 0`（还没处理任何左点，右侧全未覆盖，费用 0）。  

3. **状态转移**  
   - 对第 `i` 个左点，我们必须让它至少连到 **一个** 右点。  
   - 为了保持 DP 的简洁，只考虑“连到单个右点”，因为如果某个左点需要连到多个右点，后面的左点在以后仍然可以再补上缺失的右点，费用不会更高。  
   - 转移式：

\[
dp[i+1][mask \,|\, (1<<j)] = \min\bigl(dp[i+1][mask \,|\, (1<<j)],\; dp[i][mask] + cost[i][j]\bigr)
\]

   - 这里的 `|` 表示把第 `j` 位设为 1，意味着右点 `j` 已经被覆盖。

4. **处理剩余未覆盖的右点**  
   - 走完所有左点后，`mask` 可能仍然缺少一些右点。  
   - 对每个未覆盖的右点 `j`，我们可以任选**任意**左点再连一条线，费用最小的就是 `min_i cost[i][j]`（把它连到最便宜的左点）。  
   - 预先算出 `minCostRight[j] = min_i cost[i][j]`，然后对每个 `mask` 加上所有未覆盖右点的最小费用。

5. **答案**  

\[
\text{answer} = \min_{mask} \bigl( dp[n][mask] + \sum_{j\notin mask} minCostRight[j] \bigr)
\]

   - 这里的 `n = size1`，`mask` 遍历所有 `2^{size2}` 种可能。

**为什么只让每个左点连到一个右点就够了？**  
因为我们在最后会为每个未覆盖的右点补上一条最便宜的连线。若某个左点本来就已经连了多个右点，等价于把其中多余的连线“提前”到了补齐阶段，费用不变甚至可能更低（因为我们总是选最小的）。因此在 DP 中只考虑单连线即可大幅降低状态数。

**复杂度**  
- 状态数：`size1`（最多 12）层 × `2^{size2}`（最多 4096）  
- 每个状态遍历所有 `size2` 条可能的连线。  
- 总时间 `O(size1 * size2 * 2^{size2})`，在最坏情况下约 `12 * 12 * 4096 ≈ 590k` 次，轻松跑完。  
- 只保存两层 DP（滚动数组），空间 `O(2^{size2})`。

#### 代码（Python）

```python
from math import inf
from typing import List

def minCostConnectGroups(cost: List[List[int]]) -> int:
    """
    动态规划 + 位运算（Bitmask）
    dp[mask] 表示已经处理完当前所有左点，右侧被覆盖的集合为 mask 时的最小费用。
    """
    n, m = len(cost), len(cost[0])          # n = size1, m = size2

    # 1. 预处理：每个右点最便宜的连线费用
    min_right = [min(cost[i][j] for i in range(n)) for j in range(m)]

    # 2. 初始化 DP，只有「没有左点」且「没有右点被覆盖」的情况费用为 0
    dp = [inf] * (1 << m)
    dp[0] = 0

    # 3. 逐个左点进行转移
    for i in range(n):
        ndp = [inf] * (1 << m)               # 下一层 DP
        for mask in range(1 << m):
            if dp[mask] == inf:               # 该状态不可达，直接跳过
                continue
            # 当前左点 i 必须至少连一个右点 j
            for j in range(m):
                new_mask = mask | (1 << j)    # 把右点 j 标记为已覆盖
                ndp[new_mask] = min(ndp[new_mask],
                                   dp[mask] + cost[i][j])
        dp = ndp                              # 换到下一层

    # 4. 计算答案：遍历所有可能的覆盖情况，补齐未覆盖的右点
    answer = inf
    full_mask = (1 << m) - 1
    for mask in range(1 << m):
        # 已经覆盖的右点不需要额外费用，未覆盖的右点加上最小连线费用
        extra = 0
        for j in range(m):
            if not (mask >> j) & 1:           # 第 j 位为 0，说明未覆盖
                extra += min_right[j]
        answer = min(answer, dp[mask] + extra)

    return answer
```

> 关键行解释  
> - `min_right[j] = min(cost[i][j] for i in range(n))`：相当于“查字典”，找出把右点 `j` 连到最便宜的左点的费用。  
> - `new_mask = mask | (1 << j)`：把右点 `j` 标记为“已经被覆盖”。这一步类似“在集合里加入一个新元素”。  
> - `for mask in range(1 << m)`：遍历所有可能的右点覆盖集合，`1 << m` 就是 `2^m`，比如 `m=3` 时有 `000、001、010、011、100、101、110、111` 八种情况。  
> - `extra += min_right[j]`：把所有仍未被覆盖的右点“补一刀”，费用取最小值。

#### 复杂度

- **时间复杂度**：`O(size1 * size2 * 2^{size2})`  
  - 解释：我们有 `size1` 层循环，每层遍历 `2^{size2}` 种掩码，每个掩码再遍历 `size2` 条可能的连线。对于最大限制 `size1=12, size2=12`，大约是 `12 * 12 * 4096 ≈ 5.9×10^5` 次运算，几乎在一毫秒级完成。

- **空间复杂度**：`O(2^{size2})`  
  - 只保留当前层和下一层的 DP 数组（各 `2^{size2}` 大小），相当于“只记住最近一次的字典”。对于 `size2=12`，只需要 4096 个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**位掩码 + 动态规划**（DP on subsets）。  
  用二进制的每一位表示右侧点是否已经被覆盖，把“覆盖状态”压缩进一个整数，从而把指数级的子集枚举转化为线性的 DP 转移。

- **适用的题型**  
  1. **最小费用覆盖**（如本题）  
  2. **分配/匹配问题**（如“最小化工作分配的总时间”）  
  3. **集合覆盖类 DP**（如 LeetCode 1985 “Find the Kth Smallest Sum of a Matrix With Sorted Rows” 的子集 DP 版本）

- **一句话总结**：  
  **“把‘哪些右点已经被连’压进一个二进制整数，用 DP 按左点逐步扩展，再把剩下的右点补上最便宜的连线。”**

---

## 反思

- **第一反应**：看到“每个点至少连一次”，自然想到**全枚举**所有连线组合——这在思路上是对的，但会导致指数爆炸。

- **最容易踩的坑**  
  1. **忘记左点必须至少连一次**：在 DP 中必须保证每一步都选至少一条边，否则会出现非法状态。  
  2. **掩码的位数写错**：`1 << m` 表示 `2^m`，而不是 `1 << (m-1)`，容易导致数组越界。  
  3. **未覆盖右点的补齐**：只算完所有左点的 DP 而不加上 `min_right` 的补齐，会得到错误的答案。

- **下次类似题目第一步**：  
  先问自己“是否可以用**位掩码**描述已完成的子集”，如果答案是 Yes，就立刻考虑 **DP on subsets**，把状态压缩到 `2^{子集大小}`，再在此基础上设计转移。这样往往能把暴力的指数层数降到可接受的 `O(n·2^k)`。