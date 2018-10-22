# #141. **链表环** / Linked List Cycle

> 难度：简单 · 标签：Hash Table、Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/linked-list-cycle/)

---

## 题目（英文原版）

**Description**

Given head, the head of a linked list, determine if the linked list has a cycle in it.
There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.
Return true if there is a cycle in the linked list. Otherwise, return false.
Follow up: Can you solve it using O(1) (i.e. constant) memory?

**Examples**

**Example 1:**

```
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
```

**Example 2:**

```
Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
```

**Example 3:**

```
Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.
```

**Constraints**

- The number of the nodes in the list is in the range [0, 104].
- -105 <= Node.val <= 105
- pos is -1 or a valid index in the linked-list.

---

## 题目（中文翻译）

给定 `head`，即链表的头节点，判断该链表是否存在环（cycle）。如果链表中存在某个节点，在持续沿着 `next` 指针遍历时能够再次到达该节点，则链表中存在环。内部使用 `pos` 表示 `tail`（链表尾节点）的 `next` 指针所指向的节点下标。注意 `pos` 并不会作为函数参数传入。

- 如果链表中存在环，返回 `true`；
- 否则返回 `false`。

**示例 1**  
**示例 2**  
**示例 3**

**进阶**：能否使用 O(1)（即常数）额外空间解决此问题？

### 示例

**示例 1**  
```
Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: 链表中存在环，尾节点指向第 1 个节点（0 起始索引）。
```

**示例 2**  
```
Input: head = [1,2], pos = 0
Output: true
Explanation: 链表中存在环，尾节点指向第 0 个节点。
```

**示例 3**  
```
Input: head = [1], pos = -1
Output: false
Explanation: 链表中不存在环。
```

### 约束条件

- 链表中节点的数量在 `[0, 10^4]` 范围内。
- `-10^5 <= Node.val <= 10^5`
- `pos` 为 `-1` 或者是链表中的有效下标。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是「把遍历过的结点都记下来」，每走到一个结点，就检查它是否已经出现过。  
- **用到的数据结构**：哈希表（`set`），可以把它想象成一本「词典」：单词（结点的唯一标识）对应页码（是否已经出现）。查找一个单词是否在词典里，时间几乎是 **O(1)**，因为哈希表内部会把单词直接映射到对应的存储位置。  
- **正确性**：如果链表里有环，必然会在环中某个结点第二次被访问到；这时我们在哈希表里已经看到过该结点，就可以立刻返回 `True`。如果遍历完整条链表都没有重复出现的结点，则说明没有环，返回 `False`。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    visited = set()               # 用集合记录已经访问过的结点（相当于词典）
    cur = head
    while cur:
        if cur in visited:        # 该结点已经出现过 → 环
            return True
        visited.add(cur)          # 把当前结点加入集合，标记为已访问
        cur = cur.next            # 移动到下一个结点
    return False                  # 遍历结束都没有重复，说明没有环
```

#### 复杂度
- **时间复杂度**：`O(n)`  
  每个结点最多访问一次，`n` 为链表长度。  
- **空间复杂度**：`O(n)`  
  最坏情况下要把所有结点都放进哈希表，使用的额外内存随结点数线性增长。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **空间**：我们用了额外的哈希表保存所有已访问的结点。  
要做到 **O(1)** 额外空间，需要在不额外记录结点的情况下，仍然能判断是否出现环。  
这里可以利用「**快慢指针**」的技巧（又叫 **Floyd 判圈算法**）：

1. **设两只指针**  
   - **慢指针** `slow` 每次走一步。  
   - **快指针** `fast` 每次走两步。  
   可以把它们想象成两个人在跑道上跑步，快的那个人每次跨两格，慢的每次跨一格。

2. **为什么会相遇**  
   - 如果链表没有环，快指针最终会跑到 `None`（链表尾），两指针永不相遇。  
   - 如果有环，快指针在环里跑得更快，必然会在环内「追上」慢指针——就像在圆形跑道上跑得更快的选手必定会追上慢的选手。相遇的那一刻，说明链表中存在环。

3. **实现细节**  
   - 在每一步循环前，先检查 `fast` 和 `fast.next` 是否为 `None`，防止空指针异常。  
   - 当 `slow is fast` 成立时，直接返回 `True`。  
   - 循环结束后仍未相遇，则返回 `False`。

#### 代码（Python）

```python
def hasCycle(head: ListNode) -> bool:
    # 0 或 1 个结点时不可能有环
    if not head or not head.next:
        return False

    slow = head          # 慢指针：每次走 1 步
    fast = head.next     # 快指针：先走一步，后面每次走 2 步

    while fast and fast.next:
        if slow is fast:               # 两指针相遇 → 环
            return True
        slow = slow.next              # 慢指针走 1 步
        fast = fast.next.next         # 快指针走 2 步

    return False                       # 快指针走到链表末尾 → 没有环
```

#### 复杂度
- **时间复杂度**：`O(n)`  
  每个结点最多被快指针和慢指针访问一次，整体仍是线性时间。  
- **空间复杂度**：`O(1)`  
  只用了固定的几个指针变量，额外内存不随链表大小变化。

---

## 心得

- **核心技巧**：快慢指针（Floyd 判圈）— 通过让两个指针以不同速度遍历，利用「相遇必然」的性质检测环。  
- **适用的题型**：  
  1. 判断链表是否有环（本题）。  
  2. 找到环的入口节点（`Linked List Cycle II`）。  
  3. 判断数组是否存在重复数且满足「快慢指针」的等价条件（`Find the Duplicate Number`）。  
- **一句话总结**：让快指针追上慢指针，就是环的“探测器”。

## 反思

- **第一反应**：直接用集合记住访问过的结点，想到「哈希表」能快速判断重复。  
- **最容易踩的坑**：  
  - 忘记在循环前检查 `fast` 或 `fast.next` 是否为 `None`，会导致空指针异常。  
  - 对只有 0/1 个结点的链表没有特殊处理，会误判。  
- **下次遇到同类题**：第一步先思考「能否用两个指针的相对速度来捕获循环」，如果可以，就直接尝试快慢指针；如果不行，再考虑额外的存储（哈希表）。