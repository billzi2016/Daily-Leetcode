# #686. 重复字符串匹配 / Repeated String Match

> 难度：中等 · 标签：String、String Matching · [LeetCode 链接](https://leetcode.com/problems/repeated-string-match/)

---

## 题目（英文原版）

**Description**

Given two strings a and b, return the minimum number of times you should repeat string a so that string b is a substring of it. If it is impossible for b​​​​​​ to be a substring of a after repeating it, return -1.
Notice: string "abc" repeated 0 times is "", repeated 1 time is "abc" and repeated 2 times is "abcabc".

**Examples**

**Example 1:**

```
Input: a = "abcd", b = "cdabcdab"
Output: 3
Explanation: We return 3 because by repeating a three times "abcdabcdabcd", b is a substring of it.
```

**Example 2:**

```
Input: a = "a", b = "aa"
Output: 2
```

**Constraints**

- 1 <= a.length, b.length <= 104
- a and b consist of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `a` 和 `b`，返回最少需要将字符串 `a` 重复多少次，使得字符串 `b` 成为它的子串（substring）。如果无论重复多少次都不可能使 `b` 成为子串，返回 `-1`。

> 注意：字符串 `"abc"` 重复 0 次得到 `""`，重复 1 次得到 `"abc"`，重复 2 次得到 `"abcabc"`。

## 示例

### 示例 1
**输入**  
`a = "abcd", b = "cdabcdab"`

**输出**  
`3`

**解释**  
返回 `3`，因为将 `a` 重复三次得到 `"abcdabcdabcd"`，此时 `b` 是其子串（substring）。

### 示例 2
**输入**  
`a = "a", b = "aa"`

**输出**  
`2`

## 约束条件
- `1 <= a.length, b.length <= 10^4`
- `a` 和 `b` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串 `a` 一次一次地拼接起来**，每拼接一次就检查一次 `b` 是否已经出现在拼好的大字符串里。  
- **数据结构**：这里唯一需要的结构是一个普通的 Python `str`，它可以看作是一串字符的“珠子”。我们每次把 `a` 的珠子再往后面接上，就相当于把一个已经写好的句子再抄写一遍。  
- **为什么正确**：如果把 `a` 重复足够多次后 `b` 能成为它的子串，那么必然在我们一次一次追加的过程中出现过一次。只要我们不停地往后加，最终一定会覆盖所有可能的情况（只要不提前停下来）。  
- **时间/空间分析**：  
  - 每次拼接都需要把已有的字符串复制一遍，这在 Python 中的时间是 **O(当前长度)**。  
  - 为了判断 `b` 是否是子串，我们使用 `in` 运算符，最坏情况下也要遍历一次大字符串，时间是 **O(大字符串长度)**。  
  - 假设我们最多需要重复 `k` 次，那么大字符串的长度大约是 `k * len(a)`，所以总时间大概是 `1 + 2 + … + k`，即 **O(k² * len(a))**，这在最坏情况下会达到 **O(n²)**（把 `n` 看成 `len(b)` 的数量级）。  
  - 空间上我们只保存了一个正在增长的字符串，最大长度是 `k * len(a)`，即 **O(k * len(a))**。

> **大白话**：`O(n²)` 就好比你把 1 到 n 的所有数字都加一遍，花的时间会随 n 的增大而“平方”地增长，稍微大点儿就会慢得让人抓狂。

#### 代码（Python）

```python
def repeatedStringMatch_bruteforce(a: str, b: str) -> int:
    # 记录已经拼好的字符串，最开始是空串
    repeated = ""
    # 最多尝试 len(b) + 1 次（安全上界），防止无限循环
    for i in range(1, len(b) + 2):
        # 把 a 再接一次
        repeated += a               # 关键行：把 a 拼到已经得到的字符串后面
        # 检查 b 是否已经出现在拼好的字符串里
        if b in repeated:           # Python 的子串检查，等价于“在大串里找小串”
            return i                # 第 i 次拼接已经满足要求，返回次数
    # 循环结束仍未找到，说明不可能
    return -1
```

#### 复杂度

- **时间复杂度**：`O(k² * len(a))`，其中 `k` 是需要的最小重复次数。直观上相当于“平方级”增长，随着输入稍大就会变慢。  
- **空间复杂度**：`O(k * len(a))`，因为我们一直在保存完整的拼接结果。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的地方在于不停地把整个字符串复制、再检查**。我们可以利用以下两个观察来把工作量降到线性：

1. **只需要拼够一定长度就可以判断**  
   - 为了让 `b` 成为 `a` 的重复串的子串，`a` 至少要拼到长度 **不小于 `b` 的长度**。否则根本装不下 `b`。  
   - 但仅仅等于 `len(b)` 还不够，因为 `b` 可能跨越两次 `a` 的边界。想象 `a = "abcd"`，`b = "cdab"`，`b` 正好从第一次 `a` 的结尾跨到第二次 `a` 的开头。为了覆盖这种跨界情况，我们再多拼一次 `a`（即再加 `len(a)`），保证所有可能的“起始位置”都被囊括。  

2. **最多只需要检查 `len(b) // len(a) + 2` 次**  
   - `len(b) // len(a)` 表示把 `b` 完全放进多少个完整的 `a` 里。再多拼两次（一次够 `b` 完全覆盖，另一次处理跨界），就已经覆盖所有可能。  

基于这两个观察，算法可以写成：

- 计算 `repeat = ceil(len(b) / len(a))`（即最少需要的完整 `a` 次数）。  
- 构造 `candidate = a * repeat`，检查 `b` 是否在其中。  
- 若不在，再拼一次 `a`（`candidate += a`），再检查一次。  
- 若仍不在，说明无论再拼多少次都不可能出现 `b`，返回 `-1`。  

**核心数据结构**：仍然是字符串，只是我们一次性生成 **完整的候选串**，而不是每次都复制累加。这样 `in` 检查的时间是 **O(候选串长度)**，整体只遍历几次，达到了线性级别。

> **类比**：把 `a` 看成一块砖，`b` 是一幅画。我们只需要把砖铺到足够长（比画稍长一点），再看看画能否完整铺在砖上，而不是一次一次搬砖再搬砖。

#### 代码（Python）

```python
import math

def repeatedStringMatch(a: str, b: str) -> int:
    """
    返回最少的重复次数，使得 b 成为 a 重复后的子串。
    如果不可能则返回 -1。
    """
    # 需要的最少完整 a 的个数（向上取整）
    repeat = math.ceil(len(b) / len(a))   # 例如 len(b)=9, len(a)=4 => 3 次

    # 先尝试 repeat 次
    candidate = a * repeat                 # 把 a 拼 repeat 次，得到候选大串
    if b in candidate:                     # Python 的子串检查
        return repeat

    # 再尝试多拼一次，处理跨界的情况
    candidate += a                         # 再加一段 a
    if b in candidate:
        return repeat + 1

    # 两次都不行，说明无论再拼多少次都不可能出现 b
    return -1
```

#### 复杂度

- **时间复杂度**：`O(len(a) + len(b))`。我们只构造了最多 `repeat + 1` 次的 `a`，总长度不超过 `len(b) + 2 * len(a)`，检查子串的时间也和这个长度成正比。相比暴力的平方级，这里是**线性级**，输入变大时增长很慢。  
- **空间复杂度**：`O(len(a) + len(b))`。我们只保存了一个长度不超过 `len(b) + 2*len(a)` 的临时字符串，空间随输入线性增长。

---

## 心得

- **核心技巧**：**长度上界 + 一次性拼接 + 子串检查**。先算出最少需要多少个 `a`，再多拼一次覆盖跨界情况。  
- **适用的题型**：  
  1. “最少重复次数使得…成为子串” 类似题（如 *Repeated Substring Pattern*）。  
  2. 需要判断两个字符串的**循环匹配**或**周期**的题（如 *Find the Rotation*）。  
  3. 需要**最小覆盖**的字符串拼接问题（如 *Shortest Superstring* 的简化版）。  
- **一句话总结**：**先算够长，再只检查两次**，就能把暴力的“逐次拼接”省掉。

---

## 反思

- **第一反应**：把 `a` 一次一次地拼起来，循环检查 `b` 是否出现——这就是最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忘记考虑 `b` 跨越两个 `a` 的情况，只检查 `repeat` 次会漏掉答案。  
  - 对 `repeat` 的上界估计不足，导致在极端情况下返回 `-1` 虽其实有解。  
  - Python 中 `in` 检查是 **O(mn)**（m 为子串长度），但因为我们只检查两次，整体仍是线性。  
- **下次类似题的第一步**：**先算出长度上界**（把较短的字符串重复到不短于较长的），**再只检查一次或两次**，避免逐步累加的低效循环。