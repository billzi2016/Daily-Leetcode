# #740. 删除并得分 / Delete and Earn

> 难度：中等 · 标签：Array、Hash Table、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/delete-and-earn/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. You want to maximize the number of points you get by performing the following operation any number of times:
Return the maximum number of points you can earn by applying the above operation some number of times.

**Examples**

**Example 1:**

```
Input: nums = [3,4,2]
Output: 6
Explanation: You can perform the following operations:
- Delete 4 to earn 4 points. Consequently, 3 is also deleted. nums = [2].
- Delete 2 to earn 2 points. nums = [].
You earn a total of 6 points.
```

**Example 2:**

```
Input: nums = [2,2,3,3,3,4]
Output: 9
Explanation: You can perform the following operations:
- Delete a 3 to earn 3 points. All 2's and 4's are also deleted. nums = [3,3].
- Delete a 3 again to earn 3 points. nums = [3].
- Delete a 3 once more to earn 3 points. nums = [].
You earn a total of 9 points.
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums`。你可以任意次执行下面的操作，以尽可能获得更多的分数：

- 选择数组中任意一个整数 `x`，获得 `x` 分（每出现一次 `x` 即可获得一次 `x` 分），并删除所有等于 `x` 的元素。同时，数组中所有等于 `x-1` 和 `x+1` 的元素也会被删除。

返回在执行上述操作若干次后，你能够获得的最大分数。

**示例 1**  
Input: `nums = [3,4,2]`  
Output: `6`  
Explanation:  
- 删除 `4` 并获得 `4` 分，随后 `3` 也被删除。此时 `nums = [2]`。  
- 删除 `2` 并获得 `2` 分，`nums` 变为空。  
总共获得 `6` 分。

**示例 2**  
Input: `nums = [2,2,3,3,3,4]`  
Output: `9`  
Explanation:  
- 删除一个 `3` 并获得 `3` 分，所有的 `2` 和 `4` 同时被删除。此时 `nums = [3,3]`。  
- 再次删除一个 `3` 并获得 `3` 分，`nums = [3]`。  
- 再删除一次 `3` 并获得 `3` 分，`nums` 变为空。  
总共获得 `9` 分。

**约束条件**  
- `1 <= nums.length <= 2 * 10^4`  
- `1 <= nums[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**每一次都把数组里任选的一个数 `x` 删除，得到 `x` 分，同时把所有等于 `x‑1` 或 `x+1` 的数也一起删掉**，然后在剩下的数组上继续这样操作，直到数组为空。  
要找出「最大分数」就需要把所有可能的操作顺序全部枚举一遍，取最大的那个。

- **用到的数据结构**：我们只需要普通的 Python `list` 来保存当前剩余的数字。  
  - 可以把它想象成桌面上的一堆纸条，每次挑走一张（得到分数），并把相邻的纸条（数字相差 1）一起撕掉。  

- **为什么这个方法能得到正确答案**：因为我们穷举了**所有**合法的删除顺序，答案必然在其中。  

- **时间/空间复杂度**：  
  - 对每一种可能的操作，我们都要遍历整个数组去找 `x‑1`、`x+1`，这相当于 `O(n)` 的工作。  
  - 而操作的次数本身就是指数级的（每次都有 `n` 种选择），所以总时间是 `O(n!)`（或者说 `O(2^n)` 的量级），在最坏情况下会爆炸。  
  - 空间上只存放当前的数组，最多 `O(n)`。  

> 大白话：  
> - `O(n)` 就像“你要走完一条长 `n` 步的路”。  
> - `O(2^n)` 就像“每走一步都要分两条路走，路数会翻倍”。这里的暴力解实际上是“每一步都要尝遍所有剩下的数字”，所以会出现指数级的爆炸。

#### 代码（Python）

```python
from copy import deepcopy
from functools import lru_cache
from typing import List

def delete_and_earn_bruteforce(nums: List[int]) -> int:
    """
    暴力递归：尝试每一种可能的删除方式，返回最大得分。
    只在极小规模数据上可用（演示思路）。
    """
    # 为了避免在递归里修改原列表，使用深拷贝
    nums = tuple(sorted(nums))                     # 先排序，后面查找更方便

    @lru_cache(None)                               # 记忆化，防止重复子问题（仍然很慢）
    def dfs(state: tuple) -> int:
        if not state:                               # 没有数字了，得分 0
            return 0

        best = 0
        # 把 state 转成 list 方便删除操作
        cur = list(state)
        # 任选一个下标 i 作为本次删除的数字
        for i, x in enumerate(cur):
            # 计算删除 x 后剩下的数字
            next_state = [v for v in cur if v != x and v != x - 1 and v != x + 1]
            # 本次获得的分数是 x（注意：如果有多个相同的 x，只删掉一个，后面还能再选）
            gain = x + dfs(tuple(sorted(next_state)))   # 递归求后面的最大得分
            best = max(best, gain)
        return best

    return dfs(nums)


# 示例（仅用于演示，实际运行大数据会超时）
if __name__ == "__main__":
    print(delete_and_earn_bruteforce([3, 4, 2]))          # 6
    print(delete_and_earn_bruteforce([2, 2, 3, 3, 3, 4]))# 9
```

> **关键行注释**  
> - `@lru_cache`：把已经算过的「当前数组状态」记下来，避免重复计算。  
> - `next_state = [v for v in cur if v != x and v != x-1 and v != x+1]`：把选中的 `x` 以及所有 `x‑1`、`x+1` 删除。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`（指数级）——每一步都有多种选择，递归树会呈指数增长。  
- **空间复杂度**：`O(n)`——递归栈深度最坏是 `n`，加上缓存中保存的状态也最多 `O(n)`。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**“如果决定拿走某个数 `M`，就一定会把所有等于 `M` 的出现次数全部拿走”**。因为拿一次只能得到 `M` 分，而把所有 `M` 拿走可以得到 `cnt[M] * M` 分，而且它们之间互不冲突（同一个数不会相互影响）。  

因此，我们可以先把原数组**压缩**成“每个数出现了多少次”。这一步把问题从 **“数组长度可能 2·10⁴”** 转变为 **“数值范围最多 10⁴”**，便于后面做 DP。

把压缩后的信息记作 `points[x] = x * count[x]`，即**如果我们选择数字 `x`，一次性可以获得的总分**。接下来问题就变成：

> 在 1 … max_num 的序列上，**如果选择了 `x`，就不能选择 `x‑1` 与 `x+1`**，要让总得分最大。

这和经典的 **“打家劫舍（House Robber）”** 问题一模一样：  
- 每个 `x` 相当于一间房子，价值是 `points[x]`。  
- 不能连续抢两间相邻的房子（这里是相邻的数值），只能在相隔至少 1 的房子之间挑。

**动态规划**（DP）可以在 O(max_num) 时间内求解：

- `dp[i]` 表示**考虑数字 `1 … i` 时能够得到的最大分数**。  
- 转移方程：  
  - **不选 i**：`dp[i-1]`（保持前面的最优）  
  - **选 i**：`dp[i-2] + points[i]`（把 i-2 的最优加上 i 的价值）  
  - 取两者最大：`dp[i] = max(dp[i-1], dp[i-2] + points[i])`

初始化：  
- `dp[0] = 0`（没有数字得 0 分）  
- `dp[1] = points[1]`（只有数字 1 时只能拿它）  

**为什么是最优的？**  
- DP 的每一步只依赖已经计算好的子问题，且子问题覆盖了所有可能的“是否选 i”。  
- 通过“选/不选”两条路的比较，保证了全局最优。  

#### 代码（Python）

```python
from typing import List
from collections import Counter

def delete_and_earn(nums: List[int]) -> int:
    """
    动态规划（House Robber 思路）：
    1. 统计每个数字出现的次数，转化为“选这个数字能一次性得到的总分” points[x]。
    2. 在 1..max_num 上做 DP，dp[i] 表示只考虑到 i 时的最大得分。
    """
    if not nums:
        return 0

    # 1️⃣ 统计出现次数
    cnt = Counter(nums)                     # 类比：把所有纸条按数字分类，记录每类有多少张
    max_num = max(cnt)                      # 最大的数字决定 DP 的长度

    # 2️⃣ 把每个数字映射为一次性可以拿的分数
    points = [0] * (max_num + 1)             # points[i] = i * cnt[i]，下标从 0 开始，0 位置留空
    for x, c in cnt.items():
        points[x] = x * c

    # 3️⃣ DP：类似“打家劫舍”，不能选相邻的数字
    dp = [0] * (max_num + 1)
    dp[0] = 0
    dp[1] = points[1]

    for i in range(2, max_num + 1):
        # 不选 i -> dp[i-1]；选 i -> dp[i-2] + points[i]
        dp[i] = max(dp[i - 1], dp[i - 2] + points[i])

    return dp[max_num]


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(delete_and_earn([3, 4, 2]))               # 6
    print(delete_and_earn([2, 2, 3, 3, 3, 4]))      # 9
    # 额外测试
    print(delete_and_earn([1, 2, 3, 4, 5]))         # 9 (选 1+3+5)
```

> **关键行注释**  
> - `cnt = Counter(nums)`：把相同数字的纸条聚在一起，统计每类有几张。  
> - `points[x] = x * c`：如果决定把数字 `x` 全部拿走，一次性可以得到 `x` 分乘以出现次数。  
> - `dp[i] = max(dp[i-1], dp[i-2] + points[i])`：这一步是“要不要选第 i 个数字”。  

#### 复杂度  

- **时间复杂度**：`O(N + M)`，其中 `N = len(nums)`（遍历一次统计）`M = max(nums)`（DP 长度）。在本题约为 `O(2·10⁴)`，非常快。  
- **空间复杂度**：`O(M)` 用于存放 `points` 与 `dp` 数组，最坏约为 `O(10⁴)`，符合限制。  

---

## 心得  

- **核心技巧**：把“删除相邻数”问题转换成“在数轴上挑选不相邻的点”，再使用 **动态规划（House Robber）** 求解。  
- **该技巧适用的题型**：  
  1. **Delete and Earn**（本题）  
  2. **House Robber** / **House Robber II**（抢劫相邻房子）  
  3. **Maximum Sum of Non‑Adjacent Numbers**（数组中不相邻元素的最大和）  
- **一句话总结解题钥匙**：**“先把相同数字合并为一次性收益，再在 1…max_num 上做不相邻的最大收益 DP”。**  

---

## 反思  

- **第一反应**：看到“删除 `x` 时会把 `x‑1`、`x+1` 一起删”，立刻想到“相邻冲突”，于是联想到“打家劫舍”。  
- **最容易踩的坑**：  
  - 忘记把同一个数字的所有出现次数一起算进收益，导致多次重复计算。  
  - `max(nums)` 可能很大（但受约束 ≤ 10⁴），若直接在原数组长度上做 DP 会超时。  
  - 边界情况：`nums` 只包含 `1`，或者全是同一个数，需要正确初始化 `dp[1]`。  
- **下次遇到同类题**：第一步先**统计每个元素的总价值**，把原问题压缩为“在数值坐标上挑选不相邻的点”，再考虑 **House Robber** 的 DP 模型。