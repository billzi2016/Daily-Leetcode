# #1226. **哲学家就餐问题** / The Dining Philosophers

> 难度：中等 · 标签：Concurrency · [LeetCode 链接](https://leetcode.com/problems/the-dining-philosophers/)

---

## 题目（英文原版）

**Description**

Five silent philosophers sit at a round table with bowls of spaghetti. Forks are placed between each pair of adjacent philosophers.
Each philosopher must alternately think and eat. However, a philosopher can only eat spaghetti when they have both left and right forks. Each fork can be held by only one philosopher and so a philosopher can use the fork only if it is not being used by another philosopher. After an individual philosopher finishes eating, they need to put down both forks so that the forks become available to others. A philosopher can take the fork on their right or the one on their left as they become available, but cannot start eating before getting both forks.
Eating is not limited by the remaining amounts of spaghetti or stomach space; an infinite supply and an infinite demand are assumed.
Design a discipline of behaviour (a concurrent algorithm) such that no philosopher will starve; i.e., each can forever continue to alternate between eating and thinking, assuming that no philosopher can know when others may want to eat or think.
The problem statement and the image above are taken from wikipedia.org
The philosophers' ids are numbered from 0 to 4 in a clockwise order. Implement the function void wantsToEat(philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork) where:
Five threads, each representing a philosopher, will simultaneously use one object of your class to simulate the process. The function may be called for the same philosopher more than once, even before the last call ends.

**Examples**

**Example 1:**

```
Input: n = 1
Output: [[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],[4,0,3],[4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],[0,2,2],[1,2,1],[1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],[1,2,2]]
Explanation:
n is the number of times each philosopher will call the function.
The output array describes the calls you made to the functions controlling the forks and the eat function, its format is:
output[i] = [a, b, c] (three integers)
- a is the id of a philosopher.
- b specifies the fork: {1 : left, 2 : right}.
- c specifies the operation: {1 : pick, 2 : put, 3 : eat}.
```

**Constraints**

- 1 <= n <= 60

---

## 题目（中文翻译）

五位沉默的哲学家围坐在圆形餐桌旁，桌上有意大利面。每对相邻的哲学家之间放置一把叉子。  
每位哲学家必须交替进行思考（think）和进餐（eat）。然而，只有在同时拥有左侧和右侧的叉子时，哲学家才能进食。每把叉子同一时刻只能被一位哲学家持有，因而只有在叉子未被他人占用时才能拿起。哲学家进餐结束后，需要把两把叉子都放下，使其重新对其他人可用。哲学家可以在叉子可用时先拿起右边的叉子或左边的叉子，但只有在两把叉子都到手后才能开始进食。  

进食不受意大利面的剩余量或胃容量的限制；这里假设食物无限、需求无限。  

请设计一种行为规范（并发算法），使得没有哲学家会饿死；即在没有哲学家能够知道其他人何时想进食或思考的前提下，每位哲学家都能永远交替进行进食和思考。

哲学家的编号为 **0 到 4**，按顺时针方向排列。实现函数  

```cpp
void wantsToEat(int philosopher,
                function<void()> pickLeftFork,
                function<void()> pickRightFork,
                function<void()> eat,
                function<void()> putLeftFork,
                function<void()> putRightFork);
```

五个线程分别代表五位哲学家，它们会同时使用同一个类的实例来模拟上述过程。对同一哲学家的 `wantsToEat` 可能被多次调用，甚至在上一次调用尚未结束时再次调用。

**示例 1**

```text
Input: n = 1
Output: [[4,2,1],[4,1,1],[0,1,1],[2,2,1],[2,1,1],[2,0,3],[2,1,2],[2,2,2],
         [4,0,3],[4,1,2],[0,2,1],[4,2,2],[3,2,1],[3,1,1],[0,0,3],[0,1,2],
         [0,2,2],[1,2,1],[1,1,1],[3,0,3],[3,1,2],[3,2,2],[1,0,3],[1,1,2],
         [1,2,2]]
Explanation:
n 表示每位哲学家调用函数的次数。输出数组描述了你对控制叉子和进食的函数所做的调用顺序。
```

**约束条件**

- `1 <= n <= 60`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 叉子都看成“一把全局的锁”。  
当某个哲学家想吃饭时：

1. 先把这把全局锁 **全部占用**（相当于把所有叉子都锁住）。  
2. 然后依次调用 `pickLeftFork`、`pickRightFork`、`eat`、`putLeftFork`、`putRightFork`。  
3. 最后释放全局锁，其他哲学家才能继续执行。

> **类比**：全局锁就像一本《餐桌使用手册》，只有拿到手册的人才能动叉子。这样所有人都排队，互不干扰，自然不会出现 **死锁**（两个哲学家相互等对方的叉子而卡住）。

**为什么正确**  
- 只有拿到全局锁的哲学家才能执行拿叉子、吃饭、放叉子的完整流程。  
- 其它哲学家在全局锁未释放前只能等待，保证了 **互斥**（同一时间最多只有一个人在吃）。  
- 互斥 + 每个哲学家最终都会释放锁 ⇒ **不会饿死**（只要调度公平，所有人都会轮到）。

**时间/空间复杂度**  
- 每次吃饭都要 **抢一次全局锁**，锁的获取和释放都是 **O(1)** 的操作。  
- 但是因为只能有 **一个哲学家** 同时吃，整体执行时间是 **串行** 的：如果每个哲学家要吃 `n` 次，总共需要 `5 * n` 次完整的吃饭流程，即 **O(n)**（对单个哲学家而言）但 **并行度为 1**。  
- 空间上只需要保存一个 `Lock` 对象，**O(1)**。

#### 代码（Python）

```python
import threading
from typing import Callable

class DiningPhilosophers:
    def __init__(self):
        # 只要这把锁，谁都可以独占整个餐桌
        self.table_lock = threading.Lock()

    def wantsToEat(
        self,
        philosopher: int,
        pickLeftFork: Callable[[int], None],
        pickRightFork: Callable[[int], None],
        eat: Callable[[int], None],
        putLeftFork: Callable[[int], None],
        putRightFork: Callable[[int], None],
    ) -> None:
        # 抢全局锁，确保一次只有一个人在吃
        with self.table_lock:                     # <-- 关键：全局互斥
            # 按题目要求的顺序调用回调函数
            pickLeftFork(philosopher)             # 拿左叉
            pickRightFork(philosopher)            # 拿右叉
            eat(philosopher)                      # 吃饭
            putLeftFork(philosopher)              # 放左叉
            putRightFork(philosopher)             # 放右叉
```

> **关键行中文注释** 已在代码中标出。`with` 语句会在代码块结束时自动释放锁，即使中间抛异常也能保证叉子最终被放回。

#### 复杂度

- **时间复杂度**：`O(1)`（每次吃饭只做常数次锁操作），但因为只能串行进行，整体运行时间与并发数呈线性关系。  
- **空间复杂度**：`O(1)`，只保存一把 `Lock`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“只能有一个哲学家同时吃”**，这极大浪费了并发资源。  
真正的难点是 **防止死锁**：如果每个哲学家先拿左叉，再等右叉，可能出现环形等待（A 等 B，B 等 C … Z 等 A），导致所有人永远卡住。

要把 **并发度提升到 4**（最多有 4 位哲学家可以同时吃，因为任意 5 位必有两位相邻，至少有一把叉子被共享），常用的两种思路：

1. **资源层级（编号顺序）**  
   - 给每把叉子编号 0~4（左叉 = i，右叉 = (i+1)%5）。  
   - 哲学家总是 **先拿编号小的叉子，再拿编号大的叉子**。  
   - 这样不可能出现环形等待，因为所有的等待链都是沿着编号递增的方向，最终会在最大编号的叉子处终止。  

2. **限制并发人数（信号量）**  
   - 使用一个计数信号量 `sem = threading.Semaphore(4)`，最多允许 4 位哲学家同时进入 “拿叉子” 阶段。  
   - 当 5 位都想吃时，必定有至少一位被阻塞，因而不会出现 5 条相互等待的环。  
   - 该方案实现更简洁，且不需要对叉子编号做排序。

下面给出 **信号量 + 每把叉子的独立锁** 的实现（这是 LeetCode 官方推荐的思路），并配以细致的解释。

**关键概念解释**  

- **Lock（互斥锁）**：就像一本只能被一个人同时打开的“叉子使用手册”。只有持有锁的人才能使用对应的叉子。  
- **Semaphore（信号量）**：可以把它想象成“餐厅的座位”。`Semaphore(4)` 表示餐厅最多只能坐 4 桌客人，想进来的第 5 桌只能等座位空出来。这里的“座位”是 “同时尝试拿叉子的哲学家数量”。  

**为什么不会死锁**  
- 当已经有 4 位哲学家持有左叉（或右叉）时，第 5 位哲学家在 `sem.acquire()` 处被阻塞，**不会再去抢叉子**，于是不会出现 5 条互相等待的环。  
- 被阻塞的哲学家只会在已有哲学家 **全部吃完并释放叉子后**（即 `sem.release()`）才继续尝试，保证了系统始终能前进。

#### 代码（Python）

```python
import threading
from typing import Callable

class DiningPhilosophers:
    def __init__(self):
        # 每把叉子一把独立的锁，编号 0~4
        self.forks = [threading.Lock() for _ in range(5)]
        # 同时最多只有 4 位哲学家可以尝试拿叉子，防止环形等待
        self.sema = threading.Semaphore(4)

    def wantsToEat(
        self,
        philosopher: int,
        pickLeftFork: Callable[[int], None],
        pickRightFork: Callable[[int], None],
        eat: Callable[[int], None],
        putLeftFork: Callable[[int], None],
        putRightFork: Callable[[int], None],
    ) -> None:
        # 1. 先申请“座位”，最多 4 人同时进入
        self.sema.acquire()                       # <-- 关键：限制并发人数

        left = philosopher                         # 左叉的编号
        right = (philosopher + 1) % 5               # 右叉的编号（环形）

        # 2. 按照编号顺序锁叉子，防止出现“左先锁、右后锁”导致的环形等待
        first, second = (left, right) if left < right else (right, left)

        # 3. 拿第一把叉子
        with self.forks[first]:
            if first == left:
                pickLeftFork(philosopher)          # 如果是左叉，调用左叉回调
            else:
                pickRightFork(philosopher)         # 否则是右叉

            # 4. 再拿第二把叉子
            with self.forks[second]:
                if second == left:
                    pickLeftFork(philosopher)
                else:
                    pickRightFork(philosopher)

                # 5. 拿到两把叉子后吃饭
                eat(philosopher)

                # 6. 放下第二把叉子
                if second == left:
                    putLeftFork(philosopher)
                else:
                    putRightFork(philosopher)

            # 7. 放下第一把叉子（离开 with 块自动释放锁）
            if first == left:
                putLeftFork(philosopher)
            else:
                putRightFork(philosopher)

        # 8. 释放“座位”，让其他哲学家有机会进入
        self.sema.release()                        # <-- 关键：恢复并发资格
```

**代码要点解读**  

1. `self.sema.acquire()`：把自己排进最多 4 人的“吃饭队列”。  
2. `first, second = (left, right) if left < right else (right, left)`：**先锁编号小的叉子**，再锁大的，保证所有哲学家的锁顺序一致，杜绝环形等待。  
3. `with self.forks[first]: … with self.forks[second]:`：使用 `with` 自动加锁、解锁，避免忘记 `release`。  
4. 在每个 `with` 块内部，根据是左叉还是右叉调用对应的回调函数。  
5. 最后 `self.sema.release()` 把座位归还，使被阻塞的哲学家可以继续尝试。

#### 复杂度

- **时间复杂度**：每位哲学家一次吃饭只涉及常数次锁/解锁和函数调用，仍是 **O(1)**。相比暴力解，**并发度提升到最多 4**，整体执行时间约为 `5/4` 倍的串行时间，明显更快。  
- **空间复杂度**：需要保存 5 把叉子的锁 + 1 个信号量，**O(1)**（固定常数空间）。

---

## 心得

- **核心技巧**：**信号量限制并发人数 + 按编号顺序加锁**（资源层级法）防止死锁。  
- **适用的题型**  
  1. 经典的 **Dining Philosophers**（本题）。  
  2. 多线程的 **读者写者问题**（需要限制写者数量或使用资源层级）。  
  3. **生产者‑消费者** 中对缓冲区的互斥访问（使用信号量控制可并发的生产者/消费者数量）。  
- **一句话总结解题钥匙**：*先限制进入临界区的线程数，再保证所有线程获取锁的顺序统一，就能彻底避免死锁并提升并发度。*

---

## 反思

- **第一反应**：直接给每把叉子加锁，甚至用一把全局锁把所有人串起来。这样可以保证安全，但并发度太低。  
- **最容易踩的坑**  
  - **死锁**：如果每个人都先左后右，5 条等待链会形成环。  
  - **忘记释放锁**：手写 `lock.acquire(); …; lock.release()` 时容易遗漏 `release`，导致后面的线程永远卡住。  
  - **信号量泄漏**：`acquire` 成功后若因异常未执行 `release`，会导致系统永久卡死。使用 `with` 或 `try…finally` 可以避免。  
- **下次类似题的第一步**：先问自己“**有没有可能形成环形等待**”。如果答案是“是”，就考虑 **限制并发人数**（信号量）或 **统一锁的获取顺序**（资源层级），再去实现细节。