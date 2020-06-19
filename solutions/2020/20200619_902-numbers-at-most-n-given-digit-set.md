# #902. 给定数字集合下不超过 N 的数字 / Numbers At Most N Given Digit Set

> 难度：困难 · 标签：Array、Math、String、Binary Search、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/)

---

## 题目（英文原版）

**Description**

Given an array of digits which is sorted in non-decreasing order. You can write numbers using each digits[i] as many times as we want. For example, if digits = ['1','3','5'], we may write numbers such as '13', '551', and '1351315'.
Return the number of positive integers that can be generated that are less than or equal to a given integer n.

**Examples**

**Example 1:**

```
Input: digits = ["1","3","5","7"], n = 100
Output: 20
Explanation: 
The 20 numbers that can be written are:
1, 3, 5, 7, 11, 13, 15, 17, 31, 33, 35, 37, 51, 53, 55, 57, 71, 73, 75, 77.
```

**Example 2:**

```
Input: digits = ["1","4","9"], n = 1000000000
Output: 29523
Explanation: 
We can write 3 one digit numbers, 9 two digit numbers, 27 three digit numbers,
81 four digit numbers, 243 five digit numbers, 729 six digit numbers,
2187 seven digit numbers, 6561 eight digit numbers, and 19683 nine digit numbers.
In total, this is 29523 integers that can be written using the digits array.
```

**Example 3:**

```
Input: digits = ["7"], n = 8
Output: 1
```

**Constraints**

- 1 <= digits.length <= 9
- digits[i].length == 1
- digits[i] is a digit from '1' to '9'.
- All the values in digits are unique.
- digits is sorted in non-decreasing order.
- 1 <= n <= 109

---

## 题目（中文翻译）

给定一个按 **非递减顺序 (non-decreasing order)** 排序的 **数组 (array)** `digits`。你可以任意次数使用每个 `digits[i]` 来构造数字。例如，若 `digits = ['1','3','5']`，我们可以写出 `'13'`、`'551'`、`'1351315'` 等数字。返回可以生成且 **不大于 (≤)** 给定整数 `n` 的 **正整数 (positive integers)** 的个数。

### 示例

#### 示例 1
**输入**: `digits = ["1","3","5","7"]`, `n = 100`  
**输出**: `20`  
**解释**:  
可以写出的 20 个数字为：  
1, 3, 5, 7, 11, 13, 15, 17, 31, 33, 35, 37, 51, 53, 55, 57, 71, 73, 75, 77.

#### 示例 2
**输入**: `digits = ["1","4","9"]`, `n = 1000000000`  
**输出**: `29523`  
**解释**:  
我们可以写出  
- 3 个 1 位数，  
- 9 个 2 位数，  
- 27 个 3 位数，  
- 81 个 4 位数，  
- 243 个 5 位数，  
- 729 个 6 位数，  
- 2187 个 7 位数，  
- 6561 个 8 位数，  
- 19683 个 9 位数。  

总计 `29523` 个整数可以由 `digits` 数组写成。

#### 示例 3
**输入**: `digits = ["7"]`, `n = 8`  
**输出**: `1`

### 约束条件
- `1 <= digits.length <= 9`
- `digits[i].length == 1`
- `digits[i]` 是字符 `'1'` 到 `'9'` 之间的数字
- `digits` 中的所有值均唯一
- `digits` 已按 **非递减顺序 (non-decreasing order)** 排列
- `1 <= n <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 **digits** 当成「可使用的字母表」，把每一个正整数看成「由这些字符组成的单词」。  
我们可以从长度为 1 的数字开始递归地往后拼，每拼一次就得到一个新的整数；只要这个整数 **≤ n**，计数 +1；如果已经大于 n，直接剪枝（不必继续往下拼更长的数字，因为更长的数字一定更大）。  

**用到的数据结构**  

- **列表 `digits`**：就像一本字典，里面只有 1~9 的“词”，我们可以随意取出并重复使用。  
- **递归/栈**：相当于在做「深度优先搜索」——一次次把「字符」放到「单词」的后面。  

**为什么正确**  

- 递归遍历了 **所有** 可能的组合（长度从 1 到 `len(str(n))`），没有遗漏。  
- 每产生一个合法整数就计数，恰好对应题目要求的「能写出的正整数」集合。  

**复杂度分析（大白话）**  

- 假设 `k = len(digits)`，`L = len(str(n))`（即 n 的位数）。  
- 对每一位我们都有 `k` 种选择，最坏情况下会遍历 `k^1 + k^2 + … + k^L` 种组合。  
- 当 `k = 9`、`L = 9`（因为 n ≤ 10⁹）时，上限是 `9⁹ ≈ 3.8×10⁸`，远远超出 1 秒的计算上限。  
- 因此暴力解在最坏情况下 **时间会爆炸**（指数级），空间只需要递归栈深度 `L`，即 `O(L)`。

#### 代码（Python）

```python
from typing import List

def atMostNGivenDigitSet_bruteforce(digits: List[str], n: int) -> int:
    """暴力 DFS，遍历所有可能的数字并计数"""
    limit = str(n)               # 把 n 转成字符串，方便逐位比较
    L = len(limit)               # n 的位数
    cnt = 0                      # 计数器

    def dfs(cur: str) -> None:
        """在当前已经构造好的字符串 cur 基础上继续添加数字"""
        nonlocal cnt
        if cur:                  # 只要不是空串，就已经形成了一个正整数
            # 把字符串转成整数比较大小
            if int(cur) <= n:
                cnt += 1
            else:
                # 已经超过 n，后面的更长数字一定更大，直接剪枝
                return

        # 如果已经拼到了 n 的位数，继续往下只会产生更长的数字，必定 > n
        if len(cur) == L:
            return

        # 尝试把每一个可用的数字放到当前数字的后面
        for d in digits:
            dfs(cur + d)

    dfs("")                      # 从空串开始搜索
    return cnt
```

#### 复杂度  

- **时间复杂度**：`O(k^1 + k^2 + … + k^L)`（指数级），  
  这里的 `k = len(digits)`，`L = len(str(n))`。  
  用大白话说，就是「每增加一位，就会把可能性翻 k 倍」。
- **空间复杂度**：`O(L)`，只需要保存递归调用的深度（最多 `L` 层），相当于一条「搜索路径」的长度。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于 **“枚举所有组合”**，而我们其实不需要真的把每个数写出来，只要 **计数** 即可。  
计数可以分两部分：

1. **长度小于 n 的位数** 的所有合法数字。  
   - 若 `digits` 中有 `k` 个可选数字，长度为 `len` 的数有 `k^len` 种写法（每位都可以随意选）。  
   - 只要 `len < L`（`L = len(str(n))`），这些数一定 **小于** `n`，直接累加即可。

2. **长度等于 n 的位数** 的数字，需要逐位比较。  
   - 把 `n` 写成字符串 `s = str(n)`，从最高位往低位遍历。  
   - 对于第 `i` 位（0‑based），我们统计 **“可选数字中比 s[i] 小的数字有多少个”**，记作 `cnt_smaller`。  
   - 那么在保持前 `i` 位与 `n` 完全相同的前提下，第 `i` 位可以任选这些更小的数字，后面的 `L-i-1` 位可以随意填 `k` 种数字。于是这部分贡献 `cnt_smaller * k^(L-i-1)`。  
   - 如果 `s[i]` 本身不在 `digits` 中，说明再往下再也找不到与 `n` 前缀相同的合法数，直接结束循环。  
   - 若遍历完所有位且每一位都在 `digits` 中，则 `n` 本身也是合法数，需要再加 `1`。

整个过程只遍历 `L` 位，时间 **线性** 于 `L`，空间只需要几个整数。

> **核心技巧**：**按位计数 + 幂次**  
> - 类比：在排队买票时，先数出比自己排号早的有多少人（`cnt_smaller`），再乘以后面每个人的选择方式（`k^(remaining)`），得到自己前面有多少人。

#### 代码（Python）

```python
from typing import List

def atMostNGivenDigitSet(digits: List[str], n: int) -> int:
    """最优计数解法，时间 O(L)，空间 O(1)"""
    k = len(digits)                # 可选数字的个数
    s = str(n)                     # n 的字符串形式，方便逐位比较
    L = len(s)                     # n 的位数

    # 1. 统计所有长度 < L 的合法数字
    total = 0
    power = 1                      # k^0 = 1
    for length in range(1, L):     # length 从 1 到 L-1
        power *= k                 # k^length
        total += power             # 加上该长度的所有组合数

    # 2. 逐位处理长度恰好为 L 的情况
    # 预处理：把 digits 转成整数集合，便于比较
    digit_set = set(int(d) for d in digits)

    for i, ch in enumerate(s):
        cur = int(ch)              # n 的第 i 位（从左到右）
        # 统计比 cur 小的可选数字个数
        smaller = sum(1 for d in digit_set if d < cur)

        # 这部分数字在前 i 位与 n 完全相同，第 i 位取更小的数，后面随意填
        remaining = L - i - 1
        total += smaller * (k ** remaining)

        # 如果 cur 本身不在可选集合中，后面的位再也无法匹配 n 的前缀，直接退出
        if cur not in digit_set:
            break
    else:
        # 循环正常结束，说明 n 的每一位都在 digits 中，n 本身也是合法数
        total += 1

    return total
```

#### 复杂度  

- **时间复杂度**：`O(L)`，这里的 `L = len(str(n)) ≤ 9`。  
  用大白话说，就是「只看了一遍 n 的每一位」，和 `digits` 的大小无关。  
  相比暴力的指数级，这相当于把「枚举」变成了「算数」。
- **空间复杂度**：`O(1)`（常数级），只用了几个整数变量和一个集合（最多 9 个元素），不随输入规模增长。

---

## 心得  

- **核心技巧**：**按位计数 + 幂次**（即“在每一位上统计比目标小的选择数，再乘以后面自由填的方式数”）。  
- **适用场景**：  
  1. **数字集合限制的计数**（如本题、LeetCode 357 “Count Numbers with Unique Digits”）。  
  2. **求小于等于某个上限的组合数**（如“数位 DP”中经常出现的“前缀相等”转移）。  
  3. **字典序排列的第 K 小数**（如“寻找第 K 小的好数”）。  
- **一句话总结**：只要把「枚举」改成「每位独立计数」并利用“幂次”把后面的自由度算进去，就能把指数级降到线性级。

---

## 反思  

- **第一反应**：直接想把所有可能的数字生成出来，检查是否 ≤ n。  
- **最容易踩的坑**：  
  - 忘记把 **长度小于 n 位数** 的全部组合算进去。  
  - 在按位计数时，没有正确处理 “当前位的数字不在集合里” 时的提前结束。  
  - 计算 `k ** remaining` 时容易写成 `k ^ remaining`（异或），导致错误。  
- **下次遇到同类题**，第一步应该想到 **“先把位数分层，短的直接计数，长的按位逐位统计”**，即先把问题拆成 “长度” 与 “前缀相等” 两个子问题，再分别求解。