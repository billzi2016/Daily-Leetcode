# #234. 回文链表 / Palindrome Linked List

> 难度：简单 · 标签：Linked List、Two Pointers、Stack、Recursion · [LeetCode 链接](https://leetcode.com/problems/palindrome-linked-list/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list, return true if it is a palindrome or false otherwise.

**Examples**

**Example 1:**

```
Input: head = [1,2,2,1]
Output: true
```

**Example 2:**

```
Input: head = [1,2]
Output: false
```

**Constraints**

- The number of nodes in the list is in the range [1, 105].
- 0 <= Node.val <= 9

---

## 题目（中文翻译）

给定单向链表（singly linked list）的头节点 `head`，如果该链表是回文（palindrome）则返回 `true`，否则返回 `false`。

**示例**

**示例 1**  
输入: `head = [1,2,2,1]`  
输出: `true`

**示例 2**  
输入: `head = [1,2]`  
输出: `false`

**约束条件**

- 链表中的节点数在区间 `[1, 10^5]` 内。  
- `0 <= Node.val <= 9`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的办法是把链表的所有节点值全部取出来，放进一个 **数组（列表）** 中。  
数组可以随机访问，检查回文只需要把数组从左边和右边向中间比对，就像读一本正着和倒着的书。  

- **数据结构类比**：把链表想象成一串珠子，用手把每颗珠子的颜色记下来，放进一本记事本（数组）里。之后检查记事本的内容是否前后相同，就是在检查链表是否回文。  
- **正确性**：如果链表本身是回文，那么把所有值按顺序写下来得到的数组一定也是回文；反之亦然。  
- **时间/空间分析**：  
  - 遍历链表一次把值放进数组，需要 **O(n)** 的时间（n 为节点数）。  
  - 再遍历数组的前后两端比较，同样是 **O(n)** 的时间。  
  - 需要额外的数组来存放 n 个值，空间是 **O(n)**。  

> 大白话解释：如果你有 10 万颗珠子，先把颜色记下来再检查，花的时间大约是两遍 10 万次（每次一次），而额外占用的纸张（数组）也要能写下 10 万个颜色。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def isPalindrome_bruteforce(head: ListNode) -> bool:
    """暴力解：把链表转成数组，再判断数组是否回文"""
    values = []                 # 用来存放链表的所有节点值
    cur = head
    while cur:                  # 第一次遍历链表，把值收集到 values
        values.append(cur.val)  # 把当前节点的值加入列表
        cur = cur.next

    # 用双指针检查 values 是否回文
    left, right = 0, len(values) - 1
    while left < right:         # 只要左指针在右指针左侧，就继续比较
        if values[left] != values[right]:
            return False        # 任意一对不相等就不是回文
        left += 1
        right -= 1
    return True                 # 所有对应位置都相等，说明是回文
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 需要遍历链表一次收集数据，再遍历数组一半进行比较，整体仍然是线性时间。  
- **空间复杂度**：`O(n)` — 额外用了一个长度为 n 的数组来存放节点值。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **空间**：我们用了额外的 `O(n)` 的数组。  
要做到 **O(1) 额外空间**（只用常数个指针），可以利用链表本身的结构：

1. **快慢指针**：让两个指针同时从头开始，慢指针每次走一步，快指针每次走两步。  
   - 当快指针走到链表末尾时，慢指针正好停在链表的中点。  
   - 这一步把链表「前半段」和「后半段」分离出来的入口找到了。

2. **原地翻转后半段**：从慢指针所在的位置开始，把后半段的指针方向逐个反转。  
   - 翻转后，后半段的顺序变成了原来的逆序，正好可以和前半段正序进行一一比较。

3. **比较两段**：用两个指针分别遍历前半段（从头开始）和翻转后的后半段（从新头开始），逐个比较节点值。  
   - 若全部相等，则链表是回文。

4. **恢复链表（可选）**：面试中常常要求在函数结束后恢复原链表结构。只需要再把后半段翻转回来即可。

> **类比**：想象一列火车从两头相向而行，快指针是跑得很快的特快列车，慢指针是普通列车。特快列车到站时，普通列车正好在中间站。我们把中间站之后的车厢调头（翻转），再把前后两段对应车厢的颜色比对，最后把调头的车厢再调回来。

#### 代码（Python）

```python
def isPalindrome_optimal(head: ListNode) -> bool:
    """O(1) 额外空间的回文链表判定"""
    if not head or not head.next:      # 0 或 1 个节点一定是回文
        return True

    # 1. 用快慢指针找到中点（slow 最终指向后半段的起始节点）
    slow = fast = head
    while fast and fast.next:
        slow = slow.next               # 慢指针走一步
        fast = fast.next.next          # 快指针走两步

    # 2. 翻转后半段链表
    prev = None
    cur = slow
    while cur:
        nxt = cur.next                 # 暂存下一节点
        cur.next = prev                # 反转指针
        prev = cur                     # prev 前移
        cur = nxt                      # cur 前移
    # 翻转结束后，prev 指向后半段的头（即逆序后的链表）
    second_half_head = prev

    # 3. 比较前半段和后半段
    p1, p2 = head, second_half_head
    result = True
    while p2:                          # 只需要遍历后半段长度即可
        if p1.val != p2.val:           # 任意一对不相等
            result = False
            break
        p1 = p1.next
        p2 = p2.next

    # 4.（可选）恢复原链表结构——再次翻转后半段
    prev = None
    cur = second_half_head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    # 此时链表已恢复，head 仍指向原始头节点

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历链表常数次（一次找中点、一次翻转、一次比较、一次恢复），仍是线性时间。  
- **空间复杂度**：`O(1)` — 只用了若干指针变量（`slow、fast、prev、cur`），不随节点数增长而增长。  

---

## 心得  

- **核心技巧**：快慢指针定位中点 + 原地翻转链表 + 双指针比较。  
- **适用的题型**：  
  1. 判断链表是否回文（本题）。  
  2. 找到链表的中间节点（`Linked List Middle Node`）。  
  3. 判断链表是否为回文的变形，如「回文子链表」或「回文长度」等。  
- **一句话总结解题钥匙**：**把后半段翻转，使两端可以同步比较**。  

---

## 反思  

- **第一反应**：把链表的值全部存到数组里，直接用数组的回文检查。  
- **最容易踩的坑**：  
  - 忘记处理奇数长度链表的中间节点（它不需要比较）。  
  - 在翻转后忘记把链表恢复，导致后续代码（或面试官）看到结构被破坏。  
  - 快指针可能为空，需要在循环条件中同时检查 `fast` 与 `fast.next`。  
- **下次遇到同类题**：第一步先 **用快慢指针定位中点**，然后思考 **如何在原链表上完成比较**（如翻转、栈或递归），而不是直接搬数据到额外容器。