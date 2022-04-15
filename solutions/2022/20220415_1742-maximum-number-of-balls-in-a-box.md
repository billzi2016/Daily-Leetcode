# #1742. 盒子中最多球的数量 / Maximum Number of Balls in a Box

> 难度：简单 · 标签：Hash Table、Math、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-balls-in-a-box/)

---

## 题目（英文原版）

**Description**

You are working in a ball factory where you have n balls numbered from lowLimit up to highLimit inclusive (i.e., n == highLimit - lowLimit + 1), and an infinite number of boxes numbered from 1 to infinity.
Your job at this factory is to put each ball in the box with a number equal to the sum of digits of the ball's number. For example, the ball number 321 will be put in the box number 3 + 2 + 1 = 6 and the ball number 10 will be put in the box number 1 + 0 = 1.
Given two integers lowLimit and highLimit, return the number of balls in the box with the most balls.

**Examples**

**Example 1:**

```
Input: lowLimit = 1, highLimit = 10
Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 ...
Ball Count:  2 1 1 1 1 1 1 1 1 0  0  ...
Box 1 has the most number of balls with 2 balls.
```

**Example 2:**

```
Input: lowLimit = 5, highLimit = 15
Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 ...
Ball Count:  1 1 1 1 2 2 1 1 1 0  0  ...
Boxes 5 and 6 have the most number of balls with 2 balls in each.
```

**Example 3:**

```
Input: lowLimit = 19, highLimit = 28
Output: 2
Explanation:
Box Number:  1 2 3 4 5 6 7 8 9 10 11 12 ...
Ball Count:  0 1 1 1 1 1 1 1 1 2  0  0  ...
Box 10 has the most number of balls with 2 balls.
```

**Constraints**

- 1 <= lowLimit <= highLimit <= 105

---

## 题目（中文翻译）

你在一家球厂工作，拥有编号从 `lowLimit` 到 `highLimit`（包含两端）的 `n` 个球（即 `n == highLimit - lowLimit + 1`），以及编号从 `1` 到正无穷的无限多个盒子（boxes）。  
你的任务是把每个球放入编号等于该球编号各位数字之和的盒子中。例如，球编号 `321` 会放入盒子 `3 + 2 + 1 = 6`，球编号 `10` 会放入盒子 `1 + 0 = 1`。  
给定整数 `lowLimit` 和 `highLimit`，返回球数最多的盒子的球的数量。

## 示例

### 示例 1
**输入**: `lowLimit = 1, highLimit = 10`  
**输出**: `2`  
**解释**:  
盒子编号:  1 2 3 4 5 6 7 8 9 10 11 ...  
球的数量:  2 1 1 1 1 1 1 1 1 0  0  ...

盒子 `1` 中的球最多，数量为 `2`。

### 示例 2
**输入**: `lowLimit = 5, highLimit = 15`  
**输出**: `2`  
**解释**:  
盒子编号:  1 2 3 4 5 6 7 8 9 10 11 ...  
球的数量:  1 1 1 1 2 2 1 1 1 0  0  ...

盒子 `5` 和 `6` 中的球数量相同，都是最多的 `2` 个。

### 示例 3
**输入**: `lowLimit = 19, highLimit = 28`  
**输出**: `2`  
**解释**:  
盒子编号:  1 2 3 4 5 6 7 8 9 10 11 12 ...  
球的数量:  0 1 1 1 1 1 1 1 1 2  0  0  ...

盒子 `10` 中的球最多，数量为 `2`。

## 约束条件

- `1 <= lowLimit <= highLimit <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把每个球一个个拿出来，算出它的“盒子编号”，然后把它放进对应的盒子**。  
- **盒子编号** = 球编号各位数字之和。比如球 321 → 3+2+1 = 6，放进第 6 号盒子。  
- 为了统计每个盒子里有多少球，我们可以用 **哈希表**（在 Python 里用 `dict`）来记录：`key` 是盒子编号，`value` 是该盒子里已经放进的球数。哈希表就像一本“查字典”，你给它一个词（这里是盒子编号），它立刻告诉你对应的页码（这里是球的数量），查找、插入的时间都是常数级别的 O(1)。  

**为什么这个方法一定对？**  
因为题目要求的盒子编号就是**唯一确定的**——每个球只能对应唯一的盒子编号。只要我们遍历所有球并把它们对应的盒子计数，最后取计数最大的那个盒子即可。

**时间/空间复杂度**  
- 我们要遍历 `lowLimit … highLimit` 之间的每一个整数，最多 10⁵ 次，每次计算数字之和的时间与数字位数有关（最多 6 位），可以视为常数。因此总体时间是 **O(N)**（N 为球的数量）。  
- 哈希表里最多会出现 `maxDigitSum` 个不同的盒子编号。对 `10⁵` 以内的数字，最大位和是 `9+9+9+9+9 = 45`（实际上 100000 的位和是 1），所以空间最多是 **O(45) ≈ O(1)**，在大多数分析里写作 **O(N)** 更保守，但实际常数很小。

#### 代码（Python）

```python
def digit_sum(x: int) -> int:
    """返回整数 x 各位数字之和，例如 321 -> 6"""
    s = 0
    while x:
        s += x % 10      # 取最低位
        x //= 10         # 去掉最低位
    return s

def countBalls(lowLimit: int, highLimit: int) -> int:
    box_cnt = {}                     # 哈希表：盒子编号 -> 球的数量
    for num in range(lowLimit, highLimit + 1):
        b = digit_sum(num)           # 计算该球放进哪只盒子
        box_cnt[b] = box_cnt.get(b, 0) + 1   # 计数 +1
    # 取所有盒子里最大的球数
    return max(box_cnt.values())
```

#### 复杂度

- **时间复杂度**：`O(N)`，其中 `N = highLimit - lowLimit + 1`，因为我们对每个球只做一次常数时间的操作（计算位和 + 哈希表更新）。  
- **空间复杂度**：`O(M)`，`M` 为不同盒子编号的个数。对本题 `M ≤ 45`，可以视作 `O(1)`（常数级别）。

---

### 2. 最优解

#### 思路  

从暴力解来看，**瓶颈**并不在时间上——遍历 10⁵ 次已经足够快。  
真正可以再“优化”的地方是**空间和常数因子**：

1. **使用数组代替哈希表**  
   盒子编号的取值范围是 **1 … 45**（因为 `highLimit ≤ 10⁵`，最大位和为 45），我们完全可以用一个长度为 46（下标 0 不用）的列表 `cnt` 来直接存放每个盒子的球数。列表的随机访问同样是 O(1)，而且比字典的哈希计算更省时。

2. **增量计算位和**（可选）  
   如果想进一步减少每次求位和的循环次数，可以利用“进位”特性：`digit_sum(i+1) = digit_sum(i) - 9*k + 1`（其中 `k` 为末尾连续的 9 的个数）。但实现相对繁琐，且在本题数据规模下收益不明显，这里就不展开。

综合以上两点，最优解的核心是 **用固定大小的数组统计**，时间仍是 O(N)，空间降到真正的常数 O(1)。

#### 代码（Python）

```python
def digit_sum(x: int) -> int:
    """计算整数 x 的位和，使用简单的循环实现"""
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s

def countBalls(lowLimit: int, highLimit: int) -> int:
    # 位和最大不超过 45（5 位数全为 9），准备 46 长度的数组
    cnt = [0] * 46                 # cnt[i] 表示第 i 号盒子的球数
    for num in range(lowLimit, highLimit + 1):
        b = digit_sum(num)         # 计算盒子编号
        cnt[b] += 1                # 直接在数组里计数
    return max(cnt)                # 数组中最大的即为答案
```

#### 复杂度

- **时间复杂度**：`O(N)`，遍历每个球一次，计算位和仍是常数时间。相比暴力解，只是把字典操作换成了数组下标，实际运行更快。  
- **空间复杂度**：`O(1)`，因为数组大小固定为 46，与输入规模无关。

---

## 心得

- **核心技巧**：利用**位和的取值上界**，用**固定大小的计数数组**代替哈希表，实现 O(1) 空间。  
- **适用的题型**  
  1. “统计出现次数”且**取值范围已知且小**的题目（如 “字母出现次数”、 “统计数组中出现的每个数字”）。  
  2. “把数值映射到另一集合”且映射结果范围受限的题目（如 “把整数映射到它的位和”）。  
- **解题钥匙**：**先估算结果的取值范围**，如果范围很小，就可以用**数组直接计数**，避免额外的哈希开销。

---

## 反思

- **第一反应**：看到“把每个球放进位和对应的盒子”，立刻想到遍历所有球并用哈希表计数。  
- **最容易踩的坑**  
  - 忘记 **位和的上界**，误以为盒子编号可能很大，从而使用不必要的哈希结构。  
  - 处理 **lowLimit = highLimit** 的单个球情况，或者 **highLimit = 10⁵** 时位和为 1，需要确保数组长度足够（这里用了 46）。  
- **下次类似题的第一步**：**先算出映射结果的最大可能值**，判断是否可以用固定大小的数组来计数；如果可以，直接用数组；如果不行，再考虑哈希表或其他数据结构。