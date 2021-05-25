# #1342. 将数字减至零的步数 / Number of Steps to Reduce a Number to Zero

> 难度：简单 · 标签：Math、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/)

---

## 题目（英文原版）

**Description**

Given an integer num, return the number of steps to reduce it to zero.
In one step, if the current number is even, you have to divide it by 2, otherwise, you have to subtract 1 from it.

**Examples**

**Example 1:**

```
Input: num = 14
Output: 6
Explanation: 
Step 1) 14 is even; divide by 2 and obtain 7. 
Step 2) 7 is odd; subtract 1 and obtain 6.
Step 3) 6 is even; divide by 2 and obtain 3. 
Step 4) 3 is odd; subtract 1 and obtain 2. 
Step 5) 2 is even; divide by 2 and obtain 1. 
Step 6) 1 is odd; subtract 1 and obtain 0.
```

**Example 2:**

```
Input: num = 8
Output: 4
Explanation: 
Step 1) 8 is even; divide by 2 and obtain 4. 
Step 2) 4 is even; divide by 2 and obtain 2. 
Step 3) 2 is even; divide by 2 and obtain 1. 
Step 4) 1 is odd; subtract 1 and obtain 0.
```

**Example 3:**

```
Input: num = 123
Output: 12
```

**Constraints**

- 0 <= num <= 106

---

## 题目（中文翻译）

给定一个整数 (integer) `num`，返回将其减至 0 所需的步数 (steps)。  
在每一步中：

- 如果当前数字是偶数 (even)，则将其除以 2 (divide by 2)；
- 否则，将其减去 1 (subtract 1)。

**示例 1**

```
Input: num = 14
Output: 6
Explanation:
Step 1) 14 为偶数；除以 2 得到 7。
Step 2) 7 为奇数；减去 1 得到 6。
Step 3) 6 为偶数；除以 2 得到 3。
Step 4) 3 为奇数；减去 1 得到 2。
Step 5) 2 为偶数；除以 2 得到 1。
Step 6) 1 为奇数；减去 1 得到 0。
```

**示例 2**

```
Input: num = 8
Output: 4
Explanation:
Step 1) 8 为偶数；除以 2 得到 4。
Step 2) 4 为偶数；除以 2 得到 2。
Step 3) 2 为偶数；除以 2 得到 1。
Step 4) 1 为奇数；减去 1 得到 0。
```

**示例 3**

```
Input: num = 123
Output: 12
```

**约束条件**

- `0 <= num <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把题目描述的过程 **一步步模拟**：  
1. 判断当前数字 `num` 是偶数还是奇数。  
2. 偶数 → 除以 2；奇数 → 减 1。  
3. 记录已经执行了多少步，直到 `num` 变成 0 为止。  

这里唯一需要的“数据结构”就是一个普通的整数变量 `num`，以及一个计数器 `steps`。可以把它想象成 **厨房里的一把勺子**：我们不停地往锅里舀（除以 2）或倒掉一点（减 1），每舀一次或倒一次就记一笔。

这种方法之所以一定能得到正确答案，是因为它严格遵循了题目给出的规则，没有任何猜测或近似。

**时间/空间复杂度**  
- 每一次循环都把 `num` 往小方向推进，最多需要 `log₂(num)` 次除以 2，加上一些减 1 的操作。最坏情况下（比如 `num = 2ⁿ‑1`），每一位都要先减 1 再除以 2，步数大约是 `2·log₂(num)`，所以时间复杂度是 **O(log num)**。  
- 只用了常数个变量 (`num`, `steps`)——相当于 **O(1)** 的空间。

> 大白话：如果 `num` 是 1 000 000（约 2²⁰），最多只需要跑 40 ~ 50 次循环，几乎可以忽略不计。

#### 代码（Python）

```python
def number_of_steps(num: int) -> int:
    """
    暴力模拟：一步步把 num 变成 0，统计需要的操作次数。
    """
    steps = 0                     # 记录已经执行了多少步
    while num > 0:                # 只要还有正数，就继续操作
        if num % 2 == 0:          # 偶数：可以整除 2
            num //= 2            # Python 的整数除法，等价于 num = num / 2
        else:                     # 奇数：只能减 1
            num -= 1
        steps += 1                # 完成一步，计数器加一
    return steps
```

#### 复杂度

- **时间复杂度**：`O(log num)` — 由于每次除以 2（或减 1 再除以 2）都能把二进制位数至少减少 1，循环次数与二进制位数成正比。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  
暴力解已经是 **O(log num)**，已经相当快了。但我们可以 **不动循环**，直接用二进制的特性一次性算出答案，这样代码更简洁、常数因子更小。

观察二进制：

| 操作 | 解释 |
|------|------|
| `num` 为偶数 | 二进制最低位是 `0`，直接右移一位（相当于除以 2） |
| `num` 为奇数 | 二进制最低位是 `1`，先减 1 使最低位变成 `0`，再右移 |

因此，**每出现一个 `0`（除了最高位的那位）只需要一次除以 2 的操作**；**每出现一个 `1`（除了最高位）需要一次减 1 再一次除以 2**。唯一的例外是最高位的 `1`，它只需要一次减 1（把数字变成 0），不需要再除以 2。

所以答案可以直接从二进制位数和 `1` 的个数推算出来：

```
steps = (二进制位数 - 1)          # 每个除以 2 的操作
        + (二进制中 1 的个数)    # 每个奇数需要额外的减 1
```

如果 `num` 为 0，二进制位数是 0，`1` 的个数也是 0，答案自然是 0。

**关键概念解释**  

- **二进制位数**：把整数写成二进制后，最左边的 `1` 到最右边的位数（包括左边的 `1`），相当于 `floor(log₂(num)) + 1`。可以用 `num.bit_length()` 在 Python 中直接得到。把它想象成 “这棵树有多高”。
- **`1` 的个数**：二进制中出现多少个 `1`，即 **汉明重量**。可以用 `bin(num).count('1')` 或者 `num.bit_count()`（Python 3.8+）得到。把它想象成 “树上有多少颗果子”，每颗果子都要先摘下来（减 1）再继续往下走。

#### 代码（Python）

```python
def number_of_steps(num: int) -> int:
    """
    利用二进制特性一次性算出答案。
    - bit_length() 返回二进制位数（最高位所在的位置 + 1）
    - bit_count() 返回二进制中 1 的个数（Python 3.8+）
    """
    if num == 0:                 # 特殊情况：本来就是 0，不需要任何操作
        return 0

    bits = num.bit_length()      # 二进制位数，例如 14 -> 1110 -> 4 位
    ones = num.bit_count()       # 1 的个数，例如 14 -> 3 个 1

    # 每一位（除最高位外）都要一次除以 2，故有 (bits - 1) 次除法
    # 每个 1（包括最高位）都要一次减 1，故有 ones 次减法
    steps = (bits - 1) + ones
    return steps
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只用了常数次的位运算或字符串计数，和 `num` 的大小无关。  
- **空间复杂度**：`O(1)` — 同样只用了几个整数变量。

> 与暴力解对比：虽然暴力解已经是 `O(log num)`，但最优解把循环“消失”了，直接用数学公式一次算完，运行更快，尤其在需要处理大量查询时优势更明显。

---

## 心得

- **核心技巧**：利用二进制的结构把“每一步的规则”转化为对位的计数（位数 + 1 的个数）。  
- **适用的题型**：  
  1. “把整数变成 0 的最少操作数”类（如 LeetCode 1404、1444）。  
  2. “统计二进制中 1 的个数或位数”相关的数学/位运算题。  
- **一句话总结**：**把每一次“除以 2”看作右移，每一次“减 1”看作把最低位的 1 变成 0，答案就是位数减一再加上 1 的个数。**

---

## 反思

- **第一反应**：直接写循环模拟，边走边数——最安全的办法。  
- **最容易踩的坑**：  
  - 忘记处理 `num = 0` 的特殊情况，会导致 `bit_length()` 返回 0，公式不成立。  
  - 对最高位的 `1` 多加了一次除以 2，导致答案比真实值大 1。  
- **下次遇到同类题**：第一步先思考“这一步的规则在二进制里对应什么操作”，看能否把循环转化为位计数。这样往往能直接得到 O(1) 的公式。