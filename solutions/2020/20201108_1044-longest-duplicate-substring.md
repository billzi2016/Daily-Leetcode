# #1044. 最长重复子串 / Longest Duplicate Substring

> 难度：困难 · 标签：String、Binary Search、Sliding Window、Rolling Hash、Suffix Array、Hash Function · [LeetCode 链接](https://leetcode.com/problems/longest-duplicate-substring/)

---

## 题目（英文原版）

**Description**

Given a string s, consider all duplicated substrings: (contiguous) substrings of s that occur 2 or more times. The occurrences may overlap.
Return any duplicated substring that has the longest possible length. If s does not have a duplicated substring, the answer is "".

**Examples**

**Example 1:**

```
Input: s = "banana"
Output: "ana"
```

**Example 2:**

```
Input: s = "abcd"
Output: ""
```

**Constraints**

- 2 <= s.length <= 3 * 104
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，考虑所有 **重复子串**（substring）：在 `s` 中出现 **2 次或更多** 的（连续）子串。不同出现的位置可以重叠。

返回任意一个 **长度最长** 的重复子串。如果 `s` 没有重复子串，则返回空字符串 `""`。

**示例 1**  
**输入**: `s = "banana"`  
**输出**: `"ana"`

**示例 2**  
**输入**: `s = "abcd"`  
**输出**: `""`

**约束条件**

- `2 <= s.length <= 3 * 10^4`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把字符串 `s` 的所有可能子串都枚举出来，放进一个集合（相当于“字典”），每次往集合里插入时检查它是否已经出现过。  
- **集合（Set）** 可以类比成我们平时查字典的过程：给定一个单词（子串），如果字典里已经有这页（已经出现），就说明找到了重复的子串。  
- 我们只关心最长的重复子串，所以在遍历的过程中，记录下每次发现的重复子串的长度，如果更长就更新答案。

这种方法一定能得到正确答案，因为它穷举了所有可能的子串，哪怕是重叠的也会被检查到。

#### 代码（Python）

```python
def longestDupSubstring_bruteforce(s: str) -> str:
    n = len(s)
    best = ""                     # 当前找到的最长重复子串
    # 长度从大到小枚举，这样一旦找到就可以直接返回（可选优化）
    for length in range(n - 1, 0, -1):
        seen = set()              # 用集合存已经出现过的子串
        for i in range(n - length + 1):
            sub = s[i:i + length]   # 取出长度为 length 的子串
            if sub in seen:         # 已经出现过，说明找到了重复子串
                return sub          # 因为是从大到小枚举，直接返回就是最长的
            seen.add(sub)
    return ""                     # 没有重复子串
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层遍历子串长度（最多 `n` 次），内层遍历起始位置（平均也接近 `n` 次），所以大约是 `n × n`。  
  用大白话说，如果字符串长度是 10,000，程序大概要跑 100,000,000 次比较，明显太慢。

- **空间复杂度**：`O(n²)`（最坏情况下集合里会存 `≈ n²/2` 个子串）  
  解释：我们把所有子串都放进集合，子串本身占用的空间与它们的总长度成正比。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有子串**，导致时间和空间都呈二次增长。  
我们可以把“是否存在长度为 K 的重复子串”这个子问题抽出来，用**二分搜索**来决定答案的长度范围，然后在每一次二分判断中，用**滚动哈希（Rabin‑Karp）**在 `O(n)` 时间内快速检测是否有重复子串。

**关键步骤拆解**：

1. **二分搜索长度**  
   - 如果存在长度为 `10` 的重复子串，那么一定也存在长度为 `9、8 … 1` 的重复子串（把它截短就仍然是重复的）。  
   - 因此答案长度呈单调递增特性，适合二分。我们在 `[1, n‑1]` 区间搜索最长可行的 `K`。

2. **滚动哈希检查 K 长度是否可行**  
   - 把每个字符映射成整数（`a→0, b→1 …`），选取一个 **基数** `base`（常取 26 或 31）和一个 **大质数** `mod`（防止哈希值爆炸），计算子串的哈希值。  
   - **哈希** 可以类比成把一个长单词压缩成一个短的指纹：相同的指纹大概率对应相同的单词。  
   - 使用**滑动窗口**：已知窗口左端的哈希 `hash(i)`，要得到右移一位后的窗口 `hash(i+1)`，只需要  
     ```
     hash(i+1) = (hash(i) - left_char * base^(K-1)) * base + new_char   (mod mod)
     ```  
     这样每次只做常数次运算，整个检查过程是 `O(n)`。

3. **碰撞处理**  
   - 由于哈希是取模的，极少数不同子串会得到相同的哈希（称为碰撞）。  
   - 为了安全，我们可以使用 **双模**（两个不同的质数）或者在哈希相等时再把真实子串做一次比较。这里演示双模。

4. **返回答案**  
   - 二分结束后，`low`（或 `high`）指向最长可行的长度。我们再次用滚动哈希把对应的子串取出来返回。

#### 代码（Python）

```python
def longestDupSubstring(s: str) -> str:
    """
    二分长度 + 双模 Rabin‑Karp
    """
    n = len(s)
    nums = [ord(c) - ord('a') for c in s]          # 把字符映射成 0~25 的整数

    MOD1 = 2**61 - 1          # 取一个非常大的质数，防止溢出
    MOD2 = 2**61 - 1 - 1      # 另一个大质数（这里仅示意，实际可以选其他质数）
    BASE = 256                # 基数取 256（ASCII 范围），也可以取 26、31 等

    # 预计算 base^K % MOD，供滚动哈希使用
    def pre_pow(k, mod):
        p = 1
        for _ in range(k):
            p = (p * BASE) % mod
        return p

    # 检查是否存在长度为 K 的重复子串，若存在返回其中一个子串，否则返回空串
    def check(K):
        if K == 0:
            return ""
        h1 = h2 = 0
        base_k1 = pre_pow(K, MOD1)
        base_k2 = pre_pow(K, MOD2)

        seen = dict()   # key: (hash1, hash2) -> 起始下标列表（只存第一个即可）
        # 先算出第一个窗口的哈希
        for i in range(K):
            h1 = (h1 * BASE + nums[i]) % MOD1
            h2 = (h2 * BASE + nums[i]) % MOD2
        seen[(h1, h2)] = 0

        for start in range(1, n - K + 1):
            # 滑动窗口：移除左侧字符，加入右侧字符
            left = nums[start - 1]
            right = nums[start + K - 1]

            h1 = (h1 * BASE - left * base_k1 + right) % MOD1
            h2 = (h2 * BASE - left * base_k2 + right) % MOD2

            key = (h1, h2)
            if key in seen:
                # 为防止极端碰撞，再做一次真实子串比较
                prev = seen[key]
                if s[prev:prev + K] == s[start:start + K]:
                    return s[start:start + K]
            else:
                seen[key] = start
        return ""

    # 二分搜索最长可行的长度
    low, high = 1, n - 1
    ans = ""
    while low <= high:
        mid = (low + high) // 2
        candidate = check(mid)
        if candidate:               # 存在长度为 mid 的重复子串
            ans = candidate         # 更新答案
            low = mid + 1           # 尝试更长的
        else:
            high = mid - 1          # 必须缩短
    return ans
```

> **代码说明**（关键行中文注释已在代码中）  
> - `nums` 把字符转成数字，方便后续算哈希。  
> - `pre_pow` 预先算 `BASE^K % MOD`，因为滚动时要把最左边的字符贡献去掉。  
> - `seen` 用字典保存已经出现过的哈希对，键是 `(hash1, hash2)`，值是该子串的起始下标。  
> - `check` 函数返回任意一个长度为 `K` 的重复子串（若有），否则返回空串。  
> - 二分循环里 `mid` 代表当前尝试的长度，若 `check(mid)` 成功则说明答案长度至少是 `mid`，继续向右搜；否则向左搜。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 二分搜索需要 `log n` 次检查。  
  - 每一次检查 `check(K)` 只遍历一次字符串，使用滚动哈希，时间是 `O(n)`。  
  - 整体就是 `O(n) * O(log n)`。  
  - 与暴力的 `O(n²)` 相比，速度提升了数量级（例如 `n=30,000` 时，大约只要几百万次运算）。

- **空间复杂度**：`O(n)`  
  - `seen` 最多存储所有窗口的哈希值，数量与 `n` 成线性关系。  
  - 其他辅助变量都是常数空间。  

---

## 心得

- **核心技巧**：二分搜索 + 滚动哈希（Rabin‑Karp）  
  这两个思路组合在一起，能够把“是否存在长度为 K 的重复子串”从 `O(n²)` 降到 `O(n)`，再配合二分把整体复杂度压到 `O(n log n)`。

- **适用的题型**  
  1. **最长重复子串**（本题）  
  2. **最长公共子串**（两个字符串的最长公共子串）  
  3. **判断是否有长度为 K 的相同子数组**（数组版的相同思路）

- **一句话总结**：  
  *把“大问题”拆成“给定长度是否可行”，用二分定位，用滚动哈希快速判定。*

---

## 反思

- **第一反应**：直接枚举所有子串，检查出现次数。  
  这在思路上最自然，却忽视了输入规模（`3·10⁴`）会导致超时。

- **最容易踩的坑**  
  1. **哈希碰撞**：单一模数可能出现不同子串哈希相同的情况，需要双模或二次验证。  
  2. **滑动窗口的模运算**：负数取模会导致错误，建议在减法后加上模数再取模。  
  3. **边界条件**：字符串长度为 1 或没有任何重复子串时，需要返回空串 `""`。

- **下次遇到同类题的第一步**：  
  先判断“是否存在某个长度的解”这类**判定子问题**，并思考是否可以用**哈希/前缀和**等线性判定方法，再用**二分**把答案长度逼近。这样可以把很多看似“暴力”的搜索题，转化为 `O(n log n)` 的高效解。