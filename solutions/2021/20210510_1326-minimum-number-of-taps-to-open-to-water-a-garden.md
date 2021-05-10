# #1326. 打开最少水龙头以浇灌花园 / Minimum Number of Taps to Open to Water a Garden

> 难度：困难 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/)

---

## 题目（英文原版）

**Description**

There is a one-dimensional garden on the x-axis. The garden starts at the point 0 and ends at the point n. (i.e., the length of the garden is n).
There are n + 1 taps located at points [0, 1, ..., n] in the garden.
Given an integer n and an integer array ranges of length n + 1 where ranges[i] (0-indexed) means the i-th tap can water the area [i - ranges[i], i + ranges[i]] if it was open.
Return the minimum number of taps that should be open to water the whole garden, If the garden cannot be watered return -1.

**Examples**

**Example 1:**

```
Input: n = 5, ranges = [3,4,1,1,0,0]
Output: 1
Explanation: The tap at point 0 can cover the interval [-3,3]
The tap at point 1 can cover the interval [-3,5]
The tap at point 2 can cover the interval [1,3]
The tap at point 3 can cover the interval [2,4]
The tap at point 4 can cover the interval [4,4]
The tap at point 5 can cover the interval [5,5]
Opening Only the second tap will water the whole garden [0,5]
```

**Example 2:**

```
Input: n = 3, ranges = [0,0,0,0]
Output: -1
Explanation: Even if you activate all the four taps you cannot water the whole garden.
```

**Constraints**

- 1 <= n <= 104
- ranges.length == n + 1
- 0 <= ranges[i] <= 100

---

## 题目（中文翻译）

**描述**  
在 x 轴上有一条一维花园（one-dimensional garden），起点为 0，终点为 n（即花园的长度为 n）。  
花园的每个整数坐标点 `[0, 1, ..., n]` 处各有一个水龙头（tap）。  

给定整数 `n` 和长度为 `n + 1` 的整数数组 `ranges`，其中 `ranges[i]`（0 索引）表示第 `i` 个水龙头如果打开，能够浇灌的区间为 `[i - ranges[i], i + ranges[i]]`。  

返回能够浇灌完整个花园所需打开的水龙头的最小数量；如果无法浇灌整个花园，返回 `-1`。

**示例 1**  
```
Input: n = 5, ranges = [3,4,1,1,0,0]
Output: 1
Explanation: 
- 第 0 号水龙头可以覆盖区间 [-3,3]  
- 第 1 号水龙头可以覆盖区间 [-3,5]  
- 第 2 号水龙头可以覆盖区间 [1,3]  
- 第 3 号水龙头可以覆盖区间 [2,4]  
- 第 4 号水龙头可以覆盖区间 [4,4]  
- 第 5 号水龙头可以覆盖区间 [5,5]  

只打开第 1 号水龙头（即第二个水龙头）即可浇灌整个花园。
```

**示例 2**  
```
Input: n = 3, ranges = [0,0,0,0]
Output: -1
Explanation: 即使打开所有四个水龙头，也无法浇灌完整个花园。
```

**约束条件**  

- `1 <= n <= 10^4`  
- `ranges.length == n + 1`  
- `0 <= ranges[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个水龙头能浇到的区间列出来**，然后尝试所有可能的开关组合，看看哪一种能把 `[0, n]` 全部覆盖且用的水龙头最少。  

- **数据结构**：  
  - **区间**：`[left, right]`，左端点是 `i - ranges[i]`，右端点是 `i + ranges[i]`（注意要和 `0`、`n` 做裁剪，防止越界）。  
  - **集合**：把若干区间放进一个列表里，表示当前打开的水龙头集合。  

- **为什么正确**：  
  - 只要把所有可能的打开方式枚举出来，必然能找到最少的那一种（如果有解的话），因为我们没有漏掉任何一种组合。  

- **时间/空间复杂度**：  
  - 枚举所有子集的时间是 `2^(n+1)`，也就是**指数级**，对于 `n` 甚至只有 `10` 都会非常慢。  
  - 空间上只需要存放 `n+1` 个区间和递归栈，都是 **O(n)**，但时间是主要瓶颈。  

> **大白话**：  
> 想象你在挑选水果，盒子里有 `n+1` 个水果，你想挑出最少的水果让盒子里每一寸都被水果占满。暴力解法相当于把所有挑法都列出来检查，水果多了就根本不可能手动完成。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def minTaps_brute(n: int, ranges: List[int]) -> int:
    # 1️⃣ 把每个水龙头的浇水区间算出来，左端点不要小于 0，右端点不要大于 n
    intervals = []
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        right = min(n, i + r)
        intervals.append((left, right))

    # 2️⃣ 枚举开多少个水龙头，从少到多尝试
    for k in range(1, n + 2):                     # 最多打开 n+1 个
        # 取出所有可能的 k 个水龙头组合
        for combo in combinations(range(n + 1), k):
            # 计算这些水龙头能够覆盖的最左和最右点
            cur_left = min(intervals[i][0] for i in combo)
            cur_right = max(intervals[i][1] for i in combo)

            # 只要最左 ≤ 0 且最右 ≥ n，说明区间 [0, n] 被覆盖
            if cur_left <= 0 and cur_right >= n:
                # 但是还要检查中间有没有缺口
                # 把选中的区间按左端点排序
                segs = sorted(intervals[i] for i in combo)
                reach = 0
                ok = True
                for l, r in segs:
                    if l > reach:          # 出现了间隙
                        ok = False
                        break
                    reach = max(reach, r)
                if ok and reach >= n:
                    return k
    return -1    # 没有任何组合能覆盖全园
```

> 关键行解释（中文注释已在代码中）：  
> - `combinations(range(n + 1), k)`：从 `n+1` 个水龙头里挑 `k` 个。  
> - `cur_left <= 0 and cur_right >= n`：快速过滤掉明显不可能覆盖全园的组合。  
> - 排序后逐段检查是否出现 “间隙”——如果左端点比当前已覆盖最右点还大，就说明有未被浇到的地方。

#### 复杂度  

- **时间复杂度**：`O(2^(n+1) * n)`（指数级）。因为我们遍历了所有子集，每个子集里又要遍历选中的水龙头来检查覆盖情况。  
- **空间复杂度**：`O(n)`。只保存了 `n+1` 个区间和递归/迭代时的临时变量。  

> **含义解释**：指数级时间在实际运行时会“炸掉”——即使 `n=20`，`2^21` 已经超过两百万次循环，远远超出 1 秒限制。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“枚举所有子集”**，我们根本不需要把所有组合都试一遍，只要**贪心**地每一步选出“能把右边界推进最远的水龙头”，就能得到最少的水龙头数。  

这其实和 **“区间覆盖”**（最小区间覆盖）或 **“跳跃游戏”** 的思路一模一样：  

1. **把每个水龙头转成区间** `[left, right]`（同上），并把左端点小于 `0` 的改成 `0`，右端点大于 `n` 的改成 `n`。  
2. **把所有区间按左端点从小到大排序**。这一步类似把所有“能从哪里开始浇水”的信息排好队。  
3. 从左到右遍历区间：  
   - 维护两个变量  
     - `cur_end`：已经确定要打开的水龙头能覆盖到的最右位置（相当于我们已经走到的最远点）。  
     - `next_end`：在所有左端点 ≤ `cur_end` 的区间中，能够覆盖到的最右位置（相当于“这一步里我们还能再往前走多远”。）  
   - 当遍历到的区间左端点 **大于** `cur_end` 时，说明**出现了间隙**，无法继续覆盖，直接返回 `-1`。  
   - 每当遍历完所有左端点 ≤ `cur_end`，就把 `cur_end` 更新为 `next_end`，并且计数器 `ans` 加 1，表示我们决定在这一步打开一个水龙头（实际可能是其中覆盖最远的那一个）。  
4. 当 `cur_end` 已经 ≥ `n` 时，说明花园全部被覆盖，返回计数 `ans`。  

> **核心概念解释**  
> - **左端点 ≤ 当前已覆盖最右点**：就像你站在一条路上，手里已经点亮的灯光最远能照到 `cur_end`，只要下一个灯的灯泡（左端点）在这盏灯照到的范围内，你就可以接上去。  
> - **选最右的**：在所有可以接上的灯泡里，挑出照得最远的那盏，因为它能让你一次走得更远，省掉后面可能的多余灯。  

这就是**贪心**：每一步都做局部最优（选最远），全局结果也恰好是最优的。  

#### 代码（Python）

```python
from typing import List

def minTaps_greedy(n: int, ranges: List[int]) -> int:
    """
    贪心求最少打开的水龙头数量
    """
    # 1️⃣ 把每个水龙头转换成区间，并裁剪到 [0, n] 范围
    intervals = []
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        right = min(n, i + r)
        intervals.append((left, right))

    # 2️⃣ 按左端点从小到大排序
    intervals.sort(key=lambda x: x[0])

    ans = 0          # 已经选了多少个水龙头
    cur_end = 0      # 已经覆盖到的最右位置
    i = 0            # 遍历 intervals 的指针
    m = len(intervals)

    while cur_end < n:
        next_end = cur_end   # 在本轮可以进一步扩展到的最右位置

        # 3️⃣ 找所有左端点 ≤ cur_end 的区间，取其中右端点最大的
        while i < m and intervals[i][0] <= cur_end:
            next_end = max(next_end, intervals[i][1])
            i += 1

        # 4️⃣ 如果没有任何区间能让我们前进一步，说明出现了空洞
        if next_end == cur_end:
            return -1

        # 5️⃣ 否则我们选了一个水龙头，覆盖范围扩展到 next_end
        ans += 1
        cur_end = next_end

    return ans
```

> **关键行中文注释**  
> - `intervals.sort(key=lambda x: x[0])`：把所有“能从哪里开始浇水”的信息排好序，方便一次遍历。  
> - `while i < m and intervals[i][0] <= cur_end:`：只看左端点在已覆盖范围内的水龙头。  
> - `next_end = max(next_end, intervals[i][1])`：记录这些水龙头中最能往右浇的那个。  
> - `if next_end == cur_end:`：如果连一步都走不动，说明中间有缺口，直接返回 `-1`。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 生成区间是 `O(n)`。  
  - 排序需要 `O(n log n)`（`log n` 来自比较排序）。  
  - 线性遍历一次区间，`O(n)`。  
  - 整体 dominated（主导）by 排序，故为 `O(n log n)`。  

- **空间复杂度**：`O(n)`  
  - 需要存放 `n+1` 个区间的列表。  
  - 其余变量都是常数级别。  

> **含义解释**：`O(n log n)` 大约是“线性时间乘一个很小的系数”。对 `n=10^4` 完全可以在毫秒级完成。相比指数级的暴力解，提升了 **几万倍** 甚至 **上亿倍**。

---

## 心得  

- **核心技巧**：把每个水龙头看成一个**区间**，然后使用**贪心的最右覆盖**（类似跳跃游戏、最小区间覆盖）求最少区间数。  
- **适用的题型**  
  1. **Jump Game II**（最少跳跃次数）  
  2. **Minimum Number of Intervals to Cover a Range**（区间覆盖）  
  3. **Video Stitching**（合并视频片段覆盖全时长）  
- **一句话总结解题钥匙**：**每次都选左端点已被覆盖且右端点最远的水龙头**，如此即可最少开启次数完成全园浇水。

---

## 反思  

- **第一反应**：把每个水龙头的浇水范围算出来，然后尝试所有组合（暴力枚举）。  
- **最容易踩的坑**  
  - **区间裁剪**：左端点不能小于 `0`，右端点不能大于 `n`，否则会出现负数或超出花园的假区间。  
  - **出现间隙**：在贪心遍历时，如果当前已覆盖最右点 `cur_end` 没有任何区间可以进一步延伸，就必须立刻返回 `-1`。  
  - **边界情况**：`n=0`（花园长度为 0）时应返回 `0`，因为根本不需要打开任何水龙头。  
- **下次遇到同类题**：第一步先 **把所有“可操作的对象”转成区间**，再判断是否能 **从左到右无缝覆盖**，并在遍历时 **始终记录可达最远点**。这样就能快速判断可行性并得到最优解。