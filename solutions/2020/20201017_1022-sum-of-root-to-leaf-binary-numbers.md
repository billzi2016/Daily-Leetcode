# #1022. **根到叶子路径的二进制数之和** / Sum of Root To Leaf Binary Numbers

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/sum-of-root-to-leaf-binary-numbers/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree where each node has a value 0 or 1. Each root-to-leaf path represents a binary number starting with the most significant bit.
For all leaves in the tree, consider the numbers represented by the path from the root to that leaf. Return the sum of these numbers.
The test cases are generated so that the answer fits in a 32-bits integer.

**Examples**

**Example 1:**

```
Input: root = [1,0,1,0,1,0,1]
Output: 22
Explanation: (100) + (101) + (110) + (111) = 4 + 5 + 6 + 7 = 22
```

**Example 2:**

```
Input: root = [0]
Output: 0
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- Node.val is 0 or 1.

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，树中每个节点的值只能是 `0` 或 `1`。从根到叶子节点的每条路径都可以视为一个二进制数，路径的起点（根节点）对应最高位（most significant bit）。

对于树中的所有叶子节点，计算从根到该叶子所对应的二进制数的和，并返回该和。题目保证所有答案均能装入 32 位整数（32-bits integer）。

**示例 1**

```text
Input: root = [1,0,1,0,1,0,1]
Output: 22
Explanation: (100)₂ + (101)₂ + (110)₂ + (111)₂ = 4 + 5 + 6 + 7 = 22
```

**示例 2**

```text
Input: root = [0]
Output: 0
```

**约束条件**

- 树中节点的数量在 `[1, 1000]` 区间内。
- `Node.val` 只能是 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有根到叶子的路径都枚举出来**，每条路径得到一串 `0/1`，再把这串二进制数转换成十进制，最后把所有结果相加。

- **数据结构**：  
  - 树本身已经是二叉树，用 `TreeNode` 表示。  
  - 为了保存路径，我们可以用一个 `list`（类似装东西的背包），把遍历时经过的节点值依次放进去。  
  - 把二进制转十进制时，可以把路径当成**字符串**，再用 Python 的 `int(binary_str, 2)` 转换，或者手动遍历每位累加。  

- **为什么正确**：  
  每一次递归从根往下走，直到到达叶子节点（左右子树都是 `None`），此时 `list` 中恰好保存了从根到该叶子的全部 `0/1`。把它们看成二进制数就正好是题目要求的数值。把所有叶子的数值相加即得到答案。

- **复杂度分析（大白话）**：  
  - 假设树有 `N` 个节点，叶子节点有 `L`（`L ≤ N`）。  
  - 我们会**遍历每条根到叶的路径**一次。每条路径的长度最多是树的高度 `h`（最坏情况下 `h = N`，即链状树），所以把路径转成整数的代价是 `O(h)`。  
  - 总体时间就是所有路径长度之和，也就是 `O(N)`（因为每个节点只会被访问一次，放进/弹出 `list`），再加上转二进制的 `O(h)`，整体仍是 `O(N)`。  
  - 空间上，递归栈的深度最坏是 `h`，另外保存路径的 `list` 也最多 `h`，所以 **空间复杂度是 O(h)**，在最坏情况下是 `O(N)`。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的二进制位，0 或 1
        self.left = left
        self.right = right

def sumRootToLeaf(root: TreeNode) -> int:
    """
    暴力版：把每条根到叶的路径保存为列表，再转成十进制累加
    """
    total = 0                     # 最终答案
    path = []                     # 当前递归路径上的二进制位

    def dfs(node: TreeNode):
        nonlocal total
        if not node:               # 空节点直接返回
            return

        # 进入当前节点，记录它的值
        path.append(str(node.val))   # 把整数转成字符，方便后面拼接成二进制字符串

        # 判断是否是叶子节点
        if not node.left and not node.right:
            # 把路径 ['1','0','1'] 合并成 "101"，再转成十进制 5
            binary_str = ''.join(path)
            total += int(binary_str, 2)   # Python 自带的二进制转十进制
        else:
            # 继续向左、右子树搜索
            dfs(node.left)
            dfs(node.right)

        # 回溯：离开当前节点时把它弹出，恢复到父节点的状态
        path.pop()

    dfs(root)
    return total
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  每个节点恰好访问一次，构造二进制字符串和转十进制的工作量与路径长度成正比，累计下来仍是线性 `N`。

- **空间复杂度**：`O(h)`（最坏 `O(N)`）  
  递归栈和 `path` 列表的最大深度等于树的高度 `h`。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性时间**，已经很快了。但我们可以在**遍历的过程中直接把二进制数累加**，省掉把路径保存成列表、再转字符串的中间步骤。核心技巧是**在向下递归时把当前的二进制数左移一位并加上当前节点的值**，这正好对应二进制的位运算：

```
当前路径对应的十进制数 = (父路径对应的十进制数 << 1) | node.val
```

- **慢在哪里**：  
  暴力解把路径保存成列表、每到叶子时才一次性转成整数，额外的字符串拼接和 `int(..., 2)` 会产生一定的常数时间开销。虽然整体仍是 `O(N)`，但可以把这部分“隐藏”在递归的每一步里，做到**一次遍历一次计算**。

- **一步步推导**：  
  1. 从根开始，根节点的二进制数就是它本身（0 或 1）。  
  2. 当我们从父节点往子节点走时，等价于在二进制左边再加一位：`父数 * 2 + 子节点的值`（左移一位相当于乘以 2）。  
  3. 当到达叶子时，这个累计的数就是该根到叶路径对应的十进制值，直接加入答案即可。

- **核心算法/数据结构**：  
  - **深度优先搜索（DFS）**：递归实现，顺着一条路径一直走到叶子，再回溯。  
  - **位运算**：左移 (`<<`) 或乘以 2，快速完成二进制到十进制的转换。  
  - **递归栈**：隐式保存了当前路径对应的整数，不需要额外的列表。

- **类比**：想象你在走楼梯，每走一步都把已有的步数乘以 2（相当于把之前的步数左移），再加上当前台阶的“标记”（0/1），这样到达终点时手里正好拿着这条楼梯的编号。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def sumRootToLeaf(root: TreeNode) -> int:
    """
    最优解：在 DFS 过程中实时累计二进制数，省掉路径保存与转换
    """
    total = 0                     # 最终答案

    def dfs(node: TreeNode, cur_val: int):
        """
        node: 当前访问的节点
        cur_val: 从根到父节点已经累计的十进制数
        """
        nonlocal total
        if not node:
            return

        # 把当前节点的位加入到已有的数里：左移一位后加上 node.val
        cur_val = (cur_val << 1) | node.val   # 等价于 cur_val * 2 + node.val

        # 若是叶子，直接把 cur_val 累加到答案
        if not node.left and not node.right:
            total += cur_val
            return

        # 继续向左、右子树递归
        dfs(node.left, cur_val)
        dfs(node.right, cur_val)

    dfs(root, 0)   # 从根开始，累计值初始为 0
    return total
```

#### 复杂度

- **时间复杂度**：`O(N)` — 仍然是遍历每个节点一次，只是把“转二进制”这一步搬到了递归的每一步，常数因子更小。

- **空间复杂度**：`O(h)`（最坏 `O(N)`） — 递归栈的深度等于树的高度，额外的存储只有 `cur_val`（整数），占用常数空间。

---

## 心得

- **核心技巧**：在 DFS（或 BFS）遍历时**同步维护路径对应的数值**，利用左移/加法完成二进制转十进制的累计。  
- **适用的题型**：  
  1. “根到叶子路径求和”类题（如 LeetCode 1022 Sum of Root To Leaf Binary Numbers）。  
  2. “路径上的数值运算”类题（如 LeetCode 129 Sum Root to Leaf Numbers，只是十进制而非二进制）。  
  3. “在树/图上累计状态”类题（比如求路径最大和、路径乘积等）。  
- **一句话总结解题钥匙**：**边走边算**——把“把路径记下来再算”改成“走一步就算一步”，既省时又省空间。

---

## 反思

- **第一反应**：直接想把所有根到叶的路径收集起来，再统一转二进制求和。  
- **最容易踩的坑**：  
  - 忘记判断 **叶子节点**（左右子树都是 `None`）而在中间节点就累加。  
  - 使用字符串拼接或 `int(...,2)` 时，可能因为路径很长导致额外的时间开销。  
  - 递归时没有正确回溯（比如忘了 `pop()`），会导致路径残留错误。  
- **下次遇到同类题**：第一步先思考**能否在遍历的过程中实时更新答案**，把“路径收集+后处理”合并为“一遍遍历”。这样往往能直接得到最优解。