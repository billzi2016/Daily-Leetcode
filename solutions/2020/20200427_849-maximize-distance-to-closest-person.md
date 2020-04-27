# #849. 最大化与最近人的距离 / Maximize Distance to Closest Person

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximize-distance-to-closest-person/)

---

## 题目（英文原版）

**Description**

You are given an array representing a row of seats where seats[i] = 1 represents a person sitting in the ith seat, and seats[i] = 0 represents that the ith seat is empty (0-indexed).
There is at least one empty seat, and at least one person sitting.
Alex wants to sit in the seat such that the distance between him and the closest person to him is maximized.
Return that maximum distance to the closest person.

**Examples**

**Example 1:**

```
Input: seats = [1,0,0,0,1,0,1]
Output: 2
Explanation: 
If Alex sits in the second open seat (i.e. seats[2]), then the closest person has distance 2.
If Alex sits in any other open seat, the closest person has distance 1.
Thus, the maximum distance to the closest person is 2.
```

**Example 2:**

```
Input: seats = [1,0,0,0]
Output: 3
Explanation: 
If Alex sits in the last seat (i.e. seats[3]), the closest person is 3 seats away.
This is the maximum distance possible, so the answer is 3.
```

**Example 3:**

```
Input: seats = [0,1]
Output: 1
```

**Constraints**

- 2 <= seats.length <= 2 * 104
- seats[i] is 0 or 1.
- At least one seat is empty.
- At least one seat is occupied.

---

## 题目（中文翻译）

给定一个数组 `seats` 表示一排座位，其中 `seats[i] = 1` 表示第 `i` 个座位上有人坐着，`seats[i] = 0` 表示第 `i` 个座位是空的（0 索引）。
数组中至少有一个空座位，并且至少有一个座位被占用。
Alex 想要选择一个座位坐下，使得他与最近的人的距离最大化。
返回该最大距离。

## 示例

### 示例 1
**输入:** `seats = [1,0,0,0,1,0,1]`  
**输出:** `2`  
**解释:**  
如果 Alex 坐在第二个空座位（即 `seats[2]`），则最近的人的距离为 2。  
如果 Alex 坐在其他任何空座位，最近的人的距离为 1。  
因此，能够达到的最大距离是 2。

### 示例 2
**输入:** `seats = [1,0,0,0]`  
**输出:** `3`  
**解释:**  
如果 Alex 坐在最后一个座位（即 `seats[3]`），最近的人的距离为 3。  
这是可能的最大距离，所以答案为 3。

### 示例 3
**输入:** `seats = [0,1]`  
**输出:** `1`

## 约束条件
- `2 <= seats.length <= 2 * 10^4`
- `seats[i]` 只能是 `0` 或 `1`
- 至少有一个座位为空
- 至少有一个座位被占用

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**每一个空座位（`seats[i] == 0`），然后计算它到最近已经坐人的距离，最后取这些距离的最大值。  

- **遍历**：把座位数组从左到右扫一遍，找到所有空位的下标。  
- **求最近人**：对每个空位，再从左往右或从右往左扫描，找到最近的 `1`，记录两侧最近人的距离，取较小的那个就是该空位的“最近距离”。  
- **取最大**：把所有空位的最近距离放进一个列表，求最大值即为答案。  

> **类比**：把座位看成一排房间，`1` 就是已经住人的房间，`0` 是空房间。我们要为新来的 Alex 选一间空房，使得他离最近的邻居最远。暴力做法相当于把每间空房都跑一趟，看看最近的邻居是谁，然后挑出最远的那间。

这种方法一定能得到正确答案，因为我们检查了**所有可能的坐法**，不管哪一种最优，都会在枚举中出现。

#### 代码（Python）

```python
def maxDistToClosest_bruteforce(seats):
    n = len(seats)
    max_dist = 0                       # 记录目前找到的最大最近距离

    for i in range(n):
        if seats[i] == 0:               # 只考虑空座位
            # 向左找最近的已坐人
            left = i - 1
            while left >= 0 and seats[left] == 0:
                left -= 1
            # 向右找最近的已坐人
            right = i + 1
            while right < n and seats[right] == 0:
                right += 1

            # 计算左、右两侧最近人的距离
            left_dist = i - left if left >= 0 else float('inf')
            right_dist = right - i if right < n else float('inf')
            # 该空位的最近距离是两者的较小值
            closest = min(left_dist, right_dist)

            # 更新全局最大值
            max_dist = max(max_dist, closest)

    return max_dist
```

#### 复杂度  

- **时间复杂度**：`O(n^2)`  
  对每个空位都要向左、向右各扫描一次，最坏情况下（全部是 `0` 除了两端的 `1`）会导致每次扫描走完整个数组，形成平方级别的时间。  
  用大白话说，就是如果座位有 10,000 个，最差会进行约 100,000,000 次比较，明显太慢。  

- **空间复杂度**：`O(1)`  
  只用了常数级的额外变量（`max_dist`、`left`、`right`），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要线性扫描左、右两侧**。我们可以一次遍历就把所有信息算好，避免重复扫描。  

关键观察：

1. **连续的空座位段**（即 `0` 的子数组）决定了 Alex 能坐的最远距离。  
2. 对于 **两端的空段**（数组最左边或最右边的 `0`），Alex 只能坐在该段的最远端，距离就是该段的长度。  
3. 对于 **中间的空段**（左右两边都有人），Alex 最优的坐法是坐在该段的**中间**，此时最近人的距离是段长除以 2（向下取整），因为左右两侧的已坐人等距。  

因此，只要遍历一次数组，记录每段 `0` 的长度，并根据其位置（两端还是中间）计算对应的“可能的最大最近距离”，最后取最大即可。

实现步骤：

- 用变量 `prev_one` 记录上一次出现 `1` 的下标，初始设为 `-1`（表示还未出现）。
- 用变量 `max_dist` 记录答案。
- 从左到右遍历 `seats`：
  - 遇到 `1` 时，分两种情况：
    - **左端空段**：如果 `prev_one == -1`，说明这是第一个人，左侧全是空。此时候的候选距离是当前下标 `i`（空段长度）。
    - **中间空段**：否则，两个人之间的空段长度为 `i - prev_one - 1`，候选距离是 `(i - prev_one) // 2`（取整）。
    - 更新 `max_dist` 为两者的最大值。
    - 更新 `prev_one = i`。
- 循环结束后，可能还有右端空段（最后一个 `1` 之后全是 `0`），其长度为 `len(seats) - 1 - prev_one`，候选距离即为该长度。再次取最大。

> **类比**：把座位看成一条路，两边有树（已坐的人），我们要在树之间种一棵新树，使得它到最近树的距离最大。只要知道每段空地的长度，就能直接算出种树的最佳位置，而不必每一步都去量距离。

#### 代码（Python）

```python
def maxDistToClosest(seats):
    """
    一次遍历求最大最近距离
    """
    n = len(seats)
    prev_one = -1          # 上一个出现的 1 的下标，-1 表示还没有
    max_dist = 0           # 当前找到的最大最近距离

    for i, seat in enumerate(seats):
        if seat == 1:                      # 碰到已坐的人
            if prev_one == -1:
                # 第一个人，左侧全是空座位
                max_dist = max(max_dist, i)        # i 本身就是左端空段长度
            else:
                # 两个人之间的空段长度为 i - prev_one - 1
                # Alex 最好坐在中间，最近距离是段长除以 2（向下取整）
                dist = (i - prev_one) // 2
                max_dist = max(max_dist, dist)
            prev_one = i                # 更新上一次出现的 1 的位置

    # 处理右端空段（如果最后一个座位是 0）
    if seats[-1] == 0:
        right_len = n - 1 - prev_one   # 右端空段的长度
        max_dist = max(max_dist, right_len)

    return max_dist
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历了一遍数组，任何操作都是常数时间。用大白话说，座位有 10,000 个，只需要检查 10,000 次，就能得到答案，线性增长非常快。  

- **空间复杂度**：`O(1)`  
  只用了几个整数变量（`prev_one`、`max_dist`、`i` 等），不随输入规模增大。

---  

## 心得  

- 本题核心是**把问题抽象为“连续空段的长度”**，并分别讨论两端和中间的情况。  
- 这种“划分段落、一次遍历” 的技巧在很多数组题中都很有用，例如：  
  1. **寻找最长连续 1 的子数组**（LeetCode 525）  
  2. **最长连续 0 的子数组**（类似本题的变形）  
  3. **连续子数组最大和**（Kadane 算法的思想）  

> **解题钥匙**：一次遍历 + 记录关键位置（上一次出现的 1） → 直接算出每段空座的最佳距离。

---  

## 反思  

- **第一反应**：看到“最大化最近距离”，自然想到枚举每个空位并计算最近人，得到暴力解。  
- **最容易踩的坑**：  
  1. **两端空段的处理**：左端和右端的距离不是除以 2，而是整个段长，因为只有一侧有人。  
  2. **整数除法取整**：中间段的距离应使用 `// 2`（向下取整），否则会出现 1.5 这种不合法的距离。  
  3. **边界条件**：数组首位或尾位是 `0` 时，需要单独考虑。  

- **下次遇到类似题**：第一步先**划分连续的“特殊子段”（0 或 1）**，判断每段在整体中的位置（两端或内部），再依据位置直接算出答案，而不是逐个元素重复计算。