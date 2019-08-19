# #538. 将 BST 转换为更大树 / Convert BST to Greater Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/convert-bst-to-greater-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed to the original key plus the sum of all keys greater than the original key in BST.
As a reminder, a binary search tree is a tree that satisfies these constraints:
Note: This question is the same as 1038: https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/

**Examples**

**Example 1:**

```
Input: root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
Output: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
```

**Example 2:**

```
Input: root = [0,null,1]
Output: [1,null,1]
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- -104 <= Node.val <= 104
- All the values in the tree are unique.
- root is guaranteed to be a valid binary search tree.

---

## 题目（中文翻译）

给定一棵二叉搜索树（Binary Search Tree，BST）的根节点 `root`，将其转换为一棵**更大树（Greater Tree）**，使得原 BST 中每个键（key）的值都被替换为 **原键值 加上 BST 中所有大于该键的键值之和**。

> 提示：二叉搜索树是一种满足以下约束的树结构：  
> - 对于任意节点，其左子树中所有节点的键值均小于该节点的键值；  
> - 其右子树中所有节点的键值均大于该节点的键值；  
> - 左、右子树本身也必须是二叉搜索树。

**示例 1**  

**示例 2**  

**约束条件**  
- 树中节点的数量在 `[0, 10^4]` 的范围内。  
- `-10^4 <= Node.val <= 10^4`。  
- 树中所有键值均唯一。  
- `root` 保证是一棵合法的二叉搜索树。  

**说明**：本题与 LeetCode 第 1038 题相同，链接：https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/  

---  

### 示例

**示例 1**  
```
Input: root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
Output: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
```

**示例 2**  
```
Input: root = [0,null,1]
Output: [1,null,1]
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**先把整棵树的所有节点值收集起来**，因为二叉搜索树（BST）左子树的所有值都比根小，右子树的所有值都比根大。  
1. 用一次遍历（比如前序/中序/后序都行）把所有节点的 `val` 放进一个列表 `vals`。这一步相当于把树“摊平”，就像把一本字典的所有词条都写在一张纸上。  
2. 对列表进行排序（BST 的中序遍历本身就是升序的，如果直接用中序遍历可以省掉排序这一步）。  
3. 对排好序的列表计算**后缀和**（从右往左累计），得到每个数对应的“它右边所有更大的数之和”。这一步可以类比为：在字典里查到某个词后，想知道它后面所有词的页码之和。  
4. 再次遍历树，把每个节点的值替换为 **原值 + 后缀和**（不包括自身）。如果在步骤 2 中已经把每个原值映射到了对应的后缀和，就可以直接查表（哈希表）得到答案。  

为什么这样能得到正确答案？  
- BST 的中序遍历得到的序列恰好是从小到大的有序序列。  
- 对每个位置 `i`，后缀和 `suffix[i]` 正好是所有 **大于** `vals[i]` 的节点值之和。  
- 把 `vals[i] + suffix[i]` 赋回对应的节点，即完成了“原值 + 所有更大值之和”。  

**时间/空间复杂度**（用最朴素的实现方式）  
- 第一次遍历收集节点：`O(n)`  
- 对列表排序：`O(n log n)`（如果直接用中序遍历得到有序列表，这一步可以省掉）  
- 计算后缀和：`O(n)`  
- 第二次遍历把新值写回树：`O(n)`  
- **总时间**：`O(n log n)`（或 `O(n)` 只要用中序遍历）  
- **空间**：我们需要存放所有节点值的列表以及哈希映射，都是 `O(n)`。  

如果不利用 BST 的有序特性，而是对每个节点都去遍历整棵树去求“比我大的所有节点之和”，时间会退化到 `O(n²)`，这也是最笨的暴力写法。下面给出这种 `O(n²)` 的实现，帮助大家体会为什么要优化。

#### 代码（Python）  
```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def collect_nodes(root, nodes):
    """前序遍历把所有节点对象放进列表 nodes（这里保存的是指针）"""
    if not root:
        return
    nodes.append(root)          # 关键行：把当前节点加入列表
    collect_nodes(root.left, nodes)
    collect_nodes(root.right, nodes)


def bst_to_greater_tree_brute(root):
    """
    暴力版：对每个节点都遍历整棵树求大于它的所有节点之和 → O(n²)
    """
    if not root:
        return None

    # 1️⃣ 把所有节点对象收集到一个列表中
    all_nodes = []
    collect_nodes(root, all_nodes)   # 这里的 all_nodes 长度 = 树的节点数 n

    # 2️⃣ 对每个节点，遍历一次整棵树求“大于它的值之和”
    for node in all_nodes:
        greater_sum = 0
        for other in all_nodes:          # 这里是 O(n) 的内层循环
            if other.val > node.val:     # 只加比当前节点大的值
                greater_sum += other.val
        node.val += greater_sum           # 把原值 + 大于它的所有值写回节点

    return root
```

#### 复杂度  
- **时间复杂度**：`O(n²)` —— 对每个节点 (`n` 次) 都要遍历全部节点 (`n` 次)，相当于两层嵌套的循环。可以把 `n²` 想象成“如果树有 10,000 个节点，算法会做大约 1 亿 次比较”。  
- **空间复杂度**：`O(n)` —— 需要一个列表保存所有节点的引用，额外的递归栈深度为 `O(h)`（`h` 为树高），最坏情况下 `h = n`，但一般我们只算列表的 `O(n)`。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于重复遍历整棵树**。我们其实不需要每次都去找“大于我的节点”，只要在一次遍历过程中把“已经遍历过的更大节点的累计和”记下来，就能直接得到答案。  

BST 的一个重要特性是：**右子树的所有节点值都比根大，左子树的所有节点值都比根小**。如果我们**先访问右子树 → 再访问根 → 最后访问左子树**，这就是“逆中序遍历”。在这种顺序下，遍历到的节点值是从大到小递减的。  

设 `acc` 为“当前遍历过的所有节点值之和”。  
- 当我们第一次进入最右侧的叶子节点时，`acc = 0`，因为还没有比它更大的节点。  
- 访问完这个节点后，把它的值加到 `acc` 中（`acc += node.val`），随后再访问它的左子树。  
- 当我们访问左子树的某个节点时，`acc` 已经包含了**所有比它大的节点的值**，于是只要把 `acc` 加到该节点的原值上，就得到了“原值 + 更大节点之和”。  

这就是**递归版的“右根左”遍历**，或用显式栈实现的**迭代版**。核心思想只有一个：**在遍历过程中维护一个全局累加和**。  

下面把这个思路一步步拆开：  

1. **逆中序遍历**（右 → 根 → 左）保证我们每次看到的节点都是当前未处理的最大值。  
2. 用一个变量 `self.sum_so_far`（或外部变量 `total`) 累计已经处理过的节点值。  
3. 对每个节点执行 `node.val += self.sum_so_far`，再把 `node.val` 加到 `self.sum_so_far` 中，准备给更小的节点使用。  

这只需要一次遍历，时间是线性的，额外空间只用递归栈（树高 `h`），在平衡树情况下是 `O(log n)`，最坏情况下是 `O(n)`（链状树）。  

#### 代码（Python）  

**递归实现（最直观）**  
```python
# Definition 同上
class Solution:
    def __init__(self):
        # 用实例属性保存累计和，递归调用之间可以共享
        self.sum_so_far = 0

    def convertBST(self, root: TreeNode) -> TreeNode:
        """
        逆中序遍历（右 -> 根 -> 左），在遍历过程中累计和
        """
        self._reverse_inorder(root)
        return root

    def _reverse_inorder(self, node: TreeNode):
        if not node:
            return
        # 先递归右子树，保证先处理比当前节点大的值
        self._reverse_inorder(node.right)          # 关键行：右子树先走

        # 访问当前节点：把累计的更大值加进去
        node.val += self.sum_so_far                 # 关键行：更新节点值
        self.sum_so_far = node.val                  # 关键行：更新累计和

        # 最后递归左子树，处理更小的节点
        self._reverse_inorder(node.left)           # 关键行：左子树后走
```

**迭代实现（用显式栈）**  
```python
class SolutionIter:
    def convertBST(self, root: TreeNode) -> TreeNode:
        """
        用栈模拟逆中序遍历，避免递归深度过大
        """
        total = 0                 # 累计和
        stack = []
        node = root

        while stack or node:
            # 一直往右走，把右子树压栈
            while node:
                stack.append(node)   # 关键行：把节点压入栈
                node = node.right

            # 栈顶弹出，开始处理
            node = stack.pop()
            total += node.val        # 先把当前值加到累计和
            node.val = total         # 再把累计和写回节点

            # 转向左子树继续
            node = node.left

        return root
```

#### 复杂度  
- **时间复杂度**：`O(n)` —— 每个节点只被访问一次（一次递归或一次弹栈），相当于“遍历一次树”。比暴力的 `O(n²)` 快了很多。  
- **空间复杂度**：`O(h)` —— 递归版需要调用栈深度等于树的高度 `h`；迭代版需要显式栈同样最多存 `h` 个节点。对于平衡 BST，`h ≈ log₂ n`，可以想象成“只需要几层楼的楼梯”。最坏情况下（完全倾斜的链）`h = n`，但仍然比 `O(n)` 的额外列表要省空间。  

---

## 心得  

- **核心技巧**：**逆中序遍历 + 累计和**。利用 BST 的有序性，只要一次遍历就能把“所有更大的节点之和”累加到当前节点。  
- **适用的题型**  
  1. “把 BST 每个节点改为左子树所有节点之和” → 需要正序中序遍历累计左侧和。  
  2. “把 BST 每个节点改为子树节点值的总和” → 可以用后序遍历累计子树和。  
  3. “将数组转为前缀和 / 后缀和” → 思路相同，只是数据结构换成了线性数组。  
- **一句话总结解题钥匙**：**把“从大到小”或“从小到大”的顺序固定下来，然后在遍历时把已经处理过的累计值直接加到当前元素上**。  

---

## 反思  

- **第一反应**：看到 “BST + 更大节点之和”，立刻想到“中序遍历得到有序序列”，于是想先把所有值取出来再做后缀和。  
- **最容易踩的坑**  
  1. **递归深度**：极端不平衡的 BST 可能导致递归栈溢出，面试时可以准备迭代版。  
  2. **负数节点**：累计和也可能是负数，不能把 “只加正数” 当成前提。  
  3. **空树**：`root` 为 `None` 时直接返回 `None`，否则代码会在 `node.right` 上报错。  
- **下次遇到同类题**：第一步先思考 **“是否可以把问题转化为一次遍历中累计某个方向的和？”**，如果答案是 Yes，就尝试 **中序 / 逆中序 / 前序 / 后序** 中的合适顺序来实现。