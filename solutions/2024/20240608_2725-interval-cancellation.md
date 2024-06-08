# #2725. **间隔取消** / Interval Cancellation

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/interval-cancellation/)

---

## 题目（英文原版）

**Description**

Given a function fn, an array of arguments args, and an interval time t, return a cancel function cancelFn.
After a delay of cancelTimeMs, the returned cancel function cancelFn will be invoked.
The function fn should be called with args immediately and then called again every t milliseconds until cancelFn is called at cancelTimeMs ms.

**Examples**

**Example 1:**

```
setTimeout(cancelFn, cancelTimeMs)
```

**Example 2:**

```
Input: fn = (x) => x * 2, args = [4], t = 35
Output: 
[
   {"time": 0, "returned": 8},
   {"time": 35, "returned": 8},
   {"time": 70, "returned": 8},
   {"time": 105, "returned": 8},
   {"time": 140, "returned": 8},
   {"time": 175, "returned": 8}
]
Explanation: 
const cancelTimeMs = 190;
const cancelFn = cancellable((x) => x * 2, [4], 35);
setTimeout(cancelFn, cancelTimeMs);

Every 35ms, fn(4) is called. Until t=190ms, then it is cancelled.
1st fn call is at 0ms. fn(4) returns 8.
2nd fn call is at 35ms. fn(4) returns 8.
3rd fn call is at 70ms. fn(4) returns 8.
4th fn call is at 105ms. fn(4) returns 8.
5th fn call is at 140ms. fn(4) returns 8.
6th fn call is at 175ms. fn(4) returns 8.
Cancelled at 190ms
```

**Example 3:**

```
Input: fn = (x1, x2) => (x1 * x2), args = [2, 5], t = 30
Output: 
[
   {"time": 0, "returned": 10},
   {"time": 30, "returned": 10},
   {"time": 60, "returned": 10},
   {"time": 90, "returned": 10},
   {"time": 120, "returned": 10},
   {"time": 150, "returned": 10}
]
Explanation: 
const cancelTimeMs = 165; 
const cancelFn = cancellable((x1, x2) => (x1 * x2), [2, 5], 30) 
setTimeout(cancelFn, cancelTimeMs)

Every 30ms, fn(2, 5) is called. Until t=165ms, then it is cancelled.
1st fn call is at 0ms 
2nd fn call is at 30ms 
3rd fn call is at 60ms 
4th fn call is at 90ms 
5th fn call is at 120ms 
6th fn call is at 150ms
Cancelled at 165ms
```

**Example 4:**

```
Input: fn = (x1, x2, x3) => (x1 + x2 + x3), args = [5, 1, 3], t = 50
Output: 
[
   {"time": 0, "returned": 9},
   {"time": 50, "returned": 9},
   {"time": 100, "returned": 9},
   {"time": 150, "returned": 9}
]
Explanation: 
const cancelTimeMs = 180;
const cancelFn = cancellable((x1, x2, x3) => (x1 + x2 + x3), [5, 1, 3], 50)
setTimeout(cancelFn, cancelTimeMs)

Every 50ms, fn(5, 1, 3) is called. Until t=180ms, then it is cancelled. 
1st fn call is at 0ms
2nd fn call is at 50ms
3rd fn call is at 100ms
4th fn call is at 150ms
Cancelled at 180ms
```

**Constraints**

- fn is a function
- args is a valid JSON array
- 1 <= args.length <= 10
- 30 <= t <= 100
- 10 <= cancelTimeMs <= 500

---

## 题目（中文翻译）

给定一个函数 `fn`、一个参数数组 `args`，以及一个间隔时间 `t`，返回一个取消函数 `cancelFn`。  
在延迟 `cancelTimeMs` 毫秒后，会调用返回的取消函数 `cancelFn`。  
函数 `fn` 应当立即使用 `args` 调用一次，然后每隔 `t` 毫秒再次调用，直至在 `cancelTimeMs` 毫秒时调用 `cancelFn` 为止。

---

### 示例

#### 示例 1
```js
setTimeout(cancelFn, cancelTimeMs)
```

#### 示例 2
**输入**
```json
{
  "fn": "(x) => x * 2",
  "args": [4],
  "t": 35
}
```

**输出**
```json
[
   {"time": 0,   "returned": 8},
   {"time": 35,  "returned": 8},
   {"time": 70,  "returned": 8},
   {"time": 105, "returned": 8},
   {"time": 140, "returned": 8},
   {"time": 175, "returned": 8}
]
```

**解释**
```js
const cancelTimeMs = 190;
const cancelFn = cancellable((x) => x * 2, [4], 35);
setTimeout(cancelFn, cancelTimeMs);
```
每隔 35 ms 调用一次 `fn(4)`，直到在 190 ms 时通过 `cancelFn` 停止调用。

#### 示例 3
**输入**
```json
{
  "fn": "(x1, x2) => (x1 * x2)",
  "args": [2, 5],
  "t": 30
}
```

**输出**
```json
[
   {"time": 0,   "returned": 10},
   {"time": 30,  "returned": 10},
   {"time": 60,  "returned": 10},
   {"time": 90,  "returned": 10},
   {"time": 120, "returned": 10},
   {"time": 150, "returned": 10}
]
```

**解释**
```js
const cancelTimeMs = 165; 
const cancelFn = cancellable((x1, x2) => (x1 * x2), [2, 5], 30);
setTimeout(cancelFn, cancelTimeMs);
```
每隔 30 ms 调用一次 `fn(2, 5)`，直到在 165 ms 时被 `cancelFn` 取消。

#### 示例 4
**输入**
```json
{
  "fn": "(x1, x2, x3) => (x1 + x2 + x3)",
  "args": [5, 1, 3],
  "t": 50
}
```

**输出**
```json
[
   {"time": 0,   "returned": 9},
   {"time": 50,  "returned": 9},
   {"time": 100, "returned": 9},
   {"time": 150, "returned": 9}
]
```

**解释**
```js
const cancelTimeMs = 180;
const cancelFn = cancellable((x1, x2, x3) => (x1 + x2 + x3), [5, 1, 3], 50);
setTimeout(cancelFn, cancelTimeMs);
```
每隔 50 ms 调用一次 `fn(5, 1, 3)`，直到在 180 ms 时通过 `cancelFn` 停止。

---

### 约束条件

- `fn` 是一个函数  
- `args` 是合法的 JSON 数组  
- `1 ≤ args.length ≤ 10`  
- `30 ≤ t ≤ 100`  
- `10 ≤ cancelTimeMs ≤ 500`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **“循环 + 睡眠”**：  
1. 立刻调用一次 `fn(*args)`，把返回值记下来（题目要求把每次调用的时间点和返回值记录下来，方便后面验证）。  
2. 然后进入一个 `while` 循环，每次 `time.sleep(t / 1000)`（把毫秒转成秒），再调用一次 `fn(*args)`。  
3. 当外部的 `cancelFn` 被调用时，把一个全局变量 `cancelled` 设为 `True`，循环看到这个标记就立即退出，从而实现“在指定的 cancelTimeMs 毫秒后停止”。  

> **类比**：想象你在厨房里做饭，每隔一定时间（`t` 毫秒）就要翻一次锅（调用 `fn`）。如果有人在某个时刻（`cancelTimeMs`）叫你停下，你只要把锅的开关拉掉（把 `cancelled` 设为 `True`），循环自然结束。

**为什么这种办法能工作？**  
- `time.sleep` 能让程序暂停指定的毫秒数，恰好模拟了“每 `t` 毫秒执行一次”。  
- 循环体里只要检查一次 `cancelled` 标记，就能在外部调用 `cancelFn` 时立刻停止。  

#### 代码（Python）

```python
import time
import threading
from typing import Callable, List, Any, Dict

def cancellable_bruteforce(fn: Callable, args: List[Any], t: int, cancel_time_ms: int):
    """
    暴力实现：循环 + sleep
    返回值是记录每次调用时间和返回值的列表，外部可以通过 cancelFn() 来停止循环
    """
    # 用来记录每一次 fn 的调用结果
    logs: List[Dict[str, Any]] = []
    # 取消标记，外部的 cancelFn 会把它设为 True
    cancelled = {"flag": False}

    def cancelFn():
        """外部调用的取消函数，只负责改标记"""
        cancelled["flag"] = True

    # 立刻调用一次 fn
    start = time.time()                     # 记录起始时间点（秒）
    ret = fn(*args)
    logs.append({"time": 0, "returned": ret})   # 第 0 毫秒的记录

    # 计算一共需要执行多少次（不包括第 0 次）
    total_calls = cancel_time_ms // t        # 整除得到完整的间隔次数

    # 循环执行剩余的调用
    for i in range(1, total_calls + 1):
        # 每次睡 t 毫秒
        time.sleep(t / 1000.0)

        # 检查是否已经被取消
        if cancelled["flag"]:
            break

        # 再次调用 fn
        ret = fn(*args)
        logs.append({"time": i * t, "returned": ret})

    return logs, cancelFn


# ------------------------------------------------------------
# 示例运行（仅用于本地调试，LeetCode 平台不需要下面的代码）
if __name__ == "__main__":
    # 示例 2
    fn = lambda x: x * 2
    args = [4]
    t = 35
    cancel_time_ms = 190

    logs, cancel = cancellable_bruteforce(fn, args, t, cancel_time_ms)

    # 使用一个计时器在 cancel_time_ms 后主动调用 cancel()
    threading.Timer(cancel_time_ms / 1000.0, cancel).start()

    # 等待所有计时器结束（这里最多等 0.5 秒）
    time.sleep(0.6)
    print(logs)
```

> **关键行中文注释**  
> - `cancelled = {"flag": False}`：用字典包装布尔值，使内部函数可以修改外部变量（Python 的闭包特性）。  
> - `time.sleep(t / 1000.0)`：把毫秒转成秒，让程序暂停 `t` 毫秒。  
> - `if cancelled["flag"]: break`：一旦外部调用了 `cancelFn`，立即退出循环。

#### 复杂度

- **时间复杂度**：`O(k)`，其中 `k = cancel_time_ms // t` 是实际执行 `fn` 的次数。  
  - 大白话：如果要跑 10 次，就花 10 次的时间；如果要跑 100 次，就花 100 次的时间，正比于调用次数。  
- **空间复杂度**：`O(k)`，因为我们把每一次的返回值和时间点都存进了 `logs` 列表。  
  - 大白话：需要的内存会随调用次数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于 **同步阻塞的 `sleep` 循环**：  
- `time.sleep` 会让整个线程停下来，期间程序无法做其他事情（比如响应外部的 `cancelFn`）。  
- 在实际的前端/后端环境（JavaScript 的 `setInterval` / `clearInterval`），我们更倾向于 **“非阻塞、事件驱动”** 的方式。

**优化思路**：  
1. 利用 **计时器（Timer）** 让函数在指定的毫秒后自动执行，而不是自己去 `sleep`。  
2. 每一次计时器触发后，再 **重新创建下一个计时器**，形成“链式”调用。这样每一次调用都是独立的事件，不会阻塞主线程。  
3. 保存最近一次创建的计时器对象 `current_timer`，在外部调用 `cancelFn` 时，只需要调用 `current_timer.cancel()`（在 Python 中是 `timer.cancel()`），就能阻止后续的计时器继续执行。  

**核心数据结构**：  
- **`threading.Timer`**：相当于 JavaScript 里的 `setTimeout`，可以在指定时间后执行一次函数。我们把它当作“单次的闹钟”。  
- **标记变量 `active`**：记录当前计时器是否仍然有效，防止已经取消后仍然产生新的计时器。

**类比**：把每一次 `fn` 的调用想象成一次 “投递快递”。  
- 暴力解是让一个快递员不停走路（`sleep`），每走到一定距离就投递一次。  
- 最优解是每投递一次就让快递员把下一个投递任务交给 **另一位快递员**（新的计时器），原来的快递员只负责这一次，等他被叫停（`cancel`）后，后面的快递员根本不会出现。

#### 代码（Python）

```python
import threading
from typing import Callable, List, Any, Dict

def cancellable(fn: Callable, args: List[Any], t: int, cancel_time_ms: int):
    """
    最优实现：使用递归计时器（Timer）实现间隔调用
    返回 (logs, cancelFn)：
    - logs: 记录每次调用的时间点（相对起始时间）和返回值
    - cancelFn: 在 cancel_time_ms 毫秒后调用，可立即停止后续调用
    """
    logs: List[Dict[str, Any]] = []          # 保存结果
    start_ts = threading.Event()             # 用来记录起始时间的标记
    start_ts.set()                           # 立刻置位，后面通过 time.time() 读取

    # 用字典包装，便于在内部函数里修改（闭包）
    state = {"active": True, "timer": None, "call_cnt": 0}

    import time
    start_time = time.time()                 # 记录 0 时刻（秒）

    def record_and_schedule():
        """调用 fn、记录结果、并安排下次调用（如果仍然 active）"""
        if not state["active"]:
            return

        # 调用 fn 并记录
        ret = fn(*args)
        elapsed_ms = int((time.time() - start_time) * 1000)  # 转成毫秒整数
        logs.append({"time": elapsed_ms, "returned": ret})

        # 计数 + 判断是否已经达到取消时间
        state["call_cnt"] += 1
        if elapsed_ms >= cancel_time_ms:
            # 已经超过或等于取消时间，直接停止，不再安排新计时器
            state["active"] = False
            return

        # 再创建一个新的计时器，t 毫秒后再次执行本函数
        timer = threading.Timer(t / 1000.0, record_and_schedule)
        state["timer"] = timer
        timer.start()

    # 第一次立即调用（时间 0）
    record_and_schedule()

    def cancelFn():
        """外部调用的取消函数：直接把当前计时器取消"""
        state["active"] = False
        # 如果还有未执行的计时器，立即取消它
        cur = state.get("timer")
        if cur is not None:
            cur.cancel()

    # 为了符合题目要求：在 cancel_time_ms 后自动调用 cancelFn
    threading.Timer(cancel_time_ms / 1000.0, cancelFn).start()

    return logs, cancelFn


# ------------------------------------------------------------
# 示例运行（仅用于本地调试）
if __name__ == "__main__":
    fn = lambda x, y: x * y
    args = [2, 5]
    t = 30
    cancel_time_ms = 165

    logs, _ = cancellable(fn, args, t, cancel_time_ms)

    # 等待足够时间让所有计时器结束（这里最多 0.3 秒）
    time.sleep(0.4)
    print(logs)
```

**代码要点解释**  

| 行号 | 关键代码 | 中文解释 |
|------|----------|----------|
| 1‑2 | `import threading` | 引入计时器类，类似 JS 的 `setTimeout`。 |
| 9‑12 | `state = {"active": True, "timer": None, "call_cnt": 0}` | 用字典保存“是否仍然有效”和最近的计时器对象，便于在 `cancelFn` 中随时访问。 |
| 17‑30 | `def record_and_schedule():` | 递归函数：先执行 `fn`，记录结果，然后在 `t` 毫秒后**重新创建**一个计时器继续调用自己。 |
| 22‑23 | `elapsed_ms = int((time.time() - start_time) * 1000)` | 计算相对起始时刻的毫秒数，用来填充返回的 `time` 字段。 |
| 27‑28 | `if elapsed_ms >= cancel_time_ms: ...` | 达到或超过取消时间后直接停止，不再安排新计时器。 |
| 30‑33 | `timer = threading.Timer(t / 1000.0, record_and_schedule)` | 创建下一个计时器，让它在 `t` 毫秒后再次执行本函数。 |
| 36‑43 | `def cancelFn():` | 外部暴露的取消函数：把 `active` 设为 `False` 并立即 `cancel` 正在等待的计时器。 |
| 46‑48 | `threading.Timer(cancel_time_ms / 1000.0, cancelFn).start()` | 自动在 `cancel_time_ms` 后调用 `cancelFn`，模拟题目中 `setTimeout(cancelFn, cancelTimeMs)` 的行为。 |

#### 复杂度

- **时间复杂度**：`O(k)`，其中 `k = cancel_time_ms // t`（实际执行 `fn` 的次数）。  
  - 与暴力解相比，**常数因子更小**：没有阻塞的 `sleep`，每一次调用只花费函数本身的执行时间和创建计时器的开销。  

- **空间复杂度**：`O(k)`（存储 `logs`）+ `O(1)`（计时器对象只有一个在任意时刻是活动的）。  
  - 与暴力解相同的记录需求，但额外的计时器对象是常数级别的。

---

## 心得

- **核心技巧**：使用 **递归计时器（Timer）** 替代阻塞循环，实现“非阻塞的定时重复调用”。  
- **适用场景**：  
  1. **轮询任务**（如定时拉取服务器数据）。  
  2. **动画帧驱动**（每隔固定时间更新画面）。  
  3. **资源监控**（每隔一定间隔检查系统状态）。  
- **一句话总结**：**“用一次性计时器链式调用自己，配合取消标记即可实现可停止的间隔执行”。**

---

## 反思

- **第一反应**：直接写 `while` 循环配 `sleep`，因为这在普通脚本里最直观。  
- **最容易踩的坑**：  
  - **计时器泄漏**：如果在取消后仍然创建新的计时器，会导致程序一直跑下去。一定要在 `cancelFn` 或达到 `cancel_time_ms` 时阻止后续创建。  
  - **时间精度**：`time.sleep` 和 `threading.Timer` 都只能保证“最少”等待 `t` 毫秒，实际触发时间可能稍有偏差。题目只要求相对时间点，不需要极端精准。  
  - **共享状态**：在闭包里修改外部变量时，需要用可变对象（如字典）或 `nonlocal`，否则会出现 `UnboundLocalError`。  

- **下次类似题**：第一步应该想到 **“事件驱动的计时器”**（`setTimeout` / `threading.Timer`），而不是 **“阻塞循环 + sleep”**，因为后者在真实的并发环境里会阻塞主线程，导致不可预期的行为。