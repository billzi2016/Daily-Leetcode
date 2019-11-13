# #658. 找到最接近的 K 个元素 / Find K Closest Elements

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Sliding Window、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/find-k-closest-elements/)

---

## 题目（英文原版）

**Description**

Given a sorted integer array arr, two integers k and x, return the k closest integers to x in the array. The result should also be sorted in ascending order.
An integer a is closer to x than an integer b if:

**Examples**

**Example 1:**

```
Input: arr = [1,2,3,4,5], k = 4, x = 3
Output: [1,2,3,4]
```

**Example 2:**

```
Input: arr = [1,1,2,3,4,5], k = 4, x = -1
Output: [1,1,2,3]
```

**Constraints**

- 1 <= k <= arr.length
- 1 <= arr.length <= 104
- arr is sorted in ascending order.
- -104 <= arr[i], x <= 104

---

## 题目（中文翻译）

给定一个已排序整数数组（sorted integer array）`arr`，以及两个整数 `k` 和 `x`，返回数组中距离 `x` 最近的 `k` 个整数。返回的结果也必须按升序排列。

**距离的定义**  
若整数 `a` 与整数 `b` 相对于 `x` 的距离满足以下任意条件，则 `a` 被认为比 `b` 更接近 `x`：

1. `|a - x| < |b - x|`  
2. `|a - x| == |b - x|` 且 `a < b`

---

### 示例

**示例 1**  
输入: `arr = [1,2,3,4,5]`, `k = 4`, `x = 3`  
输出: `[1,2,3,4]`

**示例 2**  
输入: `arr = [1,1,2,3,4,5]`, `k = 4`, `x = -1`  
输出: `[1,1,2,3]`

---

### 约束条件

- `1 <= k <= arr.length`
- `1 <= arr.length <= 10^4`
- `arr` 按升序排列。
- `-10^4 <= arr[i], x <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **每个元素离 x 的距离** 计算出来，然后按照「距离小 → 距离大」的顺序排个序。  
- **数据结构**：我们可以把数组的每个元素包装成一个二元组 `(distance, value)`，类似把「词」和「页码」装进字典里，只是这里我们用列表保存所有二元组。  
- **为什么正确**：排序后，前 `k` 个二元组对应的 `value` 正好是距离 `x` 最近的 `k` 个数。因为我们先比较距离，距离相同再比较数值本身（题目要求相等时取更小的），所以排序的顺序恰好满足题目要求。  
- **复杂度分析**：  
  - 计算距离遍历一次数组，需要 `O(n)` 的时间。  
  - 对 `n` 条二元组进行排序，时间是 `O(n log n)`（这里的 `log n` 可以理解为把 `n` 件事分成两半、再分两半……不断折半的过程，需要的步数大约是 `log₂ n`，比如 `n=1024` 时 `log₂ n = 10`，所以排序只会多几次比较）。  
  - 取前 `k` 个再排序一次（因为答案要升序），额外 `O(k log k)`，但 `k ≤ n`，整体仍是 `O(n log n)`。  
  - 额外空间要存放 `n` 个二元组，`O(n)`。

#### 代码（Python）
```python
from typing import List

def findClosestElements_bruteforce(arr: List[int], k: int, x: int) -> List[int]:
    # 1. 计算每个元素到 x 的距离，组成 (distance, value) 二元组
    #    distance = abs(num - x)  —— 绝对值就像“测量尺子”，不管在左边还是右边，都是正数
    distance_pairs = [(abs(num - x), num) for num in arr]

    # 2. 按照距离升序、若距离相同则数值升序排序
    distance_pairs.sort(key=lambda pair: (pair[0], pair[1]))

    # 3. 取前 k 个元素的原始数值
    closest = [pair[1] for pair in distance_pairs[:k]]

    # 4. 最终答案要升序返回
    closest.sort()
    return closest
```

#### 复杂度
- **时间复杂度**：`O(n log n)` —— 主要耗时在对 `n` 条记录排序，`log n` 表示“把东西不断二分”的次数，实际操作大约是 `n` 乘以这个次数。
- **空间复杂度**：`O(n)` —— 需要额外存放 `n` 条 `(distance, value)` 二元组。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **全数组排序**，但原数组已经是 **升序** 的，我们可以利用这一点，只在局部进行比较。

**核心思路**：  
1. 用二分查找找出 `x` 在数组中的“插入位置” `pos`（即第一个 `≥ x` 的下标）。可以把它想象成在一本已经排好序的电话本里，快速定位应该把新号码写在哪一页的开头，时间是 `O(log n)`。  
2. 设左指针 `left = pos - 1`（指向插入位置左边的元素），右指针 `right = pos`（指向插入位置右边的元素）。  
3. 每次比较 `arr[left]` 与 `arr[right]` 哪个更靠近 `x`（距离小的保留），把对应的指针向外移动一格，直到已经选出 `k` 个元素。因为每次只移动一步，最多移动 `k` 步，时间是 `O(k)`。  
4. 最后 `left+1` 到 `right-1` 之间的子数组就是答案，直接切片返回即可，它天然是升序的。

**为什么正确**：  
- 二分得到的 `pos` 把数组分成「左边 ≤ x」和「右边 > x」两部分。最近的 `k` 个数一定在这两个指针向外扩张的范围内，因为我们每一步都把距离更小的那一侧纳入答案。  
- 当左指针走到数组左端或右指针走到数组右端时，只能继续往另一侧扩张，这正好对应「缺少元素只能从另一边补」的情况。

**另一种等价实现**：滑动窗口。先把窗口设为整个数组，然后不断收缩左边界或右边界，使得窗口长度始终为 `k`，并且窗口外的元素离 `x` 更远。该方法的时间同样是 `O(log n + k)`，这里我们用双指针的写法更直观。

#### 代码（Python）
```python
from typing import List

def findClosestElements(arr: List[int], k: int, x: int) -> List[int]:
    # 1. 二分查找，找到第一个 >= x 的位置
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1          # x 在右边，左边都小于 x
        else:
            hi = mid - 1          # arr[mid] >= x，继续左边找更靠前的
    # 循环结束后，lo 是第一个 >= x 的下标（可能等于 len(arr)）
    right = lo          # 右指针指向第一个 >= x 的位置
    left = lo - 1       # 左指针指向它左边的元素

    # 2. 从左右两侧各挑选，直到挑出 k 个
    while k > 0:
        # 左边已经没有元素，只能选右边
        if left < 0:
            right += 1
        # 右边已经没有元素，只能选左边
        elif right >= len(arr):
            left -= 1
        else:
            # 比较两侧元素到 x 的距离，距离小的那一侧被选入答案
            if abs(arr[left] - x) <= abs(arr[right] - x):
                left -= 1
            else:
                right += 1
        k -= 1

    # 3. left+1 … right-1 区间正好是答案，已经是升序
    return arr[left + 1:right]
```

#### 复杂度
- **时间复杂度**：`O(log n + k)`  
  - `log n` 用于二分定位（把大数组“折半”找位置），  
  - `k` 步用于在左右两侧挑选最近的 `k` 个数。  
  相比暴力解的 `O(n log n)`，这里在大多数情况下会更快，尤其是 `k` 远小于 `n` 时。
- **空间复杂度**：`O(1)` —— 只用了若干指针变量，没有额外随 `n` 增长的存储。

---

## 心得

- **核心技巧**：利用已排序数组的特性，结合二分查找定位和双指针（或滑动窗口）在局部比较，避免全局排序。  
- **适用的题型**：  
  1. “在排序数组中找最接近的 K 个元素”（本题）。  
  2. “在排序数组中找目标值的最近邻”（如 LeetCode 658 Find Closest Number）。  
  3. “在排序数组中找满足条件的最小/最大子数组长度”（使用滑动窗口或双指针的思路）。  
- **一句话总结解题钥匙**：**先用二分把问题“切分”，再用双指针在两侧“抢夺”最近的元素**。

---

## 反思

- **第一反应**：看到“已排序 + 最近 k 个”，本能想到先算距离再排序（暴力），因为这一步最直接、最不容易出错。  
- **最容易踩的坑**：  
  - 边界处理：`x` 比所有元素都小或都大时，二分得到的 `pos` 会是 `0` 或 `len(arr)`，需要确保左指针或右指针不会越界。  
  - 当左、右指针都还有元素时，距离相等应优先选左侧（因为左侧的数更小），否则答案顺序会不符合题目要求。  
  - `k` 可能等于数组长度，循环里一定要防止指针越界。  
- **下次遇到同类题的第一步**：先确认数组是否已排序，若是，立刻考虑 **二分定位 + 双指针/滑动窗口**，而不是直接全局排序。这样可以把时间复杂度从 `O(n log n)` 降到 `O(log n + k)`。