# #876. 链表的中间节点 / Middle of the Linked List

> 难度：简单 · 标签：Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/middle-of-the-linked-list/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list, return the middle node of the linked list.
If there are two middle nodes, return the second middle node.

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5]
Output: [3,4,5]
Explanation: The middle node of the list is node 3.
```

**Example 2:**

```
Input: head = [1,2,3,4,5,6]
Output: [4,5,6]
Explanation: Since the list has two middle nodes with values 3 and 4, we return the second one.
```

**Constraints**

- The number of nodes in the list is in the range [1, 100].
- 1 <= Node.val <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一个单向链表（singly linked list）的头节点 `head`，返回链表的中间节点（middle node）。  
如果链表有两个中间节点，则返回第二个中间节点。

**示例 1**  

**示例 2**  

**约束条件**  
- 链表中节点的数量在区间 `[1, 100]` 内。  
- `1 <= Node.val <= 100`

**示例**  

**示例 1**  
```
Input: head = [1,2,3,4,5]
Output: [3,4,5]
Explanation: 链表的中间节点是值为 3 的节点。
```

**示例 2**  
```
Input: head = [1,2,3,4,5,6]
Output: [4,5,6]
Explanation: 因为链表有两个中间节点，值分别为 3 和 4，我们返回第二个，即值为 4 的节点。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把链表全部保存到数组（或 Python 列表）里**，这样我们就可以像普通数组一样通过下标访问节点。具体步骤如下：

1. 从 `head` 开始遍历链表，把每个节点对象（或节点的值）依次放进一个列表 `nodes`。  
   - 这里的列表就像一本“顺序册子”，第 `i` 页对应链表的第 `i` 个节点。  
2. 计算链表长度 `n = len(nodes)`。  
3. 中间位置的下标是 `n // 2`（整数除法），因为题目要求“如果有两个中间节点，返回后面的那个”，正好对应向下取整的结果。  
4. 直接返回 `nodes[n // 2]` 即可。

> **为什么正确**  
> - 把所有节点都记下来后，顺序不再受链表“只能向前走”的限制。  
> - `n // 2` 正好是从 0 开始计数时的第二个中间位置（当 `n` 为偶数时），符合题意。

#### 代码（Python）

```python
# 定义单链表节点（LeetCode 已经给出，这里仅作说明）
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # 节点保存的数值
        self.next = next    # 指向下一个节点的指针

def middleNode_bruteforce(head: ListNode) -> ListNode:
    """暴力解：把链表装进数组，再直接取中间节点"""
    nodes = []               # 用来顺序保存所有节点，类似“顺序册子”
    cur = head
    while cur:               # 遍历链表，把每个节点加入列表
        nodes.append(cur)    # 把节点对象本身放进去，后面直接返回
        cur = cur.next

    mid_index = len(nodes) // 2   # 整数除法，自动向下取整
    return nodes[mid_index]       # 返回中间节点（第二个中间节点）
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 我们需要遍历一次链表，把 `n` 个节点放进列表，时间随节点数线性增长。  
  - “`O(n)`”可以理解为“如果链表有 10 个节点，就要做大约 10 次基本操作；如果有 1000 个，就要做 1000 次”。  
- **空间复杂度**：`O(n)`  
  - 额外用了一个长度为 `n` 的列表来存节点，随节点数线性增长。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**用了额外的数组**，占用了 `O(n)` 的额外空间。我们可以利用**双指针**（又称快慢指针）在一次遍历中直接找到中间节点，省掉额外存储。

**核心思想**：

- **慢指针 `slow`** 每走一步，**快指针 `fast`** 走两步。  
- 当 `fast` 到达链表末尾（`None`）时，`slow` 正好走到链表的中间。  
- 如果链表长度为偶数，`fast` 会先走到 `None`，此时 `slow` 正好指向**第二个**中间节点，正好满足题目要求。

> **生活类比**：想象两个人在跑道上跑步，慢的每走一步，快的走两步。跑到终点时，慢的正好站在跑道的中点。

**推导过程**：

1. 初始化 `slow = head`、`fast = head`。  
2. 循环条件是 `fast` 和 `fast.next` 都不为空（即快指针还能再走两步）。  
3. 循环体内：`slow = slow.next`（慢指针走一步），`fast = fast.next.next`（快指针走两步）。  
4. 当循环结束时，`slow` 就是所求的中间节点。

#### 代码（Python）

```python
def middleNode_optimal(head: ListNode) -> ListNode:
    """双指针解：一次遍历，O(1) 额外空间"""
    slow = head   # 慢指针，每次移动一步
    fast = head   # 快指针，每次移动两步

    # 只要快指针还能向前走两步，就继续循环
    while fast and fast.next:
        slow = slow.next          # 慢指针前进一步
        fast = fast.next.next     # 快指针前进两步

    # 循环结束时，slow 正好指向中间节点（第二个中间节点）
    return slow
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 仍然只需要遍历一次链表，`n` 为节点数。  
  - 与暴力解的时间相同，但常数更小，因为没有额外的列表操作。  
- **空间复杂度**：`O(1)`  
  - 只使用了两个指针变量，不随 `n` 增长。  
  - 可以理解为“只占用了固定的几块内存”，不管链表有多长都一样。

---

## 心得

- **核心技巧**：**双指针（快慢指针）**，在一次遍历中同步维护两个不同速度的指针，常用于寻找链表中点、检测环等问题。  
- **适用题型**：  
  1. “判断链表是否有环” (`Linked List Cycle`) – 使用快慢指针相遇判断。  
  2. “返回链表的倒数第 k 个节点” (`Remove Nth Node From End of List`) – 先让快指针领先 k 步，再同步移动。  
  3. “删除链表中的重复节点” (`Remove Duplicates from Sorted List`) – 需要遍历并比较相邻节点。  
- **一句话总结**：**让快指针跑两步，慢指针跑一步，快指针到终点时，慢指针正好站在中点**。

---

## 反思

- **第一反应**：把链表全部存到数组里，然后用下标取中间。这个思路直观但不够“优雅”。  
- **最容易踩的坑**：  
  - 循环条件必须写成 `while fast and fast.next:`，否则当链表长度为奇数时会出现 `None.next` 的空指针错误。  
  - 对于只有一个节点的链表，快慢指针初始都指向该节点，循环一次也不进入，直接返回 `head`，符合要求。  
- **下次类似题的第一步**：先思考“有没有一种只遍历一次、只用常数空间的办法？”——通常快慢指针是首选思路。