# #1530. 好叶子节点对的数量 / Number of Good Leaf Nodes Pairs

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/number-of-good-leaf-nodes-pairs/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree and an integer distance. A pair of two different leaf nodes of a binary tree is said to be good if the length of the shortest path between them is less than or equal to distance.
Return the number of good leaf node pairs in the tree.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,null,4], distance = 3
Output: 1
Explanation: The leaf nodes of the tree are 3 and 4 and the length of the shortest path between them is 3. This is the only good pair.
```

**Example 2:**

```
Input: root = [1,2,3,4,5,6,7], distance = 3
Output: 2
Explanation: The good pairs are [4,5] and [6,7] with shortest path = 2. The pair [4,6] is not good because the length of ther shortest path between them is 4.
```

**Example 3:**

```
Input: root = [7,1,4,6,null,5,3,null,null,null,null,null,2], distance = 3
Output: 1
Explanation: The only good pair is [2,5].
```

**Constraints**

- The number of nodes in the tree is in the range [1, 210].
- 1 <= Node.val <= 100
- 1 <= distance <= 10

---

## 题目（中文翻译）

给定二叉树（binary tree）的根节点 `root` 和一个整数 `distance`。如果二叉树中两个不同的叶子节点（leaf node）之间的最短路径（shortest path）长度小于等于 `distance`，则这对叶子节点被称为「好」的。返回树中好叶子节点对的数量。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- 树中节点的数量在 `[1, 2^10]` 区间内。  
- `1 <= Node.val <= 100`  
- `1 <= distance <= 10`

---

### 示例

**示例 1**  
**输入**: `root = [1,2,3,null,4], distance = 3`  
**输出**: `1`  
**解释**: 树的叶子节点是 `3` 和 `4`，它们之间的最短路径长度为 `3`。这是唯一的一对好叶子节点。

**示例 2**  
**输入**: `root = [1,2,3,4,5,6,7], distance = 3`  
**输出**: `2`  
**解释**: 好的叶子节点对为 `[4,5]` 和 `[6,7]`，它们的最短路径长度均为 `2`。而 `[4,6]` 不是好对，因为它们之间的最短路径长度为 `4`。

**示例 3**  
**输入**: `root = [7,1,4,6,null,5,3,null,null,null,null,null,2], distance = 3`  
**输出**: `1`  
**解释**: 唯一的好叶子节点对是 `[2,5]`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有叶子节点找出来**，然后两两比较它们之间的路径长度，判断是否 ≤ `distance`。  
- **叶子节点**：没有左子树也没有右子树的节点。可以在一次遍历（DFS 或 BFS）中收集到。  
- **两叶子之间的最短路径**：在二叉树里，两点的最短路径一定是「从叶子 A 向上走到最近的公共祖先 LCA，然后再往下走到叶子 B」。所以路径长度 = `depth(A) + depth(B) - 2*depth(LCA)`。  
  - 这里的 **depth**（深度）可以类比为「从根节点走到某个节点需要多少步」，类似我们查字典时，从目录（根）一路往下找词条（节点）的层级数。  
- **实现方式**：  
  1. 第一次 DFS 把所有叶子节点的 `depth` 和指向根的父指针（或直接记录整棵树的父指针）保存下来。  
  2. 对每一对叶子 `(i, j)`（共 `C(k,2)` 对，k 为叶子数），利用父指针向上追溯找到最近的公共祖先，计算路径长度。  
  3. 若长度 ≤ `distance`，计数 +1。  

这种方法**一定能得到正确答案**，因为我们枚举了所有可能的叶子对，并且用树的结构完整地算出了它们之间的真实距离。

**为什么会慢？**  
- 第 2 步里找 LCA 的过程是**从两个叶子向上逐层比较**，最坏情况下要走到根节点。若树高为 `h`，每对叶子最坏 O(`h`) 步。  
- 叶子数 `k` 最坏可以接近 `n/2`（满二叉树），于是总的比较次数是 `O(k² * h)`，在最坏情况下大约是 `O(n²)`（因为 `h ≤ n`）。  

**大白话解释时间复杂度**：  
- `O(n²)` 就像你让每个人和班里所有其他同学握手，人数多了，握手次数会呈平方增长，耗时会很快爆炸。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def countPairs(root, distance):
    # ---------- 第一步：收集所有叶子节点 ----------
    leaves = []                 # 存放 (leaf_node, depth, parent_map) 三元组
    parent = {root: None}       # 记录每个节点的父节点，类似“查字典”里把词对应到页码
    depth = {root: 0}           # 记录每个节点到根的距离（层数）

    def dfs(node):
        if not node:
            return
        if node.left:
            parent[node.left] = node
            depth[node.left] = depth[node] + 1
        if node.right:
            parent[node.right] = node
            depth[node.right] = depth[node] + 1
        if not node.left and not node.right:          # 叶子节点
            leaves.append(node)
        dfs(node.left)
        dfs(node.right)

    dfs(root)

    # ---------- 第二步：两两比较 ----------
    def lca(a, b):
        """返回节点 a, b 最近公共祖先的深度"""
        da, db = depth[a], depth[b]
        # 让两条向上走的“链”先对齐深度
        while da > db:
            a = parent[a]
            da -= 1
        while db > da:
            b = parent[b]
            db -= 1
        # 同时向上走，直到相遇
        while a != b:
            a = parent[a]
            b = parent[b]
        return depth[a]  # 此时 a == b 为 LCA

    ans = 0
    m = len(leaves)
    for i in range(m):
        for j in range(i + 1, m):
            d = depth[leaves[i]] + depth[leaves[j]] - 2 * lca(leaves[i], leaves[j])
            if d <= distance:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（最坏情况下每对叶子要走到根，叶子数 ≈ `n/2`，所以大约是 `n²/4`）  
  - 直观含义：如果树里有 1000 个节点，耗时大约相当于 1,000,000 次基本操作，明显不够快。  
- **空间复杂度**：`O(n)`  
  - 需要存父指针、深度以及所有叶子节点的信息，和树的规模线性相关。

---

### 2. 最优解

#### 思路  

从暴力解的**瓶颈**出发：我们在每次比较两片叶子时，都要**向上回溯**找 LCA，导致重复遍历同一段路径。  
实际上，**在一次 DFS 过程中就可以把所有叶子对的距离信息累计起来**，不必再次遍历。

核心思想是 **自底向上的深度统计 + 合并**：

1. 对每个节点，返回一个数组 `cnt[d]`，表示「以该节点为根，距离该节点 **恰好** 为 `d` 的叶子有多少个」。
   - 只需要统计到 `distance` 为止，因为更远的叶子已经不可能构成「好」的配对。
2. 对于当前节点 `cur`，它的左子树返回 `left_cnt`，右子树返回 `right_cnt`。  
   - 所有「左子树的叶子」和「右子树的叶子」之间的配对，都必须经过 `cur`，路径长度 = `dl + dr + 2`（`+2` 是左、右各向上走一步到 `cur`）。  
   - 我们遍历 `dl`、`dr`（都 ≤ `distance`），只要 `dl + dr + 2 ≤ distance`，就把 `left_cnt[dl] * right_cnt[dr]` 加到答案中。  
3. 合并计数：`cnt[d] = left_cnt[d-1] + right_cnt[d-1]`（因为向上传递时距离会增加 1）。  
   - 这里的 “-1” 就像我们把「往上走一步」的距离记进来，类似把“从子树根到父节点的距离 +1”。  
4. 递归结束后，答案已经在全局变量里累计完毕。

**为什么正确？**  
- 任何两片叶子要么在同一子树内部（递归后会在更低层计数），要么分属左右子树并且必须经过当前节点。我们在每个节点都完整地统计了「跨左右子树」的配对，且不漏不重。  
- 只统计到 `distance`，因为更远的叶子即使再往上传也只会让距离更大，不会产生合法配对。

**类比**：想象你在组织一次“相亲大会”，每个父母（树的节点）负责把自己子女（叶子）介绍给对方的子女。父母只需要告诉组织者「我这里有多少孩子距离我 1 步、2 步、…、distance 步」，组织者再根据这张表格快速算出符合距离要求的配对数，而不必让每对孩子自己跑来跑去找对方。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def countPairs(root, distance):
    ans = 0                     # 用来累计所有好配对

    def dfs(node):
        """
        返回一个长度为 distance+1 的列表 cnt，
        cnt[d] 表示「以 node 为根，距离 node 恰好为 d 的叶子数量」。
        """
        nonlocal ans
        if not node:
            # 空节点没有叶子，返回全 0 的列表
            return [0] * (distance + 1)

        if not node.left and not node.right:
            # 叶子节点：距离自身为 0 的叶子有 1 个
            cnt = [0] * (distance + 1)
            cnt[0] = 1
            return cnt

        left_cnt = dfs(node.left)    # 左子树的统计表
        right_cnt = dfs(node.right)  # 右子树的统计表

        # ----- 统计跨左右子树的好配对 -----
        for dl in range(distance + 1):          # dl 为左子树叶子到 node 的距离
            for dr in range(distance + 1):      # dr 为右子树叶子到 node 的距离
                if dl + dr + 2 <= distance:     # +2 表示左、右各走一步到 node
                    ans += left_cnt[dl] * right_cnt[dr]

        # ----- 合并计数，返回给父节点 -----
        cnt = [0] * (distance + 1)
        for d in range(1, distance + 1):
            # 往上传递时距离 +1，故把子树里距离为 d-1 的叶子累计到这里的 d
            cnt[d] = left_cnt[d - 1] + right_cnt[d - 1]
        return cnt

    dfs(root)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * distance²)`  
  - 对每个节点我们都遍历两层 `distance`（最多 10），内部是两层 `for` 循环，常数很小。  
  - 直观上：如果树有 10⁵ 个节点，而 `distance ≤ 10`，则最多约 `10⁵ * 100 = 10⁷` 次基本操作，完全能在毫秒级跑完。  
- **空间复杂度**：`O(h * distance)`（递归栈 + 每层返回的数组）  
  - `h` 为树的高度，最坏 `O(n)`（链状树），但每层只保存一个长度 `distance+1 ≤ 11` 的列表，整体仍是线性且很小。

---

## 心得

- **核心技巧**：**自底向上的距离计数 + 双子树配对**。  
- 这种思路常用于**树上计数**的题目，尤其是“**在两点之间的距离 ≤ K**”类的问题。  
- **相似题型**（可练习）  
  1. *Count Good Nodes in Binary Tree*（统计满足父子关系的节点）  
  2. *Number of Nodes in the Sub-Tree With the Same Label*（子树内部计数）  
  3. *Maximum Distance Between Any Pair of Nodes*（树上直径）  

> **解题钥匙**：在树的 **递归返回值** 中保存「**到叶子的距离分布**」，利用它在每个节点一次性完成跨子树配对的计数。

---

## 反思

- **第一反应**：直接把所有叶子列出来，两两比较路径长度——这就是暴力解。  
- **最容易踩的坑**  
  - **忘记限制距离**：返回的数组必须截断到 `distance`，否则会产生不必要的计算，甚至数组越界。  
  - **跨子树配对的 +2**：路径长度要加上从左叶子到当前节点再到右叶子的两条边，容易误写成 `+1`。  
  - **边界叶子**：单独的叶子在递归返回时要记得 `cnt[0]=1`，否则上层统计会漏掉。  
- **下次遇到同类题**，第一步应想到**“在每个节点返回关于叶子/子树的距离信息”**，再利用这些信息在局部完成全局计数，而不是遍历所有节点组合。