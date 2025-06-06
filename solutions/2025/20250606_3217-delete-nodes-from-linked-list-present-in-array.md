# #3217. 删除链表中出现在数组中的节点 / Delete Nodes From Linked List Present in Array

> 难度：中等 · 标签：Array、Hash Table、Linked List · [LeetCode 链接](https://leetcode.com/problems/delete-nodes-from-linked-list-present-in-array/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums and the head of a linked list. Return the head of the modified linked list after removing all nodes from the linked list that have a value that exists in nums.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], head = [1,2,3,4,5]
Output: [4,5]
Explanation:

Remove the nodes with values 1, 2, and 3.
```

**Example 2:**

```
Input: nums = [1], head = [1,2,1,2,1,2]
Output: [2,2,2]
Explanation:

Remove the nodes with value 1.
```

**Example 3:**

```
Input: nums = [5], head = [1,2,3,4]
Output: [1,2,3,4]
Explanation:

No node has value 5.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105
- All elements in nums are unique.
- The number of nodes in the given list is in the range [1, 105].
- 1 <= Node.val <= 105
- The input is generated such that there is at least one node in the linked list that has a value not present in nums.

---

## 题目（中文翻译）

给定一个整数数组 `nums`（array）和一个链表的头节点 `head`（linked list），请在链表中删除所有节点，其节点值（value）出现在 `nums` 中。返回删除操作后链表的头节点。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`
- `nums` 中的所有元素互不相同。
- 给定链表的节点数在 `[1, 10^5]` 范围内。
- `1 <= Node.val <= 10^5`
- 输入保证链表中至少存在一个节点的值不在 `nums` 中。

---

### 示例

**示例 1**  
**输入**: `nums = [1,2,3]`, `head = [1,2,3,4,5]`  
**输出**: `[4,5]`  
**解释**:  
删除值为 `1、2、3` 的节点。

**示例 2**  
**输入**: `nums = [1]`, `head = [1,2,1,2,1,2]`  
**输出**: `[2,2,2]`  
**解释**:  
删除值为 `1` 的节点。

**示例 3**  
**输入**: `nums = [5]`, `head = [1,2,3,4]`  
**输出**: `[1,2,3,4]`  
**解释**:  
没有节点的值为 `5`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `nums` 里的每个数都拿出来，和链表中的每个节点逐个比较**。  
- 数据结构：  
  - **链表**：像是一串用绳子相连的珠子，只有前后相邻的两个珠子能直接看到对方。遍历链表只能从头往后一步一步走。  
  - **数组 `nums`**：把它想成一本装有若干数字的“小册子”。  
- 解法步骤：  
  1. 从链表的头结点开始遍历。  
  2. 对当前节点的值，在 `nums` 中做一次线性搜索（`for x in nums`），看是否相等。  
  3. 如果相等，就把当前节点从链表中摘掉（让前一个节点的 `next` 指向当前节点的 `next`）。  
  4. 否则保留，继续往后走。  
- 为什么正确：只要遍历完所有节点，并且每次都按照上面的规则判断是否删除，最终链表中留下的节点必然不在 `nums` 中。  

**时间复杂度**  
- 对每个链表节点，我们都要在 `nums` 中遍历一次，最坏情况是 `len(nums) = m`，链表长度为 `n`。  
- 总的比较次数是 `n * m`，用大写的 **O(n·m)** 表示。  
- 大白话：如果 `nums` 有 1000 个数，链表有 1000 个节点，就要做 1000 × 1000 = 100 万次比较。

**空间复杂度**  
- 只使用了几个指针变量，和输入规模无关，用 **O(1)** 表示。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点的值
        self.next = next        # 指向下一个节点的指针

def delete_nodes_bruteforce(nums, head):
    """
    暴力解法：每个节点都在 nums 中线性搜索
    :param nums: List[int] 需要删除的值集合
    :param head: ListNode 链表头结点
    :return: ListNode 删除后的链表头
    """
    dummy = ListNode(0)          # 虚拟头结点，方便统一处理头结点被删的情况
    dummy.next = head
    prev = dummy                 # prev 永远指向当前节点的前一个节点
    cur = head                   # 当前遍历的节点

    while cur:
        # 在 nums 中逐个比较
        should_delete = False
        for x in nums:           # 线性搜索
            if cur.val == x:
                should_delete = True
                break

        if should_delete:
            # 删除 cur：让 prev.next 跳过 cur，直接指向 cur.next
            prev.next = cur.next
        else:
            # 不删除，prev 向前走一步
            prev = cur

        cur = cur.next           # 无论删不删，都把 cur 向后移
    return dummy.next
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - `n` 为链表节点数，`m` 为 `nums` 长度。  
  - 就像把每个珠子都放进一本厚厚的册子里翻一遍，最坏情况下要翻很多遍。
- **空间复杂度**：`O(1)`  
  - 只用了常数个指针，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到**瓶颈在于每次都要在 `nums` 中线性搜索**。  
如果能够把“在 `nums` 中查找是否存在”这一步变得 **O(1)**，整体复杂度就会大幅下降。  

**哈希集合（`set`）** 正好可以做到这一点：  
- 把 `nums` 的所有元素一次性放进集合中。  
- 集合的查询操作（`x in s`）在平均情况下是常数时间 `O(1)`，就像在字典里查词一样，直接把词翻到对应的页码。  

优化步骤如下：

1. **预处理**：把 `nums` 全部放入 `set_nums`（时间 `O(m)`，空间 `O(m)`）。  
2. **遍历链表**：仍然使用虚拟头结点 `dummy`，依次检查每个节点的值是否在 `set_nums` 中。  
   - 如果在集合里，说明需要删除，操作同暴力解。  
   - 如果不在，保留节点。  
3. 完成遍历后返回 `dummy.next` 即为答案。  

这样每个节点只做一次 **O(1)** 的集合查询，整体时间降到 **O(n + m)**。  

#### 代码（Python）

```python
def delete_nodes_optimal(nums, head):
    """
    最优解：利用哈希集合把“是否在 nums 中”检查降到 O(1)
    :param nums: List[int] 需要删除的值集合（元素唯一）
    :param head: ListNode 链表头结点
    :return: ListNode 删除后的链表头
    """
    # 1. 把 nums 放进集合，方便 O(1) 查询
    to_remove = set(nums)        # set 相当于“查字典”，key 是数值，value 只要存在即可

    dummy = ListNode(0)          # 虚拟头结点，统一处理头结点被删的情况
    dummy.next = head
    prev = dummy
    cur = head

    while cur:
        if cur.val in to_remove:     # O(1) 判断当前值是否需要删除
            # 删除 cur
            prev.next = cur.next
        else:
            # 保留 cur，prev 前进一步
            prev = cur
        cur = cur.next                # 移动到下一个节点
    return dummy.next
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - `m` 为 `nums` 长度（把数组装进集合），`n` 为链表节点数（遍历一次）。  
  - 与暴力解的 `O(n·m)` 相比，省掉了大量重复比较，像是把一本厚厚的册子换成了字典，查找瞬间完成。
- **空间复杂度**：`O(m)`  
  - 需要额外的集合来存放 `nums`，大小正好等于 `nums` 的长度。  
  - 除此之外仍然只用常数个指针。

---

## 心得

- **核心技巧**：使用哈希集合（`set`）实现**快速成员判定**。  
- **适用的题型**：  
  1. “从链表/数组中删除满足某集合条件的元素”。  
  2. “判断两个数组是否有交集、去重、统计出现次数”。  
  3. “在遍历过程中频繁检查元素是否在某集合里”。  
- **解题钥匙**：**把“遍历中每次都要线性搜索”改成“预处理一次，后续 O(1) 查询”。**

---

## 反思

- **第一反应**：看到“数组”和“链表”，立刻想到遍历链表并逐个对比数组，写出暴力实现。  
- **最容易踩的坑**：  
  - **头结点被删除**：如果直接在原链表上操作，删除头结点会导致失去入口，需要额外判断或使用虚拟头结点。  
  - **集合的创建**：忘记把 `nums` 转成 `set`，导致仍然是 `O(n·m)`。  
  - **输入规模**：`nums` 和链表都可能长达 10⁵，必须使用线性或接近线性的算法，否则会超时。  
- **下次类似题的第一步**：先判断“是否需要频繁判断‘元素是否在某集合里’”，如果是，立即构造哈希集合/字典，再进行主遍历。