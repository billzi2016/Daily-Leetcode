# #3443. K 次修改后最大曼哈顿距离 / Maximum Manhattan Distance After K Changes

> 难度：中等 · 标签：Hash Table、Math、String、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-manhattan-distance-after-k-changes/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of the characters 'N', 'S', 'E', and 'W', where s[i] indicates movements in an infinite grid:
Initially, you are at the origin (0, 0). You can change at most k characters to any of the four directions.
Find the maximum Manhattan distance from the origin that can be achieved at any time while performing the movements in order.

**Examples**

**Example 1:**

```
Input: s = "NWSE", k = 1
Output: 3
Explanation:
Change s[2] from 'S' to 'N' . The string s becomes "NWNE" .
The maximum Manhattan distance from the origin that can be achieved is 3. Hence, 3 is the output.
```

**Example 2:**

```
Input: s = "NSWWEW", k = 3
Output: 6
Explanation:
Change s[1] from 'S' to 'N' , and s[4] from 'E' to 'W' . The string s becomes "NNWWWW" .
The maximum Manhattan distance from the origin that can be achieved is 6. Hence, 6 is the output.
```

**Constraints**

- 1 <= s.length <= 105
- 0 <= k <= s.length
- s consists of only 'N', 'S', 'E', and 'W'.

---

## 题目（中文翻译）

你得到一个仅包含字符 `'N'`、`'S'`、`'E'`、`'W'` 的字符串 `s`，其中 `s[i]` 表示在一个无限网格（infinite grid）中的一次移动：

- 初始时，你位于原点（origin） `(0, 0)`。
- 你最多可以将至多 `k` 个字符改成四个方向中的任意一个。

求在按照字符串顺序执行所有移动的过程中，能够达到的**最大曼哈顿距离（Manhattan distance）**（即 `|x| + |y|`）是多少。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  

**示例 1**  
```
Input: s = "NWSE", k = 1
Output: 3
```
**解释**：  
将 `s[2]` 从 `'S'` 改为 `'N'`，得到字符串 `"NWNE"`。  
在执行该序列的过程中，能够达到的最大曼哈顿距离为 `3`，因此输出 `3`。

**示例 2**  
```
Input: s = "NSWWEW", k = 3
Output: 6
```
**解释**：  
将 `s[1]` 从 `'S'` 改为 `'N'`，并将 `s[4]` 从 `'E'` 改为 `'W'`，得到字符串 `"NNWWWW"`。  
在执行该序列的过程中，能够达到的最大曼哈顿距离为 `6`，因此输出 `6`。

**约束条件**  
- `1 <= s.length <= 10^5`
- `0 <= k <= s.length`
- `s` 仅由字符 `'N'`、`'S'`、`'E'`、`'W'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的修改方式**，然后逐步模拟走路，记录每一步的曼哈顿距离（`|x| + |y|`），取最大值。  

- **数据结构**：我们只需要一个二维坐标 `(x, y)`，它就像是「地图上的你」；  
  记录已经走过的每一步可以用一个列表 `positions`（相当于把每一步的坐标写在纸上），  
  用哈希表（Python 的 `dict`）可以把每个字符的下标映射到它的方向，类似于查字典：  
  `{'N': (0,1), 'S': (0,-1), 'E': (1,0), 'W': (-1,0)}`。  

- **为什么正确**：因为我们把「所有可能的改动」都遍历了一遍，必然会包含最优的改动方案，随后按照顺序执行得到的每一步坐标自然也就包含了最大曼哈顿距离。  

- **复杂度分析**：  
  - **枚举改动**：最多可以把 `k` 个字符改成 4 种方向中的任意一种，组合数是 `C(n,0)*4^0 + C(n,1)*4^1 + … + C(n,k)*4^k`，在最坏情况下接近 `O(4^k * n^k)`，随 `k` 指数增长。  
  - **模拟走路**：每一种改动都要遍历整条字符串，时间 `O(n)`。  
  - **总时间**：暴力的时间复杂度约为 **指数级** `O(4^k * n)`，当 `k` 甚至只有 10 时已经不可接受。  
  - **空间**：我们需要保存一次完整的坐标序列，`O(n)`。  

> **大白话解释**：`O(4^k)` 就像说「把一块巧克力分成 `k` 层，每层有 4 种口味」——口味数随层数指数增长，几层下来就吃不完了。  

#### 代码（Python）  

```python
from itertools import product, combinations
from typing import List, Tuple

# 方向对应的坐标增量，类似查字典：key 是字符，value 是 (dx, dy)
DIR = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
ALL_DIR = ['N', 'S', 'E', 'W']

def simulate(s: str) -> int:
    """遍历字符串，返回最大曼哈顿距离"""
    x = y = 0
    best = 0
    for ch in s:
        dx, dy = DIR[ch]
        x += dx
        y += dy
        best = max(best, abs(x) + abs(y))
    return best

def brute_max_distance(s: str, k: int) -> int:
    n = len(s)
    best = 0

    # 先把所有「可以改动的下标」的组合枚举出来
    for cnt in range(k + 1):                     # 改动多少个字符
        for idxs in combinations(range(n), cnt):  # 选哪些下标
            # 对这些下标上的字符，尝试所有 4 种方向的组合
            for new_dirs in product(ALL_DIR, repeat=cnt):
                lst = list(s)                    # 把字符串转成列表，方便修改
                for pos, nd in zip(idxs, new_dirs):
                    lst[pos] = nd                # 把选中的字符改成新方向
                cur = simulate(''.join(lst))    # 走一遍，算最大距离
                best = max(best, cur)

    return best
```

> 这段代码可以直接跑，但只能在 `len(s) ≤ 10`、`k ≤ 5` 之类的小数据上通过。

#### 复杂度  

- **时间复杂度**：`O(4^k * n)`（指数级），因为我们要尝试 `4^k` 种改动方式，每种方式都要遍历整条路径 `n` 步。  
- **空间复杂度**：`O(n)`，主要是保存临时的字符串副本以及坐标序列。  

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于**枚举所有改动的组合**。实际上，我们不需要真的去改每一个字符，只要知道**每一步最多能把距离提升多少**即可。  

观察曼哈顿距离的定义：

```
|x| + |y| = max( ( x + y ), ( x - y ), (-x + y), (-x - y) )
```

这四个表达式对应四个象限的“向右上、左上、右下、左下”。  
如果我们决定把最终的距离放在某个象限（比如右上象限 NE），那么我们只需要最大化 `x + y`，其余的符号自然会被忽略。

> **类比**：把坐标系想成四条路口的指示牌，想要离原点最远，只需要往其中一条路走得最远即可。

---

#### 2.1 把问题转化为“线性组合”

以 **NE（x≥0, y≥0）** 为例：

```
x + y = (E - W) + (N - S) = (E + N) - (W + S)
```

- `E`、`N` 本身已经让我们往右/上走，算作“好”贡献。  
- `W`、`S` 把我们往左/下拉，算作“坏”贡献。  

我们可以把每个字符的**潜在收益**写成表格（相对于 NE）：

| 原字符 | 改成什么可以提升多少 | 最大提升 |
|--------|---------------------|----------|
| `W`    | 改成 `E`（+1 x）   | **+2**（从 -1 变 +1） |
| `S`    | 改成 `N`（+1 y）   | **+2** |
| `N`    | 改成 `E`（+1 x）   | **+1** |
| `E`    | 改成 `N`（+1 y）   | **+1** |

所以每一步都有三种可能的**增益**：`0`（不改）、`+1`、`+2`。  
我们最多可以改 `k` 步，显然应该优先把**增益为 2 的字符**改掉，然后才是增益为 1 的字符。

---

#### 2.2 前缀统计 + 贪心求最大增益  

在遍历字符串的过程中，维护四个计数：

```
cntN, cntS, cntE, cntW   // 已经走过的字符各有多少
```

对每个前缀（即走到当前位置时）：

1. **当前基准距离**（不改任何字符）  
   `base = (cntE - cntW) + (cntN - cntS)`  

2. **可以得到的增益**  
   - `gain2 = cntW + cntS`（每个 W/S 改成对应的好方向可得 +2）  
   - `gain1 = cntN + cntE`（每个 N/E 再改一次可得 +1）  

3. **把最多 `k` 次改动分配给增益最大的字符**（贪心）  

```
use2 = min(k, gain2)                # 用多少次 +2
remain = k - use2
use1 = min(remain, gain1)           # 剩余的改动只能拿 +1
extra = use2 * 2 + use1 * 1
total_NE = base + extra
```

对 **NW、SE、SW** 四个象限同理，只是基准公式和增益表会变化（比如 NW 用 `x - y = (E - W) - (N - S)`）。  

遍历完整个字符串，取四个象限的最大 `total` 即为答案。

> **为什么贪心是最优的？**  
> 每一步的增益只能是 `0/1/2`，且 **更大的增益永远不劣于把同一次改动用在小增益上**。因此先用掉所有 `+2` 再用 `+1` 完全不可能错过更大的总和，这正是贪心的核心。

---

#### 2.3 复杂度  

- **时间**：我们只遍历一次字符串，四次常数操作 → **O(n)**。  
- **空间**：只需要几个计数器 → **O(1)**。  

相比暴力的指数级，这相当于把“把巧克力切成 4^k 块”变成了“一口气吃完”。  

---

#### 代码（Python）  

```python
from typing import List

# 方向对应的坐标增量，方便后面统计
DIR = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}

def max_distance_after_k_changes(s: str, k: int) -> int:
    """
    计算在至多修改 k 个字符后，执行路径时能够达到的最大曼哈顿距离。
    思路：枚举四个象限，使用前缀计数 + 贪心分配增益。
    """
    # 四个计数，分别统计已经出现的 N,S,E,W 的个数
    cntN = cntS = cntE = cntW = 0
    ans = 0                     # 最终答案

    for ch in s:
        # 先更新计数
        if ch == 'N':
            cntN += 1
        elif ch == 'S':
            cntS += 1
        elif ch == 'E':
            cntE += 1
        else:  # 'W'
            cntW += 1

        # ---------- 1️⃣ NE 方向（x≥0, y≥0） ----------
        base_ne = (cntE - cntW) + (cntN - cntS)          # 不改的基准距离
        gain2_ne = cntW + cntS                          # W / S 改成好方向可得 +2
        gain1_ne = cntN + cntE                          # N / E 再改一次可得 +1
        use2 = min(k, gain2_ne)
        use1 = min(k - use2, gain1_ne)
        total_ne = base_ne + use2 * 2 + use1 * 1
        ans = max(ans, total_ne)

        # ---------- 2️⃣ NW 方向（x≤0, y≥0） ----------
        # 对应的线性组合是  x - y = (E - W) - (N - S)
        base_nw = (cntE - cntW) - (cntN - cntS)
        # 在 NW 中，W、N 是好方向（因为 x 需要负，y 需要正）
        gain2_nw = cntE + cntS          # 把 E 改成 W / 把 S 改成 N，+2
        gain1_nw = cntW + cntN          # 把 W 再改成 N / 把 N 再改成 W，+1
        use2 = min(k, gain2_nw)
        use1 = min(k - use2, gain1_nw)
        total_nw = base_nw + use2 * 2 + use1 * 1
        ans = max(ans, total_nw)

        # ---------- 3️⃣ SE 方向（x≥0, y≤0） ----------
        # 线性组合  -x + y = (W - E) + (N - S)
        base_se = (cntW - cntE) + (cntN - cntS)
        gain2_se = cntE + cntS          # 把 E 改成 W / 把 S 改成 N，+2
        gain1_se = cntW + cntN          # 把 W 再改成 N / 把 N 再改成 E，+1
        use2 = min(k, gain2_se)
        use1 = min(k - use2, gain1_se)
        total_se = base_se + use2 * 2 + use1 * 1
        ans = max(ans, total_se)

        # ---------- 4️⃣ SW 方向（x≤0, y≤0） ----------
        # 线性组合  -x - y = (W - E) - (N - S)
        base_sw = (cntW - cntE) - (cntN - cntS)
        gain2_sw = cntE + cntN          # 把 E 改成 W / 把 N 改成 S，+2
        gain1_sw = cntW + cntS          # 把 W 再改成 S / 把 S 再改成 W，+1
        use2 = min(k, gain2_sw)
        use1 = min(k - use2, gain1_sw)
        total_sw = base_sw + use2 * 2 + use1 * 1
        ans = max(ans, total_sw)

    return ans
```

> **代码要点注释**  
> - 第 1~4 行维护四个计数，像「记录每种颜色的积木有多少」；  
> - 对每个前缀分别计算四个象限的**基准距离** `base_??`，以及**可以拿到的 +2、+1 增益**；  
> - `use2`、`use1` 用 **贪心** 把改动分配给最有价值的字符；  
> - 最后取四个方向的最大值即为答案。  

---

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次字符串，四次常数运算。  
- **空间复杂度**：`O(1)`，只用到几个整数计数器。  

与暴力解的指数级相比，提升了 **数十万倍**，可以轻松处理 `n = 10^5` 的大数据。

---

## 心得  

- **核心技巧**：把曼哈顿距离拆成四个线性组合，固定象限后只需最大化一个一次函数。  
- **适用场景**：  
  1. 需要在网格上「最多改 K 步」的最远/最近问题（如「Maximum Euclidean Distance After K Changes」）。  
  2. 任何涉及「把字符改成四种方向」并求最值的题目，都可以用「前缀计数 + 贪心增益」的思路。  
- **一句话总结**：**把目标拆成「每一步的增益」并把改动分配给增益最大的步，贪心即最优**。

---

## 反思  

- **第一反应**：先想到枚举所有改动——这在小样例上能跑通，却忽视了规模。  
- **最容易踩的坑**：  
  - 忘记 **四个象限** 必须都检查，否则可能漏掉真正的最大距离。  
  - 计算增益时把 `+2` 当成 `+1`，导致答案偏小。  
  - 边界情况 `k = 0`（不能改）或 `k >= len(s)`（可以把所有字符改成同一个方向），需要单独验证。  
- **下次第一步**：先把曼哈顿距离写成四个线性组合，思考「在固定象限下，每一步能带来多少增益」——这一步往往能直接得到 O(n) 的解法。