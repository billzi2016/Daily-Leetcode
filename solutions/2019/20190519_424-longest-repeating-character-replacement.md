# #424. 最长重复字符替换 / Longest Repeating Character Replacement

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/longest-repeating-character-replacement/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.
Return the length of the longest substring containing the same letter you can get after performing the above operations.

**Examples**

**Example 1:**

```
Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.
```

**Example 2:**

```
Input: s = "AABABBA", k = 1
Output: 4
Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
The substring "BBBB" has the longest repeating letters, which is 4.
There may exists other ways to achieve this answer too.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of only uppercase English letters.
- 0 <= k <= s.length

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`。你可以选择字符串中的任意字符，将其改成任意其他大写英文字母（uppercase English character）。此操作至多可以执行 `k` 次。  
返回在完成上述操作后，能够得到的**相同字母的最长子串（substring）**的长度。

**示例 1**  
输入: `s = "ABAB"`, `k = 2`  
输出: `4`  
解释: 将两个 `'A'` 替换成 `'B'`，或者将两个 `'B'` 替换成 `'A'`，即可得到全由同一字符组成的子串，长度为 4。

**示例 2**  
输入: `s = "AABABBA"`, `k = 1`  
输出: `4`  
解释: 将中间的一个 `'A'` 替换成 `'B'`，得到 `"AABBBBA"`。子串 `"BBBB"` 是最长的重复字符子串，长度为 4。还有其他方式也能得到相同的答案。

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由大写英文字母组成。  
- `0 <= k <= s.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**枚举所有可能的子串**，检查它能否在最多 `k` 次字符替换后变成全部相同的字符。  

- **枚举子串**：用两个指针 `left`、`right`（或双层循环）遍历所有 `[left, right]` 区间，子串长度为 `right‑left+1`。  
- **统计字符出现次数**：对于每个子串，统计 26 个大写字母各出现了多少次（相当于把子串当成一本小字典，字母是“词”，出现次数是“页码”）。  
- **判断是否可行**：如果子串长度减去出现次数最多的那个字母的次数 ≤ `k`，说明只要把其余的字符全部换成出现次数最多的那个字母，就能得到全相同的子串。  

因为我们会检查 **所有** 子串，所以一定能找到最长的合法长度，正确性天然保证。  

**时间/空间分析（大白话）**  
- 枚举子串的次数是 `n`（左指针位置）* `n`（右指针位置），即大约 `n²` 次。  
- 对每个子串我们要遍历一次子串内部来统计字符，最坏情况下也要 `O(n)`，所以整体时间是 `O(n³)`，但我们可以在枚举时直接用一个长度为 26 的数组累计，时间降到 `O(n²)`。  
- 额外空间只需要保存 26 个计数器，算作 `O(1)`（常数空间）。  

> **O(n²)** 的意思是：如果字符串长度是 10，算法大概会执行 100 次左右的主要循环；如果长度是 1000，执行次数会涨到 1 000 000 次，增长速度是平方级的。

#### 代码（Python）  

```python
def characterReplacement_bruteforce(s: str, k: int) -> int:
    n = len(s)
    ans = 0                         # 保存目前找到的最长合法长度

    # 枚举左边界
    for left in range(n):
        # cnt 用来统计当前子串里每个字母出现的次数
        cnt = [0] * 26              # 26 个大写字母对应 26 个格子

        # 枚举右边界
        for right in range(left, n):
            idx = ord(s[right]) - ord('A')
            cnt[idx] += 1           # 把新加入的字符计数加一

            # 子串长度
            length = right - left + 1
            # 出现最多的字符次数
            max_freq = max(cnt)

            # 需要替换的字符数 = 子串长度 - 最多字符的次数
            if length - max_freq <= k:
                ans = max(ans, length)   # 合法则更新答案

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `n` 次，内层循环平均也遍历 `n/2` 次，整体是平方级别。  
- **空间复杂度**：`O(1)`  
  - 只用了固定大小的 26 元素数组，和输入大小无关。

---  

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，**瓶颈在于不停地重新统计子串内部字符的次数**。如果能够在 **滑动窗口** 中“增删”字符时即时更新计数，就可以把枚举子串的代价降到线性。  

**核心概念：滑动窗口 + 维护出现次数最多的字符**  

1. **窗口含义**：我们维护一个左闭右开的区间 `[left, right)`，表示当前考虑的子串。  
2. **窗口扩张**：右指针 `right` 每次右移一位，把新字符加入窗口，同时更新对应的计数 `cnt[char]`。  
3. **窗口收缩**：窗口的合法性由下面的条件判断：  
   - `window_len - max_cnt <= k`  
   - 其中 `window_len = right - left`，`max_cnt` 是窗口内出现次数最多的字符的计数。  
   - 这句话的意思是：要把窗口变成全部相同字符，最少需要替换的字符数 = 窗口长度减去出现最多的字符的次数。如果这数 ≤ `k`，说明我们可以在 `k` 次以内把窗口变成全相同，窗口合法。  
4. **收缩策略**：如果窗口不合法（需要的替换次数 > `k`），只能左指针右移，缩小窗口，同时把左侧字符的计数减一。  
5. **关键点**：**`max_cnt` 不一定每次都精确**。在左指针移动时，`max_cnt` 可能没有立刻下降，但这不会影响最终答案，因为只要窗口合法我们就记录长度，窗口不合法时会继续收缩，最终得到的最大长度一定是正确的。  

这样，**每个字符最多进入窗口一次、离开窗口一次**，时间是 `O(n)`。  

**为什么滑动窗口适用？**  
- 我们要找的是**最长**满足某种“最多可以改 k 个字符”的子串。  
- 当右指针继续往右走时，窗口只会变大或保持大小；只要窗口合法，就可以更新答案。  
- 当窗口非法时，左指针必须收缩才能再次合法，这正好对应“把窗口的左边界往右推”。  

#### 代码（Python）  

```python
def characterReplacement(s: str, k: int) -> int:
    cnt = [0] * 26                # 统计窗口内每个字母的出现次数
    left = 0                      # 窗口左边界
    max_cnt = 0                   # 窗口内出现次数最多的字母的次数
    ans = 0                       # 记录最长合法子串长度

    # 右指针遍历整个字符串
    for right in range(len(s)):
        idx = ord(s[right]) - ord('A')
        cnt[idx] += 1            # 把新字符计数加一
        max_cnt = max(max_cnt, cnt[idx])   # 更新窗口内的最大频次

        # 当前窗口长度
        window_len = right - left + 1
        # 需要替换的字符数 = 窗口长度 - 最多字符的出现次数
        if window_len - max_cnt > k:
            # 窗口不合法，需要收缩左边界
            left_idx = ord(s[left]) - ord('A')
            cnt[left_idx] -= 1    # 把左侧字符计数减一
            left += 1             # 左指针右移，窗口缩小
            # 注意：此时 max_cnt 可能没有立刻下降，但不影响后续判断

        # 窗口合法时更新答案（即使不合法也会在后面的迭代中再次合法）
        ans = max(ans, right - left + 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：左指针和右指针各最多遍历字符串一次，所有操作都是 O(1) 的计数更新。  
- **空间复杂度**：`O(1)`  
  - 只用了长度固定为 26 的计数数组，与字符串长度无关。  

与暴力解相比，时间从平方级下降到线性级，几乎可以在最大 `10⁵` 长度的输入上毫秒通过。  

---  

## 心得  

- **核心技巧**：滑动窗口 + 维护窗口内出现次数最多的字符（或叫“窗口内的众数”）。  
- **适用的题型**：  
  1. **最长子串满足 K 次修改**（本题）。  
  2. **最长子串包含至多 K 个不同字符**（LeetCode 340 – Longest Substring with At Most K Distinct Characters）。  
  3. **最长子数组和 ≤ K**（滑动窗口求和版）。  
- **一句话总结**：**把“最多可以改 k 次”转化为“窗口长度 - 最高频次 ≤ k”，用滑动窗口一次遍历搞定。**  

---  

## 反思  

- **第一反应**：看到“把任意字符改成相同字符”，自然想到枚举子串并检查是否可以统一。  
- **最容易踩的坑**：  
  - **`max_cnt` 的维护**：左指针移动时不要每次都遍历整个计数数组去重新求最大，保持“懒更新”即可。  
  - **窗口合法性判断的等号**：`<= k` 才算合法，写成 `< k` 会漏掉恰好用完 k 次的情况。  
  - **边界条件**：`k = 0` 时相当于找最长的相同字符子串，算法仍然成立。  
- **下次遇到同类题**：第一步先**把约束写成“窗口长度 - 最高频次 ≤ k”**，确认可以用滑动窗口；然后再决定如何高效维护最高频次。