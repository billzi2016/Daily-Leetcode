# #1032. 字符流 / Stream of Characters

> 难度：困难 · 标签：Array、String、Design、Trie、Data Stream · [LeetCode 链接](https://leetcode.com/problems/stream-of-characters/)

---

## 题目（英文原版）

**Description**

Design an algorithm that accepts a stream of characters and checks if a suffix of these characters is a string of a given array of strings words.
For example, if words = ["abc", "xyz"] and the stream added the four characters (one by one) 'a', 'x', 'y', and 'z', your algorithm should detect that the suffix "xyz" of the characters "axyz" matches "xyz" from words.
Implement the StreamChecker class:

**Examples**

**Example 1:**

```
Input
["StreamChecker", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query"]
[[["cd", "f", "kl"]], ["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"], ["h"], ["i"], ["j"], ["k"], ["l"]]
Output
[null, false, false, false, true, false, true, false, false, false, false, false, true]

Explanation
StreamChecker streamChecker = new StreamChecker(["cd", "f", "kl"]);
streamChecker.query("a"); // return False
streamChecker.query("b"); // return False
streamChecker.query("c"); // return False
streamChecker.query("d"); // return True, because 'cd' is in the wordlist
streamChecker.query("e"); // return False
streamChecker.query("f"); // return True, because 'f' is in the wordlist
streamChecker.query("g"); // return False
streamChecker.query("h"); // return False
streamChecker.query("i"); // return False
streamChecker.query("j"); // return False
streamChecker.query("k"); // return False
streamChecker.query("l"); // return True, because 'kl' is in the wordlist
```

**Constraints**

- 1 <= words.length <= 2000
- 1 <= words[i].length <= 200
- words[i] consists of lowercase English letters.
- letter is a lowercase English letter.
- At most 4 * 104 calls will be made to query.

---

## 题目（中文翻译）

设计一种算法，接受一个字符流，并检查这些字符的某个后缀（suffix）是否匹配给定字符串数组（array of strings）`words` 中的某个单词。  
例如，若 `words = ["abc", "xyz"]`，而字符流依次加入四个字符 `'a'`、`'x'`、`'y'`、`'z'`，则你的算法应当检测到字符序列 `"axyz"` 的后缀 `"xyz"` 与 `words` 中的 `"xyz"` 匹配。

实现 `StreamChecker` 类：

```java
class StreamChecker {
    public StreamChecker(String[] words) { ... }
    public boolean query(char letter) { ... }
}
```

**示例 1**

```text
输入
["StreamChecker", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query", "query"]
[[["cd", "f", "kl"]], ["a"], ["b"], ["c"], ["d"], ["e"], ["f"], ["g"], ["h"], ["i"], ["j"], ["k"], ["l"]]

输出
[null, false, false, false, true, false, true, false, false, false, false, false, true]

解释
StreamChecker streamChecker = new StreamChecker(["cd", "f", "kl"]);
streamChecker.query("a"); // 返回 false
streamChecker.query("b"); // 返回 false
streamChecker.query("c"); // 返回 false
streamChecker.query("d"); // 返回 true，因为 "cd" 在单词表中
streamChecker.query("e"); // 返回 false
streamChecker.query("f"); // 返回 true，因为 "f" 在单词表中
streamChecker.query("g"); // 返回 false
streamChecker.query("h"); // 返回 false
streamChecker.query("i"); // 返回 false
streamChecker.query("j"); // 返回 false
streamChecker.query("k"); // 返回 false
streamChecker.query("l"); // 返回 true，因为 "kl" 在单词表中
```

**约束条件**

- `1 <= words.length <= 2000`
- `1 <= words[i].length <= 200`
- `words[i]` 只包含小写英文字母。
- `letter` 是小写英文字母。
- 最多会调用 `query` `4 * 10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有已经出现的字符拼成一个长字符串 `stream`，每次调用 `query(letter)` 时把新字符接在后面，然后遍历 **所有** 给定的单词 `words`，检查这些单词是否是 `stream` 的后缀。

- **数据结构**：我们只需要一个普通的 Python `list` 或 `str` 来保存已经收到的字符。可以把它想象成一本“流水账”，每次往后写一个字母。
- **正确性**：如果某个单词 `w` 正好出现在 `stream` 的末尾，那么 `stream[-len(w):] == w` 必然为真。遍历所有单词，只要出现一次相等就说明找到了匹配的后缀。
- **复杂度分析**  
  - 设 `n = len(words)`，`L = max(len(w) for w in words)`，`k` 为当前已经收到的字符数。  
  - 每次查询我们需要对每个单词做一次后缀比较，比较的长度最多是单词本身的长度 `len(w)`，所以最坏情况是 `O(L)`。整体时间是 `O(n * L)`。  
  - 空间只存储了 `stream` 本身，长度随查询次数增长，最坏是 `O(k)`。  

> **大白话**：如果把 `n` 看成“单词的数量”，`L` 看成“最长单词有多长”，那么时间复杂度 `O(n·L)` 就像“每次都要跑 `n` 条路，每条路的长度最多是 `L”，显然会很慢”。

#### 代码（Python）

```python
class StreamChecker:
    def __init__(self, words):
        """
        :type words: List[str]
        """
        self.words = words                # 保存所有单词
        self.stream = []                  # 用列表模拟字符串，方便追加字符

    def query(self, letter):
        """
        :type letter: str
        :rtype: bool
        """
        self.stream.append(letter)        # 把新字符加到流的末尾

        # 把列表转成字符串（实际可以不转，用切片比较也行，这里为直观）
        s = ''.join(self.stream)

        # 遍历所有单词，检查是否是后缀
        for w in self.words:
            if s.endswith(w):            # Python 自带的后缀检查
                return True
        return False
```

#### 复杂度

- **时间复杂度**：`O(n * L)`  
  - `n` 是单词数量，`L` 是最长单词长度。每次查询都要遍历所有单词并比较后缀。
- **空间复杂度**：`O(k)`  
  - `k` 为已经收到的字符总数，因为我们把所有字符都保留下来。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历全部单词**。我们可以把所有单词组织成一种“查找结构”，让查询只跟**最近的几个字符**有关，而不是跟全部单词数量挂钩。

**关键观察**  
- 我们只关心「后缀」是否匹配。把每个单词 **倒着写**（如 `"abc"` → `"cba"`），那么判断后缀就等价于判断「前缀」是否在这些倒序单词的集合中。

**核心数据结构：倒序 Trie（字典树）**  
- Trie 就像一本**字典**，每层对应一个字符。查单词时从根开始往下走。这里我们把所有单词倒过来插入 Trie，这样 **从最新字符往更早的字符遍历**，恰好对应「后缀」检查。  
- 类比：Trie 好比“查字典的目录”，`key` 是字母，`value` 是指向下一个字母的指针。我们只要沿着最新字符往回走，如果一路走到底有 `is_word=True`，就说明找到了匹配的后缀。

**查询过程**  
1. 把新字符加入一个**固定长度的环形缓冲区**（或 `deque`），只保留最近 `max_len`（所有单词的最长长度）个字符，防止无限增长。  
2. 从最新字符开始，在 Trie 中向下遍历。如果遍历途中某个节点标记了 `is_word=True`，立即返回 `True`。  
3. 如果遍历到某一步找不到对应的子节点，说明再往前也不可能匹配，直接返回 `False`。

**为什么快**  
- 每次查询最多只会走 `max_len` 步（最长单词的长度 ≤ 200），与单词数量无关。相当于把原来的 `n`（最多 2000）压缩到常数级别。  

**实现细节**  
- 用字典 `defaultdict(dict)` 存子节点，或自定义 `Node` 类。这里用简洁的嵌套字典实现。  
- 为了避免每次都遍历整个 `stream`，我们只保留最近的 `max_len` 个字符，用 `collections.deque(maxlen=…)` 自动弹出最旧的字符。

#### 代码（Python）

```python
from collections import deque, defaultdict

class TrieNode:
    __slots__ = ('children', 'is_word')
    def __init__(self):
        self.children = {}   # key: character, value: TrieNode
        self.is_word = False # 是否有单词在此终止

class StreamChecker:
    def __init__(self, words):
        """
        :type words: List[str]
        """
        # 1️⃣ 建立倒序 Trie
        self.root = TrieNode()
        self.max_len = 0                # 记录最长单词长度
        for w in words:
            self.max_len = max(self.max_len, len(w))
            node = self.root
            for ch in reversed(w):     # 倒着插入
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_word = True         # 标记单词结束

        # 2️⃣ 用固定长度的队列保存最近的字符
        self.buffer = deque(maxlen=self.max_len)  # 只保留 max_len 个字符

    def query(self, letter):
        """
        :type letter: str
        :rtype: bool
        """
        # 把新字符加入队首（左侧），deque 左侧是最近的字符
        self.buffer.appendleft(letter)

        node = self.root
        # 从最新字符开始，沿 Trie 向下走
        for ch in self.buffer:
            if ch not in node.children:
                # 没有对应的子节点，后面更早的字符也不可能匹配
                return False
            node = node.children[ch]
            if node.is_word:
                # 遇到一个单词结束点，说明后缀匹配成功
                return True
        return False
```

#### 复杂度

- **时间复杂度**：`O(L)`，其中 `L = max_len ≤ 200`。每次查询最多遍历 `L` 层 Trie，和单词数量 `n` 无关。  
  > 与暴力解相比，原本可能要检查上千个单词，现在只检查最多 200 步，快了几个数量级。
- **空间复杂度**：`O(T)`，`T` 为 Trie 中所有字符的总数。最坏情况下等于所有单词长度之和，`≤ 2000 * 200 = 400,000`，加上 `O(L)` 的缓冲区。  

---

## 心得

- **核心技巧**：把「后缀匹配」转化为「前缀匹配」→ 使用 **倒序 Trie**（或前缀树）实现高效查询。  
- **适用场景**  
  1. **字典搜索**：比如 LeetCode 648（Replace Words）需要在前缀树中查找最短前缀。  
  2. **实时流式模式匹配**：如 LeetCode 1032（Stream of Characters）本题，或需要在字符流中快速判断是否出现敏感词的系统。  
  3. **多模式匹配**：使用 **Aho‑Corasick** 自动机也基于 Trie，只是额外加了失配指针，适用于更复杂的多模式搜索。  
- **一句话总结**：把后缀问题倒着写，利用 Trie 把“遍历所有单词”压缩成“遍历固定长度字符”。

---

## 反思

- **第一反应**：直接把所有单词逐个比较，写出最朴素的实现。  
- **最容易踩的坑**  
  - **缓冲区无限增长**：如果不限制 `stream` 长度，内存会随查询次数线性增长，最终会 O(查询次数) 爆内存。  
  - **倒序插入忘记**：若忘记把单词倒着插入 Trie，查询时仍是前缀匹配，会导致错误结果。  
  - **字符类型**：题目保证全是小写字母，但若出现非字母，需要提前过滤或扩展 Trie 的字符集。  
- **下次遇到同类题**：第一步先问自己「我要匹配的是前缀还是后缀？」如果是后缀，立刻想到「倒序 Trie」或「Aho‑Corasick」来把搜索范围固定在最长单词长度内。