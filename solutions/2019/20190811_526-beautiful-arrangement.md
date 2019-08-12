# #526. **美丽排列** / Beautiful Arrangement

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/beautiful-arrangement/)

---

## 题目（英文原版）

**Description**

Suppose you have n integers labeled 1 through n. A permutation of those n integers perm (1-indexed) is considered a beautiful arrangement if for every i (1 <= i <= n), either of the following is true:
Given an integer n, return the number of the beautiful arrangements that you can construct.

**Examples**

**Example 1:**

```
Input: n = 2
Output: 2
Explanation: 
The first beautiful arrangement is [1,2]:
    - perm[1] = 1 is divisible by i = 1
    - perm[2] = 2 is divisible by i = 2
The second beautiful arrangement is [2,1]:
    - perm[1] = 2 is divisible by i = 1
    - i = 2 is divisible by perm[2] = 1
```

**Example 2:**

```
Input: n = 1
Output: 1
```

**Constraints**

- 1 <= n <= 15

---

## 题目（中文翻译）

假设你有 `n` 个整数，编号为 `1` 到 `n`。对这 `n` 个整数的一个排列 `perm`（**1-indexed**，即从下标 `1` 开始）如果满足以下条件，则称其为**美丽排列**（beautiful arrangement）：

对每个位置 `i`（`1 <= i <= n`），以下两条之一成立  
- `perm[i]` 能被 `i` 整除，即 `perm[i] % i == 0`；或  
- `i` 能被 `perm[i]` 整除，即 `i % perm[i] == 0`。

给定整数 `n`，返回可以构造的美丽排列的数量。

---

### 示例

**示例 1**  
```
Input: n = 2
Output: 2
Explanation:
第一种美丽排列是 [1, 2]：
- perm[1] = 1 能被 i = 1 整除
- perm[2] = 2 能被 i = 2 整除

第二种美丽排列是 [2, 1]：
- perm[1] = 2 能被 i = 1 整除
- i = 2 能被 perm[2] = 1 整除
```

**示例 2**  
```
Input: n = 1
Output: 1
```

---

### 约束条件

- `1 <= n <= 15`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
我们有 `n` 个数 `1 … n`，要求把它们排成一个排列 `perm`，并且 **每一个位置 `i`（从 1 开始计数）都要满足**  

* `perm[i]` 能被 `i` 整除，**或**  
* `i` 能被 `perm[i]` 整除  

最直接的想法就是 **把所有可能的排列枚举一遍**，逐个检查它们是否满足上面的条件。  

- **用到的数据结构**：  
  - `list`（列表）保存当前正在构造的排列，类似于我们在排队时手里拿着已经排好的队员。  
  - `bool` 数组 `used` 标记哪些数字已经被用了，像是“已经买票的观众”，防止同一个数字被重复使用。  

- **为什么正确**：  
  只要把 **所有** 的排列都尝试一次，就一定不会漏掉任何合法的排列。只要检查时满足题目条件，就计数。  

- **时间/空间分析（大白话）**：  
  - 枚举全部排列的数量是 `n!`（n 的阶乘），比如 `n=5` 时有 `5×4×3×2×1 = 120` 种可能。  
  - 对每一种排列，我们在构造的过程中会检查一次条件，最坏情况要遍历 `n` 层递归。  
  - 因此 **时间复杂度** 是 `O(n! )`，也就是说随着 `n` 增大，耗时会像“炸弹”一样急速增长。  
  - **空间复杂度** 主要是递归栈和 `used`、`perm` 两个数组，都是 `O(n)`，即只和 `n` 成正比，几乎可以忽略不计。

#### 代码（Python）

```python
def countArrangement_bruteforce(n: int) -> int:
    # 用来记录哪些数字已经被放进了排列
    used = [False] * (n + 1)          # 索引 0 不用，直接省掉
    ans = 0                           # 计数合法排列的总数

    # 递归函数，pos 表示当前要填的是第几个位置（从 1 开始）
    def backtrack(pos: int):
        nonlocal ans
        # 当所有位置都填完了，说明得到一个合法排列
        if pos > n:
            ans += 1
            return

        # 枚举所有可以放在当前位置的数字
        for num in range(1, n + 1):
            if not used[num]:
                # 检查“能被整除”或“被整除”这两个条件
                if num % pos == 0 or pos % num == 0:
                    used[num] = True          # 标记为已使用
                    backtrack(pos + 1)        # 继续填下一个位置
                    used[num] = False         # 回溯，撤销选择

    backtrack(1)      # 从位置 1 开始尝试
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n!)`  
  - `n!` 表示所有排列的数量，随着 `n` 增大，计算量呈指数级增长。  
- **空间复杂度**：`O(n)`  
  - 递归深度最多 `n`，加上 `used` 数组和临时变量，空间随 `n` 线性增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **枚举所有排列**，即使很多分支在中途就已经确定不可能满足条件，也要继续往下走。我们需要 **提前剪枝**，并利用**位运算**把状态压缩得更紧凑。

**核心观察**  

- 在第 `i` 位，只要找出所有满足 `i` 与 `num` “能整除或被整除”的数字 `num`，这些数字就是**候选集合**。  
- 当我们已经决定了前 `i‑1` 位使用了哪些数字后，后面的选择只和**剩余的数字集合**有关，而不需要记住具体的排列顺序。  

这正好可以用 **位掩码（bitmask）** 来表示“哪些数字已经被用了”。  
- 用一个整数的二进制位表示数字是否已使用，例如 `mask = 0b01011`（最低位对应数字 1）表示数字 `1,2,4` 已经使用。  

**动态规划 + 位掩码** 的思路如下：

1. `dp[mask]` 表示**已经使用了 `mask` 所代表的数字**，并且已经成功安排好前 `popcount(mask)`（即 `mask` 中 1 的个数）个位置的排列数目。  
2. 初始状态 `dp[0] = 1`，表示什么都没放时有一种空排列。  
3. 对每个 `mask`，计算它对应的已安排位置数 `i = popcount(mask) + 1`（因为下一个要安排的是第 `i` 位）。  
4. 枚举所有 **未使用** 的数字 `num`（即 `mask` 第 `num‑1` 位为 0），如果 `num` 与 `i` 满足条件，就把 `dp[mask | (1 << (num-1))] += dp[mask]`。  
5. 最终答案是 `dp[(1<<n) - 1]`，即所有数字都被使用的状态。

**为什么快**  

- 每个 `mask` 只遍历一次，状态数是 `2^n`（`n ≤ 15`，最多 `32768`），远小于 `n!`。  
- 位运算在 Python 中非常高效，`popcount`（统计 1 的个数）可以用 `bin(mask).count('1')` 或 `mask.bit_count()`（Python 3.8+）实现。  

**类比**：想象我们在玩拼图，每放好一块就把对应的拼图块编号标记下来（用灯亮起表示已用），下一块只需要看哪些灯还没亮，完全不必记住之前的拼图顺序。

#### 代码（Python）

```python
def countArrangement_dp_bitmask(n: int) -> int:
    # dp[mask] 表示已经使用了 mask 所对应的数字，能够得到的合法排列数
    size = 1 << n                     # 2^n 个状态
    dp = [0] * size
    dp[0] = 1                         # 空排列，唯一一种

    for mask in range(size):
        # 已经安排好的位置数 = mask 中 1 的个数
        i = mask.bit_count() + 1     # 下一个要安排的位置（从 1 开始计数）

        if i > n:                    # 所有位置都已经安排完，后面不需要再循环
            continue

        # 枚举所有未被使用的数字 num（1 ~ n）
        for num in range(1, n + 1):
            bit = 1 << (num - 1)      # 对应数字 num 的位掩码
            if mask & bit:            # 该数字已经用了，跳过
                continue
            # 检查“能被整除”或“被整除”两个条件
            if num % i == 0 or i % num == 0:
                nxt = mask | bit      # 把 num 加入已使用集合
                dp[nxt] += dp[mask]   # 把当前排列数累加到新状态

    return dp[size - 1]               # 所有数字都用了的状态即为答案
```

#### 复杂度  

- **时间复杂度**：`O(n * 2^n)`  
  - `2^n` 是所有可能的位掩码状态数，`n` 是每个状态里最多要遍历的候选数字。  
  - 对于本题的上限 `n = 15`，`n * 2^n ≈ 15 * 32768 ≈ 5·10⁵`，在毫秒级即可完成。  
- **空间复杂度**：`O(2^n)`  
  - 只需要保存一个长度为 `2^n` 的 DP 数组，约 `32768` 个整数，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：**位掩码 + 动态规划**（或等价的「记忆化搜索」），把「已经用了哪些数字」压缩成一个整数，避免重复枚举。  
- **适用的题型**（类似思路）  
  1. **求子集的最大价值**（如「分割等和子集」）  
  2. **排列/组合的计数问题**（如「N-Queens」的位运算实现）  
  3. **状态压缩 DP**（如「最小生成树的 DP」或「旅行商问题」的位 DP）  
- **一句话总结解题钥匙**：  
  > 把「已使用的数字」抽象成二进制的**位掩码**，用 DP 只在「状态」层面转移，既避免重复工作，又能快速统计所有合法排列。  

---

## 反思  

- **第一反应**：直接想到回溯枚举全部排列，代码容易写，但会在 `n=15` 时超时。  
- **最容易踩的坑**  
  - **忘记对每一层都检查整除条件**，导致计数错误。  
  - **位掩码的下标偏差**：数字 `num` 对应的位是 `1 << (num-1)`，容易写成 `1 << num`，导致数组越界或错误计数。  
  - **`popcount` 的使用**：在 Python 旧版本没有 `bit_count()`，需要兼容 `bin(mask).count('1')`。  
- **下次遇到同类题**：第一步先思考「有没有可以用位掩码描述已用元素的方式」，如果能做到，就直接走「状态压缩 DP」的路线，而不是盲目回溯。