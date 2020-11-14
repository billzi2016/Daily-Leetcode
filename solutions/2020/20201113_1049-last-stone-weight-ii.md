# #1049. **最后一块石头的重量 II** / Last Stone Weight II

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/last-stone-weight-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of integers stones where stones[i] is the weight of the ith stone.
We are playing a game with the stones. On each turn, we choose any two stones and smash them together. Suppose the stones have weights x and y with x <= y. The result of this smash is:
At the end of the game, there is at most one stone left.
Return the smallest possible weight of the left stone. If there are no stones left, return 0.

**Examples**

**Example 1:**

```
Input: stones = [2,7,4,1,8,1]
Output: 1
Explanation:
We can combine 2 and 4 to get 2, so the array converts to [2,7,1,8,1] then,
we can combine 7 and 8 to get 1, so the array converts to [2,1,1,1] then,
we can combine 2 and 1 to get 1, so the array converts to [1,1,1] then,
we can combine 1 and 1 to get 0, so the array converts to [1], then that's the optimal value.
```

**Example 2:**

```
Input: stones = [31,26,33,21,40]
Output: 5
```

**Constraints**

- 1 <= stones.length <= 30
- 1 <= stones[i] <= 100

---

## 题目（中文翻译）

你得到一个整数数组 `stones`，其中 `stones[i]` 表示第 `i` 块石头的重量。  
我们进行如下游戏：每回合任选两块石头，将它们撞击在一起。设这两块石头的重量分别为 `x` 和 `y`（`x ≤ y`），撞击的结果为：

- 若 `x == y`，两块石头都会被完全粉碎，不会留下任何石头；
- 若 `x != y`，重量为 `x` 的石头被粉碎，重量为 `y` 的石头会变成重量为 `y - x` 的新石头。

游戏结束时，至多会剩下一块石头。返回可能的最小剩余重量。如果所有石头都被完全粉碎，则返回 `0`。

**示例**

**示例 1**  
输入：`stones = [2,7,4,1,8,1]`  
输出：`1`  
解释：  
我们可以先将 `2` 与 `4` 碰撞得到 `2`，数组变为 `[2,7,1,8,1]`；  
再将 `7` 与 `8` 碰撞得到 `1`，数组变为 `[2,1,1,1]`；  
接着将 `2` 与 `1` 碰撞得到 `1`，数组变为 `[1,1,1]`；  
再将 `1` 与 `1` 碰撞得到 `0`，数组变为 `[1]`，此时仅剩重量为 `1` 的石头，已达到最小可能值。

**示例 2**  
输入：`stones = [31,26,33,21,40]`  
输出：`5`

**约束条件**

- `1 ≤ stones.length ≤ 30`
- `1 ≤ stones[i] ≤ 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题可以把每一次“砸石头”想象成给每块石头打上 **+** 或 **-** 号。  
- 若两块石头重量相同且相互抵消，等价于它们的符号相反，最后相加为 **0**。  
- 最终留下的唯一石头的重量，就是所有石头重量在 **+**、**-** 两种符号下的 **绝对值**（因为负号只表示被砸掉的那一侧）。

所以我们只要把每块石头分别标记为 **+** 或 **-**，把所有标记后的数相加，取绝对值的最小值，就是答案。

> **生活化类比**：把石头看成一本本字典，字典里每个词都有正负两种情绪（+ 或 -），把所有词的情绪相加，最后的“情绪总和”绝对值最小，说明正负尽可能抵消。

最直接的做法就是 **穷举** 所有可能的符号组合。  
- 对于 `n` 块石头，有 `2^n` 种 + / - 的安排。  
- 用深度优先搜索（DFS）或回溯把每块石头的符号依次决定，递归到底时计算当前的绝对和，更新全局最小值。

这种方法必然能得到正确答案，因为它遍历了所有合法的砸石过程。

#### 代码（Python）

```python
from typing import List

def lastStoneWeightII_bruteforce(stones: List[int]) -> int:
    n = len(stones)
    ans = float('inf')                 # 记录全局最小的绝对和

    def dfs(idx: int, cur_sum: int) -> None:
        """
        idx   : 当前处理到第几块石头
        cur_sum: 已经决定符号的石头的加权和（正负混合）
        """
        nonlocal ans
        if idx == n:                    # 所有石头都已分配符号
            ans = min(ans, abs(cur_sum))
            return
        # 把第 idx 块石头标记为 +
        dfs(idx + 1, cur_sum + stones[idx])
        # 把第 idx 块石头标记为 -
        dfs(idx + 1, cur_sum - stones[idx])

    dfs(0, 0)
    return ans
```

> 关键点中文注释已写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(2^n)`  
  解释：每块石头有两种选择（+ 或 -），共 `2^n` 种组合。`n` 最多 30 时，`2^30 ≈ 10^9`，在实际机器上几乎不可能跑完。

- **空间复杂度**：`O(n)`（递归栈深度）  
  只需要保存递归调用的层数，最多 `n` 层。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **指数级的枚举**。  
观察题目可以把它转化为 **“把石头分成两堆，使两堆重量之差最小”**：

- 把标记为 **+** 的石头放进左堆，标记为 **-** 的石头放进右堆。  
- 左堆总重量 `L`，右堆总重量 `R`，最终剩余石头的重量就是 `|L - R|`。  

所以我们只需要找到一个子集，使它的重量尽可能接近 **总重量的一半**（`total / 2`），因为：

```
|L - R| = |total - 2 * L|   （假设 L 为左堆重量，R = total - L）
```

当 `L` 越接近 `total/2`，`|total - 2*L|` 就越小。

这正是经典的 **0/1 背包 / 子集和** 问题：  
- **物品** = 每块石头的重量 `stones[i]`  
- **背包容量** = `total // 2`（只能装到一半）  
- **目标** = 在不超过容量的前提下，使背包里重量尽可能大（即最接近容量）。

我们可以用 **动态规划**（DP）求解：

1. 计算所有石头的总重量 `total`。  
2. 创建一个长度为 `target + 1` 的布尔数组 `dp`，`dp[j]` 表示是否能用若干石头恰好凑出重量 `j`。  
   - 初始 `dp[0] = True`（不选任何石头可以得到重量 0）。  
3. 对每块石头 `x`，从大到小遍历 `j`（防止同一块石头被重复使用）：
   - `dp[j] = dp[j] or dp[j - x]`  
   - 这一步的意义是：如果之前已经能凑出 `j - x`，那么加上当前石头 `x` 就能凑出 `j`。  
4. 最后在 `dp` 中找最大的 `j ≤ target`，满足 `dp[j] == True`。答案即为 `total - 2*j`。

> **类比**：把背包想成一个装钱的口袋，口袋最大只能装 `target` 元。我们有若干面额的硬币（石头重量），想把口袋装得尽可能满但不超。装得越满，剩下的钱（两堆差值）就越少。

#### 代码（Python）

```python
from typing import List

def lastStoneWeightII_dp(stones: List[int]) -> int:
    total = sum(stones)                # 所有石头的总重量
    target = total // 2                # 背包容量：总重量的一半

    # dp[j] 表示是否能凑出恰好重量 j
    dp = [False] * (target + 1)
    dp[0] = True                       # 0 重量永远可以凑出（不选任何石头）

    for x in stones:                  # 遍历每块石头
        # 必须倒着遍历，防止同一块石头被多次使用
        for j in range(target, x - 1, -1):
            if dp[j - x]:
                dp[j] = True

    # 在 dp 中找最大的可达重量 j，j <= target
    for j in range(target, -1, -1):
        if dp[j]:
            # 两堆之差 = total - 2 * j
            return total - 2 * j

    return 0  # 理论上不会走到这里
```

> 代码同样配有中文注释，可直接运行。

#### 复杂度

- **时间复杂度**：`O(n * total)`，其中 `n = len(stones)`，`total = sum(stones)`。  
  - 解释：外层遍历 `n` 块石头，内层遍历背包容量 `target ≈ total/2`。  
  - 由于 `stones[i] ≤ 100`，`n ≤ 30`，所以 `total ≤ 3000`，实际运行非常快（约 `30 * 1500 = 45,000` 次循环）。

- **空间复杂度**：`O(total)`（一维 DP 数组）  
  - 只需要保存 `target + 1` 个布尔值，最多约 `1501` 个，几乎可以忽略不计。

与暴力解相比，时间从指数级降到了线性乘系数级，能够轻松通过所有测试。

---

## 心得

- **核心技巧**：把“石头相互砸”转化为“给每块石头加上正负符号”，再进一步抽象为**子集和 / 0‑1 背包**问题。  
- **适用场景**：  
  1. **Partition Equal Subset Sum**（把数组分成两等和）  
  2. **Minimum Subset Sum Difference**（最小子集和差）  
  3. **Target Sum**（LeetCode 494）——同样是给每个数加正负号求目标值。  
- **一句话总结**：**“把砸石头看成两堆重量的平衡，用背包找最接近半总和的子集”。**

---

## 反思

- **第一反应**：看到“每次选两块石头砸”，立刻想到模拟过程，想写循环或递归直接模拟。  
- **最容易踩的坑**：  
  - **忘记把问题转化为子集和**，导致在实现暴力搜索时陷入超时。  
  - **DP 更新顺序写错**（正向遍历会导致同一块石头被多次使用），必须倒序遍历背包容量。  
  - **边界**：`total` 为奇数时，答案不一定是 0，需要返回 `total - 2 * best` 而不是直接 `total % 2`。  
- **下次思考类似题**：先问自己“能否把每个元素视为正负号或放入两组”，如果答案是“可以”，就立刻考虑 **子集和 / 0‑1 背包** 的 DP 思路。