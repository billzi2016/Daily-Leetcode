# #998. 最大二叉树 II / Maximum Binary Tree II

> 难度：中等 · 标签：Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-binary-tree-ii/)

---

## 题目（英文原版）

**Description**

A maximum tree is a tree where every node has a value greater than any other value in its subtree.
You are given the root of a maximum binary tree and an integer val.
Just as in the previous problem, the given tree was constructed from a list a (root = Construct(a)) recursively with the following Construct(a) routine:
Note that we were not given a directly, only a root node root = Construct(a).
Suppose b is a copy of a with the value val appended to it. It is guaranteed that b has unique values.
Return Construct(b).

**Examples**

**Example 1:**

```
Input: root = [4,1,3,null,null,2], val = 5
Output: [5,4,null,1,3,null,null,2]
Explanation: a = [1,4,2,3], b = [1,4,2,3,5]
```

**Example 2:**

```
Input: root = [5,2,4,null,1], val = 3
Output: [5,2,4,null,1,null,3]
Explanation: a = [2,1,5,4], b = [2,1,5,4,3]
```

**Example 3:**

```
Input: root = [5,2,3,null,1], val = 4
Output: [5,2,4,null,1,3]
Explanation: a = [2,1,5,3], b = [2,1,5,3,4]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 100].
- 1 <= Node.val <= 100
- All the values of the tree are unique.
- 1 <= val <= 100

---

## 题目（中文翻译）

一个最大二叉树（maximum tree）是指每个节点的值都严格大于其子树中所有其他节点的值。

给定一棵最大二叉树的根节点 `root`，以及一个整数 `val`。正如前一道题目所述，这棵树是由数组 `a` 通过递归构造函数 **Construct(a)** 构造得到的（`root = Construct(a)`），其构造过程如下：

```
Construct(a):
    if a is empty: return null
    max = maximum value in a
    node = new TreeNode(max)
    node.left = Construct(subarray of a left of max)   // 左子数组
    node.right = Construct(subarray of a right of max) // 右子数组
    return node
```

注意我们并没有直接得到数组 `a`，只知道根节点 `root = Construct(a)`。

设 `b` 为在数组 `a` 的末尾追加值 `val` 后得到的新数组。已保证 `b` 中的所有值仍然唯一。返回 `Construct(b)` 所得到的树的根节点。

## 示例

### 示例 1
**输入**  
`root = [4,1,3,null,null,2], val = 5`  

**输出**  
`[5,4,null,1,3,null,null,2]`  

**解释**  
原数组 `a = [1,4,2,3]`，在末尾追加 `val` 后得到 `b = [1,4,2,3,5]`，`Construct(b)` 的结果即为输出的树。

### 示例 2
**输入**  
`root = [5,2,4,null,1], val = 3`  

**输出**  
`[5,2,4,null,1,null,3]`  

**解释**  
原数组 `a = [2,1,5,4]`，追加后 `b = [2,1,5,4,3]`，返回 `Construct(b)`。

### 示例 3
**输入**  
`root = [5,2,3,null,1], val = 4`  

**输出**  
`[5,2,4,null,1,3]`  

**解释**  
原数组 `a = [2,1,5,3]`，追加后 `b = [2,1,5,3,4]`，返回 `Construct(b)`。

## 约束条件

- 树中节点的数量在 `[1, 100]` 之间。
- `1 <= Node.val <= 100`
- 树中所有节点的值互不相同。
- `1 <= val <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **最大二叉树** 重新“拆”成原来的数组 `a`，再把新值 `val` 加到数组尾部得到 `b`，最后按照题目给出的构造规则 `Construct(b)` 再建一棵树。

- **把树变成数组**  
  对最大二叉树做一次 **中序遍历**（左‑根‑右），恰好可以得到原始数组 `a`。可以把中序遍历想象成“把树展平”，就像把一本书的章节顺序读出来一样。

- **重新构造树**  
  现在有了数组 `b = a + [val]`，按照题目描述的递归规则：  
  1. 找到子数组里的最大值，建成根节点。  
  2. 左子数组递归构造左子树，右子数组递归构造右子树。  

  这一步就像 **“找字典里最大的单词”**（最大值）然后把它摆在最前面，剩下的左边的单词继续往左，右边的单词继续往右。

- **为什么一定对**  
  题目保证 `b` 中的所有值都是唯一的，且 `Construct` 的定义唯一确定了一棵树，所以只要我们严格按照定义去做，得到的树一定就是要求的答案。

- **时间/空间复杂度**  
  - 找最大值的过程需要遍历子数组一次，递归层数是树的高度（最坏会遍历每个子数组），导致 **时间复杂度是 O(n²)**。可以把 O(n²) 想象成“把 n 张纸每张都要再检查一次”。  
  - 我们需要保存中序遍历得到的数组以及递归栈，**空间复杂度是 O(n)**（n 为节点数）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# ---------- 暴力解 ----------
def insertIntoMaxTree_bruteforce(root: TreeNode, val: int) -> TreeNode:
    """
    1. 中序遍历得到原数组 a
    2. 在 a 末尾加上 val，得到 b
    3. 按照 Construct 规则从 b 重建树
    """
    # ① 中序遍历 → a
    def inorder(node: TreeNode, arr: list):
        if not node:
            return
        inorder(node.left, arr)   # 先左
        arr.append(node.val)      # 再根
        inorder(node.right, arr)  # 最后右

    a = []
    inorder(root, a)              # 把原树展平成数组 a

    # ② 把新值加到数组末尾
    b = a + [val]

    # ③ 递归构造最大二叉树
    def construct(nums: list) -> TreeNode:
        if not nums:               # 空子数组 → 空树
            return None
        # 找到子数组里的最大值及其下标
        max_val = max(nums)
        max_idx = nums.index(max_val)
        # 用最大值建根节点
        node = TreeNode(max_val)
        # 左右子数组递归构造左右子树
        node.left = construct(nums[:max_idx])
        node.right = construct(nums[max_idx + 1:])
        return node

    return construct(b)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 中序遍历 O(n)  
  - 每层递归都要扫描一次子数组找最大值，最坏情况（完全递归成链表）会出现 `1 + 2 + … + n = O(n²)` 次扫描。  
  - 用大白话说，就是“把每张纸都检查了好几遍”。

- **空间复杂度**：`O(n)`  
  - 用了一个数组保存原来的遍历顺序，长度为 n。  
  - 递归栈最深也不超过 n（树的高度），所以整体是线性空间。

---

### 2. 最优解

#### 思路  

暴力解的主要瓶颈在 **“每次都要遍历子数组找最大值”**。其实我们已经有了 **原来的最大二叉树**，只需要把新值 `val` **插入** 到合适的位置，而不必重新建整棵树。

**观察**：  
- `Construct(a)` 把数组的 **最大值** 放在根节点，左子树对应左侧子数组，右子树对应右侧子数组。  
- 由于 `val` 被 **追加到数组的最右端**，它只会影响原树的 **右侧路径**（右子树一直往右的那条链）。  
- 插入过程可以类比为 “在一条单向的链上插入一个新节点”，只要找到第一个比 `val` 小的节点，就把 `val` 挂在它的右边。

**具体步骤**：

1. **如果 `val` 大于根节点的值**，它就是新的全局最大值。按照构造规则，`val` 成为新根，原树变成左子树。  
   - 类比：把一本书的最大章节直接放到最前面，原来的全部章节变成它的左边（前置章节）。

2. **否则**，沿着 **右子树** 向下走（一直往右），直到遇到：
   - 当前节点的右孩子为空 **或**  
   - 右孩子的值 **小于** `val`。  

   此时 `val` 要插在这里：
   - 新建节点 `new = TreeNode(val)`。  
   - 把 `new.right` 指向原来的右孩子（如果右孩子比 `val` 小，它会成为 `new` 的右子树）。  
   - 把当前节点的右指针指向 `new`。  

   这一步相当于在链表的某个位置插入一个更大的节点，保持“右侧子树始终是原数组的后缀”。

**为什么正确**  
- 右侧路径恰好对应原数组的 **后缀**（从根的右子树一直往下的节点顺序等价于数组中根节点右边的所有元素）。  
- `val` 只会出现在这个后缀的最右端，唯一需要比较的就是它与后缀中各元素的大小关系。  
- 当 `val` 大于某个节点时，它必须成为该节点的 **父节点**（左子树保持不变），否则就只能挂在该节点的右侧，形成新的后缀结构。  

**核心数据结构**：**二叉树的指针**（左、右子树），以及 **单向遍历**（只沿右子树走）。不需要额外的数组或哈希表。

**时间复杂度**：只遍历了右侧路径，最坏情况是整棵树都是右倾的（链表），此时走完所有 `n` 个节点，**O(n)**。  
**空间复杂度**：只用了常数级的额外指针，**O(1)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# ---------- 最优解 ----------
def insertIntoMaxTree(root: TreeNode, val: int) -> TreeNode:
    """
    只在右侧路径上插入新节点，时间 O(n)，空间 O(1)。
    """
    # 1. val 成为新的全局最大值 → 新根
    if val > root.val:
        new_root = TreeNode(val)
        new_root.left = root          # 原树成为左子树
        return new_root

    # 2. 在右侧路径寻找插入位置
    cur = root
    while cur.right and cur.right.val > val:
        # 只要右孩子存在且 > val，说明 val 还不能挂在这里
        cur = cur.right

    # 3. 此时 cur.right 为 None 或者其值 < val，完成插入
    new_node = TreeNode(val)
    new_node.right = cur.right       # 原来的右子树（如果有）挂到 new_node 的右边
    cur.right = new_node             # 把 new_node 接到当前节点的右侧

    return root
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 最坏情况下需要遍历整棵树的右侧链（比如原树是递增的右倾树），这相当于检查了每个节点一次。  
  - 与暴力解的 `O(n²)` 相比，省掉了每层都要找最大值的重复扫描。

- **空间复杂度**：`O(1)`  
  - 只使用了几个临时指针 (`cur`, `new_node`)，不需要额外的数组或递归栈。  
  - 用大白话说，就是“只占用了几块桌面空间”，和节点数量无关。

---

## 心得

- **核心技巧**：**只在右子树上插入**，利用最大二叉树的构造特性把“追加到数组末尾”转化为“沿右侧链插入”。  
- **适用的题型**  
  1. **Maximum Binary Tree I**（给定数组直接构造最大二叉树）。  
  2. **Insert into a BST**（在二叉搜索树中插入），同样只需沿一条路径寻找插入点。  
  3. **把数组的后缀插入到树结构**的变形题目，如 “把新元素放到链表/树的尾部”。  
- **一句话总结**：**“只要看右侧路径，插入点就在那里”。**

---

## 反思

- **第一反应**：直接把树展开成数组再重建，思路直观但容易忽略时间浪费。  
- **最容易踩的坑**  
  - 忘记处理 `val` 大于根节点的情况，这时必须返回新的根节点。  
  - 在遍历右侧路径时，条件写反了（应该是 `cur.right.val > val`），容易导致无限循环或错误的挂载位置。  
  - 忽视空右子树的情况：如果右子树本来就是 `None`，直接把新节点接上即可。  
- **下次遇到同类题**：第一步先 **思考“新元素在原结构中的位置”**，寻找是否只涉及单一路径或局部子树，这往往能直接给出 O(n) 或 O(log n) 的优化思路。