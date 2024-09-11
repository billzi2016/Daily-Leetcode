# #2864. 最大奇数二进制数 / Maximum Odd Binary Number

> 难度：简单 · 标签：Math、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-odd-binary-number/)

---

## 题目（英文原版）

**Description**

You are given a binary string s that contains at least one '1'.
You have to rearrange the bits in such a way that the resulting binary number is the maximum odd binary number that can be created from this combination.
Return a string representing the maximum odd binary number that can be created from the given combination.
Note that the resulting string can have leading zeros.

**Examples**

**Example 1:**

```
Input: s = "010"
Output: "001"
Explanation: Because there is just one '1', it must be in the last position. So the answer is "001".
```

**Example 2:**

```
Input: s = "0101"
Output: "1001"
Explanation: One of the '1's must be in the last position. The maximum number that can be made with the remaining digits is "100". So the answer is "1001".
```

**Constraints**

- 1 <= s.length <= 100
- s consists only of '0' and '1'.
- s contains at least one '1'.

---

## 题目（中文翻译）

给定一个只包含 `'0'` 和 `'1'` 的二进制字符串（binary string）`s`，且其中至少包含一个 `'1'`。  
你需要重新排列（rearrange）其中的位（bits），使得得到的二进制数是能够由该组合形成的 **最大奇数二进制数（maximum odd binary number）**。  
返回表示该最大奇数二进制数的字符串。  
注意，结果字符串可以包含前导零。

## 示例

### 示例 1
**输入:** `s = "010"`  
**输出:** `"001"`  
**解释:** 由于只有一个 `'1'`，它必须放在最后一位（奇数位），因此答案为 `"001"`。

### 示例 2
**输入:** `s = "0101"`  
**输出:** `"1001"`  
**解释:** 必须有一个 `'1'` 位于最后一位。将其余位重新排列，使得到的数最大，即 `"100"`，再加上末位的 `'1'`，得到 `"1001"`。

## 约束条件
- `1 <= s.length <= 100`
- `s` 仅由字符 `'0'` 和 `'1'` 组成
- `s` 至少包含一个 `'1'`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把字符串 `s` 的所有字符全排列，逐个检查得到的二进制数是否为 **奇数**（即最后一位是 `'1'`），然后在所有符合条件的排列里挑出数值最大的那一个。

- **用到的数据结构**：  
  - **列表 / 数组**：用来存放字符的排列。可以把它想象成把一堆字母卡片排成一行。  
  - **哈希表（字典）**（可选）：如果要去重相同的排列，可以把已经出现过的排列放进字典里，类似查字典时，用词（key）找对应的页码（value），这里的词是排列本身，页码可以随便设。

- **为什么正确**：  
  - 所有可能的重新排列都被枚举到了，因而不会漏掉任何合法解。  
  - 只要挑选出满足“最后一位是 `'1'`”且数值最大的排列，就是答案。

- **时间/空间复杂度**（大白话解释）：  
  - **时间复杂度**：`O(n!)`（n 的阶乘）。想象有 `n` 张卡片，每张卡片都有 `n` 种放置位置，第一张有 `n` 种选择，第二张剩 `n‑1` 种……所以总共要尝试 `n × (n‑1) × … × 1` 种排列。对于 `n = 10` 已经是几千万次了，`n = 20` 更是天文数字，根本跑不完。  
  - **空间复杂度**：`O(n)`，因为我们只需要保存当前的排列（长度为 `n` 的列表）和几个临时变量。

#### 代码（Python）

```python
import itertools

def maximumOddBinaryNumber_bruteforce(s: str) -> str:
    """
    暴力枚举所有排列，挑选最大奇数。
    仅用于演示概念，实际提交会超时。
    """
    best = ""                     # 记录目前找到的最大合法字符串
    # itertools.permutations 会产生所有可能的排列（含重复）
    for perm in set(itertools.permutations(s)):
        cand = ''.join(perm)      # 把元组转回字符串
        if cand[-1] == '1':       # 奇数的必要条件：最后一位是 '1'
            # 字符串比较在二进制意义上等价于数值比较
            if cand > best:
                best = cand
    return best
```

#### 复杂度

- **时间复杂度**：`O(n!)` — 随着字符数 `n` 增长，排列数呈阶乘级增长，几乎不可能在 1 秒内完成。
- **空间复杂度**：`O(n)` — 只保存当前排列和若干临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于枚举所有排列。其实我们根本不需要真的把字符全部排出来，只要**利用二进制的性质**就能直接构造出答案。

二进制奇数的定义非常简单：**最低位（最右边）一定是 `'1'`**。  
其余位想要让数值最大，只要把所有剩余的 `'1'` 放在**最高位**（左边）即可，零自然会被推到中间或右侧。

于是可以把问题拆成两步：

1. **确定最后一位一定是 `'1'`**。因为题目保证原串里至少有一个 `'1'`，我们把其中的一个 `'1'` 留给末位。
2. **其余字符重新排列，使数值最大**。这等价于把剩下的 `'1'` 全部放在左边，剩余的 `'0'` 放在左边 `'1'` 之后（即中间），最后再接上步骤 1 的 `'1'`。

实现时，只需要统计原串中 `'1'` 的个数 `cnt1`：

- 用掉一个 `'1'` 放在末位，剩下 `cnt1-1` 个 `'1'` 放在最左侧。
- 其余位置全是 `'0'`，数量为 `len(s) - (cnt1-1) - 1`。

**类比**：想象有若干红球（代表 `'1'`）和若干蓝球（代表 `'0'`），我们要把红球尽量放在左边，使得从左到右看的“重量”最大，而最右边必须放一个红球保证奇数。

#### 代码（Python）

```python
def maximumOddBinaryNumber(s: str) -> str:
    """
    O(n) 时间直接构造最大奇数二进制字符串。
    思路：最后一定是 '1'，其余的 '1' 全部排到最左边，剩下的填 '0'。
    """
    cnt1 = s.count('1')               # 统计 '1' 的个数
    # 1) 左边放 cnt1-1 个 '1'
    left_ones = '1' * (cnt1 - 1)
    # 2) 中间放剩余的 '0'
    zeros = '0' * (len(s) - (cnt1 - 1) - 1)
    # 3) 最后固定一个 '1'
    result = left_ones + zeros + '1'
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串统计 `'1'` 的数量，然后使用字符串乘法拼接，整体线性随输入长度增长。相较于暴力的 `O(n!)`，快得多，几乎是瞬间完成。
- **空间复杂度**：`O(n)` — 生成的结果字符串占用 `n` 长度的空间，除此之外只用了常数级的临时变量。

---

## 心得

- **核心技巧**：利用二进制奇数必须以 `'1'` 结尾的特性，结合“把剩余的 `'1'` 全部放在最高位”这一贪心思想直接构造答案。
- **适用的题型**：  
  1. “最大/最小奇数（或偶数）”类问题，如 *Maximum Odd Number after Rearrangement*。  
  2. “把字符重新排列以满足某种数值最优”类，如 *Largest Number formed by Digits*（把数字字符排序）。  
  3. “利用位数特性直接构造答案”类，如 *Maximum Even Binary Number*（只需把 `'0'` 放末位）。
- **一句话总结解题钥匙**：**“奇数 → 末位必为 1；其余位最大 → 把所有剩余的 1 放左边”。**

---

## 反思

- **第一反应**：看到“重新排列二进制位得到最大奇数”，自然想到“最后一位必须是 1”，然后想办法把其余位最大化。
- **最容易踩的坑**：  
  - 忘记题目允许**前导零**，所以不需要去掉开头的 `'0'`。  
  - 当只有一个 `'1'` 时，`cnt1-1` 为 0，左侧不应出现 `'1'`，代码中需要正确处理这种情况（上述实现已兼容）。  
  - 错误地把所有 `'1'` 都放左边，导致最后一位是 `'0'`，从而得到偶数。
- **下次遇到同类题的第一步**：**先明确必然的位（奇数/偶数的最低位）**，再**把剩余的相同字符按照数值大小的贪心原则放置**（大字符左侧，小字符右侧）。这样往往可以在 O(n) 时间内直接得到答案。