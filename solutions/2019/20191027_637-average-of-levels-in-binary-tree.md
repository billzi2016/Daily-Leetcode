# #637. 二叉树的层平均值 / Average of Levels in Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/average-of-levels-in-binary-tree/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: [3.00000,14.50000,11.00000]
Explanation: The average value of nodes on level 0 is 3, on level 1 is 14.5, and on level 2 is 11.
Hence return [3, 14.5, 11].
```

**Example 2:**

```
Input: root = [3,9,20,15,7]
Output: [3.00000,14.50000,11.00000]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -231 <= Node.val <= 231 - 1

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，返回一个数组 `answer`，其中 `answer[i]` 为二叉树第 `i` 层（level）所有节点值的平均值（average）。  
层的顺序从根节点所在的第 0 层开始，依次向下递增。

**示例 1**  
**输入**: `root = [3,9,20,null,null,15,7]`  
**输出**: `[3.00000,14.50000,11.00000]`  
**解释**: 第 0 层的节点只有 `3`，平均值为 `3`；第 1 层的节点是 `9` 和 `20`，平均值为 `(9 + 20) / 2 = 14.5`；第 2 层的节点是 `15` 和 `7`，平均值为 `(15 + 7) / 2 = 11`。因此返回 `[3, 14.5, 11]`。

**示例 2**  
**输入**: `root = [3,9,20,15,7]`  
**输出**: `[3.00000,14.50000,11.00000]`

**约束条件**  
- 树中节点的数量在 `[1, 10^4]` 范围内。  
- `-2^31 <= Node.val <= 2^31 - 1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：**先求出树的层数**（也叫高度），然后**一次遍历树**，把第 `0` 层、第 `1` 层…的所有节点的值分别累加、计数，最后算平均数。

如果不想一次遍历把所有层的信息都记录下来，也可以**对每一层单独遍历**：  
1. 先用递归或循环找出树的最大深度 `h`（即有多少层）。  
2. 对层号 `0 … h‑1`，**再遍历整棵树**，只把当前层号相等的节点的值加到 sum，计数器 `cnt` 加一。  
3. 结束后 `sum / cnt` 就是该层的平均值。

> **类比**：想象你在一本厚厚的电话簿里查找不同页码的电话号码。  
> - “层号” 就像页码，  
> - “遍历整棵树” 就像从头到尾翻阅整本电话簿，找到对应页码的所有号码。  
> 这样每查一页都要把整本电话簿重新翻一遍，显然很慢，但思路最直接。

**为什么正确**：每次遍历都会把**所有**节点都检查一遍，只要节点所在的层号等于目标层，就把它的值计入该层的统计。遍历完后，统计得到的总和与计数必然对应该层的所有节点，除法自然得到平均值。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def averageOfLevels(root):
    # ---------- 第一步：求树的最大深度 ----------
    def get_height(node):
        if not node:
            return 0
        # 左右子树高度取大者，加上当前节点所在层
        return 1 + max(get_height(node.left), get_height(node.right))

    h = get_height(root)                 # 树一共有 h 层（层号 0~h-1）

    # ---------- 第二步：对每一层单独遍历 ----------
    res = []                               # 用来存放每层的平均值

    # 递归遍历整棵树，收集目标层的节点值
    def collect(node, target_level, cur_level, container):
        if not node:
            return
        if cur_level == target_level:      # 到达目标层，累计
            container[0] += node.val       # container[0] 保存 sum
            container[1] += 1              # container[1] 保存 count
        else:
            # 继续向下搜索左右子树
            collect(node.left, target_level, cur_level + 1, container)
            collect(node.right, target_level, cur_level + 1, container)

    for lvl in range(h):                   # 对每一层都做一次完整遍历
        sum_cnt = [0, 0]                   # [sum, count] 初始化为 0
        collect(root, lvl, 0, sum_cnt)    # 收集该层的所有节点值
        avg = sum_cnt[0] / sum_cnt[1]      # 计算平均值（浮点数）
        res.append(avg)

    return res
```

> **关键行中文注释** 已在代码中给出，帮助你对每一步的目的有清晰认识。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `n` 为树中节点数。  
  - 我们对每一层（至多 `h ≤ n`）都遍历一次整棵树，第一次遍历 `n` 次，第二次又 `n` 次……总共约 `n * h ≈ n²` 次操作。  
  - 用“大白话”说，就是**每个节点被检查了很多次**，所以会慢。

- **空间复杂度**：`O(h)`（递归栈）  
  - `get_height` 与 `collect` 的递归深度最多等于树的高度 `h`，在最坏情况下（完全不平衡的链状树）`h = n`，但一般情况下 `h` 远小于 `n`。  
  - 其它额外存储只有常数级别（`sum_cnt`、`res`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈**在于“每层都要重新遍历整棵树”。  
如果我们**一次遍历就把所有层的信息都收集完整**，就能把时间降到 `O(n)`。

实现思路有两种等价方式：

1. **层序遍历（Breadth‑First Search，BFS）**  
   - 使用队列一次把当前层的所有节点弹出、统计它们的值，然后把它们的子节点（下一层）全部加入队列。  
   - 这样天然“一层一层”地处理，遍历一次即可得到每层的总和与节点数。

2. **深度优先遍历（DFS）配合两条数组**  
   - 用递归记录每个节点所在的层号 `depth`。  
   - 维护两个列表 `sums[depth]`、`counts[depth]`，在访问节点时直接把它的值加到对应层的 sum，计数器 `counts` 加一。  
   - 递归结束后，遍历这两个列表算平均值。

下面采用 **BFS**（队列）实现，因为它直观易懂，且只用到**队列**这种数据结构——可以把它想象成**排队等候的队伍**，先进入的先服务。

> **类比**：把树的每一层看成电影院的不同排座位，BFS 就像一次性把第 1 排的观众叫进去坐好、统计票价，然后再叫第 2 排的，以此类推。一次叫完所有排，过程不需要回头再找。

#### 代码（Python）

```python
from collections import deque   # deque 是双端队列，适合做 BFS 的“排队”

# Definition for a binary tree node (同上)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def averageOfLevels(root):
    if not root:
        return []

    queue = deque([root])      # 初始队列只装根节点
    averages = []              # 最终返回的每层平均值

    while queue:               # 只要还有未处理的节点，就继续
        level_sum = 0          # 本层节点值的累计和
        level_cnt = len(queue) # 本层节点的数量 = 当前队列长度

        for _ in range(level_cnt):   # 逐个弹出本层的所有节点
            node = queue.popleft()   # 取出队首节点
            level_sum += node.val     # 累加值

            # 将子节点加入队列，供下一轮处理（相当于把下一层的观众叫进来）
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        averages.append(level_sum / level_cnt)   # 计算本层平均值

    return averages
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点恰好被**访问一次、加入队列一次、弹出一次**，所以总操作数与节点数线性相关。  
  - 与暴力解相比，省掉了重复遍历的 `n` 次，真正做到“一遍遍历全搞定”。

- **空间复杂度**：`O(w)`（其中 `w` 为树的最大宽度）  
  - 队列里最多同时保存同一层的所有节点。  
  - 对于一棵完全二叉树，最大宽度约为 `n/2`，但一般情况下 `w` 远小于 `n`。  
  - 额外的 `averages` 列表只保存每层一个数，空间开销可以忽略不计。

---

## 心得

- **核心技巧**：**层序遍历（BFS）**一次收集每层信息，避免重复遍历。  
- **适用的题型**  
  1. “二叉树的层序遍历” (`Binary Tree Level Order Traversal`)  
  2. “二叉树的最大宽度” (`Maximum Width of Binary Tree`)  
  3. “二叉树的最左侧视图” (`Binary Tree Left Side View`)  

- **一句话总结解题钥匙**：**一次遍历把层级信息全部记录**，不必为每层再跑一遍树。

---

## 反思

- **第一反应**：看到“每层的平均值”，自然想到“先分层、再求平均”。于是想到 **层序遍历**，但因为刚学算法，最先想到的是 **对每层单独遍历**（暴力）——直观但慢。

- **最容易踩的坑**  
  1. **空树**：题目保证至少有一个节点，但在写通用函数时仍要考虑 `root is None` 的情况。  
  2. **整数溢出**：节点值范围很大（`-2^31` 到 `2^31-1`），累计求和时使用 Python 的 `int` 完全安全，但在某些语言需要使用 64 位整数。  
  3. **浮点数精度**：输出要求保留小数，直接使用除法 `/` 得到 `float` 即可，Python 会自动保留足够精度。

- **下次遇到同类题**：第一步立刻问自己 “能否一次遍历把所有层的信息都记录下来？”——如果答案是 “能”，就去实现 **BFS**（或 DFS + 层级数组）；如果不能再考虑其他思路。这样可以快速排除暴力解，直接朝最优解前进。