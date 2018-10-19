# #138. 复制带随机指针的链表 / Copy List with Random Pointer

> 难度：中等 · 标签：Hash Table、Linked List · [LeetCode 链接](https://leetcode.com/problems/copy-list-with-random-pointer/)

---

## 题目（英文原版）

**Description**

A linked list of length n is given such that each node contains an additional random pointer, which could point to any node in the list, or null.
Construct a deep copy of the list. The deep copy should consist of exactly n brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the next and random pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.
For example, if there are two nodes X and Y in the original list, where X.random --> Y, then for the corresponding two nodes x and y in the copied list, x.random --> y.
Return the head of the copied linked list.
The linked list is represented in the input/output as a list of n nodes. Each node is represented as a pair of [val, random_index] where:
Your code will only be given the head of the original linked list.

**Examples**

**Example 1:**

```
Input: head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**Example 2:**

```
Input: head = [[1,1],[2,1]]
Output: [[1,1],[2,1]]
```

**Example 3:**

```
Input: head = [[3,null],[3,0],[3,null]]
Output: [[3,null],[3,0],[3,null]]
```

**Constraints**

- 0 <= n <= 1000
- -104 <= Node.val <= 104
- Node.random is null or is pointing to some node in the linked list.

---

## 题目（中文翻译）

给定一个长度为 n 的链表（linked list），其中每个节点除了常规的 `next` 指针外，还包含一个额外的随机指针（random pointer），该指针可以指向链表中的任意节点，或者为 `null`。

请构造该链表的深拷贝（deep copy）。深拷贝应恰好包含 n 个全新的节点，每个新节点的 `val` 与对应的原节点相同。新节点的 `next` 指针和 `random` 指针都应指向复制链表中的新节点，使得原链表和复制链表在指针指向关系上保持完全一致。复制链表中的任何指针都不能指向原链表中的节点。

例如，若原链表中有两个节点 X 与 Y，且 `X.random → Y`，则在复制链表中对应的节点 x 与 y 必须满足 `x.random → y`。

返回复制链表的头节点（head）。

链表在输入/输出中以长度为 n 的节点列表形式表示。每个节点用 `[val, random_index]` 的二元组表示，其中 `val` 为节点的值，`random_index` 为该节点的随机指针指向的节点在列表中的下标（若为 `null` 则表示随机指针为空）。

你的代码只会收到原链表的头节点 `head` 作为入口。

### 示例

#### 示例 1
**输入**  
`head = [[7,null],[13,0],[11,4],[10,2],[1,0]]`  
**输出**  
`[[7,null],[13,0],[11,4],[10,2],[1,0]]`

#### 示例 2
**输入**  
`head = [[1,1],[2,1]]`  
**输出**  
`[[1,1],[2,1]]`

#### 示例 3
**输入**  
`head = [[3,null],[3,0],[3,null]]`  
**输出**  
`[[3,null],[3,0],[3,null]]`

### 约束

- `0 <= n <= 1000`
- `-10^4 <= Node.val <= 10^4`
- `Node.random` 为 `null` 或指向链表中的某个节点

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把原链表的每个节点都复制一遍，只管把 `next` 指针接好，**不管 `random`**。  
随后我们再遍历一遍新链表，对每个新节点的 `random` 指针去原链表里**线性查找**它应该指向的那个节点（因为 `random` 可能指向任意位置），找到后再把新节点的 `random` 指向对应的复制节点。  

- **使用的数据结构**：普通的单向链表。这里没有使用哈希表，查找过程就像在一本电话簿里从头到尾找某个人的名字，一次只能比对一个条目。  
- **为什么正确**：我们保证了每个原节点都有唯一的复制节点，`next` 已经按照原顺序接好。随后对每个 `random` 用遍历找到的原节点对应的复制节点来设置，最终得到的结构和原链表完全一样，只是所有节点都是全新的对象。  

> **时间复杂度的直观解释**  
> `O(n²)` 可以理解为：如果有 1000 个节点，外层遍历 1000 次，内层最坏情况下每次要再遍历 1000 次，总共大约要做 1,000,000 次“比较”。这在数据量稍大时就会明显卡顿。  

#### 代码（Python）  

```python
# Definition for a Node.
class Node:
    def __init__(self, val: int, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random


def copyRandomList_bruteforce(head: 'Node') -> 'Node':
    if not head:
        return None

    # 1️⃣ 只复制节点的值和 next 链接
    cur = head
    dummy = Node(0)          # 虚拟头，帮助我们建立新链表
    new_cur = dummy
    while cur:
        new_cur.next = Node(cur.val)   # 创建新节点
        new_cur = new_cur.next
        cur = cur.next

    # 2️⃣ 再遍历一次，为每个新节点补上 random 指针
    #    这里需要把原链表和新链表对应起来，使用两个指针同步前进
    cur = head
    new_cur = dummy.next
    while cur:
        # 如果当前节点的 random 不是 None，需要在原链表里找它指向的节点
        if cur.random:
            # 线性查找对应的目标节点在原链表中的位置
            target = head
            steps = 0
            while target != cur.random:
                target = target.next
                steps += 1
            # 用相同的步数在新链表里找到对应的复制节点
            copy_target = dummy.next
            for _ in range(steps):
                copy_target = copy_target.next
            new_cur.random = copy_target
        # 否则 random 本来就是 None，保持不变
        cur = cur.next
        new_cur = new_cur.next

    return dummy.next
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 次复制 `next`，内层为每个 `random` 再遍历一次最坏 `n` 次。  
  - 用通俗的话说，就是“每个节点都要去找一次它的随机指向”，相当于“找东西时每次都从头再找”。  

- **空间复杂度**：`O(n)`（用于存放新节点本身）  
  - 除了新链表本身不额外使用额外的数据结构，只有递归栈/临时指针占 `O(1)`，所以额外空间是常数级。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要线性搜索原链表来定位 `random`**。如果我们能**直接把原节点和它的复制节点关联起来**，就不需要再遍历查找。  

有两种常见的“关联”方式：

1. **哈希表**：遍历一次把 `old_node → new_node` 放进字典，第二遍直接用字典查找，时间 `O(n)`，额外空间 `O(n)`。  
2. **原地交叉（Interleaving）**：在原链表的 `next` 位置**直接插入复制节点**，形成  
   ```
   A → A' → B → B' → C → C' → …
   ```
   这样原节点的 `random` 指向的目标的复制节点，就是 `original.random.next`。  
   只需要三遍线性扫描，就能完成复制、设置 `random`、拆分两条链表，**不使用额外的哈希表**，空间 `O(1)`（不计新节点本身）。  

下面详细讲解**交叉法**，因为它在 LeetCode 上是推荐的 O(1) 额外空间解法。  

**步骤拆解**  

1. **交叉复制**：遍历原链表，对每个节点 `cur` 创建一个新节点 `copy`，把 `copy` 插在 `cur` 后面，`cur.next = copy`，`copy.next = next_original`。  
   - 类比：把旧的书页和新写的笔记页 **胶合** 在一起，笔记页紧跟在原页后面。  

2. **设置 random**：再次遍历交叉链表，此时每个原节点的 `random`（如果不为空）对应的复制节点就在 `cur.random.next`。于是 `cur.next.random = cur.random.next`。  
   - 类比：原书页指向某页的脚注，笔记页的脚注只需要指向对应的笔记页即可，位置就是 “原页的脚注后面那一页”。  

3. **拆分链表**：最后一次遍历，把交叉在一起的两条链表分别拆开。利用两个指针 `old`、`new`，把 `old.next` 指回下一个原节点，`new.next` 指向下一个复制节点。遍历结束后返回复制链表的头。  

**为什么 O(1) 额外空间**：我们只使用了几个临时指针，所有“关联信息”都藏在链表本身的 `next` 指针里，没有额外的数组或字典。  

#### 代码（Python）  

```python
# Definition for a Node.
class Node:
    def __init__(self, val: int, next: 'Node' = None, random: 'Node' = None):
        self.val = val
        self.next = next
        self.random = random


def copyRandomList(head: 'Node') -> 'Node':
    if not head:
        return None

    # 1️⃣ 交叉复制：在每个原节点后面插入它的复制节点
    cur = head
    while cur:
        copy_node = Node(cur.val)          # 创建复制节点
        copy_node.next = cur.next          # 复制节点的 next 指向原节点的下一个节点
        cur.next = copy_node               # 原节点的 next 指向复制节点，实现交叉
        cur = copy_node.next               # 继续处理下一个原节点

    # 2️⃣ 为复制节点设置 random 指针
    cur = head
    while cur:
        if cur.random:                     # 原节点有 random 才需要设置
            cur.next.random = cur.random.next   # 复制节点的 random = 原节点 random 的复制节点
        # 如果 cur.random 为 None，复制节点的 random 默认就是 None
        cur = cur.next.next                # 跳过复制节点，来到下一个原节点

    # 3️⃣ 拆分两条链表，恢复原链表并得到复制链表的头部
    cur = head
    copy_head = head.next                  # 第一个复制节点的头
    while cur:
        copy_node = cur.next               # 复制节点
        cur.next = copy_node.next          # 恢复原链表：原节点的 next 跳过复制节点
        # 处理复制链表的 next（如果还有后继复制节点的话）
        if copy_node.next:
            copy_node.next = copy_node.next.next
        cur = cur.next                     # 前进到下一个原节点

    return copy_head
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了三遍链表，每遍都是线性操作。可以把它想象成“只需要走一次路就把所有东西搬完”。  

- **空间复杂度**：`O(1)`（不计新建节点本身）  
  - 只用了常数个指针变量，所有“映射信息”都藏在链表内部的 `next` 指针里。与暴力解相比，省去了额外的字典或数组。  

---  

## 心得  

- **核心技巧**：**交叉链表（Interleaving）**——把原节点和复制节点交错放在一起，利用 `next` 指针一次性完成 `random` 的指向。  
- **适用的题型**：  
  1. **复制带随机指针的链表**（本题）。  
  2. **克隆带任意指向的图/树**（如 LeetCode 133 “Clone Graph”），思路同样是“旧对象 ↔ 新对象”映射。  
  3. **复制带额外指针的结构**（如带子指针的多叉树、带父指针的链表）。  
- **一句话总结解题钥匙**：**把旧节点和新节点粘在一起，用“后一个”这条隐形的线索一次性把所有指针搬过去**。  

---  

## 反思  

- **拿到题目第一反应**：先把每个节点复制出来，随后再逐个去找 `random` 指向的目标——也就是暴力的 `O(n²)` 思路。  
- **最容易踩的坑**  
  - **空链表**：`head` 为 `None` 时直接返回 `None`。  
  - **random 为 None**：在设置 `random` 时一定要判断，否则访问 `None.next` 会报错。  
  - **拆分时忘记恢复原链表**：如果只把复制链表拆出来而不把原链表的 `next` 恢复，原链表会被破坏，后续使用会出错。  
- **下次遇到同类题，第一步该想到**：**“有没有办法把旧对象和新对象用某种方式关联起来（哈希表或原地交叉）”，这样可以把寻找对应关系的成本从 `O(n²)` 降到 `O(n)`**。