# #906. 超级回文数 / Super Palindromes

> 难度：困难 · 标签：Math、String、Enumeration · [LeetCode 链接](https://leetcode.com/problems/super-palindromes/)

---

## 题目（英文原版）

**Description**

Let's say a positive integer is a super-palindrome if it is a palindrome, and it is also the square of a palindrome.
Given two positive integers left and right represented as strings, return the number of super-palindromes integers in the inclusive range [left, right].

**Examples**

**Example 1:**

```
Input: left = "4", right = "1000"
Output: 4
Explanation: 4, 9, 121, and 484 are superpalindromes.
Note that 676 is not a superpalindrome: 26 * 26 = 676, but 26 is not a palindrome.
```

**Example 2:**

```
Input: left = "1", right = "2"
Output: 1
```

**Constraints**

- 1 <= left.length, right.length <= 18
- left and right consist of only digits.
- left and right cannot have leading zeros.
- left and right represent integers in the range [1, 1018 - 1].
- left is less than or equal to right.

---

## 题目（中文翻译）

如果一个正整数是回文（palindrome），并且它还是一个回文的平方（square），则称其为超级回文数（super‑palindrome）。给定两个正整数 `left` 和 `right`（以字符串形式表示），返回闭区间 `[left, right]` 中超级回文数的个数。

**示例 1：**  
输入: `left = "4", right = "1000"`  
输出: `4`  
说明: `4, 9, 121, 484` 均是超级回文数。需要注意 `676` 不是超级回文数，因为 `26 * 26 = 676`，但 `26` 不是回文。

**示例 2：**  
输入: `left = "1", right = "2"`  
输出: `1`

**约束条件：**
- `1 <= left.length, right.length <= 18`
- `left` 和 `right` 只包含数字。
- `left` 和 `right` 不能有前导零。
- `left` 和 `right` 表示的整数在区间 `[1, 10^18 - 1]` 内。
- `left` ≤ `right`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把区间 `[left, right]` 里所有整数都枚举出来，逐个判断：

1. **是不是回文数**  
   把整数转成字符串，正着读和倒着读一样就是回文。  
   （可以把它想象成在字典里查单词：把单词正写和倒写对比，完全相同才算“同义”。）

2. **它的平方根是不是回文数**  
   对当前数 `x`，先算 `sqrt = int(math.isqrt(x))`（整数平方根），如果 `sqrt * sqrt == x` 说明 `x` 正好是一个整数的平方。再把 `sqrt` 按上面的方法检查是否回文。

只要两个条件都满足，就把它计数。  

**为什么正确**  
- 回文的定义本身就是“正读和反读相同”，我们逐个检查，必然不会漏掉。
- 超级回文的定义是“本身是回文且是某个回文的平方”。只要我们遍历了所有可能的 `x`，并且对每个 `x` 检查它的平方根是否回文，就一定能找出所有符合要求的数。

**时间/空间复杂度**  
- 时间复杂度：`O(N * log10 N)`（`N = right - left + 1`）  
  - 对每个数我们要做两次回文检查，回文检查的时间是把整数转成字符串再翻转，长度大约是 `log10 N`（数字位数）。  
  - 如果 `right` 接近 `10^18`，`N` 可能是 `10^18`，显然跑不完。  
- 空间复杂度：`O(1)`（只用常数级的变量）

> **大白话**：`O(N)` 就像说“随区间大小线性增长”。如果区间有一万亿个数，程序就得跑一万亿次，根本不可能在几秒内完成。

#### 代码（Python）

```python
import math

def is_palindrome(num: int) -> bool:
    """判断一个整数是否是回文数，思路：把它写成字符串，正读和反读一样即为回文。"""
    s = str(num)
    return s == s[::-1]          # 逆序切片相当于倒着读

def superpalindromes_brute(left: str, right: str) -> int:
    L, R = int(left), int(right)
    cnt = 0
    for x in range(L, R + 1):
        # 1. x 本身是回文
        if not is_palindrome(x):
            continue
        # 2. x 必须是某个整数的平方
        root = math.isqrt(x)      # 整数平方根
        if root * root != x:
            continue
        # 3. 平方根也是回文
        if is_palindrome(root):
            cnt += 1
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(N * log10 N)`  
  - `N` 是区间长度。`log10 N` 是每次回文检查要看的字符数（比如 `10^12` 只有 13 位），所以整体随 `N` 线性增长。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数和字符串临时变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有区间数字**，当 `right` 接近 `10^18` 时，区间可能有上百亿甚至更多的数，根本不可能逐个检查。  
观察题目可以发现：

- 超级回文 `x` 必须是 **回文数的平方**。  
- 那么如果我们先把 **所有可能的回文根**（即 `sqrt(x)`）枚举出来，再把它们平方，检查结果是否仍是回文，就能直接得到答案。  
- 关键是：`sqrt(x)` 的最大可能值是 `sqrt(right)`。因为 `right ≤ 10^18`，所以 `sqrt(right) ≤ 10^9`（十亿），远远小于 `right` 本身。  
- 甚至更好：我们只需要枚举 **回文根**，而不是所有 `1 … 10^9` 的整数。回文根的数量远远小于十亿。

**如何高效生成回文根**  

回文数可以通过“左半部 + 中间（可选） + 左半部的逆序”来构造。  
举个例子：

| 左半部（正向） | 中间位 | 完整回文 |
|---------------|--------|----------|
| `12`          | （无） | `1221`   |
| `12`          | `3`    | `12321`  |

只要遍历左半部的所有可能（从 `1` 开始递增），再把它拼接成奇数长度或偶数长度的回文，就能得到 **所有** 长度不超过 9 位（因为根的上限是 `10^9`）的回文根。

**步骤概览**

1. 计算 `R = int(right)`，`L = int(left)`，以及 `max_root = int(math.isqrt(R))`（根的最大可能值）。  
2. 生成所有 **奇数长度** 回文根：  
   - 对每个 `i`（从 `1` 开始），把 `i` 转成字符串 `s`。  
   - 取 `s` 的逆序（不包括最后一位）拼接在 `s` 后面得到回文字符串 `pal = s + s[-2::-1]`。  
   - 把 `pal` 转成整数 `p`，如果 `p > max_root` 则停止循环。  
3. 同理生成 **偶数长度** 回文根：`pal = s + s[::-1]`。  
4. 对每个得到的根 `p`：  
   - 计算 `sq = p * p`。  
   - 若 `sq` 超出 `[L, R]`，直接跳过（或在根遍历时提前结束）。  
   - 检查 `sq` 是否是回文（同前面的 `is_palindrome`），如果是则计数。  

这样我们只遍历了大约 `2 * 10^5` 个根（因为左半部最多 5 位），每个根只做一次平方和一次回文检查，时间非常快。

#### 代码（Python）

```python
import math

def is_palindrome(num: int) -> bool:
    """判断整数是否是回文（把数字写成字符串后正读倒读相同）"""
    s = str(num)
    return s == s[::-1]

def superpalindromes_optimal(left: str, right: str) -> int:
    L, R = int(left), int(right)
    max_root = int(math.isqrt(R))      # 根的上界
    ans = 0

    # -------- 生成奇数长度的回文根 --------
    i = 1
    while True:
        s = str(i)
        # 例如 i=123 -> "12321"
        pal_str = s + s[-2::-1]        # 去掉最后一个字符再反转
        p = int(pal_str)
        if p > max_root:
            break
        sq = p * p
        if sq >= L and sq <= R and is_palindrome(sq):
            ans += 1
        i += 1

    # -------- 生成偶数长度的回文根 --------
    i = 1
    while True:
        s = str(i)
        # 例如 i=123 -> "123321"
        pal_str = s + s[::-1]
        p = int(pal_str)
        if p > max_root:
            break
        sq = p * p
        if sq >= L and sq <= R and is_palindrome(sq):
            ans += 1
        i += 1

    return ans
```

> **代码细节说明**  
> - `s[-2::-1]`：先把 `s` 从倒数第二个字符开始往前取（即去掉最右边的那位），再逆序，得到奇数长度回文的右半部。  
> - 两个 `while` 循环分别处理奇数和偶数长度的根，**都在根超过 `max_root` 时提前结束**，避免不必要的遍历。  
> - `sq >= L and sq <= R` 用来筛掉不在查询区间的平方。

#### 复杂度

- **时间复杂度**：`O(√R) ≈ O(10^5)`（实际更小）  
  - 我们只遍历左半部的所有可能，左半部最多 5 位（因为根 ≤ `10^9`），所以大约有 `10^5` 次循环。每次循环做常数次操作（平方、回文检查），整体时间几乎是常数级别的。相比暴力的 `O(N)`（可能是 `10^18`），快了天壤之别。  
- **空间复杂度**：`O(1)`  
  - 只使用了若干整数和字符串临时变量，和输入规模无关。

---

## 心得

- **核心技巧**：**只枚举回文根**，而不是枚举区间内的所有数。利用“回文数可以由左半部拼接得到”来高效生成候选根。  
- **适用的题型**  
  1. “**回文数的平方**” 类似的题目，如 *Super Palindromes*。  
  2. “**回文数的乘积/和**” 等，需要先生成回文再做运算的题目。  
  3. “**回文数的计数**” 题，例如在给定范围内统计回文数。  
- **一句话总结解题钥匙**：  
  > “把问题从‘检查每个数’翻转为‘生成所有可能的回文根’，利用结构化的构造方式把搜索空间压到几万级。”

---

## 反思

- **第一反应**：直接遍历区间、逐个检查，想法最直接但忽视了输入规模。  
- **最容易踩的坑**  
  - **上界判断**：根的上界是 `sqrt(right)`，如果忘记这一步会继续生成过大的根，导致平方溢出或不必要的计算。  
  - **奇偶长度的回文生成**：拼接时容易写错索引，导致生成的不是回文或漏掉某些长度。  
  - **边界条件**：`left`、`right` 可能非常大，使用 `int` 直接转化是安全的（Python 整数不溢出），但在其他语言需要注意 64 位整数范围。  
- **下次遇到同类题**，第一步应该思考：  
  > “有没有可以先**生成**满足某些特征的候选对象，而不是在完整空间里**遍历**？”  
  对于涉及“回文”“平方”“乘积”等限制的题目，往往可以从 **结构化生成** 入手，大幅削减搜索空间。