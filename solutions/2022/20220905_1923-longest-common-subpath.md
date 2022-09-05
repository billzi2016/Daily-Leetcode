# #1923. **最长公共子路径** / Longest Common Subpath

> 难度：困难 · 标签：Array、Binary Search、Rolling Hash、Suffix Array、Hash Function · [LeetCode 链接](https://leetcode.com/problems/longest-common-subpath/)

---

## 题目（英文原版）

**Description**

There is a country of n cities numbered from 0 to n - 1. In this country, there is a road connecting every pair of cities.
There are m friends numbered from 0 to m - 1 who are traveling through the country. Each one of them will take a path consisting of some cities. Each path is represented by an integer array that contains the visited cities in order. The path may contain a city more than once, but the same city will not be listed consecutively.
Given an integer n and a 2D integer array paths where paths[i] is an integer array representing the path of the ith friend, return the length of the longest common subpath that is shared by every friend's path, or 0 if there is no common subpath at all.
A subpath of a path is a contiguous sequence of cities within that path.

**Examples**

**Example 1:**

```
Input: n = 5, paths = [[0,1,2,3,4],
                       [2,3,4],
                       [4,0,1,2,3]]
Output: 2
Explanation: The longest common subpath is [2,3].
```

**Example 2:**

```
Input: n = 3, paths = [[0],[1],[2]]
Output: 0
Explanation: There is no common subpath shared by the three paths.
```

**Example 3:**

```
Input: n = 5, paths = [[0,1,2,3,4],
                       [4,3,2,1,0]]
Output: 1
Explanation: The possible longest common subpaths are [0], [1], [2], [3], and [4]. All have a length of 1.
```

**Constraints**

- 1 <= n <= 105
- m == paths.length
- 2 <= m <= 105
- sum(paths[i].length) <= 105
- 0 <= paths[i][j] < n
- The same city is not listed multiple times consecutively in paths[i].

---

## 题目（中文翻译）

给定一个有 `n` 座城市的国家，城市编号为 `0` 到 `n-1`。在该国家中，每一对城市之间都有一条道路相连。  
有 `m` 位朋友（friends），编号为 `0` 到 `m-1`，他们正在全国旅行。每位朋友会走一条**路径（path）**，路径由若干城市组成。每条路径用一个整数数组表示，数组中的元素按访问顺序排列。路径中可能出现同一座城市多次，但同一座城市不会在数组中出现相邻两次。

给定整数 `n` 和二维整数数组 `paths`，其中 `paths[i]` 表示第 `i` 位朋友的路径，返回所有朋友的路径中**最长公共子路径（subpath）**的长度。如果不存在公共子路径，则返回 `0`。  
**子路径（subpath）**指的是路径中连续的一段城市序列。

### 示例

#### 示例 1
```
Input: n = 5, paths = [[0,1,2,3,4],
                       [2,3,4],
                       [4,0,1,2,3]]
Output: 2
Explanation: 最长的公共子路径是 [2,3]，长度为 2。
```

#### 示例 2
```
Input: n = 3, paths = [[0],[1],[2]]
Output: 0
Explanation: 三条路径之间不存在公共子路径。
```

#### 示例 3
```
Input: n = 5, paths = [[0,1,2,3,4],
                       [4,3,2,1,0]]
Output: 1
Explanation: 可能的最长公共子路径有 [0]、[1]、[2]、[3]、[4]，它们的长度均为 1。
```

### 约束条件
- `1 <= n <= 10^5`
- `m == paths.length`
- `2 <= m <= 10^5`
- `sum(paths[i].length) <= 10^5`
- `0 <= paths[i][j] < n`
- 同一座城市在 `paths[i]` 中不会出现相邻两次。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把每个朋友的路径都枚举出所有可能的**连续子路径**（即子串），然后找出同时出现在所有路径里的最长子路径。

- **枚举子路径**：对于长度为 `L` 的路径，我们可以把它的每个起点 `i (0 ≤ i ≤ L‑len)` 取出长度为 `len` 的子数组 `[path[i], …, path[i+len‑1]]`。这跟我们在字符串里找子串的做法一模一样，只是这里的“字符”是城市编号。
- **存放子路径**：把每个子路径当作一个“单词”，放进集合（`set`）里。集合的作用类似字典的“查词”。如果我们把子路径转成一个不可变的元组 `(a,b,c,…)`，就可以直接用 Python 的 `set` 做去重与交集操作。
- **交集**：先把第一个朋友的所有子路径放进集合 `common`，随后依次和后面的朋友的子路径集合取交集（`common &= cur_set`），最后 `common` 里剩下的就是所有**共同出现**的子路径。只要 `common` 非空，就说明长度 `len` 是可行的。

为什么正确？  
因为我们把 **所有** 长度为 `len` 的子路径都列举出来，交集操作确保只保留在 **每个人** 的路径里都出现的子路径。只要交集里还有元素，就说明至少有一个公共子路径。

时间/空间复杂度（大白话）  
- 对每个人的路径长度记为 `L`，枚举子路径的次数是 `O(L)`（每个起点一次）。如果把所有朋友的路径长度总和记为 `S`（题目给的上限是 `10⁵`），枚举所有子路径的总次数就是 `O(S)`。  
- 但是我们在每一次枚举时，还要把子路径转成元组并放进集合，集合的查找/插入平均是 **常数时间**（≈O(1)），所以整体时间是 **O(S·len)**，其中 `len` 是我们当前尝试的子路径长度。  
- 空间上我们需要保存每个人的子路径集合，最坏情况下每个子路径都是不同的，数量约为 `S`，所以 **O(S)** 的额外空间。

> 注意：如果直接把 `len` 从大到小线性搜索，最坏会遍历 `len = 1 … max_len`，导致时间复杂度 **O(S·max_len)**，在最坏情况下会达到 `10⁵·10⁵`，远超时间限制。

#### 代码（Python）

```python
from typing import List, Set, Tuple

def longestCommonSubpath_brute(n: int, paths: List[List[int]]) -> int:
    # 所有路径的最小长度，最长公共子路径不可能超过它
    min_len = min(len(p) for p in paths)

    # 从长到短尝试，找到第一个可行的长度即为答案
    for length in range(min_len, 0, -1):
        # 把第一个朋友的所有子路径放进集合 common
        common: Set[Tuple[int, ...]] = set()
        first = paths[0]
        for i in range(len(first) - length + 1):
            common.add(tuple(first[i:i+length]))

        # 与后面的朋友逐个取交集
        for idx in range(1, len(paths)):
            cur_set: Set[Tuple[int, ...]] = set()
            cur = paths[idx]
            for i in range(len(cur) - length + 1):
                cur_set.add(tuple(cur[i:i+length]))
            common &= cur_set           # 只保留公共的子路径
            if not common:              # 已经空了，直接退出当前 length
                break

        if common:                      # 仍有公共子路径，说明 length 可行
            return length

    return 0
```

#### 复杂度

- **时间复杂度**：`O(S · min_len)`  
  这里 `S` 是所有路径长度之和（≤ 10⁵），`min_len` 是最短路径的长度。大白话：我们把每条路的每一个可能起点都检查一次，而且要重复检查多次（因为我们从大到小遍历长度），所以会比较慢。
- **空间复杂度**：`O(S)`  
  需要存放每个人的子路径集合，最坏情况下每个子路径都是唯一的，和总路径长度成正比。

---

### 2. 最优解

#### 思路  

暴力解慢的根源是 **重复枚举子路径**。我们可以把“检查长度 `len` 是否可行”这一步做得更高效，并且把所有可能的 `len` 用 **二分搜索**（binary search）一次性查找。

**二分搜索**的核心思想：  
- 如果长度为 `x` 的公共子路径存在，那么所有 **更短** 的长度 `y < x` 必然也存在（因为可以直接取前 `y` 个城市）。这就是**单调性**，正好满足二分的前提。
- 因此我们可以在 `[0, min_len]` 区间二分，逐步逼近最大可行的长度。

**如何快速判断 “长度为 L 的公共子路径是否存在”**？  
使用 **滚动哈希（Rolling Hash）**（又叫 Rabin‑Karp）：

1. **把子路径映射成整数哈希值**  
   把城市编号看成“字符”，对长度为 `L` 的子路径计算一个唯一的数值 `hash`。  
   - 类比：在字典里查单词时，我们先把单词映射成页码，这个页码就是哈希值。  
   - 计算方式：  
     \[
     H = (a_0·P^{L-1} + a_1·P^{L-2} + … + a_{L-1}) \bmod MOD
     \]  
     其中 `a_i` 是城市编号，`P` 是一个随机的基数（比如 10⁵+7），`MOD` 是一个大素数（防止溢出）。
2. **滚动更新**  
   当窗口从 `[i, i+L-1]` 移到 `[i+1, i+L]` 时，只需要 O(1) 时间把旧的哈希值减去左侧城市的贡献、乘以 `P`、再加上新右侧城市的编号即可。
3. **把每个人的所有长度 L 的哈希值放进集合**，然后对所有朋友取交集。若交集非空，则说明存在公共子路径。

**避免哈希冲突**  
- 单纯使用一个模数仍有极小概率冲突。常用做法是 **双模**：同时计算两个不同 `MOD`（比如 `10⁹+7` 与 `10⁹+9`），把二者组成一个元组 `(h1, h2)` 作为真正的哈希值。冲突概率几乎可以忽略不计。

**整体流程**：

```
low = 0
high = min_len
while low < high:
    mid = (low + high + 1) // 2      # 尝试更大的长度
    if exist_common_subpath_of_len(mid):
        low = mid                    # mid 可行，尝试更大
    else:
        high = mid - 1               # mid 不可行，缩小范围
return low
```

`exist_common_subpath_of_len(L)` 用滚动哈希实现，时间是 **O(S)**（只遍历一次），空间是 **O(S)**（存放每个人的哈希集合），但只在一次二分检查中使用，整体时间是 **O(S·log(min_len))**，完全满足题目约束。

#### 代码（Python）

```python
from typing import List, Set, Tuple

MOD1 = 10 ** 9 + 7
MOD2 = 10 ** 9 + 9
BASE = 100_007          # 随机选取的基数，必须大于城市编号上限 n

def longestCommonSubpath(n: int, paths: List[List[int]]) -> int:
    # 最短路径长度决定二分上界
    min_len = min(len(p) for p in paths)

    # 预先算出每条路径的前缀哈希和幂次，方便 O(1) 取子串哈希
    prefix1 = []   # 每条路径对应的前缀哈希（mod MOD1）
    prefix2 = []   # 每条路径对应的前缀哈希（mod MOD2）
    pow1 = [1] * (min_len + 1)   # BASE^i % MOD1
    pow2 = [1] * (min_len + 1)   # BASE^i % MOD2
    for i in range(1, min_len + 1):
        pow1[i] = (pow1[i-1] * BASE) % MOD1
        pow2[i] = (pow2[i-1] * BASE) % MOD2

    for path in paths:
        h1 = [0] * (len(path) + 1)   # h1[i] = 前 i 个城市的哈希值
        h2 = [0] * (len(path) + 1)
        for i, city in enumerate(path, 1):
            h1[i] = (h1[i-1] * BASE + city) % MOD1
            h2[i] = (h2[i-1] * BASE + city) % MOD2
        prefix1.append(h1)
        prefix2.append(h2)

    # ---------- 判断长度 L 是否存在公共子路径 ----------
    def check(L: int) -> bool:
        if L == 0:
            return True

        common: Set[Tuple[int, int]] = set()
        # 先处理第一条路径，得到所有长度 L 的哈希集合
        h1, h2 = prefix1[0], prefix2[0]
        for i in range(L, len(h1)):
            # 子串 [i-L, i) 的哈希 = h[i] - h[i-L] * BASE^L
            cur1 = (h1[i] - h1[i-L] * pow1[L]) % MOD1
            cur2 = (h2[i] - h2[i-L] * pow2[L]) % MOD2
            common.add((cur1, cur2))

        # 依次和后面的路径取交集
        for idx in range(1, len(paths)):
            cur_set: Set[Tuple[int, int]] = set()
            h1, h2 = prefix1[idx], prefix2[idx]
            for i in range(L, len(h1)):
                cur1 = (h1[i] - h1[i-L] * pow1[L]) % MOD1
                cur2 = (h2[i] - h2[i-L] * pow2[L]) % MOD2
                cur_set.add((cur1, cur2))
            # 只保留在所有路径中都出现的哈希
            common &= cur_set
            if not common:          # 早停，已经没有公共子路径了
                return False
        return bool(common)

    # ---------- 二分搜索 ----------
    lo, hi = 0, min_len
    while lo < hi:
        mid = (lo + hi + 1) // 2   # 向上取整，防止死循环
        if check(mid):
            lo = mid               # mid 可行，尝试更大
        else:
            hi = mid - 1           # mid 不可行，缩小范围
    return lo
```

> **代码要点注释**  
> - `prefix1 / prefix2`：前缀哈希数组，使得任意子串哈希可以 **O(1)** 计算。  
> - `pow1 / pow2`：预先计算 `BASE^L`，避免在循环里每次重复乘。  
> - `check(L)`：先把第一个朋友的所有长度 `L` 子路径哈希放进 `common`，随后逐个取交集。若交集为空直接返回 `False`，实现**提前剪枝**。  
> - 二分的 `mid` 采用上取整 `(lo+hi+1)//2`，可以保证区间收敛。

#### 复杂度

- **时间复杂度**：`O(S·log(min_len))`  
  - `check(L)` 只遍历所有路径一次，时间 `O(S)`。  
  - 二分最多进行 `log₂(min_len)`（约 17 次，因为 `min_len ≤ 10⁵`）检查。  
  - 大白话：我们把所有城市只看 **几次**（十几次），每次都像在做一次快速扫描，所以很快。

- **空间复杂度**：`O(S)`  
  - 需要保存每条路径的前缀哈希（两套）以及 `pow` 数组，规模和所有城市数相同。  
  - 交集 `common` 最多也只会保存 `S` 条哈希值。

---

## 心得

- **核心技巧**：二分搜索 + 滚动哈希（双模防冲突）  
  通过把“是否存在公共子路径”抽象成一个**单调判定函数**，再用二分快速定位最大可行长度；滚动哈希让我们在 O(1) 时间内比较两个子路径是否相同，避免了暴力枚举的 O(L) 比较。

- **适用的题型**  
  1. “最长公共子串 / 子数组” 的多序列版（如 LeetCode 718、拼图类问题）。  
  2. “数组/字符串中是否存在长度为 K 的重复子序列” 类问题（如 DNA 重复序列）。  
  3. “在多条路径/序列中找公共区间” 的变体（如最长公共子序列的变形）。

- **一句话总结**：**二分 + 双模滚动哈希** 是寻找多序列公共子段的“钥匙”，既保证了单调性，又让判定一步到位。

---

## 反思

- **第一反应**：直接把所有子路径列出来，用集合交集找公共的，代码容易写，但很慢。  
- **最容易踩的坑**  
  1. **哈希冲突**：只用单个模数可能导致错误的“存在”，使用双模或更大的模数可以几乎消除冲突。  
  2. **负数取模**：Python 的 `%` 已经把负数转成正数，但在手动计算 `(a - b * pow) % MOD` 时一定要加上 `MOD` 再取模，防止出现负数。  
  3. **边界条件**：长度为 0 的子路径始终存在，二分时要把 `mid` 向上取整防止死循环。  
  4. **指数溢出**：使用 `pow` 数组预先存储 `BASE^L % MOD`，否则每次乘法会很慢甚至溢出。

- **下次遇到同类题**：  
  1. **先判断是否有单调性**（长度增大是否更难满足）。  
  2. **把判定函数实现为 O(总长度)**（滚动哈希或前缀和），而不是 O(长度²)。  
  3. **使用二分定位答案**，把搜索空间从线性压到对数。  

这样思路更清晰，代码也更高效。祝你玩转算法！