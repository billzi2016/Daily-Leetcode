# #2042. 检查句子中的数字是否递增 / Check if Numbers Are Ascending in a Sentence

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/check-if-numbers-are-ascending-in-a-sentence/)

---

## 题目（英文原版）

**Description**

A sentence is a list of tokens separated by a single space with no leading or trailing spaces. Every token is either a positive number consisting of digits 0-9 with no leading zeros, or a word consisting of lowercase English letters.
Given a string s representing a sentence, you need to check if all the numbers in s are strictly increasing from left to right (i.e., other than the last number, each number is strictly smaller than the number on its right in s).
Return true if so, or false otherwise.

**Examples**

**Example 1:**

```
Input: s = "1 box has 3 blue 4 red 6 green and 12 yellow marbles"
Output: true
Explanation: The numbers in s are: 1, 3, 4, 6, 12.
They are strictly increasing from left to right: 1 < 3 < 4 < 6 < 12.
```

**Example 2:**

```
Input: s = "hello world 5 x 5"
Output: false
Explanation: The numbers in s are: 5, 5. They are not strictly increasing.
```

**Example 3:**

```
Input: s = "sunset is at 7 51 pm overnight lows will be in the low 50 and 60 s"
Output: false
Explanation: The numbers in s are: 7, 51, 50, 60. They are not strictly increasing.
```

**Constraints**

- 3 <= s.length <= 200
- s consists of lowercase English letters, spaces, and digits from 0 to 9, inclusive.
- The number of tokens in s is between 2 and 100, inclusive.
- The tokens in s are separated by a single space.
- There are at least two numbers in s.
- Each number in s is a positive number less than 100, with no leading zeros.
- s contains no leading or trailing spaces.

---

## 题目（中文翻译）

**描述**  
一句话（sentence）是一串以单个空格分隔的标记（token），且不含首尾空格。每个标记要么是由数字 0‑9 组成的正整数（不含前导零），要么是仅由小写英文字母组成的单词。  
给定表示一句话的字符串 `s`，请判断 `s` 中出现的所有数字是否严格递增，即从左到右依次出现的每个数字都严格小于其右侧的数字（最后一个数字除外）。  

返回 `true` 表示满足条件，返回 `false` 表示不满足。

**示例**  

示例 1  
```
Input: s = "1 box has 3 blue 4 red 6 green and 12 yellow marbles"
Output: true
Explanation: s 中的数字为 1、3、4、6、12。它们严格递增：1 < 3 < 4 < 6 < 12。
```

示例 2  
```
Input: s = "hello world 5 x 5"
Output: false
Explanation: s 中的数字为 5、5。它们不严格递增。
```

示例 3  
```
Input: s = "sunset is at 7 51 pm overnight lows will be in the low 50 and 60 s"
Output: false
Explanation: s 中的数字为 7、51、50、60。它们不严格递增。
```

**约束条件**  

- `3 <= s.length <= 200`  
- `s` 仅由小写英文字母、空格和数字 `0-9` 组成。  
- `s` 中的标记数量在 `[2, 100]` 之间。  
- 标记之间仅有单个空格分隔。  
- `s` 至少包含两个数字。  
- 每个数字都是小于 `100` 的正整数，且不含前导零。  
- `s` 不含首尾空格。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把句子 **按空格切成一个个 token**（单词或数字），随后遍历这些 token：

1. 判断当前 token 是不是数字。  
   - 在 Python 中，字符串的 `isdigit()` 方法会检查所有字符是否都是数字，类似于我们在生活中把每个字符当作“字母卡片”，只要全是数字卡片就算是数字。  
2. 如果是数字，就把它转成整数（`int(token)`），和前一个出现的数字做比较。  
   - 第一次出现的数字没有前一个可比，直接记下来。  
   - 之后每出现一个数字，都要检查 **前一个数字 < 当前数字**，如果不成立直接返回 `False`。  
3. 遍历结束后，所有数字都满足严格递增，返回 `True`。

> 为什么这个方法一定正确？  
> 因为我们严格按照题目要求的“从左到右依次比较每两个相邻的数字”，没有遗漏也没有多余的比较。

**时间/空间复杂度**  
- **时间**：我们只遍历一次句子中的每个 token，时间随 token 数量线性增长，用大写的 **O(n)** 表示。这里的 *n* 可以理解为“句子里单词/数字的总个数”。  
- **空间**：只用了常数个额外变量（上一个数字、当前数字等），不随输入大小增长，用 **O(1)** 表示。

#### 代码（Python）

```python
def areNumbersAscending(s: str) -> bool:
    """
    暴力思路：逐个 token 判断并比较
    """
    prev_num = -1               # 用 -1 代表“还没有出现数字”
    for token in s.split():     # 按空格切分得到每个 token
        if token.isdigit():     # 判断是否全是数字（数字卡片全部是 0-9）
            cur = int(token)    # 把数字字符串转成整数
            # 前一个数字必须严格小于当前数字
            if cur <= prev_num: # 如果不满足递增，直接返回 False
                return False
            prev_num = cur       # 更新最近出现的数字
    # 所有数字都满足递增
    return True
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次句子里的 token，n 越大花的时间线性增长。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，和输入长度无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈并不在遍历本身**，而是我们已经在一次遍历里完成了所有必要的比较。  
因此，这已经是最优的线性解法，无法再把时间降低到 `O(log n)` 或 `O(1)`（因为必须检查所有数字）。  
这里的“最优”体现在：

- **一次遍历**（单次扫描）即可完成任务。  
- **不需要额外的数据结构**（比如列表、哈希表），只用两个整数变量。

如果把思路写得更“算法化”，可以说我们在使用 **“滑动窗口”** 的思想：窗口只保存最近出现的一个数字，随着扫描向右移动，不断比较并更新窗口。

下面给出同样的实现，只是把变量名写得更直观，并加上更细致的注释，帮助初学者把 “滑动窗口” 的概念落到实际代码上。

#### 代码（Python）

```python
def areNumbersAscending(s: str) -> bool:
    """
    最优解：一次扫描 + 滑动窗口（只保存上一个数字）
    """
    last = -1                     # 窗口左端：上一个出现的数字，初始为 -1 表示“空”
    for word in s.split():        # 把句子切成 token（单词/数字）
        # 只关心全是数字的 token
        if word.isdigit():
            cur = int(word)       # 把当前数字字符串转成整数
            # 如果当前数字不大于上一个数字，递增关系被破坏
            if cur <= last:
                return False
            last = cur            # 窗口右端移动到当前数字
    return True
```

#### 复杂度

- **时间复杂度**：`O(n)` — 仍然是一趟扫描，n 为 token 的数量。相比暴力解没有额外开销，已经是最优。  
- **空间复杂度**：`O(1)` — 只用了常数个整数变量（`last`、`cur`），不随输入规模增长。

---

## 心得

- **核心技巧**：一次遍历 + “滑动窗口” 思想（只保存上一次出现的数字），配合字符串的 `split()` 与 `isdigit()` 完成判定。  
- **适用的题型**  
  1. 检查序列是否单调递增/递减（如 “判断数组是否严格递增”）。  
  2. 验证字符流中某类元素是否满足特定顺序（如 “检查句子中所有大写字母是否按字典序排列”。）  
  3. 简单的“相邻元素比较”问题（如 “判断一段文字里出现的年份是否递增”。）  
- **解题钥匙**：**只保留必要的状态**（这里是上一个数字），避免额外的存储和多余的遍历。

## 反思

- **第一反应**：把句子拆成单词，逐个判断是不是数字，然后比较大小。  
- **最容易踩的坑**  
  - 忽略了题目要求的“严格递增”，只检查“不小于”会导致错误。  
  - 没有考虑数字前可能出现的字母或标点（本题已保证只有空格分隔），但在实际面试中要先确认输入规范。  
  - `isdigit()` 对空字符串返回 `False`，但若自行实现判断时要防止空 token 导致异常。  
- **下次遇到同类题**，第一步应想到 **“一次遍历 + 只保留上一次的关键状态”**，这样既能保证正确性，又能做到最优的时间/空间复杂度。