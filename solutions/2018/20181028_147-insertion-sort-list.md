# #147. **插入排序链表** / Insertion Sort List

> 难度：中等 · 标签：Linked List、Sorting · [LeetCode 链接](https://leetcode.com/problems/insertion-sort-list/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list, sort the list using insertion sort, and return the sorted list's head.
The steps of the insertion sort algorithm:
The following is a graphical example of the insertion sort algorithm. The partially sorted list (black) initially contains only the first element in the list. One element (red) is removed from the input data and inserted in-place into the sorted list with each iteration.

**Examples**

**Example 1:**

```
Input: head = [4,2,1,3]
Output: [1,2,3,4]
```

**Example 2:**

```
Input: head = [-1,5,3,4,0]
Output: [-1,0,3,4,5]
```

**Constraints**

- The number of nodes in the list is in the range [1, 5000].
- -5000 <= Node.val <= 5000

---

## 题目（中文翻译）

给定一个单向链表（singly linked list）的头结点 `head`，请使用插入排序（insertion sort）对链表进行排序，并返回排序后的链表头结点。

**插入排序算法的步骤**  
下面给出插入排序算法的图示示例。最初，已排序的链表（黑色）只包含原链表的第一个节点。每一次迭代，都会从未排序的输入数据中取出一个节点（红色），并将其就地插入到已排序链表的适当位置。

**示例 1**  

**示例 2**  

**约束条件**

- 链表中节点的数量在 `[1, 5000]` 范围内。  
- `-5000 <= Node.val <= 5000`

**示例**

> 示例 1  
> **输入**: `head = [4,2,1,3]`  
> **输出**: `[1,2,3,4]`

> 示例 2  
> **输入**: `head = [-1,5,3,4,0]`  
> **输出**: `[-1,0,3,4,5]`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把链表的节点全部取出来放进一个普通的 **Python 列表**（相当于把所有书都搬到桌面上），  
然后使用 Python 内置的 `sorted`（或 `list.sort()`）一次性排好序，最后再把排好序的值重新串成链表返回。

- **数据结构类比**：  
  - 链表 → 一串挂在墙上的画，每幅画只能看到前后相邻的那幅。  
  - Python 列表 → 一本普通的书，随时可以用手指直接翻到第 *i* 页。  
  - 把链表的节点“搬进书里”就像把画全部取下来放进书中，排序后再把画挂回墙上。

- **正确性**：  
  只要把所有节点的值完整地收集起来，再按照从小到大的顺序重新写回链表，最终链表必然是有序的。

- **复杂度大白话**：  
  - **时间**：把链表遍历一次收集值是 O(n)（每个节点只看一次），  
    `sorted` 在最坏情况下要比较每一对元素，大约是 *n* × *log₂ n* 次比较，记作 **O(n log n)**。  
    想象有 1000 本书，排序需要比单纯逐本检查（O(n²)）快很多。  
  - **空间**：需要额外的数组存所有值，大小随节点数线性增长，记作 **O(n)**。  
    就像把所有画都搬到桌面上，需要占用和画数量同样多的桌面空间。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def insertionSortList_bruteforce(head: ListNode) -> ListNode:
    # 1. 把所有节点值取出来放进 Python 列表
    values = []
    cur = head
    while cur:
        values.append(cur.val)   # 记录每个节点的数值
        cur = cur.next

    # 2. 用 Python 自带的排序（时间 O(n log n)）
    values.sort()                # 原地排序，省去额外的拷贝

    # 3. 把排好序的值重新写回链表
    cur = head
    for v in values:
        cur.val = v               # 用排好序的数值覆盖原来的节点
        cur = cur.next

    return head
```

#### 复杂度

- **时间复杂度**：**O(n log n)**  
  `n` 是链表长度。遍历一次是 O(n)，排序是 O(n log n)，两者相加仍是 O(n log n)。  
  用生活中的例子来说，像把 1000 本书一次性排好序，比起每次只找出最小的那本再放回去（O(n²)）要快很多。

- **空间复杂度**：**O(n)**  
  需要额外的数组存所有节点的值，大小正好等于链表长度。  

---

### 2. 最优解

#### 思路  

**插入排序** 本身就是一种“把未排好序的元素一个一个插入到已排好序的序列中”的方法。  
在数组里实现插入排序时，需要频繁地 **移动** 后面的元素，导致 O(n²) 的时间且需要额外的空间来搬运数据。  
但是 **链表** 天生支持 **在任意位置直接插入/删除**（只改动指针），不需要搬动整段数据。

**从暴力解看瓶颈**  
- 暴力解把所有值都搬到数组里，用额外的 O(n) 空间；  
- 还有一次完整的遍历把排好序的值写回链表。

**优化思路**  
1. **不搬数据，只搬指针**：我们直接在原链表上进行插入排序。  
2. **使用哑结点（dummy）**：在链表最前面额外加一个空结点，方便把最小的节点插到最前面，避免处理头结点的特殊情况。  
3. **遍历一次**：用 `cur` 指针遍历原链表，每次把 `cur.next`（即下一个待插入的节点）取出来，**在已排好序的部分**（从 dummy 开始）找到合适的位置插入。  
4. **保持已排好序的部分始终是从 dummy 开始的连续链表**，这样每次插入都是 **O(n)**（最坏要遍历已排好序的部分），整体时间 **O(n²)**，但 **空间是 O(1)**（只用了几个额外指针）。

**核心概念解释**  
- **哑结点（dummy node）**：想象在墙的最左侧放一块空白画框，所有画（节点）都挂在它右边。这样，无论最小的画放在哪里，都不需要额外判断“是不是第一个”。  
- **指针的重新链接**：把 `node` 插入到 `prev` 与 `prev.next` 之间，只需要三条语句：
  1. `node.next = prev.next`（把 node 的后继指向插入位置后面的节点）  
  2. `prev.next = node`（把前一个节点的后继指向 node）  
  3. 记得把原链表的 `cur.next` 也指向下一个未处理的节点。

**图示（文字版）**  

```
已排好序部分: dummy -> 1 -> 3 -> 5
待插入节点: 2
遍历找到位置: prev 指向 1，prev.next 是 3
插入后:
dummy -> 1 -> 2 -> 3 -> 5
```

#### 代码（Python）

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def insertionSortList(head: ListNode) -> ListNode:
    """
    对单链表执行原地插入排序，时间 O(n^2)，空间 O(1)。
    """
    # 1. 建立哑结点，方便统一处理头部插入
    dummy = ListNode(float('-inf'))   # -inf 表示最小的哑值
    dummy.next = head

    # 2. cur 用来遍历原链表，始终指向“已排好序的最后一个节点”
    cur = head
    while cur and cur.next:
        # 如果下一个节点已经比当前节点大，说明它已经在正确位置，无需移动
        if cur.val <= cur.next.val:
            cur = cur.next
            continue

        # 3. 取出待插入的节点
        to_insert = cur.next
        cur.next = to_insert.next   # 先把 cur 与后面的节点断开

        # 4. 在已排好序的部分（从 dummy 开始）寻找插入位置
        prev = dummy
        while prev.next.val < to_insert.val:   # 找到第一个大于等于 to_insert 的位置
            prev = prev.next

        # 5. 完成插入：prev -> to_insert -> prev.next
        to_insert.next = prev.next
        prev.next = to_insert
        # 注意：此时 cur 仍指向原来的“已排好序的最后一个节点”，因为我们已经把
        # cur.next 重新指向了下一个未处理的节点（第 3 步已完成）

    return dummy.next
```

#### 复杂度

- **时间复杂度**：**O(n²)**  
  最坏情况下（链表逆序），每插入一个节点都要遍历已排好序的全部节点，形成等差数列 1 + 2 + … + (n‑1) ≈ n²/2 次比较。用生活化的说法，就是把 1000 本书从大到小重新排，每本书都要从头开始找合适位置，大约要做 500,000 次“比较”。  
  与暴力解的 O(n log n) 相比，时间更慢，但 **空间更省**，且完全在原链表上完成。

- **空间复杂度**：**O(1)**  
  只用了常数个额外指针（`dummy、cur、prev、to_insert`），不随节点数量增长。相当于在墙上重新挂画，只动了画框的挂钩，没有搬走任何画。

---

## 心得

- **核心技巧**：在单链表上实现 **原地插入排序**，关键在于 **哑结点 + 指针重连**。  
- **适用的题型**：  
  1. 链表的 **排序**（如 “Sort List”）  
  2. 需要 **在已排序序列中插入** 的场景（如 “Insert into a Sorted Linked List”）  
  3. 任何要求 **原地修改链表结构** 而不使用额外数组的题目  
- **一句话总结**：**“用哑结点统一头部插入，用指针搬砖，原地完成插入排序”。**

---

## 反思

- **第一反应**：把链表转成数组，用 Python 自带的排序函数，最省事。  
- **最容易踩的坑**：  
  - **忘记更新 `cur.next`**：在取出 `to_insert` 后，如果不把 `cur.next` 指向后面的节点，链表会出现断裂。  
  - **插入位置的比较符号**：使用 `prev.next.val < to_insert.val`（而不是 `<=`）防止出现无限循环或把相等的节点插到错误位置。  
  - **哑结点值的选取**：使用 `float('-inf')` 可以保证所有真实节点的值都比它大，避免特殊判断。  
- **下次遇到同类题**：第一步先 **判断是否可以直接在原链表上完成**（是否需要额外空间），然后 **构造哑结点**，最后 **用指针遍历找插入点**。这样思路清晰，代码也更不易出错。