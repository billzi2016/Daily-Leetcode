# #237. 删除链表中的节点 / Delete Node in a Linked List

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/delete-node-in-a-linked-list/)

---

## 题目（英文原版）

**Description**

There is a singly-linked list head and we want to delete a node node in it.
You are given the node to be deleted node. You will not be given access to the first node of head.
All the values of the linked list are unique, and it is guaranteed that the given node node is not the last node in the linked list.
Delete the given node. Note that by deleting the node, we do not mean removing it from memory. We mean:
Custom testing:

**Examples**

**Example 1:**

```
Input: head = [4,5,1,9], node = 5
Output: [4,1,9]
Explanation: You are given the second node with value 5, the linked list should become 4 -> 1 -> 9 after calling your function.
```

**Example 2:**

```
Input: head = [4,5,1,9], node = 1
Output: [4,5,9]
Explanation: You are given the third node with value 1, the linked list should become 4 -> 5 -> 9 after calling your function.
```

**Constraints**

- The number of the nodes in the given list is in the range [2, 1000].
- -1000 <= Node.val <= 1000
- The value of each node in the list is unique.
- The node to be deleted is in the list and is not a tail node.

---

## 题目（中文翻译）

**描述**  
给定一个单向链表（singly-linked list）`head`，以及链表中需要删除的节点 `node`。  
你只能访问到要删除的节点 `node`，而不能访问链表的头节点 `head`。  
链表中所有节点的值均唯一，且保证要删除的节点 `node` 不是链表的最后一个节点（tail）。  

请在不真正从内存中移除节点的前提下，实现对该节点的删除操作，使得链表在逻辑上不再包含该节点。

**自定义测试**  
（此处留空，供用户自行编写测试用例）

**示例 1**  
**输入**: `head = [4,5,1,9]`, `node = 5`  
**输出**: `[4,1,9]`  
**解释**: 给定的节点是值为 `5` 的第二个节点，调用函数后链表应变为 `4 -> 1 -> 9`。

**示例 2**  
**输入**: `head = [4,5,1,9]`, `node = 1`  
**输出**: `[4,5,9]`  
**解释**: 给定的节点是值为 `1` 的第三个节点，调用函数后链表应变为 `4 -> 5 -> 9`。

**约束条件**  

- 链表中节点的数量在 `[2, 1000]` 范围内。  
- `-1000 <= Node.val <= 1000`  
- 链表中每个节点的值互不相同。  
- 待删除的节点一定存在于链表中且不是尾节点。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**先找到要删除的节点的前驱节点**（即它前面那个节点），然后把前驱的 `next` 指针指向要删除节点的下一个节点，从而把目标节点“踢出”链表。

- **使用的数据结构**：单向链表。可以把链表想象成一串火车车厢，`next` 就是车厢之间的连接。要把某个车厢拔掉，必须先找到它前面的车厢，然后把前车厢的连接改成指向后面的车厢。
- **为什么正确**：把前驱的 `next` 改成 `node.next`，相当于把原来的指向 `node` 的指针直接跳到 `node` 的后面，这样在遍历时就永远不会再看到 `node`，等同于删除。
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(n)**，因为我们可能需要从链表头遍历到目标节点的前一个位置，最坏情况下要看遍历 `n‑1` 个节点。  
  - 空间复杂度是 **O(1)**，只用了几个指针变量，和链表大小无关。

> 注意：本题的特殊限制是**我们只能得到要删除的节点 `node`，而得不到链表的头指针 `head`**。如果真的只能拿到 `node`，上面的暴力思路是不可行的——因为没有办法从头开始遍历。但在这里先把“有头指针”的情况讲清楚，方便后面看到为什么要改进。

#### 代码（Python）

```python
# 定义单链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点的值
        self.next = next        # 指向下一个节点的指针

def delete_node_bruteforce(head: ListNode, node: ListNode) -> None:
    """
    暴力版：先找到 node 的前驱，然后把前驱的 next 指向 node.next
    这里假设我们能够拿到 head（实际题目不给），仅作演示。
    """
    # 如果 head 本身就是要删除的节点（这里不会出现，因为题目保证 node 不是尾节点且唯一）
    if head == node:
        # 只能把 head 的值和下一个节点的值交换，再删除下一个节点
        # 这里不做处理，直接返回
        return

    prev = None          # 用来记录当前遍历节点的前一个节点
    cur = head
    while cur is not None and cur != node:
        prev = cur
        cur = cur.next

    # 循环结束后，cur == node，prev 就是 node 的前驱
    if prev is not None:
        prev.next = node.next   # 前驱直接跳过 node
    # Python 会在没有引用时自动回收内存，这里不必手动 free
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 需要遍历最多 `n‑1` 个节点才能找到前驱。  
  *通俗解释*：如果链表有 1000 个元素，最坏情况下要检查 999 次才能找到要删的前面那个。
- **空间复杂度**：`O(1)` —— 只用了 `prev`、`cur` 两个指针，和链表长度无关。

---

### 2. 最优解

#### 思路  

因为**我们只能得到要删除的节点本身**，没有办法从头遍历到它的前驱。于是要**把删除的工作搬到节点本身**完成。

观察链表的结构：

```
... -> A -> B -> C -> ...
        ^node
```

要删除 `B`，只要把 `B` 的值换成后面的 `C` 的值，然后让 `B.next` 指向 `C.next`，相当于把 `C` 从链表中踢出去，而原来的 `B` 现在变成了“内容等同于 C”的节点。由于题目保证 **要删除的节点不是尾节点**，`B.next` 必然存在，这样就可以安全地复制。

- **核心技巧**：**用后继节点覆盖当前节点**。这是一种“在原位”删除的技巧，常用于只能访问局部节点的情况。
- **为什么正确**：链表中每个节点的“身份”其实是它的值加上指向下一个节点的指针。我们把 `node` 的值改成 `node.next.val`，再让 `node.next` 指向 `node.next.next`，相当于把原来的 `node.next`（即 `C`）删掉，而 `node` 本身已经变成了原来 `C` 的样子。遍历时看到的序列正好是把 `B` 删除后的结果。
- **时间/空间复杂度**：只用了常数次指针操作，**时间 O(1)**，**空间 O(1)**，远快于暴力遍历。

> 类比：想象你在一条队伍里，只能看到自己前面的人。若要让前面的人离开，你只能让自己学会前面那个人的名字，然后把前面那个人的肩膀“搬走”。这样队伍里看起来就好像那个人不在了。

#### 代码（Python）

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def delete_node(node: ListNode) -> None:
    """
    最优解：在 O(1) 时间内完成删除。
    思路：用后继节点的值覆盖当前节点，再跳过后继节点。
    """
    # 题目保证 node 不是最后一个节点，所以 node.next 必然存在
    next_node = node.next          # 保存后继节点的引用
    node.val = next_node.val       # 把后继的值写进当前节点
    node.next = next_node.next     # 把当前节点的指针直接指向后继的后继
    # Python 会自动回收 next_node（若没有其它引用），这里不需要显式删除
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做了几次指针赋值和一次值拷贝，跟链表长度无关。  
  *通俗解释*：不管链表有多少个元素，操作时间都是一样的，一下子就完成。
- **空间复杂度**：`O(1)` —— 只用了 `next_node` 这一个临时指针，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：**用后继节点覆盖当前节点**（在只能访问局部节点时的“原位删除”）。
- **适用的题型**：  
  1. **只给定要删除节点的指针**（本题）。  
  2. **在链表中实现 `swap`、`duplicate removal`** 等，需要在局部完成操作的题目。  
  3. **单链表中 “删除中间节点”** 的变形，如 “在 O(1) 时间内删除中间节点”。
- **一句话总结**：**没有前驱？把后继搬进去，指针直接跳过去。**

## 反思

- **第一反应**：先想“遍历找前驱”，因为删除链表节点的常规做法都是先定位前驱。
- **最容易踩的坑**：  
  - 忘记题目保证要删的节点不是尾节点，直接对尾节点使用上述技巧会导致 `node.next` 为 `None`，抛出异常。  
  - 误以为可以直接 `del node`，其实在 Python 中需要改指针而不是释放对象。  
  - 忽视值唯一的前提：如果链表值可能重复，单纯复制后继值会产生错误的逻辑（但本题已保证唯一）。
- **下次遇到同类题**：第一步立刻检查**是否能直接访问后继**，若能且后继存在，就考虑**用后继覆盖当前节点**的 O(1) 方法；若后继不存在，则只能回到“遍历找前驱”的思路。