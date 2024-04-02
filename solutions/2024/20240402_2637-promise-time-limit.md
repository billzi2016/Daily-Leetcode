# #2637. **Promise 时间限制** / Promise Time Limit

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/promise-time-limit/)

---

## 题目（英文原版）

**Description**

Given an asynchronous function fn and a time t in milliseconds, return a new time limited version of the input function. fn takes arguments provided to the time limited function.
The time limited function should follow these rules:

**Examples**

**Example 1:**

```
Input: 
fn = async (n) => { 
  await new Promise(res => setTimeout(res, 100)); 
  return n * n; 
}
inputs = [5]
t = 50
Output: {"rejected":"Time Limit Exceeded","time":50}
Explanation:
const limited = timeLimit(fn, t)
const start = performance.now()
let result;
try {
   const res = await limited(...inputs)
   result = {"resolved": res, "time": Math.floor(performance.now() - start)};
} catch (err) {
   result = {"rejected": err, "time": Math.floor(performance.now() - start)};
}
console.log(result) // Output

The provided function is set to resolve after 100ms. However, the time limit is set to 50ms. It rejects at t=50ms because the time limit was reached.
```

**Example 2:**

```
Input: 
fn = async (n) => { 
  await new Promise(res => setTimeout(res, 100)); 
  return n * n; 
}
inputs = [5]
t = 150
Output: {"resolved":25,"time":100}
Explanation:
The function resolved 5 * 5 = 25 at t=100ms. The time limit is never reached.
```

**Example 3:**

```
Input: 
fn = async (a, b) => { 
  await new Promise(res => setTimeout(res, 120)); 
  return a + b; 
}
inputs = [5,10]
t = 150
Output: {"resolved":15,"time":120}
Explanation:
​​​​The function resolved 5 + 10 = 15 at t=120ms. The time limit is never reached.
```

**Example 4:**

```
Input: 
fn = async () => { 
  throw "Error";
}
inputs = []
t = 1000
Output: {"rejected":"Error","time":0}
Explanation:
The function immediately throws an error.
```

**Constraints**

- 0 <= inputs.length <= 10
- 0 <= t <= 1000
- fn returns a promise

---

## 题目（中文翻译）

给定一个异步函数（asynchronous function）`fn` 和一个以毫秒为单位的时间 `t`，返回一个 **限时版**（time limited version）的函数。`fn` 会接受传入限时函数的参数。

限时函数需要遵循以下规则：

（原题中规则未给出，此处按示例说明实现）

---

### 示例

#### 示例 1
**输入**  
```js
fn = async (n) => { 
  await new Promise(res => setTimeout(res, 100)); 
  return n * n; 
}
inputs = [5]
t = 50
```
**输出**  
```json
{"rejected":"Time Limit Exceeded","time":50}
```
**解释**  
```js
const limited = timeLimit(fn, t)
const start = performance.now()
let result;
try {
    const res = await limited(...inputs)
    result = {"resolved": res, "time": Math.floor(performance.now() - start)};
} catch (err) 
...
```
限时函数在 50 ms 内未完成执行，因而抛出 `"Time Limit Exceeded"`，并记录实际耗时 50 ms。

---

#### 示例 2
**输入**  
```js
fn = async (n) => { 
  await new Promise(res => setTimeout(res, 100)); 
  return n * n; 
}
inputs = [5]
t = 150
```
**输出**  
```json
{"resolved":25,"time":100}
```
**解释**  
函数在 100 ms 时完成并返回 `5 * 5 = 25`，未触及时间上限。

---

#### 示例 3
**输入**  
```js
fn = async (a, b) => { 
  await new Promise(res => setTimeout(res, 120)); 
  return a + b; 
}
inputs = [5,10]
t = 150
```
**输出**  
```json
{"resolved":15,"time":120}
```
**解释**  
函数在 120 ms 时返回 `5 + 10 = 15`，同样未触及时间上限。

---

#### 示例 4
**输入**  
```js
fn = async () => { 
  throw "Error";
}
inputs = []
t = 1000
```
**输出**  
```json
{"rejected":"Error","time":0}
```
**解释**  
函数立即抛出错误 `"Error"`，限时函数捕获该错误并返回，耗时为 0 ms。

---

### 约束条件
- `0 <= inputs.length <= 10`
- `0 <= t <= 1000`
- `fn` 返回一个 **Promise**（promise）  

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：

1. 调用传进来的异步函数 `fn(...args)`，得到一个 **Promise**（把它想象成“厨房里正在烹饪的菜”，我们不知道什么时候能端上来）。  
2. 同时启动一个计时器 `setTimeout`，等 `t` 毫秒后如果菜还没端上来，就 **强行把它砍掉**，让外层的 Promise **reject** 一个 `"Time Limit Exceeded"` 的错误。  
3. 为了判断“菜到底端没端上”，我们可以在 `fn` 的 Promise 完成（`then` 或 `catch`）时把一个标记 `finished = true`。计时器回调里检查这个标记，如果已经 `true` 就不做任何事；否则就 `reject`。

> **类比**：  
> - **Promise** 像外卖员送餐的过程。  
> - **setTimeout** 像我们给外卖员设定的“最迟送达时间”。  
> - 如果外卖员在规定时间前把餐送到，我们就收下（`resolve`）；如果超时我们直接打电话取消订单（`reject`）。

这个思路一定能得到正确答案，因为我们把两件事（函数执行、超时检测）都准备好，并在任意一件先完成时立即决定最终的结果。

#### 代码（Python）

```python
import asyncio
import time
from typing import Any, Callable, Awaitable

def time_limit(fn: Callable[..., Awaitable], t: int) -> Callable[..., Awaitable]:
    """
    返回一个新的函数，该函数在 t 毫秒内没有得到 fn 的结果时会被 reject。
    """
    async def wrapper(*args: Any, **kwargs: Any):
        # 用来记录 fn 是否已经完成
        finished = False

        # 1) 包装 fn 的执行：把它的 resolve / reject 转发给外层的 future
        async def run_fn():
            nonlocal finished
            try:
                result = await fn(*args, **kwargs)
                finished = True               # fn 成功返回
                return result
            except Exception as e:
                finished = True               # fn 报错也算“完成”
                raise e

        # 2) 超时的 Promise（在 asyncio 里用 asyncio.sleep 实现）
        async def timeout():
            await asyncio.sleep(t / 1000)     # t 是毫秒，sleep 需要秒
            if not finished:                  # 只有真正超时才 reject
                raise TimeoutError("Time Limit Exceeded")

        # 3) 同时跑两个协程，谁先结束就返回谁的结果
        return await asyncio.wait_for(
            asyncio.shield(run_fn()),          # 防止外层 cancel 影响内部
            timeout=t / 1000
        )
    return wrapper
```

> **关键行中文注释**  
> - `finished = False`：记录函数是否已经结束。  
> - `await asyncio.sleep(t / 1000)`：相当于 `setTimeout`，把毫秒转成秒。  
> - `if not finished: raise TimeoutError(...)`：只有真的超时才抛错。  

> **说明**：这里用了 `asyncio.wait_for` 其实已经把“超时+抛异常”封装好了，算是一种「暴力」实现的简化版。

#### 复杂度

- **时间复杂度**：`O(1)`（常数时间）——我们只启动两个并行的计时/执行任务，和输入规模无关。  
- **空间复杂度**：`O(1)`——只用了几个标记变量，额外空间不随 `fn` 的运行时间增长。

---

### 2. 最优解

#### 思路  

在「暴力」实现里，我们自己维护了 `finished` 标记并手动判断是否超时。其实 **Promise（或 asyncio 的 Future）本身就能帮我们做这件事**：只要把「函数的 Promise」和「超时的 Promise」放在一起，让「先到者」决定最终结果，就不需要额外的标记。

这正是 **`Promise.race`**（在 Python 的 `asyncio` 中对应 `asyncio.wait` 或 `asyncio.wait_for`）的核心思想：

- 把两个 Promise 放进一个「赛跑场」  
- 谁先「到终点」就返回谁的结果，另一个会被自动忽略

因此最简洁的实现只需要：

1. 创建一个 **超时 Promise**：`new Promise((_, reject) => setTimeout(() => reject('Time Limit Exceeded'), t))`  
2. 把它和 `fn(...args)` 用 `Promise.race` 合在一起。  

> **类比**：两只跑步的选手（`fn` 的结果、计时器），先到终点的选手决定比赛结果，另一只即使继续跑也不影响最终判定。

这样既省去了手动维护状态，也让代码更易读、错误更少。

#### 代码（Python）

```python
import asyncio
from typing import Any, Callable, Awaitable

def time_limit(fn: Callable[..., Awaitable], t: int) -> Callable[..., Awaitable]:
    """
    最优实现：利用 asyncio.wait_for（相当于 Promise.race）直接实现超时控制。
    当 fn 在 t 毫秒内完成时返回其结果；否则抛出 "Time Limit Exceeded"。
    """
    async def wrapper(*args: Any, **kwargs: Any):
        # asyncio.wait_for 会在超时后抛 asyncio.TimeoutError，
        # 我们把它转换成题目要求的字符串错误信息。
        try:
            # t 为毫秒，需要除以 1000 转成秒
            return await asyncio.wait_for(fn(*args, **kwargs), timeout=t / 1000)
        except asyncio.TimeoutError:
            # 超时 => 按题意 reject 一个特定的错误信息
            raise TimeoutError("Time Limit Exceeded")
    return wrapper
```

> **关键行中文注释**  
> - `await asyncio.wait_for(..., timeout=t/1000)`：一次性完成「执行」与「超时」的竞争。  
> - `except asyncio.TimeoutError: raise TimeoutError("Time Limit Exceeded")`：把内部的超时异常映射为题目要求的错误字符串。  

> **为什么这已经是最优？**  
> - 只用了语言自带的超时工具，没有额外的状态变量。  
> - 代码行数最少，易于阅读和维护。  
> - 复杂度仍然是 `O(1)`，且实现更“原子”，避免了竞态条件。

#### 复杂度

- **时间复杂度**：`O(1)` —— 与输入规模无关，只是等待 `fn` 完成或超时。  
- **空间复杂度**：`O(1)` —— 只使用了函数栈和 `asyncio` 内部的少量对象。

与暴力解相比，**时间复杂度和空间复杂度完全相同**，但最优解的常数更小、代码更简洁、出错概率更低。

---

## 心得

- **核心技巧**：利用 **Promise.race / asyncio.wait_for** 实现「超时控制」的竞速模型。  
- **适用场景**：  
  1. 给任何可能耗时的异步操作设上「最大执行时间」的限制（如网络请求、文件 I/O）。  
  2. 实现「限时任务」或「倒计时」的游戏/交互逻辑。  
  3. 把多个并行任务中最先完成的结果返回（例如「先到先得」的搜索），这正是 `Promise.race` 的本意。  
- **一句话总结**：**让「函数执行」和「计时器」同时开始，谁先结束谁决定最终结果**。

---

## 反思

- **第一反应**：看到「时间限制」立刻想到 `setTimeout` 配合 `Promise`，或者在 Python 中想到 `asyncio.wait_for`。  
- **最容易踩的坑**：  
  - 忘记把毫秒转成秒（`asyncio.sleep` / `wait_for` 需要秒）。  
  - 超时后直接 `reject` 一个对象而不是题目要求的 `"Time Limit Exceeded"`。  
  - 当 `fn` 本身抛异常时，要把异常原样传出，不能把它误当成超时。  
- **下次第一步**：先问自己「有没有现成的语言特性可以让两个异步操作竞争？」——有的话直接用 `Promise.race` / `asyncio.wait_for`；没有再考虑手动维护标记。