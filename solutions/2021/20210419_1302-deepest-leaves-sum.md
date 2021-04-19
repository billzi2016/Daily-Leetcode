# #1302. 最深叶子节点之和 / Deepest Leaves Sum

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/deepest-leaves-sum/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5,null,6,7,null,null,null,null,8]
Output: 15
```

**Example 2:**

```
Input: root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]
Output: 19
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- 1 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，返回最深层叶子节点（deepest leaves）的值之和。

**示例 1：**  
**输入:** `root = [1,2,3,4,5,null,6,7,null,null,null,null,8]`  
**输出:** `15`

**示例 2：**  
**输入:** `root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]`  
**输出:** `19`

**约束条件：**  
- 树中节点的数量在 `[1, 10⁴]` 范围内。  
- `1 <= Node.val <= 100`   (节点值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「找最深的叶子」这件事拆成两步：

1. **遍历整棵树**，记录下树的最大深度（即最深的层数）。  
   - 可以把树看成「一层层的楼层」，根节点在第 1 层，往下每往左/右走一步，层数就加 1。  
   - 记录最大的层数就相当于在一幢大楼里找最高的楼层。

2. **再次遍历整棵树**，把所有深度等于最大深度的叶子节点的值加起来。  
   - 这一步类似「在字典里查单词」，我们把「层数」当作字典的 key（关键词），对应的「所有节点值的和」当作 value（页码）。遍历时只把层数等于最大层数的值累加。

**为什么这个方法一定能得到正确答案**  
- 第一次遍历保证我们知道真正的「最深层」到底是第几层。  
- 第二次遍历只把恰好在这层的叶子节点加起来，其他层的节点根本不参与求和，结果自然就是「最深叶子之和」。

**时间/空间复杂度的大白话**  
- 我们对树做了 **两次完整的遍历**，每次都要访问每个节点一次。  
  - 如果树有 `n` 个节点，遍历一次的工作量就是 `n`，两次就是 `2n`，在大 O 记号里常数 2 会被省掉，写成 **O(n)**。  
- 递归实现（DFS）会用到栈空间，最坏情况下（比如一条长链）栈的深度等于树的高度 `h`，而 `h ≤ n`，所以空间复杂度是 **O(h)**，在最坏情况下可以认为是 **O(n)**。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def deepestLeavesSum(root: TreeNode) -> int:
    """两遍遍历：先找最大深度，再求和"""

    # ---------- 第一次遍历：求最大深度 ----------
    max_depth = 0                     # 用来记录遍历过程中出现的最大层数

    def dfs_depth(node, depth):
        """深度优先搜索，遍历每个节点并更新 max_depth"""
        nonlocal max_depth
        if not node:                  # 空节点直接返回
            return
        # 更新当前看到的最大层数
        if depth > max_depth:
            max_depth = depth
        # 继续向左、右子树递归
        dfs_depth(node.left, depth + 1)
        dfs_depth(node.right, depth + 1)

    dfs_depth(root, 1)                # 根节点在第 1 层

    # ---------- 第二次遍历：累计最深叶子节点的值 ----------
    total = 0                         # 最终答案

    def dfs_sum(node, depth):
        """再次遍历，只把 depth == max_depth 的节点值加到 total"""
        nonlocal total
        if not node:
            return
        # 如果当前节点正好在最深层，累加它的值
        if depth == max_depth:
            total += node.val
        # 继续向下搜索
        dfs_sum(node.left, depth + 1)
        dfs_sum(node.right, depth + 1)

    dfs_sum(root, 1)
    return total
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要遍历两遍，每遍都是 `O(n)`，合在一起仍是线性时间。  
- **空间复杂度**：`O(h)` — 递归调用栈的深度等于树的高度 `h`，最坏情况 `h = n`，即 `O(n)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**两遍遍历的瓶颈在于重复走了一遍树**。如果我们在 **一次遍历的过程中** 同时记录：

- 当前遍历到的节点所在的层数 `depth`  
- 目前已经看到的最大层数 `max_depth`  
- 对应最大层数的叶子节点值的累计和 `total`

那么就不需要第二次遍历了。实现思路如下：

1. **一次深度优先搜索（DFS）**，从根节点开始，递归向下。  
2. **每访问一个节点**，比较它的层数 `depth` 与当前记录的 `max_depth`：
   - 如果 `depth > max_depth`，说明我们发现了更深的层，**把 `max_depth` 更新为 `depth`，并把 `total` 重置为当前节点的值**（因为之前的累计是旧的更浅层的）。
   - 如果 `depth == max_depth`，说明这个节点和已经记录的最深层在同一层，**把它的值加到 `total`**。
   - 如果 `depth < max_depth`，直接忽略，因为它不在最深层。
3. 递归结束后，`total` 就是所有最深叶子节点的和。

**为什么一次遍历就够了**  
- 我们在遍历的过程中**实时维护**了「最深层」的信息。每当发现更深的层时，立刻把累计和清零并重新计数，这保证了遍历结束时 `total` 只包含**最新、最深**层的节点值。

**核心数据结构 & 技巧**  
- **递归栈（DFS）**：把「层数」当作递归的额外参数，类似在楼层之间上下走。  
- **全局/闭包变量**：`max_depth` 与 `total` 用 `nonlocal`（或类属性）在递归的各层之间共享。

**大白话的复杂度解释**  
- 只走了一遍树，遍历每个节点一次，工作量随节点数线性增长，记作 **O(n)**。  
- 递归栈的深度仍然是树的高度 `h`，所以空间是 **O(h)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def deepestLeavesSum(root: TreeNode) -> int:
    """一次 DFS 同时维护最大深度和对应的和"""

    max_depth = 0   # 记录遍历过程中出现的最大层数
    total = 0       # 对应最大层数的节点值累计和

    def dfs(node, depth):
        """深度优先搜索，边遍历边更新 max_depth 与 total"""
        nonlocal max_depth, total
        if not node:
            return
        # -------------------------------------------------
        # 1) 当前层比已知的最大层更深 → 更新 max_depth，重置 total
        # 2) 当前层等于已知的最大层 → 累加当前节点值到 total
        # 3) 当前层更浅 → 什么也不做
        # -------------------------------------------------
        if depth > max_depth:
            max_depth = depth      # 发现更深的层
            total = node.val       # 重新开始累计，只保留当前节点
        elif depth == max_depth:
            total += node.val       # 同层节点，继续累加

        # 继续向左、右子树搜索，层数加 1
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 1)   # 根节点视作第 1 层
    return total
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次，每个节点访问一次。相比暴力解省去了一遍遍历，实际运行更快。  
- **空间复杂度**：`O(h)` — 递归栈深度等于树的高度，最坏情况 `O(n)`，平均情况更小。

---

## 心得

- 这道题考察 **树的遍历** 与 **层次信息的实时维护**。  
- 关键技巧是 **在一次遍历中同时记录最大深度和对应的累计和**，避免二次遍历。  
- 该技巧适用于类似题目，例如：
  1. **Maximum Width of Binary Tree**（求二叉树最大宽度）  
  2. **Sum of Left Leaves**（求左叶子节点之和）  
  3. **Binary Tree Right Side View**（求二叉树右视图）  

> **解题钥匙**：遍历时“看到更深的层就把累计和清零”，这样一次遍历即可得到最深层的和。

---

## 反思

- **第一反应**：把问题拆成“先找最深层，再求和”，于是写出了两遍遍历的暴力实现。  
- **最容易踩的坑**：  
  - 忘记把根节点算作第 1 层，导致深度偏移 1，答案出错。  
  - 在一次遍历实现时，没有在发现更深层时及时把 `total` 置零，导致把旧层的值错误地累加进去。  
- **下次遇到同类题**，第一步应该思考：“是否可以在一次遍历中同步维护需要的统计信息（如最大层、计数或求和）”，这样往往能直接得到最优解。