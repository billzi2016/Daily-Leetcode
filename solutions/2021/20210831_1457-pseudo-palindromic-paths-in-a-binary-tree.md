# #1457. 二叉树中的伪回文路径 / Pseudo-Palindromic Paths in a Binary Tree

> 难度：中等 · 标签：Bit Manipulation、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/pseudo-palindromic-paths-in-a-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree where node values are digits from 1 to 9. A path in the binary tree is said to be pseudo-palindromic if at least one permutation of the node values in the path is a palindrome.
Return the number of pseudo-palindromic paths going from the root node to leaf nodes.

**Examples**

**Example 1:**

```
Input: root = [2,3,1,3,1,null,1]
Output: 2 
Explanation: The figure above represents the given binary tree. There are three paths going from the root node to leaf nodes: the red path [2,3,3], the green path [2,1,1], and the path [2,3,1]. Among these paths only red path and green path are pseudo-palindromic paths since the red path [2,3,3] can be rearranged in [3,2,3] (palindrome) and the green path [2,1,1] can be rearranged in [1,2,1] (palindrome).
```

**Example 2:**

```
Input: root = [2,1,1,1,3,null,null,null,null,null,1]
Output: 1 
Explanation: The figure above represents the given binary tree. There are three paths going from the root node to leaf nodes: the green path [2,1,1], the path [2,1,3,1], and the path [2,1]. Among these paths only the green path is pseudo-palindromic since [2,1,1] can be rearranged in [1,2,1] (palindrome).
```

**Example 3:**

```
Input: root = [9]
Output: 1
```

**Constraints**

- The number of nodes in the tree is in the range [1, 105].
- 1 <= Node.val <= 9

---

## 题目（中文翻译）

**题目描述**  
给定一棵二叉树（binary tree），其中每个节点的值都是 1 到 9 的数字。若从根节点到某个叶子节点的路径上，节点值的某种排列（permutation）能够形成回文（palindrome），则该路径被称为伪回文路径（pseudo‑palindromic path）。请返回所有从根节点到叶子节点的伪回文路径的数量。

**示例**

**示例 1**  
```
Input: root = [2,3,1,3,1,null,1]
Output: 2
Explanation: 上图表示给定的二叉树。共有三条从根节点到叶子节点的路径：红色路径 [2,3,3]、绿色路径 [2,1,1] 和路径 [2,3,1]。其中只有红色路径和绿色路径是伪回文路径，因为红色路径 [2,3,3] 可以重新排列为 [3,2,3]（回文），绿色路径同理…（已截断）
```

**示例 2**  
```
Input: root = [2,1,1,1,3,null,null,null,null,null,1]
Output: 1
Explanation: 上图表示给定的二叉树。共有三条从根节点到叶子节点的路径：绿色路径 [2,1,1]、路径 [2,1,3,1] 和路径 [2,1]。只有绿色路径是伪回文路径，因为 [2,1,1] 可以重新排列为 [1,2,1]（回文）。
```

**示例 3**  
```
Input: root = [9]
Output: 1
```

**约束条件**  
- 树中节点的数量在区间 `[1, 10^5]` 内。  
- `1 <= Node.val <= 9`（节点值在 1 到 9 之间）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一条从根节点到叶子节点的路径都找出来**，然后把路径上的数字放进一个列表里，统计每个数字出现的次数，判断这条路径能否排列成回文。

- **数据结构**  
  - `list`（列表）——就像我们把路上看到的数字一个一个装进背包，等走完了再检查背包里有什么。  
  - `dict`（字典）——相当于查字典：键（key）是数字 1~9，值（value）是该数字出现的次数。  

- **为什么正确**  
  回文的本质是“左右对称”。如果把路径上的数字重新排列，只要**至多有一个数字出现奇数次**，其余数字都出现偶数次，就一定能排成回文（奇数个字符的回文中心只能有一个奇数次数的字符，偶数个字符的回文则必须全部是偶数次）。所以我们只要数一数每条路径上各数字出现的次数，检查奇数次数的数字有几个，就能判断这条路径是否伪回文。

- **时间/空间复杂度**  
  - 我们要遍历整棵树一次，找到所有根到叶的路径。设树有 `n` 个节点，树的高度（最长路径长度）记为 `h`。  
  - 对每一条路径，我们会把路径上的节点值收集到列表里，最多 `h` 个元素；随后遍历这 `h` 个元素统计出现次数。  
  - **时间复杂度** 大约是 `O(n * h)`，因为每条路径的统计都要花 `O(h)` 的时间。  
    - 用大白话说，就是如果树很“细长”（高度接近节点数），最坏情况下会接近 `O(n²)`，因为每次都要把几乎所有节点再数一遍。  
  - **空间复杂度** 为 `O(h)`，因为递归栈（或显式的栈）最多保存树的深度，加上暂存路径的列表也最多 `h` 长。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值，范围 1~9
        self.left = left        # 左子树
        self.right = right      # 右子树

class Solution:
    def pseudoPalindromicPaths(self, root: TreeNode) -> int:
        # 记录满足条件的路径数量
        self.answer = 0

        # 深度优先遍历，path 用来存当前根到当前节点的所有值
        def dfs(node: TreeNode, path: list):
            if not node:
                return

            # 把当前节点加入路径
            path.append(node.val)

            # 若到达叶子节点，统计该路径是否伪回文
            if not node.left and not node.right:
                # 用字典统计出现次数
                freq = {}
                for v in path:
                    freq[v] = freq.get(v, 0) + 1

                # 统计出现奇数次的数字有几个
                odd_cnt = sum(cnt % 2 for cnt in freq.values())
                if odd_cnt <= 1:          # 至多一个奇数次，即可排列成回文
                    self.answer += 1

            # 继续向左、右子树搜索
            dfs(node.left, path)
            dfs(node.right, path)

            # 回溯：离开当前节点时把它从路径里删掉
            path.pop()

        dfs(root, [])
        return self.answer
```

#### 复杂度  

- **时间复杂度**：`O(n * h)`  
  - `n` 是节点数，`h` 是树的高度。每条根到叶的路径都要遍历一次并统计频率，最坏情况下（树呈链状）相当于 `O(n²)`。  
- **空间复杂度**：`O(h)`  
  - 递归栈和 `path` 列表的最大长度都是树的高度。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每到达叶子节点都要重新遍历整条路径统计频次**，这导致重复工作。我们可以把“频次的奇偶性”在遍历的过程中**实时维护**，这样在到达叶子时只需要 O(1) 的时间就能判断是否伪回文。

**关键观察**  
- 判断是否可以排列成回文，只关心每个数字出现的**奇偶性**（出现奇数还是偶数），而不关心具体的次数。  
- 由于节点值只有 1~9，正好可以用 **9 位二进制** 来表示这 9 个数字的奇偶性。  
  - 第 `i` 位（0-index）代表数字 `i+1` 当前出现的次数是奇数（位为 1）还是偶数（位为 0）。  
  - 当我们经过一个节点时，只要把对应的那一位 **取反**（异或 `1 << (val-1)`），即可更新奇偶性。  

**为什么这样可以 O(1) 判断**  
- 当到达叶子时，整个路径的奇偶性已经被压缩进一个整数 `mask`。  
- 若 `mask` 只剩下 **至多一位是 1**，说明至多只有一个数字出现奇数次，满足伪回文条件。  
- 判断“至多一位是 1”可以用 `mask & (mask - 1) == 0` 来实现（这个表达式的意义是：如果把最右边的 1 去掉后结果为 0，则说明原来只有 0 或 1 个 1）。  

**算法步骤**（以深度优先搜索为例）  
1. 从根节点开始，`mask = 0`。  
2. 进入节点 `node` 时：`mask ^= 1 << (node.val - 1)`（取反对应位）。  
3. 若 `node` 是叶子节点：检查 `mask & (mask - 1) == 0`，如果成立计数加一。  
4. 递归遍历左、右子树，传递当前的 `mask`。  
5. 递归返回时**不需要手动恢复** `mask`，因为我们是**按值传递**（每层都有自己的副本），所以不需要回溯操作。  

**类比**：想象我们有一个 9 位的灯箱，灯亮代表该数字出现奇数次，灭掉代表偶数次。走过一个节点，就把对应灯的开关拨一下（开变关，关变开）。走完一条路径后，只要灯箱里亮着的灯不超过一盏，就能拼出回文。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def pseudoPalindromicPaths(self, root: TreeNode) -> int:
        """
        使用位掩码（bitmask）实时记录路径上每个数字出现的奇偶性。
        时间复杂度 O(n)，空间复杂度 O(h)（递归栈）。
        """
        def dfs(node: TreeNode, mask: int) -> int:
            if not node:
                return 0

            # 把当前节点对应的位取反，记录奇偶性变化
            mask ^= 1 << (node.val - 1)

            # 若是叶子节点，检查 mask 是否满足「至多一位为 1」的条件
            if not node.left and not node.right:
                # mask & (mask-1) 为 0 表示 mask 中最多只有一个 1
                return 1 if mask & (mask - 1) == 0 else 0

            # 继续向左右子树搜索，累加符合条件的路径数
            left_cnt = dfs(node.left, mask)
            right_cnt = dfs(node.right, mask)
            return left_cnt + right_cnt

        # 初始 mask 为 0（所有数字出现次数都是偶数，即 0 次）
        return dfs(root, 0)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只访问一次，且在访问时只做常数时间的位运算。相比暴力解的 `O(n·h)`，这里不再随树的高度增长而额外增加开销。  
- **空间复杂度**：`O(h)`  
  - 递归栈的深度等于树的高度 `h`，在最坏情况下（链状树）为 `O(n)`，但这已经是遍历树不可避免的空间开销。  

---

## 心得  

- **核心技巧**：**利用位掩码记录奇偶性**，把 “每个数字出现多少次” 简化为 “每个数字出现的是奇数还是偶数”。  
- **适用场景**：  
  1. **伪回文路径**（本题）。  
  2. **树上或数组中出现奇数次数的元素**（如 LeetCode 1372 “Longest ZigZag Path in a Binary Tree” 中的类似思路）。  
  3. **求子数组中出现奇数次数的数目**（如 “Find the Longest Subarray With Median Equals K” 中的前缀异或技巧）。  
- **一句话总结**：**把 1~9 的出现奇偶性压进 9 位二进制，叶子时只要检查这 9 位中 1 的个数是否 ≤1，即可在 O(1) 判断路径是否伪回文。**  

---

## 反思  

- **第一反应**：直接把所有根到叶的路径列出来，然后逐条统计频次。  
- **最容易踩的坑**  
  - **忘记只检查叶子节点**：中间节点不算完整路径，必须等到真正的叶子才判断。  
  - **位运算细节**：`mask ^= 1 << (val - 1)` 中的 `val - 1` 必须正确，否则会把错误的位取反。  
  - **奇偶性判断写错**：`mask & (mask - 1) == 0` 检查的是“至多一个 1”，写成 `mask == 0` 会漏掉只剩一个奇数的情况。  
- **下次类似题的第一步**：先思考“我们真正需要的是什么信息”。如果只关心奇偶性、出现次数的奇偶或是否出现过，尝试用**位掩码**或**布尔数组**在遍历过程中实时维护，而不是在遍历结束后再统计。这样往往能把复杂度从 `O(n·h)` 降到 `O(n)`。