# #1961. 检查字符串是否为数组的前缀 / Check If String Is a Prefix of Array

> 难度：简单 · 标签：Array、Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/check-if-string-is-a-prefix-of-array/)

---

## 题目（英文原版）

**Description**

Given a string s and an array of strings words, determine whether s is a prefix string of words.
A string s is a prefix string of words if s can be made by concatenating the first k strings in words for some positive k no larger than words.length.
Return true if s is a prefix string of words, or false otherwise.

**Examples**

**Example 1:**

```
Input: s = "iloveleetcode", words = ["i","love","leetcode","apples"]
Output: true
Explanation:
s can be made by concatenating "i", "love", and "leetcode" together.
```

**Example 2:**

```
Input: s = "iloveleetcode", words = ["apples","i","love","leetcode"]
Output: false
Explanation:
It is impossible to make s using a prefix of arr.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 20
- 1 <= s.length <= 1000
- words[i] and s consist of only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个字符串数组 `words`，判断 `s` 是否是 `words` 的前缀字符串。  
如果存在正整数 `k（k ≤ words.length）`，使得将 `words` 的前 `k` 个字符串依次拼接后得到的字符串恰好等于 `s`，则称 `s` 为 `words` 的前缀字符串。  

返回 `true` 表示 `s` 是前缀字符串，返回 `false` 表示不是。

## 示例

### 示例 1
**输入**: `s = "iloveleetcode", words = ["i","love","leetcode","apples"]`  
**输出**: `true`  
**解释**:  
`s` 可以通过拼接 `"i"`, `"love"` 和 `"leetcode"` 得到。

### 示例 2
**输入**: `s = "iloveleetcode", words = ["apples","i","love","leetcode"]`  
**输出**: `false`  
**解释**:  
无法仅使用 `words` 的前缀来组成 `s`。

## 约束条件
- `1 <= words.length <= 100`
- `1 <= words[i].length <= 20`
- `1 <= s.length <= 1000`
- `words[i]` 和 `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把数组的前缀全部拼出来**，然后看 `s` 是否正好等于其中的某一个。  
可以把「前缀」想象成一本书的目录：目录的每一项都是从书的第一章开始，依次累加章节标题得到的字符串。  
- **数据结构**：我们只需要一个普通的字符串变量 `cur` 来保存当前拼接得到的前缀。相当于在写字典时，每查到一个词就把它的解释写在后面，形成更长的解释。
- **正确性**：题目要求 `s` 能由数组前 `k`（`k≥1`）个单词依次拼接得到。遍历 `words` 时，`cur` 正好是第 `1,2,…,k` 个单词的拼接结果，只要有一次 `cur == s`，说明找到了合乎条件的 `k`，返回 `True` 即可。遍历结束仍未相等，则说明不存在这样的 `k`，返回 `False`。

#### 代码（Python）

```python
def isPrefixString(s: str, words: list[str]) -> bool:
    # cur 用来累计前缀字符串，初始为空
    cur = ""
    for w in words:
        cur += w               # 把当前单词接到已有前缀后面
        if cur == s:           # 完全相等 → 找到答案
            return True
        # 如果已经超过 s 的长度，就不可能再相等了
        if len(cur) > len(s):
            break
    return False               # 循环结束仍未匹配
```

#### 复杂度  

- **时间复杂度**：`O(L)`，其中 `L` 为 `words` 前缀累计的字符总数，最坏情况等于 `s` 的长度（不超过 1000）。直观上可以理解为「我们最多只需要看每个字符一次」。
- **空间复杂度**：`O(1)`（不计返回值），只用了常数个额外变量 `cur`、`w`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

在「暴力」解法里，我们已经是 **一次遍历** 并且 **即时比较**，已经达到了线性时间。  
所谓「最优」其实是**在遍历过程中提前剪枝**：  
- 当累计的前缀长度已经超过 `s` 时，后面的单词再加也不可能让前缀回到 `s`，可以立刻停止循环。  
- 同时，在每次拼接后立刻比较 `cur` 与 `s`，一旦相等立即返回，避免继续无意义的遍历。

这一步剪枝把不必要的计算彻底剔除，使得最坏情况下仍然只遍历到 `s` 的长度。核心工具仍然是 **字符串拼接**（相当于「指针」在原数组上前进），没有额外的数据结构。

#### 代码（Python）

```python
def isPrefixString(s: str, words: list[str]) -> bool:
    prefix = ""                     # 用来保存当前已经拼好的前缀
    for word in words:
        prefix += word              # 把下一个单词接在后面

        # 1️⃣ 若前缀已经等于 s，直接返回 True
        if prefix == s:
            return True

        # 2️⃣ 若前缀长度已经超过 s，后面再加只会更长，直接退出循环
        if len(prefix) > len(s):
            break

    # 循环结束仍未匹配，说明 s 不是任何前缀
    return False
```

#### 复杂度  

- **时间复杂度**：`O(|s|)`，只遍历到 `s` 的长度（最多 1000），比「暴力」的 `O(L)` 更明确地指明上界。  
- **空间复杂度**：`O(1)`，只使用了常数级别的额外空间。

---

## 心得

- **核心技巧**：**一次遍历 + 逐步构造前缀**，在构造的过程中即时比较并提前剪枝。  
- **适用场景**：  
  1. 判断一个字符串是否为若干子串的**连续拼接**（如「检查句子是否由单词列表组成」）。  
  2. 需要在数组/字符串序列中寻找**前缀匹配**的情形（如「前缀和」问题的简化版）。  
- **解题钥匙**：**“边走边比”**——遍历时同步构造并比较，一旦发现不可能再匹配就立即停止。

## 反思

- **第一反应**：把所有前缀都拼出来放进列表再比较，感觉最直接。  
- **最容易踩的坑**：  
  - 忘记在前缀长度已经超过 `s` 时提前退出，导致不必要的遍历。  
  - 没有考虑 `k` 必须为正整数（即空前缀不算），所以一开始不能直接返回 `s == ""`。  
- **下次遇到同类题**：第一步就想到 **“从左到右逐步累加并实时比较”**，把「是否匹配」的判断嵌进遍历循环里。