# #328. 奇偶链表 / Odd Even Linked List

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/odd-even-linked-list/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.
The first node is considered odd, and the second node is even, and so on.
Note that the relative order inside both the even and odd groups should remain as it was in the input.
You must solve the problem in O(1) extra space complexity and O(n) time complexity.

**Examples**

**Example 1:**

```
Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]
```

**Example 2:**

```
Input: head = [2,1,3,5,6,4,7]
Output: [2,3,6,7,1,5,4]
```

**Constraints**

- The number of nodes in the linked list is in the range [0, 104].
- -106 <= Node.val <= 106

---

## 题目（中文翻译）

给定一个单向链表（singly linked list）的头节点 `head`，请将所有奇数索引（odd indices）的节点聚集在一起，随后接上所有偶数索引（even indices）的节点，并返回重新排列后的链表。  
链表的第一个节点视为奇数索引，第二个节点视为偶数索引，依此类推。  
需要保证奇数组和偶数组内部节点的相对顺序与原链表保持一致。  
必须在 **O(1) 额外空间复杂度（extra space complexity）** 和 **O(n) 时间复杂度（time complexity）** 下完成本题。

**示例 1**

**示例 2**

**约束条件**

- 链表中节点的数量范围为 `[0, 10⁴]`。  
- `-10⁶ <= Node.val <= 10⁶`

**示例**

**示例 1**  
输入: `head = [1,2,3,4,5]`  
输出: `[1,3,5,2,4]`

**示例 2**  
输入: `head = [2,1,3,5,6,4,7]`  
输出: `[2,3,6,7,1,5,4]`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把原链表的节点一个一个取出来，分别放进 **奇数位列表** 和 **偶数位列表**，等全部遍历完后再把这两段链表拼接起来。  
- **链表节点**可以想象成一串珠子，每个珠子都有一个指向下一个珠子的绳子（`next` 指针）。  
- **奇数位列表**、**偶数位列表**就像两根新的绳子，我们把珠子按奇偶交错地挂到对应的绳子上。  
- 最后把奇数位绳子的尾巴接到偶数位绳子的头部，就得到题目要求的顺序。

这种做法之所以能得到正确答案，是因为我们严格按照原来出现的顺序把奇数下标的节点保留下来，再保留下偶数下标的节点，最后再拼接，**相对顺序没有被改变**。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点保存的数值
        self.next = next        # 指向下一个节点的指针

def oddEvenList_brute(head: ListNode) -> ListNode:
    if not head or not head.next:          # 链表长度 0 或 1 时直接返回
        return head

    # 两个哑结点（dummy）帮助我们快速创建新链表
    odd_dummy = ListNode(0)                # 奇数位链表的头结点（不计入答案）
    even_dummy = ListNode(0)               # 偶数位链表的头结点（不计入答案）
    odd_cur, even_cur = odd_dummy, even_dummy

    idx = 1                                # 记录当前节点是第几位（从 1 开始）
    cur = head
    while cur:
        if idx % 2 == 1:                   # 奇数位
            odd_cur.next = cur             # 把当前节点接到奇数链表后面
            odd_cur = odd_cur.next
        else:                              # 偶数位
            even_cur.next = cur            # 把当前节点接到偶数链表后面
            even_cur = even_cur.next
        cur = cur.next
        idx += 1

    # 结束后要把两个链表断开，防止出现环
    odd_cur.next = None
    even_cur.next = None

    # 把奇数链表接到偶数链表后面
    odd_cur.next = even_dummy.next
    return odd_dummy.next                  # 去掉哑结点，返回真实的头结点
```

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历了一遍链表，`n` 是链表的节点数。可以把 O(n) 想象成“随节点数线性增长”，节点多多少时间就多多少。  
- **空间复杂度：O(n)** — 除了原链表外，我们用了两个额外的链表来保存奇偶节点，最坏情况下需要额外保存几乎所有节点（即 `n` 个指针），因此空间不是常数。  

---

### 2. 最优解  

#### 思路  

暴力解虽然时间已经是线性的，但**用了额外的 O(n) 空间**，而题目要求 **O(1) 额外空间**。  
瓶颈在于我们把节点重新“拷贝”到两条新链表上。其实链表的节点本身已经是我们需要的“珠子”，只要把它们的 `next` 指针重新摆放，就可以在原地完成重排，不必新建任何节点。

**核心思路**：  
1. 用两个指针 `odd`、`even` 分别指向当前奇数位节点和偶数位节点。  
2. 再用一个指针 `even_head` 记住偶数位链表的起始位置（后面要接到奇数位链表后面）。  
3. 通过一次遍历，把奇数位节点的 `next` 指向下一个奇数位节点（即 `odd.next = even.next`），然后把偶数位节点的 `next` 指向下一个偶数位节点（即 `even.next = odd.next`）。  
4. 当 `even` 或 `even.next` 为 `None` 时，说明已经遍历完链表。此时把奇数位链表的尾巴 `odd` 接到偶数位链表的头 `even_head` 上即可。

可以把这个过程想象成两根手中的绳子（奇、偶），我们不断把珠子从原来的顺序“剪下来”，重新挂到对应的绳子上，最后把两根绳子拼在一起。

#### 代码（Python）

```python
def oddEvenList(head: ListNode) -> ListNode:
    """
    O(1) 额外空间的原地重排
    """
    if not head or not head.next:          # 长度 < 2 的链表直接返回
        return head

    odd = head                             # 第一个节点是奇数位
    even = head.next                       # 第二个节点是偶数位
    even_head = even                       # 记录偶数位链表的头，后面要接到 odd 链表后

    # 循环条件：确保 even 和 even.next 均不为空
    while even and even.next:
        odd.next = even.next                # odd 指向下一个奇数位节点
        odd = odd.next                      # odd 前进一步

        even.next = odd.next                # even 指向下一个偶数位节点
        even = even.next                    # even 前进一步

    # 循环结束后，odd 已经是奇数位链表的最后一个节点
    odd.next = even_head                    # 把偶数位链表接在后面
    return head
```

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历一次链表，每个节点的指针最多改动两次。  
- **空间复杂度：O(1)** — 只用了常数个指针 (`odd`, `even`, `even_head`) 来辅助，不随节点数增长。  

与暴力解相比，时间没有变化，**空间从 O(n) 降到了 O(1)**，这正是题目要求的最优解。

---

## 心得  

- **核心技巧**：**双指针（odd / even）+ 原地指针重连**，在一次遍历中把链表拆分成两段再合并。  
- **适用的题型**：  
  1. “把链表按照某种规则重新排列” 如 `Partition List`（根据阈值划分）  
  2. “链表中间分割” 如 `Reorder List`（奇偶交叉）  
  3. “删除链表中满足特定条件的节点” 如 `Remove Nth Node From End of List`（需要双指针同步前后）  
- **一句话总结解题钥匙**：**一次遍历，用指针把原链表“剪枝”成两段，再把两段拼回去**。

---

## 反思  

- **第一反应**：把所有节点拷贝到两个新链表里，然后再合并——直观但用了额外空间。  
- **最容易踩的坑**：  
  - 循环条件写错导致 `None` 的 `next` 被访问（如 `while even and even.next:` 必须同时检查两者）。  
  - 忘记在循环结束后把奇数位链表的尾巴接到偶数位链表的头，否则会出现断链。  
  - 特殊输入如空链表或只有一个节点，需要提前返回。  
- **下次遇到同类题**，第一步应该先**思考是否可以在原链表上直接调整指针**，而不是额外开辟空间。这样往往能直接想到双指针或快慢指针的原地操作方案。