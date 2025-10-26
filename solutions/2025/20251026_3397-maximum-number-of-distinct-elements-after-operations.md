# #3397. 操作后不同元素的最大数量 / Maximum Number of Distinct Elements After Operations

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-distinct-elements-after-operations/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
You are allowed to perform the following operation on each element of the array at most once:
Return the maximum possible number of distinct elements in nums after performing the operations.

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,3,3,4], k = 2
Output: 6
Explanation:
nums changes to [-1, 0, 1, 2, 3, 4] after performing operations on the first four elements.
```

**Example 2:**

```
Input: nums = [4,4,4,4], k = 1
Output: 3
Explanation:
By adding -1 to nums[0] and 1 to nums[1] , nums changes to [3, 5, 4, 4] .
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 0 <= k <= 109

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数 `k`。  
你被允许对数组中的每个元素至多执行一次以下操作：  

返回在执行完操作后，`nums` 中可能的**不同元素（distinct elements）**的最大数量。

## 示例

### 示例 1
**输入**  
`nums = [1,2,2,3,3,4]`, `k = 2`

**输出**  
`6`

**解释**  
在对前四个元素执行操作后，`nums` 变为 `[-1, 0, 1, 2, 3, 4]`。

### 示例 2
**输入**  
`nums = [4,4,4,4]`, `k = 1`

**输出**  
`3`

**解释**  
通过对 `nums[0]` 加 `-1`、对 `nums[1]` 加 `1`，`nums` 变为 `[3, 5, 4, 4]`。

## 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个数的所有可能取值列举出来**，再在这些候选集合里挑选出尽可能多的不同值。  

- **每个元素的取值范围**：`nums[i]` 可以在 `[ nums[i]‑k , nums[i]‑k+1 , … , nums[i] , … , nums[i]+k ]` 之间任选一个（相当于在原数上加上一个介于 `‑k` 到 `k` 的整数）。可以把这看成“每个数都有一把钥匙，钥匙可以在它所在的区间里随意挑一个锁”。  
- **暴力枚举**：把所有元素的钥匙都拔出来，尝试所有可能的组合。对第 `i` 个元素有 `2k+1` 种选择，`n` 个元素就会产生 `(2k+1)^n` 种组合。  
- **为什么正确**：只要枚举到了所有可能的组合，必然能找到一种使得不同钥匙（数值）最多的方案。  

显然，这种方法在 `n` 甚至 `k` 稍大一点时就会爆炸，根本跑不完。

#### 代码（Python）  

```python
from itertools import product

def maxDistinct_bruteforce(nums, k):
    """
    暴力枚举所有可能的取值组合（仅用于说明，实际会超时）。
    """
    # 为每个元素生成它的所有候选值（长度为 2k+1）
    candidates = [list(range(x - k, x + k + 1)) for x in nums]

    best = 0                     # 记录最大不同数的个数
    # product 会产生笛卡尔积，即所有可能的取值方案
    for choice in product(*candidates):
        distinct_cnt = len(set(choice))   # set 自动去重，计数
        best = max(best, distinct_cnt)

    return best
```

> **关键行解释**  
> - `range(x - k, x + k + 1)`：把 `x` 能变成的所有整数列出来。  
> - `product(*candidates)`：把每个元素的候选列表做笛卡尔积，相当于把每把钥匙都插进每个可能的锁里。  
> - `set(choice)`：把选出的数去重，`len` 就是不同数的个数。

#### 复杂度  

- **时间复杂度**：`O((2k+1)^n)` —— 每个元素有 `2k+1` 种取法，全部组合要指数级遍历。  
- **空间复杂度**：`O(n·k)` 用于存放每个元素的候选列表（其实主要是递归栈/迭代器的开销）。

> **大白话解释**：如果 `k=1`，每个数有 3 种可能；`n=10` 时组合数是 `3^10 ≈ 59000`，已经不算小了；`k=10、n=20` 时组合数直接冲到 `21^20`，根本不可能在电脑上算完。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的难点是“如何把每个数的取值区间安排得不冲突”**。  
我们不需要枚举所有组合，只要**把每个区间尽可能早地占用一个还没有被占的整数**，就能保证最终的不同数目最多。  

**关键观察**  

1. **区间左端点越小，越应该优先安排**。因为左端点小的区间“可选的整数”更少，晚安排可能被后面的区间抢走。  
2. **一次只占用最小的可用整数**。如果我们把一个区间占成了更大的数，后面的区间仍然可以使用更小的数，这样会浪费掉本可以用的小数。  

基于这两个观察，我们可以采用**贪心 + 排序**的思路：

1. 把所有元素的区间 `[nums[i]-k , nums[i]+k]` 按左端点（即 `nums[i]-k`）从小到大排序。  
2. 维护一个变量 `last`，表示**已经占用的最大整数**（初始设为负无穷）。  
3. 依次遍历排好序的区间：  
   - 计算本区间可以使用的最小整数 `candidate = max(last + 1, left)`，其中 `left = nums[i] - k`。  
   - 如果 `candidate <= right (= nums[i] + k)`，说明我们还能在这个区间里找一个未被占用的整数，于是把它占掉，`last = candidate`，答案加 1。  
   - 否则，这个区间已经没有空位，只能放弃（对应的元素只能和已有的某个数相同，不能再贡献新的不同数）。  

这样，每个区间只检查一次，整体是线性的。

> **类比**：把每个区间想象成一条“停车位”，`left` 是这条线的起点，`right` 是终点。我们把车子从左往右依次停进去，每次都把车停在离已经停好的车最近的空位上，这样可以让后面的车有更多空间。

#### 代码（Python）

```python
def maxDistinct(nums, k):
    """
    贪心 + 排序：在每个可变区间里占用最左侧未被占用的整数。
    返回最多可以得到的不同元素个数。
    """
    # 1. 把所有区间的左端点、右端点算出来并排序
    intervals = sorted((x - k, x + k) for x in nums)   # 按 left 从小到大排

    last_used = -10**20        # 已占用的最大整数，设一个足够小的初始值
    distinct_cnt = 0

    for left, right in intervals:
        # 2. 计算本区间能占的最小整数（必须大于已经占用的最大数）
        candidate = max(last_used + 1, left)

        # 3. 判断 candidate 是否仍在区间范围内
        if candidate <= right:
            distinct_cnt += 1          # 成功占到一个新数
            last_used = candidate      # 更新已占用的最大数

    return distinct_cnt
```

> **关键行解释**  
> - `sorted((x - k, x + k) for x in nums)`：把每个数的“可变区间”先算出来，再按左端点升序排好。  
> - `candidate = max(last_used + 1, left)`：我们想要的数既不能比已经占的最大数小（否则会冲突），又不能比区间左端点小（超出允许范围），于是取两者的较大值。  
> - `if candidate <= right:`：只要这个数还在区间的右端点以内，就说明可以成功占一个新位置。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`，主要来自对 `n` 个区间的排序。遍历本身是 `O(n)`。  
- **空间复杂度**：`O(n)` 用于存放排好序的区间（如果在原地排序可以降到 `O(1)`，但对初学者保持 `O(n)` 更易理解）。  

> **对比暴力**：暴力是指数级的 `O((2k+1)^n)`，根本不可接受；而贪心只需要一次排序，能够轻松处理 `10^5` 规模的数据。

---

## 心得  

- **核心技巧**：**区间贪心**——把每个元素的可取值看成一个闭区间，按左端点升序处理，每次占用区间中**最左侧尚未被占用的整数**。  
- **适用的题型**：  
  1. “给定若干区间，最多可以选多少个不相交的点？”（如 LeetCode 435 “Non-overlapping Intervals” 的变形）  
  2. “把每个数向左或向右移动一定距离，使得数组中不同元素最多”这类**离散化 + 贪心**的问题。  
  3. “给定若干任务的开始/结束时间，如何安排尽可能多的任务”——同样可以用按左端点排序的思路。  
- **一句话总结**：**把每个数的可变范围当作一段路，先让最早的路抢占最左边的空位，剩下的路才有机会继续往后走**。

---

## 反思  

- **第一反应**：把每个数能变成的所有值列出来，尝试所有组合——这自然是最直观的做法，却忽视了规模。  
- **最容易踩的坑**：  
  - 忘记 **每个元素只能改一次**，但可以向左或向右任意移动 `≤ k`，所以不是只能取 `num‑k、num、num+k` 三个值。  
  - 直接用 `set` 去重而不考虑区间冲突，会得到错误的最大值（因为可能出现两个区间只能选同一个数的情况）。  
  - 处理负数时要注意左端点可能小于 0，不能把负数误认为“不合法”。本题允许负数。  
- **下次类似题的第一步**：**把可选范围抽象成区间**，看能否通过**排序 + 贪心**一次遍历得到最优解。  

祝你玩转贪心，算法路上越走越宽！