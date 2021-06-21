# #1373. 最大二叉搜索树和 / Maximum Sum BST in Binary Tree

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree root, return the maximum sum of all keys of any sub-tree which is also a Binary Search Tree (BST).
Assume a BST is defined as follows:

**Examples**

**Example 1:**

```
Input: root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]
Output: 20
Explanation: Maximum sum in a valid Binary search tree is obtained in root node with key equal to 3.
```

**Example 2:**

```
Input: root = [4,3,null,1,2]
Output: 2
Explanation: Maximum sum in a valid Binary search tree is obtained in a single root node with key equal to 2.
```

**Example 3:**

```
Input: root = [-4,-2,-5]
Output: 0
Explanation: All values are negatives. Return an empty BST.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 4 * 104].
- -4 * 104 <= Node.val <= 4 * 104

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，返回任意子树（subtree）中所有节点键值的最大和，且该子树必须是二叉搜索树（BST）。

假设二叉搜索树（BST）的定义如下：

（此处按题目原定义给出）

---

## 示例

### 示例 1
**输入**  
``` 
root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]
```  
**输出**  
```
20
```  
**解释**  
在根节点值为 `3` 的子树中形成了一个合法的二叉搜索树，其所有节点键值之和为最大值 `20`。

### 示例 2
**输入**  
``` 
root = [4,3,null,1,2]
```  
**输出**  
```
2
```  
**解释**  
最大和出现在仅包含键值为 `2` 的单节点子树中。

### 示例 3
**输入**  
``` 
root = [-4,-2,-5]
```  
**输出**  
```
0
```  
**解释**  
所有节点值均为负数，返回空的二叉搜索树（和为 `0`）。

---

## 约束条件
- 树中节点的数量在 `[1, 4 * 10^4]` 区间内。  
- `-4 * 10^4 <= Node.val <= 4 * 10^4`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每棵子树都检查一遍**，看它是不是二叉搜索树（BST），如果是就把它所有节点的值相加，记录下最大的和。  

- **子树的概念**：把一棵树的任意一个节点当作根，它往下的所有节点组成的树就是这个节点的子树。  
- **判断 BST**：我们可以用**递归**的方式遍历子树，收集子树中最小值、最大值以及是否满足 BST 的规则。  
  - 对于当前节点 `node`，左子树的所有值都必须 `< node.val`，右子树的所有值都必须 `> node.val`。  
- **遍历所有子树**：对每个节点都执行一次「判断 BST + 计算子树和」的过程，这样就能得到所有合法 BST 的和，取最大即可。  

> **为什么这个方法一定能得到答案？**  
> 因为我们把 **所有可能的子树** 都枚举了一遍，只要子树满足 BST 条件，就会被计算其和；所以最大和一定在我们枚举的集合里。

> **时间/空间复杂度大概是什么样的？**  
> - 对每个节点，我们都要遍历它的整个子树来判断是否是 BST，这相当于 **对每个节点都做一次 O(子树大小) 的遍历**。  
> - 最坏情况下（比如一条链状树），第 1 个节点要遍历 `n` 个节点，第 2 个节点遍历 `n-1`，……，所以总共的工作量大约是 `n + (n-1) + … + 1 = n·(n+1)/2`，即 **O(n²)**。  
> - 递归调用栈的深度最多是树的高度，最坏情况下是 `n`，所以空间复杂度是 **O(n)**（主要是栈空间）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxSumBST(root: TreeNode) -> int:
    """暴力解：枚举每棵子树，检查是否是 BST，记录最大和"""
    max_sum = 0                     # 记录全局最大和

    # --------- 辅助函数：判断 subtree 是否是 BST，并返回 (is_bst, sum, min_val, max_val) ----------
    def check(node):
        """
        返回一个四元组:
        - is_bst: 这棵子树是否满足 BST
        - total:   若是 BST，子树所有节点值的和；否则随意返回 0
        - min_v:   子树中最小的节点值（用于上层判断）
        - max_v:   子树中最大的节点值（用于上层判断）
        """
        if not node:
            # 空树自然是 BST，和为 0，最小值设为 +inf，最大值设为 -inf，方便比较
            return True, 0, float('inf'), float('-inf')

        left_is, left_sum, left_min, left_max = check(node.left)
        right_is, right_sum, right_min, right_max = check(node.right)

        # 判断当前节点的子树是否满足 BST 条件
        if (left_is and right_is and
                left_max < node.val < right_min):
            # 是 BST，计算整棵子树的和
            cur_sum = left_sum + right_sum + node.val
            nonlocal max_sum
            max_sum = max(max_sum, cur_sum)      # 更新全局最大和
            # 返回当前子树的最小、最大值，供父节点使用
            cur_min = min(left_min, node.val)
            cur_max = max(right_max, node.val)
            return True, cur_sum, cur_min, cur_max
        else:
            # 不是 BST，返回一个标记让上层不要再把它当作 BST 使用
            return False, 0, 0, 0

    check(root)
    return max_sum
```

> **代码要点说明**  
> - `float('inf')`、`float('-inf')` 就像字典里「查不到」的键，方便在比较时不受影响。  
> - `nonlocal max_sum` 让内部函数可以修改外层的 `max_sum` 变量。  
> - 当子树不是 BST 时，我们直接把 `is_bst` 标记设为 `False`，并把和设为 `0`，因为它不参与答案。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个节点都要遍历它的整个子树（最坏情况下是 `n + (n-1) + … + 1`）。  
  - 大白话：如果树有 10,000 个节点，最坏会做大约 10,000 × 10,001 / 2 ≈ 50 百万次比较，已经很慢了。  
- **空间复杂度**：`O(n)`  
  - 递归栈深度等于树的高度，最坏是整棵链，深度为 `n`。  
  - 只用了常数级的额外变量，除递归栈外几乎不占内存。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复遍历子树是瓶颈**。  
我们希望在一次深度优先遍历（后序遍历）中，**把每棵子树的信息一次性算好**，这样每个节点只被访问一次，时间就能降到 `O(n)`。

**核心想法**：对每个节点返回四个信息（题目提示里已经说了）  

| 参数 | 含义 | 类比 |
|------|------|------|
| `is_bst` | 这棵子树是否是合法的 BST | 像字典里 “这个词是否在词典中”。 |
| `sum_val` | 若是 BST，这棵子树所有节点值的总和 | 像购物车里商品的总价。 |
| `min_val` | 子树中最小的节点值 | 像 “这本书里最小的页码”。 |
| `max_val` | 子树中最大的节点值 | 像 “这本书里最大的页码”。 |

**后序遍历**（先处理左右子树，再处理自己）可以保证：  
- 当我们要处理当前节点时，左、右子树的信息已经准备好。  
- 只需要检查 **左子树最大值 < 当前节点值 < 右子树最小值**，并且左右子树本身都是 BST，即可判断当前整棵子树是否是 BST。  

如果是 BST：  
- `sum_val = left.sum_val + right.sum_val + node.val`  
- 更新全局最大和 `ans = max(ans, sum_val)`  

如果不是 BST：  
- 为了不影响父节点的判断，**把 `is_bst` 设为 `False`**，并把 `sum_val` 随便设成 `0`（父节点只会在 `is_bst` 为 `True` 时才使用它）。  

**为什么这样是线性时间？**  
- 每个节点只做一次常数级的工作（读取左右子树的四个数，做几次比较和加法），没有重复遍历子树的行为。  
- 整棵树的节点数是 `n`，所以总工作量是 `O(n)`。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxSumBST(root: TreeNode) -> int:
    """
    最优解：一次后序遍历返回 (is_bst, sum, min, max)。
    通过全局变量 ans 记录遍历过程中出现的最大 BST 子树和。
    """
    ans = 0  # 全局最大和，初始为 0（空树的和）

    def dfs(node):
        """
        返回四元组:
        - is_bst: 当前子树是否是 BST
        - sum_val: 若是 BST，子树所有节点值的和；否则随意返回 0
        - min_val: 子树中最小的节点值（用于父节点比较）
        - max_val: 子树中最大的节点值（用于父节点比较）
        """
        nonlocal ans
        if not node:
            # 空树：是 BST，和为 0，最小值设 +inf，最大值设 -inf（方便比较）
            return True, 0, float('inf'), float('-inf')

        # 先递归得到左、右子树的信息
        left_is, left_sum, left_min, left_max = dfs(node.left)
        right_is, right_sum, right_min, right_max = dfs(node.right)

        # 判断当前子树是否满足 BST 条件
        if left_is and right_is and left_max < node.val < right_min:
            cur_sum = left_sum + right_sum + node.val   # 当前子树的总和
            ans = max(ans, cur_sum)                     # 更新全局最大和

            cur_min = min(left_min, node.val)           # 当前子树的最小值
            cur_max = max(right_max, node.val)          # 当前子树的最大值
            return True, cur_sum, cur_min, cur_max
        else:
            # 不是 BST，返回的 sum、min、max 对父节点没有意义
            return False, 0, 0, 0

    dfs(root)
    return ans
```

> **代码要点**  
> - `nonlocal ans` 让内部的 `dfs` 能修改外层的 `ans`，类似把答案装进一个全局的“记事本”。  
> - 空树的 `min_val = +inf`、`max_val = -inf` 是“极端值”，保证在父节点比较时不会误判。  
> - 当子树不是 BST 时，直接把 `is_bst` 设为 `False`，让上层在判断时自动失效。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只访问一次，做常数次运算。  
  - 与暴力解相比，省掉了重复遍历子树的“二次循环”。  
- **空间复杂度**：`O(h)`，其中 `h` 为树的高度（递归栈的深度）。  
  - 最坏情况下树是链状，`h = n`，即 `O(n)`；平均情况下（平衡树）`h ≈ log n`，更省内存。

---  

## 心得  

- **核心技巧**：后序遍历 + 动态规划（把子树信息向上合并）。  
- **适用的题型**  
  1. “求满足某种性质的子树的最大/最小值”，如 **“Maximum Sum Subtree with All Even Nodes”**。  
  2. “判断每个子树是否满足约束并统计”，如 **“Largest BST Subtree”**（返回节点数而非和）。  
  3. “在树上做区间/范围检查”，如 **“Validate Binary Search Tree”**（仅判断整棵树是否 BST）。  
- **一句话总结解题钥匙**：**一次后序遍历，把每棵子树的 “是否是 BST、子树和、最小值、最大值” 四件事一起带回父节点**。

## 反思  

- **第一反应**：直接把每个子树都检查一遍，写出暴力实现。  
- **最容易踩的坑**  
  - **空树的极值**：忘记把空树的 `min` 设为 `+inf`、`max` 设为 `-inf`，会导致父节点比较出错。  
  - **负数节点**：题目要求如果所有节点都是负数，返回 `0`（相当于“空 BST”），因此全局答案的初始值要设为 `0`，而不是 `-inf`。  
  - **递归深度**：在极端的链状树里递归深度会达到 `n`，在 Python 中可能需要 `sys.setrecursionlimit`（对面试代码不必担心）。  
- **下次遇到同类题**：先思考 **“能否在一次遍历中把需要的子树信息都算好并返回？”**，如果能，立刻上**后序 DP**；如果不能，再回到暴力枚举的思路。