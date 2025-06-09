# #3219. 切蛋糕的最小费用 II / Minimum Cost for Cutting Cake II

> 难度：困难 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-for-cutting-cake-ii/)

---

## 题目（英文原版）

**Description**

There is an m x n cake that needs to be cut into 1 x 1 pieces.
You are given integers m, n, and two arrays:
In one operation, you can choose any piece of cake that is not yet a 1 x 1 square and perform one of the following cuts:
After the cut, the piece of cake is divided into two distinct pieces.
The cost of a cut depends only on the initial cost of the line and does not change.
Return the minimum total cost to cut the entire cake into 1 x 1 pieces.

**Examples**

**Example 1:**

```
Input: m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5]
Output: 13
Explanation:

The total cost is 5 + 1 + 1 + 3 + 3 = 13 .
```

**Example 2:**

```
Input: m = 2, n = 2, horizontalCut = [7], verticalCut = [4]
Output: 15
Explanation:
The total cost is 7 + 4 + 4 = 15 .
```

**Constraints**

- 1 <= m, n <= 105
- horizontalCut.length == m - 1
- verticalCut.length == n - 1
- 1 <= horizontalCut[i], verticalCut[i] <= 103

---

## 题目（中文翻译）

给定一个大小为 `m x n` 的蛋糕，需要将其切割成若干 `1 x 1` 的小块。  

你会得到整数 `m`、`n`，以及两个数组：  

- `horizontalCut`：记录所有水平切割线的费用  
- `verticalCut`：记录所有垂直切割线的费用  

在一次 **操作 (operation)** 中，你可以选择任意当前仍不是 `1 x 1` 的 **蛋糕块 (piece of cake)**，并对其执行以下任意一种切割：  

- 进行一次水平切割，使用 `horizontalCut` 中对应的费用  
- 进行一次垂直切割，使用 `verticalCut` 中对应的费用  

切割后，该蛋糕块会被分成 **两个不同的块 (two distinct pieces)**。  
每条切割线的费用在整个过程中保持不变，只与该线的初始费用有关。  

求将整个蛋糕全部切割成 `1 x 1` 小块所需的 **最小总费用 (minimum total cost)**。

---

## 示例

### 示例 1
**输入**  
```
m = 3, n = 2, horizontalCut = [1,3], verticalCut = [5]
```
**输出**  
```
13
```
**解释**  
总费用为 `5 + 1 + 1 + 3 + 3 = 13` 。

### 示例 2
**输入**  
```
m = 2, n = 2, horizontalCut = [7], verticalCut = [4]
```
**输出**  
```
15
```
**解释**  
总费用为 `7 + 4 + 4 = 15` 。

---

## 约束条件
- `1 <= m, n <= 10^5`
- `horizontalCut.length == m - 1`
- `verticalCut.length == n - 1`
- `1 <= horizontalCut[i], verticalCut[i] <= 10^3`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把所有水平切割线 `horizontalCut` 和所有垂直切割线 `verticalCut` 的切割顺序全部列举一遍，算出每一种顺序对应的总费用，最后取最小值。  
- **使用的数据结构**：  
  - 两个列表分别保存水平切割费用和垂直切割费用。  
  - 用一个 **排列（permutation）** 来表示切割的顺序。排列就像把所有切割线排成一列，依次执行。  
- **为什么正确**：  
  - 只要把所有切割线都执行一遍，最后一定能把蛋糕切成 `1×1` 的小块。遍历所有可能的执行顺序，就一定会碰到费用最小的那一种。  
- **时间/空间复杂度**：  
  - 切割线总数为 `k = (m‑1) + (n‑1)`。所有可能的执行顺序数是 `k!`（k 的阶乘），也就是 **指数级** 的增长。  
  - 每一种顺序我们都要模拟一次切割，模拟过程需要 O(k) 的时间。  
  - 因此总体时间复杂度是 **O(k!·k)**，在最坏情况下会非常慢，几乎不可能在 10⁵ 规模的数据上跑完。  
  - 空间上只需要保存原始数组和递归栈，最多 O(k) 的额外空间。

> **大白话**：`O(k!·k)` 就像让你把 10 本书排成所有可能的顺序再逐个检查——根本不可能在一分钟内完成。

#### 代码（Python）

```python
import itertools

def minCost_bruteforce(m: int, n: int,
                       horizontalCut: list[int],
                       verticalCut: list[int]) -> int:
    # 把所有切割费用放到同一个列表里，记住它们的类型
    cuts = [('h', c) for c in horizontalCut] + [('v', c) for c in verticalCut]

    best = float('inf')
    # 枚举所有排列（每一种切割顺序）
    for perm in itertools.permutations(cuts):
        # 当前已经产生的水平块数和垂直块数
        h_parts, v_parts = 1, 1
        total = 0
        for typ, cost in perm:
            if typ == 'h':          # 水平切割
                total += cost * v_parts   # 这条水平线会切过所有垂直块
                h_parts += 1
            else:                   # 垂直切割
                total += cost * h_parts   # 这条垂直线会切过所有水平块
                v_parts += 1
        best = min(best, total)

    return best
```

> **注**：上述代码只适用于非常小的 `m, n`（比如 ≤ 5），否则会因排列数爆炸而卡死。

#### 复杂度

- **时间复杂度**：`O(k!·k)` —— 需要遍历所有切割顺序，`k` 为切割线总数。  
- **空间复杂度**：`O(k)` —— 保存切割线列表以及递归/迭代时的临时计数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的地方在于“顺序选择”**。我们并不需要穷举所有顺序，只要每一次都选**当前最贵的那条切割线**，就能保证总费用最小。这个思路来源于**贪心（Greedy）**策略，核心原因如下：

1. **切割费用的乘数**  
   - 当我们做一次水平切割时，它会影响 **当前已有的垂直块数**（记为 `v_parts`），费用实际是 `cost_h * v_parts`。  
   - 同理，垂直切割的费用是 `cost_v * h_parts`。  
   - 这说明 **每一次切割的费用会被“已有的块数”放大**，而块数只会随切割次数单调递增。

2. **把“大数”放在“小数”前**  
   - 假设我们有两条水平切割线 `a > b`（`a` 更贵），以及两次垂直切割（会把水平块数从 1 增加到 2）。  
   - 若先切 `b` 再切 `a`，`b` 只会乘以较小的垂直块数，`a` 会乘以较大的垂直块数，导致总费用更高。  
   - 反过来，先切 `a` 再切 `b`，`a` 乘以较小的块数，`b` 乘以较大的块数，总费用更低。  

   这正是 **“大数先乘小数，后面的大数再乘更大的数”** 的贪心原则。

3. **实现细节**  
   - 将水平切割费用和垂直切割费用分别按 **降序** 排列（从大到小）。  
   - 用两个指针 `i`、`j` 分别遍历这两个已排序的数组。  
   - 维护当前已经产生的 **水平块数 `h_parts`** 与 **垂直块数 `v_parts`**（初始均为 1）。  
   - 每一步比较当前未处理的水平费用 `horizontalCut[i]` 与垂直费用 `verticalCut[j]`，取较大的那个执行切割，并相应更新块数和累计费用。  
   - 当其中一种切割全部用完后，只剩下另一种切割，此时直接把剩余费用乘以当前对应的块数累加即可。

4. **为什么贪心是最优的**  
   - 费用的乘数只会随切割次数单调增大，**没有回头的机会**（一次切割后块数只能增加，不能减少）。  
   - 因此把 **当前最大的费用尽可能乘以当前最小的块数**，必然能让后面的费用乘以更大的块数，从而整体最小。  
   - 这是一种 **“局部最优 → 全局最优”** 的典型贪心证明，常见于“切割木板”“切割蛋糕”等题目。

> **类比**：想象你在超市买水果，水果越贵，你越想先买少量（比如先买一个），等买完后再买便宜的水果时已经有更多的预算（块数）可以“放大”它们的费用。这样总花费最少。

#### 代码（Python）

```python
def minCost(m: int, n: int,
           horizontalCut: list[int],
           verticalCut: list[int]) -> int:
    """
    贪心算法：每次切费最高的那条线
    时间复杂度 O((m+n) log(m+n))，因为要排序
    空间复杂度 O(1)（不计输入数组本身）
    """
    # 1. 把费用从大到小排序
    horizontalCut.sort(reverse=True)   # 降序
    verticalCut.sort(reverse=True)     # 降序

    # 2. 初始化块数（当前已有的水平块和垂直块）
    h_parts, v_parts = 1, 1   # 初始都是整块蛋糕

    # 3. 用指针遍历两个数组
    i, j = 0, 0               # i 指向水平切割，j 指向垂直切割
    total = 0                 # 累计费用

    # 4. 同时还有未处理的水平或垂直切割时循环
    while i < len(horizontalCut) and j < len(verticalCut):
        if horizontalCut[i] >= verticalCut[j]:
            # 取水平切割：费用 * 当前垂直块数
            total += horizontalCut[i] * v_parts
            h_parts += 1          # 水平块数加一
            i += 1
        else:
            # 取垂直切割：费用 * 当前水平块数
            total += verticalCut[j] * h_parts
            v_parts += 1          # 垂直块数加一
            j += 1

    # 5. 处理剩余的水平切割（如果垂直切割已经用完）
    while i < len(horizontalCut):
        total += horizontalCut[i] * v_parts
        i += 1
        h_parts += 1

    # 6. 处理剩余的垂直切割（如果水平切割已经用完）
    while j < len(verticalCut):
        total += verticalCut[j] * h_parts
        j += 1
        v_parts += 1

    return total
```

> **关键行中文注释** 已标注在代码里，帮助初学者快速对号入座。

#### 复杂度

- **时间复杂度**：`O((m + n) log (m + n))`  
  - 解释：我们需要对水平费用和垂直费用各自进行一次排序，排序的时间是 `O(k log k)`，`k = m‑1 + n‑1`。遍历两个已排序数组只需线性时间 `O(k)`，所以总体是 `O(k log k)`。相较于暴力的指数级，这已经是 **“把山压平”** 了。  
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 解释：只用了几个整数变量 `i, j, h_parts, v_parts, total`，没有额外的数组或递归栈，内存占用基本保持不变。

---

## 心得

- **核心技巧**：**贪心 + 排序**，在每一步都选当前费用最大的切割线，使其乘以当前块数最小的那一维。  
- **适用的题型**  
  1. **切割木板 / 蛋糕**（LeetCode 1547. Minimum Cost to Cut a Stick）  
  2. **买卖股票的最佳时机（贪心选最大收益）**  
  3. **合并石子（Greedy 合并顺序）**（虽然需要堆，但思路相似）  
- **一句话总结**：**把“大费用”先乘“小块数”，后面的“小费用自然乘上“大块数”，整体费用最小**。

---

## 反思

- **第一反应**：看到“每次切割费用乘以已有块数”，立刻想到 **枚举所有切割顺序**（暴力）来保证正确性。  
- **最容易踩的坑**  
  - **忘记乘以当前块数**：水平切割要乘以 `v_parts`，垂直切割要乘以 `h_parts`，搞混会导致答案翻倍。  
  - **边界条件**：当一种切割全部用完后，还需要把另一种剩余的全部处理完，否则会少计费用。  
  - **整数溢出**（在某些语言中）：费用最大 10³，块数最大 10⁵，乘积可能达到 10⁸，累加后仍在 64 位整数范围，但在 C++/Java 中要使用 `long long` / `long`。  
- **下次遇到同类题**：第一步就想到 **“把费用从大到小排序，贪心取最大”**，随后只要维护好当前的块数即可。这样可以直接跳过暴力搜索，迅速得到最优解。