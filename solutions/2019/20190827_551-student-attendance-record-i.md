# #551. 学生出勤记录 I / Student Attendance Record I

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/student-attendance-record-i/)

---

## 题目（英文原版）

**Description**

You are given a string s representing an attendance record for a student where each character signifies whether the student was absent, late, or present on that day. The record only contains the following three characters:
The student is eligible for an attendance award if they meet both of the following criteria:
Return true if the student is eligible for an attendance award, or false otherwise.

**Examples**

**Example 1:**

```
Input: s = "PPALLP"
Output: true
Explanation: The student has fewer than 2 absences and was never late 3 or more consecutive days.
```

**Example 2:**

```
Input: s = "PPALLL"
Output: false
Explanation: The student was late 3 consecutive days in the last 3 days, so is not eligible for the award.
```

**Constraints**

- 1 <= s.length <= 1000
- s[i] is either 'A', 'L', or 'P'.

---

## 题目（中文翻译）

你得到一个字符串 `s`，它表示一名学生的出勤记录，其中每个字符对应学生当天是缺席（Absent，`A`）、迟到（Late，`L`）还是出勤（Present，`P`）。记录仅包含这三种字符。

该学生只有在同时满足以下两个条件时才有资格获得出勤奖励（attendance award）：

1. 缺席（`A`）的次数少于 **2** 次。  
2. 没有出现连续 **3** 天或以上迟到（`L`）的情况。

返回 `true` 表示该学生符合奖励条件，返回 `false` 表示不符合。

**示例 1**  

**输入**: `s = "PPALLP"`  
**输出**: `true`  
**解释**: 学生的缺席次数少于 2 次，并且从未出现连续 3 天迟到的情况。

**示例 2**  

**输入**: `s = "PPALLL"`  
**输出**: `false`  
**解释**: 学生在最后的 3 天连续迟到，因此不符合奖励条件。

**约束条件**  

- `1 <= s.length <= 1000`  
- `s[i]` 只能是 `'A'`、`'L'` 或 `'P'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把题目要检查的两个规则分别写出来**，然后把字符串 `s` 从头到尾跑一遍：

1. **缺勤次数**  
   - 统计字符 `'A'` 出现了几次。  
   - 如果次数 > 1，则不符合“至多一次缺勤”的要求，直接返回 `False`。  
   - 这里的统计可以想象成在一本 **计数本** 上记录每次看到 `'A'` 时在本子上划一划。

2. **连续迟到次数**  
   - 在同一次遍历中，用一个计数器记录当前连续出现的 `'L'` 的个数。  
   - 每看到 `'L'` 就 `cnt += 1`，否则（遇到 `'P'` 或 `'A'`）就把计数器归零。  
   - 一旦计数器达到 3，说明出现了 “连续三天迟到”，立即返回 `False`。  
   - 这个计数器可以类比为 **连续闹钟响的次数**，一旦闹钟连续响了三次，就认为太迟了。

只要遍历结束都没有触发 “缺勤超过一次” 或 “连续迟到三次”，说明符合两个条件，返回 `True`。

> 为什么这个方法一定对？  
> 因为我们 **完整地检查了所有可能导致不合格的情况**：所有 `'A'` 的出现次数和所有长度为 3 的 `'L'` 子串。只要其中任意一个出现，答案必定是 `False`；否则必定是 `True`。

#### 代码（Python）

```python
def checkRecord(s: str) -> bool:
    # 统计缺勤次数
    absent_cnt = 0          # 用来记录 'A' 出现的次数
    late_streak = 0         # 用来记录当前连续的 'L' 数量

    for ch in s:            # 从左到右遍历每一个字符
        if ch == 'A':
            absent_cnt += 1            # 缺勤 +1
            if absent_cnt > 1:         # 超过一次缺勤，直接返回 False
                return False
            late_streak = 0            # 一旦出现 'A'，连续迟到计数器要清零
        elif ch == 'L':
            late_streak += 1           # 连续迟到计数 +1
            if late_streak >= 3:       # 连续三天迟到，直接返回 False
                return False
        else:  # ch == 'P'
            late_streak = 0            # 出现出勤，连续迟到计数器归零

    # 循环结束都没有触发不合格条件，说明符合要求
    return True
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  这里的 `n` 是字符串长度。我们只遍历了一遍，每个字符做了常数次操作。  
  “O(n)” 可以理解为“随着学生上课天数的增加，检查的时间会线性增长”，比如 10 天需要 10 步，100 天需要 100 步。

- **空间复杂度：** `O(1)`  
  只用了几个整数变量 (`absent_cnt`、`late_streak`)，不随 `n` 增长而增加。  
  用大白话说，就是“几乎不占额外空间”。

---

### 2. 最优解

#### 思路  

虽然上面的“暴力”解已经是 `O(n)`，但我们可以把 **两次检查合并成一次遍历**，并且在遍历过程中**提前结束**（一旦发现不合格就立刻返回），这就是最优的实现方式。

从暴力解出发，我们注意到：

- 计数缺勤次数和计数连续迟到次数 **本来就可以在同一次循环里完成**，不需要额外的遍历。  
- 当任意一次检查失败时（缺勤 > 1 或 连续迟到 ≥ 3），后面的字符已经不可能把结果改好，所以可以 **立即返回**，不必继续遍历。

核心技巧只有两个：  
1. **单次遍历**（一次走完所有字符）。  
2. **早停**（一旦不满足条件就直接结束）。

这两个技巧在很多字符串或数组题目里都非常常用，尤其是 “只要出现一次不合法就直接否定” 的场景。

#### 代码（Python）

```python
def checkRecord(s: str) -> bool:
    absent = 0      # 已出现的缺勤次数
    late = 0        # 当前连续迟到的天数

    for ch in s:
        if ch == 'A':
            absent += 1
            if absent > 1:          # 已经出现第二次缺勤，直接否定
                return False
            late = 0                # 缺勤打断连续迟到计数
        elif ch == 'L':
            late += 1
            if late >= 3:           # 连续三天迟到，直接否定
                return False
        else:  # ch == 'P'
            late = 0                # 出勤也会打断迟到计数

    # 循环结束仍未触发否定，说明符合所有条件
    return True
```

> **关键点说明**  
> - `late = 0` 的位置很重要：只要出现 `'A'` 或 `'P'`，连续迟到计数都必须归零，因为这两天打断了 “连续迟到”。  
> - `return False` 出现在循环内部，意味着**只要发现问题就立刻停**，不必等遍历完所有字符。

#### 复杂度

- **时间复杂度：** `O(n)`，但因为加入了 **早停**，实际运行时间往往比完整遍历更快。  
  比喻：如果学生在第 5 天就已经缺勤两次，程序只会跑 5 步，而不是跑完整个 1000 天的记录。

- **空间复杂度：** `O(1)`，仍然只使用了常数个变量。

---

## 心得

- **核心技巧**：一次遍历 + 早停。  
- **适用的题型**：  
  1. “只要出现一次不合法就直接返回”的字符串或数组检查（如合法密码、合法括号序列等）。  
  2. “计数 + 连续计数” 类问题（如判断是否有超过 K 次重复字符、是否出现连续 N 次相同操作）。  
- **一句话总结**：**“遍历时同步维护所有必要的计数，一旦任何计数突破限制就立刻返回”。**

---

## 反思

- **第一反应**：先把题目拆成两个独立的检查——缺勤次数和连续迟到天数，然后分别实现。  
- **最容易踩的坑**：  
  - 忘记在出现 `'A'` 或 `'P'` 时把 `late` 计数清零，导致错误地把不相邻的 `'L'` 误判为连续。  
  - 没有考虑字符串只有 `'A'` 或 `'L'` 的极端情况（长度为 1），但上述实现已经兼容。  
- **下次遇到同类题**：第一步就想 “**是否可以在一次遍历中同时完成所有检查，并在发现违背时立即返回**”。这样既简洁又高效。