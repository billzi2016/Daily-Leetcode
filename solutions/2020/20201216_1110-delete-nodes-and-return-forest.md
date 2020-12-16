# #1110. 删除节点并返回森林 / Delete Nodes And Return Forest

> 难度：中等 · 标签：Array、Hash Table、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/delete-nodes-and-return-forest/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, each node in the tree has a distinct value.
After deleting all nodes with a value in to_delete, we are left with a forest (a disjoint union of trees).
Return the roots of the trees in the remaining forest. You may return the result in any order.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4,5,6,7], to_delete = [3,5]
Output: [[1,2,null,4],[6],[7]]
```

**Example 2:**

```
Input: root = [1,2,4,null,3], to_delete = [3]
Output: [[1,2,4]]
```

**Constraints**

- The number of nodes in the given tree is at most 1000.
- Each node has a distinct value between 1 and 1000.
- to_delete.length <= 1000
- to_delete contains distinct values between 1 and 1000.

---

## 题目（中文翻译）

给定一棵二叉树的根节点 `root`，树中每个节点的值均互不相同。  
在删除所有值位于数组 `to_delete` 中的节点后，剩余的节点会形成一个森林（forest），即若干互不相连的树的集合。  
返回森林中每棵树的根节点。结果的顺序可以任意。

## 示例

### 示例 1
**输入**  
```json
root = [1,2,3,4,5,6,7], to_delete = [3,5]
```
**输出**  
```json
[[1,2,null,4],[6],[7]]
```

### 示例 2
**输入**  
```json
root = [1,2,4,null,3], to_delete = [3]
```
**输出**  
```json
[[1,2,4]]
```

## 约束条件
- 给定二叉树的节点数不超过 `1000`。
- 每个节点的值在 `1` 到 `1000` 之间，且互不相同。
- `to_delete.length` ≤ `1000`。
- `to_delete` 中的值互不相同，且均在 `1` 到 `1000` 之间。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**遍历整棵树**，每碰到一个节点就去检查它的值是否在 `to_delete` 列表里。  
- **数据结构**：我们只用二叉树本身和一个普通的 Python 列表 `to_delete`。列表查找相当于在一本**词典里顺序翻页**，每翻一页都要看一下，最坏要看完整本词典（`O(k)`，`k = len(to_delete)`）。  
- **正确性**：如果一个节点的值在 `to_delete` 中，就把它从原来的树中“砍掉”。砍掉后，它的左、右子树（如果有）会成为新的独立树的根，加入答案集合。否则，它仍然属于当前的树，继续递归检查它的左右孩子。  
- **时间/空间复杂度**：  
  - **时间**：对每个树节点（共 `n` 个）都要在 `to_delete` 列表里线性查找，最坏 `O(k)`，所以总体是 `O(n·k)`。如果 `k` 接近 `n`，时间就会变成 `O(n²)`，这在 1000 规模的数据上还能跑，但不够优雅。  
  - **空间**：递归调用栈的深度最坏是树的高度，最坏 `O(n)`（链状树）。额外的数据结构只有返回的根节点列表，最多 `O(n)`。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def del_nodes_brute(root, to_delete):
    """
    暴力版：每次判断节点是否需要删除，都在 to_delete 列表里线性搜索
    """
    if not root:
        return []

    # 用一个列表保存最终的森林根节点
    forest = []

    # 递归函数，返回值为当前子树的根（如果被删除则返回 None）
    def dfs(node, is_root):
        if not node:
            return None

        # 判断当前节点是否需要删除（线性搜索）
        need_del = node.val in to_delete   # O(k) 查找

        # 如果当前节点是一个“新根”且不需要删除，就加入答案
        if is_root and not need_del:
            forest.append(node)

        # 递归处理左右子树，子树的根是否是新根取决于当前节点是否被删除
        node.left = dfs(node.left, need_del)
        node.right = dfs(node.right, need_del)

        # 如果需要删除，返回 None 让父节点切断对它的引用
        return None if need_del else node

    dfs(root, True)
    return forest
```

#### 复杂度

- **时间复杂度**：`O(n·k)`  
  - `n` 为树中节点数，`k = len(to_delete)`。每访问一个节点，都要在 `to_delete` 列表里顺序查找一次，最坏是 `O(k)`，于是整体是 `O(n·k)`。  
- **空间复杂度**：`O(n)`  
  - 递归栈最深可能是 `n`（链状树），再加上存放结果的列表最多也不超过 `n`。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每次都要在 `to_delete` 列表里线性查找。  
如果我们把 `to_delete` **提前放进哈希表**（在 Python 中用 `set`），查找的时间就能从 `O(k)` 降到 **常数时间 O(1)**——就像把词典的页码提前写在每个词前面，直接就能定位。

接下来仍然使用 **深度优先搜索（DFS）**，思路不变，只是把“是否需要删除”的判定改成 `val in del_set`（哈希表查找）。  
DFS 的递归过程：

1. **进入节点**，判断它是否在 `del_set` 中（`need_del`）。
2. 如果它是**当前子树的根**（`is_root == True`）且**不需要删除**，就把它加入答案 `forest`。这一步相当于“发现了一棵新树的根”。
3. 递归处理左、右子树。**传递的 `is_root` 参数**取决于当前节点是否被删除：  
   - 若当前节点被删除，子节点会成为**新根**（`is_root = True`）。  
   - 若当前节点保留，子节点仍然是**原根的子树**（`is_root = False`）。
4. 最后，若当前节点需要删除，返回 `None`，让父节点把它的指针切掉；否则返回自身。

**核心数据结构**：

- **`set`**：哈希表实现的集合，查询 `x in set` 的时间是 `O(1)`。可以把它想象成一本**超级快速的字典**，只需要看一眼就知道某个词是否在里面。
- **递归栈**：DFS 本身的调用栈，用来保存遍历路径。深度最多是树的高度，最坏 `O(n)`。

**为什么是最优**：我们只遍历每个节点一次，且每次判定是否删除的成本是 `O(1)`，因此整体时间是 `O(n)`，已经达到了线性下界（必须检查每个节点一次）。空间除了递归栈外，只用了 `O(k)` 的集合和结果列表，也都是线性级别。

#### 代码（Python）

```python
def del_nodes_opt(root, to_delete):
    """
    最优解：使用哈希集合 O(1) 判定是否删除，DFS 一次遍历即可
    """
    if not root:
        return []

    del_set = set(to_delete)          # O(k) 建立哈希表
    forest = []                        # 保存所有新树的根

    def dfs(node, is_root):
        """返回处理后的子树根（若被删除则返回 None）"""
        if not node:
            return None

        need_del = node.val in del_set   # O(1) 判定

        # 当前节点如果是新根且不需要删除，加入答案
        if is_root and not need_del:
            forest.append(node)

        # 递归处理左右子树
        node.left = dfs(node.left, need_del)   # 如果当前被删，左子树是新根
        node.right = dfs(node.right, need_del) # 同理

        # 被删除则返回 None，父节点会切断指向
        return None if need_del else node

    dfs(root, True)   # 整棵树的根一定是“新根”
    return forest
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次，且判定是否删除是 `O(1)`（哈希表查找），所以整体是线性 `O(n)`。相比暴力解的 `O(n·k)`，速度提升明显。  
- **空间复杂度**：`O(n)`  
  - 哈希集合占 `O(k)`（`k ≤ n`），递归栈最深 `O(h)`，`h` 为树高，最坏 `O(n)`。结果列表最多存 `n` 个根节点指针，仍是线性空间。  

---

## 心得

- **核心技巧**：利用哈希集合把“是否删除”的判定从线性查找提升到常数时间，再配合一次 DFS 完成所有切割操作。  
- **适用的题型**：  
  1. **删除节点后返回森林**（本题）。  
  2. **把二叉树中的某些节点标记为“不可达”，返回剩余连通块**（如 LeetCode 366 – Find Leaves of Binary Tree 的变体）。  
  3. **在树上做批量“屏蔽/过滤”后返回剩余子树**（如 “删除子树的节点并返回剩余树的根” 系列）。  
- **一句话总结**：**“先把待删集合做成哈希表，再用一次 DFS 把树一次性切割”。**  

---

## 反思

- **第一反应**：看到“删除节点后剩下森林”，立刻想到要遍历整棵树并在删除点把子树分离——于是想到 DFS。  
- **最容易踩的坑**：  
  - **忘记把子节点当作新根**：当父节点被删除时，必须把它的左右子树（若存在）视作新的独立树根，加入答案。  
  - **递归返回值写错**：返回 `None` 时要确保父节点的指针被置空，否则会留下“悬空”引用导致错误的结构。  
  - **集合判定遗漏**：若直接用列表查找，会导致超时；一定要先 `set(to_delete)`。  
- **下次遇到同类题**，第一步应该想到 **“把待处理的关键元素放进哈希集合，利用 O(1) 判定，再用一次遍历/递归完成所有修改”。**