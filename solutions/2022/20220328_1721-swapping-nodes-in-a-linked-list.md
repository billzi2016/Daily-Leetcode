# #1721. 链表中节点交换 / Swapping Nodes in a Linked List

> 难度：中等 · 标签：Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list, and an integer k.
Return the head of the linked list after swapping the values of the kth node from the beginning and the kth node from the end (the list is 1-indexed).

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5], k = 2
Output: [1,4,3,2,5]
```

**Example 2:**

```
Input: head = [7,9,6,6,7,8,3,0,9,5], k = 5
Output: [7,9,6,6,8,7,3,0,9,5]
```

**Constraints**

- The number of nodes in the list is n.
- 1 <= k <= n <= 105
- 0 <= Node.val <= 100

---

## 题目（中文翻译）

给定一个链表的头结点 `head` 和一个整数 `k`。  
返回交换后链表的头结点，交换的对象是从链表开头算起的第 `k` 个节点与从链表末尾算起的第 `k` 个节点的 **值**（链表采用 1 索引）。

---

### 示例

**示例 1**  
输入: `head = [1,2,3,4,5]`, `k = 2`  
输出: `[1,4,3,2,5]`

**示例 2**  
输入: `head = [7,9,6,6,7,8,3,0,9,5]`, `k = 5`  
输出: `[7,9,6,6,8,7,3,0,9,5]`

---

### 约束

- 链表中的节点数记为 `n`。  
- `1 <= k <= n <= 10^5`  
- `0 <= Node.val <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把链表“拍成照片”，也就是把所有节点的值依次放进一个普通的 Python 列表（数组）里。  
- **链表 → 数组**：遍历链表，把每个 `node.val` 追加到 `arr` 中。这个过程就像把一本书的每一页内容抄到纸上，顺序不变。  
- **交换**：因为数组支持下标直接访问，找到第 `k` 个元素（下标 `k-1`）和倒数第 `k` 个元素（下标 `len(arr)-k`），把它们的值互换。  
- **数组 → 链表**：再次遍历原链表，用数组中的新值依次覆盖每个节点的 `val`。相当于把抄好的纸重新贴回书页，只是把两页的内容换了位置。

> **为什么正确？**  
> 链表的结构本身没有改变，只是节点里存的数值被调换了。我们把所有数值抽出来后再写回去，必然得到题目要求的“交换第 k 个和倒数第 k 个节点的值”。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def swapNodes_bruteforce(head: ListNode, k: int) -> ListNode:
    # 1️⃣ 把链表的值收集到数组里
    vals = []                 # 用列表模拟“相册”
    cur = head
    while cur:
        vals.append(cur.val)  # 把每个节点的值“拍照”保存
        cur = cur.next

    n = len(vals)             # 链表长度
    # 2️⃣ 交换第 k 个和倒数第 k 个位置的值
    left_idx = k - 1          # 0 基础下标
    right_idx = n - k
    vals[left_idx], vals[right_idx] = vals[right_idx], vals[left_idx]

    # 3️⃣ 再把数组里的值写回链表
    cur = head
    i = 0
    while cur:
        cur.val = vals[i]     # 把“新相片”贴回原位
        cur = cur.next
        i += 1

    return head
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  我们遍历链表两遍（一次收集，一次写回），每次都是线性 `n` 步，常数因子不重要。  
- **空间复杂度：** `O(n)`  
  需要额外的数组来存 `n` 个节点的值，相当于把链表“复制”了一遍。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **空间**：额外用了 `O(n)` 的数组。其实我们只需要 **定位** 两个节点，就可以直接在原链表上交换它们的 `val`，不必把所有值都搬出来。

关键在于 **一次遍历找到两节点**：

1. **先找到第 k 个节点**（从头数）。在遍历时计数，当计数等于 `k` 时记录下来，记作 `first`。  
2. **再找到倒数第 k 个节点**。这一步可以利用 “双指针” 的技巧：  
   - 当我们已经走到第 `k` 个节点时，让另一个指针 `second` 从链表头开始。  
   - 同时让 `first`（此时已指向第 `k` 个节点）继续向后移动，`second` 也向后移动，直到 `first` 到达链表尾部。  
   - 此时 `second` 正好指向倒数第 `k` 个节点。  
   形象地说，就像让两个人在跑道上跑，一人先跑 `k` 步，随后两人一起跑，等先跑的人到终点时，后面那个人正好走了 `n-k` 步，也就是倒数第 `k` 步。

3. **交换 `val`**：只需要 `first.val, second.val = second.val, first.val`。

> **为什么只需要一次遍历？**  
> 第一次遍历我们已经把指针移动到第 `k` 个节点，同时保留了从头到第 `k` 的路径。之后继续走到尾部的过程中，`second` 也同步前进，这样就天然完成了“从头到尾再往回数 k 步”的操作。

#### 代码（Python）

```python
def swapNodes_optimal(head: ListNode, k: int) -> ListNode:
    # 1️⃣ 找到第 k 个节点（从头数）
    cur = head
    count = 1
    while count < k:               # 前进 k-1 步
        cur = cur.next
        count += 1
    first = cur                     # 第 k 个节点

    # 2️⃣ 使用双指针找倒数第 k 个节点
    second = head
    while cur.next:                 # cur 继续走到链表末尾
        cur = cur.next
        second = second.next        # second 与 cur 同步前进

    # 3️⃣ 交换两个节点的值
    first.val, second.val = second.val, first.val

    return head
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  只遍历一次链表（虽然有两个指针，但它们都是线性前进），所以仍是线性时间。  
- **空间复杂度：** `O(1)`  
  只用了常数个额外指针 (`first`, `second`, `cur`) ，不随链表长度增长。

---

## 心得

- **核心技巧**：双指针（快慢指针）一次遍历定位倒数第 `k` 个节点。  
- **适用的题型**  
  1. “链表的倒数第 N 个节点”（LeetCode 19）  
  2. “删除链表的倒数第 N 个节点”（LeetCode 19 进阶）  
  3. “寻找链表的中间节点”（LeetCode 876）——使用快慢指针。  
- **一句话总结**：**“先走 k 步再同步前进，就能在一次遍历中同时拿到正数第 k 与倒数第 k 的位置”。**

---

## 反思

- **第一反应**：把链表转成数组，直接下标交换，思路最直接。  
- **最容易踩的坑**  
  - **k=1 或 k=n**：需要确保指针仍然有效，尤其是倒数第 `k` 与正数第 `k` 可能是同一个节点，交换时不影响即可。  
  - **链表长度为 1**：此时 `first` 与 `second` 是同一个节点，代码仍然正确。  
  - **忘记 `cur.next` 的判断**：在寻找倒数第 `k` 时，必须让 `cur` 走到最后一个节点后才停止，否则 `second` 会提前停。  
- **下次第一步**：先想能否用 **双指针** 同时定位两个目标位置，尽量避免额外的存储空间。这样往往能直接得到 `O(1)` 空间的最优解。