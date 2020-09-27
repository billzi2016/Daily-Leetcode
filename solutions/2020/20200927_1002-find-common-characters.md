# #1002. 找出共同字符 / Find Common Characters

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/find-common-characters/)

---

## 题目（英文原版）

**Description**

Given a string array words, return an array of all characters that show up in all strings within the words (including duplicates). You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: words = ["bella","label","roller"]
Output: ["e","l","l"]
```

**Example 2:**

```
Input: words = ["cool","lock","cook"]
Output: ["c","o"]
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个字符串数组（string array）`words`，返回一个字符数组，包含所有在 `words` 中每个字符串里都出现的字符（包括重复出现的字符）。返回结果的顺序可以任意。

**示例 1**  
输入: `words = ["bella","label","roller"]`  
输出: `["e","l","l"]`

**示例 2**  
输入: `words = ["cool","lock","cook"]`  
输出: `["c","o"]`

**约束条件**  

- `1 <= words.length <= 100`  
- `1 <= words[i].length <= 100`  
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个检查每个字符**是否在所有单词里都出现过。  
可以把每个字符想象成一本字典里的“词条”，我们要把这本字典的每一页（即每个字符）都翻一遍，看看它在不在每本书（每个单词）里都有出现。

实现步骤：

1. 任选一个单词（比如第一个），把它的每个字符依次取出来。  
2. 对于当前字符 `c`，遍历剩下的所有单词，统计 `c` 在每个单词里出现的次数。  
3. 只要有哪本书里没有 `c`，或者出现次数比已经记录的次数更少，就把 `c` 从答案里剔除或只保留最小的出现次数。  
4. 把所有满足条件的字符（包括重复的）放进结果列表。

为什么正确？  
只要一个字符在 **所有** 单词里出现了至少 `k` 次，那么它一定会在我们遍历的每一本书里都被计数 `k` 次。我们取每本书里出现次数的最小值，就恰好是该字符能在答案中出现的最大次数（包括重复）。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def commonChars_bruteforce(words: List[str]) -> List[str]:
    # 1️⃣ 选第一个单词作为基准，统计它每个字符出现的次数
    base_counter = Counter(words[0])          # Counter 就像“词典”，key 是字符，value 是出现次数

    # 2️⃣ 用一个字典保存所有字符在所有单词里的最小出现次数
    min_counts = dict(base_counter)           # 先把基准单词的计数拷贝过去

    # 3️⃣ 从第二个单词开始，逐个更新最小次数
    for w in words[1:]:
        cur_counter = Counter(w)              # 当前单词的字符计数
        for ch in min_counts.keys():          # 只遍历已经出现过的字符
            # 取当前单词和之前记录的最小值
            min_counts[ch] = min(min_counts[ch], cur_counter.get(ch, 0))
            # cur_counter.get(ch, 0) → 如果当前单词里没有 ch，就返回 0

    # 4️⃣ 把字符按照最小次数展开成列表
    result = []
    for ch, cnt in min_counts.items():
        result.extend([ch] * cnt)              # 把字符重复 cnt 次加入结果
    return result
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  - `m` 为单词数量，`n` 为每个单词的平均长度。  
  - 我们对每个单词都遍历一次，统计字符出现次数（`Counter` 需要遍历字符），所以整体是“单词数 × 单词长度”。  
  - 用大白话说，假设有 10 本书，每本书有 100 页，那么我们大约要翻 1000 页。

- **空间复杂度**：`O(1)`（严格来说是 `O(26)`）  
  - 我们只用到固定大小的计数表（字母表只有 26 个小写字母），不随输入规模增长。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **对每个字符都要遍历所有单词**，虽然已经是 `O(m·n)`，但我们可以把“遍历字符”这一步合并进计数过程，使代码更简洁、常数因子更小。

**关键点**：  
- 每个单词只需要一次遍历，就能得到它所有字符的出现次数。  
- 对所有单词的计数表取**逐位最小值**（对应同一个字符的计数），即可得到该字符在所有单词中出现的最小次数——这正是答案需要的重复次数。

这一步可以用 **长度为 26 的数组** 来实现，数组下标 `0~25` 分别对应字母 `'a'~'z'`。数组就像 26 个小盒子，每个盒子里装的是对应字母在当前单词里出现了多少次。

实现步骤：

1. 初始化一个长度为 26 的数组 `global_min`，全部填入一个很大的数（比如 `inf`），表示“目前还不知道最小次数”。  
2. 对每个单词：  
   - 建立一个长度为 26 的临时数组 `cnt`，遍历单词的字符，把对应盒子里的数字加 1。  
   - 把 `global_min[i]` 更新为 `min(global_min[i], cnt[i])`，即保留到目前为止的最小值。  
3. 最后遍历 `global_min`，把下标 `i` 对应的字符重复 `global_min[i]` 次加入答案列表。

为什么正确？  
因为 `global_min[i]` 记录的是 **所有单词里第 `i` 个字母出现次数的最小值**，只有当每本书都至少出现一次（即最小值 ≥ 1）时，这个字母才会出现在答案里；出现多少次就恰好是最小值本身。

#### 代码（Python）

```python
from typing import List

def commonChars_optimal(words: List[str]) -> List[str]:
    # 1️⃣ 初始化全局最小计数为一个很大的数（这里用 101 > 所有单词长度上限）
    global_min = [101] * 26                     # 26 个盒子，对应 'a'~'z'

    # 2️⃣ 对每个单词统计出现次数并更新全局最小值
    for w in words:
        cnt = [0] * 26                           # 当前单词的计数盒子
        for ch in w:
            idx = ord(ch) - ord('a')             # 把字符转成 0~25 的下标
            cnt[idx] += 1                        # 把对应盒子里的数字加 1
        # 把每个字母的最小次数取出来
        for i in range(26):
            if cnt[i] < global_min[i]:
                global_min[i] = cnt[i]

    # 3️⃣ 根据最小次数生成答案列表
    result = []
    for i, times in enumerate(global_min):
        if times > 0:                            # 只保留出现过的字母
            result.extend([chr(i + ord('a'))] * times)
    return result
```

#### 复杂度

- **时间复杂度**：`O(m * n + 26 * m)` → 简化为 `O(m * n)`  
  - 每个单词只遍历一次，统计字符（`O(n)`），随后遍历 26 次常数大小的数组（`O(26)`），所以整体仍是“单词数 × 单词长度”。  
  - 与暴力解相比，省去了对每个字符再次遍历所有单词的过程，常数更小。

- **空间复杂度**：`O(1)`（实际是 `O(26)`）  
  - 只用了两个固定长度为 26 的数组，不随输入规模增长。  

---

## 心得

- **核心技巧**：利用**字符计数数组（或哈希表）取最小值**，把“公共”转化为“每个位置的最小出现次数”。  
- **适用的题型**：  
  1. “找出两个数组的交集（包括重复）”  
  2. “统计所有字符串的共同子序列（字符频率版）”  
  3. “判断多个字符串是否是字母异位词的公共子集”  
- **一句话总结**：**把“所有字符串里都出现的字符”映射为“每个字符出现次数的全局最小值”。**

---

## 反思

- **第一反应**：看到“所有字符串都出现的字符”，立刻想到用**哈希表/计数器**统计每个字符的出现次数，然后取最小值。  
- **最容易踩的坑**：  
  - 忘记把 **重复字符** 的次数也算进去，只保留出现过一次的字符会导致答案缺少重复。  
  - 没有处理 **单词长度不同** 的情况，直接使用第一个单词的字符集合会遗漏后面单词里出现更多次数的字符。  
- **下次遇到同类题**：第一步先**为每个字符准备一个计数容器（长度 26 的数组）**，然后在遍历每个单词时**同步更新最小值**，这样思路清晰且避免遗漏。