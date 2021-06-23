# #1374. 生成字符出现奇数次数的字符串 / Generate a String With Characters That Have Odd Counts

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/generate-a-string-with-characters-that-have-odd-counts/)

---

## 题目（英文原版）

**Description**

Given an integer n, return a string with n characters such that each character in such string occurs an odd number of times.
The returned string must contain only lowercase English letters. If there are multiples valid strings, return any of them.

**Examples**

**Example 1:**

```
Input: n = 4
Output: "pppz"
Explanation: "pppz" is a valid string since the character 'p' occurs three times and the character 'z' occurs once. Note that there are many other valid strings such as "ohhh" and "love".
```

**Example 2:**

```
Input: n = 2
Output: "xy"
Explanation: "xy" is a valid string since the characters 'x' and 'y' occur once. Note that there are many other valid strings such as "ag" and "ur".
```

**Example 3:**

```
Input: n = 7
Output: "holasss"
```

**Constraints**

- 1 <= n <= 500

---

## 题目（中文翻译）

**描述**  
给定一个整数 `n`，返回一个长度为 `n` 的字符串，使得该字符串中的每个字符出现的次数都是奇数。返回的字符串只能包含小写英文字母 (`a`-`z`)。如果存在多个满足条件的字符串，返回任意一个即可。

**示例 1**  
**输入**: `n = 4`  
**输出**: `"pppz"`  
**解释**: `"pppz"` 是合法的，因为字符 `'p'` 出现了三次，字符 `'z'` 出现了一次。还有许多其他合法的字符串，例如 `"ohhh"` 和 `"love"`。

**示例 2**  
**输入**: `n = 2`  
**输出**: `"xy"`  
**解释**: `"xy"` 是合法的，因为字符 `'x'` 和 `'y'` 各出现一次。还有许多其他合法的字符串，例如 `"ag"` 和 `"ur"`。

**示例 3**  
**输入**: `n = 7`  
**输出**: `"holasss"`  

**约束条件**  
- `1 <= n <= 500`   (n 的取值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有字符都随意写出来，只要每个字符出现的次数是奇数即可**。  
- **数据结构**：我们只需要一个普通的 Python 字符串（`str`），相当于一串贴在纸上的字母。  
- **生活化类比**：把字符想象成超市的商品，奇数次购买就像买了 1、3、5 件等不成双的数量。只要每种商品的购买数量都是奇数，就满足要求。  
- **为什么正确**：题目只要求**每个出现的字符出现奇数次**，并没有限制字符种类或出现顺序。只要我们构造的字符串满足“每个字母出现奇数次”，就是合法解。  

暴力实现可以直接遍历所有可能的字符组合，检验每个字符出现次数是否为奇数，找到第一个合法的就返回。虽然思路很笨，但能帮助我们确认“只要满足奇数次即可”这件事。

#### 代码（Python）

```python
import itertools
import string

def generate_string_brute(n: int) -> str:
    """
    暴力枚举所有由小写字母组成的长度为 n 的字符串，
    找到第一个每个字符出现次数为奇数的方案返回。
    """
    letters = string.ascii_lowercase          # 'abcdefghijklmnopqrstuvwxyz'
    # itertools.product 会生成所有可能的 n 位组合（非常多！仅用于演示）
    for combo in itertools.product(letters, repeat=n):
        s = ''.join(combo)
        # 统计每个字符出现次数
        ok = True
        for ch in set(s):
            if s.count(ch) % 2 == 0:          # 出现偶数次就不满足
                ok = False
                break
        if ok:
            return s
    return ""  # 理论上不会走到这里
```

> **注意**：上面的实现只用于说明“暴力思路”，在 n 较大时（比如 n=10）会产生 26ⁿ 种组合，根本不可运行。它用来帮助我们确认「只要奇数次就行」的条件。

#### 复杂度

- **时间复杂度**：\(O(26^n \cdot n)\)。  
  - `itertools.product` 产生 26ⁿ 种可能，每种可能我们要遍历一次字符串（长度 n）并统计字符出现次数。  
  - 用大白话说，就是“指数级增长”，几乎不可能在实际测试里跑通。

- **空间复杂度**：\(O(n)\)。  
  - 只需要存放当前枚举的字符串 `s`（长度 n）以及少量临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**我们根本不需要枚举所有组合**，只要直接构造一个满足条件的字符串即可。  
**慢在哪里**：暴力解的瓶颈是「枚举」——尝试所有可能的字符排列，这会导致指数级时间。  
**优化思路**：

1. **奇偶性决定**：  
   - 如果 `n` 本身是奇数，只要让 **一种字符出现 n 次**（例如 `'a'`），因为 n 为奇数，出现次数自然是奇数，满足要求。  
   - 如果 `n` 是偶数，单纯让一种字符出现 n 次会得到偶数次，不行。我们可以把 **一个字符出现 n‑1 次**（奇数），再 **加上另一个字符出现 1 次**（也是奇数），两者相加恰好等于 n。  

2. **选哪两个字符**并不重要，题目允许任意合法答案。常用的做法是选 `'a'` 和 `'b'`，因为它们是最前面的字母，代码更直观。  

3. **构造字符串**：  
   - 当 `n` 为奇数时：返回 `'a' * n`。  
   - 当 `n` 为偶数时：返回 `'a' * (n-1) + 'b'`。  

这样只用了常数次的字符拼接，时间几乎为 O(1)，空间也只用来存放结果字符串。

**关键概念——奇数/偶数**  
- 奇数：除以 2 余 1 的整数。比如 1、3、5。  
- 偶数：除以 2 余 0 的整数。比如 2、4、6。  

我们利用了“奇数 + 奇数 = 偶数”这条数学常识来构造答案。

#### 代码（Python）

```python
def generate_string_optimal(n: int) -> str:
    """
    根据 n 的奇偶性直接构造满足要求的字符串。
    - 奇数 n：全部使用 'a'（出现次数为奇数）。
    - 偶数 n：使用 n-1 个 'a'（奇数次）+ 1 个 'b'（奇数次）。
    """
    if n % 2 == 1:                # n 为奇数
        return 'a' * n            # 只用一种字符即可
    else:                         # n 为偶数
        return 'a' * (n - 1) + 'b'   # 两种字符，均出现奇数次
```

#### 复杂度

- **时间复杂度**：\(O(n)\)。  
  - 实际上只做了字符串的复制（`'a' * k`），这需要遍历 k 次字符，所以是线性时间。用大白话说，就是“和字符串长度成正比”，不会出现指数级增长。

- **空间复杂度**：\(O(n)\)。  
  - 需要额外的空间来存放返回的字符串，长度正好是 n。除去输出本身，额外的辅助空间是常数级的。

---

## 心得

- **核心技巧**：利用**奇数/偶数的数学性质**直接构造满足条件的字符串，而不是遍历搜索。  
- **适用的题型**  
  1. 需要让某些计数满足奇数或偶数约束的字符/数组构造题（如 “Construct a String With Substring Frequency”）。  
  2. 需要把总长度分解为若干满足特定奇偶性的块的题目（如 “Split a String Into the Max Number of Unique Substrings” 的奇偶版）。  
- **一句话总结**：**奇数 + 奇数 = 偶数**，把总长度拆成奇数块即可。

## 反思

- **第一反应**：看到“每个字符出现奇数次”，立刻想到「奇数」这个概念，检查 n 本身的奇偶性。  
- **最容易踩的坑**  
  - 忘记 **所有出现的字符** 都必须是奇数次，不能出现一次出现偶数次的情况。  
  - 边界条件：`n = 1`（最小值）时只能返回单个字符；`n = 2`（最小偶数）时需要两种字符各一次。  
- **下次类似题的第一步**：先**分析整体长度的奇偶性**，判断是否可以用单一字符或需要多种字符来满足奇数计数的要求。