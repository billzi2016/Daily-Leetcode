# #2326. 螺旋矩阵 IV / Spiral Matrix IV

> 难度：中等 · 标签：Array、Linked List、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/spiral-matrix-iv/)

---

## 题目（英文原版）

**Description**

You are given two integers m and n, which represent the dimensions of a matrix.
You are also given the head of a linked list of integers.
Generate an m x n matrix that contains the integers in the linked list presented in spiral order (clockwise), starting from the top-left of the matrix. If there are remaining empty spaces, fill them with -1.
Return the generated matrix.

**Examples**

**Example 1:**

```
Input: m = 3, n = 5, head = [3,0,2,6,8,1,7,9,4,2,5,5,0]
Output: [[3,0,2,6,8],[5,0,-1,-1,1],[5,2,4,9,7]]
Explanation: The diagram above shows how the values are printed in the matrix.
Note that the remaining spaces in the matrix are filled with -1.
```

**Example 2:**

```
Input: m = 1, n = 4, head = [0,1,2]
Output: [[0,1,2,-1]]
Explanation: The diagram above shows how the values are printed from left to right in the matrix.
The last space in the matrix is set to -1.
```

**Constraints**

- 1 <= m, n <= 105
- 1 <= m * n <= 105
- The number of nodes in the list is in the range [1, m * n].
- 0 <= Node.val <= 1000

---

## 题目（中文翻译）

给定两个整数 `m` 和 `n`，表示矩阵的行数和列数。  
同时给定一个整数链表（linked list）的头节点 `head`。  
请生成一个 `m × n` 的矩阵，使其中的整数按螺旋顺序（spiral order，顺时针）填入，填充起点为矩阵的左上角。若链表中的元素全部写入后仍有剩余空格，则用 `-1` 填充这些空位。  
返回生成的矩阵。

**示例 1**  
```text
Input: m = 3, n = 5, head = [3,0,2,6,8,1,7,9,4,2,5,5,0]
Output: [[3,0,2,6,8],[5,0,-1,-1,1],[5,2,4,9,7]]
Explanation: 上图展示了链表中的值如何按照螺旋顺序写入矩阵。
注意，矩阵中剩余的空格均被填为 -1。
```

**示例 2**  
```text
Input: m = 1, n = 4, head = [0,1,2]
Output: [[0,1,2,-1]]
Explanation: 上图展示了值从左到右依次写入矩阵的过程。
矩阵最后一个位置被设为 -1。
```

**约束条件**  
- `1 <= m, n <= 10^5`  
- `1 <= m * n <= 10^5`  
- 链表节点数在 `[1, m * n]` 范围内  
- `0 <= Node.val <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把矩阵想成一个**棋盘**，从左上角出发，按顺时针螺旋的路线把链表里的数一个一个写进去。  
- **数据结构**：  
  - `matrix`：用二维列表存放结果，初始时全部填 `-1`（相当于把整个棋盘先涂成灰色）。  
  - `visited`（或直接检查 `matrix[i][j] != -1`）：用来判断当前位置是否已经写过，类似 **查字典** 时看词是否已经出现过。  
  - `directions`：四个方向的向量 `[(0,1),(1,0),(0,-1),(-1,0)]`，分别代表「右、下、左、上」，把它想象成手里的一支「指南针」，每转一次 90° 就换一个方向。  

- **写入过程**：  
  1. 把链表的头结点值写到 `(0,0)`。  
  2. 按当前方向前进一步。如果新坐标超出了矩阵边界或已经写过（`matrix[i][j] != -1`），说明该方向走不通，需要**顺时针转向**（把指南针顺时针转 90°）。  
  3. 重复步骤 2，直到链表遍历完或者矩阵已经全部填满。  

- **为什么正确**：  
  螺旋顺序的定义恰好是「在当前方向走不到了就换方向」，我们每一次都严格遵守这条规则，所以填入的顺序必然是题目要求的顺时针螺旋。

- **时间/空间复杂度**：  
  - **时间**：我们会访问每个格子至多一次（最多 `m*n` 次），每次访问只做 O(1) 的判断和写入，所以总时间是 **O(m·n)**。  
    - 大白话：如果矩阵有 10000 个格子，程序大概会跑 10000 步左右。  
  - **空间**：除了返回的 `matrix` 本身（必须的），我们还用了一个 `visited`（或直接用 `matrix` 判断）来标记已写入的格子，额外的空间是 **O(m·n)**。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def spiralMatrix(m: int, n: int, head: ListNode):
    """
    暴力模拟螺旋填表
    """
    # 1. 先把整个矩阵填成 -1，表示「空格」——相当于先把棋盘涂成灰色
    matrix = [[-1] * n for _ in range(m)]

    # 2. 四个方向，顺时针依次是「右、下、左、上」
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0                     # 当前使用的方向下标
    i, j = 0, 0                     # 起始坐标左上角

    cur = head                      # 链表当前节点
    while cur:
        matrix[i][j] = cur.val      # 把当前节点的值写进去
        cur = cur.next              # 移到下一个节点

        # 计算下一步的坐标
        ni, nj = i + dirs[dir_idx][0], j + dirs[dir_idx][1]

        # 判断「能否继续往当前方向走」：
        # 1）没有越界 2）下一个格子仍是 -1（未被写过）
        if not (0 <= ni < m and 0 <= nj < n and matrix[ni][nj] == -1):
            # 方向不通，顺时针转 90°
            dir_idx = (dir_idx + 1) % 4
            ni, nj = i + dirs[dir_idx][0], j + dirs[dir_idx][1]

        i, j = ni, nj                # 把坐标移动到下一格

    return matrix
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` — 每个格子最多访问一次，实际运行步数和格子数成正比。  
- **空间复杂度**：`O(m·n)` — 需要存放返回的矩阵，额外的 `dirs`、指针等只占常数空间。  

---

### 2. 最优解  

#### 思路  
暴力解已经是 **线性** 的时间复杂度，已经达到了题目约束（`m·n ≤ 10⁵`）的上限。  
唯一可以改进的地方是**省掉额外的 visited 标记**，直接利用**四条边界**来判断何时转向。  

- **为什么暴力会慢**  
  在暴力实现里，我们每一步都要检查「下一个格子是否已经写过」 (`matrix[ni][nj] == -1`)。虽然这一步是 O(1)，但会产生一次额外的数组读取。对 10⁵ 规模的输入影响不大，但在面试中展示「边界法」更能体现对螺旋遍历的深刻理解。  

- **核心技巧：四条边界**  
  想象我们在围一个矩形的围栏，围栏的四条边分别是  
  - `top`   ：当前可写的最上面一行的索引  
  - `bottom`: 当前可写的最下面一行的索引  
  - `left`  ：当前可写的最左边一列的索引  
  - `right` ：当前可写的最右边一列的索引  

  当我们沿着某条边写完以后，就把对应的边界向内收缩一格（比如写完最上面一行后，`top += 1`），这样自然保证了「不会碰到已经写过的格子」。  

- **实现步骤**  
  1. 初始化 `top = 0, bottom = m-1, left = 0, right = n-1`。  
  2. 按「右 → 下 → 左 → 上」四个方向循环：  
     - **右**：遍历列 `left … right`，行固定为 `top`，写完后 `top += 1`。  
     - **下**：遍历行 `top … bottom`，列固定为 `right`，写完后 `right -= 1`。  
     - **左**：遍历列 `right … left`（逆序），行固定为 `bottom`，写完后 `bottom -= 1`。  
     - **上**：遍历行 `bottom … top`（逆序），列固定为 `left`，写完后 `left += 1`。  
  3. 每写入一个格子，就把链表指针向前移动；如果链表已经空了，就直接停止循环，剩余格子保持初始的 `-1`。  

- **类比**：把矩阵看成一块披萨，`top、bottom、left、right` 就是披萨的四根刀子，每吃完一圈就把刀子往中心收紧一次，直到披萨吃完或材料用完。  

#### 代码（Python）

```python
def spiralMatrix(m: int, n: int, head: ListNode):
    """
    使用四条边界的螺旋填表，省去额外的 visited 检查
    """
    # 1. 初始化全为 -1 的矩阵
    matrix = [[-1] * n for _ in range(m)]

    # 2. 四条边界
    top, bottom = 0, m - 1
    left, right = 0, n - 1

    cur = head                     # 链表当前节点

    # 只要还有节点且还有未填满的格子，就继续
    while cur and top <= bottom and left <= right:
        # ---- 向右 ----
        for col in range(left, right + 1):
            if not cur: break
            matrix[top][col] = cur.val
            cur = cur.next
        top += 1                    # 上边界下移

        # ---- 向下 ----
        for row in range(top, bottom + 1):
            if not cur: break
            matrix[row][right] = cur.val
            cur = cur.next
        right -= 1                  # 右边界左移

        # ---- 向左 ----
        if top <= bottom:           # 可能已经没有行了
            for col in range(right, left - 1, -1):
                if not cur: break
                matrix[bottom][col] = cur.val
                cur = cur.next
            bottom -= 1             # 下边界上移

        # ---- 向上 ----
        if left <= right:           # 可能已经没有列了
            for row in range(bottom, top - 1, -1):
                if not cur: break
                matrix[row][left] = cur.val
                cur = cur.next
            left += 1               # 左边界右移

    return matrix
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` — 每个格子最多写一次，循环次数与格子数线性相关。与暴力解相比，常数更小（省去 visited 判断），在大数据下更快。  
- **空间复杂度**：`O(m·n)` — 只存放返回的矩阵，没有额外的 `visited`，额外空间是 `O(1)`（仅四个边界变量）。  

---

## 心得  

- **核心技巧**：利用四条可收缩的边界来实现螺旋遍历，既省空间又省一步「是否已访问」的判断。  
- **适用场景**：  
  1. **螺旋矩阵遍历**（LeetCode 54、59、59‑II、59‑III）  
  2. **矩形区域的层层收缩**（如「矩阵旋转 90°」）  
  3. **围栏收缩类模拟**（比如「矩阵分层求和」）  
- **一句话总结**：**“把矩阵四周的围栏一步步向内收”，就能自然得到顺时针螺旋顺序。**  

---

## 反思  

- **第一反应**：直接把链表的值写进一个预先填好的 `-1` 矩阵，遇到边界或已写的格子就转向。  
- **最容易踩的坑**：  
  - 边界条件不严谨导致重复写入或越界（特别是单行/单列的矩阵）。  
  - 链表长度可能小于 `m·n`，要记得在遍历过程中随时检查 `cur` 是否为空，提前结束循环。  
- **下次类似题的第一步**：先明确「螺旋」的转向规则，决定是用「visited 标记」还是「四条收缩边界」来判断何时换方向。这样可以快速搭建出正确且高效的遍历框架。