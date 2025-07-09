# #3259. 两种饮料的最大能量提升 / Maximum Energy Boost From Two Drinks

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-energy-boost-from-two-drinks/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays energyDrinkA and energyDrinkB of the same length n by a futuristic sports scientist. These arrays represent the energy boosts per hour provided by two different energy drinks, A and B, respectively.
You want to maximize your total energy boost by drinking one energy drink per hour. However, if you want to switch from consuming one energy drink to the other, you need to wait for one hour to cleanse your system (meaning you won't get any energy boost in that hour).
Return the maximum total energy boost you can gain in the next n hours.
Note that you can start consuming either of the two energy drinks.

**Examples**

**Example 1:**

```
Input: energyDrinkA = [1,3,1], energyDrinkB = [3,1,1]
Output: 5
Explanation:
To gain an energy boost of 5, drink only the energy drink A (or only B).
```

**Example 2:**

```
Input: energyDrinkA = [4,1,1], energyDrinkB = [1,1,3]
Output: 7
Explanation:
To gain an energy boost of 7:
```

**Constraints**

- n == energyDrinkA.length == energyDrinkB.length
- 3 <= n <= 105
- 1 <= energyDrinkA[i], energyDrinkB[i] <= 105

---

## 题目（中文翻译）

**描述**  
给定两个整数数组 `energyDrinkA` 和 `energyDrinkB`，长度相同为 `n`，它们分别表示两种能量饮料 A、B 在每个小时提供的能量提升（energy boost）。  
你希望在接下来的 `n` 小时内，通过每小时饮用一种能量饮料来使总能量提升最大化。然而，如果想要从一种饮料切换到另一种饮料，需要花费 **一小时** 来清理体内（即该小时没有任何能量提升）。  
返回在接下来的 `n` 小时内可以获得的最大总能量提升。  
注意，你可以从任意一种饮料开始饮用。

**示例 1**  
```
Input: energyDrinkA = [1,3,1], energyDrinkB = [3,1,1]
Output: 5
Explanation:
为了获得 5 的能量提升，只饮用能量饮料 A（或只饮用 B）即可。
```

**示例 2**  
```
Input: energyDrinkA = [4,1,1], energyDrinkB = [1,1,3]
Output: 7
Explanation:
为了获得 7 的能量提升：
```
（此处应列出具体的饮用方案，保持原题示例的说明结构）

**约束条件**  
- `n == energyDrinkA.length == energyDrinkB.length`  
- `3 <= n <= 10^5`  
- `1 <= energyDrinkA[i], energyDrinkB[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每一小时的选择全部枚举**，然后挑出能得到最大能量的那种方案。  
- 每一小时我们有三种可能：喝 A、喝 B、或者因为刚刚换饮料而“空等”一小时（不喝）。  
- 把所有可能的选择序列列举出来，就像把所有路线都写在纸上，再逐个算出对应的能量总和，最后取最大值。  

这相当于在每个时间点做一次**分支**，类似“树形递归”。可以把“喝 A”记作 `A`，喝 B 记作 `B`，空等记作 `-`，比如 `A B - A` 表示第 1 小时喝 A，第 2 小时喝 B（需要第 3 小时空等），第 4 小时再喝 A。  

> **为什么这种方法一定能得到答案？**  
因为我们把**所有合法的喝饮料序列**都遍历了一遍，答案必然在其中。只要不遗漏合法情况，最大值就一定被找到了。

> **时间/空间复杂度**  
- 每小时最多有 3 种选择（A、B、空），但空等只能在换饮料时出现，所以实际分支数约为 `2 * 2^(n-1)`，数量呈指数级增长，记作 **O(2ⁿ)**。  
- 递归栈深度最多是 `n`，需要保存每条路径的累计能量，空间也是 **O(n)**（递归调用本身）——但因为时间已经爆炸，这点空间其实不算主要瓶颈。

> **大白话解释**  
如果把 n 当成 20，`2ⁿ` 就是 **约 1,048,576** 种可能；n=30 时已经是 **约 1,073,741,824** 种，根本跑不完。  

#### 代码（Python）

```python
def max_energy_bruteforce(A, B):
    n = len(A)

    # 递归枚举第 i 小时的选择，prev 表示上一小时喝的是哪种饮料
    # prev = 0 -> 上一小时喝 A
    # prev = 1 -> 上一小时喝 B
    # prev = -1 -> 第一次喝，或刚刚空等（可以随意选择）
    def dfs(i, prev):
        if i == n:                     # 已经安排完所有小时
            return 0

        # 情况一：继续喝同一种饮料（不需要空等）
        best = 0
        if prev == 0:                  # 继续喝 A
            best = A[i] + dfs(i + 1, 0)
        elif prev == 1:                # 继续喝 B
            best = B[i] + dfs(i + 1, 1)
        else:                          # 第一次喝，既可以选 A，也可以选 B
            best = max(A[i] + dfs(i + 1, 0),
                       B[i] + dfs(i + 1, 1))

        # 情况二：如果要换饮料，需要空等一小时
        # 这里我们让当前小时空等，下一小时再喝另一种饮料
        # 空等只会在 i < n-1 时有意义（还有后面的小时可以喝）
        if i + 1 < n:
            # 空等后喝 A
            best = max(best, dfs(i + 2, 0))   # i+1 小时空等，i+2 小时喝 A
            # 空等后喝 B
            best = max(best, dfs(i + 2, 1))

        return best

    return dfs(0, -1)   # -1 表示“还没有喝任何饮料”
```

> **关键行解释**  
- `dfs(i, prev)`：递归函数，返回从第 `i` 小时开始、已知上一小时喝的饮料 `prev` 时的最大能量。  
- `if prev == 0:` …：如果上一次喝的是 A，则本小时只能继续喝 A（不需要空等）。  
- `if i + 1 < n:` …：只有还有剩余时间时，才考虑“空等一小时再换饮料”。  

#### 复杂度  

- **时间复杂度：O(2ⁿ)** — 解释：每小时基本都有两条分支（继续喝或换饮料），换饮料又会产生一次额外的空等，导致递归树的节点数随 n 指数级增长。  
- **空间复杂度：O(n)** — 解释：递归调用最多会产生 n 层栈帧，保存局部变量和返回值。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈在于大量的重复计算**：同样的子问题会被不同的递归路径反复求解。我们可以把“已知前 i 小时的安排，最后一小时喝的是哪种饮料”作为**状态**，把对应的最优值记下来，这正是**动态规划（DP）**的思想。  

**核心状态定义**  

| 状态 | 含义 |
|------|------|
| `dpA[i]` | 只考虑前 `i+1` 小时（即下标 0..i），并且第 `i` 小时**喝 A**时能得到的最大能量。 |
| `dpB[i]` | 同理，第 `i` 小时**喝 B**时的最大能量。 |

**状态转移**  

- 如果第 `i` 小时喝 A，有两种可能的前置情况  
  1. **前一小时也喝 A** → 不需要空等，直接在 `dpA[i‑1]` 的基础上加上 `energyDrinkA[i]`。  
  2. **前一小时喝 B** → 必须空等一小时才能换饮料，所以前两小时的安排必须是 “第 `i‑2` 小时喝 B”，即 `dpB[i‑2]`（第 `i‑1` 小时空等）。  

  因此  
  ```text
  dpA[i] = max(dpA[i-1], dpB[i-2]) + energyDrinkA[i]
  ```

- 同理，喝 B 时  
  ```text
  dpB[i] = max(dpB[i-1], dpA[i-2]) + energyDrinkB[i]
  ```

**边界处理**  

- `i = 0` 时：没有前置小时，直接喝即可  
  ```text
  dpA[0] = energyDrinkA[0]
  dpB[0] = energyDrinkB[0]
  ```
- `i = 1` 时：若想换饮料，需要空等第 0 小时，这在公式里对应 `i-2 = -1`，我们可以把不存在的 `dpX[-1]` 视作 0（相当于“前面没有任何安排”。）  

**答案**  

最后一小时可以是 A 也可以是 B，取两者的最大值：  
`answer = max(dpA[n-1], dpB[n-1])`  

**空间优化**  

上面的转移只依赖 `i-1` 和 `i-2` 两个位置的值，完全可以用 **滚动数组**（只保留最近的两行）把空间从 `O(n)` 降到 `O(1)`。  

> **类比**  
把 `dpA[i]` 想象成“把第 i 小时装进背包的最佳价值”，而 `dpB[i]` 是“装进另一种背包的最佳价值”。每次往背包里装东西（喝饮料），只能在同种背包里直接加，或者换背包时必须先留出一个空位（空等一小时）。  

#### 代码（Python）

```python
def max_energy_dp(energyDrinkA, energyDrinkB):
    n = len(energyDrinkA)
    if n == 0:
        return 0

    # 用滚动变量保存 i-2, i-1 的 dp 值，初始时把 “不存在的 dp” 设为 0
    dpA_i2, dpB_i2 = 0, 0            # 对应 dpA[i-2], dpB[i-2]
    dpA_i1 = energyDrinkA[0]         # dpA[0]
    dpB_i1 = energyDrinkB[0]         # dpB[0]

    # 只要 n >= 2，就需要遍历 i = 1 .. n-1
    for i in range(1, n):
        # 计算当前 i 时刻的 dp 值，使用 i-1、i-2 的旧值
        # max(dpA[i-1], dpB[i-2]) + A[i]
        curA = max(dpA_i1, dpB_i2) + energyDrinkA[i]
        # max(dpB[i-1], dpA[i-2]) + B[i]
        curB = max(dpB_i1, dpA_i2) + energyDrinkB[i]

        # 滚动更新：把 i-1、i-2 的值往前推
        dpA_i2, dpB_i2 = dpA_i1, dpB_i1   # 之前的 i-1 现在成为 i-2
        dpA_i1, dpB_i1 = curA, curB       # 当前 i 成为下一轮的 i-1

    # 循环结束后 dpA_i1 / dpB_i1 分别是 dpA[n-1] / dpB[n-1]
    return max(dpA_i1, dpB_i1)
```

> **关键行解释**  
- `dpA_i2, dpB_i2 = 0, 0`：对应 `i-2` 位置的值，最开始不存在，设为 0。  
- `curA = max(dpA_i1, dpB_i2) + energyDrinkA[i]`：实现公式 `dpA[i] = max(dpA[i-1], dpB[i-2]) + A[i]`。  
- `dpA_i2, dpB_i2 = dpA_i1, dpB_i1`：把“上一轮”的值向后移动，保持只用常数空间。  

#### 复杂度  

- **时间复杂度：O(n)** — 解释：只遍历一次数组，每一步做常数次算术和比较。相比指数级的暴力解，速度提升了数百倍。  
- **空间复杂度：O(1)** — 解释：只使用了固定数量的变量（四个滚动值），不随 `n` 增长。若保留完整的 `dpA`、`dpB` 表则是 `O(n)`，但完全可以省去。  

---

## 心得  

- **核心技巧**：**动态规划 + 滚动数组**。把“上一次喝的饮料”和“上上一次的状态”抽象成 DP 状态，避免重复计算。  
- **适用的题型**  
  1. 两条平行序列，切换时需要额外代价（如“换工作需要休息一天”）。  
  2. “只能在同一行连续取值，换行要空格”的网格 DP（如 **两个相邻行的最大路径和**）。  
  3. 类似 “只能在同一颜色的格子上走，换颜色要停一格” 的颜色约束路径题。  
- **一句话总结解题钥匙**：**把“上一小时喝的哪种饮料”作为状态，用 DP 把“继续喝”与“换饮料（需要空等）”两条转移分别记下来，最后取最大**。  

---

## 反思  

- **第一反应**：看到“换饮料要空等一小时”，立刻想到“需要在状态里记录‘上一次喝的是什么’”，于是想到递归/回溯。  
- **最容易踩的坑**  
  - **边界处理**：`i-2` 可能为负数，需要把不存在的 dp 看作 0。  
  - **空等的实现**：忘记在换饮料时把 “空等” 的那一小时计入总时长，导致答案偏大。  
  - **初始值**：如果直接把 `dpA[0]`、`dpB[0]` 设为 0，会错失第一小时直接喝的收益。  
- **下次类似题的第一步**：先**明确状态**（本题是“最后一小时喝的饮料是哪种”），再**写出状态转移方程**，最后检查“负索引/初始条件”。这样可以快速从暴力思路跳到 DP 解。