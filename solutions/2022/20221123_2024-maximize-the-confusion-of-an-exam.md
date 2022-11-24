# #2024. 最大化考试的混淆程度 / Maximize the Confusion of an Exam

> 难度：中等 · 标签：String、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/)

---

## 题目（英文原版）

**Description**

A teacher is writing a test with n true/false questions, with 'T' denoting true and 'F' denoting false. He wants to confuse the students by maximizing the number of consecutive questions with the same answer (multiple trues or multiple falses in a row).
You are given a string answerKey, where answerKey[i] is the original answer to the ith question. In addition, you are given an integer k, the maximum number of times you may perform the following operation:
Return the maximum number of consecutive 'T's or 'F's in the answer key after performing the operation at most k times.

**Examples**

**Example 1:**

```
Input: answerKey = "TTFF", k = 2
Output: 4
Explanation: We can replace both the 'F's with 'T's to make answerKey = "TTTT".
There are four consecutive 'T's.
```

**Example 2:**

```
Input: answerKey = "TFFT", k = 1
Output: 3
Explanation: We can replace the first 'T' with an 'F' to make answerKey = "FFFT".
Alternatively, we can replace the second 'T' with an 'F' to make answerKey = "TFFF".
In both cases, there are three consecutive 'F's.
```

**Example 3:**

```
Input: answerKey = "TTFTTFTT", k = 1
Output: 5
Explanation: We can replace the first 'F' to make answerKey = "TTTTTFTT"
Alternatively, we can replace the second 'F' to make answerKey = "TTFTTTTT". 
In both cases, there are five consecutive 'T's.
```

**Constraints**

- n == answerKey.length
- 1 <= n <= 5 * 104
- answerKey[i] is either 'T' or 'F'
- 1 <= k <= n

---

## 题目（中文翻译）

**题目描述**  
一位老师正在出一份包含 `n` 道判断题（True/False）的试卷，其中 `'T'` 表示正确，`'F'` 表示错误。老师希望通过让相同答案连续出现的次数尽可能多来“混淆”学生，即让多个 `'T'` 或多个 `'F'` 连续出现。

给定一个字符串 `answerKey`，其中 `answerKey[i]` 是第 `i` 题的原始答案。此外，还给定一个整数 `k`，表示最多可以执行以下操作的次数：

- 将任意一个字符 `'T'` 改为 `'F'`，或将 `'F'` 改为 `'T'`。

求在至多执行 `k` 次操作后，`answerKey` 中出现的最长连续 `'T'` 或 `'F'` 的长度。

---

**示例**

**示例 1**  
```
Input: answerKey = "TTFF", k = 2
Output: 4
Explanation: 我们可以把两个 `'F'` 都替换成 `'T'`，得到 answerKey = "TTTT"。此时出现了四个连续的 `'T'`。
```

**示例 2**  
```
Input: answerKey = "TFFT", k = 1
Output: 3
Explanation: 我们可以把第一个 `'T'` 替换成 `'F'`，得到 answerKey = "FFFT"。  
或者把第二个 `'T'` 替换成 `'F'`，得到 answerKey = "TFFF"。  
无论哪种方式，都会出现三个连续的 `'F'`。
```

**示例 3**  
```
Input: answerKey = "TTFTTFTT", k = 1
Output: 5
Explanation: 我们可以把第一个 `'F'` 替换成 `'T'`，得到 answerKey = "TTTTTFTT"。  
或者把第二个 `'F'` 替换成 `'T'`，得到 answerKey = "TTFTTTTT"。  
这两种情况下，最长的连续 `'T'` 长度都是 5。
```

---

**约束条件**  

- `n == answerKey.length`
- `1 <= n <= 5 * 10^4`
- `answerKey[i]` 仅为 `'T'` 或 `'F'`
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的修改方式**，把至多 `k` 个字符改成想要的 `'T'` 或 `'F'`，然后统计最长的相同字符连续段。  
实现上可以这样做：

1. 先决定我们要把连续段统一成 `'T'` 还是 `'F'`（两种情况都要算一次）。  
2. 对于每一个起始下标 `i`，尝试向右扩展到下标 `j`（`j ≥ i`），在这个区间里统计与目标字符不同的个数 `cnt`。  
3. 只要 `cnt ≤ k`，说明我们可以把这段区间全部改成目标字符，记录 `j-i+1` 作为候选答案。  
4. 当 `cnt > k` 时，说明已经超出允许的修改次数，停止向右扩展，继续从下一个起始位置 `i+1` 进行同样的尝试。

这里的 **数据结构** 只需要一个普通的字符串和几个整数计数器。可以把「计数不同字符的次数」想象成「查字典」：我们在字典里找某个单词（这里是字符），如果不匹配就记一次「需要改」的次数。

**为什么正确**：  
- 我们穷举了所有可能的起点 `i` 和终点 `j`，只要这段区间在 `k` 次修改范围内，就一定能被改成全 `'T'`（或全 `'F'`），所以最长合法区间一定会在我们的枚举中出现。

**时间/空间复杂度**  
- 外层遍历所有起点 `i`（`n` 次），内层最坏情况下要遍历到字符串末尾（最多 `n` 次），于是总操作次数是 `n × n = n²`。  
- 空间只用了常数个变量 `O(1)`。

> **大白话解释**：`O(n²)` 就好比在一张 10 000×10 000 的棋盘上逐格检查，每格都要走遍整条对角线，显然会很慢。

#### 代码（Python）

```python
def maxConsecutive_bruteforce(answerKey: str, k: int) -> int:
    n = len(answerKey)
    best = 0

    # 两种目标字符分别计算
    for target in ('T', 'F'):
        # i 为区间左端点
        for i in range(n):
            diff = 0          # 区间内与 target 不同的字符个数
            # j 为区间右端点，不断右移
            for j in range(i, n):
                if answerKey[j] != target:
                    diff += 1          # 需要一次修改
                if diff > k:          # 超出 k 次，停止扩展
                    break
                # 此时区间 [i, j] 合法，更新答案
                best = max(best, j - i + 1)

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要两层循环，最坏情况每次都遍历到字符串末尾。  
- **空间复杂度**：`O(1)` —— 只用了常数个计数器。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **「每次都从头统计不同字符的次数」**，这导致大量重复工作。  
实际上，当我们把左端点 `i` 向右移动一格时，区间内的不同字符计数只会 **减去** `answerKey[i]`（如果它本来就不等于目标字符）。这提示我们可以用 **滑动窗口（双指针）** 来维护一个“合法窗口”，让左、右指针只各自向右走一遍。

**核心思想**：  
- 维护一个窗口 `[left, right]`，窗口内 **至多** 包含 `k` 个不是目标字符的位子。  
- 当窗口合法时，窗口长度 `right - left + 1` 就是一次可能的答案。  
- 当窗口非法（不同字符数 > k）时，左指针 `left` 右移，直到窗口重新合法。  
- 对目标字符 `'T'` 与 `'F'` 分别运行一次，取最大值。

**为什么正确**：  
- 任何合法的最长相同字符子串，都可以在一次遍历中被窗口恰好覆盖，因为窗口的定义正是「包含至多 k 个需要改的字符」。  
- 当窗口非法时，左指针的收缩保证我们不会错过更长的合法窗口，因为左端点一定是导致非法的那个字符所在位置。

**数据结构解释**：  
- **双指针**：把窗口的左、右端点想象成两个人在跑道上跑，右指针负责「往前跑」扩展窗口，左指针负责「追上」并收缩窗口。  
- **计数器 `flips`**：记录窗口内需要翻转的字符数，相当于「背包里还有几块可以用的翻转卡」。

#### 代码（Python）

```python
def maxConsecutive_opt(answerKey: str, k: int) -> int:
    """使用滑动窗口，时间 O(n)，空间 O(1)"""
    n = len(answerKey)

    def max_len(target: str) -> int:
        left = 0          # 窗口左端
        flips = 0         # 窗口内需要翻转的字符数
        best = 0

        for right in range(n):                     # 右端不断右移
            if answerKey[right] != target:         # 需要一次翻转
                flips += 1

            # 若翻转次数超过 k，收缩左端
            while flips > k:
                if answerKey[left] != target:
                    flips -= 1
                left += 1

            # 此时窗口合法，更新答案
            best = max(best, right - left + 1)
        return best

    # 分别以 T 为目标、F 为目标，取更大的结果
    return max(max_len('T'), max_len('F'))
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 左右指针各只遍历一次，所有操作都是常数时间。相比暴力的 `O(n²)`，快了好几百倍。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不随输入规模增长。

---

## 心得

- **核心技巧**：**滑动窗口（双指针）** 用来维护「至多 k 次翻转」的合法区间。  
- **适用的题型**：  
  1. “最长子数组/子串满足 ≤ k 次某种操作”——如 *Longest Substring with At Most K Distinct Characters*。  
  2. “最长连续 1（或 0）的子数组，最多翻转 k 个 0（或 1）”——如 *Maximum Consecutive Ones III*。  
  3. “最小子数组长度，使得和 ≥ target，且可移动窗口”——如 *Minimum Size Subarray Sum*。  
- **一句话总结**：**把「最多 k 次修改」转化为「窗口内违背目标的字符数 ≤ k」，用滑动窗口一次遍历即可找出最长合法长度。**

---

## 反思

- **第一反应**：看到“最多可以改 k 次”，自然想到“枚举所有改动”——于是想到暴力枚举所有子串。  
- **最容易踩的坑**：  
  - 忘记分别以 `'T'` 和 `'F'` 为目标字符，直接只算一种会漏掉另一种更长的情况。  
  - 在收缩窗口时，没有正确地把左端点对应的字符是否需要翻转的计数减掉，导致 `flips` 计数错误。  
- **下次遇到同类题**：第一步就要想到 **“把限制转化为窗口内的计数”**，用双指针维护一个合法窗口，再在窗口合法时更新答案。这样可以立刻把时间复杂度从二次降到线性。