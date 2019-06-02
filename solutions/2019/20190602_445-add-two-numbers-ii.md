# #445. 两数相加 II / Add Two Numbers II

> 难度：中等 · 标签：Linked List、Math、Stack · [LeetCode 链接](https://leetcode.com/problems/add-two-numbers-ii/)

---

## 题目（英文原版）

**Description**

You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.
Follow up: Could you solve it without reversing the input lists?

**Examples**

**Example 1:**

```
Input: l1 = [7,2,4,3], l2 = [5,6,4]
Output: [7,8,0,7]
```

**Example 2:**

```
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [8,0,7]
```

**Example 3:**

```
Input: l1 = [0], l2 = [0]
Output: [0]
```

**Constraints**

- The number of nodes in each linked list is in the range [1, 100].
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros.

---

## 题目（中文翻译）

给定两个非空链表（linked list），它们分别表示两个非负整数。最高位数字在链表首部，每个节点（node）只包含一位数字。将这两个数相加，并以链表形式返回其和。可以假设输入的两个数不含前导零，除非数字本身是 `0`。

**示例 1:**  
Input: l1 = [7,2,4,3], l2 = [5,6,4]  
Output: [7,8,0,7]

**示例 2:**  
Input: l1 = [2,4,3], l2 = [5,6,4]  
Output: [8,0,7]

**示例 3:**  
Input: l1 = [0], l2 = [0]  
Output: [0]

**约束条件**  
- 每个链表中的节点数在 `[1, 100]` 范围内。  
- `0 <= Node.val <= 9`。  
- 保证链表表示的数字没有前导零。

**进阶**  
你能在不反转输入链表的情况下完成此题吗？

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把两个链表对应的整数**全部取出来**，做普通的加法，然后再把结果拆成一位一位的数字，重新挂到链表上。  

实现步骤：

1. **遍历链表**，把每个结点的 `val` 依次放进一个数组（或直接拼成字符串）。  
   - 把链表看成一排排的数字卡片，从左到右依次读出来，就像在看一本数字书。  
2. 把数组/字符串转换成 Python 的整数 `int`，利用语言本身的“大整数”能力直接相加。  
   - 这里的 `int` 就像一个“超级计算器”，可以一次性算出很大的和。  
3. 把和再拆成每一位，重新建立一个新链表返回。  
   - 把结果数字重新写进一张新纸，每个格子放一位数字，最后把格子连起来就是答案链表。  

这种做法**一定正确**，因为我们没有改变数字的顺序，也没有遗漏任何位，只是借助了语言的整数运算。

#### 代码（Python）  

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def addTwoNumbers_brute(l1: ListNode, l2: ListNode) -> ListNode:
    # 1. 把链表转成字符串（相当于把每位数字拼成一个大数）
    def to_string(node: ListNode) -> str:
        digits = []
        while node:
            digits.append(str(node.val))   # 把每个结点的数字变成字符，放进列表
            node = node.next
        return ''.join(digits)            # 合并成完整的数字字符串

    num1 = int(to_string(l1))   # Python 自动把字符串转成大整数
    num2 = int(to_string(l2))

    total = num1 + num2         # 直接相加

    # 2. 把和拆成每一位，重新生成链表
    total_str = str(total)      # 再把和变回字符串，方便逐位读取
    dummy = ListNode(0)         # 哑结点，帮助返回结果
    cur = dummy
    for ch in total_str:        # 从左到右遍历每个字符（每位数字）
        cur.next = ListNode(int(ch))
        cur = cur.next
    return dummy.next           # 跳过哑结点，返回真实头结点
```

#### 复杂度  

- **时间复杂度：** `O(n + m)`  
  - 需要遍历两条链表各一次（`n`、`m` 为链表长度），以及遍历一次结果字符串。  
  - 用大白话说，就是“看一遍所有数字”，不管数字有多大，都只看一次。  

- **空间复杂度：** `O(n + m)`  
  - 额外用了存放数字字符的列表/字符串，大小正比于输入链表的长度。  
  - 这里的空间主要是“临时纸张”，用来记下读到的每一位。  

---

### 2. 最优解  

#### 思路  

**为什么暴力解慢？**  
- 虽然时间上已经是线性的，但它依赖于把整个数字转成 Python 的 `int`，这在一些语言（没有大整数）或在面试中会被认为是“作弊”。  
- 更重要的是，题目要求**不改变原链表顺序**（不能直接 `reverse`），而且**希望只用 O(1) 额外空间**（不算输出链表本身）。

**核心难点**：我们必须从**最低位**开始相加（因为进位从低位往高位传），但链表的最高位在头部，无法直接访问低位。  

**思路的关键一步**：利用 **栈（stack）** 这种“后进先出”的结构。  
- 把每条链表的结点值依次压进栈，等全部压完后，栈顶恰好是最低位。  
- 这相当于把数字倒过来装进一个盒子，最下面的数字（低位）先出来，正好符合手算加法的顺序。  

**具体步骤**  

1. **遍历两条链表**，把每个结点的 `val` 推入各自的栈 `s1、s2`。  
   - 想象我们把数字卡片一个接一个放进两只盒子里，最后盒子里最上面的卡片就是最低位。  

2. **弹出栈顶**（即取出最低位），把两位相加并加上进位 `carry`。  
   - `total = val1 + val2 + carry`  
   - 当前位的结果是 `total % 10`，新的进位是 `total // 10`。  

3. **把计算得到的当前位** **插入到结果链表的头部**（使用哑结点的 `next` 指针）。  
   - 因为我们是从低位往高位算的，而链表要求高位在前，所以每算完一位就把它“挂在最前面”。这一步相当于把新卡片放到已有卡片的最前面。  

4. 当两栈都空且 `carry` 为 0 时，结束循环。  

5. 返回哑结点的 `next` 即为答案链表。  

**为什么只用 O(1) 额外空间？**  
- 栈本质上是对输入链表的“复制”，但在面试里常把栈算作 **O(n)** 的额外空间（因为必须保存所有节点值）。如果要做到 **O(1)**，可以使用递归（调用栈）或把链表翻转后再恢复。不过这里的“最优解”指的是 **时间 O(n+m)** 且 **不需要逆转原链表**，栈是最直观、易实现的方式。  

#### 代码（Python）  

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    # 1. 把两个链表的值压进栈
    s1, s2 = [], []
    while l1:
        s1.append(l1.val)   # 像把数字卡片放进盒子
        l1 = l1.next
    while l2:
        s2.append(l2.val)
        l2 = l2.next

    carry = 0               # 进位，初始为 0
    dummy = ListNode(0)     # 哑结点，帮助我们在头部插入新结点

    # 2. 当还有数字或进位时，继续相加
    while s1 or s2 or carry:
        v1 = s1.pop() if s1 else 0   # 栈空了就当作 0
        v2 = s2.pop() if s2 else 0

        total = v1 + v2 + carry       # 当前位的和
        carry = total // 10           # 更新进位（0 或 1）
        cur_val = total % 10          # 当前位的实际数字

        # 3. 把当前位插入到结果链表的最前面
        new_node = ListNode(cur_val)
        new_node.next = dummy.next    # 把新结点指向当前的头结点
        dummy.next = new_node         # 哑结点指向新结点，形成“头插”

    return dummy.next   # 跳过哑结点，返回真正的答案链表
```

#### 复杂度  

- **时间复杂度：** `O(n + m)`  
  - 我们只遍历了两条链表一次（压栈），以及最多再遍历一次栈（弹出），每一步都是常数时间。  
  - 用大白话说，就是“把所有数字读两遍”，仍然是线性时间。  

- **空间复杂度：** `O(n + m)`（栈空间）  
  - 需要两个栈来保存每条链表的所有节点值。  
  - 如果把栈算作“临时纸张”，它的大小正好等于输入数字的位数。  
  - 若不计入输出链表本身，这已经是最省空间的方案（相较于把链表整体翻转再恢复）。  

---

## 心得  

- **核心技巧**：**栈**（后进先出）或**头插法**实现从低位到高位的加法，同时保持结果链表的高位在前。  
- **适用场景**：  
  1. “从尾部开始处理”的链表题，例如 **Add Two Numbers II**、**Reverse Linked List II**（需要倒序遍历）。  
  2. 需要**后序遍历**或**逆序访问**的树/链表问题，如 **Binary Tree Postorder Traversal**（使用栈模拟递归）。  
- **一句话总结**：**把链表倒着装进栈，弹栈时自然得到最低位，利用头插把结果倒回正序。**  

---

## 反思  

- **第一反应**：把链表直接转成整数或把链表翻转后再相加。  
- **最容易踩的坑**：  
  - 忽略进位 `carry` 仍然存在时需要继续循环（例如 999 + 1）。  
  - 处理不同长度的链表时要把空的栈当作 0，否则会报错。  
  - 头插法时一定要先让新结点指向旧的头结点，再让哑结点指向新结点，顺序错误会导致链表断裂。  
- **下次遇到同类题**：**先想“怎么把最低位先拿到手”，如果链表只能正向遍历，就考虑栈或递归来实现逆序访问。**