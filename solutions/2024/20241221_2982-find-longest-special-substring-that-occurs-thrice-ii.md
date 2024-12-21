# #2982. 寻找出现三次的最长特殊子串 II / Find Longest Special Substring That Occurs Thrice II

> 难度：中等 · 标签：Hash Table、String、Binary Search、Sliding Window、Counting · [LeetCode 链接](https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-ii/)

---

## 题目（英文原版）

**Description**

You are given a string s that consists of lowercase English letters.
A string is called special if it is made up of only a single character. For example, the string "abc" is not special, whereas the strings "ddd", "zz", and "f" are special.
Return the length of the longest special substring of s which occurs at least thrice, or -1 if no special substring occurs at least thrice.
A substring is a contiguous non-empty sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "aaaa"
Output: 2
Explanation: The longest special substring which occurs thrice is "aa": substrings "aaaa", "aaaa", and "aaaa".
It can be shown that the maximum length achievable is 2.
```

**Example 2:**

```
Input: s = "abcdef"
Output: -1
Explanation: There exists no special substring which occurs at least thrice. Hence return -1.
```

**Example 3:**

```
Input: s = "abcaba"
Output: 1
Explanation: The longest special substring which occurs thrice is "a": substrings "abcaba", "abcaba", and "abcaba".
It can be shown that the maximum length achievable is 1.
```

**Constraints**

- 3 <= s.length <= 5 * 105
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个仅包含小写英文字母的字符串 `s`。  
如果一个字符串仅由同一个字符组成，则称其为 **特殊（special）** 字符串。例如 `"ddd"`、`"zz"`、`"f"` 是特殊字符串，而 `"abc"` 不是。  

返回 `s` 中出现至少三次的最长特殊子串（substring）的长度；如果不存在出现至少三次的特殊子串，返回 `-1`。  

子串（substring）是字符串中连续且非空的字符序列。  

### 示例  

#### 示例 1  
**输入**: `s = "aaaa"`  
**输出**: `2`  
**解释**: 出现三次的最长特殊子串是 `"aa"`，它在 `s` 中出现了三次（分别为下标 `[0,1]`、`[1,2]`、`[2,3]`）。可以证明最大长度只能是 `2`。  

#### 示例 2  
**输入**: `s = "abcdef"`  
**输出**: `-1`  
**解释**: 不存在出现至少三次的特殊子串，故返回 `-1`。  

#### 示例 3  
**输入**: `s = "abcaba"`  
**输出**: `1`  
**解释**: 出现三次的最长特殊子串是 `"a"`，它在 `s` 中出现了三次（下标分别为 `0`、`3`、`5`）。可以证明最大长度只能是 `1`。  

### 约束条件  

- `3 <= s.length <= 5 * 10^5`  
- `s` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **所有可能的子串** 都枚举出来，判断它是不是“special”（只由同一个字符组成），如果是再统计它在原串中出现了多少次，出现次数≥3 的就记录下它的长度，最后取最大长度。  

- **枚举子串**：把字符串的左端点 `i` 和右端点 `j`（`i ≤ j`）两层循环遍历，子串就是 `s[i:j+1]`。  
- **判断 special**：遍历子串的每个字符，检查是否全相同。可以把第一个字符记下来，后面的字符只要有一个不相同就立刻判定为非 special。  
- **统计出现次数**：对每一个满足 special 条件的子串，再在原串里滑动窗口查找它出现了几次（这里同样是 O(n) 的遍历）。  

> **生活化类比**：把字符串想象成一排彩色珠子。暴力解就像让小朋友把每一种颜色的连续珠子剪下来，随后再把剪下来的每段珠子放回原串里，一次又一次地找有没有完全相同的三段。  

因为我们把所有可能的子串都检查了一遍，肯定不会漏掉答案，所以方法是 **正确** 的。  

#### 代码（Python）  

```python
def longestSpecialSubstring_bruteforce(s: str) -> int:
    n = len(s)
    best = -1                         # 记录当前找到的最长长度

    # 枚举所有子串的左端点 i
    for i in range(n):
        # 枚举所有子串的右端点 j（i <= j）
        for j in range(i, n):
            # ---------- 判断子串 s[i:j+1] 是否为 special ----------
            sub = s[i:j+1]
            first_char = sub[0]
            is_special = True
            for ch in sub:
                if ch != first_char:   # 只要出现不同字符，就不是 special
                    is_special = False
                    break
            if not is_special:
                continue               # 直接进入下一个子串

            # ---------- 统计该 special 子串在原串中出现了多少次 ----------
            cnt = 0
            # 用滑动窗口遍历整个字符串，寻找完全相同的子串
            for start in range(n - len(sub) + 1):
                if s[start:start+len(sub)] == sub:
                    cnt += 1
                if cnt >= 3:           # 已经达到三次，后面不用再继续计数
                    break

            # 如果出现次数不少于三次，尝试更新答案
            if cnt >= 3:
                best = max(best, len(sub))

    return best
```

#### 复杂度  

- **时间复杂度**：  
  - 枚举子串有两层循环，组合数是 `O(n²)`（左端点 × 右端点）。  
  - 对每个子串我们最多再遍历一次原串来计数，最坏情况是 `O(n)`。  
  - 因此总体是 `O(n³)`，在最坏的 5·10⁵ 长度下根本跑不完。  
  - 用大白话说，**立方**的时间就像让 1000 个人每人排队 1000 次再排 1000 圈，速度极慢。  

- **空间复杂度**：`O(1)`，只用了常数个临时变量。  

> 暴力解虽然能帮助我们**理清问题**，但在实际面试或竞赛里根本不可用，需要进一步优化。  

---  

### 2. 最优解  

#### 思路  

从暴力解出发，**慢的地方**在于我们反复检查同一个字符的连续段。实际上，题目只关心**“只由同一字符组成的子串”**，这类子串天然就是 **某个字符的连续块**（如 `"aaa"`、`"bb"`），而不需要去枚举所有起止位置。  

**关键观察 1**：  
对每个位置 `i`，记 `len[i]` 为以 `s[i]` 结尾的最长 special 子串的长度。  
- 如果 `s[i] == s[i-1]`，则 `len[i] = len[i-1] + 1`（因为可以在前一个块后面再加一个相同字符）。  
- 否则 `len[i] = 1`（只能自己单独成块）。  

这样只需要一次线性遍历就能得到所有 `len[i]`，时间 `O(n)`。  

**关键观察 2**：  
同一个字符的所有 `len[i]` 只会出现在它自己的 **连续块**里。把这些值按照字符分组（最多 26 组），每组内部我们只关心 **出现次数最多的前三个长度**。  

为什么只要前三个？  
- 若一个字符的最长块长度是 `L1`，第二长是 `L2`，第三长是 `L3`（可能相等），  
- 那么以该字符组成的任意 special 子串的出现次数恰好等于它在原串中出现的 **块数**。  
- 要让某个长度 `L` 出现至少三次，必须在这三个块中 **每个块的长度都 ≥ L**。  
- 因此，能够满足 “出现 ≥3 次” 的最大长度正好是该字符 **第三大的块长度**（如果块数少于 3，则不存在）。  

**核心算法**：  
1. 一次遍历求 `len[i]`。  
2. 用一个字典 `top3[char] = [a, b, c]`（从大到小）记录每个字符当前的前三大块长度。  
   - 对每个 `len[i]`，把它插入对应字符的列表并保持排序，仅保留前 3。  
3. 最后遍历 26 个字符，取每个字符列表的第三个元素（如果存在）中的最大值，即答案。  

**类比**：  
把每个字符看成一种颜色的积木，`len[i]` 是某堆积木的高度。我们只需要记住每种颜色最高的三堆积木，因为想要三次出现，就必须从这三堆中挑出一个共同的高度。  

#### 代码（Python）  

```python
def longestSpecialSubstring(s: str) -> int:
    """
    返回最长的、只由同一字符组成且在 s 中出现至少三次的子串长度。
    若不存在返回 -1。
    """
    # 1. 计算以每个位置结尾的最长 special 子串长度
    n = len(s)
    cur_len = 0                     # 当前连续块的长度
    # 用字典维护每个字符的 top3（从大到小）
    top3 = {ch: [] for ch in set(s)}   # 只为出现过的字符创建键

    for i in range(n):
        if i > 0 and s[i] == s[i - 1]:
            cur_len += 1           # 同字符继续扩展
        else:
            cur_len = 1            # 新块，从 1 开始

        # 2. 将 cur_len 插入对应字符的 top3 列表
        lst = top3[s[i]]
        # 手动维护有序的前三大（因为列表长度 ≤ 3，直接线性插入即可）
        inserted = False
        for idx, val in enumerate(lst):
            if cur_len > val:
                lst.insert(idx, cur_len)
                inserted = True
                break
        if not inserted:
            lst.append(cur_len)    # 放在最后

        # 只保留最大的三个
        if len(lst) > 3:
            lst.pop()              # 删除最小的那个

    # 3. 在所有字符的 third largest 中取最大值
    answer = -1
    for lst in top3.values():
        if len(lst) >= 3:           # 至少有三块
            answer = max(answer, lst[2])   # 第三大的长度

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，所有对 `top3` 的插入、删除都是常数时间（列表长度不超过 3）。  
  - 用大白话说，就是“把 500,000 本书只读一遍”，速度很快。  

- **空间复杂度**：`O(1)`（严格来说是 `O(26)`）  
  - 我们只保存每个字符的最多 3 个整数，最多 26 × 3 = 78 个整数，和输入规模无关。  

> 与暴力解相比，时间从 **立方级** 降到了 **线性级**，几乎瞬间可以处理最大输入。  

---  

## 心得  

- **核心技巧**：把“只由单字符组成的子串”转化为“字符的连续块”，并用 **每字符的前三大块长度** 来判断是否能出现三次。  
- **适用场景**：  
  1. “出现至少 k 次的最长相同字符子串” 类似题（k 可为 2、3、4…）。  
  2. “统计每个字符出现的最长连续段并取某个排名” 的题目（如 LeetCode 2024‑06‑XX “Longest Repeating Character Substring”).  
  3. “在字符串中找满足出现次数阈值的子序列/子串” 时，利用 **分组 + 维护前 k 大** 的思路。  
- **一句话总结**：**把问题抽象成“每个字符的块高度”，只需保留前三高即可得到答案**。  

## 反思  

- **第一反应**：直接想枚举所有子串，写出暴力实现，想验证思路是否正确。  
- **最容易踩的坑**：  
  - 忘记 **块数少于 3** 时应直接返回 `-1`。  
  - 在维护 `top3` 时，如果直接使用 `sorted` 或 `heapq`，会额外增加不必要的 `O(log n)` 开销。  
  - 边界条件：字符串全相同时，`len[i]` 会一直递增，需要及时更新 `top3`，否则会错失更大的第三大值。  
- **下次类似题目**：第一步先**把字符串划分为“同字符的连续段”，统计每段长度，再**按字符分组**，只保留需要的前 k 大值。这样可以把原本的指数/平方复杂度瞬间压到线性。