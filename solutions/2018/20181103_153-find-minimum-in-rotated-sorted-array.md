# #153. 寻找旋转有序数组中的最小值 / Find Minimum in Rotated Sorted Array

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

---

## 题目（英文原版）

**Description**

Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:
Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].
Given the sorted rotated array nums of unique elements, return the minimum element of this array.
You must write an algorithm that runs in O(log n) time.

**Examples**

**Example 1:**

```
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.
```

**Example 2:**

```
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.
```

**Example 3:**

```
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times.
```

**Constraints**

- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers of nums are unique.
- nums is sorted and rotated between 1 and n times.

---

## 题目（中文翻译）

假设一个长度为 `n` 的数组原本按升序排序，随后被旋转了 1 到 `n` 次。例如，数组 `nums = [0,1,2,4,5,6,7]` 可能会变为：

> 注意，将数组 `[a[0], a[1], a[2], ..., a[n-1]]` 旋转 1 次会得到 `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`。

给定一个已旋转且元素唯一的有序数组 `nums`，返回该数组中的最小元素。你必须设计一个时间复杂度为 **O(log n)** 的算法。

### 示例

**示例 1**  
输入: `nums = [3,4,5,1,2]`  
输出: `1`  
解释: 原数组为 `[1,2,3,4,5]`，旋转了 3 次。

**示例 2**  
输入: `nums = [4,5,6,7,0,1,2]`  
输出: `0`  
解释: 原数组为 `[0,1,2,4,5,6,7]`，旋转了 4 次。

**示例 3**  
输入: `nums = [11,13,15,17]`  
输出: `11`  
解释: 原数组为 `[11,13,15,17]`，旋转了 4 次。

### 约束条件

- `n == nums.length`
- `1 <= n <= 5000`
- `-5000 <= nums[i] <= 5000`
- `nums` 中的所有整数互不相同
- `nums` 已经排序并旋转了 1 到 `n` 次

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把数组从头到尾逐个检查，找到最小的那个数。  
- **用到的数据结构**：普通的 Python 列表（list），相当于我们生活中的“装东西的盒子”，里面可以顺序放很多数字。  
- **为什么正确**：因为题目保证数组里所有元素都是唯一的，只要把每个元素都和当前最小值比较一次，最终留下的就是全局最小值。  
- **时间/空间复杂度**：  
  - 我们要遍历 **n** 次（`n` 为数组长度），每一次只做常数时间的比较，所以时间复杂度是 **O(n)**。  
    - “O(n)” 可以想象成“走 n 步”。如果数组有 1000 个元素，就要走 1000 步。  
  - 只用了几个额外的变量（`min_val`、索引），空间复杂度是 **O(1)**，即“常数级”，不随数组大小变化。

#### 代码（Python）

```python
def findMin_bruteforce(nums):
    """
    暴力遍历整个数组，找最小值
    """
    # 先把第一个元素当成最小值
    min_val = nums[0]                     # 初始化最小值

    # 从第二个元素开始依次比较
    for i in range(1, len(nums)):
        if nums[i] < min_val:             # 如果当前元素更小
            min_val = nums[i]             # 更新最小值

    return min_val
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 需要检查每一个元素，等价于走 n 步。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历整个数组**，当数组很大时会浪费很多时间。  
观察题目可以发现：

1. 原始数组是 **严格递增** 的，旋转后仍保持局部递增，只是在某一点会出现 “断层”。  
2. 断层左边的所有元素 **都大于** 数组的第一个元素，右边的所有元素 **都小于** 第一个元素。  
3. 断层的右侧第一个元素就是整个数组的最小值。

这正好符合 **二分查找**（Binary Search）的使用场景：  
- 每一步都把搜索区间 **平分成两半**，根据某个条件判断最小值一定在左半边还是右半边，从而把不可能的那一半直接丢弃。  
- 由于每次都把区间长度减半，最多只需要 `log₂ n` 次比较，就能定位到最小值，时间复杂度达到 `O(log n)`。

**实现细节**（从零解释）：

| 步骤 | 说明 | 类比 |
|------|------|------|
| 1. 初始化 | `left = 0, right = n-1`，表示当前搜索区间是整个数组。 | 把一根绳子两头固定，左手握住 `left`，右手握住 `right`。 |
| 2. 循环条件 | 当 `left < right` 时继续；当二者相等时，区间只剩一个元素，就是答案。 | 只要左手没碰到右手，就继续往里收。 |
| 3. 取中点 | `mid = (left + right) // 2`（向下取整）。 | 把绳子折成两段，`mid` 就是折点。 |
| 4. 判断方向 | - 若 `nums[mid] > nums[right]`，说明最小值在 `mid` 的右侧（因为右侧的数比 `mid` 小，说明断层在右边）。<br>- 否则，最小值在左侧或正好是 `mid`（因为 `mid` 已经不大于最右端，说明最小值不在 `mid` 右边）。 | 把两个盒子（左半段、右半段）放在天平上比较重量：如果右边更轻（`nums[mid] > nums[right]`），说明最小值在右边。 |
| 5. 缩小区间 | 根据第 4 步的判断，移动 `left` 或 `right` 指针：<br>`left = mid + 1`（右侧）或 `right = mid`（左侧）。 | 把不可能装有最小值的那段绳子松开，只保留可能的那段。 |
| 6. 循环结束 | 循环结束时 `left == right`，指向的就是最小值所在位置。返回 `nums[left]`。 | 两手终于碰在一起，正好握住最小值所在的盒子。 |

#### 代码（Python）

```python
def findMin_binary_search(nums):
    """
    二分查找（O(log n)）寻找旋转数组的最小值
    """
    left, right = 0, len(nums) - 1          # 初始化搜索区间

    # 当搜索区间长度大于 1 时继续
    while left < right:
        mid = (left + right) // 2           # 取中点（向下取整）

        # 关键判断：mid 与 right 位置的值大小关系
        if nums[mid] > nums[right]:
            # 说明最小值在 mid 右侧（断层在右边），排除左侧包括 mid 的区间
            left = mid + 1
        else:
            # 最小值在左侧或正好是 mid，保留左侧区间（包括 mid）
            right = mid

    # 循环结束时 left == right，指向最小值
    return nums[left]
```

#### 复杂度  

- **时间复杂度**：`O(log n)` —— 每次把搜索区间长度减半，类似“每走一步，剩下的路程就只剩一半”。如果数组有 1024 个元素，只需要最多 10 次比较（因为 2¹⁰ = 1024）。  
- **空间复杂度**：`O(1)` —— 只用了固定的几个指针变量 (`left`, `right`, `mid`)，不随数组大小增长。

---

## 心得

- **核心技巧**：利用数组的“有序 + 旋转”特性，结合二分查找快速定位断层（最小值）。  
- **适用的题型**：  
  1. **在有序数组中找目标**（如 “Search in Rotated Sorted Array”）  
  2. **找峰值/谷值**（如 “Find Peak Element”）  
  3. **寻找满足单调性条件的边界**（如 “First Bad Version”）  
- **一句话总结解题钥匙**：**“把数组划分成两段，比较右端值与中点值，丢弃不可能的那一段”。**

---

## 反思

- **第一反应**：看到“旋转”“有序”“最小值”，立刻想到“断层”，于是想到遍历或二分。  
- **最容易踩的坑**：  
  - 当数组根本没有旋转（即最小值就在第一个位置）时，`nums[mid] <= nums[right]` 会一直成立，必须把 `right = mid`（而不是 `right = mid - 1`），否则会错过答案。  
  - 需要使用 `while left < right` 而不是 `while left <= right`，否则会出现无限循环。  
- **下次遇到同类题的第一步**：先确认“有没有单调（递增/递减）+ 某种偏移”，然后思考 **“断点在左还是右”**，据此决定二分的比较方向。