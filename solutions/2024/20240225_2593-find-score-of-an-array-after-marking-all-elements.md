# #2593. **标记所有元素后的数组得分** / Find Score of an Array After Marking All Elements

> 难度：中等 · 标签：Array、Hash Table、Sorting、Heap (Priority Queue)、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-score-of-an-array-after-marking-all-elements/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of positive integers.
Starting with score = 0, apply the following algorithm:
Return the score you get after applying the above algorithm.

**Examples**

**Example 1:**

```
Input: nums = [2,1,3,4,5,2]
Output: 7
Explanation: We mark the elements as follows:
- 1 is the smallest unmarked element, so we mark it and its two adjacent elements: [2,1,3,4,5,2].
- 2 is the smallest unmarked element, so we mark it and its left adjacent element: [2,1,3,4,5,2].
- 4 is the only remaining unmarked element, so we mark it: [2,1,3,4,5,2].
Our score is 1 + 2 + 4 = 7.
```

**Example 2:**

```
Input: nums = [2,3,5,1,3,2]
Output: 5
Explanation: We mark the elements as follows:
- 1 is the smallest unmarked element, so we mark it and its two adjacent elements: [2,3,5,1,3,2].
- 2 is the smallest unmarked element, since there are two of them, we choose the left-most one, so we mark the one at index 0 and its right adjacent element: [2,3,5,1,3,2].
- 2 is the only remaining unmarked element, so we mark it: [2,3,5,1,3,2].
Our score is 1 + 2 + 2 = 5.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个只包含正整数的数组 `nums`。  
从 `score = 0` 开始，重复执行以下步骤，直到数组中所有元素都被标记为止：

1. 在当前未标记的元素中找到数值最小的元素；若存在多个相同的最小值，选择下标最左侧的那个。  
2. 将该元素标记，并将其左侧相邻的未标记元素（若存在）也标记，将其右侧相邻的未标记元素（若存在）也标记。  
3. 将该元素的数值加入 `score` 中。

返回最终得到的 `score`。

---

### 示例

**示例 1**

```text
输入: nums = [2,1,3,4,5,2]
输出: 7
解释:
- 1 是当前最小的未标记元素，标记它及其左右相邻的元素（下标 0、1、2）。
- 2 是剩余未标记元素中最小的（下标 5），标记它及其左侧相邻的未标记元素（下标 4）。
- 4 是唯一剩余的未标记元素，标记它。
得分为 1 + 2 + 4 = 7。
```

**示例 2**

```text
输入: nums = [2,3,5,1,3,2]
输出: 5
解释:
- 1 是当前最小的未标记元素，标记它及其左右相邻的元素（下标 2、3、4）。
- 2 是剩余未标记元素中最小的，出现两次，选择左侧的下标 0，标记它及其右侧相邻的未标记元素（下标 1）。
- 2 是唯一剩余的未标记元素，标记它。
得分为 1 + 2 + 2 = 5。
```

---

### 约束

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **一次一次地模拟题目描述的过程**：

1. 在当前还没有被标记的元素中，找出最小的那个（如果有相同的最小值，取最左边的下标）。  
2. 把它的值加入 `score`。  
3. 把它本身以及它左边、右边（如果存在）的元素全部标记为 “已标记”。  
4. 重复以上步骤，直到所有元素都被标记。

这里用到的唯一数据结构是一个长度为 `n` 的布尔数组 `marked`，用来记录每个位置是否已经被标记。可以把它想象成 **一本笔记本**，每翻一页（对应数组的一个下标），在页眉写下 “✔” 表示这页已经看过了。

> **为什么这个方法一定能得到正确答案？**  
> 题目要求“每一步都选当前未标记的最小元素”，只要我们每一步都严格遵守这条规则，并且在选完后把相邻的元素也标记，最终的 `score` 就必然等于题目要求的分数。

> **时间/空间复杂度大白话**  
> - **时间复杂度** `O(n²)`：假设数组长度为 `n`，每一次循环我们都要遍历整条数组去找最小的未标记元素，最坏情况下会进行 `n` 次循环，所以大概要做 `n × n` 次比较，称为 “平方级”。  
> - **空间复杂度** `O(n)`：只多用了一个和原数组等长的 `marked` 布尔数组，用来记住哪些位置已经被标记。

#### 代码（Python）

```python
def findScore(nums):
    n = len(nums)
    marked = [False] * n          # 记录每个位置是否已经被标记
    score = 0

    # 只要还有未标记的元素，就一直循环
    while not all(marked):
        # 1️⃣ 找最小的未标记元素（左侧优先）
        min_val = float('inf')
        min_idx = -1
        for i in range(n):
            if not marked[i] and nums[i] < min_val:
                min_val = nums[i]
                min_idx = i

        # 2️⃣ 加分
        score += min_val

        # 3️⃣ 标记自身和左右相邻的元素
        marked[min_idx] = True
        if min_idx - 1 >= 0:          # 左边界存在时标记左邻居
            marked[min_idx - 1] = True
        if min_idx + 1 < n:           # 右边界存在时标记右邻居
            marked[min_idx + 1] = True

    return score
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 每轮遍历整个数组找最小值，最坏会进行 `n` 轮。  
- **空间复杂度**：`O(n)` —— 额外的 `marked` 数组占用线性空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每一步都要线性扫描整个数组**找最小未标记元素，这导致整体是平方级时间。我们需要一种能够 **快速得到当前未标记的最小元素** 的方式。

思考过程如下：

1. **把所有元素一次性准备好**  
   - 如果我们把每个元素的 `(值, 下标)` 放进一个容器，并且按照 **值从小到大、值相同则下标从左到右** 排序，那么遍历这个容器的顺序正好就是题目要求的“每一步挑最小且左侧优先”。  
   - 排序一次 `O(n log n)`，之后只需要顺序遍历，无需再次搜索。

2. **遍历已排好序的列表**  
   - 维护同样的 `marked` 布尔数组。  
   - 对于排好序的第 `i` 个元素 `(val, idx)`，如果它已经被标记（可能是之前相邻的更小元素把它标记了），我们直接跳过。  
   - 否则，它就是当前 **最小未标记** 的元素，按题目规则把 `val` 加到 `score`，并把 `idx`、`idx-1`、`idx+1` 标记。

3. **为什么只遍历一次就够了？**  
   - 因为排序已经把所有可能的“最小未标记”出现的顺序排好了。后面出现的元素的值一定 **不小于** 前面已经处理过的值。  
   - 当我们跳过已经标记的元素时，说明它已经被更小的元素的相邻标记覆盖了，根本不可能再成为 “最小未标记”。  

> **核心数据结构：排序 + 布尔数组**  
> - **排序** 好比把所有水果（元素）先按重量（数值）从轻到重排好，重量相同的按摆放顺序（下标）从左到右。这样我们每次只需要从左往右挑最轻的未挑过的水果。  
> - **布尔数组** 就是记录哪些水果已经被挑走或已经被邻近的更轻水果“抢走”。

> **时间复杂度直观解释**  
> - 排序需要 `O(n log n)`，这是一种“先把东西排好队，再一个个处理”的思路，常见于需要多次快速找最小/最大的场景。  
> - 排序以后我们只遍历一次数组，每个元素最多检查一次，时间是 `O(n)`，所以整体仍是 `O(n log n)`。  
> - 与暴力的 `n²`（比如 `100,000` 要做 `10,000,000,000` 次比较）相比，`n log n`（约 `1,700,000` 次比较）快了好几个数量级。

#### 代码（Python）

```python
def findScore(nums):
    n = len(nums)
    # 1️⃣ 把 (值, 下标) 收集起来，并按值升序、下标升序排序
    #   相当于把所有元素排好队，最左边的最轻的先出来
    order = sorted(((val, idx) for idx, val in enumerate(nums)), key=lambda x: (x[0], x[1]))

    marked = [False] * n          # 同样的标记数组
    score = 0

    # 2️⃣ 按排好序的顺序遍历
    for val, idx in order:
        if marked[idx]:           # 已经被更小的元素的相邻标记了，直接跳过
            continue

        # 3️⃣ 这是当前最小未标记的元素，按题意加分并标记自身和左右
        score += val
        marked[idx] = True
        if idx - 1 >= 0:
            marked[idx - 1] = True
        if idx + 1 < n:
            marked[idx + 1] = True

    return score
```

#### 复杂度

- **时间复杂度**：`O(n log n)` — 主要来源于一次排序（`log n` 是对数，想象成把 `n` 本书分层归档的过程）。遍历本身是线性的 `O(n)`，不影响整体阶数。与暴力的 `O(n²)` 相比，提升显著。  
- **空间复杂度**：`O(n)` — 需要额外的 `order` 列表存放 `(值, 下标)`，以及 `marked` 布尔数组，都是线性空间。

---

## 心得

- **核心技巧**：先把所有候选元素按照“值‑下标”排序，利用一次线性遍历模拟“每次取当前最小未标记元素”的过程。  
- **适用场景**：  
  1. 需要**多次取最小（或最大）未处理元素**，且“已处理”会影响相邻元素的状态。  
  2. “最小‑左侧优先”这种严格的顺序可以在**排序**后一次遍历完成。  
  3. 典型类似题目：  
     - *“Array Elimination”*（每次删除最小元素并影响邻居）  
     - *“Maximum Points You Can Obtain from Cards”*（需要按顺序挑选）  
- **一句话总结解题钥匙**：**“先排好队，再顺序检查”**——把所有可能的最小选择预排好序，遍历时只需判断是否已被前面的更小选择覆盖。

---

## 反思

- **拿到题目第一反应**：想到“每次都要找最小未标记的元素”，于是直接写了循环里遍历全数组的暴力实现。  
- **最容易踩的坑**  
  1. **左侧优先**：当有相同值出现时，一定要选最左边的下标，排序时要把下标也作为次要键。  
  2. **边界检查**：标记左右相邻时要判断下标是否越界，否则会出现 `IndexError`。  
  3. **已标记元素的跳过**：相邻的更小元素可能已经把当前元素标记了，忘记 `if marked[idx]: continue` 会导致重复计分。  
- **下次遇到同类题的第一步**：**先判断是否可以把“每次最小未处理”转化为一次性排序**，如果可以，就用“排序 + 线性遍历”来避免每轮的线性搜索。这样常常能把 `O(n²)` 降到 `O(n log n)`，甚至 `O(n)`。