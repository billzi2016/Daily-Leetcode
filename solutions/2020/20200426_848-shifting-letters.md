# #848. 字母移位 / Shifting Letters

> 难度：中等 · 标签：Array、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/shifting-letters/)

---

## 题目（英文原版）

**Description**

You are given a string s of lowercase English letters and an integer array shifts of the same length.
Call the shift() of a letter, the next letter in the alphabet, (wrapping around so that 'z' becomes 'a').
Now for each shifts[i] = x, we want to shift the first i + 1 letters of s, x times.
Return the final string after all such shifts to s are applied.

**Examples**

**Example 1:**

```
Input: s = "abc", shifts = [3,5,9]
Output: "rpl"
Explanation: We start with "abc".
After shifting the first 1 letters of s by 3, we have "dbc".
After shifting the first 2 letters of s by 5, we have "igc".
After shifting the first 3 letters of s by 9, we have "rpl", the answer.
```

**Example 2:**

```
Input: s = "aaa", shifts = [1,2,3]
Output: "gfd"
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.
- shifts.length == s.length
- 0 <= shifts[i] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个只包含小写英文字母的字符串 `s` 和一个整数数组 `shifts`（长度与 `s` 相同）。  
称字母的 `shift()` 为字母表中的下一个字母（循环，即 `'z'` 变为 `'a'`）。  
现在对于每个 `shifts[i] = x`，我们要将 `s` 的前 `i + 1` 个字母各向后移动 `x` 次。  
返回对 `s` 应用所有此类移位操作后的最终字符串。

**示例**

示例 1:  
输入: `s = "abc", shifts = [3,5,9]`  
输出: `"rpl"`  
解释: 我们从 `"abc"` 开始。  
- 将前 1 个字母移动 3 次后得到 `"dbc"`。  
- 将前 2 个字母移动 5 次后得到 `"igc"`。  
- 将前 3 个字母移动 9 次后得到 `"rpl"`，即答案。

示例 2:  
输入: `s = "aaa", shifts = [1,2,3]`  
输出: `"gfd"`

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成。  
- `shifts.length == s.length`  
- `0 <= shifts[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**逐个执行题目描述的操作**：

1. 从左到右遍历 `shifts`，第 `i` 次需要把字符串 `s` 的前 `i+1` 个字符都向后移动 `shifts[i]` 步。  
2. “向后移动”可以把字符当成字母表的下标（`a → 0, b → 1, …, z → 25`），加上移动步数后再对 26 取模得到新的字母。  

这里用到的唯一“数据结构”是**列表（list）**，因为字符串在 Python 中是不可变的，必须把它转成列表才能逐个修改。可以把它想象成一排 **可随意替换的信封**，每个信封里放一个字母。

**为什么一定能得到正确答案**  
- 每一次循环都完整地模拟了题目要求的“把前 `i+1` 个字母整体移动 `shifts[i]` 次”。  
- 所有 `i` 都遍历完后，所有规定的移动都已经执行，自然得到最终的字符串。

**时间/空间复杂度**  
- 外层遍历 `n` 次（`n = len(s)`），第 `i` 次内部要把前 `i+1` 个字符都重新计算一次，最坏情况是 `1 + 2 + … + n = n·(n+1)/2` 次操作 → **O(n²)**。  
  大白话：如果 `n=10⁴`，大约要做 5 × 10⁷ 次字符转换，跑起来会明显慢。  
- 只用了原来的字符列表和常数个额外变量 → **O(n)** 的空间（保存结果的列表本身必须要有）。

#### 代码（Python）  

```python
def shiftingLetters_bruteforce(s: str, shifts: list[int]) -> str:
    # 把字符串转成列表，方便原地修改
    chars = list(s)                     # ['a', 'b', 'c', ...]
    n = len(chars)

    for i in range(n):                  # 第 i 次操作，i 从 0 开始
        shift = shifts[i] % 26          # 只需要保留 0~25 之间的步数
        # 把前 i+1 个字符都向后移动 shift 步
        for j in range(i + 1):          # j = 0 … i
            # 当前字符的字母序号（0~25），加上 shift 后再取模得到新字母
            new_ord = (ord(chars[j]) - ord('a') + shift) % 26
            chars[j] = chr(new_ord + ord('a'))   # 把数字再转回字符

    return ''.join(chars)                # 把列表拼成字符串返回
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层 `n` 次，内层平均也要遍历约 `n/2` 次，乘起来就是 `n²/2`，量级就是 `O(n²)`。  
- **空间复杂度**：`O(n)`  
  - 解释：我们需要一个和原字符串等长的列表来存放结果，除此之外只用了常数个变量。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈在于每次都要遍历前缀**。如果能一次性算出每个位置最终要移动多少步，就不必重复工作。

观察题目：  
- 第 `i` 次操作会把 **前 `i+1`** 个字符都向后移动 `shifts[i]` 步。  
- 那么字符 `s[k]`（下标 `k`）会被 **所有 `i ≥ k`** 的操作影响。换句话说，它最终的移动步数是 `shifts[k] + shifts[k+1] + … + shifts[n‑1]`（从自己所在位置一直到最后的所有 shift 的和）。  

这正好是**后缀和（suffix sum）**的概念。我们可以从右往左一次遍历，把累计的移动步数保存在一个变量 `cur` 中：

```
cur = 0
for i from n-1 downto 0:
    cur = (cur + shifts[i]) % 26   # 只保留 0~25，防止数字爆炸
    shift s[i] by cur steps
```

这里的 **% 26** 就像是把字母表当成一个 **环形跑道**，跑到终点再回到起点。

**为什么这样就对了**  
- 当我们从右往左走到位置 `i` 时，`cur` 已经累计了 `shifts[i] … shifts[n‑1]`，正是字符 `s[i]` 需要的总移动步数。  
- 对每个字符只做一次转换，所有的前缀操作自然都被“一次性”算进来了。

**核心数据结构**：只用了**一个整数 `cur`**和**字符列表**。不需要额外的数组来存前缀或后缀和，空间几乎为 **O(1)**（不计结果本身）。

#### 代码（Python）  

```python
def shiftingLetters_optimal(s: str, shifts: list[int]) -> str:
    # 把字符串转成列表，方便原地修改
    chars = list(s)
    n = len(chars)

    cur = 0                     # 累计的总移动步数（模 26）
    for i in range(n - 1, -1, -1):   # 从右往左遍历
        # 把当前的 shifts[i] 加入累计，总步数只保留 0~25
        cur = (cur + shifts[i]) % 26

        # 对字符 chars[i] 做一次整体移动
        new_ord = (ord(chars[i]) - ord('a') + cur) % 26
        chars[i] = chr(new_ord + ord('a'))

    return ''.join(chars)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串和一次 shifts，线性时间。相比暴力的 `O(n²)`，大幅提升。  
- **空间复杂度**：`O(1)`（不计输出字符串）  
  - 只用了一个整数 `cur` 和若干常数变量，额外空间几乎为常数。

---  

## 心得  

- **核心技巧**：利用**后缀和 + 取模**一次性算出每个字符的累计移动次数。  
- **相同思路可用的题型**  
  1. **“Range Addition”** 系列题目（如 LeetCode 370. Range Addition）——需要对区间做累计更新时可以用差分数组。  
  2. **“Prefix Sum of Rotations”**（如 1845. 序列转化）——需要把每个位置的累计效果一次性算出。  
- **一句话总结解题钥匙**：**把所有“重复的前缀操作”合并为每个位置的“后缀总和”，一次遍历完成**。  

---  

## 反思  

- **第一反应**：看到“把前 i+1 个字母都移动”就想到双层循环，直接模拟。  
- **最容易踩的坑**  
  - **取模忘记**：`shifts[i]` 可达 `10⁹`，直接相加会导致整数非常大，甚至超出语言的整数范围（Python 不会溢出，但会拖慢）。一定要在累计时 ` % 26`。  
  - **字符转数字的偏移**：`ord('a')` 必须减去再加回去，别忘了把 `'a'` 当作基准。  
  - **空字符串或单字符**：虽然约束 `len(s) ≥ 1`，但实现时仍要确保循环边界不会出错。  
- **下次类似题的第一步**：先思考**“每个元素到底会被多少次操作影响？”**，若是“前缀/后缀累计”，就立刻考虑 **前缀和 / 后缀和**（或差分数组）来把重复工作合并。