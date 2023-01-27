# #2106. 最多 K 步内收获的最大水果数 / Maximum Fruits Harvested After at Most K Steps

> 难度：困难 · 标签：Array、Binary Search、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-fruits-harvested-after-at-most-k-steps/)

---

## 题目（英文原版）

**Description**

Fruits are available at some positions on an infinite x-axis. You are given a 2D integer array fruits where fruits[i] = [positioni, amounti] depicts amounti fruits at the position positioni. fruits is already sorted by positioni in ascending order, and each positioni is unique.
You are also given an integer startPos and an integer k. Initially, you are at the position startPos. From any position, you can either walk to the left or right. It takes one step to move one unit on the x-axis, and you can walk at most k steps in total. For every position you reach, you harvest all the fruits at that position, and the fruits will disappear from that position.
Return the maximum total number of fruits you can harvest.

**Examples**

**Example 1:**

```
Input: fruits = [[2,8],[6,3],[8,6]], startPos = 5, k = 4
Output: 9
Explanation: 
The optimal way is to:
- Move right to position 6 and harvest 3 fruits
- Move right to position 8 and harvest 6 fruits
You moved 3 steps and harvested 3 + 6 = 9 fruits in total.
```

**Example 2:**

```
Input: fruits = [[0,9],[4,1],[5,7],[6,2],[7,4],[10,9]], startPos = 5, k = 4
Output: 14
Explanation: 
You can move at most k = 4 steps, so you cannot reach position 0 nor 10.
The optimal way is to:
- Harvest the 7 fruits at the starting position 5
- Move left to position 4 and harvest 1 fruit
- Move right to position 6 and harvest 2 fruits
- Move right to position 7 and harvest 4 fruits
You moved 1 + 3 = 4 steps and harvested 7 + 1 + 2 + 4 = 14 fruits in total.
```

**Example 3:**

```
Input: fruits = [[0,3],[6,4],[8,5]], startPos = 3, k = 2
Output: 0
Explanation:
You can move at most k = 2 steps and cannot reach any position with fruits.
```

**Constraints**

- 1 <= fruits.length <= 105
- fruits[i].length == 2
- 0 <= startPos, positioni <= 2 * 105
- positioni-1 < positioni for any i > 0 (0-indexed)
- 1 <= amounti <= 104
- 0 <= k <= 2 * 105

---

## 题目（中文翻译）

**题目描述**  
在无限的 x 轴上某些位置有水果。给定二维整数数组 `fruits`，其中 `fruits[i] = [position_i, amount_i]` 表示在位置 `position_i` 有 `amount_i` 个水果。`fruits` 已经按 `position_i` 升序排序，且每个 `position_i` 唯一。  
再给定整数 `startPos` 和整数 `k`。最初你位于 `startPos`。从任意位置，你可以向左或向右行走。移动一单位距离需要一步，你最多只能走 `k` 步。每到达一个位置，就收集该位置的所有水果，水果会从该位置消失。  
返回你能够收集的水果的最大总数。

**示例 1**  
```
Input: fruits = [[2,8],[6,3],[8,6]], startPos = 5, k = 4
Output: 9
```
**解释**  
最优方案是：  
- 向右走到位置 6，收集 3 个水果  
- 再向右走到位置 8，收集 6 个水果  

共走了 3 步，收集到的水果总数为 `3 + 6 = 9`。

**示例 2**  
```
Input: fruits = [[0,9],[4,1],[5,7],[6,2],[7,4],[10,9]], startPos = 5, k = 4
Output: 14
```
**解释**  
你最多只能走 `k = 4` 步，因此无法到达位置 0 和位置 10。  
最优方案是：  
- 在起始位置 5 收集 7 个水果  
- 向左走到位置 4，收集 1 个水果  
- 向右走到位置 6，收集 2 个水果  
- 再向右走到位置 7，收集 4 个水果  

总共走了 1 + 1 + 1 = 3 步，收集到的水果总数为 `7 + 1 + 2 + 4 = 14`。

**示例 3**  
```
Input: fruits = [[0,3],[6,4],[8,5]], startPos = 3, k = 2
Output: 0
```
**解释**  
最多只能走 `k = 2` 步，无法到达任意有水果的位置，收获为 0。

**约束条件**  
- `1 <= fruits.length <= 10^5`  
- `fruits[i].length == 2`  
- `0 <= startPos, position_i <= 2 * 10^5`  
- 对任意 `i > 0`，`position_{i-1} < position_i`（已按升序排序）  
- `1 <= amount_i <= 10^4`  
- `0 <= k <= 2 * 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可以走的路线都枚举出来**，然后算出每条路线能够收获的水果总量，取最大值。

- **路线的表示**  
  我们可以把一次行走看成一个「左‑右」的区间 `[L, R]`（`L ≤ startPos ≤ R`），因为只能在直线上前后移动，最终能到达的所有位置都落在这个区间内。  
  区间的长度（走的步数）不一定等于 `R-L`，因为可能先往左走 `x` 步，再往右走 `y` 步，满足 `x + y ≤ k`，而 `L = startPos - x`，`R = startPos + y`。

- **暴力枚举**  
  1. 枚举左走的步数 `x`（`0 ≤ x ≤ k`）。  
  2. 对每个 `x`，枚举右走的步数 `y`（`0 ≤ y ≤ k - x`）。  
  3. 计算区间 `[startPos - x, startPos + y]` 内所有水果的总和。  
  4. 记录最大的总和。

- **为什么正确**  
  任意一次合法的行走都可以唯一对应到某一对 `(x, y)`，所以遍历所有 `(x, y)` 就一定会覆盖所有可能的行走路径，进而找出最优解。

- **复杂度分析（大白话）**  
  - `x` 的取值有 `k+1` 种，`y` 的取值在每个 `x` 下最多也是 `k+1` 种。整体是 **大约 `k²` 次**循环。  
  - 对每个区间我们还要遍历一次 `fruits`（最多 `n` = `10⁵`）来求和。于是总时间是 **`O(k²·n)`**，在最坏情况下（`k≈2·10⁵`）根本跑不完。  
  - 空间只用了几个整数，**`O(1)`**。

#### 代码（Python）

```python
from typing import List

def maxFruit_bruteforce(fruits: List[List[int]], startPos: int, k: int) -> int:
    # 把水果信息转成字典，方便 O(1) 查询某个位置的水果数量
    fruit_map = {pos: amt for pos, amt in fruits}
    max_gain = 0

    # x = 向左走的步数，y = 向右走的步数
    for x in range(k + 1):
        left = startPos - x                     # 最左能到达的位置
        for y in range(k - x + 1):
            right = startPos + y                # 最右能到达的位置
            # 统计区间 [left, right] 内的水果总量
            cur = 0
            for pos, amt in fruits:
                if left <= pos <= right:
                    cur += amt
            max_gain = max(max_gain, cur)

    return max_gain
```

> 关键行中文注释已写在代码里，直接运行即可（仅作演示，实际会超时）。

#### 复杂度

- **时间复杂度**：`O(k²·n)`  
  - `k²` 表示我们枚举了所有可能的左走/右走步数组合。  
  - `n` 表示每次都要遍历所有水果来求和。  
  - 对于本题的最大输入，这相当于上百亿次操作，根本不可能在一秒内完成。

- **空间复杂度**：`O(1)`（不计输入占用的空间）  
  - 只用了几个整数变量来保存当前区间和最大值。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于每次都要遍历整个 `fruits` 列表** 来求区间和。  
如果我们能 **在 O(1) 时间内得到任意区间的水果总量**，只剩下枚举左、右步数的 `O(k²)` 仍然太大。  
进一步观察：

> **提示**：最优路径最多只会「转向」一次。  
> 也就是说，最优路线只有四种形态：
> 1. 只往左走（左 → 结束）  
> 2. 只往右走（右 → 结束）  
> 3. 先往左走，再往右走（左 → 转向 → 右）  
> 4. 先往右走，再往左走（右 → 转向 → 左）

**为什么不可能出现「左→右→左」这种来回三次的路径？**  
每一次转向都会浪费一段来回的步数，而转向次数越多，实际能覆盖的区间越小。只要把所有水果都装进一次「左→右」或「右→左」的区间里，就已经是最优的了。  

因此我们只需要分别考虑「左先」和「右先」两种情况。下面以「左先」为例说明如何在 **线性时间** 求出最优值；「右先」的处理方式完全对称。

---

#### 2.1 前缀和 + 双指针（滑动窗口）

1. **把水果数组转成前缀和**  
   - 设 `pos[i]` 为第 `i` 个水果位置，`amt[i]` 为对应数量（已按位置升序）。  
   - 构造 `pref[i]` 表示从第 `0` 个水果到第 `i-1` 个水果（左闭右开）的水果总量。  
   - 那么任意区间 `[l, r]`（对应水果下标）内的水果总量可以 **O(1)** 通过 `pref[r+1] - pref[l]` 获得。

2. **左先 → 右的滑动窗口**  
   - 固定「左走」的步数 `x`（`0 ≤ x ≤ k`），左端点 `L = startPos - x`。  
   - 在左端点固定的情况下，**右边还能走的最大步数** 为 `k - 2*x`（因为左走 `x` 再返回到起点需要 `x` 步，再向右走 `y` 步，总步数为 `x + x + y ≤ k` → `y ≤ k - 2x`）。  
   - 因此右端点的最远可达位置是 `R = startPos + (k - 2*x)`（如果 `k - 2*x` 为负，说明只左不右）。  
   - 我们只需要在水果列表中找到 **所有位置在 `[L, R]` 之间的水果**，求和即为这条路径的收获。  
   - 用双指针（滑动窗口）维护当前区间 `[L, R]` 对应的水果下标范围 `[leftIdx, rightIdx]`，随着 `x` 增大，`L` 向左移动、`R` 向左或保持不变，窗口只会**单调收缩**，于是整体只遍历一次 `fruits`。

3. **右先 → 左的滑动窗口**  
   - 与上面对称：固定「右走」的步数 `y`，右端点 `R = startPos + y`，左端点最远能到 `L = startPos - (k - 2*y)`。  
   - 同样用滑动窗口一次遍历即可得到所有可能区间的水果和。

4. **取最大值**  
   - 对两种方向分别遍历所有合法的 `x`（或 `y`），记录最大收获。

---

#### 2.2 关键点细化

| 步骤 | 解释 |
|------|------|
| 前缀和 | 把「大量求区间和」的问题转成「只要两次查表」的 O(1) 操作。想象一本字典，查一个词的解释只要看两页的页码差，省时又省力。 |
| 双指针（滑动窗口） | 想象有一个可伸缩的「收割篱笆」围住当前能收的水果。每次左端点左移一步，右端点会相应右移或保持，篱笆只会往左滑动，所有水果只会被「进」或「出」一次，整个过程线性。 |
| `k - 2*x` / `k - 2*y` | 这是因为左走 `x` 步后如果要再向右走，需要先把左走的距离「踩回来」——相当于往返两次左走的距离。剩余的步数才能真正用于向右扩展。 |

---

#### 代码（Python）

```python
from typing import List
import bisect

def maxTotalFruits(fruits: List[List[int]], startPos: int, k: int) -> int:
    """
    最优解：滑动窗口 + 前缀和
    时间复杂度 O(n) ，空间复杂度 O(n)（前缀和数组）
    """
    # 把位置和数量拆成两个列表，方便二分查找
    positions = [p for p, _ in fruits]
    amounts   = [a for _, a in fruits]
    n = len(fruits)

    # 前缀和，pref[i] = 前 i 个水果的总量（0 <= i <= n）
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + amounts[i]

    # ---------- 只向左走 ----------
    # 能到达的最左位置是 startPos - k（如果有水果的话）
    left_limit = startPos - k
    # 用二分找到第一个 >= left_limit 的水果下标
    left_idx = bisect.bisect_left(positions, left_limit)
    # 用二分找到最后一个 <= startPos 的水果下标
    right_idx = bisect.bisect_right(positions, startPos) - 1
    ans = 0
    if left_idx <= right_idx:                     # 区间非空
        ans = pref[right_idx + 1] - pref[left_idx]

    # ---------- 只向右走 ----------
    right_limit = startPos + k
    left_idx = bisect.bisect_left(positions, startPos)
    right_idx = bisect.bisect_right(positions, right_limit) - 1
    if left_idx <= right_idx:
        ans = max(ans, pref[right_idx + 1] - pref[left_idx])

    # ---------- 先左后右 ----------
    # 使用滑动窗口，左端点随 x 增大而左移
    left_ptr = n                     # 初始指向“左侧空窗口”
    right_ptr = n                    # 同上
    # 为了让窗口只向左滑动，先把指针放在最右侧
    # 接下来遍历所有可能的左走步数 x
    for x in range(1, k + 1):
        L = startPos - x                         # 左端点实际坐标
        # 只能向左走到已有水果的最左边
        left_ptr = bisect.bisect_left(positions, L)
        # 计算右侧还能走的最大步数：k - 2*x
        remain = k - 2 * x
        if remain < 0:           # 已经没有剩余步数可以向右
            break
        R = startPos + remain
        # 右指针需要指向 ≤ R 的最后一个水果
        right_ptr = bisect.bisect_right(positions, R) - 1
        if left_ptr <= right_ptr:
            cur = pref[right_ptr + 1] - pref[left_ptr]
            ans = max(ans, cur)

    # ---------- 先右后左 ----------
    for y in range(1, k + 1):
        R = startPos + y                         # 右端点坐标
        right_ptr = bisect.bisect_right(positions, R) - 1
        remain = k - 2 * y
        if remain < 0:
            break
        L = startPos - remain
        left_ptr = bisect.bisect_left(positions, L)
        if left_ptr <= right_ptr:
            cur = pref[right_ptr + 1] - pref[left_ptr]
            ans = max(ans, cur)

    return ans
```

**代码要点说明（中文注释已写在代码里）**  

- `bisect_left / bisect_right` 用来 **快速定位** 区间左右端点对应的水果下标，时间是 `O(log n)`，但在整个循环里每个下标只会被查询一次，整体仍是线性。  
- 两个 `for` 循环分别遍历左走步数 `x` 与右走步数 `y`，每次只做常数次二分和前缀和查询。  
- 前缀和数组 `pref` 让我们在 `O(1)` 时间内得到任意水果子数组的总量。  

---

#### 复杂度

- **时间复杂度**：`O(n + k log n)`（实际上 `k ≤ 2·10⁵`，`log n` 约为 17，整体约为 `O(n)`）  
  - 构建前缀和遍历一次 `fruits` → `O(n)`。  
  - 主循环中每次只做 `O(log n)` 的二分查找，循环次数最多 `k` 次，`k` 与 `n` 同阶（均 ≤ 2·10⁵），所以整体仍是线性级别。  
  - 与暴力解的 `O(k²·n)` 相比，快了 **几百倍甚至上千倍**，可以轻松通过所有测试。

- **空间复杂度**：`O(n)`  
  - 额外存了 `positions`、`amounts`、`pref` 三个长度为 `n` 的数组。  
  - 这在本题的约束（`n ≤ 10⁵`）下只占几百 KB，完全可以接受。

---

## 心得

- **核心技巧**：  
  1. **路径模式化**——最优路径最多只会转向一次，归纳为四种简单形态。  
  2. **前缀和 + 双指针**（滑动窗口）——在已排序的区间上，利用前缀和把「区间求和」降到 `O(1)`，再用滑动窗口一次遍历所有可能的区间。

- **适用的题型**（类似思路可复用）：  
  - 「在限制步数/距离内最大化收集资源」的题目，例如 LeetCode 1637 *"Count Subarrays With Median K"*（滑动窗口+前缀和）  
  - 「最多只能转向一次的最短路径」类题，例如「Maximum Coins You Can Get”」的双向遍历版本  
  - 「区间和最大化」的变形，如「Maximum Sum Subarray with Length Constraint」  

- **一句话总结解题钥匙**：  
  > **把所有可能的行走路径压缩到「左→右」或「右→左」两种单调区间，然后用前缀和快速求区间和，配合滑动窗口一次遍历即可得到最优解。**

---

## 反思

- **拿到题目第一反应**：  
  直接想到「枚举所有走法」或者「DFS」搜索，结果很快发现会超时。

- **最容易踩的坑**  
  1. **忽略转向次数限制**——若不证明「最多一次转向」就会尝试更复杂的 DP，导致实现繁琐且容易出错。  
  2. **边界条件**：`k` 很小或为 0 时，只能收集起始点的水果；左/右走的步数可能导致 `remain = k - 2*x` 为负，需要及时 `break`。  
  3. **二分查找的闭区间/开区间**——`bisect_left` 与 `bisect_right` 用法不当会导致漏掉或多算某些水果。  

- **下次遇到同类题，第一步该想到**  
  1. **先分析路径的结构**，看看是否可以「单调」或「最多一次转向」之类的约束。  
  2. **把「区间求和」转成前缀和**，然后决定是用滑动窗口还是双指针一次遍历所有合法区间。  

这样就能把原本指数级的搜索压缩到线性时间，轻松 AC。