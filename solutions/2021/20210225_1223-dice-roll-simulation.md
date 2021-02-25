# #1223. 掷骰子模拟 / Dice Roll Simulation

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/dice-roll-simulation/)

---

## 题目（英文原版）

**Description**

A die simulator generates a random number from 1 to 6 for each roll. You introduced a constraint to the generator such that it cannot roll the number i more than rollMax[i] (1-indexed) consecutive times.
Given an array of integers rollMax and an integer n, return the number of distinct sequences that can be obtained with exact n rolls. Since the answer may be too large, return it modulo 109 + 7.
Two sequences are considered different if at least one element differs from each other.

**Examples**

**Example 1:**

```
Input: n = 2, rollMax = [1,1,2,2,2,3]
Output: 34
Explanation: There will be 2 rolls of die, if there are no constraints on the die, there are 6 * 6 = 36 possible combinations. In this case, looking at rollMax array, the numbers 1 and 2 appear at most once consecutively, therefore sequences (1,1) and (2,2) cannot occur, so the final answer is 36-2 = 34.
```

**Example 2:**

```
Input: n = 2, rollMax = [1,1,1,1,1,1]
Output: 30
```

**Example 3:**

```
Input: n = 3, rollMax = [1,1,1,2,2,3]
Output: 181
```

**Constraints**

- 1 <= n <= 5000
- rollMax.length == 6
- 1 <= rollMax[i] <= 15

---

## 题目（中文翻译）

**描述**  
一个骰子模拟器（die simulator）在每次掷骰子时会随机生成 1 到 6 之间的一个整数。你在生成器上加入了约束：第 i 个数字在连续出现的次数不能超过 `rollMax[i]`（`i` 为 1‑索引）。  
给定整数数组 `rollMax` 和整数 `n`，返回恰好进行 `n` 次掷骰子后可以得到的不同序列的数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模的结果。  
只要两个序列中任意位置的数字不同，就视为不同的序列。

**示例 1**  
```
输入: n = 2, rollMax = [1,1,2,2,2,3]
输出: 34
解释: 进行 2 次掷骰子，如果没有约束，则共有 6 * 6 = 36 种可能。根据 `rollMax`，数字 1 和 2 最多只能连续出现一次，因此序列 (1,1) 和 (2,2) 不合法，最终答案为 36 - 2 = 34。
```

**示例 2**  
```
输入: n = 2, rollMax = [1,1,1,1,1,1]
输出: 30
```

**示例 3**  
```
输入: n = 3, rollMax = [1,1,1,2,2,3]
输出: 181
```

**约束条件**  
- `1 <= n <= 5000`  
- `rollMax.length == 6`  
- `1 <= rollMax[i] <= 15`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的投掷序列**，再把不符合 “同一个面连续出现次数超过 `rollMax[i]`” 的序列剔除。

- **用到的数据结构**：  
  - `list` 保存当前已经投掷的序列（相当于一条“路线”）。  
  - 递归函数的调用栈就像**层层叠叠的盒子**，每进入一次递归就往盒子里放一个数字，回溯时再把它拿出来。

- **为什么这个方法一定能得到答案**：  
  - 对每一次投掷我们都尝试 1~6 的全部面，遍历完所有深度为 `n` 的路径后，**所有**合法或非法的序列都会出现一次。  
  - 在递归结束时检查当前序列是否满足 `rollMax` 的限制，满足的就计数， 不满足的直接丢弃。  

- **时间/空间复杂度**（大白话版）：  
  - **时间**：每一步都有 6 种选择，投掷 `n` 次就是 `6ⁿ`（6 的 n 次方）次尝试。想象一下你有 6 条路可以走，每走一步再分成 6 条路，走完 n 步后，你会有 `6ⁿ` 条不同的路线要检查——这在 `n=20` 以后已经天文数字了。  
  - **空间**：递归栈最多保存 `n` 个数字，加上一条当前路径的列表，空间是 `O(n)`。

#### 代码（Python）

```python
MOD = 10**9 + 7

def diceRolls_bruteforce(n, rollMax):
    """
    暴力递归枚举，适用于 n 很小的情况（仅作教学演示）。
    """
    ans = 0                     # 全局计数器
    seq = []                    # 当前已经选好的投掷序列

    def valid():
        """检查 seq 最后几位是否违反 rollMax 的限制"""
        if not seq:
            return True
        last = seq[-1]          # 最后一次出现的面（0~5）
        cnt = 0
        # 向左数连续相同的面有多少个
        for i in range(len(seq)-1, -1, -1):
            if seq[i] == last:
                cnt += 1
            else:
                break
        return cnt <= rollMax[last]

    def dfs(pos):
        """在第 pos 位选数字，pos 从 0 开始计数"""
        nonlocal ans
        if pos == n:            # 已经选满 n 次
            ans = (ans + 1) % MOD
            return
        for face in range(6):   # 1~6 用 0~5 表示
            seq.append(face)
            if valid():         # 只要不违规就继续往下走
                dfs(pos + 1)
            seq.pop()           # 回溯：撤销这一次选择

    dfs(0)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(6ⁿ)`  
  - 直观理解：每一步有 6 种可能，走 `n` 步就有 `6ⁿ` 条完整路径需要遍历。
- **空间复杂度**：`O(n)`  
  - 只用了递归栈和当前序列的存储，最多保存 `n` 个数字。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每一步都要遍历 6 条分支，即使很多分支在后面很早就会因为连续次数超限而被砍掉。我们可以利用**“状态记忆”**，把“已经投了多少次，最后一次投了哪个面，已经连续出现了多少次”这三个信息抽象成一个**状态**，并把对应的合法序列数存下来，后面再需要时直接查表，而不是重新枚举。

**核心概念：动态规划（Dynamic Programming）**  
- 把大问题（`n` 次投掷的合法序列数）拆成若干子问题（前 `i` 次投掷的合法序列数），子问题之间有**重叠**，因此可以用表格（DP 表）把已经算好的子结果缓存起来。

**状态定义**  
- `dp[i][j][k]` 表示：**已经投了 `i` 次**，**第 `i` 次投的是面 `j`（0~5）**，**该面已经连续出现了 `k` 次**（`1 ≤ k ≤ rollMax[j]`）时的合法序列数。  
- 这里的 `i` 从 `1` 开始计数，`k` 必须大于等于 1，因为只要出现一次就算是一次连续。

**状态转移**  
1. **继续投同一个面**：如果当前面 `j` 的连续次数 `k` 还没有达到上限 `rollMax[j]`，则可以在第 `i+1` 次仍然投 `j`，连续次数变成 `k+1`。  
   ```
   dp[i+1][j][k+1] += dp[i][j][k]
   ```
2. **换成别的面**：在第 `i+1` 次投任意其他面 `new`（`new != j`），那么连续次数重新开始为 `1`。  
   ```
   dp[i+1][new][1] += dp[i][j][k]
   ```

**初始状态**  
- 第一次投掷时可以任选 1~6 的任意面，连续次数都是 1：  
  `dp[1][j][1] = 1`（`j = 0..5`）。

**答案**  
- 当投完 `n` 次后，所有合法状态的计数相加即为答案：  
  `ans = sum(dp[n][j][k] for j in 0..5 for k in 1..rollMax[j]) mod MOD`

**为什么这比暴力快**  
- 每个状态只会被计算一次，**不再重复遍历同一条子路径**。  
- 状态总数为 `n * 6 * max(rollMax)`，其中 `max(rollMax) ≤ 15`，所以即使 `n = 5000`，总状态也只有约 `5000 * 6 * 15 = 450,000`，完全可以在毫秒级完成。

**类比**  
- 想象你在走一条有 6 条颜色的马路，每次只能往前一步。你带着一块记事本，记录“我现在在第几格、脚踩的是什么颜色、已经连续踩了多少格”。下次再来到同样的格子、同样的颜色、相同的连续次数时，你直接翻记事本得到所有可能的走法，而不必重新从起点走一遍。

#### 代码（Python）

```python
MOD = 10**9 + 7

def diceRolls_optimal(n, rollMax):
    """
    动态规划 O(n * 6 * maxRoll) 解法
    """
    m = 6                               # 骰子面数
    max_len = max(rollMax)              # 任意面最大的连续上限
    # dp[i][j][k] -> i 次投掷后，最后一次是面 j，连续出现 k 次的方案数
    # 为了省空间，只保留上一行 i 的状态，滚动数组
    dp = [[[0] * (max_len + 1) for _ in range(m)] for _ in range(2)]

    # 初始化：第 1 次投掷
    cur = 1
    for face in range(m):
        dp[cur][face][1] = 1

    # 从第 2 次投掷开始遍历
    for i in range(1, n):               # i 表示已经投掷的次数，已处理到 i 次
        prev, cur = cur, 1 - cur        # 交替使用两块缓冲区
        # 清空当前层
        for f in range(m):
            for k in range(1, rollMax[f] + 1):
                dp[cur][f][k] = 0

        for last in range(m):           # 前一次投的面
            limit = rollMax[last]
            for cnt in range(1, limit + 1):
                ways = dp[prev][last][cnt]
                if ways == 0:
                    continue

                # 1) 继续投 same face
                if cnt < rollMax[last]:
                    dp[cur][last][cnt + 1] = (dp[cur][last][cnt + 1] + ways) % MOD

                # 2) 换成其他面
                for new in range(m):
                    if new == last:
                        continue
                    dp[cur][new][1] = (dp[cur][new][1] + ways) % MOD

    # 统计第 n 次投掷的所有合法状态
    ans = 0
    final = cur if n > 1 else 1          # n=1 时我们仍在初始化的那一层
    for face in range(m):
        for cnt in range(1, rollMax[face] + 1):
            ans = (ans + dp[final][face][cnt]) % MOD
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * 6 * maxRoll)`  
  - 直观解释：我们遍历 `n` 次，每次对 6 种可能的“上一次面”以及至多 `maxRoll`（不超过 15）种连续次数做一次转移，整体大概是 “投掷次数 × 面数 × 最大连续限制”。相较于暴力的 `6ⁿ`，这在 `n=5000` 时仍然只有几十万次运算，十分轻松。

- **空间复杂度**：`O(6 * maxRoll)`（滚动数组）  
  - 只保留当前和上一轮的状态表，省去了 `n` 维的存储。相当于只需要记住“前一步”和“这一步”的信息，而不必记住所有历史。

---

## 心得

- **核心技巧**：**多维动态规划**——把“已经投了多少次、上一次是什么、已经连续出现了多少次”三个信息压进状态里，利用记忆化消除重复计算。  
- **该技巧适用的题型**：  
  1. “连续字符/数字出现次数受限”类问题（如 LeetCode 1223 `Dice Roll Simulation`、718 `Maximum Length of Repeated Subarray` 的变形）。  
  2. “带有上限的连续子序列”问题（如 1129 `Shortest Path with Alternating Colors` 中的层次计数）。  
  3. “状态受历史影响但只需记住最近几步” 的序列计数题（如 466 `Count The Repetitions`、474 `Ones and Zeroes`）。

- **一句话总结解题钥匙**：**把“连续次数”也当作状态的一部分，转移时只需要看前一次的面和它的连续计数**。

---

## 反思

- **第一反应**：看到“不能连续出现超过 X 次”，立刻想到**回溯/枚举**，因为这类限制在递归里检查最直观。  
- **最容易踩的坑**：  
  - **忘记对每个面单独设上限**，导致状态转移时把 `rollMax` 当成统一的常数。  
  - **数组越界**：连续次数 `k` 只能到 `rollMax[face]`，如果在转移时写成 `k+1` 而没有检查上限，会访问未分配的空间。  
  - **取模遗漏**：答案需要对 `10⁹+7` 取模，忘记在每一次加法后取模会导致整数溢出。  
- **下次遇到同类题，第一步该想到**：**先抽象出“状态 = 已处理元素数 + 最近一次的关键信息 + 关键信息的计数”，再判断状态的取值范围是否足够小，若足够小就可以用 DP 把指数级搜索压到多项式级**。