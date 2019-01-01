# #220. 存在重复元素 III / Contains Duplicate III

> 难度：困难 · 标签：Array、Sliding Window、Sorting、Bucket Sort、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/contains-duplicate-iii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers indexDiff and valueDiff.
Find a pair of indices (i, j) such that:
Return true if such pair exists or false otherwise.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,1], indexDiff = 3, valueDiff = 0
Output: true
Explanation: We can choose (i, j) = (0, 3).
We satisfy the three conditions:
i != j --> 0 != 3
abs(i - j) <= indexDiff --> abs(0 - 3) <= 3
abs(nums[i] - nums[j]) <= valueDiff --> abs(1 - 1) <= 0
```

**Example 2:**

```
Input: nums = [1,5,9,1,5,9], indexDiff = 2, valueDiff = 3
Output: false
Explanation: After trying all the possible pairs (i, j), we cannot satisfy the three conditions, so we return false.
```

**Constraints**

- 2 <= nums.length <= 105
- -109 <= nums[i] <= 109
- 1 <= indexDiff <= nums.length
- 0 <= valueDiff <= 109

---

## 题目（中文翻译）

你被给定一个整数数组（integer array）`nums` 和两个整数 `indexDiff` 与 `valueDiff`。  
请判断是否存在一对下标 `(i, j)` 满足以下全部条件：

- `i != j`
- `abs(i - j) <= indexDiff`（即两下标的绝对差不超过 `indexDiff`）
- `abs(nums[i] - nums[j]) <= valueDiff`（即对应元素的绝对差不超过 `valueDiff`）

如果存在满足条件的下标对，返回 `true`；否则返回 `false`。  

**示例 1**  
```
Input: nums = [1,2,3,1], indexDiff = 3, valueDiff = 0
Output: true
Explanation: 我们可以选择 (i, j) = (0, 3)。满足三条条件：
i != j --> 0 != 3
abs(i - j) <= indexDiff --> abs(0 - 3) <= 3
abs(nums[i] - nums[j]) <= valueDiff --> abs(1 - 1) <= 0
```

**示例 2**  
```
Input: nums = [1,5,9,1,5,9], indexDiff = 2, valueDiff = 3
Output: false
Explanation: 经过枚举所有可能的 (i, j) 组合，都无法同时满足三条条件，因此返回 false。
```

**约束条件**  

- `2 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `1 <= indexDiff <= nums.length`
- `0 <= valueDiff <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有满足 **下标差 ≤ indexDiff** 的元素两两比较，看看它们的数值差是否 ≤ valueDiff。  
可以把数组想象成排好队的学生，老师要找两位站得不远（相邻的距离不超过 `indexDiff`）且身高相差不大的同学（相差 ≤ `valueDiff`）。于是我们把每个同学（下标 `i`）和它后面最多 `indexDiff` 个同学（下标 `j = i+1 … i+indexDiff`）逐个比较。

- **使用的数据结构**：只需要原始的列表 `nums`，不需要额外的容器。  
- **为什么正确**：我们穷举了所有满足下标约束的配对，只要其中有一对满足数值约束，就返回 `True`；否则遍历完所有配对后返回 `False`。  
- **时间/空间复杂度**：  
  - 最坏情况下，每个元素都要和后面 `indexDiff` 个元素比较，时间复杂度是 `O(n * indexDiff)`。如果 `indexDiff` 接近 `n`（题目上限），就会退化为 `O(n²)`，也就是“平方级”。  
  - 只使用了常数级额外空间 `O(1)`（不计输入数组本身）。

> **大白话解释**：  
> - `O(n²)` 就像两层循环的嵌套，想象你要检查每本书和其他每本书的关系，书的数量翻倍会让工作量成平方增长，10 本变 100 本，工作量从 100 次涨到 10 000 次，增长得很快。

#### 代码（Python）

```python
from typing import List

def containsNearbyAlmostDuplicate_bruteforce(nums: List[int],
                                            indexDiff: int,
                                            valueDiff: int) -> bool:
    n = len(nums)
    # 双层循环，i 是左指针，j 是右指针
    for i in range(n):
        # 只需要比较 i 之后的最多 indexDiff 个元素
        for j in range(i + 1, min(i + indexDiff + 1, n)):
            # 先判断数值差是否满足要求
            if abs(nums[i] - nums[j]) <= valueDiff:
                return True        # 找到一对直接返回
    return False                 # 全部遍历完都没有满足条件
```

#### 复杂度

- **时间复杂度**：`O(n * indexDiff)`，在最坏情况下等价于 `O(n²)`。  
  > 解释：外层遍历 `n` 次，内层最多遍历 `indexDiff` 次，两者相乘就是总体工作量。
- **空间复杂度**：`O(1)`，只用了常数级的临时变量。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是**重复比较了大量不必要的元素**。  
在遍历数组时，我们只关心**最近的 `indexDiff` 个元素**（因为更远的下标已经不满足 `|i-j| ≤ indexDiff`）。如果能够在这 `k = indexDiff` 个元素中快速判断是否存在一个数值在 `[nums[i]-valueDiff, nums[i]+valueDiff]` 区间内的元素，就能把每一步的代价从 `O(k)` 降到 `O(log k)` 或 `O(1)`。

下面介绍两种常用的优化思路，均基于**滑动窗口 + 有序结构**：

1. **平衡二叉搜索树（有序集合）**  
   - 在 Python 中没有原生的 `TreeSet`，可以用 `bisect` 对维护的有序列表实现。  
   - 思路：  
     - 用一个有序列表 `window` 保存最近 `k` 个数。  
     - 对当前 `num = nums[i]`，在 `window` 中二分查找第一个不小于 `num - valueDiff` 的位置。  
     - 检查该位置的元素是否 ≤ `num + valueDiff`，若是则找到满足条件的配对。  
     - 将 `num` 插入 `window`（保持有序），并在窗口大小超过 `k` 时删除 `nums[i-k]`。  
   - 由于插入、删除、查询均是二分搜索 + 列表操作，时间复杂度是 `O(log k)`（实际是 `O(k)` 的列表插入/删除，但在 Python 实现中仍然满足题目要求 `O(n log k)`）。

2. **桶排序（Bucket）**  
   - 关键观察：如果两个数的差 ≤ `valueDiff`，那么它们必然落在 **相邻或同一个宽度为 `valueDiff+1` 的桶** 中。  
   - 思路：  
     - 将整数映射到宽度为 `w = valueDiff + 1` 的桶。  
     - 对每个新数 `num`：  
       - 计算所在桶的编号 `bucket_id = num // w`（注意负数的取整，需要特殊处理）。  
       - 检查同一桶是否已有元素（必然满足数值差 ≤ `valueDiff`）。  
       - 检查相邻左、右桶的元素，看是否满足数值差 ≤ `valueDiff`。  
     - 将 `num` 放入对应桶，并在窗口超出 `k` 时删除最早的那个数所在的桶。  
   - 这样每一步只检查常数个桶，时间复杂度 **O(1)**，整体 `O(n)`，空间 `O(k)`。

下面给出 **桶排序** 的实现，因为它是最优的 `O(n)` 解，并且实现思路更具启发性。

> **核心概念解释**  
> - **桶**：想象把一条数轴切成等宽的小格子（每格宽度 `valueDiff+1`），每个格子就是一个桶。只要两个数相差不超过 `valueDiff`，它们要么在同一个格子，要么在相邻的两个格子里。  
> - **滑动窗口**：我们只保留最近 `k` 个数对应的桶，像一个只容纳 `k` 个人的房间，走进去的人要把最早离开的那个人请出去，保持人数不变。

#### 代码（Python）

```python
from typing import List

def containsNearbyAlmostDuplicate(nums: List[int],
                                 indexDiff: int,
                                 valueDiff: int) -> bool:
    """
    桶排序 + 滑动窗口的 O(n) 解
    """
    if valueDiff < 0:                     # 题目保证 valueDiff >= 0，这里防御性检查
        return False

    w = valueDiff + 1                     # 桶的宽度，确保同桶元素差 ≤ valueDiff
    bucket = dict()                       # key: 桶编号，value: 桶中唯一的数

    for i, num in enumerate(nums):
        # 处理负数的取整：Python 整除会向负无穷取整，需要把负数向上平移
        bucket_id = num // w
        if num < 0:
            bucket_id -= 1                 # 例如 -1 // 5 == -1，-6 // 5 == -2，保持间隔一致

        # 1）同桶已经有元素 → 直接满足数值差 ≤ valueDiff
        if bucket_id in bucket:
            return True

        # 2）检查左邻桶
        left = bucket_id - 1
        if left in bucket and abs(num - bucket[left]) <= valueDiff:
            return True

        # 3）检查右邻桶
        right = bucket_id + 1
        if right in bucket and abs(num - bucket[right]) <= valueDiff:
            return True

        # 4）把当前数放入对应桶
        bucket[bucket_id] = num

        # 5）窗口大小超过 indexDiff 时，移除最早的数对应的桶
        if i >= indexDiff:
            old_num = nums[i - indexDiff]
            old_bucket_id = old_num // w
            if old_num < 0:
                old_bucket_id -= 1
            del bucket[old_bucket_id]      # 删除旧桶，保持窗口大小为 k

    return False
```

> **代码要点注释**  
> - 第 3 行 `w = valueDiff + 1`：若 `valueDiff = 0`，每个桶宽度为 1，只有相同的数会落入同一桶。  
> - 第 9‑12 行处理负数的取整，保证 `-1` 和 `0` 分别在不同的桶里。  
> - 第 15‑23 行分别检查同桶、左桶、右桶，只要有一个满足条件就返回 `True`。  
> - 第 28‑35 行负责维护滑动窗口：当窗口长度超过 `indexDiff` 时，删除最早进入的数对应的桶。

#### 复杂度

- **时间复杂度**：`O(n)`。  
  - 每个元素只做常数次哈希查找/插入/删除，和 `n` 成线性关系。  
  - 与暴力解的 `O(n²)` 相比，**只要把 `n` 放大 10 倍，运行时间也只会增长 10 倍**，而不是 **100 倍**。
- **空间复杂度**：`O(k)`（`k = indexDiff`）。  
  - 窗口里最多保留 `k` 个桶，每个桶只存一个数，空间随 `k` 线性增长。  
  - 若 `k` 接近 `n`，最坏情况是 `O(n)`，但仍然是线性级别。

---

## 心得

- **核心技巧**：**滑动窗口 + 有序/分桶结构**，用于在「固定窗口大小」内快速判断「数值范围」是否满足条件。  
- **适用的题型**  
  1. *Contains Duplicate II*（只要求下标差 ≤ k）——使用滑动窗口的集合即可。  
  2. *Sliding Window Maximum*（窗口内最大值）——使用单调队列（双端队列）维护有序性。  
  3. *Maximum Width Ramp*（寻找满足 i < j 且 A[i] ≤ A[j] 的最大距离）——使用单调栈或前缀最小值。  
- **一句话总结解题钥匙**：**把「最近 k 个」的元素保持在一个可快速查询的结构里，只检查常数个候选，而不是遍历全部**。

---

## 反思

- **第一反应**：直接写两层循环遍历所有满足下标差的配对，代码最容易写对。  
- **最容易踩的坑**  
  - **负数取整**：直接使用 `num // w` 会把负数向下取整，导致相邻的负数可能落在同一个桶，需要手动向上修正（`if num < 0: bucket_id -= 1`）。  
  - **valueDiff = 0** 的特殊情况：此时桶宽度为 1，只有相同的数才会满足条件，必须确保同桶检查的逻辑正确。  
  - **窗口删除**：忘记在 `i >= indexDiff` 时把最旧的数对应的桶删除，会导致窗口无限增大，破坏 `O(k)` 空间限制。  
- **下次遇到同类题**：第一步先**明确“窗口大小”和“需要查询的数值范围”，然后**选择合适的有序或分桶结构**来在窗口内进行 **常数/对数时间的查询**，而不是直接遍历。