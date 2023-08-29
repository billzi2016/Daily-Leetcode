# #2381. 字母移位 II / Shifting Letters II

> 难度：中等 · 标签：Array、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/shifting-letters-ii/)

---

## 题目（英文原版）

**Description**

You are given a string s of lowercase English letters and a 2D integer array shifts where shifts[i] = [starti, endi, directioni]. For every i, shift the characters in s from the index starti to the index endi (inclusive) forward if directioni = 1, or shift the characters backward if directioni = 0.
Shifting a character forward means replacing it with the next letter in the alphabet (wrapping around so that 'z' becomes 'a'). Similarly, shifting a character backward means replacing it with the previous letter in the alphabet (wrapping around so that 'a' becomes 'z').
Return the final string after all such shifts to s are applied.

**Examples**

**Example 1:**

```
Input: s = "abc", shifts = [[0,1,0],[1,2,1],[0,2,1]]
Output: "ace"
Explanation: Firstly, shift the characters from index 0 to index 1 backward. Now s = "zac".
Secondly, shift the characters from index 1 to index 2 forward. Now s = "zbd".
Finally, shift the characters from index 0 to index 2 forward. Now s = "ace".
```

**Example 2:**

```
Input: s = "dztz", shifts = [[0,0,0],[1,1,1]]
Output: "catz"
Explanation: Firstly, shift the characters from index 0 to index 0 backward. Now s = "cztz".
Finally, shift the characters from index 1 to index 1 forward. Now s = "catz".
```

**Constraints**

- 1 <= s.length, shifts.length <= 5 * 104
- shifts[i].length == 3
- 0 <= starti <= endi < s.length
- 0 <= directioni <= 1
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s`，以及一个二维整数数组 `shifts`，其中 `shifts[i] = [start_i, end_i, direction_i]`。对于每个 `i`，将 `s` 中下标从 `start_i` 到 `end_i`（**包括**）的字符进行移位：

- 若 `direction_i = 1`，则向前移位（forward），即用字母表中的下一个字母替换该字符，`'z'` 会循环回 `'a'`。
- 若 `direction_i = 0`，则向后移位（backward），即用字母表中的前一个字母替换该字符，`'a'` 会循环回 `'z'`。

在对所有的移位操作依次执行完毕后，返回最终得到的字符串 `s`。

## 示例

### 示例 1  
**输入**  
```text
s = "abc", shifts = [[0,1,0],[1,2,1],[0,2,1]]
```
**输出**  
```text
"ace"
```
**解释**  
1. 首先，对下标 `0` 到 `1` 的字符向后移位。此时 `s = "zac"`。  
2. 其次，对下标 `1` 到 `2` 的字符向前移位。此时 `s = "zbd"`。  
3. 最后，对下标 `0` 到 `2` 的字符向前移位。此时 `s = "ace"`。

### 示例 2  
**输入**  
```text
s = "dztz", shifts = [[0,0,0],[1,1,1]]
```
**输出**  
```text
"catz"
```
**解释**  
1. 首先，对下标 `0` 到 `0` 的字符向后移位。此时 `s = "cztz"`。  
2. 最后，对下标 `1` 到 `1` 的字符向前移位。此时 `s = "catz"`。

## 约束条件

- `1 <= s.length, shifts.length <= 5 * 10^4`
- `shifts[i].length == 3`
- `0 <= start_i <= end_i < s.length`
- `0 <= direction_i <= 1`
- `s` 只由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**一次遍历每个 `shifts[i]`，把区间 `[starti, endi]` 内的字符都向前或向后移动一次**。  
- **数据结构**：我们只需要把字符串 `s` 转成字符列表（list），因为 Python 的字符串是不可变的，列表可以原地修改。  
- **生活化类比**：把字符串想成一排排的信箱，每个信箱里放着一个字母。`shifts[i]` 就是派一只小邮递员去把 **连续** 的几封信（区间）往前或往后“搬家”。  
- **为什么正确**：因为题目要求对每条指令都要完整执行一次，暴力遍历正好把每条指令都落实到每个字符上，最终得到的字符正是题目要求的结果。

#### 代码（Python）

```python
def shiftingLetters_bruteforce(s: str, shifts: list[list[int]]) -> str:
    # 把字符串转成列表，方便原地修改
    chars = list(s)

    for start, end, direction in shifts:
        # direction == 1 表示向前，0 表示向后
        delta = 1 if direction == 1 else -1

        # 对区间 [start, end] 的每个字符都移动一次
        for i in range(start, end + 1):
            # 先把字符转成 0~25 的数字（'a' -> 0, 'b' -> 1, ...）
            num = ord(chars[i]) - ord('a')
            # 加上 delta 并取模 26，保证循环到 a~z
            num = (num + delta) % 26
            # 再转回字符
            chars[i] = chr(num + ord('a'))

    # 把列表拼成字符串返回
    return ''.join(chars)
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`，其中 `m = len(shifts)`，`n = len(s)`。  
  - 大白话：如果有 10 条指令，每条指令要改动整条字符串（长度 100），我们大概要做 10 × 100 = 1000 次“搬家”。  
- **空间复杂度**：`O(n)`，用来存放字符列表。  
  - 只比原始字符串多占了一份相同大小的空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每条指令都要遍历一次区间**，当 `shifts` 很多且区间很大时会导致大量重复工作。  
我们可以把 **“把每个字符要移动多少次”** 这件事提前算好，只遍历一次字符列表即可得到最终结果。实现思路如下：

1. **把每条指令转成“差分数组”**  
   - 把 `direction = 1` 当作 **+1**，`direction = 0` 当作 **-1**（向前是正，向后是负）。  
   - 用一个长度为 `n+1` 的整数数组 `diff`（类似于记账本），在 `start` 位置加上 `delta`，在 `end+1` 位置减去 `delta`。  
   - 这样做的意义相当于：在 `start` 之后所有字符都要累计这个 `delta`，但在 `end+1` 之后要把它抵消掉。

2. **前缀和（Prefix Sum）**  
   - 对 `diff` 进行一次前缀求和，得到 `shift[i]` ——字符 `i` 最终需要向前（正）或向后（负）移动的总次数。  
   - 前缀和的过程就像把记账本里每天的收支累加，得到每一天的余额。

3. **一次遍历字符串，直接把字符按累计的位移改成最终字符**  
   - 对每个字符 `c`，先算出它在字母表中的下标 `0~25`，再加上 `shift[i]`，取模 26，得到最终字母。

**类比**：想象有一条路上有很多灯泡，每次指令是把从 `start` 到 `end` 区间的灯泡调亮（+1）或调暗（-1）。如果每次都去逐个调，那很费事。我们可以在 `start` 前放一个“开关”，在 `end+1` 前放一个“关掉的开关”。最后走一遍路，随时根据开关的状态决定灯泡亮多少。

#### 代码（Python）

```python
def shiftingLetters_optimal(s: str, shifts: list[list[int]]) -> str:
    n = len(s)
    # 1. 差分数组，长度比原字符串多 1，防止越界
    diff = [0] * (n + 1)

    # 2. 把每条指令转成差分标记
    for start, end, direction in shifts:
        delta = 1 if direction == 1 else -1      # 前进记 +1，后退记 -1
        diff[start] += delta                     # 区间起点加 delta
        diff[end + 1] -= delta                   # 区间终点的下一个位置减 delta

    # 3. 前缀和得到每个字符的累计位移
    shift = [0] * n          # shift[i] 表示第 i 个字符最终需要移动多少位
    cur = 0
    for i in range(n):
        cur += diff[i]        # 累计到当前位置的总位移
        shift[i] = cur

    # 4. 根据累计位移一次性生成结果字符串
    res = []
    for i, ch in enumerate(s):
        # 把字符转成 0~25 的整数
        base = ord(ch) - ord('a')
        # 加上累计位移后取模 26，得到最终字符下标
        new_idx = (base + shift[i]) % 26
        # 再转回字符并加入结果列表
        res.append(chr(new_idx + ord('a')))

    return ''.join(res)
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`，其中 `n = len(s)`，`m = len(shifts)`。  
  - 只遍历一次 `shifts`（做差分标记）和一次 `s`（前缀和 + 最终转换），没有嵌套循环。  
  - 与暴力解的 `O(m·n)` 相比，大幅降低了运算量。  
- **空间复杂度**：`O(n)`。  
  - 需要额外的差分数组和位移数组，各自长度约为 `n`。  
  - 只比原字符串多占了一倍的线性空间，已经是最优的线性级别。

---

## 心得

- **核心技巧**：**差分数组 + 前缀和**，用来把大量区间操作压缩成一次线性遍历。  
- **适用的题型**：  
  1. 区间加法或减法（如 LeetCode 370 “Range Addition”）  
  2. 区间翻转、翻转次数统计（如 “Flip Bits” 系列）  
  3. 需要对区间进行累计统计的字符串/数组题目（如 “Maximum Difference After Array Modification”）  
- **解题钥匙**：**把每一次“区间操作”转成两点标记，随后一次前缀和把所有操作合并**。

---

## 反思

- **第一反应**：看到“区间”+“多次操作”，下意识想到直接遍历区间，这就是暴力解。  
- **最容易踩的坑**：  
  - **方向的正负**：忘记把 `direction=0` 当作 `-1`，导致所有后移变成前移。  
  - **模运算**：位移可能是负数，直接 `% 26` 在 Python 中已经能得到正数，但要注意先把字符下标转成整数后再取模。  
  - **边界**：`diff` 长度要比字符串多 1，防止在 `end == n-1` 时访问越界。  
- **下次思路**：一看到“对同一数组/字符串的多个区间增减”，立刻想到 **差分 + 前缀和**，先把区间操作压缩，再统一遍历求解。