# #2453. 摧毁顺序目标 / Destroy Sequential Targets

> 难度：中等 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/destroy-sequential-targets/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of positive integers, representing targets on a number line. You are also given an integer space.
You have a machine which can destroy targets. Seeding the machine with some nums[i] allows it to destroy all targets with values that can be represented as nums[i] + c * space, where c is any non-negative integer. You want to destroy the maximum number of targets in nums.
Return the minimum value of nums[i] you can seed the machine with to destroy the maximum number of targets.

**Examples**

**Example 1:**

```
Input: nums = [3,7,8,1,1,5], space = 2
Output: 1
Explanation: If we seed the machine with nums[3], then we destroy all targets equal to 1,3,5,7,9,... 
In this case, we would destroy 5 total targets (all except for nums[2]). 
It is impossible to destroy more than 5 targets, so we return nums[3].
```

**Example 2:**

```
Input: nums = [1,3,5,2,4,6], space = 2
Output: 1
Explanation: Seeding the machine with nums[0], or nums[3] destroys 3 targets. 
It is not possible to destroy more than 3 targets.
Since nums[0] is the minimal integer that can destroy 3 targets, we return 1.
```

**Example 3:**

```
Input: nums = [6,2,5], space = 100
Output: 2
Explanation: Whatever initial seed we select, we can only destroy 1 target. The minimal seed is nums[1].
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= space <= 109

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的数组 `nums`，其中的元素都是正整数，表示数轴上的若干目标。同时给定一个整数 `space`。  

你拥有一台可以摧毁目标的机器。将机器以某个 `nums[i]` 为种子（seed）后，它能够摧毁所有满足以下形式的目标值：

```
nums[i] + c * space
```

其中 `c` 为任意非负整数。  

你的目标是让机器摧毁 `nums` 中尽可能多的目标。返回能够实现最大摧毁数量的种子 `nums[i]` 的 **最小值**。

---

## 示例

### 示例 1
**输入**  
`nums = [3,7,8,1,1,5], space = 2`  

**输出**  
`1`  

**解释**  
如果我们以 `nums[3]`（值为 1）为种子，则机器会摧毁所有等于 `1, 3, 5, 7, 9, …` 的目标。  
在本例中，能够摧毁 5 个目标（除了 `nums[2] = 8` 之外的全部），已是最大可能数量。因此返回 `nums[3] = 1`。

### 示例 2
**输入**  
`nums = [1,3,5,2,4,6], space = 2`  

**输出**  
`1`  

**解释**  
以 `nums[0]`（值为 1）或 `nums[3]`（值为 2）为种子都能摧毁 3 个目标。  
不可能摧毁超过 3 个目标。  
由于 `nums[0] = 1` 是能够摧毁 3 个目标的最小整数，所以返回 1。

### 示例 3
**输入**  
`nums = [6,2,5], space = 100`  

**输出**  
`2`  

**解释**  
无论选取哪个初始种子，最多只能摧毁 1 个目标。最小的可行种子是 `nums[1] = 2`，因此返回 2。

---

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= space <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个 `nums[i]` 都尝试一次**，看以它为种子能销毁多少目标。  
具体做法：

1. 选定某个 `seed = nums[i]`。  
2. 对数组里的每个元素 `x`，判断它是否满足  
   `x = seed + c * space`（`c ≥ 0 且为整数`）。  
   这等价于检查 `x - seed` 是否是 `space` 的非负倍数，即  
   `x >= seed 且 (x - seed) % space == 0`。  
3. 把满足条件的元素计数，记录最大计数以及对应的最小种子。

**用到的数据结构**：  
- 只需要遍历数组，用 **计数器**（普通整数）记录当前种子能销毁的数量。  
- 没有额外的数据结构，整个过程类似在“查字典”，只不过我们每次都把所有数字逐个对比。

**为什么正确**：  
因为我们穷举了所有可能的种子 `nums[i]`，并且对每个种子检查了所有目标是否满足销毁条件。只要找到了最大的计数，返回对应的最小种子即可。

**时间/空间复杂度**（大白话）：

- 时间复杂度：外层遍历 `n`（`n = len(nums)`）次，内层又遍历 `n` 次做判断，**总共是 n × n**，也就是 **O(n²)**。如果 `n = 10⁵`，那就是 10⁵ × 10⁵ = 10¹⁰ 次操作，显然会超时。  
- 空间复杂度：只用了常数个额外变量（计数器、答案），**O(1)**，即不随 `n` 增长。

#### 代码（Python）

```python
from typing import List

def destroyTargets_bruteforce(nums: List[int], space: int) -> int:
    """
    暴力解：枚举每个 nums[i] 作为种子，逐个检查所有元素是否可被销毁。
    """
    n = len(nums)
    best_cnt = 0          # 当前最大可以销毁的数量
    best_seed = float('inf')  # 对应的最小种子

    for i in range(n):
        seed = nums[i]
        cnt = 0
        for x in nums:
            # x 能被销毁的条件：x >= seed 且 (x - seed) 是 space 的倍数
            if x >= seed and (x - seed) % space == 0:
                cnt += 1
        # 更新答案：先比较销毁数量，数量相同再取最小的种子
        if cnt > best_cnt or (cnt == best_cnt and seed < best_seed):
            best_cnt = cnt
            best_seed = seed

    return best_seed
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 需要对每个种子检查数组中的所有元素，等价于“把 n×n 次比较全部做一遍”。  
- **空间复杂度**：`O(1)` — 只用了几个计数变量，不会随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历整个数组去计数**。  
观察条件 `x = seed + c * space`（`c ≥ 0`）可以改写为：

```
x % space == seed % space    且    x >= seed
```

也就是说，只要两个数在模 `space` 意义下余数相同，它们就位于同一条“等差数列”上。  
如果我们只关心 **“同余类”**（余数相同的那一组），那么在同一个余数下，**越小的种子可以覆盖越多的元素**——因为它能向右“延伸”到所有更大的同余数的元素。

因此，**把所有数字按照 `num % space` 分组**，每一组内部只需要记住：

- 该组出现了多少次（即可以被同一个种子一次性销毁的目标数量）。  
- 组内最小的原始数值（因为我们要返回最小的 `nums[i]`）。

步骤如下：

1. 用哈希表 `cnt` 统计每个余数 `r = num % space` 出现的次数。  
2. 同时用另一个哈希表 `min_val` 记录该余数对应的最小原始数值。  
   - 这相当于在“查字典”：key 是余数，value 是出现次数或最小值。  
3. 遍历所有余数，找到出现次数 **最大的** 那一组；如果有多组出现次数相同，则取 **最小的原始数值**。  
4. 该最小数值就是答案，因为它是可以销毁最多目标的种子中最小的那个。

**核心算法/数据结构**：

- **哈希表（字典）**：把 “余数 → 次数” 以及 “余数 → 最小值” 记录下来。查找和插入都是 **O(1)** 的平均时间，类似在字典里查词条。  
- **同余类**：把数轴上的点按 `space` 的间隔分层，余数相同的点就在同一层，机器种子只要落在该层的最左端（最小值），就能覆盖整层。

**为什么这样就快了**：我们只遍历一次数组（`O(n)`），把所有信息压缩进哈希表，再遍历哈希表的键（最多 `space` 种，但实际不超过 `n`），整体时间是线性的。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def destroyTargets(nums: List[int], space: int) -> int:
    """
    最优解：利用同余类（余数）把同一条等差数列的元素归到一起。
    只需一次遍历即可得到每个余数的出现次数和最小原始数值。
    """
    # cnt[r] = 该余数 r 出现的次数
    cnt = defaultdict(int)
    # min_val[r] = 余数 r 对应的最小 nums[i]（种子候选）
    min_val = {}

    for x in nums:
        r = x % space                # 余数，相当于“把数划到哪条等差数列”
        cnt[r] += 1                  # 该余数的计数加一
        # 更新该余数对应的最小值
        if r not in min_val or x < min_val[r]:
            min_val[r] = x

    # 在所有余数中寻找“最多目标”且“最小种子”的组合
    best_cnt = -1
    answer = float('inf')
    for r, c in cnt.items():
        if c > best_cnt or (c == best_cnt and min_val[r] < answer):
            best_cnt = c
            answer = min_val[r]

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次 `nums`（`n = len(nums)`），每次哈希操作均摊为常数时间。相比暴力的 `O(n²)`，快了 **n 倍**。  
- **空间复杂度**：`O(k)`，其中 `k` 是不同余数的个数，最多不超过 `n`，所以最坏情况下是 `O(n)` 的额外空间（哈希表保存计数和最小值）。

---

## 心得

- **核心技巧**：**同余分组（余数哈希）**。把满足 `a = b + c·space` 的数归到同一个余数类里，只需要统计每类的出现次数和最小元素即可。  
- **适用的题型**：  
  1. “把数组按照某个步长划分，同余类统计”——例如 *“Maximum Number of Points With Same Modulo”*。  
  2. “找出满足等差关系的最大子集”——如 *“Arithmetic Subarray”*。  
  3. “在环形结构上找最密集的点”——比如 *“Circular Array Maximum Points”*。  
- **一句话总结**：**把“能被同一个种子销毁”的数看成同余类，只需在每个余数里挑最小的那个即可**。

---

## 反思

- **第一反应**：直接枚举每个 `nums[i]`，逐个检查是否满足 `seed + c·space`，也就是暴力搜索。  
- **最容易踩的坑**：  
  - 忘记 **`x >= seed`** 的限制，只检查同余会把比种子小的数也算进去，导致计数错误。  
  - 对 `space` 很大（如 10⁹）时误以为需要创建长度为 `space` 的数组，实际只需要用哈希表保存出现的余数。  
  - 边界情况：所有数互不相同且 `space` 超大，此时每个余数只出现一次，答案应是数组的最小元素。  
- **下次类似题目**的第一步：**先把问题抽象成“余数/模”或“等差关系”，看看能否把大量比较压缩成哈希计数**。这样往往能把 `O(n²)` 降到 `O(n)`。