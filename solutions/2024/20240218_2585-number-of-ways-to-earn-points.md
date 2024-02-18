# #2585. 获得积分的方案数 / Number of Ways to Earn Points

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-earn-points/)

---

## 题目（英文原版）

**Description**

There is a test that has n types of questions. You are given an integer target and a 0-indexed 2D integer array types where types[i] = [counti, marksi] indicates that there are counti questions of the ith type, and each one of them is worth marksi points.
Return the number of ways you can earn exactly target points in the exam. Since the answer may be too large, return it modulo 109 + 7.
Note that questions of the same type are indistinguishable.

**Examples**

**Example 1:**

```
Input: target = 6, types = [[6,1],[3,2],[2,3]]
Output: 7
Explanation: You can earn 6 points in one of the seven ways:
- Solve 6 questions of the 0th type: 1 + 1 + 1 + 1 + 1 + 1 = 6
- Solve 4 questions of the 0th type and 1 question of the 1st type: 1 + 1 + 1 + 1 + 2 = 6
- Solve 2 questions of the 0th type and 2 questions of the 1st type: 1 + 1 + 2 + 2 = 6
- Solve 3 questions of the 0th type and 1 question of the 2nd type: 1 + 1 + 1 + 3 = 6
- Solve 1 question of the 0th type, 1 question of the 1st type and 1 question of the 2nd type: 1 + 2 + 3 = 6
- Solve 3 questions of the 1st type: 2 + 2 + 2 = 6
- Solve 2 questions of the 2nd type: 3 + 3 = 6
```

**Example 2:**

```
Input: target = 5, types = [[50,1],[50,2],[50,5]]
Output: 4
Explanation: You can earn 5 points in one of the four ways:
- Solve 5 questions of the 0th type: 1 + 1 + 1 + 1 + 1 = 5
- Solve 3 questions of the 0th type and 1 question of the 1st type: 1 + 1 + 1 + 2 = 5
- Solve 1 questions of the 0th type and 2 questions of the 1st type: 1 + 2 + 2 = 5
- Solve 1 question of the 2nd type: 5
```

**Example 3:**

```
Input: target = 18, types = [[6,1],[3,2],[2,3]]
Output: 1
Explanation: You can only earn 18 points by answering all questions.
```

**Constraints**

- 1 <= target <= 1000
- n == types.length
- 1 <= n <= 50
- types[i].length == 2
- 1 <= counti, marksi <= 50

---

## 题目（中文翻译）

**题目描述**  
有一场考试包含 n 种不同类型的题目。给定整数 **目标分数（target）** 和一个下标从 0 开始的二维整数数组 **类型数组（types）**，其中 `types[i] = [count_i, marks_i]` 表示第 i 类题目共有 `count_i` 道，每道题的分值为 `marks_i` 分。  

返回在考试中恰好获得 **目标分数（target）** 的不同做题方案数。由于答案可能非常大，请返回 **10⁹ + 7** 取模后的结果。  

注意，同一种类的题目是不可区分的。

**示例**  

**示例 1**  
```
Input: target = 6, types = [[6,1],[3,2],[2,3]]
Output: 7
```
**解释**：获得 6 分有以下 7 种方案：
- 解答 0 类题目 6 道：`1 + 1 + 1 + 1 + 1 + 1 = 6`
- 解答 0 类题目 4 道，1 类题目 1 道：`1 + 1 + 1 + 1 + 2 = 6`
- 解答 0 类题目 2 道，1 类题目 2 道：`1 + 1 + 2 + 2 = 6`
- 解答 0 类题目 3 道，1 类题目 1 道，2 类题目 1 道：`1 + 1 + 1 + 2 + 1 = 6`
- 解答 0 类题目 1 道，1 类题目 2 道，2 类题目 1 道：`1 + 2 + 2 + 1 = 6`
- 解答 0 类题目 0 道，1 类题目 3 道：`2 + 2 + 2 = 6`
- 解答 2 类题目 2 道：`3 + 3 = 6`

**示例 2**  
```
Input: target = 5, types = [[50,1],[50,2],[50,5]]
Output: 4
```
**解释**：获得 5 分有以下 4 种方案：
- 解答 0 类题目 5 道：`1 + 1 + 1 + 1 + 1 = 5`
- 解答 0 类题目 3 道，1 类题目 1 道：`1 + 1 + 1 + 2 = 5`
- 解答 0 类题目 1 道，1 类题目 2 道：`1 + 2 + 2 = 5`
- 解答 2 类题目 1 道：`5`

**示例 3**  
```
Input: target = 18, types = [[6,1],[3,2],[2,3]]
Output: 1
```
**解释**：只能通过答完所有题目得到 18 分。

**约束条件**  
- `1 <= target <= 1000`  
- `n == types.length`  
- `1 <= n <= 50`  
- `types[i].length == 2`  
- `1 <= count_i, marks_i <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一种题目 **逐个枚举**，看能否凑出 `target` 分。  
我们可以把 `types` 看成若干「盒子」：

* 第 `i` 盒子里有 `count_i` 个相同的球（题目），每个球的价值是 `marks_i` 分。  
* 盒子里的球是 **不可区分** 的——只要取了 `k` 个，具体是哪 `k` 个都算同一种情况。

于是我们只需要遍历所有可能的取法 `(k0, k1, …, kn‑1)`，其中 `0 ≤ ki ≤ count_i`，检查

```
k0 * marks_0 + k1 * marks_1 + … + kn‑1 * marks_n‑1 == target
```

如果相等，就记作一种合法的方案。  

> **为什么能得到正确答案？**  
> 因为我们把所有合法的取法都穷举了一遍，且每一种取法只会出现一次（题目同类不可区分），所以计数必然完整且不重复。

**时间/空间复杂度**  
- 时间复杂度：`O( Π (count_i + 1) )`，即所有盒子取法的乘积。  
  - 用大白话讲，就是“把每个盒子里所有可能的取法全部列出来”，如果有 5 种题目，每种最多 10 题，那么最坏要检查 `11^5 ≈ 1.6 万` 种组合。实际 `count_i` 可达 50，组合数会爆炸，根本跑不完。  
- 空间复杂度：`O(n)`（递归栈或循环中保存的当前取法），几乎可以忽略。

显然，这种「暴力」方法只能在 **极小的输入** 下使用，不能直接通过题目的限制（`target ≤ 1000, n ≤ 50, count_i ≤ 50`）。

#### 代码（Python）

```python
MOD = 10**9 + 7

def ways_bruteforce(target, types):
    n = len(types)
    ans = 0

    def dfs(idx, cur):
        """枚举第 idx 种题目取了多少，cur 为当前累计的分数"""
        nonlocal ans
        if cur > target:          # 已经超过目标，剪枝
            return
        if idx == n:              # 所有类型都枚举完了
            if cur == target:
                ans = (ans + 1) % MOD
            return

        cnt, mark = types[idx]
        # 取 0~cnt 个当前类型的题目
        for k in range(cnt + 1):
            dfs(idx + 1, cur + k * mark)

    dfs(0, 0)
    return ans
```

> **关键行中文注释**  
> - `if cur > target:`：如果当前分数已经超过目标，后面的选择只会让分数更大，直接返回剪枝。  
> - `for k in range(cnt + 1):`：枚举「取多少」这一步是暴力的核心。

#### 复杂度

- **时间复杂度**：`O( Π (count_i + 1) )`，组合数呈指数增长。  
- **空间复杂度**：`O(n)`，递归栈深度最多 `n`（≤ 50），几乎可以忽略。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**状态只和已经处理的题目类型以及累计的分数有关**。  
这正好符合「**动态规划（Dynamic Programming）**」的思路：把大问题拆成子问题，记忆化子问题的答案，避免重复计算。

我们把 `types` 看成 **有顺序的**（先处理第 0 种，再处理第 1 种……），定义：

```
dp[i][p] = 用前 i 种题目（0 … i‑1）恰好得到 p 分的方案数
```

- `i` 范围：`0 … n`（`i = 0` 表示还没处理任何题目）。
- `p` 范围：`0 … target`。

**状态转移**  
对于第 `i` 种题目（记作 `cnt, mark`），我们可以选择取 `k` 个（`0 ≤ k ≤ cnt`），只要 `k * mark ≤ p`。于是：

```
dp[i+1][p] = Σ dp[i][p - k * mark]   (k 从 0 到 cnt，且 p - k*mark ≥ 0)
```

这就是「**有界背包**」的经典转移式。  
直观看，这一步把「把第 i 种题目加入已有的方案」的所有可能都加了进来。

**为什么暴力慢**  
在暴力里，我们每次都从头重新遍历所有已选的题目组合，导致大量重复计算。  
DP 把「已经算好的子结果」存下来，后面只需要 **查表**（`dp[i][...]`），时间大幅下降。

**进一步优化**  
上面的转移式里，内层的 `k` 循环会导致 `O(cnt)` 的额外乘子。  
因为 `cnt ≤ 50`，`target ≤ 1000`，`n ≤ 50`，直接实现的时间是：

```
O(n * target * max(cnt))  ≤ 50 * 1000 * 50 = 2.5 * 10⁶
```

2.5 百万次运算在 Python 中完全可以接受，故这里直接使用 **二维 DP**（或者一维滚动数组）即可，无需更复杂的「单调队列」优化。

**实现细节**  

1. 初始化 `dp[0][0] = 1`（不选任何题目得到 0 分只有一种方式）。其余为 0。  
2. 按题目类型遍历，依次填充 `dp[i+1][*]`。  
3. 所有加法都取模 `10⁹+7` 防止溢出。  
4. 最终答案是 `dp[n][target]`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def ways_dp(target, types):
    n = len(types)
    # dp[i][p]：前 i 种题目得到 p 分的方案数
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 1                         # base case

    for i, (cnt, mark) in enumerate(types):
        for p in range(target + 1):
            # 不选第 i 种题目的情况（k = 0）
            dp[i + 1][p] = dp[i][p]      # 先把不选的方案复制下来
        # 现在把选 1~cnt 个第 i 种题目的情况加进去
        for k in range(1, cnt + 1):
            cost = k * mark
            if cost > target:            # 超过 target 的直接跳过
                break
            for p in range(cost, target + 1):
                # 把「已经用了前 i 种，且剩下 p‑cost 分」的方案数加进来
                dp[i + 1][p] = (dp[i + 1][p] + dp[i][p - cost]) % MOD

    return dp[n][target]
```

> **关键行中文注释**  
> - `dp[0][0] = 1`：没有任何题目时，得到 0 分只有一种办法（什么都不做）。  
> - `dp[i + 1][p] = dp[i][p]`：先把「不选当前类型」的方案直接搬过去。  
> - `for k in range(1, cnt + 1):`：枚举「选了多少个」当前类型的题目。  
> - `dp[i + 1][p] = (dp[i + 1][p] + dp[i][p - cost]) % MOD`：把「前 i 种已经得到 p‑cost 分」的方案数累计进来。

**空间进一步压缩**  
因为 `dp[i+1][*]` 只依赖 `dp[i][*]`（上一层），可以使用 **一维滚动数组** 把空间降到 `O(target)`：

```python
def ways_dp_1d(target, types):
    dp = [0] * (target + 1)
    dp[0] = 1
    for cnt, mark in types:
        ndp = dp[:]                     # 复制一份作为 “前 i 种”的基线
        for k in range(1, cnt + 1):
            cost = k * mark
            if cost > target:
                break
            for p in range(cost, target + 1):
                ndp[p] = (ndp[p] + dp[p - cost]) % MOD
        dp = ndp
    return dp[target]
```

这里 `ndp` 相当于 `dp[i+1]`，`dp` 相当于 `dp[i]`，逻辑完全相同，只是把二维表压平。

#### 复杂度

- **时间复杂度**：`O(n * target * max(cnt))`  
  - 直白解释：我们遍历每一种题目（最多 50 种），对每一种遍历目标分数（最多 1000），再遍历该题目可能的取数（最多 50），总共约 2.5 百万次操作，跑得很快。  
  - 与暴力解相比，指数级的组合枚举被降到了多项式级别。

- **空间复杂度**：`O(target)`（使用一维滚动数组）或 `O(n * target)`（二维 DP）  
  - `target` 只有 1000，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**有界背包动态规划**——把「每种题目可以选 0~cnt 次」的限制转化为「在每个状态里累加 k 次」的求和。  
- **适用的题型**  
  1. **硬币兑换（Coin Change）**——每种硬币数量有限的版本。  
  2. **装箱/背包（Bounded Knapsack）**——每件物品只能使用有限次。  
  3. **分配物品到固定分数/重量**——如「分配糖果使总甜度恰好为 target」等。

> **一句话总结解题钥匙**：把「选多少」这个循环放进 DP 的状态转移里，用记忆化表把所有子组合一次算完，从而避免指数级的枚举。

---

## 反思

- **第一反应**：看到「每种题目有数量限制」和「要恰好得到 target」立刻想到「背包」或「硬币」类的 DP。  
- **最容易踩的坑**  
  1. **忘记取模**：答案可能非常大，所有加法都要 `% MOD`。  
  2. **边界条件**：`dp[0][0] = 1` 必不可少，表示「什么都不选」的合法性。  
  3. **超出 target 的剪枝**：在内层循环里若 `k * mark > target`，应立即 `break`，否则会产生无意义的遍历。  
- **下次类似题的第一步**：先把「能取多少次」写成「0~cnt」的枚举，然后问自己「这枚举的结果只和已经处理的前几种有什么关系？」——如果答案是「只和前几种以及当前累计分数有关」，就立刻构造 DP 表 `dp[i][score]`。这样思路就清晰了。