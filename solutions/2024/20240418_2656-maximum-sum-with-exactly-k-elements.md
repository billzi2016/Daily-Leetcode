# #2656. 恰好选取 K 个元素的最大和 / Maximum Sum With Exactly K Elements 

> 难度：简单 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-with-exactly-k-elements/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer k. Your task is to perform the following operation exactly k times in order to maximize your score:
Return the maximum score you can achieve after performing the operation exactly k times.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5], k = 3
Output: 18
Explanation: We need to choose exactly 3 elements from nums to maximize the sum.
For the first iteration, we choose 5. Then sum is 5 and nums = [1,2,3,4,6]
For the second iteration, we choose 6. Then sum is 5 + 6 and nums = [1,2,3,4,7]
For the third iteration, we choose 7. Then sum is 5 + 6 + 7 = 18 and nums = [1,2,3,4,8]
So, we will return 18.
It can be proven, that 18 is the maximum answer that we can achieve.
```

**Example 2:**

```
Input: nums = [5,5,5], k = 2
Output: 11
Explanation: We need to choose exactly 2 elements from nums to maximize the sum.
For the first iteration, we choose 5. Then sum is 5 and nums = [5,5,6]
For the second iteration, we choose 6. Then sum is 5 + 6 = 11 and nums = [5,5,7]
So, we will return 11.
It can be proven, that 11 is the maximum answer that we can achieve.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- 1 <= k <= 100

---

## 题目（中文翻译）

给定一个 **0-indexed**（从 0 开始索引）的整数数组 `nums` 和一个整数 `k`。你需要恰好执行 **k 次** 以下操作，以使你的得分（score）最大化：  
- 在每一次操作中，从 `nums` 中选择一个元素，将其加入当前得分，并将该元素的值加 1（即 `nums[i] = nums[i] + 1`）。  

返回恰好执行 **k 次** 操作后能够得到的最大得分。

---

### 示例

#### 示例 1
**输入**: `nums = [1,2,3,4,5]`, `k = 3`  
**输出**: `18`  
**解释**: 我们需要恰好选取 3 个元素，使总和最大。  
- 第一次迭代（iteration），选择 `5`。此时得分为 `5`，`nums` 变为 `[1,2,3,4,6]`。  
- 第二次迭代，选择 `6`。此时得分为 `5 + 6`，`nums` 变为 `[1,2,3,4,7]`。  
- 第三次迭代，选择 `7`。此时得分为 `5 + 6 + 7 = 18`，`nums` 变为 `[1,2,3,4,8]`。  
因此返回 `18`。

#### 示例 2
**输入**: `nums = [5,5,5]`, `k = 2`  
**输出**: `11`  
**解释**: 我们需要恰好选取 2 个元素，使总和最大。  
- 第一次迭代，选择 `5`。此时得分为 `5`，`nums` 变为 `[5,5,6]`。  
- 第二次迭代，选择 `6`。此时得分为 `5 + 6 = 11`，`nums` 变为 `[5,5,7]`。  
可以证明，`11` 是能够得到的最大答案。

---

### 约束条件
- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`
- `1 <= k <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**每一次都把当前数组里最大的数挑出来**，因为：

- 题目要求我们在每一步都把挑选的数加入得分，同时把它的值加 1。  
- 如果这一步挑了一个不是最大值的数 `x`，而把最大值 `M` 留到以后再挑，那么这一步我们只能得到 `x`（`x ≤ M`），而把 `M` 留到以后得到的分数最多也只能是 `M`（因为 `M` 只会在被挑选后才会变成 `M+1`）。  
- 换句话说，**把最大的数先挑走，立刻得到最大的即时收益，后面再挑其他数**，总得分一定不会比先挑小数再挑大的方案更差。  

所以，**每一步都选当前最大值** 就能得到最优答案。

实现上我们可以：

1. 维护原数组 `nums`。  
2. 在每一次操作中遍历整个数组，找到最大元素的下标 `idx`。  
3. 把 `nums[idx]` 加到答案 `ans` 中，并把 `nums[idx]` 加 1（模拟“选完后值加 1”）。  
4. 重复上述过程 `k` 次。

> **类比**：想象你在超市里挑水果，每次都挑最大的那个，因为它的价值最高，挑走后它的重量会再增加一点（相当于变得更大），所以下次再挑它也仍然是最大的。

#### 代码（Python）

```python
def max_score_bruteforce(nums, k):
    """
    暴力解：每次遍历数组找最大值
    时间复杂度：O(k * n)   （k 次遍历，每次 O(n)）
    空间复杂度：O(1)       （只使用常数级额外空间）
    """
    ans = 0                     # 累计得分
    n = len(nums)

    for _ in range(k):          # 正好进行 k 次操作
        # 1️⃣ 找到当前最大的数的下标
        max_idx = 0
        for i in range(1, n):
            if nums[i] > nums[max_idx]:
                max_idx = i

        # 2️⃣ 累加得分
        ans += nums[max_idx]

        # 3️⃣ 选完后把该元素加 1
        nums[max_idx] += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(k * n)`  
  - “`k` 次”指我们要做 `k` 次挑选。  
  - 每次挑选要遍历整个数组找最大值，遍历一次是 `n` 步。  
  - 所以总步数约等于 `k × n`，如果 `k = n = 100`，最多是 10 000 步，仍然可以接受。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`ans、max_idx`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经能跑通，但每次遍历整个数组找最大值会导致 **`k` 次 `O(n)`** 的循环。  
如果把“找最大值”这一步的代价降到 **`O(log n)`**，整体时间就可以降到 **`O(k log n)`**，在数据规模更大时会快很多。

要实现 **快速取最大**，我们可以使用 **最大堆（max‑heap）**（在 Python 中用 `heapq` 实现最小堆，再把数取负即可）。堆的特点：

- 堆顶永远是当前最大（或最小）元素，取出或插入一个元素的代价是 `O(log n)`。  
- 类比：把所有水果放进一个“最大堆盒子”，每次只要打开盒子顶端就能拿到最大的水果，而不需要把所有水果都翻一遍。

**步骤**：

1. 把数组 `nums` 中的每个数取负后放入最小堆 `heap`（负数的最小值对应原数的最大值）。  
2. 重复 `k` 次：  
   - 弹出堆顶（即当前最大数 `cur = -heapq.heappop(heap)`）。  
   - 把 `cur` 加到答案 `ans`。  
   - 由于选了这个数后它会加 1，新的值是 `cur + 1`，再把 `-(cur + 1)` 放回堆中。  
3. 循环结束后 `ans` 即为最大得分。

> **为什么堆是对的？**  
> 堆始终维护了“当前所有元素中最大的那个在最前面”。因为每一步我们只需要这个最大值来决定本轮得分，堆的结构正好满足这种需求。把取走的元素再放回（值加 1）后，堆会自动重新排列，保证下次仍能快速拿到新的最大值。

#### 代码（Python）

```python
import heapq

def max_score_optimal(nums, k):
    """
    最优解：使用最大堆（负数最小堆）快速取最大值
    时间复杂度：O(k log n)
    空间复杂度：O(n)   （堆里保存 n 个元素）
    """
    # 1️⃣ 把所有元素取负放入最小堆，负数的最小值对应原数的最大值
    heap = [-x for x in nums]
    heapq.heapify(heap)          # O(n) 建堆

    ans = 0

    for _ in range(k):
        # 2️⃣ 取出当前最大的数（记得取负恢复原值）
        cur = -heapq.heappop(heap)

        # 3️⃣ 加入得分
        ans += cur

        # 4️⃣ 选完后该数加 1，重新放回堆中（仍然取负）
        heapq.heappush(heap, -(cur + 1))

    return ans
```

#### 复杂度

- **时间复杂度**：`O(k log n)`  
  - `heapify` 初始建堆是 `O(n)`，相对 `k log n` 可以忽略。  
  - 每次弹出和插入各 `O(log n)`，共 `k` 次，所以整体是 `k·log n`。  
  - 与暴力解的 `k·n` 相比，`log n`（约 7 左右）远小于 `n`（最多 100），在更大的数据规模下优势更明显。

- **空间复杂度**：`O(n)`  
  - 堆里存放了 `n` 个整数（取负后），额外使用的空间随 `n` 线性增长。

---

## 心得

- **核心技巧**：**每次挑最大值的贪心** + **最大堆（优先队列）** 实现快速取最大。  
- **适用的题型**：  
  1. “每次挑最大的元素并进行某种更新”——如 “Maximum Points You Can Obtain from Cards”。  
  2. “需要多次取极值并动态改变数据”——如 “K Closest Points to Origin”。  
  3. “每次操作只影响被取出的那个元素”——如 “Maximum Sum of Selected Elements after Increment”。  
- **一句话总结解题钥匙**：**“把当前最大值立即拿走”，用堆把“最大”这件事做成常数时间的查询**。

## 反思

- **第一反应**：看到“每次挑一个元素，挑完后它会加 1”，自然想到**每次都挑最大的**，因为这样立刻得到最大的即时收益。  
- **最容易踩的坑**：  
  - 忘记把选中的元素 **加 1 后再放回**，导致后续挑选不到递增的价值。  
  - 对堆的实现不熟悉时，直接使用 `heapq` 的最小堆，需要把数取负，否则会得到最小值。  
  - 边界情况：`k` 可能大于数组长度，需要允许同一个元素被多次挑选（这正是题目要求的）。  
- **下次类似题的第一步**：先问自己“这一步的收益是否会随被挑选而改变”，如果会，**是否每次都想让收益最大化**，那么就考虑使用 **贪心 + 优先队列** 来实现。