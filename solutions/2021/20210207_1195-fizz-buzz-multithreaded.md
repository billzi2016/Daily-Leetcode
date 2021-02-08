# #1195. Fizz Buzz Multithreaded / Fizz Buzz Multithreaded

> 难度：中等 · 标签：Concurrency · [LeetCode 链接](https://leetcode.com/problems/fizz-buzz-multithreaded/)

---

## 题目（英文原版）

**Description**

You have the four functions:
You are given an instance of the class FizzBuzz that has four functions: fizz, buzz, fizzbuzz and number. The same instance of FizzBuzz will be passed to four different threads:
Modify the given class to output the series [1, 2, "fizz", 4, "buzz", ...] where the ith token (1-indexed) of the series is:
Implement the FizzBuzz class:

**Examples**

**Example 1:**

```
Input: n = 15
Output: [1,2,"fizz",4,"buzz","fizz",7,8,"fizz","buzz",11,"fizz",13,14,"fizzbuzz"]
```

**Example 2:**

```
Input: n = 5
Output: [1,2,"fizz",4,"buzz"]
```

**Constraints**

- 1 <= n <= 50

---

## 题目（中文翻译）

**题目描述**  
你会得到一个 `FizzBuzz` 类的实例，该实例提供四个函数：`fizz`、`buzz`、`fizzbuzz` 和 `number`。同一个 `FizzBuzz` 实例会被分别传入四个不同的线程中。  

请修改（实现）该类，使其能够按照以下规则输出序列 `[1, 2, "fizz", 4, "buzz", ...]`，其中第 *i* 个 token（从 1 开始计数）的取值为：

- 若 *i* 能被 3 整除且不能被 5 整除，输出字符串 `"fizz"`；
- 若 *i* 能被 5 整除且不能被 3 整除，输出字符串 `"buzz"`；
- 若 *i* 同时能被 3 与 5 整除，输出字符串 `"fizzbuzz"`；
- 其它情况下，输出整数 *i* 本身。

每个线程只负责调用一次对应的函数：

- `fizz(printFizz)`：当满足 `"fizz"` 条件时调用 `printFizz.run()`（即打印 `"fizz"`）；
- `buzz(printBuzz)`：当满足 `"buzz"` 条件时调用 `printBuzz.run()`（即打印 `"buzz"`）；
- `fizzbuzz(printFizzBuzz)`：当满足 `"fizzbuzz"` 条件时调用 `printFizzBuzz.run()`（即打印 `"fizzbuzz"`）；
- `number(printNumber)`：当上述三种条件均不满足时调用 `printNumber.accept(i)`（即打印数字 *i*）。

**示例**  

> 示例 1  
> 输入: `n = 15`  
> 输出: `[1,2,"fizz",4,"buzz","fizz",7,8,"fizz","buzz",11,"fizz",13,14,"fizzbuzz"]`

> 示例 2  
> 输入: `n = 5`  
> 输出: `[1,2,"fizz",4,"buzz"]`

**约束条件**  

- `1 <= n <= 50`  

**实现提示**  
- 需要使用线程同步机制（如 `Lock`、`Condition`、`Semaphore`、`CyclicBarrier` 等）确保四个线程按照数字的顺序依次输出。  
- 每个函数内部只能在满足对应条件时才执行打印操作。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**不用多线程**，把 1~n 的数一次遍历完，根据题目规则把每个数映射成对应的输出：

- 能被 3 整除但不能被 5 整除 → `"fizz"`  
- 能被 5 整除但不能被 3 整除 → `"buzz"`  
- 同时能被 3 与 5 整除 → `"fizzbuzz"`  
- 其余情况 → 原数字本身  

这里只需要**一个普通的列表**（list）来保存结果。  
> 类比：把一张纸上的每一行依次填好，就像在字典里查单词，只是这里的“键”是数字，返回的“页码”是对应的字符串或数字本身。

为什么正确？因为遍历顺序恰好是题目要求的“第 i 个 token 对应第 i 个正整数”，每个数只会被检查一次，规则唯一确定。

#### 代码（Python）

```python
def fizzBuzz(n: int):
    """
    暴力单线程实现
    :param n: 需要输出的范围上限（包括 n 本身）
    :return: 按要求的序列，数字保持 int，文字保持 str
    """
    res = []                     # 用列表保存答案
    for i in range(1, n + 1):    # 从 1 遍历到 n（闭区间）
        if i % 15 == 0:          # 同时能被 3 与 5 整除
            res.append("fizzbuzz")
        elif i % 3 == 0:         # 只被 3 整除
            res.append("fizz")
        elif i % 5 == 0:         # 只被 5 整除
            res.append("buzz")
        else:                    # 其它情况直接放数字
            res.append(i)
    return res
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  大白话：我们只看一遍 1~n，每个数做几次“除以 3、5”的检查，和 n 成正比。  
- **空间复杂度：** `O(n)`  
  需要把 n 个结果全部存到列表里，空间随 n 增长。

---

### 2. 最优解（多线程同步）

#### 思路  

**从暴力解出发**，我们已经知道每个数字对应的输出是什么。  
真正的难点在于 **“四个线程分别负责 fizz、buzz、fizzbuzz、number”**，它们必须**按顺序**共同完成这段序列。  

> **慢点在哪里**  
> - 若四个线程随意打印，输出顺序会乱（比如先打印 6 的 `"fizz"` 再打印 5 的 `"buzz"`）。  
> - 需要一种“谁该说话，谁就说”，其它线程必须等到轮到它们时才继续。  

#### 关键技巧：使用 **Condition（条件变量）** 或 **Semaphore（信号量）** 实现“轮流”  

下面以 `Condition` 为例说明思路（思路同样适用于 `Semaphore`）：

1. **共享状态**  
   - `self.cur` 表示当前应该处理的数字（从 1 开始递增）。  
   - `self.n` 是上限。  

2. **Condition 对象**  
   - `self.cv = threading.Condition()` 相当于一个“哨兵”，线程可以在这里**等待**（`wait()`）或**通知**（`notify_all()`）其他线程。  

3. **四个线程的工作函数**  
   - 每个函数都在 `while True` 循环里：
     1. 先获取 `cv` 的锁（`with self.cv:`），确保检查和修改 `self.cur` 是原子操作。  
     2. 判断 `self.cur` 是否已经超过 `n`，如果是则 `break`（所有线程结束）。  
     3. 根据自己的职责检查 `self.cur` 是否满足条件（例如 `self.cur % 3 == 0 and self.cur % 5 != 0` 对应 `fizz`）。  
        - **满足** → 调用传入的回调 `printFizz()`（或 `printBuzz()` 等），随后 `self.cur += 1`，并 `self.cv.notify_all()` 唤醒其他线程。  
        - **不满足** → `self.cv.wait()` 让出锁并进入等待，直到别的线程把 `self.cur` 改成它能处理的值再被唤醒。  

4. **为什么能保证顺序**  
   - `self.cur` 永远递增且只在获得锁的线程里改动。  
   - 当某线程完成一次打印后，立即 `notify_all()`，让所有线程重新检查 `self.cur`。只有满足条件的线程会继续打印，其他的继续 `wait()`。  
   - 这样就形成了“轮到哪个数字，就只有对应的线程能抢到锁并输出”，自然保持了 1→n 的顺序。

> **类比**：把四个人围坐在一张圆桌前，每个人只负责说特定的数字/词。桌子上有一张卡片写着当前该说的数字。只有卡片上的数字符合自己职责的人才能说，其他人只能等卡片被翻到下一页。  

#### 代码（Python）

```python
import threading
from typing import Callable, List

class FizzBuzz:
    """
    多线程版 FizzBuzz
    四个线程分别调用 fizz、buzz、fizzbuzz、number 方法。
    每个方法接收一个无参的打印函数（如 printFizz），负责输出对应的 token。
    """
    def __init__(self, n: int):
        self.n = n                # 上限
        self.cur = 1              # 当前需要处理的数字（从 1 开始）
        self.cv = threading.Condition()   # 条件变量，负责线程间的“等‑叫”

    # ---------- 四个工作函数 ----------
    def fizz(self, printFizz: Callable[[], None]) -> None:
        """
        负责打印 "fizz"
        """
        while True:
            with self.cv:                     # 先获取锁
                while self.cur <= self.n and (self.cur % 3 != 0 or self.cur % 5 == 0):
                    # 不是只被 3 整除的情况，就等
                    self.cv.wait()
                if self.cur > self.n:         # 超出范围，结束
                    self.cv.notify_all()      # 把可能还在等的线程全部叫醒，让它们也退出
                    break
                # 这里一定满足只被 3 整除
                printFizz()
                self.cur += 1                 # 处理完后移动到下一个数字
                self.cv.notify_all()          # 唤醒其它线程

    def buzz(self, printBuzz: Callable[[], None]) -> None:
        """
        负责打印 "buzz"
        """
        while True:
            with self.cv:
                while self.cur <= self.n and (self.cur % 5 != 0 or self.cur % 3 == 0):
                    self.cv.wait()
                if self.cur > self.n:
                    self.cv.notify_all()
                    break
                printBuzz()
                self.cur += 1
                self.cv.notify_all()

    def fizzbuzz(self, printFizzBuzz: Callable[[], None]) -> None:
        """
        负责打印 "fizzbuzz"
        """
        while True:
            with self.cv:
                while self.cur <= self.n and self.cur % 15 != 0:
                    self.cv.wait()
                if self.cur > self.n:
                    self.cv.notify_all()
                    break
                printFizzBuzz()
                self.cur += 1
                self.cv.notify_all()

    def number(self, printNumber: Callable[[int], None]) -> None:
        """
        负责打印普通数字
        """
        while True:
            with self.cv:
                while self.cur <= self.n and (self.cur % 3 == 0 or self.cur % 5 == 0):
                    self.cv.wait()
                if self.cur > self.n:
                    self.cv.notify_all()
                    break
                printNumber(self.cur)
                self.cur += 1
                self.cv.notify_all()


# ---------- 用法示例（可直接运行） ----------
def fizzBuzzMultithreaded(n: int) -> List:
    """
    返回题目要求的序列，内部使用四个线程并发调用 FizzBuzz 的四个方法。
    """
    fb = FizzBuzz(n)
    output: List = []                     # 用来收集所有打印结果

    # 四个打印函数，负责把结果放进 output
    def printFizz():      output.append("fizz")
    def printBuzz():      output.append("buzz")
    def printFizzBuzz():  output.append("fizzbuzz")
    def printNumber(x):   output.append(x)

    # 创建四条线程
    threads = [
        threading.Thread(target=fb.fizz, args=(printFizz,)),
        threading.Thread(target=fb.buzz, args=(printBuzz,)),
        threading.Thread(target=fb.fizzbuzz, args=(printFizzBuzz,)),
        threading.Thread(target=fb.number, args=(printNumber,))
    ]

    # 启动
    for t in threads:
        t.start()
    # 等待全部结束
    for t in threads:
        t.join()

    return output


# 示例
if __name__ == "__main__":
    print(fizzBuzzMultithreaded(15))
    # 输出: [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuzz']
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  每个数字只会被检查一次并打印一次，虽然涉及线程切换，但总体工作量仍然和 `n` 成正比。  
- **空间复杂度：** `O(n)`  
  需要保存最终结果的列表 `output`（长度为 `n`），以及常数级的锁、状态变量等。

相较于暴力解，**时间上没有提升**（因为本质上仍然要遍历 `n`），但**空间和实现难度上更高**，因为我们要额外维护同步状态。  
在 LeetCode 这类并发题目里，关键在于 **正确使用同步原语**，而不是追求更低的时间复杂度。

---

## 心得  

- **核心技巧**：使用 `Condition`（或 `Semaphore`）实现**顺序协作**的多线程同步。  
- **适用场景**：  
  1. 多线程交替输出（如 “奇数偶数交替打印”）。  
  2. 生产者‑消费者模型的简化版（只有一个生产者/消费者循环）。  
  3. 多路复用任务，需要“轮流”访问共享资源的情形。  
- **解题钥匙**：把“当前该干什么”抽象成一个共享变量 + **锁 + 条件等待/通知**，让每条线程只在自己符合条件时才前进。

---

## 反思  

- **第一反应**：把四个函数写成普通的循环，忽略了并发的“顺序”。  
- **最容易踩的坑**：  
  - 忘记在 `while` 循环内部再次判断 `self.cur > n`，导致线程在 `wait()` 后永远卡死。  
  - 条件判断写错（比如 `self.cur % 3 == 0 and self.cur % 5 != 0` 与 `self.cur % 5 == 0` 混用），会导致错误的输出或死锁。  
  - `notify_all()` 必须在修改完 `self.cur` 后立即调用，否则其他线程仍会看到旧的 `cur`，产生竞争。  
- **下次遇到同类题**：第一步先 **确定共享状态**（这里是当前数字），再思考 **哪个线程负责哪个状态**，最后挑选合适的同步工具（`Condition`、`Event`、`Semaphore` 等）来实现“谁该说话，谁就说”。