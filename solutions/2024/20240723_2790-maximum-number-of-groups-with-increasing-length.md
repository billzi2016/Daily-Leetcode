# #2790. 最大递增长度分组数 / Maximum Number of Groups With Increasing Length

> 难度：困难 · 标签：Array、Math、Binary Search、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-groups-with-increasing-length/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array usageLimits of length n.
Your task is to create groups using numbers from 0 to n - 1, ensuring that each number, i, is used no more than usageLimits[i] times in total across all groups. You must also satisfy the following conditions:
Return an integer denoting the maximum number of groups you can create while satisfying these conditions.

**Examples**

**Example 1:**

```
Input: usageLimits = [1,2,5]
Output: 3
Explanation: In this example, we can use 0 at most once, 1 at most twice, and 2 at most five times.
One way of creating the maximum number of groups while satisfying the conditions is: 
Group 1 contains the number [2].
Group 2 contains the numbers [1,2].
Group 3 contains the numbers [0,1,2]. 
It can be shown that the maximum number of groups is 3. 
So, the output is 3.
```

**Example 2:**

```
Input: usageLimits = [2,1,2]
Output: 2
Explanation: In this example, we can use 0 at most twice, 1 at most once, and 2 at most twice.
One way of creating the maximum number of groups while satisfying the conditions is:
Group 1 contains the number [0].
Group 2 contains the numbers [1,2].
It can be shown that the maximum number of groups is 2.
So, the output is 2.
```

**Example 3:**

```
Input: usageLimits = [1,1]
Output: 1
Explanation: In this example, we can use both 0 and 1 at most once.
One way of creating the maximum number of groups while satisfying the conditions is:
Group 1 contains the number [0].
It can be shown that the maximum number of groups is 1.
So, the output is 1.
```

**Constraints**

- 1 <= usageLimits.length <= 105
- 1 <= usageLimits[i] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的数组 `usageLimits`，长度为 `n`。  
你的任务是使用数字 `0` 到 `n‑1` 创建若干分组，要求每个数字 `i` 在所有分组中使用的总次数不超过 `usageLimits[i]`。同时，还必须满足以下条件：

- 第 `k` 个分组的大小（即分组中数字的个数）必须严格大于第 `k‑1` 个分组的大小。

返回一个整数，表示在满足上述所有条件的情况下，你能够创建的分组的最大数量。

**示例 1**  
```
输入: usageLimits = [1,2,5]
输出: 3
解释: 在此示例中，数字 0 最多使用 1 次，数字 1 最多使用 2 次，数字 2 最多使用 5 次。
一种能够得到最大分组数的方案如下:
- 第 1 组包含数字 [2]。
- 第 2 组包含数字 [1,2]。
- 第 3 组包含数字 [0,1,2]。
可以证明，最大分组数为 3。
```

**示例 2**  
```
输入: usageLimits = [2,1,2]
输出: 2
解释: 在此示例中，数字 0 最多使用 2 次，数字 1 最多使用 1 次，数字 2 最多使用 2 次。
一种能够得到最大分组数的方案如下:
- 第 1 组包含数字 [0]。
- 第 2 组包含数字 [1,2]。
可以证明，最大分组数为 2。
```

**示例 3**  
```
输入: usageLimits = [1,1]
输出: 1
解释: 在此示例中，数字 0 和数字 1 均最多使用 1 次。
一种能够得到最大分组数的方案如下:
- 第 1 组包含数字 [0]。
可以证明，最大分组数为 1。
```

**约束条件**  
- `1 <= usageLimits.length <= 10^5`  
- `1 <= usageLimits[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的分组方式都穷举**，然后挑出满足使用次数上限的、组数最多的方案。  
可以把每个数字 `i` 看成一本字典，`usageLimits[i]` 是这本字典里可以翻到的页数——我们只能在所有的组里把这本字典翻到的页数累计不超过它的上限。  

具体做法（仅作概念展示）：

1. 先决定要创建多少组 `k`（从 1 开始逐渐增大）。  
2. 按照题目要求，第 `1` 组要放 `1` 个数，第 `2` 组要放 `2` 个数，…… 第 `k` 组要放 `k` 个数。  
3. 用回溯（Depth‑First Search）在 `0 … n‑1` 这 `n` 个数字中挑选出每组的成员，**注意同一个组里不能出现相同的数字**，并且在整个递归过程中记录每个数字已经被用了多少次，不能超过 `usageLimits[i]`。  
4. 如果成功构造出所有 `k` 组，就把 `k` 记为可行；继续尝试更大的 `k`。  

> **为什么这个方法能得到正确答案？**  
> 因为它枚举了**所有**合法的分配方式，只要有一种方式能满足要求，就一定会在搜索树的某个叶子节点被找到。  

> **时间/空间复杂度**  
> - 时间：搜索树的分支数是指数级的，最坏情况相当于在每个组里从 `n` 个数字中任选 `size` 个，复杂度大约是 `O(n^{k})`，这里的 `k` 本身也可能是 `O(√S)`（`S` 为所有上限之和），所以整体是**爆炸性的**，在实际数据（`n` 可达 `10^5`）下根本不可跑。  
> - 空间：递归栈最多保存 `k` 层，加上记录每个数字使用次数的数组，需要 `O(n + k)` 的额外空间。  

显然，暴力搜索只能用来验证思路或在极小规模的数据上实验，真正的解法必须把“慢在哪里”找出来并进行优化。

#### 代码（Python）

```python
# 仅用于演示概念，不能通过大数据测试
def brute_max_groups(usageLimits):
    n = len(usageLimits)
    used = [0] * n                     # 记录每个数字已经使用了多少次

    # 深度优先搜索，尝试构造第 cur 组（大小为 cur+1）
    def dfs(cur, target):
        if cur > target:               # 已经成功构造完所有组
            return True
        need = cur                     # 本组需要的元素个数（从 1 开始计数）
        # 选出 need 个不同的数字放进本组
        def pick(start, chosen):
            if len(chosen) == need:    # 本组已经装满
                return dfs(cur + 1, target)
            for i in range(start, n):
                if used[i] < usageLimits[i]:   # 还能再用一次
                    used[i] += 1
                    if pick(i + 1, chosen + [i]):   # 继续往后挑
                        return True
                    used[i] -= 1        # 回溯
            return False
        return pick(0, [])

    # 逐步尝试更大的组数
    k = 0
    while True:
        if not dfs(1, k + 1):          # 尝试 k+1 组
            break
        k += 1
    return k
```

> **代码说明**  
> - `used[i]` 类似于“字典里已经翻到的页码”。  
> - `pick` 函数负责在当前组里挑选不同的数字。  
> - 每一次递归都要检查是否超过 `usageLimits[i]`，确保不违背限制。  

#### 复杂度  

- 时间复杂度：`O(n^{k})`（指数级），在本题规模下不可接受。  
- 空间复杂度：`O(n + k)`，主要是记录使用次数的数组和递归栈。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于枚举每个组的具体成员**。  
其实我们并不需要知道每个组到底装了哪些数字，只要能**保证总的“可用次数”足够填满所有组的槽位**，就一定可以构造出合法的分配。  

关键观察  

1. **每个数字在同一组里最多出现一次**（组内不能有重复），而整个过程最多有 `k` 组，所以数字 `i` 最多能被使用 `min(usageLimits[i], k)` 次。  
2. 若把所有数字可以贡献的使用次数相加，得到  
   \[
   \text{totalAvailable}(k) = \sum_{i=0}^{n-1} \min(\text{usageLimits}[i],\;k)
   \]  
   只要 `totalAvailable(k)` **不小于** 所有组需要的槽位数  
   \[
   \text{need}(k) = 1 + 2 + \dots + k = \frac{k\,(k+1)}{2}
   \]  
   那么就一定可以把数字分配进 `k` 组（可以用贪心把每个数字尽量分配到不同的组里）。  

因此，**判断 `k` 是否可行**可以用上面两条式子直接计算，**不必真的去构造每一组**。  

接下来要找的是最大的 `k`，这正好适合二分搜索（Binary Search）：

- **单调性**：如果 `k` 可行，则所有 `k' < k` 也一定可行（因为需求更少）。  
- **搜索范围**：上界可以取 `sqrt(2 * sum(usageLimits)) + 1`，因为 `k(k+1)/2 ≤ sum(usageLimits)` 必须成立。  

实现步骤  

1. 计算 `total = sum(usageLimits)`。  
2. 设 `lo = 0`，`hi = int((2*total)**0.5) + 2`（安全上界）。  
3. 在 `[lo, hi)` 区间做二分：  
   - 取中点 `mid`，计算 `totalAvailable(mid)`（遍历一次数组，取 `min(limit, mid)` 累加）。  
   - 若 `totalAvailable(mid) >= mid*(mid+1)//2`，说明 `mid` 可行，左移 `lo = mid`；否则 `hi = mid`。  
4. 循环结束时 `lo` 即为最大可行的组数。  

> **为什么只要总可用次数够用就一定能分配？**  
> 想象把每个数字的可用次数视作“球”，每个组的需求视作“盒子”。  
> - 每个盒子需要 `size` 个不同颜色的球。  
> - 因为每种颜色的球最多只有 `k` 个（`k` 是盒子数量），我们可以把每种颜色的球分散到不同的盒子里，**不会出现同一个盒子里放两个相同颜色的球**。  
> - 只要所有球的总数不小于所有盒子容量的总和，就能把球逐盒填满——这正是经典的“把上限截断后求和”技巧。  

#### 代码（Python）

```python
from typing import List

def maxIncreasingGroups(usageLimits: List[int]) -> int:
    """
    返回可以创建的最大组数，使得第 i 组恰好有 i 个不同的数字，
    且每个数字 i 的使用次数不超过 usageLimits[i]。
    """
    total = sum(usageLimits)                       # 所有数字的使用上限之和

    # 二分搜索的上界：k(k+1)/2 <= total => k ≈ sqrt(2*total)
    hi = int((2 * total) ** 0.5) + 2               # +2 防止取整误差
    lo = 0

    # 判定函数：给定 k，检查是否可以完成 k 组
    def feasible(k: int) -> bool:
        need = k * (k + 1) // 2                     # 需要的总槽位数
        # 计算每个数字在 k 组里最多能贡献的次数
        available = 0
        for lim in usageLimits:
            # 如果 lim 大于 k，最多只能在 k 组里各出现一次
            available += lim if lim < k else k
            # 早停：一旦已经够了，就不必继续遍历
            if available >= need:
                return True
        return available >= need

    # 标准的二分（左闭右开区间）
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid          # mid 可行，尝试更大
        else:
            hi = mid          # mid 不可行，缩小上界

    return lo
```

> **代码要点解释**  
> - `total` 相当于“字典的总页数”。  
> - `hi` 的计算利用了 **平方根** 的直观意义：如果你把所有页数均匀分配到递增长度的组里，最多能形成多少组。  
> - `feasible(k)` 中的 `min(lim, k)`（实现方式是 `lim if lim < k else k`）相当于“把每本字典的页数截断到 k”，因为同一本字典在同一组里只能出现一次，最多出现 k 次（一次在每个组）。  
> - 通过提前判断 `available >= need` 可以 **提前退出**，在大多数情况下省去后面的循环，提升常数因子。  

#### 复杂度  

- 时间复杂度：`O(n log K)`，其中 `K` 为答案的上界（约 `sqrt(2 * sum(usageLimits))`），`log K` 大约在 `30` 左右。遍历数组一次的代价是 `O(n)`，二分大约进行 `log K` 次检查。  
- 空间复杂度：`O(1)`（只使用常数级额外变量），不需要额外的数组或递归栈。  

与暴力解相比，**时间从指数级降到了线性乘以对数级**，能够轻松处理 `n = 10^5`、`usageLimits[i]` 达到 `10^9` 的极限数据。

---

## 心得  

- **核心技巧**：把“每个数字在 k 组里最多出现 k 次”这件事抽象为 `min(limit, k)`，然后把整个问题转化为“总可用次数是否能覆盖递增长度的需求”。  
- **适用的题型**  
  1. “把资源分配到递增或固定需求的多个容器”——如 *Maximum Number of Groups With Increasing Length*（本题）  
  2. “在给定上限下，最多可以完成多少轮游戏/任务”，例如 *Maximum Number of Complete Staircases*（LeetCode 1798）  
  3. “求能满足前缀和需求的最大 k”，比如 *Maximum Size Subarray Sum Equals k* 的变形。  
- **一句话总结解题钥匙**：**把每个元素的使用上限截断到目标组数 k，然后比较截断后总和与递增需求的总和**。  

---

## 反思  

- **第一反应**：看到“每个组长度递增”立刻想到要把所有需求相加得到 `k(k+1)/2`，随后考虑如何让数字的使用次数满足这个总量。  
- **最容易踩的坑**  
  - **忽略“同组内不能重复”**：如果把 `usageLimits[i]` 直接相加，会高估可用次数。必须把每个数字的贡献上限截到 `k`。  
  - **二分上界取错**：如果上界太小会错过答案，太大则仍能得到正确结果但可能导致不必要的循环。使用 `sqrt(2*sum)` 是安全且紧凑的上界。  
  - **整数溢出**：`k*(k+1)//2` 在 Python 不会溢出，但在其他语言需要使用 64 位整数。  
- **下次类似题目第一步**：**写出需求的总量公式**（比如前缀和、等差数列求和），**再思考每个资源的最大贡献**（常用 `min(limit, k)`），最后检查两者的大小关系并用二分或贪心验证。