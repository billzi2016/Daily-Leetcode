# #3120. 统计特殊字符的数量 I / Count the Number of Special Characters I

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-special-characters-i/)

---

## 题目（英文原版）

**Description**

You are given a string word. A letter is called special if it appears both in lowercase and uppercase in word.
Return the number of special letters in word.

**Examples**

**Example 1:**

```
Input: word = "aaAbcBC"
Output: 3
Explanation:
The special characters in word are 'a' , 'b' , and 'c' .
```

**Example 2:**

```
Input: word = "abc"
Output: 0
Explanation:
No character in word appears in uppercase.
```

**Example 3:**

```
Input: word = "abBCab"
Output: 1
Explanation:
The only special character in word is 'b' .
```

**Constraints**

- 1 <= word.length <= 50
- word consists of only lowercase and uppercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `word`。如果一个字母（letter）在 `word` 中同时出现了小写（lowercase）和大写（uppercase）形式，则称其为 **特殊字符（special character）**。返回 `word` 中特殊字符的数量。

**示例 1**

**示例 2**

**示例 3**

**约束条件**

**示例**

**示例 1**  
输入: `word = "aaAbcBC"`  
输出: `3`  
解释:  
`word` 中的特殊字符有 `'a'`、`'b'` 和 `'c'`。

**示例 2**  
输入: `word = "abc"`  
输出: `0`  
解释:  
`word` 中没有字符出现大写形式。

**示例 3**  
输入: `word = "abBCab"`  
输出: `1`  
解释:  
唯一的特殊字符是 `'b'`。

**约束条件**  
- `1 <= word.length <= 50`  
- `word` 仅由小写和大写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个字符都去检查它的大小写是否同时出现**。  
我们可以把英文字母看成 52 张卡片（26 张小写 + 26 张大写），把题目给出的字符串当成一堆散乱的卡片。  
对于每一张卡片（比如 `'a'`），我们遍历整条字符串，看看是否能找到它对应的大写卡片 `'A'`；如果两张都找到了，就说明这是一张「特殊」卡片。

- **数据结构**：这里仅使用最基础的 **列表**（即字符串本身），不需要额外的哈希表或集合。  
- **正确性**：只要遍历完整个字符串，就一定能发现所有出现过的大小写配对，因而计数必然准确。  
- **时间/空间复杂度**：  
  - 时间上，我们对每个可能的字符（最多 52 种）都要 **完整扫描一次** 字符串，最坏情况是 `52 × n` 次比较（`n` 为字符串长度），这在大 O 记号里写作 **O(n·52) ≈ O(n²)**（因为 52 是常数，但在解释时可以说“每次都要遍历整个字符串”。）  
  - 空间上只用了常数个临时变量，**O(1)**。

#### 代码（Python）

```python
def countSpecialCharacters_bruteforce(word: str) -> int:
    # 记录出现过的「特殊」字符个数
    special_cnt = 0

    # 英文字母一共有 52 种，遍历小写 a~z
    for i in range(26):
        lower = chr(ord('a') + i)   # 如 'a', 'b', ...
        upper = chr(ord('A') + i)   # 如 'A', 'B', ...

        # 用两个布尔变量分别记录是否出现过小写和大写
        has_lower = False
        has_upper = False

        # 完整遍历一次 word，检查这两个字符是否出现
        for ch in word:
            if ch == lower:
                has_lower = True
            if ch == upper:
                has_upper = True

            # 两者都找到了可以提前结束内层循环
            if has_lower and has_upper:
                break

        # 同时出现则计数
        if has_lower and has_upper:
            special_cnt += 1

    return special_cnt
```

#### 复杂度

- **时间复杂度**：`O(n·52) ≈ O(n²)`  
  - 这里的 `n` 是 `word` 的长度。因为我们对每个字母都要遍历一次整个字符串，所以时间会随 `n` 的平方增长（虽然常数 52 很小，实际运行仍然很快）。
- **空间复杂度**：`O(1)`  
  - 只用了若干个计数器和布尔变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次检查都要把字符串遍历一遍**。  
我们其实可以在一次遍历中就把所有出现的字母记录下来，然后再“一次性”判断哪些字母同时出现了大小写。

这时**集合（Set）**就派上用场了：  
- 把所有出现的**小写字母**放进集合 `lower_set`，把所有出现的**大写字母**放进集合 `upper_set`。  
- 集合的查找是 **O(1)** 的（想象成一本字典，直接看页码），所以后面只需要把两套字母做交集，交集的大小就是「特殊」字母的个数。

**关键概念——集合交集**  
把 `lower_set` 看成「小写字典」，`upper_set` 看成「大写字典」。把两本字典对应的页码取交集，留下的就是既在小写里也在大写里出现的字母。

#### 代码（Python）

```python
def countSpecialCharacters_optimal(word: str) -> int:
    # 用两个集合分别记录出现过的小写和大写字母
    lower_set = set()
    upper_set = set()

    # 只遍历一次字符串
    for ch in word:
        if ch.islower():          # 判断是否为小写字母
            lower_set.add(ch)     # 加入小写集合
        else:                     # 必然是大写字母（题目保证只有英文字母）
            upper_set.add(ch)     # 加入大写集合

    # 交集：既在 lower_set 又在 upper_set 的字母
    # 由于集合里存的都是字符本身（大小写已区分），
    # 需要把大写字母统一转成对应的小写再比较
    # 这里直接把 upper_set 中的每个字符转成小写后与 lower_set 求交
    special = lower_set & {c.lower() for c in upper_set}
    return len(special)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串（`n`），每次加入集合、判断大小写都是常数时间。相比暴力解的 `O(n²)`，速度提升明显。
- **空间复杂度**：`O(1)`（严格来说是 `O(52)`）  
  - 最多只会存 26 个小写和 26 个大写字符，空间大小与字符串长度无关，视作常数。

---

## 心得

- **核心技巧**：利用 **集合**（哈希表）实现 **一次遍历 + 集合交集**，把“是否出现过”这个信息压缩到 O(1) 查询。
- **适用题型**：  
  1. 判断字符是否同时满足多种属性（如同时出现大小写、出现奇数次等）。  
  2. 统计两个字符串的公共字符集合。  
  3. 找出数组/字符串中出现过的唯一元素（如“只出现一次的数字”）。
- **一句话总结**：**“一次遍历收集信息，用集合交集快速算答案”。**

---

## 反思

- **第一反应**：看到“出现大小写两种形式”，立刻想到要分别统计小写和大写的出现次数或出现与否。
- **最容易踩的坑**：  
  - 忘记把大写字符转成对应的小写再做交集，导致交集总是空。  
  - 误把字符本身直接放进同一个集合，导致 `'a'` 与 `'A'` 被当成不同元素，交集不成立。  
  - 边界情况：字符串全是同一种大小写，返回 0；长度为 1 时也要返回 0。
- **下次第一步**：先**把字符分类存进两个集合**，再思考如何用集合的**交/并**操作得到最终答案。这样可以避免重复遍历，直接走向最优解。