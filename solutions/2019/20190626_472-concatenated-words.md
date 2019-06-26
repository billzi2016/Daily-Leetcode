# #472. 拼接词 / Concatenated Words

> 难度：困难 · 标签：Array、String、Dynamic Programming、Depth-First Search、Trie、Sorting · [LeetCode 链接](https://leetcode.com/problems/concatenated-words/)

---

## 题目（英文原版）

**Description**

Given an array of strings words (without duplicates), return all the concatenated words in the given list of words.
A concatenated word is defined as a string that is comprised entirely of at least two shorter words (not necessarily distinct) in the given array.

**Examples**

**Example 1:**

```
Input: words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]
Output: ["catsdogcats","dogcatsdog","ratcatdogcat"]
Explanation: "catsdogcats" can be concatenated by "cats", "dog" and "cats"; 
"dogcatsdog" can be concatenated by "dog", "cats" and "dog"; 
"ratcatdogcat" can be concatenated by "rat", "cat", "dog" and "cat".
```

**Example 2:**

```
Input: words = ["cat","dog","catdog"]
Output: ["catdog"]
```

**Constraints**

- 1 <= words.length <= 104
- 1 <= words[i].length <= 30
- words[i] consists of only lowercase English letters.
- All the strings of words are unique.
- 1 <= sum(words[i].length) <= 105

---

## 题目（中文翻译）

给定一个字符串数组 **words**（无重复），返回列表中所有 **拼接词（concatenated word）**。  
**拼接词** 被定义为：一个完全由 **至少两个较短的单词（shorter words）**（这些单词可以相同，也可以不同）在 **数组（array）** `words` 中拼接而成的字符串。

**示例 1**  

**示例 2**  

**约束条件**

- $1 \leq \text{words.length} \leq 10^4$
- $1 \leq \text{words}[i].\text{length} \leq 30$
- `words[i]` 只包含小写英文字母。
- `words` 中的所有字符串互不相同。
- $1 \leq \sum \text{words}[i].\text{length} \leq 10^5$

**示例**

**示例 1**  
**Input:** `words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]`  
**Output:** `["catsdogcats","dogcatsdog","ratcatdogcat"]`  
**Explanation:**  
- `"catsdogcats"` 可以由 `"cats"`、`"dog"` 和 `"cats"` 拼接得到；  
- `"dogcatsdog"` 可以由 `"dog"`、`"cats"` 和 `"dog"` 拼接得到；  
- `"ratcatdogcat"` 可以由 `"rat"`、`"cat"`、`"dog"` 和 `"cat"` 拼接得到。

**示例 2**  
**Input:** `words = ["cat","dog","catdog"]`  
**Output:** `["catdog"]`  
**Explanation:** `"catdog"` 可以由 `"cat"` 和 `"dog"` 拼接得到。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个单词拆成所有可能的两段**，然后检查左段和右段是否都已经出现在数组里。如果右段本身还能再拆，就继续往下拆，直到所有子段都是数组中的原始单词。  

- **使用的数据结构**  
  - `set`（哈希表）来存放原始单词，查找一个单词是否出现过的时间复杂度是 **O(1)**，就像查字典一样，`key` 是单词本身，`value` 可以随便（这里我们只关心是否在字典里）。  
  - 递归函数 `can_form(word)`：尝试把 `word` 按所有可能的切分点拆成两段 `prefix` + `suffix`，如果 `prefix` 在集合里且 `suffix` 也是原始单词 **或** 能递归拆分成若干原始单词，则 `word` 是“拼接词”。  

- **为什么这个方法正确**  
  - 我们穷举了 **所有** 切分方式（从第 1 个字符到倒数第 1 个字符），只要有一种切分能让每段都是数组里的单词，就说明该单词满足“由至少两个更短的单词拼接而成”。  
  - 递归保证了 **多段** 的情况（比如 `catsdogcats` 需要三段）也能被检测到。

- **时间/空间复杂度（大白话解释）**  
  - 对于长度为 `L` 的单词，切分点有 `L-1` 种可能。每一种切分都要检查左段是否在集合里（O(1)），右段要么直接在集合里，要么再递归检查。最坏情况下会把右段再次切成 `L-2` 种可能……于是时间复杂度接近 **指数级**，记作 `O(2^L)`。  
  - 空间主要是递归栈的深度，最深也不会超过 `L`，即 **O(L)**。

> 暴力解在 `L ≤ 30`、`words 数量 ≤ 10⁴` 的情况下会超时，但它帮助我们理解“到底要检查哪些切分”。

#### 代码（Python）

```python
from typing import List

def findAllConcatenatedWordsInADict_bruteforce(words: List[str]) -> List[str]:
    word_set = set(words)                     # 哈希表：快速判断一个单词是否出现过
    memo = {}                                 # 记忆化：防止同一个子串被重复计算

    # 递归检查 word 能否由集合中的其他单词拼接而成
    def can_form(word: str) -> bool:
        if word in memo:                      # 已经算过了，直接返回
            return memo[word]

        # 尝试所有切分点
        for i in range(1, len(word)):
            prefix, suffix = word[:i], word[i:]

            # 左段必须已经在集合里（原始单词），右段要么在集合，要么还能继续拆分
            if prefix in word_set and (suffix in word_set or can_form(suffix)):
                memo[word] = True
                return True

        memo[word] = False
        return False

    res = []
    for w in words:
        # 为了防止“自身”被算作拼接词，先把它从集合里移除，检查完再放回去
        word_set.remove(w)
        if can_form(w):
            res.append(w)
        word_set.add(w)                       # 还原集合，供后面的单词使用

    return res
```

#### 复杂度

- **时间复杂度**：`O(2^L)`（指数级）——因为对每个单词会尝试所有切分方式，并且每次切分后还可能递归检查右段，最坏情况会呈指数增长。  
- **空间复杂度**：`O(L)`——递归栈的最大深度不超过单词长度 `L`，再加上哈希表 `word_set`（存放所有单词）和 `memo`（最多记忆每个子串一次），总体仍是线性空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“重复检查相同子串”**。例如 `catsdogcats` 中的子串 `cats`、`dog` 会被检查很多次。我们可以通过 **动态规划（DP）** 或 **Trie** 来把这些重复工作消掉。

下面介绍两种思路，任选其一即可：

1. **按长度排序 + DP + 哈希表**  
   - 把所有单词按长度从短到长排序。这样在判断一个单词是否是拼接词时，**只需要利用已经处理好的更短单词**（它们已经在哈希表里），而不必再去用自身或更长的单词。  
   - 对每个单词 `w`，建立一个长度为 `len(w)+1` 的布尔数组 `dp`，`dp[i]` 表示 `w[:i]`（前 i 个字符）能否被拆成若干已有单词。  
   - 初始 `dp[0] = True`（空串自然可以被拆）。遍历 `i` 从 0 到 `len(w)-1`，如果 `dp[i]` 为真，就尝试所有可能的右端 `j`（`i < j ≤ len(w)`），如果 `w[i:j]` 在哈希表里，就把 `dp[j]` 设为真。  
   - 当遍历结束后，若 `dp[len(w)]` 为真且拆分次数 ≥ 2（即使用了至少两个子单词），则 `w` 是拼接词。  
   - 关键点是：**每个单词只遍历一次**，每次内部的子串查找都是 O(1)（哈希表），整体时间是 `O( Σ L_i^2 )`，其中 `L_i` 是第 i 个单词的长度。由于每个单词最长 30，`L_i^2 ≤ 900`，对 10⁴ 个单词来说完全可以接受。

2. **Trie（字典树） + DFS**（进阶）  
   - 把所有单词插入 Trie，Trie 的每条边代表一个字符，节点上标记是否为单词结尾。  
   - 对每个单词进行深度优先搜索，尝试在 Trie 中匹配前缀；每当匹配到一个完整单词时，就递归检查剩余后缀是否还能在 Trie 中匹配。  
   - 为避免把自身当作拼接词，需要在搜索时暂时把当前单词从 Trie 中“隐藏”。  
   - 这种做法的时间复杂度同样是 `O( Σ L_i^2 )`，但在字符匹配上更高效（因为一次遍历就能判断多个子串是否存在），适合字符集大、单词长度更长的场景。

下面给出 **第一种**（排序 + DP） 的完整实现，代码最简洁，易于理解。

#### 代码（Python）

```python
from typing import List

def findAllConcatenatedWordsInADict(words: List[str]) -> List[str]:
    # 1️⃣ 先把单词按照长度从短到长排序
    words.sort(key=len)

    word_set = set()               # 已经处理好的单词集合，供后面的 DP 使用
    res = []                       # 最终答案

    for w in words:
        if not w:                  # 空字符串直接跳过（题目保证不存在，但防御性写法）
            continue

        # 2️⃣ 动态规划判断 w 是否可以由 word_set 中的单词拼接而成
        n = len(w)
        dp = [False] * (n + 1)
        dp[0] = True                # 空串可以被拆

        # i 表示已经成功拆到的位置
        for i in range(n):
            if not dp[i]:
                continue          # 只有 dp[i] 为真时才有意义继续向后扩展

            # 从 i 开始尝试所有可能的右端 j
            for j in range(i + 1, n + 1):
                if w[i:j] in word_set:   # 子串在已有集合里，说明可以拆到这里
                    dp[j] = True
            # 早停：如果已经能完整拆到结尾，就不必继续遍历
            if dp[n]:
                break

        # 3️⃣ 判断：dp[n] 为真且拆分用了至少两个单词
        #    （因为 word_set 里只放了更短的单词，若只用一个单词就等价于自身，故不计入）
        if dp[n]:
            res.append(w)

        # 4️⃣ 把当前单词加入集合，供后面的更长单词使用
        word_set.add(w)

    return res
```

**代码要点解释（中文注释已在代码中）**：

- **排序**：保证在检查 `w` 时，`word_set` 只包含比 `w` 短的单词，避免“自身”被误用。  
- **dp 数组**：`dp[i] = True` 表示前 `i` 个字符已经可以被拆成已有单词。  
- **双层循环**：外层遍历起点 `i`，内层尝试所有可能的终点 `j`，相当于“从左到右”地检查所有子串是否在集合里。  
- **早停**：一旦 `dp[n]` 为真（整个单词已经可以拆完），就可以提前结束内层循环，提升常数因素。  
- **加入集合**：处理完当前单词后，才把它放进 `word_set`，这样后面的更长单词才能利用它。

#### 复杂度

- **时间复杂度**：`O( Σ L_i^2 )`，其中 `L_i` 为第 `i` 个单词的长度。  
  - 对每个单词我们最多检查 `L_i` 个起点，每个起点再检查至多 `L_i` 个终点，查找子串是否在集合里是 O(1)。  
  - 由于 `L_i ≤ 30`，最坏情况约为 `10⁴ * 30² = 9·10⁶` 次操作，完全在 1 秒左右可以完成。  
  - 与暴力解的指数级 `O(2^L)` 相比，**每个单词只遍历一次**，效率提升了数个数量级。

- **空间复杂度**：`O( Σ L_i )`（存放所有单词的集合）+ `O(L_max)`（每个单词的 DP 数组），整体是线性空间。  
  - `L_max` 为最长单词的长度（≤30），可以忽略不计。

---

## 心得

- **核心技巧**：把“拼接词”问题转化为 **“能否用已有单词完全覆盖字符串”**，利用 **动态规划 + 哈希表**（或 Trie）来消除重复子问题。  
- **适用的题型**  
  1. **单词拆分（Word Break）**：判断一个字符串是否能由字典中的若干单词组成。  
  2. **最长单词链（Longest String Chain）**：判断是否可以通过添加一个字符得到下一个单词，同样使用 DP + 哈希表。  
  3. **字典树前缀匹配**：如 “搜索建议系统”（Search Suggestions System）等需要快速前缀查询的场景。  
- **一句话总结解题钥匙**：**先把短的单词当作“砖块”，再用 DP 检查长单词能否完整铺满**。

---

## 反思

- **第一反应**：看到“由多个更短单词拼接而成”，马上想到递归穷举所有切分点。  
- **最容易踩的坑**  
  - **把自身当作拼接块**：如果在检查单词时直接把它放进集合，`word` 本身会被误判为拼接词。解决办法是先把当前单词移除（或在 DP 中只使用更短的单词）。  
  - **边界条件**：空字符串、长度为 1 的单词、以及只出现一次的单词都需要正确处理。  
  - **重复计算**：没有记忆化或 DP 会导致指数级爆炸。  
- **下次遇到同类题**，第一步应想到：**“先把子问题（更短的单词）解决好，利用它们的结果来判断更大的问题”。** 这通常意味着 **排序 + DP / Trie** 的组合。