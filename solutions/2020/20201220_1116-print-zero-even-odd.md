# #1116. Print Zero Even Odd / Print Zero Even Odd

> 难度：中等 · 标签：Concurrency · [LeetCode 链接](https://leetcode.com/problems/print-zero-even-odd/)

---

## 题目（英文原版）

**Description**

You have a function printNumber that can be called with an integer parameter and prints it to the console.
You are given an instance of the class ZeroEvenOdd that has three functions: zero, even, and odd. The same instance of ZeroEvenOdd will be passed to three different threads:
Modify the given class to output the series "010203040506..." where the length of the series must be 2n.
Implement the ZeroEvenOdd class:

**Examples**

**Example 1:**

```
Input: n = 2
Output: "0102"
Explanation: There are three threads being fired asynchronously.
One of them calls zero(), the other calls even(), and the last one calls odd().
"0102" is the correct output.
```

**Example 2:**

```
Input: n = 5
Output: "0102030405"
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

你有一个 **function**（函数）`printNumber`，它接受一个 **integer**（整数）参数并将其打印到 **console**（控制台）上。  
现在给定一个 **class**（类）`ZeroEvenOdd` 的实例，该实例提供了三个 **function**（函数）：`zero`、`even` 和 `odd`。同一个 `ZeroEvenOdd` 实例会被传递给三个不同的 **thread**（线程），每个线程分别调用其中的一个函数。

请修改给定的类，使其能够输出序列 `"010203040506..."`，该序列的长度必须为 `2n`。  

实现 `ZeroEvenOdd` 类，使其满足上述要求。

**示例 1**  
**示例 2**  
**约束条件**  

---

### 示例

#### 示例 1
**输入**: `n = 2`  
**输出**: `"0102"`  
**Explanation**: 有三个线程并发启动。  
- 一个线程调用 `zero()`，  
- 另一个线程调用 `even()`，  
- 第三个线程调用 `odd()`。  
输出 `"0102"` 即为正确结果。

#### 示例 2
**输入**: `n = 5`  
**输出**: `"0102030405"`  

**约束条件**:
- `1 <= n <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的本质是 **让三个线程交替打印**：  

1. `zero()` 负责打印 `0`，它必须在每一次 `even()` 或 `odd()` 打印数字之前先执行。  
2. `even()` 只在要打印的数字是偶数时才执行。  
3. `odd()` 只在要打印的数字是奇数时才执行。  

最直接、最“笨”的想法是 **让三个线程不停循环检查一个共享变量**，看轮到自己打印没有。  
我们可以用一个全局的整数 `state` 表示当前应该执行哪个函数：

| `state` | 含义                     |
|--------|--------------------------|
| 0      | 轮到 `zero()` 打 0       |
| 1      | 轮到 `odd()` 打奇数      |
| 2      | 轮到 `even()` 打偶数      |

每个线程都用 `while` 循环不断读取 `state`，如果 `state` 正好是自己负责的值，就调用 `printNumber` 并把 `state` 改成下一个应该执行的值。  

> **类比**：把 `state` 想成一盏灯的颜色（红、黄、绿），只有灯是红色时，零线程才能走；灯是黄时，奇数线程才能走；灯是绿时，偶数线程才能走。线程之间不需要真正的锁，只是“看灯”。  

**为什么这种办法能得到正确答案**  
只要三个线程严格遵守上表的切换规则，打印顺序就一定是 `0 1 0 2 0 3 …`，因为每一次 `zero` 打完 0，`state` 必然被改成 `1`（奇数）或 `2`（偶数），而对应的数字线程在打印完后又把 `state` 设回 `0`，于是循环往复。

**缺点**：  
- 线程不停轮询 `state`，会占用大量 CPU（类似“忙等”）。  
- 没有使用任何同步原语（锁、信号量），在真实的并发环境里会出现“可见性”问题——一个线程改了 `state`，别的线程不一定马上看到。

#### 代码（Python）

```python
import threading
import time
from typing import Callable

class ZeroEvenOdd:
    def __init__(self, n: int):
        self.n = n
        self.state = 0          # 0: zero, 1: odd, 2: even
        self.current = 1        # 下一个要打印的数字（从 1 开始）

    # 这里的 printNumber 只负责打印，不换行
    def zero(self, printNumber: Callable[[int], None]) -> None:
        while True:
            if self.state == 0:                     # 轮到 zero 打 0
                if self.current > self.n:           # 已经打印完全部数字
                    return
                printNumber(0)
                # 根据下一个数字的奇偶性决定下一个状态
                self.state = 1 if self.current % 2 else 2
            else:
                time.sleep(0.001)   # 小睡一下，防止 CPU 飙到 100%

    def odd(self, printNumber: Callable[[int], None]) -> None:
        while True:
            if self.state == 1:                     # 轮到 odd 打奇数
                if self.current > self.n:
                    return
                printNumber(self.current)
                self.current += 1
                self.state = 0                     # 打完后让 zero 接着打印 0
            else:
                time.sleep(0.001)

    def even(self, printNumber: Callable[[int], None]) -> None:
        while True:
            if self.state == 2:                     # 轮到 even 打偶数
                if self.current > self.n:
                    return
                printNumber(self.current)
                self.current += 1
                self.state = 0
            else:
                time.sleep(0.001)

# ------------------- 测试 -------------------
def test(n: int):
    zeo = ZeroEvenOdd(n)
    out = []
    def printer(x):
        out.append(str(x))

    # 创建三条线程
    t_zero = threading.Thread(target=zeo.zero, args=(printer,))
    t_odd  = threading.Thread(target=zeo.odd,  args=(printer,))
    t_even = threading.Thread(target=zeo.even, args=(printer,))

    # 启动
    t_zero.start(); t_odd.start(); t_even.start()
    # 等待结束
    t_zero.join(); t_odd.join(); t_even.join()
    print(''.join(out))

test(5)   # 期望输出 0102030405
```

> **代码注释**  
- `self.state` 用来标记当前轮到哪个线程。  
- 每次 `zero` 打完 `0` 后，根据 `self.current` 的奇偶性决定下一个状态是 `1`（odd）还是 `2`（even）。  
- 为了防止忙等导致 CPU 占用过高，使用了 `time.sleep(0.001)`（实际生产代码不建议这样做）。

#### 复杂度

- **时间复杂度**：`O(n)`  
  虽然每个线程里都有 `while True` 循环，但每一次真正的打印只会执行 `n` 次（`zero` 打 `n` 次，`odd/even` 合计也打 `n` 次），所以总体的有效工作量是线性的。  
- **空间复杂度**：`O(1)`  
  只用了几个整数变量 (`state`, `current`) 来保存状态，和 `n` 的大小无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **忙等**：线程不停地检查 `state`，浪费 CPU。  
在并发编程里，**“让线程在需要时才被唤醒”** 才是高效的做法。Python 标准库提供了几种同步原语：

| 同步原语 | 类比 | 作用 |
|---------|------|------|
| `Lock`（互斥锁） | 锁住门 | 同一时刻只能有一个线程进入临界区 |
| `Condition`（条件变量） | 等红灯，绿灯时才能跑 | 线程可以 **等待** 某个条件成立，另一线程 **通知** 它继续执行 |
| `Semaphore`（信号量） | 限流闸门 | 维护一个计数，计数 > 0 时线程可以通过，随后计数 -1；`release` 会把计数 +1 并可能唤醒等待的线程 |

这里最自然的实现是 **使用 `Semaphore`**，因为我们只需要“允许”或“阻塞”某个线程，而不需要复杂的状态判断。  

我们准备三个信号量：

| 信号量 | 初始值 | 作用 |
|--------|--------|------|
| `zero_sem` | 1 | 初始时让 `zero` 线程先执行（因为要先打印 `0`） |
| `odd_sem`  | 0 | 开始时阻塞 `odd` 线程，等 `zero` 打完 0 并且下一个数字是奇数时再放行 |
| `even_sem` | 0 | 同理，等 `zero` 打完 0 并且下一个数字是偶数时再放行 |

执行流程如下（以打印 `0 1 0 2 …` 为例）：

1. **`zero` 线程** 获得 `zero_sem`（计数为 1），打印 `0`。  
2. 根据 `current` 的奇偶性，`zero` 调用 `odd_sem.release()` 或 `even_sem.release()`，把对应信号量的计数加 1，**唤醒** 相应的 `odd/even` 线程。  
3. **`odd`（或 `even`）线程** 获得自己的信号量，打印当前数字 `current`，`current += 1`，随后调用 `zero_sem.release()`，让 `zero` 再次有机会打印下一个 `0`。  
4. 循环上述步骤，直到 `current > n`。

> **类比**：把三个信号量想成三盏红绿灯。只有拿到绿灯的线程才能前进。`zero` 的灯最开始是绿的，打印完后把对应的 `odd` 或 `even` 灯点绿，而自己把灯关红，等对方完成后再把自己的灯点绿。这样每次只有一条路是通的，天然避免了竞争。

#### 代码（Python）

```python
import threading
from typing import Callable

class ZeroEvenOdd:
    """
    使用三个 Semaphore 实现线程有序交替打印
    """
    def __init__(self, n: int):
        self.n = n
        self.current = 1               # 下一个要打印的数字（从 1 开始）

        # zero 先可以执行，odd/even 先阻塞
        self.zero_sem = threading.Semaphore(1)
        self.odd_sem  = threading.Semaphore(0)
        self.even_sem = threading.Semaphore(0)

    def zero(self, printNumber: Callable[[int], None]) -> None:
        for _ in range(self.n):
            self.zero_sem.acquire()          # 等待自己被放行
            printNumber(0)                    # 打印 0
            # 根据即将要打印的数字奇偶性，放行相应的线程
            if self.current % 2:               # 奇数
                self.odd_sem.release()
            else:                               # 偶数
                self.even_sem.release()

    def odd(self, printNumber: Callable[[int], None]) -> None:
        # 只需要打印奇数，次数为 n//2（向上取整）
        for _ in range((self.n + 1) // 2):
            self.odd_sem.acquire()            # 等待 zero 让出
            printNumber(self.current)         # 打印奇数
            self.current += 1                 # 递增到下一个数字
            self.zero_sem.release()           # 让 zero 再次打印 0

    def even(self, printNumber: Callable[[int], None]) -> None:
        # 只需要打印偶数，次数为 n//2（向下取整）
        for _ in range(self.n // 2):
            self.even_sem.acquire()           # 等待 zero 让出
            printNumber(self.current)         # 打印偶数
            self.current += 1
            self.zero_sem.release()           # 让 zero 再次打印 0

# ------------------- 测试 -------------------
def test(n: int):
    zeo = ZeroEvenOdd(n)
    out = []
    def printer(x):
        out.append(str(x))

    # 创建并启动三条线程
    t_zero = threading.Thread(target=zeo.zero, args=(printer,))
    t_odd  = threading.Thread(target=zeo.odd,  args=(printer,))
    t_even = threading.Thread(target=zeo.even, args=(printer,))

    t_zero.start(); t_odd.start(); t_even.start()
    t_zero.join(); t_odd.join(); t_even.join()

    print(''.join(out))

test(5)   # 输出 0102030405
```

> **关键行中文注释**  
- `self.zero_sem.acquire()`：`zero` 线程只有在自己对应的信号量计数大于 0 时才会继续（即被“放行”）。  
- `self.odd_sem.release()` / `self.even_sem.release()`：把对应信号量的计数加 1，**唤醒** 正在等待的 `odd` 或 `even` 线程。  
- `self.zero_sem.release()`：奇数/偶数线程打印完后，把 `zero` 的信号量恢复为 1，让它可以打印下一个 `0`。

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个数字只打印一次，`zero`、`odd`、`even` 三个循环的总迭代次数正好是 `2n`（即 2n 次 `printNumber` 调用），没有额外的循环或等待时间。相比暴力解的“忙等”，这里线程在不该执行时会 **阻塞**，CPU 真正消耗的仍然是 `O(n)`。

- **空间复杂度**：`O(1)`  
  只用了三个整数计数的信号量和几个普通变量，和 `n` 大小无关。  

---

## 心得

- **核心技巧**：利用 **信号量 (Semaphore)** 实现线程的“交叉放行”。  
- **适用的题型**  
  1. “交替打印”系列，如 `FooBar`, `PrintFooBarAlternately`。  
  2. “有序执行”系列，如 `PrintInOrder`（三个函数必须按顺序执行）。  
  3. “多线程同步”场景，如生产者‑消费者问题的简化版。  
- **一句话总结解题钥匙**：**把“谁该跑、谁该等”抽象成信号量的计数，让线程只在获得绿灯时才前进**。

---

## 反思

- **第一反应**：看到三个函数就想到用共享变量配合 `while` 循环轮询。  
- **最容易踩的坑**  
  - **忙等导致 CPU 飙升**：没有同步原语时需要 `sleep`，但仍然不可靠。  
  - **计数错误**：`odd` 与 `even` 的循环次数必须分别对应奇数/偶数的个数，容易写错导致死锁。  
  - **死锁**：若忘记在 `odd/even` 结束后 `release` `zero_sem`，`zero` 永远阻塞，程序卡住。  
- **下次遇到同类题**：第一步先思考 **“哪几条线程需要互相交替”，然后用 **信号量/条件变量** 把交替顺序显式化，而不是靠轮询实现。这样既高效又易于证明正确性。