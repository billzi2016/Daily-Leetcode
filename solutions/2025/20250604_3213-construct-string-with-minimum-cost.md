# #3213. 构造最小成本字符串 / Construct String with Minimum Cost

> 难度：困难 · 标签：Array、String、Dynamic Programming、Suffix Array · [LeetCode 链接](https://leetcode.com/problems/construct-string-with-minimum-cost/)

---

## 题目（英文原版）

**Description**

You are given a string target, an array of strings words, and an integer array costs, both arrays of the same length.
Imagine an empty string s.
You can perform the following operation any number of times (including zero):
Return the minimum cost to make s equal to target. If it's not possible, return -1.

**Examples**

**Example 1:**

```
Input: target = "abcdef", words = ["abdef","abc","d","def","ef"], costs = [100,1,1,10,5]
Output: 7
Explanation:
The minimum cost can be achieved by performing the following operations:
```

**Example 2:**

```
Input: target = "aaaa", words = ["z","zz","zzz"], costs = [1,10,100]
Output: -1
Explanation:
It is impossible to make s equal to target , so we return -1.
```

**Constraints**

- 1 <= target.length <= 5 * 104
- 1 <= words.length == costs.length <= 5 * 104
- 1 <= words[i].length <= target.length
- The total sum of words[i].length is less than or equal to 5 * 104.
- target and words[i] consist only of lowercase English letters.
- 1 <= costs[i] <= 104

---

## 题目（中文翻译）

给定一个字符串 `target`、一个字符串数组 `words`，以及一个整数数组 `costs`，`words` 与 `costs` 长度相同。  
设想一个空字符串 `s`。  
你可以任意次数（包括零次）执行以下操作：

（题目原文中省略了具体操作的描述，此处保留原句）

返回使 `s` 等于 `target` 的最小成本。如果无法实现，返回 `-1`。

**示例 1**  
**输入**  
```text
target = "abcdef", words = ["abdef","abc","d","def","ef"], costs = [100,1,1,10,5]
```  
**输出**  
```text
7
```  
**解释**  
可以通过以下操作获得最小成本：

（此处省略具体操作步骤，保留原题结构）

**示例 2**  
**输入**  
```text
target = "aaaa", words = ["z","zz","zzz"], costs = [1,10,100]
```  
**输出**  
```text
-1
```  
**解释**  
无法将 `s` 构造为 `target`，因此返回 `-1`。

**约束条件**  
- `1 <= target.length <= 5 * 10^4`
- `1 <= words.length == costs.length <= 5 * 10^4`
- `1 <= words[i].length <= target.length`
- 所有 `words[i].length` 的总和 ≤ `5 * 10^4`
- `target` 与 `words[i]` 仅由小写英文字母组成
- `1 <= costs[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把目标串 `target` 看成若干段**，每段都要恰好匹配 `words` 中的某个单词，然后把对应的费用相加，取最小值。  

我们可以用 **动态规划** 来描述这个过程：

- `dp[i]` 表示把 `target[0:i]`（左闭右开区间）拼成的最小费用。  
- 初始 `dp[0] = 0`（空串不需要费用），其余位置先设为无穷大（表示不可达）。  
- 对每一个位置 `i`（0 ≤ i < len(target)），遍历所有单词 `words[j]`：  
  - 如果 `target[i : i + len(words[j])]` 正好等于 `words[j]`，说明可以把这段单词接在已经拼好的 `target[0:i]` 之后。  
  - 那么就尝试用 `dp[i] + costs[j]` 来更新 `dp[i + len(words[j])]`。  

> **类比**：把 `dp` 想成一条路上的里程碑，`dp[i]` 是到达第 `i` 坐标的最省油的方式。每次我们检查所有“加油站”（单词），如果能正好在当前位置加油，就算上油费（成本），看看能否走得更远且更省油。

**为什么正确**：  
动态规划的状态转移枚举了所有可能的拼接方式，只要一种合法的拼接能够覆盖整个 `target`，对应的费用必然会在 `dp[len(target)]` 中出现，并且因为我们始终取最小值，最终得到的就是最小成本。

#### 代码（Python）

```python
def min_cost_bruteforce(target: str, words: list[str], costs: list[int]) -> int:
    n = len(target)
    INF = 10**18                     # 表示“不可达”
    dp = [INF] * (n + 1)
    dp[0] = 0                         # 空串的费用为 0

    # 为了加速比较，预先把每个单词的长度记下来
    word_len = [len(w) for w in words]

    for i in range(n):
        if dp[i] == INF:              # 当前位置不可达，直接跳过
            continue
        # 枚举所有单词，尝试从位置 i 开始匹配
        for w, c, l in zip(words, costs, word_len):
            if i + l > n:              # 越界，不能匹配
                continue
            if target[i:i + l] == w:   # 字符串相等，合法拼接
                # 用 dp[i]（到达 i 的最小费用）加上本次单词的费用 c
                dp[i + l] = min(dp[i + l], dp[i] + c)

    return dp[n] if dp[n] != INF else -1
```

> 关键行中文注释已写在代码里，直接可以运行。

#### 复杂度  

- **时间复杂度**：`O(N * M * L)`  
  - `N = len(target)`，`M = len(words)`，`L` 为单词平均长度。  
  - 对每个位置 `i`（最多 `N` 次）我们要遍历全部单词（`M` 次），并且比较子串（`L` 次）。  
  - 用大白话说，就是 **“每走一步都要把所有单词逐个比一遍”**，所以会比较慢，尤其当 `target` 与 `words` 都很长时会超时。

- **空间复杂度**：`O(N)`  
  - 只用了长度为 `N+1` 的 DP 数组，其余都是常数级别的辅助空间。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次都要遍历全部单词并做字符串比较**。如果能在一次线性扫描 `target` 的过程中，快速得到**所有以当前位置结束的单词**，就可以把 `M` 的因子去掉。

这正是 **多模式匹配** 经典数据结构 **Aho‑Corasick 自动机**（Trie + 失配指针）擅长的事：

1. **构建 Trie**  
   把所有单词插入一棵字典树（Trie），每个节点对应一个前缀。  
   - 类比：Trie 就像一本“前缀字典”，每走一步就往下翻一页，走到叶子时恰好拼出了一个完整单词。

2. **添加失配指针（fail 链）**  
   当在 `target` 中匹配时，遇到字符不在当前节点的子树里，就沿着 “失配指针” 跳到下一个可能的匹配状态，继续比较。  
   - 类比：失配指针相当于“回退到上一次还能继续匹配的最近字典页”，避免重新从根开始。

3. **记录每个终止节点对应的单词费用**  
   同一个终止节点可能对应多个单词（例如 `"ab"` 与 `"b"`），我们把它们的费用保存在列表中，遍历时一次性取出全部。

4. **动态规划 + 自动机扫描**  
   - `dp[i]` 同样表示 `target[:i]` 的最小费用。  
   - 我们从左到右遍历 `target`，在自动机中实时更新当前状态 `node`。  
   - 每当 `node`（或沿着 `fail` 链向上）是 **终止节点** 时，说明有若干单词在当前位置 **结束**。  
     对于每个单词长度 `l`（等于单词的字符数），我们尝试用 `dp[i - l] + cost` 来更新 `dp[i]`。  

这样，**每个字符只被处理常数次**（一次前进，一次或多次沿 fail 链遍历终止节点），总体时间是线性的。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

INF = 10**18


class AhoCorasick:
    """Aho‑Corasick 自动机，只实现本题需要的功能"""
    def __init__(self):
        # 每个节点的 children: dict(char -> node_index)
        self.children = [defaultdict(lambda: -1)]
        # fail 指针
        self.fail = [-1]
        # 输出列表，存放 (word_length, cost) 的元组
        self.output = [[]]

    def add_word(self, word: str, cost: int):
        node = 0
        for ch in word:
            nxt = self.children[node][ch]
            if nxt == -1:                     # 不存在则新建节点
                self.children.append(defaultdict(lambda: -1))
                self.fail.append(-1)
                self.output.append([])
                nxt = len(self.children) - 1
                self.children[node][ch] = nxt
            node = nxt
        # 到达终止节点，记录该单词的长度和费用
        self.output[node].append((len(word), cost))

    def build(self):
        """构建 fail 指针（层序遍历）"""
        q = deque()
        # 根节点的子节点 fail 指向根
        for ch, nxt in self.children[0].items():
            if nxt != -1:
                self.fail[nxt] = 0
                q.append(nxt)

        while q:
            cur = q.popleft()
            for ch, nxt in self.children[cur].items():
                if nxt == -1:
                    continue
                # 找到 cur 的 fail 节点的对应转移
                f = self.fail[cur]
                while f != -1 and self.children[f][ch] == -1:
                    f = self.fail[f]
                self.fail[nxt] = self.children[f][ch] if f != -1 else 0
                # 合并输出：如果 fail 指向的节点也是终止节点，需要把它的输出也加进来
                self.output[nxt].extend(self.output[self.fail[nxt]])
                q.append(nxt)

    def next_state(self, state: int, ch: str) -> int:
        """在当前状态 state 下读取字符 ch，返回新的状态"""
        while state != -1 and self.children[state][ch] == -1:
            state = self.fail[state]
        return self.children[state][ch] if state != -1 else 0


def min_cost_aho(target: str, words: List[str], costs: List[int]) -> int:
    n = len(target)
    dp = [INF] * (n + 1)
    dp[0] = 0

    # 1. 建立自动机
    ac = AhoCorasick()
    for w, c in zip(words, costs):
        ac.add_word(w, c)
    ac.build()

    state = 0  # 当前在自动机中的节点
    for i, ch in enumerate(target, 1):      # i 从 1 开始，表示 target[:i] 的长度
        state = ac.next_state(state, ch)    # 读取第 i 个字符，更新状态

        # 2. 检查所有以 i 结尾的单词（沿着 output 列表）
        for length, cost in ac.output[state]:
            # dp[i - length] 必须是可达的
            if dp[i - length] != INF:
                dp[i] = min(dp[i], dp[i - length] + cost)

    return dp[n] if dp[n] != INF else -1
```

> 代码已完整注释，直接拷贝运行即可。

#### 复杂度  

- **时间复杂度**：`O(N + Σ|words[i]| + K)`  
  - `N = len(target)`，一次线性扫描。  
  - `Σ|words[i]|` 是所有单词长度之和（≤ 5·10⁴），用于构建 Trie。  
  - `K` 为匹配过程中产生的输出次数（即每个单词在 `target` 中出现的次数），总的也不会超过 `N * √Σ|words|` 之类的线性量。  
  - 用大白话说，就是 **“一次遍历目标串，所有单词的处理都被提前压在字典树里，一次性搞定”**，远快于暴力的 `N * M`。

- **空间复杂度**：`O(Σ|words[i]| + N)`  
  - Trie 需要存储所有字符节点（即所有单词的总长度）。  
  - DP 数组需要 `O(N)`。  

---

## 心得  

- **核心技巧**：利用 **Aho‑Corasick 多模式匹配** 把“所有单词的匹配”一次性完成，再配合**动态规划**求最小费用。  
- **适用的题型**（类似思路）  
  1. “给定若干单词，统计它们在一段文本中出现的次数”——典型的多模式匹配。  
  2. “在字符串上做若干替换或拼接，要求最小代价”——需要先快速定位所有可行的子串。  
  3. “在大文本中找出所有以字典中单词结尾的位置”——同样可以用 Aho‑Corasick + DP。  
- **一句话总结**：**把所有候选子串一次性预处理（Trie + fail），再用 DP 把每一步的最优代价串起来**。

---

## 反思  

- **第一反应**：看到“把空串变成 target，能随意插入 words”，立刻想到**区间 DP** 或**背包**，于是写了遍历所有单词的 O(N·M) 暴力 DP。  
- **最容易踩的坑**  
  - **超时**：`target` 与 `words` 都可能长到 5·10⁴，暴力遍历会爆炸。  
  - **忘记合并输出**：在 Aho‑Corasick 中，某个节点的 `fail` 可能也是终止节点，需要把它的输出也加入，否则会漏掉包含在更长单词内部的短单词。  
  - **边界条件**：`dp[0] = 0` 必须初始化，且在更新时要检查 `dp[i - length]` 是否可达（不等于 INF），否则会产生错误的负数或溢出。  
- **下次遇到同类题**：**第一步先判断是否需要快速找出所有子串匹配**——如果是，立刻想到构造 **Trie + Aho‑Corasick**（或哈希+滚动哈希）来把匹配过程降到线性。随后再结合 DP/贪心等求最优解。