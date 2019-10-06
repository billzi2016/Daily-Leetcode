# #606. 从二叉树构造字符串 / Construct String from Binary Tree

> 难度：中等 · 标签：String、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/construct-string-from-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root node of a binary tree, your task is to create a string representation of the tree following a specific set of formatting rules. The representation should be based on a preorder traversal of the binary tree and must adhere to the following guidelines:

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4]
Output: "1(2(4))(3)"
Explanation: Originally, it needs to be "1(2(4)())(3()())", but you need to omit all the empty parenthesis pairs. And it will be "1(2(4))(3)".
```

**Example 2:**

```
Input: root = [1,2,3,null,4]
Output: "1(2()(4))(3)"
Explanation: Almost the same as the first example, except the () after 2 is necessary to indicate the absence of a left child for 2 and the presence of a right child.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，请按照特定的格式规则构造该树的字符串表示。字符串应基于二叉树的先序遍历（preorder traversal），并满足以下要求：

1. 对每个节点，先写出节点的值 `val`。  
2. 若该节点存在左子树，则在节点值后紧跟一对圆括号 `(` `)`，其中括号内是左子树的字符串表示；若左子树为空且右子树不为空，则必须保留空的左子树括号 `()`，以便能够正确解析右子树。  
3. 若该节点存在右子树，则在左子树（或空的 `()`）之后再紧跟一对圆括号 `(` `)`，其中括号内是右子树的字符串表示。  
4. 当左右子树均为空时，可以省略这对括号，即不输出任何括号。  

**示例 1**  
```
输入: root = [1,2,3,4]
输出: "1(2(4))(3)"
解释: 完整的形式应该是 "1(2(4)())(3()())"，但所有空的括号对都需要省略，最终得到 "1(2(4))(3)"。
```

**示例 2**  
```
输入: root = [1,2,3,null,4]
输出: "1(2()(4))(3)"
解释: 与示例 1 类似，只是 `2` 的左子树为空，需要保留 `()` 来表明左子树缺失，而右子树存在。
```

**约束条件**  
- 树中节点的数量在区间 `[1, 10^4]` 内。  
- `-1000 <= Node.val <= 1000`   (其中 `Node.val` 为节点的值)。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把整棵树的结构全部写出来**，再把“多余的空括号”删掉。  
具体步骤如下  

1. **先把树的每个节点都写成** `value(left)(right)` 的形式。  
   - `value`：当前节点的整数值。  
   - `left`、`right`：递归得到的左子树、右子树的字符串。  
   - **即使左/右子树为空，也要写成 `()`**（相当于把空节点也当作一个“占位符”）。  
2. 这样得到的字符串一定是完整的，和题目要求的“原始”形式完全一致。  
3. 最后 **把所有出现的 `()`（空括号对）全部删除**，因为题目说可以省略这些没有任何信息的括号。  

> **类比**：把哈希表想成一本字典，`key` 是单词，`value` 是解释。这里我们把每个节点想成一本“子字典”，即使这本子字典里什么也没有（空子树），我们仍然写上一对空括号 `()` 作为占位，最后再把这些“空页”去掉。  

**为什么正确**  
- 第一步把树的每一种可能的结构都完整写出来，保证不漏任何节点。  
- 第二步只删掉**完全没有内容**的 `()`，不会影响到实际有子树的括号对。于是得到的就是题目要求的最简形式。  

**时间/空间复杂度**  
- 在递归构造字符串的过程中，我们使用了 **大量的字符串拼接**（`a + b`）。在 Python 中，每一次拼接都会创建一个新字符串，旧字符串会被复制一次。若树有 `n` 个节点，最坏情况下会产生约 `1 + 2 + … + n = O(n²)` 次字符复制。  
- 递归调用本身的栈深度最多是树的高度 `h`，在最坏的单链树情况下 `h = n`，但这里的主要瓶颈是字符串复制导致的 **时间复杂度 O(n²)**。  
- 额外空间主要是递归栈和临时字符串，最坏也是 **O(n)**（保存整棵树的完整表示）。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree2str_bruteforce(root: TreeNode) -> str:
    """
    暴力解法：先完整生成所有括号，包括空的 ()，再统一删除空括号。
    """
    if not root:
        return ""

    # 1. 递归得到左、右子树的完整表示（即使为空也会返回 ""）
    left = tree2str_bruteforce(root.left)
    right = tree2str_bruteforce(root.right)

    # 2. 按照 value(left)(right) 的格式拼接
    #    注意：即使 left/right 为空，也要写成 ()
    cur = str(root.val) + "(" + left + ")" + "(" + right + ")"

    # 3. 把所有的空括号对 () 删除
    #    这里用 while 循环是因为删除一次后可能出现新的 ()，例如 "a(()())"
    while "()" in cur:
        cur = cur.replace("()", "")

    return cur
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：每一次字符串拼接都会把已有字符复制一遍，累计下来大约是 1+2+…+n 次复制。  
- **空间复杂度**：`O(n)`  
  - 解释：递归栈深度最坏是 `n`，以及保存最终字符串需要 `O(n)` 的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**真正耗时的地方是把所有空括号写进去再删掉**。如果我们在生成字符串的过程中**直接跳过不必要的空括号**，就能把时间降到线性。  

关键点如下  

1. **先序遍历（根 → 左 → 右）**：因为题目要求的顺序正好是先序。  
2. **何时需要写 '(' ')'**  
   - **左子树**：  
     - 若左子树 **存在**，必须写 `(` + 左子树字符串 + `)`。  
     - 若左子树 **不存在**，**且右子树也不存在**，则可以直接省略左括号对（因为整棵子树为空）。  
   - **右子树**：  
     - 若右子树 **存在**，必须写 `(` + 右子树字符串 + `)`。  
     - 若右子树 **不存在**，可以省略右括号对。  
   - **特殊情况**：如果左子树为空但右子树**非空**，**必须写 `()`** 来占位，表明左边真的没有节点，而右边有。否则仅写右子树会导致结构歧义。  
3. **递归实现**：把上述规则直接写进递归函数中，返回每个子树的最简字符串。  
4. **不需要额外的后处理**，因为每一步都已经保证最简。  

> **类比**：想象你在写一棵家谱。每个人都有父亲和母亲（左、右子树）。如果一个人没有父亲（左子树），但有母亲（右子树），你必须写 `()` 来说明“这里真的没有父亲”。如果两边都没有亲人，自然不写任何括号。  

**复杂度分析**  
- 每个节点只被访问一次，且在访问时只做了常数次的字符串拼接（使用列表收集再一次性 `join`），所以 **时间是 O(n)**。  
- 递归栈深度最多是树的高度 `h`，最坏是 `O(n)`，但不需要额外的数组，空间为 **O(h)**（即递归栈），在平衡树时是 `O(log n)`。  

#### 代码（Python）  

```python
def tree2str(root: TreeNode) -> str:
    """
    最优解：在遍历的同时直接构造最简字符串，避免后处理空括号。
    """
    if not root:
        return ""

    # 使用列表收集字符，最后一次性 join，避免大量的临时字符串复制
    parts = []

    def dfs(node: TreeNode):
        if not node:
            return
        # 1. 写根节点的值
        parts.append(str(node.val))

        # 2. 处理左子树
        if node.left or node.right:          # 只要左子树存在，或者右子树存在（需要占位）
            parts.append('(')
            if node.left:                     # 左子树非空，递归写入
                dfs(node.left)
            # 左子树为空但右子树非空时，这里什么也不加，形成 "()"
            parts.append(')')

        # 3. 处理右子树
        if node.right:                        # 右子树非空才写
            parts.append('(')
            dfs(node.right)
            parts.append(')')

    dfs(root)
    return ''.join(parts)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：每个节点只访问一次，列表的 `append` 是 O(1) 的操作，最终 `join` 也是线性的。相比暴力解省去了大量的字符串复制。  
- **空间复杂度**：`O(h)`（递归栈）  
  - 解释：最坏情况下树退化为链表，递归深度为 `n`，但这已经是必须的栈空间；在平衡二叉树中只有 `log n`。  

---

## 心得  

- **核心技巧**：**先序遍历 + 按需添加括号**，尤其要注意“左空右非空必须写 `()`”。  
- **适用的题型**  
  1. **二叉树序列化**（如 LeetCode 297 Serialize and Deserialize Binary Tree）  
  2. **树的括号表示**（如 LeetCode 226 Invert Binary Tree 的打印）  
  3. **树的前序/中序/后序表达式**（如表达式树转字符串）  
- **一句话总结**：  
  > 只在“需要表达结构信息”时才写括号，省去所有多余的 `()`，即可在一次遍历中得到最简字符串。  

---

## 反思  

- **第一反应**：直接写递归，把每个节点的左、右子树都用 `()` 包起来，然后想办法把空的 `()` 去掉。  
- **最容易踩的坑**  
  1. **左子树为空但右子树存在** 时忘记写 `()`，导致生成的字符串与题目要求不匹配。  
  2. 使用 `+` 进行字符串拼接导致 **时间超限**（`O(n²)`）。  
  3. 边界情况：只有根节点、只左子树、只右子树都要分别验证。  
- **下次遇到同类题**，第一步应该先**明确哪些结构信息是必须保留的**（如占位的空括号），再**在递归/迭代的同时直接输出**，避免事后再做“删减”。