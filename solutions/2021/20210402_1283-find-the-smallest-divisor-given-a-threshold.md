# #1283. 找出满足阈值的最小除数 / Find the Smallest Divisor Given a Threshold

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and an integer threshold, we will choose a positive integer divisor, divide all the array by it, and sum the division's result. Find the smallest divisor such that the result mentioned above is less than or equal to threshold.
Each result of the division is rounded to the nearest integer greater than or equal to that element. (For example: 7/3 = 3 and 10/2 = 5).
The test cases are generated so that there will be an answer.

**Examples**

**Example 1:**

```
Input: nums = [1,2,5,9], threshold = 6
Output: 5
Explanation: We can get a sum to 17 (1+2+5+9) if the divisor is 1. 
If the divisor is 4 we can get a sum of 7 (1+1+2+3) and if the divisor is 5 the sum will be 5 (1+1+1+2).
```

**Example 2:**

```
Input: nums = [44,22,33,11,1], threshold = 5
Output: 44
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- 1 <= nums[i] <= 106
- nums.length <= threshold <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数阈值 `threshold`，我们需要选取一个 **正整数除数**（divisor），用它去除数组中的每个元素，并将所有除法结果相加。求使得上述和 **小于等于** `threshold` 的 **最小除数**。

对每个元素的除法结果采用 **向上取整**（ceil），即取大于等于该商的最小整数。例如：`7 / 3 = 3`，`10 / 2 = 5`。

题目保证一定存在答案。

**示例 1**  
**输入**: `nums = [1,2,5,9]`, `threshold = 6`  
**输出**: `5`  
**解释**: 当除数为 `1` 时，和为 `1+2+5+9 = 17`。  
当除数为 `4` 时，和为 `1+1+2+3 = 7`。  
当除数为 `5` 时，和为 `1+1+1+2 = 5`，此时已满足 ≤ `threshold`，且 `5` 是最小的满足条件的除数。

**示例 2**  
**输入**: `nums = [44,22,33,11,1]`, `threshold = 5`  
**输出**: `44`

**约束条件**
- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^6`
- `nums.length <= threshold <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的除数**，把数组里的每个数除以这个除数（向上取整），把得到的结果相加，检查是否 ≤ `threshold`。  
只要找到了满足条件的除数，就记录下来，最后取最小的那个。

- **数据结构**：我们只需要遍历 `nums`，所以只用到最普通的 **列表**（list）。可以把它想象成一排装着水果的篮子，遍历篮子时把每个水果切成若干块（除以除数），剩余的碎块向上凑整块（向上取整）。
- **正确性**：因为题目保证一定有解，只要我们把**所有正整数除数**（从 1 开始，一直往上）都尝试一次，必然能找到满足条件的最小除数。
- **时间/空间分析**：  
  - 枚举除数的上界可以取 `max(nums)`（因为除数大于最大元素时，每个 `ceil(num/divisor)` 都会是 1，已经是最小可能的和）。  
  - 对每个除数我们都要遍历一次数组，时间复杂度是 `O(max(nums) * n)`，其中 `n = len(nums)`。如果 `max(nums)` 达到 `10⁶`，`n` 达到 `5·10⁴`，这会非常慢。  
  - 只使用常数级别的额外空间 `O(1)`（不计输入数组本身）。

> **大白话**：  
> - `O(n²)` 里的 `n` 不是指数组长度，而是“可能的除数数量”。如果可能的除数有 10 万个，而数组有 5 万个，遍历一次的工作量就是 10 万 × 5 万 = 5 × 10⁹ 次，计算机会受不了。

#### 代码（Python）

```python
import math
from typing import List

def smallestDivisor_bruteforce(nums: List[int], threshold: int) -> int:
    # 可能的除数最大不需要超过数组里的最大值
    for divisor in range(1, max(nums) + 1):
        total = 0                     # 累计除后的和
        for x in nums:
            # math.ceil 相当于“向上取整”，也可以写成 (x + divisor - 1) // divisor
            total += math.ceil(x / divisor)
        if total <= threshold:        # 找到第一个满足条件的除数，就是最小的
            return divisor
    # 题目保证一定有解，这行理论上不会被执行
    return -1
```

#### 复杂度

- **时间复杂度**：`O(max(nums) * n)`  
  - `max(nums)` 是可能的除数个数，`n` 是数组长度。  
  - 在最坏情况下相当于把每个可能的除数都“尝一遍”。
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**线性枚举除数**。观察可以发现：

- 当除数变大时，每个 `ceil(num / divisor)` **单调不增**（除数越大，结果越小或相等），因此 **总和** 也是单调不增的。  
- 单调性意味着我们可以用 **二分查找**（binary search）在除数的取值区间 `[1, max(nums)]` 中快速定位最小满足条件的除数。

二分查找的核心是**判断函数** `ok(d)`：  
> “当除数 = `d` 时，`sum(ceil(num / d))` 是否 ≤ `threshold`？”

如果 `ok(d)` 为真，说明 `d` 已经足够大，左边的更小除数可能不满足，我们可以把搜索区间收缩到 `[low, d]`（包括 `d`）。  
如果 `ok(d)` 为假，则说明 `d` 太小，需要把区间移动到 `[d+1, high]`。

二分查找的每一步都只遍历一次数组来计算 `ok(d)`，时间是 `O(n)`，而二分的迭代次数是 `log₂(max(nums))`（最多约 20 次，因为 `max(nums) ≤ 10⁶`），所以总时间是 `O(n log max(nums))`，足够快。

**关键概念解释**  

- **二分查找**：把一个有序（这里是单调）区间不断“对半砍”，每次排除掉不可能的半边，直至只剩下答案。可以把它想象成在一本字典里找某个单词的过程：先看中间的页码，如果目标在前面就往前翻，否则往后翻。
- **向上取整**：`ceil(a / b)` 等价于 `(a + b - 1) // b`（整数除法向下取整），这里我们加上 `b-1` 再除，以实现“凑满一整块”。例如 `7 / 3` → `(7+2)//3 = 9//3 = 3`。

#### 代码（Python）

```python
import math
from typing import List

def smallestDivisor(nums: List[int], threshold: int) -> int:
    """
    使用二分查找找到满足 sum(ceil(num / divisor)) <= threshold 的最小正整数 divisor。
    """
    # 二分的搜索区间
    low, high = 1, max(nums)          # 除数不可能小于 1，也不需要大于数组最大值

    # 判断函数：给定除数 d，返回是否满足阈值要求
    def ok(d: int) -> bool:
        total = 0
        for x in nums:
            # (x + d - 1) // d 等价于 math.ceil(x / d)
            total += (x + d - 1) // d
            # 早停：如果已经超过阈值，就不必继续累加
            if total > threshold:
                return False
        return True

    # 标准二分模板（寻找左边界）
    while low < high:
        mid = (low + high) // 2       # 取中间值，向下取整
        if ok(mid):                   # 如果 mid 已经足够大
            high = mid                # 把区间收紧到左半边，包括 mid
        else:
            low = mid + 1             # 否则答案一定在右半边
    return low                        # low == high，此时即为最小可行除数
```

#### 复杂度

- **时间复杂度**：`O(n log max(nums))`  
  - `log max(nums)` 是二分的层数（约 20 层），每层遍历数组一次 `O(n)`。相当于“把 5 万个数检查 20 次”，非常快。  
  - 与暴力的 `O(max(nums) * n)` 相比，省去了几乎所有不必要的遍历。
- **空间复杂度**：`O(1)`  
  - 只使用了常数个变量 (`low, high, mid, total`)。

---

## 心得

- **核心技巧**：利用**单调性 + 二分查找**把原本线性枚举的搜索空间压缩到对数级。  
- **适用的题型**：  
  1. “找到最小/最大满足某单调条件的数”——如 *寻找最小的容量使得搬家次数 ≤ k*（《Capacity To Ship Packages Within D Days》）。  
  2. “在有序或单调函数上搜索阈值”——如 *在数组中找最小的正整数使得…*（《Find Minimum Number of Days to Make m Bouquets》）。  
  3. “把问题转化为判断函数后二分”——如 *分配工作、划分子数组等*（《Split Array Largest Sum》）。
- **一句话总结**：**把“是否可行”抽象成一个单调布尔函数，二分定位最左侧的 True**。

---

## 反思

- **第一反应**：直接遍历所有除数，写一个 `for divisor in range(1, max(nums)+1)` 的循环。  
- **最容易踩的坑**：  
  - 忘记对除法结果**向上取整**，直接用 `//` 会导致结果偏小。  
  - 没有提前**剪枝**（如果累计和已经大于阈值就直接返回 False），会导致不必要的遍历，尤其在二分的 `ok` 函数里。  
  - 二分的区间边界写错：`low < high`、`mid = (low + high) // 2`、更新 `low = mid + 1` 或 `high = mid` 时要对应好“左边界/右边界”含义。
- **下次遇到同类题**：第一步先**确认是否存在单调性**（增/减），如果有，就立刻构造判断函数并使用二分搜索。这样可以把时间从线性甚至指数级降到对数级。