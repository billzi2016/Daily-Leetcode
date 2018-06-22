# #19. 删除链表倒数第 N 个节点 / Remove Nth Node From End of List

> 难度：中等 · 标签：Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list, remove the nth node from the end of the list and return its head.
Follow up: Could you do this in one pass?

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5], n = 2
Output: [1,2,3,5]
```

**Example 2:**

```
Input: head = [1], n = 1
Output: []
```

**Example 3:**

```
Input: head = [1,2], n = 1
Output: [1]
```

**Constraints**

- The number of nodes in the list is sz.
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

---

## 题目（中文翻译）

给定一个链表（linked list）的头节点 `head`，请删除链表中倒数第 `n` 个节点，并返回删除后的链表头节点。

**示例 1**  
**示例 2**  
**示例 3**  

**进阶**：你能否只遍历一次链表完成此操作？

## 示例

**示例 1**  
**输入**: `head = [1,2,3,4,5]`, `n = 2`  
**输出**: `[1,2,3,5]`  

**示例 2**  
**输入**: `head = [1]`, `n = 1`  
**输出**: `[]`  

**示例 3**  
**输入**: `head = [1,2]`, `n = 1`  
**输出**: `[1]`  

## 约束条件

- 链表中的节点数记为 `sz`。  
- `1 <= sz <= 30`  
- `0 <= Node.val <= 100`  
- `1 <= n <= sz`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：先把链表的长度算出来（相当于先把整条路的总里程数记在纸上），再根据 `n` 找到要删掉的节点的前驱节点，然后把它的 `next` 指针跳过要删除的节点。  

- **用到的数据结构**：  
  - **链表**：想象成一串火车车厢，每个车厢只知道自己后面接的下一个车厢（`next`），没有指向前面的指针。  
  - **计数器**：遍历时用一个整数 `cnt` 来记数，就像在路上走了多少步。  

- **为什么正确**：  
  1. 第一次遍历得到链表的总节点数 `size`，所以从头数 `size - n` 步就能正好站在要删除节点的前一个位置（如果 `n` 正好等于 `size`，说明要删除的是头结点，直接返回 `head.next`）。  
  2. 把前驱节点的 `next` 指向要删除节点的下一个节点，就相当于把这节车厢从列车上摘下来，列车仍然连通。  

- **时间/空间复杂度**：  
  - **时间**：我们要遍历两遍链表，第一遍算长度，第二遍找到前驱并修改指针。遍历一次是 `O(L)`（`L` 为链表长度），两遍就是 `O(2·L)`，在大 O 记号里常数会被省略，写成 **`O(L)`**。可以把 `O(L)` 想象成“和链表里节点个数成正比”，链表越长，花的时间越多。  
  - **空间**：只用了几个额外的整数变量（计数器、指针），与链表长度无关，记作 **`O(1)`**，即“常数级别的空间”。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点的值
        self.next = next        # 指向下一个节点的指针

def removeNthFromEnd_brute(head: ListNode, n: int) -> ListNode:
    """
    暴力解：先遍历一次得到链表长度，再遍历一次定位并删除第 n 个倒数节点。
    """
    # 第一步：计算链表长度
    size = 0
    cur = head
    while cur:                # 遍历链表直到末尾
        size += 1
        cur = cur.next

    # 如果要删除的是头结点（倒数第 size 个），直接返回 head.next
    if n == size:
        return head.next

    # 第二步：找到倒数第 n 个节点的前驱（正数第 size-n 个节点）
    cur = head
    for _ in range(size - n - 1):   # 前进 size-n-1 步就能站在前驱位置
        cur = cur.next

    # 删除操作：让前驱的 next 跳过目标节点
    cur.next = cur.next.next if cur.next else None
    return head
```

#### 复杂度

- **时间复杂度**：`O(L)` — 需要遍历链表两次，时间随链表长度线性增长。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量，不随链表大小变化。

---

### 2. 最优解

#### 思路  

暴力解的“慢点”在于我们**先算完长度才动手**，这导致要遍历两遍链表。我们希望只走一次链表就能完成所有工作。  

关键观察：如果我们能让两个指针之间保持 **固定的距离 n**，那么当后面的指针走到链表末尾时，前面的指针恰好停在要删除节点的前一个位置。  

实现步骤：

1. **创建一个哑结点**（dummy），放在链表最前面，值可以随意。它的作用是统一处理“删除头结点”的情况，避免写特殊分支。哑结点就像在火车头前面加了一节空车厢，后面所有操作都可以假设有前驱。  
2. **初始化两个指针** `first` 与 `second`，都指向哑结点。  
3. 让 `first` 先向前走 `n+1` 步（多走一步是为了让 `second` 最后停在要删除节点的前驱上）。此时 `first` 与 `second` 之间相隔 `n` 个真实节点。  
4. 同时移动 `first` 与 `second`，直到 `first` 到达链表末尾（`None`）。因为两指针间距不变，`second` 此时正好指向要删除节点的前驱。  
5. 删除：`second.next = second.next.next`。  
6. 返回 `dummy.next` 作为新的头结点。

- **核心算法/数据结构**：**双指针（Two Pointers）**，也叫**快慢指针**的变体。这里的两个指针不是快慢跑，而是保持固定间距的“追赶”。  
- **类比**：想象两个人在排队买票，后面的人比前面的人多走了 `n` 步。当前面的人到达柜台（链表末尾）时，后面的人正好站在倒数第 `n` 位的前面，随后可以直接把这位顾客（节点）请出队列。  

#### 代码（Python）

```python
def removeNthFromEnd_one_pass(head: ListNode, n: int) -> ListNode:
    """
    最优解：一次遍历完成删除，使用双指针保持固定间距。
    """
    # 哑结点：统一处理删除头结点的情况
    dummy = ListNode(0, head)

    first = dummy   # 将 first 提前 n+1 步
    second = dummy  # second 将最终停在待删节点的前驱

    # 让 first 先走 n+1 步，确保 second 与 first 之间相隔 n 个真实节点
    for _ in range(n + 1):
        first = first.next

    # 同时前进，直至 first 到达链表末尾
    while first:
        first = first.next
        second = second.next

    # 此时 second.next 正是要删除的节点
    second.next = second.next.next  # 删除操作：跳过目标节点

    # 返回新的头结点（可能已经变化）
    return dummy.next
```

#### 复杂度

- **时间复杂度**：`O(L)` — 只遍历一次链表，时间仍然随长度线性增长，但只走一次，比暴力解少了一遍遍历。  
- **空间复杂度**：`O(1)` — 只用了常数个指针（`dummy`, `first`, `second`），不随链表大小增加。

---

## 心得

- **核心技巧**：**双指针保持固定间距**（也叫“滑动窗口”思想）。  
- **适用的题型**：  
  1. “链表中倒数第 k 个节点”  
  2. “判断链表是否是回文（快慢指针）”  
  3. “滑动窗口最大值（数组）”  
- **一句话总结解题钥匙**：**让一个指针先跑 n 步，后面再一起跑，等前面到终点时，后面正好站在我们想要的“前一个位置”。**

---

## 反思

- **第一反应**：先算链表长度再定位删除位置——这是一种最自然的“先知道全局再操作”的思路。  
- **最容易踩的坑**：  
  - 删除的是头结点时，直接返回 `head.next`，否则会忘记更新返回值。使用哑结点可以一次性避免这个特例。  
  - `first` 预先走 `n+1` 步时要确保链表长度足够（题目保证 `1 ≤ n ≤ sz`，所以安全）。  
  - 删除后要返回 `dummy.next` 而不是原来的 `head`，否则在删除头结点时会返回错误的旧头。  
- **下次类似题的第一步**：**在脑中先画出两个指针的相对位置，确认要让哪个指针先走多少步，使得后面指针最终停在“目标的前一个位置”。**这样就能快速决定是否可以一次遍历完成。