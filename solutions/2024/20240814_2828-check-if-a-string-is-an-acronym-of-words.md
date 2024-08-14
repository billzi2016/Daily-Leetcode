# #2828. **检查字符串是否为单词的首字母缩写** / Check if a String Is an Acronym of Words

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/check-if-a-string-is-an-acronym-of-words/)

---

## 题目（英文原版）

**Description**

Given an array of strings words and a string s, determine if s is an acronym of words.
The string s is considered an acronym of words if it can be formed by concatenating the first character of each string in words in order. For example, "ab" can be formed from ["apple", "banana"], but it can't be formed from ["bear", "aardvark"].
Return true if s is an acronym of words, and false otherwise.

**Examples**

**Example 1:**

```
Input: words = ["alice","bob","charlie"], s = "abc"
Output: true
Explanation: The first character in the words "alice", "bob", and "charlie" are 'a', 'b', and 'c', respectively. Hence, s = "abc" is the acronym.
```

**Example 2:**

```
Input: words = ["an","apple"], s = "a"
Output: false
Explanation: The first character in the words "an" and "apple" are 'a' and 'a', respectively. 
The acronym formed by concatenating these characters is "aa". 
Hence, s = "a" is not the acronym.
```

**Example 3:**

```
Input: words = ["never","gonna","give","up","on","you"], s = "ngguoy"
Output: true
Explanation: By concatenating the first character of the words in the array, we get the string "ngguoy". 
Hence, s = "ngguoy" is the acronym.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 10
- 1 <= s.length <= 100
- words[i] and s consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组（array）`words` 和一个字符串（string）`s`，判断 `s` 是否为 `words` 的首字母缩写（acronym）。  
如果 `s` 可以通过按顺序拼接（concatenating）`words` 中每个字符串的首字符（first character）得到，则认为 `s` 是 `words` 的首字母缩写。  
例如，`"ab"` 可以由 `["apple", "banana"]` 形成，但不能由 `["bear", "aardvark"]` 形成。  

返回 `true` 表示 `s` 是 `words` 的首字母缩写，返回 `false` 表示不是。

---

**示例 1**

```text
Input: words = ["alice","bob","charlie"], s = "abc"
Output: true
Explanation: 单词 "alice"、"bob"、"charlie" 的首字符分别是 'a'、'b'、'c'。因此，`s = "abc"` 是首字母缩写。
```

**示例 2**

```text
Input: words = ["an","apple"], s = "a"
Output: false
Explanation: 单词 "an" 和 "apple" 的首字符分别是 'a'、'a'。将这些字符拼接得到的首字母缩写是 "aa"。因此，`s = "a"` 不是首字母缩写。
```

**示例 3**

```text
Input: words = ["never","gonna","give","up","on","you"], s = "ngguoy"
Output: true
Explanation: 按顺序拼接数组中单词的首字符得到的字符串是 "ngguoy"。因此，`s = "ngguoy"` 是首字母缩写。
```

---

**约束条件**

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 10`
- `1 <= s.length <= 100`
- `words[i]` 和 `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把 `words` 里每个单词的第一个字符全部挑出来，按照顺序拼成一个新字符串 `t`，然后把 `t` 和给定的 `s` 做一次完整的比较。  

- **用到的数据结构**：  
  - `list`（数组）保存输入的单词。  
  - `str`（字符串）保存拼接得到的首字母串。  
  - **类比**：把 `words` 想成一本字典，字典里每一页是一条单词记录，而我们只需要查每页的“标题字母”（即第一个字母），把这些标题字母排成一行，就是我们要的 “首字母缩写”。  

- **为什么正确**：  
  根据题意，`s` 是否是首字母缩写，唯一的判定标准就是 **“把每个单词的首字母顺序拼接后得到的字符串是否等于 `s`”。** 只要我们完整地把这些首字母拼出来，再做一次相等比较，就能得到答案。  

- **时间/空间复杂度**（大白话解释）：  
  - **时间**：我们需要遍历一次 `words`（最多 100 个），每个单词取第一个字符是 O(1) 的操作，最后再比较两个字符串（长度最多 100），所以整体是 **线性时间**，记作 `O(n)`，这里的 `n` 代表 `words` 的长度。可以想象成“走一遍所有单词”，时间随单词数量线性增长。  
  - **空间**：我们额外创建了一个保存首字母的字符串，长度恰好等于 `words` 的长度（最多 100），所以空间是 **线性的**，记作 `O(n)`。相当于“多准备一个和单词数等长的盒子”。  

#### 代码（Python）

```python
def isAcronym(words, s):
    """
    暴力解：把每个单词的首字符拼成一个新串，再和 s 做比较
    :param words: List[str]  单词数组
    :param s: str          待检测的缩写
    :return: bool          是否匹配
    """
    # 1. 把每个单词的第一个字符取出来，组成列表
    first_chars = [word[0] for word in words]   # word[0] 是第一个字符

    # 2. 将列表中的字符连接成一个字符串
    acronym = ''.join(first_chars)              # ''.join 把字符们连成一个整体

    # 3. 直接比较两串是否相等
    return acronym == s
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次 `words`（`n = len(words)`），再比较一次长度不超过 100 的字符串。  
- **空间复杂度**：`O(n)` —— 需要额外的字符串保存首字母，长度等于 `words` 的长度。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的耗时在于 **“把所有首字母都拼出来再比较”**。如果 `s` 与拼出的首字母串在某个位置已经不相等，我们完全可以提前结束，不必继续遍历剩下的单词。  

因此，**最优解**的思路是：**一次遍历 `words` 的同时，逐字符与 `s` 对比**。只要发现不匹配，就立刻返回 `False`；遍历结束后如果所有字符都匹配且长度相同，则返回 `True`。  

核心技巧是 **“双指针”**（两个指针分别指向 `words` 中当前单词的首字母和 `s` 中对应位置），但因为我们每次只取单词的第一个字符，实际上只需要一个指针 `i` 来遍历 `words`，并用 `i` 同时访问 `s[i]`。  

- **类比**：想象我们在检查一本书的章节标题首字母是否拼成了某个单词。我们一边读标题的首字母，一边在脑子里对照目标单词的对应字母，一旦发现不一样，就立刻把书合上，省掉后面的阅读时间。  

- **为什么更快**：在最坏情况下（全部匹配），时间仍然是 `O(n)`；但在多数实际输入里，只要出现一次不匹配，就能提前结束，平均性能会更好。  

- **数据结构**：仍然是原始的列表和字符串，只是没有额外的拼接操作，省掉了额外的空间。  

#### 代码（Python）

```python
def isAcronym_opt(words, s):
    """
    最优解：遍历时同步比较，遇到不匹配立即返回
    :param words: List[str]
    :param s: str
    :return: bool
    """
    # 1. 长度不等直接否定：缩写的长度必须恰好等于单词数
    if len(words) != len(s):
        return False

    # 2. 同时遍历 words 与 s 的每个位置
    for idx, word in enumerate(words):
        # word[0] 是当前单词的首字母，s[idx] 是目标缩写的对应字符
        if word[0] != s[idx]:
            # 一旦不相等，直接返回 False，后面的单词无需检查
            return False

    # 3. 所有位置都匹配，说明 s 正好是首字母缩写
    return True
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然只遍历一次 `words`，但在出现不匹配时可以提前结束。  
- **空间复杂度**：`O(1)` —— 没有额外的列表或字符串，只用了常数级别的变量（指针 `idx`），相当于“只在桌面上放了一支笔”。  

---

## 心得

- **核心技巧**：一次遍历同步比较（等价于双指针），避免不必要的中间结果存储。  
- **适用的题型**：  
  1. 判断两个字符串是否逐字符相等（如 LeetCode 1614 “Maximum Nesting Depth of the Parentheses” 中的逐字符检查）。  
  2. 判断数组中每个元素的某个属性拼接后是否等于目标字符串（如 “Check If All A’s Appear Before All B’s”）。  
- **解题钥匙**：**“先比较长度，再同步逐位比较，遇错即停”。**  

---

## 反思

- **第一反应**：直接把所有首字母拼成新字符串再比较——最直观但会多占用空间。  
- **最容易踩的坑**：  
  - 忘记先检查 `len(words) == len(s)`，导致后面访问 `s[idx]` 超出范围抛异常。  
  - 只比较了字符但忽略了顺序，必须保证“顺序一致”。  
- **下次遇到同类题**：第一步先 **“检查长度是否匹配”**，然后 **“同步逐位比较”**，如果不匹配立即返回。这样既安全又高效。