# #1945. 转换后字符串的数字之和 / Sum of Digits of String After Convert

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/sum-of-digits-of-string-after-convert/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters, and an integer k. Your task is to convert the string into an integer by a special process, and then transform it by summing its digits repeatedly k times. More specifically, perform the following steps:
For example, if s = "zbax" and k = 2, then the resulting integer would be 8 by the following operations:
Return the resulting integer after performing the operations described above.

**Examples**

**Example 1:**

```
Input: s = "iiii", k = 1
Output: 36
Explanation:
The operations are as follows: - Convert: "iiii" ➝ "(9)(9)(9)(9)" ➝ "9999" ➝ 9999 - Transform #1: 9999 ➝ 9 + 9 + 9 + 9 ➝ 36 Thus the resulting integer is 36.
```

**Example 2:**

```
Input: s = "leetcode", k = 2
Output: 6
Explanation:
The operations are as follows: - Convert: "leetcode" ➝ "(12)(5)(5)(20)(3)(15)(4)(5)" ➝ "12552031545" ➝ 12552031545 - Transform #1: 12552031545 ➝ 1 + 2 + 5 + 5 + 2 + 0 + 3 + 1 + 5 + 4 + 5 ➝ 33 - Transform #2: 33 ➝ 3 + 3 ➝ 6 Thus the resulting integer is 6.
```

**Example 3:**

```
Input: s = "zbax", k = 2
Output: 8
```

**Constraints**

- 1 <= s.length <= 100
- 1 <= k <= 10
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s` 和一个整数 `k`。你的任务是先按照特殊过程将字符串转换为一个整数，然后对该整数执行 `k` 次“求数字之和”（sum of digits）的变换。具体步骤如下：

1. **转换**：将字符串中的每个字符替换为其在字母表中的位置（`a → 1`，`b → 2`，……，`z → 26`），得到若干整数后直接拼接成一个新的字符串，再将其视为十进制整数。  
2. **变换**：对得到的整数求各位数字之和，得到新的整数。上述过程重复 `k` 次。

返回完成所有操作后得到的整数。

## 示例

### 示例 1
**输入**  
`s = "iiii", k = 1`  

**输出**  
`36`  

**解释**  
操作过程如下：  
- 转换：`"iiii"` → `"(9)(9)(9)(9)"` → `"9999"` → `9999`  
- 第 1 次变换：`9999` → `9 + 9 + 9 + 9` → `36`  

因此最终得到的整数为 `36`。

### 示例 2
**输入**  
`s = "leetcode", k = 2`  

**输出**  
`6`  

**解释**  
操作过程如下：  
- 转换：`"leetcode"` → `"(12)(5)(5)(20)(3)(15)(4)(5)"` → `"12552031545"` → `12552031545`  
- 第 1 次变换：`12552031545` → `1 + 2 + 5 + 5 + 2 + 0 + 3 + 1 + 5 + 4 + 5` → `33`  
- 第 2 次变换：`33` → `3 + 3` → `6`  

因此最终得到的整数为 `6`。

### 示例 3
**输入**  
`s = "zbax", k = 2`  

**输出**  
`8`  

## 约束条件

- `1 <= s.length <= 100`
- `1 <= k <= 10`
- `s` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **把字母转成数字**  
   - a → 1、b → 2 … z → 26。  
   - 把每个数字直接写成字符拼接在一起，得到一个很长的数字字符串。  
   - 这一步可以想象成 **把字典里每个词的页码写下来**，词是字母，页码是对应的数字。  

2. **把字符串转成整数**  
   - Python 的 `int()` 能把纯数字的字符串一次性变成整数。  

3. **重复 k 次求各位数字之和**  
   - 把整数拆成每一位，再相加得到新的整数，循环 k 次。  

> **为什么能得到正确答案**  
> 题目要求先把字母对应的数字“拼接”成一个整体数字，然后对这个整体数字做 k 次“各位求和”。上述步骤正好完整实现了这两个过程，所以一定会得到正确答案。  

#### 代码（Python）  

```python
def getLucky(s: str, k: int) -> int:
    # 1️⃣ 把每个字母转成对应的数字并拼接成一个大字符串
    num_str = ''
    for ch in s:
        # ord('a') == 97，减去 96 正好得到 1~26
        num_str += str(ord(ch) - ord('a') + 1)

    # 2️⃣ 把大字符串直接转成整数
    cur = int(num_str)

    # 3️⃣ 重复 k 次求各位数字之和
    for _ in range(k):
        nxt = 0
        while cur > 0:
            nxt += cur % 10          # 取最低位
            cur //= 10               # 去掉最低位
        cur = nxt                    # 进入下一轮
    return cur
```

#### 复杂度  

- **时间复杂度**：`O(L + k·D)`  
  - `L = len(s)`，把字母转成数字需要遍历一次 O(L)。  
  - `D` 是第一次求和时数字的位数，最坏情况是 100（因为 `s` 最长 100，最多产生 200 位），所以 `k·D` 也在可接受范围。整体上可以看成 **线性**。  
- **空间复杂度**：`O(L)`  
  - 需要一个临时字符串 `num_str` 来保存拼接后的数字，长度最多约为 200（每个字母最多两位），与输入长度同阶。

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于把所有数字拼成一个巨大的整数，然后再逐位拆分求和。事实上我们并不需要真正得到那个“大整数”，只要得到**各位数字之和**即可。

**关键观察**  

- 每个字母对应的数字最多是两位（26），所以它的各位数字之和最多是 `2 + 6 = 8`。  
- 第一次 “求和” 的结果其实就是：  
  \[
  \sum_{c\in s}\bigl(\text{十位数} + \text{个位数}\bigr)
  \]
  也就是把每个字母对应的数字直接拆成个位、十位再相加。  
- 这样我们可以在 **遍历一次字符串** 时直接得到第一次求和的结果，省掉拼接、转整数、再拆位的过程。  

**优化步骤**  

1. **遍历字符串**，对每个字符  
   - 计算 `val = ord(ch) - ord('a') + 1`（1~26）。  
   - 把 `val` 的十位和个位相加（`val // 10 + val % 10`），累加到 `total`。  
2. 现在 `total` 已经是 **第一次求和** 的结果。  
3. **剩余的 k‑1 次** 仍然是 “各位求和”。因为 `total` 已经是一个普通整数，直接用循环把它的每一位相加即可。  
   - 这里可以使用 **数字根**（digital root）快速得到最终答案，但题目限制 `k ≤ 10`，普通循环已经足够快，代码更易懂。  

> **为什么最优**  
> 只遍历一次字符串，时间上从 “O(L + D)” 降到 **O(L + k·log total)**，而 `total` 本身不超过 `100 * 26 = 2600`，所以后面的循环几乎可以忽略不计。空间只用了常数级变量 `O(1)`。

#### 代码（Python）  

```python
def getLucky(s: str, k: int) -> int:
    # 1️⃣ 第一次求和：直接把每个字母对应的数字拆成个位+十位累加
    total = 0
    for ch in s:
        val = ord(ch) - ord('a') + 1      # 1 ~ 26
        total += val // 10 + val % 10     # 十位 + 个位

    # 2️⃣ 之后再做 k-1 次各位求和
    for _ in range(k - 1):
        nxt = 0
        while total > 0:
            nxt += total % 10
            total //= 10
        total = nxt

    return total
```

#### 复杂度  

- **时间复杂度**：`O(L + k·log total)`  
  - 第一次遍历 `s` 为 `O(L)`（L ≤ 100）。  
  - 随后的每一次求和最多只需要几次循环（因为 `total` ≤ 2600，位数 ≤ 4），所以 `k·log total` 非常小。整体上几乎是线性 `O(L)`。  
- **空间复杂度**：`O(1)`  
  - 只使用了几个整数变量，没有额外的数组或字符串。

---

## 心得  

- **核心技巧**：把“把字母拼成大数再求和”转化为“直接对每个字母的数值拆位求和”。本质是**避免不必要的大数构造**。  
- **适用的题型**  
  1. **字符串转数字后求和**（如 LeetCode 1945 – Sum of Digits of String After Convert）。  
  2. **需要对每个字符的数值做累计**的题目（如把字母映射为分数求总分）。  
  3. **多次数字位求和**的题目（如求数字根、数字迭代求和）。  
- **一句话总结解题钥匙**：**“先把每一步的数学意义写清楚，再看能不能直接算出结果，省掉中间的‘大数字’”。**

---

## 反思  

- **第一反应**：把字母转换成数字后直接拼成一个长整数，再逐位求和。  
- **最容易踩的坑**  
  - 直接拼接后转 `int` 可能会产生非常大的数（虽然本题限制不大，但在更宽松的约束下会导致溢出或性能问题）。  
  - 忽视 `k` 次求和的累计效应，写成只做一次求和。  
  - 边界情况：单字符、`k = 1`，以及字母对应的两位数（如 10~26）需要拆位相加。  
- **下次遇到同类题**：第一步先**思考是否真的需要构造完整的数值**，如果只需要“各位之和”，可以直接在遍历时拆位累计，避免中间大数。