# #3560. 最小原木运输成本 / Find Minimum Log Transportation Cost

> 难度：简单 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/find-minimum-log-transportation-cost/)

---

## 题目（英文原版）

**Description**

You are given integers n, m, and k.
There are two logs of lengths n and m units, which need to be transported in three trucks where each truck can carry one log with length at most k units.
You may cut the logs into smaller pieces, where the cost of cutting a log of length x into logs of length len1 and len2 is cost = len1 * len2 such that len1 + len2 = x.
Return the minimum total cost to distribute the logs onto the trucks. If the logs don't need to be cut, the total cost is 0.

**Examples**

**Example 1:**

```
Input: n = 6, m = 5, k = 5
Output: 5
Explanation:
Cut the log with length 6 into logs with length 1 and 5, at a cost equal to 1 * 5 == 5 . Now the three logs of length 1, 5, and 5 can fit in one truck each.
```

**Example 2:**

```
Input: n = 4, m = 4, k = 6
Output: 0
Explanation:
The two logs can fit in the trucks already, hence we don't need to cut the logs.
```

**Constraints**

- 2 <= k <= 105
- 1 <= n, m <= 2 * k
- The input is generated such that it is always possible to transport the logs.

---

## 题目（中文翻译）

给定整数 `n`、`m` 和 `k`。有两根长度分别为 `n` 和 `m` 单位的原木（log），需要放入三辆卡车（truck）中，每辆卡车最多只能承载一根长度不超过 `k` 单位的原木。你可以将原木切割（cut）成更小的段，切割一根长度为 `x` 的原木为长度为 `len1` 和 `len2` 的两段的代价为  

```
cost = len1 * len2   （且 len1 + len2 = x）
```  

返回将原木分配到卡车上的最小总代价。如果不需要切割原木，则总代价为 `0`。

**示例 1**  
输入: `n = 6, m = 5, k = 5`  
输出: `5`  
解释:  
将长度为 6 的原木切割成长度为 1 和 5 的两段，代价为 `1 * 5 = 5`。此时三根长度为 1、5、5 的原木分别可以装入三辆卡车。

**示例 2**  
输入: `n = 4, m = 4, k = 6`  
输出: `0`  
解释:  
两根原木本身就能分别装入卡车，无需切割，总代价为 `0`。

**约束条件**  
- `2 <= k <= 10^5`  
- `1 <= n, m <= 2 * k`  
- 输入保证一定可以将原木运输完毕。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每根原木所有可能的切法都枚举一遍**，看哪种切法能够让得到的 ≤ 3 根木头全部 ≤ k，并且切割费用最小。

- **枚举方式**：对每根需要切的原木 `x`，遍历 `len1` 从 `1` 到 `x‑1`，把它切成 `len1` 与 `len2 = x‑len1` 两段。费用 `len1 * len2`。
- **组合检查**：把所有得到的段（最多 3 段）放进 3 辆卡车，检查每段长度是否 ≤ k。
- **数据结构类比**：这里的“段列表”就像我们在超市挑选商品的购物车，放进去的每件商品（段）都必须满足重量 ≤ k 才能装进对应的购物车（卡车）。

因为题目只要求 **最小总费用**，我们只需要在所有合法切法中取费用最小的那一个。

> 这种做法一定能得到正确答案——我们把**所有**可能的切法都尝试了一遍，只要有合法的方案就会被找到。

#### 代码（Python）

```python
def minCost_bruteforce(n: int, m: int, k: int) -> int:
    # 如果两根木头本身就能装进卡车，直接返回 0
    if n <= k and m <= k:
        return 0

    ans = float('inf')                     # 记录最小费用
    # 枚举哪根木头需要切（只需要切一根，切两根会产生 >3 段）
    for length, other in [(n, m), (m, n)]:
        # length 必须大于 k 才需要切
        if length <= k:
            continue
        # 枚举第一段的长度 len1
        for len1 in range(1, length):      # 1 … length‑1
            len2 = length - len1            # 第二段长度
            # 两段都必须 ≤ k，才能放进卡车
            if len1 <= k and len2 <= k and other <= k:
                cost = len1 * len2
                ans = min(ans, cost)
    return ans if ans != float('inf') else 0
```

> 关键行说明  
> - 第 4 行：先判断是否已经不需要切割。  
> - 第 10‑11 行：只尝试切一根木头（因为只能有最多 3 段）。  
> - 第 13‑16 行：遍历所有可能的第一段长度 `len1`，计算对应的费用并更新最小值。

#### 复杂度

- **时间复杂度**：`O(L)`，其中 `L = max(n, m)`，因为我们对需要切的那根木头的每个可能切点都遍历一次。  
  用大白话说，如果最长的木头长 1000，最坏要检查 1000 次。
- **空间复杂度**：`O(1)`，只用了常数个变量。

> 暴力解虽然思路简单，但当 `n`、`m` 接近 `2·k`（最大可达 2·10⁵）时，需要遍历 10⁵ 次，仍然可以接受，但我们还能更快。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**只会切一根木头**，因为我们只能得到最多 3 段（每辆卡车装一段）。  
再进一步分析：

1. **输入必然满足“最多只有一根木头超过 k”**  
   - 题目保证一定可以运输。若两根都 > k，则即使切一根也会留下另一根仍 > k，无法放进卡车。因此不可能出现这种情况。  
   - 所以要么两根都 ≤ k（直接返回 0），要么恰好有 **一根** 长度 `L > k`。

2. **只需要一次切割**  
   - 只对那根超长的木头 `L` 切一次，得到两段 `a` 与 `b`，再加上另一根已经 ≤ k 的木头，总共 3 段，正好装进 3 辆卡车。

3. **怎样切才能让费用最小？**  
   - 费用公式 `a * b`，且 `a + b = L`，且 `a ≤ k`、`b ≤ k`（因为每段都必须 ≤ k）。  
   - 在固定和 `L` 的情况下，**乘积在两数越不相等时越小**（可以用算术-几何均值不等式或画图理解：把一根绳子分成两段，越不均匀，乘积越小）。  
   - 因此我们让其中一段尽可能大（等于上限 `k`），另一段自然是 `L - k`。  
   - 检查 `L - k` 是否 ≤ k：因为题目给出 `L ≤ 2·k`，所以 `L - k ≤ k` 必然成立。  

4. **最小费用公式**  

\[
\text{cost} = k \times (L - k)
\]

如果 `L == k`，说明根本不需要切割，费用为 0。

> 这样我们把 “遍历所有切点” 的过程直接用数学推导一步得到最优切法，时间只剩 O(1)。

#### 代码（Python）

```python
def minCost(n: int, m: int, k: int) -> int:
    """
    返回将两根原木装进 3 辆卡车的最小切割费用。
    思路：最多只有一根木头需要切，切成 (k, L-k) 两段即可得到最小费用。
    """
    # 两根木头都已经 <= k，无需切割
    if n <= k and m <= k:
        return 0

    # 取较长的那根，需要切割的长度 L
    L = max(n, m)

    # L > k 必然成立（因为上面已经排除两根都 <= k 的情况）
    # 切成 k 与 L-k，两段均 <= k（因为 L <= 2*k）
    return k * (L - k)
```

> 关键行说明  
> - 第 5‑6 行：直接判断是否已经满足条件，返回 0。  
> - 第 9 行：找出需要切的那根最长木头 `L`。  
> - 第 13 行：返回最小费用公式 `k * (L - k)`。

#### 复杂度

- **时间复杂度**：`O(1)`，只做了常数次比较和一次乘法。  
  用大白话说：不管木头有多长，程序只跑了几步，就算是“瞬间”算完。
- **空间复杂度**：`O(1)`，只用了几个整数变量。

> 与暴力解相比，时间从最多 10⁵ 次循环降到了 1 次运算，速度提升数万倍。

---

## 心得

- **核心技巧**：利用题目“只能使用 3 辆卡车” 的限制，**把搜索空间压到只有一种可能的切割**，再用“乘积在两数越不相等越小” 的数学性质直接求最小费用。  
- **适用场景**：  
  1. **只能切一次** 的分割类问题（例如把一根绳子切成两段，使得最大段 ≤ 限制并最小化某代价）。  
  2. **固定数量容器**（卡车、背包）且容器容量上限已知，需要最少切割次数的情况。  
  3. **费用函数为 `a*b`**（或其他在不均衡时更小）的优化题目。  
- **一句话总结**：**把长的那根木头切成 “k 与 L‑k” 两段，即是费用最小的唯一切法**。

---

## 反思

- **第一反应**：先想到“遍历所有切点”，即暴力搜索。  
- **最容易踩的坑**：  
  - 忽略了“输入一定可以运输”，导致对 “两根都 > k” 的情况进行不必要的处理。  
  - 没有意识到 **乘积在不均衡时更小**，从而错过直接求最小费用的公式。  
- **下次遇到同类题**：第一步先 **分析约束（容器数量、容量上限）**，判断**最多需要几次切割**，再利用 **数学单调性**（如乘积、和的关系）直接推导最优切法，而不是盲目枚举。