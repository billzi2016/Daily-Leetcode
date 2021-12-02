# #1576. 替换所有 '?' 以避免连续重复字符 / Replace All ?'s to Avoid Consecutive Repeating Characters

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/replace-all-s-to-avoid-consecutive-repeating-characters/)

---

## 题目（英文原版）

**Description**

Given a string s containing only lowercase English letters and the '?' character, convert all the '?' characters into lowercase letters such that the final string does not contain any consecutive repeating characters. You cannot modify the non '?' characters.
It is guaranteed that there are no consecutive repeating characters in the given string except for '?'.
Return the final string after all the conversions (possibly zero) have been made. If there is more than one solution, return any of them. It can be shown that an answer is always possible with the given constraints.

**Examples**

**Example 1:**

```
Input: s = "?zs"
Output: "azs"
Explanation: There are 25 solutions for this problem. From "azs" to "yzs", all are valid. Only "z" is an invalid modification as the string will consist of consecutive repeating characters in "zzs".
```

**Example 2:**

```
Input: s = "ubv?w"
Output: "ubvaw"
Explanation: There are 24 solutions for this problem. Only "v" and "w" are invalid modifications as the strings will consist of consecutive repeating characters in "ubvvw" and "ubvww".
```

**Constraints**

- 1 <= s.length <= 100
- s consist of lowercase English letters and '?'.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母（lowercase English letters）和字符‘?’的字符串（string）`s`，将所有‘?’字符替换为小写英文字母，使得得到的字符串中 **不存在连续重复字符（consecutive repeating characters）**。原本不是‘?’的字符不可被修改。  

已知除‘?’之外，输入的字符串中不存在连续重复字符。  

返回完成所有替换（可能为零次）后的字符串。如果存在多种可能，返回任意一种即可。可以证明在题目约束下必定存在可行解。  

**示例 1**  
```
输入: s = "?zs"
输出: "azs"
解释: 本题共有 25 种解法。从 "azs" 到 "yzs" 均符合要求。唯一不合法的修改是将 '?' 替换为 "z"，因为会产生连续重复字符 "zzs"。
```

**示例 2**  
```
输入: s = "ubv?w"
输出: "ubvaw"
解释: 本题共有 24 种解法。将 '?' 替换为 "v" 或 "w" 会导致出现连续重复字符，分别得到 "ubvvw" 和 "ubvww"，因此这两种替换不可行。
```

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由小写英文字母和字符‘?’组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有出现的 `'?'` **全部列举** 出来，尝试每一种可能的填法，然后检查得到的字符串里有没有相邻的相同字符。  

- **数据结构**：  
  - 使用 **列表** 把字符串拆成字符，方便后面修改。  
  - 用 **递归**（或循环套循环）遍历每一个 `'?'`，对每个位置尝试 26 个小写字母（`'a'~'z'`），相当于在“字典”里查找所有可能的词。  
- **为什么正确**：  
  - 我们把**所有**合法的填法都穷举出来，只要检查到一种不出现相邻相同字符的方案，就可以返回。因为题目保证一定有解，遍历完整个搜索空间必然会找到答案。  
- **时间/空间复杂度**：  
  - 设字符串中 `'?'` 的个数为 `k`，每个 `'?'` 有 26 种选择，所以总的尝试次数是 `26^k`（指数级）。  
  - 对每一种尝试，我们需要 **O(n)** 的时间去检查相邻字符是否相同。于是总体时间复杂度是 **O(26^k * n)**。  
  - 递归栈深度最多 `k`，再加上把字符串转成列表的 **O(n)** 空间，整体空间复杂度是 **O(n + k)**，在最坏情况下也就是 **O(n)**。

#### 代码（Python）

```python
def replaceQuestionMarks_bruteforce(s: str) -> str:
    """暴力搜索：穷举所有 '?' 的填法，返回第一个合法结果"""
    chars = list(s)                     # 把字符串拆成列表，方便原地修改
    n = len(chars)

    def is_valid():
        """检查当前列表是否没有相邻相同字符"""
        for i in range(1, n):
            if chars[i] == chars[i - 1]:
                return False
        return True

    def dfs(idx: int) -> bool:
        """深度优先搜索，从位置 idx 开始处理"""
        if idx == n:                     # 已经处理完所有字符
            return is_valid()           # 检查是否合法
        if chars[idx] != '?':            # 不是 '?'，直接跳过
            return dfs(idx + 1)

        # 当前是 '?'，尝试 26 个小写字母
        for c in map(chr, range(ord('a'), ord('z') + 1)):
            chars[idx] = c               # 把 '?' 暂时改成 c
            if dfs(idx + 1):             # 递归处理后面的字符
                return True
        chars[idx] = '?'                  # 恢复原样（回溯）
        return False

    dfs(0)                               # 从头开始搜索
    return ''.join(chars)                # 把列表拼回字符串
```

#### 复杂度  

- **时间复杂度**：`O(26^k * n)`  
  - `k` 为 `'?'` 的数量，`26^k` 是所有可能的填法，`n` 是每次检查相邻字符的代价。  
  - 用大白话说，就是“如果有 3 个问号，就要尝试 26³ = 17576 种组合，算起来会非常慢”。  
- **空间复杂度**：`O(n)`  
  - 需要把字符串存进列表（`O(n)`），递归栈最深 `k ≤ n`，合在一起仍是线性空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**把所有可能都尝试一遍**，而实际上我们并不需要这么多尝试。  
观察题目可以发现：

1. **相邻字符只能相等**——只要保证每个 `'?'` 与左侧字符和右侧字符（如果有的话）不同，就一定满足“不出现连续重复”。  
2. **字母只有 26 个**，但我们只需要找 **一个** 与左右不同的字母。因为左、右最多占用 2 个不同的字母，剩下的 **至少有 24 个** 可供选择。  
3. **从左到右依次填** 就可以，因为左边已经确定，右边如果是 `'?'` 还未确定，我们只需要不和左边冲突，后面的步骤再保证右边不冲突即可。

于是我们可以采用**贪心**策略：

- 从左到右遍历字符串。  
- 当遇到 `'?'` 时，查看它左边已经确定的字符 `left`（如果 `i>0`）和右边原始字符 `right`（如果 `i+1 < n` 且不是 `'?'`）。  
- 从 `'a','b','c'`（任选 3 个）中挑一个既不等于 `left` 也不等于 `right` 的字母，直接填入。因为只有 3 个候选字母，必然能找到一个满足条件的（最多排除 2 个）。  

**为什么正确**：

- 对每个 `'?'`，我们只保证它与左、右相邻字符不同。左边已经是最终结果，右边如果是 `'?'`，它会在后面的迭代中再被处理，届时同样会避开当前字符。  
- 这样处理完所有位置后，整个字符串必然没有相邻相同字符。  

**核心数据结构**：  
- 仍然使用 **列表**（可原地修改）来存储字符。  
- 不需要额外的哈希表或栈，空间开销极小。

#### 代码（Python）

```python
def replaceQuestionMarks(s: str) -> str:
    """贪心实现：一次遍历，逐个把 '?' 替换成合适的字母"""
    chars = list(s)                     # 转成列表，便于原地修改
    n = len(chars)

    for i in range(n):
        if chars[i] != '?':             # 不是 '?'，直接跳过
            continue

        # 左侧已经确定的字符（如果有）
        left = chars[i - 1] if i > 0 else ''
        # 右侧原始字符，注意右边可能还是 '?'，此时不需要考虑
        right = chars[i + 1] if i + 1 < n and chars[i + 1] != '?' else ''

        # 只尝试 'a','b','c' 三个字母，必定能找到满足条件的
        for c in ('a', 'b', 'c'):
            if c != left and c != right:
                chars[i] = c            # 把当前 '?' 替换成 c
                break                   # 跳出循环，处理下一个位置

    return ''.join(chars)                # 合成最终字符串
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 我们只遍历一次字符串（`n` 次），每次最多检查 3 个候选字母，常数级操作。  
  - 与暴力解的指数级相比，这就像“从跑马拉松直接坐上了高速列车”。  
- **空间复杂度**：`O(n)`  
  - 需要把原字符串复制成列表，占用 `n` 的空间；除此之外没有额外的结构。

---

## 心得

- **核心技巧**：**贪心填字符**——在每个位置只考虑局部约束（左、右相邻字符），不必回溯全局。  
- **适用题型**：  
  1. “把字符串中的占位符替换成合法字符”——如本题、LeetCode 1576 *Replace All ?'s to Avoid Consecutive Repeating Characters*。  
  2. “颜色涂抹”类问题——如图的 3‑颜色染色，要求相邻节点颜色不同。  
  3. “构造满足局部约束的序列”——比如把数组中 `0` 替换成不相邻相同的数。  
- **一句话总结**：只要保证每个 `'?'` 与左、右相邻字符不同，就能一次遍历完成全部替换。

---

## 反思

- **第一反应**：看到 `'?'`，想到“遍历所有可能”，于是自然想到暴力枚举。  
- **最容易踩的坑**：  
  - **左侧字符已经被替换**：在判断左邻时一定要使用已经**修改后的**字符，而不是原始的 `'?'`。  
  - **右侧字符仍是 '?'**：右邻如果是 `'?'`，不需要把它加入排除集合，否则会误判找不到合法字符。  
  - **字符集合选择**：如果随意选 26 个字母，每次都遍历 26 次会稍显冗余；只取 3 个互不相同的字母即可保证找到答案。  
- **下次类似题的第一步**：先**分析局部约束**（本题是左右不相同），然后**设计一次遍历的贪心填充**，避免全局搜索。