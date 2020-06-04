# #887. 超级鸡蛋掉落 / Super Egg Drop

> 难度：困难 · 标签：Math、Binary Search、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/super-egg-drop/)

---

## 题目（英文原版）

**Description**

You are given k identical eggs and you have access to a building with n floors labeled from 1 to n.
You know that there exists a floor f where 0 <= f <= n such that any egg dropped at a floor higher than f will break, and any egg dropped at or below floor f will not break.
Each move, you may take an unbroken egg and drop it from any floor x (where 1 <= x <= n). If the egg breaks, you can no longer use it. However, if the egg does not break, you may reuse it in future moves.
Return the minimum number of moves that you need to determine with certainty what the value of f is.

**Examples**

**Example 1:**

```
Input: k = 1, n = 2
Output: 2
Explanation: 
Drop the egg from floor 1. If it breaks, we know that f = 0.
Otherwise, drop the egg from floor 2. If it breaks, we know that f = 1.
If it does not break, then we know f = 2.
Hence, we need at minimum 2 moves to determine with certainty what the value of f is.
```

**Example 2:**

```
Input: k = 2, n = 6
Output: 3
```

**Example 3:**

```
Input: k = 3, n = 14
Output: 4
```

**Constraints**

- 1 <= k <= 100
- 1 <= n <= 104

---

## 题目（中文翻译）

给定 **k** 个相同的鸡蛋（eggs），以及一栋有 **n** 层、编号为 1 到 **n** 的大楼（building）。已知存在一个楼层 **f**，满足 `0 <= f <= n`，使得：

- 在高于 **f** 的任意楼层扔下的鸡蛋都会碎（break），
- 在不高于 **f** 的任意楼层扔下的鸡蛋都不会碎（not break）。

每一次操作，你可以取一枚未碎的鸡蛋，从任意楼层 **x**（`1 <= x <= n`）扔下。如果鸡蛋碎了，则该鸡蛋无法再使用；如果鸡蛋未碎，则可以在后续操作中继续使用。

**返回** 为确定 **f** 的确切值所需的**最少移动次数**（minimum number of moves）。

---

### 示例

**示例 1**

```
Input: k = 1, n = 2
Output: 2
Explanation: 
从第 1 层扔下鸡蛋。如果它碎了，我们就知道 f = 0。
否则，从第 2 层扔下鸡蛋。如果它碎了，我们就知道 f = 1。
如果它仍未碎，则可以确定 f = 2。
因此，至少需要 2 次移动才能确定 f 的值。
```

**示例 2**

```
Input: k = 2, n = 6
Output: 3
```

**示例 3**

```
Input: k = 3, n = 14
Output: 4
```

---

### 约束条件

- `1 <= k <= 100`
- `1 <= n <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一次扔蛋的楼层**，然后把剩下的情况递归下来：

1. 选一个楼层 `x`（1 ≤ x ≤ n）把蛋扔下去  
   - **蛋碎了**：说明临界楼层 `f` 必须在 `[0, x‑1]` 之间，此时我们手里只剩 `k‑1` 个完整的蛋，需要在 `x‑1` 层楼里继续找。  
   - **蛋没碎**：说明 `f` 必须在 `[x, n]` 之间，此时蛋的数量仍是 `k`，但只剩 `n‑x` 层楼要检查。

2. 对这两种子问题分别求解，取**最坏情况**（因为我们要“确定” `f`，必须能应付最不利的分支），再加上这一次的投掷次数 `1`，得到在楼层 `x` 处投掷的总代价。  
3. 在所有可能的 `x` 中，选出总代价最小的那个，即为当前 `k`、`n` 的答案。

这就是**递归 + 记忆化**（自底向上也可以写成 DP 表格）的思路。它类似于我们平时查字典的过程：要找一个单词的意义，我们可以先把字典一页页翻过去，最坏情况下要翻到最后一页；而这里的“翻页”就是一次次投掷。

> 为什么一定能得到正确答案？  
> 因为我们穷举了**所有可能的投掷位置**，并在每个位置上考虑了**最坏的后续情况**。只要选最小的最坏代价，就一定是能够在最少次数内保证找出 `f` 的方案。

#### 代码（Python）

```python
from functools import lru_cache

def superEggDrop_bruteforce(k: int, n: int) -> int:
    """
    暴力递归 + 记忆化
    dp(k, n) 表示 k 个蛋、n 层楼时的最少投掷次数
    """
    @lru_cache(None)                     # 自动记忆化，避免重复计算
    def dp(eggs: int, floors: int) -> int:
        # 边界：没有楼层需要检查，或者只有一层楼，显然不需要投掷
        if floors == 0 or floors == 1:
            return floors                 # 0 或 1 次
        # 只有一个蛋，只能线性尝试，从第一层往上依次扔
        if eggs == 1:
            return floors

        # 暴力遍历每一种投掷楼层 x，取最小的最坏代价
        ans = float('inf')
        for x in range(1, floors + 1):
            # 蛋碎了 → eggs-1, x-1 层
            broken = dp(eggs - 1, x - 1)
            # 蛋没碎 → eggs, floors-x 层
            not_broken = dp(eggs, floors - x)
            # 这一次投掷后，最坏情况下需要的次数
            worst = 1 + max(broken, not_broken)
            ans = min(ans, worst)          # 取所有 x 中的最小值

        return ans

    return dp(k, n)
```

#### 复杂度  

- **时间复杂度**：`O(k * n^2)`  
  - 解释：对每一对 `(eggs, floors)`（共 `k * n` 种）我们都要遍历所有可能的投掷楼层 `x`（最多 `n` 次），于是乘起来就是 `k·n·n = k·n²`。  
  - “`O(n²)`” 可以想象成**在一个 100×100 的棋盘上遍历所有格子**，规模会快速膨胀。

- **空间复杂度**：`O(k * n)`  
  - 解释：记忆化表（`lru_cache`）保存了每个 `(eggs, floors)` 的结果，数量上限是 `k·n`。递归栈的深度最多 `k + n`，同样是线性级别。

> 由于 `k ≤ 100，n ≤ 10⁴`，`k·n²` 在最坏情况下会达到 `10⁸` 级别，远超时间限制，故需要更快的算法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每一步都要遍历所有可能的投掷楼层 `x`**。如果我们能直接算出在 `m` 次投掷、`k` 个蛋的情况下最多能“覆盖”多少层楼，就可以反过来找最小的 `m` 使得覆盖层数 ≥ `n`，从而得到答案。

> **核心观察**  
> 假设我们已经决定要进行 `m` 次投掷（不管实际怎么投），并且手里有 `k` 个蛋。  
> 第一次投掷我们选在第 `x` 层：
> - 蛋碎了 → 只剩 `k‑1` 个蛋，且最多还能投 `m‑1` 次，这时我们只能利用**下面的 `x‑1` 层**。
> - 蛋没碎 → 仍有 `k` 个蛋，最多还能投 `m‑1` 次，这时我们只能利用**上面的 `n‑x` 层**。

> 那么，无论第一次投在哪层，**我们能确定的楼层数** = (碎了时能覆盖的层数) + (没碎时能覆盖的层数) + 1（当前这层本身）。  
> 用数学式写成：
> ```
> dp[m][k] = dp[m-1][k-1] + dp[m-1][k] + 1
> ```
> 其中 `dp[m][k]` 表示 **在最多 m 次投掷、k 个蛋的情况下，能够判定的最高楼层**（即最坏情况下可以覆盖的楼层数）。

> 这条递推式的意义相当于**把问题拆成两段**：  
> - “左边”对应蛋碎了的情形，使用 `k‑1` 个蛋、`m‑1` 次投掷能覆盖的层数；  
> - “右边”对应蛋没碎的情形，使用 `k` 个蛋、`m‑1` 次投掷能覆盖的层数；  
> - 再加上当前这层本身，就是总共可以判定的层数。

> **如何利用这条式子求最小投掷次数？**  
> 我们从 `m = 0` 开始递增，逐步计算 `dp[m][k]`（只需要保存上一行即可），直到 `dp[m][k] ≥ n` 为止。此时的 `m` 就是答案。

> 这种做法的时间复杂度是 `O(k * log n)`（因为 `m` 的增长速度非常快，最多只需要约 `log₂ n` 次循环），空间复杂度只需要 `O(k)`。

> 下面再用一个生活化的比喻帮助理解：  
> 想象我们有 `k` 张**“纸条”**，每次可以在楼层上贴一张纸条，纸条会在**“碎”**或**“不碎”**两种情况下分别指向不同的子问题。每贴一次纸条，就把搜索范围**分成两块**，而我们只关心最坏的那块。递推式正是把这两块的可搜索范围相加再加上当前这层。

#### 代码（Python）

```python
def superEggDrop_optimal(k: int, n: int) -> int:
    """
    使用 dp[m][k] = dp[m-1][k-1] + dp[m-1][k] + 1 的逆向思路
    找到最小的投掷次数 m，使得 dp[m][k] >= n
    """
    # dp[j] 表示在当前的投掷次数 m 下，使用 j 个蛋能够覆盖的最大楼层数
    dp = [0] * (k + 1)          # 初始时 m = 0，所有 dp[j] = 0
    moves = 0                   # 已经使用的投掷次数

    # 循环直到能够覆盖 n 层楼
    while dp[k] < n:
        moves += 1
        # 必须从后向前更新，防止覆盖掉 dp[m-1][k-1] 的旧值
        for eggs in range(k, 0, -1):
            # dp[eggs]（对应 dp[m][eggs]）由上一轮的两个状态相加得到
            dp[eggs] = dp[eggs] + dp[eggs - 1] + 1
            # 解释：dp[eggs]（左边）是“蛋没碎”时还能再投 moves-1 次；
            #       dp[eggs-1]（右边）是“蛋碎了”时还能再投 moves-1 次；
            #       +1 表示当前这一次投掷的这层楼。

    return moves
```

#### 复杂度  

- **时间复杂度**：`O(k * log n)`  
  - 解释：每一次循环 `moves` 都会把 `dp[k]` 按指数级增长（大约翻倍），所以要让它达到 `n` 只需要 `log₂ n` 次循环。每次循环我们遍历 `k` 个蛋的状态，故总体是 `k * log n`。  
  - 把 `log n` 想象成**把 10,000 折半几次**（大约 14 次），这在实际运行中几乎是瞬间完成。

- **空间复杂度**：`O(k)`  
  - 只用一个长度为 `k+1` 的一维数组来保存当前投掷次数下每种蛋数的覆盖层数，空间随 `k` 线性增长。

> 与暴力解相比，**时间从 `k·n²` 降到了 `k·log n`**，在最坏数据下快了上万倍以上。

---

## 心得

- **核心技巧**：把“最少投掷次数”转化为“在固定次数内能覆盖的最大楼层”，利用递推式 `dp[m][k] = dp[m-1][k-1] + dp[m-1][k] + 1` 进行**逆向求解**。  
- **适用场景**：  
  1. **Egg Drop 系列**（经典的“鸡蛋与楼层”问题）  
  2. **找最小满足条件的次数**（如“最少次数把数组分成若干段使每段满足某条件”）  
  3. **搜索空间的二分/指数扩展**（例如在有限资源下的最大可达范围问题）  
- **一句话总结**：**把“最少次数”变“最大覆盖”，用递推快速逼近目标**。

---

## 反思

- **第一反应**：看到“k 个蛋、n 层楼”，立刻想到“暴力枚举每一次投掷的楼层”，写出递归/DP。  
- **最容易踩的坑**：  
  - **边界条件**：`k = 1` 时只能线性尝试；`n = 0` 时答案应为 `0`。  
  - **整数溢出**（在某些语言里）——递推式会快速增长，需要使用大整数或提前做截断。  
  - **更新顺序**：在一维 DP 中必须**从后向前**遍历，否则会把 `dp[m-1][k-1]` 的新值覆盖掉，导致错误。  
- **下次遇到同类题**：第一步先思考**“固定次数能做多少”**，尝试写出类似的递推关系，再用二分或线性搜索找到最小满足的次数。这样往往能把指数级搜索压缩到对数级。