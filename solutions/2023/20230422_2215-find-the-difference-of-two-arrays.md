# #2215. 找出两个数组的差异 / Find the Difference of Two Arrays

> 难度：简单 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/find-the-difference-of-two-arrays/)

---

## 题目（英文原版）

**Description**

Given two 0-indexed integer arrays nums1 and nums2, return a list answer of size 2 where:
Note that the integers in the lists may be returned in any order.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3], nums2 = [2,4,6]
Output: [[1,3],[4,6]]
Explanation:
For nums1, nums1[1] = 2 is present at index 0 of nums2, whereas nums1[0] = 1 and nums1[2] = 3 are not present in nums2. Therefore, answer[0] = [1,3].
For nums2, nums2[0] = 2 is present at index 1 of nums1, whereas nums2[1] = 4 and nums2[2] = 6 are not present in nums1. Therefore, answer[1] = [4,6].
```

**Example 2:**

```
Input: nums1 = [1,2,3,3], nums2 = [1,1,2,2]
Output: [[3],[]]
Explanation:
For nums1, nums1[2] and nums1[3] are not present in nums2. Since nums1[2] == nums1[3], their value is only included once and answer[0] = [3].
Every integer in nums2 is present in nums1. Therefore, answer[1] = [].
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 1000
- -1000 <= nums1[i], nums2[i] <= 1000

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的整数数组（integer array）`nums1` 和 `nums2`，返回一个大小为 **2** 的列表（list）`answer`，其中：

- `answer[0]` 为只出现在 `nums1` 中而不出现在 `nums2` 的 **不同** 整数集合（去重后）。
- `answer[1]` 为只出现在 `nums2` 中而不出现在 `nums1` 的 **不同** 整数集合（去重后）。

返回的每个子列表中的整数顺序可以任意。

**示例 1**  
输入: `nums1 = [1,2,3]`, `nums2 = [2,4,6]`  
输出: `[[1,3],[4,6]]`  
解释:  
- 对于 `nums1`，`nums1[1] = 2` 在 `nums2` 的下标 0 处出现，而 `nums1[0] = 1` 和 `nums1[2] = 3` 未出现在 `nums2` 中。因此 `answer[0] = [1,3]`。  
- 对于 `nums2`，`nums2[0] = 2` 在 `nums1` 的下标 1 处出现，而 `nums2[1] = 4` 和 `nums2[2] = 6` 未出现在 `nums1` 中。因此 `answer[1] = [4,6]`。

**示例 2**  
输入: `nums1 = [1,2,3,3]`, `nums2 = [1,1,2,2]`  
输出: `[[3],[]]`  
解释:  
- 对于 `nums1`，`nums1[2]` 和 `nums1[3]` 在 `nums2` 中不存在。由于它们的值相同，只保留一次，`answer[0] = [3]`。  
- `nums2` 中的每个整数都在 `nums1` 中出现过，所以 `answer[1] = []`。

**约束条件**  
- `1 <= nums1.length, nums2.length <= 1000`  
- `-1000 <= nums1[i], nums2[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是「一个一个地比较」：

1. 对 `nums1` 中的每个整数，去 `nums2` 里逐个查找，看它是否出现过。  
2. 同理，对 `nums2` 中的每个整数，去 `nums1` 里逐个查找。  

这里用到的唯一数据结构是 **列表**（list），相当于我们把所有数字排成一排，然后用手指一个一个地去摸。  
如果在另一边的列表里找不到，就把这个数字记下来。  

因为题目要求「每个整数只出现一次」的结果，我们在把数字放进答案时需要先检查答案里有没有已经有这个数字，防止重复加入。  

**为什么正确**：只要把每个元素都和另一数组的所有元素比较一次，就一定能判断出它是否存在于另一数组中，从而得到准确的差集。

**复杂度分析**（大白话版）：

- **时间复杂度**：  
  - 对 `nums1` 的每个元素，都要在 `nums2` 里遍历一次。设 `n = len(nums1)`, `m = len(nums2)`，总共要做 `n × m` 次比较。用 **O(n·m)** 表示。  
  - 举个例子，如果两个数组各有 1000 个元素，最坏情况要比较 1,000,000 次，这就是 O(n²)（因为 n≈m）。
- **空间复杂度**：  
  - 只用了几个额外的列表来存放答案和临时判断，和输入规模无关，用 **O(1)**（常数）表示。

#### 代码（Python）

```python
def findDifference(nums1, nums2):
    # answer[0] 用来存放只在 nums1 出现的数
    # answer[1] 用来存放只在 nums2 出现的数
    answer = [[], []]

    # -------- 处理 nums1 ----------
    for x in nums1:                     # 把 nums1 的每个数拿出来
        # 先检查 x 是否已经加入 answer[0]，防止重复
        if x in answer[0]:
            continue
        # 在 nums2 里逐个查找是否存在 x
        found = False
        for y in nums2:
            if x == y:
                found = True
                break
        # 如果在 nums2 里没有找到，就把 x 加进 answer[0]
        if not found:
            answer[0].append(x)

    # -------- 处理 nums2 ----------
    for x in nums2:
        if x in answer[1]:
            continue
        found = False
        for y in nums1:
            if x == y:
                found = True
                break
        if not found:
            answer[1].append(x)

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n·m)` — 需要把每个元素和另一数组的所有元素比较一次。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（答案列表的大小不算在额外空间里）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于「在另一数组里逐个查找」**。  
如果我们能把「是否出现」的查询从线性搜索变成 **常数时间**，整体速度就会快很多。

**哈希表（在 Python 中用 `set` 实现）** 正好可以做到这一点：

- 把 `nums1` 的所有不同元素放进一个集合 `set1`，以后想判断一个数是否在 `nums1` 里，只要检查它是否是 `set1` 的成员，时间是 O(1)。
- 同理，把 `nums2` 放进 `set2`。

这样：

1. 遍历 `set1`，把不在 `set2` 里的元素放进 `answer[0]`。  
2. 再遍历 `set2`，把不在 `set1` 里的元素放进 `answer[1]`。

**为什么正确**：集合本身已经把相同的数字合并（去重），所以遍历集合时每个数字只会出现一次；成员检查 O(1) 能保证我们准确判断「是否在另一数组里」。

**类比**：  
- 把集合想象成一本「电话簿」，每个号码只出现一次，查找某个号码是否在电话簿里，只需要翻到对应的页码（哈希函数直接定位），不需要一本一本地翻。

**复杂度分析**（大白话）：

- **时间复杂度**：  
  - 把两个数组各转成集合各需要 O(n) + O(m)。  
  - 再各遍历一次集合，检查成员关系也是 O(n) + O(m)。  
  - 总体是 **O(n + m)**，线性时间，远快于暴力的 O(n·m)。
- **空间复杂度**：  
  - 需要额外的两个集合，各保存不重复的元素，最坏情况下会和原数组一样多，故为 **O(n + m)**。

#### 代码（Python）

```python
def findDifference(nums1, nums2):
    """
    返回 [[只在 nums1 出现的数], [只在 nums2 出现的数]]
    使用集合（set）实现 O(n+m) 的解法
    """
    # 把两个数组去重后放进集合
    set1 = set(nums1)          # 类似“字典”里的词条，只保留唯一的数字
    set2 = set(nums2)

    # 只在 nums1 出现的数 = set1 中不在 set2 的元素
    only_in_nums1 = [x for x in set1 if x not in set2]

    # 只在 nums2 出现的数 = set2 中不在 set1 的元素
    only_in_nums2 = [x for x in set2 if x not in set1]

    return [only_in_nums1, only_in_nums2]
```

#### 复杂度

- **时间复杂度**：`O(n + m)` — 只需要线性遍历两遍，查找操作是常数时间。相比暴力解快了很多。
- **空间复杂度**：`O(n + m)` — 额外用了两个集合来存放去重后的元素。

---

## 心得

- **核心技巧**：利用哈希集合（`set`）实现「快速成员查询」与「去重」。
- **适用的题型**  
  1. 两个数组的交集、并集、差集（如 LeetCode 349、Intersection of Two Arrays II）。  
  2. 判断数组中是否存在重复元素（如 LeetCode 217）。
- **解题钥匙**：**“能不能把‘是否出现’的检查从遍历改成 O(1)？”**——如果可以，往哈希表/集合方向想。

---

## 反思

- **第一反应**：直接把每个数和另一数组的每个数比较，写成两层循环——这是最自然的暴力思路。
- **最容易踩的坑**  
  - 忘记去重：题目要求答案里每个整数只能出现一次，需要在加入答案前去重，集合天然可以帮忙。  
  - 边界情况：空数组或所有元素都相同的情况，使用集合后仍能正确返回空列表。  
- **下次类似题的第一步**：先问自己「这道题需要判断“是否在””，如果是，就立刻考虑 **集合 / 哈希表**，把查询时间从 O(n) 降到 O(1)。