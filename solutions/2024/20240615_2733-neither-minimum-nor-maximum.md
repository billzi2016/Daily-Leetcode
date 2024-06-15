# #2733. 既非最小值也非最大值 / Neither Minimum nor Maximum

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/neither-minimum-nor-maximum/)

---

## 题目（英文原版）

**Description**

Given an integer array nums containing distinct positive integers, find and return any number from the array that is neither the minimum nor the maximum value in the array, or -1 if there is no such number.
Return the selected integer.

**Examples**

**Example 1:**

```
Input: nums = [3,2,1,4]
Output: 2
Explanation: In this example, the minimum value is 1 and the maximum value is 4. Therefore, either 2 or 3 can be valid answers.
```

**Example 2:**

```
Input: nums = [1,2]
Output: -1
Explanation: Since there is no number in nums that is neither the maximum nor the minimum, we cannot select a number that satisfies the given condition. Therefore, there is no answer.
```

**Example 3:**

```
Input: nums = [2,1,3]
Output: 2
Explanation: Since 2 is neither the maximum nor the minimum value in nums, it is the only valid answer.
```

**Constraints**

- 1 <= nums.length <= 100
- 1 <= nums[i] <= 100
- All values in nums are distinct

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其中包含互不相同的正整数，找到并返回数组中**既不是最小值也不是最大值**的任意一个元素。如果不存在这样的元素，则返回 `-1`。  
返回选中的整数。

### 示例

**示例 1**  
**输入**: `nums = [3,2,1,4]`  
**输出**: `2`  
**解释**: 在该示例中，最小值为 `1`，最大值为 `4`。因此，`2` 或 `3` 都可以作为合法答案。

**示例 2**  
**输入**: `nums = [1,2]`  
**输出**: `-1`  
**解释**: 数组中没有既不是最大值也不是最小值的数字，无法选出满足条件的元素，所以返回 `-1`。

**示例 3**  
**输入**: `nums = [2,1,3]`  
**输出**: `2`  
**解释**: `2` 既不是数组的最大值也不是最小值，是唯一符合条件的答案。

### 约束条件

- `1 <= nums.length <= 100`
- `1 <= nums[i] <= 100`
- `nums` 中的所有值互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：先把数组里最小的数和最大的数找出来，然后再遍历一次数组，挑出第一个既不是最小也不是最大的数返回。  

- **数据结构**：我们只需要普通的 Python 列表（list），不需要额外的结构。  
- **生活化类比**：把数组想象成一排学生的身高，先找出最高的同学和最矮的同学（这一步像在字典里查“最高”“最矮”，只用两个变量记录），再从左到右看谁既不是最高也不是最矮，谁就是答案。  
- **为什么正确**：题目要求返回**任意**一个既不是最小也不是最大的位置上的数，只要我们找到了最小值 `min_val`、最大值 `max_val`，再找出一个既不等于它们的数，就一定满足条件。若数组长度小于 3，则不可能出现既不是最小也不是最大的位置，直接返回 `-1`。

#### 代码（Python）

```python
def findNonMinOrMax(nums):
    """
    暴力解法：先找最小、最大，再找第一个既不是最小也不是最大的位置
    """
    n = len(nums)
    # 长度不足 3，必然没有既非最小也非最大的位置
    if n < 3:
        return -1

    # 第一步：遍历一次找出最小值和最大值
    min_val = nums[0]      # 假设第一个是最小的
    max_val = nums[0]      # 假设第一个是最大的
    for x in nums:
        if x < min_val:
            min_val = x    # 更新最小值
        if x > max_val:
            max_val = x    # 更新最大值

    # 第二步：再遍历一次，找第一个既不是最小也不是最大
    for x in nums:
        if x != min_val and x != max_val:
            return x        # 找到答案直接返回

    # 如果循环结束仍未返回，说明所有数要么是最小要么是最大
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历找最小、最大是 `O(n)`，第二次遍历找答案也是 `O(n)`，两次相加仍然是线性时间。  
  - 用大白话说，就是如果数组有 100 个数，我们大概最多检查 200 次，这在实际运行中几乎和检查 100 次差不多，因为常数因素不算大。

- **空间复杂度**：`O(1)`  
  - 只用了几个额外的变量 `min_val、max_val、n`，不随数组长度增长而增加。

---

### 2. 最优解

#### 思路  
上面的“暴力”解已经是线性时间 `O(n)`，已经是最优的时间复杂度。  
如果有人把数组先排序再取中间的数，那时间会变成 `O(n log n)`，因为排序本身比一次遍历要慢。  
所以这里的“最优解”其实是**改进暴力解的实现细节**：我们可以在 **一次遍历** 中同时得到最小值、最大值以及第一个既不是最小也不是最大的位置，从而省去第二次遍历。

实现思路：

1. **一次遍历**  
   - 用 `min_val`、`max_val` 记录当前看到的最小、最大。  
   - 同时维护一个变量 `candidate`，记录当前看到的第一个既不是最小也不是最大（相对已知的 `min_val`、`max_val`）的数。  
2. **遍历结束后**  
   - 如果 `candidate` 仍然是 `None`，说明没有符合条件的数，返回 `-1`。  
   - 否则返回 `candidate`。

注意：因为在遍历过程中 `min_val`、`max_val` 会不断变化，`candidate` 可能会在后面被否定（比如之前以为它不是最小，但后来发现更小的数出现了），所以我们在遍历结束后需要再检查一次 `candidate` 是否仍然既不是最终的 `min_val` 也不是 `max_val`。

#### 代码（Python）

```python
def findNonMinOrMax(nums):
    """
    最优解：一次遍历同时得到最小值、最大值以及候选答案
    """
    n = len(nums)
    if n < 3:
        return -1

    # 初始化最小、最大为第一个元素
    min_val = max_val = nums[0]
    candidate = None   # 暂存可能的答案

    for x in nums:
        # 更新最小值和最大值
        if x < min_val:
            min_val = x
        elif x > max_val:
            max_val = x

        # 若当前数既不等于已知的最小也不等于已知的最大，尝试保存为候选
        if x != min_val and x != max_val:
            candidate = x

    # 遍历结束后，再确认 candidate 是否真的既不是全局最小也不是全局最大
    if candidate is not None and candidate != min_val and candidate != max_val:
        return candidate
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次数组。比两次遍历的暴力实现少了一次循环的常数因子，在大数据量时稍微快一点。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量。

---

## 心得

- **核心技巧**：一次遍历同时维护最值（最小、最大）以及候选答案，属于**最值维护**的典型思路。  
- **适用的题型**：  
  1. “找数组中第二大/第二小的数”。  
  2. “判断数组中是否存在既不是最小也不是最大的数”。  
  3. “在一次遍历中同时找出最大子段和最小子段”。  
- **一句话总结**：**“遍历中同步更新最小、最大，并随时记录非极值的候选”。**

---

## 反思

- **第一反应**：先把数组排序，然后直接取中间的数。虽然直观，但忘记了排序的时间开销。  
- **最容易踩的坑**：  
  - **数组长度不足 3** 时忘记直接返回 `-1`。  
  - 在一次遍历的实现里，`candidate` 可能在后面被新的最小/最大否定，需要在遍历结束后再次验证。  
- **下次遇到同类题**：第一步先**思考是否能在一次遍历中得到所有需要的信息**，而不是先做额外的排序或额外的数据结构。这样往往能得到最优的 `O(n)` 解法。