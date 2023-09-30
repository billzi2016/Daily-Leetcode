# #2419. 最大按位与的最长子数组 / Longest Subarray With Maximum Bitwise AND

> 难度：中等 · 标签：Array、Bit Manipulation、Brainteaser · [LeetCode 链接](https://leetcode.com/problems/longest-subarray-with-maximum-bitwise-and/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of size n.
Consider a non-empty subarray from nums that has the maximum possible bitwise AND.
Return the length of the longest such subarray.
The bitwise AND of an array is the bitwise AND of all the numbers in it.
A subarray is a contiguous sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,3,2,2]
Output: 2
Explanation:
The maximum possible bitwise AND of a subarray is 3.
The longest subarray with that value is [3,3], so we return 2.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 1
Explanation:
The maximum possible bitwise AND of a subarray is 4.
The longest subarray with that value is [4], so we return 1.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个大小为 `n` 的整数数组 `nums`。  
考虑所有非空的子数组（subarray），其中 **按位与（bitwise AND）** 的值是可能的最大值。  
返回满足该条件的最长子数组的长度。

**按位与** 是指对数组中的所有数字逐位执行 AND 运算得到的结果。  
子数组是数组中连续的元素序列。

## 示例

### 示例 1
**输入**  
`nums = [1,2,3,3,2,2]`

**输出**  
`2`

**解释**  
子数组的最大可能 **按位与** 为 `3`。  
拥有该值的最长子数组是 `[3,3]`，因此返回 `2`。

### 示例 2
**输入**  
`nums = [1,2,3,4]`

**输出**  
`1`

**解释**  
子数组的最大可能 **按位与** 为 `4`。  
拥有该值的最长子数组是 `[4]`，因此返回 `1`。

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **枚举所有子数组**，把子数组里的数全部做按位与（AND），记录下出现的最大 AND 值以及对应的最长长度。

- **数据结构**：我们只需要普通的列表 `nums`。在枚举子数组时，用两个循环分别固定子数组的左端点 `i` 和右端点 `j`，用一个变量 `cur` 累计 `nums[i] & nums[i+1] & … & nums[j]`。  
  - 按位与运算可以想象成 **查字典**：字典里每个单词对应的页码是 0/1 位，取交集（AND）后只保留下两本书都有的页码。  
- **为什么正确**：因为我们把 **每一种可能的连续子序列** 都算了一遍，最大 AND 肯定会在这些候选里出现，随后再统计最长的长度也不可能漏掉。

#### 代码（Python）

```python
def longestSubarray_bruteforce(nums):
    n = len(nums)
    max_and = -1          # 记录出现过的最大 AND
    best_len = 0          # 对应的最长长度

    # i 为子数组左端点
    for i in range(n):
        cur = nums[i]     # 当前子数组的 AND，先放第 i 个数
        # j 为子数组右端点（包含）
        for j in range(i, n):
            if j > i:                     # 第一次循环已经算了 nums[i]
                cur &= nums[j]            # 累计 AND
            # 更新最大 AND 与对应长度
            if cur > max_and:
                max_and = cur
                best_len = j - i + 1
            elif cur == max_and:
                best_len = max(best_len, j - i + 1)
    return best_len
```

> **关键注释**  
> - `cur &= nums[j]`：把新加入的元素和已有的 AND 结果再做一次 AND，就相当于把字典里再加一本书再取交集。  
> - `j - i + 1`：子数组长度 = 右端点 - 左端点 + 1。

#### 复杂度

- **时间复杂度**：`O(n²)`。外层遍历 `n` 次，内层最坏也遍历 `n` 次，等价于“把所有可能的子数组都算一遍”。  
  - 大白话：如果数组有 10,000 个数，暴力解要算大约 `10,000 × 10,000 / 2 ≈ 5×10⁷` 次 AND，明显会超时。  
- **空间复杂度**：`O(1)`。只用了常数个额外变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈** 在于我们把所有子数组都遍历了一遍。观察按位与的性质可以把搜索空间立刻压到 `O(n)`。

1. **AND 的单调性**  
   - 对任意两个不同的整数 `a`、`b`，`a & b` **一定小于** `max(a, b)`。因为在二进制里，最高位上如果两个数不相同，`&` 结果该位必为 0，导致整体数值变小。  
   - 这说明 **子数组的 AND 永远不可能超过子数组里最大的那个元素**。

2. **最大可能的 AND**  
   - 整个数组里最大的数记为 `mx`。显然，单独取这个元素组成的子数组的 AND 就是 `mx`，所以 **最大可能的 AND 必定是 `mx`**。  
   - 若想让子数组的 AND 仍然是 `mx`，子数组里 **不能出现比 `mx` 小的数**，因为只要有一个更小的数参与 AND，结果就会立刻下降。

3. **把问题转化**  
   - 因此，满足 “子数组 AND = mx” 的子数组 **恰好是只包含 `mx` 的连续片段**。  
   - 任务变成：**在数组中找出最长的、全部由 `mx` 组成的连续子数组**。

4. **线性扫描**  
   - 首先遍历一次得到 `mx = max(nums)`（O(n)）。  
   - 再一次遍历，用一个计数器 `cnt` 记录当前连续 `mx` 的个数，遇到非 `mx` 时把 `cnt` 与答案 `ans` 比较后归零。  
   - 整个过程只需要两次线性遍历，时间 `O(n)`，空间 `O(1)`。

> **类比**：把数组想象成一条路，`mx` 是路上最高的山峰。我们要找最长的“只走在最高山峰上的路段”。只要一旦下坡（出现更小的数字），这段路就不符合要求，计数重新开始。

#### 代码（Python）

```python
def longestSubarray(nums):
    """
    返回最长子数组的长度，使其按位与等于所有子数组可能的最大值。
    思路：最大 AND 必然是数组中的最大元素 mx，
          只有全由 mx 组成的连续段才能保持 AND = mx。
    """
    # 1️⃣ 找到数组的最大值
    mx = max(nums)                 # O(n) 的一次遍历

    # 2️⃣ 再遍历一次，统计最长连续 mx 的长度
    ans = 0        # 最终答案
    cnt = 0        # 当前连续 mx 的计数

    for v in nums:                 # O(n) 的第二次遍历
        if v == mx:                # 仍然在“最高山峰”上
            cnt += 1               # 继续累加长度
        else:                      # 遇到更低的山，计数结束
            ans = max(ans, cnt)    # 更新答案
            cnt = 0                # 重新计数

    # 循环结束后，可能最后一段就是最长的，需要再比较一次
    ans = max(ans, cnt)

    return ans
```

> **关键注释**  
> - `mx = max(nums)`：相当于先在地图上标出最高峰的海拔。  
> - `if v == mx: cnt += 1`：只要还在最高峰上，就继续走；一旦下坡，计数清零。  
> - `ans = max(ans, cnt)`：随时保存目前为止走过的最长“最高峰路段”。

#### 复杂度

- **时间复杂度**：`O(n)`。只遍历两遍数组，`n` 最多是 `10⁵`，轻松在毫秒级完成。  
  - 与暴力解相比，从 **`n²` 次计算** 降到了 **`n` 次**，速度提升约 `n` 倍（比如 `10⁵` 时提升 100,000 倍）。
- **空间复杂度**：`O(1)`。只用几个整数变量，和输入规模无关。

---

## 心得

- **核心技巧**：利用 **按位与的单调下降特性** 把“最大 AND”锁定为数组的最大元素，然后把原题转化为 “最长连续相同元素” 的统计问题。  
- **适用的题型**  
  1. “子数组/子序列的最大/最小 X 运算值” 类题（如最大 XOR、最小 OR 等），常通过 **单调性** 或 **位运算特性** 把搜索空间压缩。  
  2. “在满足某个条件的子数组中找最长/最短”——常用 **双指针 / 滑动窗口** 或 **一次线性扫描**。  
- **一句话总结**：**先找出答案的上界（这里是最大元素），再把子数组限制在只能出现上界的区间，就能线性求解**。

---

## 反思

- **第一反应**：看到“最大可能的按位与”，第一时间会想到枚举所有子数组，直接计算 AND，虽然能得到答案，但显然太慢。  
- **最容易踩的坑**  
  - 忽视 **AND 的单调下降**：以为需要考虑多个不同数的组合，导致不必要的复杂度。  
  - 忽略 **边界情况**：如所有元素都相同（答案是整个数组长度），或数组只有一个元素（答案 1）。  
- **下次遇到同类题**，第一步应该问自己：“**这个运算的结果能超过数组里最大的（或最小的）元素吗？**”。如果不能，就把问题转化为“只包含该极值的子数组”。这样往往能快速找到线性或近线性的解法。