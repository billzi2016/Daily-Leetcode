# #2900. **最长不相等相邻组子序列 I** / Longest Unequal Adjacent Groups Subsequence I

> 难度：简单 · 标签：Array、String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/longest-unequal-adjacent-groups-subsequence-i/)

---

## 题目（英文原版）

**Description**

You are given a string array words and a binary array groups both of length n.
A subsequence of words is alternating if for any two consecutive strings in the sequence, their corresponding elements at the same indices in groups are different (that is, there cannot be consecutive 0 or 1).
Your task is to select the longest alternating subsequence from words.
Return the selected subsequence. If there are multiple answers, return any of them.
Note: The elements in words are distinct.

**Examples**

**Example 1:**

```
Input: words = ["e","a","b"], groups = [0,0,1]
Output: ["e","b"]
Explanation: A subsequence that can be selected is ["e","b"] because groups[0] != groups[2] . Another subsequence that can be selected is ["a","b"] because groups[1] != groups[2] . It can be demonstrated that the length of the longest subsequence of indices that satisfies the condition is 2 .
```

**Example 2:**

```
Input: words = ["a","b","c","d"], groups = [1,0,1,1]
Output: ["a","b","c"]
Explanation: A subsequence that can be selected is ["a","b","c"] because groups[0] != groups[1] and groups[1] != groups[2] . Another subsequence that can be selected is ["a","b","d"] because groups[0] != groups[1] and groups[1] != groups[3] . It can be shown that the length of the longest subsequence of indices that satisfies the condition is 3 .
```

**Constraints**

- 1 <= n == words.length == groups.length <= 100
- 1 <= words[i].length <= 10
- groups[i] is either 0 or 1.
- words consists of distinct strings.
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个长度为 `n` 的字符串数组 `words` 与一个二进制数组（binary array）`groups`，两者长度相同。  
若子序列（subsequence）`words[i₁], words[i₂], …, words[i_k]` 中任意相邻的两个字符串，其在 `groups` 中对应的元素 **不相等**（即不存在相邻的 `0` 与 `0`，或相邻的 `1` 与 `1`），则称该子序列为 **交替的（alternating）**。  

请从 `words` 中挑选出最长的交替子序列并返回。如果存在多个答案，返回任意一个即可。  
注意：`words` 中的元素互不相同。

---

### 示例

#### 示例 1
**输入**  
```json
words = ["e","a","b"]
groups = [0,0,1]
```
**输出**  
```json
["e","b"]
```
**解释**  
可以选择的交替子序列有 `["e","b"]`，因为 `groups[0] != groups[2]`。另一个可行的子序列是 `["a","b"]`，因为 `groups[1] != groups[2]`。可以证明，满足条件的最长子序列长度为 `2`。

#### 示例 2
**输入**  
```json
words = ["a","b","c","d"]
groups = [1,0,1,1]
```
**输出**  
```json
["a","b","c"]
```
**解释**  
子序列 `["a","b","c"]` 是交替的，因为 `groups[0] != groups[1]` 且 `groups[1] != groups[2]`。另一个可行的子序列是 `["a","b","d"]`，因为 `groups[0] != groups[1]` 且 `groups[1] != groups[3]`。可以证明，满足条件的最长子序列长度为 `3`。

---

### 约束条件
- `1 <= n == words.length == groups.length <= 100`
- `1 <= words[i].length <= 10`
- `groups[i]` 只能为 `0` 或 `1`
- `words` 中的字符串互不相同
- `words[i]` 只包含小写英文字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个位置 `i`，把它当作子序列的最后一个元素，然后看看之前的哪些位置可以接在它前面**。  
如果 `groups[i]` 与前面的某个 `groups[j]`（`j < i`）不相等，那么 `words[j]` 可以紧跟在 `words[i]` 前面，形成一个合法的交替子序列。  

我们可以把 “把之前所有可以接在前面的元素找出来，选出最长的那条路” 用**动态规划**实现：

| 数据结构 | 类比 |
|---|---|
| `dp[i]`（整数） | 像是 “从家到第 `i` 家的最短路程”，这里记录的是**以 `i` 为结尾的最长交替子序列长度** |
| `pre[i]`（整数） | 像是 “前一个路口的编号”，用于在最后把具体的单词序列恢复出来 |

为什么这种方法一定能得到正确答案？  
因为我们枚举了**所有**可能的前驱 `j`（只要 `groups[i] != groups[j]`），并在 `dp[j]` 的基础上加 1，取最大值。这样得到的 `dp[i]` 就是“以 `i` 为结尾的最长合法子序列”。遍历完所有 `i`，最大的 `dp[i]` 就是全局最长长度。

**时间/空间复杂度**  
- 外层循环遍历 `i`（`n` 次），内层循环遍历 `j < i`（最坏 `n` 次），所以总共是 `O(n²)`。  
  - “`O(n²)`” 可以想象成 **每个人都要和所有人握手一次**，如果 `n=100`，最多要握手 10,000 次，仍在电脑能接受的范围。  
- 需要两个长度为 `n` 的数组 `dp`、`pre`，因此是 `O(n)` 的额外空间。

#### 代码（Python）

```python
from typing import List

def longest_alternating_subsequence_bruteforce(words: List[str],
                                               groups: List[int]) -> List[str]:
    n = len(words)
    # dp[i] = 以 i 为结尾的最长交替子序列长度
    dp = [1] * n                # 每个单独的字符本身就是长度 1
    # pre[i] 记录前驱下标，方便后面恢复序列
    pre = [-1] * n

    # 枚举每一个位置作为「结尾」
    for i in range(n):
        # 枚举它之前的所有位置，看看能否接在前面
        for j in range(i):
            # 只有当 groups 不相等时才能接在一起
            if groups[i] != groups[j] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1   # 更新以 i 为结尾的最长长度
                pre[i] = j          # 记录前驱下标

    # 找到最长子序列的结尾下标
    max_len = max(dp)
    idx = dp.index(max_len)

    # 通过 pre[] 把下标倒着恢复成答案
    ans_idx = []
    while idx != -1:
        ans_idx.append(idx)
        idx = pre[idx]
    ans_idx.reverse()               # 逆序得到正确顺序

    # 把下标映射回单词
    return [words[i] for i in ans_idx]
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 这意味着算法的运行时间会随 `n` 的平方增长。比如 `n=100` 时，大约要进行 10,000 次比较，仍然能在毫秒级完成。
- **空间复杂度**：`O(n)`  
  - 只用了两个长度为 `n` 的额外数组，随着 `n` 线性增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历所有前面的元素**，其实我们并不需要这么多信息。  
观察题目：只要相邻的 `groups` 不相等即可，**不要求子序列之间的距离最小**。这意味着：

- 只要我们 **从左到右** 按顺序挑选元素，一旦发现当前 `groups[i]` 与前一个已经挑选的元素的 `group` 不同，就一定可以把它加入答案，且不会影响后面的选择。

换句话说，**只要出现了 “0 → 1” 或 “1 → 0” 的转折点，就把对应的单词拿进来**。这就是**贪心**的思路：每一次都做局部最优（把能够加入的元素立刻加入），最终自然得到全局最长。

为什么贪心是正确的？  
设想任意一个最长交替子序列 `S`，把它的下标写成 `i1 < i2 < ... < ik`。因为 `groups[ij]` 必须交替出现，所以 `ij` 与 `ij+1` 之间一定是一次 “0→1” 或 “1→0”。而我们的贪心算法恰好在每一次出现这种转折时**立刻取第一个出现的下标**，所以它得到的下标序列必然是 `S` 的一个子序列，且长度不可能更短。于是贪心得到的序列也是最长的。

**核心技巧**：一次遍历，比较相邻的 `groups` 是否相等。  
- 类比：把 `groups` 看成一条颜色线，颜色只有黑（0）白（1）两种，只要颜色换了，就把对应的单词“贴”到答案上。

**时间/空间复杂度**  
- 只遍历一次，**`O(n)`** 时间。  
- 只保存答案列表，额外空间同样是 **`O(n)`**（最坏全都被挑选）。

#### 代码（Python）

```python
from typing import List

def longest_alternating_subsequence_greedy(words: List[str],
                                           groups: List[int]) -> List[str]:
    n = len(words)
    if n == 0:
        return []

    # 直接把第一个单词加入答案
    ans = [words[0]]
    # 记录当前答案最后一个元素对应的 group 值
    last_group = groups[0]

    # 从第二个元素开始逐个检查
    for i in range(1, n):
        # 只要当前 group 与上一个已选的不同，就可以加入
        if groups[i] != last_group:
            ans.append(words[i])
            last_group = groups[i]   # 更新最近一次加入的 group
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只需要一次线性扫描，`n` 增大时，运行时间几乎成正比增加。比如 `n=100` 时，只会进行约 100 次比较，几乎是瞬间完成。
- **空间复杂度**：`O(n)`（返回的答案本身需要存放，额外辅助空间是常数）  
  - 只用了几个变量 `last_group`、`ans`，除了答案本身几乎不占额外空间。

---

## 心得

- **核心技巧**：**贪心**——在满足“相邻组不同”这一局部约束时，立刻把当前元素加入答案。
- **适用的题型**  
  1. “最长交替子序列”类（如 LeetCode 376. Wiggle Subsequence）。  
  2. “只要满足相邻不同/相同即可的最长子序列”类（如最长交替颜色序列）。  
  3. “只关心转折点的子序列”类（如从二进制数组中挑选交替 0/1 的最长子序列）。
- **一句话总结解题钥匙**：**只要出现组别切换，就立刻收下对应的单词，整个过程只需一次遍历**。

## 反思

- **第一反应**：看到“交替”“子序列”，立刻想到动态规划，想要枚举所有前驱。  
- **最容易踩的坑**  
  - 忘记子序列不要求连续，导致误以为必须遍历所有子序列组合（指数级）。  
  - 没考虑到 **“从第一个元素开始”** 的特殊性，导致在实现贪心时忘记初始化答案。  
- **下次遇到同类题**，第一步应该先问自己：“**是否只关心相邻元素是否相同**？”如果答案是“是”，那么**尝试一次遍历的贪心**，再检查是否满足所有约束。这样可以迅速从 `O(n²)` 的 DP 跳到 `O(n)` 的最优解。