# #1539. 第 K 个缺失的正数 / Kth Missing Positive Number

> 难度：简单 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/kth-missing-positive-number/)

---

## 题目（英文原版）

**Description**

Given an array arr of positive integers sorted in a strictly increasing order, and an integer k.
Return the kth positive integer that is missing from this array.
Follow up:
Could you solve this problem in less than O(n) complexity?

**Examples**

**Example 1:**

```
Input: arr = [2,3,4,7,11], k = 5
Output: 9
Explanation: The missing positive integers are [1,5,6,8,9,10,12,13,...]. The 5th missing positive integer is 9.
```

**Example 2:**

```
Input: arr = [1,2,3,4], k = 2
Output: 6
Explanation: The missing positive integers are [5,6,7,...]. The 2nd missing positive integer is 6.
```

**Constraints**

- 1 <= arr.length <= 1000
- 1 <= arr[i] <= 1000
- 1 <= k <= 1000
- arr[i] < arr[j] for 1 <= i < j <= arr.length

---

## 题目（中文翻译）

给定一个按严格递增（strictly increasing order）排序的正整数数组 `arr`，以及一个整数 `k`。返回该数组中第 `k` 个缺失的正整数（positive integer）。

**示例 1：**  

**示例 2：**  

**进阶：**  
能否在低于 `O(n)` 的时间复杂度内完成此题？

**示例：**  

**示例 1:**  
```
Input: arr = [2,3,4,7,11], k = 5
Output: 9
Explanation: 缺失的正整数为 [1,5,6,8,9,10,12,13,...]。第 5 个缺失的正整数是 9。
```

**示例 2:**  
```
Input: arr = [1,2,3,4], k = 2
Output: 6
Explanation: 缺失的正整数为 [5,6,7,...]。第 2 个缺失的正整数是 6。
```

**约束条件：**  
- `1 <= arr.length <= 1000`  
- `1 <= arr[i] <= 1000`  
- `1 <= k <= 1000`  
- 对任意 `1 <= i < j <= arr.length`，都有 `arr[i] < arr[j]`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：从数字 `1` 开始往后枚举，每遇到一个不在数组 `arr` 里的正整数，就把它记为“缺失的正整数”。当我们记录到第 `k` 个缺失的数时，就返回它。  

- **数据结构**：这里我们只需要遍历数组 `arr`，所以用最普通的 **列表**（list）就够了。  
- **生活化类比**：把 `arr` 想象成一本已经排好序的“已收录的号码本”。我们从 `1` 开始检查每个号码是否已经在本子里，如果不在，就相当于“这本子里缺了这页”，我们就记下来。  
- **正确性**：因为我们是从最小的正整数 `1` 按顺序检查，每一次缺失的数字都恰好是当前缺失集合的下一个元素，所以第 `k` 次记录的数字一定是第 `k` 个缺失的正整数。  

#### 代码（Python）  
```python
def findKthPositive(arr, k):
    """暴力遍历，找到第 k 个缺失的正整数"""
    missing_cnt = 0          # 已经找到的缺失数的个数
    candidate = 1           # 当前检查的正整数

    # 用集合加速“是否在 arr 中”的查询（O(1)），但仍保持整体 O(n) 级别
    s = set(arr)

    while True:
        if candidate not in s:          # candidate 不在 arr 中 → 缺失
            missing_cnt += 1
            if missing_cnt == k:         # 找到第 k 个缺失的数
                return candidate
        candidate += 1                    # 检查下一个正整数
```

#### 复杂度  
- **时间复杂度**：`O(k + n)`。最坏情况下我们可能要检查到第 `k` 个缺失的数，而 `k` 可能大于 `n`（数组长度），所以整体是 `O(k)`，在本题约束 `k ≤ 1000` 时足够快。  
- **空间复杂度**：`O(n)` 用于把 `arr` 转成集合 `s`，相当于多占用一个数组的空间。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**逐个枚举**，如果 `k` 很大（比如 10⁹）就会超时。  
观察数组 `arr` 已经是严格递增的，我们可以利用**二分查找**在 `log n` 时间内定位答案。  

关键观察：  
- 对于任意下标 `i`（0‑based），`arr[i]` 左侧（不包括 `arr[i]` 本身）本应该出现的正整数个数是 `arr[i] - 1`（因为从 `1` 到 `arr[i]` 共 `arr[i]` 个数，去掉 `arr[i]` 本身剩 `arr[i]-1`）。  
- 实际已经出现的数的个数是 `i + 1`（因为数组前 `i+1` 个元素全部在 `arr` 中）。  
- 因此，**缺失的数量**在位置 `i` 处为 `missing(i) = arr[i] - (i + 1)`。  

如果 `missing(i) < k`，说明第 `k` 个缺失的数在 `arr[i]` 右侧；  
如果 `missing(i) >= k`，说明答案在 `arr[i]` 左侧（包括 `arr[i]` 本身可能就是答案的前一个已知数）。  

于是我们在 `arr` 上做二分查找，找到**第一个**满足 `missing(i) >= k` 的下标 `idx`。  

- 若找不到（即所有 `missing(i) < k`），说明缺失的数都在数组末尾，答案就是 `arr[-1] + (k - missing(last))`。  
- 否则，答案位于 `arr[idx-1]` 与 `arr[idx]` 之间，具体为 `arr[idx-1] + (k - missing(idx-1))`。  

**从零解释二分查找**：把数组想象成一本厚厚的书，想快速定位某一页的大概位置，可以先把书分成两半，看目标在前半还是后半，随后再把对应的那半再分成两半……每次都把搜索范围缩小一半，最多需要 `log₂n` 次比较就能定位。

#### 代码（Python）  
```python
def findKthPositive(arr, k):
    """二分查找 O(log n) 版，返回第 k 个缺失的正整数"""
    n = len(arr)

    # 计算 missing(i) = arr[i] - (i + 1)
    # 二分查找第一个 missing(i) >= k 的位置
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        missing = arr[mid] - (mid + 1)

        if missing < k:          # 第 k 个缺失数在右侧
            left = mid + 1
        else:                    # 在左侧（包括 mid 本身）
            right = mid - 1

    # 循环结束时，right < left
    # right 指向最后一个 missing(right) < k 的位置
    # left 指向第一个 missing(left) >= k 的位置（可能等于 n）

    if left == n:                # 所有 missing 都小于 k，答案在数组末尾
        # arr[-1] 已经出现，缺少的还剩 k - missing(last) 个
        return arr[-1] + (k - (arr[-1] - n))
    else:
        # 答案在 arr[left-1] 与 arr[left] 之间
        # missing(left-1) < k，所以需要再补 k - missing(left-1) 个数
        missing_before = arr[left - 1] - left   # 因为 left-1 + 1 = left
        return arr[left - 1] + (k - missing_before)
```

#### 复杂度  
- **时间复杂度**：`O(log n)`。二分查找每次把搜索区间减半，最多进行 `log₂n` 次比较。相比暴力的 `O(k)`，在 `k` 很大时优势显著。  
- **空间复杂度**：`O(1)`。只用了若干个整数变量，没有额外的数组或递归栈。  

---

## 心得  

- **核心技巧**：利用已排序数组的“缺失计数”公式 `arr[i] - (i+1)`，配合二分查找快速定位第 `k` 个缺失数。  
- **适用的题型**：  
  1. “Missing Number” 系列（如第 K 个缺失的正整数、缺失的最小正整数）。  
  2. “在排序数组中寻找第一个满足条件的元素” （如寻找第一个大于等于目标的数）。  
  3. “数组前缀统计 + 二分” 类问题（如前缀和 >= target）。  
- **一句话总结**：把“缺了多少”转化为可直接比较的数值，用二分把搜索空间压到对数级。

---

## 反思  

- **第一反应**：看到“缺失的正整数”，自然想到逐个枚举并计数。  
- **最容易踩的坑**：  
  - 忘记处理 **数组全部元素缺失数仍不足 k** 的情况，需要在数组末尾继续往后算。  
  - 计算 `missing(i)` 时的下标偏移容易出错（`i+1` 与 `i` 的区别）。  
  - 二分结束后 `left` 与 `right` 的关系要弄清楚，防止越界。  
- **下次类似题的第一步**：先写出**单调函数**（如缺失数量随下标单调递增），判断是否可以二分搜索，然后再推导出对应的公式。