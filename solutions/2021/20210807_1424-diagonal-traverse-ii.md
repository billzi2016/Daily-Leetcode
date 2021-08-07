# #1424. 对角线遍历 II / Diagonal Traverse II

> 难度：中等 · 标签：Array、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/diagonal-traverse-ii/)

---

## 题目（英文原版）

**Description**

Given a 2D integer array nums, return all elements of nums in diagonal order as shown in the below images.

**Examples**

**Example 1:**

```
Input: nums = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,4,2,7,5,3,8,6,9]
```

**Example 2:**

```
Input: nums = [[1,2,3,4,5],[6,7],[8],[9,10,11],[12,13,14,15,16]]
Output: [1,6,2,8,7,3,9,4,12,10,5,13,11,14,15,16]
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i].length <= 105
- 1 <= sum(nums[i].length) <= 105
- 1 <= nums[i][j] <= 105

---

## 题目（中文翻译）

给定一个 **二维整数数组（2D integer array）** `nums`，按照下图所示的对角线顺序返回 `nums` 中的所有元素。

**示例 1：**  
**示例 2：**  

**约束条件：**

- `1 <= nums.length <= 10^5`
- `1 <= nums[i].length <= 10^5`
- `1 <= sum(nums[i].length) <= 10^5`
- `1 <= nums[i][j] <= 10^5`

**示例：**

**示例 1:**  
输入: `nums = [[1,2,3],[4,5,6],[7,8,9]]`  
输出: `[1,4,2,7,5,3,8,6,9]`

**示例 2:**  
输入: `nums = [[1,2,3,4,5],[6,7],[8],[9,10,11],[12,13,14,15,16]]`  
输出: `[1,6,2,8,7,3,9,4,12,10,5,13,11,14,15,16]`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
把二维数组 **看成一张坐标纸**，每个元素都有行号 `i` 和列号 `j`。  
如果把 `i + j` 当作“对角线的编号”，会发现所有 `i + j` 相同的元素恰好在同一条对角线上（从左上往右下的方向）。  

> **类比**：把 `i + j` 想成一本字典的“页码”。同一页码的词（元素）要放在一起，最后按页码顺序翻页。

实现步骤：

1. **遍历所有元素**，把每个元素记成 `(i + j, i, value)` 的三元组。  
2. 把同一 `i + j` 的元素放进同一个“桶”。这里可以用 `defaultdict(list)`，把 `i + j` 当作键，值是 `(i, value)` 的列表。  
3. **遍历桶的键**（即对角线编号）从小到大，把每个桶里的元素按照行号 `i` 的升序取出（因为同一对角线里，行号小的在前），依次加入答案数组。  

这样得到的顺序正是题目要求的对角线遍历顺序。

> **为什么正确**：  
> - 同一对角线的所有元素必然满足 `i + j` 相等，第一步已经把它们聚到一起。  
> - 对角线编号从小到大遍历，等价于从左上角的第一条对角线一直向右下走。  
> - 在同一对角线里，行号 `i` 越小，列号 `j` 越大，恰好是题目示例中的顺序，所以对每个桶再按 `i` 排序即可。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

def findDiagonalOrder(nums: List[List[int]]) -> List[int]:
    # 1. 把每个元素放进对应的对角线桶
    buckets = defaultdict(list)          # key = i + j, value = [(i, val), ...]
    for i, row in enumerate(nums):        # 遍历行号 i
        for j, val in enumerate(row):     # 遍历列号 j
            diag = i + j                   # 对角线编号
            buckets[diag].append((i, val))

    # 2. 按对角线编号升序遍历，每个桶内部再按行号 i 升序取值
    answer = []
    for diag in sorted(buckets.keys()):   # 对角线编号从小到大
        # 对同一对角线的元素按行号 i 排序
        for _, val in sorted(buckets[diag], key=lambda x: x[0]):
            answer.append(val)

    return answer
```

> **关键行中文注释**：  
> - `buckets = defaultdict(list)` → 把相同 `i+j` 的元素放到同一个列表里（像把同页的单词放进同一本子典）。  
> - `diag = i + j` → 计算元素所在的对角线编号。  
> - `for diag in sorted(buckets.keys())` → 按照页码顺序“翻页”。  
> - `sorted(buckets[diag], key=lambda x: x[0])` → 在同一页里把行号小的（词在前）先取出来。

#### 复杂度  

- **时间复杂度**：`O(N log D)`，其中 `N` 是所有元素的总数（`≤ 10⁵`），`D` 是不同对角线的数量（`≤ N`）。  
  - 遍历所有元素是 `O(N)`。  
  - 对每个对角线的键排序需要 `O(D log D)`，`D` 最多等于 `N`，所以最坏是 `O(N log N)`。  
  - 桶内再对行号排序，总共也是 `O(N log N)`（因为每个元素只会参与一次排序）。  
- **空间复杂度**：`O(N)` 用来存放所有三元组（桶），相当于把原数组复制了一遍。  

> **大白话**：  
> - 时间上我们要先把所有数字收集好，再把“页码”排个序，就像先把所有单词写进字典再按页码翻。  
> - 空间上需要一个额外的盒子装所有数字，和原数组差不多大。

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于 **对对角线编号的排序**（`sorted(buckets.keys())`）以及 **每个桶内部再排序**。其实我们完全可以 **直接把元素放进对应编号的桶**，而不需要再排序，因为：

1. 对角线编号 `i + j` 的范围是 `0 … max_i+max_j`，最多 `N`（元素总数）个。  
2. 如果我们提前准备一个长度为 `max_diag + 1` 的列表（每个位置是一个空列表），遍历元素时直接把 `(i, val)` 加进 `bucket[diag]`，**桶的顺序天然是升序**（因为我们按 `i` 从小到大遍历行）。  

这样：

- **不需要对键排序**（因为列表索引本身就是从小到大）。  
- **不需要对桶内部再排序**（因为遍历行号 `i` 时是递增的，且在同一行中列号 `j` 递增，`i` 已经保证了正确的顺序）。  

> **核心技巧**：**桶排序（Bucket Sort）**。把元素按“对角线编号”直接放进对应的桶，利用数组下标的天然有序性省去显式排序。  

#### 代码（Python）  

```python
from typing import List

def findDiagonalOrder(nums: List[List[int]]) -> List[int]:
    # 1. 先算出最大的对角线编号，方便开辟桶数组
    max_diag = 0
    for i, row in enumerate(nums):
        if row:                               # 防止空行（题目保证不为空，但写得更健壮）
            max_diag = max(max_diag, i + len(row) - 1)

    # 2. 创建桶：每个编号对应一个列表，初始为空
    buckets = [[] for _ in range(max_diag + 1)]

    # 3. 把元素直接放进对应的桶
    for i, row in enumerate(nums):
        for j, val in enumerate(row):
            diag = i + j
            buckets[diag].append(val)   # 直接追加，顺序天然正确

    # 4. 按桶的顺序合并答案
    answer = []
    for bucket in buckets:               # 桶的下标已经是对角线编号的升序
        answer.extend(bucket)            # 把该对角线的所有元素一次性加入答案

    return answer
```

> **关键行中文注释**：  
> - `max_diag = max(max_diag, i + len(row) - 1)` → 算出最右下角的对角线编号，决定桶的数量。  
> - `buckets = [[] for _ in range(max_diag + 1)]` → 开辟若干空桶，像准备好若干信封。  
> - `buckets[diag].append(val)` → 把数字塞进对应编号的信封，顺序不需要再调整。  
> - `for bucket in buckets: answer.extend(bucket)` → 按信封的顺序“拆开”，把里面的信件依次放进结果。

#### 复杂度  

- **时间复杂度**：`O(N)`  
  - 只遍历一次所有元素，进行常数时间的 “放进桶” 操作。  
  - 合并桶时同样是线性遍历 `N` 个元素。  
- **空间复杂度**：`O(N + D)`  
  - `O(N)` 用于存放所有元素的桶（相当于复制一遍原数组）。  
  - `O(D)` 是桶的数量（`D = max_diag + 1 ≤ N`），相当于额外的指针数组。  

> **对比**：相比暴力解的 `O(N log N)` 时间，最优解只需要线性时间，真正做到“一遍扫描搞定”。  

---  

## 心得  

- **核心技巧**：**把 “行号 + 列号” 视作对角线编号，利用桶排序直接按编号收集元素**。  
- **适用场景**：  
  1. **对角线遍历**（如本题、LeetCode 498 “Diagonal Traverse”）。  
  2. **按某个线性函数分组**（例如把点按 `x + y`、`x - y` 分组的几何题）。  
  3. **需要保序的分桶**（如按年龄、分数段统计且保持出现顺序的统计题）。  
- **一句话总结**：**“把相同 i+j 的元素塞进同一个桶，桶的顺序本身就是答案的顺序”。**  

---  

## 反思  

- **第一反应**：看到“对角线”，立刻想到 `i + j` 相等的点，于是用字典收集再排序。  
- **最容易踩的坑**：  
  - **不等长的行**：`nums[i]` 长度不同，需要用 `j` 遍历每行的实际长度。  
  - **对角线编号的最大值**：如果直接用 `defaultdict`，不需要预先算最大值；但如果想用列表做桶，需要先遍历一次或在遍历过程中动态扩容。  
  - **顺序错误**：如果把 `(i, val)` 放进桶后再按值排序，可能会破坏行号的自然顺序。只要按行遍历即可。  
- **下次遇到同类题**：第一步先 **写出 “i + j”** 这条分组公式，然后判断是否可以 **用桶（数组）直接收集**，再决定是否需要额外排序。这样能迅速定位最优解的方向。