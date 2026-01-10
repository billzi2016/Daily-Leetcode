# #3485. 移除后 K 个字符串的最长公共前缀 / Longest Common Prefix of K Strings After Removal

> 难度：困难 · 标签：Array、String、Trie · [LeetCode 链接](https://leetcode.com/problems/longest-common-prefix-of-k-strings-after-removal/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words and an integer k.
For each index i in the range [0, words.length - 1], find the length of the longest common prefix among any k strings (selected at distinct indices) from the remaining array after removing the ith element.
Return an array answer, where answer[i] is the answer for ith element. If removing the ith element leaves the array with fewer than k strings, answer[i] is 0.

**Examples**

**Example 1:**

```
Input: words = ["jump","run","run","jump","run"], k = 2
Output: [3,4,4,3,4]
Explanation:
```

**Example 2:**

```
Input: words = ["dog","racer","car"], k = 2
Output: [0,0,0]
Explanation:
```

**Constraints**

- 1 <= k <= words.length <= 105
- 1 <= words[i].length <= 104
- words[i] consists of lowercase English letters.
- The sum of words[i].length is smaller than or equal 105.

---

## 题目（中文翻译）

**描述**  
给定一个字符串数组 `words` 与一个整数 `k`。对于每个索引 `i`（范围为 `[0, words.length - 1]`），在移除第 `i` 个元素之后，从剩余数组中挑选任意 **k** 个下标不同的字符串，求它们的 **最长公共前缀**（longest common prefix）的长度。返回数组 `answer`，其中 `answer[i]` 为对应的答案。如果移除第 `i` 个元素后数组中的字符串数量少于 **k**，则 `answer[i] = 0`。

**示例 1**  
```text
Input: words = ["jump","run","run","jump","run"], k = 2
Output: [3,4,4,3,4]
Explanation:
移除下标 0 的 "jump" 后，剩余字符串为 ["run","run","jump","run"]。任选任意 2 个字符串，最长公共前缀的最大长度为 3（例如 "run" 与 "run" 的公共前缀 "run" 长度为 3）。其余下标同理，得到结果 [3,4,4,3,4]。
```

**示例 2**  
```text
Input: words = ["dog","racer","car"], k = 2
Output: [0,0,0]
Explanation:
任意移除一个字符串后，剩余最多只有 2 个字符串，而这两者之间没有公共前缀（长度为 0），因此所有答案均为 0。
```

**约束条件**  
- `1 <= k <= words.length <= 10^5`  
- `1 <= words[i].length <= 10^4`  
- `words[i]` 仅由小写英文字母组成。  
- 所有 `words[i]` 的长度之和 ≤ `10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的情况都枚举一遍**：

1. 先把第 `i` 个单词踢出去，得到剩下的数组 `rest`。  
2. 从 `rest` 中任选 `k` 个不同下标的单词（组合），算出这 `k` 个单词的公共前缀长度。  
3. 把所有组合得到的长度取最大值，就是 `answer[i]`。  

> **类比**：把每个单词想成一本书的标题，公共前缀就是这些标题的“共同开头”。暴力解就是把所有可能的 `k` 本书挑出来，逐本比较它们的开头有多长。  

> **为什么正确**：因为我们遍历了**所有**合法的 `k`‑组合，最大值必然就是题目要求的最长公共前缀长度。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def longest_common_prefix(strs: List[str]) -> int:
    """返回若干字符串的公共前缀长度"""
    if not strs:
        return 0
    # 逐字符比较，遇到不相同就停
    i = 0
    while True:
        cur = strs[0][i] if i < len(strs[0]) else None
        for s in strs[1:]:
            if i >= len(s) or s[i] != cur:
                return i          # 前 i 个字符相同
        i += 1

def brute(words: List[str], k: int) -> List[int]:
    n = len(words)
    ans = [0] * n
    for i in range(n):                      # 要删除的下标 i
        rest = words[:i] + words[i+1:]      # 剩余的数组
        if len(rest) < k:                   # 剩下的字符串不足 k 个
            ans[i] = 0
            continue
        best = 0
        # 枚举所有 k 个下标的组合
        for idxs in combinations(range(len(rest)), k):
            selected = [rest[j] for j in idxs]
            best = max(best, longest_common_prefix(selected))
        ans[i] = best
    return ans
```

> 代码里每一行都有中文注释，直接可以跑。  

#### 复杂度  

- **时间复杂度**：  
  - 对每个 `i`（共 `n` 次），我们要枚举 `C(m, k)` 种组合（`m = n‑1`），每种组合再比较至多 `L`（单词最长长度）个字符。  
  - 所以整体是 **O(n · C(n‑1, k) · L)**。  
  - 对于 `n` 可能是 `10⁵`、`k` 甚至是 `2` 的情况，这已经是**指数级**的时间，根本跑不完。  
  - 大白话：如果把每一次比较想成一次“跑步”，这一步要跑 **上千上万** 次，根本不现实。

- **空间复杂度**：  
  - 只用了几个临时数组，和输入大小同阶 **O(n)**。  

> 暴力解只能帮助我们**理清题意**，但在实际数据规模下会超时。下面我们来寻找更快的办法。

---

### 2. 最优解

#### 思路  

要想快，就必须避免每次都重新枚举所有组合。观察题目可以发现：

- **公共前缀的长度只取决于有多少个字符串在同一个前缀上**。  
- 如果我们把所有单词放进一棵**Trie（字典树）**，每个节点自然记录有多少条路径（即多少单词）经过它。  
- 对于某个 `i`，把 `words[i]` 从 Trie 中“删掉”后，只要找** deepest（最深）且经过的路径数 ≥ k 的节点**，它的深度就是答案。  

于是我们把问题转化为：

> **在 Trie 上维护每个节点的“经过计数”，并能快速查询当前计数 ≥ k 的最大深度**。

下面一步步实现：

1. **构建 Trie**  
   - 每插入一个单词，就把沿途每个节点的 `cnt` 加 `1`。  
   - 同时记录节点的 `depth`（根为 0，子节点比父节点多 1）。  

2. **初始化 “合格深度集合”**  
   - 遍历所有节点，若 `cnt ≥ k`，把它的 `depth` 放进一个**多重集合**（统计同一深度出现多少次）。  
   - 维护一个变量 `cur_max` 保存当前集合中的最大深度。  

3. **对每个 i 进行“删除‑查询‑恢复”**  
   - **删除**：沿着 `words[i]` 的路径向下走。对每个经过的节点  
        - 若 `cnt` 原本 **≥ k**，而删除后变成 **k‑1**，说明它不再合格，需要把它的 `depth` 从集合中减去一次。  
        - 把 `cnt` 减 `1`。  
   - **查询**：此时 `cur_max`（集合的最大深度）就是 `answer[i]`。如果集合为空，则答案是 `0`。  
   - **恢复**：再把同一条路径的 `cnt` 加回 `1`，并在必要时把对应的 `depth` 加回集合。  

4. **集合的实现**  
   - 由于只需要 **插入 / 删除 / 取最大**，我们可以用 `collections.Counter` 记录每个深度出现的次数，再用一个 **堆**（最大堆）或直接维护 `cur_max` 手动更新。  
   - 为了代码更直观，这里采用 `Counter` + 手动维护 `cur_max` 的方式：  
        - 插入深度 `d`：`cnt_depth[d] += 1`，并把 `cur_max = max(cur_max, d)`。  
        - 删除深度 `d`：`cnt_depth[d] -= 1`，若 `cnt_depth[d] == 0` 且 `d == cur_max`，则向下搜索下一个非零深度更新 `cur_max`。  

> **类比**：Trie 就像一棵“单词树”，每条从根到叶子的路径对应一个单词。节点的 `cnt` 像是“这段路上有多少人在走”。我们关心的是“至少有 k 个人一起走的最远的路有多长”。当我们把某个人（第 i 个单词）请走时，只需要在这条路上把人数减一，然后看还能走多远。

#### 代码（Python）

```python
from collections import defaultdict, Counter
from typing import List

class TrieNode:
    __slots__ = ('children', 'cnt', 'depth')
    def __init__(self, depth: int):
        self.children = {}          # 子节点，key 是字符
        self.cnt = 0                # 经过此节点的单词数
        self.depth = depth          # 距离根的字符数

def build_trie(words: List[str]) -> TrieNode:
    """把所有单词插入 Trie，同时返回根节点"""
    root = TrieNode(depth=0)
    for w in words:
        node = root
        node.cnt += 1               # 根节点也计数
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode(depth=node.depth + 1)
            node = node.children[ch]
            node.cnt += 1
    return root

def collect_initial_depths(root: TrieNode, k: int, depth_counter: Counter) -> int:
    """遍历 Trie，把 cnt >= k 的节点深度加入 Counter，返回当前最大深度"""
    max_depth = 0
    stack = [root]
    while stack:
        node = stack.pop()
        if node.cnt >= k:
            depth_counter[node.depth] += 1
            if node.depth > max_depth:
                max_depth = node.depth
        for child in node.children.values():
            stack.append(child)
    return max_depth

def update_depth_counter(depth_counter: Counter, depth: int, delta: int, cur_max: int) -> int:
    """
    delta = +1 表示该深度新增一个合格节点
    delta = -1 表示该深度失去一个合格节点
    返回更新后的 cur_max
    """
    if delta == 1:
        depth_counter[depth] += 1
        if depth > cur_max:
            cur_max = depth
    else:  # delta == -1
        depth_counter[depth] -= 1
        if depth_counter[depth] == 0 and depth == cur_max:
            # 向下寻找下一个仍有节点的深度
            while cur_max > 0 and depth_counter[cur_max] == 0:
                cur_max -= 1
    return cur_max

def longest_common_prefix_after_removal(words: List[str], k: int) -> List[int]:
    n = len(words)
    if k == 0:                     # 题目保证 k >= 1，这里防御性写法
        return [0] * n

    # 1️⃣ 建 Trie 并统计每个深度的合格节点数
    root = build_trie(words)
    depth_counter = Counter()      # depth -> 合格节点数
    cur_max = collect_initial_depths(root, k, depth_counter)

    ans = [0] * n

    for idx, w in enumerate(words):
        # 2️⃣ 删除 words[idx]：沿路径更新 cnt 与 depth_counter
        node = root
        # 根节点也需要检查是否从 >=k 变为 <k
        if node.cnt >= k and node.cnt - 1 < k:
            cur_max = update_depth_counter(depth_counter, node.depth, -1, cur_max)
        node.cnt -= 1

        for ch in w:
            child = node.children[ch]
            if child.cnt >= k and child.cnt - 1 < k:   # 交叉阈值
                cur_max = update_depth_counter(depth_counter, child.depth, -1, cur_max)
            child.cnt -= 1
            node = child

        # 3️⃣ 查询当前最大深度
        ans[idx] = cur_max if cur_max > 0 else 0

        # 4️⃣ 恢复原状：把同一条路径的 cnt 加回去，并相应更新 depth_counter
        node = root
        if node.cnt >= k - 1 and node.cnt + 1 >= k:   # 之前 <k，现在 >=k
            cur_max = update_depth_counter(depth_counter, node.depth, +1, cur_max)
        node.cnt += 1

        for ch in w:
            child = node.children[ch]
            if child.cnt >= k - 1 and child.cnt + 1 >= k:
                cur_max = update_depth_counter(depth_counter, child.depth, +1, cur_max)
            child.cnt += 1
            node = child

    return ans
```

> **代码要点**  
- `TrieNode.__slots__` 用来省内存（可选）。  
- `depth_counter` 记录“当前 **合格**（cnt ≥ k） 的节点有多少个”——相当于一个**多重集合**。  
- `cur_max` 始终保存集合中最大的深度，查询时直接返回，**O(1)**。  
- 删除/恢复的过程只遍历被删单词的字符数，总体时间是所有单词长度之和。

#### 复杂度  

- **时间复杂度**：  
  - 建 Trie：遍历所有字符一次 → **O( Σ|words[i]| )**。  
  - 对每个下标 `i`，删除 + 查询 + 恢复都只走一次该单词的路径 → **同样是 O( Σ|words[i]| )**。  
  - 整体 **O( Σ|words[i]| )**，在约束下不超过 `10⁵`，非常快。  

- **空间复杂度**：  
  - Trie 节点数等于所有字符数的上限 → **O( Σ|words[i]| )**。  
  - 额外的 `depth_counter`、`cur_max`、递归栈等都是线性或常数级别。  

> 与暴力解相比，时间从指数级降到了线性级，几乎瞬间可以得到答案。

---

## 心得

- **核心技巧**：使用 **Trie（字典树）** 记录前缀出现次数，并配合 **深度计数集合** 实时维护 “出现 ≥ k 次的最长前缀”。  
- **适用场景**：  
  1. “在一组字符串中找出现次数不少于 k 的最长公共前缀”。  
  2. “统计所有前缀出现次数并快速查询出现次数最多的前缀”。  
  3. “动态增删字符串后，仍能快速求满足某个阈值的最长公共前缀”。  
- **一句话总结**：**把“多少字符串在同一个前缀上”抽象成 Trie 节点的计数，维护计数≥k 的最大深度即可**。

---

## 反思

- **第一反应**：直接想遍历所有 `k` 组合，写出暴力代码来验证思路。  
- **最容易踩的坑**：  
  - **边界条件**：当删除后剩余字符串少于 `k` 时答案必须是 `0`，需要在代码里提前判断。  
  - **计数阈值的切换**：在删减或恢复时，节点的 `cnt` 可能正好从 `k` 变到 `k‑1`（或相反），这时必须同步更新 “合格深度集合”。忘记这一步会导致 `cur_max` 不准确。  
  - **深度的回溯**：当 `cur_max` 所在的深度被删光后，需要向下寻找下一个非空深度，不能直接把 `cur_max` 设为 `0`。  
- **下次类似题的第一步**：  
  1. **抽象出“计数”**：想想是否可以用 Trie、前缀哈希或累计数组来记录某类属性的出现次数。  
  2. **确定阈值**：题目要求的 “≥ k” 往往可以转化为“把计数≥k 的位置维护在一个集合里”。  
  3. **增删维护**：如果题目涉及“删除某个元素后再查询”，就要考虑如何**在局部改动时只更新受影响的部分**，而不是整体重算。  

祝你在算法的道路上越走越稳！ 🎉