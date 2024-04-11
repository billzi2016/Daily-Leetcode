# #2648. 生成斐波那契序列 / Generate Fibonacci Sequence

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/generate-fibonacci-sequence/)

---

## 题目（英文原版）

**Description**

Write a generator function that returns a generator object which yields the fibonacci sequence.
The fibonacci sequence is defined by the relation Xn = Xn-1 + Xn-2.
The first few numbers of the series are 0, 1, 1, 2, 3, 5, 8, 13.

**Examples**

**Example 1:**

```
Input: callCount = 5
Output: [0,1,1,2,3]
Explanation:
const gen = fibGenerator();
gen.next().value; // 0
gen.next().value; // 1
gen.next().value; // 1
gen.next().value; // 2
gen.next().value; // 3
```

**Example 2:**

```
Input: callCount = 0
Output: []
Explanation: gen.next() is never called so nothing is outputted
```

**Constraints**

- 0 <= callCount <= 50

---

## 题目（中文翻译）

编写一个生成器函数（generator function），返回一个生成器对象（generator object），该对象按顺序产生斐波那契序列（fibonacci sequence）的值。斐波那契序列满足关系式 `Xn = Xn-1 + Xn-2`。序列的前几项为 `0, 1, 1, 2, 3, 5, 8, 13`。

示例 1  
Input: `callCount = 5`  
Output: `[0,1,1,2,3]`  
Explanation:  
```javascript
const gen = fibGenerator();
gen.next().value; // 0
gen.next().value; // 1
gen.next().value; // 1
gen.next().value; // 2
gen.next().value; // 3
```

示例 2  
Input: `callCount = 0`  
Output: `[]`  
Explanation:  
```javascript
// gen.next() 从未被调用，因此没有输出
```

约束条件  
- `0 <= callCount <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的办法是**一次性把前 `callCount` 个斐波那契数全部算出来**，放进一个普通的 Python 列表，然后返回这个列表。  
- **用到的数据结构**：列表（list），就像我们日常使用的“装东西的盒子”，可以随时往里塞元素，也可以按顺序取出来。  
- **为什么正确**：斐波那契数的定义是 `F[n] = F[n‑1] + F[n‑2]`（前两项相加得到下一项），只要我们严格按照这个递推公式从第 0 项开始往后算，就一定会得到正确的序列。  
- **大白话的复杂度解释**：如果 `callCount = n`，我们要算 `n` 次循环，每一次循环里只做一次加法和一次赋值，整体工作量随 `n` 成正比，这在算法里记作 **O(n)**。如果把所有结果都放进列表，列表本身也会占用 `n` 个位置的空间，同样是 **O(n)**。

#### 代码（Python）  

```python
def fib_bruteforce(callCount: int):
    """
    暴力实现：一次性返回前 callCount 个斐波那契数的列表
    """
    # 特殊情况：不需要任何数时直接返回空列表
    if callCount <= 0:
        return []

    # 初始化结果列表，先放入已知的前两项 0 和 1
    result = [0, 1]

    # 如果只需要 1 项，直接截断返回
    if callCount == 1:
        return result[:1]

    # 从第 3 项开始循环计算，直到得到 callCount 项
    while len(result) < callCount:
        # 前两项之和就是下一项
        next_val = result[-1] + result[-2]
        result.append(next_val)   # 把新数放进列表

    # 只保留前 callCount 项（防止 callCount == 2 时多算了一项）
    return result[:callCount]
```

#### 复杂度  

- **时间复杂度：O(n)** — “n” 就是 `callCount`，我们循环 n‑2 次，每次做常数时间的加法。  
- **空间复杂度：O(n)** — 需要一个长度为 n 的列表来存放所有结果。  

---  

### 2. 最优解  

#### 思路  
暴力解的**瓶颈**在于**一次性把所有结果都存下来**，这会占用额外的 O(n) 空间。  
如果题目只要求“逐个返回”斐波那契数，而不是一次性全部拿到，**生成器**（generator）是更合适的工具。  

生成器的工作方式可以类比为**“自动售货机”**：  
- 每调用一次 `next()`，机器就**立刻**给你一个商品（这里是下一个斐波那契数），  
- 然后**暂停**，等你下次再按按钮（再次调用 `next()`）时，才继续往下工作。  

实现思路如下：  

1. **先 `yield` 0 和 1**，对应斐波那契数列的前两项。  
2. 进入一个 **无限循环** `while True:`，在循环内部：  
   - 用两个变量 `a`、`b` 保存最近的两个数。  
   - 计算 `c = a + b`，这就是下一个斐波那契数。  
   - `yield c` 把它返回给调用者。  
   - 然后把 `a, b` 向后移动：`a = b, b = c`，为下一次迭代做准备。  

因为生成器**按需产生**数值，**只在调用时才计算**，所以它的空间占用只需要保存两个最近的数，即 **O(1)**（常数空间），而时间仍然是每次调用一次 O(1)。  

#### 代码（Python）  

```python
def fib_generator():
    """
    生成器函数：每次调用 next() 时产生下一个斐波那契数
    使用方式：
        gen = fib_generator()
        gen.__next__().   # 或者 next(gen)
    """
    # 第 0 项和第 1 项，直接给出
    a, b = 0, 1
    yield a            # 产生 0
    yield b            # 产生 1

    # 无限循环，每次产生下一个数
    while True:
        c = a + b      # 计算下一个斐波那契数
        yield c        # 把它返回给调用者
        a, b = b, c    # 更新 a、b 为最近的两项，准备下一轮
```

> **使用示例**（对应题目示例）  

```python
def take(gen, k):
    """帮助函数：从生成器中取前 k 个值，返回列表"""
    return [next(gen) for _ in range(k)]

# 示例 1：callCount = 5
gen = fib_generator()
print(take(gen, 5))   # 输出 [0, 1, 1, 2, 3]

# 示例 2：callCount = 0
gen = fib_generator()
print(take(gen, 0))   # 输出 []，因为没有调用 next()
```

#### 复杂度  

- **时间复杂度：O(k)** — 取前 `k` 项需要调用 `next()` `k` 次，每次都是常数时间的加法。  
- **空间复杂度：O(1)** — 生成器内部只保存两个整数 (`a`, `b`) ，与 `k` 无关，属于常数空间。  

相比暴力一次性创建列表的 **O(k) 空间**，生成器大幅降低了内存使用，尤其当 `k` 很大（如 10⁶）时优势更明显。  

---  

## 心得  

- **核心技巧**：**生成器（generator）** 以及 **无限循环 + 按需 `yield`**。  
- **适用的题型**：  
  1. “**斐波那契数列**”这类递推数列的按序输出。  
  2. “**遍历无限序列**” 如素数序列、自然数序列等。  
  3. “**流式数据处理**”——一次只处理一个数据块，避免一次性全部加载。  
- **一句话总结解题钥匙**：**“用生成器把‘先算后存’改成‘算了再给’，空间自然省下来”。**  

---  

## 反思  

- **第一反应**：把所有要的数一次性算完放进列表，直接返回。  
- **最容易踩的坑**：  
  - 忘记在 `callCount = 0` 时不调用 `next()`，导致返回不应出现的数。  
  - 在生成器实现里，忘记先 `yield` 前两项，导致序列从 `1,2,3...` 开始错误。  
  - 无限循环如果不正确更新 `a, b`，会产生错误的序列甚至死循环。  
- **下次遇到同类题**：第一步想到 **“这是不是可以用生成器按需产生？”**，如果答案是肯定的，就立刻把递推公式写进 `while True:` 循环并 `yield`。