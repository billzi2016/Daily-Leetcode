# #395. 至少出现 K 次的最长子串 / Longest Substring with At Least K Repeating Characters

> 难度：中等 · 标签：Hash Table、String、Divide and Conquer、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/)

---

## 题目（英文原版）

**Description**

Given a string s and an integer k, return the length of the longest substring of s such that the frequency of each character in this substring is greater than or equal to k.
if no such substring exists, return 0.

**Examples**

**Example 1:**

```
Input: s = "aaabb", k = 3
Output: 3
Explanation: The longest substring is "aaa", as 'a' is repeated 3 times.
```

**Example 2:**

```
Input: s = "ababbc", k = 2
Output: 5
Explanation: The longest substring is "ababb", as 'a' is repeated 2 times and 'b' is repeated 3 times.
```

**Constraints**

- 1 <= s.length <= 104
- s consists of only lowercase English letters.
- 1 <= k <= 105

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `s` 和一个整数 `k`，返回 `s` 中满足**每个字符出现次数**（frequency）**都不少于**`k` 的**最长子串（substring）**的长度**。  
如果不存在满足条件的子串，返回 `0`。

**示例 1**  
``` 
Input: s = "aaabb", k = 3
Output: 3
Explanation: 最长的满足条件的子串是 "aaa"，因为字符 'a' 恰好出现了 3 次。 
```

**示例 2**  
``` 
Input: s = "ababbc", k = 2
Output: 5
Explanation: 最长的满足条件的子串是 "ababb"，其中字符 'a' 出现了 2 次，字符 'b' 出现了 3 次。 
```

**约束条件**  
- `1 <= s.length <= 10^4`  
- `s` 只包含小写英文字母。  
- `1 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「枚举所有子串」，检查每个子串里每个字符出现的次数是否都 ≥ k，满足条件的子串取最长即可。

- **枚举子串**：可以用两层循环 `i`、`j`（`i` 为子串左端点，`j` 为右端点），把 `s[i:j+1]` 当作候选子串。  
- **统计字符频次**：对每个子串，用一个哈希表（在 Python 中用 `collections.Counter`）统计 26 个小写字母出现的次数。哈希表就像一本字典，单词（字符）是 *key*，对应的页码（出现次数）是 *value*。  
- **检查合法性**：遍历哈希表的所有 `value`，只要有一个小于 `k`，这个子串就不符合要求。  
- **更新答案**：如果合法，就比较它的长度和当前最大长度，取较大者。

这种方法一定能得到正确答案，因为它把**所有可能的子串**都检查了一遍。

#### 代码（Python）

```python
from collections import Counter

def longestSubstring_brute(s: str, k: int) -> int:
    n = len(s)
    ans = 0

    # 枚举左端点 i
    for i in range(n):
        # 用一个计数器在扩展右端点时逐步累计字符频次，避免每次都重新计数
        cnt = Counter()
        # 枚举右端点 j
        for j in range(i, n):
            cnt[s[j]] += 1               # 把 s[j] 加入当前子串的统计

            # 检查当前子串是否所有字符出现次数都 >= k
            if all(v >= k for v in cnt.values()):
                ans = max(ans, j - i + 1)   # 更新最大长度

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环产生 `O(n²)` 个子串。  
  - 对每个子串要遍历计数器的所有字符（最坏 26），这在大 O 记号里视为常数，但因为我们每次都用 `all(v >= k for v in cnt.values())`，在最坏情况下会遍历整个计数器，所以整体是 `O(n² * 26) ≈ O(n²)`。  
  - 由于我们在每次扩展右端点时都重新检查一次，实际运行时间接近 `O(n³)`，在 `n=10⁴` 时会超时。  
- **空间复杂度**：`O(26) = O(1)`  
  - 计数器最多存 26 个字母，视为常数空间。

---

### 2. 最优解

下面给出两种最常见的「最优」思路，任选其一即可。这里重点讲 **分治（Divide & Conquer）**，因为它思路简洁且易于实现；随后再简要说明 **滑动窗口 + 可变唯一字符数** 的思路。

#### 思路（分治）

1. **找「坏字符」**  
   在整段字符串 `s` 中统计每个字符的出现次数。若某字符出现次数 **小于 k**，我们称它为「坏字符」。  
   - 「坏字符」不可能出现在合法子串里（因为它本身已经不满足 k 次）。  
   - 因此，合法子串一定被这些坏字符 **切断**，即合法子串只能出现在 **坏字符之间的连续片段** 中。

2. **递归求解**  
   - 如果 `s` 本身没有坏字符，说明整个 `s` 已经合法，直接返回 `len(s)`。  
   - 否则，以每个坏字符为分割点，把 `s` 切成若干子段 `segments`（这些子段里不含坏字符）。对每个子段递归求解「最长合法子串」的长度，返回最大的那个。  

3. **递归结束条件**  
   - 当子段的长度小于 `k` 时，显然不可能满足「每个字符出现 ≥ k」的要求，直接返回 0。  

**类比**：把字符串想象成一根绳子，坏字符就是绳子上的结。我们只能在结之间的「平直段」里找最长的满足条件的子绳子。每次遇到结，就把绳子剪开，递归处理每段。

#### 代码（Python）

```python
from collections import Counter

def longestSubstring(s: str, k: int) -> int:
    """
    分治法：在当前区间里找出现次数 < k 的字符，将区间切分，
    对每个子区间递归求解，返回最大的合法子串长度。
    """
    # 基础剪枝：区间长度不足 k，必然不合法
    if len(s) < k:
        return 0

    # 统计当前区间的字符频次
    freq = Counter(s)

    # 找出所有「坏字符」——出现次数 < k 的字符
    bad_chars = set(ch for ch, cnt in freq.items() if cnt < k)

    # 如果没有坏字符，说明整个区间合法
    if not bad_chars:
        return len(s)

    # 以坏字符为分割点，切成若干子段
    max_len = 0
    start = 0
    for i, ch in enumerate(s):
        if ch in bad_chars:
            # 当前子段是 s[start:i]（不包含坏字符）
            max_len = max(max_len, longestSubstring(s[start:i], k))
            start = i + 1          # 跳过坏字符，开始新子段
    # 处理最后一个子段
    max_len = max(max_len, longestSubstring(s[start:], k))

    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n log n)`（平均情况）  
  - 每一层递归会遍历当前子串一次来统计频次（`O(length)`），然后把子串按坏字符切开。  
  - 最坏情况下，每次只能切掉一个字符（例如 `s = "ab...z"`，`k = 2`），递归深度达到 `O(n)`，此时复杂度退化为 `O(n²)`。  
  - 但在实际数据（字母种类固定为 26）下，坏字符往往一次能把区间切成多段，递归深度约为 `log_{26/k}(n)`，因此平均时间接近 `O(n log n)`，足以通过 `10⁴` 规模的限制。

- **空间复杂度**：`O(log n)`（递归栈深度）  
  - 递归深度与分治的层数相同，最坏 `O(n)`，平均 `O(log n)`。额外的计数器是常数大小（26 个字母）。

---

#### 思路（滑动窗口 + 可变唯一字符数）——简要说明

1. 设定窗口左指针 `left`，右指针 `right` 向右滑动。  
2. 维护窗口内 **不同字符的种类数** `unique`，以及 **出现次数≥k 的字符种类数** `count_at_least_k`。  
3. 枚举可能的「窗口内最多出现的不同字符数」`target`（从 1 到 26），对每个 `target` 用滑动窗口求最长满足 `unique == target` 且 `count_at_least_k == target` 的子串。  
4. 取所有 `target` 下的最大长度即为答案。

该方法的时间复杂度是 `O(26 * n) = O(n)`，空间 `O(26)`。如果你已经掌握滑动窗口，这是一种更快的实现思路。

---

## 心得

- **核心技巧**：**利用字符出现次数的约束把问题划分**。  
  - 在分治里，用「出现次数 < k 的字符」把字符串切割成独立子问题。  
  - 在滑动窗口里，用「窗口内不同字符的上限」把搜索空间限制到可管理的范围。  

- **适用的题型**  
  1. **最长满足字符频次条件的子串**（本题）。  
  2. **字符种类受限的子串**（如「最长无重复字符子串」）。  
  3. **分治式字符串划分**（如「划分字符串使每段满足条件」）。

- **一句话总结解题钥匙**：  
  > 把「不可能出现的字符」先找出来，把它们当作「墙」把问题分块，只在「墙」之间搜索。

---

## 反思

- **第一反应**：直接枚举所有子串检查频次——思路最直观但效率极低。  
- **最容易踩的坑**  
  - 忽略了子串长度可能小于 `k` 的情况，导致递归不终止或返回错误结果。  
  - 在滑动窗口实现时，忘记在移动左指针时同步更新 `unique` 与 `count_at_least_k`，会产生错误的窗口状态。  
- **下次遇到同类题**：  
  1. **先找出「必然不合法」的字符或位置**，把问题拆分。  
  2. **决定使用分治还是滑动窗口**：如果约束是「每个字符至少出现 k 次」且字符种类有限，分治往往更直观；若约束是「窗口内字符种类上限」则滑动窗口更高效。