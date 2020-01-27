# #748. 最短补全单词 / Shortest Completing Word

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/shortest-completing-word/)

---

## 题目（英文原版）

**Description**

Given a string licensePlate and an array of strings words, find the shortest completing word in words.
A completing word is a word that contains all the letters in licensePlate. Ignore numbers and spaces in licensePlate, and treat letters as case insensitive. If a letter appears more than once in licensePlate, then it must appear in the word the same number of times or more.
For example, if licensePlate = "aBc 12c", then it contains letters 'a', 'b' (ignoring case), and 'c' twice. Possible completing words are "abccdef", "caaacab", and "cbca".
Return the shortest completing word in words. It is guaranteed an answer exists. If there are multiple shortest completing words, return the first one that occurs in words.

**Examples**

**Example 1:**

```
Input: licensePlate = "1s3 PSt", words = ["step","steps","stripe","stepple"]
Output: "steps"
Explanation: licensePlate contains letters 's', 'p', 's' (ignoring case), and 't'.
"step" contains 't' and 'p', but only contains 1 's'.
"steps" contains 't', 'p', and both 's' characters.
"stripe" is missing an 's'.
"stepple" is missing an 's'.
Since "steps" is the only word containing all the letters, that is the answer.
```

**Example 2:**

```
Input: licensePlate = "1s3 456", words = ["looks","pest","stew","show"]
Output: "pest"
Explanation: licensePlate only contains the letter 's'. All the words contain 's', but among these "pest", "stew", and "show" are shortest. The answer is "pest" because it is the word that appears earliest of the 3.
```

**Constraints**

- 1 <= licensePlate.length <= 7
- licensePlate contains digits, letters (uppercase or lowercase), or space ' '.
- 1 <= words.length <= 1000
- 1 <= words[i].length <= 15
- words[i] consists of lower case English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `licensePlate` 和一个字符串数组 `words`，请在 `words` 中找到**最短补全单词**（shortest completing word）。  
**补全单词**的定义如下：它必须包含 `licensePlate` 中出现的所有字母（忽略数字和空格，字母不区分大小写）。如果某个字母在 `licensePlate` 中出现多次，则该字母在单词中出现的次数必须不少于该次数。

例如，`licensePlate = "aBc 12c"`，则其中包含字母 `'a'`、`'b'`（不区分大小写）以及 `'c'` 两次。可能的补全单词有 `"abccdef"`、`"caaacab"`、`"cbca"` 等。

返回 `words` 中的**最短补全单词**。题目保证一定存在答案。如果有多个长度相同的最短补全单词，返回在 `words` 中出现最早的那个。

---

### 示例

**示例 1**  
```text
Input: licensePlate = "1s3 PSt", words = ["step","steps","stripe","stepple"]
Output: "steps"
Explanation: licensePlate 包含字母 's'、'p'、's'（不区分大小写）和 't'。  
- "step" 只包含一个 's'，不满足要求。  
- "steps" 同时包含 't'、'p' 以及两个 's'，满足要求。  
- "stripe" 缺少 's'。  
- "stepple" 缺少 's'。  
因为 "steps" 是唯一满足条件的单词，故返回它。
```

**示例 2**  
```text
Input: licensePlate = "1s3 456", words = ["looks","pest","stew","show"]
Output: "pest"
Explanation: licensePlate 只包含字母 's'。所有单词都包含 's'，但长度最短的有 "pest"、"stew"、"show"。在这三个中，"pest" 在原数组中出现最早，所以返回 "pest"。
```

---

### 约束条件
- `1 <= licensePlate.length <= 7`
- `licensePlate` 只包含数字、字母（大小写任意）或空格 `' '`。
- `1 <= words.length <= 1000`
- `1 <= words[i].length <= 15`
- `words[i]` 只由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **licensePlate** 里出现的所有字母（不区分大小写）统计出来，然后把 **words** 数组里的每个单词也逐个统计字母出现的次数，比较两者是否满足“单词中的每个字母出现次数 ≥ 车牌中字母的出现次数”。  
如果满足，就说明该单词是一个 *completing word*。在所有满足条件的单词中，挑选长度最短的即可；若长度相同则返回最先出现的。

- **使用的数据结构**：  
  - **字典（Hash Table）** 用来存放字母 → 出现次数的映射。可以把它想象成一本**查字典**：键（key）是字母，值（value）是这把字母在字符串里出现了多少次。查找和插入的时间都非常快（平均 O(1)）。  
  - **列表** 用来遍历 **words**。  

- **为什么正确**：  
  - 只要单词的每个字母出现次数不小于车牌中的对应次数，说明它已经“包含”了车牌所有字母的需求。  
  - 暴力遍历会检查所有单词，保证不会错过最短的那个。  

- **时间/空间复杂度**（大白话解释）  
  - 对每个单词我们都要遍历它的字符一次，再和车牌的计数字典比较。设 `n = words 长度`，`m = 单词的最大长度（≤15）`，`k = 车牌中字母的个数（≤7）`。  
  - **时间复杂度** 大约是 `O(n * (m + k))`，因为我们要遍历所有单词并对每个单词检查所有字符。这里的 `O` 符号可以理解为“随输入规模增长的上界”，实际运行时因为 `m`、`k` 都很小，速度几乎是线性的。  
  - **空间复杂度** 只用了两个字典来保存计数，大小最多是 26（英文字母），所以是 `O(1)`（常数空间）。  

#### 代码（Python）  

```python
from collections import Counter
import string

def shortestCompletingWord_bruteforce(licensePlate: str, words):
    # 1️⃣ 统计车牌中的字母（忽略数字、空格，统一转成小写）
    plate_counter = Counter(ch.lower() for ch in licensePlate if ch.isalpha())
    # Counter 是一个字典子类，key 是字母，value 是出现次数

    best_word = None          # 用来保存当前找到的最短答案
    best_len = float('inf')   # 初始设为无限大，方便后面比较

    # 2️⃣ 逐个检查 words
    for w in words:
        # 统计当前单词的字母出现次数
        word_counter = Counter(w)
        # 3️⃣ 判断是否满足所有字母的需求
        #   all() 会遍历 plate_counter 的每个 (字母, 次数) 对
        if all(word_counter[ch] >= cnt for ch, cnt in plate_counter.items()):
            # 满足条件，看看长度是否更短
            if len(w) < best_len:
                best_word = w
                best_len = len(w)
                # 如果长度相同，保持原来的 best_word（因为它更靠前）

    return best_word
```

#### 复杂度  

- **时间复杂度**：`O(n * (m + k))`  
  - `n` 是单词数量，`m` 是每个单词的最长长度，`k` 是车牌中字母的数量。  
  - 直观上就是“遍历所有单词 + 每个单词检查一次”。  

- **空间复杂度**：`O(1)`  
  - 只用了常数大小的计数字典（最多 26 个英文字母），不随输入规模增长。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈** 并不在遍历单词本身（因为单词长度本来就很短），而在每次都重新 **统计** 单词的字母出现次数。  
我们可以把 **车牌的计数** 只算一次，然后对每个单词只做一次“字母匹配”，不必生成完整的 Counter 再比较。  

**优化步骤**  

1. **预处理车牌**：把所有字母转成小写后计数，得到 `need[26]`（长度为 26 的数组），下标 `0~25` 分别对应 `'a'~'z'`。  
2. **遍历 words**，对每个单词：  
   - 用一个长度为 26 的临时数组 `cnt[26]` 记录该单词中出现的字母次数（遍历一次单词即可）。  
   - 用 `for i in range(26): if cnt[i] < need[i]: break` 判断是否满足需求。  
   - 若满足且长度更短，就更新答案。  
3. 因为 **单词长度 ≤ 15**，即使每个单词都建立一次 26 长度的数组，整体仍然是线性时间 `O(n * m)`，空间仍是常数 `O(1)`（只用固定大小的数组）。  

**为什么更快**：  
- 省去了 `Counter` 对象的创建与哈希查找（虽然在本题数据规模不大，但这是更通用的技巧）。  
- 直接使用数组下标进行比较，CPU 对数组的访问速度更快。  

#### 代码（Python）  

```python
def shortestCompletingWord_optimal(licensePlate: str, words):
    # 1️⃣ 把车牌字母计数放到长度为 26 的数组中
    need = [0] * 26               # need[i] 表示第 i 个字母（a+i）在车牌中出现的次数
    for ch in licensePlate:
        if ch.isalpha():
            idx = ord(ch.lower()) - ord('a')
            need[idx] += 1

    answer = None                 # 当前找到的最短完成单词
    min_len = float('inf')

    # 2️⃣ 遍历每个单词
    for w in words:
        # 先排除明显不可能的：如果当前单词长度已经不比已知答案短，就不必检查
        if len(w) >= min_len:
            continue

        cnt = [0] * 26            # 统计当前单词的字母次数
        for ch in w:
            cnt[ord(ch) - ord('a')] += 1

        # 3️⃣ 检查是否满足所有需求
        ok = True
        for i in range(26):
            if cnt[i] < need[i]:  # 只要有一个字母不够，就不是完成单词
                ok = False
                break

        if ok:                    # 满足条件且更短，更新答案
            answer = w
            min_len = len(w)

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`  
  - `n` 为单词数量，`m` 为单词最大长度（≤15）。  
  - 只遍历一次车牌（常数大小），每个单词遍历一次字符并进行一次 26 次的数组比较。  

- **空间复杂度**：`O(1)`  
  - 使用固定大小的 26 元素数组两次（`need`、`cnt`），不随输入规模增长。  

与暴力解相比，**时间常数更小**，在大数据量时优势更明显；空间保持不变。  

---  

## 心得  

- **核心技巧**：字符计数（Frequency Counting） + 固定大小的数组（相当于哈希表）  
- **适用的题型**：  
  1. *找出包含所有指定字符的最短子串*（如 LeetCode 76 “Minimum Window Substring”）  
  2. *检查两个字符串是否为字母异位词*（如 LeetCode 242 “Valid Anagram”）  
  3. *找出满足字符出现次数要求的单词或句子*（如本题）  
- **一句话总结**：**把“出现次数需求”先算好，然后对每个候选只做一次线性匹配**，最短即是答案。  

---  

## 反思  

- **第一反应**：先把车牌和每个单词都转成 Counter，直接比较。  
- **最容易踩的坑**：  
  - 忽略了车牌中的数字和空格，需要过滤掉非字母字符。  
  - 大小写不统一，导致计数不匹配。  
  - 多次出现的相同字母必须满足次数要求（比如两个 `'s'`），仅检查是否出现一次会出错。  
- **下次类似题目第一步**：先把“需求”抽象成一个**固定大小的计数数组**或字典，然后用它对每个候选进行**一次线性检查**，避免重复的复杂操作。