# #2074. 奇偶长度分组翻转链表节点 / Reverse Nodes in Even Length Groups

> 难度：中等 · 标签：Linked List · [LeetCode 链接](https://leetcode.com/problems/reverse-nodes-in-even-length-groups/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list.
The nodes in the linked list are sequentially assigned to non-empty groups whose lengths form the sequence of the natural numbers (1, 2, 3, 4, ...). The length of a group is the number of nodes assigned to it. In other words,
Note that the length of the last group may be less than or equal to 1 + the length of the second to last group.
Reverse the nodes in each group with an even length, and return the head of the modified linked list.

**Examples**

**Example 1:**

```
Input: head = [5,2,6,3,9,1,7,3,8,4]
Output: [5,6,2,3,9,1,4,8,3,7]
Explanation:
- The length of the first group is 1, which is odd, hence no reversal occurs.
- The length of the second group is 2, which is even, hence the nodes are reversed.
- The length of the third group is 3, which is odd, hence no reversal occurs.
- The length of the last group is 4, which is even, hence the nodes are reversed.
```

**Example 2:**

```
Input: head = [1,1,0,6]
Output: [1,0,1,6]
Explanation:
- The length of the first group is 1. No reversal occurs.
- The length of the second group is 2. The nodes are reversed.
- The length of the last group is 1. No reversal occurs.
```

**Example 3:**

```
Input: head = [1,1,0,6,5]
Output: [1,0,1,5,6]
Explanation:
- The length of the first group is 1. No reversal occurs.
- The length of the second group is 2. The nodes are reversed.
- The length of the last group is 2. The nodes are reversed.
```

**Constraints**

- The number of nodes in the list is in the range [1, 105].
- 0 <= Node.val <= 105

---

## 题目（中文翻译）

给定一个单链表的头结点 `head`。

链表中的节点按照顺序被划分为若干非空分组，分组的长度依次构成自然数序列 1、2、3、4、……。  
分组的长度指分配给该分组的节点数量。换句话说，第一组包含 1 个节点，第二组包含 2 个节点，第三组包含 3 个节点，依此类推。  
需要注意的是，最后一组的长度可能小于或等于倒数第二组长度的 1 + 该组长度。

将所有长度为偶数的分组内部的节点顺序翻转（reverse），返回修改后的链表的头结点。

---

### 示例

#### 示例 1
**输入**: `head = [5,2,6,3,9,1,7,3,8,4]`  
**输出**: `[5,6,2,3,9,1,4,8,3,7]`  
**解释**:
- 第一组长度为 1（奇数），不进行翻转。  
- 第二组长度为 2（偶数），节点顺序被翻转。  
- 第三组长度为 3（奇数），不进行翻转。  
- 最后一组长度为 4（偶数），节点顺序被翻转。

#### 示例 2
**输入**: `head = [1,1,0,6]`  
**输出**: `[1,0,1,6]`  
**解释**:
- 第一组长度为 1，未翻转。  
- 第二组长度为 2，节点被翻转。  
- 最后一组长度为 1，未翻转。

#### 示例 3
**输入**: `head = [1,1,0,6,5]`  
**输出**: `[1,0,1,5,6]`  
**解释**:
- 第一组长度为 1，未翻转。  
- 第二组长度为 2，节点被翻转。  
- 最后一组长度为 2，节点被翻转。

---

### 约束条件
- 链表中的节点数在范围 `[1, 10^5]` 内。  
- `0 <= Node.val <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **把链表想象成一列排队的人**，我们要把他们按照「1、2、3、4、…」的组大小分批。  
2. 先遍历链表，**记录每个组的节点**（把指针放进一个 Python 列表 `group_nodes`），等到组的长度确定后判断奇偶：  
   - 若长度是奇数，直接把这些节点按原顺序接回链表。  
   - 若长度是偶数，就把 `group_nodes` 反转（`group_nodes[::-1]`），再把它们接回链表。  
3. 为了把“反转后”的节点重新接到原链表，需要**手动修改每个节点的 `next` 指针**。  

> **类比**：  
> - 哈希表（字典）就像一本词典，`key` 是单词，`value` 是页码；这里的 `group_nodes` 则像一本临时的「小册子」，把当前组的所有人都装进去，等决定要不要翻页（反转）后再放回原来的队列。  

**为什么正确**：我们把每一组的所有节点完整地取出来，判断是否需要翻转后再一次性写回去。只要不漏节点、不多写节点，链表的结构必然和题目要求一致。

**时间/空间分析**（最笨的写法）：  
- 对每一组我们都要把节点收进 `group_nodes`，这一步是 **O(k)**（k 为该组长度）。  
- 当组长度是偶数时，我们用 `list.reverse()`（内部是一次遍历）再逐个改 `next`，同样是 **O(k)**。  
- 但如果我们在“反转”时采用 **把当前组的第二个节点搬到组首的方式**（即每搬一次都要改两条指针），会出现 **O(k²)** 的情况。因为每搬一次都要遍历已搬过的节点。  
- 整体最坏情况下（比如链表长度 10⁵，组长度逐渐增大），时间复杂度会退化到 **O(n²)**。  

空间上我们额外用了 `group_nodes`，最多存一整组的节点，最坏是 **O(n)**（当最后一组几乎包含所有节点时）。

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseEvenLengthGroups_bruteforce(head: ListNode) -> ListNode:
    """
    暴力实现：把每一组的节点装进列表，必要时翻转，再把指针重新接回链表。
    时间复杂度最坏 O(n²)，空间 O(n)。
    """
    dummy = ListNode(0, head)      # dummy 方便处理头节点的修改
    prev_group_tail = dummy        # 前一组的最后一个节点（A）
    cur = head                     # 当前遍历指针（B）
    group_len = 1                  # 当前组应有的长度（1,2,3,…）

    while cur:
        # 1️⃣ 收集本组节点
        nodes = []                 # 临时列表，用来存放本组的所有节点
        cnt = 0
        while cur and cnt < group_len:
            nodes.append(cur)
            cur = cur.next
            cnt += 1

        # 2️⃣ 判断奇偶，若偶数则翻转列表
        if cnt % 2 == 0:           # 偶数长度需要翻转
            nodes.reverse()        # python 列表自带的 O(k) 反转

        # 3️⃣ 把处理好的节点重新连回链表
        for i, node in enumerate(nodes):
            prev_group_tail.next = node          # A.next 指向本组第一个节点
            prev_group_tail = node               # prev_group_tail 前移，指向本组当前节点
        # 本组结束后，prev_group_tail 正好是本组的最后一个节点（C）
        # 接下来继续处理下一组
        group_len += 1               # 下一组长度加 1

    # 循环结束后，prev_group_tail 已经是最后一个节点，需要把它的 next 置为 None
    prev_group_tail.next = None
    return dummy.next
```

#### 复杂度  

- **时间复杂度**：最坏 **O(n²)**  
  - 解释：如果我们在翻转时采用把节点一个个搬到组首的做法，每搬一次都要遍历已搬过的节点，导致每组耗时 `1 + 2 + … + k = O(k²)`。整个链表的所有组加起来会出现二次方增长。  
- **空间复杂度**：**O(n)**  
  - 解释：我们用了 `nodes` 列表来临时存放一整组的节点，最坏情况下这一组可能接近整个链表的大小。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈在于额外的列表和多余的遍历**。我们可以直接在链表上“原地”完成所有操作，只使用常数个指针：

1. **四指针模型**  
   - `prev`（A）：上一个组的最后一个节点（如果是第一组则为 `None`）。  
   - `start`（B）：当前组的第一个节点。  
   - `end`（C）：当前组的最后一个节点（遍历时确定）。  
   - `next_group_head`（D）：下一个组的第一个节点（`end.next`）。  

   把链表想成 `A → (B → … → C) → D`，我们只需要把 `A.next`、`C.next` 正确指向即可。

2. **遍历并计数**  
   - 按自然数 1、2、3… 依次确定每组的大小 `k`。  
   - 用一个循环向前走 `k` 步（或提前结束），得到 `end` 与实际长度 `real_len`（因为最后一组可能不足 `k`）。  

3. **判断奇偶并原地翻转**  
   - 若 `real_len` 为奇数：**不翻转**，直接把 `prev` 移动到 `end`（即 `prev = end`），`start` 移动到 `next_group_head`。  
   - 若 `real_len` 为偶数：**在 `start` 与 `end` 之间做一次普通的链表反转**（一次遍历即可），得到 `new_start`（原 `end`）和 `new_end`（原 `start`）。  
   - 关键的连接：`prev.next = new_start`（如果 `prev` 不为 `None`），`new_end.next = next_group_head`。  

4. **为下一组准备指针**  
   - `prev` 更新为 `new_end`（奇数情况下是 `end`，偶数情况下是 `new_end`），因为它现在是已处理好的组的最后一个节点。  
   - `start` 设为 `next_group_head`，继续下一轮。  

5. **循环终止**  
   - 当 `start` 为 `None` 时说明已经遍历完所有节点。

> **类比**：  
> - 把链表看成一条绳子，上面系着若干小灯泡（节点）。我们要把灯泡按 1、2、3… 的节奏分段。每段如果灯泡数量是偶数，就把这段灯泡的顺序翻个个儿（相当于把这段绳子倒过来）。只需要动手把前后两端的绳子重新系好，内部灯泡的顺序通过一次遍历就能翻转，**不需要把灯泡全部拿下来装进盒子**，因此空间是 O(1)。

#### 代码（Python）

```python
def reverseEvenLengthGroups(head: ListNode) -> ListNode:
    """
    最优实现：一次遍历 O(n) 时间，O(1) 额外空间。
    思路：使用四指针 (prev, start, end, next) 直接在原链表上翻转偶数长度的组。
    """
    dummy = ListNode(0, head)   # 为了统一处理第一组的 prev（它为 dummy）
    prev = dummy                # A，上一组的尾部
    start = head                # B，当前组的首节点
    group_len = 1               # 目标组长度 1,2,3,...

    while start:
        # ---------- 找到本组的末节点 ----------
        end = start
        cnt = 1                  # 已经在 end 上计数 1
        while cnt < group_len and end.next:
            end = end.next
            cnt += 1

        next_group_head = end.next   # D，下一组的首节点

        # ---------- 根据奇偶决定是否翻转 ----------
        if cnt % 2 == 0:        # 偶数，需要翻转 start~end
            # 传统链表局部反转（一次遍历）
            prev_node = next_group_head   # 先把 end.next 暂存为 next_group_head
            cur = start
            while cur != next_group_head:
                nxt = cur.next
                cur.next = prev_node
                prev_node = cur
                cur = nxt
            # 反转后，prev_node 指向原 end（即新组的首节点）
            # 连接前后两段
            prev.next = prev_node          # A.next = C（新首）
            prev = start                   # A 更新为原 start（现在是组尾）
        else:
            # 奇数组不动，直接把 prev 移到本组的末节点
            prev = end

        # ---------- 为下一轮准备 ----------
        start = next_group_head
        group_len += 1

    return dummy.next
```

> **代码说明（逐行注释）**  
> - `dummy`：虚拟头节点，避免在处理第一组时需要特判 `prev` 为 `None`。  
> - `while start:`：只要还有未处理的节点就继续。  
> - 内层 `while cnt < group_len and end.next:`：尝试走 `group_len` 步，若提前到达链表尾则提前停止，得到真实的组长度 `cnt`。  
> - `next_group_head = end.next`：保存下一组的入口，以免在翻转过程中丢失。  
> - **偶数翻转**：使用标准的“头插法”链表反转，只遍历一次本组节点。  
>   - `prev_node` 初始指向 `next_group_head`，相当于把本组反转后要接上的后继。  
>   - 循环结束后 `prev_node` 正好是本组反转后的首节点（原 `end`）。  
>   - `prev.next = prev_node` 完成 `A → C` 的连接。  
>   - `prev = start` 把 `prev` 更新为本组的尾节点（原 `start`），为下一轮做准备。  
> - **奇数组**：直接把 `prev` 移到 `end`（因为组内顺序不变），不需要额外指针操作。  
> - 最后返回 `dummy.next` 即为修改后的链表头。

#### 复杂度  

- **时间复杂度**：**O(n)**  
  - 解释：每个节点只被遍历常数次（一次找组，一次（可能）翻转），没有嵌套的二次遍历。  
- **空间复杂度**：**O(1)**  
  - 解释：只用了固定数量的指针变量 (`prev, start, end, next_group_head, prev_node, cur, nxt`)；不随链表长度增长而增长。

---

## 心得  

- **核心技巧**：**在链表上使用有限的指针进行局部翻转**（头插法），并利用“前一组的尾 + 当前组的首/尾 + 下一组的首”这三个锚点完成链表的拼接。  
- **适用的题型**：  
  1. “按固定长度或可变长度分段翻转链表”——如 **Reverse Nodes in k‑Group**（LeetCode 25）。  
  2. “分段统计或修改链表”——如 **Split Linked List in Parts**（LeetCode 725）。  
  3. “链表分组并做特殊处理”——如 **Odd Even Linked List**（LeetCode 328）。  
- **一句话总结解题钥匙**：**把每一段当成独立的小链表，先定位好段首段尾，再用一次遍历的原地翻转把偶数段倒置，最后用前后两段的指针把它们拼回去**。

---

## 反思  

- **第一反应**：看到“自然数递增的组长度”，我立刻想到“遍历时计数，遇到目标长度就停下来”。  
- **最容易踩的坑**：  
  - **最后一组可能不足目标长度**，必须用实际计数 `cnt` 而不是硬性使用 `group_len`。  
  - **指针连接错误**：在翻转后一定要记得把原组首（现在的尾）指向下一组的首，否则会出现链表断裂或环。  
  - **空指针访问**：第一组前没有前驱，使用 dummy 节点可以统一处理。  
- **下次遇到同类题**，第一步应该思考：**“我能否在原链表上一次遍历完成定位+翻转+拼接，而不是把节点搬到额外容器里？”** 这往往是把时间复杂度从 O(n²) 降到 O(n) 的关键。