# #1739. 构建盒子 / Building Boxes

> 难度：困难 · 标签：Math、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/building-boxes/)

---

## 题目（英文原版）

**Description**

You have a cubic storeroom where the width, length, and height of the room are all equal to n units. You are asked to place n boxes in this room where each box is a cube of unit side length. There are however some rules to placing the boxes:
Given an integer n, return the minimum possible number of boxes touching the floor.

**Examples**

**Example 1:**

```
Input: n = 3
Output: 3
Explanation: The figure above is for the placement of the three boxes.
These boxes are placed in the corner of the room, where the corner is on the left side.
```

**Example 2:**

```
Input: n = 4
Output: 3
Explanation: The figure above is for the placement of the four boxes.
These boxes are placed in the corner of the room, where the corner is on the left side.
```

**Example 3:**

```
Input: n = 10
Output: 6
Explanation: The figure above is for the placement of the ten boxes.
These boxes are placed in the corner of the room, where the corner is on the back side.
```

**Constraints**

- 1 <= n <= 109

---

## 题目（中文翻译）

**描述**  
你有一个宽、长、高均为 `n` 单位的立方体储藏室（cubic storeroom）。需要在该房间内放置 `n` 个盒子（box），每个盒子都是边长为 1 单位的单元立方体（unit cube）。放置盒子需要遵守以下规则：

给定整数 `n`，返回**最少**有多少个盒子会接触地面（touching the floor）。

**示例 1**  
**输入**: `n = 3`  
**输出**: `3`  
**解释**: 上图展示了三个盒子的放置方式。它们被放在房间的一个角落，角落位于左侧。

**示例 2**  
**输入**: `n = 4`  
**输出**: `3`  
**解释**: 上图展示了四个盒子的放置方式。它们被放在房间的一个角落，角落位于左侧。

**示例 3**  
**输入**: `n = 10`  
**输出**: `6`  
**解释**: 上图展示了十个盒子的放置方式。它们被放在房间的一个角落，角落位于后侧。

**约束条件**  
- `1 <= n <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有箱子都直接摆在地面**，这样所有 `n` 个箱子都接触地面，答案就是 `n`。  
这显然不是最小值，但它把问题的本质给暴露出来了：

- 我们可以把箱子 **堆叠**，让上面的箱子不直接接触地面，只需要下面有箱子支撑。
- 只要把箱子堆得够高，就能用更少的地面箱子容纳同样数量的箱子。

把箱子堆成“层”的概念最容易理解：  
第一层（最底层）放在地面，第二层必须完全坐落在第一层的箱子之上，第三层坐落在第二层之上……  
这就像 **一层层的砖**，每层的面积只能比它下面那层小（或者相等），否则上面的箱子会“悬空”。  

**数据结构**：这里不需要额外的数据结构，只要会算**等差数列的和**（也叫三角数）就行。  
把等差数列想象成 **排队买票的队伍**：第 1 个人排 1 队，第二个人排 2 队，…… 第 `m` 个人排 `m` 队，总人数就是 `1 + 2 + … + m`。

**为什么这个想法是对的**  
假设我们在地面上放了 `m` 个箱子（`m` 叫 **底层箱子数**），为了让箱子尽可能多，我们会把第二层也摆成一个 **“尽可能长”的序列**：  
- 第二层最多可以放 `m‑1` 个箱子（因为最右边的那格下面已经没有箱子可以支撑了），
- 第三层最多放 `m‑2` 个，  
- ……  
- 第 `m` 层最多放 `1` 个。

于是 **在给定 `m` 的情况下，能放的箱子总数** 就是  

```
maxBoxes(m) = m + (m‑1) + (m‑2) + … + 1 = m·(m+1) / 2
```

这正是等差数列求和公式，也叫 **三角数**。只要 `maxBoxes(m) ≥ n`，说明我们可以只用 `m` 个底层箱子把 `n` 个箱子全部摆进去。

#### 代码（Python）

```python
def max_boxes(m: int) -> int:
    """
    给定底层箱子数 m，返回最多可以摆放的箱子总数。
    公式来源于等差数列求和：1 + 2 + … + m = m·(m+1)//2
    """
    return m * (m + 1) // 2
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做一次乘法/除法运算，和 `n` 的大小无关。  
- **空间复杂度**：`O(1)` —— 只使用常数个整数变量。

---

### 2. 最优解

#### 思路  

暴力解已经把 **“在底层放 m 个箱子时，最多能放多少箱子”** 这一步算清楚了。  
接下来要解决的核心问题是：

> **找最小的 `m` 使得 `maxBoxes(m) ≥ n`。**

这一步是 **单调函数的逆问题**：  
`maxBoxes(m)` 随着 `m` 单调递增（`m` 越大，能放的箱子越多），所以答案一定是一个**最左侧**满足条件的 `m`。

寻找单调递增函数的最小满足点，最常用的技巧是 **二分搜索**（Binary Search）：

1. **搜索区间**  
   - 最小可能的 `m` 是 `1`（至少要放一个箱子在地面）。  
   - 最大可能的 `m` 不会超过 `n`，因为把所有箱子都放在地面就是一种合法方案。  

2. **二分过程**  
   - 取中点 `mid = (lo + hi) // 2`。  
   - 计算 `max_boxes = max_boxes(mid)`。  
   - 如果 `max_boxes >= n`，说明 `mid` 已经够用了，答案可能更小，继续在左半边搜索 `hi = mid`。  
   - 否则 `mid` 不够，需要更多底层箱子，搜索右半边 `lo = mid + 1`。  

3. 循环结束时 `lo == hi`，即为最小满足条件的 `m`。

**为什么二分能工作**  
二分的前提是**单调性**：`max_boxes(m)` 随 `m` 增大而不减小，这在等差数列求和公式里显而易见。  
每次比较都可以把搜索区间排除掉一半，时间复杂度是 `O(log n)`。

#### 代码（Python）

```python
def min_floor_boxes(n: int) -> int:
    """
    在边长为 n 的立方体房间里放 n 个 1×1×1 的箱子，
    求最少需要多少个箱子接触地面（即底层箱子数）。
    思路：二分搜索最小的 m 使得 m·(m+1)/2 ≥ n。
    """
    lo, hi = 1, n          # 答案一定在 [1, n] 之间
    while lo < hi:
        mid = (lo + hi) // 2
        # 计算放置 mid 个底层箱子时最多能放多少箱子
        if mid * (mid + 1) // 2 >= n:
            hi = mid        # 右边界收缩，尝试更小的 m
        else:
            lo = mid + 1    # 左边界收缩，需要更多底层箱子
    return lo                # lo == hi，即为答案
```

**代码要点注释**：

- `mid * (mid + 1) // 2`：等差数列求和，避免使用浮点数，防止精度错误。  
- `while lo < hi`：循环结束条件恰好是搜索区间只剩一个数。  
- `return lo`：此时 `lo` 已经是满足 `maxBoxes(lo) ≥ n` 的最小整数。

#### 复杂度

- **时间复杂度**：`O(log n)` —— 二分搜索的迭代次数为 `log₂ n`（最多约 30 次，因为 `n ≤ 10⁹`）。  
- **空间复杂度**：`O(1)` —— 只使用了几个整数变量。

---

## 心得

- **核心技巧**：把“最小满足条件的整数”转化为 **单调函数的逆问题**，使用 **二分搜索** 快速定位答案。  
- **适用场景**：  
  1. 给定容量上限，求最小资源量（如最少的机器、最少的天数）。  
  2. “把 n 件物品装进最少的箱子”，只要能够写出 **“给定箱子数，最多能装多少”** 的单调函数。  
  3. “在限定时间内完成任务的最小机器数”等类似的 **最小化** / **最大化** 逆向问题。  

- **一句话总结**：**把“多少能装”写成单调函数，用二分找到最左侧满足条件的点**。

---

## 反思

- **第一反应**：把所有箱子直接放在地面，答案是 `n`。这把问题转化为“如何利用堆叠”后才看到优化空间。  
- **最容易踩的坑**  
  1. **漏掉单调性**：如果写错了 `max_boxes(m)`（比如把递减写成递增），二分会失效。  
  2. **整数溢出**：`m*(m+1)` 可能超过 32 位整数范围，务必使用 Python 的大整数或在语言里使用 `long long`。  
  3. **边界条件**：`n = 1` 时答案应为 `1`，二分区间必须包含 `1`，否则会出现无限循环或错误答案。  

- **下次遇到同类题**：第一步先**写出“给定资源量，最多能完成多少任务”的单调函数；第二步判断是否可以二分（或其他单调搜索），再正式实现。这样思路清晰，代码也容易写对。