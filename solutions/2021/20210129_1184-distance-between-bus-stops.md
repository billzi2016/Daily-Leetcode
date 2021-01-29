# #1184. 公交站之间的距离 / Distance Between Bus Stops

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/distance-between-bus-stops/)

---

## 题目（英文原版）

**Description**

A bus has n stops numbered from 0 to n - 1 that form a circle. We know the distance between all pairs of neighboring stops where distance[i] is the distance between the stops number i and (i + 1) % n.
The bus goes along both directions i.e. clockwise and counterclockwise.
Return the shortest distance between the given start and destination stops.

**Examples**

**Example 1:**

```
Input: distance = [1,2,3,4], start = 0, destination = 1
Output: 1
Explanation: Distance between 0 and 1 is 1 or 9, minimum is 1.
```

**Example 2:**

```
Input: distance = [1,2,3,4], start = 0, destination = 2
Output: 3
Explanation: Distance between 0 and 2 is 3 or 7, minimum is 3.
```

**Example 3:**

```
Input: distance = [1,2,3,4], start = 0, destination = 3
Output: 4
Explanation: Distance between 0 and 3 is 6 or 4, minimum is 4.
```

**Constraints**

- 1 <= n <= 10^4
- distance.length == n
- 0 <= start, destination < n
- 0 <= distance[i] <= 10^4

---

## 题目（中文翻译）

描述  
一辆公交车（bus）有 `n` 个站点（stops），编号为 `0` 到 `n - 1`，形成一个环形（circle）。已知所有相邻站点之间的距离，其中 `distance[i]` 表示站点 `i` 与站点 `(i + 1) % n` 之间的距离。公交车可以沿两个方向行驶，即顺时针（clockwise）和逆时针（counterclockwise）。请返回给定的起点 `start` 与目的地 `destination` 之间的最短距离。

示例  

**示例 1**  
输入: `distance = [1,2,3,4], start = 0, destination = 1`  
输出: `1`  
解释: 0 与 1 之间的距离可以是 `1`（顺时针）或 `9`（逆时针），最小值为 `1`。

**示例 2**  
输入: `distance = [1,2,3,4], start = 0, destination = 2`  
输出: `3`  
解释: 0 与 2 之间的距离可以是 `3`（顺时针）或 `7`（逆时针），最小值为 `3`。

**示例 3**  
输入: `distance = [1,2,3,4], start = 0, destination = 3`  
输出: `4`  
解释: 0 与 3 之间的距离可以是 `6`（顺时针）或 `4`（逆时针），最小值为 `4`。

约束条件  
- `1 <= n <= 10^4`  
- `distance.length == n`  
- `0 <= start, destination < n`  
- `0 <= distance[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把环形公交站想象成一条闭合的跑道，站点之间的距离就像跑道上相邻两段的长度。  
我们只需要算两条可能的路线：

1. **顺时针**（clockwise）：从 `start` 按照数组的顺序一直跑到 `destination`。  
2. **逆时针**（counter‑clockwise）：走相反的方向，等价于“总路程 - 顺时针路程”。

> **类比**：哈希表就像字典，`key` 是单词，`value` 是页码。这里的 `distance` 数组就像跑道上每段的长度，索引 `i` 表示“第 i 段”。

只要把顺时针的距离算出来，另外一种方向的距离就可以用“全程长度 - 顺时针距离”得到。两条路程取最小值即为答案。

**为什么正确**：环形结构保证了顺时针和逆时针两条路径覆盖了所有可能的走法，且它们的长度之和恰好等于整个环的总长度。取最小的那条自然就是最短距离。

**复杂度分析**  
- 我们最多遍历一次数组（最坏情况要走完整个环），所以时间是 **O(n)**，这里的 *n* 就是站点数。  
- 只使用了几个整数变量保存累计距离，空间是 **O(1)**（常数级别）。

> **大白话**：`O(n)` 就相当于“和站点数成正比”。如果有 10 000 站，最多跑 10 000 步；如果只有 5 站，只跑 5 步。`O(1)` 则是“不管站点多少，使用的额外空间始终是固定的几个变量”。

#### 代码（Python）

```python
def distanceBetweenBusStops(distance, start, destination):
    """
    暴力思路：直接遍历一次数组算出顺时针距离，
    再用总长度减去它得到逆时针距离，取最小值返回。
    """
    # 如果 start 大于 destination，交换两者，使 start 在前面，方便遍历
    if start > destination:
        start, destination = destination, start

    # 1️⃣ 计算顺时针距离
    clockwise = 0
    for i in range(start, destination):
        clockwise += distance[i]          # 累加相邻站之间的距离

    # 2️⃣ 环的总长度
    total = sum(distance)                # 把所有段的长度加起来

    # 3️⃣ 逆时针距离 = 总长度 - 顺时针距离
    counter_clockwise = total - clockwise

    # 4️⃣ 返回两条路中较短的那条
    return min(clockwise, counter_clockwise)


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(distanceBetweenBusStops([1, 2, 3, 4], 0, 1))  # 1
    print(distanceBetweenBusStops([1, 2, 3, 4], 0, 2))  # 3
    print(distanceBetweenBusStops([1, 2, 3, 4], 0, 3))  # 4
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  需要遍历一次 `distance`（最坏情况下遍历全部），相当于和站点数成线性关系。

- **空间复杂度：** `O(1)`  
  只用了几个整数变量（`clockwise、total、counter_clockwise`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

上面的暴力解已经是 **线性** 的，对于单次查询已经足够快。但如果在同一个公交线路上要**多次**查询不同的 `start`、`destination`，每次都重新遍历数组就会浪费很多时间。  
我们可以把 **前缀和**（prefix sum）这个技巧引入进来：

- **前缀和数组** `pre[i]` 表示从站点 `0` 到站点 `i-1`（不含 `i`）的累计距离。  
  - 类比：在字典里查词时，`key` 是词，`value` 是页码；这里 `i` 是“站点”，`pre[i]` 是“跑到这里已经跑了多少路”。

有了前缀和后，**顺时针距离**可以在 **O(1)** 时间内直接算出：

```
if start <= destination:
    clockwise = pre[destination] - pre[start]
else:
    clockwise = total - (pre[start] - pre[destination])
```

其中 `total = pre[n]` 是整个环的总长度。逆时针距离仍然是 `total - clockwise`，取最小值即可。

> **关键点**：前缀和把“区间求和”这个 O(k) 的操作（k 为区间长度）压缩成 O(1)。因此，当查询次数很多时，总体复杂度会从 `O(q·n)` 降到 `O(n + q)`（`q` 为查询次数）。

#### 代码（Python）

```python
def distanceBetweenBusStops_opt(distance, start, destination):
    """
    最优思路：先预处理前缀和，使任意两站的顺时针距离能在 O(1) 时间内得到。
    这在单次查询时和暴力解时间相同，但对多次查询更快。
    """
    n = len(distance)

    # 1️⃣ 构造前缀和数组，pre[0] = 0，pre[i] 为前 i 段的总距离
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + distance[i]   # 累加第 i 段的长度

    total = pre[n]                         # 环的总长度

    # 2️⃣ 统一把 start、destination 变成顺时针方向的区间
    #    如果 start > destination，顺时针要“跨过”数组尾部
    if start <= destination:
        clockwise = pre[destination] - pre[start]
    else:
        clockwise = total - (pre[start] - pre[destination])

    # 3️⃣ 逆时针距离 = 总长度 - 顺时针距离
    counter_clockwise = total - clockwise

    # 4️⃣ 返回最短的那条路
    return min(clockwise, counter_clockwise)


# ------------------- 测试 -------------------
if __name__ == "__main__":
    print(distanceBetweenBusStops_opt([1, 2, 3, 4], 0, 1))  # 1
    print(distanceBetweenBusStops_opt([1, 2, 3, 4], 0, 2))  # 3
    print(distanceBetweenBusStops_opt([1, 2, 3, 4], 0, 3))  # 4
```

#### 复杂度

- **时间复杂度：** `O(n)`（一次遍历构建前缀和）+ `O(1)`（单次查询）  
  - 对单次查询而言仍是 `O(n)`，与暴力解等价。  
  - 若有 `q` 次查询，总时间为 `O(n + q)`，明显优于 `O(q·n)`。

- **空间复杂度：** `O(n)`  
  需要额外的前缀和数组 `pre`，大小为 `n+1`。相比暴力解的 `O(1)` 多用了线性空间，但换来的是查询的常数时间。

---

## 心得

- **核心技巧**：**前缀和**（把区间求和压缩到 O(1)）和**环形路径的两条方向**的最小化思路。  
- **适用题型**  
  1. 环形或循环数组的区间求和（如 LeetCode 1470 `Shuffle the Array` 的变形）。  
  2. 多次区间查询的数组题目（如 LeetCode 303 `Range Sum Query - Immutable`）。  
- **一句话总结**：**先把所有段的长度累加成前缀和，再用“顺时针 vs. 逆时针”取最小即可**。

## 反思

- **第一反应**：把环看成直线，先算顺时针距离，再用总长度减去得到逆时针距离。  
- **最容易踩的坑**  
  - `start` 与 `destination` 的大小顺序不一定，忘记交换或统一方向会导致遍历负数区间。  
  - 环的总长度可能为 0（所有 `distance[i]` 为 0），此时两条路都为 0，代码仍需正常返回。  
- **下次思考**：遇到“环形”“两端相连”或“多次区间查询”时，先问自己“是否可以用前缀和把区间求和变成 O(1)”。如果答案是肯定的，前缀和就是解题钥匙。