# #3045. 前缀与后缀配对计数 II / Count Prefix and Suffix Pairs II

> 难度：困难 · 标签：Array、String、Trie、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/count-prefix-and-suffix-pairs-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string array words.
Let's define a boolean function isPrefixAndSuffix that takes two strings, str1 and str2:
For example, isPrefixAndSuffix("aba", "ababa") is true because "aba" is a prefix of "ababa" and also a suffix, but isPrefixAndSuffix("abc", "abcd") is false.
Return an integer denoting the number of index pairs (i, j) such that i < j, and isPrefixAndSuffix(words[i], words[j]) is true.

**Examples**

**Example 1:**

```
Input: words = ["a","aba","ababa","aa"]
Output: 4
Explanation: In this example, the counted index pairs are:
i = 0 and j = 1 because isPrefixAndSuffix("a", "aba") is true.
i = 0 and j = 2 because isPrefixAndSuffix("a", "ababa") is true.
i = 0 and j = 3 because isPrefixAndSuffix("a", "aa") is true.
i = 1 and j = 2 because isPrefixAndSuffix("aba", "ababa") is true.
Therefore, the answer is 4.
```

**Example 2:**

```
Input: words = ["pa","papa","ma","mama"]
Output: 2
Explanation: In this example, the counted index pairs are:
i = 0 and j = 1 because isPrefixAndSuffix("pa", "papa") is true.
i = 2 and j = 3 because isPrefixAndSuffix("ma", "mama") is true.
Therefore, the answer is 2.
```

**Example 3:**

```
Input: words = ["abab","ab"]
Output: 0
Explanation: In this example, the only valid index pair is i = 0 and j = 1, and isPrefixAndSuffix("abab", "ab") is false.
Therefore, the answer is 0.
```

**Constraints**

- 1 <= words.length <= 105
- 1 <= words[i].length <= 105
- words[i] consists only of lowercase English letters.
- The sum of the lengths of all words[i] does not exceed 5 * 105.

---

## 题目（中文翻译）

给定一个 **0 索引** 的字符串数组（string array）`words`。  
我们定义一个布尔函数（boolean function）`isPrefixAndSuffix(str1, str2)`，其功能如下：

- 当 `str1` 同时是 `str2` 的前缀（prefix）和后缀（suffix）时返回 `true`，否则返回 `false`。  

例如，`isPrefixAndSuffix("aba", "ababa")` 为 `true`，因为 `"aba"` 既是 `"ababa"` 的前缀也是后缀；而 `isPrefixAndSuffix("abc", "abcd")` 为 `false`。

请返回满足 `i < j` 且 `isPrefixAndSuffix(words[i], words[j])` 为 `true` 的索引对（index pair）数量。

---

### 示例

#### 示例 1
**输入**: `words = ["a","aba","ababa","aa"]`  
**输出**: `4`  
**解释**: 本例中满足条件的索引对为：
- `i = 0, j = 1`，因为 `isPrefixAndSuffix("a", "aba")` 为 `true`。  
- `i = 0, j = 2`，因为 `isPrefixAndSuffix("a", "ababa")` 为 `true`。  
- `i = 0, j = 3`，因为 `isPrefixAndSuffix("a", "aa")` 为 `true`。  
- `i = 1, j = 2`，因为 `isPrefixAndSuffix("aba", "ababa")` 为 `true`。  

因此答案为 `4`。

#### 示例 2
**输入**: `words = ["pa","papa","ma","mama"]`  
**输出**: `2`  
**解释**: 本例中满足条件的索引对为：
- `i = 0, j = 1`，因为 `isPrefixAndSuffix("pa", "papa")` 为 `true`。  
- `i = 2, j = 3`，因为 `isPrefixAndSuffix("ma", "mama")` 为 `true`。  

因此答案为 `2`。

#### 示例 3
**输入**: `words = ["abab","ab"]`  
**输出**: `0`  
**解释**: 唯一的可能索引对是 `i = 0, j = 1`，但 `isPrefixAndSuffix("abab", "ab")` 为 `false`。  

因此答案为 `0`。

---

### 约束条件
- `1 <= words.length <= 10^5`
- `1 <= words[i].length <= 10^5`
- `words[i]` 仅由小写英文字母组成。
- 所有 `words[i]` 长度之和不超过 `5 * 10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的下标对 `(i, j)`（满足 `i < j`）全部枚举一遍，然后检查 `words[i]` 是否同时是 `words[j]` 的前缀和后缀。  
- **前缀**：可以把 `words[j]` 看成一本书，`words[i]` 就像是书名的开头，只要 `words[j].startswith(words[i])` 为真，就说明它是前缀。  
- **后缀**：同理，后缀就像是书的封底文字，只要 `words[j].endswith(words[i])` 为真，就说明它是后缀。  

只要这两个条件都满足，就把这对下标计入答案。

> **为什么正确？**  
> 暴力枚举遍历了所有合法的 `(i, j)`，对每一对都完整地检查了题目要求的两个条件，因此不可能漏掉也不可能多算。

> **时间/空间复杂度**  
> - 外层遍历 `i` 有 `n` 次，内层遍历 `j` 最多也有 `n` 次，整体是 `O(n²)`。  
> - 对每一对，我们要比较两个字符串的前缀和后缀，最坏情况下要检查整个短字符串的长度 `L`，所以实际时间是 `O(n²·L)`。  
> - 只用了常数级的额外空间（存几个计数器），所以空间复杂度是 `O(1)`。

> **大白话解释**：`O(n²·L)` 可以想象成“如果你有 10,000 本书，每本书平均 1000 个字，要把每本书和每本书都比较一次，那就是 10,000×10,000 次比较，每次还要读 1,000 个字”。显然这在实际中会超时。

#### 代码（Python）

```python
from typing import List

def count_prefix_suffix_pairs_bruteforce(words: List[str]) -> int:
    """
    暴力解：枚举所有 (i, j)，检查 words[i] 是否同时是 words[j] 的前缀和后缀
    """
    n = len(words)
    ans = 0
    for i in range(n):
        wi = words[i]
        for j in range(i + 1, n):
            wj = words[j]
            # 前缀检查
            if wj.startswith(wi) and wj.endswith(wi):
                ans += 1
    return ans

# 示例跑通
if __name__ == "__main__":
    print(count_prefix_suffix_pairs_bruteforce(["a","aba","ababa","aa"]))  # 4
    print(count_prefix_suffix_pairs_bruteforce(["pa","papa","ma","mama"])) # 2
    print(count_prefix_suffix_pairs_bruteforce(["abab","ab"]))            # 0
```

#### 复杂度

- **时间复杂度**：`O(n²·L)`  
  - `n` 是单词数量，`L` 是单词的平均长度。  
  - “平方”意味着随着单词数的增多，运行时间会非常快地飙升。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数计数器，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“两层循环”**——我们对每一对单词都重复做了前缀/后缀检查。  
观察题目可以发现：如果把所有已经出现过的单词按照 **“前缀‑后缀配对”** 的方式组织起来，那么在插入第 `k` 个单词时，只需要沿着它的配对路径走一遍，就能直接知道之前有多少单词已经满足 “前缀且后缀” 的条件。

##### 关键概念：配对字符 + Trie（字典树）

- **配对字符**：对于一个单词 `s`，我们把它从左往右和从右往左同步读取，形成一系列 **二元组**  
  ```
  (s[0], s[-1]), (s[1], s[-2]), (s[2], s[-3]), ...
  ```
  例如 `"aba"` → `[(a,a), (b,b), (a,a)]`。  
  这个二元组把“前缀字符”和“对应的后缀字符”绑在一起，正好对应题目要求的 “前缀也是后缀”。

- **Trie**：想象一本电话簿，里面的每一层对应一个配对字符。  
  - **根节点** 相当于空串。  
  - **子节点** 用 `(c_front, c_back)` 这对字符索引，就像在字典里查单词时每走一步都找下一个字母。  
  - 每个节点记录一个 `cnt_end`：截至目前有多少已经插入的单词 **恰好在这里结束**（即它们的全部配对字符已经遍历完）。  

> **为什么这样可以计数？**  
> 当我们把新单词 `w` 插入 Trie 时，走过的每一个节点都对应着一个已经出现的单词的 **前缀‑后缀配对**。如果某个节点的 `cnt_end > 0`，说明已经有 `cnt_end` 条旧单词在这里“结束”，而这些旧单词正好是 `w` 的 **前缀且后缀**（因为我们是同步从两端读的）。于是把 `cnt_end` 加到答案中即可。

##### 插入过程

1. 从根节点开始，依次取配对字符 `(c_left, c_right)`。  
2. 若当前节点没有对应的子节点，就新建一个。  
3. **在进入子节点前**，把该子节点的 `cnt_end` 累加到答案（因为所有在子节点结束的旧单词都满足条件）。  
4. 移动指针继续处理下一个配对字符。  
5. 当配对字符走完（即遍历完整个单词），把当前节点的 `cnt_end` 加 1，表示这条单词已经完整插入。

##### 复杂度分析（直观）

- 每个单词只遍历一次配对字符，配对字符的数量等于单词长度 `len(s)`。  
- 所有单词的长度总和 ≤ `5·10⁵`（题目限制），所以总的遍历次数也是 ≤ `5·10⁵`。  
- 因此 **时间复杂度** 为 `O(totalLength)`，线性级别。  
- Trie 中每创建一个节点就占用一个常数大小的空间，总节点数同样不超过总字符配对数，即 `O(totalLength)`。  

> **与暴力解对比**：  
> - 暴力是 `O(n²·L)`，最坏会是 `10⁵²` 级别，根本不可接受。  
> - 最优解是 `O(totalLength)`，在本题约 `5·10⁵` 次操作，轻松跑完。

#### 代码（Python）

```python
from typing import List, Tuple, Dict

class TrieNode:
    """Trie 的每个节点，key 为配对字符 (左, 右)"""
    __slots__ = ("children", "cnt_end")
    def __init__(self):
        self.children: Dict[Tuple[str, str], TrieNode] = {}
        self.cnt_end: int = 0          # 以此节点为结束的单词数量

def count_prefix_suffix_pairs_opt(words: List[str]) -> int:
    """
    最优解：使用配对字符 Trie 统计前缀且后缀的下标对数量
    """
    root = TrieNode()
    ans = 0

    for word in words:
        node = root
        L = len(word)
        # 同时从左向右、右向左遍历，生成配对字符
        for k in range(L):
            left_char = word[k]                # 前缀字符
            right_char = word[L - 1 - k]       # 对应的后缀字符
            pair = (left_char, right_char)

            # 若子节点不存在则创建
            if pair not in node.children:
                node.children[pair] = TrieNode()
            node = node.children[pair]

            # 进入该节点前，累计已经结束的旧单词数量
            ans += node.cnt_end

        # 整个单词遍历完后，这个节点就是 “完整单词的结束位置”
        node.cnt_end += 1

    return ans

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(count_prefix_suffix_pairs_opt(["a","aba","ababa","aa"]))  # 4
    print(count_prefix_suffix_pairs_opt(["pa","papa","ma","mama"])) # 2
    print(count_prefix_suffix_pairs_opt(["abab","ab"]))            # 0
```

**代码要点注释**（中文）：

- `TrieNode` 的 `children` 用字典存储，键是 `(左字符, 右字符)` 的二元组，类似 “查字典” 时用单词的首字母定位。
- 插入每个单词时，`for k in range(L)` 同时取左、右字符，形成配对，确保“前缀”和“后缀”同步比较。
- `ans += node.cnt_end` 这一步正是“把已经出现、且恰好在这里结束的单词计数”。如果当前节点的 `cnt_end` 为 3，说明有 3 条旧单词的全部配对字符已经遍历完，它们都是当前单词的前缀且后缀，答案要加 3。
- 最后 `node.cnt_end += 1` 把当前单词登记为已完成，以便后面的单词可以计数。

#### 复杂度

- **时间复杂度**：`O(Σ|words[i]|)`  
  - 只遍历每个字符一次，等价于所有单词长度之和，最多 `5·10⁵`，即线性时间。

- **空间复杂度**：`O(Σ|words[i]|)`  
  - Trie 最多会创建与遍历次数相同的节点，每个节点占用常数空间。

> 与暴力解相比，时间从 **平方级** 降到了 **线性级**，在大数据量下可以瞬间完成。

---

## 心得

- **核心技巧**：把“前缀”和“后缀”同步配对，使用 **Trie**（字典树）一次遍历即完成计数。  
- **适用的题型**：  
  1. **前后缀同时满足的匹配**（如本题、Count Prefix and Suffix Pairs I）。  
  2. **回文前缀/后缀统计**（如 “统计所有单词中既是前缀又是后缀的回文子串”。）  
  3. **双端字符约束的字符串匹配**（如 “找出所有满足左侧字符集合 = 右侧字符集合的子串”。）  
- **一句话总结**：把左右字符配对成“一对”，在 Trie 中把它们当作单个“字母”来插入，就能一次遍历搞定前缀‑后缀计数。

---

## 反思

- **第一反应**：直接枚举所有下标对，用 `startswith` / `endswith` 检查。虽然思路最直接，却忽视了输入规模的限制。  
- **最容易踩的坑**  
  - **边界条件**：单词长度为 1 时，配对字符会是 `(c, c)`，仍然要正常插入。  
  - **重复单词**：如果相同单词出现多次，`cnt_end` 必须累计，否则会漏算。  
  - **字符配对顺序**：必须同步左、右指针，否则会把前缀字符和错误的后缀字符配对，导致计数错误。  
- **下次类似题的第一步**：先思考是否可以把“左侧信息”和“右侧信息”同步压缩成单一的“状态”，再用 Trie / 哈希等结构一次遍历统计。这样往往能把平方级别的暴力降低到线性级。