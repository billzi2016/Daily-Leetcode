# #2312. 木块出售 / Selling Pieces of Wood

> 难度：困难 · 标签：Array、Dynamic Programming、Memoization · [LeetCode 链接](https://leetcode.com/problems/selling-pieces-of-wood/)

---

## 题目（英文原版）

**Description**

You are given two integers m and n that represent the height and width of a rectangular piece of wood. You are also given a 2D integer array prices, where prices[i] = [hi, wi, pricei] indicates you can sell a rectangular piece of wood of height hi and width wi for pricei dollars.
To cut a piece of wood, you must make a vertical or horizontal cut across the entire height or width of the piece to split it into two smaller pieces. After cutting a piece of wood into some number of smaller pieces, you can sell pieces according to prices. You may sell multiple pieces of the same shape, and you do not have to sell all the shapes. The grain of the wood makes a difference, so you cannot rotate a piece to swap its height and width.
Return the maximum money you can earn after cutting an m x n piece of wood.
Note that you can cut the piece of wood as many times as you want.

**Examples**

**Example 1:**

```
Input: m = 3, n = 5, prices = [[1,4,2],[2,2,7],[2,1,3]]
Output: 19
Explanation: The diagram above shows a possible scenario. It consists of:
- 2 pieces of wood shaped 2 x 2, selling for a price of 2 * 7 = 14.
- 1 piece of wood shaped 2 x 1, selling for a price of 1 * 3 = 3.
- 1 piece of wood shaped 1 x 4, selling for a price of 1 * 2 = 2.
This obtains a total of 14 + 3 + 2 = 19 money earned.
It can be shown that 19 is the maximum amount of money that can be earned.
```

**Example 2:**

```
Input: m = 4, n = 6, prices = [[3,2,10],[1,4,2],[4,1,3]]
Output: 32
Explanation: The diagram above shows a possible scenario. It consists of:
- 3 pieces of wood shaped 3 x 2, selling for a price of 3 * 10 = 30.
- 1 piece of wood shaped 1 x 4, selling for a price of 1 * 2 = 2.
This obtains a total of 30 + 2 = 32 money earned.
It can be shown that 32 is the maximum amount of money that can be earned.
Notice that we cannot rotate the 1 x 4 piece of wood to obtain a 4 x 1 piece of wood.
```

**Constraints**

- 1 <= m, n <= 200
- 1 <= prices.length <= 2 * 104
- prices[i].length == 3
- 1 <= hi <= m
- 1 <= wi <= n
- 1 <= pricei <= 106
- All the shapes of wood (hi, wi) are pairwise distinct.

---

## 题目（中文翻译）

给定两个整数 `m` 和 `n`，分别表示一块矩形木板的高度和宽度。还给定一个二维整数数组 `prices`，其中 `prices[i] = [hi, wi, pricei]` 表示可以将高度为 `hi`、宽度为 `wi` 的矩形木块以 `pricei` 美元的价格出售。

对木板进行切割时，必须沿整个高度或宽度做一次**垂直切割**（vertical cut）或**水平切割**（horizontal cut），将其分成两个更小的木块。将木板切割成若干更小的木块后，可根据 `prices` 中的记录出售这些木块。可以出售多个形状相同的木块，也可以不出售某些形状的木块。由于木纹的方向不同，**不能旋转**（rotate）木块来交换其高度和宽度。

返回在对 `m × n` 的木板进行任意次数切割后，能够获得的最大收益。

> 注意：木板可以切割任意次数。

## 示例

### 示例 1

**输入**  
`m = 3, n = 5, prices = [[1,4,2],[2,2,7],[2,1,3]]`

**输出**  
`19`

**解释**  
下图展示了一种可能的切割方案，包含以下木块：

- 2 块尺寸为 `2 × 2` 的木块，收益 `2 * 7 = 14`  
- 1 块尺寸为 `2 × 1` 的木块，收益 `1 * 3 = 3`  
- 1 块尺寸为 `1 × 4` 的木块，收益 `1 * 2 = 2`

总收益为 `14 + 3 + 2 = 19`。

### 示例 2

**输入**  
`m = 4, n = 6, prices = [[3,2,10],[1,4,2],[4,1,3]]`

**输出**  
`32`

**解释**  
下图展示了一种可能的切割方案，包含以下木块：

- 3 块尺寸为 `3 × 2` 的木块，收益 `3 * 10 = 30`  
- 1 块尺寸为 `1 × 4` 的木块，收益 `1 * 2 = 2`

总收益为 `30 + 2 = 32`。可以证明 32 是能够获得的最大收益。

## 约束条件

- `1 <= m, n <= 200`
- `1 <= prices.length <= 2 * 10^4`
- `prices[i].length == 3`
- `1 <= hi <= m`
- `1 <= wi <= n`
- `1 <= pricei <= 10^6`
- 所有木块形状 `(hi, wi)` 互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把整块 `m × n` 的木板看成“一块大披萨”。  
我们可以做两件事：

1. **直接卖**：如果价格表里恰好有尺寸 `(m, n)`，我们可以一次性卖掉，得到 `price`。
2. **切一刀**：把木板**整条**横切或竖切，分成两块更小的矩形。然后把这两块继续按同样的规则处理。

这就形成了一棵**递归树**：每个节点代表当前的矩形尺寸，子节点是一次切割后得到的两个子矩形。遍历整棵树，取所有可能的卖价之和的最大值，就是答案。

我们需要：

- 一个**哈希表**（可以类比成“查字典”），`price_map[(h,w)] = price`，把 `prices` 转成方便 O(1) 查找的结构。  
- 一个递归函数 `dfs(h, w)`，返回把尺寸 `h × w` 的木板切完后能得到的最大收益。

递归的**终止条件**：

- 当 `h == 0` 或 `w == 0` 时，木板不存在，收益为 0。  
- 当 `h × w` 在 `price_map` 中有对应的卖价时，**可以选择直接卖**，但仍要继续尝试切割，因为切后再卖可能更划算。

#### 代码（Python）

```python
from functools import lru_cache

def sellingWood_bruteforce(m: int, n: int, prices):
    # 把价格表变成字典，查价就像查字典一样快
    price_map = {(h, w): p for h, w, p in prices}

    @lru_cache(maxsize=None)          # 记忆化，防止重复计算同样的尺寸
    def dfs(h: int, w: int) -> int:
        if h == 0 or w == 0:          # 没有木头了，收益 0
            return 0

        best = price_map.get((h, w), 0)   # 直接卖的收益（如果有的话）

        # --------- 尝试所有可能的竖切 ----------
        # 把宽度 w 切成 k 和 w-k，k 从 1 到 w-1
        for k in range(1, w):
            # 左边 + 右边的最大收益
            cand = dfs(h, k) + dfs(h, w - k)
            best = max(best, cand)

        # --------- 尝试所有可能的横切 ----------
        # 把高度 h 切成 t 和 h-t，t 从 1 到 h-1
        for t in range(1, h):
            cand = dfs(t, w) + dfs(h - t, w)
            best = max(best, cand)

        return best

    return dfs(m, n)
```

> **关键行中文注释**已经写在代码里，帮助你快速对号入座。

#### 复杂度

- **时间复杂度**：`O(2^(m+n))`（指数级）  
  想象每次切割都产生两个子问题，递归树的深度大约是 `m + n`，每层分支数又在增大，导致计算量呈指数增长。大白话：如果木板稍微大一点，程序就会卡死。

- **空间复杂度**：`O(m·n)`（递归栈 + 记忆化表）  
  `lru_cache` 会把所有出现过的 `(h,w)` 组合存下来，最多 `m·n` 种。递归调用的最大深度是 `m+n`，这在 200 以内也算小。

> 暴力解只能用来验证思路或在极小输入下跑通，真正的答案需要更高效的 DP。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到：

- **瓶颈**在于大量的重复子问题。比如 `dfs(3,5)` 可能在不同的切法里被求了好几遍。
- 每一次**切割**只会把宽度或高度分成两段，**子问题的规模严格变小**，这正好符合**动态规划**（DP）的“最优子结构”特性。

**核心想法**：用 DP 表 `dp[h][w]` 记录把尺寸 `h × w` 的木板切完后能得到的最大收益。  
对于每个 `h,w`，我们有三类选择：

1. **不切，直接卖**（如果有对应价格）。  
2. **竖向切**：在所有可能的切点 `k (1 ≤ k < w)` 中，取  
   `dp[h][k] + dp[h][w‑k]` 的最大值。  
3. **横向切**：在所有可能的切点 `t (1 ≤ t < h)` 中，取  
   `dp[t][w] + dp[h‑t][w]` 的最大值。

`dp[h][w]` 就是这三者的最大值。  
因为 `dp` 只依赖于 **更小的** `h` 或 `w`，我们可以**自底向上**地填表，或者使用**记忆化递归**（自顶向下）都行。这里用自底向上的写法，思路更直观，且不依赖 `functools.lru_cache`。

**填表顺序**：先遍历所有可能的高度 `h = 1 … m`，再遍历宽度 `w = 1 … n`。这样在计算 `dp[h][w]` 时，所有需要的子状态 `dp[<h][w]`、`dp[h][<w]` 已经计算完毕。

#### 代码（Python）

```python
def sellingWood_dp(m: int, n: int, prices):
    # 1. 把价格表转成字典，方便 O(1) 查价
    price_map = {(h, w): p for h, w, p in prices}

    # 2. 建立 DP 表，dp[h][w] 表示尺寸 h×w 的最大收益
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 3. 按照从小到大的顺序填表
    for h in range(1, m + 1):
        for w in range(1, n + 1):
            # (a) 直接卖的收益（如果有的话）
            best = price_map.get((h, w), 0)

            # (b) 竖向切：把宽度 w 切成 k 与 w‑k
            for k in range(1, w // 2 + 1):   # 对称切点只算一半，省一半时间
                cand = dp[h][k] + dp[h][w - k]
                if cand > best:
                    best = cand

            # (c) 横向切：把高度 h 切成 t 与 h‑t
            for t in range(1, h // 2 + 1):   # 同理，只算一半
                cand = dp[t][w] + dp[h - t][w]
                if cand > best:
                    best = cand

            dp[h][w] = best   # 保存答案，供更大的子问题使用

    return dp[m][n]
```

> **代码要点**  
> - `price_map.get((h,w),0)` 就像在字典里查“这个尺寸有没有对应的价钱”，没有的话返回 0。  
> - 为了省时间，竖切和横切只遍历到一半（`w//2`、`h//2`），因为切点 `k` 与 `w‑k` 对称，取最大时不需要重复计算。  
> - 最外层的两层 `for` 循环保证了“先算小块，再算大块”，这正是 DP 的核心。

#### 复杂度

- **时间复杂度**：`O(m·n·(m+n))`  
  - 对每个 `h,w`（共 `m·n` 个格子）我们遍历 `O(w)` 次竖切和 `O(h)` 次横切。  
  - 最坏情况 `m=n=200` 时约为 `200·200·(200+200)=1.6×10⁷` 次基本运算，完全可以在毫秒级跑完。  
  - 大白话：我们只把每一种尺寸算一次，且每次只看几条切线，比暴力的指数级快了 **几百倍甚至上千倍**。

- **空间复杂度**：`O(m·n)`  
  - DP 表占用 ` (m+1)·(n+1) ` 个整数。  
  - 相比递归栈，这种固定大小的表更节省内存，也更容易调试。

---

## 心得

- **核心技巧**：**二维动态规划 + 记忆化**（把“切了再卖”转化为子矩形的最优子结构）。  
- **适用场景**（类似题目）  
  1. **Chocolate Cutting**（把巧克力块切成指定大小的子块求最大价值）。  
  2. **Board Cutting**（把棋盘切成若干块，每块有不同收益）。  
  3. **Stone Game VII**（在一维上切割，求最大差值的 DP 思路）。  
- **一句话总结解题钥匙**：  
  *“把每一次切割看成把大问题拆成两个独立的子问题，记住每种尺寸的最优收益，循环填表即可”。*

---

## 反思

- **第一反应**：看到“可以无限次切”，立刻想到递归枚举所有切法。  
- **最容易踩的坑**  
  1. **忘记不能旋转**：`(h,w)` 与 `(w,h)` 不是同一种形状，价格表里只能原样匹配。  
  2. **边界遗漏**：尺寸为 `1` 的木板仍然可以再切（竖切或横切会产生 `0` 宽/高的子块），必须保证 `dp[0][*] = dp[*][0] = 0`。  
  3. **重复计算**：若不做记忆化或 DP 表，指数级递归会导致超时。  
- **下次类似题**的第一步：  
  *先判断是否存在“最优子结构”（把大块切成两块后收益是子块收益之和），再决定使用记忆化递归或自底向上 DP。*