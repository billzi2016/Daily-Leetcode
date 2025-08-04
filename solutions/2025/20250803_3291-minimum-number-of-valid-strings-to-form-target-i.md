# #3291. 形成目标字符串的最少有效字符串数量 I / Minimum Number of Valid Strings to Form Target I

> 难度：中等 · 标签：Array、String、Binary Search、Dynamic Programming、Trie、Segment Tree、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-i/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words and a string target.
A string x is called valid if x is a prefix of any string in words.
Return the minimum number of valid strings that can be concatenated to form target. If it is not possible to form target, return -1.

**Examples**

**Example 1:**

```
Input: words = ["abc","aaaaa","bcdef"], target = "aabcdabc"
Output: 3
Explanation:
The target string can be formed by concatenating:
```

**Example 2:**

```
Input: words = ["abababab","ab"], target = "ababaababa"
Output: 2
Explanation:
The target string can be formed by concatenating:
```

**Example 3:**

```
Input: words = ["abcdef"], target = "xyz"
Output: -1
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 5 * 103
- The input is generated such that sum(words[i].length) <= 105.
- words[i] consists only of lowercase English letters.
- 1 <= target.length <= 5 * 103
- target consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**

给定一个字符串数组 `words` 和一个字符串 `target`。  
如果一个字符串 `x` 是 `words` 中任意字符串的前缀（prefix），则称 `x` 为**有效字符串**（valid string）。  

返回能够拼接（concatenate）成 `target` 的最少有效字符串数量。如果无法拼成 `target`，返回 `-1`。

**示例**

> 示例 1  
> 输入: `words = ["abc","aaaaa","bcdef"]`, `target = "aabcdabc"`  
> 输出: `3`  
> 解释:  
> 可以通过以下有效字符串的拼接得到 `target`：  

> 示例 2  
> 输入: `words = ["abababab","ab"]`, `target = "ababaababa"`  
> 输出: `2`  
> 解释:  
> 可以通过以下有效字符串的拼接得到 `target`：  

> 示例 3  
> 输入: `words = ["abcdef"]`, `target = "xyz"`  
> 输出: `-1`

**约束条件**

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 5 * 10^3`
- 输入保证 `∑ words[i].length <= 10^5`
- `words[i]` 仅由小写英文字母组成
- `1 <= target.length <= 5 * 10^3`
- `target` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从目标字符串 `target` 的开头往后尝试**，每一次都枚举所有可能的「合法前缀」——即 `words` 中任意单词的前缀——看能否匹配 `target` 的当前位置。  

- **数据结构**：我们只需要普通的 Python `list` 与 `str`，不需要额外的结构。可以把 `words` 看成一本「词典」，每本词典里有很多「单词」；我们每次都把「单词」的每个前缀（比如 `"abc"` 的前缀有 `"a"`、`"ab"`、`"abc"`）当作一张「卡片」去和 `target` 对比。  
- **正确性**：如果我们把 `target` 拆成若干段，每段恰好是某个单词的前缀，那么这若干段的数量就是一种可行的「拼接方案」。暴力枚举所有可能的段落并记录最少段数，必然能找到全局最优（因为我们把所有可能都尝试了）。  
- **时间/空间复杂度**：  
  - 设 `n = len(target)`，`m = len(words)`，`L = max(len(w) for w in words)`。  
  - 对每个起始位置 `i`（最多 `n` 个），我们会遍历所有单词（`m`）并检查它的每个前缀（最多 `L`），于是最坏情况下的时间是 `O(n * m * L)`，这在数据规模 (`n ≤ 5·10³，L ≤ 5·10³，m ≤ 100`) 下可能达到 **几千万次**，在 Python 中会超时。  
  - 只用到常数级额外空间（记录答案的 `dp` 数组），所以空间是 `O(n)`。

#### 代码（Python）

```python
def min_valid_strings_bruteforce(words, target):
    n = len(target)
    INF = float('inf')
    # dp[i] 表示组成 target[:i]（前 i 个字符）所需的最少合法字符串数量
    dp = [INF] * (n + 1)
    dp[0] = 0                     # 空串需要 0 个

    for i in range(n):            # 从左到右枚举起点
        if dp[i] == INF:          # 当前前缀不可达，直接跳过
            continue
        # 枚举所有单词的所有前缀
        for w in words:
            # 前缀最长只能到 target 的结尾
            max_len = min(len(w), n - i)
            for l in range(1, max_len + 1):
                # 检查 target[i:i+l] 是否等于 w[:l]
                if target[i:i + l] == w[:l]:
                    # 成功匹配一个合法前缀，更新 dp
                    dp[i + l] = min(dp[i + l], dp[i] + 1)

    return -1 if dp[n] == INF else dp[n]
```

> **关键行中文注释**  
> - `dp[i]` 保存前 i 个字符的最小拼接数。  
> - 双层循环 `for w in words`、`for l in range(1, max_len+1)` 实现「枚举所有合法前缀」。  
> - `target[i:i+l] == w[:l]` 就是把「卡片」贴到「目标」上看能否吻合。  

#### 复杂度  

- **时间复杂度**：`O(n * m * L)`  
  - `n`：目标长度。  
  - `m`：单词数量。  
  - `L`：最长单词长度。  
  - 大白话：如果目标是 5000 字，单词有 100 个，每个单词 5000 长，最坏要检查 5000 × 100 × 5000 ≈ 2.5 × 10⁹ 次，显然太慢。  

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n+1` 的 DP 数组来记状态。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**大量重复的前缀匹配**。我们每次都要把 `target[i:i+l]` 与每个单词的前缀逐字符比较，导致 `O(m·L)` 的额外工作。  
要优化，就需要一种 **一次性把所有合法前缀组织起来**、能够在 **O(1)~O(log Σ)** 的时间内判断「从位置 i 开始，最长可以匹配多少字符」的结构。  

**Trie（字典树）** 正好满足这个需求。  

- **Trie 结构**：把所有单词的每个前缀插入同一棵树。每条边代表一个字符，沿着根到某个节点的路径恰好对应一个前缀。插入过程类似把「所有卡片」按字符顺序排成一条长队，公共的前缀会共享同一段路径。  
- **查询过程**：从目标字符串的某个位置 `i` 开始，沿着 Trie 的边向下走，只要字符匹配就继续；一旦走不通，就说明再往后已经不可能匹配任何合法前缀了。遍历的字符数恰好是 **从 i 开始的最长匹配长度**。  

结合 **动态规划**：  

- `dp[i]` 仍然表示组成 `target[:i]` 所需的最少合法字符串数量。  
- 对每个可达的 `i`（`dp[i] != INF`），我们在 Trie 中从 `target[i]` 开始向后遍历，得到所有可以匹配的前缀长度 `len`，并把 `dp[i+len]` 更新为 `min(dp[i+len], dp[i] + 1)`。  

这样每个字符在 **所有起始位置的遍历总和** 只会被访问一次（因为每次遍历都沿着 Trie 向右走，最多走到目标结尾），总时间变为 `O(n * α)`，其中 `α` 是 Trie 中每条边的平均访问次数，等价于 **`O(n + total_len_of_words)`**。  

**步骤概览**  

1. **构建 Trie**  
   - 把 `words` 中的每个单词的每个字符依次插入。  
   - 不需要额外标记「单词结束」的状态，只要路径存在即代表一个合法前缀。  

2. **DP + Trie 匹配**  
   - 初始化 `dp[0] = 0`，其余为 `INF`。  
   - 对 `i` 从 `0` 到 `n-1`：  
     - 若 `dp[i]` 为 `INF`，说明前缀不可达，直接跳过。  
     - 否则，从 Trie 根开始，用指针 `node` 依次读取 `target[i], target[i+1], …`：  
       - 若当前字符不存在对应的子节点，停止遍历（再往后不可能匹配）。  
       - 否则移动到子节点，记下匹配长度 `len = j - i + 1`，更新 `dp[i+len] = min(dp[i+len], dp[i] + 1)`。  

3. **答案**  
   - 若 `dp[n]` 仍为 `INF`，返回 `-1`；否则返回 `dp[n]`。  

**类比**：把 Trie 想成一本「前缀字典」，我们把目标字符串从左到右「扫进」这本字典，每读到一个字符，就在字典里往下翻一页。如果翻不到，就说明已经没有任何前缀能继续匹配，只能停下来换一张新卡片（即计数加一，重新开始）。  

#### 代码（Python）

```python
from collections import defaultdict
from math import inf

class TrieNode:
    """Trie 的节点，只需要记录子节点即可"""
    __slots__ = ('children',)
    def __init__(self):
        self.children = dict()          # char -> TrieNode

def build_trie(words):
    """把所有单词的所有前缀插入同一棵 Trie"""
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:                    # 逐字符插入
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]   # 前缀对应的路径
    return root

def min_valid_strings(words, target):
    n = len(target)
    root = build_trie(words)

    dp = [inf] * (n + 1)
    dp[0] = 0                           # 空串需要 0 个合法子串

    for i in range(n):
        if dp[i] == inf:                # 前缀不可达，直接跳过
            continue
        node = root
        # 从位置 i 开始，沿着 Trie 向右匹配
        for j in range(i, n):
            ch = target[j]
            if ch not in node.children: # 再往后已经没有合法前缀
                break
            node = node.children[ch]    # 前缀长度 = j - i + 1
            # 更新到达位置 j+1 的最小计数
            if dp[j + 1] > dp[i] + 1:
                dp[j + 1] = dp[i] + 1

    return -1 if dp[n] == inf else dp[n]
```

> **代码要点**  
> - `TrieNode` 只保存子节点字典，省去不必要的 `is_end` 标记，因为**任何路径都是合法前缀**。  
> - `build_trie` 把所有单词一次性写进树里，时间是所有字符总数 `Σ|words[i]|`。  
> - 主循环里 `for j in range(i, n):` 每次都尝试把当前「卡片」往右延伸，遇到不存在的字符就停下来——这正是 Trie 的“快速失配”特性。  

#### 复杂度  

- **时间复杂度**：`O(n + Σ|words[i]|)`  
  - 构建 Trie：遍历所有单词的字符一次 → `Σ|words[i]|`（ ≤ 10⁵）。  
  - DP 遍历：每个目标字符最多被「向右」扫描一次，因为一旦某个起点 `i` 的匹配在位置 `j` 失配，后续更大的 `i` 不会再次走到同一条已经失配的边。整体线性于 `n`（ ≤ 5·10³）。  
  - 大白话：即使目标长度是 5000，单词总长度是 100 000，整个算法最多只跑 105 + 5000 ≈ 1.05 × 10⁵ 步，跑得非常快。  

- **空间复杂度**：`O(Σ|words[i]| + n)`  
  - Trie 占用所有字符的节点数（每个字符一个节点），即 `Σ|words[i]|`。  
  - DP 数组额外 `O(n)`。  
  - 对比暴力解的 `O(n)`，这里多了 Trie 的存储，但在题目限制下仍然是可接受的（≈ 10⁵ 个节点）。  

---

## 心得  

- **核心技巧**：使用 **Trie** 统一管理所有合法前缀，再配合 **动态规划** 计算最少段数。  
- **适用的题型**（类似思路）  
  1. *Word Break* 系列题目：判断或计数把字符串拆成字典单词的方式。  
  2. *Maximum Length of Concatenated String with Unique Characters*（需要快速前缀查询）。  
  3. *Minimum Number of Taps to Open to Water a Garden*（使用区间 DP + 前缀信息的变体）。  
- **一句话总结**：**把所有可能的“卡片”一次性装进字典树，用 DP 把目标从左到右“贴”上去，最少卡片数自然出现。**  

---

## 反思  

- **第一反应**：看到“前缀”“拼接”“最少数量”，立刻想到「动态规划」+「前缀匹配」的组合。  
- **最容易踩的坑**  
  - **前缀的定义**：不是整词，只要是任意单词的前缀都算合法，容易误以为只能使用完整单词。  
  - **重复计数**：在 DP 更新时必须使用 `min(dp[next], dp[i] + 1)`，否则可能把同一个位置的计数写大。  
  - **Trie 的构造**：忘记把每个单词的所有前缀都插入，导致部分合法前缀查不到。  
  - **边界条件**：`dp[0] = 0` 必须初始化；当目标字符串完全匹配不到时要返回 `-1`，而不是 `inf`。  
- **下次类似题的第一步**：先把「所有合法片段」用合适的数据结构（Trie、哈希集合、前缀数组等）一次性准备好，再设计 DP/贪心/双指针等主流程。这样可以把「大量重复匹配」的开销降到线性。