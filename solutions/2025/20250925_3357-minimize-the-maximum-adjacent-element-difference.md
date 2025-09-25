# #3357. 最小化相邻元素的最大差值 / Minimize the Maximum Adjacent Element Difference

> 难度：困难 · 标签：Array、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimize-the-maximum-adjacent-element-difference/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums. Some values in nums are missing and are denoted by -1.
You must choose a pair of positive integers (x, y) exactly once and replace each missing element with either x or y.
You need to minimize the maximum absolute difference between adjacent elements of nums after replacements.
Return the minimum possible difference.

**Examples**

**Example 1:**

```
Input: nums = [1,2,-1,10,8]
Output: 4
Explanation:
By choosing the pair as (6, 7) , nums can be changed to [1, 2, 6, 10, 8] .
The absolute differences between adjacent elements are:
```

**Example 2:**

```
Input: nums = [-1,-1,-1]
Output: 0
Explanation:
By choosing the pair as (4, 4) , nums can be changed to [4, 4, 4] .
```

**Example 3:**

```
Input: nums = [-1,10,-1,8]
Output: 1
Explanation:
By choosing the pair as (11, 9) , nums can be changed to [11, 10, 9, 8] .
```

**Constraints**

- 2 <= nums.length <= 105
- nums[i] is either -1 or in the range [1, 109].

---

## 题目（中文翻译）

给定一个整数数组 `nums`。数组中某些位置的值缺失，用 `-1` 表示。  
你必须恰好选择一对正整数（pair of positive integers）`(x, y)`，并将每个缺失的元素替换为 `x` 或 `y` 中的任意一个。  
替换完成后，需要使 **相邻元素（adjacent elements）** 之间的 **绝对差值（absolute difference）** 的最大值最小化。  
返回能够得到的最小可能的最大差值。

**示例 1**  
输入: `nums = [1,2,-1,10,8]`  
输出: `4`  
解释：  
选择的正整数对为 `(6, 7)`，则数组可以变为 `[1, 2, 6, 10, 8]`。  
相邻元素之间的绝对差值为：

**示例 2**  
输入: `nums = [-1,-1,-1]`  
输出: `0`  
解释：  
选择的正整数对为 `(4, 4)`，则数组可以变为 `[4, 4, 4]`。此时所有相邻元素的绝对差值均为 `0`。

**示例 3**  
输入: `nums = [-1,10,-1,8]`  
输出: `1`  
解释：  
选择的正整数对为 `(11, 9)`，则数组可以变为 `[11, 10, 9, 8]`。相邻元素之间的最大绝对差值为 `1`。

**约束条件**  
- `2 <= nums.length <= 10^5`  
- `nums[i]` 要么是 `-1`，要么在区间 `[1, 10^9]` 内。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的正整数对 (x, y)**，把数组里每个 `-1` 替换成 `x` 或 `y`（两者任选），然后计算替换后相邻元素的绝对差的最大值，最后把所有尝试得到的最大值取最小。

- **数据结构**：只需要遍历一次数组，用两个变量记录当前的最大差值。这里不需要特殊的数据结构，**数组本身就像一本书**，我们把指针从左往右搬过去，顺手算出相邻两页的差。
- **为什么正确**：因为我们把 **所有可能的 (x, y)** 都尝试了一遍，必然能找到使最大差值最小的那一对。
- **时间/空间复杂度**：  
  - 假设我们把 `x`、`y` 的取值范围限定在 `1 … M`（`M` 可能是 `10^9`），那么所有可能的组合数是 `M²`。每一种组合都要遍历整个数组（长度 `n`），所以总时间是 **O(M²·n)**。  
  - 这里的 `O` 符号可以想象成 “**乘法的层数**”。如果 `M = 10⁹`，`M²` 就是 **一万亿**，显然不可接受。  
  - 空间只用了常数个变量，**O(1)**。

> **小结**：暴力解思路很清晰，但因为搜索空间太大，实际运行会超时。

#### 代码（Python）

```python
def min_max_adjacent_diff_bruteforce(nums):
    # 这里仅作演示，实际不可能遍历到 1e9 的范围
    INF = 10 ** 9
    best = INF

    for x in range(1, INF + 1):
        for y in range(1, INF + 1):
            # 用 x / y 替换 -1，随便选哪个都行
            prev = None          # 前一个已确定的数
            cur_max = 0          # 当前方案的最大相邻差
            for v in nums:
                if v == -1:
                    v = x  # 为了演示，直接固定为 x（实际要遍历两种选择）
                if prev is not None:
                    cur_max = max(cur_max, abs(v - prev))
                prev = v
            best = min(best, cur_max)
    return best
```

> 代码中每一行都有中文注释，帮助你快速定位关键操作。但请记住，这段代码在真实数据上根本跑不完。

#### 复杂度

- **时间复杂度**：`O(M²·n)` —— 需要遍历所有可能的 `(x, y)`（`M` 可能高达 `10⁹`），每次都要遍历数组 `n` 次。  
  > 用生活化的说法，就是“先把所有可能的钥匙（M² 把）都试一遍，每把钥匙都要打开整条走廊（n）”。显然不切实际。
- **空间复杂度**：`O(1)` —— 只用了几个计数器。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈**在于我们把所有可能的 `(x, y)` 都枚举。实际上，**只要关心 `-1` 两侧的已有数字**，就能直接算出最优答案，根本不需要遍历 `x`、`y`。

**关键观察 1**：  
相邻的两个已知（非 `-1`）数字之间的差是 **固定的**，它们不受我们如何填 `-1` 影响。记这个最大固定差为 `max_fixed`。答案一定要 **不小于** `max_fixed`。

**关键观察 2**：  
只要把 `-1` 看成“被两侧已知数字包围的空位”。每个 `-1` 左右最多各有一个已知数字（如果左边是 `-1`，继续往左找直到遇到非 `-1`，同理右边）。把所有这些已知数字收集起来，记为集合 `S`。  
- 如果 `S` 为空，说明数组全是 `-1`，我们可以把所有位置都填成同一个数，最大相邻差为 `0`。  
- 否则，`S` 中的最小值记为 `mn`，最大值记为 `mx`。我们只需要让填进去的两个数 `x`、`y` **尽可能靠中间**，这样它们与 `mn`、`mx` 的差都最小。

**关键观察 3**（数学化）：  
把 `x`、`y` 选在区间 `[mn, mx]` 的中点处，最坏的差值就是 `ceil((mx - mn) / 2)`。  
- 设 `mid = (mn + mx) // 2`，取 `x = mid`，`y = mid + 1`（如果 `mx - mn` 为奇数）。  
- 任意一个已知数字 `v ∈ S` 与最近的填充值的差 ≤ `ceil((mx - mn)/2)`。  

于是**答案**为两者的最大值：

```
ans = max( max_fixed , ceil((mx - mn) / 2) )
```

其中 `ceil(a / 2)` 在整数下可以写成 `(a + 1) // 2`。

**为什么不需要更复杂的二分搜索？**  
因为上面的推导已经把最优 `x、y` 用数学式子锁定了，直接算出答案即可。二分搜索只是一种通用的“判断 d 是否可行”的思路，但这里我们已经找到了闭式解。

**类比帮助理解**：  
把已知数字看成 **墙**，`-1` 看成 **空洞**。我们要在墙之间放两块 **砖**（`x`、`y`），使得从墙到砖的距离尽可能小。把砖放在墙的中点，自然可以把最远的距离压到最小。

#### 代码（Python）

```python
def minimize_max_adjacent_difference(nums):
    """
    返回在一次性选定正整数 (x, y) 并把所有 -1 替换为 x 或 y 后，
    相邻元素的最大绝对差的最小可能值。
    """
    n = len(nums)

    # 1️⃣ 计算相邻已知数字之间的最大差值（不受 -1 影响）
    max_fixed = 0
    for i in range(n - 1):
        if nums[i] != -1 and nums[i + 1] != -1:
            max_fixed = max(max_fixed, abs(nums[i] - nums[i + 1]))

    # 2️⃣ 收集所有与 -1 相邻的已知数字
    neighbours = []          # 类似 “墙” 的位置
    for i, v in enumerate(nums):
        if v == -1:
            # 左侧最近的已知数字
            if i > 0 and nums[i - 1] != -1:
                neighbours.append(nums[i - 1])
            # 右侧最近的已知数字
            if i + 1 < n and nums[i + 1] != -1:
                neighbours.append(nums[i + 1])

    # 3️⃣ 特殊情况：全是 -1
    if not neighbours:               # 没有任何墙
        return 0                      # 全部填同一个数即可，最大差为 0

    mn = min(neighbours)             # 最左侧的墙
    mx = max(neighbours)             # 最右侧的墙

    # 4️⃣ 计算 “砖” 与墙之间的最坏距离
    #   ceil((mx - mn) / 2) 用整数实现为 (mx - mn + 1) // 2
    d = (mx - mn + 1) // 2

    # 5️⃣ 最终答案是两部分的较大者
    return max(max_fixed, d)
```

**代码要点**：

- 第 1 步遍历一次数组，找出所有 **已知‑已知** 的相邻对，记录它们的最大差 `max_fixed`。这一步相当于 “先把已经确定的墙之间的距离算出来”。
- 第 2 步只看 `-1` 两边的数，收集进 `neighbours`。这一步相当于 “把所有和空洞相连的墙挑出来”。
- 第 3 步处理全是 `-1` 的极端情况。
- 第 4 步用公式直接得到最小可能的最大差 `d`。
- 第 5 步取两者的最大值即为答案。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历数组两遍（一次找固定差，一次收集相邻已知数），每一步都是线性操作。  
  > 用生活化的说法：**只要走一遍走廊**，不需要尝试成千上万把钥匙。
- **空间复杂度**：`O(1)` —— 只用了几个整数变量（`max_fixed`, `mn`, `mx`），不随 `n` 增长。  
  > 就像我们只在口袋里放了几把钥匙，而不是把整条走廊的地图全部带走。

---

## 心得

- **核心技巧**：  
  把问题转化为“已知数字之间的固定差”和“被 `-1` 包围的邻接数字的范围”。利用**区间中点**的思想直接得到最小可能的最大相邻差。
- **适用的题型**  
  1. “把缺失值用最多两种数填充，使相邻差最小”类问题（如 LeetCode 2678）。  
  2. “在数组中插入数，使最大相邻差最小”类（如 “Make Array Non-decreasing” 的变体）。  
  3. “仅允许两种颜色涂抹缺失位置，要求相邻颜色差最小”的离散数学模型。
- **一句话总结**：**只关注 `-1` 两侧的已知数，用它们的最小/最大值决定填充值的区间，中点即是最优选择**。

---

## 反思

- **第一反应**：看到 `-1`，立刻想到“枚举所有可能的填充值”。这会把搜索空间推向天际，导致超时。
- **最容易踩的坑**  
  - 忽略全是 `-1` 的情况，直接返回 `0`。  
  - 只统计左侧或右侧的邻接数而漏掉另一侧，导致 `mn`、`mx` 计算不完整。  
  - 在计算 `ceil((mx-mn)/2)` 时忘记加 `1`，使用错误的向下取整导致答案偏小。
- **下次遇到同类题**：第一步 **先把所有已知数字之间的固定差算出来**，再 **收集所有与缺失位置相邻的已知数**，利用区间中点求最坏距离，最后取两者的最大值。这样就能在一次线性扫描内得到答案。