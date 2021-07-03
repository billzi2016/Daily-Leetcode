# #1385. 求两个数组的距离值 / Find the Distance Value Between Two Arrays

> 难度：简单 · 标签：Array、Two Pointers、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/find-the-distance-value-between-two-arrays/)

---

## 题目（英文原版）

**Description**

Given two integer arrays arr1 and arr2, and the integer d, return the distance value between the two arrays.
The distance value is defined as the number of elements arr1[i] such that there is not any element arr2[j] where |arr1[i]-arr2[j]| <= d.

**Examples**

**Example 1:**

```
Input: arr1 = [4,5,8], arr2 = [10,9,1,8], d = 2
Output: 2
Explanation: 
For arr1[0]=4 we have: 
|4-10|=6 > d=2 
|4-9|=5 > d=2 
|4-1|=3 > d=2 
|4-8|=4 > d=2 
For arr1[1]=5 we have: 
|5-10|=5 > d=2 
|5-9|=4 > d=2 
|5-1|=4 > d=2 
|5-8|=3 > d=2
For arr1[2]=8 we have:
|8-10|=2 <= d=2
|8-9|=1 <= d=2
|8-1|=7 > d=2
|8-8|=0 <= d=2
```

**Example 2:**

```
Input: arr1 = [1,4,2,3], arr2 = [-4,-3,6,10,20,30], d = 3
Output: 2
```

**Example 3:**

```
Input: arr1 = [2,1,100,3], arr2 = [-5,-2,10,-3,7], d = 6
Output: 1
```

**Constraints**

- 1 <= arr1.length, arr2.length <= 500
- -1000 <= arr1[i], arr2[j] <= 1000
- 0 <= d <= 100

---

## 题目（中文翻译）

给定两个整数数组（integer arrays）`arr1` 和 `arr2`，以及整数 `d`，返回这两个数组之间的 **距离值**（distance value）。  
**距离值**的定义为满足下列条件的 `arr1[i]` 的个数：不存在任何 `arr2[j]` 使得 `|arr1[i] - arr2[j]| <= d`。

### 示例

#### 示例 1
```
Input: arr1 = [4,5,8], arr2 = [10,9,1,8], d = 2
Output: 2
Explanation: 
对于 arr1[0]=4，有：
|4-10|=6 > d=2 
|4-9|=5 > d=2 
|4-1|=3 > d=2 
|4-8|=4 > d=2 
对于 arr1[1]=5，有：
|5-10|=5 > d=2 
|5-9|=4 > d=2 
|5-1|=4 > d=2 
|5-8|=3 > d=2 
对于 arr1[2]=8，有：
|8-10|=2 <= d=2
|8-9|=1 <= d=2
|8-1|=7 > d=2
|8-8|=0 <= d=2
```

#### 示例 2
```
Input: arr1 = [1,4,2,3], arr2 = [-4,-3,6,10,20,30], d = 3
Output: 2
```

#### 示例 3
```
Input: arr1 = [2,1,100,3], arr2 = [-5,-2,10,-3,7], d = 6
Output: 1
```

### 约束条件
- `1 <= arr1.length, arr2.length <= 500`
- `-1000 <= arr1[i], arr2[j] <= 1000`
- `0 <= d <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  
- 对 **arr1** 中的每一个元素 `x`，把 **arr2** 的所有元素都遍历一遍，计算 `|x - y|`。  
- 只要出现一次 `|x - y| ≤ d`，说明 `x` **不满足** “距离值” 的要求，直接把它舍掉。  
- 否则，遍历完 **arr2** 都没有满足条件的 `y`，就把 `x` 计入答案。

> **类比**：想象你在图书馆查找一本书的“邻近”词。暴力解就相当于把字典里每一页都翻一遍，看看有没有词和目标词的距离（这里的距离是字母相差的绝对值）不超过 `d`。虽然能找到答案，但显然很慢。

**为什么正确**  
- 我们对每个 `arr1[i]` 检查了 **所有** 可能的 `arr2[j]`，只要有一个满足 `|arr1[i]-arr2[j]| ≤ d`，就按照题意把它排除。没有遗漏，也没有误判。

**时间/空间复杂度**  
- 外层遍历 `arr1` 长度为 `n`，内层遍历 `arr2` 长度为 `m`，每一次都要做一次绝对值比较 → **O(n·m)**。  
  - 用大白话说，就是如果 `arr1` 有 100 个数，`arr2` 有 200 个数，总共要做 100×200=20 000 次比较。  
- 只用了几个计数变量，额外空间是 **O(1)**（常数级），不随输入规模增长。

#### 代码（Python）

```python
from typing import List

def findTheDistanceValue_brute(arr1: List[int], arr2: List[int], d: int) -> int:
    """
    暴力解法：对每个 arr1 元素，遍历整个 arr2，检查是否存在 |a-b| <= d
    """
    answer = 0                     # 记录符合条件的 arr1 元素个数
    for x in arr1:                 # 遍历 arr1
        ok = True                  # 假设 x 满足条件
        for y in arr2:             # 遍历 arr2
            if abs(x - y) <= d:    # 只要出现一次满足，就不计入答案
                ok = False
                break              # 立刻退出内层循环，省点时间
        if ok:                     # 如果整轮都没有 break，说明 x 合格
            answer += 1
    return answer
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`，这里的 `n = len(arr1)`, `m = len(arr2)`。  
  - “O” 表示随着输入规模增大，运行时间的增长趋势。`n·m` 表示两数组长度的乘积，规模越大，耗时越快呈指数增长。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **每个 `arr1[i]` 都要遍历完整个 `arr2`**，导致 `n·m` 的乘法关系。  
我们可以利用**排序 + 二分查找**把查询 `arr2` 中“最接近 `arr1[i]` 的元素”从线性时间降到对数时间。

**步骤**  

1. **先把 `arr2` 排序**。排序后，数值相近的元素会挨在一起，方便二分查找。  
2. 对 `arr1` 中的每个 `x`，在已排序的 `arr2` 中使用 **二分搜索** 找到第一个 **不小于 `x`** 的位置（`bisect_left`）。  
   - 这个位置左边的元素是 **最大的 ≤ x** 的数。  
   - 这个位置本身的元素是 **最小的 ≥ x** 的数。  
3. 只需要比较这两个“邻近”元素与 `x` 的距离，因为 **如果 `arr2` 中有任何元素满足 `|x - y| ≤ d`，那么最近的那个元素一定也会满足**。  
   - 具体来说，检查 `arr2[pos]`（如果 `pos` 没越界）和 `arr2[pos-1]`（如果 `pos-1` ≥ 0）这两个候选。  
4. 若这两个候选都和 `x` 的差的绝对值 **大于 d**，则 `x` 合格，计入答案。  

> **类比**：把 `arr2` 想成一本已经按字母顺序排好的词典。要找离目标词最近的词，只需要定位到“第一个不小于目标词的词”，然后检查它和它前面的词，这两个就是最可能“距离”最近的两个词，其他的词都离得更远了。

**核心算法/数据结构**  

- **排序**（`list.sort()`）——把无序的数组变成有序的，时间 `O(m log m)`。  
- **二分查找**（`bisect` 模块）——在有序数组中定位元素的插入位置，时间 `O(log m)`。  
- **双指针** 思想也可以实现：把两个数组一起从小到大遍历，但实现上二分更直观。

#### 代码（Python）

```python
from typing import List
import bisect               # Python 标准库中的二分查找工具

def findTheDistanceValue_opt(arr1: List[int], arr2: List[int], d: int) -> int:
    """
    最优解：先排序 arr2，随后对每个 arr1 元素使用二分查找
    """
    arr2.sort()                 # O(m log m) 的排序
    answer = 0

    for x in arr1:              # 对每个 arr1 元素
        # 在已排序的 arr2 中找到第一个 >= x 的位置
        pos = bisect.bisect_left(arr2, x)   # O(log m)

        # 标记 x 是否满足“没有任何 arr2 元素距离 ≤ d”
        ok = True

        # 检查右侧候选（pos 位置的元素），如果 pos 没越界
        if pos < len(arr2) and abs(arr2[pos] - x) <= d:
            ok = False

        # 检查左侧候选（pos-1 位置的元素），如果 pos-1 >= 0
        if pos > 0 and abs(arr2[pos - 1] - x) <= d:
            ok = False

        if ok:
            answer += 1

    return answer
```

#### 复杂度  

- **时间复杂度**：`O(m log m + n log m)`  
  - `m log m` 来自对 `arr2` 的一次排序。  
  - 对 `arr1` 中的每个元素做一次二分搜索，复杂度是 `log m`，共 `n` 次 → `n log m`。  
  - 与暴力解的 `n·m` 相比，`log` 级别的增长要慢得多，即使 `n`、`m` 达到上限 500，运行时间也几乎可以忽略不计。  
- **空间复杂度**：`O(1)`（不计排序时原地修改的数组本身）。  
  - 只用了常数个额外变量，和输入规模无关。

---

## 心得  

- **核心技巧**：**排序 + 二分查找**（或等价的双指针）把“在数组中寻找最近元素”的查询从线性降到对数。  
- **适用的题型**（类似思路）  
  1. *Find the Closest Number*（在有序数组中找最接近目标的数）。  
  2. *Find the Smallest Difference*（两个数组中差的最小值）。  
  3. *K Closest Points to Origin*（利用二分或堆找最近的点）。  
- **一句话总结解题钥匙**：**把要频繁查询的数组排好序，用二分定位最近的候选，只比较这几个即可**。

---

## 反思  

- **第一反应**：直接套用双层循环，逐个比较——这是最自然的“暴力”思路。  
- **最容易踩的坑**  
  - **边界检查**：二分返回的位置可能是 `0`（左边没有元素）或 `len(arr2)`（右边没有元素），必须先判断下标是否越界后再取值。  
  - **负数和绝对值**：`abs` 必不可少，别忘了把差的符号去掉。  
  - **忘记排序**：二分只能在有序数组上使用，忘记排序会导致错误的定位。  
- **下次遇到同类题**，第一步应该想到：**“能否把查询的数组排好序，然后用二分或双指针一次性解决？”** 这一步往往能把时间复杂度从平方级降到对数级。