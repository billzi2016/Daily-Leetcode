# #3008. 在给定字符串中寻找美丽下标 II / Find Beautiful Indices in the Given Array II

> 难度：困难 · 标签：Two Pointers、String、Binary Search、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/find-beautiful-indices-in-the-given-array-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s, a string a, a string b, and an integer k.
An index i is beautiful if:
Return the array that contains beautiful indices in sorted order from smallest to largest.

**Examples**

**Example 1:**

```
Input: s = "isawsquirrelnearmysquirrelhouseohmy", a = "my", b = "squirrel", k = 15
Output: [16,33]
Explanation: There are 2 beautiful indices: [16,33].
- The index 16 is beautiful as s[16..17] == "my" and there exists an index 4 with s[4..11] == "squirrel" and |16 - 4| <= 15.
- The index 33 is beautiful as s[33..34] == "my" and there exists an index 18 with s[18..25] == "squirrel" and |33 - 18| <= 15.
Thus we return [16,33] as the result.
```

**Example 2:**

```
Input: s = "abcd", a = "a", b = "a", k = 4
Output: [0]
Explanation: There is 1 beautiful index: [0].
- The index 0 is beautiful as s[0..0] == "a" and there exists an index 0 with s[0..0] == "a" and |0 - 0| <= 4.
Thus we return [0] as the result.
```

**Constraints**

- 1 <= k <= s.length <= 5 * 105
- 1 <= a.length, b.length <= 5 * 105
- s, a, and b contain only lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的字符串 **s**（string）、字符串 **a**（string）、字符串 **b**（string）以及整数 **k**。  
如果满足以下全部条件，则下标 **i** 被称为**美丽下标**（beautiful）：

1. `s[i .. i + a.length - 1] == a`  
2. 存在一个下标 **j**，使得 `s[j .. j + b.length - 1] == b` 且 `|i - j| <= k`  

请返回所有美丽下标组成的数组，按从小到大排序后输出。

**示例 1**  
``` 
Input: s = "isawsquirrelnearmysquirrelhouseohmy", a = "my", b = "squirrel", k = 15
Output: [16,33]
Explanation: 有 2 个美丽下标：16 和 33。
- 下标 16 是美丽的，因为 `s[16..17] == "my"`，且存在下标 4 使得 `s[4..11] == "squirrel"`，并且 `|16 - 4| <= 15`。
- 下标 33 是美丽的，因为 `s[33..34] == "my"`，且存在下标 18 使得 `s[18..25] == "squirrel"`，并且 `|33 - 18| <= 15`。
因此返回 `[16,33]`。
```

**示例 2**  
``` 
Input: s = "abcd", a = "a", b = "a", k = 4
Output: [0]
Explanation: 只有 1 个美丽下标：0。
- 下标 0 是美丽的，因为 `s[0..0] == "a"`，且存在下标 0 使得 `s[0..0] == "a"`，并且 `|0 - 0| <= 4`。
因此返回 `[0]`。
```

**约束条件**  
- `1 <= k <= s.length <= 5 * 10^5`  
- `1 <= a.length, b.length <= 5 * 10^5`  
- `s、a、b` 只包含小写英文字母。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的下标都枚举一遍**：

1. 在字符串 `s` 中找到所有满足 `s[i..i+|a|-1] == a` 的下标 `i`（记为 `A`）。  
2. 同理找到所有满足 `s[j..j+|b|-1] == b` 的下标 `j`（记为 `B`）。  
3. 对于 `A` 中的每一个下标 `i`，遍历 `B` 中的每一个下标 `j`，检查 `|i - j| ≤ k` 是否成立，只要有一次成立，就把 `i` 加入答案。

> **类比**：把 `A` 看成“词典里要查的词”，把 `B` 看成“词典里已有的词”。我们把每个 `i` 当成要查的词，把所有 `j` 当成字典里的词，逐一比对，看是否在“可接受的距离 `k`”之内。

**为什么正确**：  
- 第一步保证了 `i` 真的是子串 `a` 的起始位置。  
- 第二步保证了 `j` 真的是子串 `b` 的起始位置。  
- 第三步直接检查题目要求的距离条件，只要满足就说明 `i` 是“beautiful”。  

**时间/空间分析（大白话）**：  

- 找 `A`、`B` 本身需要遍历 `s` 一次，时间是 `O(|s|)`。  
- 关键的 **双层循环**：对每个 `i ∈ A`，我们要遍历 **全部** `j ∈ B`，最坏情况下 `|A|` 与 `|B|` 都接近 `|s|`（比如 `a`、`b` 都是单字符 `'a'`，而 `s` 全是 `'a'`），于是比较次数是 `|A|·|B| ≈ |s|²`。  
- 因此**总时间复杂度**是 `O(|s|²)`，在最坏的 5·10⁵ 长度下根本跑不完。  
- 我们只需要保存两个下标列表，**空间**是 `O(|s|)`。

#### 代码（Python）

```python
def beautiful_indices_bruteforce(s: str, a: str, b: str, k: int):
    n = len(s)
    la, lb = len(a), len(b)

    # 1. 暴力找出所有 a 的起始位置
    A = []
    for i in range(n - la + 1):
        if s[i:i + la] == a:          # 子串匹配
            A.append(i)

    # 2. 暴力找出所有 b 的起始位置
    B = []
    for j in range(n - lb + 1):
        if s[j:j + lb] == b:
            B.append(j)

    # 3. 检查距离条件
    ans = []
    for i in A:                         # 对每个 a 的位置
        good = False
        for j in B:                     # 与每个 b 的位置比较
            if abs(i - j) <= k:        # 距离满足
                good = True
                break
        if good:
            ans.append(i)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(|s|²)`。  
  - 直观理解：如果 `s` 长度是 10⁵，`|s|²` 就是 10¹⁰ 次比较，远远超过电脑能在一秒钟里做的次数。  
- **空间复杂度**：`O(|s|)`，只保存两个下标列表。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于第 3 步的“双层遍历”。  
实际上，**我们只需要判断是否存在** 一个 `j` 落在区间 `[i - k, i + k]`，而不必把所有 `j` 都枚举。  

**优化的关键**：

1. **快速找出所有出现位置**  
   - 使用 **KMP**（Knuth-Morris-Pratt）或 **滚动哈希**（Rabin‑Karp）在 `O(|s|)` 时间内找出 `a`、`b` 的所有起始下标。这里直接用 Python 的切片比较（在最坏情况下仍是 `O(|s|)`），因为实现滚动哈希会更繁琐，但思路保持不变。  
2. **利用已排序的下标列表**（`A` 与 `B` 天然递增）  
   - 对每个 `i ∈ A`，我们只关心最近的 `b` 出现位置。可以用 **双指针** 或 **二分搜索**：  
     - 维护一个指针 `p`，指向 `B` 中第一个 **不小于** `i - k` 的位置。  
     - 只要 `p` 仍在 `B` 范围且 `B[p] ≤ i + k`，说明在允许距离内找到了 `b`，`i` 就是 beautiful。  
   - 因为 `i` 按升序遍历，指针 `p` 只会 **向右移动**，整个过程只遍历两次列表，时间是 `O(|A| + |B|) = O(|s|)`。

**为什么双指针能工作**：

- 想象 `A` 与 `B` 是两条平行的火车轨道，火车只会向前跑。  
- 当我们检查 `i` 时，只需要把 “左边界” 的火车（`B[p]`）推到不早于 `i - k` 的位置；如果这时这辆火车还没跑出 “右边界” `i + k`，说明它正好在两站之间，我们找到了匹配。  
- 由于 `i` 只增不减，左边界永远不会需要回头，这保证了线性时间。

#### 代码（Python）

```python
def beautiful_indices(s: str, a: str, b: str, k: int):
    n = len(s)
    la, lb = len(a), len(b)

    # ---------- 1. 找出所有 a 的起始位置 ----------
    A = []
    for i in range(n - la + 1):
        if s[i:i + la] == a:          # O(1) 切片比较，整体 O(n)
            A.append(i)

    # ---------- 2. 找出所有 b 的起始位置 ----------
    B = []
    for j in range(n - lb + 1):
        if s[j:j + lb] == b:
            B.append(j)

    # ---------- 3. 双指针检查距离 ----------
    ans = []
    p = 0               # B 的指针，指向第一个 >= i - k 的位置
    m = len(B)

    for i in A:                     # A 本身已经是升序
        # 把指针推到不早于左边界 i - k
        while p < m and B[p] < i - k:
            p += 1

        # 此时若指针仍在范围内且 B[p] ≤ i + k，说明找到了合法的 b
        if p < m and B[p] <= i + k:
            ans.append(i)

    return ans
```

> **代码要点注释**  
- `for i in range(n - la + 1)`: 只遍历能完整放下子串 `a` 的起始位置。  
- `while p < m and B[p] < i - k: p += 1`：**左边界**移动，确保 `B[p]` 不比 `i - k` 更左。  
- `if p < m and B[p] <= i + k:`：只要当前 `B[p]` 没超过 **右边界**，就满足 `|i - j| ≤ k`。  

#### 复杂度  

- **时间复杂度**：`O(|s|)`。  
  - 找 `A`、`B` 各一次遍历 `s`，共 `O(|s|)`。  
  - 双指针只向右移动，总共最多遍历 `B` 一遍，也是 `O(|s|)`。  
  - 与暴力的 `O(|s|²)` 相比，提升了 **数十万倍**，可以轻松跑完 5·10⁵ 长度的测试。  
- **空间复杂度**：`O(|s|)`（存放 `A`、`B` 两个列表），相较于输入规模是线性可接受的。  

---

## 心得  

- **核心技巧**：**利用已排序的出现位置列表，配合双指针/滑动窗口进行区间判定**。  
- **适用的题型**：  
  1. “在两个子串出现位置之间满足距离约束”的问题（如本题）。  
  2. “给定两类事件的时间戳，找出时间差 ≤ k 的配对”——常见于日志分析。  
  3. “区间覆盖”类题目，如“在数组中找出满足某种距离限制的最近值”。  
- **解题钥匙**：先**把原始字符串转化为离散的、排好序的“事件点”，再用**线性扫描**（双指针）完成区间匹配。

---

## 反思  

- **第一反应**：看到“子串 a、子串 b、距离 k”，本能想到枚举所有位置再比较——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记把 `a`、`b` 的出现位置全部记录，导致漏掉合法下标。  
  - 在双指针实现时，左边界的 `while` 循环写成 `<=`，会把本应保留的 `b` 位置错误地排除。  
  - 边界条件：当 `k` 大于等于 `s` 长度时，所有 `a` 的起始位置都应该被计入。  
- **下次类似题目**：第一步先**把所有满足子串匹配的下标收集成有序数组**，随后思考“是否只需要判断是否存在某个元素在区间 `[L, R]`”。若是，则立刻考虑**二分搜索**或**双指针**来实现线性或对数时间的区间查询。