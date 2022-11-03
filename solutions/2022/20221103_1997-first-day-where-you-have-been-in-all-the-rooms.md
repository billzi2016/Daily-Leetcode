# #1997. 首次访问所有房间的第一天 / First Day Where You Have Been in All the Rooms

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/first-day-where-you-have-been-in-all-the-rooms/)

---

## 题目（英文原版）

**Description**

There are n rooms you need to visit, labeled from 0 to n - 1. Each day is labeled, starting from 0. You will go in and visit one room a day.
Initially on day 0, you visit room 0. The order you visit the rooms for the coming days is determined by the following rules and a given 0-indexed array nextVisit of length n:
Return the label of the first day where you have been in all the rooms. It can be shown that such a day exists. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nextVisit = [0,0]
Output: 2
Explanation:
- On day 0, you visit room 0. The total times you have been in room 0 is 1, which is odd.
  On the next day you will visit room nextVisit[0] = 0
- On day 1, you visit room 0, The total times you have been in room 0 is 2, which is even.
  On the next day you will visit room (0 + 1) mod 2 = 1
- On day 2, you visit room 1. This is the first day where you have been in all the rooms.
```

**Example 2:**

```
Input: nextVisit = [0,0,2]
Output: 6
Explanation:
Your room visiting order for each day is: [0,0,1,0,0,1,2,...].
Day 6 is the first day where you have been in all the rooms.
```

**Example 3:**

```
Input: nextVisit = [0,1,2,0]
Output: 6
Explanation:
Your room visiting order for each day is: [0,0,1,1,2,2,3,...].
Day 6 is the first day where you have been in all the rooms.
```

**Constraints**

- n == nextVisit.length
- 2 <= n <= 105
- 0 <= nextVisit[i] <= i

---

## 题目（中文翻译）

**描述**  
有 `n` 个房间需要访问，编号从 `0` 到 `n - 1`。每一天都有一个编号，从 `0` 开始。你每天只能进入并访问 **一个房间**。  
初始时（第 `0` 天），你访问房间 `0`。接下来几天访问房间的顺序由以下规则以及给定的 **0 索引数组** `nextVisit`（长度为 `n`）决定：

- 设第 `d` 天你所在的房间为 `cur`，并且你已经进入该房间的次数为 `cnt`（包括当天）。  
- 如果 `cnt` 为 **奇数**，则第 `d + 1` 天你将访问 `nextVisit[cur]`。  
- 如果 `cnt` 为 **偶数**，则第 `d + 1` 天你将访问 `(cur + 1) mod n`。

返回你 **首次** 访问过 **所有房间** 的那一天的编号。可以证明这样的一天一定存在。由于答案可能非常大，请返回 `answer mod (10^9 + 7)`。

**示例**

*示例 1*  
```
Input: nextVisit = [0,0]
Output: 2
Explanation:
- 第 0 天，访问房间 0。此时访问房间 0 的次数为 1（奇数），所以第 1 天访问 nextVisit[0] = 0。
- 第 1 天，访问房间 0。此时访问房间 0 的次数为 2（偶数），所以第 2 天访问 (0 + 1) mod 2 = 1。
- 第 2 天，访问房间 1。这是首次访问到所有房间的那一天。
```

*示例 2*  
```
Input: nextVisit = [0,0,2]
Output: 6
Explanation:
每天的访问顺序为: [0,0,1,0,0,1,2,...]。第 6 天是首次访问到所有房间的那一天。
```

*示例 3*  
```
Input: nextVisit = [0,1,2,0]
Output: 6
Explanation:
每天的访问顺序为: [0,0,1,1,2,2,3,...]。第 6 天是首次访问到所有房间的那一天。
```

**约束条件**

- `n == nextVisit.length`
- `2 <= n <= 10^5`
- `0 <= nextVisit[i] <= i`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是 **把题目描述完整地模拟** ：  
- 用一个数组 `cnt[i]` 记录每个房间已经进入了多少次。  
- 用变量 `day` 表示当前是第几天，用 `cur` 表示今天要去的房间编号。  
- 每天按照规则更新 `cnt[cur]`，判断奇偶决定下一天要去的房间：  

```
if cnt[cur] 是奇数 → next = nextVisit[cur]
else               → next = (cur + 1) % n
```

- 每走完一天，就检查 `cnt` 中是否所有房间的访问次数都 ≥ 1，若是则返回当前的 `day`。  

> **类比**：`cnt` 就像我们在玩“去图书馆借书”，每本书对应一个房间，`cnt[i]` 记录我们已经借过这本书几次。只要每本书至少借过一次，就算完成任务。

**为什么正确**  
因为我们严格按照题目给出的“每一天的转移规则”去执行，没有任何简化或猜测，必然得到真实的访问顺序。只要遍历到所有房间被访问过，返回的天数一定是题目要求的“第一次”。

**时间/空间复杂度**  
- 最坏情况下，**每走一步只会让我们多访问一个已经访问过的房间**，所以要等到第 `O(2^n)`（指数级）步才可能遍历完所有房间。  
- 空间只需要保存 `cnt`（长度 `n`）和几个变量，**O(n)**。

> **大白话**：`O(2^n)` 就像我们把所有可能的路径都尝试一遍，随着房间数增加，所需的天数会像“翻倍的雪球”一样疯狂增长，根本跑不完。

#### 代码（Python）

```python
MOD = 10**9 + 7  # 题目要求的取模（虽然暴力解不需要）

def firstDayBrute(nextVisit):
    n = len(nextVisit)
    cnt = [0] * n            # 记录每个房间被访问的次数
    cur = 0                  # 第 0 天进入房间 0
    day = 0

    while True:
        cnt[cur] += 1        # 今天访问了 cur
        # 检查是否所有房间都已经被访问过
        if all(c > 0 for c in cnt):
            return day       # 第一次满足条件的 day

        # 根据奇偶决定明天去哪个房间
        if cnt[cur] % 2 == 1:          # 奇数次 → 按 nextVisit
            nxt = nextVisit[cur]
        else:                           # 偶数次 → 往右走一格（循环）
            nxt = (cur + 1) % n

        cur = nxt
        day += 1
```

> 这段代码可以直接跑通小规模的例子（如 `n ≤ 10`），但对正式数据会 **超时**。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级），因为每增加一个房间，可能需要指数倍的天数才能把它拉进来。  
- **空间复杂度**：`O(n)`，只存储每个房间的访问计数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于我们每次都从头算起**，而实际上我们只关心“**第一次进入每个房间的天数**”。如果我们记住了这些天数，就可以跳过大量重复的计算。

---

#### 2.1 关键观察  

- **只能在房间 `i` 的访问次数为偶数时，才会前往 `i+1`**（题目 hint 已经给出）。  
- 因此，**第一次进入房间 `i`**（记为 `day[i]`）一定是 **在 `i-1` 被访问了偶数次之后** 才可能发生的。  
- 当我们在房间 `i-1` 第一次出现**奇数次**时，规则强制我们回到 `nextVisit[i-1]`（它的编号 ≤ `i-1`），随后再按照同样的规则回到 `i-1`，这一次恰好是 **偶数次**，于是我们才能继续前进到 `i`。  

换句话说，**从 `nextVisit[i-1]` 再回到 `i-1` 的这段过程是固定的**，只和已经算好的 `day` 有关。  

---

#### 2.2 动态规划公式  

设  

- `dp[i]` = **第一次进入房间 `i` 的天数**（从第 0 天算起，0‑based）。  
- `dp[0] = 0`，因为题目说第 0 天就已经在房间 0。  

当我们要进入房间 `i (≥1)` 时，过程如下（下面用 `i-1` 表示前一个房间）：

1. 已经在 `i-1` 的第一次出现（奇数次）时的天数是 `dp[i-1]`。  
2. 再次访问 `i-1`（变成偶数次）需要 **再走一次**，于是我们会去 `nextVisit[i-1]`，这一步花 **1 天**。  
3. 从 `nextVisit[i-1]` 再回到 `i-1` 需要 **`dp[i-1] - dp[nextVisit[i-1]]` 天**（因为 `dp[i-1]` 包含了从 `nextVisit[i-1]` 再次到达 `i-1` 的全部天数）。  
4. 再一次访问 `i-1`（此时是偶数次）再花 **1 天** 前往 `i`。

把上述四段时间相加：

```
dp[i] = dp[i-1]                # 第一次到达 i-1（奇数次）
       + 1                     # 去 nextVisit[i-1]
       + (dp[i-1] - dp[nextVisit[i-1]])   # 从 nextVisit[i-1] 回到 i-1
       + 1                     # 再次访问 i-1（偶数次）后前往 i
```

整理得到简洁的递推式：

```
dp[i] = 2 * dp[i-1] - dp[nextVisit[i-1]] + 2
```

因为答案可能非常大，需要对 `10^9+7` 取模，递推式的每一步都可以 **先取模再相加/相减**，防止溢出。

---

#### 2.3 为什么递推是 O(n)  

- 计算 `dp[i]` 只依赖 `dp[i-1]` 和 `dp[nextVisit[i-1]]`，而 `nextVisit[i-1] ≤ i-1`，所以在顺序遍历 `i = 1 … n-1` 时，这两个值一定已经算好。  
- 每一步的算术操作都是常数时间，**总共只需要 O(n) 次**。  

---

#### 2.4 伪代码（文字版）  

```
MOD = 1_000_000_007
dp[0] = 0
for i = 1 .. n-1:
    dp[i] = (2*dp[i-1] - dp[nextVisit[i-1]] + 2) % MOD
return dp[n-1]          # 第一次进入最后一个房间的那天，即所有房间都被访问过
```

> **类比**：想象每个房间都是一座城堡，`dp[i]` 记录我们第一次踏进第 `i` 座城堡的时间。城堡之间的通道（规则）让我们在 **奇数次** 必须先绕到一个更早的城堡再回来，这个“绕路”时间正好可以用已经算好的 `dp` 来表示，于是我们一步步递推得到所有城堡的“首次踏足时间”。  

---

#### 代码（Python）

```python
def firstDayWhereAllRoomsVisited(nextVisit):
    """
    动态规划 O(n) 解法
    返回第一次所有房间都被访问过的那一天（取模 1e9+7）
    """
    MOD = 10**9 + 7
    n = len(nextVisit)

    dp = [0] * n          # dp[i] = 第一次进入房间 i 的天数
    # dp[0] 已经是 0（第 0 天在房间 0）

    for i in range(1, n):
        # 根据公式 dp[i] = 2*dp[i-1] - dp[nextVisit[i-1]] + 2
        # 先做乘法再加减，最后统一取模，防止负数
        val = (2 * dp[i - 1]) % MOD                # 2 * dp[i-1]
        val = (val - dp[nextVisit[i - 1]]) % MOD   # - dp[nextVisit[i-1]]
        val = (val + 2) % MOD                      # + 2
        dp[i] = val

    return dp[-1]   # 第一次踏进最后一个房间的天数，就是答案
```

> 代码里每一行都配有中文注释，直接复制运行即可得到答案。  

---

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组 `nextVisit`，每一步做常数次加减乘取模。  
  - 与暴力解的指数级时间相比，快了 **天文倍数**，即使 `n = 10^5` 也毫秒级完成。  

- **空间复杂度**：`O(n)`（存 `dp`）  
  - 也可以只保留最近的两个值进一步压缩到 `O(1)`，但 `O(n)` 已经足够且更易于理解。  

---

## 心得  

- **核心技巧**：**把“第一次进入每个房间的天数”抽象出来，用动态规划避免重复计数**。  
- **相似题型**（可以套用同样的思路）：  
  1. LeetCode 2645 *Minimum Number of Operations to Make All Array Elements Equal to 1*（利用状态转移递推）  
  2. LeetCode 2265 *Count Nodes Equal to Average of Subtree*（对每个子树的结果做前缀/后缀累加）  
  3. LeetCode 1977 *Number of Ways to Separate Numbers into Groups*（同样把“第一次出现”转化为 DP）  

- **一句话总结**：**把“每一次真正需要计算的”抽象成一个状态，利用已知的递推关系一次遍历求出全部答案。**  

---

## 反思  

- **第一反应**：直接把规则写成循环模拟，想把“什么时候所有房间都出现过”直接判断。  
- **最容易踩的坑**：  
  - 忽视取模导致整数溢出（尤其 `2*dp[i-1]` 可能超过 64 位）。  
  - 在递推式中出现负数时忘记加上 `MOD` 再取模，导致 Python 的负数模结果不符合题意。  
  - 没有意识到 `nextVisit[i] ≤ i`，从而误以为需要额外的循环或搜索。  
- **下次类似题**：看到“**只能在某种奇偶状态下才能前进**”时，立刻思考**把每个位置的“首次达到的时间”作为 DP 状态**，并尝试从已知的**前一个状态**推导出当前状态的公式。这样往往能把指数级的过程压缩到线性时间。