# #1658. 最小操作次数使 X 减至 0 / Minimum Operations to Reduce X to Zero

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer x. In one operation, you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x. Note that this modifies the array for future operations.
Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.

**Examples**

**Example 1:**

```
Input: nums = [1,1,4,2,3], x = 5
Output: 2
Explanation: The optimal solution is to remove the last two elements to reduce x to zero.
```

**Example 2:**

```
Input: nums = [5,6,7,8,9], x = 4
Output: -1
```

**Example 3:**

```
Input: nums = [3,2,20,1,1,3], x = 10
Output: 5
Explanation: The optimal solution is to remove the last three elements and the first two elements (5 operations in total) to reduce x to zero.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 104
- 1 <= x <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `x`。一次操作中，你可以移除数组 `nums` 的最左侧或最右侧的元素，并将该元素的值从 `x` 中减去。注意，移除元素后数组会发生改变，后续的操作基于修改后的数组。  

返回将 `x` 精确减至 0 所需的最少操作次数；如果无法做到，返回 `-1`。  

### 示例

**示例 1**  
```
Input: nums = [1,1,4,2,3], x = 5
Output: 2
Explanation: 最优的做法是移除最后两个元素，使 x 减至 0。
```

**示例 2**  
```
Input: nums = [5,6,7,8,9], x = 4
Output: -1
```

**示例 3**  
```
Input: nums = [3,2,20,1,1,3], x = 10
Output: 5
Explanation: 最优的做法是先移除最后三个元素，再移除前两个元素（共 5 次操作），使 x 减至 0。
```

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^4`
- `1 <= x <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的取法**。  
因为每一步只能从左边或右边拿走一个元素，我们可以把操作次数记为 `k`，然后把 `k` 分成左边取 `i` 个，右边取 `k‑i` 个，两部分的和必须等于 `x`。

实现思路：

1. 从左侧取 `i`（`0 ≤ i ≤ n`）个元素，计算它们的和 `left_sum`。  
2. 从右侧取 `j`（`0 ≤ j ≤ n‑i`）个元素，计算它们的和 `right_sum`。  
3. 若 `left_sum + right_sum == x`，则 `i + j` 是一种合法的操作数，记录最小值。  

> **数据结构类比**：这里的“取左边/右边的元素”就像我们在排队买票，左边是从队头买，右边是从队尾买。我们要尝试所有可能的“买多少人”，所以要遍历所有组合。

这种做法必然能得到答案，因为它把**所有可能的前缀 + 后缀组合**都检查了一遍。

#### 代码（Python）

```python
from typing import List

def min_operations_bruteforce(nums: List[int], x: int) -> int:
    n = len(nums)
    ans = float('inf')                     # 用正无穷表示还没有找到合法解

    # 前缀和数组，prefix[i] 表示前 i 个元素的和（不含 nums[i]）
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    # 后缀和数组，suffix[i] 表示从 i 开始到结尾的和
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + nums[i]

    # 枚举左侧取 i 个，右侧取 j 个
    for i in range(n + 1):                 # i = 0 表示不取左侧
        left_sum = prefix[i]
        # 右侧最多还能取 n-i 个，防止取到同一个元素两次
        for j in range(n - i + 1):
            right_sum = suffix[n - j]      # suffix 的起点是 n-j
            if left_sum + right_sum == x:
                ans = min(ans, i + j)      # 记录最小操作数

    return -1 if ans == float('inf') else ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：外层循环遍历 `i = 0 … n`，内层循环遍历 `j = 0 … n‑i`，最坏情况相当于遍历了约 `n·n/2` 次，俗称“平方级”，即使 `n = 10⁵` 也会超时。  
- **空间复杂度**：`O(n)`  
  解释：我们用了两个长度为 `n+1` 的前缀/后缀和数组，额外空间随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有左/右组合**，导致二次循环。  
观察题目可以把它翻个身来看：

> 把从左边或右边拿走的元素的和设为 `x`，等价于**在原数组中留下一个连续子数组**，它的和恰好是 `total_sum - x`（其中 `total_sum` 是整个数组的和）。

**为什么？**  
把左/右两端的元素全部删掉后，数组剩下的部分就是我们**没有取走**的元素。  
设剩下的子数组和为 `remain`，则被删掉的元素和为 `total_sum - remain`，而题目要求删掉的元素和正好是 `x`，于是：

```
total_sum - remain = x  →  remain = total_sum - x
```

于是问题转化为：

> 在数组 `nums` 中，找到 **和为 `target = total_sum - x` 的最长连续子数组**。  
> 最少操作数 = `n - length_of_this_subarray`（因为我们只需要删掉其余的元素）。

这就是**最长子数组和为固定值**的问题，可以用**前缀和 + 哈希表**或**滑动窗口**在 `O(n)` 时间内解决。

因为数组中所有元素都是正数（`nums[i] ≥ 1`），**滑动窗口**特别适用：窗口的和只能增大或减小，不会出现负数导致的回退。

**滑动窗口核心步骤**（类比：在走廊里放一根绳子，两端可以向前或向后移动，绳子内的总重量要恰好等于目标）：

1. 用两个指针 `left`、`right` 表示当前窗口 `[left, right)`（左闭右开）。  
2. `curr_sum` 保存窗口内元素的和。  
3. 不断右移 `right`，把新元素加进窗口。  
4. 如果 `curr_sum` 超过 `target`，就左移 `left`，把左端元素移出窗口，直到 `curr_sum ≤ target`。  
5. 每次 `curr_sum == target` 时，更新 **最长长度**。

如果 `target` 为负数（即 `x > total_sum`），显然不可能完成，直接返回 `-1`。

#### 代码（Python）

```python
from typing import List

def min_operations(nums: List[int], x: int) -> int:
    total = sum(nums)
    target = total - x                     # 我们希望保留下来的子数组和

    if target < 0:                         # x 太大，根本删不完
        return -1

    n = len(nums)
    left = 0
    curr_sum = 0
    max_len = -1                           # 记录满足条件的最长子数组长度

    for right in range(n):                 # right 依次指向每个元素
        curr_sum += nums[right]            # 把 nums[right] 加入窗口

        # 当窗口和大于 target 时，左指针右移，缩小窗口
        while curr_sum > target and left <= right:
            curr_sum -= nums[left]
            left += 1

        # 此时窗口和要么等于 target，要么小于 target
        if curr_sum == target:
            max_len = max(max_len, right - left + 1)   # 更新最长长度

    # 如果没有找到合法子数组，说明无法凑成 x
    if max_len == -1:
        return -1
    # 最少操作数 = 总长度 - 保留下来的子数组长度
    return n - max_len
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：`right` 指针遍历一次数组，`left` 指针最多也只会向右移动 `n` 步，整体线性。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(1)`  
  解释：只用了若干个整数变量，额外空间不随 `n` 增长。

---

## 心得

- **核心技巧**：把“从两端删元素”转换为“保留中间最长子数组”。这是一种**逆向思维**的典型例子。  
- **适用场景**：  
  1. “找最长子数组，使其和等于给定值”——如 LeetCode 525 *Contiguous Array*（求最长子数组和为 0）  
  2. “删除最少元素使数组和等于目标”——如 LeetCode 1658 *Minimum Operations to Reduce X to Zero*（本题）  
  3. “在正数数组中找最短子数组，使其和 ≥ target”——如 LeetCode 209 *Minimum Size Subarray Sum*（滑动窗口的另一种变形）  
- **一句话总结解题钥匙**：**把两端的删除转成中间的保留，目标变成“最长等和子数组”。**

---

## 反思

- **第一反应**：直接想到枚举左/右的取法，用双层循环暴力搜索。  
- **最容易踩的坑**：  
  - 忘记检查 `x > total_sum` 的情况，会导致 `target` 为负数而进入无效的滑动窗口循环。  
  - 滑动窗口实现时，`while` 循环的退出条件一定要写对，防止左指针越界或死循环。  
- **下次遇到同类题**，第一步应该问自己：“是否可以把“从两端操作”转成“保留中间子数组””，或者“能否把问题倒着思考，寻找等价的子问题”。这样往往能把时间复杂度从平方级降到线性级。