# #3208. 交替组 II / Alternating Groups II

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/alternating-groups-ii/)

---

## 题目（英文原版）

**Description**

There is a circle of red and blue tiles. You are given an array of integers colors and an integer k. The color of tile i is represented by colors[i]:
An alternating group is every k contiguous tiles in the circle with alternating colors (each tile in the group except the first and last one has a different color from its left and right tiles).
Return the number of alternating groups.
Note that since colors represents a circle, the first and the last tiles are considered to be next to each other.

**Examples**

**Example 1:**

```
Input: colors = [0,1,0,1,0], k = 3
Output: 3
Explanation:

Alternating groups:
```

**Example 2:**

```
Input: colors = [0,1,0,0,1,0,1], k = 6
Output: 2
Explanation:

Alternating groups:
```

**Example 3:**

```
Input: colors = [1,1,0,1], k = 4
Output: 0
Explanation:
```

**Constraints**

- 3 <= colors.length <= 105
- 0 <= colors[i] <= 1
- 3 <= k <= colors.length

---

## 题目（中文翻译）

有一圈由红色和蓝色方块组成的环形。给定整数数组 `colors` 与整数 `k`，其中 `colors[i]` 表示第 `i` 块方块的颜色（`0` 表示红色，`1` 表示蓝色）。  
交替组（alternating group）指环形中任意 `k` 个连续的方块，其颜色交替出现（即组内除首块和末块外的每块，其颜色都不同于左侧和右侧相邻的方块）。  
返回环形中交替组的数量。  
由于 `colors` 表示的是一个环形，首块与末块被视为相邻。

**示例 1**  
**示例 2**  
**示例 3**  

**示例**  

**示例 1**  
```text
Input: colors = [0,1,0,1,0], k = 3
Output: 3
Explanation:
交替组如下所示（每三个连续方块颜色交替）：
[0,1,0]、[1,0,1]、[0,1,0]
```

**示例 2**  
```text
Input: colors = [0,1,0,0,1,0,1], k = 6
Output: 2
Explanation:
交替组如下所示：
[0,1,0,0,1,0]（不满足交替条件） → 不是交替组  
[1,0,0,1,0,1]（不满足交替条件） → 不是交替组  
实际满足条件的交替组为两个，分别是：
[0,1,0,1,0,1]、[1,0,1,0,1,0]
```

**示例 3**  
```text
Input: colors = [1,1,0,1], k = 4
Output: 0
Explanation:
整个环形只有 4 块，颜色序列为 [1,1,0,1]，不存在满足交替条件的长度为 4 的连续子序列，因此返回 0。
```

**约束条件**  

- `3 <= colors.length <= 10^5`
- `0 <= colors[i] <= 1`
- `3 <= k <= colors.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有起点**，然后检查从该起点开始的 `k` 块是否满足“相邻颜色交替”。  
- **数据结构**：只需要原数组 `colors`，不需要额外的容器。可以把它想象成一条围成圆环的彩色地砖链，检查一段地砖时，只要把指针走到下一个位置并比较颜色即可。  
- **为什么正确**：对每一个可能的起点（共 `n` 个），我们都完整地验证了它后面的 `k‑1` 条相邻关系。如果全部不同，则这段恰好是一个交替组。遍历完所有起点后，得到的计数必然是答案。  
- **时间/空间复杂度**：  
  - **时间**：对每个起点我们要检查 `k‑1` 次相邻比较，总共 `n·(k‑1)` 次，记作 **O(n·k)**。这里的 `O` 只是一种上界的表示，实际含义是“随着 `n` 或 `k` 增大，运行时间会按它们的乘积增长”。  
  - **空间**：只用了常数个临时变量，**O(1)**。

#### 代码（Python）

```python
def countAlternatingGroups_bruteforce(colors, k):
    n = len(colors)
    ans = 0

    # 枚举所有可能的起点 i（0 ~ n-1）
    for i in range(n):
        ok = True                       # 假设这段是交替的
        # 检查从 i 开始的 k-1 条相邻关系
        for j in range(k - 1):
            cur = (i + j) % n           # 圆环的下标要取模
            nxt = (i + j + 1) % n
            if colors[cur] == colors[nxt]:   # 若相邻颜色相同，说明不是交替
                ok = False
                break
        if ok:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n·k)** — 需要遍历 `n` 个起点，每个起点检查 `k‑1` 次相邻颜色。  
- **空间复杂度**：**O(1)** — 只用到几个整数变量，不随输入规模增长。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**重复检查相同的相邻关系**。  
举例说明：如果我们已经知道 `colors[2] != colors[3]`，那么在检查起点 `2`、`3`、`4` … 时，这条信息会被重新比较很多次。  
为了消除这种冗余，我们把注意力放到**“相邻两块是否相同”**这件事本身上，而不是每次完整地遍历 `k` 块。

1. **把相邻关系抽象成一个布尔数组 `good`**  
   - `good[i] = 1` 表示 `colors[i]` 与 `colors[i+1]` 颜色不同（交替），  
   - `good[i] = 0` 表示颜色相同（不交替）。  
   把它想象成一本“检查手册”，每一页只记录两块之间是否满足交替。  
   对于环形，我们把 `colors` 复制一遍（`colors * 2`），这样即使检查跨越数组结尾的窗口，也能直接用下标访问。

2. **滑动窗口**  
   - 长度为 `k-1` 的窗口恰好覆盖了一段 `k` 块内部的所有相邻关系。  
   - 只要窗口里 **没有** `0`（即 `bad == 0`），说明这段 `k` 块全都是交替的。  
   - 当窗口向右移动一格时，只需要**加入新进来的 `good` 值**、**移除最左侧的 `good` 值**，并维护 `bad`（0 的个数）。这一步的时间是 **O(1)**。

3. **只统计起点在原数组范围内的窗口**  
   - 因为我们把数组复制了一遍，窗口的左端可以跑到 `2·n`。  
   - 当左端 `l` 小于 `n`（即起点仍然是原数组的一个位置）时，才把当前窗口的结果计入答案。

这样，每个 `good` 元素只会被加入和移除各一次，整体时间 **O(n)**，额外空间只需要存 `good`（长度约 `2·n`），即 **O(n)**，如果想进一步压缩空间，也可以在遍历时直接比较而不显式保存 `good`，这里为了思路清晰保留它。

#### 代码（Python）

```python
def countAlternatingGroups(colors, k):
    """
    使用滑动窗口统计长度为 k 的交替组数量。
    时间 O(n)，空间 O(n)（good 数组）。
    """
    n = len(colors)
    # 为了处理环，复制一遍，使得跨界访问不需要取模
    colors2 = colors * 2                # 长度 2n

    # 预处理相邻关系：good[i] = 1 表示 colors2[i] 与 colors2[i+1] 不同
    good = [0] * (2 * n - 1)            # 只需要到倒数第二个元素
    for i in range(2 * n - 1):
        good[i] = 1 if colors2[i] != colors2[i + 1] else 0

    window_len = k - 1                  # 窗口覆盖的相邻关系数
    bad = 0                             # 窗口内 0 的个数（不满足交替的相邻对）
    ans = 0
    left = 0

    # 右指针遍历整个 good 数组
    for right in range(2 * n - 1):
        # 把 new = good[right] 加入窗口
        if good[right] == 0:
            bad += 1

        # 当窗口长度超过要求时，收缩左边界
        if right - left + 1 > window_len:
            if good[left] == 0:
                bad -= 1
            left += 1

        # 此时窗口正好长度为 window_len
        if right - left + 1 == window_len:
            # 只统计起点在原数组范围内的窗口
            if left < n and bad == 0:   # 没有 0，说明 k 块全交替
                ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：**O(n)** — 每个相邻对只进入、离开窗口一次，整个过程线性扫描。与暴力解相比，省去了 `k` 倍的重复比较。  
- **空间复杂度**：**O(n)** — 需要存放 `good` 数组（长度约 `2·n`），如果把它压缩为常数空间，仍然可以做到 **O(1)**，但这里的写法更易于理解。

---  

## 心得  

- **核心技巧**：把“相邻是否相同”抽象为布尔数组，再用**固定长度滑动窗口**检查是否全部为 `1`。  
- **适用的题型**：  
  1. **环形/循环数组** 中的连续子段判定（如 “Circular Subarray with All Positive”）。  
  2. **相邻关系** 判定的窗口题（如 “Maximum Consecutive Ones” 的变形）。  
  3. **固定窗口内全部满足某条件** 的计数题（如 “Number of Subarrays with All Elements ≤ K”）。  
- **一句话总结解题钥匙**：把“交替”转化为“相邻对是否相同”，用长度为 `k‑1` 的滑动窗口，只要窗口里没有冲突即为合法组。

---  

## 反思  

- **第一反应**：看到“环形”和“交替”，立刻想到把数组复制一遍来处理跨界，然后暴力枚举每个起点。  
- **最容易踩的坑**：  
  - **环的跨界**：忘记对下标取模或复制数组会导致索引越界。  
  - **窗口长度**：交替组长度是 `k`，但窗口需要检查的是 `k‑1` 条相邻关系，容易写错。  
  - **起点范围**：滑动窗口在复制后的数组上会产生多余的起点，必须限制左端 `< n`。  
- **下次类似题的第一步**：先把“相邻关系”抽象为一个 0/1 序列（或前缀和），再决定使用**滑动窗口**还是**前缀和**来快速统计满足条件的子段。