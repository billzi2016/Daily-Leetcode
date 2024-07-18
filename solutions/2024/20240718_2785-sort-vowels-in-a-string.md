# #2785. 字符串中元音字母排序 / Sort Vowels in a String

> 难度：中等 · 标签：String、Sorting · [LeetCode 链接](https://leetcode.com/problems/sort-vowels-in-a-string/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed string s, permute s to get a new string t such that:
Return the resulting string.
The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in lowercase or uppercase. Consonants comprise all letters that are not vowels.

**Examples**

**Example 1:**

```
Input: s = "lEetcOde"
Output: "lEOtcede"
Explanation: 'E', 'O', and 'e' are the vowels in s; 'l', 't', 'c', and 'd' are all consonants. The vowels are sorted according to their ASCII values, and the consonants remain in the same places.
```

**Example 2:**

```
Input: s = "lYmpH"
Output: "lYmpH"
Explanation: There are no vowels in s (all characters in s are consonants), so we return "lYmpH".
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of letters of the English alphabet in uppercase and lowercase.

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的字符串 `s`，对 `s` 进行排列得到新字符串 `t`，要求满足：

- 所有元音字母（vowels）按照 **ASCII** 值升序排列；
- 辅音字母（consonants）保持在原来的位置不变。

返回满足上述条件的字符串 `t`。

元音字母包括 `'a'、'e'、'i'、'o'、'u'`，大小写均视为元音。除元音之外的所有字母均视为辅音。

---

### 示例

**示例 1**  
**输入**: `s = "lEetcOde"`  
**输出**: `"lEOtcede"`  
**解释**: `'E'、'O'、'e'` 是 `s` 中的元音字母，`'l'、't'、'c'、'd'` 是辅音字母。元音字母按照 ASCII 值排序后依次放入原来的元音位置，辅音字母位置保持不变。

**示例 2**  
**输入**: `s = "lYmpH"`  
**输出**: `"lYmpH"`  
**解释**: `s` 中不存在元音字母（全部为辅音），因此返回原字符串。

---

### 约束

- `1 <= s.length <= 10^5`
- `s` 仅由英文字母（大小写）组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有元音字母挑出来，手动把它们排成从小到大的顺序**，然后再把排好序的元音一个一个放回原来的位置。  
这里涉及的主要数据结构只有 **列表（数组）**，它就像我们平时用的「装东西的盒子」——可以随时往里放、取出、甚至把盒子里的东西重新排个序。

实现步骤：

1. **遍历原字符串**，把每个字符是否是元音（a/e/i/o/u，大小写都算）记下来。  
   - 如果是元音，就把它加入 `vowels` 列表。  
   - 同时把它在原字符串中的下标也保存下来（因为稍后要把排好序的元音放回去）。  
2. 对 `vowels` 列表**直接使用冒泡排序**（或者任何 O(n²) 的排序）——每次比较相邻两个字符的 ASCII 码，若顺序错误就交换。  
   - 这一步虽然慢，但思路非常直观：就像我们把一堆卡片摞在一起，一次一次比较并交换，直到所有卡片都按字典顺序排好。  
3. 再次遍历原字符串的下标列表，把排好序的元音依次写回对应的位置，得到最终字符串。

**为什么正确？**  
- 第 1 步把所有元音完整收集，保证没有遗漏。  
- 第 2 步把这些元音按照 ASCII（即字母表顺序）从小到大排列。  
- 第 3 步把排好序的元音放回原来的“空位”，而非元音的字符（即辅音）保持不动，满足题目要求。

**复杂度分析（大白话版）**  
- **时间复杂度**：  
  - 第一次遍历 O(n)（一次扫过字符串）。  
  - 冒泡排序最坏情况是 O(m²)，其中 m 是元音的个数（最坏 m≈n）。  
  - 最后再遍历一次 O(m)。  
  - 综合下来是 **O(n + m²)**，在最坏情况下约等于 **O(n²)**。  
  - 用大白话说，就是如果字符串里元音很多，排序这一步会像“慢慢搬砖”一样，耗时会成平方增长。  
- **空间复杂度**：  
  - 需要额外的 `vowels` 列表和下标列表，最多各占 O(m) 空间。  
  - 最坏情况下 m≈n，所以 **O(n)** 的额外空间。  
  - 这相当于我们额外准备了一个装元音的盒子和一个装位置的盒子。

#### 代码（Python）

```python
def sortVowels_bruteforce(s: str) -> str:
    # 判断字符是否为元音（大小写都算）
    def is_vowel(ch: str) -> bool:
        return ch.lower() in {'a', 'e', 'i', 'o', 'u'}

    # 1. 收集所有元音及其所在位置
    vowels = []          # 用来存放元音字符
    idxs   = []          # 用来存放对应的下标
    for i, ch in enumerate(s):
        if is_vowel(ch):
            vowels.append(ch)
            idxs.append(i)

    # 2. 冒泡排序（O(m²)），把元音按 ASCII 从小到大排好
    m = len(vowels)
    for i in range(m):
        for j in range(0, m - i - 1):
            if vowels[j] > vowels[j + 1]:          # ASCII 大的在后面
                vowels[j], vowels[j + 1] = vowels[j + 1], vowels[j]

    # 3. 把排好序的元音放回原来的位置
    s_list = list(s)       # 字符串不可变，先转成列表方便修改
    for pos, ch in zip(idxs, vowels):
        s_list[pos] = ch

    return ''.join(s_list)
```

#### 复杂度

- **时间复杂度**：O(n²)（最坏情况所有字符都是元音，需要做冒泡排序）。  
  - 大白话：如果字符很多且全是元音，排序会像“逐个比大小、换位置”一样慢，耗时会随字符数的平方增长。  
- **空间复杂度**：O(n)（额外存放元音和下标的列表）。  
  - 大白话：我们需要准备两个装东西的盒子，最坏情况下要装下所有字符，所以空间和原字符串长度成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于 O(m²) 的排序**。  
实际上，**Python 自带的 `sorted`（基于 Timsort）可以在 O(m log m) 时间内完成排序**，这已经足够快了。  
再进一步思考：我们不需要自己实现任何复杂的数据结构，只要：

1. **一次遍历把所有元音挑出来**（同暴力解的第 1 步）。  
2. **使用内置排序**一次性把它们排好序（时间 O(m log m)），这一步比冒泡快很多。  
3. 再次遍历原字符串，用排好序的元音依次替换原位置。

这就是 **最优解**——利用语言本身的高效排序函数，省去手写 O(m²) 排序的步骤。

> **核心概念解释**  
> - **内置排序 `sorted`**：它背后使用一种叫 **Timsort** 的算法，最坏情况是 O(k log k)（k 为待排序元素个数），在实际数据里表现极佳。可以把它想象成「超级快速的排队员」——一次性把所有卡片按字母顺序排好。  
> - **列表（List）**：Python 中的列表可以随时增删改，类似「可伸缩的盒子」，非常适合把字符一个个装进去。  
> - **字符的 ASCII 大小写顺序**：大写字母的 ASCII 值比小写字母小，例如 `'A'(65) < 'a'(97)`，所以排序时大写会排在前面，这正是题目要求的「按照 ASCII 排序」。

#### 代码（Python）

```python
def sortVowels_optimal(s: str) -> str:
    # 判断是否为元音（大小写均可）
    def is_vowel(ch: str) -> bool:
        return ch.lower() in {'a', 'e', 'i', 'o', 'u'}

    # 1. 收集所有元音
    vowels = [ch for ch in s if is_vowel(ch)]

    # 2. 使用内置排序（O(m log m)），按 ASCII 从小到大排好
    vowels.sort()                     # 原地排序，也可以写 sorted(vowels)

    # 3. 再遍历原字符串，把排好序的元音依次填回
    res = []               # 用来构造最终字符串
    vowel_idx = 0          # 指向下一个要取出的已排序元音

    for ch in s:
        if is_vowel(ch):
            res.append(vowels[vowel_idx])   # 用排好序的元音替换
            vowel_idx += 1
        else:
            res.append(ch)                  # 辅音保持不变

    return ''.join(res)
```

#### 复杂度

- **时间复杂度**：O(n log m)  
  - 第一次遍历 O(n) 收集元音。  
  - 排序 O(m log m)（m 为元音个数，最多等于 n）。  
  - 第二次遍历 O(n) 生成结果。  
  - 综合来看，最坏情况下 m≈n，时间为 O(n log n)。  
  - 与暴力解的 O(n²) 相比，**对大数据（如 10⁵ 长度）提升巨大**——从「平方级」降到「对数级」。
- **空间复杂度**：O(m)  
  - 只需要额外存放元音列表和结果列表，最多占原字符串长度的两倍。  
  - 相比暴力解，这里没有额外的下标列表，空间略有减少。

---

## 心得

- **核心技巧**：先把需要排序的子集合抽出来，用高效排序后再「回填」原位置。  
- **适用的题型**  
  1. **只对特定字符或数字排序**（如「只对奇数排序」）。  
  2. **保持相对位置不变，只改变子序列的顺序**（如「保留空格位置，只排序字母」）。  
  3. **分离并排序特定属性的元素**（如「按年龄排序员工列表，只排序年龄」）。  
- **一句话总结解题钥匙**：**「先抽离再排序」**——把需要操作的部分单独拿出来，用最快的排序方式处理，然后再把结果放回原位。

---

## 反思

- **第一反应**：看到“只对元音排序”，自然想到遍历一次把元音收集起来，排序后再写回。  
- **最容易踩的坑**  
  - **大小写区别**：元音的判断要同时兼容大写和小写，忘记 `ch.lower()` 会导致遗漏。  
  - **ASCII 排序**：直接使用 `sorted` 会自动按 ASCII 排序，若误用了 `key=str.lower` 会把大写放到后面，违背题目要求。  
  - **空字符串或全辅音**：若没有元音，排序列表为空，仍要保证程序正常返回原字符串。  
- **下次类似题的第一步**：**「先定位需要变动的子集」**——明确哪些字符需要排序或重排，然后再考虑如何高效处理。