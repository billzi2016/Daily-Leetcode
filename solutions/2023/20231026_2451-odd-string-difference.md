# #2451. 奇异字符串差值 / Odd String Difference

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/odd-string-difference/)

---

## 题目（英文原版）

**Description**

You are given an array of equal-length strings words. Assume that the length of each string is n.
Each string words[i] can be converted into a difference integer array difference[i] of length n - 1 where difference[i][j] = words[i][j+1] - words[i][j] where 0 <= j <= n - 2. Note that the difference between two letters is the difference between their positions in the alphabet i.e. the position of 'a' is 0, 'b' is 1, and 'z' is 25.
All the strings in words have the same difference integer array, except one. You should find that string.
Return the string in words that has different difference integer array.

**Examples**

**Example 1:**

```
Input: words = ["adc","wzy","abc"]
Output: "abc"
Explanation: 
- The difference integer array of "adc" is [3 - 0, 2 - 3] = [3, -1].
- The difference integer array of "wzy" is [25 - 22, 24 - 25]= [3, -1].
- The difference integer array of "abc" is [1 - 0, 2 - 1] = [1, 1]. 
The odd array out is [1, 1], so we return the corresponding string, "abc".
```

**Example 2:**

```
Input: words = ["aaa","bob","ccc","ddd"]
Output: "bob"
Explanation: All the integer arrays are [0, 0] except for "bob", which corresponds to [13, -13].
```

**Constraints**

- 3 <= words.length <= 100
- n == words[i].length
- 2 <= n <= 20
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个等长字符串数组 `words`，设每个字符串的长度为 `n`。  
每个字符串 `words[i]` 可以转换为一个长度为 `n-1` 的差分整数数组（difference integer array） `difference[i]`，其中  

```
difference[i][j] = words[i][j+1] - words[i][j]   (0 ≤ j ≤ n-2)
```  

这里的字母差值指的是字母在字母表中的位置差，例如 `'a'` 的位置为 0，`'b'` 为 1，`'z'` 为 25。  

`words` 中所有字符串的差分整数数组都相同，只有 **一个**例外。请找出该字符串并返回。

**返回** `words` 中差分整数数组不同的那个字符串。

---

#### 示例 1
**输入**: `words = ["adc","wzy","abc"]`  
**输出**: `"abc"`  
**解释**:  
- `"adc"` 的差分整数数组为 `[3 - 0, 2 - 3] = [3, -1]`。  
- `"wzy"` 的差分整数数组为 `[25 - 22, 24 - 25] = [3, -1]`。  
- `"abc"` 的差分整数数组为 `[1 - 0, 2 - 1] = [1, 1]`。  

不同的数组是 `[1, 1]`，对应的字符串为 `"abc"`，因此返回它。

#### 示例 2
**输入**: `words = ["aaa","bob","ccc","ddd"]`  
**输出**: `"bob"`  
**解释**: 所有字符串的差分整数数组均为 `[0, 0]`，唯有 `"bob"` 对应的数组为 `[13, -13]`，所以返回 `"bob"`。

---

#### 约束条件
- `3 ≤ words.length ≤ 100`
- `n == words[i].length`
- `2 ≤ n ≤ 20`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把每个单词变成「差值数组」**  
   - 把字母当成「字典」里的词条，`'a'` 对应 0，`'b'` 对应 1，…，`'z'` 对应 25。  
   - 对于一个长度为 `n` 的单词 `s`，我们把相邻两个字母的编号相减，得到长度为 `n‑1` 的整数序列 `diff`，即  
     `diff[j] = code(s[j+1]) - code(s[j])`。  
   - 这一步相当于「把单词翻译成数字差值」，就像把一句话先翻成拼音再算声调差一样。

2. **找出唯一不同的差值数组**  
   - 把所有单词对应的差值数组放进一个列表 `all_diff`，用「哈希表」(Python 的 `dict`) 统计每种差值数组出现了多少次。  
   - 哈希表就像一本「查字典」：键（key）是差值数组（我们把它转成不可变的 `tuple`），值（value）是出现次数。  
   - 那个出现次数为 `1` 的键对应的就是「奇数」单词。

3. **返回对应的单词**  
   - 再遍历一次 `words`，找出它的差值数组在哈希表中计数为 `1` 的那个，即为答案。

> **为什么正确？**  
> 题目保证「除了唯一一个」之外，所有单词的差值数组都相同。于是统计出现次数，唯一出现一次的必然就是我们要找的那条。

#### 代码（Python）

```python
def oddString(words):
    """
    :param words: List[str]  # 所有单词，长度相同
    :return: str            # 差值数组与其它不同的那个单词
    """
    # ---------- 第一步：把每个单词转成差值数组 ----------
    def diff_array(s: str):
        # ord('a') == 97，减去 ord('a') 得到 0~25 的编号
        codes = [ord(ch) - ord('a') for ch in s]
        # 相邻两个编号相减，得到差值数组
        return tuple(codes[i+1] - codes[i] for i in range(len(codes)-1))

    # 保存每个单词对应的差值数组
    diffs = [diff_array(w) for w in words]

    # ---------- 第二步：统计每种差值数组出现的次数 ----------
    count = {}
    for d in diffs:
        count[d] = count.get(d, 0) + 1   # 哈希表计数

    # ---------- 第三步：找出计数为 1 的那个 ----------
    for w, d in zip(words, diffs):
        if count[d] == 1:               # 只出现一次的就是奇数
            return w

    # 题目保证一定有答案，理论上不会走到这里
    return ""
```

#### 复杂度

- **时间复杂度：** `O(m·n)`  
  - `m = len(words)`，`n = len(words[0])`。  
  - 对每个单词遍历一次字符得到差值数组（`O(n)`），共 `m` 次 → `O(m·n)`。  
  - 大白话：如果有 10 个单词，每个 5 个字母，最多算 10×5=50 次差值。

- **空间复杂度：** `O(m·n)`（用于存放所有差值数组）  
  - 也可以说是 `O(m·(n-1))`，因为每个差值数组长度是 `n-1`。  
  - 这相当于把所有单词的「差值」都复制了一遍。

---

### 2. 最优解

#### 思路  

暴力解的时间已经是 `O(m·n)`，这已经是线性时间，几乎不可能再更快。  
真正可以改进的，是**空间**：我们不必把所有差值数组都存下来，只要找出「公共」的差值模式，然后在遍历一次时直接定位异常单词。

**关键点**：

1. **只看前 3 个单词**  
   - 因为只有一个异常，至少有两个人的差值数组是相同的。  
   - 前 3 个里必定出现「两个相同」的情况，这两个相同的差值就是「公共模式」。
   - 用 `tuple`（不可变）直接当作哈希键，不需要额外的哈希表。

2. **确定公共模式**  
   - 计算前 3 个单词的差值数组 `d0, d1, d2`。  
   - 如果 `d0 == d1` 或 `d0 == d2`，公共模式就是 `d0`；否则公共模式就是 `d1`（此时 `d1 == d2`）。

3. **再次遍历找到不同的单词**  
   - 只要当前单词的差值数组不等于公共模式，即为答案。

**为什么更好？**  
- **空间降低到 `O(n)`**：只保存一个差值数组（公共模式）和当前遍历的差值数组。  
- 时间仍然是 `O(m·n)`，但常数更小，因为只遍历两遍而不是三遍（统计 + 再找）。

#### 代码（Python）

```python
def oddString(words):
    """
    只使用 O(n) 额外空间找出差值数组不同的单词。
    """
    # ---------- 辅助函数：计算单词的差值数组 ----------
    def diff_array(s: str):
        codes = [ord(ch) - ord('a') for ch in s]
        return tuple(codes[i+1] - codes[i] for i in range(len(codes)-1))

    # ---------- 第一步：先算前 3 个单词的差值 ----------
    d0 = diff_array(words[0])
    d1 = diff_array(words[1])
    d2 = diff_array(words[2])

    # ---------- 第二步：确定「公共」差值 ----------
    if d0 == d1 or d0 == d2:
        common = d0          # d0 与其他至少有一个相同
    else:
        common = d1          # 那么 d1 与 d2 必相同

    # ---------- 第三步：遍历所有单词，找出不同的 ----------
    for w in words:
        if diff_array(w) != common:   # 第一次出现不同的就是答案
            return w

    # 题目保证一定有答案，这里理论上不会执行到
    return ""
```

#### 复杂度

- **时间复杂度：** `O(m·n)`（与暴力解相同）  
  - 只遍历两遍：一次算前 3 个差值，第二次遍历全部单词。  
  - 相比暴力解少了构造完整计数表的步骤，常数更小。

- **空间复杂度：** `O(n)`  
  - 只保存「公共差值」一个 `tuple`（长度 `n-1`）以及当前遍历时的差值数组。  
  - 大白话：如果单词长度是 10，只需要记 9 个数字，而不是记所有 10×单词数的差值。

---

## 心得

- **核心技巧**：利用「多数相同、唯一不同」的特性，只通过少量样本（前 3 个）确定公共模式，再线性扫描定位异常。  
- **适用场景**：  
  1. **找出唯一不同的数/字符串**（如 LeetCode 2425 `Find the Difference of Two Arrays` 的变体）。  
  2. **多数投票算法**（多数元素问题），思路类似：先找出可能的候选，再验证。  
  3. **异常检测**（大多数数据符合某规律，少数异常），比如找出唯一的奇数/偶数。  
- **一句话总结**：**「先用少量样本锁定大多数的模式，再全局验证」是解决「唯一异常」题目的钥匙。**

---

## 反思

- **第一反应**：直接把每个单词的差值数组全部算出来，再两两比较，甚至用 `list.count` 找不同。  
- **最容易踩的坑**：  
  - 忘记把差值数组转成不可变的 `tuple` 再做哈希，导致 `dict` 报错。  
  - 没考虑到 `words` 最少有 3 条，若只取前 2 条就可能把异常当成公共模式。  
  - 对字母编号的计算忘记减去 `'a'`，导致差值范围错误（会出现负数以外的数）。  
- **下次遇到同类题**，第一步应该**先判断「多数」和「少数」的比例**，利用少量样本锁定多数的特征，再用一次线性扫描定位唯一的不同。这样既省空间又省时间。