# #129. 根到叶子路径数字之和 / Sum Root to Leaf Numbers

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/sum-root-to-leaf-numbers/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree containing digits from 0 to 9 only.
Each root-to-leaf path in the tree represents a number.
Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.
A leaf node is a node with no children.

**Examples**

**Example 1:**

```
Input: root = [1,2,3]
Output: 25
Explanation:
The root-to-leaf path 1->2 represents the number 12.
The root-to-leaf path 1->3 represents the number 13.
Therefore, sum = 12 + 13 = 25.
```

**Example 2:**

```
Input: root = [4,9,0,5,1]
Output: 1026
Explanation:
The root-to-leaf path 4->9->5 represents the number 495.
The root-to-leaf path 4->9->1 represents the number 491.
The root-to-leaf path 4->0 represents the number 40.
Therefore, sum = 495 + 491 + 40 = 1026.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- 0 <= Node.val <= 9
- The depth of the tree will not exceed 10.

---

## 题目（中文翻译）

**描述**  
给定一棵仅包含 0~9 数字的二叉树（binary tree）的根节点 `root`。树中的每一条从根到叶子节点（leaf node）的路径都表示一个整数。返回所有根到叶子路径所表示的整数之和。题目保证答案可以放入 32 位整数。

**示例 1**  
```text
Input: root = [1,2,3]
Output: 25
```
**解释**：  
根到叶子路径 `1->2` 表示数字 **12**。  
根到叶子路径 `1->3` 表示数字 **13**。  
因此，和为 **12 + 13 = 25**。

**示例 2**  
```text
Input: root = [4,9,0,5,1]
Output: 1026
```
**解释**：  
根到叶子路径 `4->9->5` 表示数字 **495**。  
根到叶子路径 `4->9->1` 表示数字 **491**。  
根到叶子路径 `4->0` 表示数字 **40**。  
因此，和为 **495 + 491 + 40 = 1026**。

**约束条件**  
- 树中节点的数量在 `[1, 1000]` 之间。  
- `0 <= Node.val <= 9`  
- 树的深度不超过 `10`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
把每条 **根‑到‑叶** 路径看成一串数字，例如路径 `1 → 2 → 5` 就是数字 **125**。  
最直接的想法是：

1. **遍历** 整棵二叉树，找到所有根到叶子的路径。  
2. 把路径上的节点值 **拼成字符串**（或列表），例如 `['1','2','5']` → `"125"`。  
3. 把字符串转成整数，放进一个 **列表** 中。  
4. 最后把列表里所有整数 **求和**。

> **数据结构类比**：  
> - **栈**（这里用递归实现）就像我们在爬山时的“背包”，每走一步就把当前节点压进去，回到父节点时再弹出来。  
> - **列表**（保存所有路径对应的数字）就像一本“账本”，每记下一个数字就往里写一行，最后把所有行相加得到总账。

这种做法一定能得到正确答案，因为我们把 **每一条合法路径** 都完整记录下来并转成对应的数值，最后求和自然就是题目要的结果。

#### 代码（Python）  
```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点值 0~9
        self.left = left        # 左子树
        self.right = right      # 右子树

def sumNumbers(root: TreeNode) -> int:
    """
    暴力解：先把所有根到叶的数字收集到列表里，再求和。
    """
    if not root:
        return 0

    all_numbers = []                     # 用来保存每条路径对应的整数

    def dfs(node, path):
        """
        深度优先遍历（递归实现），path 是当前路径上所有节点值的列表。
        """
        if not node:
            return

        # 把当前节点值加入路径
        path.append(str(node.val))       # 用字符串便于后面拼接

        # 如果是叶子节点，说明得到了一条完整路径
        if not node.left and not node.right:
            # 把路径列表转成字符串再转成整数，加入 all_numbers
            number = int(''.join(path))
            all_numbers.append(number)
        else:
            # 继续向左、右子树递归
            dfs(node.left, path)
            dfs(node.right, path)

        # 回溯：离开当前节点时把它从路径里移除
        path.pop()

    dfs(root, [])
    # 最后把所有路径对应的数字相加
    return sum(all_numbers)
```

#### 复杂度  
- **时间复杂度**：`O(N·H)`，其中 `N` 是节点数，`H` 是树的高度（最多 10）。  
  - 我们要遍历每个节点一次 (`O(N)`)。  
  - 对每条根到叶的路径，我们会把路径上的节点值拼成字符串，拼接操作的代价与路径长度 `H` 成正比，所以总体是 `O(N·H)`。  
  - 用大白话说，就是“遍历一次树，每条路径再多花一点时间把数字拼起来”。  

- **空间复杂度**：`O(N·H)`（最坏情况）。  
  - 递归栈占用 `O(H)` 空间。  
  - `all_numbers` 最多保存 `O(N)` 条数字，每条数字本身占 `O(H)`（因为是整数，实际占用常数空间，这里为了说明我们把它看作 `H` 位数），所以整体是 `O(N·H)`。  

---

### 2. 最优解  

#### 思路  
在暴力解里，**拼接字符串**、**再转成整数** 是多余的。  
其实我们在遍历树的过程中就可以 **把当前路径对应的数值实时累计**，不需要额外的列表或字符串。  

关键点：

1. **从根到叶的数字** 可以用「左移一位再加新数字」来更新。  
   - 例如已有数 `12`，再往下走到节点 `5`，新数就是 `12 * 10 + 5 = 125`。  
   - 这就像在十进制计数器上往左拨一位，然后加上新出现的数字。  

2. 使用 **深度优先搜索（DFS）**（递归或显式栈）遍历树，**携带当前累计的数值**。  
   - 递归函数的参数 `cur` 表示「从根到当前节点」已经形成的整数。  
   - 到达叶子节点时，`cur` 就是这条路径对应的完整数字，直接累加到答案 `total` 中。  

这样我们只需要 **一次遍历**，不必保存所有路径，也不必做字符串拼接，时间和空间都降到了最优。

> **数据结构类比**：  
> - 累计的整数 `cur` 像是「流水线上的产品」，每经过一个节点就「加工」一次（`*10 + node.val`），直到最终出厂（叶子）时得到完整的成品。  
> - 递归栈仍然是「登山的背包」——只记录当前走到哪一步，背包里不再装满所有历史路径，只装当前累计的数字。

#### 代码（Python）  
```python
def sumNumbers(root: TreeNode) -> int:
    """
    最优解：DFS 同时累计当前路径对应的整数，叶子节点直接加到答案里。
    """
    total = 0                     # 用来累加所有根到叶的数字

    def dfs(node, cur):
        """
        node : 当前遍历到的节点
        cur  : 从根到 node 所构成的整数（已经累计好）
        """
        nonlocal total
        if not node:
            return

        # 把当前节点的值加入路径对应的整数
        cur = cur * 10 + node.val   # 例如 12 -> 12*10+5 = 125

        # 叶子节点：直接把当前整数加入答案
        if not node.left and not node.right:
            total += cur
            return

        # 继续向左、右子树递归
        dfs(node.left, cur)
        dfs(node.right, cur)

    dfs(root, 0)                    # 初始累计值为 0
    return total
```

#### 复杂度  
- **时间复杂度**：`O(N)`。  
  - 每个节点只访问一次，且在访问时只做常数次算术运算（`*10 + val`），所以整体是线性时间。  
  - 与暴力解相比，省掉了每条路径的字符串拼接，真正只跟节点数成正比。  

- **空间复杂度**：`O(H)`（递归栈深度）。  
  - 只需要保存递归调用栈，深度不超过树的高度 `H ≤ 10`，因此空间开销非常小。  

---

## 心得  

- **核心技巧**：在遍历二叉树的过程中**实时累计**根到当前节点的数值，利用十进制的「左移」特性 `value = prev * 10 + node.val`。  
- **适用题型**：  
  1. “根到叶子路径求和” 类似题目，如 **Path Sum**（求路径和）  
  2. “路径表示数字” 的变体，如 **Binary Tree Paths**（输出所有路径字符串）  
  3. 需要在遍历时**维护前缀信息**的题目，例如 **Maximum XOR of Two Numbers in an Array**（使用前缀异或）  
- **一句话总结**：**把路径数字当作滚动的计数器，边走边算，叶子时直接收割**。

## 反思  

- **第一反应**：先想把所有路径完整保存下来再统一处理（即暴力的思路）。  
- **最容易踩的坑**：  
  - 忘记在递归返回时**回溯**累计值（如果使用全局变量容易出错）。  
  - 对空树或只有根节点的情况没有特殊处理。  
  - 误把 `cur * 10 + node.val` 写成 `cur + node.val * 10`，导致数字顺序错误。  
- **下次遇到同类题**：第一步就问自己——**“这条路径的值能否在遍历过程中即时更新？”**如果能，就直接在 DFS/ BFS 中累加，避免额外存储。