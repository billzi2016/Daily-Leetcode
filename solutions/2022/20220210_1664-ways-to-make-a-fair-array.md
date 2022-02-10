# #1664. 使数组公平的方式 / Ways to Make a Fair Array

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/ways-to-make-a-fair-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums. You can choose exactly one index (0-indexed) and remove the element. Notice that the index of the elements may change after the removal.
For example, if nums = [6,1,7,4,1]:
An array is fair if the sum of the odd-indexed values equals the sum of the even-indexed values.
Return the number of indices that you could choose such that after the removal, nums is fair.

**Examples**

**Example 1:**

```
Input: nums = [2,1,6,4]
Output: 1
Explanation:
Remove index 0: [1,6,4] -> Even sum: 1 + 4 = 5. Odd sum: 6. Not fair.
Remove index 1: [2,6,4] -> Even sum: 2 + 4 = 6. Odd sum: 6. Fair.
Remove index 2: [2,1,4] -> Even sum: 2 + 4 = 6. Odd sum: 1. Not fair.
Remove index 3: [2,1,6] -> Even sum: 2 + 6 = 8. Odd sum: 1. Not fair.
There is 1 index that you can remove to make nums fair.
```

**Example 2:**

```
Input: nums = [1,1,1]
Output: 3
Explanation: You can remove any index and the remaining array is fair.
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 0
Explanation: You cannot make a fair array after removing any index.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`。你可以恰好选择一个下标（0 基）并删除该位置的元素。删除后，数组中元素的下标会相应改变。  
例如，若 `nums = [6,1,7,4,1]`：

一个数组被称为 **公平**（fair），当且仅当奇数下标的元素之和等于偶数下标的元素之和。  
返回可以选择的下标数量，使得删除该下标对应的元素后，`nums` 成为公平数组。

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^4`

---

### 示例

**示例 1**  
**输入**: `nums = [2,1,6,4]`  
**输出**: `1`  
**解释**:  
- 删除下标 `0` → `[1,6,4]` → 偶数下标和: `1 + 4 = 5`，奇数下标和: `6` → 不公平。  
- 删除下标 `1` → `[2,6,4]` → 偶数下标和: `2 + 4 = 6`，奇数下标和: `6` → 公平。  
- 删除下标 `2` → `[2,1,4]` → 偶数下标和: `2 + 4 = 6`，奇数下标和: `1` → 不公平。  
- 删除下标 `3` → `[2,1,6]` → 偶数下标和: `2 + 6 = 8`，奇数下标和: `1` → 不公平。  
只有 1 个下标可以删除使数组公平。

**示例 2**  
**输入**: `nums = [1,1,1]`  
**输出**: `3`  
**解释**: 任意删除一个下标，剩余数组均为公平数组。

**示例 3**  
**输入**: `nums = [1,2,3]`  
**输出**: `0`  
**解释**: 删除任意下标后都无法得到公平数组。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**逐个尝试**把每个下标 `i` 的元素删掉，然后重新遍历剩下的数组，分别把奇数下标（1、3、5…）和偶数下标（0、2、4…）上的数相加，判断两者是否相等。  

- **使用的数据结构**：普通的 Python 列表 `list`。遍历列表时我们会用到下标 `idx`，把它除以 2 的余数 (`idx % 2`) 看是奇是偶。可以把下标的奇偶想象成**两条不同颜色的跑道**，每跑一步我们就把当前数字放到对应颜色的跑道上累加。  
- **为什么正确**：因为我们把所有可能的删除位置都穷举了，凡是能得到“奇数下标之和 == 偶数下标之和”的情况必然会在遍历过程中被发现。  

**时间/空间复杂度**  
- 对每个 `i`（一共 `n` 个）我们都要重新遍历一次剩下的 `n‑1` 个元素来求和，时间复杂度是 `O(n * n) = O(n²)`。这里的 `O(n²)` 可以理解为“如果数组长度是 10，最多要算 100 次”。  
- 只用了常数级别的额外空间（几个计数变量），所以空间复杂度是 `O(1)`。

#### 代码（Python）

```python
from typing import List

def waysToMakeFair_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    ans = 0                     # 记录满足条件的下标个数

    for i in range(n):          # 逐个尝试删除下标 i
        even_sum, odd_sum = 0, 0
        idx = 0                 # 删除元素后，新数组的下标从 0 开始

        for j in range(n):      # 遍历原数组
            if j == i:           # 跳过被删除的元素
                continue
            if idx % 2 == 0:    # 新下标是偶数
                even_sum += nums[j]
            else:               # 新下标是奇数
                odd_sum += nums[j]
            idx += 1

        if even_sum == odd_sum: # 判断是否公平
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` — 需要两层循环，外层 `n` 次，内层最多 `n` 次。  
- **空间复杂度**：`O(1)` — 只用到常数个整数变量。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次删除后都要重新遍历一次**，这导致 `n²` 的时间。  
观察可以发现：如果我们已经知道原数组在每个位置之前（前缀）奇、偶下标的累计和，那么删除某个元素后，**只要把前缀和与后缀和（删除元素右侧）的贡献重新拼接**，就能在 `O(1)` 时间内算出新的奇、偶下标和。  

关键点如下：

1. **前缀和**  
   - `pre_even[i]`：下标 `0 … i-1`（不包括 `i`）中，**偶数下标**的元素之和。  
   - `pre_odd[i]`：下标 `0 … i-1` 中，**奇数下标**的元素之和。  
   这相当于我们在数组左侧已经跑完的两条跑道的累计距离。

2. **后缀和的转换**  
   删除下标 `i` 后，原来在 `i` 右侧的元素会向左平移一位，下标的奇偶性会**翻转**。  
   - 原来在右侧的偶数下标元素（相对于原数组）会变成奇数下标。  
   - 原来在右侧的奇数下标元素会变成偶数下标。  

   因此，删除 `i` 后的 **偶数下标和** 等于：  
   `pre_even[i]`（左侧保持偶数下标） + `suffix_odd[i+1]`（右侧原奇数下标变偶数）  

   同理，**奇数下标和** 等于：  
   `pre_odd[i]` + `suffix_even[i+1]`  

   为了快速得到 `suffix_even / suffix_odd`，我们可以直接用 **总和** 减去对应的前缀和得到。

3. **一步遍历完成**  
   - 先算出所有前缀和（一次遍历）。  
   - 再遍历一次数组，对每个 `i` 用公式直接计算删除后奇、偶下标的和，判断是否相等。  

这就把两层循环降到了 **两次线性遍历**，时间复杂度 `O(n)`，空间只需要保存前缀数组 `O(n)`（也可以在遍历时用滚动变量降到 `O(1)`，这里为了思路清晰保留前缀数组）。

#### 代码（Python）

```python
from typing import List

def waysToMakeFair(nums: List[int]) -> int:
    n = len(nums)
    # 前缀累计和
    pre_even = [0] * (n + 1)   # pre_even[i] = nums[0..i-1] 中偶数下标的和
    pre_odd  = [0] * (n + 1)   # pre_odd[i]  = nums[0..i-1] 中奇数下标的和

    for i in range(n):
        # 把当前位置的值累加到对应的前缀数组里
        pre_even[i + 1] = pre_even[i] + (nums[i] if i % 2 == 0 else 0)
        pre_odd[i + 1]  = pre_odd[i]  + (nums[i] if i % 2 == 1 else 0)

    total_even = pre_even[n]   # 整个数组偶数下标的和
    total_odd  = pre_odd[n]    # 整个数组奇数下标的和

    ans = 0
    for i in range(n):
        # 删除 i 之前的偶/奇和
        left_even = pre_even[i]          # 0..i-1 中偶数下标和
        left_odd  = pre_odd[i]           # 0..i-1 中奇数下标和

        # 删除 i 之后的偶/奇和（相对于原数组）
        right_even = total_even - pre_even[i + 1]   # i+1..end 中偶数下标和
        right_odd  = total_odd  - pre_odd[i + 1]    # i+1..end 中奇数下标和

        # 删除 i 后，右侧的下标会整体左移 1 位，奇偶翻转
        # 新的偶数下标和 = 左侧偶数和 + 右侧原奇数和
        new_even = left_even + right_odd
        # 新的奇数下标和 = 左侧奇数和 + 右侧原偶数和
        new_odd  = left_odd  + right_even

        if new_even == new_odd:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历了两次数组（一次构造前缀和，一次判断），即使 `n` 达到 `10⁵` 也能轻松跑完。与暴力解相比，省去了 `n` 倍的重复计算。  
- **空间复杂度**：`O(n)` — 存了两个长度为 `n+1` 的前缀数组。若进一步优化，只用常数个变量（滚动前缀），可以降到 `O(1)`，但 `O(n)` 已经足够且代码更易读。

---

## 心得  

- **核心技巧**：**前缀和 + 奇偶翻转**。通过把左侧已知的累计和与右侧翻转后的累计和快速拼接，避免了重复遍历。  
- **适用的题型**  
  1. “删除一个元素后满足某种前缀/后缀条件”的题目（如 LeetCode 1663 `Smallest String With Swaps` 的变种）。  
  2. “下标奇偶性会因删除或插入而改变”的数组平衡类问题（如 “删除一个元素后数组相等分割点”）。  
- **一句话总结**：**把“左边的东西保持不变，右边的东西翻个身”**，用前缀和一次算完。

---

## 反思  

- **第一反应**：直接写双层循环暴力枚举，想先把正确性保证好再去优化。  
- **最容易踩的坑**  
  - **下标翻转**：删除元素后右侧所有下标都会向左移动 1 位，奇偶性会互换，容易忘记这一步导致计算错误。  
  - **前缀数组的大小**：要多开一个位置（`n+1`），方便把 “不包含当前位置” 的前缀和直接写进数组。  
  - **边界情况**：当删除的是第一个或最后一个元素时，左侧或右侧可能为空，确保对应的前缀或后缀和为 0。  
- **下次遇到同类题**：第一步先**写出前缀（或后缀）累计**，再思考**删除/插入后下标的变化**，把问题转化为 **O(1)** 的查询。这样就能从“一遍遍遍历”直接跳到“一遍遍遍历”。