# #1248. 统计好子数组的数量 / Count Number of Nice Subarrays

> 难度：中等 · 标签：Array、Hash Table、Math、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/count-number-of-nice-subarrays/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and an integer k. A continuous subarray is called nice if there are k odd numbers on it.
Return the number of nice sub-arrays.

**Examples**

**Example 1:**

```
Input: nums = [1,1,2,1,1], k = 3
Output: 2
Explanation: The only sub-arrays with 3 odd numbers are [1,1,2,1] and [1,2,1,1].
```

**Example 2:**

```
Input: nums = [2,4,6], k = 1
Output: 0
Explanation: There are no odd numbers in the array.
```

**Example 3:**

```
Input: nums = [2,2,2,1,2,2,1,2,2,2], k = 2
Output: 16
```

**Constraints**

- 1 <= nums.length <= 50000
- 1 <= nums[i] <= 10^5
- 1 <= k <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。连续子数组（continuous subarray）如果恰好包含 `k` 个奇数（odd numbers），则称其为好子数组（nice subarray）。返回好子数组的数量。

### 示例

#### 示例 1
``` 
Input: nums = [1,1,2,1,1], k = 3
Output: 2
Explanation: 唯一包含 3 个奇数的子数组是 [1,1,2,1] 和 [1,2,1,1]。
```

#### 示例 2
``` 
Input: nums = [2,4,6], k = 1
Output: 0
Explanation: 数组中没有奇数。
```

#### 示例 3
``` 
Input: nums = [2,2,2,1,2,2,1,2,2,2], k = 2
Output: 16
```

### 约束条件
- `1 <= nums.length <= 50000`
- `1 <= nums[i] <= 10^5`
- `1 <= k <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有可能的连续子数组** 都枚举出来，逐个检查它们里奇数的个数是否恰好等于 `k`。  
- **数据结构**：只需要原始的数组 `nums`，以及几个计数变量。可以把「奇数」想象成「红灯」，我们在遍历子数组时统计看到多少个红灯。  
- **正确性**：因为我们把每一种连续子数组都检查了一遍，只要子数组里奇数恰好 `k`，就把答案加一，所以一定不会漏掉，也不会多计。  

#### 代码（Python）  
```python
def number_of_nice_subarrays_brute(nums, k):
    n = len(nums)
    ans = 0                     # 最终答案
    for left in range(n):       # 枚举子数组的左端点
        odd_cnt = 0             # 当前子数组中奇数的个数
        for right in range(left, n):   # 枚举右端点
            # 判断 nums[right] 是否为奇数（奇数 % 2 == 1）
            if nums[right] % 2 == 1:
                odd_cnt += 1
            # 如果奇数个数正好等于 k，说明找到了一个「nice」子数组
            if odd_cnt == k:
                ans += 1
            # 若奇数已经超过 k，后面再往右扩展也不可能变回 k，直接退出内层循环
            if odd_cnt > k:
                break
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n²)`  
  这里的 `n²` 表示「最坏情况下我们要检查大约 n × n/2 个子数组」，也就是随着数组长度的增长，耗时会呈二次方增长。  
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量，和输入规模无关。

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **每次都要从左到右遍历子数组**，导致大量重复计数。  
我们可以把「奇数」映射成 `1`，「偶数」映射成 `0`，这样问题就变成：

> 在只包含 `0` 与 `1` 的数组中，求和恰好等于 `k` 的子数组个数。

这正好可以用 **前缀和 + 哈希表**（字典）来高效求解。  

**步骤**  
1. 设 `pre` 为遍历到当前位置为止出现的奇数（即 `1`）的累计个数。`pre` 相当于「走了多少红灯」。  
2. 对于当前的 `pre`，如果之前出现过 `pre - k`，说明在它们之间的子数组里恰好有 `k` 个奇数。于是把「之前出现 `pre - k` 的次数」加到答案里。  
3. 用字典 `cnt` 记录每个前缀和出现的次数，类似查字典：键是前缀和的数值，值是出现的次数。  
4. 初始时把 `cnt[0] = 1` 放进去，表示「在第一个元素之前，奇数个数为 0」这种情况也要计数。  

这样只需要 **一次线性遍历**，每一步的查询和更新都是 `O(1)`，整体是 `O(n)`。

#### 代码（Python）  
```python
def number_of_nice_subarrays(nums, k):
    """
    返回恰好包含 k 个奇数的连续子数组个数。
    思路：把奇数当作 1，偶数当作 0，使用前缀和 + 哈希表计数。
    """
    from collections import defaultdict

    cnt = defaultdict(int)   # 哈希表：前缀和 -> 出现次数
    cnt[0] = 1                # 前缀和为 0 的空子数组计数 1 次
    pre = 0                   # 当前遍历到的位置，奇数的累计个数
    ans = 0

    for num in nums:
        # 把奇数记为 1，偶数记为 0
        if num % 2 == 1:
            pre += 1          # 累计奇数个数

        # 若之前出现过 pre - k，说明从那个位置的后面到现在恰好有 k 个奇数
        need = pre - k
        ans += cnt[need]      # 把对应的出现次数加入答案

        # 更新哈希表，记录当前前缀和出现了一次
        cnt[pre] += 1

    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  只遍历一次数组，`n` 是数组长度。对每个元素的「查字典」和「写字典」都是常数时间，所以整体随 `n` 成线性关系。  
- **空间复杂度**：`O(n)`（最坏情况）  
  哈希表里会存放每一种可能的前缀和，前缀和的取值范围是 `0 … n`，因此最多需要 `n+1` 条记录。相对于输入规模，这算是线性空间。  

---  

## 心得  

- **核心技巧**：把奇数/偶数转换为 `1/0`，利用「前缀和 + 哈希表」统计恰好等于 `k` 的子数组。  
- **适用的类似题目**  
  1. *Subarray Sum Equals K*（求和恰为 K 的子数组个数）  
  2. *Number of Subarrays with Bounded Maximum*（利用双指针/滑动窗口的计数思路）  
  3. *Count Number of Nice Subarrays* 的变体，如要求偶数个数等于 `k` 等。  
- **一句话总结**：**把问题抽象成「0/1 前缀和」后，用字典记录每个前缀出现的次数，瞬间得到恰好 k 个奇数的子数组数目。**  

## 反思  

- **第一反应**：直接想到枚举所有子数组，检查奇数个数。  
- **最容易踩的坑**  
  - 忘记在遍历时把「奇数」映射成 `1`，导致前缀和统计错误。  
  - 忘记初始化 `cnt[0] = 1`，会漏掉从数组开头就已经满足条件的子数组。  
  - 对于极端输入（全偶数或全奇数），要确保算法仍能返回 `0` 或正确的计数。  
- **下次遇到同类题的第一步**：**先把数组二值化（奇数→1，偶数→0），思考“前缀和差等于 k” 的计数方式**，然后决定是用哈希表还是滑动窗口实现。