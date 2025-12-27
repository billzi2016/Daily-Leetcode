# #3470. 排列 IV / Permutations IV

> 难度：困难 · 标签：Array、Math、Combinatorics、Enumeration · [LeetCode 链接](https://leetcode.com/problems/permutations-iv/)

---

## 题目（英文原版）

**Description**

Given two integers, n and k, an alternating permutation is a permutation of the first n positive integers such that no two adjacent elements are both odd or both even.
Return the k-th alternating permutation sorted in lexicographical order. If there are fewer than k valid alternating permutations, return an empty list.

**Examples**

**Example 1:**

```
Input: n = 4, k = 6
Output: [3,4,1,2]
Explanation:
The lexicographically-sorted alternating permutations of [1, 2, 3, 4] are:
Since k = 6 , we return [3, 4, 1, 2] .
```

**Example 2:**

```
Input: n = 3, k = 2
Output: [3,2,1]
Explanation:
The lexicographically-sorted alternating permutations of [1, 2, 3] are:
Since k = 2 , we return [3, 2, 1] .
```

**Example 3:**

```
Input: n = 2, k = 3
Output: []
Explanation:
The lexicographically-sorted alternating permutations of [1, 2] are:
There are only 2 alternating permutations, but k = 3 , which is out of range. Thus, we return an empty list [] .
```

**Constraints**

- 1 <= n <= 100
- 1 <= k <= 1015

---

## 题目（中文翻译）

给定两个整数 `n` 和 `k`，**交替排列（alternating permutation）** 指的是前 `n` 个正整数的一个排列，使得相邻的两个元素不存在同时为奇数或同时为偶数的情况。  
返回字典序（lexicographical order）排序后的第 `k` 个交替排列。如果满足条件的交替排列少于 `k` 个，返回空列表。

**示例 1**  
**输入**: `n = 4, k = 6`  
**输出**: `[3,4,1,2]`  
**解释**:  
`[1, 2, 3, 4]` 的所有字典序排序后的交替排列为:  
（此处列出所有交替排列）  
由于 `k = 6`，所以返回 `[3, 4, 1, 2]`。

**示例 2**  
**输入**: `n = 3, k = 2`  
**输出**: `[3,2,1]`  
**解释**:  
`[1, 2, 3]` 的所有字典序排序后的交替排列为:  
（此处列出所有交替排列）  
由于 `k = 2`，所以返回 `[3, 2, 1]`。

**示例 3**  
**输入**: `n = 2, k = 3`  
**输出**: `[]`  
**解释**:  
`[1, 2]` 的所有字典序排序后的交替排列为:  
（此处列出所有交替排列）  
只有 2 种交替排列，但 `k = 3` 超出范围。因此返回空列表 `[]`。

**约束条件**  
- `1 <= n <= 100`  
- `1 <= k <= 10^15`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 `1 … n` 的所有排列全部枚举出来，逐个检查「相邻两个数奇偶性不同」这个条件，满足的留下来，排好字典序（lexicographical order）后直接取第 `k` 个。

- **用到的数据结构**：  
  - `itertools.permutations` 可以一次性生成所有排列，就像把一本字典的每一页都翻一遍。  
  - “奇偶性检查”相当于在字典里查每一页的内容，判断它是否符合我们想要的“奇-偶-奇-偶 …”模式。  

- **为什么正确**：  
  - 我们把所有可能的排列都列出来，过滤出合法的交替排列，然后按照字典序排序。只要第 `k` 个合法排列存在，必然就在这个列表的第 `k` 位。  

- **复杂度分析**：  
  - **时间**：枚举 `n!`（`n` 的阶乘）个排列，每个排列要检查 `n-1` 次相邻奇偶性，时间大约是 `O(n!·n)`。  
    - `n!` 代表“从 1 到 n 按任意顺序排”的所有可能，就像把所有可能的钥匙都试一遍。即使 `n=10`，`10! = 3,628,800`，已经很大了；`n=20` 时已经天文数字。  
  - **空间**：需要把所有合法排列保存下来，最坏情况下是 `O(n!·n)`（每个排列占 `n` 个整数的空间）。  

显然，这种方法只能在 `n` 很小（比如 `n≤8`）时才会跑得动，根本不满足题目 `n ≤ 100`、`k ≤ 10^15` 的要求。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**。其实我们并不需要真的把所有排列列出来，只要能 **快速算出** 在某个前缀固定后，剩下的合法排列有多少个，就可以像“数数”一样决定第 `k` 个排列的每一位。

下面一步步推导：

1. **观察奇偶交替的本质**  
   - 只要知道前一个数是奇还是偶，接下来只能选 **另一种奇偶** 的数。  
   - 这就像在走棋盘时只能横向或纵向走一步，方向被前一步锁定。

2. **把剩余的“资源”抽象成两类**  
   - **奇数** 的数量 `o`（odd），  
   - **偶数** 的数量 `e`（even）。  
   只要知道 `o`、`e` 和上一个数的奇偶性，就能唯一决定后面还能组成多少合法排列。

3. **动态规划（DP）计数**  
   - 状态 `dp[o][e][p]`：还有 `o` 个奇数、`e` 个偶数未使用，且上一个放的数的奇偶性是 `p`（`p = 0` 表示偶，`p = 1` 表示奇，`p = -1` 表示还没有放任何数）。  
   - 转移：  
     - 若 `p = -1`（还没有放数），我们可以任选一个奇数或偶数作为第一个数。  
       ```
       dp[o][e][-1] = o * dp[o-1][e][1] + e * dp[o][e-1][0]
       ```
       乘以 `o`（或 `e`）是因为不同的具体数字会产生不同的排列，就像字典里每一页都是唯一的。  
     - 若 `p = 0`（上一个是偶），下一个必须是奇数：
       ```
       dp[o][e][0] = o * dp[o-1][e][1]
       ```
     - 若 `p = 1`（上一个是奇），下一个必须是偶数：
       ```
       dp[o][e][1] = e * dp[o][e-1][0]
       ```
   - 递归结束条件：`o == 0 and e == 0` 时已经排完所有数，只有一种合法方式 → `1`。  
   - 为防止整数爆炸（`n!` 极大），我们把计数 **上限截断** 到 `INF = 10^18`（大于题目给出的最大 `k`），只要超过 `k` 就不必再继续精确计数。

4. **构造第 k 个排列**  
   - 从左到右依次决定每一位的数字。  
   - 在第 `pos` 位，遍历所有 **未使用且满足奇偶交替** 的数字（从小到大），计算若选它作为当前位，后面还能形成多少合法排列 `cnt = dp[remaining_o][remaining_e][parity(chosen)]`。  
   - 如果 `cnt >= k`，说明第 `k` 个排列就在这些以 `chosen` 为前缀的集合里，**确定** 这位为 `chosen`，并继续决定下一位。  
   - 否则，`k -= cnt`，说明第 `k` 个排列不在这块子集合里，继续尝试更大的数字。  
   - 若遍历完所有候选数字仍未找到（即原始总数 < `k`），直接返回空列表 `[]`。

5. **为什么快**  
   - DP 状态数只有 `(~50) × (~50) × 2 ≈ 5,000`，每个状态只计算一次，时间几乎可以忽略。  
   - 构造答案时每一步最多遍历 `n` 个数字，整体时间 `O(n²)`（`n ≤ 100`），完全可以接受。  

#### 代码（Python）

```python
from functools import lru_cache
from typing import List

INF = 10 ** 18          # 超过这个值就不必继续精确计数

def kthAlternatingPermutation(n: int, k: int) -> List[int]:
    """
    返回第 k (1-indexed) 个交替排列；若不存在返回 []。
    """

    # ---------- 1. 预处理奇偶数的数量 ----------
    total_odd = (n + 1) // 2          # 1..n 中奇数的个数
    total_even = n // 2              # 偶数的个数

    # ---------- 2. DP：统计剩余 o、e、上一个奇偶的排列数 ----------
    @lru_cache(None)
    def dp(o: int, e: int, last: int) -> int:
        """
        o: 还剩多少奇数未使用
        e: 还剩多少偶数未使用
        last: 前一个数的奇偶性
              -1 -> 还没有放任何数（即是第一位）
               0 -> 前一个是偶数
               1 -> 前一个是奇数
        返回可以组成的合法排列数（上限为 INF）
        """
        if o == 0 and e == 0:               # 已经排完
            return 1

        total = 0
        if last == -1:                      # 第一次选数，可以任选奇数或偶数
            if o > 0:
                total += o * dp(o - 1, e, 1)   # 选一个奇数作为首位
            if e > 0:
                total += e * dp(o, e - 1, 0)   # 选一个偶数作为首位
        elif last == 0:                     # 前一个是偶数，下一个必须是奇数
            if o == 0:
                return 0
            total += o * dp(o - 1, e, 1)
        else:                               # last == 1，前一个是奇数，下一个必须是偶数
            if e == 0:
                return 0
            total += e * dp(o, e - 1, 0)

        # 防止数值爆炸，只保留到 INF（因为 k ≤ 1e15）
        return total if total < INF else INF

    # ---------- 3. 构造第 k 个排列 ----------
    # 记录哪些数字已经用了，使用布尔数组快速判断
    used = [False] * (n + 1)               # 1-indexed
    result = []
    remaining_odd, remaining_even = total_odd, total_even
    last_parity = -1                       # -1 表示还没有放数

    for pos in range(n):
        # 依次尝试当前未使用且满足奇偶交替的最小数字
        found = False
        for cand in range(1, n + 1):
            if used[cand]:
                continue
            cand_parity = cand & 1          # 1 -> 奇数, 0 -> 偶数
            # 检查奇偶交替约束
            if last_parity != -1 and cand_parity == last_parity:
                continue

            # 计算如果把 cand 放在当前位置，后面还能组成多少合法排列
            o = remaining_odd - (cand_parity == 1)
            e = remaining_even - (cand_parity == 0)
            cnt = dp(o, e, cand_parity)

            if cnt >= k:                    # 第 k 个排列一定在这块子集合里
                # 确定当前位
                result.append(cand)
                used[cand] = True
                remaining_odd, remaining_even = o, e
                last_parity = cand_parity
                found = True
                break
            else:
                # 第 k 个不在这里，跳过这块子集合
                k -= cnt

        if not found:                       # k 超出总数，直接返回空列表
            return []

    return result


# ---------- 4. 示例测试 ----------
if __name__ == "__main__":
    print(kthAlternatingPermutation(4, 6))   # [3, 4, 1, 2]
    print(kthAlternatingPermutation(3, 2))   # [3, 2, 1]
    print(kthAlternatingPermutation(2, 3))   # []
```

**代码要点解释**  

| 行号 | 中文注释 |
|------|----------|
| 1‑2  | 设置一个非常大的上限 `INF`，防止计数爆炸。 |
| 10‑12| 计算 `n` 中奇数、偶数的总数。 |
| 15‑33| `dp` 函数使用 **记忆化搜索**（`lru_cache`），每个 `(o,e,last)` 只算一次。 |
| 21‑28| 根据上一个数的奇偶性决定本轮只能选奇数还是偶数，乘以对应的剩余数量得到所有可能的具体数字。 |
| 36‑44| 构造答案的主循环：遍历位置、尝试候选数字、利用 `dp` 计数决定是否“跳过”。 |
| 47‑55| 计算把候选数字放进去后，剩余奇偶数的数量以及后续排列数 `cnt`。 |
| 57‑63| 若 `cnt >= k`，说明第 `k` 个排列在这块子集合里，确定该位并进入下一轮；否则 `k` 减去这块子集合的大小，继续尝试更大的数字。 |
| 68‑71| 如果在某一位找不到合法数字，说明总排列数 < 原始 `k`，直接返回空列表。 |

#### 复杂度

- **时间复杂度**：  
  - DP 只会被调用 `O(o·e·2) ≤ O(50·50·2) ≈ 5·10³` 次，几乎可以忽略。  
  - 构造答案的循环最多 `n` 次，每次遍历未使用的数字（最多 `n`），所以 `O(n²)`，在 `n ≤ 100` 时最多 `10⁴` 步，极快。  
  - 与暴力解的 `O(n!·n)` 相比，**下降到了多项式时间**，完全可以接受。

- **空间复杂度**：  
  - DP 表大小 `O(o·e·2) ≈ 5·10³`，再加上 `used`、`result` 等数组，总共 `O(n²)`（这里的 `n²` 只是一个上界，实际常数非常小）。  

---

## 心得

- **核心技巧**：把「交替奇偶」约束转化为「只看上一个数字的奇偶性」+「剩余奇数/偶数的计数」，用**记忆化 DP**快速求出「剩余数字可以组成多少合法排列」。
- **适用的题型**  
  1. **交替约束**的排列计数（如「奇数‑偶数交替」或「上升‑下降交替」）。  
  2. **固定前缀 + 计数**的第 k 大/小排列（典型的「字典序第 k 个排列」变形）。  
  3. **两类资源交替使用**的组合计数（例如「男女交替坐排队」）。
- **一句话总结解题钥匙**：  
  > 把「是否满足」的检查从「遍历全部」搬到「只用计数」——用 DP 计算「剩余资源在当前约束下的排列数」，再逐位“数”出第 k 个字典序。

---

## 反思

- **第一反应**：直接枚举所有排列，然后过滤、排序。  
- **最容易踩的坑**  
  1. **计数溢出**：`n!` 很大，直接使用 Python 的整数虽安全，但会导致不必要的计算，需提前截断到 `k` 的上界。  
  2. **奇偶交替的起始限制**：当 `n` 为奇数时，首位必须是奇数；代码中通过 DP 的 `last = -1` 自动处理，别忘了这一步。  
  3. **边界条件**：`o` 或 `e` 为 0 时的转移必须返回 `0`（没有合法的下一个数），否则会产生错误的计数。  
- **下次类似题目**，第一步应该想到：  
  > 「先把约束抽象为状态（比如剩余奇/偶数、上一个数字的属性），用 DP 统计『以某前缀为起点』的合法排列数，再用这个计数逐位构造第 k 个排列。」