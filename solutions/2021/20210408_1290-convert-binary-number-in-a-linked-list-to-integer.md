# #1290. 将链表中的二进制数转换为整数 / Convert Binary Number in a Linked List to Integer

> 难度：简单 · 标签：Linked List、Math · [LeetCode 链接](https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/)

---

## 题目（英文原版）

**Description**

Given head which is a reference node to a singly-linked list. The value of each node in the linked list is either 0 or 1. The linked list holds the binary representation of a number.
Return the decimal value of the number in the linked list.
The most significant bit is at the head of the linked list.

**Examples**

**Example 1:**

```
Input: head = [1,0,1]
Output: 5
Explanation: (101) in base 2 = (5) in base 10
```

**Example 2:**

```
Input: head = [0]
Output: 0
```

**Constraints**

- The Linked List is not empty.
- Number of nodes will not exceed 30.
- Each node's value is either 0 or 1.

---

## 题目（中文翻译）

给定 `head`，它是指向一个单向链表（singly‑linked list）的引用节点。链表中每个节点的值仅为 `0` 或 `1`，链表整体保存了一个数的二进制表示（binary representation）。请返回该二进制数对应的十进制值（decimal value）。  
链表的头节点存放的是最高位（most significant bit）。

## 示例

### 示例 1  
**输入:** `head = [1,0,1]`  
**输出:** `5`  
**解释:** 二进制 `101`（base 2）等于十进制 `5`（base 10）

### 示例 2  
**输入:** `head = [0]`  
**输出:** `0`

## 约束条件
- 链表非空。  
- 节点数不超过 `30`。  
- 每个节点的值仅为 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把链表里的每个 `0/1` 按顺序记下来，组成一个二进制字符串（比如 `101`），然后把这个二进制数转换成十进制。  
- **用到的数据结构**：我们可以把每个节点的值放进一个 Python 列表或直接拼接成字符串。把链表想象成一本书的章节，`list`/`str` 就像把章节标题写在一张纸上，方便一次性查看。  
- **为什么正确**：二进制数的每一位就是链表的每个节点值，按照从头到尾的顺序就是从最高位到最低位。把它们拼成完整的二进制表示后，用语言自带的转换函数（`int(..., 2)`）就能得到对应的十进制数。  

#### 代码（Python）

```python
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val          # 节点保存的 0 或 1
        self.next = next        # 指向下一个节点的指针

def getDecimalValue_bruteforce(head: ListNode) -> int:
    """
    暴力解法：遍历链表，把每个节点的值收集成二进制字符串，
    最后用 int(str, 2) 转成十进制。
    """
    bits = []                     # 用列表临时保存每一位二进制字符
    cur = head
    while cur:                    # 只要还有节点，就一直往后走
        bits.append(str(cur.val)) # 把当前节点的 0/1 转成字符加入列表
        cur = cur.next            # 移动到下一个节点

    binary_str = ''.join(bits)    # 把列表里的字符拼成完整的二进制字符串
    # int(x, 2) 表示把以 2 为进制的字符串 x 转成十进制整数
    return int(binary_str, 2)
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  这里的 `n` 是链表的节点数。我们遍历一次链表（`while cur`），每个节点只处理一次，所以时间随节点数线性增长。  
- **空间复杂度**：`O(n)`  
  需要额外的列表 `bits` 来保存所有二进制位，列表的长度正好等于节点数 `n`，因此占用的额外空间也是线性的。

---

### 2. 最优解

#### 思路  
暴力解的慢点不在遍历，而是在**额外使用了 O(n) 的存储**（列表或字符串）。我们可以把“把二进制位拼起来”这一步，直接在遍历的过程中完成，而不需要额外的容器。  

关键在于二进制的**左移**操作：  
- 已经得到的十进制值 `num`，如果再往后接一个新的二进制位 `b`，相当于把 `num` 左移一位（相当于乘以 2），然后把 `b` 加到最低位。  
- 这正好可以用位运算表达：`num = (num << 1) | b`。  
  - `<< 1` 把 `num` 的二进制整体左移一位（相当于在右边补一个 0）。  
  - `| b` 把左移后最右边的 0 用当前节点的值 `b`（0 或 1）覆盖。  

把这一步放进遍历链表的循环里，就能在 **一次遍历、常数额外空间** 内得到答案。  

> **类比**：想象你在写一个电话号码，每读进一个新数字，就把已有的号码整体左移（在末尾留出一个空位），再把新数字写进去。最终写完所有数字后，手里就得到完整的号码，无需再把每个数字单独记下来。

#### 代码（Python）

```python
def getDecimalValue_optimal(head: ListNode) -> int:
    """
    最优解：在遍历链表的同时，使用位运算把二进制转成十进制。
    只需要 O(1) 的额外空间。
    """
    num = 0            # 用来累计答案的变量，初始为 0
    cur = head
    while cur:
        # 先把已有的答案左移一位（相当于乘以 2），再把当前位放到最低位
        num = (num << 1) | cur.val
        # 解释：假设目前 num = 5 (二进制 101)，
        #   左移后变成 1010 (十进制 10)，
        #   如果当前节点值是 1，则 1010 | 1 = 1011 (十进制 11)。
        cur = cur.next
    return num
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  仍然只遍历一次链表，每个节点只做常数次的位运算，时间随节点数线性增长。  
- **空间复杂度**：`O(1)`  
  只使用了几个整数变量（`num`、`cur`），与链表大小无关，属于常数级别的额外空间。

---

## 心得

- **核心技巧**：利用二进制的左移 (`<<`) 与或 (`|`) 运算，在遍历过程中实时累计结果，做到 **一次遍历、常数空间**。  
- **适用的题型**  
  1. **二进制转十进制**（如本题、LeetCode 1019）。  
  2. **在遍历过程中累加/构造数值**（比如把链表转成十进制整数、把字符流转成整数）。  
  3. **滑动窗口或前缀和的位运算版本**（如“子数组按位或”等）。  
- **一句话总结**：**左移再或**，让二进制“一路向左”，随手把每位塞进去，即可得到十进制。

---

## 反思

- **第一反应**：看到链表里都是 0/1，立刻想到把它们拼成二进制字符串再转换。  
- **最容易踩的坑**  
  - **忘记最高位在头部**：如果把链表倒着读，会得到相反的结果。  
  - **遗漏空链表**：虽然题目保证非空，但实际写代码时最好防御性检查。  
  - **位运算优先级**：`num << 1 | cur.val` 必须加括号写成 `(num << 1) | cur.val`，否则会先执行 `|` 再左移，得到错误答案。  
- **下次第一步**：判断是否可以在遍历时“即时累积”结果，思考对应的数学/位运算（如乘 2、加、或），而不是先把所有数据收集再统一处理。