# #2262. 字符串的总吸引力 / Total Appeal of A String

> 难度：困难 · 标签：Hash Table、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/total-appeal-of-a-string/)

---

## 题目（英文原版）

**Description**

The appeal of a string is the number of distinct characters found in the string.
Given a string s, return the total appeal of all of its substrings.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "abbca"
Output: 28
Explanation: The following are the substrings of "abbca":
- Substrings of length 1: "a", "b", "b", "c", "a" have an appeal of 1, 1, 1, 1, and 1 respectively. The sum is 5.
- Substrings of length 2: "ab", "bb", "bc", "ca" have an appeal of 2, 1, 2, and 2 respectively. The sum is 7.
- Substrings of length 3: "abb", "bbc", "bca" have an appeal of 2, 2, and 3 respectively. The sum is 7.
- Substrings of length 4: "abbc", "bbca" have an appeal of 3 and 3 respectively. The sum is 6.
- Substrings of length 5: "abbca" has an appeal of 3. The sum is 3.
The total sum is 5 + 7 + 7 + 6 + 3 = 28.
```

**Example 2:**

```
Input: s = "code"
Output: 20
Explanation: The following are the substrings of "code":
- Substrings of length 1: "c", "o", "d", "e" have an appeal of 1, 1, 1, and 1 respectively. The sum is 4.
- Substrings of length 2: "co", "od", "de" have an appeal of 2, 2, and 2 respectively. The sum is 6.
- Substrings of length 3: "cod", "ode" have an appeal of 3 and 3 respectively. The sum is 6.
- Substrings of length 4: "code" has an appeal of 4. The sum is 4.
The total sum is 4 + 6 + 6 + 4 = 20.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.

---

## 题目（中文翻译）

一个字符串的吸引力（appeal）是该字符串中不同字符的数量。  
给定字符串 `s`，返回其所有子串（substring）的总吸引力。  
子串（substring）是字符串中连续的字符序列。

**示例 1**  
**输入**: `s = "abbca"`  
**输出**: `28`  
**解释**: `"abbca"` 的所有子串如下：  
- 长度为 1 的子串: `"a"`, `"b"`, `"b"`, `"c"`, `"a"` 的吸引力分别为 1, 1, 1, 1, 1，累计为 5。  
- 长度为 2 的子串: `"ab"`, `"bb"`, `"bc"`, `"ca"` 的吸引力分别为 2, 1, 2, 2，累计为 7。  
- 长度为 3 的子串: `"abb"`, `"bbc"`, `"bca"` 的吸引力分别为 2, 2, 3，...（已截断）

**示例 2**  
**输入**: `s = "code"`  
**输出**: `20`  
**解释**: `"code"` 的所有子串如下：  
- 长度为 1 的子串: `"c"`, `"o"`, `"d"`, `"e"` 的吸引力分别为 1, 1, 1, 1，累计为 4。  
- 长度为 2 的子串: `"co"`, `"od"`, `"de"` 的吸引力分别为 2, 2, 2，累计为 6。  
- 长度为 3 的子串: `"cod"`, `"ode"` 的吸引力分别为 3, 3，累计为 6。  
- 长度为 4 的子串: `"code"` 的吸引力为 4，...（已截断）

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有子串**，对每个子串统计它包含多少种不同的字符（即“appeal”），再把所有子串的 appeal 加起来。

- **枚举子串**：可以用两个循环 `i`（子串左端）和 `j`（子串右端）遍历所有 `i ≤ j` 的区间。
- **统计不同字符**：对每个子串建立一个集合（`set`），把子串里的字符逐个放进去，集合的大小就是该子串的 appeal。  
  集合在生活中的类比：就像查字典，往字典里装词条，最后看有多少页码（不同词条）被使用。

**为什么正确**：我们遍历了 **所有** 连续子串，并且对每个子串都准确计算了它的 distinct character 数目，求和自然得到答案。

**时间/空间复杂度**（大白话版）：

- 时间：外层 `i` 循环 O(n)，内层 `j` 循环最多 O(n) 次，且每次往集合里插入字符最坏要 O(1)（哈希表），但集合要遍历子串的字符，整体是 O(n³)？  
  实际上我们在遍历 `j` 时可以把子串的字符一次性加入集合，**每个左端 i** 需要 O(n) 的插入操作，总共 O(n²) 次插入，集合大小最多 26（字母表），所以 **整体时间是 O(n²)**。  
  用大白话说：如果字符串长 10⁴，时间大概是 10⁴ × 10⁴ = 100 000 000 次操作，已经很慢了。

- 空间：每次我们都要一个集合保存当前子串的字符，最多 26 个字符，所以 **O(1)**（常数空间）。如果把所有子串的集合都保留下来，那就是 O(n²)，但我们只需要临时的一个集合。

#### 代码（Python）

```python
def appealSum_bruteforce(s: str) -> int:
    n = len(s)
    total = 0

    # i 为子串的左端
    for i in range(n):
        distinct = set()          # 用集合记录当前子串出现的字符
        # j 为子串的右端，逐步扩展子串 [i, j]
        for j in range(i, n):
            distinct.add(s[j])    # 把新字符放进集合，集合会自动去重
            total += len(distinct)   # 当前子串的 appeal 加到答案里

    return total
```

#### 复杂度

- **时间复杂度**：O(n²)  
  意味着如果字符串长度是 10⁴，需要大约 10⁸ 次基本操作，实际运行会比较慢。

- **空间复杂度**：O(1)  
  只用了一个大小不超过 26 的集合，和字符串长度无关。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现 **瓶颈** 在于每次都要遍历子串来统计不同字符。  
如果能在 **遍历一次字符串** 的过程中，直接得到“以当前位置 i 为右端的所有子串的 appeal”，就可以把时间降到线性。

**关键观察**：

1. 对于固定的字符 `c`（比如 `'a'`），它对以位置 `i` 结尾的子串的贡献，只取决于它最近一次出现的位置。  
   - 记 `last[c]` 为字符 `c` 上一次出现的下标（从 0 开始），如果 `c` 从未出现过，则 `last[c] = -1`。  
   - 那么以 `i` 为右端的子串中，**包含字符 `c` 的子串数量** = `i - last[c]`。  
     解释：所有左端 `L` 必须满足 `last[c] < L ≤ i`，左端可以取 `i-last[c]` 种可能。

2. 对所有 26 个小写字母求和，得到 **以 i 为右端的子串的总 appeal**。  
   把每个位置的贡献累加，就得到整个字符串所有子串的总 appeal。

3. 为了在 O(1) 时间得到 `i - last[c]`，我们维护一个长度为 26 的数组 `last`，随时更新每个字符的最新出现位置。

**算法步骤**：

- 初始化 `last` 为 `[-1] * 26`（-1 表示“从未出现过”），`cur = 0`（当前以 i 为右端的子串的 appeal），`ans = 0`（最终答案）。
- 从左到右遍历字符串，设当前下标为 `i`，字符为 `ch`。
  1. 计算 `idx = ord(ch) - ord('a')`，得到字符在数组中的索引。
  2. 更新 `last[idx] = i`（记录最新出现位置）。
  3. 重新计算 `cur`：遍历所有 26 个字符，`cur += i - last[j]`（如果 `last[j] == -1`，则 `i - (-1) = i+1`，表示该字符在所有子串中都算作 “不存在”，但公式仍然成立，因为 `i - (-1)` 实际上是 `i+1`，对应所有左端均合法）。
  4. 把 `cur` 加到答案 `ans` 中。

**为什么正确**：  
对每个字符 `c`，`i - last[c]` 正好是左端 `L` 的合法取值个数，使得子串 `[L, i]` 包含 `c`。把所有字符的合法子串数相加，就得到 **以 i 为右端的所有子串的 distinct character 总数**，即该位置的 appeal。累加所有位置即为题目要求的总和。

**类比**：  
想象有 26 把钥匙（每个字母对应一把），每次出现字母时，就把对应的钥匙插到最新的锁孔（位置 i）。要统计所有以 i 为终点的房间里有多少把钥匙在用，只需要看每把钥匙最近插入的锁孔位置，剩下的房间（左端）都是合法的。

#### 代码（Python）

```python
def appealSum(s: str) -> int:
    """
    返回所有子串的 appeal 之和，时间 O(n)，空间 O(1)
    """
    n = len(s)
    last = [-1] * 26               # 记录每个字符最近出现的下标，-1 表示还未出现
    cur_appeal = 0                 # 以当前位置 i 为右端的子串的总 appeal
    ans = 0                        # 最终答案

    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')   # 把字符映射到 0~25 的下标

        # 更新该字符的最近出现位置
        last[idx] = i

        # 重新计算以 i 为右端的子串的 appeal
        cur_appeal = 0
        for pos in last:
            # 对于字符 c，合法的左端 L 必须 > pos，左端可以取 i - pos 种
            cur_appeal += i - pos

        ans += cur_appeal          # 累加到全局答案

    return ans
```

> **代码说明**  
> - `last` 类似“字典”，但因为字符只有 26 种，用列表更快。把它想象成 **查字典**：key 是字母，value 是它最近出现的下标。  
> - `i - pos` 的含义：从 `pos+1` 到 `i`（共 `i-pos` 个位置）都可以作为子串的左端，使得该子串一定包含这个字符。  
> - 循环遍历 26 次是常数时间（26 是固定的），所以整体是线性 O(n)。

#### 复杂度

- **时间复杂度**：O(n)  
  我们只遍历一次字符串，每个位置内部只遍历固定的 26 次（与字符串长度无关），所以即使 `n = 10⁵`，运行也非常快。

- **空间复杂度**：O(1)  
  只用了长度为 26 的数组 `last`，占用常数空间，和输入大小无关。

---

## 心得

- **核心技巧**：利用**每个字符最近出现位置**来直接计算“以当前索引结尾的子串中包含该字符的个数”。这是一种**前缀贡献**的思路，常用于统计子数组/子串的某类属性。
- **适用题型**：  
  1. “子数组/子串中不同元素的数量求和” 类题（如 LeetCode 828、Count Unique Characters of All Substrings of a Given String）。  
  2. “子数组/子串满足某种出现次数限制的计数” （如统计子数组中恰好出现 K 次的元素）。  
  3. “基于最近位置的贡献累加” 类的动态规划/前缀和问题。
- **一句话总结**：**把每个字符的最近出现位置当作“贡献起点”，一次遍历即可把所有子串的 distinct character 统计完。**

---

## 反思

- **第一反应**：想到枚举所有子串，直接统计 distinct 字符，忽视了时间复杂度会爆炸。  
- **最容易踩的坑**：  
  - 忘记把字符未出现时的 `last` 初始化为 `-1`，导致 `i - last` 计算错误。  
  - 在累计 `cur_appeal` 时忘记每次都要重新遍历 26 个字符，导致累计的是错误的递增值。  
  - 对大写字母或非英文字母的输入没有做限制（本题已保证全是小写）。
- **下次遇到同类题**：第一步就思考“能否把子串的贡献拆分到每个位置/每个字符上”，寻找 **最近出现位置** 或 **前缀计数** 这类 **线性时间** 的统计方法。