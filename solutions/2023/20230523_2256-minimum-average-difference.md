# #2256. **最小平均差** / Minimum Average Difference

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-average-difference/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of length n.
The average difference of the index i is the absolute difference between the average of the first i + 1 elements of nums and the average of the last n - i - 1 elements. Both averages should be rounded down to the nearest integer.
Return the index with the minimum average difference. If there are multiple such indices, return the smallest one.
Note:

**Examples**

**Example 1:**

```
Input: nums = [2,5,3,9,5,3]
Output: 3
Explanation:
- The average difference of index 0 is: |2 / 1 - (5 + 3 + 9 + 5 + 3) / 5| = |2 / 1 - 25 / 5| = |2 - 5| = 3.
- The average difference of index 1 is: |(2 + 5) / 2 - (3 + 9 + 5 + 3) / 4| = |7 / 2 - 20 / 4| = |3 - 5| = 2.
- The average difference of index 2 is: |(2 + 5 + 3) / 3 - (9 + 5 + 3) / 3| = |10 / 3 - 17 / 3| = |3 - 5| = 2.
- The average difference of index 3 is: |(2 + 5 + 3 + 9) / 4 - (5 + 3) / 2| = |19 / 4 - 8 / 2| = |4 - 4| = 0.
- The average difference of index 4 is: |(2 + 5 + 3 + 9 + 5) / 5 - 3 / 1| = |24 / 5 - 3 / 1| = |4 - 3| = 1.
- The average difference of index 5 is: |(2 + 5 + 3 + 9 + 5 + 3) / 6 - 0| = |27 / 6 - 0| = |4 - 0| = 4.
The average difference of index 3 is the minimum average difference so return 3.
```

**Example 2:**

```
Input: nums = [0]
Output: 0
Explanation:
The only index is 0 so return 0.
The average difference of index 0 is: |0 / 1 - 0| = |0 - 0| = 0.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个下标从 0 开始、长度为 *n* 的整数数组 `nums`。  
下标 `i` 的 **平均差（average difference）** 定义为：

- 取前 `i + 1` 个元素的平均值（向下取整），记为 `leftAvg`；
- 取后 `n - i - 1` 个元素的平均值（向下取整），记为 `rightAvg`（若后面没有元素，则 `rightAvg` 为 0）；

`i` 处的平均差为 `| leftAvg - rightAvg |`，即两者的绝对差。

返回平均差最小的下标。如果有多个下标的平均差相同，返回最小的下标。

---

### 示例

**示例 1**

> **输入**: `nums = [2,5,3,9,5,3]`  
> **输出**: `3`  
> **解释**:  
> - 下标 0 的平均差为 `| 2 / 1 - (5+3+9+5+3) / 5 | = | 2 - 5 | = 3`。  
> - 下标 1 的平均差为 `| (2+5) / 2 - (3+9+5+3) / 4 | = | 3 - 5 | = 2`。  
> - 下标 2 的平均差为 `| (2+5+3) / 3 - (9+5+3) / 3 | = | 3 - 5 | = 2`。  
> - 下标 3 的平均差为 `| (2+5+3+9) / 4 - (5+3) / 2 | = | 4 - 4 | = 0`。  
> - 下标 4 的平均差为 `| (2+5+3+9+5) / 5 - 3 / 1 | = | 4 - 3 | = 1`。  
> - 下标 5 的平均差为 `| (2+5+3+9+5+3) / 6 - 0 | = | 4 - 0 | = 4`。  
> 最小的平均差为 0，出现在下标 3，故返回 3。

**示例 2**

> **输入**: `nums = [0]`  
> **输出**: `0`  
> **解释**: 唯一的下标是 0，返回 0。  
> 下标 0 的平均差为 `| 0 / 1 - 0 | = | 0 - 0 | = 0`。

---

### 约束

- `1 <= nums.length <= 10^5`  
- `0 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个下标**计算它的“平均差”。  
对每个下标 `i`：

1. 取前 `i+1` 个数求和 → 记作 `sum_left`，再除以 `i+1`（向下取整）得到左侧平均值 `avg_left`。  
2. 取后面 `n-i-1` 个数求和 → 记作 `sum_right`，再除以 `n-i-1`（向下取整）得到右侧平均值 `avg_right`。  
3. 计算两者的绝对差 `|avg_left - avg_right|`，记录最小的差对应的下标。

这里用到的**求和**可以类比成在超市里把商品一个一个放进购物车并累计价格——没有任何“技巧”，只能一步一步加。

**为什么正确**：  
因为题目要求的正是对每个下标分别计算上述两段平均值的差，暴力遍历不漏掉任何下标，自然能得到答案。

**复杂度分析（大白话）**：

- 对每个下标我们都要遍历一次数组去求左边和右边的和。  
  - 如果数组长度是 `n`，我们会做 `n` 次 “遍历整条数组” 的工作，等价于 `n × n` 次基本操作。  
  - 在算法分析里，这种 **二次方** 的增长记作 `O(n²)`，意思是当 `n` 增大到 10 倍时，耗时会增加到大约 100 倍。  
- 只用了几个整数变量来保存当前的和、平均值等，额外空间几乎不变，记作 `O(1)`。

#### 代码（Python）

```python
from typing import List

def minimumAverageDifference_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best_idx = -1          # 记录当前最小差对应的下标
    best_diff = float('inf')   # 记录当前最小差的数值

    for i in range(n):
        # 1️⃣ 计算左侧和左侧平均（向下取整）
        left_sum = sum(nums[:i + 1])          # 把前 i+1 个数全部加起来
        left_avg = left_sum // (i + 1)        # // 是向下取整除法

        # 2️⃣ 计算右侧和右侧平均（如果右侧为空，平均视为 0）
        if i == n - 1:                        # 最后一个元素右侧没有数
            right_avg = 0
        else:
            right_sum = sum(nums[i + 1:])      # 把后面的数全部加起来
            right_avg = right_sum // (n - i - 1)

        # 3️⃣ 计算绝对差
        diff = abs(left_avg - right_avg)

        # 4️⃣ 更新答案（如果相同差距取更小的下标）
        if diff < best_diff:
            best_diff = diff
            best_idx = i

    return best_idx
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每个下标都要遍历一次数组求和，等价于 `n` 次 `O(n)` 的求和操作。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个临时变量（`left_sum、right_sum…`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复的求和**是性能瓶颈。  
例如在下标 `i` 与 `i+1` 之间，左侧的和只多加了一个元素 `nums[i+1]`，右侧的和则少了同一个元素。  
如果我们把所有前缀的累计和事先算好，就可以 **在 O(1) 时间** 内得到任意区间的和，这正是**前缀和（Prefix Sum）**的用法。

**前缀和的类比**：  
想象把一本厚厚的字典每页的页码累加起来，记下每一页的累计页码数（前缀和）。  
以后要知道第 3~7 页的总页码，只需要 `prefix[7] - prefix[2]`，不必重新把 3~7 页一个字一个字数。

**具体步骤**：

1. **一次遍历**算出所有前缀和 `pref[i] = nums[0] + ... + nums[i]`（`i` 为 0‑based）。  
   - 这样 `pref[i]` 就是下标 `i` 左侧（包括 `i`）的总和。  
2. **总和** `total = pref[n-1]` 同时保存，后面可以直接用 `total - pref[i]` 得到右侧的和。  
3. 再遍历一次数组，对每个下标 `i`：
   - 左侧平均 `left_avg = pref[i] // (i+1)`（向下取整）。  
   - 右侧元素个数 `right_cnt = n - i - 1`。  
   - 若 `right_cnt == 0`（即 `i` 为最后一个位置），右侧平均设为 `0`；否则右侧平均 `right_avg = (total - pref[i]) // right_cnt`。  
   - 计算差值 `diff = abs(left_avg - right_avg)`，实时维护最小差及对应下标。  
4. 最终返回记录的下标。

**为什么是最优**：  
- 前缀和只需要 **一次** `O(n)` 的遍历来准备，随后每个下标的左右和都能在 **常数时间** (`O(1)`) 直接算出。  
- 整体只遍历两遍数组，时间是线性的 `O(n)`，远快于 `O(n²)`。  
- 只用了一个长度为 `n` 的前缀和数组，额外空间 `O(n)`（如果想进一步节省空间，也可以在遍历时直接累加左侧和而不保存完整的前缀数组，空间降为 `O(1)`，这里先保持直观的实现）。

#### 代码（Python）

```python
from typing import List

def minimumAverageDifference(nums: List[int]) -> int:
    n = len(nums)
    # 1️⃣ 计算前缀和数组
    prefix = [0] * n
    cur = 0
    for i, v in enumerate(nums):
        cur += v               # 累计到当前位置
        prefix[i] = cur        # 把累计和保存下来

    total = prefix[-1]          # 整个数组的和

    best_idx = 0                # 默认答案是下标 0
    best_diff = float('inf')    # 初始差距设为无限大

    # 2️⃣ 再遍历一次，计算每个下标的平均差
    for i in range(n):
        left_sum = prefix[i]                # 左侧（包括 i）总和
        left_cnt = i + 1
        left_avg = left_sum // left_cnt     # 向下取整

        right_cnt = n - i - 1                # 右侧元素个数
        if right_cnt == 0:                   # 右侧为空时平均视为 0
            right_avg = 0
        else:
            right_sum = total - left_sum     # 总和减去左侧即为右侧和
            right_avg = right_sum // right_cnt

        diff = abs(left_avg - right_avg)     # 绝对差

        # 若出现更小的差，或差相同但下标更小，则更新答案
        if diff < best_diff:
            best_diff = diff
            best_idx = i

    return best_idx
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历两遍数组，每次都是线性时间。  
  - 与暴力解 `O(n²)` 相比，规模扩大 10 倍只会花费约 10 倍时间，而不是 100 倍，快得多。  
- **空间复杂度**：`O(n)` — 需要存放前缀和数组 `prefix`（长度 `n`）。  
  - 如果把左侧累计和直接存进变量而不保留全部前缀，则可以把空间降到 `O(1)`（常数级），但这里的实现更易于理解。

---

## 心得

- **核心技巧**：前缀和（Prefix Sum）——把“区间求和”从线性降到常数。  
- **适用的题型**  
  1. “区间和”类问题，如 **子数组和等于 K**、**区间求平均**。  
  2. “前缀最值”类，如 **最大子序和**（Kadane）需要前缀最小值。  
  3. “区间乘积/区间最大最小值” 也可以通过前缀积或单调栈等类似思路实现。  
- **一句话总结**：**把所有“重复求和”提前算好，用 O(1) 的查询代替 O(n) 的遍历**，就是这道题的解题钥匙。

---

## 反思

- **第一反应**：看到“左侧平均”和“右侧平均”就想到“遍历每个位置分别求和”，也就是暴力解。  
- **最容易踩的坑**  
  1. **右侧为空**时除以零，需要单独处理（平均值设为 0）。  
  2. **向下取整**：在 Python 中使用 `//` 而不是 `/`，否则会得到浮点数。  
  3. **大数相减**时仍在整数范围（题目给的数值上限 10⁵，长度 10⁵，和最多 10¹⁰，Python 整数足够安全）。  
- **下次类似题的第一步**：先判断是否可以**预处理**（前缀和、前缀乘积、前缀最大/最小等），如果可以，就把 O(n) 的“重复工作”压缩到 O(1) 查询。这样往往能直接把暴力 `O(n²)` 降到线性 `O(n)`。