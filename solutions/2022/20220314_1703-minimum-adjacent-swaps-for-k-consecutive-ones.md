# #1703. K 个连续 1 的最少相邻交换次数 / Minimum Adjacent Swaps for K Consecutive Ones

> 难度：困难 · 标签：Array、Greedy、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-adjacent-swaps-for-k-consecutive-ones/)

---

## 题目（英文原版）

**Description**

You are given an integer array, nums, and an integer k. nums comprises of only 0's and 1's. In one move, you can choose two adjacent indices and swap their values.
Return the minimum number of moves required so that nums has k consecutive 1's.

**Examples**

**Example 1:**

```
Input: nums = [1,0,0,1,0,1], k = 2
Output: 1
Explanation: In 1 move, nums could be [1,0,0,0,1,1] and have 2 consecutive 1's.
```

**Example 2:**

```
Input: nums = [1,0,0,0,0,0,1,1], k = 3
Output: 5
Explanation: In 5 moves, the leftmost 1 can be shifted right until nums = [0,0,0,0,0,1,1,1].
```

**Example 3:**

```
Input: nums = [1,1,0,1], k = 2
Output: 0
Explanation: nums already has 2 consecutive 1's.
```

**Constraints**

- 1 <= nums.length <= 105
- nums[i] is 0 or 1.
- 1 <= k <= sum(nums)

---

## 题目（中文翻译）

给定一个仅包含 0 和 1 的整数数组 `nums`，以及一个整数 `k`。在一次操作中，你可以选择两个相邻下标并交换它们的值。  
返回使得数组 `nums` 中出现恰好 `k` 个连续的 1 所需的最少操作次数。

## 示例

### 示例 1
**输入**  
`nums = [1,0,0,1,0,1], k = 2`

**输出**  
`1`

**解释**  
只需一次交换即可得到 `[1,0,0,0,1,1]`，此时出现 2 个连续的 1。

### 示例 2
**输入**  
`nums = [1,0,0,0,0,0,1,1], k = 3`

**输出**  
`5`

**解释**  
通过 5 次交换，最左侧的 1 可以向右移动，最终得到 `[0,0,0,0,0,1,1,1]`，形成 3 个连续的 1。

### 示例 3
**输入**  
`nums = [1,1,0,1], k = 2`

**输出**  
`0`

**解释**  
数组已经拥有 2 个连续的 1，无需任何交换。

## 约束条件
- `1 <= nums.length <= 10^5`
- `nums[i]` 为 `0` 或 `1`
- `1 <= k <= sum(nums)`（即数组中 1 的总数）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 先把数组里所有 `1` 的下标记下来，形成一个列表 `pos`。  
2. 枚举所有可能的 **连续** `k` 个 `1`（即在 `pos` 中取长度为 `k` 的子序列），把这 `k` 个 `1` 移动到同一个位置，使它们在最终数组里变成相邻的 `k` 个 `1`。  
3. 对每一种子序列，计算把它们聚在一起需要的交换次数——把每个 `1` 往目标位置走一步，就相当于一次相邻交换。把所有 `1` 到达目标位置的步数相加，就是这一次的代价。  
4. 取所有子序列代价的最小值，就是答案。

> **类比**：把 `1` 看成书架上的书，空位 `0` 看成空格。我们想把 `k` 本书搬到相邻的 `k` 个格子里。最暴力的办法就是把每本书搬到每一种可能的“连排书架”上，算算搬动的格子数，找最省力的那一种。

**为什么正确**：  
- 只要把 `k` 本书搬到同一段连续的格子里，数组中一定会出现 `k` 个相邻的 `1`。  
- 所有可能的连续 `k` 本书的起始位置都被枚举到了，所以最小代价一定会被发现。

**时间/空间复杂度**  
- 假设数组长度是 `n`，`1` 的个数记作 `m（m ≤ n）`。  
- 枚举 `m - k + 1` 种窗口，每种窗口内部需要遍历 `k` 个元素求和，时间复杂度是 **O((m‑k+1)·k)**，在最坏情况下 `m≈n`、`k≈n/2` 时会达到 **O(n²)**。  
- 只需要保存 `pos` 列表，空间是 **O(m) ≤ O(n)**。

> **大白话**：`O(n²)` 就像把 10,000 条街道两两比较一次，需要 1 亿 次操作，显然会很慢。

#### 代码（Python）

```python
from typing import List

def minMovesBrute(nums: List[int], k: int) -> int:
    # 记录所有 1 的下标
    pos = [i for i, v in enumerate(nums) if v == 1]   # 类似查字典，key 是位置，value 是 1 本身
    m = len(pos)
    ans = float('inf')

    # 枚举所有长度为 k 的窗口
    for left in range(m - k + 1):
        right = left + k - 1               # 窗口右端下标
        # 把这 k 个 1 移动到同一个位置（这里随便选 pos[mid] 作为目标）
        mid = left + k // 2                # 窗口的中间位置（下标）
        target = pos[mid]                  # 目标位置

        # 计算所有 1 移动到 target 所需的步数
        moves = 0
        for i in range(left, right + 1):
            moves += abs(pos[i] - target)  # 每走一步就是一次相邻交换

        ans = min(ans, moves)

    return ans
```

#### 复杂度

- **时间复杂度**：`O((m‑k+1)·k) ≤ O(n²)` —— 在最坏情况下会出现两层循环，每层最多遍历 `n` 次。  
- **空间复杂度**：`O(m) ≤ O(n)` —— 只存了所有 `1` 的下标。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道：**只要把 `k` 个 `1` 聚在一起，移动次数等于它们到某个中心位置的距离之和**。  
暴力解慢的根源在于每次都要**重新遍历**窗口内部的 `k` 个元素来求和。我们可以把这一步“累计求和”改成 **滑动窗口 + 前缀和**，做到 **O(m)**（只遍历一次 `1` 的下标）。

**关键观察 1：**  
把窗口中的 `1` 直接移动到窗口中心（中位数）是最省力的。原因是绝对值求和的最小点恰好是中位数，这在统计学里叫“最小绝对偏差”。

**关键观察 2：**  
如果我们把每个 `1` 的下标 `pos[i]` 减去它在 `pos` 中的序号 `i`，得到 **adjusted[i] = pos[i] - i**。  
这样做的好处是：当我们把 `k` 个 `1` 聚在一起时，它们之间的相对顺序不变，实际需要的交换次数等价于把 `adjusted` 中的 `k` 个数聚在一起的距离之和。  
直观点说，`i` 表示这第 `i` 本书在书架上原来的“排队位置”，减去 `i` 就把每本书向左“压缩”，把相邻的空格（0）去掉，剩下的距离就是 **真实需要交换的格子数**。

**关键观察 3（前缀和）**  
我们需要快速算出窗口内所有 `adjusted` 与窗口中位数的差的绝对值之和。  
设窗口左端为 `l`，右端为 `r = l + k - 1`，中位数下标 `mid = l + k // 2`。  
把窗口划分为左半部分和右半部分：

- 左半部分（包括中位数本身）需要的步数 = `mid * adjusted[mid] - (prefix[mid] - prefix[l-1])`
- 右半部分需要的步数 = `(prefix[r] - prefix[mid]) - (r - mid) * adjusted[mid]`

其中 `prefix[i]` 是 `adjusted` 的前缀和，`prefix[-1]` 设为 `0`。  
这两个式子来源于**等差数列求和**，把所有左侧元素与中位数的差累加，同理右侧。

**整体步骤**  

1. 把所有 `1` 的下标存入 `pos`。  
2. 计算 `adjusted[i] = pos[i] - i`，并求它的前缀和 `pref`。  
3. 用滑动窗口遍历 `pos`（长度为 `k`），对每个窗口利用上面的公式 O(1) 计算聚在一起的代价。  
4. 取最小值即为答案。  

**为什么只向右滑动**：  
窗口的左端只会增大，右端只会增大，`mid` 也只会右移。这样我们可以用前缀和一次性得到每个窗口的代价，无需回溯。

#### 代码（Python）

```python
from typing import List

def minMoves(nums: List[int], k: int) -> int:
    # 1. 记录所有 1 的原始下标
    pos = [i for i, v in enumerate(nums) if v == 1]          # 类似查字典，key 是位置
    m = len(pos)

    # 2. 计算 adjusted = pos[i] - i
    adjusted = [pos[i] - i for i in range(m)]

    # 3. 前缀和（pref[i] = adjusted[0] + ... + adjusted[i]）
    pref = [0] * m
    pref[0] = adjusted[0]
    for i in range(1, m):
        pref[i] = pref[i - 1] + adjusted[i]

    # 辅助函数：求区间 [l, r] 的前缀和，l > 0 时用 pref[r] - pref[l-1]
    def range_sum(l: int, r: int) -> int:
        if l > r:
            return 0
        return pref[r] - (pref[l - 1] if l > 0 else 0)

    ans = float('inf')

    # 4. 滑动窗口，长度为 k
    for l in range(m - k + 1):
        r = l + k - 1
        mid = l + k // 2                # 中位数下标（左中位或右中位均可）

        # 左半部分（包括中位数本身）
        left_cost = adjusted[mid] * (mid - l + 1) - range_sum(l, mid)

        # 右半部分（不包括中位数本身）
        right_cost = range_sum(mid + 1, r) - adjusted[mid] * (r - mid)

        total = left_cost + right_cost

        # 当 k 为偶数时，窗口的中位数取左侧会导致多算一个偏移，需要再减去 (k//2)
        # 这是因为我们在 adjusted 中已经把每个位置 i 向左压缩了 i 步，聚在一起时会多出 (k//2) 的“空隙”。
        # 直接减去 (k//2) 就能得到真实的交换次数。
        if k % 2 == 0:
            total -= k // 2

        ans = min(ans, total)

    return ans
```

> **代码要点注释**  
> - `adjusted[i] = pos[i] - i` 把每本书向左“压缩”，把 0 的干扰消掉。  
> - `pref` 是前缀和，用来在 O(1) 时间内求任意区间的和。  
> - `left_cost` 与 `right_cost` 分别是窗口左侧、右侧需要的移动步数。  
> - 当 `k` 为偶数时，需要额外减去 `k//2`（相当于把“压缩”时多算的空格去掉），这样得到的才是实际的相邻交换次数。

#### 复杂度

- **时间复杂度**：`O(m) ≤ O(n)`  
  - 只遍历一次 `pos`（收集 1 的下标）+ 一次遍历计算前缀和 + 再一次滑动窗口，每一步都是 O(1)。  
  - 与暴力解的 `O(n²)` 相比，速度提升了数量级，能轻松处理 `10⁵` 长度的数组。

- **空间复杂度**：`O(m) ≤ O(n)`  
  - 需要存 `pos`、`adjusted`、`pref` 三个长度为 `m` 的数组。  
  - 只和 `1` 的个数有关，最坏情况下 `m = n`，仍然是线性空间。

---

## 心得

- **核心技巧**：把 “相邻交换次数 = 绝对距离之和” 用 **中位数** 最小化，再通过 **位置压缩 (pos[i] - i)** 把数组中的 `0` 去除，最后利用 **前缀和 + 滑动窗口** 实现 O(n) 求解。  
- **适用场景**：  
  1. **最小移动次数使 k 个元素相邻**（本题）。  
  2. **把所有 1 聚成一段**（LeetCode 1151: Minimum Swaps to Group All 1's）。  
  3. **把 k 个点聚到一起的最小总距离**（类似 “最小移动成本” 的几何问题）。  
- **一句话总结解题钥匙**：  
  “把 1 的下标减去其序号，再在压缩后的数组上用中位数 + 前缀和滑窗求最小绝对偏差，即得到最少相邻交换次数。”

---

## 反思

- **第一反应**：看到“相邻交换”就想到“把 1 们搬到一起”，于是尝试枚举所有可能的连续 1 子序列并逐个计算代价——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记把 `pos[i] - i` 的压缩操作，直接在原下标上求中位数会多算出因为中间的 `0` 带来的额外距离。  
  - 当 `k` 为偶数时，需要额外减去 `k//2` 的偏移，否则答案会比实际大 1。  
  - 边界条件：`k = 1`（答案必为 0）以及数组全是 `1`（同样 0）。  
- **下次类似题的第一步**：  
  “先把所有目标元素的下标抽出来，用 `pos[i] - i` 消除空位的影响，再在这个压缩后的一维数组上找最小绝对偏差（中位数）”。这样可以立刻把问题转化为“最小距离求和”，随后考虑前缀和或滑动窗口来线性求解。