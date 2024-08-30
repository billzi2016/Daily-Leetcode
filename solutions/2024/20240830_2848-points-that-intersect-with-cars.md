# #2848. 与车辆相交的点 / Points That Intersect With Cars

> 难度：简单 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/points-that-intersect-with-cars/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array nums representing the coordinates of the cars parking on a number line. For any index i, nums[i] = [starti, endi] where starti is the starting point of the ith car and endi is the ending point of the ith car.
Return the number of integer points on the line that are covered with any part of a car.

**Examples**

**Example 1:**

```
Input: nums = [[3,6],[1,5],[4,7]]
Output: 7
Explanation: All the points from 1 to 7 intersect at least one car, therefore the answer would be 7.
```

**Example 2:**

```
Input: nums = [[1,3],[5,8]]
Output: 7
Explanation: Points intersecting at least one car are 1, 2, 3, 5, 6, 7, 8. There are a total of 7 points, therefore the answer would be 7.
```

**Constraints**

- 1 <= nums.length <= 100
- nums[i].length == 2
- 1 <= starti <= endi <= 100

---

## 题目（中文翻译）

给定一个下标从 0 开始的二维整数数组 `nums`，表示停放在数轴上的汽车的坐标。对于任意下标 `i`，`nums[i] = [starti, endi]`，其中 `starti` 是第 `i` 辆车的起点，`endi` 是第 `i` 辆车的终点。返回数轴上被任意一辆汽车覆盖的整数点的个数。

### 示例 1
**输入:** `nums = [[3,6],[1,5],[4,7]]`  
**输出:** `7`  
**解释:** 所有从 1 到 7 的整数点至少与一辆汽车相交，因此答案为 7。

### 示例 2
**输入:** `nums = [[1,3],[5,8]]`  
**输出:** `7`  
**解释:** 与至少一辆汽车相交的点为 1、2、3、5、6、7、8，共计 7 个点，因此答案为 7。

### 约束条件
- `1 <= nums.length <= 100`
- `nums[i].length == 2`
- `1 <= starti <= endi <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **所有可能的整数点** 都列出来，看看每个点是否被至少一辆车覆盖。  
- 这里的 “整数点” 就像一排编号的格子（1 号格、2 号格 …），我们可以把它们想象成 **字典的页码**，要查某个格子里有没有车，就像在字典里查某个词是否存在。  
- 对每一辆车的区间 `[start, end]`，把 `start … end` 之间的每个格子都标记为 “被占”。  
- 最后统计被标记的格子数，就是答案。  

这种做法一定是对的，因为我们把 **所有** 可能的格子都检查了一遍，只要格子在任意区间内，就会被记上。

#### 代码（Python）

```python
def numberOfPoints(nums):
    # 题目给出的坐标范围都在 1~100 之间
    # 用一个长度为 101（下标 0~100）的布尔数组来标记每个整数点是否被占
    occupied = [False] * 101          # False 表示当前点还没有车

    for start, end in nums:           # 遍历每辆车的区间
        # 把区间里的每个整数点都标记为 True
        for p in range(start, end + 1):
            occupied[p] = True        # 标记为已占

    # 统计被标记为 True 的点的个数
    return sum(occupied)               # True 当作 1 来加，总和就是答案
```

#### 复杂度  

- **时间复杂度**：`O(N * L)`  
  - `N` 是车的数量（最多 100），`L` 是每辆车区间的长度（最长也不超过 100）。  
  - 大白话：最坏情况下我们会把 100 辆车的每个点（最多 100 个）都遍历一次，总共 10,000 次操作，仍然在可以接受的范围。  

- **空间复杂度**：`O(1)`（常数空间）  
  - 只用了一个固定大小的 `occupied` 数组（长度 101），不随 `N` 增长而增长。  

---

### 2. 最优解  

#### 思路  

暴力解的 “慢” 点在于**重复遍历**同一个点很多次：如果两个区间重叠，重叠部分会被标记多次。  
我们可以把所有区间**合并**后，只算一次每段连续的长度，这样就不会重复计数。

合并区间的常用技巧是 **先排序** 再线性扫描：

1. **排序**：把所有区间按照左端点 `start` 从小到大排好序。  
   - 想象把所有车排成一条线，左边的车先出来，右边的车后出来，这样相邻的车最有可能重叠。  

2. **扫描合并**：维护当前合并后的区间 `[cur_start, cur_end]`。  
   - 对于下一个区间 `[s, e]`：  
     - 如果 `s` **大于** `cur_end`，说明它们不相交，当前合并区间结束，计入答案，然后把 `[s, e]` 当作新的合并区间。  
     - 否则（`s ≤ cur_end`），两段区间相交或相邻，只需要把 `cur_end` 拉伸到 `max(cur_end, e)` 即可。  

3. **累计长度**：每当一个合并区间确定下来（不再会与后面的区间相交），把它的整数点数 `cur_end - cur_start + 1` 加到答案中。  

这样每个区间只会被处理一次，时间从 `O(N * L)` 降到 `O(N log N)`（排序的代价），空间只用常数。

#### 代码（Python）

```python
def numberOfPoints(nums):
    # 1. 按 start 升序排序，若 start 相同再按 end 排序
    nums.sort(key=lambda x: (x[0], x[1]))

    ans = 0               # 最终答案
    cur_start, cur_end = nums[0]   # 第一个区间作为当前合并区间

    for s, e in nums[1:]:          # 从第二个区间开始遍历
        if s > cur_end:            # 与当前区间不相交
            # 统计当前区间覆盖的整数点数
            ans += cur_end - cur_start + 1
            # 开启一个新的合并区间
            cur_start, cur_end = s, e
        else:                      # 有交集或相邻，合并
            cur_end = max(cur_end, e)   # 右端点取更大的

    # 最后一个合并区间没有在循环里计入，需要单独加上
    ans += cur_end - cur_start + 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(N log N)`  
  - `N` 为车的数量（≤100），排序需要 `log N` 的比较次数。  
  - 大白话：先把车排好队（相当于把书按照字母顺序排好），排队的时间是主要开销，之后只走一遍队列，几乎不花时间。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整型变量来记录当前区间和答案，未使用额外的数组或哈希表。  

---

## 心得  

- **核心技巧**：**区间合并（线段合并）**。把所有可能重叠的区间整理成不相交的若干段，再求长度。  
- **适用的题型**：  
  1. “合并区间”系列（LeetCode 56 Merge Intervals）。  
  2. “区间求并集长度”或“统计被覆盖的点数”类（如本题）。  
  3. “会议室计数”或“求最少会议室数”需要先排序再扫描。  
- **解题钥匙**：**先排序，再用“当前合并区间”滚动更新**。

---

## 反思  

- **第一反应**：看到“求被覆盖的整数点数”，本能想把每个点都列出来检查——这就是暴力思路。  
- **最容易踩的坑**：  
  - **忘记 +1**：区间是闭区间 `[start, end]`，整数点数应为 `end - start + 1`，容易漏掉最后一个点。  
  - **相邻区间**：如 `[1,3]` 与 `[4,5]`，它们不重叠但点 `3` 与 `4` 不是同一点，仍然是两个独立区间，合并时要使用 `s > cur_end`（严格大于）判断。  
- **下次第一步**：先 **排序** 再 **判断是否相交**，看能否直接合并或直接计数。这样可以立刻把暴力的重复计数问题化解。