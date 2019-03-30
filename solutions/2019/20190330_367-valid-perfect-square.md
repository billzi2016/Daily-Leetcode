# #367. 验证完全平方数 / Valid Perfect Square

> 难度：简单 · 标签：Math、Binary Search · [LeetCode 链接](https://leetcode.com/problems/valid-perfect-square/)

---

## 题目（英文原版）

**Description**

Given a positive integer num, return true if num is a perfect square or false otherwise.
A perfect square is an integer that is the square of an integer. In other words, it is the product of some integer with itself.
You must not use any built-in library function, such as sqrt.

**Examples**

**Example 1:**

```
Input: num = 16
Output: true
Explanation: We return true because 4 * 4 = 16 and 4 is an integer.
```

**Example 2:**

```
Input: num = 14
Output: false
Explanation: We return false because 3.742 * 3.742 = 14 and 3.742 is not an integer.
```

**Constraints**

- 1 <= num <= 231 - 1

---

## 题目（中文翻译）

**描述**  
给定一个正整数 `num`，如果 `num` 是完全平方数（perfect square）则返回 `true`，否则返回 `false`。  
完全平方数是某个整数与其自身相乘的结果。换句话说，它是 **整数**（integer） 与自身的乘积。  
要求不能使用任何内置库函数（built‑in library function），例如 `sqrt`。

**示例 1**  
**输入**: `num = 16`  
**输出**: `true`  
**解释**: 返回 `true`，因为 `4 * 4 = 16`，且 `4` 是 **整数**（integer）。

**示例 2**  
**输入**: `num = 14`  
**输出**: `false`  
**解释**: 返回 `false`，因为 `3.742 * 3.742 = 14`，而 `3.742` 不是 **整数**（integer）。

**约束条件**  
- `1 <= num <= 2^31 - 1`   (即 `num` 在 32 位有符号整数范围内)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：从 `1` 开始逐个尝试整数 `i`，把 `i*i`（`i` 的平方）和目标 `num` 比较。  
- **如果 `i*i` 正好等于 `num`**，说明 `num` 是完全平方数，返回 `True`。  
- **如果 `i*i` 已经大于 `num`**，说明后面更大的 `i` 只会让平方更大，`num` 不可能是平方数，直接返回 `False`。

这里用到的唯一数据结构是 **整数**，不需要额外的容器。可以把它想成“把一个盒子里装的球数从 1、2、3… 逐个尝试”，一旦装的球数（平方）超过目标，就可以停下来。

这种方法一定能得到正确答案，因为我们穷举了所有可能的整数 `i`（从 `1` 到 `√num`），不遗漏任何可能的平方根。

#### 代码（Python）

```python
def isPerfectSquare_brute(num: int) -> bool:
    """暴力枚举 i，从 1 开始，检查 i*i 是否等于 num"""
    i = 1
    while i * i <= num:               # 只要 i 的平方不超过 num，就继续尝试
        if i * i == num:               # 找到恰好相等的情况
            return True
        i += 1                         # i 增大，继续下一个整数
    return False                       # 循环结束仍未相等，说明不是完全平方数
```

#### 复杂度  

- **时间复杂度：** `O(√n)`  
  这里的 `√n` 其实是“根号 n”，表示我们最多检查 `1 … √num` 共约 `√num` 次。比如 `num = 10⁶` 时，只会循环约 `1000` 次，而不是一百万次。  
- **空间复杂度：** `O(1)`  
  只用了几个整数变量，空间几乎不随 `num` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **线性遍历**：即使只遍历到 `√num`，当 `num` 很大（如 `2³¹‑1`）时，仍然需要大约 `46340` 次循环，仍有提升空间。  
要加速搜索，我们可以把“在 `[1, num]` 之间找一个整数 `x` 使得 `x*x = num`”的问题转化为 **在有序区间里找目标**，这正是 **二分查找**（Binary Search）擅长的。

二分查找的核心思想：

1. 设定搜索区间 `[left, right]`，最开始 `left = 1`，`right = num`（或 `num // 2 + 1`，因为平方根不会超过 `num/2`，但为了简洁直接用 `num`）。
2. 取区间中点 `mid = (left + right) // 2`，计算 `mid * mid`（注意可能会产生大数，但 Python 整数不溢出）。
3. 与 `num` 比较：
   - 若 `mid*mid == num`，找到了整数平方根，返回 `True`。
   - 若 `mid*mid < num`，说明平方根在右半边，`left = mid + 1`。
   - 若 `mid*mid > num`，说明平方根在左半边，`right = mid - 1`。
4. 循环直到 `left > right`，若仍未相等，则 `num` 不是完全平方数。

把二分查找想象成 **在一本排好序的字典里找单词**：每次都把字典对半分，只查看中间那页的单词，决定往左还是往右继续找，效率远高于逐页翻阅。

#### 代码（Python）

```python
def isPerfectSquare(num: int) -> bool:
    """二分查找判断 num 是否为完全平方数"""
    if num < 2:               # 0、1 本身就是完全平方数（题目保证正整数，这里只处理 1）
        return True

    left, right = 2, num // 2  # 平方根不可能大于 num//2（除 1 之外），从 2 开始搜索
    while left <= right:
        mid = (left + right) // 2
        sq = mid * mid          # mid 的平方

        if sq == num:           # 正好等于 num，找到整数平方根
            return True
        elif sq < num:          # 平方太小，根在右侧
            left = mid + 1
        else:                   # 平方太大，根在左侧
            right = mid - 1
    return False                # 循环结束仍未相等，说明不是完全平方数
```

#### 复杂度  

- **时间复杂度：** `O(log n)`  
  每一次循环把搜索区间大小 **减半**，所以循环次数大约是 `log₂(num)`（对数），对 `2³¹‑1` 也只需要约 31 次迭代。相比暴力的 `√n`（约 46340 次）快了好几个数量级。  
- **空间复杂度：** `O(1)`  
  同样只用了常数个变量，没有额外的递归栈或数组。

---

## 心得

- 这道题的核心技巧是 **二分查找**，把“找平方根”转化为“在有序区间里搜索”。  
- 类似的二分查找题型还有：  
  1. **寻找有序数组中的目标值**（经典 LeetCode 704）  
  2. **在单调函数中求满足条件的最小/最大值**（如 LeetCode 704、744）  
  3. **求整数平方根的整数部分**（LeetCode 69）  
- **一句话总结解题钥匙**：把“遍历全部可能”改成“每次排除一半”，用对数时间快速定位。

---

## 反思

- **第一反应**：直接从 `1` 开始枚举 `i*i`，写出暴力循环。  
- **最容易踩的坑**：  
  - 当 `num` 很大时，`i*i` 可能导致整数溢出（在 C/C++ 语言里），但在 Python 整数自动扩容，这点需要注意。  
  - 边界值 `num = 1`（或者 `0`）要单独处理，否则二分区间会出现 `right = 0` 导致循环不进入。  
- **下次遇到同类题**：第一步先判断是否可以把 “线性搜索” 转化为 “二分搜索” 或者 “单调函数的二分”。确认搜索区间后，快速写出 `mid`、比较、收敛的模板代码。