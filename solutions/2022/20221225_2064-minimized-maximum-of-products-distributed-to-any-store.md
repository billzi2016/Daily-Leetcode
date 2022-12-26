# #2064. 最小化任意商店分配的产品最大数量 / Minimized Maximum of Products Distributed to Any Store

> 难度：中等 · 标签：Array、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimized-maximum-of-products-distributed-to-any-store/)

---

## 题目（英文原版）

**Description**

You are given an integer n indicating there are n specialty retail stores. There are m product types of varying amounts, which are given as a 0-indexed integer array quantities, where quantities[i] represents the number of products of the ith product type.
You need to distribute all products to the retail stores following these rules:
Return the minimum possible x.

**Examples**

**Example 1:**

```
Input: n = 6, quantities = [11,6]
Output: 3
Explanation: One optimal way is:
- The 11 products of type 0 are distributed to the first four stores in these amounts: 2, 3, 3, 3
- The 6 products of type 1 are distributed to the other two stores in these amounts: 3, 3
The maximum number of products given to any store is max(2, 3, 3, 3, 3, 3) = 3.
```

**Example 2:**

```
Input: n = 7, quantities = [15,10,10]
Output: 5
Explanation: One optimal way is:
- The 15 products of type 0 are distributed to the first three stores in these amounts: 5, 5, 5
- The 10 products of type 1 are distributed to the next two stores in these amounts: 5, 5
- The 10 products of type 2 are distributed to the last two stores in these amounts: 5, 5
The maximum number of products given to any store is max(5, 5, 5, 5, 5, 5, 5) = 5.
```

**Example 3:**

```
Input: n = 1, quantities = [100000]
Output: 100000
Explanation: The only optimal way is:
- The 100000 products of type 0 are distributed to the only store.
The maximum number of products given to any store is max(100000) = 100000.
```

**Constraints**

- m == quantities.length
- 1 <= m <= n <= 105
- 1 <= quantities[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`，表示有 `n` 家专营零售店 (specialty retail stores)。还有 `m` 种不同的产品类型 (product types)，其数量由下标从 0 开始的整数数组 `quantities` 给出，其中 `quantities[i]` 表示第 `i` 种产品的总数量。

需要将所有产品分配给这些零售店，满足以下规则：

1. 每个店只能收到同一种产品类型的产品。  
2. 同一种产品可以分配到多个店，每个店收到的该产品数量可以不同。  
3. 所有产品必须全部分配完。

返回能够使 **任意一家店所收到的产品数量的最大值** 最小化的可能的 `x`。

**示例**

> 示例 1  
> 输入: `n = 6`, `quantities = [11,6]`  
> 输出: `3`  
> 解释: 一种最优分配方式为：  
> - 第 0 种产品的 11 件分配给前四家店，分别为 `2, 3, 3, 3` 件；  
> - 第 1 种产品的 6 件分配给后两家店，分别为 `3, 3` 件。  
> 此时任意一家店收到的产品数量的最大值为 `max(2, 3, 3, 3, 3, 3) = 3`。

> 示例 2  
> 输入: `n = 7`, `quantities = [15,10,10]`  
> 输出: `5`  
> 解释: 一种最优分配方式为：  
> - 第 0 种产品的 15 件分配给前三家店，分别为 `5, 5, 5` 件；  
> - 第 1 种产品的 10 件分配给接下来的两家店，分别为 `5, 5` 件；  
> - 第 2 种产品的 10 件分配给最后两家店，分别为 `5, 5` 件。  
> 此时任意一家店收到的产品数量的最大值为 `5`。

> 示例 3  
> 输入: `n = 1`, `quantities = [100000]`  
> 输出: `100000`  
> 解释: 唯一的分配方式是将全部 `100000` 件第 0 种产品分配给唯一的那家店。  
> 最大值为 `max(100000) = 100000`。

**约束条件**

- `m == quantities.length`
- `1 <= m <= n <= 10^5`
- `1 <= quantities[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的最大商店负荷 `x`**，然后判断在这个 `x` 下能否把所有商品分配完。  
- **枚举范围**：`x` 至少要是 1（最小可能），最多不超过所有商品里最多的那种数量 `max(quantities)`，因为如果 `x` 大于这个数，显然所有商品都能直接装进一个店。
- **判断方式**：对每一种商品 `i`，如果每家店最多只能装 `x` 件，那么这种商品至少需要 `ceil(quantities[i] / x)` 家店。把所有商品需要的店数加起来，看看是否 **不超过** 总店数 `n`。  
  - 这里的 `ceil` 可以想象成 “把一本厚厚的词典分成若干本薄薄的小册子，每本最多装 `x` 页，最后需要多少本？”  
- **如果** 所需的店数 ≤ `n`，说明 `x` 能够满足要求；否则 `x` 太小，必须增大。

**为什么这个方法一定正确**  
因为我们穷举了所有可能的最大负荷 `x`，只要找到一个 `x` 能让所有商品在不超过 `n` 家店的前提下分配完，它就是一个可行解；最小的那一个就是答案。

#### 代码（Python）

```python
import math
from typing import List

def minmaxProducts_bruteforce(n: int, quantities: List[int]) -> int:
    # 1. 可能的最大负荷从 1 到 max(quantities) 逐个尝试
    max_q = max(quantities)
    for x in range(1, max_q + 1):          # 这里是暴力枚举
        needed = 0                         # 记录当前 x 需要的店数
        for q in quantities:
            # 每种商品至少要 ceil(q / x) 家店才能装完
            needed += math.ceil(q / x)     # 类比：把一本厚书拆成每本最多 x 页的小册子
        if needed <= n:                    # 如果店数不超 n，说明 x 可行
            return x                       # 第一个可行的 x 就是最小的
    return max_q                           # 理论上永远不会走到这里
```

#### 复杂度

- **时间复杂度**：`O(max(quantities) * m)`  
  - `max(quantities)` 可能高达 `10⁵`，`m`（商品种类数）最多 `10⁵`，所以最坏会是 `10¹⁰` 次运算，实际会超时。  
  - 用大白话说，就是“把所有可能的答案一个一个尝试”，每次都要遍历所有商品，显得非常慢。
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（`needed`、`x` 等），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于“逐个枚举 `x`”。  
观察 `canDistribute(x)`（判断 `x` 能否分配完）这件事的**单调性**：

- 当 `x` **增大** 时，每种商品需要的店数 `ceil(q / x)` **不增**（可能会减），所以 `needed` 单调 **不增**。  
- 换句话说：如果某个 `x` 已经可以分配完，那么所有更大的 `x` 也一定可以分配完；反之，如果 `x` 不能分配完，那么所有更小的 `x` 也一定不行。

这正好符合 **二分查找** 的使用前提：答案在一个有序（单调）区间里，左侧是“不行”，右侧是“可以”。  
因此我们可以：

1. 设定搜索区间 `[lo, hi]`，其中 `lo = 1`（最小可能），`hi = max(quantities)`（最大可能）。  
2. 每次取中点 `mid = (lo + hi) // 2`，用 `canDistribute(mid)` 检查可行性。  
   - 如果 `mid` 可行 → 把右边界收紧到 `mid`（因为我们想要更小的答案）。  
   - 如果 `mid` 不可行 → 把左边界提升到 `mid + 1`（因为更小的 `mid` 更不可能）。  
3. 循环结束时 `lo == hi`，此时的 `lo`（或 `hi`）就是最小的可行 `x`。

**核心工具：`canDistribute(k)`**  

```python
def canDistribute(k: int) -> bool:
    needed = sum((q + k - 1) // k for q in quantities)  # (q + k - 1) // k == ceil(q/k)
    return needed <= n
```

- 这里的 `(q + k - 1) // k` 是整数除法实现 `ceil`，避免使用浮点数和 `math.ceil`，更快也更安全。  
- 这一步相当于 “把每本厚书拆成每本最多 k 页的小册子”，算出所有小册子总数是否 ≤ `n`。

#### 代码（Python）

```python
from typing import List

def minmaxProducts(n: int, quantities: List[int]) -> int:
    """
    二分查找最小的最大负荷 x，使得所有商品都能在不超过 n 家店的前提下分配完。
    """
    # ---------- 辅助函数：判断给定的上限 k 能否完成分配 ----------
    def canDistribute(k: int) -> bool:
        # 对每种商品，所需的店数 = ceil(q / k) = (q + k - 1) // k
        needed = 0
        for q in quantities:
            needed += (q + k - 1) // k   # 关键行：整数除法实现向上取整
            # 如果已经超出 n，提前返回 False，省去后面的循环
            if needed > n:
                return False
        return True                     # 所需店数不超过 n，说明 k 可行

    lo, hi = 1, max(quantities)          # 搜索区间的左右边界
    while lo < hi:                       # 只要区间长度大于 1，就继续二分
        mid = (lo + hi) // 2
        if canDistribute(mid):           # mid 能分配 → 向左收紧区间
            hi = mid
        else:                            # mid 不能分配 → 向右收紧区间
            lo = mid + 1
    return lo                             # lo == hi，即为答案
```

#### 复杂度

- **时间复杂度**：`O(m · log(max_q))`  
  - `log(max_q)` 大约是 `log₂(10⁵) ≈ 17`，所以即使 `m` 达到 `10⁵`，整体也只在几百万次循环之内，轻松跑完。  
  - 与暴力解相比，省去了对每一个可能的 `x` 的遍历，只在“二分的层数”上做检查，快了 **指数级**。
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量 `lo、hi、mid、needed`，不随输入规模增长。

---

## 心得

- **核心技巧**：利用单调性 + 二分查找把 “遍历所有可能” 转化为 “对数级别的查找”。  
- **适用场景**：  
  1. **分配类**问题——如“把若干任务分配给机器，使最大负载最小”。  
  2. **容量类**问题——如“在有限的容器里装物品，求最小容器容量”。  
  3. **阈值类**问题——如“找最小的速度，使得在限定时间内完成所有工作”。  
- **一句话总结**：**“先判断‘给定上限能否完成’，再二分逼近最小可行上限”。**

---

## 反思

- **拿到题目第一反应**：先想“把所有可能的最大负荷逐个试”，即暴力枚举。  
- **最容易踩的坑**：  
  - 忘记 **向上取整** (`ceil`) 会导致计算所需店数不足，从而误判 `k` 可行。  
  - 直接使用 `math.ceil` 会产生浮点数，可能出现精度或性能问题，最好用整数技巧 `(q + k - 1) // k`。  
  - 没有在 `canDistribute` 中提前退出，当 `needed` 已经大于 `n` 时仍继续循环，会导致不必要的时间浪费。  
- **下次遇到同类题**：第一步先思考“**给定一个阈值，能否检查可行性**”，如果可以 O(m) 检查，就立刻考虑二分搜索寻找最小阈值。这样往往能把指数级的暴力解直接压缩到对数级。