# #3575. Maximum Good Subtree Score / Maximum Good Subtree Score

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Tree、Depth-First Search、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-good-subtree-score/)

---

## 题目（英文原版）

**Description**

You are given an undirected tree rooted at node 0 with n nodes numbered from 0 to n - 1. Each node i has an integer value vals[i], and its parent is given by par[i].
A subset of nodes within the subtree of a node is called good if every digit from 0 to 9 appears at most once in the decimal representation of the values of the selected nodes.
The score of a good subset is the sum of the values of its nodes.
Define an array maxScore of length n, where maxScore[u] represents the maximum possible sum of values of a good subset of nodes that belong to the subtree rooted at node u, including u itself and all its descendants.
Return the sum of all values in maxScore.
Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: vals = [2,3], par = [-1,0]
Output: 8
Explanation:
```

**Example 2:**

```
Input: vals = [1,5,2], par = [-1,0,0]
Output: 15
Explanation:
```

**Example 3:**

```
Input: vals = [34,1,2], par = [-1,0,1]
Output: 42
Explanation:
```

**Example 4:**

```
Input: vals = [3,22,5], par = [-1,0,1]
Output: 18
Explanation:
```

**Constraints**

- 1 <= n == vals.length <= 500
- 1 <= vals[i] <= 109
- par.length == n
- par[0] == -1
- 0 <= par[i] < n for i in [1, n - 1]
- The input is generated such that the parent array par represents a valid tree.

---

## 题目（中文翻译）

你被给定一棵 **无向树（undirected tree）**，根节点为 0，树中共有 n 个节点，编号为 0 到 n‑1。每个节点 i 拥有整数值 `vals[i]`，其父节点由数组 `par[i]` 给出。  

在某个节点的子树（subtree）内部选取若干节点构成的集合，如果所选节点的值的十进制表示中，数字 0~9 每个至多出现一次，则称该集合为 **好集合（good subset）**。  

好集合的 **得分（score）** 为其所有节点值的总和。  

定义数组 `maxScore`，长度为 n，其中 `maxScore[u]` 表示 **以节点 u 为根的子树**（包括 u 本身及其所有后代）中可以选取的好集合的最大可能总和。  

返回 `maxScore` 中所有元素的和。由于答案可能很大，请返回 **模 10^9 + 7** 的结果。  

---  

### 示例  

**示例 1**  
```text
Input: vals = [2,3], par = [-1,0]
Output: 8
Explanation:
```

**示例 2**  
```text
Input: vals = [1,5,2], par = [-1,0,0]
Output: 15
Explanation:
```

**示例 3**  
```text
Input: vals = [34,1,2], par = [-1,0,1]
Output: 42
Explanation:
```

**示例 4**  
```text
Input: vals = [3,22,5], par = [-1,0,1]
Output: 18
Explanation:
```

---  

### 约束条件  

- 1 ≤ n = `vals.length` ≤ 500  
- 1 ≤ `vals[i]` ≤ 10^9  
- `par.length` = n  
- `par[0]` = -1  
- 对于 i ∈ [1, n‑1]，0 ≤ `par[i]` < n  
- 输入保证数组 `par` 构成一棵合法的树  

---  

返回值需对 **10^9 + 7** 取模。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**每个节点所在子树中的所有可能子集，检查子集是否“好”，然后取分数最大的那个。  

- **子集**：可以把子树看成一堆水果，直接把它们全部挑出来或不挑，所有挑法的组合就是子集。  
- **好子集的判定**：把每个选中的节点的数值写成十进制，例如 `34 → {3,4}`。把出现的数字放进一个集合，若出现了重复的数字（比如两个节点都用了 `3`，或者同一个节点的数值里出现了两次 `5`），就不满足“每个数字至多出现一次”。这相当于在检查 **哈希表**（字典）里有没有冲突：键是数字，值是出现的次数。  
- **为什么正确**：遍历了**全部**合法子集，最大分数自然不会错过。  

显然，这种做法在 **n ≤ 500** 时根本不可行，因为子树里节点数可能达到 500，子集数是 `2^500`，天文数字。

#### 代码（Python）  

```python
from itertools import combinations
from collections import defaultdict

def brute(vals, par):
    n = len(vals)
    # 建立孩子表
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[par[i]].append(i)

    # 返回以 u 为根的子树中所有节点的列表
    def collect(u):
        nodes = [u]
        for v in children[u]:
            nodes.extend(collect(v))
        return nodes

    maxScore = [0] * n
    MOD = 10**9 + 7

    for u in range(n):
        nodes = collect(u)                # 子树所有节点
        best = 0
        # 枚举子集的大小，从 0 到 len(nodes)
        for k in range(len(nodes) + 1):
            for combo in combinations(nodes, k):
                used = set()               # 已经使用的数字
                total = 0
                ok = True
                for idx in combo:
                    s = str(vals[idx])
                    # 同一个数值内部出现重复数字直接判为非法
                    if len(set(s)) != len(s):
                        ok = False
                        break
                    for ch in s:
                        if ch in used:
                            ok = False
                            break
                        used.add(ch)
                    if not ok:
                        break
                    total += vals[idx]
                if ok:
                    best = max(best, total)
        maxScore[u] = best
    return sum(maxScore) % MOD
```

> 代码可以跑通小样例，但在 `n=20` 以上就会超时。

#### 复杂度  

- **时间复杂度**：对每个节点的子树枚举所有子集，最坏是 `O(2^k)`（`k` 为子树大小），整体是指数级，实际不可接受。  
- **空间复杂度**：主要是递归栈和集合 `used`，`O(k)`，同样随子树大小线性增长。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于 **“枚举所有子集”**。  
观察题目可以发现：

1. **数字种类只有 10 种（0~9）**。  
   因此我们可以用 **10 位二进制掩码** 来记录已经用了哪些数字。  
   - 把每个节点的数值拆成数字集合，例如 `34 → 0b0000001100`（第 3、4 位为 1）。  
   - 如果一个数值内部出现重复数字，它对应的掩码会出现同一位被“多次使用”，这在掩码里表现为 **该位已经是 1**，所以这种节点根本 **不能被选**。  

2. **子树结构** 让我们可以使用 **树形动态规划（Tree DP）**。  
   - 对每个节点 `u`，我们维护一个 DP 表 `dp_u[mask]`，表示**在 `u` 的子树中**（可以选也可以不选 `u`）**使用了 `mask` 这些数字时，能够得到的最大分数。  
   - `mask` 的范围是 `0 … 2^10-1 = 1023`，最多只有 **1024** 种状态，十分小。  

3. **合并子树** 类似 **背包合并**：  
   - 先把 `u` 本身的情况放进去（如果它的数字不冲突），得到初始 `dp_u`。  
   - 然后依次把每个孩子 `v` 的 DP 表合并进来。合并时要保证两侧的掩码不冲突（`mask1 & mask2 == 0`），新的掩码是 `mask1 | mask2`，对应的分数是 `score1 + score2`，取最大值。  

这样，遍历完所有子树后，`dp_u` 中的所有值就是 **合法子集的所有可能分数**，取最大即为 `maxScore[u]`。  

#### 关键概念的零基础解释  

| 概念 | 类比 | 说明 |
|------|------|------|
| **位掩码（bitmask）** | **钥匙孔**：每个数字对应一把钥匙，只要钥匙已经插进去（对应位为 1），就不能再插同样的钥匙。 | 用 10 位二进制数记录哪些数字已被使用，`1` 表示已经占用。 |
| **树形 DP** | **自底向上组装拼图**：先把每个小块（叶子）做好，再把它们拼到父块上，父块的状态取决于子块的所有可能组合。 | 在 DFS 的返回过程中，把子树的状态合并到父节点。 |
| **背包合并** | **装箱子**：两个箱子里装的东西不能有相同颜色的球（数字），合并时只要颜色不冲突就可以一起装进更大的箱子。 | 两个子集的掩码不交叉才可以合并。 |

#### 代码（Python）

```python
from typing import List, Dict

MOD = 10**9 + 7
FULL_MASK = (1 << 10) - 1          # 10 位全 1，即 0b1111111111 = 1023

def maxGoodSubtreeScore(vals: List[int], par: List[int]) -> int:
    n = len(vals)

    # ---------- 1. 建立树的孩子表 ----------
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[par[i]].append(i)

    # ---------- 2. 预处理每个节点的数字掩码 ----------
    # 若数值内部出现重复数字，则标记为 -1（不可选）
    node_mask = []
    for v in vals:
        mask = 0
        ok = True
        for ch in str(v):
            d = int(ch)
            bit = 1 << d
            if mask & bit:          # 已经出现过该数字
                ok = False
                break
            mask |= bit
        node_mask.append(mask if ok else -1)

    # ---------- 3. 深度优先遍历 + DP ----------
    maxScore = [0] * n               # 最终答案数组

    def dfs(u: int) -> Dict[int, int]:
        """
        返回字典 dp:
        key   -> 已使用的数字掩码 (0~1023)
        value -> 在 u 子树中得到的最大分数
        """
        dp = {0: 0}                 # 什么都不选，分数 0

        # 如果 u 本身可以被选，加入一种只选自己的状态
        if node_mask[u] != -1:
            dp[node_mask[u]] = vals[u]

        # 依次合并每个孩子的 dp 表
        for v in children[u]:
            child_dp = dfs(v)       # 递归得到子树 v 的 dp
            new_dp = dp.copy()      # 用来存放合并后的结果

            for mask1, sum1 in dp.items():
                for mask2, sum2 in child_dp.items():
                    if mask1 & mask2:        # 掩码冲突，数字重复
                        continue
                    merged = mask1 | mask2
                    cand = sum1 + sum2
                    # 取最大值
                    if cand > new_dp.get(merged, -1):
                        new_dp[merged] = cand
            dp = new_dp               # 更新为合并后的 dp

        # 当前节点的 maxScore 即 dp 中的最大分数
        maxScore[u] = max(dp.values())
        return dp

    dfs(0)                           # 从根节点 0 开始

    # ---------- 4. 结果求和并取模 ----------
    return sum(maxScore) % MOD
```

> 代码已加入详细中文注释，直接复制即可运行。  

#### 复杂度  

- **时间复杂度**  
  - 每个节点的 DP 表最多有 `2^10 = 1024` 条记录。  
  - 合并一次子树相当于两张表的 **笛卡尔积**，最坏是 `1024 × 1024 ≈ 1e6` 次比较。  
  - 对所有 `n‑1` 条边进行合并，整体是 `O(n * 2^10 * 2^10)`，即 `O(n * 1e6)`。  
  - 这里 `n ≤ 500`，所以最多约 `5×10^8` 次极限操作；实际因为很多掩码不存在（多数为 -1），常数更小，能够在 1‑2 秒内跑完。  

- **空间复杂度**  
  - 每个递归层只保存当前节点的 DP 表，大小 `O(2^10)`。  
  - 递归深度最多 `n`，但我们复用同一个字典对象，整体空间为 `O(n + 2^10)` ≈ `O(n)`（约几千字节），完全可以接受。

与暴力解相比，时间从 **指数级** 降到了 **多项式级**（事实上是常数级的 2^10），在所有约束下都能轻松通过。

---

## 心得  

- **核心技巧**：把“每个数字只能出现一次”转化为 **10 位二进制掩码**，再利用 **树形 DP + 背包合并** 求最大权值子集。  
- **适用的题型**  
  1. **树上带有位掩码约束的最大权值子集**（如 “Maximum Subtree of Unique Letters”）。  
  2. **带有 0/1 冲突约束的背包合并**（如 “Maximum Weight Independent Set on Tree with Color Conflict”。）  
  3. **子集冲突判定的位运算 DP**（如 “Maximum Sum of Non‑Overlapping Digit Numbers”。）  

- **一句话总结解题钥匙**：  
  “把十种数字映射成 10 位二进制，利用树的自底向上合并，确保掩码不冲突时取最大和。”

---

## 反思  

- **拿到题目第一反应**：先想到“枚举所有子集”，因为题目本身在说“子集”。  
- **最容易踩的坑**  
  1. **同一个数值内部出现重复数字**（如 `11`、`100`）也会违反 “每个数字至多出现一次”，必须在预处理时直接剔除。  
  2. **掩码冲突的判断**必须用位运算 `mask1 & mask2 == 0`，否则容易写成 `!= 0` 导致逻辑相反。  
  3. **取最大分数时忘记考虑空集**（掩码 `0`），导致某些子树返回 `-inf`。  
  4. **结果取模**：只在最终求和时取模，局部 DP 中不需要取模，否则可能导致错误的比较。  

- **下次遇到同类题的第一步**：  
  “先把约束转化为位掩码（或集合），看能否利用小的状态空间（2^k）进行 DP，再在树/图结构上做自底向上的合并”。  

祝你在算法的旅程中不断升级！