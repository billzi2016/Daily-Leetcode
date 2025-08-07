# #3297. 统计可以重新排列后使 word2 成为前缀的子串数量 / Count Substrings That Can Be Rearranged to Contain a String I

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-i/)

---

## 题目（英文原版）

**Description**

You are given two strings word1 and word2.
A string x is called valid if x can be rearranged to have word2 as a prefix.
Return the total number of valid substrings of word1.

**Examples**

**Example 1:**

```
Input: word1 = "bcca", word2 = "abc"
Output: 1
Explanation:
The only valid substring is "bcca" which can be rearranged to "abcc" having "abc" as a prefix.
```

**Example 2:**

```
Input: word1 = "abcabc", word2 = "abc"
Output: 10
Explanation:
All the substrings except substrings of size 1 and size 2 are valid.
```

**Example 3:**

```
Input: word1 = "abcabc", word2 = "aaabc"
Output: 0
```

**Constraints**

- 1 <= word1.length <= 105
- 1 <= word2.length <= 104
- word1 and word2 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`。  
如果一个字符串 `x` 可以通过重新排列（rearranged）后，使 `word2` 成为其前缀（prefix），则称 `x` 为**有效**（valid）字符串。  
返回 `word1` 中所有有效子串（substrings）的总数。

**示例 1**  
``` 
Input: word1 = "bcca", word2 = "abc"
Output: 1
Explanation:
唯一的有效子串是 "bcca"，它可以重新排列为 "abcc"，从而使 "abc" 成为前缀。
```

**示例 2**  
``` 
Input: word1 = "abcabc", word2 = "abc"
Output: 10
Explanation:
除长度为 1 和长度为 2 的子串外，所有子串均为有效。
```

**示例 3**  
``` 
Input: word1 = "abcabc", word2 = "aaabc"
Output: 0
```

**约束条件**

- `1 <= word1.length <= 10^5`
- `1 <= word2.length <= 10^4`
- `word1` 和 `word2` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **word1** 的所有子串都列举出来，逐个检查它们能否“经过重新排列后”以 **word2** 为前缀。  

- **列举子串**：可以用两个循环，外层固定左端点 `i`，内层把右端点 `j` 从 `i` 向右推进，得到子串 `word1[i:j+1]`。这相当于把一根绳子从左到右逐段剪开，所有可能的段都拿出来检查。  
- **检查合法性**：把子串的字符出现次数统计到一个哈希表（在 Python 中用 `collections.Counter`），再把 **word2** 的字符出现次数也统计到另一个哈希表。只要子串里每个字符的数量 **不小于** 对应的 **word2** 中的数量，就说明可以把子串重新排列，使得前 `len(word2)` 个字符恰好是 **word2**。这一步类似于查字典：字典的 “键” 是字符， “值” 是出现次数；我们只要确保子串的每个键对应的值 ≥ 目标字典的值即可。  

**为什么正确**：如果子串包含 **word2** 所需的每种字符的足够数量，那么我们完全可以把这些字符搬到子串的最前面，形成以 **word2** 为前缀的排列。反之，缺少任意一种字符都不可能做到。  

#### 代码（Python）  
```python
from collections import Counter

def count_substrings_brute(word1: str, word2: str) -> int:
    n = len(word1)
    m = len(word2)
    # 先算出 word2 的字符频率，只算一次
    need = Counter(word2)

    ans = 0
    # i 为左端点，j 为右端点（闭区间）
    for i in range(n):
        cur = Counter()               # 当前子串的字符频率
        for j in range(i, n):
            cur[word1[j]] += 1        # 把右端点扩进来
            # 只要子串长度 ≥ word2 长度，才有可能满足前缀要求
            if j - i + 1 >= m:
                # 检查每个字符的数量是否足够
                ok = True
                for ch, cnt in need.items():
                    if cur[ch] < cnt:   # 只要缺少一种字符，就不行
                        ok = False
                        break
                if ok:
                    ans += 1
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n² * 26)`（`n` 为 `word1` 长度）。外层两层循环产生 `≈ n²/2` 个子串，每次检查要遍历 26 个小写字母（实际上只遍历 `need` 中出现的字符），所以整体是二次方级别的。可以把 `O(n²)` 想象成“把 10,000 长的字符串的所有子串都写下来，大约有 50,000,000 条”。  
- **空间复杂度**：`O(26)`（即常数级）。我们只维护两个长度为 26 的计数字典 `need` 与 `cur`，不随子串数量增长。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **重复统计**：窗口每向右扩展一步，都重新遍历整个子串去统计字符。我们可以把“窗口”这根绳子 **滑动**，在移动时 **增删** 端点对应的字符，这样每次只做 **O(1)** 的更新。  

关键观察：

1. **条件单调**  
   对于固定的左端点 `l`，如果窗口 `[l, r]` 已经满足“每种字符的数量 ≥ word2 所需”，那么把右端点继续往右推（即加入更多字符）**仍然满足**。因为我们只是往已有的字符集合里添加新字符，原有的字符数量不会减少。  

2. **最小右端点**  
   对每个左端点 `l`，只要找到最左的、第一次让窗口合法的右端点 `r_min`，那么从 `r_min` 到字符串末尾的所有右端点都合法。于是以左端点 `l` 为起点的合法子串数量就是 `len(word1) - r_min`。  

3. **双指针滑动窗口**  
   - 用指针 `left` 固定左端点，指针 `right` 向右移动寻找 `r_min`。  
   - 维护一个长度为 26 的数组 `window[26]`，记录当前窗口 `[left, right]` 中每个字符的出现次数。  
   - 同时保存 **word2** 的字符需求 `need[26]`。  
   - 判断窗口是否合法，只需要检查 `window[i] >= need[i]` 对所有 `i`（0~25）是否成立。  

滑动过程：

```
right 从 0 开始向右扩，直到窗口合法（或已经到末尾）。
此时以 left 为左端的合法子串数 = n - right。
将 left 向右移动一格，删掉 word1[left] 对应的计数。
如果窗口因为删字符而不再合法，继续让 right 向右扩，直至再次合法。
重复直到 left 扫完全部位置。
```

这样每个字符最多被 `right` 加入一次、被 `left` 删除一次，整体线性时间 `O(n)`。  

#### 代码（Python）  
```python
def count_substrings_opt(word1: str, word2: str) -> int:
    n = len(word1)
    m = len(word2)
    if n < m:                 # 子串长度本身就不足，直接返回 0
        return 0

    # 1）把 word2 的字符需求转成长度为 26 的数组
    need = [0] * 26
    for ch in word2:
        need[ord(ch) - ord('a')] += 1

    # 2）滑动窗口的计数数组
    window = [0] * 26

    # 记录当前窗口是否合法的辅助函数
    def ok() -> bool:
        # 只要有一种字符不够，就返回 False
        for i in range(26):
            if window[i] < need[i]:
                return False
        return True

    ans = 0
    right = 0                 # 窗口右端（闭区间）
    # left 从 0 扫到 n-1
    for left in range(n):
        # 把 right 往右推进，直至窗口合法（或者已经到最右）
        while right < n and not ok():
            idx = ord(word1[right]) - ord('a')
            window[idx] += 1
            right += 1

        # 此时如果仍然不合法，说明后面已经没有可能的子串了，直接结束
        if not ok():
            break

        # 以 left 为左端的合法子串数量 = n - (right-1)
        # 注意 right 已经指向合法窗口的**右侧下一个位置**，所以实际最小合法右端是 right-1
        ans += n - (right - 1)

        # 移动 left，准备考察下一个左端点
        idx_left = ord(word1[left]) - ord('a')
        window[idx_left] -= 1      # 把左端字符从窗口计数中删掉
        # left 增加后，窗口可能不再合法，循环的 while 会再把 right 拉进来

    return ans
```

> **代码要点解释**  
> - `need` 与 `window` 都是长度 26 的列表，索引 `0~25` 分别对应 `'a'~'z'`，类似于“字典的页码”。  
> - `ok()` 每次检查 26 次，时间常数（`26` 远小于 `n`），所以整体仍是线性。  
> - `right` 永远只会向右移动，从不回退，保证每个字符最多被加入一次。  

#### 复杂度  
- **时间复杂度**：`O(n * 26)` → 实际上是 `O(n)`，因为 26 是常数。每个字符只会被 `right` 加入一次、被 `left` 删除一次。与暴力的 `O(n²)` 相比，速度提升了数量级。  
- **空间复杂度**：`O(26)` → 常数级，只用了两个长度为 26 的数组来存计数。  

---

## 心得  

- **核心技巧**：**滑动窗口 + 计数数组**（相当于“字典查表”），利用“合法性单调”把二次遍历降到一次遍历。  
- **适用的题型**  
  1. “子数组/子串的最小/最大长度满足某种计数约束”——例如 *Minimum Window Substring*（最小覆盖子串）。  
  2. “统计满足字符频率要求的子串个数”——例如 *Number of Substrings Containing All Three Characters*。  
  3. “在字符串上找满足某种累计条件的所有区间”——例如 *Subarrays with K Different Integers*。  
- **一句话总结解题钥匙**：**把“能否满足”转化为“窗口计数是否全部≥需求”，利用窗口右端的单调增长一次遍历完成统计**。  

---

## 反思  

- **第一反应**：看到“可以重新排列后拥有 word2 作为前缀”，立刻想到“只要子串包含 word2 所需的字符即可”。于是想到暴力遍历所有子串。  
- **最容易踩的坑**  
  1. **长度不足**：子串长度必须 **≥ len(word2)**，否则不可能拥有足够的字符。  
  2. **窗口合法性检查**：忘记在 `right` 达到字符串末尾后仍要判断一次，导致漏算最后几段。  
  3. **计数数组的负数**：左端移出时要把对应计数减 1，确保不会出现负数导致 `ok()` 误判。  
- **下次遇到同类题**：第一步先思考“是否合法是单调的么？”如果是，就立刻尝试 **双指针/滑动窗口**，并准备好一个 **字符频率数组** 来实现 O(1) 的增删检查。