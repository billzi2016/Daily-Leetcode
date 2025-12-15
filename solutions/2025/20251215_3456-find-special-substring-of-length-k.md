# #3456. 寻找长度为 K 的特殊子串 / Find Special Substring of Length K

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/find-special-substring-of-length-k/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k.
Determine if there exists a substring of length exactly k in s that satisfies the following conditions:
Return true if such a substring exists. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: s = "aaabaaa", k = 3
Output: true
Explanation:
The substring s[4..6] == "aaa" satisfies the conditions.
```

**Example 2:**

```
Input: s = "abc", k = 2
Output: false
Explanation:
There is no substring of length 2 that consists of one distinct character and satisfies the conditions.
```

**Constraints**

- 1 <= k <= s.length <= 100
- s consists of lowercase English letters only.

---

## 题目（中文翻译）

你得到一个字符串 `s` 和一个整数 `k`。  
判断 `s` 中是否存在恰好长度为 `k` 的子串（substring），该子串满足题目所给的条件。  

如果存在满足条件的子串，返回 `true`；否则返回 `false`。  

### 示例

#### 示例 1  
**输入**: `s = "aaabaaa", k = 3`  
**输出**: `true`  
**解释**: 子串 `s[4..6] == "aaa"` 满足条件。  

#### 示例 2  
**输入**: `s = "abc", k = 2`  
**输出**: `false`  
**解释**: 不存在长度为 2 且仅由一种不同字符组成的子串满足条件。  

### 约束条件
- `1 <= k <= s.length <= 100`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有长度恰好为 k 的子串** 都枚举出来，逐个检查它们是不是“全由同一个字符组成”。  
- **枚举子串**：把字符串看成一排小盒子，每个盒子里放一个字符。我们可以把左指针 `i` 放在第 `0` 个盒子，然后让右指针 `j = i + k - 1` 指向第 `k` 个盒子，这样 `[i, j]` 就是一个长度为 `k` 的子串。把 `i` 从 `0` 移动到 `len(s)-k`，就能遍历所有可能的子串。  
- **检查是否相同**：把子串里的每个字符依次和第一个字符比较，只要出现不同的字符，就说明这段子串不满足要求。这里可以把字符对应的 **哈希表** 想象成一本“字典”，`key` 是字符，`value` 是出现次数。我们只需要检查字典里是否只有一种 `key`，但因为子串很短，用遍历更直观。  

这种做法一定能得到正确答案，因为我们把 **所有** 可能的子串都检查了一遍。

#### 代码（Python）

```python
def check_substring_brute(s: str, k: int) -> bool:
    n = len(s)
    # i 为子串的起始位置，最多只能到 n - k
    for i in range(n - k + 1):
        # 取出长度为 k 的子串
        sub = s[i:i + k]

        # 检查子串里的字符是否全相同
        first_char = sub[0]          # 取第一个字符作基准
        all_same = True              # 假设全部相同
        for ch in sub:               # 逐个比较
            if ch != first_char:     # 只要出现不同的字符
                all_same = False
                break                # 立刻停止检查这段子串
        if all_same:                 # 找到满足条件的子串
            return True
    # 所有子串都检查完，仍未找到
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - `n` 是字符串长度，外层循环要跑 `n‑k+1` 次，内层最多要比较 `k` 个字符。可以把 `O(n * k)` 想象成“每走一步都要检查 k 次”。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`i`, `sub`, `first_char`, `all_same`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的慢点在 **每次都要遍历整段子串**，这会导致 `k` 重复检查很多次。  
实际上，我们只关心 **相同字符的连续段**（也叫“跑”），如果某段连续相同字符的长度 ≥ k，那么必然可以在这段里取出一个长度为 k 的子串。于是我们可以一次遍历字符串，统计每个字符连续出现的次数，一旦计数达到 `k` 就可以立刻返回 `True`，不必再检查后面的字符。

**核心算法**：单次线性扫描 + 连续计数  
- 用一个变量 `cnt` 记录当前字符与前一个字符是否相同。如果相同，就把 `cnt` 加 1；否则把 `cnt` 重新置为 1（因为新字符自己算作长度 1 的连续段）。  
- 每次更新 `cnt` 后检查 `cnt >= k`，若成立说明找到了满足条件的子串。

**类比**：想象一列火车车厢，每节车厢都有颜色。我们站在列车前端，数数同颜色的车厢连续出现了多少节，只要连续出现的数量达到 `k`，就说明可以挑出 `k` 节相同颜色的车厢拼成子串。

#### 代码（Python）

```python
def check_substring_opt(s: str, k: int) -> bool:
    cnt = 0               # 当前连续相同字符的长度
    prev = ''             # 上一个字符，初始为空

    for ch in s:          # 依次遍历每个字符
        if ch == prev:    # 与前一个字符相同，连续段长度加一
            cnt += 1
        else:             # 不同，重新开始计数
            cnt = 1
            prev = ch      # 更新前一个字符

        if cnt >= k:      # 连续段已经够长，直接返回 True
            return True

    # 遍历完仍未找到长度 >= k 的连续段
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，`n` 次比较就结束。相比暴力的 `O(n*k)`，把“每走一步都要检查 k 次”压缩成“每走一步只检查一次”。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数/字符变量，和输入规模无关。

---

## 心得

- **核心技巧**：**连续计数（Run Length）**。只要把“相同字符连续出现的长度”记录下来，就能在 O(n) 时间内判断是否存在长度为 k 的全相同子串。  
- **适用的题型**  
  1. “判断字符串中是否有连续出现 ≥ k 次的字符”  
  2. “最长连续相同字符的长度” （LeetCode 1446）  
  3. “压缩字符串（Run‑Length Encoding）” 相关的题目  
- **一句话总结**：**把“所有子串”改成“所有连续段”，一次遍历即可得到答案。**

## 反思

- **第一反应**：直接把所有长度为 k 的子串枚举检查（暴力思路），因为这最容易写出来。  
- **最容易踩的坑**  
  - 忘记把 `k` 与 **连续段长度** 比较，而是错误地比较子串的 **不同字符数**。  
  - 边界条件：`k = 1` 时任何字符都满足，需要确保代码在 `cnt` 初始化为 1 时能直接返回 `True`。  
  - 当字符串全是不同字符且 `k > 1` 时，必须返回 `False`，不要因为循环结束后忘记返回默认值。  
- **下次类似题**：第一步先问自己 “这道题是否在找“连续出现” 的模式？” 如果答案是“是”，就立刻想到 **一次线性扫描 + 计数**，而不是先暴力枚举子串。