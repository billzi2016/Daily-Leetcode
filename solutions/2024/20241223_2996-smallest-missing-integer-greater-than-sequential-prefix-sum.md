# #2996. 大于顺序前缀和的最小缺失整数 / Smallest Missing Integer Greater Than Sequential Prefix Sum

> 难度：简单 · 标签：Array、Hash Table、Sorting · [LeetCode 链接](https://leetcode.com/problems/smallest-missing-integer-greater-than-sequential-prefix-sum/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of integers nums.
A prefix nums[0..i] is sequential if, for all 1 <= j <= i, nums[j] = nums[j - 1] + 1. In particular, the prefix consisting only of nums[0] is sequential.
Return the smallest integer x missing from nums such that x is greater than or equal to the sum of the longest sequential prefix.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,2,5]
Output: 6
Explanation: The longest sequential prefix of nums is [1,2,3] with a sum of 6. 6 is not in the array, therefore 6 is the smallest missing integer greater than or equal to the sum of the longest sequential prefix.
```

**Example 2:**

```
Input: nums = [3,4,5,1,12,14,13]
Output: 15
Explanation: The longest sequential prefix of nums is [3,4,5] with a sum of 12. 12, 13, and 14 belong to the array while 15 does not. Therefore 15 is the smallest missing integer greater than or equal to the sum of the longest sequential prefix.
```

**Constraints**

- 1 <= nums.length <= 50
- 1 <= nums[i] <= 50

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。  
如果对所有 `1 <= j <= i` 均满足 `nums[j] = nums[j - 1] + 1`，则前缀 `nums[0..i]` 为 **顺序前缀（sequential prefix）**。特别地，仅包含 `nums[0]` 的前缀也视为顺序前缀。  

返回满足以下条件的最小整数 `x`：`x` 不在 `nums` 中，且 `x` 大于等于 **最长顺序前缀（the longest sequential prefix）** 的元素和。

---

### 示例

**示例 1**  
```text
Input: nums = [1,2,3,2,5]
Output: 6
Explanation: nums 的最长顺序前缀是 [1,2,3]，其和为 6。6 不在数组中，因此 6 是满足条件的最小缺失整数。
```

**示例 2**  
```text
Input: nums = [3,4,5,1,12,14,13]
Output: 15
Explanation: nums 的最长顺序前缀是 [3,4,5]，其和为 12。12、13、14 都在数组中，而 15 不在数组中，所以 15 是满足条件的最小缺失整数。
```

---

### 约束条件

- `1 <= nums.length <= 50`
- `1 <= nums[i] <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的做法可以分成两步：

1. **找到最长的顺序前缀**  
   从左到右遍历数组 `nums`，只要后面的元素恰好比前一个大 `1`，前缀就还能继续延伸。  
   - 类比：想象一串楼梯，每一级只能比前一级高 `1`，只要踩得上去，前缀就还能往前走。  
   - 当出现 `nums[i] != nums[i‑1] + 1` 时，说明这段“楼梯”断了，前缀在 `i‑1` 处结束。

2. **在数组里找第一个 ≥ 前缀和且不存在的整数**  
   先把整个数组放进一个哈希表（在 Python 里就是 `set`），相当于查字典：  
   - **键（key）** 是数组中的每个数，**值（value）** 不用关心，只要能判断“这个数在不在”。  
   然后从前缀和 `S` 开始，一直往上尝试 `S, S+1, S+2 …`，第一次在哈希表里查不到的数字就是答案。

这个办法一定能得到正确答案，因为：
- 前缀和 `S` 已经是“最长顺序前缀的所有元素之和”，题目要求的 `x` 必须 **不小于** `S`；
- 我们从 `S` 起逐个检查是否出现过，只要找到了第一个缺失的，就是 **最小** 的满足条件的整数。

**时间复杂度**  
- 找前缀：最多遍历一次数组，`O(n)`。  
- 建哈希表：同样是一次遍历，`O(n)`。  
- 从 `S` 向上查找缺失数：最坏情况下可能要检查 `O(M)` 次，其中 `M` 是答案与 `S` 的差距。因为 `nums[i] ≤ 50, n ≤ 50`，`S` 最大约为 `50·51/2 = 1275`，所以实际检查次数也非常小。整体仍可视为 `O(n + M)`，在本题约为 `O(n)`。

**空间复杂度**  
- 哈希表存放所有数组元素，需要 `O(n)` 的额外空间。

#### 代码（Python）

```python
from typing import List

def smallest_missing(nums: List[int]) -> int:
    # 1️⃣ 找最长的顺序前缀并求和
    prefix_sum = nums[0]          # 前缀至少包含第一个元素
    longest_len = 1               # 前缀长度
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:   # 仍然是顺序的
            prefix_sum += nums[i]
            longest_len += 1
        else:                           # 前缀在 i-1 处结束
            break

    # 2️⃣ 把所有元素放进集合，便于 O(1) 判断是否出现
    present = set(nums)   # 相当于一本“查字典”，key 是数，value 不用管

    # 3️⃣ 从 prefix_sum 开始往上找第一个缺失的整数
    x = prefix_sum
    while True:
        if x not in present:   # 没在字典里，说明缺失
            return x
        x += 1                 # 继续检查下一个数
```

#### 复杂度

- **时间复杂度**：`O(n + M)`，这里的 `n` 是数组长度，`M` 是从前缀和到答案的距离。由于题目规模很小，实际运行几乎是线性 `O(n)`。
- **空间复杂度**：`O(n)`，用于存放哈希表（集合）里的所有数组元素。

---

### 2. 最优解

#### 思路  
在上述暴力方案里，唯一的“冗余”是我们把整个数组全部放进哈希表。其实我们只需要判断 **从 S 开始的连续整数** 是否在数组中，而这些整数的范围并不大（最多到 `S + n`），所以仍然可以使用哈希表，但可以在一次遍历中完成所有工作：

1. **一次遍历同时完成两件事**  
   - 计算最长顺序前缀的和 `S`（同前面的做法）。  
   - 把数组元素放进集合 `present`（这一步仍然是 `O(1)` 插入）。

2. **直接从 S 开始检查**  
   - 因为集合的查询是 `O(1)`，我们不需要额外的循环去找缺失数的上界，只要一直往上递增检查，必然在有限次（不超过 `n+1`）后找到答案。  
   - 解释：如果从 `S` 开始的 `n+1` 个整数全部都在数组里，那么数组里至少有 `n+1` 个不同的数，这与 `nums` 长度 `n` 矛盾（数组元素可能有重复，但题目没有限制不能重复）。因此答案一定在 `S … S+n` 之间。

这一步的核心思想是 **“鸽巢原理”**：`n` 个格子装不下 `n+1` 只鸽子，必有空格。这里的格子是 `nums` 中的不同数，鸽子是连续的整数。

**核心数据结构**：仍然是 **哈希表（集合）**，因为它提供 **常数时间的查找**，相当于一本“随时可查的字典”。

#### 代码（Python）

```python
from typing import List

def smallest_missing(nums: List[int]) -> int:
    # ---------- 第一次遍历：求最长顺序前缀的和，同时建集合 ----------
    prefix_sum = nums[0]      # 前缀一定包含第一个元素
    present = {nums[0]}       # 把第一个元素放进集合
    for i in range(1, len(nums)):
        present.add(nums[i])  # 同时收集所有出现的数
        if nums[i] == nums[i - 1] + 1:   # 仍然保持顺序
            prefix_sum += nums[i]
        else:                           # 前缀在 i-1 处结束
            break

    # ---------- 第二步：从 prefix_sum 往上找缺失的最小整数 ----------
    x = prefix_sum
    # 根据鸽巢原理，最多检查 n+1 次就能找到答案
    while x in present:
        x += 1
    return x
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 第一次遍历一次搞定前缀和与集合构建。  
  - 第二步最多检查 `n+1` 次（鸽巢原理保证），仍然是线性量级。  

- **空间复杂度**：`O(n)`  
  - 只需要一个集合保存所有出现的数，大小不超过数组长度。

与暴力解相比，最优解把 **两次遍历** 合并成 **一次遍历**，省去了额外的 `O(n)` 循环，使代码更紧凑，且在理论上更快。

---

## 心得

- **核心技巧**：**一次遍历求前缀和 + 哈希表快速判重**，以及 **鸽巢原理**（在有限范围内必有缺失）。
- **适用的题型**  
  1. “找数组中缺失的最小正整数” （LeetCode 41）  
  2. “数组中第一个出现的重复元素”  
  3. “从某个阈值起找不存在的数” 类似的“缺口”问题。
- **一句话总结**：**先把问题限定在一个小范围（前缀和），再用哈希表 O(1) 判重，缺口必然出现。**

---

## 反思

- **第一反应**：先手写两段代码——先算前缀和，再遍历找缺失数。  
- **最容易踩的坑**  
  - 忘记把 **第一个元素** 也计入集合，导致 `x = nums[0]` 时误判为缺失。  
  - 前缀长度为 `1` 时（数组只有一个元素或第二个元素不满足顺序），要确保 `prefix_sum` 只等于 `nums[0]`。  
  - 边界情况：所有可能的整数都出现了（例如 `nums = [1,2,3]`），答案应该是 `sum([1,2,3]) = 6` 本身不在数组里，代码必须能返回 `6` 而不是继续无限循环。  
- **下次遇到同类题**：  
  1. **先定位一个上界**（这里是前缀和），把搜索范围压缩。  
  2. **用集合/哈希表做 O(1) 判重**，避免多次遍历。  
  3. **思考鸽巢原理**：在有限的“格子”里找不到的数一定存在，从而保证循环终止。