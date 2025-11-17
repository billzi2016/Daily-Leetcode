# #3425. 最长特殊路径 / Longest Special Path

> 难度：困难 · 标签：Array、Hash Table、Tree、Depth-First Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/longest-special-path/)

---

## 题目（英文原版）

**Description**

You are given an undirected tree rooted at node 0 with n nodes numbered from 0 to n - 1, represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi, lengthi] indicates an edge between nodes ui and vi with length lengthi. You are also given an integer array nums, where nums[i] represents the value at node i.
A special path is defined as a downward path from an ancestor node to a descendant node such that all the values of the nodes in that path are unique.
Note that a path may start and end at the same node.
Return an array result of size 2, where result[0] is the length of the longest special path, and result[1] is the minimum number of nodes in all possible longest special paths.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], nums = [2,1,2,1,3,1]
Output: [6,2]
Explanation:

The longest special paths are 2 -> 5 and 0 -> 1 -> 4 , both having a length of 6. The minimum number of nodes across all longest special paths is 2.
```

**Example 2:**

```
Input: edges = [[1,0,8]], nums = [2,2]
Output: [0,1]
Explanation:

The longest special paths are 0 and 1 , both having a length of 0. The minimum number of nodes across all longest special paths is 1.
```

**Constraints**

- 2 <= n <= 5 * 104
- edges.length == n - 1
- edges[i].length == 3
- 0 <= ui, vi < n
- 1 <= lengthi <= 103
- nums.length == n
- 0 <= nums[i] <= 5 * 104
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

**描述**  
给定一棵以节点 `0` 为根的无向树，树中有 `n` 个节点，编号为 `0` 到 `n-1`，用长度为 `n-1` 的二维数组 `edges` 表示，其中 `edges[i] = [ui, vi, lengthi]` 表示节点 `ui` 与节点 `vi` 之间有一条长度为 `lengthi` 的边。另给定整数数组 `nums`，其中 `nums[i]` 表示节点 `i` 的取值。

**特殊路径（special path）** 定义为一条从祖先节点到其后代节点的向下路径，且该路径上所有节点的取值互不相同。路径可以起点与终点相同，即只包含一个节点。

返回长度为 `2` 的数组 `result`，其中 `result[0]` 为最长特殊路径的总长度，`result[1]` 为所有可能的最长特殊路径中节点数量的最小值。

---

**示例 1**  
```text
Input: edges = [[0,1,2],[1,2,3],[1,3,5],[1,4,4],[2,5,6]], nums = [2,1,2,1,3,1]
Output: [6,2]
Explanation:
最长的特殊路径有两条：2 -> 5 和 0 -> 1 -> 4，它们的长度都是 6。所有最长特殊路径中节点数量的最小值为 2。
```

**示例 2**  
```text
Input: edges = [[1,0,8]], nums = [2,2]
Output: [0,1]
Explanation:
最长的特殊路径是节点 0 或节点 1 本身，长度均为 0。所有最长特殊路径中节点数量的最小值为 1。
```

**约束条件**  
- `2 <= n <= 5 * 10^4`  
- `edges.length == n - 1`  
- `edges[i].length == 3`  
- `0 <= ui, vi < n`  
- `1 <= lengthi <= 10^3`  
- `nums.length == n`  
- `0 <= nums[i] <= 5 * 10^4`  
- 输入保证 `edges` 构成一棵合法的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把树看成一张“地图”，我们想找 **从上往下的连续路线**（祖先 → 后代），并且这条路上出现的数字都不相同。  
最直接的想法是：

1. 以每个节点 `i` 为起点，向下深度优先搜索（DFS）所有可能的后代。  
2. 在搜索的过程中维护一个 `set`（相当于查字典），把已经走过的节点值存进去，遇到重复的值就必须停止向下走。  
3. 同时累计走过的边的长度，记录下每条合法路径的长度和节点数，更新全局的最大长度和对应的最小节点数。

> **类比**：`set` 就像一本词典，`key` 是单词（这里是节点的值），`value` 是页码（这里我们只关心是否出现过）。只要在词典里找不到这个单词，就可以继续往下走。

只要把 **所有** 起点都遍历一遍，所有合法的向下路径都会被枚举到，答案自然可以得到。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple

def longestSpecialPath_bruteforce(edges: List[List[int]], nums: List[int]) -> List[int]:
    n = len(nums)
    # 建立邻接表，存 (邻居, 边长)
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    best_len = 0          # 当前已知的最长路径长度
    best_cnt = 1          # 对应的最小节点数（单节点长度为 0）

    # ---------- 以 start 为起点的 DFS ----------
    def dfs(cur: int, parent: int, cur_len: int,
            seen: set, cnt: int) -> None:
        """
        cur      : 当前所在的节点编号
        parent   : 防止回到父节点
        cur_len  : 从 start 到 cur 累计的边长
        seen     : 当前路径上已经出现的节点值集合
        cnt      : 当前路径的节点数量
        """
        nonlocal best_len, best_cnt

        # 先更新答案
        if cur_len > best_len or (cur_len == best_len and cnt < best_cnt):
            best_len, best_cnt = cur_len, cnt

        # 向下继续搜索
        for nxt, w in g[cur]:
            if nxt == parent:          # 不能回到已经走过的父节点
                continue
            val = nums[nxt]
            if val in seen:            # 出现重复值，不能再往这条路走了
                continue
            seen.add(val)
            dfs(nxt, cur, cur_len + w, seen, cnt + 1)
            seen.remove(val)           # 回溯，撤销对 nxt 的记录

    # 对每个节点都当作起点尝试一次
    for start in range(n):
        seen = {nums[start]}          # 起点本身已经占用
        dfs(start, -1, 0, seen, 1)

    return [best_len, best_cnt]
```

> 关键行的中文注释已写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个节点都要遍历它下面的所有后代，最坏情况下树是链状的，第一层要走 `n` 步，第二层 `n‑1` 步 …，总和约为 `n·(n+1)/2 ≈ n²/2`。  
  - 大白话：如果有 10,000 个节点，最慢可能要做 100,000,000 次“检查”，这对 5×10⁴ 的数据量已经吃不消了。

- **空间复杂度**：`O(n)`  
  - 递归栈最深可能是 `n`（链状树），另外 `set` 最多保存 `n` 个不同的值。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都从头重新遍历整条路径**。其实我们在一次深度优先遍历（从根到叶子）时，就可以把“最近一次出现相同值的节点”记下来，这样每到一个新节点，就能 **立刻算出** 以它为终点的最长合法向下路径，而不必重新遍历。

核心思路：

1. **前缀和**  
   - `pref[i]` 记录从根到当前路径第 `i` 个节点（0‑based）累计的边长。  
   - 两个节点之间的距离 = `pref[j] - pref[i-1]`（`i ≤ j`），类似“区间和”。

2. **哈希表记录最近出现位置**  
   - 用字典 `last[value] = idx` 保存 **当前遍历路径** 中该值最近出现的下标 `idx`（0 表示根）。  
   - 当来到新节点 `cur`（下标 `idx`）时，若它的值之前出现过，最近的冲突位置就是 `last[value]`。  
   - 那么 **合法路径的起点** 必须在冲突位置的下一位：`start = last[value] + 1`（如果从未出现过，则 `last[value] = -1`，`start = 0`）。

3. **即时计算路径长度与节点数**  
   - 当前合法路径的长度 = `pref[idx] - pref[start-1]`（`start==0` 时前者直接为 `pref[idx]`）。  
   - 当前合法路径的节点数 = `idx - start + 1`。  
   - 与全局最佳比较，更新 `best_len` 与 `best_cnt`（相同长度时取更少节点数）。

4. **回溯恢复**  
   - DFS 结束后，需要把 `last[value]` 恢复到进入该节点前的状态（因为不同分支共享同一条哈希表）。  
   - 只要记住进入节点前的旧值 `prev`，退出时恢复即可。

整个过程只遍历一次树，所有操作都是 **O(1)**，于是整体是线性时间。

> **类比**：  
> - 前缀和就像在一本账本里记录“累计收入”。想知道第 5 天到第 8 天赚了多少，只要 `累计到第 8 天 - 累计到第 4 天` 就行了。  
> - `last` 哈希表像一本“最近一次出现的字典”，每次查询 “这个数字上次出现在哪？” 都是常数时间。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def longestSpecialPath_opt(edges: List[List[int]], nums: List[int]) -> List[int]:
    n = len(nums)
    # 1. 建图（邻接表），每条边保存 (邻居, 长度)
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    best_len = 0          # 当前最长路径长度
    best_cnt = 1          # 对应的最少节点数（单节点默认 1）

    path_vals = []        # 当前从根到节点的值序列，便于回溯
    pref_len = []         # 对应的前缀路径长度序列
    last = {}             # value -> 最近出现的下标（在 path_vals 中的索引）

    def dfs(cur: int, parent: int, edge_to_cur: int) -> None:
        """
        cur            : 当前访问的节点编号
        parent         : 防止回到已经遍历的父节点
        edge_to_cur    : 从父节点到 cur 的边长（根节点传 0）
        """
        nonlocal best_len, best_cnt

        # ---- 进入 cur 节点 ----
        idx = len(path_vals)                # 当前节点在路径中的下标
        # 更新前缀和：如果是根节点 idx==0，前缀长度为 0；否则累加 edge_to_cur
        cur_pref = (pref_len[-1] if pref_len else 0) + edge_to_cur
        path_vals.append(nums[cur])
        pref_len.append(cur_pref)

        # 记录进入之前该值的上一次出现位置（可能不存在）
        prev = last.get(nums[cur], -1)
        # 更新为最新出现位置
        last[nums[cur]] = idx

        # ---- 计算以 cur 为终点的最长合法向下路径 ----
        # 合法起点必须在上一次出现该值的后一位
        start = prev + 1                     # 0 <= start <= idx
        # 计算路径长度
        cur_len = cur_pref - (pref_len[start - 1] if start > 0 else 0)
        # 计算节点数
        cur_cnt = idx - start + 1

        # 更新全局答案
        if cur_len > best_len or (cur_len == best_len and cur_cnt < best_cnt):
            best_len, best_cnt = cur_len, cur_cnt

        # ---- 继续向子树遍历 ----
        for nxt, w in g[cur]:
            if nxt == parent:
                continue
            dfs(nxt, cur, w)

        # ---- 回溯：恢复状态 ----
        # 先把 last 恢复到进入 cur 前的状态
        if prev == -1:
            del last[nums[cur]]          # 说明在当前路径中第一次出现
        else:
            last[nums[cur]] = prev
        # 再弹出路径信息
        path_vals.pop()
        pref_len.pop()

    # 从根节点 0 开始 DFS，根节点没有入边长度，用 0 代替
    dfs(0, -1, 0)

    return [best_len, best_cnt]
```

> 代码中每一行都配有中文注释，直接复制运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只进入一次、退出一次，所有字典、列表操作都是 `O(1)`。  
  - 与暴力的 `n²` 相比，线性时间在 5×10⁴ 的规模下毫无压力。

- **空间复杂度**：`O(n)`  
  - 递归栈深度最坏为 `n`（链状树），`path_vals`、`pref_len`、`last` 最多存 `n` 条记录。  

---

## 心得

- **核心技巧**：在 **从根到当前节点的唯一值窗口** 上维护「最近一次出现位置」 + 「前缀路径长度」的双重信息。  
- **适用题型**（类似思路）：
  1. **树上最长不重复值路径**（本题的变形）。  
  2. **数组/字符串中最长不重复子序列**（滑动窗口 + 哈希表）。  
  3. **带权图中满足某种约束的最长路径**（使用前缀和 + 最近冲突位置）。  
- **一句话总结解题钥匙**：`前缀和 + 哈希表记录最近冲突 → O(1) 直接算出每个节点的最佳起点`。

---

## 反思

- **第一反应**：把每条可能的向下路径都枚举出来，用 `set` 检查是否有重复。  
- **最容易踩的坑**  
  1. **回溯时忘记恢复 `last`**，导致不同分支之间共享了错误的最近出现位置。  
  2. **根节点的前缀长度** 必须是 `0`（因为没有入边），否则会把根到根的长度算成非零。  
  3. **长度为 0 的路径**（单节点）同样是合法的，需要在答案初始化时考虑 `best_cnt = 1`。  
- **下次遇到同类题**：第一步先想「**在一次遍历中把所有需要的历史信息保存下来**」——比如「最近出现位置」或「最小/最大前缀」等，这往往能把原本的 `O(n²)` 暴力直接降到 `O(n)`。