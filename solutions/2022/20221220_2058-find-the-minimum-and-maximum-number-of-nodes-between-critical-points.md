# #2058. 查找关键点之间的最小和最大节点数 / Find the Minimum and Maximum Number of Nodes Between Critical Points

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/)

---

## 题目（英文原版）

**Description**

A critical point in a linked list is defined as either a local maxima or a local minima.
A node is a local maxima if the current node has a value strictly greater than the previous node and the next node.
A node is a local minima if the current node has a value strictly smaller than the previous node and the next node.
Note that a node can only be a local maxima/minima if there exists both a previous node and a next node.
Given a linked list head, return an array of length 2 containing [minDistance, maxDistance] where minDistance is the minimum distance between any two distinct critical points and maxDistance is the maximum distance between any two distinct critical points. If there are fewer than two critical points, return [-1, -1].

**Examples**

**Example 1:**

```
Input: head = [3,1]
Output: [-1,-1]
Explanation: There are no critical points in [3,1].
```

**Example 2:**

```
Input: head = [5,3,1,2,5,1,2]
Output: [1,3]
Explanation: There are three critical points:
- [5,3,1,2,5,1,2]: The third node is a local minima because 1 is less than 3 and 2.
- [5,3,1,2,5,1,2]: The fifth node is a local maxima because 5 is greater than 2 and 1.
- [5,3,1,2,5,1,2]: The sixth node is a local minima because 1 is less than 5 and 2.
The minimum distance is between the fifth and the sixth node. minDistance = 6 - 5 = 1.
The maximum distance is between the third and the sixth node. maxDistance = 6 - 3 = 3.
```

**Example 3:**

```
Input: head = [1,3,2,2,3,2,2,2,7]
Output: [3,3]
Explanation: There are two critical points:
- [1,3,2,2,3,2,2,2,7]: The second node is a local maxima because 3 is greater than 1 and 2.
- [1,3,2,2,3,2,2,2,7]: The fifth node is a local maxima because 3 is greater than 2 and 2.
Both the minimum and maximum distances are between the second and the fifth node.
Thus, minDistance and maxDistance is 5 - 2 = 3.
Note that the last node is not considered a local maxima because it does not have a next node.
```

**Constraints**

- The number of nodes in the list is in the range [2, 105].
- 1 <= Node.val <= 105

---

## 题目（中文翻译）

A **critical point（关键点）** 在链表（linked list）中被定义为局部最大值（local maxima）或局部最小值（local minima）。  
- 当当前节点的值严格大于前一个节点和后一个节点的值时，该节点是局部最大值。  
- 当当前节点的值严格小于前一个节点和后一个节点的值时，该节点是局部最小值。  

注意，只有当节点同时存在前驱节点和后继节点时，它才可能是局部最大值或局部最小值。  

给定链表的 `head`，返回长度为 2 的数组 `[minDistance, maxDistance]`，其中  
- `minDistance` 为任意两个不同关键点之间的最小距离，  
- `maxDistance` 为任意两个不同关键点之间的最大距离。  

如果关键点少于两个，返回 `[-1, -1]`。

---

### 示例

**Example 1:**  
**Input:** `head = [3,1]`  
**Output:** `[-1,-1]`  
**Explanation:** 在 `[3,1]` 中没有关键点。

**Example 2:**  
**Input:** `head = [5,3,1,2,5,1,2]`  
**Output:** `[1,3]`  
**Explanation:** 存在三个关键点：
- 第三个节点是局部最小值，因为 `1` 小于 `3` 和 `2`。  
- 第五个节点是局部最大值，因为 `5` 大于 `2` 和 `1`。  
- 第六个节点是局部最小值，因为 `1` 小于 `5` 和 `2`。  

最小距离出现在第五个节点和第六个节点之间，距离为 `1`。  
最大距离出现在第三个节点和第六个节点之间，距离为 `3`。

**Example 3:**  
**Input:** `head = [1,3,2,2,3,2,2,2,7]`  
**Output:** `[3,3]`  
**Explanation:** 存在两个关键点：
- 第二个节点是局部最大值，因为 `3` 大于 `1` 和 `2`。  
- 第五个节点是局部最大值，因为 `3` 大于 `2` 和 `2`。  

最小距离和最大距离均为这两个关键点之间的距离，即 `5 - 2 = 3`。

---

### 约束条件

- 链表中的节点数在区间 `[2, 10^5]` 内。  
- `1 <= Node.val <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：先把链表的所有节点全部保存到一个 Python 列表 `nodes` 中（相当于把一条长长的“链子”平铺成一排），  
随后遍历 `nodes`，判断每个节点（除了第一个和最后一个）是否是 **局部极大** 或 **局部极小**——这一步只需要比较它左边和右边的值。  

把所有满足条件的下标（在 `nodes` 中的位置）记下来，得到 `critical_indices`。  
如果关键点少于 2 个，直接返回 `[-1, -1]`。  

否则，使用**双层循环**遍历 `critical_indices` 中的每一对关键点，计算它们的距离（下标相减的绝对值），并维护全局的最小距离 `min_dist` 与最大距离 `max_dist`。  

> **类比**：  
> - 哈希表像是一本“查字典”，这里我们不需要哈希表，只是把链表“摊平”成普通数组，像把一本书的每页都拍成照片，方便我们随时翻到任意页。  
> - 双层循环就像让每个人分别和其他所有人握手，找出最近和最远的两个人，时间会比较长。  

**为什么正确**：  
- 只要遍历到了每一个节点，就一定能判断它是否是局部极值；  
- 记录所有关键点后，遍历所有关键点对能够得到**所有可能的距离**，从而找出最小和最大值。  

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def nodes_to_array(head):
    """把链表摊平成数组，返回 [node, index] 列表"""
    arr = []
    idx = 0
    cur = head
    while cur:
        arr.append((cur, idx))   # (节点对象, 在链表中的下标)
        cur = cur.next
        idx += 1
    return arr


def find_min_max_critical_bruteforce(head):
    """暴力解：O(n^2) 时间，O(n) 空间"""
    if not head:
        return [-1, -1]

    nodes = nodes_to_array(head)               # 把链表放进普通列表
    n = len(nodes)

    # 1️⃣ 找出所有关键点的下标
    critical_idx = []
    for i in range(1, n - 1):                  # 只有前后都有节点的才可能是关键点
        prev_val = nodes[i - 1][0].val
        cur_val = nodes[i][0].val
        next_val = nodes[i + 1][0].val
        if (cur_val > prev_val and cur_val > next_val) or \
           (cur_val < prev_val and cur_val < next_val):
            critical_idx.append(i)            # 记录下标

    # 2️⃣ 少于两个关键点直接返回
    if len(critical_idx) < 2:
        return [-1, -1]

    # 3️⃣ 双层循环遍历所有关键点对，求最小/最大距离
    min_dist = float('inf')
    max_dist = -1
    m = len(critical_idx)
    for i in range(m):
        for j in range(i + 1, m):
            dist = abs(critical_idx[j] - critical_idx[i])
            min_dist = min(min_dist, dist)
            max_dist = max(max_dist, dist)

    return [min_dist, max_dist]
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `n` 是链表节点数。我们先遍历一次得到所有关键点（`O(n)`），随后对关键点的每一对进行比较，最坏情况下关键点数量接近 `n`，于是需要 `n × n` 次比较。  
  - 用“大白话”说，就是“如果链表有 10,000 条数据，暴力解大概要算 100,000,000 次”。  

- **空间复杂度**：`O(n)`  
  - 需要一个额外的列表把链表全部复制下来，最多存 `n` 个节点的引用。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于**两层循环**——我们在重复计算已经知道的距离。  
观察题目要求的两个值：

1. **最大距离** 必然是**第一个关键点**和**最后一个关键点**之间的距离。  
2. **最小距离** 只需要在**相邻关键点**之间寻找最小差值，因为如果两点之间还有其他关键点，距离会更大。

因此，只要在一次遍历链表的过程中：

- 记录下每个关键点出现的**下标**（相对于链表头的顺序）。  
- 用 `first_idx` 保存第一个关键点的下标，`prev_idx` 保存上一次出现的关键点下标，`last_idx` 保存遍历结束时的关键点下标。  
- 每遇到一个新的关键点，就用 `cur_idx - prev_idx` 更新 `min_dist`（相邻关键点的距离），并把 `prev_idx` 移到当前下标。  

遍历结束后：

- 如果关键点数量 < 2 → `[-1, -1]`。  
- 否则 `max_dist = last_idx - first_idx`（最远的两个关键点），`min_dist` 已在遍历中求得。

> **类比**：  
> - 把链表想象成一条路，关键点是路上的加油站。最大距离就是从第一个加油站到最后一个加油站的路程；最小距离就是最近的两个相邻加油站之间的距离。我们只需要一次开车走完这条路，顺手记下每次加油站出现的位置，就能得到答案。  

**核心技巧**：**一次遍历 + 记录首尾 + 只比较相邻关键点**。这属于**单指针/一次扫描**的技巧，常用于求“最远/最近”这类问题。  

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def find_min_max_critical_optimal(head: ListNode):
    """
    最优解：只遍历一次链表，时间 O(n)，空间 O(1)。
    返回 [minDistance, maxDistance]，若关键点不足两个返回 [-1, -1]。
    """
    if not head or not head.next:
        return [-1, -1]

    # 初始化
    index = 0                     # 当前节点在链表中的下标（从 0 开始）
    prev = head                   # 前一个节点（用来判断极值）
    cur = head.next               # 当前节点
    next_node = cur.next          # 后一个节点（可能为空）

    first_idx = -1                # 第一个关键点的下标
    last_idx = -1                 # 最近一次出现的关键点的下标
    prev_crit_idx = -1            # 上一个关键点的下标（用于计算相邻距离）
    min_dist = float('inf')       # 当前已知的最小距离

    while next_node:              # 只要后面还有节点，就可以判断 cur 是否为关键点
        # 判断 cur 是否为局部极大或极小
        if (cur.val > prev.val and cur.val > next_node.val) or \
           (cur.val < prev.val and cur.val < next_node.val):
            # cur 是关键点，记录下标（此时 index 对应 cur）
            if first_idx == -1:               # 第一次遇到关键点
                first_idx = index
            else:
                # 与上一个关键点比较距离，更新最小距离
                min_dist = min(min_dist, index - prev_crit_idx)
            # 更新上一个关键点的下标
            prev_crit_idx = index
            # 记录最新的关键点位置（用于最后的最大距离）
            last_idx = index

        # 向前移动指针，准备检查下一个三元组
        prev, cur, next_node = cur, next_node, next_node.next
        index += 1

    # 关键点不足两个
    if first_idx == -1 or first_idx == last_idx:
        return [-1, -1]

    max_dist = last_idx - first_idx   # 最远的两个关键点之间的距离
    return [min_dist, max_dist]
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次链表，每个节点做常数次比较和赋值。  
  - 用“大白话”说，就是“链表有 100,000 条数据，只需要走一遍，算的次数跟节点数成正比”。  

- **空间复杂度**：`O(1)`  
  - 只用了若干个整数变量来记录下标和距离，和链表长度无关。  
  - 也就是说，不管链表有多长，额外占用的内存基本保持不变。  

---

## 心得  

- **核心技巧**：一次遍历中记录首个、最近、上一个关键点下标，利用“相邻关键点最小、首尾关键点最大”这两个性质。  
- **该技巧适用的题型**  
  1. “链表/数组中相邻满足条件的元素之间的最小/最大距离”  
     - 例：**Maximum Distance Between Two Consecutive Ones**（数组中 1 的最大间距）  
  2. “求首尾满足某种属性的元素之间的距离”  
     - 例：**Maximum Width of Binary Tree**（记录最左、最右节点）  
- **一句话总结解题钥匙**：**只要把“关键点的位置”记下来，最小距离看相邻，最大距离看首尾**。  

---

## 反思  

- **第一反应**：把链表全部存进数组，然后用两层循环暴力比较。  
- **最容易踩的坑**  
  1. **边界条件**：链表长度 < 3 时根本不可能出现关键点，需要提前返回 `[-1, -1]`。  
  2. **判断极值时忘记“严格大于/小于”**，相等的情况不算关键点。  
  3. **下标的维护**：在遍历时 `index` 必须对应当前 `cur` 节点，否则计算距离会错位。  
- **下次遇到同类题的第一步**：先明确“关键点”或“满足条件的元素”在一次遍历中能否直接记录位置；如果可以，立刻用**首尾 + 相邻**的思路求最小/最大距离，避免二次循环。