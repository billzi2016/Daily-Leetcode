# #676. 实现魔法字典 / Implement Magic Dictionary

> 难度：中等 · 标签：Hash Table、String、Depth-First Search、Design、Trie · [LeetCode 链接](https://leetcode.com/problems/implement-magic-dictionary/)

---

## 题目（英文原版）

**Description**

Design a data structure that is initialized with a list of different words. Provided a string, you should determine if you can change exactly one character in this string to match any word in the data structure.
Implement the MagicDictionary class:

**Examples**

**Example 1:**

```
Input
["MagicDictionary", "buildDict", "search", "search", "search", "search"]
[[], [["hello", "leetcode"]], ["hello"], ["hhllo"], ["hell"], ["leetcoded"]]
Output
[null, null, false, true, false, false]

Explanation
MagicDictionary magicDictionary = new MagicDictionary();
magicDictionary.buildDict(["hello", "leetcode"]);
magicDictionary.search("hello"); // return False
magicDictionary.search("hhllo"); // We can change the second 'h' to 'e' to match "hello" so we return True
magicDictionary.search("hell"); // return False
magicDictionary.search("leetcoded"); // return False
```

**Constraints**

- 1 <= dictionary.length <= 100
- 1 <= dictionary[i].length <= 100
- dictionary[i] consists of only lower-case English letters.
- All the strings in dictionary are distinct.
- 1 <= searchWord.length <= 100
- searchWord consists of only lower-case English letters.
- buildDict will be called only once before search.
- At most 100 calls will be made to search.

---

## 题目（中文翻译）

设计一个数据结构（data structure），在初始化时接受一个由不同单词组成的列表。给定一个字符串，需要判断是否能够恰好修改该字符串中的 **一个字符**，从而匹配数据结构中任意一个单词。

实现 `MagicDictionary` 类：

- `MagicDictionary()`：构造函数，初始化数据结构。  
- `void buildDict(String[] dictionary)`：使用给定的单词列表 `dictionary` 建立字典。  
- `boolean search(String searchWord)`：判断是否存在字典中的某个单词，只需把 `searchWord` 中的 **一个字符** 替换成其他字符即可得到该单词。

**示例 1**

```json
Input
["MagicDictionary", "buildDict", "search", "search", "search", "search"]
[[], [["hello", "leetcode"]], ["hello"], ["hhllo"], ["hell"], ["leetcoded"]]
Output
[null, null, false, true, false, false]
```

**解释**
```java
MagicDictionary magicDictionary = new MagicDictionary();
magicDictionary.buildDict(["hello", "leetcode"]);
magicDictionary.search("hello");      // 返回 false
magicDictionary.search("hhllo");      // 可以把第二个 'h' 改成 'e'，匹配 "hello"，返回 true
magicDictionary.search("hell");       // 返回 false
magicDictionary.search("leetcoded");  // 返回 false
```

**约束条件**

- `1 <= dictionary.length <= 100`
- `1 <= dictionary[i].length <= 100`
- `dictionary[i]` 只包含小写英文字母。
- `dictionary` 中的所有字符串互不相同。
- `1 <= searchWord.length <= 100`
- `searchWord` 只包含小写英文字母。
- `buildDict` 仅会在 `search` 之前调用一次。
- 最多会调用 `search` 100 次。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **字典里的每个单词** 都拿出来和 `searchWord` 逐字符比较：

1. 先判断两个单词的长度是否相同，长度不一样一定改不了成同一个单词。  
2. 再从左到右逐个字符对比，统计不同的字符个数。  
3. 如果遍历结束后恰好出现 **1** 个不同的字符，就说明只需要改掉这一个字符就能匹配上字典中的某个单词，返回 `True`。  
4. 把所有字典单词都检查完都没有找到符合条件的，就返回 `False`。

> **哈希表的类比**：这里我们没有用到哈希表，完全像是把字典里的每本书（单词）都翻开来看，逐页（字符）比对，最慢但最直观。  

这个方法之所以 **正确**，是因为题目只要求“恰好改掉一个字符”。只要我们把所有可能的字典单词都检查一遍，必然能找到（或找不到）满足条件的那一个。

**时间/空间复杂度**  
- **时间复杂度**：设字典里有 `n` 个单词，单词平均长度为 `L`，我们每次搜索都要遍历 `n` 个单词并对每个单词比较 `L` 次字符，整体是 `O(n·L)`。  
  - 大白话：如果字典里有 100 本书，每本书 100 页，最坏情况下我们要把 **100×100=10,000** 页都看一遍。  
- **空间复杂度**：只需要保存字典本身，额外的辅助空间是 `O(1)`（常数级），因为我们不创建额外的数组或哈希表。

#### 代码（Python）

```python
class MagicDictionary:
    def __init__(self):
        # 用列表保存所有单词，等价于把字典的每本书都放进书架
        self.words = []

    def buildDict(self, dictionary):
        """
        :type dictionary: List[str]
        :rtype: None
        """
        self.words = dictionary          # 直接存下来

    def search(self, searchWord):
        """
        :type searchWord: str
        :rtype: bool
        """
        for w in self.words:            # 逐个遍历字典里的单词
            if len(w) != len(searchWord):
                continue                # 长度不相等直接跳过
            diff = 0                    # 记录不同字符的个数
            for c1, c2 in zip(w, searchWord):
                if c1 != c2:
                    diff += 1
                    if diff > 1:       # 超过1个不同就没有必要继续比较
                        break
            if diff == 1:               # 正好一个字符不同，返回 True
                return True
        return False                    # 没有任何单词满足条件
```

#### 复杂度  

- **时间复杂度**：`O(n·L)` —— 需要把所有 `n` 本书（单词）都翻一遍，每本书看 `L` 页（字符）。  
- **空间复杂度**：`O(1)` 除了保存字典本身之外，不需要额外的空间。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于每次 `search` 都要遍历整个字典。  
如果我们在 **构建阶段** 把一些有用的信息提前算好，搜索时就能 **只看几条记录**，时间就会大幅下降。

这里有两种常见的优化思路：

1. **通配符哈希表**（本解法采用）。  
2. **Trie（字典树）+ 深度优先搜索**（另一种实现方式，稍后简要说明）。

下面重点讲 **通配符哈希表**，因为它概念最直观、代码最简洁，且对初学者友好。

---

#### 2.1 通配符哈希表的核心想法  

把每个字典单词的每一个位置都“用 `*` 替换”，得到 **通配形式**（generic form）。  
例如单词 `"hello"` 可以生成 5 种通配形式：

```
*ello, h*llo, he*lo, hel*o, hell*
```

把这些通配形式当作 **键**，把出现次数（或对应的原单词列表）当作 **值**，存进哈希表。

- **为什么这样可以判断只改一个字符？**  
  当我们搜索 `searchWord` 时，同样把它的每个位置替换成 `*`，得到同样数量的通配形式。  
  - 如果某个通配形式在哈希表中出现过，说明字典里 **恰好有一个单词** 与 `searchWord` 在除 `*` 位置外的所有字符都相同。  
  - 只要满足以下任意一种情况，就可以返回 `True`：  
    1. 哈希表中该通配形式对应的单词数 **≥ 2**（说明字典里有不同的单词和 `searchWord` 只差一个字符）。  
    2. 对应的单词数 **= 1** 且该单词 **不是** `searchWord` 本身（因为题目要求必须改掉一个字符，不能保持不变）。  

这样，**搜索的时间**只和单词长度 `L` 成正比：我们只需要遍历 `L` 个通配形式并在哈希表中查找，复杂度是 `O(L)`。

> **哈希表的类比**：把每本书的每一页都贴上一张“标签”（通配形式），同一标签的书放在同一个抽屉里。搜索时只需要看对应标签的抽屉，而不是把所有书都翻遍。

---

#### 2.2 代码实现（Python）

```python
from collections import defaultdict

class MagicDictionary:
    def __init__(self):
        # key: 通配形式（如 "*ello"），value: 出现次数或对应原单词集合
        self.pattern_map = defaultdict(set)   # 用 set 记录所有出现过的原单词

    def buildDict(self, dictionary):
        """
        :type dictionary: List[str]
        :rtype: None
        """
        for word in dictionary:
            for i in range(len(word)):
                # 把第 i 个字符换成 '*'
                pattern = word[:i] + '*' + word[i+1:]
                self.pattern_map[pattern].add(word)   # 把原单词放进对应的集合

    def search(self, searchWord):
        """
        :type searchWord: str
        :rtype: bool
        """
        for i in range(len(searchWord)):
            pattern = searchWord[:i] + '*' + searchWord[i+1:]
            if pattern not in self.pattern_map:
                continue                      # 这个通配形式根本不存在，直接跳过

            candidates = self.pattern_map[pattern]   # 可能的匹配单词集合
            # 情况1：集合里有不止一个单词（一定有一个不同于 searchWord）
            if len(candidates) > 1:
                return True
            # 情况2：集合里只有一个单词，但它不是 searchWord 本身
            if len(candidates) == 1 and (searchWord not in candidates):
                return True
        return False
```

> **代码要点注释**  
- `defaultdict(set)`：类似于一本“字典”，每个键自动对应一个空集合，省去判断键是否存在的代码。  
- `word[:i] + '*' + word[i+1:]`：把第 `i` 位字符换成 `*`，相当于在第 `i` 页贴上通配标签。  
- `candidates`：在同一抽屉（通配键）里的所有原单词。只要抽屉里有 **其他** 单词，就满足“改掉一个字符”。

---

#### 2.3 复杂度分析  

- **构建阶段**  
  - 时间：每个单词长度为 `L`，我们要生成 `L` 个通配形式，整个字典有 `n` 个单词，时间为 `O(n·L)`。  
  - 空间：哈希表中每个通配形式对应一个集合，最坏情况每个通配形式存一个单词，总共也会是 `O(n·L)`（因为每个单词产生 `L` 条记录）。  

- **搜索阶段**  
  - 时间：只遍历 `searchWord` 的 `L` 个位置并在哈希表中做 O(1) 查找，整体是 `O(L)`。  
    - 与暴力解 `O(n·L)` 对比，**省去了遍历字典**，在字典很大的时候优势明显。  
  - 空间：仅使用常数级额外空间 `O(1)`（只保存临时变量和一次查找到的集合引用）。  

---

#### 2.4 另一种思路：Trie + DFS（可选）

如果你想进一步练习 **Trie（字典树）**，可以把所有字典单词插入 Trie。搜索时用 **深度优先搜索**，在遍历字符时允许 **恰好一次** 的字符不匹配。  
- 构建 Trie：`O(n·L)` 时间、`O(n·L)` 空间。  
- 搜索：`O(26·L)`（每一步最多尝试 26 种字符的替换），在本题约等于 `O(L)`。  

Trie 的好处是可以在 **前缀相同** 的大量单词中进一步剪枝，但实现相对繁琐，初学者可以先掌握通配哈希表的方案。

---

## 心得  

- **核心技巧**：把“改掉恰好一个字符”的约束转化为“两个单词在除一个位置外其余字符全部相同”。  
- **适用的题型**  
  1. **单词搜索类**（如 *Implement a Magic Dictionary*、*Word Ladder* 的变体）。  
  2. **模糊匹配**（如 *Search Suggestions System*、*K-Edit Distance* 的简化版）。  
  3. **密码/拼写检查**（允许单字符错误的场景）。  
- **一句话总结解题钥匙**：**预处理所有“只缺一个字符”的通配形式，用哈希表一次查找即可判断是否只差一个字母**。

---

## 反思  

- **第一反应**：直接遍历字典、逐字符比较——最直观但效率低。  
- **最容易踩的坑**  
  - **长度不相等**：必须先排除，否则会误判。  
  - **搜索词本身已经在字典里**：题目要求“恰好改掉一个字符”，所以不能直接返回 `True`。  
  - **重复计数**：如果同一个通配形式对应多个相同单词（字典本身已保证唯一），需要用集合防止误判。  
- **下次类似题的第一步**：**把“只差一个字符”的条件抽象为“把每个位置都打上通配符”，看能否用哈希表或 Trie 进行快速匹配**。这样可以从一开始就避免遍历全部单词，思路更清晰。