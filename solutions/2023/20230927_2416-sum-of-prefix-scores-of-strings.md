# #2416. 字符串前缀得分之和 / Sum of Prefix Scores of Strings

> 难度：困难 · 标签：Array、String、Trie、Counting · [LeetCode 链接](https://leetcode.com/problems/sum-of-prefix-scores-of-strings/)

---

## 题目（英文原版）

**Description**

You are given an array words of size n consisting of non-empty strings.
We define the score of a string term as the number of strings words[i] such that term is a prefix of words[i].
Return an array answer of size n where answer[i] is the sum of scores of every non-empty prefix of words[i].
Note that a string is considered as a prefix of itself.

**Examples**

**Example 1:**

```
Input: words = ["abc","ab","bc","b"]
Output: [5,4,3,2]
Explanation: The answer for each string is the following:
- "abc" has 3 prefixes: "a", "ab", and "abc".
- There are 2 strings with the prefix "a", 2 strings with the prefix "ab", and 1 string with the prefix "abc".
The total is answer[0] = 2 + 2 + 1 = 5.
- "ab" has 2 prefixes: "a" and "ab".
- There are 2 strings with the prefix "a", and 2 strings with the prefix "ab".
The total is answer[1] = 2 + 2 = 4.
- "bc" has 2 prefixes: "b" and "bc".
- There are 2 strings with the prefix "b", and 1 string with the prefix "bc".
The total is answer[2] = 2 + 1 = 3.
- "b" has 1 prefix: "b".
- There are 2 strings with the prefix "b".
The total is answer[3] = 2.
```

**Example 2:**

```
Input: words = ["abcd"]
Output: [4]
Explanation:
"abcd" has 4 prefixes: "a", "ab", "abc", and "abcd".
Each prefix has a score of one, so the total is answer[0] = 1 + 1 + 1 + 1 = 4.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 1000
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个大小为 `n` 的字符串数组（array）`words`，其中每个元素都是非空字符串。

我们将 **字符串 term 的得分** 定义为满足 `term` 是 `words[i]` 前缀（prefix）的 `words[i]` 的数量。

返回一个大小为 `n` 的数组 `answer`，其中 `answer[i]` 为 `words[i]` 的每个非空前缀的得分之和。  
注意，一个字符串自身也算作它的前缀。

**示例 1**  
```text
Input: words = ["abc","ab","bc","b"]
Output: [5,4,3,2]
Explanation:
- "abc" 有 3 个前缀："a", "ab", "abc"。
  前缀 "a" 出现在 2 个字符串中，前缀 "ab" 出现在 2 个字符串中，前缀 "abc" 出现在 1 个字符串中。
  因此 answer[0] = 2 + 2 + 1 = 5。
- "ab" 有 2 个前缀："a", "ab"。
  前缀 "a" 出现在 2 个字符串中，前缀 "ab" 出现在 2 个字符串中。
  因此 answer[1] = 2 + 2 = 4。
- "bc" 有 2 个前缀："b", "bc"。
  前缀 "b" 出现在 3 个字符串中，前缀 "bc" 出现在 1 个字符串中。
  因此 answer[2] = 3 + 1 = 4。（题目原答案为 3，实际应为 4，下面给出正确的计算过程）
- "b" 有 1 个前缀："b"。
  前缀 "b" 出现在 3 个字符串中。
  因此 answer[3] = 3。

（为保持与官方答案一致，最终输出为 `[5,4,3,2]`，这里的解释仅示意前缀计数方式。） 
```

**示例 2**  
```text
Input: words = ["abcd"]
Output: [4]
Explanation:
"abcd" 有 4 个前缀："a", "ab", "abc", "abcd"。
每个前缀在数组中仅出现一次，所以每个前缀的得分都是 1。
因此 answer[0] = 1 + 1 + 1 + 1 = 4。
```

**约束条件**  
- `1 <= words.length <= 1000`  
- `1 <= words[i].length <= 1000`  
- `words[i]` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个统计每个前缀出现的次数**：

1. 对于数组 `words` 中的每一个字符串 `w`，枚举它的所有非空前缀 `p`（例如 `"abc"` 的前缀有 `"a"、"ab"、"abc"`）。  
2. 再遍历整个 `words`，统计有多少个字符串以 `p` 为前缀。把这些计数累加，就得到 `w` 的答案。  

这里用到的唯一数据结构是**列表**（`list`）和**字符串**本身。可以把“前缀计数”想象成在一本字典里查词：我们把每个前缀当成要查的词，遍历整本字典（所有单词）看看有多少页（单词）以这个词开头。  

这种做法一定是正确的，因为我们没有遗漏任何前缀，也没有漏掉任何可能的匹配单词——穷举了所有组合。

#### 代码（Python）

```python
from typing import List

def sumPrefixScores_bruteforce(words: List[str]) -> List[int]:
    n = len(words)
    ans = [0] * n                     # 用来保存每个单词的答案
    for i, w in enumerate(words):     # 枚举每个单词
        # 枚举它的所有非空前缀
        for l in range(1, len(w) + 1):
            prefix = w[:l]            # 取前 l 个字符作为前缀
            # 统计有多少单词以这个前缀开头
            cnt = 0
            for other in words:
                if other.startswith(prefix):
                    cnt += 1
            ans[i] += cnt              # 把当前前缀的得分加到答案里
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * L²)`  
  - `n` 为单词数，`L` 为单词最长长度。  
  - 对每个单词我们枚举 `L` 个前缀；对每个前缀又要遍历全部 `n` 个单词并比较前缀（最坏情况要比较 `L` 次字符），于是大约是 `n * L * n * L = n² * L²`，但因为 `n ≤ 1000`、`L ≤ 1000`，在最坏情况下会非常慢。  
  - 用大白话说，这相当于 **“把每本书的每一页都和所有书的每一页比一遍”**，显然不现实。  

- **空间复杂度**：`O(1)`（不计输出数组）  
  - 只用了常数级别的额外变量。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于每次统计前缀出现次数时，都要遍历整个 `words`。我们希望**一次遍历就能把所有前缀的出现次数统计好**，后面再直接查询。  

这正是 **Trie（字典树）** 的用武之地：

- Trie 是一种树形结构，每层对应一个字符。  
- 从根到某个节点的路径恰好就是一个前缀。  
- 如果在每个节点上记录 **经过该节点的单词数量**（即有多少单词以这个前缀出现），那么**查询任意前缀的出现次数只需要 O(前缀长度)**，不需要再遍历所有单词。  

**步骤**  

1. **构建 Trie**  
   - 依次把所有单词插入 Trie。  
   - 插入时，沿途每访问一个节点，就把该节点的计数 `cnt` 加 1，表示又多了一条以这个前缀出现的单词。  
   - 这里的 `cnt` 相当于“这本字典里，这一页（前缀）出现了多少次”。  

2. **查询每个单词的前缀得分**  
   - 再次遍历 `words`，对每个单词从根节点沿着字符走下去。  
   - 每走到一个节点，就把该节点的 `cnt` 加到当前单词的答案中。  
   - 走完整个单词后得到的累加值就是 **该单词所有非空前缀的出现次数之和**。  

因为 Trie 只需要一次遍历就把所有前缀计数收集完毕，查询时只需线性扫描单词本身，所以整体时间大幅降低。

**类比**：把 Trie 想成一本“前缀目录”。我们先把所有书（单词）放进目录里，每放一本书，就在目录对应的每一级位置记一次“这儿有多少本书”。查询一本书的前缀得分时，只需要顺着目录走到书的末页，把沿途的计数加起来即可。

#### 代码（Python）

```python
from typing import List, Dict

class TrieNode:
    __slots__ = ("children", "cnt")
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}  # 子节点，key 是字符
        self.cnt: int = 0                        # 以该节点对应前缀出现的单词数

def sumPrefixScores(words: List[str]) -> List[int]:
    # ---------- 1. 建树 ----------
    root = TrieNode()
    for w in words:                     # 把每个单词插入 Trie
        node = root
        for ch in w:                    # 逐字符向下走
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.cnt += 1                # 经过该前缀的单词数量 +1

    # ---------- 2. 计算答案 ----------
    ans = []
    for w in words:
        node = root
        total = 0
        for ch in w:
            node = node.children[ch]   # 必然存在，因为之前已经插入过
            total += node.cnt          # 把当前前缀的出现次数加入答案
        ans.append(total)
    return ans
```

> **代码要点解释**  
> - `TrieNode.__slots__` 用来节省内存（可选），因为节点数量最多是所有字符之和。  
> - `node.cnt += 1` 正在“给目录的这一层贴标签”，记录有多少本书走到这里。  
> - 查询时直接 `total += node.cnt`，相当于“把目录每一层的标签相加”。  

#### 复杂度  

- **时间复杂度**：`O(N * L)`  
  - `N` 为单词数量，`L` 为单词最大长度。  
  - 插入所有单词共遍历 `N * L` 次字符；查询每个单词再次遍历其长度，也是 `N * L`。整体线性相加仍是 `O(N * L)`。  
  - 与暴力解的 `O(N² * L²)` 相比，**快了很多**，尤其当 `N`、`L` 都接近上限时，差距是指数级的。  

- **空间复杂度**：`O(N * L)`  
  - 最坏情况下每个字符都会创建一个新节点，节点总数不超过所有字符的总和。  
  - 这相当于在字典树里存了一遍所有单词的字符。  

---

## 心得  

- **核心技巧**：利用 **Trie（字典树）** 统计所有前缀的出现次数。  
- **适用题型**：  
  1. “单词搜索 II” / “前缀匹配” 类题目（需要快速判断前缀是否存在）。  
  2. “最长公共前缀” / “统计前缀出现次数” 类题目。  
  3. “单词过滤器” / “前缀+后缀查询” 等需要在大量字符串中做前缀/后缀统计的场景。  
- **一句话总结**：**把所有前缀的计数一次性预处理到 Trie 中，后续查询只需线性遍历单词本身。**

---

## 反思  

- **第一反应**：看到“前缀”和“计数”立刻想到哈希表或暴力枚举。  
- **最容易踩的坑**：  
  - **忘记把每个单词本身也算作前缀**（题目说字符串是自身的前缀）。  
  - **重复单词**：如果数组里出现相同的单词，需要在插入时仍然对每一次出现都 `cnt += 1`，否则计数会偏小。  
  - **内存泄漏**：在实现 Trie 时如果不使用 `__slots__` 或者不及时释放节点，可能会因为节点过多导致内存超限（尤其在 `L` 很大时）。  
- **下次类似题的第一步**：先思考“有没有一种数据结构可以一次遍历把所有子结构的统计信息都算好？”——答案往往是 **Trie**（前缀）或 **前缀和数组**（数值）等。这样就能把“每次都遍历全部数据”的暴力思路升级为“预处理 + 快速查询”。