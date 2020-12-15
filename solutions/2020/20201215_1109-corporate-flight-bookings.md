# #1109. **企业航班预订** / Corporate Flight Bookings

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/corporate-flight-bookings/)

---

## 题目（英文原版）

**Description**

There are n flights that are labeled from 1 to n.
You are given an array of flight bookings bookings, where bookings[i] = [firsti, lasti, seatsi] represents a booking for flights firsti through lasti (inclusive) with seatsi seats reserved for each flight in the range.
Return an array answer of length n, where answer[i] is the total number of seats reserved for flight i.

**Examples**

**Example 1:**

```
Input: bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5
Output: [10,55,45,25,25]
Explanation:
Flight labels:        1   2   3   4   5
Booking 1 reserved:  10  10
Booking 2 reserved:      20  20
Booking 3 reserved:      25  25  25  25
Total seats:         10  55  45  25  25
Hence, answer = [10,55,45,25,25]
```

**Example 2:**

```
Input: bookings = [[1,2,10],[2,2,15]], n = 2
Output: [10,25]
Explanation:
Flight labels:        1   2
Booking 1 reserved:  10  10
Booking 2 reserved:      15
Total seats:         10  25
Hence, answer = [10,25]
```

**Constraints**

- 1 <= n <= 2 * 104
- 1 <= bookings.length <= 2 * 104
- bookings[i].length == 3
- 1 <= firsti <= lasti <= n
- 1 <= seatsi <= 104

---

## 题目（中文翻译）

有 `n` 条航班，编号从 `1` 到 `n`。  
给定一个航班预订（flight bookings）数组 `bookings`，其中 `bookings[i] = [first_i, last_i, seats_i]` 表示一次预订，预订的航班范围是 `first_i` 到 `last_i`（**包括** `last_i`），并且在该范围内的每条航班上都预留了 `seats_i` 个座位。  
返回一个长度为 `n` 的数组 `answer`，其中 `answer[i]` 表示第 `i` 条航班预留的座位总数。

**示例 1**  

**输入**: `bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5`  
**输出**: `[10,55,45,25,25]`  
**解释**:  
航班编号:            1   2   3   4   5  
预订 1 预留:        10  10  
预订 2 预留:            20  20  
预订 3 预留:            25  25  25  25  
总座位数:         10  55  45  25  25  
因此，`answer = [10,55,45,25,25]`  

**示例 2**  

**输入**: `bookings = [[1,2,10],[2,2,15]], n = 2`  
**输出**: `[10,25]`  
**解释**:  
航班编号:            1   2  
预订 1 预留:        10  10  
预订 2 预留:            15  
总座位数:         10  25  
因此，`answer = [10,25]`  

**约束条件**  
- `1 <= n <= 2 * 10^4`  
- `1 <= bookings.length <= 2 * 10^4`  
- `bookings[i].length == 3`  
- `1 <= first_i <= last_i <= n`  
- `1 <= seats_i <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一次预订都展开**，把它对应的每一趟航班的座位数都加到答案数组里。  
可以把 `answer` 想象成一张**记事本**，第 `i` 行记录第 `i` 趟航班已经被预订的座位数。  
每条预订 ` [first, last, seats] ` 就像在记事本上从第 `first` 行写到第 `last` 行，每行都加上 `seats`。  

> **类比**：哈希表（字典）就像一本**查字典**，key 是单词，value 是解释；这里的记事本每一行就是一个“key”（航班编号），对应的“value”是累计的座位数。

只要遍历所有预订，再遍历每个预订的 `[first, last]` 区间，把 `seats` 累加进去，最后返回记事本（即 `answer`）即可。

**为什么这个方法一定正确？**  
因为我们把所有预订的影响都完整地、逐一地加到了对应的航班上，所有航班的座位数就是所有预订在该航班上的总和，这正是题目要的答案。

#### 代码（Python）

```python
def corpFlightBookings(bookings, n):
    # 创建长度为 n 的记事本，初始全为 0
    answer = [0] * n                # answer[i] 表示第 i+1 趟航班的座位数

    # 对每一条预订记录逐个展开
    for first, last, seats in bookings:
        # 注意：题目里的航班编号是从 1 开始的，列表索引是从 0 开始的
        for i in range(first - 1, last):   # 从 first-1 到 last-1（闭区间）
            answer[i] += seats            # 把 seats 加到对应的航班上

    return answer
```

#### 复杂度

- **时间复杂度：** `O(m * k)`  
  - `m = len(bookings)` 是预订的条数，`k` 是每条预订的区间长度（`last - first + 1`）。最坏情况下每条预订都跨越所有航班，`k` ≈ `n`，于是时间复杂度退化为 `O(m * n)`。  
  - **大白话**：如果有 10 条预订，每条都要遍历 5 条航班，就要做 10×5=50 次加法。

- **空间复杂度：** `O(n)`  
  - 只用了一个长度为 `n` 的数组 `answer` 来存结果。  
  - **大白话**：我们只需要和航班数量等大的纸张来记录结果，不会额外再占用很多空间。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每条预订都要遍历它覆盖的所有航班**，导致大量重复的加法操作。  
我们可以把“区间加”这个操作改写成“差分 + 前缀和”。  

**核心概念——差分数组**  
想象有一条数轴，每个位置记录当前的座位数。我们不直接把每个位置的值改掉，而是记录**变化点**：

- 在区间左端 `first` 位置 **加** `seats`（表示从这里开始座位数要增加）。
- 在区间右端的下一位 `last+1` 位置 **减** `seats`（表示从这里开始要恢复原来的值）。

这样，真正的座位数就可以通过**一次遍历累计（前缀和）**得到。

> **类比**：把记事本想象成一条水管，`+seats` 是在某个位置打开阀门让水流入，`-seats` 是在另一位置关闭阀门。最终每段管子里的水量，只需要从头开始累计阀门的开关状态。

**步骤**  

1. 创建长度为 `n+1` 的差分数组 `diff`，全部初始化为 0。多加一个位置是为了方便在 `last+1` 位置做减法而不越界。  
2. 对每条预订 `[first, last, seats]`：  
   - `diff[first-1] += seats`（因为数组索引从 0 开始）  
   - `diff[last]   -= seats`（如果 `last` 已经是最后一趟航班，则此步可以省略，因为 `diff[n]` 其实是多余的）  
3. 把差分数组转成真正的答案：从左到右累计求前缀和，得到每趟航班的座位数。  

这样，每条预订只会进行 **常数时间** 的两次修改，整体时间是 `O(m + n)`，远快于暴力的 `O(m·n)`。

#### 代码（Python）

```python
def corpFlightBookings(bookings, n):
    # 1. 初始化差分数组，长度为 n+1（多一个位置方便做减法）
    diff = [0] * (n + 1)          # diff[i] 表示第 i+1 趟航班座位数的“变化量”

    # 2. 对每一条预订，只在区间左右端做两次修改
    for first, last, seats in bookings:
        diff[first - 1] += seats          # 区间左端开始增加 seats
        if last < n:                      # 若右端不是最后一趟航班，才需要在 next 位置减去 seats
            diff[last] -= seats           # 区间右端的下一位开始恢复（减去） seats

    # 3. 通过前缀和把差分数组恢复成真实的答案
    answer = [0] * n
    cur = 0                               # cur 保存从左到右累计的座位数
    for i in range(n):
        cur += diff[i]                     # 累计到第 i 趟航班的座位数
        answer[i] = cur                    # 写入答案

    return answer
```

#### 复杂度

- **时间复杂度：** `O(m + n)`  
  - `m` 是预订的条数，`n` 是航班的数量。每条预订只做两次常数操作，随后只遍历一次 `diff`（长度 `n`）求前缀和。  
  - **大白话**：如果有 10 条预订和 5 条航班，只需要大约 10×2 + 5 ≈ 25 次基本操作，比暴力的 50 次少了一半。

- **空间复杂度：** `O(n)`  
  - 只用了一个长度为 `n+1` 的差分数组和一个长度为 `n` 的答案数组。  
  - **大白话**：仍然只需要和航班数量等大的纸张来记录变化，额外再多一格而已。

---

## 心得

- **核心技巧**：**差分数组 + 前缀和**（又叫区间增量技巧）。  
- **适用的题型**  
  1. “区间加” 类问题，如 LeetCode 370 *Range Addition*。  
  2. “区间求和” 类问题，如 LeetCode 307 *Range Sum Query - Mutable*（使用差分或线段树实现）。  
  3. “数组差分” 统计题，如统计每一天的温度变化等。  

- **一句话总结**：  
  *把每个区间的“加”拆成左端“加”、右端“减”，一次遍历累计即可得到所有答案。*

---

## 反思

- **第一反应**：直接把每条预订的区间展开，逐个累加——也就是暴力解。  
- **最容易踩的坑**  
  1. **索引偏移**：航班编号从 1 开始，Python 列表从 0 开始，需要注意 `first-1`、`last` 的转换。  
  2. **边界处理**：当 `last == n` 时，`diff[last]` 实际是 `diff[n]`（超出答案范围），此时不需要减法。  
  3. **整数范围**：虽然题目限制 `seats ≤ 10⁴`，但累计可能超过 32 位整数，使用 Python 的大整数即可。  

- **下次遇到同类题**，第一步应该想到：  
  *“这是不是一个‘区间增量’的问题？能否用差分数组把每个区间的操作压缩到 O(1)？”*  

这样可以迅速从暴力思路跳到最优解，写出更高效的代码。