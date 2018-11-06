# #160. 两个链表的交点 / Intersection of Two Linked Lists

> 难度：简单 · 标签：Hash Table、Linked List、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/intersection-of-two-linked-lists/)

---

## 题目（英文原版）

**Description**

Given the heads of two singly linked-lists headA and headB, return the node at which the two lists intersect. If the two linked lists have no intersection at all, return null.
For example, the following two linked lists begin to intersect at node c1:
The test cases are generated such that there are no cycles anywhere in the entire linked structure.
Note that the linked lists must retain their original structure after the function returns.
Custom Judge:
The inputs to the judge are given as follows (your program is not given these inputs):
The judge will then create the linked structure based on these inputs and pass the two heads, headA and headB to your program. If you correctly return the intersected node, then your solution will be accepted.

**Examples**

**Example 1:**

```
Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
Output: Intersected at '8'
Explanation: The intersected node's value is 8 (note that this must not be 0 if the two lists intersect).
From the head of A, it reads as [4,1,8,4,5]. From the head of B, it reads as [5,6,1,8,4,5]. There are 2 nodes before the intersected node in A; There are 3 nodes before the intersected node in B.
- Note that the intersected node's value is not 1 because the nodes with value 1 in A and B (2nd node in A and 3rd node in B) are different node references. In other words, they point to two different locations in memory, while the nodes with value 8 in A and B (3rd node in A and 4th node in B) point to the same location in memory.
```

**Example 2:**

```
Input: intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
Output: Intersected at '2'
Explanation: The intersected node's value is 2 (note that this must not be 0 if the two lists intersect).
From the head of A, it reads as [1,9,1,2,4]. From the head of B, it reads as [3,2,4]. There are 3 nodes before the intersected node in A; There are 1 node before the intersected node in B.
```

**Example 3:**

```
Input: intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
Output: No intersection
Explanation: From the head of A, it reads as [2,6,4]. From the head of B, it reads as [1,5]. Since the two lists do not intersect, intersectVal must be 0, while skipA and skipB can be arbitrary values.
Explanation: The two lists do not intersect, so return null.
```

**Constraints**

- The number of nodes of listA is in the m.
- The number of nodes of listB is in the n.
- 1 <= m, n <= 3 * 104
- 1 <= Node.val <= 105
- 0 <= skipA <= m
- 0 <= skipB <= n
- intersectVal is 0 if listA and listB do not intersect.
- intersectVal == listA[skipA] == listB[skipB] if listA and listB intersect.

---

## 题目（中文翻译）

**描述**  
给定两个单向链表（singly linked list）`headA` 和 `headB` 的头节点，返回两条链表相交的节点。如果两条链表根本不相交，返回 `null`。  

例如，下图中的两条链表在节点 `c1` 处开始相交：  

> 测试用例保证整个链表结构中不存在环。  

> 注意，函数返回后链表必须保持原来的结构不变。

**自定义判题器**  
判题器的输入形式如下（你的程序不会直接得到这些输入）：  
判题器会根据输入构造链表结构，并将两个头节点 `headA`、`headB` 传给你的程序。只要你正确返回相交的节点，答案即被接受。

**示例**  

**示例 1**  
Input: `intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3`  
Output: `Intersected at '8'`  
**Explanation:** 相交节点的值为 8（若两链表相交，这个值一定非 0）。  
从链表 A 的头部读取的序列为 `[4,1,8,4,5]`，从链表 B 的头部读取的序列为 `[5,6,1,8,4,5]`。在 A 中相交节点之前有 2 个节点，在 B 中相交节点之前有 3 个节点。  
- 注意，值为 1 的节点并不是相交节点，因为 A 中的第 2 个节点和 B 中的第 3 个节点是不同的内存地址；而值为 8 的节点（A 的第 3 个节点、B 的第 4 个节点）指向同一块内存，因而是相交点。

**示例 2**  
Input: `intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1`  
Output: `Intersected at '2'`  
**Explanation:** 相交节点的值为 2（若两链表相交，这个值一定非 0）。  
从链表 A 的头部读取的序列为 `[1,9,1,2,4]`，从链表 B 的头部读取的序列为 `[3,2,4]`。在 A 中相交节点之前有 3 个节点，在 B 中相交节点之前有 1 个节点。

**示例 3**  
Input: `intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2`  
Output: `No intersection`  
**Explanation:** 从链表 A 的头部读取的序列为 `[2,6,4]`，从链表 B 的头部读取的序列为 `[1,5]`。由于两条链表不相交，`intersectVal` 必须为 0，`skipA`、`skipB` 可以是任意合法值。  
**Explanation:** 两条链表不相交，返回 `null`。

**约束条件**  

- 链表 A 的节点数记为 `m`，链表 B 的节点数记为 `n`。  
- `1 <= m, n <= 3 * 10^4`  
- `1 <= Node.val <= 10^5`  
- `0 <= skipA <= m`  
- `0 <= skipB <= n`  
- 若两链表不相交，`intersectVal` 为 0。  
- 若两链表相交，则 `intersectVal == listA[skipA] == listB[skipB]`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把链表 A 中的每个节点都和链表 B 的每个节点两两比较**，只要找到两个指针指向同一个内存地址（即同一个节点对象），那就是交点。  
- **使用的结构**：这里的“节点”其实是对象的引用，就像我们平时在字典里查“单词”，只不过这里查的是“地址”。  
- **为什么正确**：因为题目要求返回两个链表**第一次相遇的同一个节点**，如果我们把所有可能的配对都检查一遍，必然会发现这一次相遇。  
- **时间/空间分析**：  
  - 对于每个 A 中的节点（共 `m` 个），我们都要遍历一次 B（共 `n` 个），所以总共要做 `m × n` 次比较。  
  - 用大白话说，**O(m·n)** 就像“把两箱苹果里每个苹果都配对检查”，如果两箱各有 10,000 个苹果，那检查次数就是 1 亿次，明显太慢。  
  - 只用了常数级的额外空间（几个指针），所以 **空间复杂度是 O(1)**。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def getIntersectionNode_brute(headA: ListNode, headB: ListNode) -> ListNode:
    """暴力双循环：逐个比较两个链表的节点引用"""
    curA = headA
    while curA:                     # 遍历链表 A 的每一个节点
        curB = headB
        while curB:                 # 对每个 A 节点，再遍历链表 B
            if curA is curB:        # "is" 判断是否是同一个对象（同一块内存）
                return curA        # 找到交点，直接返回
            curB = curB.next
        curA = curA.next
    return None                      # 两个链表没有交点，返回 None
```

#### 复杂度  

- **时间复杂度**：`O(m·n)` —— 需要把 A 的每个节点和 B 的每个节点都比一次，想象成“两个笛卡尔积”。  
- **空间复杂度**：`O(1)` —— 只用了几个遍历指针，没有额外的数据结构。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**慢在哪里？**  
- **瓶颈**在于双层循环：每次都要把 B 从头遍历完。  
- 我们只需要一次遍历就能判断是否相同，只要能让两个指针**在同一时间走完相同的路程**，就能在交点相遇。

**关键观察**：  
把两条链表看成两条跑道，长度可能不同。若让两个人分别从两个跑道的起点出发跑，当跑完自己的跑道后，**立刻换到对方的跑道继续跑**，那么他们最终会在交点（如果有的话）相遇。  
- 为什么？因为此时每个人走的总路程都是 `lenA + lenB`。如果有交点，两个跑者在交点前的路程是相同的；如果没有交点，两人会在走完两条跑道后同时到达 `null`。

**实现细节**（双指针）  
1. 用指针 `pA`、`pB` 分别指向 `headA`、`headB`。  
2. 每一步都把指针往后走 (`pA = pA.next`，`pB = pB.next`)。  
3. 当指针走到 `null` 时，**切换到另一条链表的头**（`pA = headB`，`pB = headA`）。  
4. 最终两个指针要么在交点相遇（`pA is pB`），要么同时为 `null`（没有交点），循环结束。

**类比**：  
想象两条不同长度的绳子，两个人分别从绳子的一头抓住，走到另一头后再抓住另一根绳子的起点继续走，等他们走的总长度相同，自然会在重叠的那段绳子上相遇。

#### 代码（Python）

```python
def getIntersectionNode_optimal(headA: ListNode, headB: ListNode) -> ListNode:
    """
    双指针技巧：遍历完各自链表后换到另一条链表继续遍历。
    时间 O(m+n)，空间 O(1)。
    """
    if not headA or not headB:      # 任意一条链表为空，直接没有交点
        return None

    pA, pB = headA, headB

    # 最多循环两次链表长度的总和，保证两指针一定会在同一点相遇或同时为 None
    while pA is not pB:
        # 当走到链表尾部时，切换到另一条链表的头部
        pA = pA.next if pA else headB   # 如果 pA 为 None，重新指向 headB
        pB = pB.next if pB else headA   # 同理，pB 为 None 时指向 headA

    # 循环结束时，pA 与 pB 要么同指向交点，要么同为 None
    return pA
```

#### 复杂度  

- **时间复杂度**：`O(m + n)` —— 每个指针最多遍历两条链表的长度，总共不超过 `2·(m+n)` 步。和暴力解相比，**把平方级降到了线性级**，相当于一次“把两箱苹果合并后再检查”。  
- **空间复杂度**：`O(1)` —— 只用了固定数量的指针，**不需要额外的数组或哈希表**。

---

## 心得  

- **核心技巧**：双指针（Two‑Pointer）交叉遍历，让两条不同长度的链表“同步”走完相同的路程。  
- **适用的题型**：  
  1. “环形链表的入口” (`Linked List Cycle II`)——同样使用双指针找相遇点。  
  2. “相加链表的倒序输出” (`Add Two Numbers`)——虽然思路不同，但需要两指针同步遍历。  
  3. “回文链表” (`Palindrome Linked List`)——通过快慢指针定位中点，再反转后比较。  
- **一句话总结**：**让两个指针跑同样的总路程，它们自然会在交点相遇**。

---

## 反思  

- **第一反应**：看到“找交点”，立刻想到把所有节点放进集合（哈希表）再检查。虽然可行，但会用额外的 O(m) 空间。  
- **最容易踩的坑**：  
  - 忘记处理空链表的情况，直接访问 `.next` 会报错。  
  - 误以为可以只比较节点的 `val`，但题目要求比较 **节点本身的引用**（内存地址），否则相同值的不同节点会被误判为交点。  
  - 循环终止条件一定是 `pA is pB`（指针相同），而不是 `pA.val == pB.val`。  
- **下次类似题的第一步**：先思考**“两条路径的长度是否相同”**，如果不相同，就考虑让指针“换跑道”或使用额外空间（哈希表）来对齐长度，再进行比较。这样可以快速定位到双指针或哈希表的解法。