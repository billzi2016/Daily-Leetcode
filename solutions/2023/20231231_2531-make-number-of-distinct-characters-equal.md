# #2531. **使不同字符数相等** / Make Number of Distinct Characters Equal

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/make-number-of-distinct-characters-equal/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed strings word1 and word2.
A move consists of choosing two indices i and j such that 0 <= i < word1.length and 0 <= j < word2.length and swapping word1[i] with word2[j].
Return true if it is possible to get the number of distinct characters in word1 and word2 to be equal with exactly one move. Return false otherwise.

**Examples**

**Example 1:**

```
Input: word1 = "ac", word2 = "b"
Output: false
Explanation: Any pair of swaps would yield two distinct characters in the first string, and one in the second string.
```

**Example 2:**

```
Input: word1 = "abcc", word2 = "aab"
Output: true
Explanation: We swap index 2 of the first string with index 0 of the second string. The resulting strings are word1 = "abac" and word2 = "cab", which both have 3 distinct characters.
```

**Example 3:**

```
Input: word1 = "abcde", word2 = "fghij"
Output: true
Explanation: Both resulting strings will have 5 distinct characters, regardless of which indices we swap.
```

**Constraints**

- 1 <= word1.length, word2.length <= 105
- word1 and word2 consist of only lowercase English letters.

---

## 题目（中文翻译）

给定两个 **0 索引的** 字符串 `word1` 和 `word2`。  
一次 **移动（move）** 定义为：选择满足 `0 <= i < word1.length` 且 `0 <= j < word2.length` 的下标 `i`、`j`，并交换 `word1[i]` 与 `word2[j]`。  

返回 `true` 当且仅当仅通过 **一次交换（swap）** 就可以使 `word1` 与 `word2` 中 **不同字符的数量（distinct characters）** 相等，否则返回 `false`。

---

#### 示例

**示例 1**  
```
Input: word1 = "ac", word2 = "b"
Output: false
Explanation: 任意一对交换都会导致第一个字符串拥有两个不同字符，而第二个字符串只有一个不同字符。
```

**示例 2**  
```
Input: word1 = "abcc", word2 = "aab"
Output: true
Explanation: 我们交换第一个字符串的下标 2 与第二个字符串的下标 0。交换后得到 `word1 = "abac"` 与 `word2 = "cab"`，两者的不同字符数量均为 3。
```

**示例 3**  
```
Input: word1 = "abcde", word2 = "fghij"
Output: true
Explanation: 不论交换哪一对下标，两个结果字符串的不同字符数量都会是 5。
```

---

#### 约束条件

- `1 <= word1.length, word2.length <= 10^5`
- `word1` 和 `word2` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的交换都试一遍**，看哪一次能让两段字符串的「不同字符的种类数」相等。

- **遍历所有下标**：对 `word1` 的每个位置 `i`（`0 ≤ i < len(word1)`）以及 `word2` 的每个位置 `j`（`0 ≤ j < len(word2)`）都尝试一次交换。  
- **交换后重新计数**：把这两个字符换位后，分别统计 `word1`、`word2` 中出现了多少种不同的字符（相当于把字符当成“词”，种类数就像字典里有多少页）。  
- **只要有一次相等就返回 `True`，全部尝试完都不行则返回 `False`**。

> **为什么能得到正确答案？**  
> 因为题目要求「恰好一次交换」后是否可能相等，枚举所有可能的交换必然会覆盖答案所在的那一次。

#### 代码（Python）

```python
from collections import Counter

def isItPossible_bruteforce(word1: str, word2: str) -> bool:
    n, m = len(word1), len(word2)

    # 计算原始的不同字符个数，后面会用来做快速对比
    def distinct_cnt(s: str) -> int:
        return len(set(s))

    # 直接遍历所有 i、j 组合
    for i in range(n):
        for j in range(m):
            # 复制一份字符串（因为 Python 的字符串是不可变的，需要生成新串）
            w1_list = list(word1)
            w2_list = list(word2)

            # 交换两个字符
            w1_list[i], w2_list[j] = w2_list[j], w1_list[i]

            # 统计交换后的不同字符数
            cnt1 = distinct_cnt(''.join(w1_list))
            cnt2 = distinct_cnt(''.join(w2_list))

            if cnt1 == cnt2:          # 找到一次成功的交换
                return True
    return False                     # 没有任何一次成功
```

> **关键行中文注释**  
> - `len(set(s))`：把字符串转成集合，集合里自动去重，长度就是不同字符的种类数。  
> - `w1_list[i], w2_list[j] = w2_list[j], w1_list[i]`：一次性完成两边字符的互换。  

#### 复杂度  

- **时间复杂度**：`O(n * m * (n + m))`  
  - 外层两层循环遍历所有 `i、j` 组合，次数是 `n·m`。  
  - 每一次交换后我们要重新遍历整个字符串求不同字符，最坏要看完整个 `word1`（`n`）和 `word2`（`m`），所以乘上 `n+m`。  
  - 用大白话说，就是如果两段文字各有 10⁵ 个字符，时间会天文数字级别，根本跑不动。

- **空间复杂度**：`O(n + m)`  
  - 需要把原始字符串转成列表（复制），最坏要占用和原字符串同等大小的额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“每一次交换都重新遍历整段字符串”**。  
实际上我们只需要关心 **每个字符出现的次数**，而不是字符的顺序。于是可以把每段字符串的字符频率放进长度为 26 的数组（因为只含小写英文字母），这相当于一本“字符出现次数的字典”，下标 `0~25` 对应 `'a'~'z'`，值是出现次数。

> **核心观察**  
> 设 `cnt1[c]` 为 `word1` 中字符 `c` 的出现次数，`cnt2[c]` 为 `word2` 中字符 `c` 的出现次数。  
> 把 `word1[i] = x` 与 `word2[j] = y` 交换后，只有 **四个计数会变化**：  
> - `cnt1[x]` 减 1，`cnt1[y]` 加 1  
> - `cnt2[y]` 减 1，`cnt2[x]` 加 1  

> 其余字符的出现次数保持不变。  
> 因此我们可以 **在 O(1) 时间内** 计算交换后两段字符串的不同字符数（即出现次数 > 0 的种类数），而不必重新遍历整个字符串。

> **怎么遍历所有可能的交换？**  
> 由于字符种类只有 26 种，**所有可能的字符对 (x, y) 只有 26×26 = 676 种**，这在计算上完全可以接受。我们只需要枚举这 676 种「把字符 x 从 word1 换到 word2、把字符 y 从 word2 换到 word1」的情况，并判断是否会使两段字符串的不同字符数相等。

> **步骤**  
> 1. 统计 `cnt1`、`cnt2`（各 26 长度的列表），并记录原始的不同字符数 `diff1`、`diff2`。  
> 2. 对每一对字符 `(x, y)`（`0~25`），如果 `cnt1[x] == 0` 且 `cnt2[y] == 0`，说明这两个字符在各自的字符串里根本不存在，交换没有意义，直接跳过。  
> 3. 计算交换后 `diff1'`、`diff2'`：  
>    - **对 word1**：  
>        - 如果 `cnt1[x] == 1`（交换后 x 消失），`diff1' = diff1 - 1`；  
>        - 如果 `cnt1[y] == 0`（交换后 y 第一次出现），`diff1' = diff1 + 1`；  
>        - 其余情况不影响 `diff1`。  
>    - **对 word2** 同理，只是把 `x`、`y` 的角色换一下。  
> 4. 检查 `diff1' == diff2'`，若成立则返回 `True`。  
> 5. 循环结束仍未找到则返回 `False`。

> **为什么只检查 676 种情况就够了？**  
> 因为交换的结果只和被换出的字符种类有关，而不和它们在字符串中的具体位置有关。只要字符种类相同，任意位置的交换产生的计数变化完全相同。

#### 代码（Python）

```python
def isItPossible(word1: str, word2: str) -> bool:
    # 1️⃣ 统计每个字符出现的次数（长度为 26 的数组）
    cnt1 = [0] * 26          # word1 中每个字母的频率
    cnt2 = [0] * 26          # word2 中每个字母的频率

    for ch in word1:
        cnt1[ord(ch) - ord('a')] += 1
    for ch in word2:
        cnt2[ord(ch) - ord('a')] += 1

    # 2️⃣ 计算原始的不同字符种类数
    diff1 = sum(1 for c in cnt1 if c > 0)   # word1 里不同字符的个数
    diff2 = sum(1 for c in cnt2 if c > 0)   # word2 里不同字符的个数

    # 3️⃣ 枚举所有可能的字符对 (x, y)
    for x in range(26):          # x 表示想从 word1 换出去的字符
        for y in range(26):      # y 表示想从 word2 换进去的字符
            if cnt1[x] == 0 and cnt2[y] == 0:
                # 两边都没有这个字符，换来换去没有任何影响，直接跳过
                continue

            # ---------- 计算交换后 word1 的不同字符数 ----------
            new_diff1 = diff1
            # 交换后 x 可能会消失
            if cnt1[x] == 1:          # 原来只出现一次，换走后就没有了
                new_diff1 -= 1
            # 交换后 y 可能会首次出现
            if cnt1[y] == 0:          # 原来 word1 没有 y，换进来后出现
                new_diff1 += 1

            # ---------- 计算交换后 word2 的不同字符数 ----------
            new_diff2 = diff2
            # 交换后 y 可能会消失
            if cnt2[y] == 1:
                new_diff2 -= 1
            # 交换后 x 可能会首次出现
            if cnt2[x] == 0:
                new_diff2 += 1

            # ---------- 检查是否相等 ----------
            if new_diff1 == new_diff2:
                return True

    # 没有任何一次交换可以使两边不同字符数相等
    return False
```

> **关键行中文解释**  
> - `ord(ch) - ord('a')`：把字符 `'a'~'z'` 映射到数组下标 `0~25`。  
> - `sum(1 for c in cnt1 if c > 0)`：统计频率数组里大于 0 的位置个数，即不同字符的种类数。  
> - `if cnt1[x] == 1: new_diff1 -= 1`：如果 `x` 在 `word1` 中只出现一次，换走后 `word1` 失去一种字符。  
> - `if cnt1[y] == 0: new_diff1 += 1`：如果 `y` 原本不在 `word1`，换进来后多出一种字符。  

#### 复杂度  

- **时间复杂度**：`O(26 × 26 + n + m) ≈ O(n + m)`  
  - 统计频率数组遍历两遍字符串，需要 `O(n + m)`。  
  - 枚举字符对最多 676 次，常数级别，可视作 `O(1)`。  
  - 与暴力解相比，省掉了 `n·m` 那么大的循环，真正跑得动。

- **空间复杂度**：`O(1)`（常数空间）  
  - 只用了两个长度为 26 的整数数组和若干常量变量，和输入规模无关。

---

## 心得

- **核心技巧**：用**字符频率数组（相当于 26 格的哈希表）**把「是否出现」转化为「计数是否为 0」；再利用**计数增减对不同字符种类数的影响**，在常数时间内模拟一次交换的效果。  
- **适用的题型**  
  1. 需要比较两段字符串「不同字符数量」的题目（如 *“两个字符串的异或字符数”*）。  
  2. 只允许一次或有限次数的字符/元素交换，且交换后只关心「出现次数」而不是顺序（如 *“交换一次使两个数组的不同元素数相等”*）。  
- **一句话总结解题钥匙**：**把「字符是否出现」抽象成「计数是否为 0」，然后枚举所有可能的字符对，用计数的增减直接判断结果**。

---

## 反思

- **第一反应**：看到「交换」和「不同字符数」立刻想到遍历所有下标直接模拟——这就是暴力思路。  
- **最容易踩的坑**  
  1. **忽略字符本身不存在的情况**：如果某字符在两段字符串里都为 0，交换不会改变任何计数，必须跳过，否则会产生错误的相等判断。  
  2. **计数增减的细节**：只有当某字符的出现次数从 1 变成 0（消失）或从 0 变成 1（首次出现）时，才会影响「不同字符的种类数」。遗漏这一步会导致错误的 `new_diff` 计算。  
  3. **边界条件**：字符串长度可能只有 1，仍需正常工作；字符相同的交换（`x == y`）也要考虑，它实际上不会改变任何计数，除非两边都只有这一个字符。  

- **下次遇到同类题的第一步**：**先统计每个字符的出现次数**，把「不同字符的种类」转化为「非零计数的数量」，再思考一次操作会怎样影响这些计数，从而在 **O(1)** 时间内评估每一种可能的操作。这样就能快速从暴力枚举跳到常数时间的优化。