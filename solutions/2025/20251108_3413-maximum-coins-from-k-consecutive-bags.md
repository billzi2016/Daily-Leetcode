# #3413. 从 K 连续袋子中的最大硬币数 / Maximum Coins From K Consecutive Bags

> 难度：中等 · 标签：Array、Binary Search、Greedy、Sliding Window、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-coins-from-k-consecutive-bags/)

---

## 题目（英文原版）

**Description**

There are an infinite amount of bags on a number line, one bag for each coordinate. Some of these bags contain coins.
You are given a 2D array coins, where coins[i] = [li, ri, ci] denotes that every bag from li to ri contains ci coins.
The segments that coins contain are non-overlapping.
You are also given an integer k.
Return the maximum amount of coins you can obtain by collecting k consecutive bags.

**Examples**

**Example 1:**

```
Input: coins = [[8,10,1],[1,3,2],[5,6,4]], k = 4
Output: 10
Explanation:
Selecting bags at positions [3, 4, 5, 6] gives the maximum number of coins: 2 + 0 + 4 + 4 = 10 .
```

**Example 2:**

```
Input: coins = [[1,10,3]], k = 2
Output: 6
Explanation:
Selecting bags at positions [1, 2] gives the maximum number of coins: 3 + 3 = 6 .
```

**Constraints**

- 1 <= coins.length <= 105
- 1 <= k <= 109
- coins[i] == [li, ri, ci]
- 1 <= li <= ri <= 109
- 1 <= ci <= 1000
- The given segments are non-overlapping.

---

## 题目（中文翻译）

描述  
在数轴上每个坐标都有一个袋子，袋子数量无限。部分袋子中含有硬币。  
给定一个二维数组（2D array）`coins`，其中 `coins[i] = [li, ri, ci]` 表示坐标从 `li` 到 `ri` 的每个袋子都含有 `ci` 枚硬币。  
这些区间（segments）互不重叠。  
同时给定一个整数 `k`。  
返回在连续 `k` 个袋子中可以收集到的硬币的最大数量。

示例  

**示例 1**  
输入: `coins = [[8,10,1],[1,3,2],[5,6,4]], k = 4`  
输出: `10`  
解释: 选择坐标为 `[3, 4, 5, 6]` 的四个连续袋子可以获得最多硬币：`2 + 0 + 4 + 4 = 10`。

**示例 2**  
输入: `coins = [[1,10,3]], k = 2`  
输出: `6`  
解释: 选择坐标为 `[1, 2]` 的两个连续袋子可以获得最多硬币：`3 + 3 = 6`。

约束条件  
- `1 <= coins.length <= 10^5`  
- `1 <= k <= 10^9`  
- `coins[i] == [li, ri, ci]`  
- `1 <= li <= ri <= 10^9`  
- `1 <= ci <= 1000`  
- 给定的区间互不重叠。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有 **有硬币的袋子** 展开成一个「一维数组」，数组的第 `i` 位代表坐标 `i` 上的袋子里有多少枚硬币。  
然后把长度为 `k` 的窗口在这条数组上滑动，算出每个窗口的硬币总数，取最大的那个。

> **类比**：想象你站在一条长长的走廊，每个格子里可能有硬币。你一次只能抓住连续 `k` 格子里的硬币，直接把每一种可能的起点都试一遍，就是暴力法。

因为坐标范围可以到 `10⁹`，直接展开数组根本不可行（需要太多内存）。但为了说明「暴力」的概念，我们可以 **把每个坐标都当成一个元素**，用两层循环：

1. **外层**遍历所有可能的窗口左端 `start`（这里我们只考虑 `coins` 中出现的左端 `li`，因为题目提示最优起点一定在 `li` 或 `ri‑k+1`，但在暴力实现里我们仍然把每个 `li` 当作起点）。
2. **内层**从 `start` 开始往右数 `k` 步，逐个检查每个坐标属于哪个区间，累加对应的硬币数。

> **为什么一定对？**  
> 我们把每一种可能的窗口都算了一遍，肯定能找到最大值。只是不考虑效率。

#### 代码（Python）

```python
def maxCoins_bruteforce(coins, k):
    """
    暴力解：枚举每个可能的窗口左端，逐格累加硬币数
    复杂度极高，仅作思路演示。
    """
    # 把区间按左端排序，方便后面查找
    coins.sort(key=lambda x: x[0])

    best = 0                     # 记录最大硬币数
    # 所有可能的左端只取每个区间的左端 li（实际还会有很多其它起点，这里只演示）
    for seg in coins:
        start = seg[0]           # 以当前区间的左端作为窗口左端
        total = 0                # 当前窗口的硬币总和
        # 逐格检查窗口内的 k 个坐标
        for pos in range(start, start + k):
            # 找到 pos 落在哪个区间
            for l, r, c in coins:
                if l <= pos <= r:          # 区间覆盖到了 pos
                    total += c
                    break                 # 每个坐标只会被一个区间覆盖
        best = max(best, total)           # 更新答案
    return best
```

> **代码说明**  
> - `range(start, start + k)` 表示窗口内的每一个具体坐标。  
> - 两层 `for` 循环分别是「所有起点」和「窗口内每个格子」，因此时间会非常慢。

#### 复杂度

- **时间复杂度**：`O(N * k)`（`N` 为区间个数，`k` 为窗口长度）。  
  大白话：如果有 1000 个区间，窗口长 10000，你得算 1000 × 10000 = 1 0000 000 次，显然不可接受。
- **空间复杂度**：`O(1)`，只用了几个临时变量。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在 **「逐格遍历」**——每次都要检查 `k` 个坐标。  
要想快，就要 **一次性算出窗口内所有坐标的硬币总和**，而不是一个一个加。

观察题目：

- 区间之间 **不重叠**，且每个区间内部的硬币数是恒定的（每个袋子都有 `ci` 枚）。
- 窗口是 **连续的 `k` 个坐标**，可以把窗口想成一根长 `k` 的绳子在数轴上滑动，绳子覆盖的部分会把对应的硬币全部收进来。

这正好可以用 **「双指针 + 前缀和」** 的思路来解决：

1. **把每个区间抽象成两件事**  
   - `len_i = ri - li + 1`  （区间的长度，即有多少个袋子）  
   - `sum_i = len_i * ci` （这段区间里所有硬币的总数）  

2. **维护一个滑动窗口**，窗口内的「总长度」不超过 `k`，窗口内的「硬币总数」随时可得。  
   - 用 `right` 指针把窗口往右扩展，直到窗口长度 **超过** `k`。  
   - 当超过 `k` 时，**左指针 `left` 向右收缩**，把最左边的区间（或其一部分）剔除，使窗口长度恰好 ≤ `k`。  
   - 在收缩/扩展的过程中，**只需要更新几个变量**（当前长度、当前硬币数），不必遍历每个坐标。

3. **处理「部分区间」**  
   - 当窗口的左边界落在某个区间的中间时，只收取该区间的 **右侧** 部分；同理，右边界落在区间中间时，只收取 **左侧** 部分。  
   - 这可以通过 **记录左指针所在区间的已经「丢掉」的长度** 来实现。

4. **遍历完所有区间后，记录的最大硬币数即为答案**。

> **类比**：想象一根绳子在一条装有若干段「糖果」的轨道上滑动。每段糖果的甜度相同，长度不同。我们每次只关心绳子上有多少甜度，而不是每颗糖果。用双指针就像把绳子的一端固定，另一端不断往前推，然后再把左端收回来，始终保持绳子长度 ≤ `k`。

**关键点**  
- 先把区间按照左端 `li` 排序（因为后面要按顺序滑动）。  
- 使用 **长整型**（`int` 在 Python 已经是大整数）防止乘法溢出。  
- 只需要 `O(N)` 的时间和 `O(1)` 的额外空间（排序除外）。

#### 代码（Python）

```python
def maxCoins(coins, k):
    """
    最优解：双指针滑动窗口（O(N log N) 由于排序，主体 O(N)）
    """
    # 1️⃣ 把区间按左端排序，方便顺序遍历
    coins.sort(key=lambda x: x[0])

    n = len(coins)
    left = 0          # 窗口最左侧区间的索引
    cur_len = 0       # 窗口已经覆盖的坐标个数
    cur_sum = 0       # 窗口内已收集的硬币总数
    best = 0          # 记录最大值

    # 右指针遍历每个区间
    for right in range(n):
        l, r, c = coins[right]
        seg_len = r - l + 1               # 该区间的长度
        seg_sum = seg_len * c             # 该区间全部硬币数

        # 把整个区间加入窗口
        cur_len += seg_len
        cur_sum += seg_sum

        # 2️⃣ 如果窗口长度已经 > k，需要从左侧收缩
        while cur_len > k:
            lL, rL, cL = coins[left]
            left_seg_len = rL - lL + 1

            # 计算左侧区间还有多少已经在窗口之外（已经“丢掉”）
            excess = cur_len - k          # 需要剔除的长度

            if excess >= left_seg_len:    # 整个左区间都要丢掉
                cur_len -= left_seg_len
                cur_sum -= left_seg_len * cL
                left += 1                 # 完全移出左区间
            else:                         # 只丢掉左区间的一部分
                # 只保留左区间的右 side，长度变为 left_seg_len - excess
                cur_len -= excess
                cur_sum -= excess * cL
                # 更新左区间的左端位置，使其“向右移动”excess 步
                coins[left][0] += excess   # 直接修改 l 值（因为后面不再需要原始 l）
                break

        # 3️⃣ 此时窗口长度 ≤ k，更新答案
        best = max(best, cur_sum)

    return best
```

> **代码逐行解释**  
> - `coins.sort(...)`：把所有区间从左到右排好序，像把书架上的书按编号摆好。  
> - `cur_len`、`cur_sum`：分别记录窗口当前覆盖了多少个坐标、收集了多少硬币。  
> - `while cur_len > k`：窗口太宽了，需要把左边多余的部分「剪掉」——这一步是双指针的核心。  
> - `excess`：多出的长度（比如窗口已经 12，k=8，则 excess=4，需要从左边删掉 4）。  
> - 当 `excess` 大于等于左侧整个区间的长度时，直接把整个左区间踢出窗口；否则，只把左区间的左侧 **一小段** 剪掉（通过 `coins[left][0] += excess` 把左端坐标向右移动）。  
> - `best = max(best, cur_sum)`：每次窗口合法后，更新全局最大值。

#### 复杂度

- **时间复杂度**：`O(N log N)`  
  - `O(N log N)` 用于对 `coins` 按左端排序（相当于把散乱的盒子排成一排）。  
  - 排序后，双指针只会 **各自向右移动一次**，所以主体是 `O(N)`。  
  与暴力的 `O(N·k)` 相比，快了几个数量级——即使 `k` 达到 `10⁹` 也不影响时间。

- **空间复杂度**：`O(1)`（不计输入本身）。  
  - 只用了几个整数变量 `left, cur_len, cur_sum, best`，没有额外的数组。  
  - “常数空间”可以理解为“无论数据多大，额外占用的内存几乎不变”。

---

## 心得

- **核心技巧**：**双指针 + 前缀和（或区间累计）**，在「区间不重叠」且「每个区间内部属性相同」的场景下，能把「逐格累加」压缩成「整体搬运」。
- **适用题型**  
  1. 在一条数轴上，求长度为 `k` 的窗口能够覆盖的最大「权值」——如「Maximum Sum of Subarray with Length at Most K」  
  2. 「在若干段时间区间里，找出连续 `k` 天收益最高」——如股票、日志分析等  
  3. 「在若干段道路上，找出长度为 `k` 的道路段的最高维修价值」——类似本题的变形
- **一句话总结解题钥匙**：  
  > 把「每个坐标」的循环换成「每段区间」的整体搬运，用双指针保证窗口长度恰好 `k`。

---

## 反思

- **第一反应**：看到「无限袋子」和「区间不重叠」就想把所有袋子展开成数组，直接滑动窗口。  
- **最容易踩的坑**  
  - **坐标范围太大**：`li, ri` 可以到 `10⁹`，直接展开会导致内存爆炸。  
  - **窗口跨越区间边界**：需要处理左、右两端只取区间的一部分，不能只把完整区间的总和相加。  
  - **`k` 可能大于所有区间的总长度**：此时窗口会覆盖所有袋子，答案是所有硬币的总和，代码必须能正确处理「窗口仍未填满」的情况。  
- **下次类似题的第一步**：  
  > 先把「每个点」抽象成「区间长度 × 单位价值」的 **块**，检查是否可以用「双指针」在块之间滑动来控制窗口长度，而不是逐点遍历。这样既能避免大数据的展开，又能在 O(N) 或 O(N log N) 时间内得到答案。