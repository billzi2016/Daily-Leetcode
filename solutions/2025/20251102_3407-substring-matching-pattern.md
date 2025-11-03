# #3407. 子串匹配模式 / Substring Matching Pattern

> 难度：简单 · 标签：String、String Matching · [LeetCode 链接](https://leetcode.com/problems/substring-matching-pattern/)

---

## 题目（英文原版）

**Description**

You are given a string s and a pattern string p, where p contains exactly one '*' character.
The '*' in p can be replaced with any sequence of zero or more characters.
Return true if p can be made a substring of s, and false otherwise.

**Examples**

**Example 1:**

```
Input: s = "leetcode", p = "ee*e"
Output: true
Explanation:
By replacing the '*' with "tcod" , the substring "eetcode" matches the pattern.
```

**Example 2:**

```
Input: s = "car", p = "c*v"
Output: false
Explanation:
There is no substring matching the pattern.
```

**Example 3:**

```
Input: s = "luck", p = "u*"
Output: true
Explanation:
The substrings "u" , "uc" , and "uck" match the pattern.
```

**Constraints**

- 1 <= s.length <= 50
- 1 <= p.length <= 50
- s contains only lowercase English letters.
- p contains only lowercase English letters and exactly one '*'

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `s` 和一个模式字符串 `p`，其中 `p` 恰好包含一个 `'*'` 字符。  
`p` 中的 `'*'` 可以替换为任意长度（包括长度为 0）的字符序列。  
返回 `true` 表示可以通过替换 `'*'` 使得模式 `p` 成为 `s` 的子串（substring），否则返回 `false`。

**示例 1**  
```text
Input: s = "leetcode", p = "ee*e"
Output: true
Explanation:
将 '*' 替换为 "tcod" 后，子串 "eetcode" 与模式匹配。
```

**示例 2**  
```text
Input: s = "car", p = "c*v"
Output: false
Explanation:
不存在匹配该模式的子串。
```

**示例 3**  
```text
Input: s = "luck", p = "u*"
Output: true
Explanation:
子串 "u"、"uc"、"uck" 都可以匹配该模式。
```

**约束条件**  
- `1 <= s.length <= 50`
- `1 <= p.length <= 50`
- `s` 仅由小写英文字母组成。
- `p` 仅由小写英文字母和恰好一个 `'*'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可能的子串都枚举出来，然后把模式 `p` 中的 `*` 当成“可以匹配任意字符（包括空）”的通配符，逐个检查子串能否匹配。  
- **子串枚举**：把字符串 `s` 的每一个起点 `i`（0 ≤ i < len(s)）和终点 `j`（i ≤ j ≤ len(s)）组合起来，就得到 `s[i:j]` 这个子串。  
- **匹配方式**：把模式 `p` 按 `*` 分成左半部分 `pre` 和右半部分 `suf`（如果 `*` 在最左或最右，`pre` 或 `suf` 可能为空）。  
  - 先检查子串是否以 `pre` 开头；  
  - 再检查子串是否以 `suf` 结尾；  
  - 中间的字符（如果有）就交给 `*`，不管它是什么都可以。  

> **类比**：把 `*` 想成一本空白的日记本，里面可以随意写任意长度的文字；只要前面几页（`pre`）和后面几页（`suf`）和我们手中的纸条（子串）对应上，就算匹配成功。

由于 `s` 最长只有 50，子串的数量至多 `50 * 51 / 2 = 1275`，完全可以一次性枚举完。

#### 代码（Python）

```python
def is_match_bruteforce(s: str, p: str) -> bool:
    # 把模式按 * 分成左、右两段
    pre, suf = p.split('*')
    n = len(s)

    # 枚举所有子串 s[i:j]（左闭右开区间）
    for i in range(n + 1):          # 起点可以在最末尾（空串）
        for j in range(i, n + 1):   # 终点可以等于起点，得到空串
            sub = s[i:j]

            # 1️⃣ 检查左段是否匹配
            if not sub.startswith(pre):
                continue            # 左段不匹配，直接下一个子串

            # 2️⃣ 检查右段是否匹配
            if not sub.endswith(suf):
                continue            # 右段不匹配

            # 3️⃣ 此时左、右都匹配，* 能覆盖中间的所有字符
            # （不需要额外判断，因为 * 可以匹配 0~任意字符）
            return True

    # 没有任何子串满足条件
    return False
```

#### 复杂度

- **时间复杂度**：`O(n³)`（最坏情况）  
  - `n` 是 `s` 的长度（≤50）。  
  - 两层循环枚举子串是 `O(n²)`，每次匹配 `startswith` / `endswith` 需要 `O(n)`（检查字符），所以总体是 `O(n³)`。  
  - 由于 `n` 很小，这种“三次方”算力在实际运行中毫无压力。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，子串 `sub` 通过切片直接引用原字符串，不会产生额外的线性空间。

---

### 2. 最优解

#### 思路  

暴力解的“慢点”在于 **枚举所有子串**，其实我们并不需要真的把子串取出来，只要找到 **左段** 出现的位置，再检查 **右段** 是否在它之后出现即可。  

关键观察：

1. `*` 可以匹配 **任意长度**，所以只要左段 `pre` 出现在 `s` 的某个位置 `i`，右段 `suf` 出现在 `i + len(pre)` 之后的任意位置，就一定可以把 `*` 填成中间的那段字符，使得整个模式成为 `s` 的一个子串。  
2. 如果左段为空，等价于“从字符串最左边开始检查右段”。同理右段为空，只要左段出现一次就行。  

基于此，我们只需要：

- 用 `str.find`（或手写循环）找出 **所有** 左段出现的位置 `i`。  
- 对每个 `i`，在 `s[i + len(pre):]` 中再次调用 `find` 看右段是否出现。  
- 任意一次成功即返回 `True`，全部失败则返回 `False`。

> **类比**：把 `pre` 看成钥匙孔的左半边，`suf` 看成右半边。只要左半边能插进去，右半边在左半边后面还能找到匹配的凹槽，剩下的空隙交给 `*`（万能胶）填平，就能“拼合”出完整的图案。

#### 代码（Python）

```python
def is_match_optimal(s: str, p: str) -> bool:
    pre, suf = p.split('*')
    n = len(s)

    # 只要左段出现一次，且右段在它之后出现，就匹配成功
    start = 0
    while True:
        # 在 s 中找左段的下一个出现位置
        idx = s.find(pre, start)
        if idx == -1:                     # 再也找不到左段了
            break

        # 计算右段必须开始检查的下标（左段结束后）
        after_left = idx + len(pre)

        # 在剩余字符串里查找右段（可以是空串）
        if suf == "" or s.find(suf, after_left) != -1:
            return True                    # 找到匹配

        # 否则继续在更靠后的位置寻找左段
        start = idx + 1

    # 左段根本不存在，或者每次左段后面都找不到右段
    return False
```

**说明**：

- `s.find(sub, pos)` 会返回 `sub` 在 `s` 中 **第一次** 出现且不小于 `pos` 的下标，找不到返回 `-1`。  
- 当 `pre` 为 `""`（即 `*` 位于最左）时，`s.find("", start)` 永远返回 `start`，相当于我们从每个位置都尝试一次；此时只要 `suf` 能在任意位置出现（包括空串），答案就是 `True`。  
- 同理 `suf` 为 `""` 时，只要左段出现一次就行。

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况）  
  - 外层循环遍历左段所有出现位置，最坏会有 `O(n)` 次。  
  - 每一次都在剩余子串里调用一次 `find`，`find` 本身最坏是线性 `O(n)`。  
  - 综合下来是 `O(n * n) = O(n²)`，在 `n ≤ 50` 时毫秒级完成。  
  - 与暴力的 `O(n³)` 相比，少了一层枚举子串的循环，实际跑得更快。

- **空间复杂度**：`O(1)`  
  - 只使用了几个整数变量，未额外分配随 `n` 增长的空间。

---

## 心得

- **核心技巧**：把只含一个 `*` 的模式拆成 “左段 + 任意字符 + 右段”，只要左段出现且右段在左段之后出现，就一定能匹配。  
- **适用的题型**  
  1. **单通配符匹配**（如 LeetCode 44 `Wildcard Matching` 的简化版）。  
  2. **前缀‑后缀匹配**（判断字符串是否以某前缀开头且以某后缀结尾）。  
  3. **子串搜索**（在长文本中寻找满足特定前后缀的片段）。  
- **一句话总结**：  
  > “只要左半段出现，右半段在左半段后出现，`*` 自动把中间的空白填满。”

---

## 反思

- **第一反应**：看到 `*` 能匹配任意长度，马上想到把模式拆成两段，然后在原字符串里找这两段的相对位置。  
- **最容易踩的坑**  
  - **空串情况**：`pre` 或 `suf` 可能为空，需要单独处理，否则 `find` 会把空串当作每个位置的匹配。  
  - **重叠匹配**：左段和右段可以相互重叠（例如 `p = "a*a"`），只要右段的起点 **不早于** 左段结束即可。  
  - **边界检查**：左段出现在字符串末尾时，`after_left` 可能等于 `len(s)`，此时仍需要检查右段是否为空。  
- **下次遇到同类题**：第一步先 **把模式按唯一通配符拆分**，再在原字符串里 **分别定位左段和右段**，检查它们的相对顺序即可。这样可以直接跳过“枚举所有子串”的低效步骤。