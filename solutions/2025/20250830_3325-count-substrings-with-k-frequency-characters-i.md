# #3325. 计数出现至少 k 次字符的子串 I / Count Substrings With K-Frequency Characters I

> 难度：中等 · 标签：Hash Table、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-substrings-with-k-frequency-characters-i/)

---

## 题目（英文原版）

**Description**

Given a string s and an integer k, return the total number of substrings of s where at least one character appears at least k times.

**Examples**

**Example 1:**

```
Input: s = "abacb", k = 2
Output: 4
Explanation:
The valid substrings are:
```

**Example 2:**

```
Input: s = "abcde", k = 1
Output: 15
Explanation:
All substrings are valid because every character appears at least once.
```

**Constraints**

- 1 <= s.length <= 3000
- 1 <= k <= s.length
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`，返回 `s` 中满足**至少有一个字符出现次数不少于 `k` 次**的子串（substring）的总数。

**示例 1**  
Input: `s = "abacb", k = 2`  
Output: `4`  
Explanation:  
有效的子串有：

**示例 2**  
Input: `s = "abcde", k = 1`  
Output: `15`  
Explanation:  
所有子串均有效，因为每个字符至少出现一次。

**约束条件**  
- `1 <= s.length <= 3000`  
- `1 <= k <= s.length`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的子串枚举出来，逐一检查它们是否满足“至少有一个字符出现 k 次”。  
实现细节：

1. **枚举左端点 `left`**：从 `0` 到 `len(s)-1`。  
2. **枚举右端点 `right`**：从 `left` 开始向右扩展，每次把新字符加入一个计数表（哈希表），相当于在“查字典”：字符是 **key**，出现次数是 **value**。  
3. **检查条件**：遍历计数表，只要有一个 `value >= k`，说明当前子串合法，计数器 `ans` 加一。  

为什么正确？  
因为我们没有漏掉任何子串——左端点、右端点的每一种组合都被遍历一次；只要满足题目要求，就把它记下来。

**时间/空间复杂度**  
- 外层 `left` 循环 `n` 次，内层 `right` 最多也走 `n` 次，整体是 **O(n²)**。  
- 对每个子串我们维护一个计数表，最多记录 26 个小写字母，空间是 **O(1)**（常数级别）。  

> 大白话解释：如果字符串长度是 1000，暴力解大概要做 1,000,000 次“检查”，在电脑里跑还是能接受，但如果长度是 3000，次数会涨到 9,000,000，已经不够快了。

#### 代码（Python）

```python
def count_substrings_brute(s: str, k: int) -> int:
    n = len(s)
    ans = 0                     # 最终答案

    for left in range(n):       # 固定左端点
        freq = [0] * 26         # 哈希表：字符 -> 出现次数（用数组实现更快）
        for right in range(left, n):   # 右端点向右扩展
            idx = ord(s[right]) - ord('a')
            freq[idx] += 1                # 把新字符加入计数表

            # 检查是否已有字符出现 >= k 次
            ok = any(cnt >= k for cnt in freq)
            if ok:
                ans += 1                 # 满足条件，答案加一

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子串。  
- **空间复杂度**：`O(1)` —— 只用固定大小的数组（26），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于：每次右端点移动一步，都要**重新遍历整个计数表**去判断是否已经有字符出现 `k` 次。  
其实，只要我们把 **右端点只向右移动**（永不回退），并且在左端点每次左移时相应地更新计数表，就可以把检查过程变成 **常数时间**。这正是 **滑动窗口（双指针）** 的核心思想。

关键观察：

- 对固定的 `left`，如果子串 `s[left..right]` 已经满足条件，那么把 `right` 再往右扩展，子串仍然满足（因为已有字符的出现次数只会增多或保持不变）。  
- 因此，对每个 `left`，我们只需要找到**最左**的 `right` 使条件成立，记为 `first_ok`。那么以 `left` 为左端点的所有合法子串数量就是 `n - first_ok`（因为 `right` 可以是 `first_ok, first_ok+1, …, n-1`）。

实现步骤：

1. 用两个指针 `left`、`right` 表示当前窗口 `[left, right]`（右端点是**闭区间**）。  
2. `freq[26]` 记录窗口内每个字符的出现次数，`good` 表示窗口中 **出现次数 ≥ k 的字符种类数**。只要 `good > 0`，窗口就满足题目要求。  
3. 当 `good == 0` 时，继续右移 `right` 并更新计数表；当 `good > 0` 时，说明已经找到了 `first_ok`，此时把 `n - right` 加到答案中，然后左移 `left`，并相应地减掉 `freq`，可能导致 `good` 变回 0，需要再次右移 `right`。  
4. 特殊情况 `k == 1`：每个字符出现一次就满足，所有子串都是合法的，直接返回 `n*(n+1)//2`。

整个过程每个字符最多进入窗口一次、离开窗口一次，时间是 **线性 O(n)**。

#### 代码（Python）

```python
def count_substrings_opt(s: str, k: int) -> int:
    n = len(s)
    if k == 1:                               # 特例：所有子串合法
        return n * (n + 1) // 2

    freq = [0] * 26                           # 哈希表：字符出现次数
    good = 0                                  # 窗口中出现次数 >= k 的字符种类数
    ans = 0
    right = 0

    for left in range(n):                     # 固定左端点
        # 扩大右端点，直到窗口满足条件或右端点已经到末尾
        while right < n and good == 0:
            idx = ord(s[right]) - ord('a')
            freq[idx] += 1
            if freq[idx] == k:                # 第一次达到 k 次
                good += 1
            right += 1

        if good == 0:                         # 整个剩余字符串都不满足，直接结束
            break

        # 此时 right 已经指向第一个使窗口合法的下标（右端点是开区间），
        # 所有以 left 为左端点、右端点 >= right-1 的子串都合法
        ans += n - (right - 1)

        # 收缩左端点，准备考察下一个 left
        l_idx = ord(s[left]) - ord('a')
        if freq[l_idx] == k:                  # 之前恰好 k 次，离开窗口后 good 减 1
            good -= 1
        freq[l_idx] -= 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个字符最多进入窗口一次、离开一次。相比暴力的 `O(n²)`，速度提升了一个数量级。  
- **空间复杂度**：`O(1)` —— 只用大小为 26 的固定数组存字符计数。

---

## 心得

- **核心技巧**：**滑动窗口**（双指针）配合**计数表**，把“是否满足条件”转化为窗口内部的一个可维护状态 `good`。  
- **适用题型**  
  1. “子数组/子串满足某个频次条件”类（如 *Longest Substring with At Most K Distinct Characters*）。  
  2. “子数组/子串长度满足单调性条件”类（如 *Minimum Size Subarray Sum*）。  
- **一句话总结**：**找到每个左端点对应的最左合法右端点，后面的子串自然合法**。

## 反思

- **第一反应**：直接枚举所有子串检查，想到用哈希表统计字符频次。  
- **最容易踩的坑**  
  - 忘记 `right` 是**开区间**，导致计数时少加或多加一次。  
  - 当 `good` 变回 0 时，需要继续右移 `right`，否则会陷入死循环。  
  - `k == 1` 的特例必须单独处理，否则滑动窗口会在 `good` 为 0 前就提前停止。  
- **下次思路**：遇到“子串满足单调条件”时，第一步就想 **双指针**——固定左端点，右端点只增不减，利用单调性快速定位“第一个合法位置”。这样往往能把二次暴力降到线性。