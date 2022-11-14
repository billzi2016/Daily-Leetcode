# #2012. 数组的美丽和 / Sum of Beauty in the Array

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/sum-of-beauty-in-the-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. For each index i (1 <= i <= nums.length - 2) the beauty of nums[i] equals:
Return the sum of beauty of all nums[i] where 1 <= i <= nums.length - 2.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3]
Output: 2
Explanation: For each index i in the range 1 <= i <= 1:
- The beauty of nums[1] equals 2.
```

**Example 2:**

```
Input: nums = [2,4,6,4]
Output: 1
Explanation: For each index i in the range 1 <= i <= 2:
- The beauty of nums[1] equals 1.
- The beauty of nums[2] equals 0.
```

**Example 3:**

```
Input: nums = [3,2,1]
Output: 0
Explanation: For each index i in the range 1 <= i <= 1:
- The beauty of nums[1] equals 0.
```

**Constraints**

- 3 <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`。对于每个索引 `i`（`1 <= i <= nums.length - 2`）`nums[i]` 的美丽等于：

返回所有满足 `1 <= i <= nums.length - 2` 的 `nums[i]` 的美丽之和。

**示例 1**  
输入：`nums = [1,2,3]`  
输出：`2`  
**解释**：对于范围 `1 <= i <= 1` 中的每个索引 `i`：  
- `nums[1]` 的美丽等于 `2`。

**示例 2**  
输入：`nums = [2,4,6,4]`  
输出：`1`  
**解释**：对于范围 `1 <= i <= 2` 中的每个索引 `i`：  
- `nums[1]` 的美丽等于 `1`。  
- `nums[2]` 的美丽等于 `0`。

**示例 3**  
输入：`nums = [3,2,1]`  
输出：`0`  
**解释**：对于范围 `1 <= i <= 1` 中的每个索引 `i`：  
- `nums[1]` 的美丽等于 `0`。

**约束条件**  

- `3 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求我们对数组 `nums` 的每个 **内部** 元素（下标 `i` 满足 `1 ≤ i ≤ n‑2`）计算它的 *beauty*，然后把所有 beauty 加起来。

> **beauty 的定义**（题目省略的那段）  
> 对于下标 `i`，  
> - 如果左侧（下标 `< i`）存在一个 **更小** 的数，则记一次贡献 `1`；  
> - 如果右侧（下标 `> i`）存在一个 **更大** 的数，则再记一次贡献 `1`。  
> 最终 `beauty[i]` 就是这两次贡献的和，可能是 `0、1、2`。

可以把这个过程想象成“检查左边有没有比我小的，同学们常说的‘左边有人比我矮’”，以及“检查右边有没有比我高的”。  
如果左边有，右边也有，就得到 `2`；只满足其中一边则得到 `1`；两边都不满足则是 `0`。

**最直接的做法**：对每个 `i`，遍历左侧找最小值、遍历右侧找最大值，判断是否满足条件。

- **数据结构**：只需要普通的 `for` 循环和变量保存当前最小/最大值。  
- **为什么正确**：我们把左侧所有元素都看了一遍，必然能发现是否存在比 `nums[i]` 更小的数；右侧同理。

#### 代码（Python）

```python
from typing import List

def sum_of_beauty(nums: List[int]) -> int:
    n = len(nums)
    total = 0                     # 累计所有 beauty
    # i 只能取内部位置，省去两端的元素
    for i in range(1, n - 1):
        left_smaller = False      # 左侧是否出现更小的数
        right_larger = False      # 右侧是否出现更大的数

        # 检查左侧：遍历 0 ~ i-1
        for j in range(i):
            if nums[j] < nums[i]:
                left_smaller = True
                break            # 找到一个就够了，直接退出

        # 检查右侧：遍历 i+1 ~ n-1
        for j in range(i + 1, n):
            if nums[j] > nums[i]:
                right_larger = True
                break            # 同上

        # beauty = 左侧满足 + 右侧满足（布尔值 True 当作 1）
        total += left_smaller + right_larger
    return total
```

> **代码要点注释**  
> - `left_smaller`、`right_larger` 用布尔值记录是否满足对应条件，`True` 在算数运算时会自动转成 `1`。  
> - `break` 能让我们在找到第一个满足条件的元素后立即停止循环，稍微省点时间。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n‑2` 次，内层最坏情况下要遍历 `i` 次左侧 + `n‑i‑1` 次右侧，整体是二次方级别。  
  - 用大白话说，就是如果数组有 10,000 个元素，程序大概要跑 10,000 × 10,000 = 1 亿次比较，明显太慢。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`total`、`left_smaller`、`right_larger`），和数组长度无关。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次都要重新遍历左侧和右侧，导致大量的重复工作。  
实际上，我们只需要知道：

1. **左侧的最大值**（记作 `prefix_max[i]`）——只要 `prefix_max[i] < nums[i]`，就一定存在左边更小的数。  
2. **右侧的最小值**（记作 `suffix_min[i]`）——只要 `nums[i] < suffix_min[i]`，就一定存在右边更大的数。

这两个信息可以 **预处理** 一遍得到，之后每个位置的判断只需要 O(1) 时间。

> **前缀数组（prefix）**  
> `prefix_max[i]` 保存区间 `[0, i‑1]`（左边全部）的最大值。  
> 计算方式：从左到右遍历，`prefix_max[i] = max(prefix_max[i‑1], nums[i‑1])`。  
> 类比：把左边所有数装进一本“最大值字典”，随时可以查到左边最大的那本。

> **后缀数组（suffix）**  
> `suffix_min[i]` 保存区间 `[i+1, n‑1]`（右边全部）的最小值。  
> 计算方式：从右到左遍历，`suffix_min[i] = min(suffix_min[i+1], nums[i+1])`。  
> 类比：把右边所有数装进一本“最小值字典”，随时可以查到右边最小的那本。

有了这两个数组，`beauty[i]` 的计算公式非常直接：

```text
beauty[i] = (prefix_max[i] < nums[i]) + (nums[i] < suffix_min[i])
```

这正是我们在暴力解中要判断的两件事，只是现在查询是 **O(1)**。

#### 代码（Python）

```python
from typing import List

def sum_of_beauty(nums: List[int]) -> int:
    n = len(nums)
    # 1. 构建前缀最大值数组
    prefix_max = [0] * n          # prefix_max[i] 只在 i >= 1 时有意义
    cur_max = nums[0]             # 到当前位置左边的最大值
    for i in range(1, n):
        prefix_max[i] = cur_max
        cur_max = max(cur_max, nums[i])

    # 2. 构建后缀最小值数组
    suffix_min = [0] * n          # suffix_min[i] 只在 i <= n-2 时有意义
    cur_min = nums[-1]            # 到当前位置右边的最小值
    for i in range(n - 2, -1, -1):
        suffix_min[i] = cur_min
        cur_min = min(cur_min, nums[i])

    # 3. 逐个位置计算 beauty 并累计
    total = 0
    for i in range(1, n - 1):     # 只看内部元素
        left_ok  = prefix_max[i] < nums[i]   # 左侧是否有更小的数
        right_ok = nums[i] < suffix_min[i]   # 右侧是否有更大的数
        total += left_ok + right_ok          # 布尔值 True 会被当作 1 加进来
    return total
```

> **代码要点注释**  
> - `prefix_max[i]` 保存的是 **左边**（不包括自己）的最大值；同理 `suffix_min[i]` 保存的是 **右边**（不包括自己）的最小值。  
> - 预处理过程只遍历两遍数组，时间是线性的。  
> - 最终遍历一次即可得到答案，每次判断只用两次比较。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 前缀、后缀各遍历一次，最后再遍历一次计算 beauty，都是线性操作。  
  - 用大白话说：如果数组有 100,000 个元素，程序只会做大约 300,000 次比较，轻松跑完。

- **空间复杂度**：`O(n)`  
  - 需要额外的两个同长度数组 `prefix_max`、`suffix_min`，每个元素占用常数空间。  
  - 如果想进一步压缩空间，可以在遍历时直接使用两个变量（左侧最大值和右侧最小值）交替更新，空间降到 `O(1)`，但实现会稍微复杂一些，这里保持易懂的 `O(n)` 方案。

---

## 心得

- **核心技巧**：**前缀最大 / 后缀最小** 预处理。  
  把“左边有没有更小的数”转化为“左边的最大值是否小于当前”，把“右边有没有更大的数”转化为“右边的最小值是否大于当前”。  
- **适用场景**：  
  1. **左侧/右侧关系** 判断（如 “左边是否全部小于当前”， “右边是否全部大于当前”）。  
  2. **区间极值** 查询的经典技巧（例如 “子数组最大最小值” 相关题目）。  
- **解题钥匙**：**一次遍历把区间信息收集好，后面每个位置只做 O(1) 判断**。

---

## 反思

- **第一反应**：直接对每个元素分别遍历左、右，写出暴力解，以确保对题意完全理解。  
- **最容易踩的坑**：  
  - **边界**：只对下标 `1 … n‑2` 计算 beauty，首尾元素不参与。  
  - **比较方向**：左侧要比较 **最大值** 与当前，右侧要比较 **最小值** 与当前，容易写成相反导致答案全为 `0`。  
  - **数据范围**：`n` 可达 `10⁵`，必须避免 `O(n²)` 的做法。  
- **下次类似题目**：第一步先想 “我需要左/右区间的极值吗？” 若是，则立刻考虑 **前缀/后缀数组**（或单调栈）来一次性预处理。这样就能把看似二次的遍历压到线性时间。