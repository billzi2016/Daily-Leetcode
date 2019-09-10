# #567. 字符串的排列 / Permutation in String

> 难度：中等 · 标签：Hash Table、Two Pointers、String、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/permutation-in-string/)

---

## 题目（英文原版）

**Description**

Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
In other words, return true if one of s1's permutations is the substring of s2.

**Examples**

**Example 1:**

```
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
Explanation: s2 contains one permutation of s1 ("ba").
```

**Example 2:**

```
Input: s1 = "ab", s2 = "eidboaoo"
Output: false
```

**Constraints**

- 1 <= s1.length, s2.length <= 104
- s1 and s2 consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s1` 和 `s2`，如果 `s2` 包含 `s1` 的一个排列（permutation），则返回 `true`，否则返回 `false`。换句话说，如果 `s1` 的某个排列是 `s2` 的子字符串（substring），则返回 `true`。

Example 1:
Example 2:
Constraints:

示例：
示例 1:
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
解释：s2 包含 s1 的一种排列（"ba"）。

示例 2:
Input: s1 = "ab", s2 = "eidboaoo"
Output: false

约束条件：
- 1 <= s1.length, s2.length <= 10^4
- s1 和 s2 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `s1` 的所有排列（即全排列）都列出来，然后在 `s2` 中逐个去找这些排列是否出现过。  
- **数据结构**：可以把每个排列当成一个字符串，存进列表（list）里。列表就像一本“所有可能的单词册”。  
- **正确性**：如果 `s2` 包含了 `s1` 的任意一个排列，那么一定能在这些列出的排列里找到对应的子串。  

但这里有两个致命问题：

1. `s1` 的长度记为 `m`，全排列的数量是 `m!`（阶乘），即使 `m=8`，`8! = 40320`，已经很大；`m=10` 时更是 3,628,800。遍历这么多排列显然不可行。  
2. 对每个排列我们都要在 `s2`（长度记为 `n`）里做一次子串匹配，时间复杂度会是 `O(m! * n)`，会导致 **超时（TLE）**。

#### 代码（Python）

```python
import itertools

def checkInclusion_brute(s1: str, s2: str) -> bool:
    """暴力法：枚举 s1 的全部排列，然后在 s2 中逐个匹配"""
    m, n = len(s1), len(s2)
    if m > n:
        return False

    # 1. 生成所有排列，排列本身是一个 tuple，需要转成字符串
    perms = {''.join(p) for p in itertools.permutations(s1)}   # 用集合去重

    # 2. 在 s2 中滑动窗口，长度为 m，逐个比较是否在 perms 中
    for i in range(n - m + 1):
        sub = s2[i:i + m]                # 当前窗口子串
        if sub in perms:                 # “字典”里找到了
            return True
    return False
```

> **注**：上述代码在概念上是正确的，但在实际测试中会因为 `permutations` 的指数级爆炸而 **超时**。

#### 复杂度  

- **时间复杂度**：`O(m! * n)`  
  - `m!` 是生成所有排列的代价，`n` 是在 `s2` 上滑动窗口的次数。  
  - 用大白话说，就是“先把所有可能的拼图块全部做出来（很多很多），再一个一个去看 `s2` 能不能放进去”。  
- **空间复杂度**：`O(m!)`  
  - 需要把所有排列存进集合，最坏情况下需要 `m!` 个字符串。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **瓶颈** 在于：

1. **枚举所有排列**（指数级）  
2. **每次都完整比较子串**（线性）  

我们要想办法 **一次遍历** 就能判断窗口内的字符组成是否和 `s1` 相同。关键观察：

- 两个字符串是排列关系，当且仅当它们的 **字符出现次数完全相同**。  
- 只涉及小写英文字母（26 个），可以用一个长度为 26 的整数数组来统计每个字符出现的次数，这相当于 “字典”，但更轻量。  
- 当我们在 `s2` 上使用 **滑动窗口**（窗口大小固定为 `len(s1)`）时，只会有两种字符的计数发生变化：**窗口右移时加入的字符** 和 **窗口左移时移出的字符**。所以我们可以 **增量更新** 计数数组，而不必每次重新统计整个窗口。

基于此，整体思路如下：

1. 先统计 `s1` 中每个字符的出现次数，记为 `need[26]`。  
2. 在 `s2` 上维护一个同样大小的计数数组 `window[26]`，它记录当前窗口（长度为 `len(s1)`）中字符的出现次数。  
3. 使用 **两个指针** `left`、`right` 表示窗口左右边界，初始都指向 0。  
4. 每次把 `right` 向右移动一步，把对应字符计数加入 `window`。  
5. 当窗口长度等于 `len(s1)` 时，比较 `window` 与 `need` 是否完全相同：  
   - 完全相同 → 找到一个排列，直接返回 `True`。  
   - 不同 → 把 `left` 向右移动一步，把左侧字符的计数从 `window` 中减掉，窗口长度仍保持 `len(s1)`。  
6. 循环结束仍未匹配，则返回 `False`。

**为什么只比较一次完整数组就能判断？**  
因为字符种类只有 26 种，两个长度相同的数组如果每个位置的计数都相等，说明两段字符串的字符频率一模一样，必然是彼此的排列。

#### 代码（Python）

```python
def checkInclusion(s1: str, s2: str) -> bool:
    """滑动窗口 + 计数数组（哈希表）"""
    m, n = len(s1), len(s2)
    if m > n:                     # s1 长度比 s2 长，必不可能
        return False

    # 1. 统计 s1 中每个字符的出现次数，数组下标 0~25 对应 'a'~'z'
    need = [0] * 26
    for ch in s1:
        need[ord(ch) - ord('a')] += 1

    # 2. 窗口计数数组，初始全 0
    window = [0] * 26
    left = 0                      # 窗口左边界

    # 3. 右指针遍历 s2
    for right in range(n):
        idx = ord(s2[right]) - ord('a')
        window[idx] += 1          # 把新字符加入窗口计数

        # 当窗口长度超过 m 时，左侧字符要移出窗口
        if right - left + 1 > m:
            left_idx = ord(s2[left]) - ord('a')
            window[left_idx] -= 1
            left += 1             # 收缩左边界

        # 此时窗口长度恰好等于 m，检查是否匹配
        if right - left + 1 == m and window == need:
            return True

    return False
```

> **关键行中文注释** 已经写在代码里，帮助初学者快速对应每一步的意义。

#### 复杂度  

- **时间复杂度**：`O(n)`（线性）  
  - 只遍历了一遍 `s2`（长度为 `n`），每一步的操作都是 **O(1)**（数组下标直接访问），没有嵌套循环。  
  - 与暴力解的 `O(m! * n)` 相比，几乎是 **天壤之别**，在最坏情况下也只需要几万次操作（`n ≤ 10^4`）。

- **空间复杂度**：`O(1)`（常数）  
  - 我们只用了两个长度为 26 的整数数组和几个指针，和输入大小无关。  
  - 用“大白话”说，就是“只需要一个装 26 支笔的盒子”，不管字符串有多长，都不需要额外的空间。

---

## 心得

- **核心技巧**：利用字符出现次数（频率）相同的特性，用 **计数数组**（哈希表）配合 **固定长度滑动窗口** 完成 O(n) 检查。  
- **适用的题型**  
  1. **找子串的排列**（本题）  
  2. **最小覆盖子串**（LeetCode 76）——同样是窗口 + 计数，只是窗口大小不固定。  
  3. **长度相同的字母异位词子串计数**（LeetCode 438）——统计所有满足条件的窗口。  
- **一句话总结解题钥匙**：*“只要两个字符串的字符频率相同，它们就是排列；用 26 长的计数数组在滑动窗口里增删字符，即可线性判定”。*

---

## 反思

- **第一反应**：看到“排列”，立刻想到全排列或排序后比较，结果很快意识到会超时。  
- **最容易踩的坑**  
  - **窗口大小错误**：忘记在窗口长度大于 `len(s1)` 时及时移除左侧字符，会导致计数不匹配。  
  - **字符映射错误**：`ord(ch) - ord('a')` 必须对应 0~25，若误用了 `- 'A'` 会导致数组越界。  
  - **比较方式**：直接比较两个列表 `window == need`，在 Python 中是 O(26) 的常数时间，别用 `for` 循环逐个比较，容易写出低效代码。  
- **下次遇到同类题**：第一步就思考“两个字符串是否有相同的字符频率”，并尝试用 **计数哈希表 + 滑动窗口** 来做增量维护，而不是枚举或排序。这样往往能直接把时间复杂度压到线性。