# #725. 分割链表为 K 部分 / Split Linked List in Parts

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/split-linked-list-in-parts/)

---

## 题目（英文原版）

**Description**

Given the head of a singly linked list and an integer k, split the linked list into k consecutive linked list parts.
The length of each part should be as equal as possible: no two parts should have a size differing by more than one. This may lead to some parts being null.
The parts should be in the order of occurrence in the input list, and parts occurring earlier should always have a size greater than or equal to parts occurring later.
Return an array of the k parts.

**Examples**

**Example 1:**

```
Input: head = [1,2,3], k = 5
Output: [[1],[2],[3],[],[]]
Explanation:
The first element output[0] has output[0].val = 1, output[0].next = null.
The last element output[4] is null, but its string representation as a ListNode is [].
```

**Example 2:**

```
Input: head = [1,2,3,4,5,6,7,8,9,10], k = 3
Output: [[1,2,3,4],[5,6,7],[8,9,10]]
Explanation:
The input has been split into consecutive parts with size difference at most 1, and earlier parts are a larger size than the later parts.
```

**Constraints**

- The number of nodes in the list is in the range [0, 1000].
- 0 <= Node.val <= 1000
- 1 <= k <= 50

---

## 题目（中文翻译）

给定一个单向链表（singly linked list）的头节点 `head` 和一个整数 `k`，将该链表拆分成 `k` 段连续的链表部分（consecutive linked list parts）。  
每一段的长度应尽可能相等：任意两段的大小之差不能超过 1。这可能导致某些段为 `null`（空）。  
各段必须保持在原链表中的出现顺序，且出现较早的段大小必须大于或等于后面的段。  
返回一个长度为 `k` 的数组，数组中的每个元素对应拆分后得到的链表段。

**示例 1**  
**示例 2**  

**约束条件**  

- 链表中的节点数在 `[0, 1000]` 区间内。  
- `0 <= Node.val <= 1000`  
- `1 <= k <= 50`  

---

### 示例

#### 示例 1
**输入**: `head = [1,2,3]`, `k = 5`  
**输出**: `[[1],[2],[3],[],[]]`  
**解释**:  
第一个元素 `output[0]` 的 `val` 为 `1`，`next` 为 `null`。  
最后一个元素 `output[4]` 为 `null`，但其在 `ListNode` 中的字符串表示为 `[]`。

#### 示例 2
**输入**: `head = [1,2,3,4,5,6,7,8,9,10]`, `k = 3`  
**输出**: `[[1,2,3,4],[5,6,7],[8,9,10]]`  
**解释**:  
输入被拆分为连续的几段，每段的大小差不超过 `1`，且前面的段比后面的段更大。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **先遍历一遍链表**，算出链表的总长度 `N`。  
2. 对于每一个要切的 part（共 `k` 个），**从头再走一次**，数出该 part 应该有多少节点，然后把这些节点“摘下来”。  

> **类比**：把链表想象成一本书的章节。我们先数出总页数 `N`，然后每次想要拿出一段章节时，都从书的开头重新翻起，数到需要的页数再撕下来。显然，这样会反复翻同一页，效率不高。

**为什么正确**  
- 我们每次都严格按照“前面的 part 大于或等于后面的 part”以及“相邻两段大小相差不超过 1”来决定每段的长度。只要把链表按这些长度顺序切开，得到的就是题目要求的答案。

**时间/空间复杂度**  
- **时间**：我们先遍历一次 O(N) 统计长度，然后对每个 part 再遍历一次，最坏情况是 `k` 次遍历每次都走 `N/k`（近似），总计 `O(N * k)`。如果 `k` 接近 `N`（比如 `N=1000, k=1000`），时间会达到 O(N²)≈10⁶ 步，仍在可接受范围，但不是最优的。  
- **空间**：只使用了常数级别的额外变量（计数器、指针），所以是 O(1)。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def splitListToParts_bruteforce(head: ListNode, k: int):
    # ---------- 第一步：统计链表总长度 ----------
    length = 0
    cur = head
    while cur:
        length += 1
        cur = cur.next          # 走完链表一次，得到 N

    # ---------- 第二步：逐段切割 ----------
    result = [None] * k          # 预先准备 k 个返回位置
    cur = head                   # 重新指向链表头部

    for i in range(k):
        # 计算第 i 段应该有多少节点
        # 这里直接用“从头再数”——暴力做法
        part_len = 0
        temp = cur
        while temp and part_len < (length // k + (1 if i < length % k else 0)):
            part_len += 1
            temp = temp.next

        # 如果当前已经没有节点了，后面的全部都是 None
        if not cur:
            result[i] = None
            continue

        # ---------- 把这一段摘下来 ----------
        result[i] = cur          # 记录本段的头结点
        # 移动 cur 指针，使其指向本段最后一个节点
        for _ in range(part_len - 1):
            cur = cur.next
        # 断开本段与后续的连接
        nxt = cur.next if cur else None
        if cur:
            cur.next = None
        cur = nxt                # 为下一段准备

    return result
```

#### 复杂度  

- **时间复杂度**：`O(N * k)` —— 需要对每一段都重新遍历链表，最坏情况下相当于 `N` 与 `k` 的乘积。  
  - **大白话**：如果链表有 1000 个节点，`k` 也是 1000，那么我们大约要走 1 000 000 步，明显可以更快。  
- **空间复杂度**：`O(1)` —— 只用了几个指针和计数器，和链表本身的大小无关。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复遍历链表是主要的性能瓶颈**。我们只需要遍历一次链表，就能把每段的长度算好并直接切割。关键在于：

1. **先算出总长度 `N`**（一次遍历）。  
2. 根据整数除法和取余的性质，**每段的基础长度** 为 `base = N // k`，**前 `extra = N % k` 段** 需要再多一个节点。  
   - 这就像把 `N` 块糖果平均放进 `k` 只碗里，先每只碗放 `base` 块，剩下的 `extra` 块再依次放进前面的碗。  
3. 再次遍历链表，这一次**按顺序一次性切割**：  
   - 对第 `i` 段，先记录它的头结点 `head_i`，然后走 `size_i = base + (1 if i < extra else 0)` 步，走完后把当前节点的 `next` 设为 `None`，断开与后面的连接。  
   - 这样每个节点只被访问一次，整体是 O(N)。  

**核心算法**：**一次遍历 + 计算分配**（不需要额外的数据结构）。  
- **前缀和**的思想在这里体现在“先算总和（长度），再均匀分配”。  
- **双指针**：`cur` 用来遍历链表，`prev`（或直接用 `cur`）帮助我们在恰当的位置断链。

#### 代码（Python）

```python
def splitListToParts(head: ListNode, k: int):
    # ---------- 第一步：统计总长度 ----------
    length = 0
    cur = head
    while cur:
        length += 1
        cur = cur.next

    # ---------- 第二步：计算每段的长度 ----------
    base = length // k               # 每段最少的节点数
    extra = length % k               # 前 extra 段需要多一个

    # ---------- 第三步：一次遍历完成切割 ----------
    parts = [None] * k               # 预留 k 个返回位置
    cur = head                       # 重新指向链表头部

    for i in range(k):
        # 记录本段的起始节点
        parts[i] = cur
        # 计算本段实际需要的节点数
        part_len = base + (1 if i < extra else 0)

        # 在本段内部走 part_len-1 步，使 cur 停在本段最后一个节点
        for _ in range(part_len - 1):
            if cur:
                cur = cur.next

        # 如果 cur 仍然非空，说明本段还有节点，需要断开
        if cur:
            nxt = cur.next            # 保存下一段的起点
            cur.next = None           # 把本段最后一个节点的 next 设为 None
            cur = nxt                 # cur 移动到下一段的起点
        # 若 cur 已经是 None，后面的 parts[i] 会自动保持为 None

    return parts
```

#### 复杂度  

- **时间复杂度**：`O(N)` —— 只遍历链表两次（一次算长度，一次切割），每个节点恰好被访问一次。  
  - **大白话**：链表有 1000 个节点，就走 1000 步，几乎是最快能做到的。  
- **空间复杂度**：`O(k)` —— 需要存放返回的 `k` 个头指针（题目要求的返回值），除此之外只用了常数级别的指针。  

---

## 心得  

- **核心技巧**：先统计总量，再用“整数除法 + 余数”均匀分配，是处理“尽量平均划分”类问题的常用套路。  
- **适用的题型**：  
  1. **分配资源**：比如把 `N` 件物品分到 `k` 个人手中，使差值最小（LeetCode 1103 `分配糖果`）。  
  2. **数组/链表均分**：如把数组切成 `k` 段，每段长度相差不超过 1（LeetCode 1470 `重新排列数组` 的变体）。  
  3. **工作负载均衡**：把任务列表均匀分配到多台机器（面试常见的“把任务均匀分配”）。  
- **一句话总结**：**“先算总量，再用除法+余数决定前几段多一个”，一次遍历即可完成均匀切分。**  

---

## 反思  

- **第一反应**：看到“把链表分成 k 段，尽量相等”，自然想到先求长度，再均匀分配。  
- **最容易踩的坑**：  
  - **空链表**：`head` 为 `None` 时，仍需要返回 `k` 个 `None`。  
  - **k 大于长度**：会出现很多空段，必须确保循环中 `cur` 为 `None` 时不再访问 `cur.next`。  
  - **断链时忘记保存 `next`**：直接把 `cur.next = None` 之后再 `cur = cur.next` 会导致 `cur` 变成 `None`，后面的节点全部丢失。  
- **下次遇到同类题**：第一步先 **“求总量 + 用除法/余数划分”**，再 **“一遍遍历完成切割/分配”**，避免重复遍历。