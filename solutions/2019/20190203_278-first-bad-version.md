# #278. 第一个错误的版本 / First Bad Version

> 难度：简单 · 标签：Binary Search、Interactive · [LeetCode 链接](https://leetcode.com/problems/first-bad-version/)

---

## 题目（英文原版）

**Description**

You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.
Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one, which causes all the following ones to be bad.
You are given an API bool isBadVersion(version) which returns whether version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

**Examples**

**Example 1:**

```
Input: n = 5, bad = 4
Output: 4
Explanation:
call isBadVersion(3) -> false
call isBadVersion(5) -> true
call isBadVersion(4) -> true
Then 4 is the first bad version.
```

**Example 2:**

```
Input: n = 1, bad = 1
Output: 1
```

**Constraints**

- 1 <= bad <= n <= 231 - 1

---

## 题目（中文翻译）

你是一名产品经理，正带领团队开发一款新产品。遗憾的是，最新的版本未通过质量检查。由于每个版本都是在前一个版本的基础上开发的，所以一旦出现错误的版本，之后的所有版本也都会出错。

假设你有 `n` 个版本，编号为 `[1, 2, ..., n]`，需要找出第一个错误的版本，即导致后续所有版本都出错的那个版本。

系统提供了一个 API（应用程序编程接口）`bool isBadVersion(version)`，它会返回给定 `version` 是否是错误的。请实现一个函数来寻找第一个错误的版本，并且要 **尽量减少** 对该 API 的调用次数。

**示例 1**

**示例 2**

**约束条件**

- `1 <= bad <= n <= 2^31 - 1`

---

### 示例

#### 示例 1
**输入**: `n = 5, bad = 4`  
**输出**: `4`  
**解释**:  
调用 `isBadVersion(3)` → `false`  
调用 `isBadVersion(5)` → `true`  
调用 `isBadVersion(4)` → `true`  
因此 `4` 是第一个错误的版本。

#### 示例 2
**输入**: `n = 1, bad = 1`  
**输出**: `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是从第 1 版开始，一版一版地检查 `isBadVersion(version)`，  
一旦遇到返回 `True` 的版本，就说明它是第一个坏版本，直接返回。  

- **使用的数据结构**：只需要一个普通的整数变量 `version`，相当于我们手里的一本书的页码，一页一页翻过去，看到错页就停下来。  
- **为什么正确**：题目保证“坏版本”在出现后会一直持续到最后，也就是说版本序列是 **非递减** 的（前面全好，后面全坏）。所以第一个返回 `True` 的版本必然就是我们要找的答案。  
- **时间/空间复杂度**：最坏情况下需要检查所有 `n` 个版本，时间复杂度是 `O(n)`。只用了常数个变量，空间复杂度是 `O(1)`。  
  - 大白话解释：如果 `n = 1,000,000`，我们最差要调用一百万次 API，显然有点慢。  

#### 代码（Python）

```python
# 已知的 API
# def isBadVersion(version: int) -> bool: ...

def firstBadVersion(n: int) -> int:
    """
    暴力线性扫描，从 1 到 n 依次调用 isBadVersion，
    第一次返回 True 的版本就是答案。
    """
    version = 1                     # 从第 1 版开始
    while version <= n:             # 只要还没超过上限就继续
        if isBadVersion(version):   # 调用 API 检查当前版本
            return version          # 找到第一个坏版本，直接返回
        version += 1                # 否则检查下一版
    # 题目保证一定有坏版本，这里理论上不会走到这里
    return -1
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 需要逐个检查，最坏情况要调用 `n` 次 API。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **线性遍历**：每次只能前进一步，导致调用次数和 `n` 成正比。  
观察题目可以发现：  
- 所有版本形成一个 **单调不递减** 的序列（好 → 坏 → 坏 → …）。  
- 只要我们能快速定位“从好变坏的分界点”，就不需要检查每一个版本。

这正好符合 **二分查找**（Binary Search）的使用场景：在一个有序（单调）序列中查找目标位置。  

二分查找的核心是每次把搜索区间缩小一半：

1. 设 `left = 1`（最左边） ，`right = n`（最右边）。  
2. 取中间位置 `mid = left + (right - left) // 2`（防止 `left + right` 溢出）。  
3. 调用 `isBadVersion(mid)`：  
   - 如果 `mid` 版是坏的，说明第一个坏版本一定在 `mid` 或它左边，`right = mid`。  
   - 如果 `mid` 版是好的，说明第一个坏版本一定在 `mid` 右边，`left = mid + 1`。  
4. 循环结束时，`left == right`，此时指向的就是第一个坏版本。

> **类比**：把所有版本想象成排好队的学生，老师要找第一个迟到的学生。  
> 老师不必一个一个检查，只要每次让队伍对半分，让前半部分的学生站出来检查是否全都准时，若有迟到就继续在这半队里二分，否则在后半队里继续二分，最终就能快速定位到第一位迟到的学生。

#### 代码（Python）

```python
# 已知的 API
# def isBadVersion(version: int) -> bool: ...

def firstBadVersion(n: int) -> int:
    """
    使用二分查找，在 O(log n) 次调用内找到第一个坏版本。
    """
    left, right = 1, n               # 初始化搜索区间 [1, n]
    while left < right:              # 当区间长度大于 1 时继续
        mid = left + (right - left) // 2   # 防止整数溢出
        if isBadVersion(mid):        # 中间版本是坏的
            right = mid               # 第一个坏版本在左半边（含 mid）
        else:                         # 中间版本是好的
            left = mid + 1            # 第一个坏版本在右半边（不含 mid）
    # 循环结束时 left == right，即为答案
    return left
```

#### 复杂度

- **时间复杂度**：`O(log n)` —— 每次把搜索区间缩小一半，调用次数大约是 `log₂(n)` 次。  
  - 大白话：如果 `n = 1,000,000`，只需要大约 20 次 API 调用就能定位答案，远快于暴力的 1,000,000 次。  
- **空间复杂度**：`O(1)` —— 只用了常数个变量，没有额外的数据结构。

---

## 心得

- **核心技巧**：二分查找（Binary Search）在单调（递增或递减）序列中定位转折点。  
- **适用的题型**：
  1. **Search Insert Position**（在有序数组中寻找插入位置）  
  2. **Find Minimum in Rotated Sorted Array**（在旋转排序数组中找最小值）  
  3. **Peak Index in a Mountain Array**（寻找山峰索引）  
- **一句话总结**：把“第一个坏版本”看成“从好到坏的第一道门”，二分把门一次次关半，最快找到那扇门。

## 反思

- **第一反应**：直接从头到尾检查，每次调用 API，想当然地把它写成循环。  
- **最容易踩的坑**：
  - **溢出**：`mid = (left + right) // 2` 在某些语言（如 Java）会因 `left + right` 超过整数上限而出错，使用 `left + (right - left)//2` 更安全。  
  - **死循环**：如果在 `isBadVersion(mid)` 为 `True` 时写成 `right = mid - 1`，会把答案排除掉，导致循环永不收敛。  
  - **边界条件**：`n = 1` 或者坏版本恰好是第一个（`bad = 1`）时，必须确保循环能够结束并返回正确答案。  
- **下次遇到同类题**：第一步先判断“序列是否单调”，如果是，就立刻想到 **二分查找**，并明确是找**左边界**（第一个满足条件的）还是**右边界**（最后一个满足条件的）。这样可以快速锁定最优解的方向。