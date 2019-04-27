# #398. 随机索引 / Random Pick Index

> 难度：中等 · 标签：Hash Table、Math、Reservoir Sampling、Randomized · [LeetCode 链接](https://leetcode.com/problems/random-pick-index/)

---

## 题目（英文原版）

**Description**

Given an integer array nums with possible duplicates, randomly output the index of a given target number. You can assume that the given target number must exist in the array.
Implement the Solution class:

**Examples**

**Example 1:**

```
Input
["Solution", "pick", "pick", "pick"]
[[[1, 2, 3, 3, 3]], [3], [1], [3]]
Output
[null, 4, 0, 2]

Explanation
Solution solution = new Solution([1, 2, 3, 3, 3]);
solution.pick(3); // It should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
solution.pick(1); // It should return 0. Since in the array only nums[0] is equal to 1.
solution.pick(3); // It should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- -231 <= nums[i] <= 231 - 1
- target is an integer from nums.
- At most 104 calls will be made to pick.

---

## 题目（中文翻译）

给定一个可能包含重复元素的整数数组（array）`nums`，随机返回给定目标值的一个索引（index）。可以保证目标值一定存在于数组中。

实现 `Solution` 类，使其满足以下接口：

```java
class Solution {
    public Solution(int[] nums) { … }
    public int pick(int target) { … }
}
```

**示例 1**

```
Input
["Solution", "pick", "pick", "pick"]
[[[1, 2, 3, 3, 3]], [3], [1], [3]]
Output
[null, 4, 0, 2]
```

**解释**

```
Solution solution = new Solution([1, 2, 3, 3, 3]);
solution.pick(3); // 应随机返回下标 2、3 或 4 中的任意一个。每个下标被返回的概率相等。
solution.pick(1); // 应返回 0，因为数组中只有 nums[0] 等于 1。
solution.pick(3); // 同上，随机返回下标 2、3 或 4，概率相等。
```

**约束条件**

- `1 <= nums.length <= 2 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `target` 为 `nums` 中的一个整数
- 最多调用 `pick` 方法 `10^4` 次

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次要 pick(target) 时，都把数组从头遍历一遍，找出所有等于 target 的下标，放进一个临时列表，然后随机挑一个返回**。  

- **用到的数据结构**：  
  - **列表（list）**：把符合条件的下标一个一个装进去，就像把所有符合条件的“钥匙”放进一个抽屉，随后从抽屉里随手抽一把。  
- **为什么正确**：  
  - 我们遍历了整个数组，保证每一个等于 target 的位置都被收集进来了。随后使用 `random.choice`（等概率抽取）从这些下标中挑一个，自然每个合法下标出现的概率相同。  
- **时间/空间复杂度的大白话**：  
  - **时间复杂度 O(n)**：这里的 `n` 是数组长度。想象你要检查一箱子 1000 颗糖，每颗都要尝一尝是否是红色的，这就需要 1000 次“尝”。  
  - **空间复杂度 O(k)**：`k` 是 target 出现的次数。最坏情况 target 出现在所有位置，空间就会是 O(n)。这相当于把所有符合条件的糖都挑出来放进另一个盒子，盒子大小随符合条件的糖数量线性增长。

#### 代码（Python）

```python
import random
from typing import List

class Solution:
    def __init__(self, nums: List[int]):
        self.nums = nums                     # 保存原数组

    def pick(self, target: int) -> int:
        # 1️⃣ 把所有等于 target 的下标收集起来
        candidates = []                     # 用列表当“抽屉”
        for i, v in enumerate(self.nums):   # enumerate 同时给出下标 i 和元素值 v
            if v == target:                 # 符合条件就放进抽屉
                candidates.append(i)

        # 2️⃣ 随机抽取一个下标返回
        # random.choice 从列表里等概率抽一个元素
        return random.choice(candidates)    # 直接返回抽中的下标
```

#### 复杂度  

- **时间复杂度**：**O(n)**  
  - 每次调用 `pick` 都要遍历整个数组一次。想象你在一次抽奖活动里，需要把所有参与者的号码都写下来再抽，这一步是线性的。  
- **空间复杂度**：**O(k)**（`k` 为目标出现次数）  
  - 只在临时列表里保存符合条件的下标。最坏情况下 `k = n`，所以空间最多是 O(n)。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，**慢的地方在于每次 `pick` 都要遍历整个数组**。如果我们可以把“哪些下标对应哪些数字”这件事**提前算好**，后面每次查询就可以 **O(1)** 完成。  

**一步步推导**：

1. **预处理阶段**（构造对象时）  
   - 把数组一次遍历，建立一个 **哈希表（字典）**：`value → [所有下标]`。  
   - 哈希表就像一本“下标目录”，把每个数字的所有出现位置记录下来，查找时只要把数字当作关键字（key），马上能得到对应的下标列表。  

2. **查询阶段**（`pick`）  
   - 直接从哈希表里取出目标数字对应的下标列表。  
   - 使用 `random.choice` 在这个列表里等概率抽一个下标返回。  

这样 **遍历数组只做一次**（在 `__init__`），后面的每次 `pick` 只需要 O(1) 的时间。  

**核心数据结构：哈希表（字典）**  
- 类比：**查字典**。字典的“词条”是数组里的数值，**页码**是该数值出现的所有位置。你只要知道词条，就能瞬间翻到对应的页码列表。  

如果出于内存限制不能一次性保存所有下标列表，也可以在每次 `pick` 时使用 **Reservoir Sampling（水塘抽样）**，只遍历一次数组但仍保持等概率抽取。这里我们把两种思路都写出来，后者是 **空间最优**（O(1) 额外空间）但时间仍是 O(n) 每次调用。

#### 代码（Python）  

##### 方法一：哈希表预处理（推荐）

```python
import random
from collections import defaultdict
from typing import List, Dict

class Solution:
    def __init__(self, nums: List[int]):
        # 1️⃣ 预处理：把每个数字对应的所有下标收集起来
        self.idx_map: Dict[int, List[int]] = defaultdict(list)
        for i, v in enumerate(nums):
            self.idx_map[v].append(i)      # v 出现一次，就把 i 加到它的列表里
        # 现在 idx_map[3] == [2, 3, 4]（示例数组中 3 的所有下标）

    def pick(self, target: int) -> int:
        # 2️⃣ 直接从对应的下标列表里等概率抽取
        # random.choice 能在 O(1) 时间内抽取列表中的任意元素
        return random.choice(self.idx_map[target])
```

##### 方法二：Reservoir Sampling（空间 O(1)）

```python
import random
from typing import List

class Solution:
    def __init__(self, nums: List[int]):
        self.nums = nums                     # 只保存原数组，不额外建哈希表

    def pick(self, target: int) -> int:
        # Reservoir Sampling 的核心：遍历一次数组，遇到 target 时以 1/(已遇到次数) 的概率保留当前下标
        count = 0          # 已经看到多少个 target
        result = -1        # 最终返回的下标
        for i, v in enumerate(self.nums):
            if v == target:
                count += 1
                # 生成 0~1 之间的随机数，如果小于 1/count，就选当前下标
                if random.random() < 1 / count:
                    result = i
        return result
```

#### 复杂度  

- **方法一（哈希表）**  
  - **时间复杂度**：  
    - 构造阶段 O(n)（只遍历一次数组），后续每次 `pick` 为 **O(1)**（直接取列表并抽取）。  
    - 对比暴力解的 O(n) 每次调用，提升明显。  
  - **空间复杂度**：**O(n)**（存放所有下标），相当于为每个数字准备了一本“下标目录”。  

- **方法二（Reservoir Sampling）**  
  - **时间复杂度**：每次 `pick` 仍是 **O(n)**，因为要遍历整个数组一次。  
  - **空间复杂度**：**O(1)**（只使用几个计数器），适合内存极限严格的场景。  
  - 与暴力解相比，**时间相同**，但不需要额外的列表存储，省空间。  

---

## 心得  

- **核心技巧**：  
  - **哈希表**（映射）把「值」和「所有出现位置」关联起来，实现 **一次预处理、常数时间查询**。  
  - **Reservoir Sampling**（水塘抽样）在不事先知道元素总数的情况下，仍能 **等概率抽取**，且只用 **O(1) 额外空间**。  

- **适用的题型**（类似技巧）  
  1. **“随机取值”** 系列，如 “Random Pick with Weight”。  
  2. **“统计出现次数并快速查询”**，如 “Ransom Note”（判断字符是否足够）可以用哈希表计数。  
  3. **流式数据等概率抽样**，如 “Shuffle an Array” 需要 Fisher‑Yates 洗牌。  

- **一句话总结解题钥匙**：  
  > **把“要找的东西”提前做好索引（哈希表），或在一次遍历中使用水塘抽样保持等概率。**  

---

## 反思  

- **第一反应**：直接遍历数组收集目标下标，再随机抽取——这是最自然的“先找后抽”。  
- **最容易踩的坑**：  
  - **忘记等概率**：如果只在遍历时记录最后一次出现的下标，会导致概率偏向后面的元素。  
  - **边界条件**：目标只出现一次时，列表只有一个元素，`random.choice` 仍能正常工作。  
  - **多次调用的效率**：如果每次都完整遍历，时间会爆炸；必须在构造阶段做好准备（哈希表）或使用水塘抽样。  
- **下次遇到同类题**，第一步应该思考：**“这道题是否可以把查询的关键信息提前预处理成哈希表（或其他索引结构）？”** 如果内存受限，再考虑 **“一次遍历中如何保持等概率（Reservoir Sampling）？”**