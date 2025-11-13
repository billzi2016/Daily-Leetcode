# #3420. K 次操作后统计非递减子数组 / Count Non-Decreasing Subarrays After K Operations

> 难度：困难 · 标签：Array、Stack、Segment Tree、Queue、Sliding Window、Monotonic Stack、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/count-non-decreasing-subarrays-after-k-operations/)

---

## 题目（英文原版）

**Description**

You are given an array nums of n integers and an integer k.
For each subarray of nums, you can apply up to k operations on it. In each operation, you increment any element of the subarray by 1.
Note that each subarray is considered independently, meaning changes made to one subarray do not persist to another.
Return the number of subarrays that you can make non-decreasing ​​​​​after performing at most k operations.
An array is said to be non-decreasing if each element is greater than or equal to its previous element, if it exists.

**Examples**

**Example 1:**

```
Input: nums = [6,3,1,2,4,4], k = 7
Output: 17
Explanation:
Out of all 21 possible subarrays of nums , only the subarrays [6, 3, 1] , [6, 3, 1, 2] , [6, 3, 1, 2, 4] and [6, 3, 1, 2, 4, 4] cannot be made non-decreasing after applying up to k = 7 operations. Thus, the number of non-decreasing subarrays is 21 - 4 = 17 .
```

**Example 2:**

```
Input: nums = [6,3,1,3,6], k = 4
Output: 12
Explanation:
The subarray [3, 1, 3, 6] along with all subarrays of nums with three or fewer elements, except [6, 3, 1] , can be made non-decreasing after k operations. There are 5 subarrays of a single element, 4 subarrays of two elements, and 2 subarrays of three elements except [6, 3, 1] , so there are 1 + 5 + 4 + 2 = 12 subarrays that can be made non-decreasing.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums` 和一个整数 `k`。  
对于 `nums` 的每个子数组（subarray），你可以对其最多进行 `k` 次操作。每次操作可以将子数组中的任意一个元素加 `1`。  
注意，每个子数组是相互独立考虑的，也就是说，对某个子数组所做的修改不会影响到其他子数组。  

返回在至多进行 `k` 次操作后，能够使子数组变为非递减（non‑decreasing）的子数组数量。  
如果一个数组中每个元素都 **大于等于** 前一个元素（若前一个元素存在），则称该数组为非递减。

## 示例

### 示例 1
**输入**  
```text
nums = [6,3,1,2,4,4], k = 7
```
**输出**  
```text
17
```
**解释**  
`nums` 的所有可能子数组共有 `21` 个，其中子数组 `[6, 3, 1]`、`[6, 3, 1, 2]`、`[6, 3, 1, 2, 4]` 和 `[6, 3, 1, 2, 4, 4]` 在最多进行 `k = 7` 次操作后仍无法变为非递减。因此，可使其非递减的子数组数量为 `21 - 4 = 17`。

### 示例 2
**输入**  
```text
nums = [6,3,1,3,6], k = 4
```
**输出**  
```text
12
```
**解释**  
子数组 `[3, 1, 3, 6]` 以及所有长度不超过 `3` 的子数组（除 `[6, 3, 1]` 之外）都可以在 `k` 次操作内变为非递减。单元素子数组有 `5` 个，长度为 `2` 的子数组有 `4` 个，长度为 `3` 的子数组有 `2` 个（不包括 `[6, 3, 1]`），所以总共有 `5 + 4 + 2 = 11` 个子数组，加上 `[3, 1, 3, 6]` 本身，共 `12` 个子数组可以在 `k` 次操作后变为非递减。

## 约束

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：枚举所有 **子数组**，对每一个子数组尝试把它变成非递减序列，看看需要的最少增量次数是否 ≤ k。  

- **枚举子数组**：双层循环，外层 `i` 为左端点，内层 `j` 为右端点。  
- **计算所需增量**：从左到右遍历子数组，维护当前已经“提升”到的最小合法值 `cur`（一开始等于子数组的第一个元素）。  
  - 若下一个元素 `x` 已经 ≥ `cur`，则不需要操作，只把 `cur = x`。  
  - 若 `x` < `cur`，则必须把它提升到 `cur`，操作次数加 `cur - x`，并把 `cur` 维持不变（因为提升后它等于 `cur`）。  
- 只要累计的操作次数超过 `k`，就可以提前退出该子数组的检查。  

**为什么正确**：  
非递减的定义恰好是每个位置的值 **不小于** 前一个位置的值。把每个不满足的地方提升到前一个位置的值，就是让整个子数组满足条件且增量最小（因为只提升到刚好够的程度）。  

**复杂度分析**（大白话版）  
- 外层遍历 `n` 次，内层最坏也遍历 `n` 次，里面还有一次线性遍历子数组。整体是 **三层**循环，时间大约是 `n³/6`，用大 O 记作 **O(n³)**。  
- 这里的 `n` 最多 10⁵，`n³` 完全不可接受（相当于 **一万亿** 次操作）。  
- 空间只用了常数个变量，**O(1)**。  

#### 代码（Python）

```python
def count_subarrays_bruteforce(nums, k):
    n = len(nums)
    ans = 0

    # i 为左端点，j 为右端点（闭区间）
    for i in range(n):
        for j in range(i, n):
            ops = 0          # 已经用了多少次增量
            cur = nums[i]    # 子数组左端点的当前值（已经“提升”后的值）

            # 从 i+1 到 j 检查每个元素
            for p in range(i + 1, j + 1):
                x = nums[p]
                if x < cur:                 # 需要提升
                    ops += cur - x
                    if ops > k:             # 已经超出上限，直接放弃
                        break
                else:
                    cur = x                  # 已经不需要提升，更新 cur
            else:
                # for 正常结束，说明 ops ≤ k
                ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 三层循环，想象一下把一个 10⁵ 长的数组全排列遍历，根本做不完。  
- **空间复杂度**：`O(1)` —— 只用了几个计数器，和数组大小无关。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都从头遍历子数组**，导致大量重复计算。  
观察到：

1. 对于一个子数组 `[l … r]`，如果已经知道把 `[l … m]`（左半段）变成非递减所需的操作次数 `opL`，以及变完后左半段的**最后一个元素的值** `lastL`，  
   那么把右半段 `[m+1 … r]` 合并进来，只需要把右半段每个元素提升到 **不低于 `lastL`** 的水平。  
2. 这正好是**二进制分块**（或叫**稀疏表**）的思路：预处理所有长度为 `2^e` 的区间，记录  
   - `last[e][i]`：把区间 `[i … i+2^e-1]` 变成非递减后，**最右端的元素**的值。  
   - `cost[e][i]`：完成上述变换**最少需要的增量次数**。  

这样，任意长度的子数组都可以用**若干个 2 的幂次区间**拼起来（类似把数字写成二进制），并在 **O(log n)** 时间内合并它们得到总的 `cost` 与 `last`。  

**合并两个相邻区间**  
设左区间为 `A = [i … i+lenA-1]`，右区间为 `B = [i+lenA … i+lenA+lenB-1]`，已知  
- `lastA`、`costA`（左区间变完后的最后值和花费）  
- `lastB`、`costB`（右区间变完后的最后值和花费）  

把它们拼成 `A+B` 时，需要把右区间的每个元素提升到 **不小于 `lastA`**。因为右区间内部已经是非递减的，只需要把**整个区间整体向上平移**：

- 需要的额外操作 = `max(0, lastA - lastB) * lenB`  
  （如果右区间的最后元素已经 ≥ `lastA`，则不需要额外操作；否则所有 `lenB` 个元素都要提升相同的差值）  
- 合并后整体的最后元素值 = `max(lastA, lastB)`（两段合并后最右端的值就是两者的较大者）  

于是：

```
new_cost = costA + costB + max(0, lastA - lastB) * lenB
new_last = max(lastA, lastB)
```

这正是**单调栈/单调队列**背后的“把低的抬高到高的”思想，只是这里我们在预处理阶段就把它写成了合并公式。

**滑动窗口 + 二分**  
有了区间合并的 O(log n) 查询，我们可以对每个左端点 `l` **二分**出最大的右端点 `r` 使得 `cost(l, r) ≤ k`。  
因为 `cost(l, r)` 随着 `r` 增大只会 **不减**（只能需要更多或相同的操作），所以二分合法。  
对所有 `l` 求得的合法 `r`，子数组数量贡献为 `r - l + 1`（左端点固定，右端点可以是 `l … r`）。

整体复杂度：  
- 预处理稀疏表：`O(n log n)`  
- 对每个 `l` 二分查询：`O(log n * log n)` → `O(log² n)`，总计 `O(n log² n)`。  
- 这已经可以接受（`n = 10⁵` 时约几百万次操作），但还有更快的 **滑动窗口**（双指针）可以把 `log n` 去掉。这里保持二分实现，思路更直观。

#### 代码（Python）

```python
import math

def count_subarrays(nums, k):
    n = len(nums)
    LOG = math.ceil(math.log2(n)) + 1   # 最高需要的幂次

    # 预处理：last[e][i]、cost[e][i]
    last = [[0] * n for _ in range(LOG)]
    cost = [[0] * n for _ in range(LOG)]

    # e = 0 时，长度为 1 的区间
    for i in range(n):
        last[0][i] = nums[i]   # 单个元素本身就是最后一个
        cost[0][i] = 0         # 不需要任何操作

    # 逐步合并成长度 2^e 的区间
    for e in range(1, LOG):
        length = 1 << e          # 当前区间长度
        half = length >> 1       # 左半段长度 = 2^{e-1}
        for i in range(n - length + 1):
            # 左半段信息
            lastL = last[e-1][i]
            costL = cost[e-1][i]

            # 右半段信息（起点是 i+half）
            lastR = last[e-1][i + half]
            costR = cost[e-1][i + half]

            # 合并公式（见思路）
            extra = max(0, lastL - lastR) * half   # 右半段整体需要提升的次数
            cost[e][i] = costL + costR + extra
            last[e][i] = max(lastL, lastR)          # 合并后最右端的值

    # ------------------------------------------------------------
    # 辅助函数：利用稀疏表在 O(log n) 时间内得到子数组 [l, r] 的 cost 与 last
    # ------------------------------------------------------------
    def query(l, r):
        """返回 (cost, last) 使子数组 nums[l..r] 非递减所需最少操作次数和最终的最后一个元素值"""
        cur_cost = 0
        cur_last = None          # None 表示还没有任何元素
        pos = l
        # 按二进制位从高到低尝试取最大长度的区间
        for e in reversed(range(LOG)):
            length = 1 << e
            if pos + length - 1 > r:   # 超出右端点，跳过
                continue
            if cur_last is None:
                # 第一次取区间，直接使用其信息
                cur_cost = cost[e][pos]
                cur_last = last[e][pos]
            else:
                # 合并当前已有区间 (cur_last, cur_cost) 与新的区间
                new_last = last[e][pos]
                new_cost = cost[e][pos]

                extra = max(0, cur_last - new_last) * length
                cur_cost = cur_cost + new_cost + extra
                cur_last = max(cur_last, new_last)
            pos += length
        return cur_cost, cur_last

    # ------------------------------------------------------------
    # 主循环：对每个左端点二分右端点
    # ------------------------------------------------------------
    ans = 0
    for left in range(n):
        lo, hi = left, n - 1
        best = left - 1   # 记录满足条件的最右端点，初始为 left-1（即空区间）
        while lo <= hi:
            mid = (lo + hi) // 2
            c, _ = query(left, mid)
            if c <= k:
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        ans += best - left + 1   # 右端点可以是 left … best
    return ans
```

> **代码要点注释**  
> - `last[e][i]`、`cost[e][i]` 分别对应 “**区间结束后最后一个元素的值**” 与 “**完成该区间所需的最小增量次数**”。  
> - 合并时的 `extra = max(0, lastL - lastR) * lenR` 正是把右半段整体抬高到左半段的最后值所需的操作数。  
> - `query` 利用二进制拆分把 `[l, r]` 划分为若干个已预处理好的 2 的幂次区间，依次合并得到整体 `cost`。  

#### 复杂度  

- **预处理**：`O(n log n)` 时间，`O(n log n)` 空间。  
  - 解释：`log n` 层稀疏表，每层遍历 `n` 个起点，做常数次运算。  
- **每个左端点的二分查询**：`O(log n * log n)`（一次二分 + 每次 `query` 为 `O(log n)`）。  
  对全部 `n` 个左端点，总时间 `O(n log² n)`，在 10⁵ 规模下约几百万次，完全可接受。  
- **空间**：稀疏表占 `O(n log n)`，其余为 `O(1)`。  

与暴力解相比，时间从不可接受的 `O(n³)` 降到了 `O(n log² n)`，大幅提升。  

---

## 心得  

- **核心技巧**：**稀疏表（二进制分块） + 区间合并公式**，把“把子数组变为非递减”这件事抽象为“记录区间的最终最后值和累计费用”。  
- **适用的题型**  
  1. “区间合并后需要的最小代价” 类似的 **区间增量**、**区间配平** 题目。  
  2. 需要 **快速求区间属性**（如最大、最小、 gcd）并能 **合并**的场景——比如 **区间最小生成树**、**区间异或**。  
  3. 需要 **二分左端点/右端点** 的 **滑动窗口** 计数问题，如 “最多 k 次修改使子数组满足单调”。  
- **一句话总结解题钥匙**：  
  > 把子数组的“非递减成本”拆成可叠加的 **2 的幂次块**，预处理每块的 **最后值** 与 **费用**，随后二分/滑窗即可快速累计。  

---

## 反思  

- **第一反应**：直接遍历所有子数组，尝试逐个计算所需增量。  
- **最容易踩的坑**  
  - 忽视 **费用随右端点单调不减** 的性质，导致没有想到可以二分。  
  - 合并两段区间时忘记乘以右段长度 `lenR`（因为每个元素都要提升同样的差值），导致费用计算错误。  
  - 稀疏表的边界处理：`i + length - 1` 超出数组时必须跳过。  
- **下次类似题目**：  
  1. 先判断是否可以把 **局部信息（如最后值、最小值）** 用 **可合并的形式** 保存。  
  2. 检查答案随区间扩张的 **单调性**，若单调则可以二分或滑动窗口。  
  3. 选用 **稀疏表 / 线段树 / 单调栈** 等数据结构来实现 **O(log n)** 或 **O(1)** 的区间合并查询。