# #3331. 更改后子树大小 / Find Subtree Sizes After Changes

> 难度：中等 · 标签：Array、Hash Table、String、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/find-subtree-sizes-after-changes/)

---

## 题目（英文原版）

**Description**

You are given a tree rooted at node 0 that consists of n nodes numbered from 0 to n - 1. The tree is represented by an array parent of size n, where parent[i] is the parent of node i. Since node 0 is the root, parent[0] == -1.
You are also given a string s of length n, where s[i] is the character assigned to node i.
We make the following changes on the tree one time simultaneously for all nodes x from 1 to n - 1:
Return an array answer of size n where answer[i] is the size of the subtree rooted at node i in the final tree.

**Examples**

**Example 1:**

```
Input: parent = [-1,0,0,1,1,1], s = "abaabc"
Output: [6,3,1,1,1,1]
Explanation:
The parent of node 3 will change from node 1 to node 0.
```

**Example 2:**

```
Input: parent = [-1,0,4,0,1], s = "abbba"
Output: [5,2,1,1,1]
Explanation:
The following changes will happen at the same time:
```

**Constraints**

- n == parent.length == s.length
- 1 <= n <= 105
- 0 <= parent[i] <= n - 1 for all i >= 1.
- parent[0] == -1
- parent represents a valid tree.
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一棵以节点 0 为根的树，树中共有 n 个节点，编号为 0 到 n - 1。树通过大小为 n 的数组 parent 表示，其中 parent[i] 是节点 i 的父节点。由于 0 是根节点，满足 parent[0] == -1。

同时给定一个长度为 n 的字符串 s， s[i] 是分配给节点 i 的字符。

我们对树进行一次统一的修改，针对所有节点 x （1 ≤ x ≤ n - 1）同时执行下面的操作：

（题目原文中未给出具体的修改规则，此处保持原样）

返回大小为 n 的数组 answer，其中 answer[i] 是最终树中以节点 i 为根的子树（subtree）的大小。

**示例 1**  
**输入**: `parent = [-1,0,0,1,1,1]`, `s = "abaabc"`  
**输出**: `[6,3,1,1,1,1]`  
**解释**:  
节点 3 的父节点会从节点 1 改变为节点 0。

**示例 2**  
**输入**: `parent = [-1,0,4,0,1]`, `s = "abbba"`  
**输出**: `[5,2,1,1,1]`  
**解释**:  
以下修改会同时发生：

---

### 约束条件
- `n == parent.length == s.length`
- `1 <= n <= 10^5`
- `0 <= parent[i] <= n - 1` 对所有 `i >= 1` 成立
- `parent[0] == -1`
- `parent` 表示一棵有效的树
- `s` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个节点的所有祖先都枚举一遍**，找出最近的、字符和自己相同的祖先，然后把父节点改成它。  
实现步骤：

1. 先把 `parent` 数组转换成“子节点列表”，即一棵普通的树结构。  
2. 对每个节点 `x (1 … n‑1)`，从 `x` 往上沿 `parent` 一直走到根，检查 `s[ancestor] == s[x]`。  
3. 找到最近的满足条件的祖先 `y`（如果有），把 `x` 的父节点改成 `y`；否则保持原来的父节点。  
4. 改完所有节点后，再遍历一次新树，统计每个节点的子树大小（后序遍历即可）。

> **类比**：把树想象成公司组织结构，`parent[i]` 是员工 `i` 的直接上级。我们要把每位员工（除 CEO）“调动”到最近的、和自己兴趣相同的上级那里。暴力做法就是让每位员工不停往上找上级，直到找到兴趣相同的那位。

**为什么正确**  
因为题目要求的“同时”改动只影响父指针的最终值，而不影响查找过程——每个节点在决定新父亲时，只看原来的祖先关系。逐个枚举所有祖先正好满足这个要求。

**时间/空间复杂度**  

- 对每个节点最坏要向上遍历到根，时间是 `O(n²)`（想象一条链状树，第一层要走 `n` 步，第二层 `n‑1` 步……）。  
- 额外的存储只需要原树的子节点列表和答案数组，都是 `O(n)`。

> **大白话**：`O(n²)` 就像把 10 000 本书都从头读到尾，时间会很长；而 `O(n)` 只需要把每本书读一次，快多了。

#### 代码（Python）

```python
def subtreeSizes_bruteforce(parent, s):
    n = len(parent)

    # 1️⃣ 把 parent 转成子节点列表（邻接表）
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)

    # 2️⃣ 记录每个节点改完父亲后的新父亲
    new_parent = parent[:]                     # 先复制一份
    for x in range(1, n):
        cur = parent[x]
        while cur != -1:                       # 向上找祖先
            if s[cur] == s[x]:                 # 找到相同字符
                new_parent[x] = cur            # 改父亲
                break
            cur = parent[cur]                  # 继续往上

    # 3️⃣ 根据 new_parent 重新构造新树
    new_children = [[] for _ in range(n)]
    for i in range(1, n):
        new_children[new_parent[i]].append(i)

    # 4️⃣ 后序遍历求子树大小
    ans = [0] * n

    def dfs(u):
        size = 1                               # 包含自己
        for v in new_children[u]:
            size += dfs(v)
        ans[u] = size
        return size

    dfs(0)                                     # 根一定是 0
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 最坏情况下（链形树），每个节点向上遍历的步数是 `1 + 2 + … + (n‑1) = O(n²)`。  
- **空间复杂度**：`O(n)`  
  - 只用了几张长度为 `n` 的数组（子节点列表、答案等），与 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要从节点往上遍历整个祖先链**。  
我们可以在一次深度优先搜索（DFS）中**同步维护每个字符最近出现的祖先**，这样查询“最近的同字符祖先”可以在 **O(1)** 时间完成。

关键点：

1. **DFS 从根遍历原树**。在递归进入子节点前，记录当前路径上每个字符最近出现的节点。  
2. 用一个长度为 26 的数组 `last[26]`（下标对应 `'a'…'z'`），`last[c]` 保存 **当前 DFS 路径上** 最近出现字符 `c` 的节点编号，若不存在则为 `-1`。  
   - 这相当于 **哈希表**，只不过字符范围固定，用数组更快。  
   - 类比：`last` 就像一本字典，查字母 `c` 能立刻告诉你最近的那本书（节点）在哪。  
3. 对于正在访问的子节点 `v`（原树的孩子）：
   - 如果 `last[s[v]] != -1`，说明在它的祖先中已经出现过相同字符，**最近的** 那个就是 `last[s[v]]`，于是 `v` 的新父亲就是它。  
   - 否则，它没有同字符祖先，父亲保持原来的 `u`（当前 DFS 的节点）。  
   - 把这条新边加入 `new_children`（新树的邻接表）。  
4. 递归进入 `v` 前，先把 `v` 本身加入 `last`（因为它会成为后代的祖先），递归结束后恢复 `last`（相当于“弹栈”），保持路径信息的正确性。  
5. 完成一次 DFS，就能得到 **新树的结构**。随后再做一次后序 DFS，直接在新树上累计子树大小。

> **为什么是一次遍历就能搞定**  
> - 在 DFS 过程中，路径上所有已经访问过的节点就是当前节点的全部祖先。  
> - `last` 始终指向“最近一次出现”的同字符节点，正好对应题目要求的“最近的祖先”。  
> - 所以每个节点只做 **常数次** 操作，整体线性 `O(n)`。

#### 代码（Python）

```python
def findSubtreeSizes(parent, s):
    n = len(parent)
    # 1️⃣ 把原树转成邻接表（子节点列表）
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)

    # 2️⃣ 用来存新树的邻接表
    new_children = [[] for _ in range(n)]

    # 3️⃣ last[c] = 最近出现字符 c 的节点编号，-1 表示还没出现
    last = [-1] * 26

    # 4️⃣ 深度优先遍历原树，同时构造新树
    def dfs(u):
        # 把当前节点加入路径（供后代使用）
        idx = ord(s[u]) - ord('a')
        prev = last[idx]          # 记住之前的值，稍后要恢复
        last[idx] = u

        # 处理所有原来的孩子
        for v in children[u]:
            # 看看在路径上是否已经出现过相同字符
            same_char_ancestor = last[ord(s[v]) - ord('a')]
            if same_char_ancestor != -1:               # 有同字符祖先
                new_parent = same_char_ancestor
            else:                                      # 没有，保持原父亲
                new_parent = u
            new_children[new_parent].append(v)        # 在新树里加边

            dfs(v)                                     # 递归处理子树

        # 退出当前节点时恢复 last 的状态（相当于出栈）
        last[idx] = prev

    dfs(0)                     # 从根节点开始

    # 5️⃣ 再一次后序遍历新树，计算子树大小
    ans = [0] * n

    def calc(u):
        size = 1
        for v in new_children[u]:
            size += calc(v)
        ans[u] = size
        return size

    calc(0)
    return ans
```

**代码要点注释（已在代码中）**：

- `last` 类似 “字典”，下标是字符，值是最近出现的节点。  
- `prev` 用来**保存并恢复**，保证在回到父节点时路径信息不被污染。  
- `new_children` 记录**最终**的树结构，后面再用它算子树大小。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只进入一次 `dfs`、一次 `calc`，每次只做常数时间的操作。  
  - 与暴力的 `O(n²)` 相比，快了几个数量级。  
- **空间复杂度**：`O(n)`  
  - 存储原树和新树的邻接表各 `O(n)`，以及 `last`、递归栈等均为线性。  

---

## 心得  

- **核心技巧**：在一次深度优先搜索中维护“路径上最近出现的每种字符的节点”。  
- **适用场景**：  
  1. **最近相同属性的祖先**（如字符、颜色、值）查询——比如 “在树上找最近相同颜色的祖先”。  
  2. **路径上信息的快速查询**——如“最近出现的奇数值节点”。  
  3. **同时变更结构但不影响查询**——先在原结构上完成所有决定，再构造新结构。  
- **一句话总结解题钥匙**：*把“往上找最近同字符”转化为“在 DFS 过程中实时记录每种字符的最近出现”，从而把二次遍历降到一次线性遍历*。

---

## 反思  

- **第一反应**：直接遍历每个节点的所有祖先（暴力），因为最直观。  
- **最容易踩的坑**  
  1. **同时改动的误解**：有些人会在处理子节点时就使用已经改动后的父指针，导致后代找不到正确的祖先。正确做法是**始终依据原始树的祖先关系**，只在最后一步构造新树。  
  2. **恢复状态**：在 DFS 中记录 `last` 时忘记回溯会导致后面的节点误认为已经出现的字符。一定要在递归返回前把 `last` 恢复到进入该节点之前的状态。  
  3. **字符映射**：直接用 `dict` 也行，但因为字符固定为 26 种，用数组会更快、更省空间。  
- **下次遇到同类题**：第一步先思考“在遍历路径上需要快速获取某类信息吗？”，如果答案是“是”，就尝试用**路径状态数组/栈**在一次 DFS 中维护这些信息。这样往往能把 `O(n²)` 降到 `O(n)`。