# #1339. 二叉树分割后最大乘积 / Maximum Product of Splitted Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-product-of-splitted-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, split the binary tree into two subtrees by removing one edge such that the product of the sums of the subtrees is maximized.
Return the maximum product of the sums of the two subtrees. Since the answer may be too large, return it modulo 109 + 7.
Note that you need to maximize the answer before taking the mod and not after taking it.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5,6]
Output: 110
Explanation: Remove the red edge and get 2 binary trees with sum 11 and 10. Their product is 110 (11*10)
```

**Example 2:**

```
Input: root = [1,null,2,3,4,null,null,5,6]
Output: 90
Explanation: Remove the red edge and get 2 binary trees with sum 15 and 6.Their product is 90 (15*6)
```

**Constraints**

- The number of nodes in the tree is in the range [2, 5 * 104].
- 1 <= Node.val <= 104

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，通过删除一条边（edge）将这棵二叉树分割成两个子树（subtrees），使得两个子树的节点值之和（sum）的乘积（product）达到最大。返回这两个子树和的乘积的最大值。由于答案可能非常大，返回结果对 `10^9 + 7` 取模后的值。**注意**：需要在取模之前先求出最大乘积，再对结果取模，而不是在取模后再求最大值。

**示例 1**  
**输入**: `root = [1,2,3,4,5,6]`  
**输出**: `110`  
**解释**: 删除红色的那条边后得到两棵二叉树，分别的节点和值为 `11` 和 `10`。它们的乘积为 `110` (`11 * 10`)。

**示例 2**  
**输入**: `root = [1,null,2,3,4,null,null,5,6]`  
**输出**: `90`  
**解释**: 删除红色的那条边后得到两棵二叉树，分别的节点和值为 `15` 和 `6`。它们的乘积为 `90` (`15 * 6`)。

**约束条件**  
- 树中节点的数量在区间 `[2, 5 * 10^4]` 内。  
- `1 <= Node.val <= 10^4`   (其中 `Node.val` 为节点的值)。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一条边都剪掉一次**，然后分别算出被割开的两棵子树的节点值之和，求它们的乘积，取最大值。  

- **数据结构**：  
  - 二叉树本身用 `TreeNode` 表示。  
  - 为了方便“剪掉一条边”，我们可以在遍历时记录每条边对应的**子树根节点**。这有点像把树的每一根枝条都标记出来，剪掉哪根枝条就相当于把它下面的整棵子树单独拿出来。  
  - 计算子树和时可以用递归（深度优先搜索），类似“查字典”。递归的返回值就是当前节点所在子树的**总和**，就像在字典里查到某个词对应的解释长度。

- **正确性**：  
  对每一条边，剪掉后必然得到 **恰好两棵** 子树，且这两棵子树的节点集合是原树的一个划分。遍历所有边，就一定会遍历到**所有可能的划分**，所以取最大乘积一定是答案。

- **时间/空间复杂度**：  
  - 对每条边（大约 `n‑1` 条）我们都要**重新遍历整棵树**来算子树和，遍历一次是 `O(n)`。于是总时间是 `O(n²)`，这在 `n ≤ 5·10⁴` 时会非常慢。  
  - 递归调用栈的深度最多等于树的高度，最坏是 `O(n)`（链状树），但我们只保存常数级的额外变量，空间是 `O(n)`（递归栈）。

> **大白话解释**：  
> `O(n²)` 可以想象成“有 `n` 个人，每个人都要检查 `n` 次”，所以如果 `n` 是几万，检查次数就会是几千万，电脑会很吃力。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def subtree_sum(root: TreeNode) -> int:
    """返回以 root 为根的子树所有节点值之和"""
    if not root:
        return 0
    # 递归左、右子树的和，再加上当前节点的值
    return root.val + subtree_sum(root.left) + subtree_sum(root.right)


def maxProduct_bruteforce(root: TreeNode) -> int:
    MOD = 10**9 + 7
    total = subtree_sum(root)               # 整棵树的总和

    max_prod = 0

    def dfs(node: TreeNode) -> int:
        """后序遍历，顺便尝试把以 node 为根的子树剪掉"""
        nonlocal max_prod
        if not node:
            return 0
        left = dfs(node.left)   # 左子树和
        right = dfs(node.right) # 右子树和

        cur = node.val + left + right   # 当前子树的和

        # 这里把 “剪掉 node 与父节点的那条边” 视为一种可能
        # 剩下的另一棵树的和就是 total - cur
        prod = cur * (total - cur)
        if prod > max_prod:
            max_prod = prod

        return cur   # 返回给父节点继续累计

    dfs(root)
    return max_prod % MOD
```

> **代码要点注释**  
> - `subtree_sum` 负责一次完整遍历得到整棵树的总和。  
> - `dfs` 采用**后序遍历**（先算左右子树，再算当前节点），这样每次返回的 `cur` 就是**以当前节点为根的子树和**，正好可以当作“剪掉这条边后得到的子树”。  
> - `total - cur` 正是**另一棵子树的和**，两者乘积即为该割法的得分。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：对每个节点都要重新遍历整棵树一次（`n`），共 `n` 次，故是 `n × n`。
- **空间复杂度**：`O(n)`  
  - 解释：递归栈最深可能等于树的高度，最坏情况下是 `n`，其余只用了常数级变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于重复遍历树来求子树和**。如果我们在一次遍历中就把**所有子树的和**全部记下来，后面再计算乘积就可以 **O(1)** 完成。

**关键两步**：

1. **一次 DFS（深度优先搜索）**，把每个节点对应的子树和算出来，并存进一个列表 `sums`。  
   - 这一步类似“把每棵小树的体重都称一遍”。  
   - 同时我们还能得到整棵树的总和 `total`（列表里最后一个元素就是根节点的子树和）。

2. 再遍历 `sums`（不包括根节点本身），对每个子树和 `x` 计算  
   `product = x * (total - x)`，取最大值。  
   - 这里的 `total - x` 正是“剪掉这条边后另一边的体重”。  

**为什么只遍历一次就够了？**  
因为二叉树的每条边唯一对应一个 **子树根节点**（子树在父节点下面），剪掉这条边后得到的两棵树的和正好是 **该子树的和** 与 **剩余部分的和**。所以只要知道所有子树的和，就能枚举所有割法。

**核心算法/数据结构**：

- **后序遍历（后根遍历）**：先算左、右子树的和，再算当前节点的和，保证子树和已经准备好。  
- **列表（Array）**：用来收集每个子树的和，类似“记事本”。  
- **取模**：答案可能非常大，需要在最后对 `10⁹+7` 取模。

**类比**：  
想象有一根树干，上面挂满了果子（节点值）。我们想把树干剪成两段，使得两段果子的总重量乘积最大。我们先把每根枝条（子树）上的果子重量记下来，然后遍历这些重量，看看如果把这根枝条剪掉后，两段的重量乘积是多少，挑出最大的那一次。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxProduct(root: TreeNode) -> int:
    MOD = 10**9 + 7
    subtree_sums = []          # 用来存放每个子树的和

    def dfs(node: TreeNode) -> int:
        """后序遍历，返回以 node 为根的子树和，并把它加入列表"""
        if not node:
            return 0
        left_sum = dfs(node.left)
        right_sum = dfs(node.right)
        cur_sum = node.val + left_sum + right_sum
        subtree_sums.append(cur_sum)   # 记录当前子树的和
        return cur_sum

    total = dfs(root)          # 第一次遍历，顺便得到整棵树的总和
    max_prod = 0

    # 遍历所有子树和（除去根节点本身，因为根节点没有“父边”可以剪）
    for s in subtree_sums[:-1]:   # 最后一个元素就是 total，跳过它
        product = s * (total - s)   # 计算剪掉这条边后的乘积
        if product > max_prod:
            max_prod = product

    return max_prod % MOD
```

> **代码要点注释**  
> - `subtree_sums.append(cur_sum)` 把每个子树的“体重”记下来。  
> - `subtree_sums[:-1]` 通过切片去掉最后一个元素（根节点的子树和），因为根节点没有父亲，不能“剪掉根与父”的边。  
> - `max_prod % MOD` 是在**所有乘积都算完以后**才取模，确保先比较真实的大小。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只需要一次完整的 DFS（`O(n)`）以及一次对 `subtree_sums` 的线性遍历（也是 `O(n)`），两者相加仍是线性。  
  - 与暴力解相比，从 `n²` 降到 `n`，提升非常明显。

- **空间复杂度**：`O(n)`  
  - 需要额外的列表保存每个子树的和，大小正好是节点数 `n`。递归栈同样最多 `O(n)`（链状树），所以总体仍是线性。

---

## 心得

- **核心技巧**：一次 DFS 收集所有子树和，然后在这些和上做“一次遍历”求最大乘积。  
- **适用的题型**：  
  1. **二叉树分割最大乘积**（本题）。  
  2. **删除一条边后使两棵树的差的绝对值最小**（同样可以利用子树和）。  
  3. **求二叉树中两节点路径和的最大乘积**（先算前缀和/后缀和再枚举）。  
- **一句话总结**：*把“每条可能的剪法”映射成“子树的和”，一次遍历搞定全部信息*。

---

## 反思

- **第一反应**：直接想把每条边都剪一次，分别算两棵树的和——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记 **先算整棵树的总和**，导致在计算 `total - subtree_sum` 时出错。  
  - 在取最大乘积后才取模，而不是每次乘积都取模（题目要求先比较原始值）。  
  - 忽视根节点没有父边，导致在遍历 `subtree_sums` 时把根的和也当作可剪的情况，得到错误答案。  
- **下次类似题的第一步**：先思考 **“能否一次遍历把所有需要的局部信息（子树和、子树大小等）都收集起来？”**，如果能，就往“一次遍历 + 线性后处理”方向走。