# #1669. 在链表之间合并 / Merge In Between Linked Lists

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/merge-in-between-linked-lists/)

---

## 题目（英文原版）

**Description**

You are given two linked lists: list1 and list2 of sizes n and m respectively.
Remove list1's nodes from the ath node to the bth node, and put list2 in their place.
The blue edges and nodes in the following figure indicate the result:
Build the result list and return its head.

**Examples**

**Example 1:**

```
Input: list1 = [10,1,13,6,9,5], a = 3, b = 4, list2 = [1000000,1000001,1000002]
Output: [10,1,13,1000000,1000001,1000002,5]
Explanation: We remove the nodes 3 and 4 and put the entire list2 in their place. The blue edges and nodes in the above figure indicate the result.
```

**Example 2:**

```
Input: list1 = [0,1,2,3,4,5,6], a = 2, b = 5, list2 = [1000000,1000001,1000002,1000003,1000004]
Output: [0,1,1000000,1000001,1000002,1000003,1000004,6]
Explanation: The blue edges and nodes in the above figure indicate the result.
```

**Constraints**

- 3 <= list1.length <= 104
- 1 <= a <= b < list1.length - 1
- 1 <= list2.length <= 104

---

## 题目（中文翻译）

给定两个链表（linked list）：`list1` 和 `list2`，长度分别为 `n` 和 `m`。请删除 `list1` 中第 `a` 个节点到第 `b` 个节点（含）之间的所有节点，并将整条 `list2` 插入到被删除的位置。构造得到的结果链表并返回其头节点（head）。

下面的示意图中，用蓝色的边和节点标记了合并后的结果。

## 示例

### 示例 1
**输入**  
`list1 = [10,1,13,6,9,5]`，`a = 3`，`b = 4`，`list2 = [1000000,1000001,1000002]`

**输出**  
`[10,1,13,1000000,1000001,1000002,5]`

**解释**  
我们删除了第 3、4 个节点（值为 6 和 9），并把整个 `list2` 插入到它们的位置。上图中用蓝色的边和节点展示了合并后的链表。

### 示例 2
**输入**  
`list1 = [0,1,2,3,4,5,6]`，`a = 2`，`b = 5`，`list2 = [1000000,1000001,1000002,1000003,1000004]`

**输出**  
`[0,1,1000000,1000001,1000002,1000003,1000004,6]`

**解释**  
同样地，删除了 `list1` 中第 2 到第 5 个节点（值为 2、3、4、5），并将 `list2` 完整插入。蓝色的边和节点在上图中标示了最终的链表结构。

## 约束条件
- `3 <= list1.length <= 10^4`
- `1 <= a <= b < list1.length - 1`
- `1 <= list2.length <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是 **一次遍历** 完成所有“拆、接”操作。  
- 先在 `list1` 中找到第 `a‑1` 个节点（记作 `preA`），它是要保留下来的左侧边界。  
- 再找到第 `b+1` 个节点（记作 `postB`），它是要保留下来的右侧边界。  
- 把 `preA.next` 指向 `list2` 的头结点 `head2`，把 `list2` 的最后一个节点的 `next` 指向 `postB`。  

可以把链表想象成 **火车**，每个节点是车厢，`next` 是车厢之间的连接杆。  
- 要把 `a~b` 这段车厢拆下来，只需要把 `preA`（左侧的车厢）和 `postB`（右侧的车厢）用新的连接杆分别和 `list2`（另一列火车）首尾相连。  

**为什么正确**  
- `preA` 之前的所有节点保持不变。  
- `list2` 完全插入到 `preA` 与 `postB` 之间。  
- `postB` 之后的节点同样保持不变。  
因此得到的链表正是题目要求的结果。

**时间/空间复杂度**  
- 我们只需要 **一次遍历** `list1` 找到 `preA` 与 `postB`，以及一次遍历 `list2` 找到它的尾节点。  
- 所以时间复杂度是 `O(n + m)`（`n` 为 `list1` 长度，`m` 为 `list2` 长度）。  
- 只使用了几个指针变量，额外空间为 `O(1)`，即常数级空间。

> 大白话解释：  
> - `O(n+m)` 就是“遍历每条链表一次”，不会出现指数级或平方级的增长。  
> - `O(1)` 表示我们不需要额外的数组、哈希表之类的“大箱子”，只用几根指针就够了。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点存的数值
        self.next = next        # 指向下一个节点的指针

class Solution:
    def mergeInBetween(self, list1: ListNode, a: int, b: int, list2: ListNode) -> ListNode:
        """
        将 list1 中第 a~b（含）个节点删除，并把 list2 整体插入到这里。
        """
        # ---------- 1. 找到 preA (第 a-1 个节点) ----------
        cur = list1
        idx = 0
        while idx < a - 1:          # 循环到第 a-1 个位置
            cur = cur.next
            idx += 1
        preA = cur                  # 记录左侧边界

        # ---------- 2. 找到 postB (第 b+1 个节点) ----------
        cur = list1
        idx = 0
        while idx < b + 1:          # 循环到第 b+1 个位置
            cur = cur.next
            idx += 1
        postB = cur                 # 记录右侧边界

        # ---------- 3. 把 preA 接到 list2 ----------
        preA.next = list2           # preA 的后继直接指向 list2 头

        # ---------- 4. 找到 list2 的尾节点 ----------
        tail2 = list2
        while tail2.next:           # 一直往后走，直到最后一个节点
            tail2 = tail2.next

        # ---------- 5. 把 list2 尾接到 postB ----------
        tail2.next = postB          # 完成插入

        return list1                # 返回新的头结点
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - `n` 是 `list1` 长度，`m` 是 `list2` 长度。我们分别遍历它们一次，所需的操作数随输入规模线性增长。  
- **空间复杂度**：`O(1)`  
  - 只用了几个指针变量（`preA`, `postB`, `cur`, `tail2`），不随输入大小增长。

---  

### 2. 最优解  

#### 思路  
其实上面的“暴力”已经是最优的了，因为链表的本质是 **只能顺序访问**，不可能像数组那样直接跳到第 `k` 个元素。  
唯一可以改进的地方是 **合并两个遍历**：  

1. 在一次遍历 `list1` 的过程中，同时记录 `preA`（第 `a‑1`）和 `postB`（第 `b+1`）的位置。  
2. 再遍历一次 `list2` 找到它的尾节点。  

这样我们把 **两次遍历 `list1`** 合并为 **一次遍历**，时间仍然是 `O(n + m)`，但常数因子更小。  

核心概念仍然是 **指针**（`next`）的重新连接，只是更“省事”。  

> **类比**：  
> 把 `list1` 看成一条长路，`a`、`b` 是路上的两个里程碑。我们一次开车沿路走，顺手记下这两个里程碑的前后路口，然后把 `list2`（另一条支路）接进来。  

#### 代码（Python）

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeInBetween(self, list1: ListNode, a: int, b: int, list2: ListNode) -> ListNode:
        """
        单遍历找 preA 与 postB，再把 list2 接进去。
        """
        # 1. 同时找 preA (a-1) 和 postB (b+1)
        cur = list1
        idx = 0
        preA = postB = None

        while cur:                     # 只遍历一次 list1
            if idx == a - 1:
                preA = cur            # 记录左侧边界
            if idx == b + 1:
                postB = cur           # 记录右侧边界
                break                # 已经找齐，可提前结束循环
            cur = cur.next
            idx += 1

        # 2. 把 preA 接到 list2
        preA.next = list2

        # 3. 找到 list2 的尾节点
        tail2 = list2
        while tail2.next:
            tail2 = tail2.next

        # 4. 把 list2 的尾接到 postB
        tail2.next = postB

        return list1
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 只遍历一次 `list1`（找到 `preA` 与 `postB`），再遍历一次 `list2`（找到尾节点），整体仍是线性时间。  
  - 与前面的暴力解相比，省掉了一次对 `list1` 的遍历，常数因子更小。  

- **空间复杂度**：`O(1)`  
  - 仍然只使用常数个指针变量。

---  

## 心得  

- **核心技巧**：**链表的指针重连**（重新安排 `next` 指向），以及**一次遍历找到多个目标节点**。  
- **适用的题型**：  
  1. **删除链表区间**（如 “Remove Nth Node From End of List”）  
  2. **在链表指定位置插入子链表**（如 “Insert into a Sorted Circular Linked List”）  
  3. **链表的合并或拼接**（如 “Merge Two Sorted Lists”）  
- **一句话总结**：**把链表当作火车，用几根指针把车厢拆下来再重新拼接**，不需要额外空间，只要弄清楚“左边界”和“右边界”。  

## 反思  

- **第一反应**：先把 `list1` 的 `a‑1`、`b+1` 两个位置找出来，再把 `list2` 接进去——这正是最自然的思路。  
- **最容易踩的坑**：  
  - **索引从 0 开始** 与题目中 **从 1 开始** 的差异，需要在代码里做 `a‑1`、`b+1` 的转换。  
  - **a 与 b 之间可能只有一个节点**（如 `a == b`），仍然要正确处理 `preA.next` 与 `postB`。  
  - **list2 可能只有一个节点**，遍历找尾节点时要注意 `while tail2.next` 防止空指针错误。  
- **下次遇到同类题**，第一步应该先**定位要修改的前后边界节点**（左侧前驱、右侧后继），随后**只动指针**完成拼接，避免在链表上做不必要的复制或额外遍历。