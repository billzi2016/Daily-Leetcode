# #82. 删除排序链表中的重复节点 II / Remove Duplicates from Sorted List II

> 难度：中等 · 标签：Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)

---

## 题目（英文原版）

**Description**

Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

**Examples**

**Example 1:**

```
Input: head = [1,2,3,3,4,4,5]
Output: [1,2,5]
```

**Example 2:**

```
Input: head = [1,1,1,2,3]
Output: [2,3]
```

**Constraints**

- The number of nodes in the list is in the range [0, 300].
- -100 <= Node.val <= 100
- The list is guaranteed to be sorted in ascending order.

---

## 题目（中文翻译）

给定一个已排序的链表（linked list）的头节点 `head`，删除所有出现重复值的节点，只保留原链表中出现一次的节点。返回处理后的链表，链表仍然保持升序排列。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  
**示例 1:**  
```
Input: head = [1,2,3,3,4,4,5]
Output: [1,2,5]
```

**示例 2:**  
```
Input: head = [1,1,1,2,3]
Output: [2,3]
```

**约束条件**  
- 链表中的节点数在范围 `[0, 300]` 内。  
- `-100 <= Node.val <= 100`。  
- 链表保证按升序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**遍历链表两遍**：

1. **第一遍**统计每个数出现的次数。我们可以把每个节点的 `val` 当作“单词”，出现的次数当作“页码”。把它们放进一个哈希表（相当于一本查词典的书，`key` 是词，`value` 是出现次数），这样我们就知道哪些值是重复的，哪些是唯一的。  
2. **第二遍**再走一遍链表，只把 **出现次数为 1** 的节点接到结果链表上，其他的全部跳过（相当于只把字典里只出现一次的词挑出来装进新书）。

> 为什么这样一定对？  
> 因为我们已经明确了每个数到底出现了几次，只要保留出现一次的节点，重复的自然全部删掉。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def deleteDuplicates(head: ListNode) -> ListNode:
    # ---------- 第一次遍历：统计出现次数 ----------
    freq = {}                     # 哈希表：val -> 次数
    cur = head
    while cur:
        freq[cur.val] = freq.get(cur.val, 0) + 1
        cur = cur.next

    # ---------- 第二次遍历：只保留出现一次的节点 ----------
    dummy = ListNode(0)           # 哑节点，帮助处理头节点被删的情况
    tail = dummy                  # tail 始终指向结果链表的最后一个节点
    cur = head
    while cur:
        if freq[cur.val] == 1:    # 只出现一次的节点才接入结果链表
            tail.next = cur
            tail = tail.next
        cur = cur.next
    tail.next = None              # 防止原链表中残留的旧指针形成环

    return dummy.next
```

#### 复杂度

- **时间复杂度：O(n)**  
  我们遍历了两遍链表，`n` 是节点数。两遍加起来仍然是线性时间，`O(2n) ≈ O(n)`。这里的 `O(n)` 可以想象成“每个节点只被看一次”，所以运行时间随节点数线性增长。

- **空间复杂度：O(m)**  
  `m` 是不同数值的种类数（哈希表的键数），最坏情况下每个节点的值都不相同，`m = n`，因此空间复杂度是 `O(n)`。这相当于我们额外开了一张“出现次数表”，需要和原链表等量的额外空间。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经是 **O(n) 时间**，但它用了额外的哈希表，空间不是最优的。我们可以 **只用一次遍历**，且 **不借助额外的数据结构**，只利用链表本身的结构来判断是否有重复。

**关键观察**：  
- 链表是**已排序**的，重复的节点一定是 **相邻** 出现的。  
- 当我们看到 `cur.val == cur.next.val` 时，说明从 `cur` 开始的一段连续节点都是相同的，需要全部跳过。

**双指针 + 哑节点** 的做法：

1. 创建一个 **哑节点**（dummy），它的 `next` 指向原链表的头部。哑节点的作用是统一处理“头节点被删”的特殊情况。  
2. 用 `prev` 指针指向**已经确认没有重复**的最后一个节点（初始指向 dummy），用 `cur` 指向待检查的节点（初始指向 head）。  
3. 当 `cur` 与 `cur.next` 的值相等时，记录下这个重复的值 `dup = cur.val`，然后 **一直向后移动 `cur`**，直到跳出所有相同的节点（即 `cur` 为 `None` 或 `cur.val != dup`）。此时，这段重复的节点全部被“丢掉”。  
4. 如果 `cur` 与 `cur.next` 不相等，说明 `cur` 是一个**唯一**的节点，可以安全地接到 `prev.next`，并把 `prev` 前进到 `cur`。  
5. 重复步骤 3~4，直到遍历完整个链表。

整个过程只走了一遍链表，没有额外的哈希表，空间只用了常数个指针。

> 类比：想象你在一本已经排好序的名单里挑选“只出现一次的名字”。你拿着两根手指（`prev`、`cur`），如果发现连续的相同名字，就把整段名字全部跳过去；否则，就把这个名字写进新名单。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def deleteDuplicates(head: ListNode) -> ListNode:
    dummy = ListNode(0)       # 哑节点，防止头节点被删
    dummy.next = head
    prev = dummy              # 已确定不重复的最后一个节点
    cur = head                # 正在检查的节点

    while cur:
        # 如果当前节点后面还有相同值，说明出现了重复
        if cur.next and cur.val == cur.next.val:
            dup_val = cur.val
            # 跳过所有值等于 dup_val 的节点
            while cur and cur.val == dup_val:
                cur = cur.next
            # 此时 cur 已经指向第一个不等于 dup_val 的节点（或 None）
            prev.next = cur     # 把 prev 与后面的非重复部分相连
        else:
            # cur 是唯一的，直接保留
            prev = cur
            cur = cur.next

    return dummy.next
```

#### 复杂度

- **时间复杂度：O(n)**  
  每个节点至多被访问两次（一次作为 `cur`，一次在跳过重复段的 `while` 循环中），整体仍然是线性时间。可以想象为“从头到尾一次走完”，不管有多少重复，整体步数不超过 `2n`。

- **空间复杂度：O(1)**  
  只用了固定数量的指针 (`dummy`, `prev`, `cur`, `dup_val`)，不随链表长度增长而增加。相当于“只占用常数级别的额外空间”，这是最优的。

---

## 心得

- **核心技巧**：利用**已排序**的特性，结合**双指针**（`prev`、`cur`）和**哑节点**一次遍历完成去重。  
- **适用场景**：  
  1. 删除有序数组/链表中的重复元素（LeetCode 26、80）。  
  2. 在有序序列中查找唯一出现一次的元素（如“只出现一次的数字”问题）。  
- **一句话总结**：**“在有序结构里，重复总是相邻，用指针跳过整段相同即可”。**

---

## 反思

- **第一反应**：看到“已排序的链表”，立刻想到可以利用相邻相等的特性，一遍遍历就能判断重复。  
- **最容易踩的坑**：  
  - **头节点被删除**：如果直接操作 `head`，可能会忘记更新返回值。使用哑节点可以避免这类错误。  
  - **跳过重复段后忘记连接**：在跳过一段重复节点后，需要把 `prev.next` 指向 `cur`，否则会形成断链。  
  - **空链表或全是重复**：要确保 `while cur:` 循环能正确处理 `head = None` 或全部节点被删除的情况。  
- **下次第一步**：**检查相邻节点是否相等**，如果相等就准备“跳过整段相同”，否则保留当前节点并向前移动。这样就能快速锁定最关键的优化点。