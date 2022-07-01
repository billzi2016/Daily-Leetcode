# #1839. 有序全部元音的最长子串 / Longest Substring Of All Vowels in Order

> 难度：中等 · 标签：String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-substring-of-all-vowels-in-order/)

---

## 题目（英文原版）

**Description**

A string is considered beautiful if it satisfies the following conditions:
For example, strings "aeiou" and "aaaaaaeiiiioou" are considered beautiful, but "uaeio", "aeoiu", and "aaaeeeooo" are not beautiful.
Given a string word consisting of English vowels, return the length of the longest beautiful substring of word. If no such substring exists, return 0.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: word = "aeiaaioaaaaeiiiiouuuooaauuaeiu"
Output: 13
Explanation: The longest beautiful substring in word is "aaaaeiiiiouuu" of length 13.
```

**Example 2:**

```
Input: word = "aeeeiiiioooauuuaeiou"
Output: 5
Explanation: The longest beautiful substring in word is "aeiou" of length 5.
```

**Example 3:**

```
Input: word = "a"
Output: 0
Explanation: There is no beautiful substring, so return 0.
```

**Constraints**

- 1 <= word.length <= 5 * 105
- word consists of characters 'a', 'e', 'i', 'o', and 'u'.

---

## 题目（中文翻译）

一个字符串如果满足以下条件，则被认为是 **beautiful（美观）** 的：
- 只包含元音字符 `'a'`, `'e'`, `'i'`, `'o'`, `'u'`；
- 必须按照字母顺序 `a → e → i → o → u` 出现，且每个元音至少出现一次；
- 同一元音可以连续出现多次，但不能出现逆序或跳过的元音。

给定仅由英文元音组成的字符串 `word`，返回 `word` 中最长 **beautiful（美观）** 子串（**substring**）的长度。如果不存在这样的子串，返回 `0`。  
子串是字符串中连续的字符序列。

### 示例

**示例 1**  
```
Input: word = "aeiaaioaaaaeiiiiouuuooaauuaeiu"
Output: 13
Explanation: 最长的美观子串是 "aaaaeiiiiouuu"，长度为 13。
```

**示例 2**  
```
Input: word = "aeeeiiiioooauuuaeiou"
Output: 5
Explanation: 最长的美观子串是 "aeiou"，长度为 5。
```

**示例 3**  
```
Input: word = "a"
Output: 0
Explanation: 不存在美观子串，返回 0。
```

### 约束条件
- `1 <= word.length <= 5 * 10^5`
- `word` 仅由字符 `'a'`, `'e'`, `'i'`, `'o'`, `'u'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从每一个字符开始，尝试往后扩展，看看能否得到一个“漂亮子串”。**  
> *漂亮子串* 的定义是：只包含元音且必须严格按照 `a → e → i → o → u` 的顺序出现，每个字母出现的次数可以大于等于 1，但顺序不能错位。

可以把这个过程想象成 **在一排字母里找连续的“彩虹”，从 `a` 开始往后依次往右走，只要下一个字母不是比当前字母更大的（比如在 `a` 后面出现了 `i`），就必须停下来。**  

具体步骤：

1. 用两层循环，外层 `i` 表示子串的起始位置，内层 `j` 向右扫描。  
2. 维护一个 **当前应该出现的元音**（用一个列表 `['a','e','i','o','u']` 和一个指针 `idx` 表示）。  
3. 当 `word[j]` 与 `word[j-1]` 相同，或者是 **恰好是下一个元音**（`word[j] == order[idx+1]`），就可以继续扩展；否则本次子串结束。  
4. 如果在扩展结束时已经遍历到了 `u`（即 `idx == 4`），说明得到一个合法的漂亮子串，更新答案的最大长度。  

**为什么正确？**  
因为我们从每个可能的起点出发，严格按照题目要求检查每个字符是否符合“顺序不倒退、只能前进或停留”的规则，遍历完所有起点后，必然会找到所有合法的子串，自然也能得到最长的那一个。

**时间/空间复杂度**  
- 外层遍历 `n` 次，内层最坏情况下也会遍历 `n` 次（比如全是 `a`），所以时间复杂度是 **O(n²)**。  
  - 大白话：如果字符串长 10⁴，需要检查 10⁴ × 10⁴ = 1 亿次，计算机会慢到不忍直视。  
- 只用了常数个额外变量（指针、计数器），空间复杂度是 **O(1)**。

#### 代码（Python）

```python
def longestBeautifulSubstring_bruteforce(word: str) -> int:
    order = ['a', 'e', 'i', 'o', 'u']          # 元音的正确顺序
    n = len(word)
    ans = 0

    for i in range(n):                         # ① 选取子串的左端点
        idx = 0                                 # 当前应该匹配的元音在 order 中的下标
        if word[i] != 'a':                      # 必须以 'a' 开头，直接跳过
            continue

        for j in range(i, n):                   # ② 向右扩展子串
            # 如果当前字符不是合法的元音，直接终止
            if word[j] not in order:
                break

            # 若字符比当前需要的元音更大，尝试向后移动 idx
            while idx < 4 and word[j] == order[idx + 1]:
                idx += 1                         # 进入下一个元音阶段

            # 若出现了倒退的字符（比如在 'e' 阶段出现 'a'），子串结束
            if order[idx] != word[j]:
                break

            # 当已经遍历到 'u'（idx == 4）时，子串合法，更新答案
            if idx == 4:
                ans = max(ans, j - i + 1)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环导致最坏情况要检查每对起止位置。  
- **空间复杂度**：`O(1)` —— 只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每个起点都要重新扫描**，导致大量重复工作。  
我们可以把“从左到右一次遍历，动态维护当前窗口是否仍然是漂亮的”这一思路抽象为 **滑动窗口（Sliding Window）**。

滑动窗口的核心是：

1. **左指针 `left`** 标记当前窗口的左边界，**右指针 `right`** 逐步向右移动扩展窗口。  
2. 窗口内必须满足 **“元音顺序不倒退、且已经出现过的元音只能向后或保持不变”**。  
3. 当出现**倒退**（比如从 `i` 突然回到 `a`）时，说明窗口已经不合法，需要把左指针移到**倒退字符的下一个位置**，并重新统计已经出现的元音阶段。  

为了快速判断当前字符是否符合顺序，我们可以使用一个 **字典 `pos`** 把每个元音映射到它在顺序中的下标：

```python
pos = {'a':0, 'e':1, 'i':2, 'o':3, 'u':4}
```

遍历过程中维护一个变量 `stage`，表示窗口已经走到的最大元音下标（0~4）。  
- 当 `pos[word[right]]` **等于** `stage`（同一阶段）或 **等于** `stage+1`（刚好进入下一个阶段）时，窗口仍合法，`stage` 相应更新。  
- 否则说明出现了倒退，需要把左指针 **移动到 `right`**（重新以当前字符为新窗口的起点），并把 `stage` 重置为该字符对应的下标。

每当 `stage == 4`（窗口已经覆盖到 `u`）时，说明当前窗口是一个合法的漂亮子串，更新最大长度。

> 类比：把字符串想象成一条河流，**窗口** 是一艘船。船只能顺流而下（只能向后或保持），一旦遇到逆流（倒退字符），就必须把船拉回到逆流的起点重新出发。

**为什么线性 O(n)？**  
因为每个字符最多被右指针访问一次，左指针也最多向右移动 `n` 步，整体是一次线性扫描，没有嵌套循环。

#### 代码（Python）

```python
def longestBeautifulSubstring(word: str) -> int:
    # 元音对应的顺序编号，类似查字典：'a' 在第0位，'e' 在第1位 ...
    pos = {'a': 0, 'e': 1, 'i': 2, 'o': 3, 'u': 4}

    left = 0               # 窗口左边界
    stage = 0              # 已经遍历到的最大元音下标（0~4）
    ans = 0

    for right, ch in enumerate(word):          # 右指针从左到右遍历
        cur = pos[ch]                           # 当前字符的顺序编号

        # 1. 如果出现倒退（cur < stage），必须重新开始窗口
        if cur < stage:
            left = right                         # 左边界直接跳到当前字符
            stage = cur                          # stage 重新以当前字符为起点
        else:
            # 2. 正常情况：cur == stage 或 cur == stage+1
            stage = max(stage, cur)              # 记录已经到达的最高阶段

        # 3. 当窗口已经包含了完整的 a->e->i->o->u（stage == 4）时，更新答案
        if stage == 4:
            ans = max(ans, right - left + 1)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只进行一次线性遍历，`n` 为字符串长度。与暴力解的 `O(n²)` 相比，速度提升了数百倍。  
- **空间复杂度**：`O(1)` —— 只用了常数个变量（字典、指针、计数器），不随输入规模增长。

---

## 心得

- 这道题考察的核心技巧是 **滑动窗口 + 状态维护**（记录当前已进入的元音阶段）。  
- 类似技巧常用于：  
  1. **最长无重复字符子串**（LeetCode 3）——维护字符出现位置的窗口。  
  2. **最长子数组和为 K**（LeetCode 560）——使用前缀和配合窗口。  
- **解题钥匙**：一次遍历中“只要窗口不合法就立刻收缩”，保持窗口始终合法即可。

---

## 反思

- **第一反应**：从每个 `'a'` 开始向后枚举，看能否形成完整的 `aeiou` 顺序。  
- **最容易踩的坑**：  
  - 忘记处理 **倒退** 的情况，只判断是否是下一个元音会导致错误的窗口。  
  - 边界条件：只有单个字符或没有完整 `aeiou` 时应返回 `0`。  
  - `stage` 的初始化要对应 `'a'` 的下标，否则会把合法的 `'a'` 当作倒退。  
- **下次遇到同类题**，第一步应该思考 **“是否可以用滑动窗口把合法区间动态维护？”**，如果答案是“可以”，就尝试记录窗口的状态（如最大阶段、字符计数等），再在遍历中即时收缩或扩张。