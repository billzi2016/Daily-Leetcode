# #1909. 移除一个元素后使数组严格递增 / Remove One Element to Make the Array Strictly Increasing

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/remove-one-element-to-make-the-array-strictly-increasing/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums, return true if it can be made strictly increasing after removing exactly one element, or false otherwise. If the array is already strictly increasing, return true.
The array nums is strictly increasing if nums[i - 1] < nums[i] for each index (1 <= i < nums.length).

**Examples**

**Example 1:**

```
Input: nums = [1,2,10,5,7]
Output: true
Explanation: By removing 10 at index 2 from nums, it becomes [1,2,5,7].
[1,2,5,7] is strictly increasing, so return true.
```

**Example 2:**

```
Input: nums = [2,3,1,2]
Output: false
Explanation:
[3,1,2] is the result of removing the element at index 0.
[2,1,2] is the result of removing the element at index 1.
[2,3,2] is the result of removing the element at index 2.
[2,3,1] is the result of removing the element at index 3.
No resulting array is strictly increasing, so return false.
```

**Example 3:**

```
Input: nums = [1,1,1]
Output: false
Explanation: The result of removing any element is [1,1].
[1,1] is not strictly increasing, so return false.
```

**Constraints**

- 2 <= nums.length <= 1000
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个 **0 索引整数数组 (0-indexed integer array)** `nums`，如果在恰好移除 **一个元素** 后可以使数组 **严格递增（strictly increasing）**，则返回 `true`，否则返回 `false`。如果数组本身已经是严格递增的，也返回 `true`。  

数组 `nums` 在满足 `nums[i - 1] < nums[i]`（对所有 `1 <= i < nums.length`）时称为 **严格递增（strictly increasing）**。

## 示例

### 示例 1
**输入**: `nums = [1,2,10,5,7]`  
**输出**: `true`  
**解释**: 移除下标 `2` 处的 `10` 后，数组变为 `[1,2,5,7]`。`[1,2,5,7]` 是严格递增的，因此返回 `true`。

### 示例 2
**输入**: `nums = [2,3,1,2]`  
**输出**: `false`  
**解释**:  
- 移除下标 `0` 得到 `[3,1,2]`  
- 移除下标 `1` 得到 `[2,1,2]`  
- 移除下标 `2` 得到 `[2,3,2]`  
- 移除下标 `3` 得到 `[2,3,1]`  

上述所有结果均不是严格递增的，所以返回 `false`。

### 示例 3
**输入**: `nums = [1,1,1]`  
**输出**: `false`  
**解释**: 任意移除一个元素后得到的数组都是 `[1,1]`，而 `[1,1]` 并非严格递增，故返回 `false`。

## 约束条件
- `2 <= nums.length <= 1000`
- `1 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**要删掉的下标 `i`（`0 ≤ i < len(nums)`），把第 `i` 个元素暂时移除，然后检查剩下的数组是否是严格递增的。  

- **数据结构**：只需要用 **列表**（Python 中的 `list`）保存原数组，删除元素可以通过切片 `nums[:i] + nums[i+1:]` 得到一个新列表。  
- **为什么正确**：因为题目要求“恰好删除一个元素后数组是严格递增”，我们把每一种可能的删除方式都试一遍，只要有一种成功就返回 `True`，全部尝试完仍未成功则返回 `False`。  
- **复杂度分析**：  
  - 对每个下标 `i`（共 `n` 次）我们都要遍历一次剩余的数组来检查递增性，检查一次需要 `O(n)` 的时间。  
  - 所以总时间是 `O(n × n) = O(n²)`。  
  - 空间上我们每次都会生成一个长度为 `n‑1` 的新列表，最坏情况需要 `O(n)` 的额外空间（实际可以复用原列表，但这里为了代码简洁就直接生成新列表）。

> **大白话**：`O(n²)` 可以想象成“把每个人都和每个人比一次”，当 `n` 只有几百甚至几千时还能接受，但如果 `n` 很大（比如几万、几百万）就会非常慢。

#### 代码（Python）

```python
def check_strictly_increasing(arr: list[int]) -> bool:
    """返回 arr 是否严格递增（每个相邻元素满足前小后大）"""
    for i in range(1, len(arr)):
        if arr[i - 1] >= arr[i]:          # 只要出现不满足的情况就返回 False
            return False
    return True


def can_be_increasing_bruteforce(nums: list[int]) -> bool:
    n = len(nums)
    # 枚举要删除的下标 i
    for i in range(n):
        # 生成删除第 i 个元素后的新数组
        new_arr = nums[:i] + nums[i + 1:]
        # 检查新数组是否严格递增
        if check_strictly_increasing(new_arr):
            return True                 # 只要找到一种可行方案，立即返回 True
    return False                        # 所有方案都不行，返回 False
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每次尝试删除都要遍历一次剩余数组，`n` 次尝试 × `n` 长度 ≈ `n²`。  
- **空间复杂度**：`O(n)`  
  - `new_arr` 需要额外存放 `n‑1` 个元素的拷贝，最坏情况下占用线性空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历**：我们每次都重新检查整个数组，而实际上只需要一次遍历就能判断是否可以通过删除一个元素得到严格递增。  

1. **一次遍历找“违背点”**  
   - 当 `nums[i-1] >= nums[i]` 时，说明在下标 `i-1` 与 `i` 之间出现了不递增的情况。我们把这种情况记为 **违背点**。  
   - 如果违背点出现 **两次以上**，无论删哪个元素都不可能让整体严格递增，因为已经有两段不符合，删除一个元素只能修复其中一段。此时直接返回 `False`。

2. **只有 0 或 1 个违背点**  
   - **0 个**：数组本身已经严格递增，直接返回 `True`（题目允许“恰好删除一个元素”，即使不删也算满足条件）。  
   - **1 个**：设违背点的下标为 `i`（即 `nums[i-1] >= nums[i]`）。我们只能删除 `nums[i-1]` 或 `nums[i]` 中的一个。  
     - 删除 `nums[i-1]` 能否成功？需要检查 `nums[i-2] < nums[i]`（如果 `i-2` 存在）。因为删除 `i-1` 后，`i-2` 会直接和 `i` 相邻。  
     - 删除 `nums[i]` 能否成功？需要检查 `nums[i-1] < nums[i+1]`（如果 `i+1` 存在）。因为删除 `i` 后，`i-1` 会直接和 `i+1` 相邻。  
   - 只要上述两条检查中有一条成立，就可以通过删除对应的元素让数组严格递增。

3. **边界情况**  
   - 当违背点出现在数组开头（`i == 1`）或结尾（`i == n-1`）时，`i-2` 或 `i+1` 可能不存在，此时只需要检查另一侧即可，实际上删除任意一个都可以让剩下的序列保持递增。

> **核心概念——“前缀/后缀”**  
> 想象数组是一条道路，违背点是路口的坑。我们只能填平 **一个** 坑（删除一个元素），所以如果出现两个坑，就不可能一次修好全部道路。

#### 代码（Python）

```python
def can_be_increasing(nums: list[int]) -> bool:
    n = len(nums)
    cnt = 0               # 记录违背点的个数
    idx = -1              # 记录第一次违背点出现的位置

    # 第一次遍历：统计违背点
    for i in range(1, n):
        if nums[i - 1] >= nums[i]:   # 发现不递增的地方
            cnt += 1
            idx = i                  # 记录 i（后面的元素较小）
            if cnt > 1:              # 超过一个违背点直接返回 False
                return False

    # 没有违背点，已经严格递增
    if cnt == 0:
        return True

    # 只有一个违背点，检查能否通过删除一个元素解决
    # 下面的 i == idx，对应的是 nums[i-1] >= nums[i]
    i = idx
    # 情形 1：删除 nums[i-1]，需要前面的元素（若存在）小于 nums[i]
    cond1 = (i - 2 < 0) or (nums[i - 2] < nums[i])
    # 情形 2：删除 nums[i]，需要后面的元素（若存在）大于 nums[i-1]
    cond2 = (i + 1 >= n) or (nums[i - 1] < nums[i + 1])

    return cond1 or cond2
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，最多做常数次比较。相比暴力的 `O(n²)`，速度提升了一个数量级。  
- **空间复杂度**：`O(1)`  
  - 只使用了若干个整数变量，额外空间不随输入规模增长。

---

## 心得  

- **核心技巧**：一次遍历找出“不递增的点”，并利用**局部判断**（前后元素的关系）决定是否可以通过删除一个元素修复。  
- **适用的题型**：  
  1. “删除最多 k 个元素使数组严格递增”——可以把 `k` 设为 1 的思路推广到更大的 `k`（需要更复杂的 DP 或滑动窗口）。  
  2. “检查数组是否可以通过一次修改（而不是删除）变为严格递增”。  
  3. “最长严格递增子序列长度 ≥ n‑1”——等价于本题的另一种表述。  
- **一句话总结**：**只要数组中违背递增的地方不超过一次，并且那一次的前后元素能够“连通”，就可以删掉一个元素让整个数组递增。**

---

## 反思  

- **第一反应**：直接想到遍历每个下标、删掉后再检查——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忽略了边界（`i‑2`、`i+1` 可能不存在）导致索引错误。  
  - 只检查 `nums[i‑2] < nums[i]` 而忘记同时考虑 `nums[i‑1] < nums[i+1]`，会误判。  
  - 把“已经严格递增”误写成必须删除一个元素才能返回 `True`，实际上不删也算满足要求。  
- **下次遇到同类题**：第一步先**统计违背递增的次数**，如果超过允许的次数（本题是 1），直接返回 `False`；否则再**局部检查**能否通过一次删除/修改解决。这样可以把时间从二次降到一次。