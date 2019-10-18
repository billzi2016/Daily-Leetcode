# #624. 数组中的最大距离 / Maximum Distance in Arrays

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-distance-in-arrays/)

---

## 题目（英文原版）

**Description**

You are given m arrays, where each array is sorted in ascending order.
You can pick up two integers from two different arrays (each array picks one) and calculate the distance. We define the distance between two integers a and b to be their absolute difference |a - b|.
Return the maximum distance.

**Examples**

**Example 1:**

```
Input: arrays = [[1,2,3],[4,5],[1,2,3]]
Output: 4
Explanation: One way to reach the maximum distance 4 is to pick 1 in the first or third array and pick 5 in the second array.
```

**Example 2:**

```
Input: arrays = [[1],[1]]
Output: 0
```

**Constraints**

- m == arrays.length
- 2 <= m <= 105
- 1 <= arrays[i].length <= 500
- -104 <= arrays[i][j] <= 104
- arrays[i] is sorted in ascending order.
- There will be at most 105 integers in all the arrays.

---

## 题目（中文翻译）

**描述**  
给定 `m` 个数组，每个数组均已按升序排序。你可以从两个不同的数组中各选取一个整数（每个数组选一个），并计算它们的距离。我们定义两个整数 `a` 和 `b` 的距离为它们的绝对差 `|a - b|`。返回可能的最大距离。

**示例 1**  
```text
Input: arrays = [[1,2,3],[4,5],[1,2,3]]
Output: 4
```
**解释**：一种得到最大距离 4 的方式是：在第一个或第三个数组中选取 `1`，在第二个数组中选取 `5`。

**示例 2**  
```text
Input: arrays = [[1],[1]]
Output: 0
```
**解释**：只能在两个数组中各选取唯一的 `1`，距离为 `0`。

**约束条件**  
- `m == arrays.length`  
- `2 <= m <= 10^5`  
- `1 <= arrays[i].length <= 500`  
- `-10^4 <= arrays[i][j] <= 10^4`  
- `arrays[i]` 已按升序排序。  
- 所有数组中的整数总数至多为 `10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把**所有可能的组合**都算一遍：  
- 从第 `i` 个数组里任选一个数 `a`，  
- 再从第 `j`（`j ≠ i`）个数组里任选一个数 `b`，  
- 计算它们的距离 `|a - b|`，取最大值。  

这就像在超市里挑选两件商品，**每件商品都有很多种型号**，我们把每一种可能的搭配都列出来，挑出价差最大的那一对。  

因为每个子数组本身已经排好序了，我们仍然可以把它们当成普通的“列表”，不需要额外的数据结构。只要把 **所有两两数组** 以及 **数组内部的每个元素** 全部遍历一遍，就一定能找到答案——因为我们没有遗漏任何一种取法。

> **为什么这个方法一定正确？**  
> 我们枚举了 *所有* 合法的取法，最大距离自然会在这些取法之中出现。只要遍历完整，就不可能错过最优解。

#### 代码（Python）

```python
from typing import List

def maxDistance_bruteforce(arrays: List[List[int]]) -> int:
    """
    暴力解：遍历每一对数组，再遍历每一对元素，求绝对差的最大值。
    时间复杂度很高，只适合用来验证思路或在数据非常小的情况下使用。
    """
    ans = 0
    m = len(arrays)                         # 数组的个数
    for i in range(m):                      # 任选第 i 个数组
        for j in range(i + 1, m):           # 再任选第 j 个数组（j != i）
            # 对这两个数组中的每个元素两两组合
            for a in arrays[i]:
                for b in arrays[j]:
                    diff = abs(a - b)      # 计算距离
                    if diff > ans:         # 维护最大值
                        ans = diff
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(N²)`  
  - 这里的 `N` 代表 **所有数组中元素的总数**（最多 `10⁵`）。  
  - “`O(N²)`” 可以想象成“如果有 1000 个数字，要比较的次数大概是 1000 × 1000 = 100 万次”。当 `N` 很大时，计算量会爆炸，实际运行会超时。  
- **空间复杂度：** `O(1)`  
  - 只用了常数个额外变量 (`ans`, `i`, `j`, `a`, `b`)，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定最大距离的**，往往是**每个数组的最小值**和**最大值**。  
因为数组内部是升序的，取中间的数再和别的数组比较，得到的差距一定不如取该数组的**最左**（最小）或**最右**（最大）元素来得大。

**关键观察**：

- 假设我们已经遍历了前 `k` 个数组，记这 `k` 个数组里出现过的**全局最小值** `global_min` 和**全局最大值** `global_max`。  
- 当我们看到第 `k+1` 个数组 `cur` 时，若想让距离最大，只需要考虑两种情况：
  1. 用 `cur` 的 **最大元素** `cur_max` 与之前出现过的 **最小元素** `global_min` 组合 → 距离 `|cur_max - global_min|`  
  2. 用 `cur` 的 **最小元素** `cur_min` 与之前出现过的 **最大元素** `global_max` 组合 → 距离 `|cur_min - global_max|`  

这两种组合一定覆盖了所有可能的最优解，因为：

- 若最优解的左边来自某个已经遍历过的数组，那么它一定是该数组的最小值（否则可以把左边换成更小的数，使距离更大）。  
- 若最优解的右边来自当前数组，那么它一定是当前数组的最大值（同理）。  
- 反之亦然，最优解的右边可能来自之前的数组的最大值，左边来自当前数组的最小值。

于是我们可以 **一次遍历** 所有数组，实时维护 `global_min`、`global_max`，并在每一步计算上述两种距离，取最大即可。

> **类比**：想象有一排房子，每座房子都有最低温度和最高温度。我们想找两座不同房子之间的温差最大值。只要记录到目前为止出现过的最低温度和最高温度，每到一座新房子，就把它的最高温度和之前的最低温度比较，或者把它的最低温度和之前的最高温度比较，就能得到当前的最大温差。这样不需要把所有温度两两比较，省时又省力。

#### 代码（Python）

```python
from typing import List

def maxDistance(arrays: List[List[int]]) -> int:
    """
    最优解：一次遍历，维护已遍历数组的全局最小值和全局最大值，
    每处理一个新数组时，只比较两种可能的距离。
    时间 O(m)，空间 O(1)。
    """
    # 第一个数组的最小值和最大值先记下来
    global_min = arrays[0][0]               # 已遍历数组的最小元素
    global_max = arrays[0][-1]              # 已遍历数组的最大元素
    ans = 0                                 # 当前的最大距离

    # 从第二个数组开始遍历
    for idx in range(1, len(arrays)):
        cur = arrays[idx]
        cur_min = cur[0]                     # 当前数组的最小元素
        cur_max = cur[-1]                    # 当前数组的最大元素

        # 两种可能的最大距离
        dist1 = abs(cur_max - global_min)    # 当前最大 vs 之前最小
        dist2 = abs(cur_min - global_max)    # 当前最小 vs 之前最大
        ans = max(ans, dist1, dist2)         # 取三者的最大值

        # 更新全局最小值和最大值，供后面的数组使用
        global_min = min(global_min, cur_min)
        global_max = max(global_max, cur_max)

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(m)`（`m` 为数组的个数）  
  - 我们只遍历了一遍所有数组，每个数组只看了最左和最右两个数。  
  - 与暴力解的 `O(N²)`（`N` 为所有元素总数）相比，快了几个数量级。可以想象成“即使有 10⁵ 座房子，也只需要一次走访，就能算出最大温差”。  

- **空间复杂度：** `O(1)`  
  - 只用了常数个变量 `global_min`、`global_max`、`ans`，不随输入规模增长。

---

## 心得

- **核心技巧**：**只关注每个子数组的最小值和最大值**，并利用“全局最小 / 全局最大”进行一次遍历的贪心思路。  
- **适用的题型**：  
  1. “最大距离”类问题（如 LeetCode 624 – Maximum Distance in Arrays）。  
  2. “两组数的最大差”类问题（如在两行数组中找最大差）。  
  3. “全局极值 + 局部极值” 的优化思路（如在矩阵中找最大 Manhattan 距离）。  
- **一句话总结**：**只要把每个子数组的两端保存下来，遍历一次即可求出跨数组的最大距离。**

---

## 反思

- **第一反应**：看到“每个数组已排好序”，立刻想到“极值一定在两端”，于是尝试把每个数组的首尾元素取出来比较。  
- **最容易踩的坑**：  
  - **忘记“不同数组”** 的限制，误把同一数组的最小和最大直接相减。  
  - **边界条件**：只有一个元素的数组时，最小值和最大值是同一个，需要确保代码不会因为 `cur[0]` 与 `cur[-1]` 相同而出错。  
  - **更新顺序**：先计算距离再更新全局最小/最大，否则会把同一数组的两个端点错误地算成跨数组的组合。  
- **下次类似题目第一步**：**先找出每个子结构（数组、行、列）最有可能产生最优解的“关键点”**（如最小值/最大值），再考虑如何在一次遍历中利用这些关键点完成比较。