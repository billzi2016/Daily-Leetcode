# #2181. 合并零之间的节点 / Merge Nodes in Between Zeros

> 难度：中等 · 标签：Linked List、Simulation · [LeetCode 链接](https://leetcode.com/problems/merge-nodes-in-between-zeros/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list, which contains a series of integers separated by 0's. The beginning and end of the linked list will have Node.val == 0.
For every two consecutive 0's, merge all the nodes lying in between them into a single node whose value is the sum of all the merged nodes. The modified list should not contain any 0's.
Return the head of the modified linked list.

**Examples**

**Example 1:**

```
Input: head = [0,3,1,0,4,5,2,0]
Output: [4,11]
Explanation: 
The above figure represents the given linked list. The modified list contains
- The sum of the nodes marked in green: 3 + 1 = 4.
- The sum of the nodes marked in red: 4 + 5 + 2 = 11.
```

**Example 2:**

```
Input: head = [0,1,0,3,0,2,2,0]
Output: [1,3,4]
Explanation: 
The above figure represents the given linked list. The modified list contains
- The sum of the nodes marked in green: 1 = 1.
- The sum of the nodes marked in red: 3 = 3.
- The sum of the nodes marked in yellow: 2 + 2 = 4.
```

**Constraints**

- The number of nodes in the list is in the range [3, 2 * 105].
- 0 <= Node.val <= 1000
- There are no two consecutive nodes with Node.val == 0.
- The beginning and end of the linked list have Node.val == 0.

---

## 题目（中文翻译）

你得到一个链表（linked list）的头结点 `head`，该链表由一系列整数构成，且这些整数之间由值为 `0` 的节点分隔。链表的起始节点和结束节点的 `Node.val` 均为 `0`。

对于每两个相邻的 `0` 节点，将它们之间的所有节点合并为一个节点，新的节点值为这些被合并节点值的总和。修改后的链表中不应再出现任何 `0` 节点。

返回修改后链表的头结点。

## 示例

### 示例 1  
**输入**: `head = [0,3,1,0,4,5,2,0]`  
**输出**: `[4,11]`  
**解释**:  
上图表示给定的链表。修改后的链表包含  
- 绿色标记节点的和: `3 + 1 = 4`  
- 红色标记节点的和: `4 + 5 + 2 = 11`

### 示例 2  
**输入**: `head = [0,1,0,3,0,2,2,0]`  
**输出**: `[1,3,4]`  
**解释**:  
上图表示给定的链表。修改后的链表包含  
- 绿色标记节点的和: `1 = 1`  
- 红色标记节点的和: `3 = 3`  
- 黄色标记节点的和: `2 + 2 = 4`

## 约束条件
- 链表中节点的数量在 `[3, 2 * 10^5]` 区间内。  
- `0 <= Node.val <= 1000`  
- 不会出现两个相邻节点的 `Node.val` 均为 `0` 的情况。  
- 链表的起始节点和结束节点的 `Node.val` 均为 `0`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把链表所有节点的值先读到一个 Python 列表 `arr` 中，再按照“两个相邻的 0 之间求和” 的规则把 `arr` 重新组织成结果列表，最后再把结果列表转回链表返回。

- **读取链表**：从 `head` 开始遍历，每访问一个节点就把 `node.val` 放进 `arr`。这一步相当于把链表“拍照”，把所有信息都记下来。
- **分段求和**：用一个变量 `cur_sum` 累加非零值，遇到 `0` 时把 `cur_sum`（如果不为 0）加入结果列表 `res`，然后把 `cur_sum` 重新置为 0。这里的 `0` 就像字典里的分隔符，告诉我们上一段已经结束。
- **生成新链表**：把 `res` 中的每个数创建成一个新的 `ListNode`，按顺序用 `next` 串起来，形成最终链表。

> **为什么正确**  
> 题目保证链表的首尾都是 `0`，且不存在相邻的两个 `0`，所以每一次“遇到 `0`”必然对应一次完整的区间求和。把所有区间的和依次写入新链表，正好满足“合并相邻 0 之间的节点”。

> **复杂度大白话**  
> - **时间复杂度 O(n)**：我们需要遍历整条链表一次（`n` 是链表节点数），每个节点只看一次。  
> - **空间复杂度 O(k)**：`k` 是合并后节点的数量（即区间个数），最坏情况下 `k ≈ n/2`，所以需要额外的列表来保存这些和。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeNodes_bruteforce(head: ListNode) -> ListNode:
    """暴力解：先把链表值放到数组，再重新构造链表"""
    # 1️⃣ 把链表全部读进数组
    vals = []
    cur = head
    while cur:
        vals.append(cur.val)   # 把每个节点的值记下来
        cur = cur.next

    # 2️⃣ 按 0 分段求和，得到结果数组
    sums = []          # 用来存每段的和
    cur_sum = 0
    for v in vals:
        if v == 0:                     # 碰到 0，说明一段结束
            if cur_sum != 0:           # 第一个 0 前的 cur_sum 为 0，跳过
                sums.append(cur_sum)   # 把本段的和保存
            cur_sum = 0                # 重置，准备下一段
        else:
            cur_sum += v                # 累加非零值

    # 3️⃣ 根据 sums 创建新链表
    dummy = ListNode(0)   # 哑结点，帮助我们省去判断 head 是否为空的代码
    tail = dummy
    for s in sums:
        tail.next = ListNode(s)   # 把和作为新节点接在后面
        tail = tail.next          # tail 始终指向链表的最后一个节点

    return dummy.next   # 去掉哑结点，返回真实的头结点
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们遍历链表一次（`n` 次），随后遍历一次数组（也是 `n` 次），总共是线性时间。

- **空间复杂度**：`O(k)`（`k` 为合并后节点数，最坏 `≈ n/2`）  
  解释：额外用了 `vals`（存原链表所有值）和 `sums`（存每段的和）两个列表，空间随输入大小线性增长。

---

### 2. 最优解

#### 思路  

暴力解已经是 **O(n)** 的时间，但它用了额外的数组。我们可以直接在原链表上完成“合并”，只使用常数级别的额外空间。

**关键观察**  
- 合并的结果只需要保留每段和对应的一个节点，这个节点恰好是 **区间左侧的 0**（即该段的起始 0）。
- 当遍历到右侧的 0 时，左侧的 0 节点的 `val` 已经累计了该段的全部和；随后可以把左侧 0 的 `next` 指向右侧 0 的 `next`，相当于“删除”中间的所有节点。

**双指针技巧**  
- `write` 指针指向当前正在写入合并结果的节点（即上一个 0）。
- `cur` 指针遍历整个链表，负责累计和。
- 当 `cur.val == 0`（遇到右侧的 0）时，说明一段结束：  
  1. `write.val = segment_sum`（把累计的和写进左侧的 0 节点）  
  2. `write.next = cur.next`（把左侧 0 的 `next` 直接指向右侧 0 之后的节点）  
  3. 把 `write` 移到 `cur.next`（下一个段的左侧 0）  
  4. 重置 `segment_sum = 0`，继续遍历。

这样只遍历一次链表，且不需要额外的数组。

> **为什么正确**  
> - 每次累计的 `segment_sum` 正好是两个相邻 0 之间所有节点的和。  
> - 当右侧 0 被发现时，我们立刻把左侧 0 改写为这段和的节点，并把它的 `next` 跳过中间的所有节点，等价于“把中间节点删掉”。  
> - 最终链表只保留了每段的和节点，且顺序不变。

> **大白话的复杂度解释**  
> - **时间 O(n)**：只走了一遍链表，`n` 是节点总数。  
> - **空间 O(1)**：只用了几个指针变量（`write、cur、segment_sum`），不随输入规模增长。

#### 代码（Python）

```python
def mergeNodes_optimal(head: ListNode) -> ListNode:
    """
    最优解：一次遍历原链表，原地合并区间，空间复杂度 O(1)
    """
    write = head          # write 指向当前段的左侧 0
    cur = head.next       # 从左侧 0 的下一个节点开始遍历
    segment_sum = 0

    while cur:            # 遍历到链表末尾（末尾必为 0）
        if cur.val == 0:          # 遇到右侧的 0，说明一段结束
            write.val = segment_sum   # 把累计的和写进左侧的 0
            write.next = cur.next     # 跳过中间的节点，直接指向右侧 0 之后的节点
            write = write.next        # write 移动到下一段的左侧 0
            segment_sum = 0           # 为下一段重新累计
        else:
            segment_sum += cur.val    # 不是 0，继续累加
        cur = cur.next                # 向前走一步

    return head   # head 已经被改写为结果链表的第一个和节点
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次链表，`n` 是节点总数。相比暴力解，没有额外的遍历或复制步骤。
- **空间复杂度**：`O(1)` — 只使用了常数个指针变量，不随链表长度增长。

---

## 心得

- **核心技巧**：**双指针原地修改链表**（一个指针累计求和，另一个指针负责写入结果并跳过无用节点）。
- **适用题型**  
  1. “在链表中删除满足某种条件的连续子段”——如 “删除所有值为 0 的节点”。  
  2. “链表分段统计”——如 “把相同值的连续段压缩为计数节点”。  
  3. “链表两指针合并/分割”——如 “分割链表为奇数位和偶数位两条链表”。

- **一句话总结**：**遇到分界标记（这里是 0）时，用左侧的标记节点存储累计结果并直接跳过中间节点，实现 O(1) 额外空间的原地合并**。

---

## 反思

- **第一反应**：看到“0 分割”“合并区间”，我首先想到把所有值搬到数组里再处理——最直观但会占用额外空间。
- **最容易踩的坑**  
  - 忘记把最后一个合并节点的 `next` 指向 `None`（或 `cur.next`），导致链表出现循环或多余节点。  
  - 误把首尾的 0 也算进结果，导致输出中出现不应有的 0。  
  - 在累计和时忘记在遇到右侧 0 时把 `segment_sum` 清零，导致后面的段累计错误。
- **下次第一步**：看到“两个特殊标记之间的操作”，立刻在脑中构建“双指针：一个负责遍历累计，另一个负责写入并跳过”，判断是否能 **原地** 完成，若可以则直接实现 O(1) 空间解。