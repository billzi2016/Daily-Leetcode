# #109. 将有序链表转换为二叉搜索树 / Convert Sorted List to Binary Search Tree

> 难度：中等 · 标签：Linked List、Divide and Conquer、Tree、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list where elements are sorted in ascending order, convert it to a height-balanced binary search tree.

**Examples**

**Example 1:**

```
Input: head = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: One possible answer is [0,-3,9,-10,null,5], which represents the shown height balanced BST.
```

**Example 2:**

```
Input: head = []
Output: []
```

**Constraints**

- The number of nodes in head is in the range [0, 2 * 104].
- -105 <= Node.val <= 105

---

## 题目（中文翻译）

给定一个单向链表（singly linked list）的头节点 `head`，链表中的元素按升序排列，请将其转换为一棵高度平衡（height-balanced）的二叉搜索树（binary search tree）。

## 示例

### 示例 1
**输入**  
`head = [-10,-3,0,5,9]`

**输出**  
`[0,-3,9,-10,null,5]`

**解释**  
一种可能的答案是 `[0,-3,9,-10,null,5]`，它对应的即是题目所示的高度平衡二叉搜索树。

### 示例 2
**输入**  
`head = []`

**输出**  
`[]`

## 约束条件

- 链表中节点的数量在区间 `[0, 2 * 10^4]` 内。  
- `-10^5 <= Node.val <= 10^5`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **有序链表** 先全部读取到一个 **数组**（或者 Python 列表）里。  
- 链表就像一本只能顺着页码往后翻的笔记本，数组则像一本可以随意翻页的词典，查找第 *k* 个元素的时间从 O(n) 降到 O(1)。  
- 把所有值放进数组后，数组本身已经是升序的。此时我们可以把 “找中间” 这件事交给递归：  
  1. 取数组中间的元素作为根节点（这相当于把词典的中间词当作章节标题）。  
  2. 左半段递归构造左子树，右半段递归构造右子树。  
- 由于每一次递归都把当前区间均分，所以得到的二叉搜索树天然 **高度平衡**（左子树、右子树的高度差不会超过 1）。  

这个方法之所以 **正确**，是因为：
- 中序遍历二叉搜索树会得到升序序列，而我们恰好把升序序列的中间当根，这正好满足二叉搜索树的定义。  
- 递归的子区间仍然保持升序，继续用同样的“取中间”策略，层层递进，最终所有节点都会被安排好位置。  

**时间/空间复杂度**（大白话解释）  
- **时间**：我们需要遍历链表一次把所有元素放进数组，花费 O(n)（n 是节点数）。随后每层递归都只做 O(1) 的工作（取中间、创建节点），递归的层数是 log₂n（因为每次把区间对半划分），所以总时间仍是 O(n)。  
- **空间**：数组需要存放 n 个整数，额外的递归栈深度是 log₂n（树的高度），总体是 O(n)（主要是数组的空间）。  

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sortedListToBST(head: ListNode) -> TreeNode:
    """
    暴力思路：先把链表转成数组，再用递归中间划分构造平衡 BST。
    """
    # 1️⃣ 把链表所有值收集到列表中
    nums = []
    cur = head
    while cur:
        nums.append(cur.val)      # 链表顺序读取，类似“把笔记本的每一页内容抄到词典里”
        cur = cur.next

    # 2️⃣ 递归函数：在 nums[l:r]（左闭右开）区间内构造 BST
    def build(l: int, r: int) -> TreeNode:
        if l >= r:                 # 区间为空，返回空树
            return None
        mid = (l + r) // 2         # 取中间下标，作为根节点
        root = TreeNode(nums[mid])  # 创建根节点
        # 递归左子树：左半段 [l, mid)
        root.left = build(l, mid)
        # 递归右子树：右半段 [mid+1, r)
        root.right = build(mid + 1, r)
        return root

    # 3️⃣ 调用递归，完整区间是 [0, len(nums))
    return build(0, len(nums))
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：遍历链表一次 O(n) + 递归每个节点只创建一次 O(n)，合起来仍是线性时间。  

- **空间复杂度**：`O(n)`  
  - 解释：额外的数组存了 n 个数，递归栈最多 `log₂n` 层（可以忽略不计），所以整体是线性空间。  



---  

### 2. 最优解  

#### 思路  

从暴力解出发，**慢点** 在哪里？  

1. **额外的数组**：把链表全部复制一遍需要 O(n) 额外空间。  
2. **中间查找**：如果不使用数组，而是每次在链表里用快慢指针找中点，时间会退化到 `O(n log n)`（每层都要遍历一次子链表）。  

**优化目标**：只遍历一次链表、且不额外占用 O(n) 空间。  

**关键观察**：  
- 中序遍历（左 → 根 → 右）会得到升序序列。  
- 题目给出的链表本身已经是升序的，只要我们按照 **中序遍历的顺序** 去“消费”链表节点，就能同步构造 BST。  

**实现思路**（一步步推导）  

1. **先算出链表长度 n**（只遍历一次，O(n)）。  
2. **递归构造**：  
   - 对于当前子树，我们先递归构造左子树，左子树的节点数是 `size // 2`（因为要保持平衡）。  
   - 当左子树完成后，**当前链表指针指向的节点** 正好是该子树根节点的值。把它取出来，生成 `TreeNode`。  
   - 然后把链表指针向后移动一位（相当于“消费”了一个节点）。  
   - 最后递归构造右子树，右子树的节点数是 `size - size // 2 - 1`（去掉左子树和根节点）。  
3. 递归的**返回值**是根节点，**全局变量** `head`（或用闭包）记录当前链表位置。  

这样，链表只被顺序遍历一次，**不需要额外的数组**，空间只剩递归栈，深度是 `log₂n`（树的高度），符合最优。  

**类比**：想象你在排队买票，每个人只能一次前进。你先让左半边的人排好座位（递归左子树），轮到中间的那个人时，你把他安排在当前空位（根），再让右半边的人依次入座（递归右子树）。整个过程不需要回头看前面的人，只顺序前进。  

#### 代码（Python）  

```python
# 同样的 ListNode、TreeNode 定义略（保持与上面相同）

def sortedListToBST(head: ListNode) -> TreeNode:
    """
    最优思路：利用中序遍历的顺序，直接在链表上“原地”构造平衡 BST。
    只遍历一次链表，额外空间为递归栈（O(log n)）。
    """
    # 1️⃣ 先求链表长度
    def get_length(node: ListNode) -> int:
        cnt = 0
        while node:
            cnt += 1
            node = node.next
        return cnt

    size = get_length(head)

    # 2️⃣ 使用闭包保存当前遍历指针（外部变量）
    cur = head   # 这里的 cur 会在递归里被更新

    # 3️⃣ 递归构造函数，返回子树根节点
    def build(l: int, r: int) -> TreeNode:
        """
        构造区间 [l, r)（左闭右开）对应的子树。
        区间长度 = r - l
        """
        nonlocal cur               # 让内部可以修改外部的 cur
        if l >= r:                  # 区间为空
            return None

        mid = (l + r) // 2          # 中间位置，先构造左子树

        # 递归左子树，左半部分节点数是 mid - l
        left_child = build(l, mid)

        # 当左子树完成后，cur 指向的节点就是根节点的值
        root = TreeNode(cur.val)    # 创建根节点
        root.left = left_child      # 挂上左子树

        cur = cur.next              # “消费”当前链表节点，指向下一个

        # 递归右子树，右半部分是 [mid+1, r)
        root.right = build(mid + 1, r)

        return root

    # 4️⃣ 从整个链表区间 [0, size) 开始构造
    return build(0, size)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：先遍历一次求长度 O(n)，随后每个节点恰好被创建一次、指针前进一次，整体仍是线性时间。相比暴力解省掉了数组拷贝的常数因子。  

- **空间复杂度**：`O(log n)`  
  - 解释：额外使用的只有递归栈，深度等于树的高度（平衡二叉树的高度约为 `log₂n`），不再有 O(n) 的数组。  

---  

## 心得  

- **核心技巧**：**中序遍历 + 链表顺序消费**，即在递归过程中让左子树先完成，再取当前链表节点作为根，最后构造右子树。  
- **适用的题型**：  
  1. 将有序数组/链表转成平衡 BST（如本题）。  
  2. “从有序结构重建树”系列题目（如 `Convert Sorted Array to Binary Search Tree`）。  
  3. 需要 **原地** 线性构造二叉树的题目（如 “把有序数组转成高度平衡的 AVL 树” 的类似思路）。  
- **一句话总结解题钥匙**：**“把中序遍历的顺序对齐到链表的顺序”，让两者同步前进即可”。  



## 反思  

- **第一反应**：看到“有序链表”和“高度平衡 BST”，本能想到“先转成数组，再用分治”。这就是暴力解。  
- **最容易踩的坑**：  
  - **边界条件**：空链表要返回 `None`，递归区间使用左闭右开 `[l, r)` 防止死循环。  
  - **指针同步**：在递归左子树完成后，才取当前链表节点；如果顺序写错（先取根再递归左子树），会导致结构不平衡。  
  - **递归深度**：虽然 Python 默认递归深度足够 (`log₂(2*10⁴) ≈ 15`)，但在极端情况下仍需注意栈溢出。  
- **下次遇到同类题**：第一步先思考**“能否在一次遍历中同步构造结构？”**，如果答案是肯定的，就尝试用**中序遍历/前序遍历 + 递归指针**的方式实现。