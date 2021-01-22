# #1171. 删除链表中和为零的连续节点 / Remove Zero Sum Consecutive Nodes from Linked List

> 难度：中等 · 标签：Hash Table、Linked List · [LeetCode 链接](https://leetcode.com/problems/remove-zero-sum-consecutive-nodes-from-linked-list/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list, we repeatedly delete consecutive sequences of nodes that sum to 0 until there are no such sequences.
After doing so, return the head of the final linked list.  You may return any such answer.
(Note that in the examples below, all sequences are serializations of ListNode objects.)

**Examples**

**Example 1:**

```
Input: head = [1,2,-3,3,1]
Output: [3,1]
Note: The answer [1,2,1] would also be accepted.
```

**Example 2:**

```
Input: head = [1,2,3,-3,4]
Output: [1,2,4]
```

**Example 3:**

```
Input: head = [1,2,3,-3,-2]
Output: [1]
```

**Constraints**

- The given linked list will contain between 1 and 1000 nodes.
- Each node in the linked list has -1000 <= node.val <= 1000.

---

## 题目（中文翻译）

给定链表（linked list）的头节点（head），我们需要反复删除那些**和（sum）为 0 的连续节点序列**，直到不存在这样的序列为止。  
处理完毕后，返回最终链表（final linked list）的头节点。任意符合条件的答案均可接受。  
（注意，示例中的所有序列都是对 `ListNode` 对象的序列化表示。）

## 示例

### 示例 1
**输入**  
`head = [1,2,-3,3,1]`

**输出**  
`[3,1]`

**说明**  
答案 `[1,2,1]` 也会被接受。

### 示例 2
**输入**  
`head = [1,2,3,-3,4]`

**输出**  
`[1,2,4]`

### 示例 3
**输入**  
`head = [1,2,3,-3,-2]`

**输出**  
`[1]`

## 约束条件

- 给定的链表中节点数在 **1 到 1000** 之间。
- 链表中每个节点的取值满足 **-1000 ≤ node.val ≤ 1000**。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历链表的每一个起点**，从这个起点向后累加节点值，看看有没有出现累计和为 `0` 的情况。  
- 如果找到了累计和为 `0` 的子序列，就把这段连续的节点全部删除，然后从链表头重新开始检查（因为删除后前面的节点可能又形成了新的零和段）。  
- 继续这个过程，直到遍历一遍都没有找到零和子序列为止。  

**用到的数据结构**  
- **链表**（`ListNode`）本身：我们需要能够“跳过”一段节点，即把前一个节点的 `next` 指向零和子序列后面的节点。可以把它想象成一本书的章节目录，删掉一段章节后，前一章的目录直接指向下一章的起始页。  
- **临时累加变量**：用来记录从当前起点到当前节点的累计和。  

**为什么正确**  
只要我们遍历到所有可能的起点，并检查从该起点向后所有连续的子序列，所有零和子序列必定会被发现并删除。即使删除后产生了新的零和子序列，我们重新从头遍历就能再次捕获它们，直到再也找不到为止。  

**复杂度分析（大白话版）**  
- 对每个节点我们都要向后遍历一次，最坏情况下会遍历 `n` 次，每次遍历的长度也是 `n`，所以时间复杂度是 **O(n²)**。可以把它想象成“每个人都要检查所有人的背包”。  
- 只用了几个指针和一个累计和变量，额外空间是 **O(1)**（不计入输入链表本身的空间）。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def removeZeroSumSublists_bruteforce(head: ListNode) -> ListNode:
    """
    暴力解：对每个起点向后累加，若累计和为 0 则删除这段子链表
    """
    # 为了方便统一处理头节点被删除的情况，先造一个哑节点
    dummy = ListNode(0)
    dummy.next = head

    # 外层循环：遍历每一个可能的起点
    start = dummy
    while start:
        cur_sum = 0          # 累计和，从 start.next 开始
        runner = start.next  # 用 runner 向后遍历
        # 内层循环：尝试所有从 start 开始的子序列
        while runner:
            cur_sum += runner.val
            if cur_sum == 0:               # 找到零和子序列
                # 把 start.next 直接指向 runner.next，等价于删除中间的节点
                start.next = runner.next
                # 删除后要重新从 dummy 开始检查，因为可能出现新的零和段
                break
            runner = runner.next
        # 如果内层循环没有 break，说明从 start 开始没有零和子序列
        if not runner:
            start = start.next
    return dummy.next
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 想象有 `n` 个人排队，每个人都要检查后面所有人的背包，总共要检查约 `n × n / 2` 次。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个指针和一个整数变量，额外占用的空间不随链表长度增长。  



---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要从头遍历一次**，导致大量重复计算。  
我们可以利用**前缀和 + 哈希表** 的思想，只遍历两遍链表，就能一次性找出所有需要删除的零和子序列。

**关键概念——前缀和**  
- 把链表看成一个数组，`prefix[i]` 表示从链表头（包括）到第 `i` 个节点的累计和。  
- 如果在位置 `i` 和位置 `j`（`j > i`）出现了**相同的前缀和**，说明 `i+1 … j` 这段节点的和为 `0`（因为两段累计和相同，中间的增量必须是 `0`）。  
- 于是我们只要把 `i` 节点直接指向 `j` 的下一个节点，就能一次性删掉整段零和子序列。

**哈希表的作用**  
- 哈希表（在 Python 里是 `dict`）可以把“前缀和”映射到**最靠后的出现位置**的节点。  
- 当我们再次遍历链表时，若当前前缀和已经在哈希表里出现过，就直接跳到哈希表中记录的节点的 `next`，等价于把中间的零和段全部删掉。  

**两遍遍历的意义**  
1. **第一遍**：遍历链表，记录每个前缀和最后一次出现的节点。  
2. **第二遍**：再次从头遍历，用同样的前缀和去查表，若表中对应的节点不是当前节点本身，就把当前节点的 `next` 指向表中节点的 `next`，实现删除。  

这样所有零和子序列一次性全部去除，时间只需要 `O(n)`。

**类比**  
- 把链表想象成一条河流，前缀和是河流上游的水位标记。若两段标记相同，说明中间的水位变化相抵消了，形成了“闭环”。我们只要把河道直接从上游的标记连到下游的标记后面，就可以把这段闭环（零和段）剪掉。  

#### 代码（Python）

```python
def removeZeroSumSublists_optimal(head: ListNode) -> ListNode:
    """
    前缀和 + 哈希表（字典）实现 O(n) 的解法
    """
    dummy = ListNode(0)      # 哑节点，统一处理头节点被删除的情况
    dummy.next = head

    # 第一步：遍历记录每个前缀和最后出现的节点
    prefix_to_node = {}      # key: 前缀和，value: 最后出现该前缀和的节点
    cur_sum = 0
    node = dummy
    while node:
        cur_sum += node.val
        prefix_to_node[cur_sum] = node   # 始终覆盖，使得记录的是最靠后的节点
        node = node.next

    # 第二步：再次遍历，用哈希表把零和段跳过
    cur_sum = 0
    node = dummy
    while node:
        cur_sum += node.val
        # 哈希表中对应的节点一定是最靠后的出现位置
        # 直接让当前节点的 next 指向那个节点的 next，即可删除中间的零和段
        node.next = prefix_to_node[cur_sum].next
        node = node.next

    return dummy.next
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了两遍链表，想象每个人只需要检查一次自己的背包，总共 `n` 次操作。比暴力的 `n²` 快了很多。  

- **空间复杂度**：`O(n)`  
  - 需要一个哈希表来存储每个前缀和对应的节点，最坏情况下每个节点的前缀和都不相同，需要 `n` 条记录。相当于在路边放了 `n` 张标记牌。  



---  

## 心得  

- **核心技巧**：前缀和 + 哈希表（字典）能够在一次遍历中定位所有“累计和相同的两点”，从而一次性删掉中间的零和子序列。  
- **适用的题型**：  
  1. **数组/链表中寻找和为目标值的连续子数组**（如 LeetCode 560. Subarray Sum Equals K）。  
  2. **删除链表中满足某种累计条件的节点**（如 LeetCode 1171. Remove Zero Sum Consecutive Nodes from Linked List）。  
  3. **前缀和配合哈希表的区间求和问题**（如 LeetCode 1124. Longest Well-Performing Interval）。  
- **一句话总结**：**“相同的前缀和 → 中间段和为 0，直接跳过即可”。**  



---  

## 反思  

- **第一反应**：把链表转成数组或直接暴力遍历，想“一次一次删”。这往往会导致超时。  
- **最容易踩的坑**：  
  - **哑节点的使用**：如果头节点本身属于零和段，没有哑节点会导致无法正确更新 `head`。  
  - **前缀和的覆盖**：在第一遍遍历时必须记录**最后一次**出现的节点，否则第二遍跳过的范围会不完整。  
  - **负数与正数混合**：累加时要注意负数的影响，前缀和可以是负数，哈希表键值必须完整保存。  
- **下次遇到同类题**：第一步先想“**有没有累计和相同的两个位置**”，如果有，就可以用 **前缀和 + 哈希表** 把中间的区间一次性处理。