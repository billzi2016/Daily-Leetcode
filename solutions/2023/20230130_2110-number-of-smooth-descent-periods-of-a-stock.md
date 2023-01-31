# #2110. 股票平滑下降期间的数量 / Number of Smooth Descent Periods of a Stock

> 难度：中等 · 标签：Array、Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/)

---

## 题目（英文原版）

**Description**

You are given an integer array prices representing the daily price history of a stock, where prices[i] is the stock price on the ith day.
A smooth descent period of a stock consists of one or more contiguous days such that the price on each day is lower than the price on the preceding day by exactly 1. The first day of the period is exempted from this rule.
Return the number of smooth descent periods.

**Examples**

**Example 1:**

```
Input: prices = [3,2,1,4]
Output: 7
Explanation: There are 7 smooth descent periods:
[3], [2], [1], [4], [3,2], [2,1], and [3,2,1]
Note that a period with one day is a smooth descent period by the definition.
```

**Example 2:**

```
Input: prices = [8,6,7,7]
Output: 4
Explanation: There are 4 smooth descent periods: [8], [6], [7], and [7]
Note that [8,6] is not a smooth descent period as 8 - 6 ≠ 1.
```

**Example 3:**

```
Input: prices = [1]
Output: 1
Explanation: There is 1 smooth descent period: [1]
```

**Constraints**

- 1 <= prices.length <= 105
- 1 <= prices[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `prices`，表示某只股票的每日价格历史，其中 `prices[i]` 是第 `i` 天的股票价格。  
**平滑下降期间**（smooth descent period）指的是由一个或多个连续天数（contiguous days）组成的区间，且该期间内每一天的价格比前一天的价格恰好低 1。期间的第一天不受此规则约束。  

返回平滑下降期间的总数。

**示例 1**  
**输入**: `prices = [3,2,1,4]`  
**输出**: `7`  
**解释**: 存在 7 个平滑下降期间：  
`[3]`, `[2]`, `[1]`, `[4]`, `[3,2]`, `[2,1]`, `[3,2,1]`  
注意，单天的区间也算作平滑下降期间。

**示例 2**  
**输入**: `prices = [8,6,7,7]`  
**输出**: `4`  
**解释**: 存在 4 个平滑下降期间：`[8]`, `[6]`, `[7]`, `[7]`  
`[8,6]` 不满足平滑下降期间的条件，因为 `8 - 6 ≠ 1`。

**示例 3**  
**输入**: `prices = [1]`  
**输出**: `1`  
**解释**: 仅有 1 个平滑下降期间：`[1]`

**约束条件**  
- `1 <= prices.length <= 10^5`  
- `1 <= prices[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的连续子数组**，然后检查它们是否满足「相邻两天的价格恰好下降 1」的条件。  

- **枚举子数组**：可以用两层循环，外层固定子数组的左端点 `i`，内层把右端点 `j` 从 `i` 往后移动。  
- **检查条件**：遍历子数组 `prices[i…j]`，只要发现有任意相邻两天的差不是 `1`，就立刻认定这不是平滑下降期。  
- **计数**：只要子数组通过检查，就把答案 `ans` 加 `1`。

> **类比**：把数组想象成一本书的章节目录，暴力解就是把每一页（左端点）当作起点，然后把后面的每一页（右端点）依次翻过去，看看这段文字是否满足「每句话都比前一句少 1 个字」的规则。

这个方法一定能得到正确答案，因为我们把**所有**可能的连续区间都检查了一遍。  

#### 代码（Python）

```python
def countSmoothDescentPeriods_bruteforce(prices):
    n = len(prices)
    ans = 0                     # 最终计数

    # 枚举左端点 i
    for i in range(n):
        # 只要左端点不变，右端点往右扩展
        for j in range(i, n):
            ok = True           # 标记子数组 [i, j] 是否满足条件
            # 检查子数组内部的相邻差是否都是 1
            for k in range(i + 1, j + 1):
                if prices[k - 1] - prices[k] != 1:
                    ok = False
                    break      # 只要有一次不满足，就可以提前结束
            if ok:
                ans += 1        # 统计一个合法的平滑下降期

    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n³)`  
  - 外层两层循环分别是 `O(n)`，内部再遍历一次子数组检查差值，也是 `O(n)`，最坏情况会出现 `n·n·n` 次操作。  
  - **大白话**：如果数组有 1000 天，暴力解大约要跑 10⁹ 次小判断，几乎不可能在合理时间内完成。  

- **空间复杂度：** `O(1)`  
  - 只用了常数个额外变量，和数组长度无关。

---

### 2. 最优解  

#### 思路  

从暴力解出发，**慢的根源在于重复检查相同的子区间**。  
实际上，**只要我们知道每段最长的平滑下降序列的长度 `k`，就能直接算出这段里所有合法子区间的个数**，不必逐个枚举。

**关键观察**  
- 任意一个满足条件的区间，都可以拆成若干**最长的**平滑下降段。例如  
  `prices = [5, 4, 3, 8, 7, 6, 6]` → `[5,4,3]` + `[8,7,6]` + `[6]`。  
- 对于长度为 `k` 的最长段，内部所有合法子区间的个数等于  
  `1 + 2 + … + k = k·(k+1)/2`（等差数列求和公式）。  
  > **类比**：把这段看成一排连续的积木块，任取左端点后，右端点只能向右延伸，形成的子区间数就是「1块的区间、2块的区间、…、k块的区间」的总和。

**线性遍历实现**  
- 用一个指针 `i` 从左到右扫描数组，维护当前平滑下降段的长度 `cur_len`（至少为 1，因为单独一天也是合法的）。  
- 当 `prices[i] - prices[i+1] == 1` 时，说明可以继续往右扩展，`cur_len += 1`。  
- 否则，当前段结束，使用公式把 `cur_len` 转化为子区间数量累加到答案中，然后把 `cur_len` 重置为 1（从下一个元素重新开始）。  
- 循环结束后别忘了把最后一段的贡献也加上。

**双指针视角**  
- `left` 指向当前段的起始位置，`right` 向右移动，只要满足「前一天 - 当天 = 1」就继续；不满足时，用 `right-left+1` 计算长度 `k`，累加 `k·(k+1)//2`，再把 `left` 移到 `right`，继续向前。

整个过程只遍历一次数组，**时间 O(n)**，空间 `O(1)`。

#### 代码（Python）

```python
def countSmoothDescentPeriods(prices):
    """
    线性遍历，统计每个最长平滑下降段的长度，
    用等差数列求和公式把该段内部所有合法子区间计数。
    """
    n = len(prices)
    ans = 0          # 最终答案
    cur_len = 1      # 当前段的长度，最少为 1（单独一天）

    for i in range(1, n):
        # 判断是否还能继续向右扩展当前段
        if prices[i - 1] - prices[i] == 1:   # 前一天比今天高恰好 1
            cur_len += 1                     # 段长度加一
        else:
            # 当前段结束，累计贡献
            ans += cur_len * (cur_len + 1) // 2
            cur_len = 1                      # 重新从当前元素开始计数

    # 循环结束后，最后一段可能还未计入
    ans += cur_len * (cur_len + 1) // 2
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次数组，`n` 是天数。  
  - **大白话**：如果有 100 000 天，只需要 100 000 次简单比较和加法，几乎是瞬间完成。  

- **空间复杂度：** `O(1)`  
  - 只用了几个整数变量，和 `n` 大小无关。

---

## 心得  

- **核心技巧**：把「满足某种递推关系的子数组」划分为**最长连续段**，再利用**等差数列求和**快速计数。  
- **适用场景**：  
  1. **连续递增/递减子数组计数**（如「连续递增子数组的数量」）。  
  2. **满足固定差值的子数组**（如本题的差值恰为 1）。  
  3. **相等子数组计数**（如「相同元素连续子数组的数量」）。  
- **一句话总结**：先把数组切成「最长合法段」，每段内部的合法子区间数等价于「1 + 2 + … + 段长」。

---

## 反思  

- **第一反应**：看到「连续下降且差值为 1」的描述，我立刻想到**枚举子数组**，因为这是最安全的暴力思路。  
- **最容易踩的坑**：  
  - 忘记把**单独一天**算作合法区间，导致答案少 `n`。  
  - 在累加时使用整数除法出错（应使用 `//` 保证整数结果）。  
  - 结束循环后没有把**最后一段**的贡献加入答案。  
- **下次类似题的第一步**：先**找出最长满足条件的连续段**（可以用两指针或一次遍历），再**用数学公式**把段内部所有子区间计数，而不是逐个枚举。