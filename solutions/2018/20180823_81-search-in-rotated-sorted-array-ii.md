# #81. 搜索旋转排序数组 II / Search in Rotated Sorted Array II

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/)

---

## 题目（英文原版）

**Description**

There is an integer array nums sorted in non-decreasing order (not necessarily with distinct values).
Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4].
Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums.
You must decrease the overall operation steps as much as possible.
Follow up: This problem is similar to Search in Rotated Sorted Array, but nums may contain duplicates. Would this affect the runtime complexity? How and why?

**Examples**

**Example 1:**

```
Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true
```

**Example 2:**

```
Input: nums = [2,5,6,0,0,1,2], target = 3
Output: false
```

**Constraints**

- 1 <= nums.length <= 5000
- -104 <= nums[i] <= 104
- nums is guaranteed to be rotated at some pivot.
- -104 <= target <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其原本按非递减顺序（non‑decreasing order）排序（不一定所有元素互不相同）。在传入你的函数之前，`nums` 会在一个未知的枢轴索引 `k`（0 ≤ k < nums.length）处被旋转，使得得到的数组为  

```
[nums[k], nums[k+1], ..., nums[n‑1], nums[0], nums[1], ..., nums[k‑1]]
```  

（0 索引）。例如，`[0,1,2,4,4,4,5,6,6,7]` 可能在枢轴索引 5 处被旋转，变成 `[4,5,6,6,7,0,1,2,4,4]`。

给定旋转后的数组 `nums` 与整数 `target`，如果 `target` 在 `nums` 中则返回 `true`，否则返回 `false`。要求尽可能降低整体的操作步数。

**示例 1**  

**示例 2**  

**约束条件**  

- 1 ≤ nums.length ≤ 5000  
- -10⁴ ≤ nums[i] ≤ 10⁴  
- `nums` 必定在某个枢轴处被旋转  
- -10⁴ ≤ target ≤ 10⁴  

**进阶**：本题与 *Search in Rotated Sorted Array* 类似，但 `nums` 可能包含重复元素。这会影响运行时复杂度吗？如何以及为什么？

---

### 示例

**示例 1**  
```
Input: nums = [2,5,6,0,0,1,2], target = 0
Output: true
```

**示例 2**  
```
Input: nums = [2,5,6,0,0,1,2], target = 3
Output: false
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把数组从头到尾全部遍历一遍，看到哪个元素等于 `target` 就返回 `True`，遍历结束仍未找到则返回 `False`。  

- **使用的数据结构**：只需要原数组本身和一个循环计数器。可以把遍历想象成在超市里把每件商品逐个检查是否是我们要找的商品，虽然慢，但最保险。  
- **为什么正确**：因为我们把每一个位置都检查了一遍，若目标真的在数组里，必然会在某一次比较时被发现；若不在，则所有位置都不相等，最终返回 `False`。  

#### 代码（Python）

```python
def search(nums, target):
    """
    暴力遍历：逐个检查是否等于 target
    """
    for i, num in enumerate(nums):          # enumerate 同时得到下标 i 和元素 num
        # 如果找到了直接返回 True
        if num == target:
            # print(f"在下标 {i} 处找到了目标 {target}")
            return True
    # 循环结束仍未找到，说明不存在
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - “O(n)” 可以理解为「随着数组长度 n 增大，最多要检查 n 次」。最坏情况下（目标不在数组里），我们要遍历全部 `n` 个元素。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（循环计数器 `i`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要检查所有元素**。这道题的数组虽然被旋转了，但仍然保留了「局部有序」的特性：  
- 在没有重复元素的情况下，二分查找可以把搜索区间每次缩小一半。  
- 这里出现了 **重复元素**，会导致「左右两端的值相等」的情况，使我们无法直接判断哪一半是有序的。  

**优化的关键步骤**：

1. **二分搜索的基本框架**  
   - 设 `left`、`right` 为当前搜索区间的左右端点。每次取中点 `mid = (left + right) // 2`。  
   - 若 `nums[mid] == target`，直接返回 `True`。

2. **判断哪一半是有序的**  
   - 正常情况下（没有重复），如果 `nums[left] <= nums[mid]`，说明左半边是有序的；否则右半边有序。  
   - 有了重复元素后，可能出现 `nums[left] == nums[mid] == nums[right]`，此时我们 **无法判断** 哪边有序，因为两个端点的值相同，区间可能跨越旋转点。

3. **遇到相等时的退化处理**  
   - 当 `nums[left] == nums[mid] == nums[right]`，只能 **线性收缩** 区间：`left += 1`，`right -= 1`。这一步的代价是 `O(1)`，但最坏情况下会退化为 `O(n)`（所有元素都相同），这也是题目要求的「最坏情况仍然是线性」的原因。

4. **利用有序段进行剪枝**  
   - 如果左半边有序且 `target` 落在 `[nums[left], nums[mid])` 区间，就把搜索范围缩小到左半边 `right = mid - 1`；否则搜索右半边 `left = mid + 1`。  
   - 右半边有序时同理。

下面用一个形象的类比帮助理解：  
把数组想象成一条**环形跑道**，跑道上标有数字。我们站在 `left` 位置，想找 `target`。如果我们能确定从 `left` 到 `mid` 这段跑道的数字是递增的（像普通跑道），我们就可以判断 `target` 是否在这段路上，从而决定往哪边跑。如果跑道两端的数字相同，说明我们站在一个“雾区”，看不清前方是否递增，只能小步前进（`left += 1`）来尝试走出雾区。

#### 代码（Python）

```python
def search(nums, target):
    """
    二分搜索 + 处理重复元素的特殊情况
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2          # 取中点

        # 直接命中
        if nums[mid] == target:
            return True

        # -------------------------------------------------
        # 1️⃣ 当左、右、mid 三个位置的值相等时，无法判断有序区间
        #    只能把搜索区间收缩，等价于“跳出雾区”
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
            continue

        # -------------------------------------------------
        # 2️⃣ 判断左半边是否有序
        if nums[left] <= nums[mid]:        # 注意这里用 <=，因为左端点可能等于 mid
            # 左半边有序，检查 target 是否在左半边
            if nums[left] <= target < nums[mid]:
                right = mid - 1            # 把搜索范围限制到左半边
            else:
                left = mid + 1             # 否则去右半边继续找
        else:
            # -------------------------------------------------
            # 3️⃣ 左半边无序，说明右半边一定是有序的
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    # 循环结束仍未找到
    return False
```

#### 复杂度  

- **时间复杂度**：`O(log n)` **平均情况**，`O(n)` **最坏情况**。  
  - 平均情况下，数组中重复元素不多，我们每次都能确定有序段，搜索区间会像普通二分一样每次减半，时间就是 `log₂ n`（对数），可以想象成「每次把问题规模砍掉一半」的速度。  
  - 最坏情况下（比如全部元素相同且不等于 target），我们每次只能把 `left`、`right` 各收缩 1，等价于线性遍历，时间退化为 `O(n)`。这也是出现重复元素时二分法不可避免的限制。

- **空间复杂度**：`O(1)`。只用了几个整数指针 `left、right、mid`，不随数组大小增长。

---

## 心得

- **核心技巧**：在旋转数组中利用「有序区间」进行二分搜索；遇到重复元素导致无法判断有序区间时，用线性收缩来跳出模糊区间。  
- **适用的题型**  
  1. `Search in Rotated Sorted Array`（无重复元素）  
  2. `Find Minimum in Rotated Sorted Array`（寻找旋转数组最小值）  
  3. `Find Peak Element`（利用单调性进行二分）  
- **一句话总结解题钥匙**：**先二分定位有序段，若两端相等则一步步“扫除雾气”。**

---

## 反思

- **第一反应**：看到“旋转有序数组”，立刻想到二分搜索；但一看到“可能有重复”，就担心传统二分的判断条件会失效。  
- **最容易踩的坑**  
  1. **相等判断写成 `nums[left] < nums[mid]`**，导致在 `left == mid` 时错误地认为左半边无序。  
  2. **忘记在 `nums[left] == nums[mid] == nums[right]` 时收缩两端**，会出现死循环。  
  3. **边界条件**：`left <= right` 而不是 `<`，否则会漏掉最后一个元素。  
- **下次遇到同类题的第一步**：先判断是否存在“无法比较的相等情形”，若有则准备好线性收缩的退化处理；随后再按照普通二分的思路划分有序区间。