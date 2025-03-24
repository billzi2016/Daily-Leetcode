# #3116. 单一面额组合的第 k 小金额 / Kth Smallest Amount With Single Denomination Combination

> 难度：困难 · 标签：Array、Math、Binary Search、Bit Manipulation、Combinatorics、Number Theory · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-amount-with-single-denomination-combination/)

---

## 题目（英文原版）

**Description**

You are given an integer array coins representing coins of different denominations and an integer k.
You have an infinite number of coins of each denomination. However, you are not allowed to combine coins of different denominations.
Return the kth smallest amount that can be made using these coins.

**Examples**

**Example 1:**

```
Input: coins = [3,6,9], k = 3
Output: 9
Explanation: The given coins can make the following amounts: Coin 3 produces multiples of 3: 3, 6, 9, 12, 15, etc. Coin 6 produces multiples of 6: 6, 12, 18, 24, etc. Coin 9 produces multiples of 9: 9, 18, 27, 36, etc. All of the coins combined produce: 3, 6, 9 , 12, 15, etc.
```

**Example 2:**

```
Input: coins = [5,2], k = 7
Output: 12
Explanation: The given coins can make the following amounts: Coin 5 produces multiples of 5: 5, 10, 15, 20, etc. Coin 2 produces multiples of 2: 2, 4, 6, 8, 10, 12, etc. All of the coins combined produce: 2, 4, 5, 6, 8, 10, 12 , 14, 15, etc.
```

**Constraints**

- 1 <= coins.length <= 15
- 1 <= coins[i] <= 25
- 1 <= k <= 2 * 109
- coins contains pairwise distinct integers.

---

## 题目（中文翻译）

给定一个整数数组 `coins`，其中每个元素表示一种不同面额的硬币，以及一个整数 `k`。  
你拥有每种面额的无限硬币，但 **不允许** 将不同面额的硬币混合使用。  

返回可以用这些硬币组成的第 k 小的金额。

---

**示例 1**  
**输入**: `coins = [3,6,9]`, `k = 3`  
**输出**: `9`  
**解释**:  
- 面额为 3 的硬币可以组成 3 的倍数：`3, 6, 9, 12, 15, …`。  
- 面额为 6 的硬币可以组成 6 的倍数：`6, 12, 18, 24, …`。  
- 面额为 9 的硬币可以组成 9 的倍数：`9, 18, 27, 36, …`。  

所有硬币单独产生的金额合并后为：`3, 6, 9, 12, 15, …`，第 3 小的金额是 `9`。

---

**示例 2**  
**输入**: `coins = [5,2]`, `k = 7`  
**输出**: `12`  
**解释**:  
- 面额为 5 的硬币可以组成 5 的倍数：`5, 10, 15, 20, …`。  
- 面额为 2 的硬币可以组成 2 的倍数：`2, 4, 6, 8, 10, 12, …`。  

合并后得到的金额序列为：`2, 4, 5, 6, 8, 10, 12, 14, 15, …`，第 7 小的金额是 `12`。

---

**约束条件**

- `1 <= coins.length <= 15`
- `1 <= coins[i] <= 25`
- `1 <= k <= 2 * 10^9`
- `coins` 中的元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种面值的硬币的所有倍数都列出来**，然后把它们合并、去重、排好序，取第 `k` 小的那个。  
可以把每一种硬币想象成一条**无限长的流水线**，流水线上会不断输出 `coin, 2·coin, 3·coin …`。  
我们把这些流水线的输出放进一个**最小堆**（也叫优先队列），每次弹出堆顶的最小值，就得到当前所有未出现的最小金额。  

为什么这样能得到正确答案？

- 每次弹出的数一定是所有未弹出金额中的最小值（堆的性质）。
- 把弹出的数再乘以对应的硬币面值，放回堆里，就相当于把这条流水线推进一步，保证后面的倍数还能被考虑到。
- 用 `set`（或在弹出时判断是否已经出现）去掉重复的金额，保证每个金额只计一次。

> **注意**：这种方法在 `k` 很大（题目里 `k ≤ 2·10⁹`）时会非常慢，因为我们必须一次一次地弹出 `k` 次。它更像是把 “把所有水倒进杯子再数杯子” 的做法，时间会随 `k` 线性增长。

#### 代码（Python）

```python
import heapq

def kth_smallest_bruteforce(coins, k):
    """
    暴力解：使用最小堆逐个生成金额，直至第 k 小
    只适用于 k 较小的情况，演示思路用
    """
    # 去重的集合，防止同一个金额被多次加入堆
    visited = set()
    # 最小堆，初始放入每种硬币的第一个倍数（即硬币本身）
    heap = []
    for c in coins:
        heapq.heappush(heap, c)
        visited.add(c)

    ans = None
    for _ in range(k):
        # 取出当前最小的金额
        ans = heapq.heappop(heap)
        # 把该金额对应的硬币再向后推一个倍数加入堆
        # 例如弹出 6（来自硬币 3），下一个应该是 9（3*3）
        # 为了知道是哪枚硬币产生的，这里直接遍历所有硬币
        for c in coins:
            # 只有当 ans 是 c 的倍数时，它才是这枚硬币产生的
            if ans % c == 0:
                nxt = ans + c          # 下一个倍数
                if nxt not in visited: # 防止重复加入
                    visited.add(nxt)
                    heapq.heappush(heap, nxt)
                break  # 每次只会匹配到唯一的一枚硬币
    return ans
```

> **关键行中文注释**  
> - `heapq.heappush(heap, c)`：把每种硬币的第一个可支付金额放进堆里。  
> - `ans = heapq.heappop(heap)`：弹出当前最小的金额。  
> - `nxt = ans + c`：把对应硬币的下一个倍数算出来，再放回堆。  
> - `visited` 用来记住已经出现过的金额，防止同一个数多次进入堆。

#### 复杂度

- **时间复杂度**：`O(k log n)`  
  - 每弹出一次堆顶，需要 `log n`（`n` 为硬币种类数，最多 15）时间来维护堆；弹出 `k` 次所以是 `k·log n`。  
  - 当 `k` 很大时（比如 10⁹），这几乎等同于 **线性** 增长，计算量会爆炸。

- **空间复杂度**：`O(k)`（最坏情况）  
  - 为了去重，我们用 `visited` 集合保存已经出现的金额，最多会存 `k` 个数。  

> 这套方法只能用于 **“先跑跑”** 的教学示例，真正解大数据范围的题目需要更巧的思路。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到：**瓶颈在于逐个枚举金额**。我们其实不需要真的把每个金额列出来，只要能够**快速判断**“截至某个值 `x`，一共有多少不同的金额可以被凑出来”。有了这个“计数函数”，就可以在答案空间上**二分搜索**第 `k` 小的金额。

**计数函数的核心**  
- 对于单一种类的硬币 `c`，它能凑出的金额是 `c, 2c, 3c, …`，在区间 `[1, x]` 内的个数是 `⌊x / c⌋`（整数除法）。
- 多种硬币会产生**重叠**：比如 `6` 同时是 `3` 的倍数也是 `6` 的倍数。我们不能把它算两次。  
- 这正是**容斥原理（Inclusion‑Exclusion Principle）**的用武之地。  
  - 对所有非空子集 `S`（子集里包含若干硬币），计算这些硬币的 **最小公倍数** `l = lcm(S)`。  
  - `x // l` 表示 **同时是子集里所有硬币的倍数** 的金额个数。  
  - 如果子集大小为奇数，就 **加** 这个数量；如果为偶数，就 **减**。把所有子集的贡献加起来，就得到 **“至多 x 的不同金额总数”**。

因为 `coins.length ≤ 15`，子集总数 `2^15 - 1 = 32767`，完全可以遍历。每个子集只需要求一次 LCM，时间开销很小。

**二分搜索的区间**  
- 最小可能的金额是 `min(coins)`（最小硬币本身）。
- 最大可能的第 `k` 小金额不会超过 `min(coins) * k`（只使用最小硬币就能得到前 `k` 个金额的上界）。
- 所以我们在 `[1, min(coins) * k]` 区间上二分，找第一个使 “计数 ≥ k” 的 `x`，这就是答案。

#### 代码（Python）

```python
import math
from functools import reduce

def lcm(a, b):
    """返回 a 与 b 的最小公倍数，利用 gcd（最大公约数）"""
    return a // math.gcd(a, b) * b

def count_up_to(x, coins):
    """
    使用容斥原理统计 ≤ x 的不同金额个数
    - 遍历所有非空子集
    - 对子集求 lcm，利用 x // lcm 计数
    - 奇数子集加，偶数子集减
    """
    n = len(coins)
    total = 0
    # 子集用 1..(1<<n)-1 表示，二进制位为 1 时对应的硬币在子集里
    for mask in range(1, 1 << n):
        bits = 0          # 子集大小（用于判断奇偶）
        cur_lcm = 1
        for i in range(n):
            if mask >> i & 1:
                bits += 1
                cur_lcm = lcm(cur_lcm, coins[i])
                # 若 lcm 已经大于 x，后面再乘也不会贡献任何数，直接退出子集
                if cur_lcm > x:
                    break
        else:  # 只有当 for 循环没有因 break 提前退出时才执行
            cnt = x // cur_lcm
            if bits % 2 == 1:   # 奇数子集 → 加
                total += cnt
            else:               # 偶数子集 → 减
                total -= cnt
    return total

def kth_smallest(coins, k):
    """
    二分答案 + 容斥计数 → O(2^n * log(max_answer))
    """
    coins = sorted(set(coins))          # 去重、排序（虽说题目已保证不重复）
    lo, hi = 1, min(coins) * k          # 搜索区间
    while lo < hi:
        mid = (lo + hi) // 2
        if count_up_to(mid, coins) >= k:
            hi = mid                     # 第 k 小 ≤ mid，继续左侧
        else:
            lo = mid + 1                 # 第 k 小 > mid，右移
    return lo
```

> **关键行中文注释**  
> - `cur_lcm = lcm(cur_lcm, coins[i])`：把当前子集的 LCM 不断累乘，得到子集全部硬币的最小公倍数。  
> - `if cur_lcm > x: break`：如果 LCM 已经超过搜索上限 `x`，`x // cur_lcm` 为 0，后面的硬币再加入只会更大，直接跳出子集循环可以省时。  
> - `if bits % 2 == 1: total += cnt else: total -= cnt`：容斥原理的奇偶加减规则。  
> - 二分循环 `while lo < hi`：每次把搜索区间缩小一半，直到最小满足条件的 `lo` 为答案。

#### 复杂度

- **时间复杂度**：`O(2^n * log(max_answer))`  
  - `2^n`（最多 32768）是遍历所有子集的次数。  
  - `log(max_answer)` 约等于 `log(min(coins) * k)`，`k ≤ 2·10⁹`，所以最多约 60 次二分。  
  - 综合来看，大约 `32768 * 60 ≈ 2·10⁶` 次基本运算，轻松跑在 1 秒以内。

- **空间复杂度**：`O(1)`（不计递归栈）  
  - 只用了若干整数变量，未额外分配与 `n`、`k` 成正比的数组。  

> 与暴力解相比，**时间从线性 `k` 降到了对数 `log(k)`**，空间也从 `O(k)` 降到了常数级，彻底突破了大数值的限制。

---

## 心得

- **核心技巧**：**容斥原理 + 二分搜索**。  
  - 先把“到底有多少个合法金额”这个计数问题抽象出来，用容斥快速求解。  
  - 再在答案空间上二分，找到第 `k` 小的阈值。

- **适用的题型**  
  1. “给定若干集合，求 ≤ X 的元素总数”——如 **“有多少整数同时被若干数整除”**。  
  2. “在无限序列中找第 k 小的数”，常用二分+计数（如 **Ugly Number**、**Kth Missing Positive Number**）。  
  3. “多种约束下的计数问题”，需要容斥或 Inclusion‑Exclusion（如 **“求满足至少一个条件的元素个数”**）。

- **一句话总结**：**把“枚举”换成“计数”，再用二分定位**，是处理 “第 k 小” 类问题的万能钥匙。

---

## 反思

- **第一反应**：直接把每种硬币的倍数合并，用堆/集合逐个生成第 `k` 小的金额。  
- **最容易踩的坑**  
  - 忽视 `k` 可能高达 `2·10⁹`，导致暴力枚举根本不可行。  
  - 容斥时忘记对 **LCM 超过上限** 的子集提前剪枝，会产生不必要的计算甚至整数溢出。  
  - 二分的上界选得不够紧（比如用了 `max(coins) * k`），仍能通过但会多做约 2 倍的二分步数。  

- **下次遇到同类题**：第一步先**思考是否能把“是否 ≤ X”转化为一个可以快速求值的计数函数**；如果可以，就立刻用二分搜索答案，而不是逐个枚举。这样可以把时间复杂度从线性降到对数，轻松应对大输入。