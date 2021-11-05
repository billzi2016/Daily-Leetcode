# #1540. K 次移动内能否将字符串转换 / Can Convert String in K Moves

> 难度：中等 · 标签：Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/can-convert-string-in-k-moves/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, your goal is to convert s into t in k moves or less.
During the ith (1 <= i <= k) move you can:
Shifting a character means replacing it by the next letter in the alphabet (wrapping around so that 'z' becomes 'a'). Shifting a character by i means applying the shift operations i times.
Remember that any index j can be picked at most once.
Return true if it's possible to convert s into t in no more than k moves, otherwise return false.

**Examples**

**Example 1:**

```
Input: s = "input", t = "ouput", k = 9
Output: true
Explanation: In the 6th move, we shift 'i' 6 times to get 'o'. And in the 7th move we shift 'n' to get 'u'.
```

**Example 2:**

```
Input: s = "abc", t = "bcd", k = 10
Output: false
Explanation: We need to shift each character in s one time to convert it into t. We can shift 'a' to 'b' during the 1st move. However, there is no way to shift the other characters in the remaining moves to obtain t from s.
```

**Example 3:**

```
Input: s = "aab", t = "bbb", k = 27
Output: true
Explanation: In the 1st move, we shift the first 'a' 1 time to get 'b'. In the 27th move, we shift the second 'a' 27 times to get 'b'.
```

**Constraints**

- 1 <= s.length, t.length <= 10^5
- 0 <= k <= 10^9
- s, t contain only lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，你的目标是将在 **k** 次移动（move）或更少的次数内将 `s` 转换成 `t`。  
在第 `i`（`1 <= i <= k`）次移动中，你可以：

- **移位（shifting）** 一个字符，即用字母表中的下一个字母替换它（循环后移，使得 `'z'` 变为 `'a'`）。将字符移位 `i` 次意味着对该字符执行 `i` 次移位操作。
- 注意，同一索引（index）`j` 最多只能被选取一次。

如果能够在不超过 **k** 次移动内完成转换，返回 `true`；否则返回 `false`。

## 示例

### 示例 1
**Input:** `s = "input", t = "ouput", k = 9`  
**Output:** `true`  
**Explanation:** 在第 6 次移动中，我们将字符 `'i'` 向后移位 6 次得到 `'o'`。在第 7 次移动中，我们将字符 `'n'` 向后移位得到 `'u'`。

### 示例 2
**Input:** `s = "abc", t = "bcd", k = 10`  
**Output:** `false`  
**Explanation:** 我们需要将 `s` 中的每个字符各移位一次才能得到 `t`。可以在第 1 次移动中将 `'a'` 移位到 `'b'`，但在剩余的移动次数中无法同时完成对 `'b'` 和 `'c'` 的移位，使得 `s` 转换为 `t`。

### 示例 3
**Input:** `s = "aab", t = "bbb", k = 27`  
**Output:** `true`  
**Explanation:** 在第 1 次移动中，我们将第一个 `'a'` 移位 1 次得到 `'b'`。在第 27 次移动中，我们将第二个 `'a'` 移位 27 次得到 `'b'`。

## 约束条件
- `1 <= s.length, t.length <= 10^5`
- `0 <= k <= 10^9`
- `s`、`t` 仅包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一次「第 i 步」都当成一次**可选的操作**，把它分配给还没有转换好的字符：

1. 先遍历所有下标 `j`，算出把 `s[j]` 变成 `t[j]` 需要向后移动多少次，记为 `diff`（`0~25`）。  
2. 从第 `1` 步到第 `k` 步，逐步检查这一步的 **移动次数 = i**（即第 `i` 步可以把字符往后移动 `i` 次）。  
3. 如果当前步 `i` 的 `i % 26` 正好等于某个还未完成的字符的 `diff`，就把这一步分配给它，标记该字符已经完成。  
4. 所有字符都完成 → `True`；遍历完 `k` 步仍有未完成的字符 → `False`。

> **类比**：把每一步想成一本《字母表》手册的页码，`i` 页对应的「向后移动次数」是 `i`。我们要把每个字符对应的「目标页码」`diff` 配到一本手册的某一页上，而同一本手册的同一页只能使用一次（每个下标只能被选一次）。

**为什么能得到正确答案**  
只要我们真的找到了一种把每一步唯一分配给需要的字符的方式，就满足题目「每个下标最多一次」且「步数不超过 k」的限制。相反，如果遍历完所有可能的步数后仍找不到合法分配，则说明不存在任何合法方案。

**时间/空间复杂度**  
- 对每一步 `i`（最多 `k` 步）都要在剩余字符里寻找匹配的 `diff`，最坏情况要遍历全部字符 `n`（`n = len(s)`）。因此时间复杂度是 **O(k·n)**，在 `k`、`n` 都可能达到 `10^5`~`10^9` 时根本跑不完。  
- 只需要保存原字符串、目标字符串以及一个标记数组，空间是 **O(n)**。

> **大白话**：  
> - `O(k·n)` 就好比「有 `k` 位老师，每位老师要检查 `n` 本作业」——老师多了，作业多了，工作量会爆炸。  
> - `O(n)` 的空间相当于「只需要把所有作业排好队」——这本身并不占太多桌子。

---

#### 代码（Python）

```python
def can_convert_bruteforce(s: str, t: str, k: int) -> bool:
    n = len(s)
    # 计算每个位置需要的移动次数（0~25）
    need = [(ord(t[i]) - ord(s[i])) % 26 for i in range(n)]
    used = [False] * n          # 记录该位置是否已经完成

    # 遍历每一步 i = 1 .. k
    for i in range(1, k + 1):
        shift = i % 26          # 第 i 步等价于向后移动 shift 次
        # 在所有未完成的位置中找一个恰好需要 shift 次的
        for idx in range(n):
            if not used[idx] and need[idx] == shift:
                used[idx] = True
                break           # 这一步已经被使用，去下一步

    # 所有位置都完成即为 True
    return all(used)
```

> **提示**：上述实现只用于说明思路，实际运行会在 `k`、`n` 较大时超时。

#### 复杂度

- **时间复杂度**：`O(k·n)` —— 每一步都要遍历全部字符。  
- **空间复杂度**：`O(n)` —— 需要存放 `need` 与 `used` 两个长度为 `n` 的数组。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**一次一次遍历**每一步 `i`，而实际上我们只关心每个字符需要的**余数** `diff = (t‑s) mod 26`。  
因为把字母向后移动 `x` 次和向后移动 `x + 26` 次的效果是完全一样的（字母表是环形的），所以第 `i` 步真正能帮助的字符，只取决于 `i % 26`。

**关键观察**  

| 步数 i | 实际作用等价于向后移动多少次 |
|-------|---------------------------|
| i = 1 | 1 次 (1 % 26 = 1) |
| i = 27| 1 次 (27 % 26 = 1) |
| i = 53| 1 次 (53 % 26 = 1) |
| …     | … |

同一种余数（比如 `1`）的步数会每隔 **26** 出现一次。  
如果我们有 **c** 个字符都需要 `diff = 1`，那么它们必须分别占用：

```
第 1 步  (1)
第 27 步 (1 + 26)
第 53 步 (1 + 2·26)
...
第 1 + (c-1)·26 步
```

所以对于每一个 `diff (1~25)`，只要 **最多的那一次需要的步数 ≤ k**，就一定能安排好所有字符。  

**实现步骤**  

1. 遍历字符串一次，统计每个 `diff` 出现的次数 `cnt[diff]`（使用字典或长度为 26 的数组）。  
2. 对每个出现的 `diff`，计算它们最远一次需要的步数  
   ```
   max_step = diff + 26 * (cnt[diff] - 1)
   ```
   - 第一次使用最小的步数 `diff`，第二次要加 `26`，依次类推。  
3. 如果任意 `max_step > k`，说明即使把所有可用的步数都用上，也仍然不够，返回 `False`。  
4. 否则所有字符都能安排在 `k` 步之内，返回 `True`。

**为什么是最优**  

- 我们没有枚举每一步，而是直接用数学公式算出**最坏情况**（即同余数出现最多时的最远一步）。  
- 如果最坏情况已经在 `k` 步以内，那么所有更早的步数自然都能满足。  
- 这一步骤只遍历一次字符串，时间 `O(n)`，空间只需要 26 个计数，`O(1)`。

#### 代码（Python）

```python
def canConvert(s: str, t: str, k: int) -> bool:
    """
    判断是否能在不超过 k 步的情况下把 s 转换为 t。
    思路：统计每个需要的余数 diff 的出现次数，
          检查 diff + 26 * (cnt-1) 是否 <= k。
    """
    from collections import defaultdict

    cnt = defaultdict(int)          # diff -> 出现次数

    # 1. 统计每个字符需要的移动次数（余数）
    for ch_s, ch_t in zip(s, t):
        diff = (ord(ch_t) - ord(ch_s)) % 26
        if diff:                     # diff == 0 表示已经相同，无需操作
            cnt[diff] += 1

    # 2. 对每种 diff 检查最远一步是否超出 k
    for diff, c in cnt.items():
        # 第一次用 diff，第二次用 diff+26，... 第 c 次用 diff+26*(c-1)
        max_step = diff + 26 * (c - 1)
        if max_step > k:             # 超出 k 步，无法安排
            return False

    return True
```

> **关键行中文注释**  
> - `diff = (ord(ch_t) - ord(ch_s)) % 26`  # 计算需要向后移动多少次（环形）  
> - `if diff:`  # 已经相同的字符不计数  
> - `max_step = diff + 26 * (c - 1)`  # 同余数出现 c 次时最远需要的步数  

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串，`n = len(s)`。  
  > 与暴力解的 `O(k·n)` 相比，省去了对每一步的循环，等价于「只请一次老师批改全部作业」。
- **空间复杂度**：`O(1)` —— 计数数组最多 26 个整数，常数级别的额外空间。  

---

## 心得  

- **核心技巧**：把「第 i 步可以移动 i 次」转化为「只关心 i 对 26 的余数」，利用**模运算的周期性**把问题压缩到 26 种情况。  
- **适用场景**：  
  1. 需要把若干操作分配到固定序号且每个序号只能使用一次的题目（如「按顺序使用不同的跳板」）。  
  2. 任何涉及 **循环周期**（如时钟、环形数组）且操作次数可以“叠加 26” 的情形。  
- **一句话总结**：**同余数决定唯一步数，出现次数决定最远步数，只要最远步数 ≤ k 即可**。

---

## 反思  

- **第一反应**：看到「第 i 步可以移动 i 次」立刻想到「枚举每一步」或「回溯」——这在规模大时会炸。  
- **最容易踩的坑**：  
  - 忽略 `diff == 0` 的情况（已经相同的字符不需要任何步数）。  
  - 没有考虑 **循环**：`i` 与 `i+26` 的效果相同，导致把步数算得太大。  
  - `k` 可能为 `0`，需要直接返回 `s == t`。  
- **下次遇到同类题**：第一步先**把操作的本质抽象为模数**（余数），统计每种余数的需求量，再用**等差数列**求出最远需要的编号，和 `k` 做比较。这样可以立刻得到 O(n) 的解法。