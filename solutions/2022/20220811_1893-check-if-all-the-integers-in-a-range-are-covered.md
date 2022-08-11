# #1893. 检查区间内的所有整数是否被覆盖 / Check if All the Integers in a Range Are Covered

> 难度：简单 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/check-if-all-the-integers-in-a-range-are-covered/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array ranges and two integers left and right. Each ranges[i] = [starti, endi] represents an inclusive interval between starti and endi.
Return true if each integer in the inclusive range [left, right] is covered by at least one interval in ranges. Return false otherwise.
An integer x is covered by an interval ranges[i] = [starti, endi] if starti <= x <= endi.

**Examples**

**Example 1:**

```
Input: ranges = [[1,2],[3,4],[5,6]], left = 2, right = 5
Output: true
Explanation: Every integer between 2 and 5 is covered:
- 2 is covered by the first range.
- 3 and 4 are covered by the second range.
- 5 is covered by the third range.
```

**Example 2:**

```
Input: ranges = [[1,10],[10,20]], left = 21, right = 21
Output: false
Explanation: 21 is not covered by any range.
```

**Constraints**

- 1 <= ranges.length <= 50
- 1 <= starti <= endi <= 50
- 1 <= left <= right <= 50

---

## 题目（中文翻译）

**描述**  
给定一个二维整数数组 `ranges` 和两个整数 `left`、`right`。`ranges[i] = [starti, endi]` 表示一个包含区间（inclusive interval），区间的左端点为 `starti`，右端点为 `endi`（两端均包含）。  

返回 `true` 当且仅当区间 `[left, right]`（两端均包含）中的每个整数都被 `ranges` 中的至少一个区间覆盖。否则返回 `false`。  

如果整数 `x` 满足 `starti <= x <= endi`，则称 `x` 被区间 `ranges[i] = [starti, endi]` 覆盖。

**示例 1**  
```text
Input: ranges = [[1,2],[3,4],[5,6]], left = 2, right = 5
Output: true
Explanation: 2 到 5 之间的每个整数都被覆盖：
- 2 被第一个区间覆盖。
- 3 和 4 被第二个区间覆盖。
- 5 被第三个区间覆盖。
```

**示例 2**  
```text
Input: ranges = [[1,10],[10,20]], left = 21, right = 21
Output: false
Explanation: 21 没有被任何区间覆盖。
```

**约束条件**  
- `1 <= ranges.length <= 50`  
- `1 <= starti <= endi <= 50`  
- `1 <= left <= right <= 50`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是 **把左边界 `left` 到右边界 `right` 的每一个整数都逐个检查**，看它们是否至少出现在 `ranges` 中的某个区间里。  

- **遍历检查**：对每个待检查的整数 `x`（从 `left` 到 `right`），再遍历一次所有区间 `ranges[i] = [start, end]`，只要找到一个满足 `start ≤ x ≤ end` 的区间，就说明 `x` 被覆盖了。  
- **数据结构类比**：这里的 `ranges` 就像一本“区间字典”，每一行是一本书的章节起止页码。我们要做的，就是把要检查的页码（`x`）逐页翻，看它能不能在任意章节的页码范围里出现。  

这种做法一定能得到正确答案，因为我们穷举了 **所有可能的 x**，并且对每个 x 都确认了它是否被至少一个区间覆盖。

#### 代码（Python）  

```python
def isCovered(ranges, left, right):
    # 对 [left, right] 中的每一个整数 x
    for x in range(left, right + 1):
        covered = False                # 标记 x 是否被覆盖
        # 遍历所有区间，看看有没有一个区间能覆盖 x
        for start, end in ranges:
            if start <= x <= end:      # 区间包含 x
                covered = True
                break                  # 找到一个即可，不用继续找
        if not covered:                # 只要有一个 x 没被覆盖，就直接返回 False
            return False
    return True                       # 所有 x 都被覆盖
```

#### 复杂度  

- **时间复杂度**：`O((right - left + 1) * n)`，其中 `n = len(ranges)`。  
  - **大白话**：如果左、右边界之间有 10 个数，区间有 5 个，那么我们最多会检查 10 × 5 = 50 次。最坏情况下，`right-left` 可能是 49（因为上限是 50），`n` 最多 50，所以最多检查 2500 次，仍然在能接受的范围。  
- **空间复杂度**：`O(1)`，只用了常数个额外变量（`covered`、循环计数器），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  
暴力解的 **瓶颈** 在于每检查一个数 `x` 都要遍历所有区间，导致 *二次循环*。我们可以把 **“哪些整数被覆盖”** 这件事提前算好，后面只需要 **一次查询**。  

两种常见的优化思路：

1. **使用布尔数组（或哈希表）标记**  
   - 题目限制 `starti, endi, left, right ≤ 50`，所以所有可能的整数只在 `[1, 50]` 这 50 个位置。  
   - 建立一个长度为 51（下标 0~50，方便直接使用数字作为下标）的布尔数组 `covered[51]`，初始全为 `False`。  
   - 遍历每个区间 `[start, end]`，把 `covered[start] … covered[end]` 全部标记为 `True`。这一步相当于一次性把所有被覆盖的整数写进“字典”。  
   - 最后只要检查 `covered[left] … covered[right]` 是否全为 `True`，即可得到答案。  

2. **前缀和（差分数组）**  
   - 对于更大范围的题目，直接把每个区间的每个点都标记会导致 `O(range * n)`。  
   - 使用差分数组 `diff[52]`：对每个区间 `[l, r]`，做 `diff[l] += 1`，`diff[r+1] -= 1`。随后对 `diff` 做一次前缀和，得到每个位置的覆盖次数。只要覆盖次数>0，即表示被覆盖。  
   - 这里因为范围只有 50，直接用布尔数组即可，思路更直观。

下面给出 **布尔数组** 的实现，并在代码中稍作解释。

#### 代码（Python）  

```python
def isCovered(ranges, left, right):
    # 1. 创建一个长度为 51 的布尔数组，索引直接对应整数值
    covered = [False] * 51          # 下标 0 不会用到，方便直接使用数字

    # 2. 把所有区间的整数都标记为 True
    for start, end in ranges:
        # 将 start ~ end 之间的每个位置都设为 True
        for num in range(start, end + 1):
            covered[num] = True

    # 3. 检查 [left, right] 区间是否全部为 True
    for num in range(left, right + 1):
        if not covered[num]:        # 只要有一个没有被覆盖，就返回 False
            return False
    return True                     # 全部被覆盖
```

> **如果想进一步提升到 O(n + maxVal) 的时间**（即不在内部再循环每个区间的每个点），可以改用差分数组。下面给出差分写法，仅作补充：

```python
def isCovered_diff(ranges, left, right):
    diff = [0] * 52                 # 多一个位置存放 r+1 的减法
    for start, end in ranges:
        diff[start] += 1
        diff[end + 1] -= 1

    # 前缀和得到每个位置的覆盖次数
    cur = 0
    for i in range(1, 51):
        cur += diff[i]
        if left <= i <= right and cur == 0:   # 在查询区间内出现 0，说明未被覆盖
            return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O( maxVal + n )`，这里 `maxVal = 50`（常数），`n = len(ranges)`。  
  - **大白话**：我们只遍历了所有区间一次（`n` 次），以及遍历一次长度为 50 的数组进行标记和检查，总共不到 100 步，几乎是瞬间完成。相比暴力解的 “每个数 × 每个区间”，省去了二次循环。  
- **空间复杂度**：`O(maxVal)`，即额外使用了长度约为 51 的布尔数组（或差分数组）。这也是常数级别的空间。

---  

## 心得  

- **核心技巧**：利用**离散化 + 直接映射**（布尔数组/差分数组）把“区间覆盖”问题转化为“数组标记+一次遍历”。  
- **适用场景**：  
  1. **区间覆盖检查**（本题）。  
  2. **区间求交 / 求并的计数**（如 LeetCode 1893 “检查子数组和是否为 0”）。  
  3. **频率统计**（如“统计数组中出现次数大于 1 的数字”），都可以使用类似的“离散化 + 前缀和”思路。  
- **一句话总结**：**把所有要判断的点提前映射到一个小数组里，一遍标记一遍检查，就能把二次循环降到一次遍历**。  

---  

## 反思  

- **第一反应**：看到“区间”和“范围”，立刻想到遍历每个数并逐个判断是否在区间里——这就是暴力思路。  
- **最容易踩的坑**：  
  - **边界忘记**：`right` 是 **inclusive**（闭区间），所以循环要写成 `range(right + 1)`。  
  - **数组下标越界**：题目数值最大是 50，若使用差分数组，需要多开一个位置（`diff[52]`），防止对 `r+1` 越界。  
  - **重复标记**：即使一个数被多个区间覆盖，布尔数组只需要一次 `True`，不必计数。  
- **下次类似题目第一步**：先判断数值范围是否足够小，若是，则考虑 **离散化 + 直接映射**（布尔数组或差分数组），把区间操作转为数组操作，避免嵌套循环。