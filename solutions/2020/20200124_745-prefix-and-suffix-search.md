# #745. 前缀和后缀搜索 / Prefix and Suffix Search

> 难度：困难 · 标签：Array、Hash Table、String、Design、Trie · [LeetCode 链接](https://leetcode.com/problems/prefix-and-suffix-search/)

---

## 题目（英文原版）

**Description**

Design a special dictionary that searches the words in it by a prefix and a suffix.
Implement the WordFilter class:

**Examples**

**Example 1:**

```
Input
["WordFilter", "f"]
[[["apple"]], ["a", "e"]]
Output
[null, 0]
Explanation
WordFilter wordFilter = new WordFilter(["apple"]);
wordFilter.f("a", "e"); // return 0, because the word at index 0 has prefix = "a" and suffix = "e".
```

**Constraints**

- 1 <= words.length <= 104
- 1 <= words[i].length <= 7
- 1 <= pref.length, suff.length <= 7
- words[i], pref and suff consist of lowercase English letters only.
- At most 104 calls will be made to the function f.

---

## 题目（中文翻译）

设计一个特殊的字典，能够同时根据前缀（prefix）和后缀（suffix）来搜索其中的单词。  

实现 `WordFilter` 类，使其具备如下功能：

```text
WordFilter wordFilter = new WordFilter(words);
int index = wordFilter.f(pref, suff);
```

- `WordFilter(words)`：使用给定的单词列表 `words` 初始化字典。  
- `f(pref, suff)`：返回字典中 **同时** 以 `pref` 为前缀且以 `suff` 为后缀的单词的 **最大下标**（index）。如果不存在满足条件的单词，返回 `-1`。

---

## 示例

**示例 1**

```text
Input
["WordFilter", "f"]
[[["apple"]], ["a", "e"]]
Output
[null, 0]
Explanation
WordFilter wordFilter = new WordFilter(["apple"]);
wordFilter.f("a", "e"); // 返回 0，因为下标为 0 的单词 "apple" 的前缀是 "a"，后缀是 "e"。
```

---

## 约束条件

- `1 <= words.length <= 10^4`
- `1 <= words[i].length <= 7`
- `1 <= pref.length, suff.length <= 7`
- `words[i]、pref 和 suff` 只包含小写英文字母。
- 最多会调用函数 `f` `10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有单词都保存下来**，每次调用 `f(pref, suff)` 时，遍历整个单词列表，检查：

1. 该单词是否以 `pref` 为前缀（可以用 `str.startswith`）  
2. 该单词是否以 `suff` 为后缀（可以用 `str.endswith`）  

如果两者都满足，就把它的下标（题目称为 *weight*）记下来，最后返回最大的下标。  

- **用到的数据结构**：Python 的 `list`（保存原始单词）和 `int`（记录下标）。  
- **生活化类比**：把单词列表想象成一本通讯录，查询时就像把所有联系人逐个翻开，看看名字是否以“张”开头、是否以“伟”结尾——慢但最直观。  
- **为什么正确**：只要遍历了所有单词，就不可能漏掉满足条件的词，取最大下标自然满足题目要求。  

#### 代码（Python）

```python
class WordFilter:
    def __init__(self, words):
        """
        把单词原样保存，顺便记录它们的下标（weight）。
        """
        self.words = words          # List[str]，下标就是 weight

    def f(self, pref: str, suff: str) -> int:
        """
        暴力遍历所有单词，找出同时满足前缀和后缀的最大下标。
        """
        max_weight = -1             # 记录找到的最大下标，-1 表示没有符合的
        for i, w in enumerate(self.words):
            # 检查前缀
            if not w.startswith(pref):
                continue
            # 检查后缀
            if not w.endswith(suff):
                continue
            # 同时满足，两者取最大下标
            max_weight = i
        return max_weight
```

#### 复杂度  

- **时间复杂度**：`O(N * L)`  
  - `N` 是单词数量，`L` 是单词最长长度（≤7）。  
  - 直观解释：每次查询我们都要看 **所有** 单词（相当于把所有联系人都翻一遍），每个单词检查前缀/后缀的时间和它的长度成正比。  
- **空间复杂度**：`O(N * L)`（存储原始单词）  
  - 只用了一个列表保存所有单词，和输入规模是一样的。  

> 暴力解虽然实现简单，但在最坏情况下（`N = 10⁴`、查询次数也达 `10⁴`）会导致约 `10⁸` 次字符比较，明显超时。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于**每次查询都要遍历所有单词**。我们希望把“前缀 + 后缀”这两个条件**提前合并**，在查询时只需要一次查找。  
下面一步步推导出一种高效的做法——**把所有可能的 “后缀{前缀” 组合存进一棵 Trie（字典树）**，查询时只需在 Trie 中走一次路径。

1. **把后缀和前缀拼在一起**  
   - 取单词 `apple`，所有可能的后缀有 `""、e、le、ple、pple、apple`（包括空串）。  
   - 把每个后缀与完整单词（即前缀）用一个特殊字符 `'{`' 拼接，得到  
     ```
     "{apple", "e{apple", "le{apple", "ple{apple", "pple{apple", "apple{apple"
     ```
   - 这里的 `'{`' 选自 ASCII，恰好在 `'z'` 之后，保证它不会和普通字母冲突。

2. **把这些拼接串插入 Trie**  
   - Trie 的每个节点保存 **当前走到的字符对应的最大下标**（即 weight）。  
   - 插入时如果走到已有节点，只需要把节点的 `weight` 更新为更大的下标即可。  
   - 这样，查询某个组合时，走到的最后一个节点的 `weight` 就是满足条件的最大下标。

3. **查询**  
   - 给定 `pref` 与 `suff`，我们只要在 Trie 中查找 `suff + '{' + pref`。  
   - 若路径完整存在，最后节点的 `weight` 就是答案；否则返回 `-1`（表示没有单词同时满足前缀和后缀）。

4. **为什么快**  
   - **构造阶段**一次性把所有可能的组合都写进 Trie，时间代价是 `O(N * L²)`（因为每个单词会产生 `L+1` 个后缀，每个后缀长度最多 `L`），但这只在初始化时执行一次。  
   - **查询阶段**只需要走 `len(suff) + len(pref) + 1 ≤ 2L+1` 步，时间是 `O(L)`，与单词数量无关。

5. **Trie 结构简述**  
   - 每个节点有 27 个子指针（26 个小写字母 + `'{'`），用列表 `children[27]` 存放。  
   - `weight` 保存走到该节点时出现的最大下标。  

#### 代码（Python）

```python
class TrieNode:
    __slots__ = ("children", "weight")
    def __init__(self):
        # 0-25 对应 'a'~'z'，26 对应特殊字符 '{'
        self.children = [None] * 27
        self.weight = -1          # 经过此节点的单词的最大下标

class WordFilter:
    def __init__(self, words):
        """
        构造函数：一次性把所有后缀+{+前缀的组合插入 Trie。
        """
        self.root = TrieNode()
        for weight, word in enumerate(words):
            # 为每个单词生成所有后缀（包括空串）
            long_word = word + '{' + word   # 为了后面统一插入，只需要一次循环
            # 这里我们实际上只需要插入 suffix+{+word，其中 suffix 取 word[ i: ]
            # 为了代码简洁，直接在循环里遍历所有 i
            for i in range(len(word) + 1):
                # suffix = word[i:]，拼接后得到 suffix + '{' + word
                cur = self.root
                # 先遍历 suffix
                for ch in word[i:]:
                    idx = ord(ch) - ord('a')
                    if cur.children[idx] is None:
                        cur.children[idx] = TrieNode()
                    cur = cur.children[idx]
                    cur.weight = weight          # 更新为当前更大的下标
                # 再遍历分隔符 '{'
                sep_idx = 26                     # '{' 的索引
                if cur.children[sep_idx] is None:
                    cur.children[sep_idx] = TrieNode()
                cur = cur.children[sep_idx]
                cur.weight = weight
                # 最后遍历完整的 word（作为前缀）
                for ch in word:
                    idx = ord(ch) - ord('a')
                    if cur.children[idx] is None:
                        cur.children[idx] = TrieNode()
                    cur = cur.children[idx]
                    cur.weight = weight          # 记录下标

    def f(self, pref: str, suff: str) -> int:
        """
        在 Trie 中查找 suffix + '{' + prefix。
        若路径不存在返回 -1。
        """
        cur = self.root
        # 先走后缀
        for ch in suff:
            idx = ord(ch) - ord('a')
            if cur.children[idx] is None:
                return -1
            cur = cur.children[idx]
        # 走分隔符 '{'
        sep_idx = 26
        if cur.children[sep_idx] is None:
            return -1
        cur = cur.children[sep_idx]
        # 再走前缀
        for ch in pref:
            idx = ord(ch) - ord('a')
            if cur.children[idx] is None:
                return -1
            cur = cur.children[idx]
        return cur.weight
```

> **代码说明**  
> - `TrieNode.__slots__` 只保留必要属性，能稍微节省内存。  
> - 插入时每经过一个节点都把 `weight` 更新为当前单词的下标，保证查询时得到的是**最大**下标。  
> - 查询过程严格按照 “后缀 → `{` → 前缀” 的顺序走，若中途找不到对应子节点直接返回 `-1`。

#### 复杂度  

- **构造时间复杂度**：`O(N * L²)`  
  - `N` 为单词数，`L` 为单词最大长度（≤7）。  
  - 每个单词会产生 `L+1` 个后缀，每个后缀最长 `L`，所以总字符插入次数约为 `N * (L+1) * (L+1) ≈ N * L²`。  
  - 对于本题的限制（`N ≤ 10⁴, L ≤ 7`），最多约 `5 * 10⁵` 次字符操作，完全可以接受。

- **查询时间复杂度**：`O(L)`  
  - 只需遍历 `len(suff) + len(pref) + 1 ≤ 2L+1` 个字符。  
  - 与单词数量无关，换句话说：**不管字典里有多少单词，查询都只花几步**。

- **空间复杂度**：`O(N * L²)`（Trie 的节点数）  
  - 每插入一次字符就会产生一个节点（如果之前不存在），最坏情况下节点数与插入的字符总数相同。  
  - 同样在本题的限制下，这个空间大小约几百 KB~几 MB，完全可行。

> 与暴力解相比，**查询从 `O(N·L)` 降到 `O(L)`**，在大量查询时优势非常明显。

---

## 心得

- **核心技巧**：把“前缀 + 后缀”合并为一个统一的搜索键，并使用 **Trie（字典树）** 记录每个键对应的最大下标。  
- **适用的题型**  
  1. 同时要求前缀和后缀匹配的搜索（本题）。  
  2. “单词搜索 II” 中需要快速判断一个字符串是否是若干单词的前缀或后缀。  
  3. “设计搜索自动补全” 类问题，需要在大量字符串中快速定位满足特定模式的词。  
- **一句话总结**：把后缀放在前面、用一个不冲突的分隔符拼在一起，再用 Trie 记住最大下标，就能实现 **O(长度) 的查询**。

---

## 反思

- **第一反应**：直接遍历所有单词检查前后缀，代码最容易写。  
- **最容易踩的坑**  
  - 忘记把空后缀 `""` 也加入 Trie，导致查询 `pref` 而 `suff` 为 `""` 时返回 `-1`。  
  - 选的分隔符与字母表冲突（如使用 `z`），会把合法的组合错误地合并。  
  - 在插入时没有把 `weight` 更新为 **最大** 下标，导致返回的不是要求的最大索引。  
- **下次类似题的第一步**：先思考**能否把多重条件合并成单一键**（比如前缀+后缀、左侧/右侧约束），再找适合的 **字典树 / 哈希表** 结构一次性存储所有键值对。这样可以把查询从线性降低到常数/对数级。