# #508. 出现次数最多的子树和 / Most Frequent Subtree Sum

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/most-frequent-subtree-sum/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the most frequent subtree sum. If there is a tie, return all the values with the highest frequency in any order.
The subtree sum of a node is defined as the sum of all the node values formed by the subtree rooted at that node (including the node itself).

**Examples**

**Example 1:**

```
Input: root = [5,2,-3]
Output: [2,-3,4]
```

**Example 2:**

```
Input: root = [5,2,-5]
Output: [2]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -105 <= Node.val <= 105

---

## 题目（中文翻译）

给定二叉树（binary tree）的根节点（root），返回出现次数最多的子树和（subtree sum）。如果出现次数出现平局，返回所有出现频率最高的子树和值，顺序任意。

子树和（subtree sum）定义为以某个节点为根的子树中所有节点值的总和（包括该节点本身）。

**示例 1：**
``` 
Input: root = [5,2,-3]
Output: [2,-3,4]
```

**示例 2：**
``` 
Input: root = [5,2,-5]
Output: [2]
```

**约束条件：**
- 树中节点的数量在 [1, 10^4] 范围内。
- -10^5 <= 节点值（Node.val） <= 10^5

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「对每一个节点，都把它所在的子树全部遍历一遍，算出子树的节点值之和」。  
可以把二叉树想象成一棵家谱树：每个人（节点）都有自己的后代（左子树、右子树）。  
如果我们要知道某个人的「家族财富」——即他和所有后代的价值之和，只需要把这棵子树的每个人的价值加起来。

实现步骤：

1. **遍历所有节点**（先序/中序/后序都行），把每个节点记下来。  
2. 对于遍历到的每个节点，**再次做一次深度优先搜索**，把它的左子树、右子树以及它本身的 `val` 累加，得到「子树和」。  
3. 用一个哈希表（在 Python 中就是 `dict`）统计每个子树和出现的次数。哈希表可以类比为一本「词典」：`key` 是子树和，`value` 是出现的次数。  
4. 最后遍历哈希表，找出出现次数最多的那些 `key`，即为答案。

> **为什么正确？**  
> 每个节点的子树和一定会在第 2 步被完整算出来；而哈希表把所有出现的次数记录下来，取最大即可。

**时间/空间复杂度分析（大白话版）**

- 对每个节点我们都要**再遍历一次它的整棵子树**。如果树有 `n` 个节点，最坏情况下（比如链式结构）第一个节点要遍历 `n` 次，第二个节点要遍历 `n‑1` 次……于是总遍历次数约为 `n + (n‑1) + … + 1 = n·(n+1)/2`，这就是 **O(n²)**。  
  - *O(n²) 可以想象成“做 n 次每次要遍历 n 个东西”，比起一次遍历全树（O(n)）要慢很多。*

- 哈希表里最多会出现 `n` 个不同的子树和，所以 **空间是 O(n)**。  
  - 递归栈的深度最坏也会是 `n`（链式树），所以整体空间仍是 O(n)。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


def most_frequent_subtree_sum_bruteforce(root: TreeNode):
    """暴力解：对每个节点都重新遍历它的子树，统计子树和的出现次数"""
    if not root:
        return []

    # 1. 收集所有节点（这里用前序遍历）
    all_nodes = []

    def collect(node):
        if not node:
            return
        all_nodes.append(node)   # 把当前节点记下来
        collect(node.left)
        collect(node.right)

    collect(root)

    # 2. 对每个节点计算子树和（每次都重新遍历一次子树）
    def subtree_sum(node):
        if not node:
            return 0
        # 左右子树的和 + 当前节点的值
        return subtree_sum(node.left) + subtree_sum(node.right) + node.val

    freq = {}                     # 哈希表：key=子树和，value=出现次数
    for node in all_nodes:
        s = subtree_sum(node)    # 重新遍历子树得到和
        freq[s] = freq.get(s, 0) + 1

    # 3. 找出出现次数最多的子树和
    max_cnt = max(freq.values())
    return [s for s, cnt in freq.items() if cnt == max_cnt]
```

#### 复杂度

- **时间复杂度：O(n²)**  
  - 想象一下有 10,000 个节点，暴力解大约要做 100,000,000 次加法，明显太慢。

- **空间复杂度：O(n)**  
  - 需要存 `all_nodes`（最多 n 个）和 `freq`（最多 n 个不同的和），再加上递归栈最坏 O(n)。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 出在「每个节点都要重复遍历它的子树」这一步。  
实际上，**子树的和** 本身就可以在一次遍历中顺带算出来：如果我们已经知道左子树的和 `L`、右子树的和 `R`，那么当前节点的子树和就是 `L + R + node.val`。这正好符合 **后序遍历**（先算左子树、再算右子树、最后算根）的顺序。

**核心技巧**：一次 DFS（深度优先搜索）在**回溯**的过程中把每个节点的子树和算出来，并立即把它记进哈希表。这样每个节点只被访问一次，时间从 O(n²) 降到 **O(n)**。

下面把关键概念解释给初学者：

- **深度优先搜索（DFS）**：想象在森林里走路，每次尽可能往下走到叶子再返回，这就是「先往左、再往右、最后回到父节点」的遍历方式。  
- **后序遍历**：先把左边的树走完、再把右边的树走完，最后才处理当前节点。正好符合「先知道子树的和，再算父节点的和」的需求。  
- **哈希表**：就像查字典，`key` 是「子树和」这本「词」，`value` 是「这本词出现了多少次」的「页码」。查找、插入都是 O(1) 的快操作。

实现步骤：

1. 定义一个全局（或闭包）字典 `cnt`，用来统计每个子树和出现的次数。  
2. 编写递归函数 `dfs(node)`：  
   - 若 `node` 为 `None`，返回 0（空子树的和是 0）。  
   - 递归求左子树的和 `left = dfs(node.left)`。  
   - 递归求右子树的和 `right = dfs(node.right)`。  
   - 当前子树的和 `total = left + right + node.val`。  
   - 把 `total` 写入 `cnt`：`cnt[total] = cnt.get(total, 0) + 1`。  
   - 返回 `total` 给父节点使用。  
3. 调用 `dfs(root)` 完成一次遍历后，`cnt` 中已经记录了所有子树和以及它们的出现次数。  
4. 取出现次数最大的那些键，即为答案。

**为什么是最优的？**  
- 每个节点只访问一次，时间是 **O(n)**。  
- 只用了一个字典和递归栈，空间是 **O(n)**（字典最多 n 条记录，递归栈最坏深度 n）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def most_frequent_subtree_sum(root: TreeNode):
    """
    最优解：一次后序遍历统计所有子树和的出现次数
    返回出现次数最多的子树和（可能有多个）
    """
    if not root:
        return []

    freq = {}  # 哈希表：key=子树和，value=出现次数

    # ---------- 后序遍历的递归函数 ----------
    def dfs(node: TreeNode) -> int:
        """返回以 node 为根的子树的和，同时更新 freq"""
        if not node:
            return 0                     # 空子树的和为 0

        left_sum = dfs(node.left)        # 左子树的和
        right_sum = dfs(node.right)      # 右子树的和

        total = left_sum + right_sum + node.val   # 当前子树的和
        freq[total] = freq.get(total, 0) + 1      # 统计出现次数
        return total                    # 把子树和返回给父节点

    # 触发一次完整的后序遍历
    dfs(root)

    # 找出出现次数最高的子树和
    max_cnt = max(freq.values())                     # 最高出现次数
    return [s for s, c in freq.items() if c == max_cnt]
```

#### 复杂度

- **时间复杂度：O(n)**  
  - 每个节点只被访问一次，想象有 10,000 个节点，只需要 10,000 次加法和字典操作，速度快很多。

- **空间复杂度：O(n)**  
  - `freq` 最多保存 `n` 条记录；递归栈最坏深度为树的高度，最坏情况（链式树）是 `n`。整体仍是线性空间。

---

## 心得

- **核心技巧**：一次后序遍历（DFS）即可在回溯时算出每个节点的子树和，并利用哈希表统计频次。  
- **适用场景**：  
  1. 需要**“自底向上”**聚合信息的树形问题（如「二叉树的最大路径和」）。  
  2. 需要统计**子结构**出现次数的题目（如「子树中出现的相同值」）。  
  3. 需要在遍历过程中**即时更新全局信息**的情形（如「求二叉树中所有路径和」）。  
- **一句话总结**：一次后序遍历 + 哈希表，即可把“每个子树的和”和“出现次数”同步算完，省去重复遍历的开销。

---

## 反思

- **拿到题目第一反应**：先想「遍历所有节点，分别求子树和」——这就是暴力思路。  
- **最容易踩的坑**：  
  - **递归返回值忘记累加**：后序遍历必须把左、右子树的和返回并相加，否则只能得到单节点的值。  
  - **空树的处理**：`None` 节点的子树和应为 0，防止 `None` 报错。  
  - **出现次数相同的多解**：一定要遍历哈希表把所有出现次数等于最大值的键都收集，而不是只返回一个。  
- **下次遇到同类题的第一步**：问自己「是否可以在一次遍历中把子结构的信息（和、大小、状态）直接算出来并记录？」如果答案是「可以」，那就立刻写后序（或相应的）DFS；如果不行，再考虑是否需要额外的 DP、单调栈等技巧。