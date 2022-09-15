# #1935. 可输入的最大单词数 / Maximum Number of Words You Can Type

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-words-you-can-type/)

---

## 题目（英文原版）

**Description**

There is a malfunctioning keyboard where some letter keys do not work. All other keys on the keyboard work properly.
Given a string text of words separated by a single space (no leading or trailing spaces) and a string brokenLetters of all distinct letter keys that are broken, return the number of words in text you can fully type using this keyboard.

**Examples**

**Example 1:**

```
Input: text = "hello world", brokenLetters = "ad"
Output: 1
Explanation: We cannot type "world" because the 'd' key is broken.
```

**Example 2:**

```
Input: text = "leet code", brokenLetters = "lt"
Output: 1
Explanation: We cannot type "leet" because the 'l' and 't' keys are broken.
```

**Example 3:**

```
Input: text = "leet code", brokenLetters = "e"
Output: 0
Explanation: We cannot type either word because the 'e' key is broken.
```

**Constraints**

- 1 <= text.length <= 104
- 0 <= brokenLetters.length <= 26
- text consists of words separated by a single space without any leading or trailing spaces.
- Each word only consists of lowercase English letters.
- brokenLetters consists of distinct lowercase English letters.

---

## 题目（中文翻译）

**题目描述**

键盘出现故障，部分字母键失灵，其余所有键均正常工作。  
给定一个由单个空格分隔的单词字符串 `text`（string），以及一个包含所有失灵字母键的、不重复的字母集合 `brokenLetters`（string），返回在该键盘上能够完整输入的单词数量。

**示例**

**示例 1**

```
Input: text = "hello world", brokenLetters = "ad"
Output: 1
Explanation: 我们无法输入 "world"，因为字符 'd' 对应的键失灵。
```

**示例 2**

```
Input: text = "leet code", brokenLetters = "lt"
Output: 1
Explanation: 我们无法输入 "leet"，因为字符 'l' 和 't' 对应的键失灵。
```

**示例 3**

```
Input: text = "leet code", brokenLetters = "e"
Output: 0
Explanation: 两个单词都无法输入，因为字符 'e' 对应的键失灵。
```

**约束条件**

- `1 <= text.length <= 104`
- `0 <= brokenLetters.length <= 26`
- `text` 由单个空格分隔的单词组成，且不存在前导或尾随空格。
- 每个单词仅包含小写英文字母。
- `brokenLetters` 由不重复的小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `text` 按空格切成一个个单词，**逐个检查**这些单词里有没有出现坏掉的字母。  
- **数据结构**：我们只需要一个容器来存放坏掉的字母。最直观的办法是把 `brokenLetters` 当成一个 **列表**，遍历时逐个比较。可以把它想象成一本**字典**，我们要把每个单词的每个字母都去“查页码”。如果在字典里找到了（即该字母是坏的），这整个单词就不能打出来。  
- **正确性**：只要一个单词中出现了坏字母，就说明它无法完整输入；只有当**所有**字母都不在坏字母集合中时，才算这单词可打。把所有单词都这么检查一遍，计数即可得到答案。  

#### 代码（Python）  

```python
def canBeTyped_bruteforce(text: str, brokenLetters: str) -> int:
    # 把坏掉的字母放进列表，后面会逐个对比
    broken_list = list(brokenLetters)

    # 按空格分割成单词列表
    words = text.split(' ')

    # 统计可以完整输入的单词数
    count = 0

    # 遍历每个单词
    for w in words:
        # 假设这个单词可以输入
        can_type = True

        # 检查单词里的每个字符
        for ch in w:
            # 如果当前字符在坏字母列表里，就不能输入
            if ch in broken_list:          # O(1) 的列表查找（实际上是线性，但列表很短）
                can_type = False          # 标记为不能输入
                break                     # 立即退出当前单词的检查，省点时间

        # 如果整个单词都没有坏字母，就计数
        if can_type:
            count += 1

    return count
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - `m` 为单词的总字符数（`text` 长度），`n` 为 `brokenLetters` 的长度（最多 26）。  
  - 大白话：我们要把每个字符都和坏字母表里的每个字母比较一次，最坏情况下要比较 26 次。  
- **空间复杂度**：`O(n)`  
  - 只用了一个列表保存坏字母，最多 26 个字符，算是常数级空间。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于：每检查一个字符，都要在列表里遍历一次寻找是否是坏字母。虽然 `brokenLetters` 最多只有 26 个，但我们完全可以把查找操作降到 **O(1)**，即“一眼就能判断”。这正是 **哈希表**（在 Python 中用 `set`）擅长的事。  

**优化步骤**  

1. **把坏字母装进集合**  
   - 集合的查找时间是常数级（`O(1)`），相当于把字典的“词条”直接映射到“页码”，一查即得。  
2. **逐词、逐字符检查**  
   - 和暴力思路一样遍历单词，但这次每遇到一个字符，只需要 `if ch in broken_set`，时间是常数。  
3. **计数**  
   - 与之前相同，只要整词没有出现坏字母，就计数。  

> **类比**：把坏字母列表想象成一本**电话簿**（查找需要逐页翻），而集合则是**手机通讯录**（直接点开联系人），查找快多了。  

#### 代码（Python）  

```python
def canBeTyped_optimal(text: str, brokenLetters: str) -> int:
    # 把坏字母放进集合，查找速度是 O(1)
    broken_set = set(brokenLetters)      # 如同把所有坏键记在一本“坏键清单”

    # 按空格切分得到每个单词
    words = text.split(' ')

    # 计数可打的单词数量
    count = 0

    # 逐个检查单词
    for w in words:
        # 使用 Python 的 all()：只有当所有字符都不在坏集合中时才返回 True
        if all(ch not in broken_set for ch in w):
            count += 1                    # 这单词可以完整输入

    return count
```

#### 复杂度  

- **时间复杂度**：`O(m)`  
  - 只遍历 `text` 中的每个字符一次，查找坏字母是常数时间。  
  - 与暴力解相比，省去了每次字符都遍历 26 次的开销。  
- **空间复杂度**：`O(n)`  
  - 只多用了一个集合保存坏字母，最多 26 个字符，仍然是常数级空间。  

---

## 心得  

- **核心技巧**：利用 **集合（哈希表）** 实现 O(1) 的成员判定。  
- **适用场景**：  
  1. 判断字符串中是否出现指定字符集合（如 “不允许的字符”）。  
  2. 统计数组中是否包含某些目标值（如 “两个数组的交集”）。  
  3. 检查单词是否全部由合法字符组成（如 “密码合法性检测”）。  
- **一句话总结**：把“要查的东西”放进集合，一查即中，避免重复遍历。

## 反思  

- **第一反应**：把句子拆成单词，然后逐字检查是否有坏键。  
- **最容易踩的坑**：  
  - 忽略了 **空格分割** 的细节，导致首尾可能出现空字符串。  
  - 对 `brokenLetters` 直接使用 `in` 判断时，如果使用列表会导致额外的线性查找，影响效率。  
- **下次类似题的第一步**：先把“需要快速判断是否存在的元素”放进 `set`，再遍历主数据结构进行判定。