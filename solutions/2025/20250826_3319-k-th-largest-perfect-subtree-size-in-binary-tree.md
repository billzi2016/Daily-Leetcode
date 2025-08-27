# #3319. 二叉树中第 k 大完美子树的大小 / K-th Largest Perfect Subtree Size in Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Sorting、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/k-th-largest-perfect-subtree-size-in-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree and an integer k.
Return an integer denoting the size of the kth largest perfect binary subtree, or -1 if it doesn't exist.
A perfect binary tree is a tree where all leaves are on the same level, and every parent has two children.

**Examples**

**Example 1:**

```
Input: root = [5,3,6,5,2,5,7,1,8,null,null,6,8], k = 2
Output: 3
Explanation:

The roots of the perfect binary subtrees are highlighted in black. Their sizes, in non-increasing order are [3, 3, 1, 1, 1, 1, 1, 1] . The 2 nd largest size is 3.
```

**Example 2:**

```
Input: root = [1,2,3,4,5,6,7], k = 1
Output: 7
Explanation:

The sizes of the perfect binary subtrees in non-increasing order are [7, 3, 3, 1, 1, 1, 1] . The size of the largest perfect binary subtree is 7.
```

**Example 3:**

```
Input: root = [1,2,3,null,4], k = 3
Output: -1
Explanation:

The sizes of the perfect binary subtrees in non-increasing order are [1, 1] . There are fewer than 3 perfect binary subtrees.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 2000].
- 1 <= Node.val <= 2000
- 1 <= k <= 1024

---

## 题目（中文翻译）

**题目描述**

给定一棵二叉树（binary tree）的根节点 `root` 和一个整数 `k`。  
返回第 `k` 大完美二叉子树（perfect binary subtree）的节点数（size），如果不存在则返回 `-1`。  

**完美二叉树（perfect binary tree）** 的定义为：所有叶子节点（leaf）位于同一层，且每个内部节点（parent）恰好拥有两个子节点。

---

**示例**

**示例 1**

``` 
Input: root = [5,3,6,5,2,5,7,1,8,null,null,6,8], k = 2
Output: 3
Explanation:
图中用黑色标记的节点即为完美二叉子树的根。它们的大小按非递增顺序为 [3, 3, 1, 1, 1, 1, 1, 1]，第 2 大的大小是 3。
```

**示例 2**

``` 
Input: root = [1,2,3,4,5,6,7], k = 1
Output: 7
Explanation:
完美二叉子树的大小按非递增顺序为 [7, 3, 3, 1, 1, 1, 1]，最大的完美二叉子树大小为 7。
```

**示例 3**

``` 
Input: root = [1,2,3,null,4], k = 3
Output: -1
Explanation:
完美二叉子树的大小按非递增顺序为 [1, 1]，数量不足 3 个，因此返回 -1。
```

---

**约束条件**

- 树中节点数在 `[1, 2000]` 范围内。
- `1 <= Node.val <= 2000`
- `1 <= k <= 1024`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把每一个节点当作子树根」，然后**单独检查**这棵子树是否是“完美二叉树”。  
检查的方法可以用递归：

1. 从根节点往下遍历，得到这棵子树的所有节点。  
2. 判断这棵子树的叶子是否在同一层、每个内部节点是否都有左右孩子。  
3. 若满足条件，就记下这棵子树的节点数量（即大小）。

把所有满足条件的子树大小收集起来，排序后取第 k 大的即可。

> **类比**：  
> 哈希表（字典）就像一本**词典**，单词是 key，页码是 value。这里我们用 **list** 来存放所有子树的大小，像是把所有“词的出现次数”记在一本小本子里，最后再把本子按大小排序。

**为什么正确**  
每个节点都被当作根来检查一次，所有可能的子树都会被枚举。只要检查的过程完全符合“完美二叉树”的定义，收集到的大小一定是所有合法子树的大小集合，排序后第 k 大的答案自然正确。

**复杂度分析（大白话）**  

- 对每个节点（最多 N 个），我们都会重新遍历它的整棵子树来判断是否完美。最坏情况下根节点的子树有 N 个节点，第二层的子树约 N/2 个，依此类推，整体时间大约是 **N + (N‑1) + (N‑2) + … + 1 ≈ N²**，即 **O(N²)**。  
  - 用大白话说，就是“把每本书都从头读一遍”，而书的总页数是 N，读 N 遍自然是 N² 次操作。
- 我们只需要一个列表来存放子树大小，最多 N 个元素，空间是 **O(N)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_perfect(root):
    """
    检查以 root 为根的子树是否是完美二叉树
    返回 (bool, height, size)
    """
    if not root:                      # 空树不算完美
        return False, 0, 0
    if not root.left and not root.right:   # 叶子节点：高度 1，大小 1，必然是完美的
        return True, 1, 1

    # 递归检查左右子树
    left_ok, left_h, left_sz = is_perfect(root.left)
    right_ok, right_h, right_sz = is_perfect(root.right)

    # 必须左右子树都完美且高度相同，才能让当前节点形成完美二叉树
    if left_ok and right_ok and left_h == right_h:
        return True, left_h + 1, left_sz + right_sz + 1
    return False, 0, 0                 # 不是完美子树


def collect_sizes(root, sizes):
    """
    把所有以某个节点为根的完美子树大小加入列表 sizes
    """
    if not root:
        return
    ok, _, sz = is_perfect(root)       # 为当前根检查一次
    if ok:
        sizes.append(sz)                # 记录大小
    # 继续向下遍历
    collect_sizes(root.left, sizes)
    collect_sizes(root.right, sizes)


def kthLargestPerfectSubtreeSize(root, k):
    sizes = []
    collect_sizes(root, sizes)          # 暴力收集所有完美子树大小
    sizes.sort(reverse=True)            # 大到小排序
    return sizes[k - 1] if k <= len(sizes) else -1
```

#### 复杂度

- **时间复杂度**：`O(N²)`  
  - 想象每个节点都要把它所在的那棵子树从头到尾检查一遍，像是把 N 本书每本都从头读到尾，总共要读 N² 页。
- **空间复杂度**：`O(N)`  
  - 只用了一个列表来存所有子树的大小，最多 N 个元素；递归栈深度最坏为 N （链状树），也是 O(N)。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于对同一棵子树会被检查多次：根节点检查整棵树，左子树的根又会重新检查左子树，…… 这导致 **重复劳动**。

要把重复的工作消除，只需要**一次遍历**就把每个节点的“完美子树信息”算出来，并顺手把大小记录下来。  
这正好可以用 **后序遍历（深度优先搜索）** 来实现：先处理左子树、右子树，再根据它们的结果决定当前节点的状态。

我们在遍历时为每个节点返回三个信息：

1. `is_perfect`：这棵子树是否是完美的。  
2. `height`：如果是完美的，它的层高是多少（叶子层高为 1）。  
3. `size`：如果是完美的，它的节点总数。

递推公式：

- 叶子节点：`is_perfect = True, height = 1, size = 1`（显然是完美的）。
- 非叶子节点：
  - 必须 **左右子树都存在**（否则不可能是完美二叉树）。
  - 必须 **左右子树都是完美的**，且 **高度相等**。  
    这两条同时满足时，当前节点的子树也是完美的，`height = left.height + 1`，`size = left.size + right.size + 1`。
  - 否则 `is_perfect = False`（高度、大小随意返回即可）。

在后序遍历的过程中，一旦发现 `is_perfect` 为 `True`，就把对应的 `size` 加入一个 **全局列表**。遍历结束后，列表里恰好装着所有完美子树的大小，随后排序取第 k 大即可。

> **类比**：  
> 想象你在检查一座建筑的结构安全。先检查最底层的每根柱子（叶子），确认它们都稳固；再往上检查每层楼板是否两边都有柱子且高度相同。只要一次检查完所有层，就不需要再回头重新检查已经确认的层了。

**复杂度**  
- 每个节点只被访问一次，所有信息在一次 DFS 中算完，**时间 O(N)**。  
- 额外保存所有完美子树的大小，需要最多 O(N) 空间；递归栈深度最坏 O(N)（链状树），总体仍是 **O(N)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def kthLargestPerfectSubtreeSize(root: TreeNode, k: int) -> int:
    perfect_sizes = []               # 用来收集所有完美子树的大小

    def dfs(node):
        """
        后序遍历返回 (is_perfect, height, size)
        同时把每个完美子树的 size 加入 perfect_sizes
        """
        if not node:                 # 空节点不计入
            return False, 0, 0

        # 先递归左、右子树
        left_perfect, left_h, left_sz = dfs(node.left)
        right_perfect, right_h, right_sz = dfs(node.right)

        # 判断当前节点的子树是否完美
        if node.left and node.right and left_perfect and right_perfect and left_h == right_h:
            cur_h = left_h + 1                     # 高度加一
            cur_sz = left_sz + right_sz + 1       # 节点数相加再加根节点
            perfect_sizes.append(cur_sz)          # 记录大小
            return True, cur_h, cur_sz
        else:
            # 只要不是完美子树，就直接返回 False，其他值随意
            return False, 0, 0

    dfs(root)                       # 从根节点开始一次遍历

    # 按大小降序排列
    perfect_sizes.sort(reverse=True)
    return perfect_sizes[k - 1] if k <= len(perfect_sizes) else -1
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  - 每个节点只访问一次，就像只把每本书读一遍，整个阅读过程只需要 **N** 页。
- **空间复杂度**：`O(N)`  
  - 需要一个列表保存所有完美子树的大小，最坏情况每个节点都是叶子，列表长度为 **N**；递归栈深度同样最多 **N**。

---

## 心得

- **核心技巧**：利用后序遍历一次性求出每棵子树是否为完美二叉树，并在遍历过程中收集答案。  
- **适用场景**（类似题目）：
  1. “统计二叉树中所有满二叉树（每个节点要么有两个子节点，要么没有）的大小”。  
  2. “求二叉树中所有高度相等的左右子树的根节点”。  
  3. “找出二叉树中所有满足某种递归结构（如 BST、平衡树）的子树”。  
- **一句话总结**：一次后序遍历即可把“子树是否完美”这件事从 **根到叶** 递推下来，避免重复检查。

---

## 反思

- **第一反应**：看到“完美二叉树”就想到“叶子在同一层、每个内部节点都有左右孩子”，于是尝试对每个节点单独检查——这就是暴力思路。  
- **最容易踩的坑**：
  - 忘记 **左右子树必须同时存在**（单侧子树的情况会导致误判）。  
  - 高度相等的判断必须在 **左右子树都是完美** 的前提下进行，否则会把不完整的子树误算进来。  
  - 边界条件：只有根节点或全是叶子时，`k` 可能大于可选子树数量，需要返回 `-1`。  
- **下次类似题**：先思考“能否用一次 DFS 把子树的状态（是否满足条件、对应属性）自底向上递推”，如果可以，就立刻写出递归返回值的设计，而不是去枚举每个根节点。这样往往能把时间从 **O(N²)** 降到 **O(N)**。