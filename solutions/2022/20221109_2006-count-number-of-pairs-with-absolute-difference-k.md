# #2006. 计数绝对差为 K 的数对 / Count Number of Pairs With Absolute Difference K

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/count-number-of-pairs-with-absolute-difference-k/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return the number of pairs (i, j) where i < j such that |nums[i] - nums[j]| == k.
The value of |x| is defined as:

**Examples**

**Example 1:**

```
Input: nums = [1,2,2,1], k = 1
Output: 4
Explanation: The pairs with an absolute difference of 1 are:
- [1,2,2,1]
- [1,2,2,1]
- [1,2,2,1]
- [1,2,2,1]
```

**Example 2:**

```
Input: nums = [1,3], k = 3
Output: 0
Explanation: There are no pairs with an absolute difference of 3.
```

**Example 3:**

```
Input: nums = [3,2,1,5,4], k = 2
Output: 3
Explanation: The pairs with an absolute difference of 2 are:
- [3,2,1,5,4]
- [3,2,1,5,4]
- [3,2,1,5,4]
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i] <= 100
- 1 <= k <= 99

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，返回满足 `i < j 且 |nums[i] - nums[j]| == k` 的数对 `(i, j)` 的数量。  
`|x|` 表示 **绝对值**，其定义为：

### 示例

#### 示例 1
Input: nums = [1,2,2,1], k = 1  
Output: 4  
Explanation: 绝对差为 1 的数对有：
- [1,2,2,1]
- [1,2,2,1]
- [1,2,2,1]
- [1,2,2,1]

#### 示例 2
Input: nums = [1,3], k = 3  
Output: 0  
Explanation: 不存在绝对差为 3 的数对。

#### 示例 3
Input: nums = [3,2,1,5,4], k = 2  
Output: 3  
Explanation: 绝对差为 2 的数对有：
- [3,2,1,5,4]
- [3,2,1,5,4]
- [3,2,1,5,4]

### 约束条件
- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 100`
- `1 <= k <= 99`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把所有可能的下标对 `(i, j)`（其中 `i < j`）都枚举一遍，检查它们的数值差的绝对值是否等于 `k`。  

- **用到的数据结构**：只需要一个普通的列表 `nums`，因为我们直接在列表里取元素。可以把它想象成一排排的盒子，每个盒子里装着一个数字。我们要把每两个盒子拿出来比较一次。  
- **为什么正确**：只要遍历了所有满足 `i < j` 的组合，就不会漏掉任何合法的配对；只要对每一对都做 `|nums[i] - nums[j]| == k` 的判断，就能准确统计出答案。  
- **复杂度分析**：  
  - **时间**：外层循环走 `n` 次，内层循环平均走 `n/2` 次，总共大约 `n × n/2 ≈ n²/2` 次比较，用大写的 **O(n²)** 表示。这里的 O(n²) 并不是说真的要跑 `n²` 次机器指令，而是说随着输入规模 `n` 增大，运行时间会呈二次方增长。  
  - **空间**：只用了常数个额外变量（计数器、循环索引），所以是 **O(1)**，即不随 `n` 增大而增长的空间。  

#### 代码（Python）  

```python
def count_pairs_bruteforce(nums, k):
    n = len(nums)
    ans = 0                     # 用来累计满足条件的配对数
    # i 从 0 到 n-2，j 从 i+1 到 n-1，确保 i < j
    for i in range(n - 1):
        for j in range(i + 1, n):
            # 计算绝对差并判断是否等于 k
            if abs(nums[i] - nums[j]) == k:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：O(n²) —— 随着数组长度的增大，比较次数会呈二次方增长。  
- **空间复杂度**：O(1) —— 只用了几个整数变量，和输入规模无关。  



---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈** 在于两层循环导致的 `n²` 次比较。实际上，我们只需要知道每个数出现了多少次，就能快速算出它能和哪些数配对。  

1. **把数组的出现次数记下来**。  
   - 使用哈希表（在 Python 中就是 `dict`），把「数字」当作 **key**，把「出现次数」当作 **value**。这一步类似查字典：我们先把所有单词（这里是数字）和它们对应的页码（出现次数）记好，以后想知道某个单词出现了多少次，只需要一次查询。  
2. **遍历哈希表的键**，对每个数字 `x` 看看 `x + k` 是否也在表里。  
   - 如果 `x + k` 存在，说明所有 `x` 与所有 `x + k` 的组合都是合法的配对。配对数就是 `freq[x] * freq[x + k]`（`freq` 为出现次数）。  
   - 为什么不需要考虑 `x - k`？因为我们只遍历一次，`x` 与 `x - k` 的配对已经在遍历到 `x - k` 时算过了，避免重复计数。  
3. **把所有配对数加起来**，就是答案。  

**核心技巧**：**哈希表 + 计数**。通过一次遍历把频率统计完（O(n)），再一次遍历键集合统计配对（最多 O(m)，`m` 为不同数字的个数，`m ≤ n`），整体是线性时间。  

#### 代码（Python）  

```python
def count_pairs_optimal(nums, k):
    # 1️⃣ 统计每个数字出现的次数
    freq = {}
    for num in nums:
        freq[num] = freq.get(num, 0) + 1   # get(...,0) 相当于字典的默认值

    ans = 0
    # 2️⃣ 对每个不同的数字 x，检查 x + k 是否也出现过
    for x, cnt_x in freq.items():
        target = x + k
        if target in freq:                 # 哈希表查询 O(1)
            ans += cnt_x * freq[target]    # 组合数：cnt_x 种选法 × freq[target] 种选法
    return ans
```

#### 复杂度  

- **时间复杂度**：O(n) —— 第一次遍历统计频率 O(n)，第二次遍历键集合 O(m)（最多 O(n)），总共线性增长。比暴力的 O(n²) 快很多。  
- **空间复杂度**：O(m) —— 需要额外的哈希表保存每个不同数字的计数，最坏情况下 `m = n`（所有数字都不相同），所以是线性空间。  

---  

## 心得  

- **核心技巧**：利用哈希表把「出现次数」记下来，再用「差值等于 k」的关系直接算配对数。  
- **适用的题型**：  
  1. “两数之和”类（判断是否存在两数差/和为目标值）  
  2. “统计出现次数”类（如：数组中出现次数超过一次的元素个数）  
  3. “区间计数”类（如：子数组和为 k 的个数）  
- **一句话总结**：把“遍历所有配对”转化为“遍历所有数”，用哈希表一次查询完成配对计数。  



## 反思  

- **第一反应**：直接写两层循环枚举所有下标对。  
- **最容易踩的坑**：  
  - **重复计数**：如果同时检查 `x + k` 与 `x - k`，会把同一对算两次。  
  - **边界条件**：`k = 0` 时，需要注意配对是同值不同下标的组合，公式 `freq[x] * freq[x]` 会把 `(i,i)` 也算进去，需要改为 `freq[x] * (freq[x] - 1) // 2`。本题约束 `k ≥ 1`，所以可以不处理。  
  - **整数溢出**：Python 整数不会溢出，但在其他语言需要注意乘积可能超过 32 位。  
- **下次遇到类似题**：第一步先思考「能不能把信息压缩成哈希表」，把「两两比较」转化为「一次查询」。这样往往能把二次暴力降到线性。