# #1691. 堆叠长方体的最大高度 / Maximum Height by Stacking Cuboids 

> 难度：困难 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-height-by-stacking-cuboids/)

---

## 题目（英文原版）

**Description**

Given n cuboids where the dimensions of the ith cuboid is cuboids[i] = [widthi, lengthi, heighti] (0-indexed). Choose a subset of cuboids and place them on each other.
You can place cuboid i on cuboid j if widthi <= widthj and lengthi <= lengthj and heighti <= heightj. You can rearrange any cuboid's dimensions by rotating it to put it on another cuboid.
Return the maximum height of the stacked cuboids.

**Examples**

**Example 1:**

```
Input: cuboids = [[50,45,20],[95,37,53],[45,23,12]]
Output: 190
Explanation:
Cuboid 1 is placed on the bottom with the 53x37 side facing down with height 95.
Cuboid 0 is placed next with the 45x20 side facing down with height 50.
Cuboid 2 is placed next with the 23x12 side facing down with height 45.
The total height is 95 + 50 + 45 = 190.
```

**Example 2:**

```
Input: cuboids = [[38,25,45],[76,35,3]]
Output: 76
Explanation:
You can't place any of the cuboids on the other.
We choose cuboid 1 and rotate it so that the 35x3 side is facing down and its height is 76.
```

**Example 3:**

```
Input: cuboids = [[7,11,17],[7,17,11],[11,7,17],[11,17,7],[17,7,11],[17,11,7]]
Output: 102
Explanation:
After rearranging the cuboids, you can see that all cuboids have the same dimension.
You can place the 11x7 side down on all cuboids so their heights are 17.
The maximum height of stacked cuboids is 6 * 17 = 102.
```

**Constraints**

- n == cuboids.length
- 1 <= n <= 100
- 1 <= widthi, lengthi, heighti <= 100

---

## 题目（中文翻译）

给定 `n` 个长方体（cuboid），第 `i` 个长方体的尺寸为 `cuboids[i] = [width_i, length_i, height_i]`（0 索引）。从中挑选一个子集并将它们依次叠放。

如果满足 `width_i <= width_j`、`length_i <= length_j` 且 `height_i <= height_j`，则可以将长方体 `i` 放在长方体 `j` 上。每个长方体的三维尺寸可以通过旋转任意重新排列，以便能够放置在另一长方体上。

返回能够叠放的长方体的**最大总高度**。

**示例 1**  
**输入**: `cuboids = [[50,45,20],[95,37,53],[45,23,12]]`  
**输出**: `190`  
**解释**:  
- 将长方体 1 底面选为 `53x37`，高度为 `95`，放在最底层。  
- 将长方体 0 底面选为 `45x20`，高度为 `50`，放在其上。  
- 将长方体 2 底面选为 `23x12`，高度为 `45`，放在最上层。  
- 总高度为 `95 + 50 + 45 = 190`。

**示例 2**  
**输入**: `cuboids = [[38,25,45],[76,35,3]]`  
**输出**: `76`  
**解释**:  
两个长方体无法相互堆叠。我们选择长方体 1 并将其旋转，使 `35x3` 为底面，高度为 `76`。

**示例 3**  
**输入**: `cuboids = [[7,11,17],[7,17,11],[11,7,17],[11,17,7],[17,7,11],[17,11,7]]`  
**输出**: `102`  
**解释**:  
经过旋转后，所有长方体的尺寸均相同。可以将 `11x7` 作为底面放置，所有长方体的高度均为 `17`。  
最大堆叠高度为 `6 * 17 = 102`。

**约束条件**  
- `n == cuboids.length`  
- `1 <= n <= 100`  
- `1 <= width_i, length_i, height_i <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的堆叠方式** 都穷举一遍，找出高度最大的那一种。  
具体可以这么做：

1. **先选子集**：从 `n` 个立方体中挑出任意若干个（包括只选一个、全选或不选）。这一步相当于遍历所有子集，子集的数量是 `2ⁿ`。  
2. **排列顺序**：对选中的立方体，尝试所有可能的放置顺序（即全排列），因为不同的顺序会导致不同的能否堆叠。`k` 个立方体的全排列有 `k!` 种。  
3. **尝试所有旋转**：每个立方体可以把三条边任意调换位置（相当于 6 种旋转），只要有一种旋转方式满足 “宽 ≤ 下方宽、长 ≤ 下方长、高 ≤ 下方高” 就算合法。  

只要找到一种合法的旋转+顺序组合，就可以算出这堆的总高度，最后取最大值。

> **类比**：把每个立方体想象成一本书，暴力解相当于把书全部挑出来，尝试所有可能的排放顺序和翻面方式，看看能否叠成最高的书塔。

这个方法之所以 **正确**，是因为它遍历了题目要求的所有合法堆叠方式，必然能找到最优解。  

但显而易见，它的 **时间复杂度** 极其庞大：  
- 选子集：`2ⁿ`  
- 每个子集内部全排列：最坏情况下是 `n!`  
- 每个立方体的 6 种旋转：`6ⁿ`  

整体是 `O(2ⁿ * n! * 6ⁿ)`，在 `n ≤ 100` 时根本不可行。

**空间复杂度** 只需要保存递归栈和临时数组，约 `O(n)`。

#### 代码（Python）

```python
from itertools import combinations, permutations, product
from copy import deepcopy

def maxHeight_bruteforce(cuboids):
    n = len(cuboids)
    best = 0

    # 所有子集（从 1 到 n，空集高度为 0）
    for k in range(1, n + 1):
        for idx_set in combinations(range(n), k):
            chosen = [cuboids[i] for i in idx_set]

            # 对子集进行全排列（尝试所有放置顺序）
            for order in permutations(range(k)):
                # 依次尝试每个立方体的 6 种旋转
                # 用 product 生成每个立方体的所有可能旋转（6 种）
                rotations = [list(set(permutations(chosen[i]))) for i in order]
                for rot_comb in product(*rotations):
                    ok = True
                    total_h = 0
                    # 逐个检查能否堆叠
                    for i, dims in enumerate(rot_comb):
                        w, l, h = dims
                        total_h += h
                        if i > 0:
                            pw, pl, ph = prev
                            if w > pw or l > pl or h > ph:
                                ok = False
                                break
                        prev = dims
                    if ok:
                        best = max(best, total_h)
    return best
```

> 代码仅作概念演示，实际运行会因指数级复杂度而超时。

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n! * 6ⁿ)` —— 这是一种“爆炸性增长”，即使 `n=10` 也会非常慢。  
- **空间复杂度**：`O(n)` —— 只用到了若干临时数组和递归栈。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **两大瓶颈**：

1. **子集和全排列**：我们不需要枚举所有顺序，只要把立方体排成一种 **非递减** 的顺序（宽 ≤、长 ≤、高 ≤），后面的立方体自然可以放在前面的上面。  
2. **旋转**：每个立方体可以自由旋转，只要把 **三个维度按从小到大排序**，就固定了一种“标准姿势”。因为如果我们把宽、长、高分别定义为 **排序后的第 1、2、3 位**，那么在比较两块立方体时，只要这三个数都不大于对应的数，就一定能找到一种旋转方式让它们合法堆叠。

基于这两点，我们可以把问题转化为：

> **在所有立方体的“标准姿势”下，挑选一个子序列，使得序列中的每个立方体的三个维度都不小于前一个立方体的对应维度，且总高度最大。**

这正是 **“最长递增子序列（LIS）”** 的变形，只是这里的“递增”是三维的，并且我们要求 **高度之和最大** 而不是子序列长度。

实现步骤：

1. **标准化每个立方体**：对每个 `cuboids[i]` 进行升序排序，使得 `w ≤ l ≤ h`。这一步相当于把立方体“摆正”，以后比较时直接使用这三个数。  
2. **整体排序**：把所有标准化后的立方体按 **宽 → 长 → 高** 的字典序排序（即先比较宽，不同再比较长，仍不同再比较高）。排序后，若 `i < j`，则 `cuboid[i]` 的宽一定 ≤ `cuboid[j]` 的宽，长也可能 ≤，高也可能 ≤。这保证了我们只需要在已排好序的列表中向后查找合法堆叠，而不必回头。  
3. **动态规划**：设 `dp[i]` 为**以第 i 个立方体（排好序后）作为最上层时能够得到的最大总高度**。  
   - 初始化 `dp[i] = height_i`（单独放一个立方体的高度）。  
   - 对每个 `i`，遍历所有前面的 `j < i`，如果 `cuboid[j]` 的三个维度都 ≤ `cuboid[i]`（即 `j` 可以放在 `i` 下方），则可以把 `i` 放在 `j` 上面，更新  
     `dp[i] = max(dp[i], dp[j] + height_i)`。  
4. **答案**：所有 `dp[i]` 的最大值即为最高塔的高度。

> **类比**：把每个立方体想象成一本已经按照宽、长、厚排好序的书。我们想把书叠起来，规则是上一本的每个尺寸都不能比下一本大。动态规划就像在记录“以这本书为最上层的最高书塔有多高”。  

**为什么排序后 DP 能工作？**  
排序保证了如果 `j < i`，则 `width_j ≤ width_i`。只有当 **长和高** 也满足 ≤ 时，才可以堆叠。这样我们只需要检查前面的立方体，而不必考虑“跳回去”的情况，时间大幅下降。

#### 代码（Python）

```python
from typing import List

def maxHeight(cuboids: List[List[int]]) -> int:
    # 1. 每个立方体内部升序排列，确保 width <= length <= height
    norm = [sorted(c) for c in cuboids]          # 例如 [50,45,20] -> [20,45,50]

    # 2. 按三维字典序整体排序，保证宽从小到大
    norm.sort()                                  # Python 默认按列表的字典序比较

    n = len(norm)
    dp = [0] * n                                 # dp[i] = 以 i 为最上层的最大高度

    for i in range(n):
        w_i, l_i, h_i = norm[i]
        dp[i] = h_i                               # 单独放 i 时的高度
        # 检查所有可以放在 i 下方的 j
        for j in range(i):
            w_j, l_j, h_j = norm[j]
            if w_j <= w_i and l_j <= l_i and h_j <= h_i:
                # j 能放在 i 下方，尝试把 i 放在 j 上面
                dp[i] = max(dp[i], dp[j] + h_i)

    return max(dp)                               # 最高塔的总高度
```

**代码要点解释**  

- `sorted(c)`：把每个立方体的三条边从小到大排好，等价于“把立方体旋转到最有利的姿势”。  
- `norm.sort()`：整体排序后，后面的立方体宽一定不小于前面的，简化后续比较。  
- `if w_j <= w_i and l_j <= l_i and h_j <= h_i:`：检查三维是否都满足堆叠条件。  
- `dp[i] = max(dp[i], dp[j] + h_i)`：如果 `j` 能在 `i` 下方，则把 `i` 放在 `j` 的顶部，更新最高高度。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 排序 `O(n log n)`（相较于 `n²` 可以忽略）。  
  - 双层循环遍历每对立方体 `i, j`，共 `n·(n-1)/2` 次比较。  
  - 对于 `n ≤ 100`，`n² = 10⁴`，非常快。  
  - 与暴力解的指数级时间相比，提升巨大。  

- **空间复杂度**：`O(n)`  
  - 只需存储排序后的列表 `norm`（`n` 个 3 元组）和 `dp` 数组（长度 `n`）。  

---

## 心得  

- **核心技巧**：把每个立方体的三维先**升序标准化**，再**整体排序**，把多维堆叠问题转化为“一维”动态规划（类似最长递增子序列）。  
- **适用的题型**  
  1. “盒子堆叠（Box Stacking）” 类似问题，需要先对每个盒子旋转后排序。  
  2. “俄罗斯套娃（Russian Doll Envelopes）”——在二维上使用 LIS。  
  3. “矩形的最大嵌套数”——同样先排序后 DP/LIS。  
- **一句话总结解题钥匙**：**先把所有立方体统一“正面”，再按宽-长-高排序，用 DP 求最大递增子序列的高度和**。

---

## 反思  

- **第一反应**：直接想枚举所有子集和排列，忽视了立方体可以旋转的特性导致搜索空间巨大。  
- **最容易踩的坑**  
  - **忘记对每个立方体内部排序**：如果不把三维升序，后面的比较会漏掉合法的旋转方式。  
  - **排序时的比较顺序**：必须使用宽 → 长 → 高的字典序，否则可能出现 `width` 相等但 `length` 逆序的情况，导致 DP 误判。  
  - **高度的累加**：DP 中只能累加当前立方体的 **height（已排序后的第三维）**，不能把宽或长当作高度。  
- **下次类似题的第一步**：**把每个物体的维度统一排序（标准化）**，然后 **整体排序**，再考虑使用 **LIS / DP** 求解最大可堆叠/嵌套的总量。