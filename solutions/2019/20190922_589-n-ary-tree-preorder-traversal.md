# #589. N叉树的前序遍历 / N-ary Tree Preorder Traversal

> 难度：简单 · 标签：Stack、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/n-ary-tree-preorder-traversal/)

---

## 题目（英文原版）

**Description**

Given the root of an n-ary tree, return the preorder traversal of its nodes' values.
Nary-Tree input serialization is represented in their level order traversal. Each group of children is separated by the null value (See examples)
Follow up: Recursive solution is trivial, could you do it iteratively?

**Examples**

**Example 1:**

```
Input: root = [1,null,3,2,4,null,5,6]
Output: [1,3,5,6,2,4]
```

**Example 2:**

```
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: [1,2,3,6,7,11,14,4,8,12,5,9,13,10]
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- 0 <= Node.val <= 104
- The height of the n-ary tree is less than or equal to 1000.

---

## 题目（中文翻译）

**描述**  
给定一棵 n叉树（n-ary tree）的根节点，返回其节点值的前序遍历（preorder traversal）。  
n叉树的序列化采用层序遍历的方式表示，每一组子节点之间使用 `null` 分隔（参见示例）。

**示例 1**  
Input: root = [1,null,3,2,4,null,5,6]  
Output: [1,3,5,6,2,4]

**示例 2**  
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]  
Output: [1,2,3,6,7,11,14,4,8,12,5,9,13,10]

**约束**  
- 树中节点的数量在 `[0, 10^4]` 范围内。  
- `0 <= 节点（Node）.val <= 10^4`。  
- n叉树的高度不超过 `1000`。

**进阶**  
递归解法比较直接，能否实现迭代解法？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观、最“笨”的办法就是**递归**地按照先序遍历的顺序访问每个节点：

1. 先把当前节点的值加入答案列表（相当于先读这本书的封面）。
2. 再依次对它的每一个子节点 **递归** 做同样的操作（把每个子树当成一本“小书”再从封面读起）。

这里用到的唯一数据结构是**列表**（`list`），用来把遍历得到的节点值一个一个地装进去。  
如果把树想象成公司组织结构图，递归就像让每个部门的负责人先报自己的名字，再把任务交给下属部门的负责人继续报——层层下去，最终把所有人的名字都收集完。

**为什么正确**  
先序遍历的定义正是“先访问根，再按照从左到右的顺序访问子树”。递归天然满足“先根后子树”，只要我们在递归函数里先把根加入答案，再递归遍历子节点，就一定得到符合要求的顺序。

#### 代码（Python）

```python
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val                 # 节点的数值
        self.children = children or []  # 子节点列表，默认空列表

def preorder(root: Node) -> list[int]:
    """
    递归实现 N 叉树的先序遍历
    """
    res = []                         # 用来存放遍历结果

    def dfs(node: Node):
        if not node:                 # 空树直接返回
            return
        res.append(node.val)         # ① 先把根节点的值加入答案
        for child in node.children:  # ② 依次递归遍历每个子节点
            dfs(child)

    dfs(root)                        # 从根节点开始递归
    return res
```

#### 复杂度

- **时间复杂度：** `O(N)`  
  这里的 `N` 是树中节点的总数。每个节点恰好被访问一次，做了常数次操作（加入列表、遍历子列表），所以整体时间随节点数线性增长。可以把 `O(N)` 想象成“走一遍所有房间”，房间越多，时间越长，正比关系。

- **空间复杂度：** `O(H)`（递归栈） + `O(N)`（答案列表）  
  - `O(H)`：递归调用会占用栈空间，最坏情况下树退化成链表，递归深度等于树高 `H`（≤1000），所以栈占用 `H` 层。  
  - `O(N)`：答案列表需要存放所有节点的值。若只关心额外空间（不计输出），则主要是递归栈 `O(H)`。

---

### 2. 最优解

#### 思路  

递归实现虽然代码简洁，但它会使用系统调用栈，**在极端深度（如 1000）时仍然安全**，但有的语言会因为栈溢出而报错。**面试官往往更关注**我们是否能用显式的数据结构自己实现遍历，即**迭代**版。

**慢在哪里？**  
递归的“慢点”其实不是时间，而是 **隐式使用系统栈**，我们无法控制其大小。若要求 **手动管理栈**，就需要把递归改写成 **显式栈 + 循环** 的形式。

**核心思路：**  
- 使用 **栈（stack）** 来模拟递归调用的过程。栈的特性是**后进先出（LIFO）**，正好对应递归的“回溯”。
- 先把根节点压入栈中。每次弹出栈顶节点：
  1. 把它的值加入答案（先序的 “根” 步骤）。
  2. 将它的子节点 **逆序** 压入栈中。逆序是关键：因为栈是后进先出，逆序压入后，最左边的子节点会最先被弹出，保证遍历顺序和递归一致。

**类比**：想象你有一叠待处理的信件（栈），每次取出最上面的一封，先阅读（加入答案），再把这封信里提到的需要进一步处理的信件（子节点）放回叠子里——为了保持原来的阅读顺序，需要把这些信件倒着放回去。

#### 代码（Python）

```python
# Definition for a Node, 同上
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children or []

def preorder_iterative(root: Node) -> list[int]:
    """
    迭代（显式栈）实现 N 叉树的先序遍历
    """
    if not root:                     # 空树直接返回空列表
        return []

    stack = [root]                   # 栈初始化，只放根节点
    res = []                         # 用来存放遍历结果

    while stack:                     # 栈不为空就一直循环
        node = stack.pop()           # ① 弹出栈顶节点
        res.append(node.val)         # ② 先序：先记录根节点的值

        # ③ 将子节点逆序压入栈中
        #   逆序是为了保证左侧子节点先被弹出
        for child in reversed(node.children):
            stack.append(child)      # 子节点入栈，等待后续处理

    return res
```

#### 复杂度

- **时间复杂度：** `O(N)`  
  每个节点同样只会被弹出一次、压入一次，做的操作仍是常数级别，整体随节点数线性增长。相较于递归，时间上没有额外开销。

- **空间复杂度：** `O(N)`（最坏情况的栈） + `O(N)`（答案列表）  
  - 栈的最大容量取决于树的结构。最坏情况下（比如根只有一个子节点，形成一条长链），栈会同时保存 `N` 个节点。  
  - 若只计额外空间（不计答案），则是 `O(N)`，这也是先序遍历在迭代实现中不可避免的开销。

与递归版相比，**空间的主要区别在于**递归使用系统调用栈，而迭代使用我们自己显式的 Python 列表作为栈；两者在最坏情况下的大小是相同的，只是控制权不同。

---

## 心得

- **核心技巧**：用栈模拟递归的深度优先遍历（先序），关键在于逆序压入子节点保证左到右的顺序。
- **适用的题型**  
  1. 任意树结构的 **前序 / 中序 / 后序** 深度优先遍历（如二叉树、N 叉树）。  
  2. **图的深度优先搜索**（DFS）需要显式栈来避免递归。  
  3. **树的层序遍历**（广度优先）则对应使用 **队列**（FIFO）实现。
- **一句话总结解题钥匙**：**“栈 + 逆序入栈 = 递归的手动版”。**

---

## 反思

- **第一反应**：立刻想到递归写法，因为先序遍历的定义天然递归。  
- **最容易踩的坑**  
  - **空树**：`root` 为 `None` 时必须直接返回空列表，防止后续访问属性报错。  
  - **子节点顺序**：忘记逆序压栈会导致遍历顺序颠倒（右子树先遍历），答案不符合题目要求。  
  - **栈的大小**：在极端深度的树上，递归可能触发 Python 的递归深度限制（默认 1000），需要提前 `sys.setrecursionlimit` 或改用迭代。  
- **下次类似题的第一步**：先判断是否可以用递归快速写出正确答案，然后思考 “递归用了什么隐式数据结构（栈/队列）”，再把它显式化得到迭代解。这样既保证正确性，又能满足面试官对**空间/控制**的进一步要求。