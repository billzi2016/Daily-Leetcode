# #449. 序列化与反序列化二叉搜索树 / Serialize and Deserialize BST

> 难度：中等 · 标签：String、Tree、Depth-First Search、Breadth-First Search、Design、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/serialize-and-deserialize-bst/)

---

## 题目（英文原版）

**Description**

Serialization is converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.
Design an algorithm to serialize and deserialize a binary search tree. There is no restriction on how your serialization/deserialization algorithm should work. You need to ensure that a binary search tree can be serialized to a string, and this string can be deserialized to the original tree structure.
The encoded string should be as compact as possible.

**Examples**

**Example 1:**

```
Input: root = [2,1,3]
Output: [2,1,3]
```

**Example 2:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- 0 <= Node.val <= 104
- The input tree is guaranteed to be a binary search tree.

---

## 题目（中文翻译）

序列化（serialization）是将数据结构或对象转换为比特序列的过程，以便可以将其存储到文件或内存缓冲区，或通过网络连接传输，并在相同或其他计算机环境中重新构建。

设计一种算法来序列化（serialize）和反序列化（deserialize）二叉搜索树（BST）。对你的序列化/反序列化算法没有任何限制。你需要确保一棵二叉搜索树可以被序列化为字符串，并且该字符串能够被反序列化回原始的树结构。

编码后的字符串应尽可能紧凑。

示例 1:

示例 2:

约束条件：
- 树中节点的数量范围为 \[0, 10⁴\]。
- 0 ≤ Node.val ≤ 10⁴。
- 输入的树保证是二叉搜索树。  

示例：

示例 1:  
Input: root = [2,1,3]  
Output: [2,1,3]  

示例 2:  
Input: root = []  
Output: []

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接、最“笨”的办法是把二叉树的结构完整地写出来。  
一种常见的写法是 **层序遍历（BFS）**，把每一层从左到右的节点依次放进列表，同时把空子树用特殊符号（比如 `#`）占位。  
- **数据结构**：我们把树看成一本字典，**键** 是节点在层序遍历中的位置，**值** 是节点的数值或 `#`（空位），就像查字典时先定位页码，再看具体单词。  
- **为什么正确**：层序遍历把树的每一层完整记录下来，空位也记录，所以只要把这个序列再按照同样的顺序读回来，就能恢复出原来的结构。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """暴力版：使用层序遍历 + 空位标记"""
    
    def serialize(self, root: TreeNode) -> str:
        """把树转换成字符串"""
        if not root:
            return ""                     # 空树直接返回空串

        from collections import deque
        q = deque([root])                # 队列实现层序遍历
        vals = []                        # 用来收集序列化后的节点值

        while q:
            node = q.popleft()
            if node:
                vals.append(str(node.val))   # 记录真实节点的值
                q.append(node.left)          # 左子树入队
                q.append(node.right)         # 右子树入队
            else:
                vals.append('#')              # 用 # 表示空位

        # 为了避免尾部大量的 #，可以把最后的 # 全部去掉（可选）
        while vals and vals[-1] == '#':
            vals.pop()

        return ','.join(vals)            # 用逗号把所有元素拼成一个字符串

    def deserialize(self, data: str) -> TreeNode:
        """把字符串恢复成原来的树"""
        if not data:
            return None                  # 空串对应空树

        vals = data.split(',')           # 把字符串拆分成列表
        from collections import deque
        q = deque()                      # 用队列帮助逐层构造树

        root = TreeNode(int(vals[0]))    # 第一个元素一定是根节点
        q.append(root)
        i = 1                            # 下一个要处理的列表下标

        while q:
            node = q.popleft()
            # 处理左子树
            if i < len(vals) and vals[i] != '#':
                node.left = TreeNode(int(vals[i]))
                q.append(node.left)
            i += 1
            # 处理右子树
            if i < len(vals) and vals[i] != '#':
                node.right = TreeNode(int(vals[i]))
                q.append(node.right)
            i += 1

        return root
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  这里的 `n` 是树的节点数。遍历一次树（序列化）和一次队列重建（反序列化）都只会访问每个节点一次。用“大白话”说，就是如果树里有 1000 个节点，代码大约会跑 1000 次基本操作。  
- **空间复杂度**：`O(n)`  
  需要保存序列化后的 `vals` 列表以及 BFS 时的队列，这些都和节点数成正比。  

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **“空位标记”**：  
- 为了完整记录结构我们必须额外存很多 `#`，这会让序列化结果比实际需要的长。  
- 对于 **二叉搜索树（BST）**，我们还有一个隐藏的性质：**左子树的所有节点值都 < 根节点值，右子树的所有节点值都 > 根节点值**。  
  利用这个性质，我们可以只记下节点的 **前序遍历**（根 → 左 → 右），而不需要任何空位标记。  
  前序序列天然满足“根在前，左子树所有值比根小，右子树所有值比根大”。只要在反序列化时 **按照这个顺序并用上下界限制**，就能唯一地恢复出原树。  

**关键算法——带上下界的递归**  
1. 把前序序列保存为一个列表 `pre`，并用一个全局指针 `idx` 表示当前要取哪个值。  
2. 递归函数 `build(lower, upper)` 表示“在 `(lower, upper)` 区间内可以放的节点”。  
   - 如果 `pre[idx]` 不在区间内，说明当前子树为空，直接返回 `None`。  
   - 否则创建节点 `node = TreeNode(pre[idx])`，`idx += 1`，递归构造左子树（区间 `(lower, node.val)`），再递归构造右子树（区间 `(node.val, upper)`）。  
3. 初始调用 `build(-inf, +inf)`，即可得到完整的 BST。  

这种方法不需要任何 `#`，序列化字符串的长度恰好等于节点数（每个节点一个整数），是 **最紧凑** 的方案。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    """最优版：利用 BST 的有序性，仅保存前序遍历"""
    
    def serialize(self, root: TreeNode) -> str:
        """前序遍历 + 用逗号分隔，得到最简字符串"""
        vals = []

        def preorder(node: TreeNode):
            if not node:
                return                # BST 不需要记录空位，直接返回
            vals.append(str(node.val))  # 记录根节点
            preorder(node.left)         # 递归左子树
            preorder(node.right)        # 递归右子树

        preorder(root)
        return ','.join(vals)           # 例子： "2,1,3"

    def deserialize(self, data: str) -> TreeNode:
        """利用前序序列和 BST 区间约束恢复树结构"""
        if not data:
            return None

        pre = list(map(int, data.split(',')))  # 把字符串转成整数列表
        self.idx = 0                           # 全局指针，指向下一个待使用的值

        import math
        def build(lower: int, upper: int) -> TreeNode:
            """在 (lower, upper) 区间内构造子树"""
            if self.idx == len(pre):
                return None                     # 已经用完所有节点
            val = pre[self.idx]
            if not (lower < val < upper):       # 当前值不在合法区间，说明子树为空
                return None

            # 合法 → 创建节点并递归构造左右子树
            self.idx += 1
            node = TreeNode(val)
            node.left = build(lower, val)       # 左子树的上界是当前节点值
            node.right = build(val, upper)      # 右子树的下界是当前节点值
            return node

        return build(-math.inf, math.inf)       # 初始区间是全局无界
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  前序遍历一次（序列化） + 递归一次（反序列化），每个节点只被访问一次。  
- **空间复杂度**：`O(n)`  
  需要保存前序列表 `pre`（长度等于节点数）以及递归栈的深度。递归栈最坏情况是树呈线性（高度 `n`），所以也是 `O(n)`。  
  与暴力解相比，**输出字符串的长度更短**（没有 `#`），这正是题目要求的“尽可能紧凑”。

---

## 心得

- **核心技巧**：利用 BST 的 **值的有序性** 进行无空位的前序序列化，并在反序列化时使用 **上下界递归** 还原树结构。  
- **适用场景**：  
  1. 任何需要 **紧凑存储 BST** 的场景（如数据库、网络传输）。  
  2. 类似的 “只要满足某种单调关系的树” 也可以使用相同思路，例如 **二叉搜索堆**（BST + 堆序）。  
  3. 其它需要 **依据顺序约束重建结构** 的题目，如 “从前序/后序序列恢复唯一的 BST”。  
- **一句话总结**：  
  *只要记下根节点的值，左子树全比根小、右子树全比根大——利用这条“大小界限”，就能省去所有空位标记，实现最紧凑的序列化。*

---

## 反思

- **第一反应**：看到 “BST + 序列化” 立刻想到层序遍历加 `#`，因为这种写法对所有二叉树都通用，最安全。  
- **最容易踩的坑**：  
  1. **边界条件**：反序列化时如果不检查 `idx` 是否越界，递归会访问空列表导致错误。  
  2. **区间判断**：要使用严格的 `<`（而不是 `<=`），否则相同的值会导致歧义（题目保证值唯一，但严格写法更稳健）。  
  3. **整数范围**：上下界选 `-inf / +inf` 防止溢出；直接用 `-10**9`、`10**9` 也行，但不够通用。  
- **下次思路**：  
  1. 首先判断 **数据结构的特殊属性**（这里是 BST 的有序性）。  
  2. 再思考 **如何用最少的信息表达完整结构**（前序 + 区间）。  
  3. 最后实现时，注意 **递归边界** 与 **全局指针的同步**，防止遗漏或越界。