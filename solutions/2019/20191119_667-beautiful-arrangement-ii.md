# #667. 漂亮排列 II / Beautiful Arrangement II

> 难度：中等 · 标签：Array、Math · [LeetCode 链接](https://leetcode.com/problems/beautiful-arrangement-ii/)

---

## 题目（英文原版）

**Description**

Given two integers n and k, construct a list answer that contains n different positive integers ranging from 1 to n and obeys the following requirement:
Return the list answer. If there multiple valid answers, return any of them.

**Examples**

**Example 1:**

```
Input: n = 3, k = 1
Output: [1,2,3]
Explanation: The [1,2,3] has three different positive integers ranging from 1 to 3, and the [1,1] has exactly 1 distinct integer: 1
```

**Example 2:**

```
Input: n = 3, k = 2
Output: [1,3,2]
Explanation: The [1,3,2] has three different positive integers ranging from 1 to 3, and the [2,1] has exactly 2 distinct integers: 1 and 2.
```

**Constraints**

- 1 <= k < n <= 104

---

## 题目（中文翻译）

给定两个整数 `n` 和 `k`，构造一个列表 `answer`，该列表包含从 `1` 到 `n` 的 `n` 个不同的正整数，并满足以下要求：

返回列表 `answer`。如果存在多个满足条件的答案，返回任意一个。

## 示例

### 示例 1
**输入:** `n = 3, k = 1`  
**输出:** `[1,2,3]`  
**解释:** `[1,2,3]` 包含三个不同的正整数，范围在 `1` 到 `3` 之间，且 `[1,1]` 恰好有 `1` 个不同的整数：`1`

### 示例 2
**输入:** `n = 3, k = 2`  
**输出:** `[1,3,2]`  
**解释:** `[1,3,2]` 包含三个不同的正整数，范围在 `1` 到 `3` 之间，且 `[2,1]` 恰好有 `2` 个不同的整数：`1` 和 `2`

## 约束条件
- `1 <= k < n <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的排列**（1 ~ n 的全排列）都列举出来，逐个检查它们相邻元素的绝对差值集合是否恰好有 `k` 种不同的数。如果满足，就把这条排列返回。  

- **用到的数据结构**  
  - **数组/列表**：用来存放当前的排列。  
  - **集合（Set）**：在检查时把相邻差值放进去，集合天然去重，最后看它的大小是否等于 `k`。  
  - **全排列生成器**（在 Python 中可以用 `itertools.permutations`），它就像一本“所有可能的字典”，每一次调用都给你下一个完整的排列。  

- **为什么正确**  
  因为我们遍历了**所有**合法的排列，只要有满足条件的答案，就一定会被找出来。  

- **时间/空间复杂度**  
  - **时间**：全排列的数量是 `n!`（n 的阶乘），每条排列我们还要遍历一次长度为 `n` 的数组来算差值，所以时间复杂度是 `O(n!·n)`。  
    - 大白话：`n!` 甚至比“每天刷 10 次抖音”快几千倍，`n=10` 时已经是 3 628 800 条，`n=12` 就是 479 001 600 条，根本跑不完。  
  - **空间**：保存一条排列需要 `O(n)`，另外递归/迭代产生全排列时会使用 `O(n)` 的栈空间（或迭代器内部的缓冲），所以整体是 `O(n)`。  

#### 代码（Python）

```python
import itertools

def beautifulArrangement_bruteforce(n: int, k: int):
    """
    暴力解：枚举所有排列，找到第一个满足条件的返回。
    仅适用于 n 很小的情况（如 n <= 8），用于理解思路。
    """
    for perm in itertools.permutations(range(1, n + 1)):
        # 计算相邻差值的集合
        diff_set = {abs(perm[i] - perm[i + 1]) for i in range(n - 1)}
        if len(diff_set) == k:          # 正好有 k 种不同的差值
            return list(perm)           # 转成列表返回
    return []                           # 理论上不会到这里
```

> **提示**：在 LeetCode 上直接提交这段代码会因为超时而被判 `Time Limit Exceeded`，它只用来帮助大家“先想出最直观的办法”。

#### 复杂度

- 时间复杂度：`O(n!·n)` — 先生成 `n!` 条排列，每条再扫一遍 `n` 长度的数组。
- 空间复杂度：`O(n)` — 只保存当前的排列和差值集合。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**遍历全部排列是最大的瓶颈**。我们需要 **直接构造** 出一种满足条件的排列，而不是去找。

**关键观察**  

1. 我们只关心**相邻差值的种类数**，而不在乎它们出现的顺序。  
2. 若我们能够让前 `k+1` 个位置产生 `k, k-1, …, 1` 这 `k` 个不同的差值，后面的差值只要全部是 `1` 就不会再引入新种类。  
3. `k` 最大可以是 `n-1`（因为相邻差值最多只有 `n-1` 种），所以我们只需要在前 `k+1` 位“制造”这些不同的差值，其余位置随意填充即可。

**如何制造 `k, k-1, …, 1`？**  

把数列的两端交替取数：

- 设 `low = 1`（最小未使用的数），`high = n`（最大未使用的数）。  
- 第 `0` 位取 `low`，第 `1` 位取 `high`，第 `2` 位再取 `low+1`，第 `3` 位取 `high-1`，如此交替。  
- 这样得到的前 `k+1` 个数的相邻差值恰好是 `high-low, (high-1)-low, (high-1)-(low+1), …`，其绝对值依次递减，正好形成 `k, k-1, …, 1`（因为每次我们把两端的距离缩小 1）。  

**剩余位置**  

当已经用了 `k+1` 个数后，`low` 与 `high` 之间只剩下连续的一段数（比如 `low … high`）。把它们 **按升序** 直接接在后面即可，此时相邻差值全部是 `1`，不再产生新种类。

**类比**  

想象有一根绳子两头分别挂着编号 `1`（左）和 `n`（右）的球。我们要让球之间的距离每一步都变小 1：先把左边的球放下，再把右边的球放下，左边再往里放，右边再往里放……前 `k+1` 步的距离就会是 `k, k-1, …, 1`。剩下的球都排成一列，距离自然都是 `1`。

**算法步骤**  

1. 初始化 `low = 1, high = n, ans = []`。  
2. 循环 `i` 从 `0` 到 `k`（共 `k+1` 次）  
   - 若 `i` 为偶数，`ans.append(low)`，`low += 1`。  
   - 若 `i` 为奇数，`ans.append(high)`，`high -= 1`。  
3. 循环结束后，`low … high` 之间的数仍未使用。把它们 **顺序加入** `ans`（`for x in range(low, high+1): ans.append(x)`）。  
4. 返回 `ans`。

#### 代码（Python）

```python
def beautifulArrangement(n: int, k: int):
    """
    最优解：构造满足相邻差值恰好有 k 种不同的排列。
    思路：前 k+1 位交替取最小/最大，使差值形成 k, k-1, …, 1；
          剩余位置顺序填充，只产生差值 1。
    时间复杂度 O(n)，空间复杂度 O(1)（不计输出数组）。
    """
    ans = []
    low, high = 1, n

    # 1️⃣ 交替取数，制造 k 种不同的差值
    for i in range(k + 1):
        if i % 2 == 0:          # 偶数位取左边的最小数
            ans.append(low)
            low += 1
        else:                   # 奇数位取右边的最大数
            ans.append(high)
            high -= 1

    # 2️⃣ 把剩下的数按升序填充，差值全部是 1
    for x in range(low, high + 1):
        ans.append(x)

    return ans
```

> **运行示例**  
> ```python
> print(beautifulArrangement(3, 1))   # [1, 2, 3]
> print(beautifulArrangement(3, 2))   # [1, 3, 2]
> print(beautifulArrangement(7, 3))   # [1, 7, 2, 6, 3, 4, 5]
> ```  

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组（前 `k+1` 次循环 + 余下的线性填充），比暴力的 `n!·n` 快了指数级。  
- **空间复杂度**：`O(1)`（不计返回的答案列表）——只用到常数个额外变量 `low、high、i`，没有额外的数组或哈希表。

---

## 心得

- **核心技巧**：**交替取两端** 让差值逐步递减，随后**顺序填充** 只产生已有的差值。  
- **适用的题型**  
  1. **构造满足差值集合大小的排列**（如本题）。  
  2. **要求相邻元素差值的范围或数量**（如 “Maximum Alternating Subarray Sum” 的构造思路）。  
  3. **需要在数组两端交替取数的贪心题**（如 “Beautiful Arrangement I” 中的相邻差值最大化）。  
- **一句话总结**：把最小和最大交错放 `k+1` 次，后面顺序填，差值自然恰好有 `k` 种。

---

## 反思

- **第一反应**：把所有排列枚举完再挑，忽视了“构造”这条捷径。  
- **最容易踩的坑**  
  - 忘记 `k` 的取值范围是 `< n`，所以一定有 **剩余位置**（`n - (k+1) ≥ 0`），不必担心越界。  
  - 交替取数时要先判断 **偶数位** 取左边，**奇数位** 取右边，顺序颠倒会导致差值集合不完整（比如出现重复差值）。  
  - 当 `k = 0`（题目保证 `k ≥ 1`，但如果放宽）时，只需要顺序 `1..n`，代码仍然适用，因为循环 `k+1 = 1` 只取一次 `low`。  
- **下次遇到同类题**：第一步先思考 **“怎样用最少的操作产生所需的不同差值？”**，往往可以通过 **两端交替** 或 **前缀/后缀递增递减** 的方式直接构造。