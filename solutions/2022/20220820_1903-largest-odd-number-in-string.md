# #1903. **字符串中的最大奇数** / Largest Odd Number in String

> 难度：简单 · 标签：Math、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/largest-odd-number-in-string/)

---

## 题目（英文原版）

**Description**

You are given a string num, representing a large integer. Return the largest-valued odd integer (as a string) that is a non-empty substring of num, or an empty string "" if no odd integer exists.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: num = "52"
Output: "5"
Explanation: The only non-empty substrings are "5", "2", and "52". "5" is the only odd number.
```

**Example 2:**

```
Input: num = "4206"
Output: ""
Explanation: There are no odd numbers in "4206".
```

**Example 3:**

```
Input: num = "35427"
Output: "35427"
Explanation: "35427" is already an odd number.
```

**Constraints**

- 1 <= num.length <= 105
- num only consists of digits and does not contain any leading zeros.

---

## 题目（中文翻译）

你得到一个字符串 `num`，它表示一个很大的整数。返回 `num` 的非空子串（substring）中，值最大的奇整数（odd integer），并以字符串形式返回；如果不存在奇整数，则返回空字符串 `""`。

子串（substring）是指字符串中连续的一段字符序列。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  

- $1 \leq \text{num.length} \leq 10^5$
- `num` 仅由数字组成，且不含前导零。

**示例**

**示例 1**  
Input: `num = "52"`  
Output: `"5"`  
Explanation: 所有非空子串为 `"5"`、`"2"` 和 `"52"`。其中只有 `"5"` 是奇数。

**示例 2**  
Input: `num = "4206"`  
Output: `""`  
Explanation: 在 `"4206"` 中不存在奇数。

**示例 3**  
Input: `num = "35427"`  
Output: `"35427"`  
Explanation: `"35427"` 本身已经是奇数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的非空子串** 都枚举出来，逐个判断它们对应的整数是否是奇数，最后挑选出最大的那个。  
- **子串**：可以把字符串想象成一串珠子，子串就是把相邻的几颗珠子挑出来。  
- **奇数判断**：整数的奇偶只跟最后一位数字有关，奇数的最后一位一定是 1、3、5、7、9。  

实现步骤：

1. 用两层循环，外层决定子串的左端点 `i`，内层决定右端点 `j`（`i ≤ j < n`），这样就能得到 `num[i:j+1]` 这段子串。  
2. 把子串转成整数（或直接看最后一位字符），判断是否为奇数。  
3. 若是奇数，更新答案为当前子串（因为我们是从左到右、从短到长遍历的，直接比较字符串大小即可）。  

> **为什么正确？**  
> 我们遍历了 *所有* 合法的子串，且每个子串都检查了奇偶性并与当前最优答案比较，最终留下的必然是最大奇数子串。

#### 代码（Python）

```python
def largestOddNumber_bruteforce(num: str) -> str:
    n = len(num)
    best = ""                     # 用来保存目前找到的最大奇数子串
    for i in range(n):            # 左端点 i
        for j in range(i, n):      # 右端点 j（包含）
            sub = num[i:j+1]       # 取出子串
            # 判断子串对应的整数是否为奇数，只需看最后一位字符
            if int(sub[-1]) % 2 == 1:   # 奇数
                # 直接比较字符串大小（长度相同则字典序相同），更长的自然更大
                if len(sub) > len(best) or (len(sub) == len(best) and sub > best):
                    best = sub
    return best
```

> **关键行中文注释**  
> - `for i in range(n):` 遍历子串左边界  
> - `for j in range(i, n):` 遍历子串右边界  
> - `if int(sub[-1]) % 2 == 1:` 检查子串最后一位是否为奇数  

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层 `n` 次，内层平均也要遍历 `n/2` 次，约等于 `n²/2`，大概是“平方级”。当 `n = 10⁵` 时，`n²` 会达到 10¹⁰，远远超出计算机在一秒内能完成的次数，实际会超时。  
- **空间复杂度**：`O(1)`（不计返回值）  
  只用了常数级的额外变量 `best`、`i`、`j` 等。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于枚举所有子串——这一步是 `O(n²)`。  
观察题目要求的“最大奇数子串”，我们不需要真的枚举，它有一个非常重要的**位置特性**：

> **如果一个奇数子串存在，那么它一定以最靠右的奇数字符结尾。**  
> 因为奇数的奇偶性只和最后一位有关，若我们把子串往右扩展，只要右端仍是奇数，数值只会变大（多了左边的高位），所以答案必然是 **从字符串开头一直取到最右侧的奇数位**。

基于此，只需一次线性扫描：

1. 从右向左遍历 `num`，找到第一个奇数字符（`1,3,5,7,9`）。  
2. 若找到了，返回 `num[:pos+1]`（从开头到该奇数位，包括它）。  
3. 若遍历完仍未找到奇数，说明整个字符串里没有奇数子串，返回空串 `""`。

这一步只需要一次遍历，时间 `O(n)`，空间 `O(1)`。

#### 代码（Python）

```python
def largestOddNumber(num: str) -> str:
    """
    返回 num 中最大的奇数子串（作为字符串）。
    思路：从右往左找第一个奇数字符，返回左侧全部字符。
    """
    # 从右往左检查每个字符是否为奇数
    for i in range(len(num) - 1, -1, -1):
        if (ord(num[i]) - ord('0')) % 2 == 1:   # ord('3')-ord('0') = 3，取模判断奇偶
            # 找到后，直接切片返回左侧全部字符（包括当前奇数位）
            return num[:i + 1]
    # 没有任何奇数位，返回空串
    return ""
```

> **关键行中文注释**  
> - `for i in range(len(num) - 1, -1, -1):` 从右向左遍历索引  
> - `if (ord(num[i]) - ord('0')) % 2 == 1:` 利用字符的 ASCII 码判断奇偶（不必转成整数）  
> - `return num[:i + 1]` 切片得到从开头到当前奇数位的子串  

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次字符串，线性级别。对比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(1)`  
  只用了几个整数变量 `i`，不随输入规模增长。

---

## 心得

- **核心技巧**：**从右往左寻找满足条件的字符**，利用“奇数只和最后一位有关”这一数学性质把子串问题转化为单字符定位。  
- **适用场景**（类似题目）  
  1. “找出能被 5 整除的最大子串” → 从右找首个能被 5 整除的数字（0 或 5）。  
  2. “删除最右侧的偶数，使剩余部分最大” → 同理从右找偶数。  
  3. “找出字母表中最大（或最小）字符出现位置并截断” → 从右找对应字符。  
- **一句话总结**：**只要答案的“奇偶”只受最后一位决定，就把问题简化为“找最右的满足位”，其左侧全保留即为最大答案**。

## 反思

- **第一反应**：想到枚举所有子串检查奇偶——这是一种“全搜索”的直觉。  
- **最容易踩的坑**  
  - 忘记子串必须是 **非空**，所以即使没有奇数也要返回 `""` 而不是 `None`。  
  - 直接把子串转成整数会导致 **大整数溢出**（虽然 Python 能处理，但在语言限制下会出错），实际上只要检查最后一位字符即可。  
  - 忽略了 **从右往左** 的思路，导致仍做不必要的遍历。  
- **下次遇到同类题**：第一步先思考“答案的关键属性是否只依赖于某一位（或局部）”，如果是，就尝试 **单遍扫描定位**，而不是全局枚举。这样往往能把时间复杂度从平方级降到线性级。