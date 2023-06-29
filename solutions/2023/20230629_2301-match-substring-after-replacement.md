# #2301. 匹配替换后子串 / Match Substring After Replacement

> 难度：困难 · 标签：Array、Hash Table、String、String Matching · [LeetCode 链接](https://leetcode.com/problems/match-substring-after-replacement/)

---

## 题目（英文原版）

**Description**

You are given two strings s and sub. You are also given a 2D character array mappings where mappings[i] = [oldi, newi] indicates that you may perform the following operation any number of times:
Each character in sub cannot be replaced more than once.
Return true if it is possible to make sub a substring of s by replacing zero or more characters according to mappings. Otherwise, return false.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "fool3e7bar", sub = "leet", mappings = [["e","3"],["t","7"],["t","8"]]
Output: true
Explanation: Replace the first 'e' in sub with '3' and 't' in sub with '7'.
Now sub = "l3e7" is a substring of s, so we return true.
```

**Example 2:**

```
Input: s = "fooleetbar", sub = "f00l", mappings = [["o","0"]]
Output: false
Explanation: The string "f00l" is not a substring of s and no replacements can be made.
Note that we cannot replace '0' with 'o'.
```

**Example 3:**

```
Input: s = "Fool33tbaR", sub = "leetd", mappings = [["e","3"],["t","7"],["t","8"],["d","b"],["p","b"]]
Output: true
Explanation: Replace the first and second 'e' in sub with '3' and 'd' in sub with 'b'.
Now sub = "l33tb" is a substring of s, so we return true.
```

**Constraints**

- 1 <= sub.length <= s.length <= 5000
- 0 <= mappings.length <= 1000
- mappings[i].length == 2
- oldi != newi
- s and sub consist of uppercase and lowercase English letters and digits.
- oldi and newi are either uppercase or lowercase English letters or digits.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `sub`。同时提供一个二维字符数组 **mappings**，其中 `mappings[i] = [oldi, newi]` 表示你可以任意次数执行以下操作：将 `sub` 中的某个字符 **oldi** 替换为 **newi**。  
**注意**：`sub` 中的每个字符至多只能被替换一次。

返回 `true` 当且仅当通过零次或多次按照 **mappings** 进行替换后，能够使 `sub` 成为 `s` 的 **子串（substring）**。否则返回 `false`。  
**子串（substring）** 指的是字符串中连续的、非空的字符序列。

---

### 示例

#### 示例 1
```text
Input: s = "fool3e7bar", sub = "leet", mappings = [["e","3"],["t","7"],["t","8"]]
Output: true
```
**解释**：将 `sub` 中的第一个 `'e'` 替换为 `'3'`，将 `'t'` 替换为 `'7'`，得到 `sub = "l3e7"`，它是 `s` 的子串，所以返回 `true`。

#### 示例 2
```text
Input: s = "fooleetbar", sub = "f00l", mappings = [["o","0"]]
Output: false
```
**解释**：字符串 `"f00l"` 不是 `s` 的子串，且无法进行任何合法替换。需要注意，不能将 `'0'` 替换回 `'o'`。

#### 示例 3
```text
Input: s = "Fool33tbaR", sub = "leetd", mappings = [["e","3"],["t","7"],["t","8"],["d","b"],["p","b"]]
Output: true
```
**解释**：将 `sub` 中的两个 `'e'` 分别替换为 `'3'`，将 `'d'` 替换为 `'b'`，得到 `sub = "l33tb"`，它是 `s` 的子串，所以返回 `true`。

---

### 约束

- `1 <= sub.length <= s.length <= 5000`
- `0 <= mappings.length <= 1000`
- `mappings[i].length == 2`
- `oldi != newi`
- `s` 和 `sub` 只包含大小写英文字母和数字。
- `oldi` 与 `newi` 均为大小写英文字母或数字。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **枚举** `s` 中所有长度等于 `sub` 的连续子串（窗口）。  
2. 对每一个窗口，逐字符检查它能否和 `sub` 的对应字符“对上”。  
   - 对于 `sub` 中的字符 `c`，我们可以**不替换**，也可以把它替换成映射表里直接给出的 `new`。  
   - 因此 `c` 实际上可以变成的字符集合是  
     ```text
     {c} ∪ { new | [c, new] 出现在 mappings 中 }
     ```  
     把它想象成一本 **查字典**：键（key）是原字符 `c`，值（value）是它可以“变成”的所有字符。  
   - 检查窗口中的字符 `w` 是否在这个集合里，如果全部匹配成功，则说明通过若干次（每个字符至多一次）替换后，`sub` 能成为 `s` 的子串，返回 `True`。  

**为什么正确**  
- 我们穷举了所有可能的起始位置，且对每个位置检查了**所有合法的替换**（因为集合已经把“保持不变”和“单次直接替换”都包含进来了）。  
- 若存在一种替换方式使 `sub` 成为子串，那么对应的窗口必然会在枚举过程中被检测到并返回 `True`。  

**时间 / 空间复杂度**  
- 枚举窗口的次数是 `|s|‑|sub|+1`（最多约 `5000` 次），每次最坏要比较 `|sub|` 个字符。  
- 直接用列表查找映射会导致每次比较的代价是 `O(k)`（`k` 为映射条数），所以**最朴素的**暴力实现时间复杂度是 `O(|s|·|sub|·k)`。  
- 用大白话讲，`O(n·m·k)` 就像“先挑出 `n` 本书，每本书翻 `m` 页，每页再去找 `k` 条注释”。  

#### 代码（Python）

```python
def can_make_substring_bruteforce(s: str, sub: str, mappings) -> bool:
    # ---------- 1. 把映射整理成「查字典」 ----------
    # old_char -> {new_char1, new_char2, ...}
    replace_dict = {}
    for old, new in mappings:
        replace_dict.setdefault(old, set()).add(new)

    # ---------- 2. 为 sub 的每个位置预先算出「可以得到的字符集合」 ----------
    # 这里我们直接在比较时算集合，保持最朴素的写法
    n, m = len(s), len(sub)

    # ---------- 3. 枚举所有长度为 m 的窗口 ----------
    for start in range(n - m + 1):               # 每一个可能的起点
        ok = True                                 # 假设这段窗口可以匹配
        for i in range(m):                       # 对窗口里的每个字符
            ch_sub = sub[i]                       # sub 的原字符
            ch_s   = s[start + i]                 # 窗口对应的字符

            # ① 不替换的情况
            if ch_s == ch_sub:
                continue

            # ② 看看有没有直接映射可以把 ch_sub 变成 ch_s
            if ch_sub in replace_dict and ch_s in replace_dict[ch_sub]:
                continue

            # ③ 都不行，说明这个窗口匹配失败
            ok = False
            break

        if ok:                                     # 找到一个成功的窗口
            return True

    return False                                   # 所有窗口都不行
```

#### 复杂度

- **时间复杂度**：`O(|s|·|sub|·k)`  
  - `|s|` 是主字符串的长度，`|sub|` 是子串的长度，`k` 是映射条数。  
  - 大白话：如果 `s` 长 5000，`sub` 长 5000，映射有 1000 条，最坏要做 5000·5000·1000 ≈ 2.5 × 10¹⁰ 次检查，显然太慢了。  

- **空间复杂度**：`O(k)`  
  - 只用了一个字典存映射表，大小随 `k` 增长。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于每次比较字符时都要遍历映射表去判断是否可以替换，导致额外的 `k` 因子。  
优化的关键是**把「可以得到的字符集合」提前算好**，这样在比较时只需要 O(1) 的集合查找。  

具体步骤：

1. **预处理映射**  
   - 建立一个 **哈希表** `allow[char] = set([...])`，其中 `allow[c]` 包含 `c` 本身以及所有能直接把 `c` 替换成的字符。  
   - 这一步相当于把「查字典」提前装好，后面查的时候只要看 `c2 in allow[c1]` 即可，时间是 O(1)。  

2. **滑动窗口**（仍然枚举所有起点）  
   - 对每个起点 `i`，逐字符比较 `s[i+j]` 与 `sub[j]`。  
   - 只要有一次 `s[i+j]` 不在 `allow[sub[j]]`，就立刻**提前退出**当前窗口的检查。  
   - 由于每次比较都是 O(1)，整体时间变成 `O(|s|·|sub|)`，空间只多了 `O(Σ|allow|) ≤ O(62·62)`（因为字符集合只包含大小写字母和数字），几乎可以忽略。  

3. **为什么仍然遍历所有窗口**  
   - `|s|` 最多 5000，`|sub|` 最多 5000，`|s|·|sub|` 最多 25 000 000 次字符比较。  
   - 这在 Python 中是完全可以接受的，且实现非常直观。  

> **小技巧**：如果想进一步提升常数（比如在竞赛中追求极限），可以把每个字符映射成 **位掩码**（bitmask），利用位运算一次性判断是否匹配。但这里不必引入额外复杂度，直接用 `set` 已经足够快且易懂。

#### 代码（Python）

```python
def can_make_substring(s: str, sub: str, mappings) -> bool:
    """
    最优实现：预处理映射，使每次字符匹配 O(1)。
    """
    # ---------- 1. 预处理映射 ----------
    # allow[c] = {c, all characters that c can be replaced with}
    allow = {chr(i): {chr(i)} for i in range(128)}   # 初始化：每个字符默认可以保持不变
    for old, new in mappings:
        allow[old].add(new)                         # 直接把 new 加入 old 的集合

    n, m = len(s), len(sub)

    # ---------- 2. 枚举所有起始位置 ----------
    for start in range(n - m + 1):
        ok = True
        for j in range(m):
            if s[start + j] not in allow[sub[j]]:   # O(1) 集合查找
                ok = False
                break
        if ok:
            return True

    return False
```

#### 复杂度

- **时间复杂度**：`O(|s|·|sub|)`  
  - 只剩下两层循环，内层的“字符能否匹配”是 O(1)。  
  - 用大白话讲，就是“先挑出最多 5000 本书，每本书只翻一次 5000 页”，最多 25 百万次操作，跑得很快。  

- **空间复杂度**：`O(Σ|allow|) ≈ O(1)`（常数级）  
  - `allow` 表只存 62（大小写字母+数字）个字符的集合，每个集合最多再装 62 个字符，整体大小固定。  

---

## 心得  

- **核心技巧**：把「字符可以被哪些字符替换」的关系提前预处理成 **哈希表/集合**，把每次匹配的判断从 “遍历映射表” 降到 **O(1) 查表**。  
- **适用场景**：  
  1. **带有一次性字符映射的模式匹配**（本题）。  
  2. **带有通配符/替换规则的字符串搜索**（如 `*`、`?` 的简化版）。  
  3. **字符转换限制的编辑距离/变形匹配**（每个字符只能被替换一次的情形）。  
- **一句话总结**：**把所有合法替换一次性装进查字典，匹配时直接查表即可**。

---

## 反思  

- **第一反应**：看到“可以把 sub 的字符替换成别的字符”，立刻想到 **枚举所有子串** 再逐字符比较。  
- **最容易踩的坑**：  
  - 忘记 **每个字符只能替换一次**，误把多次链式替换（`a→b→c`）算进来。  
  - 忽视 **保持不变** 的情况，导致匹配时遗漏了原字符本身。  
  - 边界条件：`sub` 长度等于 `s` 长度时只能检查一次窗口；`mappings` 为空时只能直接比较。  
- **下次思路**：看到“字符 → 若干候选字符”这类描述时，第一步就 **把候选集合预处理成哈希表**，再进行匹配，避免在循环里重复遍历映射表。这样既保证正确性，又能把时间复杂度压到最小。