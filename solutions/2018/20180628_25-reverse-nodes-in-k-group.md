# #25. 以 k 为单位翻转链表节点 / Reverse Nodes in k-Group

> 难度：困难 · 标签：Linked List、Recursion · [LeetCode 链接](https://leetcode.com/problems/reverse-nodes-in-k-group/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list, reverse the nodes of the list k at a time, and return the modified list.
k is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of k then left-out nodes, in the end, should remain as it is.
You may not alter the values in the list's nodes, only nodes themselves may be changed.
Follow-up: Can you solve the problem in O(1) extra memory space?

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
```

**Example 2:**

```
Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]
```

**Constraints**

- The number of nodes in the list is n.
- 1 <= k <= n <= 5000
- 0 <= Node.val <= 1000

---

## 题目（中文翻译）

给定链表（linked list）的头结点 `head`，将链表中的节点每 `k` 个一组进行翻转，并返回修改后的链表。  
`k` 为正整数且不超过链表的长度。如果链表节点的总数不是 `k` 的整数倍，则剩余的节点保持原样，不进行翻转。  
**要求**：只能改变节点本身的指向，不能修改节点中的数值 `Node.val`。

**示例 1**  

**示例 2**  

**约束条件**  
- 进阶要求：能否在 **O(1)** 额外空间内完成本题？

**示例**  
**示例 1**  
输入：`head = [1,2,3,4,5]`, `k = 2`  
输出：`[2,1,4,3,5]`

**示例 2**  
输入：`head = [1,2,3,4,5]`, `k = 3`  
输出：`[3,2,1,4,5]`

**约束**  
- 链表中节点的数量记为 `n`。  
- `1 <= k <= n <= 5000`  
- `0 <= Node.val <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每 `k` 个节点先取出来，放进一个 Python 列表（相当于“临时存储箱”），再把它们倒着重新链接回链表**。  
- **链表**就像一串手拉手的孩子，每个孩子只认识下一个孩子（`next` 指针）。  
- **列表**（或数组）可以随意访问第 `i` 个元素，就像把孩子们排成一排，随时可以把第 `i` 位的孩子叫出来。  
- 把 `k` 个节点装进列表后，我们把列表顺序倒置，再把倒置后的节点重新连回原链表，这样就实现了“每 `k` 个一组翻转”。

为什么这样能得到正确答案？因为我们没有改变节点内部的数值，只是把指针的指向改成了倒序；而每一组翻转后，组与组之间的连接仍保持原来的顺序（如果最后不足 `k` 个，就直接保持不动），正好满足题目要求。

**时间复杂度**：我们遍历整条链表一次，每次处理 `k` 个节点，整体仍是 `O(n)`（`n` 为链表长度），因为每个节点只会被访问常数次。  
**空间复杂度**：每次需要一个长度为 `k` 的临时列表，最坏情况下 `k` 可以和 `n` 接近，所以额外空间是 `O(k)`，在最坏情况下是 `O(n)`。

> 大白话：  
> - `O(n)` 就是“和链表的长度成正比”，链表有 1000 个节点，就要跑 1000 步。  
> - `O(k)` 就是“和每组的大小成正比”，如果每组 10 个，就需要最多 10 个临时格子。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点保存的数值
        self.next = next        # 指向下一个节点的指针

def reverseKGroup(head: ListNode, k: int) -> ListNode:
    dummy = ListNode(0)          # 哑结点，方便处理头节点的变化
    dummy.next = head
    group_prev = dummy           # 上一组的尾巴（初始指向哑结点）

    while True:
        # 1）检查剩余节点是否足够 k 个
        kth = group_prev
        for i in range(k):
            kth = kth.next
            if not kth:           # 不足 k 个，直接结束
                return dummy.next

        # 2）把这 k 个节点收进列表
        nodes = []
        cur = group_prev.next
        for _ in range(k):
            nodes.append(cur)
            cur = cur.next

        # 3）倒序链接
        #   - 先把倒序后的第一个节点（原来的第 k 个）接到前一组的尾巴
        group_prev.next = nodes[-1]
        #   - 依次把后面的节点链接起来
        for i in range(k - 1, 0, -1):
            nodes[i].next = nodes[i - 1]
        #   - 最后一个节点（原来的第一个）指向后面未翻转的部分
        nodes[0].next = cur

        # 4）移动指针，准备处理下一组
        group_prev = nodes[0]     # 现在的 group_prev 是这一组翻转后的尾巴

# 下面的代码仅用于本地调试，可忽略
def to_list(head):
    """帮助把链表转成 Python 列表，便于打印」"""
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res
```

#### 复杂度

- **时间复杂度**：`O(n)` — 每个节点只进出一次临时列表，整体遍历一次链表。
- **空间复杂度**：`O(k)` — 只需要保存当前正在翻转的 `k` 个节点，`k` 最多等于 `n`，最坏是 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于使用了额外的列表来存储节点，虽然时间已经是 `O(n)`，但空间并非 `O(1)`（常数级）。  
**目标**是**只用指针本身**完成翻转，不借助额外的数据结构。思路如下：

1. **先判断当前段是否有足够的 `k` 个节点**。如果不足，直接返回，不做任何翻转。  
2. **原地翻转这 `k` 个节点**。这一步和“单链表整体翻转”类似，只是只翻转前 `k` 个。我们用 **三指针**（`prev、cur、next`）在遍历的过程中不断把 `cur.next` 指向 `prev`，从而实现指针方向的倒转。  
3. **连接前后两段**：  
   - `group_prev.next`（前一段的尾巴）应该指向这段翻转后的新头（即原来的第 `k` 个节点）。  
   - 翻转后原来的第一个节点（现在是这一段的尾巴）应该指向后面的未翻转部分 `next_group_head`。  
4. **移动 `group_prev` 到当前段的尾巴**，继续处理下一段。

整个过程只使用了常数个额外指针，**不需要额外的列表或递归栈**，因此满足 **O(1) 额外空间** 的要求。

> **核心技巧——指针翻转**  
> 把链表想象成一条单向的“传送带”。我们把传送带上的每个盒子（节点）向后搬一次，让它指向前一个盒子，就完成了“倒车”。只要记住当前盒子、它的下一个盒子、以及已经搬好的前一个盒子，就能一步一步完成。

#### 代码（Python）

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseKGroup(head: ListNode, k: int) -> ListNode:
    dummy = ListNode(0)          # 哑结点，统一处理头节点的变化
    dummy.next = head
    group_prev = dummy           # 前一段的尾巴（初始为哑结点）

    while True:
        # ---------- 1）检查是否还有足够的 k 个节点 ----------
        kth = group_prev
        for i in range(k):
            kth = kth.next
            if not kth:           # 不足 k 个，结束循环
                return dummy.next

        # ---------- 2）原地翻转这 k 个节点 ----------
        group_next = kth.next     # 记录第 k+1 个节点（后面未翻转的起点）
        # 开始翻转的指针
        prev = group_next         # 第一次翻转时，cur.next 应该指向 group_next
        cur = group_prev.next    # 当前段的第一个节点

        # 翻转 k 次
        for _ in range(k):
            nxt = cur.next        # 暂存下一个节点
            cur.next = prev       # 让当前节点指向已经翻好的部分
            prev = cur            # prev 前移
            cur = nxt             # cur 前移

        # ---------- 3）重新链接 ----------
        # 此时 prev 是翻转后段的头节点（原来的第 k 个）
        # group_prev.next 需要指向新的头
        new_group_head = prev
        old_group_head = group_prev.next   # 翻转前的头，即现在的尾巴
        group_prev.next = new_group_head
        # old_group_head 已经是翻转后段的尾巴，指向后面的未翻转部分
        #（在上面循环里已经完成 cur.next = group_next 的工作）

        # ---------- 4）准备处理下一段 ----------
        group_prev = old_group_head   # 把指针移到本段的尾巴，继续向后

# 辅助函数（用于本地调试，可忽略）
def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res
```

#### 复杂度

- **时间复杂度**：`O(n)` — 每个节点恰好被遍历一次并改动指针，和链表长度成正比。  
- **空间复杂度**：`O(1)` — 只使用了常数个指针变量（`dummy、group_prev、kth、prev、cur、nxt`），不随 `n` 增长。

> 与暴力解对比：时间相同，空间从 `O(k)` 降到了真正的常数 `O(1)`，更符合面试官的“Follow‑up”要求。

---

## 心得

- **核心技巧**：**原地指针翻转**（三指针法）+ **分段处理**（先判断是否够 `k` 再翻转）。  
- **适用场景**：  
  1. “翻转链表的子区间”——如 LeetCode 92 *Reverse Linked List II*。  
  2. “按固定长度分块处理”——如把链表分成每 `k` 个一组做聚合或删减。  
  3. “在链表上做滑动窗口”——需要在窗口内做 O(1) 操作的题目。  
- **一句话总结**：**只要把每一段的 `k` 个节点当作独立的“小链表”，用三指针把它们原地倒转，再把段落之间的指针拼好，就是答案。**

---

## 反思

- **第一反应**：把 `k` 个节点装进数组再倒序，代码好写，但忽视了空间限制。  
- **最容易踩的坑**：  
  - **判断是否还有足够的 `k` 个节点**，忘了会导致最后一段不完整时仍然翻转。  
  - **翻转时的边界指针**，`prev` 初始必须指向 `group_next`，否则会出现环或断链。  
  - **更新 `group_prev`**：必须指向本段翻转后的 **尾巴**（原来的头），否则后续段落会接错。  
- **下次类似题**：第一步先**“分段+检查长度”**，确定可以安全操作的子区间，再在子区间内部**“原地指针翻转”**或其他原地操作。这样思路清晰，容易避免链表指针错误。