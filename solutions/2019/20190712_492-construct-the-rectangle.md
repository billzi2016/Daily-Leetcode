# #492. 构造矩形 / Construct the Rectangle

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/construct-the-rectangle/)

---

## 题目（英文原版）

**Description**

A web developer needs to know how to design a web page's size. So, given a specific rectangular web page’s area, your job by now is to design a rectangular web page, whose length L and width W satisfy the following requirements:
Return an array [L, W] where L and W are the length and width of the web page you designed in sequence.

**Examples**

**Example 1:**

```
Input: area = 4
Output: [2,2]
Explanation: The target area is 4, and all the possible ways to construct it are [1,4], [2,2], [4,1]. 
But according to requirement 2, [1,4] is illegal; according to requirement 3,  [4,1] is not optimal compared to [2,2]. So the length L is 2, and the width W is 2.
```

**Example 2:**

```
Input: area = 37
Output: [37,1]
```

**Example 3:**

```
Input: area = 122122
Output: [427,286]
```

**Constraints**

- 1 <= area <= 107

---

## 题目（中文翻译）

给定一个矩形网页的面积 **area**，请设计一个矩形网页，使其长度 **L** 和宽度 **W** 满足以下要求：

1. **L × W = area**  
2. **L ≥ W**  
3. 在满足前两条的前提下，**L - W** 最小  

返回一个数组 **[L, W]**，其中 **L** 为长度，**W** 为宽度，顺序即为 **[L, W]**。

---

### 示例

#### 示例 1
**输入:** `area = 4`  
**输出:** `[2,2]`  
**解释:** 目标面积是 4，所有可能的构造方式有 `[1,4]、[2,2]、[4,1]`。  
但根据要求 2，`[1,4]` 不合法；根据要求 3，`[4,1]` 相比 `[2,2]` 不是最优的。  
因此长度 **L** 为 2，宽度 **W** 为 2。

#### 示例 2
**输入:** `area = 37`  
**输出:** `[37,1]`

#### 示例 3
**输入:** `area = 122122`  
**输出:** `[427,286]`

---

### 约束条件
- `1 <= area <= 10^7`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **面积** 看成一个大盒子，所有能够拼出这个盒子的长 `L` 与宽 `W` 必须满足 `L × W = area`。  
于是我们可以把 **每一个正整数** 都当作可能的宽 `W`，把它从 `1` 试到 `area`，只要 `area` 能被 `W` 整除（`area % W == 0`），就得到对应的长度 `L = area // W`。  

- **数据结构**：这里只用到普通的整数变量和一个列表来存放答案，根本不需要像哈希表（字典）那样的“查字典”结构。  
- **正确性**：如果 `W` 能整除 `area`，那么 `L = area / W` 必然是整数，二者的乘积正好等于 `area`，满足题目要求。遍历所有 `W`，一定会找到所有合法的 `(L, W)`，再挑选 `L - W` 最小的即可。  
- **时间/空间复杂度**：  
  - **时间**：最坏情况要检查 `1 … area` 共 `area` 次，时间复杂度记作 **O(area)**。如果把 `area = 10⁷` 代进去，想象一下需要循环 **一千万次**，对初学者来说已经不算快了。  
  - **空间**：只用了常数个变量，空间复杂度是 **O(1)**（不随 `area` 增大而增加）。

#### 代码（Python）

```python
import math
from typing import List

def constructRectangle_bruteforce(area: int) -> List[int]:
    """
    暴力遍历所有可能的宽度 W，找到满足 L * W = area 且 L >= W，
    并使 L - W 最小的那一对。
    """
    best_L, best_W = area, 1          # 先把最差的情况 (area, 1) 记下来
    for w in range(1, area + 1):      # 从 1 试到 area
        if area % w == 0:             # 能整除说明 w 是合法宽度
            l = area // w             # 对应的长度
            if l - w < best_L - best_W:   # 看看差距是否更小
                best_L, best_W = l, w
    return [best_L, best_W]
```

#### 复杂度  

- **时间复杂度**：`O(area)` —— 需要检查 `area` 次，每次只做常数时间的除法和比较。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不会随输入大小增长。

---

### 2. 最优解  

#### 思路  

在暴力解里，**瓶颈** 是我们把宽度的上界设成了 `area`，实际上宽度不可能比 `√area` 还大。  
**为什么？**  
设 `W ≤ L`（题目要求长不小于宽），则有  

```
area = L * W  ≥  W * W  =>  W ≤ √area
```

也就是说，**合法的最宽的宽度** 必然不超过 `√area`。  
因此我们只需要在 `√area` 附近寻找因子即可。  

优化思路：

1. 先算出 `sqrt_area = int(math.isqrt(area))`（整数平方根），这是可能的最大宽度。  
2. 从 `sqrt_area` 向下递减遍历 `w`，因为我们希望 `L` 与 `W` 越接近越好，**越靠近 √area 的因子** 就越满足“差距最小”。  
3. 第一次遇到 `area % w == 0` 时，`w` 就是答案的宽度，`l = area // w` 是对应的长度，直接返回。  

这样最多检查 `√area` 次，**时间从 O(area) 降到 O(√area)**，在 `area ≤ 10⁷` 时最多只遍历约 `3162` 次，几乎可以忽略不计。

#### 代码（Python）

```python
import math
from typing import List

def constructRectangle(area: int) -> List[int]:
    """
    只在 sqrt(area) 以下搜索因子，第一次找到的即为最优解。
    """
    # 计算整数平方根，等价于 floor(sqrt(area))
    w = int(math.isqrt(area))          # 最大可能的宽度
    while w > 0:                       # 向下遍历，直到找到合法的因子
        if area % w == 0:              # 能整除说明 w 是合法宽度
            l = area // w              # 对应的长度
            return [l, w]              # 直接返回，满足 L >= W 且差距最小
        w -= 1                         # 继续向下尝试更小的宽度
    # 理论上永远不会走到这里，因为 1 总是因子
    return [area, 1]
```

#### 复杂度  

- **时间复杂度**：`O(√area)` —— 只遍历至 `√area`，对 `area = 10⁷` 而言约 `3162` 次，远快于一千万次。  
- **空间复杂度**：`O(1)` —— 只用了常数个整数变量。

---

## 心得  

- **核心技巧**：利用数学性质把搜索范围从 `area` 缩到 `√area`，即“**只在平方根以内找因子**”。  
- **适用题型**：  
  1. “找两个数的乘积等于给定值且差最小”——如本题、LeetCode 1015（可被 K 整除的最小整数）中涉及因子搜索。  
  2. “把一个数拆分成两个因子，使得某种代价最小”——如求最接近正方形的矩形、最小化周长等。  
- **一句话总结解题钥匙**：**“先把问题限制在平方根范围，再从大到小找第一个因子”。**

---

## 反思  

- **第一反应**：直接枚举所有可能的宽度，写一个 `for i in range(1, area+1)` 的循环。  
- **最容易踩的坑**：  
  - 忘记 **`L ≥ W`** 的约束，导致返回的顺序颠倒。  
  - 没有利用 **`W ≤ √area`** 的限制，导致超时。  
  - 对 **`area = 1`** 这种极小值忘记处理，实际上 `sqrt(1)=1`，仍然能正常返回 `[1,1]`。  
- **下次遇到同类题**，第一步应该想到：**“先用数学分析把搜索空间压缩到根号级别”，然后从最有可能的点（如 √area）开始搜索**。