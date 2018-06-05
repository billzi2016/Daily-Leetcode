# #2. 两数相加 / Add Two Numbers

> 难度：中等 · 标签：Linked List、Math、Recursion · [LeetCode 链接](https://leetcode.com/problems/add-two-numbers/)

---

## 题目（英文原版）

**Description**

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.

**Examples**

**Example 1:**

```
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
```

**Example 2:**

```
Input: l1 = [0], l2 = [0]
Output: [0]
```

**Example 3:**

```
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```

**Constraints**

- The number of nodes in each linked list is in the range [1, 100].
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros.

---

## 题目（中文翻译）

**描述**  
给定两个非空的链表（linked list），分别表示两个非负整数（non‑negative integer）。每个链表的数字以逆序方式存储，并且每个节点（node）只包含一位数字。请将这两个数字相加，并以链表的形式返回其和。  
可以假设除数字 0 本身外，这两个数都不存在前导零（leading zero）。

**示例**  

示例 1  
```
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
解释: 342 + 465 = 807.
```

示例 2  
```
Input: l1 = [0], l2 = [0]
Output: [0]
```

示例 3  
```
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```

**约束条件**  

- 每个链表的节点数在 `[1, 100]` 区间内。  
- `0 <= Node.val <= 9`。  
- 保证链表表示的数字没有前导零。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把链表“翻译”成普通整数，两个整数相加后再把结果拆成链表。  
- **把链表转成整数**：链表的每个结点只保存一位数字，且是 **逆序**（最低位在前）。我们可以遍历链表，用一个变量 `num` 累加 `num += node.val * (10 ** position)`，`position` 随遍历递增。  
- **相加**：Python 的整数可以任意大，所以直接 `total = num1 + num2`。  
- **把结果再写回链表**：把 `total` 按十进制一位位取出来（`total % 10`），生成新的链表结点，取完后 `total //= 10`，直到 `total` 为 0。  

> **类比**：把链表看成一本**倒着排的数字手册**，我们先把手册的每页数字抄到一张大纸上（得到整数），再把两张纸相加，最后把相加后的数字重新写回一本新手册（链表）。  

这种方法一定能得到正确答案，因为我们没有改变每位数字的意义，只是换了一种表现形式。  

#### 代码（Python）  
```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 当前结点保存的数字
        self.next = next        # 指向下一个结点

def list_to_int(node: ListNode) -> int:
    """把逆序链表转成整数"""
    num = 0
    base = 1               # 10 的幂次，从 1 开始
    while node:
        num += node.val * base
        base *= 10
        node = node.next
    return num

def int_to_list(num: int) -> ListNode:
    """把整数转成逆序链表（即使 num 为 0 也要返回一个结点）"""
    # 特殊情况：数字本身是 0
    if num == 0:
        return ListNode(0)

    dummy = ListNode(0)    # 虚拟头结点，方便后续操作
    cur = dummy
    while num:
        cur.next = ListNode(num % 10)   # 取最低位
        cur = cur.next
        num //= 10                      # 删除最低位
    return dummy.next   # 返回真实的头结点

def addTwoNumbers_brute(l1: ListNode, l2: ListNode) -> ListNode:
    """暴力解：先转整数，再相加，最后转回链表"""
    n1 = list_to_int(l1)   # 把 l1 转成整数
    n2 = list_to_int(l2)   # 把 l2 转成整数
    total = n1 + n2        # 直接相加
    return int_to_list(total)   # 再写回链表
```

#### 复杂度  
- **时间复杂度**：`O(N + M)`，其中 `N`、`M` 分别是两条链表的长度。我们各遍历一次链表（转整数），再一次遍历结果整数的位数（最多 `max(N, M) + 1` 位），所以整体是线性的。  
- **空间复杂度**：`O(1)`（不计返回链表本身的空间）。在 Python 中大整数会占用额外的内存，但相对于链表长度仍然是常数级别。

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈其实不在时间，而在**“把链表直接变成整数”** 这一步。  
- 在一些语言（如 C/C++、Java）里，整数有固定的位数，超出范围会溢出。  
- 即使在 Python 中，直接构造大整数也会带来额外的 **大数运算开销**（乘 10、加法等），不如直接在链表上做**逐位相加**来得自然。  

**优化思路**：  
1. 同时遍历两条链表，取对应结点的值相加，再加上上一位的进位 `carry`。  
2. 当前位的结果是 `sum % 10`，进位是 `sum // 10`。  
3. 把结果 `sum % 10` 写进新链表的结点。  
4. 当两条链表都遍历完且没有进位时结束。  

这就是**手算加法**的过程，只是把纸上的每一步搬到了代码里。  

> **类比**：把两本**倒着排的数字手册**摞在一起，用笔记本记下每一页的相加结果和进位，最后得到的新手册就是答案。  

核心数据结构仍是**单向链表**，只不过我们不再把它“翻译”为整数，而是**原地**（在新链表上）完成加法。  

#### 代码（Python）  
```python
def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    """
    最优解：边遍历边相加，使用进位变量 carry。
    时间 O(max(N, M))，空间 O(max(N, M))（返回的链表）。
    """
    dummy = ListNode(0)   # 虚拟头结点，帮助处理第一个结点
    cur = dummy
    carry = 0             # 记录上一位的进位，初始为 0

    # 同时遍历两条链表，直到两条都走完且没有进位
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0   # 如果 l1 已经结束，用 0 填充
        v2 = l2.val if l2 else 0   # 同理处理 l2

        total = v1 + v2 + carry    # 当前位的和 + 进位
        carry = total // 10        # 计算新的进位
        cur.next = ListNode(total % 10)   # 当前位的结果放入新结点
        cur = cur.next                     # 移动指针

        # 推进原链表指针（如果还有的话）
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    return dummy.next   # 返回真实的头结点
```

#### 复杂度  
- **时间复杂度**：`O(max(N, M))`。我们只遍历两条链表一次，每次做常数次的加法、取模、除法等操作。  
- **空间复杂度**：`O(max(N, M))`。返回的链表长度最多是 `max(N, M) + 1`（最高位可能产生进位），这属于**输出空间**，算法本身只用了常数级的额外变量（`carry`、`dummy`、`cur`）。  

与暴力解相比，时间上没有本质差别，但**不依赖大整数**，在任何语言都能安全、快速地通过。

---

## 心得  

- 本题考察的是**链表的遍历**和**进位加法**的模拟。  
- 关键技巧：  
  1. 同时遍历多条链表，缺少的位用 `0` 填补。  
  2. 用一个 `carry` 记录进位，保证每一位的计算都是独立的。  
- 类似题型：  
  - *两数相加*（本题的逆序版）  
  - *两数相乘*（链表版）  
  - *链表中的回文数检测*（需要双指针遍历）  
- **一句话总结**：把手算加法搬到链表上，逐位相加并记住进位，就是解题钥匙。  

---

## 反思  

- **第一反应**：把链表转成整数再相加。这个想法直观，但在实际面试中会被问及溢出风险。  
- **最容易踩的坑**：  
  - 忽略了进位会产生新的最高位（如 `999 + 1 = 1000`）。  
  - 当一条链表已经遍历完而另一条还有时，需要用 `0` 补位，否则会出现 `None` 访问错误。  
  - 忘记在循环结束后检查 `carry` 是否为 0，导致最高位缺失。  
- **下次类似题**：第一步先在脑子里写出 **“逐位相加 + 进位”** 的流程，确认每一步都能在链表上实现，再动手编码。