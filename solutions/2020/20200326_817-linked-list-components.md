# #817. 链表组件 / Linked List Components

> 难度：中等 · 标签：Array、Hash Table、Linked List · [LeetCode 链接](https://leetcode.com/problems/linked-list-components/)

---

## 题目（英文原版）

**Description**

You are given the head of a linked list containing unique integer values and an integer array nums that is a subset of the linked list values.
Return the number of connected components in nums where two values are connected if they appear consecutively in the linked list.

**Examples**

**Example 1:**

```
Input: head = [0,1,2,3], nums = [0,1,3]
Output: 2
Explanation: 0 and 1 are connected, so [0, 1] and [3] are the two connected components.
```

**Example 2:**

```
Input: head = [0,1,2,3,4], nums = [0,3,1,4]
Output: 2
Explanation: 0 and 1 are connected, 3 and 4 are connected, so [0, 1] and [3, 4] are the two connected components.
```

**Constraints**

- The number of nodes in the linked list is n.
- 1 <= n <= 104
- 0 <= Node.val < n
- All the values Node.val are unique.
- 1 <= nums.length <= n
- 0 <= nums[i] < n
- All the values of nums are unique.

---

## 题目（中文翻译）

给定一个 **链表**（linked list）的头节点 `head`，该链表中的节点值互不相同；再给定一个整数数组 `nums`，它是链表中值的一个子集（subset）。  
返回 `nums` 中的 **连通分量**（connected components）的数量，其中如果两个值在链表中是相邻出现的，则它们被视为连接在一起。

**示例 1**  

**示例 2**  

**约束条件**

- 链表中的节点数为 `n`。  
- `1 <= n <= 10^4`  
- `0 <= Node.val < n`  
- 所有 `Node.val` 均唯一。  
- `1 <= nums.length <= n`  
- `0 <= nums[i] < n`  
- `nums` 中的所有值均唯一。  

---

## 示例

### 示例 1
**输入**: `head = [0,1,2,3]`, `nums = [0,1,3]`  
**输出**: `2`  
**解释**: `0` 和 `1` 在链表中相邻，所以形成一个连通分量 `[0, 1]`；`3` 单独成另一个连通分量 `[3]`。因此共有 2 个连通分量。

### 示例 2
**输入**: `head = [0,1,2,3,4]`, `nums = [0,3,1,4]`  
**输出**: `2`  
**解释**: `0` 与 `1` 相邻，`3` 与 `4` 相邻，分别形成两个连通分量 `[0, 1]` 和 `[3, 4]`。因此返回 2。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每一个 `nums` 中的元素，去链表里把它找出来，然后看它的前后节点是否也在 `nums` 中**。  
如果相邻的两个节点都在 `nums`，说明它们属于同一个连通分量；否则就把它算作一个新的分量。  

这里用到的主要数据结构是 **链表**（`ListNode`）和 **数组**（`nums`）。  
- 链表可以看成一串手牵手的孩子，从头结点依次往后走，每次只能看到下一个孩子。  
- `nums` 就像一张“名单”，我们只关心名单里出现的孩子。  

暴力做法的步骤：  

1. 对 `nums` 中的每个值 `x`，从链表的头结点开始遍历，找到值为 `x` 的节点（线性搜索）。  
2. 找到后检查它的 `next` 节点的值是否也在 `nums` 中。如果是，则把这两个节点视为同一组件的一部分；如果不是，则 `x` 开始一个新组件。  
3. 用一个计数器 `components` 记录出现的组件数量。  

**为什么这个方法是对的**  
只要我们能准确判断每个 `nums` 中的元素是否与它的下一个链表节点也在 `nums`，就能确定它们是否属于同一连通块。遍历完整个 `nums`，每发现一次“前后不相连”，就说明一个新块的开始，最终计数即为答案。

**时间/空间复杂度分析（大白话）**  

- 对 `nums` 长度为 `m`，链表长度为 `n`。  
- 第一步里，每找一个 `x` 都要从链表头开始遍历，最坏情况要走 `n` 步。  
- 所以总的时间是 `m × n`，记作 **O(m·n)**。如果把 `m` 看成和 `n` 同级（因为 `m ≤ n`），可以说是 **O(n²)**，意思是“时间会随节点数量的平方而增长”。  
- 额外使用的空间只有计数器和几个指针，和输入规模无关，记作 **O(1)**（常数级）。


#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def numComponents_bruteforce(head: ListNode, nums: list[int]) -> int:
    """暴力解：对 nums 中的每个值，在链表里线性搜索"""
    components = 0                      # 记录连通块数量
    for x in nums:                      # 逐个检查 nums 中的元素
        # 1. 从链表头开始找值为 x 的节点
        cur = head
        while cur and cur.val != x:     # 线性遍历链表
            cur = cur.next
        # 这里根据题意，x 必定在链表中（nums 是链表的子集），所以 cur 不会是 None
        # 2. 检查下一个节点是否也在 nums 中
        if not cur.next or cur.next.val not in nums:
            # 若没有下一个，或下一个不在 nums，说明这是一个组件的结束
            components += 1
    return components
```

#### 复杂度  

- **时间复杂度**：**O(m·n)**（最坏情况下约为 O(n²)），因为对 `nums` 中的每个元素都要遍历一次完整链表。  
- **空间复杂度**：**O(1)**，只用了常数级的额外变量。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要从链表头部重新遍历**，这导致了二次遍历的灾难。  
实际上，我们只需要一次遍历链表就能判断所有连通块。关键在于**快速判断一个节点的值是否在 `nums` 中**。  

**优化步骤**  

1. **把 `nums` 放进哈希表（Python 中的 `set`）**。  
   - 哈希表像一本“字典”，可以在 O(1) 的时间内（几乎瞬间）判断一个键是否存在。  
2. **一次遍历链表**，对每个节点 `cur` 做两件事：  
   - 如果 `cur.val` 在 `set(nums)` 中，说明它是我们关心的节点。  
   - 再检查它的下一个节点 `cur.next` 是否也在 `set(nums)`。  
     - 若 **不在**（或者已经是链表末尾），说明 `cur` 是当前连通块的**结束**，于是计数器 `components` 加 1。  
   - 若 **在**，说明 `cur` 与下一个节点属于同一个块，什么都不做，等后面再处理。  
3. 遍历结束后，`components` 就是答案。  

**为什么只遍历一次就够了**  
因为链表本身已经给出了节点的顺序。只要我们知道哪些节点是 “目标集合” (`nums`)，就可以在顺序遍历时直接判断“当前节点是否是块的最后一个”。这相当于在链表上“标记”了所有感兴趣的节点，然后把相邻的标记合并成一个块。

**核心数据结构**：  
- **哈希集合（set）**：查找是否在 `nums` 中的时间复杂度是 O(1)。把它想象成一本“快速查找手册”，只要翻一页就能知道某个数字是否在名单里。  
- **指针遍历**：一次顺序遍历链表，时间线性 O(n)。  

**时间/空间复杂度大白话**  

- 只遍历一次链表，节点数 `n`，所以时间是 **O(n)**，意思是“随着链表长度线性增长”。  
- 额外存了一个集合，大小等于 `nums` 长度 `m ≤ n`，所以空间是 **O(m)**，最多也就是 O(n)。  

#### 代码（Python）

```python
def numComponents(head: ListNode, nums: list[int]) -> int:
    """最优解：一次遍历 + 哈希集合"""
    target = set(nums)          # 把 nums 放进哈希集合，O(1) 判断是否在集合中
    components = 0              # 记录连通块数量

    cur = head
    while cur:                  # 线性遍历链表
        if cur.val in target:   # 当前节点是我们关心的
            # 判断下一个节点是否也在 nums 中
            # 若下一个不存在或不在集合，则当前节点是块的末尾
            if not cur.next or cur.next.val not in target:
                components += 1
        cur = cur.next          # 前进到下一个节点
    return components
```

#### 复杂度  

- **时间复杂度**：**O(n)**，只遍历一次链表，每个节点的判断都是 O(1)。比暴力的 O(n²) 快很多。  
- **空间复杂度**：**O(m)**，额外存储 `nums` 的集合，最坏情况下和链表长度相同（O(n)），但不随遍历次数增长。

---  

## 心得  

- 这道题的核心技巧是 **利用哈希集合把“是否在集合”转化为 O(1) 的查询**，从而把原本的二次遍历降到一次遍历。  
- 该技巧常用于需要 **快速成员判定** 的题目，例如：  
  1. **Intersection of Two Arrays**（求两个数组交集）  
  2. **Longest Consecutive Sequence**（最长连续序列）  
  3. **Word Break**（单词拆分）中判断子串是否在字典里。  
- 一句话总结解题钥匙：**把需要频繁判断“在不在”的元素预先放进哈希表，遍历一次即可完成所有判定**。  

## 反思  

- **第一反应**：看到链表和子集，立刻想到要遍历链表并在子集里查找，结果想到用哈希表加速。  
- **最容易踩的坑**：  
  - 忘记处理链表末尾的情况（`cur.next` 为 `None`），会导致空指针错误。  
  - 误把 “相邻的两个值都在 `nums`” 当成 “只要出现一次相邻即算一个块”，其实需要判断 **块的结束**（即下一个不在集合）来计数。  
- **下次遇到同类题**，第一步应该思考：**是否可以把关键的“成员关系”预处理为 O(1) 的查找结构**，然后再决定遍历策略。这样往往能把暴力的二次遍历直接降到线性时间。