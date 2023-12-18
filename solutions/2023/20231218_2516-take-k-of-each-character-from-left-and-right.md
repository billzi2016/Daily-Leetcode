# #2516. 从左侧和右侧各取 k 个字符 / Take K of Each Character From Left and Right

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of the characters 'a', 'b', and 'c' and a non-negative integer k. Each minute, you may take either the leftmost character of s, or the rightmost character of s.
Return the minimum number of minutes needed for you to take at least k of each character, or return -1 if it is not possible to take k of each character.

**Examples**

**Example 1:**

```
Input: s = "aabaaaacaabc", k = 2
Output: 8
Explanation: 
Take three characters from the left of s. You now have two 'a' characters, and one 'b' character.
Take five characters from the right of s. You now have four 'a' characters, two 'b' characters, and two 'c' characters.
A total of 3 + 5 = 8 minutes is needed.
It can be proven that 8 is the minimum number of minutes needed.
```

**Example 2:**

```
Input: s = "a", k = 1
Output: -1
Explanation: It is not possible to take one 'b' or 'c' so return -1.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of only the letters 'a', 'b', and 'c'.
- 0 <= k <= s.length

---

## 题目（中文翻译）

给定一个仅由字符 `'a'`、`'b'`、`'c'` 组成的字符串 `s`，以及一个非负整数 `k`。每分钟，你可以从 `s` 的左端取走最左侧的字符，或者从右端取走最右侧的字符。  
返回至少取到每种字符各 `k` 个所需的最少分钟数；如果无法取到每种字符各 `k` 个，则返回 `-1`。

### 示例

**示例 1**  
```
Input: s = "aabaaaacaabc", k = 2
Output: 8
Explanation: 
从左侧取走三个字符，此时获得两个 `'a'` 和一个 `'b'`。  
再从右侧取走五个字符，此时获得四个 `'a'`、两个 `'b'`、两个 `'c'`。  
总共 3 + 5 = 8 分钟即可完成。可以证明 8 是所需的最小分钟数。
```

**示例 2**  
```
Input: s = "a", k = 1
Output: -1
Explanation: 无法取到 `'b'` 或 `'c'`，因此返回 -1。
```

### 约束条件
- `1 <= s.length <= 10^5`
- `s` 仅由字母 `'a'`、`'b'`、`'c'` 组成
- `0 <= k <= s.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举左边取多少字符**，记为 `L`（`0 ≤ L ≤ n`，`n = len(s)`），  
然后再从右边依次取字符，直到手里拥有每种字符至少 `k` 个为止。  
把左、右各取的字符数量相加，就是一种可行的“分钟数”。  
把所有 `L` 的情况都算一遍，最小的那个就是答案。

- **用到的数据结构**：  
  - 一个长度为 `3` 的计数数组（或字典）来记录当前已经拿到的 `'a'、'b'、'c'` 的数量。  
    这可以类比成**查字典**：键是字符 `'a'、'b'、'c'`，值是已经拿到的数量。  
  - 两个指针 `left`（固定在 `L`）和 `right`（从字符串最右端向左移动）来模拟取字符的过程。

- **为什么一定正确**：  
  对每个可能的左取数 `L`，我们都把右边的字符一个一个加入手中，直到满足 “每种字符 ≥ k”。  
  只要存在一种取法能满足条件，这种枚举必然会找到它；遍历完所有 `L` 后，最小的取法即为答案。

- **复杂度分析（大白话版）**  
  - 外层遍历 `L` 有 `n+1` 次。  
  - 对每个 `L`，右指针最坏要走完整个字符串（最多 `n` 步）。  
  - 所以最坏情况是 `n × n`，也就是 **O(n²)**。  
    把 `O(n²)` 想象成“把一本 10 万页的书每页都和每页再比一次”，显然会很慢。  
  - 计数数组只有 3 个格子，空间上只用了 **O(1)**（常数级）额外空间。

#### 代码（Python）

```python
def minMinutes_bruteforce(s: str, k: int) -> int:
    n = len(s)
    # 先检查整体是否可能
    total = {'a': 0, 'b': 0, 'c': 0}
    for ch in s:
        total[ch] += 1
    if any(total[ch] < k for ch in 'abc'):      # 任意一种字符本身不足 k
        return -1

    ans = float('inf')                          # 记录最小分钟数
    # 枚举左边取多少字符
    for L in range(n + 1):
        # 已经从左边拿到的计数
        have = {'a': 0, 'b': 0, 'c': 0}
        for i in range(L):
            have[s[i]] += 1

        # 如果左边已经满足了，就直接更新答案
        if all(have[ch] >= k for ch in 'abc'):
            ans = min(ans, L)
            continue

        # 从右边开始往左取，直到满足条件或右边取完为止
        R = 0
        right_idx = n - 1
        while right_idx >= L and not all(have[ch] >= k for ch in 'abc'):
            have[s[right_idx]] += 1
            R += 1
            right_idx -= 1

        # 检查是否真的满足了
        if all(have[ch] >= k for ch in 'abc'):
            ans = min(ans, L + R)

    return -1 if ans == float('inf') else ans
```

> 关键行的中文注释已经写在代码里。可以直接粘到 Python 环境里跑。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  想象把每个左侧取法都“重新检查一遍右侧”，所以会出现二次遍历的情况。  
- **空间复杂度**：`O(1)`  
  只用了几个计数变量，和字符串长度无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都重新遍历右边**，导致二次遍历。  
我们可以把视角换一下：  
> **如果把左、右两端取走的字符想象成“被删掉的”部分，那么剩下的中间连续子串就是“没被取走的”。**  

设整个字符串的每种字符总数为 `cnt[ch]`。  
要拿到至少 `k` 个字符 `ch`，等价于**在中间留下的子串中至多保留 `cnt[ch] - k` 个**（因为剩下的都必须被取走）。  

于是问题转化为：

> 在原串中，找 **最长的连续子串**，使得它内部每种字符的出现次数 **不超过** `cnt[ch] - k`。  
> 最后答案 = `n - 长度_of_最长子串`（因为我们把最长的“可以不取”的子串留在中间，其余全部取走）。

这正好可以用**滑动窗口（双指针）**一次遍历完成：

1. 预先统计 `cnt[ch]`，如果任意 `cnt[ch] < k`，直接返回 `-1`（根本取不到）。  
2. 设 `limit[ch] = cnt[ch] - k` 为每种字符在“中间子串”中允许的最大出现次数。  
3. 用两个指针 `left`、`right` 构造窗口 `[left, right)`，保持窗口内每种字符的计数 `window[ch]` **不超过** `limit[ch]`。  
   - 当加入 `s[right]` 仍合法时，右指针右移。  
   - 若加入后违背了限制（某字符出现次数 > limit），就**收缩左指针**，直到合法为止。  
4. 每次窗口合法时，用 `right - left` 更新 `max_len`（最长合法子串的长度）。  
5. 最终答案 = `n - max_len`。

> **类比**：把窗口看成一条可伸缩的橡皮筋，橡皮筋里装的字符不能超过盒子里给定的容量 `limit`。我们不断往右拉（尝试让子串更长），若超过容量就往左收回一点，保持“容量不超”。整个过程只遍历一次字符串。

#### 代码（Python）

```python
def minMinutes(s: str, k: int) -> int:
    n = len(s)
    # 1️⃣ 统计整体字符出现次数
    total = {'a': 0, 'b': 0, 'c': 0}
    for ch in s:
        total[ch] += 1

    # 2️⃣ 先判断是否可能完成任务
    if any(total[ch] < k for ch in 'abc'):   # 任意字符本身不足 k
        return -1

    # 3️⃣ 计算每种字符在“中间子串”中允许的最大次数
    limit = {ch: total[ch] - k for ch in 'abc'}

    # 4️⃣ 滑动窗口寻找最长合法子串
    left = 0
    window = {'a': 0, 'b': 0, 'c': 0}
    max_len = 0

    for right in range(n):                     # 右指针一次遍历整个字符串
        ch = s[right]
        window[ch] += 1                        # 把右边的新字符加入窗口

        # 只要有字符超过了限制，就把左边的字符移出窗口
        while any(window[c] > limit[c] for c in 'abc'):
            left_ch = s[left]
            window[left_ch] -= 1               # 左指针左移，窗口收缩
            left += 1

        # 此时窗口合法，更新最长长度
        cur_len = right - left + 1
        if cur_len > max_len:
            max_len = cur_len

    # 5️⃣ 答案 = 总长度 - 最长可以“保留”的子串长度
    return n - max_len
```

> 代码中的每一步都写了中文注释，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n)`  
  左右指针每个最多前进 `n` 步，整个过程只遍历一次字符串。相比暴力的 `O(n²)`，快了几个数量级。  
- **空间复杂度**：`O(1)`  
  只用了几个常数大小的计数器（`total、limit、window`），与 `n` 无关。

---

## 心得

- **核心技巧**：把“从两端取字符”转化为“在中间留下一个合法子串”，进而使用 **滑动窗口**（双指针）找最长满足上限的子串。  
- **适用的题型**  
  1. “最少删除使字符串满足某种条件”——如 *最少删除子数组使其和 ≤ target*。  
  2. “在字符/数字序列中找最长满足频次上限的子段”。  
  3. “从两端取元素，目标是满足计数条件”——本题的变形。  
- **一句话总结解题钥匙**：**把两端取走的操作视作“删除”，则问题等价于“保留最长合法子串”，滑动窗口一次遍历即可求解**。

---

## 反思

- **第一反应**：直接枚举左侧取多少，再从右侧补齐——这就是暴力思路。  
- **最容易踩的坑**  
  - 忘记先检查整体字符数量是否足够 `k`，会在后面出现错误的负数答案。  
  - 滑动窗口中“窗口非法”时的收缩条件要写对：**任何字符出现次数 > limit**，而不是只看单个字符。  
  - `k = 0` 时，答案应该是 `0`（不需要取任何字符），代码在统计 `limit` 时自然会得到 `limit = total`，窗口可以是全串，返回 `n - n = 0`，但要确保没有除以 0 的错误。  
- **下次遇到同类题**：第一步先**把“取/删”问题转化为“保留子数组的约束”**，然后思考是否可以用 **滑动窗口** 或 **前缀和** 在 O(n) 时间内完成。这样就能快速跳出暴力的陷阱。