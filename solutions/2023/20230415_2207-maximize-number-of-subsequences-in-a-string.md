# #2207. 最大化字符串中的子序列数量 / Maximize Number of Subsequences in a String

> 难度：中等 · 标签：String、Greedy、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximize-number-of-subsequences-in-a-string/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string text and another 0-indexed string pattern of length 2, both of which consist of only lowercase English letters.
You can add either pattern[0] or pattern[1] anywhere in text exactly once. Note that the character can be added even at the beginning or at the end of text.
Return the maximum number of times pattern can occur as a subsequence of the modified text.
A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.

**Examples**

**Example 1:**

```
Input: text = "abdcdbc", pattern = "ac"
Output: 4
Explanation:
If we add pattern[0] = 'a' in between text[1] and text[2], we get "abadcdbc". Now, the number of times "ac" occurs as a subsequence is 4.
Some other strings which have 4 subsequences "ac" after adding a character to text are "aabdcdbc" and "abdacdbc".
However, strings such as "abdcadbc", "abdccdbc", and "abdcdbcc", although obtainable, have only 3 subsequences "ac" and are thus suboptimal.
It can be shown that it is not possible to get more than 4 subsequences "ac" by adding only one character.
```

**Example 2:**

```
Input: text = "aabb", pattern = "ab"
Output: 6
Explanation:
Some of the strings which can be obtained from text and have 6 subsequences "ab" are "aaabb", "aaabb", and "aabbb".
```

**Constraints**

- 1 <= text.length <= 105
- pattern.length == 2
- text and pattern consist only of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的字符串 `text` 和另一个长度为 2 的下标从 0 开始的字符串 `pattern`，两者仅由小写英文字母组成。  
你可以在 `text` 的任意位置（包括开头和结尾）恰好插入一次字符，该字符可以是 `pattern[0]` 或 `pattern[1]`。  
返回在插入字符后，`pattern` 作为子序列（subsequence）出现在修改后 `text` 中的最大次数。  

子序列是指通过删除原字符串中的若干（也可以为零）字符而不改变剩余字符顺序得到的字符串。

**示例**  

**示例 1**  
Input: `text = "abdcdbc"`, `pattern = "ac"`  
Output: `4`  
Explanation:  
如果在 `text[1]` 与 `text[2]` 之间插入 `pattern[0] = 'a'`，得到 `"abadcdbc"`。此时 `"ac"` 作为子序列出现了 4 次。  
其他一些在插入一个字符后也能得到 4 条 `"ac"` 子序列的字符串包括 `"aabdcdbc"` 和 `"abdacdbc"`。  
然而像 `"abdcadbc"`、`"abdccdbc"`、`"abdcdbcc"` 这样的字符串虽然可以通过插入得到，但它们的 `"ac"` 子序列数并不达到最大值……

**示例 2**  
Input: `text = "aabb"`, `pattern = "ab"`  
Output: `6`  
Explanation:  
一些通过在 `text` 中插入字符后能够得到 6 条 `"ab"` 子序列的字符串示例有 `"aaabb"`、`"aaabb"`（插入位置不同）以及 `"aabbb"`。

**约束条件**  

- `1 <= text.length <= 10^5`  
- `pattern.length == 2`  
- `text` 与 `pattern` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把字符 `pattern[0]` 或 `pattern[1]` 插入到 `text` 的每一个可能位置**（包括最前面和最后面），然后重新统计模式在新字符串中出现了多少次。  

- **插入位置**：设原字符串长度为 `n`，那么我们一共有 `n+1` 种插入方式（在下标 `0` 前、在下标 `1` 前、……、在下标 `n-1` 前、在下标 `n` 后）。  
- **统计子序列**：因为模式长度固定为 `2`，计数可以简化为“左边是 `pattern[0]`，右边是 `pattern[1]` 的配对数”。遍历一次字符串，维护已经看到的 `pattern[0]` 的数量 `cnt0`，每遇到一个 `pattern[1]` 就把 `cnt0` 加到答案中。  

把两步组合起来，就是：  
1. 对每个插入位置 `i`，生成新字符串 `new_text`（在 `i` 处插入 `pattern[0]` 或 `pattern[1]`）。  
2. 用上面的方法 O(n) 统计 `new_text` 中模式出现的次数。  
3. 取所有尝试中的最大值即为答案。  

这就是所谓的**暴力枚举**，思路清晰但效率不高。

#### 代码（Python）  

```python
def count_subseq(s: str, pat: str) -> int:
    """统计字符串 s 中模式 pat 出现的次数（长度为 2）。"""
    cnt0 = 0          # 已经看到的 pat[0] 的个数
    ans = 0
    for ch in s:
        if ch == pat[0]:
            cnt0 += 1
        if ch == pat[1]:
            ans += cnt0      # 每个 pat[1] 能和之前的所有 pat[0] 配对
    return ans


def max_subseq_bruteforce(text: str, pattern: str) -> int:
    n = len(text)
    best = 0
    # 试在每个位置插入 pattern[0] 或 pattern[1]
    for i in range(n + 1):                     # i 表示插入点，0 ≤ i ≤ n
        # 插入 pattern[0]
        s0 = text[:i] + pattern[0] + text[i:]
        best = max(best, count_subseq(s0, pattern))

        # 插入 pattern[1]
        s1 = text[:i] + pattern[1] + text[i:]
        best = max(best, count_subseq(s1, pattern))
    return best
```

> 关键行解释  
> - `cnt0 += 1`：相当于在“查字典”，把出现的 `pattern[0]` 记下来。  
> - `ans += cnt0`：每碰到 `pattern[1]`，就把它能配对的所有左侧 `pattern[0]` 加进去。  

#### 复杂度  

- **时间复杂度**：外层循环有 `n+1` 个插入位置，内层统计需要遍历一次新字符串（长度 `n+1`），所以总体是 `O((n+1) * (n+1)) ≈ O(n²)`。  
  - 大白话：如果原字符串有 10,000 个字符，暴力解大概要做 100 000 000 次“计数”，会明显超时。  
- **空间复杂度**：只用了常数个额外变量 `O(1)`（不计新建的临时字符串），但临时字符串本身会占用 `O(n)` 的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，我们发现 **真正耗时的地方是每次都重新遍历整条字符串**。  
其实我们根本不需要真的把字符插进去再重新计数，只要**知道插入后会多出多少配对**即可。  

下面一步步推导：

1. **原始配对数**  
   - 只需要一次遍历，统计 `text` 中已有的 `pattern` 子序列数，记作 `base`。  
   - 同样用 `cnt0` 记录左侧 `pattern[0]` 的出现次数，遍历时每遇到 `pattern[1]` 累加 `cnt0`。

2. **插入 `pattern[0]` 的效果**  
   - 把一个新的 `pattern[0]` 放在位置 `i`（`i` 前面有 `i` 个字符），它只能和**插入点右侧**的所有 `pattern[1]` 配对。  
   - 因此新增的配对数 = 右侧 `pattern[1]` 的个数。  
   - 只要我们知道每个位置右侧还有多少 `pattern[1]`（即 **后缀计数**），就可以直接算出插入 `pattern[0]` 的最佳增益。

3. **插入 `pattern[1]` 的效果**  
   - 同理，把 `pattern[1]` 放在位置 `i`，它只能和左侧的 `pattern[0]` 配对。  
   - 新增配对数 = 左侧 `pattern[0]` 的个数。  
   - 只要我们知道每个位置左侧有多少 `pattern[0]`（即 **前缀计数**），同样可以直接算出最佳增益。

4. **把两种情况取最大**  
   - `add0 = max_{i} (右侧 pattern[1] 个数)`  
   - `add1 = max_{i} (左侧 pattern[0] 个数)`  
   - 最终答案 = `base + max(add0, add1)`。

5. **特殊情况：两个字符相同**  
   - 当 `pattern[0] == pattern[1]` 时，模式变成 `"aa"`，配对方式是**任意两个相同字符的顺序**。  
   - 原本有 `c` 个该字符，配对数是 `C(c,2) = c*(c-1)/2`。  
   - 插入一个相同字符后，总数变成 `c+1`，配对数变为 `C(c+1,2)`。  
   - 直接返回 `(c+1)*c//2`，不需要前缀/后缀计算。

6. **实现细节**  
   - 只需要一次遍历就能得到 `base`、所有前缀 `pattern[0]` 的计数以及后缀 `pattern[1]` 的计数。  
   - 为了得到后缀计数，我们可以先遍历一次统计总的 `pattern[1]` 数，然后在第二遍从左到右维护“已经走过的 `pattern[0]` 数”和“剩余的 `pattern[1]` 数”。  

这样整体只需要 **O(n)** 的时间和 **O(1)** 的额外空间，完美满足题目约束。

#### 代码（Python）  

```python
def max_subseq_opt(text: str, pattern: str) -> int:
    # pattern 长度一定是 2
    a, b = pattern[0], pattern[1]

    # ---------- 特殊情况：两个字符相同 ----------
    if a == b:
        cnt = text.count(a)          # 原字符串中该字符的个数
        # 加入一个相同字符后，配对数 = C(cnt+1, 2)
        return (cnt + 1) * cnt // 2

    # ---------- 一遍遍历得到 base、前缀/后缀计数 ----------
    total_b = text.count(b)          # 所有 b 的总数
    pref_a = 0                        # 已经遍历到当前位置左侧的 a 的个数
    suffix_b = total_b                # 当前位置右侧（包括当前位置）b 的个数
    base = 0                          # 原始 text 中模式出现的次数
    max_add0 = 0                      # 插入 a 能得到的最大增益（右侧 b 的最多数量）
    max_add1 = 0                      # 插入 b 能得到的最大增益（左侧 a 的最多数量）

    for ch in text:
        # 当前字符属于右侧的 b，需要先把它从 suffix 中减掉
        if ch == b:
            suffix_b -= 1            # 以后遍历到的位置，右侧 b 少了一个

        # 统计原始配对数：每遇到一个 b，就把左侧已有的 a 加进去
        if ch == b:
            base += pref_a

        # 计算在“此插入点”插入 a / b 的增益
        # 插入 a：能配对的都是右侧的 b（即 suffix_b）
        max_add0 = max(max_add0, suffix_b)
        # 插入 b：能配对的都是左侧的 a（即 pref_a）
        max_add1 = max(max_add1, pref_a)

        # 最后再把当前字符计入左侧的 a（如果是 a 的话）
        if ch == a:
            pref_a += 1

    # ---------- 结果 ----------
    return base + max(max_add0, max_add1)
```

> 关键行解释  
> - `suffix_b -= 1`：相当于“把字典里后面的 b 抹掉”，因为我们已经走过它了。  
> - `base += pref_a`：每个 `b` 能和左边所有 `a` 配对，和暴力计数里 `ans += cnt0` 是同一个道理。  
> - `max_add0 = max(max_add0, suffix_b)`：记录“如果把 `a` 插在这里，右边还有多少 `b`”，取最大值即为最佳位置。  
> - `max_add1 = max(max_add1, pref_a)`：记录“如果把 `b` 插在这里，左边已有多少 `a`”。  

#### 复杂度  

- **时间复杂度**：只遍历一次字符串（或两次计数），每个字符做 O(1) 操作，整体是 **O(n)**。  
  - 对比暴力的 `O(n²)`，当 `n = 10⁵` 时，优化后只需要约 `10⁵` 次操作，秒级完成。  
- **空间复杂度**：只使用常数个变量 `O(1)`（不计输入本身），没有额外数组或哈希表。  

---

## 心得  

- **核心技巧**：把“插入后新增的配对数”拆解为**左侧计数**或**右侧计数**，利用**前缀和 / 后缀和**的思想在一次遍历中直接求出最大增益。  
- **适用场景**：  
  1. “在字符串中插入字符，使某种子序列/子串的出现次数最大” 类问题。  
  2. “固定模式长度为 2，统计配对数” 的计数问题，如 `count("ab")`、`count("xy")`。  
  3. 类似的 “在数组中插入元素，使逆序对/升序对数量最大” 的贪心/前缀计数题。  
- **一句话总结**：**插入一个字符的价值只取决于它左边已有的配对源或右边还有的配对目标，求最大即可。**  

---

## 反思  

- **第一反应**：直接暴力枚举所有插入位置并重新计数，想到“遍历+统计”。  
- **最容易踩的坑**：  
  - 忘记处理 `pattern[0] == pattern[1]` 的特殊情况，会导致前缀/后缀计数逻辑出错（因为左侧和右侧其实是同一种字符）。  
  - 计算后缀 `b` 时要先把当前字符从后缀中减掉，再使用，否则会把自己算进去，导致多加一次配对。  
  - 边界位置（最前面、最后面）同样需要考虑，因为插入点前/后可能为空。  
- **下次类似题目第一步**：先**明确插入一个字符会增加多少“配对”**，再用前缀/后缀统计快速求最大，而不是直接枚举。