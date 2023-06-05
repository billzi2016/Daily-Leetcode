# #2271. 最大覆盖白色瓷砖数量的地毯 / Maximum White Tiles Covered by a Carpet

> 难度：中等 · 标签：Array、Binary Search、Greedy、Sliding Window、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-white-tiles-covered-by-a-carpet/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array tiles where tiles[i] = [li, ri] represents that every tile j in the range li <= j <= ri is colored white.
You are also given an integer carpetLen, the length of a single carpet that can be placed anywhere.
Return the maximum number of white tiles that can be covered by the carpet.

**Examples**

**Example 1:**

```
Input: tiles = [[1,5],[10,11],[12,18],[20,25],[30,32]], carpetLen = 10
Output: 9
Explanation: Place the carpet starting on tile 10. 
It covers 9 white tiles, so we return 9.
Note that there may be other places where the carpet covers 9 white tiles.
It can be shown that the carpet cannot cover more than 9 white tiles.
```

**Example 2:**

```
Input: tiles = [[10,11],[1,1]], carpetLen = 2
Output: 2
Explanation: Place the carpet starting on tile 10. 
It covers 2 white tiles, so we return 2.
```

**Constraints**

- 1 <= tiles.length <= 5 * 104
- tiles[i].length == 2
- 1 <= li <= ri <= 109
- 1 <= carpetLen <= 109
- The tiles are non-overlapping.

---

## 题目（中文翻译）

**描述**  
给定一个二维整数数组 `tiles`，其中 `tiles[i] = [l_i, r_i]` 表示区间 `l_i ≤ j ≤ r_i` 内的每块瓷砖 `j` 均为白色。  
同时给定一个整数 `carpetLen`，表示一块长度为 `carpetLen` 的地毯可以放置在任意位置。  
返回地毯能够覆盖的最多白色瓷砖数量。

**示例 1**  
```text
Input: tiles = [[1,5],[10,11],[12,18],[20,25],[30,32]], carpetLen = 10
Output: 9
Explanation: 将地毯放在第 10 块瓷砖处开始。  
它覆盖了 9 块白色瓷砖，所以返回 9。  
注意可能还有其他位置也能覆盖 9 块白色瓷砖。  
可以证明，地毯最多只能覆盖 9 块白色瓷砖。
```

**示例 2**  
```text
Input: tiles = [[10,11],[1,1]], carpetLen = 2
Output: 2
Explanation: 将地毯放在第 10 块瓷砖处开始。  
它覆盖了 2 块白色瓷砖，所以返回 2。
```

**约束条件**  
- `1 ≤ tiles.length ≤ 5 * 10^4`  
- `tiles[i].length == 2`  
- `1 ≤ l_i ≤ r_i ≤ 10^9`  
- `1 ≤ carpetLen ≤ 10^9`  
- 所有区间互不重叠。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把地毯的左端从 1 移动到可能的每一个位置**，然后逐个统计这块地毯能够覆盖多少白色瓷砖。  
- 这里的“位置”可以理解为整数坐标轴上的点，就像我们把一块尺子从左到右平移，尺子左端所在的坐标就是一种“放置方式”。  
- 对每一种放置方式，我们遍历所有 `tiles`，判断每段白色区间 `[li, ri]` 与地毯 `[start, start+carpetLen-1]` 是否有交集，交集的长度即为被覆盖的白砖数。  
- 只要记录下最大的覆盖数即可。

**为什么这个方法一定能得到答案**  
因为我们枚举了**所有可能的左端坐标**，只要把左端放在任意整数位置，所有合法的放置方式都会被检查到。于是最大值必然被捕获。

**时间/空间复杂度大白话**  
- 假设地毯左端可以放在 `M` 种不同的坐标（这里我们粗略取 `M` 为所有白砖的左端或右端，加上 `carpetLen`，最坏情况下 `M` 可能和 `tiles` 的数量成正比）。  
- 对每一种放置方式我们都要遍历全部 `n` 段白砖区间，判断是否相交并计算交集长度。  
- 因此时间复杂度大概是 `O(M·n)`，在最坏情况下 `M≈n`，于是 **O(n²)**。  
  - “O(n²)” 可以想象成：如果有 1000 段白砖，我们要做大约 1000 × 1000 = 1,000,000 次比较，随着 `n` 增大，工作量会 **平方** 增长，很快就不可接受了。  
- 只使用了几个整数变量和原始的 `tiles` 数组，空间复杂度是 **O(1)**（不计输入本身）。

#### 代码（Python）

```python
from typing import List

def maximumWhiteTiles_bruteforce(tiles: List[List[int]], carpetLen: int) -> int:
    # 1. 先把所有可能的左端位置收集起来，简化枚举范围
    #    我们只需要考虑每段白砖的左端以及右端- carpetLen + 1 这几个点
    candidates = set()
    for l, r in tiles:
        candidates.add(l)                     # 地毯左端恰好在白砖左端
        candidates.add(r - carpetLen + 1)    # 地毯右端恰好在白砖右端

    max_cover = 0
    for start in candidates:
        if start < 0:        # 坐标不可能为负，直接跳过
            continue
        end = start + carpetLen - 1          # 地毯右端坐标（闭区间）
        covered = 0
        # 2. 遍历每段白砖，求交集长度
        for l, r in tiles:
            # 没有交集的情况：白砖全部在地毯左边或右边
            if r < start or l > end:
                continue
            # 有交集：取交集的左端、右端，再算长度
            inter_l = max(l, start)
            inter_r = min(r, end)
            covered += inter_r - inter_l + 1   # +1 因为区间是闭的
        max_cover = max(max_cover, covered)

    return max_cover
```

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况下 `n` 为白砖段数）。  
  - 直观上，就是“每个候选位置都要检查所有白砖”，工作量随 `n` 的平方增长。
- **空间复杂度**：`O(n)`（用于存放 `candidates` 集合），若只遍历所有整数坐标则为 `O(1)`。  
  - 这里的额外空间主要是保存候选起点，规模与 `tiles` 长度相同。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每一个起点都要遍历全部区间**。如果我们能够在 **O(1)** 或 **O(log n)** 的时间内快速求出地毯覆盖的白砖数，就可以把整体复杂度降到 `O(n log n)` 或 `O(n)`。

下面的优化思路分两步：

1. **先把所有白砖区间按照左端 `li` 排序**（题目已保证不重叠，但未必有序）。  
   排序后，区间在坐标轴上呈现“从左到右”的顺序，类似排好队的顾客，后面的顾客只能站在前面顾客的右边。

2. **使用前缀和 + 双指针（滑动窗口）**  
   - **前缀和**：`pre[i]` 表示前 `i` 段区间（`0` 到 `i-1`）全部白砖的总长度。  
     这样我们可以在 **O(1)** 时间内得到任意连续区间的白砖总数：`pre[j] - pre[i]`。  
   - **滑动窗口**：我们维护两个指针 `left`、`right`，表示当前窗口覆盖的区间段是 `[left, right)`（左闭右开）。  
     窗口对应的实际坐标范围是 `[tiles[left][0], tiles[right-1][1]]`，但因为地毯长度是固定的 `carpetLen`，我们让 **窗口的右边界始终不超过左边界 + carpetLen**。  
   - 当窗口右端的区间 **完全在** 地毯范围内时，我们直接把整段长度计入答案（使用前缀和）。  
   - 当窗口右端的区间 **只能部分覆盖** 时，只把它与地毯的交集长度计入答案（直接算 `min(r, left+carpetLen-1) - l + 1`）。  
   - 每次左指针向右移动时，窗口宽度会缩小，右指针再向右尽可能扩张，整个过程只遍历一次 `tiles`，时间为 `O(n)`。

**二分搜索的另一种写法**  
如果不想写滑动窗口，也可以对每一个区间的左端 `li` 进行二分搜索，找出 **地毯右端 `li+carpetLen-1`** 第一次超过的区间下标，然后用前缀和快速求出完全覆盖的部分，再加上最后一个可能只覆盖部分的区间。二分搜索的时间是 `O(log n)`，整体 `O(n log n)`，同样足够快。

下面我们采用 **滑动窗口 + 前缀和** 的实现，因为它只需要一次遍历，最直观。

#### 代码（Python）

```python
from typing import List

def maximumWhiteTiles(tiles: List[List[int]], carpetLen: int) -> int:
    # 1. 按左端排序，确保区间从左到右依次出现
    tiles.sort(key=lambda x: x[0])

    n = len(tiles)
    # 2. 前缀和：pre[i] = 前 i 段区间的白砖总数（i 从 0 开始）
    pre = [0] * (n + 1)
    for i in range(n):
        l, r = tiles[i]
        pre[i + 1] = pre[i] + (r - l + 1)   # 区间长度是闭区间

    ans = 0
    right = 0   # 窗口右指针（指向第一个不在窗口里的区间）
    for left in range(n):
        # 确保右指针总是向右移动（窗口只会向右滑动）
        while right < n and tiles[right][1] <= tiles[left][0] + carpetLen - 1:
            # 区间 right 完全在地毯覆盖范围内，窗口可以继续向右扩张
            right += 1

        # 现在 tiles[right]（如果存在）是第一个“可能只被部分覆盖”的区间
        cur_cover = pre[right] - pre[left]   # 完全被覆盖的区间总长度

        # 处理可能的部分覆盖区间
        if right < n:
            # 地毯右端坐标
            carpet_end = tiles[left][0] + carpetLen - 1
            # 与 tiles[right] 的交集长度
            overlap = max(0, carpet_end - tiles[right][0] + 1)
            cur_cover += overlap

        ans = max(ans, cur_cover)

        # 当左指针左移离开当前窗口后，right 仍然指向上一次的右边界，
        # 因为窗口只会向右滑动，所以不需要把 right 向左收缩。
    return ans
```

**代码关键点解释（配合生活化类比）**

| 行号 | 作用 | 类比 |
|------|------|------|
| `tiles.sort(...)` | 把所有白砖排成一列，左边的在前，右边的在后 | 把所有顾客按到达时间排队 |
| `pre[i+1] = pre[i] + (r-l+1)` | 记录到第 `i` 位顾客为止，所有白砖的总数 | 累计每位顾客买的商品总价值 |
| `while right < n and tiles[right][1] <= ...` | 把窗口右边尽可能往右扩，直到出现“只能部分覆盖”的区间 | 把地毯往右铺，直到最后一块白砖只露出一点 |
| `cur_cover = pre[right] - pre[left]` | 直接算出窗口内**全部**被覆盖的白砖数 | 用累计的账单减去前面已经结算的账单，得到本次消费 |
| `overlap = max(0, carpet_end - tiles[right][0] + 1)` | 计算最后一个区间的**部分**覆盖长度 | 把地毯的末端伸到下一块白砖上，只能覆盖一小段 |

#### 复杂度

- **时间复杂度**：`O(n log n)`（排序）+ `O(n)`（滑动窗口遍历）= `O(n log n)`。  
  - 对比暴力的 `O(n²)`，`log n` 只比 `n` 小一点，但在 `n` 达到 5×10⁴ 时，`n²` 已经是 2.5 × 10⁹ 次操作，根本跑不完，而 `n log n` 只有约 8 × 10⁵ 次，轻松在一秒内完成。  
- **空间复杂度**：`O(n)`（前缀和数组），额外使用的变量都是常数级别。  
  - `O(n)` 可以理解为“我们需要额外记住每段白砖的累计长度”，这与原始输入同量级。

---

## 心得

- **核心技巧**：利用**排序 + 前缀和 + 滑动窗口**（或二分搜索）把“逐个统计”转化为“快速区间求和”。  
- **适用的类似题型**  
  1. *Maximum Number of Events That Can Be Attended*（区间覆盖最大值）  
  2. *Find the Smallest Subarray With a Given Sum*（子数组求和）  
  3. *Maximum Points Inside a Circle*（固定半径圆内点的最大数量）  
- **一句话总结解题钥匙**：**把“每次都遍历所有区间”改成“利用有序结构一次滑动，借助前缀和瞬间求和”。**

---

## 反思

- **第一反应**：直接把地毯左端往每个可能坐标搬，逐段检查覆盖情况——这就是暴力思路。  
- **最容易踩的坑**  
  - 忘记 **区间是闭区间**，导致交集长度少算或多算 `+1`。  
  - 只考虑了 `tiles[left][0]` 作为左端候选，却遗漏了左端可能在白砖内部的情况（其实滑动窗口已经自动涵盖）。  
  - 边界条件：`right` 越界时要先判断，否则会访问 `tiles[right]` 越界。  
- **下次遇到同类题**：第一步先 **排序**，然后思考“固定左端，右端如何快速移动？”——这通常暗示 **滑动窗口** 或 **二分搜索 + 前缀和** 的方向。