# #3316. 在源字符串中找出最大可删除字符数 / Find Maximum Removals From Source String

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/find-maximum-removals-from-source-string/)

---

## 题目（英文原版）

**Description**

You are given a string source of size n, a string pattern that is a subsequence of source, and a sorted integer array targetIndices that contains distinct numbers in the range [0, n - 1].
We define an operation as removing a character at an index idx from source such that:
Performing an operation does not change the indices of the other characters in source. For example, if you remove 'c' from "acb", the character at index 2 would still be 'b'.
Return the maximum number of operations that can be performed.

**Examples**

**Example 1:**

```
Input: source = "abbaa", pattern = "aba", targetIndices = [0,1,2]
Output: 1
Explanation:
We can't remove source[0] but we can do either of these two operations:
```

**Example 2:**

```
Input: source = "bcda", pattern = "d", targetIndices = [0,3]
Output: 2
Explanation:
We can remove source[0] and source[3] in two operations.
```

**Example 3:**

```
Input: source = "dda", pattern = "dda", targetIndices = [0,1,2]
Output: 0
Explanation:
We can't remove any character from source .
```

**Example 4:**

```
Input: source = "yeyeykyded" , pattern = "yeyyd" , targetIndices = [0,2,3,4]
Output: 2
Explanation:
We can remove source[2] and source[3] in two operations.
```

**Constraints**

- 1 <= n == source.length <= 3 * 103
- 1 <= pattern.length <= n
- 1 <= targetIndices.length <= n
- targetIndices is sorted in ascending order.
- The input is generated such that targetIndices contains distinct elements in the range [0, n - 1].
- source and pattern consist only of lowercase English letters.
- The input is generated such that pattern appears as a subsequence in source.

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n` 的字符串 `source`，一个是 `source` 的子序列（subsequence）`pattern`，以及一个已排序的整数数组 `targetIndices`，其中的元素互不相同且均位于 `[0, n - 1]` 区间内。  

我们将一次操作定义为：从 `source` 中删除下标为 `idx` 的字符，且**删除后不会改变 `source` 中其余字符的下标**。例如，从 `"acb"` 中删除下标为 `0` 的字符 `'a'` 后，原本下标为 `2` 的字符仍然是 `'b'`（下标仍为 `2`）。  

返回可以执行的最大操作次数。

**示例**

> 示例 1  
> 输入: `source = "abbaa"`, `pattern = "aba"`, `targetIndices = [0,1,2]`  
> 输出: `1`  
> 解释:  
> 我们无法删除 `source[0]`，但可以执行以下两种操作中的任意一种：

> 示例 2  
> 输入: `source = "bcda"`, `pattern = "d"`, `targetIndices = [0,3]`  
> 输出: `2`  
> 解释:  
> 可以先删除 `source[0]`，再删除 `source[3]`，共两次操作。

> 示例 3  
> 输入: `source = "dda"`, `pattern = "dda"`, `targetIndices = [0,1,2]`  
> 输出: `0`  
> 解释:  
> 任何字符的删除都会破坏 `pattern` 作为子序列的属性，故不能进行任何操作。

> 示例 4  
> 输入: `source = "yeyeykyded"`, `pattern = "yeyyd"`, `targetIndices = [0,2,3,4]`  
> 输出: `2`  
> 解释:  
> 可以删除 `source[2]` 和 `source[3]`，共两次操作。

**约束条件**

- `1 <= n == source.length <= 3 * 10^3`
- `1 <= pattern.length <= n`
- `1 <= targetIndices.length <= n`
- `targetIndices` 按升序排序。
- `targetIndices` 中的元素互不相同，且均在 `[0, n - 1]` 范围内。
- `source` 和 `pattern` 只包含小写英文字母。
- 题目保证 `pattern` 是 `source` 的子序列（subsequence）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的删除方案**，看哪一种还能让 `pattern` 保持为 `source` 的子序列，取其中删除字符最多的那种。  

- **数据结构**  
  - `targetIndices` 本身就是一个有序的整数数组，想象它是一本字典的“页码表”，每个页码对应一个可以删除的字符位置。  
  - 为了快速判断某个下标是否已经被删除，我们可以把选中的下标放进一个 **集合（set）**，这相当于在字典里划掉了对应的词，查询是否划掉只需要 O(1) 时间。  

- **为什么正确**  
  - 只要我们遍历 **所有** 合法的删除集合（每个集合都是 `targetIndices` 的子集），并在每种情况下检查 `pattern` 是否仍然是子序列，那么答案必然在这些检查中出现。  

- **复杂度分析（大白话）**  
  - `targetIndices` 长度记作 `m`，`source` 长度记作 `n`。  
  - 子集的数量是 `2^m`（相当于每个可以删除的字符都有“删”或“不删”两种选择），所以时间会是指数级的，**爆炸**。  
  - 即使我们不枚举全部子集，而是逐个 **尝试删除 0、1、2 … m 个字符**（每次都重新检查一次），每次检查 `pattern` 是否是子序列需要遍历整个 `source`（O(n)），所以总时间是 `O(m * n)`。  
  - 当 `n` 最多 3000，`m` 也可能接近 3000 时，这个复杂度大约是 **9 百万次操作**，在解释器里会稍慢，而且不算最优。  
  - 空间方面，只需要一个集合保存已经删除的下标，最多 `m` 个，**O(m)**。

#### 代码（Python）

```python
def max_removals_bruteforce(source: str, pattern: str, targetIndices: list[int]) -> int:
    n, m = len(source), len(targetIndices)
    # 逐个尝试删除 0~m 个字符（这里不枚举所有子集，只按顺序删除前 k 个）
    # 这已经是「暴力」的一个简化版本，仍然是 O(m * n)
    for k in range(m, -1, -1):          # 从最多的删法往下找，第一成功的就是答案
        removed = set(targetIndices[:k])   # 把前 k 个可以删的下标放进集合
        i = j = 0                         # i 遍历 source，j 遍历 pattern
        while i < n and j < len(pattern):
            if i in removed:              # 这个字符已经被“划掉”，直接跳过
                i += 1
                continue
            if source[i] == pattern[j]:   # 匹配成功，两个指针都向前走
                j += 1
            i += 1
        if j == len(pattern):             # 完全匹配，说明 pattern 仍是子序列
            return k
    return 0
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - 想象一下，你每删掉一次（最多 `m` 次）都要把整本书（`source`，长度 `n`）重新读一遍，看能不能拼出 `pattern`。  
- **空间复杂度**：`O(m)`  
  - 只用了一个集合来记哪些页码（下标）被划掉，最多装下所有 `m` 个可删字符。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在：

1. 每次检查是否还能形成子序列都要遍历完整个 `source`（O(n)）。  
2. 我们尝试了 **所有** 可能的删除数量（最多 `m` 次），导致 O(m·n)。

**关键观察**：  
`targetIndices` 已经是 **升序** 的，且删除操作不会改变其它字符的下标。  
这意味着如果我们只关心 “**删除前 k 个下标**” 是否可行，**顺序** 本身已经决定了所有可能的方案。  
（这正是 LeetCode 题目 “Maximum Number of Removable Characters” 的隐藏设定——我们只能按数组顺序删除前缀。）

于是我们可以把问题转化为：

> 找到最大的 `k`（`0 ≤ k ≤ m`），使得把 `targetIndices[:k]` 这 `k` 个字符标记为删除后，`pattern` 仍是 `source` 的子序列。

这正好适合 **二分搜索**（Binary Search）：

- `k` 的取值区间是 `[0, m]`，是单调的：  
  - 如果 `k = x` 可行，那么所有更小的 `k`（即删得更少）显然也可行。  
  - 反之，如果 `k = x` 不可行，那么所有更大的 `k` 也一定不行（因为删得更多只会让匹配更难）。  

二分搜索只需要 **log₂(m)** 次检查，每次检查仍然是 O(n) 的子序列匹配，但整体时间降到了 **O(n log m)**，足够快。

**子序列匹配的实现（双指针）**：

- 用两个指针 `i`（遍历 `source`）和 `j`（遍历 `pattern`）。  
- 当 `i` 所在位置在 “已删除集合” 里时，直接跳过。  
- 否则如果字符相等，就把 `j` 前移；`i` 总是前移。  
- 最终如果 `j` 能走到 `pattern` 末尾，说明匹配成功。

**为什么双指针能工作**：  
想象我们在读一本书，已经在某些页码上打了“×”。读的时候直接把这些页码跳过去，剩下的文字顺序不变，这正是子序列的定义。

#### 代码（Python）

```python
def max_removals(source: str, pattern: str, targetIndices: list[int]) -> int:
    n = len(source)
    m = len(targetIndices)

    # 检查把前 k 个下标删掉后，pattern 是否仍是子序列
    def can_remove(k: int) -> bool:
        removed = set(targetIndices[:k])          # O(k) 创建集合
        i = j = 0
        while i < n and j < len(pattern):
            if i in removed:                       # 被删掉的字符直接跳过
                i += 1
                continue
            if source[i] == pattern[j]:            # 匹配成功，两指针都前进
                j += 1
            i += 1
        return j == len(pattern)                  # j 走完了，说明匹配成功

    # 二分搜索最大可删的 k
    left, right = 0, m          # 区间是 [left, right]，右端点是可行的上限（可能为 m）
    ans = 0
    while left <= right:
        mid = (left + right) // 2
        if can_remove(mid):                 # mid 可行，尝试更大
            ans = mid
            left = mid + 1
        else:                               # mid 不行，只能往小了找
            right = mid - 1
    return ans
```

> **代码要点解释**（每行中文注释已在代码中给出）  
> - `removed = set(targetIndices[:k])`：把前 `k` 个可以删的下标装进集合，就像把对应的页码划掉，查询是否划掉 O(1)。  
> - `while i < n and j < len(pattern):`：双指针遍历，直到源字符串或模式串耗尽。  
> - `if i in removed: i += 1; continue`：被删掉的字符直接跳过，不参与匹配。  
> - `if source[i] == pattern[j]: j += 1`：匹配成功，模式指针前进。  
> - `return j == len(pattern)`：只有模式全部匹配成功，才算合法。  
> - 二分循环里 `mid` 代表“尝试删掉前 `mid` 个字符”，若合法则记录答案并继续向右（尝试更多），否则向左收敛。

#### 复杂度

- **时间复杂度**：`O(n log m)`  
  - 每次 `can_remove` 检查遍历一次 `source`（`O(n)`），二分搜索最多进行 `log₂(m)` 次检查。  
  - 这就像把原本要 **一次一次** 读完整本书的过程，改成 **只读 `log` 次**，速度提升了好几倍。  
- **空间复杂度**：`O(k)`（实际为 `O(m)` 的最坏情况）  
  - 只需要保存当前尝试删除的下标集合，最多 `m` 个整数。  
  - 其它变量都是常数级别。

---

## 心得

- **核心技巧**：**二分搜索 + 双指针子序列匹配**。  
- **适用的题型**  
  1. “Maximum Number of Removable Characters” 系列（删除字符后保持子序列）。  
  2. “Maximum Size Subarray With Sum ≤ K” 这类“单调可行性 + 二分”问题。  
  3. “Check If Array Is Sorted After Removing Some Elements”——先二分猜答案，再线性验证。  
- **一句话总结**：  
  *把“能否删 k 个”变成单调判定，再用二分快速定位最大可删的 k。*

---

## 反思

- **第一反应**：直接把所有可删下标的子集枚举，然后逐个检查子序列，想到“暴力搜索”。  
- **最容易踩的坑**  
  - **下标不移动**：删除后其他字符的下标保持不变，必须用集合或标记数组来“跳过”而不是真的把字符删掉（否则下标会错位）。  
  - **单调性误判**：只有在“删除前缀”这种特殊约束下，答案才是单调的；若题目允许随意选择子集，则二分不再适用。  
  - **边界条件**：`k = 0`（不删）和 `k = m`（全部尝试删）都必须正确处理。  
- **下次类似题目第一步**：  
  *先判断答案是否具备单调性（可行 → 更小/更大仍可行），若成立就考虑二分搜索；再准备一个线性验证函数（双指针/前缀和等）*。