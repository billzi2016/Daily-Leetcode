# #3306. 包含所有元音且恰好 K 个辅音的子串计数 II / Count of Substrings Containing Every Vowel and K Consonants II

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/)

---

## 题目（英文原版）

**Description**

You are given a string word and a non-negative integer k.
Return the total number of substrings of word that contain every vowel ('a', 'e', 'i', 'o', and 'u') at least once and exactly k consonants.

**Examples**

**Example 1:**

```
Input: word = "aeioqq", k = 1
Output: 0
Explanation:
There is no substring with every vowel.
```

**Example 2:**

```
Input: word = "aeiou", k = 0
Output: 1
Explanation:
The only substring with every vowel and zero consonants is word[0..4] , which is "aeiou" .
```

**Example 3:**

```
Input: word = " ieaouqqieaouqq ", k = 1
Output: 3
Explanation:
The substrings with every vowel and one consonant are:
```

**Constraints**

- 5 <= word.length <= 2 * 105
- word consists only of lowercase English letters.
- 0 <= k <= word.length - 5

---

## 题目（中文翻译）

**题目描述**  

给定一个字符串 `word` 和一个非负整数 `k`。返回 `word` 中满足以下条件的子串（substring）总数：该子串至少包含每个元音（vowel）`'a'`, `'e'`, `'i'`, `'o'`, `'u'` 各一次，并且恰好包含 `k` 个辅音（consonant）。

**示例**  

示例 1:  
```
Input: word = "aeioqq", k = 1
Output: 0
Explanation:
不存在同时包含所有元音的子串。
```

示例 2:  
```
Input: word = "aeiou", k = 0
Output: 1
Explanation:
唯一满足条件的子串是 word[0..4]，即 "aeiou"，它包含所有元音且没有辅音。
```

示例 3:  
```
Input: word = "ieaouqqieaouqq", k = 1
Output: 3
Explanation:
满足条件的子串有三段，分别是：
（此处列出具体的子串，可根据原题实际给出）
```

**约束条件**  

- $5 \leq \text{word.length} \leq 2 \times 10^5$
- `word` 仅由小写英文字母组成。
- $0 \leq k \leq \text{word.length} - 5$

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有子串**，逐个检查它们是否满足下面两个条件：

1. 包含 `'a','e','i','o','u'` 五个元音字母 **至少一次**。  
2. 子串中的**辅音（非元音）恰好出现 `k` 次**。

> **类比**：把字符串想成一条长长的火车，子串就是火车上连续的几节车厢。我们把每节车厢标记为“元音”或“辅音”。暴力解相当于把所有可能的连续车厢组合都挑出来检查一遍——虽然能得到答案，但会非常慢。

**为什么一定能得到正确答案**  
因为我们没有漏掉任何一种可能的子串：所有的左端点 `l`（从 `0` 到 `n-1`）和右端点 `r`（从 `l` 到 `n-1`）都会被遍历一次。只要判断函数 `check(l,r)` 正确，答案必然正确。

**复杂度分析**  
- 外层两层循环分别枚举左端点 `l` 和右端点 `r`，总共大约有 `n*(n+1)/2` ≈ `O(n²)` 个子串。  
- 对每个子串，我们要遍历一次子串本身去统计元音集合和辅音个数，最坏情况下子串长度是 `n`，于是每次检查是 `O(n)`。  
- 综合下来时间复杂度是 **`O(n³)`**，在最坏情况下会超时（`n` 最多可达 `2·10⁵`）。  
- 只用了常数级的额外空间，**空间复杂度是 `O(1)`**。

> **大白话**：  
> - `O(n³)` 就好比把一条 200,000 米的河划分成所有可能的区段，然后每个区段再把整条河跑一遍来数数——显然不可能在几秒钟内完成。

#### 代码（Python）

```python
def count_substrings_bruteforce(word: str, k: int) -> int:
    n = len(word)
    vowels = set('aeiou')
    ans = 0

    # 枚举左端点 l
    for l in range(n):
        # 当前子串里出现的元音集合
        seen = set()
        # 当前子串里辅音的个数
        cons_cnt = 0

        # 枚举右端点 r（从 l 向右扩展）
        for r in range(l, n):
            ch = word[r]
            if ch in vowels:
                seen.add(ch)          # 记录出现的元音
            else:
                cons_cnt += 1         # 辅音计数加一

            # 同时检查两个条件
            if cons_cnt == k and len(seen) == 5:
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - `n` 为字符串长度。三层循环（左端点、右端点、子串内部遍历）导致立方级别的耗时。
- **空间复杂度**：`O(1)`  
  - 只用了几个计数器和集合，和 `n` 无关。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于我们每次都要重新遍历子串来统计元音和辅音。  
我们需要**在遍历一次字符串的过程中**，把这些信息“提前准备好”，以后查询时能够 **`O(log n)`** 或 **`O(1)`** 完成。

下面一步步推导出一种 **前缀和 + 哈希表 + 二分查找** 的方案（时间 `O(n log n)`）：

1. **把“辅音个数”转化为前缀和**  
   - 定义 `pref[i]` 为 `word[:i]`（左闭右开）的辅音个数，`pref[0]=0`。  
   - 那么子串 `word[l..r]`（左闭右闭）的辅音数 = `pref[r+1] - pref[l]`。  
   - 这一步把“统计辅音”从 `O(len)` 降到 `O(1)`。

2. **记录每个元音最近一次出现的位置**  
   - 用字典 `last = {'a': -1, 'e': -1, ...}`，遍历字符时更新。  
   - 对于右端点 `r`，要让子串 `l..r` 包含 **所有五个元音**，左端点 `l` 必须 **不大于**这五个元音中出现最早的那一次（即 `min_last = min(last.values())`）。  
   - 如果还有元音没有出现（值为 `-1`），说明当前 `r` 还不能形成合法子串，直接跳过。

3. **把“左端点的前缀辅音数”放进哈希表**  
   - 我们关心的是 **`pref[l]` 的值**，因为子串辅音数的公式里只用了 `pref[l]`。  
   - 对每一个可能的 `pref` 值，维护一个**递增的下标列表** `pos[pref]`，记录所有出现过的左端点 `l`（即 `pref` 的索引）。  
   - 由于我们是从左到右遍历，往列表里添加的下标天然是 **有序** 的，后面可以直接二分。

4. **对每个右端点 `r` 计算答案**  
   - 目标前缀值 `target = pref[r+1] - k`（因为 `pref[r+1] - pref[l] = k`）。  
   - 若 `target` 不在哈希表中，说明没有左端点能让辅音数恰好为 `k`，直接跳过。  
   - 否则，取出 `pos[target]`（所有满足 `pref[l]=target` 的左端点），**统计其中 ≤ `min_last` 的个数**。这一步用 `bisect_right`（二分）完成，时间 `O(log n)`。  
   - 统计的数量就是以当前 `r` 为右端点的合法子串数，累加到答案。

5. **把当前下标 `r+1`（即 `pref` 对应的左端点）加入哈希表**，为后续的右端点做准备。

> **类比**：  
> - 想象一条跑道上有标记牌（前缀辅音数），每次跑完一段我们都把这块牌的编号记下来。要找满足“恰好跑了 `k` 步且已经经过所有五个检查点”的区间，就等价于在标记牌里找两块编号之差为 `k`，且左块的下标不超过最早检查点的位置。利用哈希表把同编号的牌放在一起，用二分快速计数。

#### 代码（Python）

```python
from bisect import bisect_right
from collections import defaultdict

def count_substrings(word: str, k: int) -> int:
    n = len(word)
    vowels = set('aeiou')

    # 1. 前缀辅音数
    pref = [0] * (n + 1)          # pref[i] = word[:i] 中的辅音个数
    for i, ch in enumerate(word, 1):
        pref[i] = pref[i - 1] + (0 if ch in vowels else 1)

    # 2. 记录每个元音最近出现的位置
    last = {v: -1 for v in vowels}

    # 3. 哈希表：前缀值 -> 所有出现过的左端点下标（递增）
    pos = defaultdict(list)
    pos[0].append(0)              # l = 0 对应的前缀值是 0

    ans = 0

    # 4. 遍历右端点 r（0-indexed）
    for r, ch in enumerate(word):
        # 更新元音的最近位置
        if ch in vowels:
            last[ch] = r

        # 只有当五个元音都出现过，才可能构成合法子串
        if -1 in last.values():
            # 仍然要把当前的左端点加入 pos，以备后面的 r 使用
            pos[pref[r + 1]].append(r + 1)
            continue

        # 左端点必须 ≤ 最早出现的元音位置
        min_last = min(last.values())

        # 目标前缀值，使得辅音数恰好为 k
        target = pref[r + 1] - k
        if target in pos:
            # 在 pos[target] 中统计下标 ≤ min_last 的数量
            # 因为 pos[target] 已经是递增的，用二分即可
            cnt = bisect_right(pos[target], min_last)
            ans += cnt

        # 把当前的左端点（对应 pref[r+1]）加入哈希表
        pos[pref[r + 1]].append(r + 1)

    return ans
```

**代码要点说明**  

| 行号 | 关键操作 | 中文注释 |
|------|----------|----------|
| 5‑7 | 计算前缀辅音数 `pref` | `pref[i]` 记录前 i 个字符中辅音的累计个数 |
| 12‑13 | 初始化每个元音的最近出现位置为 `-1` | 表示尚未出现 |
| 16‑17 | `pos[0].append(0)` | 左端点为 0 时的前缀值为 0，先放进哈希表 |
| 22‑26 | 更新 `last` 字典 | 把当前字符若是元音，就记下它的下标 |
| 28‑30 | 判断是否所有元音都出现过 | 只要有 `-1`，说明还有元音缺失，直接跳过计数 |
| 33‑35 | 计算 `min_last` 与 `target` | `min_last` 是左端点的上界，`target` 是满足 `k` 辅音的前缀值 |
| 36‑40 | 二分统计合法左端点数 | `bisect_right` 返回 ≤ `min_last` 的元素个数 |
| 43‑44 | 把当前 `pref` 对应的下标加入 `pos` | 为后面的右端点做好准备 |

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 主循环遍历 `n` 次，每次只做 `O(1)` 的字典/列表操作和一次二分查找 `O(log n)`。  
  - 与暴力解的 `O(n³)` 相比，速度提升了 **指数级**，在 `n ≤ 2·10⁵` 时完全可接受。

- **空间复杂度**：`O(n)`  
  - `pref`、`pos`、`last` 共占用线性空间。  
  - `pos` 中每个前缀值最多对应若干下标，总数正好是 `n+1`（因为每个左端点只会加入一次），所以空间是线性的。

---

## 心得

- **核心技巧**：  
  1. **前缀和** 把“区间统计”转化为“两个前缀的差”。  
  2. **哈希表 + 有序列表** 记录相同前缀值出现的位置，以便快速计数。  
  3. **维护元音最近出现位置**，把“包含所有元音”转化为左端点的上界 `min_last`。  

- **适用的题型**（类似思路）  
  1. “子串中恰好出现 `k` 个特定字符” → 前缀计数 + 哈希表。  
  2. “子串满足某种计数约束且必须包含全部关键字符” → 记录关键字符的最左/最右位置。  
  3. “子数组和等于目标值且满足额外限制” → 前缀和 + 双指针/二分。

- **一句话总结解题钥匙**：  
  > 把“区间条件”拆成 **前缀差** 与 **左端点的范围约束**，利用哈希表存前缀值并二分计数，即可在 `O(n log n)` 内完成统计。

---

## 反思

- **第一反应**：直接枚举所有子串并逐个检查——这就是暴力解。  
- **最容易踩的坑**  
  1. **元音未全部出现** 时仍然尝试计数，会导致 `min_last = -1`，产生错误的计数。  
  2. **前缀下标的对应关系**（`pref[l]` 与 `pref[r+1]`）容易弄混，导致辅音数公式写错。  
  3. **二分的边界**：使用 `bisect_right` 而不是 `bisect_left`，确保左端点 **≤** `min_last`（而不是 `<`）。  

- **下次遇到同类题**，第一步应该：  
  1. 把**区间统计**转化为**前缀差**（是否可以用前缀和/前缀计数）。  
  2. 明确**额外约束**（如必须包含全部关键字符）如何转化为左/右端点的范围限制。  
  3. 再决定使用 **哈希表 + 有序容器**、**滑动窗口** 还是 **双指针** 来高效计数。