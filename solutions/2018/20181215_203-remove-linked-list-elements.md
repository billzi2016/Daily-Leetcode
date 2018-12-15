# #203. 删除链表元素 / Remove Linked List Elements

> 难度：简单 · 标签：Linked List、Recursion · [LeetCode 链接](https://leetcode.com/problems/remove-linked-list-elements/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list and an integer val, remove all the nodes of the linked list that has Node.val == val, and return the new head.

**Examples**

**Example 1:**

```
Input: head = [1,2,6,3,4,5,6], val = 6
Output: [1,2,3,4,5]
```

**Example 2:**

```
Input: head = [], val = 1
Output: []
```

**Example 3:**

```
Input: head = [7,7,7,7], val = 7
Output: []
```

**Constraints**

- The number of nodes in the list is in the range [0, 104].
- 1 <= Node.val <= 50
- 0 <= val <= 50

---

## 题目（中文翻译）

给定一个链表（linked list）的头节点（head）和一个整数（val），删除链表中所有满足 `Node.val == val` 的节点（node），并返回新的头节点。

示例 1:
```
Input: head = [1,2,6,3,4,5,6], val = 6
Output: [1,2,3,4,5]
```

示例 2:
```
Input: head = [], val = 1
Output: []
```

示例 3:
```
Input: head = [7,7,7,7], val = 7
Output: []
```

约束条件：
- 链表中节点的数量在 `[0, 10^4]` 区间内。
- `1 <= Node.val <= 50`
- `0 <= val <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
我们先把链表想成“一串珠子”，每个珠子都有一个数字（`Node.val`），相邻的珠子之间有一根细线（`Node.next`）把它们串起来。  
题目要求把所有数字等于给定 `val` 的珠子全部摘掉，剩下的珠子仍然要保持原来的顺序。

最直接的想法就是 **从头到尾一次遍历**，每看到一个节点就判断它的值是否等于 `val`：

- 如果不相等，就什么也不做，继续往后走；
- 如果相等，就把它从链表中“剪掉”。剪掉的意思是让前一个节点的 `next` 指向当前节点的 `next`，相当于把当前珠子从串里挑出来。

为了实现“前一个节点”，我们在遍历时需要记住 **上一个节点**（`prev`）。另外，链表的头结点本身也可能被删除，这种情况比较麻烦，因为没有“前一个节点”。一种常见的技巧是**在链表最前面再造一个哑结点（dummy node）**，它的 `next` 指向原来的头结点，这样即使原头结点被删掉，哑结点也能帮我们完成链接。

> **类比**：哑结点就像一本书的封面，封面本身不算章节，但它指向第一章。即使第一章被删掉，封面仍然可以把我们带到第二章。

只要遍历一次就能把所有满足条件的节点全部去掉，这就是“暴力”解法——直接、最符合直觉的做法。

#### 代码（Python）

```python
# 定义单链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点的数值
        self.next = next        # 指向下一个节点的指针

def removeElements(head: ListNode, val: int) -> ListNode:
    # 1. 创建哑结点，next 指向原链表头部
    dummy = ListNode(next=head)   # 哑结点的值随意，这里默认 0
    prev = dummy                  # prev 永远指向当前检查节点的前一个节点

    # 2. 从哑结点后面的第一个真实节点开始遍历
    while prev.next:              # 只要后面还有节点，就继续检查
        if prev.next.val == val:  # 发现需要删除的节点
            # 让 prev 的 next 跳过被删节点，直接指向下一个
            prev.next = prev.next.next
            # 注意：这里不需要把 prev 前移，因为 prev 仍然指向
            # 已经处理好的节点，它的 next 已经是新的节点了
        else:
            # 当前节点不需要删除，prev 向后移动一位
            prev = prev.next

    # 3. 哑结点的 next 就是处理完后的新链表头
    return dummy.next
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历了一遍链表，`n` 是链表的节点数。用大白话说，就是“链表有多少珠子，就检查多少次”，不管 `val` 出现多少次，检查次数始终等于珠子总数。
- **空间复杂度**：`O(1)` —— 只用了几个额外的指针（`dummy`、`prev`），和链表长度无关。即使链表有上万节点，也不需要额外的数组或递归栈。

---

### 2. 最优解

#### 思路  
上面的暴力解已经是 **最优的线性遍历** 方案，时间上已经达到了 `O(n)`，空间也只用了常数级别。  
如果一定要再“优化”，可以从 **代码的简洁性** 和 **递归实现** 两个角度出发：

1. **递归版**：从链表尾部开始回溯，每一次返回时决定当前节点是否保留。递归的本质也是一次遍历，只是把遍历的控制权交给了系统的调用栈。  
   - 递归的“基线条件”是当 `head` 为 `None`（空链表）时直接返回 `None`。  
   - 递归返回后，我们已经得到了 **去掉所有目标值的子链表**（`head.next` 已经处理完），只需要检查当前 `head.val` 是否等于 `val`，若相等则直接返回 `head.next`（相当于把当前节点剪掉），否则把 `head.next` 接回去。

2. **无需哑结点的迭代版**：先把头结点中所有等于 `val` 的节点全部跳过，得到真正的头部，然后再用 `prev` 和 `curr` 两指针完成剩余部分的删除。这种写法在空间上仍是 `O(1)`，但省去了额外的哑结点对象。

下面分别给出递归版和“省哑结点”的迭代版，供大家根据自己的习惯选择。

#### 代码（Python）

**（A）递归版**（思路清晰，适合学习递归）

```python
def removeElements_recursive(head: ListNode, val: int) -> ListNode:
    # 基线条件：空链表直接返回 None
    if not head:
        return None

    # 递归处理后面的子链表，返回处理好的子链表头
    head.next = removeElements_recursive(head.next, val)

    # 当前节点若等于 val，就跳过它；否则保留
    return head.next if head.val == val else head
```

**（B）省哑结点的迭代版**（写法更紧凑）

```python
def removeElements_iter(head: ListNode, val: int) -> ListNode:
    # 1. 先把头部所有等于 val 的节点跳过，找到真正的头
    while head and head.val == val:
        head = head.next          # 直接把 head 往后移，旧的头节点会被 GC 回收

    # 2. 此时 head 要么是 None，要么是第一个不等于 val 的节点
    cur = head                    # cur 用来遍历剩余链表
    while cur and cur.next:       # 只要还有后继节点就继续检查
        if cur.next.val == val:   # 后继节点需要删除
            cur.next = cur.next.next   # 把它跳过去
        else:
            cur = cur.next              # 后继节点保留，指针前移
    return head
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 递归版和迭代版都只遍历一次链表，`n` 为节点数。递归的每一次调用对应链表的一个节点，整体仍是线性时间。
- **空间复杂度**：  
  - 递归版：`O(n)`（递归调用栈的深度最坏为链表长度）——如果链表很长（如 10⁴），递归深度可能导致栈溢出。  
  - 迭代版：`O(1)`（只用常数个指针）——更安全，实际面试中更常用。

> **对比**：如果只看时间，两种实现都一样快；如果考虑空间和安全性，**迭代版**（无论是否使用哑结点）是最优选择。

---

## 心得

- **核心技巧**：遍历链表时**维护前驱指针**或使用**哑结点**来统一处理“头结点被删”的特殊情况。递归思路则是把“处理后面的子问题”交给函数自身。
- **适用题型**：  
  1. 删除链表中满足某些条件的节点（如 `removeElements`）。  
  2. 在链表中插入/删除特定位置的节点（如 `Insert Node in a Linked List`）。  
  3. 链表的过滤或压缩问题（如 `Delete Duplicates from Sorted List`）。
- **一句话总结**：**“遍历一次，利用前驱指针或哑结点统一处理删除，递归则把同样的过程交给函数栈”。**

---

## 反思

- **第一反应**：看到“删除链表中值相等的节点”，立刻想到“一次遍历、检查每个节点”。随后想到头结点可能被删，需要额外处理，于是想到了哑结点。
- **最容易踩的坑**：  
  - **忘记处理头结点**：直接在遍历时只检查 `curr` 而不考虑 `head` 本身是否需要删除，会导致遗漏。  
  - **指针移动错误**：在删除节点后如果错误地把 `prev` 前移，会导致跳过检查后面的节点。  
  - **递归深度**：递归实现虽简洁，但在链表很长时可能导致栈溢出，需要注意。
- **下次类似题的第一步**：先判断“是否需要统一的前驱节点（哑结点）”，再决定是 **迭代** 还是 **递归** 实现，确保头结点的特殊情况被覆盖。