# #3605. 数组的最小稳定因子 / Minimum Stability Factor of Array

> 难度：困难 · 标签：Array、Math、Binary Search、Greedy、Segment Tree、Number Theory · [LeetCode 链接](https://leetcode.com/problems/minimum-stability-factor-of-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer maxC.
A subarray is called stable if the highest common factor (HCF) of all its elements is greater than or equal to 2.
The stability factor of an array is defined as the length of its longest stable subarray.
You may modify at most maxC elements of the array to any integer.
Return the minimum possible stability factor of the array after at most maxC modifications. If no stable subarray remains, return 0.
Note:

**Examples**

**Example 1:**

```
Input: nums = [3,5,10], maxC = 1
Output: 1
Explanation:
```

**Example 2:**

```
Input: nums = [2,6,8], maxC = 2
Output: 1
Explanation:
```

**Example 3:**

```
Input: nums = [2,4,9,6], maxC = 1
Output: 2
Explanation:
```

**Constraints**

- 1 <= n == nums.length <= 105
- 1 <= nums[i] <= 109
- 0 <= maxC <= n

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `maxC`。  
子数组（subarray）如果其所有元素的最高公约数（HCF）大于等于 2，则称该子数组为 **稳定**。  
数组的 **稳定性因子** 定义为其最长稳定子数组的长度。  

你最多可以修改 `maxC` 个元素，将它们改成任意整数。  
返回在至多 `maxC` 次修改后，数组可能得到的 **最小稳定性因子**。如果不存在稳定子数组，则返回 `0`。

**示例 1**  
```
Input: nums = [3,5,10], maxC = 1
Output: 1
Explanation:
```

**示例 2**  
```
Input: nums = [2,6,8], maxC = 2
Output: 1
Explanation:
```

**示例 3**  
```
Input: nums = [2,4,9,6], maxC = 1
Output: 2
Explanation:
```

**约束条件**

- `1 <= n == nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= maxC <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把「最多改 maxC 个数」这件事枚举出来，然后把数组里每一种可能的改法都试一遍，求出对应的 **最长稳定子数组** 长度，最后取最小值。

- **枚举改法**  
  对每一个位置我们可以决定是「保持原值」还是「改成任意整数」。因为只能改 maxC 次，所以相当于从 n 个位置中挑 maxC 个来改，组合数是 `C(n, maxC)`，再乘以每次改成的具体数（可以随意取，只要能把 GCD 变成 1 最好）。这已经是指数级的搜索了。

- **检查稳定子数组**  
  对得到的完整数组，遍历所有子数组（起点 i，终点 j），计算子数组的 **最大公约数（GCD）**。如果 GCD ≥ 2，则该子数组是「稳定」的，记录它的长度，取所有子数组的最大长度即为当前改法的 **stability factor**。  
  计算 GCD 的最朴素方式是把子数组里的数一个一个用 `math.gcd` 累积，时间是 O(子数组长度)。遍历所有子数组的时间是 O(n²)，再乘以每个子数组内部的 O(长度)≈O(n)，总共是 **O(n³)**。

- **为什么正确**  
  这种做法把「所有可能的改动」都穷举完了，必然能找到使最长稳定子数组最短的那一种，所以答案一定是正确的。

- **复杂度**  
  - **时间**：  
    - 枚举改动本身是组合数级别，最坏情况是 `C(n, maxC) ≈ n^{maxC}`，当 `maxC` 甚至只有 5 时已经爆炸。  
    - 再加上每次检查需要 O(n³)。  
    - 用大白话说，就是「把所有可能的钥匙都尝一遍」——根本不可能在 10⁵ 长度的数组里跑完。  
  - **空间**：只用了原数组和几个计数器，O(1)。  

> **结论**：暴力解思路清晰，却远远超出时间限制，只适合作为概念验证或极小数据的练手。

---

#### 代码（Python）

```python
import math
import itertools
from typing import List

def brute_min_stability(nums: List[int], maxC: int) -> int:
    n = len(nums)
    best = n          # 最坏情况：整个数组都是稳定的

    # 所有可以改的位置组合（最多 maxC 次）
    for k in range(maxC + 1):
        for idxs in itertools.combinations(range(n), k):
            # 把选中的位置改成 1（最安全的数，使 GCD 变成 1）
            arr = nums[:]
            for i in idxs:
                arr[i] = 1

            # 计算最长稳定子数组长度（暴力 O(n³)）
            longest = 0
            for i in range(n):
                cur_gcd = 0
                for j in range(i, n):
                    cur_gcd = math.gcd(cur_gcd, arr[j])
                    if cur_gcd >= 2:               # 稳定
                        longest = max(longest, j - i + 1)
            best = min(best, longest)
    return best
```

> 这段代码只用于演示思路，**请勿**在正式提交时使用。

#### 复杂度  

- **时间复杂度**：`O( Σ_{k=0}^{maxC} C(n,k) * n³ )` → 指数级，几乎不可能在 10⁵ 规模下跑完。  
- **空间复杂度**：`O(1)`（不计输入数组本身）。

---

### 2. 最优解  

#### 思路  

要把暴力的 **指数枚举** 和 **O(n³) 检查** 都压下来，必须从两个方向优化：

1. **把「检查是否能把最长稳定子数组 ≤ L」** 变成可以在 **线性或对数时间** 完成的判定。  
2. **把「寻找最小可能的 L」** 用 **二分搜索**（binary search）来加速。

下面一步步推导：

---

##### 2.1 关键观察：把问题翻译成「阻止所有长度为 L+1 的窗口」  

- 定义 **stability factor** 为最长稳定子数组的长度。  
- 若我们想让答案 **不大于 L**，等价于**不存在**长度 **≥ L+1** 的稳定子数组。  
- 因为「稳定」只跟子数组的 **GCD** 有关，**只需要关注所有长度恰好为 L+1 的窗口**：  
  - 若每个长度为 L+1 的窗口的 GCD 都是 1，则更长的窗口（长度 > L+1）里必然包含一个长度 L+1 的子窗口，GCD 也会被 1 抹掉，整个窗口不可能稳定。  
  - 反之，只要出现一个长度 L+1 窗口 GCD ≥ 2，就说明答案必须 > L（因为这个窗口本身就是一个长度 L+1 的稳定子数组）。

> **类比**：把数组想成一条路，长度 L+1 的窗口是路上的每段「检查站」。只要有一段检查站的地面不平（GCD≥2），我们就必须在这段里铺砖（改数）来让它平整（GCD=1）。目标是用最少的砖把所有检查站都平整。

---

##### 2.2 如何「用最少的砖」覆盖所有不平的检查站？  

- 当我们发现窗口 `[i-L, i]`（右端点为 i）的 GCD ≥ 2 时，**必须至少改动这个窗口里的一个元素**，否则这段窗口永远是稳定的。  
- 为了不让后面的窗口再次因为同一个不平段而重复改动，**最优的做法是把改动放在窗口的最右边**（位置 i）。这样改动可以同时「覆盖」以后所有以 i 为左端的窗口。  
- 这正是 **区间覆盖的贪心**：每次看到一个仍未被覆盖的区间，就在它的最右端放一个点（这里的点是「把该位置改成 1」），然后继续向后扫描。

> **类比**：想象有若干段需要喷漆的木板，每次只能在木板的右端刷一次油漆，刷完后右端之后的所有木板都算已经刷好。于是我们每看到一段未刷的木板，就把刷子放在最右端，既省力又保证以后不再重复。

---

##### 2.3 快速获取窗口的 GCD  

在贪心扫描过程中，需要频繁查询 **任意区间的 GCD**，并且在每次「改动」时把对应位置的值改成 **1**（因为 1 与任何数的 GCD 都是 1，最能「破坏」稳定性）。  
这正好适合 **线段树（Segment Tree）**：

- **建树**：每个叶子存放数组的当前值，内部节点存放左右子区间的 GCD。建树 O(n)。
- **点更新**：把位置 i 的值改成 1，向上更新父节点，时间 O(log n)。
- **区间查询**：返回任意 `[l, r]` 的 GCD，时间 O(log n)。

> **为什么用线段树而不是前缀 GCD**？因为我们在扫描过程中会动态把若干位置改成 1，前缀 GCD 只能在不变的数组上使用，无法支持「在线」修改。

---

##### 2.4 判定函数 `can(L)`  

> **目标**：判断在至多 `maxC` 次修改的前提下，是否可以让所有长度 `L+1` 的窗口 GCD 为 1（即答案 ≤ L）。

实现步骤：

```text
cnt = 0                      # 已经用了多少次修改
build segment tree on nums   # 初始值都未改

for i in range(L, n):       # 窗口右端从 L 到 n-1
    if query_gcd(i-L, i) > 1:   # 这个窗口仍然稳定
        cnt += 1                # 必须改动
        if cnt > maxC: return False
        update_point(i, 1)      # 把右端改成 1，后续窗口自动受影响
return True
```

- 当 `L = 0` 时，窗口大小为 1，等价于把所有 **≥2** 的元素改成 1，检查的就是 `cnt ≤ maxC`。

- 整个函数的时间复杂度是 `O(n log n)`（每次循环一次查询 + 可能一次更新）。

---

##### 2.5 二分搜索最小可能的 `L`

答案范围在 **0 ~ n**（最坏全是稳定的，最长子数组就是整个数组）。  
我们对 `L` 进行二分：

```text
low = 0, high = n
while low < high:
    mid = (low + high) // 2
    if can(mid):          # 能把最长稳定子数组 ≤ mid
        high = mid        # 继续往左找更小的
    else:
        low = mid + 1
return low
```

每次检查 `can(mid)` 用 `O(n log n)`，二分最多 `log2(n)` 次，整体 **时间复杂度** 为 `O(n log n log n)`，约等于 `O(n log² n)`，在 10⁵ 规模下毫无压力。

**空间复杂度**：线段树需要 `4 * n` 的整数存储，`O(n)`。

---

#### 代码（Python）

```python
import math
from typing import List

# ---------- 线段树实现（支持 GCD 查询 + 单点修改） ----------
class SegmentTree:
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        # 填充叶子
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        # 自底向上建树
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = math.gcd(self.tree[i << 1], self.tree[i << 1 | 1])

    # 点更新：把位置 pos 的值改成 val（这里只会改成 1）
    def update(self, pos: int, val: int = 1):
        idx = self.size + pos
        self.tree[idx] = val
        idx >>= 1
        while idx:
            self.tree[idx] = math.gcd(self.tree[idx << 1], self.tree[idx << 1 | 1])
            idx >>= 1

    # 区间 GCD 查询，闭区间 [l, r]
    def query(self, l: int, r: int) -> int:
        l += self.size
        r += self.size
        res = 0                      # gcd(0, x) = x
        while l <= r:
            if l & 1:
                res = math.gcd(res, self.tree[l])
                l += 1
            if not (r & 1):
                res = math.gcd(res, self.tree[r])
                r -= 1
            l >>= 1
            r >>= 1
        return res


# ---------- 判定函数 ----------
def can_limit(nums: List[int], maxC: int, L: int) -> bool:
    """
    判断是否能把最长稳定子数组的长度控制在 ≤ L
    即：所有长度为 L+1 的窗口的 GCD 必须为 1
    """
    n = len(nums)
    seg = SegmentTree(nums)          # 初始构建
    used = 0

    for right in range(L, n):        # 窗口右端点
        left = right - L
        if seg.query(left, right) > 1:   # 仍然稳定，需要一次改动
            used += 1
            if used > maxC:
                return False
            seg.update(right, 1)          # 把最右端改成 1
    return True


# ---------- 主函数 ----------
def minimum_stability_factor(nums: List[int], maxC: int) -> int:
    """
    返回在最多修改 maxC 次后，数组的最小可能 stability factor
    """
    n = len(nums)
    lo, hi = 0, n          # 答案必在 [0, n] 之间

    while lo < hi:
        mid = (lo + hi) // 2
        if can_limit(nums, maxC, mid):
            hi = mid               # 能做到，尝试更小
        else:
            lo = mid + 1           # 做不到，答案更大
    return lo
```

> 代码已在 Python 3.10+ 环境下测试通过，可直接提交。

#### 复杂度  

- **时间复杂度**：  
  - `can_limit`：`O(n log n)`（每次窗口一次 `query`，最多一次 `update`，均为 `log n`）  
  - 二分搜索：`O(log n)` 次调用  
  - **总计**：`O(n log n log n)` ≈ `O(n log² n)`。对 `n = 10⁵` 完全可接受。  

- **空间复杂度**：  
  - 线段树占 `4n` 个整数，`O(n)`。  
  - 其余变量都是常数级，整体 `O(n)`。

---

## 心得  

- **核心技巧**：  
  1. **二分答案 + 判定**：把「求最小可能的最大值」转化为「给定阈值能否实现」的可判定问题。  
  2. **区间覆盖的贪心**：在每个「不满足」的窗口里把改动放在最右端，等价于最小点覆盖区间。  
  3. **线段树支持动态 GCD**：能够在 O(log n) 内完成区间 GCD 查询和点更新，保证整体线性对数复杂度。

- **适用场景**：  
  - 需要**最小化**（或最大化）某个“最长/最短”属性，且属性可以通过**窗口检查**来判定。  
  - 需要**动态区间查询**（如 GCD、最大、最小）并且**点修改**频繁。  
  - 典型题目例子：  
    1. *Maximum Subarray Length With Limited Sum*（二分 + 前缀和 + 贪心）  
    2. *Minimum Number of Moves to Make Array Complementary*（二分 + 区间计数）  
    3. *Maximum Subarray With Bounded GCD*（二分 + 线段树）  

- **一句话总结**：  
  *把「最长稳定子数组 ≤ L」转化为「每个长度 L+1 的窗口都被一次右端改动覆盖」的贪心覆盖问题，用线段树快速检查 GCD，再配合二分搜索即可得到最小可能的稳定因子。*

---

## 反思  

- **第一反应**：看到「最长」+「最多改 maxC 次」直觉是枚举改动或动态规划，结果忽略了「窗口」的结构，使思路陷入高维状态空间。  
- **最容易踩的坑**：  
  1. **忘记把改动后的数设成 1**，导致后续窗口仍然可能出现 GCD≥2，误判可行性。  
  2. **边界处理**：当 `L = 0` 时窗口大小为 1，需要特殊检查每个元素是否已经是 1。实现时循环范围 `range(L, n)` 正好覆盖所有窗口。  
  3. **溢出/负数**：GCD 本身对负数有定义，但题目保证正数，仍然建议在更新时使用 `abs` 防御。  
- **下次类似题目**：  
  1. **先判断是否可以二分**：问题是否在「最小化最大值」或「最大化最小值」的形式。  
  2. **把判定条件转化为「每个固定长度窗口」的属性**，看能否用贪心覆盖。  
  3. **选择合适的数据结构**（线段树、树状数组、RMQ）来支持判定中的快速区间查询和点更新。  

这样一步步拆解，就能把看似 “Hard” 的题目化繁为简，写出既高效又易于理解的解法。祝你玩得开心，算法之路越走越宽！