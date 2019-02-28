# #319. 灯泡开关 / Bulb Switcher

> 难度：中等 · 标签：Math、Brainteaser · [LeetCode 链接](https://leetcode.com/problems/bulb-switcher/)

---

## 题目（英文原版）

**Description**

There are n bulbs that are initially off. You first turn on all the bulbs, then you turn off every second bulb.
On the third round, you toggle every third bulb (turning on if it's off or turning off if it's on). For the ith round, you toggle every i bulb. For the nth round, you only toggle the last bulb.
Return the number of bulbs that are on after n rounds.

**Examples**

**Example 1:**

```
Input: n = 3
Output: 1
Explanation: At first, the three bulbs are [off, off, off].
After the first round, the three bulbs are [on, on, on].
After the second round, the three bulbs are [on, off, on].
After the third round, the three bulbs are [on, off, off]. 
So you should return 1 because there is only one bulb is on.
```

**Example 2:**

```
Input: n = 0
Output: 0
```

**Example 3:**

```
Input: n = 1
Output: 1
```

**Constraints**

- 0 <= n <= 109

---

## 题目（中文翻译）

**描述**  
有 `n` 盏最初处于关闭状态的灯泡（bulb）。  
第一轮，你把所有灯泡都打开；随后在第二轮，你关闭每隔一个灯泡（即每第 2 盏灯泡）。  
在第三轮，你切换（toggle）每第 3 盏灯泡的状态（如果是关闭的就打开，打开的就关闭）。  
第 `i` 轮时，你切换每第 `i` 盏灯泡的状态。  
第 `n` 轮时，只会切换最后一盏灯泡。  

返回进行完 `n` 轮操作后，仍保持打开状态的灯泡数量。

**示例**

示例 1  
```
Input: n = 3
Output: 1
Explanation: 最初，三盏灯泡的状态为 [off, off, off]。  
第一轮后，状态变为 [on, on, on]。  
第二轮后，状态变为 [on, off, on]。  
第三轮后，状态变为 [on, off, off]。  
因此返回 1，因为只有一盏灯泡保持打开状态。
```

示例 2  
```
Input: n = 0
Output: 0
```

示例 3  
```
Input: n = 1
Output: 1
```

**约束条件**  
- `0 <= n <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是 **模拟** 题目描述的每一轮开关操作：

1. 先把 1~n 盏灯全部打开（全部设为 `True`）。
2. 第 2 轮：把所有编号能被 2 整除的灯切换一次（`True` → `False`，`False` → `True`）。
3. 第 3 轮：把所有编号能被 3 整除的灯切换一次。
4. ……第 i 轮：把所有编号能被 i 整除的灯切换一次，直到第 n 轮。

> **类比**：把灯的状态想成一本字典里的词条，`True/False` 就是词条的定义。每一轮我们把“能被 i 整除的词条”全部翻页（打开 → 关闭，关闭 → 打开），相当于在字典里查所有符合条件的词并把它们的解释取反。

只要把每一盏灯的状态记录下来，最后统计 `True` 的个数即可。

> **为什么正确**  
> 对第 `i` 盏灯来说，它会在每一个能整除 `i` 的轮次被切换一次。于是它被切换的次数等于 `i` 的约数个数。约数个数为奇数的灯最终会保持打开（因为 `关 → 开 → 关 …`，奇数次恰好是 `开`），约数个数为偶数的灯最终是关闭。暴力模拟把所有切换过程完整执行，自然得到相同的结果。

#### 代码（Python）

```python
def bulbSwitch_bruteforce(n: int) -> int:
    # 用列表保存每盏灯的状态，False 表示关，True 表示开
    lights = [False] * (n + 1)          # 0 号灯我们不使用，方便下标对应灯的编号

    # 第 1 轮把所有灯打开
    for i in range(1, n + 1):
        lights[i] = True

    # 从第 2 轮到第 n 轮，依次切换能被 i 整除的灯
    for i in range(2, n + 1):
        # 步长为 i，直接跳到所有 i 的倍数
        for j in range(i, n + 1, i):
            lights[j] = not lights[j]   # 取反：开→关，关→开

    # 统计最终为 True（打开）的灯的数量
    return sum(lights)                  # True 在 Python 中等价于 1，直接求和即可
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 第 1 轮是 `O(n)`。  
  - 第 2~n 轮的总循环次数近似 `n/2 + n/3 + … + n/n ≈ n·(1/2 + 1/3 + … + 1/n) = O(n log n)`（调和级数）。  
  - 用大白话说，就是随着灯的数量增大，程序的运行时间大约是 `n` 乘以一个慢慢增长的对数因子（比如 n=10⁶ 时约为 10⁶·14）。

- **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n+1` 的数组保存每盏灯的状态，随灯的数量线性增长。

---

### 2. 最优解

#### 思路  
从暴力解可以看出，每盏灯最终状态只和 **它的约数个数的奇偶性** 有关：

- 被切换奇数次 → 最终是 **开**。  
- 被切换偶数次 → 最终是 **关**。

**约数个数为奇数** 的数有什么特殊性质？  
只有**完全平方数**（如 1、4、9、16 …）的约数出现配对时会多出一个“自配对”的约数（√k 本身只配对一次），因此约数个数为奇数。  

> **类比**：把约数配对想成一对手套，左手套和右手套成对出现。只有正方形的手套（比如 9 的约数 1&9、3&3），中间的那只手套只能和自己配对一次，导致总数为奇数。

所以，**最终打开的灯的编号** 正好是 **1 到 n 之间的完全平方数**，数量就是 `⌊√n⌋`（不超过 n 的最大整数平方根）。

> **关键点**  
> 1. 认识到每盏灯的状态只取决于约数个数的奇偶性。  
> 2. 证明约数个数为奇数 ↔ 完全平方数。  
> 3. 直接用数学公式求根号，无需模拟。

#### 代码（Python）

```python
import math

def bulbSwitch(n: int) -> int:
    """
    返回经过 n 轮切换后仍然是打开的灯的数量。
    结论：打开的灯的编号恰好是完全平方数，数量等于 sqrt(n) 向下取整。
    """
    # math.isqrt 在 Python 3.8+ 提供整数平方根，等价于 int(math.sqrt(n))
    return math.isqrt(n)          # 直接返回不超过 n 的最大整数 sqrt
```

> **代码解释**  
> - `math.isqrt(n)` 用整数算法计算 `⌊√n⌋`，不涉及浮点数，安全且高效。  
> - 整个函数只做了一次 O(1) 的计算，时间几乎为常数。

#### 复杂度  

- **时间复杂度**：`O(1)`  
  - 只进行一次整数平方根运算，和 `n` 的大小无关。  
  - 与暴力解相比，时间从 `O(n log n)` 降到常数级，几乎瞬间完成。

- **空间复杂度**：`O(1)`  
  - 不需要额外的数组或列表，只用几个整数变量。

---

## 心得

- **核心技巧**：把“操作次数奇偶性”转化为“约数个数奇偶性”，再用数论性质（完全平方数）直接求解。  
- **适用的题型**：  
  1. “灯泡开关”“门的切换”等需要多轮切换的题目。  
  2. “找出满足某种奇偶性条件的编号”类题目（如找出约数个数为奇数的数）。  
  3. “从 n 中统计满足某种数学特性的数”——常见的有完全平方数、完全立方数等。  
- **一句话总结**：**“约数配对 → 奇数约数 ⇔ 完全平方数 → 用 sqrt 直接计数”。**

---

## 反思

- **第一反应**：直接去模拟每一轮的切换，因为描述的过程很直观。  
- **最容易踩的坑**：  
  - 忘记第 0 轮（题目从第 1 轮开始），导致数组下标错误。  
  - 对 `n = 0`、`n = 1` 等极小值没有单独考虑，可能出现数组越界。  
  - 在最优解中使用浮点数 `math.sqrt` 再取 `int`，可能因为精度问题导致 `sqrt(9)` 得到 `2.999999…`，进而错误。使用 `math.isqrt` 可以避免。  
- **下次遇到同类题**：第一步先思考 **“每个元素被操作多少次”**，找出次数的数学规律（如约数、因子、倍数），再看是否有已知的数论结论可以直接求解。这样往往能把暴力的 `O(n·log n)` 或 `O(n²)` 降到 `O(1)`。