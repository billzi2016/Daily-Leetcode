# #2807. 在链表中插入最大公约数 / Insert Greatest Common Divisors in Linked List

> 难度：中等 · 标签：Linked List、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/)

---

## 题目（英文原版）

**Description**

Given the head of a linked list head, in which each node contains an integer value.
Between every pair of adjacent nodes, insert a new node with a value equal to the greatest common divisor of them.
Return the linked list after insertion.
The greatest common divisor of two numbers is the largest positive integer that evenly divides both numbers.

**Examples**

**Example 1:**

```
Input: head = [18,6,10,3]
Output: [18,6,6,2,10,1,3]
Explanation: The 1st diagram denotes the initial linked list and the 2nd diagram denotes the linked list after inserting the new nodes (nodes in blue are the inserted nodes).
- We insert the greatest common divisor of 18 and 6 = 6 between the 1st and the 2nd nodes.
- We insert the greatest common divisor of 6 and 10 = 2 between the 2nd and the 3rd nodes.
- We insert the greatest common divisor of 10 and 3 = 1 between the 3rd and the 4th nodes.
There are no more adjacent nodes, so we return the linked list.
```

**Example 2:**

```
Input: head = [7]
Output: [7]
Explanation: The 1st diagram denotes the initial linked list and the 2nd diagram denotes the linked list after inserting the new nodes.
There are no pairs of adjacent nodes, so we return the initial linked list.
```

**Constraints**

- The number of nodes in the list is in the range [1, 5000].
- 1 <= Node.val <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个链表的头节点 `head`，链表中的每个节点都包含一个整数值。  
在每一对相邻节点之间，插入一个新节点，其值等于这两个节点值的最大公约数（Greatest Common Divisor，GCD）。  
返回插入完成后的链表。  

最大公约数是能够同时整除两个数的最大正整数。

**示例 1**  
```
Input: head = [18,6,10,3]
Output: [18,6,6,2,10,1,3]
Explanation: 
- 第一个图示表示原始链表，第二个图示表示插入新节点后的链表（蓝色节点为插入的节点）。
- 在第 1 个节点 18 与第 2 个节点 6 之间插入它们的最大公约数 6。
- 在第 2 个节点 6 与第 3 个节点 10 之间插入它们的最大公约数 2。
- 在第 3 个节点 10 与第 4 个节点 3 之间插入它们的最大公约数 1。
```

**示例 2**  
```
Input: head = [7]
Output: [7]
Explanation: 
- 第一个图示表示原始链表，第二个图示表示插入新节点后的链表。
- 由于链表中不存在相邻节点对，直接返回原链表。
```

**约束条件**  

- 链表中的节点数在范围 `[1, 5000]` 内。  
- `1 <= Node.val <= 1000`   (节点值的取值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把链表从头到尾走一遍，遇到相邻的两个节点 `a` 与 `b` 时：

1. **算出它们的最大公约数（GCD）**。  
   暴力的做法是把 `1 … min(a,b)` 逐个尝试，看哪些整数能同时整除 `a` 与 `b`，取最大的那个。  
   这一步可以想象成 **“在字典里逐页翻找”**：我们从最小的可能答案（1）开始，一页页往上翻，直到找不到更大的能同时整除的数字为止。

2. **在 `a` 与 `b` 之间插入一个新节点**，值就是算出的 GCD。  
   链表的插入就像在一条人形队列中间塞进一个新同学，只需要把前后两个人的 `next` 指针重新指向新同学，再把新同学的 `next` 指向后面那个人。

只要对每一对相邻节点都这么做，最终的链表就满足题目要求。

> **为什么这个方法一定对？**  
> 因为我们对每一对相邻节点都 **严格按照题目描述** 计算了它们的 GCD 并插入了对应的节点，未改变原有节点的相对顺序，也没有遗漏任何相邻对。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def gcd_brute(a: int, b: int) -> int:
    """暴力求最大公约数：从 1 检查到 min(a,b)"""
    limit = min(a, b)
    ans = 1
    for d in range(1, limit + 1):
        if a % d == 0 and b % d == 0:   # 同时能整除
            ans = d                     # 记录最大的 d
    return ans

def insertGreatestCommonDivisors_brute(head: ListNode) -> ListNode:
    """遍历链表，暴力计算 GCD 并插入新节点"""
    cur = head
    while cur and cur.next:          # 只要还有相邻的两个节点
        a, b = cur.val, cur.next.val
        g = gcd_brute(a, b)          # 计算 GCD（暴力版）

        # 在 cur 与 cur.next 之间插入新节点
        new_node = ListNode(g)
        new_node.next = cur.next     # 新节点指向后面的旧节点
        cur.next = new_node          # 前面的节点指向新节点

        # 移动指针：跳过新插入的节点，继续检查下一个原始相邻对
        cur = new_node.next
    return head
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`，其中 `n` 是链表长度，`m = max(Node.val)`（最多 1000）。  
  暴力求 GCD 需要遍历 `1 … min(a,b)`，最坏情况相当于遍历到 1000，所以每对节点的时间是 `O(m)`，全部遍历是 `O(n·m)`。  
  用大白话说，就是“每走一步都要把一把钥匙从第一格一直尝试到第千格”。

- **空间复杂度**：`O(1)`（不计输出链表本身）。  
  我们只用了常数个临时变量，链表本身的节点都是原地复用或新建的，额外占用的内存几乎为零。

---

### 2. 最优解

#### 思路  

暴力求 GCD 的瓶颈在 **“逐个尝试所有可能的除数”**，这一步非常慢。  
数学上已经有更快的办法——**欧几里得算法**（也叫辗转相除法），它利用“`gcd(a,b) = gcd(b, a % b)`”的性质，快速把问题规模缩小。

**优化步骤**：

1. **遍历链表**（这一步本身已经是 `O(n)`，无法再快），对每对相邻节点 `a, b`：
2. 用 **欧几里得算法** 在 `O(log min(a,b))` 的时间内算出 GCD。  
   想象成“把大块的数字不断切成更小的块，直到只能切成 0 为止”，每一步都把问题规模至少减半，所以非常快。
3. **插入新节点** 的操作和暴力版完全相同，仍然是 `O(1)`。

这样整体时间就从 `O(n·m)` 降到了 `O(n·log V)`，其中 `V ≤ 1000`，在实际运行中几乎是瞬间完成。

#### 代码（Python）

```python
def gcd_euclid(a: int, b: int) -> int:
    """欧几里得算法求最大公约数，时间 O(log min(a,b))"""
    while b:
        a, b = b, a % b   # 交换并取余
    return a

def insertGreatestCommonDivisors(head: ListNode) -> ListNode:
    """遍历链表，使用欧几里得算法求 GCD 并插入新节点"""
    cur = head
    while cur and cur.next:
        a, b = cur.val, cur.next.val
        g = gcd_euclid(a, b)      # 快速求 GCD

        # 插入新节点（同暴力版）
        new_node = ListNode(g)
        new_node.next = cur.next
        cur.next = new_node

        cur = new_node.next       # 继续向后走
    return head
```

#### 复杂度  

- **时间复杂度**：`O(n · log V)`，`V` 为链表中节点值的最大值（≤1000）。  
  用大白话说，就是“遍历链表一次，每次只需要把数字除几次（最多 10 次左右）就能得到答案”，相比暴力版的“从 1 扫到 1000”，快了好几百倍。

- **空间复杂度**：`O(1)`（同样只用了常数个临时变量）。

---

## 心得

- **核心技巧**：**欧几里得算法**（快速求最大公约数） + **链表原地插入**。  
- **适用的题型**：  
  1. 需要频繁求 GCD 的链表/数组题目（如 “删除链表中 GCD 大于 1 的节点”）。  
  2. 需要在相邻元素之间插入或删除信息的题目（如 “在数组中插入两数之和”）。  
- **一句话总结**：**把慢的“枚举所有可能”换成快的“数学递推”**，链表本身的遍历不变。

## 反思

- **第一反应**：直接遍历链表，遇到相邻节点就算 GCD、插入新节点——这已经是解法的雏形，只是算 GCD 时用了最直观的枚举。  
- **最容易踩的坑**：  
  - **忘记跳过新插入的节点**，导致在同一对原始节点上重复插入。  
  - **GCD 实现错误**：如果用 `while a != b` 的“暴力相减法”，在数值大时会超时。  
  - **空链表或单节点**：需要提前判断 `head` 是否为空或只有一个节点，直接返回即可。  
- **下次遇到同类题**，第一步应该想到：**“这道题的核心运算是什么？”**如果是 GCD、最小公倍数、素数等，立刻检查是否有**已知的高效算法**（欧几里得、埃拉托斯特尼筛等），再把它和链表/数组的遍历结合起来。