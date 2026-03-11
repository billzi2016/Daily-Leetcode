# #3556. 最大质数子串之和 / Sum of Largest Prime Substrings

> 难度：中等 · 标签：Hash Table、Math、String、Sorting、Number Theory · [LeetCode 链接](https://leetcode.com/problems/sum-of-largest-prime-substrings/)

---

## 题目（英文原版）

**Description**

Given a string s, find the sum of the 3 largest unique prime numbers that can be formed using any of its substrings.
Return the sum of the three largest unique prime numbers that can be formed. If fewer than three exist, return the sum of all available primes. If no prime numbers can be formed, return 0.
Note: Each prime number should be counted only once, even if it appears in multiple substrings. Additionally, when converting a substring to an integer, any leading zeros are ignored.

**Examples**

**Example 1:**

```
Input: s = "12234"
Output: 1469
Explanation:
```

**Example 2:**

```
Input: s = "111"
Output: 11
Explanation:
```

**Constraints**

- 1 <= s.length <= 10
- s consists of only digits.

---

## 题目（中文翻译）

给定一个字符串 `s`，找出可以由其任意子串（substring）组成的 **3 个最大且唯一的质数（prime number）** 的和并返回。  
- 若可组成的质数少于三个，则返回所有可得质数的和。  
- 若不存在任何质数，则返回 `0`。  

**注意事项**  
- 每个质数只计一次，即使它出现在多个子串中。  
- 将子串转换为整数时，前导零会被忽略。

## 示例

### 示例 1
**输入**  
```
s = "12234"
```
**输出**  
```
1469
```
**解释**  
（此处填写对示例的具体解释）

### 示例 2
**输入**  
```
s = "111"
```
**输出**  
```
11
```
**解释**  
（此处填写对示例的具体解释）

## 约束条件
- `1 <= s.length <= 10`
- `s` 仅由数字字符组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把字符串的所有**子串**都列出来，把每个子串当作十进制整数（前导零会自动被 `int()` 忽略），检查它是不是质数，若是就放进集合去重，最后把集合里最大的三个数相加。

- **子串**：把原始字符串看成一根珠子串，任选左边的起点 `i`，再任选右边的终点 `j`（`i ≤ j`），`s[i:j+1]` 就是一个子串。  
- **哈希表（集合）**：这里的集合像是一本“已出现数字的字典”，把已经找到的质数记下来，防止同一个质数因为出现在不同子串里而被重复计数。  
- **质数判定**：最常见的做法是试除法：对一个数 `n`，只要在 `2 … sqrt(n)` 之间找不到能整除它的整数，它就是质数。

因为字符串长度最多只有 `10`，子串的数量最多是 `n·(n+1)/2 = 55`，完全可以用暴力把它们全部枚举并逐个判定。

**为什么正确**  
- 我们遍历了 **所有** 可能的子串，所以不可能遗漏任何能够形成的整数。  
- 对每个整数都做了 **完整的质数判定**，只要它是质数就一定会被加入集合。  
- 最后从集合中取最大的三个（或所有）质数求和，正是题目要求的返回值。

#### 代码（Python）

```python
def is_prime(n: int) -> bool:
    """试除法判断 n 是否为质数。"""
    if n < 2:                     # 0、1 不是质数
        return False
    if n == 2:                    # 2 是唯一的偶数质数
        return True
    if n % 2 == 0:                # 其余偶数直接否定
        return False
    # 只需要检查到 sqrt(n)，且只检查奇数
    i = 3
    while i * i <= n:
        if n % i == 0:            # 找到因子，说明不是质数
            return False
        i += 2
    return True                   # 没有因子，是真质数

def sum_largest_three_primes(s: str) -> int:
    n = len(s)
    primes = set()                # 用集合去重
    # 枚举所有子串
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j+1]        # 取子串
            num = int(sub)        # 自动忽略前导零
            if is_prime(num):
                primes.add(num)   # 加入集合
    # 按从大到小排序
    sorted_primes = sorted(primes, reverse=True)
    # 取前 3（若不足 3 个则全部取）求和
    return sum(sorted_primes[:3])
```

#### 复杂度  

- **时间复杂度**：`O(n² * √M)`  
  - `n²` 来自子串的枚举（`n ≤ 10`，最多 55 次）。  
  - `√M` 是每个数的试除法成本，`M` 为子串对应的整数大小（最多 10 位数，约 `10⁵` 的平方根约 `10³`）。  
  - 综上，最坏情况大约是 `55 * 1000 ≈ 5.5×10⁴` 次基本运算，完全可以接受。  
- **空间复杂度**：`O(K)`  
  - `K` 为不同质数的个数，最多不超过子串总数（55），所以只用几十个整数的额外空间。

---

### 2. 最优解

#### 思路  

虽然暴力已经够快，但我们仍可以把「判定质数」这一步进一步提速，使整体思路在更大输入（如果约束放宽）时仍然可行。优化的关键在于：

1. **避免重复判定**  
   同一个整数可能出现在多个子串里（例如 `"1010"` 中的子串 `"10"` 出现两次），如果我们每次都重新做试除法，会浪费时间。我们可以在遍历子串时把已经检查过的整数记在一个哈希表里，下次再遇到相同的整数直接复用结果。

2. **更快的质数检测**  
   对 10 位以内的整数（最大约 `10⁹`）使用 **确定性 Miller‑Rabin** 素性测试要比试除法快得多。Miller‑Rabin 是一种基于随机性的概率算法，但在 **固定的基数集合** 下（例如 `[2, 3, 5, 7, 11]`）对 32 位整数是 **确定性的**，即若测试通过就一定是质数。其时间复杂度约为 `O(log³ n)`，对我们的规模几乎可以忽略不计。

3. **直接取前三大**  
   在收集质数的同时维护一个长度为 3 的“小顶堆”（最小堆），这样无需把所有质数全部排好序，只需要在堆满时比较并保留最大的三个。Python 的 `heapq` 已经实现了最小堆，只要堆的大小超过 3，就弹出最小的那个即可。

综上，最优解的整体流程：

- 枚举所有子串（仍是 `O(n²)`，因为 `n ≤ 10`，这一步不可再快）。  
- 把子串转成整数 `num`。  
- 若 `num` 已经在 `checked`（哈希表）中，直接拿到它的质数与否结果；否则用 Miller‑Rabin 检测并把结果写入 `checked`。  
- 若是质数且不在 `unique_primes`（集合）里，加入集合并把它推入长度不超过 3 的最小堆 `top3`。  
- 最后把堆里剩下的元素求和返回。

> **核心数据结构解释**  
> - **哈希表（字典/集合）**：像是一本“数字-是否为质数”的查字典，查找/写入都是 `O(1)`。  
> - **最小堆**：把最大的三个数保存在一个小箱子里，箱子里最小的数随时在最上面，超过三个时弹掉它，保证箱子里永远是当前最大的三个。

#### 代码（Python）

```python
import heapq

def miller_rabin(n: int) -> bool:
    """确定性 Miller‑Rabin 素性测试（适用于 n < 2^32）。"""
    if n < 2:
        return False
    # 小于等于 3 的质数直接返回
    small_primes = [2, 3, 5, 7, 11]
    for p in small_primes:
        if n % p == 0:
            return n == p

    # 将 n-1 写成 d * 2^s (d 为奇数)
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # 对每个基数 a 进行测试
    for a in small_primes:
        x = pow(a, d, n)          # x = a^d mod n
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:                     # 循环正常结束，说明 a 是“见证”
            return False
    return True                 # 所有基数都通过，必为质数

def sum_largest_three_primes_opt(s: str) -> int:
    n = len(s)
    checked = {}                 # num -> 是否为质数，避免重复检测
    unique_primes = set()        # 用于去重
    top3 = []                    # 最小堆，保存当前最大的 3 个质数

    for i in range(n):
        for j in range(i, n):
            num = int(s[i:j+1])  # 自动去掉前导零

            # 先看是否已经检查过
            if num in checked:
                is_p = checked[num]
            else:
                is_p = miller_rabin(num)
                checked[num] = is_p

            if is_p and num not in unique_primes:
                unique_primes.add(num)
                # 维护大小为 3 的最小堆
                heapq.heappush(top3, num)
                if len(top3) > 3:
                    heapq.heappop(top3)   # 弹出最小的，保持堆里是最大的 3 个

    return sum(top3)   # 堆中最多 3 个数，直接相加即可
```

#### 复杂度  

- **时间复杂度**：`O(n² + U·log³M)`  
  - `n²` 仍是子串枚举的成本（最多 55 次）。  
  - `U` 为不同整数的数量（≤ 55），每个整数只会被 Miller‑Rabin 检测一次，复杂度约为 `log³M`（`M` 为整数大小，最多 10 位），在实际运行中几乎可以视作常数。  
  - 综上，总体时间比暴力的 `O(n²·√M)` 快了一个数量级，尤其当 `M` 很大时优势更明显。

- **空间复杂度**：`O(U)`  
  - `checked`、`unique_primes`、`top3` 最多存放 `U`（≤55）个整数，空间需求极小。

---

## 心得

- **核心技巧**：**哈希表去重 + 更快的素性测试（Miller‑Rabin） + 小顶堆维护前 k 大**。  
- **适用题型**  
  1. “从所有子串/子数组中挑出满足某种数值性质的前 k 大”——如 “最大 k 个不同回文数”。  
  2. “大量候选数需要快速判素且去重”——如 “给定数字序列，找出所有互质的前 k 大”。  
  3. “需要在遍历过程中实时维护 Top‑k”——如 “滑动窗口中最大 k 个不同元素”。  
- **一句话总结**：**先把所有候选值去重，再用最快的质数判定并用最小堆实时保留最大的三个**。

---

## 反思

- **第一反应**：直接把所有子串枚举出来，用最朴素的试除法检查质数，然后排序取前三。  
- **最容易踩的坑**  
  - **前导零**：`int("0013")` 会自动变成 `13`，不需要手动去除，但要记得题目允许忽略前导零。  
  - **重复计数**：同一个质数可能出现在不同子串里，必须用集合去重，否则会把同一个数算多次。  
  - **没有质数的情况**：返回 `0` 而不是空列表或错误。  
- **下次类似题**：**先思考“去重”和“如何高效判断”**，尤其是当候选数的规模可能很大时，提前准备快速的判定算法（如 Miller‑Rabin）和 Top‑k 维护技巧，会让解法既简洁又高效。