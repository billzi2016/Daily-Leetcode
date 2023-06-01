# #2265. 统计子树平均值等于节点值的节点数 / Count Nodes Equal to Average of Subtree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/count-nodes-equal-to-average-of-subtree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the number of nodes where the value of the node is equal to the average of the values in its subtree.
Note:

**Examples**

**Example 1:**

```
Input: root = [4,8,5,0,1,null,6]
Output: 5
Explanation: 
For the node with value 4: The average of its subtree is (4 + 8 + 5 + 0 + 1 + 6) / 6 = 24 / 6 = 4.
For the node with value 5: The average of its subtree is (5 + 6) / 2 = 11 / 2 = 5.
For the node with value 0: The average of its subtree is 0 / 1 = 0.
For the node with value 1: The average of its subtree is 1 / 1 = 1.
For the node with value 6: The average of its subtree is 6 / 1 = 6.
```

**Example 2:**

```
Input: root = [1]
Output: 1
Explanation: For the node with value 1: The average of its subtree is 1 / 1 = 1.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- 0 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，返回满足 **节点值等于其子树（subtree）中所有节点值的平均值** 的节点数量。

**示例 1**

```
Input: root = [4,8,5,0,1,null,6]
Output: 5
Explanation:
对于值为 4 的节点：其子树的平均值为 (4 + 8 + 5 + 0 + 1 + 6) / 6 = 24 / 6 = 4。
对于值为 5 的节点：其子树的平均值为 (5 + 6) / 2 = 11 / 2 = 5。
对于值为 0 的节点：其子树的平均值为 0 / 1 = 0。
对于值为 1 的节点：其子树的平均值为 1 / 1 = 1。
对于值为 6 的节点：其子树的平均值为 6 / 1 = 6。
（其余节点的平均值不等于节点值，故不计入结果。）
```

**示例 2**

```
Input: root = [1]
Output: 1
Explanation:
对于值为 1 的节点：其子树的平均值为 1 / 1 = 1。
```

**约束条件**

- 树中节点的数量在 `[1, 1000]` 区间内。
- `0 <= Node.val <= 1000`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每个节点**，把它所在的子树的所有节点值都收集起来，算出平均值（向下取整），然后和当前节点的值比较是否相等。  

- **数据结构**：  
  - **队列/栈**：遍历子树时可以使用递归（系统自带的调用栈），也可以显式用 `list` 当作栈，类似把树的每个分支当成“要去超市买东西的购物清单”。  
  - **列表**：把子树里出现的所有节点值存进列表，像把所有商品的价格记在一张纸上，最后求和再除以数量得到平均价。  

- **为什么正确**：  
  对每个节点我们都完整地遍历了它的子树，拿到了子树里所有节点的值，计算的平均值就是题目要求的子树平均值。如果这一步得到的平均值恰好等于节点本身的值，则该节点满足条件。遍历所有节点后计数即为答案。

- **复杂度分析**（大白话）  
  - 对每个节点我们都要 **再次遍历它的子树**。假设树有 `n` 个节点，根节点的子树大小是 `n`，第二层的两个节点各自的子树大小约为 `n/2`，如此往下。总的遍历次数大约是 `n + (n-1) + (n-2) + … + 1 = n·(n+1)/2`，这就是 **O(n²)** 的时间复杂度。可以把它想象成：有 `n` 本书，每本书都要把前面所有的书都读一遍，显然会很慢。  
  - 额外空间只用来保存一次遍历时的临时列表，最坏情况下列表里会装下整棵树的所有节点值，大小为 `O(n)`。如果用递归实现，还会有递归栈深度 `O(h)`（`h` 为树高），在最坏的链状树里 `h = n`，所以总体仍是 **O(n)** 的空间。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def countNodes(root: TreeNode) -> int:
    """暴力解：对每个节点都遍历它的子树求平均"""
    if not root:
        return 0

    # 1. 先统计整棵树里有多少个节点
    nodes = []

    def preorder(node: TreeNode):
        """先序遍历，把所有节点放进列表 nodes 中"""
        if not node:
            return
        nodes.append(node)          # 把当前节点记下来
        preorder(node.left)         # 左子树
        preorder(node.right)        # 右子树

    preorder(root)

    ans = 0

    # 2. 对每个节点，计算它子树的和与节点数
    for cur in nodes:
        vals = []   # 用来存子树里所有节点的值

        def dfs(node: TreeNode):
            """深度优先遍历 cur 为根的子树，把所有值收集到 vals"""
            if not node:
                return
            vals.append(node.val)   # 类似把商品价格写进账本
            dfs(node.left)
            dfs(node.right)

        dfs(cur)                     # 收集 cur 子树的所有值
        total = sum(vals)            # 子树所有值的总和
        cnt = len(vals)              # 子树的节点个数
        avg = total // cnt           # 向下取整的平均值
        if avg == cur.val:           # 判断是否相等
            ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  想象把每本书都要把之前的所有书都读一遍，随 `n` 增大，工作量呈二次方增长。

- **空间复杂度**：`O(n)`  
  需要一个列表保存全部节点（`O(n)`），以及递归栈的最深深度 `O(h)`，在最坏情况下 `h=n`，仍然是线性空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复遍历子树** 是主要的性能瓶颈。我们可以把“子树的**和**”和“子树的**节点数**”这两个信息**一次遍历就算好**，然后在回溯的过程中直接比较平均值，这样每个节点只被访问一次，时间降到线性 `O(n)`。

实现思路：

1. **后序遍历**（先左、后右、最后根），因为要先知道左、右子树的和与大小，才能算出当前节点的子树信息。  
2. 对每个节点返回一个二元组 `(size, sum)`：  
   - `size` = 左子树节点数 + 右子树节点数 + 1（自己）  
   - `sum`  = 左子树所有值的和 + 右子树所有值的和 + `node.val`  
3. 在返回之前，先用 `sum // size` 计算向下取整的平均值，若等于 `node.val`，计数器 `ans` 加一。  
4. 整棵树遍历完后，`ans` 就是答案。

**核心数据结构**：

- **递归调用栈**：把树的结构天然映射为函数调用的层次，类似“把每层楼的工作交给对应的工作人员”，不需要额外的容器。  
- **整数**：只需要保存两个整数（子树大小、子树和），相当于“只记账本的两行：总金额、件数”，极其轻量。

**为什么正确**：

后序遍历保证了在处理当前节点时，左、右子树的信息已经完整且正确地算出来了。因为子树的和和大小是**唯一确定的**（不受遍历顺序影响），用它们算平均值得到的结果必然等价于题目中“把子树所有节点值相加再除以节点数”。因此每次比较都是合法的，计数的总和就是符合条件的节点数。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def countNodes(root: TreeNode) -> int:
    """最优解：一次 DFS 返回子树大小和子树和，时间 O(n)"""
    ans = 0  # 用来统计满足条件的节点个数

    def dfs(node: TreeNode):
        """
        返回 (size, total)：
        - size : 子树的节点数
        - total: 子树所有节点值的和
        同时在递归过程中更新全局计数 ans
        """
        nonlocal ans
        if not node:
            return (0, 0)          # 空子树：大小 0，和 0

        # 递归左、右子树，得到它们的 (size, total)
        left_size, left_sum = dfs(node.left)
        right_size, right_sum = dfs(node.right)

        # 当前子树的大小和和
        cur_size = left_size + right_size + 1
        cur_sum = left_sum + right_sum + node.val

        # 计算向下取整的平均值
        avg = cur_sum // cur_size   # // 是整数除法，自动向下取整

        # 若平均值恰好等于当前节点的值，则计数器加一
        if avg == node.val:
            ans += 1

        return (cur_size, cur_sum)  # 把信息向上层返回

    dfs(root)   # 从根节点开始遍历
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个节点只被访问一次（一次函数调用），相当于“只读一遍书”，所以随 `n` 增大，工作量线性增长。

- **空间复杂度**：`O(h)`（递归栈深度）  
  只需要保存递归调用的栈帧。`h` 是树的高度，最坏情况下（链状树）`h = n`，此时空间是 `O(n)`；在平衡二叉树里 `h ≈ log n`，更省空间。相比暴力解的 `O(n)` 列表，已经大幅降低。

---

## 心得

- **核心技巧**：后序遍历（DFS）一次性返回子树的**大小**和**和**，利用这些信息即可在 O(1) 时间内判断当前节点是否满足条件。  
- **适用题型**：  
  1. “子树信息聚合”类，如 **“子树中节点的最大/最小值”**、**“子树中满足某种属性的节点数”**。  
  2. **“树的均值/加权平均”**、**“树的直径”**（需要从子树向上合并信息）。  
  3. **“返回每个节点的子树大小/子树和”**（如 LeetCode 814、1028 等）。  
- **一句话总结**：**“把子树需要的所有信息一次算好，后续比较只用 O(1) 时间”**。

---

## 反思

- **第一反应**：看到“子树的平均值”就想到要把子树的所有节点值收集起来，于是想到暴力的“遍历子树求和”方案。  
- **最容易踩的坑**：  
  - 忘记对 **空子树** 返回 `(0,0)`，导致除以 0 错误。  
  - 使用普通除法 `/` 得到浮点数，而题目要求向下取整（整数除法 `//`），容易导致比较不相等。  
  - 对 **递归返回值** 的顺序写反（先返回和再返回大小），会导致后续计算错误。  
- **下次类似题的第一步**：先思考**“要比较的条件需要哪些子树信息”**（比如和、大小、最大值），然后设计**一次遍历返回这些信息**的递归函数，避免重复遍历。