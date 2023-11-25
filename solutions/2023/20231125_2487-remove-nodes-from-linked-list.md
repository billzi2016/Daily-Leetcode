# #2487. 从链表中删除节点 / Remove Nodes From Linked List

> 难度：中等 · 标签：Linked List、Stack、Recursion、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/remove-nodes-from-linked-list/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list.
Remove every node which has a node with a greater value anywhere to the right side of it.
Return the head of the modified linked list.

**Examples**

**Example 1:**

```
Input: head = [5,2,13,3,8]
Output: [13,8]
Explanation: The nodes that should be removed are 5, 2 and 3.
- Node 13 is to the right of node 5.
- Node 13 is to the right of node 2.
- Node 8 is to the right of node 3.
```

**Example 2:**

```
Input: head = [1,1,1,1]
Output: [1,1,1,1]
Explanation: Every node has value 1, so no nodes are removed.
```

**Constraints**

- The number of the nodes in the given list is in the range [1, 105].
- 1 <= Node.val <= 105

---

## 题目（中文翻译）

你得到一个链表的头节点（head）。
删除每一个其右侧（anywhere to the right side）存在值更大的节点（node with a greater value）的节点（node）。
返回修改后链表的头节点（head）。

### 示例

#### 示例 1
**输入**: `head = [5,2,13,3,8]`  
**输出**: `[13,8]`  
**解释**: 需要删除的节点是 5、2 和 3。  
- 节点 13 位于节点 5 的右侧。  
- 节点 13 位于节点 2 的右侧。  
- 节点 8 位于节点 3 的右侧。

#### 示例 2
**输入**: `head = [1,1,1,1]`  
**输出**: `[1,1,1,1]`  
**解释**: 每个节点的值都是 1，因此没有节点被删除。

### 约束条件
- 给定链表中的节点数量在 `[1, 10^5]` 区间内。  
- `1 <= Node.val <= 10^5`   (节点值的范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个结点，都往它右边全部遍历一次，看看是否出现了更大的值**。  
如果找到了比当前结点值大的结点，就把当前结点删掉（在链表中把前驱的 `next` 指向当前结点的 `next`），否则保留它。

> **数据结构类比**  
> - 链表就像是一条“人形队列”，每个人只知道下一个人的位置（`next`），而不知道前面或后面的所有人。  
> - “往右遍历”相当于让当前人一个一个地向后看，检查后面有没有比自己更高的大个子。

这种方法一定能得到正确答案，因为我们对每个结点都检查了所有可能的“右侧更大结点”。只要有一个更大的，就按题意删掉。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_nodes_brute(head: ListNode) -> ListNode:
    """暴力解：对每个结点都向右遍历检查是否有更大的值"""
    dummy = ListNode(0)          # 哑结点，方便统一处理头结点被删的情况
    dummy.next = head
    prev = dummy                 # prev 永远指向当前检查结点的前驱

    cur = head
    while cur:
        # 在 cur 右侧寻找是否有更大的值
        runner = cur.next
        need_delete = False
        while runner:
            if runner.val > cur.val:   # 发现更大的结点
                need_delete = True
                break
            runner = runner.next

        if need_delete:                 # 删除 cur
            prev.next = cur.next
        else:                           # 保留 cur，prev 向前走一步
            prev = cur

        cur = cur.next                  # 无论删不删，都向右移动
    return dummy.next
```

#### 复杂度

- **时间复杂度：** `O(n²)`  
  对每个结点都要向右遍历一次，最坏情况下（链表是递增的）要比较 `1 + 2 + … + (n-1) ≈ n²/2` 次。  
  “`O(n²)`” 可以想象成“把 `n` 本书两两配对比较”，次数会非常多。

- **空间复杂度：** `O(1)`  
  只用了几个指针变量，和链表长度无关，常数级空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要往右遍历**，导致大量重复比较。  
观察题目可以发现：

> 如果我们从**右侧往左**遍历链表，已经看到的结点就是当前结点右边的全部结点。  
> 那么只要记录一个「截至目前出现的最大值」`max_sofar`，就能立即判断当前结点是否需要被删除：

- 若 `cur.val < max_sofar` → 右边已经有更大的结点，直接删掉 `cur`。  
- 否则 `cur.val >= max_sofar` → 当前结点是右侧的最大值，需要保留，同时更新 `max_sofar = cur.val`。

**关键点**：链表是单向的，不能直接从尾到头遍历。我们可以把链表的节点值放到栈（或列表）里，先把所有结点压入栈，再弹出时相当于从右到左遍历。

实现步骤：

1. **遍历一次链表，把所有结点放进栈**（栈的特点是后进先出）。  
2. **弹出栈顶元素**，此时弹出的顺序正好是原链表的逆序。  
3. 用 `max_sofar` 维护已经看到的最大值，决定弹出的结点是否保留。  
4. 把保留下来的结点重新用 `next` 链接，构成新的链表（这一步可以在弹出时直接建立，也可以先收集再反向连接）。

这样只遍历了两次链表（一次压栈，一次弹栈），没有嵌套循环，时间降到 `O(n)`。

> **类比**  
> 想象你在看一本从左到右排好的书，每页都有一个数字。  
> 如果你把书翻到最后一页，然后把书页往后倒着放进一个盒子（相当于栈），再从盒子里一页一页抽出来，你看到的顺序就是从后往前的。这样，你只需要记住「看到的最大数字」就能决定每页是否保留。

#### 代码（Python）

```python
def remove_nodes_opt(head: ListNode) -> ListNode:
    """最优解：单调栈 + 逆序遍历，时间 O(n)，空间 O(n)"""
    if not head:
        return None

    # 1. 把所有结点压入栈
    stack = []
    cur = head
    while cur:
        stack.append(cur)      # 入栈，相当于把结点放进盒子
        cur = cur.next

    # 2. 逆序弹栈，维护右侧最大值
    max_sofar = -float('inf')   # 负无穷，保证第一个结点一定会被保留
    new_head = None              # 最终返回的头结点
    while stack:
        node = stack.pop()       # 弹出的是右侧的结点
        if node.val >= max_sofar:
            # 当前结点是右侧的最大值，保留它
            max_sofar = node.val
            node.next = new_head  # 把它接在已经构造好的新链表前面
            new_head = node
        # else: 直接丢弃，不需要任何操作

    return new_head
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  只遍历两遍链表（一次压栈，一次弹栈），每个结点最多被处理两次，和 `n` 成线性关系。  
  相比暴力的 `O(n²)`，这就像把“把 `n` 本书两两配对比较”改成“只顺序读一遍书”，快了很多。

- **空间复杂度：** `O(n)`  
  使用了一个栈保存所有结点，最坏情况下需要 `n` 个指针的空间。  
  （如果不计入输出链表本身的空间，这属于**额外**空间。）

---

## 心得

- **核心技巧**：**单调栈 + 逆序遍历**，通过一次遍历记录右侧最大值，避免重复比较。  
- **适用的题型**  
  1. “删除左侧小于右侧最大值的元素”——如本题。  
  2. “求每个元素右侧第一个更大/更小元素”——典型的 **单调栈** 应用。  
  3. “把数组/链表从右到左处理”——如“逆波兰表达式求值”等。  
- **解题钥匙**：**把“向右看”转化为“从右往左遍历”，并用一个变量记住“目前看到的最大值”。  

---

## 反思

- **第一反应**：直接想到暴力遍历每个结点的右侧。  
- **最容易踩的坑**  
  - **链表头结点被删除**时，需要哑结点或重新返回新的头结点。  
  - **空间限制**：虽然栈的额外空间是 `O(n)`，但在题目限制 `n ≤ 10⁵` 时仍然可以接受；若要求 `O(1)` 空间，需要使用 **递归反转链表**（注意递归深度）或 **原地逆序遍历**（先把链表整体翻转）。  
  - **忘记更新 `next` 指针**：在保留结点时必须把它指向已经构造好的新链表，否则会出现环或断链。  

- **下次类似题目**：第一步先问自己“**能不能把遍历方向反过来**”，如果可以，往往可以把 “右侧最大值” 这类信息用 **一次遍历** 记录下来，从而大幅提升效率。