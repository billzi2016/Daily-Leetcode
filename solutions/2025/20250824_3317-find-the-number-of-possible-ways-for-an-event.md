# #3317. 找出事件可能的安排方式数 / Find the Number of Possible Ways for an Event

> 难度：困难 · 标签：Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-possible-ways-for-an-event/)

---

## 题目（英文原版）

**Description**

You are given three integers n, x, and y.
An event is being held for n performers. When a performer arrives, they are assigned to one of the x stages. All performers assigned to the same stage will perform together as a band, though some stages might remain empty.
After all performances are completed, the jury will award each band a score in the range [1, y].
Return the total number of possible ways the event can take place.
Since the answer may be very large, return it modulo 109 + 7.
Note that two events are considered to have been held differently if either of the following conditions is satisfied:

**Examples**

**Example 1:**

```
Input: n = 1, x = 2, y = 3
Output: 6
Explanation:
```

**Example 2:**

```
Input: n = 5, x = 2, y = 1
Output: 32
Explanation:
```

**Example 3:**

```
Input: n = 3, x = 3, y = 4
Output: 684
```

**Constraints**

- 1 <= n, x, y <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定三个整数 `n`、`x` 和 `y`。  
一次活动有 `n` 位表演者（performer）。当一位表演者到达时，需要将其分配到 `x` 个舞台（stage）中的一个。被分配到同一舞台的所有表演者将组成一个乐队（band）一起演出，某些舞台可以保持空置。  
所有表演结束后，评审团（jury）会为每支乐队打一个分数，分数取值范围为 `[1, y]`。  
返回该活动所有可能的安排方式总数。由于答案可能非常大，请返回 **模** `10^9 + 7` 的结果。

**不同的安排**  
若满足以下任意条件，则认为两次活动的安排不同：

* 任意表演者被分配到的舞台不同；
* 任意乐队的最终得分不同。

**示例**

> 示例 1  
> 输入: `n = 1, x = 2, y = 3`  
> 输出: `6`  
> 说明: （此处填写解释）

> 示例 2  
> 输入: `n = 5, x = 2, y = 1`  
> 输出: `32`  
> 说明: （此处填写解释）

> 示例 3  
> 输入: `n = 3, x = 3, y = 4`  
> 输出: `684`  
> 说明: （此处填写解释）

**约束条件**  
- `1 <= n, x, y <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一步都**枚举**出来：

1. **给每个表演者挑舞台**  
   - 每个表演者都有 `x` 种选择（第 1、2 … x 舞台）。  
   - 这相当于把 `n` 个人放进 `x` 个盒子里，盒子可以空。  
   - 在代码里可以用一个长度为 `n` 的数组 `stage[i]` 保存第 `i` 个人选的舞台编号。

2. **给每个非空舞台打分**  
   - 先遍历所有舞台，找出哪些舞台里有人（即非空），记为 `k`。  
   - 对每个非空舞台，都有 `y` 种可能的分数（1~y），所以一共有 `y^k` 种打分方式。  

3. **把两步的结果相乘**，得到一种完整的“事件”。把所有可能的 `stage` 组合全部遍历并累加，就得到答案。

> **类比**：把每个人想成一本书，把舞台想成书架的层。先决定每本书放在哪层（可以有空层），再给每个有书的层贴上一个标签（分数）。把所有可能的摆放方式和标签组合列举完，就是暴力解。

**为什么正确**  
- 我们枚举了 **所有** 可能的表演者分配方式以及 **所有** 可能的分数组合，且没有遗漏或重复计数。  
- 只要把每一种合法的完整配置都加进去，最终的总和自然就是答案。

**时间/空间复杂度**  

- 分配阶段：每个表演者有 `x` 种选择，`n` 个人就有 `x^n` 种可能。  
- 打分阶段：对每种分配，需要遍历最多 `x` 个舞台，计算 `y^k`（`k ≤ x`），这在指数级的 `x^n` 前已经可以忽略不计。  

> **复杂度**：  
> - **时间**：`O(x^n)`，也就是指数级增长。即使 `n=5, x=3` 也要遍历 `3^5 = 243` 种，`n=10, x=5` 已经是 `9,765,625` 种，根本跑不完。  
> - **空间**：只需要保存当前的 `stage` 数组，`O(n)`。

显然，这种暴力方法只能用来**验证思路**，不能直接提交。

---

### 2. 最优解  

#### 思路  

从暴力解出发，我们可以看到两大**瓶颈**：

1. **表演者分配的枚举**：`x^n` 远远超过题目要求的 `n, x ≤ 1000`。  
2. **打分的枚举**：虽然 `y^k` 只在 `k ≤ x`，但仍然是指数级。

要把这两个指数级的枚举压到 **多项式时间**，必须**把相同结构的组合“合并计数”**。  
下面一步步推导出可行的计数公式。

---

#### 2.1 先固定「非空舞台的个数」  

设最终有 `k` 个非空舞台（`1 ≤ k ≤ min(n, x)`），其余 `x‑k` 个舞台保持空。  
把问题拆成三部分：

| 步骤 | 要做的事 | 计数方式 | 解释 |
|------|----------|----------|------|
| A    | 选出哪 `k` 个舞台会被使用 | `C(x, k)`（组合） | 从 `x` 个舞台中挑出 `k` 个，不考虑顺序 |
| B    | 把 `n` 位表演者分配到这 `k` 个已选舞台，使每个舞台至少有 1 人 | **全射**（surjection）计数 | 把 `n` 个人放进 `k` 个 **标记好的**盒子，且每盒子非空 |
| C    | 给这 `k` 个非空舞台打分 | `y^k` | 每个非空舞台独立有 `y` 种分数选择 |

最终答案是所有可能 `k` 的加和：

\[
\text{Ans} = \sum_{k=1}^{\min(n,x)}  C(x,k) \times \underbrace{\text{全射}(n\to k)}_{\text{步骤 B}} \times y^{k}
\]

---

#### 2.2 计算「全射」的数量  

把 `n` 位表演者划分成 `k` **不相交**、**非空** 的组，然后把这些组分别放到 `k` 个已选舞台上。

1. **先把表演者划分成 `k` 个无标签的非空集合**  
   - 这正是 **第二类 Stirling 数** `S(n, k)` 的定义。  
   - 直观理解：把 `n` 本不同的书分到 `k` 盒子里，盒子不标号，只要求每盒子里至少有一本书。

2. **把这些无标签的集合对应到已选的 `k` 个具体舞台**  
   - 因为舞台是有编号的（第 1、2 … k），我们需要把 `k` 个集合 **排列** 到 `k` 个舞台上，方式为 `k!`（全排列）。  

于是：

\[
\text{全射}(n\to k) = k! \times S(n, k)
\]

把它代入上面的式子，得到：

\[
\text{Ans} = \sum_{k=1}^{\min(n,x)}  C(x,k) \times k! \times S(n,k) \times y^{k}
\]

注意 `C(x,k) × k!` 正好等于 **排列数** `P(x,k) = x! / (x-k)!`，即「从 `x` 个舞台里挑出 `k` 个并排好顺序」的方式。于是公式可以写得更紧凑：

\[
\boxed{\displaystyle
\text{Ans}= \sum_{k=1}^{\min(n,x)}  P(x,k) \times S(n,k) \times y^{k}
}
\]

---

#### 2.3 动态规划求 Stirling 数  

`n, x ≤ 1000`，直接把所有 `S(n,k)` 预计算一次即可。  

递推式（取模后）：

\[
S(0,0)=1,\quad S(i,0)=0\;(i>0),\quad S(0,j)=0\;(j>0)
\]

\[
S(i,j)=j\cdot S(i-1,j) + S(i-1,j-1) \pmod{M}
\]

- 第一个项 `j·S(i‑1,j)`：把第 `i` 个人放进已有的 `j` 个非空集合中的任意一个（有 `j` 种选择）。  
- 第二个项 `S(i‑1,j‑1)`：把第 `i` 个人单独开辟一个新集合，剩下 `i‑1` 人分成 `j‑1` 组。

只需要两层循环 `i = 1..n`、`j = 1..i`，时间 `O(n²)`（≈ 10⁶），空间 `O(n²)` 或 **滚动数组**压到 `O(n)`。

---

#### 2.4 其余准备工作  

- **阶乘 & 逆元**：为了快速算 `P(x,k) = x! / (x‑k)!`，预先计算 `fact[i] = i! mod M`（`i = 0..max(n,x)`），以及 `inv_fact[i] = (i!)^{-1} mod M`（利用费马小定理 `a^{M‑2} ≡ a^{-1} (mod M)`）。  
- **幂**：`y^k` 直接在循环里用快速幂或累乘得到，时间 `O(k)`，整体仍是 `O(min(n,x))`。

---

#### 2.5 完整公式实现步骤  

1. **预处理**  
   - `M = 1_000_000_007`（题目要求的模数）。  
   - `maxV = max(n, x)`  
   - 计算 `fact[0..maxV]`、`inv_fact[0..maxV]`。  

2. **计算 Stirling** `S[0..n][0..n]`（或只保留上一行）。  

3. **遍历 k = 1 .. min(n,x)**  
   - `perm = fact[x] * inv_fact[x-k] % M`   ← `P(x,k)`  
   - `stir = S[n][k]`  
   - `pow_y = pow(y, k, M)` （Python 内置快速幂）  
   - `ans = (ans + perm * stir % M * pow_y) % M`  

4. **返回 ans**。

---

#### 代码（Python）

```python
MOD = 1_000_000_007

def numberOfWays(n: int, x: int, y: int) -> int:
    # ---------- 1. 预处理阶乘 ----------
    maxV = max(n, x)
    fact = [1] * (maxV + 1)
    for i in range(1, maxV + 1):
        fact[i] = fact[i - 1] * i % MOD

    # 逆元：使用费马小定理 a^(MOD-2) ≡ a^{-1} (mod MOD)
    inv_fact = [1] * (maxV + 1)
    inv_fact[maxV] = pow(fact[maxV], MOD - 2, MOD)
    for i in range(maxV, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # ---------- 2. 计算 Stirling 数 S(n, k) ----------
    # 只保留上一行，空间压到 O(n)
    stir = [0] * (n + 1)
    stir[0] = 1                     # S(0,0) = 1
    for i in range(1, n + 1):
        new = [0] * (n + 1)
        for k in range(1, i + 1):
            # S(i,k) = k * S(i-1,k) + S(i-1,k-1)
            new[k] = (k * stir[k] + stir[k - 1]) % MOD
        stir = new                 # 换行

    # ---------- 3. 累加所有可能的 k ----------
    limit = min(n, x)
    ans = 0
    for k in range(1, limit + 1):
        # P(x,k) = x! / (x-k)!
        perm = fact[x] * inv_fact[x - k] % MOD
        # Stirling number S(n,k) 已经在 stir[k] 中
        ways_assign = perm * stir[k] % MOD
        ways_score = pow(y, k, MOD)           # y^k % MOD
        ans = (ans + ways_assign * ways_score) % MOD

    return ans
```

> **代码说明**  
> - `fact` / `inv_fact` 用来快速算排列数 `P(x,k)`。  
> - `stir` 数组只保留当前行的 Stirling 值，节约空间。  
> - `pow(y, k, MOD)` 是 Python 内置的 **快速幂**，时间 `O(log k)`，对本题来说足够快。  

---

#### 复杂度  

- **时间**：  
  - 预处理阶乘 `O(max(n,x))`。  
  - 计算 Stirling `O(n²)`（因为两层循环 `i·k`，最多 `1000·1000 = 10⁶`）。  
  - 主循环遍历 `k`，`O(min(n,x))`。  
  - **总计** `O(n²)`，即约一百万次运算，完全可以在 1 秒内完成。  

- **空间**：  
  - 阶乘数组 `O(max(n,x))`。  
  - Stirling 只保留两行 `O(n)`。  
  - **总计** `O(max(n,x))`，约几千个整数，几乎不占内存。

与暴力解的 `O(x^n)` 时间相比，优化幅度是 **指数级 → 多项式级**，在所有合法输入下都能跑得很快。

---

## 心得  

- **核心技巧**：  
  把“把 `n` 个人分配到 `x` 个舞台并给非空舞台打分”拆成**组合**（选舞台）+**全射计数**（分配且每舞台非空）+**幂**（打分），并利用 **Stirling 数** 与 **排列数** 把指数级枚举压缩成多项式级求和。  

- **适用的题型**（类似思路）  
  1. **把物品分到若干非空盒子**，如“把 `n` 个球放进 `k` 个箱子，每箱至少一个”。  
  2. **给每个非空集合标记颜色/分数**，如“不同颜色的涂色题”。  
  3. **选取子集后再排列**，如“从 `x` 人中挑 `k` 人排成队”。  

- **一句话总结**：  
  **“先固定非空集合的个数，用组合×Stirling×幂的乘积求和”。**  

---

## 反思  

- **第一反应**：看到“每个表演者选舞台、每个舞台打分”，自然想到暴力枚举 `x^n`。这在小数据时能验证思路，但很快会卡在时间上。  

- **最容易踩的坑**  
  1. **忘记“每个非空舞台必须至少有一位表演者”**，导致使用简单的 `x^n` 分配而忽略了空舞台的处理。  
  2. **模运算的顺序**：在乘法链中任何一步都要取模，防止中间值溢出。  
  3. **边界**：当 `k=0`（所有舞台空）不算合法事件，循环必须从 `1` 开始；`y=0`（不可能，因为约束 `y≥1`）也要注意。  

- **下次遇到同类题的第一步**：  
  **“先把‘非空集合的个数’固定下来”，看能否把整体计数拆成‘选集合’ × ‘把集合分配到具体对象’ × ‘对每个集合的额外操作’**。这样往往能把指数爆炸的问题转化为可用组合数、Stirling 数或 DP 求解的多项式问题。