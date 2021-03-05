# #1235. 工作调度的最大利润 / Maximum Profit in Job Scheduling

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-profit-in-job-scheduling/)

---

## 题目（英文原版）

**Description**

We have n jobs, where every job is scheduled to be done from startTime[i] to endTime[i], obtaining a profit of profit[i].
You're given the startTime, endTime and profit arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.
If you choose a job that ends at time X you will be able to start another job that starts at time X.

**Examples**

**Example 1:**

```
Input: startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
Output: 120
Explanation: The subset chosen is the first and fourth job. 
Time range [1-3]+[3-6] , we get profit of 120 = 50 + 70.
```

**Example 2:**

```
Input: startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
Output: 150
Explanation: The subset chosen is the first, fourth and fifth job. 
Profit obtained 150 = 20 + 70 + 60.
```

**Example 3:**

```
Input: startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
Output: 6
```

**Constraints**

- 1 <= startTime.length == endTime.length == profit.length <= 5 * 104
- 1 <= startTime[i] < endTime[i] <= 109
- 1 <= profit[i] <= 104

---

## 题目（中文翻译）

我们有 **n** 个工作，每个工作 **i** 的执行时间为 `startTime[i]` 到 `endTime[i]`，完成后可以获得 `profit[i]` 的收益。  
给定 `startTime`、`endTime` 和 `profit` 三个数组，返回在不选择时间区间重叠的工作集合的前提下，能够获得的最大总收益。  
如果你选择的某个工作在时间 **X** 结束，则可以立即开始另一个在时间 **X** 开始的工作。

### 示例

#### 示例 1
**输入**  
```text
startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
```
**输出**  
```text
120
```
**解释**  
选择第 1 个和第 4 个工作。时间区间 `[1-3] + [3-6]`，总收益为 `120 = 50 + 70`。

#### 示例 2
**输入**  
```text
startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
```
**输出**  
```text
150
```
**解释**  
选择第 1、4、5 个工作。总收益为 `150 = 20 + 70 + 60`。

#### 示例 3
**输入**  
```text
startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
```
**输出**  
```text
6
```

### 约束条件
- `1 <= startTime.length == endTime.length == profit.length <= 5 * 10^4`
- `1 <= startTime[i] < endTime[i] <= 10^9`
- `1 <= profit[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的工作组合**，然后挑出收益最高且不冲突的那一个。  
可以把每一份工作看成一张卡片，**要么选，要么不选**，于是总共有 `2ⁿ` 种选择（`n` 为工作数量）。  
遍历每一种选择，检查其中的工作是否有时间重叠，如果没有冲突，就把它们的 profit 加起来，取最大值。

- **数据结构**：我们只需要用普通的列表保存 `startTime、endTime、profit`，以及一个 `int` 记录当前组合的收益。  
- **正确性**：因为我们把所有可能的组合都尝试了一遍，肯定不会漏掉最优解，所以答案一定是对的。  
- **时间/空间复杂度**：  
  - **时间**：每个工作都有 “选 / 不选” 两种状态，需要遍历 `2ⁿ` 种组合，检查冲突也要遍历最多 `n` 次，所以时间是指数级的，记作 **O(2ⁿ)**。在大白话里，这意味着 **随着工作数量稍微多一点，计算时间就会呈爆炸式增长**，比如 `n=20` 时已经要检查约 `1,048,576` 种组合。  
  - **空间**：只用到保存输入的三个数组和递归栈（深度最多 `n`），所以是 **O(n)**。

> 暴力法在 `n` 很小（比如 `n ≤ 15`）时还能跑，但本题 `n` 可达 `5·10⁴`，显然不可行。

#### 代码（Python）

```python
from typing import List

def jobScheduling_brute(startTime: List[int], endTime: List[int], profit: List[int]) -> int:
    n = len(startTime)
    best = 0                       # 保存全局最大收益

    # 用深度优先搜索枚举所有子集
    def dfs(idx: int, cur_profit: int, last_end: int):
        nonlocal best
        if idx == n:                # 所有工作都已经考虑完
            best = max(best, cur_profit)
            return

        # 1️⃣ 不选第 idx 个工作
        dfs(idx + 1, cur_profit, last_end)

        # 2️⃣ 选第 idx 个工作（前提是时间不冲突）
        if startTime[idx] >= last_end:   # 可以接在上一份工作后面
            dfs(idx + 1,
                cur_profit + profit[idx],
                endTime[idx])

    dfs(0, 0, 0)                     # 从第 0 份工作开始，当前收益 0，上一份工作的结束时间设为 0
    return best
```

#### 复杂度

- **时间复杂度**：`O(2ⁿ)` —— 随着工作数量指数增长，实际运行会在 `n` 较小的情况下才可接受。  
- **空间复杂度**：`O(n)` —— 递归栈的深度最多是 `n`，其余只用常数级额外空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查相同的子问题**。比如，当我们已经决定了前面几份工作的安排后，后面的子问题只和“从第 i 份工作开始往后的最优收益”有关，而与前面已经选了哪些工作无关。于是可以**用动态规划**把这些子问题缓存下来，避免重复计算。

**关键步骤**：

1. **按开始时间排序**  
   把每个工作看成一个三元组 `(start, end, profit)`，按照 `start` 升序排列。这样后面的工作一定 **不早于** 前面的工作，方便后面二分查找。

2. **定义 DP 状态**  
   - `dp[i]` 表示**从第 i 份工作（包括 i）开始往后，能够得到的最大收益**。答案最终是 `dp[0]`（从第一份工作开始的最优值）。  
   - 递推时有两种选择：**不选第 i 份工作** → 收益为 `dp[i+1]`；**选第 i 份工作** → 收益为 `profit[i] + dp[next]`，其中 `next` 是**第一个开始时间 ≥ end[i] 的工作索引**（因为结束时间等于下一个工作的开始时间是允许的）。

3. **二分搜索找到 `next`**  
   排序后，所有 `start` 形成了一个递增数组。我们可以用 Python 标准库 `bisect_left`（相当于 C++ 的 `lower_bound`）在 `O(log n)` 时间内找到 `next`。  
   - 类比：把 `start` 看成一本字典的“词条”，我们要找“第一个词条不早于某个时间 X”，这正是二分查找的典型场景。

4. **自后向前填表**  
   从后往前遍历工作列表，利用已知的 `dp[i+1]` 和 `dp[next]` 计算 `dp[i]`。这样每个状态只算一次，时间是线性加上二分的对数因子。

5. **返回答案**  
   `dp[0]` 即为最大利润。

**为什么正确**  
- DP 的递推式覆盖了所有合法的子集合：不选当前工作 → 所有方案都在 `dp[i+1]` 中；选当前工作 → 必须跳到第一个不冲突的工作 `next`，后面的最优收益就是 `dp[next]`，两者取最大即为从 i 开始的最优。  
- 二分搜索保证我们总是找到了最早可以接的工作，确保不会遗漏合法的接续。

#### 代码（Python）

```python
from typing import List
import bisect

def jobScheduling(startTime: List[int], endTime: List[int], profit: List[int]) -> int:
    # 1️⃣ 把每份工作组织成 (start, end, profit) 的元组并排序
    jobs = sorted(zip(startTime, endTime, profit), key=lambda x: x[0])
    n = len(jobs)

    # 把排序后的开始时间单独抽出来，方便二分查找
    starts = [job[0] for job in jobs]

    # 2️⃣ dp[i] 表示从第 i 份工作开始能够获得的最大利润
    dp = [0] * (n + 1)          # 多一个哨兵位置，dp[n] = 0 表示没有工作时利润为 0

    # 3️⃣ 从后往前遍历
    for i in range(n - 1, -1, -1):
        s, e, p = jobs[i]

        # 用二分找第一个 start >= e 的工作索引
        nxt = bisect.bisect_left(starts, e)

        # 两种选择：不选 / 选
        take = p + dp[nxt]          # 选第 i 份工作后，加上从 nxt 开始的最优利润
        not_take = dp[i + 1]        # 不选第 i 份工作，直接看下一个位置的最优值

        dp[i] = max(take, not_take) # 取两者最大

    return dp[0]                     # 从第 0 份工作开始的最优利润
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `O(n log n)` 来自排序（`n log n`）和每个工作一次二分搜索（`log n`），两者同阶。大白话是：**随着工作数量增长，运行时间大约是工作数的对数倍**，比暴力的指数增长慢得多，几乎可以在 5·10⁴ 条数据下瞬间得到答案。

- **空间复杂度**：`O(n)`  
  - 需要存储排序后的工作列表、`starts` 数组和 `dp` 表，都是线性大小。相较于暴力的递归栈，这里只用了几倍的额外内存，仍然是可接受的。

---

## 心得

- **核心技巧**：**加权区间调度（Weighted Interval Scheduling）**——使用**动态规划 + 二分搜索**求解。  
- **适用场景**（类似题目）：
  1. LeetCode 1235 《Maximum Profit in Job Scheduling》（本题）。  
  2. LeetCode 435 《Non-overlapping Intervals》（只要判断能否安排全部区间，思路相似）。  
  3. 经典的“**活动选择**”或“**会议室安排**”的变形，只是这里每个区间还有收益，需要取最大总收益。  
- **一句话总结解题钥匙**：**把区间按开始时间排好序，利用 DP 把“从这里往后能赚多少钱”记下来，再用二分快速定位下一个不冲突的区间**。

---

## 反思

- **第一反应**：看到“最大利润 + 没有重叠”，立刻想到**枚举所有子集**，因为最直接的思路总是“把所有可能都试一遍”。  
- **最容易踩的坑**：  
  1. **时间边界**——题目说明“结束时间等于下一工作开始时间是允许的”，所以二分要用 `bisect_left`（≥），而不是 `bisect_right`（>）。  
  2. **排序依据**——一定要按 **开始时间** 排序（而不是结束时间），否则二分查找的基准数组就不再单调递增。  
  3. **大数范围**——结束时间可达 `10⁹`，不能用数组下标直接映射时间，需要用二分这种 **对数搜索** 而非线性遍历。  
- **下次遇到同类题**：第一步先**把区间按开始时间排序**，再**思考 DP 状态（从当前位置往后最大收益）**，最后**用二分定位下一个合法区间**。只要抓住这三点，基本都能写出最优解。