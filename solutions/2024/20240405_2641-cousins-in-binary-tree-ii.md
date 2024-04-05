# #2641. 二叉树的堂兄弟 II / Cousins in Binary Tree II

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/cousins-in-binary-tree-ii/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, replace the value of each node in the tree with the sum of all its cousins' values.
Two nodes of a binary tree are cousins if they have the same depth with different parents.
Return the root of the modified tree.
Note that the depth of a node is the number of edges in the path from the root node to it.

**Examples**

**Example 1:**

```
Input: root = [5,4,9,1,10,null,7]
Output: [0,0,0,7,7,null,11]
Explanation: The diagram above shows the initial binary tree and the binary tree after changing the value of each node.
- Node with value 5 does not have any cousins so its sum is 0.
- Node with value 4 does not have any cousins so its sum is 0.
- Node with value 9 does not have any cousins so its sum is 0.
- Node with value 1 has a cousin with value 7 so its sum is 7.
- Node with value 10 has a cousin with value 7 so its sum is 7.
- Node with value 7 has cousins with values 1 and 10 so its sum is 11.
```

**Example 2:**

```
Input: root = [3,1,2]
Output: [0,0,0]
Explanation: The diagram above shows the initial binary tree and the binary tree after changing the value of each node.
- Node with value 3 does not have any cousins so its sum is 0.
- Node with value 1 does not have any cousins so its sum is 0.
- Node with value 2 does not have any cousins so its sum is 0.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 105].
- 1 <= Node.val <= 104

---

## 题目（中文翻译）

**描述**  
给定一棵二叉树 (binary tree) 的根节点 `root`，将树中每个节点的值替换为其所有堂兄弟（cousins）节点值的和。  
如果两节点在二叉树中具有相同的深度（depth）且父节点不同，则称它们为堂兄弟。  
返回修改后的树的根节点 `root`。  
注意，节点的深度是指从根节点到该节点路径上的边数。

**示例 1**  
```
输入: root = [5,4,9,1,10,null,7]
输出: [0,0,0,7,7,null,11]
解释: 上图展示了原始二叉树以及每个节点值被替换后的二叉树。
- 值为 5 的节点没有堂兄弟，和为 0。
- 值为 4 的节点没有堂兄弟，和为 0。
- 值为 9 的节点没有堂兄弟，和为 0。
- 值为 1 的节点的堂兄弟是节点 7，和为 7。
- 值为 10 的节点的堂兄弟也是节点 7，和为 7。
- 值为 7 的节点的堂兄弟是节点 1 与 10，和为 1+10=11。
```

**示例 2**  
```
输入: root = [3,1,2]
输出: [0,0,0]
解释: 上图展示了原始二叉树以及每个节点值被替换后的二叉树。
- 值为 3 的节点没有堂兄弟，和为 0。
- 值为 1 的节点没有堂兄弟，和为 0。
- 值为 2 的节点没有堂兄弟，和为 0。
```

**约束条件**  
- 树中节点的数量在 `[1, 10^5]` 范围内。  
- `1 <= Node.val <= 10^4`   (节点值的取值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个节点都单独去找它的表亲**（cousins），把所有表亲的值加起来就得到答案。  
要实现这个想法，需要下面几件事：

1. **知道每个节点的深度（depth）**。  
   深度就像我们在楼层里找房间的层数，根节点在第 0 层，往下走一次深度加 1。

2. **知道每个节点的父节点（parent）**。  
   只有父节点不相同的才算表亲。

3. **遍历整棵树，收集同层的所有节点**，再把和当前节点父节点相同的节点（即兄弟）剔除，剩下的就是表亲。

可以把这一步实现为**对每个节点做一次 BFS/DFS**，在遍历过程中记录每个访问到的节点的深度和父节点，然后在同一层中累加不属于同一父节点的值。

> **类比**：把树看成公司组织结构，根节点是 CEO，深度是“层级”。我们想知道某位员工的“同层但不同部门的同事”总工资。最笨的办法就是把所有员工都列出来，再一个个筛选。

**为什么这个方法能得到正确答案**  
因为我们严格按照题目定义：  
- 同层 → 深度相同  
- 不同父节点 → 父节点不相同  
只要把满足这两个条件的节点的值全部相加，就恰好是“所有表亲的值”。  

**时间/空间复杂度**  
- 对每个节点我们都要遍历整棵树一次，树里有 `n` 个节点，所以总共要做 `n` 次遍历，时间复杂度是 **O(n²)**。  
  > 这里的 `O(n²)` 可以想象成“把 10,000 本书每本都翻一遍，找出同页码的词”。当节点很多时，效率极低。

- 额外空间只用来保存遍历时的临时信息（比如 BFS 队列），最多存 `O(n)`（最坏情况下整层节点都在队列里）。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def cousinsSumBrute(root: TreeNode) -> TreeNode:
    """
    暴力解：对每个节点都遍历整棵树，计算同层且父节点不同的节点之和。
    """
    # 先把所有节点的 (depth, parent) 信息保存下来，方便后面查询
    info = []  # 每个元素是 (node, depth, parent)
    
    def dfs(node, depth, parent):
        if not node:
            return
        info.append((node, depth, parent))
        dfs(node.left, depth + 1, node)
        dfs(node.right, depth + 1, node)
    
    dfs(root, 0, None)   # 第一次遍历，收集信息
    
    # 对每个节点计算表亲和
    for cur_node, cur_depth, cur_parent in info:
        cousin_sum = 0
        for node, depth, parent in info:
            # 同层且父节点不同 → 表亲
            if depth == cur_depth and parent != cur_parent:
                cousin_sum += node.val
        cur_node.val = cousin_sum   # 直接改写原节点的值
    
    return root
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：对每个节点（`n` 个）都要遍历全部节点（`n` 次），所以是 `n × n`。

- **空间复杂度**：`O(n)`  
  解释：我们把所有节点的信息存进一个列表，列表大小正好是节点数 `n`，再加上递归栈的深度（最坏 `O(n)`）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历整棵树**。我们注意到：

1. **同一层的所有节点的值之和**是固定的，只需要算一次。  
2. 对于某个节点，它的表亲之和 = **该层总和** - **它和兄弟（同父节点的子）之和**。  
   - 因为同层的节点要么是它的兄弟，要么是表亲。把兄弟的值减掉，剩下的就是表亲的值。

所以我们可以把工作分成两遍：

- **第一遍**（DFS 或 BFS）  
  - 记录每一层的总和 `level_sum[depth]`。  
  - 同时记录每个父节点的子节点之和 `parent_sum[parent]`（如果父节点只有一个孩子，则该和就是那个孩子的值）。

- **第二遍**  
  - 再遍历一次树，对每个节点把 `new_val = level_sum[depth] - parent_sum[parent]`（根节点没有父节点，直接设为 0）。  
  - 把节点的值改为 `new_val`。

> **类比**：把每层的所有员工工资加起来得到“部门总工资”。要算某位员工的“跨部门同层同事工资”，只要把本部门（即兄弟）工资扣掉，剩下的就是答案。

**核心数据结构**  

- **字典（Hash Table）**：  
  - `level_sum` 用来把深度映射到该层的总值，像查字典一样 `level_sum[depth]` 直接得到。  
  - `parent_sum` 用来把父节点对象映射到它所有子节点值的总和。  
  - 哈希表在这里相当于一本“员工-部门工资总表”，查询和插入都是 O(1)。

**为什么是线性时间**  
- 每一次遍历只访问每个节点一次，所有的加法、字典写入/读取都是 O(1)。  
- 两次遍历相加仍是 **O(n)**，远远快于 O(n²)。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def replaceValueInTree(root: TreeNode) -> TreeNode:
    """
    最优解：两次遍历，第一次收集每层总和和每个父节点的子节点总和；
    第二次根据公式 new_val = level_sum[depth] - parent_sum[parent] 更新节点值。
    """
    from collections import defaultdict, deque

    # ---------- 第一次遍历：收集信息 ----------
    level_sum = defaultdict(int)      # depth -> 本层所有节点值之和
    parent_sum = defaultdict(int)     # parent node -> 该父节点所有子节点值之和

    # 使用 BFS 方便同时得到 depth 和 parent
    q = deque()
    q.append((root, 0, None))   # (当前节点, 深度, 父节点)

    while q:
        node, depth, parent = q.popleft()
        if not node:
            continue

        # 更新本层总和
        level_sum[depth] += node.val

        # 如果有父节点，累计该父节点的子节点和
        if parent:
            parent_sum[parent] += node.val

        # 将子节点加入队列，深度+1，当前节点成为它们的父节点
        q.append((node.left, depth + 1, node))
        q.append((node.right, depth + 1, node))

    # ---------- 第二次遍历：更新节点值 ----------
    q.append((root, 0, None))   # 再次从根开始遍历
    while q:
        node, depth, parent = q.popleft()
        if not node:
            continue

        # 根节点没有表亲，直接设为 0
        if parent is None:
            node.val = 0
        else:
            # 同层总和 - 同父节点子节点之和 = 表亲之和
            node.val = level_sum[depth] - parent_sum[parent]

        # 继续遍历子树
        q.append((node.left, depth + 1, node))
        q.append((node.right, depth + 1, node))

    return root
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们只遍历了两遍每个节点一次，所有字典操作都是常数时间。

- **空间复杂度**：`O(n)`  
  - `level_sum` 最多存 `树的最大深度`（≤ `n`）个整数。  
  - `parent_sum` 最多存 `n-1` 个父节点（根节点除外）。  
  - BFS 队列在最坏情况下会同时保存一层的所有节点，也不超过 `n`。  

相较于暴力解，时间提升了 **从平方级别到线性级别**，在节点数达到 10⁵ 时差距非常明显。

---

## 心得

- **核心技巧**：先**统计层级信息**（前缀和/层和），再利用**哈希表**把“同层-同父”关系快速抵消，得到表亲和。  
- **适用场景**：  
  1. “同层节点之间的某种聚合”类问题（例如 LeetCode 1022‑**子树的最大平均值**的层次遍历版本）。  
  2. “排除同父/同子/同兄弟的聚合”类问题（例如“每层节点的值减去兄弟之和”。）  
  3. 需要**两遍遍历**才能先收集全局信息再局部更新的题目（如“每层节点的值设为该层最大值”）。  
- **一句话总结**：**先算层总和，再减去同父子节点和**，即可一次遍历完成所有表亲求和。

---

## 反思

- **第一反应**：直接对每个节点遍历整棵树去找表亲，代码能写出来但显得很慢。  
- **最容易踩的坑**  
  - **根节点没有父节点**，需要单独处理（答案应为 0）。  
  - **只有单个子节点的父节点**，`parent_sum[parent]` 只包含这个子节点本身，公式仍然成立。  
  - **大树深度很深**，递归实现可能导致栈溢出，建议使用显式的 BFS/迭代 DFS。  
- **下次类似题目**：第一步先问自己“是否可以一次遍历把所有‘全局’信息（层和、全局最大/最小等）算出来”，然后再在第二遍利用这些信息做局部更新。这样往往能把 O(n²) 的暴力解降到 O(n)。