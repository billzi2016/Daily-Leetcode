# #3186. 最大总伤害 / Maximum Total Damage With Spell Casting

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、Binary Search、Dynamic Programming、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/maximum-total-damage-with-spell-casting/)

---

## 题目（英文原版）

**Description**

A magician has various spells.
You are given an array power, where each element represents the damage of a spell. Multiple spells can have the same damage value.
It is a known fact that if a magician decides to cast a spell with a damage of power[i], they cannot cast any spell with a damage of power[i] - 2, power[i] - 1, power[i] + 1, or power[i] + 2.
Each spell can be cast only once.
Return the maximum possible total damage that a magician can cast.

**Examples**

**Example 1:**

```
Input: power = [1,1,3,4]
Output: 6
Explanation:
The maximum possible damage of 6 is produced by casting spells 0, 1, 3 with damage 1, 1, 4.
```

**Example 2:**

```
Input: power = [7,1,6,6]
Output: 13
Explanation:
The maximum possible damage of 13 is produced by casting spells 1, 2, 3 with damage 1, 6, 6.
```

**Constraints**

- 1 <= power.length <= 105
- 1 <= power[i] <= 109

---

## 题目（中文翻译）

描述  
一名魔法师拥有各种咒语。  
给定一个数组 `power`，其中每个元素表示一个咒语的伤害值。不同的咒语可能具有相同的伤害值。  
已知如果魔法师决定施放伤害为 `power[i]` 的咒语，则他 **不能** 再施放伤害为 `power[i] - 2`、`power[i] - 1`、`power[i] + 1` 或 `power[i] + 2` 的任何咒语。  
每个咒语只能施放一次。  
返回魔法师能够施放的 **最大可能的总伤害**。

示例  

示例 1  
```text
Input: power = [1,1,3,4]
Output: 6
Explanation:
通过施放下标为 0、1、3 的咒语（伤害分别为 1、1、4），可以得到最大总伤害 6。
```

示例 2  
```text
Input: power = [7,1,6,6]
Output: 13
Explanation:
通过施放下标为 1、2、3 的咒语（伤害分别为 1、6、6），可以得到最大总伤害 13。
```

约束条件  
- `1 <= power.length <= 10^5`  
- `1 <= power[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的施法组合**，把每一种组合的总伤害算出来，挑出最大的那一个。  

- **数据结构**：可以把 `power` 看成一堆“牌”。每张牌上写着它的伤害值。我们要从这些牌里挑出若干张，使得任意两张牌的伤害差不小于 3（因为相差 1、2 都会被禁用）。  
- **为什么正确**：只要遍历到了所有合法的子集合，最大值一定会在其中。也就是说，穷举没有遗漏，答案自然正确。  
- **时间/空间复杂度**：  
  - 设 `n = len(power)`。每张牌有“选”或“不选”两种可能，所以所有子集合的数量是 `2^n`，这就是指数级的增长。  
  - 空间方面只需要保存递归栈或临时集合，最多 `O(n)`。  
  - 用大白话说，`O(2^n)` 就像在每一步都要翻开一本“选择树”，树的深度是 `n`，每层都有两个分支，枝杈会很快把所有可能撑爆，`n` 只要大于 20，计算机就吃不消了。

> **结论**：暴力解只能在 `n` 极小（比如 ≤ 15）时才算得起，根本不适用于本题的上限 `10^5`。

#### 代码（Python）

```python
from itertools import combinations

def max_damage_bruteforce(power):
    n = len(power)
    best = 0
    # 枚举子集合的大小，从 0 到 n
    for k in range(n + 1):
        for idxs in combinations(range(n), k):          # 选出 k 张牌的下标
            ok = True
            total = 0
            # 检查是否有冲突
            for i in range(k):
                for j in range(i + 1, k):
                    if abs(power[idxs[i]] - power[idxs[j]]) <= 2:
                        ok = False
                        break
                if not ok:
                    break
                total += power[idxs[i]]
            if ok:
                best = max(best, total)
    return best
```

> 这段代码只能在 **极小** 的输入下跑通，实际提交会 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O(2^n * n^2)`  
  - `2^n` 来自所有子集合的数量，`n^2` 来自每次检查冲突的两层循环。  
  - 用口语解释，就是“每一种可能的选法都要花 n² 的时间去确认是否合法”。  
- **空间复杂度**：`O(n)`  
  - 主要是递归/迭代时保存的临时下标列表。

---

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们发现瓶颈在于**重复检查相同伤害值的冲突**，以及**指数级的枚举**。  
实际上，题目只关心 **伤害值**，而不是具体是哪一张牌。相同伤害的牌完全等价：如果决定使用伤害为 `x` 的牌，那么**所有**伤害为 `x` 的牌都可以一起使用（因为它们之间的差为 0，满足 “不冲突” 的条件），并且 **不使用** 伤害为 `x` 的牌时，才可能去考虑 `x±1`、`x±2` 的牌。

因此可以把原始数组压缩成：

| 伤害值 `v` | 该伤害出现的次数 `cnt[v]` | 总伤害贡献 `v * cnt[v]` |
|-----------|---------------------------|--------------------------|

接下来把所有出现过的 **唯一伤害值** 排序，记为 `vals = [v1, v2, …, vm]`（`m ≤ n`），对应的贡献记为 `gain[i] = vals[i] * cnt[vals[i]]`。

现在问题变成：**在这条有序的数轴上挑选若干个点**，如果挑选了 `vals[i]`，则必须 **跳过** 与之距离 ≤ 2 的点（即 `vals[i-1]`、`vals[i-2]` 只要满足 `vals[i] - vals[j] ≤ 2`）。这正好是**经典的“删除并获得”（Delete and Earn）**的变形，只是间距从 1 变成了 2。

这可以用 **动态规划** 线性求解：

- `dp[i]` 表示**考虑到第 `i`（含）个唯一伤害值时，能够得到的最大总伤害**。
- 对于第 `i` 个值 `vals[i]`，有两种选择：
  1. **不选**它 → `dp[i] = dp[i-1]`（直接继承前面的最优）。
  2. **选**它 → 必须把所有与之冲突的前面的值排除。因为数组已排序，只要找出最近的 **不冲突** 的下标 `pre`（满足 `vals[i] - vals[pre] > 2`），则 `dp[i] = gain[i] + dp[pre]`（如果 `pre` 为 `-1`，表示前面没有可以兼容的，直接取 `gain[i]`）。

找 `pre` 的过程可以 **二分搜索**（因为 `vals` 已排好序），时间是 `O(log m)`；也可以用双指针一次遍历得到 `O(m)`。这里用双指针更简洁。

**伪代码**（双指针版）：

```
sort vals
pre = -1               # 指向当前 i 能兼容的最右边的下标
for i from 0 to m-1:
    while vals[i] - vals[pre+1] > 2:
        pre += 1       # 前移 pre，保持 pre 与 i 之间的距离 > 2
    take = gain[i] + (dp[pre] if pre >= 0 else 0)
    not_take = dp[i-1] if i > 0 else 0
    dp[i] = max(take, not_take)
return dp[m-1]
```

这样只遍历一次 `vals`，时间 `O(m log m)`（排序）+ `O(m)`（DP），空间 `O(m)`。

#### 代码（Python）

```python
from collections import Counter

def maxDamage(power):
    """
    返回在满足相邻伤害差 >= 3 的前提下，能够获得的最大总伤害。
    思路：先统计每个伤害值出现的次数 → 排序唯一伤害 → DP（类似 Delete and Earn）
    """
    # 1. 统计每个伤害值出现的次数
    cnt = Counter(power)                 # 哈希表：key=伤害值，value=出现次数
    # 2. 把出现过的伤害值取出来并排序
    vals = sorted(cnt.keys())             # 类似把字典的“词条”排成字典序
    m = len(vals)

    # 3. 预先算好每个伤害值如果全部使用可以得到的总伤害
    gain = [v * cnt[v] for v in vals]     # 例如 v=4, 出现 3 次 → 4*3=12

    # 4. 动态规划数组
    dp = [0] * m
    # 双指针：pre 指向当前 i 可以兼容的最右下标（即与 i 的差 > 2）
    pre = -1
    for i in range(m):
        # 前移 pre，直到不满足 “vals[i] - vals[pre+1] > 2” 为止
        while pre + 1 < i and vals[i] - vals[pre + 1] > 2:
            pre += 1

        # 选 i：gain[i] + dp[pre]（如果 pre==-1 则没有前缀可加）
        take = gain[i] + (dp[pre] if pre >= 0 else 0)

        # 不选 i：沿用前一个的最优解
        not_take = dp[i - 1] if i > 0 else 0

        dp[i] = max(take, not_take)      # 取两者最大

    return dp[-1]                         # 最后一个即为整体最优
```

> 代码已在本地通过示例测试，时间复杂度约 `O(n log n)`，可轻松处理 `10^5` 规模的数据。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - `O(n)` 用来统计出现次数（哈希表遍历）。  
  - `O(m log m)`（`m ≤ n`）是对唯一伤害值排序的代价。  
  - DP 只需一次线性遍历 `O(m)`。  
  - 用口语说，就是“先把所有牌按伤害排好序（花点时间），然后顺着排好的顺序一次走完就能算出答案”。比暴力的指数级快了 **天文倍数**。  

- **空间复杂度**：`O(m)`  
  - 需要存放计数哈希表、排序后的唯一值数组、每个值的总贡献以及 DP 表。  
  - 相当于只保存“每种伤害的总分”和“到当前位置的最佳分数”，不需要保存所有子集合。

---

## 心得  

- **核心技巧**：把“相邻伤害冲突”转化为“在数轴上挑选间距 ≥ 3 的点”，进而使用 **排序 + 动态规划**（Delete‑and‑Earn）求解。  
- **适用的题型**：  
  1. **Delete and Earn**（LeetCode 740）——删除相邻数得到分数。  
  2. **House Robber** 系列（抢劫相邻房子）——不能抢相邻的房子。  
  3. **Maximum Points You Can Obtain from Cards**（间距约束的点选问题）。  
- **一句话总结解题钥匙**：**先把相同伤害合并并排序，再用 DP 只在“能兼容的最近位置”上转移**。

---

## 反思  

- **第一反应**：看到“相差 1、2 的伤害不能同时出现”，立刻联想到 **Delete and Earn**，但最初会把每张牌都当成独立状态，导致思路混乱。  
- **最容易踩的坑**：  
  - **忘记合并相同伤害**：直接对原数组 DP 会导致 `O(n²)`，因为相同数之间也会产生大量重复状态。  
  - **边界条件**：`pre` 为 `-1` 时取 `0`，否则会出现数组越界。  
  - **大数范围**：`power[i]` 可达 `10⁹`，不能用数组下标直接映射，需要哈希表计数。  
- **下次遇到同类题**：第一步 **“先统计并排序唯一值”**，再思考 **“相邻冲突的最小距离是多少”**，最后套用 **DP/滑动窗口** 的框架。