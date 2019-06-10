# #452. 射爆气球的最少箭数 / Minimum Number of Arrows to Burst Balloons

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)

---

## 题目（英文原版）

**Description**

There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array points where points[i] = [xstart, xend] denotes a balloon whose horizontal diameter stretches between xstart and xend. You do not know the exact y-coordinates of the balloons.
Arrows can be shot up directly vertically (in the positive y-direction) from different points along the x-axis. A balloon with xstart and xend is burst by an arrow shot at x if xstart <= x <= xend. There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.
Given the array points, return the minimum number of arrows that must be shot to burst all balloons.

**Examples**

**Example 1:**

```
Input: points = [[10,16],[2,8],[1,6],[7,12]]
Output: 2
Explanation: The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
- Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].
```

**Example 2:**

```
Input: points = [[1,2],[3,4],[5,6],[7,8]]
Output: 4
Explanation: One arrow needs to be shot for each balloon for a total of 4 arrows.
```

**Example 3:**

```
Input: points = [[1,2],[2,3],[3,4],[4,5]]
Output: 2
Explanation: The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 2, bursting the balloons [1,2] and [2,3].
- Shoot an arrow at x = 4, bursting the balloons [3,4] and [4,5].
```

**Constraints**

- 1 <= points.length <= 105
- points[i].length == 2
- -231 <= xstart < xend <= 231 - 1

---

## 题目（中文翻译）

描述  
有若干个球形气球（balloon）贴在表示 XY 平面的平面墙上。气球用一个二维整数数组 `points` 表示，其中 `points[i] = [xStart, xEnd]` 表示一个气球的水平直径在 `xStart` 与 `xEnd` 之间。你不知道这些气球的具体 y 坐标。  

可以从 x 轴上的不同位置向正 y 方向（垂直向上）射出箭矢（arrow）。若射出的箭矢的 x 坐标为 `x`，满足 `xStart ≤ x ≤ xEnd`，则该气球会被击中并爆裂。射出的箭矢没有数量限制，且射出后会无限向上飞行，沿途会击中所有满足条件的气球。  

给定数组 `points`，返回必须射出的最少箭矢数量，使所有气球全部爆裂。

示例  

示例 1  
输入: `points = [[10,16],[2,8],[1,6],[7,12]]`  
输出: `2`  
解释: 可以用 2 支箭矢爆裂所有气球:  
- 在 `x = 6` 处射出一支箭，爆裂气球 `[2,8]` 和 `[1,6]`。  
- 在 `x = 11` 处射出一支箭，爆裂气球 `[10,16]` 和 `[7,12]`。

示例 2  
输入: `points = [[1,2],[3,4],[5,6],[7,8]]`  
输出: `4`  
解释: 每个气球都需要单独射出一支箭，共计 4 支。

示例 3  
输入: `points = [[1,2],[2,3],[3,4],[4,5]]`  
输出: `2`  
解释: 可以用 2 支箭矢爆裂所有气球:  
- 在 `x = 2` 处射出一支箭，爆裂气球 `[1,2]` 和 `[2,3]`。  
- 在 `x = 4` 处射出一支箭，爆裂气球 `[3,4]` 和 `[4,5]`。

约束条件  
- `1 ≤ points.length ≤ 10^5`  
- `points[i].length == 2`  
- `-2^31 ≤ xStart < xEnd ≤ 2^31 - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个气球都单独用一支箭射掉**。  
可以把每根箭想成一根“笔”，从某个 `x` 位置向上划一道直线，只要这根笔经过气球的区间 `[x_start, x_end]`，气球就会被扎破。  
如果我们不考虑任何“共享”机会，而是对每个气球都新开一根笔，那么显然所有气球都会被射爆——因为每根笔必定落在对应气球的区间内。

> **为什么这个方法一定对？**  
> 因为题目只要求把所有气球都弄破，没说必须最少使用箭。只要每个气球都对应一根箭，必然满足条件。

> **时间/空间复杂度**  
> - **时间**：我们只需要遍历一次 `points`，对每个气球执行常数次操作（新建一根箭），所以是 **O(n)**。  
>   这里的 `O(n)` 可以读作“数量级为 `n`”，也就是说如果有 10 000 个气球，程序大约会执行 10 000 次主要操作。  
> - **空间**：只用到几个计数变量，和 `n` 无关，记作 **O(1)**（常数级），即不管气球多少，额外占用的内存几乎不变。

#### 代码（Python）

```python
def findMinArrowShots_bruteforce(points):
    """
    暴力思路：每个气球都用一支独立的箭
    时间复杂度 O(n)，空间复杂度 O(1)
    """
    # 箭的数量直接等于气球的数量
    return len(points)
```

#### 复杂度

- **时间复杂度**：O(n) — 线性遍历一次列表，操作次数随气球数量线性增长。  
- **空间复杂度**：O(1) — 只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**我们总是可以把多支箭合并成更少的箭**，只要它们的射击位置能够同时落在多个气球的区间交集里。  
要找最少的箭，核心是**尽可能多地让一支箭覆盖相邻的气球**。这类“覆盖区间”的问题常用**贪心（Greedy）**策略来解决。

**慢在哪里？**  
暴力解没有利用气球之间的重叠信息，每个气球都单独算一根箭，导致答案远远不是最小。

**一步步推导优化思路**  

1. **把气球按照右端点 `x_end` 从小到大排好序**。  
   - 想象每个气球是一根横向的木条，右端点越靠左的木条先摆好，后面的木条如果左端点在它右端点左边，就可以被同一根箭一起射爆。  
   - 排序后，左端点较大的气球一定在右端点较大的气球后面出现，这样我们只需要看当前箭的射击位置是否还能覆盖下一个气球。

2. **维护一个“当前箭射击位置”**，初始设为第一个气球的右端点 `end`。  
   - 为什么取右端点？因为我们希望这根箭尽可能向左靠近，以便后面的气球（右端点更大）仍然能够被覆盖。  
   - 当遍历到下一个气球 `[s, e]` 时：  
     - **如果 `s` ≤ `end`**，说明这个气球的左端点在当前箭的射击位置左侧或正好在上，两个区间有交集，**同一根箭就能扎破**，`end` 不需要改变。  
     - **否则**（`s` > `end`），当前箭已经射不到这个气球了，需要**新起一根箭**，把射击位置更新为这个气球的右端点 `e`。

3. **遍历结束后，箭的计数即为答案**。

> **核心算法/数据结构**  
> - **排序（Sorting）**：把区间按右端点升序排列。  
> - **贪心（Greedy）**：每次尽量让当前箭射到最左的可行位置（即当前区间的右端点），从而最大化后续区间的覆盖可能。

> **类比**  
> 把每根箭想成一把“剪刀”。我们把所有气球的区间排好队，让剪刀从最左侧的气球“切”起，剪到右端点为止。只要后面的气球的左端点在剪刀的切割范围内，就不需要再换剪刀，直接一起“切”。一旦出现左端点在剪刀右侧的气球，就必须换一把新剪刀继续。

#### 代码（Python）

```python
def findMinArrowShots(points):
    """
    贪心解法：先按右端点排序，然后用最少的箭覆盖所有区间
    时间复杂度 O(n log n) —— 排序是最耗时的步骤
    空间复杂度 O(1)      —— 只使用常数个额外变量（不计输入本身）
    """
    if not points:               # 防止空列表导致错误
        return 0

    # 1. 按区间的右端点升序排列
    #   类比：把所有木条从最左的右端点排成一列，最左的先放好
    points.sort(key=lambda x: x[1])

    arrows = 1                    # 至少需要一根箭射第一个气球
    current_end = points[0][1]    # 第一次射击的位置定在第一个气球的右端点

    # 2. 逐个检查后面的气球
    for start, end in points[1:]:
        if start > current_end:   # 这根箭射不到，必须重新射一根
            arrows += 1
            current_end = end    # 新的射击位置定位在当前气球的右端点
        # else: 仍然在覆盖范围内，不需要增加箭，保持 current_end 不变

    return arrows
```

#### 复杂度

- **时间复杂度**：O(n log n) — “n log n” 可以理解为“先把 n 条气球排好序，需要 n 次比较，每次比较的成本大约是 log n（约等于把 n 条信息分层查找的次数）”。这一步是所有步骤里最耗时的，后面的遍历是线性的 O(n)。  
- **空间复杂度**：O(1) — 只用了几个整数变量 `arrows`、`current_end`，不随气球数量增加而增长（如果算 Python 的原地排序，需要 O(log n) 的递归栈空间，但通常我们写成 O(1)）。

---

## 心得

- **核心技巧**：先按右端点排序，再用贪心一次遍历找最小覆盖数。  
- **适用的题型**  
  1. “区间调度”类问题（如 **Maximum Number of Non‑Overlapping Intervals**）。  
  2. “最少移动次数使区间相交”类问题（如 **Minimum Number of Platforms Required**）。  
  3. “最少覆盖点”类问题（如 **Set Intersection Size At Least Two**）。  
- **一句话总结解题钥匙**：**“把区间按右端点排好，尽量让每根箭停在最左的右端点”。**

---

## 反思

- **第一反应**：看到每个气球都是一个 `[x_start, x_end]` 区间，就想到“区间覆盖”或“区间调度”这类经典模型。  
- **最容易踩的坑**  
  - **忘记排序**：直接按原顺序遍历会错失很多可以共享的箭。  
  - **处理重叠边界**：题目要求 `x_start <= x <= x_end`，所以当下一个区间的左端点恰好等于当前箭的射击位置时，仍然可以用同一根箭，判断条件要写成 `start > current_end`（而不是 `>=`）。  
  - **空输入**：虽然约束里 `points.length ≥ 1`，但写代码时最好防御性地检查空列表。  
- **下次遇到同类题**：第一步就**把所有区间按右端点排序**，然后用**贪心**遍历寻找最小覆盖集合。这样可以把思路快速锁定在正确的方向上。