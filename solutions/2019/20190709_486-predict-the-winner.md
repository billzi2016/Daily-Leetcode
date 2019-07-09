# #486. 预测赢家 / Predict the Winner

> 难度：中等 · 标签：Array、Math、Dynamic Programming、Recursion、Game Theory · [LeetCode 链接](https://leetcode.com/problems/predict-the-winner/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. Two players are playing a game with this array: player 1 and player 2.
Player 1 and player 2 take turns, with player 1 starting first. Both players start the game with a score of 0. At each turn, the player takes one of the numbers from either end of the array (i.e., nums[0] or nums[nums.length - 1]) which reduces the size of the array by 1. The player adds the chosen number to their score. The game ends when there are no more elements in the array.
Return true if Player 1 can win the game. If the scores of both players are equal, then player 1 is still the winner, and you should also return true. You may assume that both players are playing optimally.

**Examples**

**Example 1:**

```
Input: nums = [1,5,2]
Output: false
Explanation: Initially, player 1 can choose between 1 and 2. 
If he chooses 2 (or 1), then player 2 can choose from 1 (or 2) and 5. If player 2 chooses 5, then player 1 will be left with 1 (or 2). 
So, final score of player 1 is 1 + 2 = 3, and player 2 is 5. 
Hence, player 1 will never be the winner and you need to return false.
```

**Example 2:**

```
Input: nums = [1,5,233,7]
Output: true
Explanation: Player 1 first chooses 1. Then player 2 has to choose between 5 and 7. No matter which number player 2 choose, player 1 can choose 233.
Finally, player 1 has more score (234) than player 2 (12), so you need to return True representing player1 can win.
```

**Constraints**

- 1 <= nums.length <= 20
- 0 <= nums[i] <= 107

---

## 题目（中文翻译）

你被给定一个整数数组 `nums`。现在有两位玩家在这条数组上进行游戏：玩家 1 和玩家 2。  
玩家 1 先手，双方交替行动。两位玩家的初始得分均为 0。每一回合，当前玩家必须从数组的 **两端** 取走一个数（即 `nums[0]` 或 `nums[nums.length - 1]`），取走后数组长度减 1。玩家将取走的数加入自己的得分。数组中的所有元素被取完后游戏结束。  

**返回** `true` 当且仅当玩家 1 能够获胜。若两位玩家得分相等，仍视为玩家 1 获胜，也应返回 `true`。你可以假设双方都采用最优策略。

### 示例

**示例 1**  
```text
Input: nums = [1,5,2]
Output: false
Explanation: 最初，玩家 1 可以在 1 和 2 之间选择。  
- 若他选择 2（或 1），则玩家 2 接下来只能在 1（或 2）和 5 中选。  
- 若玩家 2 选择 5，则玩家 1 只能得到剩下的 1（或 2）。  

于是玩家 1 的最终得分为 1 + 2 = 3，玩家 2 的得分为 5。  
因此玩家 1 永远不可能成为赢家，返回 `false`。
```

**示例 2**  
```text
Input: nums = [1,5,233,7]
Output: true
Explanation: 玩家 1 首先选择 1。此时玩家 2 必须在 5 和 7 中选。  
不论玩家 2 选哪个，玩家 1 都可以在下一轮取走 233。  
最终玩家 1 的得分为 1 + 233 = 234，玩家 2 的得分为 5 + 7 = 12，玩家 1 获胜，返回 `true`。
```

### 约束条件

- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一步的所有可能都枚举出来**，看到底谁的总分更高。  
- 游戏每轮只能从数组的左端或右端取一个数，这相当于在一棵二叉树里向左走（取左端）或向右走（取右端）。  
- 于是我们可以用递归把这棵“决策树”遍历完，记录玩家 1 最终的得分，取所有分支中的最大值。  

这里用到的唯一数据结构是**递归调用栈**，它就像我们在写日记时不断“打开新的一页”，写完后再回到上一页继续写。  

**为什么正确？**  
因为我们把**所有**合法的取数顺序都考虑了，而题目保证双方都“最优”，所以只要我们在每个分支里都让玩家 1 选取能让自己分数最高的路径，就一定能得到真实的输赢结果。

**复杂度分析（大白话）**  
- 每一轮有 2 种选择，数组长度为 `n` 时，总共会出现 `2ⁿ` 条不同的取数路径。  
- 所以时间复杂度是 **O(2ⁿ)**，也就是说随着数组长度的增加，耗时会像翻倍一样快速增长。  
- 递归调用栈的深度最多是 `n`，所以空间复杂度是 **O(n)**（只需要保存 `n` 层函数调用的信息）。

#### 代码（Python）

```python
from functools import lru_cache

class Solution:
    def PredictTheWinner(self, nums):
        """
        暴力递归：返回玩家1是否能赢
        """
        n = len(nums)

        @lru_cache(None)                     # 记忆化，避免重复计算
        def dfs(l, r, turn):
            """
            l, r : 当前数组的左右边界（闭区间）
            turn : 0 表示玩家1的回合，1 表示玩家2的回合
            返回值为玩家1在此局面的最终得分差（player1 - player2）
            """
            if l > r:                         # 没有数字可取，得分差为 0
                return 0

            # 玩家1想让差值最大，玩家2想让差值最小
            if turn == 0:                     # 玩家1回合
                take_left = nums[l] + dfs(l + 1, r, 1)   # 取左边
                take_right = nums[r] + dfs(l, r - 1, 1)  # 取右边
                return max(take_left, take_right)       # 选更大的差值
            else:                             # 玩家2回合（等价于把差值取负）
                take_left = -nums[l] + dfs(l + 1, r, 0)
                take_right = -nums[r] + dfs(l, r - 1, 0)
                return min(take_left, take_right)       # 选更小的差值

        # 初始时差值 >= 0，说明玩家1不输
        return dfs(0, n - 1, 0) >= 0
```

#### 复杂度

- **时间复杂度：O(2ⁿ)**  
  每层递归有两个分支，深度为 `n`，所以总的调用次数是指数级的。  
- **空间复杂度：O(n)**  
  递归栈的最大深度为 `n`，再加上 `lru_cache` 用的哈希表（这里算在时间复杂度里），主要的额外空间是栈。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于大量的重复子问题：  
- 例如区间 `[2, 5]` 可能在不同的取数顺序里被多次计算。  
- 只要我们把同样的区间只算一次，就能省掉指数级的工作。

这正是**动态规划**（Dynamic Programming）的核心思想：  
> 把“大问题”拆成“小问题”，把已经算好的“小问题”记下来（称为“记忆化”或“DP 表”），以后直接复用。

下面用两种等价的视角来解释最优解：

1. **“得分差”视角**（零和博弈）  
   - 假设 `scoreDiff(l, r)` 表示**当前玩家**（轮到谁拿）在区间 `[l, r]` 能取得的 **自己分数 - 对手分数** 的最大值。  
   - 当轮到玩家 1 时，他希望这个差值越大越好；当轮到玩家 2 时，他实际上是在让差值变小（因为对手的视角翻转了符号）。  
   - 递推式：  
     ```
     scoreDiff(l, r) = max( nums[l] - scoreDiff(l+1, r),
                           nums[r] - scoreDiff(l, r-1) )
     ```
     解释：如果当前玩家拿左边 `nums[l]`，那么对手在剩下的子区间 `[l+1, r]` 能得到的差值是 `scoreDiff(l+1, r)`，于是自己的最终差值就是 `拿到的值 - 对手的差值`。同理右边。

2. **“先手能否获胜”视角**（布尔 DP）  
   - 记 `dp[l][r]` 为 **先手**（当前轮的玩家）在 `[l, r]` 是否能赢（或平局）。  
   - 先手如果能让对手在子区间里 **输**，那么先手就赢。  
   - 递推式：  
     ```
     dp[l][r] = (nums[l] - dp[l+1][r] >= 0) or (nums[r] - dp[l][r-1] >= 0)
     ```
   - 这里的 `dp[l+1][r]`、`dp[l][r-1]` 实际上是**对手的最佳得分差**，我们只要判断自己拿了某个数后，剩下的局面对手是否还能保持不负即可。

下面采用 **得分差** 的写法，因为它更直观且只需要一个整数 DP 表。

**实现细节**  

- DP 表 `dp[i][j]` 表示区间 `[i, j]` 的最优差值。  
- 边界：当 `i == j` 时，只剩一个数，差值就是它本身（先手直接拿走）。  
- 填表顺序：从短区间到长区间。外层遍历区间长度 `len`，内层遍历左端点 `i`，右端点 `j = i + len - 1`。  
- 最终答案：`dp[0][n-1] >= 0` 表示先手（玩家 1）不输。

**空间优化**  
因为递推式只依赖 `dp[i+1][j]` 和 `dp[i][j-1]`（即左下和右上两个格子），我们可以把二维表压缩成一维数组 `dp[j]`，在遍历时自底向上更新。这样空间降到 **O(n)**。

#### 代码（Python）

```python
class Solution:
    def PredictTheWinner(self, nums):
        """
        动态规划（得分差版）：
        dp[i][j] 表示区间 nums[i..j] 中，当前玩家相对对手的最大分数差。
        最终只要 dp[0][n-1] >= 0，玩家1就不会输。
        """
        n = len(nums)
        # 一维 dp，初始时 dp[i] = nums[i]（区间长度为 1）
        dp = nums[:]                     # dp[j] 对应区间 [i, j]，i 随外层循环变化

        # 按区间长度从 2 到 n 逐步扩大
        for length in range(2, n + 1):   # length 为当前考虑的子数组长度
            for i in range(n - length + 1):
                j = i + length - 1       # 子数组右端点
                # 递推式：取左边或右边，减去对手在剩余区间的最佳差值
                dp[j] = max(nums[i] - dp[j],   # 拿左边，剩下的是 [i+1, j]，其差值已保存在 dp[j]
                             nums[j] - dp[j-1])  # 拿右边，剩下的是 [i, j-1]，其差值在 dp[j-1]
                # 这里的 dp[j] 会在下一次 i 循环时被当作 “dp[i+1][j]” 使用

        # dp[n-1] 即为整个数组的最优差值
        return dp[-1] >= 0
```

#### 复杂度

- **时间复杂度：O(n²)**  
  我们遍历所有可能的区间（`n*(n+1)/2` ≈ `n²/2`），每个区间只做 O(1) 的计算。相较于暴力的指数级，这已经快了很多。  
- **空间复杂度：O(n)**  
  只使用了一个长度为 `n` 的一维数组来存储当前行的 DP 值，远比二维表的 `O(n²)` 要省内存。

---

## 心得

- **核心技巧**：把“谁能赢”转化为“先手能取得的分数差最大是多少”。这是一种**零和博弈**的思考方式，适用于所有双方交替取值、总分固定的游戏。  
- **适用题型**（类似题）  
  1. *Stone Game* 系列（Stone Game I/II/III）  
  2. *Coins in a Line*（线性硬币取数）  
  3. *Burst Balloons*（气球爆炸）——同样用区间 DP 处理子问题。  
- **一句话总结解题钥匙**：**把每一步的“取值”转化为“分数差”，用 DP 把区间的最优差值记下来，最终判断差值是否非负。**

---

## 反思

- **第一反应**：直接写递归把所有可能枚举完，觉得好像可以直接得到答案。  
- **最容易踩的坑**  
  - 忘记对手也是“最优”，所以在递推时必须用 “当前得分 - 对手的最佳差值”。  
  - 边界条件：当只剩一个数时，差值应直接等于该数，否则会出现索引越界。  
  - 在一维 DP 实现时，更新顺序必须从左到右（或相应的方向）保证 `dp[j-1]` 仍是上一轮的旧值。  
- **下次类似题的第一步**：先问自己“这是一场零和博弈吗？能否用‘先手的优势（分数差）’来描述”。如果答案是肯定的，就马上写出递推式并考虑记忆化/动态规划。