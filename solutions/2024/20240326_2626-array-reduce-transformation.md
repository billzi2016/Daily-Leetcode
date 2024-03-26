# #2626. 数组归约转换 / Array Reduce Transformation

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/array-reduce-transformation/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, a reducer function fn, and an initial value init, return the final result obtained by executing the fn function on each element of the array, sequentially, passing in the return value from the calculation on the preceding element.
This result is achieved through the following operations: val = fn(init, nums[0]), val = fn(val, nums[1]), val = fn(val, nums[2]), ... until every element in the array has been processed. The ultimate value of val is then returned.
If the length of the array is 0, the function should return init.
Please solve it without using the built-in Array.reduce method.

**Examples**

**Example 1:**

```
Input: 
nums = [1,2,3,4]
fn = function sum(accum, curr) { return accum + curr; }
init = 0
Output: 10
Explanation:
initially, the value is init=0.
(0) + nums[0] = 1
(1) + nums[1] = 3
(3) + nums[2] = 6
(6) + nums[3] = 10
The final answer is 10.
```

**Example 2:**

```
Input: 
nums = [1,2,3,4]
fn = function sum(accum, curr) { return accum + curr * curr; }
init = 100
Output: 130
Explanation:
initially, the value is init=100.
(100) + nums[0] * nums[0] = 101
(101) + nums[1] * nums[1] = 105
(105) + nums[2] * nums[2] = 114
(114) + nums[3] * nums[3] = 130
The final answer is 130.
```

**Example 3:**

```
Input: 
nums = []
fn = function sum(accum, curr) { return 0; }
init = 25
Output: 25
Explanation: For empty arrays, the answer is always init.
```

**Constraints**

- 0 <= nums.length <= 1000
- 0 <= nums[i] <= 1000
- 0 <= init <= 1000

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`、一个归约函数 `fn`（reducer function），以及一个初始值 `init`，返回对数组中每个元素依次执行 `fn` 后得到的最终结果。每次调用 `fn` 时，都把前一次计算得到的返回值作为累计值传入。

实现过程如下：

```
val = fn(init, nums[0])
val = fn(val, nums[1])
val = fn(val, nums[2])
...
```

直至数组中的所有元素均被处理完毕，最终返回 `val`。  
如果数组长度为 `0`，函数应直接返回 `init`。  
请在实现时不要使用内置的 `Array.reduce` 方法。

---

### 示例

**示例 1**  
```text
Input: 
nums = [1,2,3,4]
fn = function sum(accum, curr) { return accum + curr; }
init = 0
Output: 10
Explanation:
initially, the value is init=0.
(0) + nums[0] = 1
(1) + nums[1] = 3
(3) + nums[2] = 6
(6) + nums[3] = 10
The final answer is 10.
```

**示例 2**  
```text
Input: 
nums = [1,2,3,4]
fn = function sum(accum, curr) { return accum + curr * curr; }
init = 100
Output: 130
Explanation:
initially, the value is init=100.
(100) + nums[0] * nums[0] = 101
(101) + nums[1] * nums[1] = 105
(105) + nums[2] * nums[2] = 114
(114) + nums[3] * nums[3] = 130
The final answer is 130.
```

**示例 3**  
```text
Input: 
nums = []
fn = function sum(accum, curr) { return 0; }
init = 25
Output: 25
Explanation: For empty arrays, the answer is always init.
```

---

### 约束条件
- `0 <= nums.length <= 1000`
- `0 <= nums[i] <= 1000`
- `0 <= init <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把题目描述的“顺序把每个元素交给 reducer 函数”照搬出来。  
- **数据结构**：只需要一个普通的列表 `nums`，以及一个变量 `res` 用来保存“累计值”。可以把 `res` 想象成一本记事本，记下每一步的结果。  
- **为什么正确**：题目说每一步的输入都是上一步的返回值，再加上当前数组元素。只要我们严格按照这个顺序执行，就一定会得到题目要求的最终结果。  
- **时间/空间复杂度**：我们遍历一次数组，对每个元素调用一次 `fn`，所以时间是 **O(n)**（n 为数组长度）。只用了常数个额外变量（`res`、循环计数器），空间是 **O(1)**。  
> 大白话解释：如果数组有 5 个数，我们就会跑 5 步，每一步都花一点时间（调用一次函数），所以时间跟数组有多长成正比。空间只占几块纸，跟数组大小无关。

#### 代码（Python）  

```python
from typing import List, Callable, Any

def array_reduce(nums: List[int], fn: Callable[[Any, int], Any], init: Any) -> Any:
    """
    暴力实现：遍历 nums，逐个把累计值 res 与当前元素交给 fn，返回最终结果。
    """
    res = init                     # 先把累计值设为 init，像记事本里写下“起点”
    for i, cur in enumerate(nums):
        # 调用 reducer，得到新累计值
        res = fn(res, cur)        # 这里的 fn 就像一本“自定义的计算手册”
        # 可选：打印调试信息帮助理解
        # print(f"第 {i} 步: fn({res}, {cur}) -> {res}")
    return res                     # 循环结束，返回记事本里最后的数
```

#### 复杂度  
- **时间复杂度**：`O(n)` — 需要遍历一次数组，n 越大，花的时间越多。  
- **空间复杂度**：`O(1)` — 只用了几个变量，和数组长度无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解看，唯一的**瓶颈**是遍历数组的次数。  
- 如果我们不遍历一次，就根本不知道每个元素该怎么累计，**不可能更快**。  
- 因此 **线性遍历一次** 已经是最优的时间复杂度 `O(n)`。  
- 同时我们只需要保存当前的累计值 `res`，不必额外的数组或栈，空间 `O(1)` 已经是最低的。  

所以最优解和直觉解本质上是同一个实现，只是把它称作“最优”。下面的代码把 **函数签名** 写得更“Pythonic”，并演示了如何把任意的 Python 函数（比如 `lambda x, y: x + y`）当作 `fn` 传进去。

#### 代码（Python）  

```python
from typing import List, Callable, Any

def array_reduce_opt(nums: List[int], fn: Callable[[Any, int], Any], init: Any) -> Any:
    """
    最优实现：一次遍历 + 常数额外空间。
    """
    # 1. 初始化累计值
    acc = init

    # 2. 逐个处理数组元素
    for num in nums:
        # 把当前累计值和当前元素交给 fn，得到新的累计值
        acc = fn(acc, num)

    # 3. 返回最终累计值
    return acc
```

#### 复杂度  
- **时间复杂度**：`O(n)` — 与暴力解相同，已经是理论下界，无法再快。  
- **空间复杂度**：`O(1)` — 只用一个额外变量 `acc`，最小空间占用。  

---

## 心得  

- **核心技巧**：**一次遍历 + 累计变量**（类似“前缀和”思想），把每一步的结果保留下来供下一步使用。  
- **适用的题型**：  
  1. 累计求和 / 乘积（如 LeetCode 统计数组元素之和）。  
  2. 累计求最大/最小值（如求数组的前缀最大）。  
  3. 自定义累积操作（如把字符串列表拼接成一句话）。  
- **一句话总结**：只要题目要求“把前一次的结果继续往下传”，**循环一次、用一个变量记录累计值** 就是钥匙。  

## 反思  

- **第一反应**：看到“reduce”，立刻想到要把数组“压缩”为一个值，于是想到遍历一次、用 `res = fn(res, cur)`。  
- **最容易踩的坑**：  
  - 忘记处理空数组的情况，直接在循环里访问 `nums[0]` 会报错。正确做法是先把 `res` 设为 `init`，若数组为空直接返回 `init`。  
  - `fn` 的返回类型可能和 `init` 不同（比如返回字符串），所以在写类型注解时使用 `Any` 更安全。  
- **下次遇到同类题**：第一步就想 “**有没有只需要一次遍历就能把所有信息累计起来？**”——如果答案是肯定的，就直接写累计循环。