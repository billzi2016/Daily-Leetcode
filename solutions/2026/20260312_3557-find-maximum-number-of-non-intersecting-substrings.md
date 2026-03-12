# #3557. 寻找最多不相交子串的数量 / Find Maximum Number of Non Intersecting Substrings

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/find-maximum-number-of-non-intersecting-substrings/)

---

## 题目（英文原版）

**Description**

You are given a string word.
Return the maximum number of non-intersecting substrings of word that are at least four characters long and start and end with the same letter.

**Examples**

**Example 1:**

```
Input: word = "abcdeafdef"
Output: 2
Explanation:
The two substrings are "abcdea" and "fdef" .
```

**Example 2:**

```
Input: word = "bcdaaaab"
Output: 1
Explanation:
The only substring is "aaaa" . Note that we cannot also choose "bcdaaaab" since it intersects with the other substring.
```

**Constraints**

- 1 <= word.length <= 2 * 105
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `word`。  
返回 `word` 中 **长度至少为 4 且首尾字符相同的** 不相交子串（non-intersecting substring）的最大数量。

---

### 示例

**示例 1**  
```
Input: word = "abcdeafdef"
Output: 2
```
**解释**：  
这两个子串分别是 `"abcdea"` 和 `"fdef"` 。

**示例 2**  
```
Input: word = "bcdaaaab"
Output: 1
```
**解释**：  
唯一符合条件的子串是 `"aaaa"`。注意不能同时选择 `"bcdaaaab"`，因为它与前面的子串相交。

---

### 约束条件

- `1 <= word.length <= 2 * 10^5`
- `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有满足条件的子串都枚举出来，然后在这些子串中挑选出**不相交且数量最多**的一组。  
- **子串的条件**：长度 ≥ 4，且首尾字符相同。  
- **不相交**：两个子串的下标区间没有交叉，像 `[l1, r1]` 与 `[l2, r2]` 必须满足 `r1 < l2` 或 `r2 < l1`。  

实现思路：

1. 双层循环 `i`、`j`（`i` 为左端点，`j` 为右端点），检查 `j - i + 1 ≥ 4` 且 `word[i] == word[j]`，如果成立就把区间 `[i, j]` 加入「候选列表」  
   - 这里用到的 **哈希表**（字典）可以类比成一本「查字典」：键是字符，值是该字符出现的所有下标，帮助我们快速判断 `i`、`j` 是否是同一个字符。  
2. 把所有候选区间按右端点从小到大排序，使用**区间调度**的贪心算法：每次挑选最早结束且不与已选区间冲突的区间。  

**为什么能得到正确答案？**  
区间调度的经典贪心证明告诉我们：如果我们总是选择结束最早的可行区间，就一定能得到最多的非交叉区间。因为结束早的区间会留下更多「空间」给后面的区间。

**时间/空间复杂度**  
- 双层循环会遍历所有 `i < j`，最坏情况是 `n`（字符串长度）≈ 2·10⁵ 时，需要检查约 `n²/2` 次，时间复杂度是 **O(n²)**，这在实际中会非常慢（想象一下 200 000² ≈ 4·10¹⁰ 次操作）。  
- 保存所有合法区间需要额外的列表，最坏情况下也可能是 **O(n²)**（每两个相同字符且相距≥3 都会产生一个区间）。  

用大白话说，**O(n²)** 就像「把每个人都和每个人握手」一样，人数多时几乎不可能完成。

#### 代码（Python）

```python
def max_non_intersecting_substrings_bruteforce(word: str) -> int:
    n = len(word)
    intervals = []                     # 保存所有合法区间 (左, 右)

    # 1. 暴力枚举所有子串
    for i in range(n):
        for j in range(i + 3, n):      # j - i + 1 >= 4 等价于 j >= i + 3
            if word[i] == word[j]:     # 首尾字符相同
                intervals.append((i, j))

    # 2. 按右端点升序排序，贪心挑选不相交区间
    intervals.sort(key=lambda x: x[1])   # 按右端点排序
    cnt = 0
    last_end = -1                        # 上一个已选区间的右端点
    for l, r in intervals:
        if l > last_end:                 # 与前面的区间不相交
            cnt += 1
            last_end = r

    return cnt
```

> **注意**：这段代码在 `len(word) = 10⁵` 时会直接卡死，属于「教学演示」用的暴力解。

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要检查每一对起止下标，等价于「每个人和每个人握手」的次数。  
- **空间复杂度**：`O(n²)` — 最坏情况下会保存几乎所有的区间，类似「把每一次握手的记录都存下来」。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有可能的区间**，这一步产生了 `O(n²)` 的开销。  
我们注意到：

1. 只要知道 **每个字符出现的下标**，合法区间就只能在同字符的下标之间产生。  
2. 对于同一个字符的下标序列 `p0 < p1 < … < pk`，如果我们想在位置 `pi` 作为右端点构造子串，只需要找一个左端点 `pj`（`j < i`）满足 `pi - pj ≥ 3`。  
3. 为了让后面的子串有更多「空间」，我们希望选 **最早结束** 的子串。换句话说，在右端点固定时，只要挑选 **左端点尽可能靠左**（但仍满足长度≥4）即可得到最短的合法子串，也就最有可能成为最早结束的区间。

于是我们可以把「挑选区间」的过程转化为 **动态规划**：

- `dp[i]` 表示考虑前 `i+1` 个字符（下标 `0…i`）时，能够得到的最多子串数。  
- 初始时 `dp[-1] = 0`（空串能选 0 个）。  
- 对每个位置 `i`，我们有两种选择  
  1. **不选** 以 `i` 结尾的子串 → `dp[i] = dp[i-1]`  
  2. **选** 一个以 `i` 为右端点的合法子串 `[l, i]` → `dp[i] = max(dp[i], dp[l-1] + 1)`  

关键在于**快速求出** `max(dp[l-1] + 1)`，其中 `l` 是同字符且满足 `i - l ≥ 3` 的左端点。  
我们对每个字符维护：

- `pos[c]`：该字符已出现的下标列表（按出现顺序保存）。  
- `ptr[c]`：指向 `pos[c]` 中**尚未满足距离≥3** 的第一个下标的指针。  
- `best[c]`：在当前遍历到 `i` 时，**所有已经满足 `i - l ≥ 3` 的左端点**中，`dp[l-1] + 1` 的最大值。  

遍历字符串一次（`i` 从左到右）：

1. **继承** 前缀的答案：`dp[i] = dp[i-1]`（若 `i==0` 则 `dp[0]=0`）。  
2. **把新出现的左端点**（即之前遍历到的同字符位置）加入 `best`：  
   - 当 `i - pos[c][ptr] ≥ 3` 时，这个左端点已经可以和当前 `i` 组合形成合法子串。  
   - 计算 `candidate = dp[pos-1] + 1`（`pos==0` 时 `dp[-1]` 视作 0），更新 `best[c]`。  
   - 将指针 `ptr` 向后移动，保证每个左端点只被处理一次。  
3. **使用 `best` 更新** `dp[i]`：如果 `best[c]` 大于当前 `dp[i]`，说明以 `i` 为右端点可以得到更好的方案。  
4. **把当前下标加入 `pos`**，为将来的右端点做准备。  

整个过程每个字符的每个下标只会进入 `pos`、被指针扫描一次，时间 **O(n)**，空间 **O(n)**（存储所有下标）。

> **类比**：把每个字符看成「同一家快递公司的配送点」，`pos[c]` 是该公司的所有站点。我们要在同一家站点之间挑选「距离≥3」的配对，且希望配对尽可能「早结束」——这就像让快递员尽快把货送完，后面的货才能继续装车。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def max_non_intersecting_substrings(word: str) -> int:
    """
    返回最多可以选取的互不相交、长度≥4 且首尾字符相同的子串数量。
    时间复杂度 O(n) ，空间复杂度 O(n)。
    """
    n = len(word)
    if n < 4:                     # 长度不足 4，直接返回 0
        return 0

    # dp[i]：前 i+1 个字符（下标 0..i）能得到的最大子串数
    dp: List[int] = [0] * n

    # 对每个字符维护出现位置列表、指针、以及目前可用的最大值
    pos = defaultdict(list)      # char -> [出现下标]
    ptr = defaultdict(int)       # char -> 已经处理完的下标指针
    best = defaultdict(lambda: -10**9)   # char -> max(dp[l-1] + 1) for eligible l

    for i, ch in enumerate(word):
        # 1) 继承前缀的最优解
        if i > 0:
            dp[i] = dp[i - 1]

        # 2) 把之前出现的同字符位置，若满足距离≥3，就加入 best
        lst = pos[ch]                     # 已经出现的下标列表
        p = ptr[ch]                       # 当前还未处理的指针
        while p < len(lst) and i - lst[p] >= 3:
            left = lst[p]
            # dp 在 left 左侧的最优解，左端点为 0 时视作 0
            prev = dp[left - 1] if left > 0 else 0
            candidate = prev + 1          # 选取区间 [left, i] 后的子串数
            if candidate > best[ch]:
                best[ch] = candidate
            p += 1
        ptr[ch] = p                       # 记住已处理到的位置

        # 3) 使用 best 更新 dp[i]（若以 i 为右端点能得到更好解）
        if best[ch] > dp[i]:
            dp[i] = best[ch]

        # 4) 把当前下标加入 pos，供以后作为左端点使用
        pos[ch].append(i)

    # dp[-1] 对应整个字符串的答案
    return dp[-1]
```

**代码要点注释**（已在代码中标注）：

- `dp[i] = dp[i-1]` —— 把「不选」的情况带进来。  
- `while i - lst[p] >= 3` —— 当右端点与左端点距离够大（≥ 3）时，左端点正式「合格」可以参与构造子串。  
- `candidate = prev + 1` —— 选中 `[left, i]` 后，子串数加一。  
- `best[ch]` —— 记录所有已经「合格」的左端点中，能够得到的最大子串数，保证后面每次只用 O(1) 就能更新 `dp[i]`。  

#### 复杂度

- **时间复杂度**：`O(n)` — 每个字符的下标只会进入 `pos`、被指针扫描一次，等价于「一次遍历」整个字符串。  
- **空间复杂度**：`O(n)` — 需要保存每个字符出现的所有下标，总数不超过 `n`。

相较于暴力的 `O(n²)`，`O(n)` 就像「一次性把所有快递点排好队」而不是「每次都重新找一遍」——快得多。

---

## 心得

- **核心技巧**：把「选区间」的问题转化为**前缀动态规划**，并利用**同字符出现位置的单调性**来在 `O(1)` 时间内得到每个右端点的最优左端点。  
- **适用场景**：  
  1. 需要在字符串中挑选满足特定起止关系的子串（如「首尾相同且长度≥k」）。  
  2. 任意**区间调度**类问题，只要能够在遍历时维护「当前可用的最优左端点」即可。  
  3. 类似「最多不相交的好子数组」或「最大不相交的好区间」的 DP/贪心混合题目。  
- **一句话总结解题钥匙**：**“对每个字符维护可用左端点的最大前缀价值”**，即在遍历时把「能组成合法子串的左端点」提前算好，用 `best` 表示。

---

## 反思

- **第一反应**：直接枚举所有子串，尝试用区间调度贪心求解。  
- **最容易踩的坑**：  
  - 忘记 **长度≥4** 的限制，导致产生非法子串。  
  - 在 DP 转移时误把 `dp[l]` 当作 `dp[l-1]`，导致区间相交。  
  - 对指针 `ptr` 的更新不当，会把同一个左端点多次计入 `best`，导致错误的计数。  
- **下次遇到同类题**：第一步先思考 **“是否可以把子串映射为区间，然后用前缀 DP + 单调结构维护最优左端点？”**，如果答案是肯定的，就可以直接走向线性时间的解法。