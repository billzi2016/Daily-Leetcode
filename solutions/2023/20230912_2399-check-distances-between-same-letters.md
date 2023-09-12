# #2399. 检查相同字母之间的距离 / Check Distances Between Same Letters

> 难度：简单 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/check-distances-between-same-letters/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s consisting of only lowercase English letters, where each letter in s appears exactly twice. You are also given a 0-indexed integer array distance of length 26.
Each letter in the alphabet is numbered from 0 to 25 (i.e. 'a' -> 0, 'b' -> 1, 'c' -> 2, ... , 'z' -> 25).
In a well-spaced string, the number of letters between the two occurrences of the ith letter is distance[i]. If the ith letter does not appear in s, then distance[i] can be ignored.
Return true if s is a well-spaced string, otherwise return false.

**Examples**

**Example 1:**

```
Input: s = "abaccb", distance = [1,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: true
Explanation:
- 'a' appears at indices 0 and 2 so it satisfies distance[0] = 1.
- 'b' appears at indices 1 and 5 so it satisfies distance[1] = 3.
- 'c' appears at indices 3 and 4 so it satisfies distance[2] = 0.
Note that distance[3] = 5, but since 'd' does not appear in s, it can be ignored.
Return true because s is a well-spaced string.
```

**Example 2:**

```
Input: s = "aa", distance = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: false
Explanation:
- 'a' appears at indices 0 and 1 so there are zero letters between them.
Because distance[0] = 1, s is not a well-spaced string.
```

**Constraints**

- 2 <= s.length <= 52
- s consists only of lowercase English letters.
- Each letter appears in s exactly twice.
- distance.length == 26
- 0 <= distance[i] <= 50

---

## 题目（中文翻译）

**描述**  
给定一个只包含小写英文字母的 0 索引字符串 `s`，其中每个字母恰好出现两次。另给定一个长度为 26 的 0 索引整数数组 `distance`。字母表中的字母按顺序编号为 0 到 25（即 `'a'` → 0，`'b'` → 1，`'c'` → 2，……，`'z'` → 25）。

在一个间距恰当的字符串（well‑spaced string）中，第 `i` 个字母的两次出现之间的字母个数应等于 `distance[i]`。如果第 `i` 个字母未出现在 `s` 中，则可以忽略 `distance[i]`。

返回 `true` 表示 `s` 是间距恰当的字符串，否则返回 `false`。

**示例 1**  
```text
Input: s = "abaccb", distance = [1,3,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: true
Explanation:
- 字母 'a' 出现在索引 0 和 2 处，因此满足 distance[0] = 1。
- 字母 'b' 出现在索引 1 和 5 处，因此满足 distance[1] = 3。
- 字母 'c' 出现在索引 3 和 4 处，因此满足 distance[2] = 0。
- 注意 distance[3] = 5，但由于字母 'd' 未出现在 s 中，可予以忽略。
```

**示例 2**  
```text
Input: s = "aa", distance = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: false
Explanation:
- 字母 'a' 出现在索引 0 和 1 处，两者之间没有字母，即间隔为 0。
由于 distance[0] = 1，s 不是间距恰当的字符串。
```

**约束条件**  
- `2 <= s.length <= 52`
- `s` 仅由小写英文字母组成
- 每个字母在 `s` 中恰好出现两次
- `distance.length == 26`
- `0 <= distance[i] <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每个字母出现的下标都找出来**，然后逐个检查它们之间的间隔是否等于 `distance` 中对应的值。  
- **使用的数据结构**：可以把 26 个字母想成一本字典（哈希表），键（key）是字母，值（value）是这个字母在字符串里出现的所有位置（下标列表）。  
- **为什么正确**：题目说每个字母恰好出现两次，只要我们把这两个下标拿出来，用 `j - i - 1`（两下标之差再减 1）算出它们之间的字符数，和 `distance[字母编号]` 比较，一致就说明这个字母满足要求。所有字母都满足则整体满足。  
- **时间/空间复杂度**：  
  - 暴力实现会对每个字母都遍历整个字符串去找它的出现位置，最坏情况要 **`26 * n` 次比较**（`n` 是字符串长度），这在大 O 记号里写成 **O(n²)**（因为 `n ≤ 52`，常数不大，但理论上是二次级别）。  
  - 需要额外的存放下标的空间，最坏每个字母保存两个下标，整体是 **O(1)**（因为最多 26×2 个整数，视作常数空间）。  

#### 代码（Python）

```python
def checkDistances_bruteforce(s: str, distance: list[int]) -> bool:
    # 逐个字母检查（'a' 到 'z'）
    for ch in range(26):
        letter = chr(ord('a') + ch)          # 把编号转成字符，类似查字典
        first = -1
        second = -1

        # 在整个字符串里找两次出现的位置
        for idx, c in enumerate(s):
            if c == letter:
                if first == -1:               # 第一次出现
                    first = idx
                else:                         # 第二次出现
                    second = idx
                    break                     # 已找到两次，可提前结束本次循环

        # 如果字母根本没出现，就直接跳过（distance 可以忽略）
        if first == -1:
            continue

        # 计算两次出现之间的字符数
        real_dist = second - first - 1
        # 与给定的 distance 比较
        if real_dist != distance[ch]:
            return False                     # 任意一个不匹配就返回 False
    return True
```

#### 复杂度  

- **时间复杂度：O(n²)** — 想象一下，你每检查一个字母，都要把整个字符串从头到尾再跑一遍，像在跑“往返”赛跑，跑的次数会随 `n` 的平方增长。  
- **空间复杂度：O(1)** — 只用了几个整数来记下标，跟字符串长度无关，常数级别的空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**最大的问题在于我们对每个字母都重复遍历字符串**。实际上，只要 **一次遍历** 就能把每个字母的第一次出现位置记下来，等到第二次出现时立刻算出间隔并比较。  

关键点如下：

1. **一次遍历**：用 `enumerate(s)` 同时得到下标 `i` 与字符 `c`。  
2. **记录第一次出现**：准备一个长度为 26 的数组 `first_pos`（把它想成“字母的第一次出现的笔记本”，下标对应字母编号），初始值设为 `-1` 表示“还没见过”。  
3. **遇到第二次出现**：当 `first_pos[idx]` 已经不是 `-1`，说明这就是该字母的第二次出现。此时直接用公式 `i - first_pos[idx] - 1` 计算间隔，与 `distance[idx]` 对比。  
4. **立即返回**：如果发现不匹配，立刻返回 `False`，不必继续遍历。遍历结束后仍未出现不匹配，则返回 `True`。  

这种方法的核心是 **哈希表（这里用数组）**：把字母映射到它第一次出现的下标，查询、插入都是 O(1) 时间，整个过程只需要一次线性扫描。

> **类比**：想象你在超市排队买东西，第一次看到某件商品就把它的编号写在小本子上，等到再次看到同件商品时，你直接翻本子查到第一次的编号，算出两次出现之间隔了多少人，而不需要重新回头数。

#### 代码（Python）

```python
def checkDistances(s: str, distance: list[int]) -> bool:
    # first_pos[i] 保存字母 i（0 对应 'a'）第一次出现的下标，-1 表示还未出现
    first_pos = [-1] * 26

    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')          # 把字符转成 0~25 的编号，类似字典的键

        if first_pos[idx] == -1:          # 第一次出现，记下来
            first_pos[idx] = i
        else:                             # 第二次出现，直接比较间距
            real_dist = i - first_pos[idx] - 1
            if real_dist != distance[idx]:
                return False              # 只要有一个不匹配，立刻返回 False
    return True                           # 所有字母都满足条件
```

#### 复杂度  

- **时间复杂度：O(n)** — 只遍历一次字符串，`n` 是字符串长度（最多 52），相当于一次“跑完马拉松”。  
- **空间复杂度：O(1)** — 额外使用的 `first_pos` 长度固定为 26，视作常数空间。与暴力解相比，时间快了很多，空间保持不变。

---

## 心得  

- **核心技巧**：一次遍历配合「字母 → 第一次出现位置」的哈希表（数组）记录。  
- **适用的题型**：  
  1. “找字母第一次/最后一次出现位置” 类题（如 **1650. 低位相等的最长子序列**）。  
  2. “判断字符间距或出现次数是否满足条件” 类题（如 **2420. 找到所有好下标**）。  
  3. “配对出现的字符” 类题（如 **2421. 好数对的数目**）。  
- **一句话总结**：**只要一次遍历把“第一次出现”记下来，第二次出现时立刻验证，即可得到最优解**。

---

## 反思  

- **第一反应**：看到“每个字母出现两次”，自然想到把每个字母的下标全部找出来，然后比较，这就是暴力思路。  
- **最容易踩的坑**：  
  - **下标计算错误**：间隔是 `j - i - 1`，不要忘记减去 1。  
  - **忽略未出现的字母**：`distance` 中对应未出现字母的值不需要检查。  
  - **字符到编号的映射**：一定要用 `ord(ch) - ord('a')`，否则会越界。  
- **下次遇到同类题**：第一步就想到 “**一次遍历 + 记录第一次出现位置**”，用数组或哈希表保存状态，遇到第二次出现立即判断。这样可以把时间从平方级降到线性级。