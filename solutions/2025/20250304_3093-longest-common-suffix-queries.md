# #3093. 最长公共后缀查询 / Longest Common Suffix Queries

> 难度：困难 · 标签：Array、String、Trie · [LeetCode 链接](https://leetcode.com/problems/longest-common-suffix-queries/)

---

## 题目（英文原版）

**Description**

You are given two arrays of strings wordsContainer and wordsQuery.
For each wordsQuery[i], you need to find a string from wordsContainer that has the longest common suffix with wordsQuery[i]. If there are two or more strings in wordsContainer that share the longest common suffix, find the string that is the smallest in length. If there are two or more such strings that have the same smallest length, find the one that occurred earlier in wordsContainer.
Return an array of integers ans, where ans[i] is the index of the string in wordsContainer that has the longest common suffix with wordsQuery[i].

**Examples**

**Example 1:**

```
Input: wordsContainer = ["abcd","bcd","xbcd"], wordsQuery = ["cd","bcd","xyz"]
Output: [1,1,1]
Explanation:
Let's look at each wordsQuery[i] separately:
```

**Example 2:**

```
Input: wordsContainer = ["abcdefgh","poiuygh","ghghgh"], wordsQuery = ["gh","acbfgh","acbfegh"]
Output: [2,0,2]
Explanation:
Let's look at each wordsQuery[i] separately:
```

**Constraints**

- 1 <= wordsContainer.length, wordsQuery.length <= 104
- 1 <= wordsContainer[i].length <= 5 * 103
- 1 <= wordsQuery[i].length <= 5 * 103
- wordsContainer[i] consists only of lowercase English letters.
- wordsQuery[i] consists only of lowercase English letters.
- Sum of wordsContainer[i].length is at most 5 * 105.
- Sum of wordsQuery[i].length is at most 5 * 105.

---

## 题目（中文翻译）

给定两个字符串数组（array）`wordsContainer` 和 `wordsQuery`。  
对于每个 `wordsQuery[i]`，需要在 `wordsContainer` 中找到一个字符串，使其与 `wordsQuery[i]` 的公共后缀（suffix）最长。若有多个字符串拥有相同的最长公共后缀，则选取长度最短的那个；若仍有多个长度相同的字符串，则选取在 `wordsContainer` 中出现最早的那个。  

返回一个整数数组 `ans`，其中 `ans[i]` 为对应的 `wordsContainer` 中字符串的下标（index）。

### 示例

#### 示例 1
输入:  
```
wordsContainer = ["abcd","bcd","xbcd"], wordsQuery = ["cd","bcd","xyz"]
```
输出:  
```
[1,1,1]
```
解释:  
逐个查看 `wordsQuery[i]`：

- `wordsQuery[0] = "cd"` 与 `wordsContainer` 中的 `"bcd"`（下标 1）共享后缀 `"cd"`，长度为 2；与 `"abcd"`（下标 0）共享后缀 `"cd"` 同样长度为 2，但 `"bcd"` 更短（长度 3 < 4），因此选下标 1。  
- `wordsQuery[1] = "bcd"` 与 `"bcd"`（下标 1）完全相同，公共后缀长度为 3，显然是最长的。  
- `wordsQuery[2] = "xyz"` 与 `wordsContainer` 中所有字符串的公共后缀长度均为 0，按照长度最短且出现最早的原则，选下标 1（`"bcd"` 的长度为 3，最短且最先出现）。

#### 示例 2
输入:  
```
wordsContainer = ["abcdefgh","poiuygh","ghghgh"], wordsQuery = ["gh","acbfgh","acbfegh"]
```
输出:  
```
[2,0,2]
```
解释:  
逐个查看 `wordsQuery[i]`：

- `wordsQuery[0] = "gh"` 与 `"ghghgh"`（下标 2）共享后缀 `"gh"`，长度为 2；与其他两个字符串共享的后缀长度也为 2，但 `"ghghgh"` 的长度最短（6 < 7、8），因此选下标 2。  
- `wordsQuery[1] = "acbfgh"` 与 `"abcdefgh"`（下标 0）共享后缀 `"fgh"`，长度为 3；与 `"poiuygh"` 只共享 `"gh"`（长度 2），与 `"ghghgh"` 共享 `"gh"`（长度 2），所以选下标 0。  
- `wordsQuery[2] = "acbfegh"` 与 `"ghghgh"`（下标 2）共享后缀 `"gh"`，长度为 2；与 `"abcdefgh"` 共享后缀 `"gh"` 长度同样为 2，但两者长度相同（均为 8），而 `"ghghgh"` 在 `wordsContainer` 中出现更晚，但根据规则需选取出现更早的，即下标 2（因为在相同长度的候选中，`"ghghgh"` 的长度 6 更短）。  

### 约束条件
- `1 <= wordsContainer.length, wordsQuery.length <= 10^4`
- `1 <= wordsContainer[i].length <= 5 * 10^3`
- `1 <= wordsQuery[i].length <= 5 * 10^3`
- `wordsContainer[i]` 仅由小写英文字母组成。
- `wordsQuery[i]` 仅由小写英文字母组成。
- 所有 `wordsContainer[i]` 的长度之和至多为 `5 * 10^5`。
- 所有 `wordsQuery[i]` 的长度之和至多为 `5 * 10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每个查询 `wordsQuery[i]` 与 `wordsContainer` 中的每个字符串逐个比较**，求出它们的公共后缀长度，然后挑选出满足题目要求的那个下标。

- **比较后缀**：可以把两个字符串从尾巴往前遍历，只要字符相等就继续计数，遇到不相等就停下来。  
- **记录最优**：遍历 `wordsContainer` 时维护三个指标  
  1. **最长的公共后缀长度**（越大越好）  
  2. **最短的容器字符串长度**（在后缀长度相同的情况下，越短越好）  
  3. **最早出现的下标**（长度也相同的情况下，取下标更小的）  

这样遍历完所有容器字符串，就能得到答案。

> **生活化类比**：  
> 把 `wordsContainer` 想成一本字典，`wordsQuery[i]` 是我们手里的一张纸条。我们要在字典里找出和纸条“尾巴”最相同的词，若有多本相同的，就挑最短的那本，仍然相同就挑最先放进字典的那本。

**为什么正确**：因为我们把所有可能的配对都检查了一遍，严格按照题目给出的优先级（后缀长 → 长度短 → 下标小）挑选最优，所以必然得到正确答案。

#### 代码（Python）

```python
from typing import List

def longest_common_suffix(a: str, b: str) -> int:
    """返回 a 与 b 的公共后缀长度。"""
    i, j = len(a) - 1, len(b) - 1
    cnt = 0
    while i >= 0 and j >= 0 and a[i] == b[j]:
        cnt += 1
        i -= 1
        j -= 1
    return cnt


def brute_force(wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
    n = len(wordsContainer)
    ans = []
    for q in wordsQuery:                     # 对每个查询逐个处理
        best_idx = -1
        best_suf = -1        # 最长后缀长度
        best_len = float('inf')  # 容器字符串的最小长度
        for idx, w in enumerate(wordsContainer):
            suf = longest_common_suffix(q, w)   # 计算公共后缀长度
            # 按题目优先级比较：后缀长 → 长度短 → 下标小
            if (suf > best_suf or
                (suf == best_suf and len(w) < best_len) or
                (suf == best_suf and len(w) == best_len and idx < best_idx)):
                best_suf = suf
                best_len = len(w)
                best_idx = idx
        ans.append(best_idx)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(|Q| * |C| * L)`  
  - `|Q|` 为查询数量，`|C|` 为容器字符串数量，`L` 为两者平均长度。  
  - 直观上可以把 `O(|Q| * |C| * L)` 想成“每个查询要和每个容器字符串进行一次‘从尾巴往前比字符’的操作”。如果 `|Q|=10⁴，|C|=10⁴，L≈10³`，显然会超时。  
- **空间复杂度**：`O(1)`（不计输出数组），只用了常数级的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次查询都要遍历整个 `wordsContainer`**，导致 `|Q| * |C|` 的乘法爆炸。  
我们需要一种 **“一次预处理，查询时快速定位”** 的结构。

> **关键观察**：  
> 把所有字符串 **反转**（reverse）后，**公共后缀** 就变成了 **公共前缀**。  
> 于是问题等价于：  
> “在一组已经反转的字符串里，找出与查询字符串（同样反转）拥有最长公共前缀的那一个”。  

> **前缀查询的常用数据结构**：**Trie（字典树）**。  
> Trie 的每个节点代表一个字符，从根到某节点的路径就是一个前缀。我们只要沿着查询的字符一路下去，就能得到最长公共前缀对应的最深节点。

**如何在 Trie 中直接得到满足三重条件的答案？**  

在每个 Trie 节点我们保存 **“截至当前前缀，最优的容器字符串的下标”**。  
插入每个容器字符串（已反转）时，沿路径走到每个节点，**比较当前保存的最优下标与正在插入的字符串下标**，如果新字符串更好，就用它来覆盖。

比较的规则正好是题目要求的优先级：

1. **前缀越长 → 后缀越长**（因为我们在同一个节点，深度相同，后缀长度相同）  
2. **容器字符串越短**（长度短的更好）  
3. **下标越小**（出现更早的更好）

因为我们在 **插入时** 已经把最优下标写进每个节点，查询时只需要沿着查询的字符一路往下走，**最后能走到的最深节点的记录就是答案**（如果某一步找不到对应的子节点，就停在当前节点）。

**步骤概览**：

1. **预处理**  
   - 把 `wordsContainer` 中的每个字符串反转。  
   - 建立 Trie，插入每个反转字符串。插入时更新每个节点的 `best_idx`。  

2. **查询**  
   - 把每个查询字符串反转。  
   - 从根节点开始，逐字符向下走，记录走到的最深节点的 `best_idx`。  
   - 当字符在 Trie 中不存在对应子节点时，停止，返回当前节点保存的下标。  

这样每个查询只需要 **O(查询字符串长度)** 的时间，整个过程的总时间是 **所有字符长度之和**，满足题目约束。

#### 代码（Python）

```python
from typing import List, Dict

class TrieNode:
    __slots__ = ('children', 'best_idx')
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.best_idx: int = -1          # 当前前缀下最优的容器下标

def better(a_idx: int, b_idx: int,
           container: List[str]) -> int:
    """
    返回两者中更好的那个下标。
    - a_idx, b_idx 均可能为 -1（表示不存在）。
    - 按 “后缀长 → 长度短 → 下标小” 的规则比较。
    """
    if a_idx == -1: return b_idx
    if b_idx == -1: return a_idx
    a = container[a_idx]
    b = container[b_idx]
    # 这里的 “后缀长” 已经在 Trie 深度上体现，只比较长度和下标即可
    if len(a) < len(b):          # 长度更短更好
        return a_idx
    if len(a) > len(b):
        return b_idx
    # 长度相同，取下标更小的
    return a_idx if a_idx < b_idx else b_idx


def build_trie(container: List[str]) -> TrieNode:
    """把 container 中的每个字符串（已反转）插入 Trie，并维护每个节点的 best_idx。"""
    root = TrieNode()
    for idx, word in enumerate(container):
        node = root
        # 从第一个字符（即原串的最后一个字符）开始插入
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            # 更新当前节点的 best_idx
            node.best_idx = better(node.best_idx, idx, container)
    # 根节点也需要记录全局最优（全部容器都经过根节点）
    root.best_idx = better(root.best_idx, min(range(len(container)), key=lambda i: (len(container[i]), i)), container)
    return root


def query_trie(root: TrieNode, q_rev: str, container: List[str]) -> int:
    """在 Trie 中寻找 q_rev 的最长公共前缀对应的最优下标。"""
    node = root
    best = node.best_idx                 # 即使根节点已经是答案
    for ch in q_rev:
        if ch not in node.children:      # 前缀中断，直接返回当前 best
            break
        node = node.children[ch]
        best = node.best_idx             # 越往下深，公共前缀越长
    return best


def optimal(wordsContainer: List[str], wordsQuery: List[str]) -> List[int]:
    # 1️⃣ 把容器字符串反转
    rev_container = [w[::-1] for w in wordsContainer]
    # 2️⃣ 建 Trie（插入时维护 best_idx）
    trie_root = build_trie(rev_container)

    # 3️⃣ 逐查询求答案
    ans = []
    for q in wordsQuery:
        rev_q = q[::-1]
        ans.append(query_trie(trie_root, rev_q, wordsContainer))
    return ans
```

> **代码要点说明**  
> - `TrieNode.best_idx` 保存 **“截至当前前缀的最优容器下标”**。  
> - `better` 函数把 **长度短 → 下标小** 的比较抽象出来，方便在插入时统一使用。  
> - 插入时每经过一个节点就调用 `better`，保证每个节点始终保存最优答案。  
> - 查询时只要沿着查询的字符走到最深的可达节点，那个节点的 `best_idx` 就是答案。

#### 复杂度  

- **时间复杂度**  
  - **构建 Trie**：`O( Σ |wordsContainer[i]| )`，即所有容器字符串长度之和（不超过 `5·10⁵`）。  
  - **每个查询**：`O( |wordsQuery[i]| )`，所有查询共 `O( Σ |wordsQuery[i]| )`（同样不超过 `5·10⁵`）。  
  - **总计**：`O( Σ|container| + Σ|query| )`，约 `10⁶` 级别，轻松跑完。  
  - 与暴力解的 `O(|Q|·|C|·L)` 相比，省去了乘法，几乎快了 **上千倍**。

- **空间复杂度**  
  - Trie 中每个字符对应一个节点，最多 `Σ|wordsContainer[i]|` 个节点。每个节点只保存子节点指针（字典）和一个整数，下标。  
  - 因此空间 `O( Σ|wordsContainer[i]| )`，即约 `5·10⁵` 个节点，符合限制。  

---

## 心得

- **核心技巧**：把 “公共后缀” 通过 **字符串反转** 转化为 “公共前缀”，随后利用 **Trie（字典树）** 进行前缀的快速匹配，并在构建阶段就把 **最优下标** 存进每个节点。  
- **适用的题型**  
  1. “最长公共后缀 / 前缀查询” 系列（如 LeetCode 1146、1061）  
  2. “前缀/后缀匹配 + 额外排序/筛选条件” 的多查询问题  
  3. 需要 **一次预处理、批量快速查询** 的字符串匹配题（如搜索引擎自动补全）  
- **一句话总结解题钥匙**：**“反转 + Trie + 预存最优”**。

---

## 反思

- **第一反应**：直接套用双层循环，逐对比较后缀。  
- **最容易踩的坑**  
  - 忘记在后缀相同的情况下还要比较 **容器字符串长度** 与 **出现顺序**，导致答案不符合题目细则。  
  - 对 **极长字符串**（长度可达 5 000）使用暴力会导致超时。  
  - Trie 实现时若只存 `best_idx` 而不在插入时及时更新，查询得到的可能不是**最短**的同层字符串。  
- **下次类似题的第一步**：**先思考能否把 “后缀” 转换为 “前缀”**（反转字符串），再寻找 **适合前缀的高效结构**（Trie、前缀哈希等），并在构建阶段把所有筛选条件一起预处理进去。