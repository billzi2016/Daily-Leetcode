# #1467. **两个盒子拥有相同数量不同颜色球的概率** / Probability of a Two Boxes Having The Same Number of Distinct Balls

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Backtracking、Combinatorics、Probability and Statistics · [LeetCode 链接](https://leetcode.com/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/)

---

## 题目（英文原版）

**Description**

Given 2n balls of k distinct colors. You will be given an integer array balls of size k where balls[i] is the number of balls of color i.
All the balls will be shuffled uniformly at random, then we will distribute the first n balls to the first box and the remaining n balls to the other box (Please read the explanation of the second example carefully).
Please note that the two boxes are considered different. For example, if we have two balls of colors a and b, and two boxes [] and (), then the distribution [a] (b) is considered different than the distribution [b] (a) (Please read the explanation of the first example carefully).
Return the probability that the two boxes have the same number of distinct balls. Answers within 10-5 of the actual value will be accepted as correct.

**Examples**

**Example 1:**

```
Input: balls = [1,1]
Output: 1.00000
Explanation: Only 2 ways to divide the balls equally:
- A ball of color 1 to box 1 and a ball of color 2 to box 2
- A ball of color 2 to box 1 and a ball of color 1 to box 2
In both ways, the number of distinct colors in each box is equal. The probability is 2/2 = 1
```

**Example 2:**

```
Input: balls = [2,1,1]
Output: 0.66667
Explanation: We have the set of balls [1, 1, 2, 3]
This set of balls will be shuffled randomly and we may have one of the 12 distinct shuffles with equal probability (i.e. 1/12):
[1,1 / 2,3], [1,1 / 3,2], [1,2 / 1,3], [1,2 / 3,1], [1,3 / 1,2], [1,3 / 2,1], [2,1 / 1,3], [2,1 / 3,1], [2,3 / 1,1], [3,1 / 1,2], [3,1 / 2,1], [3,2 / 1,1]
After that, we add the first two balls to the first box and the second two balls to the second box.
We can see that 8 of these 12 possible random distributions have the same number of distinct colors of balls in each box.
Probability is 8/12 = 0.66667
```

**Example 3:**

```
Input: balls = [1,2,1,2]
Output: 0.60000
Explanation: The set of balls is [1, 2, 2, 3, 4, 4]. It is hard to display all the 180 possible random shuffles of this set but it is easy to check that 108 of them will have the same number of distinct colors in each box.
Probability = 108 / 180 = 0.6
```

**Constraints**

- 1 <= balls.length <= 8
- 1 <= balls[i] <= 6
- sum(balls) is even.

---

## 题目（中文翻译）

给定 2n 个颜色各不相同的球。输入为长度为 k 的整数数组 `balls`，其中 `balls[i]` 表示颜色 i 的球的数量。  
所有球会 **均匀随机洗牌**（shuffle uniformly at random），随后我们将前 n 个球放入第一个盒子，其余 n 个球放入第二个盒子（请仔细阅读示例 2 的说明）。  
请注意，两个盒子是 **不同** 的（considered different），例如若有两球颜色分别为 a 和 b，两个盒子记为 `[]` 与 `()`，则分配方式 `[a] (b)` 与 `[b] (a)` 被视为不同（请仔细阅读示例 1 的说明）。  

返回两个盒子中 **不同颜色的球的数量相同** 的概率。答案在实际值的 10⁻⁵ 以内均视为正确。

---

### 示例

**示例 1**  
```text
Input: balls = [1,1]
Output: 1.00000
Explanation: 只有两种等分方式：
- 将颜色 1 的球放入盒子 1，颜色 2 的球放入盒子 2
- 将颜色 2 的球放入盒子 1，颜色 1 的球放入盒子 2
两种方式中，每个盒子拥有的不同颜色数量均相等。概率为 2/2 = 1
```

**示例 2**  
```text
Input: balls = [2,1,1]
Output: 0.66667
Explanation: 球的集合为 [1, 1, 2, 3]。  
这些球会随机洗牌，共有 12 种不同的洗牌方式，每种出现概率相等（即 1/12）：
[1,1 / 2,3], [1,1 / 3,2], [1,2 / 1,3], [1,2 / 3,1], [1,3 / 1,2], [1,3 / 2,1],
[2,1 / 1,3], [2,1 / 3,1], [2,3 / 1,1], [3,1 / 1,2], [3,1 / 2,1], [3,2 / 1,1]  
随后我们把前 2 个球放入盒子 1，后 2 个球放入盒子 2。  
在这 12 种情况中，有 8 种使得两个盒子中不同颜色的数量相同，故概率为 8/12 = 0.66667。
```

**示例 3**  
```text
Input: balls = [1,2,1,2]
Output: 0.60000
Explanation: 球的集合为 [1, 2, 2, 3, 4, 4]。  
虽然难以列举全部 180 种随机洗牌，但可以验证其中有 108 种使得两个盒子中不同颜色的数量相等。  
概率 = 108 / 180 = 0.6
```

---

### 约束

- `1 <= balls.length <= 8`
- `1 <= balls[i] <= 6`
- `sum(balls)` 为偶数。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有可能的分配全部枚举一遍**，看哪些分配满足「两个盒子里不同颜色的种类数相同」即可。  

- **数据结构**：我们把每一种颜色的球的数量记在数组 `balls` 中。  
  - 想象 `balls[i]` 就像一本字典里第 `i` 个词的出现次数，**每种颜色是一种“词”，出现的次数就是该词的“页码”。**  
- **枚举方式**：对第 `i` 种颜色的球，我们可以把 `0 … balls[i]` 个放进盒子 1，剩下的放进盒子 2。  
  - 用一个递归（或回溯）把每种颜色的取法都遍历出来，形成一个长度为 `k` 的向量 `(x1, x2, …, xk)`，其中 `xi` 表示第 `i` 种颜色放进盒子 1 的球数。  
- **合法性检查**：  
  - 必须保证盒子 1 正好得到 `n = total/2` 个球：`x1 + x2 + … + xk = n`。  
  - 计算两盒子的不同颜色数：  
    - 盒子 1 的不同颜色数 = `cnt1 = |{ i | xi > 0 }|`  
    - 盒子 2 的不同颜色数 = `cnt2 = |{ i | balls[i] - xi > 0 }|`  
  - 若 `cnt1 == cnt2`，这就是「满足条件」的分配。  
- **统计方式**：每一种 `(xi)` 的出现概率并不是 `1/全部分配数`，而是  
  \[
  \frac{\displaystyle\prod_{i=1}^{k} \binom{balls[i]}{xi}}{\displaystyle\binom{2n}{n}}
  \]  
  其中分子是「从第 `i` 种颜色的 `balls[i]` 个球里挑 `xi` 个」的组合数的乘积，分母是「从全部 `2n` 球里挑 `n` 个」的组合数。  
  - **组合数**（`C(a, b)`）可以类比为「从一本有 `a` 页的字典里挑 `b` 页」的方式数。  

**为什么正确**：  
- 我们枚举了**所有**可能的 `(xi)`，每一种对应唯一的分配方式（不管球的顺序怎样，只要每种颜色的数量分配好，顺序已经在组合数里算进去了）。  
- 把每种分配出现的次数（组合数）相加，除以总的可能次数，正好得到所求概率。  

#### 代码（Python）

```python
from math import comb
from typing import List

def probability_bruteforce(balls: List[int]) -> float:
    k = len(balls)                 # 颜色种类数
    total = sum(balls)             # 2n
    n = total // 2                 # 每个盒子必须得到的球数

    # 先算出总的分配方式数 C(2n, n)
    total_ways = comb(total, n)

    ans = 0.0                      # 累计满足条件的方式数（已经乘上对应的组合数）

    # 递归枚举每种颜色放进盒子1的数量
    def dfs(idx: int, taken: int, cnt1: int, cnt2: int, ways: int):
        """
        idx   : 正在处理第 idx 种颜色
        taken : 目前盒子1已经拿了多少球
        cnt1  : 盒子1当前的不同颜色数
        cnt2  : 盒子2当前的不同颜色数（已经确定的颜色里出现的种类数）
        ways  : 到目前为止的组合数乘积
        """
        if idx == k:                         # 所有颜色都决定好了
            if taken == n:                    # 正好 n 球
                if cnt1 == cnt2:               # 不同颜色数相等
                    nonlocal ans
                    ans += ways                # 加上这条路径的组合数
            return

        c = balls[idx]                       # 第 idx 种颜色的球数
        # 枚举把 xi 个球放进盒子1（0 <= xi <= c）
        for xi in range(c + 1):
            new_taken = taken + xi
            if new_taken > n:                # 超过 n 球直接剪枝
                break
            # 更新两盒子的不同颜色数
            new_cnt1 = cnt1 + (1 if xi > 0 else 0)
            new_cnt2 = cnt2 + (1 if c - xi > 0 else 0)
            # 这一步的组合数是 C(c, xi)
            new_ways = ways * comb(c, xi)
            dfs(idx + 1, new_taken, new_cnt1, new_cnt2, new_ways)

    dfs(0, 0, 0, 0, 1)   # 从第 0 种颜色开始，初始计数全为 0，组合数为 1

    # 概率 = 满足条件的方式数 / 所有可能的方式数
    return ans / total_ways
```

- 关键行已经加上中文注释，直接运行即可得到答案。

#### 复杂度  

- **时间复杂度**：  
  - 我们对每种颜色最多枚举 `balls[i] + 1 ≤ 7` 次。  
  - 最坏情况下的枚举树大小是 \(\prod_{i=1}^{k} (balls[i] + 1)\)。  
  - 受约束 `k ≤ 8, balls[i] ≤ 6`，所以最多约为 \(7^8 ≈ 5.7\) 万次，完全可以接受。  
  - 用大白话说：**时间随颜色种类和每种颜色的球数指数增长**，但因为限制很小，实际运行几毫秒。

- **空间复杂度**：  
  - 递归深度最多 `k ≤ 8`，再加上常数级的临时变量，**O(k)**，几乎可以忽略不计。

---

### 2. 最优解  

#### 思路  

暴力解已经能跑通，但我们可以把「枚举所有 (xi)」的过程用**动态规划**（DP）写得更紧凑、更易于理解，也能避免重复计算。  

**慢在哪里？**  
- 暴力递归每走到一个状态都会重新计算子树的组合数乘积。  
- 实际上，**相同的「已处理颜色数」+「已选球数」+「两盒子颜色数差」** 会出现多次，完全可以把它们的结果记下来，后面直接复用。  

**核心想法**：  
- 用 DP 按颜色逐步累加，每一步只记录「已经选了多少球」以及「两盒子颜色种类数的差值」(`diff = cnt1 - cnt2`)。  
- `diff` 为负时表示盒子 2 的不同颜色更多，正时相反。  
- 当遍历完所有颜色后，`diff == 0` 且已选球数正好是 `n` 的状态，就是我们要的「满足条件」的方式数。  

**需要的工具**：  
1. **组合数 C(a, b)**  
   - 直接用数学公式 `C(a,b)=a!/(b!·(a-b)!)`。  
   - 为了快速查询，预先算好 `0 … 2n` 的阶乘（factorial），再用公式求组合数。  
   - 阶乘可以类比为「把 1、2、3、…、a 连乘起来」的结果，后面求组合数时只需要把已经算好的乘积相除即可。  

2. **状态定义**  
   - `dp[i][j][d]` = **在前 i 种颜色处理完后**，  
     - 已经挑了 `j` 球放进盒子 1，  
     - 两盒子颜色种类数的差为 `d`（`d` 可能为负），  
     - 对应的 **方式数**（即组合数乘积的和）。  

3. **状态转移**  
   - 对第 `i` 种颜色，球数为 `c = balls[i]`，我们可以选 `x = 0 … c` 球放进盒子 1。  
   - 新的已选球数 `j' = j + x`（必须 ≤ n）。  
   - 新的差值 `d' = d + (1 if x>0 else 0) - (1 if c-x>0 else 0)`。  
   - 乘上本次选法的组合数 `C(c, x)`，累加到 `dp[i+1][j'][d']`。  

4. **答案**  
   - 所有颜色遍历完后（`i = k`），我们只关心 `j = n` 且 `d = 0` 的状态。  
   - `favorable = dp[k][n][0]`。  
   - 总方式数 `total = C(2n, n)`（把所有球随意挑 n 个进盒子 1）。  
   - 最终概率 = `favorable / total`。  

**为什么 DP 正确**  
- DP 把「每种颜色的选法」抽象成独立的决策，每一步只依赖之前的累计信息（已选球数、颜色差），完全符合乘法原理。  
- 因为我们把所有可能的 `x`（从 0 到 `c`）都枚举，并乘以对应的组合数，**每一种合法的全局分配都会被计数一次且仅一次**。  

**类比帮助理解**：  
- 想象你在玩「拼图」：每块拼图代表一种颜色的球，你可以把这块拼图的若干小块（0~c）放进左边的盒子，剩下的放右边。  
- 你手里有两块记事本：一本记录「左边已经放了多少块」 (`j`)，另一本记录「左、右颜色数的差」 (`d`)。  
- 每放一块，你就在记事本上写下新的数字，并把「这块拼图有几种放法」乘进去。最后只看记事本上「左边正好 n 块且差为 0」的那一行，就得到答案。  

#### 代码（Python）

```python
from math import comb
from typing import List

def probability_dp(balls: List[int]) -> float:
    k = len(balls)
    total = sum(balls)          # 2n
    n = total // 2

    # 预计算组合数 C(a, b) 用 factorial（这里直接用 math.comb 也行）
    # 为了让代码更显式，下面手动算阶乘并存进数组
    max_n = total
    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i

    def C(a: int, b: int) -> int:
        if b < 0 or b > a:
            return 0
        return fact[a] // (fact[b] * fact[a - b])

    # dp[i][j][d] 用字典压缩第二、三维，节省空间
    # offset 用来把可能的负 diff 平移为非负索引
    offset = sum(balls)          # 最大可能的 |diff| 不会超过 total
    dp = [ [dict() for _ in range(n + 1)] for _ in range(k + 1) ]
    dp[0][0][offset] = 1        # 初始状态：0 种颜色、0 球、diff = 0（用 offset 表示）

    for i in range(k):                 # 遍历每一种颜色
        c = balls[i]                    # 该颜色的球数
        for j in range(n + 1):          # 已经挑了 j 球进盒子1
            for d_key, ways in dp[i][j].items():
                diff = d_key - offset    # 把偏移恢复成真实的 diff
                # 枚举本颜色放进盒子1的球数 x
                for x in range(c + 1):
                    nj = j + x
                    if nj > n:          # 盒子1 不能超过 n 球
                        break
                    # 计算新 diff
                    ndiff = diff + (1 if x > 0 else 0) - (1 if c - x > 0 else 0)
                    nd_key = ndiff + offset
                    add = ways * C(c, x)   # 本轮选法的组合数乘上已有方式数
                    dp[i + 1][nj][nd_key] = dp[i + 1][nj].get(nd_key, 0) + add

    favorable = dp[k][n].get(offset, 0)   # diff == 0 对应的键是 offset
    total_ways = C(total, n)
    return favorable / total_ways
```

- **关键注释**已在代码中给出，帮助你一步步对应到思路。  
- 使用 `dict` 存储 `diff`，可以只保留实际出现的差值，避免创建巨大的三维数组。  

#### 复杂度  

- **时间复杂度**  
  - 外层遍历 `k ≤ 8` 种颜色。  
  - 对每种颜色我们遍历 `j = 0 … n`（最多 24）以及所有出现过的 `diff`（范围约 `[-total, total]`，实际出现的远少于 2·total）。  
  - 每个状态内部再遍历 `x = 0 … balls[i] ≤ 6`。  
  - 整体大约是 `O(k * n * max_diff * max_ball)`，在最坏情况下约 `8 * 24 * 48 * 6 ≈ 55k` 次运算，远小于暴力的 5.7 万次，而且每次只做常数级的乘除。  

- **空间复杂度**  
  - 我们只保存两层 DP（`i` 与 `i+1`）的状态，使用 `dict` 按需存放。  
  - 最多 `O(n * max_diff)`，即 `≈ 24 * 48 ≈ 1152` 个整数，**几乎可以忽略**。  

与暴力解相比，DP 通过**记忆化**消除了重复子问题，代码结构更清晰，且在更大输入（如 `k=8, balls[i]=6`）时依然保持快速。

---

## 心得  

- **核心技巧**：**枚举每种颜色分配的数量 + 组合数计数 + 动态规划压缩状态**。  
- **适用的题型**：  
  1. “把多种物品分成两堆，使两堆满足某种计数相等”——如 *分割数组使两边和相等*（子集和）  
  2. “在多颜色球中抽取固定数量，求颜色分布的概率”——如 *颜色相同的概率*（本题）  
  3. “多维背包/计数 DP”——比如 *不同种类的硬币分配*、*装箱问题*  

- **一句话总结解题钥匙**：**把“把每种颜色的球分配多少”当成独立决策，用组合数计数，再用 DP 累计所有决策的方式数**。

---

## 反思  

- **第一反应**：看到“随机打乱后前 n 球进盒子 1”，立刻想到“等价于直接从全部球里挑 n 球”。这一步把乱序的过程简化为组合计数。  
- **最容易踩的坑**：  
  1. **忘记把两盒子视为有序**——题目强调盒子 1 与盒子 2 不相同，不能把 `[a] (b)` 与 `(b) [a]` 合并。  
  2. **边界条件**：`xi = 0` 或 `xi = balls[i]` 时对应的颜色在另一盒子仍然出现，需要正确更新 `cnt1 / cnt2`（使用 `>0` 判断）。  
  3. **组合数溢出/精度**：在 Python 中使用整数阶乘不会溢出，但在语言里需要用 `long double` 或 `bigint`。最终概率用浮点除法即可，误差容忍 `1e-5`。  
- **下次类似题的第一步**：**先把随机过程抽象为“从全集中挑固定大小的子集”，再思考每种元素的选取次数如何影响目标属性**。这样就能快速定位到“枚举每种元素的选取数量 + 组合数计数”的思路。