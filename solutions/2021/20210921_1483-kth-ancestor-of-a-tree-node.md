# #1483. 树节点的第 K 代祖先 / Kth Ancestor of a Tree Node

> 难度：困难 · 标签：Binary Search、Dynamic Programming、Tree、Depth-First Search、Breadth-First Search、Design · [LeetCode 链接](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/)

---

## 题目（英文原版）

**Description**

You are given a tree with n nodes numbered from 0 to n - 1 in the form of a parent array parent where parent[i] is the parent of ith node. The root of the tree is node 0. Find the kth ancestor of a given node.
The kth ancestor of a tree node is the kth node in the path from that node to the root node.
Implement the TreeAncestor class:

**Examples**

**Example 1:**

```
Input
["TreeAncestor", "getKthAncestor", "getKthAncestor", "getKthAncestor"]
[[7, [-1, 0, 0, 1, 1, 2, 2]], [3, 1], [5, 2], [6, 3]]
Output
[null, 1, 0, -1]

Explanation
TreeAncestor treeAncestor = new TreeAncestor(7, [-1, 0, 0, 1, 1, 2, 2]);
treeAncestor.getKthAncestor(3, 1); // returns 1 which is the parent of 3
treeAncestor.getKthAncestor(5, 2); // returns 0 which is the grandparent of 5
treeAncestor.getKthAncestor(6, 3); // returns -1 because there is no such ancestor
```

**Constraints**

- 1 <= k <= n <= 5 * 104
- parent.length == n
- parent[0] == -1
- 0 <= parent[i] < n for all 0 < i < n
- 0 <= node < n
- There will be at most 5 * 104 queries.

---

## 题目（中文翻译）

给定一棵包含 `n` 个节点的树，节点编号为 `0` 到 `n-1`，以父节点数组 `parent` 的形式表示，其中 `parent[i]` 是第 `i` 个节点的父节点。树的根节点是 `0`。请找到指定节点的第 `k` 代祖先。

树节点的第 `k` 代祖先是指从该节点到根节点路径上第 `k` 个节点。

实现 `TreeAncestor` 类，使其能够高效地处理查询。

---

**示例 1**

```json
["TreeAncestor", "getKthAncestor", "getKthAncestor", "getKthAncestor"]
[[7, [-1, 0, 0, 1, 1, 2, 2]], [3, 1], [5, 2], [6, 3]]
```

输出：

```
[null, 1, 0, -1]
```

**解释**

```java
TreeAncestor treeAncestor = new TreeAncestor(7, [-1, 0, 0, 1, 1, 2, 2]);
treeAncestor.getKthAncestor(3, 1); // 返回 1，3 的父节点
treeAncestor.getKthAncestor(5, 2); // 返回 0，5 的祖父节点
treeAncestor.getKthAncestor(6, 3); // 返回 -1，6 没有第 3 代祖先
```

---

**约束条件**

- `1 <= k <= n <= 5 * 10^4`
- `parent.length == n`
- `parent[0] == -1`
- `0 <= parent[i] < n`，对所有 `0 < i < n` 均成立
- `0 <= node < n`
- 最多会有 `5 * 10^4` 次查询

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把查询当成“向上爬树”。  
- **数据结构**：只需要原始的 `parent` 数组。`parent[i]` 就像一本**字典**，词是节点编号，页码是它的父节点。  
- **做法**：给定 `node` 和 `k`，把 `node` 当作当前指针，循环 `k` 次，每次把指针换成它的父节点 `parent[node]`。如果在某一步指针已经是 `-1`（根的父亲），说明已经爬到树根上了，再往上也不可能，有答案 `-1`。  
- **正确性**：因为每一次循环都严格沿着“从子到父”的唯一路径前进，恰好走了 `k` 步后指向的就是第 `k` 个祖先（如果不存在则是 `-1`），这正是题目要求的定义。

#### 代码（Python）

```python
class TreeAncestor:
    def __init__(self, n: int, parent: list[int]):
        # 保存原始父亲数组，后面直接查表
        self.parent = parent

    def getKthAncestor(self, node: int, k: int) -> int:
        # 按题意向上爬 k 步
        cur = node
        while k > 0 and cur != -1:      # 只要还有步数且没到根的父亲就继续
            cur = self.parent[cur]      # 走一步
            k -= 1                      # 步数-1
        return cur                       # 走完了 k 步，返回所在节点（可能是 -1）
```

#### 复杂度

- **时间复杂度**：`O(k)`。如果 `k` 很大（比如接近 `n`），每次查询都要走上万步。这里的 `O(k)` 里的 `k` 就是“爬的层数”，想象成在楼梯上一步一步往上走，需要走多少步就花多少时间。
- **空间复杂度**：`O(1)`（不计输入数组）。只用了几个临时变量，额外占用的内存几乎可以忽略不计。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次查询都要逐层向上走**，最坏情况要走 `O(k)` 步，而 `k` 可能和 `n` 同阶（`5·10⁴`），在查询 `5·10⁴` 次时会导致 **时间超限**。  
我们需要一种“**跳跃**”的方式，让一次查询可以一次跨过多层，而不是一步一步。

**核心想法——二进制提升（Binary Lifting）**  
- 把每个节点的 **2⁰（1）层、2¹（2）层、2²（4）层…** 的祖先预先算好，存进表格。  
- 查询时，把 `k` 用二进制拆分，例如 `k = 13 = 1101₂ = 8 + 4 + 1`，只需要一次跳到第 8 层祖先、一次跳到第 4 层祖先、一次跳到第 1 层祖先，**最多 `log₂k` 次跳**。

**如何预处理**  
设 `up[i][j]` 表示节点 `i` 向上 `2^j` 步后所在的节点（若不存在则为 `-1`）。  
- `j = 0` 时，`up[i][0] = parent[i]`（直接父亲）。  
- 对于更大的 `j`：`up[i][j] = up[ up[i][j‑1] ][j‑1]`。  
  换句话说，先上 `2^{j‑1}` 步到 `mid = up[i][j‑1]`，再从 `mid` 再上 `2^{j‑1}` 步，就是总共上 `2^j` 步。

**查询**  
把 `k` 的二进制位从低到高遍历：如果第 `j` 位是 `1`，就把当前节点跳到 `up[node][j]`。若在跳的过程中遇到 `-1`，直接返回 `-1`。

**为什么快**  
- 预处理只需要遍历 `n * log n` 次，`log n` 大约是 16（因为 `n ≤ 5·10⁴`），很小。  
- 每次查询只检查 `log k ≤ log n` 位，最多 16 次跳，**时间降到 `O(log n)`**。

#### 代码（Python）

```python
class TreeAncestor:
    def __init__(self, n: int, parent: list[int]):
        """
        构造二进制提升表 up[n][LOG]。
        LOG = 能覆盖 n 的最大二进制位数（2^LOG > n）。
        """
        import math
        self.LOG = math.ceil(math.log2(n)) + 1   # 多留一位防止越界
        self.up = [[-1] * self.LOG for _ in range(n)]

        # j = 0 时直接填父亲
        for i in range(n):
            self.up[i][0] = parent[i]

        # 动态规划求 up[i][j]（上 2^j 步的祖先）
        for j in range(1, self.LOG):
            for i in range(n):
                mid = self.up[i][j - 1]          # 先上 2^{j-1} 步
                if mid != -1:                    # 如果中间节点存在
                    self.up[i][j] = self.up[mid][j - 1]  # 再上 2^{j-1} 步
                # 否则保持 -1（已经到根的上方）

    def getKthAncestor(self, node: int, k: int) -> int:
        """
        把 k 拆成二进制位, 按位跳。
        """
        cur = node
        bit = 0
        while k > 0 and cur != -1:
            if k & 1:                     # 当前最低位是 1，需要跳 2^bit 步
                cur = self.up[cur][bit]   # 一次跳到 2^bit 祖先
            k >>= 1                        # 右移，处理下一位
            bit += 1
        return cur
```

#### 复杂度

- **时间复杂度**  
  - 预处理：`O(n log n)`。因为外层 `log n`（约 16）次循环，每次遍历 `n` 个节点。  
  - 单次查询：`O(log n)`。只需要检查 `k` 的二进制位数，最多 `log₂k ≤ log₂n` 次跳。相较于暴力的 `O(k)`，把“走楼梯”变成“坐电梯”，速度提升数十倍。  
- **空间复杂度**：`O(n log n)`。存放 `up` 表需要 `n * LOG` 个整数，同样是约 `n * 16`，在本题限制下完全可接受。

---

## 心得

- **核心技巧**：二进制提升（Sparse Table / Binary Lifting）——把“向上 k 步”拆成若干 “向上 2^j 步”的组合，用预处理表一次性跳过去。  
- **适用题型**  
  1. “第 k 代祖先”或“查询两节点的最近公共祖先（LCA）”等树上向上跳的问题。  
  2. “在有向无环图（DAG）上求 k 次跳转”或“跳表（Jump Game）”的离线查询。  
- **一句话总结**：**把大步拆成二进制的若干小步，预处理一次，查询只用 `log` 次跳**。

---

## 反思

- **第一反应**：直接用循环逐层向上爬，代码最简单，却忽略了查询次数可能很多导致超时。  
- **最容易踩的坑**  
  - **边界条件**：根节点的父亲是 `-1`，后续任何跳都应保持 `-1`，否则会出现数组越界。  
  - **LOG 的取值**：必须保证 `2^LOG` 大于等于 `n`，否则最高位的跳会缺失。  
  - **查询时的 `k` 为 0**：按定义返回自身，这里实现时会直接跳过循环，返回 `node`（因为 `k` 为 0 时循环不进入），要注意不误删。  
- **下次遇到同类题**：第一步先思考“能不能把一次操作拆成若干固定长度的跳”，如果可以，就立刻想到 **二进制提升**（或离线 DP）来做预处理。这样既能保证正确性，又能把每次查询的时间压到对数级别。