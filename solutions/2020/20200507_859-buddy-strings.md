# #859. 伙伴字符串 / Buddy Strings

> 难度：简单 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/buddy-strings/)

---

## 题目（英文原版）

**Description**

Given two strings s and goal, return true if you can swap two letters in s so the result is equal to goal, otherwise, return false.
Swapping letters is defined as taking two indices i and j (0-indexed) such that i != j and swapping the characters at s[i] and s[j].

**Examples**

**Example 1:**

```
Input: s = "ab", goal = "ba"
Output: true
Explanation: You can swap s[0] = 'a' and s[1] = 'b' to get "ba", which is equal to goal.
```

**Example 2:**

```
Input: s = "ab", goal = "ab"
Output: false
Explanation: The only letters you can swap are s[0] = 'a' and s[1] = 'b', which results in "ba" != goal.
```

**Example 3:**

```
Input: s = "aa", goal = "aa"
Output: true
Explanation: You can swap s[0] = 'a' and s[1] = 'a' to get "aa", which is equal to goal.
```

**Constraints**

- 1 <= s.length, goal.length <= 2 * 104
- s and goal consist of lowercase letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `goal`，如果可以通过交换（swap）`s` 中的两个字母使结果等于 `goal`，则返回 `true`；否则返回 `false`。  
交换字母的定义为：取两个下标 `i` 和 `j`（0 索引），且 `i != j`，交换 `s[i]` 与 `s[j]` 处的字符。

**示例 1:**  
```
Input: s = "ab", goal = "ba"
Output: true
Explanation: 你可以交换 s[0] = 'a' 和 s[1] = 'b'，得到 "ba"，与 goal 相等。
```

**示例 2:**  
```
Input: s = "ab", goal = "ab"
Output: false
Explanation: 唯一可以交换的字母是 s[0] = 'a' 和 s[1] = 'b'，交换后得到 "ba" != goal。
```

**示例 3:**  
```
Input: s = "aa", goal = "aa"
Output: true
Explanation: 你可以交换 s[0] = 'a' 和 s[1] = 'a'，仍得到 "aa"，与 goal 相等。
```

**约束条件**
- `1 <= s.length, goal.length <= 2 * 10^4`
- `s` 和 `goal` 仅由小写字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `s` 中所有可能的两两位置 `(i, j)`（`i != j`）都尝试一次换位，然后看换完以后是否和 `goal` 完全相同**。  

- **数据结构**：只需要用到 Python 的字符串（可以把它看成一串字符的链条）和一个临时的列表/字符串来保存换位后的结果。  
- **为什么正确**：题目只允许换一次两字符的位置，所以只要把所有合法的换位情况都枚举一遍，就一定能找到答案（如果答案存在的话）。  
- **时间/空间复杂度**：  
  - 枚举所有 `(i, j)` 组合需要 `C(n,2) = n·(n-1)/2` 次，大约是 **O(n²)**（这里的 `n` 是字符串长度）。  
  - 每一次换位后要把新字符串和 `goal` 比较一次，这一步是 **O(n)** 的线性比较。  
  - 综合下来，总时间是 **O(n³)**（`n²` 次换位 × `n` 次比较），对长度最高 2·10⁴ 的字符串来说根本不可接受。  
  - 额外空间只需要存放临时的换位后字符串，大小为 `n`，即 **O(n)**。

#### 代码（Python）

```python
def buddyStrings_bruteforce(s: str, goal: str) -> bool:
    # 长度不相同直接返回 False
    if len(s) != len(goal):
        return False

    n = len(s)
    # 把字符串转成列表，方便交换字符
    s_list = list(s)

    # 枚举所有 i < j 的位置
    for i in range(n):
        for j in range(i + 1, n):
            # 交换 s[i] 与 s[j]
            s_list[i], s_list[j] = s_list[j], s_list[i]

            # 把列表再拼成字符串，和 goal 做比较
            if ''.join(s_list) == goal:
                return True   # 找到一种合法的换位，使得两串相等

            # 换回来，恢复原状，准备尝试下一个 (i, j)
            s_list[i], s_list[j] = s_list[j], s_list[i]

    # 所有可能都尝试完了，仍然没有相等的情况
    return False
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - `n²` 次遍历所有两两位置，内部的字符串拼接和比较是 `O(n)`，所以总体是立方级别。  
  - 用生活化的说法：如果 `n=1000`，大约要进行 **10⁹** 次操作，电脑跑起来会非常慢。

- **空间复杂度**：`O(n)`  
  - 只用了一个和原字符串等长的列表来做临时换位，额外的内存随字符串长度线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有位置**。实际上，我们不需要真的去尝试每一次换位，只要观察两串之间的差异，就能直接判断是否能通过一次换位得到 `goal`。

分几种情况讨论：

1. **长度不相同**  
   - 直接返回 `False`，因为换位不会改变字符串的长度。

2. **两串完全相等**  
   - 此时如果字符串内部出现 **任意一个字符出现两次或以上**（比如 `"aa"`、`"abca"`），我们可以把这两个相同字符互换，字符串仍保持不变，满足题意。  
   - 检查是否有重复字符可以使用 **哈希表**（在这里用 Python 的 `set`）来统计出现次数。哈希表类似于字典查词：`key` 是字符，`value` 是出现次数。  
   - 如果有重复字符，返回 `True`；否则返回 `False`（因为只能换两个不同位置的字符，而换后会产生变化，导致不等于 `goal`）。

3. **两串不相等**  
   - 记录下所有 **不相同的下标**。如果不相同的下标数量不是 **恰好 2**，说明一次换位无法把两串对齐，直接返回 `False`。  
   - 当恰好有两个不相同的位置 `i`、`j` 时，只要满足 `s[i] == goal[j]` 并且 `s[j] == goal[i]`，就可以通过交换 `s[i]` 与 `s[j]` 使两串相等。  

整个过程只需要一次遍历字符串（`O(n)`），不需要额外的大结构，空间只用来保存不相同的下标和一个字符计数集合，都是 **O(1)**（因为字符集固定为小写英文字母，最多 26 种）。

#### 代码（Python）

```python
def buddyStrings(s: str, goal: str) -> bool:
    # 1️⃣ 长度不同直接否
    if len(s) != len(goal):
        return False

    # 2️⃣ 两串相等的特殊情况
    if s == goal:
        # 检查是否有任意字符出现 >= 2 次
        # 用 set 存已经出现过的字符，如果发现重复就返回 True
        seen = set()
        for ch in s:
            if ch in seen:          # 第三次或第二次出现，说明可以交换相同字符
                return True
            seen.add(ch)
        # 没有重复字符，无法通过一次换位保持不变
        return False

    # 3️⃣ 两串不相等时，找出所有不同的下标
    diff = []                     # 用列表保存不同位置的下标
    for i, (c1, c2) in enumerate(zip(s, goal)):
        if c1 != c2:
            diff.append(i)
            # 只要超过两个不同位置，就可以提前结束
            if len(diff) > 2:
                return False

    # 必须恰好有两个不同位置，且交叉匹配才能成功
    return len(diff) == 2 and \
           s[diff[0]] == goal[diff[1]] and \
           s[diff[1]] == goal[diff[0]]
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串（`n` 为字符串长度），每一步的操作都是常数时间。  
  - 与暴力解的 `O(n³)` 相比，速度提升了 **n²** 倍，实际运行时即使 `n=2·10⁴` 也能在毫秒级完成。

- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外空间（几个变量、一个最多存 2 个下标的列表、一个最多 26 个元素的 `set`）。  
  - 用生活化的说法：不管字符串多长，我们只需要记住几个关键位置和几个字母，就能判断答案。

---

## 心得

- **核心技巧**：**分类讨论 + 只记录关键差异**。  
  - 当两串相等时，判断是否有重复字符；  
  - 当两串不等时，只关心“不相同的下标”是否恰好为 2 并且交叉匹配。  

- **适用的题型**  
  1. **相同字符换位类**：如 LeetCode 859 *`Buddy Strings`*（本题）。  
  2. **只允许一次操作的字符串匹配**：如 1790 *`Check if One String Swap Can Make Strings Equal`*。  
  3. **仅比较差异位置的题目**：如 1630 *`Arithmetic Subarrays`*（需要找出不等位置的数量）。

- **一句话总结**：  
  *“一次换位只能纠正恰好两个错误位置，先找出错误，再看能否交叉匹配；若字符串本来就相等，则需要有可互换的相同字符。”*

---

## 反思

- **第一反应**：直接想遍历所有两两位置尝试换位，结果会超时。  
- **最容易踩的坑**  
  - 忘记处理 `s == goal` 且 **没有重复字符** 的情况，会错误返回 `True`。  
  - 在记录不同位置时，忘记在发现超过两个不相同的位置时提前退出，导致不必要的遍历。  
  - 边界情况：长度为 1 的字符串、全相同字符的长串，都需要正确返回结果。

- **下次类似题目第一步**：  
  *先比较两串是否相等，再统计“不同位置的下标”数量，利用“只能一次操作”这一限制快速做出判断。*