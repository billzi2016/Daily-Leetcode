# #92. 反转链表 II / Reverse Linked List II

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/reverse-linked-list-ii/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list and two integers left and right where left <= right, reverse the nodes of the list from position left to position right, and return the reversed list.

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5], left = 2, right = 4
Output: [1,4,3,2,5]
```

**Example 2:**

```
Input: head = [5], left = 1, right = 1
Output: [5]
```

**Constraints**

- The number of nodes in the list is n.
- 1 <= n <= 500
- -500 <= Node.val <= 500
- 1 <= left <= right <= n

---

## 题目（中文翻译）

给定单链表的头节点 `head` 和两个整数 `left`、`right`（满足 `left <= right`），请将链表中从位置 `left` 到位置 `right` 的节点进行反转，并返回反转后的链表。

**示例 1**  
**Input:** `head = [1,2,3,4,5], left = 2, right = 4`  
**Output:** `[1,4,3,2,5]`

**示例 2**  
**Input:** `head = [5], left = 1, right = 1`  
**Output:** `[5]`

**约束条件**
- 链表中的节点数为 `n`。
- `1 <= n <= 500`
- `-500 <= Node.val <= 500`
- `1 <= left <= right <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把链表变成普通的 Python 列表（数组）**，因为数组可以直接用索引访问，翻转子区间非常方便。  

1. **遍历链表**，把每个节点的值依次存进 `vals`（相当于把链表的“内容”抄写到纸上）。  
2. **在数组上翻转** `[left-1, right-1]` 这段子数组。这里的 `left`、`right` 是从 1 开始计数的，而 Python 的列表是从 0 开始，所以要减 1。  
3. **根据修改后的数组重新构造链表**。重新创建 `ListNode`，把值依次链接起来，得到新的链表头。  

> **类比**：把链表想象成一本书的章节标题，先把所有标题抄到纸上（数组），在纸上把想要倒置的章节标题顺序改掉，再把纸上的标题重新装订成一本新书（链表）。  

**为什么正确**  
- 把所有节点值完整保存下来后，原链表的结构信息已经全部转移到数组里。  
- 在数组上翻转子区间等价于在链表上翻转对应的节点顺序。  
- 重新按照数组的顺序创建节点，得到的链表正好是题目要求的结果。  

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseBetween_brute(head: ListNode, left: int, right: int) -> ListNode:
    """
    暴力解法：把链表转成数组，翻转子数组，再把数组变回链表。
    """
    # 1️⃣ 把链表的所有值存进列表
    vals = []                       # 用列表来临时保存节点值
    cur = head
    while cur:
        vals.append(cur.val)        # 相当于把每个节点的“内容”抄下来
        cur = cur.next

    # 2️⃣ 在数组上翻转指定区间（注意下标从 0 开始）
    # left、right 是基于 1 的位置，需要减 1 才是列表的下标
    vals[left - 1 : right] = reversed(vals[left - 1 : right])

    # 3️⃣ 根据翻转后的数组重新生成链表
    dummy = ListNode(0)             # 虚拟头结点，方便统一处理头指针
    cur = dummy
    for v in vals:                  # 依次把数组里的值挂到新链表上
        cur.next = ListNode(v)
        cur = cur.next

    return dummy.next               # 返回真实的头结点
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历把链表转成数组需要 `O(n)`，  
  - 翻转子数组最多也是 `O(n)`（因为子区间长度 ≤ n），  
  - 再次遍历数组生成链表同样是 `O(n)`。  
  - 综合下来就是线性时间 `O(n)`，即“随节点个数线性增长”。  

- **空间复杂度**：`O(n)`  
  - 额外用了一个长度为 `n` 的数组 `vals` 来存所有节点值，空间随节点数线性增长。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于**用了额外的数组**，占用了 `O(n)` 的额外空间。链表本身已经是“指针串”，我们完全可以**原地在链表上完成翻转**，只需要常数级别的额外变量。  

**核心技巧**：**子链表的原地翻转（head‑insertion 方法）**。  
- 先找到**左边界前一个节点** `pre`（即第 `left-1` 个节点），以及**左边界节点** `cur`（第 `left` 个节点）。  
- 然后在 `[left, right]` 区间内，**把 `cur` 后面的节点一个个摘下来，插到 `pre` 的后面**。  
- 这相当于把子链表的节点**头插**到 `pre` 之后，循环 `right-left` 次后，子链表就完成了翻转。  

下面一步步解释：

1. **加一个哑节点（dummy）**：为了统一处理 `left = 1`（即翻转从头开始）的情况，先在链表头部加一个值为 `0` 的虚拟节点 `dummy`，让 `dummy.next` 指向原头结点。这样 `pre` 永远可以安全地指向“左边界前一个节点”。  

2. **定位 `pre`**：从 `dummy` 开始走 `left-1` 步，得到 `pre`。  
   - 类比：在书的目录里，先翻到第 `left-1` 章节的标题，这个标题就是 `pre`。  

3. **`cur` 指向左边界节点**：`cur = pre.next`，此时 `cur` 是要被翻转的子链表的第一个节点。  

4. **循环翻转**（`right-left` 次）  
   - `temp = cur.next`：取出 `cur` 后面的节点 `temp`（相当于把后面的章节取下来）。  
   - `cur.next = temp.next`：把 `cur` 的指针直接跳过 `temp`，指向 `temp` 的后继。  
   - `temp.next = pre.next`：把 `temp` 插到 `pre` 后面，即插到已经翻转好的子链表最前端。  
   - `pre.next = temp`：更新 `pre` 的后继为 `temp`，完成一次“头插”。  
   - 重复上述步骤，子链表的节点会逐个被搬到 `pre` 之后，顺序自然被逆转。  

5. **返回结果**：`dummy.next` 即为翻转后的链表头。  

> **为什么只需要 O(1) 额外空间**：我们只使用了 `dummy、pre、cur、temp` 四个指针，都是常数个变量，和链表长度无关。  

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    """
    最优解：一次遍历、原地翻转子链表（O(1) 额外空间）。
    """
    # 0️⃣ 加一个哑节点，统一处理 left = 1 的情况
    dummy = ListNode(0)
    dummy.next = head

    # 1️⃣ 找到 left 前一个节点 pre（走 left-1 步）
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next          # pre 最终指向第 left-1 个节点

    # 2️⃣ cur 指向子链表的第一个节点（第 left 个节点）
    cur = pre.next

    # 3️⃣ 在 [left, right] 区间内进行 head‑insertion 翻转
    # 需要翻转的次数是 right - left
    for _ in range(right - left):
        temp = cur.next        # 取出 cur 后面的节点
        # 把 cur 与 temp 之间的链接断开，cur 直接指向 temp 的后继
        cur.next = temp.next
        # 把 temp 插到 pre 之后（即已翻转部分的最前面）
        temp.next = pre.next
        pre.next = temp
        # 经过一次循环，子链表长度不变，但最前面的节点已经换成了 temp

    # 4️⃣ 返回新的头结点
    return dummy.next
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历链表一次（找 `pre` 以及翻转子链表的过程均在同一次遍历中完成），  
  - 随节点数线性增长，和暴力解的时间相同，但不需要额外的遍历。  

- **空间复杂度**：`O(1)`  
  - 只用了固定数量的指针变量，**不随链表长度增长**，所以是常数级别的空间。  

---

## 心得  

- **核心技巧**：子链表的**原地翻转（head‑insertion）**。  
- **适用题型**：  
  1. *Reverse Linked List*（完整链表翻转）  
  2. *Remove Nth Node From End of List*（需要定位前驱节点）  
  3. *Swap Nodes in Pairs*（两两翻转）  
- **一句话总结**：  
  > 把子链表的每个节点依次“摘下来”插到左边界前面，就完成了原地逆序。  

---

## 反思  

- **拿到题目第一反应**：先把链表变成数组，翻转后再恢复——因为数组操作最直观。  
- **最容易踩的坑**  
  - **`left = 1`** 时，左边界前没有节点，若不加哑节点会导致空指针错误。  
  - **循环次数**：要翻转 `right-left` 次，而不是 `right-left+1`（因为 `cur` 本身已经在子链表的开头）。  
  - **指针更新顺序**：一定要先保存 `temp = cur.next`，否则 `cur.next` 改动后会失去后继信息。  
- **下次遇到同类题的第一步**：  
  - 先在链表头部加一个 **哑节点**，把“左边界前一个节点”定位出来，然后思考“把后面的节点一个个搬到前面”是否能完成目标。