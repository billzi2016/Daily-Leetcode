# #2770. 到达最后下标的最大跳跃次数 / Maximum Number of Jumps to Reach the Last Index

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of n integers and an integer target.
You are initially positioned at index 0. In one step, you can jump from index i to any index j such that:
Return the maximum number of jumps you can make to reach index n - 1.
If there is no way to reach index n - 1, return -1.

**Examples**

**Example 1:**

```
Input: nums = [1,3,6,4,1,2], target = 2
Output: 3
Explanation: To go from index 0 to index n - 1 with the maximum number of jumps, you can perform the following jumping sequence:
- Jump from index 0 to index 1. 
- Jump from index 1 to index 3.
- Jump from index 3 to index 5.
It can be proven that there is no other jumping sequence that goes from 0 to n - 1 with more than 3 jumps. Hence, the answer is 3.
```

**Example 2:**

```
Input: nums = [1,3,6,4,1,2], target = 3
Output: 5
Explanation: To go from index 0 to index n - 1 with the maximum number of jumps, you can perform the following jumping sequence:
- Jump from index 0 to index 1.
- Jump from index 1 to index 2.
- Jump from index 2 to index 3.
- Jump from index 3 to index 4.
- Jump from index 4 to index 5.
It can be proven that there is no other jumping sequence that goes from 0 to n - 1 with more than 5 jumps. Hence, the answer is 5.
```

**Example 3:**

```
Input: nums = [1,3,6,4,1,2], target = 0
Output: -1
Explanation: It can be proven that there is no jumping sequence that goes from 0 to n - 1. Hence, the answer is -1.
```

**Constraints**

- 2 <= nums.length == n <= 1000
- -109 <= nums[i] <= 109
- 0 <= target <= 2 * 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`（长度为 `n`）以及一个整数 `target`。  
初始时你位于下标 `0`。在一次移动中，你可以从下标 `i` 跳到任意下标 `j`（`i < j`），前提是满足  

```
|nums[i] - nums[j]| ≤ target
```  

返回能够到达下标 `n - 1` 的**最大跳跃次数**。如果不存在任何跳跃序列能够到达下标 `n - 1`，返回 `-1`。

## 示例

### 示例 1
**输入**  
```json
nums = [1,3,6,4,1,2], target = 2
```  
**输出**  
```
3
```  
**解释**  
为了在从下标 `0` 到下标 `n - 1` 的过程中获得最多的跳跃次数，你可以按如下顺序跳跃：  
- 从下标 `0` 跳到下标 `1`（|1‑3| = 2 ≤ 2）。  
- 从下标 `1` 跳到下标 `3`（|3‑4| = 1 ≤ 2）。  
- 从下标 `3` 跳到下标 `5`（|4‑2| = 2 ≤ 2）。  

可以证明不存在其他跳跃序列能够在满足条件的前提下使用 **超过 3 次**的跳跃。因此答案为 `3`。

### 示例 2
**输入**  
```json
nums = [1,3,6,4,1,2], target = 3
```  
**输出**  
```
5
```  
**解释**  
在 `target = 3` 的情况下，能够获得最多跳跃次数的序列为：  
- 0 → 1（|1‑3| = 2）  
- 1 → 2（|3‑6| = 3）  
- 2 → 3（|6‑4| = 2）  
- 3 → 4（|4‑1| = 3）  
- 4 → 5（|1‑2| = 1）  

不存在其他满足条件的跳跃序列能够使用 **超过 5 次**的跳跃，所以答案为 `5`。

### 示例 3
**输入**  
```json
nums = [1,3,6,4,1,2], target = 0
```  
**输出**  
```
-1
```  
**解释**  
当 `target = 0` 时，只有数值相等的下标之间才可以跳跃。虽然 `nums[0]` 与 `nums[4]` 相等，但从 `4` 再也找不到后续相等的元素能够到达下标 `5`，因此不存在从 `0` 到 `n‑1` 的合法跳跃序列，答案为 `-1`。

## 约束条件
- `2 ≤ nums.length == n ≤ 1000`
- `-10^9 ≤ nums[i] ≤ 10^9`
- `0 ≤ target ≤ 2·10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有**可能的跳跃路径**都枚举一遍，看看哪条路径能够在到达最后一个下标 `n-1` 时拥有最多的跳步数。  
- **数据结构**：我们可以把数组的每个下标当成图中的一个节点，满足 `|nums[j] - nums[i]| ≤ target` 的 `i → j` 视作一条有向边。  
- **遍历方式**：从起点 `0` 开始，用深度优先搜索（DFS）递归地尝试每一次合法跳跃，记录已经走过的跳数。  
- **正确性**：因为我们把 **所有** 合法的跳跃顺序都尝试了一遍，最终得到的最大跳数一定是题目要求的答案（如果有路径的话）。  

> 类比：想象你在一个城市的每条街道上行走，只有满足某个条件的街道才能通行。暴力解就像把每条可能的路线都走一遍，记下走了多少步，最后挑出走得最久的那条。

#### 代码（Python）

```python
from typing import List

def maxJumps_bruteforce(nums: List[int], target: int) -> int:
    n = len(nums)
    ans = -1                     # 用来保存全局的最大跳数，默认 -1 表示不可达

    def dfs(pos: int, jumps: int) -> None:
        """
        pos   : 当前所在的下标
        jumps : 已经跳了多少步
        """
        nonlocal ans
        # 如果已经到达最后一个下标，更新答案
        if pos == n - 1:
            ans = max(ans, jumps)
            return

        # 尝试所有合法的下一个下标 j（j 必须在 pos 右侧）
        for nxt in range(pos + 1, n):
            if -target <= nums[nxt] - nums[pos] <= target:   # 跳跃条件
                dfs(nxt, jumps + 1)                         # 继续往后走

    dfs(0, 0)   # 从下标 0 开始，跳数为 0
    return ans
```

> **关键行中文注释**  
> - `if -target <= nums[nxt] - nums[pos] <= target:`：检查跳跃是否满足题目给出的数值差限制。  
> - `ans = max(ans, jumps)`：一旦到达终点，用 `max` 保留最大的跳数。  

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级）。因为每个位置都有可能向右跳到后面的若干位置，最坏情况下会产生指数级的递归树。可以把它想象成“在每一步都有很多分叉”，所有分叉都要走完才算完事。  
- **空间复杂度**：`O(n)`，主要是递归调用栈的深度，最深可能到 `n` 层。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**：同一个下标 `i` 可能被多次以不同路径访问，而它到达 `i` 时的最大跳数其实只和 `i` 本身有关，不需要每次都重新搜索。  

我们可以把“从起点走到每个位置的最大跳数”记下来，用**动态规划（DP）**来一步步递推：

1. **状态定义**：`dp[i]` 表示**从下标 0 到下标 i** 能得到的**最大跳数**。如果 `i` 根本不可达，则 `dp[i] = -inf`（这里用 `-1` 方便后面比较）。
2. **状态转移**：要得到 `dp[j]`（j>i），只要找一个 **合法的前驱 i**（满足 `|nums[j]-nums[i]| ≤ target`），并且 `dp[i]` 已经算出来了。  
   那么 `dp[j] = max(dp[j], dp[i] + 1)`。  
   直白点说：如果我能从 `i` 跳到 `j`，并且已经知道从起点到 `i` 最多能跳多少步，那么到 `j` 的跳数就是 “到 `i` 的跳数 + 这一步”。我们在所有可能的 `i` 中挑出最大的那个。
3. **初始化**：`dp[0] = 0`（站在起点还没有跳），其余设为 `-1` 表示不可达。  
4. **遍历顺序**：外层遍历 `j`（从左到右），内层遍历所有左侧的 `i`。因为 `dp[i]` 在计算 `dp[j]` 前一定已经确定。

> 类比：想象一排小格子，每个格子只能往右跳，跳的距离受数字差的限制。我们从左往右依次把每个格子“能到达的最远步数”写在纸上，后面的格子只需要看左边已经写好的数，就能快速算出自己的最大步数。

**为什么这就是最优**  
- 每个位置只算一次 `dp`，没有重复递归。  
- 总共要检查所有 `(i, j)` 对，时间是 `O(n²)`，而 `n ≤ 1000`，在实际运行中已经非常快。  
- 空间只需要一个长度为 `n` 的数组，`O(n)`。

#### 代码（Python）

```python
from typing import List

def maxJumps_dp(nums: List[int], target: int) -> int:
    n = len(nums)
    dp = [-1] * n          # dp[i] = 从 0 到 i 的最大跳数，-1 表示不可达
    dp[0] = 0              # 起点不需要跳

    # 枚举每个终点 j
    for j in range(1, n):
        # 枚举所有可能的前驱 i（i 必须在 j 左侧）
        for i in range(j):
            # 只有当 i 可达且两数之差在 [-target, target] 时才可以跳
            if dp[i] != -1 and -target <= nums[j] - nums[i] <= target:
                dp[j] = max(dp[j], dp[i] + 1)   # 更新 j 的最大跳数

    return dp[-1]          # dp[n-1] 即为答案，若为 -1 则表示不可达
```

> **关键行中文注释**  
> - `dp = [-1] * n`：把所有位置先标记为“不可达”。  
> - `if dp[i] != -1 and -target <= nums[j] - nums[i] <= target:`：只有当 `i` 本身已经能到达且跳跃满足条件时，才考虑从 `i` 到 `j`。  
> - `dp[j] = max(dp[j], dp[i] + 1)`：取所有合法前驱中能得到的最大跳数。

#### 复杂度

- **时间复杂度**：`O(n²)`。我们需要检查每一对 `(i, j)`（`i < j`），这相当于在做 `n*(n-1)/2` 次比较。对于 `n ≤ 1000`，大约只有 500,000 次操作，几乎在瞬间完成。  
- **空间复杂度**：`O(n)`。只用了一个长度为 `n` 的一维数组来保存每个位置的最大跳数。

---

## 心得

- **核心技巧**：**动态规划 + 前缀遍历**。把“到达每个位置的最优解”保存下来，后面的计算只依赖已经求好的子问题，避免了重复搜索。  
- **适用的题型**  
  1. “跳跃游戏”类（如 LeetCode 55/45）——求最少/最多跳数。  
  2. “区间/数值差限制的最长子序列”类（如 LeetCode 718）——在满足条件的前提下求最长或最大。  
  3. “有向无环图的最长路径”——把 DAG 的拓扑序列换成数组的顺序，使用 DP 求最长路径。  
- **一句话总结**：**把每一步的最优解记下来，后面只看左边已经算好的答案，就能一次遍历搞定。**

---

## 反思

- **第一反应**：看到“从 i 可以跳到任意满足条件的 j”，本能想到**DFS**把所有路径枚举。  
- **最容易踩的坑**  
  - 忘记把不可达的状态用 `-1`（或负无穷）标记，导致错误地把不可达的 `dp[i]` 参与转移。  
  - 只检查 `i < j` 而忘记 **数值差的正负**，实际上条件是 `|nums[j] - nums[i]| ≤ target`，等价于 `-target ≤ nums[j] - nums[i] ≤ target`。  
  - 对 `target = 0` 的特殊情况没有额外处理：只有数值相同的相邻位置才能跳，容易误判为全部可达。  
- **下次类似题的第一步**：先把“**从起点到每个位置的最优值**”抽象成 DP 状态，判断转移是否只依赖左侧已计算好的状态，如果是，就立刻写出 `dp` 方程；否则再考虑更复杂的结构（如单调队列、线段树等）。