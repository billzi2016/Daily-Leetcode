# #3200. 三角形的最大高度 / Maximum Height of a Triangle

> 难度：简单 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-height-of-a-triangle/)

---

## 题目（英文原版）

**Description**

You are given two integers red and blue representing the count of red and blue colored balls. You have to arrange these balls to form a triangle such that the 1st row will have 1 ball, the 2nd row will have 2 balls, the 3rd row will have 3 balls, and so on.
All the balls in a particular row should be the same color, and adjacent rows should have different colors.
Return the maximum height of the triangle that can be achieved.

**Examples**

**Example 1:**

```
Input: red = 2, blue = 4
Output: 3
Explanation:

The only possible arrangement is shown above.
```

**Example 2:**

```
Input: red = 2, blue = 1
Output: 2
Explanation:
The only possible arrangement is shown above.
```

**Example 3:**

```
Input: red = 1, blue = 1
Output: 1
```

**Example 4:**

```
Input: red = 10, blue = 1
Output: 2
Explanation:
The only possible arrangement is shown above.
```

**Constraints**

- 1 <= red, blue <= 100

---

## 题目（中文翻译）

给定两个整数 `red` 和 `blue`，分别表示红色球和蓝色球的数量。需要将这些球排成一个三角形，使得第 1 行放 1 个球，第 2 行放 2 个球，第 3 行放 3 个球，依此类推。  
同一行内的所有球必须颜色相同，且相邻的两行颜色必须不同。  
返回可以构造的三角形的最大高度。

## 示例

### 示例 1  
**输入**: `red = 2, blue = 4`  
**输出**: `3`  
**解释**:  

唯一可能的排列如上图所示，最高可以到第 3 行。

### 示例 2  
**输入**: `red = 2, blue = 1`  
**输出**: `2`  
**解释**:  

唯一可能的排列如上图所示，最高可以到第 2 行。

### 示例 3  
**输入**: `red = 1, blue = 1`  
**输出**: `1`  

### 示例 4  
**输入**: `red = 10, blue = 1`  
**输出**: `2`  
**解释**:  

唯一可能的排列如上图所示，最高只能到第 2 行。

## 约束条件

- `1 <= red, blue <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**从第一层开始，一层一层往上搭**。  
- 第 1 行放 1 颗球，第 2 行放 2 颗球，第 3 行放 3 颗球 …… 这样每行的球数恰好等于行号。  
- 同一行的球必须颜色相同，且相邻两行颜色必须不同。  

我们只需要考虑两种起始颜色：

1. **红球在最上面**（第 1 行用红球），随后第 2 行用蓝球，第 3 行再用红球……  
2. **蓝球在最上面**（第 1 行用蓝球），随后第 2 行用红球，第 3 行再用蓝球……  

对每一种起始颜色，依次检查第 `i` 行需要的球数 `i` 是否足够。如果当前颜色的球数剩余 `< i`，说明已经搭不下去了，当前的行号 `i‑1` 就是可以得到的最大高度。  

> **类比**：想象你在排队买票，手里有两种不同面值的票（红票、蓝票），每买一张票需要的面值随排队顺序递增。只要手里对应面值的票够付，就可以继续排下去。

这种做法一定能得到答案，因为我们没有跳过任何可能的行号——只要有足够的球，就一定会把它用上。

#### 代码（Python）  
```python
def maxHeight_bruteforce(red: int, blue: int) -> int:
    """
    暴力模拟，两次尝试：红球在顶、蓝球在顶
    """
    def height(start_red: bool) -> int:
        # start_red 为 True 表示第 1 行用红球
        r, b = red, blue          # 复制一份计数，防止相互影响
        h = 0                     # 已经成功搭好的层数
        i = 1                     # 当前层需要的球数（等于层号）
        while True:
            if start_red:        # 当前层应使用红球
                if r < i:        # 红球不够，结束
                    break
                r -= i           # 用掉 i 颗红球
            else:                # 当前层应使用蓝球
                if b < i:
                    break
                b -= i
            h += 1                # 成功搭好一层
            i += 1                # 下一层需要的球数加 1
            start_red = not start_red   # 颜色交替
        return h

    # 分别尝试两种起始颜色，取较大的高度
    return max(height(True), height(False))
```

#### 复杂度  
- **时间复杂度**：`O(h)`，其中 `h` 为最终能搭的层数。因为每一层只检查一次，层数最多约为 `√(red+blue)`（因为 1+2+…+h ≈ h²/2），所以在最坏情况下是 `O(√N)`，这里的 `N` 为球的总数。  
- **空间复杂度**：`O(1)`，只用了若干个整数变量，和输入规模无关。

---

### 2. 最优解  

#### 思路  
暴力解已经很快（`O(√N)`），但我们可以把 **“一层一层试”** 改成 **“直接算能不能搭到第 h 层”**，再用二分查找快速定位最大 `h`。  

关键在于**统计每种颜色到底需要多少球**。  
假设第 1 行使用红球（即红球在顶），则红球出现的行号是 **奇数**：`1, 3, 5, …`，蓝球出现的行号是 **偶数**：`2, 4, 6, …`。  

- 奇数行的和：`1 + 3 + 5 + … + (2·k‑1) = k²`（**奇数求和等于平方**，这里的 `k` 为奇数行的数量）。  
- 偶数行的和：`2 + 4 + 6 + … + 2·k = k·(k+1)`（偶数行可以看成 `2·(1+2+…+k)`，而 `1+2+…+k = k(k+1)/2`）。

如果总层数为 `h`，则  
- 红球的行数 = `ceil(h/2)`（向上取整），蓝球的行数 = `floor(h/2)`（向下取整）。  
- 对应的球需求：
  - 红球需要 `ceil(h/2)²` 颗（奇数行求和）  
  - 蓝球需要 `floor(h/2)·(floor(h/2)+1)` 颗（偶数行求和）

当起始颜色相反时，只需要把红、蓝的需求互换即可。

于是我们可以 **二分** `h`（从 0 到 `sqrt(red+blue)*2` 的安全上界），检查上述两套需求是否都满足，取最大的合法 `h`。

> **类比**：把每层需要的球看成“费用”，我们想买尽可能多的层，但每种费用只能用对应颜色的“预算”。二分查找就像在找最大的“可买层数”，每次检查只需要算出两种预算是否足够。

#### 代码（Python）  
```python
def maxHeight_opt(red: int, blue: int) -> int:
    """
    使用二分查找直接计算最大高度，时间 O(log N)，空间 O(1)。
    """
    # 辅助函数：判断在以 start_red 为顶的情况下，高度 h 是否可行
    def can_build(h: int, start_red: bool) -> bool:
        # 计算红、蓝各自需要的层数
        red_rows = (h + 1) // 2 if start_red else h // 2   # ceil(h/2) 或 floor(h/2)
        blue_rows = h // 2 if start_red else (h + 1) // 2

        # 对应的球数需求
        need_red = red_rows * red_rows                     # 奇数行求和 = k^2
        need_blue = blue_rows * (blue_rows + 1)           # 偶数行求和 = k*(k+1)

        return need_red <= red and need_blue <= blue

    # 二分搜索上界：当所有球都用同一种颜色时，最高层数约为 sqrt(2*total)
    total = red + blue
    hi = int((2 * total) ** 0.5) + 2   # 足够大的安全上界
    lo = 0
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_build(mid, True) or can_build(mid, False):
            ans = mid          # mid 合法，尝试更大
            lo = mid + 1
        else:
            hi = mid - 1       # 不合法，减小高度
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(log H)`，其中 `H` 为答案的最大可能高度（约为 `√(red+blue)`），二分查找只需要对数次数的检查。相比暴力的 `O(√N)`，在大输入时更快。  
- **空间复杂度**：`O(1)`，只用了常数个整数变量。

---

## 心得  

- **核心技巧**：把“每行颜色交替”转化为 **奇偶行求和**，利用数学公式（奇数和 = `k²`，偶数和 = `k·(k+1)`）快速算出每种颜色需要的球数。  
- **适用场景**：  
  1. 需要 **交替使用两种资源**，且每一步消耗递增的情形（如交替使用两种硬币支付递增金额）。  
  2. “层数”或“长度”随层号线性增长，且资源分配固定模式的题目（如 **Maximum Height of a Triangle**、**Construct Staircase**）。  
- **一句话总结**：把层号的奇偶划分为两组，用平方或平方+线性公式直接求和，然后二分确定最大可行层数。  

---

## 反思  

- **第一反应**：看到“每行球数递增、颜色交替”，立刻想到**从上往下逐层模拟**，因为这样最直观。  
- **最容易踩的坑**：  
  - 忘记两种起始颜色都要尝试，导致在某些输入下得到错误的高度。  
  - 计算偶数层球数时写成 `k²`（其实是奇数层），导致需求估算偏小/偏大。  
  - 边界条件：当某种颜色的球数为 `0` 时，只能有 **1 层**（因为第一层必须使用某种颜色），代码中要避免除零或负数判断。  
- **下次类似题目**：先**写出递增需求的前缀和公式**（或直接模拟），再判断是否需要二分或其他优化——**“先求和再比较”**往往是关键第一步。