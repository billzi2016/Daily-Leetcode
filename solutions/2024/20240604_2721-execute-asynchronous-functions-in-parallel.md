# #2721. 并行执行异步函数 / Execute Asynchronous Functions in Parallel

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/execute-asynchronous-functions-in-parallel/)

---

## 题目（英文原版）

**Description**

Given an array of asynchronous functions functions, return a new promise promise. Each function in the array accepts no arguments and returns a promise. All the promises should be executed in parallel.
promise resolves:
promise rejects:
Please solve it without using the built-in Promise.all function.

**Examples**

**Example 1:**

```
Input: functions = [
  () => new Promise(resolve => setTimeout(() => resolve(5), 200))
]
Output: {"t": 200, "resolved": [5]}
Explanation: 
promiseAll(functions).then(console.log); // [5]

The single function was resolved at 200ms with a value of 5.
```

**Example 2:**

```
Input: functions = [
    () => new Promise(resolve => setTimeout(() => resolve(1), 200)), 
    () => new Promise((resolve, reject) => setTimeout(() => reject("Error"), 100))
]
Output: {"t": 100, "rejected": "Error"}
Explanation: Since one of the promises rejected, the returned promise also rejected with the same error at the same time.
```

**Example 3:**

```
Input: functions = [
    () => new Promise(resolve => setTimeout(() => resolve(4), 50)), 
    () => new Promise(resolve => setTimeout(() => resolve(10), 150)), 
    () => new Promise(resolve => setTimeout(() => resolve(16), 100))
]
Output: {"t": 150, "resolved": [4, 10, 16]}
Explanation: All the promises resolved with a value. The returned promise resolved when the last promise resolved.
```

**Constraints**

- functions is an array of functions that returns promises
- 1 <= functions.length <= 10

---

## 题目（中文翻译）

**描述**  
给定一个由异步函数（asynchronous functions）组成的数组 `functions`，返回一个新的 Promise（promise）。数组中的每个函数不接受参数，且返回一个 Promise。所有的 Promise 应并行执行。

- 当所有 Promise 均成功时，返回的 Promise 成功（resolves），并返回所有结果组成的数组。  
- 任意一个 Promise 失败时，返回的 Promise 失败（rejects），并返回相同的错误。

请在实现时不要使用内置的 `Promise.all` 方法。

**示例 1**  
```text
Input: functions = [
  () => new Promise(resolve => setTimeout(() => resolve(5), 200))
]
Output: {"t": 200, "resolved": [5]}
```
**解释**  
`promiseAll(functions).then(console.log); // [5]`  

唯一的函数在 200 ms 后以值 `5` 成功。

**示例 2**  
```text
Input: functions = [
    () => new Promise(resolve => setTimeout(() => resolve(1), 200)), 
    () => new Promise((resolve, reject) => setTimeout(() => reject("Error"), 100))
]
Output: {"t": 100, "rejected": "Error"}
```
**解释**  
由于其中一个 Promise 在 100 ms 时被拒绝，返回的 Promise 也在同一时间以相同的错误被拒绝。

**示例 3**  
```text
Input: functions = [
    () => new Promise(resolve => setTimeout(() => resolve(4), 50)), 
    () => new Promise(resolve => setTimeout(() => resolve(10), 150)), 
    () => new Promise(resolve => setTimeout(() => resolve(16), 100))
]
Output: {"t": 150, "resolved": [4, 10, 16]}
```
**解释**  
所有 Promise 都成功。返回的 Promise 在最后一个 Promise（150 ms）完成时成功，结果为 `[4, 10, 16]`。

**约束条件**  
- `functions` 是一个返回 Promise 的函数数组。  
- `1 <= functions.length <= 10`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **functions** 数组里的每个函数都立刻调用，让它们各自返回一个 Promise。  
随后我们把这些 Promise 放进一个普通的 Python 列表（相当于 JavaScript 里的数组），再用 `for` 循环为每一个 Promise 绑定 `.then`（成功）和 `.catch`（失败）的回调：

- **列表**（list）在这里充当“收集所有 Promise 的容器”。可以把它想象成一本笔记本，里面每一页记下一个异步任务的结果。  
- **计数器** 用来统计已经成功返回结果的任务数。计数器类似于超市收银台前排队的顾客数，所有人都结账完毕，才能算“全部成功”。  
- **标记位**（如 `hasRejected`）记录是否已经出现过失败。因为一旦有一个 Promise 被 reject，整个 `promiseAll` 就应该立刻 reject，后面的成功结果就不需要再等了。

这样做的正确性来源于 **并行执行**：所有函数在同一时刻被调用，它们内部的异步操作（比如 `setTimeout`）会自行调度，互不干扰。我们只需要在回调里收集结果或错误即可。

**时间/空间复杂度**（大白话版）  
- **时间复杂度**：`O(n)`，这里的 `n` 是函数的个数。我们只遍历一次数组来启动所有任务，后面的等待时间取决于最慢的那个 Promise（比如 200 ms），但这不算在 “算法的遍历” 里。  
- **空间复杂度**：`O(n)`，因为我们要存放每个 Promise 的返回值（或错误），相当于为每个任务准备了一个小盒子。

#### 代码（Python）

```python
import asyncio
from typing import Callable, List, Any

# ----------------------------------------------------------------------
# 这里的 functions 是一个列表，列表里的每个元素都是
# “无参函数 → 返回一个 asyncio.Future/Task”
# ----------------------------------------------------------------------
async def promise_all_bruteforce(functions: List[Callable[[], asyncio.Future]]) -> List[Any]:
    """
    暴力实现：手动收集每个 promise 的结果/错误
    """
    n = len(functions)                     # 任务总数
    results = [None] * n                    # 用来保存每个任务的成功结果
    completed = 0                           # 已经成功返回的数量
    has_rejected = False                    # 是否已经出现 reject

    # 为每个函数创建一个 task（相当于启动 promise）
    tasks = [asyncio.create_task(fn()) for fn in functions]

    # 为每个 task 注册回调
    for idx, task in enumerate(tasks):
        # asyncio.Task 本身支持 add_done_callback
        def _make_cb(i):
            def _cb(t: asyncio.Task):
                nonlocal completed, has_rejected
                if has_rejected:                     # 已经 reject 了，直接返回
                    return
                if t.exception():                    # 任务抛出了异常 → reject
                    has_rejected = True
                    # 把异常抛出，让外层的 await 捕获
                    raise t.exception()
                else:                                 # 成功 → 保存结果
                    results[i] = t.result()
                    completed += 1
                    if completed == n:               # 所有任务都成功了
                        # 这里不需要显式 resolve，await 后会直接得到 results
                        pass
            return _cb
        task.add_done_callback(_make_cb(idx))

    # 等待所有 task 完成（如果已经 reject，会在这里抛异常）
    await asyncio.gather(*tasks, return_exceptions=False)
    return results
```

> **关键注释**  
> - `asyncio.create_task(fn())` 相当于立刻执行函数并返回一个 **Promise**（这里是 `Task`）。  
> - `add_done_callback` 用来在 Promise 完成后执行自定义逻辑，类似于 JavaScript 的 `.then/.catch`。  
> - `nonlocal` 让回调能够修改外层函数的计数器和标记位。  

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次 `functions`，每个任务并行执行。  
- **空间复杂度**：`O(n)` —— 需要 `results`、`tasks` 两个长度为 `n` 的列表来保存中间状态。

---

### 2. 最优解  

#### 思路  

暴力解已经能工作，但实现上稍显冗长，尤其是每个任务都要手动写一次回调。  
**瓶颈** 在于：

1. **重复的计数/错误检查**：每个回调里都要写相同的 “已完成吗？”、“是否已经 reject？” 的代码。  
2. **不必要的中间列表**：我们可以直接在 `asyncio.gather` 的回调里收集结果，而不必为每个任务单独保存一个盒子。

优化思路：

- 使用 **计数器**（`remaining`）记录还有多少任务没有结束。每当有任务成功，就把 `remaining` 减 1；当 `remaining` 变成 0 时，就说明所有任务都成功，直接 `resolve`。  
- 一旦有任何任务 **reject**，立刻 `reject` 整个 Promise，并且把剩余的任务全部取消（可选），这样可以避免不必要的等待。  
- 把所有任务的 **回调** 合并到同一个函数里，代码更简洁、可读性更高。

核心概念——**计数器**：把它想象成厨房里还有多少锅在炖菜，只要锅子全都端出来（`remaining == 0`），就可以上菜（`resolve`）。如果哪锅突然烧焦（`reject`），立刻叫停整个厨房（`reject`）。

#### 代码（Python）

```python
import asyncio
from typing import Callable, List, Any

async def promise_all_opt(functions: List[Callable[[], asyncio.Future]]) -> List[Any]:
    """
    更简洁的实现：用计数器和一次性回调完成所有任务的收集。
    """
    n = len(functions)
    results = [None] * n          # 保存成功结果，顺序和 functions 保持一致
    remaining = n                 # 还剩多少任务未完成
    loop = asyncio.get_event_loop()
    # 创建一个 Future，充当我们要返回的 “整体 Promise”
    overall = loop.create_future()

    async def wrapper(idx: int, coro):
        """
        为每个任务单独包装一层，统一在这里处理成功/失败。
        """
        nonlocal remaining
        try:
            res = await coro               # 等待单个任务完成
            results[idx] = res             # 保存对应位置的结果
            remaining -= 1                 # 计数器减一
            if remaining == 0 and not overall.done():
                overall.set_result(results)   # 所有任务成功 → resolve
        except Exception as e:
            if not overall.done():
                overall.set_exception(e)      # 任意任务失败 → reject
            # 可选：取消其余仍在执行的任务，以免浪费资源
            # for t in pending:
            #     t.cancel()

    # 启动所有任务
    pending = [asyncio.create_task(wrapper(i, fn())) for i, fn in enumerate(functions)]

    # 等待 overall 完成（成功或失败都会在这里结束）
    return await overall
```

> **关键注释**  
> - `overall` 是我们手动创建的 “总 Promise”。`set_result` 相当于 `resolve`，`set_exception` 相当于 `reject`。  
> - `wrapper` 把每个单独的 Promise 包装成统一的成功/失败处理流程，内部只用一次 `try/except`，代码更集中。  
> - `remaining` 计数器在每次成功后递减，等于 0 时说明所有任务都已经成功，直接 `resolve`。  

#### 复杂度  

- **时间复杂度**：`O(n)` —— 仍然只遍历一次函数列表，所有任务并行执行。相比暴力解，额外的包装函数只增加了常数级的开销。  
- **空间复杂度**：`O(n)` —— 需要保存 `results`、`pending` 两个长度为 `n` 的列表，以及一个计数器。

---

## 心得  

- **核心技巧**：使用计数器（或剩余任务数）配合统一的 `Future/Promise` 来收集并行任务的结果，并在任意任务失败时立刻 `reject`。  
- **适用场景**：  
  1. 实现 `Promise.all`、`Promise.allSettled`、`Promise.race` 等并行控制工具。  
  2. 多个独立的网络请求、文件读写或计时任务需要同时发起，并在全部完成后统一处理。  
  3. 并行计算（如多线程/多进程）中，需要等待全部子任务结束才能继续的情形。  
- **一句话总结**：**“用一个计数器记录还有多少任务未完成，一旦计数归零即 resolve；若任意任务抛错立即 reject”。**

---

## 反思  

- **第一反应**：看到 “所有 promise 并行执行，返回一个新 promise”，马上想到 `Promise.all`，于是尝试自己手写 `then/catch` 收集。  
- **最容易踩的坑**：  
  - **忘记保持结果顺序**：即使任务完成顺序不同，也必须把结果放回原来的下标位置。  
  - **多次 resolve/reject**：如果在某个任务 reject 后仍然继续调用 `resolve`（比如计数器仍在递减），会导致异常。必须在 `overall.done()` 前检查。  
  - **异常未捕获**：在 `async` 包装函数里一定要 `try/except`，否则异常会直接冒泡导致整个协程挂掉。  
- **下次思路**：遇到类似 “等待一批异步任务的整体结果” 时，先在脑中构建 “计数器 + 统一 Future” 的模型，然后把每个子任务包装进统一的回调里，确保 **一次成功或一次失败** 即可决定整体 Promise 的状态。