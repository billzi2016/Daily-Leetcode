# #2816. **链表表示的数字翻倍** / Double a Number Represented as a Linked List

> 难度：中等 · 标签：Linked List、Math、Stack · [LeetCode 链接](https://leetcode.com/problems/double-a-number-represented-as-a-linked-list/)

---

## 题目（英文原版）

**Description**

You are given the head of a non-empty linked list representing a non-negative integer without leading zeroes.
Return the head of the linked list after doubling it.

**Examples**

**Example 1:**

```
Input: head = [1,8,9]
Output: [3,7,8]
Explanation: The figure above corresponds to the given linked list which represents the number 189. Hence, the returned linked list represents the number 189 * 2 = 378.
```

**Example 2:**

```
Input: head = [9,9,9]
Output: [1,9,9,8]
Explanation: The figure above corresponds to the given linked list which represents the number 999. Hence, the returned linked list reprersents the number 999 * 2 = 1998.
```

**Constraints**

- The number of nodes in the list is in the range [1, 104]
- 0 <= Node.val <= 9
- The input is generated such that the list represents a number that does not have leading zeros, except the number 0 itself.

---

## 题目（中文翻译）

给定一个非空链表的头节点 `head`，它表示一个没有前导零的非负整数。请返回将该整数翻倍后的链表头节点。

**示例 1**  

**输入**: `head = [1,8,9]`  
**输出**: `[3,7,8]`  
**解释**: 上图对应的链表表示数字 `189`，因此返回的链表表示 `189 * 2 = 378`。

**示例 2**  

**输入**: `head = [9,9,9]`  
**输出**: `[1,9,9,8]`  
**解释**: 上图对应的链表表示数字 `999`，因此返回的链表表示 `999 * 2 = 1998`。

**约束条件**

- 链表的节点数在 `[1, 10⁴]` 范围内。  
- `0 <= Node.val <= 9`。  
- 输入保证链表表示的数字没有前导零（除非数字本身是 `0`）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把链表“翻译”成一个普通整数，直接做乘法，再把结果重新写回链表。  

- **把链表变成整数**：从头到尾遍历，每读到一个节点，就把当前的数左移一位（乘以 10）再加上节点的值。这个过程就像把一串数字 **"1 8 9"** 按顺序拼成 **189**。  
- **整数乘以 2**：Python 的整数可以任意大，直接 `num * 2` 就得到答案。  
- **整数转回链表**：把结果拆成每一位，再按顺序创建新的节点。  

> **类比**：哈希表就像一本查字典的书，键是单词，值是页码。这里我们把链表看成一行行手写的数字，先把它们抄到纸上（整数），算完再抄回去（链表）。  

这个方法一定正确，因为我们没有改变数字的意义，只是换了一个更方便的表达形式。  

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def doubleNumber_bruteforce(head: ListNode) -> ListNode:
    """暴力解：把链表转成整数 → 乘 2 → 再转成链表"""
    # 1️⃣ 把链表转成整数
    num = 0
    cur = head
    while cur:                     # 从左到右依次读取每位
        num = num * 10 + cur.val   # 相当于在十进制数后面“拼”一个新数字
        cur = cur.next

    # 2️⃣ 直接乘以 2
    num *= 2

    # 3️⃣ 把结果转成链表（注意 0 的特殊情况）
    if num == 0:
        return ListNode(0)

    # 把每一位放到栈里，方便逆序取出（因为链表是从高位到低位）
    stack = []
    while num:
        stack.append(num % 10)      # 取出最低位
        num //= 10                  # 去掉最低位

    # 依次弹出，构造链表（弹出顺序正好是高位到低位）
    dummy = ListNode(0)            # 虚拟头结点，简化代码
    cur = dummy
    while stack:
        cur.next = ListNode(stack.pop())
        cur = cur.next

    return dummy.next
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 遍历链表一次把数字读出来 `O(n)`，再把整数拆位也最多 `O(n)`（因为位数不超过链表长度），所以总体是线性时间。  
  - 大白话：如果链表有 10 000 个节点，程序跑的步数大概和 10 000 成正比。  

- **空间复杂度**：`O(n)`  
  - 需要额外的栈（或列表）来存放每一位，最坏情况和链表等长。  

---  

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于把整个数字搬到 Python 的大整数里。虽然 Python 能处理，但这一步会占用额外的 `O(n)` 空间，而且在面试中往往希望我们 **直接在链表上完成**。  

**核心思路**：从 **最低位** 开始逐位乘以 2，处理进位（carry），最后如果最高位还有进位，就在最前面再补一个节点。  

因为链表是单向的，不能直接从尾部往前遍历。我们有两种常见的技巧：

1. **反转链表** → 正向遍历（此时原来的尾部变成头部） → 再反转回来。  
2. **使用栈**：把所有节点压进栈，随后弹出时自然是从尾到头的顺序。  

这里选用 **栈**，因为它保持了原链表结构，不需要额外的指针操作，思路更直观。  

**步骤拆解**  

1. **遍历链表，把每个节点压进栈**。这一步相当于把数字的每一位“放进盒子”，盒子最上面的是最低位。  
2. **弹出栈**，从最低位开始乘以 2，并加上上一次的进位 `carry`。  
   - `total = node.val * 2 + carry`  
   - 当前位的值 = `total % 10`（因为十进制只能保留 0~9）  
   - 新的进位 = `total // 10`（可能是 0 或 1）  
   - 用弹出的节点直接改写它的值（就地修改），不需要新建节点。  
3. **处理完所有节点后**，如果 `carry` 仍为 1，需要在最前面再创建一个新节点，值为 1，指向原来的头结点。  
4. **返回新的头结点**（可能是新创建的节点，也可能是原始头结点）。  

> **类比**：想象你在纸上写下一个大数，然后从最右边的数字开始向左算乘法，遇到进位就往左边的数字“递交”。栈就像一叠纸，把最右边的数字放在最上面，弹出来时自然先处理右边的。  

#### 代码（Python）  

```python
def doubleNumber_optimal(head: ListNode) -> ListNode:
    """最优解：使用栈逐位乘以 2，原地修改链表"""
    if not head:                     # 防御性写法，实际题目保证非空
        return None

    # 1️⃣ 把所有节点压进栈（相当于把数字倒过来存）
    stack = []
    cur = head
    while cur:
        stack.append(cur)            # 保存节点本身，后面可以直接改值
        cur = cur.next

    carry = 0                        # 初始没有进位
    # 2️⃣ 从低位到高位弹出，完成乘 2 + 进位
    while stack:
        node = stack.pop()           # 现在 node 对应当前处理的位
        total = node.val * 2 + carry
        node.val = total % 10        # 更新该位的值
        carry = total // 10          # 计算新的进位（0 或 1）

    # 3️⃣ 最高位仍有进位，需要在最前面加一个新节点
    if carry:
        new_head = ListNode(carry)   # 进位只能是 1，因为 9*2+1=19
        new_head.next = head
        head = new_head

    return head
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历链表一次把节点压栈 `O(n)`，再弹栈一次做乘法 `O(n)`，常数因子很小。  
  - 与暴力解相比，**不再需要把数字搬到 Python 的大整数**，但时间量级相同，仍是线性。  

- **空间复杂度**：`O(n)`（栈）  
  - 需要额外的栈来保存节点指针，最坏情况和链表等长。  
  - 如果允许**原地反转链表**，可以把空间降到 `O(1)`（不再需要栈），但实现稍微繁琐，这里保留栈的写法因为更易懂。  

---  

## 心得  

- **核心技巧**：**逐位模拟十进制运算 + 进位处理**，配合**栈**实现从低位到高位的遍历。  
- **适用场景**：  
  1. “链表表示的整数 + 整数” 类问题（如 `Add Two Numbers`、`Multiply Two Numbers`）。  
  2. 需要 **逆序遍历** 单向链表的场景（如 `Reverse Linked List`、`Palindrome Linked List` 判断时的比较）。  
- **解题钥匙**：**把“从右往左”转化为“从栈顶弹出”或“把链表反转”，再逐位做普通的十进制运算**。  

---  

## 反思  

- **第一反应**：把链表直接转成整数，然后乘 2，最后再转回链表。  
- **最容易踩的坑**：  
  - 忘记处理最高位的进位，导致结果少了一个最高位（比如 999 → 1998）。  
  - 进位可能是 1，也可能是 0，写代码时一定要把 `carry` 继续向左传播。  
  - 对空链表或仅有一个节点的特殊情况要有防御性检查。  
- **下次类似题的第一步**：**先确定遍历顺序**（是从低位还是高位），如果是单向链表且需要逆序，立刻想到 “栈 + 逆序弹出” 或 “链表反转” 两种技巧之一。