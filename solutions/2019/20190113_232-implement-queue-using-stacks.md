# #232. 使用栈实现队列 / Implement Queue using Stacks

> 难度：简单 · 标签：Stack、Design、Queue · [LeetCode 链接](https://leetcode.com/problems/implement-queue-using-stacks/)

---

## 题目（英文原版）

**Description**

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty).
Implement the MyQueue class:
Notes:
Follow-up: Can you implement the queue such that each operation is amortized O(1) time complexity? In other words, performing n operations will take overall O(n) time even if one of those operations may take longer.

**Examples**

**Example 1:**

```
Input
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 1, 1, false]

Explanation
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false
```

**Constraints**

- 1 <= x <= 9
- At most 100 calls will be made to push, pop, peek, and empty.
- All the calls to pop and peek are valid.

---

## 题目（中文翻译）

实现一个 **先进先出 (FIFO) 队列**，仅使用两个 **栈（stack）**。实现的队列应支持普通队列的全部功能：`push`、`peek`、`pop` 和 `empty`。

实现 `MyQueue` 类，使其能够：

- `push(x)`: 将元素 `x` 添加到队列的末尾  
- `peek()`: 返回队列头部元素（不移除）  
- `pop()`: 移除并返回队列头部元素  
- `empty()`: 当队列为空时返回 `true`，否则返回 `false`

**示例 1**

```text
Input
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 1, 1, false]
```

**解释**

```java
MyQueue myQueue = new MyQueue();
myQueue.push(1); // 队列变为: [1]
myQueue.push(2); // 队列变为: [1, 2]（最左侧为队列的前端）
myQueue.peek(); // 返回 1
myQueue.pop();  // 返回 1，队列变为 [2]
myQueue.empty(); // 返回 false
```

**约束条件**

- `1 <= x <= 9`
- 最多调用 `push`、`pop`、`peek`、`empty` 共 100 次
- 所有对 `pop` 和 `peek` 的调用均为合法操作

**进阶**

是否可以实现每个操作的摊销时间复杂度为 **O(1)**？换句话说，执行 `n` 次操作的总体时间复杂度为 **O(n)**，即使其中某些单次操作可能耗时更长。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把队列本身当作一个 **列表**（`list`），把新元素 **append** 到列表尾部，取元素时 **pop(0)**（从左边弹出）。  
- `list.append(x)` 就像把东西往队尾放，时间很快（相当于往纸箱里再塞一个盒子）。  
- `list.pop(0)` 相当于从纸箱最前面取出一个盒子，但 Python 必须把后面的所有盒子向前搬一次位置，这一步会比较慢。

虽然这不符合“只能使用两个栈”的要求，但作为**暴力解**可以帮助我们验证功能的正确性。

#### 代码（Python）

```python
class MyQueue:
    def __init__(self):
        # 用一个列表直接模拟队列
        self.buf = []                     # buf[0] 为队首，buf[-1] 为队尾

    def push(self, x: int) -> None:
        """把元素放到队尾，相当于往列表末尾追加"""
        self.buf.append(x)                # O(1)

    def pop(self) -> int:
        """弹出队首元素，需要把所有后面的元素向前搬一次"""
        return self.buf.pop(0)            # O(n) —— 因为要移动 n-1 个元素

    def peek(self) -> int:
        """查看队首元素，但不删除"""
        return self.buf[0]                # O(1)

    def empty(self) -> bool:
        """判断队列是否为空"""
        return len(self.buf) == 0         # O(1)
```

#### 复杂度  

- **时间复杂度**  
  - `push`：`O(1)`（只在列表尾部追加）  
  - `pop`：`O(n)`（需要把后面的所有元素左移）  
  - `peek`、`empty`：`O(1)`  
  整体来看，最坏情况下每次 `pop` 都要线性扫描，和真正的队列相比太慢。  
- **空间复杂度**：`O(n)`，只用一个列表保存全部元素。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **`pop`**：每次都要把所有元素搬动一次。  
要想把每次操作都变快，需要 **避免频繁搬动**。  
这里可以借助 **栈**（后进先出）的特性：  
- 栈 A 只负责 **`push`**（把新元素压进去）。  
- 栈 B 只负责 **`pop/peek`**（从栈顶弹出元素，相当于队首）。  

关键是 **什么时候把 A 的元素倒到 B**：  
- 当 B 为空且需要 `pop`/`peek` 时，**一次性把 A 中所有元素全部弹出再压入 B**。  
- 这样倒转的过程把 **最早进入 A 的元素** 放到 B 的栈顶，正好是队首。  

这种做法的好处是：**每个元素最多只会在两个栈之间移动一次**，因此 **摊销时间** 为 `O(1)`。  
可以把它想象成：  
- 把一堆信件先放进“进货箱”（栈 A），  
- 当需要发信时，把“进货箱”里的信一次性倒进“发货箱”（栈 B），倒完后从“发货箱”取信，直到它空了再倒一次。

#### 代码（Python）

```python
class MyQueue:
    def __init__(self):
        # 两个栈：in_stack 用来存放新压入的元素，out_stack 用来弹出/查看队首
        self.in_stack = []   # 对应栈 A
        self.out_stack = []  # 对应栈 B

    def push(self, x: int) -> None:
        """把元素压入 in_stack，时间始终是 O(1)"""
        self.in_stack.append(x)   # O(1)

    def _transfer(self) -> None:
        """
        当 out_stack 为空时，把 in_stack 中的所有元素倒进 out_stack。
        这一步把元素顺序翻转，使得最早进入的元素出现在 out_stack 顶部。
        每个元素只会被转移一次，摊销下来仍是 O(1)。
        """
        while self.in_stack:
            self.out_stack.append(self.in_stack.pop())   # O(1) 逐个弹出再压入

    def pop(self) -> int:
        """弹出队首元素"""
        if not self.out_stack:          # 如果 out_stack 为空，需要先转移
            self._transfer()
        return self.out_stack.pop()     # O(1)

    def peek(self) -> int:
        """查看队首元素但不弹出"""
        if not self.out_stack:          # 同样需要先保证 out_stack 有元素
            self._transfer()
        return self.out_stack[-1]       # 栈顶即队首，O(1)

    def empty(self) -> bool:
        """当两个栈都为空时，队列为空"""
        return not self.in_stack and not self.out_stack   # O(1)
```

#### 复杂度  

- **时间复杂度**  
  - `push`：`O(1)`，直接压入 `in_stack`。  
  - `pop` / `peek`：摊销 `O(1)`。虽然在某一次 `pop` 时会执行一次完整的转移（最坏 `O(n)`），但每个元素只会被转移一次，所以 **n 次操作总体是 O(n)**。  
  - `empty`：`O(1)`。  
  与暴力解相比，**所有操作的平均耗时都降到了常数级**，大幅提升性能。  

- **空间复杂度**：`O(n)`，两个栈共同保存所有元素，额外空间仅是常数级的指针。

---

## 心得

- 这道题的核心技巧是 **利用两个栈实现队列的“摊销 O(1)”**，通过一次性转移来把先进先出的顺序恢复。  
- 类似的技巧还能用于：  
  1. 用栈实现 **最小栈**（在每个元素里额外存当前最小值）。  
  2. 用两个队列实现 **栈**（入队/出队的逆向操作）。  
- **一句话总结解题钥匙**：*把“只能后进先出”的栈，通过一次性倒置，转化为“先进先出”的队列*。

---

## 反思

- **第一反应**：直接用列表或 `collections.deque` 实现，忽视了只能使用栈的限制。  
- **最容易踩的坑**：  
  - 忘记在 `pop`/`peek` 前检查 `out_stack` 是否为空，导致在空栈上 `pop` 抛异常。  
  - 在转移过程中写成 `while self.out_stack:`（错误的方向），会导致死循环。  
  - 边界情况：连续 `push` 多次后直接 `empty`，应返回 `True`。  
- **下次遇到同类题**：第一步先思考 **“把哪个操作交给哪个数据结构”，再判断是否需要一次性转移或延迟操作**，从而把复杂度压到摊销 `O(1)`。