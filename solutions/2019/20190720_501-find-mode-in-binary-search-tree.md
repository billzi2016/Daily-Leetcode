# #501. 二叉搜索树中的众数 / Find Mode in Binary Search Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/find-mode-in-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary search tree (BST) with duplicates, return all the mode(s) (i.e., the most frequently occurred element) in it.
If the tree has more than one mode, return them in any order.
Assume a BST is defined as follows:

**Examples**

**Example 1:**

```
Input: root = [1,null,2,2]
Output: [2]
```

**Example 2:**

```
Input: root = [0]
Output: [0]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -105 <= Node.val <= 105

---

## 题目（中文翻译）

给定一棵可能包含重复元素的二叉搜索树（Binary Search Tree, BST）的根节点 `root`，返回其中所有出现频率最高的元素（即众数）。如果树中存在多个众数，返回它们的顺序可以任意。

假设 BST 的定义如下：

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  
**示例 1:**  
```
Input: root = [1,null,2,2]
Output: [2]
```

**示例 2:**  
```
Input: root = [0]
Output: [0]
```

**约束条件**  
- 树中节点的数量在 `[1, 10^4]` 区间内。  
- `-10^5 <= Node.val <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把树里所有的数字都摘下来，统计每个数字出现了几次」，类似于我们平时把一堆水果装进盒子里，然后逐个数每种水果的数量。

实现时可以：

1. **遍历整棵二叉搜索树**（先序、后序或层序都行），把每个节点的 `val` 加到一个 **哈希表**（Python 的 `dict`）中。  
   - 哈希表就像一本“字典”，`key` 是水果的种类（这里是节点的数值），`value` 是出现的次数。查找、插入、更新的时间都是 **O(1)**，所以统计过程非常快。
2. 统计完后，遍历哈希表找到最大的出现次数 `max_cnt`，把所有出现次数等于 `max_cnt` 的键收集起来，就是答案。

> **为什么正确？**  
> 我们遍历了每一个节点，并且对每个节点的值都做了完整的计数。最后挑出出现次数最多的值，必然就是出现频率最高的元素（即**众数**），不管树的结构是怎样的都不会错。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def findMode(root: TreeNode) -> list[int]:
    """暴力解：使用哈希表统计每个值出现的次数"""
    if not root:
        return []

    # 1. 用字典统计出现次数，key 是节点的值，value 是出现次数
    count = {}

    def dfs(node: TreeNode):
        """深度优先遍历整棵树"""
        if not node:
            return
        # 把当前节点的值计数 +1
        count[node.val] = count.get(node.val, 0) + 1
        dfs(node.left)   # 左子树
        dfs(node.right)  # 右子树

    dfs(root)

    # 2. 找到最大的出现次数
    max_cnt = max(count.values())

    # 3. 收集所有出现次数等于 max_cnt 的值
    modes = [val for val, cnt in count.items() if cnt == max_cnt]
    return modes
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  需要访问每个节点一次，`N` 为树的节点数。遍历哈希表找最大值和收集答案同样是 `O(N)`，所以整体是线性时间。  
  > *大白话：如果树里有 10,000 个节点，代码大约会跑 10,000 步。*

- **空间复杂度：** `O(N)`  
  哈希表最坏情况下会存下所有不同的节点值，最多需要 `N` 个键值对。递归栈的深度是树高 `H`，但在最坏的链状树里 `H = N`，所以总体仍是 `O(N)`。  
  > *大白话：如果每个节点的值都不相同，我们要准备一个能装 10,000 条记录的“字典”。*  

---

### 2. 最优解

#### 思路  

暴力解的 **时间** 已经是线性的，无法再快；但 **空间** 用了 `O(N)` 的额外哈希表。  
我们可以利用 **二叉搜索树（BST）** 的特性：**中序遍历**（左‑根‑右）会得到 **递增有序** 的序列。  

在有序序列里，**相同的数会连在一起**，所以只要一次遍历就能统计每个数连续出现的次数，而不需要额外的哈希表。我们只需要维护几个变量：

| 变量 | 作用 |
|------|------|
| `prev_val` | 上一次遍历到的数值（用于判断是否和当前值相同） |
| `cur_cnt`  | 当前值连续出现的次数 |
| `max_cnt`  | 迄今为止出现次数的最大值 |
| `modes`    | 收集所有出现次数等于 `max_cnt` 的值 |

遍历过程：

1. **中序遍历** 树，保证我们一次看到的值是从小到大的。  
2. 对每个访问到的节点 `node.val`：  
   - 若 `node.val` 与 `prev_val` 相同 → `cur_cnt += 1`（继续计数）。  
   - 否则 → `cur_cnt = 1`（重新开始计数），并更新 `prev_val`。  
3. 与 `max_cnt` 比较：  
   - 若 `cur_cnt > max_cnt` → 更新 `max_cnt`，并把 `modes` 清空后加入当前值。  
   - 若 `cur_cnt == max_cnt` → 把当前值再加入 `modes`（可能出现多个众数）。  

因为只使用了常数个额外变量（递归栈除外），空间降到了 **O(H)**，其中 `H` 为树的高度。对平衡树来说 `H = O(log N)`，对最坏的链状树来说 `H = O(N)`，但这已经是题目允许的 **隐式递归栈空间**，不算在“额外空间”里。

#### 代码（Python）

```python
def findMode(root: TreeNode) -> list[int]:
    """最优解：利用 BST 的中序遍历，省去哈希表"""
    if not root:
        return []

    # 下面的变量会在闭包里被修改
    modes = []          # 最终答案列表
    prev_val = None     # 前一个访问的值
    cur_cnt = 0         # 当前值的连续计数
    max_cnt = 0         # 目前为止最大的计数

    def inorder(node: TreeNode):
        """递归实现中序遍历（左-根-右）"""
        nonlocal prev_val, cur_cnt, max_cnt, modes
        if not node:
            return
        inorder(node.left)   # 先遍历左子树

        # ---------- 处理当前节点 ----------
        if prev_val is None or node.val != prev_val:
            # 遇到新值，计数重新开始
            cur_cnt = 1
            prev_val = node.val
        else:
            # 与前一个值相同，计数加一
            cur_cnt += 1

        # 与最大计数比较，更新答案列表
        if cur_cnt > max_cnt:
            max_cnt = cur_cnt          # 发现更大的频率
            modes = [node.val]         # 重新开始收集众数
        elif cur_cnt == max_cnt:
            modes.append(node.val)      # 频率相同，也加入

        inorder(node.right)  # 最后遍历右子树

    inorder(root)
    return modes
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  每个节点恰好访问一次（中序遍历），不做额外的遍历或哈希表操作。  
  > *大白话：不管树有多少层，代码只会跑一次“走访每个节点”，和暴力解一样快。*

- **空间复杂度：** `O(H)`（递归栈）  
  只用了常数个额外变量 `prev_val、cur_cnt、max_cnt、modes`，真正占用的额外空间是递归调用栈的深度 `H`。  
  - 对平衡 BST，`H ≈ log₂N`，非常小。  
  - 对最坏的链状 BST，`H = N`，但这已经是语言本身的递归栈，通常不计入“额外空间”。  
  > *大白话：如果树像一条直线，递归会像层层叠加的纸牌，最多需要 N 张纸；如果是平衡树，只需要几层纸（大约 log N 张）。*  

---

## 心得

- **核心技巧**：利用二叉搜索树的中序遍历得到有序序列，进而在一次遍历中完成**计数 + 维护最大频率**。  
- **适用场景**：  
  1. “在有序结构中找出现次数最多的元素” —— 如有序数组、链表。  
  2. “在 BST 中统计某类属性（如出现次数、连续相同节点）” —— 如求最长递增路径、统计不同值的数量。  
  3. “需要 O(1) 额外空间的统计类问题” —— 如求数组的众数（使用摩尔投票法）等。  
- **一句话总结**：**“先把树排好队（中序），再顺着队伍一次遍历，统计连续相同的次数”。**

---

## 反思

- **第一反应**：直接把所有节点的值放进哈希表计数——最自然的“遍历+统计”。  
- **最容易踩的坑**：  
  1. **递归栈溢出**：树极端不平衡时递归深度可能达到 `10⁴`，在某些语言或环境会导致栈溢出。可以改写为显式的 **栈迭代** 中序遍历。  
  2. **第一次访问时 `prev_val` 为 `None`**，需要单独处理，否则会把计数误认为是连续。  
  3. **返回结果的顺序**：题目说“任意顺序”，所以不必额外排序，只要把收集到的众数直接返回即可。  
- **下次思路**：一看到 “BST + 统计” 的题目，先检查能否利用 **中序遍历的有序性**，把“统计”与“遍历”合二为一，尽量降低空间消耗。