# #117. 填充每个节点的下一个右侧指针 II / Populating Next Right Pointers in Each Node II

> 难度：中等 · 标签：Linked List、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)

---

## 题目（英文原版）

**Description**

Given a binary tree
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.
Initially, all next pointers are set to NULL.
Follow-up:

**Examples**

**Example 1:**

```
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
```

**Example 2:**

```
Input: root = [1,2,3,4,5,null,7]
Output: [1,#,2,3,#,4,5,7,#]
Explanation: Given the above binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.
```

**Example 3:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 6000].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树（binary tree），请为每个节点填充其 **next 指针**（next pointer），使其指向右侧的下一个节点。如果右侧不存在下一个节点，则 **next 指针** 应设为 `NULL`。最初，所有 **next 指针** 均为 `NULL`。

---

### 示例 1  

```cpp
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
```

### 示例 2  

**输入**  
`root = [1,2,3,4,5,null,7]`

**输出**  
`[1,#,2,3,#,4,5,7,#]`

**解释**  
如图 A 所示的二叉树，函数应为每个节点的 **next 指针** 填充指向其右侧的下一个节点，结果如图 B 所示。序列化的输出采用层序遍历的方式，并按照 **next 指针** 的连接顺序排列，`'#'` 表示每一层的结束。

### 示例 3  

**输入**  
`root = []`

**输出**  
`[]`

---

### 约束条件

- 树中节点的数量范围为 `[0, 6000]`。
- `-100 <= Node.val <= 100`。

### 进阶

- 你能否在使用 **常数级额外空间**（即 O(1) 额外空间）的条件下完成此题？（递归调用栈的空间不计入额外空间）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直观的办法是 **层序遍历**（Breadth‑First Search），把每一层的所有节点取出来后，再把它们依次用 `next` 指针相连。  
- **层序遍历** 常用 **队列**（queue）实现。把根节点放进队列，每次弹出一个节点，把它的左、右子节点（如果有）再压进去。这样弹出的顺序恰好就是从上到下、从左到右的遍历顺序。  
- 当我们把同一层的所有节点弹完以后，就可以把它们按照弹出的顺序用 `next` 链接起来，最后一个节点的 `next` 设为 `None`（在 Python 中写成 `null`）。  

> 类比：队列就像排队买票的队伍，先进入的人先买票（先出），后进的排在后面。我们把每层的节点看成同一批人，等这批人全部买完票（出队）后，再把他们手拉手（设 `next`），最后一个人手里没有人，就留空。  

这个办法一定能得到正确的 `next` 指针，因为我们严格按照题目要求的“同一层从左到右”顺序去连接。  

#### 代码（Python）  

```python
# Definition for a Node.
class Node:
    def __init__(self, val: int = 0,
                 left: 'Node' = None,
                 right: 'Node' = None,
                 next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


from collections import deque   # deque 是双端队列，适合作为普通队列使用

def connect(root: 'Node') -> 'Node':
    """
    暴力层序遍历版
    """
    if not root:
        return None

    q = deque([root])          # 先把根放进队列
    while q:
        level_size = len(q)    # 当前层有多少节点
        prev_node = None       # 用来记录前一个弹出的节点
        for _ in range(level_size):
            node = q.popleft()          # 从队首取出一个节点
            if prev_node:               # 如果不是本层的第一个节点
                prev_node.next = node   # 前一个节点的 next 指向当前节点
            prev_node = node            # 更新 prev_node 为当前节点

            # 把左右孩子加入队列，供下一层使用
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        # 循环结束后，prev_node 是本层最后一个节点，它的 next 本来就是 None
        # （初始化时已经是 None，这里不必显式赋值）

    return root
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  每个节点恰好进入队列一次、弹出一次、检查左右子树一次，`n` 是树中节点数。  
- **空间复杂度：** `O(n)`（最坏情况）  
  队列里最多会同时存放同一层的所有节点。对于一棵完全二叉树，最底层大约有 `n/2` 个节点，空间随 `n` 成线性增长。  

---  

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于使用了额外的队列，空间是 `O(n)`。  
我们注意到题目已经为每个节点准备了一个 `next` 指针，**可以利用已经建立好的 `next` 链** 在同一层之间横向移动，从而在 **不额外使用队列** 的情况下完成层序遍历。  

核心想法如下：

1. **使用已经填好的 `next` 指针遍历当前层**  
   - 从当前层的最左侧节点 `head` 开始，沿着 `head.next` 一路向右，顺序访问这一层的所有节点。  

2. **在遍历当前层的同时，构造下一层的 `next` 链**  
   - 为下一层准备一个 “哑节点” `dummy`（值随意），它的 `next` 将指向下一层的第一个真实节点。  
   - 再用一个指针 `tail`（最初指向 `dummy`），每当我们在当前层看到一个子节点（左或右），就把 `tail.next` 指向这个子节点，并把 `tail` 前进到这个子节点。这样，所有子节点会按照从左到右的顺序被串成一条链。  

3. **层与层之间的切换**  
   - 当当前层遍历结束（`head` 为 `None`），`dummy.next` 就是下一层的最左节点。把 `head` 移到 `dummy.next`，再把 `dummy.next` 清空，继续处理下一层。  

> 类比：想象每层的节点已经手拉手组成了一条“人链”。我们站在这条链的最左端，顺着手（`next`）走过去，沿路把每个人的孩子（左、右）拉成另一条新的人链（用 `dummy` 和 `tail` 维护）。当这层走完后，我们直接跳到新链的开头继续走。整个过程不需要额外的排队队伍（队列），只用了几根手（指针）。  

这个思路的关键在于 **一次遍历同时完成两件事**：读取当前层、构造下一层。因为每个节点只被访问一次，时间仍是 `O(n)`，而额外空间只用了常数个指针 `O(1)`。

#### 代码（Python）  

```python
def connect(root: 'Node') -> 'Node':
    """
    O(1) 额外空间的层序遍历（利用 next 指针）
    """
    if not root:
        return None

    # head 指向当前层的最左侧节点
    head = root

    while head:
        dummy = Node(0)   # 哑节点，帮助我们连接下一层
        tail = dummy      # tail 永远指向已连接好的链的最后一个节点

        # 遍历当前层，使用已经建立好的 next 指针
        cur = head
        while cur:
            if cur.left:          # 若左子节点存在，就接到 tail 后面
                tail.next = cur.left
                tail = tail.next
            if cur.right:         # 若右子节点存在，也接到 tail 后面
                tail.next = cur.right
                tail = tail.next
            cur = cur.next        # 沿着本层的 next 向右移动

        # 完成本层后，dummy.next 指向下一层的最左节点
        head = dummy.next         # 进入下一层
        # 循环结束后，所有 next 指针已经正确链接

    return root
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  每个节点只被访问一次（一次作为当前层的 `cur`，一次作为子节点被 `tail` 链接），所以整体线性。  
- **空间复杂度：** `O(1)`（不计递归栈）  
  只用了常数个额外指针 `head、dummy、tail、cur`，不随节点数量增长。相比暴力解省掉了队列的 `O(n)` 空间。  

---  

## 心得  

- **核心技巧**：在已有的 `next` 指针上做“横向遍历”，配合哑节点 (`dummy`) 与尾指针 (`tail`) 逐层构造下一层的链表，实现 **常数空间的层序遍历**。  
- **适用场景**  
  1. 本题系列的第 1 题 “Populating Next Right Pointers in Each Node” （完全二叉树），同样可以用 `next` + `dummy` 的思路，只是因为是满二叉树可以更简化。  
  2. “Binary Tree Level Order Traversal II” 需要倒序层序输出，也可以在遍历时利用 `next` 指针实现 O(1) 空间。  
  3. “Flatten Binary Tree to Linked List” 中把树展开为链表时，也会使用类似的“先遍历后链接”思路。  

> **解题钥匙**：**把已知的指针当作“通道”，在通道上走的同时再铺设下一层的通道**。  

---  

## 反思  

- **第一反应**：立刻想到 BFS + 队列，因为层序遍历最自然。  
- **最容易踩的坑**  
  - 忘记在遍历当前层时把 `next` 指针已经设置好的节点也当作 “已经访问” 的节点，导致出现环或重复连接。  
  - 对空树或只有一个节点的极端情况没有提前返回，代码会报空指针错误。  
  - 在使用哑节点时忘记把 `tail` 移动到新接入的节点，导致所有子节点都指向同一个节点。  
- **下次类似题的第一步**：先判断是否可以 **复用已有指针**（如 `next`、`parent`） 来 **省去额外空间**，如果不行再考虑显式的数据结构（队列、栈）。  

祝你在树的世界里“一指穿梭”，快速连通每一层！