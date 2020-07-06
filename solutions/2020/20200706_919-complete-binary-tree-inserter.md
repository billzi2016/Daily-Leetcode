# #919. 完全二叉树插入器 / Complete Binary Tree Inserter

> 难度：中等 · 标签：Tree、Breadth-First Search、Design、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/complete-binary-tree-inserter/)

---

## 题目（英文原版）

**Description**

A complete binary tree is a binary tree in which every level, except possibly the last, is completely filled, and all nodes are as far left as possible.
Design an algorithm to insert a new node to a complete binary tree keeping it complete after the insertion.
Implement the CBTInserter class:

**Examples**

**Example 1:**

```
Input
["CBTInserter", "insert", "insert", "get_root"]
[[[1, 2]], [3], [4], []]
Output
[null, 1, 2, [1, 2, 3, 4]]

Explanation
CBTInserter cBTInserter = new CBTInserter([1, 2]);
cBTInserter.insert(3);  // return 1
cBTInserter.insert(4);  // return 2
cBTInserter.get_root(); // return [1, 2, 3, 4]
```

**Constraints**

- The number of nodes in the tree will be in the range [1, 1000].
- 0 <= Node.val <= 5000
- root is a complete binary tree.
- 0 <= val <= 5000
- At most 104 calls will be made to insert and get_root.

---

## 题目（中文翻译）

**描述**  
完全二叉树（complete binary tree）是一种二叉树，除最后一层外，每一层的节点数都达到最大，并且所有节点都尽可能靠左。  
设计一种算法，在保持完全二叉树性质的前提下向其插入一个新节点。  
实现 `CBTInserter` 类，使其能够完成上述操作。

**实现 `CBTInserter` 类**  
（题目中会给出具体的类接口要求，此处略）

**示例 1**  

```json
Input
["CBTInserter", "insert", "insert", "get_root"]
[[[1, 2]], [3], [4], []]

Output
[null, 1, 2, [1, 2, 3, 4]]
```

**解释**  
```java
CBTInserter cBTInserter = new CBTInserter([1, 2]);
cBTInserter.insert(3);  // 返回 1
cBTInserter.insert(4);  // 返回 2
cBTInserter.get_root(); // 返回 [1, 2, 3, 4]
```

**约束条件**  

- 树中节点的数量在 `[1, 1000]` 区间内。  
- `0 <= Node.val <= 5000`。  
- 给定的 `root` 必须是一棵完全二叉树。  
- `0 <= val <= 5000`。  
- 最多会调用 `insert` 和 `get_root` 方法 `10^4` 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：每次要插入一个新节点时，都从根节点开始**层序遍历**（即 **广度优先搜索 BFS**），  
找到第一个“左孩子或右孩子为空”的位置，然后把新节点挂上去。  

- **层序遍历**可以想象成排队买票：我们从前往后依次检查每个人是否还有空位坐（左/右孩子），  
  第一个发现还有空位的人，就是我们要把新朋友坐进去的位置。  
- **队列（Queue）**在这里相当于“排队的队伍”。我们把每访问到的节点依次放进队列，随后弹出检查。

只要把新节点挂在第一个缺位的位置，二叉树必然仍保持**完全二叉树**的性质——因为完全二叉树的定义恰好是“从上到下、从左到右依次填满”。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class CBTInserter:
    def __init__(self, root: TreeNode):
        """把根节点保存下来，后面插入时会用到"""
        self.root = root

    def insert(self, val: int) -> int:
        """暴力 BFS 找到第一个缺少子节点的父节点并插入"""
        from collections import deque
        q = deque([self.root])                     # 队列初始化，只装根节点
        while q:
            node = q.popleft()                     # 取出队首节点
            # 先检查左孩子
            if not node.left:                      # 左孩子为空 → 把新节点挂左边
                node.left = TreeNode(val)
                return node.val                   # 返回父节点的值
            else:
                q.append(node.left)                # 左孩子不为空，加入队列待检查

            # 再检查右孩子
            if not node.right:                     # 右孩子为空 → 把新节点挂右边
                node.right = TreeNode(val)
                return node.val
            else:
                q.append(node.right)               # 右孩子不为空，加入队列

        # 理论上不会走到这里，因为题目保证一定能插入
        return -1

    def get_root(self) -> TreeNode:
        """直接返回根节点"""
        return self.root
```

> 关键行的中文注释已经写在代码里，直接复制粘贴即可运行。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - “n” 是当前树的节点数。因为每次 `insert` 都要从根开始层序遍历，最坏情况下要遍历到倒数第二层的所有节点才能找到空位。  
  - 用大白话说，就是“插入一次可能要检查整棵树”，所以如果你插入 1000 次，最坏会检查 1000 × 1000 次节点。

- **空间复杂度**：`O(n)`  
  - BFS 用的队列在最坏情况下会装下树的 **一层** 节点，完整二叉树的最宽一层大约是 `n/2`，所以空间也跟节点数成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次插入都重新遍历整棵树**。其实我们可以把“哪些节点还有空位”这件事**提前做好**，插入时直接使用它们，省掉重复遍历。

**核心想法**：维护一个**只装“尚未填满的节点”的队列**（记作 `candidate`），
- 队首永远是当前最左、最上面的缺位父节点；
- 当它的左孩子或右孩子被填满后，如果两个孩子都已存在，就把它从队列弹出；
- 新插入的节点本身暂时没有孩子，所以它本身也是一个“候选父节点”，要加入队列的尾部。

这样，**每次 `insert` 只做 O(1) 次操作**（检查队首、挂左/右孩子、可能弹出/加入），而不需要再遍历整棵树。

实现步骤：

1. **初始化**  
   - 对给定的根节点做一次 BFS。  
   - 把所有“左或右孩子缺失”的节点加入 `candidate` 队列。  
   - 这一步只做一次，耗时 `O(n)`，之后的插入都很快。

2. **插入**  
   - 取 `candidate` 队首 `parent`。  
   - 如果 `parent.left` 为空，就把新节点挂左边；否则挂右边。  
   - 挂完后，如果 `parent` 已经有左右孩子（即已满），就把它弹出 `candidate`。  
   - 把新节点（它本身是空的）加入 `candidate` 队尾，以备以后继续插入。

3. **获取根节点**  
   - 直接返回保存的根引用即可。

下面用**排队买票**的类比帮助理解：  
- `candidate` 队列就是“还有空位的座位”。我们一开始把所有有空位的座位排好队。  
- 每来一个新朋友（插入节点），我们让他坐在队首的空位上（左或右）。坐满后，这个座位就不再出现在候补队列里。新朋友本身的座位（左、右都空）会被加入队列，等待后面的人来坐。

#### 代码（Python）

```python
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class CBTInserter:
    def __init__(self, root: TreeNode):
        """
        初始化时做一次完整的层序遍历，把所有“还缺孩子”的节点放进 candidate 队列。
        这样后续插入只需要 O(1) 时间。
        """
        self.root = root
        self.candidate = deque()          # 只装未满的节点

        q = deque([root])
        while q:
            node = q.popleft()
            # 若当前节点左或右有空位，加入候选队列
            if not node.left or not node.right:
                self.candidate.append(node)

            # 继续层序遍历子树
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

    def insert(self, val: int) -> int:
        """
        O(1) 插入：直接使用 candidate 队首节点作为父节点。
        返回插入后父节点的值。
        """
        parent = self.candidate[0]        # 队首一定是最左、最高的缺位父节点
        new_node = TreeNode(val)

        # 按完全二叉树的规则先填左孩子，再填右孩子
        if not parent.left:
            parent.left = new_node
        else:                              # left 已经有了，只剩右孩子
            parent.right = new_node
            # 此时 parent 已经满了，弹出队首
            self.candidate.popleft()

        # 新节点本身没有孩子，必然是候选父节点，加入队尾
        self.candidate.append(new_node)

        return parent.val                 # 按题目要求返回父节点的值

    def get_root(self) -> TreeNode:
        """直接返回根节点"""
        return self.root
```

#### 复杂度  

- **时间复杂度**：`O(1)`（摊销）  
  - 插入时只做常数次指针检查、赋值、队列的 push/pop，和树的大小无关。  
  - 与暴力解的 `O(n)` 对比，**即使插入 10⁴ 次，也只需要几百步操作**。

- **空间复杂度**：`O(n)`  
  - `candidate` 队列最多保存所有**未满**的节点。  
  - 在完全二叉树中，未满的节点最多只会出现在**倒数第二层**，数量约为 `n/2`，仍然是线性空间。  
  - 与暴力解相比，额外空间只是一小部分（不需要每次都重新创建队列）。

---

## 心得

- **核心技巧**：利用**额外的数据结构（候选队列）**把“需要重复检查的状态”提前缓存，实现 **常数时间插入**。  
- **适用场景**  
  1. **完全二叉树/堆的动态维护**（如实现自定义的堆插入）。  
  2. **层序遍历的增量更新**（如动态添加节点的 BFS 维护）。  
  3. **需要频繁查询“第一个满足条件的元素”** 的情形（如滑动窗口最大值的单调队列）。  
- **一句话总结**：把“缺位的父节点”提前放进队列，插入时直接取，用 O(1) 完成。

---

## 反思

- **第一反应**：看到“完整二叉树”，自然想到层序遍历，因为它恰好对应从左到右、从上到下的填充顺序。于是想到每次都遍历找空位——这就是暴力解。  
- **最容易踩的坑**  
  1. **忘记在初始化时把所有缺位节点都加入队列**，导致后续插入找不到正确父节点。  
  2. **插入后没有把新节点加入候选队列**，会导致后面再插入时找不到空位。  
  3. **返回值写错**：题目要求返回**父节点的值**，而不是新节点的值。  
- **下次遇到同类题**，第一步应思考**“哪些信息在后续操作中会被重复查询？”**，把这些信息预先保存（如队列、栈、哈希表），再设计**增量更新**的方式。这样往往能把原本的 O(n) 操作降到 O(1)。