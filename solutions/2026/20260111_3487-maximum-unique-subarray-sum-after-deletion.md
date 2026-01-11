# #3487. 最大唯一子数组和（Maximum Unique Subarray Sum After Deletion） / Maximum Unique Subarray Sum After Deletion

> 难度：简单 · 标签：Array、Hash Table、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-unique-subarray-sum-after-deletion/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
You are allowed to delete any number of elements from nums without making it empty. After performing the deletions, select a subarray of nums such that:
Return the maximum sum of such a subarray.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,5]
Output: 15
Explanation:
Select the entire array without deleting any element to obtain the maximum sum.
```

**Example 2:**

```
Input: nums = [1,1,0,1,1]
Output: 1
Explanation:
Delete the element nums[0] == 1 , nums[1] == 1 , nums[2] == 0 , and nums[3] == 1 . Select the entire array [1] to obtain the maximum sum.
```

**Example 3:**

```
Input: nums = [1,2,-1,-2,1,0,-1]
Output: 3
Explanation:
Delete the elements nums[2] == -1 and nums[3] == -2 , and select the subarray [2, 1] from [1, 2, 1, 0, -1] to obtain the maximum sum.
```

**Constraints**

- 1 <= nums.length <= 100
- -100 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
你可以删除任意数量的元素（但不能将数组删空），随后在剩余的数组中选择一个子数组（subarray），要求该子数组中的所有元素互不相同。返回所有满足条件的子数组中可能的最大和。

**示例 1**  
**输入**: `nums = [1,2,3,4,5]`  
**输出**: `15`  
**解释**: 不删除任何元素，直接选择整个数组即可得到最大和。

**示例 2**  
**输入**: `nums = [1,1,0,1,1]`  
**输出**: `1`  
**解释**: 删除 `nums[0] = 1`、`nums[1] = 1`、`nums[2] = 0`、`nums[3] = 1`，剩下的数组为 `[1]`，选择它得到最大和。

**示例 3**  
**输入**: `nums = [1,2,-1,-2,1,0,-1]`  
**输出**: `3`  
**解释**: 删除 `nums[2] = -1` 和 `nums[3] = -2`，得到数组 `[1,2,1,0,-1]`。在其中选择子数组 `[2,1]`，其和为 `3`，为最大可能和。

**约束条件**  
- `1 <= nums.length <= 100`  
- `-100 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子数组**（连续的一段），判断这段子数组里是否满足“所有元素唯一”，如果满足就计算它的和，取最大值。

- **数据结构**：  
  - **集合（Set）**：就像查字典一样，往集合里放元素时如果已经存在，就说明出现了重复。  
- **为什么正确**：  
  - 题目要求在删除任意元素后再选取一个子数组，使得子数组中没有重复元素且和最大。遍历所有子数组相当于把“删除”这一步全部考虑进去（因为任意子数组都可以通过删除不在该子数组的元素得到）。只要子数组内部元素唯一，就一定是合法的选择。  
- **复杂度分析**：  
  - 枚举子数组有 `n` 个起点，每个起点最多往后扩展 `n` 步，总共大约 `n²` 次。  
  - 对每个子数组，我们要检查是否有重复，这可以在遍历子数组时用集合记录，最坏情况要遍历子数组长度 `O(n)`，所以整体时间是 **O(n³)**。如果我们在遍历时直接检查并在发现重复时提前结束，则实际会接近 **O(n²)**。  
  - 额外空间只需要一个集合，最多装下 `n` 个元素，**O(n)**。

#### 代码（Python）

```python
from typing import List

def max_unique_subarray_sum_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best = float('-inf')                     # 用来保存全局最大和

    # 枚举子数组的左端点
    for left in range(n):
        seen = set()                          # 记录当前子数组里出现过的数
        cur_sum = 0

        # 枚举右端点，逐步扩展子数组
        for right in range(left, n):
            val = nums[right]

            # 如果出现了重复，后面的更长子数组肯定也会有重复，直接结束这一行
            if val in seen:
                break

            seen.add(val)                     # 把新元素加入集合
            cur_sum += val                     # 更新子数组的和
            best = max(best, cur_sum)         # 更新全局最大

    # 若所有数都是负数，best 已经是最大的负数
    return best
```

#### 复杂度

- **时间复杂度**：**O(n²)**（最坏情况下每个左端点会遍历到右端点，且一旦出现重复立即退出）。
- **空间复杂度**：**O(n)**（集合最多保存 `n` 个不同的元素）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于大量的子数组枚举**。其实这道题可以用更高层次的观察来直接得到答案：

1. **如果数组里全是负数**，不管怎么删，选到的子数组里至少会有一个元素，而所有负数的和只会更小。此时**最大子数组和就是最大的那个负数**。  
2. **只要数组里出现了非负数（0 或正数）**，我们完全可以把所有负数全部删掉，只保留**每个非负数的唯一一次出现**。因为  
   - 负数删掉不会让和变小（负数加进去只会让和更小）。  
   - 同一个正数出现多次会导致“元素不唯一”，我们只能保留一次，否则子数组不合法。  
   - 只要把所有 **不重复的非负数** 放在一起，它们本身已经构成一个合法的子数组（删掉中间的负数或重复的正数即可），而它们的和显然是最大的可能。  

于是答案就是：

- 若所有元素都 < 0，返回 `max(nums)`。  
- 否则，返回 **所有唯一的非负数的总和**。  

这一步只需要一次遍历，用 **集合** 记录已经出现过的非负数，累计求和即可。

#### 代码（Python）

```python
from typing import List

def maximum_unique_subarray_sum(nums: List[int]) -> int:
    """
    最优解：一次遍历即可求得答案
    """
    # 先检查是否全为负数
    max_elem = max(nums)                # 最大元素
    if max_elem < 0:                     # 全负数的情况
        return max_elem

    # 至少有一个非负数，统计所有唯一的非负数
    seen = set()
    total = 0
    for v in nums:
        if v >= 0 and v not in seen:    # 只加第一次出现的非负数
            seen.add(v)
            total += v
    return total
```

#### 复杂度

- **时间复杂度**：**O(n)**（只遍历一次数组）。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：**O(k)**，其中 `k` 是不同的非负数的个数，最坏 `k ≤ n`，所以仍是线性空间。

---

## 心得

- **核心技巧**：利用**全局唯一非负数的性质**直接求和，避免枚举子数组。  
- **适用的题型**：  
  1. “在数组中删除元素后满足某种唯一性或非负性条件的最大和”  
  2. “只保留满足特定属性的唯一元素求和”  
  3. “全部为负数时返回最大负数”的特殊判定（常见于最大子数组类问题）  
- **解题钥匙**：**先观察极端情况（全负）再利用集合去重的“唯一+非负”特性**。

---

## 反思

- **第一反应**：直接想到遍历所有子数组检查唯一性，写出暴力解。  
- **最容易踩的坑**：  
  - 忽略了 **全负数** 的特殊情况，直接返回 0 会错误。  
  - 没有注意到 **重复的正数** 必须只算一次，否则会违反唯一性。  
- **下次思路**：看到“删除任意元素后再选子数组”这类描述时，第一步先思考是否可以**把所有不想要的元素一次性全部删掉**（如负数或重复），再看剩余元素能否直接构成答案。这样往往能把复杂的枚举转化为一次线性扫描。