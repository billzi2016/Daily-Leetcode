# #2213. **最长单字符重复子串** / Longest Substring of One Repeating Character

> 难度：困难 · 标签：Array、String、Segment Tree、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/longest-substring-of-one-repeating-character/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s. You are also given a 0-indexed string queryCharacters of length k and a 0-indexed array of integer indices queryIndices of length k, both of which are used to describe k queries.
The ith query updates the character in s at index queryIndices[i] to the character queryCharacters[i].
Return an array lengths of length k where lengths[i] is the length of the longest substring of s consisting of only one repeating character after the ith query is performed.

**Examples**

**Example 1:**

```
Input: s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]
Output: [3,3,4]
Explanation: 
- 1st query updates s = "bbbacc". The longest substring consisting of one repeating character is "bbb" with length 3.
- 2nd query updates s = "bbbccc". 
  The longest substring consisting of one repeating character can be "bbb" or "ccc" with length 3.
- 3rd query updates s = "bbbbcc". The longest substring consisting of one repeating character is "bbbb" with length 4.
Thus, we return [3,3,4].
```

**Example 2:**

```
Input: s = "abyzz", queryCharacters = "aa", queryIndices = [2,1]
Output: [2,3]
Explanation:
- 1st query updates s = "abazz". The longest substring consisting of one repeating character is "zz" with length 2.
- 2nd query updates s = "aaazz". The longest substring consisting of one repeating character is "aaa" with length 3.
Thus, we return [2,3].
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.
- k == queryCharacters.length == queryIndices.length
- 1 <= k <= 105
- queryCharacters consists of lowercase English letters.
- 0 <= queryIndices[i] < s.length

---

## 题目（中文翻译）

给定一个下标从 0 开始的字符串 `s`。同时给定长度为 `k` 的下标从 0 开始的字符串 `queryCharacters` 和下标从 0 开始的整数数组 `queryIndices`，它们共同描述了 `k` 条查询。

第 `i` 条查询将 `s` 中下标为 `queryIndices[i]` 的字符更新为 `queryCharacters[i]`。

返回一个长度为 `k` 的数组 `lengths`，其中 `lengths[i]` 为执行第 `i` 条查询后，`s` 中仅由同一个字符连续构成的最长子字符串（substring）的长度。

---

### 示例

#### 示例 1
**输入**  
```text
s = "babacc"
queryCharacters = "bcb"
queryIndices = [1,3,3]
```
**输出**  
```text
[3,3,4]
```
**解释**  
- 第 1 条查询后，`s` 变为 `"bbbacc"`。最长的仅由同一字符组成的子字符串是 `"bbb"`，长度为 3。  
- 第 2 条查询后，`s` 变为 `"bbbccc"`。最长的仅由同一字符组成的子字符串可以是 `"bbb"` 或 `"ccc"`，长度为 3。  
- 第 3 条查询后，`s` 变为 `"bbbbcc"`。最长的仅由同一字符组成的子字符串是 `"bbbb"`，长度为 4。  

#### 示例 2
**输入**  
```text
s = "abyzz"
queryCharacters = "aa"
queryIndices = [2,1]
```
**输出**  
```text
[2,3]
```
**解释**  
- 第 1 条查询后，`s` 变为 `"abazz"`。最长的仅由同一字符组成的子字符串是 `"zz"`，长度为 2。  
- 第 2 条查询后，`s` 变为 `"aaazz"`。最长的仅由同一字符组成的子字符串是 `"aaa"`，长度为 3。  

---

### 约束条件
- `1 <= s.length <= 10^5`
- `s` 只包含小写英文字母。
- `k == queryCharacters.length == queryIndices.length`
- `1 <= k <= 10^5`
- `queryCharacters` 只包含小写英文字母。
- `0 <= queryIndices[i] < s.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：每收到一次查询，就把字符串 `s` 中对应位置的字符改掉，然后**整体遍历一次**，找出最长的只含同一个字符的连续子串。  

- **遍历**：从左到右走一遍，用一个计数器 `cnt` 记录当前字符连续出现的长度；如果下一个字符和前一个相同，`cnt += 1`，否则把 `cnt` 与全局最大值 `ans` 比较后重置为 `1`。  
- **更新字符**：把 `s[queryIndices[i]] = queryCharacters[i]`，这一步和改写纸上的文字差不多，直接赋值即可。  

> **类比**：把字符串想成一排颜色相同的积木，查询就像把某块积木重新涂色。暴力解相当于每次改完颜色后，从左到右重新数一遍每段相同颜色的积木有多长。

这个方法一定能得到正确答案，因为我们在每一次查询后都完整地检查了所有可能的子串。

#### 代码（Python）

```python
def longest_substring_bruteforce(s: str, queryChars: str, queryIdx: list[int]) -> list[int]:
    s = list(s)                     # 方便原地修改字符
    res = []

    for ch, idx in zip(queryChars, queryIdx):
        s[idx] = ch                 # ① 更新字符

        # ② 完整遍历一次，求最长同字符子串
        max_len = 1
        cur_len = 1
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:    # 与前一个字符相同，长度+1
                cur_len += 1
            else:                   # 不同，重新计数
                max_len = max(max_len, cur_len)
                cur_len = 1
        max_len = max(max_len, cur_len)   # 最后一次比较
        res.append(max_len)

    return res
```

#### 复杂度

- **时间复杂度**：`O(k * n)`，其中 `n = len(s)`，`k` 是查询次数。  
  大白话：每一次查询都要把整条字符串从头到尾数一遍，最坏情况下要 `n` 次遍历，查询有 `k` 次，所以乘起来。  
- **空间复杂度**：`O(n)`（存放可变的字符列表）+ `O(k)`（返回结果），不算输入本身，这里主要是把字符串转成列表需要的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次查询都要遍历整个字符串**。我们需要一种数据结构，能够在**局部修改后**快速得到**整个区间的最长同字符子串**。这正是**线段树（Segment Tree）**的强项：  

1. **局部更新**：把某个位置的字符改掉，只需要 `O(log n)` 时间更新涉及到的树节点。  
2. **区间合并**：每个线段树节点保存足够的信息，使得合并左右子区间时能够立即得到该区间的答案。

##### 需要在每个节点保存的 5 项信息  

| 信息 | 含义 | 类比 |
|------|------|------|
| `left_char` | 区间最左边的字符 | “左端的积木颜色” |
| `right_char` | 区间最右边的字符 | “右端的积木颜色” |
| `pref_len` | **前缀**（从左端开始）连续相同字符的最大长度 | 从左边往右数，连续相同颜色的积木数 |
| `suff_len` | **后缀**（到右端结束）连续相同字符的最大长度 | 从右边往左数，连续相同颜色的积木数 |
| `best_len` | 区间内部**任意位置**最长的同字符子串长度 | 整段积木里最长的同色连续块 |

有了这些信息，**合并**两个相邻区间 `L` 与 `R` 时：

- `left_char = L.left_char`
- `right_char = R.right_char`
- `pref_len = L.pref_len`，如果 `L.pref_len == len(L)` 且 `L.right_char == R.left_char`，则可以把左区间全部连上右区间的前缀：`pref_len = L.len + R.pref_len`
- `suff_len` 同理，若 `R.suff_len == len(R)` 且 `L.right_char == R.left_char`，则 `suff_len = R.len + L.suff_len`
- `best_len` 取三者最大：`max(L.best_len, R.best_len, L.suff_len + R.pref_len if L.right_char == R.left_char else 0)`

这里的 `len(L)` 表示左子区间的长度（可以在建树时存），同理 `len(R)`。

这样，每次 **点更新**（把某个字符改成新字符）只需要在树的高度（约 `log₂ n`）上重新计算这些信息，**查询整个字符串的答案**只需要查看根节点的 `best_len`。

> **类比**：想象把整条积木链分成很多小段，每段都记好左端颜色、右端颜色、左端连续同色的长度、右端连续同色的长度以及段内最长同色块。修改一块积木时，只需要重新检查它所在的小段以及向上合并的段，像拼图一样快速得到整体信息。

##### 实现要点

- 用数组 `tree` 存线段树，节点编号从 `1` 开始，左子 `2*i`，右子 `2*i+1`。
- 每个节点保存一个 `Node` 对象，属性如上。
- 建树时递归把每个字符包装成叶子节点：`pref_len = suff_len = best_len = 1`，`left_char = right_char = ch`。
- 更新时递归下沉到对应叶子，修改字符后回溯合并。
- 每次查询只读取根节点的 `best_len` 并加入答案列表。

#### 代码（Python）

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    left_char: str   # 区间最左侧字符
    right_char: str  # 区间最右侧字符
    pref_len: int    # 前缀相同字符的最大长度
    suff_len: int    # 后缀相同字符的最大长度
    best_len: int    # 区间内部最长相同字符子串长度
    length: int      # 区间总长度（方便合并时使用）

def merge(a: Node, b: Node) -> Node:
    """合并相邻的两个区间 a、b，返回新的 Node"""
    if a is None: return b
    if b is None: return a

    # 左右端字符
    left_char = a.left_char
    right_char = b.right_char

    # 前缀长度
    pref_len = a.pref_len
    if a.pref_len == a.length and a.right_char == b.left_char:
        pref_len = a.length + b.pref_len

    # 后缀长度
    suff_len = b.suff_len
    if b.suff_len == b.length and a.right_char == b.left_char:
        suff_len = b.length + a.suff_len

    # 最佳长度：左区、右区、跨区（如果左右端字符相同）
    cross = a.suff_len + b.pref_len if a.right_char == b.left_char else 0
    best_len = max(a.best_len, b.best_len, cross)

    return Node(
        left_char=left_char,
        right_char=right_char,
        pref_len=pref_len,
        suff_len=suff_len,
        best_len=best_len,
        length=a.length + b.length,
    )

class SegmentTree:
    def __init__(self, s: str):
        self.n = len(s)
        self.tree = [None] * (4 * self.n)   # 足够大的数组
        self._build(1, 0, self.n - 1, s)

    def _build(self, idx: int, l: int, r: int, s: str):
        """递归建树"""
        if l == r:                     # 叶子节点，只有一个字符
            ch = s[l]
            self.tree[idx] = Node(ch, ch, 1, 1, 1, 1)
            return
        mid = (l + r) // 2
        self._build(idx * 2, l, mid, s)
        self._build(idx * 2 + 1, mid + 1, r, s)
        self.tree[idx] = merge(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def update(self, pos: int, new_ch: str):
        """把位置 pos 的字符改成 new_ch"""
        self._update(1, 0, self.n - 1, pos, new_ch)

    def _update(self, idx: int, l: int, r: int, pos: int, new_ch: str):
        if l == r:                     # 到达叶子
            self.tree[idx] = Node(new_ch, new_ch, 1, 1, 1, 1)
            return
        mid = (l + r) // 2
        if pos <= mid:
            self._update(idx * 2, l, mid, pos, new_ch)
        else:
            self._update(idx * 2 + 1, mid + 1, r, pos, new_ch)
        self.tree[idx] = merge(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def query_best(self) -> int:
        """根节点的 best_len 即整条字符串的答案"""
        return self.tree[1].best_len

def longest_substring_segment_tree(s: str,
                                   queryChars: str,
                                   queryIdx: List[int]) -> List[int]:
    seg = SegmentTree(s)
    ans = []
    for ch, idx in zip(queryChars, queryIdx):
        seg.update(idx, ch)          # O(log n) 更新
        ans.append(seg.query_best()) # O(1) 读取根节点
    return ans
```

#### 复杂度

- **时间复杂度**：`O((n + k) * log n)`  
  - 建树一次遍历 `n`，每次查询的点更新需要沿树高更新，树高约为 `log₂ n`，所以 `k` 次查询共 `k·log n`。  
  - 大白话：把整条积木链先拆成小段（一次 O(n)），以后每改一块，只需要重新检查 **树的层数**，层数大约是 `log₂ n`（比如 n=100000 时约 17 层），所以每次改动都很快。

- **空间复杂度**：`O(n)`  
  - 线段树需要约 `4·n` 个节点，每个节点保存常数个属性，和原字符串同量级。  

与暴力解相比，时间从 `O(k·n)` 降到了 `O(k·log n)`，在 `n、k` 都可能高达 `10⁵` 时提升非常明显。

---

## 心得

- **核心技巧**：利用线段树在**点更新**后快速合并区间信息，保持「区间内最长同字符子串」的状态。
- **适用的题型**  
  1. **区间最大连续相同子序列**（如本题）  
  2. **区间最大连续 1 的长度**（二进制数组）  
  3. **区间最大连续递增/递减子段长度**（需要类似的前缀/后缀信息）  
- **一句话总结解题钥匙**：**在每个区间保存「左端字符、右端字符、前缀长度、后缀长度、区间最佳」五个属性，利用这些属性在合并时即可得到整体答案。**

---

## 反思

- **第一反应**：把每次修改后整个字符串重新遍历一遍——最直接但不够高效。  
- **最容易踩的坑**  
  1. **合并时忘记判断左右端字符是否相同**，导致跨区长度错误。  
  2. **前缀/后缀的特殊情况**：左（右）子区间本身全部相同字符时，需要把整段长度加到另一侧的前缀/后缀上。  
  3. **索引越界**：线段树的递归区间 `[l, r]` 要严格对应原字符串的下标范围。  
- **下次遇到同类题**：第一步先思考「每个区间需要保存哪些信息」使得两段可以**无缝合并**，然后再决定使用线段树还是其他区间树（如树状数组、区间并查集）。这样可以快速从暴力到最优的转化。