# #2280. **表示折线图的最少直线段数** / Minimum Lines to Represent a Line Chart

> 难度：中等 · 标签：Array、Math、Geometry、Sorting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimum-lines-to-represent-a-line-chart/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array stockPrices where stockPrices[i] = [dayi, pricei] indicates the price of the stock on day dayi is pricei. A line chart is created from the array by plotting the points on an XY plane with the X-axis representing the day and the Y-axis representing the price and connecting adjacent points. One such example is shown below:
Return the minimum number of lines needed to represent the line chart.

**Examples**

**Example 1:**

```
Input: stockPrices = [[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]]
Output: 3
Explanation:
The diagram above represents the input, with the X-axis representing the day and Y-axis representing the price.
The following 3 lines can be drawn to represent the line chart:
- Line 1 (in red) from (1,7) to (4,4) passing through (1,7), (2,6), (3,5), and (4,4).
- Line 2 (in blue) from (4,4) to (5,4).
- Line 3 (in green) from (5,4) to (8,1) passing through (5,4), (6,3), (7,2), and (8,1).
It can be shown that it is not possible to represent the line chart using less than 3 lines.
```

**Example 2:**

```
Input: stockPrices = [[3,4],[1,2],[7,8],[2,3]]
Output: 1
Explanation:
As shown in the diagram above, the line chart can be represented with a single line.
```

**Constraints**

- 1 <= stockPrices.length <= 105
- stockPrices[i].length == 2
- 1 <= dayi, pricei <= 109
- All dayi are distinct.

---

## 题目（中文翻译）

给定一个二维整数数组 `stockPrices`，其中 `stockPrices[i] = [dayi, pricei]` 表示第 `dayi` 天的股票价格为 `pricei`。在 XY 平面上绘制这些点，X 轴代表天数，Y 轴代表价格，并依次连接相邻的点，即可得到一张折线图（line chart）。返回表示该折线图所需的最少直线段（line）数量。

**示例 1**

**输入**  
`stockPrices = [[1,7],[2,6],[3,5],[4,4],[5,4],[6,3],[7,2],[8,1]]`

**输出**  
`3`

**解释**  
上图展示了输入对应的折线图，X 轴为天数，Y 轴为价格。可以使用以下 3 条直线来完整表示该折线图：

- **直线 1**（红色）从点 `(1,7)` 到点 `(4,4)`，经过 `(1,7)`, `(2,6)`, `(3,5)`, `(4,4)`。
- **直线 2**（蓝色）从点 `(4,4)` 到点 `(5,4)`。
- **直线 3**（绿色）从点 `(5,4)` 到点 `(8,1)`，经过 `(5,4)`, `(6,3)`, `(7,2)`, `(8,1)`。

**示例 2**

**输入**  
`stockPrices = [[3,4],[1,2],[7,8],[2,3]]`

**输出**  
`1`

**解释**  
如上图所示，整个折线图可以用一条直线表示。

**约束条件**

- `1 <= stockPrices.length <= 10^5`
- `stockPrices[i].length == 2`
- `1 <= dayi, pricei <= 10^9`
- 所有 `dayi` 均不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把所有点先按照 **day**（横坐标）从小到大排好序，然后依次检查相邻的三点  
`(x1, y1) , (x2, y2) , (x3, y3)` 是否在同一直线上。  

- **如果在同一直线上**，说明这三点可以用同一根线段来表示，继续往后看下一个点。  
- **如果不在同一直线上**，就必须在 `(x2, y2)` 处折线，新增一根线段。

> **为什么这样能得到正确答案？**  
> 线图本身就是把相邻的点用直线相连。如果一段连续的点全都共线，那么它们之间只需要 **一根** 线段；一旦出现不共线的转折点，就必须新开一根线段。因此只要把所有转折点数出来（第一个点必然是线段的起点），答案就出来了。

- **判断三点共线**：  
  两向量的叉乘为 0 表示平行，即  
  \[
  (x2-x1)*(y3-y2) = (y2-y1)*(x3-x2)
  \]  
  这里全用整数运算，避免浮点误差。

#### 代码（Python）

```python
from typing import List

def minimumLines(stockPrices: List[List[int]]) -> int:
    # 1. 按天数排序，保证相邻点在图中真的相邻
    stockPrices.sort(key=lambda p: p[0])          # 类比：把散落的日历页按日期顺序排好

    n = len(stockPrices)
    if n <= 2:                                    # 0 条或 1 条线段的特殊情况
        return 0 if n == 1 else 1

    # 2. 统计需要的线段数量，初始为 1（第一根线段一定存在）
    lines = 1

    # 3. 从第 3 个点开始检查是否需要新建线段
    for i in range(2, n):
        x1, y1 = stockPrices[i - 2]
        x2, y2 = stockPrices[i - 1]
        x3, y3 = stockPrices[i]

        # 叉乘判断是否共线： (x2-x1)*(y3-y2) == (y2-y1)*(x3-x2)
        if (x2 - x1) * (y3 - y2) != (y2 - y1) * (x3 - x2):
            lines += 1          # 出现拐点，需要多加一根线段

    return lines
```

#### 复杂度

- **时间复杂度：** `O(n log n)`  
  主要耗时在排序（`n` 为点的数量），遍历检查每组三点只需 `O(1)`，所以整体是 `n log n`。  
  大白话：如果有 10 万个点，先把它们排好序大概要花 10 万 * log₂10万 ≈ 10 万 * 17 次比较。

- **空间复杂度：** `O(1)`（不计排序的原地交换）  
  只用了常数个额外变量，跟点的数量无关。

---

### 2. 最优解

#### 思路  

暴力解已经是最直接的 `O(n log n)`，再往下的优化只能在 **不排序** 的前提下做。但题目已经保证 **所有 day 都不同**，而且 **day 的取值范围很大**（到 10⁹），如果不排序我们就不知道相邻点的顺序，无法判断哪些点应该连在一起。

因此 **最优解** 仍然是：

1. **先排序**（唯一必须的步骤）。  
2. **遍历一次**，用 **斜率的唯一表示**（约分后的分子/分母）来判断是否换线。

与暴力解的区别在于：  
- 暴力解每次都做两次乘法比较（叉乘），而最优解把 **斜率** 直接标准化为最简分数 `(dy/g, dx/g)`（`g = gcd(dy, dx)`），随后只比较这两个整数是否相等。  
- 这样可以把“是否共线”判断抽象成“相邻两段的斜率是否相同”，代码更直观，也避免了在极端情况下乘法溢出（Python 整数不溢出，但在某些语言里会）。

**关键数据结构**：  
- **哈希表（字典）** 用来记录上一段的斜率。这里的哈希表就像查字典一样，`key` 是 `(dy, dx)`，`value` 只是一段斜率的标记。  
- **最大公约数（gcd）**：把斜率约成最简分数，防止 `(2,4)` 与 `(1,2)` 被误判为不同。把斜率约分就像把“1/2 米/秒”化成最简的“0.5 米/秒”，更容易比较。

**步骤**  

1. 按 day 排序。  
2. 计算第一段的斜率 `(dy, dx)`，约分后保存为 `prev`.  
3. 从第二段开始，依次计算当前段的斜率 `cur`（同样约分）。  
   - 若 `cur == prev`，说明仍在同一直线上，不增加线段计数。  
   - 否则，`lines += 1` 并把 `prev = cur`。  
4. 遍历结束，返回 `lines`。

**为什么这样快**  
- 排序 `O(n log n)` 是不可避免的下界（因为输出本身与点的顺序有关）。  
- 之后的遍历只做常数次整数运算（`gcd`、加减、比较），所以整体仍是 `O(n log n)`，但常数更小，代码更易读。

#### 代码（Python）

```python
import math
from typing import List

def minimumLines(stockPrices: List[List[int]]) -> int:
    # 1. 按 day 排序
    stockPrices.sort(key=lambda p: p[0])

    n = len(stockPrices)
    if n <= 2:                # 1 个点不需要线段，2 个点只需要 1 条线段
        return 0 if n == 1 else 1

    # 2. 计算第一段的最简斜率
    x0, y0 = stockPrices[0]
    x1, y1 = stockPrices[1]
    dx = x1 - x0
    dy = y1 - y0
    g = math.gcd(dx, dy)
    prev = (dy // g, dx // g)   # 用 (分子, 分母) 表示斜率

    lines = 1                    # 至少有一根线段

    # 3. 从第 3 个点开始逐段比较斜率
    for i in range(2, n):
        x_prev, y_prev = stockPrices[i - 1]
        x_cur,  y_cur  = stockPrices[i]

        dx = x_cur - x_prev
        dy = y_cur - y_prev
        g = math.gcd(dx, dy)
        cur = (dy // g, dx // g)   # 当前段的最简斜率

        if cur != prev:            # 斜率变化，必须折线
            lines += 1
            prev = cur              # 更新为新的斜率基准

    return lines
```

#### 复杂度

- **时间复杂度：** `O(n log n)`  
  - 排序仍然是 `n log n`。  
  - `gcd` 的时间复杂度是 `O(log max(dx, dy))`，在本题的数值范围内可以视为常数。  
  与暴力解相比，去掉了每次的乘法比较，实际运行更快。

- **空间复杂度：** `O(1)`（原地排序）  
  只使用了几条临时变量，不随 `n` 增长。

---

## 心得

- **核心技巧**：**利用斜率的唯一化（约分后比较）来合并共线的连续点**。  
- **适用的题型**：  
  1. “把若干点连成最少的直线段” 类似题，如 *“Number of Lines To Represent a Chart”*。  
  2. “判断若干点是否在同一直线上” 的几何题。  
  3. “找出一组点中斜率变化的次数”，如 *“Maximum Points on a Line”* 的简化版。  
- **一句话总结解题钥匙**：**把“是否共线”转化为“相邻斜率是否相同”，用最简分数做唯一标识**。

---

## 反思

- **第一反应**：看到“最少线段”立刻想到“把能共线的点合并”，于是想到检查相邻三点是否共线。  
- **最容易踩的坑**  
  - **整数溢出**：直接用浮点数比较斜率会出现精度误差；用乘法叉乘或约分的整数方式才安全。  
  - **斜率为 0 或无穷大**：`dx`、`dy` 可能为 0，必须在约分前先处理 `gcd`，Python 的 `math.gcd(0, a) = a` 能帮忙。  
  - **未排序**：忘记先把点按 day 排序会导致错误的相邻关系。  
- **下次类似题的第一步**：**先把点排序**，然后**把“是否在同一直线”抽象成“斜率是否相等”**，再利用哈希/约分做唯一化比较。