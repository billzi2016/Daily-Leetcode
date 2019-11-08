# #652. 寻找重复的子树 / Find Duplicate Subtrees

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/find-duplicate-subtrees/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return all duplicate subtrees.
For each kind of duplicate subtrees, you only need to return the root node of any one of them.
Two trees are duplicate if they have the same structure with the same node values.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,null,2,4,null,null,4]
Output: [[2,4],[4]]
```

**Example 2:**

```
Input: root = [2,1,1]
Output: [[1]]
```

**Example 3:**

```
Input: root = [2,2,2,3,null,3,null]
Output: [[2,3],[3]]
```

**Constraints**

- The number of the nodes in the tree will be in the range [1, 5000]
- -200 <= Node.val <= 200

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，返回所有出现重复的子树（subtree）。  
对于每一种重复的子树，只需要返回其中任意一个根节点。  
如果两棵树的结构相同且对应节点的值相同，则认为它们是重复的。

**示例**

**示例 1**  
输入: `root = [1,2,3,4,null,2,4,null,null,4]`  
输出: `[[2,4],[4]]`

**示例 2**  
输入: `root = [2,1,1]`  
输出: `[[1]]`

**示例 3**  
输入: `root = [2,2,2,3,null,3,null]`  
输出: `[[2,3],[3]]`

**约束条件**

- 树中节点的数量在 `[1, 5000]` 范围内。  
- `-200 <= Node.val <= 200`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每棵子树** 都“记录下来”，然后两两比较，看有没有完全相同的。  
- **子树**：从某个节点出发，包括它自己以及下面的所有节点。  
- **记录方式**：可以把子树序列化成一个字符串，例如「根-左-右」的前序遍历 `"1,2,#,#,3,#,#"`（`#` 表示空节点）。这样两棵结构相同且节点值相同的子树，就会得到完全相同的字符串。  

把所有子树的序列化结果放进一个 **列表**，随后遍历列表，找出出现次数 ≥2 的序列，对应的根节点即为重复子树的根。

> **类比**：把每棵子树想象成一本书的章节标题，用一本“大字典”记录所有出现过的标题（序列化字符串）。如果同一个标题出现了两次以上，就说明这两章内容完全相同。

**为什么正确**：  
- 两棵子树相同 ⇔ 它们的结构相同且每个位置的值相同。  
- 前序遍历（根-左-右）在遇到空节点时也写入 `#`，保证了结构信息不丢失。  
- 因此相同的子树一定得到相同的序列化字符串，反之亦然。

**复杂度分析（大白话）**  
- **时间**：  
  1) 对每个节点都要做一次序列化，序列化过程会遍历整棵子树，最坏情况是根节点的子树包含了所有 `N` 个节点。于是每个节点的序列化平均要遍历 `O(N)`，总共是 `O(N²)`。  
  2) 再把所有序列化结果两两比较，最坏也是 `O(N²)`。  
  综合下来，时间复杂度是 **O(N²)**，即“如果树有 1000 个节点，程序可能要跑上 1000×1000 次操作”。  

- **空间**：  
  - 保存所有序列化字符串需要 `O(N²)`（每个字符串最坏长度是 `N`，有 `N` 条）。  
  - 递归栈深度最坏是 `O(N)`（链状树）。  
  故总体空间是 **O(N²)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def serialize(root):
    """把以 root 为根的子树序列化为字符串，使用前序遍历 + # 标记空节点"""
    if not root:
        return "#"
    # 递归序列化左、右子树
    left_str = serialize(root.left)
    right_str = serialize(root.right)
    # 用逗号把各部分拼起来，形成唯一标识
    return f"{root.val},{left_str},{right_str}"

def findDuplicateSubtrees(root):
    """暴力版：收集所有子树的序列化，再找出现多次的根节点"""
    if not root:
        return []

    # 1) 收集所有子树的序列化 + 对应根节点
    all_subtrees = []                     # [(序列化字符串, 根节点)]
    def dfs(node):
        if not node:
            return "#"
        s = f"{node.val},{dfs(node.left)},{dfs(node.right)}"
        all_subtrees.append((s, node))
        return s
    dfs(root)

    # 2) 统计出现次数
    count = {}
    for s, _ in all_subtrees:
        count[s] = count.get(s, 0) + 1

    # 3) 只保留出现 >=2 次的子树根节点（每种只要一个）
    res = []
    seen = set()
    for s, node in all_subtrees:
        if count[s] >= 2 and s not in seen:
            res.append(node)
            seen.add(s)   # 防止同一种子树再加入多次
    return res
```

#### 复杂度

- **时间复杂度**：`O(N²)`  
  > 这里的 `N` 是树的节点数。因为对每个节点都要遍历整棵子树来生成序列化，等价于「每个节点都做一次全树的遍历」。
- **空间复杂度**：`O(N²)`  
  > 保存所有子树的序列化字符串需要 `N` 条，每条最坏长度是 `N`，所以总体是 `N²`。递归栈最多 `O(N)`，不影响总体阶。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **重复遍历** 同一棵子树很多次。  
我们可以在 **一次遍历**（后序遍历）里把子树序列化的工作完成，并且把每个序列化结果立即记到哈希表中，这样：

1. **后序遍历**（左→右→根）保证当我们要序列化当前节点时，它的左右子树已经被序列化并且得到唯一的标识（字符串或整数）。  
2. 用一个 **字典** `cnt` 记录每个序列化标识出现的次数。  
3. 当某个标识的计数恰好变成 `2`（第一次发现重复），把对应的根节点加入答案列表。这样每种重复子树只会被加入一次。  

> **类比**：把每棵子树想成一本书的章节，后序遍历就像先把左边、右边的章节内容写好，再写本章节的标题。写完后立刻把标题放进“出现次数表”。如果同一个标题第二次出现，就把这本章节的指针记下来。

**核心技巧**：  
- **后序遍历 + 哈希计数**：一次遍历完成序列化与重复检测。  
- **序列化的唯一性**：使用 `#` 标记空节点，确保结构信息不丢失。  
- **只记录计数为 2 的节点**：防止同一种子树被多次加入答案。

**为什么是 O(N) 时间**：每个节点只被访问一次，序列化操作只涉及常数次字符串拼接（或改用整数 ID），所以整体是线性时间。

**空间**：  
- 哈希表最多存放 `N` 条唯一的子树标识 → `O(N)`。  
- 递归栈深度最坏 `O(N)`（链状树），整体 `O(N)`。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findDuplicateSubtrees(root):
    """
    最优解：后序遍历 + 哈希表记录子树序列化
    返回所有重复子树的根节点（每种只返回一个）
    """
    from collections import defaultdict
    cnt = defaultdict(int)      # 记录每个序列化字符串出现的次数
    ans = []                     # 最终答案

    def dfs(node):
        """返回以 node 为根的子树的序列化字符串"""
        if not node:
            return "#"           # 空节点的唯一标识
        # 先递归得到左右子树的序列化
        left = dfs(node.left)
        right = dfs(node.right)
        # 组合成当前子树的唯一标识
        serial = f"{node.val},{left},{right}"
        cnt[serial] += 1
        # 当计数恰好等于 2 时，说明第一次发现重复，加入答案
        if cnt[serial] == 2:
            ans.append(node)
        return serial

    dfs(root)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  > 每个节点只做一次递归调用和常数次字符串拼接，等价于「走遍树一次」。
- **空间复杂度**：`O(N)`  
  > 哈希表存放至多 `N` 条子树标识，递归栈深度最坏 `N`，总体是线性空间。

---

## 心得

- **核心技巧**：后序遍历结合哈希计数，用唯一序列化标识一次遍历完成重复检测。  
- **适用题型**：  
  1. “寻找相同子结构” 类的题目（如 **Find Duplicate Subtrees**、**Find Duplicate Subtrees II**）。  
  2. “子树序列化” 相关的题目（如 **Serialize and Deserialize Binary Tree**）。  
  3. “树的同构” 判断（如 **Isomorphic Trees**）。  
- **一句话总结**：一次后序遍历把每棵子树“写进字典”，计数为 2 时即是重复子树的钥匙。

## 反思

- **第一反应**：先想把所有子树保存下来，然后逐个比较——这就是暴力思路。  
- **最容易踩的坑**：  
  - 序列化时忘记加入空节点的标记 `#`，导致结构不同的子树误判相同。  
  - 只记录计数 `>1` 的节点会把同一种子树加入多次，需要在计数恰好等于 2 时才加入答案。  
  - 递归深度过大（链状树）可能导致栈溢出，实际 `N≤5000` 一般安全。  
- **下次类似题的第一步**：先思考“能否在一次遍历中把子结构信息收集起来？”——如果能，用哈希表记录出现次数；如果不能，再考虑暴力或额外的遍历。