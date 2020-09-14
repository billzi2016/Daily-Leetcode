# #988. 最小字符串从叶子开始 / Smallest String Starting From Leaf

> 难度：中等 · 标签：String、Backtracking、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/smallest-string-starting-from-leaf/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree where each node has a value in the range [0, 25] representing the letters 'a' to 'z'.
Return the lexicographically smallest string that starts at a leaf of this tree and ends at the root.
As a reminder, any shorter prefix of a string is lexicographically smaller.
A leaf of a node is a node that has no children.

**Examples**

**Example 1:**

```
Input: root = [0,1,2,3,4,3,4]
Output: "dba"
```

**Example 2:**

```
Input: root = [25,1,3,1,3,0,2]
Output: "adz"
```

**Example 3:**

```
Input: root = [2,2,1,null,1,0,null,0]
Output: "abc"
```

**Constraints**

- The number of nodes in the tree is in the range [1, 8500].
- 0 <= Node.val <= 25

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，其中每个节点的值在 `[0, 25]` 范围内，分别对应字母 `'a'` 到 `'z'`。请返回从该树的叶子节点（leaf）出发、以根节点结束的字典序（lexicographically）最小的字符串。  
需要注意的是，任意字符串的较短前缀在字典序上更小。  
叶子节点是指没有子节点的节点。

**示例 1**  
**示例 2**  
**示例 3**

**示例**  
示例 1:  
```
Input: root = [0,1,2,3,4,3,4]
Output: "dba"
```

示例 2:  
```
Input: root = [25,1,3,1,3,0,2]
Output: "adz"
```

示例 3:  
```
Input: root = [2,2,1,null,1,0,null,0]
Output: "abc"
```

**约束条件**  
- 树中节点的数量在 `[1, 8500]` 区间内。  
- `0 <= Node.val <= 25`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每条从根到叶子的路径都列出来**，然后把路径上的数字转换成字符，得到若干字符串，最后挑出字典序最小的那个。

- **数据结构**  
  - **递归栈**：把树的遍历想象成一次“爬山”。我们从根往下走，每往下一层，就把当前节点的字符压进一个列表（相当于背包），到叶子时把背包里的字符倒序拼成字符串。  
  - **列表 → 字符串**：列表就像一串珠子，`['a','b','c']` 用 `''.join()` 把珠子连起来就得到 `"abc"`。  

- **为什么正确**  
  - 树的每一条根‑叶路径必然对应唯一的一条字符串（因为每个节点的值固定），遍历所有路径就不会漏掉任何可能的答案。  
  - 把所有字符串收集后，用 Python 的比较运算符直接找最小的，即可得到字典序最小的字符串。  

- **复杂度分析（大白话）**  
  - **时间**：我们要访问树里的每个节点一次（`O(N)`），并且在每条路径结束时把路径转成字符串。最坏情况下树是一条链，路径长度为 `N`，所以拼接字符串的代价是 `O(N)`，整体是 `O(N²)`。可以把 `N²` 想象成“如果树有 1000 个节点，最坏情况下大约要做 1,000,000 次基本操作”。  
  - **空间**：递归栈的最大深度等于树的高度，最坏是 `N`，再加上保存所有路径字符串的列表（最坏每条路径都要保存一次），所以 `O(N²)` 的空间。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 0~25，对应 'a'~'z'
        self.left = left
        self.right = right

class Solution:
    def smallestFromLeaf(self, root: TreeNode) -> str:
        # 用来保存所有叶子到根的字符串
        all_strings = []

        # 深度优先遍历，path 用列表记录从根到当前节点的字符（正序）
        def dfs(node, path):
            if not node:
                return
            # 把当前节点的字符加入路径
            path.append(chr(ord('a') + node.val))   # 0 -> 'a', 1 -> 'b', ...

            # 如果是叶子节点，生成 leaf->root 的字符串
            if not node.left and not node.right:
                # path 现在是根到叶的顺序，反转后就是叶到根
                leaf_to_root = ''.join(reversed(path))
                all_strings.append(leaf_to_root)

            # 继续向左、右子树遍历
            dfs(node.left, path)
            dfs(node.right, path)

            # 回溯：离开当前节点时把它弹出，恢复到父节点的状态
            path.pop()

        dfs(root, [])
        # Python 的 min 能直接比较字典序
        return min(all_strings)
```

#### 复杂度

- **时间复杂度**：`O(N²)`  
  - 解释：每个节点都会被访问一次 (`O(N)`)；在最坏的链状树里，拼接字符串需要遍历整条路径 (`O(N)`)，两者相乘得到 `O(N²)`。  
- **空间复杂度**：`O(N²)`  
  - 解释：递归栈最深 `O(N)`，再加上保存所有叶子路径字符串的列表（最坏每条路径都要保存一次），整体也是 `O(N²)`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“保存所有路径再找最小”**是低效的。我们只需要**在遍历的过程中实时维护当前最小的字符串**，不必把所有字符串都记下来。这样可以把空间从 `O(N²)` 降到 `O(N)`（递归栈），时间也降到 `O(N)`。

**关键瓶颈**  
- 暴力解在每条叶子路径结束时都要**复制并反转**路径列表，导致额外的 `O(L)`（路径长度）开销。  
- 另外，把所有字符串放进列表再 `min()`，相当于多了一遍遍历。

**优化思路**  

1. **深度优先遍历**（DFS）仍然是最自然的方式，因为我们需要从根往下走才能知道每条路径。  
2. 在递归的 **返回阶段**（即从子节点回到父节点时），**直接构造当前节点到叶子的字符串**，并把它和全局最小答案比较。这样我们只会在叶子节点生成一次字符串，内部不需要额外的列表复制。  
3. 使用 **字符串拼接** 而不是列表反转。因为 Python 的字符串是不可变的，频繁拼接会产生新对象，但我们只在每条路径的 **叶子** 处做一次完整拼接，整体仍是 `O(N)`。  
4. 维护一个全局变量 `best`，初始化为一个非常大的字符串（比如 `~`），每次得到新的 candidate 时，用 `if candidate < best` 更新。

**类比**：想象我们在山上寻找海拔最低的山谷。暴力解是把所有山谷的海拔记录下来，最后挑最小；最优解是边走边记“到目前为止看到的最低海拔”，不必把所有海拔都写下来。

#### 代码（Python）

```python
class Solution:
    def smallestFromLeaf(self, root: TreeNode) -> str:
        # 初始化为一个比任何合法答案都大的字符，'{' 的 ASCII > 'z'
        self.best = '{'   # 只要有一个字符更大即可

        # dfs 返回从当前节点到叶子最小的字符串（leaf->current）
        def dfs(node):
            if not node:
                # 空节点不贡献字符，返回空字符串
                return ""

            # 递归得到左、右子树的“叶子到当前子节点”的字符串
            left_str = dfs(node.left)
            right_str = dfs(node.right)

            # 当前字符
            cur_char = chr(ord('a') + node.val)

            # 如果左右子树都为空，说明是叶子节点
            if not node.left and not node.right:
                candidate = cur_char   # 叶子本身就是 leaf->root 的字符串（此时只有一个字符）
                if candidate < self.best:
                    self.best = candidate
                return cur_char

            # 否则，选取左右子树中字典序更小的那条路径
            # 注意：子树返回的字符串已经是 leaf->child 的顺序，需要在前面加上当前字符
            if left_str and (not right_str or left_str < right_str):
                best_child = left_str
            else:
                best_child = right_str

            # 当前节点到叶子的完整字符串
            candidate = best_child + cur_char
            # 更新全局最小答案
            if candidate < self.best:
                self.best = candidate

            return candidate  # 把这条最小路径往上传递给父节点

        dfs(root)
        return self.best
```

**代码要点说明**  

- `self.best = '{'`：字符 `'{'` 的 ASCII 码是 123，正好比 `'z'`（122）大，保证任何合法字符串都会比它小。  
- `dfs` **返回值** 是**从叶子到当前节点**的字符串（而不是根到叶），这样在父节点只需要把自己的字符拼在后面即可。  
- 当节点是叶子时，直接把自己的字符当作 candidate；否则，从左、右子树返回的两条路径中挑字典序更小的一条，再加上自己的字符。  
- 每访问一个节点只做 **常数次** 字符比较和拼接，整体线性。

#### 复杂度

- **时间复杂度**：`O(N)`  
  - 解释：每个节点只被访问一次，内部只做常数次字符比较和拼接（拼接长度等于路径深度，但每条路径的拼接只在一次返回时完成），所以整体随节点数线性增长。  
- **空间复杂度**：`O(H)`（递归栈），其中 `H` 为树的高度，最坏 `O(N)`（链状树），平均 `O(log N)`（平衡二叉树）。不再额外保存所有路径字符串。

---

## 心得

- **核心技巧**：**深度优先遍历 + 在递归返回时即时构造并比较路径字符串**。  
- **适用的题型**  
  1. “找根到叶子路径上满足某种条件的最小/最大值” （如 LeetCode 1248 `Count Number of Nice Subarrays` 的类似思路）。  
  2. “树上路径的字典序比较” （如 988 `Smallest String Starting From Leaf`、1081 `Smallest Subsequence of Distinct Characters` 中的贪心思路）。  
  3. “需要在遍历过程中维护全局最优解” 的各种回溯/DFS 题目。  

- **一句话总结解题钥匙**：**“在遍历的过程中把答案“边走边算”，不要等所有路径都列完再比较”。**

---

## 反思

- **第一反应**：看到“从叶子到根的字符串”，立刻想到要把所有根‑叶路径列出来，然后比较字典序。  
- **最容易踩的坑**  
  - **字符串方向**：题目要求 **叶子 → 根**，而常规 DFS 是根 → 叶，容易写反。  
  - **字典序比较**：忘记“短前缀更小”的规则，导致在比较时只看字符逐个而忽略长度。  
  - **递归返回值的设计**：如果返回的是根→叶顺序，拼接会很麻烦，需要额外的反转。  
- **下次遇到同类题**：第一步先**明确路径的方向**（是从根到叶还是相反），然后**考虑在递归返回时直接把当前节点的字符加入路径**，并**实时维护最优解**，避免全局收集所有路径。