# #3399. 相同字符的最小子串 II / Smallest Substring With Identical Characters II

> 难度：困难 · 标签：String、Binary Search · [LeetCode 链接](https://leetcode.com/problems/smallest-substring-with-identical-characters-ii/)

---

## 题目（英文原版）

**Description**

You are given a binary string s of length n and an integer numOps.
You are allowed to perform the following operation on s at most numOps times:
You need to minimize the length of the longest substring of s such that all the characters in the substring are identical.
Return the minimum length after the operations.

**Examples**

**Example 1:**

```
Input: s = "000001", numOps = 1
Output: 2
Explanation:
By changing s[2] to '1' , s becomes "001001" . The longest substrings with identical characters are s[0..1] and s[3..4] .
```

**Example 2:**

```
Input: s = "0000", numOps = 2
Output: 1
Explanation:
By changing s[0] and s[2] to '1' , s becomes "1010" .
```

**Example 3:**

```
Input: s = "0101", numOps = 0
Output: 1
```

**Constraints**

- 1 <= n == s.length <= 105
- s consists only of '0' and '1'.
- 0 <= numOps <= n

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为 `n` 的二进制字符串 `s`（binary string）和一个整数 `numOps`。  
你最多可以对 `s` 执行 `numOps` 次以下操作（operation）：

- 将任意位置的字符从 `'0'` 改为 `'1'`，或从 `'1'` 改为 `'0'`。

在完成至多 `numOps` 次操作后，需要**最小化** `s` 中**最长子串**（longest substring）使得该子串内的所有字符都相同（identical）。  
返回经过上述操作后能够得到的最小可能长度。

**示例**

**示例 1**  
```
Input: s = "000001", numOps = 1
Output: 2
Explanation:
通过将 s[2] 改为 '1'，字符串变为 "001001"。此时最长的相同字符子串是 s[0..1] 和 s[3..4]，长度均为 2。
```

**示例 2**  
```
Input: s = "0000", numOps = 2
Output: 1
Explanation:
将 s[0] 和 s[2] 均改为 '1'，得到 "1010"，此时最长相同字符子串的长度为 1。
```

**示例 3**  
```
Input: s = "0101", numOps = 0
Output: 1
```

**约束条件**
- `1 <= n == s.length <= 10^5`
- `s` 只包含字符 `'0'` 和 `'1'`
- `0 <= numOps <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有可能的翻转方案都枚举一遍**，然后在每一种方案下计算最长的同字符子串长度，取最小值。  

- **枚举翻转**：从字符串的 `n` 个位置中挑出至多 `numOps` 个位置，分别把 `'0'` 改成 `'1'` 或 `'1'` 改成 `'0'`。这相当于在「查字典」——我们把每个下标看成字典的“词”，把是否翻转看成“页码”。  
- **计算最长相同子串**：遍历一次字符串，记录当前连续相同字符的长度，取最大值即可。  

> 为什么这种方法能得到正确答案？  
> 因为我们把**所有**合法的翻转方式都尝试了一遍，答案一定出现在这些尝试中。只要遍历完整个搜索空间，最小的最长子串长度就一定被找到。

> 但是…  
> 这种做法的搜索空间是 `C(n,0)+C(n,1)+…+C(n,numOps)`，在最坏情况下接近 `2^n`，对 `n ≤ 10^5` 完全不可行。

#### 代码（Python）  

```python
from itertools import combinations
from math import inf

def brute_force(s: str, numOps: int) -> int:
    n = len(s)
    best = inf                     # 记录全局最小的最长子串长度

    # 枚举翻转的个数 0~numOps
    for k in range(numOps + 1):
        # 从 n 个位置中挑出 k 个进行翻转
        for idxs in combinations(range(n), k):
            lst = list(s)          # 把字符串变成可修改的列表
            for i in idxs:         # 执行翻转
                lst[i] = '1' if lst[i] == '0' else '0'
            # 计算翻转后最长相同子串的长度
            cur = 1
            longest = 1
            for i in range(1, n):
                if lst[i] == lst[i-1]:
                    cur += 1
                else:
                    longest = max(longest, cur)
                    cur = 1
            longest = max(longest, cur)
            best = min(best, longest)
    return best
```

> **注意**：这段代码只能在非常小的 `n`（比如 `n ≤ 10`）上跑得通，主要用于说明思路。

#### 复杂度  

- **时间复杂度**：`O( C(n,0)+C(n,1)+…+C(n,numOps) * n )`，在最坏情况下接近 `O(2^n * n)`，即指数级别，根本不可接受。  
- **空间复杂度**：`O(n)` 用来保存临时的字符列表。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈在于枚举所有翻转方式**。其实我们并不需要知道**哪**些位置被翻转，只需要知道**是否能在不超过 `numOps` 次翻转的前提下，把所有同字符子串的长度都控制在某个上限 `L`**。这正好可以用**二分搜索**来寻找答案的最小可能值。

**核心问题** → 给定一个上限 `L`，判断是否只用 ≤ `numOps` 次翻转，就能把原字符串中所有连续相同字符的块（我们称之为“跑”）的长度全部 ≤ `L`。  

下面一步步推导如何判断：

1. **把字符串拆成若干“跑”**  
   例如 `s = "00000111"` → `runs = [(0,5), (1,3)]`，其中每个元组是 `(字符, 长度)`。这相当于把一条长长的道路划分成若干段，每段的颜色相同。

2. **在一段长度为 `len` 的跑里，最多允许出现 `L` 个相同字符**。  
   为了实现这一点，我们可以在跑内部“插入”翻转，使得每段被切成若干小块，每块长度 ≤ `L`。  
   - 最理想的做法是每隔 `L+1` 个位置翻转一次（因为翻转后会产生一个不同字符，天然把前面的 `L` 个相同字符和后面的 `L` 个相同字符隔开）。  
   - 需要的最少翻转次数为  

\[
\text{need} = \left\lfloor\frac{\text{len} - 1}{L + 1}\right\rfloor
\]

   直观解释：如果跑的长度是 `len`，我们先保留前 `L` 个相同字符，然后必须在第 `L+1` 位翻转一次，接着再保留 `L`，如此循环。除去最后一段可能不足 `L` 的剩余，翻转的次数正好是上式。

3. **把所有跑需要的翻转次数加起来**，如果总和 ≤ `numOps`，说明上限 `L` 是可行的；否则不可行。

4. **二分搜索**  
   - `low = 0`（理论上可以把所有字符都翻成交替的，最长块长度为 1；但为了统一写法我们从 0 开始）  
   - `high = n`（最坏情况不做任何翻转，最长块长度等于原字符串的最长跑）  
   - 每次取中点 `mid = (low + high) // 2`，用上面的判断函数 `feasible(mid)` 检查可行性。  
   - 如果可行 → 说明答案可以更小，`high = mid`；否则 → 需要更大的上限，`low = mid + 1`。  
   - 循环结束时 `low`（或 `high`）即为**最小可能的最长同字符子串长度**。

**为什么二分能工作？**  
因为可行性随 `L` 的增大而**单调不下降**：如果某个 `L` 能做到，则任何更大的 `L` 也一定能做到（只需要少翻或不翻）。单调性正是二分搜索的前提。

#### 代码（Python）

```python
def smallest_substring_length(s: str, numOps: int) -> int:
    """
    返回在至多 numOps 次翻转后，最长同字符子串的最小可能长度。
    """
    n = len(s)

    # 1️⃣ 把字符串划分为连续相同字符的跑
    runs = []                       # 每个元素是该跑的长度
    cnt = 1
    for i in range(1, n):
        if s[i] == s[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1
    runs.append(cnt)                # 最后一段

    # 2️⃣ 判定函数：给定上限 L，是否只用 ≤ numOps 次翻转即可
    def feasible(L: int) -> bool:
        need = 0                     # 累计需要的翻转次数
        for length in runs:
            # 对每个跑，计算把它切成长度 ≤ L 的块至少要翻多少次
            # 公式来源于：把跑分成 (L+1) 大小的区间，最后一个区间不需要翻转
            need += (length - 1) // (L + 1)
            if need > numOps:       # 早停：已经超出上限
                return False
        return need <= numOps

    # 3️⃣ 二分搜索答案
    low, high = 0, n                # 搜索区间 [low, high]
    while low < high:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid               # 还能更小
        else:
            low = mid + 1            # 必须更大
    return low
```

**代码要点解释**  

| 行号 | 关键代码 | 中文注释 |
|------|----------|----------|
| 9‑15 | 把 `s` 拆成 `runs` 列表 | 把同字符连续出现的段落记下来，后面只需要看每段多长 |
| 20‑28| `feasible(L)` | 判断在最长块不超过 `L` 的前提下，需要的翻转次数是否 ≤ `numOps` |
| 23   | `(length - 1) // (L + 1)` | 计算单个跑需要的最少翻转次数，公式来源于“每 L+1 位必翻一次” |
| 31‑38| 二分搜索主循环 | 不断缩小搜索区间，`low` 最终就是答案 |

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 构造 `runs` 只需一次遍历 `O(n)`。  
  - 每次二分检查 `feasible` 需要遍历所有跑，最多 `O(n)`（因为跑的总长度等于 `n`）。  
  - 二分的迭代次数是 `log2(n)`，所以总体是 `O(n log n)`。  
  - 与暴力解相比，指数级的搜索被压缩到对数级别，完全可以跑满 `10^5` 的数据。

- **空间复杂度**：`O(n)`（最坏情况下每个字符都是单独的跑，需要存 `n` 个长度），额外的常数级别空间用于计数和二分变量。

---

## 心得  

- **核心技巧**：**二分答案 + 计算每段需要的最少翻转次数**。  
- **适用场景**：  
  1. “在至多 `k` 次操作后，使某个数值 ≤ X” 类型的题目（如 **“Maximum Frequency After K Increments”**）。  
  2. “把数组/字符串分割成若干块，每块满足上限，求最小上限” （如 **“Split Array Largest Sum”**、**“Minimum Size Subarray Sum”**）。  
- **一句话总结解题钥匙**：把“**能否做到**”转化为**单调判定函数**，再用**二分搜索**快速定位最小可行值。

---

## 反思  

- **第一反应**：直接想遍历所有翻转组合（暴力），因为题目描述看起来像“选哪几位翻最好”。  
- **最容易踩的坑**：  
  - 忽略了 **单调性**——没有证明可行性随 `L` 增大而不变，导致二分不成立。  
  - 计算每段所需翻转次数时写错公式（比如用了 `ceil(len / L)`），会导致多算或少算翻转次数，进而得到错误答案。  
  - 边界情况：`numOps = 0`（只能原样检查）和 `L = 0`（理论上不可能，但二分区间要包括 `0` 防止无限循环）。  
- **下次遇到同类题**：第一步立刻思考 **“能否用二分搜索答案？”**，然后 **构造单调的判定函数**（往往是累计所需的操作次数），再把细节归结为 **每个独立子结构的最小代价**。这样可以把指数级搜索直接压到 `O(n log n)`。