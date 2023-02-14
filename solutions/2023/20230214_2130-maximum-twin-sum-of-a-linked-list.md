# #2130. 链表的最大孪生和 / Maximum Twin Sum of a Linked List

> 难度：中等 · 标签：Linked List、Two Pointers、Stack · [LeetCode 链接](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/)

---

## 题目（英文原版）

**Description**

In a linked list of size n, where n is even, the ith node (0-indexed) of the linked list is known as the twin of the (n-1-i)th node, if 0 <= i <= (n / 2) - 1.
The twin sum is defined as the sum of a node and its twin.
Given the head of a linked list with even length, return the maximum twin sum of the linked list.

**Examples**

**Example 1:**

```
Input: head = [5,4,2,1]
Output: 6
Explanation:
Nodes 0 and 1 are the twins of nodes 3 and 2, respectively. All have twin sum = 6.
There are no other nodes with twins in the linked list.
Thus, the maximum twin sum of the linked list is 6.
```

**Example 2:**

```
Input: head = [4,2,2,3]
Output: 7
Explanation:
The nodes with twins present in this linked list are:
- Node 0 is the twin of node 3 having a twin sum of 4 + 3 = 7.
- Node 1 is the twin of node 2 having a twin sum of 2 + 2 = 4.
Thus, the maximum twin sum of the linked list is max(7, 4) = 7.
```

**Example 3:**

```
Input: head = [1,100000]
Output: 100001
Explanation:
There is only one node with a twin in the linked list having twin sum of 1 + 100000 = 100001.
```

**Constraints**

- The number of nodes in the list is an even integer in the range [2, 105].
- 1 <= Node.val <= 105

---

## 题目（中文翻译）

在长度为 *n*（且 *n* 为偶数）的链表中，若 `0 <= i <= (n / 2) - 1`，则第 *i* 个节点（0 索引）被称为第 *(n‑1‑i)* 个节点的 **孪生节点（twin）**。  
**孪生和（twin sum）** 定义为一个节点与其孪生节点的数值之和。  

给定一个长度为偶数的链表的头节点 `head`，返回该链表的 **最大孪生和**。

---

### 示例

#### 示例 1
```
Input: head = [5,4,2,1]
Output: 6
Explanation:
节点 0 与节点 3 为孪生节点，节点 1 与节点 2 为孪生节点。它们的孪生和均为 5+1=6、4+2=6。
链表中不存在其他孪生节点对，因此最大孪生和为 6。
```

#### 示例 2
```
Input: head = [4,2,2,3]
Output: 7
Explanation:
存在以下孪生节点对：
- 节点 0 与节点 3，孪生和为 4 + 3 = 7；
- 节点 1 与节点 2，孪生和为 2 + 2 = 4。
最大孪生和为 max(7, 4) = 7。
```

#### 示例 3
```
Input: head = [1,100000]
Output: 100001
Explanation:
链表中只有一对孪生节点，孪生和为 1 + 100000 = 100001。
```

---

### 约束条件

- 链表中的节点数为偶数，范围为 `[2, 10^5]`。
- `1 <= Node.val <= 10^5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把链表看成一排数字**，先把所有节点的值存进一个普通的 Python 列表 `arr`（相当于把链表“拍照”），然后按题目定义的「孪生」关系两两相加，取最大值。

- **数据结构类比**：把链表的每个节点想象成一本字典里的词条，`arr` 就像把整本字典的所有词条抄到纸上，方便随时查找第 `i` 条和第 `n‑1‑i` 条。
- **正确性**：因为我们把所有值完整记录下来，随后使用题目给出的公式 `twin(i) = n‑1‑i`，必然会遍历到每一对孪生节点，得到的最大和一定是答案。
- **时间/空间分析**：  
  - 把链表搬到数组需要遍历一次链表，时间是 `O(n)`。  
  - 再用两层循环去计算每一对的和：外层遍历 `i = 0 … n/2‑1`，内层去链表里找第 `n‑1‑i` 个节点（需要再次从头遍历），这一步的时间是 `O(n)`，于是总时间是 `O(n²)`。  
  - 额外空间用了一个长度为 `n` 的数组，空间复杂度是 `O(n)`。  
  - 大白话解释：`O(n²)` 就像“先跑完一次马拉松（`n` 步），再在每一步都回头跑一次马拉松（再 `n` 步）”，所以总步数是 `n × n`。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def pairSum_bruteforce(head: ListNode) -> int:
    # 1️⃣ 把链表所有值搬到数组里
    vals = []
    cur = head
    while cur:
        vals.append(cur.val)          # 记录当前节点的数值
        cur = cur.next

    n = len(vals)                     # 链表长度（保证是偶数）
    max_sum = 0

    # 2️⃣ 暴力枚举每一对孪生节点
    for i in range(n // 2):
        # 第 i 个节点的孪生节点是第 n-1-i 个
        twin_sum = vals[i] + vals[n - 1 - i]
        if twin_sum > max_sum:
            max_sum = twin_sum        # 维护最大和值

    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 第一次遍历链表是 `O(n)`，随后每一次求孪生和都要再遍历一次链表（最坏情况 `O(n)`），共 `n/2` 次，乘起来就是 `O(n²)`。
- **空间复杂度**：`O(n)`  
  - 需要额外的数组来保存所有节点的值，长度等于链表长度 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次寻找孪生节点都要从链表头重新遍历**。如果我们能够让两端的指针同时前进，就能把每对孪生节点的和一次算完，时间降到线性 `O(n)`。

实现思路分三步：

1. **用快慢指针把链表分成前后两段**  
   - 快指针每次走两步，慢指针每次走一步。当快指针走到末尾时，慢指针恰好停在链表中点（即前半段的最后一个节点）。这一步只需要一次遍历，时间 `O(n)`，空间 `O(1)`。

2. **把后半段链表** **原地翻转**  
   - 翻转后，后半段的顺序变成原来从尾到头的顺序。这样，前半段的第 `i` 个节点正好对应翻转后后半段的第 `i` 个节点——正是题目要求的「孪生」关系。  
   - 翻转只需要遍历一次后半段，仍是 `O(n)` 时间，且不额外使用数组，只用几个指针，空间 `O(1)`。

3. **双指针同步遍历两段，计算最大孪生和**  
   - 设 `p1` 指向前半段头，`p2` 指向翻转后后半段头。每次把 `p1.val + p2.val` 与当前最大值比较，然后同时向前移动 `p1`、`p2`。遍历结束后得到答案。  

4. **可选：恢复链表原状**（面试中常被要求保持原链表不变）  
   - 再把后半段翻转回来，恢复原来的顺序。恢复的过程和步骤 2 完全相同。

> **关键点解释**  
> - **快慢指针**：把链表比作一条路，快车一次跑两段路，慢车一次跑一段路。快车到达终点时，慢车正好跑到中点。  
> - **原地翻转**：把链表的指针方向全部反过来，就像把一串珠子倒过来挂在另一根绳子上。这样，原来的尾巴变成了新的头，方便从头开始遍历。  
> - **双指针同步**：两个人分别站在链表的前后两端，步伐相同地向中间走，每走一步就把两人的身高相加，记录最高的那一次——这正是「最大孪生和」。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def pairSum(head: ListNode) -> int:
    """
    返回链表中所有孪生节点和的最大值
    思路：快慢指针定位中点 → 翻转后半段 → 双指针计算 →（可选）恢复链表
    """

    # ---------- 1. 快慢指针找到中点 ----------
    slow = fast = head
    while fast and fast.next:          # fast 每次走两步，slow 每次走一步
        slow = slow.next
        fast = fast.next.next
    # 此时 slow 指向后半段的第一个节点（中点）

    # ---------- 2. 翻转后半段 ----------
    prev = None
    cur = slow
    while cur:
        nxt = cur.next                 # 暂存后继节点
        cur.next = prev                # 翻转指针方向
        prev = cur                     # prev 向前移动
        cur = nxt                      # cur 继续向后遍历
    # 翻转结束后，prev 是翻转后链表的头（原链表的尾部）

    # ---------- 3. 双指针遍历计算最大孪生和 ----------
    p1, p2 = head, prev
    max_sum = 0
    while p2:                          # p2 会遍历完后半段（长度为 n/2）
        cur_sum = p1.val + p2.val
        if cur_sum > max_sum:
            max_sum = cur_sum
        p1 = p1.next
        p2 = p2.next

    # ---------- 4.（可选）恢复原链表 ----------
    # 再把后半段翻转回来，使整个链表保持原样
    cur = prev
    prev = None
    while cur:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    # 此时 prev 又指向原来的中点，链表已恢复

    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 快慢指针一次遍历定位中点 `O(n)`。  
  - 翻转后半段、双指针遍历、再翻转回来每步都是线性遍历，累计仍是 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，**每个节点只看了常数次**，速度快了很多。

- **空间复杂度**：`O(1)`  
  - 只用了几个指针变量（`slow、fast、prev、cur、p1、p2`），没有额外的与 `n` 成正比的存储空间。  
  - 用“大白话”说就是：“我们只在手里拿了几根小棍子（指针），没有额外搬运任何东西”。

---

## 心得

- **核心技巧**：**快慢指针 + 原地翻转 + 双指针同步遍历**。这套组合在很多「前后对应」的链表题目里都是「万能钥匙」。
- **适用的题型**（类似思路）  
  1. *Palindrome Linked List*（判断链表是否回文）——先找中点、翻转后半段、逐节点比较。  
  2. *Reorder List*（重新排列链表）——同样先找中点、翻转后半段、交叉合并。  
  3. *Add Two Numbers II*（从高位开始相加）——先把两链表翻转，再像普通加法那样遍历。
- **一句话总结解题钥匙**：**让「左」和「右」的指针同步前进，配合一次翻转即可一次遍历得到所有孪生和**。

---

## 反思

- **第一反应**：看到「孪生」这个词，我第一时间想到「把链表拆成两半，前后对应」——于是想到把链表转成数组再配对。  
- **最容易踩的坑**  
  - **忘记恢复链表**：有的面试会检查你是否破坏了原结构，忘记翻转回来会导致后续代码出错。  
  - **指针移动顺序错误**：在翻转或双指针遍历时，先改指针再取 `next` 会导致链表断裂。  
  - **边界条件**：链表长度最小是 2，必须确保快慢指针循环结束后 `slow` 正好指向后半段的首节点。  
- **下次遇到同类题的第一步**：**先用快慢指针定位中点**——定位好后，后面的「翻转」与「同步遍历」思路自然浮现。