# #2901. **最长不相等相邻分组子序列 II** / Longest Unequal Adjacent Groups Subsequence II

> 难度：中等 · 标签：Array、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-unequal-adjacent-groups-subsequence-ii/)

---

## 题目（英文原版）

**Description**

You are given a string array words, and an array groups, both arrays having length n.
The hamming distance between two strings of equal length is the number of positions at which the corresponding characters are different.
You need to select the longest subsequence from an array of indices [0, 1, ..., n - 1], such that for the subsequence denoted as [i0, i1, ..., ik-1] having length k, the following holds:
Return a string array containing the words corresponding to the indices (in order) in the selected subsequence. If there are multiple answers, return any of them.
Note: strings in words may be unequal in length.

**Examples**

**Example 1:**

```
Input: words = ["bab","dab","cab"], groups = [1,2,2]
Output: ["bab","cab"]
Explanation: A subsequence that can be selected is [0,2] .
So, a valid answer is [words[0],words[2]] = ["bab","cab"] .
Another subsequence that can be selected is [0,1] .
So, another valid answer is [words[0],words[1]] = ["bab","dab"] .
It can be shown that the length of the longest subsequence of indices that satisfies the conditions is 2 .
```

**Example 2:**

```
Input: words = ["a","b","c","d"], groups = [1,2,3,4]
Output: ["a","b","c","d"]
Explanation: We can select the subsequence [0,1,2,3] .
It satisfies both conditions.
Hence, the answer is [words[0],words[1],words[2],words[3]] = ["a","b","c","d"] .
It has the longest length among all subsequences of indices that satisfy the conditions.
Hence, it is the only answer.
```

**Constraints**

- 1 <= n == words.length == groups.length <= 1000
- 1 <= words[i].length <= 10
- 1 <= groups[i] <= n
- words consists of distinct strings.
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `words` 和一个整数数组 `groups`，两个数组的长度均为 `n`。  
两个等长字符串之间的汉明距离（Hamming distance）定义为对应位置字符不同的个数。  

要求从索引数组 `[0, 1, ..., n - 1]` 中选取一个最长的子序列，使得该子序列记为 `[i₀, i₁, ..., i_{k-1}]`（长度为 `k`）时满足题目给出的条件（略）。  

返回一个字符串数组，包含所选子序列对应的单词，顺序保持与子序列中的索引顺序一致。如果存在多个答案，返回任意一个即可。  

> 注：`words` 中的字符串长度可能不相等。

### 示例

**示例 1**

```
输入: words = ["bab","dab","cab"], groups = [1,2,2]
输出: ["bab","cab"]
解释: 可以选取的一个子序列是 [0,2]，因此合法答案为 [words[0], words[2]] = ["bab","cab"]。
另一个可选的子序列是 [0,1]，对应的合法答案为 [words[0], words[1]] = ["bab","dab"]。
可以证明，满足条件的最长索引子序列的长度为 …
（原题内容已截断）
```

**示例 2**

```
输入: words = ["a","b","c","d"], groups = [1,2,3,4]
输出: ["a","b","c","d"]
解释: 我们可以选取子序列 [0,1,2,3]，它同时满足所有条件。
因此答案为 [words[0],words[1],words[2],words[3]] = ["a","b","c","d"]。
该答案在所有满足条件的索引子序列中长度最长，所以它是唯一的答案。
```

### 约束条件

- `1 <= n == words.length == groups.length <= 1000`
- `1 <= words[i].length <= 10`
- `1 <= groups[i] <= n`
- `words` 中的字符串互不相同。
- `words[i]` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把所有可能的子序列都枚举出来**，然后检查每个子序列是否满足题目要求：  

1. 相邻两个下标对应的 `groups` 必须不相等；  
2. 两个单词的长度必须相同；  
3. 两个单词的 **Hamming 距离**（对应位置不同的字符个数）恰好为 1。  

如果满足，就记下它的长度，最后取最长的那个。  

- **用到的数据结构**  
  - `list`（列表）保存当前枚举的下标序列。  
  - “哈希表”在这里其实不需要，用 **字典** 来存 `words[i] -> i` 只会让检查更快，但暴力解不依赖它。  
  - **Hamming 距离**的计算可以类比成“查字典”。我们把两个单词当成两本书，同一页（同一字符位置）如果字不同，就记一笔，最后统计笔数。  

- **为什么这个方法正确**  
  因为我们把**所有**合法子序列都遍历了一遍，只要有合法解一定会被找到，最长的自然不会错过。  

- **复杂度分析（大白话）**  
  - 枚举所有子序列的数量是 `2^n`（每个下标要么选要么不选），相当于把 0/1 开关打开 1000 次，根本不可能在电脑里跑完。  
  - 对每个子序列我们还要检查相邻元素的 3 条条件，每检查一次要遍历单词的每个字符（最多 10），所以每个子序列的检查成本是 `O(k·L)`（k 为子序列长度，L ≤ 10）。  
  - 综合起来时间复杂度是 **指数级** `O(2^n · n · L)`，空间只需要保存递归栈或当前子序列，`O(n)`。  
  - 用大白话说：如果 n=20，`2^20≈10⁶` 已经接近一百万次循环；n=30 时已经是十亿次，根本跑不完。  

#### 代码（Python）  

```python
from typing import List

def hamming_one(a: str, b: str) -> bool:
    """返回 True 当且仅当 a 与 b 长度相等且恰好有 1 个字符不同"""
    if len(a) != len(b):
        return False
    diff = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            diff += 1
            if diff > 1:          # 超过 1 就直接返回 False，省掉后面的比较
                return False
    return diff == 1

def longest_unequal_adjacent_bruteforce(words: List[str], groups: List[int]) -> List[str]:
    n = len(words)
    best_seq: List[int] = []          # 记录最佳下标序列

    def dfs(idx: int, cur_seq: List[int]) -> None:
        """深度优先搜索，从 idx 开始决定是否把它加入当前序列"""
        nonlocal best_seq
        # 结束条件：已经遍历完所有下标
        if idx == n:
            if len(cur_seq) > len(best_seq):
                best_seq = cur_seq[:]   # 复制一份保存
            return

        # 选 idx：检查是否能接在当前序列后面
        if not cur_seq:
            # 序列为空，直接加入
            dfs(idx + 1, cur_seq + [idx])
        else:
            j = cur_seq[-1]                     # 前一个下标
            if (groups[idx] != groups[j] and
                len(words[idx]) == len(words[j]) and
                hamming_one(words[idx], words[j])):
                dfs(idx + 1, cur_seq + [idx])  # 选 idx

        # 不选 idx：直接跳过
        dfs(idx + 1, cur_seq)

    dfs(0, [])
    return [words[i] for i in best_seq]
```

> 代码里每一行都有中文注释，帮助你把抽象的递归过程映射到实际的“选 / 不选”操作上。  

#### 复杂度  

- **时间复杂度**：`O(2^n · n · L)`（指数级）——因为会遍历所有子序列。  
  - `2^n` 表示“每个位置选或不选”；  
  - `n` 是检查相邻元素时最坏需要遍历的次数；  
  - `L ≤ 10` 是单词长度，算作常数。  
- **空间复杂度**：`O(n)`——递归栈深度最多 `n`，以及保存当前序列的列表。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于它把“选哪几个下标”这件事全部枚举了。实际上，**子序列的顺序已经固定为原数组的顺序**，我们只需要关心“以某个下标结尾的最长合法子序列有多长”。这正好符合**动态规划（DP）**的思想：  

1. **状态**  
   - `dp[i]`：以 `words[i]`（即下标 `i`）结尾的最长合法子序列的长度。  
   - `pre[i]`：构成该最长子序列的前一个下标（用于后续回溯得到答案）。  

2. **状态转移**  
   对每个 `i`，我们尝试把它接在前面所有可以合法连接的 `j (j < i)` 之后：  

   - `groups[i] != groups[j]`（组号不同）  
   - `len(words[i]) == len(words[j])`（单词长度相同）  
   - `hamming_one(words[i], words[j])` 为 `True`（恰好只有 1 个字符不同）  

   若上述条件都满足，`dp[i]` 可以由 `dp[j] + 1` 获得。我们取所有满足条件的 `j` 中 `dp[j]` 的最大值即可。  

   ```text
   dp[i] = max( dp[j] ) + 1   (j < i 且满足三个条件)
   如果没有满足条件的 j，则 dp[i] = 1（单独成一个子序列）
   ```

3. **答案构造**  
   - 找到 `dp` 中的最大值 `max_len`，以及对应的下标 `pos`（若有多个随便取一个）。  
   - 从 `pos` 开始，用 `pre[pos]` 一直往前追溯，得到完整的下标序列（倒序）。  
   - 最后把下标映射回 `words` 即可。  

4. **为什么是最优**  
   - 每个下标只会被计算一次，所有可能的前驱 `j` 只遍历一次，**时间复杂度降到了 `O(n²·L)`**。  
   - `n ≤ 1000`，`L ≤ 10`，所以 `n²·L ≤ 10⁶`，在 Python 中毫秒级完成。  

5. **关键工具——计算 Hamming 距离**  
   - 直接遍历字符比较，计数不同的位数，一旦超过 1 就提前返回 `False`，可以省掉不必要的比较。  

#### 代码（Python）  

```python
from typing import List

def hamming_one(a: str, b: str) -> bool:
    """判断两个等长字符串是否恰好只在 1 个位置不同"""
    if len(a) != len(b):
        return False
    diff = 0
    for ca, cb in zip(a, b):
        if ca != cb:
            diff += 1
            if diff > 1:          # 超过 1 直接退出，省时
                return False
    return diff == 1            # 必须恰好等于 1

def longest_unequal_adjacent_dp(words: List[str], groups: List[int]) -> List[str]:
    n = len(words)
    dp = [1] * n                 # 每个位置至少可以单独成长度 1 的子序列
    pre = [-1] * n               # 前驱下标，-1 表示没有前驱

    # 主循环：从左到右枚举结尾位置 i
    for i in range(n):
        # 枚举所有可能的前驱 j（j 必须在 i 左边）
        for j in range(i):
            # 只在满足题目三条条件时考虑转移
            if groups[i] != groups[j] and \
               len(words[i]) == len(words[j]) and \
               hamming_one(words[i], words[j]):
                # 若把 i 接在 j 后能得到更长的序列，就更新 dp[i] 与 pre[i]
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    pre[i] = j

    # 找到最长的长度以及对应的下标
    max_len = max(dp)
    pos = dp.index(max_len)      # 取第一个出现的最大下标

    # 通过前驱数组回溯得到下标序列（倒序）
    idx_seq: List[int] = []
    while pos != -1:
        idx_seq.append(pos)
        pos = pre[pos]
    idx_seq.reverse()            # 正序

    # 把下标映射回单词返回
    return [words[i] for i in idx_seq]
```

> 代码要点注释已写在每行旁边，帮助你把“状态转移”这一抽象概念具体化为 **两层循环 + 条件检查** 的实现。  

#### 复杂度  

- **时间复杂度**：`O(n²·L)`  
  - 外层循环 `i` 遍历 `n` 次，内层循环 `j` 最多遍历 `i-1` 次，合计约 `n·(n-1)/2 ≈ n²/2` 次。  
  - 每次检查需要比较两个单词的字符（最长 10），所以乘以 `L`。  
  - 用大白话说：如果 `n=1000`，大约需要 500,000 次比较，每次最多看 10 个字符，整体仍在几百万次操作之内，跑得非常快。  

- **空间复杂度**：`O(n)`  
  - `dp`、`pre` 两个长度为 `n` 的数组 plus 最后返回的结果列表。  

---

## 心得  

- **核心技巧**：**一维动态规划 + 前驱数组**（把“以 i 结尾的最优子结构”记下来），配合**Hamming 距离的快速判断**。  
- **该技巧适用的题型**（可在面试中举例）：  
  1. “最长递增子序列（LIS）”——状态 `dp[i]` 表示以 `i` 结尾的最长递增子序列长度。  
  2. “最长相同字符差 1 的子序列”——类似本题，只是条件换成字符差值为 1。  
  3. “带限制的最长路径”——在 DAG（有向无环图）上做 DP，限制条件可以是颜色、权值等。  
- **一句话总结解题钥匙**：  
  > **把“以当前元素结尾的最优解”保存下来，遍历所有可能的前驱，只要满足约束，就把前驱的最优值 + 1 作为当前的候选答案。**  

---

## 反思  

- **第一反应**：看到“子序列”“相邻下标要满足条件”，立刻想到“最长递增子序列”这种经典 DP，尝试把题目改写成“以 i 结尾的最长合法子序列”。  
- **最容易踩的坑**  
  1. **Hamming 距离计算**忘记提前退出，导致 O(L) 乘以 O(n²) 仍能接受，但在更大数据时会拖慢。  
  2. **组号相等的情况**忘记排除，导致错误的序列被计入。  
  3. **单词长度不同**的情况也必须排除，否则 Hamming 距离函数会直接返回 `False`，但在 DP 中仍会浪费一次不必要的检查。  
  4. **回溯时忘记把前驱设为 -1**，导致无限循环。  
- **下次遇到同类题**：  
  1. 先**明确状态**（通常是“以 i 为结尾的最优子结构”）。  
  2. **列出转移条件**（本题的三条），把它们写成代码里的 `if`。  
  3. 用**前驱数组**保存路径，最后**逆向回溯**得到答案。  

这样一步步拆解，既能保证正确性，又能在 `O(n²)` 量级内跑完题目。祝你玩转 DP！