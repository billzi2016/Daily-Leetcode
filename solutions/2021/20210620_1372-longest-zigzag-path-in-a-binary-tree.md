# #1372. 二叉树中的最长锯齿形路径 / Longest ZigZag Path in a Binary Tree

> 难度：中等 · 标签：Dynamic Programming、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree.
A ZigZag path for a binary tree is defined as follow:
Zigzag length is defined as the number of nodes visited - 1. (A single node has a length of 0).
Return the longest ZigZag path contained in that tree.

**Examples**

**Example 1:**

```
Input: root = [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]
Output: 3
Explanation: Longest ZigZag path in blue nodes (right -> left -> right).
```

**Example 2:**

```
Input: root = [1,1,1,null,1,null,null,1,1,null,1]
Output: 4
Explanation: Longest ZigZag path in blue nodes (left -> right -> left -> right).
```

**Example 3:**

```
Input: root = [1]
Output: 0
```

**Constraints**

- The number of nodes in the tree is in the range [1, 5 * 104].
- 1 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`。

**锯齿形路径（ZigZag path）** 在二叉树中的定义如下：
- 锯齿形长度（ZigZag length）定义为访问的节点数减 1。（单个节点的长度为 0）

返回该树中最长的锯齿形路径的长度。

**示例 1**  
**输入**: `root = [1,null,1,1,1,null,null,1,1,null,1,null,null,null,1]`  
**输出**: `3`  
**解释**: 最长的锯齿形路径由蓝色节点组成（右 → 左 → 右）。

**示例 2**  
**输入**: `root = [1,1,1,null,1,null,null,1,1,null,1]`  
**输出**: `4`  
**解释**: 最长的锯齿形路径由蓝色节点组成（左 → 右 → 左 → 右）。

**示例 3**  
**输入**: `root = [1]`  
**输出**: `0`

**约束条件**  
- 树中节点的数量在区间 `[1, 5 * 10^4]` 内。  
- `1 <= Node.val <= 100`   (其中 `Node.val` 为节点的值)。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**每一个节点都可能是“锯齿路径”的起点**，我们从它出发，分别往左走一次、往右走一次，然后按照“左‑右‑左‑右…”的规则继续往下走，直到走不动为止。  

- **数据结构**：二叉树本身已经提供了左、右子节点的指针。我们只需要递归地访问它们，不需要额外的结构。  
- **为什么正确**：因为锯齿路径的定义只要求“相邻两条边的方向必须相反”。只要我们在每一步都强制切换方向，就一定得到一条合法的锯齿路径。遍历所有起点、所有起始方向，就能覆盖**所有**可能的锯齿路径，自然能找出最长的那一条。  
- **时间/空间复杂度**：  
  - 对每个节点，我们会再次遍历它的子树来计算路径长度。若树有 `n` 个节点，最坏情况下每次遍历都会触及 `O(n)` 个节点，故总体是 `O(n²)`。可以把 `n²` 想象成“每个人都要和所有人合照一次”。  
  - 递归调用的深度最多等于树的高度 `h`（最坏 `h = n`），因此额外的空间是 `O(h)`，即“栈帧占用的层数”。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def longestZigZag(root: TreeNode) -> int:
    """
    暴力解：对每个节点尝试两种起始方向，返回最长长度
    """
    if not root:
        return 0

    # 递归计算从 node 开始、direction 指定的最长锯齿长度
    # direction = 0 -> 下一步要往左走；1 -> 下一步要往右走
    def dfs(node: TreeNode, direction: int) -> int:
        if not node:
            return -1          # -1 是因为到空节点时实际长度应减 1
        if direction == 0:    # 要往左走
            left_len = dfs(node.left, 1)   # 左走后下一步必须往右
            # 右子树不符合当前方向，直接返回 -1
            return left_len + 1
        else:                 # 要往右走
            right_len = dfs(node.right, 0)
            return right_len + 1

    # 对每个节点尝试两种起始方向，取最大值
    left_start = dfs(root.left, 1)   # 从 root 左子树开始，方向为“右”
    right_start = dfs(root.right, 0) # 从 root 右子树开始，方向为“左”
    # 递归遍历左右子树，分别求它们的最长锯齿路径
    left_sub = longestZigZag(root.left)
    right_sub = longestZigZag(root.right)

    return max(left_start, right_start, left_sub, right_sub)


# ------------------- 测试 -------------------
# 用列表构造二叉树的辅助函数（仅用于本地测试，可忽略）
def build_tree(arr):
    if not arr:
        return None
    nodes = [None if v is None else TreeNode(v) for v in arr]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids: node.left = kids.pop()
            if kids: node.right = kids.pop()
    return root

# 示例 1
root1 = build_tree([1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1])
print(longestZigZag(root1))  # 输出 3
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 想象有 `n` 本书，每本书都要把所有 `n` 本书的目录全部翻一遍，最坏情况就是 `n × n` 次操作。这里的 `n` 是树的节点数。  
- **空间复杂度**：`O(h)`（递归栈），`h` 为树的高度，最坏 `O(n)`，相当于“最深的递归层数”。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**大量重复计算**：对同一个子树我们会多次求“从这里往左/往右的最长锯齿”。如果能在一次遍历中把这些信息保存下来，就可以把时间降到线性 `O(n)`。

**关键观察**：

1. 对每个节点 `node`，只关心两种“起始方向”的最长路径长度：  
   - `left[node]`：从 `node` 开始、第一步往左走的最长锯齿长度。  
   - `right[node]`：从 `node` 开始、第一步往右走的最长锯齿长度。  

2. 这两个值可以**由子节点的值递推**得到：  
   - 若要 `left[node]`，第一步必须左走到 `node.left`，接下来必须右走，于是 `left[node] = 1 + right[node.left]`（如果左子节点不存在则为 0）。  
   - 同理，`right[node] = 1 + left[node.right]`（右子节点不存在则为 0）。  

3. 在一次深度优先遍历（DFS）中，我们同时返回 `left[node]` 与 `right[node]`，并用一个全局变量 `ans` 记录出现过的最大值。  

**类比**：把每个节点想象成“转向指示牌”。左指示牌告诉你“往左，然后下一个必须往右”，右指示牌则相反。只要把每块指示牌的“下一块指示牌的长度”记下来，就能快速算出从这块指示牌开始的最长路线。

**算法步骤**：

1. 初始化全局最大 `ans = 0`。  
2. 递归函数 `dfs(node)` 返回 `(left_len, right_len)`。  
   - 若 `node` 为 `None`，返回 `(-1, -1)`（这里返回 `-1` 是为了让父节点算 `1 + (-1) = 0`，即空子树贡献 0 长度）。  
   - 递归左、右子树得到它们的 `(l_left, l_right)` 与 `(r_left, r_right)`。  
   - 计算当前节点的 `left_len = 1 + l_right`（左走后必须右走），`right_len = 1 + r_left`。  
   - 更新 `ans = max(ans, left_len, right_len)`。  
   - 返回 `(left_len, right_len)`。  
3. 最后返回 `ans`（如果树只有一个节点，`ans` 仍为 0，符合题意）。  

**复杂度**：  
- 每个节点只被访问一次，所有计算都是常数时间 → **`O(n)`**。  
- 递归栈深度至多树高 `h` → **`O(h)`**（最坏 `O(n)`），这就是额外空间。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def longestZigZag(root: TreeNode) -> int:
    """
    最优解：一次 DFS，返回以当前节点为起点、分别向左/向右的最长锯齿长度。
    """
    ans = 0                     # 用来记录全局最大长度

    def dfs(node: TreeNode):
        nonlocal ans
        if not node:
            # -1 的原因见思路中的解释，返回后父节点会算 1 + (-1) = 0
            return -1, -1

        # 递归左、右子树，分别得到它们的 (左起, 右起) 长度
        left_left, left_right = dfs(node.left)    # 左子树的两种起始长度
        right_left, right_right = dfs(node.right)  # 右子树的两种起始长度

        # 当前节点向左走：必须去左子树，然后下一步要向右走
        left_len = 1 + left_right   # 若左子树为空，left_right 为 -1，得到 0
        # 当前节点向右走：必须去右子树，然后下一步要向左走
        right_len = 1 + right_left

        # 更新全局最大值
        ans = max(ans, left_len, right_len)

        # 返回当前节点的两种起始长度，供父节点使用
        return left_len, right_len

    dfs(root)
    return ans
        

# ------------------- 测试 -------------------
def build_tree(arr):
    if not arr:
        return None
    nodes = [None if v is None else TreeNode(v) for v in arr]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids: node.left = kids.pop()
            if kids: node.right = kids.pop()
    return root

# 示例 1
root1 = build_tree([1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1])
print(longestZigZag(root1))  # 3

# 示例 2
root2 = build_tree([1,1,1,None,1,None,None,1,1,None,1])
print(longestZigZag(root2))  # 4

# 示例 3
root3 = build_tree([1])
print(longestZigZag(root3))  # 0
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只访问一次，就像“一遍走遍所有房间”。  
- **空间复杂度**：`O(h)`（递归栈），`h` 为树的高度。最坏情况下 `h = n`（链状树），相当于“递归深度和节点数一样多”。  

---

## 心得

- **核心技巧**：在树的 DFS 中**同时记录两种状态**（向左起、向右起），并利用子节点的状态来递推出父节点的状态。  
- **适用的题型**：  
  1. “最长交替路径”类（如二叉树中交替颜色、交替增减等）。  
  2. “从节点出发的两种方向”问题（如最长单调递增/递减路径）。  
  3. “状态压缩 DP”在树上应用的例子（如树形背包、树形最长路径）。  
- **一句话总结解题钥匙**：**把每个节点的“向左”和“向右”两条信息存起来，递归合并即可，一遍遍历搞定全部。**

---

## 反思

- **第一反应**：看到“ZigZag”，立刻想到“左‑右交替”，于是想遍历每个节点并尝试两种起始方向——这就是暴力思路。  
- **最容易踩的坑**：  
  - **空子树的处理**：递归返回 `-1` 而不是 `0`，否则会多算一次步数。  
  - **全局最大值的更新**：一定要在每个节点处比较 `left_len` 与 `right_len`，否则只会得到某条单一路径的长度。  
  - **递归深度**：树可能很深（10⁴），在 Python 中递归深度默认 1000，需要在提交时使用 `sys.setrecursionlimit(10**6)`（这里省略，平台一般已处理）。  
- **下次思路**：遇到“从节点出发的交替/单调路径”时，第一步就**思考是否可以把“方向”作为状态**，然后用一次 DFS 同时返回所有状态，避免重复遍历。这样往往能把 `O(n²)` 降到 `O(n)`。