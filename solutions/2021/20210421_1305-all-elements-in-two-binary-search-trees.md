# #1305. 两棵二叉搜索树中的所有元素 / All Elements in Two Binary Search Trees

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Sorting、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/all-elements-in-two-binary-search-trees/)

---

## 题目（英文原版）

**Description**

Given two binary search trees root1 and root2, return a list containing all the integers from both trees sorted in ascending order.

**Examples**

**Example 1:**

```
Input: root1 = [2,1,4], root2 = [1,0,3]
Output: [0,1,1,2,3,4]
```

**Example 2:**

```
Input: root1 = [1,null,8], root2 = [8,1]
Output: [1,1,8,8]
```

**Constraints**

- The number of nodes in each tree is in the range [0, 5000].
- -105 <= Node.val <= 105

---

## 题目（中文翻译）

给定两棵二叉搜索树 `root1` 和 `root2`，返回一个列表，包含两棵树中所有整数，并按升序排序。

**示例 1：**  
**示例 2：**  

**约束条件：**

- 每棵树的节点数范围为 `[0, 5000]`。
- `-10^5 <= Node.val <= 10^5`

**示例：**

**示例 1：**  
输入: `root1 = [2,1,4]`, `root2 = [1,0,3]`  
输出: `[0,1,1,2,3,4]`

**示例 2：**  
输入: `root1 = [1,null,8]`, `root2 = [8,1]`  
输出: `[1,1,8,8]`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **把两棵二叉搜索树（BST）都遍历一遍**，把每个节点的值收集到两个列表 `list1`、`list2` 中。  
   - 对于遍历方式，使用 **深度优先搜索（DFS）**（递归或栈）即可。DFS 就像我们在森林里一路走到底再回头的探险，能把所有树枝（节点）都走到。  
2. 把两个列表合并成一个大列表 `merged = list1 + list2`。  
3. 对合并后的列表直接使用 Python 内置的 `sorted` 排序函数，得到升序的结果。  

> **为什么这样一定对？**  
> - BST 的特性（左子树 < 根 < 右子树）保证了 **遍历一次可以得到所有节点值**，不管顺序怎样，都能收集完整。  
> - 合并后再排序，排序算法会把所有数从小到大排列，正好满足题目要求的“升序”。  

**时间/空间复杂度**（大白话版）：

| 步骤 | 时间复杂度 | 空间复杂度 | 解释 |
|------|------------|-----------|------|
| DFS遍历两棵树 | O(m + n) | O(m + n) | 需要访问每个节点一次，`m`、`n` 分别是两棵树的节点数。递归栈或显式栈最多保存树的深度，最坏情况下等于节点数。 |
| 合并列表 | O(m + n) | O(m + n) | 直接把两个列表拼接，只是把已有的元素搬过去。 |
| 排序 `sorted` | O((m+n)·log(m+n)) | O(m + n) | 排序是最耗时的步骤，常见的 Timsort（Python）在 10⁴‑10⁵ 规模下表现良好。 |

综合起来，**总体时间复杂度是 O((m+n)·log(m+n))**，**空间复杂度是 O(m+n)**（保存所有节点值的列表）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traverse(root, out):
    """深度优先遍历（前序）把所有节点值放进 out 列表"""
    if not root:
        return
    out.append(root.val)          # 访问当前节点
    inorder_traverse(root.left, out)   # 递归左子树
    inorder_traverse(root.right, out)  # 递归右子树

def getAllElements(root1, root2):
    """
    暴力解：遍历两棵树 → 合并 → 排序
    返回所有元素的升序列表
    """
    list1, list2 = [], []
    inorder_traverse(root1, list1)   # 收集第一棵树的所有值
    inorder_traverse(root2, list2)   # 收集第二棵树的所有值

    merged = list1 + list2            # 合并两个列表
    return sorted(merged)            # Python 内置排序，返回升序结果
```

#### 复杂度

- **时间复杂度**：`O((m+n)·log(m+n))`  
  - `m`、`n` 分别是两棵树的节点数。遍历是线性的，真正耗时的是排序，排序的代价是 `N·log N`（`N = m+n`），这就像把 `N` 本书排好顺序，需要比较 `log N` 次才能决定每本书的位置。  
- **空间复杂度**：`O(m+n)`  
  - 需要两个列表存所有节点值，还要额外的递归栈空间，最坏情况下也是 `O(m+n)`。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈在排序**：我们把所有值收集后再整体排序，实际上已经浪费了 BST 本身“天然有序”的特性。  
**BST 的中序遍历（左‑根‑右）会得到一个已排序的序列**。如果我们对每棵树分别做中序遍历，就能得到两个已经排好序的列表 `sorted1`、`sorted2`。接下来只需要把这两个有序列表 **像合并两个有序数组那样**，一次遍历完成合并，时间线性，不再需要额外的 `log` 因子。

核心步骤：

1. **中序遍历**得到有序列表  
   - 递归版或迭代版都可以，这里用递归，代码简洁。  
2. **双指针合并**  
   - 用两个指针 `i`、`j` 分别指向 `sorted1`、`sorted2` 的当前位置。  
   - 每次比较 `sorted1[i]` 与 `sorted2[j]`，把较小的放进结果列表，指针向前移动。  
   - 当其中一个列表耗尽后，直接把剩余的另一列表全部接到结果后面。  
   - 这一步类似于“归并排序”里合并两个有序子序列的过程，时间是线性的。  

> **类比**：把两条已经排好序的队伍（比如排队买票的两队）合并成一条更长的有序队伍，只需要比较队首的两个人，决定谁先走，重复此过程即可。

#### 代码（Python）

```python
def inorder_collect(root, arr):
    """递归中序遍历，直接把节点值按升序放入 arr"""
    if not root:
        return
    inorder_collect(root.left, arr)   # 先左子树（更小的值）
    arr.append(root.val)              # 再根节点
    inorder_collect(root.right, arr)  # 最后右子树（更大的值）

def merge_sorted(list1, list2):
    """把两个已升序的列表合并成一个升序列表（双指针）"""
    i = j = 0
    merged = []
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    # 把剩余的元素直接加到结果里
    merged.extend(list1[i:])
    merged.extend(list2[j:])
    return merged

def getAllElements(root1, root2):
    """
    最优解：利用 BST 的中序遍历得到有序序列 → 双指针合并
    """
    sorted1, sorted2 = [], []
    inorder_collect(root1, sorted1)   # 生成第一棵树的有序列表
    inorder_collect(root2, sorted2)   # 生成第二棵树的有序列表

    return merge_sorted(sorted1, sorted2)
```

#### 复杂度

- **时间复杂度**：`O(m + n)`  
  - 中序遍历各一次是线性的 `O(m)`、`O(n)`，合并两个有序列表也是线性的 `O(m+n)`。没有额外的 `log` 因子，比暴力解快很多。  
- **空间复杂度**：`O(m + n)`  
  - 需要存放两棵树的所有节点值（两个列表），递归栈深度最多是树的高度，最坏情况下（完全不平衡）仍是 `O(m+n)`，但在平衡树时只会是 `O(log m) + O(log n)`，比暴力解的额外空间没有增加。

---

## 心得

- **核心技巧**：**利用二叉搜索树的中序遍历得到有序序列 + 双指针合并两个有序数组**。  
- **适用的题型**  
  1. 合并两个已排序的数据结构（如两条有序链表、两个有序数组）。  
  2. “把多棵 BST 的所有元素合并成一个有序序列”这类题目（如 LeetCode 1305, 1582）。  
- **一句话总结解题钥匙**：**把“排序的工作交给 BST 本身”，只在已有序的结果上做线性合并**。

---

## 反思

- **第一反应**：直接把所有节点收集后整体排序，思路最直接，却忽略了 BST 本身的有序性。  
- **最容易踩的坑**  
  - **递归深度**：如果树极度不平衡（链状），递归会达到 `O(N)` 深度，可能导致栈溢出。可以改写为显式栈的迭代中序遍历来规避。  
  - **空树**：`root` 可能为 `None`，要确保遍历函数能安全返回空列表。  
  - **重复值**：BST 允许相同值出现在不同树中，合并时必须保留所有出现次数，不能去重。  
- **下次遇到同类题**：第一步先问自己“这棵树有没有天然的顺序可以直接利用？”如果答案是“有”，就把 **中序遍历** 当作“把树变成排好序的数组”，再考虑如何把多个有序数组**高效合并**。