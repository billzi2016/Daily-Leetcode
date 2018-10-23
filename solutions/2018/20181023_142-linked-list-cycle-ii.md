# #142. 环形链表 II / Linked List Cycle II

> 难度：中等 · 标签：Hash Table、Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/linked-list-cycle-ii/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.
There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.
Do not modify the linked list.
Follow up: Can you solve it using O(1) (i.e. constant) memory?

**Examples**

**Example 1:**

```
Input: head = [3,2,0,-4], pos = 1
Output: tail connects to node index 1
Explanation: There is a cycle in the linked list, where tail connects to the second node.
```

**Example 2:**

```
Input: head = [1,2], pos = 0
Output: tail connects to node index 0
Explanation: There is a cycle in the linked list, where tail connects to the first node.
```

**Example 3:**

```
Input: head = [1], pos = -1
Output: no cycle
Explanation: There is no cycle in the linked list.
```

**Constraints**

- The number of the nodes in the list is in the range [0, 104].
- -105 <= Node.val <= 105
- pos is -1 or a valid index in the linked-list.

---

## 题目（中文翻译）

给定链表的头节点 `head`，返回环的起始节点。如果链表中不存在环，返回 `null`。  
当链表中存在环时，意味着存在某个节点可以通过不断沿 `next` 指针再次回到该节点。题目内部使用 `pos` 来表示尾节点的 `next` 指针所连接的节点索引（**0** 起始），若不存在环则 `pos = -1`。**注意**：`pos` 并不会作为函数参数传入。  
**要求**：不要修改链表。

**示例 1**  
**示例 2**  
**示例 3**

**进阶**：能否使用 **O(1)**（即常数）额外空间完成？

---

### 示例

#### 示例 1
```
Input: head = [3,2,0,-4], pos = 1
Output: tail connects to node index 1
Explanation: 链表中存在一个环，尾节点指向第二个节点。
```

#### 示例 2
```
Input: head = [1,2], pos = 0
Output: tail connects to node index 0
Explanation: 链表中存在一个环，尾节点指向第一个节点。
```

#### 示例 3
```
Input: head = [1], pos = -1
Output: no cycle
Explanation: 链表中不存在环。
```

---

### 约束条件

- 链表中节点的数量范围为 `[0, 10^4]`。
- `-10^5 <= Node.val <= 10^5`
- `pos` 为 `-1` 或者是链表中合法的索引。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有已经走过的结点记下来**，再往后走时检查下一个结点是否已经出现过。  
- 这里用到的数据结构是 **哈希表（或 Python 的 `set`）**，它就像一本字典：我们把结点本身（它的地址）当作单词，出现过就记下来，相当于把页码写进字典。  
- 当遍历到一个已经在集合里的结点时，说明我们已经走进了环，环的入口就是这个结点。  
- 如果遍历到 `None`（链表尾部），说明没有环，直接返回 `None`。

这个方法之所以一定能得到正确答案，是因为链表的每个结点在内存中都有唯一的身份（地址），只要出现两次，必然是环的入口或环中的其它结点。只要我们把每个结点的身份全部记录下来，就不会漏掉。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def detectCycle(head: ListNode) -> ListNode:
    """
    暴力解：使用哈希集合记录已经访问过的结点
    """
    visited = set()               # 用 set 当“字典”，存放已经遍历过的结点对象
    cur = head
    while cur:                    # 只要还有结点就继续
        if cur in visited:        # 这个结点已经出现过 → 环的入口
            return cur
        visited.add(cur)          # 记下当前结点
        cur = cur.next            # 向后走一步
    return None                   # 走到链表末尾仍未相遇，说明没有环
```

#### 复杂度  

- **时间复杂度：O(n)**  
  这里的 *n* 表示链表的节点数。我们最多遍历每个结点一次，检查/插入集合的操作在平均情况下是常数时间（`O(1)`），所以整体是线性时间。  
  用大白话说，就是“链表有多长，就要跑多少步”。

- **空间复杂度：O(n)**  
  最坏情况下（没有环）我们要把所有结点的地址都存进集合，集合的大小随节点数线性增长。  
  用生活中的比喻：如果你把每次走过的路标都贴在背包里，背包的容量就会随走的路长而变大。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **空间**：需要额外的 `O(n)` 记忆来存放已经访问的结点。  
我们可以利用 **快慢指针（Two Pointers）** 只用常数空间来判断是否有环，并进一步定位环的入口。  
下面一步步解释整个过程：

1. **环的存在性检测**  
   - 设置两个指针：`slow` 每次走一步，`fast` 每次走两步。  
   - 如果链表没有环，`fast` 最终会走到 `None`，循环结束，返回 `None`。  
   - 如果有环，`fast` 必然会在环里“追上”`slow`（因为 `fast` 跑得更快），两者会在环中的某个结点相遇。  

2. **找到环入口**  
   - 设链表头到环入口的距离为 `a`，入口到相遇点的距离为 `b`，环的长度为 `c`（即 `b + c` 是环中一次完整的循环）。  
   - 第一次相遇时，`slow` 走了 `a + b` 步，`fast` 走了 `2(a + b)` 步。  
   - 因为 `fast` 比 `slow` 多走了整整 `k` 圈环：`2(a + b) = a + b + k·c` → `a + b = k·c`。  
   - 于是 `a = k·c - b`，这意味着如果我们把其中一个指针重新放回链表头，让它和另一个指针一起每次走一步，它们会在 `a` 步后相遇，而这一步正好是环的入口。  

3. **实现细节**  
   - 第一次相遇后，把 `slow`（或 `fast`）重新指向 `head`，然后两个指针同步前进，第一次相遇的结点就是环的入口。  

整个过程只用了两个指针，空间是 **O(1)**，时间仍是线性 **O(n)**。

#### 代码（Python）

```python
def detectCycle(head: ListNode) -> ListNode:
    """
    Floyd 判圈算法（快慢指针）+ 环入口定位
    """
    if not head or not head.next:   # 空链表或只有一个结点，直接返回 None
        return None

    # 1. 用快慢指针判断是否有环
    slow = head
    fast = head
    while fast and fast.next:       # fast 需要检查两步，防止空指针异常
        slow = slow.next            # slow 走一步
        fast = fast.next.next       # fast 走两步
        if slow is fast:            # 两指针相遇，说明有环
            break
    else:
        # while 正常结束（没有 break），说明没有环
        return None

    # 2. 寻找环的入口
    slow = head                     # 把 slow 拉回到链表头
    while slow is not fast:         # 同步前进，第一次相遇即为环入口
        slow = slow.next
        fast = fast.next
    return slow                     # 或者 return fast，二者已经相等
```

#### 复杂度  

- **时间复杂度：O(n)**  
  第一次遍历（快慢指针）最多走 `n` 步就能相遇或确认无环；第二次同步前进最多再走 `n` 步找到入口。整体仍是线性时间。  
  用通俗的话说，就是“最多跑两趟链表”，但常数因子很小。

- **空间复杂度：O(1)**  
  只用了固定数量的指针变量（`slow`、`fast`、`head`），不随链表长度增加。  
  相当于“只带了一个小背包”，不需要额外的记忆空间。

---

## 心得

- **核心技巧**：**快慢指针（Floyd 判圈）** 能在常数空间内检测环并定位入口。  
- **适用的相似题型**：  
  1. **LeetCode 141 – Linked List Cycle**（只要求判断是否有环）。  
  2. **LeetCode 287 – Find the Duplicate Number**（数组中寻找重复数，等价于链表环检测）。  
  3. **LeetCode 202 – Happy Number**（判断数是否进入循环）。  
- **一句话总结**：**让快指针追上慢指针，再让其中一个从头出发，两者同步相遇的地方就是环的入口**。

---

## 反思

- **第一反应**：直接用哈希集合记录访问过的结点，想到“把走过的路标贴下来”。  
- **最容易踩的坑**：  
  - 忘记处理空链表或只有一个结点的情况，会导致 `fast.next` 报错。  
  - 在第一次相遇后没有把指针重新指向头部，而是直接继续前进，得不到正确的入口。  
  - 返回值必须是结点对象本身，而不是它的值或索引。  
- **下次遇到同类题**：第一步先思考 **“能否用两个指针的相对速度差来捕获循环？”**，即尝试快慢指针的思路。