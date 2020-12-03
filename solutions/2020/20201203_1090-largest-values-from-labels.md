# #1090. 标签限制下的最大价值 / Largest Values From Labels

> 难度：中等 · 标签：Array、Hash Table、Greedy、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/largest-values-from-labels/)

---

## 题目（英文原版）

**Description**

You are given n item's value and label as two integer arrays values and labels. You are also given two integers numWanted and useLimit.
Your task is to find a subset of items with the maximum sum of their values such that:
Return the maximum sum.

**Examples**

**Example 1:**

```
Input: values = [5,4,3,2,1], labels = [1,1,2,2,3], numWanted = 3, useLimit = 1
Output: 9
Explanation:
The subset chosen is the first, third, and fifth items with the sum of values 5 + 3 + 1.
```

**Example 2:**

```
Input: values = [5,4,3,2,1], labels = [1,3,3,3,2], numWanted = 3, useLimit = 2
Output: 12
Explanation:
The subset chosen is the first, second, and third items with the sum of values 5 + 4 + 3.
```

**Example 3:**

```
Input: values = [9,8,8,7,6], labels = [0,0,0,1,1], numWanted = 3, useLimit = 1
Output: 16
Explanation:
The subset chosen is the first and fourth items with the sum of values 9 + 7.
```

**Constraints**

- n == values.length == labels.length
- 1 <= n <= 2 * 104
- 0 <= values[i], labels[i] <= 2 * 104
- 1 <= numWanted, useLimit <= n

---

## 题目（中文翻译）

给定两个整数数组 `values` 和 `labels`，分别表示 `n` 个项目的价值和标签。还给定两个整数 `numWanted` 和 `useLimit`。  
你的任务是选择若干项目构成一个子集（subset），使得该子集的价值总和最大，并且满足以下条件：

- 子集中最多只能包含 `numWanted` 个项目；
- 任意同一标签的项目在子集中的出现次数不能超过 `useLimit`。

返回可以获得的最大价值总和。

## 示例

### 示例 1
**输入**  
`values = [5,4,3,2,1]`, `labels = [1,1,2,2,3]`, `numWanted = 3`, `useLimit = 1`

**输出**  
`9`

**解释**  
选择第 1、3、5 项，价值和为 `5 + 3 + 1 = 9`。

### 示例 2
**输入**  
`values = [5,4,3,2,1]`, `labels = [1,3,3,3,2]`, `numWanted = 3`, `useLimit = 2`

**输出**  
`12`

**解释**  
选择第 1、2、3 项，价值和为 `5 + 4 + 3 = 12`。

### 示例 3
**输入**  
`values = [9,8,8,7,6]`, `labels = [0,0,0,1,1]`, `numWanted = 3`, `useLimit = 1`

**输出**  
`16`

**解释**  
选择第 1、4 项，价值和为 `9 + 7 = 16`。

## 约束条件

- `n == values.length == labels.length`
- `1 <= n <= 2 * 10^4`
- `0 <= values[i], labels[i] <= 2 * 10^4`
- `1 <= numWanted, useLimit <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的子集枚举出来**，算出每个子集的价值总和，挑选满足条件且价值最大的那个。  

- **子集**可以类比为“挑选哪些商品进购物车”。  
- 为了判断一个子集是否合法，需要检查两件事：  
  1. 选中的商品数不能超过 `numWanted`（购物车里最多放这么多件）。  
  2. 同一种标签（`label`）的商品不能超过 `useLimit`（比如每种颜色的衣服只能买这么多件）。  
- 我们可以用 **哈希表**（想象成一本字典，`key` 是标签，`value` 是已经挑选的该标签商品数量）来统计每个标签已使用的次数。  

这种做法一定能得到正确答案，因为我们穷举了所有可能的选择，必然包含最优解。只不过 **“穷举”** 的代价非常高。

#### 代码（Python）

```python
from itertools import combinations
from collections import defaultdict
from typing import List

def largestValsFromLabels_bruteforce(values: List[int],
                                    labels: List[int],
                                    numWanted: int,
                                    useLimit: int) -> int:
    n = len(values)
    best = 0                     # 当前找到的最大价值和
    # 枚举子集大小从 1 到 numWanted（0 可以直接返回 0）
    for k in range(1, numWanted + 1):
        # combinations 会返回所有长度为 k 的下标组合
        for idx_tuple in combinations(range(n), k):
            label_cnt = defaultdict(int)   # 统计每个标签出现的次数
            cur_sum = 0
            valid = True
            for i in idx_tuple:
                lbl = labels[i]
                # 如果已经达到该标签的上限，就直接把这个子集标记为非法
                if label_cnt[lbl] >= useLimit:
                    valid = False
                    break
                label_cnt[lbl] += 1
                cur_sum += values[i]
            if valid:
                best = max(best, cur_sum)
    return best
```

> **关键行解释**  
> - `combinations(range(n), k)`: 把 `0 … n-1` 这些下标全排列组合，类似“把所有商品挑 k 件”。  
> - `defaultdict(int)`: 像一本空字典，查询不存在的标签会返回 `0`，方便计数。  
> - `if label_cnt[lbl] >= useLimit`: 判断该标签是否已经用到上限。

#### 复杂度  

- **时间复杂度**：  
  - 对每个 `k (1 … numWanted)`，我们都要遍历 `C(n, k)`（组合数）个子集。  
  - 最坏情况下 `numWanted = n`，总的组合数是 `2^n - 1`（所有非空子集），所以时间复杂度是 **O(2ⁿ)**。  
  - 用大白话说，就是“指数级”，即使 `n = 20` 都会非常慢，`n = 10⁴` 完全不可行。  
- **空间复杂度**：  
  - 只用了常数级的额外空间（`defaultdict`、若干局部变量），所以是 **O(1)**（不计输入数组本身）。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于 **枚举所有子集**。实际上，这道题只需要 **挑选价值最大的若干个商品**，并且要满足每个标签的使用上限。  
这正好符合 **贪心**（greedy）思路：**把价值大的商品先考虑**，只要它不违反约束，就把它放进结果集合。

**具体步骤**：

1. **把所有商品按照价值从大到小排序**。  
   - 类比：在超市挑商品时，先把最贵的（或最值钱的）放在手里，决定是否买。  
2. **遍历排好序的商品**，用哈希表记录每个标签已经选了多少件。  
   - 若当前商品的标签已经用了 `useLimit` 件，就**跳过**（相当于“这件已经买够了，不能再买”。）  
   - 否则，把它加入答案，累计价值，并把该标签的计数加一。  
3. **当已经选的商品数达到 `numWanted` 时停止**，因为再选也不会增加价值（已经选够了）。  

这一步骤只遍历一次排好序的列表，时间主要花在排序上。排序的时间复杂度是 **O(n log n)**，遍历是 **O(n)**，整体是 **O(n log n)**，足以处理 `n ≤ 2·10⁴` 的规模。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def largestValsFromLabels(values: List[int],
                         labels: List[int],
                         numWanted: int,
                         useLimit: int) -> int:
    # 1. 把价值和标签打包成 (value, label) 元组，方便一起排序
    items = list(zip(values, labels))
    # 2. 按价值降序排列，value 大的排在前面
    items.sort(key=lambda x: x[0], reverse=True)

    label_used = defaultdict(int)   # 记录每个标签已经用了多少件
    total = 0                        # 累计选中的价值和
    taken = 0                        # 已经选了多少件商品

    for value, label in items:
        # 如果已经选够了 numWanted 件，直接结束循环
        if taken == numWanted:
            break
        # 检查当前标签是否已经达到上限
        if label_used[label] >= useLimit:
            continue          # 该标签已满，跳过这件商品
        # 选中这件商品
        total += value
        taken += 1
        label_used[label] += 1

    return total
```

> **关键行解释**  
> - `items = list(zip(values, labels))`：把价值和标签配对，好比“把每件商品的价格和颜色绑在一起”。  
> - `items.sort(key=lambda x: x[0], reverse=True)`：按照价值从大到小排序，`reverse=True` 就是“倒序”。  
> - `if label_used[label] >= useLimit: continue`：如果该标签已经买够，就直接不买（跳过）。  
> - `if taken == numWanted: break`：已经买够想要的件数，后面的商品即使再好也不需要考虑了。

#### 复杂度  

- **时间复杂度**：  
  - 排序需要 **O(n log n)**。  
  - 之后的遍历是 **O(n)**（每件商品最多检查一次）。  
  - 综合起来是 **O(n log n)**，对 `n = 2·10⁴` 完全够快。  
- **空间复杂度**：  
  - 需要存放排序后的列表，大小为 `n`，以及哈希表最多存放不超过 `n` 个不同标签。  
  - 因此是 **O(n)** 的额外空间（实际常数很小），相当于线性空间。

---

## 心得

- **核心技巧**：**贪心 + 哈希表**。先把价值最大的商品挑出来，再用哈希表实时检查每个标签的使用次数是否超限。  
- **适用的题型**  
  1. “挑选 k 项，使总价值最大且满足某种计数限制”——如 **"Maximum Subsequence Score"**。  
  2. “在满足频率上限的前提下，选取最多/最少的元素”——如 **"Maximum Number of Darts Inside a Circle"**（利用计数限制）。  
  3. “按某种属性排序后，逐个检查约束”——如 **"Find the Kth Largest Sum of a Subarray"**。  
- **一句话总结解题钥匙**：**把价值最高的先拿出来，用哈希表把每个标签的配额记住，超额就跳过，够了就停**。

---

## 反思

- **第一反应**：看到“最大和”“标签上限”，第一时间想到 **枚举**，因为不确定怎么直接构造答案。  
- **最容易踩的坑**  
  1. **忘记 `numWanted` 上限**：只检查标签上限，却可能选的商品数超过 `numWanted`。  
  2. **标签计数忘记初始化**：使用普通字典而不是 `defaultdict`，导致访问不存在的标签时报错。  
  3. **排序顺序写反**：如果升序而不是降序，贪心就会选到价值小的，答案会偏小。  
- **下次遇到同类题**：第一步先 **把所有元素按照价值（或收益）排序**，然后 **用哈希表/计数器实时检查约束**，在满足约束的前提下尽可能多取价值大的元素。