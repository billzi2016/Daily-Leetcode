# #956. 最高广告牌 / Tallest Billboard

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/tallest-billboard/)

---

## 题目（英文原版）

**Description**

You are installing a billboard and want it to have the largest height. The billboard will have two steel supports, one on each side. Each steel support must be an equal height.
You are given a collection of rods that can be welded together. For example, if you have rods of lengths 1, 2, and 3, you can weld them together to make a support of length 6.
Return the largest possible height of your billboard installation. If you cannot support the billboard, return 0.

**Examples**

**Example 1:**

```
Input: rods = [1,2,3,6]
Output: 6
Explanation: We have two disjoint subsets {1,2,3} and {6}, which have the same sum = 6.
```

**Example 2:**

```
Input: rods = [1,2,3,4,5,6]
Output: 10
Explanation: We have two disjoint subsets {2,3,5} and {4,6}, which have the same sum = 10.
```

**Example 3:**

```
Input: rods = [1,2]
Output: 0
Explanation: The billboard cannot be supported, so we return 0.
```

**Constraints**

- 1 <= rods.length <= 20
- 1 <= rods[i] <= 1000
- sum(rods[i]) <= 5000

---

## 题目（中文翻译）

你正在安装一块广告牌，想让它的高度尽可能大。广告牌两侧各有一根钢支架，**两根支架的高度必须相等**。  
现在给定一组可以焊接在一起的杆子（rods），例如长度为 1、2、3 的杆子，你可以把它们焊接成长度为 6 的支架。  
返回能够实现的最大广告牌高度。如果无法支撑广告牌，返回 0。

Example 1:
Example 2:
Example 3:
Constraints:

示例 1:
Input: rods = [1,2,3,6]
Output: 6
Explanation: 我们可以选取两个不相交的子集 {1,2,3} 和 {6}，它们的和相等，均为 6。

示例 2:
Input: rods = [1,2,3,4,5,6]
Output: 10
Explanation: 我们可以选取两个不相交的子集 {2,3,5} 和 {4,6}，它们的和相等，均为 10。

示例 3:
Input: rods = [1,2]
Output: 0
Explanation: 广告牌无法被支撑，因此返回 0。

约束条件：
- 1 <= rods.length <= 20
- 1 <= rods[i] <= 1000
- sum(rods[i]) <= 5000

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每根木棒 **逐个** 放到左边支柱、右边支柱或丢弃。  
可以把这三种选择想成“左、右、不要”，相当于 **把每根棒子放进三个盒子**。  

- **左支柱**：把棒子长度加到左边的总和 `L`  
- **右支柱**：把棒子长度加到右边的总和 `R`  
- **不要**：什么也不做  

遍历完所有棒子后，如果 `L == R`，说明找到了一个合法的方案，答案就是 `L`（或者 `R`）。  
因为我们把 **所有可能的放法都枚举了一遍**，所以一定能得到最大高度。

> **类比**：想象你有一堆拼图块，要把它们分别拼成两块完全相同面积的拼图。最笨的办法就是把每块拼图块尝试放到左边、右边或不放，全部尝试完后再挑最高的合法拼图。

**正确性**：枚举所有可能的分配方式，必然会覆盖所有合法的（左右总和相等）方案，取最大即为答案。

**时间/空间复杂度**：

- 每根棒子有 3 种选择，`n` 根棒子就是 `3ⁿ` 种可能，时间复杂度是 **O(3ⁿ)**。  
  - 大白话：如果有 10 根棒子，可能的组合大约是 3ⁱ⁰ ≈ 59,000 种；20 根棒子就会爆炸到 3²⁰ ≈ 3.5 × 10⁹ 种，根本跑不完。  
- 递归调用栈最多 `n` 层，空间复杂度是 **O(n)**（存放递归的临时变量）。

#### 代码（Python）

```python
from typing import List

def tallestBillboard_bruteforce(rods: List[int]) -> int:
    n = len(rods)
    best = 0                     # 记录目前找到的最大相等高度

    def dfs(idx: int, left: int, right: int) -> None:
        """深度优先遍历第 idx 根棒子，left/right 分别是左右支柱的当前高度"""
        nonlocal best
        if idx == n:              # 所有棒子都已经决定去向
            if left == right:     # 合法方案
                best = max(best, left)
            return

        # 1. 不使用第 idx 根棒子
        dfs(idx + 1, left, right)

        # 2. 放到左支柱
        dfs(idx + 1, left + rods[idx], right)

        # 3. 放到右支柱
        dfs(idx + 1, left, right + rods[idx])

    dfs(0, 0, 0)
    return best
```

#### 复杂度

- **时间复杂度**：O(3ⁿ) —— 每根棒子都有 3 种选择，指数级增长。  
- **空间复杂度**：O(n) —— 递归栈深度最多 `n`，`n ≤ 20`，很小。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“左右支柱的绝对高度”** 这两个维度让状态爆炸。  
观察发现，只要 **左右高度的差值** 已知，就可以推出较高一侧的具体高度（因为我们只关心相等时的高度）。  

> **类比**：把两根支柱想成天平的两边，天平只关心**两边的重量差**，而不是每边的具体重量。只要知道差值，我们就能算出天平的“最高点”。  

因此我们把 **状态** 定义为：

- `diff = left - right`（可能为负数，表示右边更高）  
- `tall = max(left, right)`（较高一侧的总长度）

用一个字典 `dp` 保存所有可能的 `diff` 对应的最大 `tall`：

```
dp[diff] = 当前已经处理的棒子中，能够得到 diff 差值时，较高支柱的最大长度
```

初始时只有一种情况：`diff = 0, tall = 0`（两边都为空）。

遍历每根棒子 `x`，我们对已有的每个 `(diff, tall)` 进行三种更新：

1. **不使用**：`dp` 不变（相当于把 `x` 丢弃）。
2. **放到较高的一侧**（即加到 `tall` 那边）  
   - 新的差值 `newDiff = diff + x`（因为较高侧再多了 `x`）  
   - 新的较高高度 `newTall = tall + x`  
   - `dp[newDiff] = max(dp.get(newDiff, 0), newTall)`
3. **放到较低的一侧**（即把 `x` 加到另一边，使差值缩小或翻转）  
   - 新的差值 `newDiff = abs(diff - x)`（因为两边的差会变成 `|left - right|`）  
   - 新的较高高度 `newTall = max(tall, tall - diff + x)`  
     - 解释：如果 `x` 小于 `diff`，仍然是右边更低，较高侧不变；如果 `x` 大于 `diff`，右边会超过左边，较高侧会变成原来的 `tall - diff + x`。  
   - `dp[newDiff] = max(dp.get(newDiff, 0), newTall)`

遍历完所有棒子后，`dp[0]` 就是左右支柱高度相等时的最大高度，即答案。

**为什么正确**：

- `diff` 完全描述了两侧的相对关系，所有可能的分配方式都可以映射到唯一的 `(diff, tall)`。  
- 动态规划保证我们在每一步都保留了 **最高** 的 `tall`，所以最终的 `dp[0]` 是全局最优。

**复杂度分析**：

- `diff` 的取值范围在 `[-sum, sum]`，其中 `sum ≤ 5000`（题目限制）。  
- 对每根棒子我们遍历当前字典的所有键，键的数量最多 `2*sum+1 ≈ 10001`。  
- 因此时间复杂度是 **O(n * sum)**，在本题最多约 `20 * 5000 = 1e5`，非常快。  
- 空间上只需要保存一个字典，大小同样是 `O(sum)`。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def tallestBillboard(rods: List[int]) -> int:
    """
    动态规划：dp[diff] = 当前已处理的棒子中，
                     差值为 diff 时，较高支柱的最大长度
    """
    dp = {0: 0}                     # 初始：差值 0，较高支柱高度 0

    for x in rods:                  # 逐根处理棒子
        cur = dp.copy()             # 为了避免在遍历时修改正在使用的字典
        for diff, tall in cur.items():
            # 1. 不使用 x —— 已经在 dp 中，无需额外操作

            # 2. 把 x 加到较高的一侧（让差值增大）
            new_diff = diff + x
            new_tall = tall + x
            if new_tall > dp.get(new_diff, 0):
                dp[new_diff] = new_tall

            # 3. 把 x 加到较低的一侧（让差值缩小或翻转）
            #    新的差值是两边高度的绝对差
            new_diff = abs(diff - x)
            #   较高支柱的高度取决于 x 是否超过了差值 diff
            new_tall = max(tall, tall - diff + x)
            if new_tall > dp.get(new_diff, 0):
                dp[new_diff] = new_tall

    return dp[0]                     # diff 为 0 时，两边相等，返回最高支柱高度
```

#### 复杂度

- **时间复杂度**：O(n × sum) ≈ O(20 × 5000) = O(10⁵)。  
  - 与暴力的 O(3ⁿ) 相比，指数级下降到线性级别，实际运行毫秒级完成。
- **空间复杂度**：O(sum) ≈ O(5000)。  
  - 只需要保存一个大小不超过 10001 的字典，内存占用非常小。

---

## 心得

- **核心技巧**：把“左右两侧的绝对高度”转化为“高度差 + 较高侧长度”的状态，用动态规划在差值维度上压缩搜索空间。  
- **适用的题型**  
  1. **Partition Equal Subset Sum**（等分子集和）——利用差值 DP 判断能否把数组划分成两段相等。  
  2. **Last Stone Weight II**（最后一块石头的重量）——同样是让两堆石头重量尽可能相近。  
  3. **Stone Game VI**（石子游戏）——需要考虑两人分数差值的最优策略。  
- **一句话总结解题钥匙**：**把“平衡”问题抽象为“差值”状态，用 DP 只记录每个差值下的最大可能高度**。

---

## 反思

- **第一反应**：直接枚举每根棒子的三种去向，写出递归暴力搜索。  
- **最容易踩的坑**  
  - 忘记在 DP 转移时更新 `new_tall` 的公式，导致差值相同但高度不最大。  
  - 处理 `diff` 为负数时没有使用 `abs`，导致字典键冲突或遗漏。  
  - 边界条件：所有棒子都不使用时，答案应为 0，必须初始化 `dp[0]=0`。  
- **下次遇到同类题**：第一步先问自己——“这是不是一个让两堆重量相等（或差值最小）的平衡问题？”  
  - 若答案是“是”，就尝试用 **差值 + 最大/最小对应值** 的 DP 思路，而不是直接枚举子集。