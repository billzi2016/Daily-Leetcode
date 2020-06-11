# #894. 所有可能的满二叉树 / All Possible Full Binary Trees

> 难度：中等 · 标签：Dynamic Programming、Tree、Recursion、Memoization、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/all-possible-full-binary-trees/)

---

## 题目（英文原版）

**Description**

Given an integer n, return a list of all possible full binary trees with n nodes. Each node of each tree in the answer must have Node.val == 0.
Each element of the answer is the root node of one possible tree. You may return the final list of trees in any order.
A full binary tree is a binary tree where each node has exactly 0 or 2 children.

**Examples**

**Example 1:**

```
Input: n = 7
Output: [[0,0,0,null,null,0,0,null,null,0,0],[0,0,0,null,null,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,null,null,null,null,0,0],[0,0,0,0,0,null,null,0,0]]
```

**Example 2:**

```
Input: n = 3
Output: [[0,0,0]]
```

**Constraints**

- 1 <= n <= 20

---

## 题目（中文翻译）

给定一个整数 `n`，返回所有可能的满二叉树（full binary tree）构成的列表（list），其中每棵树恰好包含 `n` 个节点（node）。  
答案中的每棵树的每个节点（node）都必须满足 `Node.val == 0`。  
答案的每个元素都是一棵可能的树的根节点（root node）。返回的树列表（list）可以任意顺序。  

满二叉树（full binary tree）是指每个节点（node）要么没有子节点，要么恰好有两个子节点（children）的二叉树（binary tree）。

**示例 1**  
输入: `n = 7`  
输出: `[[0,0,0,null,null,0,0,null,null,0,0],[0,0,0,null,null,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,null,null,null,null,0,0],[0,0,0,0,0,null,null,0,0]]`

**示例 2**  
输入: `n = 3`  
输出: `[[0,0,0]]`

**约束条件**  
- `1 <= n <= 20`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **全二叉树的定义**：每个节点要么没有子节点（叶子），要么恰好有两个子节点（左、右各一棵子树）。  
2. **把问题拆成子问题**：根节点占 1 个位置，剩下的 `n-1` 个节点必须被划分到左子树和右子树。设左子树有 `i` 个节点，右子树就有 `n-1-i` 个节点。  
3. **只考虑合法的划分**：因为每棵全二叉树的节点数一定是奇数（根 + 两个子树），所以 `i` 必须是奇数，`n-1-i` 也必须是奇数。  
4. **递归枚举**：对每一种合法的 `i`，递归生成所有可能的左子树列表 `leftList` 和右子树列表 `rightList`，然后把左、右子树两两组合，挂到根节点下，得到完整的树。  
5. **暴力实现**：不做任何记忆化（Memo），每次递归都会重新计算相同规模的子树，导致大量重复工作。

> **类比**：把「全二叉树」想象成「拼装玩具」。根节点是主体，左、右各是一套子玩具。我们要把所有可能的左套和右套全部尝试一遍，哪怕之前已经拼装过同样的套装，也要再拼一次——这就是「暴力」的做法。

#### 代码（Python）

```python
# 定义二叉树节点（LeetCode 中的标准写法）
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 题目要求所有节点的值都是 0
        self.left = left
        self.right = right

def all_possible_fbt_bruteforce(n: int):
    """
    暴力递归：不使用记忆化，直接枚举所有划分
    返回所有根节点组成的列表
    """
    # 只有 1 个节点时，唯一合法的全二叉树就是单节点树
    if n == 1:
        return [TreeNode(0)]

    result = []
    # 左子树节点数 i 必须是奇数，且 1 <= i <= n-2
    for i in range(1, n, 2):
        left_cnt = i
        right_cnt = n - 1 - i
        # 递归生成左子树、右子树的所有可能
        left_trees = all_possible_fbt_bruteforce(left_cnt)
        right_trees = all_possible_fbt_bruteforce(right_cnt)

        # 两两组合，挂到根节点下
        for left in left_trees:
            for right in right_trees:
                root = TreeNode(0)      # 创建根节点，值固定为 0
                root.left = left        # 把左子树接上
                root.right = right      # 把右子树接上
                result.append(root)     # 收集当前完整树
    return result
```

#### 复杂度  

- **时间复杂度**：`O(C_n)`（Catalan 数），大约是 `O(2^n)` 的量级。  
  - 解释：每次划分会产生左、右子树的笛卡尔积，递归树的规模呈指数增长。对于 `n=7`，会产生 5 棵树；`n=15` 时会产生 429 棵树，数量快速爆炸。  
- **空间复杂度**：`O(n)`（递归栈深度）+ 保存所有树的空间。  
  - 解释：递归的最大深度等于树的高度，大约是 `n/2`（因为每层至少占 2 个节点），再加上要把所有生成的树全部存下来，实际占用会更大。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**大量重复计算** 是主要瓶颈。比如在 `n=7` 的递归过程中，会多次求解「节点数为 3 的全二叉树」——每次都要重新遍历同样的子树结构。

**关键优化点**：**记忆化（Memoization）** + **自底向上的动态规划**。  

1. **记忆化**：把已经算好的 `f(i)`（所有 `i` 个节点的全二叉树列表）缓存起来，下次需要相同 `i` 时直接取，避免重复递归。  
2. **自底向上**：先算最小的子问题（`n=1`），再逐步算 `3、5、7…`，每一次都使用已经缓存好的子问题结果。这样每种规模的树只会被构造一次。  
3. **核心数据结构——哈希表**：在 Python 中使用字典 `memo` 把 `n` 映射到对应的树列表。字典就像一本「查字典」，我们给它一个「词」`n`，它立刻告诉我们对应的「页码」——已经生成好的树集合。  

**组合过程**与暴力解相同：遍历所有奇数划分 `i`，把左、右子树的所有组合挂到根节点。唯一的不同是左、右子树直接从 `memo` 里取，而不是再次递归。

> **类比**：想象你在拼装玩具，每次需要一套左子玩具和右子玩具。记忆化相当于在背包里提前把每种尺寸的玩具套装准备好，下次再拼时直接拿出来，不必重新制造。

#### 代码（Python）

```python
from functools import lru_cache   # Python 标准库提供的记忆化装饰器

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def all_possible_fbt(n: int):
    """
    使用记忆化的递归（自底向上）求所有全二叉树
    """
    @lru_cache(maxsize=None)          # 自动把函数的返回值缓存起来
    def helper(nodes: int):
        # 只有 1 个节点时，唯一解
        if nodes == 1:
            return [TreeNode(0)]

        trees = []
        # 左子树节点数 i 必须是奇数
        for i in range(1, nodes, 2):
            left_cnt = i
            right_cnt = nodes - 1 - i

            left_subtrees = helper(left_cnt)   # 直接从缓存拿
            right_subtrees = helper(right_cnt)

            # 两两组合
            for left in left_subtrees:
                for right in right_subtrees:
                    root = TreeNode(0)
                    root.left = left
                    root.right = right
                    trees.append(root)
        return trees

    # 题目规定 n 必须是奇数，否则不存在全二叉树
    if n % 2 == 0:
        return []
    return helper(n)
```

> **代码要点说明**  
> - `@lru_cache`：装饰器会把 `helper(k)` 的返回值保存下来，下次再调用 `helper(k)` 时直接返回，省去递归。  
> - `if n % 2 == 0: return []`：偶数个节点根本不可能构成全二叉树，因为每增加一层必须成对增加子节点。  
> - 每创建一个 `TreeNode` 时都把左右指针指向对应的子树，最终返回的列表里每个元素都是一棵完整的树。

#### 复杂度  

- **时间复杂度**：`O(C_n)`（Catalan 数），但**每种规模只算一次**，实际常数比暴力解小很多。  
  - 解释：对每个奇数 `i (1 ≤ i ≤ n)`，我们遍历左、右子树的所有组合。组合的总次数正好等于所有可能全二叉树的数量——Catalan 数。因为没有重复递归，时间等价于「生成所有合法树」的成本。  
- **空间复杂度**：`O(C_n * n)`（存放所有树的节点）+ `O(n)`（递归栈）  
  - 解释：需要把所有生成的树保存下来，树的总节点数约为 `C_n * n`（每棵树有 `n` 个节点），再加上递归深度 `≈ n/2` 的栈空间。

与暴力解相比，**时间从指数级的重复计算降到了仅生成一次**，实际运行在 `n ≤ 20` 时毫秒即可完成。

---

## 心得  

- **核心技巧**：**记忆化递归 / 动态规划**，把「子问题的答案」保存下来，避免重复计算。  
- **适用题型**：  
  1. **所有可能的二叉树结构**（如「不同的二叉搜索树」LeetCode 95）  
  2. **分割类 DP**（如「不同的划分方法」LeetCode 119）  
  3. **组合类递归**（如「不同的硬币找零」LeetCode 322）  
- **一句话总结**：**把大问题拆成相同子规模的子问题，记住每一次拆分的结果，下次直接复用**。

---

## 反思  

- **第一反应**：看到“全二叉树”，立刻想到“根占 1，左右各是一棵全二叉树”，于是写出递归枚举的雏形。  
- **最容易踩的坑**：  
  1. **奇偶性**：忘记检查 `n` 是否为奇数，导致返回空列表或无限递归。  
  2. **深拷贝**：在组合左右子树时必须为每一次组合新建根节点，否则会出现同一个子树被多次共享，导致最终结果被破坏。  
  3. **缓存键**：如果自行实现记忆化，键必须是节点数 `int`，不能使用可变对象。  
- **下次遇到同类题的第一步**：**先判断子问题是否可以重复利用（是否存在重叠子结构）**，若有，则立刻准备记忆化或 DP 表。这样可以把“暴力递归”快速升级为“高效递归”。