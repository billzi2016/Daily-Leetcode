# #2196. 根据描述创建二叉树 / Create Binary Tree From Descriptions

> 难度：中等 · 标签：Array、Hash Table、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/create-binary-tree-from-descriptions/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array descriptions where descriptions[i] = [parenti, childi, isLefti] indicates that parenti is the parent of childi in a binary tree of unique values. Furthermore,
Construct the binary tree described by descriptions and return its root.
The test cases will be generated such that the binary tree is valid.

**Examples**

**Example 1:**

```
Input: descriptions = [[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]
Output: [50,20,80,15,17,19]
Explanation: The root node is the node with value 50 since it has no parent.
The resulting binary tree is shown in the diagram.
```

**Example 2:**

```
Input: descriptions = [[1,2,1],[2,3,0],[3,4,1]]
Output: [1,2,null,null,3,4]
Explanation: The root node is the node with value 1 since it has no parent.
The resulting binary tree is shown in the diagram.
```

**Constraints**

- 1 <= descriptions.length <= 104
- descriptions[i].length == 3
- 1 <= parenti, childi <= 105
- 0 <= isLefti <= 1
- The binary tree described by descriptions is valid.

---

## 题目（中文翻译）

给定一个二维整数数组 `descriptions`，其中 `descriptions[i] = [parent_i, child_i, isLeft_i]` 表示在一棵节点值唯一的二叉树（binary tree）中，`parent_i` 是 `child_i` 的父节点，`isLeft_i` 为 `1` 表示 `child_i` 是左子节点，为 `0` 表示 `child_i` 是右子节点。  
请根据 `descriptions` 构造这棵二叉树，并返回其根节点。  

测试用例保证描述的二叉树是合法的。

**示例 1**  
**输入**: `descriptions = [[20,15,1],[20,17,0],[50,20,1],[50,80,0],[80,19,1]]`  
**输出**: `[50,20,80,15,17,19]`  
**解释**: 根节点是值为 `50` 的节点，因为它没有父节点。  
结果二叉树如图所示。

**示例 2**  
**输入**: `descriptions = [[1,2,1],[2,3,0],[3,4,1]]`  
**输出**: `[1,2,null,null,3,4]`  
**解释**: 根节点是值为 `1` 的节点，因为它没有父节点。  
结果二叉树如图所示。

**约束条件**  
- `1 <= descriptions.length <= 10^4`  
- `descriptions[i].length == 3`  
- `1 <= parent_i, child_i <= 10^5`  
- `0 <= isLeft_i <= 1`  
- `descriptions` 所描述的二叉树是有效的。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
我们先把所有出现的数值当成“节点”，每次遍历 `descriptions` 时，都去 **找** 对应的父节点和子节点，然后把子节点挂到父节点的左/右指针上。  
- **数据结构**：可以用一个普通的 Python `list` 保存所有已创建的 `TreeNode`，把每个节点的 `val` 当作“名字”。  
- **类比**：把 `list` 想象成一排排的抽屉，抽屉里放的是树的节点。要把某个孩子放到父亲的左边，需要先在抽屉里 **翻找**（线性搜索）出父亲对应的抽屉，再把孩子放进去。  
- **为什么正确**：因为题目保证描述的二叉树合法，所有父子关系都能在这些抽屉里找到对应的节点，最终形成一棵完整的树。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def buildTree_bruteforce(descriptions):
    nodes = []               # 用列表保存所有创建的节点
    child_set = set()        # 记录所有出现过的“孩子”，后面找根节点要用

    # 辅助函数：在 nodes 列表里线性搜索 val 对应的节点
    def get_node(val):
        for nd in nodes:                     # 逐个检查
            if nd.val == val:
                return nd
        # 没找到就新建一个节点并放进列表
        new_nd = TreeNode(val)
        nodes.append(new_nd)
        return new_nd

    # 逐条处理描述
    for parent, child, isLeft in descriptions:
        parent_node = get_node(parent)
        child_node = get_node(child)
        child_set.add(child)                 # 记录 child，根节点永远不在这里

        # 根据 isLeft 决定挂左孩子还是右孩子
        if isLeft == 1:
            parent_node.left = child_node
        else:
            parent_node.right = child_node

    # 根节点是「没有当过孩子」的那个节点
    for nd in nodes:
        if nd.val not in child_set:
            return nd          # 找到根后直接返回
    return None               # 安全起见，实际不会走到这里
```

#### 复杂度  
- **时间复杂度**：`O(n²)`  
  - `n` 为 `descriptions` 的长度。每条描述都要在 `nodes` 列表里线性搜索父子节点，最坏情况列表长度会随 `n` 增长，所以总共是 `1 + 2 + … + n = O(n²)`。  
  - 用大白话说，就是如果有 1000 条描述，程序大约会做 1 000 000 次“找抽屉”的操作。  
- **空间复杂度**：`O(n)`  
  - 需要存储所有节点以及 `child_set`，数量和描述条数成正比。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **每次都要遍历列表去找节点**。我们可以把“找抽屉”这一步变成 **一次查找**，方法是用 **哈希表（字典）** 把节点的值直接映射到对应的 `TreeNode` 对象上。  

1. **一次遍历** `descriptions`，对每个 `[parent, child, isLeft]`：  
   - 如果 `parent` 还没出现，就在字典里新建 `TreeNode(parent)`。  
   - 同理，如果 `child` 还没出现，就新建 `TreeNode(child)`。  
   - 把子节点挂到父节点的左/右指针。  
   - 同时把 `child` 放进一个 `set`，记录所有出现过的孩子。  
2. **找根节点**：遍历所有出现过的节点（字典的键），根节点是 **不在孩子集合里的那个**。因为根节点没有父节点，自然不会被记为孩子。  

**为什么快**：字典的查找、插入都是 **O(1)**（常数时间），所以每条描述只做常数次操作，总体是线性时间 `O(n)`。  

**类比**：把字典想象成一本**电话簿**，里面写着“姓名 → 电话”。只要知道姓名，就能立刻在电话簿里找到对应的电话号码，而不必翻遍所有页码。

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def buildTree_optimal(descriptions):
    nodes = {}          # val -> TreeNode，充当“电话簿”
    children = set()   # 记录所有出现过的 child

    for parent, child, isLeft in descriptions:
        # 若节点不存在则创建，随后直接取出（O(1)）
        if parent not in nodes:
            nodes[parent] = TreeNode(parent)
        if child not in nodes:
            nodes[child] = TreeNode(child)

        # 通过 isLeft 把子节点挂到父节点
        if isLeft == 1:
            nodes[parent].left = nodes[child]
        else:
            nodes[parent].right = nodes[child]

        children.add(child)   # 记录 child，后面找根节点用

    # 根节点：出现过但没有当过孩子的那个节点
    for val, node in nodes.items():
        if val not in children:   # 只要不是孩子，就是根
            return node
    return None   # 题目保证一定有根，这行不会被执行
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 只遍历一次 `descriptions`，每一步的字典操作都是常数时间。可以想象成“只走了一趟路”。  
- **空间复杂度**：`O(n)`  
  - 需要保存 `n` 个节点的对象以及 `children` 集合，和输入规模线性相关。  

---  

## 心得  

- **核心技巧**：利用哈希表（字典）实现**值 ↔ 节点**的快速映射，同时用集合记录“孩子”，进而在 O(n) 时间内找出根节点。  
- **适用的题型**  
  1. “根据父子关系重建树/图”类（如 LeetCode 1719 *Number Of Ways To Reorder Array To Get Same BST*）。  
  2. “根据边信息求根/源点”类（如 261 *Graph Valid Tree*、207 *Course Schedule*）。  
- **解题钥匙**：**先把数据组织成“可以 O(1 查找”的结构，再利用题目给出的唯一性（根节点唯一）完成最后一步**。  

---  

## 反思  

- **第一反应**：看到“parent‑child‑isLeft”三元组，我首先想到把所有节点放进一个列表，然后逐条连接。  
- **最容易踩的坑**  
  - **根节点的寻找**：忘记记录所有出现过的孩子，导致找根时只能随意返回某个节点，结果出错。  
  - **重复创建节点**：如果不检查字典是否已有该值，会产生多个同值的 `TreeNode`，从而破坏树结构。  
  - **边界情况**：只有一条描述（单根节点）时，`children` 为空，需要仍然能返回唯一的节点。  
- **下次类似题的第一步**：**先把所有元素映射到唯一对象（使用字典或集合）**，再在此基础上做连线或拓扑排序。这样可以避免重复创建并快速定位根/源点。