# #430. 展开多层双向链表 / Flatten a Multilevel Doubly Linked List

> 难度：中等 · 标签：Linked List、Depth-First Search、Doubly-Linked List · [LeetCode 链接](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/)

---

## 题目（英文原版）

**Description**

You are given a doubly linked list, which contains nodes that have a next pointer, a previous pointer, and an additional child pointer. This child pointer may or may not point to a separate doubly linked list, also containing these special nodes. These child lists may have one or more children of their own, and so on, to produce a multilevel data structure as shown in the example below.
Given the head of the first level of the list, flatten the list so that all the nodes appear in a single-level, doubly linked list. Let curr be a node with a child list. The nodes in the child list should appear after curr and before curr.next in the flattened list.
Return the head of the flattened list. The nodes in the list must have all of their child pointers set to null.
How the multilevel linked list is represented in test cases:
We use the multilevel linked list from Example 1 above:
The serialization of each level is as follows:
To serialize all levels together, we will add nulls in each level to signify no node connects to the upper node of the previous level. The serialization becomes:
Merging the serialization of each level and removing trailing nulls we obtain:

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]
Output: [1,2,3,7,8,11,12,9,10,4,5,6]
Explanation: The multilevel linked list in the input is shown.
After flattening the multilevel linked list it becomes:
```

**Example 2:**

```
Input: head = [1,2,null,3]
Output: [1,3,2]
Explanation: The multilevel linked list in the input is shown.
After flattening the multilevel linked list it becomes:
```

**Example 3:**

```
Input: head = []
Output: []
Explanation: There could be empty list in the input.
```

**Example 4:**

```
1---2---3---4---5---6--NULL
         |
         7---8---9---10--NULL
             |
             11--12--NULL
```

**Example 5:**

```
[1,2,3,4,5,6,null]
[7,8,9,10,null]
[11,12,null]
```

**Example 6:**

```
[1,    2,    3, 4, 5, 6, null]
             |
[null, null, 7,    8, 9, 10, null]
                   |
[            null, 11, 12, null]
```

**Example 7:**

```
[1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]
```

**Constraints**

- The number of Nodes will not exceed 1000.
- 1 <= Node.val <= 105

---

## 题目（中文翻译）

你会得到一个**双向链表**（doubly linked list），其中的每个节点除了拥有 `next` 指针、`prev`（previous）指针外，还额外拥有一个 **子指针**（child pointer）。该子指针要么指向 `null`，要么指向另一个**子链表**（child list），该子链表同样由满足上述特性的节点组成。这些子链表可能再拥有自己的子链表，如此递归下去，形成题目示例中所示的**多层结构**（multilevel data structure）。

给定第一层链表的 `head`，请将整个结构**扁平化**（flatten），使所有节点按顺序出现在同一层的**双向链表**中。设 `curr` 为一个拥有子链表的节点，则该子链表中的节点应出现在 `curr` 之后、`curr.next` 之前。返回扁平化后的链表头节点，并确保所有节点的 `child` 指针均被置为 `null`。

---

## 示例

### 示例 1
**输入**  
`head = [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]`

**输出**  
`[1,2,3,7,8,11,12,9,10,4,5,6]`

**解释**  
输入中的多层双向链表如题目示例所示。扁平化后，链表变为：

### 示例 2
**输入**  
`head = [1,2,null,3]`

**输出**  
`[1,3,2]`

**解释**  
输入的多层双向链表如题目示例所示。扁平化后，链表变为：

### 示例 3
**输入**  
`head = []`

**输出**  
`[]`

**解释**  
输入可能为空链表。

### 示例 4
```
1---2---3---4---5---6--NULL
         |
         7---8---9---10--NULL
             |
             11--12--NULL
```

### 示例 5
```
[1,2,3,4,5,6,null]
[7,8,9,10,null]
[11,12,null]
```

### 示例 6
```
[1,    2,    3, 4, 5, 6, null]
             |
[null, null, 7,    8, 9, 10, null]
                   |
[            null, 11, 12, null]
```

### 示例 7
```
[1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]
```

---

## 约束条件

- 节点数量不超过 `1000`。
- `1 <= Node.val <= 10^5`。

---

## 测试用例中多层链表的序列化方式

我们使用示例 1 中的多层链表进行说明：

- 每一层的序列化方式如题目所示。
- 为了将所有层合并序列化，在每一层的末尾加入 `null`，表示该层没有节点连接到上一层的上层节点。合并后去掉末尾的多余 `null`，得到最终的序列化表示。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历整条链表**，一旦遇到 `child` 指针不为空的节点，就把它的子链表“拼”到当前节点和 `next` 之间。  
拼接的过程可以分为三步：

1. **找到子链表的最后一个节点**（就像在一本书里找章节的最后一页，需要顺着 `next` 一直往后走）。
2. **把子链表接在当前节点后面**：  
   - `curr.next` 指向子链表的头部，子链表头的 `prev` 指回 `curr`。  
3. **把原来的 `next`（如果有）接到子链表的尾部**：  
   - 子链表尾的 `next` 指向原来的 `curr.next`，原来的 `next.prev` 指回子链表尾。

完成一次拼接后，继续向后遍历，直到链表结束。

> **为什么正确？**  
> 链表的每一次拼接都保证了 **子链表的所有节点都出现在父节点之后、父节点的原 `next` 之前**，这正是题目要求的顺序。遍历完所有节点后，所有子链表都会被一次性拉平。

> **时间/空间分析（大白话）**  
> - 为每个有子链表的节点，我们都要**从子链表的头走到尾**，这一步是线性的。  
> - 如果有 `k` 个子链表，且每个子链表的长度分别是 `c1, c2, …, ck`，总的遍历次数是 `c1 + c2 + … + ck`。在最坏情况下（每个节点都有子链表且子链表很长），我们会重复遍历同一段链表多次，导致 **时间复杂度接近 O(N²)**（N 为所有节点总数）。  
> - 我们只用了几个指针变量，没有额外的容器，**空间复杂度是 O(1)**。

#### 代码（Python）

```python
# Definition for a Node.
class Node:
    def __init__(self, val, prev=None, next=None, child=None):
        self.val = val          # 节点值
        self.prev = prev        # 前驱指针
        self.next = next        # 后继指针
        self.child = child      # 子链表指针

def flatten_bruteforce(head: 'Node') -> 'Node':
    """暴力版：每次遇到 child，都遍历子链表找到尾部再拼接"""
    if not head:
        return None

    cur = head
    while cur:
        if cur.child:                     # 发现子链表
            # 1️⃣ 找到子链表的最后一个节点
            child_tail = cur.child
            while child_tail.next:        # 像翻书一样一直往后找
                child_tail = child_tail.next

            # 2️⃣ 把子链表接到 cur 后面
            nxt = cur.next                # 先记住原来的 next
            cur.next = cur.child          # cur 的 next 变成子链表头
            cur.child.prev = cur          # 子链表头的 prev 指回 cur
            cur.child = None              # 题目要求 child 置空

            # 3️⃣ 把原来的 nxt 接到子链表尾部
            child_tail.next = nxt
            if nxt:
                nxt.prev = child_tail

        # 继续向后遍历
        cur = cur.next

    return head
```

#### 复杂度

- **时间复杂度**：`O(N²)`（最坏情况下，每次都要遍历子链表的全部节点，类似“每次都把整本书翻一遍”。）
- **空间复杂度**：`O(1)`（只用了常数个指针，没有额外的数据结构。）

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要遍历子链表找尾部**。如果我们能 **一次遍历就把所有节点按照深度优先的顺序连接起来**，就能把时间降到线性 `O(N)`。

一种常用的线性解法是 **使用栈模拟深度优先搜索（DFS）**：

1. **准备一个栈**，先把链表的头节点压进去。栈顶永远保存“下一步要处理的节点”。
2. **循环弹出栈顶**，记为 `node`，把它接到已经展开的链表尾部（维护一个 `prev` 指针指向已经处理好的最后一个节点）。
3. 如果 `node` 有 `next`，先把 `next` **压入栈**（因为我们希望先处理 `child`，后处理 `next`，所以 `next` 要后压）。
4. 如果 `node` 有 `child`，也把 `child` **压入栈**。这样栈顶会先是 `child`，保证子链表在深度优先顺序中先被展开。
5. **切断 `child` 指针**（置为 `None`），因为题目要求所有 `child` 必须为空。
6. 循环结束后，整个链表已经被重新链接成一条平坦的双向链表。

> **为什么正确？**  
> 栈的行为恰好模拟了递归的调用栈：每进入一个子链表，就把当前节点的 `next` 暂时“记住”放进栈，等子链表处理完再回来继续。这样遍历的顺序正是 **先父后子、子先于父的后继**，即题目所要求的顺序。

> **核心数据结构解释**  
> - **栈**：想象成一叠盘子，后放进去的盘子先拿出来。我们把“后面的工作”压进去，等前面的工作（子链表）完成后再取出来继续。
> - **prev 指针**：相当于我们在搭建一条新路，每放一个节点就把它连到前面的路口上。

> **时间/空间分析（大白话）**  
> - 每个节点只会被 **弹出一次、压入一次**，所以总共的操作次数是线性的 `O(N)`。  
> - 栈最多同时保存的节点数等于链表的最大深度（最深的嵌套层数），在最坏情况下可能是 `N`，所以 **空间复杂度是 O(N)**（递归实现的空间也一样）。如果把栈换成递归函数，空间占用同样是递归深度。

#### 代码（Python）

```python
def flatten(head: 'Node') -> 'Node':
    """最优解：使用栈的深度优先遍历，一次遍历完成展开"""
    if not head:
        return None

    stack = [head]          # 栈里先放头结点
    prev = None             # 已经展开好的链表的尾巴

    while stack:
        node = stack.pop()  # 取出当前要处理的节点

        # ① 把 node 接到已展开链表的后面
        if prev:
            prev.next = node
            node.prev = prev
        prev = node          # 更新 tail

        # ② 先把 next 放进栈（后处理），再把 child 放进栈（先处理）
        if node.next:
            stack.append(node.next)   # 记住后面的路
        if node.child:
            stack.append(node.child)  # 先走进子路
            node.child = None         # 题目要求 child 必须置空

    # 最后一个节点的 next 本来已经是 None，保持不变
    return head
```

#### 复杂度

- **时间复杂度**：`O(N)`（每个节点只被访问一次，等价于一次“全程走遍”。）
- **空间复杂度**：`O(N)`（最坏情况下栈里会保存所有节点，相当于递归的调用栈。实际使用中往往远小于 N，因为链表的层数一般不会太深。）

---

## 心得

- **核心技巧**：**深度优先遍历 + 栈（或递归）**，把多层结构按“先子后兄”的顺序线性化。  
- **适用场景**（类似题目）  
  1. **Flatten Nested List Iterator**（把嵌套列表扁平化）  
  2. **Binary Tree Right Side View**（深度优先遍历决定可见节点顺序）  
  3. **N-ary Tree Preorder Traversal**（同样需要栈模拟递归）  
- **一句话总结**：**把“后面的工作”压栈，先把子链表展开，等子链表走完再回头处理原来的后继**。

---

## 反思

- **第一反应**：看到“child 指针”，自然想到递归或 DFS，把子链表当成“子树”来遍历。  
- **最容易踩的坑**  
  - **忘记把 `child` 置空**，导致返回的结构仍然保留旧指针，违反题目要求。  
  - **处理 `prev` 指针不当**，会出现链表断裂或循环（尤其在压栈顺序写反时）。  
  - **空链表或单节点**的特殊情况，需要提前返回。  
- **下次思路**：一看到“多层结构 + 要展开为单层”，立刻联想到 **深度优先 + 栈（或递归）**，先把“后面的兄弟节点”记下来，再把“子层”先处理完。这样可以直接写出线性时间的解法。