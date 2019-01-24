# #242. 有效的字母异位词 / Valid Anagram

> 难度：简单 · 标签：Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/valid-anagram/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, return true if t is an anagram of s, and false otherwise.
Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

**Examples**

**Example 1:**

```
Input: s = "anagram", t = "nagaram"
Output: true
```

**Example 2:**

```
Input: s = "rat", t = "car"
Output: false
```

**Constraints**

- 1 <= s.length, t.length <= 5 * 104
- s and t consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，如果 `t` 是 `s` 的字母异位词（anagram），则返回 `true`；否则返回 `false`。

**示例 1**  
**输入**: `s = "anagram", t = "nagaram"`  
**输出**: `true`

**示例 2**  
**输入**: `s = "rat", t = "car"`  
**输出**: `false`

**约束条件**  
- `1 <= s.length, t.length <= 5 * 10^4`  
- `s` 和 `t` 只包含小写英文字母。

**进阶**  
如果输入可能包含 Unicode 字符，该如何调整你的解法？（考虑字符集更大的情况）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把字符串 `s` 的每一个字符都在 `t` 中找一遍，如果能全部匹配且不剩余字符，就说明 `t` 是 `s` 的字母重排（anagram）。  
这相当于把 `t` 当成一本“字典”，我们一页一页地翻，找对应的词（字符），找到后把这页撕掉（把字符从 `t` 中删除），继续找下一页。  

- **使用的数据结构**：这里我们直接把 `t` 当成一个可变的列表（或者用字符串切片），每找到一个匹配的字符就把它删掉。  
- **为什么正确**：如果两个字符串真的只是在字符顺序上不同，那么每次我们在 `t` 中都能找到对应的字符，最终 `t` 会被删光；如果有任意一个字符找不到，或者删完后 `t` 还有剩余字符，说明两者不是字母重排。  

#### 代码（Python）
```python
def isAnagram_bruteforce(s: str, t: str) -> bool:
    # 长度不同一定不是 anagram
    if len(s) != len(t):
        return False

    # 把 t 变成列表，方便删除元素
    t_list = list(t)

    # 遍历 s 的每个字符，尝试在 t_list 中找匹配的字符
    for ch in s:
        if ch in t_list:                 # 在 t 中找到了对应字符
            t_list.remove(ch)            # 删除该字符，防止重复使用
        else:                             # 没找到，说明不是 anagram
            return False

    # 所有字符都匹配成功，t_list 应该被删空
    return not t_list
```

#### 复杂度
- **时间复杂度**：`O(n²)`  
  解释：外层遍历 `s`（`n` 次），每次 `in` 操作和 `remove` 都要在列表里线性搜索，最坏情况下要遍历 `t` 的剩余长度，平均是 `n/2`，所以整体大约是 `n × n = n²`。用大白话说，就是“每找一个字母都要翻一遍剩下的所有字母”，会变得很慢。
- **空间复杂度**：`O(n)`  
  解释：我们额外开辟了一个 `t_list`，它的长度和原字符串 `t` 相同。  

---

### 2. 最优解

#### 思路  
从暴力解可以看到，瓶颈在于**频繁地线性搜索并删除字符**。如果我们能在 **常数时间**（`O(1)`）内判断某个字符是否出现过、出现了多少次，就可以把整体复杂度降下来。  

这正是**哈希表**（在 Python 中用 `dict`）擅长的事：  
- 把每个字符当成 “键（key）”，把它出现的次数当成 “值（value）”。  
- 先遍历 `s`，把每个字符的计数加一；再遍历 `t`，把对应字符的计数减一。  
- 最后检查所有计数是否都回到了零，若是则两个字符串是字母重排，否则不是。

> 类比：哈希表就像一本**词典**，我们把字母当成单词，出现次数当成页码。查找、增减页码的操作都像翻字典一样快，时间几乎不随词条数量增长。

**Unicode 兼容**：Python 的 `dict` 可以直接存放任意 Unicode 字符，不需要额外处理，只要把字符当作普通的键即可。

#### 代码（Python）
```python
def isAnagram(s: str, t: str) -> bool:
    # 长度不同直接返回 False
    if len(s) != len(t):
        return False

    # 第一步：统计 s 中每个字符出现的次数
    count = {}                         # 空字典，类似“词典”
    for ch in s:
        count[ch] = count.get(ch, 0) + 1   # get 返回当前计数，若不存在返回 0

    # 第二步：遍历 t，逐个字符把计数减一
    for ch in t:
        if ch not in count:                # t 中出现了 s 没有的字符
            return False
        count[ch] -= 1                     # 把对应的页码减一
        if count[ch] < 0:                  # 出现次数超出 s 中的数量
            return False

    # 第三步：检查所有计数是否都为 0
    # （这里其实已经保证了，只要没有提前返回 False，计数必然全为 0）
    return True
```

#### 复杂度
- **时间复杂度**：`O(n)`  
  解释：我们只遍历了两遍字符串，每次对哈希表的增、删、查都是 **常数时间**（`O(1)`），所以整体是线性时间。用大白话说，就是“每个字母只看一次”，非常快。
- **空间复杂度**：`O(1)`（严格来说是 `O(k)`）  
  解释：哈希表最多存放不同字符的种类数 `k`。本题限制字符为小写英文字母，`k ≤ 26`，可以视作常数空间。如果放宽到任意 Unicode，空间仍然是 `O(k)`，即字符种类数的线性空间。

---

## 心得

- **核心技巧**：利用哈希表（字典）计数，做到一次遍历完成字符匹配。  
- **适用的题型**  
  1. 判断两个字符串是否互为字母重排（本题）。  
  2. 判断一段文字中是否包含所有给定字符（“ransom note” 类题）。  
  3. 统计数组/字符串中出现次数最多的元素（“majority element”）。  
- **一句话总结解题钥匙**：**把“出现多少次”放进字典，用增减抵消的方式快速比较两组数据**。

---

## 反思

- **第一反应**：先想到把两个字符串排序后直接比较，虽然也能得到正确答案，但时间是 `O(n log n)`，不是最优。  
- **最容易踩的坑**  
  - 忘记先检查长度是否相等，导致后面的计数过程多余。  
  - 在计数过程中没有及时判断负数或不存在的键，可能会出现 `KeyError` 或错误的 `True` 结果。  
- **下次遇到同类题的第一步**：**先想“怎么用哈希表把出现次数记录下来”，如果能在一次遍历完成增删，就基本达到了最优**。