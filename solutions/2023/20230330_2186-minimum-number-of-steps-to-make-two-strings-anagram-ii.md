# #2186. 将两个字符串变为字母异位词的最少步骤 II / Minimum Number of Steps to Make Two Strings Anagram II

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-steps-to-make-two-strings-anagram-ii/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t. In one step, you can append any character to either s or t.
Return the minimum number of steps to make s and t anagrams of each other.
An anagram of a string is a string that contains the same characters with a different (or the same) ordering.

**Examples**

**Example 1:**

```
Input: s = "leetcode", t = "coats"
Output: 7
Explanation: 
- In 2 steps, we can append the letters in "as" onto s = "leetcode", forming s = "leetcodeas".
- In 5 steps, we can append the letters in "leede" onto t = "coats", forming t = "coatsleede".
"leetcodeas" and "coatsleede" are now anagrams of each other.
We used a total of 2 + 5 = 7 steps.
It can be shown that there is no way to make them anagrams of each other with less than 7 steps.
```

**Example 2:**

```
Input: s = "night", t = "thing"
Output: 0
Explanation: The given strings are already anagrams of each other. Thus, we do not need any further steps.
```

**Constraints**

- 1 <= s.length, t.length <= 2 * 105
- s and t consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`。在一次操作中，你可以向 `s` 或 `t` 任意一侧追加（append）任意字符。  
返回使 `s` 与 `t` 成为字母异位词（anagram）的最少操作次数。  

字母异位词（anagram）指的是字符组成相同、顺序可以不同（也可以相同）的字符串。

**示例 1**  
**输入**: `s = "leetcode", t = "coats"`  
**输出**: `7`  
**解释**:  
- 在 2 步内，我们可以把 `"as"` 追加到 `s = "leetcode"`，得到 `s = "leetcodeas"`。  
- 在 5 步内，我们可以把 `"leede"` 追加到 `t = "coats"`，得到 `t = "coatsleede"`。  
`"leetcodeas"` 与 `"coatsleede"` 现在是字母异位词。  
总共使用了 `2 + 5 = 7` 步。  
可以证明不存在使用更少步数的方法。

**示例 2**  
**输入**: `s = "night", t = "thing"`  
**输出**: `0`  
**解释**: 给定的两个字符串已经是字母异位词，无需任何操作。

**约束条件**  
- `1 <= s.length, t.length <= 2 * 10^5`  
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两串字符一个一个对比**，看哪些字符在两边的出现次数不一样，然后把缺少的字符“补”进去。  
可以把这个过程想象成两个人在玩拼字游戏：

1. 第一个人手里有字符串 `s`，第二个人手里有字符串 `t`。  
2. 两个人把自己的每个字母一个一个拿出来，和对方的字母进行配对。  
3. 配不上的字母就是需要“追加”的字符。  

实现上最笨的办法是：

- 对 `s` 中的每个字符，去 `t` 中找一模一样的字符（用两层循环），如果找到了就把这两个字符标记为“已配对”。  
- 再把剩下没有配对的字符全部计数，这些字符的数量就是需要追加的步数。  

因为每次寻找都要遍历一次对方的全部字符，这相当于 **两层循环**，时间会是 `O(|s| * |t|)`，在最坏情况下接近 `O(n²)`（`n` 为两串长度的最大值）。  

> **为什么这种方法能得到正确答案？**  
> 只要把每个字符都尝试配对一次，配不上的字符一定是两串字符频数不相等的部分。把它们全部补齐后，两串必然拥有相同的字符集合，也就是互为字母异位词（anagram）。

#### 代码（Python）

```python
def minSteps_brute(s: str, t: str) -> int:
    # 把字符列表化，方便标记是否已配对
    s_list = list(s)
    t_list = list(t)

    # visited 用来标记 t 中的字符是否已经被配对
    visited = [False] * len(t_list)

    # 已配对的字符数量
    matched = 0

    # 双层循环：遍历 s 中的每个字符，尝试在 t 中找相同的字符
    for i, ch_s in enumerate(s_list):
        for j, ch_t in enumerate(t_list):
            if not visited[j] and ch_s == ch_t:   # 找到未配对且相同的字符
                visited[j] = True                # 标记 t[j] 已配对
                matched += 1                     # 配对成功计数加一
                break                            # 该 s[i] 已配对，去找下一个

    # 需要追加的字符数 = 两串总长度 - 已配对字符数 * 2
    # （每对配好的字符在最终的 anagram 中出现两次）
    total_len = len(s) + len(t)
    steps = total_len - 2 * matched
    return steps
```

#### 复杂度

- **时间复杂度**：`O(|s| * |t|)`  
  用大白话说，就是如果 `s` 长 10，`t` 长 10，需要比较 100 次；如果两串都是 10⁵ 长，就要比较 10¹⁰ 次，几乎不可能在合理时间内跑完。

- **空间复杂度**：`O(|t|)`  
  只用了一个 `visited` 数组来记录 `t` 中字符是否已配对，额外空间与 `t` 长度成正比。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于每次都要遍历整串去找匹配**。其实我们并不需要知道“哪一个具体字符配对了”，只需要知道每个字母在两串里出现了多少次。  

> **关键观察**  
> 两个字符串是字母异位词 ⇔ 对每个英文字母 `'a' … 'z'`，它们的出现次数相同。  
> 因此，只要把每个字母的出现次数算出来，比较两边的差值，差值的绝对值就是需要追加的字符数。  

这正好可以用 **哈希表（或数组）** 来实现：  
- 把 `s` 的每个字符计数放进数组 `cnt[26]`（下标 0 对应 `'a'`，1 对应 `'b'`，依此类推）。  
- 再遍历 `t`，对相同的下标减去计数。  
- 最后把数组中每个位置的绝对值相加，就是最少的追加步数。  

> **类比**  
> 把 `cnt` 想成一本 **字典**，键是字母，值是“当前多余多少”。  
> - 当遍历 `s` 时，向字典里“存入”字母（值加 1）。  
> - 当遍历 `t` 时，向字典里“取出”字母（值减 1）。  
> 最终每个键的值正负表示两串的差距，取绝对值并相加就是答案。

#### 代码（Python）

```python
def minSteps(s: str, t: str) -> int:
    """
    最优解：只用一次遍历统计字符频率，时间 O(|s| + |t|)，空间 O(1)（固定 26 长度数组）。
    """
    # 26 个小格子，分别对应 'a' ~ 'z' 的计数差值
    diff = [0] * 26

    # 把 s 中每个字符的计数加一
    for ch in s:
        idx = ord(ch) - ord('a')   # 计算字符在数组中的下标
        diff[idx] += 1

    # 把 t 中每个字符的计数减一
    for ch in t:
        idx = ord(ch) - ord('a')
        diff[idx] -= 1

    # 统计所有字符差值的绝对值之和，即为最少的追加步数
    steps = sum(abs(x) for x in diff)
    return steps
```

#### 复杂度

- **时间复杂度**：`O(|s| + |t|)`  
  只需要一次遍历 `s` 和一次遍历 `t`，相当于把两串的长度加起来的线性时间。与暴力解相比，省掉了大量的“寻找配对”操作，快得多。

- **空间复杂度**：`O(1)`（常数空间）  
  虽然用了一个长度为 26 的数组，但它的大小不随输入规模变化，始终是常数。

---

## 心得

- **核心技巧**：利用字符计数（哈希表/数组）比较两串的频率差。  
- **适用的题型**：  
  1. “使两个字符串成为字母异位词”系列（如 LeetCode 1347、1657）。  
  2. “最少删除使两个字符串相同”类问题（如 LeetCode 583）。  
  3. “找出字符串中出现次数最多的字符”类统计题。  
- **一句话总结解题钥匙**：**把字符当作“字典的键”，只比较出现次数的差值**。

---

## 反思

- **第一反应**：看到“把字符追加到任意一串”，直觉上会想到“把缺的字符补上”。于是想到逐个配对的暴力实现。  
- **最容易踩的坑**：  
  - 忽略了字符顺序无关，错误地尝试使用排列或子序列的思路。  
  - 没有考虑到只需要计数，不需要真的构造新的字符串，导致不必要的空间与时间浪费。  
  - 边界情况：空字符串或只有一种字符的极端情况，都能通过计数方法统一处理。  
- **下次遇到同类题的第一步**：**先问自己“是否只关心字符出现次数？”** 若答案是肯定的，就直接用计数（哈希表/数组）来求解。