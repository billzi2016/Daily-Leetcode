# #820. 单词的最短编码 / Short Encoding of Words

> 难度：中等 · 标签：Array、Hash Table、String、Trie · [LeetCode 链接](https://leetcode.com/problems/short-encoding-of-words/)

---

## 题目（英文原版）

**Description**

A valid encoding of an array of words is any reference string s and array of indices indices such that:
Given an array of words, return the length of the shortest reference string s possible of any valid encoding of words.

**Examples**

**Example 1:**

```
Input: words = ["time", "me", "bell"]
Output: 10
Explanation: A valid encoding would be s = "time#bell#" and indices = [0, 2, 5].
words[0] = "time", the substring of s starting from indices[0] = 0 to the next '#' is underlined in "time#bell#"
words[1] = "me", the substring of s starting from indices[1] = 2 to the next '#' is underlined in "time#bell#"
words[2] = "bell", the substring of s starting from indices[2] = 5 to the next '#' is underlined in "time#bell#"
```

**Example 2:**

```
Input: words = ["t"]
Output: 2
Explanation: A valid encoding would be s = "t#" and indices = [0].
```

**Constraints**

- 1 <= words.length <= 2000
- 1 <= words[i].length <= 7
- words[i] consists of only lowercase letters.

---

## 题目（中文翻译）

给定一个单词数组 `words`，**有效编码**（valid encoding）指的是任意的参考字符串 `s` 与索引数组 `indices`，满足：

- `s` 是由若干单词加上分隔符 `'#'` 组成的字符串；
- 对于每个单词 `words[i]`，`indices[i]` 指向 `s` 中该单词出现的起始位置，且该单词在 `s` 中以 `'#'` 为结束标记。

返回所有可能的有效编码中，参考字符串 `s` 的最小可能长度。

## 示例

### 示例 1

**输入**  
`words = ["time", "me", "bell"]`

**输出**  
`10`

**解释**  
一种可行的编码方式是 `s = "time#bell#"`，`indices = [0, 2, 5]`。  

- `words[0] = "time"`：`s` 中从 `indices[0] = 0` 开始到下一个 `'#'` 的子串为 **time**。  
- `words[1] = "me"`：`s` 中从 `indices[1] = 2` 开始到下一个 `'#'` 的子串为 **me**。  
- `words[2] = "bell"`：`s` 中从 `indices[2] = 5` 开始到下一个 `'#'` 的子串为 **bell**。

### 示例 2

**输入**  
`words = ["t"]`

**输出**  
`2`

**解释**  
一种可行的编码方式是 `s = "t#"`，`indices = [0]`。

## 约束条件

- `1 <= words.length <= 2000`
- `1 <= words[i].length <= 7`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**只要一个单词不是别的单词的后缀，就必须完整地出现在编码串 `s` 中**，否则它可以被别的单词“盖住”。  

- **后缀**：如果把单词 `me` 看成 `time` 的尾巴，那么在 `time#` 里已经包含了 `me`，我们就不必再把 `me#` 再写一次。  
- **数据结构**：这里只需要 **数组** 和 **字符串**，不需要高级结构。我们把每个单词两两比较，判断它是否是另一单词的后缀。可以把“查后缀”想象成在一本书里找某段文字的结尾，若能在更长的段落里完整出现，就不必单独记下来。

**为什么正确**  
如果一个单词 `w` 是别的单词 `v` 的后缀，那么在编码 `v#` 时，`w` 已经出现在 `v#` 的最后几位，读取从 `w` 开始到下一个 `#` 的子串正好得到 `w`。于是 `w` 不需要额外占用空间。只有那些**不被任何其他单词覆盖的单词**才必须各自占用 `len(word)+1`（加上结尾的 `#`）的长度。把所有必须出现的单词长度相加，就是最短可能的编码长度。

**复杂度分析（大白话）**  
- 我们要把每个单词和其他所有单词比较一次，最坏情况是 `n`（单词数）乘以 `n-1`，即 **O(n²)** 次比较。每次比较要检查后缀关系，最长单词只有 7 个字符，所以这一步可以看作常数时间。  
- 额外的空间只用了几个临时变量和一个保存结果的整数，**O(1)**（常数）空间。

#### 代码（Python）

```python
from typing import List

def minimumLengthEncoding_bruteforce(words: List[str]) -> int:
    # 先去重，避免相同单词多次计数
    uniq = list(set(words))
    n = len(uniq)
    # 用一个布尔数组标记哪些单词是“被覆盖的后缀”
    is_suffix = [False] * n

    # 两层循环：把每个单词和其他所有单词比较
    for i in range(n):
        if is_suffix[i]:
            continue          # 已经知道是后缀就可以跳过
        for j in range(n):
            if i == j:
                continue
            # 如果 uniq[i] 是 uniq[j] 的后缀，则标记为 True
            if uniq[j].endswith(uniq[i]):   # endswith 就是“是否是后缀”
                is_suffix[i] = True
                break

    # 累加所有不是后缀的单词长度，加上每个单词后面的 '#'
    ans = 0
    for i in range(n):
        if not is_suffix[i]:
            ans += len(uniq[i]) + 1   # +1 为结尾的 '#'
    return ans
```

#### 复杂度

- **时间复杂度**：**O(n²)**  
  解释：如果有 2000 个单词，最坏要比较约 4 百万 次（2000×2000），这在电脑里仍然能跑完，但并不是最省时的做法。
- **空间复杂度**：**O(1)**（不计输入数组）  
  只用了常数个额外变量和一个布尔数组（长度为 `n`，相对于 `n` 本身已经算在输入里）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键是快速判断一个单词是否是其他单词的后缀**。如果我们把所有单词 **倒着写**（例如 `"time"` → `"emit"`），后缀关系就变成了 **前缀关系**：  
- `me` 是 `time` 的后缀 ⇔ `em` 是 `emit` 的前缀。

于是我们可以把所有 **倒序单词** 放进一棵 **Trie（前缀树）**。Trie 的特点是：

- 每个节点代表一个字符的集合，沿着从根到叶子的路径恰好对应一个单词的前缀（这里是倒序后的前缀）。
- **叶子节点**（没有子节点的节点）对应的单词 **没有任何更长的单词以它为前缀**，也就是说在原始方向上，它 **不是任何其他单词的后缀**，必须单独计入编码长度。

步骤如下：

1. **去重**：相同的单词只需要出现一次。  
2. **倒序插入**：把每个单词倒过来，逐字符插入 Trie。插入时记录最后一个字符所在的节点（即对应原单词的根节点）。  
3. 插入完毕后，遍历所有记录的节点：  
   - 若该节点 **没有子节点**（即是叶子），说明这个单词在原始方向上不是别的单词的后缀，需要 `len(word) + 1` 的空间。  
   - 若有子节点，则已经被更长单词覆盖，可以省略。  
4. 把所有必须计入的长度相加，即得到最短编码的长度。

**为什么 Trie 更快**  
- 插入每个单词只需要遍历它的字符（最长 7），所以总时间是 **O(N·L)**，其中 `N` 为单词数，`L` 为单词最大长度（这里是常数 7）。  
- 与暴力解的 **O(N²)** 比，省去了两两比较的成本。  

**类比**：把 Trie 想象成一本“倒写的字典”。我们把所有倒写的单词放进去，如果一个单词的路径一直走不到其他单词的分叉点（没有子节点），说明它是“独立的词根”，必须单独记下来。

#### 代码（Python）

```python
from typing import List

class TrieNode:
    __slots__ = ('children',)   # 只保留 children，节省内存
    def __init__(self):
        self.children = {}       # key: 字符，value: TrieNode

def minimumLengthEncoding(words: List[str]) -> int:
    # 1️⃣ 去重
    uniq = set(words)

    # 2️⃣ 建立 Trie（倒序插入）
    root = TrieNode()
    # 用来记录每个单词对应的“入口节点”
    nodes = {}

    for w in uniq:
        cur = root
        # 从后往前遍历字符
        for ch in reversed(w):
            if ch not in cur.children:
                cur.children[ch] = TrieNode()
            cur = cur.children[ch]
        # 记录下这个单词结束时所在的节点
        nodes[w] = cur

    # 3️⃣ 统计叶子节点对应的单词长度
    ans = 0
    for w, node in nodes.items():
        if not node.children:          # 没有子节点 → 叶子
            ans += len(w) + 1          # +1 为结尾的 '#'
    return ans
```

#### 复杂度

- **时间复杂度**：**O(N·L)**  
  解释：`N` 最多 2000，`L` ≤ 7，实际上最多只需要遍历 14000 次字符，几乎是瞬间完成。相比暴力的 O(N²)（约 4 百万 次比较），速度提升显著。  
- **空间复杂度**：**O(N·L)**  
  Trie 中最多会有 `N·L` 个节点（每个字符一个节点），这在本题的约束下也非常小。额外的哈希表 `nodes` 只保存 `N` 条记录。

---

## 心得

- **核心技巧**：利用 **后缀 → 前缀** 的转换，把“是否被包含”问题转化为 **Trie 叶子节点** 的判定。  
- **适用的题型**  
  1. **最短编码**（本题）  
  2. **单词集合的唯一前缀**（如 LeetCode 14）  
  3. **字符串集合的最大独立子集**（比如“删除所有后缀”类题目）  
- **一句话总结解题钥匙**：  
  “把所有单词倒着放进前缀树，只有没有子节点的单词才必须占位”。

---

## 反思

- **第一反应**：看到“后缀”“编码”，立刻想到“把短的单词去掉，只保留不被包含的”。  
- **最容易踩的坑**  
  - 忘记 **去重**：相同单词出现多次会导致错误的计数。  
  - 误把 “前缀” 当成 “后缀” 直接比较，导致遗漏倒序的必要步骤。  
  - 在 Trie 实现时，忘记检查 **子节点是否为空**，而是错误地检查父节点。  
- **下次遇到同类题**：第一步先 **倒序**（或反向）思考，把“是否是后缀”转化为 “是否是前缀”，然后考虑 **Trie** 或 **哈希集合** 来快速判定。