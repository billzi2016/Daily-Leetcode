# #1957. 删除字符使字符串变为时髦字符串 / Delete Characters to Make Fancy String

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/delete-characters-to-make-fancy-string/)

---

## 题目（英文原版）

**Description**

A fancy string is a string where no three consecutive characters are equal.
Given a string s, delete the minimum possible number of characters from s to make it fancy.
Return the final string after the deletion. It can be shown that the answer will always be unique.

**Examples**

**Example 1:**

```
Input: s = "leeetcode"
Output: "leetcode"
Explanation:
Remove an 'e' from the first group of 'e's to create "leetcode".
No three consecutive characters are equal, so return "leetcode".
```

**Example 2:**

```
Input: s = "aaabaaaa"
Output: "aabaa"
Explanation:
Remove an 'a' from the first group of 'a's to create "aabaaaa".
Remove two 'a's from the second group of 'a's to create "aabaa".
No three consecutive characters are equal, so return "aabaa".
```

**Example 3:**

```
Input: s = "aab"
Output: "aab"
Explanation: No three consecutive characters are equal, so return "aab".
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
时髦字符串（fancy string）是指任意三个连续字符都不相等的字符串。  
给定一个字符串 `s`，请删除最少数量的字符，使得 `s` 变为时髦字符串。  
返回删除后的最终字符串。可以证明答案唯一。

**示例**  

示例 1  
```
Input: s = "leeetcode"
Output: "leetcode"
Explanation:
从第一个连续的 `'e'` 组中删除一个 `'e'`，得到 "leetcode"。
此时不存在三个连续相同的字符，返回 "leetcode"。
```

示例 2  
```
Input: s = "aaabaaaa"
Output: "aabaa"
Explanation:
从第一个连续的 `'a'` 组中删除一个 `'a'`，得到 "aabaaaa"。
再从第二个连续的 `'a'` 组中删除两个 `'a'`，得到 "aabaa"。
此时不存在三个连续相同的字符，返回 "aabaa"。
```

示例 3  
```
Input: s = "aab"
Output: "aab"
Explanation:
没有三个连续相同的字符，直接返回 "aab"。
```

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**不停地在字符串里找出现了 3 个或以上相同字符的连续片段**，然后把多余的字符删掉。  
可以把这个过程想象成：

- **字典**：我们要在一段文字里“查找”连续的相同字符，就像在字典里查单词的定义一样，需要一次遍历才能定位。
- **剪刀**：找到以后，用剪刀把多余的字符剪掉，只留下前两个。

实现上可以这样写：

1. 把原字符串转成列表（因为 Python 的字符串不可变，列表更容易删除）。
2. 从左到右扫描列表，遇到 `i-2, i-1, i` 三个字符相同，就把 `i` 位置的字符删掉（`pop`）。
3. 由于删除会导致后面的字符左移，需要把指针往前退一步，继续检查前面的组合是否又出现了 3 连续相同的情况。
4. 循环结束后，列表里就没有任何 3 连续相同的字符了。

**为什么正确**：每次我们只在出现 3 连续相同的地方删除最右侧的字符，保留前两个。这样做不会影响已经检查过的左侧字符，因为左侧最多只有两个相同的字符；而右侧的字符会在后续的遍历中再次被检查。最终所有连续 3+ 的块都会被削减到长度 2，满足题意。

**复杂度分析（大白话）**  

- **时间**：每删除一次字符，都要把指针往前挪一步，最坏情况下会导致每个字符被检查多次。设字符串长度为 `n`，最坏会出现 `O(n²)` 次比较和删除。可以把它想象成在一条长队里，反复回头检查，每检查一次都要重新排队，花的时间会指数级增长。
- **空间**：我们用了一个字符列表来存放结果，大小和原字符串相同，即 `O(n)`。除此之外只用了常数级别的额外变量。

#### 代码（Python）

```python
def make_fancy_string_bruteforce(s: str) -> str:
    # 把字符串转成列表，方便原地删除
    chars = list(s)
    i = 2                     # 从第三个字符开始检查
    while i < len(chars):
        # 如果当前字符与前两个相同，就删掉当前字符
        if chars[i] == chars[i - 1] == chars[i - 2]:
            chars.pop(i)      # 删除第 i 位，列表长度会自动减 1
            # 删除后，需要把指针往前挪一步，防止漏掉新形成的“三连”
            i = max(i - 2, 2) # 保证 i 不小于 2，防止越界
        else:
            i += 1            # 没有三连，继续向右走
    return ''.join(chars)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - **含义**：如果字符串长度是 10,000，最坏情况下可能要做 100,000,000 次比较，运行时间会明显变慢。
- **空间复杂度**：`O(n)`  
  - **含义**：我们额外用了和原字符串等长的列表来存放字符，所需内存随输入规模线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次删除后都要回退检查**，导致大量重复比较。其实我们不需要“回头”，只要在一次遍历中把符合条件的字符直接跳过即可。

关键观察：

1. **“最多只能保留两个相同字符”**——只要保证结果里没有出现连续 3 个相同字符，就已经是最优的（因为我们每次都尽可能保留字符）。
2. 当我们从左到右构造新字符串时，只需要检查**新加入的字符**和**已经在结果里最后两个字符**是否相同。  
   - 如果相同，则说明加入后会形成 3 连续相同，**此时直接跳过**（相当于“删掉”）。
   - 如果不同，就可以放心加入。

这相当于**单遍扫描 + 构造答案**，不需要任何回溯。可以把它类比为：

- **装配线**：原材料（字符）从左到右进入装配线，装配线的“检查员”只看最近装好的两件产品，决定当前这件是否可以放上去。若会导致“三连”，检查员直接把这件扔掉。

实现步骤：

1. 初始化一个空列表 `res` 用来存放最终字符（相当于答案的“装配线”）。
2. 遍历原字符串的每个字符 `c`：
   - 若 `len(res) >= 2` 且 `res[-1] == res[-2] == c`，说明加入会产生 3 连，**跳过**。
   - 否则，把 `c` 加入 `res`。
3. 循环结束后，把 `res` 转成字符串返回。

这样只遍历一次，时间 `O(n)`，空间只需要保存结果 `O(n)`（实际上也是最小可能的空间，因为答案本身就可能和原字符串等长）。

#### 代码（Python）

```python
def make_fancy_string(s: str) -> str:
    """
    一遍遍历构造答案，保证没有出现连续 3 个相同字符。
    """
    res = []                     # 用列表模拟“答案字符串”，便于追加
    for c in s:
        # 当答案已经有至少两个字符，且这两个字符与当前字符相同
        if len(res) >= 2 and res[-1] == res[-2] == c:
            # 直接跳过当前字符，相当于“删掉”
            continue
        res.append(c)            # 否则把字符加入答案
    return ''.join(res)          # 把列表转成字符串返回
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - **含义**：只需要一次线性扫描，字符数为 100,000 时，只会做约 100,000 次比较，运行非常快。
- **空间复杂度**：`O(n)`  
  - **含义**：我们保存的结果最多和原字符串一样长，已经是必须的最小空间。

---

## 心得

- **核心技巧**：**一次遍历构造答案 + 只检查最近两位**。这是一种常见的“滑动窗口/双指针”思路的简化版。
- **适用的题型**  
  1. “删除字符使字符串满足某种局部约束”——如 *删除重复字符使相邻字符不相同*（LeetCode 1047）。
  2. “压缩字符串”类问题——如 *把相邻相同字符压缩成计数*（LeetCode 443）。
  3. “维护固定窗口内的属性”——如 *最长无重复子串*（LeetCode 3）。
- **一句话总结解题钥匙**：**只要能在加入新字符时判断是否会违反限制，就可以直接跳过，无需回溯。**

## 反思

- **第一反应**：看到“连续三个相同字符”，立刻想到“把多余的删掉”，于是想到逐段统计后删除。  
- **最容易踩的坑**  
  - **边界条件**：字符串长度小于 3 时直接返回原串，代码里需要 `len(res) >= 2` 的判断防止索引错误。  
  - **忘记更新检查条件**：只检查当前字符和前两个字符，别把更早的字符也考虑进去，否则会误删。  
- **下次遇到同类题**：第一步先思考**“加入一个新元素会不会导致局部违规？”**，如果会，就直接舍弃；如果不会，就保留——这往往能直接得到线性时间的最优解。