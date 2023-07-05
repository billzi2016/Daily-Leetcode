# #2309. 大小写字母中最大的英文字母 / Greatest English Letter in Upper and Lower Case

> 难度：简单 · 标签：Hash Table、String、Enumeration · [LeetCode 链接](https://leetcode.com/problems/greatest-english-letter-in-upper-and-lower-case/)

---

## 题目（英文原版）

**Description**

Given a string of English letters s, return the greatest English letter which occurs as both a lowercase and uppercase letter in s. The returned letter should be in uppercase. If no such letter exists, return an empty string.
An English letter b is greater than another letter a if b appears after a in the English alphabet.

**Examples**

**Example 1:**

```
Input: s = "lEeTcOdE"
Output: "E"
Explanation:
The letter 'E' is the only letter to appear in both lower and upper case.
```

**Example 2:**

```
Input: s = "arRAzFif"
Output: "R"
Explanation:
The letter 'R' is the greatest letter to appear in both lower and upper case.
Note that 'A' and 'F' also appear in both lower and upper case, but 'R' is greater than 'F' or 'A'.
```

**Example 3:**

```
Input: s = "AbCdEfGhIjK"
Output: ""
Explanation:
There is no letter that appears in both lower and upper case.
```

**Constraints**

- 1 <= s.length <= 1000
- s consists of lowercase and uppercase English letters.

---

## 题目（中文翻译）

给定一个只包含英文字母（English letters）的字符串 `s`，返回在 `s` 中既以小写形式出现又以大写形式出现的最大英文字母（greatest English letter）。返回的字母应为大写形式。如果不存在这样的字母，返回空字符串。

字母 `b` 大于字母 `a` 当且仅当 `b` 在英文字母表中出现在 `a` 之后。

## 示例

**示例 1**

```text
Input: s = "lEeTcOdE"
Output: "E"
Explanation:
字母 'E' 是唯一同时出现小写和大写形式的字母。
```

**示例 2**

```text
Input: s = "arRAzFif"
Output: "R"
Explanation:
字母 'R' 是同时出现小写和大写形式的最大字母。注意 'A' 和 'F' 也同时出现，但 'R' 大于 'F' 或 'A'。
```

**示例 3**

```text
Input: s = "AbCdEfGhIjK"
Output: ""
Explanation:
不存在同时出现小写和大写形式的字母。
```

## 约束条件

- `1 <= s.length <= 1000`
- `s` 只由小写和大写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把字符串 `s` 的每一个字符都和后面的字符两两比较，看看有没有一对字符是同一个字母但是大小写相反（比如 `'a'` 与 `'A'`）。如果找到了，就把这个字母记下来，最后挑出字母表顺序最大的那一个。

- **用到的数据结构**：这里我们只用到最基本的 **列表**（Python 中的字符串本身就可以当作字符数组）和 **循环**，不需要额外的容器。可以把“遍历所有字符”想象成在一本书里逐页翻，每翻一页就和后面的每一页比较一次——很慢，但最直观。
- **为什么正确**：只要遍历到了所有可能的字符对，就一定不会漏掉任何满足“同时出现大小写”的字母。因此，只要把所有符合条件的字母收集起来，挑出最大的那一个就一定是答案。
- **复杂度分析**：  
  - **时间复杂度**：外层遍历 `n` 次，内层最多再遍历 `n` 次（因为每个字符要和后面的字符比较），所以总共是 `O(n²)`。这里的 `n` 就是字符串的长度，比如 `n = 1000` 时，最坏情况要比较约 1 000 000 次。  
  - **空间复杂度**：只用了常数级的额外空间（存放答案的变量），所以是 `O(1)`。

#### 代码（Python）

```python
def greatestLetter_bruteforce(s: str) -> str:
    n = len(s)
    candidates = []                     # 用来保存所有同时出现大小写的字母

    # 双层循环遍历所有字符对
    for i in range(n):
        for j in range(i + 1, n):
            # 如果两个字符是同一个字母但大小写相反
            if s[i].lower() == s[j].lower() and s[i] != s[j]:
                # 记录大写形式，方便后面比较大小写字母表顺序
                candidates.append(s[i].upper())
                # 已经找到这对字母，后面不需要再比较它们
                break

    # 如果没有任何符合条件的字母，返回空串
    if not candidates:
        return ""

    # 在所有候选字母中挑出字母表顺序最大的（直接使用 max）
    return max(candidates)
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要两层循环，最坏情况下每两个字符都要比较一次。
- **空间复杂度**：`O(1)` — 只用了几个常数级变量（`candidates` 最多 26 个元素，视作常数）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于大量的重复比较：同一个字符会被多次和后面的字符比较，导致 `O(n²)` 的时间。其实我们只需要知道每个字母是否出现过 **大写**、**小写**，不必关心它出现的具体位置。

**优化思路**：

1. **一次遍历** 把所有出现过的字符放进一个 **集合（set）**。集合的特性类似于字典查找——像查字典一样，`O(1)` 时间就能判断一个字符是否已经出现。这里的集合相当于一本“出现过的字符清单”，每次看到新字符就记下来。
2. **从 Z 到 A**（即从字母表的最后往前）检查每个大写字母 `ch`，看集合里是否同时包含 `ch`（大写）和 `ch.lower()`（对应的小写）。因为我们是从大到小检查的，第一次满足条件的字母就是答案，直接返回即可。
3. 如果全部检查完都没有满足条件的字母，返回空串。

**核心数据结构**：**集合（set）**  
- 类比：把集合想象成一本 **“出现过的字符索引”**，每翻一页（检查一个字符）就把它写进去，以后要查某个字符是否出现，只要看这本索引里有没有就行，速度非常快。

**为什么是最优**：我们只遍历字符串一次（`O(n)`），再遍历常数个字母（最多 26 次），整体时间是线性的，空间只需要存放最多 52 个字符（全部英文字母的大写和小写），也是常数级别。

#### 代码（Python）

```python
def greatestLetter(s: str) -> str:
    # 1. 把所有出现过的字符放进集合
    seen = set(s)                     # O(n) 时间，O(1) 空间（最多 52 个字符）

    # 2. 从 'Z' 到 'A' 依次检查
    for code in range(ord('Z'), ord('A') - 1, -1):
        upper = chr(code)             # 当前的大写字母，例如 'Z'
        lower = upper.lower()         # 对应的小写字母，例如 'z'

        # 同时出现大写和小写，就找到了答案
        if upper in seen and lower in seen:
            return upper              # 必须返回大写形式

    # 3. 没有任何满足条件的字母
    return ""
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串（`n` 为字符串长度），再检查 26 次固定字母，时间随输入线性增长。相较于暴力的 `O(n²)`，提升明显。
- **空间复杂度**：`O(1)` — 集合里最多只会有 52 个字符（全部大小写英文字母），不随 `n` 增长。

---

## 心得

- **核心技巧**：利用 **集合**（哈希表）实现 **出现一次即记住**，并结合 **从大到小遍历字母表** 的顺序直接找出最大满足条件的字母。
- **适用题型**：  
  1. “判断字符是否同时出现两种形式” 类题，如 “找出出现过的数字中最大且是偶数的”  
  2. “一次遍历后再做常数次检查” 类题，如 “检查字符串中是否同时出现数字和字母”。  
  3. “使用集合快速去重或查重” 的所有题目。
- **一句话总结解题钥匙**：**先把出现过的字符收进哈希表，再按需求的顺序一次遍历检查**。

## 反思

- **第一反应**：看到“出现大写和小写”，自然会想到“把出现的字符存起来，然后逐个比对”。  
- **最容易踩的坑**：  
  - 忘记返回 **大写** 形式（题目要求），直接返回小写会得错。  
  - 没有从 **Z 到 A**（大到小）遍历，而是从 A 到 Z，导致需要额外的 `max` 操作，失去最优的直接返回。  
  - 对空字符串或没有满足条件的情况返回 `None` 而不是空串 `""`，会导致提交错误。  
- **下次第一步**：**先把所有字符放进集合（或哈希表）**，因为这一步能把“出现”这件事以 O(1) 时间保存下来，为后面的快速检查奠定基础。