# #590. N叉树后序遍历 / N-ary Tree Postorder Traversal

> 难度：简单 · 标签：Stack、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/n-ary-tree-postorder-traversal/)

---

## 题目（英文原版）

**Description**

Given the root of an n-ary tree, return the postorder traversal of its nodes' values.
Nary-Tree input serialization is represented in their level order traversal. Each group of children is separated by the null value (See examples)
Follow up: Recursive solution is trivial, could you do it iteratively?

**Examples**

**Example 1:**

```
Input: root = [1,null,3,2,4,null,5,6]
Output: [5,6,3,2,4,1]
```

**Example 2:**

```
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: [2,6,14,11,7,3,12,8,4,13,9,10,5,1]
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- 0 <= Node.val <= 104
- The height of the n-ary tree is less than or equal to 1000.

---

## 题目（中文翻译）

给定一棵 n叉树 (n-ary tree) 的根节点 (root)，返回其节点值的后序遍历 (postorder traversal)。  
n叉树的输入序列化采用层序遍历 (level order traversal) 的方式表示。每一组子节点之间使用 `null` 值 (null value) 进行分隔（参见示例）。

**示例 1**  

**示例 2**  

**进阶**：递归解法很直接，你能实现一个迭代解法吗？

---

### 示例

**示例 1**  
```
Input: root = [1,null,3,2,4,null,5,6]
Output: [5,6,3,2,4,1]
```

**示例 2**  
```
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: [2,6,14,11,7,3,12,8,4,13,9,10,5,1]
```

---

### 约束条件

- 树中节点的数量在 `[0, 10^4]` 区间内。
- `0 <= Node.val <= 10^4`
- n叉树的高度不超过 `1000`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法是 **递归**：  
后序遍历的顺序是「先遍历所有子节点，再访问根节点」。  
我们可以把「遍历所有子节点」这件事交给递归函数自己去完成，等子树全部走完后，再把当前节点的值加入答案列表。

> **类比**：递归就像你把一件事交给“小朋友”去做，等小朋友把手头的事全部完成后，才轮到你自己去做。  
> - `Node.children` 就像每个节点的「孩子们」的名单，遍历它们相当于把任务交给每个孩子。  
> - `result.append(node.val)` 就是「我自己」最后才出场。

只要树不为空，递归一定会遍历到每一个节点，因此答案必然正确。

#### 代码（Python）

```python
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        # children 如果为 None，就当成空列表处理，避免后面遍历时报错
        self.children = children if children is not None else []


def postorder(root: 'Node') -> list[int]:
    """
    递归实现 N 叉树的后序遍历
    """
    if root is None:                     # 空树直接返回空列表
        return []

    ans = []                              # 用来收集遍历顺序

    def dfs(node: 'Node'):
        # 先遍历所有子节点
        for child in node.children:       # 遍历 children 列表
            dfs(child)                    # 递归进入子树
        # 再把当前节点的值加入答案
        ans.append(node.val)              # 访问根节点

    dfs(root)                             # 从根节点开始递归
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  这里的 `N` 是树中节点的数量。每个节点恰好被访问一次（进入一次递归），所以总耗时与节点数成正比。可以把 `O(N)` 想象成「走遍所有房间一次」的时间。

- **空间复杂度**：`O(H)`  
  递归调用会占用调用栈，最深的递归层数等于树的高度 `H`。在最坏情况下（比如一条链），`H = N`，所以最坏时空间是 `O(N)`；在平衡树里 `H` 远小于 `N`。可以把它看成「爬楼梯时背的背包容量」。

---

### 2. 最优解

#### 思路  

递归实现虽然代码简洁，但使用了系统调用栈，**在极端深度（>1000）时可能导致栈溢出**。  
LeetCode 的「Follow up」要求我们 **用迭代方式** 完成同样的遍历。迭代的核心是 **显式栈**（自己维护的 `list`），把递归过程手动搬到循环里。

**后序遍历的顺序**是「子 → 根」，而普通的 **前序遍历**（根 → 子）用栈实现很自然。  
如果我们把「根 → 子」的前序遍历得到的序列 **倒序**，恰好就是「子 → 根」的后序遍历。  
因此思路如下：

1. 用一个栈 `stack`，先把根节点压进去。  
2. 每次弹出栈顶 `node`，把 `node.val` 加到结果列表 `res`（这一步相当于「先根后子」）。  
3. 再把 `node` 的所有子节点 **全部压入栈**（顺序随意，因为最后会整体倒序）。  
4. 循环结束后，`res` 中的顺序是「根 → 子」，只需要 `res.reverse()` 就得到真正的后序遍历。

> **类比**：想象你把所有礼物（节点）先按「先大后小」的顺序放进箱子（栈），箱子弹出时是「后进先出」，于是你得到的顺序是「大→小」。如果你把这个顺序再翻个面（倒序），就得到「小→大」——这正是我们想要的后序。

#### 代码（Python）

```python
# Definition for a Node, 同上
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []


def postorder_iterative(root: 'Node') -> list[int]:
    """
    迭代实现 N 叉树的后序遍历
    思路：先做「根→子」的前序遍历，最后整体逆序得到后序。
    """
    if root is None:               # 空树直接返回空列表
        return []

    stack = [root]                 # 用列表模拟栈，先把根压进去
    res = []                       # 用来收集「根→子」的遍历顺序

    while stack:
        node = stack.pop()         # 弹出栈顶节点（后进先出）
        res.append(node.val)       # 先记录根节点的值
        # 把所有子节点压入栈中
        # 这里不需要特意倒序，因为最终会整体逆序
        for child in node.children:
            stack.append(child)    # 子节点会在后面被弹出，形成「根→子」顺序

    # 把「根→子」的序列整体倒过来，得到「子→根」的后序遍历
    res.reverse()
    return res
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  每个节点恰好被压入栈一次、弹出一次、加入结果一次，操作次数与节点数线性相关。与递归版一样，只是把递归的「函数调用」换成了「显式栈」的 push/pop。

- **空间复杂度**：`O(N)`（最坏情况）  
  栈里最多同时存放树的某一层的所有节点。最坏情况下（比如根节点只有一个子链），栈的深度会达到 `N`，因此空间是 `O(N)`。这比递归版的 `O(H)` 更保守，因为我们在遍历时会把所有未访问的子节点都留在栈里。

---

## 心得

- **核心技巧**：利用「先根后子」的前序遍历 + 整体逆序，巧妙实现后序遍历的迭代版。  
- **适用场景**：  
  1. 任意树结构的后序遍历（如二叉树、N 叉树）。  
  2. 需要在遍历过程中**先处理子节点再处理父节点**的题目（如文件系统的删除操作）。  
  3. 需要避免递归深度导致栈溢出的场景。  
- **一句话总结**：把后序看成「前序的倒序」，用栈模拟前序遍历，再整体翻转即可。

---

## 反思

- **第一反应**：立刻写递归，因为递归天然符合「先子后父」的思路。  
- **最容易踩的坑**：  
  - 忘记对空树 (`root is None`) 做特判，直接访问会报错。  
  - 在迭代版里，若把子节点压栈的顺序写成「逆序」再倒序，容易产生「顺序错误」的结果。  
  - 递归深度超过 Python 默认递归限制（约 1000）时会抛 `RecursionError`，需要改为迭代。  
- **下次第一步**：先判断「是否可以用递归」以及「递归深度是否安全」。如果深度可能很大，立刻考虑用显式栈实现遍历，再根据遍历顺序决定是否需要逆序。