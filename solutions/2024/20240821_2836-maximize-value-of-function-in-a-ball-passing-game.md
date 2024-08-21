# #2836. 球传递游戏中函数值的最大化 / Maximize Value of Function in a Ball Passing Game

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/maximize-value-of-function-in-a-ball-passing-game/)

---

## 题目（英文原版）

**Description**

You are given an integer array receiver of length n and an integer k. n players are playing a ball-passing game.
You choose the starting player, i. The game proceeds as follows: player i passes the ball to player receiver[i], who then passes it to receiver[receiver[i]], and so on, for k passes in total. The game's score is the sum of the indices of the players who touched the ball, including repetitions, i.e. i + receiver[i] + receiver[receiver[i]] + ... + receiver(k)[i].
Return the maximum possible score.
Notes:

**Examples**

**Example 1:**

```
Input: receiver = [2,0,1], k = 4
Output: 6
Explanation:
Starting with player i = 2 the initial score is 2:
```

**Example 2:**

```
Input: receiver = [1,1,1,2,3], k = 3
Output: 10
Explanation:
Starting with player i = 4 the initial score is 4:
```

**Constraints**

- 1 <= receiver.length == n <= 105
- 0 <= receiver[i] <= n - 1
- 1 <= k <= 1010

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `receiver` 和一个整数 `k`。`n` 名玩家参与一个传球游戏。

你可以选择任意玩家 `i` 作为起始玩家。游戏过程如下：玩家 `i` 将球传给玩家 `receiver[i]`，该玩家再将球传给 `receiver[receiver[i]]`，如此循环，总共进行 `k` 次传球。游戏的得分为所有触球玩家的下标之和，**下标可以重复计入**，即 `i + receiver[i] + receiver[receiver[i]] + … + receiver⁽ᵏ⁾[i]`。

返回 **可能的最大得分**。

**示例 1**  
``` 
Input: receiver = [2,0,1], k = 4
Output: 6
Explanation:
从玩家 i = 2 开始，初始得分为 2:
```

**示例 2**  
``` 
Input: receiver = [1,1,1,2,3], k = 3
Output: 10
Explanation:
从玩家 i = 4 开始，初始得分为 4:
```

**约束条件**

- `1 <= receiver.length == n <= 10^5`
- `0 <= receiver[i] <= n - 1`
- `1 <= k <= 10^10`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每一个玩家都当作起点**，然后**一步一步地传球**，记录下每一次传到的玩家编号并累加。  

- 用到的数据结构只有一个**数组** `receiver`（相当于“谁把球传给谁”的映射表），和几个**整数变量** 来保存当前玩家、已经传了几次、以及累计的分数。  
- 类比：把 `receiver` 想成一本**电话簿**，下标是“你”，值是“你要打给谁”。从某个人出发，顺着电话簿一直拨下去，直到拨了 `k` 次。  
- 只要我们把这个过程完整跑一遍，就一定得到 **正确** 的总分，因为题目本身就是要把这条传球链的所有编号相加。  

**为什么会对**：  
- 每一次传球的目标都是唯一确定的（`receiver[i]`），所以模拟的过程没有歧义。  
- 我们遍历了 **所有** 起点，取最大值，自然得到答案。

#### 代码（Python）

```python
def maxScore_bruteforce(receiver, k):
    n = len(receiver)
    ans = 0
    for start in range(n):                     # 每个玩家都尝试一次
        cur = start
        total = cur                             # 把起点本身计入分数
        for _ in range(k):                     # 正好传 k 次
            cur = receiver[cur]                # 按电话簿找下一个接球人
            total += cur                       # 累加这个玩家的编号
        ans = max(ans, total)                  # 记录最大的总分
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - `n` 是玩家数，`k` 是传球次数。  
  - 用大白话说，就是**“每个人都要走 `k` 步”，如果 `k` 很大（比如 10^10），这根本跑不完。**  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于要**一步步模拟 `k` 次传球**，而 `k` 可能高达 10^10，根本不可能一次一次地跑。  
我们需要把 **“一次传球”** 的操作 **合并**，一次性跳过很多步。  

这时可以借助 **二进制提升（Binary Lifting）** 的思想：  

1. **把 `k` 用二进制拆开**  
   - 任意整数 `k` 都可以写成若干个 2 的幂之和，例如 `k = 13 = 8 + 4 + 1 = 2^3 + 2^2 + 2^0`。  
   - 如果我们能够一次性“跳 2^0 步、2^1 步、2^2 步 …”，那么把对应的跳数叠加起来就恰好是 `k` 步。  

2. **预处理**  
   对每个玩家 `x`，记录 **“从 `x` 出发跳 2^j 步后会站在哪儿”** 以及 **“这 2^j 步中所有经过的玩家编号之和”**。  
   - `next[x][j]`  → 2^j 步后所在的玩家（相当于“查字典”，key 是起点和步数，value 是终点）  
   - `pref[x][j]` → 这 2^j 步中所有玩家编号的累计和（包括每一步到达的玩家）  

   递推公式（类似“爬楼梯”）  
   ```
   next[x][0] = receiver[x]                 # 只走一步
   pref[x][0] = receiver[x]                 # 这一步经过的玩家编号

   next[x][j] = next[ next[x][j-1] ][j-1]   # 先走 2^(j-1) 步到 A，再从 A 走 2^(j-1) 步到 B
   pref[x][j] = pref[x][j-1] + pref[ next[x][j-1] ][j-1]
   ```
   - 类比：把一段路程拆成**两段相同长度的子路程**，先算好每段的终点和路程长度，再把它们拼起来。  

3. **查询**  
   对每个起点 `x`，遍历 `k` 的二进制位（从低位到高位），如果第 `j` 位是 `1`，就**跳 2^j 步**：  
   ```
   ans += pref[cur][j]      # 把这段路程的分数加进去
   cur = next[cur][j]       # 更新当前位置
   ```
   同时别忘了把起点本身的编号加进总分。  

4. **取最大**  
   对所有起点求得的总分取最大即为答案。  

**为什么快**：  
- 预处理只需要 `log2(k)` 次循环，每次遍历所有 `n` 个玩家，时间 `O(n log k)`。  
- 查询每个起点时，只看 `k` 的二进制位（至多 `log2(k)` 位），所以每个起点 `O(log k)`，全部起点 `O(n log k)`。  
- 总体时间 `O(n log k)`，在本题 `n ≤ 10^5、k ≤ 10^10` 的限制下轻松通过。  

#### 代码（Python）

```python
def maxScore(receiver, k):
    """
    二进制提升 + 前缀和
    :param receiver: List[int]，receiver[i] 表示把球传给谁
    :param k: int，传球次数（不包括起点）
    :return: int，最大可能得分
    """
    n = len(receiver)
    LOG = k.bit_length()            # 最高需要多少位，k=13 -> LOG=4（因为 2^3 < 13 < 2^4）

    # 预处理二维表，使用 list 的复制方式创建
    nxt = [[0] * LOG for _ in range(n)]   # nxt[x][j] = 从 x 出发走 2^j 步后所在的玩家
    sm  = [[0] * LOG for _ in range(n)]   # sm[x][j]  = 这 2^j 步经过的玩家编号之和

    # 第 0 层（走 1 步）
    for i in range(n):
        nxt[i][0] = receiver[i]          # 只走一步直接到 receiver[i]
        sm[i][0]  = receiver[i]          # 这一步经过的玩家编号

    # 递推更高的层次（走 2^j 步）
    for j in range(1, LOG):
        for i in range(n):
            mid = nxt[i][j-1]            # 先走 2^(j-1) 步到的中间玩家
            nxt[i][j] = nxt[mid][j-1]    # 再从中间玩家走 2^(j-1) 步
            sm[i][j] = sm[i][j-1] + sm[mid][j-1]   # 两段路程的分数相加

    best = 0
    # 对每个可能的起点尝试
    for start in range(n):
        cur = start
        total = cur          # 把起点本身计入分数
        steps = k
        bit = 0
        while steps:
            if steps & 1:    # 当前位为 1，需要跳 2^bit 步
                total += sm[cur][bit]   # 累加这段路程的分数
                cur = nxt[cur][bit]     # 更新当前位置
            steps >>= 1
            bit += 1
        best = max(best, total)
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n * log k)`  
  - 预处理遍历 `n * LOG`，查询每个起点同样是 `log k` 步。  
  - 与暴力解的 `O(n * k)` 相比，**把“十万乘一万亿”降到了“十万乘三十多”。**  

- **空间复杂度**：`O(n * log k)`  
  - 需要存两个 `n × LOG` 的表，`LOG ≤ 34`（因为 `2^34 ≈ 1.7e10 > 1e10`），所以最多约 `3.4·10⁶` 个整数，约 30 MB，完全可接受。  

---

## 心得  

- **核心技巧**：**二进制提升（Binary Lifting）** + **前缀和**，把“多步跳”拆成若干个“2 的幂步”，一次查询只看二进制位数。  
- **适用的题型**  
  1. “函数迭代后第 k 步的值” 类问题（如 LeetCode 1696. Jump Game VI 的变体）。  
  2. “在有向图中走 k 步的最远/最大/最小值” （如树上祖先查询、链式跳转）。  
  3. “循环或重复结构中累计求和” 的大步模拟（如 “循环数组的第 k 次访问和”。）  
- **一句话总结**：**把大步拆成二进制的若干小步，预先算好每一步的终点和贡献，查询时只看二进制位就能瞬间跳完。**  

---

## 反思  

- **第一反应**：看到“k 可能非常大”，立刻想到**二进制分解**或**快速幂**的思想，寻找能把指数级的循环压缩的方法。  
- **最容易踩的坑**  
  - **忘记把起点本身计入分数**（题目要求包括起始玩家）。  
  - **数组越界**：在预处理时 `next[x][j-1]` 必须已经在表中，确保 `LOG` 足够大（`k.bit_length()`）。  
  - **整数溢出**（在 Python 不会）或 **使用 Python 列表嵌套导致内存爆炸**，要注意 `LOG` 只取必要的位数。  
- **下次遇到同类题**，第一步应该：**把大次数写成二进制，思考是否可以用“跳表/二进制提升”预处理每个状态的 2^i 步转移和累计值**，再在每个起点上按位跳。