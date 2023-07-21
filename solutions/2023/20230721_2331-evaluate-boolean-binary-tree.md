# #2331. 计算布尔二叉树 / Evaluate Boolean Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/evaluate-boolean-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a full binary tree with the following properties:
The evaluation of a node is as follows:
Return the boolean result of evaluating the root node.
A full binary tree is a binary tree where each node has either 0 or 2 children.
A leaf node is a node that has zero children.

**Examples**

**Example 1:**

```
Input: root = [2,1,3,null,null,0,1]
Output: true
Explanation: The above diagram illustrates the evaluation process.
The AND node evaluates to False AND True = False.
The OR node evaluates to True OR False = True.
The root node evaluates to True, so we return true.
```

**Example 2:**

```
Input: root = [0]
Output: false
Explanation: The root node is a leaf node and it evaluates to false, so we return false.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- 0 <= Node.val <= 3
- Every node has either 0 or 2 children.
- Leaf nodes have a value of 0 or 1.
- Non-leaf nodes have a value of 2 or 3.

---

## 题目（中文翻译）

You are given the root of a **full binary tree**（满二叉树） with the following properties:  

- **Leaf nodes**（叶子节点） have a value of `0` or `1`, representing `false` and `true` respectively.  
- **Non‑leaf nodes** have a value of `2` or `3`:
  - `2` 表示逻辑 **OR**（或）运算。  
  - `3` 表示逻辑 **AND**（与）运算。  
- The evaluation of a node is defined as:
  - If the node is a leaf, return its boolean value (`0 → false`, `1 → true`).  
  - Otherwise, recursively evaluate its two children, then apply the operator indicated by the node’s value (`OR` 或 `AND`).  

Return the boolean result of evaluating the **root node**.  

A **full binary tree** is a binary tree in which every node has either `0` or `2` children.  
A **leaf node** is a node that has zero children.  

---

### 示例

**示例 1**  

```
Input: root = [2,1,3,null,null,0,1]
Output: true
Explanation: 如上图所示的求值过程：
- AND 节点（值为 3）计算为 False AND True = False。  
- OR 节点（值为 2）计算为 True OR False = True。  
- 根节点的结果为 True，因此返回 true。
```

**示例 2**  

```
Input: root = [0]
Output: false
Explanation: 根节点是叶子节点，值为 0，代表 false，所以返回 false。
```

---

### 约束条件

- 树中节点的数量在 `[1, 1000]` 区间内。  
- `0 <= Node.val <= 3`。  
- 每个节点要么没有子节点，要么恰好有两个子节点。  
- 叶子节点的值只能是 `0` 或 `1`。  
- 非叶子节点的值只能是 `2` 或 `3`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是**把二叉树里的每个节点按照题目给出的规则算出一个布尔值**，最后把根节点的值返回。  
最直接的想法就是：

1. 从树的底部（叶子）开始往上算——这叫**后序遍历**（先左子树、后右子树、最后处理当前节点）。  
2. 递归（或栈）把每个节点的左、右子树的结果算好后，再根据当前节点的类型（`0/1`、`2`、`3`）合并得到它自己的布尔值。  

> **数据结构类比**  
> - **树**就像公司组织结构，叶子是最基层的员工，非叶子是部门经理。要知道部门的整体表现，需要先知道下属员工的表现。  
> - **哈希表**在这里并不需要，但如果你想把每个节点算好的结果记下来，以后重复使用，可以把它想成“字典”，key 是节点 id，value 是已经算好的布尔值。

这个方法一定能得到正确答案，因为我们严格遵循了题目给出的**每种节点的运算规则**，而且每个节点都会被访问一次。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 0/1 为叶子，2 为 AND，3 为 OR
        self.left = left
        self.right = right

def evaluateTree(root: TreeNode) -> bool:
    """
    暴力的后序遍历（递归版），把每个子树的布尔值算出来再合并
    """
    # 递归基：叶子节点，直接返回它的布尔值
    if not root.left and not root.right:          # 没有左子树也没有右子树 → 叶子
        return bool(root.val)                     # 0 → False, 1 → True

    # 递归求左、右子树的布尔值
    left_val = evaluateTree(root.left)            # 先算左边
    right_val = evaluateTree(root.right)          # 再算右边

    # 根据当前节点的类型合并结果
    if root.val == 2:                             # AND 节点
        return left_val and right_val
    else:                                         # OR 节点，题目保证只有 2 或 3
        return left_val or right_val
```

#### 复杂度  

- **时间复杂度：`O(n)`**  
  `n` 为树中节点数。我们对每个节点只访问一次（递归进入一次），所以时间随节点数线性增长。  
  “`O(n)`”可以想象成“如果树有 1000 个节点，就会做大约 1000 次计算”。

- **空间复杂度：`O(h)`**（`h` 为树的高度）  
  递归调用会占用栈空间，最坏情况下树是“链状”的，`h ≈ n`，此时需要 `O(n)` 的栈空间；在完全平衡的二叉树里，`h ≈ log₂ n`，只需要很少的空间。  

---

### 2. 最优解

#### 思路  

从暴力解来看，**唯一的瓶颈是递归调用本身的栈空间**。如果想把空间进一步压到 `O(1)`（不计返回值的存储），可以改用**显式栈的迭代后序遍历**，把递归改写成循环。思路如下：

1. 用一个栈 `stack` 保存待访问的节点，另一个集合 `visited`（或把节点的左/右子树结果临时存到节点本身）记录已经处理过左、右子树的节点。  
2. 每次弹出栈顶节点：  
   - 若它是叶子，直接得到布尔值并放进一个字典 `result`。  
   - 若它不是叶子且**左右子树都已经算好**（在 `result` 中），就根据 `AND/OR` 规则合并并存到 `result`。  
   - 否则，把当前节点重新压回栈顶，再把右子树、左子树依次压进去（保证左子树先被处理）。  

这样整个过程仍然是 **后序遍历**，但不依赖语言的递归栈，空间最多只需要 `O(h)`（栈的大小），在最坏情况下仍是 `O(n)`，但对一些语言或平台的递归深度限制更友好。

> **核心算法：后序遍历（Depth‑First Search）**  
> - **后序**的意义是“先把孩子们的结果算好，再算父亲”。可以把它想象成**先把配料准备好，最后再做菜**。  

#### 代码（Python）

```python
def evaluateTreeIter(root: TreeNode) -> bool:
    """
    迭代版后序遍历（显式栈），不使用系统递归
    """
    if not root:
        return False

    stack = [root]               # 待处理的节点栈
    result = {}                  # 记录每个节点算好的布尔值，key 为节点对象

    while stack:
        node = stack.pop()

        # 1️⃣ 叶子节点：直接把它的布尔值放进 result
        if not node.left and not node.right:
            result[node] = bool(node.val)
            continue

        # 2️⃣ 非叶子节点：检查左右子树是否已经算好
        left_done = node.left in result
        right_done = node.right in result

        if left_done and right_done:          # 左右都已经有结果 → 可以合并
            left_val = result[node.left]
            right_val = result[node.right]
            if node.val == 2:                 # AND
                result[node] = left_val and right_val
            else:                             # OR，题目保证是 3
                result[node] = left_val or right_val
        else:
            # 还有子树没有算好 → 先把当前节点压回去，等子树算完再来合并
            stack.append(node)               # 先把自己放回去，稍后再处理
            # 右子树先压，左子树后压 → 出栈顺序是左 → 右 → 父
            if not right_done:
                stack.append(node.right)
            if not left_done:
                stack.append(node.left)

    # 循环结束时，根节点的结果一定在 result 中
    return result[root]
```

#### 复杂度  

- **时间复杂度：`O(n)`**  
  每个节点仍然只会被压栈、弹栈、检查一次，整体操作次数与节点数成正比。与递归版的时间相同，只是实现方式不同。

- **空间复杂度：`O(h)`**（最坏 `O(n)`）  
  只使用了显式栈 `stack` 与结果字典 `result`。栈的最大深度等于树的高度 `h`，在平衡树时约为 `log₂ n`，在最坏的链状树时会退化到 `n`。相较于递归版，这种实现对语言的递归深度限制更安全。

---

## 心得

- **核心技巧**：后序遍历（DFS）配合**根据节点类型做布尔运算**。  
- **适用的题型**：  
  1. 计算表达式树的值（如 `+、-、*、/`）。  
  2. 判断二叉树是否满足某种“自底向上”的约束（如所有子树和等于父节点值）。  
  3. 树形 DP（每个节点的状态由子节点决定）。  
- **解题钥匙**：**“先把孩子算好，再算父亲”**——这句话提醒我们使用后序遍历。

---

## 反思

- **第一反应**：看到“叶子是 0/1，内部是 AND/OR”，立刻想到递归后序遍历，因为只有这样才能先拿到子树的布尔值。  
- **最容易踩的坑**：  
  - 忘记判断叶子节点的 **`not node.left and not node.right`**，导致把内部节点当成叶子误算。  
  - 对 `AND`/`OR` 的取值搞混（2 → AND，3 → OR）。  
  - 在迭代版里忘记把当前节点重新压回栈，导致子树算完后没有机会合并。  
- **下次遇到同类题**：第一步先**画出树的结构并标记每种节点的意义**，确认“从叶子往上合并”是自然的计算顺序，然后决定用递归还是显式栈实现后序遍历。