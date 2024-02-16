# #2583. 二叉树中第 k 大层和 / Kth Largest Sum in a Binary Tree

> 难度：中等 · 标签：Tree、Breadth-First Search、Sorting、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/kth-largest-sum-in-a-binary-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree and a positive integer k.
The level sum in the tree is the sum of the values of the nodes that are on the same level.
Return the kth largest level sum in the tree (not necessarily distinct). If there are fewer than k levels in the tree, return -1.
Note that two nodes are on the same level if they have the same distance from the root.

**Examples**

**Example 1:**

```
Input: root = [5,8,9,2,1,3,7,4,6], k = 2
Output: 13
Explanation: The level sums are the following:
- Level 1: 5.
- Level 2: 8 + 9 = 17.
- Level 3: 2 + 1 + 3 + 7 = 13.
- Level 4: 4 + 6 = 10.
The 2nd largest level sum is 13.
```

**Example 2:**

```
Input: root = [1,2,null,3], k = 1
Output: 3
Explanation: The largest level sum is 3.
```

**Constraints**

- The number of nodes in the tree is n.
- 2 <= n <= 105
- 1 <= Node.val <= 106
- 1 <= k <= n

---

## 题目（中文翻译）

**题目描述**  
给定一棵二叉树的根节点 `root` 和一个正整数 `k`。  
树的**层和**（level sum）指的是同一层（即与根的距离相同）的所有节点值之和。  
返回树中第 `k` 大的层和（层和可以相同）。如果树的层数少于 `k`，返回 `-1`。  
注意，若两个节点到根的距离相同，则它们位于同一层。

**示例**  

*示例 1*  
```
输入: root = [5,8,9,2,1,3,7,4,6], k = 2
输出: 13
解释: 各层的层和如下:
- 第 1 层: 5
- 第 2 层: 8 + 9 = 17
- 第 3 层: 2 + 1 + 3 + 7 = 13
- 第 4 层: 4 + 6 = 10
第 2 大的层和为 13。
```

*示例 2*  
```
输入: root = [1,2,null,3], k = 1
输出: 3
解释: 最大的层和为 3。
```

**约束条件**  
- 树中节点的数量为 `n`。  
- `2 <= n <= 10^5`  
- `1 <= Node.val <= 10^6`  
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **层序遍历**（Breadth‑First Search，BFS）  
   - 想象我们在看一棵树的“楼层”。同一层的所有节点就在同一层次上，和我们坐电梯时每次只上下同一层的乘客差不多。  
   - 用 **队列**（queue）来模拟电梯：先把根节点放进队列，每次取出当前层的所有节点，记录它们的值之和，然后把它们的左、右孩子依次放进队列，进入下一层。  

2. **收集每层的和**  
   - 把每层算出的和放进一个普通的列表 `level_sums`，相当于把每层的“总收入”记在纸上。

3. **找第 k 大的和**  
   - 把 `level_sums` 按从大到小排序（像把纸上的数字从高到低排好序），第 `k‑1` 个位置的数字就是答案。  
   - 如果层数不足 `k`，直接返回 `-1`。

> **为什么一定能得到正确答案？**  
> - BFS 能保证我们遍历到每一个节点，而且每个节点只会被访问一次。  
> - 对每层我们把所有节点的值相加，正好得到题目定义的“层和”。  
> - 排序后取第 `k` 大，和题目要求完全一致。

#### 代码（Python）

```python
from collections import deque
from typing import Optional, List

# ------------------- 二叉树节点定义 -------------------
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

# ------------------- 暴力解 -------------------
def kthLargestLevelSum_bruteforce(root: TreeNode, k: int) -> int:
    if not root:                     # 空树直接返回 -1（题目说不会出现，但防御性写法）
        return -1

    q = deque([root])                # 队列用于层序遍历
    level_sums: List[int] = []      # 用来存每层的和

    while q:
        level_size = len(q)          # 当前层有多少节点
        cur_sum = 0                  # 累计本层的节点值
        for _ in range(level_size):
            node = q.popleft()       # 取出本层的一个节点
            cur_sum += node.val      # 加到本层和里
            if node.left:           # 左子树加入队列，准备进入下一层
                q.append(node.left)
            if node.right:          # 右子树同理
                q.append(node.right)
        level_sums.append(cur_sum)   # 本层遍历完，保存本层和

    # 把所有层和从大到小排序
    level_sums.sort(reverse=True)

    # 如果层数不足 k，返回 -1
    if k > len(level_sums):
        return -1
    return level_sums[k - 1]          # 第 k 大的层和（下标从 0 开始）
```

#### 复杂度  

- **时间复杂度**：`O(n + L log L)`  
  - `n` 是节点数，遍历一次树需要 `O(n)`。  
  - `L` 是层数（`L ≤ n`），对 `L` 个层和排序需要 `O(L log L)`。  
  - 简单理解：如果树有 10 万个节点，排序 10 万个数字大约是 “几万次” 的比较，算是比较慢的步骤。  

- **空间复杂度**：`O(L)`  
  - 只存每层的和，最多和层数一样多。  
  - 队列在最坏情况下最多保存一层的所有节点，最多也是 `O(width)`，而宽度 ≤ `L`，所以整体是 `O(L)`。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于**对所有层和进行完整排序**。如果层数很多（比如接近 10⁵），排序的 `log L` 会让程序稍慢。实际上我们只关心第 `k` 大的那个值，不需要把所有层和全部排好序。

**关键想法**：用 **小根堆（min‑heap）** 只保存当前最大的 `k` 个层和。  

- 小根堆的特点是堆顶（根节点）是最小的元素。  
- 当堆的大小小于 `k` 时，直接把新的层和加入堆。  
- 当堆已经有 `k` 个元素时，比较新层和与堆顶：  
  - 如果新层和 **大于** 堆顶，说明它应该进入前 `k` 大的集合。于是把堆顶弹出（最小的那一个），再把新层和加入堆。  
  - 如果新层和 **不大于** 堆顶，说明它不可能进入前 `k` 大，直接丢弃。

遍历完所有层后，堆里恰好保存了前 `k` 大的层和，堆顶就是第 `k` 大的那个值。

**为什么只用 `O(k)` 空间就能得到第 `k` 大？**  
- 想象我们在做一次“选拔赛”，只保留成绩最好的 `k` 个人。每次有新选手来，只要比当前最差的（堆顶）好，就把最差的踢出去，保持人数不变。最后留下的就是成绩前 `k` 的选手，最差的那位（堆顶）正好是第 `k` 名。

**实现细节**  

1. 仍然用 BFS（队列）一次遍历整棵树，得到每层的和。  
2. 对每个层和，按上面的规则维护一个大小不超过 `k` 的 **最小堆**（Python 的 `heapq` 默认就是小根堆）。  
3. 遍历结束后：  
   - 如果实际层数 `< k`，返回 `-1`。  
   - 否则堆顶 `heap[0]` 就是第 `k` 大的层和。

#### 代码（Python）

```python
import heapq
from collections import deque
from typing import Optional, List

# ------------------- 二叉树节点定义（同上） -------------------
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

# ------------------- 最优解 -------------------
def kthLargestLevelSum(root: TreeNode, k: int) -> int:
    if not root:
        return -1

    q = deque([root])               # BFS 用的队列
    min_heap: List[int] = []        # 保存当前最大的 k 个层和（小根堆）

    while q:
        level_size = len(q)
        cur_sum = 0
        for _ in range(level_size):
            node = q.popleft()
            cur_sum += node.val
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        # -------- 维护大小为 k 的小根堆 ----------
        if len(min_heap) < k:               # 堆还没满，直接放进去
            heapq.heappush(min_heap, cur_sum)
        else:
            # 堆已满，只有当当前层和更大时才进入前 k
            if cur_sum > min_heap[0]:       # 与堆顶（第 k 小）比较
                heapq.heapreplace(min_heap, cur_sum)
                # heapreplace = pop + push，效率更高

    # 最后检查层数是否足够
    if len(min_heap) < k:
        return -1
    return min_heap[0]          # 堆顶是第 k 大的层和
```

#### 复杂度  

- **时间复杂度**：`O(n log k)`  
  - BFS 仍然是 `O(n)`（每个节点访问一次）。  
  - 对每层和执行堆操作，堆的大小最多是 `k`，插入/替换的代价是 `O(log k)`。  
  - 因此整体是 `O(n log k)`。如果 `k` 远小于层数，这比 `O(n log L)` 要快得多。  

- **空间复杂度**：`O(k)`  
  - 只保存一个大小为 `k` 的堆（加上 BFS 队列的宽度，宽度 ≤ 层数 ≤ `k` 在最坏情况下也不超过 `O(k)`）。  
  - 与暴力解的 `O(L)`（可能是 `O(n)`）相比，节省了大量内存。

---

## 心得

- **核心技巧**：**利用小根堆维护前 K 大**（也叫 “Top‑K” 思路）。  
- **适用题型**  
  1. “返回第 K 大/小的元素”系列（如 LeetCode 215、Kth Largest Element in an Array）。  
  2. “在大量数据中找前 K 名”类问题（如 Top K Frequent Words、K Closest Points to Origin）。  
- **一句话总结解题钥匙**：**只保留必要的 K 个候选，避免对全部数据做完整排序**。

## 反思

- **第一反应**：先想到层序遍历求每层的和，然后想“一刀切”地把所有和排个序。  
- **最容易踩的坑**  
  - **层数不足 k**：一定要在返回前检查堆/列表的长度。  
  - **大数相加可能超出 Python 整数范围**：Python 整数是任意精度的，这里不用担心。  
  - **忘记把子节点加入队列**，导致层次不完整。  
- **下次遇到同类题**：第一步先 **确定只需要前 K**，然后直接考虑 **堆或快速选择**（quickselect）来避免完整排序。这样可以在时间和空间上都更省。