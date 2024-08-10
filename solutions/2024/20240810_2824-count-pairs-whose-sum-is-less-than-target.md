# #2824. 计数和小于目标的下标对 / Count Pairs Whose Sum is Less than Target

> 难度：简单 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-pairs-whose-sum-is-less-than-target/)

---

## 题目（英文原版）

**Description**



**Examples**

**Example 1:**

```
Input: nums = [-1,1,2,3,1], target = 2
Output: 3
Explanation: There are 3 pairs of indices that satisfy the conditions in the statement:
- (0, 1) since 0 < 1 and nums[0] + nums[1] = 0 < target
- (0, 2) since 0 < 2 and nums[0] + nums[2] = 1 < target 
- (0, 4) since 0 < 4 and nums[0] + nums[4] = 0 < target
Note that (0, 3) is not counted since nums[0] + nums[3] is not strictly less than the target.
```

**Example 2:**

```
Input: nums = [-6,2,5,-2,-7,-1,3], target = -2
Output: 10
Explanation: There are 10 pairs of indices that satisfy the conditions in the statement:
- (0, 1) since 0 < 1 and nums[0] + nums[1] = -4 < target
- (0, 3) since 0 < 3 and nums[0] + nums[3] = -8 < target
- (0, 4) since 0 < 4 and nums[0] + nums[4] = -13 < target
- (0, 5) since 0 < 5 and nums[0] + nums[5] = -7 < target
- (0, 6) since 0 < 6 and nums[0] + nums[6] = -3 < target
- (1, 4) since 1 < 4 and nums[1] + nums[4] = -5 < target
- (3, 4) since 3 < 4 and nums[3] + nums[4] = -9 < target
- (3, 5) since 3 < 5 and nums[3] + nums[5] = -3 < target
- (4, 5) since 4 < 5 and nums[4] + nums[5] = -8 < target
- (4, 6) since 4 < 6 and nums[4] + nums[6] = -4 < target
```

**Constraints**

- 1 <= nums.length == n <= 50
- -50 <= nums[i], target <= 50

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个整数 `target`，统计满足以下条件的下标对 `(i, j)` 的数量：

- `i < j`  
- `nums[i] + nums[j] < target`

返回满足条件的下标对的总数。

---

### 示例

#### 示例 1  
**输入**  
``` 
nums = [-1,1,2,3,1], target = 2
```  
**输出**  
```
3
```  
**解释**  
满足条件的下标对共有 3 对：

- `(0, 1)` 因为 `0 < 1` 且 `nums[0] + nums[1] = 0 < target`
- `(0, 2)` 因为 `0 < 2` 且 `nums[0] + nums[2] = 1 < target`
- `(0, 4)` 因为 `0 < 4` 且 `nums[0] + nums[4] = 0 < target`

注意 `(0, 3)` 不计入，因为 `nums[0] + nums[3]` 并未严格小于目标值。

#### 示例 2  
**输入**  
``` 
nums = [-6,2,5,-2,-7,-1,3], target = -2
```  
**输出**  
```
10
```  
**解释**  
满足条件的下标对共有 10 对，例如：

- `(0, 1)` 因为 `0 < 1` 且 `nums[0] + nums[1] = -4 < target`
- `(0, 3)` 因为 `0 < 3` 且 `nums[0] + nums[3] = -8 < target`
- `(0, 4)` 因为 `0 < 4` 且 `nums[0] + nums[4] = -13 < target`
- `(0, 5)` 因为 `0 < 5` 且 `nums[0] + nums[5] = -7 < target`
- `(0, 6)` 因为 `0 < 6` 且 `nums[0] + nums[6] = -3 < target`
- …（其余满足条件的对省略）

---

### 约束条件
- `1 <= nums.length == n <= 50`
- `-50 <= nums[i], target <= 50`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的「下标对」都枚举一遍，然后检查它们的和是否严格小于 `target`。  
- **数据结构**：只需要一个普通的 Python 列表 `nums`，不需要额外的结构。  
- **生活化类比**：把数组想象成一排座位，每个人都有一个数字。我们要把所有「左边坐的人」和「右边坐的人」配对，看看他们的分数和是否低于目标分数。  
- **正确性**：因为我们遍历了所有满足 `i < j` 的下标组合（即左边的下标永远小于右边的），只要把每一对的和和 `target` 做比较，就不会漏掉任何合法的配对。  

#### 代码（Python）

```python
def count_pairs_brute(nums, target):
    """
    暴力枚举所有 i < j 的组合，统计 nums[i] + nums[j] < target 的次数
    """
    n = len(nums)
    ans = 0
    # 外层遍历左边的下标 i
    for i in range(n):
        # 内层遍历右边的下标 j，保证 j > i
        for j in range(i + 1, n):
            # 如果两数之和小于 target，计数加一
            if nums[i] + nums[j] < target:
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 这里的 `n` 是数组长度。我们用了两层循环，第一层 `n` 次，第二层平均约 `n/2` 次，乘起来就是大约 `n²/2` 次操作。  
  - 用大白话说，就是如果数组有 50 个元素，最坏情况下要检查 50 × 49 / 2 ≈ 1,225 对，仍然可以接受（因为 `n ≤ 50`）。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`n、ans、i、j`），和输入数组本身无关，不会随 `n` 增大而增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于「每一对都要检查」，这会产生 `O(n²)` 的时间。我们可以利用**排序 + 双指针**的技巧把时间降到 `O(n log n)`（排序）+ `O(n)`（双指针）≈ `O(n log n)`。

**关键观察**  
- 把数组从小到大排好序后，左侧的数越小，右侧的数越大。  
- 对于固定的左指针 `l`（指向较小的数），如果 `nums[l] + nums[r] < target`，那么只要 `r` 往左移动（变小），和会更小，**一定**满足条件。于是 **以 `l` 为左端点，所有 `l < k ≤ r` 的 `k` 都可以构成合法对**，这一次就可以一次性计数 `r - l` 对。  
- 若 `nums[l] + nums[r] >= target`，说明右边的数太大，需要把右指针左移，使和变小。

**算法步骤**  

1. 对 `nums` 进行升序排序。  
2. 初始化左指针 `l = 0`，右指针 `r = len(nums) - 1`。  
3. 当 `l < r` 时循环：  
   - 若 `nums[l] + nums[r] < target`：  
     - 说明 `l` 与 `l+1 … r` 都合法，计数 `r - l`。  
     - 左指针右移 `l += 1`（尝试以更大的左数继续计数）。  
   - 否则（和不小于 target）：  
     - 右指针左移 `r -= 1`（把右边的大数缩小）。  
4. 循环结束后返回计数。

**类比帮助理解**  
想象两个人站在一条直线的两端，左边的叫“小明”，右边的叫“小红”。我们要让他们手拉手的距离（这里是数值和）小于某个阈值。  
- 如果现在小明和小红的距离已经太远（和 ≥ target），我们让小红往左走一步（右指针左移）。  
- 如果距离已经够近（和 < target），那么小明可以和小红之间的所有人（包括小红）都手拉手，这一次我们一次性统计所有可能的组合，然后让小明往右走一步（左指针右移），继续检查。

#### 代码（Python）

```python
def count_pairs_opt(nums, target):
    """
    排序 + 双指针：在 O(n log n) 时间内统计满足 nums[i] + nums[j] < target 且 i < j 的配对数
    """
    nums.sort()                     # O(n log n) 的排序
    n = len(nums)
    left, right = 0, n - 1
    ans = 0

    while left < right:
        # 当前左、右指针对应的和
        current_sum = nums[left] + nums[right]

        if current_sum < target:
            # 只要左指针固定，右指针及其左侧的所有元素都满足条件
            # 例如 left=2, right=5 => 合法对有 (2,3),(2,4),(2,5) 共 5-2=3 对
            ans += right - left     # 直接一次性计数
            left += 1               # 左指针右移，尝试更大的左数
        else:
            # 和不够小，需要把右边的大数缩小
            right -= 1              # 右指针左移

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，双指针的遍历每次至少移动一个指针，最多 `n` 步，故为 `O(n)`。整体以较大的 `O(n log n)` 为主。  
  - 与暴力解的 `O(n²)` 相比，尤其在 `n` 较大时（虽然本题 `n ≤ 50`），速度提升明显。

- **空间复杂度**：`O(1)`（不计排序使用的原地排序）  
  - 只用了常数个额外变量 `left、right、ans、current_sum`。如果使用 Python 的 `list.sort()`，它是原地排序，不会额外占用与 `n` 成正比的空间。

---

## 心得

- **核心技巧**：**排序 + 双指针**，把「两数之和」的问题转化为「在有序序列中寻找满足不等式的区间」。
- **适用题型**  
  1. “两数之和小于/大于目标” 类问题（如 LeetCode 1679: `Max Number of K-Sum Pairs` 的变形）。  
  2. “三数之和” 这类需要在有序数组中快速定位区间的题目（如 259 `3Sum Smaller`）。  
  3. “区间计数” 类问题，例如统计子数组和小于目标值的数量（可以用前缀和 + 双指针或二分）。
- **一句话总结**：**先把数据排好序，再用两个指针一次遍历，把所有满足条件的组合一次性算完**。

---

## 反思

- **第一反应**：看到「计数满足 nums[i] + nums[j] < target」直接想到暴力双循环，因为约束很小，先写出最容易实现的方案验证正确性。  
- **最容易踩的坑**  
  1. **下标顺序**：必须保证 `i < j`，否则会重复计数。双指针自然满足这一点，但在手写暴力时要注意循环范围。  
  2. **负数和目标值**：因为数组和目标都可能为负数，不能把 “>” 或 “>=” 写错。  
  3. **排序后计数**：在双指针计数时，记得一次性加 `right - left`，而不是只加 1，否则会退化回 `O(n²)`。  
- **下次遇到同类题**：**第一步先思考能否排序**，如果可以，立刻尝试 **双指针** 或 **二分搜索** 来把「枚举」的时间降到线性或对数级。这样往往能从 “能做” 直接跳到 “更快”。