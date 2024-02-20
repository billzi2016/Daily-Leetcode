# #2587. 重新排列数组以最大化前缀得分 / Rearrange Array to Maximize Prefix Score

> 难度：中等 · 标签：Array、Greedy、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/rearrange-array-to-maximize-prefix-score/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. You can rearrange the elements of nums to any order (including the given order).
Let prefix be the array containing the prefix sums of nums after rearranging it. In other words, prefix[i] is the sum of the elements from 0 to i in nums after rearranging it. The score of nums is the number of positive integers in the array prefix.
Return the maximum score you can achieve.

**Examples**

**Example 1:**

```
Input: nums = [2,-1,0,1,-3,3,-3]
Output: 6
Explanation: We can rearrange the array into nums = [2,3,1,-1,-3,0,-3].
prefix = [2,5,6,5,2,2,-1], so the score is 6.
It can be shown that 6 is the maximum score we can obtain.
```

**Example 2:**

```
Input: nums = [-2,-3,0]
Output: 0
Explanation: Any rearrangement of the array will result in a score of 0.
```

**Constraints**

- 1 <= nums.length <= 105
- -106 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`。你可以将 `nums` 中的元素重新排列成任意顺序（包括保持原顺序）。  
设 `prefix` 为重新排列后数组的前缀和（prefix sums）数组，即 `prefix[i]` 为重新排列后 `nums` 中下标 `0` 到 `i` 的元素之和。数组 `nums` 的得分（score）定义为 `prefix` 中正整数的个数。  

返回你能够得到的最大得分。

**示例 1**  
```
Input: nums = [2,-1,0,1,-3,3,-3]
Output: 6
```
**解释**：我们可以将数组重新排列为 `nums = [2,3,1,-1,-3,0,-3]`。  
`prefix = [2,5,6,5,2,2,-1]`，因此得分为 6。可以证明 6 是能够取得的最大得分。

**示例 2**  
```
Input: nums = [-2,-3,0]
Output: 0
```
**解释**：无论如何重新排列数组，得到的得分均为 0。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `-10^6 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的排列都尝试一遍**，然后统计每一种排列得到的前缀和数组中正数的个数，取最大值。

- **使用的数据结构**  
  - `list`：存放数组的一个排列。  
  - `int`：记录前缀和以及正数计数。  

- **为什么它是正确的**  
  对于每一种合法的排列，题目都要求我们计算「前缀和数组中正数的数量」并取最大值。遍历**全部**排列自然不会错过最优解，所以这种「枚举」方法一定可以得到正确答案。

- **时间/空间复杂度分析（大白话）**  
  - **时间**：如果数组长度是 `n`，排列的总数是 `n!`（读作「n 的阶乘」），每次要遍历一次数组计算前缀和，耗时 `O(n)`。于是总时间是 `O(n! * n)`，这就像把 10!（≈ 3,600 万）次运算再乘以 10，根本不可接受。  
  - **空间**：只需要保存当前排列和几个计数器，`O(n)` 的额外空间。

> **结论**：暴力枚举思路虽然直观、一定正确，但在 `n` 达到 10⁵ 时根本跑不完，只能作为「思考起点」来帮助我们寻找更快的办法。

#### 代码（Python）

```python
import itertools
from typing import List

def max_score_bruteforce(nums: List[int]) -> int:
    """
    暴力枚举所有排列，返回最大前缀正数个数。
    只适合极小规模的演示（比如 n <= 6），否则会超时。
    """
    best = 0
    # itertools.permutations 会生成所有排列
    for perm in itertools.permutations(nums):
        prefix_sum = 0
        cnt = 0
        for x in perm:
            prefix_sum += x          # 累加得到当前前缀和
            if prefix_sum > 0:       # 前缀和为正数则计数
                cnt += 1
        best = max(best, cnt)        # 记录最大的得分
    return best
```

#### 复杂度

- **时间复杂度**：`O(n! * n)` —— 先生成 `n!` 种排列，再对每个排列线性扫描。  
- **空间复杂度**：`O(n)` —— 只保存当前排列和几个计数器。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**关键不是遍历所有排列，而是找出一种「最优」的排列**。  
我们先思考「哪个位置的元素对前缀和的贡献最大」：

1. 前缀和是「从左到右累计求和」的结果。  
2. 若把一个大的正数放在前面，它会被累加进 **所有后面的前缀**，对正数计数的帮助最大。  
3. 相反，负数如果放在前面，会把后面的累计和拉低，导致后面的前缀可能变成非正。  

于是**把数组从大到小排序**（降序）是最自然的猜想——大的正数先出现，负数尽量往后推。  

下面用更严谨的方式说明：

- **证明思路（贪心）**  
  假设我们已经得到一个最优排列 `P`，但 `P` 里出现了相邻的两个元素 `a, b`，且 `a < b`（即 `a` 在前，`b` 在后）。  
  把它们交换得到新排列 `P'`，其余位置不变。  
  - 对于交换前的前缀和，`a` 对它自己以及之后所有前缀的贡献是 `a`，`b` 对它自己以及之后所有前缀的贡献是 `b`。  
  - 交换后，`b` 贡献给更早的前缀，`a` 贡献给更晚的前缀。因为 `b > a`，**早期的前缀和只会变大或不变**，而晚期的前缀和只会变小或不变。  
  - 重要的是：**前缀和从正变负的转折点只能往后移动**，不会出现新的负前缀出现在更前面。于是正数前缀的数量 **不会减少**，可能会增加。  

  这说明在任意最优解中，**不存在前面比后面小的相邻元素**，即数组必须是非递增（降序）的。  

- **算法步骤**  
  1. 将 `nums` 按 **从大到小** 排序。  
  2. 依次累加得到前缀和，统计前缀和大于 0 的次数。  
  3. 返回统计值即为最大得分。  

- **类比**  
  想象你在排队买电影票，手里有一些「优惠券」价值正（正数）和「罚款」价值负（负数）。如果把大额优惠券先用掉，后面的总费用（前缀和）就更容易保持正数，罚款（负数）自然留到最后，影响最小。

#### 代码（Python）

```python
from typing import List

def max_score(nums: List[int]) -> int:
    """
    贪心算法：把数组降序排列，然后统计正前缀的个数。
    时间复杂度 O(n log n) 来自排序，空间复杂度 O(1)（原地排序可省去额外数组）。
    """
    # 1. 降序排列。sorted 会返回新列表，若想节省空间可使用 nums.sort(reverse=True)
    nums_sorted = sorted(nums, reverse=True)

    prefix = 0          # 当前前缀和
    score = 0           # 正前缀的数量

    # 2. 依次累加并计数
    for x in nums_sorted:
        prefix += x     # 加上当前元素得到新的前缀和
        if prefix > 0:  # 前缀和为正则计数
            score += 1

    return score
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `log n` 来自对 `n` 个元素的排序（最快的比较排序下界），遍历一次数组是 `O(n)`，所以总体是 `O(n log n)`。  
  - 相比暴力的 `O(n! * n)`，这已经是可以在 `10⁵` 规模下瞬间跑完的速度。

- **空间复杂度**：`O(1)`（若使用原地 `sort`）或 `O(n)`（若使用 `sorted` 返回新列表）。  
  - 只需要几个整数变量保存前缀和和计数，额外的存储几乎可以忽略不计。

---

## 心得

- **核心技巧**：**贪心 + 降序排序**  
  把「对后面影响最大的」元素提前，让正数前缀尽可能多。

- **适用的题型**  
  1. **最大化前缀/后缀正数个数**（如本题）。  
  2. **让累计和始终为正的最小移除次数**（类似 LeetCode 1665. Minimum Initial Energy to Finish Tasks）。  
  3. **安排任务使得完成时间最早**（如「任务调度」类贪心问题）。

- **一句话总结解题钥匙**  
  > 把「越大越好」的数尽早使用，负数尽量往后排——降序排列即可。

---

## 反思

- **第一反应**：看到「前缀和」和「正数个数」的统计，立刻想到「遍历所有排列」——这是一种最直观但不可行的暴力思路。  
- **最容易踩的坑**  
  - 忽略了 **负数** 的影响，误以为只要把正数排前面就一定最优。实际上，需要把 **所有** 元素整体降序，负数之间的相对顺序也会影响累计和。  
  - 边界条件：全是非正数时，答案应该是 `0`，代码中 `if prefix > 0` 正确处理了这一点。  
- **下次遇到同类题**，第一步应该问自己：  
  - 「有没有一种排序或贪心策略可以让对后面影响最大的元素提前出现？」  
  - 若答案是肯定的，就尝试 **排序 + 线性扫描**，而不是直接暴力枚举。