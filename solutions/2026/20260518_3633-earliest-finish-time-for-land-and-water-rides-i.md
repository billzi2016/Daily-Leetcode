# #3633. 陆地和水上游乐设施的最早完成时间 I / Earliest Finish Time for Land and Water Rides I

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/earliest-finish-time-for-land-and-water-rides-i/)

---

## 题目（英文原版）

**Description**

You are given two categories of theme park attractions: land rides and water rides.
A tourist must experience exactly one ride from each category, in either order.
Return the earliest possible time at which the tourist can finish both rides.

**Examples**

**Example 1:**

```
Input: landStartTime = [2,8], landDuration = [4,1], waterStartTime = [6], waterDuration = [3]
Output: 9
Explanation: ​​​​​​​
Plan A gives the earliest finish time of 9.
```

**Example 2:**

```
Input: landStartTime = [5], landDuration = [3], waterStartTime = [1], waterDuration = [10]
Output: 14
Explanation: ​​​​​​​
Plan A provides the earliest finish time of 14. ​​​​​​​
```

**Constraints**

- 1 <= n, m <= 100
- landStartTime.length == landDuration.length == n
- waterStartTime.length == waterDuration.length == m
- 1 <= landStartTime[i], landDuration[i], waterStartTime[j], waterDuration[j] <= 1000

---

## 题目（中文翻译）

给定两类主题公园设施（attractions）：**陆地游乐设施**（land rides）和 **水上游乐设施**（water rides）。  
游客必须分别选择并体验每类中恰好一项，顺序可以任意。  
请返回游客完成这两项游乐设施的**最早可能时间**（earliest possible finish time）。

## 示例  

### 示例 1  
**输入**  
```
landStartTime = [2,8], landDuration = [4,1], 
waterStartTime = [6], waterDuration = [3]
```  
**输出**  
```
9
```  
**解释**  
方案 A（先玩陆地游乐设施，再玩水上游乐设施）能够在时间 9 完成，两项游乐设施的最早完成时间即为 9。  

### 示例 2  
**输入**  
```
landStartTime = [5], landDuration = [3], 
waterStartTime = [1], waterDuration = [10]
```  
**输出**  
```
14
```  
**解释**  
方案 A（先玩水上游乐设施，再玩陆地游乐设施）能够在时间 14 完成，两项游乐设施的最早完成时间即为 14。  

## 约束条件  

- 1 ≤ n, m ≤ 100  
- `landStartTime.length == landDuration.length == n`  
- `waterStartTime.length == waterDuration.length == m`  
- 1 ≤ `landStartTime[i]`, `landDuration[i]`, `waterStartTime[j]`, `waterDuration[j]` ≤ 1000

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求游客必须恰好挑选 **一项** 陆地游乐设施和 **一项** 水上游乐设施，先后顺序任意。  
每个设施都有：

* `startTime`：最早可以进入的时间（就像商店的开门时间）。  
* `duration`：游玩需要的时长（相当于在店里逛完需要的时间）。

如果先玩陆地设施 `i`，则：

1. **完成陆地** 的时间 = `landStartTime[i] + landDuration[i]`（因为我们可以立刻在开门时进去）。  
2. **开始水上** 的时间必须不早于水上设施的开门时间 `waterStartTime[j]`，同时也不能早于陆地结束时间。于是实际开始时间 = `max(finishLand, waterStartTime[j])`。  
3. **完成水上** 的时间 = `max(finishLand, waterStartTime[j]) + waterDuration[j]`。

水上先玩、陆地后玩同理，只是把顺序换一下。

把所有可能的陆地‑水上组合枚举一遍，算出两种顺序的结束时间，取最小值，就是答案。

> **类比**：把每个设施想成一本字典，`startTime` 是书的上架时间，`duration` 是阅读这本书需要的分钟数。我们要挑两本书读完，先后顺序随意，只要在它们上架后才能开始阅读。暴力解就是把所有书对儿都尝一遍，看看哪种阅读顺序最早能读完。

这个方法一定能得到正确答案，因为我们没有遗漏任何合法的组合。

#### 代码（Python）

```python
from typing import List

def earliestFinishTime(
    landStartTime: List[int], landDuration: List[int],
    waterStartTime: List[int], waterDuration: List[int]
) -> int:
    n = len(landStartTime)
    m = len(waterStartTime)
    ans = float('inf')                     # 用一个很大的数先占位

    for i in range(n):                     # 枚举每一条陆地设施
        finish_land = landStartTime[i] + landDuration[i]   # 完成陆地的时间

        for j in range(m):                 # 枚举每一条水上设施
            # 方案 1：先玩陆地，再玩水上
            start_water = max(finish_land, waterStartTime[j])   # 必须等陆地结束或水上开门
            finish1 = start_water + waterDuration[j]           # 两项全部结束的时间
            ans = min(ans, finish1)                            # 取更早的

            # 方案 2：先玩水上，再玩陆地（对称写法）
            finish_water = waterStartTime[j] + waterDuration[j]
            start_land = max(finish_water, landStartTime[i])
            finish2 = start_land + landDuration[i]
            ans = min(ans, finish2)

    return ans
```

#### 复杂度

- **时间复杂度：** `O(n * m)`  
  这里的 `n`、`m` 分别是陆地和水上设施的数量。我们对每一对 `(i, j)` 都算两次（两种顺序），所以总共的操作次数与两数组长度的乘积成正比。可以把它想成“如果你有 10 条陆地设施和 8 条水上设施，就要检查 80 种组合”。

- **空间复杂度：** `O(1)`  
  除了输入数组外，只用了常数个临时变量（如 `ans`、`finish_land` 等），不随 `n`、`m` 增长。

---

### 2. 最优解

#### 思路  

在本题的约束下（`n, m ≤ 100`），**暴力解已经是最优的**。  
- 任何更“高级”的技巧（比如排序、前缀最小等）都无法把枚举所有组合的次数进一步降低，因为答案依赖于 **具体的两两配对**，而不是单独的最早结束时间。  
- 我们已经只用了 `O(n·m)` 的时间，没有额外的空间开销，这已经是理论上的下界：必须检查每一对陆地‑水上设施才能保证不遗漏最优解。

因此，**最优解** 与 **直觉解** 完全相同，只是把实现写得更简洁一点。

#### 代码（Python）

```python
def earliestFinishTime(
    landStartTime, landDuration,
    waterStartTime, waterDuration
) -> int:
    ans = float('inf')
    for ls, ld in zip(landStartTime, landDuration):
        finish_land = ls + ld
        for ws, wd in zip(waterStartTime, waterDuration):
            # 陆→水
            ans = min(ans, max(finish_land, ws) + wd)
            # 水→陆
            finish_water = ws + wd
            ans = min(ans, max(finish_water, ls) + ld)
    return ans
```

#### 复杂度

- **时间复杂度：** `O(n·m)` —— 与暴力解相同，已经是最小可能的。
- **空间复杂度：** `O(1)` —— 仅使用常数级别的额外变量。

---

## 心得

- **核心技巧**：枚举所有合法的两两组合，并对每种顺序分别计算结束时间。  
- **适用题型**：  
  1. “两类任务各选一个，求最早完成时间”——如**机场起降调度**（飞机和跑道）。  
  2. “两条线路各选一段，求最短总路程”——如**双线公交换乘**。  
  3. “两种资源各占用一次，求最早结束时间”——如**CPU 与 I/O 任务配对**。  
- **一句话总结**：**把所有可能的配对全遍历，一边算两种顺序的结束时间，最小值即答案。**

---

## 反思

- **第一反应**：看到“各选一个、顺序任意”，自然想到“枚举每个陆地和每个水上组合”，并分别考虑先后顺序。  
- **最容易踩的坑**：  
  - 忘记取 `max(startTime, previousFinish)`，导致出现“提前开始”不符合题意的错误。  
  - 只算了一种顺序（比如只算陆→水），遗漏了水→陆可能更早的情况。  
  - 边界条件：只有一条陆地或水上设施时仍需遍历两种顺序，代码不能假设 `n>1`、`m>1`。  
- **下次遇到同类题**：第一步先明确“每个任务都有最早开始时间 + 持续时间”，然后**列出两种顺序的公式**，最后决定是否需要全枚举（通常是）。