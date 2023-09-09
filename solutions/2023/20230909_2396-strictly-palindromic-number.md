# #2396. 严格回文数 / Strictly Palindromic Number

> 难度：中等 · 标签：Math、Two Pointers、Brainteaser · [LeetCode 链接](https://leetcode.com/problems/strictly-palindromic-number/)

---

## 题目（英文原版）

**Description**

An integer n is strictly palindromic if, for every base b between 2 and n - 2 (inclusive), the string representation of the integer n in base b is palindromic.
Given an integer n, return true if n is strictly palindromic and false otherwise.
A string is palindromic if it reads the same forward and backward.

**Examples**

**Example 1:**

```
Input: n = 9
Output: false
Explanation: In base 2: 9 = 1001 (base 2), which is palindromic.
In base 3: 9 = 100 (base 3), which is not palindromic.
Therefore, 9 is not strictly palindromic so we return false.
Note that in bases 4, 5, 6, and 7, n = 9 is also not palindromic.
```

**Example 2:**

```
Input: n = 4
Output: false
Explanation: We only consider base 2: 4 = 100 (base 2), which is not palindromic.
Therefore, we return false.
```

**Constraints**

- 4 <= n <= 105

---

## 题目（中文翻译）

一个整数 **n** 若满足：对于所有介于 2 到 **n**−2（含）之间的进制 **b**（base），整数 **n** 在该进制下的字符串表示是回文的（palindromic），则称 **n** 为**严格回文数**。  
给定整数 **n**，如果 **n** 是严格回文数返回 `true`，否则返回 `false`。  

**回文字符串**（palindromic string）指正读和倒读完全相同的字符串。

### 示例

#### 示例 1
**输入**  
```
n = 9
```
**输出**  
```
false
```
**解释**  
- 在进制 2 中：9 = 1001（base 2），是回文的。  
- 在进制 3 中：9 = 100（base 3），不是回文的。  

因此 9 不是严格回文数，返回 `false`。注意在进制 4、5、6、7 中，9 也都不是回文的。

#### 示例 2
**输入**  
```
n = 4
```
**输出**  
```
false
```
**解释**  
我们只需考虑进制 2：4 = 100（base 2），不是回文的。  

所以返回 `false`。

### 约束条件
- 4 ≤ **n** ≤ 10⁵

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把 n 用每一种可能的进制（2 … n‑2）都写出来，检查每个字符串是不是回文**。  
- **把整数转成其它进制**：可以像除法进位一样不断除以基数 `b`，把余数记下来，最后倒序得到该进制下的表示。  
- **回文判断**：把得到的字符串和它反转后的字符串比较，若相同则是回文。  

> **类比**：把哈希表想成一本字典，键（key）是单词，值（value）是页码。这里我们把「进制」当作「字典的查找入口」，每一次查找（即把 n 转成该进制）都会得到一段「文字」——我们要检查这些文字是否前后读起来一样。

只要对所有基数都做一次检查，所有检查都通过就返回 `True`，否则返回 `False`。

#### 代码（Python）

```python
def is_strictly_palindromic_bruteforce(n: int) -> bool:
    # 把整数 x 转成进制 b 的字符串
    def to_base(x: int, b: int) -> str:
        digits = []
        while x:
            digits.append(str(x % b))   # 余数就是当前位
            x //= b
        # 余数是倒序得到的，需要反转回来
        return ''.join(reversed(digits))

    # 检查一个字符串是否回文
    def is_palindrome(s: str) -> bool:
        return s == s[::-1]   # Python 切片，省时省力

    # 暴力遍历所有可能的进制 2 … n-2
    for base in range(2, n - 1):
        representation = to_base(n, base)
        if not is_palindrome(representation):
            return False        # 只要有一个进制不是回文，就不是严格回文数
    return True
```

#### 复杂度

- **时间复杂度**：`O(n * log_b n)`，这里 `log_b n` 表示把 n 转成进制 b 时产生的位数。最坏情况下（b=2）位数约为 `log₂ n`，而我们要遍历 `n‑2` 种进制，所以大致是 `O(n log n)`。用大白话说，就是**随着 n 增大，运行时间会像 n 乘以它的二进制位数那样增长**，在最坏的 `10⁵` 时会比较慢。
- **空间复杂度**：`O(log n)`，因为一次转换只需要保存当前进制下的位数（最多 `log₂ n` 位），不随遍历的进制数增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于我们要遍历几乎所有的进制**。事实上，这道题有一个非常关键的数学观察，使得我们根本不需要真的遍历：

> **观察**：对于任意 `n ≥ 4`，在进制 `b = n‑2` 下，`n` 的表示必然是 `"12"`（因为 `n = 1·(n‑2) + 2`），而 `"12"` 显然不是回文。

由于题目要求「对于 **所有** 基数 2 … n‑2 都要是回文」，只要找到 **任意一个** 不满足的基数就可以直接返回 `False`。进制 `n‑2` 总是满足不回文的条件（`n ≥ 4`），所以 **不存在任何 `n` 会是严格回文数**。

因此最优解只需要 **直接返回 `False`**，不需要做任何计算。

> **类比**：想象你在检查一列灯是否全亮，只要发现第一盏灯是灭的，就立刻可以断定「全亮」不成立，而不必检查后面的灯。这里的「第一盏灯」就是进制 `n‑2`，它总是「灭」的（不是回文），所以直接返回 `False`。

#### 代码（Python）

```python
def is_strictly_palindromic(n: int) -> bool:
    """
    对于任意 n >= 4，n 在进制 (n-2) 下的表示是 "12"，必定不是回文。
    因此严格回文数不存在，直接返回 False。
    """
    return False
```

#### 复杂度

- **时间复杂度**：`O(1)`，只做一次常数时间的返回操作。与 `n` 的大小无关，几乎是瞬间完成。
- **空间复杂度**：`O(1)`，不使用额外的存储。

---

## 心得

- **核心技巧**：利用**数学推导**直接排除所有可能性，而不是穷举检查。  
- **适用的题型**：  
  1. 需要对所有“某个范围内的所有情况”都满足条件的问题，往往可以找一个**必然不满足的特例**直接否定。  
  2. “进制/数位”相关的题目，经常可以通过**进制的极端取值**（如 `b = n-1、n-2`）快速得到结论。  
  3. 需要判断“是否所有 X 都满足 Y”的题目，思路是**找出一个反例**即可。
- **一句话总结**：**只要进制 `n‑2` 的表示不是回文，严格回文数永远不存在**。

---

## 反思

- **第一反应**：看到「所有基数都要回文」自然想到**遍历全部基数**，这是一种直觉的暴力思路。  
- **最容易踩的坑**：忘记考虑 **极端进制**（如 `b = n-2`），导致不必要的复杂实现；或者在实现进制转换时忘记处理 `n` 为 0 的特殊情况（本题中 n≥4 不会出现）。  
- **下次遇到同类题**：第一步先**思考是否存在必然不满足的极端情况**，如果能找到，就可以直接得出答案；否则再考虑逐一枚举或使用更高效的算法。