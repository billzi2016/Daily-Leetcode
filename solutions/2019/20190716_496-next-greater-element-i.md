# #496. 下一个更大元素 I / Next Greater Element I

> 难度：简单 · 标签：Array、Hash Table、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/next-greater-element-i/)

---

## 题目（英文原版）

**Description**

The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.
You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.
For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.
Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.

**Examples**

**Example 1:**

```
Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
Output: [-1,3,-1]
Explanation: The next greater element for each value of nums1 is as follows:
- 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
- 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
- 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
```

**Example 2:**

```
Input: nums1 = [2,4], nums2 = [1,2,3,4]
Output: [3,-1]
Explanation: The next greater element for each value of nums1 is as follows:
- 2 is underlined in nums2 = [1,2,3,4]. The next greater element is 3.
- 4 is underlined in nums2 = [1,2,3,4]. There is no next greater element, so the answer is -1.
```

**Constraints**

- 1 <= nums1.length <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 104
- All integers in nums1 and nums2 are unique.
- All the integers of nums1 also appear in nums2.

---

## 题目（中文翻译）

**描述**  
数组中某个元素 `x` 的下一个更大元素（next greater element）是指在同一数组中 `x` 右侧出现的第一个大于 `x` 的元素。  
给定两个互不相同且下标从 0 开始的整数数组 `nums1` 和 `nums2`，其中 `nums1` 是 `nums2` 的子集。  
对于每个 `0 <= i < nums1.length`，找到下标 `j` 使得 `nums1[i] == nums2[j]`，并确定 `nums2[j]` 在 `nums2` 中的下一个更大元素。如果不存在下一个更大元素，则该查询的答案为 `-1`。  
返回长度为 `nums1.length` 的数组 `ans`，其中 `ans[i]` 即为上述定义的下一个更大元素。

**示例 1**  
```
输入: nums1 = [4,1,2], nums2 = [1,3,4,2]
输出: [-1,3,-1]
解释: nums1 中每个值对应的下一个更大元素如下:
- 4 在 nums2 = [1,3,4,2] 中被下划线标记。右侧没有更大的元素，所以答案是 -1。
- 1 在 nums2 = [1,3,4,2] 中被下划线标记。下一个更大元素是 3。
- 2 在 nums2 = [1,3,4,2] 中被下划线标记。右侧没有更大的元素，所以答案是 -1。
```

**示例 2**  
```
输入: nums1 = [2,4], nums2 = [1,2,3,4]
输出: [3,-1]
解释: nums1 中每个值对应的下一个更大元素如下:
- 2 在 nums2 = [1,2,3,4] 中被下划线标记。下一个更大元素是 3。
- 4 在 nums2 = [1,2,3,4] 中被下划线标记。右侧没有更大的元素，所以答案是 -1。
```

**约束条件**  
- `1 <= nums1.length <= nums2.length <= 1000`  
- `0 <= nums1[i], nums2[i] <= 10^4`  
- `nums1` 和 `nums2` 中的所有整数互不相同。  
- `nums1` 中的所有整数均出现在 `nums2` 中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：对 `nums1` 中的每一个数，去 `nums2` 里找它出现的位置 `j`，然后从 `j+1` 开始往右扫描，遇到第一个比它大的数就把它记下来。如果一直扫描到数组末尾都没有比它大的，就返回 `-1`。

- **用到的数据结构**：  
  - **数组**：我们只需要顺序访问元素，数组就像一本排好序的相册，左到右依次翻页。  
  - **哈希表（可选）**：如果想把“找位置”这一步加速，可以先把 `nums2` 的每个数及其下标存进哈希表，查找就像在字典里找单词的页码，`O(1)` 时间。

- **为什么正确**：  
  对每个 `nums1[i]`，我们在 `nums2` 中找到了它真实出现的位置 `j`。从 `j+1` 开始的每个元素都是它右边的候选，按照顺序检查，第一个满足“大于”条件的，就是题目要求的 **最近的更大元素**。如果没有，则答案只能是 `-1`。

- **时间/空间复杂度**：  
  - 暴力扫描每个查询时，最坏情况要遍历 `nums2` 的剩余部分。设 `m = len(nums1)`, `n = len(nums2)`，则时间复杂度是 `O(m·n)`。  
    - 大白话：如果 `nums1` 有 100 个数，`nums2` 长 1000，最坏情况下我们要做 100 × 1000 = 10⁵ 次比较。  
  - 只用了常数级别的额外空间（哈希表可以省掉），所以空间复杂度是 `O(1)`（不计输入本身）。

#### 代码（Python）

```python
from typing import List

def next_greater_element_brute(nums1: List[int], nums2: List[int]) -> List[int]:
    res = []                       # 最终答案列表
    for x in nums1:                # 对 nums1 中的每个元素逐个处理
        # 1️⃣ 找到 x 在 nums2 中的下标
        idx = nums2.index(x)       # list.index 会线性搜索，最坏 O(n)
        # 2️⃣ 从 idx+1 开始向右找第一个更大的数
        next_greater = -1          # 默认答案是 -1
        for y in nums2[idx + 1:]: # 逐个检查右侧的元素
            if y > x:              # 第一个比 x 大的就是答案
                next_greater = y
                break
        res.append(next_greater)   # 把答案放进结果数组
    return res
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - `m` 是 `nums1` 的长度，`n` 是 `nums2` 的长度。每次要先 `index`（最坏 `O(n)`），再遍历右侧子数组（最坏 `O(n)`），所以总体是 `O(m·n)`。
- **空间复杂度**：`O(1)`（不计输出数组）  
  - 只用了几个临时变量，额外空间几乎为常数。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于对每个查询都要重新向右扫描，这导致大量重复工作。实际上，`nums2` 中每个位置的「下一个更大元素」只需要算一次，后面所有查询都可以直接查表得到。

**核心技巧：单调栈（Monotonic Stack）**  
- **单调栈**是一种只保存「递增」或「递减」顺序元素的栈。这里我们维护一个 **递减栈**（栈顶最小），从左到右遍历 `nums2`：
  1. 当前元素 `cur` 与栈顶元素 `top` 比较。  
  2. 如果 `cur > top`，说明 `cur` 是 `top` 的「下一个更大元素」，把 `cur` 记下来，弹出 `top`。  
  3. 继续比较，直到栈为空或栈顶大于等于 `cur`。  
  4. 把 `cur` 入栈，等待后面的更大元素来「救它」。
- 通过一次遍历（`O(n)`），我们可以得到 `nums2` 中每个数对应的「下一个更大」值，保存到哈希表 `next_greater`（相当于「词典」），键是数本身，值是它的答案（若没有则为 `-1`）。

**为什么单调栈能一次搞定**  
- 栈里保存的都是「还没有找到更大元素」的数，而且它们的顺序是从左到右、从大到小（递减）。当出现一个更大的数时，它一定是栈中所有比它小的数的最近更大元素，因为比它小的数在它左边，且在它出现之前没有更大的数出现过。

**步骤**  
1. 初始化空栈 `stack=[]`，空哈希表 `next_greater={}`。  
2. 遍历 `nums2` 中的每个数 `x`：  
   - 当栈不空且 `x > stack[-1]` 时，弹出栈顶 `prev`，并把 `next_greater[prev] = x`。  
   - 重复上述步骤直到不满足条件。  
   - 把 `x` 入栈 `stack.append(x)`。  
3. 遍历结束后，栈中剩余的元素没有更大的数，默认答案 `-1`（可以在哈希表里统一设为 `-1`）。  
4. 最后，对 `nums1` 按顺序查表得到答案。

**类比**：把栈想象成一列排队的孩子，身高从前往后递减。当一个新来的孩子比队尾的孩子高时，队尾的孩子可以立刻看到更高的孩子（就是他的「下一个更大」），于是离开队列。这样每个孩子只会离开一次，整体过程只走一遍。

#### 代码（Python）

```python
from typing import List

def next_greater_element(nums1: List[int], nums2: List[int]) -> List[int]:
    # 1️⃣ 预处理：用单调栈算出 nums2 中每个数的下一个更大元素
    stack: List[int] = []                 # 递减栈，保存还没找到答案的数
    next_greater: dict[int, int] = {}     # 哈希表：数 -> 下一个更大数（若无则为 -1）

    for x in nums2:                       # 从左到右遍历 nums2
        # 栈顶元素如果比当前 x 小，说明 x 是它的下一个更大元素
        while stack and x > stack[-1]:
            prev = stack.pop()            # 把栈顶弹出
            next_greater[prev] = x        # 记录答案
        stack.append(x)                  # 当前元素入栈，等待更大的数来救它

    # 栈里剩下的元素没有更大的数，统一设为 -1
    while stack:
        prev = stack.pop()
        next_greater[prev] = -1

    # 2️⃣ 根据哈希表直接得到 nums1 的答案
    return [next_greater[num] for num in nums1]
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - `n = len(nums2)`：单调栈遍历一次，每个元素最多进栈一次、出栈一次，合计 `O(n)`。  
  - `m = len(nums1)`：查表是 `O(1)`，遍历 `nums1` 需要 `O(m)`。  
  - 相比暴力的 `O(m·n)`，这里把重复扫描全部消掉了，速度提升显著。

- **空间复杂度**：`O(n)`  
  - 哈希表 `next_greater` 存储了 `nums2` 中每个数的答案，需要 `O(n)` 的额外空间。  
  - 栈的最大长度也不会超过 `n`，所以整体仍是 `O(n)`。

---

## 心得

- **核心技巧**：单调栈（Monotonic Stack）用于「下一个更大/更小」这类一次性求解的场景。  
- **适用题型**：  
  1. **Next Greater Element II**（环形数组版）  
  2. **Daily Temperatures**（每日温度）  
  3. **Largest Rectangle in Histogram**（柱状图中最大矩形）  
- **一句话总结**：一次遍历，用递减栈把「谁还在等更大的」记录下来，查询时直接查表即可。

## 反思

- **第一反应**：看到「下一个更大」会立刻想到「暴力向右扫描」——最直观但慢。  
- **最容易踩的坑**：  
  - 忘记处理栈中剩余元素的情况，导致未赋值的键返回 `KeyError`。  
  - 把「下一个更大」误写成「所有更大的」或「左侧更大」——要明确是「右侧第一个更大的」才对。  
- **下次遇到同类题**：先问自己「每个位置的答案只需要算一次吗？」如果是，立刻想到使用 **单调栈** 或 **前缀/后缀** 结构来一次完成。