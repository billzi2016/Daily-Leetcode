# #225. 用队列实现栈 / Implement Stack using Queues

> 难度：简单 · 标签：Stack、Design、Queue · [LeetCode 链接](https://leetcode.com/problems/implement-stack-using-queues/)

---

## 题目（英文原版）

**Description**

Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (push, top, pop, and empty).
Implement the MyStack class:
Notes:
Follow-up: Can you implement the stack using only one queue?

**Examples**

**Example 1:**

```
Input
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
Output
[null, null, null, 2, 2, false]

Explanation
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top(); // return 2
myStack.pop(); // return 2
myStack.empty(); // return False
```

**Constraints**

- 1 <= x <= 9
- At most 100 calls will be made to push, pop, top, and empty.
- All the calls to pop and top are valid.

---

## 题目（中文翻译）

**题目描述**  
使用仅两个队列（queue）实现一个后进先出（last‑in‑first‑out，LIFO）栈。实现的栈需要支持普通栈的全部操作：`push`、`top`、`pop` 与 `empty`。

**实现要求**  
实现 `MyStack` 类，使其具备以下方法：

- `void push(int x)`: 将元素 `x` 压入栈中。  
- `int top()`: 返回栈顶元素。  
- `int pop()`: 删除并返回栈顶元素。  
- `boolean empty()`: 当栈为空时返回 `true`，否则返回 `false`。

**进阶**  
你能仅使用一个队列（queue）来实现该栈吗？

**示例**  

```
Input
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]

Output
[null, null, null, 2, 2, false]

Explanation
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top();   // 返回 2
myStack.pop();   // 返回 2
myStack.empty(); // 返回 false
```

**约束条件**  

- `1 <= x <= 10^9`（题目原始约束中可能为 `1 <= x <= 9`，此处保留原始含义）  
- 最多会调用 `push`、`pop`、`top`、`empty` 共计 100 次。  
- 所有对 `pop` 与 `top` 的调用均是合法的（即在栈非空的情况下进行）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把栈的所有操作全部交给两个普通的队列来完成**。  
我们可以把 `queue1` 当作“主队列”，`queue2` 当作“暂存队列”。  
- **push**：把新元素直接放进 `queue1`（队列的 `append` 就像往排队的队尾加人）。
- **top / pop**：因为队列只能从队首取元素，而栈需要从队尾取元素。于是我们把 `queue1` 中除了最后一个元素之外的所有元素，逐个 `popleft`（相当于让前面的人一个一个走出队列），依次放进 `queue2`。此时 `queue1` 只剩下最后加入的元素，它正好是栈顶。  
  - `top` 只需要把这个元素 peek 出来，然后再把它放回 `queue2`。  
  - `pop` 直接把这个元素弹出（不放回），相当于把栈顶弹走。  
- 最后把 `queue2` 的内容整体搬回 `queue1`，为下一次操作做准备。

> **类比**：想象有两条排队的队伍，想要得到最后一个排进去的人（栈顶），只能让前面的人一个一个走到另一条队伍，最后一个人自然就站在前面了。

这种做法虽然每一步都能得到正确答案，但每次 `top`、`pop` 都要把几乎所有元素搬来搬去，显然很慢。

#### 代码（Python）

```python
from collections import deque

class MyStack:
    def __init__(self):
        # 两个普通队列，用 deque 实现（deque 的 popleft 是 O(1)）
        self.q1 = deque()
        self.q2 = deque()

    # 入栈：直接把元素放到 q1 的尾部
    def push(self, x: int) -> None:
        self.q1.append(x)          # 类似把新顾客加入排队的末尾

    # 取栈顶元素（不弹出）
    def top(self) -> int:
        # 把 q1 除最后一个元素外全部移到 q2
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        # 此时 q1 只剩下栈顶元素
        top_elem = self.q1[0]      # 直接读取队首元素，即栈顶
        # 把栈顶元素也搬到 q2，保持结构不变
        self.q2.append(self.q1.popleft())
        # 交换 q1、q2 的引用，恢复 “主队列”
        self.q1, self.q2 = self.q2, self.q1
        return top_elem

    # 弹出栈顶元素并返回
    def pop(self) -> int:
        while len(self.q1) > 1:
            self.q2.append(self.q1.popleft())
        # 现在 q1 只剩下栈顶元素，直接弹出
        pop_elem = self.q1.popleft()
        # 交换 q1、q2，准备下次操作
        self.q1, self.q2 = self.q2, self.q1
        return pop_elem

    # 判断栈是否为空
    def empty(self) -> bool:
        return not self.q1          # q1 为空即栈为空
```

#### 复杂度

- **时间复杂度**  
  - `push`：`O(1)`，只做一次 `append`。  
  - `top`、`pop`：最坏情况需要把除栈顶外的全部元素从 `q1` 移到 `q2`，这相当于遍历一次所有元素，记作 **`O(n)`**（n 为当前栈的大小）。  
  - `empty`：`O(1)`，只看一下队列是否为空。

  用大白话说，`O(n)` 就是“跟元素个数成正比”，如果栈里有 1000 个数，这两个操作大概要跑 1000 次基本操作。

- **空间复杂度**  
  - 只用了两个队列保存所有元素，额外空间是 `O(n)`（n 为栈中元素数），没有额外的“大箱子”。

---

### 2. 最优解

#### 思路  

从上面的暴力解可以看到，**瓶颈在于每次 `top` / `pop` 都要把几乎所有元素搬来搬去**。  
如果我们把“搬运”工作提前到 `push` 时完成，就能把 `pop`、`top` 变成 `O(1)` 的操作。  

**核心思路**：在每次 `push` 时，把新元素放到 `q2`，然后把 `q1` 中的全部旧元素一次性全部搬到 `q2`，最后把 `q2` 换成新的 `q1`。这样，新元素会一直位于 `q1` 的队首（因为所有旧元素都排在它后面），而栈顶正好对应队首，**弹出或查看栈顶只需要一次 `popleft`**。

实现细节：

1. `push(x)`  
   - 把 `x` 放进空的 `q2`。  
   - 把 `q1` 中的所有元素逐个 `popleft` 并 `append` 到 `q2`（相当于把旧的排队全部搬到新队列的后面）。  
   - 交换 `q1` 与 `q2` 的引用，保持 `q1` 为主队列。  
   - 这样 `q1` 的队首就是最新压入的元素，即栈顶。

2. `pop()` / `top()`  
   - 直接对 `q1` 做 `popleft`（弹出）或取 `q1[0]`（查看），时间都是 `O(1)`。

3. `empty()` 同样检查 `q1` 是否为空。

> **类比**：把每次新来的客人先放到一条新队伍的前面，然后把原来的所有客人依次跟在后面。于是新客人永远站在队首，想要叫他出来只需要“一声令下”，不需要再搬人。

#### 代码（Python）

```python
from collections import deque

class MyStack:
    def __init__(self):
        # 只需要两个队列，q1 永远保存“真实栈”的顺序
        self.q1 = deque()
        self.q2 = deque()

    # 入栈：把新元素放到 q2，然后把 q1 全部搬过去，最后让 q2 成为新的 q1
    def push(self, x: int) -> None:
        self.q2.append(x)               # 新元素先进入空的 q2（相当于新客人先站好）
        # 把旧的所有元素搬到 q2 的后面
        while self.q1:
            self.q2.append(self.q1.popleft())
        # 交换 q1、q2 的角色
        self.q1, self.q2 = self.q2, self.q1

    # 返回栈顶元素但不弹出
    def top(self) -> int:
        return self.q1[0]               # 队首就是栈顶，直接读取

    # 弹出栈顶元素并返回
    def pop(self) -> int:
        return self.q1.popleft()        # 直接从队首弹出

    # 判断栈是否为空
    def empty(self) -> bool:
        return not self.q1
```

#### 复杂度

- **时间复杂度**  
  - `push`：需要把旧的全部元素搬一次，最坏是 `O(n)`（n 为当前栈大小）。  
  - `pop`、`top`：只做一次 `popleft` 或一次下标访问，**`O(1)`**（常数时间），和元素个数无关。  
  - `empty`：`O(1)`。

  与暴力解相比，**我们把“慢的”操作从每次查询/弹出转移到每次插入**，这在实际使用中更符合栈的使用场景（通常 `push`、`pop` 交替出现，查询栈顶也很频繁）。

- **空间复杂度**  
  - 同样只用了两个队列保存所有元素，**`O(n)`** 的额外空间。

---

## 心得

- **核心技巧**：把队列的“只能从头取”限制，通过在 `push` 时把旧元素全部倒进新队列，让最新元素永远处在队首，从而实现栈的 LIFO 行为。
- **适用场景**：  
  1. 需要用 **队列实现栈**（本题）。  
  2. 用 **队列实现循环缓冲**（把新元素放在队首或队尾的思路类似）。  
  3. 需要把 **“倒序”** 操作交给队列完成的题目（如 “用队列实现队列的逆序”）。
- **一句话总结**：**让最新元素永远站在队首，弹出和查看只需一次 O(1) 操作**。

---

## 反思

- **第一反应**：直接把两个普通队列当作“栈的两只手”，每次 `pop`、`top` 时把元素搬来搬去——这就是最直观的暴力实现。
- **最容易踩的坑**  
  - 忘记在 `push` 完成后交换 `q1`、`q2`，导致后续操作仍在旧队列上执行。  
  - `top` 实现时误把元素弹出而不是仅仅读取。  
  - 边界情况：空栈调用 `pop`/`top`（题目保证不会出现，但实际写代码时仍需防御性检查）。
- **下次遇到同类题**：第一步先思考 **“哪个操作最频繁？”**，把 **最耗时的工作提前到不常用的操作**（本例中把搬运工作提前到 `push`），再利用队列的特性设计“把最新元素放在队首”的策略。