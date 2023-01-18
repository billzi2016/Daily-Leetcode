# #2095. 删除链表的中间节点 / Delete the Middle Node of a Linked List

> 难度：中等 · 标签：Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list. Delete the middle node, and return the head of the modified linked list.
The middle node of a linked list of size n is the ⌊n / 2⌋th node from the start using 0-based indexing, where ⌊x⌋ denotes the largest integer less than or equal to x.

**Examples**

**Example 1:**

```
Input: head = [1,3,4,7,1,2,6]
Output: [1,3,4,1,2,6]
Explanation:
The above figure represents the given linked list. The indices of the nodes are written below.
Since n = 7, node 3 with value 7 is the middle node, which is marked in red.
We return the new list after removing this node.
```

**Example 2:**

```
Input: head = [1,2,3,4]
Output: [1,2,4]
Explanation:
The above figure represents the given linked list.
For n = 4, node 2 with value 3 is the middle node, which is marked in red.
```

**Example 3:**

```
Input: head = [2,1]
Output: [2]
Explanation:
The above figure represents the given linked list.
For n = 2, node 1 with value 1 is the middle node, which is marked in red.
Node 0 with value 2 is the only node remaining after removing node 1.
```

**Constraints**

- The number of nodes in the list is in the range [1, 105].
- 1 <= Node.val <= 105

---

## 题目（中文翻译）

给定链表 (linked list) 的头节点 (head)。请删除其中的中间节点，并返回修改后的链表头节点。

链表中大小为 n 的中间节点定义为从起始位置起的第 ⌊n / 2⌋ 个节点，采用 0 基索引，其中 ⌊x⌋ 表示不大于 x 的最大整数。

### 示例

#### 示例 1
**输入:** `head = [1,3,4,7,1,2,6]`  
**输出:** `[1,3,4,1,2,6]`  
**解释:**  
上图展示了给定的链表，节点的索引标在下方。  
由于 n = 7，索引为 3、值为 7 的节点是中间节点（已用红色标记）。  
删除该节点后返回新的链表。

#### 示例 2
**输入:** `head = [1,2,3,4]`  
**输出:** `[1,2,4]`  
**解释:**  
上图展示了给定的链表。  
当 n = 4 时，索引为 2、值为 3 的节点是中间节点（已用红色标记），将其删除后得到结果。

#### 示例 3
**输入:** `head = [2,1]`  
**输出:** `[2]`  
**解释:**  
上图展示了给定的链表。  
当 n = 2 时，索引为 1、值为 1 的节点是中间节点（已用红色标记），删除后仅剩下索引为 0、值为 2 的节点。

### 约束条件
- 链表中的节点数在 `[1, 10^5]` 区间内。
- `1 <= Node.val <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**先把整个链表遍历一遍，统计出节点总数 `n`，再根据 ⌊n/2⌋ 计算出中间节点的下标**，随后再遍历一次链表，找到前驱节点（即中间节点的前一个），把它的 `next` 指针直接指向中间节点的后继，从而把中间节点“摘掉”。  

- **使用的数据结构**：  
  - **链表**本身就是一种“线性容器”，每个元素只知道下一个元素的地址。我们只能顺着 `next` 指针一个接一个地访问。  
  - **计数器**（整数）相当于在“记事本”上记下我们走了多少步。  
  - **指针变量** `prev`、`cur` 类似于“指路牌”，帮助我们定位到需要修改的节点。  

- **为什么正确**：  
  1. 第一次遍历得到的 `n` 正好是链表的真实长度。  
  2. 根据题目定义，**中间节点的下标是 ⌊n/2⌋**（0‑based），所以只要走到第 `⌊n/2⌋` 步，就一定能站在中间节点上。  
  3. 把前驱节点的 `next` 指向后继节点，就等价于把中间节点从链表中移除，且不影响其它节点的相对顺序。  

- **时间/空间复杂度**：  
  - **时间**：我们要 **遍历两遍** 链表，第一遍算长度 `n`，第二遍走到中间位置并修改指针。遍历一次的工作量是 `O(n)`，两次就是 `2·O(n)`，仍然记作 **O(n)**。这里的 `n` 代表链表的节点数。  
  - **空间**：只使用了几个额外的整型变量和指针，**不随 n 增长**，所以是 **O(1)**（常数空间）。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # 节点保存的数值
        self.next = next    # 指向下一个节点的指针

def deleteMiddle(head: ListNode) -> ListNode:
    # 特殊情况：只有一个节点，直接返回 None（空链表）
    if not head or not head.next:
        return None

    # ---------- 第一次遍历：统计长度 ----------
    length = 0
    cur = head
    while cur:
        length += 1          # 走一步，计数器加一
        cur = cur.next

    # 计算中间节点的下标（0-based）
    mid_index = length // 2   # 向下取整，相当于 ⌊n/2⌋

    # ---------- 第二次遍历：找到前驱并修改指针 ----------
    prev = None               # 前驱指针，初始为 None
    cur = head
    for _ in range(mid_index):
        prev = cur            # prev 永远落后 cur 一步
        cur = cur.next        # 向前走一步

    # 此时 cur 正好指向中间节点，prev 指向它的前驱
    # 把 prev 的 next 跳过 cur，指向 cur.next
    prev.next = cur.next
    # Python 会自动回收 cur（中间节点）占用的内存

    return head
```

#### 复杂度

- **时间复杂度**：`O(n)` — 需要遍历链表两次，`n` 是链表长度。  
- **空间复杂度**：`O(1)` — 只用了常数个指针和计数器，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**两次遍历是多余的**：我们在第一次遍历就已经知道了每一步走了多少步，为什么不在同一次遍历里同步得到中间节点呢？  

**关键观察**：如果有两只“指针”，一只快一只慢，快指针每次走两格，慢指针每次走一格，那么当快指针走到链表末尾时，慢指针恰好走到链表的中间。  
- 这正是**快慢指针（Two Pointers）**的经典用法。  
- 快指针的速度是慢指针的两倍，就像提示里说的：“如果一个点速度是 s，走 n 单位；另一个点速度是 2s，走 2n 单位”。  

**实现步骤**：

1. **初始化**  
   - `slow` 指向头结点（慢指针），`fast` 也指向头结点（快指针）。  
   - 再准备一个 `prev` 用来记录 `slow` 的前驱，因为删除节点时需要前驱的 `next` 指针。  

2. **同步移动**  
   - 在循环里：`fast` 每次走两步 `fast = fast.next.next`（如果还能走两步），`slow` 每次走一步 `slow = slow.next`。  
   - 同时把 `prev` 更新为 `slow` 之前的节点 `prev = prev.next`（或在循环前先把 `prev = head`，随后在每次 `slow` 前进前更新 `prev`）。  

3. **循环结束条件**  
   - 当 `fast` 走到末尾（`fast is None` 或 `fast.next is None`）时，`slow` 正好停在 **中间节点**（⌊n/2⌋）。  

4. **删除中间节点**  
   - `prev.next = slow.next` 把前驱直接指向中间节点的后继。  
   - 若链表只有一个节点（`head.next is None`），直接返回 `None`。  

**为什么快慢指针能一次完成**：

- 快指针走的距离是慢指针的两倍。设链表长度为 `n`，循环执行 `k` 次后：  
  - 快指针走了 `2k` 步，慢指针走了 `k` 步。  
  - 当快指针到达或越过末尾时，`2k ≥ n`，所以 `k ≥ n/2`。  
  - 此时慢指针恰好走了 `⌊n/2⌋` 步，正是中间节点的下标。  

**类比**：想象两个人在跑道上跑，快的每次跨两步，慢的每次跨一步。快的跑到终点时，慢的正好站在跑道的中点。

#### 代码（Python）

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def deleteMiddle(head: ListNode) -> ListNode:
    # 边界情况：只有一个节点，删除后返回空链表
    if not head or not head.next:
        return None

    # 初始化：slow 为慢指针，fast 为快指针，prev 用来记录 slow 的前驱
    slow = head          # 慢指针从头开始
    fast = head          # 快指针也从头开始
    prev = None          # 前驱初始为 None

    # 同步移动，fast 每次跳两格，slow 每次跳一格
    while fast and fast.next:
        fast = fast.next.next   # 快指针前进两步（若还能前进）
        prev = slow             # 在 slow 前进一步前，记录它的前驱
        slow = slow.next        # 慢指针前进一步

    # 循环结束时，slow 正好指向中间节点，prev 指向它的前驱
    # 把 prev 的 next 指向 slow 的 next，完成删除
    prev.next = slow.next
    # Python 自动回收被删除的节点

    return head
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次链表，`n` 为节点数。相比暴力解的两次遍历，常数因子更小。  
- **空间复杂度**：`O(1)` — 只用了固定数量的指针变量（`slow`、`fast`、`prev`），不随 `n` 增长。

---

## 心得

- **核心技巧**：**快慢指针**（Two Pointers）一次遍历找中点，随后利用前驱指针完成删除。  
- **适用的题型**：  
  1. “寻找链表中点”或“判断链表是否有环”类题目（如 LeetCode 876、LeetCode 142）。  
  2. “删除链表倒数第 k 个节点”（LeetCode 19）——同样可以用快慢指针实现一次遍历。  
  3. “判断回文链表”（LeetCode 234）——快慢指针帮助找到中点后反转后半段。  
- **一句话总结**：**让快的走两步，慢的走一步，快到终点时慢正好在中点**——这就是“快慢指针找中点”的钥匙。

---

## 反思

- **第一反应**：先统计长度再删除——自然想到两遍遍历的暴力方案。  
- **最容易踩的坑**：  
  - **边界条件**：只有一个节点时需要返回空链表，否则 `prev` 为 `None` 会导致空指针错误。  
  - **快指针的终止条件**：必须检查 `fast` 和 `fast.next` 同时存在，防止访问 `None.next` 抛异常。  
  - **前驱指针的更新时机**：`prev` 必须在 `slow` 前进一步之前更新，否则会指向错误的节点。  
- **下次遇到同类题**，第一步应该想到 **“能否用快慢指针一次遍历完成定位？”**，然后再决定是否需要额外的前驱或后继信息进行修改。