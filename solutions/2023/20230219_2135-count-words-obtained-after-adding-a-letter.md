# #2135. **在添加一个字母后可得到的单词计数** / Count Words Obtained After Adding a Letter

> 难度：中等 · 标签：Array、Hash Table、String、Bit Manipulation、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-words-obtained-after-adding-a-letter/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed arrays of strings startWords and targetWords. Each string consists of lowercase English letters only.
For each string in targetWords, check if it is possible to choose a string from startWords and perform a conversion operation on it to be equal to that from targetWords.
The conversion operation is described in the following two steps:
Return the number of strings in targetWords that can be obtained by performing the operations on any string of startWords.
Note that you will only be verifying if the string in targetWords can be obtained from a string in startWords by performing the operations. The strings in startWords do not actually change during this process.

**Examples**

**Example 1:**

```
Input: startWords = ["ant","act","tack"], targetWords = ["tack","act","acti"]
Output: 2
Explanation:
- In order to form targetWords[0] = "tack", we use startWords[1] = "act", append 'k' to it, and rearrange "actk" to "tack".
- There is no string in startWords that can be used to obtain targetWords[1] = "act".
  Note that "act" does exist in startWords, but we must append one letter to the string before rearranging it.
- In order to form targetWords[2] = "acti", we use startWords[1] = "act", append 'i' to it, and rearrange "acti" to "acti" itself.
```

**Example 2:**

```
Input: startWords = ["ab","a"], targetWords = ["abc","abcd"]
Output: 1
Explanation:
- In order to form targetWords[0] = "abc", we use startWords[0] = "ab", add 'c' to it, and rearrange it to "abc".
- There is no string in startWords that can be used to obtain targetWords[1] = "abcd".
```

**Constraints**

- 1 <= startWords.length, targetWords.length <= 5 * 104
- 1 <= startWords[i].length, targetWords[j].length <= 26
- Each string of startWords and targetWords consists of lowercase English letters only.
- No letter occurs more than once in any string of startWords or targetWords.

---

## 题目（中文翻译）

你得到两个下标从 0 开始的字符串数组 `startWords` 和 `targetWords`。每个字符串仅由小写英文字母组成。  
对于 `targetWords` 中的每个字符串，判断是否可以从 `startWords` 中选择一个字符串并对其执行以下**转换操作**，使其等于该 `targetWords` 中的字符串。

**转换操作**分两步进行：

1. 向选中的 `startWords` 中的字符串**添加**（append）恰好一个字母；
2. 对得到的字符串**重新排列**（rearrange）字符顺序，使其与目标字符串相同。

返回能够通过对任意 `startWords` 中的字符串执行上述操作而得到的 `targetWords` 中的字符串的数量。

> 注意：这里只是验证 `targetWords` 中的字符串是否可以由 `startWords` 中的某个字符串通过上述操作得到，`startWords` 本身在整个过程并不会真的改变。

---

### 示例

#### 示例 1
```text
Input: startWords = ["ant","act","tack"], targetWords = ["tack","act","acti"]
Output: 2
Explanation:
- 为了得到 targetWords[0] = "tack"，我们使用 startWords[1] = "act"，向其追加字母 'k'，得到 "actk"，再将其重新排列为 "tack"。
- 没有任何 startWords 中的字符串能够得到 targetWords[1] = "act"。虽然 "act" 本身已经存在于 startWords 中，但必须向字符串中**追加**一个字母后才能进行匹配。
```

#### 示例 2
```text
Input: startWords = ["ab","a"], targetWords = ["abc","abcd"]
Output: 1
Explanation:
- 为了得到 targetWords[0] = "abc"，我们使用 startWords[0] = "ab"，添加字母 'c' 后得到 "abc"，无需再重新排列。
- 没有任何 startWords 中的字符串能够得到 targetWords[1] = "abcd"。
```

---

### 约束条件

- `1 <= startWords.length, targetWords.length <= 5 * 10^4`
- `1 <= startWords[i].length, targetWords[j].length <= 26`
- `startWords` 和 `targetWords` 中的每个字符串仅由小写英文字母组成。
- 任意字符串内部的字母不会出现重复。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个 `targetWords` 的单词都和 `startWords` 中的每个单词逐一比较**。  
比较的过程可以拆成两步：

1. **在 `startWords` 的单词后面随意加一个字母**（只加一个，不能删或换）。  
2. **把加完字母后的单词随意重新排列**（即把字母顺序打乱），看能否得到目标单词。

> **类比**：想象 `startWords` 里的单词是一本字典，每翻一页（一个单词），我们往后面贴一张字母卡，然后把整页的字母全部打乱，看看能不能拼出 `targetWords` 里的一页。

因为每个单词的长度最多只有 26，**我们可以直接枚举所有可能的加字母方式**，然后把得到的字符集合（即重新排列后的结果）和目标单词比较是否相同。

**为什么能得到正确答案**  
- 只要我们尝试了所有 `startWords` + “任意一个字母” 的组合，并把字母排序（或用其它方式把字符集合统一表示），就一定会覆盖所有合法的转换方式。
- 若某个目标单词能够被得到，那么必定会在我们的枚举中出现一次相同的字符集合，于是我们可以计数。

**复杂度分析（大白话）**  
- 对每个 `targetWords`（设有 `m` 个），我们要遍历所有 `startWords`（设有 `n` 个），并且对每个 `startWords` 再尝试加 **26** 个可能的字母。  
- 每一次尝试都要把字符排序（长度 ≤ 27），这一步可以看作是常数时间。  

所以总体时间是 `O(m * n * 26)`，在最坏情况下约等于 `O(m * n)`，但因为 `m`、`n` 最多都有 `5·10⁴`，这会导致 **约 2.5×10⁹ 次操作**，远远超出 1 秒的限制，根本不可行。  

空间上我们只需要保存输入的两个列表，额外再开几个临时字符串，空间复杂度是 `O(1)`（不计输入）。

#### 代码（Python）

```python
from typing import List

def brute_force(startWords: List[str], targetWords: List[str]) -> int:
    cnt = 0
    for t in targetWords:                     # 遍历每个目标单词
        found = False
        for s in startWords:                  # 与每个起始单词比对
            if len(s) + 1 != len(t):          # 必须只多一个字母，长度不符直接跳过
                continue
            # 把 s 的字母放进集合，再尝试加入 t 中多出的那个字母
            for ch in 'abcdefghijklmnopqrstuvwxyz':   # 枚举要添加的字母
                cand = sorted(s + ch)          # 加完字母后把字符排好序，等价于“任意重新排列”
                if cand == sorted(t):          # 与目标单词的排好序的字符比较
                    found = True
                    break
            if found:
                break
        if found:
            cnt += 1
    return cnt
```

> **关键行中文注释**  
> - `for t in targetWords:`：遍历每个要检查的单词。  
> - `if len(s) + 1 != len(t): continue`：只可能把 `s` 加一个字母后长度才等于 `t`，不满足直接跳过。  
> - `for ch in 'abcdefghijklmnopqrstuvwxyz':`：枚举可以添加的 26 个小写字母。  
> - `cand = sorted(s + ch)`：把加完字母后的字符排序，等价于“任意重新排列”。  
> - `if cand == sorted(t):`：如果排序后相等，说明可以得到目标单词。

#### 复杂度

- **时间复杂度**：`O(m * n * 26)`，约等于 `O(m * n)`。  
  - 这里的 `O(m * n)` 代表“对每个目标单词都要检查所有起始单词”，在最坏情况下会非常慢。  
- **空间复杂度**：`O(1)`（不计输入），只用了几个临时变量。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **“重复检查相同的字符集合”**。  
观察题目可以发现：

1. **字母不重复**：每个单词里所有字母都是唯一的（题目限制），这让我们可以用 **位掩码（bit mask）** 把一个单词唯一地表示出来。  
   - 把字母 `'a'` 当作第 0 位，`'b'` 当作第 1 位，…… `'z'` 当作第 25 位。  
   - 单词 `"act"` 对应的掩码是 `1<<0 | 1<<2 | 1<<19`。  
   - 两个单词只要掩码相同，就说明它们的字符集合相同（不管顺序如何）。

2. **只需要判断 “能否通过添加一个字母得到”**：  
   - 对于目标单词 `t`，把它的掩码记作 `mask_t`。  
   - 如果我们从 `mask_t` 中 **去掉** 某一位（对应去掉一个字母），得到的子掩码正好在 `startWords` 的掩码集合里，则说明 `t` 可以由对应的起始单词通过“加一个字母 + 任意排列”得到。

基于这两个观察，**只需要一次遍历**：

- 把所有 `startWords` 转成掩码，放进 **哈希表**（Python 的 `set`），相当于“一本只记录字符集合的字典”。  
- 对每个 `targetWords`，尝试把它的掩码的每一位都去掉一次，检查去掉后得到的子掩码是否在集合中。只要有一次匹配成功，就计数。

> **类比**：把每个单词想成一本装有 26 张卡片的抽屉，卡片上写着出现的字母。`startWords` 的抽屉里只放了原始卡片集合。要检查 `targetWords` 能否从某个抽屉里“再加一张卡片”，我们只需要把目标抽屉里的一张卡片拿走，看看剩下的卡片是否正好和某个原始抽屉相同。

#### 代码（Python）

```python
from typing import List

def countWords(startWords: List[str], targetWords: List[str]) -> int:
    """
    最优解：使用位掩码 + 哈希集合
    """
    # 1️⃣ 把 startWords 转成掩码，放进集合
    start_set = set()
    for w in startWords:
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - ord('a'))   # 把字母对应的位设为 1
        start_set.add(mask)                     # 同样字符集合的不同排列会得到相同的 mask

    ans = 0
    # 2️⃣ 检查每个 targetWords 是否可以由某个 startWord 通过“加一字母”得到
    for w in targetWords:
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - ord('a'))

        # 尝试把目标单词的每一位都去掉一次，看是否能匹配到 start_set
        for ch in w:
            sub_mask = mask ^ (1 << (ord(ch) - ord('a')))   # 把该字母对应的位翻转成 0
            if sub_mask in start_set:                      # 哈希集合 O(1) 查找
                ans += 1
                break   # 只要找到一种可能，就算成功，继续下一个目标单词

    return ans
```

> **关键行中文注释**  
> - `mask |= 1 << (ord(ch) - ord('a'))`：把当前字母对应的第 `k` 位设为 1，构造位掩码。  
> - `start_set.add(mask)`：把每个起始单词的字符集合放进哈希集合，去重并提供 O(1) 查询。  
> - `sub_mask = mask ^ (1 << (ord(ch) - ord('a')))`：把目标单词的某个字母位翻转成 0，即“去掉这一个字母”。  
> - `if sub_mask in start_set:`：如果去掉后得到的子集合恰好在起始集合里，说明可以通过加这个字母得到目标单词。

#### 复杂度

- **时间复杂度**：`O(N + M * L)`  
  - `N = len(startWords)`，把所有起始单词转成掩码只需要遍历一次，每个单词最长 26，实际是 `O(N * 26) ≈ O(N)`。  
  - 对每个目标单词 `w`（共 `M` 个），我们遍历它的每个字符（至多 26）并在集合中做 O(1) 查找，故是 `O(M * 26) ≈ O(M)`。  
  - 整体是线性级别，远快于暴力的 `O(N*M)`。

- **空间复杂度**：`O(N)`  
  - 只额外存储 `start_set`，其中最多有 `N` 个不同的掩码（每个掩码是一个 32 位整数），相当于几乎不占额外内存。

---

## 心得

- **核心技巧**：利用 **位掩码** 把不含重复字母的字符串唯一映射为整数，再配合 **哈希集合** 实现 O(1) 的存在性检查。  
- **适用的题型**  
  1. “判断两个字符串是否只差一个字符” 类似题（如 LeetCode 2451）。  
  2. “判断子集/超集关系的快速判定” 题目（如字母集合的包含关系）。  
  3. “字符集合唯一表示” 的各种变形（如判断两个单词是否为同构词、是否可以通过一次置换得到等）。  
- **一句话总结**：**把“字符集合”压成整数，用集合快速匹配，省去所有排列的枚举**。

---

## 反思

- **第一反应**：看到“添加一个字母后可以任意重新排列”，我立刻想到把字符串排序后比较，结果想到暴力枚举每个可能的添加字母。  
- **最容易踩的坑**  
  1. **重复字母**：如果题目没有说明不含重复字母，位掩码就不再唯一，需要改用计数数组或多位表示。  
  2. **边界条件**：目标单词长度恰好比起始单词长 1 时才可能成功，长度差大于 1 必然不可能。  
  3. **集合去重**：`startWords` 中可能出现相同字符集合的不同排列，需要在放入集合前去重，否则会多余计数。  
- **下次遇到同类题**：**第一步就把每个单词转成位掩码或计数向量**，把“字符集合相等/包含”这类判定转化为整数的位运算或数组比较，这样可以立刻得到 O(1) 的查找效率，避免暴力枚举。