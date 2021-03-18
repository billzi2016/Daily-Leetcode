# #1255. 字母组成单词的最大得分 / Maximum Score Words Formed by Letters

> 难度：困难 · 标签：Array、String、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-score-words-formed-by-letters/)

---

## 题目（英文原版）

**Description**

Given a list of words, list of  single letters (might be repeating) and score of every character.
Return the maximum score of any valid set of words formed by using the given letters (words[i] cannot be used two or more times).
It is not necessary to use all characters in letters and each letter can only be used once. Score of letters 'a', 'b', 'c', ... ,'z' is given by score[0], score[1], ... , score[25] respectively.

**Examples**

**Example 1:**

```
Input: words = ["dog","cat","dad","good"], letters = ["a","a","c","d","d","d","g","o","o"], score = [1,0,9,5,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0]
Output: 23
Explanation:
Score  a=1, c=9, d=5, g=3, o=2
Given letters, we can form the words "dad" (5+1+5) and "good" (3+2+2+5) with a score of 23.
Words "dad" and "dog" only get a score of 21.
```

**Example 2:**

```
Input: words = ["xxxz","ax","bx","cx"], letters = ["z","a","b","c","x","x","x"], score = [4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,10]
Output: 27
Explanation:
Score  a=4, b=4, c=4, x=5, z=10
Given letters, we can form the words "ax" (4+5), "bx" (4+5) and "cx" (4+5) with a score of 27.
Word "xxxz" only get a score of 25.
```

**Example 3:**

```
Input: words = ["leetcode"], letters = ["l","e","t","c","o","d"], score = [0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0]
Output: 0
Explanation:
Letter "e" can only be used once.
```

**Constraints**

- 1 <= words.length <= 14
- 1 <= words[i].length <= 15
- 1 <= letters.length <= 100
- letters[i].length == 1
- score.length == 26
- 0 <= score[i] <= 10
- words[i], letters[i] contains only lower case English letters.

---

## 题目（中文翻译）

**描述**  
给定一个单词列表（`words`），一个可能包含重复字符的单字符字母列表（`letters`），以及每个字符的得分（`score`）。  
返回使用给定字母能够组成的任意**有效的单词集合（valid set of words）**的最大总得分（`words[i]` 不能使用两次或更多次）。  
不必使用 `letters` 中的所有字符，且每个字母只能使用一次。字符 `'a'、'b'、'c'、…、'z'` 的得分分别由 `score[0]、score[1]、score[2]、…、score[25]` 给出。  

**示例**  

**示例 1**  
```text
Input: words = ["dog","cat","dad","good"], letters = ["a","a","c","d","d","d","g","o","o"], score = [1,0,9,5,0,0,3,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0]
Output: 23
Explanation:
Score  a=1, c=9, d=5, g=3, o=2
Given letters, we can form the words "dad" (5+1+5) and "good" (3+2+2+5) with a score of 23.
Words "dad" and "dog" only get a score of 21.
```

**示例 2**  
```text
Input: words = ["xxxz","ax","bx","cx"], letters = ["z","a","b","c","x","x","x"], score = [4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,10]
Output: 27
Explanation:
Score  a=4, b=4, c=4, x=5, z=10
Given letters, we can form the words "ax" (4+5), "bx" (4+5) and "cx" (4+5) with a score of 27.
Word "xxxz" only get a score of 25.
```

**示例 3**  
```text
Input: words = ["leetcode"], letters = ["l","e","t","c","o","d"], score = [0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0]
Output: 0
Explanation:
Letter "e" can only be used once.
```

**约束条件**  
- `1 <= words.length <= 14`  
- `1 <= words[i].length <= 15`  
- `1 <= letters.length <= 100`  
- `letters[i].length == 1`  
- `score.length == 26`  
- `0 <= score[i] <= 10`  
- `words[i]`、`letters[i]` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有单词的使用情况全部列举一遍**，然后挑选合法且得分最高的组合。  

- **枚举方式**：每个单词有「选」或「不选」两种状态，`words` 的长度记为 `n`，于是所有可能的组合数是 `2ⁿ`（二进制的每一位代表一个单词是否被选）。这就像把所有单词排成一排，给每个单词贴上「开」或「关」的标签，遍历所有标签的排列。  
- **合法性判断**：对于当前枚举的单词集合，统计它们需要的每个字母的数量（类似查字典：字母是 key，出现次数是 value），然后和手里提供的 `letters`（同样统计成字典）逐一比较。只要每种字母的需求不超过手中拥有的数量，就算合法。  
- **得分计算**：合法后，把该组合里所有单词的字母分数相加即可。分数字典 `score` 把字母映射到整数分值，求和过程就像把每个字母的“价签”加到一起。

> **为什么暴力一定能得到正确答案？**  
> 因为我们把所有可能的单词子集都穷举了，答案必然出现在其中。只要每个子集都检查合法性并计算分数，最大分数必然被记录下来。

**时间/空间复杂度的大白话**  

- **时间**：我们要遍历 `2ⁿ`（最多 2¹⁴ = 16384）个子集。对每个子集，我们要把所有选中的单词的字母计数一次，最坏情况下所有单词长度相加不超过 `n * 15 = 210`，所以每个子集的检查是 **O(total_word_len)**，整体时间是 **O(2ⁿ * total_word_len)**，可以看成 **O(2ⁿ·15·n)**。对初学者来说，只要 `n ≤ 14`，这个数是非常小的。  
- **空间**：我们只需要保存字母计数的数组（长度 26）和若干临时变量，空间是 **O(1)**（常数级），不随 `n` 增长。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def maxScoreWords(words: List[str], letters: List[str], score: List[int]) -> int:
    # 1️⃣ 把手里的字母统计成字典，key 是字母，value 是出现次数
    letters_cnt = Counter(letters)               # 类似查字典，key = 字母，value = 余量

    # 2️⃣ 预先把每个单词的字母计数和单词分数算好，后面会重复使用
    word_cnt = []      # 每个单词的 Counter
    word_score = []    # 每个单词的总分
    for w in words:
        cnt = Counter(w)
        word_cnt.append(cnt)
        # 计算该单词的分数：每个字母的出现次数 × 对应分值
        sc = sum(cnt[ch] * score[ord(ch) - ord('a')] for ch in cnt)
        word_score.append(sc)

    n = len(words)
    best = 0

    # 3️⃣ 枚举所有子集：0 ~ (1<<n)-1，每一位表示是否选第 i 个单词
    for mask in range(1 << n):
        cur_cnt = Counter()   # 当前子集需要的字母总量
        cur_score = 0
        valid = True

        for i in range(n):
            if mask >> i & 1:               # 第 i 个单词被选中
                # 先把该单词的字母需求加到 cur_cnt
                cur_cnt += word_cnt[i]
                cur_score += word_score[i]

        # 4️⃣ 检查是否超过手中字母的数量
        for ch, need in cur_cnt.items():
            if need > letters_cnt.get(ch, 0):
                valid = False
                break

        if valid:
            best = max(best, cur_score)

    return best
```

> **代码要点注释**  
> - `Counter` 相当于「查字典」工具，自动统计每个字母出现多少次。  
> - `mask >> i & 1` 用二进制的第 i 位判断是否选第 i 个单词。  
> - `cur_cnt += word_cnt[i]` 是 Counter 的“合并”，相当于把两张字母表合在一起。

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n * L)`，其中 `L` 为单词的最大长度（≤15）。在本题 `n ≤ 14`，所以最多约 `2⁴⁰ ≈ 1.6×10⁴` 次枚举，完全可接受。  
- **空间复杂度**：`O(1)`（只用到固定大小的计数数组/Counter），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解已经能够在题目给出的约束下跑完，但我们可以把 **合法性检查的成本** 再压缩一点，做到 **边枚举边剪枝**，从而把时间常数进一步降低。核心思路：

1. **从“枚举子集”转向“回溯搜索”**  
   - 按单词的顺序递归决定「选」或「不选」当前单词。  
   - 在「选」的分支里，先检查加入该单词后是否仍然满足字母库存。如果不满足，直接**剪掉**这个分支，不再继续往下递归。这样可以省掉很多不合法的子集的完整遍历。  

2. **使用 **位掩码 (bitmask)** 记录已使用的字母**  
   - 由于字母只有 26 种，且每种字母最多出现 100 次（但我们只关心是否足够），我们可以把每种字母的剩余次数放在长度为 26 的数组 `remain` 中。  
   - 每次尝试加入单词时，遍历该单词的字母表，判断 `remain[ch]` 是否足够。若足够，就在 `remain` 中扣除相应数量；递归结束后再恢复（回溯）。  

3. **递归返回的值即「从当前位置开始能得到的最大得分」**  
   - 对每个位置 `i`，我们有两种选择：**不选** `words[i]` → 得分为 `dfs(i+1, remain)`；**选**（前提是合法）→ 得分为 `word_score[i] + dfs(i+1, remain_after_use)`。取两者最大即为答案。  

4. **记忆化搜索（可选）**  
   - 由于 `remain` 的状态空间（每种字母最多 100）很大，直接记忆化不划算。这里我们依赖 **剪枝** 已经足够快，故不做额外记忆化。  

**类比帮助理解**：  
- 想象你在玩拼字游戏，每次你决定是否把手里的字母拼成某个单词。如果拼不成，就直接放弃这条路（剪枝），继续尝试下一个单词。整个过程就像在树形图里走路径，只有合法的路径才会继续深入。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def maxScoreWords(words: List[str], letters: List[str], score: List[int]) -> int:
    # 统计可用字母的剩余次数
    remain = [0] * 26
    for ch in letters:
        remain[ord(ch) - ord('a')] += 1

    # 预处理每个单词的字母计数和单词得分
    word_cnt = []
    word_score = []
    for w in words:
        cnt = [0] * 26
        for ch in w:
            cnt[ord(ch) - ord('a')] += 1
        word_cnt.append(cnt)

        sc = sum(cnt[i] * score[i] for i in range(26))
        word_score.append(sc)

    n = len(words)

    # 深度优先搜索 + 剪枝
    def dfs(idx: int) -> int:
        """从 idx 开始，返回能够取得的最大得分"""
        if idx == n:               # 已经遍历完所有单词
            return 0

        # 1) 不选当前单词
        best = dfs(idx + 1)

        # 2) 尝试选当前单词（先检查是否合法）
        cnt = word_cnt[idx]
        for i in range(26):
            if cnt[i] > remain[i]:     # 剩余字母不够，直接放弃选这个单词
                break
        else:  # 所有字母都够用，进入选的分支
            # 把字母消耗掉
            for i in range(26):
                remain[i] -= cnt[i]
            # 递归得到后面的最大得分，加上当前单词的得分
            best = max(best, word_score[idx] + dfs(idx + 1))
            # 恢复现场（回溯）
            for i in range(26):
                remain[i] += cnt[i]

        return best

    return dfs(0)
```

> **代码要点**  
> - `remain` 用长度为 26 的列表代替 `Counter`，下标 `0~25` 对应字母 `'a'~'z'`，访问速度更快。  
> - `for i in range(26): ... else:` 这段结构的意义是：只有当循环 **没有** 因 `break` 提前退出时（即所有字母都足够），才会执行 `else` 块里的选单词逻辑。  
> - 递归结束后恢复 `remain`，这一步叫 **回溯**，保证后续分支仍然看到完整的字母库存。

#### 复杂度  

- **时间复杂度**：在最坏情况下仍然是遍历所有子集 `O(2ⁿ)`，但每次加入单词前都会先做 O(26) 的合法性检查，且不合法的分支会被立刻剪掉。实际运行时间比纯暴力的 `2ⁿ * n * L` 更小，常数更低。  
- **空间复杂度**：递归深度最多 `n`（≤14），加上 `remain`、`word_cnt` 等固定大小数组，总空间为 **O(n + 26)**，即 **O(1)**（常数级）。

---

## 心得  

- **核心技巧**：**枚举子集 + 计数合法性检查**（暴力） → **回溯 + 剪枝**（更快）。  
- **适用的题型**：  
  1. “选或不选” 的组合优化问题，如 **Maximum Subset XOR**、**Maximum Profit in Job Scheduling**（需要判断资源是否冲突）。  
  2. 需要对“小规模”集合进行 **位掩码/子集遍历** 的题目，例如 **Maximum Length of a Concatenated String with Unique Characters**。  
- **一句话总结解题钥匙**：**先把所有资源（字母）统计好，用回溯逐个尝试加入单词并在非法时立刻剪枝**。

---

## 反思  

- **第一反应**：看到 “words ≤ 14”，立刻想到 **枚举所有子集**（2ⁿ）是可行的。  
- **最容易踩的坑**：  
  - **字母计数越界**：忘记在检查合法性时对每种字母分别比较，导致使用同一字母超过库存。  
  - **忘记回溯恢复**：在递归选单词后没有把 `remain` 加回，后面的分支会误以为字母已被消耗。  
  - **忽视空集**：如果所有单词都不可拼，答案应是 `0`，代码需要能够返回空集的得分。  
- **下次遇到同类题**：第一步先 **统计资源**（这里是字母），然后 **决定是直接子集遍历还是回溯剪枝**（看规模），确保在每一步都检查资源是否足够再继续。