# #1499. 方程的最大值 / Max Value of Equation

> 难度：困难 · 标签：Array、Queue、Sliding Window、Heap (Priority Queue)、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/max-value-of-equation/)

---

## 题目（英文原版）

**Description**

You are given an array points containing the coordinates of points on a 2D plane, sorted by the x-values, where points[i] = [xi, yi] such that xi < xj for all 1 <= i < j <= points.length. You are also given an integer k.
Return the maximum value of the equation yi + yj + |xi - xj| where |xi - xj| <= k and 1 <= i < j <= points.length.
It is guaranteed that there exists at least one pair of points that satisfy the constraint |xi - xj| <= k.

**Examples**

**Example 1:**

```
Input: points = [[1,3],[2,0],[5,10],[6,-10]], k = 1
Output: 4
Explanation: The first two points satisfy the condition |xi - xj| <= 1 and if we calculate the equation we get 3 + 0 + |1 - 2| = 4. Third and fourth points also satisfy the condition and give a value of 10 + -10 + |5 - 6| = 1.
No other pairs satisfy the condition, so we return the max of 4 and 1.
```

**Example 2:**

```
Input: points = [[0,0],[3,0],[9,2]], k = 3
Output: 3
Explanation: Only the first two points have an absolute difference of 3 or less in the x-values, and give the value of 0 + 0 + |0 - 3| = 3.
```

**Constraints**

- 2 <= points.length <= 105
- points[i].length == 2
- -108 <= xi, yi <= 108
- 0 <= k <= 2 * 108
- xi < xj for all 1 <= i < j <= points.length
- xi form a strictly increasing sequence.

---

## 题目（中文翻译）

给定一个数组 `points`，其中存放平面上点的坐标，且已按 **x** 坐标递增排序，`points[i] = [xi, yi]` 并满足对于所有 `1 <= i < j <= points.length` 都有 `xi < xj`。同时给定一个整数 `k`。  
返回满足 `|xi - xj| <= k` 且 `1 <= i < j <= points.length` 的所有点对 `(i, j)` 中，表达式 `yi + yj + |xi - xj|` 的最大值。  

题目保证至少存在一对点满足约束 `|xi - xj| <= k`。

## 示例

### 示例 1
**输入**  
``` 
points = [[1,3],[2,0],[5,10],[6,-10]], k = 1
```
**输出**  
```
4
```
**解释**  
前两个点的 `|xi - xj|` 为 `1`，满足条件，计算得到 `3 + 0 + |1 - 2| = 4`。  
第三个和第四个点也满足条件，得到的值为 `10 + (-10) + |5 - 6| = 1`。  
没有其他点对满足条件，故返回 `max(4, 1) = 4`。

### 示例 2
**输入**  
``` 
points = [[0,0],[3,0],[9,2]], k = 3
```
**输出**  
```
3
```
**解释**  
只有前两个点的 **x** 坐标差的绝对值不超过 `3`，其计算结果为 `0 + 0 + |0 - 3| = 3`。

## 约束条件
- `2 <= points.length <= 10^5`
- `points[i].length == 2`
- `-10^8 <= xi, yi <= 10^8`
- `0 <= k <= 2 * 10^8`
- 对所有 `1 <= i < j <= points.length`，都有 `xi < xj`
- `xi` 构成严格递增序列。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有点两两配对，逐个检查它们之间的 `x` 差是否不超过 `k`，如果满足，就把公式  

\[
yi + yj + |xi - xj|
\]

算出来，取最大的那个。  

- **使用的数据结构**：只需要一个普通的列表（`list`）来保存 `points`，再用两层 `for` 循环遍历所有 `(i, j)` 组合。  
- **生活化类比**：把每个点想成一张卡片，暴力解就是把所有卡片排成一行，然后让每两张卡片站在一起聊天，看看它们的聊天分数（公式值）有多高。  
- **为什么一定正确**：我们枚举了**所有**满足 `i < j` 且 `|xi - xj| ≤ k` 的配对，最大值自然不会漏掉。  

#### 代码（Python）

```python
from typing import List

def findMaxValueOfEquation_bruteforce(points: List[List[int]], k: int) -> int:
    """
    暴力解：两层循环枚举所有点对
    """
    n = len(points)
    ans = -10**18                     # 先设一个很小的值
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            if xj - xi > k:           # 因为 points 已经按 x 升序，后面的点只会更远
                break                # 直接跳出内层循环，省点时间
            # 计算公式值
            cur = yi + yj + (xj - xi)   # xi < xj 所以 |xi-xj| = xj - xi
            ans = max(ans, cur)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “平方”可以想象成如果有 1000 个点，暴力会检查大约 1000×1000 = 100 万次。  
- **空间复杂度**：`O(1)`（只用了常数级别的额外变量）

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有之前的点**，这导致 `O(n²)` 的时间。  
观察公式并利用题目给出的 **x 坐标严格递增** 的特性，可以把它改写成：

\[
\begin{aligned}
yi + yj + |xi - xj|
&= yi + yj + (xj - xi) \quad (\text{因为 } xi < xj)\\
&= (yi - xi) + (yj + xj)
\end{aligned}
\]

对每个 **当前点 j**，只要知道在它左侧、且满足 `xj - xi ≤ k` 的点中，`yi - xi` 的最大值，就可以在 **O(1)** 时间算出该 `j` 对应的最优配对值。

因此问题转化为：

> 在一个随时间（`x`）滑动的窗口里，实时维护 `yi - xi` 的最大值。

这正好可以用**单调队列**或**最大堆（优先队列）**来实现。这里按照提示使用最大堆：

1. **堆中存放** `(yi - xi, xi)`。堆顶永远是当前窗口里 `yi - xi` 最大的点。  
2. 当遍历到第 `j` 个点时，先把所有 **超出窗口**（即 `xj - xi > k`）的堆顶元素弹出。  
3. 此时堆顶就是窗口内 `yi - xi` 的最大值，计算  
   \[
   \text{candidate} = (\text{堆顶的 } yi - xi) + yj + xj
   \]  
   更新答案。  
4. 最后把当前点 `(yj - xj, xj)` 加入堆中，继续向后遍历。

> **为什么堆能工作？**  
> 堆是一种“随时能拿到最大值”的数据结构，和我们要的“窗口最大值”需求完全匹配。弹出不在窗口的元素，只需要检查堆顶的 `xi` 是否太老即可。

如果想把复杂度进一步降到 `O(n)`，可以使用 **单调递减队列**（deque），但这里先用更直观的堆来说明。

#### 代码（Python）

```python
import heapq
from typing import List

def findMaxValueOfEquation(points: List[List[int]], k: int) -> int:
    """
    最优解：使用最大堆（优先队列）维护滑动窗口内的最大 (yi - xi)
    """
    # Python 的 heapq 是最小堆，存负数即可模拟最大堆
    max_heap = []               # 每个元素是 (- (yi - xi), xi)
    ans = -10**18               # 记录全局最大值

    for xj, yj in points:       # 按 x 的升序遍历（题目已保证）
        # 1. 弹出所有已经超出窗口的点
        while max_heap and xj - max_heap[0][1] > k:
            heapq.heappop(max_heap)

        # 2. 若堆非空，则堆顶对应的 (yi - xi) 为当前窗口的最大值
        if max_heap:
            # 取负号恢复真实的 yi - xi
            best_yi_minus_xi = -max_heap[0][0]
            cur = best_yi_minus_xi + yj + xj   # 公式 (yi - xi) + (yj + xj)
            ans = max(ans, cur)

        # 3. 把当前点加入堆中，供后面的点使用
        #    注意这里存的是 -(yi - xi) 让堆成为最大堆
        heapq.heappush(max_heap, (-(yj - xj), xj))

    return ans
```

> **代码要点注释**  
> - `heapq.heappush` / `heappop` 分别是“往堆里放”与“从堆里取”。  
> - `-(yj - xj)` 把原本要找的最大值变成最小堆的最小值（负数越大，原值越大）。  
> - `while` 循环保证堆里只保留 **合法**（`xj - xi ≤ k`）的点。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 每个点最多进堆一次、出堆一次，堆的操作是 `log n`，所以整体是 `n log n`。  
  - 与暴力的 `O(n²)` 相比，**对数**级的增长要慢得多。比如 `n=10⁵` 时，`n²` 是 10⁰¹⁰，而 `n log n` 只约 1.7×10⁶。  
- **空间复杂度**：`O(n)`（最坏情况下堆里可能保存所有点）  
  - 实际上因为窗口宽度受 `k` 限制，堆的大小往往远小于 `n`。

> 如果使用 **单调递减队列**（deque）实现，同样可以把时间降到 `O(n)`，空间仍是 `O(k)`（窗口大小），感兴趣的同学可以自行尝试。

---

## 心得  

- **核心技巧**：把原公式拆解为两部分，其中一部分只与左侧点有关，另一部分只与当前点有关，转化为“滑动窗口最大值”。  
- **适用场景**  
  1. **LeetCode 239. Sliding Window Maximum** – 需要在窗口内实时获取最大值。  
  2. **LeetCode 862. Shortest Subarray with Sum at Least K** – 使用单调队列维护前缀和的最小值。  
  3. **LeetCode 1696. Jump Game VI** – 同样把 DP 转化为窗口最大值问题。  
- **一句话总结**：**把“两点之间的函数”拆成 “左点的贡献 + 右点的贡献”，再用滑动窗口最大值来快速求最优左点**。

---

## 反思  

- **第一反应**：看到 `|xi - xj|`，立刻想到把点按 `x` 排序后用双指针或滑动窗口。  
- **最容易踩的坑**  
  - 忘记 `xi < xj` 已经保证了 `|xi - xj| = xj - xi`，导致公式拆解出错。  
  - 在使用堆时，没有及时弹出超出窗口的元素，导致堆顶可能是非法点，答案会被低估。  
  - 处理负数时忘记恢复符号，导致计算出错。  
- **下次遇到同类题**：第一步先**改写公式**，看看能否把变量分离成 “只依赖左边” 与 “只依赖右边”，然后考虑 **滑动窗口 + 单调结构**（堆或 deque）来维护左边的最优值。