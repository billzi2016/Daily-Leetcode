# #2741. 特殊排列 / Special Permutations

> 难度：中等 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/special-permutations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums containing n distinct positive integers. A permutation of nums is called special if:
Return the total number of special permutations. As the answer could be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [2,3,6]
Output: 2
Explanation: [3,6,2] and [2,6,3] are the two special permutations of nums.
```

**Example 2:**

```
Input: nums = [1,4,3]
Output: 2
Explanation: [3,1,4] and [4,1,3] are the two special permutations of nums.
```

**Constraints**

- 2 <= nums.length <= 14
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

你被给定一个下标从 **0** 开始的整数数组 `nums`，其中包含 `n` 个互不相同的正整数。若一个 `nums` 的全排列满足以下条件，则称其为 **特殊排列（special permutation）**：

- 对于每个 `i`（`0 <= i < n - 1`），要么 `perm[i] % perm[i+1] == 0`，要么 `perm[i+1] % perm[i] == 0`。

返回特殊排列的总数。由于答案可能非常大，请返回 **模（modulo）** `10^9 + 7` 的结果。

**示例 1**  
输入: `nums = [2,3,6]`  
输出: `2`  
解释: `[3,6,2]` 和 `[2,6,3]` 是 `nums` 的两种特殊排列。

**示例 2**  
输入: `nums = [1,4,3]`  
输出: `2`  
解释: `[3,1,4]` 和 `[4,1,3]` 是 `nums` 的两种特殊排列。

**约束条件**

- `2 <= nums.length <= 14`
- `1 <= nums[i] <= 10^9`
- `nums` 中的所有元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 `nums` 的所有排列都枚举出来，逐个检查它们是否满足「特殊排列」的定义。  
- **数据结构**：我们可以用 Python 的 `itertools.permutations` 直接生成全排列，想象它像「把所有可能的排队顺序」一次列出来，就像把一本字典的每一页都翻一遍。  
- **正确性**：因为我们把**所有**可能的排列都遍历了一遍，凡是满足题目条件的排列必然会被计数，所以答案一定是正确的。  

#### 代码（Python）

```python
import itertools

MOD = 10 ** 9 + 7

def specialPerm_bruteforce(nums):
    n = len(nums)
    ans = 0

    # 生成所有 n! 种排列
    for perm in itertools.permutations(nums):
        ok = True
        # 检查相邻两数是否满足“前后任意一个能整除另一个”
        for i in range(n - 1):
            a, b = perm[i], perm[i + 1]
            if a % b != 0 and b % a != 0:   # 两者都不能整除则不符合
                ok = False
                break
        if ok:
            ans = (ans + 1) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是全排列的个数（比如 `n=14` 时已经是 `≈ 8.7e10`，根本不可接受）。  
  - 每个排列内部要遍历 `n-1` 条相邻关系，故乘以 `n`。  
  - 大白话：把所有可能的排队方式全部试一遍，时间会随 `n` 爆炸式增长。

- **空间复杂度**：`O(n)`  
  - 只保存当前遍历的一个排列和几个计数变量，和 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**，这一步导致指数级时间。  
我们注意到：

1. **状态只和「已经使用了哪些数字」以及「当前排列的最后一个数字」有关**。  
   - 已使用的数字可以用一个 **位掩码（bitmask）** 表示：第 `i` 位为 `1` 表示 `nums[i]` 已经放进排列。  
   - 最后一个数字决定了接下来能接的数字——只有能被它整除或能整除它的数才合法。  

2. 于是我们可以用 **动态规划（DP） + 位掩码** 来把「枚举所有排列」压缩成「遍历所有子集」的规模。  
   - `dp[last][mask]` 表示「已经使用集合 `mask`，且排列最后一个元素是 `nums[last]` 时，合法排列的个数」。  

3. 转移方程：  
   - 对于每一个未使用的元素 `next`（即 `mask` 第 `next` 位是 `0`），如果 `nums[last]` 与 `nums[next]` 满足「能整除」的关系，则可以把 `next` 接在后面。  
   - 新的状态是 `dp[next][mask | (1 << next)] += dp[last][mask]`。  

4. 初始状态：每个数字单独成一个长度为 1 的排列都是合法的。  
   - `dp[i][1 << i] = 1`（只用了第 `i` 个数）。  

5. 最终答案：所有使用了全部 `n` 个数字的状态之和。  

**为什么只需要这两个状态？**  
- `mask` 已经记录了「已经用了哪些数字」，不需要再记「用了多少个」因为可以通过 `mask` 的二进制位个数得到。  
- `last` 决定了接下来合法的候选集合，其他信息都不影响后续选择。

#### 代码（Python）

```python
from functools import lru_cache

MOD = 10 ** 9 + 7

def specialPerm(nums):
    n = len(nums)
    # 预处理能否相连的关系，方便后面查表
    can = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = nums[i], nums[j]
            can[i][j] = (a % b == 0) or (b % a == 0)   # a 能整除 b 或 b 能整除 a

    # dp[last][mask] 用字典实现稀疏存储，防止 2^14 * 14 的大数组
    from collections import defaultdict
    dp = [defaultdict(int) for _ in range(n)]

    # 初始：每个数字单独成排列
    for i in range(n):
        dp[i][1 << i] = 1

    # 枚举所有 mask（子集），从小到大扩展
    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)):   # last 不在当前子集里，跳过
                continue
            cur_cnt = dp[last][mask]
            if cur_cnt == 0:
                continue
            # 尝试把一个未使用的 next 加到末尾
            for nxt in range(n):
                if mask & (1 << nxt):      # nxt 已经使用
                    continue
                if not can[last][nxt]:     # 不能满足「能整除」的要求
                    continue
                new_mask = mask | (1 << nxt)
                dp[nxt][new_mask] = (dp[nxt][new_mask] + cur_cnt) % MOD

    full_mask = (1 << n) - 1
    ans = 0
    for last in range(n):
        ans = (ans + dp[last][full_mask]) % MOD
    return ans
```

> **代码要点解释**  
> - `can[i][j]` 就像「字典」的查表，`i` 对应的单词是 `nums[i]`，`j` 对应的页码是 `nums[j]`，看它们是否满足「能整除」的条件。  
> - `mask` 用二进制 0/1 表示「这本书的哪些页已经翻过了」；`1 << i` 把第 `i` 位设为 1，类似把第 `i` 本书标记为已读。  
> - `defaultdict(int)` 自动把未出现的键当作 0，省去显式初始化。  

#### 复杂度  

- **时间复杂度**：`O(n² * 2ⁿ)`  
  - `2ⁿ` 是所有子集的个数（`n ≤ 14`，最大约 `16384`，完全可接受）。  
  - 对每个子集我们遍历所有可能的 `last`（最多 `n`）以及所有可能的 `next`（再最多 `n`），于是得到 `n² * 2ⁿ`。  
  - 与暴力的 `n!` 相比，指数下降了很多：`14! ≈ 8.7e10` → `14²·2¹⁴ ≈ 3.2e6`。

- **空间复杂度**：`O(n * 2ⁿ)`  
  - `dp` 中保存每个 `last` 对应的所有子集的计数。  
  - 对 `n=14` 来说约 `14·16384 ≈ 2.3e5` 个整数，几百 KB 的内存。

---

## 心得

- **核心技巧**：**状态压缩 DP（位掩码）**，把「已经用了哪些元素」抽象为二进制掩码，只保留「上一个元素」作为转移依据。  
- **适用题型**：  
  1. 「旅行商问题」类的排列计数（如 LeetCode 943 *Find the Shortest Superstring*）。  
  2. 「子集状态」的计数或判定（如 LeetCode 1987 *Number of Unique Good Substrings*）。  
  3. 「满足相邻约束」的排列计数（本题即是典型例子）。  
- **一句话总结**：把「已选元素集合」压成二进制，用「最后一个元素」驱动转移，枚举子集即可高效计数。

---

## 反思

- **第一反应**：看到「排列」和「相邻满足整除」的限制，立刻想到「穷举所有排列」检验。  
- **最容易踩的坑**：  
  1. **位运算写错**：`mask & (1 << i)` 判断是否已使用，记得使用括号避免优先级错误。  
  2. **转移条件写反**：要检查 `nums[last]` 与 `nums[next]` **任意一方能整除另一方**，而不是只检查 `nums[last] % nums[next] == 0`。  
  3. **取模忘记**：累加时要及时 `% MOD`，否则中间值会爆掉。  
- **下次类似题**：第一步先思考「状态」——哪些信息足以唯一决定后续选择？若「已使用集合」和「最近一次决定」足够，就可以尝试 **DP + 位掩码**。