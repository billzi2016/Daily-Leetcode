# #1985. 数组中第 K 大的整数 / Find the Kth Largest Integer in the Array

> 难度：中等 · 标签：Array、String、Divide and Conquer、Sorting、Heap (Priority Queue)、Quickselect · [LeetCode 链接](https://leetcode.com/problems/find-the-kth-largest-integer-in-the-array/)

---

## 题目（英文原版）

**Description**

You are given an array of strings nums and an integer k. Each string in nums represents an integer without leading zeros.
Return the string that represents the kth largest integer in nums.
Note: Duplicate numbers should be counted distinctly. For example, if nums is ["1","2","2"], "2" is the first largest integer, "2" is the second-largest integer, and "1" is the third-largest integer.

**Examples**

**Example 1:**

```
Input: nums = ["3","6","7","10"], k = 4
Output: "3"
Explanation:
The numbers in nums sorted in non-decreasing order are ["3","6","7","10"].
The 4th largest integer in nums is "3".
```

**Example 2:**

```
Input: nums = ["2","21","12","1"], k = 3
Output: "2"
Explanation:
The numbers in nums sorted in non-decreasing order are ["1","2","12","21"].
The 3rd largest integer in nums is "2".
```

**Example 3:**

```
Input: nums = ["0","0"], k = 2
Output: "0"
Explanation:
The numbers in nums sorted in non-decreasing order are ["0","0"].
The 2nd largest integer in nums is "0".
```

**Constraints**

- 1 <= k <= nums.length <= 104
- 1 <= nums[i].length <= 100
- nums[i] consists of only digits.
- nums[i] will not have any leading zeros.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串数组 `nums` 和一个整数 `k`。`nums` 中的每个字符串均表示一个没有前导零的整数。  
返回表示 `nums` 中第 `k` 大整数的字符串。

**注意**  
重复的数字也应分别计数。例如，若 `nums` 为 `["1","2","2"]`，则 `"2"` 是第一大整数，第二个 `"2"` 是第二大整数，`"1"` 是第三大整数。

**示例 1**  
```text
Input: nums = ["3","6","7","10"], k = 4
Output: "3"
Explanation:
将 `nums` 中的数字按非递减顺序排序得到 ["3","6","7","10"]。第 4 大的整数是 "3"。
```

**示例 2**  
```text
Input: nums = ["2","21","12","1"], k = 3
Output: "2"
Explanation:
将 `nums` 中的数字按非递减顺序排序得到 ["1","2","12","21"]。第 3 大的整数是 "2"。
```

**示例 3**  
```text
Input: nums = ["0","0"], k = 2
Output: "0"
Explanation:
将 `nums` 中的数字按非递减顺序排序得到 ["0","0"]。第 2 大的整数是 "0"。
```

**约束条件**  

- `1 <= k <= nums.length <= 10^4`
- `1 <= nums[i].length <= 100`
- `nums[i]` 只包含数字字符。
- `nums[i]` 不会有任何前导零。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的办法是把所有字符串 **先全部转成可以比较大小的形式**，再把它们排个序，最后取第 `k` 大的那个。  
- **数据结构**：我们只需要一个普通的 Python 列表 `list`，把所有字符串放进去。  
  - 类比：把一堆数字装进一个抽屉（list），抽屉里可以随意取放。  
- **比较大小**：题目中的数字是以字符串形式给出的，且没有前导零。比较两个数字的大小可以用两条规则：  
  1. **长度不同** → 长的那个一定更大（因为位数多）。  
  2. **长度相同** → 从左到右逐位比较字符大小，遇到第一个不同的字符，字符大的那边的数字更大。  
- **实现**：把上述比较规则写成一个 **自定义排序键**（key），让 Python 的 `sorted` 能直接按照“数值大小”对字符串排序。  
- **为什么正确**：排序的定义正是把所有元素按从小到大（或从大到小）排列，只要比较函数符合数值大小的规则，排序后第 `k` 大的元素必然就是答案。  

#### 代码（Python）  
```python
from typing import List

def kthLargestNumber(nums: List[str], k: int) -> str:
    # ---------- 自定义比较规则 ----------
    # 1. 先比较长度，长度大的数一定更大
    # 2. 长度相同则逐字符比较（字符本身就是数字，'9' > '8' ...）
    def cmp_key(num: str):
        # 返回一个元组，Python 会先比较第一个元素（长度），再比较第二个元素（字符串本身）
        return (len(num), num)

    # ---------- 排序 ----------
    # sorted 默认升序，放入 reverse=True 就得到从大到小的顺序
    sorted_nums = sorted(nums, key=cmp_key, reverse=True)

    # ---------- 取第 k 大 ----------
    # 列表是 0-indexed，k 是 1-indexed，所以要减 1
    return sorted_nums[k - 1]
```

#### 复杂度  
- **时间复杂度**：`O(n log n)`  
  - `n` 是数组长度。排序需要比较 `log n` 层，每层都要遍历全部 `n` 条元素。  
  - 大白话：如果有 10,000 条数字，排序大约需要 `10,000 × log2(10,000) ≈ 10,000 × 14` 次比较，数量级上比直接遍历要大很多。  
- **空间复杂度**：`O(n)`  
  - 排序会产生一个新的列表（Python 的 `sorted` 会返回新列表），所以额外占用和原数组等量的空间。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **完整排序**，我们其实只需要找出第 `k` 大的元素，而不必把全部元素排好序。  
从 **“找第 k 大”** 这件事本身出发，有两种常用的技巧可以把工作量从 `O(n log n)` 降到 `O(n log k)` 或 `O(n)`：  

1. **最小堆（大小为 k）**  
   - 思路：维护一个只装 **当前最大的 k 个数字** 的最小堆（heap）。堆顶始终是这 k 个数字中最小的，也就是第 `k` 大的候选。  
   - 遍历数组时：  
     - 把新数字加入堆 `O(log k)`。  
     - 如果堆的大小超过 `k`，就弹出堆顶（最小的），保持堆始终只有 k 个元素。  
   - 最后堆顶就是第 `k` 大的数字。  
   - 适合 `k` 远小于 `n` 的情况，时间是 `O(n log k)`，空间是 `O(k)`。  

2. **Quickselect（快速选择）**  
   - 思路：和快速排序的划分过程相同，只是只递归处理包含第 `k` 大元素的那一侧。平均时间 `O(n)`，最坏情况 `O(n²)`（可以通过随机化降低概率）。  
   - 这里为了保持代码简洁、易于理解，我们实现 **最小堆** 方案。  

**关键点——比较大小**  
堆里放的仍然是字符串，为了让堆能比较大小，需要把比较规则交给 Python 的 `heapq`。最直接的办法是 **把每个字符串映射成一个可以直接比较的键**（与排序时相同），然后把 `(key, original_string)` 这个二元组放进堆。二元组的第一个元素 `key` 会被用来比较大小，第二个元素是原始字符串，最终返回时直接取出来。

#### 代码（Python）  
```python
import heapq
from typing import List

def kthLargestNumber(nums: List[str], k: int) -> str:
    # ---------- 辅助函数：把字符串映射成可比较的键 ----------
    def cmp_key(num: str):
        # 长度越大越重要，长度相同再比较字符串本身
        return (len(num), num)

    # ---------- 最小堆（大小维持在 k） ----------
    min_heap = []                     # heap 中的元素形如 (key, original_str)

    for num in nums:
        # 把当前数字连同比较键一起压入堆
        heapq.heappush(min_heap, (cmp_key(num), num))
        # 如果堆的大小超过 k，弹出最小的（也就是第 k+1 大的那个）
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    # 循环结束后，堆里恰好保存了最大的 k 个数字，堆顶是第 k 大
    return min_heap[0][1]   # 取出原始字符串
```

#### 复杂度  
- **时间复杂度**：`O(n log k)`  
  - 每次 `heappush`/`heappop` 的代价是 `log k`（因为堆最多只有 k 个元素），遍历 `n` 条数据，总共 `n·log k` 次操作。  
  - 大白话：如果 `n = 10,000`，`k = 100`，那么只需要大约 `10,000 × log2(100) ≈ 10,000 × 7` 次比较，比完整排序的 `10,000 × 14` 次明显更少。  

- **空间复杂度**：`O(k)`  
  - 堆里最多只存 `k` 条记录，若 `k` 远小于 `n`，可以节省大量内存。  

---  

## 心得  

- **核心技巧**：利用 **堆（优先队列）** 只保留 “前 k 大” 的元素，避免对全部数据排序。  
- **适用的题型**：  
  1. “第 k 大/小元素” 系列（如 LeetCode 215 `Kth Largest Element in an Array`）。  
  2. “前 K 个最小/最大” 类问题（如 Top K Frequent Elements）。  
  3. “流式数据” 场景下的实时排名（如实时统计网站访问量前 K）。  
- **一句话总结**：**“只保留你需要的 k 条最大记录，用最小堆把它们维持在一起”。**  

---  

## 反思  

- **第一反应**：直接把所有字符串排序，然后取第 `k` 大。  
- **最容易踩的坑**：  
  - **比较规则写错**：忽略了字符串长度不同的情况，导致 “100” 被错误地认为比 “99” 小。  
  - **堆的比较键**：直接把字符串放进堆会按照字典序比较，而不是数值大小，需要自行提供键。  
  - **边界条件**：`k = 1`（最大值）或 `k = len(nums)`（最小值）时，堆的大小仍然要维持 `k`，否则会提前弹出导致错误。  
- **下次遇到同类题**：第一步先问自己 “我真的需要完整排序吗？” 若答案是否定的，立刻考虑 **堆** 或 **Quickselect** 来只保留必要的前 K（或后 K）元素。