# #2208. 将数组和减半的最少操作次数 / Minimum Operations to Halve Array Sum

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-halve-array-sum/)

---

## 题目（英文原版）

**Description**

You are given an array nums of positive integers. In one operation, you can choose any number from nums and reduce it to exactly half the number. (Note that you may choose this reduced number in future operations.)
Return the minimum number of operations to reduce the sum of nums by at least half.

**Examples**

**Example 1:**

```
Input: nums = [5,19,8,1]
Output: 3
Explanation: The initial sum of nums is equal to 5 + 19 + 8 + 1 = 33.
The following is one of the ways to reduce the sum by at least half:
Pick the number 19 and reduce it to 9.5.
Pick the number 9.5 and reduce it to 4.75.
Pick the number 8 and reduce it to 4.
The final array is [5, 4.75, 4, 1] with a total sum of 5 + 4.75 + 4 + 1 = 14.75. 
The sum of nums has been reduced by 33 - 14.75 = 18.25, which is at least half of the initial sum, 18.25 >= 33/2 = 16.5.
Overall, 3 operations were used so we return 3.
It can be shown that we cannot reduce the sum by at least half in less than 3 operations.
```

**Example 2:**

```
Input: nums = [3,8,20]
Output: 3
Explanation: The initial sum of nums is equal to 3 + 8 + 20 = 31.
The following is one of the ways to reduce the sum by at least half:
Pick the number 20 and reduce it to 10.
Pick the number 10 and reduce it to 5.
Pick the number 3 and reduce it to 1.5.
The final array is [1.5, 8, 5] with a total sum of 1.5 + 8 + 5 = 14.5. 
The sum of nums has been reduced by 31 - 14.5 = 16.5, which is at least half of the initial sum, 16.5 >= 31/2 = 15.5.
Overall, 3 operations were used so we return 3.
It can be shown that we cannot reduce the sum by at least half in less than 3 operations.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 107

---

## 题目（中文翻译）

**题目描述**

给定一个由正整数构成的数组 `nums`。一次 **操作（operation）** 可以选择 `nums` 中的任意一个数，并将其减半（即精确地变为原来的一半）。**注意**：在后续的操作中，你仍然可以选择已经被减半的数继续操作。

返回使 `nums` 的 **和（sum）** 至少减小一半所需的最少操作次数。

**示例 1**

> **输入**  
> `nums = [5,19,8,1]`  
> **输出**  
> `3`  
> **解释**  
> 初始数组的和为 `5 + 19 + 8 + 1 = 33`。以下是一种使和至少减半的操作序列：  
> 1. 选取数字 `19`，将其减半得到 `9.5`。  
> 2. 选取数字 `9.5`，再将其减半得到 `4.75`。  
> 3. 选取数字 `8`，将其减半得到 `4`。  
> 最终数组为 `[5, 4.75, 4, 1]`，其和为 `5 + 4.75 + 4 + 1 = 14.75`，已经不超过原和的一半 (`33 / 2 = 16.5`)。

**示例 2**

> **输入**  
> `nums = [3,8,20]`  
> **输出**  
> `3`  
> **解释**  
> 初始数组的和为 `3 + 8 + 20 = 31`。以下是一种使和至少减半的操作序列：  
> 1. 选取数字 `20`，将其减半得到 `10`。  
> 2. 选取数字 `10`，再将其减半得到 `5`。  
> 3. 选取数字 `3`，将其减半得到 `1.5`。  
> 最终数组为 `[1.5, 8, 5]`，其和为 `1.5 + 8 + 5 = 14.5`，已经不超过原和的一半 (`31 / 2 = 15.5`)。

**约束条件**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^7`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**每一次都遍历整个数组，找到当前最大的数，拿它减半**，然后把数组的和更新，直到总和 ≤ 原来的一半为止。  

- **使用的数据结构**：普通的 Python 列表 `list`。我们把它想象成一排排的商品，想要找最贵的商品就得一个个去称价，最慢的办法就是把所有商品都拿出来比较一次。  
- **为什么它是对的**：题目里已经说明“把最大的数减半是最优的”，所以只要每一步都挑最大的数，最终的操作次数一定是最少的。只要我们能够**正确地挑出最大的数**，不管怎么挑，最终都能达到目标。  
- **时间/空间复杂度**：  
  - 每一次操作我们都要遍历一遍数组寻找最大值，这一步的时间是 `O(n)`（`n` 为数组长度）。  
  - 最坏情况下我们可能需要做 `O(n·logS)` 次操作（`S` 为原始总和），因为每次至少把某个数除以 2，直到总和降到原来的一半。这里不必精确，只要知道次数会比 `n` 多很多。  
  - 因此总时间复杂度大约是 `O(n * 操作次数)`，在最坏情况下会接近 `O(n²)`。  
  - 只用了原数组本身，没有额外的数据结构，空间复杂度是 `O(1)`。

> **大白话解释**：`O(n²)` 可以想象成“把 100 本书每本都读 100 次”，显然很慢。

#### 代码（Python）

```python
def min_operations_brute(nums):
    """
    暴力解法：每次遍历找最大值并减半，直到总和降到原来的一半。
    """
    total = sum(nums)                 # 原始总和
    target = total / 2.0              # 目标是原来的一半
    ops = 0                           # 记录操作次数

    while total > target:             # 只要还没有达到目标就继续
        # 线性扫描找最大元素的下标
        max_idx = 0
        for i in range(1, len(nums)):
            if nums[i] > nums[max_idx]:
                max_idx = i

        # 把找到的最大元素减半
        reduction = nums[max_idx] / 2.0
        nums[max_idx] = reduction      # 更新数组中的值
        total -= reduction              # 总和相应减少
        ops += 1                        # 操作次数加一

    return ops
```

#### 复杂度

- **时间复杂度**：`O(n * k)`，其中 `k` 为实际需要的操作次数。最坏情况下接近 `O(n²)`，因为每次都要遍历整个数组寻找最大值。  
- **空间复杂度**：`O(1)`，只在原数组上原地修改，没有额外的存储。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要线性扫描找最大元素**，这一步耗时最多。我们可以把“找最大”这件事交给一种**专门支持快速取最大值的数据结构**——**最大堆（max‑heap）**（在 Python 中用 `heapq` 的负数技巧实现）。

**核心优化步骤**：

1. **把所有数字放进最大堆**。堆是一棵完全二叉树，根节点始终是当前最大的元素。插入 `n` 个数的代价是 `O(n)`（一次性建堆）或 `O(n log n)`（逐个插入），这里我们直接用 `heapify`。
2. **每次弹出堆顶（最大数），把它减半后再放回堆**。弹出和插入的代价都是 `O(log n)`，因为堆的高度是 `log n`。
3. **累计已经减少的总和**，一旦累计的减少量 ≥ 原始总和的一半，停止循环。  

**为什么只要每次处理最大的数就一定最优**：

- 把一个数 `x` 减半能贡献的“减量”是 `x/2`。如果我们把一个更小的数 `y < x` 减半，它能贡献的减量只有 `y/2`，显然不如把 `x` 减半来的多。  
- 题目已经给出提示：“It is always optimal to halve the largest element.” 这相当于数学上的 **贪心选择性质**：每一步的局部最优（选最大）能够导向全局最优。

**类比**：想象有一堆重量不等的箱子，要把总重量减到原来的一半。每次我们都挑最重的箱子拆成两半，拆掉一半的重量，这样最省力。

#### 代码（Python）

```python
import heapq

def min_operations(nums):
    """
    最优解：使用最大堆（通过负数实现）贪心地每次把最大的数减半。
    """
    total = sum(nums)                 # 原始总和
    target = total / 2.0              # 目标是原来的一半
    ops = 0                           # 操作次数

    # Python 的 heapq 是最小堆，取负数即可得到最大堆
    max_heap = [-x for x in nums]     # 把所有数取负放进列表
    heapq.heapify(max_heap)           # O(n) 建堆

    reduced = 0.0                     # 已经累计减少的总和

    while reduced < target:           # 只要累计减量不足目标就继续
        # 取出当前最大的数（因为是负数，所以取负号恢复正数）
        largest = -heapq.heappop(max_heap)   # O(log n)
        half = largest / 2.0                  # 减半后的新值
        reduced += largest - half              # 本次真正减少的量
        heapq.heappush(max_heap, -half)        # 把减半后的数重新放回堆，保持负号
        ops += 1                               # 操作次数加一

    return ops
```

#### 复杂度

- **时间复杂度**：`O(k log n)`，其中 `k` 为实际执行的操作次数。每一次弹出和插入都只需要 `log n` 的时间。因为每次至少把某个数减半，`k` 最多是 `O(log(max(nums)))` 乘以 `n`，在题目约束下非常快。  
  - 与暴力解相比，`log n`（比如 `log 10⁵ ≈ 17`）远小于 `n`（最多 10⁵），所以速度提升几个数量级。  
- **空间复杂度**：`O(n)`，需要额外存放一个大小为 `n` 的堆（相当于复制了一遍数组），这在题目限制内完全可接受。

---

## 心得

- **核心技巧**：**贪心 + 最大堆**。每次优先处理当前最大的元素，利用堆快速获取最大值。
- **适用的题型**  
  1. “把数组总和减到某个阈值” 类似题（如 *Minimum Operations to Reduce X to Zero*）。  
  2. “每次取最大/最小进行合并或分割” 的问题（如 *Minimum Cost to Connect Sticks*、*Find Kth Largest Element in an Array*）。  
- **解题钥匙**：**“把最能‘贡献’的那件事先做”** → 用堆把最大（或最小）元素快速找出来。

---

## 反思

- **第一反应**：看到“把数减半”，本能想到“一次一次遍历找最大”。这其实已经是正确的思路，只是实现方式不够高效。
- **最容易踩的坑**  
  - **浮点数误差**：减半会产生小数，累计的 `reduced` 需要使用 `float`，比较时直接用 `<` 即可，避免因精度导致的无限循环。  
  - **忘记把减半后的数重新放回堆**：如果不放回，后面的操作就只能在已经减半的数上进行，导致结果不正确。  
  - **边界条件**：当数组只有一个元素且已经小于目标的一半时，循环应直接结束，返回 `0`。
- **下次类似题的第一步**：先判断**是否有“每次都需要取极值（最大/最小）”的需求**，如果有，就立刻想到使用**堆**（或有序集合）来提升效率。