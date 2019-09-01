# #557. 翻转字符串中的单词 III / Reverse Words in a String III

> 难度：简单 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/reverse-words-in-a-string-iii/)

---

## 题目（英文原版）

**Description**

Given a string s, reverse the order of characters in each word within a sentence while still preserving whitespace and initial word order.

**Examples**

**Example 1:**

```
Input: s = "Let's take LeetCode contest"
Output: "s'teL ekat edoCteeL tsetnoc"
```

**Example 2:**

```
Input: s = "Mr Ding"
Output: "rM gniD"
```

**Constraints**

- 1 <= s.length <= 5 * 104
- s contains printable ASCII characters.
- s does not contain any leading or trailing spaces.
- There is at least one word in s.
- All the words in s are separated by a single space.

---

## 题目（中文翻译）

给定一个字符串 (string) `s`，请在保持空格 (whitespace) 以及单词原始顺序不变的前提下，反转句子中每个单词内部的字符顺序。

示例 1  
输入: `s = "Let's take LeetCode contest"`  
输出: `"s'teL ekat edoCteeL tsetnoc"`

示例 2  
输入: `s = "Mr Ding"`  
输出: `"rM gniD"`

约束条件：
- `1 <= s.length <= 5 * 10^4`
- `s` 只包含可打印的 ASCII 字符。
- `s` 不含前导或尾随空格。
- `s` 至少包含一个单词。
- 所有单词之间仅由单个空格分隔。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把句子拆成一个个单词，分别把每个单词的字符顺序翻转后再拼回去。  
- **拆分**：把字符串按空格分割，得到一个单词列表。把它想象成把一句话拆成若干块积木，每块就是一个单词。  
- **翻转**：对每块积木内部的字母顺序倒过来，像把积木倒置。Python 中可以直接用切片 `word[::-1]` 完成。  
- **拼接**：把所有倒置后的积木用空格重新连起来，得到最终答案。  

这种做法之所以正确，是因为题目只要求 **每个单词内部** 的字符顺序翻转，而 **单词之间的相对位置** 和 **空格数量** 都保持不变。只要我们不动空格，只翻转单词本身，就一定满足要求。

#### 代码（Python）

```python
def reverseWords(s: str) -> str:
    # 1. 按空格把句子切成单词列表
    words = s.split(' ')          # ['Let\'s', 'take', 'LeetCode', 'contest']

    # 2. 对每个单词使用切片[::-1]进行翻转
    reversed_words = [word[::-1] for word in words]

    # 3. 用空格把翻转后的单词重新拼起来
    return ' '.join(reversed_words)
```

#### 复杂度  

- **时间复杂度：O(n)**  
  这里的 *n* 是字符串的长度。我们遍历了一遍字符串来切分，又遍历了一遍来翻转每个字符，总共是线性时间。  
  用大白话说，就是“处理的字符数量和原字符串一样多”，不会出现指数级的爆炸。

- **空间复杂度：O(n)**  
  `split` 会产生一个新的列表，`join` 又会生成新的字符串，这些都需要额外的存储，和原字符串等长。  

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性时间**，已经很快了。不过如果想进一步 **降低额外空间**，可以在原字符序列上就地翻转每个单词。思路如下：

1. **把字符串变成字符数组**  
   Python 的字符串不可修改，先把它转成 `list(s)`，得到可写的字符列表。想象成把整句话写在一排可移动的字母卡片上。

2. **使用双指针定位每个单词**  
   - `left` 指向当前单词的首字符位置。  
   - `right` 向右移动，直到遇到空格或到达字符串末尾，此时 `[left, right‑1]` 就是一个完整的单词。  
   这一步像在卡片中找出“一段连续的字母”，空格相当于分隔符。

3. **原地翻转这段子数组**  
   用两个指针 `i`、`j` 在子数组内部从两端向中间交换字符，直到相遇。这样就实现了 **单词内部的翻转**，而不需要额外的字符串或列表。

4. **继续处理下一个单词**  
   把 `left` 移到下一个单词的起始位置（`right + 1`），重复上述过程，直至遍历完所有字符。

这种做法的核心是 **双指针**（Two Pointers）——一种常见的“从两头向中间收敛”技巧，适用于翻转、移动、匹配等问题。

#### 代码（Python）

```python
def reverseWords(s: str) -> str:
    # 把不可变的字符串转成可变的字符列表
    chars = list(s)                # ['L', 'e', 't', "'", 's', ' ', ...]

    n = len(chars)
    left = 0                       # 当前单词的左边界

    while left < n:
        # 找到单词的右边界（空格或字符串末尾）
        right = left
        while right < n and chars[right] != ' ':
            right += 1             # right 指向空格或 n

        # 在 [left, right-1] 区间内原地翻转字符
        i, j = left, right - 1
        while i < j:
            chars[i], chars[j] = chars[j], chars[i]   # 交换
            i += 1
            j -= 1

        # 跳过空格，准备处理下一个单词
        left = right + 1

    # 把字符列表再拼成字符串返回
    return ''.join(chars)
```

#### 复杂度  

- **时间复杂度：O(n)**  
  每个字符只会被访问常数次（一次寻找单词边界，最多一次交换），所以仍是线性时间。相比暴力解，没有额外的遍历开销。

- **空间复杂度：O(n)**  
  由于 Python 字符串不可变，我们必须把它复制成列表，这一步占用了 *n* 的额外空间。不过在语言允许原地修改的情况下（如 C++ 的字符数组），额外空间可以降到 **O(1)**，即只使用常数个指针变量。

---

## 心得

- **核心技巧**：双指针在同一数据结构上从两端向中间移动，实现原地翻转。  
- **适用题型**：  
  1. 翻转字符串中的单词（本题）  
  2. 判断回文字符串（两指针从两端比较）  
  3. 移除数组中的特定元素并保持顺序（快慢指针）  
- **一句话总结**：把“每个单词内部”当成独立的区间，用双指针把区间里的字符倒置，即可一次遍历完成全部翻转。

---

## 反思

- **第一反应**：直接把句子 `split`、`reverse`、`join`，写出最直观的代码。  
- **最容易踩的坑**：  
  - 忘记处理最后一个单词后面没有空格的情况（循环结束条件要写对）。  
  - 直接在原字符串上尝试修改，会报 “str object does not support item assignment”。  
- **下次类似题的第一步**：先明确“需要原地操作还是可以额外空间”，如果要求空间最小，就把问题抽象为“在同一序列上找出连续区间并翻转”，随后使用双指针实现。