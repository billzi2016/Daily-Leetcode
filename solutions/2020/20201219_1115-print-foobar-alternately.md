# #1115. Print FooBar Alternately / Print FooBar Alternately

> 难度：中等 · 标签：Concurrency · [LeetCode 链接](https://leetcode.com/problems/print-foobar-alternately/)

---

## 题目（英文原版）

**Description**

Suppose you are given the following code:
The same instance of FooBar will be passed to two different threads:
Modify the given program to output "foobar" n times.

**Examples**

**Example 1:**

```
class FooBar {
  public void foo() {
    for (int i = 0; i < n; i++) {
      print("foo");
    }
  }

  public void bar() {
    for (int i = 0; i < n; i++) {
      print("bar");
    }
  }
}
```

**Example 2:**

```
Input: n = 1
Output: "foobar"
Explanation: There are two threads being fired asynchronously. One of them calls foo(), while the other calls bar().
"foobar" is being output 1 time.
```

**Example 3:**

```
Input: n = 2
Output: "foobarfoobar"
Explanation: "foobar" is being output 2 times.
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

假设你得到如下代码：

同一个 **FooBar** 实例会被传递给两个不同的 **线程（thread）**。  
请修改给定的程序，使其交替输出 `"foobar"` 共 **n** 次。

## 示例

### 示例 1

```java
class FooBar {
  public void foo() {
    for (int i = 0; i < n; i++) {
      print("foo");
    }
  }

  public void bar() {
    for (int i = 0; i < n; i++) {
      print("bar");
    }
  }
}
```

### 示例 2

**输入**: `n = 1`  
**输出**: `"foobar"`  

**解释**: 有两个线程异步启动。一个线程调用 `foo()`，另一个线程调用 `bar()`。  
`"foobar"` 被输出 1 次。

### 示例 3

**输入**: `n = 2`  
**输出**: `"foobarfoobar"`  

**解释**: `"foobar"` 被输出 2 次。

## 约束

- `1 <= n <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**不使用任何并发工具**，把两个函数 `foo` 和 `bar` 按顺序直接写在同一个线程里：

```python
for i in range(n):
    print("foo", end='')
    print("bar", end='')
```

- **用到的数据结构**：这里只用了最基本的循环（`for`），相当于在生活中一次一次把“foo”和“bar”这两个积木块放到一条生产线上。
- **为什么正确**：因为题目只要求最终的输出顺序是 `foobar` 重复 `n` 次，只要我们保证每一次先打印 `foo` 再打印 `bar`，不管是同一个线程还是两个线程都能得到正确答案。
- **时间/空间复杂度**：  
  - **时间复杂度**：`O(n)`。循环执行 `n` 次，每次只做常数次打印操作，整体随 `n` 成线性增长。  
  - **空间复杂度**：`O(1)`。只用了几个计数变量，和 `n` 的大小无关。

> **大白话**：`O(n)` 就像排队买票，人数越多排队时间就越长；`O(1)` 就像只需要一张纸记下当前的号码，不会因为排队人数增多而占用更多纸张。

#### 代码（Python）

```python
def foo_bar_sequential(n):
    """最直白的顺序实现，仅用于说明思路。"""
    for _ in range(n):
        print("foo", end='')   # 先打印 foo
        print("bar", end='')   # 再打印 bar
    print()                     # 换行，保持输出整洁
```

#### 复杂度

- **时间复杂度**：`O(n)` — 随着 `n` 增大，循环次数线性增加。
- **空间复杂度**：`O(1)` — 只用了固定数量的变量。

---

### 2. 最优解

#### 思路  

在实际面试中，**题目要求两个不同的线程分别调用 `foo` 与 `bar`**，并且必须交替输出。这就涉及到**线程同步**，如果不加任何限制，两个线程可能会出现以下情况：

```
foo foo foo ...   # 一个线程抢占了所有 CPU 时间片
bar bar bar ...
```

导致输出顺序错乱。  
我们需要让两个线程**“轮流”**执行：`foo` 完成一次后，`bar` 才能执行一次，然后再轮到 `foo`，如此循环 `n` 次。

**瓶颈**  
- 两个线程需要互相“让位”。如果只用普通的 `Lock`（互斥锁），会导致 **死锁**：`foo` 持有锁后 `bar` 无法获取，`foo` 又等 `bar` 释放锁，程序卡住。

**优化思路**  
使用 **信号量（Semaphore）** 或 **条件变量（Condition）** 来实现“谁该跑，谁就拿到许可”。下面用最简洁的 **两个 Semaphore** 来演示：

1. **初始化**  
   - `foo_sem = Semaphore(1)` → 允许 `foo` 线程先运行一次（因为一开始要先打印 `foo`）。  
   - `bar_sem = Semaphore(0)` → `bar` 线程一开始 **不能** 运行，必须等 `foo` 先释放许可。

2. **foo 方法**（每次循环）  
   - `foo_sem.acquire()` → 获取执行权，若当前没有许可会阻塞。  
   - 打印 `"foo"`。  
   - `bar_sem.release()` → 给 `bar` 线程一张“通行证”，让它可以继续。

3. **bar 方法**（每次循环）  
   - `bar_sem.acquire()` → 等待 `foo` 发来的通行证。  
   - 打印 `"bar"`。  
   - `foo_sem.release()` → 再把执行权交回 `foo`。

这样，两条线程会 **交替** 获得执行权，恰好形成 `foobar` 的顺序。

**关键概念解释**  

- **线程（Thread）**：程序里可以同时跑的“小工”。不同线程可以并行执行，互不干扰（除非共享资源）。
- **信号量（Semaphore）**：想象成一个**只能容纳固定人数的房间**。`acquire()` 进去需要先检查房间里是否还有空位，若满了就等；`release()` 离开后会让房间腾出一个位置给下一个等待的人。这里我们把房间容量设为 1 或 0，来控制谁可以先进入。

#### 代码（Python）

```python
import threading

class FooBar:
    """
    两个线程交替调用 foo() 与 bar()，最终输出 "foobar" 重复 n 次。
    """
    def __init__(self, n: int):
        self.n = n
        # foo 线程先拥有执行权，bar 线程先阻塞
        self.foo_sem = threading.Semaphore(1)   # 初始值 1，允许 foo 先跑
        self.bar_sem = threading.Semaphore(0)   # 初始值 0，bar 需要等 foo

    def foo(self, printFoo):
        """
        printFoo 是一个函数，调用 printFoo() 会输出 "foo"（不换行）。
        """
        for _ in range(self.n):
            self.foo_sem.acquire()        # 等待自己被允许执行
            printFoo()                     # 输出 "foo"
            self.bar_sem.release()        # 让 bar 线程获得执行权

    def bar(self, printBar):
        """
        printBar 是一个函数，调用 printBar() 会输出 "bar"（不换行）。
        """
        for _ in range(self.n):
            self.bar_sem.acquire()        # 等待 foo 完成一次后才继续
            printBar()                     # 输出 "bar"
            self.foo_sem.release()        # 再把执行权交回 foo

# ------------------- 测试代码（可直接运行） -------------------
def test_foobar(n):
    foobar = FooBar(n)

    # 这里的 lambda 负责实际打印，使用 end='' 防止自动换行
    def printFoo(): print("foo", end='')
    def printBar(): print("bar", end='')

    t1 = threading.Thread(target=foobar.foo, args=(printFoo,))
    t2 = threading.Thread(target=foobar.bar, args=(printBar,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print()   # 最后换行，保持输出整洁

# 示例
test_foobar(1)   # 输出: foobar
test_foobar(2)   # 输出: foobarfoobar
```

**代码要点注释**  

- `self.foo_sem = threading.Semaphore(1)`：把“房间”里先放一张票给 `foo`，它可以直接进去。  
- `self.bar_sem = threading.Semaphore(0)`：`bar` 先没有票，只能等 `foo` 完成后 `release()` 再拿到。  
- `acquire()` 与 `release()` 的配对保证了 **严格交替**，不会出现 `foofoo` 或 `barbar` 的情况。  

#### 复杂度

- **时间复杂度**：`O(n)` — 每个线程循环 `n` 次，打印操作是常数时间。相比暴力解唯一的差别是多了同步原语的调度开销，仍然是线性级别。  
- **空间复杂度**：`O(1)` — 只用了两个信号量（常数个对象），不随 `n` 增长。

---

## 心得

- **核心技巧**：利用 **信号量（Semaphore）** 或 **条件变量（Condition）** 实现线程的交替执行。  
- **适用的题型**：  
  1. “交替打印” 类题目（如 `Print Alternating Zero One`、`Print Zero Even Odd`）。  
  2. “顺序执行多线程任务” 类题目（如 “多线程的顺序打印 A、B、C”）。  
- **一句话总结**：**让每个线程在自己该跑的时候拿到“通行证”，跑完后把通行证交给下一个线程**。

---

## 反思

- **第一反应**：看到“两个线程交替输出”，立刻想到使用 **锁** 或 **信号量** 来控制执行顺序。  
- **最容易踩的坑**：  
  - 忘记在 `foo` 完成后 `release` `bar` 的信号量，导致 `bar` 永远阻塞。  
  - 初始信号量的值写反（把 `foo` 的设为 0），会导致程序直接卡死。  
  - 打印函数默认会换行，题目要求不换行，需要使用 `end=''` 或自行实现 `printFoo/printBar`。  
- **下次遇到同类题**：第一步先**明确谁先执行**，然后**用一个计数或信号量把执行权在两条线程之间交替传递**。这样就能快速搭建出正确的同步框架。