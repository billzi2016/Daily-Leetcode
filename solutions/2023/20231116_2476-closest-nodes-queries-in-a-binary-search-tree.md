# #2476. 二叉搜索树中的最近节点查询 / Closest Nodes Queries in a Binary Search Tree

> 难度：中等 · 标签：Array、Binary Search、Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/closest-nodes-queries-in-a-binary-search-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary search tree and an array queries of size n consisting of positive integers.
Find a 2D array answer of size n where answer[i] = [mini, maxi]:
Return the array answer.

**Examples**

**Example 1:**

```
Input: root = [6,2,13,1,4,9,15,null,null,null,null,null,null,14], queries = [2,5,16]
Output: [[2,2],[4,6],[15,-1]]
Explanation: We answer the queries in the following way:
- The largest number that is smaller or equal than 2 in the tree is 2, and the smallest number that is greater or equal than 2 is still 2. So the answer for the first query is [2,2].
- The largest number that is smaller or equal than 5 in the tree is 4, and the smallest number that is greater or equal than 5 is 6. So the answer for the second query is [4,6].
- The largest number that is smaller or equal than 16 in the tree is 15, and the smallest number that is greater or equal than 16 does not exist. So the answer for the third query is [15,-1].
```

**Example 2:**

```
Input: root = [4,null,9], queries = [3]
Output: [[-1,4]]
Explanation: The largest number that is smaller or equal to 3 in the tree does not exist, and the smallest number that is greater or equal to 3 is 4. So the answer for the query is [-1,4].
```

**Constraints**

- The number of nodes in the tree is in the range [2, 105].
- 1 <= Node.val <= 106
- n == queries.length
- 1 <= n <= 105
- 1 <= queries[i] <= 106

---

## 题目（中文翻译）

给定一棵二叉搜索树（Binary Search Tree）的根节点 `root` 和一个大小为 `n`、由正整数构成的数组 `queries`（查询）。  
请找出一个大小为 `n` 的二维数组 `answer`（答案），其中 `answer[i] = [mini, maxi]`：

- `mini` 为树中 **小于或等于** `queries[i]` 的最大节点值；如果不存在则记为 `-1`。  
- `maxi` 为树中 **大于或等于** `queries[i]` 的最小节点值；如果不存在则记为 `-1`。

返回数组 `answer`。

---

### 示例

**示例 1**

```
Input: root = [6,2,13,1,4,9,15,null,null,null,null,null,null,14], queries = [2,5,16]
Output: [[2,2],[4,6],[15,-1]]
```

**Explanation**  
我们按以下方式回答每个查询：

- 对于查询 `2`，树中小于或等于 `2` 的最大值是 `2`，大于或等于 `2` 的最小值也是 `2`，因此答案为 `[2,2]`。  
- 对于查询 `5`，树中小于或等于 `5` 的最大值是 `4`，大于或等于 `5` 的最小值是 `6`，因此答案为 `[4,6]`。  
- 对于查询 `16`，树中小于或等于 `16` 的最大值是 `15`，但不存在大于或等于 `16` 的节点，所以答案为 `[15,-1]`。

---

**示例 2**

```
Input: root = [4,null,9], queries = [3]
Output: [[-1,4]]
```

**Explanation**  
查询 `3` 在树中没有小于或等于的节点（记为 `-1`），大于或等于 `3` 的最小节点值为 `4`，因此答案为 `[-1,4]`。

---

### 约束条件

- 树中节点的数量在区间 `[2, 10^5]` 内。  
- `1 <= Node.val <= 10^6`  
- `n == queries.length`  
- `1 <= n <= 10^5`  
- `1 <= queries[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个查询单独在树上走一遍**，在遍历的过程中维护两个变量：

* `pre` – 当前遍历到的、且 **≤ query** 的最大值  
* `suc` – 当前遍历到的、且 **≥ query** 的最小值  

遍历可以用 **深度优先搜索**（递归或栈）实现。  
把树想象成一座迷宫，查询就是让我们在这座迷宫里寻找两个特定的房间：  
- “不超过查询值的最大房间”（前驱）  
- “不低于查询值的最小房间”（后继）  

每走到一个节点，就把它的值和查询值比较，决定是否更新 `pre` 或 `suc`。遍历完所有节点后，`pre`、`suc` 就是答案。如果遍历过程中根本没有满足条件的节点，就保持为 `-1`。

> **为什么这个方法一定正确？**  
> 因为我们检查了**所有**节点，凡是满足条件的节点都会被拿来比较，最终留下的就是最大（或最小）的那个。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def closestNodes(root, queries):
    """
    暴力解：对每个 query 都遍历整棵树
    """
    # ---------- 辅助函数：DFS 遍历 ----------
    def dfs(node, q, pre_suc):
        if not node:
            return
        # 更新前驱（pre）——比 q 小且最大的
        if node.val <= q and node.val > pre_suc[0]:
            pre_suc[0] = node.val
        # 更新后继（suc）——比 q 大且最小的
        if node.val >= q and node.val < pre_suc[1]:
            pre_suc[1] = node.val
        # 继续遍历左、右子树
        dfs(node.left, q, pre_suc)
        dfs(node.right, q, pre_suc)

    ans = []
    for q in queries:
        # 初始值设为 -1 表示「不存在」
        pre_suc = [-1, -1]          # pre_suc[0] -> 前驱, pre_suc[1] -> 后继
        dfs(root, q, pre_suc)
        ans.append(pre_suc)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - `m` = 查询数量，`n` = 树的节点数。每个查询都要遍历 `n` 个节点，等价于 “每次都把整棵树翻一遍”。  
  - 大白话：如果树有 10 万个节点，查询有 10 万个，那最坏情况下要跑 **10 万 × 10 万 = 1 亿元**次比较，显然太慢了。

- **空间复杂度**：`O(h)`（递归栈）  
  - `h` 为树的高度，最坏是 `O(n)`（链状树），平均是 `O(log n)`（平衡树）。除此之外只用了常数级的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每个查询都要把整棵树遍历一遍**。  
我们可以把 **“树的结构”** 抽离出来，先把所有节点的值按照从小到大的顺序保存下来。这样，后面的查询就只需要在 **已经排好序的数组** 中找前驱和后继，时间就能降到对数级。

**关键两步**：

1. **中序遍历**（In‑order Traversal）把 BST 转成有序数组  
   - 对二叉搜索树来说，中序遍历的顺序恰好是从小到大。把它想成“把树里的所有数字倒进一个排好序的抽屉”。  
   - 复杂度是 `O(n)`，只需要一次遍历。

2. **二分查找**（Binary Search）在有序数组里定位前驱/后继  
   - Python 标准库的 `bisect` 提供了 `bisect_left`（找第一个 **≥ x** 的位置）和 `bisect_right`（找第一个 **> x** 的位置）。  
   - 对于查询值 `q`：  
     * `idx = bisect_left(arr, q)` → `arr[idx]` 是 **≥ q** 的最小值（后继），如果 `idx == len(arr)` 则不存在。  
     * `pre = arr[idx-1]`（前提是 `idx > 0`） → 最大的 **≤ q**（前驱），如果 `idx == 0` 则不存在。  
   - 每次查询只需要 `O(log n)` 次比较。

> **为什么二分查找一定能找到答案？**  
> 因为数组已经是严格递增的序列，二分查找利用“左边全小、右边全大”的特性快速定位阈值。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def closestNodes(root: TreeNode, queries: List[int]) -> List[List[int]]:
    """
    最优解：先把 BST 中的值取出来排好序，再对每个 query 用二分查找
    """

    # ---------- 第一步：中序遍历得到有序数组 ----------
    inorder = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)          # 先左
        inorder.append(node.val)  # 再根
        dfs(node.right)         # 最后右
    dfs(root)                    # O(n)

    # ---------- 第二步：对每个 query 做二分 ----------
    ans = []
    n = len(inorder)
    for q in queries:
        # idx = 第一个 >= q 的位置
        idx = bisect_left(inorder, q)

        # 计算后继（>= q）
        suc = inorder[idx] if idx < n else -1

        # 计算前驱（<= q）
        pre = inorder[idx - 1] if idx > 0 else -1

        ans.append([pre, suc])
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n + m log n)`  
  - `n`：树的节点数（一次中序遍历）  
  - `m`：查询数量（每个查询一次二分）  
  - 对比暴力的 `O(m·n)`，我们把 **每个查询的时间从线性降到对数**，在数据量大时提升非常明显。

- **空间复杂度**：`O(n)`  
  - 需要额外存储排好序的数组 `inorder`，大小等于树的节点数。递归栈同样是 `O(h)`，但已被 `O(n)` 所覆盖。

---

## 心得

- **核心技巧**：把二叉搜索树的中序遍历结果视作“有序数组”，随后利用二分查找快速定位前驱/后继。  
- **适用的题型**  
  1. “在 BST 中查找某个值的前驱/后继”  
  2. “把树转成有序列表后做区间查询”  
  3. “在有序集合上求上界/下界”（例如 LeetCode 2409 – 统计兼具前缀和后缀的数组等）  
- **一句话总结解题钥匙**：**先把树“排好序”，再用二分“快速定位”。**

---

## 反思

- **第一反应**：直接遍历树，边走边记录满足条件的最大/最小值。  
- **最容易踩的坑**  
  1. **边界条件**：查询值小于树中最小节点或大于最大节点时，需要返回 `-1`。  
  2. **递归深度**：极端不平衡的 BST 可能导致递归栈过深，生产环境可以改写为显式栈或使用迭代中序遍历。  
  3. **重复值**：题目保证节点值唯一（BST 的常规假设），若出现重复，需要在比较时保持 `≤`、`≥` 的一致性。  
- **下次遇到同类题的第一步**：**思考是否能把树或其它结构“线性化”成有序序列**，因为有序序列往往能借助二分、前缀和等成熟算法把复杂度压到 `O(log n)`。