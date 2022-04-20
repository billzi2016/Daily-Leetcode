# #1749. 任意子数组的最大绝对和 / Maximum Absolute Sum of Any Subarray

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-absolute-sum-of-any-subarray/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. The absolute sum of a subarray [numsl, numsl+1, ..., numsr-1, numsr] is abs(numsl + numsl+1 + ... + numsr-1 + numsr).
Return the maximum absolute sum of any (possibly empty) subarray of nums.
Note that abs(x) is defined as follows:

**Examples**

**Example 1:**

```
Input: nums = [1,-3,2,3,-4]
Output: 5
Explanation: The subarray [2,3] has absolute sum = abs(2+3) = abs(5) = 5.
```

**Example 2:**

```
Input: nums = [2,-5,1,-4,3,-2]
Output: 8
Explanation: The subarray [-5,1,-4] has absolute sum = abs(-5+1-4) = abs(-8) = 8.
```

**Constraints**

- 1 <= nums.length <= 105
- -104 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`。子数组（subarray）`[nums[l], nums[l+1], ..., nums[r-1], nums[r]]` 的绝对和定义为 `abs(nums[l] + nums[l+1] + ... + nums[r-1] + nums[r])`。返回 `nums` 中任意（可能为空）子数组的最大绝对和。

注意，`abs(x)` 的定义如下：

**示例 1**  
输入: `nums = [1,-3,2,3,-4]`  
输出: `5`  
解释: 子数组 `[2,3]` 的绝对和为 `abs(2+3) = abs(5) = 5`。

**示例 2**  
输入: `nums = [2,-5,1,-4,3,-2]`  
输出: `8`  
解释: 子数组 `[-5,1,-4]` 的绝对和为 `abs(-5+1-4) = abs(-8) = 8`。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `-10^4 <= nums[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子数组**，把它们的和算出来，取绝对值后再找最大值。  
- 数据结构：只需要一个普通的 Python 列表 `nums`，以及几个整数变量来记录当前子数组的和、最大绝对和等。可以把子数组看成一本书里的连续章节，暴力枚举就相当于把每一本书的每一种可能的章节组合都读一遍，记下它的总字数（和），然后取最大的绝对值。  
- 正确性：因为我们把**所有**合法的子数组都遍历了一遍，最大绝对和一定会在这遍历过程中被发现。  

#### 代码（Python）

```python
from typing import List

def max_absolute_subarray_bruteforce(nums: List[int]) -> int:
    """
    暴力枚举所有子数组，计算绝对和的最大值
    """
    n = len(nums)
    max_abs = 0                     # 用来保存目前找到的最大绝对和
    # i 为子数组的左端点
    for i in range(n):
        cur_sum = 0                  # 从 i 开始累计子数组的和
        # j 为子数组的右端点（包括 i 本身）
        for j in range(i, n):
            cur_sum += nums[j]       # 累加当前元素，得到 [i, j] 的和
            max_abs = max(max_abs, abs(cur_sum))   # 更新最大绝对值
    return max_abs
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  解释：外层循环跑 `n` 次，内层循环平均也跑 `n/2` 次，整体大概是 `n × n`，所以说是二次方。对 10⁵ 长度的数组来说，这已经太慢了，会超时。  
- **空间复杂度**：`O(1)`。  
  解释：只用了常数个额外变量（`max_abs、cur_sum、i、j`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复累计子数组的和**。  
如果我们把“从左到右累计”这个过程保存下来，就可以在一次遍历中得到所有子数组的最大和和最小和。  
这正是 **Kadane 算法**（卡德恩算法）要解决的问题：  
- 计算**最大子数组和**（不取绝对值），只需要在遍历时维护一个“以当前元素结尾的最大子数组和”。  
- 同理，如果把每个数都换成它的相反数（即乘 `-1`），求的就是**最小子数组和**的相反数。于是我们只要再跑一次 Kadane（或者在同一次遍历中维护最小和），就能得到最小子数组和。

关键点：**最大绝对子数组和 = max(最大子数组和, -最小子数组和)**。  
因为绝对值把负数变正，最小的负和的绝对值等价于它的相反数。

下面一步步解释 Kadane：

1. **当前最大和 `cur_max`**：表示**以当前位置结尾**的子数组的最大可能和。如果把 `cur_max` 加上 `nums[i]` 仍然比单独 `nums[i]` 大，就说明把前面的子数组接上去更好；否则就从 `i` 重新开始。  
2. **全局最大和 `global_max`**：遍历过程中出现过的最大 `cur_max`。  
3. 同理，**当前最小和 `cur_min`** 和 **全局最小和 `global_min`** 用相同的思路，只是比较方向改成 “更小”。

这样只需要一次遍历（`O(n)`）就能得到答案。

#### 代码（Python）

```python
from typing import List

def max_absolute_subarray(nums: List[int]) -> int:
    """
    Kadane 两遍（一次同时求最大和与最小和），时间 O(n)，空间 O(1)
    """
    # 初始化为第一个元素，防止数组全为负数或全为正数的特殊情况
    cur_max = global_max = nums[0]   # 以当前位置结尾的最大子数组和
    cur_min = global_min = nums[0]   # 以当前位置结尾的最小子数组和

    # 从第二个元素开始遍历
    for x in nums[1:]:
        # 更新以 x 结尾的最大子数组和
        cur_max = max(x, cur_max + x)   # 要么从 x 开始，要么把前面的继续加
        global_max = max(global_max, cur_max)  # 记录全局最大

        # 更新以 x 结尾的最小子数组和（同理，只是取 min）
        cur_min = min(x, cur_min + x)   # 要么从 x 开始，要么继续累加
        global_min = min(global_min, cur_min)  # 记录全局最小

    # 最大绝对和要么是正的最大子数组和，要么是负的最小子数组和的相反数
    return max(global_max, -global_min)
```

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  解释：只遍历一次数组，每个元素做了常数次加减比较，和数组长度成线性关系。相较于 `O(n²)`，速度提升了 **n 倍**，在 10⁵ 长度时毫秒级即可完成。  
- **空间复杂度**：`O(1)`。  
  解释：只用了四个整数变量来记录中间状态，和输入规模无关。

---

## 心得

- **核心技巧**：Kadane 算法（最大子数组和） + 同时维护最小子数组和，利用绝对值的对称性转化为 “最大或最小” 的比较。  
- **适用题型**：  
  1. “最大子数组和”（LeetCode 53）  
  2. “最小子数组和”（变形）  
  3. “子数组乘积最大”（需要类似的动态规划思路）  
- **解题钥匙**：**把“绝对值最大”拆成“正向最大”和“负向最小”，分别求解后取较大者**。

---

## 反思

- **第一反应**：直接想到枚举子数组，写双层循环。虽然能得到正确答案，但忽视了时间限制。  
- **最容易踩的坑**：  
  - 忘记考虑全部为负数的情况，直接返回 `0` 会出错（空子数组在本题是允许的，但题目要求“可能为空”，若返回 0 仍然是合法的，但更保险的做法是按照 Kadane 的初始化方式处理）。  
  - 只算最大子数组和而忘记最小子数组和，导致在全部负数或整体和为负的情况下得到错误的绝对值。  
- **下次思路**：看到“最大/最小/绝对”这类描述时，先在脑中把问题**拆分**为正向最大和负向最小两个子问题，判断是否可以用一次遍历的 DP（Kadane）一次性搞定。这样可以迅速定位到最优解的方向。