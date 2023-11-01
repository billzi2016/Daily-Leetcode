# #2457. 最小加法使整数美观 / Minimum Addition to Make Integer Beautiful

> 难度：中等 · 标签：Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-addition-to-make-integer-beautiful/)

---

## 题目（英文原版）

**Description**

You are given two positive integers n and target.
An integer is considered beautiful if the sum of its digits is less than or equal to target.
Return the minimum non-negative integer x such that n + x is beautiful. The input will be generated such that it is always possible to make n beautiful.

**Examples**

**Example 1:**

```
Input: n = 16, target = 6
Output: 4
Explanation: Initially n is 16 and its digit sum is 1 + 6 = 7. After adding 4, n becomes 20 and digit sum becomes 2 + 0 = 2. It can be shown that we can not make n beautiful with adding non-negative integer less than 4.
```

**Example 2:**

```
Input: n = 467, target = 6
Output: 33
Explanation: Initially n is 467 and its digit sum is 4 + 6 + 7 = 17. After adding 33, n becomes 500 and digit sum becomes 5 + 0 + 0 = 5. It can be shown that we can not make n beautiful with adding non-negative integer less than 33.
```

**Example 3:**

```
Input: n = 1, target = 1
Output: 0
Explanation: Initially n is 1 and its digit sum is 1, which is already smaller than or equal to target.
```

**Constraints**

- 1 <= n <= 1012
- 1 <= target <= 150
- The input will be generated such that it is always possible to make n beautiful.

---

## 题目（中文翻译）

给定两个正整数 `n` 和 `target`。  
如果一个整数的各位数字之和（digit sum）小于等于 `target`，则该整数被视为 **美观**（beautiful）。  
返回最小的非负整数 `x`，使得 `n + x` 为美观整数。题目保证一定可以通过添加某个非负整数使 `n` 变为美观。

## 示例

### 示例 1
**输入:** `n = 16, target = 6`  
**输出:** `4`  
**解释:** 初始 `n` 为 16，数字之和为 `1 + 6 = 7`。加上 4 后，`n` 变为 20，数字之和为 `2 + 0 = 2`。可以证明不存在小于 4 的非负整数能够使 `n` 变为美观。

### 示例 2
**输入:** `n = 467, target = 6`  
**输出:** `33`  
**解释:** 初始 `n` 为 467，数字之和为 `4 + 6 + 7 = 17`。加上 33 后，`n` 变为 500，数字之和为 `5 + 0 + 0 = 5`。可以证明不存在小于 33 的非负整数能够使 `n` 变为美观。

### 示例 3
**输入:** `n = 1, target = 1`  
**输出:** `0`  
**解释:** 初始 `n` 为 1，数字之和为 1，已经小于等于 `target`，因此不需要添加任何数。

## 约束条件

- `1 <= n <= 10^12`
- `1 <= target <= 150`
- 输入保证一定可以使 `n` 变为美观。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**从 0 开始枚举**要加的数 `x`，每次检查 `n + x` 的各位数字之和是否 ≤ `target`，一旦满足条件就返回当前的 `x`。  

- **用到的数据结构**：只需要整数和一个计算数字和的函数。可以把「计算数字和」想象成把一个大数拆成若干个「小纸条」（每个纸条是一个数字），然后把这些纸条的数值全部相加，就像我们在超市里把商品的价格一个个相加一样。  
- **为什么正确**：因为我们从最小的可能值 `0` 开始逐渐递增，只要找到第一个满足条件的 `x`，它必然是最小的非负整数，使得 `n + x` 的数位和 ≤ `target`。  
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(answer × log₁₀ n)**，因为每检查一次 `x` 都要遍历 `n + x` 的所有位（位数大约是 `log₁₀ n`），而最坏情况下 `answer` 可能非常大（比如 `n = 10¹²‑1, target = 1` 时需要加 `1`），所以会超时。  
  - 空间复杂度是 **O(1)**，只用了常数级的变量。

> 大白话解释：  
> - `O(n²)` 里的 `n` 不是题目里的 `n`，而是「我们循环的次数」。如果循环次数是几千、几万甚至上百万，那程序就会慢得像乌龟一样。  

#### 代码（Python）

```python
def digit_sum(x: int) -> int:
    """返回整数 x 各位数字之和。把 x 当成一堆纸条，一张张拿出来相加。"""
    s = 0
    while x:
        s += x % 10      # 取最右边一位
        x //= 10         # 去掉已经取出的那一位
    return s


def min_addition_bruteforce(n: int, target: int) -> int:
    """暴力枚举 x，找到最小的使 (n+x) 的数位和 ≤ target 的 x。"""
    x = 0
    while True:
        if digit_sum(n + x) <= target:   # 检查当前的 n+x 是否满足要求
            return x
        x += 1                            # 继续尝试更大的 x
```

#### 复杂度

- **时间复杂度**：`O(answer × log₁₀ n)`  
  - `answer` 是最终需要加的最小数，`log₁₀ n` 是每次计算数位和要遍历的位数。若 `answer` 很大，程序会非常慢。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，空间几乎可以忽略不计。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**逐个尝试**，每次只加 `1`，导致可能要循环上百万次甚至更多。我们要找一种方式，让每一步都能**跳过**大量不可能的 `x`。  

观察数位和的性质：

1. **把低位变成 0** 能立刻降低数位和。  
   - 例如 `467` → 加 `3` 变成 `470`（最低位 7 变 0，进位到十位），数位和从 `17` 降到 `11`。  
2. **一次把右侧所有非零位全部清零**，再让更高位加 1，能够让数位和下降最多。  
   - 把 `467` 加 `33` 直接变成 `500`，一次把 “6、7” 都变成 0，数位和从 `17` 降到 `5`。  

因此我们可以 **贪心**：每次把最右边的非零位变成 0（必要时向更高位进位），并累计这一步需要加的数值。循环这个过程，直到数位和 ≤ `target`。  

实现细节：

- `inc = 10 - n % 10` 是把最低位变成 0 所需的最小增量（如果最低位已经是 0，`inc` 为 0，直接跳过）。  
- 把 `inc` 加到 `n`，同时把它记到答案 `ans` 中。  
- 由于加法可能会产生进位，`n` 的高位会自动增加，接下来继续检查新的 `n`。  
- 重复上述步骤，最多只需要遍历 **数位的个数**（最多 13 位，因为 `n ≤ 10¹²`），时间非常快。

> 类比：把一个数字想象成一根带有不同颜色珠子的项链。我们每次都把最右侧（最近的）不是白珠的珠子换成白珠（0），并把左边的珠子往前推一个颜色（进位）。这样一次就能把很多彩色珠子一次性换成白珠，快速降低整体的“颜色总量”（即数位和）。

#### 代码（Python）

```python
def digit_sum(x: int) -> int:
    """返回整数 x 各位数字之和（同上）。"""
    s = 0
    while x:
        s += x % 10
        x //= 10
    return s


def min_addition_greedy(n: int, target: int) -> int:
    """
    贪心算法：每次把最低位非零数字变为 0（必要时向更高位进位），
    直至数位和 <= target。
    """
    ans = 0            # 累计需要加的总量
    while digit_sum(n) > target:   # 只要数位和仍然大于目标，就继续处理
        inc = (10 - n % 10) % 10    # 需要加多少才能让最低位变 0
        # 如果最低位已经是 0，inc 为 0，直接跳到更高位
        if inc == 0:                # 这一步是为了避免死循环
            n //= 10                # 把已经是 0 的位直接去掉，继续检查更高位
            continue
        ans += inc                  # 把这一步的增量记到答案里
        n += inc                    # 实际把 n 增大，使最低位变 0（并可能产生进位）
    return ans
```

#### 复杂度

- **时间复杂度**：`O(log₁₀ n)`  
  - 我们最多只会遍历 `n` 的每一位一次（最多 13 次），每次的数位和计算也只需要遍历这些位，所以整体是线性于位数的。相对于暴力的 `answer` 次循环，这几乎是瞬间完成。  
- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量，额外空间常数级。

---

## 心得

- **核心技巧**：**贪心 + 按位处理**。把「把右侧非零位一次性清零」的想法运用到数位和问题上，可以在每一步最大化地降低数位和。  
- **适用的题型**：  
  1. “最小增量使数位和 ≤ k” 类似题（本题即例）。  
  2. “把数字变成下一个回文数”——同样可以按位进位处理。  
  3. “最小加法使数字能被 10 的幂整除”——本质上也是把低位变 0。  
- **一句话总结解题钥匙**：**“每次让最低位‘归零’，并让高位承担进位”，这样可以在最少步数内把数位和降到目标以下。**

## 反思

- **第一反应**：直接想“从 0 开始枚举”，因为这最直观。  
- **最容易踩的坑**：  
  - 忘记对已经是 0 的最低位做特殊处理，导致 `inc = 0` 时循环不前进（死循环）。  
  - 计算 `inc` 时没有取模，可能出现 `inc = 10` 的情况，导致答案多加了一位不必要的 0。  
  - 忽略了 `n` 可能会变得非常大（进位会产生更高位），所以要用 `while digit_sum(n) > target` 而不是一次性检查。  
- **下次遇到同类题**，第一步应该问自己：“能否一次性把某些低位清零并把高位进位？”如果答案是“可以”，那就尝试用**按位贪心**的思路来构造增量。