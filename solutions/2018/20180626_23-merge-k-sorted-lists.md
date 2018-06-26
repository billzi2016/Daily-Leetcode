# #23. 合并 k 个已排序链表 / Merge k Sorted Lists

> 难度：困难 · 标签：Linked List、Divide and Conquer、Heap (Priority Queue)、Merge Sort · [LeetCode 链接](https://leetcode.com/problems/merge-k-sorted-lists/)

---

## 题目（英文原版）

**Description**

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

**Examples**

**Example 1:**

```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6
```

**Example 2:**

```
Input: lists = []
Output: []
```

**Example 3:**

```
Input: lists = [[]]
Output: []
```

**Constraints**

- k == lists.length
- 0 <= k <= 104
- 0 <= lists[i].length <= 500
- -104 <= lists[i][j] <= 104
- lists[i] is sorted in ascending order.
- The sum of lists[i].length will not exceed 104.

---

## 题目（中文翻译）

给定一个长度为 k 的数组（array） `lists`，其中每个元素都是一个已按升序排序的链表（linked-list）。  
请将所有链表合并为一个已排序的链表（linked-list），并返回该链表。

**示例 1**  
Input: lists = [[1,4,5],[1,3,4],[2,6]]  
Output: [1,1,2,3,4,4,5,6]  
Explanation: 给出的链表如下：  
```
[
  1->4->5,
  1->3->4,
  2->6
]
```  
将它们合并后得到的升序链表为：  
```
1->1->2->3->4->4->5->6
```

**示例 2**  
Input: lists = []  
Output: []  

**示例 3**  
Input: lists = [[]]  
Output: []  

**约束条件**  

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` 已按升序排序。
- 所有 `lists[i].length` 之和不超过 `10^4`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有链表的节点“摘下来”，放进一个普通的 Python 列表里，然后一次性排序，最后再把排好序的值重新串成一条链表返回。

- **用到的数据结构**  
  - **列表**（list）：就像我们平时用的装东西的盒子，能够随意添加、删除元素。  
  - **链表节点**（`ListNode`）：每个节点相当于一张纸条，上面写着一个数字（`val`）和指向下一张纸条的指针（`next`）。把这些纸条按顺序贴在一起就形成了链表。  

- **为什么正确**  
  把所有节点的值都收集到一起后，使用 Python 自带的 `sort()`（底层是 **归并排序** / **快排**）就可以得到一个严格递增的序列。把这个序列重新装进链表，自然就是题目要求的“合并后仍然有序”的链表。

- **时间/空间复杂度**  
  - **时间复杂度**：设所有链表总共包含 `N` 个节点。把节点值收集进列表是 `O(N)`，排序是 `O(N log N)`（`log` 表示对数，直观理解就是“把 N 分成一半、再把每半分成一半…”的层数），最后重建链表又是 `O(N)`，整体是 `O(N log N)`。  
  - **空间复杂度**：我们额外用了一个长度为 `N` 的列表来存放所有值，还需要几个指针变量，整体是 `O(N)` 的额外空间。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x: int):
        self.val = x          # 节点保存的数值
        self.next = None      # 指向下一个节点的指针

def mergeKLists(lists):
    """
    暴力解法：收集所有节点值，排序后重建链表
    :type lists: List[ListNode]
    :rtype: ListNode
    """
    values = []                     # 用来装所有节点值的列表
    for head in lists:              # 遍历每一条链表
        cur = head
        while cur:                  # 把链表展开成数组
            values.append(cur.val) # 把值加入数组
            cur = cur.next

    if not values:                  # 所有链表为空的情况
        return None

    values.sort()                   # 对所有值进行升序排序

    # 根据排好序的数组重新创建链表
    dummy = ListNode(0)             # 哑节点，帮助我们省去判断头结点的代码
    cur = dummy
    for v in values:
        cur.next = ListNode(v)      # 创建新节点并接在当前节点后面
        cur = cur.next

    return dummy.next               # 哑节点的下一个就是我们真正的头结点
```

#### 复杂度

- **时间复杂度**：`O(N log N)` —— 先收集 `N` 条数据是线性时间 `O(N)`，排序是 `O(N log N)`，整体受排序支配。  
- **空间复杂度**：`O(N)` —— 需要额外存放 `N` 个整数的列表。

---

### 2. 最优解

#### 思路  

从暴力解来看，耗时的主要“瓶颈”在 **排序** 步骤。我们其实不必把所有节点一次性收集再排序，只要在**合并的过程中始终挑出当前最小的节点**，就可以直接构造出有序链表。

> **核心想法**：把每条链表的“当前头结点”放进一个**最小堆**（priority queue）。堆是一种特殊的容器，能够在 `O(log k)` 的时间内把最小元素弹出（`k` 是堆里元素的个数）。这就像在超市排队结账，最先结账的总是排在最前面的那个人。

**步骤**：

1. **初始化堆**  
   把每条非空链表的第一个节点（即头结点）放进堆里。堆的大小最多是 `k`（链表的条数），因为每条链表最多只会有一个“当前节点”在堆中。

2. **循环取最小**  
   - 弹出堆顶（最小值）节点，将它接到答案链表的尾部。  
   - 如果弹出的节点还有后继（`node.next != None`），把后继节点再放进堆里。这样堆里始终保持着每条链表“当前最前面的未合并节点”。

3. **结束**  
   当堆为空时，说明所有节点都已经被取出并接入答案链表，返回答案即可。

**为什么是最优的**  
- 每次弹出最小值的代价是 `log k`，而不是 `log N`（因为堆里只装 `k` 条链表的当前节点）。  
- 总共要弹出 `N` 次（每个节点恰好弹出一次），所以时间复杂度是 `O(N log k)`，这比 `O(N log N)` 更快，尤其当 `k << N` 时优势明显。  
- 额外空间只用了堆，最多装 `k` 个节点，空间复杂度是 `O(k)`。

> **类比**：想象有 `k` 条队伍，每条队伍的成员已经按身高从低到高排好。我们要把所有人按身高排成一列，只需要每次看每条队伍最前面的那个人，挑出最矮的，放进大队列，然后把被挑出的人所在队伍的下一个人送进“候选池”。这正是堆的工作方式。

#### 代码（Python）

```python
import heapq   # Python 标准库里的堆实现（最小堆）

class ListNode:
    def __init__(self, x: int):
        self.val = x
        self.next = None

class Wrapper:
    """
    因为 heapq 要比较堆中元素的大小，而 ListNode 本身没有实现比较运算符，
    我们包装一下，让堆只比较节点的值 (val)。如果值相同，Python 仍需要比较
    两个对象，为了防止 TypeError，这里再加一个唯一的计数器。
    """
    __slots__ = ('node', 'idx')
    def __init__(self, node, idx):
        self.node = node
        self.idx = idx          # 唯一标识，保证堆中元素可比较

    def __lt__(self, other):
        # 先比较节点值，值相同再比较唯一标识
        if self.node.val == other.node.val:
            return self.idx < other.idx
        return self.node.val < other.node.val

def mergeKLists(lists):
    """
    最优解：利用最小堆始终弹出当前最小节点
    :type lists: List[ListNode]
    :rtype: ListNode
    """
    heap = []                     # 用来存放堆元素的列表
    counter = 0                   # 为每个节点生成唯一序号

    # 1️⃣ 把每条链表的头结点放进堆（如果该链表非空）
    for head in lists:
        if head:                  # 只处理非空链表
            heapq.heappush(heap, Wrapper(head, counter))
            counter += 1

    dummy = ListNode(0)           # 哑节点，方便统一处理头结点
    cur = dummy

    # 2️⃣ 循环弹出最小节点并维护堆
    while heap:
        smallest = heapq.heappop(heap).node   # 取出堆顶节点
        cur.next = smallest                    # 接到答案链表
        cur = cur.next

        if smallest.next:                      # 若弹出节点还有后继
            heapq.heappush(heap, Wrapper(smallest.next, counter))
            counter += 1

    return dummy.next               # 返回真实的头结点
```

#### 复杂度

- **时间复杂度**：`O(N log k)` —— 总共弹出 `N` 次，每次堆操作 `log k`，所以整体是 `N` 与 `log k` 的乘积。相比暴力解的 `O(N log N)`，当 `k`（链表数量）远小于 `N` 时更快。  
- **空间复杂度**：`O(k)` —— 堆里最多同时保存 `k` 个节点（每条链表的当前头），额外空间随 `k` 线性增长。

---

## 心得

- **核心技巧**：**最小堆（优先队列）** 用来在多路有序序列中快速取最小值。  
- **适用的题型**：  
  1. 合并多个有序数组/链表（如本题）。  
  2. “找第 K 小的数”——在两个有序数组中使用堆找第 K 小元素。  
  3. “滑动窗口最大/最小值”——利用单调队列（也是一种特殊的堆）实现。  
- **一句话总结解题钥匙**：**把“每条序列的当前最小候选”放进堆，循环弹最小并补新候选**。

---

## 反思

- **第一反应**：直接把所有节点收集到列表里排序，代码最简单。  
- **最容易踩的坑**：  
  - `ListNode` 不能直接放进 `heapq`（没有定义 `<`），需要包装或自定义比较。  
  - 处理空链表的情况：`lists = []`、`lists = [[]]` 都要返回 `None`（空链表）。  
  - 当多个节点值相同，堆比较会报错，需要额外的唯一标识（如计数器）来打破平局。  
- **下次遇到同类题**：第一步先思考“我能否在合并过程中随时拿到最小元素”，如果答案是“可以”，就考虑使用最小堆或双指针等结构。这样往往能直接得到 `O(N log k)` 的高效方案。