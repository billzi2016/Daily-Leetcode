# #2125. 银行中的激光束数量 / Number of Laser Beams in a Bank

> 难度：中等 · 标签：Array、Math、String、Matrix · [LeetCode 链接](https://leetcode.com/problems/number-of-laser-beams-in-a-bank/)

---

## 题目（英文原版）

**Description**

Anti-theft security devices are activated inside a bank. You are given a 0-indexed binary string array bank representing the floor plan of the bank, which is an m x n 2D matrix. bank[i] represents the ith row, consisting of '0's and '1's. '0' means the cell is empty, while'1' means the cell has a security device.
There is one laser beam between any two security devices if both conditions are met:
Laser beams are independent, i.e., one beam does not interfere nor join with another.
Return the total number of laser beams in the bank.

**Examples**

**Example 1:**

```
Input: bank = ["011001","000000","010100","001000"]
Output: 8
Explanation: Between each of the following device pairs, there is one beam. In total, there are 8 beams:
 * bank[0][1] -- bank[2][1]
 * bank[0][1] -- bank[2][3]
 * bank[0][2] -- bank[2][1]
 * bank[0][2] -- bank[2][3]
 * bank[0][5] -- bank[2][1]
 * bank[0][5] -- bank[2][3]
 * bank[2][1] -- bank[3][2]
 * bank[2][3] -- bank[3][2]
Note that there is no beam between any device on the 0th row with any on the 3rd row.
This is because the 2nd row contains security devices, which breaks the second condition.
```

**Example 2:**

```
Input: bank = ["000","111","000"]
Output: 0
Explanation: There does not exist two devices located on two different rows.
```

**Constraints**

- m == bank.length
- n == bank[i].length
- 1 <= m, n <= 500
- bank[i][j] is either '0' or '1'.

---

## 题目（中文翻译）

防盗安全装置已在银行内部激活。给定一个 **0 索引** 的二进制字符串数组 `bank`，表示银行的平面图，它是一个 `m × n` 的二维矩阵。`bank[i]` 表示第 `i` 行，由 `'0'` 和 `'1'` 组成。`'0'` 表示该单元格为空，`'1'` 表示该单元格中有安全装置。

如果满足以下两个条件，则任意两个安全装置之间会有一束激光束（laser beam）：

- 激光束是相互独立的，即一束不会干扰或与另一束相连。

返回银行中激光束的总数。

### 示例

**示例 1**  
```text
Input: bank = ["011001","000000","010100","001000"]
Output: 8
Explanation: 在以下每一对装置之间都有一束激光，总计 8 条激光束：
 * bank[0][1] -- bank[2][1]
 * bank[0][1] -- bank[2][3]
 * bank[0][2] -- bank[2][1]
 * bank[0][2] -- bank[2][3]
 * bank[0][5] -- bank[2][1]
 * bank[0][5] -- bank[2][3]
 * bank[2][1] -- bank[3][2]
 * bank[2][3] -- bank[3][2]
注意，...
```

**示例 2**  
```text
Input: bank = ["000","111","000"]
Output: 0
Explanation: 不存在位于不同行的两个装置，因此没有激光束。
```

### 约束条件

- `m == bank.length`
- `n == bank[i].length`
- `1 <= m, n <= 500`
- `bank[i][j]` 仅为 `'0'` 或 `'1'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们先把题目拆开来看：  

- 银行的平面图是一个 `m × n` 的二进制矩阵，`1` 表示该格子里有安防装置，`0` 表示空格。  
- 两个装置之间**如果**满足两个条件，就会形成一条激光束  
  1. 两个装置在 **不同行**（同一行的装置之间不算）  
  2. 这两行之间 **没有其他行** 含有装置（换句话说，只能在“相邻的有装置的行”之间产生激光束）  

于是我们可以把每一行看成一个**装置的集合**，只要把相邻（在行号上相邻且两行都有装置）的两行的装置两两配对，就得到激光束的数量。

> **类比**：把每一行的装置想象成一本书的章节标题。激光束只会在“相邻的有标题的章节”之间产生，标题之间的配对数量等于左边章节标题数 × 右边章节标题数。

最直观的做法是：

1. 对每一行，统计该行中 `'1'` 的个数 `cnt[i]`（这一步是 O(n)）。
2. 对所有 **行对** `(i, j)`（`i < j`）检查：  
   - 如果 `cnt[i] == 0` 或 `cnt[j] == 0`，显然这两行之间没有激光束，直接跳过。  
   - 再检查 `i` 与 `j` 之间是否有其他行的 `cnt[k] > 0`（即是否有装置行夹在中间）。如果有，则这两行不算相邻，跳过。  
   - 否则，这两行是“相邻的有装置的行”，激光束数量为 `cnt[i] * cnt[j]`，累加到答案中。  

这种做法把每一对行都枚举了一遍，最坏情况下会遍历 `m·(m-1)/2 ≈ O(m²)` 对行，且每对行内部还要再遍历一次中间的行来判断是否相邻，整体时间复杂度是 **O(m³)**（在实现时可以把相邻判定提前到 O(1)，但这里先把最笨的思路写出来，帮助大家理清“先暴力后优化”的过程）。  

空间上我们只需要保存每行的装置个数 `cnt`，即 **O(m)** 的额外空间。

#### 代码（Python）

```python
from typing import List

def number_of_beams_bruteforce(bank: List[str]) -> int:
    m = len(bank)                     # 行数
    # 1. 统计每行的装置个数
    cnt = [row.count('1') for row in bank]   # O(m * n)

    total = 0
    # 2. 枚举所有行对 (i, j)
    for i in range(m):
        if cnt[i] == 0:               # 第 i 行没有装置，直接跳过
            continue
        for j in range(i + 1, m):
            if cnt[j] == 0:           # 第 j 行没有装置，直接跳过
                continue

            # 检查 i 与 j 之间是否有其他装置行
            has_mid = False
            for k in range(i + 1, j):
                if cnt[k] > 0:        # 中间出现了装置行，i、j 不是相邻的有装置行
                    has_mid = True
                    break
            if has_mid:
                continue

            # i、j 是相邻的有装置行，激光束数量 = cnt[i] * cnt[j]
            total += cnt[i] * cnt[j]

    return total
```

#### 复杂度

- **时间复杂度**：`O(m³)`（最坏情况下需要三层循环：行对枚举 + 中间行检查）。  
  - 这里的 `O(m³)` 可以想象成“把 `m` 层楼的每两层之间都检查一次，还要在每次检查时再走一遍中间的楼层”。在 `m ≤ 500` 时已经会超时。
- **空间复杂度**：`O(m)`（只保存每行装置数量的数组）。  
  - 类似于我们只在桌面上放了 `m` 张纸来记录每行的统计信息。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**慢点**主要集中在两个地方：

1. **枚举所有行对**：我们其实只需要考虑“相邻的有装置的行”，而不是所有行对。  
2. **判断相邻**：在暴力解里，每次都要遍历中间的行来判断是否相邻，这也是不必要的重复劳动。

**关键观察**：  
- 同一行内部的装置互不影响，它们只会分别与下一行（最近的有装置的行）产生激光束。  
- 因此，只要把每行的装置数量记下来，**依次遍历**这些数量，跳过为 `0` 的行，**相邻的两个非零数量**之间的激光束数目就是它们的乘积。  
- 把所有相邻非零行的乘积加起来，就是答案。

这一步把原来的 `O(m²)`（甚至 `O(m³)`）直接压缩到 **一次线性遍历**，时间复杂度降到 `O(m)`。

下面把这个思路拆解成更细的步骤，方便初学者理解：

1. **预处理**：遍历 `bank`，统计每行 `'1'` 的个数，得到数组 `cnt`。这一步是 `O(m·n)`，因为每行要看 `n` 个字符。  
2. **线性累加**：维护一个变量 `prev`，记录**最近一次出现装置的行的装置数量**。遍历 `cnt`：  
   - 如果当前行 `cnt[i] == 0`，说明这行没有装置，直接跳过，不改变 `prev`。  
   - 否则（`cnt[i] > 0`），说明找到了一个**相邻的有装置的行**：`prev`（上一次有装置的行） 与 `cnt[i]`（当前行）之间会产生 `prev * cnt[i]` 条激光束。把这个乘积加入答案，然后把 `prev` 更新为 `cnt[i]`（因为当前行现在成为“最近的有装置的行”。）  
3. 循环结束后，`ans` 就是所有激光束的总数。

> **类比**：把每一行的装置数量看成一串数字，`0` 像是“断开的电线”。我们只关心**相邻的非零数字**之间的乘积，就像在一条链子上，每两个相邻的节点相连，连接数等于两端的重量相乘。

#### 代码（Python）

```python
from typing import List

def number_of_beams(bank: List[str]) -> int:
    """
    最优解：只遍历一次数组，时间 O(m * n)，空间 O(1)（不计输入本身）。
    """
    ans = 0          # 累计激光束数量
    prev = 0         # 最近一次出现装置的行的装置数量

    for row in bank:               # O(m) 行
        cnt = row.count('1')       # 统计当前行的装置个数，O(n) 字符遍历
        if cnt == 0:
            continue               # 这一行没有装置，跳过
        # 当前行与最近的有装置的行构成相邻的有装置行
        ans += prev * cnt          # 乘积即为激光束数
        prev = cnt                 # 更新最近的装置行数量

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - 只遍历一次输入的每个字符来统计每行的 `'1'` 数，然后再线性遍历 `m` 行做乘积累加。  
  - 对于 `m, n ≤ 500`，最多只有 `250,000` 次字符检查，完全在毫秒级完成。  
- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了几个整数变量 `ans`、`prev`、`cnt`，没有额外的数组或矩阵。  
  - 相比暴力解的 `O(m)`，我们省掉了保存整行计数的数组（其实在实现时直接在遍历中统计也可以），更节省空间。

---

## 心得

- **核心技巧**：把二维矩阵压缩成“一维装置计数”，利用“相邻非零行”这一结构特性，只需一次线性遍历即可完成计数。  
- **适用场景**：  
  1. **行/列间的配对计数**（如 LeetCode 1812 *Maximum Sum of Rectangle No Larger Than K* 的行前缀压缩）  
  2. **相邻非零段的乘积或和**（如 “Maximum Product of Splitted Binary Tree” 中的相邻子树计数）  
  3. **只关注非零元素的序列**（如 “Maximum Area of Island” 中的连续岛屿计数）  
- **一句话总结**：**把二维问题转化为“一维相邻非零段的乘积求和”，一次遍历搞定**。

---

## 反思

- **第一反应**：看到“激光束只在相邻的有装置的行之间”，立刻想到**统计每行装置数**，然后**相邻乘积**，这就是最直接的思路。  
- **最容易踩的坑**：  
  - 忽略了“相邻的行”指的是**最近的有装置的行**，而不是行号相差 1（两行之间可能全是 `0`）。  
  - 在统计每行装置数时忘记把 `'0'` 行跳过，导致错误地把 `0` 参与乘积，答案会变成 `0`。  
  - 边界情况：整个银行只有一行有装置，或者全是 `0`，答案应该是 `0`，代码需要正确处理 `prev` 初始值。  
- **下次遇到同类题**：  
  - **第一步**：把二维/高维结构“投影”到一维（统计每行/列的特征值）。  
  - **第二步**：明确相邻/相对关系的定义（是物理相邻还是最近非零相邻），再决定是**遍历所有组合**还是**只看相邻配对**。  
  - **第三步**：寻找是否可以“一次遍历+累计”来完成，避免双层或三层循环。