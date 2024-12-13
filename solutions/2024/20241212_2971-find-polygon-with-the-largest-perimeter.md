# #2971. 寻找最大周长的多边形 / Find Polygon With the Largest Perimeter

> 难度：中等 · 标签：Array、Greedy、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-polygon-with-the-largest-perimeter/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums of length n.
A polygon is a closed plane figure that has at least 3 sides. The longest side of a polygon is smaller than the sum of its other sides.
Conversely, if you have k (k >= 3) positive real numbers a1, a2, a3, ..., ak where a1 <= a2 <= a3 <= ... <= ak and a1 + a2 + a3 + ... + ak-1 > ak, then there always exists a polygon with k sides whose lengths are a1, a2, a3, ..., ak.
The perimeter of a polygon is the sum of lengths of its sides.
Return the largest possible perimeter of a polygon whose sides can be formed from nums, or -1 if it is not possible to create a polygon.

**Examples**

**Example 1:**

```
Input: nums = [5,5,5]
Output: 15
Explanation: The only possible polygon that can be made from nums has 3 sides: 5, 5, and 5. The perimeter is 5 + 5 + 5 = 15.
```

**Example 2:**

```
Input: nums = [1,12,1,2,5,50,3]
Output: 12
Explanation: The polygon with the largest perimeter which can be made from nums has 5 sides: 1, 1, 2, 3, and 5. The perimeter is 1 + 1 + 2 + 3 + 5 = 12.
We cannot have a polygon with either 12 or 50 as the longest side because it is not possible to include 2 or more smaller sides that have a greater sum than either of them.
It can be shown that the largest possible perimeter is 12.
```

**Example 3:**

```
Input: nums = [5,5,50]
Output: -1
Explanation: There is no possible way to form a polygon from nums, as a polygon has at least 3 sides and 50 > 5 + 5.
```

**Constraints**

- 3 <= n <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个长度为 `n` 的正整数数组 `nums`。  
**多边形 (polygon)** 是一种闭合的平面图形，至少有 3 条边。多边形的最长边必须小于其他所有边长度之和。  
反过来，如果你有 `k (k ≥ 3)` 个正实数 `a₁ ≤ a₂ ≤ a₃ ≤ … ≤ a_k`，且满足 `a₁ + a₂ + … + a_{k-1} > a_k`，则必定可以构造出一条具有这 `k` 条边长的多边形。  
**周长 (perimeter)** 是多边形所有边长的总和。  
返回可以从 `nums` 中选取若干边长组成的多边形的最大可能 **周长**，如果无法构成任何多边形则返回 `-1`。

**示例 1**  
**输入**: `nums = [5,5,5]`  
**输出**: `15`  
**解释**: 唯一可以用 `nums` 构造的多边形只有 3 条边，长度分别为 5、5、5。其 **周长** 为 `5 + 5 + 5 = 15`。

**示例 2**  
**输入**: `nums = [1,12,1,2,5,50,3]`  
**输出**: `12`  
**解释**: 可以构成最大 **周长** 的多边形有 5 条边，长度分别为 `1, 1, 2, 3, 5`。其 **周长** 为 `1 + 1 + 2 + 3 + 5 = 12`。  
无法以 `12` 或 `50` 为最长边构成多边形，因为不存在两条或更多更短的边使其长度之和大于这两条最长边。

**示例 3**  
**输入**: `nums = [5,5,50]`  
**输出**: `-1`  
**解释**: 无法用 `nums` 构成任何多边形，因为多边形至少需要 3 条边，而 `50 > 5 + 5`。

**约束条件**  
- `3 ≤ n ≤ 10⁵`  
- `1 ≤ nums[i] ≤ 10⁹`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有可能的选边组合都枚举一遍」，然后检查每一种组合是否能组成多边形，能的话就算出它的周长，最后取最大值。

- **数据结构**：我们只需要一个普通的 Python `list` 保存当前组合的边长。  
  把「所有组合」想象成「一本装满各种配料的菜谱」——每一页（子集）记录了一种可能的配料（边长）组合。

- **为什么正确**：  
  题目说，只要满足「最长边 < 其余所有边之和」就一定能拼成多边形。遍历**所有**子集，自然不会漏掉任何合法的配料组合，所以一定能得到最大周长。

- **复杂度分析（大白话）**：  
  - **时间**：`n` 个数的子集有 `2ⁿ` 种（每个数要么选要么不选），每检查一次需要把子集里的数加起来并找出最大值，最坏情况下要遍历子集中的全部 `n` 个数。于是时间是 `O(n·2ⁿ)`，也就是「指数级」——随着 `n` 增大会很快爆炸。  
  - **空间**：递归或位运算时需要保存当前子集的临时列表，最多 `O(n)`（因为子集最多 `n` 个元素），这在这里可以算是「线性」的。

> **提示**：这种解法只能在 `n ≤ 20` 左右的小样例上跑得动，远远不够满足题目 `n ≤ 10⁵` 的要求，只是帮助我们先理清「什么是合法」的概念。

#### 代码（Python）

```python
from typing import List

def largest_perimeter_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best = -1                                 # 记录目前找到的最大周长
    # 用位运算枚举所有子集（不包括空集和只有 1、2 条边的情况）
    for mask in range(1 << n):
        # 统计子集里选了多少条边
        cnt = mask.bit_count()
        if cnt < 3:               # 多边形至少需要 3 条边
            continue

        sides = []                # 当前子集的所有边长
        total = 0                 # 边长和
        longest = 0               # 当前子集的最长边
        for i in range(n):
            if mask >> i & 1:     # 第 i 条边被选中
                v = nums[i]
                sides.append(v)
                total += v
                if v > longest:
                    longest = v

        # 判断「最长边 < 其余边之和」是否成立
        if total - longest > longest:
            best = max(best, total)   # 更新最大周长

    return best
```

> 关键行注释已用中文标明。运行时请注意 `n` 较大时会非常慢。

#### 复杂度

- **时间复杂度**：`O(n·2ⁿ)`  
  - `2ⁿ` 是所有子集的数量，`n` 是每次遍历子集时累加求和的代价。可以把它想象成「每次都要把所有水果都搬一遍」——水果越多，搬运的工作量呈指数增长。

- **空间复杂度**：`O(n)`  
  - 只需要保存当前子集的边长列表，最多 `n` 个数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈**是「我们把所有子集都枚举了」，但实际上我们只需要找 **一个**满足条件的「最大」子集即可。观察以下两个事实：

1. **把所有小于等于最长边的边都选上**，永远不会让答案变差。  
   - 类比：想象你在做三明治，已经决定了最大的面包片（最长边），把所有能放进去的配料（更短的边）都加进去，只会让三明治更大、更好吃，而不会让它塌下来。因为条件是「最长边 < 其余所有边之和」，加入更多（且不超过最长边的）边只会让右边的和更大。

2. **只要把最长边定下来，判断是否可行就只需要比较一次**：  
   - 把所有**不大于**这个最长边的边的总长度 `sum_rest` 与 `longest` 比较，若 `sum_rest > longest`，则 **整个集合**（包括这条最长边）就已经是合法的多边形，且周长是最大的（因为我们已经用了所有可能的边）。  
   - 若不满足，则这条最长边 **必定不能出现在答案里**，因为连所有更短的边都不足以超过它。于是我们把它丢掉，继续把次大的边当作「最长边」再检查。

基于这两个观察，我们可以得到 **贪心 + 排序** 的线性扫描算法：

1. **排序**：把 `nums` 从小到大排列。  
   - 排序后，`nums[i]` 就是第 `i` 小的边，`nums[-1]` 是最大的边。排序相当于把所有边排成一条长队，最短的在前，最长的在后，方便我们「从后往前」依次「踢掉」不合格的最长边。

2. **从后往前累加**：  
   - 先计算所有边的总和 `total_sum`。  
   - 从最大的边向前遍历（下标 `i` 从 `n-1` 到 `2`），每一步检查 `total_sum - nums[i] > nums[i]`（即「其余边之和」是否大于「当前最长边」）。  
   - 若成立，说明 **包括从 `0` 到 `i` 的所有边** 已经可以组成多边形，且已经用了尽可能多的边，周长就是 `total_sum`，直接返回。  
   - 若不成立，说明 `nums[i]` 必须被排除，于是把它从 `total_sum` 中减去，继续检查下一个更小的候选最长边。

3. **遍历结束仍未成功**，说明没有任何合法的三条或以上的边，返回 `-1`。

> **核心概念解释**  
> - **贪心**：每一步都「尽可能选最多的边」而不考虑以后会怎样，因为我们已经证明「多选不会让条件变坏」；  
> - **前缀和/后缀和**：这里的 `total_sum` 相当于「从左到右的前缀和的最后一个值」；在遍历过程中不断「去掉」最右侧的元素，相当于在维护「当前后缀的和」。

#### 代码（Python）

```python
from typing import List

def largest_perimeter(nums: List[int]) -> int:
    """
    贪心 + 排序
    1. 将所有边从小到大排序
    2. 从最大的边开始往前尝试，把不满足条件的最长边逐个剔除
    3. 第一次出现 “其余边之和 > 最长边” 时即得到最大周长
    """
    nums.sort()                     # 小到大排好队
    total = sum(nums)               # 所有边的总长度

    # 从最大的边往前检查（i 必须 >= 2，保证至少还有 2 条更短的边）
    for i in range(len(nums) - 1, 1, -1):
        longest = nums[i]           # 当前候选的最长边
        rest = total - longest      # 其余所有边的长度和
        # 条件：其余边之和 必须 大于 最长边
        if rest > longest:
            return total            # 此时 total 已经是最大可能周长
        # 否则 longest 不能用，剔除它
        total -= longest

    # 没有任何合法的多边形
    return -1
```

> 关键行已加中文注释，代码可直接运行。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `n log n` 来自排序（把所有边排好队）。随后只进行一次线性遍历 `O(n)`，相当于「排完队后只走一遍队列」——远比指数级快得多。  
  - 与暴力解相比，时间从「指数级」降到了「对数级」乘以线性，几乎可以在 `10⁵` 的规模下瞬间完成。

- **空间复杂度**：`O(1)`（不计排序本身的原地修改）  
  - 只用了几个整数变量 `total、longest、rest`，不随 `n` 增长而增长。可以把它想象成「只在手里握着几支笔」而不是「把所有书都搬进来」。

---

## 心得

- **核心技巧**：**排序 + 贪心** —— 先把所有候选边排好序，再从最大的边开始「逐个剔除」直到满足「最长边 < 其余边之和」的条件。  
- **此技巧适用的题型**  
  1. **最长/最短三角形/多边形**（如 LeetCode 976 “Largest Perimeter Triangle”）  
  2. **选取最大子集满足某种“和大于最大元素”约束**（如“最大可行团队规模”）  
  3. **背包类的贪心优化**（如“最大长度的木棍可以围成矩形”）  
- **一句话总结**：  
  > “把所有边排好队，先把最大的边挑出来，若它被所有更短的边“压倒”了，就把它踢出队列；第一次成功时的总长度就是答案。”

---

## 反思

- **拿到题目第一反应**：  
  想到了「枚举所有子集」的暴力思路，随后意识到这会超时，必须找出只检查少数几种情况的办法。

- **最容易踩的坑**  
  1. **忽略最少 3 条边的限制**——即使某两个边满足 `a + b > c`，仍然不足以构成多边形。代码中必须确保 `i ≥ 2`（即至少保留 3 条边）才进行检查。  
  2. **整数溢出**（在某些语言中）——`sum(nums)` 可能达到 `10⁵ * 10⁹ = 10¹⁴`，在 Python 不会溢出，但在 C/C++ 需要使用 `long long`。  
  3. **忘记排序**——如果不先排序，直接从任意顺序的数组里挑最长边进行比较，可能会误把一个大边当成「当前最长」而遗漏更大的边。

- **下次遇到同类题，第一步该想到**  
  > “把所有数从小到大排好序，然后从最大的数开始，检查‘其余数之和’是否能‘压倒’它——如果不能，就把它剔除继续往前”。这一步几乎把问题转化为一次线性扫描，后面的实现自然水到渠成。