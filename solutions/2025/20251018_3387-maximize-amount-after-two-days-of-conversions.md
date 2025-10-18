# #3387. 两天转换后最大金额 / Maximize Amount After Two Days of Conversions

> 难度：中等 · 标签：Array、String、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/maximize-amount-after-two-days-of-conversions/)

---

## 题目（英文原版）

**Description**

You are given a string initialCurrency, and you start with 1.0 of initialCurrency.
You are also given four arrays with currency pairs (strings) and rates (real numbers):
You can perform any number of conversions, including zero, using rates1 on day 1, followed by any number of additional conversions, including zero, using rates2 on day 2.
Return the maximum amount of initialCurrency you can have after performing any number of conversions on both days in order.
Note: Conversion rates are valid, and there will be no contradictions in the rates for either day. The rates for the days are independent of each other.

**Examples**

**Example 1:**

```
Input: initialCurrency = "EUR", pairs1 = [["EUR","USD"],["USD","JPY"]], rates1 = [2.0,3.0], pairs2 = [["JPY","USD"],["USD","CHF"],["CHF","EUR"]], rates2 = [4.0,5.0,6.0]
Output: 720.00000
Explanation:
To get the maximum amount of EUR , starting with 1.0 EUR :
```

**Example 2:**

```
Input: initialCurrency = "NGN", pairs1 = [["NGN","EUR"]] , rates1 = [9.0] , pairs2 = [["NGN","EUR"]] , rates2 = [6.0]
Output: 1.50000
Explanation:
Converting NGN to EUR on day 1 and EUR to NGN using the inverse rate on day 2 gives the maximum amount.
```

**Example 3:**

```
Input: initialCurrency = "USD", pairs1 = [["USD","EUR"]], rates1 = [1.0], pairs2 = [["EUR","JPY"]], rates2 = [10.0]
Output: 1.00000
Explanation:
In this example, there is no need to make any conversions on either day.
```

**Constraints**

- 1 <= initialCurrency.length <= 3
- initialCurrency consists only of uppercase English letters.
- 1 <= n == pairs1.length <= 10
- 1 <= m == pairs2.length <= 10
- pairs1[i] == [startCurrencyi, targetCurrencyi]
- pairs2[i] == [startCurrencyi, targetCurrencyi]
- 1 <= startCurrencyi.length, targetCurrencyi.length <= 3
- startCurrencyi and targetCurrencyi consist only of uppercase English letters.
- rates1.length == n
- rates2.length == m
- 1.0 <= rates1[i], rates2[i] <= 10.0
- The input is generated such that there are no contradictions or cycles in the conversion graphs for either day.
- The input is generated such that the output is at most 5 * 1010.

---

## 题目（中文翻译）

**描述**  
给定一个字符串 `initialCurrency`，你从 1.0 单位的 `initialCurrency` 开始。  
同时提供四个数组，分别描述两天的货币对（字符串）和汇率（实数）：

- `pairs1` 与 `rates1` 表示第 1 天的可用货币对及其汇率  
- `pairs2` 与 `rates2` 表示第 2 天的可用货币对及其汇率  

你可以在第 1 天使用任意次数（包括零次）的转换，汇率取自 `rates1`；随后在第 2 天再使用任意次数（包括零次）的转换，汇率取自 `rates2`。  
返回在按照上述顺序完成任意次数转换后，能够拥有的最多的 `initialCurrency` 数量。

**注意**  
- 所有汇率均是有效的，且同一天内的汇率不存在矛盾。  
- 两天的汇率相互独立。  

---

### 示例

#### 示例 1  
```text
Input: initialCurrency = "EUR",
       pairs1 = [["EUR","USD"],["USD","JPY"]], rates1 = [2.0,3.0],
       pairs2 = [["JPY","USD"],["USD","CHF"],["CHF","EUR"]], rates2 = [4.0,5.0,6.0]
Output: 720.00000
Explanation:
要在起始的 1.0 EUR 基础上得到最多的 EUR：

1. 第一天：
   - EUR → USD，汇率 2.0，得到 2.0 USD
   - USD → JPY，汇率 3.0，得到 6.0 JPY

2. 第二天：
   - JPY → USD，汇率 4.0，得到 24.0 USD
   - USD → CHF，汇率 5.0，得到 120.0 CHF
   - CHF → EUR，汇率 6.0，得到 720.0 EUR
```

#### 示例 2  
```text
Input: initialCurrency = "NGN",
       pairs1 = [["NGN","EUR"]], rates1 = [9.0],
       pairs2 = [["NGN","EUR"]], rates2 = [6.0]
Output: 1.50000
Explanation:
在第 1 天将 NGN 换成 EUR，然后在第 2 天使用逆向汇率将 EUR 再换回 NGN，可得到最大金额。
```

#### 示例 3  
```text
Input: initialCurrency = "USD",
       pairs1 = [["USD","EUR"]], rates1 = [1.0],
       pairs2 = [["EUR","JPY"]], rates2 = [10.0]
Output: 1.00000
Explanation:
本例中，无需在任意一天进行转换，保持原有的 1.0 USD 即为最大值。
```

---

### 约束条件
- `1 <= initialCurrency.length <= 3`
- `initialCurrency` 仅由大写英文字母组成
- `1 <= n == pairs1.length <= 10`
- `1 <= m == pairs2.length <= 10`
- `pairs1[i] == [startCurrency_i, targetCurrency_i]`
- `pairs2[i] == [startCurrency_i, targetCurrency_i]`
- `1 <= startCurrency_i.length, targetCurrency_i.length <= 3`
- `startCurrency_i` 与 `targetCurrency_i` 仅由大写英文字母组成
- `rates1.length == n`
- `rates2.length == m`
- `1.0 <= rates1[i], rates2[i] <= 10.0`
- 输入保证同一天的转换图不存在矛盾或环路
- 输入保证输出不超过 `5 * 10^10`  

---

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把每一天的兑换规则看成一张**有向图**：  
- **节点** = 货币（比如 `EUR、USD、JPY`）。  
- **有向边** = 可以直接兑换的货币对，边权 = 兑换比例（比如 `EUR → USD` 的比例是 `2.0`）。  

我们从 `initialCurrency` 出发，在第 1 天可以走任意条有向边（可以走零条），把手里的钱乘上对应的比例；第 2 天再在另一张图上走任意条有向边，最后要回到 `initialCurrency`。  

**暴力做法**就是对每一天分别**枚举所有可能的兑换路径**，记录从起点到每个货币的最大乘积（即最大能换到多少该货币），随后在第二天再枚举所有路径，找出“先在第一天换到 X → 再在第二天把 X 换回起始货币”的最大乘积。

> **类比**：把图想象成一张城市地图，边的权重是从一个城市到另一个城市的“燃油折算率”。我们想找出从出发城市出发，先在第一天走任意路线到某个中转城市，再在第二天走任意路线回到出发城市，能够让油箱里的油最多的路线。

因为题目保证每一天的图中**不存在矛盾的汇率**（即不存在能让我们无限放大的环），所以即使我们在枚举时不特意去掉环，乘积也不会无限增长，只会在遍历完所有可能的路径后得到一个最大值。

**实现细节**  
- 对每一天分别用 **DFS**（深度优先搜索）遍历图。  
- 维护 `cur_rate`（当前路径的乘积），以及 `best[to]`（到达货币 `to` 的最大乘积）。  
- 为防止无限递归，使用 `visited` 集合记录当前递归栈上的节点（不允许在同一次递归中再次进入同一个节点）。  
- DFS 完成后得到 `day1_best[c]` = 第一天从 `initialCurrency` 换到 `c` 的最大比例，同理得到 `day2_best[c]` = 第二天从 `c` 换回 `initialCurrency` 的最大比例。  
- 最终答案 = `max( 1.0 , max_{c} day1_best[c] * day2_best[c] )`，`1.0` 表示什么都不换的情况。

#### 代码（Python）

```python
from typing import List, Dict, Set

def maxAmount_bruteforce(initialCurrency: str,
                         pairs1: List[List[str]], rates1: List[float],
                         pairs2: List[List[str]], rates2: List[float]) -> float:
    # ---------- 把 pairs + rates 建成邻接表 ----------
    def build_graph(pairs: List[List[str]], rates: List[float]) -> Dict[str, List[tuple]]:
        g: Dict[str, List[tuple]] = {}
        for (a, b), r in zip(pairs, rates):
            g.setdefault(a, []).append((b, r))   # a -> b，乘以 r
        return g

    g1 = build_graph(pairs1, rates1)
    g2 = build_graph(pairs2, rates2)

    # ---------- 深度优先搜索：得到从 src 出发能到达每个货币的最大乘积 ----------
    def dfs(graph: Dict[str, List[tuple]], src: str) -> Dict[str, float]:
        best: Dict[str, float] = {src: 1.0}   # 到自己的最大乘积显然是 1

        def _search(cur: str, cur_rate: float, visited: Set[str]) -> None:
            # 只要找到了更大的乘积，就更新 best 并继续往下走
            for nxt, rate in graph.get(cur, []):
                if nxt in visited:          # 防止在同一路径中形成环
                    continue
                new_rate = cur_rate * rate
                if new_rate > best.get(nxt, 0.0):
                    best[nxt] = new_rate
                    visited.add(nxt)
                    _search(nxt, new_rate, visited)
                    visited.remove(nxt)

        _search(src, 1.0, {src})
        return best

    day1_best = dfs(g1, initialCurrency)   # 第一天从初始货币能到达的最大比例
    day2_best = dfs(g2, initialCurrency)   # 第二天从初始货币能到达的最大比例（这里其实是反向的，后面会用到）

    # 为了得到“第二天从某货币 C 换回初始货币”的比例，需要在第二天的图上
    # 以 C 为起点再跑一次 DFS，或者直接在 DFS 里记录所有到达初始货币的比例。
    # 为了代码简洁，这里再跑一次，只不过起点换成每个可能的中转货币。
    # 由于规模极小，这样的额外开销可以忽略不计。
    max_amount = 1.0          # 什么都不换的情况
    for cur, rate1 in day1_best.items():
        # 计算从 cur 再走第二天的图能回到初始货币的最大比例
        day2_from_cur = dfs(g2, cur)
        rate2 = day2_from_cur.get(initialCurrency, 0.0)
        max_amount = max(max_amount, rate1 * rate2)

    return max_amount
```

> **关键行解释**  
> - `best: Dict[str, float] = {src: 1.0}`：把起点的最大乘积初始化为 1（相当于“把 1 单位的自己换成自己”）。  
> - `if nxt in visited: continue`：防止在同一次递归中出现环，避免无限递归。  
> - `if new_rate > best.get(nxt, 0.0):`：只在找到了更好的兑换比例时才继续向下搜索，这样可以剪枝。  

#### 复杂度  

- **时间复杂度**：  
  - 每天的 DFS 最坏会遍历所有可能的路径。因为最多只有 `n ≤ 10` 条边，节点数也不超过 20，路径数是指数级的（约 O(2^n)），但常数极小，实际运行毫秒级。  
  - 整体时间约为 `O(枚举所有路径) ≈ O(2^n)`，在本题约为 `O(2^10) ≈ 1024`，完全可以接受。  

- **空间复杂度**：  
  - 递归栈深度 ≤ 节点数 ≤ 20，外加邻接表和 `best` 字典，都是 O(V)≈O(20)。  

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于我们对每一天都做了指数级的路径枚举。实际上，我们只需要知道：

> **从 `initialCurrency` 到任意货币 X 的**“最大乘积路径”**的比例**  
> **以及从 X 回到 `initialCurrency` 的最大乘积路径的比例**  

这正是**“单源最短路”**的乘积版，只是把“最短”改成“最大”。  
把乘积转成加法是常见技巧：取对数后，乘积 `a * b` 变成 `log a + log b`，于是**最大乘积路径**就等价于**最大和路径**。  
然而我们不必真的去取对数，因为**Floyd‑Warshall**（全源最短路）本身可以直接在“乘积”上做“松弛”：

```
if rate[i][k] * rate[k][j] > rate[i][j]:
    rate[i][j] = rate[i][k] * rate[k][j]
```

这一步的意义是：如果经过中间货币 `k` 能得到更大的兑换比例，就把它记下来。  
因为每一天的图规模很小（最多 10 条边），使用 Floyd‑Warshall 的 **O(V³)** 完全绰绰有余，而且它一次性算出 **任意两点之间的最大乘积**，不需要重复 DFS。

**步骤概览**  

1. **收集所有出现的货币**，给每个货币分配一个整数编号（0…V‑1）。  
2. 建立 `V × V` 的矩阵 `best[i][j]`，初始值为 `0`（表示不可达），对角线设为 `1.0`（自己换自己）。  
3. 把当天的直接兑换比例写入矩阵：`best[u][v] = rate`。  
4. **Floyd‑Warshall**：三层循环 `k,i,j`，更新 `best[i][j] = max(best[i][j], best[i][k] * best[k][j])`。  
5. 完成后，`best[s][c]` 即是 **第 d 天** 从 `s`（起始货币）到 `c` 的最大乘积。  
6. 计算答案：遍历所有货币 `c`，`ans = max(ans, best1[s][c] * best2[c][s])`，再与 `1.0` 比较。

> **类比**：想象有若干种商品之间的兑换比例，我们想知道“把 A 换成 B 再换成 C”是否比直接 “A 换成 C” 更划算。Floyd‑Warshall 就像在所有商品之间反复试探“中转一次”，把每一次的最优结果记下来，最终得到全局最优的兑换比例。

#### 代码（Python）

```python
from typing import List, Dict

def maxAmount_optimal(initialCurrency: str,
                     pairs1: List[List[str]], rates1: List[float],
                     pairs2: List[List[str]], rates2: List[float]) -> float:
    # ---------- 1. 把所有出现的货币映射成整数编号 ----------
    currencies = set([initialCurrency])
    for a, b in pairs1 + pairs2:
        currencies.add(a); currencies.add(b)
    idx: Dict[str, int] = {c: i for i, c in enumerate(currencies)}
    n = len(currencies)                       # 节点数

    # ---------- 2. 通用的 Floyd‑Warshall 求最大乘积 ----------
    def floyd(pairs: List[List[str]], rates: List[float]) -> List[List[float]]:
        # 初始化矩阵，0 表示不可达，1 表示自己到自己
        mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            mat[i][i] = 1.0
        # 写入直接兑换比例
        for (a, b), r in zip(pairs, rates):
            u, v = idx[a], idx[b]
            mat[u][v] = max(mat[u][v], r)      # 若出现多条相同方向的边，取更大的比例

        # Floyd‑Warshall：尝试让每条路径经过一个中间节点 k
        for k in range(n):
            for i in range(n):
                if mat[i][k] == 0:   # i 到 k 不可达，直接跳过
                    continue
                for j in range(n):
                    if mat[k][j] == 0:
                        continue
                    # 经过 k 的乘积 = i→k * k→j
                    via_k = mat[i][k] * mat[k][j]
                    if via_k > mat[i][j]:
                        mat[i][j] = via_k
        return mat

    day1_mat = floyd(pairs1, rates1)   # 第一天任意两货币间的最大乘积
    day2_mat = floyd(pairs2, rates2)   # 第二天任意两货币间的最大乘积

    s = idx[initialCurrency]           # 起始货币的编号
    ans = 1.0                          # 什么都不换的基准

    # ---------- 3. 枚举中转货币 ----------
    for c in range(n):
        rate1 = day1_mat[s][c]         # 第一天从初始换到 c 的最大比例
        rate2 = day2_mat[c][s]         # 第二天从 c 换回初始的最大比例
        if rate1 > 0 and rate2 > 0:    # 必须两段都可达
            ans = max(ans, rate1 * rate2)

    return ans
```

> **关键行解释**  
> - `mat[i][i] = 1.0`：把“自己换成自己”视为乘积 1，方便后面的乘法松弛。  
> - `if mat[i][k] == 0: continue`：若 `i→k` 不可达，就没有必要尝试 `k→j`。这一步大幅降低了常数。  
> - `via_k = mat[i][k] * mat[k][j]`：把“先到 k 再到 j”的整体比例算出来，和已有的 `mat[i][j]` 比较取更大的。  

#### 复杂度  

- **时间复杂度**：  
  - 建图 + 初始化 O(V²)（V ≤ 20）。  
  - Floyd‑Warshall 三层循环是 O(V³)。在最坏情况下 V≈20，故 `O(20³) = O(8000)`，几乎瞬间完成。  
  - 枚举中转货币 O(V)。  
  - **总体** `O(V³)`，远快于暴力的指数级。  

- **空间复杂度**：  
  - 两个 `V × V` 的矩阵，每个存放浮点数，空间为 O(V²)。在本题 ≤ 400，几乎可以忽略。  

---

## 心得  

- **核心技巧**：把“最大乘积路径”转化为 **全源最短路的乘积版**，利用 **Floyd‑Warshall** 一次性求出任意两点之间的最优兑换比例。  
- **适用题型**  
  1. 任意两点间的最大/最小乘积（或加和）问题，如 “货币兑换最大收益”。  
  2. 需要在两段独立图之间组合路径的情形（例如两天的交易、两阶段的运输）。  
  3. 图中边权是比例/概率，需要求最大整体比例的场景（如 “信任传递最大可信度”）。  
- **一句话总结解题钥匙**：  
  > “把乘积转成‘乘法松弛’，用 Floyd‑Warshall 把所有中转一次的机会都尝遍，一遍遍历就能得到全局最优”。  

---

## 反思  

- **拿到题目第一反应**：先想 “先遍历所有路径”，因为图小，直接 DFS 能写出来。  
- **最容易踩的坑**  
  1. **环导致无限递归**：如果不记录 `visited`，DFS 可能在比例 ≤1 的环里无限循环。  
  2. **忘记“可以不做任何兑换”**：答案至少是 `1.0`，否则在没有可盈利路径时会误返回 `0`。  
  3. **矩阵初始化错误**：对角线必须是 `1.0`，否则 `i→k→i` 的乘积会被错误地压成 `0`。  
  4. **浮点精度**：题目只要求 1e‑5 以内的误差，直接使用 Python `float` 足够，不必额外做高精度处理。  

- **下次遇到同类题**，第一步应该思考：“我只需要**任意两点之间的最优乘积**吗？”如果答案是肯定的，就立刻转向 **Floyd‑Warshall（或对数 + Bellman‑Ford）**，而不是先写遍历递归。这样既能保证正确性，又能省去大量不必要的搜索。