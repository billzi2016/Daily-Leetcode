# #1028. 根据前序遍历恢复二叉树 / Recover a Tree From Preorder Traversal

> 难度：困难 · 标签：String、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/recover-a-tree-from-preorder-traversal/)

---

## 题目（英文原版）

**Description**

We run a preorder depth-first search (DFS) on the root of a binary tree.
At each node in this traversal, we output D dashes (where D is the depth of this node), then we output the value of this node.  If the depth of a node is D, the depth of its immediate child is D + 1.  The depth of the root node is 0.
If a node has only one child, that child is guaranteed to be the left child.
Given the output traversal of this traversal, recover the tree and return its root.

**Examples**

**Example 1:**

```
Input: traversal = "1-2--3--4-5--6--7"
Output: [1,2,5,3,4,6,7]
```

**Example 2:**

```
Input: traversal = "1-2--3---4-5--6---7"
Output: [1,2,5,3,null,6,null,4,null,7]
```

**Example 3:**

```
Input: traversal = "1-401--349---90--88"
Output: [1,401,null,349,88,90]
```

**Constraints**

- The number of nodes in the original tree is in the range [1, 1000].
- 1 <= Node.val <= 109

---

## 题目（中文翻译）

我们对二叉树的根节点进行**前序深度优先搜索（DFS）**。  
在遍历的每个节点处，先输出 `D` 个短横线（`-`），其中 `D` 为该节点的**深度**，随后输出该节点的值。根节点的深度为 `0`，其直接子节点的深度为 `D + 1`。  

如果某个节点只有一个子节点，则该子节点一定是左子节点。  
给定上述遍历的输出字符串 `traversal`，请恢复原二叉树并返回其根节点。

---

### 示例

**示例 1**  
输入: `traversal = "1-2--3--4-5--6--7"`  
输出: `[1,2,5,3,4,6,7]`

**示例 2**  
输入: `traversal = "1-2--3---4-5--6---7"`  
输出: `[1,2,5,3,null,6,null,4,null,7]`

**示例 3**  
输入: `traversal = "1-401--349---90--88"`  
输出: `[1,401,null,349,88,90]`

---

### 约束条件

- 原二叉树中的节点数在 `[1, 1000]` 区间内。  
- `1 <= Node.val <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **先把字符串全部拆成「深度‑节点值」的列表**  
   - 从左到右遍历 `traversal`，遇到连续的 `-` 就记下来，它的个数就是当前节点的深度 `D`。  
   - 接下来读取连续的数字，就是节点的值 `val`。  
   - 把 `(depth, val)` 加入一个数组 `nodes`。  

2. **递归地把列表恢复成二叉树**  
   - 设 `build(start, depth)` 返回从 `start` 开始、深度为 `depth` 的子树根节点。  
   - `nodes[start]` 必须正好是 `depth`，否则说明这里没有该深度的节点，返回 `None`。  
   - 对左子树：在 `start+1` 位置继续寻找深度为 `depth+1` 的节点（如果有的话）。  
   - 对右子树：左子树占用了若干个连续的元素后，继续在后面寻找深度仍为 `depth+1` 的节点。  
   - 递归结束的条件是 `start` 越界或深度不匹配。  

> **类比**：把 `nodes` 看成一本「层次记录册」，`build` 就像在这本册子里翻页，找到对应层级的章节再把它们拼装起来。

**为什么这个方法能得到正确的树**  
- 前序遍历的顺序恰好是「根 → 左子树 → 右子树」，我们在 `nodes` 中保持了同样的顺序。  
- 递归函数每次只在「当前深度」上寻找节点，深度不匹配就说明该位置应该是空子树，正好对应二叉树的 `None`。  

**时间/空间复杂度**  
- 解析字符串得到 `nodes` 需要遍历一次，`O(n)`（`n` 为字符数）。  
- 递归恢复树时，每次都要在 `nodes` 中线性搜索左/右子树的起始位置，最坏会遍历 `O(n)` 次，导致总体 **时间复杂度 `O(n²)`**。  
- 递归调用栈深度最多等于树的高度，最坏是 `O(n)`，再加上存放 `nodes` 的数组，同样是 **空间复杂度 `O(n)`**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def recoverFromPreorder(traversal: str) -> TreeNode:
    # 1️⃣ 把字符串转成 (depth, value) 列表
    nodes = []                      # 存放 (depth, val)
    i = 0
    while i < len(traversal):
        d = 0                       # 统计连着的 '-'，得到深度
        while i < len(traversal) and traversal[i] == '-':
            d += 1
            i += 1
        v = 0                       # 读取数字，得到节点值
        while i < len(traversal) and traversal[i].isdigit():
            v = v * 10 + int(traversal[i])
            i += 1
        nodes.append((d, v))

    # 2️⃣ 递归构造二叉树
    def build(start: int, depth: int):
        """返回从 start 开始、深度为 depth 的子树根节点，以及下一个未使用的下标"""
        if start >= len(nodes) or nodes[start][0] != depth:
            return None, start            # 没有对应深度的节点，返回空

        root = TreeNode(nodes[start][1])  # 创建根节点
        # 左子树
        left_child, nxt = build(start + 1, depth + 1)
        root.left = left_child
        # 右子树（左子树可能用了若干个元素）
        right_child, nxt2 = build(nxt, depth + 1)
        root.right = right_child
        return root, nxt2                # 返回根节点和已消费到的下标

    root, _ = build(0, 0)
    return root
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 最外层遍历 `nodes` 是 `O(n)`，但每一次递归都要线性扫描寻找子树的起始位置，最坏会出现 `1 + 2 + … + n = O(n²)` 次比较。  
- **空间复杂度**：`O(n)`  
  - `nodes` 列表占 `O(n)`，递归栈深度最坏为树的高度 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次递归都要线性搜索子树起始位置**。如果我们在遍历 `traversal` 的同时，**实时维护一个「当前路径」的栈**，就能在 **O(1)** 时间内找到父节点，从而把节点直接挂到正确的位置。

**核心步骤**  

1. **同样先把字符串解析为「深度‑值」的序列**（这一步仍是 `O(n)`，不可避免）。  
2. **用栈 `stack` 保存已经创建好的节点，栈顶始终是「最近一次出现的、深度最深的」节点**。  
   - 栈中元素的顺序恰好对应从根到当前节点的路径。  
3. **遍历 `(depth, val)` 列表**  
   - 当栈的长度大于 `depth` 时，说明我们已经回到了更高层，需要 **弹出**（`pop`）多余的节点，直至栈的大小恰好等于 `depth`。  
   - 此时栈顶（如果存在）就是当前节点的父节点。因为题目保证「如果只有一个子节点，它一定是左子节点」，我们只需要判断父节点的左子是否为空来决定挂左还是挂右。  
   - 创建新节点 `node = TreeNode(val)`，把它挂到父节点，然后 **压入栈**，成为新的最深节点。  
4. **遍历结束后，栈底的那个节点就是根**。  

> **类比**：想象我们在爬楼梯，每上一步就把当前的楼层号压进栈；如果要下楼（深度变小），就把多余的楼层号弹出，保持栈顶恰好是我们现在所在的层。这样随时都知道「我现在的父层是哪一层」。

**为什么正确**  
- 前序遍历的顺序保证我们在看到某个节点时，它的父节点一定已经创建并且仍在栈中（因为父节点的深度一定小于当前节点）。  
- 当深度变小，弹出多余的节点正好把「已经处理完的子树」从路径中移除，确保后面的节点能正确挂到同一层的右子树上。  

**时间/空间复杂度**  
- 只遍历一次 `traversal`，每个字符最多被读取一次，**时间复杂度 `O(n)`**。  
- 栈最多保存从根到叶子的路径，深度不超过节点数，**空间复杂度 `O(h)`**（`h` 为树高），最坏 `O(n)`，但比 `O(n²)` 好很多。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def recoverFromPreorder(traversal: str) -> TreeNode:
    # 1️⃣ 解析成 (depth, value) 序列
    pairs = []                         # [(depth, val), ...]
    i = 0
    while i < len(traversal):
        d = 0
        while i < len(traversal) and traversal[i] == '-':
            d += 1
            i += 1
        v = 0
        while i < len(traversal) and traversal[i].isdigit():
            v = v * 10 + int(traversal[i])
            i += 1
        pairs.append((d, v))

    stack = []                         # 保存路径上的节点，栈底是根
    for depth, val in pairs:
        node = TreeNode(val)           # 创建当前节点

        # 2️⃣ 把栈调到和当前深度一致（弹出多余的祖先）
        while len(stack) > depth:      # 栈的大小 == 已经走过的深度
            stack.pop()

        # 3️⃣ 把当前节点挂到父节点上（如果有父节点）
        if stack:                       # 不是根节点
            parent = stack[-1]          # 栈顶即为父节点
            if not parent.left:
                parent.left = node      # 左子为空时先填左子
            else:
                parent.right = node     # 否则一定是右子（题目保证）

        # 4️⃣ 当前节点入栈，成为以后节点的潜在父节点
        stack.append(node)

    # 栈底的节点就是根
    return stack[0] if stack else None
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次输入字符串，栈的每个元素最多被 `push`、`pop` 各一次，整体线性。  
- **空间复杂度**：`O(h)`（`h` 为树的高度），最坏 `O(n)`  
  - 只需要保存当前路径上的节点，深度越大占用的空间越多。

---

## 心得

- **核心技巧**：利用「深度信息 + 栈」在一次遍历中完成树的重建。  
- **适用场景**：  
  1. 任何给出 **前序遍历 + 深度/层级信息** 的树恢复题（如 LeetCode 1028 / 1029）。  
  2. 需要 **从带层次标记的序列** 构造层次结构的场景（比如组织结构图、文件系统路径）。  
  3. 处理 **括号匹配**、**表达式树** 等需要「实时维护父子关系」的问题。  
- **一句话总结**：**深度决定栈的高度，栈顶即为当前节点的父亲**——把这句话记住，几乎所有类似的层次恢复题都能迎刃而解。

---

## 反思

- **第一反应**：看到「- 的个数代表深度」立刻想到把字符串拆成 `(depth, val)`，然后想用递归去找左、右子树。  
- **最容易踩的坑**  
  1. **深度不匹配时的返回**：递归版容易忘记在深度不等时直接返回 `None`，导致错误的左/右子树链接。  
  2. **只有左子树的情况**：题目保证「若只有一个子节点一定是左子」，在栈解法里一定要先检查 `parent.left` 是否为空，再决定挂左还是挂右。  
  3. **大数值**：节点值可达 `10⁹`，一定要用 `int`（Python 自带大整数，没问题），但在手写代码时注意不要把字符直接当成 ASCII 码。  
- **下次类似题的第一步**：**先把「层级信息」抽取出来**（比如深度、缩进、括号层数），随后 **用栈或递归保持当前路径**，这样就能在 O(n) 时间内完成构造。