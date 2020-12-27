# #1128. 等价多米诺对的数量 / Number of Equivalent Domino Pairs

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/number-of-equivalent-domino-pairs/)

---

## 题目（英文原版）

**Description**

Given a list of dominoes, dominoes[i] = [a, b] is equivalent to dominoes[j] = [c, d] if and only if either (a == c and b == d), or (a == d and b == c) - that is, one domino can be rotated to be equal to another domino.
Return the number of pairs (i, j) for which 0 <= i < j < dominoes.length, and dominoes[i] is equivalent to dominoes[j].

**Examples**

**Example 1:**

```
Input: dominoes = [[1,2],[2,1],[3,4],[5,6]]
Output: 1
```

**Example 2:**

```
Input: dominoes = [[1,2],[1,2],[1,1],[1,2],[2,2]]
Output: 3
```

**Constraints**

- 1 <= dominoes.length <= 4 * 104
- dominoes[i].length == 2
- 1 <= dominoes[i][j] <= 9

---

## 题目（中文翻译）

给定一个多米诺骨牌列表 `dominoes`，其中 `dominoes[i] = [a, b]` 当且仅当满足以下任意一种情况时，等价于 `dominoes[j] = [c, d]`：  

- `a == c` 且 `b == d`  
- `a == d` 且 `b == c`  

即可以将一块多米诺旋转后与另一块完全相同。  

返回满足 `0 <= i < j < dominoes.length` 且 `dominoes[i]` 与 `dominoes[j]` 等价的索引对 `(i, j)` 的数量。

**示例 1**  
**输入**: `dominoes = [[1,2],[2,1],[3,4],[5,6]]`  
**输出**: `1`

**示例 2**  
**输入**: `dominoes = [[1,2],[1,2],[1,1],[1,2],[2,2]]`  
**输出**: `3`

**约束条件**  
- `1 <= dominoes.length <= 4 * 10^4`  
- `dominoes[i].length == 2`  
- `1 <= dominoes[i][j] <= 9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有的多米诺骨牌两两比较，看看它们是否等价。  
等价的定义是两块骨牌要么正好相同，要么把其中一块翻转（把左边的数和右边的数交换）后相同。  

- **使用的数据结构**：只需要一个普通的二维列表 `dominoes`，因为我们直接在列表里遍历元素。  
- **生活化类比**：把每块骨牌想象成一张双面卡片，正面写 `[a,b]`，背面写 `[b,a]`。要判断两张卡片是否相同，只要看正面是否相同，或者正面和另一张卡片的背面相同即可。  

**为什么正确**：我们枚举了所有可能的 `(i, j)`（`i < j`），只要找到符合等价条件的就计数，遍历完所有组合后得到的计数必然是答案。

#### 代码（Python）

```python
from typing import List

def numEquivDominoPairs_bruteforce(dominoes: List[List[int]]) -> int:
    n = len(dominoes)
    ans = 0
    # 两层循环，枚举所有 i < j 的组合
    for i in range(n):
        a, b = dominoes[i]
        for j in range(i + 1, n):
            c, d = dominoes[j]
            # 判断是否等价：正向相同或翻转后相同
            if (a == c and b == d) or (a == d and b == c):
                ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们用了两层循环，外层 `n` 次，内层最多 `n-1` 次，整体大概是 `n × n`，也就是 **平方级别**。如果 `n = 10⁴`，则需要约 `10⁸` 次比较，实际运行会很慢。

- **空间复杂度**：`O(1)`  
  解释：只用了几个临时变量，和输入规模无关，常数级别的额外空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于大量重复比较**。  
实际上，只要我们能快速判断“已经出现过多少块等价的骨牌”，就不必再两两比较了。  

**关键点**：  
1. 对于每块骨牌 `[a, b]`，把它 **规范化** 成唯一的表示形式。因为 `[a,b]` 与 `[b,a]` 等价，我们可以把较小的数放在前面，较大的放在后面。即 `key = (min(a,b), max(a,b))`。  
2. 用 **哈希表**（在 Python 中是 `dict`）记录每种规范化骨牌出现的次数。  
3. 当遍历到第 `j` 块骨牌时，查询哈希表里已经出现的相同 `key` 的数量，这个数量就是以当前骨牌为结尾的等价对数。随后把当前 `key` 的计数加一，继续遍历。  

- **哈希表类比**：就像一本“字典”，单词是 `key`，出现次数是 `value`。查找某个单词的出现次数是 **O(1)** 的操作，速度非常快。  

**为什么正确**：  
- 规范化保证了所有等价的骨牌映射到同一个 `key`。  
- 哈希表在遍历过程中实时统计出现次数，当前骨牌能配对的数量正好是之前出现的相同 `key` 的次数。累计这些配对数即为答案。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def numEquivDominoPairs(dominoes: List[List[int]]) -> int:
    """
    统计等价多米诺骨牌对数，时间 O(n)，空间 O(m)（m 为不同骨牌种类数，最多 45 种）
    """
    cnt = defaultdict(int)   # key -> 已出现次数
    ans = 0

    for a, b in dominoes:
        # 规范化：把较小的放前面，较大的放后面，得到唯一的 key
        key = (min(a, b), max(a, b))

        # 之前已经出现了 cnt[key] 块相同的骨牌，
        # 这些骨牌都可以和当前这块组成等价对
        ans += cnt[key]

        # 把当前骨牌计入哈希表，供后面的骨牌使用
        cnt[key] += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：只遍历了一遍 `dominoes`（`n` 为骨牌数量），每一步的哈希表查询和更新都是 **常数时间**（`O(1)`），所以整体是线性级别。相比暴力的 `O(n²)`，快了很多。

- **空间复杂度**：`O(m)`，其中 `m` 是不同规范化骨牌的种类数。  
  解释：因为每个数字只能是 1~9，两个数字的组合最多是 `9*10/2 = 45` 种（不考虑顺序），所以最坏只会存 45 条记录，空间几乎可以视为常数 `O(1)`。

---

## 心得

- **核心技巧**：利用哈希表统计出现次数 + 规范化（把等价对象映射到唯一键）。  
- **适用的题型**：  
  1. “计数相同/相似元素对数”——例如 **相同字母对数**、**相同子数组和** 等。  
  2. “把对称或可翻转的对象统一表示后计数”——如 **相同的无序对**、**无向图的边计数**。  
- **一句话总结解题钥匙**：**把等价的东西统一成唯一标识，再用哈希表一次遍历累计配对数**。

---

## 反思

- **第一反应**：直接想到两层循环枚举所有组合，觉得实现最直观。  
- **最容易踩的坑**：  
  - 忘记对骨牌进行规范化，导致 `[1,2]` 与 `[2,1]` 被误判为不同。  
  - 统计配对时使用 `i < j` 的顺序错误，可能出现重复计数。  
  - 对哈希表的默认值没有处理好（使用 `defaultdict(int)` 可以避免 `KeyError`）。  
- **下次类似题的第一步**：先思考“是否可以把等价对象映射到唯一键”，如果可以，就立刻考虑使用哈希表“一遍遍历 + 计数” 的方案。