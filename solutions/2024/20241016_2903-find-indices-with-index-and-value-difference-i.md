# #2903. 找出满足索引和值差异的下标 I / Find Indices With Index and Value Difference I

> 难度：简单 · 标签：Array、Two Pointers · [LeetCode 链接](https://leetcode.com/problems/find-indices-with-index-and-value-difference-i/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums having length n, an integer indexDifference, and an integer valueDifference.
Your task is to find two indices i and j, both in the range [0, n - 1], that satisfy the following conditions:
Return an integer array answer, where answer = [i, j] if there are two such indices, and answer = [-1, -1] otherwise. If there are multiple choices for the two indices, return any of them.
Note: i and j may be equal.

**Examples**

**Example 1:**

```
Input: nums = [5,1,4,1], indexDifference = 2, valueDifference = 4
Output: [0,3]
Explanation: In this example, i = 0 and j = 3 can be selected.
abs(0 - 3) >= 2 and abs(nums[0] - nums[3]) >= 4.
Hence, a valid answer is [0,3].
[3,0] is also a valid answer.
```

**Example 2:**

```
Input: nums = [2,1], indexDifference = 0, valueDifference = 0
Output: [0,0]
Explanation: In this example, i = 0 and j = 0 can be selected.
abs(0 - 0) >= 0 and abs(nums[0] - nums[0]) >= 0.
Hence, a valid answer is [0,0].
Other valid answers are [0,1], [1,0], and [1,1].
```

**Example 3:**

```
Input: nums = [1,2,3], indexDifference = 2, valueDifference = 4
Output: [-1,-1]
Explanation: In this example, it can be shown that it is impossible to find two indices that satisfy both conditions.
Hence, [-1,-1] is returned.
```

**Constraints**

- 1 <= n == nums.length <= 100
- 0 <= nums[i] <= 50
- 0 <= indexDifference <= 100
- 0 <= valueDifference <= 50

---

## 题目（中文翻译）

给定一个 **0 索引**（0-indexed）整数数组 `nums`，其长度为 `n`，以及两个整数 `indexDifference` 和 `valueDifference`。  
你的任务是找到两个下标 `i` 和 `j`（均位于区间 `[0, n - 1]`），使得它们满足以下条件：

- `abs(i - j) >= indexDifference`  
- `abs(nums[i] - nums[j]) >= valueDifference`

返回一个整数数组 `answer`：

- 若存在满足条件的两下标，则 `answer = [i, j]`（任意一组符合要求的解均可）。  
- 若不存在，则返回 `answer = [-1, -1]`。

**注意**：`i` 与 `j` 可以相等。

---

### 示例

**示例 1**

> **输入**：`nums = [5,1,4,1]`, `indexDifference = 2`, `valueDifference = 4`  
> **输出**：`[0,3]`  
> **解释**：此例中可以选择 `i = 0`、`j = 3`。  
> `abs(0 - 3) >= 2` 且 `abs(nums[0] - nums[3]) >= 4`，因此 `[0,3]` 是合法答案。  
> `[3,0]` 也是合法答案。

**示例 2**

> **输入**：`nums = [2,1]`, `indexDifference = 0`, `valueDifference = 0`  
> **输出**：`[0,0]`  
> **解释**：此例中可以选择 `i = 0`、`j = 0`。  
> `abs(0 - 0) >= 0` 且 `abs(nums[0] - nums[0]) >= 0`，因此 `[0,0]` 是合法答案。  
> 其他合法答案还有 `[0,1]`、`[1,0]`、`[1,1]`。

**示例 3**

> **输入**：`nums = [1,2,3]`, `indexDifference = 2`, `valueDifference = 4`  
> **输出**：`[-1,-1]`  
> **解释**：可以证明不存在满足两个条件的下标组合，所以返回 `[-1,-1]`。

---

### 约束条件

- `1 <= n == nums.length <= 100`  
- `0 <= nums[i] <= 50`  
- `0 <= indexDifference <= 100`  
- `0 <= valueDifference <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的下标组合都枚举一遍，然后检查它们是否满足题目给出的两个条件：

1. `abs(i - j) >= indexDifference` —— 两个下标之间的距离要够大。  
2. `abs(nums[i] - nums[j]) >= valueDifference` —— 两个数值之间的差距也要够大。

这就像在找两个人：我们先把所有人两两配对（就像把所有可能的两本书配对），然后一个一个地检查这两个人是否够“远”（下标差）且“不同”（数值差）。  

- **使用的数据结构**：只需要原始的列表 `nums`，再加两个嵌套的 `for` 循环来遍历所有 `(i, j)`。  
- **为什么正确**：因为我们检查了**所有**可能的下标对，只要有一对满足条件，就一定会被找到；如果遍历完都没有找到，说明根本不存在这样的下标对。  

#### 代码（Python）

```python
from typing import List

def findIndices(nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
    n = len(nums)
    # 双层循环遍历所有 (i, j) 组合
    for i in range(n):
        for j in range(n):
            # 条件 1：下标距离
            if abs(i - j) < indexDifference:
                continue          # 距离不够，直接跳到下一个 j
            # 条件 2：数值差距
            if abs(nums[i] - nums[j]) < valueDifference:
                continue          # 差距不够，继续尝试下一个 j
            # 两个条件都满足，直接返回答案
            return [i, j]
    # 没有找到任何满足条件的下标对
    return [-1, -1]
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - 这里的 `n` 是数组长度。我们用两层循环把每个下标和其它下标配对，最坏情况下要检查 `n × n` 次。  
  - 用大白话说，就是如果数组有 10 个元素，就要检查 100 次；如果有 100 个元素，就要检查 10 000 次。  

- **空间复杂度**：`O(1)`。  
  - 只用了常数级别的额外变量（`i、j、n`），不随 `n` 增长而增长。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **两层循环**，它把每一对下标都检查了一遍。  
其实我们可以利用题目给出的 **数值范围很小**（`0 ≤ nums[i] ≤ 50`）来加速。

观察条件：

1. `abs(i - j) >= indexDifference`  
   - 只要我们知道某个数值 `v` 在数组中出现过的最早位置 `first[v]` 和最晚位置 `last[v]`，  
     那么对于当前下标 `i`，只要 `i - first[v] >= indexDifference` 或 `last[v] - i >= indexDifference`，  
     就能保证下标距离满足要求。

2. `abs(nums[i] - nums[j]) >= valueDifference`  
   - 对于当前数值 `nums[i] = cur`，我们只需要找 **与 cur 差距够大的数值**。  
   - 因为数值范围只有 0~50，遍历所有可能的 `v`（最多 51 个）即可判断是否存在满足差距的数。

基于上述想法，我们可以一次遍历数组（`O(n)`），在遍历过程中维护两个数组：

- `first[v]`：数值 `v` 第一次出现的下标（如果还没出现，用 `inf` 表示）。  
- `last[v]`：数值 `v` 最后一次出现的下标（如果还没出现，用 `-inf` 表示）。

遍历到下标 `i` 时：

1. 计算 `cur = nums[i]`。  
2. 枚举所有数值 `v`（0~50），如果 `abs(cur - v) >= valueDifference`，说明 `v` 与 `cur` 的差距够大。  
3. 检查 `first[v]` 和 `last[v]` 是否已经记录了满足 **下标距离** 的位置。  
   - 如果 `i - first[v] >= indexDifference`，则 `[first[v], i]` 是答案。  
   - 如果 `last[v] - i >= indexDifference`，则 `[i, last[v]]` 是答案。  

如果上述检查都没有成功，则把当前下标 `i` 用来更新 `first[cur]`（如果是第一次出现）和 `last[cur]`（每次都更新为最新位置），继续向后遍历。

因为数值的可能取值只有 51 种，枚举过程是常数级别的，整体时间复杂度是 `O(n * 51) ≈ O(n)`。

#### 代码（Python）

```python
from typing import List
import math

def findIndices(nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
    n = len(nums)
    MAX_VAL = 50                     # 题目给出的最大数值

    # 初始化 first[v] 为正无穷，last[v] 为负无穷
    first = [math.inf] * (MAX_VAL + 1)
    last  = [-math.inf] * (MAX_VAL + 1)

    for i, cur in enumerate(nums):
        # 1️⃣ 枚举所有可能的数值 v，检查数值差是否满足
        for v in range(MAX_VAL + 1):
            if abs(cur - v) < valueDifference:
                continue            # 差距不够，直接跳过

            # 2️⃣ 检查已经出现过的 v 是否能和当前 i 组成合法的下标差
            if first[v] != math.inf and i - first[v] >= indexDifference:
                return [first[v], i]    # 先出现的 v 在左侧
            if last[v] != -math.inf and last[v] - i >= indexDifference:
                return [i, last[v]]     # 先出现的 v 在右侧

        # 3️⃣ 更新 first[cur] 与 last[cur]（为后面的下标提供参考）
        if first[cur] == math.inf:      # 只在第一次出现时写入
            first[cur] = i
        last[cur] = i                    # 每次都写，保持最新位置

    # 遍历结束仍未找到，说明不存在满足条件的下标对
    return [-1, -1]
```

#### 复杂度  

- **时间复杂度**：`O(n * V)`，其中 `V = 51`（数值的可能取值个数），等价于 `O(n)`。  
  - 用大白话说：我们只需要遍历数组一次，每个元素最多检查 51 次（像在超市里挑 51 种商品），所以整体花的时间随数组长度线性增长。  

- **空间复杂度**：`O(V)`，即 `O(1)`（因为 `V` 是常数 51）。  
  - 只用了两个长度为 51 的数组来记录每个数值出现的最早和最晚位置，大小固定不随输入规模变化。  

---

## 心得  

- **核心技巧**：利用「数值范围小」这一特性，用**哈希表/数组**记录每个数值的出现位置，再结合**一次遍历**完成检查。  
- **适用的题型**  
  1. 需要同时满足「下标距离」和「数值差距」的配对问题（如本题）。  
  2. 「在数组中找满足某个数值区间的下标」类题目（例如 “Maximum Distance Between Two Same Elements”）。  
  3. 「数值范围有限」且要快速查询历史信息的问题（如 “Contains Duplicate III” 的变种）。  
- **一句话总结解题钥匙**：**把「数值」和「位置」分别用数组记录，遍历时只检查有限的可能数值，即可把 O(n²) 降到 O(n)。**  

---

## 反思  

- **第一反应**：看到两个 `abs` 条件，立刻想到「双层循环全部枚举」——最安全、最直接的办法。  
- **最容易踩的坑**  
  - **下标差的方向**：`abs(i - j) >= indexDifference`，要记得两边都可能满足（`i` 在左或右），因此在最优解中要分别检查 `first[v]` 与 `last[v]`。  
  - **数值差的边界**：当 `valueDifference = 0` 时，所有数值都满足差距条件，需要确保代码不会误把 `v == cur` 排除。  
  - **初始化**：`first` 用 `inf`、`last` 用 `-inf` 防止未出现的数值误参与比较。  
- **下次遇到同类题**：第一步先问自己「数值范围是否小」或「是否可以用哈希/数组记录出现信息」，如果答案是「是」，就立刻考虑 **一次遍历 + 预处理** 的思路，而不是直接套用暴力双循环。