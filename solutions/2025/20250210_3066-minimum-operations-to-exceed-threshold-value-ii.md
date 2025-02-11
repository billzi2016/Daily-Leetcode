# #3066. 最小操作次数使所有元素不小于阈值 II / Minimum Operations to Exceed Threshold Value II

> 难度：中等 · 标签：Array、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-exceed-threshold-value-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums, and an integer k.
You are allowed to perform some operations on nums, where in a single operation, you can:
Note that you can only apply the described operation if nums contains at least two elements.
Return the minimum number of operations needed so that all elements of the array are greater than or equal to k.

**Examples**

**Example 1:**

```
Input: nums = [2,11,10,1,3], k = 10
Output: 2
Explanation:
At this stage, all the elements of nums are greater than or equal to 10 so we can stop.
It can be shown that 2 is the minimum number of operations needed so that all elements of the array are greater than or equal to 10.
```

**Example 2:**

```
Input: nums = [1,1,2,4,9], k = 20
Output: 4
Explanation:
At this stage, all the elements of nums are greater than 20 so we can stop.
It can be shown that 4 is the minimum number of operations needed so that all elements of the array are greater than or equal to 20.
```

**Constraints**

- 2 <= nums.length <= 2 * 105
- 1 <= nums[i] <= 109
- 1 <= k <= 109
- The input is generated such that an answer always exists. That is, after performing some number of operations, all elements of the array are greater than or equal to k.

---

## 题目（中文翻译）

You are given a 0-indexed integer array `nums`, and an integer `k`.  
You are allowed to perform some operations on `nums`, where in a single operation, you can:  
*（此处原题给出的操作描述略去）*  

**Note that you can only apply the described operation if `nums` contains at least two elements.**  

Return the minimum number of operations needed so that all elements of the array are greater than or equal to `k`.

#### 示例

**示例 1**  
```text
Input: nums = [2,11,10,1,3], k = 10
Output: 2
Explanation:
At this stage, all the elements of nums are greater than or equal to 10 so we can stop.
It can be shown that 2 is the minimum number of operations needed so that all elements of the array are greater than or equal to 10.
```

**示例 2**  
```text
Input: nums = [1,1,2,4,9], k = 20
Output: 4
Explanation:
At this stage, all the elements of nums are greater than 20 so we can stop.
It can be shown that 4 is the minimum number of operations needed so that all elements of the array are greater than or equal to 20.
```

#### 约束条件
- `2 <= nums.length <= 2 * 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= 10^9`
- The input is generated such that an answer always exists. That is, after performing some number of operations, all elements of the array are greater than or equal to `k`.

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：每一次操作都从数组里找出 **最小的两个数** `a` 与 `b`（把数组想象成一堆小石子，最小的两块石子最容易被挑出来），  
然后按照题目要求把它们合并成 `a + 2 * b`，再把得到的数放回数组。  

- **数据结构**：我们只用 Python 的普通 `list`，用 `min()` 去遍历一次找最小值，类似在字典里查词条——一次遍历才能找到“最小的词”。  
- **正确性**：因为题目只限制“每次只能选最小的两个”，只要我们每一步都真的挑出最小的两个人，操作顺序就和题目要求完全一致，最终得到的数组一定是合法的。  

**为什么会慢**：  
每一次挑最小的两个都要遍历整个数组一次（`O(n)`），而一次操作会把数组长度减 1，最多要进行 `n‑1` 次操作，所以总时间是 `O(n + (n‑1) + … + 1) = O(n²)`。  
对于 `n` 高达 `2·10⁵` 的数据，这个 quadratic（平方）级别的耗时根本不可接受。

#### 代码（Python）

```python
def min_operations_bruteforce(nums, k):
    """
    暴力版：每次都遍历数组找最小的两个数
    """
    ops = 0                     # 记录操作次数
    while True:
        # 检查所有元素是否已经 >= k
        if all(x >= k for x in nums):
            return ops

        # 找最小的两个数的下标
        # 第一次遍历找最小值
        min1_idx = min2_idx = -1
        for i, v in enumerate(nums):
            if min1_idx == -1 or v < nums[min1_idx]:
                min2_idx = min1_idx   # 原来的最小变成第二小
                min1_idx = i
            elif min2_idx == -1 or v < nums[min2_idx]:
                min2_idx = i

        a, b = nums[min1_idx], nums[min2_idx]
        new_val = a + 2 * b          # 按题目规则合并

        # 把两个数从列表中移除（先删下标大的，防止索引错位）
        for idx in sorted([min1_idx, min2_idx], reverse=True):
            nums.pop(idx)

        nums.append(new_val)         # 把新数放回数组
        ops += 1
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  大白话：如果数组有 10 万个数，粗略估计要做 10 万次遍历，每次遍历又要看 10 万个数，时间会像 10 万 × 10 万 那么大，几乎不可能在一秒内跑完。

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  只用了几个额外的变量来记录下标和新值，和数组大小无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**瓶颈在于每次都要线性扫描去找最小的两个数**。  
如果我们能把“随时拿出最小的两个数”这件事的代价降低到 **对数级别**，整体速度就会快很多。  

这正是 **优先队列（最小堆）** 的强项：  
- 堆是一棵完全二叉树，根节点总是当前最小的元素。  
- `heappop()` 可以 **O(log n)** 时间弹出最小元素，`heappush()` 同样是 **O(log n)** 把新元素放进去。  

**步骤**：

1. 把所有 `nums` 放进最小堆（相当于把所有石子排好队，最小的石子自然站在最前面）。  
2. 循环检查堆顶（最小元素）是否已经 `>= k`。如果是，说明所有元素都达标，返回操作次数。  
3. 否则弹出堆中最小的两个数 `a` 与 `b`，计算 `a + 2 * b`，再把结果压回堆中。  
4. 计数器 `ops` 加一，继续下一轮。  

因为每次操作都把数组长度减 1，最多进行 `n‑1` 次，而每次弹出/插入的代价是 `log n`，所以总时间是 `O(n log n)`，完全可以接受。

**为什么一定能得到答案**：  
题目保证“答案一定存在”。每次合并都会产生一个 **不小于** 两个原数中较大的那个（因为 `a + 2*b >= b`），所以堆中最大的数不会变小，最终一定能把所有小于 `k` 的数合并成足够大的数。

#### 代码（Python）

```python
import heapq

def min_operations(nums, k):
    """
    最优解：使用最小堆（优先队列）高效地获取最小的两个数
    """
    # 1. 把所有元素建成最小堆
    heapq.heapify(nums)          # O(n)

    ops = 0                       # 已经进行的操作次数

    # 2. 当堆顶元素仍然小于 k 时，需要继续合并
    while nums[0] < k:            # 只要最小的还不够，就一定还有别的也不够
        a = heapq.heappop(nums)   # 取出最小的 a   O(log n)
        b = heapq.heappop(nums)   # 取出次小的 b   O(log n)

        new_val = a + 2 * b       # 按题目规则合并
        heapq.heappush(nums, new_val)  # 把新数放回堆   O(log n)

        ops += 1

    return ops
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 建堆 `O(n)`（一次性把所有数放进堆）。  
  - 每次操作弹出两次、插入一次，都是 `log n`，最多 `n‑1` 次操作。  
  - 用大白话讲，就是“每次只需要找最小的两块石子，花的时间和石子总数的对数成正比”，远比每次遍历全体石子快得多。

- **空间复杂度**：`O(n)`  
  - 堆本身需要存放所有元素，和原数组大小相同。额外的变量只占常数空间。

---

## 心得

- **核心技巧**：使用 **最小堆（优先队列）** 来在动态变化的集合中快速获取最小的两个元素。  
- **适用题型**  
  1. “合并最小的两个数” 类问题，例如 **Minimum Cost to Connect Sticks**、**Combine Stones**。  
  2. 需要不断取出极值并重新插入的模拟题，如 **Find K Pairs with Smallest Sums**。  
- **一句话总结**：**堆让“每次找最小的两个数”从线性降到对数，是本题的解题钥匙。**

---

## 反思

- **第一反应**：直接写循环遍历找最小值，觉得代码好写，没意识到会超时。  
- **最容易踩的坑**  
  - **忘记检查堆是否为空**：当只剩一个元素时，仍需判断它是否已经 ≥ k。  
  - **合并顺序错误**：必须每次都取 **当前** 最小的两个数，不能随意选。  
  - **整数溢出**：在其他语言里 `a + 2*b` 可能超过 32 位，需要用 64 位整数；Python 自动大整数所以不怕。  
- **下次类似题的第一步**：**先想能不能用堆（或其他能快速取极值的数据结构）**，把“每次找最小/最大”这一步的时间复杂度降下来。这样往往能直接把暴力的 `O(n²)` 提升到 `O(n log n)`，轻松通过大数据规模的限制。