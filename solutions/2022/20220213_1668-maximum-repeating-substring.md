# #1668. 最大重复子串 / Maximum Repeating Substring

> 难度：简单 · 标签：String、Dynamic Programming、String Matching · [LeetCode 链接](https://leetcode.com/problems/maximum-repeating-substring/)

---

## 题目（英文原版）

**Description**

For a string sequence, a string word is k-repeating if word concatenated k times is a substring of sequence. The word's maximum k-repeating value is the highest value k where word is k-repeating in sequence. If word is not a substring of sequence, word's maximum k-repeating value is 0.
Given strings sequence and word, return the maximum k-repeating value of word in sequence.

**Examples**

**Example 1:**

```
Input: sequence = "ababc", word = "ab"
Output: 2
Explanation: "abab" is a substring in "ababc".
```

**Example 2:**

```
Input: sequence = "ababc", word = "ba"
Output: 1
Explanation: "ba" is a substring in "ababc". "baba" is not a substring in "ababc".
```

**Example 3:**

```
Input: sequence = "ababc", word = "ac"
Output: 0
Explanation: "ac" is not a substring in "ababc".
```

**Constraints**

- 1 <= sequence.length <= 100
- 1 <= word.length <= 100
- sequence and word contains only lowercase English letters.

---

## 题目（中文翻译）

对于一个字符串 `sequence`，如果将字符串 `word` 连续拼接 `k` 次得到的字符串是 `sequence` 的子串（substring），则称 `word` 是 **k 次重复**（k‑repeating）的。`word` 的最大 `k` 次重复值是满足上述条件的最大整数 `k`。如果 `word` 本身不是 `sequence` 的子串，则其最大 `k` 次重复值为 `0`。  
给定字符串 `sequence` 和 `word`，返回 `word` 在 `sequence` 中的最大 `k` 次重复值。

**示例 1**  
```
Input: sequence = "ababc", word = "ab"
Output: 2
Explanation: "abab" 是 "ababc" 的子串。
```

**示例 2**  
```
Input: sequence = "ababc", word = "ba"
Output: 1
Explanation: "ba" 是 "ababc" 的子串，而 "baba" 不是 "ababc" 的子串。
```

**示例 3**  
```
Input: sequence = "ababc", word = "ac"
Output: 0
Explanation: "ac" 不是 "ababc" 的子串。
```

**约束条件**  

- `1 <= sequence.length <= 100`
- `1 <= word.length <= 100`
- `sequence` 和 `word` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **word** 按不同的重复次数 `k` 拼接起来，形成 `"word"*k`（即 word 连着 k 次），然后检查这个大字符串是否出现在 **sequence** 中。  
- **数据结构**：这里唯一需要的结构是 **字符串** 本身，`in` 操作在 Python 中相当于在一本大书里找一个短句子，底层会做一次子串匹配。可以把它想象成 **查字典**：我们把 `"word"*k` 当作要查的“词”，而 **sequence** 就是字典的全部内容。  
- **正确性**：如果 `"word"*k` 能在 **sequence** 中找到，说明 `word` 连着出现了 `k` 次；如果找不到，说明再往更大的 `k`（更长的拼接）也一定找不到，因为它已经比上一次更长了。于是我们可以从 `k = 1` 开始，一直尝试，直到第一次不匹配为止，之前的最大 `k` 就是答案。  

#### 代码（Python）

```python
def maxRepeating_bruteforce(sequence: str, word: str) -> int:
    # 先算出可能的最大 k，防止无意义的循环
    max_possible = len(sequence) // len(word)
    k = 0                         # 记录当前能够匹配的最大 k
    # 从 1 开始尝试每一个 k
    for cur_k in range(1, max_possible + 1):
        repeated = word * cur_k   # 把 word 连在一起 cur_k 次
        # Python 的 `in` 相当于“在 sequence 里找 repeated”
        if repeated in sequence:
            k = cur_k              # 能匹配，就更新答案
        else:
            break                  # 第一次不匹配，后面的更长的肯定也不行
    return k
```

#### 复杂度  

- **时间复杂度**：`O(n²)`（这里的 *n* 代表 `len(sequence)`）。解释一下：我们最多会尝试 `n / len(word)` 次，每一次都要把 `word` 重复 `k` 次（最多 `O(n)` 长），再去做一次子串查找，这一步本身在最坏情况下也是 `O(n)`，于是整体是 `O(n * n) = O(n²)`。  
- **空间复杂度**：`O(n)`，因为 `repeated = word * cur_k` 会产生一个最多和 **sequence** 等长的临时字符串。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次都重新创建完整的 `"word"*k` 并重新扫描整个 **sequence**。我们可以把这两个步骤合并：  
1. **一次遍历** **sequence**，在每个位置尝试匹配 **word**。  
2. 如果匹配成功，就继续往后检查下一个 **word** 是否紧跟着出现，直到不匹配为止。这样可以直接得到从该起点开始的连续重复次数。  
3. 把所有起点得到的最大次数取最大值，就是答案。

这里的核心技巧是 **双指针**（或者说“滑动窗口”）：

- **左指针 `i`**：遍历 **sequence** 的起始位置。  
- **右指针 `j`**：每次向后跳 `len(word)` 的步长，检查子串 `sequence[j:j+len(word)]` 是否等于 **word**。只要相等，就说明又多了一次重复。  

因为每次 `j` 都向后跳 `len(word)`，整个过程只会遍历 `sequence` 至多一次（每个字符最多被访问一次），所以时间复杂度降到了 `O(n * m)`，其中 `m = len(word)`。这已经是最优的线性级别了。

#### 代码（Python）

```python
def maxRepeating_optimal(sequence: str, word: str) -> int:
    n, m = len(sequence), len(word)
    max_k = 0                       # 记录全局最大重复次数

    i = 0
    while i <= n - m:               # 起点必须保证至少能放下一个 word
        # 只在当前位置恰好是 word 开头时才开始计数
        if sequence[i:i + m] == word:
            cur_k = 0
            j = i
            # 连续向后检查，每次跨过一个 word 长度
            while j <= n - m and sequence[j:j + m] == word:
                cur_k += 1
                j += m
            max_k = max(max_k, cur_k)   # 更新全局最大值
            # 已经检查过的区域不需要再从中间位置重新开始
            i = j                         # 跳到本次连续块的末尾继续向后
        else:
            i += 1                        # 普通字符，直接左移一格

    return max_k
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`。解释：外层循环遍历 `sequence`（`O(n)`），而内部的连续匹配每次最多比较 `m` 个字符。因为每个字符在一次成功匹配后会被 `i` 跳过，所以整体仍是线性级别。相较于暴力的 `O(n²)`，这里明显更快。  
- **空间复杂度**：`O(1)`，只用了常数级别的额外变量（`i, j, cur_k, max_k`），不随输入规模增长。

---

## 心得

- **核心技巧**：在字符串中寻找**连续重复子串**，使用双指针/滑动窗口一次遍历即可得到最大重复次数。  
- **适用的题型**：  
  1. “重复子串最大次数” 类似题目，如 **Maximum Repeating Substring**（本题）。  
  2. “最长相同子数组/子串” 需要连续匹配的题目，例如 “连续子数组的最大和”。  
  3. “字符串中连续出现的模式” 如 “Repeated Substring Pattern”。  
- **一句话总结**：**把连续匹配的过程合并到一次遍历中，就能把指数级的暴力降到线性。**

---

## 反思

- **第一反应**：看到 “k‑repeating” 这几个字，马上想到“把 word 拼成更长的字符串，然后 `in` 检查”。这就是暴力的自然思路。  
- **最容易踩的坑**：  
  - 忘记 **word** 可能根本不在 **sequence**，此时直接返回 `0`。  
  - 循环边界要写对，尤其是 `i <= n - m`，否则会出现切片越界。  
  - 在最优解里，`i` 必须在一次连续匹配结束后直接跳到块的末尾，否则会重复检查已经确认的字符，导致时间不降。  
- **下次第一步**：先判断 **word** 是否在 **sequence** 中（`if word not in sequence: return 0`），然后考虑是否可以一次遍历同时统计连续出现的次数，而不是每次都重新拼接字符串。这样思路更清晰，代码也更高效。