# #622. 设计循环队列 / Design Circular Queue

> 难度：中等 · 标签：Array、Linked List、Design、Queue · [LeetCode 链接](https://leetcode.com/problems/design-circular-queue/)

---

## 题目（英文原版）

**Description**

Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle, and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer".
One of the benefits of the circular queue is that we can make use of the spaces in front of the queue. In a normal queue, once the queue becomes full, we cannot insert the next element even if there is a space in front of the queue. But using the circular queue, we can use the space to store new values.
Implement the MyCircularQueue class:
You must solve the problem without using the built-in queue data structure in your programming language.

**Examples**

**Example 1:**

```
Input
["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
Output
[null, true, true, true, false, 3, true, true, true, 4]

Explanation
MyCircularQueue myCircularQueue = new MyCircularQueue(3);
myCircularQueue.enQueue(1); // return True
myCircularQueue.enQueue(2); // return True
myCircularQueue.enQueue(3); // return True
myCircularQueue.enQueue(4); // return False
myCircularQueue.Rear();     // return 3
myCircularQueue.isFull();   // return True
myCircularQueue.deQueue();  // return True
myCircularQueue.enQueue(4); // return True
myCircularQueue.Rear();     // return 4
```

**Constraints**

- 1 <= k <= 1000
- 0 <= value <= 1000
- At most 3000 calls will be made to enQueue, deQueue, Front, Rear, isEmpty, and isFull.

---

## 题目（中文翻译）

设计你的循环队列实现。循环队列是一种线性数据结构（linear data structure），其操作遵循先进先出（FIFO，First In First Out）原则，并且最后一个位置连接回第一个位置形成环形。它也被称为“环形缓冲区”（Ring Buffer）。

循环队列的一个好处是可以利用队列前部的空闲空间。在普通队列中，一旦队列满了，即使前面有空闲位置也无法插入新元素。但使用循环队列，可以把这些空闲位置用于存储新值。

实现 `MyCircularQueue` 类：

- 不能使用语言自带的队列（queue）数据结构。

---

### 示例 1

**输入**
```
["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
```

**输出**
```
[null, true, true, true, false, 3, true, true, true, 4]
```

**解释**
```java
MyCircularQueue myCircularQueue = new MyCircularQueue(3);
myCircularQueue.enQueue(1); // 返回 true
myCircularQueue.enQueue(2); // 返回 true
myCircularQueue.enQueue(3); // 返回 true
myCircularQueue.enQueue(4); // 返回 false，队列已满
myCircularQueue.Rear();     // 返回 3
myCircularQueue.isFull();   // 返回 true
myCircularQueue.deQueue();  // 返回 true
myCircularQueue.enQueue(4); // 返回 true
myCircularQueue.Rear();     // 返回 4
```

---

### 约束条件

- `1 <= k <= 1000`
- `0 <= value <= 1000`
- 最多会调用 `enQueue`、`deQueue`、`Front`、`Rear`、`isEmpty`、`isFull` 共计 3000 次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把队列当成 **普通的 Python 列表** 来操作：

- **入队** (`enQueue`)：直接 `list.append(value)`，把新元素放到列表尾部。  
- **出队** (`deQueue`)：把列表最前面的元素取出来，然后使用 `list.pop(0)` 删除它。`pop(0)` 会把后面的所有元素往前搬一次，就像把排队的第一位踢出去，后面的人依次向前走。  
- **获取队首/队尾**：分别返回 `list[0]` 和 `list[-1]`（如果列表为空则返回 `-1`）。  
- **判断空/满**：用 `len(list) == 0` 判断空，用 `len(list) == k`（容量）判断满。

> **类比**：想象我们在超市排队，超市没有环形通道，只有一条直线。要让第一个离开的顾客离开，后面所有人都必须往前走一步，这正是 `pop(0)` 的工作方式。

这种实现 **正确**，因为它完整地遵循了 FIFO（先入先出）的规则，并且在容量限制 `k` 之内进行判断。

#### 代码（Python）

```python
class MyCircularQueue:
    def __init__(self, k: int):
        """
        :param k: 队列的最大容量
        """
        self.k = k               # 最大容量
        self.q = []              # 用普通列表模拟队列

    def enQueue(self, value: int) -> bool:
        """往队尾插入一个元素，成功返回 True，已满返回 False"""
        if len(self.q) == self.k:   # 已经满了，不能插入
            return False
        self.q.append(value)        # 把元素放到列表尾部
        return True

    def deQueue(self) -> bool:
        """删除队首元素，成功返回 True，空队列返回 False"""
        if not self.q:              # 队列为空
            return False
        self.q.pop(0)               # 删除第一个元素，后面的元素会整体前移
        return True

    def Front(self) -> int:
        """返回队首元素的值，若队列为空返回 -1"""
        return self.q[0] if self.q else -1

    def Rear(self) -> int:
        """返回队尾元素的值，若队列为空返回 -1"""
        return self.q[-1] if self.q else -1

    def isEmpty(self) -> bool:
        """判断队列是否为空"""
        return len(self.q) == 0

    def isFull(self) -> bool:
        """判断队列是否已满"""
        return len(self.q) == self.k
```

#### 复杂度

- **时间复杂度**  
  - `enQueue`：`O(1)`（直接在列表尾部追加）。  
  - `deQueue`：`O(n)`，因为 `pop(0)` 需要把后面的 `n‑1` 个元素整体前移。这里的 `n` 最多是 `k`，也就是队列的最大容量。  
  - 其它查询操作均为 `O(1)`。  
  用大白话说，**删除队首** 的时候要“搬家”，最坏情况下要搬 `k` 次。

- **空间复杂度**  
  - `O(k)`，我们用一个列表保存最多 `k` 个元素。  

> 由于 `deQueue` 需要线性搬家，当调用次数很多时（题目最多 3000 次），整体运行时间可能会超出限制，这就是暴力解的 **瓶颈**。

---

### 2. 最优解

#### 思路  

要把所有操作都做到 **常数时间**（`O(1)`），关键在于 **避免搬家**。这正是环形队列（Ring Buffer）设计的初衷：

1. **固定大小的数组**：在构造函数里创建一个长度为 `k` 的列表（或 `[-1]*k`），提前分配好所有空间。  
2. **两个指针**  
   - `head` 指向当前 **队首** 的位置。  
   - `tail` 指向 **下一个可写入** 的位置（即队尾的下一格）。  
3. **取模运算实现环形**：当指针移动到数组末尾时，用 `(pos + 1) % k` 把它“绕回”数组开头，就像跑道上的跑步者跑完一圈后回到起点。  
4. **计数器 `size`**：记录当前队列中有多少元素。它帮助我们快速判断 **空**（`size == 0`）和 **满**（`size == k`），而不必靠指针相等来区分（因为 `head == tail` 既可能是空也可能是满）。  

**步骤演示**（以 `k = 3` 为例）：

- 初始状态：`head = 0`, `tail = 0`, `size = 0`，数组全是占位值 `-1`。  
- `enQueue(1)` → 把 `1` 放在 `tail`（位置 0），`tail = (0+1)%3 = 1`, `size = 1`。  
- `enQueue(2)` → 放在位置 1，`tail = 2`, `size = 2`。  
- `deQueue()` → 把 `head` 位置的值设为 `-1`（可选），`head = (0+1)%3 = 1`, `size = 1`。  
- 再次 `enQueue(3)` → 放在 `tail`（位置 2），`tail = 0`（回到开头），`size = 2`。  

这样每一次 **入队**、**出队**、**查询** 都只涉及指针的移动或一次数组访问，时间是 `O(1)`，没有搬家。

#### 代码（Python）

```python
class MyCircularQueue:
    def __init__(self, k: int):
        """
        :param k: 队列的最大容量
        """
        self.k = k                     # 最大容量
        self.buf = [-1] * k            # 环形缓冲区，预先分配固定大小
        self.head = 0                  # 指向队首元素的位置
        self.tail = 0                  # 指向下一个可写入的位置（队尾的下一格）
        self.size = 0                  # 当前队列中已有元素个数

    def enQueue(self, value: int) -> bool:
        """如果队列未满，写入 value 并返回 True；否则返回 False"""
        if self.isFull():
            return False               # 已经满了，不能再插入
        self.buf[self.tail] = value    # 把元素写到 tail 位置
        # tail 向后移动一格，遇到数组末尾时回到开头
        self.tail = (self.tail + 1) % self.k
        self.size += 1                 # 元素个数加一
        return True

    def deQueue(self) -> bool:
        """如果队列非空，删除队首元素并返回 True；否则返回 False"""
        if self.isEmpty():
            return False               # 空队列无法删除
        self.buf[self.head] = -1       # 可选：把被删除的位置恢复为占位值，便于调试
        # head 向后移动一格，同样使用取模实现环形
        self.head = (self.head + 1) % self.k
        self.size -= 1                 # 元素个数减一
        return True

    def Front(self) -> int:
        """返回队首元素的值，若队列为空返回 -1"""
        return self.buf[self.head] if not self.isEmpty() else -1

    def Rear(self) -> int:
        """返回队尾元素的值（即最近入队的元素），若队列为空返回 -1"""
        if self.isEmpty():
            return -1
        # tail 指向“下一个写入位置”，所以真实的队尾在 tail 前一格
        rear_index = (self.tail - 1 + self.k) % self.k
        return self.buf[rear_index]

    def isEmpty(self) -> bool:
        """判断队列是否为空"""
        return self.size == 0

    def isFull(self) -> bool:
        """判断队列是否已满"""
        return self.size == self.k
```

#### 复杂度

- **时间复杂度**：所有操作（`enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, `isFull`）均为 `O(1)`。只需要一次指针移动或一次数组访问，**不随元素个数增长**。  
  与暴力解相比，`deQueue` 从 `O(k)` 降到了 `O(1)`，这就是性能提升的关键。

- **空间复杂度**：`O(k)`，因为我们预先分配了一个固定大小为 `k` 的数组来存放元素。额外的指针和计数器只占用常数空间。

---

## 心得

- **核心技巧**：**使用固定大小数组 + 双指针 + 取模实现环形**，实现所有队列操作的常数时间。  
- **适用场景**（类似题目）  
  1. **Design Front Middle Back Queue**（LeetCode 1670）——需要在队列两端快速插入/删除，可借助双指针或双端队列。  
  2. **Design MyQueue**（LeetCode 232）或 **Design Stack Using Queues**（LeetCode 225）——利用两个栈/队列实现另一种数据结构，思路同样是“把复杂操作拆成 O(1) 的基本操作”。  
  3. **Moving Average from Data Stream**（LeetCode 346）——滑动窗口可以用环形缓冲区实现，避免每次都重新创建列表。  

- **一句话总结**：  
  “把队列装进环形缓冲区，用头尾指针和取模把空间循环利用，所有操作瞬间完成。”

---

## 反思

- **第一反应**：直接用 Python 列表 `append`/`pop(0)`，因为最熟悉，写起来最快。  
- **最容易踩的坑**  
  1. **`deQueue` 的搬家成本**：在大量删除时会导致时间爆炸。  
  2. **环形指针的取模**：忘记在 `tail` 前移时加上 `k` 防止负数，导致索引错误。  
  3. **空/满的判定**：仅靠 `head == tail` 无法区分，需要额外的 `size` 计数或在写入前后做特殊标记。  
- **下次第一步**：先判断“是否需要 **O(1)** 的全部操作”，如果是，就立刻考虑 **固定数组 + 双指针 + 取模** 的环形结构，而不是直接使用可变长列表。这样能在设计阶段就把时间复杂度控制在常数级。