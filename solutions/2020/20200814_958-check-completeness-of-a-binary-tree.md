# #958. 检查二叉树的完全性 / Check Completeness of a Binary Tree

> 难度：中等 · 标签：Tree、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/check-completeness-of-a-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, determine if it is a complete binary tree.
In a complete binary tree, every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5,6]
Output: true
Explanation: Every level before the last is full (ie. levels with node-values {1} and {2, 3}), and all nodes in the last level ({4, 5, 6}) are as far left as possible.
```

**Example 2:**

```
Input: root = [1,2,3,4,5,null,7]
Output: false
Explanation: The node with value 7 isn't as far left as possible.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 100].
- 1 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，判断它是否为**完全二叉树**（complete binary tree）。  
在完全二叉树中，除可能的最后一层外，每一层都必须被完全填满，且最后一层的所有节点必须尽可能靠左排列。最后一层（层号记为 `h`）的节点数可以在 `1` 到 `2^h`（含）之间。

**示例 1**  

**示例 2**  

**约束条件**  

- 树中节点的数量在 `[1, 100]` 范围内。  
- `1 <= Node.val <= 1000`

---

### 示例

#### 示例 1
**输入**: `root = [1,2,3,4,5,6]`  
**输出**: `true`  
**解释**: 除最后一层外，前面的每一层都是满的（即层 `{1}` 和层 `{2, 3}`），且最后一层的所有节点（`{4, 5, 6}`）都尽可能向左。

#### 示例 2
**输入**: `root = [1,2,3,4,5,null,7]`  
**输出**: `false`  
**解释**: 值为 `7` 的节点没有尽可能向左。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把树“展开”成一行，按照 **层序遍历**（Breadth‑First Search，简称 BFS）从上到下、从左到右依次访问每个节点。  
如果在遍历的过程中出现了 **空位**（即某个节点的左子或右子是 `None`），我们把它记下来。  
在完整二叉树的定义里：**一旦出现空位，后面的所有节点都必须是空位**，否则说明有节点不在最左侧。

> 类比：想象一本词典，词条按照字母顺序排好。当你在某一页发现空白（没有词条）时，后面的页码再出现词条就不合理——所有空白页后面只能是空白。

实现时：

1. 使用队列 `deque` 把根节点放进去。  
2. 只要队列不空，就弹出队首节点 `node`。  
   - 如果 `node` 不是 `None`，把它的左子、右子（即使是 `None`）依次加入队列。  
   - 如果 `node` 是 `None`，把一个标记 `found_null = True`，表示已经碰到空位。  
3. 当 `found_null` 为 `True` 时，如果后面再次弹出 **非空** 节点，就说明出现了“空位后还有节点”，直接返回 `False`。  
4. 循环结束后，没有违规情况，说明是完整二叉树，返回 `True`。

**为什么正确？**  
层序遍历恰好对应二叉树的“从上到下、从左到右”顺序。如果在这个顺序里出现了空位后还有节点，必然违背了“最后一层的节点必须尽可能靠左”的要求。反之，若始终没有这种情况，则一定满足完整二叉树的定义。

**复杂度大白话**  
- **时间 O(n)**：我们最多访问每个节点一次，`n` 是树的节点数。  
- **空间 O(n)**：最坏情况下队列里会同时保存一整层的节点，二叉树最宽的一层大约有 `n/2` 个节点，用 `O(n)` 的空间来描述。

#### 代码（Python）

```python
from collections import deque
from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def isCompleteTree_bruteforce(root: TreeNode) -> bool:
    """
    暴力的层序遍历实现：
    一旦出现空位（None），后面再出现非空节点就返回 False。
    """
    if not root:
        return True  # 空树也算完整（题目保证至少有一个节点）

    q = deque([root])      # 队列初始化，只放根节点
    found_null = False     # 标记是否已经遇到过空位

    while q:
        node = q.popleft()  # 取出队首

        if node is None:
            # 已经出现空位，后面只要还有节点就不完整
            found_null = True
        else:
            # 只要已经出现过空位，但现在又碰到实际节点，就不完整
            if found_null:
                return False
            # 把左右孩子（可能是 None）都加入队列，保持层序顺序
            q.append(node.left)
            q.append(node.right)

    # 循环结束，没有违背规则，说明是完整二叉树
    return True
```

#### 复杂度

- **时间复杂度：O(n)** — 需要遍历所有节点一次，`n` 为节点总数。  
  > “O(n)” 可以理解为“随节点数线性增长”，比如 10 个节点需要 10 步，1000 个节点需要 1000 步。

- **空间复杂度：O(n)** — 最宽层可能有接近 `n/2` 个节点，要同时存进队列。  
  > 这里的 `O(n)` 不是指一定会占满 `n` 的内存，而是“在最坏情况下不超过常数倍的 n”。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道：**关键在于“空位之后不能再出现节点”**。  
暴力实现里我们用了 `found_null` 标记并且在遍历完整棵树后才返回结果。  
实际上，这已经是最优的 **时间 O(n)**、**空间 O(n)** 方案——因为我们必须检查每个节点一次，且层序遍历本身就需要保存当前层的节点。

所谓“最优”，这里指 **在一次遍历中即可完成判定**，不需要额外的列表或两次遍历。实现上只要：

1. 用同样的 BFS。  
2. 第一次出现 `None` 时，记下 `found_null = True`。  
3. 之后若再弹出非空节点，立刻返回 `False`（提前终止），无需继续遍历。  

这样可以在最早发现违规时就停下来，平均运行时间会更好，最坏情况仍是 O(n)。

> 类比：检查排队的队伍是否有人插队。只要发现有人空位（离开），后面再有人出现（重新加入），就立刻判定为“不合法”。不必等所有人都检查完。

#### 代码（Python）

```python
def isCompleteTree(root: TreeNode) -> bool:
    """
    最优实现：在遍历过程中一旦发现空位后还有真实节点，就立即返回 False。
    """
    if not root:
        return True

    q = deque([root])
    found_null = False

    while q:
        node = q.popleft()
        if node is None:
            found_null = True
        else:
            # 已经出现过空位，但现在又出现真实节点，直接返回 False
            if found_null:
                return False
            q.append(node.left)
            q.append(node.right)

    return True
```

#### 复杂度

- **时间复杂度：O(n)** — 必须检查每个节点一次，最坏情况下遍历完整棵树。  
  > 与暴力解相比，最坏情况相同，但**提前终止**可以在出现违规的早期就结束，实际运行更快。

- **空间复杂度：O(n)** — 仍然需要队列保存当前层的节点。  
  > 这已经是层序遍历的下界，无法再进一步压缩（除非使用递归的深度优先，但会失去层序的“左到右”顺序）。

---

## 心得

- **核心技巧**：层序遍历（BFS） + “空位后不能再出现节点”的判定。  
- **适用的题型**  
  1. 判断二叉树是否是 **完全二叉树**（本题）。  
  2. 判断二叉树是否是 **满二叉树**（每层节点数恰好为 2ⁱ）。  
  3. 判断二叉树是否是 **完美二叉树**（满且所有叶子在同一层）。  
- **解题钥匙**：**一次遍历中记录“是否已经出现空位”，再遇到真实节点即判负**。

---

## 反思

- **第一反应**：看到“完整二叉树”，立刻想到层序遍历，因为它自然对应“从上到下、从左到右”的顺序。  
- **最容易踩的坑**  
  - **忘记把空子节点也加入队列**：如果只在非空节点时才加入子节点，空位信息会丢失，导致误判。  
  - **没有提前终止**：虽然不影响正确性，但会浪费时间。  
  - **特殊情况**：只有根节点的树、完全左倾或右倾的树，都必须通过测试。  
- **下次遇到同类题**：第一步想到 **“层序遍历 + 标记空位”**，然后判断是否出现 “空位后还有节点”。如果有，则直接返回 `False`。这样思路清晰、代码简洁。