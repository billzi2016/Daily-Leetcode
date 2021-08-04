# #1420. 构造数组使得恰好进行 K 次比较即可找到最大值 / Build Array Where You Can Find The Maximum Exactly K Comparisons

> 难度：困难 · 标签：Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/)

---

## 题目（英文原版）

**Description**

You are given three integers n, m and k. Consider the following algorithm to find the maximum element of an array of positive integers:
You should build the array arr which has the following properties:
Return the number of ways to build the array arr under the mentioned conditions. As the answer may grow large, the answer must be computed modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 2, m = 3, k = 1
Output: 6
Explanation: The possible arrays are [1, 1], [2, 1], [2, 2], [3, 1], [3, 2] [3, 3]
```

**Example 2:**

```
Input: n = 5, m = 2, k = 3
Output: 0
Explanation: There are no possible arrays that satisfy the mentioned conditions.
```

**Example 3:**

```
Input: n = 9, m = 1, k = 1
Output: 1
Explanation: The only possible array is [1, 1, 1, 1, 1, 1, 1, 1, 1]
```

**Constraints**

- 1 <= n <= 50
- 1 <= m <= 100
- 0 <= k <= n

---

## 题目（中文翻译）

给定三个整数 n、m 和 k。考虑以下寻找正整数数组 **arr** 中最大元素的算法：

1. 初始化 `current_max = 0`，`comparisons = 0`。  
2. 依次遍历数组中的每个元素 `x`：  
   - 如果 `x > current_max`，则把 `current_max` 更新为 `x`，并将 `comparisons` 加 1。

要求构造满足下列条件的数组 **arr**（长度为 n，元素取值范围为 [1, m]）：

* 在执行上述算法的过程中，`comparisons` 最终恰好等于 k。

返回满足条件的数组 **arr** 的构造方式数目。由于答案可能非常大，请对 **10⁹ + 7** 取模后输出。

---

### 示例

**示例 1**  
输入: `n = 2, m = 3, k = 1`  
输出: `6`  
解释: 可能的数组有 `[1,1]、[2,1]、[2,2]、[3,1]、[3,2]、[3,3]`。

**示例 2**  
输入: `n = 5, m = 2, k = 3`  
输出: `0`  
解释: 不存在满足条件的数组。

**示例 3**  
输入: `n = 9, m = 1, k = 1`  
输出: `1`  
解释: 唯一可能的数组是 `[1,1,1,1,1,1,1,1,1]`。

---

### 约束条件

- `1 <= n <= 50`
- `1 <= m <= 100`
- `0 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的数组**，然后模拟题目中“从左到右找最大值”的过程，统计比较（即出现新最大值的次数），看是否恰好等于 `k`。  

- **数据结构**：  
  - 用普通的 Python 列表 `arr` 来保存数组。  
  - 用一个整数 `cnt` 记录在遍历过程中出现新最大值的次数。  
  - 把所有可能的数组想象成一本“字典”，每一页对应一种取值组合。遍历这本字典就像 **暴力搜索**，不需要额外的哈希表或堆等高级结构。  

- **为什么正确**：  
  - 我们把 **所有** 长度为 `n`、每个元素在 `[1, m]` 范围内的数组都检查了一遍。只要满足条件的就计数，显然不会漏掉任何合法答案。  

- **复杂度分析（大白话）**：  
  - 每个位置有 `m` 种可能，长度是 `n`，所以总共有 `mⁿ` 种数组。  
  - 对每一种数组，我们要遍历一次（`O(n)`）来统计比较次数。  
  - 综合下来时间是 `O(n·mⁿ)`，这在实际里是 **天文数字**（比如 `n=5, m=100` 就是 10¹⁰ 种），根本跑不完。  
  - 空间只用了存放当前枚举的数组，`O(n)`。  

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def brute_force(n: int, m: int, k: int) -> int:
    ans = 0
    # product 会产生所有长度为 n、取值范围 [1,m] 的组合
    for arr in itertools.product(range(1, m + 1), repeat=n):
        cur_max = 0          # 当前最大值，初始为 0（因为所有数都是正数）
        cnt = 0              # 出现新最大值的次数
        for x in arr:
            if x > cur_max:  # 找到更大的数，就算一次比较
                cur_max = x
                cnt += 1
        if cnt == k:         # 正好等于 k 次
            ans = (ans + 1) % MOD
    return ans
```

> 这段代码在 LeetCode 的最大测试数据下会 **超时**，仅用于说明最直接的思路。

#### 复杂度  

- **时间复杂度**：`O(n·mⁿ)`  
  - 直观理解：`mⁿ` 是所有可能的数组个数，`n` 是每个数组要遍历的长度。  
- **空间复杂度**：`O(n)`  
  - 只保存当前枚举的数组（`itertools.product` 使用迭代器），不需要额外的大表。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于**枚举全部数组**。我们要把“枚举”变成“计数”。  
观察题目：

1. **扫描过程**：从左到右遍历数组，维护当前的最大值 `cur_max`。  
2. **两种情况**  
   - 新放进去的数 **≤ cur_max** → **不产生新比较**（因为最大值不变）。  
   - 新放进去的数 **> cur_max** → **产生一次新比较**，并且 `cur_max` 变成这个更大的数。  

所以，构造数组时只需要关心 **当前的最大值** 和 **已经产生了多少次比较**。这自然引出 **动态规划**（DP）——把大问题拆成“小问题”，每一步只记录必要的状态，而不是整个数组。

---

#### 状态定义  

`dp[i][j][v]` = 前 `i` 个位置已经构造好，  
- 已经产生了恰好 `j` 次比较（即出现了 `j` 次新最大值），  
- 当前的最大值是 `v`（`1 ≤ v ≤ m`），  
- 这种情况出现的方案数（取模后）。

---

#### 初始状态  

第一个位置一定会产生一次比较（因为它本身就是最大值），并且最大值就是它本身：

```
for v in 1 .. m:
    dp[1][1][v] = 1
```

其它状态均为 0。

---

#### 转移方程  

设已经处理好前 `i-1` 位，状态是 `dp[i-1][j][v]`（最大值为 `v`，比较次数为 `j`）。

- **放入 ≤ v 的数**（不产生新比较）  
  - 有 `v` 种取法（`1 … v`），最大值仍然是 `v`，比较次数保持不变。  

```
dp[i][j][v] += dp[i-1][j][v] * v
```

- **放入 > v 的数**（产生一次新比较）  
  - 取值可以是 `v+1 … m`，每一种都会把最大值更新为新的数 `new_v`。  
  - 对每个 `new_v`（`new_v > v`），方案数只加一次（因为选定了具体的 `new_v`）。  

```
for new_v in v+1 .. m:
    dp[i][j+1][new_v] += dp[i-1][j][v]
```

把上面的两段合在一起，就是完整的转移。

> **复杂度提示**  
> 直接实现第二段的双层循环会是 `O(m²)`，总体 `O(n·k·m²)`。  
> 这里 `n ≤ 50, m ≤ 100, k ≤ n`，所以最坏约 `5·10⁷` 次运算，Python 仍能在 1 秒左右跑完。  
> 若想更快，可使用 **前缀和** 把 `v+1 … m` 的求和压缩到 `O(1)`，但为了易懂，这里保留最直观的 `O(m²)` 写法。

---

#### 结果获取  

遍历所有可能的最大值 `v`，把长度为 `n`、比较次数恰好 `k` 的方案数相加：

```
answer = sum(dp[n][k][v] for v in 1..m) % MOD
```

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def num_of_arrays(n: int, m: int, k: int) -> int:
    """
    动态规划实现
    dp[i][j][v] : 前 i 位，已经产生 j 次比较，当前最大值为 v 的方案数
    """
    # 三维数组，+1 是为了下标从 1 开始更直观
    dp = [[[0] * (m + 1) for _ in range(k + 2)] for __ in range(n + 1)]

    # 初始化：第一个元素一定产生一次比较，最大值就是它本身
    for v in range(1, m + 1):
        dp[1][1][v] = 1

    # 从第二个位置开始填表
    for i in range(2, n + 1):               # 位置 i
        for j in range(1, k + 1):           # 已经产生的比较次数
            for cur_max in range(1, m + 1):    # 当前的最大值
                cur_cnt = dp[i - 1][j][cur_max]
                if cur_cnt == 0:
                    continue

                # 1) 放入 ≤ cur_max 的数，比较次数不变
                #    有 cur_max 种取法（1~cur_max）
                dp[i][j][cur_max] = (dp[i][j][cur_max] + cur_cnt * cur_max) % MOD

                # 2) 放入 > cur_max 的数，比较次数 +1
                #    对每一个可能的新最大值 new_v，都加一次 cur_cnt
                for new_max in range(cur_max + 1, m + 1):
                    dp[i][j + 1][new_max] = (dp[i][j + 1][new_max] + cur_cnt) % MOD

    # 把所有以不同最大值结束的方案相加
    ans = sum(dp[n][k][v] for v in range(1, m + 1)) % MOD
    return ans
```

> **代码解释（关键行）**  
> - `dp = [[[0] * (m + 1) for _ in range(k + 2)] ...]`：三维表，`k+2` 是为了在 `j+1` 时不会越界。  
> - `dp[i][j][cur_max] = (dp[i][j][cur_max] + cur_cnt * cur_max) % MOD`：把“选一个 ≤ 当前最大值”的 `cur_max` 种可能全部计入。  
> - `for new_max in range(cur_max + 1, m + 1): ...`：把“选一个更大的数并更新最大值”的所有可能逐一加入。  
> - 最后 `sum(dp[n][k][v] ...)`：把长度正好 `n`、比较次数正好 `k` 的所有方案合在一起。

---

#### 复杂度  

- **时间复杂度**：`O(n·k·m²)`  
  - 直观理解：  
    - `n` 次遍历每个位置；  
    - 对每个位置要考虑 `k` 种可能的比较次数；  
    - 对每个 `cur_max`（`m` 种）还要遍历所有更大的 `new_max`（最坏 `m` 次），于是是 `m²`。  
  - 在本题约束（`n≤50, m≤100, k≤n`）下，大约几千万次基本可以接受。  

- **空间复杂度**：`O(n·k·m)`  
  - 需要保存三维 DP 表。  
  - 如果只保留前一行（`i-1`）和当前行（`i`），可以进一步压缩到 `O(k·m)`，但这里保留完整表便于阅读。

---

## 心得  

- **核心技巧**：把“比较次数”抽象为状态，利用 **动态规划** 按位置、比较次数、当前最大值分层计数。  
- **适用的类似题目**  
  1. LeetCode 1420 – **Maximum Number of Points You Can Obtain from Cards**（同样需要按顺序累计状态）  
  2. LeetCode 1359 – **Count Number of Teams**（状态是“递增/递减的子序列数”）  
  3. LeetCode 2290 – **Minimum Obstacle Removal to Reach Corner**（状态是“已经移除的障碍数”）  
- **一句话总结**：**把“遍历过程中的关键信息”——当前最大值和已产生的比较次数——用 DP 记录下来，就能在不枚举全部数组的情况下直接算出答案。**

---

## 反思  

- **第一反应**：看到“找最大值的比较次数”，立刻想到 **每次出现新最大值就计数**，于是想到把“新最大值出现的次数”作为 DP 的维度。  
- **最容易踩的坑**  
  - **初始状态**：别忘了第一个元素本身已经算一次比较，否则会少算一层。  
  - **边界**：`k` 可以为 0，但题目保证 `k ≤ n`，实现时要保证数组下标不越界（如 `j+1` 的时候要有足够的空间）。  
  - **取模**：每一次累加都要 `% MOD`，防止整数溢出。  
- **下次类似题的第一步**：先把**过程抽象成状态**（例如“当前最大值/当前最小值/已使用的资源数”），再写出**转移**，最后再考虑如何优化（前缀和、空间压缩）。