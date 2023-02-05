# #2117. 区间乘积的缩写 / Abbreviating the Product of a Range

> 难度：困难 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/abbreviating-the-product-of-a-range/)

---

## 题目（英文原版）

**Description**

You are given two positive integers left and right with left <= right. Calculate the product of all integers in the inclusive range [left, right].
Since the product may be very large, you will abbreviate it following these steps:
Return a string denoting the abbreviated product of all integers in the inclusive range [left, right].

**Examples**

**Example 1:**

```
Input: left = 1, right = 4
Output: "24e0"
Explanation: The product is 1 × 2 × 3 × 4 = 24.
There are no trailing zeros, so 24 remains the same. The abbreviation will end with "e0".
Since the number of digits is 2, which is less than 10, we do not have to abbreviate it further.
Thus, the final representation is "24e0".
```

**Example 2:**

```
Input: left = 2, right = 11
Output: "399168e2"
Explanation: The product is 39916800.
There are 2 trailing zeros, which we remove to get 399168. The abbreviation will end with "e2".
The number of digits after removing the trailing zeros is 6, so we do not abbreviate it further.
Hence, the abbreviated product is "399168e2".
```

**Example 3:**

```
Input: left = 371, right = 375
Output: "7219856259e3"
Explanation: The product is 7219856259000.
```

**Constraints**

- 1 <= left <= right <= 104

---

## 题目（中文翻译）

你得到两个正整数 `left` 和 `right`，且满足 `left <= right`。计算闭区间 `[left, right]` 中所有整数的乘积（product）。由于乘积可能非常大，需要按以下步骤进行缩写（abbreviation）：

返回一个字符串，表示闭区间 `[left, right]` 中所有整数的缩写乘积。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- `1 <= left <= right <= 10^4`

---

### 示例

#### 示例 1
**输入**: `left = 1, right = 4`  
**输出**: `"24e0"`  
**解释**:  
乘积为 `1 × 2 × 3 × 4 = 24`。  
没有尾随零（trailing zeros），因此保持为 `24`。缩写形式以 `"e0"` 结尾，表示去掉了 0 个尾随零。  
去掉尾随零后的数字位数为 2，小于 10，故不需要进一步缩写。  
最终表示为 `"24e0"`。

#### 示例 2
**输入**: `left = 2, right = 11`  
**输出**: `"399168e2"`  
**解释**:  
乘积为 `39916800`。  
其中有 2 个尾随零，去掉后得到 `399168`。缩写形式以 `"e2"` 结尾，表示去掉了 2 个尾随零。  
去掉尾随零后的数字位数为 6，小于 10，故不需要进一步缩写。  
因此缩写乘积为 `"399168e2"`。

#### 示例 3
**输入**: `left = 371, right = 375`  
**输出**: `"7219856259e3"`  
**解释**:  
乘积为 `7219856259000`。  
去掉 3 个尾随零后得到 `7219856259`，并在末尾加上 `"e3"`，表示去掉了 3 个尾随零。  
数字位数为 10，已满足要求，故最终结果为 `"7219856259e3"`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是把 `[left, right]` 区间里的所有整数全部相乘，得到完整的乘积 `P`，然后再按照题目要求：

1. 把末尾的 `0` 去掉，记住去掉了多少个 `0`（记为 `cntZero`）。  
2. 把剩下的数字转成字符串，如果长度超过 10，就只保留前 5 位和后 5 位，中间用 `...` 省略（本题的描述中只要求返回 **前 5 位 + "e" + cntZero**，这里我们直接把完整的数字输出即可，只要不超过 Python 整数的范围）。  
3. 最后拼成 `"{前5位或全部数字}e{cntZero}"` 返回。

> **类比**：把这一步想象成“把所有水果放进一个大篮子”，然后把篮子里多余的水（末尾的 `0`）倒掉，记录倒了多少水。

**为什么能得到正确答案**  
- 乘积本身一定是所有整数的乘积，直接算出来自然是正确的。  
- 去掉末尾的 `0` 相当于把乘积除以 `10^{cntZero}`，这正是题目要求的“去掉所有尾随零”。  
- 记录除去的 `0` 的个数即是 `cntZero`，再把它放在 `e` 后面即可。

**时间/空间复杂度**  
- **时间复杂度**：我们要遍历 `[left, right]` 中的每个数并做一次乘法，假设区间长度为 `n = right - left + 1`，则时间是 `O(n)`。乘法本身在 Python 的大整数实现里会随位数增长而变慢，但我们这里只用“大白话”说明为 `O(n)`。  
- **空间复杂度**：只需要保存一个大整数 `product`，空间是 `O(1)`（不计入结果字符串本身的空间）。

> **大白话解释**：`O(n)` 就是“随区间里数字的多少线性增长”，如果区间有 1000 个数，就要做 1000 次乘法。`O(1)` 表示不管区间多大，我们只用常数个变量来存东西。

#### 代码（Python）

```python
def abbreviateProduct_bruteforce(left: int, right: int) -> str:
    # 1. 直接算出完整乘积
    product = 1
    for num in range(left, right + 1):
        product *= num                     # 把每个数都乘进去

    # 2. 去掉末尾的 0，统计去掉了多少个
    cnt_zero = 0
    while product % 10 == 0:               # 只要还能被 10 整除，就继续除
        product //= 10
        cnt_zero += 1

    # 3. 把剩余的数字转成字符串
    s = str(product)

    # 4. 题目要求的返回格式
    return f"{s}e{cnt_zero}"
```

#### 复杂度  

- **时间复杂度**：`O(n)`，`n = right - left + 1`，因为我们遍历一次区间并做乘法。  
- **空间复杂度**：`O(1)`，只用常数个变量（`product`, `cnt_zero`, `s`），不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“乘积会非常大”**。  
- 当 `right` 接近 `10^4` 时，区间长度可能有 10,000，乘积的位数会达到几万位，直接算完整乘积会导致 **时间**（大整数乘法的位数成本）和 **空间**（存储巨大的整数）都爆炸。  
- 题目只要求 **“前 5 位 + e + 尾随零的个数”**，所以我们完全不需要保存整个乘积，只要分别算出这三件事：

1. **尾随零的个数** `cntZero`  
   - 乘积中每出现一次因子 `2` 与因子 `5` 的配对，就会产生一个 `10`，即一个尾随零。  
   - 因此 `cntZero = min(total_twos, total_fives)`，其中 `total_twos` 是区间内所有数分解质因数后 `2` 出现的总次数，`total_fives` 同理。  

2. **去掉尾随零后的最后 5 位**（其实本题不需要，但很多变体会用到）  
   - 在遍历每个数时，先把它能贡献的 `2`、`5` 取走（但不要超过 `cntZero`），剩下的部分再取模 `10^5` 累乘，保持只保留低 5 位。  
   - 这里的 **模运算** 类似“只记住最后几位”，相当于把一个很长的数字放进 **只容纳 5 位的盒子**，多余的会被丢掉。  

3. **去掉尾随零后的前 5 位**  
   - 乘积的 **对数** 可以把乘法转换成加法：  
     \[
     \log_{10} P = \sum_{i=left}^{right} \log_{10} i
     \]  
   - 设 `S = Σ log10(i)`，把 `S` 拆成整数部分 `int_part` 和小数部分 `frac_part`。  
   - 前 5 位其实就是 `10^{frac_part + 4}` 的整数部分（因为 `10^{frac_part}` 是首位的 `1~9`，再乘 `10^4` 就把前 5 位搬到小数点左侧）。  
   - 计算时只需要 `float`（双精度）即可，误差在前 5 位以内是安全的。  

综上，我们的 **核心算法** 包含：

- **遍历 + 计数因子**（求 `total_twos`、`total_fives`）  
- **遍历 + 取模**（求去掉零后的最后 5 位）  
- **遍历 + 对数累加**（求去掉零后的前 5 位）  

这些步骤都是 **线性 O(n)**，但每一步只做常数时间的简单操作，根本不产生大整数，空间也只用 `O(1)`。

> **类比**：  
> - 统计 `2`、`5` 就像在超市里统计每种水果的数量，只记录 “有多少个苹果（2）”“有多少个橙子（5）”。  
> - 取模保留后 5 位好比“只记住每个商品的最后五位条码”。  
> - 对数求前 5 位则是“把所有商品的价格先转成对数（相当于把价格的位数压缩），再累加，最后把压缩后的结果展开回去得到前几位”。  

#### 代码（Python）

```python
import math

def abbreviateProduct(left: int, right: int) -> str:
    """
    返回形如 "xxxxxey" 的字符串，其中
    - xxxxx 为去掉尾随零后的前 5 位（如果位数不足 5 位，则全部输出）
    - y 为尾随零的个数
    """
    MOD = 10 ** 5               # 只保留最后 5 位的模数
    total_twos = total_fives = 0
    prod_mod = 1                # 乘积在模 MOD 意义下的值（用于后 5 位，虽非必须）
    log_sum = 0.0               # Σ log10(i)，用于计算前 5 位

    # 先遍历一次，统计 2、5 的出现次数以及累计对数
    for x in range(left, right + 1):
        tmp = x
        # 统计因子 2
        while tmp % 2 == 0:
            total_twos += 1
            tmp //= 2
        # 统计因子 5
        while tmp % 5 == 0:
            total_fives += 1
            tmp //= 5
        # 取模后乘进去（这里的 tmp 已经把所有 2、5 去掉了）
        prod_mod = (prod_mod * (tmp % MOD)) % MOD
        # 对数累加
        log_sum += math.log10(x)

    # 尾随零的个数 = 配对的 (2,5) 最小值
    cnt_zero = min(total_twos, total_fives)

    # 把多余的 2、5（即未配对的那部分）重新乘进去，保持乘积的“实际值”不变
    # 只需要把 (total_twos - cnt_zero) 个 2 和 (total_fives - cnt_zero) 个 5
    # 再次取模，防止数值爆炸
    extra_twos = total_twos - cnt_zero
    extra_fives = total_fives - cnt_zero
    prod_mod = (prod_mod * pow(2, extra_twos, MOD)) % MOD
    prod_mod = (prod_mod * pow(5, extra_fives, MOD)) % MOD

    # ---------- 计算前 5 位 ----------
    # log_sum = log10(P) = int_part + frac_part
    int_part = int(log_sum)
    frac_part = log_sum - int_part
    # 前 5 位 = floor(10^{frac_part + 4})
    first_five = int(10 ** (frac_part + 4))

    # 如果实际位数少于 5 位（比如 left=1,right=4），需要把前 5 位修正为完整数
    # 真实位数 = int_part + 1（因为 log10(P) 的整数部分是位数-1）
    total_digits = int_part + 1
    if total_digits < 5:
        # 此时 prod_mod 已经是完整的（去掉尾随零后）数，因为它本身不足 5 位
        first_five = prod_mod  # 直接使用完整数字

    # ---------- 组装答案 ----------
    return f"{first_five}e{cnt_zero}"
```

**代码要点说明（中文注释已在代码中）**  

- `while tmp % 2 == 0` / `while tmp % 5 == 0`：统计每个数里出现的 `2`、`5` 的次数。  
- `prod_mod` 只在 **去掉所有 `2`、`5`** 后乘进去，防止在后面再次产生多余的零。  
- `pow(base, exp, MOD)`：快速求 `base^exp mod MOD`，相当于 “把大幂次压进只能装 5 位的盒子”。  
- `log_sum` 用 `math.log10` 累加，得到乘积的十进制对数。  
- `first_five = int(10 ** (frac_part + 4))`：把小数部分搬到左边四位，从而得到前 5 位。  
- 最后 `return f"{first_five}e{cnt_zero}"` 即为题目要求的字符串。

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n = right - left + 1`。我们只遍历一次区间，对每个数做常数次的除法、取模、对数运算，全部是 `O(1)` 的操作。  
  - 与暴力解相比，**不再出现位数随乘积指数级增长的额外成本**，所以即使 `n=10^4` 也能在毫秒级完成。  

- **空间复杂度**：`O(1)`。只使用了若干整数变量和一个浮点数 `log_sum`，不随 `n` 增长。

---

## 心得  

- **核心技巧**：利用 **质因数计数** 求尾随零、**模运算** 保留低位、**对数相加** 求首位。  
- **适用的题型**  
  1. “计算区间乘积的前/后若干位”——如 LeetCode 1024、1649 等。  
  2. “统计阶乘或组合数的尾随零”——经典的 `factorial trailing zeros`。  
  3. “大数乘积的前几位/后几位”——常见于数论或概率题。  
- **一句话总结**：**把“大乘积”拆成“计数 2、5 + 取模保留低位 + 对数求高位”，就能在 O(n)·O(1) 的代价得到答案。**

---

## 反思  

- **第一反应**：直接把所有数相乘，然后去掉尾随零。  
- **最容易踩的坑**  
  1. **整数溢出 / 超大内存**：直接乘积会产生几万位的大数，导致运行超时或内存不足。  
  2. **尾随零计数错误**：只统计 `2` 或只统计 `5` 都不对，必须取两者的最小值。  
  3. **对数精度**：使用双精度浮点数时要注意小数部分的误差，确保前 5 位不被四舍五入错误影响。  
  4. **位数不足 5 位的特殊情况**：区间很小的时候需要直接输出完整数字，而不是强行截取 5 位。  

- **下次遇到同类题的第一步**：先判断题目只需要 **“前几位/后几位/尾随零”**，然后 **“把乘积拆成可以单独处理的三块”**（因子计数、模运算、对数），避免直接算完整乘积。