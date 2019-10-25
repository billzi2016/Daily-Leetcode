# #633. 平方数之和 / Sum of Square Numbers

> 难度：中等 · 标签：Math、Two Pointers、Binary Search · [LeetCode 链接](https://leetcode.com/problems/sum-of-square-numbers/)

---

## 题目（英文原版）

**Description**

Given a non-negative integer c, decide whether there're two integers a and b such that a2 + b2 = c.

**Examples**

**Example 1:**

```
Input: c = 5
Output: true
Explanation: 1 * 1 + 2 * 2 = 5
```

**Example 2:**

```
Input: c = 3
Output: false
```

**Constraints**

- 0 <= c <= 231 - 1

---

## 题目（中文翻译）

**题目描述**  
给定一个非负整数（non‑negative integer）`c`，判断是否存在两个整数（integer）`a` 和 `b` 使得 `a² + b² = c`。

**示例 1**  
``` 
Input: c = 5
Output: true
Explanation: 1 * 1 + 2 * 2 = 5
```

**示例 2**  
``` 
Input: c = 3
Output: false
```

**约束条件**  
- `0 <= c <= 2³¹ - 1`   (即 `c` 的取值范围为 0 到 2³¹‑1)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的整数 `a`、`b` 都枚举一遍，看看是否满足  

```
a² + b² = c
```

- **遍历范围**：因为 `a²`、`b²` 都不可能超过 `c`，所以 `a`、`b` 的取值只需要在 `[0, √c]` 之间。  
- **数据结构**：这里不需要额外的数据结构，单纯用两个 `for` 循环即可。可以把它想象成在一个 **矩阵** 中逐格检查：行号代表 `a`，列号代表 `b`，每格里放的是 `a² + b²`，只要有格子的数等于 `c`，答案就是 `True`。

**为什么正确**  
只要遍历了所有合法的 `(a, b)` 对，就一定能找到满足等式的组合（如果存在的话），所以答案一定是对的。

**时间/空间复杂度**  
- 外层循环跑 `√c + 1` 次，内层循环同样跑 `√c + 1` 次，整体是 `O((√c)²) = O(c)`。  
  用大白话说，就是当 `c` 很大时，程序的运行时间会和 `c` 本身差不多——比如 `c = 10⁶` 时要循环大约一百万次，明显有点慢。  
- 只用了常数级别的额外空间（几个整数变量），所以空间复杂度是 `O(1)`。

#### 代码（Python）

```python
import math

def judgeSquareSum_brute(c: int) -> bool:
    """
    暴力枚举 a、b，检查 a^2 + b^2 是否等于 c
    """
    # a 的取值范围是 0 ~ sqrt(c)
    limit = int(math.isqrt(c))          # math.isqrt 返回整数平方根，避免浮点误差
    for a in range(limit + 1):          # 包含 limit 本身
        a2 = a * a                       # 预先算出 a^2，避免每次循环都乘
        for b in range(limit + 1):
            if a2 + b * b == c:          # 判断是否满足等式
                return True
    return False
```

#### 复杂度

- **时间复杂度**：`O(c)` —— 这里的 `c` 其实是 `√c` 的平方，意思是随着 `c` 增大，循环次数几乎和 `c` 成正比，速度会变慢。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不会随 `c` 增大而占用更多内存。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**双重循环**：每次都把 `a`、`b` 的所有组合都尝试一次。  
观察等式 `a² + b² = c`，如果我们把 `a` 设为一个递增的指针，而让 `b` 从大到小递减，**两指针**的技巧就能把搜索空间压到线性级别 `O(√c)`。

**为什么两指针可行**  

- 当 `a` 取最小值 `0` 时，`b` 必须是 `√c`（或者更小），因为 `b² ≤ c`。  
- 当 `a` 增大时，`a²` 也增大，若此时 `a² + b²` 已经 **大于** `c`，说明 `b` 取得太大，需要把 `b` 往左（减小）移动；  
- 若 `a² + b²` **小于** `c`，说明 `a` 仍然太小，需要把 `a` 往右（增大）移动。  

这就像在一条**有序数轴**上，两个人从两端走向中间，遇到和就停下来，否则根据大小决定谁往前走。

**核心算法**：双指针（Two Pointers）  
- `left`（对应 `a`）从 `0` 开始递增  
- `right`（对应 `b`）从 `⌊√c⌋` 开始递减  
- 每一步计算 `left² + right²`，根据结果调节指针，直至 `left > right`（搜索结束）  

**类比**：想象你在找两块不同重量的砝码，使得它们的总重量恰好等于 `c`。一块砝码从最轻开始递增，另一块从最重开始递减，只要总重量太轻就把轻的那块加重，太重就把重的那块减轻，最终要么找到配对，要么确认不存在。

#### 代码（Python）

```python
import math

def judgeSquareSum(c: int) -> bool:
    """
    双指针法：左指针 a 从 0 增大，右指针 b 从 √c 减小。
    时间 O(√c)，空间 O(1)。
    """
    left = 0
    right = int(math.isqrt(c))          # 最大可能的 b

    while left <= right:                # 只要左指针没有越过右指针，就还有可能
        cur = left * left + right * right   # 计算 a^2 + b^2
        if cur == c:                    # 正好等于 c，找到答案
            return True
        elif cur < c:                   # 和太小，需要让 a 更大（左指针右移）
            left += 1
        else:                           # 和太大，需要让 b 更小（右指针左移）
            right -= 1
    return False                         # 循环结束仍未找到，返回 False
```

#### 复杂度

- **时间复杂度**：`O(√c)` —— 只会遍历一次 `0 … √c`，每次循环都让 `left` 或 `right` 向中间靠拢。用大白话说，就是当 `c = 10⁶` 时，只需要大约一千次循环，速度快了 **千倍**。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和输入大小无关。

---

## 心得

- **核心技巧**：**双指针**（Two Pointers）在有序数值空间里寻找满足特定和的两数组合。  
- **适用题型**  
  1. “Two Sum - Input array is sorted”  
  2. “Find if array contains a pair with given sum”  
  3. 本题 “Sum of Square Numbers” （利用数的平方仍然保持单调递增）  
- **一句话总结**：把问题转化为“在单调序列中寻找两数之和”，用左右指针一步步逼近即可。

---

## 反思

- **第一反应**：直接写双层循环把所有 `a、b` 暴力枚举。  
- **最容易踩的坑**  
  - 忘记 `c` 的上限是 `2³¹‑1`，直接使用 `int(math.sqrt(c))` 可能产生浮点误差，最好用 `math.isqrt`（整数平方根）保证精度。  
  - 边界情况 `c = 0`、`c = 1`：需要确保 `right` 初始为 `0` 或 `1` 时仍然能正常进入循环。  
- **下次遇到同类题**：第一步先判断**是否可以把搜索空间排序或单调化**（本题的平方函数是单调递增），随后立刻想到**双指针**或**二分搜索**来把时间从 `O(N²)` 降到 `O(N)`（或 `O(log N)`）。