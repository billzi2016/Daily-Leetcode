# #199. 二叉树的右侧视图 / Binary Tree Right Side View

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-right-side-view/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]
Explanation:
```

**Example 2:**

```
Input: root = [1,2,3,4,null,null,null,5]
Output: [1,3,4,5]
Explanation:
```

**Example 3:**

```
Input: root = [1,null,3]
Output: [1,3]
```

**Example 4:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树 (binary tree) 的根节点 `root`，想象你站在树的右侧，从上到下返回所有能够看到的节点值，顺序从顶部到底部。

**示例 1**  
**示例 2**  
**示例 3**  
**示例 4**  

**约束条件**  

- 树中节点的数量在 `[0, 100]` 区间内。  
- 每个节点的取值满足 `-100 <= Node.val <= 100`。

**示例**

**示例 1:**  
```
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]
Explanation:
```

**示例 2:**  
```
Input: root = [1,2,3,4,null,null,null,5]
Output: [1,3,4,5]
Explanation:
```

**示例 3:**  
```
Input: root = [1,null,3]
Output: [1,3]
Explanation:
```

**示例 4:**  
```
Input: root = []
Output: []
Explanation:
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把整棵树的所有节点都遍历一遍**，记录每一层从左到右出现的节点，然后把每层最右边的节点挑出来返回。  

- **遍历方式**：我们可以使用递归的深度优先搜索（DFS）或显式的栈来实现“先左后右”。只要在遍历时把当前节点的层数（depth）记下来，就能把同一层的节点放进同一个容器（比如 `list of lists`）。  
- **数据结构类比**：把每一层看成一本书的章节，`depth` 就是章节号，章节里按顺序记下出现的词（节点值），最后取每章节的最后一个词，就是我们从右侧看到的节点。  
- **为什么正确**：因为我们把**每层所有节点都完整记录**，所以右侧看到的节点必定是该层的最后一个出现的节点。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rightSideView_brute(root: TreeNode):
    """
    暴力解法：先把每层所有节点收集起来，再取每层的最后一个。
    """
    if not root:
        return []

    # level_nodes[i] 保存第 i 层（根为第 0 层）的所有节点值
    level_nodes = []

    def dfs(node: TreeNode, depth: int):
        """先左后右的深度优先遍历"""
        if not node:
            return
        # 如果还没有创建当前层的列表，就先创建
        if depth == len(level_nodes):
            level_nodes.append([])

        # 把当前节点值加入对应层的列表
        level_nodes[depth].append(node.val)

        # 继续往左子树、右子树走，depth 加 1
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)

    # 取每层最后一个元素即为右侧视图
    return [nodes[-1] for nodes in level_nodes]
```

#### 复杂度

- **时间复杂度**：`O(N)`，其中 `N` 是树中节点的数量。我们会**恰好访问每个节点一次**，所以时间随节点数线性增长。  
- **空间复杂度**：`O(N)`。最坏情况下（比如完全不平衡的链状树）`level_nodes` 里会保存所有节点的值；递归栈的深度同样可能达到 `N`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈不在时间（已经是 `O(N)`），而在**额外的存储**：我们保存了每层所有节点，只为取最后一个。我们可以在遍历时**直接记录每层的最右节点**，不必把左侧的节点全部记下来。

两种常见的“直接记录”思路：

1. **层序遍历（BFS）**  
   - 按层遍历二叉树，**每次进入新的一层时先记录该层第一个弹出的节点**（如果我们从右子树先入队），这就是右侧能看到的节点。  
   - 用队列（`collections.deque`）实现，队列里一次只保存当前层的节点，遍历完该层后再进入下一层。  

2. **先右后左的深度优先遍历（DFS）**  
   - 递归时**先访问右子树，再访问左子树**。  
   - 当我们第一次来到某一层（`depth == len(res)`），说明之前还没有记录该层的任何节点，而此时访问的必然是最右侧的节点。于是直接把它加入结果列表。  

下面给出两种实现，任选其一均可得到最优解。这里我们重点讲解 **先右后左的 DFS**，因为它只用递归栈，不需要额外的队列，代码更简洁。

- **核心概念——深度优先 + 先右**  
  把树想象成一座高楼，每层只能看到最右边的窗户。我们从楼顶（根）往下走，**先尝试右侧的窗户**，如果该层还没有记录过，就把这扇窗户的编号（节点值）记下来。之后再去左侧尝试，但此时层已经有记录，不会再改动。

#### 代码（Python）

```python
def rightSideView(root: TreeNode):
    """
    最优解：先右后左的深度优先遍历，只保留每层第一次出现的节点。
    """
    view = []                     # 最终结果：每层最右侧的节点值

    def dfs(node: TreeNode, depth: int):
        if not node:
            return
        # 第一次到达这一层（depth 与 view 长度相同），说明这是最右侧的节点
        if depth == len(view):
            view.append(node.val)   # 直接把它加入结果

        # 先遍历右子树，再遍历左子树，保证先看到右侧节点
        dfs(node.right, depth + 1)
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return view
```

#### 复杂度

- **时间复杂度**：`O(N)`。每个节点仍然只被访问一次，没有额外的循环。  
- **空间复杂度**：`O(H)`，其中 `H` 是树的高度。递归栈最多保存从根到最深叶子的路径。对平衡二叉树 `H ≈ logN`，最坏情况（链状树）`H = N`，但仍比暴力解的 `O(N)` 额外列表要省空间。

---

## 心得

- **核心技巧**：**先右后左的深度优先遍历** 或 **层序遍历时从右到左入队**，利用“第一次到达某层”这一特性直接得到右侧视图。  
- **适用题型**：  
  1. “二叉树的左侧视图”（只把遍历顺序改为先左后右）。  
  2. “二叉树的层序遍历”中需要每层的最大/最小值。  
  3. “二叉树的垂直遍历”需要按层次记录第一次出现的节点。  
- **一句话总结**：**把“先看右边”这一步写进遍历顺序，第一次碰到的就是答案**。

---

## 反思

- **第一反应**：把树每层全部收集，再取每层最后一个——直觉自然但会浪费空间。  
- **最容易踩的坑**：  
  - 递归实现时忘记先遍历右子树，导致记录的是左侧节点。  
  - 空树 (`root = None`) 必须返回空列表，防止 `None` 引发异常。  
  - 深度 `depth` 与结果列表长度的比较要写成 `depth == len(view)`，否则会漏掉某些层。  
- **下次类似题目第一步**：**明确“先看哪一侧”**，把它体现在遍历顺序（右/左）或入队顺序上，然后利用“第一次出现即为答案”的特性直接记录。