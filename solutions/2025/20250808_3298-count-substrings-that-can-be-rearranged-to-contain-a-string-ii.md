# #3298. 计数可重排后包含指定字符串的子串 II / Count Substrings That Can Be Rearranged to Contain a String II

> 难度：困难 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-ii/)

---

## 题目（英文原版）

**Description**

You are given two strings word1 and word2.
A string x is called valid if x can be rearranged to have word2 as a prefix.
Return the total number of valid substrings of word1.
Note that the memory limits in this problem are smaller than usual, so you must implement a solution with a linear runtime complexity.

**Examples**

**Example 1:**

```
Input: word1 = "bcca", word2 = "abc"
Output: 1
Explanation:
The only valid substring is "bcca" which can be rearranged to "abcc" having "abc" as a prefix.
```

**Example 2:**

```
Input: word1 = "abcabc", word2 = "abc"
Output: 10
Explanation:
All the substrings except substrings of size 1 and size 2 are valid.
```

**Example 3:**

```
Input: word1 = "abcabc", word2 = "aaabc"
Output: 0
```

**Constraints**

- 1 <= word1.length <= 106
- 1 <= word2.length <= 104
- word1 and word2 consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `word1` 和 `word2`。  
若一个字符串 `x` 能够通过重新排列（rearranged）使得 `word2` 成为其前缀（prefix），则称 `x` 为有效（valid）。  
返回 `word1` 中所有有效子串的数量。  
注意，本题的内存限制比平时更小，因而必须实现 **线性时间复杂度**（O(n)）的解法。

示例 1:  
Input: word1 = "bcca", word2 = "abc"  
Output: 1  
Explanation:  
唯一的有效子串是 `"bcca"`，它可以重新排列为 `"abcc"`，从而使 `"abc"` 成为前缀。

示例 2:  
Input: word1 = "abcabc", word2 = "abc"  
Output: 10  
Explanation:  
除长度为 1 和 2 的子串外，所有子串均有效。

示例 3:  
Input: word1 = "abcabc", word2 = "aaabc"  
Output: 0  

约束条件  
- 1 ≤ `word1`.length ≤ 10⁶  
- 1 ≤ `word2`.length ≤ 10⁴  
- `word1` 和 `word2` 仅由小写英文字母组成

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 `word1` 的所有子串枚举出来，逐个判断它们能否通过重新排列得到 `word2` 作为前缀。  

- **枚举子串**：两层循环，外层决定子串的左端点 `i`，内层决定右端点 `j`（`i ≤ j`），子串就是 `word1[i:j+1]`。  
- **检查合法性**：把子串的字符出现次数统计到一个长度为 26 的数组（相当于“查字典”，字母是键，出现次数是页码），再和 `word2` 的字符频次数组逐个比较：只要每个字母在子串里的次数 **不少于** 在 `word2` 里的次数，说明可以把子串重新排列，使得 `word2` 成为前缀。  

> **为什么正确？**  
> 重新排列只会改变字符的顺序，不会改变每种字符的出现次数。只要子串里已经“拥有” `word2` 所需的每种字符的数量，就一定能把这些字符搬到子串的最前面，形成以 `word2` 为前缀的排列。

#### 代码（Python）

```python
def count_substrings_bruteforce(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    if m > n:                         # word2 太长，根本不可能
        return 0

    # 统计 word2 的字符需求，类似字典查词义
    need = [0] * 26
    for ch in word2:
        need[ord(ch) - ord('a')] += 1

    ans = 0
    # 枚举所有子串的左端点 i
    for i in range(n):
        # cnt 用来统计当前子串里每个字符的出现次数
        cnt = [0] * 26
        # 枚举右端点 j，逐步扩展子串
        for j in range(i, n):
            idx = ord(word1[j]) - ord('a')
            cnt[idx] += 1                # 把新字符加入统计

            # 子串长度必须至少和 word2 一样长才有可能合法
            if j - i + 1 < m:
                continue

            # 检查是否满足所有字符的需求
            ok = True
            for k in range(26):
                if cnt[k] < need[k]:
                    ok = False
                    break
            if ok:
                ans += 1                 # 合法子串计数
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n² * 26)` ≈ `O(n²)`  
  - 两层循环产生 `≈ n²/2` 个子串，每次检查需要遍历 26 个字母（常数），所以整体是二次方级别。  
  - 用大白话说，如果 `word1` 长度是 10⁴，算法大概要做 10⁸ 次简单操作，已经很慢了。  
- **空间复杂度**：`O(26)` ≈ `O(1)`  
  - 只用了两个长度为 26 的数组来存字符计数，和字符串长度无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有子串**，这导致了二次方的时间。  
观察一下题目要求：

> 子串只要 **包含** `word2` 所需的每种字符的足够数量，就一定可以重新排列得到以 `word2` 为前缀的字符串。  

这是一种 “**至少** 满足” 的条件，具有**单调性**：  
- 把窗口往右扩大（加入更多字符）不会让已经满足的窗口变“不满足”。  
- 只要窗口满足条件，窗口内部的任意更大的子串（左端点更左）也一定满足。

单调性提示我们可以使用 **滑动窗口 + 双指针** 来一次遍历完成计数。

**核心概念**  

| 概念 | 类比 | 解释 |
|------|------|------|
| `need[26]` | 查字典的“页码” | `need[c]` 表示 `word2` 中字符 `c` 需要出现多少次 |
| `window[26]` | 手里拿的“字母卡片” | 当前窗口 `[left, right]` 中每个字符的实际出现次数 |
| `missing` | 还缺多少“卡片” | 统计当前窗口仍然缺少的 `word2` 必要字符的总数，`missing==0` 表示窗口已经满足条件 |

**步骤**  

1. **预处理**  
   - 统计 `word2` 的字符需求 `need`。  
   - 用变量 `missing = total_needed`（即 `len(word2)`）记录窗口还缺多少必需字符。  

2. **右指针扩张**（遍历 `word1`）  
   - 把 `right` 指向的字符加入 `window`。  
   - 如果加入的字符仍然在需求范围内（即加入前 `window[c] < need[c]`），则把 `missing` 减 1，因为我们刚刚补齐了一个必需字符。  

3. **左指针收缩**（寻找 **最左** 的合法起点）  
   - 当 `missing == 0`（窗口已经满足）时，尝试把左端点左移，前提是 **去掉的字符不是必需字符的最后一个**。也就是说，`window[word1[left]] > need[char]` 时可以安全删除，`missing` 保持 0。  
   - 循环结束后，`left` 就是 **最左** 能让窗口合法的下标。  

4. **计数**  
   - 对当前的 `right`，所有以 `0 … left` 为起点的子串都合法（因为把左端点再往左只会让窗口更大，必定仍满足）。  
   - 因此，把 `left + 1` 加到答案中。  

5. **继续右移**，重复 2~4，直至遍历完 `word1`。  

**为什么是线性时间？**  

- 每个字符最多被右指针加入一次，又最多被左指针移出一次。  
- 所以所有指针的移动次数总和 ≤ `2 * len(word1)`，即 `O(n)`。  

**空间** 只需要两个长度为 26 的数组和几个整数，属于常数级别。

#### 代码（Python）

```python
def count_substrings(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    if m > n:                     # word2 长度超过 word1，直接返回 0
        return 0

    # 1️⃣ 统计 word2 的需求（类似查字典的页码）
    need = [0] * 26
    for ch in word2:
        need[ord(ch) - ord('a')] += 1

    # 2️⃣ 滑动窗口的状态
    window = [0] * 26          # 当前窗口内每个字母的计数
    missing = m                # 还缺多少必需字符（初始等于 word2 长度）
    left = 0
    ans = 0

    # 3️⃣ 右指针遍历 word1
    for right, ch in enumerate(word1):
        idx = ord(ch) - ord('a')
        window[idx] += 1

        # 如果加入的这个字符仍然在需求范围内，missing 减 1
        if window[idx] <= need[idx]:
            missing -= 1

        # 4️⃣ 当窗口已经满足（missing == 0）时，尽量左移 left
        if missing == 0:
            # 把左端点尽量往右收缩，只要移除的字符不是必需字符的“最后一张”
            while left <= right:
                l_idx = ord(word1[left]) - ord('a')
                # 如果窗口里还有多余的该字符，安全移除
                if window[l_idx] > need[l_idx]:
                    window[l_idx] -= 1
                    left += 1
                else:               # 再移除就会缺少必需字符，停下来
                    break

            # 5️⃣ 计数：所有以 0 … left 为起点的子串都是合法的
            ans += left + 1

    return ans
```

> **代码解释（关键行）**  
> - `need[idx]`：记录 `word2` 中字符 `ch` 需要多少个。  
> - `missing`：当它降到 0 时，说明窗口已经拥有了 `word2` 所需的全部字符。  
> - `while window[l_idx] > need[l_idx]`：只要左端点的字符在窗口里是“多余的”，就可以把它踢出，进一步左移 `left`，让窗口 **尽可能小**。  
> - `ans += left + 1`：`left` 是当前能够得到的 **最左** 合法起点，下标 `0 … left` 都合法，所以加上 `left+1` 个子串。

#### 复杂度  

- **时间复杂度**：`O(n)`（`n = len(word1)`）  
  - 每个字符最多进入窗口一次、离开窗口一次。  
  - 与暴力解的 `O(n²)` 相比，快了一个数量级，能够轻松处理 `10⁶` 级别的输入。  

- **空间复杂度**：`O(1)`（常数 26）  
  - 只用了两个长度为 26 的数组和若干整数，和字符串长度无关。

---

## 心得  

- **核心技巧**：利用 **滑动窗口 + 双指针** 统计“满足至少某个字符频次要求”的子数组/子串数量。  
- **适用题型**（类似思路）：  
  1. “子数组/子串中包含所有目标字符（或数字）”——如 LeetCode 76 `Minimum Window Substring`。  
  2. “子数组和大于等于 K”——使用双指针求满足条件的子数组个数。  
  3. “统计满足字符出现次数上限的子串”——如 LeetCode 340 `Longest Substring with At Most K Distinct Characters`。  
- **一句话总结解题钥匙**：**把窗口尽可能收紧到“刚好满足所有必需字符”，然后利用单调性把左端点左侧的所有起点都算进答案**。

---

## 反思  

- **第一反应**：直接枚举子串检查，没想到可以利用“只要包含足够字符就行”的单调性。  
- **最容易踩的坑**：  
  - **遗漏 `missing` 的更新**：加入字符时只在 `window[idx] <= need[idx]` 时才减 `missing`，否则会错误地把多余字符也算进缺口。  
  - **左指针收缩的条件**：必须判断 **“窗口里还有多余的该字符”**，否则会把必需字符的最后一个也删掉，导致窗口不再合法。  
  - **边界情况**：`word2` 长度大于 `word1` 时直接返回 0，防止后续循环出现负数 `missing`。  
- **下次类似题目**的第一步：**先明确“满足条件”是否具备单调性**（窗口扩大不会破坏），如果是，就立刻考虑 **滑动窗口** 并找出“最左/最右”合法起点或终点的办法。