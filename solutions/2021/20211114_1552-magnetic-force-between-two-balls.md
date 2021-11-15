# #1552. 两个球之间的磁力 / Magnetic Force Between Two Balls

> 难度：中等 · 标签：Array、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/magnetic-force-between-two-balls/)

---

## 题目（英文原版）

**Description**

In the universe Earth C-137, Rick discovered a special form of magnetic force between two balls if they are put in his new invented basket. Rick has n empty baskets, the ith basket is at position[i], Morty has m balls and needs to distribute the balls into the baskets such that the minimum magnetic force between any two balls is maximum.
Rick stated that magnetic force between two different balls at positions x and y is |x - y|.
Given the integer array position and the integer m. Return the required force.

**Examples**

**Example 1:**

```
Input: position = [1,2,3,4,7], m = 3
Output: 3
Explanation: Distributing the 3 balls into baskets 1, 4 and 7 will make the magnetic force between ball pairs [3, 3, 6]. The minimum magnetic force is 3. We cannot achieve a larger minimum magnetic force than 3.
```

**Example 2:**

```
Input: position = [5,4,3,2,1,1000000000], m = 2
Output: 999999999
Explanation: We can use baskets 1 and 1000000000.
```

**Constraints**

- n == position.length
- 2 <= n <= 105
- 1 <= position[i] <= 109
- All integers in position are distinct.
- 2 <= m <= position.length

---

## 题目（中文翻译）

**题目描述**  
在宇宙 **Earth C-137** 中，Rick 发现如果把两个球放进他新发明的篮子里，会产生一种特殊的磁力（magnetic force）。Rick 拥有 `n` 个空篮子，第 `i` 个篮子位于 `position[i]` 处；Morty 有 `m` 个球，需要将这些球分配到篮子中，使得任意两个球之间的最小磁力最大化。  
Rick 给出的磁力定义为：位于位置 `x` 与 `y` 的两个不同球之间的磁力等于 `|x - y|`。  
给定整数数组 `position` 和整数 `m`，返回能够实现的最大最小磁力值。

**示例**  

示例 1  
```
Input: position = [1,2,3,4,7], m = 3
Output: 3
Explanation: 将 3 个球分别放入篮子 1、4、7，可得到球对之间的磁力为 [3, 3, 6]。其中最小的磁力为 3，无法得到更大的最小磁力。
```

示例 2  
```
Input: position = [5,4,3,2,1,1000000000], m = 2
Output: 999999999
Explanation: 可以选择篮子 1 和 1000000000。
```

**约束条件**  

- `n == position.length`
- `2 <= n <= 10^5`
- `1 <= position[i] <= 10^9`
- `position` 中的所有整数互不相同
- `2 <= m <= position.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `m` 个球全部放进所有可能的篮子组合里，遍历每一种放置方式，算出每对球之间的磁力（其实就是它们位置的距离），取这一次放置的 **最小磁力**，再在所有放置方式中挑出 **最大的最小磁力**。

- **数据结构**：  
  - `position` 数组本身就是一排篮子的位置。  
  - 组合可以用 **列表** 保存每次选中的篮子下标，类似“从字典里挑单词”，把每个组合看成字典的一个条目。  
- **为什么正确**：  
  - 只要把所有合法的放球方式都枚举一遍，就一定能找到让“最小磁力最大化”的那一种。  
- **时间/空间复杂度**：  
  - 组合数是 `C(n, m)`（从 `n` 个篮子里挑 `m` 个），这在最坏情况下会是指数级别的，比如 `n=20, m=10` 时就有上百万种组合。  
  - 对每一种组合我们都要算 `m·(m-1)/2` 对距离，时间大约是 `O(C(n,m) * m²)`。  
  - 空间只需要保存当前组合，`O(m)`，但因为组合数巨大，整体上是 **不可接受** 的。  

> **大白话解释**：  
> - `O(n²)` 就是“n 乘以 n”，比如 `n=1000` 时相当于要做 1 000 000 次操作。这里的 `C(n,m)` 甚至比 `n²` 还要大，根本跑不动。

#### 代码（Python）

```python
import itertools
from typing import List

def max_min_force_bruteforce(position: List[int], m: int) -> int:
    # 先把篮子位置排好序，后面算距离更直观
    pos = sorted(position)

    best = 0                     # 记录目前找到的最大“最小磁力”
    # 枚举所有选取 m 个篮子的组合
    for combo in itertools.combinations(pos, m):
        # 计算该组合里任意两球之间的距离的最小值
        min_force = min(abs(combo[i] - combo[j])
                        for i in range(m) for j in range(i + 1, m))
        best = max(best, min_force)   # 取最大值
    return best
```

> 这段代码只能在 `n` 很小（比如 `n≤15`）时跑得完。

#### 复杂度

- **时间复杂度**：`O(C(n,m) * m²)` —— 组合数乘以每组内部两两比较的次数，极其庞大，实际不可用。  
- **空间复杂度**：`O(m)` —— 只存当前选中的 `m` 个位置。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**枚举所有放置方式**。其实我们不需要真的把球放出来，只要判断“**给定一个磁力阈值 x**，能否把 `m` 球放进篮子，使得任意两球距离 ≥ x””。如果能，那说明答案至少是 `x`；如果不能，答案肯定小于 `x`。这正好满足**单调性**，于是可以在答案空间上做二分搜索。

**关键点 1：单调性**  
> 如果把球间最小距离设为 `x` 能成功放球，那么把距离设为更小的 `y (< x)` 肯定也能成功（因为约束更宽松了）。反之，若 `x` 放不下，则更大的 `y` 也放不下。

**关键点 2：贪心判定**  
给定阈值 `x`，我们想快速判断是否可行。把篮子位置从小到大排好序，然后**从左到右依次放球**：  
1. 第一个球放在最左边的篮子。  
2. 之后的每个球，必须放在距离上一个已放球 **至少 x** 的最左篮子。  
如果最终能放下 `m` 球，说明 `x` 可行；否则不可行。

这种“最左放”是贪心的，因为把球往左放不会妨碍后面的球更容易满足距离要求，反而会为后面的球留出更大的空间。

**关键点 3：二分搜索答案**  
- **搜索范围**：最小可能的磁力是 `1`（位置是整数且互不相同），最大可能的磁力是 `max(position) - min(position)`（把球分别放在最左和最右的篮子）。  
- **二分过程**：取中间值 `mid`，用贪心判定能否放下 `m` 球。若能，说明答案至少是 `mid`，于是把左边界移动到 `mid+1`；若不能，右边界移动到 `mid-1`。循环结束时，右边界恰好是最大的可行磁力。

**核心算法/数据结构解释**  

- **二分搜索**：想象在一本有序的字典里找某个词的页码，我们每次先看中间的页码，如果目标词在左边就往左找，右边就往右找。这里的“有序”体现在答案随阈值单调递增/递减。  
- **贪心**：把球放在最左边符合要求的篮子，就像排队买票时总是选择最早的空位，保证后面的人还有机会。

#### 代码（Python）

```python
from typing import List

def max_min_force(position: List[int], m: int) -> int:
    """
    二分答案 + 贪心判定
    返回能够让任意两球距离的最小值尽可能大的那个值
    """
    # 1. 排序，方便后面从左到右放球
    pos = sorted(position)

    # 2. 判定函数：给定距离 d，能否放下 m 球？
    def can_place(d: int) -> bool:
        # 第一个球放在最左边
        count = 1
        last = pos[0]                # 记录上一个已放球的位置
        for p in pos[1:]:
            if p - last >= d:        # 与上一个球的距离满足要求
                count += 1
                last = p
                if count == m:       # 已经放够 m 球，直接返回 True
                    return True
        return False                 # 遍历结束仍未放够

    # 3. 二分搜索答案区间
    left, right = 1, pos[-1] - pos[0]   # 最小可能是 1，最大是最左最右之差
    ans = 0
    while left <= right:
        mid = (left + right) // 2      # 取中间值，尝试这个距离
        if can_place(mid):             # 若能放下，则答案至少是 mid
            ans = mid                   # 记录下来，继续尝试更大的距离
            left = mid + 1
        else:                           # 放不下，说明距离太大，需要缩小
            right = mid - 1
    return ans
```

> 代码中每一行都配有中文注释，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n log D)`  
  - `n` 是篮子数量（`len(position)`），因为每次二分判断 `can_place` 都要遍历一次数组。  
  - `log D` 是答案范围的二分次数，`D = max(position) - min(position)`，最大约为 `10⁹`，所以 `log₂(10⁹) ≈ 30`。  
  - **大白话**：最多只会遍历 30 次整条篮子列表，完全可以接受（即使 `n=10⁵` 也只要几百万次基本操作）。
- **空间复杂度**：`O(1)`（不计输入数组本身）——只用了几个整数变量，额外空间常数级。

---

## 心得

- **核心技巧**：**二分搜索答案 + 贪心判定**。先把问题转化为“给定阈值能否实现”，利用单调性做二分；在判定子问题时，用最左放的贪心策略快速验证可行性。  
- **适用题型**：  
  1. “在数组中放置 k 个元素，使得相邻元素距离最大”——如 LeetCode 1552. **磁力最大化**（本题）。  
  2. “在 N 条路线上放置 K 个仓库，使得最远的客户距离最小”——类似**分配仓库**问题。  
  3. “把 K 根绳子切成段，使得最短段长度最大”——**划分数组**类问题。  
- **一句话总结解题钥匙**：**把“最大化最小值”转成“判断阈值可行性”，利用二分+贪心即可高效求解。**

---

## 反思

- **第一反应**：看到“最大化最小磁力”，立刻想到二分搜索，因为答案随阈值单调。  
- **最容易踩的坑**：  
  - 忘记先对 `position` 排序，导致贪心判定出错。  
  - 二分的左右边界写反，或循环条件写成 `while left < right` 导致遗漏最大可行值。  
  - 判定函数里没有提前返回 `True`（当已经放够 `m` 球时），会导致不必要的遍历，稍微影响性能。  
- **下次遇到同类题**：第一步立刻问自己“**答案是否满足单调性**”，如果是，就准备**二分答案**；接着思考**在固定阈值下如何快速验证**（往往是贪心或前缀和等线性扫描）。这样可以把搜索空间从指数级压到对数级。