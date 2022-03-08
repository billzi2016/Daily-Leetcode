# #1695. 最大擦除值 / Maximum Erasure Value

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-erasure-value/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums and want to erase a subarray containing unique elements. The score you get by erasing the subarray is equal to the sum of its elements.
Return the maximum score you can get by erasing exactly one subarray.
An array b is called to be a subarray of a if it forms a contiguous subsequence of a, that is, if it is equal to a[l],a[l+1],...,a[r] for some (l,r).

**Examples**

**Example 1:**

```
Input: nums = [4,2,4,5,6]
Output: 17
Explanation: The optimal subarray here is [2,4,5,6].
```

**Example 2:**

```
Input: nums = [5,2,1,2,5,2,1,2,5]
Output: 8
Explanation: The optimal subarray here is [5,2,1] or [1,2,5].
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个正整数数组 `nums`，要求擦除一个只包含唯一元素的子数组（subarray）。擦除该子数组得到的得分等于其所有元素之和。返回恰好擦除 **一个** 子数组所能获得的最大得分。

数组 `b` 被称为数组 `a` 的子数组（subarray），如果它是 `a` 的一个连续子序列（contiguous subsequence），即存在下标对 `(l, r)` 使得 `b = a[l], a[l+1], ..., a[r]`。

## 示例

### 示例 1

**输入**  
`nums = [4,2,4,5,6]`

**输出**  
`17`

**解释**  
最优的子数组是 `[2,4,5,6]`，其元素和为 `2+4+5+6 = 17`。

### 示例 2

**输入**  
`nums = [5,2,1,2,5,2,1,2,5]`

**输出**  
`8`

**解释**  
最优的子数组可以是 `[5,2,1]` 或 `[1,2,5]`，两者的元素和均为 `8`。

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把所有可能的连续子数组都枚举一遍**，对每个子数组判断它是否满足“所有元素唯一”，如果满足就把子数组的元素求和，最后取最大的和。

- **枚举子数组**：可以用两个循环，外层循环固定左边界 `l`，内层循环让右边界 `r` 从 `l` 移动到数组末尾，这样就遍历了所有 `[l, r]` 的连续区间。
- **判断唯一性**：遍历子数组的过程中，用一个集合（`set`）记录已经出现过的数字。集合的工作方式可以类比为“查字典”：我们把每个数字当作单词，集合里存的是已经出现过的单词，遇到已经在集合里的数字就说明出现了重复。
- **计算子数组和**：在遍历子数组的同时累加元素得到当前子数组的和。

这种方法一定能得到正确答案，因为它把**所有合法的子数组**都检查了一遍。

**时间/空间分析（大白话版）**  
- 外层循环跑 `n` 次，内层最坏情况下也会跑 `n` 次，所以总共大约是 `n × n`，即 **O(n²)**。把它想象成你在一张长方形网格里，从左上角走到右下角的每一条横向路径，都要走一次，步数是面积的平方级别。
- 需要一个集合来存放当前子数组里出现的数字，最坏情况下集合里会有 `n` 个元素，所以 **O(n)** 的额外空间。

#### 代码（Python）

```python
from typing import List

def maximumUniqueSubarray_brute(nums: List[int]) -> int:
    n = len(nums)
    ans = 0                         # 记录最大得分
    for left in range(n):           # 枚举左边界
        seen = set()                # 用来判断唯一性，类似查字典
        cur_sum = 0                 # 当前子数组的和
        for right in range(left, n):   # 右边界向右扩展
            if nums[right] in seen:     # 出现重复，子数组不合法，直接结束本次内层循环
                break
            seen.add(nums[right])       # 把新元素记进集合
            cur_sum += nums[right]      # 累加和
            ans = max(ans, cur_sum)     # 更新全局最大
    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n²)**  
  这表示当数组长度 `n` 加倍时，运行时间大约会增加 **四倍**（因为平方关系）。对 10⁵ 长度的数组来说，几乎不可能在合理时间内跑完。
- **空间复杂度**：**O(n)**  
  主要是集合 `seen` 最多会保存 `n` 个不同的数字。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次左边界固定后，都要重新遍历右边界并重新建立集合**。其实我们可以让左右边界像“滑动的窗帘”一样一起向右移动，只要保证窗口内部元素唯一，就不需要每次都从头检查。

**核心技巧：滑动窗口 + 哈希表（集合）**  

1. **左指针 `left`、右指针 `right`**：窗口是 `[left, right)`（左闭右开），`right` 每次向右扩展一个元素。
2. **集合 `window`**：记录当前窗口里出现的数字。  
   - 如果 `nums[right]` **不在** `window`，说明加入后仍然唯一，直接把它加入集合，`right` 前进一步，同时把它的值加到当前窗口的和 `cur_sum` 中。  
   - 如果 `nums[right]` **已经在** `window`，说明窗口出现了重复，这时候要把左边界 `left` 向右移动，**逐个移除**左侧的元素（从集合中删掉，`cur_sum` 减去对应值），直到把重复的那个数字踢出窗口为止。这样窗口再次恢复唯一性后，就可以继续向右扩展。
3. **维护最大和**：每次窗口合法（即所有元素唯一）时，用 `ans = max(ans, cur_sum)` 更新答案。

**为什么这样快？**  
- 每个元素最多会被 **加入集合一次、移出集合一次**，所以整体操作次数是线性的 `O(n)`，不像暴力解那样会重复检查同一个元素很多次。可以把它想象成 **一次遍历的旅程**：指针只会向前走，不会回头。
- 集合的“查字典”操作（`in`、`add`、`remove`）在平均情况下都是 **O(1)**，所以整体仍是线性时间。

#### 代码（Python）

```python
from typing import List

def maximumUniqueSubarray(nums: List[int]) -> int:
    left = 0                     # 窗口左边界
    cur_sum = 0                  # 当前窗口元素之和
    ans = 0                      # 记录最大得分
    window = set()               # 哈希集合，记录窗口内的数字（相当于查字典）

    for right, val in enumerate(nums):   # 右指针从左到右遍历每个元素
        # 如果出现重复，需要收缩左边界，直到窗口重新唯一
        while val in window:
            # 移除左边界的元素
            window.remove(nums[left])
            cur_sum -= nums[left]   # 同时把它的值从当前和中减去
            left += 1                # 左指针右移一格

        # 此时窗口已无重复，可以安全加入当前元素
        window.add(val)
        cur_sum += val               # 更新窗口和

        # 更新答案：当前窗口已经满足“唯一元素”，比较最大值
        ans = max(ans, cur_sum)

    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n)**  
  每个元素最多进出集合一次，指针只向右走一次。对长度为 10⁵ 的数组也能在毫秒级完成。  
- **空间复杂度**：**O(m)**（`m` 为窗口内不同元素的个数，最坏情况下 `m ≤ n`）  
  只需要保存当前窗口的元素集合，最多占用 `n` 个整数的空间。

---

## 心得  

- **核心技巧**：**滑动窗口**（Two‑Pointer）配合 **哈希集合** 检查唯一性。  
- **适用场景**：  
  1. **最长子串不含重复字符**（LeetCode 3）  
  2. **无重复子数组的最大和**（本题）  
  3. **子数组之和小于 K 的最长长度**（LeetCode 862）  
- **解题钥匙**：**“让窗口一直保持合法”，每次非法就收缩左边界，合法时更新答案”。**  

---

## 反思  

- **第一反应**：看到“子数组必须唯一”，立刻想到“集合”来判断唯一，随后想到“遍历所有子数组”。这就是暴力解的起点。  
- **最容易踩的坑**：  
  - **忘记在收缩窗口时同步更新当前和 `cur_sum`**，导致答案偏大。  
  - **循环条件写错**，比如在 `while val in window:` 里忘记移动左指针，导致死循环。  
  - **边界情况**：数组长度为 1 时，直接返回该元素；全部元素相同时，窗口只能容纳一个元素。  
- **下次思路**：看到“子数组/子串 + 唯一/满足某种约束”，第一步就想 **滑动窗口**，再判断是否需要哈希结构来快速判断合法性。这样可以迅速从暴力思路跳到线性解。