# #2650. 可取消函数设计 / Design Cancellable Function

> 难度：困难 · 标签： · [LeetCode 链接](https://leetcode.com/problems/design-cancellable-function/)

---

## 题目（英文原版）

**Description**

Sometimes you have a long running task, and you may wish to cancel it before it completes. To help with this goal, write a function cancellable that accepts a generator object and returns an array of two values: a cancel function and a promise.
You may assume the generator function will only yield promises. It is your function's responsibility to pass the values resolved by the promise back to the generator. If the promise rejects, your function should throw that error back to the generator.
If the cancel callback is called before the generator is done, your function should throw an error back to the generator. That error should be the string "Cancelled" (Not an Error object). If the error was caught, the returned promise should resolve with the next value that was yielded or returned. Otherwise, the promise should reject with the thrown error. No more code should be executed.
When the generator is done, the promise your function returned should resolve the value the generator returned. If, however, the generator throws an error, the returned promise should reject with the error.
An example of how your code would be used:
If instead cancel() was not called or was called after t=100ms, the promise would have resolved 5.

**Examples**

**Example 1:**

```
function* tasks() {
  const val = yield new Promise(resolve => resolve(2 + 2));
  yield new Promise(resolve => setTimeout(resolve, 100));
  return val + 1; // calculation shouldn't be done.
}
const [cancel, promise] = cancellable(tasks());
setTimeout(cancel, 50);
promise.catch(console.log); // logs "Cancelled" at t=50ms
```

**Example 2:**

```
Input: 
generatorFunction = function*() { 
  return 42; 
}
cancelledAt = 100
Output: {"resolved": 42}
Explanation:
const generator = generatorFunction();
const [cancel, promise] = cancellable(generator);
setTimeout(cancel, 100);
promise.then(console.log); // resolves 42 at t=0ms

The generator immediately yields 42 and finishes. Because of that, the returned promise immediately resolves 42. Note that cancelling a finished generator does nothing.
```

**Example 3:**

```
Input:
generatorFunction = function*() { 
  const msg = yield new Promise(res => res("Hello")); 
  throw `Error: ${msg}`; 
}
cancelledAt = null
Output: {"rejected": "Error: Hello"}
Explanation:
A promise is yielded. The function handles this by waiting for it to resolve and then passes the resolved value back to the generator. Then an error is thrown which has the effect of causing the promise to reject with the same thrown error.
```

**Example 4:**

```
Input: 
generatorFunction = function*() { 
  yield new Promise(res => setTimeout(res, 200)); 
  return "Success"; 
}
cancelledAt = 100
Output: {"rejected": "Cancelled"}
Explanation:
While the function is waiting for the yielded promise to resolve, cancel() is called. This causes an error message to be sent back to the generator. Since this error is uncaught, the returned promise rejected with this error.
```

**Example 5:**

```
Input:
generatorFunction = function*() { 
  let result = 0; 
  yield new Promise(res => setTimeout(res, 100));
  result += yield new Promise(res => res(1)); 
  yield new Promise(res => setTimeout(res, 100)); 
  result += yield new Promise(res => res(1)); 
  return result;
}
cancelledAt = null
Output: {"resolved": 2}
Explanation:
4 promises are yielded. Two of those promises have their values added to the result. After 200ms, the generator finishes with a value of 2, and that value is resolved by the returned promise.
```

**Example 6:**

```
Input: 
generatorFunction = function*() { 
  let result = 0; 
  try { 
    yield new Promise(res => setTimeout(res, 100)); 
    result += yield new Promise(res => res(1)); 
    yield new Promise(res => setTimeout(res, 100)); 
    result += yield new Promise(res => res(1)); 
  } catch(e) { 
    return result; 
  } 
  return result; 
}
cancelledAt = 150
Output: {"resolved": 1}
Explanation:
The first two yielded promises resolve and cause the result to increment. However, at t=150ms, the generator is cancelled. The error sent to the generator is caught and the result is returned and finally resolved by the returned promise.
```

**Example 7:**

```
Input: 
generatorFunction = function*() { 
  try { 
    yield new Promise((resolve, reject) => reject("Promise Rejected")); 
  } catch(e) { 
    let a = yield new Promise(resolve => resolve(2));
    let b = yield new Promise(resolve => resolve(2)); 
    return a + b; 
  }; 
}
cancelledAt = null
Output: {"resolved": 4}
Explanation:
The first yielded promise immediately rejects. This error is caught. Because the generator hasn't been cancelled, execution continues as usual. It ends up resolving 2 + 2 = 4.
```

**Constraints**

- cancelledAt == null or 0 <= cancelledAt <= 1000
- generatorFunction returns a generator object

---

## 题目（中文翻译）

有时会有一个长期运行的任务，你可能希望在它完成之前将其取消。为此，请实现一个函数 **cancellable**，它接受一个 **生成器（generator）** 对象并返回一个包含两个值的数组：一个 **取消函数（cancel function）** 和一个 **Promise（promise）**。

- 你可以假设生成器函数只会 **yield** **Promise（promise）**。你的函数需要把 **Promise（promise）** 解析后的值传回生成器。如果 **Promise（promise）** 被拒绝（reject），则应把该 **error（error）** 抛回给生成器。
- 如果在生成器完成之前调用了取消函数，函数应向生成器抛出一个错误，该错误的内容必须是字符串 `"Cancelled"`（而不是 `Error` 对象）。  
  - 若该错误被捕获，返回的 **Promise（promise）** 应当以随后 **yield** 出的值（或返回值）**resolve**。  
  - 否则，返回的 **Promise（promise）** 应当 **reject** 该错误，并且不再执行后续代码。
- 当生成器结束时，返回的 **Promise（promise）** 应 **resolve** 生成器返回的值。若生成器抛出错误，则返回的 **Promise（promise）** 应 **reject** 该错误。

下面给出函数的使用示例（若 `cancel()` 未被调用或在 `t = 100ms` 之后才调用，`promise` 将 **resolve** 为 `5`）。

### 示例 1
```javascript
function* tasks() {
  const val = yield new Promise(resolve => resolve(2 + 2));
  yield new Promise(resolve => setTimeout(resolve, 100));
  return val + 1; // 计算不应被执行
}
const [cancel, promise] = cancellable(tasks());
setTimeout(cancel, 50);
promise.catch(console.log); // 在 t=50ms 时输出 "Cancelled"
```

### 示例 2
**输入**  
```javascript
generatorFunction = function*() { 
  return 42; 
}
cancelledAt = 100
```
**输出**  
```json
{"resolved": 42}
```
**解释**  
```javascript
const generator = generatorFunction();
const [cancel, promise] = cancellable(generator);
setTimeout(cancel, 100);
promise.then(console.log); // 在 t=0ms 时 resolve 为 42
```
生成器立即返回 `42` 并结束。因此返回的 **Promise（promise）** 立刻 **resolve** 为 `42`。

### 示例 3
**输入**  
```javascript
generatorFunction = function*() { 
  const msg = yield new Promise(res => res("Hello")); 
  throw `Error: ${msg}`; 
}
cancelledAt = null
```
**输出**  
```json
{"rejected": "Error: Hello"}
```
**解释**  
生成器 **yield** 一个 **Promise（promise）**，该 **Promise（promise）** 解析为 `"Hello"`，随后把该值传回生成器。接着生成器抛出错误 `Error: Hello`，导致返回的 **Promise（promise）** **reject** 该错误。

### 示例 4
**输入**  
```javascript
generatorFunction = function*() { 
  yield new Promise(res => setTimeout(res, 200)); 
  return "Success"; 
}
cancelledAt = 100
```
**输出**  
```json
{"rejected": "Cancelled"}
```
**解释**  
在等待 `yield` 的 **Promise（promise）** 完成期间，`cancel()` 被调用。于是向生成器抛出字符串 `"Cancelled"`。由于该错误未被捕获，返回的 **Promise（promise）** **reject** 为 `"Cancelled"`，且后续代码不再执行。

### 示例 5
**输入**  
```javascript
generatorFunction = function*() { 
  let result = 0; 
  yield new Promise(res => setTimeout(res, 100));
  result += yield new Promise(res => res(1)); 
  yield new Promise(res => setTimeout(res, 100)); 
  result += yield new Promise(res => res(1)); 
  return result;
}
cancelledAt = null
```
**输出**  
```json
{"resolved": 2}
```
**解释**  
共 **yield** 四个 **Promise（promise）**，其中两个返回 `1` 并被累加，最终 **resolve** 为 `2`。

### 示例 6
**输入**  
```javascript
generatorFunction = function*() { 
  let result = 0; 
  try { 
    yield new Promise(res => setTimeout(res, 100)); 
    result += yield new Promise(res => res(1)); 
    yield new Promise(res => setTimeout(res, 100)); 
    result += yield new Promise(res => res(1)); 
  } catch(e) { 
    return result; 
  } 
  return result; 
}
cancelledAt = 150
```
**输出**  
```json
{"resolved": 1}
```
**解释**  
在第二个 `setTimeout` 仍未完成时（约 `t=150ms`）调用 `cancel()`，导致抛出 `"Cancelled"`。该错误在 `catch` 块中被捕获，返回当前累计的 `result`（即 `1`），因此 **Promise（promise）** **resolve** 为 `1`。

### 示例 7
**输入**  
```javascript
generatorFunction = function*() { 
  try { 
    yield new Promise((resolve, reject) => reject("Promise Rejected")); 
  } catch(e) { 
    let a = yield new Promise(resolve => resolve(2));
    let b = yield new Promise(resolve => resolve(2)); 
    return a + b; 
  }; 
}
cancelledAt = null
```
**输出**  
```json
{"resolved": 4}
```
**解释**  
第一个 **yield** 的 **Promise（promise）** 立即被拒绝（reject），错误被 `catch` 捕获。随后两个 **Promise（promise）** 分别解析为 `2`，相加后 **resolve** 为 `4`。

---

**约束条件**

- `cancelledAt == null` 或 `0 <= cancelledAt <= 1000`
- `generatorFunction` 必须返回一个 **生成器（generator）** 对象

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **一步一步顺序执行生成器**，每次 `yield` 出来的都是一个 Promise，等它完成后把结果再 `next` 回去；如果 Promise 被 reject，就把错误 `throw` 回去。  

为了能够在任意时刻把任务“打断”，我们再准备一个 **取消标记**（一个布尔变量）和一个 **取消函数** `cancel()`。  
* `cancel()` 被调用后把标记设为 `true`，并立即向生成器抛出字符串 `"Cancelled"`（而不是 `Error` 对象）。  
* 生成器如果捕获到了这个错误，就可以自行决定返回什么值；如果没有捕获，外层的 `promise` 必须 **reject** 这个错误。  

可以把这套流程想象成 **邮递员**：  
1. 邮递员（我们的 `cancellable`）把一封信（Promise）交给收件人（生成器），  
2. 收件人看完信后回信（`next` 的返回值），邮递员继续送下一封信。  
3. 如果在送信途中收到 “撤回信件” 的指令（`cancel()`），邮递员就把 “Cancelled” 这封信直接塞进收件人的信箱（`generator.throw("Cancelled")`），后面的信件全部不再送。

> 为什么这种办法一定能得到正确答案？  
因为我们严格遵守了 **生成器与外部代码的双向通信协议**：  
- `next(value)` → 把 `yield` 表达式的返回值设为 `value`。  
- `throw(err)` → 把 `err` 当作 `yield` 处抛出的异常。  

只要按照协议一步步走，生成器内部的业务逻辑（无论是普通计算、`try/catch`、`finally`）都会照常执行，最终要么 `return` 一个值，要么抛出一个未捕获的错误。

**复杂度分析**  
- 时间复杂度：`O(k)`，其中 `k` 是生成器实际 `yield` 的次数。每一次都要等对应的 Promise 完成，所以实际耗时由 Promise 本身决定，但在算法层面我们只遍历一次。  
- 空间复杂度：`O(1)`（不计入 Promise 本身占用的内存），因为我们只维护一个标记、一个生成器实例和几个局部变量。

#### 代码（Python）

```python
import asyncio
from typing import Any, Callable, Tuple

def cancellable(gen):
    """
    接收一个已经 **启动**（已经调用了 generatorFunction()）的生成器对象，
    返回 (cancel, promise) 两个东西。
    - cancel: () -> None   # 调用后会向生成器抛出 "Cancelled"
    - promise: asyncio.Future，等同于 JS 中的 Promise
    """
    loop = asyncio.get_event_loop()
    # 用 Future 来模拟外部返回的 Promise
    outer_promise = loop.create_future()
    cancelled = False   # 取消标记

    def cancel():
        nonlocal cancelled
        cancelled = True
        # 立即把 "Cancelled" 抛进生成器
        try:
            gen.throw("Cancelled")
        except StopIteration as e:
            # 生成器在捕获了 Cancelled 后自行返回了结果
            if not outer_promise.done():
                outer_promise.set_result(e.value)
        except Exception as e:
            # 未捕获的 Cancelled 需要让外部 promise reject
            if not outer_promise.done():
                outer_promise.set_exception(e)

    async def run():
        """
        递归地驱动生成器。每一次:
        - 调用 gen.next(value) 或 gen.throw(err)
        - 得到的对象一定是 Promise（这里用 await 对应）
        """
        nonlocal cancelled
        try:
            # 第一次进入生成器，等价于 gen.next()
            yielded = gen.send(None)
        except StopIteration as e:
            # 生成器根本没有 yield，直接返回
            outer_promise.set_result(e.value)
            return
        except Exception as e:
            outer_promise.set_exception(e)
            return

        while True:
            try:
                # 等待当前 yield 出来的 Promise 完成
                result = await yielded
                # 把 Promise 的成功值塞回生成器
                yielded = gen.send(result)
            except Exception as err:
                # Promise 被 reject，或外部调用 cancel 丢进的错误
                try:
                    yielded = gen.throw(err)
                except StopIteration as e:
                    # 生成器捕获了错误并正常结束
                    outer_promise.set_result(e.value)
                    return
                except Exception as e2:
                    # 错误未被捕获，直接让外部 promise 失效
                    outer_promise.set_exception(e2)
                    return
            else:
                # 正常走到这里说明没有异常，继续循环
                pass

    # 启动异步任务（相当于 JS 中的立即执行的 async 函数）
    asyncio.ensure_future(run())
    return cancel, outer_promise
```

> **关键行中文注释**  
> - `cancelled = False`：记录是否已经请求取消。  
> - `gen.throw("Cancelled")`：把字符串 `"Cancelled"` 当作异常抛进生成器。  
> - `yielded = gen.send(result)`：把 Promise 成功的结果传回生成器。  
> - `yielded = gen.throw(err)`：把 Promise 失败的错误（或 Cancelled）抛回生成器。  

#### 复杂度

- **时间复杂度**：`O(k)`，`k` 为 `yield` 次数。每一步只做常数次操作（`send`、`throw`、`await`），所以整体随 `yield` 数线性增长。  
- **空间复杂度**：`O(1)`，只用了几条标记变量和一次递归（这里用 `while` 循环实现），不随 `k` 增长。

---

### 2. 最优解  

#### 思路  

在上面的“暴力”实现里，我们已经把每一步的 **等待**、**传值**、**错误传播** 写得很清晰。  
真正的“瓶颈”并不是时间，而是 **代码的可读性** 与 **对异常/取消的统一处理**。  

我们可以把 **“把 Promise 的结果或错误送回生成器”** 这件事抽象成一个 **辅助函数**，让主循环只关注 **“下一个要处理的 Promise 是哪个”**。  

核心技巧：

| 技巧 | 作用 |
|------|------|
| `async`/`await` | 把异步流程写成同步的线性代码，省去手动 `then/catch` 的嵌套 |
| `generator.throw` | 把错误直接抛进生成器，生成器内部的 `try/catch` 能自动捕获 |
| `asyncio.Future` | 用来模拟外部返回的 Promise，能够在任何时刻 `set_result` / `set_exception` |

**一步步推导**  

1. **把取消变成一次异常**：只要 `cancel()` 被调用，就向生成器抛出 `"Cancelled"`。这和 Promise 被 reject 的情形完全一样——都要走 `generator.throw(err)` 分支。  
2. **统一的“处理一次 yield”**：  
   - `await yielded` → 成功 → `generator.send(value)`  
   - `await yielded` 抛异常 → `generator.throw(err)`  
   - `cancel()` → 直接 `generator.throw("Cancelled")`（同上）  
3. **循环驱动**：只要生成器没有结束（`StopIteration`），就继续取出下一个 `yield` 的 Promise。  

这样做的好处是：

- **时间复杂度仍是 O(k)**，没有额外开销。  
- **代码更短、更易读**，尤其对初学者更友好。  
- **错误/取消的传播路径统一**，不容易遗漏某种情况。

#### 代码（Python）

```python
import asyncio
from typing import Any, Tuple

def cancellable(gen) -> Tuple[Callable[[], None], asyncio.Future]:
    """
    最简洁的实现思路：
    1. 用一个布尔 flag 记录是否已经取消。
    2. 每一次从生成器拿到的 yielded 必定是 Promise（这里用 await）。
    3. 统一的 try/except 把成功值或异常送回生成器。
    """
    loop = asyncio.get_event_loop()
    outer = loop.create_future()          # 对应题目要求返回的 Promise
    cancelled = False                     # 取消标记

    def cancel() -> None:
        nonlocal cancelled
        if cancelled:                     # 防止重复 cancel
            return
        cancelled = True
        try:
            # 直接把 "Cancelled" 抛进生成器
            gen.throw("Cancelled")
        except StopIteration as e:        # 生成器自行捕获并返回了结果
            if not outer.done():
                outer.set_result(e.value)
        except Exception as e:            # 未捕获，外部 promise 需要 reject
            if not outer.done():
                outer.set_exception(e)

    async def drive():
        """
        负责“驱动”生成器的协程。循环体里只处理一次 yield，
        成功或失败的分支都交给统一的异常处理逻辑。
        """
        try:
            # 第一次调用 gen.send(None) 等价于 gen.next()
            yielded = gen.send(None)
        except StopIteration as e:        # 没有 yield，直接返回
            outer.set_result(e.value)
            return
        except Exception as e:
            outer.set_exception(e)
            return

        while True:
            try:
                # 等待当前 Promise 完成
                value = await yielded
                # 把成功值塞回生成器，得到下一个 Promise
                yielded = gen.send(value)
            except Exception as err:        # 包含 Promise reject 与 cancel()
                try:
                    # 把错误抛进生成器，获取下一次 yield（如果有的话）
                    yielded = gen.throw(err)
                except StopIteration as e: # 生成器捕获错误后正常结束
                    outer.set_result(e.value)
                    return
                except Exception as e2:    # 错误未被捕获，外部 promise 失效
                    outer.set_exception(e2)
                    return

    # 把驱动协程提交给事件循环（相当于立刻开始执行）
    asyncio.ensure_future(drive())
    return cancel, outer
```

**代码亮点解释**  

- `cancel()` 只做两件事：标记 `cancelled` 并 **一次性** 把 `"Cancelled"` 抛进生成器。后面的错误传播全部交给 `drive()` 里的统一 `except` 处理。  
- `drive()` 中的 `while True` 循环每次只处理 **一个** `yield`，这样思路非常线性：`await` → `send` / `throw` → 下一轮 `await`。  
- `except StopIteration as e` 捕获到生成器结束时的返回值，立即把它写入外部 `Future`（即题目要求的 Promise）。  

#### 复杂度

- **时间复杂度**：`O(k)`（`k` 为 `yield` 的次数），与暴力解完全相同，只是把每一步的代码压缩成更简洁的形式。  
- **空间复杂度**：`O(1)`，仅使用常数级别的额外变量；所有异步状态都保存在生成器本身和单个 `Future` 中。

---

## 心得  

- **核心技巧**：利用 **生成器的双向通信**（`next` / `send` 与 `throw`）配合 **Promise/async‑await** 完成异步流程的“同步化”。  
- **适用场景**：  
  1. `redux-saga` 那类 **基于 generator 的副作用管理**。  
  2. 需要 **可撤销的异步任务**（如网络请求、动画、定时器）时的封装。  
  3. 实现 **协程调度器**，把一系列异步步骤串成一个看似同步的函数。  
- **一句话总结**：**把每一次 `yield` 当成“等一个 Promise”，把成功值 `send` 回去，错误 `throw` 回去，取消就等价于一次特殊的 `throw`。**  

---

## 反思  

- **第一反应**：把生成器当成普通函数，直接循环 `next()`，忘记了 `yield` 必须等 Promise 完成后才能继续。  
- **最容易踩的坑**：  
  - 忘记在 `cancel()` 里使用 `generator.throw`，导致取消后仍然继续执行后面的 `yield`。  
  - 没有捕获 `StopIteration`，导致外部 Promise 永远不 `resolve`。  
  - 对 **同步返回**（生成器直接 `return`）的情况处理不完整。  
- **下次类似题**的第一步**：先写出“每次 `await` 一个 Promise，成功 `send`，失败 `throw`”的循环框架，再在此框架上加入 `cancel` 标记的处理。这样思路清晰，错误也容易定位。