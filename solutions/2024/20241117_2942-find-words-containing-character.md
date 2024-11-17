# #2942. 查找包含指定字符的单词 / Find Words Containing Character

> 难度：简单 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/find-words-containing-character/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of strings words and a character x.
Return an array of indices representing the words that contain the character x.
Note that the returned array may be in any order.

**Examples**

**Example 1:**

```
Input: words = ["leet","code"], x = "e"
Output: [0,1]
Explanation: "e" occurs in both words: "leet", and "code". Hence, we return indices 0 and 1.
```

**Example 2:**

```
Input: words = ["abc","bcd","aaaa","cbc"], x = "a"
Output: [0,2]
Explanation: "a" occurs in "abc", and "aaaa". Hence, we return indices 0 and 2.
```

**Example 3:**

```
Input: words = ["abc","bcd","aaaa","cbc"], x = "z"
Output: []
Explanation: "z" does not occur in any of the words. Hence, we return an empty array.
```

**Constraints**

- 1 <= words.length <= 50
- 1 <= words[i].length <= 50
- x is a lowercase English letter.
- words[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的字符串数组（array）`words` 和一个字符 `x`。  
返回一个整数数组（array），其中的下标表示 `words` 中包含字符 `x` 的单词。  
返回的数组顺序可以任意。

**示例 1**  
**输入**: `words = ["leet","code"], x = "e"`  
**输出**: `[0,1]`  
**解释**: 字符 `"e"` 出现在 `"leet"` 和 `"code"` 中。因此返回下标 `0` 和 `1`。

**示例 2**  
**输入**: `words = ["abc","bcd","aaaa","cbc"], x = "a"`  
**输出**: `[0,2]`  
**解释**: 字符 `"a"` 出现在 `"abc"` 和 `"aaaa"` 中。因此返回下标 `0` 和 `2`。

**示例 3**  
**输入**: `words = ["abc","bcd","aaaa","cbc"], x = "z"`  
**输出**: `[]`  
**解释**: 字符 `"z"` 没有出现在任何单词中。因此返回空数组。

**约束条件**  
- `1 <= words.length <= 50`  
- `1 <= words[i].length <= 50`  
- `x` 为小写英文字母。  
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每个单词都检查一遍**，看里面有没有出现字符 `x`。  
可以把这个过程想象成：

- **词典**（list `words`）里有很多本子（每个本子是一串字符）。
- 我们手里有一支笔（字符 `x`），要把每本子从头到尾翻一遍，看看笔写的字有没有出现。

实现时，用两层循环：

1. 外层遍历 `words`，用下标 `i` 记录当前是第几本本子（这也是答案要返回的索引）。
2. 内层遍历当前单词的每个字符，若等于 `x`，就把 `i` 加入答案列表并立即结束本次内层循环（因为已经找到了，不需要再继续检查这本单子）。

这种做法一定能得到正确答案，因为我们**没有遗漏任何单词，也没有遗漏单词里的任何字符**。

#### 代码（Python）

```python
def findWordsContainingChar(words, x):
    """
    :param words: List[str] - 单词数组
    :param x: str - 需要查找的字符（长度为 1）
    :return: List[int] - 包含字符 x 的单词下标
    """
    ans = []                         # 用来存放符合条件的下标
    for i, w in enumerate(words):    # 外层循环：遍历每个单词及其下标
        for ch in w:                 # 内层循环：遍历单词里的每个字符
            if ch == x:              # 找到目标字符
                ans.append(i)        # 记录下标
                break                # 这本单子已经满足条件，退出内层循环
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n * m)`  
  - `n` 是单词数量，`m` 是单词的平均长度。  
  - 大白话：如果有 50 本本子，每本本子平均有 20 页（字符），我们最坏要翻 50×20 = 1000 页。  
- **空间复杂度：** `O(k)`  
  - `k` 是答案列表的长度（即包含字符 `x` 的单词数），额外只用到了存放结果的空间。  
  - 其它变量都是常数级别的。

---

### 2. 最优解

#### 思路  

对于本题，**检查每个单词是否包含字符 `x`** 是不可避免的，因为只有遍历才能确认是否出现。  
所以“最优”并不是把时间复杂度进一步压缩，而是**把代码写得更简洁、更 Pythonic**，同时保持同样的 `O(n·m)` 复杂度。

优化方向：

1. **利用 Python 的成员运算符 `in`**：`x in w` 能在内部一次遍历单词，就判断是否出现，等价于我们手写的内层循环，却更易读。
2. **使用列表推导式（list comprehension）** 或 `enumerate` 直接生成答案，省去手动 `append`、`break` 的细节。

如果想进一步提升查询速度，可以把每个单词先转成集合 `set(w)`，这样判断字符是否在集合里是 `O(1)`，但构造集合本身也要遍历整个单词，整体仍是 `O(n·m)`，且会额外占用 `O(m)` 的空间。因此在本题约束下，直接使用 `in` 已经是最简且高效的做法。

#### 代码（Python）

```python
def findWordsContainingChar(words, x):
    """
    更简洁的实现：利用 Python 的成员运算符 `in` 与列表推导式
    """
    # enumerate 同时得到下标 i 和单词 w，若字符 x 在单词 w 中则保留下标 i
    return [i for i, w in enumerate(words) if x in w]
```

#### 复杂度  

- **时间复杂度：** `O(n * m)`  
  - 与暴力解相同，因为每个单词仍然要检查一次。  
  - 与暴力解对比：代码更短，实际运行时的常数因子略小（内部实现用了 C 语言层面的优化）。
- **空间复杂度：** `O(k)`  
  - 同样只需要存放答案列表。  
  - 额外的临时空间几乎为零（列表推导式在生成时直接写入结果列表）。

---

## 心得

- **核心技巧**：遍历 + 成员判定（`in`），以及利用 `enumerate` 与列表推导式写出简洁代码。
- **适用的题型**  
  1. “找出满足某个字符/子串条件的下标” 类题（如 LeetCode 1935 `Maximum Number of Words You Can Type`）。  
  2. “过滤满足条件的元素并返回其索引” 类题（如 LeetCode 2251 `Number of Flowers in Full Bloom` 的简化版）。  
- **解题钥匙**：**把“遍历+判断”写成最直接的表达式**，不必刻意追求更高的时间复杂度。

## 反思

- **第一反应**：看到“返回包含字符的单词下标”，自然想到双层循环逐字符比较。
- **最容易踩的坑**  
  - 忘记在找到字符后立刻 `break`，导致同一个单词被多次加入答案。  
  - 忽视输入可能为空或字符不存在的情况，需要返回空列表 `[]`。  
- **下次思路**：遇到“是否包含”这类判断时，先考虑 Python 的内置成员运算符 `in`，再决定是否需要手写循环。这样既能保证正确性，又能写出简洁高效的代码。