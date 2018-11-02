# #152. 最大乘积子数组 / Maximum Product Subarray

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-product-subarray/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, find a subarray that has the largest product, and return the product.
The test cases are generated so that the answer will fit in a 32-bit integer.

**Examples**

**Example 1:**

```
Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.
```

**Example 2:**

```
Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- -10 <= nums[i] <= 10
- The product of any subarray of nums is guaranteed to fit in a 32-bit integer.

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums`，找出乘积（product）最大的连续子数组（subarray），并返回该乘积。测试用例保证答案能够放入 32 位整数（32-bit integer）中。

示例 1:
Input: nums = [2,3,-2,4]
Output: 6
Explanation: `[2,3]` 的乘积最大，为 `6`。

示例 2:
Input: nums = [-2,0,-1]
Output: 0
Explanation: 结果不能是 `2`，因为 `[-2,-1]` 不是连续子数组（subarray）。

约束条件：
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- 任意子数组（subarray）的乘积（product）均保证能够放入 32 位整数中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的「连续子数组」都枚举一遍，算出它们的乘积，然后找出最大的那个。  

- **数据结构**：我们只需要一个普通的 Python 列表 `nums` 来存放输入。遍历时，用两个嵌套的循环分别表示子数组的左端点 `i` 和右端点 `j`。  
- **生活化类比**：把数组想象成一排商品，每件商品都有一个「价值」`nums[k]`（可以是正数、负数或 0）。我们想找出一段连续的商品，使得把它们的价值相乘后得到的「总价值」最大。暴力解相当于「把每一段可能的商品组合都试一次」——就像把所有可能的购物清单都算一遍再挑最贵的。  
- **为什么正确**：因为我们穷举了**所有**合法的子数组，必然会覆盖到最优解所在的那段子数组，所以答案一定在枚举得到的乘积里。  

#### 代码（Python）

```python
from typing import List

def maxProduct_bruteforce(nums: List[int]) -> int:
    """
    暴力枚举所有连续子数组，计算乘积，返回最大值。
    """
    n = len(nums)
    # 先把答案初始化为第一个元素，防止全部都是负数的情况
    max_prod = nums[0]

    # i 为子数组的左端点
    for i in range(n):
        prod = 1                     # 从左到右累计乘积
        # j 为子数组的右端点，逐步扩大子数组
        for j in range(i, n):
            prod *= nums[j]          # 累乘当前元素
            # 更新全局最大乘积
            if prod > max_prod:
                max_prod = prod
    return max_prod
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `i` 走 `n` 步，内层循环 `j` 最多也走 `n` 步，最坏情况下相当于 `n × n` 次乘法运算。用大白话说，就是「如果数组有 10,000 个数，暴力解要做大约 100,000,000 次乘法」——显然会超时。  
- **空间复杂度**：`O(1)`  
  - 只用了几个额外的变量 `max_prod、prod、i、j`，不随输入规模增长而增加。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有子数组是最慢的环节**，因为我们重复计算了很多相同的乘积。  
关键观察：

1. **乘积的符号会翻转**：当我们遇到负数时，原本很大的正乘积会变成负数，而原本很小的负乘积（绝对值大）乘以负数后会变成一个很大的正数。  
2. **只需要关注「以当前位置结尾」的最大乘积和最小乘积**：因为后面的元素只能接在「当前」这个位置后面，若想得到更大的乘积，只可能是  
   - 把「之前的最大正乘积」继续乘上当前元素（如果当前元素是正数），  
   - 或者把「之前的最小负乘积」乘上当前元素（如果当前元素是负数），这样负负得正。  

于是我们维护两个变量：

- `max_ending_here`：以 `nums[i]` 为结尾的**最大**乘积子数组  
- `min_ending_here`：以 `nums[i]` 为结尾的**最小**乘积子数组（因为最小的负数乘以负数可能会成为最大正数）

遍历数组时，**每一步都只用前一步的这两个值**，不需要回头查看更早的子数组。  

> **类比**：把这两个变量想成「两条跑道」——一条跑道专门跑「正向」的最大成绩，另一条跑道跑「负向」的最差成绩。每到一个新选手（数组元素），我们让两条跑道都决定是「继续跑」还是「重新开始」——取决于这位选手的正负号。

具体转移方程：

```
if nums[i] >= 0:
    max_ending_here = max(nums[i], max_ending_here * nums[i])
    min_ending_here = min(nums[i], min_ending_here * nums[i])
else:   # nums[i] 为负数，需要交换角色
    temp = max_ending_here
    max_ending_here = max(nums[i], min_ending_here * nums[i])
    min_ending_here = min(nums[i], temp * nums[i])
```

遍历过程中用一个全局变量 `ans` 保存历史最高的 `max_ending_here` 即可。

#### 代码（Python）

```python
from typing import List

def maxProduct(nums: List[int]) -> int:
    """
    动态规划（DP）解法：
    只维护两个状态 —— 以当前位置结尾的最大乘积和最小乘积。
    时间 O(n)，空间 O(1)。
    """
    # 初始化：第一个元素本身既是最大也是最小
    max_ending_here = min_ending_here = ans = nums[0]

    # 从第二个元素开始遍历
    for i in range(1, len(nums)):
        cur = nums[i]

        # 当当前数为负数时，最大/最小会互换角色
        if cur < 0:
            # 交换两个变量的值，避免使用额外的临时变量
            max_ending_here, min_ending_here = min_ending_here, max_ending_here

        # 计算以当前位置结尾的最大/最小乘积
        # 取「单独使用当前元素」或「把它接在之前的乘积后面」的较大/较小者
        max_ending_here = max(cur, max_ending_here * cur)
        min_ending_here = min(cur, min_ending_here * cur)

        # 更新全局最大答案
        ans = max(ans, max_ending_here)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，`n` 次乘法/比较。对比暴力的 `O(n²)`，相当于「把 10,000 个数的循环次数从 100,000,000 次降到 10,000 次」，效率提升了 10,000 倍。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个变量 (`max_ending_here、min_ending_here、ans、cur`) 与输入规模无关。

---

## 心得

- **核心技巧**：在涉及乘积的区间问题时，**正负号的翻转**是关键。维护**最大和最小两条「跑道」**可以在一次遍历中同时兼顾正负数的影响。  
- **适用题型**：  
  1. **Maximum Product Subarray**（本题）  
  2. **Maximum Product of Three Numbers**（找出三个数的最大乘积）  
  3. **Shortest Subarray with Sum at Least K**（需要前缀和 + 单调队列的思路，类似维护极值）  
- **一句话总结**：遇到乘积区间问题，记得同步追踪「最大正」和「最小负」两条状态。

---

## 反思

- **第一反应**：直接想到「遍历所有子数组」——最自然但最慢的办法。  
- **最容易踩的坑**：  
  - 忽视 **0** 的作用：0 会把前面的乘积全部清零，必须在 DP 中把「单独使用当前元素」的情况考虑进去。  
  - 只维护最大乘积而不记录最小乘积：负数出现时会导致答案错误。  
  - 边界情况：数组长度为 1 时，答案就是唯一的元素。  
- **下次遇到同类题**：第一步先问自己「乘积的符号会怎么变化？」如果出现负数，就立刻想到「同时维护最大和最小」的动态规划思路。