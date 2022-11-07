# #2001. 可互换矩形对的数量 / Number of Pairs of Interchangeable Rectangles

> 难度：中等 · 标签：Array、Hash Table、Math、Counting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/)

---

## 题目（英文原版）

**Description**

You are given n rectangles represented by a 0-indexed 2D integer array rectangles, where rectangles[i] = [widthi, heighti] denotes the width and height of the ith rectangle.
Two rectangles i and j (i < j) are considered interchangeable if they have the same width-to-height ratio. More formally, two rectangles are interchangeable if widthi/heighti == widthj/heightj (using decimal division, not integer division).
Return the number of pairs of interchangeable rectangles in rectangles.

**Examples**

**Example 1:**

```
Input: rectangles = [[4,8],[3,6],[10,20],[15,30]]
Output: 6
Explanation: The following are the interchangeable pairs of rectangles by index (0-indexed):
- Rectangle 0 with rectangle 1: 4/8 == 3/6.
- Rectangle 0 with rectangle 2: 4/8 == 10/20.
- Rectangle 0 with rectangle 3: 4/8 == 15/30.
- Rectangle 1 with rectangle 2: 3/6 == 10/20.
- Rectangle 1 with rectangle 3: 3/6 == 15/30.
- Rectangle 2 with rectangle 3: 10/20 == 15/30.
```

**Example 2:**

```
Input: rectangles = [[4,5],[7,8]]
Output: 0
Explanation: There are no interchangeable pairs of rectangles.
```

**Constraints**

- n == rectangles.length
- 1 <= n <= 105
- rectangles[i].length == 2
- 1 <= widthi, heighti <= 105

---

## 题目（中文翻译）

你得到一个由 `n` 个矩形组成的 **0 索引** 二维整数数组 `rectangles`，其中 `rectangles[i] = [width_i, height_i]` 表示第 `i` 个矩形的宽度和高度。  

如果两个矩形 `i` 和 `j`（`i < j`）的宽高比相同，则称它们是 **可互换的（interchangeable）**。更形式化地说，若  

```
width_i / height_i == width_j / height_j
```  

（使用十进制除法，而非整数除法），则这两个矩形可互换。  

请返回数组 `rectangles` 中所有可互换矩形对的数量。

### 示例

**示例 1**  
> **输入**: `rectangles = [[4,8],[3,6],[10,20],[15,30]]`  
> **输出**: `6`  
> **解释**: 以下是按下标（0 索引）列出的可互换矩形对：  
> - 矩形 0 与矩形 1: `4/8 == 3/6`。  
> - 矩形 0 与矩形 2: `4/8 == 10/20`。  
> - 矩形 0 与矩形 3: `4/8 == 15/30`。  
> - 矩形 1 与矩形 2: `3/6 == 10/20`。  
> - 矩形 1 与矩形 3: `3/6 == 15/30`。  
> - 矩形 2 与矩形 3: `10/20 == 15/30`。

**示例 2**  
> **输入**: `rectangles = [[4,5],[7,8]]`  
> **输出**: `0`  
> **解释**: 没有可互换的矩形对。

### 约束条件

- `n == rectangles.length`
- `1 <= n <= 10^5`
- `rectangles[i].length == 2`
- `1 <= width_i, height_i <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有矩形两两比较**，看它们的宽高比是否相等。  
具体步骤：

1. 依次取第 `i` 个矩形 `(wi, hi)`，再把后面的每个矩形 `(wj, hj)`（`j > i`）取出来。  
2. 计算两者的宽高比 `wi / hi` 与 `wj / hj`（使用浮点除法），判断是否相等。  
3. 如果相等，就把答案计数 `+1`。

> **类比**：把每个矩形想象成一本书的封面，宽度是书的宽，长度是书的高。暴力解相当于把每本书的封面都拿出来，和书架上后面的所有封面逐一比对，看看是不是“长宽比例”完全相同。

**为什么正确**：只要遍历到了所有可能的 `(i, j)` 组合，且每一次都严格按照题目要求比较宽高比，就一定能统计出所有可互换的矩形对。

#### 代码（Python）

```python
from typing import List

def interchangeableRectangles_bruteforce(rectangles: List[List[int]]) -> int:
    n = len(rectangles)
    ans = 0
    # 双层循环枚举所有 i < j 的组合
    for i in range(n):
        wi, hi = rectangles[i]
        for j in range(i + 1, n):
            wj, hj = rectangles[j]
            # 用浮点数直接除，比较是否相等
            if wi / hi == wj / hj:
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - “平方”意味着如果有 10,000 条矩形，需要比较约 100,000,000 次；当 `n` 达到 10⁵ 时，计算量几乎不可接受（相当于把 100,000 人每两个人都握手一次）。
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **两层循环**，导致 `n²` 次比较。  
观察题目可以发现：

- 两个矩形是否可互换，只取决于 **宽高比例**，而不关心它们的具体宽高数值。  
- 如果把每个矩形的比例 **归一化**（即把 `width/height` 化成唯一的标识），相同标识的矩形就可以两两配对。

于是我们把“遍历所有组合”换成“把相同比例的矩形聚在一起”，再用组合计数公式求出配对数。

**关键点：如何唯一表示一个比例？**  
直接使用浮点数会出现精度误差（比如 `1/3` 用二进制表示不精确），因此要把比例化为 **最简分数**：

```
ratio = width / height
=> 用 (width / g, height / g) 表示
   其中 g = gcd(width, height)（两数的最大公约数）
```

这样 `(4,8)`、`(2,4)`、`(10,20)` 都会被化成 `(1,2)`，自然相同。

实现步骤：

1. 遍历 `rectangles`，对每个 `[w, h]` 计算 `g = gcd(w, h)`，得到归一化的键 `key = (w // g, h // g)`。  
2. 用 **哈希表**（Python 的 `dict`）记录每种键出现的次数 `cnt[key]`。  
   - 类比：把每种比例想成一本词典的“词条”，`key` 是词条，`cnt[key]` 是这本词典里该词出现了多少页。  
3. 再遍历哈希表，对于出现 `c` 次的比例，能够组成的不同矩形对数是组合数 `c * (c - 1) / 2`（从 `c` 个元素中任选两个）。把所有键的组合数相加即为答案。

#### 代码（Python）

```python
from typing import List
from math import gcd
from collections import defaultdict

def interchangeableRectangles(rectangles: List[List[int]]) -> int:
    # 用 defaultdict 自动把不存在的键初始化为 0
    freq = defaultdict(int)

    # 1️⃣ 统计每种最简比例出现的次数
    for w, h in rectangles:
        g = gcd(w, h)          # 求最大公约数
        key = (w // g, h // g) # 归一化为最简分数，作为哈希表的键
        freq[key] += 1

    # 2️⃣ 根据组合数公式累加答案
    ans = 0
    for cnt in freq.values():
        # C(cnt, 2) = cnt * (cnt - 1) // 2
        ans += cnt * (cnt - 1) // 2
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * log M)`（其中 `M = 10⁵` 为宽高上限）  
  - 主要耗时在 `gcd` 计算，欧几里得算法的时间复杂度是 `O(log min(w, h))`，对每个矩形只算一次。整体线性遍历 `n`，所以是 **线性**（相较于 `n²`，快了几个数量级）。  
- **空间复杂度**：`O(k)`，`k` 为不同最简比例的种类数，最坏情况下 `k ≤ n`，即最多存 `n` 条键值对。  
  - 对比暴力解的 `O(1)`，这里多用了哈希表的额外空间，但在 `n ≤ 10⁵` 时仍然是可接受的。

---

## 心得

- **核心技巧**：把“宽高比相同”转化为“最简分数相同”，利用哈希表统计频次，再用组合数求配对数。  
- **适用的题型**  
  1. “相同比例/相同斜率”类问题（如 LeetCode 1492 `The kth Factor of n` 的变体）  
  2. “相同商/相同余数”类计数（如统计同余数对数）  
  3. “相同向量方向”或“相同角度”计数（如二维向量方向归一化）  
- **一句话总结**：**把可比的属性标准化为唯一键，用哈希计数再配对**。

---

## 反思

- **第一反应**：直接两层循环枚举所有矩形对，感觉最简单。  
- **最容易踩的坑**  
  - **浮点误差**：直接用 `width/height` 比较会因为精度问题漏掉本该相等的对。  
  - **约分遗漏**：忘记把比例化为最简分数，会把本该相同的比例误判为不同。  
  - **大数溢出**：组合数乘法要先做除法或使用整数除 `//`，防止中间结果超出 Python 整数范围（Python 本身大整数安全，但在其他语言要注意）。  
- **下次类似题的第一步**：**先思考是否能把“相等关系”转化为“相同键”，并用哈希表统计频次**，再决定是否需要约分、归一化或其他标准化手段。