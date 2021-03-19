# #1261. 在受污染的二叉树中查找元素 / Find Elements in a Contaminated Binary Tree

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Design、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/find-elements-in-a-contaminated-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree with the following rules:
Now the binary tree is contaminated, which means all treeNode.val have been changed to -1.
Implement the FindElements class:

**Examples**

**Example 1:**

```
Input
["FindElements","find","find"]
[[[-1,null,-1]],[1],[2]]
Output
[null,false,true]
Explanation
FindElements findElements = new FindElements([-1,null,-1]); 
findElements.find(1); // return False 
findElements.find(2); // return True
```

**Example 2:**

```
Input
["FindElements","find","find","find"]
[[[-1,-1,-1,-1,-1]],[1],[3],[5]]
Output
[null,true,true,false]
Explanation
FindElements findElements = new FindElements([-1,-1,-1,-1,-1]);
findElements.find(1); // return True
findElements.find(3); // return True
findElements.find(5); // return False
```

**Example 3:**

```
Input
["FindElements","find","find","find","find"]
[[[-1,null,-1,-1,null,-1]],[2],[3],[4],[5]]
Output
[null,true,false,false,true]
Explanation
FindElements findElements = new FindElements([-1,null,-1,-1,null,-1]);
findElements.find(2); // return True
findElements.find(3); // return False
findElements.find(4); // return False
findElements.find(5); // return True
```

**Constraints**

- TreeNode.val == -1
- The height of the binary tree is less than or equal to 20
- The total number of nodes is between [1, 104]
- Total calls of find() is between [1, 104]
- 0 <= target <= 106

---

## 题目（中文翻译）

给定一棵二叉树（binary tree），其原始节点值满足以下规则：

- 根节点的值为 `0`。
- 任意节点 `node` 的左子节点（left child）值为 `2 * node.val + 1`，右子节点（right child）值为 `2 * node.val + 2`。

现在这棵二叉树被 **污染**（contaminated），即所有 `node.val` 都被改成了 `-1`。

请实现 `FindElements` 类：

- `FindElements(TreeNode* root)`：构造函数，接收被污染的二叉树根节点 `root`，并恢复树中每个节点的原始值。
- `bool find(int target)`：返回 `true` 当且仅当在恢复后的树中存在值为 `target` 的节点。

---

### 示例

#### 示例 1
**输入**
```
["FindElements","find","find"]
[[[-1,null,-1]],[1],[2]]
```
**输出**
```
[null,false,true]
```
**解释**
```java
FindElements findElements = new FindElements([-1,null,-1]); 
findElements.find(1); // 返回 false
findElements.find(2); // 返回 true
```

#### 示例 2
**输入**
```
["FindElements","find","find","find"]
[[[-1,-1,-1,-1,-1]],[1],[3],[5]]
```
**输出**
```
[null,true,true,false]
```
**解释**
```java
FindElements findElements = new FindElements([-1,-1,-1,-1,-1]);
findElements.find(1); // 返回 true
findElements.find(3); // 返回 true
findElements.find(5); // 返回 false
```

#### 示例 3
**输入**
```
["FindElements","find","find","find","find"]
[[[-1,null,-1,-1,null,-1]],[2],[3],[4],[5]]
```
**输出**
```
[null,true,false,false,true]
```
**解释**
```java
FindElements findElements = new FindElements([-1,null,-1,-1,null,-1]);
findElements.find(2); // 返回 true
findElements.find(3); // 返回 false
findElements.find(4); // 返回 false
findElements.find(5); // 返回 true
```

---

### 约束条件

- 所有 `TreeNode.val == -1`（即树已被污染）。
- 二叉树的高度（height） ≤ 20。
- 树中节点总数在 `[1, 10^4]` 之间。
- `find` 方法的调用次数在 `[1, 10^4]` 之间。
- `0 ≤ target ≤ 10^6`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出的二叉树所有节点的值都被污染成 `-1`，但我们知道原本的值满足以下规则：

- 根节点的值是 `0`。  
- 若某节点的值为 `x`，则左孩子的值是 `2*x + 1`，右孩子的值是 `2*x + 2`。

最直接的想法是：**每次调用 `find(target)` 时，从根节点出发，按照二叉树的结构实时计算出每个节点的真实值**，一边遍历一边检查是否出现了 `target`。  
这相当于把「恢复」的过程和「查找」的过程混在一起。

> **类比**：把二叉树想成一条森林小路，根节点是入口。我们每次要找一块特定的石头（`target`），就从入口一步步往下走，沿途记录每块石头的编号（节点值），看是否能恰好等于目标编号。

**为什么正确**  
因为恢复规则是唯一且确定的：只要知道父节点的值，就能唯一算出左/右孩子的值。因此在遍历的过程中，一旦我们把父节点的真实值算出来，子节点的真实值就一定是 `2*parent+1`（左）或 `2*parent+2`（右），不可能出错。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 这里最开始都是 -1，后面会在遍历时“恢复”
        self.left = left
        self.right = right


class FindElements:
    def __init__(self, root: TreeNode):
        """构造函数，只保存根节点，恢复过程交给 find() 完成"""
        self.root = root

    def _dfs(self, node: TreeNode, cur_val: int, target: int) -> bool:
        """
        深度优先遍历，实时恢复节点值并与 target 对比。
        返回 True 表示在子树中找到了目标。
        """
        if not node:
            return False

        # 恢复当前节点的真实值
        node.val = cur_val
        if cur_val == target:          # 找到目标
            return True

        # 继续向左、右子树搜索
        left_found = self._dfs(node.left, 2 * cur_val + 1, target)
        if left_found:
            return True
        right_found = self._dfs(node.right, 2 * cur_val + 2, target)
        return right_found

    def find(self, target: int) -> bool:
        """每次查询都重新遍历整棵树，时间开销较大"""
        return self._dfs(self.root, 0, target)
```

#### 复杂度  

- **时间复杂度**：`O(N)`（每次 `find` 最坏需要遍历整棵树，`N` 为节点数）。  
  用大白话说，就是如果树有 10,000 个节点，我们每查询一次都要看 10,000 次，比较慢。
- **空间复杂度**：`O(H)`，递归栈的深度等于树的高度 `H`（≤20），可以视作常数级别的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次查询都要重新遍历整棵树**。  
其实，树的结构是固定的，恢复后的每个节点值也只会算一次。只要在构造函数里把所有真实值一次性算出来并保存下来，后面的 `find` 就可以 **O(1) 直接查询**。

实现思路分两步：

1. **恢复树并收集所有值**  
   - 使用一次 DFS（或 BFS）遍历整棵树。  
   - 进入一个节点时，根据父节点的值算出当前节点的真实值 `cur`（根为 `0`，左子 `2*parent+1`，右子 `2*parent+2`）。  
   - 把 `cur` 放进哈希集合 `self.valid`（相当于“字典”，键是节点值，查找时直接返回是否存在）。  
   - 同时把 `node.val` 设为 `cur`（可选，题目没有要求恢复后再使用树）。

2. **查询**  
   - `find(target)` 只要检查 `target` 是否在 `self.valid` 中即可，时间是常数 `O(1)`。

> **类比**：把树想成一本已经印好页码的目录册。构造函数一次性把所有页码（节点值）写进一本“速查本”（哈希集合）。以后要找第几页，只要在速查本里翻一眼（哈希查找），不必再跑遍整个目录。

**为什么正确**  
- 恢复规则唯一，遍历一次即可得到所有真实值。  
- 哈希集合的特性是 **查找、插入均摊时间 O(1)**，所以后续查询必然返回正确答案且效率极高。

#### 代码（Python）

```python
class FindElements:
    def __init__(self, root: TreeNode):
        """
        构造函数一次性恢复整棵树，并把所有合法的节点值存入集合 self.valid
        """
        self.valid = set()                 # 哈希集合，存放所有可以被找到的值
        self._recover(root, 0)             # 从根节点开始，根的真实值是 0

    def _recover(self, node: TreeNode, cur_val: int):
        """DFS 恢复节点值并收集到集合中"""
        if not node:
            return
        node.val = cur_val                 # 恢复当前节点的真实值（可选）
        self.valid.add(cur_val)            # 把值加入集合，后续查询用

        # 递归恢复左、右子树
        self._recover(node.left, 2 * cur_val + 1)   # 左子：2*x+1
        self._recover(node.right, 2 * cur_val + 2)  # 右子：2*x+2

    def find(self, target: int) -> bool:
        """只需要在集合中检查是否存在 target，时间 O(1)"""
        return target in self.valid
```

#### 复杂度  

- **时间复杂度**  
  - 构造阶段：`O(N)`，遍历一次所有节点（`N ≤ 10⁴`），每个节点只处理一次。  
  - 查询阶段：`O(1)`，哈希集合的查找是常数时间。  
  与暴力解相比，查询速度提升了数千倍（从遍历整棵树到只看一本速查本）。

- **空间复杂度**  
  - `O(N)` 用于存放集合 `self.valid`，需要保存每个节点的值。  
  - 递归栈深度仍为 `O(H)`（`H ≤ 20`），可以忽略不计。  
  - 用大白话说，就是我们用了额外的“记事本”把所有节点的编号记下来，占用的空间和树的大小成正比。

---

## 心得

- **核心技巧**：一次性遍历恢复（DFS/BFS） + 哈希集合快速查找。  
- **适用场景**  
  1. “预处理 + 多次查询” 的问题，例如 LeetCode *Design Add and Search Words Data Structure*（前缀树）中的批量构建。  
  2. “把树/图的状态映射到可哈希的标识” 的题目，如 *Find Duplicate Subtrees*（用序列化字符串存入集合）。  
- **一句话总结**：把所有可能的答案预先存进哈希集合，查询就能做到 **O(1)**。

---

## 反思

- **第一反应**：看到“恢复二叉树”和“查询”，本能地想到每次查询都直接遍历树——这就是暴力解。  
- **最容易踩的坑**  
  - **递归深度**：虽然树高 ≤ 20，但如果使用递归实现，需要确保不会因为 Python 默认递归深度限制（约 1000）而报错——这里安全。  
  - **忘记把根节点值设为 0**：根节点是唯一的起点，若误设成 `-1`，后面的计算全部错位。  
  - **集合存储的类型**：`target` 范围可达 `10⁶`，使用 `set` 而不是列表可以避免 O(target) 的空间浪费。  
- **下次类似题目第一步**：判断是否可以一次性 **预处理所有答案**（如遍历、序列化、哈希），把查询转化为常数时间操作。这样往往能把 “多次查询” 的瓶颈一次性解决。