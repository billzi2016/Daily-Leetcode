# #707. 设计链表 / Design Linked List

> 难度：中等 · 标签：Linked List、Design · [LeetCode 链接](https://leetcode.com/problems/design-linked-list/)

---

## 题目（英文原版）

**Description**

Design your implementation of the linked list. You can choose to use a singly or doubly linked list.
A node in a singly linked list should have two attributes: val and next. val is the value of the current node, and next is a pointer/reference to the next node.
If you want to use the doubly linked list, you will need one more attribute prev to indicate the previous node in the linked list. Assume all nodes in the linked list are 0-indexed.
Implement the MyLinkedList class:

**Examples**

**Example 1:**

```
Input
["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"]
[[], [1], [3], [1, 2], [1], [1], [1]]
Output
[null, null, null, null, 2, null, 3]

Explanation
MyLinkedList myLinkedList = new MyLinkedList();
myLinkedList.addAtHead(1);
myLinkedList.addAtTail(3);
myLinkedList.addAtIndex(1, 2);    // linked list becomes 1->2->3
myLinkedList.get(1);              // return 2
myLinkedList.deleteAtIndex(1);    // now the linked list is 1->3
myLinkedList.get(1);              // return 3
```

**Constraints**

- 0 <= index, val <= 1000
- Please do not use the built-in LinkedList library.
- At most 2000 calls will be made to get, addAtHead, addAtTail, addAtIndex and deleteAtIndex.

---

## 题目（中文翻译）

设计你的链表实现。你可以选择使用单向链表（singly linked list）或双向链表（doubly linked list）。  
单向链表中的节点（node）应包含两个属性（attribute）：`val` 和 `next`。`val` 表示当前节点的值，`next` 为指向下一个节点的指针/引用（pointer/reference）。  
如果使用双向链表，则还需额外的属性 `prev` 来指示链表中前一个节点。假设链表中的所有节点均采用 **0 索引**（0-indexed）。

实现 `MyLinkedList` 类：

```text
示例 1:
Input
["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"]
[[], [1], [3], [1, 2], [1], [1], [1]]
Output
[null, null, null, null, 2, null, 3]

Explanation
MyLinkedList myLinkedList = new MyLinkedList();
myLinkedList.addAtHead(1);
myLinkedList.addAtTail(3);
myLinkedList.addAtIndex(1, 2);    // 链表变为 1->2->3
myLinkedList.get(1);              // 返回 2
myLinkedList.deleteAtIndex(1);    // 此时链表为 1->3
myLinkedList.get(1);              // 返回 3
```

约束条件
- `0 <= index, val <= 1000`
- 请不要使用语言自带的 `LinkedList` 库。
- 至多会调用 `get`、`addAtHead`、`addAtTail`、`addAtIndex` 和 `deleteAtIndex` 共计 2000 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把链表当成 **Python 列表**（`list`）来实现：  
- 用一个普通的数组 `arr` 保存所有元素的值。  
- `addAtHead(val)` 就是把 `val` 插到数组最前面（`arr.insert(0, val)`），  
- `addAtTail(val)` 把 `val` 追加到数组末尾（`arr.append(val)`），  
- `addAtIndex(index, val)` 用 `arr.insert(index, val)`，  
- `deleteAtIndex(index)` 用 `arr.pop(index)`，  
- `get(index)` 直接返回 `arr[index]`（如果下标合法）。  

这里用到的 **数据结构** 是 Python 的动态数组。可以把它想象成一本 **笔记本**，每页记录一个数字；插入、删除时要把后面的页码往后（或往前）搬一搬，就像在纸上写字时需要把后面的文字整体移动一样。

**为什么这个方法是正确的**：  
只要我们保证每次操作都严格按照题目要求在数组的对应位置插入、删除或读取，就一定能得到和真正链表同样的顺序和结果。因为链表本质上也是“一个一个节点顺序相连”，而数组把这些节点顺序紧凑地存放在内存里，两者在功能上是等价的。

**复杂度分析**（用大白话解释）：

| 操作 | 关键函数 | 最坏情况需要搬动多少元素？ | 时间复杂度 | 解释 |
|------|----------|---------------------------|------------|------|
| `addAtHead` / `addAtTail` | `list.insert(0, ...)` / `list.append` | `addAtHead` 需要把所有元素往后搬一位，`addAtTail` 不需要搬动 | `O(n)` / `O(1)` | `n` 是当前链表长度，`O(n)` 就是“和链表长度成正比”。 |
| `addAtIndex` | `list.insert(index, ...)` | 最多搬动 `n-index` 个元素，最坏是搬动 `n` 个 | `O(n)` | 仍然和链表长度成正比。 |
| `deleteAtIndex` | `list.pop(index)` | 需要搬动 `n-index-1` 个元素，最坏是搬动 `n` 个 | `O(n)` | 同理。 |
| `get` | 直接索引 | 不搬动 | `O(1)` | 直接取值，跟数组下标一样快。 |

空间上我们只用了一个数组来存所有节点，**空间复杂度是 `O(n)`**（`n` 为链表当前的元素个数），因为每个元素都要占一个位置。

#### 代码（Python）  

```python
class MyLinkedList:
    """ 暴力版：内部直接用 Python 列表实现 """
    def __init__(self):
        # 用一个列表保存所有节点的值
        self.arr = []                     # 相当于“笔记本的所有页”

    def get(self, index: int) -> int:
        # 如果下标越界，返回 -1
        if index < 0 or index >= len(self.arr):
            return -1
        return self.arr[index]            # 直接读第 index 页的内容

    def addAtHead(self, val: int) -> None:
        # 在最前面插入，需要把后面的页码整体往后搬
        self.arr.insert(0, val)

    def addAtTail(self, val: int) -> None:
        # 在最后面追加，不需要搬动其他页
        self.arr.append(val)

    def addAtIndex(self, index: int, val: int) -> None:
        # 如果 index 大于当前长度，直接不插入（题目要求）
        if index > len(self.arr):
            return
        # index 为负数时，等价于在头部插入
        if index < 0:
            index = 0
        self.arr.insert(index, val)       # 把后面的页整体往后搬

    def deleteAtIndex(self, index: int) -> None:
        # 越界直接不操作
        if index < 0 or index >= len(self.arr):
            return
        self.arr.pop(index)               # 删除后面的页整体往前搬
```

#### 复杂度  

- **时间复杂度**  
  - `get`：`O(1)`，直接索引。  
  - `addAtHead`、`addAtIndex`、`deleteAtIndex`：最坏 `O(n)`，因为可能要搬动整个数组。  
  - `addAtTail`：`O(1)`，只在末尾追加。  

- **空间复杂度**  
  - `O(n)`，需要额外的数组来存储所有节点的值。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于每次插入或删除都要把后面的元素整体搬动，这在链表的实际实现里是不需要的。真实的链表是由 **节点**（`Node`）通过指针（`next`）串起来的，插入或删除只需要改动几条指针，而不需要遍历其余节点。

**从暴力到真正的链表**，我们要做的改动有三步：

1. **定义节点结构**  
   - 每个节点保存自己的数值 `val`，以及指向下一个节点的指针 `next`。  
   - 为了让头部的插入、删除更统一，常用一个 **哑节点（dummy head）**。它本身不存储有效数据，只是一个“假的头”，这样即使要在第 0 位插入，也不需要额外判断“是否为空”。  

2. **维护链表长度**  
   - 记录当前链表的节点数 `size`，这样在 `addAtIndex`、`deleteAtIndex`、`get` 时可以先判断下标是否合法，避免遍历整个链表去找 “是否已经到了末尾”。  

3. **实现每个接口**  
   - `get(index)`：从哑节点的下一个开始走 `index` 步，返回对应节点的值。  
   - `addAtHead(val)`：其实是 `addAtIndex(0, val)` 的特例，只需要把新节点插在哑节点之后。  
   - `addAtTail(val)`：等价于 `addAtIndex(size, val)`，因为 `size` 正好是末尾的下一个位置。  
   - `addAtIndex(index, val)`：先判断 `0 ≤ index ≤ size`（等于 `size` 时是尾部插入），然后遍历到 **前驱节点**（即第 `index‑1` 个节点），把新节点接在它后面。  
   - `deleteAtIndex(index)`：先判断 `0 ≤ index < size`，遍历到前驱节点，把它的 `next` 指向要删除节点的下一个，从而把目标节点“踢出去”。  

**关键数据结构**：**单向链表 + 哑节点**。可以把哑节点想象成 **一根专门用来挂链表的绳子起点**，不管链表怎么增删，都只需要在这根绳子上操作，避免了“头部特殊处理”的麻烦。

**为什么时间会提升**：  
- 在链表里插入或删除只需要改动常数条指针，**不需要搬动后面的所有元素**。  
- 但是我们仍然需要 **遍历到目标位置的前驱节点**，这一步是线性的 `O(index)`，最坏情况下是 `O(n)`（当操作在链表尾部时）。  
- 这已经是对题目要求的最优时间了，因为没有额外的辅助结构（如哈希表）可以在 `O(1)` 时间定位任意下标的节点，而题目只允许使用链表本身。

#### 代码（Python）  

```python
class Node:
    """链表的节点"""
    __slots__ = ('val', 'next')          # 节省内存的写法（可选）

    def __init__(self, val: int = 0, next: 'Node' = None):
        self.val = val                     # 节点存的数值
        self.next = next                   # 指向下一个节点的指针


class MyLinkedList:
    """真正的单向链表实现（带哑节点）"""

    def __init__(self):
        # 哑节点不存实际数据，只是链表的“入口”
        self.dummy = Node(0)
        self.size = 0                       # 当前链表的节点个数

    def _get_node(self, index: int) -> Node:
        """
        辅助函数：返回第 index 个节点（从 0 开始计数）。
        这里的 index 必须合法（0 <= index < size），调用前请自行检查。
        """
        cur = self.dummy.next               # 第 0 个真实节点
        for _ in range(index):
            cur = cur.next
        return cur

    def get(self, index: int) -> int:
        """返回第 index 个节点的值，若非法返回 -1"""
        if index < 0 or index >= self.size:
            return -1
        node = self._get_node(index)
        return node.val

    def addAtHead(self, val: int) -> None:
        """在链表头部插入一个新节点"""
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        """在链表尾部追加一个新节点"""
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """
        在第 index 个位置之前插入一个新节点。
        - 若 index == size，等价于在尾部插入。
        - 若 index > size，什么也不做。
        - 若 index < 0，视作在头部插入。
        """
        if index > self.size:
            return
        if index < 0:
            index = 0

        # 找到前驱节点（第 index-1 个），哑节点是第 -1 个前驱
        prev = self.dummy
        for _ in range(index):
            prev = prev.next

        # 把新节点插在 prev 之后
        new_node = Node(val, prev.next)
        prev.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        """删除第 index 个节点（若合法）"""
        if index < 0 or index >= self.size:
            return

        # 找到前驱节点
        prev = self.dummy
        for _ in range(index):
            prev = prev.next

        # 删除操作：让前驱直接指向要删除节点的下一个
        to_delete = prev.next
        prev.next = to_delete.next
        # Python 会自动回收 to_delete（垃圾回收）
        self.size -= 1
```

#### 复杂度  

- **时间复杂度**  
  - `get`：`O(n)`（最坏需要遍历到第 `index` 个节点）。  
  - `addAtHead` / `addAtTail` / `addAtIndex`：`O(n)`（因为需要找到插入位置的前驱）。  
  - `deleteAtIndex`：`O(n)`（同样需要遍历到前驱）。  
  - 这里的 `n` 是当前链表的长度。相较于暴力版，**没有额外的搬动开销**，每次只改动常数条指针。  

- **空间复杂度**  
  - `O(n)` 用于存储 `n` 个节点。  
  - 额外的哑节点和少量变量都是 `O(1)` 的常数空间。  

---

## 心得  

- **核心技巧**：利用 **哑节点** 消除「头部」的特例，配合 **遍历寻找前驱** 完成所有增删改查。  
- **适用场景**：  
  1. 需要频繁在链表中间插入或删除元素的题目（如 “MyLinkedList” 系列、设计双端队列等）。  
  2. 实现 **LRU Cache** 时的双向链表维护。  
  3. 需要在 **单向链表** 中检测环、翻转链表等基础操作。  
- **一句话总结**：**“把链表看成一串用指针相连的珠子，插入删除只动几根线，不搬珠子”。**  

---

## 反思  

- **第一反应**：直接用 Python 列表实现，写起来最快，却忽略了链表的指针特性。  
- **最容易踩的坑**  
  - **下标合法性**：`addAtIndex` 允许 `index == size`（尾部插入），但不允许更大；`deleteAtIndex` 必须 `0 ≤ index < size`。  
  - **负数下标**：题目规定负数视为在头部插入，需要自行处理。  
  - **哑节点的使用**：忘记把新节点接在 `prev.next` 前会导致链表断裂。  
- **下次遇到同类题**：第一步先 **画出节点结构和哑节点的位置**，确认插入/删除都只需要改动指针，再再写代码。这样可以避免边界条件的遗漏，也能更快写出正确实现。