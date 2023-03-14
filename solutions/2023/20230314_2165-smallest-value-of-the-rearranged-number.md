# #2165. 重新排列数字后的最小值 / Smallest Value of the Rearranged Number

> 难度：中等 · 标签：Math、Sorting · [LeetCode 链接](https://leetcode.com/problems/smallest-value-of-the-rearranged-number/)

---

## 题目（英文原版）

**Description**

You are given an integer num. Rearrange the digits of num such that its value is minimized and it does not contain any leading zeros.
Return the rearranged number with minimal value.
Note that the sign of the number does not change after rearranging the digits.

**Examples**

**Example 1:**

```
Input: num = 310
Output: 103
Explanation: The possible arrangements for the digits of 310 are 013, 031, 103, 130, 301, 310. 
The arrangement with the smallest value that does not contain any leading zeros is 103.
```

**Example 2:**

```
Input: num = -7605
Output: -7650
Explanation: Some possible arrangements for the digits of -7605 are -7650, -6705, -5076, -0567.
The arrangement with the smallest value that does not contain any leading zeros is -7650.
```

**Constraints**

- -1015 <= num <= 1015

---

## 题目（中文翻译）

给定一个整数 `num`。请重新排列 `num` 的各位数字，使得得到的数值最小且**不含前导零**（leading zeros）。返回该最小值的重新排列结果。  
注意，重新排列数字后 **符号**（sign）保持不变，即正数仍为正数，负数仍为负数。

## 示例

**示例 1**  
```
Input: num = 310
Output: 103
```
**解释**：310 的各位数字可能的排列有 013、031、103、130、301、310。  
在这些排列中，**不含前导零**且数值最小的是 103。

**示例 2**  
```
Input: num = -7605
Output: -7650
```
**解释**：-7605 的各位数字可能的排列有 -7650、-6705、-5076、-0567。  
在这些排列中，**不含前导零**且数值最小的是 -7650。

## 约束条件

- \(-10^{15} \leq \text{num} \leq 10^{15}\)   (即 \(-1015 <= num <= 1015\))

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有数字的排列** 都列举出来，挑出满足「没有前导零」且「符号不变」的最小（或最大）值。

- **数据结构**  
  - **列表** 用来保存每个数字字符。  
  - **哈希表**（这里用 `set`）可以帮助我们去重，防止相同排列被多算一次。把哈希表想象成「字典」：我们把已经检查过的排列记下来，下一次再出现同样的排列时直接跳过。

- **为什么正确**  
  把所有可能的排列都遍历一遍，必然会包括答案。只要我们在遍历时过滤掉「以 0 开头」的情况（因为题目不允许前导零），剩下的最小（正数）或最小（负数，即数值最小）就是我们要的结果。

- **复杂度分析（大白话）**  
  - 假设数字有 `k` 位，排列数是 `k!`（即 1×2×3…×k），这在实际里会非常大（比如 10 位就有 3,628,800 种）。  
  - 对每一种排列，我们要把字符列表拼成整数，这一步是 `O(k)`。  
  - 所以 **时间复杂度** 是 `O(k! * k)`，意思是「随位数的阶乘增长，几乎不可能在大数据下跑完」。  
  - **空间复杂度**：需要保存当前的排列和去重集合，最多 `O(k!)`（最坏情况全部不重复），但实际只要 `O(k)` 的临时列表即可。

#### 代码（Python）

```python
import itertools

def smallestNumber_bruteforce(num: int) -> int:
    # 1️⃣ 先把符号和数字分开
    sign = -1 if num < 0 else 1
    digits = list(str(abs(num)))               # 把每位数字当作字符存入列表

    best = None                                 # 用来记录目前找到的最小（或最大）答案

    # 2️⃣ 枚举所有排列，itertools.permutations 会返回一个生成器，省内存
    for perm in set(itertools.permutations(digits)):
        # 3️⃣ 跳过前导零的情况
        if perm[0] == '0':
            continue

        # 4️⃣ 把字符元组拼成整数，并恢复原来的符号
        candidate = sign * int(''.join(perm))

        # 5️⃣ 更新答案
        if best is None:
            best = candidate
        else:
            # 对正数我们要更小的，对负数我们要更小（即数值更负）
            if candidate < best:
                best = candidate

    return best if best is not None else 0   # 只会在 num == 0 时走到这里
```

#### 复杂度

- **时间复杂度**：`O(k! * k)`  
  > 「k!」是所有排列的数量，「k」是把每个排列转成整数的代价。对 10 位数字来说已经是几百万次循环，实际不可接受。

- **空间复杂度**：`O(k!)`（去重集合）  
  > 虽然我们用 `set` 去重，但最坏情况下仍然要保存所有不同排列，空间随位数指数增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「枚举所有排列」。实际上我们只需要 **一次排序** 就能得到答案，因为题目只要求「最小的」而不是「所有可能的」。

- **正数**  
  1. 把数字从小到大排（升序）。  
  2. 如果最小的那位是 `0`，说明出现了前导零。我们把第一个非零的最小数字换到最前面，其余保持升序。  
  这一步可以类比为「把所有小石子从左到右排好，如果左边的第一块是透明的（0），就把第一块不透明的石子（>0）搬到最左边」。

- **负数**  
  负数的符号不变，数值越小（越负）其实 **绝对值越大**。所以我们让绝对值尽可能大：把数字从大到小排（降序），直接拼起来即可。  
  想象把「重量」最大的石子放在最前面，整条链就会更沉（数值更小）。

- **核心工具**：**排序**（Python 的 `sorted`）和 **一次遍历** 找到第一个非零数字。排序的时间复杂度是 `O(k log k)`，已经是最优的理论下界，因为我们必须看完每一位数字。

#### 代码（Python）

```python
def smallestNumber(num: int) -> int:
    # 0 是特例，直接返回
    if num == 0:
        return 0

    sign = -1 if num < 0 else 1                 # 记录符号
    digits = list(str(abs(num)))                # 取绝对值后转成字符列表

    if sign > 0:                                # 正数
        digits.sort()                           # 升序排列
        # 若首位是 '0'，需要把第一个非零数字换到最前面
        if digits[0] == '0':
            # 找到第一个不为 '0' 的下标
            for i, d in enumerate(digits):
                if d != '0':
                    # 把它和首位交换
                    digits[0], digits[i] = digits[i], digits[0]
                    break
        result = int(''.join(digits))           # 合成整数
    else:                                        # 负数
        digits.sort(reverse=True)                # 降序排列，绝对值最大化
        result = -int(''.join(digits))           # 再加回负号

    return result
```

#### 复杂度

- **时间复杂度**：`O(k log k)`  
  > `k` 是数字的位数（最多 16 位），排序需要 `k log k` 的时间。相比暴力的阶乘级别，快了很多——即使是 16 位也只需要几百次比较。

- **空间复杂度**：`O(k)`  
  > 只用了一个保存数字字符的列表和若干临时变量，和位数线性相关。

---

## 心得

- **核心技巧**：**根据符号选择升序或降序排序，再处理正数的前导零**。  
- **适用的题型**：  
  1. “把数字重新排列得到最大/最小值” 类似题（如 LeetCode 1790 `Maximum Number of Groups` 中的数字排序）  
  2. “构造最小/最大整数” 题目（如 LeetCode 1493 `Largest Number`）  
  3. “无前导零的数字重排” 变体（如 “把数字重新排列成回文数”）  
- **一句话总结**：**正数取升序、把第一非零搬到最前；负数直接取降序**，即可得到最小合法数。

---

## 反思

- **第一反应**：看到“重新排列数字”，第一时间想到“全排列”。这在概念上最直观，却忽视了“只要最小/最大就不必遍历全部”的关键。
- **最容易踩的坑**  
  1. **前导零**：正数如果直接升序会得到形如 `013` 的非法答案，需要额外处理。  
  2. **负号的处理**：不能把负数当作正数排序后再加负号，否则会得到错误的“最大负数”。  
  3. **特殊输入**：`0`、全是 `0` 的负数（如 `-0` 实际上是 `0`）需要单独返回。  
- **下次思路**：看到“最小/最大”且“仅涉及排列”，立刻想到 **排序** 而不是 **全排列**，并检查是否有额外的约束（如前导零、符号）。这样可以在第一步就把时间复杂度从指数级降到对数级。