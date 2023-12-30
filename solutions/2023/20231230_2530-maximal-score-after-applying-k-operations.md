# #2530. 最大化 K 次操作后的得分 / Maximal Score After Applying K Operations

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximal-score-after-applying-k-operations/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer k. You have a starting score of 0.
In one operation:
Return the maximum possible score you can attain after applying exactly k operations.
The ceiling function ceil(val) is the least integer greater than or equal to val.

**Examples**

**Example 1:**

```
Input: nums = [10,10,10,10,10], k = 5
Output: 50
Explanation: Apply the operation to each array element exactly once. The final score is 10 + 10 + 10 + 10 + 10 = 50.
```

**Example 2:**

```
Input: nums = [1,10,3,3,3], k = 3
Output: 17
Explanation: You can do the following operations:
Operation 1: Select i = 1, so nums becomes [1,4,3,3,3]. Your score increases by 10.
Operation 2: Select i = 1, so nums becomes [1,2,3,3,3]. Your score increases by 4.
Operation 3: Select i = 2, so nums becomes [1,2,1,3,3]. Your score increases by 3.
The final score is 10 + 4 + 3 = 17.
```

**Constraints**

- 1 <= nums.length, k <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums` 和一个整数 `k`。一开始你的得分为 0。  

在一次操作中，你可以选择任意下标 `i`（0 ≤ i < nums.length），将 `nums[i]` 加入当前得分，然后将 `nums[i]` 替换为 `ceil(nums[i] / 3)`，其中 **ceil**（天花板函数）是大于或等于给定值的最小整数。  

请返回恰好执行 `k` 次操作后，你能够获得的最大可能得分。

**示例 1**  
```
输入: nums = [10,10,10,10,10], k = 5
输出: 50
解释: 对每个数组元素各执行一次操作。最终得分为 10 + 10 + 10 + 10 + 10 = 50。
```

**示例 2**  
```
输入: nums = [1,10,3,3,3], k = 3
输出: 17
解释: 你可以按以下方式进行操作:
操作 1: 选择 i = 1，数组变为 [1,4,3,3,3]，得分增加 10。
操作 2: 选择 i = 1，数组变为 [1,2,3,3,3]，得分增加 4。
操作 3: 选择 i = 2，数组变为 [1,2,1,3,3]，得分增加 3。
最终得分为 10 + 4 + 3 = 17。
```

**约束条件**  

- `1 <= nums.length, k <= 10^5`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一次操作的下标**，把所有可能的操作序列全部尝试一遍，记下最大的得分。  
实现上可以用递归（或回溯）：

1. 进入第 `t` 步（`t` 从 `0` 到 `k-1`），遍历数组的每一个位置 `i`。  
2. 把当前 `nums[i]` 加到总分 `score` 中。  
3. 按题目要求把 `nums[i]` 改为 `ceil(nums[i] / 3)`，然后递归进入第 `t+1` 步。  
4. 递归结束后把数组恢复原状（回溯），继续尝试下一个 `i`。  

> **数据结构类比**：这里把数组想成一排装有不同重量的盒子，递归相当于每次把手伸进去挑选一个盒子拿走（记分），随后把盒子里剩下的东西（`ceil(val/3)`）放回去。我们要把所有可能的挑选顺序都尝试一遍。

**为什么正确**：因为我们遍历了**所有**合法的 `k` 次操作序列，最大分数必然在其中，所以最终得到的答案一定是最优的。

**时间/空间复杂度**  
- 时间：每一步都有 `n` 种选择，共 `k` 步，时间复杂度是 `O(n^k)`（指数级）。如果 `n`、`k` 都是 10⁵，这根本不可行。  
- 空间：递归深度为 `k`，加上保存数组的额外拷贝，空间复杂度是 `O(k)`。

> **大白话解释**：`O(n^k)` 就像让你把 10 个水果放进 5 层的抽屉，每层抽屉里可以放任意一种水果，一共要尝试 `10⁵ = 100 000` 种放法，根本不可能在一分钟内算完。

#### 代码（Python）

```python
import math
from typing import List

def maximalScore_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    best = 0                         # 记录全局最大得分

    def dfs(step: int, cur_score: int) -> None:
        nonlocal best
        if step == k:                 # 已经做了 k 次操作
            best = max(best, cur_score)
            return

        for i in range(n):
            original = nums[i]        # 记住当前位置原来的值，方便回溯
            gain = nums[i]            # 本次操作能得到的分数
            nums[i] = math.ceil(nums[i] / 3)   # 按题目规则更新数组
            dfs(step + 1, cur_score + gain)    # 继续下一步
            nums[i] = original        # 回溯：恢复原来的值

    dfs(0, 0)
    return best
```

> 这段代码可以跑通小规模测试（比如 `len(nums) ≤ 5, k ≤ 5`），但在正式数据下会 **超时**。

#### 复杂度

- **时间复杂度**：`O(n^k)` —— 每一步都有 `n` 种选择，深度为 `k`，指数级增长。  
- **空间复杂度**：`O(k)` —— 递归栈的深度是 `k`，其余只用了常数级的额外空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于每一步都要遍历整个数组寻找“该选哪个”。  
实际上，**每一次我们只关心当前最大的数**，因为：

- 题目给出的提示：*“总是最优的做法是选择数组中最大的元素”。*  
- 设想如果我们在某一步选择了一个不是最大的数 `x`，而把更大的数 `y` 留到以后再选。  
  - 当我们最终选到 `y` 时，它已经被 `ceil(y/3)` 可能多次缩小，得到的分数只会更小。  
  - 因此把大的数早点取走，能保证我们拿到的分数更高。

所以每一步的**最优选择**是“当前数组的最大值”。这让我们只需要一个能够**快速取最大并支持更新**的数据结构——**最大堆（Priority Queue）**。

**最大堆的工作原理**（类比）：

- 把数组看成一堆装有不同重量的石头的盒子。  
- 最大堆就像一个“看得见最大石头的窗口”，每次只要敲一下窗口，就能把最重的石头拿出来（`O(log n)`）。  
- 拿走后把石头的重量改成 `ceil(weight/3)` 再放回窗口，窗口会自动重新排序。

**算法步骤**：

1. 把所有 `nums[i]` 放进最大堆 `heap`（Python 的 `heapq` 是最小堆，取负数即可实现最大堆）。  
2. 初始化 `score = 0`。  
3. 重复 `k` 次：
   - `cur = -heapq.heappop(heap)` 取出当前最大值（记得恢复正数）。  
   - `score += cur` 把它加入总分。  
   - `new_val = (cur + 2) // 3`（等价于 `ceil(cur/3)`），把新值放回堆 `heapq.heappush(heap, -new_val)`。  
4. 循环结束后返回 `score`。

**为什么正确**（归纳法）：

- **基础**：第 1 步显然要取最大值，才能得到最高的第一笔得分。  
- **归纳假设**：假设前 `t` 步我们每一步都取了当时的最大值，得到了最优的前缀得分。  
- **归纳步骤**：第 `t+1` 步的数组状态正好是对前 `t` 步操作后得到的数组。若此时不取最大值 `M` 而取了一个更小的值 `x`，则 `M` 会在以后某一步被取走，但那时它已经被若干次 `ceil/3` 缩小，导致最终得分不如直接在第 `t+1` 步取 `M`。所以“取最大”仍然是最优的选择。  
- 由归纳可知，整个 `k` 步都取当前最大值即为全局最优。

**核心数据结构**：**最大堆**（优先队列），支持  
- `push`（放入新值）——`O(log n)`  
- `pop`（弹出最大值）——`O(log n)`

#### 代码（Python）

```python
import heapq
from typing import List

def maximalScore(nums: List[int], k: int) -> int:
    """
    使用最大堆（通过取负数实现）贪心地每一步取当前最大的元素。
    """
    # 1. 把所有元素放入堆，Python 的 heapq 是最小堆，用负数模拟最大堆
    max_heap = [-x for x in nums]   # 取负后变成“最小堆”
    heapq.heapify(max_heap)         # O(n) 建堆

    score = 0

    for _ in range(k):
        # 2. 取出当前最大值（记得恢复正数）
        cur = -heapq.heappop(max_heap)   # O(log n)

        # 3. 累计得分
        score += cur

        # 4. 计算新的值：ceil(cur / 3) 可以用整数运算 (cur + 2) // 3
        new_val = (cur + 2) // 3

        # 5. 把新值放回堆中
        heapq.heappush(max_heap, -new_val)   # O(log n)

    return score
```

> **关键行中文注释**  
> - 第 4 行：把负数放进去是为了让 `heapq` 变成“最大堆”。  
> - 第 12 行：`-heapq.heappop` 把最小的负数（即最大的正数）弹出来。  
> - 第 16 行：`(cur + 2) // 3` 等价于向上取整 `ceil(cur/3)`，因为整数除法会向下取整，先加上除数-1 再除即可。

#### 复杂度

- **时间复杂度**：`O(k log n)`  
  - 每一次操作弹出、插入堆各一次，都是 `O(log n)`，共进行 `k` 次。  
  - 与暴力解的 `O(n^k)` 相比，指数级的时间被压缩到了线性乘对数级，能够轻松处理 `n, k ≤ 10⁵` 的规模。

- **空间复杂度**：`O(n)`  
  - 堆里保存了 `n` 个元素（负数形式），除此之外只用了常数级的额外空间。  

> **对比**：暴力解需要遍历所有可能的组合，时间呈指数增长；最优解只需维护一个堆，时间随 `k` 线性增长，几乎可以在一瞬间完成 10⁵ 次操作。

---

## 心得

- **核心技巧**：**贪心 + 最大堆**  
  每一步都选当前最大的元素，用堆实现快速获取与更新。

- **适用的题型**（类似思路）  
  1. **LeetCode 2530. Maximal Score After Applying K Operations**（本题）  
  2. **LeetCode 215. Kth Largest Element in an Array** – 需要维护最大（或最小）堆来快速取第 K 大。  
  3. **LeetCode 2182. Construct String With Repeat Limit** – 通过最大堆按字母出现次数贪心构造字符串。

- **一句话总结解题钥匙**：  
  *“只要每一步都把当前最大的收益拿走，并用堆把最大值的查询和更新压到对数时间，就能在大数据下轻松拿满分。”*

---

## 反思

- **第一反应**：看到“每次把选中的元素除以 3 向上取整”，立刻想到要把大的数字尽早使用，否则会被多次削减——于是想到贪心。

- **最容易踩的坑**  
  1. **取整错误**：`ceil(x/3)` 不能直接写 `x // 3`，需要向上取整。使用 `(x + 2) // 3` 或 `math.ceil`。  
  2. **堆的方向**：Python `heapq` 是最小堆，忘记取负数会导致每次取最小值而不是最大值。  
  3. **整数溢出**：在某些语言需要注意 `nums[i]` 可达 `10⁹`，但 Python 的整数是无限精度，这里不必担心。

- **下次遇到同类题的第一步**：  
  *“先判断是否每一步都只关心当前的极值（最大/最小），如果是，就考虑用堆（或有序容器）实现 O(log n) 的取极值与更新。”*