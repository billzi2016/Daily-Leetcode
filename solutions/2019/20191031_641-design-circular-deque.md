# #641. 循环双端队列 / Design Circular Deque

> 难度：中等 · 标签：Array、Linked List、Design、Queue · [LeetCode 链接](https://leetcode.com/problems/design-circular-deque/)

---

## 题目（英文原版）

**Description**

Design your implementation of the circular double-ended queue (deque).
Implement the MyCircularDeque class:

**Examples**

**Example 1:**

```
Input
["MyCircularDeque", "insertLast", "insertLast", "insertFront", "insertFront", "getRear", "isFull", "deleteLast", "insertFront", "getFront"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
Output
[null, true, true, true, false, 2, true, true, true, 4]

Explanation
MyCircularDeque myCircularDeque = new MyCircularDeque(3);
myCircularDeque.insertLast(1);  // return True
myCircularDeque.insertLast(2);  // return True
myCircularDeque.insertFront(3); // return True
myCircularDeque.insertFront(4); // return False, the queue is full.
myCircularDeque.getRear();      // return 2
myCircularDeque.isFull();       // return True
myCircularDeque.deleteLast();   // return True
myCircularDeque.insertFront(4); // return True
myCircularDeque.getFront();     // return 4
```

**Constraints**

- 1 <= k <= 1000
- 0 <= value <= 1000
- At most 2000 calls will be made to insertFront, insertLast, deleteFront, deleteLast, getFront, getRear, isEmpty, isFull.

---

## 题目（中文翻译）

设计循环双端队列（circular double-ended queue，deque）的实现。  
实现 `MyCircularDeque` 类，使其能够在固定容量 `k` 内支持在两端插入、删除以及查询操作。

**实现的成员函数**  
- `MyCircularDeque(k)`：构造函数，初始化容量为 `k` 的循环双端队列。  
- `insertFront(value)`：在队列头部插入 `value`，成功返回 `true`，若队列已满返回 `false`。  
- `insertLast(value)`：在队列尾部插入 `value`，成功返回 `true`，若队列已满返回 `false`。  
- `deleteFront()`：删除队列头部的元素，成功返回 `true`，若队列为空返回 `false`。  
- `deleteLast()`：删除队列尾部的元素，成功返回 `true`，若队列为空返回 `false`。  
- `getFront()`：获取队列头部的元素，若队列为空返回 `-1`。  
- `getRear()`：获取队列尾部的元素，若队列为空返回 `-1`。  
- `isEmpty()`：若队列为空返回 `true`，否则返回 `false`。  
- `isFull()`：若队列已满返回 `true`，否则返回 `false`。  

**示例**

```json
Input
["MyCircularDeque", "insertLast", "insertLast", "insertFront", "insertFront", "getRear", "isFull", "deleteLast", "insertFront", "getFront"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]

Output
[null, true, true, true, false, 2, true, true, true, 4]
```

**解释**
```java
MyCircularDeque myCircularDeque = new MyCircularDeque(3);
myCircularDeque.insertLast(1);   // 返回 true
myCircularDeque.insertLast(2);   // 返回 true
myCircularDeque.insertFront(3);  // 返回 true
myCircularDeque.insertFront(4);  // 返回 false，队列已满
myCircularDeque.getRear();       // 返回 2
myCircularDeque.isFull();        // 返回 true
myCircularDeque.deleteLast();    // 返回 true
myCircularDeque.insertFront(4);  // 返回 true
myCircularDeque.getFront();      // 返回 4
```

**约束条件**
- `1 <= k <= 1000`
- `0 <= value <= 1000`
- 最多会调用 `insertFront`、`insertLast`、`deleteFront`、`deleteLast`、`getFront`、`getRear`、`isEmpty`、`isFull` 共计 2000 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把双端队列（deque）看成 **普通的 Python 列表**，  
- **在前端插入 / 删除** 用 `list.insert(0, x)` / `list.pop(0)`  
- **在后端插入 / 删除** 用 `list.append(x)` / `list.pop()`  

这就像在一本笔记本的最前面或最后面写字、擦字，代码实现非常直观。  
因为题目只要求判断是否“已满”或“为空”，我们在每次操作前检查列表的长度是否已经等于容量 `k`，如果是就返回 `False`（插入失败），否则执行对应的列表方法并返回 `True`。

> **为什么正确**  
> - `list.append` 把元素放在“尾部”，对应题目中的 `insertLast`。  
> - `list.insert(0, x)` 把元素放在“前端”，对应 `insertFront`。  
> - `pop`、`pop(0)` 分别把元素从尾部或前端移除，正好对应 `deleteLast`、`deleteFront`。  
> - `list[0]`、`list[-1]` 能直接得到队首和队尾的值。只要我们严格控制长度不超过 `k`，所有行为都符合题意。

#### 代码（Python）  

```python
class MyCircularDeque:
    """
    暴力实现：内部直接使用 Python list
    每个操作都可能需要 O(n) 的时间（因为 insert(0) / pop(0) 要搬迁元素）
    """
    def __init__(self, k: int):
        self.capacity = k          # 最大容量
        self.q = []                # 用列表模拟双端队列

    # 在队首插入
    def insertFront(self, value: int) -> bool:
        if len(self.q) == self.capacity:   # 已满，插不进去
            return False
        self.q.insert(0, value)            # 把元素放到最前面
        return True

    # 在队尾插入
    def insertLast(self, value: int) -> bool:
        if len(self.q) == self.capacity:
            return False
        self.q.append(value)               # 把元素放到最后面
        return True

    # 删除队首
    def deleteFront(self) -> bool:
        if not self.q:                     # 空队列
            return False
        self.q.pop(0)                      # 删除最前面的元素
        return True

    # 删除队尾
    def deleteLast(self) -> bool:
        if not self.q:
            return False
        self.q.pop()                       # 删除最后面的元素
        return True

    # 读取队首元素
    def getFront(self) -> int:
        if not self.q:
            return -1
        return self.q[0]

    # 读取队尾元素
    def getRear(self) -> int:
        if not self.q:
            return -1
        return self.q[-1]

    # 判断是否为空
    def isEmpty(self) -> bool:
        return len(self.q) == 0

    # 判断是否已满
    def isFull(self) -> bool:
        return len(self.q) == self.capacity
```

#### 复杂度  

- **时间复杂度**  
  - `insertFront` / `deleteFront` 需要把所有元素往后（或往前）搬一位，最坏是 **O(k)**，在这里我们把它写成 **O(n)**（n 为当前元素个数），相当于“线性时间”。  
  - `insertLast` / `deleteLast` 只在列表尾部操作，时间是 **O(1)**（常数时间）。  
- **空间复杂度**  
  - 只用了一个列表保存最多 `k` 个元素，**O(k)** 的额外空间。  
  - 这里的 `k` 最多 1000，空间完全可以接受。

> 大白话解释：  
> - **O(k)** 就是“最坏情况下要遍历一遍所有格子”，想象你要把一本笔记本里所有页码往后搬一格，最多要搬 `k` 次。  
> - **O(1)** 就是“一下子搞定”，像在笔记本的最末页直接写字，不需要搬别的页。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 出在前端的 `insertFront` 与 `deleteFront`，因为它们要把整个列表“搬砖”。  
要把这两个操作也做到 **O(1)**，我们需要一种 **不搬元素、只动指针** 的结构——**循环数组（环形缓冲区）**。

**循环数组的核心概念**  

| 名称 | 类比 | 作用 |
|------|------|------|
| **head** | 笔记本的“第一页”指针 | 指向当前队首所在的下标 |
| **tail** | 笔记本的“最后一页”指针的下一个位置 | 指向队尾的后一个位置（即下一个可以写入的位置） |
| **capacity** | 笔记本的总页数（固定） | 决定数组大小 `k+1`（多留一个空位，用来区分空和满） |
| **取模 `%`** | 把指针“环回”到笔记本的开头 | 当指针走到数组末尾再往前，就回到 0 位置，实现“循环” |

为什么要把数组大小设为 `k+1`？  
- 当 **head == tail** 时，表示 **空**。  
- 当 **(tail + 1) % size == head** 时，表示 **满**。  
多留一个格子可以让这两种状态通过指针的位置唯一判定，避免“满”和“空”混淆。

**一步步实现**  

1. **初始化**：创建长度为 `k+1` 的列表 `data`（所有位置先填 `0`），`head = 0, tail = 0`。  
2. **insertFront(value)**  
   - 先判断是否已满：`(tail + 1) % size == head`。  
   - 若未满，`head = (head - 1 + size) % size`（向左循环），把 `value` 放到 `data[head]`。  
3. **insertLast(value)**  
   - 同样先判断满。  
   - 若未满，`data[tail] = value`，然后 `tail = (tail + 1) % size`（向右循环）。  
4. **deleteFront()**  
   - 若空直接返回 `False`。  
   - 否则 `head = (head + 1) % size`，相当于把队首“向右移”，原来的元素自然被覆盖。  
5. **deleteLast()**  
   - 若空返回 `False`。  
   - 否则 `tail = (tail - 1 + size) % size`（向左循环），相当于把队尾“向左移”。  
6. **getFront / getRear**  
   - 空时返回 `-1`。  
   - 前端是 `data[head]`，后端是 `data[(tail - 1 + size) % size]`（因为 `tail` 指向的是“下一个空位”）。  
7. **isEmpty / isFull**  
   - 前面已经给出判定方式。

这样每一次操作只改动常数个指针或写入一个数组元素，**时间都是 O(1)**，空间仍是 **O(k)**。

#### 代码（Python）  

```python
class MyCircularDeque:
    """
    环形数组实现的循环双端队列
    所有操作均为 O(1) 时间，空间 O(k)
    """
    def __init__(self, k: int):
        # 为了区分「空」和「满」需要多留一个位置
        self.size = k + 1               # 实际数组长度
        self.data = [0] * self.size     # 初始化数组
        self.head = 0                   # 指向队首元素
        self.tail = 0                   # 指向队尾后面的第一个空位

    # ------------------- 判空/判满 -------------------
    def isEmpty(self) -> bool:
        return self.head == self.tail

    def isFull(self) -> bool:
        # tail 的下一个位置恰好是 head，说明已经满了
        return (self.tail + 1) % self.size == self.head

    # ------------------- 插入操作 -------------------
    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        # head 向左移动一个位置（循环）
        self.head = (self.head - 1 + self.size) % self.size
        self.data[self.head] = value
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        self.data[self.tail] = value
        # tail 向右移动一个位置（循环）
        self.tail = (self.tail + 1) % self.size
        return True

    # ------------------- 删除操作 -------------------
    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        # head 向右移动一个位置，原来的元素自然被「抛弃」
        self.head = (self.head + 1) % self.size
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        # tail 向左移动一个位置，实际删除队尾元素
        self.tail = (self.tail - 1 + self.size) % self.size
        return True

    # ------------------- 读取操作 -------------------
    def getFront(self) -> int:
        if self.isEmpty():
            return -1
        return self.data[self.head]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1
        # tail 指向的是「下一个空位」，所以真实的队尾是 tail-1
        return self.data[(self.tail - 1 + self.size) % self.size]
```

#### 复杂度  

- **时间复杂度**  
  - 所有 7 个接口（`insertFront/Last`, `deleteFront/Last`, `getFront/Rear`, `isEmpty`, `isFull`）均只做常数次算术运算和数组读写，**O(1)**。  
  - 与暴力解相比，前端的 `insert`/`delete` 也不再需要搬迁元素，速度提升显著。  

- **空间复杂度**  
  - 使用了长度为 `k+1` 的数组以及两个指针，**O(k)** 的额外空间。  
  - 与暴力解相同，但这里的空间利用率更高（只多留了一个位置用于区分满/空）。

> **对比**：  
> - 暴力解的最坏时间是 **O(k)**（线性），在 `k=1000` 时仍能跑通，但如果 `k` 更大或调用次数很多，性能会明显下降。  
> - 最优解每一步都是常数时间，几乎不受 `k` 大小的影响，是真正符合「设计」题目要求的实现。

---

## 心得  

- **核心技巧**：**循环数组（环形缓冲区）** + **双指针**，通过取模实现“头尾相接”。  
- **适用的题型**（类似思路）  
  1. **设计循环队列**（LeetCode 622）  
  2. **设计循环双端队列**（本题）  
  3. **实现固定大小的缓存（LRU）** 时常用环形缓冲区来管理时间戳或位置。  
- **一句话总结**：**把“满”和“空”用指针位置的相对关系区分开，所有操作只搬指针，就能 O(1) 完成双端队列**。

---

## 反思  

- **第一反应**：直接把 `deque` 当成 Python 列表，用 `insert(0)`、`pop(0)` 实现，代码好写但不够高效。  
- **最容易踩的坑**  
  - **区分空和满**：如果只用 `head == tail` 来判断两者，会导致满时误以为空。解决办法是 **数组多留一个空位**，或额外维护当前元素数量。  
  - **取模运算**：指针越界时要记得加上 `size` 再 `% size`，否则负数取模会出错。  
  - **边界条件**：`getFront/getRear` 在空队列时必须返回 `-1`，而不是访问数组导致错误。  
- **下次遇到同类题**：第一步先问自己“是否可以用固定大小的环形缓冲区把所有操作都转化为指针的移动？”如果答案是“可以”，就直接走环形数组路线。  

祝你玩转数据结构，代码写得顺手，思路更顺畅！