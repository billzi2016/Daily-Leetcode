# #33. 搜索旋转排序数组 / Search in Rotated Sorted Array

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/search-in-rotated-sorted-array/)

---

## 题目（英文原版）

**Description**

There is an integer array nums sorted in ascending order (with distinct values).
Prior to being passed to your function, nums is possibly rotated at an unknown pivot index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].
Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.
You must write an algorithm with O(log n) runtime complexity.

**Examples**

**Example 1:**

```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

**Example 2:**

```
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

**Example 3:**

```
Input: nums = [1], target = 0
Output: -1
```

**Constraints**

- 1 <= nums.length <= 5000
- -104 <= nums[i] <= 104
- All values of nums are unique.
- nums is an ascending array that is possibly rotated.
- -104 <= target <= 104

---

## 题目（中文翻译）

存在一个整数数组（integer array）`nums`，该数组按升序（ascending order）排列，且所有值均唯一（distinct values）。

在传入函数之前，数组可能在未知的枢轴索引 `k`（`1 <= k < nums.length`）处被旋转，使得得到的数组为  
`[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`（0-indexed）。例如，数组 `[0,1,2,4,5,6,7]` 可以在枢轴索引 `3` 处旋转后变为 `[4,5,6,7,0,1,2]`。

给定可能已经旋转后的数组 `nums` 和一个整数 `target`，返回 `target` 在 `nums` 中的索引；如果不存在则返回 `-1`。

你必须设计一个时间复杂度为 **O(log n)** 的算法（runtime complexity）。

### 示例

**示例 1**  
输入: `nums = [4,5,6,7,0,1,2]`, `target = 0`  
输出: `4`

**示例 2**  
输入: `nums = [4,5,6,7,0,1,2]`, `target = 3`  
输出: `-1`

**示例 3**  
输入: `nums = [1]`, `target = 0`  
输出: `-1`

### 约束条件
- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- 所有 `nums` 的值互不相同。
- `nums` 是一个可能已经旋转的升序数组。
- `-10^4 <= target <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把整个数组从头到尾一次遍历，和 `target` 做比较，找到就返回下标，找不到就返回 `-1`。  
这里用到的数据结构只有 **列表（list）** 本身，遍历它就像在超市的货架上顺序挑商品：从左到右一个一个看，看到想要的就停下来。

这种方法之所以一定能得到正确答案，是因为题目保证数组里没有重复元素，只要把每个位置都检查一遍，就一定不会漏掉目标值。

#### 代码（Python）

```python
def search_brute(nums, target):
    """
    暴力线性搜索
    :param nums: List[int] 已经可能被旋转的升序数组
    :param target: int 要查找的目标值
    :return: int 目标所在的下标，若不存在返回 -1
    """
    for i, num in enumerate(nums):          # enumerate 同时拿到下标 i 和元素 num
        if num == target:                    # 找到目标
            return i
    return -1                                # 遍历完都没找到
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  这里的 `n` 是数组长度。大白话说就是“最坏情况下要看 `n` 次”，如果数组有 1000 个元素，就可能要检查 1000 次。

- **空间复杂度：** `O(1)`  
  只用了常数级的额外变量（`i`、`num`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要从头遍历**，时间是线性的。  
我们要把时间压到 `O(log n)`，这正是 **二分查找** 能做到的——每一步把搜索区间砍掉一半。

普通的二分查找要求数组是**整体有序**的，但这里的数组被旋转了，整体已经不是单调的了。  
关键在于：**即使整体被旋转，任意时刻左半段或右半段必定是有序的**（因为只在一个位置“断开”）。  

思路步骤：

1. 设 `lo = 0, hi = len(nums) - 1`，循环 `while lo <= hi`。  
2. 取中点 `mid = (lo + hi) // 2`。  
3. 如果 `nums[mid] == target`，直接返回 `mid`。  
4. 判断哪一侧是有序的：  
   - 如果 `nums[lo] <= nums[mid]`，说明左半段 `[lo, mid]` 是有序的。  
   - 否则，右半段 `[mid, hi]` 是有序的。  
5. 根据目标值所在的区间，决定下一步在有序段的左侧还是右侧继续二分：  
   - **左半段有序**且 `target` 落在 `[nums[lo], nums[mid])` 之间 → 把搜索区间缩小到左半段：`hi = mid - 1`。  
   - 否则 → 目标在右半段（可能是无序的那段），把左边界往右推：`lo = mid + 1`。  
   - 同理处理右半段有序的情况。  

通过每次比较“哪边有序 + 目标是否落在有序区间”，我们能够像普通二分一样把搜索范围减半，最终在 `O(log n)` 步内找到目标或确认不存在。

> **类比**：想象你在一条环形跑道上找一个特定的标记。跑道上只有一段是连续递增的（比如颜色从浅到深），你先确定这段在哪，然后判断目标颜色是否在这段里。如果在，就沿这段继续找；不在，就直接跳到另一段继续搜索。每次都把可选的范围缩小一半。

#### 代码（Python）

```python
def search(nums, target):
    """
    在可能被旋转的有序数组中使用二分查找寻找 target
    :param nums: List[int] 旋转后的升序数组，元素唯一
    :param target: int 待查找的数值
    :return: int 目标下标，若不存在返回 -1
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2               # 取中点
        if nums[mid] == target:            # 正好命中
            return mid

        # 判断左半段是否有序
        if nums[lo] <= nums[mid]:          # 左半段有序
            # target 落在有序的左半段范围内
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1                # 缩小到左半段
            else:
                lo = mid + 1                # 目标在右半段（可能是无序的）
        else:                               # 右半段有序
            # target 落在有序的右半段范围内
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1                # 缩小到右半段
            else:
                hi = mid - 1                # 目标在左半段

    return -1                               # 循环结束仍未找到
```

#### 复杂度  

- **时间复杂度：** `O(log n)`  
  每次循环把搜索区间长度减半，类似把一根绳子不断折半，最多需要 `log₂ n` 次比较。比如 `n = 1024`，最多只需要约 10 次。

- **空间复杂度：** `O(1)`  
  只用了几个整数变量 `lo、hi、mid`，不随输入规模增长。

---

## 心得

- **核心技巧**：在**旋转有序数组**中利用“任意时刻至少有一侧是有序的”这一性质，结合**二分查找**实现 `O(log n)` 的搜索。  
- **适用的题型**：  
  1. *Search in Rotated Sorted Array II*（允许重复元素，需要稍微改动判断）。  
  2. *Find Minimum in Rotated Sorted Array*（寻找旋转数组的最小值）。  
  3. *Find Peak Element*（利用单调性定位峰值）。  
- **一句话总结**：**先定位有序区间，再把目标锁进有序区间的二分**，就是这道题的解题钥匙。

---

## 反思

- **第一反应**：看到“数组已经排序但被旋转”，立刻想到普通二分失效，需要先“恢复”有序状态或另辟蹊径。  
- **最容易踩的坑**：  
  - 判断左/右半段是否有序时要使用 `<=`（包括相等），否则在极端情况下（如只有两个元素）会误判。  
  - 当 `target` 正好在断点两侧时，容易忘记把搜索区间向另一侧移动，导致死循环。  
  - 边界条件 `lo == hi` 时仍需检查一次，否则会漏掉唯一元素的情况。  
- **下次遇到同类题的第一步**：**先确认哪一半是有序的**，然后利用有序性的比较把搜索范围缩小，这一步几乎是所有“旋转/部分有序”二分题的通用起点。