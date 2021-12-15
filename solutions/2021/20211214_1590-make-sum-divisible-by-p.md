# #1590. 使和可被 P 整除 / Make Sum Divisible by P

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/make-sum-divisible-by-p/)

---

## 题目（英文原版）

**Description**

Given an array of positive integers nums, remove the smallest subarray (possibly empty) such that the sum of the remaining elements is divisible by p. It is not allowed to remove the whole array.
Return the length of the smallest subarray that you need to remove, or -1 if it's impossible.
A subarray is defined as a contiguous block of elements in the array.

**Examples**

**Example 1:**

```
Input: nums = [3,1,4,2], p = 6
Output: 1
Explanation: The sum of the elements in nums is 10, which is not divisible by 6. We can remove the subarray [4], and the sum of the remaining elements is 6, which is divisible by 6.
```

**Example 2:**

```
Input: nums = [6,3,5,2], p = 9
Output: 2
Explanation: We cannot remove a single element to get a sum divisible by 9. The best way is to remove the subarray [5,2], leaving us with [6,3] with sum 9.
```

**Example 3:**

```
Input: nums = [1,2,3], p = 3
Output: 0
Explanation: Here the sum is 6. which is already divisible by 3. Thus we do not need to remove anything.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= p <= 109

---

## 题目（中文翻译）

给定一个只包含正整数（positive integers）的数组 **nums**，请移除最短的子数组（subarray）（可以为空），使得剩余元素的和能够被 **p** 整除。**不允许**移除整个数组。

返回需要移除的最短子数组的长度；如果不存在这样的子数组，则返回 **-1**。

子数组（subarray）定义为数组中连续的元素块（contiguous block of elements）。

## 示例

**示例 1**  
**输入**: `nums = [3,1,4,2]`, `p = 6`  
**输出**: `1`  
**解释**: 数组所有元素的和为 10，不能被 6 整除。我们可以移除子数组 `[4]`，此时剩余元素的和为 6，能够被 6 整除。

**示例 2**  
**输入**: `nums = [6,3,5,2]`, `p = 9`  
**输出**: `2`  
**解释**: 无法通过移除单个元素使和可被 9 整除。最佳方案是移除子数组 `[5,2]`，剩下的 `[6,3]` 的和为 9，满足要求。

**示例 3**  
**输入**: `nums = [1,2,3]`, `p = 3`  
**输出**: `0`  
**解释**: 整个数组的和为 6，已经能够被 3 整除，因此不需要移除任何元素。

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= p <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子数组**，把它们逐个尝试删除，看看剩余的和是否能被 `p` 整除。

- **子数组**：连续的一段元素，就像一根绳子被剪成若干段，只能从头或尾剪，不能跳着剪。
- **枚举方式**：双层循环，外层固定子数组的左端点 `i`，内层遍历右端点 `j`（`i ≤ j`），把 `nums[i…j]` 的和算出来，再用 `total - sub_sum` 判断能否被 `p` 整除。

为什么这个方法一定能得到答案？  
因为我们把**所有**合法的子数组都检查了一遍，只要有一种可以让剩余和被 `p` 整除，就一定会在枚举过程中被发现。于是最小长度自然会在所有满足条件的子数组中被挑选出来。

**时间/空间分析（大白话）**  
- 时间复杂度：外层 `n` 次，内层最坏也要遍历 `n` 次，算子数组和的过程再是 `O(1)`（用累加得到）。于是总共是 `O(n²)`，也就是“**平方级**”。如果 `n = 10⁵`，`n²` 会是 `10¹⁰`，远远超出机器在一秒内能做的运算量。
- 空间复杂度：只用了常数个额外变量（总和、子数组和、最小长度），所以是 `O(1)`，即“**常数级**”，几乎不占内存。

#### 代码（Python）

```python
from typing import List

def min_subarray_bruteforce(nums: List[int], p: int) -> int:
    n = len(nums)
    total = sum(nums)                     # 整个数组的和
    if total % p == 0:                    # 已经能被 p 整除，直接返回 0
        return 0

    target = total % p                    # 需要删除的子数组余数必须等于 target
    ans = n + 1                           # 用一个比最大可能长度大的数来做初始值

    # 前缀和数组，prefix[i] 表示 nums[0..i-1] 的和，方便快速求子数组和
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    # 枚举所有子数组
    for left in range(n):
        for right in range(left, n):
            sub_sum = prefix[right + 1] - prefix[left]   # 子数组 nums[left..right] 的和
            if sub_sum % p == target:                     # 删除后剩余和能被 p 整除
                ans = min(ans, right - left + 1)          # 记录最小长度

    return -1 if ans == n + 1 else ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有子数组，`n` 越大，耗时呈平方增长。  
- **空间复杂度**：`O(n)` —— 需要一个长度为 `n+1` 的前缀和数组；如果不使用前缀和，也只需要 `O(1)`。

> **小结**：暴力解思路简单、代码直观，但在本题的约束（`n ≤ 10⁵`）下会超时，需要进一步优化。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈在于枚举所有子数组**，导致 `O(n²)` 的时间。我们需要把“找子数组”这一步改成 **`O(1)` 或 `O(log n)`** 的查询。

关键观察：

1. **整体余数**  
   设 `total = sum(nums)`，记 `total % p = target`。如果 `target == 0`，说明整个数组已经满足条件，答案是 `0`（不需要删任何东西）。

2. **删除子数组的等价条件**  
   删除子数组 `nums[l..r]` 后，剩余和为 `total - sub_sum`。要求它能被 `p` 整除，即  

   \[
   (total - sub\_sum) \bmod p = 0
   \Longrightarrow sub\_sum \bmod p = total \bmod p = target
   \]

   所以我们只要在数组里找到 **余数恰好等于 `target` 的最短子数组**，长度就是答案（除去整条数组的情况）。

3. **前缀和 + 哈希表**  
   令 `pre[i] = (nums[0] + … + nums[i‑1]) % p` 为前缀和的余数。  
   子数组 `nums[l..r]` 的和的余数可以用前缀余数相减得到：

   \[
   sub\_sum \bmod p = (pre[r+1] - pre[l]) \bmod p
   \]

   为了让 `sub_sum % p = target`，我们需要  

   \[
   (pre[r+1] - pre[l]) \bmod p = target
   \Longrightarrow pre[l] = (pre[r+1] - target) \bmod p
   \]

   换句话说：**当我们遍历到位置 `r+1`（记作 `i`）时，只要在之前出现过满足上式的前缀余数，就能得到一个合法子数组**。

4. **为什么要保存“最右侧”下标**  
   设当前下标为 `i`，我们要找 `j < i` 使 `pre[j] = need`，子数组长度为 `i - j`。要让长度尽可能 **短**，`j` 越 **大** 越好（越靠近 `i`）。因此在哈希表里我们保存 **出现过的下标中最大的那个**（即最右侧），这样每次查询都能得到最短的候选长度。

5. **不能删除整条数组**  
   当候选长度等于 `n` 时，需要排除，因为题目不允许把全部元素都删掉。

#### 步骤概览

| 步骤 | 目的 |
|------|------|
| 计算 `total` 并取余得到 `target` | 判断是否已满足或确定需要删除的子数组余数 |
| 初始化哈希表 `mod_index = {0: -1}` | 前缀余数 `0` 出现在下标 `-1`（方便子数组从开头开始） |
| 从左到右遍历数组，实时维护 `cur_mod = (cur_mod + num) % p` | 得到每个位置的前缀余数 |
| 计算 `need = (cur_mod - target) % p` 并在哈希表中查找 | 找到满足条件的最右侧前缀下标 |
| 更新答案 `ans = min(ans, i - j)` | 记录最小子数组长度 |
| 将当前 `cur_mod` 以及对应下标 `i` 写入哈希表（覆盖旧值） | 保持“最右侧”下标的属性 |
| 最后检查 `ans < n`，否则返回 `-1` | 确保没有把全部元素删掉 |

#### 代码（Python）

```python
from typing import List

def min_subarray(nums: List[int], p: int) -> int:
    """
    返回需要删除的最短子数组长度，使得剩余元素和能被 p 整除。
    若不存在合法子数组，返回 -1。
    """
    total = sum(nums)
    target = total % p               # 需要删除的子数组的余数
    if target == 0:                  # 已经满足条件
        return 0

    n = len(nums)
    ans = n + 1                      # 初始为不可能的“大数”

    mod_index = {0: -1}              # 前缀余数 0 出现在下标 -1
    cur_mod = 0                      # 当前前缀和 % p

    for i, num in enumerate(nums):
        cur_mod = (cur_mod + num) % p               # 前缀余数 pre[i+1]
        # 需要的前缀余数，使得 (cur_mod - need) % p == target
        need = (cur_mod - target) % p

        # 若 need 已经出现过，说明找到了一个合法子数组
        if need in mod_index:
            length = i - mod_index[need]            # 子数组长度 = i - j
            if length < ans:                        # 只保留更短的
                ans = length

        # 更新哈希表，保存当前余数出现的最右侧下标（覆盖旧值）
        mod_index[cur_mod] = i

    # 不能把全部元素删掉
    return -1 if ans == n + 1 or ans == n else ans
```

> **关键点注释**  
> - `mod_index = {0: -1}`：把“空前缀”当作下标 `-1`，这样当子数组从索引 `0` 开始时，`i - (-1) = i+1` 正好是长度。  
> - `need = (cur_mod - target) % p`：Python 的 `%` 已经保证结果为非负，等价于数学中的模运算。  
> - `mod_index[cur_mod] = i`：覆盖旧值，使哈希表始终保存**最右**的出现位置，从而得到最短子数组。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，每一步的哈希表查询/写入是 `O(1)`（均摊），所以整体是线性级，`n` 增长 10 倍，耗时只增加约 10 倍，能够轻松通过 `10⁵` 的数据量。
- **空间复杂度**：`O(p)` 的最坏情况是哈希表里存了每个可能的余数（最多 `p` 种），但实际受限于 `n`（不可能出现超过 `n+1` 个不同余数），所以记作 `O(n)`。在本题中这只是一张大小约为 `10⁵` 的字典，内存消耗很小。

> 与暴力解相比，时间从 **平方级** 降到了 **线性级**，空间从 **常数/前缀数组** 升到了 **哈希表**，但整体仍然非常轻量。

---

## 心得

- **核心技巧**：利用**前缀和 + 哈希表**把“子数组求和”转化为**余数匹配**，从而在 `O(1)` 时间内判断是否存在满足条件的子数组。
- **适用的题型**  
  1. “最短子数组使得和满足某个模数条件”——如本题、LeetCode 1656 *Minimum Deletions to Make Array Divisible by K*。  
  2. “最长子数组满足和为 0（或等于某值）”——如 LeetCode 560 *Subarray Sum Equals K*（使用前缀和 + 哈希表）。  
  3. “数组中出现频率最高的子数组长度”——需要快速定位前后出现位置，同样可以用哈希表保存最左/最右下标。
- **一句话总结解题钥匙**：  
  “**把要删除的子数组的余数等式转化为前缀余数的匹配问题，利用哈希表在遍历时即时找最右匹配下标，即可得到最短合法长度**”。

---

## 反思

- **第一反应**：看到“删除子数组，使剩余和能被 `p` 整除”，本能想到**枚举子数组**，因为子数组是连续的，直接检查最直观。
- **最容易踩的坑**  
  1. **忘记取模负数**：在计算 `need = (cur_mod - target) % p` 时，如果直接写 `cur_mod - target` 可能得到负数，需要再 `% p` 保证非负。  
  2. **全删情况**：即使找到了长度等于 `n` 的子数组，也要返回 `-1`，因为题目禁止删除整个数组。  
  3. **初始化哈希表**：没有把 `0` 对应的下标设为 `-1`，会导致子数组从开头开始时找不到匹配，从而漏掉合法答案。  
- **下次类似题的第一步**：先**把全局约束（比如总和的余数）写成等式**，看“删除/添加”后对余数的影响，然后**用前缀和 + 哈希表**把等式转化为“前缀余数匹配”，再考虑如何在遍历中维护“最左/最右”下标，以得到最短或最长的子数组。