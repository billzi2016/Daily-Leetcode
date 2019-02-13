# #297. 序列化与反序列化二叉树 / Serialize and Deserialize Binary Tree

> 难度：困难 · 标签：String、Tree、Depth-First Search、Breadth-First Search、Design、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

---

## 题目（英文原版）

**Description**

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.
Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
```

**Example 2:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

序列化（serialization）是将数据结构或对象转换为比特序列的过程，以便可以将其存储在文件或内存缓冲区中，或通过网络连接传输，随后在相同或不同的计算机环境中重新构建。

设计一种算法来 **序列化**（serialize）和 **反序列化**（deserialize）二叉树。对你的序列化/反序列化算法没有特定限制，只需确保能够把二叉树序列化为字符串，并且该字符串能够反序列化回原始的树结构。

**说明**：LeetCode 使用的输入/输出格式与二叉树的序列化方式相同。你并不一定必须遵循该格式，欢迎自行设计其他实现思路。

### 示例

#### 示例 1
```
Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
```

#### 示例 2
```
Input: root = []
Output: []
```

### 约束条件
- 树中节点的数量范围为 **[0, 10⁴]**。
- 每个节点的取值满足 **-1000 ≤ Node.val ≤ 1000**。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把树的遍历顺序直接写成字符串**，以后再把这个字符串按照相同的顺序读回来。  
这里我们采用「前序遍历」`根 → 左 → 右`，因为它天然符合「先写根，再写左子树，最后写右子树」的顺序。  

- **数据结构**  
  - **栈（递归调用栈）**：递归本质上就是用系统栈保存「当前要处理的节点」和「返回后要继续的工作」。  
  - **字符串**：把遍历得到的节点值和特殊标记（如 `#`）拼接起来，用逗号 `,` 作为分隔符。  
  - **哈希表**：这里不需要哈希表，但如果你把「节点值」看成「字典的键」，`#` 就像「找不到的页码」——告诉我们这里没有节点。

- **为什么正确**  
  前序遍历的顺序唯一决定了一棵二叉树的结构，只要在遍历时把「空位置」也记下来（这里用 `#` 表示），反序列化时就能严格按照「根 → 左 → 右」的顺序把节点一个一个恢复出来，空位自然会保持为空。

- **时间/空间复杂度**  
  - **时间**：我们要访问每个节点一次，记下来一次，读回来一次 → `O(n)`（`n` 是节点数）。  
  - **空间**：递归需要 `O(h)` 的调用栈，`h` 是树的高度，最坏情况下 `h = n`（链状树），所以最坏空间是 `O(n)`；另外生成的字符串长度也是 `O(n)`（每个节点产生一个字符和一个分隔符）。

> 大白话解释：  
> - `O(n)` 就是「和节点个数成正比」——节点多，时间/空间就多。  
> - `O(h)` 就是「和树的层数成正比」——树高多少，递归层数就多少。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """把二叉树序列化为字符串，再反序列化回原来的树"""

    # ------------------- 序列化 -------------------
    def serialize(self, root: TreeNode) -> str:
        """前序遍历 + '#' 记录空节点，使用逗号分隔"""
        vals = []  # 用来收集遍历过程中的每个字符

        def preorder(node: TreeNode):
            if not node:
                vals.append('#')          # 空节点用 '#' 标记
                return
            vals.append(str(node.val))   # 记录当前节点值
            preorder(node.left)          # 递归左子树
            preorder(node.right)         # 递归右子树

        preorder(root)
        return ','.join(vals)            # 把列表变成一个长字符串

    # ------------------- 反序列化 -------------------
    def deserialize(self, data: str) -> TreeNode:
        """把字符串按逗号切割后，用前序顺序重新构造二叉树"""
        if not data:                     # 空字符串对应空树
            return None

        vals = iter(data.split(','))     # 生成一个迭代器，逐个取值

        def build() -> TreeNode:
            val = next(vals)             # 取出下一个字符
            if val == '#':               # 空节点
                return None
            node = TreeNode(int(val))    # 创建节点
            node.left = build()          # 递归构造左子树
            node.right = build()         # 递归构造右子树
            return node

        return build()
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们对每个节点做了常数次操作（写入/读取），所以整体随节点数线性增长。

- **空间复杂度**：`O(n)`  
  - 递归栈最坏 `O(n)`（链状树）  
  - 生成的序列字符串本身也需要 `O(n)` 的空间来存放每个节点的值和 `#`。

---

### 2. 最优解

#### 思路  

虽然前序递归已经是 `O(n)`，但它在 **深度很大的树**（比如链表形）时会导致 **递归层数等于节点数**，这会触发 Python 的递归深度限制（默认约 1000），从而抛出 `RecursionError`。  
为了让代码在所有合法输入（最多 10⁴ 个节点）下都安全，我们改用 **层序遍历（广度优先搜索，BFS）** 来序列化，同时在反序列化时也使用队列按层恢复节点。这样：

1. **不依赖递归** → 不会受到系统栈深度的限制。  
2. **一次遍历即可** → 仍然是 `O(n)`。  

核心数据结构：

- **队列（Queue）**：BFS 必须用「先入先出」的队列来保证「先处理当前层的节点，再处理下一层」的顺序。可以用 `collections.deque` 实现。  
- **字符串 + 分隔符**：同样用 `,` 分隔每个值，`#` 表示空位。  

**层序序列化**的过程：

1. 把根节点放进队列。  
2. 每次弹出队首节点 `node`：  
   - 若 `node` 为 `None`，在结果里写 `#`。  
   - 否则写 `node.val`，并把 `node.left`、`node.right`（即使是 `None`）依次加入队列。  
3. 当队列全部为空时，遍历结束。  

**层序反序列化**的过程：

1. 把序列化得到的字符串切成列表 `vals`。  
2. 第一个元素必然是根节点的值（若是 `#` 则整棵树为空）。创建根节点并把它放进队列。  
3. 维护一个指针 `i` 指向 `vals` 中下一个未处理的元素。每次从队列弹出一个父节点 `parent`，依次取 `vals[i]`、`vals[i+1]` 来决定 `parent` 的左、右子节点（若是 `#` 则保持 `None`），并把非空子节点加入队列。指针向后移动两位。  
4. 当指针走完所有元素时，树已完整重建。

> 类比：  
> 想象你在组织一次学校的点名，老师先叫“一年级”，再叫“一年级的左边同学”，再叫“一年级的右边同学”。如果一次点完所有人（层序），就不会出现老师一次叫到“第 1000 层”而导致声音嘶哑（递归栈溢出）。

#### 代码（Python）

```python
from collections import deque

# 同样的二叉树节点定义
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """使用层序遍历（BFS）实现序列化/反序列化，避免递归深度限制"""

    # ------------------- 序列化 -------------------
    def serialize(self, root: TreeNode) -> str:
        if not root:
            return ''                     # 空树返回空字符串

        q = deque([root])                # 队列初始化，只装根节点
        parts = []                       # 用来存放序列化后的每个字符

        while q:
            node = q.popleft()           # 取出当前层的第一个节点
            if node:
                parts.append(str(node.val))   # 记录节点值
                q.append(node.left)            # 左子节点（可能是 None）
                q.append(node.right)           # 右子节点（可能是 None）
            else:
                parts.append('#')               # 空位用 '#' 标记

        # 为了去掉末尾多余的 '#', 可以在这里做一次裁剪（可选）
        # while parts and parts[-1] == '#':
        #     parts.pop()
        return ','.join(parts)

    # ------------------- 反序列化 -------------------
    def deserialize(self, data: str) -> TreeNode:
        if not data:
            return None                    # 空字符串对应空树

        vals = data.split(',')             # 把字符串拆成列表
        root_val = vals[0]
        if root_val == '#':
            return None

        root = TreeNode(int(root_val))
        q = deque([root])                  # 队列保存待处理的父节点
        i = 1                              # 指向下一个未处理的值

        while q and i < len(vals):
            parent = q.popleft()

            # 处理左子节点
            left_val = vals[i]
            i += 1
            if left_val != '#':
                left_node = TreeNode(int(left_val))
                parent.left = left_node
                q.append(left_node)       # 非空左子节点加入队列

            # 处理右子节点（可能已经遍历完）
            if i < len(vals):
                right_val = vals[i]
                i += 1
                if right_val != '#':
                    right_node = TreeNode(int(right_val))
                    parent.right = right_node
                    q.append(right_node)  # 非空右子节点加入队列

        return root
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：每个节点只会被 **入队一次、出队一次**，并且只写入或读取一次字符，整体仍然随节点数线性增长。

- **空间复杂度**：`O(n)`  
  - 队列在最坏情况下会同时保存一整层的节点，最多 `O(width)`，而二叉树的最大宽度不超过 `n`，所以是 `O(n)`。  
  - 序列化产生的字符串同样需要 `O(n)` 空间。

> 与暴力解的对比：时间相同，但**不依赖递归**，在深度极大的树上更安全、更稳健。

---

## 心得

- **核心技巧**：**使用遍历顺序（前序或层序）记录空位**，并利用 **队列**（BFS）或 **递归栈**（DFS）实现完整的序列化/反序列化。  
- **适用的题型**  
  1. 任意二叉树的序列化/反序列化（本题）。  
  2. 「把树压平为数组」或「从数组恢复树」的题目（如 LeetCode 108、110）。  
  3. 「树的层序遍历」相关的题目（如 `Binary Tree Level Order Traversal`）。  
- **一句话总结**：**“把树的结构用‘值 + 空位’完整记录下来，再按相同顺序恢复”** 是解这类题的钥匙。

---

## 反思

- **第一反应**：想到「把树遍历成列表」——于是用了前序递归并加 `#` 标记。  
- **最容易踩的坑**  
  - **递归深度**：链状树会导致 `RecursionError`。  
  - **字符串分隔**：忘记加分隔符会导致 `12` 与 `1,2` 混淆。  
  - **末尾多余的空位**：序列化后可能会有很多连续的 `#`，反序列化时要保证读取顺序一致。  
- **下次遇到同类题**：第一步先判断「树的高度是否可能很大」——如果有风险，就直接选用 **层序+BFS**（非递归）方案；否则可以快速写出 **前序递归** 的简洁实现。