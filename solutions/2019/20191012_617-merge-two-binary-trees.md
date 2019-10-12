# #617. 合并二叉树 / Merge Two Binary Trees

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/merge-two-binary-trees/)

---

## 题目（英文原版）

**Description**

You are given two binary trees root1 and root2.
Imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not. You need to merge the two trees into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of the new tree.
Return the merged tree.
Note: The merging process must start from the root nodes of both trees.

**Examples**

**Example 1:**

```
Input: root1 = [1,3,2,5], root2 = [2,1,3,null,4,null,7]
Output: [3,4,5,5,4,null,7]
```

**Example 2:**

```
Input: root1 = [1], root2 = [1,2]
Output: [2,2]
```

**Constraints**

- The number of nodes in both trees is in the range [0, 2000].
- -104 <= Node.val <= 104

---

## 题目（中文翻译）

**描述**  
给定两棵二叉树 `root1` 和 `root2`。  
想象把其中一棵树覆盖在另一棵树上时，部分节点会重叠，另一些则不重叠。你需要将这两棵树合并为一棵新的二叉树。合并规则如下：

- 如果两个节点（node）重叠，则将它们的值相加，作为合并后节点的新值。  
- 否则，非空的节点将直接作为新树中的节点。

返回合并后的二叉树。  
**注意**：合并过程必须从两棵树的根节点（root）开始。

**示例**

示例 1:  
输入: `root1 = [1,3,2,5]`, `root2 = [2,1,3,null,4,null,7]`  
输出: `[3,4,5,5,4,null,7]`

示例 2:  
输入: `root1 = [1]`, `root2 = [1,2]`  
输出: `[2,2]`

**约束条件**  

- 两棵树的节点数量范围为 `[0, 2000]`。  
- `-10^4 <= Node.val <= 10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两棵树同时从根节点往下遍历**，遇到同位置的两个节点就把它们的值相加，生成新的节点；如果某个位置只有一棵树有节点（另一棵是 `null`），直接把非空的那个节点挂到新树上。

> 类比：把两本树形目录（像《百科全书》）摞在一起，左手指着第一本的章节，右手指着第二本的章节。如果两本同一层都有章节，就把章节标题合并（这里是数值相加）；如果只有一本有章节，就把这本的章节直接搬到新目录里。

实现时可以用 **深度优先搜索（DFS）** 递归：

1. **递归入口**：`merge(root1, root2)`  
2. **终止条件**：如果 `root1` 为 `None` → 返回 `root2`（因为没有冲突，直接使用 `root2` 的子树）。同理，如果 `root2` 为 `None` → 返回 `root1`。  
3. **合并当前节点**：`root1.val += root2.val`（把两棵树的值加到 `root1` 上，直接在原节点上改写，省去额外的创建工作）。  
4. **递归合并左子树**：`root1.left = merge(root1.left, root2.left)`  
5. **递归合并右子树**：`root1.right = merge(root1.right, root2.right)`  
6. **返回** 合并后的 `root1`（它已经是新树的根节点）。

为什么正确？  
- 递归保证了每一层、每一个对应位置的节点都会被访问一次。  
- 只要有任意一棵树在该位置提供了节点，就会在新树中出现该节点；若两棵都有，则按照题意把值相加。  
- 递归的返回值把子树拼回去，完整构造了整棵新树。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


def mergeTrees(root1: TreeNode, root2: TreeNode) -> TreeNode:
    """
    递归合并两棵二叉树，返回合并后的根节点
    """
    # 如果其中一棵树已经为空，直接返回另一棵（相当于把非空子树“搬过去”）
    if not root1:
        return root2
    if not root2:
        return root1

    # 两棵树都有节点 → 把值相加，保存在 root1 上（就地修改）
    root1.val += root2.val

    # 递归合并左子树，结果接回 root1 的左指针
    root1.left = mergeTrees(root1.left, root2.left)

    # 递归合并右子树，结果接回 root1 的右指针
    root1.right = mergeTrees(root1.right, root2.right)

    # 返回已经合并好的根节点
    return root1
```

#### 复杂度

- **时间复杂度：O(N)**  
  `N` 为两棵树中**非空节点的总数**。每个节点最多被访问一次（一次递归调用），所以耗时与节点数线性相关。可以把 `O(N)` 想象成“走遍所有房间一次”，房间越多，花的时间越多，正比增长。

- **空间复杂度：O(H)**  
  递归调用会占用栈空间，深度 `H` 为**两棵树的最大深度**（取较大的那棵）。最坏情况下树是链表形状，`H≈N`，此时空间复杂度退化为 `O(N)`；在平衡树中，`H≈log N`，空间则是 `O(log N)`。这里的空间是“递归层数”，不是额外存储节点。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈其实不在时间**——我们已经只遍历了一遍所有节点，达到了 `O(N)` 的下界（必须看每个节点一次才能决定它在新树里的样子）。唯一可以改进的，是**空间使用**：

- 递归方式需要栈空间 `O(H)`。如果对空间要求更严格（比如极深的树可能导致栈溢出），可以改用 **迭代的广度优先搜索（BFS）** 或 **显式栈的深度优先搜索**，把递归改写为循环，使用 `queue`/`stack` 手动管理节点。这样仍然是 `O(N)` 时间，但栈/队列最多也只会保存同一层的节点数，最坏情况下仍是 `O(H)`，但避免了系统递归深度限制。

下面给出 **迭代 BFS** 的实现思路（对初学者友好，直观“层层遍历”）：

1. **准备工作**：如果 `root1` 为 `None` → 直接返回 `root2`；反之同理。否则把 `root1`（作为合并结果的根）放进队列，`root2` 也放进另一队列。  
2. **循环遍历**：只要两个队列都不为空，弹出一对对应节点 `n1, n2`。  
   - 把 `n2.val` 加到 `n1.val`（同样在原节点上就地修改）。  
   - **左子树**：  
     - 若 `n1.left` 为 `None` 且 `n2.left` 不为 `None` → 把 `n2.left` 直接接到 `n1.left`（相当于“搬过去”）。  
     - 若两者都不为 `None` → 把这对左子节点再次压入队列，等待后续合并。  
   - **右子树**：同左子树的处理方式。  
3. 循环结束后，`root1` 已经变成了完整的合并树，直接返回即可。

核心数据结构是 **队列**（可以用 `collections.deque`），它的作用类似于“排队的游客”，先进入的先处理，正好对应层序遍历的顺序。

#### 代码（Python）

```python
from collections import deque

# 仍然使用前面定义的 TreeNode 类

def mergeTrees(root1: TreeNode, root2: TreeNode) -> TreeNode:
    """
    迭代版（BFS）合并两棵二叉树，避免递归深度限制
    """
    # 任何一棵树为空时，直接返回另一棵
    if not root1:
        return root2
    if not root2:
        return root1

    # 两棵树都非空，使用队列保存对应节点
    q1 = deque([root1])   # 合并后树的节点（最终返回的根在这里）
    q2 = deque([root2])   # 第二棵树的节点

    while q1 and q2:
        n1 = q1.popleft()   # 取出对应的两个节点
        n2 = q2.popleft()

        # 合并当前节点的值
        n1.val += n2.val

        # ---------- 处理左子树 ----------
        if n1.left and n2.left:               # 两棵都有左子节点 → 继续合并
            q1.append(n1.left)
            q2.append(n2.left)
        elif not n1.left and n2.left:         # 只有第二棵有左子节点 → 直接搬过去
            n1.left = n2.left

        # ---------- 处理右子树 ----------
        if n1.right and n2.right:
            q1.append(n1.right)
            q2.append(n2.right)
        elif not n1.right and n2.right:
            n1.right = n2.right

    # 循环结束后，root1 已经是合并好的树
    return root1
```

#### 复杂度

- **时间复杂度：O(N)**  
  与递归版相同，每个非空节点最多被访问一次。遍历顺序改成层序，但“看多少节点”仍然是 `N`，所以时间不变。

- **空间复杂度：O(H)**  
  队列中最多同时存放同一层的节点数，最坏情况下是树的最大宽度。对于完全二叉树，宽度约为 `2^{H-1}`，但这仍然是 `O(N)` 的上界。相较于递归的调用栈，显式队列可以避免系统递归深度限制，更安全。

---

## 心得

- **核心技巧**：**同步遍历两棵树**（递归或迭代），并在遍历过程中“原地”修改其中一棵树，使之成为合并结果。  
- **适用场景**：  
  1. 合并两棵相同结构的树（如 LeetCode 617 “Merge Two Binary Trees”）。  
  2. 同步遍历两棵树进行比较或映射（如判断两树是否相同、交叉合并等）。  
  3. 对两棵树做“按位”操作的题目（如两树对应节点求最大、最小等）。  
- **一句话总结**：**把两棵树的对应节点配对，一边遍历一边直接把值累加或搬迁，就是合并的钥匙。**

---

## 反思

- **第一反应**：看到“合并根节点、左子树、右子树”，立刻想到递归——把问题拆成子问题，和“求树的深度”“遍历树”等经典递归模式一样。  
- **最容易踩的坑**：  
  - **忘记处理空节点**：如果直接 `root1.val += root2.val` 而不检查 `None`，会出现属性错误。  
  - **返回值错误**：递归版必须返回合并后的根节点，否则上层无法拼接子树。  
  - **修改原树**：题目允许原地修改任意一棵树，但若在面试中要求“返回全新树”，就需要额外 `new TreeNode`，代码会稍微复杂。  
- **下次遇到同类题**：**先画出两棵树的对应位置，确认“同步遍历”是否能一次完成**。如果能，就直接用递归/迭代实现；如果有额外限制（比如不能修改原树），再考虑额外创建节点的方案。