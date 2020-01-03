# #719. 第 K 小的数对距离 / Find K-th Smallest Pair Distance

> 难度：困难 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)

---

## 题目（英文原版）

**Description**

The distance of a pair of integers a and b is defined as the absolute difference between a and b.
Given an integer array nums and an integer k, return the kth smallest distance among all the pairs nums[i] and nums[j] where 0 <= i < j < nums.length.

**Examples**

**Example 1:**

```
Input: nums = [1,3,1], k = 1
Output: 0
Explanation: Here are all the pairs:
(1,3) -> 2
(1,1) -> 0
(3,1) -> 2
Then the 1st smallest distance pair is (1,1), and its distance is 0.
```

**Example 2:**

```
Input: nums = [1,1,1], k = 2
Output: 0
```

**Example 3:**

```
Input: nums = [1,6,1], k = 3
Output: 5
```

**Constraints**

- n == nums.length
- 2 <= n <= 104
- 0 <= nums[i] <= 106
- 1 <= k <= n * (n - 1) / 2

---

## 题目（中文翻译）

数对（pair）\(a\) 与 \(b\) 的距离（distance）定义为它们的绝对差的值，即 \(|a-b|\)。  
给定一个整数数组 `nums` 和一个整数 `k`，返回所有满足 \(0 \le i < j < \text{nums.length}\) 的数对 `nums[i]` 与 `nums[j]` 的距离中第 `k` 小的那个。

**示例 1：**  
**输入：** `nums = [1,3,1]`, `k = 1`  
**输出：** `0`  
**解释：** 所有数对及其距离如下：  
- \((1,3) \rightarrow 2\)  
- \((1,1) \rightarrow 0\)  
- \((3,1) \rightarrow 2\)  
第 1 小的距离对应的数对是 \((1,1)\)，其距离为 `0`。

**示例 2：**  
**输入：** `nums = [1,1,1]`, `k = 2`  
**输出：** `0`  
**解释：** 所有数对的距离均为 `0`，因此第 2 小的距离仍是 `0`。

**示例 3：**  
**输入：** `nums = [1,6,1]`, `k = 3`  
**输出：** `5`  
**解释：** 数对及其距离为 \((1,6) \rightarrow 5\)、\((1,1) \rightarrow 0\)、\((6,1) \rightarrow 5\)。第 3 小的距离是 `5`。

**约束条件：**  
- `n == nums.length`  
- \(2 \le n \le 10^4\)  
- \(0 \le \text{nums}[i] \le 10^6\)  
- \(1 \le k \le \frac{n \times (n - 1)}{2}\)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 合法的数对 `(i, j)`（`i < j`）都列举出来，算出它们的距离 `|nums[i] - nums[j]|`，放进一个列表，然后把列表从小到大排好序，最后取第 `k` 小的元素。

- **用到的数据结构**  
  - `list`（列表）：就像我们平时记事本，把每一对的距离一个个写下来。  
  - `sort`（排序）：相当于把记事本里的数字从小到大排好顺序，类似把字典里的词按字母顺序排列。

- **为什么正确**  
  把所有可能的距离都算出来后，排好序后第 `k` 位的数必然就是第 `k` 小的距离，因为我们没有遗漏也没有多余的。

- **复杂度分析（大白话）**  
  - **时间**：要遍历所有的数对，`n` 个数有 `n·(n-1)/2` 对（相当于“从 `n` 个人里挑出两个人”的组合数），每对都要算一次距离，再把所有距离排序。  
    - 生成距离的循环是 **O(n²)**（比如 `n=10⁴` 时，大约要跑 5 × 10⁷ 次），  
    - 排序的时间是 **O(m log m)**，其中 `m = n·(n-1)/2`，也大约是 **O(n² log n)**。  
    综合下来就是 **O(n² log n)**。  
  - **空间**：我们要把所有距离存下来，数量同样是 `m ≈ n²/2`，所以需要 **O(n²)** 的额外空间。

> **小结**：暴力解思路简单，代码几行就能写好，但在最坏情况下会占用几百 MB 的内存并且跑得很慢，无法通过大数据规模的测试。

#### 代码（Python）

```python
from typing import List

def smallestDistancePair_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # 1. 计算所有距离，存进列表
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            distances.append(abs(nums[i] - nums[j]))   # 计算绝对差
    # 2. 对所有距离排序
    distances.sort()                                   # 从小到大排好序
    # 3. 第 k 小的即为答案（k 从 1 开始计数）
    return distances[k - 1]
```

#### 复杂度

- **时间复杂度**：`O(n² log n)`  
  - `n²` 来自两层循环遍历所有数对，`log n` 来自对 `n²` 个元素的排序。  
  - 用生活中的例子比喻：如果你要把 10 000 本书的每两本之间的相似度算出来并排序，那显然不太实际。

- **空间复杂度**：`O(n²)`  
  - 需要把所有距离都存下来，相当于把每一对的“差距”都写在纸上，纸张数量随 `n²` 指数增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有数对**（`O(n²)`）以及 **存储所有距离**。我们需要一种办法 **不显式列举每一对**，却仍能判断 “有多少对的距离 ≤ 某个阈值 X”。如果能做到这一点，就可以对答案本身进行二分搜索（Binary Search on Answer），把时间降到 `O(n log maxDist)`。

**关键观察**：

1. **距离的取值范围是有界的**  
   - 所有数都是非负且 ≤ `10⁶`，所以任意两数的最大距离不超过 `10⁶`（即 `max(nums) - min(nums)`）。
2. **单调性**  
   - 设 `cnt(X)` 为「距离 ≤ X 的数对数量」。如果 `X₁ < X₂`，显然 `cnt(X₁) ≤ cnt(X₂)`，因为把阈值放大只会让更多对满足条件。  
   - 这正好是二分搜索需要的「单调函数」属性。

**如何在 O(n) 或 O(n log n) 内求 cnt(X)？**  

先把数组 **排序**。排序后，对于每个左指针 `i`，我们可以用右指针 `j` 向右移动，保持 `nums[j] - nums[i] ≤ X`。此时所有满足条件的对就是 `(i, i+1)…(i, j)`，共计 `j - i` 对。随后把左指针右移，右指针不需要回退，因为数组是递增的，`j` 只会继续向右走。这种 **双指针（Two Pointers）** 的遍历一次完成所有 `cnt(X)` 的统计，时间是 `O(n)`。

**整体算法**：

1. 对 `nums` 进行升序排序（`O(n log n)`）。
2. 设搜索区间 `[low, high] = [0, max(nums) - min(nums)]`。
3. 二分搜索：
   - 取中点 `mid = (low + high) // 2`。
   - 用双指针统计 `cnt(mid)`：有多少对距离 ≤ `mid`。
   - 若 `cnt(mid) >= k`，说明第 `k` 小的距离 **不大于** `mid`，把 `high` 收紧到 `mid`；否则把 `low` 收紧到 `mid + 1`。
4. 循环结束时 `low`（或 `high`）即为答案。

**类比**：  
想象你在图书馆排队借书，想找第 `k` 本最早出版的书。先把所有书按出版年份排序，然后用「二分」的方式快速定位第 `k` 本的年份，而不是把所有书一本一本检查。

#### 代码（Python）

```python
from typing import List

def smallestDistancePair(nums: List[int], k: int) -> int:
    # 1. 排序，后面用双指针才能线性统计
    nums.sort()
    
    # 2. 定义搜索范围：最小可能距离 0，最大可能距离 max-min
    low, high = 0, nums[-1] - nums[0]

    # 3. 二分搜索答案
    while low < high:
        mid = (low + high) // 2           # 试探的距离阈值
        # 用双指针统计距离 <= mid 的对数
        count = 0
        left = 0
        for right in range(len(nums)):
            # 移动 left，使得 nums[right] - nums[left] <= mid 成立
            while nums[right] - nums[left] > mid:
                left += 1
            # 此时 (left, right) 之间的所有左指针位置都满足条件
            count += right - left         # 贡献的对数
        # 根据计数决定收敛方向
        if count >= k:                     # enough pairs, answer ≤ mid
            high = mid
        else:                              # not enough, answer > mid
            low = mid + 1
    # 循环结束时 low == high，即为第 k 小的距离
    return low
```

> **代码要点说明**  
> - `nums.sort()`：把数组变成有序序列，类似把所有学生按身高排好队。  
> - 双指针 `left`、`right`：`right` 负责向右“扩张”，`left` 负责“收紧”，保证窗口内的距离始终 ≤ `mid`。  
> - `count += right - left`：窗口里除了 `right` 本身，左侧的每一个元素都与 `right` 形成一对满足条件的距离。  
> - 二分循环 `while low < high`：每次都把搜索区间压缩一半，直至唯一解。

#### 复杂度

- **时间复杂度**：`O(n log D)`，其中 `D = max(nums) - min(nums)`（最大可能距离）。  
  - 排序 `O(n log n)`（占主导），  
  - 二分搜索的迭代次数约为 `log₂(D)`（最多约 20 次，因为 `D ≤ 10⁶`），每次遍历数组一次 `O(n)`，所以二分部分是 `O(n log D)`。  
  - 综合起来仍是 `O(n log n + n log D)`，在本题数据范围内可以视作 `O(n log n)`。

- **空间复杂度**：`O(1)`（不计输入数组本身的存储）。  
  - 只用了几个整数指针和计数器，和数组大小无关。

> 与暴力解对比：  
> - 暴力解需要 `O(n²)` 的时间和空间，最坏情况下会超时或内存炸掉。  
> - 最优解把时间降到了接近 `O(n log n)`，空间几乎不增，只用了常数级别的额外空间。

---

## 心得

- **核心技巧**：**二分答案 + 双指针计数**。先把搜索空间变成「距离」的范围，再用线性双指针快速判断「≤ 某阈值」的对数，实现对单调函数的二分搜索。
- **适用题型**  
  1. “第 K 小/大”类的数值答案（如第 K 小的子数组和、第 K 大的矩形面积）。  
  2. 需要判断「满足某个阈值的组合数量」的场景（如船运载重量、划分区间的最大最小值）。
- **一句话总结**：把「找第 K 小」转化为「阈值 X 下有多少对」，利用单调性二分搜索即可快速定位答案。

---

## 反思

- **第一反应**：看到「所有数对的距离」就想到直接枚举，然后排序取第 `k`。这是一条常见的直觉路径，却忽视了规模限制。
- **最容易踩的坑**  
  - **忘记先排序**：双指针统计依赖数组有序，若未排序会导致错误计数。  
  - **计数溢出**：`count` 可能超过 32 位整数范围（在 Python 中自动扩展，但在其他语言要使用 `long`）。  
  - **二分边界**：循环条件要写成 `while low < high`，并在 `count >= k` 时收紧右边界 `high = mid`，否则会出现无限循环或错过答案。
- **下次遇到同类题**：第一步想到「能否把答案本身二分？」——即把「第 K 小」转化为「阈值下的计数」问题，再寻找一种 **线性或对数级** 的计数方式（如双指针、前缀和、滑动窗口）。这样思路就已经指向最优解的雏形。