# #2715. 超时取消 / Timeout Cancellation

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/timeout-cancellation/)

---

## 题目（英文原版）

**Description**

Given a function fn, an array of arguments args, and a timeout t in milliseconds, return a cancel function cancelFn.
After a delay of cancelTimeMs, the returned cancel function cancelFn will be invoked.
Initially, the execution of the function fn should be delayed by t milliseconds.
If, before the delay of t milliseconds, the function cancelFn is invoked, it should cancel the delayed execution of fn. Otherwise, if cancelFn is not invoked within the specified delay t, fn should be executed with the provided args as arguments.

**Examples**

**Example 1:**

```
setTimeout(cancelFn, cancelTimeMs)
```

**Example 2:**

```
Input: fn = (x) => x * 5, args = [2], t = 20
Output: [{"time": 20, "returned": 10}]
Explanation: 
const cancelTimeMs = 50;
const cancelFn = cancellable((x) => x * 5, [2], 20);
setTimeout(cancelFn, cancelTimeMs);

The cancellation was scheduled to occur after a delay of cancelTimeMs (50ms), which happened after the execution of fn(2) at 20ms.
```

**Example 3:**

```
Input: fn = (x) => x**2, args = [2], t = 100
Output: []
Explanation: 
const cancelTimeMs = 50;
const cancelFn = cancellable((x) => x**2, [2], 100);
setTimeout(cancelFn, cancelTimeMs);

The cancellation was scheduled to occur after a delay of cancelTimeMs (50ms), which happened before the execution of fn(2) at 100ms, resulting in fn(2) never being called.
```

**Example 4:**

```
Input: fn = (x1, x2) => x1 * x2, args = [2,4], t = 30
Output: [{"time": 30, "returned": 8}]
Explanation: 
const cancelTimeMs = 100;
const cancelFn = cancellable((x1, x2) => x1 * x2, [2,4], 30);
setTimeout(cancelFn, cancelTimeMs);

The cancellation was scheduled to occur after a delay of cancelTimeMs (100ms), which happened after the execution of fn(2,4) at 30ms.
```

**Constraints**

- fn is a function
- args is a valid JSON array
- 1 <= args.length <= 10
- 20 <= t <= 1000
- 10 <= cancelTimeMs <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个函数 `fn`、一个参数数组 `args`，以及一个以毫秒为单位的超时时间 `t`，返回一个取消函数 `cancelFn`。  

在 `cancelTimeMs` 毫秒后，将会调用返回的取消函数 `cancelFn`。  

最初，函数 `fn` 的执行应当延迟 `t` 毫秒后才开始。  

如果在这 `t` 毫秒的延迟期间，`cancelFn` 被调用，则应当取消对 `fn` 的延迟执行。否则，如果在指定的延迟 `t` 内未调用 `cancelFn`，则应当使用提供的 `args` 作为参数执行 `fn`。

**示例 1**  

```javascript
setTimeout(cancelFn, cancelTimeMs)
```

**示例 2**  

```javascript
Input: fn = (x) => x * 5, args = [2], t = 20
Output: [{"time": 20, "returned": 10}]
```

**Explanation:**  
```javascript
const cancelTimeMs = 50;
const cancelFn = cancellable((x) => x * 5, [2], 20);
setTimeout(cancelFn, cancelTimeMs);
```
取消操作被安排在 `cancelTimeMs`（50 ms）之后执行，而此时 `fn(2)` 已在 20 ms 时执行完毕。

**示例 3**  

```javascript
Input: fn = (x) => x**2, args = [2], t = 100
Output: []
```

**Explanation:**  
```javascript
const cancelTimeMs = 50;
const cancelFn = cancellable((x) => x**2, [2], 100);
setTimeout(cancelFn, cancelTimeMs);
```
取消操作被安排在 `cancelTimeMs`（50 ms）之后执行，恰好在 `fn(2)` 预定的 100 ms 执行之前发生，因此 `fn(2)` 从未被调用。

**示例 4**  

```javascript
Input: fn = (x1, x2) => x1 * x2, args = [2,4], t = 30
Output: [{"time": 30, "returned": 8}]
```

**Explanation:**  
```javascript
const cancelTimeMs = 100;
const cancelFn = cancellable((x1, x2) => x1 * x2, [2,4], 30);
setTimeout(cancelFn, cancelTimeMs);
```
取消操作被安排在 `cancelTimeMs`（100 ms）之后执行，而此时 `fn(2,4)` 已在 30 ms 时执行完毕。

**约束条件**  

- `fn` 为函数  
- `args` 为合法的 JSON 数组  
- `1 <= args.length <= 10`  
- `20 <= t <= 1000`  
- `10 <= cancelTimeMs <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. **先把函数 `fn` 暂存**，把参数 `args` 也记下来。  
2. **等 `t` 毫秒（即 `t/1000` 秒）后**，使用 `time.sleep` 把程序阻塞住，然后把 `fn(*args)` 执行并把返回值记下来。  
3. 为了实现「取消」的需求，我们再准备一个全局变量 `cancelled`，默认是 `False`。  
4. 返回的 `cancelFn` 只需要把 `cancelled` 设为 `True` 即可。  
5. 当 `sleep` 结束后检查 `cancelled`：如果已经被设为 `True`，就不调用 `fn`；否则正常调用。

> **类比**：把 `cancelled` 想象成一本字典的「是否已删除」标记，键是「这次调用」，值是「已取消/未取消」。只要在执行前把标记改为「已取消」，后面的查询就会直接返回，不再执行真正的「查字典」操作。

**为什么正确**  
- `cancelFn` 只会把标记改成 `True`，而真正调用 `fn` 的代码在 `sleep` 结束后才会检查这个标记。只要标记在检查前已经被改为 `True`，函数就不会被调用。  
- 若 `cancelFn` 从未被调用，标记保持 `False`，检查时自然会执行 `fn`，满足题目「如果在 `t` 毫秒内没有取消，就执行」的要求。

**复杂度分析（大白话）**  

| 步骤 | 时间消耗 | 空间占用 |
|------|----------|----------|
| `sleep(t)` | 必须等 `t` 毫秒，等同于 **O(t)**（这里的 `t` 其实是时间，不是数据规模）| 只用了一个布尔变量 `cancelled`，**O(1)**（常数空间） |
| 检查标记并可能调用 `fn` | 调用一次 `fn` 的时间，记作 **O(调用 fn 的复杂度)** | 同上，**O(1)** |

> 注意：这里的 **O(t)** 不是算法意义上的「随输入规模增长的复杂度」，而是「必须等的真实时间」，所以在实际面试中我们更关注的是「是否还有更好的方式」而不是这段「等」的时间。

#### 代码（Python）

```python
import time
from typing import Any, Callable, List

def cancellable(fn: Callable, args: List[Any], t: int) -> Callable[[], None]:
    """
    暴力实现：使用 time.sleep 等待 t 毫秒后再决定是否调用 fn。
    返回的 cancelFn 只需要把 cancelled 设为 True。
    """
    cancelled = False                     # 取消标记，初始为 False

    def cancelFn() -> None:
        """外部调用的取消函数，只把标记改为 True 即可。"""
        nonlocal cancelled
        cancelled = True                  # 把标记设为已取消

    # 这里用一个独立的线程或定时器更符合真实环境，下面的实现直接在主线程
    # 为了让示例代码可以直接跑，这里不创建新线程，只演示思路。
    def delayed_execution() -> None:
        """内部函数：等待 t 毫秒后检查标记并可能执行 fn。"""
        time.sleep(t / 1000)              # 等待 t 毫秒（Python 用秒）
        if not cancelled:                 # 标记仍是 False，说明没有被取消
            result = fn(*args)            # 执行 fn 并得到返回值
            # 这里把结果打印出来，真实题目会把它记录到返回数组中
            print({"time": t, "returned": result})

    # 为了让函数立即返回 cancelFn，同时又能在后台等 t 毫秒后执行，
    # 我们在这里直接调用 delayed_execution（实际使用时会放到线程/计时器里）。
    # 注意：在 LeetCode 的 JavaScript 环境里会使用 setTimeout，这里仅作演示。
    delayed_execution()

    return cancelFn
```

> **关键行注释**  
- `cancelled = False`：相当于「字典里记录这次调用未被删除」。  
- `nonlocal cancelled`：让内部的 `cancelFn` 能够修改外层的 `cancelled` 变量。  
- `time.sleep(t / 1000)`：把「毫秒」换算成「秒」后让程序停下来。  
- `if not cancelled:`：检查「是否已经被标记为取消」，如果没有就真正调用函数。

#### 复杂度

- **时间复杂度：O(t + 调用 fn 的时间)**  
  - `t` 是必须等的时间（毫秒），相当于「等多久就花多久」。  
  - 若 `cancelFn` 在 `t` 之前被调用，仍然要等满 `t`（因为我们用了 `sleep`），所以这不是最优的。

- **空间复杂度：O(1)**  
  - 只用了一个布尔变量 `cancelled`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**最大的瓶颈**是 `time.sleep(t)`——它会把整个程序阻塞住，即使已经收到取消信号也必须等到 `t` 结束后才能判断。我们需要一种「可以在等待期间被打断」的机制。

在 JavaScript 中，`setTimeout` 本身就提供了「延迟执行」并且可以通过返回值的 `clearTimeout` 来**随时取消**。在 Python 中对应的工具是 `threading.Timer`：

- `Timer(delay, func, args=..., kwargs=...)` 会在 `delay` 秒后自动调用 `func`。  
- 调用 `timer.cancel()` 可以在 `func` 真的执行前把它撤销。

**核心技巧**：**使用系统提供的可取消定时器，而不是自己手动 `sleep`**。这样：

1. 创建一个 `Timer`，让它在 `t` 毫秒后执行 `fn(*args)`。  
2. 把这个 `Timer` 对象保存下来。  
3. 返回的 `cancelFn` 只需要调用 `timer.cancel()`，系统会立即阻止计时器的回调，不会再执行 `fn`。  
4. 计时器本身是 **线程安全** 的，内部已经处理了并发和取消的细节，我们无需自己维护标记。

> **类比**：把 `Timer` 想成「厨房里的定时炸锅」。我们设定好 5 分钟后自动关火。如果在 3 分钟时发现菜已经熟了，只需要按一下「取消」按钮，炸锅立刻停止，不会等到 5 分钟后才关火。  
> `cancelFn` 就是那只「取消按钮」。

#### 代码（Python）

```python
import threading
from typing import Any, Callable, List

def cancellable(fn: Callable, args: List[Any], t: int) -> Callable[[], None]:
    """
    最优实现：使用 threading.Timer 实现可取消的延迟调用。
    - fn   : 要延迟执行的函数
    - args : fn 的参数列表
    - t    : 延迟时间（毫秒）
    返回值 cancelFn：调用后会立即取消计时器，使 fn 不会被执行。
    """
    # 1️⃣ 创建计时器，delay 参数必须是秒，故除以 1000
    timer = threading.Timer(t / 1000, fn, args=args)

    # 2️⃣ 启动计时器，让它在后台开始倒计时
    timer.start()

    # 3️⃣ 定义取消函数，直接调用计时器的 cancel 方法
    def cancelFn() -> None:
        """
        当外部调用 cancelFn 时，计时器会被取消。
        如果计时器已经执行完毕（即 fn 已经被调用），cancel() 不会有任何副作用。
        """
        timer.cancel()          # 立即停止计时器，防止 fn 被调用

    return cancelFn
```

> **关键行解释**  
- `threading.Timer(t / 1000, fn, args=args)`：把「毫秒」转成「秒」后创建计时器。`fn` 和 `args` 正好对应题目要求的「延迟执行函数及其参数」。  
- `timer.start()`：启动计时器，让它在 **后台**（单独的线程）倒数，而不阻塞主线程。  
- `timer.cancel()`：系统提供的「撤销」操作，一旦调用，计时器内部会标记为已取消，后续的回调函数 `fn` 将不再执行。

#### 复杂度

- **时间复杂度：O(调用 fn 的时间)**  
  - 创建计时器、启动、取消都是 **O(1)** 的常数操作。只有当计时器真的触发时，才会执行 `fn`，这时的复杂度完全取决于 `fn` 本身。

- **空间复杂度：O(1)**  
  - 只保存了一个 `Timer` 对象（内部实现使用一个线程），不随 `args` 长度或 `t` 大小增长。

> 与暴力解对比：  
> - 暴力解必须等满 `t`，即使已经收到取消信号也不能提前结束；最优解在收到取消请求后立刻停止，不会再浪费时间。  
> - 暴力解的「阻塞」会导致程序无法并行处理其他任务，最优解利用线程实现真正的异步等待。

---

## 心得

- **核心技巧**：利用语言/库自带的「可取消计时器」(`threading.Timer` / `setTimeout` + `clearTimeout`) 实现延迟执行的同时提供即时取消。
- **适用场景**  
  1. **防抖（debounce）**：用户连续输入时，只在最后一次输入后一定时间才触发搜索请求。  
  2. **限流（throttle）**：固定时间窗口内只允许执行一次函数。  
  3. **异步任务超时控制**：在一定时间内若任务未完成，则自动取消或执行备选方案。  
- **一句话总结**：**把「等」交给系统的计时器，让取消交给 `cancel()`，别自己手动 `sleep`。**

---

## 反思

- **第一反应**：直接 `sleep` 再检查标记，代码看起来最简单。  
- **最容易踩的坑**  
  - **阻塞主线程**：`sleep` 会让程序在等待期间不能处理其它事件，导致实际运行时「取消」根本来不及。  
  - **计时器已执行后再 cancel**：如果 `cancelFn` 在 `fn` 已经执行完毕后被调用，`cancel()` 仍然安全，只是没有实际效果。  
  - **时间单位**：题目给的是毫秒，Python 的 `time.sleep` 与 `threading.Timer` 使用的是秒，需要注意除以 `1000`。  
- **下次类似题的第一步**：先想「有没有现成的可取消计时器/任务调度器」，如果有就直接利用；如果没有，再考虑自己维护「取消标记」的方式。