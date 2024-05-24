# #2707. 字符串中的额外字符 / Extra Characters in a String

> 难度：中等 · 标签：Array、Hash Table、String、Dynamic Programming、Trie · [LeetCode 链接](https://leetcode.com/problems/extra-characters-in-a-string/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s and a dictionary of words dictionary. You have to break s into one or more non-overlapping substrings such that each substring is present in dictionary. There may be some extra characters in s which are not present in any of the substrings.
Return the minimum number of extra characters left over if you break up s optimally.

**Examples**

**Example 1:**

```
Input: s = "leetscode", dictionary = ["leet","code","leetcode"]
Output: 1
Explanation: We can break s in two substrings: "leet" from index 0 to 3 and "code" from index 5 to 8. There is only 1 unused character (at index 4), so we return 1.
```

**Example 2:**

```
Input: s = "sayhelloworld", dictionary = ["hello","world"]
Output: 3
Explanation: We can break s in two substrings: "hello" from index 3 to 7 and "world" from index 8 to 12. The characters at indices 0, 1, 2 are not used in any substring and thus are considered as extra characters. Hence, we return 3.
```

**Constraints**

- 1 <= s.length <= 50
- 1 <= dictionary.length <= 50
- 1 <= dictionary[i].length <= 50
- dictionary[i] and s consists of only lowercase English letters
- dictionary contains distinct words

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的字符串 `s` 和一个单词字典 `dictionary`。你需要将 `s` 拆分成一个或多个**不重叠的子字符串**（substring），使得每个子字符串都在 `dictionary` 中。`s` 中可能会有一些字符不属于任何子字符串，这些字符被视为**额外字符**（extra characters）。  
返回在最优拆分下，剩余的最少额外字符数。

**示例 1**  
输入: `s = "leetscode", dictionary = ["leet","code","leetcode"]`  
输出: `1`  
解释: 我们可以将 `s` 拆分为两个子字符串："leet"（下标 0~3）和 "code"（下标 5~8）。仅有 1 个未使用的字符（下标 4），因此返回 1。

**示例 2**  
输入: `s = "sayhelloworld", dictionary = ["hello","world"]`  
输出: `3`  
解释: 我们可以将 `s` 拆分为两个子字符串："hello"（下标 3~7）和 "world"（下标 8~12）。下标 0、1、2 的字符未被任何子字符串使用，算作额外字符，所以返回 3。

**约束条件**  
- `1 <= s.length <= 50`  
- `1 <= dictionary.length <= 50`  
- `1 <= dictionary[i].length <= 50`  
- `dictionary[i]` 和 `s` 仅由小写英文字母组成  
- `dictionary` 中的单词互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串 `s` 的每一个位置都当作「可能的切分点」，尝试所有切分方式，然后统计每种切法下没有匹配到字典里单词的字符数，取最小值。

- **数据结构**：  
  - `dictionary` 用 **集合（set）** 存放，类似于查字典时的「词→页码」映射，判断一个子串是否在字典里，只需要 O(1) 的时间。  
  - 递归/回溯用 **列表** 记录当前已经切好的子串。

- **为什么正确**：  
  对每一种切分方式（包括不切的情况），我们都能完整地遍历整条字符串，并且把所有出现的子串和字典逐一比较。如果子串在字典里就算「匹配成功」，否则这些字符就算「额外字符」。遍历完所有可能的切分后，最小的额外字符数必然就是答案。

- **复杂度分析**：  
  - 对长度为 `n` 的字符串，切分点有 `n-1` 个，每个点可以「切」也可以「不切」，所以总共有 `2^(n-1)` 种切法。  
  - 对每一种切法，我们需要检查每个子串是否在字典里，最坏情况是 O(n)（因为子串总长度不超过 `n`），所以整体时间是 **O( n * 2^(n) )**，这在 `n ≤ 50` 时根本不可接受。  
  - 递归栈深度最多 `n`，额外使用的集合、列表等都只存放常数级别的数据，空间是 **O(n)**。

#### 代码（Python）

```python
from typing import List, Set

def min_extra_char_bruteforce(s: str, dictionary: List[str]) -> int:
    word_set: Set[str] = set(dictionary)          # 哈希表：查词快

    n = len(s)
    best = n                                      # 先把答案设为最坏情况（全部是额外字符）

    def dfs(idx: int, extra: int) -> None:
        """从位置 idx 开始继续切分，extra 为当前累计的额外字符数"""
        nonlocal best
        # 剪枝：已经比当前最优更差，就不用继续下去了
        if extra >= best:
            return
        # 已经遍历完全部字符，更新答案
        if idx == n:
            best = min(best, extra)
            return

        # 方案 1：把 s[idx] 当作额外字符直接跳过
        dfs(idx + 1, extra + 1)

        # 方案 2：尝试所有以 idx 为左端点的子串，看能否匹配字典
        for end in range(idx + 1, n + 1):        # end 为子串的右端点（不含）
            sub = s[idx:end]
            if sub in word_set:                  # 哈希表查询 O(1)
                dfs(end, extra)                  # 匹配成功，不增加额外字符

    dfs(0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：`O(n * 2^n)`  
  解释：对每个字符都有「切」或「不切」两种选择，导致指数级的状态数；每条路径最多遍历 `n` 个字符。
- **空间复杂度**：`O(n)`  
  解释：递归栈深度至多 `n`，其余使用的集合、字符串等都是常数级别。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于「枚举所有切分」——状态爆炸。我们需要把「从左到右遍历」的过程记住，避免重复计算。**动态规划（DP）** 正好可以做到这点。

1. **定义状态**  
   `dp[i]` 表示处理到字符下标 `i-1`（即前 `i` 个字符）时，能够得到的最少额外字符数。  
   - `dp[0] = 0`：空字符串不需要任何额外字符。  
   - 目标是求 `dp[n]`（`n = len(s)`）。

2. **状态转移**  
   对每个位置 `i`（从 1 到 n），我们有两种选择：  
   - **不匹配**：把第 `i-1` 个字符当作额外字符，`dp[i] = dp[i-1] + 1`。  
   - **匹配字典中的单词**：如果存在某个单词 `w` 长度为 `len_w`，且恰好等于 `s[i-len_w : i]`，则可以把这段直接「吃掉」，不产生额外字符，`dp[i] = min(dp[i], dp[i-len_w])`。  
   为了快速判断子串是否在字典里，我们仍然使用 **集合**（哈希表），时间是 O(1)。遍历所有单词的长度最多 `50`，所以每个 `i` 的转移复杂度是 `O(|dictionary| * max_word_len)`，在本题约为 `2500`，完全可以接受。

3. **进一步优化——Trie（字典树）**  
   当字典很大、单词长度各不相同时，遍历所有单词会有点浪费。我们可以把所有单词建成 **Trie**，从当前位置往后逐字符向下走 Trie，只要路径仍然存在，就说明有可能匹配到某个单词；每当走到一个「单词结尾」节点时，就得到一个合法的匹配。这样每个起点的搜索最多遍历 `max_word_len` 个字符，总体仍是 `O(n * max_word_len)`，但不必遍历整个字典。

4. **算法流程**（这里采用集合实现，思路更直观；随后给出 Trie 版）  
   - 初始化 `dp[0] = 0`，其余为正无穷。  
   - 对 `i` 从 `1` 到 `n`：  
        1. 默认 `dp[i] = dp[i-1] + 1`（把当前字符当作额外字符）。  
        2. 对字典中每个单词 `w`：如果 `i >= len(w)` 且 `s[i-len(w):i] == w`，则 `dp[i] = min(dp[i], dp[i-len(w)])`。  
   - 最终返回 `dp[n]`。

5. **核心概念解释**  
   - **动态规划**：把大问题拆成「前缀」子问题，记住每一步的最优解，后面的决策只需要查表，不必重新计算。  
   - **Trie（字典树）**：一种树形结构，每层对应一个字符，从根到某个节点的路径拼起来就是字典里某个前缀。查询是否是字典单词，只需沿路径走，时间与单词长度成正比。

#### 代码（Python）

> **实现 1：使用集合（更易懂）**
```python
from typing import List, Set

def min_extra_char_dp(s: str, dictionary: List[str]) -> int:
    word_set: Set[str] = set(dictionary)          # O(1) 判词
    n = len(s)
    INF = n + 1                                    # 一个足够大的数

    dp = [INF] * (n + 1)
    dp[0] = 0                                      # 空前缀

    for i in range(1, n + 1):
        # 方案1：把 s[i-1] 当作额外字符
        dp[i] = dp[i - 1] + 1

        # 方案2：尝试所有可能的单词匹配
        for w in word_set:
            lw = len(w)
            if i >= lw and s[i - lw:i] == w:      # 子串相等则匹配成功
                dp[i] = min(dp[i], dp[i - lw])    # 不产生额外字符

    return dp[n]
```

> **实现 2：使用 Trie（进阶）**
```python
from typing import List, Dict

class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_word: bool = False               # 是否恰好是字典中的完整单词

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True

def min_extra_char_trie(s: str, dictionary: List[str]) -> int:
    trie = Trie()
    for w in dictionary:
        trie.insert(w)

    n = len(s)
    INF = n + 1
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        # 方案1：把当前字符当作额外字符
        dp[i] = dp[i - 1] + 1

        # 方案2：从 i 开始向后尝试匹配字典中的单词（其实是从 i-1 往左走）
        node = trie.root
        # 这里从 i-1 向左最多检查 max_word_len 步
        for j in range(i - 1, -1, -1):
            ch = s[j]
            if ch not in node.children:
                break                     # 已经找不到更长的匹配了
            node = node.children[ch]
            if node.is_word:
                dp[i] = min(dp[i], dp[j])   # 匹配到一个单词，前缀到 j 已经处理好
    return dp[n]
```

#### 复杂度

- **时间复杂度（集合版）**：`O(n * m * L)`  
  - `n` 为字符串长度（≤50），  
  - `m` 为字典单词数（≤50），  
  - `L` 为单词最大长度（≤50）。  
  实际上我们在每个 `i` 只遍历字典一次，子串比较最多 `L` 次，所以整体约 `O(n * m * L)`，在题目限制下几千次操作，毫秒级完成。

- **空间复杂度（集合版）**：`O(n)`  
  - `dp` 数组长度为 `n+1`，其余只存放哈希集合（大小 ≤ 50），属于常数级空间。

- **时间复杂度（Trie 版）**：`O(n * L)`  
  - 对每个起点 `i`，最多沿 Trie 向左走 `L` 步（最长单词长度），因此比遍历整个字典更快，尤其当 `m` 很大时优势明显。

- **空间复杂度（Trie 版）**：`O(total_characters_in_dictionary)`  
  - Trie 的节点数等于所有单词字符总和，最多 `m * L ≤ 2500`，同样很小。

---

## 心得

- **核心技巧**：利用「前缀 DP」把“把字符串切成若干合法子串”转化为“在每个位置只关注之前的最优解”。  
- **适用题型**：  
  1. **单词拆分**（Word Break）——判断是否可以完全由字典单词组成。  
  2. **最少分割次数**（Minimum Cuts for Palindrome Partitioning）——在每个位置决定是否切割。  
  3. **删除最少字符使字符串可由字典拼成**（本题的变体）。  
- **一句话总结解题钥匙**：**把全局最优拆分拆成「左边已处理好」+「右边尝试匹配」的递推关系，用 DP 表记住左边的最小额外字符数**。

---

## 反思

- **第一反应**：看到“把字符串分成若干子串，每个子串必须在字典里”，立刻想到“回溯/暴力枚举所有切法”。这自然会产生指数级的时间。
- **最容易踩的坑**  
  1. **边界条件**：`dp[0]` 必须初始化为 0，表示空前缀不需要额外字符。  
  2. **子串匹配时的下标**：`s[i-len(w):i]` 要确保 `i >= len(w)`，否则会出现负索引导致错误匹配。  
  3. **重复计算**：在暴力解里会对同一前缀多次递归，导致超时；DP 正是为了解决这类「子问题重复」的情况。  
- **下次遇到同类题**：第一步先 **写出 DP 状态定义**（比如 `dp[i]` 表示前 `i` 个字符的最优值），再思考**状态转移**——是「不使用当前字符」还是「使用一个满足条件的单词」——最后决定是否需要额外的数据结构（如 Trie）来加速匹配。