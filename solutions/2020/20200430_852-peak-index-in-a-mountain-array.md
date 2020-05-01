# #852. 山脉数组中的峰值索引 / Peak Index in a Mountain Array

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/peak-index-in-a-mountain-array/)

---

## 题目（英文原版）

**Description**

You are given an integer mountain array arr of length n where the values increase to a peak element and then decrease.
Return the index of the peak element.
Your task is to solve it in O(log(n)) time complexity.

**Examples**

**Example 1:**

```
Input: arr = [0,1,0]
Output: 1
```

**Example 2:**

```
Input: arr = [0,2,1,0]
Output: 1
```

**Example 3:**

```
Input: arr = [0,10,5,2]
Output: 1
```

**Constraints**

- 3 <= arr.length <= 105
- 0 <= arr[i] <= 106
- arr is guaranteed to be a mountain array.

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数山脉数组（mountain array） `arr`，其中数组的数值先递增至一个峰值元素（peak element），随后递减。  
返回该峰值元素的索引。  
要求使用 `O(log(n))` 的时间复杂度完成。

## 示例

### 示例 1
**输入**: `arr = [0,1,0]`  
**输出**: `1`

### 示例 2
**输入**: `arr = [0,2,1,0]`  
**输出**: `1`

### 示例 3
**输入**: `arr = [0,10,5,2]`  
**输出**: `1`

## 约束条件
- `3 <= arr.length <= 10^5`
- `0 <= arr[i] <= 10^6`
- `arr` 保证是一个山脉数组（mountain array）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**顺序遍历**整个数组，找到满足“左边比它小、右边也比它小”的元素——这就是峰值。  
- **使用的数据结构**：只需要原数组本身，遍历时用两个指针`i-1`和`i+1`来查看左右邻居。可以把数组想象成一排山坡上的标记，站在第`i`个标记上，左边和右边的标记如果都比自己低，那我们就在峰顶了。  
- **为什么正确**：题目已经保证数组一定是“先上升后下降”的山形，也就是说必然只有一个峰。遍历到峰时左边一定比它小，右边也一定比它小，满足条件即可返回。  

#### 代码（Python）

```python
def peakIndexInMountainArray(arr):
    """
    暴力遍历寻找峰值
    :param arr: List[int] 山形数组
    :return: int 峰值的下标
    """
    n = len(arr)
    # 从下标 1 开始，因为峰不可能出现在最左边
    for i in range(1, n - 1):
        # 判断左、右两个相邻元素是否都比当前元素小
        if arr[i - 1] < arr[i] and arr[i] > arr[i + 1]:
            return i          # 找到峰，直接返回下标
    # 按题意一定会有答案，下面这行理论上永远不会执行
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 需要一次遍历，最坏情况下要检查所有 `n` 个元素。可以把 `O(n)` 想象成“随数组长度线性增长”，数组长度翻倍，时间也会大约翻倍。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（`i、n`），不随输入规模增大而增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每个元素都要检查一次**，时间是线性的。  
观察山形数组的特性：左侧是严格递增，右侧是严格递减。  
如果我们任选一个中间位置 `mid`：

- 若 `arr[mid] < arr[mid + 1]`，说明我们还在**上升段**，峰一定在 `mid` 的右侧。  
- 若 `arr[mid] > arr[mid + 1]`，说明我们已经进入**下降段**，峰要么是 `mid`，要么在 `mid` 的左侧。

这正好符合**二分查找**的思路：每次都可以把搜索区间砍掉一半，直至收敛到峰的位置。  
二分查找的核心是**不断比较相邻两个元素的大小**，不需要额外的数据结构，只用两个指针 `left`、`right` 来限定搜索范围。

> 类比：把山峰想象成一条路上的最高点，你站在路中间向左看比右高，说明最高点在右边；向右看更高，说明最高点在左边。每次都把不可能的那边抛掉，最后只剩下最高点。

#### 代码（Python）

```python
def peakIndexInMountainArray(arr):
    """
    二分查找找到山峰下标，时间 O(log n)
    :param arr: List[int] 山形数组
    :return: int 峰值的下标
    """
    left, right = 0, len(arr) - 1          # 初始化搜索区间
    while left < right:                    # 当区间长度大于 1 时继续
        mid = (left + right) // 2          # 取区间中点（整数除法）
        # 判断 mid 与其右邻居的大小关系
        if arr[mid] < arr[mid + 1]:
            # 仍在上升段，峰在右侧，排除左半部分（包括 mid）
            left = mid + 1
        else:
            # 已经在下降段，峰在左侧或正好是 mid，保留 mid
            right = mid
    # 循环结束时 left == right，指向峰值下标
    return left
```

#### 复杂度  

- **时间复杂度**：`O(log n)` —— 每次循环把搜索区间长度减半，类似每次把一条长绳子对折。对数复杂度可以理解为“即使数组有上百万个元素，循环也只会进行大约 20 次”。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量 `left、right、mid`，不随输入规模增长。

---

## 心得

- **核心技巧**：利用**单调性**（左侧递增、右侧递减）配合**二分查找**快速定位峰值。  
- **适用的题型**：  
  1. “寻找有序数组中的目标”类（经典二分查找）。  
  2. “单调函数的零点/极值”类，如 LeetCode 1095 *Find in Mountain Array*、1629 *Slowest Key*（在单调递增的时间戳中二分）。  
- **一句话总结解题钥匙**：**用相邻元素的大小关系把“上升段”和“下降段”分开，二分逼近唯一的峰**。

## 反思

- **第一反应**：直接遍历找峰，想到二分查找是因为题目要求 `O(log n)`，于是审视数组的单调结构。  
- **最容易踩的坑**：  
  - **边界访问**：`mid + 1` 必须在数组范围内，所以循环条件使用 `left < right` 而不是 `<=`，并且 `right` 初始设为 `len(arr) - 1`（而不是 `len(arr) - 2`）。  
  - **相等情况**：题目保证严格递增/递减，所以不存在 `arr[mid] == arr[mid+1]` 的情况；若遇到非严格山形，需要额外处理。  
- **下次类似题的第一步**：先确认**单调区间**（上升/下降、递增/递减），然后思考**如何用二分把区间逐步缩小**。  

祝你在算法的山路上越走越高！ 🚀