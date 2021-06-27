# #1379. 在克隆二叉树中找到对应的节点 / Find a Corresponding Node of a Binary Tree in a Clone of That Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/find-a-corresponding-node-of-a-binary-tree-in-a-clone-of-that-tree/)

---

## 题目（英文原版）

**Description**

Given two binary trees original and cloned and given a reference to a node target in the original tree.
The cloned tree is a copy of the original tree.
Return a reference to the same node in the cloned tree.
Note that you are not allowed to change any of the two trees or the target node and the answer must be a reference to a node in the cloned tree.
Follow up: Could you solve the problem if repeated values on the tree are allowed?

**Examples**

**Example 1:**

```
Input: tree = [7,4,3,null,null,6,19], target = 3
Output: 3
Explanation: In all examples the original and cloned trees are shown. The target node is a green node from the original tree. The answer is the yellow node from the cloned tree.
```

**Example 2:**

```
Input: tree = [7], target =  7
Output: 7
```

**Example 3:**

```
Input: tree = [8,null,6,null,5,null,4,null,3,null,2,null,1], target = 4
Output: 4
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- The values of the nodes of the tree are unique.
- target node is a node from the original tree and is not null.

---

## 题目（中文翻译）

给定两棵二叉树 `original` 和 `cloned`，以及 `original` 树中一个指向节点 `target` 的引用。  
`cloned` 树是 `original` 树的完整拷贝。  
请返回 `cloned` 树中对应的节点引用。

> **注意**：不得修改任意一棵树或 `target` 节点，返回的答案必须是 `cloned` 树中的一个节点引用。

## 示例

### 示例 1  
**输入**  
```
tree = [7,4,3,null,null,6,19], target = 3
```  
**输出**  
```
3
```  
**解释**：在所有示例中，左侧展示的是原始树 `original`，右侧展示的是克隆树 `cloned`。绿色节点是原始树中的目标节点 `target`，黄色节点是克隆树中对应的节点，即答案。

### 示例 2  
**输入**  
```
tree = [7], target = 7
```  
**输出**  
```
7
```  

### 示例 3  
**输入**  
```
tree = [8,null,6,null,5,null,4,null,3,null,2,null,1], target = 4
```  
**输出**  
```
4
```  

## 约束条件

- 树中节点的数量在 `[1, 10^4]` 范围内。  
- 树中每个节点的值都是唯一的。  
- `target` 节点来自原始树 `original`，且非 `null`。

## 进阶

如果树中允许出现重复值，你能解决此问题吗？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **先在原树 `original` 中找到目标节点 `target` 的值**，再在克隆树 `cloned` 中把同样的值对应的节点找出来。  

- **用到的数据结构**：  
  - **二叉树的遍历**（可以用递归实现深度优先搜索，或者用队列实现广度优先搜索）。遍历二叉树就像在一棵“家谱树”里逐层或逐枝查找某个人。  
  - **哈希表**（可选）可以把遍历到的每个节点的值和节点本身存起来，类似于查字典：键是“名字”，值是“这个人所在的具体位置”。这里我们不一定需要哈希表，只需要一次遍历把值记下来即可。

- **为什么这个方法一定能找到答案**：  
  题目保证原树和克隆树的结构完全相同，且每个节点的值在整棵树里唯一。于是，只要在原树里找到了目标节点的值 `v`，在克隆树里搜索值为 `v` 的节点一定能找到对应的那个节点。

- **时间/空间复杂度**：  
  - 第一次遍历原树找到 `target` 的值，需要访问每个节点一次，**时间是 O(N)**（N 为节点数）。  
  - 第二次遍历克隆树找同值节点，又要访问每个节点一次，**时间仍是 O(N)**。两次遍历相加仍是 O(N)。  
  - 递归实现需要保存函数调用栈，最坏情况下树呈链状，栈深度是树的高度 `H`，**空间是 O(H)**（`H ≤ N`）。

> **大白话**：  
> “O(N)” 就是说如果树里有 1 000 000 个节点，程序大概会跑 1 000 000 次基本操作；  
> “O(H)” 就是说如果树很“瘦高”，比如像一根棍子，栈里最多会放 H = 1 000 000 层调用，最坏会占用和节点数同等的空间；如果树比较“矮胖”，比如满二叉树，`H` 只会是 `log₂N`（大约 20 层），占用的空间就很小。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def getTargetCopy(original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:
    """
    暴力解：先在 original 中找 target 的值，再在 cloned 中找同值节点。
    """
    # ---------- 第一步：在 original 中找到 target.val ----------
    def find_val(node: TreeNode, val: int) -> bool:
        if not node:
            return False
        if node.val == val:
            return True
        # 递归左、右子树
        return find_val(node.left, val) or find_val(node.right, val)

    target_val = target.val               # 目标节点的唯一值
    # 此处其实不需要显式检查是否真的在 original 中（题目已保证），
    # 只要记住 target_val 即可。

    # ---------- 第二步：在 cloned 中找同值节点 ----------
    def dfs(node: TreeNode) -> TreeNode:
        if not node:
            return None
        if node.val == target_val:        # 找到对应节点
            return node
        # 先左后右搜索
        left_res = dfs(node.left)
        if left_res:                      # 左子树已经找到
            return left_res
        return dfs(node.right)            # 继续右子树

    return dfs(cloned)                    # 返回克隆树中对应的节点
```

#### 复杂度

- **时间复杂度**：`O(N)` — 两次遍历每棵树各一次，总共访问不超过 `2N` 次，数量级仍是线性的 `N`。  
- **空间复杂度**：`O(H)` — 递归栈深度等于树的高度 `H`，最坏 `H = N`（链状），最优 `H = log₂N`（满二叉树）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **把两棵树分成了两次遍历**。其实我们可以在一次遍历的过程中 **同步走原树和克隆树**，当原树的指针正好指向 `target` 时，克隆树的指针自然就指向对应的节点，直接返回即可。

关键点：

1. **同步遍历**：从根节点开始，递归地同时向左子树、右子树前进。每一步我们都有一对“原树节点 `o`”和“克隆树节点 `c`”。  
2. **停止条件**：只要 `o` 正好等于 `target`（指针相等），说明我们已经在原树找到了目标，此时返回 `c`。  
3. **递归返回值**：如果左子树找到了对应节点，就直接返回；否则继续在右子树寻找。  
4. **为何是最优**：整个过程只遍历了每个节点一次，时间是 `O(N)`；递归栈深度仍是树的高度 `O(H)`，这已经是对这类树遍历的下界，无法再进一步降低。

> **从零解释核心概念**  
> - **深度优先搜索（DFS）**：把树看成一条条“道路”，每次沿着一条路一直走到底（左子树或右子树），再回头走另一条路。递归实现时，函数的调用本身就保存了“我现在在哪条路上”。  
> - **同步遍历**：把两棵结构相同的树想象成两条平行的道路，只要左脚在原树上走一步，右脚在克隆树上必须同步走一步，这样两只脚永远保持同一位置的对应关系。

#### 代码（Python）

```python
def getTargetCopy(original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:
    """
    最优解：一次同步遍历原树和克隆树，找到 target 时直接返回克隆树中的节点。
    """
    # 递归函数同时接受原树节点 o 和克隆树节点 c
    def dfs(o: TreeNode, c: TreeNode) -> TreeNode:
        if not o:                 # 到达空节点，说明这条路径上没有 target
            return None
        if o is target:           # 原树指针恰好等于目标指针
            return c              # 克隆树指针就是答案

        # 先在左子树同步搜索
        left_res = dfs(o.left, c.left)
        if left_res:              # 左子树已经找到答案，直接返回
            return left_res

        # 再在右子树同步搜索
        return dfs(o.right, c.right)

    return dfs(original, cloned)   # 从根节点开始同步遍历
```

#### 复杂度

- **时间复杂度**：`O(N)` — 每个节点至多访问一次，和暴力解相同，但只用了“一次遍历”。  
- **空间复杂度**：`O(H)` — 递归栈的深度仍然是树的高度。相比两次遍历的空间消耗没有增加，却省去了第二遍的时间开销。

---

## 心得

- **核心技巧**：同步深度优先遍历（或同步广度优先遍历），在遍历的同时比较原树指针与 `target`，一旦相等即返回克隆树对应指针。  
- **适用的题型**：  
  1. **在两棵结构相同的树之间寻找对应节点**（如本题）。  
  2. **在原树中定位某个节点后，在克隆树或镜像树中返回对应节点**。  
  3. **在两棵相似的图/树结构中同步搜索**（如“二叉树的镜像对应节点”）。
- **一句话总结解题钥匙**：**让两棵树“一起走”，当原树到达目标时，克隆树自然站在对应位置**。

---

## 反思

- **第一反应**：看到“原树”和“克隆树”，本能想到先分别遍历两遍——先找值再找对应节点。  
- **最容易踩的坑**：  
  - 把“值相同”当作唯一标识而直接用 `node.val == target.val`，在题目**允许重复值**的扩展版本中会出错。真正安全的做法是比较指针（`node is target`）。  
  - 递归实现时忘记在左子树返回 `None` 的情况下继续搜索右子树，导致只检查左子树。  
- **下次类似题的第一步**：先思考 **是否可以在一次遍历中同步进行两棵树的操作**，如果可以，就立刻把同步遍历写出来，而不是先拆成两次独立遍历。