# #2855. 最小右移次数使数组有序 / Minimum Right Shifts to Sort the Array

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/minimum-right-shifts-to-sort-the-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of length n containing distinct positive integers. Return the minimum number of right shifts required to sort nums and -1 if this is not possible.
A right shift is defined as shifting the element at index i to index (i + 1) % n, for all indices.

**Examples**

**Example 1:**

```
Input: nums = [3,4,5,1,2]
Output: 2
Explanation: 
After the first right shift, nums = [2,3,4,5,1].
After the second right shift, nums = [1,2,3,4,5].
Now nums is sorted; therefore the answer is 2.
```

**Example 2:**

```
Input: nums = [1,3,5]
Output: 0
Explanation: nums is already sorted therefore, the answer is 0.
```

**Example 3:**

```
Input: nums = [2,1,4]
Output: -1
Explanation: It's impossible to sort the array using right shifts.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- nums contains distinct integers.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始、长度为 `n` 的数组 `nums`，其中包含互不相同的正整数。返回使 `nums` 有序（sorted）所需的最小右移次数（right shift），如果无法通过右移得到有序数组则返回 `-1`。  
右移的定义是：对所有下标 `i`，将下标为 `i` 的元素移动到下标 `(i + 1) % n` 的位置。

**示例**

*示例 1*  
输入: `nums = [3,4,5,1,2]`  
输出: `2`  
解释:  
第一次右移后，`nums = [2,3,4,5,1]`。  
第二次右移后，`nums = [1,2,3,4,5]`。  
此时数组已排序（sorted），因此答案为 `2`。

*示例 2*  
输入: `nums = [1,3,5]`  
输出: `0`  
解释: 数组已经是有序的（sorted），所以答案为 `0`。

*示例 3*  
输入: `nums = [2,1,4]`  
输出: `-1`  
解释: 无法通过右移使数组有序（sorted），因此返回 `-1`。

**约束条件**  
- `1 <= nums.length <= 100`  
- `1 <= nums[i] <= 100`  
- `nums` 中的整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把右移操作一次一次地模拟**，每次右移后检查数组是否已经是递增有序的。如果有序，就把已经做的右移次数返回；如果全部 `n` 次（数组长度）都没有出现有序的情况，说明根本不可能通过右移得到有序数组，返回 `-1`。

- **用到的数据结构**：  
  - `list`（数组本身），我们会把它复制一份再做右移，避免把原数组破坏。  
  - “哈希表”在这里不需要，用到的唯一工具就是**遍历**，就像我们在超市里把每件商品依次检查一遍，看看有没有过期。

- **为什么正确**：  
  - 右移的定义是“把每个元素往后搬一格，最后一个搬到最前面”。如果我们真的能通过若干次右移把数组排好序，那么必然会在 **0 ≤ k < n** 次右移中出现一次排好序的状态（因为右移 `n` 次会回到原来的排列）。所以枚举所有可能的 `k` 并检查即可。

- **复杂度分析（大白话）**：  
  - **时间**：我们最多要做 `n` 次右移，每次右移要遍历整个数组检查是否有序，遍历一次是 `n` 步，所以总共是 `n × n = n²` 步。用大写的 **O(n²)** 表示，意思是“随着数组长度的增长，耗时会像平方一样快”。  
  - **空间**：我们只需要一个额外的同样大小的数组来保存每次右移后的结果，大小是 `n`，记作 **O(n)**。如果直接在原数组上原地右移，还可以把空间降到 **O(1)**（常数级），但为了代码更易懂这里使用额外数组。

#### 代码（Python）

```python
def min_right_shifts_bruteforce(nums):
    """
    暴力模拟：每次右移后检查是否已经有序
    :param nums: List[int]，题目给定的数组（不修改原数组）
    :return: 最少右移次数，若不可能返回 -1
    """
    n = len(nums)
    # 已经有序直接返回 0
    if nums == sorted(nums):
        return 0

    # 把原数组复制一份，后面会在这份上做右移
    cur = nums[:]

    for shift in range(1, n + 1):               # 最多右移 n 次
        # 右移一步：把最后一个元素搬到最前面，其余元素整体向后平移
        cur = [cur[-1]] + cur[:-1]               # 关键行：实现右移

        # 检查是否有序
        if cur == sorted(cur):                  # 如果已经升序
            return shift                        # 返回当前右移次数

    # 循环结束仍未有序，说明不可能
    return -1
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：如果 `n = 100`，最多要检查 `100 × 100 = 10,000` 步。随着 `n` 增大，耗时会以平方的速度增长。
- **空间复杂度**：`O(n)`  
  - 解释：我们额外保存了一个长度为 `n` 的数组 `cur`，占用的空间随 `n` 成线性关系增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都把整个数组重新右移并检查**，这相当于把同一个过程重复了 `n` 次。其实右移的本质是**把数组视为一个环，找出环上的“断点”**——也就是数组中第一个出现 **下降** 的位置（`nums[i] < nums[i‑1]`）。如果这样的下降点恰好 **只有一个**，并且把数组从该点切开后拼接起来是升序的，那么这就是一个**旋转有序数组**，只需要一次数学计算就能得到答案。

具体步骤：

1. **统计下降点的数量**  
   - 遍历一遍数组，记录下满足 `nums[i] < nums[i-1]` 的下标 `i`。  
   - 如果出现 **0** 次，说明数组本身已经有序，答案是 `0`。  
   - 如果出现 **>1** 次，说明数组不是单纯的旋转有序（会出现多个不连续的“乱序”，根本无法通过右移恢复），答案是 `-1`。

2. **唯一的下降点**  
   - 设唯一的下降点下标为 `pivot = i`（`i` 从 `1` 开始），此时 `nums[pivot]` 是最小的元素。  
   - 为了把数组变成有序，需要把 **pivot** 前面的所有元素整体搬到后面，也就是 **右移 `n - pivot` 次**（因为每一次右移都把最后一个元素搬到最前面）。  
   - 但是我们还要再确认：把数组切成两段 `[pivot … n‑1]` 和 `[0 … pivot‑1]` 后拼接起来是否真的严格递增。只要 `nums[pivot:] + nums[:pivot]` 与 `sorted(nums)` 完全相同即可。

3. **返回答案**  
   - 若验证通过，返回 `n - pivot`；否则返回 `-1`（理论上不会出现这种情况，因为唯一的下降点已经保证了整体是旋转有序的，但写上防御性检查更严谨）。

> **类比**：想象一根围着圆形跑道的跑步标志牌，上面写着数字。正常情况下数字应该顺时针递增。如果标牌在某个位置被搬到了跑道的起点（即出现一次“断点”），我们只需要把跑道整体顺时针转动几格，就能让数字重新按顺序排列。

#### 代码（Python）

```python
def min_right_shifts_optimal(nums):
    """
    最优解：利用“旋转有序数组”的特性一次遍历找出唯一的下降点
    :param nums: List[int]，不含重复元素的正整数数组
    :return: 最少右移次数，若不可能返回 -1
    """
    n = len(nums)
    if n == 1:                     # 单元素数组天然有序
        return 0

    # 1. 找出所有下降点的下标
    drop_indices = []              # 用来保存 i，使得 nums[i] < nums[i-1]
    for i in range(1, n):
        if nums[i] < nums[i - 1]:
            drop_indices.append(i)

    # 2. 根据下降点的个数判断情况
    if len(drop_indices) == 0:     # 完全有序
        return 0
    if len(drop_indices) > 1:      # 多于一个断点，无法通过右移恢复
        return -1

    # 3. 唯一的下降点
    pivot = drop_indices[0]        # 该位置是最小元素的下标

    # 4. 验证切分后拼接是否真的有序（防御性检查）
    rotated = nums[pivot:] + nums[:pivot]
    if rotated != sorted(nums):    # 若不等，说明不是合法的旋转有序数组
        return -1

    # 5. 计算需要的右移次数：把前面的 (pivot) 个元素搬到后面
    #    每一次右移都把最后一个元素搬到最前面，所以需要 n - pivot 次
    return n - pivot
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：只遍历了一遍数组（`n` 步），后面的拼接与排序比较在最坏情况下也是线性时间（因为 `sorted(nums)` 只需要 `O(n log n)`，但这里我们可以直接比较两段是否递增，仍然是 `O(n)`），总体随 `n` 成线性增长。相较于暴力的 `O(n²)`，提升显著。

- **空间复杂度**：`O(1)`（不计返回的整数）  
  - 解释：只用了常数个额外变量 `drop_indices`（最多保存两个下标）和 `pivot`，没有随 `n` 增长的额外存储。如果把 `rotated` 用切片实现而不复制（`rotated = nums[pivot:] + nums[:pivot]` 会产生新列表），仍然最多占用 `O(n)` 的临时空间，但可以改写为逐个比较来做到真·`O(1)`。这里为了代码简洁保留了切片，空间仍然是线性级别。

---

## 心得

- **核心技巧**：判断数组是否是“**旋转有序**”，即只出现一次下降点。  
- **适用的题型**：  
  1. “寻找旋转数组的最小值” (`Find Minimum in Rotated Sorted Array`)  
  2. “判断数组是否可以通过一次旋转变为有序” (`Check if Array Is Sorted after Rotation`)  
  3. “最大连续递增子数组长度” 之类需要先定位断点的题目。  
- **一句话总结**：**“只要数组只有一个‘断点’，右移的次数就是数组长度减去断点位置。”**

---

## 反思

- **第一反应**：直接想到模拟右移——最直观但最慢的办法。  
- **最容易踩的坑**：  
  - 忽略 **多个下降点** 的情况，导致错误地返回一个右移次数。  
  - 没有检查 **切分后拼接是否真的有序**（例如 `[3,1,2]` 只出现一次下降点，但拼接后仍不是升序）。  
  - 边界条件：长度为 `1` 的数组、已经有序的数组以及全逆序的数组。  
- **下次类似题的第一步**：先 **统计数组中的下降点**（`nums[i] < nums[i-1]`），依据其数量快速判断是否可能以及可能的右移次数。