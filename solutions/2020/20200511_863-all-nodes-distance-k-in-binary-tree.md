# #863. 二叉树中距离为 K 的所有节点 / All Nodes Distance K in Binary Tree

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, the value of a target node target, and an integer k, return an array of the values of all nodes that have a distance k from the target node.
You can return the answer in any order.

**Examples**

**Example 1:**

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
Output: [7,4,1]
Explanation: The nodes that are a distance 2 from the target node (with value 5) have values 7, 4, and 1.
```

**Example 2:**

```
Input: root = [1], target = 1, k = 3
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [1, 500].
- 0 <= Node.val <= 500
- All the values Node.val are unique.
- target is the value of one of the nodes in the tree.
- 0 <= k <= 1000

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`、一个目标节点（target node）`target` 的值，以及一个整数 `k`，返回一个数组（array），其中包含所有与目标节点的距离（distance）恰好为 `k` 的节点的值。答案可以以任意顺序返回。

**示例 1**  
**输入**: `root = [3,5,1,6,2,0,8,null,null,7,4]`, `target = 5`, `k = 2`  
**输出**: `[7,4,1]`  
**解释**: 与目标节点（值为 5）距离为 2 的节点的值为 7、4 和 1。

**示例 2**  
**输入**: `root = [1]`, `target = 1`, `k = 3`  
**输出**: `[]`

**约束条件**  
- 树中节点的数量在区间 `[1, 500]` 内。  
- `0 <= Node.val <= 500`  
- 所有 `Node.val` 的取值互不相同。  
- `target` 是树中某个节点的值。  
- `0 <= k <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个节点都当成“起点”，分别去找一遍它到目标节点的距离**，如果距离恰好等于 `k`，就把它的值加入答案。  

实现时可以这样：

1. **遍历整棵树**，把所有节点保存到一个列表 `all_nodes`（相当于把树的所有“人”都叫出来排成一排）。  
2. 对列表中的每个节点 `node`，**用一次深度优先搜索（DFS）** 从 `node` 出发，寻找目标节点 `target`，记录走了多少步——这就是 `node` 到目标的距离。  
3. 如果得到的距离正好是 `k`，把 `node.val` 放进结果数组。

> **类比**：把树想象成一座城镇，节点是房子，边是道路。暴力做法就是把每一栋房子出发，跑一遍全城去找目标房子，记录路程——显然很费力。

**为什么正确**：  
DFS 能完整遍历从起点到所有可达节点的路径，找到了目标节点后返回的步数就是两者之间的最短距离（因为树中任意两点只有唯一一条路径）。只要把所有节点都尝试一次，就一定能找出所有距离为 `k` 的节点。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def distance(root: TreeNode, start: TreeNode, target_val: int) -> int:
    """
    从 start 出发，用 DFS 找到值为 target_val 的节点，返回路径长度。
    若找不到返回 -1（这里在树里一定能找到）。
    """
    if not root:
        return -1
    if root.val == target_val:
        return 0                     # 已经在目标节点，距离 0

    # 递归左子树
    left = distance(root.left, start, target_val)
    if left != -1:                    # 左子树找到了
        return left + 1               # 加上从当前节点到左子节点的这一步

    # 递归右子树
    right = distance(root.right, start, target_val)
    if right != -1:                   # 右子树找到了
        return right + 1

    return -1                         # 本子树不存在目标节点

def collect_nodes(root: TreeNode, nodes: list):
    """把整棵树的所有节点收集到列表 nodes 中（相当于把所有人叫出来）。"""
    if not root:
        return
    nodes.append(root)
    collect_nodes(root.left, nodes)
    collect_nodes(root.right, nodes)

def distanceK_bruteforce(root: TreeNode, target: TreeNode, k: int) -> list:
    all_nodes = []
    collect_nodes(root, all_nodes)            # 第一步：把所有节点放进列表

    ans = []
    for node in all_nodes:                     # 对每个节点都尝试一次
        d = distance(root, node, target.val)   # 计算 node 到 target 的距离
        if d == k:
            ans.append(node.val)               # 距离恰好为 k，加入答案
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N²)`  
  - 解释：`N` 是树的节点数。我们对每个节点都要跑一次完整的 DFS，最坏情况下每次遍历整棵树，等价于 `N` 次 `N` 的工作，即 `N × N = N²`。把 `O(N²)` 想成“如果树有 1000 个节点，程序大概要做 100 万 次基本操作”。  
- **空间复杂度**：`O(N)`  
  - 解释：递归栈深度最多 `N`（当树退化成链表时），加上保存所有节点的列表同样是 `N`，所以整体是线性的。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要重新遍历整棵树** 来算距离。实际上，树本身是一种 **无向图**：每条父子关系都可以视作两条双向道路。只要把这条“道路”两端都记下来，就可以像在普通图里那样 **一次 BFS（广度优先搜索）** 从目标节点出发，层层向外扩散，恰好第 `k` 层的节点就是答案。

实现步骤：

1. **把二叉树转换成邻接表**（每个节点对应一个列表，存放它的相邻节点）。  
   - 递归遍历树，**把左子节点和父节点、右子节点和父节点互相加入**。这一步相当于把“父子道路”拆成两条可以双向走的路。  
   - 用 `defaultdict(list)`（类似于查字典，键是节点的值，值是相邻节点的对象）保存。  
2. **从目标节点 `target` 开始做 BFS**。  
   - 使用队列 `deque`，先把 `target` 放进去，记录已访问的节点防止回头（就像在城镇里走路不想走回头路）。  
   - 每弹出一次队列元素，就把它的未访问邻居全部加入队列，层数 `dist` 加 1。  
   - 当 `dist == k` 时，队列里剩下的所有节点就是恰好距离 `k` 的节点，直接把它们的值收集返回。  
3. 如果 BFS 完成都没有到达第 `k` 层（比如 `k` 超出树的最大深度），返回空列表。

> **核心技巧**：把树视为无向图 + BFS 求“第几层的节点”。  
> **类比**：想象在一座城镇里，目标房子是出发点，所有道路都是双向的。我们让一个小队从目标房子出发，一圈一圈（层）向外搜寻，搜到第 `k` 圈时，看到的所有房子就是答案。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def build_graph(node: TreeNode, graph: defaultdict):
    """
    递归遍历二叉树，把每条父子关系都写成无向边。
    graph[父] 包含 子，graph[子] 包含 父。
    """
    if not node:
        return
    if node.left:
        graph[node.val].append(node.left)          # 父 -> 左子
        graph[node.left.val].append(node)          # 左子 -> 父（双向）
        build_graph(node.left, graph)
    if node.right:
        graph[node.val].append(node.right)         # 父 -> 右子
        graph[node.right.val].append(node)         # 右子 -> 父（双向）
        build_graph(node.right, graph)

def distanceK(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    # 1️⃣ 把树转换成无向图
    graph = defaultdict(list)      # key: 节点值，value: 相邻节点对象列表
    build_graph(root, graph)

    # 2️⃣ BFS 从 target 开始
    q = deque([target])             # 队列里存的是 TreeNode 对象
    visited = set([target.val])     # 已访问集合，防止回头
    dist = 0                        # 当前层数（距离）

    while q:
        if dist == k:               # 已经走到第 k 步，队列里都是答案
            return [node.val for node in q]

        # 否则继续向外扩散一层
        for _ in range(len(q)):     # 只遍历当前层的节点
            cur = q.popleft()
            for nxt in graph[cur.val]:
                if nxt.val not in visited:
                    visited.add(nxt.val)
                    q.append(nxt)
        dist += 1                    # 层数+1

    # BFS 结束仍未到达 k，说明 k 超出树的深度
    return []
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 解释：构图遍历每个节点一次 `O(N)`，BFS 也最多遍历每个节点一次，总共不超过两遍，所以仍是线性时间。相比暴力的 `N²`，如果树有 500 个节点，最多只需要大约 1000 次基本操作。  
- **空间复杂度**：`O(N)`  
  - 解释：邻接表保存每条边，两端各存一次，总数与节点数同阶 `O(N)`；BFS 队列和 visited 集合同样最多装 `N` 个节点。

---

## 心得

- **核心技巧**：把二叉树视作无向图，再用 **BFS** 求第 `k` 层节点。  
- **适用的题型**（类似思路）  
  1. `866. 回文串分割 II` → 把状态图转成无向图，BFS 求最短转换次数。  
  2. `1129. 颜色分类` → 把相邻格子看成图的节点，BFS/DFS 求连通块。  
  3. `1971. 寻找图中是否存在路径` → 直接在无向图上做 BFS/DFS。  
- **一句话总结**：**把树变成可以“双向走”的图，一次 BFS 就能一次性得到所有距离为 K 的节点**。

---

## 反思

- **第一反应**：先想“从目标往上、往下走”，于是想到把父指针记录下来，随后再遍历。但最直接的实现是把整棵树直接变成无向图，省去手动找父节点的繁琐。  
- **最容易踩的坑**  
  1. **忘记把父节点加入邻接表**，导致只能向下搜索，找不到向上走的节点。  
  2. **BFS 层数计数错误**：要在层结束后才 `dist += 1`，否则会提前或延迟判断。  
  3. **目标节点本身的值可能是唯一的**，但在构图时要用 `TreeNode` 对象而不是仅值，以免出现同值不同节点的混淆（本题值唯一，仍建议保持对象引用）。  
- **下次遇到同类题**：第一步立刻思考 **“这棵树/结构能否当成图来处理？”**，如果可以，优先考虑 **BFS（最短层）或 DFS（遍历所有）**，而不是逐个节点重复遍历。