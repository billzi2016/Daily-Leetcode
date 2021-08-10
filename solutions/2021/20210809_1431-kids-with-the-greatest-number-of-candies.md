# #1431. 拥有最多糖果的孩子 / Kids With the Greatest Number of Candies

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/)

---

## 题目（英文原版）

**Description**

There are n kids with candies. You are given an integer array candies, where each candies[i] represents the number of candies the ith kid has, and an integer extraCandies, denoting the number of extra candies that you have.
Return a boolean array result of length n, where result[i] is true if, after giving the ith kid all the extraCandies, they will have the greatest number of candies among all the kids, or false otherwise.
Note that multiple kids can have the greatest number of candies.

**Examples**

**Example 1:**

```
Input: candies = [2,3,5,1,3], extraCandies = 3
Output: [true,true,true,false,true] 
Explanation: If you give all extraCandies to:
- Kid 1, they will have 2 + 3 = 5 candies, which is the greatest among the kids.
- Kid 2, they will have 3 + 3 = 6 candies, which is the greatest among the kids.
- Kid 3, they will have 5 + 3 = 8 candies, which is the greatest among the kids.
- Kid 4, they will have 1 + 3 = 4 candies, which is not the greatest among the kids.
- Kid 5, they will have 3 + 3 = 6 candies, which is the greatest among the kids.
```

**Example 2:**

```
Input: candies = [4,2,1,1,2], extraCandies = 1
Output: [true,false,false,false,false] 
Explanation: There is only 1 extra candy.
Kid 1 will always have the greatest number of candies, even if a different kid is given the extra candy.
```

**Example 3:**

```
Input: candies = [12,1,12], extraCandies = 10
Output: [true,false,true]
```

**Constraints**

- n == candies.length
- 2 <= n <= 100
- 1 <= candies[i] <= 100
- 1 <= extraCandies <= 50

---

## 题目（中文翻译）

有 `n` 个孩子，每个孩子手中都有一定数量的糖果。给定一个整数数组 `candies`，其中 `candies[i]` 表示第 `i` 个孩子拥有的糖果数，以及一个整数 `extraCandies`，表示你手中拥有的额外糖果数量。

返回一个布尔数组 `result`，长度为 `n`。若在将所有 `extraCandies` 都赠予第 `i` 个孩子后，该孩子的糖果数成为所有孩子中 **最大的**（greatest），则 `result[i]` 为 `true`；否则为 `false`。  
注意，可能会有多个孩子同时拥有 **最大的** 糖果数。

## 示例

### 示例 1
```
Input: candies = [2,3,5,1,3], extraCandies = 3
Output: [true,true,true,false,true]
Explanation:
如果把所有额外糖果都给：
- 第 1 个孩子，他们将拥有 2 + 3 = 5 颗糖果，是所有孩子中最多的。
- 第 2 个孩子，他们将拥有 3 + 3 = 6 颗糖果，是所有孩子中最多的。
- 第 3 个孩子，他们将拥有 5 + 3 = 8 颗糖果，是所有孩子中最多的。
- 第 4 个孩子，他们将拥有 1 + 3 = 4 颗糖果，**不是**最多的。
- 第 5 个孩子，他们将拥有 3 + 3 = 6 颗糖果，是所有孩子中最多的。
```

### 示例 2
```
Input: candies = [4,2,1,1,2], extraCandies = 1
Output: [true,false,false,false,false]
Explanation:
只有 1 颗额外糖果。即使把这颗糖果给其他孩子，孩子 1（原本拥有 4 颗）仍然是糖果最多的。
```

### 示例 3
```
Input: candies = [12,1,12], extraCandies = 10
Output: [true,false,true]
Explanation:
- 给第 1 个孩子后，他们拥有 12 + 10 = 22 颗糖果，仍是最多的。
- 给第 2 个孩子后，他们拥有 1 + 10 = 11 颗糖果，不是最多的。
- 给第 3 个孩子后，他们拥有 12 + 10 = 22 颗糖果，和第 1 个孩子并列最多。
```

## 约束条件
- `n == candies.length`
- `2 <= n <= 100`
- `1 <= candies[i] <= 100`
- `1 <= extraCandies <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个小朋友都分别尝试一次**，把 `extraCandies` 全部给他，然后把所有小朋友的糖果数重新算一遍，看看他是不是最多的。  

- **用到的数据结构**：  
  - `list`（数组）保存原始的糖果数。  
  - 再建一个同样长度的 `list` 保存每次“加完糖果”后的最大值。  
  - 类比：把 `list` 想成一排排小朋友的糖果盒子，遍历盒子时像是逐个检查每个人的糖果是否够多。

- **为什么正确**：  
  对每个孩子 `i`，我们都把 `extraCandies` 加到 `candies[i]` 上，得到 `candies[i] + extraCandies`。随后再遍历一次所有孩子，求出这一次的最大糖果数 `max_now`。如果 `candies[i] + extraCandies` 正好等于 `max_now`，说明在把全部额外糖果给他后，他可以成为（或并列成为）糖果最多的孩子。因为我们对每个孩子都做了完整的“加完‑比较‑求最大”流程，所以一定不会漏掉任何可能。

- **复杂度分析（大白话）**：  
  - 外层循环要遍历 `n` 次（`n` 是小朋友的数量），每一次内部又要再遍历一次全部 `n` 个孩子去找最大值。于是总共要做 `n × n` 次比较，记作 **O(n²)**，这就像是把一张 `n×n` 的方格纸全部涂满一样。  
  - 额外使用的空间只有几个临时变量和结果数组，大小和 `n` 成正比，记作 **O(n)**（结果数组本身必须返回）。

#### 代码（Python）

```python
from typing import List

def kidsWithCandies_bruteforce(candies: List[int], extraCandies: int) -> List[bool]:
    n = len(candies)                     # 小朋友的数量
    result = [False] * n                 # 先全装 False，后面再改成 True

    # 对每个孩子 i，尝试把所有 extraCandies 给他
    for i in range(n):
        # 计算 i 加完糖果后的数量
        cur = candies[i] + extraCandies

        # 在这一次“加完”后，遍历所有孩子找出最大值
        max_now = cur                     # 先假设 i 自己是最大
        for j in range(n):
            # 其他孩子保持原来的糖果数
            if j != i:
                max_now = max(max_now, candies[j])

        # 如果 i 的数量等于这次的最大值，就说明 i 可以成为（并列）最多的孩子
        result[i] = (cur == max_now)

    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - `n` 次外层循环 × `n` 次内部遍历 = `n²` 次比较。  
  - 当 `n=100`（题目上限）时，最多需要 10,000 次比较，仍然能跑完，但不是最优的。

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的布尔结果数组和若干常数级变量。  
  - 这部分空间是必须的，因为最终要把每个孩子的判断结果返回给调用者。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要遍历全部孩子去求最大值。实际上，这个最大值 **不依赖于** 哪个孩子得到额外糖果——它只和原始数组 `candies` 本身有关。  

**优化的关键**：

1. **先算出原数组的最大值** `max_candy`（只遍历一次）。  
2. 对每个孩子 `i`，只需要判断 `candies[i] + extraCandies >= max_candy`。  
   - 如果成立，即使把所有额外糖果给 `i`，他的糖果数也不会低于原来的最大值，所以 `i` 能成为（并列）最多的孩子。  
   - 这一步只需要 **O(1)** 的比较。

这样我们把 **两层遍历** 合并成 **两次单层遍历**：一次求最大值，第二次逐个判断，时间复杂度降为 **O(n)**。

**核心概念**：**前缀最大**（prefix max）——在遍历数组的过程中，随时维护已经看到的最大值。这里我们只需要一次完整遍历就能得到全局最大值。

**类比**：想象你在操场上排队，老师先让所有小朋友报数，记下最高的数（最大糖果）。随后老师只需要看每个人加上额外糖果后是否 ≥ 最高数，就能快速判断谁可能是“糖果之王”。不需要每次都重新数一遍全体。

#### 代码（Python）

```python
from typing import List

def kidsWithCandies_optimal(candies: List[int], extraCandies: int) -> List[bool]:
    # 1️⃣ 先找出原始糖果数的最大值
    max_candy = max(candies)                 # O(n) 一遍遍历

    # 2️⃣ 再遍历一次，逐个判断是否可以达到或超过最大值
    result = []
    for c in candies:                        # O(n) 再遍历一次
        # 加上 extraCandies 后是否 >= 原来的最大值
        result.append(c + extraCandies >= max_candy)   # 布尔值直接加入列表
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次遍历求最大值 + 第二次遍历做比较 = `2n` 次操作，数量级仍是 `n`。  
  - 与暴力解的 `n²` 相比，**快了整整 `n` 倍**，当 `n` 很大时优势非常明显。

- **空间复杂度**：`O(n)`  
  - 仍然需要返回一个长度为 `n` 的布尔数组。  
  - 额外的临时变量只有 `max_candy` 和循环计数器，属于常数级空间。

---

## 心得

- **核心技巧**：先求全局最大（或最小），再用一次遍历完成判定。  
- **适用的题型**  
  1. “判断每个元素加上某个值后是否成为最大”——如 **“Maximum Difference After Adding to Elements”**。  
  2. “找出所有满足 >= 某阈值的元素”——如 **“Elements Greater Than a Threshold”**。  
  3. “是否可以在一次操作后使数组单调递增/递减”——常用先算极值再比较的思路。  

- **一句话总结**：**先把“全局信息”准备好，再用“局部检查”快速得出答案**。

---

## 反思

- **第一反应**：把每个孩子都单独“模拟”一次，加完糖果后重新找最大——这就是暴力解。  
- **最容易踩的坑**  
  - **忘记包括自己**：判断时要把 `extraCandies` 加到当前孩子的糖果数上，而不是只比较原始值。  
  - **多余的比较**：如果直接在遍历时每次都 `max(candies[i] + extraCandies, ...)`，会不必要地重复求最大。  
  - **返回类型**：题目要求返回布尔列表，别写成整数 `0/1` 或者直接打印。  

- **下次类似题**：第一步先 **“提取全局特征（最大/最小/总和）”**，再 **“用 O(1) 的局部判断”** 完成整个数组的遍历。这样既简洁又高效。