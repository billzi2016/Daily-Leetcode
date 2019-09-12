# #572. 另一棵树的子树 / Subtree of Another Tree

> 难度：简单 · 标签：Tree、Depth-First Search、String Matching、Binary Tree、Hash Function · [LeetCode 链接](https://leetcode.com/problems/subtree-of-another-tree/)

---

## 题目（英文原版）

**Description**

Given the roots of two binary trees root and subRoot, return true if there is a subtree of root with the same structure and node values of subRoot and false otherwise.
A subtree of a binary tree tree is a tree that consists of a node in tree and all of this node's descendants. The tree tree could also be considered as a subtree of itself.

**Examples**

**Example 1:**

```
Input: root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true
```

**Example 2:**

```
Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false
```

**Constraints**

- The number of nodes in the root tree is in the range [1, 2000].
- The number of nodes in the subRoot tree is in the range [1, 1000].
- -104 <= root.val <= 104
- -104 <= subRoot.val <= 104

---

## 题目（中文翻译）

给定两棵二叉树（binary tree）的根节点 `root` 和 `subRoot`，如果 `root` 中存在一个子树（subtree），其结构和节点值完全与 `subRoot` 相同，则返回 `true`；否则返回 `false`。  
二叉树的子树是指由树中某个节点以及该节点的所有后代节点组成的树。整棵树本身也可以视为它自己的子树。

**示例 1**  
**示例 2**  
**约束条件**  

示例：

**示例 1:**  
```
Input: root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true
```

**示例 2:**  
```
Input: root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false
```

约束条件：

- `root` 树的节点数在范围 `[1, 2000]` 内。  
- `subRoot` 树的节点数在范围 `[1, 1000]` 内。  
- `-10^4 <= root.val <= 10^4`  
- `-10^4 <= subRoot.val <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `root` 上的每一个节点都当成可能的子树根节点**，  
然后检查从这个节点开始的子树结构是否和 `subRoot` 完全一样。

- **遍历 `root`**：我们可以用递归的深度优先搜索（DFS）依次访问每个节点。  
- **比较子树是否相同**：再写一个递归函数 `is_same(s, t)`，判断两棵树 `s`、`t` 是否**同构且节点值相等**。  
  - 如果两棵树都为空，说明相等。  
  - 如果只有一棵为空或根节点值不相等，说明不相等。  
  - 否则递归比较左子树和右子树。  

> **类比**：  
> - 哈希表查字典时，`key` 就是我们要找的“词”，`value` 是对应的“页码”。这里的 `root` 就像一本厚厚的词典，我们要在每一页（每个节点）上尝试查找是否能匹配整本“小词典” `subRoot`。  

**为什么正确**：  
- 如果 `subRoot` 真的是 `root` 的子树，那么必然在 `root` 的某个节点处出现一次完整匹配；遍历所有节点必然能找到它。  
- 反之，如果遍历所有节点都没有找到完全相同的结构，则 `subRoot` 不可能是子树。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


class Solution:
    # 主函数：判断 subRoot 是否是 root 的子树
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        # 递归遍历 root 的每个节点
        def dfs(node: TreeNode) -> bool:
            if not node:                     # 到叶子下面的空节点，直接返回 False
                return False
            # 只要当前节点开始的子树和 subRoot 完全相同，就返回 True
            if self.isSame(node, subRoot):
                return True
            # 否则继续向左、向右搜索
            return dfs(node.left) or dfs(node.right)

        return dfs(root)

    # 辅助函数：判断两棵树是否完全相同（结构 + 节点值）
    def isSame(self, s: TreeNode, t: TreeNode) -> bool:
        if not s and not t:          # 两棵树都为空 → 相同
            return True
        if not s or not t:           # 只有一棵为空 → 不相同
            return False
        if s.val != t.val:           # 根节点值不同 → 不相同
            return False
        # 递归比较左子树和右子树
        return self.isSame(s.left, t.left) and self.isSame(s.right, t.right)
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 设 `m = len(root)`，`n = len(subRoot)`。  
  - 对 `root` 的每个节点（最坏 `m` 次）都要调用 `isSame`，而 `isSame` 最多遍历 `subRoot` 的全部节点（`n` 次），所以乘起来是 `m·n`。  
  - 用大白话说，就是“如果两棵树都很大，可能要把每个节点的子树都检查一遍，时间会像两本书的页数相乘那么多”。  

- **空间复杂度**：`O(h1 + h2)`（递归栈）  
  - `h1` 是 `root` 的高度，`h2` 是 `subRoot` 的高度。递归调用会占用与树深度成正比的栈空间。最坏情况下（链状树）高度等于节点数，但总体仍是线性 `O(m + n)`，而不是额外的数组或哈希表。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每次比较子树都要重新遍历 `subRoot`**，导致 `O(m·n)`。  
如果我们把整棵树“序列化”成一个字符串，再利用 **字符串匹配** 的高效算法，就能把比较过程降到线性时间。

**关键点**：

1. **树的序列化**  
   - 采用前序遍历（根‑左‑右）把树写成字符串。  
   - 为了防止结构歧义，需要在遍历时显式记录空节点，例如使用 `#` 代表 `None`。  
   - 示例：  
     ```
     树   3
        / \
       4   5
     前序序列化 → "3,4,1,#,#,2,#,#,5,#,#"
     ```
   - 这样即使节点值相同，空指针的出现也能唯一确定结构。

2. **子串匹配**  
   - 把 `root` 序列化得到 `S`，`subRoot` 序列化得到 `T`。  
   - 判断 `T` 是否是 `S` 的子串。  
   - 为了在最坏情况下仍保持线性时间，使用 **KMP（Knuth-Morris-Pratt）算法** 或 Python 内置的 `in`（实现基于 `O(n)` 的 Boyer‑Moore）。这里演示手写 KMP，思路更清晰。

3. **为什么是线性**  
   - 序列化两棵树各只遍历一次，得到长度分别为 `|S|`、`|T|` 的字符串。  
   - KMP 的匹配过程是 `O(|S| + |T|)`，不需要嵌套循环。  
   - 整体时间复杂度 `O(m + n)`（因为序列化本身就是遍历所有节点），空间复杂度 `O(m + n)` 用于存放序列化结果和 KMP 的部分匹配表（前缀函数）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    # ---------- 1. 序列化 ----------
    def serialize(self, root: TreeNode) -> str:
        """前序遍历 + 空节点标记，返回用逗号分隔的字符串"""
        vals = []

        def preorder(node: TreeNode):
            if not node:
                vals.append('#')          # 用 # 表示空节点，防止结构歧义
                return
            vals.append(str(node.val))    # 记录节点值
            preorder(node.left)           # 左子树
            preorder(node.right)          # 右子树

        preorder(root)
        return ','.join(vals)            # 用逗号分割，防止 12 和 1,2 混淆

    # ---------- 2. KMP 匹配 ----------
    def kmp(self, text: str, pattern: str) -> bool:
        """返回 pattern 是否是 text 的子串（KMP 实现）"""
        if not pattern:          # 空模式永远匹配
            return True
        # 1）构建部分匹配表（next 数组）
        m = len(pattern)
        nxt = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = nxt[j - 1]           # 回退到上一个可能的匹配长度
            if pattern[i] == pattern[j]:
                j += 1
                nxt[i] = j

        # 2）在 text 中查找 pattern
        j = 0
        for i, ch in enumerate(text):
            while j > 0 and ch != pattern[j]:
                j = nxt[j - 1]           # 同样回退
            if ch == pattern[j]:
                j += 1
                if j == m:               # 完全匹配
                    return True
        return False

    # ---------- 主函数 ----------
    def isSubtree(self, root: TreeNode, subRoot: TreeNode) -> bool:
        s = self.serialize(root)      # 主树的序列化
        t = self.serialize(subRoot)   # 子树的序列化
        return self.kmp(s, t)          # 判断是否为子串
```

> **代码说明**  
> - `serialize` 用前序遍历把树转换成唯一的字符串。  
> - `kmp` 里先算出 `pattern`（子树）每个位置的“最长相同前后缀”长度（`next` 数组），随后在 `text`（主树）中快速滑动匹配。  
> - `isSubtree` 只要 `t` 是 `s` 的子串，就返回 `True`，否则 `False`。

#### 复杂度  

- **时间复杂度**：`O(m + n)`  
  - `serialize` 分别遍历两棵树，花费 `O(m)` 与 `O(n)`。  
  - KMP 匹配过程同样是线性 `O(m + n)`。  
  - 整体相加仍是 `O(m + n)`，即**只和节点总数成正比**，比暴力的 `O(m·n)` 快很多。

- **空间复杂度**：`O(m + n)`  
  - 需要存放两棵树的序列化字符串（长度约等于节点数），以及 KMP 的 `next` 数组（长度为 `|t| = O(n)`）。  
  - 递归序列化使用的栈深度为树的高度 `O(h)`，但已被字符串空间所覆盖，整体仍是线性。  

---  

## 心得  

- **核心技巧**：把树结构转成唯一的序列（前序遍历 + 空节点标记），再利用**字符串子串匹配**（KMP）实现线性时间判定。  
- **适用场景**  
  1. 判断两棵树是否相同（`isSameTree`）——可以直接比较序列化结果是否相等。  
  2. 判断一棵树是否是另一棵树的**翻转子树**（先把翻转后的树序列化再匹配）。  
  3. 处理树的**模式匹配**、树的“序列化搜索”类问题（如 LeetCode 1238 “Circular Permutation in Binary Tree”）。  
- **一句话总结**：把树“写成文字”，再用高速的“找字”算法检查子串即可。

---  

## 反思  

- **第一反应**：把 `root` 的每个节点都拿来和 `subRoot` 对比，写递归检查是否相同。  
- **最容易踩的坑**  
  - **空节点的标记**：若序列化时不记录 `None`，会出现结构歧义，例如 `[1,2]` 与 `[1,null,2]` 会产生相同的序列。  
  - **递归深度**：树可能呈链状，递归层数可达 2000，需要注意 Python 递归深度限制（可以 `sys.setrecursionlimit` 或改用迭代）。  
  - **字符串分隔**：直接拼接数字会出现 `12` 与 `1,2` 混淆，使用逗号或其他分隔符可以避免。  
- **下次遇到同类题**：第一步先思考 **“能否把结构转成一维的、容易比较的形式？”**（如序列化、前缀和、哈希），再决定是直接遍历比较还是使用成熟的“一维匹配”算法。