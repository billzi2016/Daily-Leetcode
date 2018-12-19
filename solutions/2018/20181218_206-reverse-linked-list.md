# #206. 反转链表 / Reverse Linked List

> 难度：简单 · 标签：Linked List、Recursion · [LeetCode 链接](https://leetcode.com/problems/reverse-linked-list/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list, reverse the list, and return the reversed list.
Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
```

**Example 2:**

```
Input: head = [1,2]
Output: [2,1]
```

**Example 3:**

```
Input: head = []
Output: []
```

**Constraints**

- The number of nodes in the list is the range [0, 5000].
- -5000 <= Node.val <= 5000

---

## 题目（中文翻译）

给定单向链表（singly linked list）的头节点 `head`，请将链表进行反转，并返回反转后的链表。

**示例 1：**  
**示例 2：**  
**示例 3：**  

**进阶：** 链表可以通过迭代或递归的方式进行反转。你能实现这两种方法吗？

### 示例

**示例 1**  
输入: `head = [1,2,3,4,5]`  
输出: `[5,4,3,2,1]`

**示例 2**  
输入: `head = [1,2]`  
输出: `[2,1]`

**示例 3**  
输入: `head = []`  
输出: `[]`

### 约束条件

- 链表中节点的数量范围为 `[0, 5000]`。  
- `-5000 <= Node.val <= 5000`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直观的想法是**先把链表的所有节点值读出来放进一个 Python 列表**（相当于把链表的内容抄到纸上），再**按照倒序把这些值重新创建成新的链表**。  
- **列表**就像一本记事本，`list[i]` 能直接拿到第 *i* 条记录，查找速度非常快，类似“查字典”。  
- 这个方法一定能得到正确答案，因为我们没有改变原链表的结构，只是把值重新排列后再组装成新链表，顺序自然是反的。  

不过，这种做法用了额外的存储空间来保存所有节点的值，所以不是最省空间的做法。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点保存的数值
        self.next = next        # 指向下一个节点的指针

def reverseList_brute(head: ListNode) -> ListNode:
    """暴力版：借助额外的列表存值，然后重新构造链表"""
    # 1. 把所有值读取到 Python 列表中
    vals = []
    cur = head
    while cur:                # 当 cur 不是 None 时循环
        vals.append(cur.val)  # 把当前节点的值加入列表
        cur = cur.next        # 移动到下一个节点

    # 2. 根据倒序的值重新创建链表
    dummy = ListNode()        # 哑节点，帮助我们简化链表的创建
    cur = dummy
    for v in reversed(vals):  # reversed 会把列表倒着遍历
        cur.next = ListNode(v)  # 创建新节点并接在当前节点后面
        cur = cur.next          # 移动指针

    return dummy.next          # 哑节点的下一个才是真正的头节点
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：我们遍历链表一次把值存进列表，又遍历列表一次把节点重新创建，总共是 `n + n = 2n` 步，数量级记作 `O(n)`，也就是“随节点数线性增长”。  
- **空间复杂度**：`O(n)`  
  解释：我们额外用了一个长度为 `n` 的 Python 列表来存所有节点的值，和原链表的大小成正比，所以是 `O(n)` 的额外空间。

---

### 2. 最优解

#### 思路  
**瓶颈**在于暴力解使用了额外的列表，占用了 `O(n)` 的空间。  
链表的本质是**指针**（`next`）把节点一个接一个串起来，我们只要把这些指针的方向全部翻转，就可以在 **原地**（不新建节点）得到反向链表。

**核心技巧：三指针翻转**  
- `prev`：当前节点翻转后应该指向的前一个节点（最开始是 `None`，因为新链表的尾部要指向空）。  
- `cur`：正在处理的节点。  
- `next_tmp`：`cur` 原来的下一个节点（因为翻转指针后我们会失去这个信息，需要先保存）。  

处理过程可以想象成**把链表拆成两段**：左边已经翻转好的部分，右边是还未处理的剩余部分。每一步把右边的第一个节点搬到左边的最前面，直到右边为空。  

**递归版思路**  
递归本质上也是把问题拆成「把后面的子链表反转」+「把当前节点接到子链表后面」两步。递归的调用栈会保存每一次的 `head`，相当于隐式的「指针栈」，所以代码更简洁，但会占用 `O(n)` 的栈空间。

#### 代码（Python）

```python
# Definition for singly-linked list (保持不变)
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# ---------- 迭代版（空间 O(1)） ----------
def reverseList_iter(head: ListNode) -> ListNode:
    """使用三指针在原链表上就地翻转"""
    prev = None          # 翻转后当前节点的前驱，最开始是空
    cur = head           # 从头节点开始遍历
    while cur:
        next_tmp = cur.next   # 先保存下一个节点，防止指针翻转后找不到后继
        cur.next = prev       # 翻转指针：当前节点指向前一个节点
        prev = cur            # prev 前进到当前节点
        cur = next_tmp        # cur 前进到原来的下一个节点
    # 当 while 结束时，prev 正好指向新的头节点
    return prev

# ---------- 递归版（空间 O(n) 递归栈） ----------
def reverseList_recursive(head: ListNode) -> ListNode:
    """递归方式翻转链表，返回新的头节点"""
    # 递归终止条件：空链表或只有一个节点，不需要翻转
    if not head or not head.next:
        return head

    # 递归翻转子链表，new_head 是翻转后子链表的头节点
    new_head = reverseList_recursive(head.next)

    # 把当前节点接到子链表的尾部（即原来 head.next 的 next）
    head.next.next = head   # 把原来的后继节点指向当前节点
    head.next = None        # 当前节点的 next 置空，成为新尾部

    return new_head
```

#### 复杂度  

- **迭代版**  
  - 时间复杂度：`O(n)`  
    只遍历一次链表，每个节点做常数次指针操作。  
  - 空间复杂度：`O(1)`  
    只用了 `prev、cur、next_tmp` 三个指针，不随 `n` 增长。  

- **递归版**  
  - 时间复杂度：`O(n)`（同理，遍历一次）  
  - 空间复杂度：`O(n)`  
    递归调用会在系统栈中保存 `n` 层函数调用，每层占用一定空间。  

> 与暴力解对比：时间相同，但迭代版把空间从 `O(n)` 降到了 `O(1)`，更高效。

---

## 心得

- **核心技巧**：链表的指针翻转（迭代的“三指针”或递归的“后序处理”）。  
- **适用题型**：  
  1. 反转链表（LeetCode 206）  
  2. 反转链表的子区间（LeetCode 92 – Reverse Linked List II）  
  3. 两两交换链表节点（LeetCode 24 – Swap Nodes in Pairs）  
- **一句话总结**：**把“指向后一个”的箭头改成“指向前一个”，一步步把链表倒着拼起来。**

---

## 反思

- **第一反应**：先把所有节点的值复制到数组里再倒着重建——因为数组的随机访问很直观。  
- **最容易踩的坑**：  
  - 忘记在迭代过程中先保存 `next`，导致指针翻转后链表断裂。  
  - 递归终止条件写错，出现无限递归。  
  - 没有处理空链表或只有一个节点的特殊情况。  
- **下次思路**：一看到“链表翻转”关键词，立刻想到**原地指针翻转**（迭代）或**后序递归**，先判断是否可以在 O(1) 空间内完成，再决定实现方式。