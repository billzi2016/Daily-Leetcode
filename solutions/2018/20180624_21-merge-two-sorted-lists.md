# #21. 合并两个有序链表 / Merge Two Sorted Lists

> 难度：简单 · 标签：Linked List、Recursion · [LeetCode 链接](https://leetcode.com/problems/merge-two-sorted-lists/)

---

## 题目（英文原版）

**Description**

You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
Return the head of the merged linked list.

**Examples**

**Example 1:**

```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
```

**Example 2:**

```
Input: list1 = [], list2 = []
Output: []
```

**Example 3:**

```
Input: list1 = [], list2 = [0]
Output: [0]
```

**Constraints**

- The number of nodes in both lists is in the range [0, 50].
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order.

---

## 题目（中文翻译）

给定两个已排序的链表（linked list）`list1` 和 `list2` 的头结点（head）。  
将这两个链表合并为一个有序链表，合并过程通过直接拼接（splice）两个链表的节点（node）实现，而不是创建新节点。  
返回合并后链表的头结点（head）。

**示例 1:**  
**示例 2:**  
**示例 3:**  

**约束条件**

- 两个链表的节点数量在 `[0, 50]` 范围内。  
- `-100 <= Node.val <= 100`  
- `list1` 和 `list2` 均按非递减顺序排序。

**示例**

**示例 1:**  
Input: list1 = [1,2,4], list2 = [1,3,4]  
Output: [1,1,2,3,4,4]

**示例 2:**  
Input: list1 = [], list2 = []  
Output: []

**示例 3:**  
Input: list1 = [], list2 = [0]  
Output: [0]

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把两条链表的所有节点取出来，放进普通的 Python 列表（`list`）里，再把这个列表排序，最后再把排好序的值一个一个地重新生成链表。

- **把链表“拉平”**：遍历 `list1` 与 `list2`，把每个节点的 `val` 加到一个普通数组 `vals` 中。这里的数组就像把所有书页的文字都抄到一张纸上一样，方便后面一次性处理。
- **排序**：对 `vals` 调用 Python 内置的 `sort()`，相当于把纸上的文字按字母顺序重新排好。
- **重建链表**：根据排好序的 `vals`，依次创建新节点并用 `next` 指针串起来，得到最终的有序链表。

> 为什么这样一定对？因为我们把所有值全部取出来后再排序，排序的结果必然是非递减的。把排序好的值重新链接成链表，自然就满足“合并后仍然有序”。

**复杂度分析（大白话）**  
- **时间**：遍历两条链表得到 `O(m + n)`（`m、n` 是两条链表的长度），再对 `vals` 排序需要 `O((m+n) log(m+n))`。整体是 `O((m+n) log(m+n))`，相当于把 100 本书的章节先全部抄下来，再用电脑排序，需要的时间比直接把两本书的章节顺序合并要多很多。  
- **空间**：我们额外用了一个数组 `vals` 来存放所有节点的值，大小正好是两条链表的节点数 `O(m+n)`，相当于在桌面上放了一堆纸张。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点存的数值
        self.next = next        # 指向下一个节点的指针

def mergeTwoLists_bruteforce(list1: ListNode, list2: ListNode) -> ListNode:
    # 1. 把两个链表的值全部取出来
    vals = []                         # 用普通数组暂存所有值
    cur = list1
    while cur:                        # 遍历 list1
        vals.append(cur.val)
        cur = cur.next
    cur = list2
    while cur:                        # 遍历 list2
        vals.append(cur.val)
        cur = cur.next

    # 2. 排序
    vals.sort()                       # Python 内置的快排，时间复杂度 O(k log k)

    # 3. 根据排好序的值重新生成链表
    dummy = ListNode()                # 哑结点，帮助我们统一写法
    tail = dummy
    for v in vals:                    # 把每个值变成一个新节点并接到链表尾部
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next                 # 返回真正的头结点
```

#### 复杂度

- **时间复杂度**：`O((m+n) log (m+n))`  
  *解释*：先遍历两条链表是线性时间 `O(m+n)`，随后排序是 `O(k log k)`（`k=m+n`），两者相加的最高阶仍是 `O(k log k)`。
- **空间复杂度**：`O(m+n)`  
  *解释*：我们额外用了一个长度为 `m+n` 的数组来存放所有节点的值。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **额外的数组排序**，这一步把时间复杂度提升到了 `log` 级别。实际上，两条链表本身已经是有序的，只要我们一次比较两个链表当前指针指向的值，就能直接把较小的那个节点接到结果链表后面，这样既不需要额外的存储，也不需要再排序。

核心思路如下（类比）：

- 把两条有序的书稿放在两张桌子上，每次比较两本书当前章节的标题，取字母顺序更靠前的章节放进新书。因为每本书本身已经是按顺序排好的，这种“逐段合并”不会破坏整体顺序。

实现细节：

1. **哑结点（dummy）**  
   创建一个不存实际数据的节点 `dummy`，它的 `next` 最终指向合并后的链表头。这样可以避免在处理第一个节点时的特殊情况，写代码更简洁。

2. **双指针**  
   用 `p1`、`p2` 分别指向 `list1`、`list2` 的当前节点。每一步比较 `p1.val` 与 `p2.val`，把较小的节点接到 `tail.next`，并把对应指针往后移动一格。

3. **剩余节点**  
   当其中一条链表遍历完后，另一条链表剩下的节点本身已经有序，直接把它们接到结果链表尾部即可。

4. **递归写法（可选）**  
   递归的本质和上述迭代相同，只是把 “取最小节点、后移指针、继续合并” 用函数调用的方式表达。递归更简洁，但要注意 Python 的递归深度限制（本题节点数 ≤ 50，安全）。

#### 代码（Python）

##### 迭代版（推荐）

```python
def mergeTwoLists_iterative(list1: ListNode, list2: ListNode) -> ListNode:
    dummy = ListNode()          # 哑结点，帮助统一处理头结点
    tail = dummy                # tail 永远指向结果链表的最后一个节点

    p1, p2 = list1, list2       # 两个指针分别遍历两条链表

    while p1 and p2:            # 同时都有节点时才比较
        if p1.val <= p2.val:    # 取较小的那个
            tail.next = p1      # 把 p1 接到结果链表后面
            p1 = p1.next        # p1 向前走一步
        else:
            tail.next = p2
            p2 = p2.next
        tail = tail.next        # tail 也向前走一步，保持指向最后

    # 退出循环后，至少有一条链表已经耗尽，另一条可能还有剩余
    tail.next = p1 if p1 else p2   # 直接把剩余的整段接上

    return dummy.next                # 返回真实的头结点
```

##### 递归版（思路相同，只是写法不同）

```python
def mergeTwoLists_recursive(list1: ListNode, list2: ListNode) -> ListNode:
    if not list1:                     # 如果 list1 为空，直接返回 list2
        return list2
    if not list2:                     # 如果 list2 为空，直接返回 list1
        return list1

    if list1.val <= list2.val:
        # 取 list1 的节点，然后递归合并 list1.next 与 list2
        list1.next = mergeTwoLists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = mergeTwoLists_recursive(list1, list2.next)
        return list2
```

#### 复杂度

- **时间复杂度**：`O(m + n)`  
  *解释*：我们只遍历每个节点一次，比较、指针移动的操作都是常数时间。相当于把两本书的章节各看一遍，线性时间。

- **空间复杂度**：  
  - 迭代版：`O(1)`（不计输出链表本身的空间）  
    *解释*：只用了几个指针变量，额外占用的内存是常数级别。  
  - 递归版：`O(m + n)`（递归调用栈）  
    *解释*：每次递归都会压入一次栈帧，最坏情况下会有 `m+n` 层深度。由于本题节点数 ≤ 50，实际也不会出现栈溢出，但若链表很长，迭代版更安全。

---

## 心得

- **核心技巧**：**双指针合并有序序列**（也叫“归并”），它是归并排序的基础，也是处理有序链表、数组的常用手段。  
- **适用的题型**  
  1. 合并 K 条有序链表（LeetCode 23）  
  2. 合并两个有序数组（LeetCode 88）  
  3. 合并区间（LeetCode 56）  
- **一句话总结**：把两条已经排好序的链表像两条排队的队伍一样，两头比较，谁小谁先走，剩下的直接接上。

---

## 反思

- **第一反应**：把两个链表的值全部取出来再排序——因为我把“有序”这一步忽略了，直接想到最熟悉的排序方法。  
- **最容易踩的坑**  
  - 忘记处理 **空链表**（`list1` 或 `list2` 为 `None`）的情况，导致 `AttributeError`。  
  - 在迭代实现中忘记把 `tail` 移动到新接入的节点，结果会形成环或只返回第一个节点。  
  - 递归版如果链表很长会导致栈溢出，需要记得 `O(1)` 空间的迭代写法更稳妥。  
- **下次第一步**：看到“两个已排序的结构”，立刻想 **双指针逐个比较、直接拼接**，而不是再做一次整体排序。这样思路更清晰、效率更高。