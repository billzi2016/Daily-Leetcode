# #2471. **按层排序二叉树的最少操作次数** / Minimum Number of Operations to Sort a Binary Tree by Level

> 难度：中等 · 标签：Tree、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree with unique values.
In one operation, you can choose any two nodes at the same level and swap their values.
Return the minimum number of operations needed to make the values at each level sorted in a strictly increasing order.
The level of a node is the number of edges along the path between it and the root node.

**Examples**

**Example 1:**

```
Input: root = [1,4,3,7,6,8,5,null,null,null,null,9,null,10]
Output: 3
Explanation:
- Swap 4 and 3. The 2nd level becomes [3,4].
- Swap 7 and 5. The 3rd level becomes [5,6,8,7].
- Swap 8 and 7. The 3rd level becomes [5,6,7,8].
We used 3 operations so return 3.
It can be proven that 3 is the minimum number of operations needed.
```

**Example 2:**

```
Input: root = [1,3,2,7,6,5,4]
Output: 3
Explanation:
- Swap 3 and 2. The 2nd level becomes [2,3].
- Swap 7 and 4. The 3rd level becomes [4,6,5,7].
- Swap 6 and 5. The 3rd level becomes [4,5,6,7].
We used 3 operations so return 3.
It can be proven that 3 is the minimum number of operations needed.
```

**Example 3:**

```
Input: root = [1,2,3,4,5,6]
Output: 0
Explanation: Each level is already sorted in increasing order so return 0.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 105].
- 1 <= Node.val <= 105
- All the values of the tree are unique.

---

## 题目（中文翻译）

给定一棵节点值唯一的二叉树（binary tree）的根节点 `root`。  
一次操作可以选择同一层（level）上的任意两个节点并交换它们的值。  
返回使每一层的节点值都按照严格递增顺序（strictly increasing order）排序所需的最少操作次数。

节点的层数定义为该节点到根节点之间的边数。

---

### 示例

#### 示例 1
**输入**  
`root = [1,4,3,7,6,8,5,null,null,null,null,9,null,10]`

**输出**  
`3`

**解释**  
- 交换 4 与 3，第二层变为 `[3,4]`。  
- 交换 7 与 5，第三层变为 `[5,6,8,7]`。  
- 再次交换 8 与 7，第三层变为 `[5,6,7,8]`。  
共用了 3 次操作，因此返回 3。可以证明 3 是所需的最小操作次数。

#### 示例 2
**输入**  
`root = [1,3,2,7,6,5,4]`

**输出**  
`3`

**解释**  
- 交换 3 与 2，第二层变为 `[2,3]`。  
- 交换 7 与 4，第三层变为 `[4,6,5,7]`。  
- 交换 6 与 5，第三层变为 `[4,5,6,7]`。  
共用了 3 次操作，因此返回 3。可以证明 3 是最小操作次数。

#### 示例 3
**输入**  
`root = [1,2,3,4,5,6]`

**输出**  
`0`

**解释**  
每一层已经是递增有序的，故返回 0。

---

### 约束条件
- 树中节点的数量在 `[1, 10^5]` 区间内。  
- `1 <= Node.val <= 10^5`  
- 所有节点值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一层的节点值当成一个数组，直接用最笨的排序方法把它排好**，在排的过程中记录下我们用了多少次「交换两个同层节点的值」的操作。  
这相当于把树的每一层想象成**一排书**，我们只能把同一排里的两本书互换位置，目标是让这排书从左到右严格递增。  

- **使用的数据结构**：  
  - `Queue`（队列）实现 **层序遍历（BFS）**，把树按层拆成若干个数组。  
  - `list`（列表）保存每层的节点值。  
  - 为了统计交换次数，我们可以直接使用**冒泡排序**（每次相邻两个元素不满足顺序就交换）或者**选择排序**（每次把当前未排序区间的最小值换到前面）。这些排序的核心就是「一次交换」对应题目中的一次操作。  

- **为什么这个方法一定能得到正确答案**：  
  只要我们把每层的数组完全排序好，所有层自然都满足「严格递增」的要求。因为每一次交换都是合法的（同层、任意两节点），所以任何合法的序列都可以通过若干次这样的交换实现。  

- **时间/空间复杂度的大白话**：  
  - **时间复杂度**：假设第 `i` 层有 `k_i` 个节点，冒泡排序在最坏情况下要比较 `k_i*(k_i-1)/2` 次，大约是 `k_i²/2`，所以整棵树的时间是  
    \[
    O\!\left(\sum_i k_i^2\right)
    \]  
    这在最坏情况下（比如只有一层有 `N` 个节点）会退化成 `O(N²)`，也就是「如果你有 10 000 个数字，可能要做 1 亿 次比较」——显然太慢了。  
  - **空间复杂度**：只需要额外的队列和每层的数组，最多 `O(N)`（因为所有节点都要放进队列一次），这在实际中是可以接受的。  

#### 代码（Python）

```python
from collections import deque
from typing import List, Optional

# ---------- 辅助函数：把树按层拆成若干数组 ----------
def bfs_levels(root: Optional['TreeNode']) -> List[List[int]]:
    """层序遍历，返回每层节点值的列表（顺序同树的层次）"""
    if not root:
        return []
    q = deque([root])
    levels = []
    while q:
        level_size = len(q)               # 当前层有多少节点
        cur_level = []
        for _ in range(level_size):
            node = q.popleft()
            cur_level.append(node.val)    # 记录节点值
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(cur_level)
    return levels


# ---------- 暴力解：用冒泡排序统计交换次数 ----------
def min_swaps_bruteforce(root: Optional['TreeNode']) -> int:
    levels = bfs_levels(root)
    total_swaps = 0

    for arr in levels:                     # 对每一层独立处理
        n = len(arr)
        # 冒泡排序——每次相邻不满足顺序就交换
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]  # 交换两节点的值
                    total_swaps += 1
    return total_swaps
```

> **注意**：这里的 `TreeNode` 定义请自行补全（LeetCode 已经提供），代码可以直接跑通。

#### 复杂度

- **时间复杂度**：`O(N²)` —— 把每层当成普通数组，用冒泡排序，需要对每层做 `k_i²` 次比较，最坏情况下全部节点都在同一层。  
  - 大白话：如果树有 10⁵ 个节点，最差会需要约 10¹⁰ 次比较，显然不现实。  
- **空间复杂度**：`O(N)` —— 需要存储层序遍历时的队列和所有层的数组。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于「排序」的方式**：我们不需要真的把数组一步步冒泡到有序，只要知道最少需要多少次「任意两元素交换」就行。  

**关键观察**：  
- 对于任意一个数组，要把它排成升序，只需要把「不在正确位置的元素」两两交换即可。  
- 这正是**最小交换次数**问题：把数组映射到它的排好序后的位置，统计**置换的循环数**（cycle decomposition）。  
- 置换中的每个循环长度为 `len`，把它们变成有序只需要 `len - 1` 次交换。  
- 所以 **最小交换次数 = 总元素数 - 循环数**。  

**为什么这比冒泡快**：  
- 我们只遍历一次数组（`O(k)`），并且一次排序（`O(k log k)`) 用来得到「每个元素应该去哪里」的映射。  
- 这样每层的复杂度从 `O(k²)` 降到了 `O(k log k)`，整体上变成 `O(N log N)`，足以应对 10⁵ 规模的输入。

**实现步骤**（把每层当成独立的子问题）：

1. **层序遍历**：同暴力解，用 BFS 把树拆成层。  
2. 对每层的数组 `arr`：  
   a. 复制一份并排序得到 `sorted_arr`。  
   b. 用哈希表 `pos` 把 **值 → 排序后的位置** 建立映射（类似字典查词典：词是节点值，页码是它应该去的下标）。  
   c. 用 `visited` 数组标记哪些下标已经在正确位置或已经被计入循环。  
   d. 从左到右遍历 `arr`，如果当前下标 `i` 已访问或已经在正确位置（`pos[arr[i]] == i`），跳过。否则沿着映射一直跳，形成一个循环，循环长度记为 `cycle_len`，对应需要 `cycle_len - 1` 次交换。累计到本层的答案。  
3. 把所有层的交换次数相加，即为答案。

**类比**：想象每层的数字是**一堆乱放的信封**，每个信封上写着应该放在第几号格子里（`pos`），我们一次可以把任意两个信封换位置。把所有信封最终放到对应格子里，只需要把每个「环」拆开——每拆开一个环，就少一次「错位」，所以环的大小决定了需要的交换次数。

#### 代码（Python）

```python
from collections import deque
from typing import List, Optional

# ---------- 辅助函数：层序遍历 ----------
def bfs_levels(root: Optional['TreeNode']) -> List[List[int]]:
    if not root:
        return []
    q = deque([root])
    levels = []
    while q:
        level_size = len(q)
        cur = []
        for _ in range(level_size):
            node = q.popleft()
            cur.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        levels.append(cur)
    return levels


# ---------- 最优解：利用置换的循环计数 ----------
def min_swaps_optimal(root: Optional['TreeNode']) -> int:
    levels = bfs_levels(root)
    total_swaps = 0

    for arr in levels:                     # 每层独立处理
        n = len(arr)
        # 1) 排序得到目标顺序
        sorted_arr = sorted(arr)
        # 2) 建立「值 → 目标下标」的映射（字典查词典）
        pos = {val: idx for idx, val in enumerate(sorted_arr)}
        visited = [False] * n

        for i in range(n):
            if visited[i] or pos[arr[i]] == i:
                # 已经访问过或已经在正确位置，无需操作
                visited[i] = True
                continue

            # 开始遍历一个置换循环
            cycle_len = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = pos[arr[j]]            # 跳到「应该放在这里」的下标
                cycle_len += 1

            # 一个长度为 cycle_len 的循环，需要 cycle_len-1 次交换
            total_swaps += cycle_len - 1

    return total_swaps
```

> **说明**：  
> - `pos[arr[j]]` 直接把当前值映射到它在排好序数组中的下标。  
> - `visited` 防止同一个元素被重复计入多个循环。  

#### 复杂度

- **时间复杂度**：`O(N log N)`  
  - 对每层先排序（`k_i log k_i`），再一次线性遍历（`O(k_i)`）。所有层的 `k_i` 加起来是 `N`，所以整体是 `O(N log N)`。  
  - 与暴力的 `O(N²)` 相比，**速度提升了几个数量级**（比如 `N=10⁵` 时，`N log N ≈ 1.7×10⁶`，完全可接受）。  

- **空间复杂度**：`O(N)`  
  - 需要存放层序遍历得到的所有节点值以及每层的哈希表、访问数组。总额不超过 `2N`，在 10⁵ 规模下仍然很轻量。  

---

## 心得

- **核心技巧**：**把每层看成独立的数组，求「最小交换次数」**——这本质上是**置换的循环分解**（cycle decomposition）问题。  
- **适用的题型**：  
  1. “最少交换次数使数组有序” 类似题（LeetCode 1535、565 等）。  
  2. 需要在同一层/同一组内部自由交换元素的树或图题（例如“按层翻转二叉树”变形）。  
- **一句话总结**：**把「同层任意交换」抽象成「置换」，统计循环数即可得到最小操作数**。

---

## 反思

- **第一反应**：看到「同层任意交换」立刻想到「每层独立」以及「排序」——于是先写了最直观的冒泡实现。  
- **最容易踩的坑**：  
  - **忘记「严格递增」**：必须确保排序后没有相等的情况，题目已保证所有值唯一，仍需用 `sorted` 而不是 `sort(reverse=True)` 等误用。  
  - **循环计数写错**：`cycle_len - 1` 是关键，容易误写成 `cycle_len` 或漏掉 `visited` 标记导致无限循环。  
  - **边界情况**：单节点树、某层只有一个节点时循环长度为 1，应该贡献 0 次交换。  
- **下次类似题的第一步**：**先把问题拆成「每组独立」+「最小交换次数」**，然后回忆置换循环的公式，快速得到 `O(k log k)` 的解法。