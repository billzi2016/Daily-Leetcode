# #3114. **替换字符后可获得的最晚时间** / Latest Time You Can Obtain After Replacing Characters

> 难度：简单 · 标签：String、Enumeration · [LeetCode 链接](https://leetcode.com/problems/latest-time-you-can-obtain-after-replacing-characters/)

---

## 题目（英文原版）

**Description**

You are given a string s representing a 12-hour format time where some of the digits (possibly none) are replaced with a "?".
12-hour times are formatted as "HH:MM", where HH is between 00 and 11, and MM is between 00 and 59. The earliest 12-hour time is 00:00, and the latest is 11:59.
You have to replace all the "?" characters in s with digits such that the time we obtain by the resulting string is a valid 12-hour format time and is the latest possible.
Return the resulting string.

**Examples**

**Example 1:**

```
Input: s = "1?:?4"
Output: "11:54"
Explanation: The latest 12-hour format time we can achieve by replacing "?" characters is "11:54" .
```

**Example 2:**

```
Input: s = "0?:5?"
Output: "09:59"
Explanation: The latest 12-hour format time we can achieve by replacing "?" characters is "09:59" .
```

**Constraints**

- s.length == 5
- s[2] is equal to the character ":".
- All characters except s[2] are digits or "?" characters.
- The input is generated such that there is at least one time between "00:00" and "11:59" that you can obtain after replacing the "?" characters.

---

## 题目（中文翻译）

你得到一个字符串 `s`，它表示 12 小时制时间（12-hour format time），其中部分数字（可能没有）被字符 `'?'` 替代。  
12 小时制时间的格式为 `"HH:MM"`，其中 `HH` 的取值范围是 `00` 到 `11`，`MM` 的取值范围是 `00` 到 `59`。最早的时间是 `00:00`，最晚的时间是 `11:59`。  

请将 `s` 中所有的 `'?'` 替换为数字，使得得到的字符串表示的时间是合法的 12 小时制时间，并且在所有可能的合法时间中尽可能晚。返回得到的字符串。

**示例 1**  
输入: `s = "1?:?4"`  
输出: `"11:54"`  
解释: 通过替换 `'?'`，能够得到的最晚的 12 小时制时间是 `"11:54"`。

**示例 2**  
输入: `s = "0?:5?"`  
输出: `"09:59"`  
解释: 通过替换 `'?'`，能够得到的最晚的 12 小时制时间是 `"09:59"`。

**约束条件**  

- `s.length == 5`  
- `s[2]` 必须是字符 `":"`。  
- 除了 `s[2]` 之外，所有字符要么是数字，要么是字符 `'?'`。  
- 输入保证至少存在一种方式可以将 `'?'` 替换成数字，使得得到的时间介于 `"00:00"` 与 `"11:59"` 之间。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有合法的 12 小时制时间枚举出来，然后和给定的带 `?` 的字符串逐字符对比，看哪个符合模式，挑出最大的那一个。

- **枚举**：12 小时制的时间只有 `00:00 ~ 11:59`，共 `12 × 60 = 720` 种。我们可以用两层循环，外层遍历小时 `0~11`，内层遍历分钟 `0~59`。
- **匹配**：把每一对 `(hour, minute)` 用 `"%02d:%02d"` 的格式化方式写成 `"HH:MM"`，然后逐字符检查：如果原字符串对应位置是数字且不相等，则这一次枚举不符合；如果是 `'?'`，则可以随意匹配。
- **取最大**：符合模式的时间用整数 `hour*60 + minute` 表示，记录最大的那一次即可。

> **类比**：把所有可能的时间想象成一本字典（哈希表的“查字典”），我们在这本字典里找出所有“匹配模式”的词，然后挑出字典序最大的那个词。

#### 代码（Python）

```python
def latestTimeBruteForce(s: str) -> str:
    best = -1               # 用来保存当前找到的最大时间（分钟数）
    best_str = ""           # 对应的字符串形式

    # 枚举所有合法的 hour（0~11） 和 minute（0~59）
    for hour in range(12):
        for minute in range(60):
            cur = f"{hour:02d}:{minute:02d}"   # 把时间转成 "HH:MM" 形式

            # 检查每一位是否和 s 匹配
            match = True
            for i, ch in enumerate(s):
                if ch != '?' and ch != cur[i]:   # 不是 '?'，且不相等，则不匹配
                    match = False
                    break
            if not match:
                continue

            # 计算当前时间对应的“分钟数”，用于比较大小
            total_min = hour * 60 + minute
            if total_min > best:          # 发现更大的合法时间
                best = total_min
                best_str = cur

    return best_str
```

#### 复杂度

- **时间复杂度**：`O(12 × 60 × 5) ≈ O(720)`，常数很小。这里的 `5` 是因为每次比较要遍历 5 个字符（`HH:MM`）。
  - **大白话**：我们最多检查 720 种时间，每种时间只看 5 位字符，几乎可以忽略不计。
- **空间复杂度**：`O(1)`，只用常数级别的变量保存当前最优解。

---

### 2. 最优解

#### 思路  

暴力解虽然已经足够快，但我们可以直接**构造**出最大的合法时间，而不必遍历所有可能。关键在于逐位决定该填什么数字，使得整体仍然合法且尽可能大。

1. **先确定小时的十位**（`s[0]`）  
   - 合法范围是 `0` 或 `1`（因为 12 小时制最高是 `11`）。  
   - 如果已经是数字，直接使用。  
   - 如果是 `'?'`，我们想让它尽量大：  
     - 当第二位（`s[1]`）是 `'?'`、`'0'`、`'1'` 时，十位可以设为 `1`，因为 `1x` 仍在合法范围内。  
     - 否则（第二位已经是 `2~9`），十位只能设为 `0`，否则会产生 `2x`、`3x`… 这类非法小时。

2. **确定小时的个位**（`s[1]`）  
   - 已知十位后，个位的取值受限：  
     - 十位是 `1` → 小时只能是 `10` 或 `11`，所以最大是 `1`。  
     - 十位是 `0` → 小时可以是 `00~09`，最大是 `9`。  
   - 同样，如果已经是数字，直接保留；如果是 `'?'`，填上对应的最大值。

3. **确定分钟的十位**（`s[3]`）  
   - 分钟的十位只能是 `0~5`（因为分钟最高是 `59`）。  
   - `'?'` 时直接填 `5`，得到最大可能的十位。

4. **确定分钟的个位**（`s[4]`）  
   - 没有额外限制，`0~9` 都合法。  
   - `'?'` 时填 `9`。

这样一步步填完四个数字，就得到在所有满足模式的时间中**最大的**那一个。

> **类比**：想象你在给一把锁设密码，每个转盘只能转到一定的范围。我们从左到右依次把每个转盘调到该范围内的最大数字，最后得到的密码自然是所有合法密码里最大的。

#### 代码（Python）

```python
def latestTimeOptimal(s: str) -> str:
    # 把字符串转成列表，方便原地修改字符
    t = list(s)

    # ---------- 处理小时 ----------
    # 第 0 位（十位）
    if t[0] == '?':
        # 看第 1 位能否接受十位为 1
        if t[1] in ('?', '0', '1'):
            t[0] = '1'          # 十位设为 1，尽可能大
        else:
            t[0] = '0'          # 否则只能是 0

    # 第 1 位（个位）
    if t[1] == '?':
        if t[0] == '1':
            t[1] = '1'          # 十位是 1 时，最大只能是 11
        else:  # t[0] == '0'
            t[1] = '9'          # 十位是 0 时，最大可以是 09

    # ---------- 处理分钟 ----------
    # 第 3 位（十位）只能是 0~5
    if t[3] == '?':
        t[3] = '5'              # 直接填最大合法的 5

    # 第 4 位（个位）0~9，直接填 9
    if t[4] == '?':
        t[4] = '9'

    # 合并回字符串并返回
    return "".join(t)
```

#### 复杂度

- **时间复杂度**：`O(1)`，只遍历固定的 5 个字符，时间不随输入长度变化（因为长度恒为 5）。
- **空间复杂度**：`O(1)`，只用了一个长度为 5 的列表来暂存字符。

> 与暴力解对比：  
> - 暴力解需要遍历 720 种可能，时间上仍是常数级别，但写法更冗长。  
> - 最优解一步到位，只做有限次判断，概念上更清晰，也更符合面试中“**直接构造**”的思路。

---

## 心得

- **核心技巧**：**按位限制构造**（Greedy by position）。先弄清每一位的合法取值范围，再在该范围内挑最大。
- **适用题型**  
  1. “把 `?` 替换成数字得到最大/最小合法数”——例如 *Maximum Number From Digits After Replacement*。  
  2. “在满足一定约束的情况下，构造字典序最大的字符串”——例如 *Largest Number After Digit Swap*。  
  3. “根据限定的区间，求满足条件的最大时间/日期”——例如 *Maximum Time Using Digits*（24 小时制）。
- **一句话总结**：**先明确每一位的合法上界，再把每个 `'?'` 填成这个上界**，即可得到答案。

---

## 反思

- **第一反应**：看到 `?`，立刻想到枚举所有可能（暴力搜索），因为这样最保险。
- **最容易踩的坑**  
  - **小时十位的判断**：忽略了第二位已经是 `2~9` 时，十位必须是 `0`，否则会产生非法的 `2x`、`3x`…。  
  - **分钟十位只能到 5**：如果直接填 `9`，会得到非法的分钟（如 `69`），必须记得这个额外的上限。  
  - **字符串不可变**：直接对 `s` 赋值会报错，需要先转成列表或使用切片拼接。
- **下次遇到同类题**：第一步先**写出每个位置的合法取值范围**，再**从左到右贪心填最大（或最小）**。这样既能保证合法，又能直接得到极值。