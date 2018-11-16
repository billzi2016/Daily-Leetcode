# #173. 二叉搜索树迭代器 / Binary Search Tree Iterator

> 难度：中等 · 标签：Stack、Tree、Design、Binary Search Tree、Binary Tree、Iterator · [LeetCode 链接](https://leetcode.com/problems/binary-search-tree-iterator/)

---

## 题目（英文原版）

**Description**

Implement the BSTIterator class that represents an iterator over the in-order traversal of a binary search tree (BST):
Notice that by initializing the pointer to a non-existent smallest number, the first call to next() will return the smallest element in the BST.
You may assume that next() calls will always be valid. That is, there will be at least a next number in the in-order traversal when next() is called.
Follow up:

**Examples**

**Example 1:**

```
Input
["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
[[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
Output
[null, 3, 7, true, 9, true, 15, true, 20, false]

Explanation
BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
bSTIterator.next();    // return 3
bSTIterator.next();    // return 7
bSTIterator.hasNext(); // return True
bSTIterator.next();    // return 9
bSTIterator.hasNext(); // return True
bSTIterator.next();    // return 15
bSTIterator.hasNext(); // return True
bSTIterator.next();    // return 20
bSTIterator.hasNext(); // return False
```

**Constraints**

- The number of nodes in the tree is in the range [1, 105].
- 0 <= Node.val <= 106
- At most 105 calls will be made to hasNext, and next.

---

## 题目（中文翻译）

实现 BSTIterator 类，使其能够对二叉搜索树（binary search tree，BST）进行中序遍历（in-order traversal）的迭代操作。  
注意：通过将指针初始化到一个不存在的最小值，第一次调用 `next()` 时会返回 BST 中的最小元素。  
可以假设所有对 `next()` 的调用都是合法的，即在调用 `next()` 时中序遍历中必然还有下一个节点。

**示例 1**

```json
Input
["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
[[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
Output
[null, 3, 7, true, 9, true, 15, true, 20, false]
```

**解释**

```java
BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
bSTIterator.next();    // 返回 3
bSTIterator.next();    // 返回 7
bSTIterator.hasNext(); // 返回 true
bSTIterator.next();    // 返回 9
bSTIterator.hasNext(); // 返回 true
bSTIterator.next();    // 返回 15
bSTIterator.hasNext(); // 返回 true
bSTIterator.next();    // 返回 20
bSTIterator.hasNext(); // 返回 false
```

**约束条件**

- 树中节点数范围为 `[1, 10^5]`。
- `0 <= Node.val <= 10^6`。
- `hasNext` 与 `next` 的调用总次数不超过 `10^5` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一次性把整棵二叉搜索树的中序遍历序列全部算出来**，保存到一个列表里。  
- 中序遍历（左 → 根 → 右）恰好会得到递增的节点值，这正是题目要求的遍历顺序。  
- 把所有值存进列表后，`next()` 只需要返回列表的下一个元素，`hasNext()` 只要判断指针是否已经到了列表末尾即可。

> **类比**：把树想成一本字典，字典里每个单词都有对应的页码。我们一次性把所有单词按照字母顺序排好（这一步相当于中序遍历），放进一个“目录”列表里。以后要找下一个单词，只需要顺着目录往后走一步，根本不必再去翻整本字典。

这个方法一定能得到正确答案，因为中序遍历的定义保证了顺序是从最小到最大，而我们没有改变这个顺序，只是把它提前算好、保存下来。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    def __init__(self, root: TreeNode):
        """构造函数：一次性完成全部中序遍历并保存到 self.seq"""
        self.seq = []          # 用来存放遍历结果的列表
        self._inorder(root)   # 私有方法，递归遍历
        self.idx = 0           # 指向下一个要返回的元素下标

    def _inorder(self, node: TreeNode):
        """递归的中序遍历：左 → 根 → 右"""
        if not node:
            return
        self._inorder(node.left)   # 先遍历左子树
        self.seq.append(node.val)  # 再访问根节点
        self._inorder(node.right)  # 最后遍历右子树

    def next(self) -> int:
        """返回当前指针指向的值，并把指针向后移动一位"""
        val = self.seq[self.idx]   # 取出答案
        self.idx += 1              # 指针右移
        return val

    def hasNext(self) -> bool:
        """只要指针还没到列表末尾，就说明还有下一个元素"""
        return self.idx < len(self.seq)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 初始化时要遍历所有 `n` 个节点一次，构造列表的过程是线性的。  
  - 之后 `next()`、`hasNext()` 都是 `O(1)`（常数时间），因为只做下标访问。

- **空间复杂度**：`O(n)`  
  - 需要额外的列表来存放全部节点值，最坏情况下会占用和树节点数相同的空间。

---

### 2. 最优解

#### 思路  

虽然暴力解很直观，但它在 **空间** 上用了 `O(n)`，当树非常大（如 `10⁵` 个节点）时会占用大量内存。  
我们要 **只在需要时才展开遍历**，即每次调用 `next()` 时才“走到”下一个最小节点，而不是一次性把全部节点都展开。

**关键点**：二叉搜索树的中序遍历可以用 **栈** 来模拟递归过程。栈里保存的是**沿着左子树一直往下走时遇到的节点**。  
- 当我们想得到下一个最小元素时，栈顶就是当前最小的未访问节点。  
- 访问完栈顶后，需要把它的右子树的最左边节点全部压入栈，这样下一个最小节点又会出现在栈顶。

> **类比**：把树看成一条蜿蜒的山路，左子树是往下坡，右子树是上坡。我们把沿着下坡一路上所有的“路标”（节点）放进背包（栈）里。每次走到一个路标（`next()`），如果这段路标后面还有上坡（右子树），我们再把上坡路上所有的下坡路标装进背包，保证背包顶端永远是最近的下一个路标。

**为什么快**  
- 每个节点只会被 **压栈一次、弹栈一次**，所以总体的工作量仍是 `O(n)`，但分摊到每一次 `next()` 调用上，平均是 `O(1)`（摊销分析）。  
- 只保存从根到当前节点的路径，最多是树的高度 `h`，空间从 `O(n)` 降到 `O(h)`，在平衡树中 `h ≈ log n`。

#### 代码（Python）

```python
class BSTIterator:
    def __init__(self, root: TreeNode):
        """
        初始化时，只把左子树一路向下的节点压入栈，
        这样栈顶就是当前最小的节点（即第一个要返回的节点）。
        """
        self.stack = []          # 用列表模拟栈
        self._push_left_branch(root)

    def _push_left_branch(self, node: TreeNode):
        """
        把从 node 开始一直向左的所有节点压入栈，
        直到左子树到底（node 为 None）。
        """
        while node:
            self.stack.append(node)   # 压栈
            node = node.left          # 往左走

    def next(self) -> int:
        """
        弹出栈顶节点，它就是当前未访问的最小节点。
        然后把该节点的右子树的左边界全部压栈，
        为后续的 next() 做准备。
        """
        # 弹出最小节点
        node = self.stack.pop()
        val = node.val               # 记录返回值

        # 如果有右子树，需要把右子树的最左边节点全部压栈
        if node.right:
            self._push_left_branch(node.right)

        return val

    def hasNext(self) -> bool:
        """只要栈不为空，就说明还有未访问的节点"""
        return len(self.stack) > 0
```

#### 复杂度  

- **时间复杂度**：`O(1)`（摊销）  
  - 单次 `next()` 可能会把右子树的左链压栈，这一步的节点数在整个遍历过程中只会累计到 `n`。所以 **平均** 每次 `next()` 只花常数时间。  
  - `hasNext()` 只检查栈是否为空，显然是 `O(1)`。

- **空间复杂度**：`O(h)`，`h` 为树的高度  
  - 栈里最多只会保存从根到当前节点的路径，最坏情况下是树的深度。对于平衡二叉搜索树，`h ≈ log₂ n`，远小于 `n`。

---

## 心得

- **核心技巧**：使用 **栈模拟递归的中序遍历**，实现“惰性遍历”。  
- **适用的题型**  
  1. “二叉树的迭代器”系列（如前序、后序遍历迭代器）。  
  2. “在二叉搜索树中查找第 k 小/大的元素”。  
  3. “利用栈实现树的深度优先搜索（DFS）”。  
- **一句话总结**：**把左子树一路压栈，栈顶永远是下一个最小值**，每次弹栈后把右子树的左链再压进去。

---

## 反思

- **第一反应**：直接把整棵树遍历一遍，存进数组里，这样实现最直接。  
- **最容易踩的坑**  
  - **忘记在 `next()` 后处理右子树**：如果只弹栈不压右子树的左链，后面的元素顺序会错。  
  - **边界条件**：空树或只有一个节点时，初始化和 `hasNext()` 的判断要正确。  
  - **空间误判**：把所有节点都放进列表会导致 `O(n)` 内存，违背题目“Follow up”对空间的要求。  
- **下次类似题的第一步**：**先想“只保存路径上的节点”，用栈或递归模拟遍历的状态**，而不是一次性把所有结果全部存下来。