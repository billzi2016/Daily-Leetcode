# #1534. 计数好三元组 / Count Good Triplets

> 难度：简单 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/count-good-triplets/)

---

## 题目（英文原版）

**Description**

Given an array of integers arr, and three integers a, b and c. You need to find the number of good triplets.
A triplet (arr[i], arr[j], arr[k]) is good if the following conditions are true:
Where |x| denotes the absolute value of x.
Return the number of good triplets.

**Examples**

**Example 1:**

```
Input: arr = [3,0,1,1,9,7], a = 7, b = 2, c = 3
Output: 4
Explanation: There are 4 good triplets: [(3,0,1), (3,0,1), (3,1,1), (0,1,1)].
```

**Example 2:**

```
Input: arr = [1,1,2,2,3], a = 0, b = 0, c = 1
Output: 0
Explanation: No triplet satisfies all conditions.
```

**Constraints**

- 3 <= arr.length <= 100
- 0 <= arr[i] <= 1000
- 0 <= a, b, c <= 1000

---

## 题目（中文翻译）

给定一个整数数组 (array) `arr`，以及三个整数 `a`、`b` 和 `c`。需要找出满足条件的好三元组的数量。

如果三元组 `(arr[i], arr[j], arr[k])` 同时满足以下条件，则称其为好三元组：

- `i < j < k`
- `|arr[i] - arr[j]| <= a`
- `|arr[j] - arr[k]| <= b`
- `|arr[i] - arr[k]| <= c`

其中 `|x|` 表示 `x` 的绝对值。

返回好三元组的数量。

### 示例

**示例 1**  
```text
Input: arr = [3,0,1,1,9,7], a = 7, b = 2, c = 3
Output: 4
Explanation: 有 4 个好三元组：[(3,0,1), (3,0,1), (3,1,1), (0,1,1)]。
```

**示例 2**  
```text
Input: arr = [1,1,2,2,3], a = 0, b = 0, c = 1
Output: 0
Explanation: 没有任何三元组同时满足所有条件。
```

### 约束条件

- `3 <= arr.length <= 100`
- `0 <= arr[i] <= 1000`
- `0 <= a, b, c <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把所有可能的三元组都枚举出来，逐一检查它们是否满足题目给出的三个不等式：  

1. `|arr[i] - arr[j]| ≤ a`  
2. `|arr[j] - arr[k]| ≤ b`  
3. `|arr[i] - arr[k]| ≤ c`  

其中下标必须满足 `i < j < k`（即先后顺序）。  

- **用到的数据结构**：只需要原数组 `arr` 本身。可以把它想象成一本书的章节顺序，`i、j、k` 就是章节的页码，必须按顺序阅读。  
- **为什么正确**：因为我们把所有合法的下标组合都检查了一遍，凡是满足条件的必然被计数，凡是不满足的必然被排除。  
- **复杂度大白话**：我们用了三个嵌套的 `for` 循环，外层循环跑 `n` 次，第二层循环最多跑 `n` 次，最内层同理，整体大概是 `n × n × n = n³` 次操作。这里的 `O(n³)` 可以理解为“随着数组长度每增加一次，运算次数会增长大约 `n²` 倍”。空间上我们只用了几个计数器，和输入规模无关，记作 `O(1)`（常数级）。

#### 代码（Python）

```python
from typing import List

def countGoodTriplets(arr: List[int], a: int, b: int, c: int) -> int:
    n = len(arr)
    ans = 0                     # 用来累计满足条件的三元组个数
    # 第一个下标 i，从左到右依次尝试
    for i in range(n - 2):      # 至少还要留出两个位置给 j、k
        # 第二个下标 j，必须在 i 右侧
        for j in range(i + 1, n - 1):
            # 先判断第一个条件，若不满足直接跳过内部循环
            if abs(arr[i] - arr[j]) > a:
                continue
            # 第三个下标 k，必须在 j 右侧
            for k in range(j + 1, n):
                # 检查剩下的两个条件
                if abs(arr[j] - arr[k]) <= b and abs(arr[i] - arr[k]) <= c:
                    ans += 1   # 找到一个好三元组，计数加一
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 三层循环每层最多遍历 `n` 次，整体是立方级别。对 `n ≤ 100` 的数据来说，最多只有 `1,000,000` 次比较，完全可以在毫秒级完成。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`i, j, k, ans`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

在本题的约束下（`n ≤ 100`），暴力三重循环已经足够快，**不存在明显的更低阶的渐进时间复杂度**（例如 `O(n²)`）的通用算法。  
但我们仍可以在暴力的框架上做一点“小优化”，把不必要的比较提前剔除，从而在平均情况下跑得更快。思路如下：

1. **提前判断第一个条件** `|arr[i] - arr[j]| ≤ a`。如果这一步不满足，就不必再去检查 `j` 之后的 `k`，直接进入下一个 `j`。这相当于在找钥匙时先把不合格的钥匙挑出来，省去后面的检查。  
2. 对于已经满足 `i, j` 条件的情况，再遍历 `k`，只检查剩下的两个不等式。  
3. 由于 `i < j < k` 的顺序已经在循环中保证，不需要额外的数据结构。

这套优化仍然是三层循环，最坏情况下仍是 `O(n³)`，但在很多随机输入里会明显快一些（因为第一条不等式往往能把大量 `(i, j)` 对剔除）。

> **核心概念**：**提前剪枝（pruning）**。在遍历搜索树时，尽早发现“不可能成功”的分支并舍弃，能够显著降低实际运行时间。这里的“搜索树”就是所有可能的 `(i, j, k)` 组合。

#### 代码（Python）

```python
from typing import List

def countGoodTriplets_opt(arr: List[int], a: int, b: int, c: int) -> int:
    n = len(arr)
    ans = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            # 剪枝：如果前两元素差距已经超出 a，后面的 k 再也救不回来
            if abs(arr[i] - arr[j]) > a:
                continue
            # 只剩下两条条件需要检查
            for k in range(j + 1, n):
                if abs(arr[j] - arr[k]) <= b and abs(arr[i] - arr[k]) <= c:
                    ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：**最坏情况**仍是 `O(n³)`，因为如果所有 `(i, j)` 都满足第一条条件，就会遍历完整的三层循环。**平均情况**会因为提前剪枝而更快。  
- **空间复杂度**：`O(1)` —— 与暴力解相同，仅使用常数级额外空间。

---

## 心得  

- **核心技巧**：**枚举 + 剪枝**。先把最容易判定的不等式写在最外层，尽早过滤不合法的组合。  
- **适用的题型**：  
  1. “计数满足多个条件的三元组” 类题目（如 **Count Number of Nice Pairs**）。  
  2. “固定顺序的子序列计数” 需要检查若干不等式的情形（如 **Number of Triplets That Can Form Two Arrays of Equal XOR**）。  
  3. 任何 **枚举 + 条件过滤** 能显著降低常数的组合问题。  
- **一句话总结**：**把最严格、最容易判断的条件放在最外层循环，先把不合格的组合剔除，再继续深入检查**。

---

## 反思  

- **第一反应**：看到 “三个整数 a、b、c”，以及 “i < j < k” 的限制，第一时间想到“三层循环枚举”。  
- **最容易踩的坑**：  
  - 忘记下标的顺序要求（必须是 `i < j < k`），导致重复计数或遗漏。  
  - 绝对值写成 `abs(x-y)` 而不是 `x - y`，容易忘记取正。  
  - 边界条件：数组长度恰好为 3 时，只有一种三元组，需要确保循环的上界写对（`range(n-2)`、`range(i+1, n-1)`、`range(j+1, n)`）。  
- **下次遇到同类题的第一步**：先在纸上写出 “枚举所有下标组合” 的框架，然后思考哪些条件最容易判断、可以提前剪枝，把它们放到最外层循环。这样即使最终仍是 `O(n³)`，也能在实践中跑得更快。