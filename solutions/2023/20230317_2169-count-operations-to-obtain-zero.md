# #2169. 计数使数值变为零的操作次数 / Count Operations to Obtain Zero

> 难度：简单 · 标签：Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/count-operations-to-obtain-zero/)

---

## 题目（英文原版）

**Description**

You are given two non-negative integers num1 and num2.
In one operation, if num1 >= num2, you must subtract num2 from num1, otherwise subtract num1 from num2.
Return the number of operations required to make either num1 = 0 or num2 = 0.

**Examples**

**Example 1:**

```
Input: num1 = 2, num2 = 3
Output: 3
Explanation: 
- Operation 1: num1 = 2, num2 = 3. Since num1 < num2, we subtract num1 from num2 and get num1 = 2, num2 = 3 - 2 = 1.
- Operation 2: num1 = 2, num2 = 1. Since num1 > num2, we subtract num2 from num1.
- Operation 3: num1 = 1, num2 = 1. Since num1 == num2, we subtract num2 from num1.
Now num1 = 0 and num2 = 1. Since num1 == 0, we do not need to perform any further operations.
So the total number of operations required is 3.
```

**Example 2:**

```
Input: num1 = 10, num2 = 10
Output: 1
Explanation: 
- Operation 1: num1 = 10, num2 = 10. Since num1 == num2, we subtract num2 from num1 and get num1 = 10 - 10 = 0.
Now num1 = 0 and num2 = 10. Since num1 == 0, we are done.
So the total number of operations required is 1.
```

**Constraints**

- 0 <= num1, num2 <= 105

---

## 题目（中文翻译）

**题目描述**  
给定两个非负整数 `num1` 和 `num2`。  
在一次操作（operation）中：

- 如果 `num1 >= num2`，则必须用 `num2` 减去 `num1`（即 `num1 = num1 - num2`）；
- 否则，用 `num1` 减去 `num2`（即 `num2 = num2 - num1`）。

返回使 `num1 = 0` 或 `num2 = 0` 所需的操作次数。

**示例 1**  
```
输入: num1 = 2, num2 = 3
输出: 3
解释:
- 操作 1: num1 = 2, num2 = 3。因为 num1 < num2，使用 num1 减去 num2，得到 num1 = 2, num2 = 3 - 2 = 1。
- 操作 2: num1 = 2, num2 = 1。因为 num1 > num2，使用 num2 减去 num1，得到 num1 = 2 - 1 = 1, num2 = 1。
- 操作 3: num1 = 1, num2 = 1。因为 num1 == num2，使用 num2 减去 num1，得到 num1 = 1 - 1 = 0, num2 = 1。
此时 num1 = 0，结束。总操作次数为 3。
```

**示例 2**  
```
输入: num1 = 10, num2 = 10
输出: 1
解释:
- 操作 1: num1 = 10, num2 = 10。因为 num1 == num2，使用 num2 减去 num1，得到 num1 = 10 - 10 = 0, num2 = 10。
此时 num1 = 0，结束。总操作次数为 1。
```

**约束条件**  
- `0 <= num1, num2 <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把题目描述的过程一步一步地照搬**下来：  
- 维护两个变量 `a = num1`, `b = num2`。  
- 每一次循环判断 `a >= b` 还是 `a < b`，然后按要求把较大的数减去较小的数。  
- 同时用一个计数器 `cnt` 记录已经执行了多少次减法。  
- 当 `a == 0` 或 `b == 0` 时循环结束，返回计数器。

> **类比**：想象你有两根长度不等的绳子，每次把长的绳子剪掉短的绳子长度，记录剪了多少次，直到一根绳子被剪光为止。

这个方法一定能得到正确答案，因为它严格遵守了题目规定的每一步操作规则，且每一步都让两个数的和严格变小，必然会在有限步数内出现 0。

#### 代码（Python）

```python
def count_operations_bruteforce(num1: int, num2: int) -> int:
    a, b = num1, num2          # 把输入拷贝到局部变量，防止修改原数据
    cnt = 0                    # 记录操作次数

    # 当两数都不为 0 时继续循环
    while a != 0 and b != 0:
        if a >= b:
            a -= b            # 大的减去小的
        else:
            b -= a
        cnt += 1               # 完成一次减法，计数器加一
    return cnt
```

#### 复杂度  

- **时间复杂度：**`O(k)`，其中 `k` 是实际执行的减法次数。最坏情况下（比如 `num1 = 1, num2 = 10⁵`），每次只会把大的数减去 1，导致约 `10⁵` 次循环。可以把它想象成 “每次只走一步”，所以复杂度随数值大小线性增长。  
- **空间复杂度：**`O(1)`，只用了常数个额外变量（`a, b, cnt`），不随输入规模变化。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次只能减去一次较小的数，如果两数相差很大，就会进行大量的循环。  
我们可以借鉴**欧几里得算法**（求最大公约数的过程），它的核心思想是：  
> “把较大的数一次性减去 **若干次** 较小的数”，而不是一次一次地减。

具体来说：

1. 当 `a >= b` 时，`a` 实际上会被 `b` **整除** 若干次后才会小于 `b`。  
2. 这一次性减去的次数正好是 `a // b`（整数除法），于是我们可以直接把 `cnt += a // b`，并把 `a` 更新为 `a % b`（余数）。  
3. 同理，当 `b > a` 时，用 `cnt += b // a`，`b = b % a`。  
4. 重复上述步骤，直到其中一个数为 0。

这样每一步都把较大的数“压缩”成余数，循环次数等同于欧几里得算法的迭代次数，最多是 `O(log min(num1, num2))`，非常快。

> **类比**：如果你有两根绳子，长度分别是 100 和 3。暴力解每次只剪掉 3，需剪 33 次；最优解一次性算出需要剪 33 次，然后直接把 100 换成余数 1，省掉了大量重复操作。

#### 代码（Python）

```python
def count_operations_optimal(num1: int, num2: int) -> int:
    a, b = num1, num2
    cnt = 0

    # 当两数都不为 0 时循环
    while a != 0 and b != 0:
        if a >= b:
            # a 可以减去 b (a // b) 次，余数为 a % b
            cnt += a // b          # 计数一次性减去的次数
            a = a % b              # 更新为余数
        else:
            cnt += b // a
            b = b % a
    return cnt
```

#### 复杂度  

- **时间复杂度：**`O(log min(num1, num2))`。每一次循环都相当于欧几里得算法的一步，数值大小会快速下降，最多只需要对数级别的步数。可以把它想象成 “每次都把大数字切成更小的碎片”，所以即使 `num1`、`num2` 达到 `10⁵`，循环次数也在 20 左右。  
- **空间复杂度：**`O(1)`，同样只用了常数个变量。

---

## 心得

- **核心技巧**：把一次“减一次”转化为“一次性减多次”，即利用整数除法和取余来一次性计数，这实际上是 **欧几里得算法** 的思路。  
- **适用的题型**  
  1. 与两数相减相关的模拟题（如 *“两数相减计数”*）。  
  2. 求最大公约数或最小公倍数的题目（欧几里得算法本身）。  
  3. 需要统计“操作次数”的数论题（如 *“把一个数变成另一个数的最少操作次数”*）。  
- **一句话总结**：**把重复的减法用除法一次算完，计数器直接加上除数的商**。

## 反思

- **第一反应**：直接照搬题目描述，写一个循环不停地减，直到出现 0。  
- **最容易踩的坑**  
  - 忘记在 `a` 或 `b` 为 0 时立即结束循环，导致除以 0 的错误。  
  - 在最优解中，如果直接写 `cnt += a // b` 而没有先判断 `b != 0`，会在 `b = 0` 时抛异常。  
  - 边界情况：`num1 = 0` 或 `num2 = 0` 时，答案应该是 0（因为根本不需要任何操作）。  
- **下次遇到同类题**：第一步先思考“有没有办法一次性完成多次相同的操作？”——如果是减法、加法或乘法，往往可以用除法/乘法/指数来一次性计数，从而把暴力的 `O(k)` 优化到 `O(log n)`。