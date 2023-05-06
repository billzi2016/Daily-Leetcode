# #2233. **K 次增量后的最大乘积** / Maximum Product After K Increments

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-product-after-k-increments/)

---

## 题目（英文原版）

**Description**

You are given an array of non-negative integers nums and an integer k. In one operation, you may choose any element from nums and increment it by 1.
Return the maximum product of nums after at most k operations. Since the answer may be very large, return it modulo 109 + 7. Note that you should maximize the product before taking the modulo.

**Examples**

**Example 1:**

```
Input: nums = [0,4], k = 5
Output: 20
Explanation: Increment the first number 5 times.
Now nums = [5, 4], with a product of 5 * 4 = 20.
It can be shown that 20 is maximum product possible, so we return 20.
Note that there may be other ways to increment nums to have the maximum product.
```

**Example 2:**

```
Input: nums = [6,3,3,2], k = 2
Output: 216
Explanation: Increment the second number 1 time and increment the fourth number 1 time.
Now nums = [6, 4, 3, 3], with a product of 6 * 4 * 3 * 3 = 216.
It can be shown that 216 is maximum product possible, so we return 216.
Note that there may be other ways to increment nums to have the maximum product.
```

**Constraints**

- 1 <= nums.length, k <= 105
- 0 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个非负整数数组 `nums` 和一个整数 `k`。一次操作中，你可以选择 `nums` 中的任意元素并将其增加 1（increment）。  
返回至多进行 `k` 次操作后，`nums` 的最大乘积（product）。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。**注意**：应在取模之前先求出最大乘积。

**示例 1**  
**输入**: `nums = [0,4]`, `k = 5`  
**输出**: `20`  
**解释**: 将第一个数字增加 5 次。此时 `nums = [5, 4]`，乘积为 `5 * 4 = 20`。可以证明 20 是可能的最大乘积，因此返回 20。  
（也可能存在其他增量方式能够得到相同的最大乘积）

**示例 2**  
**输入**: `nums = [6,3,3,2]`, `k = 2`  
**输出**: `216`  
**解释**: 将第二个数字增加 1 次，将第四个数字增加 1 次。此时 `nums = [6, 4, 3, 3]`，乘积为 `6 * 4 * 3 * 3 = 216`。可以证明 216 是可能的最大乘积，因此返回 216。  
（也可能存在其他增量方式能够得到相同的最大乘积）

**约束条件**  
- `1 <= nums.length, k <= 10^5`  
- `0 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的增量分配方式都穷举一遍，算出每种情况下的乘积，取最大值**。  
- **数据结构**：我们可以用一个列表 `cur` 保存当前的数组，每次递归/循环把 `k` 次“+1”分配到不同的下标上。  
- **生活化类比**：想象有 `k` 块糖果，要分给 `n` 个人，每个人手里的糖果数就是数组元素。我们把所有可能的分配方式都列出来，看看哪种分配下大家手里糖果数的乘积最大。  
- **为什么正确**：因为我们遍历了**所有**合法的增量分配方案，必然会包含最优方案，所以取最大乘积一定是答案。  

显然，这种方法在 `k`、`n` 较大时会爆炸：  
- 对每一次增量都有 `n` 种选择，全部遍历的时间是 `O(n^k)`，根本不可行。  
- 空间上只需要保存一个数组 `O(n)`，但递归栈深度可能达到 `k`，也不友好。

#### 代码（Python）

```python
from itertools import product
from math import prod
from typing import List

MOD = 10**9 + 7

def maxProduct_bruteforce(nums: List[int], k: int) -> int:
    """
    暴力枚举：把 k 次 +1 分配到 len(nums) 个位置上。
    这里用 product 产生所有长度为 k 的下标序列（每一次增量的目标下标）。
    """
    n = len(nums)
    best = 0

    # 产生所有可能的增量序列，例如 k=2, n=3 -> (0,0) (0,1) ... (2,2)
    for seq in product(range(n), repeat=k):
        cur = nums[:]                     # 复制原数组
        for idx in seq:                   # 按序列中的下标逐个 +1
            cur[idx] += 1
        best = max(best, prod(cur))       # 计算乘积，取最大

    return best % MOD                     # 最后再取模
```

> **注意**：上述代码只能在 `n`、`k` 极小（如 ≤5）时跑得完，主要用于帮助大家理解“遍历所有可能”的思路。

#### 复杂度  

- **时间复杂度**：`O(n^k)`  
  - “指数级”增长：如果把 `O` 看成“每多一次增量，就要把所有位置都尝试一次”，所以时间会像 `n` 的 `k` 次方一样迅速膨胀。  
- **空间复杂度**：`O(n)`  
  - 只保存一份数组和若干临时变量，和输入规模线性相关。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到：**每一次增量都只影响一个元素，而我们只关心最终乘积的最大化**。  
**关键观察**：

1. **一次增量应该加到哪个元素上？**  
   设当前数组为 `a1, a2, …, an`，如果我们把 `+1` 加到 `ai`，乘积会变成  
   `P' = P / ai * (ai + 1)`，其中 `P` 是原乘积。  
   为了让 `P'` 最大，**我们希望 `ai` 越小越好**（因为分子分母的比值 `(ai+1)/ai` 在 `ai` 小的时候更大）。  
   直观来说，把糖果先给糖最少的那个人，能让整体乘积提升最多。

2. **每一步都把 +1 加到最小的数**，这就是一个**贪心**策略。  
   为了高效找到当前最小的数，我们需要一种**能够快速取最小值并支持更新**的数据结构——**最小堆（min‑heap）**。  
   - **最小堆的类比**：想象一堆石子，最小的那颗石子总是放在最上面，随手抓一下就是最小的。  
   - 堆的两个核心操作：`heappop`（取出最小并把堆重新整理）和 `heappush`（把新元素放进去并保持堆性质），时间都是 `O(log n)`。

3. **完整流程**  
   - 把所有数组元素放进最小堆。  
   - 重复 `k` 次：弹出堆顶最小值 `x`，把它加一得到 `x+1`，再压回堆。  
   - 循环结束后，堆里剩下的就是最终的数组（顺序不重要），把它们全部乘起来取模即可。

4. **为什么贪心最优**  
   - **局部最优 ⇒ 全局最优**：每一步我们都让乘积的提升幅度最大。假设有另一种分配方式在某一步把 `+1` 加到了更大的数 `y (≥ x)`，则那一步的乘积提升比例 ` (y+1)/y ≤ (x+1)/x`，整体乘积不可能超过我们贪心的选择。  
   - 通过**交换论证**可以形式化：如果最优解在某一步没有把 `+1` 加到当前最小数上，我们可以把这一步的增量“换到”最小数上，乘积不会变小，最终得到同等或更好的解。于是贪心策略必然能得到最优答案。

#### 代码（Python）

```python
import heapq
from typing import List

MOD = 10**9 + 7

def maxProduct(nums: List[int], k: int) -> int:
    """
    贪心 + 最小堆
    1. 把所有元素放进 min‑heap
    2. 重复 k 次：弹出最小值 x，推回 x+1
    3. 最后把堆中所有数相乘并取模
    """
    # 1. 建堆，heapify 的时间是 O(n)
    heap = nums[:]
    heapq.heapify(heap)

    # 2. 逐次增量
    for _ in range(k):
        x = heapq.heappop(heap)   # 取出当前最小的数
        heapq.heappush(heap, x + 1)  # 加 1 再放回堆

    # 3. 计算乘积（取模时要防止中间乘积溢出，用 long）
    ans = 1
    while heap:
        ans = (ans * heapq.heappop(heap)) % MOD
    return ans
```

> **代码要点**  
> - `heapq.heapify` 一次性把列表变成堆，时间 `O(n)`。  
> - `heappop` 与 `heappush` 各是 `O(log n)`，循环 `k 次`，总时间 `O(k log n)`。  
> - 乘积时每一步都 `% MOD`，防止 Python 整数太大（虽然 Python 本身支持大整数，但取模可以省掉不必要的计算）。

#### 复杂度  

- **时间复杂度**：`O(k log n)`  
  - **含义解释**：每一次增量（共 `k` 次）都要在堆里找最小值并重新整理，整理的代价相当于“把一堆东西重新排队”，大约是 `log n`（对数）级别。整体就是 `k` 乘以 `log n`。  
  - 与暴力 `O(n^k)` 相比，指数级下降，能够轻松处理 `n、k ≤ 10^5` 的数据规模。

- **空间复杂度**：`O(n)`  
  - 堆里保存了全部 `n` 个数，外加常数级的临时变量。与输入规模线性相关。

---

## 心得

- **核心技巧**：**贪心 + 最小堆**，即每一步把增量放在当前最小的数上，以最大化乘积的提升比例。  
- **适用题型**  
  1. “把资源（次数、糖果、钱）分配到多个数上，使乘积/几何均值最大”的问题。  
  2. “每次操作都要选择当前最小/最大元素” 的题目，如 **“将数组中最小元素增加 k 次”**、**“最大化数组的最小值”**。  
  3. 需要频繁取最值并更新的场景，常用 **堆**（priority queue）实现高效。  
- **一句话总结解题钥匙**：**“把每一次 +1 都投给最小的数，用堆快速找最小”**。

---

## 反思

- **第一反应**：看到“每次可以把任意元素 +1，求最大乘积”，立刻想到“把 +1 给最大的数？”但乘积的增长比例其实取决于**相对大小**，于是转而思考“把 +1 给最小的数”。  
- **最容易踩的坑**  
  1. **忘记取模的时机**：题目要求先最大化乘积再取模，不能在每一步都直接对 `k` 取模后再比较，否则会影响贪心的判断。正确做法是只在最终乘积阶段取模。  
  2. **0 的特殊性**：如果数组里有 `0`，乘积为 `0`，此时必须先把 `0` 增到 `1`（或更大）才能让乘积起飞。堆自然会把 `0` 放在最前面，贪心会先处理它，避免遗漏。  
  3. **大数溢出**：在语言不支持大整数时，需要在每次乘积时取模防止溢出。Python 本身支持大整数，但仍建议在乘积循环里 `% MOD`，保持运算高效。  
- **下次类似题的第一步**：**判断“每次操作的最优对象”**（最小还是最大），并选用 **堆** 或 **排序** 来快速定位它。这样可以把“每一步都找最值”的复杂度从 `O(n)` 降到 `O(log n)`，为后续的贪心或 DP 打下坚实基础。