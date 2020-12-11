# #1104. 锯齿标记二叉树中的路径 / Path In Zigzag Labelled Binary Tree

> 难度：中等 · 标签：Math、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/path-in-zigzag-labelled-binary-tree/)

---

## 题目（英文原版）

**Description**

In an infinite binary tree where every node has two children, the nodes are labelled in row order.
In the odd numbered rows (ie., the first, third, fifth,...), the labelling is left to right, while in the even numbered rows (second, fourth, sixth,...), the labelling is right to left.
Given the label of a node in this tree, return the labels in the path from the root of the tree to the node with that label.

**Examples**

**Example 1:**

```
Input: label = 14
Output: [1,3,4,14]
```

**Example 2:**

```
Input: label = 26
Output: [1,2,6,10,26]
```

**Constraints**

- 1 <= label <= 10^6

---

## 题目（中文翻译）

在一棵每个节点都有两个子节点的无限二叉树（binary tree）中，节点的标签（label）按照层序（row order）进行标记。  
在奇数层（即第 1、3、5 … 层）中，标签从左到右递增；而在偶数层（第 2、4、6 … 层）中，标签从右到左递增。  
给定该树中某个节点的标签，返回从根节点到该标签所在节点的路径上所有节点的标签。

**示例 1**  
输入: `label = 14`  
输出: `[1,3,4,14]`

**示例 2**  
输入: `label = 26`  
输出: `[1,2,6,10,26]`

**约束条件**  
- `1 <= label <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把树从根节点一直“画”到目标 label 所在的那一层**，在画的过程中把每个节点的父子关系记下来，最后再从目标节点往上回溯得到根到它的路径。

- **用到的数据结构**：  
  - **哈希表（字典）**。把每个节点的 **parent** 记录下来，`parent[child] = parent_node`。哈希表就像一本查字典，**key** 是子节点的编号，**value** 是它的父节点编号，查找和写入都很快（均摊 O(1) 时间）。  
  - **队列**（用于层序遍历）。层序遍历相当于“按行”一次一次地把树展开，和我们在生活中从上往下排队买东西的顺序一样。

- **为什么这个方法能得到正确答案**：  
  - 层序遍历保证我们严格按照树的层次（行）顺序访问每一个节点。  
  - 每访问到一个节点，就把它的左右子节点（如果编号 ≤ 给定的 `label`）加入队列并记录父子关系。于是，当遍历结束时，**所有编号 ≤ label 的节点的父节点信息都已经完整保存**，自然可以把目标节点一直往上找至根节点。

- **时间/空间复杂度的大白话解释**：  
  - 假设目标 `label` 为 `n`，我们需要把编号从 `1` 到 `n` 的所有节点都遍历一遍。遍历一次相当于“看一遍”这个节点，时间随 `n` 成正比，用数学语言记作 **O(n)**（读作 “欧‑恩”），意思是当 `n` 翻倍时，耗时也会大概翻倍。  
  - 同时，我们把每个节点的父节点都存进字典，需要额外的空间，同样是 **O(n)**。

#### 代码（Python）

```python
from collections import deque

def path_in_zigzag_tree_bruteforce(label: int):
    """
    暴力实现：层序遍历到 label，记录每个节点的父节点
    """
    # 哈希表：child -> parent
    parent = {1: None}                # 根节点没有父节点
    q = deque([1])                    # 队列初始化，只放根节点
    level = 1                         # 当前层数（从 1 开始）

    while q:
        # 当前层有多少个节点
        size = len(q)
        # 这一层的标签范围（左到右的顺序）
        start = 2 ** (level - 1)
        end   = 2 ** level - 1

        # 判断这一层是否是“从右往左”标号的偶数层
        reverse = (level % 2 == 0)

        for i in range(size):
            node = q.popleft()
            # 如果已经到了目标节点，停止遍历
            if node == label:
                q.clear()
                break

            # 计算左右子节点的真实编号（仍然是左到右的顺序）
            left  = node * 2
            right = node * 2 + 1

            # 只把编号不超过 label 的子节点加入队列
            for child in (left, right):
                if child > label:
                    continue

                # 在偶数层需要把顺序翻转一下才是真实的标号
                if reverse:
                    # 这一层的最左编号 start 对应的实际标号是 end，最右编号 end 对应的实际标号是 start
                    # 公式：real = start + (end - child)
                    real = start + (end - child)
                else:
                    real = child

                parent[real] = node          # 记录父节点
                q.append(real)               # 加入队列继续遍历

        level += 1

    # 从 label 往上回溯得到路径
    path = []
    cur = label
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]                     # 反转得到根到 label 的顺序
```

#### 复杂度  

- **时间复杂度**：`O(n)`（这里的 `n` 是 `label` 的大小），因为我们可能要遍历所有编号 ≤ `label` 的节点。  
- **空间复杂度**：`O(n)`，字典里要保存每个节点的父节点信息，同样和遍历的节点数成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于我们把整棵树都“画”出来了**，而事实上我们只需要知道 **每一层的父节点应该是多少**，不必真的去构造整层的所有节点。  

下面一步步推导出只用 **O(log label)** 时间和空间的做法：

1. **先定位目标节点所在的层**  
   - 二叉树的第 `k` 层（根层记为 1）包含的编号范围是  
     \[
     [2^{k-1},\; 2^{k}-1]
     \]  
   - 只要把 `label` 和 `2^{k}` 比较一下，就能找到最小的 `k` 使得 `label ≤ 2^{k}-1`。这一步只需要不断把 `label` 除以 2（即右移），所以时间是 `O(log label)`。

2. **把“之字形”转成普通的左到右顺序**  
   - 假设当前层是 **偶数层**（从右往左标号），我们把它 **镜像** 到左到右的顺序，得到一个 “普通” 编号 `mirror`。  
   - 公式（层 `k`）：
     \[
     mirror = 2^{k-1} + (2^{k}-1 - label)
     \]  
     直观理解：左边的第 `i` 个位置，在右往左标号时对应的就是右边第 `i` 个位置，所以用 `左端 + (右端 - 当前)` 进行翻转。

3. **求父节点**  
   - 在 **普通的二叉树**（左到右标号）里，父节点的编号就是 `child // 2`（整数除以 2）。  
   - 把上一步得到的 `mirror` 除以 2，得到 **父层的普通编号** `parent_mirror`。

4. **再把父层的普通编号映射回实际的之字形编号**  
   - 父层的层号是 `k-1`。如果父层是 **偶数层**（仍然是右往左），则需要再次镜像；否则直接使用 `parent_mirror`。  
   - 镜像公式同上，只是换成父层的范围。

5. **重复向上**  
   - 把得到的父节点当作新的 `label`，层号减 1，继续上述步骤，直到到根节点（层号 1）。  
   - 每次循环层号减 1，最多循环 `log₂(label)` 次。

6. **收集路径**  
   - 从目标节点往上找的顺序是 **从下往上**，把每一步的实际编号保存到列表中，最后把列表倒序即可得到 **根 → 目标** 的路径。

> **核心技巧**：**层级镜像**（把右往左的编号翻转成左到右的普通编号），配合 **整数除 2** 找父节点。整个过程只需要知道每层的最左、最右编号，根本不需要真的建树。

#### 代码（Python）

```python
def path_in_zigzag_tree(label: int):
    """
    O(log label) 解法：直接从 label 往上找父节点
    """
    path = []
    cur = label
    # 先算出 cur 所在的层（从 1 开始计数）
    level = cur.bit_length()            # 2^{k-1} <= cur < 2^{k} => k = bit_length

    while cur >= 1:
        path.append(cur)                # 记录当前层的实际编号
        # 计算本层的最左、最右编号（左到右的顺序）
        left  = 2 ** (level - 1)
        right = 2 ** level - 1

        # 把当前编号翻转到普通的左到右编号
        #   若本层是奇数层，left->right 顺序本身就是普通的，翻转后仍是 cur
        #   若本层是偶数层，需要做镜像
        cur_mirror = left + (right - cur)

        # 父节点在普通二叉树中的编号（左到右顺序）
        parent_mirror = cur_mirror // 2

        # 父层的层号
        level -= 1
        if level == 0:                   # 已经到根节点的父层，结束循环
            break

        # 父层的最左、最右编号
        left_parent  = 2 ** (level - 1)
        right_parent = 2 ** level - 1

        # 把父层的普通编号再映射回实际的之字形编号
        #   父层如果是偶数层，需要再次镜像
        if level % 2 == 0:               # 偶数层 → 右往左，需要翻转
            cur = left_parent + (right_parent - parent_mirror)
        else:                            # 奇数层 → 左到右，直接使用
            cur = parent_mirror

    # 最后把路径倒过来，得到根到 label 的顺序
    return path[::-1]
```

> **代码解释（逐行中文注释）**  
> - `bit_length()`：返回二进制表示中最高位所在的位置（即层号），相当于 `⌊log₂(label)⌋ + 1`。  
> - `left`、`right`：本层左、右端的编号，**左到右顺序**的范围。  
> - `cur_mirror`：把本层的实际编号（可能是右往左）翻转成普通左到右的编号。奇数层翻转后不变，偶数层会真正“镜像”。  
> - `parent_mirror = cur_mirror // 2`：在普通二叉树里，父节点就是子节点编号除以 2。  
> - 接下来把父层的普通编号再映射回之字形的实际编号，取决于父层是奇数还是偶数。  
> - 循环结束后 `path` 中保存的是从目标往上到根的顺序，`[::-1]` 把它反转。

#### 复杂度  

- **时间复杂度**：`O(log label)`。  
  - 每一次循环都把层号减 1，最多循环 `log₂(label)` 次（因为二叉树的层数随编号呈对数增长）。  
  - “对数”可以想象成：如果 `label` 是 1 000 000，大约只需要走 20 步就能到根。

- **空间复杂度**：`O(log label)`。  
  - 只用一个列表保存路径，列表长度等于树的层数，同样是对数级别。

---

## 心得

- **核心技巧**：**层级镜像 + 整数除 2 求父节点**。先把之字形的编号翻转成普通二叉树的编号，再利用普通二叉树的父子关系求解，最后再映射回原来的编号。  
- **该技巧适用的题型**：  
  1. **Zigzag/反向标号的树或数组**（如 “Zigzag Conversion” 的思路类比）。  
  2. **只需要沿父链向上/向下移动的二叉树题**（如 “Binary Tree Paths” 的变体，只是要先把编号统一）。  
  3. **涉及层次范围映射的数学题**（如 “Find the K-th Smallest in a BST” 的二分层次解法）。  
- **一句话总结解题钥匙**：**把“奇怪的标号”先统一成“正常的左到右标号”，再用普通二叉树的规律求父子关系，最后把结果映射回原来的标号**。

---

## 反思

- **第一反应**：看到“之字形标号”，本能想到要把树“画”出来再找路径，于是想到了 BFS/哈希表的暴力办法。  
- **最容易踩的坑**：  
  - **层号的计算**：直接用 `while 2**k <= label` 会写成 `2**k < label`，导致层号偏小。使用 `bit_length()` 或 `log2` 更安全。  
  - **镜像公式写错**：`right - cur` 必须在同一层的范围内，否则会得到负数。记住公式是 `left + (right - cur)`。  
  - **边界条件**：当 `label = 1`（根节点）时，循环应直接结束，否则会出现 `level = 0` 时再做镜像导致错误。  
- **下次遇到同类题**：第一步先 **确定层级**，第二步 **把特殊标号统一成普通标号**（往往是一次镜像或翻转），随后 **使用常规二叉树的性质**（如 `//2`、`*2`）求解。这样可以把“奇怪的规则”转化为熟悉的普通规则，思路会清晰很多。