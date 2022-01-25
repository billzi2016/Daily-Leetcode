# #1642. 最远可达建筑 / Furthest Building You Can Reach

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/furthest-building-you-can-reach/)

---

## 题目（英文原版）

**Description**

You are given an integer array heights representing the heights of buildings, some bricks, and some ladders.
You start your journey from building 0 and move to the next building by possibly using bricks or ladders.
While moving from building i to building i+1 (0-indexed),
Return the furthest building index (0-indexed) you can reach if you use the given ladders and bricks optimally.

**Examples**

**Example 1:**

```
Input: heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1
Output: 4
Explanation: Starting at building 0, you can follow these steps:
- Go to building 1 without using ladders nor bricks since 4 >= 2.
- Go to building 2 using 5 bricks. You must use either bricks or ladders because 2 < 7.
- Go to building 3 without using ladders nor bricks since 7 >= 6.
- Go to building 4 using your only ladder. You must use either bricks or ladders because 6 < 9.
It is impossible to go beyond building 4 because you do not have any more bricks or ladders.
```

**Example 2:**

```
Input: heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2
Output: 7
```

**Example 3:**

```
Input: heights = [14,3,19,3], bricks = 17, ladders = 0
Output: 3
```

**Constraints**

- 1 <= heights.length <= 105
- 1 <= heights[i] <= 106
- 0 <= bricks <= 109
- 0 <= ladders <= heights.length

---

## 题目（中文翻译）

你得到一个整数数组 `heights`，其中 `heights[i]` 表示第 `i` 座建筑的高度，同时还有若干块砖（bricks）和若干根梯子（ladders）。

你从第 0 座建筑出发，依次前往后面的建筑。在从第 `i` 座建筑移动到第 `i+1` 座建筑（下标均为 0 起始）时：

- 如果 `heights[i+1] ≤ heights[i]`，则不需要使用砖或梯子。
- 如果 `heights[i+1] > heights[i]`，则需要克服高度差 `diff = heights[i+1] - heights[i]`，可以选择使用 **砖**（消耗 `diff` 块砖）或 **梯子**（不消耗砖）。

在使用给定的砖和梯子的前提下，**最优**地分配它们，使你能够到达的最远建筑下标（0 起始）是多少？

---

## 示例

### 示例 1  
**输入**  
```text
heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1
```  
**输出**  
```text
4
```  
**解释**  
从建筑 0 开始，你可以按以下方式前进：

- 前往建筑 1：`4 ≥ 2`，无需使用砖或梯子。  
- 前往建筑 2：`2 < 7`，需要克服高度差 5，使用 5 块砖。  
- 前往建筑 3：`7 ≥ 6`，无需使用砖或梯子。  
- 前往建筑 4：`6 < 9`，使用唯一的梯子。  
此时已无砖或梯子可用，无法再前进到建筑 5，故最远可达下标为 4。

---

### 示例 2  
**输入**  
```text
heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2
```  
**输出**  
```text
7
```  

---

### 示例 3  
**输入**  
```text
heights = [14,3,19,3], bricks = 17, ladders = 0
```  
**输出**  
```text
3
```  

---

## 约束条件

- `1 ≤ heights.length ≤ 10^5`
- `1 ≤ heights[i] ≤ 10^6`
- `0 ≤ bricks ≤ 10^9`
- `0 ≤ ladders ≤ heights.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

从第 0 栋楼出发，每次只能往右走到相邻的第 i+1 栋楼。  
如果下一栋楼比当前楼高 `diff = heights[i+1] - heights[i] > 0`，我们必须花 **砖块**（消耗 `diff` 块）或 **梯子**（不消耗砖块）来克服这段上升；如果 `diff ≤ 0`，直接走过去，不需要任何资源。

最直接的想法是：**遍历所有可能的走法**，把每一次上升都尝试所有分配砖块或梯子的方式，看看最远能走到哪。  
这相当于在每一次需要资源时，做一次“二选一”的递归/回溯。

- **数据结构**：只需要一个普通的列表 `heights`，以及两个整数 `bricks`、`ladders` 来记录剩余资源。  
  - 把 **砖块** 想成口袋里的“小石子”，每次上坡要用掉对应数量的石子。  
  - 把 **梯子** 想成“一把万能的跳板”，一次可以直接跨过去任意高度的上坡。

- **为什么正确**：因为我们枚举了**所有**可能的分配方式，哪怕是最差的也会被尝试到，最终得到的最远位置必然是最优的。

- **复杂度分析**：  
  - 每一次上坡都要分两路递归，最坏情况下会出现指数级的分支数。设 `n = len(heights)`，上坡次数最多是 `n-1`，所以时间复杂度约为 `O(2^{n})`，这在实际中根本不可接受。  
  - 空间上需要保存递归栈，最深为 `n`，即 `O(n)`。

> **大白话**：  
> `O(2^{n})` 就像每走一步就要把所有可能的选择全部列出来，走到第 20 步时就要列出 1,048,576 种情况，根本不可能在电脑里跑完。

#### 代码（Python）

```python
def furthest_building_bruteforce(heights, bricks, ladders):
    """
    暴力递归搜索所有可能的砖块/梯子分配方式
    返回能到达的最远建筑下标
    """
    n = len(heights)

    def dfs(idx, remain_bricks, remain_ladders):
        """
        idx: 当前所在的建筑下标
        remain_bricks / remain_ladders: 剩余资源
        返回从 idx 出发最远能到达的下标
        """
        # 已经是最后一栋楼，直接返回
        if idx == n - 1:
            return idx

        # 计算到下一栋楼的高度差
        diff = heights[idx + 1] - heights[idx]

        # 如果不需要上升，直接前进
        if diff <= 0:
            return dfs(idx + 1, remain_bricks, remain_ladders)

        # 需要资源：尝试使用砖块
        ans = idx  # 默认最远位置就是当前 idx
        if remain_bricks >= diff:
            ans = max(ans, dfs(idx + 1, remain_bricks - diff, remain_ladders))

        # 尝试使用梯子
        if remain_ladders > 0:
            ans = max(ans, dfs(idx + 1, remain_bricks, remain_ladders - 1))

        # 两种选择都不行时，停在当前楼
        return ans

    return dfs(0, bricks, ladders)
```

#### 复杂度

- **时间复杂度**：`O(2^{n})` — 每一次需要上升都要分两条路递归，指数级增长，实际不可用。  
- **空间复杂度**：`O(n)` — 递归调用栈的最大深度等于建筑数量。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈**在于每次上坡都要“决定”使用砖块还是梯子。  
如果我们能**一次性**决定哪些上坡用梯子，哪些用砖块，就不必枚举所有可能。

**关键观察**：

- 梯子可以跨任意高度的上坡，显然我们想把梯子留给“**最高的上坡**”。  
- 对于其余的上坡，使用砖块的代价就是它们的高度差之和。

于是我们可以 **遍历建筑**，把每一次需要上坡的 `diff` 放进一个 **最小堆（小根堆）** 中：

1. **把每一次上坡的 `diff` 都压入堆**。堆里保存的是已经“暂时使用梯子”的上坡高度差（因为我们先假设每一次上坡都用梯子）。
2. 当堆的大小 **超过可用梯子数量 `ladders`** 时，说明已经有太多“用梯子”的上坡了。此时我们 **弹出堆中最小的 `diff`**，把它改为使用砖块（因为它是所有已用梯子的上坡里最省砖块的那一个），并把对应的砖块数累加到 `used_bricks`。
3. **如果此时累计的砖块数 `used_bricks` 超过了可用砖块 `bricks`**，说明已经没有足够的砖块来支撑当前的决定，**只能停在当前建筑**，返回下标 `i`。

这样遍历结束（或者提前退出）时，返回的下标就是最远能到达的建筑。

- **数据结构**：**最小堆**（Python 中的 `heapq`），类似于“装有小石子的盒子”，每次可以 **快速取出最小的那块石子**（即最小的上坡），时间复杂度为 `O(log k)`（`k` 为堆的大小）。
- **为什么最优**：因为我们始终把梯子留给最大的 `ladders` 次上坡；其余的上坡必然是用砖块的最小集合，累计砖块最小，符合“用最少砖块走得最远”的目标。

#### 代码（Python）

```python
import heapq

def furthest_building(heights, bricks, ladders):
    """
    使用最小堆实现贪心算法
    返回能够到达的最远建筑下标（0-indexed）
    """
    # 小根堆，存放已经“用梯子”处理的上坡高度差
    min_heap = []
    used_bricks = 0  # 已经消耗的砖块数量

    for i in range(len(heights) - 1):
        diff = heights[i + 1] - heights[i]
        if diff <= 0:
            # 不需要任何资源，直接前进
            continue

        # 暂时把这次上坡当作使用梯子，放进堆
        heapq.heappush(min_heap, diff)

        # 如果梯子使用次数超过了可用数量，需要把最小的那次改为使用砖块
        if len(min_heap) > ladders:
            smallest = heapq.heappop(min_heap)   # 取出最小的 diff
            used_bricks += smallest               # 用砖块来完成这段上坡

        # 检查砖块是否已经不够用了
        if used_bricks > bricks:
            # 第 i 栋楼已经无法前进到 i+1，返回 i
            return i

    # 循环结束说明所有建筑都能到达
    return len(heights) - 1
```

#### 复杂度

- **时间复杂度**：`O(n log ladders)`  
  - 遍历 `n` 次，每次对堆进行 `push`（`O(log k)`）和最多一次 `pop`（`O(log k)`），其中堆的大小最多是 `ladders + 1`，所以是 `O(log ladders)`。  
  - 与暴力解相比，指数级的 `2^n` 降到了线性乘对数级，几乎可以在 10⁵ 条数据内轻松跑完。

- **空间复杂度**：`O(ladders)`  
  - 堆中最多保存 `ladders + 1` 个元素（因为超过后会弹出），与建筑数量无关，只和梯子数目有关。  

> **对比**：暴力解需要指数时间，根本不可用；最优解只需 `n` 次遍历加上对堆的对数操作，真正实用。

---

## 心得

- **核心技巧**：**贪心 + 最小堆** —— 把“把梯子留给最大的上坡”这一直觉用堆实现，保证每一步的决策都是局部最优且全局最优。
- **适用题型**  
  1. **分配有限资源让损失最小**（如「分配 k 条绳子跨河」）  
  2. **需要动态维护“前 k 大”或“前 k 小”元素**（如「找到第 K 大的子数组和」）  
  3. **在顺序遍历中随时决定使用哪种资源**（如「最大化可到达的城市数量」）
- **一句话总结**：**“把梯子用在最高的几段跳，剩下的用砖块，堆帮我们随时挑最小的跳换成砖块”。**

---

## 反思

- **第一反应**：看到“砖块”和“梯子”两种资源，马上想到要**枚举**每一次的使用方式，导致想到暴力递归。
- **最容易踩的坑**  
  - 忘记处理 `diff ≤ 0`（下坡或平地）时不消耗资源，会误把负数加入堆导致错误。  
  - 堆的大小判断写成 `>= ladders` 而不是 `> ladders`，会提前把本应该用梯子的跳改为砖块，导致砖块提前耗尽。  
  - 边界条件：当 `ladders = 0` 时，堆始终为空，算法仍然正确；当 `bricks` 很大时，可能根本不需要弹出堆，直接遍历完。
- **下次思路**：面对“有限资源分配”类问题，**先假设把所有资源都用最贵的方式（梯子）**，再用堆把“最贵的”逐步换成“便宜的”（砖块），检查是否仍在预算内。这样可以快速得到最优解。