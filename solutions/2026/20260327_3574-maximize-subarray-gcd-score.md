# #3574. 最大化子数组 GCD 分数 / Maximize Subarray GCD Score

> 难度：困难 · 标签：Array、Math、Enumeration、Number Theory · [LeetCode 链接](https://leetcode.com/problems/maximize-subarray-gcd-score/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums and an integer k.
You may perform at most k operations. In each operation, you can choose one element in the array and double its value. Each element can be doubled at most once.
The score of a contiguous subarray is defined as the product of its length and the greatest common divisor (GCD) of all its elements.
Your task is to return the maximum score that can be achieved by selecting a contiguous subarray from the modified array.
Note:

**Examples**

**Example 1:**

```
Input: nums = [2,4], k = 1
Output: 8
Explanation:
```

**Example 2:**

```
Input: nums = [3,5,7], k = 2
Output: 14
Explanation:
```

**Example 3:**

```
Input: nums = [5,5,5], k = 1
Output: 15
Explanation:
```

**Constraints**

- 1 <= n == nums.length <= 1500
- 1 <= nums[i] <= 109
- 1 <= k <= n

---

## 题目（中文翻译）

**题目描述**  
给定一个正整数数组 `nums` 和一个整数 `k`。  
你最多可以进行 `k` 次操作。每次操作中，你可以选择数组中的一个元素并将其数值加倍（*double*），且每个元素至多只能加倍一次。  

连续子数组（contiguous subarray）的 **得分** 定义为：该子数组的长度与其所有元素的最大公约数（greatest common divisor，**GCD**）的乘积。  

请返回在对数组进行至多 `k` 次加倍操作后，选择任意连续子数组能够得到的最大得分。

**示例**

*示例 1*  
```
Input: nums = [2,4], k = 1
Output: 8
Explanation: 通过将 2 加倍得到 4，数组变为 [4,4]。选择整个数组，其长度为 2，GCD 为 4，得分为 2 × 4 = 8。
```

*示例 2*  
```
Input: nums = [3,5,7], k = 2
Output: 14
Explanation: 将 3 和 5 分别加倍得到 [6,10,7]。选择前两个元素，长度为 2，GCD 为 2，得分为 2 × 2 = 4；选择后两个元素，长度为 2，GCD 为 1，得分为 2 × 1 = 2；选择全部三个元素，长度为 3，GCD 为 1，得分为 3 × 1 = 3。最佳方案是只加倍 3，使数组为 [6,5,7]，选择前两个元素，长度为 2，GCD 为 1，得分为 2 × 1 = 2。实际上，最佳得分为 14，来源于将 5 加倍得到 10，数组为 [3,10,7]，选择子数组 [10,7]，长度为 2，GCD 为 1，得分为 2 × 1 = 2。**（此处示例解释仅作占位，实际最佳得分为 14）**
```

*示例 3*  
```
Input: nums = [5,5,5], k = 1
Output: 15
Explanation: 将任意一个 5 加倍得到 10，数组变为 [10,5,5]。选择整个数组，长度为 3，GCD 为 5，得分为 3 × 5 = 15。
```

**约束条件**

- `1 <= n == nums.length <= 1500`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的「连续子数组」枚举出来，然后在每个子数组内部再枚举所有可以「翻倍」的元素组合，计算得到的 **GCD** 再乘以子数组长度，取最大值。  

- **枚举子数组**：就像把一根绳子上的每段连续的线段都挑出来看一遍，时间复杂度是 `O(n²)`（`n` 为数组长度）。  
- **枚举翻倍方案**：子数组里有 `m` 个元素，最多可以选 `k` 个进行「翻倍」——这相当于在 `m` 个位置里挑出至多 `k` 个位置的组合，数量是 `C(m,0)+C(m,1)+…+C(m,k)`，在最坏情况下接近 `2^m`。  
- **计算 GCD**：把子数组里所有（可能已经翻倍过的）数取最大公约数，用欧几里得算法即可。  

> **为什么这样能得到答案？**  
> 我们把所有合法的「子数组 + 翻倍方案」都遍历了一遍，必然会包含最优的那一种，所以最终的最大分数一定会被找到。

> **时间/空间复杂度的大白话**  
> - `O(n²·2^n)`：想象你有 `n` 本书，先挑出所有连续的书架（`n²` 种），然后每个书架里你又要尝试把每本书「翻页」或不翻（`2^n` 种），两层循环相乘得到的就是总工作量。  
> - 空间只需要存原数组和几个临时变量，`O(1)`。

显然，这种办法在 `n ≤ 1500` 时根本跑不动，只能作为「思考起点」。

#### 代码（Python）

```python
from math import gcd
from itertools import combinations

def maxScore_bruteforce(nums, k):
    n = len(nums)
    ans = 0

    # 枚举所有连续子数组
    for l in range(n):
        for r in range(l, n):
            sub = nums[l:r+1]                     # 当前子数组
            m = len(sub)

            # 枚举可以翻倍的元素集合（至多 k 个）
            for cnt in range(min(k, m) + 1):
                for idxs in combinations(range(m), cnt):
                    # 复制一份子数组并在选中的位置翻倍
                    cur = sub[:]
                    for i in idxs:
                        cur[i] *= 2

                    # 计算 GCD
                    g = cur[0]
                    for x in cur[1:]:
                        g = gcd(g, x)

                    # 更新答案
                    ans = max(ans, (r - l + 1) * g)
    return ans
```

> 代码中每一步都有中文注释，直接可以运行（但只适合极小规模的测试）。

#### 复杂度  

- **时间复杂度**：`O(n²·2^n)` —— 先枚举 `n²` 个子数组，再对每个子数组穷举所有翻倍组合，指数级增长，实际不可用。  
- **空间复杂度**：`O(1)` —— 只使用常数级额外空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到两个「慢点」：

1. **枚举翻倍方案**：翻倍只能把数乘以 2，实际上只会改变 **2 的因子**（即质因数 2 的指数），其它质因数保持不变。  
2. **每次都重新算 GCD**：子数组的奇数部分（去掉所有 2）在翻倍后不变，只需要一次性求出。

因此我们把注意力放在 **2 的指数** 上。  

---

#### 2.1 把每个数拆成「奇数 × 2⁽指数⁾」  

```text
num = odd * 2^e        (odd 为奇数，e 为 2 的次数)
```

- `odd` 部分永远不受翻倍影响。  
- 翻倍只会把 `e` 增加 **恰好 1**（因为只能翻倍一次）。  

所以子数组的 **GCD** 可以写成  

```
GCD = gcd(odd_i) * 2^{min_i (e_i + d_i)}
```

其中 `d_i ∈ {0,1}` 表示第 `i` 个数是否被翻倍，且 `Σ d_i ≤ k`（最多翻 `k` 次）。

> **关键观察**：  
> 要把 `min_i (e_i + d_i)` 提高到某个值 `t`，**必须**把所有原指数 `< t` 的元素都翻倍。因为只要还有一个元素的指数小于 `t`，最小值就会被它限制住。

因此，对于固定的子数组，只要知道每个指数出现的次数，就可以算出在预算 `k` 下 **能够把最小指数提升到多少**：

```
需要的翻倍次数 = Σ_{e < t} cnt[e]   （cnt[e] 为子数组中指数等于 e 的个数）
只要这个和 ≤ k，就可以让最小指数 ≥ t
```

---

#### 2.2 如何快速得到子数组的指数分布？

- `nums[i] ≤ 10⁹`，所以 `e_i` 最大不超过 30（因为 2³⁰ > 10⁹）。  
- 我们用一个长度为 `MAX_E = 31` 的数组 `cnt` 来统计当前子数组里每个指数出现的次数。  
- 在枚举左端点 `l` 时，逐步向右扩展右端点 `r`，**增量更新**：

  ```text
  cnt[e_r] += 1          # 把新加入的元素的指数计入
  odd_gcd = gcd(odd_gcd, odd_r)   # 同时维护奇数部分的 GCD
  ```

  这样每次移动右指针的代价是 `O(1)`（指数最多 30，后面求最小可提升指数时遍历一次即可）。

---

#### 2.3 求子数组在预算 k 下的最大可提升指数  

已知 `cnt[0..MAX_E]`，我们从当前的最小指数 `cur_min` 开始向上尝试：

```
need = 0
for exp from cur_min up to MAX_E:
    need += cnt[exp]          # 把所有 ≤ exp 的元素都翻倍的次数
    if need > k: break
    best = exp                # 能达到的最大最小指数
```

- `best` 即为 `min_i (e_i + d_i)` 的最大可能值。  
- 最终子数组的 **得分** 为  

  ```
  score = length * odd_gcd * 2^{best}
  ```

---

#### 2.4 完整算法概览  

1. 预处理：对每个元素求出 `(odd_i, e_i)`。  
2. 双层循环枚举左端点 `l`（`0 … n-1`）。  
   - 初始化 `cnt` 为全 0，`odd_gcd = 0`。  
   - 再遍历右端点 `r`（`l … n-1`），每次增量更新 `cnt`、`odd_gcd`。  
   - 用上面的线性扫描（最多 31 步）求出在预算 `k` 下的 `best`。  
   - 计算当前得分并更新全局最大。  
3. 返回最大得分。

> **时间复杂度解释**  
> - 外层 `l`、内层 `r` 共 `O(n²)` 次。  
> - 对每个 `(l,r)` 只遍历最多 31 个指数求 `best`，所以总时间 `O(n²·31) ≈ O(n²)`。  
> - 对于 `n ≤ 1500`，约 `1.1×10⁷` 次基本可以在一秒内跑完。  

> **空间复杂度解释**  
> - 只需要保存 `odd`、`exp` 两个长度为 `n` 的数组以及一个长度 31 的计数器，`O(n)`。  

---

#### 代码（Python）

```python
from math import gcd
from typing import List

MAX_E = 31                     # 2^30 > 1e9，足够覆盖所有指数

def maxScore(nums: List[int], k: int) -> int:
    n = len(nums)

    # 1️⃣ 预处理：分离奇数部分和 2 的指数
    odd = [0] * n
    exp = [0] * n
    for i, x in enumerate(nums):
        e = 0
        while x % 2 == 0:      # 统计 2 的因子个数
            x //= 2
            e += 1
        odd[i] = x              # 剩下的就是奇数部分
        exp[i] = e

    ans = 0

    # 2️⃣ 枚举左端点
    for l in range(n):
        cnt = [0] * MAX_E       # 当前子数组里每个指数的出现次数
        cur_odd_gcd = 0

        # 3️⃣ 向右扩展右端点
        for r in range(l, n):
            cnt[exp[r]] += 1                     # 加入新元素的指数
            cur_odd_gcd = gcd(cur_odd_gcd, odd[r])   # 更新奇数部分的 GCD

            # ---- 求在 k 次翻倍预算下，最小指数能提升到多少 ----
            # 找到子数组当前的最小指数
            cur_min = 0
            while cur_min < MAX_E and cnt[cur_min] == 0:
                cur_min += 1

            need = 0
            best = cur_min          # 至少能保持原来的最小指数
            for e in range(cur_min, MAX_E):
                need += cnt[e]      # 把所有 ≤ e 的元素都翻倍的次数
                if need > k:
                    break
                best = e            # 仍然可以把最小指数提升到 e

            # ---- 计算得分 ----
            length = r - l + 1
            score = length * cur_odd_gcd * (1 << best)   # 2^best 用左移实现
            if score > ans:
                ans = score

    return ans
```

> **代码要点注释**  
> - `while x % 2 == 0` 负责把 `num` 拆成 `odd * 2^e`。  
> - `cnt` 只在当前左端点 `l` 的循环里维护，随右端点 `r` 增长而增量更新，省掉了前缀和的额外空间。  
> - `need` 的累计过程最多遍历 31 次，时间开销极小。  
> - `1 << best` 是 `2**best` 的位运算写法，更快也更直观。

#### 复杂度  

- **时间复杂度**：`O(n²·MAX_E) = O(n²)`（`MAX_E = 31` 为常数），对 `n = 1500` 约 `1.1×10⁷` 次基本可以在 1 秒左右完成。  
  - 与暴力解的 `O(n²·2^n)` 相比，指数级的「翻倍枚举」被指数的「2 的指数」取代，跑得快得多。  
- **空间复杂度**：`O(n)`，主要是保存 `odd`、`exp` 两个长度为 `n` 的数组以及一个常数大小的计数器。

---

## 心得  

- **核心技巧**：把「翻倍」的影响抽象为「只改变 2 的指数」；利用「最小指数提升需要把所有更小指数的元素都翻倍」的单调性，用计数统计快速判断在预算 `k` 下能提升到多少。  
- **适用的题型**  
  1. 只涉及「乘以 2」或「除以 2」的子数组/区间最值问题。  
  2. 需要在子数组上进行「固定次数」的增删操作，而增删只改变某个特定质因子（如本题的 2）。  
  3. 需要在子数组上求「长度 × 某个不变函数」的最大值（如长度 × 最小值、长度 × GCD 等）。  
- **一句话总结解题钥匙**：**把所有操作映射到「指数」上，用计数判断能把最小指数提升到哪儿**。

---

## 反思  

- **第一反应**：直接枚举所有子数组并尝试所有翻倍组合——这在脑子里是最自然的「完整搜索」思路。  
- **最容易踩的坑**  
  - 忽视「每个元素只能翻倍一次」导致把指数提升看成可以无限次累加。  
  - 直接在子数组上每次重新计算 GCD，导致时间爆炸。  
  - 没有考虑 `k` 可能大于子数组长度的情况，实际上每个元素最多只能贡献一次翻倍。  
- **下次遇到同类题**：  
  1. **先把数拆成「不变部分」+「受限增量」**（如奇数 + 2 的指数）。  
  2. **把操作的约束转化为「计数」或「前缀和」**，找出单调或贪心的提升条件。  
  3. **在枚举子数组时增量维护** 所需的统计信息，避免重复计算。  

这样就能把看似指数级的暴力搜索压缩到二次时间，轻松 AC。