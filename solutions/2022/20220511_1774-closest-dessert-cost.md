# #1774. 最接近的甜点费用 / Closest Dessert Cost

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking · [LeetCode 链接](https://leetcode.com/problems/closest-dessert-cost/)

---

## 题目（英文原版）

**Description**

You would like to make dessert and are preparing to buy the ingredients. You have n ice cream base flavors and m types of toppings to choose from. You must follow these rules when making your dessert:
You are given three inputs:
You want to make a dessert with a total cost as close to target as possible.
Return the closest possible cost of the dessert to target. If there are multiple, return the lower one.

**Examples**

**Example 1:**

```
Input: baseCosts = [1,7], toppingCosts = [3,4], target = 10
Output: 10
Explanation: Consider the following combination (all 0-indexed):
- Choose base 1: cost 7
- Take 1 of topping 0: cost 1 x 3 = 3
- Take 0 of topping 1: cost 0 x 4 = 0
Total: 7 + 3 + 0 = 10.
```

**Example 2:**

```
Input: baseCosts = [2,3], toppingCosts = [4,5,100], target = 18
Output: 17
Explanation: Consider the following combination (all 0-indexed):
- Choose base 1: cost 3
- Take 1 of topping 0: cost 1 x 4 = 4
- Take 2 of topping 1: cost 2 x 5 = 10
- Take 0 of topping 2: cost 0 x 100 = 0
Total: 3 + 4 + 10 + 0 = 17. You cannot make a dessert with a total cost of 18.
```

**Example 3:**

```
Input: baseCosts = [3,10], toppingCosts = [2,5], target = 9
Output: 8
Explanation: It is possible to make desserts with cost 8 and 10. Return 8 as it is the lower cost.
```

**Constraints**

- n == baseCosts.length
- m == toppingCosts.length
- 1 <= n, m <= 10
- 1 <= baseCosts[i], toppingCosts[i] <= 104
- 1 <= target <= 104

---

## 题目（中文翻译）

你想要制作甜点，并且正在准备购买所需的配料。你有 `n` 种冰淇淋基底口味（base）和 `m` 种配料（topping）可供选择。制作甜点时必须遵守以下规则：

- 必须先选择 **一个** 基底口味（base）。
- 对于每一种配料（topping），你可以选择 **0、1 或 2** 份。
- 甜点的总费用等于基底费用加上所有选中配料的费用之和。

给定三个输入：

- `baseCosts`：长度为 `n` 的整数数组，`baseCosts[i]` 表示第 `i` 种基底的费用。
- `toppingCosts`：长度为 `m` 的整数数组，`toppingCosts[i]` 表示第 `i` 种配料的单份费用。
- `target`：一个整数，表示你希望甜点的总费用尽可能接近的目标值。

返回甜点总费用最接近 `target` 的可能值。如果存在多个最接近的费用，返回较小的那个。

---

### 示例

**示例 1**

```text
Input: baseCosts = [1,7], toppingCosts = [3,4], target = 10
Output: 10
Explanation: 考虑以下组合（下标均从 0 开始）：
- 选择基底 1：费用 7
- 取 1 份配料 0：1 × 3 = 3
- 取 0 份配料 1：0 × 4 = 0
总费用：7 + 3 + 0 = 10。
```

**示例 2**

```text
Input: baseCosts = [2,3], toppingCosts = [4,5,100], target = 18
Output: 17
Explanation: 考虑以下组合（下标均从 0 开始）：
- 选择基底 1：费用 3
- 取 1 份配料 0：1 × 4 = 4
- 取 2 份配料 1：2 × 5 = 10
- 取 0 份配料 2：0 × 100 = 0
总费用：3 + 4 + 10 + 0 = 17。无法组合出总费用为 18 的甜点。
```

**示例 3**

```text
Input: baseCosts = [3,10], toppingCosts = [2,5], target = 9
Output: 8
Explanation: 可以组合出费用为 8 和 10 的甜点。返回较小的 8。
```

---

### 约束条件

- `n == baseCosts.length`
- `m == toppingCosts.length`
- `1 <= n, m <= 10`
- `1 <= baseCosts[i], toppingCosts[i] <= 10^4`
- `1 <= target <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的要求其实很直接：**选一个冰淇淋底料 + 若干种配料（每种配料可以选 0、1 或 2 次），让总花费最接近 target**。  
因为题目给出的规模非常小：

* 底料数量 `n ≤ 10`  
* 配料数量 `m ≤ 10`  
* 每种配料最多出现 2 次  

我们可以把所有可能的组合都枚举出来，然后挑出最接近 target 的那个。  

> **类比**：想象你在超市里挑商品，底料相当于必买的主食，配料相当于可以随意加的配菜（每种配菜最多两份）。你可以把所有的购物清单写在纸上，算出每份清单的总价，最后挑出最接近预算的那份。

**为什么暴力一定能得到正确答案？**  
只要把“所有合法的组合”都列举出来，就不会漏掉任何一种可能性。遍历完后，比较每个组合的总价与 target 的差距，取差距最小且成本更低的那个——这正是题目要求的答案。

**复杂度分析（大白话版）**  

* 对每一种底料，我们都要遍历所有配料的选择情况。  
* 每种配料有 3 种取法（0、1、2），所以 `m` 种配料一共会产生 `3^m` 种组合。  
* 再乘以底料的数量 `n`，总的遍历次数大约是 `n × 3^m`。

对照实际数字：`n = 10, m = 10` 时，`3^10 = 59049`，乘以 10 仍然只有 **约 60 万** 次，完全可以在一秒内跑完。

空间上，只需要保存当前递归路径的费用（一个整数）和最好的答案，所以是 **O(1)**（不计递归栈深度）。


#### 代码（Python）

```python
from typing import List

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        # 最佳答案初始化为一个非常大的差值
        best = float('inf')          # 记录当前最小的 |cost - target|
        ans  = None                  # 记录对应的实际花费

        # -------------------------------------------------
        # 递归枚举配料的 0 / 1 / 2 次选择
        # -------------------------------------------------
        def dfs(idx: int, cur_cost: int) -> None:
            """遍历到第 idx 种配料时的递归函数"""
            nonlocal best, ans

            # ---------- 更新答案 ----------
            diff = abs(cur_cost - target)
            if diff < best or (diff == best and cur_cost < ans):
                best = diff
                ans  = cur_cost

            # 已经遍历完所有配料，直接返回
            if idx == len(toppingCosts):
                return

            # ---------- 对当前配料的三种取法 ----------
            # 0 次
            dfs(idx + 1, cur_cost)

            # 1 次
            dfs(idx + 1, cur_cost + toppingCosts[idx])

            # 2 次
            dfs(idx + 1, cur_cost + 2 * toppingCosts[idx])

        # -------------------------------------------------
        # 枚举每一种底料，作为递归的起点
        # -------------------------------------------------
        for base in baseCosts:
            dfs(0, base)   # 从第 0 种配料开始，当前费用为 base

        return ans
```

> **代码要点注释**  
> - `best` 保存当前最小的“与 target 的距离”。  
> - `ans` 保存对应的实际花费。  
> - `dfs` 递归遍历配料，每层有三条分支（0、1、2 次）。  
> - 递归的 **剪枝**（这里没有显式剪枝，因为规模已经够小）可以在后面最优解里讨论。  

#### 复杂度

- **时间复杂度**：`O(n × 3^m)`  
  > “n×3^m” 就是我们前面算的遍历次数，实际运行时最多约 60 万次，足够快。  
- **空间复杂度**：`O(m)`（递归栈的深度）  
  > 只需要保存递归调用的层数，最多 `m ≤ 10`，几乎可以忽略不计。

---

### 2. 最优解

#### 思路  

暴力解已经能 AC，但我们可以把“枚举所有组合”改写成**动态规划（DP）**的形式，让代码更简洁、易于理解，也更容易在更大的数据规模下扩展。

**慢在哪里？**  
暴力解的递归会在每条分支上重复计算相同的子问题。例如，配料 `[3,4]`，在处理完配料 0 后得到的费用 `base+3`，无论后面配料 1 选 0、1、2 次，都会再次以 `base+3` 为起点进行递归。这样会产生大量重复计算。

**优化思路**：  
把“所有已经可以达到的费用集合”保存下来，遍历配料时只在这套集合的基础上**扩展**一次，而不是每次都重新遍历全部分支。

具体步骤：

1. **初始化**：把所有底料费用加入一个集合 `possible`，因为底料必须选且只能选一次。  
2. **遍历每一种配料**：  
   - 对当前配料 `c`，我们可以在已有的费用上 **加一次 `c`** 或 **加两次 `c`**（0 次已经在集合里）。  
   - 为了避免在遍历过程中“把新加入的费用再继续加同一种配料”，我们先把当前集合拷贝一份 `new_set`，在这份拷贝上进行扩展，然后合并回 `possible`。  
3. **遍历结束后**，`possible` 中保存了 **所有合法的总费用**（底料 + 任意配料的 0/1/2 次组合）。  
4. **找最接近 target 的费用**：遍历集合，比较 `abs(cost - target)`，如果相等则取更小的 `cost`。

**为什么这一步是 DP？**  
我们把“考虑前 i 种配料后能得到的费用集合”记作 `dp[i]`。  
`dp[i+1] = dp[i] ∪ { x + c, x + 2c | x ∈ dp[i] }`。  
这正是 DP 的递推公式，只是我们用 **集合**（Set）来实现，省去显式的二维数组。

**类比**：  
想象你在玩“拼钱游戏”。先有若干张面值为底料的钞票（只能拿一张），再有若干面值为配料的钞票（每种最多两张）。每次你把手里的所有可能的金额记下来（集合），然后把新的一种配料的金额加进去，得到新的可能金额。最后，你只要在这张“大账本”里挑最接近目标的那笔钱即可。

#### 代码（Python）

```python
from typing import List

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        # 1. 所有可能的费用集合，先放入所有底料（必须选且只能选一次）
        possible = set(baseCosts)

        # 2. 逐个处理配料
        for c in toppingCosts:
            # 把当前集合拷贝出来，防止在遍历时把新加的费用再次使用同一种配料
            cur = list(possible)          # list 便于遍历
            for cost in cur:
                # 加一次该配料
                possible.add(cost + c)
                # 加两次该配料
                possible.add(cost + 2 * c)

        # 3. 在所有可能费用里找最接近 target 的答案
        best = float('inf')
        ans  = None
        for cost in possible:
            diff = abs(cost - target)
            if diff < best or (diff == best and cost < ans):
                best = diff
                ans  = cost

        return ans
```

> **代码要点注释**  
> - `possible` 用 `set` 自动去重，防止同一个费用出现多次。  
> - `cur = list(possible)` 这一步是“快照”，保证每种配料只被使用最多两次。  
> - 最后遍历 `possible` 时的比较逻辑与暴力解完全相同。

#### 复杂度

- **时间复杂度**：`O(n + m × S)`，其中 `S` 为所有可能费用的个数。  
  - `n` 是底料数量（把底料放进集合的成本）。  
  - 对每种配料我们遍历一次当前集合，最多把集合大小扩大 2 倍。  
  - 由于 `target ≤ 10⁴`、每个费用 ≤ `10⁴`，实际 `S` 不会超过几千，整体仍然远小于暴力的 `3^m`。  
- **空间复杂度**：`O(S)`，保存所有可能的费用。  
  - `S` 最多也就是所有合法费用的数量，最多约 `2·target + max(base)`，在本题的数值范围内（≤ 2·10⁴）也很小。

相比暴力的 `O(n·3^m)` 时间，DP 把指数级的 **3ⁿ** 降到了 **线性**（相对于可能费用的数量），在更大的输入规模下也能保持可接受。

---

## 心得

- **核心技巧**：**枚举 + 集合去重（等价于 DP）**。  
  - 先把必选的底料加入集合；  
  - 再对每种配料，利用集合的“已有元素 + 0/1/2 次”进行一次扩展。  
- **适用的题型**（类似思路）  
  1. *Combination Sum IV*（求不同组合数）  
  2. *Target Sum*（正负号分配，使和等于 target）  
  3. *Partition Equal Subset Sum*（把数组分成两部分，使和相等）  
- **一句话总结解题钥匙**：**把“所有可能的费用”当成状态集合，逐步用配料扩展状态，最后从集合里挑最接近 target 的值**。

---

## 反思

- **第一反应**：看到“每种配料可以选 0、1、2 次”，立刻想到 **三叉树递归**（暴力枚举）。  
- **最容易踩的坑**  
  - 忘记配料的 **最多两次** 限制，导致代码产生无限循环或错误的计数。  
  - 在 DP 实现时，直接在 `for cost in possible:` 循环里修改 `possible`，会把同一种配料使用超过两次。解决办法是先复制一份当前集合（快照）再进行扩展。  
  - 当多种费用距离 target 相同，记得返回 **较小的费用**（代码里 `if diff == best and cost < ans`）。  
- **下次类似题的第一步**：  
  1. 明确“每个元素的使用次数上限”。  
  2. 判断是否可以把“所有可能的结果”用集合/DP 逐步累加，而不是一次性递归遍历全部分支。  

这样既能保证正确性，又能在规模稍大时保持效率。祝你玩得开心，算法之路越走越宽！