# #1095. 在山脉数组中查找 / Find in Mountain Array

> 难度：困难 · 标签：Array、Binary Search、Interactive · [LeetCode 链接](https://leetcode.com/problems/find-in-mountain-array/)

---

## 题目（英文原版）

**Description**

(This problem is an interactive problem.)
You may recall that an array arr is a mountain array if and only if:
Given a mountain array mountainArr, return the minimum index such that mountainArr.get(index) == target. If such an index does not exist, return -1.
You cannot access the mountain array directly. You may only access the array using a MountainArray interface:
Submissions making more than 100 calls to MountainArray.get will be judged Wrong Answer. Also, any solutions that attempt to circumvent the judge will result in disqualification.

**Examples**

**Example 1:**

```
Input: mountainArr = [1,2,3,4,5,3,1], target = 3
Output: 2
Explanation: 3 exists in the array, at index=2 and index=5. Return the minimum index, which is 2.
```

**Example 2:**

```
Input: mountainArr = [0,1,2,4,2,1], target = 3
Output: -1
Explanation: 3 does not exist in the array, so we return -1.
```

**Constraints**

- 3 <= mountainArr.length() <= 104
- 0 <= target <= 109
- 0 <= mountainArr.get(index) <= 109

---

## 题目（中文翻译）

**描述**  
（本题为交互式（interactive）题目。）  
你可能已经了解，若且仅若数组 `arr` 满足以下条件，则称其为**山脉数组（mountain array）**：  
- `arr.length >= 3`  
- 存在某个索引 `i`（`0 < i < arr.length - 1`），使得 `arr[0] < arr[1] < … < arr[i‑1] < arr[i]` 且 `arr[i] > arr[i+1] > … > arr[arr.length‑1]`  

给定一个山脉数组 `mountainArr`，返回满足 `mountainArr.get(index) == target` 的**最小索引**。如果不存在这样的索引，返回 `-1`。

**注意**  
- 你不能直接访问整个数组，只能通过 `MountainArray` 接口的 `get(index)` 方法读取单个元素。  
- 若调用 `MountainArray.get` 的次数超过 **100 次**，提交将被判为 **Wrong Answer**。  
- 任何试图规避判题系统的行为都将导致 **disqualification**（取消资格）。

**示例**

*示例 1*  
```
Input: mountainArr = [1,2,3,4,5,3,1], target = 3
Output: 2
Explanation: 3 在数组中出现，两次，分别位于索引 2 和索引 5。返回最小的索引 2。
```

*示例 2*  
```
Input: mountainArr = [0,1,2,4,2,1], target = 3
Output: -1
Explanation: 数组中不存在 3，故返回 -1。
```

**约束条件**  
- `3 <= mountainArr.length() <= 10^4`  
- `0 <= target <= 10^9`  
- `0 <= mountainArr.get(index) <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是把整座“山”都遍历一遍，看到哪个下标的值等于 `target` 就返回。  
- **使用的数据结构**：只需要一个普通的 Python 列表（或题目提供的 `MountainArray` 接口）来顺序访问每个元素。可以把它想象成 **一本顺序翻页的相册**，我们从第 0 页翻到最后一页，逐页检查是否是想找的那张照片。  
- **为什么正确**：因为我们检查了每一个可能的下标，若目标值真的在数组里，一定会被找到；若不在，遍历完后自然返回 `-1`。  
- **复杂度分析**：  
  - 时间复杂度是 **O(n)**，这里的 `n` 是山的长度。大白话说，就是“我们最多要看一次山的每一块”。  
  - 空间复杂度是 **O(1)**，只用了常数级的额外变量（比如 `i`、`ans`），不随 `n` 增长。

> **注意**：在真实交互题目里，`MountainArray.get` 的调用次数被限制在 100 次以内，而线性遍历会调用 `n` 次（最多 10⁴），所以这个暴力解在正式提交时会被判为 **Wrong Answer**。它仅用来帮助我们理清最基本的正确性。

#### 代码（Python）  

```python
# 这里的 MountainArray 只是一种“只能用 get(i) 取值”的包装，
# 为了演示我们把它实现成普通列表的封装。
class MountainArray:
    def __init__(self, nums):
        self.nums = nums
    
    def get(self, index: int) -> int:
        return self.nums[index]
    
    def length(self) -> int:
        return len(self.nums)


def findInMountainArray_bruteforce(target: int, mountainArr: MountainArray) -> int:
    """线性遍历所有下标，找到最小的 target 位置"""
    n = mountainArr.length()
    for i in range(n):
        # 每次都要通过接口取值，等价于翻一页相册
        if mountainArr.get(i) == target:
            return i                # 找到第一个就是最小下标
    return -1                       # 整座山都没找到
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 需要检查每一个位置，最坏情况下要看 `n` 次。  
- **空间复杂度**：`O(1)` —— 只用了几个局部变量，额外空间不随 `n` 增长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**我们只需要在山的两侧各搜索一次**，不必把整座山都遍历。  
山的结构有三个明显的区间：

1. **左上坡**：`A[i-1] < A[i]`，单调递增。  
2. **峰顶**：`A[i-1] < A[i] > A[i+1]`，是最高点。  
3. **右下坡**：`A[i-1] > A[i]`，单调递减。  

如果我们先**找到峰顶的下标**，就可以把问题拆成两个**单调数组**的二分查找：

- **左侧**：递增数组 → 标准二分查找（小的在左，大的在右）。  
- **右侧**：递减数组 → 只需要把比较方向反过来（大值在左，小值在右），同样是二分。  

二分查找的核心思想是 **“每次把搜索区间砍掉一半”**，所以只需要 `log₂ n` 次查询就能定位目标。  

**关键点一：找峰顶**  
我们可以在整个山上做一次二分搜索。设 `mid = (l + r) // 2`，比较 `mid` 与 `mid+1` 的大小：

- 若 `mountainArr.get(mid) < mountainArr.get(mid+1)`，说明我们在左上坡，峰在右侧 → `l = mid + 1`。  
- 否则（`>=`），说明我们在峰或右下坡，峰在左侧或就是 `mid` → `r = mid`。  

循环结束时 `l == r`，即为峰顶下标。

**关键点二：在两侧二分**  

左侧二分（递增）：

```text
while l <= r:
    mid = (l + r) // 2
    val = get(mid)
    if val == target: return mid
    elif val < target: l = mid + 1
    else: r = mid - 1
```

右侧二分（递减）：

```text
while l <= r:
    mid = (l + r) // 2
    val = get(mid)
    if val == target: return mid
    elif val > target: l = mid + 1   # 这里方向反了
    else: r = mid - 1
```

**为什么总调用次数 ≤ 100**  
- 找峰顶的二分最多 `log₂ n` 次（`n ≤ 10⁴`，约 14 次）。  
- 左侧二分再 `log₂ n` 次，右侧二分同理。  
- 合计不超过 `3 * log₂ 10⁴ ≈ 42` 次，远小于 100 次的限制。

#### 代码（Python）  

```python
class MountainArray:
    """题目提供的交互式接口的简化实现（仅用于本地测试）"""
    def __init__(self, nums):
        self.nums = nums
    
    def get(self, index: int) -> int:
        return self.nums[index]
    
    def length(self) -> int:
        return len(self.nums)


def findPeak(mountainArr: MountainArray) -> int:
    """二分找峰顶下标"""
    left, right = 0, mountainArr.length() - 1
    while left < right:                     # 注意是 < 而不是 <=
        mid = (left + right) // 2
        # 与右邻居比较，判断在上坡还是下坡
        if mountainArr.get(mid) < mountainArr.get(mid + 1):
            left = mid + 1                   # 峰在右边
        else:
            right = mid                      # 峰在左边或就是 mid
    return left                              # left == right，此时指向峰顶


def binarySearch(mountainArr: MountainArray, target: int,
                 left: int, right: int, asc: bool) -> int:
    """
    在 [left, right] 区间做二分查找。
    asc = True 表示递增序列，False 表示递减序列。
    若找到返回下标，否则返回 -1。
    """
    while left <= right:
        mid = (left + right) // 2
        val = mountainArr.get(mid)
        if val == target:
            return mid
        if asc:                               # 递增序列
            if val < target:
                left = mid + 1
            else:
                right = mid - 1
        else:                                 # 递减序列，比较方向相反
            if val > target:
                left = mid + 1
            else:
                right = mid - 1
    return -1


def findInMountainArray(target: int, mountainArr: MountainArray) -> int:
    """
    主函数：先找峰，再分别在左侧（递增）和右侧（递减）二分。
    返回最小的目标下标，若不存在返回 -1。
    """
    n = mountainArr.length()
    peak = findPeak(mountainArr)              # 第一次二分，找到峰

    # 1）左侧递增区间 [0, peak]
    idx = binarySearch(mountainArr, target, 0, peak, asc=True)
    if idx != -1:
        return idx                            # 已经是最左侧的下标

    # 2）右侧递减区间 [peak+1, n-1]
    return binarySearch(mountainArr, target, peak + 1, n - 1, asc=False)
```

#### 复杂度  

- **时间复杂度**：`O(log n)`  
  - 找峰顶 `log n` 次查询，左侧二分 `log n` 次，右侧二分 `log n` 次，总共不超过 `3·log n`。  
  - 大白话：**每次我们都把搜索范围缩小一半，最多只需要几次“翻页”就能定位目标**。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个局部变量（`left, right, mid, val`），不随数组长度增长。  

---  

## 心得  

- **核心技巧**：**利用数组的单调性进行二分搜索**（先定位峰点，再在递增/递减子数组中二分）。  
- **适用的题型**  
  1. “山脉数组”类题目（如本题）。  
  2. “先升后降”或“先降后升”的数组搜索（例如寻找峰值、寻找最小峰值等）。  
  3. 需要在**单调区间**快速定位的场景（比如在有序旋转数组中搜索）。  
- **一句话总结解题钥匙**：**先把整体结构拆成单调的两段，再用二分把每段快速砍掉一半**。  

---  

## 反思  

- **拿到题目第一反应**：先想到“山的形状是先上升后下降”，于是想先找最高点，再分别搜索两侧。  
- **最容易踩的坑**  
  - **调用次数限制**：忘记 `MountainArray.get` 只能调用 100 次，导致使用线性遍历被判 WA。  
  - **右侧是递减的**：在右侧二分时忘记把比较符号反过来，会导致永远找不到目标。  
  - **边界条件**：峰可能在数组的第一个或最后一个位置（虽然题目保证山的长度 ≥ 3），实现时要确保 `mid+1` 不越界。  
- **下次遇到同类题的第一步**：**先判断数组是否有单调子区间（如峰点），用二分定位该分界点，再分别在每个单调区间做二分搜索**。