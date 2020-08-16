# #960. 删除列使其有序 III / Delete Columns to Make Sorted III

> 难度：困难 · 标签：Array、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/delete-columns-to-make-sorted-iii/)

---

## 题目（英文原版）

**Description**

You are given an array of n strings strs, all of the same length.
We may choose any deletion indices, and we delete all the characters in those indices for each string.
For example, if we have strs = ["abcdef","uvwxyz"] and deletion indices {0, 2, 3}, then the final array after deletions is ["bef", "vyz"].
Suppose we chose a set of deletion indices answer such that after deletions, the final array has every string (row) in lexicographic order. (i.e., (strs[0][0] <= strs[0][1] <= ... <= strs[0][strs[0].length - 1]), and (strs[1][0] <= strs[1][1] <= ... <= strs[1][strs[1].length - 1]), and so on). Return the minimum possible value of answer.length.

**Examples**

**Example 1:**

```
Input: strs = ["babca","bbazb"]
Output: 3
Explanation: After deleting columns 0, 1, and 4, the final array is strs = ["bc", "az"].
Both these rows are individually in lexicographic order (ie. strs[0][0] <= strs[0][1] and strs[1][0] <= strs[1][1]).
Note that strs[0] > strs[1] - the array strs is not necessarily in lexicographic order.
```

**Example 2:**

```
Input: strs = ["edcba"]
Output: 4
Explanation: If we delete less than 4 columns, the only row will not be lexicographically sorted.
```

**Example 3:**

```
Input: strs = ["ghi","def","abc"]
Output: 0
Explanation: All rows are already lexicographically sorted.
```

**Constraints**

- n == strs.length
- 1 <= n <= 100
- 1 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串数组 `strs`，所有字符串长度相同。  
我们可以选择任意的 **删除索引**（deletion indices），并在每个字符串中删除这些索引对应的字符。

例如，若 `strs = ["abcdef","uvwxyz"]` 且删除索引集合为 `{0, 2, 3}`，则删除后的数组为 `["bef", "vyz"]`。

假设我们选择了一组删除索引 `answer`，使得删除后得到的最终数组中，每一行（即每个字符串）内部都是 **字典序**（lexicographic order）递增的，即  

- `strs[0][0] <= strs[0][1] <= ... <= strs[0][strs[0].length - 1]`  
- `strs[1][0] <= strs[1][1] <= ... <= strs[1][strs[1].length - 1]`  
- …  

返回可能的最小 `answer.length`（即最少需要删除的列数）。

## 示例

### 示例 1
> Input: `strs = ["babca","bbazb"]`  
> Output: `3`  
> **解释**：删除列 `0、1、4` 后，数组变为 `["bc", "az"]`。  
> 这两行各自都已满足字典序（`strs[0][0] <= strs[0][1]` 且 `strs[1][0] <= strs[1][1]`）。  
> 注意，`strs[0] > strs[1]` —— 整个数组不要求整体按字典序排列。

### 示例 2
> Input: `strs = ["edcba"]`  
> Output: `4`  
> **解释**：如果删除的列少于 `4`，唯一的一行仍然不是字典序排序的。

### 示例 3
> Input: `strs = ["ghi","def","abc"]`  
> Output: `0`  
> **解释**：所有行已经满足字典序，无需删除任何列。

## 约束

- `n == strs.length`
- `1 <= n <= 100`
- `1 <= strs[i].length <= 100`
- `strs[i]` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删除方案**，然后检验删除后每一行是否已经是非递减的（即字符从左到右不变小）。  
- **数据结构**：我们可以把每一列看成一个“位置”。把要删除的列下标放进一个集合（类似把字典里不需要的词条全部划掉，剩下的就是我们保留的内容）。  
- **正确性**：只要遍历了**所有**可能的删除集合，就一定会碰到最优的那一个。对每一种集合，检查每行是否满足 `c0 ≤ c1 ≤ …`，若满足则记录删除的列数，最终取最小值。  

> 这就像把一堆钥匙全部尝一遍，哪把能打开门就选哪把——虽然肯定能找到答案，但会花很多时间。

#### 代码（Python）

```python
from itertools import combinations

def minDeletionSize_bruteforce(strs):
    m = len(strs[0])               # 列数
    best = m                       # 最坏情况：全部删掉

    # 枚举要保留的列数 k，从 0 到 m
    for k in range(m + 1):
        # 组合出所有可能的保留列下标集合
        for keep in combinations(range(m), k):
            ok = True
            # 检查每一行是否已经非递减
            for row in strs:
                # 按保留的列顺序取字符形成新串
                new_row = [row[c] for c in keep]
                # 判断是否单调不下降
                if any(new_row[i] > new_row[i + 1] for i in range(len(new_row) - 1)):
                    ok = False
                    break
            if ok:
                # 删除的列数 = 总列数 - 保留列数
                best = min(best, m - k)
                # 已经找到最小的可能，直接返回
                return best
    return best
```

> 关键行解释  
> - `combinations(range(m), k)`：从 `0…m-1` 中挑出 `k` 列，类似“从字典里挑出想看的页码”。  
> - `new_row = [row[c] for c in keep]`：把保留下来的字符拼成新字符串。  
> - `any(new_row[i] > new_row[i + 1] ...)`：只要出现 “前一个字符更大”，就说明该行不满足非递减。

#### 复杂度  

- **时间复杂度**：`O(2^m * n * m)`  
  - `2^m` 是所有列子集的数量（每列要么删要么保）。  
  - 对每个子集要遍历 `n` 行，每行最多检查 `m` 个字符。  
  - **含义**：如果列数是 20，`2^20 ≈ 1,048,576`，已经很大；列数 100 时根本不可能跑完。  
- **空间复杂度**：`O(m)`  
  - 只用了常数级别的额外空间，主要是存放当前子集的下标列表。

> 暴力解虽然思路最直观，却因为指数级的枚举在本题（`m ≤ 100`）里不可行，只能作为“思考的起点”。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到：**我们关心的其实是保留的列的顺序**，而不是具体删掉哪些列。  
- **瓶颈**：暴力遍历所有子集，导致指数时间。  
- **关键观察**：如果我们决定保留列 `i`（在原序列中的位置），那么它左边所有已经保留下来的列 `j (j < i)` 必须满足：**对每一行的字符，列 `j` 的字符 ≤ 列 `i` 的字符**。换句话说，列 `j` 必须“在所有行上不大于”列 `i`。  

把每一列看成一个 **向量** `V_i = (strs[0][i], strs[1][i], …, strs[n‑1][i])`。  
我们要找的是最长的 **单调递增子序列**（LIS），但递增的比较是 **逐维（逐行）比较**：  

```
V_j ≤ V_i  ⇔  for every row r : strs[r][j] ≤ strs[r][i]
```

这正好构成一个 **有向无环图（DAG）**：  
- 节点是列 `0 … m-1`。  
- 若 `j < i` 且 `V_j ≤ V_i`，在 `j → i` 之间连一条有向边。  

在 DAG 中，**最长路径**的长度就是我们能保留的最多列数。  
因为 `m ≤ 100`，我们可以直接用 **动态规划** O(m²·n) 来求最长路径。

**DP 公式**  

```
dp[i] = 以第 i 列结尾的最长合法子序列长度
dp[i] = 1                                            # 只保留第 i 列本身
dp[i] = max(dp[j] + 1)   (j < i 且 V_j ≤ V_i)        # 选前面可以接上的列
```

答案 = `m - max(dp)`（总列数减去保留下来的最大列数）。

#### 代码（Python）

```python
def minDeletionSize(strs):
    """
    返回最少需要删除的列数，使得每一行的字符序列非递减。
    思路：把每一列看成向量，求在所有行上逐维递增的最长子序列。
    """
    n = len(strs)          # 行数
    m = len(strs[0])       # 列数

    # dp[i] 表示以第 i 列结尾的最长合法子序列长度
    dp = [1] * m           # 每列单独成序列长度为 1

    # 遍历所有列，尝试把它接在左边更小的列后面
    for i in range(m):
        for j in range(i):
            # 检查列 j 是否可以接在列 i 前面：所有行上字符不大于
            ok = True
            for r in range(n):
                if strs[r][j] > strs[r][i]:
                    ok = False
                    break
            if ok:
                dp[i] = max(dp[i], dp[j] + 1)

    # 最长可以保留的列数
    longest = max(dp)
    # 需要删除的列数 = 总列数 - 保留列数
    return m - longest
```

> 关键行解释  
> - `for i in range(m):`、`for j in range(i):`：遍历所有列对，保证顺序不被打乱（只能向右“跳”）。  
> - `if strs[r][j] > strs[r][i]:`：逐行比较，确保 **向量** `V_j ≤ V_i`。这一步相当于“检查两本书的每一页的字母是否不大于”。  
> - `dp[i] = max(dp[i], dp[j] + 1)`：如果可以接上，就把子序列长度加 1，取最大。  

#### 复杂度  

- **时间复杂度**：`O(m²·n)`  
  - 外层两层遍历列对是 `m²`（最多 10,000 次）。  
  - 每次比较要遍历 `n` 行（最多 100），所以总共约 `10⁶` 次基本操作。  
  - **含义**：相当于“一百个人两两比较，每次再看一百件事”，在本题约 0.01 秒即可跑完。  
- **空间复杂度**：`O(m)`  
  - 只用了 `dp` 长度为列数的数组，额外的常数空间。  

> 与暴力解对比：从指数级 `2^m` 降到多项式 `m²·n`，在 `m,n ≤ 100` 的限制下轻松通过。

---  

## 心得  

- **核心技巧**：把每一列看成一个多维向量，利用 **逐维非递减** 的关系把问题转化为 **最长递增子序列（LIS）** 的求解。  
- **适用的题型**  
  1. **Delete Columns to Make Sorted II** – 同样是逐行递增，只是要求最终的行序列也递增。  
  2. **Longest Chain of Pairs** – 把二维对 `(a,b)` 视作向量，求最长可接链。  
  3. **Maximum Width Ramp**（变形） – 需要在一维上满足 `nums[i] ≤ nums[j]`，本质是单维 LIS。  
- **一句话总结解题钥匙**：**把“列”抽象成“向量”，在向量间找最长的逐维递增链**。

---  

## 反思  

- **第一反应**：直接想遍历所有删除方案，检查每行是否有序——这自然是暴力思路。  
- **最容易踩的坑**  
  - 忘记**所有行**都必须满足 `col_j ≤ col_i`，只检查了一行会导致错误答案。  
  - 处理空子序列的情况：当所有列都需要删除时，`dp` 仍然要返回 0（本实现通过 `m - max(dp)` 自动得到）。  
  - 边界条件 `n = 1` 或 `m = 1`，仍然适用 DP，注意不要除以 0。  
- **下次类似题的第一步**：  
  1. 把“全局约束”转化为**局部比较**（比如列与列之间的逐维关系）。  
  2. 判断是否可以用 **DP / DAG 最长路径** 来求解，而不是枚举子集。  

这样就能快速从暴力思路跳到多项式解法，写出既正确又高效的代码。