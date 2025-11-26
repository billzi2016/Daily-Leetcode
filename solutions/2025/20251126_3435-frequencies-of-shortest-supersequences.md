# #3435. **最短公共超序列的频率** / Frequencies of Shortest Supersequences

> 难度：困难 · 标签：Array、String、Bit Manipulation、Graph、Topological Sort、Enumeration · [LeetCode 链接](https://leetcode.com/problems/frequencies-of-shortest-supersequences/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words. Find all shortest common supersequences (SCS) of words that are not permutations of each other.
A shortest common supersequence is a string of minimum length that contains each string in words as a subsequence.
Return a 2D array of integers freqs that represent all the SCSs. Each freqs[i] is an array of size 26, representing the frequency of each letter in the lowercase English alphabet for a single SCS. You may return the frequency arrays in any order.

**Examples**

**Example 1:**

```
Input: words = ["ab","ba"]
Output: [[1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
Explanation:
The two SCSs are "aba" and "bab" . The output is the letter frequencies for each one.
```

**Example 2:**

```
Input: words = ["aa","ac"]
Output: [[2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
Explanation:
The two SCSs are "aac" and "aca" . Since they are permutations of each other, keep only "aac" .
```

**Example 3:**

```
Input: words = ["aa","bb","cc"]
Output: [[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
Explanation:
"aabbcc" and all its permutations are SCSs.
```

**Constraints**

- 1 <= words.length <= 256
- words[i].length == 2
- All strings in words will altogether be composed of no more than 16 unique lowercase letters.
- All strings in words are unique.

---

## 题目（中文翻译）

给定一个字符串数组 `words`。请找出所有 **最短公共超序列**（shortest common supersequence，SCS），且这些 SCS 之间互不为排列（permutations）关系。  
最短公共超序列是指长度最小且能够把 `words` 中每个字符串作为子序列（subsequence）包含进去的字符串。  

返回一个二维整数数组 `freqs`，其中每个 `freqs[i]` 为长度为 26 的数组，表示对应 SCS 中小写英文字母的出现次数。返回的频率数组顺序不限。

---

#### 示例

**示例 1**  
Input: `words = ["ab","ba"]`  
Output: `[[1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]`  
Explanation:  
两个最短公共超序列分别是 `"aba"` 和 `"bab"`，输出为它们各自的字母频率。

**示例 2**  
Input: `words = ["aa","ac"]`  
Output: `[[2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]`  
Explanation:  
最短公共超序列为 `"aac"` 和 `"aca"`。由于两者互为排列，只保留 `"aac"` 对应的频率。

**示例 3**  
Input: `words = ["aa","bb","cc"]`  
Output: `[[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]`  
Explanation:  
`"aabbcc"` 及其所有排列都是最短公共超序列。

---

#### 约束条件

- `1 <= words.length <= 256`
- `words[i].length == 2`
- 所有字符串中出现的不同小写字母总数不超过 `16`
- `words` 中的字符串互不相同

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**把所有可能的字符序列都枚举出来**，然后逐个检查它们是不是每个给定单词的子序列。  
- **枚举的对象**：因为每个单词只有两个字符，所有出现的字符集合的大小至多为 16（题目限制），我们先把这些字符记下来。  
- **如何生成候选序列**：把这些字符全部放进一个列表，允许出现两次（因为有的字符可能需要出现两次才能满足所有顺序约束），然后对列表进行全排列。全排列的过程就像把字典里的所有单词排好序，只是这里的“字典”是我们自己造的字符集合。  
- **子序列检查**：给定一个候选序列 `cand`，我们依次遍历 `cand`，用两个指针分别指向 `cand` 和当前单词 `w`。每当 `cand` 的字符和 `w` 的当前字符相等时，就把 `w` 的指针向后移动一位。等遍历完 `cand` 后，如果 `w` 的指针已经走到单词末尾，说明 `w` 是 `cand` 的子序列。把所有单词都检查一遍，全部通过则 `cand` 是一个公共超序列。  

> **为什么这个方法一定能得到答案？**  
> 我们把 **所有** 可能的字符排列（包括出现两次的情况）都尝试了一遍，只要有一种排列能够让每个单词都出现为子序列，它一定会在我们的枚举里被发现。于是最短的那几个必然会被找出来。

#### 代码（Python）

```python
import itertools
from collections import Counter
from typing import List

def is_superseq(cand: str, words: List[str]) -> bool:
    """判断 cand 是否同时是所有 words 的子序列"""
    for w in words:
        i = 0                 # w 的指针
        for ch in cand:
            if ch == w[i]:
                i += 1
                if i == len(w):   # 已经匹配完 w
                    break
        if i != len(w):            # w 没匹配完，cand 不是超序列
            return False
    return True

def brute_force(words: List[str]) -> List[List[int]]:
    # 1. 收集出现的不同字符
    chars = sorted({c for w in words for c in w})   # 最多 16 个
    n = len(chars)

    # 2. 为每个字符准备「出现一次」和「出现两次」的两种可能
    #    我们把「出现两次」的情况直接写进枚举的基数里：
    #    对每个字符，决定它出现 1 次还是 2 次（2^n 种选择）。
    best_len = float('inf')
    best_freqs = []

    for mask in range(1 << n):          # mask 的第 i 位 = 1 表示字符 chars[i] 出现两次
        # 生成当前 mask 对应的字符列表
        cur_list = []
        for i, ch in enumerate(chars):
            cur_list.append(ch)               # 必出现一次
            if (mask >> i) & 1:               # 需要第二次
                cur_list.append(ch)
        # 3. 对当前字符列表全排列（暴力），找出最短的公共超序列
        for perm in set(itertools.permutations(cur_list)):
            cand = ''.join(perm)
            if is_superseq(cand, words):
                if len(cand) < best_len:
                    best_len = len(cand)
                    best_freqs = []
                if len(cand) == best_len:
                    # 统计频率，转成 26 维向量
                    cnt = [0] * 26
                    for c in cand:
                        cnt[ord(c) - ord('a')] += 1
                    best_freqs.append(cnt)
                break   # 已经找到该 mask 的最短长度，后面的排列不必继续
    # 去重（不同排列但频率相同算同一个答案）
    uniq = []
    seen = set()
    for f in best_freqs:
        tup = tuple(f)
        if tup not in seen:
            seen.add(tup)
            uniq.append(f)
    return uniq
```

> **关键行注释**  
> - `chars = sorted({c for w in words for c in w})`：把所有出现的字符收集起来，就像把字典里所有单词的首字母挑出来放进一个集合。  
> - `mask` 的第 i 位为 1 表示该字符需要出现两次，类似“在字典里查到同一个词出现了两次”。  
> - `itertools.permutations(cur_list)`：把字符全排列，就像把字典里的单词全部排成所有可能的顺序。  

#### 复杂度  

- **时间复杂度**：  
  - 枚举 `2^n`（n ≤ 16）个出现次数的方案。  
  - 对每个方案，枚举所有全排列，最坏情况下是 `(2n)!`（因为每个字符最多出现两次）。  
  - 再对每个排列检查 `|words| ≤ 256` 个子序列，子序列检查是线性的。  
  - 整体时间是 **指数级**，在最坏情况下不可接受（大约 `O(2^n * (2n)!)`），所以只能作为“思路演示”。  

- **空间复杂度**：  
  - 存放字符集合、一个排列以及计数数组，都是 `O(n)`，即最多几百个字符，几乎可以忽略不计。  

> **大白话解释**：  
> `O(2^n * (2n)!)` 意思是“先挑出每个字符出现一次还是两次（2 的 n 次方种挑法），然后把挑好的字符排成所有可能的顺序（阶乘增长），再逐个检查”。阶乘增长非常快，哪怕 n=10 也已经无法在电脑里跑完。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有排列**。其实我们根本不需要真的把字符排出来，只要知道**每个字符出现几次**（1 次还是 2 次）就能唯一确定答案，因为两种出现次数相同的序列互为全排列，频率数组完全相同，题目要求只保留一种。  

下面的最优解把问题转化为**有向无环图（DAG）可否拓扑排序**：

1. **把每个字符看成一个节点**。  
   - 例如单词 `"ab"` 表示 “a 必须出现在 b 前面”，于是我们在图里加一条有向边 `a → b`。  
   - 这条边就像字典里查词的顺序：词条 `a` 在 `b` 之前。

2. **为何最多出现两次？**  
   - 每条边只要求 **“至少有一次 a 在 b 前面”**。  
   - 如果图中没有环（即所有约束可以一次性满足），每个字符只需要出现一次。  
   - 只要出现环，就必须把环里的一些字符 **复制一次**，让它们可以既在前面又在后面出现。因为每条约束只涉及两个字符，复制一次就足够，**不可能需要出现三次**。  

3. **枚举哪些字符需要复制**  
   - 设出现的不同字符集合大小为 `k (≤16)`。  
   - 用一个 `k` 位的二进制掩码 `mask` 表示复制方案：第 `i` 位为 `1` → 字符 `i` 出现 **两次**；为 `0` → 只出现一次。  
   - 对所有 `2^k` 种掩码进行遍历（最多 `2^16 = 65536`，非常可接受）。

4. **对每个掩码构造“复制图”并检测是否是 DAG**  
   - **节点**：  
     - 每个字符 `c` 至少有一个节点 `c₁`（第一次出现）。  
     - 如果 `mask` 对应的字符需要复制，则再创建第二个节点 `c₂`。  
   - **边的添加规则**（关键！）：  
     - 对每个原始单词 `uv`（即边 `u → v`）：
       - 必须保证 **第一次出现的 u 在第一次出现的 v 前** → 加边 `u₁ → v₁`。  
       - 如果 `v` 被复制了（有 `v₂`），**第一次 u 仍然在第二次 v 前** → 加边 `u₁ → v₂`。  
       - 如果 `u` 被复制了（有 `u₂`），**第二次 u 必须在第二次 v 前** → 加边 `u₂ → v₂`。  
       - **不加** `u₂ → v₁`，因为这会让第二次 u 出现在第一次 v 之前，违背 “至少有一次 u 在 v 前面” 的要求。  
   - 这样得到的有向图最多有 `2k ≤ 32` 个节点，边数 `≤ 3 * |words|`（每条原始边最多产生三条新边）。

5. **拓扑排序检测环**  
   - 用 **Kahn 算法**（入度为 0 的节点逐个弹出）判断是否存在环。  
   - 若可以全部弹出，则说明当前 `mask` 能生成一个合法的公共超序列。  
   - 此时序列长度 = `k + popcount(mask)`（每个被复制的字符多占一个位置）。

6. **记录最短长度的所有合法掩码**  
   - 在遍历所有掩码的过程中维护 `min_len`。  
   - 只保留长度等于 `min_len` 且拓扑成功的掩码。  

7. **把合法掩码转成频率数组**  
   - 对每个字符 `c`：出现次数 = `1 + (mask>>i & 1)`。  
   - 把 26 个字母对应的计数填进数组即可。  

> **核心概念解释**  
> - **有向图（Directed Graph）**：把字符看成城市，边看成“必须先到达的道路”。  
> - **拓扑排序（Topological Sort）**：把所有城市排成一条路线，使得所有“先到达”要求都满足。只要路线存在，就没有环路（没有“先回到自己”的矛盾）。  
> - **复制节点**：相当于在同一个城市建了两座楼，分别对应“第一次出现”和“第二次出现”。  

#### 代码（Python）

```python
from typing import List
from collections import deque

def shortest_superseq_frequencies(words: List[str]) -> List[List[int]]:
    # 1️⃣ 收集所有出现的字符，映射到 0..k-1
    chars = sorted({c for w in words for c in w})          # 最多 16 个
    k = len(chars)
    idx = {c: i for i, c in enumerate(chars)}               # 字符 → 编号

    # 预处理原始边 (u -> v) 的编号
    edges = [(idx[w[0]], idx[w[1]]) for w in words]

    min_len = float('inf')
    good_masks = []

    # 2️⃣ 枚举所有可能的“复制方案”
    for mask in range(1 << k):                 # 2^k ≤ 65536
        n_nodes = k + bin(mask).count('1')     # 实际节点数（每个复制字符多一个节点）
        # 为每个字符分配节点编号：
        #   first copy: i
        #   second copy (若被复制): i + k
        #   注意：只在 mask 对应位为 1 时才使用第二个编号
        indeg = [0] * (k * 2)                  # 最多 2k 个节点
        adj   = [[] for _ in range(k * 2)]

        # 3️⃣ 根据复制情况添加有向边
        for u, v in edges:
            # u1 -> v1 必须存在
            adj[u].append(v)
            indeg[v] += 1

            # u1 -> v2（如果 v 被复制）
            if (mask >> v) & 1:
                adj[u].append(v + k)
                indeg[v + k] += 1

            # u2 -> v2（如果 u 被复制）
            if (mask >> u) & 1:
                adj[u + k].append(v + k)
                indeg[v + k] += 1

        # 4️⃣ 拓扑排序检测是否有环
        q = deque([i for i in range(k * 2) if indeg[i] == 0 and (i < k or (mask >> (i - k) & 1))])
        visited = 0
        while q:
            cur = q.popleft()
            visited += 1
            for nb in adj[cur]:
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    q.append(nb)

        # 只要所有实际使用的节点都被访问到，就说明是 DAG
        if visited == n_nodes:
            cur_len = n_nodes                     # 长度 = 节点数
            if cur_len < min_len:
                min_len = cur_len
                good_masks = [mask]
            elif cur_len == min_len:
                good_masks.append(mask)

    # 5️⃣ 把每个合法的 mask 转成 26 维频率数组
    answer = []
    for mask in good_masks:
        freq = [0] * 26
        for i, ch in enumerate(chars):
            cnt = 1 + ((mask >> i) & 1)          # 出现一次还是两次
            freq[ord(ch) - ord('a')] = cnt
        answer.append(freq)

    return answer
```

> **关键行中文注释**  
> - `idx = {c: i for i, c in enumerate(chars)}`：把每个字母对应到一个小编号，像给每本书贴上标签，后面查找更快。  
> - `if (mask >> v) & 1:`：判断字符 `v` 是否需要第二次出现，如果需要，就在图里多建一座“第二层楼”。  
> - `q = deque([...])`：把所有没有前置要求（入度为 0）的楼层先放进队列，类似“先检查所有没有先行限制的任务”。  
> - `if visited == n_nodes:`：如果所有楼层都被排进了顺序，说明没有环路，方案可行。  

#### 复杂度  

- **时间复杂度**  
  - 枚举 `2^k`（k ≤ 16）个掩码 → 最多 65 536 次。  
  - 对每个掩码构建图并做一次拓扑排序，节点数 ≤ 2k ≤ 32，边数 ≤ 3·|words| ≤ 768。  
  - 拓扑排序的时间是 `O(V + E)`，这里是常数级。  
  - **总体**：`O(2^k · (k + |words|))` ≈ `O(2^16 · 256) ≈ 1.6×10⁷` 操作，完全可以在一秒内跑完。  

- **空间复杂度**  
  - 图的邻接表最多 `2k` 个列表，合计 `O(k + |words|)`，即几百个整数。  
  - 额外的 `indeg`、`queue` 等也是 `O(k)`。  
  - 整体 `O(k + |words|)`，非常小。

> **大白话解释**：  
> `O(2^k·(k+|words|))` 就是“先把每个字符是否要出现两次的 2ⁿ 种可能全部尝一遍（最多 65536 次），每次只做一次很快的检查（几十步）”。相当于把所有可能的“复制方案”一次性列出来检查，算得快，因为每次检查的工作量极小。

---

## 心得  

- **核心技巧**：把 “每个长度为 2 的单词必须保持相对顺序” 转化为 **有向图的拓扑约束**，并通过 **枚举字符是否需要复制**（最多两次）来消除环路。  
- **适用的题型**  
  1. **最短公共超序列**（尤其是所有子序列长度固定为 2 的情况）。  
  2. **字符出现次数受限的序列重建**，如 “每个字符最多出现 k 次” 的约束问题。  
  3. **基于相对顺序的排列计数**，比如 “给定若干对 (a,b) 必须 a 在 b 前，求所有合法排列”。  
- **一句话总结解题钥匙**：**把顺序要求抽象成有向图，枚举最少的“复制节点”使图无环，即得到所有最短超序列的频率**。

---

## 反思  

- **第一反应**：看到 “每个单词长度为 2”，立刻想到把每个单词当成一条有向边，构造图。随后想到了“是否有环”决定是否需要复制字符。  
- **最容易踩的坑**  
  1. **忘记“复制后只能在后面使用”**：在构造复制图时一定不能加入 `second_u → first_v` 的边，否则会错误地允许 “第二次 u 在第一次 v 前”。  
  2. **错误的长度计算**：最短长度不是所有字符出现一次的长度，而是 `distinct_chars + number_of_copied_chars`。  
  3. **遗漏去重**：不同拓扑序对应的字符串是排列的关系，它们的频率数组完全相同，只需要保留一次。  
- **下次类似题目第一步**：**先把所有“先后关系”抽象成有向图**，判断是否已有拓扑序；若不存在，则考虑 **最小化复制/拆分节点** 使图变成 DAG（通常可以通过位掩码枚举、位运算或动态规划实现）。