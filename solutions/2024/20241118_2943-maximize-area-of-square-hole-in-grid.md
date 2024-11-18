# #2943. **网格中方形孔的最大面积** / Maximize Area of Square Hole in Grid

> 难度：中等 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-area-of-square-hole-in-grid/)

---

## 题目（英文原版）

**Description**

You are given the two integers, n and m and two integer arrays, hBars and vBars. The grid has n + 2 horizontal and m + 2 vertical bars, creating 1 x 1 unit cells. The bars are indexed starting from 1.
You can remove some of the bars in hBars from horizontal bars and some of the bars in vBars from vertical bars. Note that other bars are fixed and cannot be removed.
Return an integer denoting the maximum area of a square-shaped hole in the grid, after removing some bars (possibly none).

**Examples**

**Example 1:**

```
Input: n = 2, m = 1, hBars = [2,3], vBars = [2]
Output: 4
Explanation:
The left image shows the initial grid formed by the bars. The horizontal bars are [1,2,3,4] , and the vertical bars are [1,2,3] .
One way to get the maximum square-shaped hole is by removing horizontal bar 2 and vertical bar 2.
```

**Example 2:**

```
Input: n = 1, m = 1, hBars = [2], vBars = [2]
Output: 4
Explanation:
To get the maximum square-shaped hole, we remove horizontal bar 2 and vertical bar 2.
```

**Example 3:**

```
Input: n = 2, m = 3, hBars = [2,3], vBars = [2,4]
Output: 4
Explanation:
One way to get the maximum square-shaped hole is by removing horizontal bar 3, and vertical bar 4.
```

**Constraints**

- 1 <= n <= 109
- 1 <= m <= 109
- 1 <= hBars.length <= 100
- 2 <= hBars[i] <= n + 1
- 1 <= vBars.length <= 100
- 2 <= vBars[i] <= m + 1
- All values in hBars are distinct.
- All values in vBars are distinct.

---

## 题目（中文翻译）

你得到两个整数 `n` 和 `m`，以及两个整数数组 `hBars` 和 `vBars`。网格由 `n + 2` 条水平杆（horizontal bars）和 `m + 2` 条垂直杆（vertical bars）组成，形成大小为 `1 × 1` 的单元格。杆的编号从 `1` 开始。

你可以移除 `hBars` 中指定的部分水平杆，以及 `vBars` 中指定的部分垂直杆。注意，未在这两个数组中的其他杆是固定的，不能被移除。

返回一个整数，表示在移除若干杆（也可能不移除）后，网格中能够形成的最大**正方形孔**（square-shaped hole）的面积。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= n <= 10^9`
- `1 <= m <= 10^9`
- `1 <= hBars.length <= 100`
- `2 <= hBars[i] <= n + 1`
- `1 <= vBars.length <= 100`
- `2 <= vBars[i] <= m + 1`
- `hBars` 中的所有值互不相同。
- `vBars` 中的所有值互不相同。

**示例**

**示例 1:**  
```
Input: n = 2, m = 1, hBars = [2,3], vBars = [2]
Output: 4
```
**解释:**  
左图展示了由杆构成的初始网格。水平杆为 `[1,2,3,4]`，垂直杆为 `[1,2,3]`。一种得到最大正方形孔的方法是移除水平杆 `2` 和垂直杆 `2`。

**示例 2:**  
```
Input: n = 1, m = 1, hBars = [2], vBars = [2]
Output: 4
```
**解释:**  
要得到最大正方形孔，移除水平杆 `2` 和垂直杆 `2`。

**示例 3:**  
```
Input: n = 2, m = 3, hBars = [2,3], vBars = [2,4]
Output: 4
```
**解释:**  
一种得到最大正方形孔的方法是移除水平杆 `3` 和垂直杆 `4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把整个网格想象成一张纸，上面画了很多条横线（水平柱子）和竖线（垂直柱子），这些线把纸划分成一个个 1×1 的小格子。  
题目只允许我们把 **能够被删除的** 那些横线或竖线摘掉，其他的线是固定的，不能动。

> **目标**：摘掉若干横线和竖线后，形成一个最大的 **正方形空洞**（即正方形区域里没有任何线），返回它的面积。

最直观的想法是：**枚举所有可能的正方形位置**，看能否通过删除允许的线得到它。  
具体做法：

1. 把所有横线的编号记在一个数组 `all_h = [1, 2, …, n+2]`，同理所有竖线记在 `all_v = [1, 2, …, m+2]`。其中编号 `1` 和 `n+2`（或 `m+2`）是网格的最外层边界，**永远不能被删除**。
2. 对横线：枚举任意两根**保留下来的**横线 `top`、`bottom`（它们可以是外层边界，也可以是我们没有删除的内部线）。如果在这两根线之间的所有内部横线（`top+1 … bottom-1`）**全部都在 `hBars` 中**，说明我们可以把它们全部摘掉，形成一段连续的缺口，缺口的高度等于 `bottom - top`.
3. 对竖线同理，得到每一段可形成的缺口宽度 `right - left`。
4. 把每一段可形成的高度和宽度配对，取 `side = min(height, width)`，因为正方形的边长不能超过任意一方向的缺口长度。把 `side²` 记录下来，取最大值即为答案。

> **类比**：把 `hBars` 想成一本字典里可以随意翻开的页码，只有这些页码对应的线可以“撕掉”。要想在纸上留下一个连续的空白区域，必须所有被撕掉的页码是 **连续的**，否则中间会有“残留的线”把空洞划分成两段。

这个办法一定能找到答案，因为我们遍历了所有可能的上、下、左、右边界组合，只要有一种组合能形成正方形，必定会被检测到。

#### 代码（Python）

```python
from typing import List

def maxSquareArea_bruteforce(n: int, m: int,
                             hBars: List[int],
                             vBars: List[int]) -> int:
    # 把可删除的横线、竖线放进集合，查询 O(1)
    h_set = set(hBars)
    v_set = set(vBars)

    # 所有横线的编号（包括最外层的 1 和 n+2）
    h_all = list(range(1, n + 3))
    v_all = list(range(1, m + 3))

    max_side = 0

    # ---------- 枚举横向缺口 ----------
    # top、bottom 分别是保留下来的两根横线
    for i in range(len(h_all)):
        for j in range(i + 1, len(h_all)):
            top, bottom = h_all[i], h_all[j]
            # 检查两根线之间的所有内部线是否都可以被删除
            ok = True
            for k in range(top + 1, bottom):
                if k not in h_set:          # 这根线是固定的，不能删除
                    ok = False
                    break
            if not ok:
                continue
            height = bottom - top           # 缺口的高度（相邻两根线之间的格子数）

            # ---------- 枚举竖向缺口 ----------
            for p in range(len(v_all)):
                for q in range(p + 1, len(v_all)):
                    left, right = v_all[p], v_all[q]
                    ok2 = True
                    for r in range(left + 1, right):
                        if r not in v_set:   # 这根竖线是固定的
                            ok2 = False
                            break
                    if not ok2:
                        continue
                    width = right - left     # 缺口的宽度

                    side = min(height, width)    # 正方形的边长不能超过任意一方向的缺口
                    max_side = max(max_side, side)

    return max_side * max_side           # 面积 = 边长²
```

> 关键行解释  
> - `h_set = set(hBars)`：把可删除的横线放进集合，查询是否可删除的时间从 `O(k)` 降到 `O(1)`。  
> - `for k in range(top + 1, bottom):`：遍历两根保留下来的横线之间的所有内部线，检查它们是否全部在 `h_set` 中。  
> - `side = min(height, width)`：正方形的边长受限于较短的那一边。  

#### 复杂度

- **时间复杂度**：  
  - 横向枚举需要 `O((|hBars|+2)²)` 次（外层两根线的组合），竖向同理是 `O((|vBars|+2)²)`。  
  - 在每次组合里我们还要遍历中间的线段，最坏情况是 `O(|hBars|)` 与 `O(|vBars|)`。  
  - 综合下来是 `O(|hBars|³ + |vBars|³)`，但因为 `|hBars|,|vBars| ≤ 100`，实际运行仍在可接受范围。  
  - 用大白话说，就是**几千次循环**，对电脑来说几乎是瞬间完成。

- **空间复杂度**：`O(|hBars| + |vBars|)` 用来存集合，几乎可以忽略不计（只存了几百个整数）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们一次又一次检查「两根保留下来的线之间的所有内部线是否全部可删除」——这是一段**连续性**的判断。  
实际上，只要我们能找到一段 **最长的连续可删除横线**，以及一段 **最长的连续可删除竖线**，就已经足够构造最大正方形了，原因如下：

1. 假设横向我们能连续摘掉 `k` 根横线，编号为 `hx, hx+1, …, hy`（其中 `hy - hx = k-1`）。  
   - 把这 `k` 根横线全部删除后，上下边界自然是 `hx-1` 与 `hy+1`（这两根线是固定的，不能删）。  
   - 两者之间的格子行数等于 `(hy+1) - (hx-1) = hy - hx + 2 = k + 1`。  
   - 换句话说，**连续的可删除横线段长度 + 2** 就是我们可以得到的最大“高度”。

2. 竖向同理，得到最大“宽度”为 `vy - vx + 2`。

3. 正方形的边长受限于高度和宽度的较小者：  

   ```
   side = min( hy - hx + 2 , vy - vx + 2 )
   ```

4. 最后面积 = `side * side`。

因此，**核心任务**简化为：

- 在 `hBars` 中找出 **最长的连续整数子序列**（不要求排序后连续，只要数值本身是连续的）。  
- 在 `vBars` 中同理。

这可以在 **O(k log k)**（先排序，再一次扫描）完成，`k ≤ 100`，非常快。

> **为什么只需要最长的那一段**？  
> 如果我们选了两段不相邻的可删除横线，之间必然会有一根固定的横线阻断，导致高度更小。于是最长的连续段必然能提供最大可能的高度。

#### 代码（Python）

```python
from typing import List

def longest_consecutive(seq: List[int]) -> int:
    """
    在整数序列 seq 中返回最长连续整数子序列的长度。
    例如 seq = [2,3,5,6,7] -> 返回 3（对应 5,6,7）。
    """
    if not seq:
        return 0
    seq.sort()                     # 先排序，保证相邻元素在数值上相邻
    best = cur = 1                 # 当前连续段长度，和全局最大长度
    for i in range(1, len(seq)):
        if seq[i] == seq[i-1] + 1: # 与前一个数相差恰好 1 → 继续连续
            cur += 1
        else:                      # 不连续，重新开始计数
            best = max(best, cur)
            cur = 1
    return max(best, cur)          # 最后一次比较

def maxSquareArea(n: int, m: int,
                  hBars: List[int],
                  vBars: List[int]) -> int:
    """
    返回最大正方形空洞的面积。
    思路：分别求水平、垂直可删除柱子中最长的连续段，
    再用公式 side = min(len_h + 2, len_v + 2)。
    """
    # longest 连续段的「柱子数量」(不包括两侧固定的柱子)
    longest_h = longest_consecutive(hBars)
    longest_v = longest_consecutive(vBars)

    # 根据提示，正方形的边长 = min( longest_h + 2 , longest_v + 2 )
    side = min(longest_h + 2, longest_v + 2)

    return side * side              # 面积 = 边长的平方
```

> 关键行解释  
> - `seq.sort()`：先把可删除的柱子编号排好序，后面只需要一次线性扫描就能判断是否连续。  
> - `if seq[i] == seq[i-1] + 1:`：判断两个相邻数字在数值上是否相差 1，即是否是连续的。  
> - `side = min(longest_h + 2, longest_v + 2)`：**+2** 表示在连续可删除段的两端各有一根固定的柱子，形成的缺口高度/宽度比可删除的数量多两格。  

#### 复杂度

- **时间复杂度**：  
  - 对 `hBars`、`vBars` 各自排序，`O(k log k)`（`k ≤ 100`），随后一次线性扫描 `O(k)`。  
  - 整体 `O(k log k)`，在实际数据里几乎是瞬间完成。  
  - 与暴力解相比，**从几千次循环降到几百次比较**，快了一个数量级。

- **空间复杂度**：  
  - 只用了若干额外的整数变量和排序时的临时列表，`O(k)`，即几百个整数的空间，几乎可以忽略。

---

## 心得

- **核心技巧**：**寻找数组中的最长连续整数子序列**（Longest Consecutive Subsequence）。  
- 该技巧常用于需要「连续缺口」或「连续可用资源」的题目，例如  
  1. **Longest Consecutive Sequence**（LeetCode 128）  
  2. **Maximum Length of Subarray With Positive Product**（需要连续正数）  
  3. **Maximum Consecutive Ones**（二进制数组中连续 1 的长度）  
- **一句话总结解题钥匙**：*把可以删除的柱子看成“可缺口的格子”，最长的连续缺口决定了最大正方形的边长*。

---

## 反思

- **第一反应**：先想把所有可能的正方形位置枚举出来，检查能否通过删除得到。  
- **最容易踩的坑**：  
  - 忽略了最外层的两根柱子是 **固定不能删** 的，需要在计算缺口长度时加上它们的贡献（`+2`）。  
  - 连续性判断必须基于 **数值连续**（相差 1），而不是在原数组中的相邻位置。  
  - 当 `hBars`、`vBars` 为空时（虽然题目不允许），公式仍需返回最小的正方形（边长 2），要注意边界。  
- **下次类似题目第一步**：先思考“能形成的连续缺口有多大”，把问题抽象为 **最长连续子序列**，再再去设计具体实现。