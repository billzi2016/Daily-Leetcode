# #24. 两两交换节点 / Swap Nodes in Pairs

> 难度：中等 · 标签：Linked List、Recursion · [LeetCode 链接](https://leetcode.com/problems/swap-nodes-in-pairs/)

---

## 题目（英文原版）

**Description**

Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4]
Output: [2,1,4,3]
Explanation:
```

**Example 2:**

```
Input: head = []
Output: []
```

**Example 3:**

```
Input: head = [1]
Output: [1]
```

**Example 4:**

```
Input: head = [1,2,3]
Output: [2,1,3]
```

**Constraints**

- The number of nodes in the list is in the range [0, 100].
- 0 <= Node.val <= 100

---

## 题目（中文翻译）

给定一个链表（linked list），交换每两个相邻的节点并返回其头节点（head）。必须在不修改链表节点中值的前提下解决此问题（即只能改变节点本身）。

示例 1:
Input: head = [1,2,3,4]
Output: [2,1,4,3]
Explanation:

示例 2:
Input: head = []
Output: []
Explanation:

示例 3:
Input: head = [1]
Output: [1]
Explanation:

示例 4:
Input: head = [1,2,3]
Output: [2,1,3]
Explanation:

约束条件：
- 链表中节点的数量在区间 [0, 100] 内。
- 0 <= Node.val <= 100

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把链表的节点先全部摘下来放进一个「数组」里（想象成把一串珠子取下来排成一排），这样我们就可以像操作普通列表一样，直接把相邻的两个元素互换位置。  
- **数据结构**：这里用到的「数组」相当于生活中的「编号盒子」——我们把每个节点放进去，盒子的下标就是节点在链表中的顺序。  
- **为什么正确**：把节点顺序记在数组里后，互换数组中相邻的两个元素，就等价于把链表中相邻的两个节点的指针调换。最后把数组里的节点重新按照顺序连起来，就得到题目要求的链表。  
- **复杂度分析**：我们需要遍历整条链表一次把节点放进数组（O(n)），再遍历数组一次进行两两交换（O(n)），最后再遍历一次把指针重新接回去（O(n)）。总时间是 3 × O(n) ≈ **O(n)**。  
  但我们用了额外的数组来存放所有节点，额外空间是 **O(n)**（因为需要保存 n 个节点的引用）。

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # 节点的数值
        self.next = next    # 指向下一个节点的指针

def swapPairs_bruteforce(head: ListNode) -> ListNode:
    """
    暴力解：先把所有节点放进数组，再两两交换，最后重新连接成链表。
    """
    # 1. 把链表所有节点收集到列表 nodes 中
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)          # 把当前节点的引用加入数组
        cur = cur.next

    # 2. 两两交换数组中的节点引用
    i = 0
    while i + 1 < len(nodes):
        # 交换相邻的两个元素
        nodes[i], nodes[i + 1] = nodes[i + 1], nodes[i]
        i += 2                     # 跳过已经处理好的两节点

    # 3. 根据新顺序重新链接指针
    for j in range(len(nodes) - 1):
        nodes[j].next = nodes[j + 1]   # 当前节点指向下一个节点
    if nodes:                           # 处理非空链表的情况
        nodes[-1].next = None           # 最后一个节点的 next 设为 None
        return nodes[0]                 # 新的头结点
    else:
        return None                     # 空链表直接返回 None
```

#### 复杂度  

- **时间复杂度**：**O(n)** —— 只要遍历链表三次，每次都是线性规模。  
  这里的 `n` 是链表的节点数。说 O(n) 就是说，节点数翻倍，耗时大概也会翻倍。  

- **空间复杂度**：**O(n)** —— 额外用了一个长度为 `n` 的数组来保存所有节点的引用。  
  如果把链表想成一串珠子，额外的数组就相当于再准备了一盒同样数量的空格子来临时放珠子。

---  

### 2. 最优解  

#### 思路  
从暴力解我们可以看到「两两交换」的本质：只需要把相邻的两个节点的指针重新指向即可，不必把所有节点搬到额外的容器里。  
- **慢在哪里**：暴力解的瓶颈是额外的数组，占用了 O(n) 的空间。实际上我们只需要**局部**地调整指针，不需要全局记住所有节点。  

- **优化思路**：遍历链表时，始终保持对「当前待处理的两节点」的引用。  
  1. 设 `first` 为当前的第一个节点，`second` 为它后面的节点。  
  2. 让 `first.next` 指向 `second.next`（把 `first` 的后继指向「后面未处理的部分」）。  
  3. 让 `second.next` 指向 `first`（完成 `second → first` 的翻转）。  
  4. 再把前一段已经处理好的链表（如果有的话）的尾巴指向 `second`，形成完整的链。  
  5. 把指针移动到 `first.next`，继续处理下一对。  

- **核心数据结构**：**单链表的指针**（`next`），我们只在常数个变量之间来回切换。没有额外容器，空间是 **O(1)**。  

- **递归写法**：另一个直观的实现方式是「把后面的子链表先处理好，再把当前这对节点接在前面」。递归天然符合「先处理子问题」的思路。  
  - 基线情况：链表为空或只有一个节点时，直接返回原头结点。  
  - 递归步骤：`new_head = second`（第二个节点将成为新头），`first.next = swapPairs(second.next)`（把 `first` 接在已处理好的子链表后），`second.next = first`（完成当前这对的翻转）。  

下面分别给出 **迭代版** 与 **递归版**，两者时间均为 O(n)，空间迭代版是 O(1)，递归版因调用栈深度最多 `n/2`，空间是 O(n)（在 Python 中仍然可以接受，因为 n ≤ 100）。

#### 代码（Python）  

```python
# 迭代版：原地两两交换，空间 O(1)
def swapPairs_iterative(head: ListNode) -> ListNode:
    """
    采用哑结点（dummy）简化边界处理。
    通过不断移动指针，把相邻的两节点翻转。
    """
    dummy = ListNode(0)   # 哑结点相当于链表的“前置空位”，方便统一处理头结点
    dummy.next = head
    prev = dummy          # prev 永远指向已经处理好的部分的最后一个节点

    while prev.next and prev.next.next:   # 确保还有至少两节点可以翻转
        first = prev.next                # 第一个待翻转的节点
        second = first.next              # 第二个待翻转的节点

        # ---------- 开始翻转 ----------
        first.next = second.next          # 1) first 指向后面的子链表
        second.next = first               # 2) second 指向 first，完成翻转
        prev.next = second                # 3) 把已处理好的部分接到 second 前面
        # ---------- 翻转结束 ----------

        # 移动 prev 到本轮处理好的最后一个节点（即 original first）
        prev = first

    return dummy.next   # 最终的头结点是 dummy 的下一个节点
```

```python
# 递归版：思路清晰，代码简洁
def swapPairs_recursive(head: ListNode) -> ListNode:
    """
    递归地把后面的子链表先处理好，然后把当前两节点翻转接在前面。
    """
    # 基线条件：空链表或只有一个节点，直接返回
    if not head or not head.next:
        return head

    first = head               # 当前的第一个节点
    second = head.next         # 当前的第二个节点

    # 递归处理后面的子链表，返回的新头接在 first 后面
    first.next = swapPairs_recursive(second.next)

    # 完成本层的翻转：second 成为新头，指向 first
    second.next = first

    return second              # 返回本层的新头结点
```

#### 复杂度  

- **时间复杂度**：**O(n)** —— 每个节点恰好访问一次（无论是迭代还是递归），所以耗时随节点数线性增长。  
- **空间复杂度**：  
  - 迭代版：**O(1)** —— 只用了常数个指针变量，额外空间不随 `n` 增长。  
  - 递归版：**O(n)**（递归栈深度 ≤ n/2），因为每一次递归都会占用一次函数调用的栈帧。但在本题的约束（n ≤ 100）下完全可以接受。  

与暴力解相比，最优解省掉了额外的数组，真正做到「原地」交换，空间使用从 O(n) 降到了 O(1)（或递归的 O(n) 但仍比数组更省）。

---  

## 心得  

- **核心技巧**：**原地指针翻转**（两两交换）以及**哑结点**的使用，帮助统一处理头结点的特殊情况。  
- **适用的题型**：  
  1. “翻转链表的部分或全部” 类题目（如 **Reverse Linked List**, **Reverse Nodes in k-Group**）。  
  2. “删除/插入链表中的特定节点” 类题目（如 **Remove Nth Node From End of List**）。  
  3. “合并/分割链表” 类题目（如 **Merge Two Sorted Lists**, **Split Linked List in Parts**）。  
- **一句话总结**：**只要保持对当前两节点的指针，循环或递归即可在 O(1) 空间内完成两两交换**。

---  

## 反思  

- **第一反应**：把链表全部取出来放进数组，像普通列表那样交换——这就是最直接的「暴力」思路。  
- **最容易踩的坑**：  
  - 忘记处理 **空链表** 或 **只有一个节点** 的情况，会导致 `None` 的属性访问错误。  
  - 在迭代实现中，如果不使用哑结点，处理头结点的翻转会特别繁琐，容易写错 `prev` 的指向。  
  - 递归版要记得把 `first.next` 指向递归结果，否则会形成环路或丢失后面的节点。  
- **下次类似题**：**先思考「局部」如何翻转或连接**，确认是否需要额外容器；若不需要，就立即考虑「指针原地操作」或「递归拆解子问题」的方案。这样可以直接跳到最优解的思路，避免先走不必要的暴力路径。