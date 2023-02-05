# #2119. 双重反转后的数字 / A Number After a Double Reversal

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/a-number-after-a-double-reversal/)

---

## 题目（英文原版）

**Description**

Reversing an integer means to reverse all its digits.
Given an integer num, reverse num to get reversed1, then reverse reversed1 to get reversed2. Return true if reversed2 equals num. Otherwise return false.

**Examples**

**Example 1:**

```
Input: num = 526
Output: true
Explanation: Reverse num to get 625, then reverse 625 to get 526, which equals num.
```

**Example 2:**

```
Input: num = 1800
Output: false
Explanation: Reverse num to get 81, then reverse 81 to get 18, which does not equal num.
```

**Example 3:**

```
Input: num = 0
Output: true
Explanation: Reverse num to get 0, then reverse 0 to get 0, which equals num.
```

**Constraints**

- 0 <= num <= 106

---

## 题目（中文翻译）

**描述**  
反转（reverse）一个整数指的是把它的所有数字顺序倒置。  
给定整数 `num`，先将 `num` 反转得到 `reversed1`，再将 `reversed1` 反转得到 `reversed2`。如果 `reversed2` 与 `num` 相等，则返回 `true`；否则返回 `false`。

**示例**

**示例 1**  
```
Input: num = 526
Output: true
Explanation: 将 num 反转得到 625，再将 625 反转得到 526，恰好等于原始的 num。
```

**示例 2**  
```
Input: num = 1800
Output: false
Explanation: 将 num 反转得到 81，再将 81 反转得到 18，结果不等于原始的 num。
```

**示例 3**  
```
Input: num = 0
Output: true
Explanation: 将 num 反转得到 0，再将 0 反转得到 0，仍然等于原始的 num。
```

**约束条件**  
- `0 <= num <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把整数 **逐位翻转** 两次，然后比较结果是否和原数相等。  
翻转整数可以有两种常见实现方式：

1. **把整数转成字符串**，再把字符串倒序（`[::-1]`），最后再转回整数。  
   - 类比：把一本书的每一页号码写在纸上，先把纸翻过去再翻回来，等价于把页码顺序倒置。
2. **数学方式**：不断取最低位 (`num % 10`) 放到新数的高位 (`rev = rev*10 + digit`)，然后把原数除以 10 (`num //= 10`)。  
   - 类比：把装满弹珠的管子倒过来，让最下面的弹珠先出来，依次往新管子里装。

无论哪种实现，只要把**第一次翻转**得到 `rev1`，再把 `rev1` 再翻转一次得到 `rev2`，最后比较 `rev2 == original` 即可。

**为什么这个方法一定正确？**  
因为我们严格按照“把所有数字顺序倒过来”的定义去做两次，数学上把一个序列倒两次会恢复原序列（除非在倒序过程中丢失了信息，例如末尾的 0 被去掉），所以只要实现不出错，答案必然是对的。

#### 代码（Python）

```python
def reverse_number(num: int) -> int:
    """
    将整数 num 的每一位翻转，返回翻转后的整数。
    这里使用数学方式避免字符串带来的额外开销。
    """
    rev = 0
    while num > 0:
        digit = num % 10          # 取最低位数字
        rev = rev * 10 + digit    # 把它放到新数的最高位
        num //= 10                # 去掉已经处理过的最低位
    return rev

def is_double_reverse_equal(num: int) -> bool:
    """
    先翻转一次，再翻转一次，比较是否等于原数。
    """
    rev1 = reverse_number(num)    # 第一次翻转
    rev2 = reverse_number(rev1)   # 第二次翻转
    return rev2 == num
```

#### 复杂度

- **时间复杂度：** `O(d)`，`d` 为数字的位数。  
  - 大白话：我们每走一位数字就做一次循环，位数越多花的时间越多。  
- **空间复杂度：** `O(1)`，只用了几个整数变量，和数字的大小无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正耗时的地方是**逐位遍历**数字。  
但观察题目可以发现：  
- 当我们把 `526` 翻转得到 `625`，再翻转回去又是 `526`，因为 **没有末尾的 0**。  
- 当我们把 `1800` 翻转得到 `81`，再翻转回去得到 `18`，因为 **原数末尾的 0 被丢掉**，信息永久消失了。

**关键点**：  
- 只要一个正整数 **不以 0 结尾**（即个位不是 0），翻转两次必然恢复原数。  
- 唯一的例外是 `0` 本身，虽然它“以 0 结尾”，但翻转后仍是 `0`，仍然满足条件。

所以我们不需要真的去翻转，只要检查：

1. `num == 0` → 返回 `True`。  
2. `num % 10 == 0`（个位是 0） → 返回 `False`。  
3. 其他情况 → 返回 `True`。

这一步只用了 **一次取余** 操作，时间几乎可以忽略不计。

#### 代码（Python）

```python
def is_double_reverse_equal(num: int) -> bool:
    """
    只通过检查末尾是否为 0（以及特殊的 0 本身）来判断两次翻转是否等于原数。
    """
    if num == 0:               # 0 翻转后仍是 0
        return True
    # 只要个位是 0，翻转一次就会丢掉这个 0，导致信息不可恢复
    return num % 10 != 0
```

#### 复杂度

- **时间复杂度：** `O(1)`，只做了常数次的整数运算。  
  - 大白话：不管数字有多大，程序只跑了一两步，速度永远是“瞬间”。  
- **空间复杂度：** `O(1)`，只用了几个整数变量。

---

## 心得

- **核心技巧**：利用**数位特性**（末位是否为 0）直接判断，而不是实际翻转。  
- **适用的题型**  
  1. 判断翻转后是否相同的题目（如 “Palindrome Number” 只需要检查两端是否相同）。  
  2. 需要判断整数在某种“对称”操作后是否保持不变的题目（如 “是否是回文数的倍数”）。  
- **解题钥匙**：**找出导致信息丢失的关键点**（这里是末尾的 0），往往能把 O(n) 的做法降到 O(1)。

## 反思

- **第一反应**：直接把数翻转两遍再比较，写出完整的翻转函数。  
- **最容易踩的坑**  
  - 忘记处理 `0` 这个特殊值，导致错误返回 `False`。  
  - 没意识到 **末位 0 会在第一次翻转时被丢掉**，从而误以为需要完整翻转才能判断。  
- **下次遇到类似题**：第一步先思考**“哪些位会在操作中消失或改变？”**，如果能定位到少数几个关键位，往往能直接得出 O(1) 的判断式。