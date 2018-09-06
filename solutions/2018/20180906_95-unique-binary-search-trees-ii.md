# #95. 不同的二叉搜索树 II / Unique Binary Search Trees II

> 难度：中等 · 标签：Dynamic Programming、Backtracking、Tree、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/unique-binary-search-trees-ii/)

---

## 题目（英文原版）

**Description**

Given an integer n, return all the structurally unique BST's (binary search trees), which has exactly n nodes of unique values from 1 to n. Return the answer in any order.

**Examples**

**Example 1:**

```
Input: n = 3
Output: [[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]
```

**Example 2:**

```
Input: n = 1
Output: [[1]]
```

**Constraints**

- 1 <= n <= 8

---

## 题目（中文翻译）

给定一个整数 `n`，返回所有结构上唯一的二叉搜索树（BST），这些树恰好包含 `n` 个取值为 `1` 到 `n` 的不同节点。答案可以以任意顺序返回。

**示例 1**  
**输入:** `n = 3`  
**输出:** `[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]`  
**解释:** 当 `n = 3` 时，能够形成的不同 BST 如上所示，共有 5 种。

**示例 2**  
**输入:** `n = 1`  
**输出:** `[[1]]`  
**解释:** 只有一种可能的树，即仅包含根节点 `1` 的 BST。

**约束条件**  
- `1 <= n <= 8`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把所有可能的节点排列**（即 1~n 的全排列）都列出来，然后把每一种排列依次 **插入** 到一棵二叉搜索树（BST）中。  

- **全排列**：把 1~n 的数字按不同顺序排成一列。可以把它想象成“把一本词典的所有单词重新排顺序”。  
- **插入 BST**：从根节点开始，遇到比当前节点小的数就往左走，大的就往右走，直到找到空位插进去。这个过程就像在一棵“有序的树”里找合适的树枝安放新果子。  

如果把 **树的结构** 看作一种“语言”，那么不同的插入顺序会产生不同的语言表达，也就是不同的 BST。只要把所有排列都走一遍，就一定能得到 **所有** 结构唯一的 BST。  

**为什么正确？**  
- BST 的定义决定了：只要插入顺序不同，最终的树结构就可能不同。  
- 由于我们枚举了 **所有** 排列，必然不会漏掉任何一种合法的结构。  

**时间/空间分析（大白话）**  
- 全排列的数量是 `n!`（n 的阶乘），比如 n=3 时有 6 种，n=4 时有 24 种，随 n 增大会“炸裂”。  
- 对每一种排列，我们要把 n 个数逐个插入 BST，插入一次最坏要走到树的最底层，最多 O(n) 步。  
- 因此总体时间复杂度是 **O(n! × n)**，也就是“阶乘级别乘以线性”。这在 n=8 时已经是 40320 × 8 ≈ 3·10⁵ 次操作，仍可接受，但空间上我们要保存所有生成的树，树的节点总数也是 O(n! × n)。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

from itertools import permutations
import copy

def insert_into_bst(root: TreeNode, val: int) -> TreeNode:
    """把 val 按 BST 规则插入到已有的树中，返回根节点"""
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root

def generate_trees_bruteforce(n: int):
    """暴力枚举所有排列并插入，得到所有唯一的 BST"""
    if n == 0:
        return []
    result = []
    for perm in permutations(range(1, n + 1)):   # 1~n 的全排列
        root = None
        for v in perm:                          # 按顺序插入
            root = insert_into_bst(root, v)
        # 为了后面不被修改，需要深拷贝整棵树
        result.append(copy.deepcopy(root))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n! × n)`  
  - `n!` 表示所有排列的数量，`n` 是每次插入的最坏步数。  
- **空间复杂度**：`O(n! × n)`  
  - 需要存储所有生成的树，每棵树最多有 `n` 个节点。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **大量重复的子结构**。比如在排列 `[1,2,3]` 与 `[1,3,2]` 中，根节点都是 1，左子树始终为空，而右子树只和 `{2,3}` 的排列有关。我们不必每次都重新构造这些相同的子树，只要把 **“以某个区间的数字可以形成的所有 BST”** 记下来，后面需要时直接取用即可。  

这正是**动态规划 + 递归（记忆化搜索）** 的思路：  

1. **定义子问题**  
   `generate(l, r)` 表示“用区间 `[l, r]`（包含两端）内的所有整数，能够组成的所有唯一 BST”。  

2. **递归划分**  
   - 任选 `i`（`l ≤ i ≤ r`）作为根节点。  
   - 左子树只能由 `[l, i-1]` 的数构成，右子树只能由 `[i+1, r]` 的数构成。  
   - 把左子树的所有可能（记作 `left_trees`）和右子树的所有可能（记作 `right_trees`）两两组合，拼成完整的树。  

3. **边界**  
   - 当 `l > r` 时，区间为空，只有一种“空树”，用 `None` 表示。  
   - 当 `l == r` 时，只有一种树：根节点为唯一的 `l`，左右子树均为空。  

4. **记忆化**  
   - 同一个区间 `[l, r]` 会被多次求值（比如 `[2,3]` 在根为 1、2、3 时都会出现），我们把已经算好的结果存进字典 `memo[(l,r)]`，以后直接返回，避免重复计算。  

5. **最终答案**  
   - 调用 `generate(1, n)`，返回的就是所有使用 1~n 的唯一 BST 列表。  

**核心数据结构解释**  
- **字典（哈希表）**：像一本“查词典”，把区间 `(l,r)` 当作“单词”，对应的所有树列表当作“页码”。查找 `memo[(l,r)]` 就是直接在词典里找对应的解释，时间是 O(1)。  
- **递归**：把大问题拆成小问题，就像把一块大披萨切成更小的块，一块块吃。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def generateTrees(n: int):
    """返回所有唯一 BST（使用 1~n）"""
    if n == 0:
        return []

    from functools import lru_cache

    @lru_cache(maxsize=None)          # 自动记忆化，key 为 (l,r) 元组
    def generate(l: int, r: int):
        """返回区间 [l, r] 所有可能的 BST 根节点列表"""
        trees = []
        if l > r:                      # 空区间 → 只可能是 None
            return [None]

        # 任选 i 作为根
        for i in range(l, r + 1):
            left_subtrees = generate(l, i - 1)   # 所有左子树
            right_subtrees = generate(i + 1, r)  # 所有右子树

            # 把左、右子树两两配对，生成完整树
            for left in left_subtrees:
                for right in right_subtrees:
                    root = TreeNode(i)          # 新根节点
                    root.left = left
                    root.right = right
                    trees.append(root)          # 加入结果列表
        return trees

    return generate(1, n)
```

#### 复杂度  

- **时间复杂度**：`O(C_n)`（Catalan 数），约等于 `O(4^n / n^{3/2})`。  
  - 这里的 `C_n` 是第 n 个 Catalan 数，恰好等于不同 BST 的数量。我们必须把每一种树都生成一次，无法更快。相比暴力的 `n!`，Catalan 数增长要慢得多（例如 n=8 时 C₈=1430，而 8! = 40320）。  
- **空间复杂度**：`O(C_n)` 用于保存所有树的引用 + 递归栈 `O(n)`。  
  - 每棵树占用 `O(n)` 的节点空间，总体仍是 `O(C_n × n)`，但因为 `C_n` 远小于 `n!`，实际使用的内存大幅下降。  

---  

## 心得  

- **核心技巧**：**区间划分 + 记忆化递归**（即“动态规划的递归写法”），把“根节点的选择”抽象成子问题，避免重复构造相同子树。  
- **适用的题型**  
  1. **Unique Binary Search Trees**（LeetCode 96）——只要求返回计数，思路完全相同，只是不需要实际生成树。  
  2. **Different Ways to Add Parentheses**（LeetCode 241）——把表达式拆成子区间，递归组合结果。  
  3. **Palindrome Partitioning**（LeetCode 131）——对字符串区间进行划分，递归枚举所有合法分割。  
- **一句话总结解题钥匙**：  
  “把大区间的所有可能拆成根 + 左子区间 + 右子区间的组合，并用哈希表记住已经算好的区间。”  

---  

## 反思  

- **拿到题目第一反应**：先想“枚举所有排列然后插树”，因为这一步最符合直觉的“把所有可能都试一次”。  
- **最容易踩的坑**  
  - **空子树的处理**：区间为空时必须返回 `[None]`（而不是空列表），否则左/右子树配对会出错。  
  - **重复子结构**：不使用记忆化会导致指数级的重复计算，导致超时。  
  - **深拷贝**：在暴力解里若直接把同一个节点对象加入结果列表，后面的修改会影响之前的树，需要 `deepcopy`。  
- **下次遇到同类题**：第一步先思考“能否把问题划分为左/右子区间的组合”，若答案是肯定的，就立刻写出递归子问题并加入记忆化。这样既能保证正确性，又能把时间控制在合理范围。