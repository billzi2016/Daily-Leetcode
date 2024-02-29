# #2597. **美丽子集的数量** / The Number of Beautiful Subsets

> 难度：中等 · 标签：Array、Hash Table、Math、Dynamic Programming、Backtracking、Sorting、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/the-number-of-beautiful-subsets/)

---

## 题目（英文原版）

**Description**

You are given an array nums of positive integers and a positive integer k.
A subset of nums is beautiful if it does not contain two integers with an absolute difference equal to k.
Return the number of non-empty beautiful subsets of the array nums.
A subset of nums is an array that can be obtained by deleting some (possibly none) elements from nums. Two subsets are different if and only if the chosen indices to delete are different.

**Examples**

**Example 1:**

```
Input: nums = [2,4,6], k = 2
Output: 4
Explanation: The beautiful subsets of the array nums are: [2], [4], [6], [2, 6].
It can be proved that there are only 4 beautiful subsets in the array [2,4,6].
```

**Example 2:**

```
Input: nums = [1], k = 1
Output: 1
Explanation: The beautiful subset of the array nums is [1].
It can be proved that there is only 1 beautiful subset in the array [1].
```

**Constraints**

- 1 <= nums.length <= 18
- 1 <= nums[i], k <= 1000

---

## 题目（中文翻译）

你得到一个由正整数构成的数组 `nums` 和一个正整数 `k`。  
如果一个 `nums` 的子集（subset）中不存在两数的绝对差（absolute difference）等于 `k`，则称该子集是 **美丽的**（beautiful）。  
返回数组 `nums` 中非空美丽子集的数量。

> **子集（subset）** 是通过删除 `nums` 中的若干（也可能不删除）元素得到的数组。  
> 当且仅当被删除的索引集合不同，两个子集才被视为不同。

### 示例

**示例 1**  
```
Input: nums = [2,4,6], k = 2
Output: 4
Explanation: nums 的美丽子集有: [2], [4], [6], [2, 6]。可以证明在数组 [2,4,6] 中仅有这 4 个美丽子集。
```

**示例 2**  
```
Input: nums = [1], k = 1
Output: 1
Explanation: nums 的唯一美丽子集是 [1]。可以证明在数组 [1] 中仅有 1 个美丽子集。
```

### 约束条件
- `1 <= nums.length <= 18`
- `1 <= nums[i], k <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组的每一种取法都枚举一遍，看看它是不是「美丽子集」。  
- **枚举方式**：把每个元素看成「要不要放进子集」的二选一，共有 `2ⁿ` 种可能（`n = len(nums)`），这正好对应 **回溯（backtracking）** 的思路。  
- **冲突检查**：在构造子集的过程中，维护一个哈希表 `cnt`（可以把它想象成「字典」：键是数字的值，值是已经选了多少个该数字）。每次想把 `nums[i]` 加进去时，只要检查 `cnt[nums[i] - k]` 是否大于 0，说明已经选了一个和它差 `k` 的数，这时候就 **不能** 再选 `nums[i]`。否则可以选，并把 `cnt[nums[i]]` 加 1。  

> **为什么这样能得到正确答案？**  
> - 回溯遍历了所有可能的子集（不遗漏），  
> - 只要发现冲突就立刻剪枝，保证留下的子集一定满足「任意两数差不等于 k」的条件。  

#### 代码（Python）

```python
from collections import Counter
from typing import List

def beautifulSubsets(nums: List[int], k: int) -> int:
    # 先把数组排序，后面的剪枝会更高效（可选）
    nums.sort()
    n = len(nums)
    cnt = Counter()          # 哈希表，记录已经选了哪些数
    ans = 0                   # 计数器

    def backtrack(idx: int) -> None:
        """从下标 idx 开始继续枚举子集"""
        nonlocal ans
        if idx == n:          # 已经考虑完所有元素
            return

        # ① 不选 nums[idx]，直接进入下一个
        backtrack(idx + 1)

        # ② 选 nums[idx] 前先检查冲突
        if cnt[nums[idx] - k] == 0:   # 没有已经选的数与它差 k
            cnt[nums[idx]] += 1       # 把它放进子集
            ans += 1                  # 只要选了一个元素，就构成了一个非空美丽子集
            backtrack(idx + 1)       # 继续向后枚举
            cnt[nums[idx]] -= 1       # 回溯：撤销选择

    backtrack(0)
    return ans
```

> **关键行解释**  
> - `cnt[nums[idx] - k] == 0`：相当于在字典里查「有没有已经选的数等于 `nums[idx] - k`」；如果没有，就可以安全选当前数。  
> - `ans += 1`：每次成功把一个新元素加入子集，当前子集（包括之前已经选的元素）就是一个合法的非空子集，计数器加一。  

#### 复杂度

- **时间复杂度**：`O(2ⁿ)`  
  解释：每个元素都有「选」或「不选」两种可能，最坏情况下会遍历所有 `2ⁿ` 种子集。`n ≤ 18`，所以即使是指数级也能跑完。  
- **空间复杂度**：`O(n)`  
  解释：递归栈的深度最多 `n`，再加上哈希表 `cnt` 最多保存 `n` 个键值对。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **指数级的枚举**。其实我们可以利用题目给出的限制 `nums[i] ≤ 1000`、`k ≤ 1000`，以及「差恰好等于 k」的特殊结构，把问题转化为「在若干条独立的链上计数不相邻的选取方式」。

**关键观察 1**  
若两个数的差为 `k`，它们一定拥有相同的余数 `mod k`（因为 `a - b = k ⇒ a ≡ b (mod k)`）。  
于是**冲突只会发生在同一个余数类**里，不同余数类之间互不影响。

**关键观察 2**  
在同一个余数类里，把所有出现的不同数值从小到大排序。  
如果两个相邻的数值恰好相差 `k`，它们之间会产生冲突；  
如果相差大于 `k`，则它们之间根本不冲突，等价于把整个序列拆成了若干**不相连的段**。

**关键观察 3**  
对每个「不相连的段」而言，内部的数值恰好形成一条「链」：  
```
v, v+k, v+2k, … , v+m·k
```
其中每个 `v + t·k` 可能出现多次（重复元素）。  
在这条链上，**同一个数值的重复出现可以随意挑选**（因为它们之间的差为 0，不是 k），  
但**相邻的两个不同数值**（相差恰好 k）**不能同时出现**。

这正好是「**不选相邻节点**」的经典计数问题。  
如果把「选该数值的方式数」记为 `choose_i = 2^{cnt_i} - 1`（从 `cnt_i` 个相同元素中选至少一个），
「不选该数值」只有一种方式 `1`，则对链上第 `i` 个不同数值有以下递推：

```
dp[i] = dp[i-1] * 1                     # 不选第 i 个数值
        + dp[i-2] * choose_i           # 选第 i 个数值，必须保证第 i-1 个不选
```

**关键观察 4**  
如果当前数值与前一个数值的差 > k，说明它们不在同一条链上，**可以直接把它们的方案数相乘**，相当于把 `dp` 重置。

**整体算法**  

1. 统计每个数值出现的次数 `cnt[x]`。  
2. 按 `x % k` 把所有不同的数值分到 `k` 个余数类（实际只需要遍历出现的余数）。  
3. 对每个余数类，取出该类的所有不同数值并排序。  
4. 用上面的 DP 计算该类内部所有合法子集的数量 `ways_class`。  
5. 把所有余数类的 `ways_class` **相乘**，得到所有合法子集（包括空集）。  
6. 最后减去 1，排除空集，即为答案。

**复杂度分析**  
- 排序所有数值：`O(n log n)`（`n = len(nums)`），是唯一的 `log` 项。  
- 其余遍历、哈希表、DP 都是线性 `O(n)`。  
- 空间上只用了若干哈希表和 DP 数组，都是 `O(n)`。

#### 代码（Python）

```python
from collections import Counter, defaultdict
from typing import List

def beautifulSubsets(nums: List[int], k: int) -> int:
    # 1️⃣ 统计出现次数
    freq = Counter(nums)                     # freq[x] = 出现次数

    # 2️⃣ 按余数分组（只对出现过的余数建表）
    groups = defaultdict(list)               # groups[r] = 同余数 r 的所有不同数值（未排序）
    for x in freq:
        groups[x % k].append(x)

    total = 1                                 # 乘积初始化为 1（空集的贡献）

    for r, values in groups.items():
        # 3️⃣ 对每个余数类内部的不同数值排序
        values.sort()
        m = len(values)

        # dp[i] 表示考虑前 i 个不同数值（1-indexed）时的合法子集数
        dp = [0] * (m + 1)
        dp[0] = 1                              # 空集

        for i in range(1, m + 1):
            cur = values[i - 1]               # 第 i 个数值
            cnt_cur = freq[cur]               # 该数值出现的次数
            choose_cur = (1 << cnt_cur) - 1   # 2^{cnt_cur} - 1，选至少一个

            # ① 不选当前数值
            dp[i] = dp[i - 1]

            # ② 检查是否与前一个数值相差恰好 k
            if i >= 2 and cur - values[i - 2] == k:
                # 必须保证前一个数值不选，才能选当前数值
                dp[i] += dp[i - 2] * choose_cur
            else:
                # 与前一个数值不冲突，直接把「选当前」的方式数乘进去
                dp[i] += dp[i - 1] * choose_cur

        # 该余数类所有合法子集（含空集）的数量
        total *= dp[m]

    # 4️⃣ 去掉整体的空集
    return total - 1
```

> **代码要点解释**  
> - `freq` 类似「字典」：键是数字，值是它出现了多少次。  
> - `choose_cur = (1 << cnt_cur) - 1` 用位移实现 `2^{cnt}`，因为 `cnt ≤ 18`，不会溢出。  
> - `dp[i]` 的两种转移对应「不选」和「选」两种决策；如果相差恰好 `k`，选当前必须把「上一个」的状态拉到 `i‑2`。  
> - 最后 `total` 是所有余数类独立贡献的乘积，减去 1 就把唯一的空子集排除掉。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序所有 `n` 个元素（`n ≤ 18`）是最耗时的步骤。其余遍历、哈希表操作、DP 都是线性 `O(n)`。  
- **空间复杂度**：`O(n)`  
  - 需要存放频率表、分组哈希表以及每个余数类的 DP 数组，均与 `n` 成正比。

---

## 心得

- **核心技巧**：把「绝对差为 k」的冲突关系转化为「同余数类内部的链式冲突」，利用「不选相邻」的动态规划计数。  
- **适用场景**：  
  1. 任意两数差不能为固定值（如本题）。  
  2. 「不能选相邻元素」的子集计数（经典的斐波那契 DP）。  
  3. 把冲突图拆成若干独立的「路径」或「树」后求独立集计数。  
- **一句话总结**：**把全局冲突拆解为余数类内部的链，分别 DP 再相乘，就是答案。**

---

## 反思

- **第一反应**：看到「子集」+「不含差为 k 的两数」直接想到「枚举子集」的回溯。  
- **最容易踩的坑**  
  - **重复元素**：要记得同一个数可以选多个（`2^{cnt}`），而不是只能选一次。  
  - **空集**：题目要求「非空」子集，最后记得减去 1。  
  - **相邻差 > k**：如果忘记把相隔大于 k 的数视为独立，DP 会错误地强加不选限制。  
- **下次类似题的第一步**：先判断冲突关系是否只在「某种固定距离」或「某种局部结构」内出现，尝试把问题拆成若干独立的「线性」或「树形」子问题，再用 DP/组合计数合并。