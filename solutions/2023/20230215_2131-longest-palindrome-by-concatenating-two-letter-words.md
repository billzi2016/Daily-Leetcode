# #2131. **通过连接两个字母单词构造最长回文串** / Longest Palindrome by Concatenating Two Letter Words

> 难度：中等 · 标签：Array、Hash Table、String、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/longest-palindrome-by-concatenating-two-letter-words/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words. Each element of words consists of two lowercase English letters.
Create the longest possible palindrome by selecting some elements from words and concatenating them in any order. Each element can be selected at most once.
Return the length of the longest palindrome that you can create. If it is impossible to create any palindrome, return 0.
A palindrome is a string that reads the same forward and backward.

**Examples**

**Example 1:**

```
Input: words = ["lc","cl","gg"]
Output: 6
Explanation: One longest palindrome is "lc" + "gg" + "cl" = "lcggcl", of length 6.
Note that "clgglc" is another longest palindrome that can be created.
```

**Example 2:**

```
Input: words = ["ab","ty","yt","lc","cl","ab"]
Output: 8
Explanation: One longest palindrome is "ty" + "lc" + "cl" + "yt" = "tylcclyt", of length 8.
Note that "lcyttycl" is another longest palindrome that can be created.
```

**Example 3:**

```
Input: words = ["cc","ll","xx"]
Output: 2
Explanation: One longest palindrome is "cc", of length 2.
Note that "ll" is another longest palindrome that can be created, and so is "xx".
```

**Constraints**

- 1 <= words.length <= 105
- words[i].length == 2
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `words`，其中每个元素都是由两个小写英文字母组成的单词。  
你可以从 `words` 中选择若干个元素（每个元素最多选择一次），按照任意顺序将它们连接（concatenate）起来，构造一个回文串（palindrome）。返回可以构造的最长回文串的长度。如果无法构造任何回文串，返回 `0`。

> **回文串** 是指正读和反读完全相同的字符串。

### 示例

**示例 1**  
```text
Input: words = ["lc","cl","gg"]
Output: 6
Explanation: 最长的回文串之一是 "lc" + "gg" + "cl" = "lcggcl"，长度为 6。
另外，"clgglc" 也是可以构造的最长回文串。
```

**示例 2**  
```text
Input: words = ["ab","ty","yt","lc","cl","ab"]
Output: 8
Explanation: 最长的回文串之一是 "ty" + "lc" + "cl" + "yt" = "tylcclyt"，长度为 8。
另外，"lcyttycl" 也是可以构造的最长回文串。
```

**示例 3**  
```text
Input: words = ["cc","ll","xx"]
Output: 2
Explanation: 最长的回文串之一是 "cc"，长度为 2。
同样，"ll" 和 "xx" 也都是可以构造的最长回文串。
```

### 约束条件

- `1 <= words.length <= 10^5`
- `words[i].length == 2`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：把 **所有** 可能的子集都枚举出来，尝试每一种排列组合，判断拼接后的字符串是否是回文，如果是就记录它的长度，最后取最大值。  

- **数据结构**：  
  - 用列表 `subset` 保存当前挑选的若干单词。  
  - 用 `itertools.permutations` 生成所有排列，类似把单词排成一条“队伍”。  
  - 判断回文时，把所有单词拼成一个大字符串，然后像检查普通句子是否回文一样，从两端向中间比较字符。  

- **为什么正确**：  
  - 我们遍历了 **所有** 合法的挑选方式和排列顺序，只要有一种能组成回文，就一定会在枚举过程中被检查到，自然也能找到最长的那一个。

- **复杂度分析（大白话）**：  
  - 假设有 `n` 个单词。  
  - 子集的数量是 `2^n`（每个单词要么选要么不选），每个子集内部又要排列，最坏情况下是 `k!`（`k` 是子集大小），所以总的操作次数大约是 `O(n! )`，这在实际中几乎不可能跑完。  
  - 空间上我们只需要存当前的子集和排列，最多 `O(n)`。  

> **时间复杂度 O(n! )**：这里的 `!` 表示“阶乘”，比如 `5! = 5×4×3×2×1 = 120`，随 `n` 增大增长非常快，几分钟内就会爆炸。  
> **空间复杂度 O(n)**：只跟输入规模线性相关，存几个临时数组。

#### 代码（Python）  

```python
import itertools

def is_palindrome(s: str) -> bool:
    """判断字符串 s 是否是回文，像检查镜子里的文字一样"""
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True

def longest_palindrome_bruteforce(words):
    n = len(words)
    best = 0

    # 逐个子集（用二进制位表示是否选取）
    for mask in range(1, 1 << n):          # 1<<n == 2**n
        subset = [words[i] for i in range(n) if mask & (1 << i)]

        # 子集内部所有排列
        for perm in itertools.permutations(subset):
            candidate = ''.join(perm)      # 把单词连成一个大字符串
            if is_palindrome(candidate):
                best = max(best, len(candidate))

    return best

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(longest_palindrome_bruteforce(["lc", "cl", "gg"]))   # 6
    print(longest_palindrome_bruteforce(["ab","ty","yt","lc","cl","ab"]))   # 8
    print(longest_palindrome_bruteforce(["cc","ll","xx"]))   # 2
```

> 这段代码只能在 **极小** 的测试数据上跑通，主要用来帮助大家理清“枚举所有可能”这一最原始思路。

#### 复杂度  

- **时间复杂度**：`O(n! )`（指数级爆炸），因为我们要遍历所有子集并对每个子集做全排列。  
- **空间复杂度**：`O(n)`，只存当前子集和排列的临时列表。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**枚举所有排列** 是最大的性能瓶颈。  
我们需要利用题目给出的特殊信息：

1. **每个单词恰好两个字母**。  
2. **回文的本质是“左边的东西要和右边的东西完全相反”。**  

把这两点结合，就可以把问题转化为“配对”而不是“排列”。

---

**步骤 1：统计每个单词出现的次数**  
使用哈希表（Python 的 `dict`）记录每个两字母单词出现了多少次。  
哈希表就像一本“字典”，键是单词，值是出现次数。

**步骤 2：处理互为翻转的单词**  
对于任意单词 `ab`（`a != b`），它的“镜像”必须是 `ba` 才能在回文的两侧对应。  
我们可以把 `ab` 和 `ba` 配成一对，使用的次数是两者出现次数的 **最小值**（因为配对需要一对一）。  
每配成一对，就能往回文左侧加 `ab`，右侧加 `ba`，长度增加 `4`（每个单词长度 2，左右各两段）。

**步骤 3：处理自身就是回文的单词**  
形如 `aa`、`bb` 的单词本身已经是回文。  
- **成对使用**：把两个相同的回文单词放在左右两侧，同样能贡献 `4` 长度。  
- **中心单词**：如果还有剩余的回文单词（至少一个），可以把 **恰好一个** 放在最中间，贡献 `2` 长度，且只能放一次，因为回文的中心只能有一个“单独的块”。

**步骤 4：把所有贡献加起来**  
把步骤 2、3 的长度累加，即得到最长回文的长度。

---

**为什么这样是最优的？**  

- 对于 `ab` 与 `ba`，只能配对使用 `min(cnt[ab], cnt[ba])` 次，配更多就会缺少对应的镜像，导致不对称，无法形成回文。  
- 对于自回文单词 `aa`，每两个可以形成一对，剩下的最多只能放在中心一次，放两次会破坏对称性。  
- 所有能够贡献长度的地方我们都已经利用到了，剩下的单词要么没有对应的镜像，要么已经用了中心位，无法再加入，故此方案一定是最长的。

---

#### 代码（Python）  

```python
from collections import Counter

def longestPalindrome(words):
    """
    返回可以拼成的最长回文的长度
    思路：统计出现次数 → 配对互为翻转的单词 → 处理自身回文的单词
    """
    cnt = Counter(words)          # 哈希表：单词 → 出现次数
    ans = 0                       # 累计已经确定的长度
    used_center = False           # 标记中心是否已经放了一个自回文单词

    for w in list(cnt.keys()):    # 遍历所有出现过的单词
        rev = w[::-1]              # 翻转，例如 "ab" -> "ba"

        if w == rev:               # 情况 1：自身就是回文，如 "aa"
            pairs = cnt[w] // 2    # 能组成多少对
            ans += pairs * 4       # 每对贡献 4（左+右各两个字符）
            cnt[w] -= pairs * 2    # 用掉这些单词

            # 还有剩余的 "aa" 可以放在中间一次
            if cnt[w] > 0 and not used_center:
                ans += 2           # 中心单词贡献 2
                used_center = True
                cnt[w] = 0         # 中心已经用掉

        elif w < rev:              # 为了避免重复计数，只在 w < rev 时处理一次
            # 情况 2：互为翻转的单词，如 "ab" 与 "ba"
            pair_cnt = min(cnt[w], cnt.get(rev, 0))
            ans += pair_cnt * 4    # 每对贡献 4
            # 用掉对应的数量
            cnt[w] -= pair_cnt
            cnt[rev] -= pair_cnt

    return ans

# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(longestPalindrome(["lc","cl","gg"]))                 # 6
    print(longestPalindrome(["ab","ty","yt","lc","cl","ab"])) # 8
    print(longestPalindrome(["cc","ll","xx"]))                # 2
```

> 代码中的关键行都有中文注释，直接复制运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组统计次数 (`O(n)`)，随后遍历哈希表的键（最多也是 `n`），每一步都是常数时间操作。  
  - 相比暴力的指数级，这里基本是线性增长，`n` 增到 10⁵ 仍然轻松跑完。

- **空间复杂度**：`O(m)`  
  - `m` 为不同单词的种类数，最多也不超过 `26 * 26 = 676`（因为只有两字母），所以即使 `n` 很大，哈希表也只占几百个键，几乎可以视作常数空间。

---  

## 心得  

- **核心技巧**：利用“互为翻转配对”和“自回文单词的中心/成对使用”。  
- **适用的题型**：  
  1. **两字符配对**（如 LeetCode 1513. Number of Substrings With Only 1s）  
  2. **构造最长回文**（如 LeetCode 409. Longest Palindrome）  
  3. **字符串翻转配对**（如 LeetCode 859. Buddy Strings 的思路变体）  

> **一句话总结**：把回文看成左右镜像，所有可以“左‑右配对”的块都尽量配对，剩下唯一能放中间的自回文块即可。

---  

## 反思  

- **第一反应**：看到“每个单词长度都是 2”，立刻想到可以把它们视作有向边或两字母的“码”，从而考虑配对而不是排列。  
- **最容易踩的坑**：  
  - 忘记 **只放一个** 自回文单词在中心，放多个会破坏对称。  
  - 在配对 `ab` 与 `ba` 时重复计数（如同时遍历 `ab` 和 `ba`），导致长度翻倍。用 `w < rev` 或在遍历时直接删除已配对的键可以避免。  
  - 忽略了字符全部相同的单词（如 `"aa"`），它们既能成对也能单独作中心。  

- **下次遇到类似题目**：第一步先 **统计出现次数**，再 **根据题目对称/配对的本质**，找出可以“配对”或“单独使用”的类别，最后把贡献加起来。这样思路清晰，代码也自然简洁。