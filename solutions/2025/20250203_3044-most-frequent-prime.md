# #3044. 最常出现的质数 / Most Frequent Prime

> 难度：中等 · 标签：Array、Hash Table、Math、Matrix、Counting、Enumeration、Number Theory · [LeetCode 链接](https://leetcode.com/problems/most-frequent-prime/)

---

## 题目（英文原版）

**Description**

You are given a m x n 0-indexed 2D matrix mat. From every cell, you can create numbers in the following way:
Return the most frequent prime number greater than 10 out of all the numbers created by traversing the matrix or -1 if no such prime number exists. If there are multiple prime numbers with the highest frequency, then return the largest among them.
Note: It is invalid to change the direction during the move.

**Examples**

**Example 1:**

```
Input: mat = [[1,1],[9,9],[1,1]]
Output: 19
Explanation: 
From cell (0,0) there are 3 possible directions and the numbers greater than 10 which can be created in those directions are:
East: [11], South-East: [19], South: [19,191].
Numbers greater than 10 created from the cell (0,1) in all possible directions are: [19,191,19,11].
Numbers greater than 10 created from the cell (1,0) in all possible directions are: [99,91,91,91,91].
Numbers greater than 10 created from the cell (1,1) in all possible directions are: [91,91,99,91,91].
Numbers greater than 10 created from the cell (2,0) in all possible directions are: [11,19,191,19].
Numbers greater than 10 created from the cell (2,1) in all possible directions are: [11,19,19,191].
The most frequent prime number among all the created numbers is 19.
```

**Example 2:**

```
Input: mat = [[7]]
Output: -1
Explanation: The only number which can be formed is 7. It is a prime number however it is not greater than 10, so return -1.
```

**Example 3:**

```
Input: mat = [[9,7,8],[4,6,5],[2,8,6]]
Output: 97
Explanation: 
Numbers greater than 10 created from the cell (0,0) in all possible directions are: [97,978,96,966,94,942].
Numbers greater than 10 created from the cell (0,1) in all possible directions are: [78,75,76,768,74,79].
Numbers greater than 10 created from the cell (0,2) in all possible directions are: [85,856,86,862,87,879].
Numbers greater than 10 created from the cell (1,0) in all possible directions are: [46,465,48,42,49,47].
Numbers greater than 10 created from the cell (1,1) in all possible directions are: [65,66,68,62,64,69,67,68].
Numbers greater than 10 created from the cell (1,2) in all possible directions are: [56,58,56,564,57,58].
Numbers greater than 10 created from the cell (2,0) in all possible directions are: [28,286,24,249,26,268].
Numbers greater than 10 created from the cell (2,1) in all possible directions are: [86,82,84,86,867,85].
Numbers greater than 10 created from the cell (2,2) in all possible directions are: [68,682,66,669,65,658].
The most frequent prime number among all the created numbers is 97.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 6
- 1 <= mat[i][j] <= 9

---

## 题目（中文翻译）

**描述**  
给定一个 $m \times n$、**0 索引**（0-indexed）的二维矩阵 `mat`。从每个单元格（cell）出发，你可以沿任意固定方向（不允许在移动过程中改变方向）依次拼接经过的数字，形成一个整数。  

返回所有可能形成的整数中 **大于 10 的质数（prime number）** 出现次数最多的那个。如果不存在满足条件的质数，返回 `-1`。若有多个质数出现次数相同且为最高频率，则返回其中数值最大的那个。

> **注意**：在移动过程中不能改变方向。

**约束条件**  
- $m = \text{mat}.length$  
- $n = \text{mat}[i].length$  
- $1 \le m, n \le 6$  
- $1 \le \text{mat}[i][j] \le 9$

**示例**

> 示例 1  
> ```  
> Input: mat = [[1,1],[9,9],[1,1]]  
> Output: 19  
> Explanation:  
> 从单元格 (0,0) 出发，有 3 种可能的方向，沿这些方向能够形成的 **大于 10** 的数字为：  
> - 向东（East）: [11]  
> - 向东南（South-East）: [19]  
> - 向南（South）: [19, 191]  
>  
> 从单元格 (0,1) 的所有可能方向能够形成的 **大于 10** 的数字为：  
> [19, 191, 19, 11]。  
> （后续省略）  
> ```

> 示例 2  
> ```  
> Input: mat = [[7]]  
> Output: -1  
> Explanation: 唯一能够形成的数字是 7。虽然 7 是质数，但它 **不大于 10**，因此返回 -1。  
> ```

> 示例 3  
> ```  
> Input: mat = [[9,7,8],[4,6,5],[2,8,6]]  
> Output: 97  
> Explanation:  
> 从单元格 (0,0) 的所有可能方向能够形成的 **大于 10** 的数字为：  
> [97, 978, 96, 966, 94, 942]。  
> 从单元格 (0,1) 的所有可能方向能够形成的 **大于 10** 的数字为：  
> [78, 75, 76, 768, 74, 79]。  
> 从单元格 (0,2) 的所有可能方向能够形成的 **大于 10** 的数字为：  
> [85, 856, 86, 862, 87, 879]。  
> （后续省略）  
> ```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「所有可能的数字」全部枚举出来，然后把大于 10 的素数挑出来计数，最后挑出出现次数最多的那个（若出现次数相同则挑最大的）。

- **遍历起点**：矩阵里每一个格子都可以作为起点。把它想象成一张纸上的起笔点，后面要往不同方向「写」数字。
- **遍历方向**：从一个格子出发，数字只能沿 **一条直线** 向前走，不能转弯。这里有 8 种可能的方向（上下左右以及四个对角线），可以把它们想象成指南针的 8 个指向。  
  - 例如向东（`(0, +1)`）就是「一直往右写」；向西南（`(+1, -1)`）就是「往左下斜着写」。
- **沿方向累加数字**：在选定的方向上，一次走一步，把经过的格子里的数字拼接到一起形成一个更长的整数。  
  - 把数字拼接可以用 `num = num * 10 + digit`，这相当于在十进制里「在后面加一位」。
- **收集满足条件的数**：每走一步，就得到一个新的整数。只要它 **大于 10**，就检查它是不是素数（后面会说怎么检查），如果是就把它加入计数表。  
  - 计数表可以用 **哈希表**（Python 的 `defaultdict(int)`）来实现，哈希表就像一本“字典”，键是数字，值是出现次数。
- **遍历结束**：把所有起点、所有方向、所有长度的数字都检查完后，哈希表里就记录了每个符合条件的素数出现了多少次。遍历哈希表找出出现次数最高的素数（出现次数相同则取更大的那个）即为答案。

> **为什么正确？**  
> 题目要求“所有可能的数字”，而我们的枚举正好覆盖了每一种「起点 + 方向 + 步数」的组合，没有遗漏，也没有重复计数（同一个数字在同一次遍历里只会出现一次）。所以统计的频率就是题目要求的频率。

#### 代码（Python）

```python
from collections import defaultdict
from math import isqrt
from typing import List

def is_prime(x: int) -> bool:
    """判断正整数 x 是否为素数（只会被 2~sqrt(x) 的整数整除）"""
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2               # 只有 2 是偶数素数
    # 只需要检查奇数因子
    limit = isqrt(x)                # sqrt(x) 的整数部分
    for d in range(3, limit + 1, 2):
        if x % d == 0:
            return False
    return True

def most_frequent_prime(mat: List[List[int]]) -> int:
    m, n = len(mat), len(mat[0])
    # 8 个方向的行、列增量（上、右上、右、右下、下、左下、左、左上）
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)]

    cnt = defaultdict(int)   # prime -> 出现次数

    for i in range(m):
        for j in range(n):
            # 以 (i,j) 为起点，尝试 8 种方向
            for dr, dc in dirs:
                r, c = i, j
                num = 0
                # 沿当前方向一直走，直到走出矩阵边界
                while 0 <= r < m and 0 <= c < n:
                    num = num * 10 + mat[r][c]   # 把当前格子数字拼到末尾
                    if num > 10 and is_prime(num):
                        cnt[num] += 1            # 记录一次出现
                    r += dr
                    c += dc

    # 在哈希表里找出现次数最多的素数
    best_prime = -1
    best_freq = 0
    for prime, freq in cnt.items():
        if freq > best_freq or (freq == best_freq and prime > best_prime):
            best_prime = prime
            best_freq = freq

    return best_prime
```

#### 复杂度  

- **时间复杂度**：  
  - 外层两层遍历所有格子：`m * n` 次。  
  - 每个格子尝试 8 种方向，每条方向最多走 `max(m, n)` 步（因为矩阵最宽或最高的长度）。  
  - 所以总的步数是 `O(m * n * 8 * max(m, n)) = O(m * n * max(m, n))`。  
  - 在本题的约束 `m, n ≤ 6` 下，这个数最多是 `6*6*6 = 216` 步，几乎可以忽略不计。  
  - 素数判定 `is_prime` 最坏要检查到 √num（num ≤ 999999），即约 1000 次，但这也是常数级别。  
  - 综合来看，整体时间是 **线性** 的，记作 `O(m * n * max(m, n))`，在题目限制下完全可以接受。

- **空间复杂度**：  
  - 计数哈希表最多存放所有出现的素数。因为数字的范围是 `10 < num ≤ 999999`，而矩阵很小，实际出现的素数数量也很少，最多 `O(m * n * max(m, n))` 个。  
  - 额外的递归/栈空间几乎为 0（我们用了循环），所以总体是 **线性** 的 `O(m * n * max(m, n))`。

---

### 2. 最优解

#### 思路  

在本题的约束下，**暴力枚举已经是最优的**。原因如下：

1. **搜索空间极小**：  
   - `m, n ≤ 6`，所以最多只有 36 个起点。  
   - 每条方向最多走 6 步，方向数固定为 8。  
   - 整体可能产生的数字数量上限只有几百个，远远小于常规「指数爆炸」的情况。

2. **没有可进一步削减的重复**：  
   - 同一个数字如果可以由不同起点或不同方向得到，它本来就应该计数多次（题目要求「出现次数」），所以不能去重。  
   - 任何「剪枝」或「动态规划」都无法减少本质上必须遍历的所有路径。

3. **素数检查成本可接受**：  
   - 最大数字只有 6 位，使用 `O(√num)` 的试除法足够快。  
   - 若要进一步加速，可以预先用 **埃拉托斯特尼筛** 生成 ≤ 999999 的所有素数，查询时 O(1)。但在本题规模下实现复杂度提升不值得。

因此，**保持上面的暴力实现** 已经是时间、空间最优的方案。下面给出一种稍微「优化」的写法：利用一次遍历同时完成数字拼接、边界检查和素数计数，代码结构更简洁。

#### 代码（Python）

```python
from collections import defaultdict
from math import isqrt
from typing import List

def is_prime(x: int) -> bool:
    """快速判断 x 是否为素数（仅用于 ≤ 999999 的整数）"""
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    limit = isqrt(x)
    for d in range(3, limit + 1, 2):
        if x % d == 0:
            return False
    return True

def most_frequent_prime(mat: List[List[int]]) -> int:
    m, n = len(mat), len(mat[0])
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)]

    freq = defaultdict(int)   # prime -> 次数

    for r0 in range(m):
        for c0 in range(n):
            for dr, dc in dirs:
                r, c = r0, c0
                num = 0
                while 0 <= r < m and 0 <= c < n:
                    num = num * 10 + mat[r][c]
                    if num > 10 and is_prime(num):
                        freq[num] += 1
                    r += dr
                    c += dc

    # 选出出现次数最多、且数值最大的素数
    ans, best = -1, 0
    for p, f in freq.items():
        if f > best or (f == best and p > ans):
            ans, best = p, f
    return ans
```

> **为什么仍然是最优？**  
> - 仍然是一次完整的遍历，时间复杂度仍为 `O(m·n·max(m,n))`。  
> - 代码没有使用递归或额外的缓存，空间开销最小（仅哈希表）。  
> - 若想进一步提升素数检查速度，可把所有 ≤ 999999 的素数预先筛出来放进集合 `prime_set`，`is_prime` 只需要一次哈希查询 `O(1)`，但这对本题的运行时间影响几乎为零，只是实现上稍微繁琐。

#### 复杂度  

- **时间复杂度**：`O(m * n * max(m, n))`，与暴力解相同。  
- **空间复杂度**：`O(K)`，其中 `K` 为出现的素数种类数（最坏仍是 `O(m * n * max(m, n))`），哈希表之外几乎不占额外空间。

---

## 心得

- **核心技巧**：**枚举所有起点 + 8 条固定方向 + 逐步拼接数字**，配合 **哈希表计数** 与 **素数判定**。  
- **适用的题型**：  
  1. **矩阵路径数字**（如「从左上到右下只能向右或下」形成的数）。  
  2. **固定方向的字符/数字串统计**（如「在棋盘上找所有单词」的变形）。  
  3. **遍历所有直线子序列**（如「找所有子数组的最大和」的二维版）。  
- **一句话总结**：  
  “在小规模矩阵里，直接遍历每个格子、每个方向、每个长度，配合哈希表统计，就是最快的解法。”

---

## 反思

- **第一反应**：看到「从每个格子、沿任意方向」就想到 **枚举**，随后担心会不会出现指数级别的爆炸。  
- **最容易踩的坑**：  
  1. **忘记「不能转向」**：必须保持同一方向走到底，否则会产生错误的数字。  
  2. **数字拼接错误**：直接使用字符串拼接会导致额外的转换开销，使用 `num = num * 10 + digit` 更高效且直观。  
  3. **边界条件**：走到矩阵外时要立刻停止，否则会产生索引错误。  
  4. **素数判定范围**：只检查 `>10` 的数，忘记这一步会把 2、3、5、7 错误计入答案。  
- **下次遇到同类题**：第一步先 **估算搜索空间大小**（矩阵大小、最大路径长度），如果仍在几千级别以内，就直接 **暴力枚举 + 哈希统计**；若空间太大，再考虑 **预处理（如前缀哈希、动态规划）** 或 **剪枝**。