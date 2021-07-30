# #1415. 长度为 n 的所有快乐字符串的第 k 小字典序字符串 / The k-th Lexicographical String of All Happy Strings of Length n

> 难度：中等 · 标签：String、Backtracking · [LeetCode 链接](https://leetcode.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/)

---

## 题目（英文原版）

**Description**

A happy string is a string that:
For example, strings "abc", "ac", "b" and "abcbabcbcb" are all happy strings and strings "aa", "baa" and "ababbc" are not happy strings.
Given two integers n and k, consider a list of all happy strings of length n sorted in lexicographical order.
Return the kth string of this list or return an empty string if there are less than k happy strings of length n.

**Examples**

**Example 1:**

```
Input: n = 1, k = 3
Output: "c"
Explanation: The list ["a", "b", "c"] contains all happy strings of length 1. The third string is "c".
```

**Example 2:**

```
Input: n = 1, k = 4
Output: ""
Explanation: There are only 3 happy strings of length 1.
```

**Example 3:**

```
Input: n = 3, k = 9
Output: "cab"
Explanation: There are 12 different happy string of length 3 ["aba", "abc", "aca", "acb", "bab", "bac", "bca", "bcb", "cab", "cac", "cba", "cbc"]. You will find the 9th string = "cab"
```

**Constraints**

- 1 <= n <= 10
- 1 <= k <= 100

---

## 题目（中文翻译）

一个 **快乐字符串（happy string）** 定义为仅由字符 `'a'`、`'b'`、`'c'` 组成且任意相邻两个字符都不相同的字符串。  

例如，字符串 `"abc"`、`"ac"`、`"b"`、`"abcbabcbcb"` 都是快乐字符串，而 `"aa"`、`"baa"`、`"ababbc"` 不是快乐字符串。  

给定两个整数 `n` 和 `k`，考虑所有长度为 `n` 的快乐字符串，按字典序（lexicographical order）排列成的列表。  
返回该列表中第 `k` 个字符串；如果长度为 `n` 的快乐字符串总数少于 `k`，则返回空字符串 `""`。

## 示例

### 示例 1  
**输入**: `n = 1, k = 3`  
**输出**: `"c"`  
**解释**: 列表 `["a", "b", "c"]` 包含所有长度为 1 的快乐字符串。第 3 个字符串是 `"c"`。

### 示例 2  
**输入**: `n = 1, k = 4`  
**输出**: `""`  
**解释**: 只有 3 个长度为 1 的快乐字符串。

### 示例 3  
**输入**: `n = 3, k = 9`  
**输出**: `"cab"`  
**解释**: 长度为 3 的快乐字符串共有 12 种，按字典序排列为  
`["aba", "abc", "aca", "acb", "bab", "bac", "bca", "bcb", "cab", "cac", "cba", "cbc"]`。第 9 个字符串即为 `"cab"`。

## 约束条件
- `1 <= n <= 10`
- `1 <= k <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有满足条件的字符串全部列出来**，然后按字典序（lexicographical order）排序，最后直接取第 `k` 个。  
- **数据结构**：我们用一个列表 `res` 来保存所有 “happy string”。列表就像装东西的盒子，往里 `append` 就是往盒子里放东西。  
- **happy string 的定义**：相邻字符不能相同。我们可以用**回溯（backtracking）**的方式逐位尝试 `'a'、'b'、'c'`，只要当前字符和前一个字符不同，就把它加入当前路径；当路径长度达到 `n` 时，把完整的字符串加入 `res`。  
- **为什么一定能得到正确答案**：回溯会遍历 **所有** 可能的字符组合，而我们在加入路径前做了 “相邻字符不同” 的检查，所以得到的每一个字符串必然是 happy 的；而我们遍历完所有可能后，`res` 中就恰好装了 **全部** happy strings。  

#### 代码（Python）

```python
def getHappyString_bruteforce(n: int, k: int) -> str:
    """暴力版：生成全部 happy string，排序后返回第 k 个（1-indexed）"""
    happy = []                     # 用来装所有合法字符串

    def backtrack(path: str):
        """递归生成长度为 n 的 happy string，path 为已经构造好的前缀"""
        if len(path) == n:         # 已经达到目标长度
            happy.append(path)     # 保存完整字符串
            return
        for ch in 'abc':           # 按字典序尝试 a、b、c
            if not path or ch != path[-1]:   # 保证相邻字符不同
                backtrack(path + ch)         # 继续往下尝试

    backtrack("")                  # 从空串开始构造
    happy.sort()                   # 字典序排序（列表自带的 sort 就是字典序）
    # k 是 1-indexed，list 是 0-indexed
    return happy[k - 1] if k <= len(happy) else ""
```

#### 复杂度

- **时间复杂度**：`O(3 * 2^{n-1} + m log m)`  
  - 生成所有 happy string 的过程：第 1 位有 3 种选择，后面的每一位只能选 **除去上一个字符的另外 2 种**，所以总数是 `3 * 2^{n-1}`，每个字符串的构造都需要 O(n) 的时间，但 `n ≤ 10`，常数可以忽略。  
  - 排序需要 `m log m`，其中 `m = 3 * 2^{n-1}` 是字符串的数量。  
  - 用大白话说，就是“先把所有可能的组合列出来（数量会指数级增长），再把它们排个序”。  
- **空间复杂度**：`O(m * n)`  
  - 需要把所有字符串存进列表，每个字符串长度是 `n`，共 `m` 条，所以占用的空间是 `m*n`。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“全部生成再排序”**，当 `n` 稍大时，字符串的数量会呈指数增长（虽然本题 `n ≤ 10`，但培养好的思维仍然重要）。  
我们可以 **直接定位第 k 个**，不必真的把前面的全部列出来。核心思路如下：

1. **先算出每个前缀可以产生多少个完整 happy string**。  
   - 第一个字符可以是 `'a'、'b'、'c'`（3 种），每选定一个后，后面每一位只能在 **剩下的两个字符** 中选，且相互独立。  
   - 因此，固定了前缀长度为 `len`，剩余 `remain = n - len` 位可以产生 `2^{remain}` 种不同的完成方式（因为每位都有 2 种选择）。  
2. **按字典序遍历字符**，利用上面的计数直接跳过不需要的整块子树。  
   - 例如，当前已经决定了前缀 `"a"`，还有 `remain = n-1` 位未决定。  
   - 以 `'a'` 为前缀的所有 happy string 共 `2^{remain}` 条。如果 `k` 大于这个数量，说明第 k 个不在这块里，我们可以 **直接把 k 减去这块的大小**，并尝试下一个字符 `'b'`。  
   - 当 `k` 落在某个字符对应的块里时，就把这个字符加入答案，继续处理下一位。  
3. **递归/循环实现**：每一步只做 O(1) 的计数和比较，最多循环 `n` 次，整体时间是 O(n)。  

**类比**：想象有三本书 `A、B、C`，每本书里都有 `2^{remain}` 页的章节。我们要找第 `k` 章节所在的书。先看 `A` 书的章节数，如果 `k` 超过它，就把 `k` 减掉 `A` 的章节数，转而看 `B` 书，依次类推。这样我们不需要把所有章节真的写出来，只用计数就能定位。

#### 代码（Python）

```python
def getHappyString_optimal(n: int, k: int) -> str:
    """最优解：利用计数直接构造第 k 个 happy string（1-indexed）"""
    # 先算出每个前缀后面还能产生多少种组合
    # cnt[i] 表示长度为 i 的前缀后，还剩 (n-i) 位可以填的组合数
    cnt = [1] * (n + 1)            # cnt[n] = 1，表示已经填满时只剩一种“空”方式
    for i in range(n - 1, -1, -1):
        cnt[i] = cnt[i + 1] * 2    # 每往前一位，多出 2 种选择

    total = 3 * cnt[1]             # 所有 happy string 的总数 = 3 * 2^{n-1}
    if k > total:                  # 如果 k 超出范围，直接返回空串
        return ""

    ans = []                       # 用列表收集字符，最后 join 成字符串
    prev = ''                      # 前一个字符，初始为空
    # 依次决定第 0、1、2... 位的字符
    for pos in range(n):
        # 当前可以选的字符集合（按照字典序）
        for ch in 'abc':
            if ch == prev:         # 不能和前一个相同，跳过
                continue
            # 以 ch 为当前位置的前缀，后面还能产生 cnt[pos+1] 种完整字符串
            block = cnt[pos + 1]
            if k > block:          # 第 k 个不在这个块里，跳过
                k -= block
            else:                  # 第 k 个就在这个块里，确定这个字符
                ans.append(ch)
                prev = ch
                break               # 进入下一位的决定
    return ''.join(ans)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只循环 `n` 次（`n ≤ 10`），每次在 `'a','b','c'` 中最多检查 3 次，所有操作都是常数时间。  
  - 与暴力解相比，省掉了 `2^{n-1}` 级别的遍历和排序，真正做到“只看需要的那一条”。  
- **空间复杂度**：`O(1)`（不计输出字符串本身）  
  - 只用了几个整数和一个长度为 `n` 的字符列表，和 `n` 成线性关系，常数级别的额外空间。

---

## 心得

- **核心技巧**：**利用递归计数（或叫“子树大小剪枝”）直接定位第 k 项**，而不是枚举全部。  
- **适用的题型**：  
  1. “第 k 个字典序排列/组合” 类（如第 K 个排列序列、第 K 个无重复字符的字符串）。  
  2. “计数剪枝” 需要在搜索树中快速跳过整块不相关子树的场景（如 LeetCode 440. K-th Smallest in Lexicographical Order）。  
- **一句话总结解题钥匙**：**先算出每一步可以产生多少种结果，利用这个数字在字典序上“跳块”定位**。

---

## 反思

- **第一反应**：看到 “happy string” 只要相邻字符不同，立刻想到回溯枚举所有可能，然后排序取第 k。  
- **最容易踩的坑**：  
  - 忘记 **相邻字符不能相同** 的约束，导致生成了非法字符串。  
  - 在暴力解里忘记把 `k` 当作 **1-indexed**（题目要求第 k 个），导致返回下标错误。  
  - 对计数剪枝的实现不够严谨时，容易出现 `k` 没有在任何块里而仍继续循环，导致错误答案或索引越界。  
- **下次类似题的第一步**：先 **估算每一步的分支数量**（子树大小），判断是否可以用计数直接跳过，而不是直接把所有组合都写出来。这样思路更清晰，代码也更高效。