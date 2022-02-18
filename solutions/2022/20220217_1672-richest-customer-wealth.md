# #1672. 最富有的客户财富 / Richest Customer Wealth

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/richest-customer-wealth/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer grid accounts where accounts[i][j] is the amount of money the i​​​​​​​​​​​th​​​​ customer has in the j​​​​​​​​​​​th​​​​ bank. Return the wealth that the richest customer has.
A customer's wealth is the amount of money they have in all their bank accounts. The richest customer is the customer that has the maximum wealth.

**Examples**

**Example 1:**

```
Input: accounts = [[1,2,3],[3,2,1]]
Output: 6
Explanation:
1st customer has wealth = 1 + 2 + 3 = 6
2nd customer has wealth = 3 + 2 + 1 = 6
Both customers are considered the richest with a wealth of 6 each, so return 6.
```

**Example 2:**

```
Input: accounts = [[1,5],[7,3],[3,5]]
Output: 10
Explanation: 
1st customer has wealth = 6
2nd customer has wealth = 10 
3rd customer has wealth = 8
The 2nd customer is the richest with a wealth of 10.
```

**Example 3:**

```
Input: accounts = [[2,8,7],[7,1,3],[1,9,5]]
Output: 17
```

**Constraints**

- m == accounts.length
- n == accounts[i].length
- 1 <= m, n <= 50
- 1 <= accounts[i][j] <= 100

---

## 题目（中文翻译）

给定一个 `m x n` 的整数网格（grid）`accounts`，其中 `accounts[i][j]` 表示第 `i` 位客户在第 `j` 家银行拥有的金额。返回最富有的客户的财富（wealth）。

客户的财富是其在所有银行账户中的金额之和。最富有的客户指拥有最大财富的客户。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- `m == accounts.length`  
- `n == accounts[i].length`  
- `1 <= m, n <= 50`  
- `1 <= accounts[i][j] <= 100`

---

### 示例

**示例 1**  
Input: `accounts = [[1,2,3],[3,2,1]]`  
Output: `6`  
Explanation:  
第 1 位客户的财富 = `1 + 2 + 3 = 6`  
第 2 位客户的财富 = `3 + 2 + 1 = 6`  
两位客户的财富均为 6，视为最富有的客户，返回 `6`。

**示例 2**  
Input: `accounts = [[1,5],[7,3],[3,5]]`  
Output: `10`  
Explanation:  
第 1 位客户的财富 = `6`  
第 2 位客户的财富 = `10`  
第 3 位客户的财富 = `8`  
第 2 位客户拥有最大财富 10，返回 `10`。

**示例 3**  
Input: `accounts = [[2,8,7],[7,1,3],[1,9,5]]`  
Output: `17`  
Explanation:  
第 1 位客户的财富 = `2 + 8 + 7 = 17`  
第 2 位客户的财富 = `7 + 1 + 3 = 11`  
第 3 位客户的财富 = `1 + 9 + 5 = 15`  
第 1 位客户最富有，返回 `17`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一个 **m × n** 的整数矩阵 `accounts`，`accounts[i][j]` 表示第 *i* 位顾客在第 *j* 家银行的存款。  
要得到“最富有的顾客的财富”，我们只需要：

1. 对每一行（即每位顾客）**求和**，得到该顾客的总财富。  
   - 求和可以类比为把顾客所有银行的存折放在一起，数一遍总共有多少钱。  
2. 把所有顾客的财富放进一个列表，**找最大值**。  
   - 最大值就像在一堆成绩单里挑出最高分一样。

为什么这样一定对？因为题目定义的“财富”正是每行的元素之和，求最大即是答案。

时间复杂度上，这种做法会遍历矩阵中的每一个数字一次，也就是 **O(m·n)**。  
空间上，只需要保存一个当前行的临时和以及全局最大值，**O(1)**（常数级）额外空间。

> **大白话解释**  
> - `O(m·n)` 表示如果矩阵有 10 行 10 列，总共要看 100 次数字；如果是 50×50，则要看 2500 次。数字多多少时间就多多少。  
> - `O(1)` 表示不管矩阵多大，我们只用固定的几个变量，内存几乎不变。

#### 代码（Python）

```python
from typing import List

def maximumWealth(accounts: List[List[int]]) -> int:
    """
    计算最富有顾客的财富
    :param accounts: m 行 n 列的整数矩阵
    :return: 最大的行和
    """
    max_wealth = 0                     # 用来记录目前看到的最大财富

    for idx, customer in enumerate(accounts):
        # 把第 idx 位顾客在所有银行的存款加起来
        cur_sum = 0
        for amount in customer:
            cur_sum += amount           # 累加每家银行的金额
        # 更新全局最大值
        if cur_sum > max_wealth:
            max_wealth = cur_sum

    return max_wealth
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 需要遍历矩阵的每一个元素一次。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`max_wealth`、`cur_sum`、循环计数器）。

---

### 2. 最优解

#### 思路  

其实在本题中，上面的“暴力”解已经是最优的了，因为：

- 题目要求**所有**顾客的财富都必须被计算一次，无法跳过任何元素。  
- 矩阵大小上限只有 `50 × 50`，即最多 2500 个数字，遍历一次本身就很快。

我们可以把 **求和 + 同时更新最大值** 合并到一次遍历里，省去把每行的和先存到列表再取最大这一步的额外循环。实现上只需要在遍历每行时直接比较并保存最大值。

核心技巧就是**“一遍遍历，两件事一起做”**，这在很多需要“统计 + 找极值”的题目中都很常用。

> **类比**：想象你在超市结账，边扫商品条码（遍历），边把每件商品的价钱累加（求和），同时把最高的单笔消费记下来（找最大），一次就完成了所有工作。

#### 代码（Python）

```python
from typing import List

def maximumWealth(accounts: List[List[int]]) -> int:
    """
    单次遍历完成求和与最大值更新，时间 O(m·n)，空间 O(1)
    """
    max_wealth = 0
    for customer in accounts:          # 逐行（逐顾客）遍历
        # Python 的 sum() 能一次性把一行加完，内部仍是 O(n) 遍历
        cur_sum = sum(customer)        # 计算当前顾客的总财富
        max_wealth = max(max_wealth, cur_sum)  # 与全局最大比较并更新
    return max_wealth
```

> 这里使用了 Python 内置的 `sum()` 与 `max()`，代码更简洁，但底层仍是线性遍历，复杂度不变。

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 仍然需要看每个数字一次，只是把两步合并在同一个循环里。  
- **空间复杂度**：`O(1)` —— 只用了 `max_wealth`、`cur_sum` 两个变量。

与暴力解相比，**时间上没有实质差距**（因为原本已经是最优），但**代码更简洁、更易读**，而且避免了不必要的临时列表。

---

## 心得

- **核心技巧**：在一次遍历中同步完成“统计”和“比较”两件事。  
- **适用场景**：  
  1. 求数组/矩阵每行（列）和的最大值（如 “Maximum Row Sum”）。  
  2. 同时统计元素出现次数并找出现最多的元素（如 “找出现频率最高的字符”）。  
  3. 在遍历时寻找最小/最大距离、最小/最大差值等（如 “最大子数组和” 的 Kadane 算法）。  
- **一句话总结**：**遍历一次，边累加边比较，省时又省力。**

## 反思

- **第一反应**：看到“每位顾客的财富 = 该行所有数字之和”，立刻想到对每行 `sum`，再取最大。  
- **最容易踩的坑**：  
  - 忘记初始化最大值为 0（若所有财富都是正数，这样安全），或错误地用 `-inf` 导致类型不匹配。  
  - 忽视矩阵可能只有一行或一列的极端情况，导致索引错误。  
- **下次遇到同类题**：第一步先问自己“需要对每个子集合（行/列）做什么统计”，然后思考是否可以在同一次遍历中把 “统计” 与 “极值比较” 合并。这样就能快速写出最简洁的解法。