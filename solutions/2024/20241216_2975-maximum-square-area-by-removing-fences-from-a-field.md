# #2975. 移除围栏后可形成的最大正方形面积 / Maximum Square Area by Removing Fences From a Field

> 难度：中等 · 标签：Array、Hash Table、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-square-area-by-removing-fences-from-a-field/)

---

## 题目（英文原版）

**Description**

There is a large (m - 1) x (n - 1) rectangular field with corners at (1, 1) and (m, n) containing some horizontal and vertical fences given in arrays hFences and vFences respectively.
Horizontal fences are from the coordinates (hFences[i], 1) to (hFences[i], n) and vertical fences are from the coordinates (1, vFences[i]) to (m, vFences[i]).
Return the maximum area of a square field that can be formed by removing some fences (possibly none) or -1 if it is impossible to make a square field.
Since the answer may be large, return it modulo 109 + 7.
Note: The field is surrounded by two horizontal fences from the coordinates (1, 1) to (1, n) and (m, 1) to (m, n) and two vertical fences from the coordinates (1, 1) to (m, 1) and (1, n) to (m, n). These fences cannot be removed.

**Examples**

**Example 1:**

```
Input: m = 4, n = 3, hFences = [2,3], vFences = [2]
Output: 4
Explanation: Removing the horizontal fence at 2 and the vertical fence at 2 will give a square field of area 4.
```

**Example 2:**

```
Input: m = 6, n = 7, hFences = [2], vFences = [4]
Output: -1
Explanation: It can be proved that there is no way to create a square field by removing fences.
```

**Constraints**

- 3 <= m, n <= 109
- 1 <= hFences.length, vFences.length <= 600
- 1 < hFences[i] < m
- 1 < vFences[i] < n
- hFences and vFences are unique.

---

## 题目（中文翻译）

给定一个大小为 \((m-1) \times (n-1)\) 的矩形场地，左下角坐标为 \((1,1)\)，右上角坐标为 \((m,n)\)。场地内部有若干水平围栏（horizontal fences）和垂直围栏（vertical fences），分别存放在数组 `hFences` 和 `vFences` 中。

- 第 `i` 条水平围栏的坐标为 \((hFences[i], 1)\) 到 \((hFences[i], n)\)；
- 第 `i` 条垂直围栏的坐标为 \((1, vFences[i])\) 到 \((m, vFences[i])\)。

返回通过移除若干围栏（可以为 0）后能够形成的 **正方形场地** 的最大面积；如果无法形成正方形场地，则返回 \(-1\)。由于答案可能很大，返回结果需取模 \(10^9 + 7\)。

> **说明**：场地的四条边由两条水平围栏 \((1,1) \rightarrow (1,n)\) 与 \((m,1) \rightarrow (m,n)\) 以及两条垂直围栏 \((1,1) \rightarrow (m,1)\) 与 \((1,n) \rightarrow (m,n)\) 组成，这四条围栏不可被移除。

## 示例

### 示例 1
**输入**  
`m = 4, n = 3, hFences = [2,3], vFences = [2]`

**输出**  
`4`

**解释**  
移除位于 \(2\) 的水平围栏和位于 \(2\) 的垂直围栏后，可得到面积为 \(4\) 的正方形场地。

### 示例 2
**输入**  
`m = 6, n = 7, hFences = [2], vFences = [4]`

**输出**  
`-1`

**解释**  
可以证明，无论如何移除围栏，都无法构成正方形场地。

## 约束条件

- \(3 \le m, n \le 10^9\)
- \(1 \le \text{hFences.length}, \text{vFences.length} \le 600\)
- \(1 < \text{hFences}[i] < m\)
- \(1 < \text{vFences}[i] < n\)
- `hFences` 与 `vFences` 中的元素互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把题目想成在一张被若干条“竖线”(横向栅栏)和“横线”(纵向栅栏)划分开的网格里，**我们只关心保留下来的四条边**。  
- 横向栅栏的坐标集合记为 `X = {1, hFences…, m}`，每两个坐标之间的距离就是一段可能的 **宽度**。  
- 纵向栅栏的坐标集合记为 `Y = {1, vFences…, n}`，每两个坐标之间的距离就是一段可能的 **高度**。  

最直接的做法是：  
1. 从 `X` 中任选左边界 `x1`、右边界 `x2`（`x1 < x2`），得到宽度 `w = x2 - x1`。  
2. 再从 `Y` 中任选上边界 `y1`、下边界 `y2`（`y1 < y2`），得到高度 `h = y2 - y1`。  
3. 检查 `w == h`，如果相等说明可以得到一个正方形，记录面积 `w*w` 的最大值。  

> **类比**：这就像在一排木板（横坐标）和一排柱子（纵坐标）之间挑选两块木板和两根柱子，看看挑出来的矩形是否是正方形。  

这种“枚举四条边”的方法必然能得到正确答案，因为我们遍历了**所有**可能的边界组合。  

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def maxSquareArea_bruteforce(m: int, n: int,
                             hFences: List[int],
                             vFences: List[int]) -> int:
    # 把外边界也加入集合，后面直接枚举
    xs = [1] + sorted(hFences) + [m]
    ys = [1] + sorted(vFences) + [n]

    best = -1                     # 记录最大的正方形边长
    # 枚举左、右边界
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            w = xs[j] - xs[i]      # 横向宽度
            # 枚举上、下边界
            for p in range(len(ys)):
                for q in range(p + 1, len(ys)):
                    h = ys[q] - ys[p]  # 纵向高度
                    if w == h:         # 正方形
                        best = max(best, w)

    if best == -1:
        return -1
    return (best * best) % MOD
```

#### 复杂度  

- 时间复杂度：`O(|X|^2 * |Y|^2)`，最坏情况下约为 `(602^2)*(602^2) ≈ 1.3×10^11`，在实际中会超时。  
  - **大白话**：我们要把每一条横线和每一条竖线两两配对，再配对另一组的两条线，想象成把 600 本书两两组合，再把另一堆 600 本书两两组合，最后把两套组合全部配对，数量会爆炸。  
- 空间复杂度：`O(1)`（只用了常数级别的额外变量）。

> 这一步虽然可以保证正确，但明显太慢，必须找出瓶颈并优化。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 出在四层循环里：我们把 “左/右” 与 “上/下” 的配对完全交叉了。  
其实我们只需要关心 **宽度** 和 **高度** 是否相等，而不必记住是哪两条具体的边界。  

**关键观察**  
- 任意两条横向栅栏之间的距离 `d = x2 - x1` 都可以成为矩形的 **宽度**。  
- 任意两条纵向栅栏之间的距离 `d = y2 - y1` 都可以成为矩形的 **高度**。  

如果一个数 `d` 同时出现在“所有可能的宽度集合” 和 “所有可能的高度集合” 中，就说明我们可以选出四条边，使得宽高相等，得到一个边长为 `d` 的正方形。  

于是问题转化为：

> **在两组差值集合里，找出最大的公共元素**。  

**如何快速得到差值集合**  
- 把外边界 `1`、`m`（或 `n`）加入对应的栅栏数组，排序后得到长度至多 `602` 的列表。  
- 两层循环遍历该列表的所有 **有序对**（`i < j`），计算差值 `arr[j] - arr[i]`，放进一个 `set`（哈希表）。  
  - 哈希表就像一本“查字典”，我们只需要把每个差值登记进去，后面想要判断是否出现，只要看字典里有没有对应的页码即可，时间是 **O(1)**。  

**整体流程**  
1. 构造 `X = {1} ∪ hFences ∪ {m}`，排序。  
2. 用两层循环把所有 `x[j] - x[i]` 放入集合 `diffX`。  
3. 同理构造 `Y`，得到集合 `diffY`。  
4. 取交集 `common = diffX ∩ diffY`，如果为空返回 `-1`。  
5. 否则 `L = max(common)`，答案是 `L*L % MOD`。  

因为 `|X|,|Y| ≤ 602`，两层循环的次数最多 `602*601/2 ≈ 1.8×10⁵`，完全可以接受。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def maxSquareArea(m: int, n: int,
                  hFences: List[int],
                  vFences: List[int]) -> int:
    """
    返回能够得到的最大正方形面积，若不存在返回 -1
    思路：把所有横向间距和纵向间距分别收集到集合里，取公共最大值
    """
    # -------------------------------------------------
    # 1. 把外边界也加入，得到完整的坐标列表并排序
    # -------------------------------------------------
    xs = [1] + sorted(hFences) + [m]
    ys = [1] + sorted(vFences) + [n]

    # -------------------------------------------------
    # 2. 收集所有可能的宽度（横向间距）
    # -------------------------------------------------
    diff_x = set()                     # 哈希表，存放所有 x 间距
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            diff = xs[j] - xs[i]       # 两条竖线之间的距离
            diff_x.add(diff)           # O(1) 插入

    # -------------------------------------------------
    # 3. 收集所有可能的高度（纵向间距）
    # -------------------------------------------------
    diff_y = set()
    for i in range(len(ys)):
        for j in range(i + 1, len(ys)):
            diff = ys[j] - ys[i]       # 两条横线之间的距离
            diff_y.add(diff)

    # -------------------------------------------------
    # 4. 找公共的间距，取最大的那个
    # -------------------------------------------------
    common = diff_x & diff_y           # 集合交集，得到同时出现的距离
    if not common:                     # 没有公共距离，无法构成正方形
        return -1

    side = max(common)                 # 最大的公共间距就是最大正方形的边长
    return (side * side) % MOD         # 题目要求取模
```

#### 复杂度  

- 时间复杂度：`O(|X|^2 + |Y|^2)` ≈ `O(600²) ≈ 3.6×10⁵`。  
  - **解释**：我们只做了两次“遍历所有有序对”，每次大约 180,000 次操作，远远小于暴力的 10⁹ 级别。  
- 空间复杂度：`O(|X|^2 + |Y|^2)` 最坏情况下集合里会存放所有不同的差值，数量同样不超过约 180,000，属于 **线性**（相对于输入规模）空间。  

相较于暴力的四层循环，这个方案把 **宽度** 与 **高度** 的枚举分离开来，利用哈希表的“快速查找”特性，显著降低了时间消耗。

---

## 心得  

- **核心技巧**：把“找相等的宽高”转化为“求两个差值集合的交集”。  
- **适用场景**：  
  1. 给定两组点，求能够组成等边图形（正方形、等腰矩形等）的最大尺寸。  
  2. “拆分+哈希” 类问题，例如在一维数组中找两个子数组长度相同且和相等的最大长度。  
  3. 需要比较两组**差值**或**距离**集合的题目（如 LeetCode 2244 “Maximum Number of Words Found in Sentences” 的思路类似）。  
- **一句话总结**：把“选四条边”变成“选两条边的距离”，利用集合快速找公共最大距离，就是解题钥匙。

---

## 反思  

- **第一反应**：直接枚举四条边（左、右、上、下），检查宽高是否相等。  
- **最容易踩的坑**：  
  - 忘记把外部的两条不可移除的栅栏 `1` 与 `m`（或 `n`）加入集合，导致漏掉可能的最大正方形。  
  - 直接用列表存差值并遍历寻找公共值，时间会爆炸；必须使用哈希表（`set`）实现 O(1) 查找。  
- **下次类似题**：先思考能否把“几何约束”抽象成**数值集合的交/并**，如果可以，就立刻把问题转化为集合运算，从而把多维枚举降到一维或二维的“差值”集合。