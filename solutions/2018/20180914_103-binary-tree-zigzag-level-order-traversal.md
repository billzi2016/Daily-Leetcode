# #103. 二叉树之锯齿形层序遍历 / Binary Tree Zigzag Level Order Traversal

> 难度：中等 · 标签：Tree、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]
```

**Example 2:**

```
Input: root = [1]
Output: [[1]]
```

**Example 3:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 2000].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，返回其节点值的锯齿形层序遍历结果。即第一层从左到右遍历，第二层从右到左遍历，之后的层交替进行。

**示例**

**示例 1**  
Input: `root = [3,9,20,null,null,15,7]`  
Output: `[[3],[20,9],[15,7]]`

**示例 2**  
Input: `root = [1]`  
Output: `[[1]]`

**示例 3**  
Input: `root = []`  
Output: `[]`

**约束条件**

- 树中节点的数量在 `[0, 2000]` 区间内。  
- `-100 <= Node.val <= 100`（节点值的范围）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐层遍历**二叉树（层序遍历），把每一层的节点值收集成一个列表。  
层序遍历本质上是 **广度优先搜索（BFS）**，我们可以用 **队列** 来实现。  
- 队列就像排队买饭的队伍，先进入的人先出来（先进先出）。  
- 把根节点先放进队列，然后循环：取出队首节点，记录它的值，同时把它的左、右子节点（如果有）依次加入队列。这样每次循环结束后，队列里恰好是**下一层**的所有节点。

得到每层的节点列表后，只要把奇数层（从 0 开始计数）的列表**反转**，就可以得到锯齿形（Zigzag）的遍历顺序。

> 为什么这个方法一定能得到正确答案？  
> 因为 BFS 保证我们一次只处理同一层的节点，层与层之间的相对顺序不被打乱。只要在收集完每层后根据层数决定是否反转，就能完整地模拟“左→右、右→左、左→右 …”的要求。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


from collections import deque
def zigzagLevelOrder(root: TreeNode) -> list[list[int]]:
    if not root:                     # 空树直接返回空列表
        return []

    result = []                      # 最终返回的二维列表
    queue = deque([root])            # 用 deque 实现队列，初始只放根节点
    left_to_right = True             # 标记当前层的遍历方向

    while queue:                     # 只要队列不空，就还有未访问的层
        level_size = len(queue)      # 这一层有多少节点
        level_vals = []              # 暂存当前层的节点值

        for _ in range(level_size):  # 逐个弹出本层节点
            node = queue.popleft()   # 取出队首节点
            level_vals.append(node.val)

            # 把子节点加入队列，供下一层使用
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        # 根据遍历方向决定是否要反转本层结果
        if not left_to_right:
            level_vals.reverse()     # 右向左时把列表倒过来

        result.append(level_vals)    # 把处理好的本层加入答案
        left_to_right = not left_to_right   # 翻转方向，为下一层做准备

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 这里的 `n` 是树中节点的数量。我们每个节点只会被 **弹出一次**、**检查一次子节点**，所以总操作次数和节点数成正比。  
  - 大白话：如果树有 1000 个节点，算法大约会跑 1000 次基本操作。

- **空间复杂度**：`O(n)`（最坏情况）  
  - 主要的额外空间是队列 `queue`。在最宽的一层（比如完全二叉树的最后一层），队列里可能会同时存放约 `n/2` 个节点。  
  - 大白话：如果树有 2000 个节点，最多会同时占用大约 1000 个节点的内存空间。

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性时间**，已经是最优的时间复杂度了。但我们可以在 **空间使用** 和 **实现细节** 上再做一点改进，使代码更简洁、常数因子更小。

**瓶颈**  
- 在暴力解里，我们在每层结束后用 `list.reverse()` 把列表倒序，这一步虽然是 `O(k)`（k 为本层节点数），但会产生一次额外的遍历。  
- 还有一种思路是：直接在遍历时决定把节点值放到当前层列表的 **左端** 还是 **右端**，这样就不需要事后再反转。

**优化思路**  
使用 **双端队列（deque）** 作为当前层的容器：

- 当本层的遍历方向是 **左→右** 时，像普通 BFS 那样把节点值 **追加到右端**（`append`）。
- 当遍历方向是 **右→左** 时，改为把节点值 **追加到左端**（`appendleft`），这样得到的列表天然就是倒序的。

这样我们只遍历一次节点，就完成了“收集 + 方向处理”。空间仍然是 `O(n)`，但省掉了 `reverse` 的额外遍历，代码也更直观。

#### 代码（Python）

```python
from collections import deque
def zigzagLevelOrder_opt(root: TreeNode) -> list[list[int]]:
    if not root:
        return []

    result = []
    node_queue = deque([root])      # 用于层序遍历的普通队列
    left_to_right = True            # 当前层的遍历方向

    while node_queue:
        level_size = len(node_queue)
        level_vals = deque()        # 双端队列，支持左端/右端追加

        for _ in range(level_size):
            node = node_queue.popleft()
            # 根据方向决定把值放到左端还是右端
            if left_to_right:
                level_vals.append(node.val)      # 正序放在右端
            else:
                level_vals.appendleft(node.val)  # 逆序放在左端

            # 子节点仍然按左、右顺序加入下一层的队列
            if node.left:
                node_queue.append(node.left)
            if node.right:
                node_queue.append(node.right)

        result.append(list(level_vals))   # 把 deque 转成普通 list 保存
        left_to_right = not left_to_right  # 翻转方向

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次，`appendleft` 也是 `O(1)` 的操作。相比暴力解省掉了每层的 `reverse`，常数因子更小。

- **空间复杂度**：`O(n)`  
  - 仍然需要保存整棵树的节点（队列）以及每层的结果列表。使用 `deque` 存放当前层的值并不会额外增加数量级的空间。

---

## 心得

- **核心技巧**：**双端队列（deque）** 能在 **O(1)** 时间完成“左端插入 / 右端插入”，非常适合需要在同一层里根据方向动态决定顺序的场景。  
- **适用题型**：  
  1. `Binary Tree Zigzag Level Order Traversal`（本题）。  
  2. `Spiral Matrix`（矩阵的螺旋遍历）——同样需要在不同方向上交替插入。  
  3. `Deque Sliding Window Maximum`（滑动窗口最大值）——利用双端队列维护窗口内的单调序列。  
- **一句话总结**：**用 deque 把“顺序”和“逆序”合并到同一次遍历里，就能一次搞定锯齿层序**。

## 反思

- **第一反应**：看到“Zigzag”立刻想到普通层序遍历 + 每层反转。  
- **最容易踩的坑**：  
  - 忘记在空树（`root = None`）时直接返回空列表，会导致后面的 `queue.popleft()` 报错。  
  - 在实现 `appendleft` 时把方向写反，导致最终结果是左→右、左→右…的普通层序。  
  - 处理完一层后忘记翻转遍历方向，导致所有层都走同一种顺序。  
- **下次遇到同类题**：第一步先**确定遍历顺序是否会随层变化**，如果会，考虑用 **deque** 在遍历时直接决定插入方向，避免事后再翻转。这样思路更清晰，代码也更简洁。