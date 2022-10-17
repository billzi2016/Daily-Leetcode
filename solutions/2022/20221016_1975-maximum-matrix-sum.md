# #1975. 矩阵最大和 / Maximum Matrix Sum

> 难度：中等 · 标签：Array、Greedy、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-matrix-sum/)

---

## 题目（英文原版）

**Description**

You are given an n x n integer matrix. You can do the following operation any number of times:
Two elements are considered adjacent if and only if they share a border.
Your goal is to maximize the summation of the matrix's elements. Return the maximum sum of the matrix's elements using the operation mentioned above.

**Examples**

**Example 1:**

```
Input: matrix = [[1,-1],[-1,1]]
Output: 4
Explanation: We can follow the following steps to reach sum equals 4:
- Multiply the 2 elements in the first row by -1.
- Multiply the 2 elements in the first column by -1.
```

**Example 2:**

```
Input: matrix = [[1,2,3],[-1,-2,-3],[1,2,3]]
Output: 16
Explanation: We can follow the following step to reach sum equals 16:
- Multiply the 2 last elements in the second row by -1.
```

**Constraints**

- n == matrix.length == matrix[i].length
- 2 <= n <= 250
- -105 <= matrix[i][j] <= 105

---

## 题目（中文翻译）

给定一个 `n × n` 的整数矩阵 `matrix`。你可以任意次执行以下操作：

- 选取任意一行或任意一列，将其中所有元素同时乘以 `-1`。

两个元素 **相邻（adjacent）** 当且仅当它们共享一条边。

你的目标是通过上述操作，使矩阵中所有元素的和达到最大。返回能够得到的最大和。

## 示例

### 示例 1
**输入**  
```text
matrix = [[1,-1],[-1,1]]
```

**输出**  
```text
4
```

**解释**  
我们可以按以下步骤得到和为 `4`：

1. 将第一行的两个元素乘以 `-1`。  
2. 将第一列的两个元素乘以 `-1`。

### 示例 2
**输入**  
```text
matrix = [[1,2,3],[-1,-2,-3],[1,2,3]]
```

**输出**  
```text
16
```

**解释**  
我们可以按以下步骤得到和为 `16`：

- 将第二行的后两个元素乘以 `-1`。

## 约束条件

- `n == matrix.length == matrix[i].length`
- `2 <= n <= 250`
- `-10^5 <= matrix[i][j] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个格子的正负都枚举一遍**，看哪一种组合能得到最大的矩阵和。  
- **数据结构**：我们可以把矩阵展平成一个一维数组 `flat`，长度为 `n*n`，这样每个格子对应一个下标。  
- **生活化类比**：把矩阵想成一排排的灯泡，每盏灯可以是亮（正）也可以是灭（负），我们想把所有灯调到“亮”。暴力做法就是把每盏灯的开关都尝试打开或关闭，看看哪一种最亮。  
- **为什么正确**：遍历了所有可能的正负分配，自然不会漏掉最优的那一种。  

显然，这种方法的时间会非常久，因为 **每个格子有两种状态**（正或负），总共要尝试 `2^(n*n)` 种情况。

#### 代码（Python）

```python
from itertools import product
from typing import List

def max_matrix_sum_bruteforce(matrix: List[List[int]]) -> int:
    n = len(matrix)
    # 把矩阵拉平成一维，方便枚举
    flat = [matrix[i][j] for i in range(n) for j in range(n)]

    best = -10**18  # 记录最大和

    # product 会生成 0/1 的所有排列，0 表示不翻转，1 表示翻转一次（乘以 -1）
    for signs in product([1, -1], repeat=n * n):
        cur_sum = 0
        for val, sgn in zip(flat, signs):
            cur_sum += val * sgn          # 按当前的符号计算和
        best = max(best, cur_sum)        # 更新最大值

    return best
```

> **注释**  
> - 第 4 行把矩阵变成一维列表，后面枚举时更方便。  
> - 第 9 行 `product([1, -1], repeat=n*n)` 产生所有 `2^(n*n)` 种符号组合。  
> - 第 12‑13 行把每个元素乘上对应的符号，累加得到当前矩阵和。  

#### 复杂度  

- **时间复杂度**：`O(2^{n^2} * n^2)`  
  - `2^{n^2}` 是所有符号组合的数量，`n^2` 是每次遍历矩阵求和的代价。  
  - 用大白话说，就是“指数级的增长”，即使 `n=2`（4 个格子）也要检查 16 种情况，`n=5`（25 个格子）就要检查 33,554,432 种，根本不可行。  
- **空间复杂度**：`O(n^2)`  
  - 只用了一个长度为 `n^2` 的一维数组来存放矩阵的值，以及 `product` 生成的临时迭代器。

> 暴力解只能用来验证思路或在极小的测试数据上跑通，真正解题需要更聪明的办法。

---

### 2. 最优解

#### 思路  

**观察操作本质**：一次操作可以把 **两个相邻格子**（上下或左右相邻）同时乘以 `-1`。  
这等价于“把这两个格子的符号翻转”。翻转两个格子会改变负数的个数 **但不会改变负数个数的奇偶性**（因为负数个数增减了 0、2 或 -2，都是偶数）。

> **类比**：想象一盘棋子，每颗棋子正面朝上是“正”，背面朝上是“负”。一次操作是把两颗相邻的棋子一起翻面。翻面两颗会把“负”的总数加 2、减 2 或保持不变——总是保持 **奇偶性不变**。

因此，**整个矩阵中负数的奇偶性是不可改变的**。我们只能在保持这个奇偶性的前提下，让矩阵的和尽可能大。

**如何让和最大？**  
- 把所有数都变成 **绝对值**（即正数），这会得到最大的理论和 `sum_abs = Σ |a[i][j]|`。  
- 但如果原始矩阵负数的个数是 **奇数**，我们只能保留 **一个**负号（因为负数个数必须保持奇数）。保留哪一个负号最合适？显然应该保留 **绝对值最小的那个**，因为它对总和的“损失”最小。  

于是得到下面的公式：

```
sum_abs = Σ |matrix[i][j]|
cnt_neg = number of elements < 0
min_abs = min |matrix[i][j]|

if cnt_neg % 2 == 0:
    answer = sum_abs
else:
    answer = sum_abs - 2 * min_abs
```

- 当负数个数是偶数时，我们可以把所有负数配对翻转，使它们全部变正，得到 `sum_abs`。  
- 当负数个数是奇数时，最好的办法是让 **最小的绝对值** 保持负号，这相当于在 `sum_abs` 基础上减去两倍的 `min_abs`（因为本来已经算作正的 `min_abs` 需要变成负，差值是 `2 * min_abs`）。

**为什么不需要考虑矩阵的形状（相邻关系）？**  
因为任意两个格子只要是相邻的，就可以翻转它们的符号。通过一系列相邻翻转，我们可以把 **任何**负号“移动”到任意位置，最终只要满足奇偶性约束，就能实现上述最优方案。换句话说，**相邻的限制不影响最终的可达性**，只影响过程的步骤数，而我们只关心结果。

#### 代码（Python）

```python
from typing import List

def max_matrix_sum(matrix: List[List[int]]) -> int:
    """
    计算在任意次数的「相邻两格同时乘 -1」操作后，矩阵元素之和的最大可能值。
    思路：保持负数个数的奇偶性不变，尽量让所有数取绝对值。
    """
    total_abs = 0          # Σ |a[i][j]|
    cnt_neg = 0            # 负数个数
    min_abs = float('inf') # 最小的绝对值

    for row in matrix:
        for v in row:
            av = abs(v)
            total_abs += av
            if v < 0:
                cnt_neg += 1
            if av < min_abs:
                min_abs = av

    # 如果负数个数是奇数，需要把最小的绝对值保留为负号
    if cnt_neg % 2 == 1:
        total_abs -= 2 * min_abs   # 从全部正的和中减去两倍的最小绝对值

    return total_abs
```

> **关键行中文注释**  
> - 第 9‑10 行累计所有元素的绝对值 `total_abs`，这相当于把每个格子都变成正数的和。  
> - 第 11‑13 行统计负数的个数 `cnt_neg`，以及记录最小的绝对值 `min_abs`。  
> - 第 19‑21 行根据负数奇偶性决定是否要「牺牲」最小的绝对值，使得负数个数保持原来的奇偶性。

#### 复杂度  

- **时间复杂度**：`O(n^2)`  
  - 只需要遍历一次矩阵，做常数次的加减和比较。用大白话说，就是“和矩阵里格子数量成正比”，即使 `n=250`（62,500 个格子）也能在毫秒级完成。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`total_abs`, `cnt_neg`, `min_abs`），不随 `n` 增长。

> 与暴力解相比，时间从指数级下降到线性级，几乎可以瞬间算完所有合法输入。

---

## 心得

- **核心技巧**：**利用操作不改变负数个数的奇偶性**，把问题转化为“所有数取绝对值后，若负数个数是奇数则扣除最小绝对值的两倍”。  
- **适用的题型**  
  1. **相邻翻转类**（如“翻转相邻两位的符号”）  
  2. **全局奇偶约束类**（如“只能改变偶数个元素的符号”）  
  3. **矩阵/数组的最大和问题**，其中操作只影响符号而不改变数值大小。  
- **一句话总结**：**保持负数奇偶性不变，尽可能把所有数变为正，唯一的“牺牲品”是最小的绝对值**。

---

## 反思

- **第一反应**：看到“相邻两格乘 -1”，立刻想到“把负数配对翻转”，于是尝试枚举所有翻转方案（暴力）。  
- **最容易踩的坑**  
  - 忘记 **奇偶性不变** 的关键限制，误以为可以把所有负数都翻正。  
  - 误把矩阵的行/列整体翻转（每次翻转 `n` 个格子）当成操作，导致公式出现 `n` 的奇偶性判断。  
  - 边界情况：矩阵中所有元素都是 `0`，此时 `min_abs` 为 `0`，公式仍然成立。  
- **下次遇到同类题**：第一步先**思考操作对“负数个数的奇偶性”有什么影响**，再决定是否需要保留某个最小绝对值的负号。这样可以快速定位最优解的方向。