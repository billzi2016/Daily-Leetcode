# #83. 删除已排序链表中的重复元素 / Remove Duplicates from Sorted List

> 难度：简单 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)

---

## 题目（英文原版）

**Description**

Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.

**Examples**

**Example 1:**

```
Input: head = [1,1,2]
Output: [1,2]
```

**Example 2:**

```
Input: head = [1,1,2,3,3]
Output: [1,2,3]
```

**Constraints**

- The number of nodes in the list is in the range [0, 300].
- -100 <= Node.val <= 100
- The list is guaranteed to be sorted in ascending order.

---

## 题目（中文翻译）

给定一个已排序链表 (sorted linked list) 的头节点 `head`，删除所有重复节点，使得每个元素只出现一次。返回同样保持排序的链表。

**示例 1:**  
**示例 2:**  
**约束条件：**

**示例：**  
**示例 1:**  
```
Input: head = [1,1,2]
Output: [1,2]
```

**示例 2:**  
```
Input: head = [1,1,2,3,3]
Output: [1,2,3]
```

**约束条件：**  
- 链表中节点的数量在 `[0, 300]` 区间内。  
- `-100 <= Node.val <= 100`  
- 链表保证按升序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**对每个结点都把后面所有相同的值全部删掉**。  
可以把链表想象成一条“火车”，我们让火车头（`cur`）从头到尾跑；每跑到一个车厢，就让另一根指针（`runner`）从它后面一直往后看，只要发现和 `cur.val` 相同的车厢，就把这节车厢“脱轨”（即把前一个结点的 `next` 指向它的下一个结点）。  

- **数据结构**：这里只用到链表本身以及两个遍历指针。  
  - `cur` 相当于我们手里拿的“放大镜”，指向当前要检查的车厢。  
  - `runner` 像是“清道夫”，负责在 `cur` 后面把所有同样颜色的车厢清理掉。  

这种做法一定能把所有重复的结点删掉，因为每当 `cur` 停在一个值上，`runner` 会把**所有**后面与它相同的结点全部移除。  

**时间复杂度**：  
- 外层遍历 `cur` 需要 O(n) 次。  
- 对每个 `cur`，`runner` 最多会遍历剩下的结点，最坏情况是前 1 个结点要遍历 n‑1 次，第二个结点遍历 n‑2 次……于是总次数约为 n + (n‑1) + … + 1 = O(n²)。  
  - 用大白话说，就是如果链表有 1000 个结点，最多要检查 1000 × 1000/2 ≈ 500 000 次，这在实际中会明显慢下来。  

**空间复杂度**：只用了常数个指针，O(1)。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def deleteDuplicates_bruteforce(head: ListNode) -> ListNode:
    """
    暴力解：对每个结点都用 runner 在后面把相同的值全部删掉
    """
    cur = head                     # cur 负责遍历每个结点
    while cur:                     # 只要还有结点就继续
        runner = cur.next          # runner 从 cur 的下一个结点开始
        prev = cur                 # prev 记录 runner 前面的结点，方便删除
        while runner:              # 遍历 cur 之后的所有结点
            if runner.val == cur.val:          # 发现重复值
                # 把 runner 从链表中摘除：prev.next 直接指向 runner.next
                prev.next = runner.next
                # runner 向后移动，但 prev 不动，因为 prev 仍然指向上一个有效结点
                runner = runner.next
            else:
                # 没有重复，prev 与 runner 都向后走一步
                prev = runner
                runner = runner.next
        cur = cur.next              # cur 前进到下一个结点
    return head
```

#### 复杂度

- **时间复杂度**：`O(n²)` — “n²” 代表如果结点数是 n，最坏情况下要比较大约 n²/2 次。对 300 个结点来说也许还能接受，但随着规模增长会非常慢。  
- **空间复杂度**：`O(1)` — 只用了固定数量的指针，不会随链表长度增长而占用更多额外空间。

---

### 2. 最优解

#### 思路  
从暴力解可以看到**瓶颈**在于每次都要用 `runner` 再遍历一次剩余链表。其实因为**链表已经排好序**，相同的值必然是相邻的。于是我们只需要**一次遍历**，把相邻且相同的结点直接跳过即可。

实现方法：

1. 用一个指针 `cur` 从头到尾走。  
2. 当 `cur` 的下一个结点 `cur.next` 存在且 `cur.val == cur.next.val` 时，说明出现了重复。我们把 `cur.next` 指向 `cur.next.next`，相当于把重复的结点“剪掉”。  
3. 否则，`cur` 向后移动一格。  

这就像在排好序的书架上挑出重复的书，只需要顺手把相邻的同一本书合并，而不必再回头检查整排。  

**核心算法**：**双指针**（其实这里只需要一个指针 `cur`，但逻辑上可以把 `cur.next` 看作第二根指针）。  
- **为什么只要 O(n)**：每个结点最多被访问两次（一次是作为 `cur`，一次是被 `cur.next` 指向后被跳过），所以总体是线性时间。  

**空间**仍然是常数，因为我们只用了几个指针。

#### 代码（Python）

```python
def deleteDuplicates(head: ListNode) -> ListNode:
    """
    最优解：一次遍历，利用链表已排序的特性直接跳过相邻的重复结点
    """
    cur = head                     # cur 指向当前正在检查的结点
    while cur and cur.next:        # 只要当前结点和它的下一个结点都存在
        if cur.val == cur.next.val:        # 两个相邻结点值相同 → 重复
            # 把 cur 的 next 指向下下个结点，等于把中间的重复结点删掉
            cur.next = cur.next.next
            # 注意这里不移动 cur，因为可能还有更多相同的结点需要继续删除
        else:
            # 没有重复，正常向后走一步
            cur = cur.next
    return head
```

#### 复杂度

- **时间复杂度**：`O(n)` — “n” 表示链表长度，遍历一次就完成所有操作。相较于暴力解的 `n²`，效率提升了一个数量级。  
- **空间复杂度**：`O(1)` — 只用了固定的指针，不会随链表长度增加而占用额外内存。

---

## 心得

- **核心技巧**：利用**有序链表的相邻相等**特性，使用**双指针（或单指针 + next）**一次遍历即可去重。  
- **适用的题型**：  
  1. “合并两个有序链表”——同样利用有序性一次遍历。  
  2. “删除链表中所有出现超过一次的节点”——需要稍微改动，但仍然基于相邻比较。  
  3. “对有序数组去重”——思路几乎相同，只是把指针换成数组下标。  
- **一句话总结解题钥匙**：**有序 → 相邻相等 → 只需一次线性扫描**。

## 反思

- **第一反应**：看到“已排序”立刻想到相邻元素一定相等，想用两个指针比较。  
- **最容易踩的坑**：  
  - 忘记在删除节点后 **不要** 移动 `cur`，否则会漏掉连续的多个重复值。  
  - 对空链表或只有一个结点的情况没有提前判断，会导致 `None.next` 报错。  
- **下次遇到同类题**，第一步应该问自己：“数据是否已排序？如果是，重复元素是否一定相邻？”答案是肯定的，就可以直接套用“一遍遍历、相邻比较并跳过”的模板。