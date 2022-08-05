# #1884. 两枚鸡蛋和 N 层楼的掉落问题 / Egg Drop With 2 Eggs and N Floors

> 难度：中等 · 标签：Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/egg-drop-with-2-eggs-and-n-floors/)

---

## 题目（英文原版）

**Description**

You are given two identical eggs and you have access to a building with n floors labeled from 1 to n.
You know that there exists a floor f where 0 <= f <= n such that any egg dropped at a floor higher than f will break, and any egg dropped at or below floor f will not break.
In each move, you may take an unbroken egg and drop it from any floor x (where 1 <= x <= n). If the egg breaks, you can no longer use it. However, if the egg does not break, you may reuse it in future moves.
Return the minimum number of moves that you need to determine with certainty what the value of f is.

**Examples**

**Example 1:**

```
Input: n = 2
Output: 2
Explanation: We can drop the first egg from floor 1 and the second egg from floor 2.
If the first egg breaks, we know that f = 0.
If the second egg breaks but the first egg didn't, we know that f = 1.
Otherwise, if both eggs survive, we know that f = 2.
```

**Example 2:**

```
Input: n = 100
Output: 14
Explanation: One optimal strategy is:
- Drop the 1st egg at floor 9. If it breaks, we know f is between 0 and 8. Drop the 2nd egg starting from floor 1 and going up one at a time to find f within 8 more drops. Total drops is 1 + 8 = 9.
- If the 1st egg does not break, drop the 1st egg again at floor 22. If it breaks, we know f is between 9 and 21. Drop the 2nd egg starting from floor 10 and going up one at a time to find f within 12 more drops. Total drops is 2 + 12 = 14.
- If the 1st egg does not break again, follow a similar process dropping the 1st egg from floors 34, 45, 55, 64, 72, 79, 85, 90, 94, 97, 99, and 100.
Regardless of the outcome, it takes at most 14 drops to determine f.
```

**Constraints**

- 1 <= n <= 1000

---

## 题目（中文翻译）

你有两枚完全相同的鸡蛋（egg），并且可以进入一栋楼，它有编号为 1 到 n 的 n 层楼。  
已知存在一个楼层 f（0 ≤ f ≤ n），满足：

- 把鸡蛋从高于 f 的楼层扔下会碎；
- 把鸡蛋从 f 或更低的楼层扔下不会碎。

每一次操作（move），你可以拿一枚未碎的鸡蛋，从任意楼层 x（1 ≤ x ≤ n）扔下。如果鸡蛋碎了，则这枚鸡蛋不能再使用；如果鸡蛋未碎，则可以在后续操作中继续使用它。  

返回在 **确定** f 的值所需的**最小操作次数**。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

#### 示例 1
> **输入**: n = 2  
> **输出**: 2  
> **解释**:  
> 我们可以先在第 1 层扔第一枚鸡蛋，然后在第 2 层扔第二枚鸡蛋。  
> - 若第一枚鸡蛋碎了，则可确定 f = 0。  
> - 若第二枚鸡蛋碎而第一枚鸡蛋未碎，则可确定 f = 1。  
> - 若两枚鸡蛋都未碎，则可确定 f = 2。

#### 示例 2
> **输入**: n = 100  
> **输出**: 14  
> **解释**: 一种最优策略如下：  
> - 第一次在第 9 层扔第一枚鸡蛋。如果它碎了，则 f 在 0~8 之间。此时用第二枚鸡蛋从第 1 层开始逐层向上试，最多再扔 8 次即可确定 f。总共 1 + 8 = 9 次。  
> - 如果第一枚鸡蛋未碎，则再次在第 22 层扔第一枚鸡蛋。如果它碎了，则 f 在 9~21 之间。随后用第二枚鸡蛋逐层试，……（已截断）

### 约束条件
- 1 ≤ n ≤ 1000

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举每一种可能的投掷策略**，然后取最坏情况下（也就是最慢的情况）需要的步数的最小值。  
我们可以把问题抽象成“状态+决策”：

- **状态**：还有几只完整的鸡蛋（`egg`）以及当前剩余的楼层数（`floor`）。  
- **决策**：在第 `x` 层（`1 ≤ x ≤ floor`）把鸡蛋扔下去。  

投掷后会出现两种情况：

1. **鸡蛋碎了** → 剩下 `egg-1` 只鸡蛋，需要在 **下面的 `x-1` 层** 继续寻找临界楼层 `f`。  
2. **鸡蛋没碎** → 仍有 `egg` 只鸡蛋，需要在 **上面的 `floor-x` 层** 继续寻找 `f`（因为 `f` 必然在 `x` 以上或等于 `x`）。

所以，**最坏步数** = `1 + max( 破碎时的步数, 不破碎时的步数 )`。  
对所有可能的 `x` 取最小值，即得到当前状态的最优步数。

这就是典型的**动态规划**（DP）思路：  
- 小问题：`dp[egg][floor]` 表示在 `egg` 只鸡蛋、`floor` 层楼时，保证找出 `f` 所需的最少步数。  
- 大问题：从小问题递推得到大问题的答案。

> **类比**：把 DP 表想象成一本“查字典”。`egg` 是“词”，`floor` 是“页码”。我们把每个 `(egg, floor)` 对应的最优步数记在字典里，后面查询时直接返回，省去重复计算。

为什么这个方法一定能得到正确答案？  
因为我们遍历了**所有可能的第一步**，并且在每一步都考虑了**最坏情况**（因为我们必须在最坏情况下也能确定 `f`），递归地把问题拆成更小的子问题。递推到最底层（`egg==1` 或 `floor==0/1`）时显然是正确的，所以整个过程是自底向上的正确归纳。

#### 代码（Python）  
```python
def super_egg_drop_bruteforce(n: int) -> int:
    """
    暴力 DP：dp[e][f] 为 e 只鸡蛋、f 层楼时的最小步数
    时间复杂度 O(e * f^2)（这里 e 固定为 2，故近似 O(n^2)）
    空间复杂度 O(e * f)
    """
    # 只需要两只鸡蛋，所以 e = 2
    E = 2
    # 初始化 DP 表，dp[e][f] = 0 当 f == 0，dp[e][1] = 1
    dp = [[0] * (n + 1) for _ in range(E + 1)]

    # 只要有 1 只鸡蛋，最坏情况只能线性搜索
    for f in range(1, n + 1):
        dp[1][f] = f

    # 计算 dp[2][f]（因为题目只要两只鸡蛋）
    for f in range(1, n + 1):
        # 初始值设为一个很大的数，后面取最小值
        dp[2][f] = float('inf')
        # 枚举第一层投掷的位置 x
        for x in range(1, f + 1):
            # 碎了 → dp[1][x-1]，没碎 → dp[2][f-x]
            worst = 1 + max(dp[1][x - 1], dp[2][f - x])
            dp[2][f] = min(dp[2][f], worst)   # 取所有 x 中的最小值
    return dp[2][n]
```

#### 复杂度  
- **时间复杂度：`O(n²)`**  
  - “`O(n²)`” 的含义可以这么想：如果 `n = 1000`，程序大约会执行 1,000,000 次内部循环。  
- **空间复杂度：`O(n)`**（这里是 `O(E·n)`，因为 `E` 固定为 2，实际只和 `n` 成正比）  
  - 只需要保存一个大小为 `2 × (n+1)` 的表格，随 `n` 增大线性增长。

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**每一次都要遍历所有可能的投掷层 `x`**，导致二次方的时间。  
其实，对于**只有 2 只鸡蛋**的情况，我们可以把策略写得更“均匀”。  
设我们决定在第 `k` 步时最多还能进行 `k` 次投掷（因为每一步都要算一次），则第一只鸡蛋的投掷层次可以设为：

```
第 1 步：   第 k 层
第 2 步：   第 (k-1) 层 再往上（即 k + (k-1)）
第 3 步：   第 (k-2) 层 再往上（即 k + (k-1) + (k-2)）
...
第 k 步：   第 1 层 再往上（即 k + (k-1) + ... + 1）
```

这样设计的好处是**无论第一只鸡蛋在第几步碎掉，剩下的楼层数都不超过当时已经用掉的步数**，从而保证**最坏情况下的总步数等于 `k`**。

所以我们要找的 `k` 满足：

```
1 + 2 + 3 + ... + k  >=  n
=> k * (k + 1) / 2  >=  n
```

也就是说，**只要找最小的 `k` 使得 `k(k+1)/2` 大于等于 `n`**，这个 `k` 就是答案。

> **类比**：把 `k` 看成一把梯子，第一格跨 1 层，第二格跨 2 层，依次递增。只要这把梯子总高度够到楼顶，就一定能在 `k` 步之内找到临界层。

求最小 `k` 的方法有两种：

1. **数学公式**：直接求解二次不等式 `k² + k - 2n ≥ 0`，得到 `k = ceil( (-1 + sqrt(1 + 8n)) / 2 )`。  
2. **线性/二分搜索**：从 `1` 开始累加，直到累计和 ≥ `n`（时间 `O(sqrt(n))`），或用二分 `O(log n)`。

下面用 **二分搜索** 实现，代码简洁且避免浮点误差。

#### 代码（Python）  
```python
import math

def super_egg_drop_optimal(n: int) -> int:
    """
    最优解：只需要找到最小的 k，使得 k*(k+1)/2 >= n
    时间复杂度 O(log n)（二分查找），空间复杂度 O(1)
    """
    # 二分搜索范围：最低 1 步，最高 n 步（显然不可能超过 n 步）
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        # 累计的最大可覆盖层数
        total = mid * (mid + 1) // 2
        if total >= n:          # 足够高，尝试更小的步数
            hi = mid
        else:                   # 不够高，需要更多步数
            lo = mid + 1
    return lo
```

> **为什么二分有效？**  
> 我们把 `k` 当作单调递增的函数 `f(k) = k(k+1)/2`，当 `k` 增大时 `f(k)` 只会变大。于是“`f(k) >= n`”这个条件在 `k` 上形成一个 **前缀为 False、后缀为 True** 的区间，正好适合二分查找。

#### 复杂度  
- **时间复杂度：`O(log n)`**  
  - 相比暴力的 `O(n²)`，`log n` 只在 `n=1000` 时需要约 10 次循环，几乎可以忽略不计。  
- **空间复杂度：`O(1)`**  
  - 只用了常数个变量，不会随 `n` 增大而占用更多内存。

---  

## 心得  

- **核心技巧**：把“两只鸡蛋的最坏步数”转化为**等差数列求和**，找到满足 `k(k+1)/2 ≥ n` 的最小 `k`。  
- **适用场景**：  
  1. **单调递增的搜索空间**（如找最小步数、最小容量等）可以用二分或等差求和。  
  2. **鸡蛋掉落问题的特殊情形**（鸡蛋数固定为 2）可以用**三角数**直接求解。  
  3. **分段递增资源分配**（如分配最少次数的预算，使总覆盖≥目标）同样适用。  
- **一句话总结解题钥匙**：*把“最坏情况的步数”变成“覆盖的层数”，用等差数列的和求最小步数*。

---  

## 反思  

- **第一反应**：看到“2 只鸡蛋”，立刻想到经典的 DP 状态转移 `dp[e][f] = 1 + min_x max(dp[e-1][x-1], dp[e][f-x])`，于是写出暴力解。  
- **最容易踩的坑**：  
  1. **边界**：`n = 0` 时答案应为 `0`（不需要任何投掷），代码要能处理。  
  2. **整数溢出**（在语言是 C/C++ 时），`k*(k+1)/2` 可能超出 32 位整数范围，需要使用 64 位或提前判断。  
  3. **浮点误差**：直接用公式 `ceil((-1+sqrt(1+8n))/2)` 时，`sqrt` 产生的误差可能导致向下取整错误，二分法可以规避。  
- **下次遇到同类题**：先**判断是否可以把步数转化为单调函数的阈值**（如等差、等比求和），如果可以，直接用数学或二分求解；如果不行，再考虑完整的 DP。  

祝你在算法的道路上越走越稳！ 🚀