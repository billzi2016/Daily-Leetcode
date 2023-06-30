# #2302. **计数得分小于 K 的子数组** / Count Subarrays With Score Less Than K

> 难度：困难 · 标签：Array、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-subarrays-with-score-less-than-k/)

---

## 题目（英文原版）

**Description**

The score of an array is defined as the product of its sum and its length.
Given a positive integer array nums and an integer k, return the number of non-empty subarrays of nums whose score is strictly less than k.
A subarray is a contiguous sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [2,1,4,3,5], k = 10
Output: 6
Explanation:
The 6 subarrays having scores less than 10 are:
- [2] with score 2 * 1 = 2.
- [1] with score 1 * 1 = 1.
- [4] with score 4 * 1 = 4.
- [3] with score 3 * 1 = 3. 
- [5] with score 5 * 1 = 5.
- [2,1] with score (2 + 1) * 2 = 6.
Note that subarrays such as [1,4] and [4,3,5] are not considered because their scores are 10 and 36 respectively, while we need scores strictly less than 10.
```

**Example 2:**

```
Input: nums = [1,1,1], k = 5
Output: 5
Explanation:
Every subarray except [1,1,1] has a score less than 5.
[1,1,1] has a score (1 + 1 + 1) * 3 = 9, which is greater than 5.
Thus, there are 5 subarrays having scores less than 5.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105
- 1 <= k <= 1015

---

## 题目（中文翻译）

数组的得分定义为其元素之和与长度的乘积。  
给定一个正整数数组 `nums` 和整数 `k`，返回 `nums` 中所有 **非空子数组（subarray）** 的数量，这些子数组的得分严格小于 `k`。  
子数组（subarray）是数组中连续的元素序列。

### 示例

#### 示例 1
```
Input: nums = [2,1,4,3,5], k = 10
Output: 6
Explanation:
得分小于 10 的 6 个子数组如下：
- [2]，得分为 2 * 1 = 2。
- [1]，得分为 1 * 1 = 1。
- [4]，得分为 4 * 1 = 4。
- [3]，得分为 3 * 1 = 3。 
- [5]，得分为 5 * 1 = 5。
- [2,1]，得分为 (2 + 1) * 2 = 6。
需要注意的是，子数组如 [1,4] 与 [4,3,5] 不计入，因为它们的得分分别为 10 与 36，均不满足 “小于 k” 的条件。
```

#### 示例 2
```
Input: nums = [1,1,1], k = 5
Output: 5
Explanation:
除了子数组 [1,1,1] 之外，所有子数组的得分都小于 5。
[1,1,1] 的得分为 (1 + 1 + 1) * 3 = 9，超过了 5。
因此，得分小于 5 的子数组共有 5 个。
```

### 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`
- `1 <= k <= 10^15`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**枚举所有子数组**，逐个算出它们的“分数”(sum × length)，看是否 `< k`。  

- **枚举子数组**：把数组的左端点 `i` 从 `0` 到 `n‑1`，右端点 `j` 从 `i` 到 `n‑1`，每一对 `(i, j)` 对应一个连续子序列 `nums[i…j]`。  
- **求子数组的和**：可以在枚举的过程中累计 `sum += nums[j]`，这样不需要每次都遍历子数组求和。  
- **判断**：如果 `sum * (j‑i+1) < k`，计数器 `ans` 加一。  

> **类比**：把数组想象成一排书，左端点 `i` 是“从哪本书开始”，右端点 `j` 是“读到哪本书”。我们把每一种“读书方案”都尝试一次，看看这本书的总页数（`sum`）乘以阅读的天数（`length`）是否小于老师给的阈值 `k`。

**为什么正确**：因为我们检查了**所有**可能的连续子序列，凡是满足条件的都被计数，凡是不满足的都被排除，答案自然就是满足条件的子数组个数。

#### 代码（Python）

```python
def countSubarrays_bruteforce(nums, k):
    n = len(nums)
    ans = 0                     # 记录满足条件的子数组个数
    for left in range(n):       # 左端点 i
        cur_sum = 0
        for right in range(left, n):   # 右端点 j
            cur_sum += nums[right]      # 累加得到子数组的和
            length = right - left + 1   # 子数组长度
            if cur_sum * length < k:    # 判断分数是否小于 k
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “平方”代表如果 `n = 10⁴`，算法大约要跑 `10⁸` 次循环，远远超出 1 秒的限制。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（`ans、cur_sum、left、right`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每个左端点都要从头遍历到右端点**，导致 `O(n²)`。  
观察题目条件：

- 数组中的元素都是 **正整数**（`nums[i] ≥ 1`）。  
- 当我们**把右端点往右扩展**时，子数组的**长度**会 +1，**和**也会 +`nums[right]`，于是**分数** `sum * length` **只会增大**（不会出现先增后减的情况）。  

这正好满足**滑动窗口（Two Pointers）**的使用前提：  
> 当窗口满足条件时，继续往右扩展会让条件更难满足；当窗口不满足时，左端点右移会让条件更容易满足。  

**滑动窗口的核心步骤**：

1. 维护两个指针 `left`（窗口左边）和 `right`（窗口右边，左闭右开区间 `[left, right)`）。  
2. `cur_sum` 保存窗口内元素的和，`length = right - left` 是窗口长度。  
3. **向右扩展**：只要 `cur_sum * length < k`，就把 `right` 向右移动一位并累计 `cur_sum`。  
4. 当条件不再满足时，**收缩左边**：把 `nums[left]` 从 `cur_sum` 中减掉，`left` 向右移动一位。  
5. 对每个 `left`，**窗口 `[left, right)`** 中的所有子数组（即以 `left` 为左端点，右端点在 `left … right‑1`）都是合法的。合法子数组的数量等于 `right - left`。把它加入答案。  

因为所有数都是正的，**右指针只会单调递增**，整个过程只遍历数组两遍，时间是 `O(n)`。

> **类比**：把 `left`、`right` 想成两个人在跑步。右边的跑者（`right`）尽可能往前跑，只要两人的距离乘以跑者们手中“糖果的总重量”（`sum`）小于 `k`。一旦距离太大，左边的跑者（`left`）就往前走，减轻“糖果重量”。这样两个人永远向前跑，永不回头。

#### 代码（Python）

```python
def countSubarrays(nums, k):
    """
    返回分数 < k 的子数组个数，时间 O(n)，空间 O(1)
    """
    n = len(nums)
    left = 0               # 窗口左端点
    cur_sum = 0            # 窗口内元素和
    ans = 0                # 结果计数

    for right in range(n):                 # 右端点一次遍历整个数组
        cur_sum += nums[right]              # 把新元素加入窗口
        # 如果窗口不满足条件，左指针右移直至满足（或窗口为空）
        while left <= right and cur_sum * (right - left + 1) >= k:
            cur_sum -= nums[left]           # 移除左端点元素
            left += 1                       # 左指针右移

        # 此时窗口 [left, right]（闭区间）全部合法
        # 以 right 为右端点、左端点在 left … right 的子数组数 = right-left+1
        ans += right - left + 1

    return ans
```

**关键注释解释**  

- `cur_sum * (right - left + 1) >= k`：判断当前窗口的 **分数** 是否已经不小于 `k`。  
- `while` 循环里不断把左端点元素踢出窗口，直到窗口重新满足 `< k`。  
- `ans += right - left + 1`：以当前 `right` 为最右端点，所有左端点在 `[left, right]` 的子数组都合法，数量即窗口长度。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个元素最多被右指针加入一次，又最多被左指针移除一次，整体线性遍历。相较于暴力的 `O(n²)`，速度提升了 **n 倍**（例如 `n=10⁵` 时只需要约 `10⁵` 次操作）。  
- **空间复杂度**：`O(1)`  
  - 只使用了固定数量的变量（`left、right、cur_sum、ans`），不随 `n` 增长。

---

## 心得  

- **核心技巧**：**双指针（滑动窗口）**，利用数组元素全为正数，使得窗口的“分数”随右端点单调递增，从而可以线性计数。  
- **相似题型**：  
  1. “子数组乘积小于 K”（LeetCode 713）——同样用滑动窗口，只是条件是 `product < k`。  
  2. “最长子数组和不超过 K”（LeetCode 862）——求最长长度，而不是计数。  
  3. “子数组和小于 K 的个数”（LeetCode 327）——需要前缀和 + 二分/有序集合，但思路同样是把 “窗口不满足” 的情况转化为计数。  
- **一句话总结**：**把“分数随窗口扩大只能增大”这一单调性抽出来，用两个指针维护最宽合法窗口，窗口长度直接给出合法子数组的个数。**

---

## 反思  

- **第一反应**：看到“子数组的分数 = 和 × 长度”，想到 **枚举所有子数组**，因为没有立刻想到乘积随长度的单调性。  
- **最容易踩的坑**：  
  - **整数溢出**：`sum` 可能达到 `10⁵ × 10⁵ = 10¹⁰`，再乘以长度会超过 32 位整数范围。使用 Python 自带的大整数即可，或在 C/C++ 中使用 `long long`。  
  - **左指针越界**：`while left <= right` 必须加上 `left <= right` 的判断，防止左指针跑到右指针右边导致负长度。  
  - **k 很小**（比如 `k=1`），窗口可能一直空，需要保证 `while` 循环能够把左指针赶到 `right+1`，此时 `right-left+1` 为 0，不会错误计数。  
- **下次类似题的第一步**：先判断**数组元素是否全为正**（或全为非负），如果是，尝试**滑动窗口**；如果不是，需要考虑**前缀和 + 二分/有序结构** 或 **单调队列**。