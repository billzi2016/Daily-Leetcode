# #3085. 使字符串成为 K‑特殊的最少删除次数 / Minimum Deletions to Make String K-Special

> 难度：中等 · 标签：Hash Table、String、Greedy、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-deletions-to-make-string-k-special/)

---

## 题目（英文原版）

**Description**

You are given a string word and an integer k.
We consider word to be k-special if |freq(word[i]) - freq(word[j])| <= k for all indices i and j in the string.
Here, freq(x) denotes the frequency of the character x in word, and |y| denotes the absolute value of y.
Return the minimum number of characters you need to delete to make word k-special.

**Examples**

**Example 1:**

```
Input: word = "aabcaba", k = 0
Output: 3
Explanation: We can make word 0 -special by deleting 2 occurrences of "a" and 1 occurrence of "c" . Therefore, word becomes equal to "baba" where freq('a') == freq('b') == 2 .
```

**Example 2:**

```
Input: word = "dabdcbdcdcd", k = 2
Output: 2
Explanation: We can make word 2 -special by deleting 1 occurrence of "a" and 1 occurrence of "d" . Therefore, word becomes equal to "bdcbdcdcd" where freq('b') == 2 , freq('c') == 3 , and freq('d') == 4 .
```

**Example 3:**

```
Input: word = "aaabaaa", k = 2
Output: 1
Explanation: We can make word 2 -special by deleting 1 occurrence of "b" . Therefore, word becomes equal to "aaaaaa" where each letter's frequency is now uniformly 6 .
```

**Constraints**

- 1 <= word.length <= 105
- 0 <= k <= 105
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 **word** 和一个整数 **k**。  
如果对字符串中任意下标 **i**、**j**，都有  

\[
| \text{freq}(\text{word}[i]) - \text{freq}(\text{word}[j]) | \le k
\]

则称 **word** 为 **k‑特殊 (k-special)**。  

其中，**freq(x)** 表示字符 **x** 在 **word** 中的出现次数（频率 (frequency)），**|y|** 表示 **y** 的绝对值 (absolute value)。  

返回为了使 **word** 成为 **k‑特殊** 所需删除的最少字符数。

### 示例

#### 示例 1
**输入**  
```text
word = "aabcaba", k = 0
```
**输出**  
```text
3
```
**解释**  
我们可以通过删除 2 个 `'a'` 和 1 个 `'c'` 来使字符串 0‑特殊。此时 **word** 变为 `"baba"`，其中 `freq('a') == freq('b') == 2`。

#### 示例 2
**输入**  
```text
word = "dabdcbdcdcd", k = 2
```
**输出**  
```text
2
```
**解释**  
删除 1 个 `'a'` 和 1 个 `'d'` 后，字符串变为 `"bdcbdcdcd"`，此时 `freq('b') == 2`，`freq('c') == 3`，`freq('d') == 4`，满足 2‑特殊。

#### 示例 3
**输入**  
```text
word = "aaabaaa", k = 2
```
**输出**  
```text
1
```
**解释**  
删除 1 个 `'b'` 后，字符串变为 `"aaaaaa"`，所有字符的频率均为 6，满足 2‑特殊。

### 约束条件
- $1 \le \text{word.length} \le 10^5$
- $0 \le k \le 10^5$
- **word** 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **先统计每个字母出现的次数**  
   用 `Counter`（相当于一本“字典”，把字母当成单词，出现次数当成页码）把 `word` 中每个字符的频率记下来。因为英文小写字母只有 26 个，表格最多只有 26 行。

2. **假设最小频率是 `x`，把所有字符都“调节”到满足 `max‑freq – min‑freq ≤ k`**  
   - 如果某字符的出现次数 `f` **小于** `x`，说明它在最终字符串里根本不出现了，需要把这 `f` 个字符全部删掉。  
   - 如果 `f` **大于** `x + k`，说明它的次数太多，需要删掉 `f - (x + k)` 个，使它恰好等于 `x + k`（这样它和最小频率的字符差不超过 `k`）。  
   - 其他情况 (`x ≤ f ≤ x + k`) 就不需要删。  

   把所有字符按照上面的规则算一遍，得到“如果最小频率是 `x`，需要删多少字符”。把所有可能的 `x`（从 `0` 到出现次数的最大值）都尝试一遍，取最小值即为答案。

3. **为什么这一定是正确的**  
   - 只要我们固定了最终字符串里最小的出现次数 `x`，其它字符的合法区间只能是 `[x, x+k]`。于是每个字符要么被全部删除（`f < x`），要么被削减到区间上限（`f > x+k`），要么保持不动。没有别的更省删法。  
   - 因此遍历所有可能的 `x`，必然能找到全局最优的删字符数。

4. **时间/空间复杂度**  
   - **时间**：我们要遍历 `x = 0 … maxFreq`（最多 `10⁵`），每次遍历所有 26 个字符，时间复杂度是 `O(26·maxFreq) ≈ O(maxFreq)`。可以把它想象成“每天检查 26 位老师的成绩，最高分不超过 10⁵”，所以最多检查约 260 万次，完全跑得动。  
   - **空间**：只用了一个长度为 26 的数组/字典来存频率，`O(1)`（常数级）空间。

#### 代码（Python）

```python
from collections import Counter

def min_deletions_bruteforce(word: str, k: int) -> int:
    # 统计每个字母出现的次数，像查字典一样，key 是字母，value 是出现次数
    freq = Counter(word)               # 只会有至多 26 条记录
    max_f = max(freq.values())         # 出现次数的最大值

    best = len(word)                    # 最坏情况：全部删掉

    # x 表示最终保留下来的字符中最小的出现次数
    for x in range(max_f + 1):          # 0 … max_f 都尝试一次
        deletions = 0
        for f in freq.values():
            if f < x:                   # 这类字符全删掉
                deletions += f
            elif f > x + k:             # 超出上限，需要删掉多余的部分
                deletions += f - (x + k)
            # else: 在 [x, x+k] 之间，不删
        best = min(best, deletions)     # 记录最小的删除次数

    return best
```

#### 复杂度

- **时间复杂度**：`O(26·maxFreq) ≈ O(maxFreq)`，`maxFreq ≤ 10⁵`，实际运行约几百万次操作，足够快。  
- **空间复杂度**：`O(1)`，只用了常数个计数器（最多 26 个字母）。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于：我们把 `x` 从 `0` 扫到 `maxFreq`，虽然 `maxFreq` 只有 `10⁵`，但实际上 `x` 的取值不需要这么细——**最优的 `x` 必然是某个已有字符的出现次数（或 0）**。  

**推导过程**  

1. 设最终字符串的最小频率是 `x`，并且 `x` 不是任何字符原始出现次数。  
2. 把 `x` 向上移动到下一个更大的已有频率 `x'`（必然 `x' > x`），会产生两种变化：  
   - 所有原本 `f < x` 的字符已经被全部删掉，向上移动 `x` 不会让它们重新出现。  
   - 对于 `x ≤ f ≤ x+k` 的字符，仍然不需要删。  
   - 对于 `f > x+k` 的字符，删掉的数量是 `f - (x+k)`，而 `x' ≥ x` 会让上限 `x'+k` **更大**，于是需要删的字符数只会 **减少**（或者保持不变）。  
3. 因此把 `x` 调整到最近的已有频率不会增加删除次数，反而可能更少。  
4. 综上，**只需要枚举 `x` 为 0 或者出现次数列表中的每一个值**。出现次数最多只有 26 个，枚举次数从 `10⁵` 降到了至多 `27`，时间几乎可以忽略不计。

**核心算法**  

- 统计频率（仍然是哈希表 / Counter）。  
- 把出现次数非零的值放进列表 `vals`，再把 `0` 加进去形成候选 `x` 集合。  
- 对每个候选 `x` 按同样的删字符规则计算需要删除的总数，取最小值。

**类比**：把每个字符的频率想象成一排装满水的杯子，`x` 是我们决定保留下来的最小杯子水位。只要把最小水位调到已经有水的杯子高度，就不会浪费更多的水（删除次数）。

#### 代码（Python）

```python
from collections import Counter

def min_deletions_optimal(word: str, k: int) -> int:
    # 1. 统计频率
    freq = Counter(word)                 # 最多 26 条记录
    values = list(freq.values())         # 只保留出现次数

    # 2. 可能的最小频率候选集合：0 + 所有出现次数
    candidates = [0] + values

    best = len(word)                     # 初始设为全部删除

    # 3. 对每个候选 x 计算需要删除的字符数
    for x in candidates:
        deletions = 0
        for f in values:
            if f < x:                    # 完全删掉
                deletions += f
            elif f > x + k:              # 超出上限，删掉多余的
                deletions += f - (x + k)
            # else: 在合法区间内，不删
        best = min(best, deletions)

    return best
```

#### 复杂度

- **时间复杂度**：`O(m²)`，其中 `m` 是不同字母的个数，`m ≤ 26`。实际上只会遍历 `≤ 27` 次每次 `≤ 26` 个频率，几乎是常数时间。相比暴力的 `O(maxFreq)`，提升非常明显。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外数组（最多 27 个候选值）。

---

## 心得

- **核心技巧**：**枚举最小频率**并利用**频率区间** `[x, x+k]` 直接算删除数。关键是认识到最优的 `x` 必然是已有的出现次数（或 0），从而把原本可能的大遍历压缩到常数遍历。  
- **适用的题型**  
  1. “使所有元素差值不超过 `k`”的字符/数字统计类问题。  
  2. “删除最少元素使数组满足某种区间约束”——例如把数组元素限制在 `[low, high]`。  
  3. “选择子集使最大值‑最小值 ≤ k”——常见的贪心/滑动窗口变形。  
- **一句话总结解题钥匙**：**把问题转化为“选定最小值”，只需遍历有限的候选最小值即可得到全局最优**。

---

## 反思

- **第一反应**：看到 “频率差 ≤ k” 立刻想到统计每个字母的出现次数，然后想办法把所有频率拉进一个宽度为 `k` 的窗口。  
- **最容易踩的坑**  
  - **忘记可以把某些字符全部删掉**（即频率 < 最小值的情况）。  
  - **漏算 `k = 0` 时的特殊情况**：所有保留下来的字符频率必须完全相同。  
  - **边界条件**：`x = 0` 必须加入候选集合，否则全部删除的情况会被遗漏。  
- **下次类似题目**：第一步先 **统计频率**，然后 **枚举最小频率**（或最大频率）作为“基准”，利用区间约束直接计算删除/修改代价。这样可以把看似指数级的搜索压缩到常数级或线性级。