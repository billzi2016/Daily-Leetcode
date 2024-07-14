# #2779. **对数组应用操作后的最大美丽值** / Maximum Beauty of an Array After Applying Operation

> 难度：中等 · 标签：Array、Binary Search、Sliding Window、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums and a non-negative integer k.
In one operation, you can do the following:
The beauty of the array is the length of the longest subsequence consisting of equal elements.
Return the maximum possible beauty of the array nums after applying the operation any number of times.
Note that you can apply the operation to each index only once.
A subsequence of an array is a new array generated from the original array by deleting some elements (possibly none) without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [4,6,1,2], k = 2
Output: 3
Explanation: In this example, we apply the following operations:
- Choose index 1, replace it with 4 (from range [4,8]), nums = [4,4,1,2].
- Choose index 3, replace it with 4 (from range [0,4]), nums = [4,4,1,4].
After the applied operations, the beauty of the array nums is 3 (subsequence consisting of indices 0, 1, and 3).
It can be proven that 3 is the maximum possible length we can achieve.
```

**Example 2:**

```
Input: nums = [1,1,1,1], k = 10
Output: 4
Explanation: In this example we don't have to apply any operations.
The beauty of the array nums is 4 (whole array).
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i], k <= 105

---

## 题目（中文翻译）

给定一个下标从 0 开始的数组 `nums` 和一个非负整数 `k`。  
在一次操作中，你可以对数组中的任意下标 `i` 执行以下步骤：

- 将 `nums[i]` 替换为区间 `[nums[i] - k, nums[i] + k]` 中的任意整数（上下界均包含）。

数组的 **美丽度** 定义为**相同元素的最长子序列（subsequence）**的长度。  
返回对数组 `nums` 任意次数地执行上述操作后，能够得到的最大可能美丽度。  
注意，每个下标至多只能被操作一次。

> **子序列（subsequence）**：从原数组中删除若干（可能为零）元素后，保持剩余元素相对顺序得到的新数组。

---

### 示例

**示例 1**

```
Input: nums = [4,6,1,2], k = 2
Output: 3
Explanation:
- 选择下标 1，将其替换为 4（取自区间 [4,8]），此时 nums = [4,4,1,2]。
- 选择下标 3，将其替换为 4（取自区间 [0,4]），此时 nums = [4,4,1,4]。
经过上述操作后，数组的美丽度为 3（由下标 0、1、3 组成的子序列全部为 4）。
可以证明，3 是能够达到的最大美丽度。
```

**示例 2**

```
Input: nums = [1,1,1,1], k = 10
Output: 4
Explanation:
在此例中无需进行任何操作，数组本身的美丽度即为 4（整个数组都是相同元素）。
```

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `0 <= nums[i], k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的子序列**，检查它们是否能够在一次操作（每个位置最多改一次）后全部变成同一个数。  

- **子序列**：可以把它想象成从原数组里挑出若干个位置，保持原来的顺序，就像从一本书里挑出几页不打乱顺序一样。  
- **每个位置的可改范围**：对于下标 `i`，我们只能把 `nums[i]` 改成 `[nums[i]-k, nums[i]+k]` 区间里的任意整数。可以把这个区间比作“词典”，词典的**键**是原数，**值**是它可以改到的所有页码（数值）。  
- **能否统一成同一个数**：只要所有挑出来的区间有交集（即存在一个数同时落在每个区间里），就可以把它们全部改成这个数。  

于是我们可以：

1. 先不考虑顺序，直接在原数组里任选一段连续的下标 `[i, j]`（因为子序列的相对顺序不影响能否统一，只要取的下标集合相同）。  
2. 检查这段区间的所有可改范围是否有公共交集。  
   - 交集不为空的充要条件是：**最大左端点 ≤ 最小右端点**。  
   - 对于 `nums[i]…nums[j]`，左端点是 `nums[t]-k`，右端点是 `nums[t]+k`。  
   - 简化后得到 `nums[j] - nums[i] ≤ 2*k`（因为左端点最大的是 `nums[j]-k`，右端点最小的是 `nums[i]+k`）。  

所以暴力做法就是：**枚举所有 `i`，向右扩展 `j`，只要 `nums[j] - nums[i] ≤ 2k` 就继续，否则停止**。记录最大的窗口长度即为答案。

> 这里的枚举是 **O(n²)** 的，因为 `i` 有 `n` 种，`j` 最多也会遍历 `n` 次。

#### 代码（Python）

```python
from typing import List

def max_beauty_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    ans = 1                     # 至少能保留一个元素
    # 枚举左端点 i
    for i in range(n):
        # 从 i 开始往右尝试所有可能的右端点 j
        for j in range(i, n):
            # 判断区间 [i, j] 是否可以统一成同一个数
            if nums[j] - nums[i] <= 2 * k:
                # 符合条件，窗口长度为 j-i+1
                ans = max(ans, j - i + 1)
            else:
                # 已经超过 2k，后面的 j 更大只会更不满足，直接跳出
                break
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`。想象一下，你在一次遍历中，要把每个人和后面所有人都比一遍，最坏情况下会出现 `n * n / 2` 次比较。  
- **空间复杂度**：`O(1)`。只用了几个额外变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要从左端点重新扫描右端点**，导致大量重复比较。我们可以把“左端点最大左端点 ≤ 右端点最小右端点”这件事**用排序+滑动窗口**一次性搞定。

**关键观察**  

1. **排序后，区间的左端点和右端点的顺序会对应**。把 `nums` 从小到大排好序，记为 `arr`。  
2. 对于排好序的 `arr[i]…arr[j]`，若 `arr[j] - arr[i] ≤ 2k`，则必然有公共交集（因为左端点最大的是 `arr[j]-k`，右端点最小的是 `arr[i]+k`）。  
3. 这正好是**寻找最长满足 `arr[j] - arr[i] ≤ 2k` 的子数组**的问题。  
4. “子数组”在排好序的数组里对应**原数组的某个子序列**（因为排序只改变了位置顺序，但我们只关心是否能统一成同一个数，而不在乎原来的相对顺序）。

于是我们可以使用 **双指针（滑动窗口）**：

- `left` 指向窗口左端，`right` 向右逐步扩张。  
- 每次把 `right` 往右移动一步，检查 `arr[right] - arr[left]` 是否仍 ≤ `2k`。  
  - 若满足，窗口合法，更新答案 `max_len = max(max_len, right-left+1)`。  
  - 若不满足，说明左端太小，需要把 `left` 向右收缩，直到窗口重新合法。  
- 整个过程只遍历数组一次，时间 `O(n)`。

**为什么排序不会破坏答案？**  
因为我们只关心“是否存在一个公共交集”，而这个条件只与数值大小有关，与它们在原数组中的相对位置无关。排序后把相近的数放在一起，恰好帮助我们快速找到最长合法窗口。

#### 代码（Python）

```python
from typing import List

def max_beauty(nums: List[int], k: int) -> int:
    # 1. 先把数组从小到大排好序
    arr = sorted(nums)               # 排序相当于把“词典”里的词按照字母顺序排好

    left = 0                         # 窗口左端的指针
    max_len = 1                      # 至少能保留一个元素

    # 2. right 指针从左到右遍历整个数组
    for right in range(len(arr)):
        # 3. 若窗口不满足 arr[right] - arr[left] <= 2k，就把左端收缩
        while arr[right] - arr[left] > 2 * k:
            left += 1                # 收缩左端，等价于把“不合格的词”丢掉
        # 4. 此时窗口合法，更新最大长度
        max_len = max(max_len, right - left + 1)

    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n log n)`。排序需要 `O(n log n)`，滑动窗口只需一次线性遍历 `O(n)`，两者相加仍是 `O(n log n)`。相对于暴力的 `O(n²)`，提升显著。  
- **空间复杂度**：`O(1)`（不计排序本身的原地实现）。只用了几个指针变量，和数组大小无关。

---

## 心得

- **核心技巧**：把“每个数能改到的区间有公共交集”转化为 **“最大值与最小值之差 ≤ 2k”**，再用 **排序 + 双指针（滑动窗口）** 在一次遍历中求最长满足条件的子数组。  
- **适用场景**：  
  1. “区间交集非空”类问题（如 LeetCode 2520. Count the Number of Pairs With Absolute Difference K）。  
  2. “在数值范围内找最长子序列”类问题（如 1004. Max Consecutive Ones III、424. Longest Repeating Character Replacement）。  
- **一句话总结**：**把每个元素的可改范围抽象成区间，利用排序让区间左右端点有序，再用滑动窗口一次扫完所有可能的窗口**。

---

## 反思

- **第一反应**：看到“每个位置只能改一次”，立刻想到**区间交集**，于是尝试枚举子序列检查交集。  
- **最容易踩的坑**：  
  - 忘记把 `nums[i]` 的改动范围写成 `[nums[i]-k, nums[i]+k]`，导致条件写成 `nums[j] - nums[i] ≤ k`（少乘 2）。  
  - 只在原数组上滑动窗口而不排序，导致错过跨越原来顺序的合法组合。  
- **下次类似题的第一步**：先**把每个元素的可行取值范围抽象成区间**，思考“所有区间是否有公共交集”，如果答案只跟数值大小有关，立刻**考虑排序 + 双指针**。