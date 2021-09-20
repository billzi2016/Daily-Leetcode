# #1482. **制作 m 束花所需的最少天数** / Minimum Number of Days to Make m Bouquets

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/)

---

## 题目（英文原版）

**Description**

You are given an integer array bloomDay, an integer m and an integer k.
You want to make m bouquets. To make a bouquet, you need to use k adjacent flowers from the garden.
The garden consists of n flowers, the ith flower will bloom in the bloomDay[i] and then can be used in exactly one bouquet.
Return the minimum number of days you need to wait to be able to make m bouquets from the garden. If it is impossible to make m bouquets return -1.

**Examples**

**Example 1:**

```
Input: bloomDay = [1,10,3,10,2], m = 3, k = 1
Output: 3
Explanation: Let us see what happened in the first three days. x means flower bloomed and _ means flower did not bloom in the garden.
We need 3 bouquets each should contain 1 flower.
After day 1: [x, _, _, _, _]   // we can only make one bouquet.
After day 2: [x, _, _, _, x]   // we can only make two bouquets.
After day 3: [x, _, x, _, x]   // we can make 3 bouquets. The answer is 3.
```

**Example 2:**

```
Input: bloomDay = [1,10,3,10,2], m = 3, k = 2
Output: -1
Explanation: We need 3 bouquets each has 2 flowers, that means we need 6 flowers. We only have 5 flowers so it is impossible to get the needed bouquets and we return -1.
```

**Example 3:**

```
Input: bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3
Output: 12
Explanation: We need 2 bouquets each should have 3 flowers.
Here is the garden after the 7 and 12 days:
After day 7: [x, x, x, x, _, x, x]
We can make one bouquet of the first three flowers that bloomed. We cannot make another bouquet from the last three flowers that bloomed because they are not adjacent.
After day 12: [x, x, x, x, x, x, x]
It is obvious that we can make two bouquets in different ways.
```

**Constraints**

- bloomDay.length == n
- 1 <= n <= 105
- 1 <= bloomDay[i] <= 109
- 1 <= m <= 106
- 1 <= k <= n

---

## 题目（中文翻译）

给定一个整数数组 `bloomDay`、一个整数 `m` 和一个整数 `k`。  
你想要制作 `m` 束花（bouquets）。制作一束花需要使用花园中 **相邻**（adjacent）`k` 朵花。  
花园中共有 `n` 朵花，第 `i` 朵花会在第 `bloomDay[i]` 天开放，开放后只能用于 **恰好一束**（exactly one bouquet）。  

返回能够从花园中制作 `m` 束花所需等待的 **最少天数**（minimum number of days）。如果无法制作 `m` 束花，返回 `-1`。

---

### 示例

#### 示例 1
```text
Input: bloomDay = [1,10,3,10,2], m = 3, k = 1
Output: 3
Explanation: 观察前三天的情况。`x` 表示该位置的花已经开放，`_` 表示未开放。
我们需要 3 束花，每束包含 1 朵花。
- 第 1 天后: [x, _, _, _, _]   // 只能制作一束
- 第 2 天后: [x, _, _, _, x]   // 只能制作两束
- 第 3 天后: [x, _, x, _, x]   // 可以制作三束
```

#### 示例 2
```text
Input: bloomDay = [1,10,3,10,2], m = 3, k = 2
Output: -1
Explanation: 我们需要 3 束花，每束包含 2 朵花，也即需要 6 朵花。但花园中只有 5 朵花，无法满足要求，返回 -1。
```

#### 示例 3
```text
Input: bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3
Output: 12
Explanation: 我们需要 2 束花，每束包含 3 朵花。
以下是第 7 天和第 12 天的花园状态：
- 第 7 天后: [x, x, x, x, _, x, x]
  可以用前面连续的三朵花组成一束，但后面三朵花并非相邻，无法组成第二束。
- 第 12 天后: [x, x, x, x, x, x, x]
  此时可以组成两束相邻的三朵花。
```

---

### 约束条件

- `bloomDay.length == n`
- `1 <= n <= 10^5`
- `1 <= bloomDay[i] <= 10^9`
- `1 <= m <= 10^6`
- `1 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**模拟每一天**，把已经绽放的花标记出来，然后在这一天里遍历一遍数组，统计能够组成多少个满足「`k` 朵相邻」的花束。  
- **数据结构**：我们只需要一个长度为 `n` 的布尔数组 `bloomed`（或者直接在原数组上比较），用来记录第 `i` 朵花在当前天数是否已经开放。把它想象成花园里的灯，亮了就说明那朵花已经可以用。  
- **为什么正确**：因为我们逐天检查，必然会在第一个可以完成 `m` 朵花束的天数停下来，这就是答案。  

**步骤**  
1. 从第 `1` 天开始，一天一天往后走。  
2. 对每一天 `day`，遍历 `bloomDay`，把 `bloomDay[i] ≤ day` 的位置视为已开放。  
3. 再遍历一次，用一个计数器 `cnt` 记录当前连续已开放的花的数量；当 `cnt == k` 时，说明得到一束花，`cnt` 归零，花束计数 `bouquets++`。  
4. 如果 `bouquets >= m`，返回当前的 `day`。  
5. 若遍历完所有可能的天数仍未满足，则返回 `-1`（其实在实际实现里我们可以直接在第一步判断 `n < m*k`，如果不够花直接返回 `-1`）。

#### 代码（Python）  

```python
def minDays_bruteforce(bloomDay, m, k):
    n = len(bloomDay)
    # 先排除根本不可能的情况
    if n < m * k:
        return -1

    # 最多需要等到所有花都开完的那一天
    max_day = max(bloomDay)

    for day in range(1, max_day + 1):          # 逐天尝试
        bouquets = 0          # 已经凑好的花束数
        consecutive = 0       # 当前连续开放的花的计数

        for d in bloomDay:
            if d <= day:               # 这朵花已经开放
                consecutive += 1
                if consecutive == k:   # 满足一束
                    bouquets += 1
                    consecutive = 0   # 重置，继续找下一束
            else:
                consecutive = 0       # 不相邻，计数清零

        if bouquets >= m:              # 已经可以凑够 m 束
            return day

    return -1   # 理论上走不到这里，因为 max_day 已经包含所有可能
```

> 关键行的中文注释已经写在代码里，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(max(bloomDay) * n)`。  
  - `max(bloomDay)` 代表最坏情况下我们要检查的天数（可能高达 `10^9`），每一天都要遍历一次长度为 `n`（最多 `10^5`）的数组。  
  - 用大白话说，就是“每天都要走遍整个花园”，如果天数很大，这个办法会非常慢。  

- **空间复杂度**：`O(1)`（不计输入数组本身），只用了几个计数变量。  

---

### 2. 最优解  

#### 思路  

**观察**：  
- 如果在第 `x` 天我们已经可以凑出 `m` 束花，那么在第 `y (y > x)` 天一定也可以。因为天数只会让更多的花开放，已经满足的相邻块不会消失。  
- 这说明“能否在 `day` 天完成”是一个 **单调不降** 的函数：从“不可能”到“可能”只会改变一次。  

**利用单调性**：  
- 对于单调函数，**二分搜索**是找最小满足条件的 `day` 的理想工具。我们把搜索范围设在 `[min(bloomDay), max(bloomDay)]`。  

**核心子问题**：  
- 给定一个具体的天数 `mid`，我们要快速判断 **是否可以凑到至少 `m` 束**。  
- 这一步可以用 **一次线性扫描**完成：遍历 `bloomDay`，把 `bloomDay[i] ≤ mid` 的位置视为已开放，累计连续已开放的花的数量 `cnt`，每当 `cnt == k` 时凑成一束，计数 `bouquets++`，并把 `cnt` 归零。整个过程和暴力解里“检查一天是否可行”的部分相同，只是这里的 `mid` 是二分搜索得到的候选天数。  

**步骤**  

1. **预检查**：如果 `n < m * k`（花的总数不足），直接返回 `-1`。  
2. 初始化二分搜索区间：`left = min(bloomDay)`, `right = max(bloomDay)`。  
3. 循环 `while left < right`：  
   - `mid = (left + right) // 2`。  
   - 调用 `canMake(mid)`（线性扫描）判断是否能凑够 `m` 束。  
   - 若能凑够，则说明答案不大于 `mid`，把 `right = mid`（继续向左找更小的可能）。  
   - 否则答案一定大于 `mid`，把 `left = mid + 1`。  
4. 循环结束时 `left == right`，即为最小满足条件的天数。返回 `left`。  

**为什么是最优**  
- 二分搜索把天数的搜索空间从可能的最大值（最高开花天）压缩到 **对数级**，即 `log(maxDay - minDay)` 次迭代。  
- 每次迭代只需要一次 `O(n)` 的线性扫描，整体时间复杂度为 `O(n log D)`，其中 `D = max(bloomDay) - min(bloomDay)`。对 `n ≤ 10^5`、`D ≤ 10^9` 来说，这已经非常快。  

#### 代码（Python）  

```python
def minDays(bloomDay, m, k):
    """
    返回能够凑成 m 束、每束 k 朵相邻花的最少天数；若不可能返回 -1
    """
    n = len(bloomDay)

    # 预检查：花不够用直接返回 -1
    if n < m * k:
        return -1

    # 辅助函数：判断在 given_day 天是否能凑到 >= m 束
    def can_make(given_day: int) -> bool:
        bouquets = 0          # 已经凑好的花束数
        consecutive = 0       # 当前连续已开放的花的计数

        for d in bloomDay:
            if d <= given_day:          # 这朵花已经开放
                consecutive += 1
                if consecutive == k:   # 达到 k 朵，凑成一束
                    bouquets += 1
                    consecutive = 0    # 重置，继续寻找下一束
                    if bouquets >= m:  # 提前结束，省时间
                        return True
            else:
                consecutive = 0        # 断开，计数清零
        return False

    left, right = min(bloomDay), max(bloomDay)

    # 二分搜索最小的满足条件的天数
    while left < right:
        mid = (left + right) // 2
        if can_make(mid):
            right = mid          # 可能更小，向左收敛
        else:
            left = mid + 1       # 必须更大，向右收敛

    return left  # 此时 left == right，即为答案
```

> 代码里每一步都有中文注释，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n log D)`，其中 `D = max(bloomDay) - min(bloomDay)`。  
  - 解释：二分搜索需要 `log D` 次迭代，每次迭代我们遍历一次长度为 `n` 的数组进行检查。对比暴力解的 `O(maxDay * n)`，我们把“每天”改成了“对数天”，速度提升了好几个数量级。  

- **空间复杂度**：`O(1)`（只使用了常数个额外变量），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**单调性 + 二分搜索**。先把“能否完成”抽象成一个单调判断函数，再用二分在天数空间里快速定位最小可行值。  
- **适用的题型**：  
  1. “最小/最大满足条件的数值” 类问题，如 *Minimum Size Subarray Sum*、*Capacity To Ship Packages Within D Days*。  
  2. “在某个阈值下能否完成任务” 的判断，如 *Find the Minimum Time to Complete All Jobs*、*Split Array Largest Sum*。  
- **一句话总结解题钥匙**：**把“是否可行”变成一个可以 O(n) 检查的单调函数，然后二分定位最小满足的阈值**。

---

## 反思  

- **第一反应**：直接模拟每一天，想要一步步看到花开过程。虽然思路简单，但忽视了天数上限可能非常大。  
- **最容易踩的坑**：  
  - **边界条件**：`n < m * k` 时直接返回 `-1`，否则二分会永远找不到答案。  
  - **计数归零的时机**：在凑成一束后必须把 `consecutive` 归零，否则会把同一朵花计入多束。  
  - **二分终止条件**：使用 `while left < right` 并在找到可行 `mid` 时把 `right = mid`（而不是 `mid - 1`），防止遗漏最小可行值。  
- **下次类似题的第一步**：先判断是否存在**单调性**（随阈值增大，满足条件的可能性只增不减），如果有，就立刻想到 **二分搜索 + O(一次线性检查)** 的框架。