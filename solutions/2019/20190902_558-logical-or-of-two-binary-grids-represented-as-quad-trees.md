# #558. 二进制网格的逻辑或（Quad-Tree 表示） / Logical OR of Two Binary Grids Represented as Quad-Trees

> 难度：中等 · 标签：Divide and Conquer、Tree · [LeetCode 链接](https://leetcode.com/problems/logical-or-of-two-binary-grids-represented-as-quad-trees/)

---

## 题目（英文原版）

**Description**

A Binary Matrix is a matrix in which all the elements are either 0 or 1.
Given quadTree1 and quadTree2. quadTree1 represents a n * n binary matrix and quadTree2 represents another n * n binary matrix.
Return a Quad-Tree representing the n * n binary matrix which is the result of logical bitwise OR of the two binary matrixes represented by quadTree1 and quadTree2.
Notice that you can assign the value of a node to True or False when isLeaf is False, and both are accepted in the answer.
A Quad-Tree is a tree data structure in which each internal node has exactly four children. Besides, each node has two attributes:
We can construct a Quad-Tree from a two-dimensional area using the following steps:
If you want to know more about the Quad-Tree, you can refer to the wiki.
Quad-Tree format:
The input/output represents the serialized format of a Quad-Tree using level order traversal, where null signifies a path terminator where no node exists below.
It is very similar to the serialization of the binary tree. The only difference is that the node is represented as a list [isLeaf, val].
If the value of isLeaf or val is True we represent it as 1 in the list [isLeaf, val] and if the value of isLeaf or val is False we represent it as 0.

**Examples**

**Example 1:**

```
class Node {
    public boolean val;
    public boolean isLeaf;
    public Node topLeft;
    public Node topRight;
    public Node bottomLeft;
    public Node bottomRight;
}
```

**Example 2:**

```
Input: quadTree1 = [[0,1],[1,1],[1,1],[1,0],[1,0]]
, quadTree2 = [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,[1,0],[1,0],[1,1],[1,1]]
Output: [[0,0],[1,1],[1,1],[1,1],[1,0]]
Explanation: quadTree1 and quadTree2 are shown above. You can see the binary matrix which is represented by each Quad-Tree.
If we apply logical bitwise OR on the two binary matrices we get the binary matrix below which is represented by the result Quad-Tree.
Notice that the binary matrices shown are only for illustration, you don't have to construct the binary matrix to get the result tree.
```

**Example 3:**

```
Input: quadTree1 = [[1,0]], quadTree2 = [[1,0]]
Output: [[1,0]]
Explanation: Each tree represents a binary matrix of size 1*1. Each matrix contains only zero.
The resulting matrix is of size 1*1 with also zero.
```

**Constraints**

- quadTree1 and quadTree2 are both valid Quad-Trees each representing a n * n grid.
- n == 2x where 0 <= x <= 9.

---

## 题目（中文翻译）

二进制矩阵（binary matrix）是指所有元素均为 `0` 或 `1` 的矩阵。  
给定 `quadTree1` 和 `quadTree2`，其中 `quadTree1` 表示一个 `n × n` 的二进制矩阵，`quadTree2` 表示另一个 `n × n` 的二进制矩阵。返回一个 **Quad-Tree**（四叉树），它表示这两个二进制矩阵进行按位逻辑或（OR）运算后的 `n × n` 二进制矩阵。  
> 注意：当节点的 `isLeaf` 为 `False` 时，你可以把该节点的 `val` 设为 `True` 或 `False`，答案两者均可接受。

### Quad-Tree（四叉树）简介
Quad-Tree 是一种树形数据结构，每个内部节点恰好有四个子节点。每个节点包含以下两个属性：

| 属性 | 含义 |
|------|------|
| `isLeaf` | 是否为叶子节点（leaf） |
| `val`    | 当 `isLeaf == True` 时，表示该区域的值 (`True` → `1`，`False` → `0`) |

除此之外，节点还有四个指针，分别指向左上、右上、左下、右下子区域：

```java
Node topLeft;
Node topRight;
Node bottomLeft;
Node bottomRight;
```

构造 Quad-Tree 的基本步骤（从二维区域递归划分）：

1. 若当前区域所有元素相同，则创建一个 `isLeaf = True`、`val` 为该元素值的叶子节点。  
2. 否则，将区域等分为四个子区域，递归构造四个子节点，并将 `isLeaf = False`、`val` 任意设置（`True` 或 `False` 均可）。  

如需了解更多，可参考维基百科的 Quad-Tree 条目。

### 序列化格式
输入/输出使用层序遍历（level order）序列化 Quad-Tree。`null` 表示该路径终止，没有后续节点。  
每个节点序列化为列表 `[isLeaf, val]`，其中：

- `isLeaf == True` → 用 `1` 表示，否则用 `0`。  
- `val == True` → 用 `1` 表示，否则用 `0`。  

### 约束条件
- `quadTree1` 与 `quadTree2` 均为合法的 Quad-Tree，分别表示一个 `n × n` 的网格。  
- `n = 2^x`，其中 `0 ≤ x ≤ 9`。  

---

## 示例

### 示例 1
```java
class Node {
    public boolean val;
    public boolean isLeaf;
    public Node topLeft;
    public Node topRight;
    public Node bottomLeft;
    public Node bottomRight;
}
```

### 示例 2
**输入**
```
quadTree1 = [[0,1],[1,1],[1,1],[1,0],[1,0]],
quadTree2 = [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,[1,0],[1,0],[1,1],[1,1]]
```
**输出**
```
[[0,0],[1,1],[1,1],[1,1],[1,0]]
```
**解释**  
`quadTree1` 与 `quadTree2` 如上图所示。可以看到每棵 Quad-Tree 所对应的二进制矩阵。  
对这两个二进制矩阵执行按位逻辑或（OR）后得到的矩阵如下所示，它正好由输出的结果 Quad-Tree 所表示。  
> 注意：题目中展示的二进制矩阵仅用于说明，你并不需要显式构造矩阵再求结果。

### 示例 3
**输入**
```
quadTree1 = [[1,0]],
quadTree2 = [[1,0]]
```
**输出**
```
[[1,0]]
```
**解释**  
每棵树都表示一个 `1 × 1` 大小的二进制矩阵，矩阵中只有一个元素 `0`。  
对这两个矩阵进行逻辑或后仍然是 `0`，因此结果树同样为 `[[1,0]]`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把两棵四叉树都 **展开** 成普通的 `n × n` 二进制矩阵（`0/1`），在矩阵上做逐位的 **或** 运算，得到结果矩阵后再 **压缩** 成四叉树返回。  

- **展开**：递归遍历四叉树，把每个叶子节点对应的子方块全部填上它的 `val`（`True`→`1`、`False`→`0`）。可以把四叉树想象成一本“分层的地图”，把每块地图的颜色（黑/白）写到一张大纸上，就是展开的过程。  
- **位运算**：对两个同大小的矩阵，同坐标位置做 `a[i][j] or b[i][j]`，这一步和我们平时在 Excel 里对两列数据做“或”一样，直接遍历即可。  
- **压缩**：把得到的矩阵重新构造成四叉树。递归检查一个子方块是否全是 `0` 或全是 `1`，如果是，就生成一个叶子节点；否则把它继续拆成四个象限，递归下去。

> **为什么正确**  
> 四叉树的本质就是对矩阵的 **层次划分**，展开后得到的矩阵与原树表示的是同一个图像。对矩阵做按位或得到的图像，重新压缩成四叉树，恰好是题目要求的返回值。

#### 代码（Python）

```python
# ---------- 定义四叉树节点 ----------
class Node:
    def __init__(self, val: bool, isLeaf: bool,
                 topLeft=None, topRight=None,
                 bottomLeft=None, bottomRight=None):
        self.val = val                # 叶子时代表 0/1，内部节点随意
        self.isLeaf = isLeaf          # 是否为叶子
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


# ---------- 1. 展开四叉树得到矩阵 ----------
def build_matrix(root: Node, size: int) -> list:
    """把四叉树展开成 size×size 的 0/1 矩阵"""
    mat = [[0] * size for _ in range(size)]

    def fill(node: Node, x: int, y: int, length: int):
        if node.isLeaf:                               # 叶子：直接填满子方块
            for i in range(x, x + length):
                for j in range(y, y + length):
                    mat[i][j] = 1 if node.val else 0
        else:                                          # 非叶子：递归四个象限
            half = length // 2
            fill(node.topLeft,     x,         y,         half)
            fill(node.topRight,    x,         y + half,  half)
            fill(node.bottomLeft,  x + half,  y,         half)
            fill(node.bottomRight, x + half,  y + half,  half)

    fill(root, 0, 0, size)
    return mat


# ---------- 2. 两矩阵按位或 ----------
def or_matrix(a: list, b: list) -> list:
    n = len(a)
    return [[a[i][j] | b[i][j] for j in range(n)] for i in range(n)]


# ---------- 3. 把矩阵压缩成四叉树 ----------
def compress(mat: list) -> Node:
    """把全 0/1 矩阵压缩成四叉树"""
    n = len(mat)

    def helper(x: int, y: int, length: int) -> Node:
        # 检查子方块是否全相同
        first = mat[x][y]
        same = True
        for i in range(x, x + length):
            for j in range(y, y + length):
                if mat[i][j] != first:
                    same = False
                    break
            if not same:
                break

        if same:                         # 全相同 → 叶子
            return Node(val=bool(first), isLeaf=True)

        half = length // 2
        return Node(
            val=False,                   # 非叶子时 val 随意，设 False
            isLeaf=False,
            topLeft=helper(x, y, half),
            topRight=helper(x, y + half, half),
            bottomLeft=helper(x + half, y, half),
            bottomRight=helper(x + half, y + half, half)
        )

    return helper(0, 0, n)


# ---------- 主函数 ----------
def intersect_bruteforce(root1: Node, root2: Node, n: int) -> Node:
    """暴力版：展开 → 按位或 → 压缩"""
    m1 = build_matrix(root1, n)
    m2 = build_matrix(root2, n)
    m = or_matrix(m1, m2)
    return compress(m)
```

> 代码里每一步都有中文注释，帮助你快速定位关键逻辑。

#### 复杂度  

- **时间复杂度**：  
  - 展开两棵树各需要遍历 `n²` 个格子 → `O(n²)`。  
  - 按位或同样是遍历 `n²` → `O(n²)`。  
  - 压缩时也要检查每个格子（最坏情况下每个格子都要访问一次） → `O(n²)`。  
  - **总计** `O(n²)`，即随矩阵面积线性增长。  
  - 大白话：如果矩阵是 1024×1024（≈10⁶ 个格子），程序会大约遍历 10⁶ 次，和直接看完整张图片的工作量差不多。  

- **空间复杂度**：  
  - 两个完整的 `n×n` 矩阵各占 `n²` 空间 → `O(n²)`。  
  - 递归栈深度是树的高度 `log₂ n`，相对于 `n²` 可忽略。  

---

### 2. 最优解

#### 思路  

**从暴力解出发，瓶颈在哪里？**  
- 暴力解把整张图片都写进内存，浪费了四叉树的压缩特性。  
- 当两棵树的某个子区域已经可以确定结果时（比如其中一棵是全 `1` 的叶子），我们完全不需要继续向下展开。

**关键观察**  

1. **按位或的“短路”特性**：  
   - 若 `node1` 是叶子且值为 `1`（全 1 区域），`node1 OR anything` 必然是全 `1`，直接返回 `node1`（或新建一个叶子 `True`）即可，无需看 `node2`。  
   - 同理，如果 `node2` 是叶子且值为 `1`，直接返回 `node2`。  
2. **递归合并**：  
   - 当两个节点都不是 “全 1” 叶子时，需要对四个象限分别递归合并，得到四个子树。  
   - 合并完四个子树后，如果它们 **全部是叶子且值相同**（全 `0` 或全 `1`），可以 **合并成父节点的叶子**，这一步叫 “合并剪枝”。  

**算法步骤**  

```
def merge(a, b):
    if a.isLeaf:
        if a.val:            # a 全 1
            return Node(True, True)
        else:                # a 全 0 → 结果完全由 b 决定
            return b
    if b.isLeaf:
        if b.val:            # b 全 1
            return Node(True, True)
        else:                # b 全 0 → 结果完全由 a 决定
            return a

    # 两个都不是全 1 的叶子，需要分别递归四个象限
    tl = merge(a.topLeft,  b.topLeft)
    tr = merge(a.topRight, b.topRight)
    bl = merge(a.bottomLeft, b.bottomLeft)
    br = merge(a.bottomRight, b.bottomRight)

    # 合并剪枝：如果四个子树都是叶子且值相同，就把它们合并成父叶子
    if tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf \
       and tl.val == tr.val == bl.val == br.val:
        return Node(tl.val, True)
    else:
        return Node(False, False, tl, tr, bl, br)
```

**核心概念解释**  

- **递归（divide & conquer）**：把大问题（合并两整棵树）拆成四个小问题（合并对应的四个象限），每次都往更细的层次走，直到可以直接判断答案（遇到叶子）。  
- **短路**：类似我们在布尔表达式 `A or B` 中，如果 `A` 为真，`B` 根本不需要计算。这里把 “叶子且值为 1” 当作“真”，直接返回。  
- **剪枝**：当四个子树都长得一样时，我们把它们“合并”为一个更大的叶子，这相当于把已经统一的区域再压缩一次。

#### 代码（Python）

```python
# ---------- 四叉树节点定义（同上） ----------
class Node:
    def __init__(self, val: bool, isLeaf: bool,
                 topLeft=None, topRight=None,
                 bottomLeft=None, bottomRight=None):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


# ---------- 最优解：递归合并 ----------
def intersect(root1: Node, root2: Node) -> Node:
    """
    合并两棵四叉树，返回表示两矩阵按位或后的四叉树。
    思路：递归 + 短路 + 剪枝
    """
    # 1️⃣ 任意一棵是 “全 1” 叶子 → 直接返回全 1 叶子
    if root1.isLeaf:
        if root1.val:                     # 全 1
            return Node(True, True)       # 结果必然全 1
        # 否则是全 0，结果完全由 root2 决定
        return root2

    if root2.isLeaf:
        if root2.val:                     # 全 1
            return Node(True, True)
        return root1

    # 2️⃣ 两棵都不是全 1 叶子 → 递归四个子象限
    tl = intersect(root1.topLeft,  root2.topLeft)
    tr = intersect(root1.topRight, root2.topRight)
    bl = intersect(root1.bottomLeft, root2.bottomLeft)
    br = intersect(root1.bottomRight, root2.bottomRight)

    # 3️⃣ 合并剪枝：如果四个子树都是叶子且值相同，就升为父叶子
    if (tl.isLeaf and tr.isLeaf and bl.isLeaf and br.isLeaf and
        tl.val == tr.val == bl.val == br.val):
        return Node(tl.val, True)         # 统一的叶子

    # 4️⃣ 否则返回内部节点，子树保持各自结构
    return Node(False, False, tl, tr, bl, br)
```

> 代码只用了 30 行左右，核心逻辑全部在 `intersect` 函数里。每一步都有中文解释，帮助你把递归的“拆分-合并”过程想象成拼图游戏。

#### 复杂度  

- **时间复杂度**：`O(m)`，其中 `m` 是两棵四叉树的节点总数。  
  - 每次递归只访问当前对应的两个节点一次，若遇到叶子直接返回，不会继续向下。  
  - 最坏情况下（两棵树都展开到最细的 1×1 叶子），节点数正好是矩阵的每个格子 `n²`，此时复杂度退化为 `O(n²)`，但这已经是**不可避免**的下界，因为输出本身也需要这么多信息。  
  - 相比暴力解，我们省掉了额外的 `n²` 矩阵空间以及重复遍历的常数因子，实际运行更快。

- **空间复杂度**：`O(h)`，递归栈深度等于四叉树的高度 `h = log₂ n`（因为每次都把区域尺寸减半）。  
  - 只要不把矩阵全部展开，我们只需要保存递归调用栈，最多几百层（`n ≤ 2^9 = 512` → `h ≤ 9`），几乎可以忽略不计。  

> **对比**：暴力解需要 `O(n²)` 的额外矩阵空间，而最优解只用 `O(log n)` 的递归栈空间，省了大量内存，且在大多数输入下运行更快。

---

## 心得

- **核心技巧**：**递归合并 + 短路剪枝**。  
  - 短路让我们在遇到“全 1”叶子时立刻确定答案，避免不必要的递归。  
  - 剪枝把四个相同的子叶子再压缩成父叶子，保持四叉树的紧凑性。  

- **该技巧适用的题型**  
  1. 两棵四叉树的合并（本题、LeetCode 558 “四叉树交集” 只不过是按位与）。  
  2. 四叉树的 **求交** / **求并** / **求差** 等布尔运算。  
  3. 区域分治类的树结构合并，如 **线段树合并**、**KD‑Tree 合并** 等。  

- **一句话总结解题钥匙**：  
  *“遇到可以直接判断的叶子就停下来，用递归把问题拆到最细，再把相同的子结果合并回去。”*

---

## 反思

- **第一反应**：直接把四叉树“还原成矩阵”，因为矩阵是最直观的表示，写代码最容易。  
- **最容易踩的坑**  
  1. **叶子为 0 的情况**：如果 `node.isLeaf` 为 `True` 且 `val=False`，不能直接返回 `node`，因为另一个树可能在该区域有 `1`，必须返回另一个树的结果。  
  2. **合并剪枝的条件**：四个子树必须全部是叶子且 `val` 完全相同，否则不能合并。忘记检查 `isLeaf` 会导致错误的内部节点被错误地压缩成叶子。  
  3. **递归深度**：虽然 `log₂ n` 很小，但在实现时仍要确保每次都正确传递对应的子节点，防止出现 `None` 引用错误。  

- **下次遇到同类题，第一步该想到**：  
  “先检查两棵树的当前节点能否**直接得出答案**（全 1/全 0 叶子），如果不能，就**递归**处理四个子象限，最后**尝试合并**子结果”。这样可以一次性把“暴力展开 → 合并 → 压缩”的思路转化为递归式的 **分而治之**。