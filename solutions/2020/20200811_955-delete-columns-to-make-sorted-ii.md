# #955. 删除列使其有序 II / Delete Columns to Make Sorted II

> 难度：中等 · 标签：Array、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/delete-columns-to-make-sorted-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of n strings strs, all of the same length.
We may choose any deletion indices, and we delete all the characters in those indices for each string.
For example, if we have strs = ["abcdef","uvwxyz"] and deletion indices {0, 2, 3}, then the final array after deletions is ["bef", "vyz"].
Suppose we chose a set of deletion indices answer such that after deletions, the final array has its elements in lexicographic order (i.e., strs[0] <= strs[1] <= strs[2] <= ... <= strs[n - 1]). Return the minimum possible value of answer.length.

**Examples**

**Example 1:**

```
Input: strs = ["ca","bb","ac"]
Output: 1
Explanation: 
After deleting the first column, strs = ["a", "b", "c"].
Now strs is in lexicographic order (ie. strs[0] <= strs[1] <= strs[2]).
We require at least 1 deletion since initially strs was not in lexicographic order, so the answer is 1.
```

**Example 2:**

```
Input: strs = ["xc","yb","za"]
Output: 0
Explanation: 
strs is already in lexicographic order, so we do not need to delete anything.
Note that the rows of strs are not necessarily in lexicographic order:
i.e., it is NOT necessarily true that (strs[0][0] <= strs[0][1] <= ...)
```

**Example 3:**

```
Input: strs = ["zyx","wvu","tsr"]
Output: 3
Explanation: We have to delete every column.
```

**Constraints**

- n == strs.length
- 1 <= n <= 100
- 1 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串数组 `strs`，所有字符串长度相同。  
我们可以选择任意若干列的索引进行删除，删除后每个字符串在这些列上的字符都会被去除。  
例如，若 `strs = ["abcdef","uvwxyz"]` 且删除列索引集合为 `{0, 2, 3}`，则删除后的数组为 `["bef", "vyz"]`。  

设我们选择的删除列集合为 `answer`，使得删除完成后得到的数组满足字典序（lexicographic order）  
`strs[0] <= strs[1] <= strs[2] <= ... <= strs[n‑1]`。返回 `answer` 的最小可能大小，即需要删除的列数的最小值。

---

### 示例

**示例 1**

```text
Input: strs = ["ca","bb","ac"]
Output: 1
Explanation:
删除第一列后，strs 变为 ["a","b","c"]。
此时 strs 已按字典序排列（即 strs[0] <= strs[1] <= strs[2]）。
因为最初 strs 并未满足字典序，需要至少删除 1 列，所以答案为 1。
```

**示例 2**

```text
Input: strs = ["xc","yb","za"]
Output: 0
Explanation:
strs 已经按字典序排列，无需删除任何列。
注意，strs 中的每一行本身不一定按字典序递增，即不一定满足 (strs[0][0] <= strs[0][1] <= ...)。
```

**示例 3**

```text
Input: strs = ["zyx","wvu","tsr"]
Output: 3
Explanation:
必须删除所有列。
```

---

### 约束条件

- `n == strs.length`
- `1 <= n <= 100`
- `1 <= strs[i].length <= 100`
- `strs[i]` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删除列集合**，找出其中能让字符串数组变成字典序且删除列最少的那一种。

- **数据结构**：把每一列当成一个“开关”。如果把第 `j` 列删除，就把它对应的开关设为 `1`，否则设为 `0`。整个开关序列（长度为 `m`，`m` 为字符串长度）就唯一决定了最终的字符串。
- **生活类比**：想象你在一本书里把某几页撕掉，剩下的页面顺序决定了读者看到的故事。我们要找出最少的页面数，使得阅读顺序符合字典序。
- **正确性**：只要遍历了 **所有** 可能的删除方案，就一定能找到最优解（因为最优解本身也是所有方案中的一个）。
- **复杂度分析**：  
  - 共有 `m` 列，每列有 “删 / 不删” 两种选择，所有方案数是 `2^m`（指数级）。  
  - 对每一种方案，需要把每行的剩余字符拼接起来再比较相邻两行的字典序，时间大约是 `O(n·m)`。  
  - 因此总时间是 `O(2^m · n·m)`，空间只需要保存当前方案的字符串，`O(n·m)`。

> **大白话**：`2^m` 就像把 10 列的灯全部打开或关闭，有 `2^10 = 1024` 种可能；如果列数是 20，可能性就变成 `1,048,576`，很快就算不过来。

#### 代码（Python）

```python
from itertools import product
from typing import List

def minDeletionSize_bruteforce(strs: List[str]) -> int:
    n = len(strs)
    m = len(strs[0])

    # 所有 0/1 组合，0 表示保留该列，1 表示删除该列
    best = m  # 最坏情况：全部删除
    for mask in product([0, 1], repeat=m):
        # 统计已经删除的列数，若已经不比当前 best 好，直接跳过
        deletions = sum(mask)
        if deletions >= best:
            continue

        # 生成删除后的新字符串列表
        new_strs = []
        for s in strs:
            kept = [ch for j, ch in enumerate(s) if mask[j] == 0]
            new_strs.append(''.join(kept))

        # 检查是否已按字典序排列
        ok = all(new_strs[i] <= new_strs[i + 1] for i in range(n - 1))
        if ok:
            best = deletions        # 找到更小的答案
    return best
```

> 代码要点  
> - `product([0,1], repeat=m)` 生成所有列的删除/保留组合。  
> - `mask[j] == 0` 表示第 `j` 列**不**被删除。  
> - `all(new_strs[i] <= new_strs[i+1] ...)` 用来判断最终数组是否已经有序。

#### 复杂度

- **时间复杂度**：`O(2^m · n·m)` —— 随着列数的增加会爆炸，实际只能在 `m ≤ 10` 左右的小例子里跑通。  
- **空间复杂度**：`O(n·m)` —— 需要存放每次删除后的 `new_strs`（每个字符串最长 `m`）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有列的删除组合**。  
我们注意到：**只要左边的列已经确定了两行的相对顺序，右边的列就不需要再去比较这两行**。这点可以帮助我们一步步“锁定”已经有序的相邻行对，从而决定是否需要删除当前列。

**核心贪心思想**（从左到右扫描列）：

1. 维护一个布尔数组 `sorted[i]`（`0 ≤ i < n-1`），表示第 `i` 行和第 `i+1` 行已经确定 `strs[i] < strs[i+1]`（即它们已经不再会因为后面的列产生冲突）。初始全为 `False`。
2. 从第 `0` 列开始检查：
   - **冲突检测**：如果在当前列中，出现了 `sorted[i] == False` 且 `strs[i][col] > strs[i+1][col]`，说明这对相邻行在这列上已经违背字典序，而它们之前的列都相等，**必须删除当前列**。此时计数 `ans += 1`，直接进入下一列（不更新 `sorted`）。
   - **安全保留**：如果没有上述冲突，则可以保留此列。随后遍历所有相邻行对，把 **严格小于** 的情况标记为已排序：`if strs[i][col] < strs[i+1][col]: sorted[i] = True`。这些行对以后就不需要再检查了。
3. 当所有列都处理完后，`ans` 即为最少需要删除的列数。

**为什么这个贪心是对的？**  
- 我们总是**尽量保留左边的列**，因为左边的列对字典序的影响最大。只有在**不可避免的冲突**（即某对未确定顺序的行在此列出现逆序）时才删除列。  
- 一旦把某对行标记为已排序，后面的列再怎么变化都不会破坏已经确认的顺序，因为字典序比较只在第一次出现不同字符时决定大小。  
- 由于每列只检查一次且只在冲突时删除，这保证了全局最优。

**类比**：想象一排排的小朋友在排队，每次只比较他们的第一件衣服颜色。如果颜色相同，继续比较第二件，以此类推。我们从左到右一次决定是否“裁掉”这件衣服（列），只在出现“前面小朋友颜色更深”而且之前的衣服都一样时才裁掉。

#### 代码（Python）

```python
from typing import List

def minDeletionSize(strs: List[str]) -> int:
    """
    贪心解：从左到右遍历列，只有在出现不可调和的逆序时才删除当前列。
    """
    n = len(strs)
    m = len(strs[0])
    # sorted[i] == True 表示第 i 行已确定小于第 i+1 行
    sorted_pair = [False] * (n - 1)
    deletions = 0

    for col in range(m):
        # 1. 检查当前列是否会导致冲突
        need_delete = False
        for i in range(n - 1):
            if not sorted_pair[i] and strs[i][col] > strs[i + 1][col]:
                need_delete = True
                break

        if need_delete:
            deletions += 1          # 删除该列
            continue                # 直接进入下一列，sorted_pair 不变

        # 2. 若不删除，则利用本列把已经确定顺序的行对标记出来
        for i in range(n - 1):
            if not sorted_pair[i] and strs[i][col] < strs[i + 1][col]:
                sorted_pair[i] = True

        # 若所有相邻行对都已确定顺序，后面直接可以停止（可选优化）
        if all(sorted_pair):
            break

    return deletions
```

> 代码要点  
> - `sorted_pair[i]` 相当于“这对兄弟已经不需要再比较”。  
> - `need_delete` 用来判断本列是否必须被删除。  
> - 一旦 `sorted_pair` 全部为 `True`，说明已经保证整个数组有序，后面的列无论保留与否都不会影响答案（可以提前结束循环，进一步提升效率）。

#### 复杂度

- **时间复杂度**：`O(n·m)` —— 每列最多遍历一次所有相邻行对。相比暴力的指数级，线性时间在 `n,m ≤ 100` 的限制下轻松通过。  
- **空间复杂度**：`O(n)` —— 只需要 `sorted_pair` 数组来记录相邻行对的状态。

---

## 心得

- **核心技巧**：**贪心 + “已排序对” 记忆**。从左到右决定是否删除列，只在出现不可调和的逆序时动手，已确定顺序的行对以后不再参与比较。
- **适用题型**：  
  1. **Delete Columns to Make Sorted I**（只需要判断每列是否单调递增，可直接统计不满足的列）。  
  2. **Monotone Increasing Subsequence**（需要保留顺序的子序列，类似的“首次出现不同”原则）。  
  3. **Minimum Deletion Size to Make Array Sorted**（数组而非字符串，思路相同）。
- **一句话总结**：**“只在左侧已经相等且右侧出现逆序时才删列”，把已经确定顺序的行对锁定，即可得到最少删除次数。**

---

## 反思

- **第一反应**：看到“删除列后使数组有序”，立刻想到“枚举所有列的删除组合”。这导致想到暴力解，但很快会发现 `2^m` 爆炸。
- **最容易踩的坑**  
  1. **忽视已排序对**：如果每次都重新比较所有行对，会错过可以提前锁定的机会，导致误删列。  
  2. **边界条件**：当只有一行或一列时，答案必然是 `0`，代码需要能够自然处理 `n-1 = 0` 的 `sorted_pair`。  
  3. **提前结束的时机**：如果所有相邻行对已经确定顺序，后面的列可以直接跳过，忘记这一步会多余的遍历，虽不影响正确性但影响效率。
- **下次遇到同类题**：第一步先思考 **“从左到右，什么时候必须删除？”**，找出“已确定顺序的子问题”，再用贪心或动态规划把它们固定下来。这样往往能把指数级搜索压缩到线性时间。