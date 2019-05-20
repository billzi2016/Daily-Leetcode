# #427. **构造四叉树** / Construct Quad Tree

> 难度：中等 · 标签：Array、Divide and Conquer、Tree、Matrix · [LeetCode 链接](https://leetcode.com/problems/construct-quad-tree/)

---

## 题目（英文原版）

**Description**

Given a n * n matrix grid of 0's and 1's only. We want to represent grid with a Quad-Tree.
Return the root of the Quad-Tree representing grid.
A Quad-Tree is a tree data structure in which each internal node has exactly four children. Besides, each node has two attributes:
We can construct a Quad-Tree from a two-dimensional area using the following steps:
If you want to know more about the Quad-Tree, you can refer to the wiki.
Quad-Tree format:
You don't need to read this section for solving the problem. This is only if you want to understand the output format here. The output represents the serialized format of a Quad-Tree using level order traversal, where null signifies a path terminator where no node exists below.
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
Input: grid = [[0,1],[1,0]]
Output: [[0,1],[1,0],[1,1],[1,1],[1,0]]
Explanation: The explanation of this example is shown below:
Notice that 0 represents False and 1 represents True in the photo representing the Quad-Tree.
```

**Example 3:**

```
Input: grid = [[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0],[1,1,1,1,0,0,0,0]]
Output: [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,[1,0],[1,0],[1,1],[1,1]]
Explanation: All values in the grid are not the same. We divide the grid into four sub-grids.
The topLeft, bottomLeft and bottomRight each has the same value.
The topRight have different values so we divide it into 4 sub-grids where each has the same value.
Explanation is shown in the photo below:
```

**Constraints**

- n == grid.length == grid[i].length
- n == 2x where 0 <= x <= 6

---

## 题目（中文翻译）

给定一个仅包含 `0` 和 `1` 的 `n × n` 矩阵 `grid`。我们希望用四叉树（Quad-Tree）来表示 `grid`，并返回表示该 `grid` 的四叉树的根节点。

四叉树是一种树形数据结构，每个内部节点恰好有四个子节点。除此之外，每个节点还有两个属性：  
- `isLeaf`：表示该节点是否为叶子节点。  
- `val`：当节点为叶子节点时，表示该区域的值（`0` 或 `1`）。

我们可以使用以下步骤从二维区域构建四叉树：

1. 如果当前子矩阵的所有元素相同，则创建一个叶子节点 `isLeaf = true`，`val` 为该元素的值。  
2. 否则，将当前子矩阵划分为四个等大小的子矩阵，递归构造左上、右上、左下、右下四个子节点，并将 `isLeaf = false`。

如果想了解更多关于四叉树的内容，可参考维基百科（wiki）。

### 四叉树的序列化格式

下面的说明仅用于理解输出格式，**不必阅读此部分来求解本题**。输出使用层序遍历（level order traversal）对四叉树进行序列化，`null` 表示该路径结束（不存在子节点）。这与二叉树的序列化非常相似，唯一的区别是每个节点用列表 `[isLeaf, val]` 表示：

- `isLeaf` 为 `true` 时记作 `1`，为 `false` 时记作 `0`。  
- `val` 为 `true` 时记作 `1`，为 `false` 时记作 `0`。

### 示例

**示例 1**

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

**示例 2**

```
Input: grid = [[0,1],[1,0]]
Output: [[0,1],[1,0],[1,1],[1,1],[1,0]]
Explanation: 下面的示意图展示了该示例的解释：
注意，图中 `0` 代表 `False`，`1` 代表 `True`，对应四叉树的 `isLeaf` 与 `val`。
```

**示例 3**

```
Input: grid = [[1,1,1,1,0,0,0,0],
               [1,1,1,1,0,0,0,0],
               [1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1],
               [1,1,1,1,0,0,0,0],
               [1,1,1,1,0,0,0,0],
               [1,1,1,1,0,0,0,0],
               [1,1,1,1,0,0,0,0]]
Output: [[0,1],[1,1],[0,1],[1,1],[1,0],null,null,null,null,[1,0],[1,0],[1,1],[1,1]]
Explanation: 网格中的所有值并不全部相同，需要将其划分为四个子网格。  
左上、左下和右下子网格的值相同，构成叶子节点。  
右上子网格的值不相同，进一步划分为四个子网格，每个子网格的值都相同。  
下面的示意图展示了该过程的可视化。
```

### 约束条件

- `n == grid.length == grid[i].length`
- `n == 2^x`，其中 `0 <= x <= 6` (即 `n` 为 1、2、4、8、16、32、64、128)

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **递归** 把矩阵不断划分成四个子矩阵，直到子矩阵里的所有元素全部相同为止。  
实现步骤如下：

1. **判断当前子矩阵是否全为 0 或全为 1**  
   - 直接遍历子矩阵的每一个格子，用两个 `for` 循环检查是否出现不同的值。  
   - 这一步可以想象成在一本书里翻页查找：我们把要查的区域当作“一页”，把每个格子当作“词”，逐个对比，看是否全是同一个词。

2. **如果全相同** → 建立一个 **叶子节点** (`isLeaf=True`，`val` 为该统一的值)。  

3. **否则** → 把矩阵划分成左上、右上、左下、右下四块，递归处理每块，得到四个子节点，再把它们挂到一个 **内部节点** (`isLeaf=False`) 上。

> 为什么这一步一定能得到正确答案？  
> 四叉树的定义正是把一个区域不断细分，直到每块区域内部的值统一为止。我们用递归恰好模拟了这种“不断细分、到底”的过程，所以得到的树一定满足题目要求。

**时间/空间分析（大白话）**  

- **时间复杂度**：每次判断子矩阵是否统一都要遍历整个子矩阵。最坏情况下（矩阵里交错出现 0、1），我们会对每一个子矩阵都进行一次完整遍历。设矩阵边长为 `n`，递归层数约为 `log₂ n`，每层会检查 `n² / 4^level` 大小的子矩阵，总体时间大约是  
  \[
  O\big(n^2 + 4\cdot\frac{n^2}{4} + 16\cdot\frac{n^2}{16} + \dots\big)=O(n^3)
  \]  
  简单理解就是：**每个格子会被检查很多次**，最差会被检查到 `log n` 次，导致整体是立方级别。

- **空间复杂度**：递归调用栈的深度最多 `log₂ n`，每层只保存常数个指针，所以是  
  \[
  O(\log n)
  \]  
  （不计返回的四叉树本身，它是题目要求的输出）。

#### 代码（Python）

```python
# Definition for a QuadTree node.
class Node:
    def __init__(self, val, isLeaf, topLeft=None, topRight=None,
                 bottomLeft=None, bottomRight=None):
        self.val = val                # True / False
        self.isLeaf = isLeaf          # 是否为叶子节点
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


class Solution:
    def construct(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: Node
        """
        n = len(grid)

        # 递归函数：处理左上角坐标 (x, y) 和子矩阵的边长 size
        def helper(x, y, size):
            # 1️⃣ 检查子矩阵是否全相同
            first = grid[x][y]               # 取左上角的值作基准
            same = True
            for i in range(x, x + size):
                for j in range(y, y + size):
                    if grid[i][j] != first:  # 只要出现不同的，就不是统一子矩阵
                        same = False
                        break
                if not same:
                    break

            # 2️⃣ 若统一 → 直接返回叶子节点
            if same:
                return Node(bool(first), True)

            # 3️⃣ 否则 → 四等分，递归处理四个子区域
            half = size // 2
            tl = helper(x, y, half)                     # 左上
            tr = helper(x, y + half, half)              # 右上
            bl = helper(x + half, y, half)              # 左下
            br = helper(x + half, y + half, half)       # 右下
            return Node(True, False, tl, tr, bl, br)    # 内部节点，val 随便填

        return helper(0, 0, n)
```

#### 复杂度  

- **时间复杂度**：`O(n³)` — 因为每层递归都要遍历整个子矩阵，格子会被重复检查多次。  
- **空间复杂度**：`O(log n)` — 递归栈的最大深度是矩阵划分的层数（`log₂ n`），其余空间仅是常数级别。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出 **瓶颈** 在于「每次都要遍历子矩阵来判断是否统一」。  
如果我们能够 **在 O(1) 时间内快速得到任意子矩阵中 1 的个数**，就可以立刻判断该子矩阵是否全 0（计数为 0）或全 1（计数等于面积），从而避免重复遍历。

**核心技巧：二维前缀和（Prefix Sum）**  

- 把原矩阵 `grid` 转换成一个同样大小的累计矩阵 `pre`，其中 `pre[i][j]` 表示左上角 `(0,0)` 到 `(i-1, j-1)`（不含 `i, j`）的所有元素之和。  
- 这一步类似于在一本词典里做「章节累计页码」：我们预先算好每一段的总页数，后面查询任意段落的页数只需要几次加减运算。  

**查询子矩阵和的公式**（左闭右开区间）：

```
sum = pre[x2][y2] - pre[x1][y2] - pre[x2][y1] + pre[x1][y1]
```

其中 `(x1, y1)` 为左上角，`(x2, y2)` 为右下角的**下一个**坐标（即不包括在内），`size = x2 - x1 = y2 - y1`。

利用前缀和，我们的递归判断只需要 **一次 O(1) 查询**，随后再递归四个子区域。这样每个格子只会在**构造前缀和**时被访问一次，之后的判断不再遍历格子。

**整体流程**：

1. **预处理**：构造二维前缀和 `pre`，时间 `O(n²)`。  
2. **递归构造**：  
   - 用前缀和快速得到当前子矩阵的 1 的总数 `ones`。  
   - 若 `ones == 0` → 全部为 0，返回叶子节点 `val=False`。  
   - 若 `ones == size*size` → 全部为 1，返回叶子节点 `val=True`。  
   - 否则 → 按四等分递归，生成内部节点。  

**为什么这样更快？**  
- 每个格子只参与一次前缀和的累加，之后的判断不再遍历格子。  
- 递归层数仍是 `log₂ n`，但每层的工作量是 **常数**（四次 O(1) 查询），于是总时间是 `O(n²)`，与读取矩阵本身的代价持平。

#### 代码（Python）

```python
# Definition for a QuadTree node.
class Node:
    def __init__(self, val, isLeaf, topLeft=None, topRight=None,
                 bottomLeft=None, bottomRight=None):
        self.val = val                # True / False
        self.isLeaf = isLeaf          # 是否为叶子节点
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


class Solution:
    def construct(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: Node
        """
        n = len(grid)

        # ---------- 1️⃣ 预处理：二维前缀和 ----------
        # pre[i][j] 表示左上角 (0,0) 到 (i-1, j-1)（不含 i、j）的 1 的总数
        pre = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            row_sum = 0
            for j in range(n):
                row_sum += grid[i][j]                 # 累计当前行的和
                pre[i + 1][j + 1] = pre[i][j + 1] + row_sum
                # pre[i][j+1] 是上一行累计的和，row_sum 是本行到 (i, j) 的和

        # ---------- 2️⃣ 递归构造四叉树 ----------
        def helper(x, y, size):
            """
            x, y : 当前子矩阵左上角坐标（相对于原矩阵）
            size : 子矩阵的边长
            """
            # 使用前缀和 O(1) 求子矩阵中 1 的个数
            x2, y2 = x + size, y + size
            ones = (pre[x2][y2] - pre[x][y2] - pre[x2][y] + pre[x][y])

            # 全 0
            if ones == 0:
                return Node(False, True)
            # 全 1
            if ones == size * size:
                return Node(True, True)

            # 否则继续划分
            half = size // 2
            tl = helper(x, y, half)                       # 左上
            tr = helper(x, y + half, half)                # 右上
            bl = helper(x + half, y, half)                # 左下
            br = helper(x + half, y + half, half)         # 右下
            return Node(True, False, tl, tr, bl, br)      # 内部节点

        return helper(0, 0, n)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 构造前缀和遍历矩阵一次 `O(n²)`。  
  - 递归阶段每个子矩阵只做 O(1) 的前缀和查询，递归节点总数不超过 `4/3 * n²`（与矩阵格子数同阶），所以整体仍是 `O(n²)`。  
  - 与暴力解相比，从 **立方级** 降到了 **平方级**，大幅提升效率。

- **空间复杂度**：`O(n²)`（前缀和矩阵）+ `O(log n)`（递归栈）  
  - 前缀和额外占用一个 `n+1 × n+1` 的整数矩阵。  
  - 递归深度最多 `log₂ n`，相对于 `n ≤ 64`（因为 `n = 2^x, x ≤ 6`），栈空间可以忽略不计。

---

## 心得  

- **核心技巧**：**二维前缀和** + **递归划分**（Divide & Conquer）。  
- **适用题型**  
  1. “子矩阵求和” 类问题（例如 LeetCode 304、1314）。  
  2. 需要快速判断子区域是否满足某种“统一性” 的题目（如“矩阵区域是否全为 0/1”）。  
  3. 类似的四叉树或线段树构造问题。  

- **一句话总结解题钥匙**：  
  *“先把全局信息预处理好（前缀和），后面每次只用 O(1) 直接判断是否需要继续细分”。*  

---

## 反思  

- **拿到题目第一反应**：先写递归检查每块是否统一——最自然的实现方式，却会在最坏情况下重复遍历大量格子。  
- **最容易踩的坑**  
  1. **边界坐标**：前缀和的查询是左闭右开区间，容易把 `+1` 写错导致越界或漏计。  
  2. **叶子节点的 `val` 类型**：题目要求 `bool`，而 `grid` 中是 `0/1`，记得在返回时用 `bool()` 转换。  
  3. **递归结束条件**：一定要在 `size == 1` 时返回叶子，防止出现无限递归（虽然前缀和已经能判断统一性，但大小为 1 时更直观）。  
- **下次遇到同类题**：第一步就思考“有没有办法一次性把子区域的信息预先算好”，如果可以，用前缀和或其他前缀结构把“是否统一” 的判定变成 O(1)。这样就能把暴力的重复遍历降到线性级别。