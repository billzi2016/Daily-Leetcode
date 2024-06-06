# #2723. 两个 Promise 求和 / Add Two Promises

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/add-two-promises/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: 
promise1 = new Promise(resolve => setTimeout(() => resolve(2), 20)), 
promise2 = new Promise(resolve => setTimeout(() => resolve(5), 60))
Output: 7
Explanation: The two input promises resolve with the values of 2 and 5 respectively. The returned promise should resolve with a value of 2 + 5 = 7. The time the returned promise resolves is not judged for this problem.
```

**Example 2:**

```
Input: 
promise1 = new Promise(resolve => setTimeout(() => resolve(10), 50)), 
promise2 = new Promise(resolve => setTimeout(() => resolve(-12), 30))
Output: -2
Explanation: The two input promises resolve with the values of 10 and -12 respectively. The returned promise should resolve with a value of 10 + -12 = -2.
```

**Constraints**

- promise1 and promise2 are promises that resolve with a number

---

## 题目（中文翻译）

**描述**  
给定两个 Promise（Promise）对象 `promise1` 和 `promise2`，它们最终都会以数值（number）形式 resolve。实现一个函数，使其返回一个新的 Promise（Promise），该 Promise 在 `promise1` 与 `promise2` 都 resolve 之后，以它们 resolve 值的和 resolve。

> **注意**：返回的 Promise（Promise）何时 resolve 并不在本题的评判范围内，只需要保证它的 resolve 值等于两个输入 Promise（Promise）的 resolve 值之和。

**示例 1**  
```javascript
promise1 = new Promise(resolve => setTimeout(() => resolve(2), 20));
promise2 = new Promise(resolve => setTimeout(() => resolve(5), 60));
```
**输出**: `7`  
**解释**: 两个输入 Promise（Promise）分别以数值 `2` 和 `5` resolve。返回的 Promise（Promise）应以 `2 + 5 = 7` resolve。返回 Promise（Promise）何时 resolve 本题不做判断。

**示例 2**  
```javascript
promise1 = new Promise(resolve => setTimeout(() => resolve(10), 50));
promise2 = new Promise(resolve => setTimeout(() => resolve(-12), 30));
```
**输出**: `-2`  
**解释**: 两个输入 Promise（Promise）分别以数值 `10` 和 `-12` resolve。返回的 Promise（Promise）应以 `10 + -12 = -2` resolve。

**约束条件**  
- `promise1` 与 `promise2` 均为会以数值（number） resolve 的 Promise（Promise）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
- **把 Promise 想成“信封”**：信封里装的是一个数字，但要等到信封被邮递员（异步任务）送达后才能打开。  
- 最直接的办法就是**先打开第一个信封，等它的数字出来后再打开第二个**，把两个数字相加后再装进新的信封返回。  
- 在 Python 里，`Promise` 对应的是 `asyncio.Future` / `awaitable`（可等待对象）。我们只要把两个 `awaitable` 挨个 `await`，就能得到它们的结果。  

这样做是**一定能得到正确答案**的，因为我们严格按照题目要求：等两个 Promise 都 resolved（即都得到数字），再把它们相加。

#### 代码（Python）  
```python
import asyncio
from typing import Awaitable

async def add_two_promises_brute(promise1: Awaitable[int],
                                 promise2: Awaitable[int]) -> int:
    """
    暴力解：依次 await 两个 promise，得到数字后相加。
    """
    # 先等 promise1 完成，拿到第一个数字
    val1 = await promise1          # <-- 等待第一个 promise
    # 再等 promise2 完成，拿到第二个数字
    val2 = await promise2          # <-- 等待第二个 promise
    # 把两个数字相加后返回
    return val1 + val2
```

> **使用示例**（在交互式环境或 `asyncio.run` 中执行）  
> ```python
> async def demo():
>     p1 = asyncio.sleep(0.02, result=2)   # 相当于 setTimeout(resolve(2), 20)
>     p2 = asyncio.sleep(0.06, result=5)   # 相当于 setTimeout(resolve(5), 60)
>     print(await add_two_promises_brute(p1, p2))  # 输出 7
> 
> asyncio.run(demo())
> ```

#### 复杂度  

- **时间复杂度：O(t₁ + t₂)**  
  - `t₁`、`t₂` 分别是两个 promise 完成所需的时间。因为我们是**顺序**等待，必须等完第一个再等第二个，所以总耗时是两者之和。可以把它想成“先排队等 20 ms，再排队等 60 ms”。  
- **空间复杂度：O(1)**  
  - 只用了常数级的额外变量（`val1`、`val2`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于顺序等待**：  
- 如果 `promise1` 需要 20 ms，`promise2` 需要 60 ms，暴力解会耗时 80 ms。  
- 实际上，这两个异步任务是 **可以并行** 的：我们只要把它们同时交给事件循环，让它们“各自跑”，等两个都完成后再相加，整体耗时只会是 **较慢的那一个**（即 `max(t₁, t₂)`），而不是两者相加。

Python `asyncio` 提供了 `asyncio.gather`（或 `await` 多个协程的写法）来一次性等待多个 awaitable 同时完成。  

**核心技巧：并行等待（并发）**  
- 把两个 promise 放进同一个 `gather`，让它们在同一个事件循环中“同时跑”。  
- `gather` 会返回一个包含所有结果的列表，顺序和传入的顺序保持一致。  

> **类比**：把两个信封同时放进邮递员的投递箱，邮递员会把两封信一起送达；我们只需要等“所有信封都到手”这一步，而不是一个接一个地等。

#### 代码（Python）  
```python
import asyncio
from typing import Awaitable, List

async def add_two_promises_opt(promise1: Awaitable[int],
                               promise2: Awaitable[int]) -> int:
    """
    最优解：使用 asyncio.gather 并行等待两个 promise，
    等它们同时完成后再相加。
    """
    # asyncio.gather 会并发地等待所有传入的 awaitable 完成
    # 它返回一个列表，顺序对应传入的顺序
    results: List[int] = await asyncio.gather(promise1, promise2)
    # results[0] 是第一个 promise 的结果，results[1] 是第二个的
    return results[0] + results[1]
```

> **使用示例**  
> ```python
> async def demo_opt():
>     p1 = asyncio.sleep(0.05, result=10)   # 50 ms
>     p2 = asyncio.sleep(0.03, result=-12)  # 30 ms
>     print(await add_two_promises_opt(p1, p2))  # 输出 -2
> 
> asyncio.run(demo_opt())
> ```

#### 复杂度  

- **时间复杂度：O(max(t₁, t₂))**  
  - 两个 promise 同时进行，整体耗时只受最慢的那个限制。相当于“只等最慢的那封信”。  
- **空间复杂度：O(1)**（不计返回值）  
  - `gather` 内部会保存两个结果，但这两个整数本身就是必须的输出，额外的开销仍是常数级。

> 与暴力解对比：如果 `t₁ = 20 ms，t₂ = 60 ms`，暴力解 80 ms，最优解只要 60 ms，快了 **25%**（相当于省下 20 ms 的等待时间）。

---

## 心得  

- **核心技巧**：并行等待（`asyncio.gather` / 多协程并发）。  
- **适用的题型**  
  1. 多个独立的异步请求需要一起处理（如同时请求两个 API 并合并结果）。  
  2. “等待所有任务完成后再统一返回”的场景（比如读取多个文件的内容后一起处理）。  
  3. “任意一个任务完成即返回”的变体可以使用 `asyncio.wait` 或 `asyncio.as_completed`。  
- **解题钥匙**：**先找出可以并行的子任务，再用 `gather` 同时等待**。

---

## 反思  

- **第一反应**：把两个 promise 挨个 `await`，写成最直观的顺序代码。  
- **最容易踩的坑**  
  - 忘记 `await`：直接返回 `promise1 + promise2` 会得到一个协程对象而不是数值。  
  - 错误的并发写法：把 `await` 写在 `gather` 外面（如 `await promise1; await promise2`），仍是顺序等待。  
  - 边界情况：如果其中一个 promise 可能抛异常，`gather` 默认会把异常向上传递，需要自行捕获。  
- **下次类似题的第一步**：先判断“子任务之间是否相互独立”。如果是，就立刻考虑使用 `asyncio.gather`（或其他并发工具）一次性并行等待，而不是顺序 `await`。