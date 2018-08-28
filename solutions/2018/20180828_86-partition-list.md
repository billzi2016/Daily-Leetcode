# #86. 分割链表 / Partition List

> 难度：中等 · 标签：Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/partition-list/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list and a value x, partition it such that all nodes less than x come before nodes greater than or equal to x.
You should preserve the original relative order of the nodes in each of the two partitions.

**Examples**

**Example 1:**

```
Input: head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]
```

**Example 2:**

```
Input: head = [2,1], x = 2
Output: [1,2]
```

**Constraints**

- The number of nodes in the list is in the range [0, 200].
- -100 <= Node.val <= 100
- -200 <= x <= 200

---

## 题目（中文翻译）

给定链表（linked list）的头节点 `head` 和一个整数 `x`，对链表进行划分，使得所有 **值小于 `x` 的节点** 都出现在 **值大于等于 `x` 的节点** 之前。  
在每个划分内部，需要 **保持节点的相对顺序**（relative order）不变。

**示例 1**  
**示例 2**  

**约束条件**  
- 链表中的节点数在 `[0, 200]` 区间内。  
- `-100 ≤ Node.val ≤ 100`  
- `-200 ≤ x ≤ 200`  

**示例**

**示例 1**  
输入: `head = [1,4,3,2,5,2], x = 3`  
输出: `[1,2,2,4,3,5]`

**示例 2**  
输入: `head = [2,1], x = 2`  
输出: `[1,2]`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**“一次遍历把所有节点都搬到合适的位置”**。  
我们可以把链表想象成一串火车车厢，每节车厢都有自己的编号（`val`）。  
现在要把所有 **编号 < x** 的车厢搬到前面，**编号 ≥ x** 的车厢搬到后面，同时保持每个分区内部的顺序不变。

一种“笨办法”是：

1. 从头到尾遍历链表，找到第一个 **≥ x** 的节点，记作 `pivot`。  
2. 再继续往后遍历，如果发现某个节点的值 **< x**，就把它 **摘下来**，插入到 `pivot` 前面。  
3. 插入后，`pivot` 仍然指向原来的 **第一个 ≥ x** 的节点（因为我们把小于 x 的节点搬到了它前面），继续向后扫描。  

> **类比**：想象一条河里有两种颜色的石子（小于 x 的蓝石子和大于等于 x 的红石子），我们用手把每块蓝石子挑出来，放到最前面的红石子之前。每挑一次都要把手伸过去找蓝石子，最坏情况下会重复很多次，所以时间会很长。

**为什么正确**：  
- 我们始终保持 **“已处理好的部分”**（从链表头到 `pivot` 前的所有节点）已经满足题意。  
- 每次把一个 `< x` 的节点插到 `pivot` 前面，等价于把它移动到左分区的末尾，左分区内部顺序保持不变。  
- 当遍历结束时，所有 `< x` 的节点都已经被搬到了左边，右边自然只剩下 `≥ x` 的节点，且相对顺序未被打乱。

**时间/空间复杂度**：  
- 每次发现一个 `< x` 的节点，都要 **遍历** 到 `pivot` 前插入，最坏情况是每个节点都要移动一次，导致 **O(n²)** 次指针操作（n 是链表长度）。  
- 只用了几个指针变量（`prev`, `cur`, `pivot`），额外空间是 **O(1)**。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def partition_brute(head: ListNode, x: int) -> ListNode:
    """
    暴力解：每找到一个小于 x 的节点，就把它摘下来插到第一个
    大于等于 x 的节点之前。时间复杂度 O(n^2)，空间 O(1)。
    """
    if not head:
        return None

    # 先找第一个 >= x 的位置，作为 pivot（分界点）
    dummy = ListNode(0, head)          # dummy 用来处理头节点被移动的情况
    prev = dummy                       # prev 始终指向 pivot 前一个节点
    cur = head

    # 找到第一个 >= x 的节点
    while cur and cur.val < x:
        prev = cur
        cur = cur.next

    # 如果整条链表都小于 x，直接返回原链表
    if not cur:
        return head

    # pivot 指向第一个 >= x 的节点
    pivot = cur
    prev = pivot                       # prev 用来在后面遍历时记录前驱

    # 从 pivot 的下一个节点开始继续遍历
    while cur.next:
        nxt = cur.next                  # nxt 为下一个待检查的节点
        if nxt.val < x:                 # 需要搬到左边
            # 1）摘除 nxt
            cur.next = nxt.next
            # 2）把 nxt 插到 pivot 前面
            nxt.next = pivot
            prev.next = nxt
            # 3）更新 pivot（仍指向原来的第一个 >= x 的节点）
            #    prev 仍指向旧的 pivot 前驱，不需要移动
        else:
            # 当前节点已经在右边，直接往后走
            cur = cur.next

    return dummy.next
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  - “n²” 可以想象成 **“把每根草都拔起再种回去”**，每次搬动都要遍历到分界点，次数会随链表长度的平方增长。  
- **空间复杂度：O(1)**  
  - 只用了常数个指针，跟链表长度无关。

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于每次插入都要遍历到分界点**。  
如果我们在遍历链表的同时，**把所有 < x 的节点和 ≥ x 的节点分别收集起来**，最后再把两段拼接，就不需要再回头插入，时间就可以降到线性 O(n)。

实现思路：

1. **准备两个“虚拟头结点”**（`less_head`、`greater_head`），分别代表左分区和右分区的起点。  
   - 虚拟头结点就像是 **“字典的封面页”**，我们只需要记住它的指针，就能快速找到整段链表的入口。  
2. 用两个指针 `less`、`greater`，分别指向当前左、右分区的尾部。  
3. **一次遍历原链表**：  
   - 若节点值 `< x`，把它接到 `less` 的后面，`less` 前移。  
   - 否则，把它接到 `greater` 的后面，`greater` 前移。  
4. 遍历结束后，**把左分区的尾巴 `less` 接到右分区的头 `greater_head.next`**，形成完整的链表。  
5. 最后 **记得把右分区的尾巴 `greater.next` 设为 `None`**，防止出现环。  

这样只遍历一次，每个节点恰好被处理一次，时间 O(n)。  
额外只用了几个指针（两个虚拟头结点），空间 O(1)。

> **类比**：想象把所有蓝石子装进一个盒子（左分区），红石子装进另一个盒子（右分区），最后把两个盒子依次摆放。我们只需要一次把石子搬进去，不需要来回搬动。

#### 代码（Python）

```python
def partition(head: ListNode, x: int) -> ListNode:
    """
    最优解：一次遍历把节点分到两个链表，再合并。
    时间 O(n)，空间 O(1)。
    """
    # 两个虚拟头结点，帮助我们轻松拼接
    less_head = ListNode(0)      # 存放 < x 的节点
    greater_head = ListNode(0)   # 存放 >= x 的节点

    less = less_head             # 当前左分区的尾指针
    greater = greater_head       # 当前右分区的尾指针
    cur = head

    while cur:
        if cur.val < x:
            # 加入左分区
            less.next = cur
            less = less.next
        else:
            # 加入右分区
            greater.next = cur
            greater = greater.next
        # 继续遍历下一个节点
        cur = cur.next

    # 防止右分区的最后一个节点指向原链表中已经处理过的节点，形成环
    greater.next = None

    # 把左分区和右分区拼接起来
    less.next = greater_head.next

    # 返回合并后的链表头（去掉虚拟头结点）
    return less_head.next
```

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历一次链表，`n` 是节点数。  
  - 相比暴力解的 “每搬一次都要找分界点”，这里一次遍历就把所有节点安置好。  
- **空间复杂度：O(1)** — 只用了常数个额外指针（两个虚拟头结点和几个遍历指针），不随 `n` 增长。

---  

## 心得  

- 这道题的核心技巧是 **“两条链表分治 + 虚拟头结点”**，即把满足不同条件的元素分别收集，再拼接。  
- 这种技巧在以下题型中也非常常见：  
  1. **`odd-even linked list`**（奇偶链表重排）  
  2. **`reverse linked list II`**（区间翻转）  
  3. **`reorder list`**（重新排列链表）  
- **一句话总结解题钥匙**：**“用两个指针分别收集符合条件的节点，再一次性合并”**。

## 反思  

- **第一反应**：看到“把小于 x 的节点搬到前面”，直觉是“每次找到就插到前面”，于是想到了暴力的搬移实现。  
- **最容易踩的坑**：  
  - 忘记在合并后把右分区的尾部 `greater.next` 设为 `None`，会导致原链表残留的指针形成环，遍历时出现死循环。  
  - 处理空链表或全部节点都在同一分区的情况，需要确保返回的头结点是正确的（即 `less_head.next` 或 `greater_head.next`）。  
- **下次遇到类似题**，第一步应该想到 **“是否可以用两个虚拟头结点把数据分流，再一次性拼接”**，这往往能把时间复杂度直接降到线性。