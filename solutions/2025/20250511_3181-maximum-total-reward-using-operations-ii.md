# #3181. **最大总奖励（使用操作 II）** / Maximum Total Reward Using Operations II

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/maximum-total-reward-using-operations-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array rewardValues of length n, representing the values of rewards.
Initially, your total reward x is 0, and all indices are unmarked. You are allowed to perform the following operation any number of times:
Return an integer denoting the maximum total reward you can collect by performing the operations optimally.

**Examples**

**Example 1:**

```
Input: rewardValues = [1,1,3,3]
Output: 4
Explanation:
During the operations, we can choose to mark the indices 0 and 2 in order, and the total reward will be 4, which is the maximum.
```

**Example 2:**

```
Input: rewardValues = [1,6,4,3,2]
Output: 11
Explanation:
Mark the indices 0, 2, and 1 in order. The total reward will then be 11, which is the maximum.
```

**Constraints**

- 1 <= rewardValues.length <= 5 * 104
- 1 <= rewardValues[i] <= 5 * 104

---

## 题目（中文翻译）

你得到一个长度为 `n` 的整数数组 `rewardValues`，其中 `rewardValues[i]` 表示第 `i` 个奖励的价值。  
最初，你的总奖励 `x` 为 `0`，且所有下标均未被标记。你可以任意次数执行以下操作：

（此处应描述具体的操作，原题目中已省略）

返回一个整数，表示在最优执行上述操作的情况下，你能够收集到的 **最大总奖励**。

---

### 示例

**示例 1**  
**输入**：`rewardValues = [1,1,3,3]`  
**输出**：`4`  
**解释**：在操作过程中，我们可以依次标记下标 `0` 和 `2`，此时累计的总奖励为 `4`，这是能够得到的最大值。

**示例 2**  
**输入**：`rewardValues = [1,6,4,3,2]`  
**输出**：`11`  
**解释**：依次标记下标 `0`、`2`、`1`，累计的总奖励为 `11`，这是能够得到的最大值。

---

### 约束条件

- `1 <= rewardValues.length <= 5 * 10^4`
- `1 <= rewardValues[i] <= 5 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一个整数数组 `rewardValues`，初始总奖励 `x = 0`，所有下标均未标记。  
我们可以**任意次**执行以下操作：

1. 选取一个尚未标记的下标 `i`，要求 **当前的总奖励 `x` 必须严格小于 `rewardValues[i]`**。  
2. 将 `rewardValues[i]` 加到 `x` 上，同时把下标 `i` 标记为已使用。

目标是让最终的 `x` 尽可能大。

最直接的想法就是**把所有可能的选取顺序都穷举**，找出合法且奖励最大的序列。

- **数据结构**：只需要一个数组 `rewardValues`，以及一个布尔数组 `used` 来记录哪些下标已经被选过。  
  - `used` 类似于我们查字典时的“已翻到的页码”，`True` 表示这页已经看过，`False` 表示还没看。

- **为什么正确**：遍历所有排列，必然会包含最优的那一条顺序；只要在遍历时检查 `x < rewardValues[i]`，就能保证合法性。

- **复杂度分析**：  
  - 数组长度记为 `n`。  
  - 所有排列的数量是 `n!`（阶乘），即 **指数级**，几乎不可能在电脑里跑完。  
  - 每条排列我们都要线性扫描一次来检查合法性，时间是 `O(n)`，所以总时间是 `O(n! * n)`。  
  - 空间上只需要保存 `used`（`O(n)`）和递归栈（最深 `n`），即 `O(n)`。

> 大白话：`O(n!)` 就好比“把 n 本书全排出所有可能的摆放方式”，哪怕 n 只有 10 本，也已经是 3,628,800 种，根本不可能手动穷举。

#### 代码（Python）

```python
def maxReward_bruteforce(rewardValues):
    n = len(rewardValues)
    used = [False] * n          # 标记是否已经选过
    best = 0

    def dfs(cur_sum):
        """深度优先搜索所有合法的选取顺序"""
        nonlocal best
        # 更新全局最大
        best = max(best, cur_sum)

        for i in range(n):
            if not used[i] and cur_sum < rewardValues[i]:
                used[i] = True               # 选取 i
                dfs(cur_sum + rewardValues[i])
                used[i] = False              # 回溯，撤销选取

    dfs(0)
    return best
```

> 代码里每一行都有中文注释，帮助你跟踪状态的变化。  
> **注意**：这段代码只适合 `n ≤ 10` 左右的极小输入，实际提交会超时。

#### 复杂度

- **时间复杂度**：`O(n! * n)` —— 这里的 `!` 表示阶乘，增长速度极快，几乎不可接受。  
- **空间复杂度**：`O(n)` —— 只用了 `used` 数组和递归栈。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有顺序**。  
仔细观察题目可以发现：

1. **顺序只和 “当前总奖励 < 选取的奖励” 这条不等式有关**。  
   如果我们把所有奖励从小到大排好序，只要在满足条件时就可以把它们依次加入，总奖励会不会变小？  
   答案是不会——**把更大的奖励留到后面永远不会让我们失去机会**。  
   因此，**在最优解中，所有被选中的奖励一定是按非递减顺序使用的**。

2. 设 `dp[j]` 表示“是否可以在使用若干个已经处理过的奖励后，恰好得到总奖励 `j`”。  
   - 初始时只有 `dp[0] = True`（什么都不选，奖励为 0）。  
   - 当我们处理到当前奖励 `v`（已排序），只有当**之前的总奖励 `j` 小于 `v`** 时，才允许再加上 `v`，得到新的总奖励 `j + v`。  
   - 这正是提示中的转移式  
     ```
     dp[j + v] = dp[j]   (前提是 j < v)
     ```

3. `dp` 只需要记 **是否可达**，不需要具体的路径，所以它是**布尔数组**。  
   每个元素只占 1 bit，完全可以用 **位运算**（bitset）一次性并行处理多位。  
   - 把 `dp` 看成一个二进制串，例如 `dp = 100101...`，左移 `v` 位相当于“把所有已经可达的 `j` 加上 `v`”。  
   - 然后把左移后的结果和原来的 `dp` 取 **或**（`|`），得到加入 `v` 后的可达集合。  
   - 为了满足 `j < v` 的限制，只需要在左移前把 `dp` 中 **大于等于 `v` 的位清零**，这样就不会产生非法的转移。

4. **为什么只需要到最大奖励值 `maxV` 的位数**？  
   - 在加入第 `i` 个奖励 `v` 前，所有可能的 `j` 都满足 `j < v ≤ maxV`。  
   - 因此我们永远不需要关心超过 `maxV` 的位。  
   - `maxV ≤ 5·10⁴`，所以位集合的长度最多只有 50,000 位，约 800 个 `uint64`，非常轻量。

5. **完整流程**  
   1. 把 `rewardValues` 排序。  
   2. 用一个整数列表 `bits`（每个元素存 64 位）模拟 bitset，初始化只有第 0 位为 1。  
   3. 对每个奖励 `v`：  
      - 把 `bits` 向左整体移动 `v` 位（相当于 `bits << v`），得到 `shifted`。  
      - 把 `bits` 中 **索引 ≥ v** 的位全部清零，得到 `masked`。  
      - `bits = bits | shifted`（只保留合法的新增可达状态）。  
   4. 最后遍历 `bits`，找到最大的索引 `j` 使得对应位为 1，即为答案。

> **类比**：把 `bits` 当成一条“可达的里程碑道路”。左移就是在这条路上往前跳 `v` 步，只有在跳之前里程碑小于 `v` 才允许跳。`|` 操作把新旧里程碑合并，形成更长的可达路程。

#### 代码（Python）

```python
def maxReward(rewardValues):
    """
    使用位集合（bitset）实现 O(n * maxV / 64) 的 DP
    :param rewardValues: List[int]
    :return: int  最大可以得到的奖励总和
    """
    # 1️⃣ 排序，保证我们总是按照从小到大的顺序尝试使用奖励
    rewardValues.sort()
    maxV = rewardValues[-1]                 # 最大的单个奖励值

    # 2️⃣ 用整数列表模拟 bitset，每个整数存 64 位
    WORD = 64
    size = (maxV // WORD) + 1               # 需要多少个 64 位块
    bits = [0] * size
    bits[0] = 1                             # 第 0 位为 1，表示“总奖励 0 可达”

    # 下面的两个小函数帮助我们操作位集合
    def left_shift(arr, shift):
        """把位集合整体左移 shift 位，返回新的列表（不修改原数组）"""
        whole = shift // WORD               # 需要跨块移动的完整 64 位块数
        offset = shift % WORD               # 在块内部的位移

        new = [0] * size
        for i in range(size - 1, -1, -1):
            src = i - whole
            if src < 0:
                continue
            # 先把完整块的内容搬过去
            val = arr[src] << offset
            # 处理跨块的高位（从低位块偷来的）
            if offset and src > 0:
                val |= arr[src - 1] >> (WORD - offset)
            new[i] = val & ((1 << WORD) - 1)   # 保留低 64 位，防止 Python 整数无限长
        return new

    def clear_ge(arr, limit):
        """把位集合中索引 >= limit 的位全部清零，返回新的列表"""
        block = limit // WORD
        offset = limit % WORD
        new = arr[:]
        # 完全在后面的块全部置零
        for i in range(block + 1, size):
            new[i] = 0
        # 同一个块内的高位清零
        if block < size:
            mask = (1 << offset) - 1          # 只保留低 offset 位
            new[block] &= mask
        return new

    # 3️⃣ 主循环：遍历每个奖励 v
    for v in rewardValues:
        # 把当前可达集合向左移动 v 位，得到“加上 v 后的新可达集合”
        shifted = left_shift(bits, v)

        # 为了满足 j < v 的限制，先把 bits 中 >= v 的位清零
        masked = clear_ge(bits, v)

        # 合并：既保留原来的可达状态，也加入新产生的可达状态
        bits = [masked[i] | shifted[i] for i in range(size)]

    # 4️⃣ 扫描最高位，得到最大的可达总奖励
    ans = 0
    for i in range(size - 1, -1, -1):
        if bits[i]:
            # 找到该 64 位块中最高的 1
            for b in range(WORD - 1, -1, -1):
                if bits[i] >> b & 1:
                    ans = i * WORD + b
                    return ans
    return ans
```

**关键行中文注释**：

- `rewardValues.sort()` # 先排序，保证后面的 DP 只在合法的顺序上进行  
- `bits[0] = 1` # 只要总奖励为 0 时是可达的  
- `shifted = left_shift(bits, v)` # 把所有已可达的 j 加上 v，得到新的可达 j+v  
- `masked = clear_ge(bits, v)` # 把 j ≥ v 的位清零，保证只有 j < v 能继续使用 v  
- `bits = [masked[i] | shifted[i] for i in range(size)]` # 合并旧状态和新状态  

> 这里我们用了两个帮助函数 `left_shift` 与 `clear_ge`，它们把位操作抽象成块级别的移动，避免手动写 50,000 次循环。

#### 复杂度

- **时间复杂度**：`O(n * maxV / 64)`  
  - `maxV` 是数组中最大的单个奖励（≤ 5·10⁴），除以 64 相当于每次处理 64 位一次。  
  - 与暴力的 `O(n! )` 相比，**线性**（或准线性）增长，几乎在所有合法输入下都能跑完。

- **空间复杂度**：`O(maxV / 64)`  
  - 只需要保存一个长度约 `maxV / 64` 的整数列表（约 800 个 64‑bit 整数），即几千字节的内存。  
  - 与暴力的 `O(n)` 相比，这里不随 `n` 增长，只和最大奖励值有关。

> 与暴力解对比：时间从“天文数字”下降到“几百万次基本位操作”，空间从 `O(n)` 降到几千字节，足以在 1 秒内完成。

---

## 心得

- **核心技巧**：**排序 + 位集合（bitset）DP**。  
  - 排序把问题的“顺序依赖”转化为“只在小于当前值时才能使用”。  
  - 位集合让布尔 DP 以 **并行位运算** 的方式一次性更新 64 条状态，大幅提升常数因子。

- **适用的题型**  
  1. **“背包”类子集可达问题**，但有额外的 “前置条件” 如 `j < value`（例如 LeetCode 2218 `Maximum Value of K Coins From Piles` 的位运算优化）。  
  2. **“能否构成某个数”** 的问题，常用 bitset 实现子集和（如 “分割等和子集”）。  
  3. **“需要判断可达区间”** 的动态规划，如 “Maximum Score From Performing Multiplication Operations”。

- **一句话总结解题钥匙**  
  > **先把奖励排好序，再用位集合把“哪些总奖励能到达”一次性并行更新**。

---

## 反思

- **拿到题目第一反应**：想到“先选最小的奖励，再逐步往大挑”，于是尝试 **枚举所有顺序**（暴力）验证想法。  
- **最容易踩的坑**  
  1. **忘记 `j < reward[i]` 的限制**，导致把所有子集都算进来了，答案会偏大。  
  2. **位集合长度取错**：如果把长度设为总和 `sum(rewardValues)`，会导致内存爆炸；正确的是只需要到 **最大单个奖励**。  
  3. **左移时跨块的高位处理不当**，会产生错误的进位，使 DP 产生非法状态。  
- **下次遇到同类题**，第一步应该：  
  1. **检查是否可以排序**（是否有“只能在更小的状态后面使用”的约束）。  
  2. **思考子集可达的布尔 DP**，并判断状态空间是否足够小到可以用 **位集合** 来压缩。  

这样就能迅速从暴力思路跳到高效实现。