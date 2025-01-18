# #3026. **最大好子数组和** / Maximum Good Subarray Sum

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-good-subarray-sum/)

---

## 题目（英文原版）

**Description**

You are given an array nums of length n and a positive integer k.
A subarray of nums is called good if the absolute difference between its first and last element is exactly k, in other words, the subarray nums[i..j] is good if |nums[i] - nums[j]| == k.
Return the maximum sum of a good subarray of nums. If there are no good subarrays, return 0.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5,6], k = 1
Output: 11
Explanation: The absolute difference between the first and last element must be 1 for a good subarray. All the good subarrays are: [1,2], [2,3], [3,4], [4,5], and [5,6]. The maximum subarray sum is 11 for the subarray [5,6].
```

**Example 2:**

```
Input: nums = [-1,3,2,4,5], k = 3
Output: 11
Explanation: The absolute difference between the first and last element must be 3 for a good subarray. All the good subarrays are: [-1,3,2], and [2,4,5]. The maximum subarray sum is 11 for the subarray [2,4,5].
```

**Example 3:**

```
Input: nums = [-1,-2,-3,-4], k = 2
Output: -6
Explanation: The absolute difference between the first and last element must be 2 for a good subarray. All the good subarrays are: [-1,-2,-3], and [-2,-3,-4]. The maximum subarray sum is -6 for the subarray [-1,-2,-3].
```

**Constraints**

- 2 <= nums.length <= 105
- -109 <= nums[i] <= 109
- 1 <= k <= 109

---

## 题目（中文翻译）

给定一个长度为 `n` 的数组 `nums` 和一个正整数 `k`。  
如果一个子数组（subarray）的首元素与尾元素的绝对差恰好等于 `k`，即子数组 `nums[i..j]` 满足 `|nums[i] - nums[j]| == k`，则称该子数组为 **好子数组**（good subarray）。

返回 `nums` 中好子数组的最大和。如果不存在好子数组，返回 `0`。

---

### 示例

#### 示例 1
**输入**  
```
nums = [1,2,3,4,5,6], k = 1
```
**输出**  
```
11
```
**解释**  
好子数组的首尾元素的绝对差必须为 `1`。所有满足条件的子数组为：`[1,2]`、`[2,3]`、`[3,4]`、`[4,5]`、`[5,6]`。其中子数组 `[5,6]` 的和最大，为 `11`。

#### 示例 2
**输入**  
```
nums = [-1,3,2,4,5], k = 3
```
**输出**  
```
11
```
**解释**  
好子数组的首尾元素的绝对差必须为 `3`。所有满足条件的子数组为：`[-1,3,2]`、`[2,4,5]`。其中子数组 `[2,4,5]` 的和最大，为 `11`。

#### 示例 3
**输入**  
```
nums = [-1,-2,-3,-4], k = 2
```
**输出**  
```
-6
```
**解释**  
好子数组的首尾元素的绝对差必须为 `2`。所有满足条件的子数组为：`[-1,-2,-3]`、`[-2,-3,-4]`。其中子数组 `[-1,-2,-3]` 的和最大，为 `-6`。

---

### 约束条件
- `2 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `1 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**枚举所有子数组**，检查它们是否满足「首尾元素差的绝对值等于 k」的条件，满足的就计算子数组的和，最后取最大值。  

- **枚举子数组**：用两个循环 `i`（子数组起点）和 `j`（子数组终点），`i < j`。  
- **判断好子数组**：`abs(nums[i] - nums[j]) == k`。这里的 `abs` 就像我们在生活中算两个数的距离，要求恰好等于 k。  
- **求子数组和**：把 `nums[i] … nums[j]` 的所有元素相加。可以在内层循环里累加，也可以先算前缀和再求和。  

> **为什么一定能得到正确答案？**  
> 因为我们把所有可能的子数组都检查了一遍，符合条件的子数组的和一定会被记录，最终的最大值就是答案。  

#### 代码（Python）  
```python
def maximumGoodSubarraySum_bruteforce(nums, k):
    n = len(nums)
    ans = float('-inf')          # 用极小值表示“还没有找到好子数组”
    for i in range(n):           # 枚举子数组左端点
        cur_sum = 0               # 累加从 i 开始的子数组和
        for j in range(i, n):    # 枚举右端点
            cur_sum += nums[j]    # 动态维护子数组和，省去每次重新求和
            if j > i and abs(nums[i] - nums[j]) == k:   # 必须长度 ≥ 2
                ans = max(ans, cur_sum)                # 更新最大和
    return ans if ans != float('-inf') else 0          # 若没有好子数组返回 0
```

#### 复杂度  
- **时间复杂度**：`O(n²)`。两个循环嵌套，最坏情况下要检查 `n·(n-1)/2` 个子数组。可以把 `O(n²)` 想象成「如果 n=10,000，运算次数大约是 100 百万」——对 10⁵ 的数据量来说会超时。  
- **空间复杂度**：`O(1)`。只用了常数级别的额外变量（`cur_sum`、`ans`），不随 `n` 增长。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**重复计算子数组和**以及**频繁遍历所有起点**。我们可以利用**前缀和**把子数组求和的过程降到 `O(1)`，再结合**哈希表**快速找到满足首尾差为 `k` 的起点。  

1. **前缀和**  
   - 定义 `pref[i]` 为数组前 `i` 个元素的和（不含第 `i` 个），即 `pref[0]=0`，`pref[i+1]=pref[i]+nums[i]`。  
   - 任意子数组 `nums[l..r]` 的和可以用前缀和快速算出：`sum(l,r) = pref[r+1] - pref[l]`。这就像我们把所有钱放进一个大箱子，想知道第 `l` 到 `r` 的钱有多少，只要看箱子在 `r+1` 时的总额减去在 `l` 时的总额即可。  

2. **哈希表记录“起点候选”**  
   - 对于每个位置 `i`（作为子数组的 **右端点**），我们需要找所有左端点 `l` 使得 `|nums[l] - nums[i]| = k`。  
   - 设 `nums[l] = x`，则 `x` 必须等于 `nums[i] - k` 或 `nums[i] + k`。这两个值我们可以在 **哈希表** 中快速查找。  
   - 哈希表的键：**数组元素的值**（`nums[l]`），值：**该元素作为左端点时对应的最小前缀和** `pref[l]`。为什么要保存最小前缀和？因为子数组和 `pref[i+1] - pref[l]` 要想最大，只需要 `pref[l]` 最小即可（减去一个更小的数，差就更大）。  

3. **遍历过程**  
   - 初始化哈希表 `best = {}`，其中 `best[val]` 表示出现过的值 `val` 对应的**最小**前缀和。  
   - 从左到右遍历数组，维护当前的前缀和 `cur_pref`（等于 `pref[i]`）。  
   - 对于当前位置 `i`（右端点），检查 `nums[i] - k` 与 `nums[i] + k` 是否已经出现在 `best` 中。  
     - 若出现，则对应的左端点的最小前缀和记为 `left_pref`。当前好子数组的和为 `cur_pref + nums[i] - left_pref`（因为 `cur_pref + nums[i] = pref[i+1]`）。  
     - 用这个和更新答案 `ans`。  
   - 然后把当前位置的 **元素值** `nums[i]` 以及对应的 **前缀和** `cur_pref`（即 `pref[i]`）加入哈希表。若同一个值出现多次，只保留**更小的前缀和**（因为后面的子数组会受益于更小的 `pref[l]`）。  

> **核心技巧**：  
> - 前缀和把「区间求和」变成「两个点的差」；  
> - 哈希表把「在整个左侧寻找满足条件的元素」降到 `O(1)`；  
> - 只保存**最小前缀和**，相当于在左侧“挑选最有利的起点”。  

#### 代码（Python）  
```python
def maximumGoodSubarraySum(nums, k):
    """
    返回满足 |nums[l] - nums[r]| == k 的子数组的最大和。
    若不存在这样的子数组，返回 0。
    """
    best = {}                 # key: 数组元素的值, value: 该值出现时对应的最小前缀和
    cur_pref = 0              # 当前遍历到的位置 i 前的前缀和，即 pref[i]
    ans = float('-inf')       # 记录最大好子数组和

    for i, val in enumerate(nums):
        # 先检查以当前元素为右端点的所有可能左端点
        for need in (val - k, val + k):          # 可能的左端点元素值
            if need in best:                     # 哈希表中存在对应左端点
                left_pref = best[need]           # 该左端点的最小前缀和
                # 当前子数组的和 = pref[i+1] - pref[l]
                cur_sum = cur_pref + val - left_pref
                ans = max(ans, cur_sum)

        # 更新哈希表：把当前元素值及其对应的前缀和加入
        # 只保留更小的前缀和，因为它能产生更大的子数组和
        if val not in best or cur_pref < best[val]:
            best[val] = cur_pref

        # 推进前缀和到下一个位置
        cur_pref += val

    # 若从未更新过 ans，说明没有好子数组
    return ans if ans != float('-inf') else 0
```

> **代码要点注释**  
> - `best` 类似“字典查找”，就像在一本词典里找单词对应的页码。  
> - `cur_pref` 是“走到这一步口袋里已有的钱”。  
> - `cur_sum = cur_pref + val - left_pref` 等价于 `pref[i+1] - pref[l]`，即「右端点累计的总额」减去「左端点之前的累计总额」。  

#### 复杂度  
- **时间复杂度**：`O(n)`。我们只遍历一次数组，每个位置只做常数次哈希表查找/写入。相比 `O(n²)`，这就像把「检查所有可能的配对」变成了「只看相邻的两个人」。  
- **空间复杂度**：`O(m)`，其中 `m` 是数组中不同元素的数量（最坏 `O(n)`）。我们需要保存每个出现过的值对应的最小前缀和。  

---  

## 心得  

- **核心技巧**：前缀和 + 哈希表（记录每个值的最小前缀和），实现「区间求和」的快速查询与「满足特定首尾差」的高效匹配。  
- **适用题型**  
  1. **子数组和满足某种条件**（如「子数组和等于 target」）——常用前缀和 + 哈希表。  
  2. **首尾元素满足关系**（如「首尾差为固定值」）——同样可以把左端点信息存进哈希表。  
  3. **区间最大/最小值问题**（如「在满足条件的区间里取最大和」）——结合单调栈或前缀最值。  
- **一句话总结**：把「遍历所有子数组」压缩成「遍历一次数组 + 哈希表快速定位合适的左端点」就是解题钥匙。  

---  

## 反思  

- **第一反应**：直接双层循环枚举子数组，随后发现会超时。  
- **最容易踩的坑**  
  - 忘记子数组长度必须 ≥ 2（`i` 与 `j` 不能相同）。  
  - 在哈希表中保存的不是「任意」前缀和，而是**最小**前缀和，否则会错失更大的子数组和。  
  - 处理全部负数的情况：即使所有子数组和都是负数，仍要返回最大的（即「负数中最大的」），而不是直接返回 0，除非根本没有好子数组。  
- **下次类似题**：一看到「子数组」+「某种首尾关系」或「子数组和满足固定值」时，先想到**前缀和 + 哈希表**，然后判断是否需要保存最值（最小/最大）来进一步优化。