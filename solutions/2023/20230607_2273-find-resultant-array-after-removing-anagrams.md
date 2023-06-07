# #2273. 删除相邻异位词后的结果数组 / Find Resultant Array After Removing Anagrams

> 难度：简单 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-resultant-array-after-removing-anagrams/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string array words, where words[i] consists of lowercase English letters.
In one operation, select any index i such that 0 < i < words.length and words[i - 1] and words[i] are anagrams, and delete words[i] from words. Keep performing this operation as long as you can select an index that satisfies the conditions.
Return words after performing all operations. It can be shown that selecting the indices for each operation in any arbitrary order will lead to the same result.
An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase using all the original letters exactly once. For example, "dacb" is an anagram of "abdc".

**Examples**

**Example 1:**

```
Input: words = ["abba","baba","bbaa","cd","cd"]
Output: ["abba","cd"]
Explanation:
One of the ways we can obtain the resultant array is by using the following operations:
- Since words[2] = "bbaa" and words[1] = "baba" are anagrams, we choose index 2 and delete words[2].
  Now words = ["abba","baba","cd","cd"].
- Since words[1] = "baba" and words[0] = "abba" are anagrams, we choose index 1 and delete words[1].
  Now words = ["abba","cd","cd"].
- Since words[2] = "cd" and words[1] = "cd" are anagrams, we choose index 2 and delete words[2].
  Now words = ["abba","cd"].
We can no longer perform any operations, so ["abba","cd"] is the final answer.
```

**Example 2:**

```
Input: words = ["a","b","c","d","e"]
Output: ["a","b","c","d","e"]
Explanation:
No two adjacent strings in words are anagrams of each other, so no operations are performed.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 10
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

你得到一个下标从 0 开始的字符串数组 `words`，其中 `words[i]` 仅由小写英文字母组成。  
一次操作中，选择任意满足 `0 < i < words.length` 且 `words[i - 1]` 与 `words[i]` 是异位词（anagram）的下标 `i`，并将 `words[i]` 从数组中删除。只要仍然存在满足条件的下标，就继续执行此操作。  
返回完成所有操作后的 `words`。可以证明，无论以何种顺序选择下标进行操作，最终结果均相同。  

**异位词（anagram）**是指通过重新排列另一个单词或短语的所有字母且恰好使用一次而形成的单词或短语。例如，`"dacb"` 是 `"abdc"` 的异位词。

### 示例 1

```text
Input: words = ["abba","baba","bbaa","cd","cd"]
Output: ["abba","cd"]
```

**解释：**  
我们可以通过以下一系列操作得到结果数组：

- 因为 `words[2] = "bbaa"` 与 `words[1] = "baba"` 是异位词，选择下标 `2` 并删除 `words[2]`。此时 `words = ["abba","baba","cd","cd"]`。  
- 接着 `words[1] = "baba"` 与 `words[0] = "abba"` 是异位词，选择下标 `1` 并删除 `words[1]`。此时 `words = ["abba","cd","cd"]`。  
- 再次 `words[2] = "cd"` 与 `words[1] = "cd"` 是相同的字符串（自然也是异位词），选择下标 `2` 并删除 `words[2]`。最终得到 `words = ["abba","cd"]`。

### 示例 2

```text
Input: words = ["a","b","c","d","e"]
Output: ["a","b","c","d","e"]
```

**解释：**  
相邻的字符串之间没有任何一对是异位词，因此不进行任何操作，数组保持不变。

### 约束条件

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 10`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步一步模拟题目描述的操作** ：

1. 从左到右遍历数组 `words`，找到任意满足 `words[i‑1]` 与 `words[i]` 是字母重排（anagram）的相邻位置 `i`。  
2. 把 `words[i]` 删除（即把这个元素从列表中移除），数组长度会立刻变短。  
3. 继续从头或从删除位置的前面重新检查，直到再也找不到相邻的 anagram 为止。

> **数据结构类比**  
> - Python 列表就像一本书的“活页”，删掉一页后后面的页码会整体向前移动。  
> - 判断两个单词是否是 anagram 可以把它们的字母排序后比较，排序就像把字母装进字典里查“顺序”，相同的排序结果说明两本字典的内容完全一样。

**为什么能得到正确答案**  
只要我们不断删掉右侧的 anagram，最终的数组里相邻的两个单词就不可能再是 anagram（否则还能继续删）。题目保证 **不管删的顺序怎样，最终数组唯一**，所以只要我们一直删下去，就一定能得到那唯一的结果。

**时间 / 空间复杂度分析（大白话）**  

- 每次找到一对相邻的 anagram，就要把右边的元素从列表中弹出，这在 Python 里是 `O(n)`（因为后面的所有元素都要向前移动一位）。  
- 最坏情况下，数组里每两个相邻元素都是 anagram，需要删除 `n‑1` 次。于是总体时间是 `O(n) * O(n) = O(n²)`。  
- 只用了原来的列表和若干临时变量，额外空间是 `O(1)`（不算返回的结果）。

#### 代码（Python）

```python
from typing import List

def are_anagrams(a: str, b: str) -> bool:
    """把两个单词的字母排序后比较，返回它们是否是字母重排。"""
    return sorted(a) == sorted(b)

def removeAnagrams_bruteforce(words: List[str]) -> List[str]:
    """
    暴力模拟：不断删除右侧的相邻 anagram，直到不能再删。
    """
    i = 1                     # 从第二个元素开始检查
    while i < len(words):
        if are_anagrams(words[i - 1], words[i]):
            # 删除右侧的 anagram（pop 会把后面的元素整体左移）
            words.pop(i)
            # 删除后，i 保持不变，因为新的 words[i] 仍然是
            # 原来 words[i+1]，需要再次和左边比较
        else:
            i += 1            # 两者不是 anagram，继续向右检查
    return words
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 想象 `n = 100`，最坏情况下要比较 100 次、删除 99 次，每次删除都要把后面的元素整体搬移，累计的工作量接近 100 × 100。
- **空间复杂度**：`O(1)`（只用了常数个临时变量，不计返回的列表本身）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每删一次都要把后面的元素整体左移**，导致整体是二次的。我们可以把 “删除右侧 anagram” 这一步 **改写成一次遍历构造最终数组**：

- 从左到右依次读取 `words[i]`。  
- **只保留** 那些 **与前一个保留下来的单词不是 anagram** 的单词。  
- 为了快速判断是否是 anagram，**把每个单词的字母排序后得到一个“标准形式”**（如 `"baba"` → `"aabb"`）。相同的标准形式说明是 anagram。  
- 用一个 **栈 / 结果列表** 保存已经确定会出现在最终答案里的单词。遍历时只需要和栈顶（最近保留下来的单词）比较即可。

> **核心算法：一次遍历 + 哈希表（或排序）**  
> - “排序后得到的字符串” 就像是字典的**页码**：不同的单词如果是字母重排，它们对应的页码完全相同。我们只需要比较页码是否相同，而不必一次次把两个单词的字母逐个对比。  
> - 这一步的时间是 `O(m log m)`（`m` 为单词长度），因为 `sorted` 本身是基于比较的排序。由于每个单词最长只有 10 个字符，这个开销几乎可以忽略。

**为什么只和栈顶比较就够了？**  
假设我们已经把前面的若干单词都处理好了，得到的结果列表 `res` 保证 **相邻的两个单词不构成 anagram**。如果当前单词 `cur` 与 `res[-1]`（即最近保留下来的单词）是 anagram，那么按照题目规则 `cur` 必须被删除（因为它在右侧），所以我们直接 **不把它加入 `res`**。如果不是 anagram，说明 `cur` 与左侧所有保留下来的单词都不相同（因为最近的那个已经不是 anagram），于是 `cur` 必然会保留下来，加入 `res`。

**一步搞定**：遍历结束后，`res` 就是题目要求的最终数组。

#### 代码（Python）

```python
from typing import List

def canonical(word: str) -> str:
    """
    把单词的字母排序后返回，作为判断 anagram 的标准形式。
    例如 "baba" -> "aabb"
    """
    # sorted 返回字符列表，join 把它们拼成新字符串
    return ''.join(sorted(word))

def removeAnagrams_optimal(words: List[str]) -> List[str]:
    """
    最优解：一次遍历，利用“排序后字符串”判断相邻是否为 anagram。
    """
    result: List[str] = []          # 用来保存最终会留下的单词
    last_canonical = ''             # 记录 result 最后一个单词的标准形式

    for w in words:
        cur_canonical = canonical(w)   # 计算当前单词的标准形式
        if cur_canonical != last_canonical:
            # 与左侧最近保留下来的单词不是 anagram，保留它
            result.append(w)
            last_canonical = cur_canonical   # 更新记录
        # 否则是 anagram，直接丢弃（不加入 result）

    return result
```

#### 复杂度

- **时间复杂度**：`O(n * m log m)`  
  - `n` 为单词个数（≤100），`m` 为单词最大长度（≤10）。对每个单词我们做一次排序 `O(m log m)`，其余操作都是 `O(1)`。因为 `m` 很小，这在实际运行中几乎是线性的 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，**只需要一次遍历**，快了几个数量级。

- **空间复杂度**：`O(n)`  
  - 需要一个 `result` 列表来保存最终答案，最坏情况下全部保留下来。除此之外只用了常数级的临时变量 (`last_canonical`、`cur_canonical`)。

---

## 心得

- **核心技巧**：把“是否是 anagram”抽象为“排序后得到的标准形式是否相同”。利用这个标准形式，只需比较相邻（最近保留下来的）元素，就能一次遍历完成删除操作。  
- **适用的题型**  
  1. “删除相邻重复/相似元素” 类问题（例如 LeetCode 1047 **Remove All Adjacent Duplicates In String**）。  
  2. “压缩相邻相同/等价元素” 的数组或字符串处理（如 443. **String Compression**）。  
  3. “基于哈希/标准化表示的去重” （例如 217. **Contains Duplicate** 的变体）。  
- **一句话总结解题钥匙**：**把判断相等的条件标准化（排序/计数），再用“一次遍历 + 记住最近的合法元素”**。

---

## 反思

- **第一反应**：看到“相邻的两个单词是 anagram，就删掉右边的”，立刻想到 **模拟删除**，于是写出暴力解。  
- **最容易踩的坑**  
  - **删除时下标变化**：`pop(i)` 后数组收缩，若不把指针回退会漏掉新的相邻对。  
  - **判断 anagram 的方式**：直接用 `sorted`，但要记得每次比较前后两次 `sorted` 的结果，而不是只比较一次。  
  - **边界情况**：只有一个单词或全部单词都不相邻 anagram，代码必须直接返回原数组。  
- **下次遇到同类题**：第一步先 **想能否把“相等/相似”转化为一种容易比较的“标记”**（如排序、计数数组），随后 **尝试一次遍历+栈/结果列表** 的思路，避免频繁的删除导致的二次时间复杂度。