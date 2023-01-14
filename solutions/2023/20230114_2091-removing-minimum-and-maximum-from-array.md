# #2091. 删除数组中的最小值和最大值 / Removing Minimum and Maximum From Array

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/removing-minimum-and-maximum-from-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of distinct integers nums.
There is an element in nums that has the lowest value and an element that has the highest value. We call them the minimum and maximum respectively. Your goal is to remove both these elements from the array.
A deletion is defined as either removing an element from the front of the array or removing an element from the back of the array.
Return the minimum number of deletions it would take to remove both the minimum and maximum element from the array.

**Examples**

**Example 1:**

```
Input: nums = [2,10,7,5,4,1,8,6]
Output: 5
Explanation: 
The minimum element in the array is nums[5], which is 1.
The maximum element in the array is nums[1], which is 10.
We can remove both the minimum and maximum by removing 2 elements from the front and 3 elements from the back.
This results in 2 + 3 = 5 deletions, which is the minimum number possible.
```

**Example 2:**

```
Input: nums = [0,-4,19,1,8,-2,-3,5]
Output: 3
Explanation: 
The minimum element in the array is nums[1], which is -4.
The maximum element in the array is nums[2], which is 19.
We can remove both the minimum and maximum by removing 3 elements from the front.
This results in only 3 deletions, which is the minimum number possible.
```

**Example 3:**

```
Input: nums = [101]
Output: 1
Explanation:  
There is only one element in the array, which makes it both the minimum and maximum element.
We can remove it with 1 deletion.
```

**Constraints**

- 1 <= nums.length <= 105
- -105 <= nums[i] <= 105
- The integers in nums are distinct.

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始、元素互不相同的整数数组 `nums`。  
数组中必然存在一个取值最小的元素和一个取值最大的元素，分别称为 **最小值**（minimum）和 **最大值**（maximum）。你的目标是将这两个元素都从数组中删除。

一次 **删除**（deletion）定义为：从数组的 **前端**（front）删除一个元素，或从数组的 **后端**（back）删除一个元素。

返回删除最小值和最大值所需的 **最少删除次数**（minimum number of deletions）。

**示例**

示例 1  
Input: `nums = [2,10,7,5,4,1,8,6]`  
Output: `5`  
Explanation:  
数组中的最小值是 `nums[5] = 1`，最大值是 `nums[1] = 10`。  
我们可以从前端删除 2 个元素，从后端删除 3 个元素，恰好把最小值和最大值都删掉。  
共计 `2 + 3 = 5` 次删除，这是可能的最少次数。

示例 2  
Input: `nums = [0,-4,19,1,8,-2,-3,5]`  
Output: `3`  
Explanation:  
最小值是 `nums[1] = -4`，最大值是 `nums[2] = 19`。  
只需从前端删除 3 个元素即可同时删掉最小值和最大值。  
因此只需 3 次删除，这是最小的可能值。

示例 3  
Input: `nums = [101]`  
Output: `1`  
Explanation:  
数组中只有一个元素，它既是最小值也是最大值。  
一次删除即可将其移除。

**约束条件**  

- `1 <= nums.length <= 10^5`  
- `-10^5 <= nums[i] <= 10^5`  
- `nums` 中的整数互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把所有可能的删除顺序都枚举一遍，找出最少的步数**。  
- 我们只能从数组的左端（前）或右端（后）删元素，每一次删除都会把数组长度减 1。  
- 于是可以把“从前删 k 次、从后删 m 次”这种组合全部尝试，检查在这些删除后，数组里是否已经把最小值和最大值都去掉了。  
- 具体实现可以使用两层循环：外层遍历前面删 k 个元素（`k` 从 0 到 n），内层遍历后面删 m 个元素（`m` 从 0 到 n‑k），每次判断剩下的子数组是否已经不含最小值和最大值。  

> **类比**：把数组想象成一本书，只有书的前面和后面可以撕页。暴力做法就是把每一种“先撕 k 页前面、再撕 m 页后面”的组合都试一遍，看看哪种最省力。  

**为什么正确**：  
只要遍历了所有合法的 (k,m) 组合，就一定能找到最少的那一种。因为题目只要求**最小的删除次数**，不在乎具体的删除顺序，只要能把最小值和最大值都删掉即可。

**时间/空间复杂度**：  
- 外层 k 有 n 种取值，内层 m 最多也有 n 种，最坏情况要检查 n·n ≈ n² 次。  
- 每次检查是否已经删除了最小/最大，只需要 O(1) 的比较（因为我们可以预先记下最小值和最大值的下标），所以总时间是 **O(n²)**。  
- 只用了常数级的额外变量（最小/最大下标、循环计数器），空间是 **O(1)**。  

> **大白话**：  
`O(n²)` 就像把 10 000 个苹果两两配对检查，需要 100 000 000 次操作，显然在 10⁵ 规模的数组里会太慢。

#### 代码（Python）  

```python
def min_deletions_bruteforce(nums):
    n = len(nums)
    # 先找出最小值和最大值的下标
    min_idx = nums.index(min(nums))
    max_idx = nums.index(max(nums))

    # 暴力枚举前删 k 次，后删 m 次
    best = n                     # 最坏情况就是全部删掉
    for k in range(n + 1):       # k 可以为 0~n
        for m in range(n - k + 1):   # m 不能超过剩余的长度
            # 删除前 k 个和后 m 个后，剩下的子数组是 nums[k:n-m]
            left = k
            right = n - m - 1
            # 判断子数组里是否还包含 min_idx 或 max_idx
            # 如果两者都不在子数组里，说明已经删掉了
            if not (left <= min_idx <= right) and not (left <= max_idx <= right):
                best = min(best, k + m)
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)` — 需要遍历所有可能的前删 k 和后删 m 组合，类似把 n 个元素两两配对检查。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正影响删除次数的只有最小值和最大值的位置**，其余元素的相对顺序并不重要。  
我们只需要考虑三种“删除策略”，因为每一次删除只能从两端进行，下面的三种已经覆盖了所有可能：

| 场景 | 说明 | 需要的删除次数 |
|------|------|----------------|
| 1️⃣ 只从前面删 | 两个目标都在数组左侧（靠前） | `max(min_idx, max_idx) + 1` |
| 2️⃣ 只从后面删 | 两个目标都在数组右侧（靠后） | `n - min(min_idx, max_idx)` |
| 3️⃣ 前后各删一次 | 一个在左边，一个在右边 | `min_idx + 1 + (n - max_idx)`（假设 `min_idx < max_idx`） |

**为什么这三种就够了？**  
- 删除只能从两端进行，**要把某个元素删掉，必须把它左边（或右边）所有的元素都删掉**。  
- 因此，若我们决定只用前端删除，就必须一直删到离它们最远的那个位置（即 `max(min_idx, max_idx)`），这正是场景 1。  
- 同理，只用后端删除则需要一直删到离它们最近后端的位置（即 `min(min_idx, max_idx)`），得到场景 2。  
- 若我们选择前后各删一次，那么必然是把左边的那个（下标更小的）从前端删掉，把右边的那个（下标更大的）从后端删掉，得到场景 3。  
- 这三种情况已经囊括了所有可能的最优方案，因为任何混合的删除顺序最终都会归结为“前删 k 次、后删 m 次”，而 `k` 与 `m` 的最小组合恰好是上表中的三种。

**关键点——前缀/后缀的概念**：  
- “从前删 k 次”相当于取数组的 **前缀**（前 k 个元素）。  
- “从后删 m 次”相当于取数组的 **后缀**（后 m 个元素）。  
- 只要前缀和后缀的并集覆盖了最小值和最大值所在的位置，就完成了任务。

**实现步骤**  

1. 扫描一次数组，记录最小值和最大值的下标 `min_idx`、`max_idx`。  
2. 为了统一处理，把下标排序，使 `left = min(min_idx, max_idx)`，`right = max(min_idx, max_idx)`。  
3. 计算三种场景的删除次数：  
   - `front = right + 1`  
   - `back = n - left`  
   - `both = left + 1 + (n - right)`  
4. 返回这三个数的最小值。  

**复杂度**：只遍历一次数组，时间 **O(n)**，额外空间只有几个整数，**O(1)**。

#### 代码（Python）  

```python
def min_deletions(nums):
    """
    返回最少的删除次数，使数组同时不含最小值和最大值。
    删除只能从数组的前端或后端进行。
    """
    n = len(nums)

    # 1. 找到最小值和最大值的下标
    min_idx = max_idx = 0
    for i, v in enumerate(nums):
        if v < nums[min_idx]:
            min_idx = i
        if v > nums[max_idx]:
            max_idx = i

    # 2. 把下标排个序，left 为左边的下标，right 为右边的下标
    left = min(min_idx, max_idx)
    right = max(min_idx, max_idx)

    # 3. 三种可能的删除方式
    #   - 只从前面删到 right（把两个元素都删掉）
    front = right + 1                     # 0-indexed，所以 +1 表示实际删除的个数
    #   - 只从后面删到 left
    back = n - left
    #   - 前后各删一次，左边从前删，右边从后删
    both = left + 1 + (n - right)

    # 4. 取最小值即为答案
    return min(front, back, both)
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只需要一次遍历找到最小/最大下标，后面的计算都是常数时间。  
  与暴力解的 `O(n²)` 相比，速度提升了 **n 倍**（比如 n=10⁵ 时，暴力需要 10¹⁰ 次操作，最优解只要 10⁵ 次）。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，不随输入规模增长。  

---

## 心得  

- **核心技巧**：**只关注最值的位置**，利用“只能从两端删除”这一限制，枚举三种极端策略。  
- **适用场景**：  
  1. “删除数组两端的元素，使满足某种条件”类题目（如 LeetCode 1658 `Minimum Operations to Reduce X to Zero`）。  
  2. “在数组中找最左/最右出现的特定元素，然后计算前缀或后缀长度”类题目（如 “最长子数组的和为 K” 的前缀哈希法变形）。  
- **一句话总结**：**把问题化简为只涉及最小值和最大值的下标，三种端点删除方案必有最优解。**

---

## 反思  

- **第一反应**：看到“只能从前或后删除”，自然想到“前缀+后缀”。于是先想到枚举所有前缀/后缀的组合（暴力），随后思考是否可以只看关键元素。  
- **最容易踩的坑**：  
  - 忘记把下标排序，导致 `left`、`right` 位置颠倒，计算 `both` 时会出错。  
  - 忽视数组长度为 1 的特殊情况；此时最小值和最大值是同一个元素，答案应该是 1。  
  - 计算 “只从后面删” 时的公式写成 `n - right`（错误），正确的是 `n - left`。  
- **下次类似题目第一步**：**先定位关键元素的下标（或位置），再利用题目给出的操作限制（只能从两端）枚举少数几种极端方案**。这样可以快速从 O(n²) 的暴力思路跳到 O(n) 的最优解。