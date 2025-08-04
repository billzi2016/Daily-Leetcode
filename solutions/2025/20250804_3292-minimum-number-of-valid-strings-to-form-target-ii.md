# #3292. **形成目标字符串的最少有效字符串数量 II** / Minimum Number of Valid Strings to Form Target II

> 难度：困难 · 标签：Array、String、Binary Search、Dynamic Programming、Segment Tree、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words and a string target.
A string x is called valid if x is a prefix of any string in words.
Return the minimum number of valid strings that can be concatenated to form target. If it is not possible to form target, return -1.

**Examples**

**Example 1:**

```
Input: words = ["abc","aaaaa","bcdef"], target = "aabcdabc"
Output: 3
Explanation:
The target string can be formed by concatenating:
```

**Example 2:**

```
Input: words = ["abababab","ab"], target = "ababaababa"
Output: 2
Explanation:
The target string can be formed by concatenating:
```

**Example 3:**

```
Input: words = ["abcdef"], target = "xyz"
Output: -1
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 5 * 104
- The input is generated such that sum(words[i].length) <= 105.
- words[i] consists only of lowercase English letters.
- 1 <= target.length <= 5 * 104
- target consists only of lowercase English letters.

---

## 题目（中文翻译）

你得到一个字符串数组 `words` 和一个目标字符串 `target`。  
如果字符串 `x` 是 `words` 中任意一个字符串的前缀（prefix），则称 `x` 为**有效字符串**（valid string）。  
返回可以拼接成 `target` 的最少有效字符串数量。如果无法拼接出 `target`，返回 `-1`。

---

### 示例

**示例 1**  
```
Input: words = ["abc","aaaaa","bcdef"], target = "aabcdabc"
Output: 3
Explanation:
可以通过拼接以下有效字符串得到目标字符串：
```

**示例 2**  
```
Input: words = ["abababab","ab"], target = "ababaababa"
Output: 2
Explanation:
可以通过拼接以下有效字符串得到目标字符串：
```

**示例 3**  
```
Input: words = ["abcdef"], target = "xyz"
Output: -1
```

---

### 约束

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 5 * 10^4`
- 输入满足 `sum(words[i].length) <= 10^5`
- `words[i]` 仅由小写英文字母组成
- `1 <= target.length <= 5 * 10^4`
- `target` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从左到右依次尝试所有可能的合法前缀**，把它们拼起来，看能否恰好得到 `target`，并记录使用的段数最少是多少。  

- **合法前缀**：只要它是 `words` 中任意一个单词的前缀即可。可以把所有单词的所有前缀都列举出来，放进一个集合（`set`）里。  
  - 把集合想象成一本**词典**：词典里记的每一条都是“合法前缀”。查找一个子串是否在词典里，就像在字典里查词一样，只要 `O(1)`（哈希表的查找）就能得到答案。  

- **暴力拼接**：对 `target` 的每一个位置 `i`，尝试把从 `i` 开始的每一种长度 `len`（只要 `i+len` 不越界）都检查一下，看 `target[i:i+len]` 是否在合法前缀集合里。  
  - 如果在，就把它当作一个“块”，继续往后拼接。  
  - 用递归或遍历把所有可能的拼法全部列举出来，最后挑出块数最少的那一种。

> 为什么这个方法一定能得到正确答案？因为我们把 **所有** 合法前缀都考虑进来了，遍历 **所有** 可能的拼接顺序，自然不会遗漏最优解。  

#### 代码（Python）

```python
from typing import List

def minValidStrings_bruteforce(words: List[str], target: str) -> int:
    # 1️⃣ 把所有合法前缀放进哈希集合（相当于查字典）
    valid_prefixes = set()
    for w in words:
        for l in range(1, len(w) + 1):          # 前缀长度从 1 到整词
            valid_prefixes.add(w[:l])           # 把前缀加入集合

    n = len(target)
    # dp[i] 表示拼出 target 前 i 个字符最少需要多少块，初始设为无限大
    INF = n + 1
    dp = [INF] * (n + 1)
    dp[0] = 0                                   # 空串需要 0 块

    # 2️⃣ 暴力尝试每一个起点 i
    for i in range(n):
        if dp[i] == INF:        # 前 i 个字符根本不可达，直接跳过
            continue
        # 从 i 开始尝试所有可能的长度
        for j in range(i + 1, n + 1):
            sub = target[i:j]               # 子串 target[i:j]
            if sub in valid_prefixes:       # ✅ 是合法前缀
                dp[j] = min(dp[j], dp[i] + 1)   # 更新到达位置 j 的最小块数

    return -1 if dp[n] == INF else dp[n]
```

#### 复杂度  

- **时间复杂度**：  
  - 生成合法前缀集合需要遍历所有单词的每个字符，最多 `Σ|words[i]| ≤ 10⁵`，即 `O(10⁵)`。  
  - 主循环里，两层嵌套遍历 `i`、`j`，最坏情况是 `target` 长度 `m = 5·10⁴`，会检查 `O(m²)`（约 2.5×10⁹）次子串，远远超出时间限制。  
  - 用大白话说，`O(m²)` 就像在一条 5 万米的马拉松跑道上，每跑一步都要回头检查前面所有已经跑过的路段，根本跑不完。

- **空间复杂度**：  
  - 合法前缀集合最多存 `10⁵` 条字符串，`O(10⁵)`。  
  - `dp` 数组长度为 `m+1`，也是 `O(m)`。  
  - 总体 `O(10⁵ + m)`，在本题数据范围内是可以接受的。

> 结论：虽然思路很直观，但由于二次遍历导致的 **时间爆炸**，在真实测评中会 TLE（超时）。我们需要把“找最长合法子串”的步骤加速——这就是最优解的出发点。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每个起点 `i` 都要逐个尝试所有可能的结束位置 `j`，检查子串是否是合法前缀。  
如果我们能 **快速得到**：从位置 `i` 开始，**最长** 的合法前缀到底有多长，就能一次性把 `dp[i]` 的信息向后传播，而不必逐个枚举。  

实现这个目标需要三件工具：

1. **前缀哈希（Rabin‑Karp）**  
   - 把每个字符串看成一个 **大整数的“指纹”**（哈希值），相同的子串一定会得到相同的指纹。  
   - 用滚动哈希可以在 `O(1)` 时间内得到任意区间 `[l, r)` 的哈希值，前提是我们预先算好幂次和前缀哈希数组。  
   - 类比：把一本书的每一页都贴上唯一的二维码，想要知道第 `i` 到第 `j` 页的内容是否在词典里，只要扫描这几页的二维码就行了。

2. **二分查找**  
   - 对于固定的起点 `i`，合法前缀的长度是 **单调递增** 的（如果长度 `len` 合法，所有更短的长度自然也合法，因为它们是更短的前缀）。  
   - 因此我们可以在 `[i, n]` 区间上二分，快速定位最长合法长度 `L`，只需要 `O(log n)` 次哈希查询。

3. **线段树（或「懒更新」的数组）**  
   - 当我们知道 `dp[i]`（拼出前 `i` 个字符的最少块数）以及从 `i` 出发的最长合法长度 `L` 时，**所有** 区间 `i+1 … i+L` 的 `dp` 值都可以尝试用 `dp[i] + 1` 来更新。  
   - 为了在 `O(log n)` 时间内完成「区间取最小」的更新，我们使用 **线段树**（每个节点维护该区间的最小值）。  
   - 对于初学者，也可以把线段树想象成“一棵能快速把一段路上的收费站费用改成最小值的树”。  

下面一步步把这些工具组合起来：

1. **准备哈希集合**  
   - 对每个单词的每个前缀计算哈希值，放进 `HashSet`。  
   - 这里不存字符串本身，只存哈希值，省空间且比较快。

2. **预处理目标串的滚动哈希**  
   - 选定一个大质数模 `MOD`（如 `10⁹+7`）和一个基数 `BASE`（如 `91138233`），计算 `pref[i]`（前 i 个字符的哈希）和 `pow[i]`（BASEⁱ % MOD）。

3. **DP + 线段树**  
   - `dp[0] = 0`，其余初始化为正无穷。  
   - 用线段树把 `dp` 存起来，支持两类操作：  
     * **查询单点**：得到当前 `dp[i]` 的最小值（即 `tree.query(i,i)`）。  
     * **区间最小更新**：把 `dp[i]+1` 这个值写入区间 `[i+1, i+L]`（`tree.range_update(l, r, value)`），如果已有更小的值则保持不变。  

4. **遍历每个起点**  
   - 用线段树查询 `dp[i]`。如果 `dp[i]` 仍是无穷大，说明前 `i` 个字符根本不可达，直接跳过。  
   - 对 `i` 进行二分：  
     * 设 `lo = i+1, hi = n`。  
     * 中点 `mid` 对应子串 `target[i:mid]`，用滚动哈希得到它的哈希值 `h`，检查 `h` 是否在合法前缀集合里。  
     * 若在，说明长度 `mid-i` 合法，尝试更长；否则收缩区间。  
   - 二分结束后得到最长合法长度 `L = best - i`（`best` 为二分得到的最右合法右端点）。  
   - 用线段树把 `dp[i]+1` 更新到区间 `[i+1, i+L]`。  

5. **答案**  
   - 最后 `dp[n]`（即 `tree.query(n,n)`）即为目标串的最小块数；若仍是无穷大则返回 `-1`。

> **核心技巧**：  
> - **滚动哈希** 把“子串相等判断”从 `O(len)` 降到 `O(1)`。  
> - **二分** 把“寻找最长合法子串”从 `O(len)` 降到 `O(log n)`。  
> - **线段树** 把“区间最小更新”从 `O(len)` 降到 `O(log n)`。  
> 综合起来，整体复杂度从 `O(n²)` 降到 `O(n log n)`，能够轻松通过 5·10⁴ 规模的测试。

#### 代码（Python）

```python
from typing import List

MOD = 10 ** 9 + 7          # 大质数取模，防止哈希冲突
BASE = 91138233            # 随机选的基数，越大冲突概率越低

class SegTree:
    """支持区间最小赋值的线段树（懒标记）"""
    def __init__(self, n: int):
        self.N = 1
        while self.N < n:          # 把大小扩展到最近的 2 的幂
            self.N <<= 1
        self.inf = 10 ** 9
        self.data = [self.inf] * (2 * self.N)   # 维护最小值
        self.lazy = [self.inf] * (2 * self.N)   # 懒标记：待更新的最小值

    def _push(self, node: int):
        """把懒标记向下传递"""
        if self.lazy[node] != self.inf:
            for child in (node << 1, node << 1 | 1):
                # 子节点取最小的懒标记
                self.lazy[child] = min(self.lazy[child], self.lazy[node])
                self.data[child] = min(self.data[child], self.lazy[node])
            self.lazy[node] = self.inf

    def range_update(self, l: int, r: int, val: int):
        """把区间 [l, r]（左闭右闭）里的最小值尝试设为 val"""
        self._range_update(l, r, val, 1, 0, self.N - 1)

    def _range_update(self, l, r, val, node, nl, nr):
        if r < nl or nr < l:               # 完全不相交
            return
        if l <= nl and nr <= r:            # 完全覆盖
            self.lazy[node] = min(self.lazy[node], val)
            self.data[node] = min(self.data[node], val)
            return
        self._push(node)                    # 先把懒标记下放
        mid = (nl + nr) >> 1
        self._range_update(l, r, val, node << 1, nl, mid)
        self._range_update(l, r, val, node << 1 | 1, mid + 1, nr)
        self.data[node] = min(self.data[node << 1], self.data[node << 1 | 1])

    def point_query(self, idx: int) -> int:
        """查询单点 idx 的当前最小值"""
        return self._point_query(idx, 1, 0, self.N - 1)

    def _point_query(self, idx, node, nl, nr):
        if nl == nr:
            return self.data[node]
        self._push(node)
        mid = (nl + nr) >> 1
        if idx <= mid:
            return self._point_query(idx, node << 1, nl, mid)
        else:
            return self._point_query(idx, node << 1 | 1, mid + 1, nr)


def minValidStrings(words: List[str], target: str) -> int:
    n = len(target)

    # ---------- 1. 把所有合法前缀的哈希放进集合 ----------
    valid_hash = set()
    for w in words:
        h = 0
        for ch in w:                     # 逐字符累加哈希，形成前缀哈希
            h = (h * BASE + (ord(ch) - 96)) % MOD
            valid_hash.add(h)            # 当前前缀对应的哈希值

    # ---------- 2. 预处理 target 的滚动哈希 ----------
    pref = [0] * (n + 1)                  # pref[i] = hash of target[:i]
    power = [1] * (n + 1)                 # power[i] = BASE^i % MOD
    for i, ch in enumerate(target, 1):
        pref[i] = (pref[i - 1] * BASE + (ord(ch) - 96)) % MOD
        power[i] = (power[i - 1] * BASE) % MOD

    def get_hash(l: int, r: int) -> int:
        """返回 target[l:r]（左闭右开）的哈希，O(1)"""
        return (pref[r] - pref[l] * power[r - l]) % MOD

    # ---------- 3. DP + 线段树 ----------
    seg = SegTree(n + 1)                 # 位置 0~n
    seg.range_update(0, 0, 0)            # dp[0] = 0

    for i in range(n):
        cur = seg.point_query(i)         # 当前 dp[i]
        if cur >= seg.inf:               # 这个前缀根本不可达
            continue

        # ---- 二分找最长合法子串 ----
        lo, hi = i + 1, n
        best = i                         # 最右合法右端点（左闭右开）
        while lo <= hi:
            mid = (lo + hi) >> 1
            h = get_hash(i, mid)         # target[i:mid] 的哈希
            if h in valid_hash:          # 合法前缀
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        if best > i:                     # 至少有一个合法子串
            # 把 dp[i] + 1 更新到区间 (i, best]，即下标 i+1 … best
            seg.range_update(i + 1, best, cur + 1)

    ans = seg.point_query(n)
    return -1 if ans >= seg.inf else ans
```

#### 复杂度  

- **时间复杂度**  
  1. 生成合法前缀哈希：`O( Σ|words[i]| ) ≤ 10⁵`。  
  2. 预处理 `target` 的滚动哈希：`O(|target|) ≤ 5·10⁴`。  
  3. 主循环遍历 `i = 0 … n-1`：  
     - 每次二分查找最长合法长度：`O(log n)` 次哈希查询。  
     - 区间最小更新（线段树）：`O(log n)`。  
     综合为 `O(n log n)`，其中 `n = |target| ≤ 5·10⁴`。  
  - 用大白话说，`log n` 只相当于“把 5 万次操作压缩成约 16 次”，所以整体运行非常快。

- **空间复杂度**  
  - 合法前缀哈希集合：`O( Σ|words[i]| ) ≤ 10⁵`。  
  - 前缀哈希数组、幂次数组各 `O(n)`。  
  - 线段树大小约为 `4 * (n+1)`，也是 `O(n)`。  
  - 总体 `O(n + Σ|words[i]|)`，约几百千的整数，完全在内存限制内。

> 与暴力解相比，时间从 **二次方** 降到了 **线性乘对数**，在本题的大数据范围下实现了 **秒级** 通过。

---

## 心得

- **核心技巧**：  
  1. **滚动哈希** 把子串比较降到 `O(1)`。  
  2. **二分搜索** 利用“合法长度单调递增”快速定位最长合法子串。  
  3. **线段树（区间最小更新）** 把 DP 的“区间放松”操作压缩到 `O(log n)`。

- **适用的题型**（可以复用上述组合）  
  - “把字符串分割成若干合法片段的最小/最大数量”  
  - “在字符串中寻找满足某种前缀/后缀约束的最短覆盖”  
  - “使用若干子串（或子数组）覆盖整个序列的最小代价”  

- **一句话总结解题钥匙**  
  > **把“遍历每个起点并逐个尝试” → “一次二分定位最长合法区间 + 区间最小更新”。**

---

## 反思

- **第一反应**：直接枚举所有合法前缀，做 DP，代码写得很快，但忽视了时间复杂度。  
- **最容易踩的坑**  
  1. **哈希冲突**：使用双模（两个不同的 MOD）可以进一步降低冲突概率，这里为简化只用了单模。  
  2. **边界条件**：`dp` 初始化为无穷大、`target` 长度为 0（虽然题目保证≥1）以及二分的左闭右开写法容易写错。  
  3. **线段树懒标记**：忘记向下推送会导致后面的查询得到错误的最小值。  
- **下次类似题目第一步**：  
  > “先把所有合法子串的**快速判定**手段做好（哈希或 Trie），再思考如何把 DP 的**状态转移**从 O(n) 降到 O(log n)”。