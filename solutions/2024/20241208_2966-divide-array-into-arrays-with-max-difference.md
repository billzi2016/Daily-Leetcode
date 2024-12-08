# #2966. 将数组划分为满足最大差值的子数组 / Divide Array Into Arrays With Max Difference

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/divide-array-into-arrays-with-max-difference/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of size n where n is a multiple of 3 and a positive integer k.
Divide the array nums into n / 3 arrays of size 3 satisfying the following condition:
Return a 2D array containing the arrays. If it is impossible to satisfy the conditions, return an empty array. And if there are multiple answers, return any of them.

**Examples**

**Example 1:**

```
Input: nums = [1,3,4,8,7,9,3,5,1], k = 2
Output: [[1,1,3],[3,4,5],[7,8,9]]
Explanation:
The difference between any two elements in each array is less than or equal to 2.
```

**Example 2:**

```
Input: nums = [2,4,2,2,5,2], k = 2
Output: []
Explanation:
Different ways to divide nums into 2 arrays of size 3 are:
Because there are four 2s there will be an array with the elements 2 and 5 no matter how we divide it. since 5 - 2 = 3 > k , the condition is not satisfied and so there is no valid division.
```

**Example 3:**

```
Input: nums = [4,2,9,8,2,12,7,12,10,5,8,5,5,7,9,2,5,11], k = 14
Output: [[2,2,2],[4,5,5],[5,5,7],[7,8,8],[9,9,10],[11,12,12]]
Explanation:
The difference between any two elements in each array is less than or equal to 14.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- n is a multiple of 3
- 1 <= nums[i] <= 105
- 1 <= k <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`，长度为 `n`，且 `n` 是 `3` 的倍数，同时给定一个正整数 `k`。  
请将数组 `nums` 划分为 `n / 3` 个大小为 `3` 的子数组（subarray），使得每个子数组中任意两个元素的差值 **不超过** `k`。  

返回一个二维数组，其中包含所有满足条件的子数组。如果不存在满足条件的划分方式，返回空数组 `[]`。若存在多种合法划分，返回任意一种即可。

## 示例

### 示例 1  
**输入**: `nums = [1,3,4,8,7,9,3,5,1]`, `k = 2`  
**输出**: `[[1,1,3],[3,4,5],[7,8,9]]`  
**解释**: 每个子数组中任意两个元素的差值均 `≤ 2`。

### 示例 2  
**输入**: `nums = [2,4,2,2,5,2]`, `k = 2`  
**输出**: `[]`  
**解释**:  
可能的划分方式只有两种（每种都是将 6 个元素分成两个大小为 3 的子数组）。  
由于数组中出现了四个 `2`，无论如何划分，总会出现一个子数组包含元素 `2` 与 `5`。而 `5 - 2 = 3 > k`，不满足条件，因此不存在有效的划分。

### 示例 3  
**输入**: `nums = [4,2,9,8,2,12,7,12,10,5,8,5,5,7,9,2,5,11]`, `k = 14`  
**输出**: `[[2,2,2],[4,5,5],[5,5,7],[7,8,8],[9,9,10],[11,12,12]]`  
**解释**: 每个子数组中任意两个元素的差值均 `≤ 14`。

## 约束条件

- `n == nums.length`
- `1 <= n <= 10^5`
- `n` 是 `3` 的倍数
- `1 <= nums[i] <= 10^5`
- `1 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有可能的 3 人一组的组合全部枚举出来，看看能否把每个元素恰好分配到一组且每组的最大差值 ≤ k」。  
这类似于把一堆水果（`nums`）全部摆进若干个装 3 个水果的盒子里，要求同一个盒子里的水果重量差不超过 `k`。

实现上可以采用**回溯（递归）**：

1. 从数组中任选 3 个未使用的元素组成一组，检查这 3 个数的 `max - min` 是否 ≤ k。  
2. 如果合法，就把这组放进当前的答案，然后继续递归处理剩余的元素。  
3. 当所有元素都被分配完（递归深度达到 `n/3`）时，得到一个可行解；若在某一步找不到合法的三元组，就回溯到上一步尝试别的组合。

> 这里的「任选 3 个」相当于在「字典」里随意挑词——效率极低，因为要检查所有组合。

#### 代码（Python）

```python
from typing import List

def brute_force(nums: List[int], k: int) -> List[List[int]]:
    n = len(nums)
    used = [False] * n               # 标记哪些下标已经被使用
    res = []                          # 最终答案

    def backtrack(groups: List[List[int]]) -> bool:
        # 所有元素都已被分配
        if len(groups) == n // 3:
            res.extend(groups)        # 把找到的分组复制到外层的 res
            return True

        # 找到第一个未使用的下标，作为本轮选取的起点（剪枝）
        first = 0
        while first < n and used[first]:
            first += 1
        if first == n:                 # 已经没有未使用的元素，说明不可能
            return False

        # 依次尝试把 first 与后面的两个未使用元素凑成一组
        for i in range(first + 1, n):
            if used[i]:
                continue
            for j in range(i + 1, n):
                if used[j]:
                    continue
                trio = [nums[first], nums[i], nums[j]]
                if max(trio) - min(trio) <= k:   # 检查差值是否满足要求
                    # 标记已使用
                    used[first] = used[i] = used[j] = True
                    if backtrack(groups + [trio]):   # 递归继续
                        return True
                    # 回溯，撤销标记
                    used[first] = used[i] = used[j] = False
        return False

    backtrack([])      # 从空分组开始搜索
    return res          # 若未找到合法划分，res 仍为空列表
```

#### 复杂度  

- **时间复杂度**：`O( C(n,3) * C(n-3,3) * … )`，实际上是 **指数级**（大约 `O((n/3)!)`），因为要尝试所有可能的三元组划分。可以把 `O(n³)` 看作「把所有 3‑元组合都枚举一次」的粗略上界，实际会更慢。  
- **空间复杂度**：`O(n)`，主要是递归栈和 `used` 数组占用的空间。

> 由于指数级时间，暴力解只能在 `n ≤ 9`（即最多 3 组）左右的小样例上跑得通，无法应对题目给出的 `n ≤ 10⁵`。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于枚举所有组合**。我们需要一种「一次排好序就能直接分组」的思路。  

**关键观察**：

- 对于任意合法划分，若把所有数从小到大排好序，那么同一组内部的最大差值一定不大于 `k`。  
- 为了让每组的差值尽可能小，**把相邻的三个数放在一起是最好的**。因为如果把第 `i`、`i+1`、`i+3` 放在一组，而把 `i+2` 放到别的组，那么必然会导致某组的最大差值 ≥ `nums[i+3] - nums[i]`，而把 `i,i+1,i+2` 放在一起可以把差值压到 `nums[i+2] - nums[i]`（更小或相等）。

换句话说，**如果存在一种合法划分，那么把排好序的数组按顺序每 3 个切成一段，一定也是合法的**。因此我们只需要：

1. **排序** `nums`（把水果从轻到重排好，类似把字典按字母顺序排好）。排序的时间复杂度是 `O(n log n)`。  
2. 按顺序检查每三个相邻元素 `nums[i]、nums[i+1]、nums[i+2]`（`i = 0,3,6,…`），看它们的最大差 `nums[i+2] - nums[i]` 是否 ≤ k。  
   - 若全部满足，直接返回这些三元组。  
   - 若有任意一组不满足，说明 **没有任何可能的划分**，直接返回空列表。

这就是典型的**贪心**策略：每一步都做「局部最优」——把相邻的最小的三个数放一起，保证差值最小，从而最大化整体成功的概率。

#### 代码（Python）

```python
from typing import List

def divideArray(nums: List[int], k: int) -> List[List[int]]:
    """
    贪心 + 排序：把排好序的数组每三个一组，检查差值是否满足要求。
    """
    nums.sort()                     # 1️⃣ 排序，时间 O(n log n)

    groups = []                     # 用来存放最终的三元组
    for i in range(0, len(nums), 3):
        # 取相邻的三个数
        trio = [nums[i], nums[i + 1], nums[i + 2]]
        # 2️⃣ 检查最大差值是否 ≤ k
        if trio[-1] - trio[0] > k:   # trio 已经是升序，trio[-1] 是最大，trio[0] 是最小
            return []                # 只要有一组不满足，说明不存在合法划分
        groups.append(trio)          # 合法则加入答案

    return groups                    # 全部检查通过，返回划分结果
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`。主要耗时在排序，随后一次线性遍历检查 `n/3` 组，时间为 `O(n)`，相较于暴力解的指数级快得多。  
- **空间复杂度**：`O(n)`（返回的结果需要存 `n/3` 组，每组 3 个整数），如果不计输出空间，仅使用 `O(1)` 的额外变量。

> 与暴力解相比，时间从「几乎不可能在 10⁵ 规模下跑完」降到「几毫秒内搞定」。

---

## 心得

- **核心技巧**：先排序，再**贪心**地把相邻的三个数分在一起。  
- **适用场景**：  
  1. 需要把元素分成固定大小的若干组，且每组内部要满足「最大值‑最小值」的约束（如「把学生按成绩分成三人小组，差距不超过 k」）。  
  2. 类似题目还有 **“分割数组使每段最大差值不超过 k”**（可用同样的排序+滑动窗口思路）。  
  3. **“把数组划分为若干对，使每对差 ≤ k”**（把 `3` 换成 `2`，思路相同）。  
- **一句话总结**：**把数排好序，局部最小差值的三元组必是全局可行解的唯一候选**。

---

## 反思

- **第一反应**：立刻想到「暴力枚举所有三元组」——因为最直观的做法就是「把所有可能的组合都试一遍」。
- **最容易踩的坑**：  
  - 忽略了 **“n 必须是 3 的倍数”**，导致在取 `nums[i+2]` 时出现越界。  
  - 没有先 **排序**，直接在原数组里随意挑三个数会导致差值不最小，从而误判为不可行。  
  - 在实现贪心时忘记检查每组的差值，直接返回分组，可能产生错误答案。  
- **下次类似题的第一步**：**先把数据排序**，然后思考「如果把相邻的固定大小元素放在一起，能否满足约束？」——这往往能把搜索空间从指数级压到线性或 `n log n`。