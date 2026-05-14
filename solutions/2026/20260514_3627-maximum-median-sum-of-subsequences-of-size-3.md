# #3627. 大小为 3 的子序列的最大中位数和 / Maximum Median Sum of Subsequences of Size 3

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/maximum-median-sum-of-subsequences-of-size-3/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums with a length divisible by 3.
You want to make the array empty in steps. In each step, you can select any three elements from the array, compute their median, and remove the selected elements from the array.
The median of an odd-length sequence is defined as the middle element of the sequence when it is sorted in non-decreasing order.
Return the maximum possible sum of the medians computed from the selected elements.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,2,1,3]
Output: 5
Explanation:
Hence, the sum of the medians is 3 + 2 = 5 .
```

**Example 2:**

```
Input: nums = [1,1,10,10,10,10]
Output: 20
Explanation:
Hence, the sum of the medians is 10 + 10 = 20 .
```

**Constraints**

- 1 <= nums.length <= 5 * 105
- nums.length % 3 == 0
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，其长度可以被 3 整除。  
你需要通过若干步骤将数组中的所有元素全部移除。每一步，你可以从数组中任选 **三个** 元素，计算这三个数的中位数（median），然后将这三个元素全部删除。  
**中位数**的定义：对奇数长度的序列，将其按非递减顺序排序后，位于中间位置的元素即为中位数。  

求在所有可能的操作序列中，**中位数之和的最大值**。

#### 示例

**示例 1**  
输入：`nums = [2,1,3,2,1,3]`  
输出：`5`  
解释：一种最优的选择是先取 `[2,3,1]`，其中位数为 `2`；再取剩余的 `[2,3,1]`，其中位数为 `3`。因此中位数之和为 `2 + 3 = 5`。

**示例 2**  
输入：`nums = [1,1,10,10,10,10]`  
输出：`20`  
解释：可以先取 `[1,10,10]`，其中位数为 `10`；再取 `[1,10,10]`，其中位数仍为 `10`。中位数之和为 `10 + 10 = 20`。

#### 约束条件

- `1 <= nums.length <= 5 * 10^5`
- `nums.length % 3 == 0`
- `1 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**穷举**所有可能的取法：  
1. 从数组 `nums` 中任选 3 个数，求出这 3 个数的中位数（把它们排序后取第二大的）。  
2. 把这 3 个数从数组里删掉，递归地对剩下的元素继续做同样的操作。  
3. 把所有递归分支得到的中位数之和取最大值，即为答案。  

> **类比**：把 `nums` 看成一盒子里的彩球，每次从盒子里随手抓出 3 颗，记下这 3 颗中“第二大”的颜色编号，然后把这 3 颗扔掉。要想得到最大的编号总和，就必须把**所有**可能的抓法都试一遍。

这种方法一定能得到正确答案，因为它枚举了**所有合法的分组方式**，没有漏掉任何一种可能。

#### 代码（Python）  

```python
from itertools import combinations
from functools import lru_cache

def median_of_three(a, b, c):
    """返回三个数的中位数（第二大的数）"""
    # 把 3 个数放进列表，排序后取下标 1 的元素
    return sorted([a, b, c])[1]

def brute_max_median_sum(nums):
    n = len(nums)
    # 为了能够使用缓存，先把列表转成元组（不可变），并排序以保证状态唯一
    nums = tuple(sorted(nums))

    @lru_cache(None)                # 记忆化搜索，避免重复计算相同子问题
    def dfs(state):
        """state 是当前剩余元素的元组，返回最大中位数和"""
        if not state:               # 已经没有元素了，和为 0
            return 0
        m = len(state)
        best = 0
        # 任意挑选 3 个下标组成组合
        for i, j, k in combinations(range(m), 3):
            # 取出这三个数
            a, b, c = state[i], state[j], state[k]
            med = median_of_three(a, b, c)
            # 把这三个数从状态里删掉，形成新的元组
            new_state = list(state)
            # 必须从大到小下标删除，防止索引错位
            for idx in sorted((i, j, k), reverse=True):
                new_state.pop(idx)
            new_state = tuple(new_state)
            # 递归求后面的最大和，加上当前的中位数
            best = max(best, med + dfs(new_state))
        return best

    return dfs(nums)

# 仅用于演示，实际只能跑在 n 很小（如 n<=9）的情况下
print(brute_max_median_sum([2,1,3,2,1,3]))   # 5
```

> **说明**：  
> - `itertools.combinations` 用来枚举所有 3 元组的下标组合。  
> - `functools.lru_cache` 把已经算过的子问题记下来，避免指数级重复计算。  
> - 即使用了记忆化，整体复杂度仍然是指数级，只能在 **极小规模**（`len(nums) ≤ 9`）下跑得完。

#### 复杂度  

- **时间复杂度**：`O( C(n,3) * T(n-3) )`，递归深度是 `n/3`，每层都要遍历 `C(remaining,3)` 种取法，整体约为 **指数级**（类似 `O( (n)! )`），实际只能用于教学或小规模验证。  
- **空间复杂度**：递归栈深度为 `n/3`，加上缓存保存的状态，最坏情况下需要 `O( C(n,3) )` 的空间，同样是指数级。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有可能的三元组**，这导致搜索空间爆炸。  
观察题目要求的“最大化所有中位数的和”，我们可以从**排序**的角度思考：

1. **把数组从小到大排好序**。  
2. 为了让每一组三个数的中位数尽可能大，我们希望 **中位数本身取大的**。  
3. 在一组三个数里，若把 **最大的两个数**放进同一个组，而把 **最小的数**作为“填充”，那么这组的中位数就是**第二大的数**，恰好是我们想要的大数。  
4. 具体做法是：  
   - 先把最小的 `n/3` 个数作为“填充”，它们只负责占位，不影响中位数。  
   - 剩下的 `2n/3` 个数按从大到小的顺序两两配对，每对的**第二大**（即这两数中较小的那个）就是该组的中位数。  

把上述过程写成下标的操作更直观：  
- 排序后，设 `len = n`。  
- 我们需要取 `n/3` 个中位数，分别是下标 `len-2, len-4, len-6, …`（每次向左跳两个位置）。  

> **类比**：想象把排好队的学生分成三列，左边第一列最矮的学生只负责站位，右边两列的学生都是高个儿。每组的“中位数”就是右边两列中**较矮的那位**，因为左边的学生太矮，根本不影响“中位数”。于是我们只要把最高的学生和次高的学生配在一起，次高的自然成为该组的贡献。

这一步把**原本指数级的搜索**直接压缩成了**一次排序 + 线性遍历**。

#### 代码（Python）  

```python
def max_median_sum(nums):
    """
    返回把数组按题意分组后，能够得到的最大中位数之和。
    思路：先排序，然后每次取倒数第二个、倒数第四个……的元素求和。
    """
    nums.sort()                         # 从小到大排好序
    n = len(nums)
    groups = n // 3                     # 需要多少组
    ans = 0
    # 从倒数第二个元素开始，每次往左跳两个位置，取出 groups 次
    for i in range(1, groups + 1):
        # 第 i 组的中位数位于下标 n - 2*i
        ans += nums[n - 2 * i]
    return ans

# 示例
print(max_median_sum([2,1,3,2,1,3]))          # 5
print(max_median_sum([1,1,10,10,10,10]))     # 20
```

> **关键行解释**  
> - `nums.sort()`：把数组排好序，后面取值才能有规律。  
> - `for i in range(1, groups + 1):`：遍历每一组。  
> - `nums[n - 2 * i]`：取倒数第 `2*i` 个元素，即每组的中位数。  
> - `ans += ...`：把所有中位数累加得到答案。

#### 复杂度  

- **时间复杂度**：`O(n log n)` —— 主要耗时在排序，`n` 为数组长度。  
  - **含义**：如果 `n = 10⁶`，排序大约需要 `10⁶ * log₂(10⁶) ≈ 20·10⁶` 次比较，仍在几秒内可以接受。  
- **空间复杂度**：`O(1)`（不计入输入本身的存储），只用了几个整数变量。  
  - **含义**：算法运行时不需要额外的数组或递归栈，内存占用几乎是常数。

---

## 心得  

- **核心技巧**：**排序 + 贪心配对**。把数组排序后，利用“把最大的两个数和最小的数凑成一组” 的贪心策略，使每组的中位数恰好是第二大的数，从而最大化总和。  
- **适用题型**：  
  1. “分组取中位数/最大值/最小值之和” 类似的题目（如 *Maximum Sum of Minimum Elements of Pairs*）。  
  2. 需要**把大数尽可能保留下来**的组合优化问题（如 *Array Partition I*、*Maximum Sum of Two Non‑Overlapping Subarrays*）。  
  3. 任何可以通过**排序后固定取子序列**解决的最大化/最小化问题。  

> **一句话总结解题钥匙**：**先排序，再把最大的两两配对，配对的第二大即为每组的最佳中位数**。

---

## 反思  

- **第一反应**：看到“每次取 3 个数的中位数”，自然想到**枚举所有三元组**，于是想到递归或暴力搜索。  
- **最容易踩的坑**：  
  - 忽视数组长度一定是 `3` 的倍数，导致循环边界写错。  
  - 错误地把“最大两个数”配对后取**最大值**而不是**第二大**，会低估答案。  
  - 对于极大输入（`5×10⁵`），若仍使用递归或大量额外数组，会出现 **超时 / 内存溢出**。  
- **下次遇到同类题**，第一步应该：**先思考是否可以通过排序把“好”与“坏”分离**，再检验是否存在“把最大元素配对” 的贪心策略。若能，就立刻转向 **O(n log n)** 的排序+线性遍历方案，而不是盲目递归枚举。