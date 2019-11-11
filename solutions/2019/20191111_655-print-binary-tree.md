# #655. **打印二叉树** / Print Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/print-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, construct a 0-indexed m x n string matrix res that represents a formatted layout of the tree. The formatted layout matrix should be constructed using the following rules:
Return the constructed matrix res.

**Examples**

**Example 1:**

```
Input: root = [1,2]
Output: 
[["","1",""],
 ["2","",""]]
```

**Example 2:**

```
Input: root = [1,2,3,null,4]
Output: 
[["","","","1","","",""],
 ["","2","","","","3",""],
 ["","","4","","","",""]]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 210].
- -99 <= Node.val <= 99
- The depth of the tree will be in the range [1, 10].

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，构造一个下标从 0 开始的 `m × n` 字符串矩阵 `res`，该矩阵用于以格式化的方式展示这棵树。矩阵的构造需要遵循以下规则（题目原文中给出）：

- **返回** 构造好的矩阵 `res`。

**示例 1**  
**示例 2**  

**约束条件**  

- 树中节点的数量在 `[1, 2^10]` 范围内。  
- `-99 ≤ Node.val ≤ 99`  
- 树的深度在 `[1, 10]` 范围内。  

**示例**

**示例 1**  
输入: `root = [1,2]`  
输出: 
```json
[["","1",""],
 ["2","",""]]
```

**示例 2**  
输入: `root = [1,2,3,null,4]`  
输出: 
```json
[["","","","1","","",""],
 ["","2","","","","3",""],
 ["","","4","","","",""]]
```

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **先求树的高度**  
   树的高度（根到最深叶子的层数）决定了矩阵的行数 `m`。  
   - 递归求左子树高度、右子树高度，取较大者再加 1。  
   - 这一步相当于“先把树的大小量一下”，后面才能安排位置。

2. **确定矩阵宽度**  
   根据题目要求，第 `i` 行（0‑index）最多能放 `2^i` 个节点。  
   整棵树的宽度 `n = 2^m - 1`（把所有可能的节点位置都预留出来），  
   就好像在一张纸上画出一棵完整的二叉树的框架，空格用空字符串 `""` 填充。

3. **暴力地找每个节点的列坐标**  
   - 对每个节点，我们把它的 **左子树节点数** 作为偏移量。  
   - 具体做法：  
     1. 递归地遍历整棵树（先序或中序均可）。  
     2. 对当前节点 `node`，先递归左子树得到左子树的节点总数 `left_cnt`。  
     3. 该节点在所在行的列索引 = `left_cnt + offset`，`offset` 是从根开始累计的偏移（根的 `offset = (n-1)//2`）。  
     4. 再递归右子树，继续累加左子树节点数 + 1（当前节点）作为新的 `offset`。  

   这里把 **左子树的节点数** 当成“左边已经占了多少格”，就像在排队时看前面已经站了几个人，决定自己要站在哪个位置。  
   由于每次都要遍历整棵子树来统计节点数，这一步的时间代价会是 **O(N²)**（N 为节点数），尤其在树很不平衡时会出现大量重复计数。

4. **把结果写进矩阵**  
   先把 `m × n` 的矩阵全部填成空字符串 `""`，随后把每个节点的值（转成字符串）写入对应的 `[row][col]` 位置即可。

#### 代码（Python）

```python
from typing import List, Optional

# ------------------- 辅助定义 -------------------
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


# ------------------- 暴力解 -------------------
def printTree_bruteforce(root: TreeNode) -> List[List[str]]:
    # 1. 求树高
    def get_height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return 1 + max(get_height(node.left), get_height(node.right))

    m = get_height(root)                # 行数
    n = (1 << m) - 1                     # 2^m - 1，列数
    # 2. 初始化全空矩阵
    res = [["" for _ in range(n)] for _ in range(m)]

    # 3. 统计子树节点数（暴力版会重复统计）
    def count_nodes(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)

    # 4. 递归填值，同时计算列坐标
    def dfs(node: Optional[TreeNode], row: int, offset: int) -> None:
        if not node:
            return
        # 左子树节点数决定当前节点的列位置
        left_cnt = count_nodes(node.left)          # 每次都遍历左子树 → O(N²)
        col = offset + left_cnt
        res[row][col] = str(node.val)              # 写入矩阵

        # 递归左、右子树，左子树的 offset 不变，右子树的 offset 需要加上左子树+当前节点
        dfs(node.left, row + 1, offset)
        dfs(node.right, row + 1, offset + left_cnt + 1)

    dfs(root, 0, 0)
    return res
```

#### 复杂度  

- **时间复杂度**：`O(N²)`  
  - `count_nodes` 在每个节点上都会遍历它的左子树一次，最坏情况下会导致 `1 + 2 + … + N ≈ N²/2` 次访问。  
  - “`N²`” 可以理解为：如果有 1000 个节点，程序大约会做 1,000,000 次基本操作，远大于线性 `N`（1000）级别。

- **空间复杂度**：`O(N)`  
  - 主要是存放返回的矩阵（`m × n ≈ N`），以及递归栈深度最多为树的高度 `m ≤ 10`（本题受限），所以总体是线性空间。

---  

### 2. 最优解  

#### 思路  

1. **瓶颈在哪？**  
   暴力解的慢点在于每次都要**重新统计左子树的节点数**，这相当于“每次都去重新数一遍已经数过的东西”。我们只需要在 **一次遍历** 中把每个节点应该出现的列位置算出来即可。

2. **利用二分法的列宽递减规律**  
   - 题目已经暗示了列宽的递减方式：根节点位于最中间 `(n-1)//2`，左子树的根向左移动 `gap = 2^{height-2}`，右子树向右同样移动 `gap`，然后 `gap` 再除以 2，层层递减。  
   - 这正好像我们在一棵 **满二叉树**（每层都填满）里定位节点，只是实际树可能有空洞，我们仍然按照满树的“框架”来放置。

3. **核心算法：递归/DFS + 前置宽度**  
   - 先求树的高度 `h`，得到矩阵宽度 `n = 2^h - 1`。  
   - 从根开始，设根所在列 `mid = (n-1)//2`。  
   - 对左子树，列坐标 = `mid - offset`；对右子树，列坐标 = `mid + offset`，其中 `offset = 2^{h - depth - 2}`（`depth` 为当前层数，从 0 开始）。  
   - 递归向下时，`offset` 每进入下一层就 **除以 2**，因为左右两侧的空位越来越少。  

   这一步只遍历一次树，**每个节点只计算一次列坐标**，时间是线性的 `O(N)`。

4. **实现细节**  
   - **矩阵初始化**：`res = [["" for _ in range(n)] for _ in range(h)]`。  
   - **递归函数** `fill(node, row, col, offset)`：  
     - 把 `node.val` 写入 `res[row][col]`。  
     - 若左子树存在，递归 `fill(node.left, row+1, col-offset, offset//2)`。  
     - 若右子树存在，递归 `fill(node.right, row+1, col+offset, offset//2)`。  
   - `offset` 初始值为 `2^{h-2}`（根的左右子树间隔），当 `h == 1` 时（只有根），`offset` 为 0，递归直接结束。

5. **类比帮助理解**  
   把完整的二叉树想象成 **一条尺子**，根在尺子的正中间，两边分别是左、右子树的“伸展区”。每往下一层，左右两侧的伸展区都 **缩小一半**，就像把尺子折叠一次。我们只需要记录每次折叠的长度（`offset`），就能直接定位每个节点的位置。

#### 代码（Python）

```python
from typing import List, Optional

# ------------------- 辅助定义 -------------------
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


# ------------------- 最优解 -------------------
def printTree(root: TreeNode) -> List[List[str]]:
    # 1. 计算树高（递归）
    def get_height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return 1 + max(get_height(node.left), get_height(node.right))

    h = get_height(root)                # 行数
    n = (1 << h) - 1                     # 列数 = 2^h - 1

    # 2. 初始化全空矩阵
    res = [["" for _ in range(n)] for _ in range(h)]

    # 3. 递归填值
    def fill(node: Optional[TreeNode], row: int, col: int, offset: int) -> None:
        if not node:
            return
        res[row][col] = str(node.val)   # 把当前节点写进矩阵

        # 左子树：列坐标往左 offset，右子树往右 offset
        # offset //= 2 代表下一层的间距减半
        if node.left:
            fill(node.left, row + 1, col - offset, offset // 2)
        if node.right:
            fill(node.right, row + 1, col + offset, offset // 2)

    # 根节点的列坐标是矩阵最中间，初始 offset = 2^{h-2}
    initial_offset = (1 << (h - 2)) if h >= 2 else 0
    fill(root, 0, (n - 1) // 2, initial_offset)

    return res
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 每个节点只被访问一次，做常数次计算（写入矩阵、计算下一层的 offset），所以运行时间与节点数线性增长。  
  - 相比暴力的 `N²`，如果有 1000 个节点，最优解只需要大约 1000 次操作。

- **空间复杂度**：`O(N)`  
  - 矩阵本身占 `h × (2^h-1) ≈ N`（因为满二叉树的节点数恰好是 `2^h-1`），递归栈深度最多为树的高度 `h ≤ 10`，可以忽略不计。

---  

## 心得  

- **核心技巧**：利用二叉树的满树结构，**递归/DFS** 中把“间距 `offset`”随层数除以 2，直接定位每个节点的列坐标。  
- **适用的题型**  
  1. “把二叉树打印成二维数组” 系列（如 LeetCode 655 Print Binary Tree）。  
  2. “二叉树的垂直遍历” 需要把节点映射到固定列坐标。  
  3. “二叉树的层序遍历（Zigzag）” 中也会用到层号与列号的对应关系。  
- **一句话总结**：**一次遍历，递归维护每层的列间距**，就是这道题的“解题钥匙”。  

---  

## 反思  

- **第一反应**：先算出树的高度，然后按照 `2^h-1` 的宽度把每层的“空位”全部铺开，接着想办法把每个节点放到对应的格子里。  
- **最容易踩的坑**  
  1. **高度为 1 时 offset 计算**：`2^{h-2}` 在 `h=1` 时会出现负指数，需要单独判断（设为 0）。  
  2. **整数除法**：`offset // 2` 必须使用整数除法，否则会得到浮点数导致索引错误。  
  3. **矩阵列索引越界**：根节点列是 `(n-1)//2`，一定要确保所有递归产生的 `col ± offset` 不会超过 `[0, n-1]`（满二叉树的结构天然保证）。  
- **下次类似题的第一步**：**先把完整的“框架”算出来（高度 → 行数、宽度 → 列数），再用递归把每个节点放进框架的对应位置**。这样思路清晰，代码也容易写对。