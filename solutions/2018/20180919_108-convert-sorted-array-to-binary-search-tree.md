# #108. 将有序数组转换为二叉搜索树 / Convert Sorted Array to Binary Search Tree

> 难度：简单 · 标签：Array、Divide and Conquer、Tree、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.

**Examples**

**Example 1:**

```
Input: nums = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: [0,-10,5,null,-3,null,9] is also accepted:
```

**Example 2:**

```
Input: nums = [1,3]
Output: [3,1]
Explanation: [1,null,3] and [3,1] are both height-balanced BSTs.
```

**Constraints**

- 1 <= nums.length <= 104
- -104 <= nums[i] <= 104
- nums is sorted in a strictly increasing order.

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其中的元素已按升序排序，将其转换为一棵高度平衡的二叉搜索树（binary search tree，BST）。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1**  
输入: `nums = [-10,-3,0,5,9]`  
输出: `[0,-3,9,-10,null,5]`  
解释: `[0,-10,5,null,-3,null,9]` 也是一种合法答案。

**示例 2**  
输入: `nums = [1,3]`  
输出: `[3,1]`  
解释: `[1,null,3]` 和 `[3,1]` 都是高度平衡的 BST。

**约束条件**  
- `1 <= nums.length <= 10^4`  
- `-10^4 <= nums[i] <= 10^4`  
- `nums` 按严格递增顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把数组里的每个数依次 **插入** 到一棵二叉搜索树（BST）中。  
- **二叉搜索树**：左子树的所有节点都比根小，右子树的所有节点都比根大。可以把它想象成一本“有序的电话本”，每次查找或插入都从根开始，往左走表示“更小”，往右走表示“更大”。  
- **插入过程**：从根节点开始比较大小，若要插入的值比当前节点小，就往左子树走；否则往右子树走，直到找到一个空位把新节点挂上去。

因为原数组已经是升序的，这种逐个插入的方式可以得到一棵二叉搜索树。但它 **不一定是高度平衡**（即左右子树深度相差不超过 1），所以在最坏情况下（比如数组是递增的），树会退化成一条链表，深度等于 `n`，查询/插入的时间就会变成 `O(n)`。

**为什么这种方法是正确的？**  
二叉搜索树的定义只要求左子树所有节点都比根小，右子树所有节点都比根大。只要我们每次都按照这个规则把新元素挂上去，最终得到的树一定满足 BST 的性质。即使它不平衡，题目只要求“高度平衡的 BST”，所以这一步算是 **暴力基线**，后面再优化。

#### 代码（Python）

```python
# 定义树节点
class TreeNode:
    def __init__(self, val):
        self.val = val          # 节点保存的数值
        self.left = None        # 左子树
        self.right = None       # 右子树

def insert(root: TreeNode, val: int) -> TreeNode:
    """把 val 插入到以 root 为根的 BST 中，返回根节点"""
    if root is None:                     # 空树直接生成根节点
        return TreeNode(val)
    if val < root.val:                   # 小于根节点，往左走
        root.left = insert(root.left, val)
    else:                                # 大于等于根节点，往右走
        root.right = insert(root.right, val)
    return root

def sortedArrayToBST_bruteforce(nums):
    """暴力版：依次把数组元素插入 BST"""
    root = None
    for num in nums:                     # 按顺序遍历数组
        root = insert(root, num)         # 把每个数插入树中
    return root
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 最好情况（树比较平衡）每次插入的路径长度约为 `log n`，总共 `n` 次插入，时间 `O(n log n)`。  
  - **最坏情况**（数组递增导致树退化成链表），第 `i` 次插入需要走 `i‑1` 步，总步数 `1 + 2 + … + (n‑1) = O(n²)`。这里的 `O(n²)` 可以理解为“如果你有 10,000 个数，最坏情况下可能要做大约 100,000,000 次比较”。  

- **空间复杂度：** `O(n)`  
  - 递归调用栈的深度等于树的高度，最坏情况下是 `n`，再加上存放 `n` 个节点本身的空间。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：每次插入都要沿着已有的路径走到底，导致大量重复比较。  
要想让树 **高度平衡**，我们应该让每一次递归都 **挑选中间的元素作为根**，这样左、右子数组的长度相差不超过 1，递归下去自然得到平衡的 BST。

**核心思想：分治（Divide and Conquer）**  
- 把已排序的数组看成一本“有序的书”。如果我们把中间的那一页（中间的数）作为章节标题（根节点），左边的页面自然是左子树，右边的页面是右子树。  
- 对左半段递归同样选中间的数做根，对右半段也如此。递归的终止条件是子数组为空。

**为什么这样能得到平衡树？**  
每一次都把数组均分成两段，左子树和右子树的元素个数最多相差 1。树的高度大约是 `log₂(n)`，这正是平衡二叉树的定义。

**实现细节**  
1. 用两个指针 `l`（左边界）和 `r`（右边界）标记当前子数组的范围。  
2. 计算中间位置 `mid = (l + r) // 2`（整数除法向下取整），这相当于“取中间的那页”。  
3. 创建根节点 `TreeNode(nums[mid])`。  
4. 递归构造左子树 `build(l, mid-1)`，右子树 `build(mid+1, r)`。  
5. 当 `l > r` 时，说明子数组为空，返回 `None`（空指针），递归结束。

#### 代码（Python）

```python
# 同样的树节点定义
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def sortedArrayToBST(nums):
    """最优解：分治法，直接把中间元素当根"""
    
    def build(l: int, r: int) -> TreeNode:
        # 递归终止条件：子数组为空
        if l > r:
            return None
        
        # 取中间位置，向下取整保证左子树不比右子树多超过 1
        mid = (l + r) // 2
        
        # 创建根节点
        root = TreeNode(nums[mid])
        
        # 递归构造左子树和右子树
        root.left  = build(l, mid - 1)   # 左半段
        root.right = build(mid + 1, r)   # 右半段
        return root
    
    # 从完整数组开始递归
    return build(0, len(nums) - 1)
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 每个数组元素恰好被创建一次对应的 `TreeNode`，递归调用的总次数等于元素个数 `n`，没有额外的遍历。可以把它想成“只需要一次遍历，就把所有数字都安放好”。  

- **空间复杂度：** `O(log n)`（递归栈）  
  - 递归深度等于树的高度，平衡二叉树的高度约为 `log₂(n)`。如果把递归看成“在纸上写下每一层的决定”，最多只会写 `log n` 行。再加上返回的树本身占用 `O(n)` 空间，但这部分是题目要求的输出，不计入额外空间。  

---

## 心得

- 这道题的核心技巧是 **“分治 + 中点选根”**，利用数组本身的有序性直接构造平衡 BST。  
- 该技巧常用于 **“把有序结构转换成平衡树”** 的题型，例如：  
  1. *Convert Sorted List to Binary Search Tree*（把有序链表转成平衡 BST）  
  2. *Balanced Binary Search Tree*（从无序数组先排序再建树）  
  3. *Maximum Binary Tree*（虽然规则不同，但也是递归挑选极值构树）  
- **一句话总结**：把中间的数当根，左右递归——这把“均分”变成了“平衡”。  

---

## 反思

- **第一反应**：先想到把每个数逐个插入 BST，觉得最简单。  
- **最容易踩的坑**：  
  - 忘记递归的终止条件 `l > r`，导致无限递归。  
  - 选中点时使用 `(l + r) // 2` 而不是 `(l + r + 1) // 2`，会导致左子树比右子树多一个节点，虽然仍是平衡的，但在某些实现（比如要求左子树更小）可能不符合预期。  
  - 对空数组或长度为 1 的数组处理不当，返回 `None` 或错误节点。  
- **下次类似题的第一步**：先判断“输入是否已经有序”。如果有序，直接用 **“中点分治”** 建树；如果无序，则先排序或考虑其它构造方式。这样思路更清晰，也能快速定位最优解。