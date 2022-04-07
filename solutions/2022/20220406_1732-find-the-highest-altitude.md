# #1732. 最高海拔 / Find the Highest Altitude

> 难度：简单 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-highest-altitude/)

---

## 题目（英文原版）

**Description**

There is a biker going on a road trip. The road trip consists of n + 1 points at different altitudes. The biker starts his trip on point 0 with altitude equal 0.
You are given an integer array gain of length n where gain[i] is the net gain in altitude between points i​​​​​​ and i + 1 for all (0 <= i < n). Return the highest altitude of a point.

**Examples**

**Example 1:**

```
Input: gain = [-5,1,5,0,-7]
Output: 1
Explanation: The altitudes are [0,-5,-4,1,1,-6]. The highest is 1.
```

**Example 2:**

```
Input: gain = [-4,-3,-2,-1,4,3,2]
Output: 0
Explanation: The altitudes are [0,-4,-7,-9,-10,-6,-3,-1]. The highest is 0.
```

**Constraints**

- n == gain.length
- 1 <= n <= 100
- -100 <= gain[i] <= 100

---

## 题目（中文翻译）

有一名骑行者正在进行一次公路旅行。旅行包含 n + 1 个海拔不同的点，骑行者从点 0 出发，初始海拔为 0。  
给定一个长度为 n 的整数数组 `gain`，其中 `gain[i]` 表示点 i 与点 i + 1 之间的海拔净增量（net gain in altitude），满足 0 ≤ i < n。返回旅行中任意一点的最高海拔。

**示例 1**  
**输入**: `gain = [-5,1,5,0,-7]`  
**输出**: `1`  
**解释**: 各点的海拔分别为 `[0,-5,-4,1,1,-6]`，最高海拔为 1。

**示例 2**  
**输入**: `gain = [-4,-3,-2,-1,4,3,2]`  
**输出**: `0`  
**解释**: 各点的海拔分别为 `[0,-4,-7,-9,-10,-6,-3,-1]`，最高海拔为 0。

**约束条件**
- `n == gain.length`
- `1 <= n <= 100`
- `-100 <= gain[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**逐个点重新累加**：  
1. 第 0 点海拔已经知道是 `0`。  
2. 对于第 i（i≥1）点的海拔，直接把 `gain[0] … gain[i‑1]` 全部加起来，得到从起点到该点的累计升高/降低。  
3. 把所有点的海拔都算出来后，取最大值即可。  

> **数据结构类比**：这里用到的数组就像一本日记，`gain[i]` 记的是第 i 天到第 i+1 天的高度变化。要知道第 3 天的高度，就得把前面三天的变化全部翻出来相加，类似“查字典”时要把所有词义都读一遍。  

**为什么正确**：  
- 根据题意，第 i 点的海拔正好等于起点海拔 `0` 加上前 i 条路段的累计增益，这正是我们每次把 `gain[0..i‑1]` 求和得到的结果。  
- 只要把每个点的海拔算出来，最大值必然是答案。  

#### 代码（Python）  

```python
def highestAltitude_bruteforce(gain):
    n = len(gain)                     # 路段数量
    altitudes = [0] * (n + 1)         # 存放每个点的海拔，长度 n+1
    # 暴力求每个点的海拔
    for i in range(1, n + 1):        # i 表示第 i 个点（从 1 开始）
        total = 0                     # 用来累加 gain[0..i-1]
        for j in range(i):           # 逐个累加前面的增益
            total += gain[j]
        altitudes[i] = total          # 第 i 点的海拔
    # 直接取最大值
    return max(altitudes)
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 外层循环跑 `n` 次，内层累计也最坏要跑 `n` 次，合在一起是“平方级”。可以把 `n²` 想象成如果你有 100 条路段，需要算 100×100=10,000 次加法，明显有点慢。  
- **空间复杂度：** `O(n)`  
  - 需要额外的数组 `altitudes` 保存 `n+1` 个海拔值，随 `n` 成线性增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复累加是浪费**：  
- 当我们已经算出第 i 点的海拔后，第 i+1 点的海拔只需要在此基础上 **再加上 `gain[i]`**，不必重新把前面的所有增益全部相加。  

这正是**前缀和（Prefix Sum）**的思想：  
- 维护一个变量 `cur`，始终保存**当前点的海拔**。  
- 每遍历一个 `gain[i]`，把它加到 `cur`，得到下一个点的海拔。  
- 同时用另一个变量 `max_alt` 记录遍历过程中出现的最大海拔。  

> **类比**：想象你在爬山，每走一步都记录当前的高度。下一步只要在前一步的高度上加上这一步的升高（或降低），不需要重新算一次整个爬升过程。  

**关键步骤**  
1. 初始化 `cur = 0`（起点海拔），`max_alt = 0`（起点也是可能的最高点）。  
2. 遍历 `gain`：  
   - `cur += gain[i]` → 更新到下一个点的海拔。  
   - `max_alt = max(max_alt, cur)` → 维护最高海拔。  
3. 循环结束后，`max_alt` 就是答案。  

#### 代码（Python）  

```python
def highestAltitude(gain):
    cur = 0           # 当前点的海拔，初始为起点 0
    max_alt = 0       # 记录遍历过程中的最高海拔，起点也可能是最高点
    for delta in gain:          # 依次遍历每段路的海拔变化
        cur += delta            # 到达下一个点的海拔
        if cur > max_alt:       # 如果当前海拔更高，就更新最高记录
            max_alt = cur
    return max_alt
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 只遍历一次 `gain`，每个元素做一次加法和一次比较，和路段数成线性关系。相比 `O(n²)`，如果 `n=100`，只需要 100 次运算，几乎是瞬间完成。  
- **空间复杂度：** `O(1)`  
  - 只用常数个额外变量 (`cur`、`max_alt`)，不随输入规模增长。  

---  

## 心得  

- **核心技巧**：前缀和（累计求和）+ 在遍历过程中同步维护最大值。  
- **适用的题型**  
  1. “子数组最大和” 类似的累计求和题（如 LeetCode 53 最大子数组和）。  
  2. “统计区间和” 需要快速求任意前缀和的题目（如 LeetCode 303 区域子数组和）。  
- **一句话总结解题钥匙**：**“把每一步的状态保留下来，后续只在前一步的基础上增量更新”。**  

## 反思  

- **第一反应**：看到“gain”数组，马上想到“累计求和”。  
- **最容易踩的坑**  
  - 忽略起点海拔 `0` 也是可能的最高点（比如全部为负数时答案应为 0）。  
  - 边界条件：`gain` 可能只有 1 个元素，代码仍需正常工作。  
- **下次遇到同类题**：第一步先**判断是否可以用前缀和/累计变量**，如果可以，就立刻转向 O(n) 的线性遍历思路。