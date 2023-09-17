# #2405. 字符串的最优划分 / Optimal Partition of String

> 难度：中等 · 标签：Hash Table、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/optimal-partition-of-string/)

---

## 题目（英文原版）

**Description**

Given a string s, partition the string into one or more substrings such that the characters in each substring are unique. That is, no letter appears in a single substring more than once.
Return the minimum number of substrings in such a partition.
Note that each character should belong to exactly one substring in a partition.

**Examples**

**Example 1:**

```
Input: s = "abacaba"
Output: 4
Explanation:
Two possible partitions are ("a","ba","cab","a") and ("ab","a","ca","ba").
It can be shown that 4 is the minimum number of substrings needed.
```

**Example 2:**

```
Input: s = "ssssss"
Output: 6
Explanation:
The only valid partition is ("s","s","s","s","s","s").
```

**Constraints**

- 1 <= s.length <= 105
- s consists of only English lowercase letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，将其划分为一个或多个子串（substring），要求每个子串中的字符全部唯一，即同一个字符在同一子串中最多出现一次。返回能够满足此条件的划分方案中子串的最小数量。

需要注意的是，划分后每个字符必须恰好属于一个子串。

**示例 1**  
**示例 2**  
**约束条件**：

### 示例

**示例 1**  
```text
Input: s = "abacaba"
Output: 4
Explanation:
两种可能的划分方式分别是 ("a","ba","cab","a") 和 ("ab","a","ca","ba")。
可以证明，4 是满足条件的最少子串数量。
```

**示例 2**  
```text
Input: s = "ssssss"
Output: 6
Explanation:
唯一合法的划分方式是 ("s","s","s","s","s","s")。
```

### 约束条件

- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的切分方式都枚举出来，然后挑选出符合“每个子串里字符不重复”这个条件的、子串数量最少的那一种。  
可以把切分看成在字符串的每两个相邻字符之间放一个“分割点”。长度为 `n` 的字符串有 `n‑1` 个可能的分割位置，每个位置可以 **放** 或 **不放** 分割点，所以所有切分方式的总数是 `2^(n‑1)`，这就是指数级的搜索空间。

> **类比**：想象你在走一条只有左、右两条路的长廊，每一步都可以决定是否在这里拐弯（相当于放一个分割点）。全部走完的所有可能路径就是指数级的。

遍历每一种切分方式：
1. 依据分割点把原字符串切成若干子串。  
2. 检查每个子串里是否有重复字符（可以用 `set` 判断）。  
3. 若全部合法，就记录子串的数量，取最小值。

虽然思路非常直观，但会遍历 **所有** 可能的切分，时间会爆炸。

#### 代码（Python）

```python
def min_partitions_bruteforce(s: str) -> int:
    n = len(s)
    # 2^(n-1) 种切分方式，用二进制表示是否在每个位置分割
    best = n  # 最坏情况每个字符单独成串，最多 n 个子串

    for mask in range(1 << (n - 1)):          # 逐个枚举分割方案
        cnt = 1                                # 子串计数，至少有一个
        start = 0                              # 当前子串的起始下标
        ok = True                              # 标记当前方案是否合法

        for i in range(n - 1):
            if (mask >> i) & 1:                # 在 i 与 i+1 之间放置分割点
                part = s[start:i + 1]          # 取出子串
                if len(set(part)) != len(part):# 判断是否有重复字符
                    ok = False
                    break
                cnt += 1
                start = i + 1

        if ok:                                 # 处理最后一个子串
            part = s[start:]
            if len(set(part)) != len(part):
                ok = False
        if ok:
            best = min(best, cnt)              # 取最小子串数

    return best
```

> 代码中 `mask` 的每一位相当于“是否在这里切断”。  
> `set(part)` 把子串里的字符收集到集合中，集合会自动去重，若集合大小不等于子串长度，则说明有重复字符。

#### 复杂度

- **时间复杂度**：`O(2^{n} * n)`  
  解释：有 `2^{n-1}` 种切分方式，每种方式最坏需要遍历整个字符串来检查重复，故整体是指数级的，几乎不可能在 `n ≤ 10^5` 时通过。

- **空间复杂度**：`O(n)`（主要是递归/循环中保存子串的临时变量）  
  实际上额外使用的空间与字符串长度线性相关，但相对于时间来说并不是瓶颈。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举所有切分** 完全没有必要。我们只需要 **贪心** 地决定何时必须开始一个新子串即可。

**核心观察**：  
从左到右遍历字符串时，只要当前子串里没有出现过的字符，就可以继续往后扩展；一旦出现了已经出现过的字符（即重复），**必须**在此字符之前结束当前子串，开启一个新子串。因为如果不在这里切分，子串里必然会出现重复字符，违背题目要求。

**为什么贪心有效？**  
- 对于已经遍历过的字符，我们已经把它们放进了当前子串，若继续往后加入一个已出现的字符，唯一的解决办法就是把它放到下一个子串。  
- 把子串尽可能延长可以**减少**子串的总数：每新增一个子串只会增加计数，若可以把更多字符放进同一个子串，就不会产生额外的子串。

**实现细节**：

1. 用一个 `set`（哈希表）记录当前子串已经出现的字符。  
   - 哈希表就像一本“查字典”，键是字符，值是“已经出现过”。查找是否已经出现是 `O(1)` 的操作。  
2. 从左到右遍历 `s`：
   - 若字符 `c` 不在 `set` 中，说明可以继续放进当前子串，直接 `add` 到集合。  
   - 若字符 `c` 已经在 `set` 中，说明当前子串已经不能再容纳 `c`，于是：
     - **计数器 +1**（表示完成一个子串）；
     - 清空 `set`，重新开始一个新子串；
     - 把 `c` 加入新的 `set`（因为新子串已经包含了这个字符）。  
3. 循环结束后，还会有最后一个子串未计数，需要再 `+1`。

这样只遍历一次字符串，时间线性。

#### 代码（Python）

```python
def partitionString(s: str) -> int:
    """
    贪心算法：从左到右扫描，遇到重复字符就开启新子串。
    """
    substr_cnt = 0          # 已完成的子串数量
    seen = set()            # 当前子串已经出现的字符集合

    for ch in s:
        if ch in seen:      # 发现重复字符，必须切分
            substr_cnt += 1 # 完成当前子串
            seen.clear()    # 开启新子串，先清空集合
        seen.add(ch)        # 把当前字符放进（新或旧）子串

    # 循环结束后，最后一个子串还未计入
    return substr_cnt + 1
```

**关键行中文注释**：

- `if ch in seen:`  # 判断字符是否已经在当前子串出现过  
- `substr_cnt += 1` # 记录已经结束的子串数量  
- `seen.clear()`  # 清空集合，准备开始新的子串  
- `seen.add(ch)`  # 把当前字符加入当前子串的集合  

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次字符串，`n` 是字符串长度。  
  大白话：如果字符串有 10 万个字符，程序只会看 10 万次，每次操作都是常数时间。

- **空间复杂度**：`O(1)`（严格来说是 `O(Alphabet)`）——集合里最多保存 26 个小写字母，和输入规模无关。  
  类比：就像装东西的背包最多只能装 26 件不同的工具，永远不会因为字符串变长而装得更多。

---

## 心得

- **核心技巧**：**贪心 + 哈希集合**，在遍历过程中即时决定切分点，使每个子串尽可能长。
- **适用的题型**：
  1. “最小子数组划分，使每个子数组满足某种唯一性约束”  
     - 例：`Split Array into Consecutive Subsequences`（连续递增子序列划分）  
  2. “在遍历序列时，遇到冲突立即重新开始”  
     - 例：`Longest Substring Without Repeating Characters`（求最长不含重复字符的子串）  
- **一句话总结**：**只要字符不重复，就把它留在当前子串；一旦重复，立刻切分**——这就是解题钥匙。

---

## 反思

- **第一反应**：看到“每个子串字符唯一”，立刻想到用集合检查重复，然后考虑所有切分的可能性——于是写出了暴力递归。  
- **最容易踩的坑**：
  1. **忘记计数最后一个子串**：循环结束后仍有一个未计数的子串，需要额外 `+1`。  
  2. **集合没有清空**：在切分后必须 `clear()`，否则后面的字符会错误地认为已经出现。  
  3. **字符集大小**：虽然题目只限定小写字母，但如果扩展到更大的字符集，仍然只需要 `O(Alphabet)` 的空间。  
- **下次遇到同类题**：第一步先思考“是否可以一次遍历决定切分点”，如果答案是“可以”，就尝试用**贪心 + 记录状态**（集合、哈希表、计数器）来实现。