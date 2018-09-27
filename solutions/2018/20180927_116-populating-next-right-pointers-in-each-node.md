# #116. 填充每个节点的下一个右侧指针 / Populating Next Right Pointers in Each Node

> 难度：中等 · 标签：Linked List、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/)

---

## 题目（英文原版）

**Description**

You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:
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
Input: root = [1,2,3,4,5,6,7]
Output: [1,#,2,3,#,4,5,6,7,#]
Explanation: Given the above perfect binary tree (Figure A), your function should populate each next pointer to point to its next right node, just like in Figure B. The serialized output is in level order as connected by the next pointers, with '#' signifying the end of each level.
```

**Example 3:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 212 - 1].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵 **完美二叉树（perfect binary tree）**，其所有叶子节点都位于同一层，并且每个父节点恰好有两个子节点。二叉树的节点定义如下：

```cpp
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;   // 指向下一个右侧节点的指针
}
```

请为每个节点的 **next 指针（next pointer）** 填入指向其右侧相邻节点的指针。如果该节点右侧没有节点，则将 **next 指针** 设为 `NULL`。最初，所有节点的 **next 指针** 均为 `NULL`。

---

## 示例

### 示例 1  

**输入**  
```cpp
struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
```

（此处仅展示节点结构定义，实际输入为对应的树）

### 示例 2  

**输入**  
```
root = [1,2,3,4,5,6,7]
```

**输出**  
```
[1,#,2,3,#,4,5,6,7,#]
```

**解释**  
如图 A 所示的完美二叉树，函数应将每个节点的 **next 指针** 指向其右侧相邻节点，形成图 B 的效果。序列化输出采用层序遍历的方式，并使用 `#` 表示每一层的结束。

### 示例 3  

**输入**  
```
root = []
```

**输出**  
```
[]
```

---

## 约束

- 树中节点的数量在区间 `[0, 212 - 1]` 内。  
- `-1000 <= Node.val <= 1000`

---

## 进阶

（原题目中提供的进阶提示，此处保持标题）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法是 **层序遍历**（Breadth‑First Search），把每一层的节点一个接一个地取出来，然后把它们的 `next` 指针依次指向同层的下一个节点。  
- **队列**（Queue）是实现层序遍历的常用工具。可以把它想象成排队买票的队伍，最先进入队列的节点最先被处理。  
- 把根节点放进队列后，每次取出队首节点，并把它的左子节点、右子节点（如果有）依次加入队列，这样队列里永远保持的是 **按层次顺序** 的节点。  
- 当我们遍历完当前层的所有节点（可以通过记录当前层的节点数来判断）后，就把最后一个节点的 `next` 设为 `None`（在 Python 中默认就是 `None`），随后进入下一层的遍历。

这个方法之所以一定能得到正确答案，是因为我们严格按照层的顺序访问每个节点，并且在同一层内部按照从左到右的顺序依次链接 `next`，正好满足题意。

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


from collections import deque

def connect(root: 'Node') -> 'Node':
    if not root:                      # 空树直接返回 None
        return None

    q = deque([root])                 # 用双端队列模拟普通队列
    while q:
        level_size = len(q)           # 当前层有多少节点
        prev_node = None              # 记录前一个已经处理的节点

        for _ in range(level_size):
            node = q.popleft()        # 取出队首节点（最早进队的）

            # 把前一个节点的 next 指向当前节点
            if prev_node:
                prev_node.next = node
            prev_node = node          # 更新 prev_node 为当前节点

            # 将子节点加入队列，保证下一轮可以遍历下一层
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        # 本层最后一个节点的 next 已经是默认的 None，无需额外处理
    return root
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  这里的 `N` 是树中节点的总数。我们把每个节点恰好访问一次，和“遍历一次所有节点”是同等规模的。  
  用大白话说，就是如果树里有 1000 个节点，算法大约会跑 1000 步左右。

- **空间复杂度：** `O(W)`，其中 `W` 为任意一层的最大节点数（即树的宽度）。  
  对于完美二叉树，最宽的一层大约有 `N/2` 个节点，所以最坏情况下需要的额外空间接近 `N/2`。可以把它想象成排队买票时，最拥挤那一层需要站多少人。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **额外的队列空间**：我们用了 `O(N)` 的额外存储，而题目要求 **常数级额外空间**（不计递归栈）。  
观察题目特性：

1. **完美二叉树**：每个父节点都有左右两个子节点，且所有叶子在同一层。  
2. 我们已经要把每层的节点通过 `next` 指针串起来——这本身就可以成为遍历下一层的“桥梁”。  

思路步骤：

- **利用已建立的 `next` 链**：当我们完成第 `i` 层的 `next` 链接后，第 `i+1` 层的所有节点可以通过第 `i` 层的 `next` 指针依次访问。  
- **逐层向下**：从根节点开始，遍历每一层的节点（使用 `next` 指针而不是队列），在遍历的过程中把它们的子节点（左、右）相互链接。  
- **内部链接规则**  
  - 对同一个父节点，`parent.left.next = parent.right`（左孩子的 `next` 指向右孩子）。  
  - 对相邻的父节点，`parent.right.next = parent.next.left`（右孩子的 `next` 指向下一个父节点的左孩子）。  
- 当当前层的最右边节点的 `right` 已经没有右邻居时，它的 `next` 保持 `None`。  
- 完成一层后，进入下一层：只需要把指针移动到当前层最左边的节点的左子节点即可（因为是完美二叉树，左子节点一定存在，除非已经到底部）。

通过这套方式，我们只用了 **几个指针变量**，没有额外的容器，满足了常数空间的要求。

#### 代码（Python）

```python
# Definition for a Node (同上)
class Node:
    def __init__(self, val: int = 0,
                 left: 'Node' = None,
                 right: 'Node' = None,
                 next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def connect(root: 'Node') -> 'Node':
    if not root:
        return None

    # level_start 始终指向当前层最左侧的节点
    level_start = root

    while level_start.left:          # 只要还有下一层（完美二叉树保证 left 存在）
        cur = level_start            # cur 用来遍历当前层的所有节点

        while cur:
            # 1) 同一父节点的左右孩子相连
            cur.left.next = cur.right

            # 2) 当前节点的右孩子指向下一个父节点的左孩子（如果有 next）
            if cur.next:
                cur.right.next = cur.next.left

            # 移动到当前层的下一个节点
            cur = cur.next

        # 进入下一层：左子节点一定存在
        level_start = level_start.left

    return root
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  每个节点只被访问一次（在它所在的层做常数次操作），所以时间仍然是线性的。  
  与暴力解相比，步数相同，只是省掉了队列的“进出”开销。

- **空间复杂度：** `O(1)`（常数级）  
  只用了几个指针变量 `level_start`、`cur`，不随树的大小增长。  
  用生活化的说法，就是我们只需要准备几根绳子来把树的每层串起来，而不需要额外的“大箱子”来装节点。

---

## 心得

- **核心技巧**：**利用已建立的指针（next）在同层遍历**，从而在 O(1) 额外空间内完成层序链接。  
- **适用的题型**：  
  1. “Populating Next Right Pointers in Each Node” 系列（包括非完美二叉树的变体）。  
  2. “Binary Tree Right Side View”——需要按层遍历但可以利用 `next` 来简化。  
  3. “Flatten Binary Tree to Linked List”——把树的结构改写为链表，同样可以使用指针“搬砖”。  
- **一句话总结**：**把“层序遍历”从“借助队列”转为“借助已连好的 next 指针”。**

## 反思

- **第一反应**：看到“next 指针”立刻想到层序遍历，用队列把每层节点拿出来再手动连接。  
- **最容易踩的坑**：  
  - 忘记在同层的 **相邻父节点** 之间也要建立链接（`cur.right.next = cur.next.left`），导致右侧子树的 `next` 仍为 `None`。  
  - 对空树或只有根节点的特殊情况没有提前返回。  
  - 在循环条件里写成 `while level_start` 会导致在叶子层仍继续循环，需要检测 `level_start.left` 是否为空。  
- **下次第一步**：先确认是否可以利用已有的指针结构（如 `next`、父指针）在 **同层** 直接遍历，若可以，就尝试 O(1) 空间的层序遍历方案。