# #756. **金字塔转移矩阵** / Pyramid Transition Matrix

> 难度：中等 · 标签：Bit Manipulation、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/pyramid-transition-matrix/)

---

## 题目（英文原版）

**Description**

You are stacking blocks to form a pyramid. Each block has a color, which is represented by a single letter. Each row of blocks contains one less block than the row beneath it and is centered on top.
To make the pyramid aesthetically pleasing, there are only specific triangular patterns that are allowed. A triangular pattern consists of a single block stacked on top of two blocks. The patterns are given as a list of three-letter strings allowed, where the first two characters of a pattern represent the left and right bottom blocks respectively, and the third character is the top block.
You start with a bottom row of blocks bottom, given as a single string, that you must use as the base of the pyramid.
Given bottom and allowed, return true if you can build the pyramid all the way to the top such that every triangular pattern in the pyramid is in allowed, or false otherwise.

**Examples**

**Example 1:**

```
Input: bottom = "BCD", allowed = ["BCC","CDE","CEA","FFF"]
Output: true
Explanation: The allowed triangular patterns are shown on the right.
Starting from the bottom (level 3), we can build "CE" on level 2 and then build "A" on level 1.
There are three triangular patterns in the pyramid, which are "BCC", "CDE", and "CEA". All are allowed.
```

**Example 2:**

```
Input: bottom = "AAAA", allowed = ["AAB","AAC","BCD","BBE","DEF"]
Output: false
Explanation: The allowed triangular patterns are shown on the right.
Starting from the bottom (level 4), there are multiple ways to build level 3, but trying all the possibilites, you will get always stuck before building level 1.
```

**Constraints**

- 2 <= bottom.length <= 6
- 0 <= allowed.length <= 216
- allowed[i].length == 3
- The letters in all input strings are from the set {'A', 'B', 'C', 'D', 'E', 'F'}.
- All the values of allowed are unique.

---

## 题目（中文翻译）

你正在堆叠方块构建金字塔。每个方块都有一种颜色，用单个字母表示。金字塔的每一层比其下方的层少一个方块，并且居中放置。

为了使金字塔美观，只允许出现特定的**三角形模式（triangular pattern）**。一个三角形模式由一个方块放在两个方块之上组成。所有允许的模式以长度为 3 的字符串列表形式给出，其中前两个字符分别表示左下和右下的方块，第三个字符表示顶部的方块。

已知底层方块 `bottom`（以字符串形式给出），你必须以它为金字塔的基座。给定 `bottom` 和 `allowed`，如果能够构建出完整的金字塔，使得金字塔中的每一个三角形模式都在 `allowed` 中，则返回 `true`；否则返回 `false`。

---

### 示例

**示例 1**

```text
Input: bottom = "BCD", allowed = ["BCC","CDE","CEA","FFF"]
Output: true
```

**解释**：右侧展示了允许的三角形模式。  
从底层（第 3 层）开始，我们可以在第 2 层构造出 `"CE"`，随后在第 1 层构造出 `"A"`。  
金字塔中共有三个三角形模式，分别是 `"BCC"`、`"CDE"` 和 `"CEA"`，全部都在 `allowed` 中。

**示例 2**

```text
Input: bottom = "AAAA", allowed = ["AAB","AAC","BCD","BBE","DEF"]
Output: false
```

**解释**：右侧展示了允许的三角形模式。  
从底层（第 4 层）开始，虽然第 3 层有多种构造方式，但尝试所有可能后，都会在构造第 1 层之前卡住，无法完成金字塔。

---

### 约束条件

- `2 <= bottom.length <= 6`
- `0 <= allowed.length <= 216`
- `allowed[i].length == 3`
- 所有输入字符串中的字母均来自集合 `{ 'A', 'B', 'C', 'D', 'E', 'F' }`
- `allowed` 中的所有值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是：**在给定的底层字符串 `bottom` 上，一层层往上堆叠，直到只剩一个字符。如果每一次堆叠的三元组都在 `allowed` 列表里，就返回 `true`，否则返回 `false`。**  

最直接的想法是**把所有可能的堆叠方式全部枚举出来**，只要找到一种合法的堆叠路径，就可以提前结束。  
这属于典型的“**回溯（Backtracking）**”思路：

1. **把 `allowed` 转成查询表**  
   - 用一个哈希表（Python 的 `dict`）记录每一种底部两字符对应的所有可能的顶部字符。  
   - 类比：哈希表就像一本字典，左边的两个字母是“词”，对应的顶部字母是“解释”。查一次可以直接得到所有合法解释。

2. **从底层往上一层层递归**  
   - 给定当前层的字符串 `cur`（比如 `"BCD"`），先枚举第 `i`、`i+1` 两个字符能堆出哪些顶部字符。  
   - 把所有位置的候选顶部字符组合成 **下一层的所有可能字符串**（例如 `"BCD"` 下面可以得到 `"CE"`，再往上得到 `"A"`）。  
   - 对每一种可能的下一层字符串递归地继续向上尝试。  
   - 只要递归最终走到只剩一个字符，就说明找到了合法的金字塔，返回 `True`。

3. **剪枝**  
   - 如果在某一步发现某对底部字符在 `allowed` 中找不到任何合法的顶部字符，说明这条路径不可能成功，立刻回溯。

> 为什么这个方法一定正确？  
> 因为我们**没有遗漏任何一种合法的堆叠方式**——每一次都把所有可能的顶部字符列举出来并继续往上尝试，等价于在搜索一棵完整的决策树，只要树中有一条从根到叶子满足条件的路径，就一定会被遍历到。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def pyramidTransition(bottom: str, allowed: List[str]) -> bool:
    # ---------- 1. 把 allowed 建成查询表 ----------
    # key: 两个底部字符 (e.g., "AB")
    # value: 所有可以放在它上面的字符列表 (e.g., ["C","D"])
    nxt = defaultdict(list)
    for triple in allowed:
        pair, top = triple[:2], triple[2]
        nxt[pair].append(top)          # 哈希表的写法，O(1) 插入

    # ---------- 2. 深度优先搜索 ----------
    def dfs(cur: str) -> bool:
        # 已经堆到顶点，说明成功
        if len(cur) == 1:
            return True

        # 生成下一层所有可能的字符串集合
        candidates = []                # 每个位置的候选字符列表
        for i in range(len(cur) - 1):
            pair = cur[i:i+2]
            if pair not in nxt:        # 这对底部没有合法顶部，直接失败
                return False
            candidates.append(nxt[pair])

        # ---------- 3. 递归枚举所有组合 ----------
        # 使用回溯把每个位置的候选字符拼成完整的下一层字符串
        def backtrack(idx: int, path: List[str]) -> bool:
            if idx == len(candidates):            # 已经拼完一整层
                next_row = "".join(path)
                return dfs(next_row)               # 继续往上搜索
            for ch in candidates[idx]:            # 当前位置的每一种选择
                path.append(ch)
                if backtrack(idx + 1, path):      # 只要有一种成功就返回 True
                    return True
                path.pop()                         # 撤销选择，尝试下一个
            return False

        return backtrack(0, [])

    return dfs(bottom)
```

#### 复杂度

- **时间复杂度：**  
  对每一层我们都要枚举所有可能的顶部字符组合。设底层长度为 `n (≤6)`，每对底部字符最多有 `k`（`k ≤ 6`）种可能的顶部字符。第 `i` 层的宽度是 `n-i`，因此该层的组合数最多是 `k^{(n-i)}`。整体上最坏情况是遍历整棵决策树，时间复杂度约为 `O(k^{n})`。  
  大白话：如果每一次都有 6 种选择，底层 6 个字符的话，最坏会尝试 `6⁶ ≈ 46,656` 种堆叠方式，仍然在可以接受的范围。

- **空间复杂度：**  
  - 哈希表 `nxt` 保存所有 `allowed`，最多 `216` 条，空间 `O(216)`（常数）。  
  - 递归深度最多 `n-1 ≤ 5`，每层保存一个长度不超过 `n` 的字符串，空间 `O(n²)`，实际也很小。  

---

### 2. 最优解

#### 思路  

在本题的约束下（`bottom.length ≤ 6`），**暴力回溯已经足够快**，没有更低的渐进复杂度可以做到。不过，我们仍可以从“暴力”出发，进一步**减少不必要的重复搜索**，让代码更简洁、更具可读性。

关键的优化点：

1. **提前剪枝**  
   - 在递归进入下一层之前，先检查当前层的每一对底部字符是否都有合法的顶部字符。只要有一对不合法，就不必继续生成组合。

2. **使用记忆化搜索（Memoization）**  
   - 同一层的字符串可能会在不同路径上出现多次（例如 `"ABC"` 可能由不同的底层组合得到）。如果我们已经尝试过这个字符串并得到了 `False`，再次遇到时可以直接返回 `False`，避免重复计算。  
   - 用一个 `set` 记录已经搜索过且失败的层字符串。

3. **改用 BFS（广度优先搜索）**  
   - 从底层开始，一层层往上 **层层展开**，把所有可能的下一层字符串放进队列。只要在某一层出现了长度为 `1` 的字符串，就说明成功。  
   - BFS 的优势是可以一次性看到同一层的所有状态，容易配合记忆化去重。

下面给出 **记忆化 DFS** 版本（在原始暴力的基础上加了 `visited` 集合），它是实际使用中最常见的“最优”实现。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Set

def pyramidTransition(bottom: str, allowed: List[str]) -> bool:
    # ---------- 1. 建立查询表 ----------
    nxt = defaultdict(list)
    for triple in allowed:
        pair, top = triple[:2], triple[2]
        nxt[pair].append(top)

    # ---------- 2. 记忆化集合 ----------
    visited: Set[str] = set()   # 记录已经尝试过且失败的层字符串

    # ---------- 3. 深度优先搜索（带记忆化） ----------
    def dfs(cur: str) -> bool:
        if len(cur) == 1:                # 已经堆到顶点
            return True
        if cur in visited:               # 之前已经搜索过，肯定失败
            return False

        # 生成每一对底部字符的候选顶部字符列表
        cand = []
        for i in range(len(cur) - 1):
            pair = cur[i:i+2]
            if pair not in nxt:           # 没有合法顶部，剪枝
                visited.add(cur)
                return False
            cand.append(nxt[pair])

        # 回溯拼接下一层字符串
        def backtrack(idx: int, path: List[str]) -> bool:
            if idx == len(cand):
                next_row = "".join(path)
                if dfs(next_row):         # 递归往上
                    return True
                return False
            for ch in cand[idx]:
                path.append(ch)
                if backtrack(idx + 1, path):
                    return True
                path.pop()
            return False

        result = backtrack(0, [])
        if not result:                    # 整条搜索树都没有成功，记下来
            visited.add(cur)
        return result

    return dfs(bottom)
```

#### 复杂度

- **时间复杂度：**  
  加入记忆化后，每个不同的层字符串只会被搜索一次。层字符串的数量上限为 `O(k^{n})`（同前面的分析），但实际会因为剪枝和记忆化大幅降低。最坏仍是 `O(k^{n})`，但常数更小。

- **空间复杂度：**  
  - 哈希表 `nxt`：`O(216)`（常数）。  
  - 记忆化集合 `visited`：最多保存所有可能的层字符串，数量同样是 `O(k^{n})`。  
  - 递归栈深度 `O(n)`。整体仍然是指数级的 **状态空间**，但因为 `n ≤ 6`，实际占用极小。

---

## 心得

- **核心技巧**：  
  使用 **哈希表快速定位合法的顶部字符** + **回溯（DFS）遍历所有堆叠路径**，并配合 **记忆化剪枝** 防止重复搜索。

- **适用的题型**  
  1. “字母三元组”或 “拼图” 类的组合约束问题（如 LeetCode 2078 `Find the Score of All Prefixes`）。  
  2. “从底向上逐层构造” 的 DP/DFS 题目（如 LeetCode 1120 `Maximum Average Subtree` 的层次遍历变体）。  
  3. 需要枚举所有可能状态并判断是否存在满足条件的路径的搜索题（如 LeetCode 79 `Word Search`）。

- **一句话总结解题钥匙**：  
  **把“每一对底部字符 → 所有可能的顶部字符”预处理成哈希表，再用记忆化 DFS/回溯把所有层层堆叠的组合遍历一遍**。

## 反思

- **第一反应**：看到“底层 → 顶层” 的层层堆叠，立刻想到 **递归枚举每一层的所有可能**，即回溯搜索。

- **最容易踩的坑**  
  1. **漏掉剪枝**：如果直接暴力枚举所有组合而不检查每对底部是否有合法顶部，会出现大量无意义的递归，导致超时。  
  2. **忘记记忆化**：同一层字符串可能在不同分支出现多次，未去重会导致指数级的重复计算。  
  3. **边界条件**：当 `allowed` 为空或底层长度为 1 时，需要直接返回 `False`/`True`，否则会出现 `KeyError`。

- **下次遇到同类题的第一步**：  
  **先把“局部合法性”抽象成哈希表（或类似的快速查询结构）**，然后判断是否可以从底层逐层向上“拼接”。如果可以，再考虑回溯或 BFS 加记忆化来搜索完整路径。