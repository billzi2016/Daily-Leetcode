# #1247. 使字符串相等的最小交换次数 / Minimum Swaps to Make Strings Equal

> 难度：中等 · 标签：Math、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-swaps-to-make-strings-equal/)

---

## 题目（英文原版）

**Description**

You are given two strings s1 and s2 of equal length consisting of letters "x" and "y" only. Your task is to make these two strings equal to each other. You can swap any two characters that belong to different strings, which means: swap s1[i] and s2[j].
Return the minimum number of swaps required to make s1 and s2 equal, or return -1 if it is impossible to do so.

**Examples**

**Example 1:**

```
Input: s1 = "xx", s2 = "yy"
Output: 1
Explanation: Swap s1[0] and s2[1], s1 = "yx", s2 = "yx".
```

**Example 2:**

```
Input: s1 = "xy", s2 = "yx"
Output: 2
Explanation: Swap s1[0] and s2[0], s1 = "yy", s2 = "xx".
Swap s1[0] and s2[1], s1 = "xy", s2 = "xy".
Note that you cannot swap s1[0] and s1[1] to make s1 equal to "yx", cause we can only swap chars in different strings.
```

**Example 3:**

```
Input: s1 = "xx", s2 = "xy"
Output: -1
```

**Constraints**

- 1 <= s1.length, s2.length <= 1000
- s1.length == s2.length
- s1, s2 only contain 'x' or 'y'.

---

## 题目（中文翻译）

给定两个等长字符串 `s1` 和 `s2`，它们仅由字符 `'x'` 和 `'y'` 组成。你的任务是通过交换字符使这两个字符串相等。一次 **交换（swap）** 指的是选取两个字符分别来自不同的字符串，即交换 `s1[i]` 与 `s2[j]`。  

返回使 `s1` 与 `s2` 相等所需的最少交换次数；如果无法实现，则返回 `-1`。

**示例 1**  
**输入**: `s1 = "xx", s2 = "yy"`  
**输出**: `1`  
**解释**: 交换 `s1[0]` 与 `s2[1]`，此后 `s1 = "yx", s2 = "yx"`。

**示例 2**  
**输入**: `s1 = "xy", s2 = "yx"`  
**输出**: `2`  
**解释**:  
1. 交换 `s1[0]` 与 `s2[0]`，得到 `s1 = "yy", s2 = "xx"`。  
2. 再交换 `s1[0]` 与 `s2[1]`，得到 `s1 = "xy", s2 = "xy"`。  

注意，不能交换 `s1[0]` 与 `s1[1]` 来使 `s1` 变为 `"yx"`，因为只能在不同的字符串之间进行 **交换**。

**示例 3**  
**输入**: `s1 = "xx", s2 = "xy"`  
**输出**: `-1`

**约束条件**  
- `1 <= s1.length, s2.length <= 1000`  
- `s1.length == s2.length`  
- `s1`、`s2` 只包含字符 `'x'` 或 `'y'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可以交换的字符都试一遍，看看哪一次能把两串变得相等。  
具体做法：

1. 先遍历两个字符串，找到所有不相等的位置 `i`（即 `s1[i] != s2[i]`）。  
2. 对每一对不相等的位置 `i`，尝试把 `s1[i]` 和 `s2[j]`（`j` 也是不相等的位置）交换一次。  
3. 交换后检查两串是否已经完全相同；如果相同，就记录下这一次用了几次交换。  
4. 把这一次的交换撤销（恢复原样），继续尝试其它 `i, j` 的组合。  
5. 所有组合都尝试完，取最小的交换次数；如果没有任何一次能够成功，则返回 `-1`。

> **类比**：想象你有两列相同长度的磁带，上面只写了 `x`、`y` 两种字符。现在你只能把两列磁带上 **不同列** 的磁带块互相换位。暴力做法就像是把每一块磁带块都搬来搬去，尝试所有可能的搬运方式，看看哪一种能让两列磁带完全相同。

**为什么这个方法一定能得到答案？**  
因为我们把所有合法的交换顺序都穷举了，只要存在一种可以使两串相等的交换序列，暴力搜索必然会在某一步发现它。

**时间/空间分析**  
- 假设不相等的位置有 `k`（`k ≤ n`，`n` 为字符串长度）。  
- 我们要枚举所有 `i, j` 的组合，最多是 `k²` 种；每一次尝试后要检查两串是否相等，需要 `O(n)` 的时间。  
- 因此最坏情况下的时间复杂度是 **O(k²·n) ≤ O(n³)**。  
- 只使用了常数级别的额外空间（几个临时变量），所以空间复杂度是 **O(1)**。

> **大白话**：`O(n³)` 可以想象成“如果字符串长度是 100，最坏要做 1,000,000 次左右的操作”，对电脑来说已经算是慢了。

#### 代码（Python）

```python
def minSwap_bruteforce(s1: str, s2: str) -> int:
    # 把字符串转成列表，方便原地修改
    a, b = list(s1), list(s2)
    n = len(a)

    # 找出所有不相等的位置
    diff_idx = [i for i in range(n) if a[i] != b[i]]
    k = len(diff_idx)

    # 如果已经相等，直接返回 0
    if k == 0:
        return 0

    # 暴力尝试所有交换组合
    INF = float('inf')
    best = INF

    # 递归搜索所有可能的交换序列
    def dfs(start: int, swaps: int):
        nonlocal best
        # 剪枝：已经超过当前最优解，就不继续搜索了
        if swaps >= best:
            return
        # 若所有位置都已经匹配，更新最优解
        if all(a[i] == b[i] for i in range(n)):
            best = swaps
            return
        # 从 start 开始找第一个仍不匹配的位置 i
        for i in range(start, n):
            if a[i] != b[i]:
                break
        else:
            return  # 全部匹配，已在上面处理

        # 把 i 与后面的每个 j（j>i 且仍不匹配）尝试交换
        for j in range(i + 1, n):
            if a[j] != b[j]:
                # 只允许跨字符串交换：a[i] ↔ b[j] 或 b[i] ↔ a[j]
                # 情况 1：把 a[i] 换到 b[j]
                a[i], b[j] = b[j], a[i]
                dfs(i + 1, swaps + 1)
                a[i], b[j] = b[j], a[i]  # 恢复

                # 情况 2：把 b[i] 换到 a[j]
                b[i], a[j] = a[j], b[i]
                dfs(i + 1, swaps + 1)
                b[i], a[j] = a[j], b[i]  # 恢复

                # 只需要尝试一次就可以，因为后面的递归会继续处理剩余的不匹配
                break

    dfs(0, 0)
    return -1 if best == INF else best
```

> 代码里用了递归深度优先搜索（DFS）来遍历所有合法的交换顺序。每一次交换后都检查是否已经全部相等，若是则更新最小交换次数。

#### 复杂度

- **时间复杂度**：`O(n³)` —— 最坏情况下要尝试 `n²` 种交换组合，每种组合检查一次完整的字符串（`O(n)`）。
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量（递归栈的深度最多 `n`，在本题 `n ≤ 1000`，仍算作常数级别的额外空间）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有交换顺序**，而实际只需要关注 **不匹配的字符类型**，不必真的去执行每一次交换。  
把每个位置的 `(s1[i], s2[i])` 看成一对：

| s1[i] | s2[i] | 记号 |
|------|------|------|
| x    | x    | 已匹配 |
| y    | y    | 已匹配 |
| x    | y    | **xy**（记作一种不匹配） |
| y    | x    | **yx**（记作另一种不匹配） |

只要把所有 **xy** 和 **yx** 配对好，就能让两串相等。配对的方式有两种：

1. **同类配对**：`xy` 与 `xy`（或 `yx` 与 `yx`）  
   - 把其中一个 `x` 与另一个 `y` 交换，一次交换即可解决这两个位置。  
   - 需要 `cnt_xy // 2`（或 `cnt_yx // 2`）次交换。

2. **异类配对**：剩下的 `xy` 与 `yx`（各剩一个）  
   - 这时只能先把其中一个字符换到同类位置，再再换一次才能完成。  
   - 需要 **2 次** 交换来消除这对剩余的不匹配。

于是只要统计 `cnt_xy`（出现的 `xy` 对数）和 `cnt_yx`（出现的 `yx` 对数），答案就可以直接算出来：

```
 swaps = cnt_xy // 2 + cnt_yx // 2          # 同类配对的次数
 swaps += 2 * (cnt_xy % 2)                 # 如果剩下奇数个，则需要两次额外交换
```

> **为什么会出现“奇数个”这种情况？**  
> 因为每一次同类配对会消掉 **两个** 不匹配，如果 `cnt_xy` 和 `cnt_yx` 都是偶数，所有不匹配都能两两配对完毕；如果两者都是奇数，则会剩下 **各一个** `xy` 和 `yx`，这正是上面说的“异类配对”，需要两次额外交换。  
> 如果只有一个奇数（比如 `cnt_xy` 为奇数、`cnt_yx` 为偶数），说明整体不匹配字符总数是奇数，此时根本不可能把两串变得相同，返回 `-1`。

> **类比**：把不匹配的字符想成“袜子”。`xy` 像是一只左脚的袜子，`yx` 像是一只右脚的袜子。我们想把左脚袜子和左脚袜子配成一双（一次换位），右脚同理。如果剩下的只有一只左脚和一只右脚，那只能先把左脚袜子换到右脚位置，再再换回来——相当于两次换位。

#### 代码（Python）

```python
def minSwap(s1: str, s2: str) -> int:
    """
    返回将 s1、s2 通过跨字符串交换后相等所需的最少交换次数。
    若不可能则返回 -1。
    """
    cnt_xy = cnt_yx = 0   # 分别统计 "xy" 与 "yx" 的出现次数

    for a, b in zip(s1, s2):
        if a == b:
            continue          # 已匹配的位子直接跳过
        if a == 'x' and b == 'y':
            cnt_xy += 1
        else:                 # a == 'y' and b == 'x'
            cnt_yx += 1

    # 总的不匹配字符数必须为偶数，否则不可能配对完毕
    if (cnt_xy + cnt_yx) % 2 == 1:
        return -1

    # 同类配对各自可以直接消掉一半
    swaps = cnt_xy // 2 + cnt_yx // 2

    # 如果还有剩余（即 cnt_xy、cnt_yx 均为奇数），需要两次额外交换
    if cnt_xy % 2 == 1:          # 此时 cnt_yx % 2 也一定是 1
        swaps += 2

    return swaps
```

> **代码说明**  
> - `zip(s1, s2)` 同时遍历两个字符串的对应字符。  
> - 只统计不相等的两种情况 (`xy` 与 `yx`)；已匹配的直接跳过，省时省力。  
> - 第一步的奇偶性判断是“不可达”的根本原因：每次跨字符串交换会改变两对字符的种类，总的不匹配数必须是偶数才能全部配对。  
> - 最后根据公式计算最少交换次数，整个过程只需要一次遍历，时间复杂度是线性的。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只需一次遍历字符串，`n` 为长度（最多 1000），对每个字符做常数次操作。  
  - 与暴力解的 `O(n³)` 相比，快了 **n²** 倍以上，几乎瞬间得到答案。
- **空间复杂度**：`O(1)` —— 只用了几个计数器，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：把问题抽象成「不匹配的字符对」并计数，用「配对」的思想求最小操作数。  
- **适用的题型**  
  1. `LeetCode 1247 – Minimum Swaps to Make Strings Equal`（本题）  
  2. `LeetCode 1650 – Lowest Common Ancestor of a Binary Tree III`（利用配对计数的思路）  
  3. `LeetCode 1055 – Shortest Way to Form String`（同样把字符需求转化为计数问题）  
- **一句话总结解题钥匙**：**先把“相同位置不同字符”抽出来统计，剩下的配对问题用数学公式直接算**。

---

## 反思

- **第一反应**：看到只能跨字符串交换，立刻想到把所有可能的交换都枚举（暴力搜索）。  
- **最容易踩的坑**  
  - 忘记检查 **奇偶性**：如果不匹配的总数是奇数，答案一定是 `-1`。  
  - 把 `xy` 与 `yx` 混在一起计数，导致公式写错。  
  - 边界情况：全相等的字符串应该直接返回 `0`，而不是继续计算。  
- **下次遇到同类题**，第一步应该 **把“不同位置的字符差异”抽象成计数问题**，再判断是否满足配对的必要条件（奇偶性），最后用公式求最小操作数。