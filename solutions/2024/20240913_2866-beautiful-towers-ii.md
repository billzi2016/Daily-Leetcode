# #2866. 美丽塔 II / Beautiful Towers II

> 难度：中等 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/beautiful-towers-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array maxHeights of n integers.
You are tasked with building n towers in the coordinate line. The ith tower is built at coordinate i and has a height of heights[i].
A configuration of towers is beautiful if the following conditions hold:
Array heights is a mountain if there exists an index i such that:
Return the maximum possible sum of heights of a beautiful configuration of towers.

**Examples**

**Example 1:**

```
Input: maxHeights = [5,3,4,1,1]
Output: 13
Explanation: One beautiful configuration with a maximum sum is heights = [5,3,3,1,1]. This configuration is beautiful since:
- 1 <= heights[i] <= maxHeights[i]  
- heights is a mountain of peak i = 0.
It can be shown that there exists no other beautiful configuration with a sum of heights greater than 13.
```

**Example 2:**

```
Input: maxHeights = [6,5,3,9,2,7]
Output: 22
Explanation: One beautiful configuration with a maximum sum is heights = [3,3,3,9,2,2]. This configuration is beautiful since:
- 1 <= heights[i] <= maxHeights[i]
- heights is a mountain of peak i = 3.
It can be shown that there exists no other beautiful configuration with a sum of heights greater than 22.
```

**Example 3:**

```
Input: maxHeights = [3,2,5,5,2,3]
Output: 18
Explanation: One beautiful configuration with a maximum sum is heights = [2,2,5,5,2,2]. This configuration is beautiful since:
- 1 <= heights[i] <= maxHeights[i]
- heights is a mountain of peak i = 2. 
Note that, for this configuration, i = 3 can also be considered a peak.
It can be shown that there exists no other beautiful configuration with a sum of heights greater than 18.
```

**Constraints**

- 1 <= n == maxHeights.length <= 105
- 1 <= maxHeights[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `maxHeights`，长度为 `n`。  
你需要在数轴上建造 `n` 座塔。第 `i` 座塔建在坐标 `i`，其高度为 `heights[i]`。

如果满足以下条件，则称该塔的配置是 **美丽的**（beautiful）：

1. 对所有 `i`，`1 <= heights[i] <= maxHeights[i]`。  
2. 数组 `heights` 是 **山脉**（mountain），即存在一个峰值索引 `i`，使得  
   - 对所有 `j < i`，`heights[j] <= heights[j+1]`（单调不降）；  
   - 对所有 `j >= i`，`heights[j] >= heights[j+1]`（单调不升）。  

返回美丽配置的 `heights` 和的最大可能值。

---

## 示例

### 示例 1
**输入**: `maxHeights = [5,3,4,1,1]`  
**输出**: `13`  
**解释**:  
一种最大和的美丽配置为 `heights = [5,3,3,1,1]`。该配置满足：  
- `1 <= heights[i] <= maxHeights[i]`  
- `heights` 是峰值索引 `i = 0` 的山脉。  
可以证明不存在和大于 `13` 的美丽配置。

### 示例 2
**输入**: `maxHeights = [6,5,3,9,2,7]`  
**输出**: `22`  
**解释**:  
一种最大和的美丽配置为 `heights = [3,3,3,9,2,2]`。该配置满足：  
- `1 <= heights[i] <= maxHeights[i]`  
- `heights` 是峰值索引 `i = 3` 的山脉。  
可以证明不存在和大于 `22` 的美丽配置。

### 示例 3
**输入**: `maxHeights = [3,2,5,5,2,3]`  
**输出**: `18`  
**解释**:  
一种最大和的美丽配置为 `heights = [2,2,5,5,2,2]`。该配置满足：  
- `1 <= heights[i] <= maxHeights[i]`  
- `heights` 是峰值索引 `i = 2` 的山脉。  
注意，对于该配置，`i = 3` 也可以视为峰值。  
可以证明不存在和大于 `18` 的美丽配置。

---

## 约束

- `1 <= n == maxHeights.length <= 10^5`  
- `1 <= maxHeights[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求我们在每个坐标 `i` 处建一座高度不超过 `maxHeights[i]` 的塔，所有塔的高度构成 **山形**（mountain）：

* 存在一个峰值下标 `p`，  
  * `heights[0] ≤ heights[1] ≤ … ≤ heights[p]`（左侧单调不降）  
  * `heights[p] ≥ heights[p+1] ≥ … ≥ heights[n‑1]`（右侧单调不升）

在满足上述两个条件的前提下，让所有塔的高度之和尽可能大。

最直接的想法是**枚举峰值 `p`**，然后分别向左、向右“填”高度：

* 峰值处我们可以直接取最高 `maxHeights[p]`（再高也不违背限制）。
* 向左走时，第 `i`（`i < p`）的塔高度不能超过右边已经确定的高度 `heights[i+1]`，否则左侧就会出现下降。于是
  ```
  heights[i] = min( maxHeights[i] , heights[i+1] )
  ```
* 向右走时，同理
  ```
  heights[i] = min( maxHeights[i] , heights[i-1] )
  ```

把左、右两段得到的高度相加，就是以 `p` 为峰的山形的最大总和。遍历所有 `p`，取最大的那个即可。

> **类比**：把 `maxHeights` 想成一条山脉的“最高限制”。我们从峰往两边“削坡”，每一步只能把高度削到不高于左（右）边已经确定的那段坡度，类似把一根木棍压在一条不平的路面上，让木棍始终贴在路面上且不向上跳。

这种做法虽然能得到正确答案，但**时间复杂度是 O(n²)**：对每个峰 `p`（`n` 次），我们都要遍历一次全数组来向左、向右填充。

#### 代码（Python）

```python
from typing import List

def max_sum_bruteforce(maxHeights: List[int]) -> int:
    n = len(maxHeights)
    best = 0

    # 枚举每一个可能的峰值下标 p
    for p in range(n):
        heights = [0] * n

        # 峰值尽可能取最高
        heights[p] = maxHeights[p]

        # 向左填：保持 non‑decreasing（从左往右看是递增的）
        for i in range(p - 1, -1, -1):
            # 不能超过右边已经确定的高度，也不能超过自己的上限
            heights[i] = min(maxHeights[i], heights[i + 1])

        # 向右填：保持 non‑increasing（从左往右看是递减的）
        for i in range(p + 1, n):
            heights[i] = min(maxHeights[i], heights[i - 1])

        # 计算当前峰的总和
        cur_sum = sum(heights)
        best = max(best, cur_sum)

    return best
```

#### 复杂度  

* **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 个可能的峰，内层对每个峰都要遍历整个数组（左、右各一次），所以是二次方。  
  - 对于 `n = 10⁵` 的数据，这已经完全不可接受（相当于 10⁵ × 10⁵ ≈ 10¹⁰ 次操作）。

* **空间复杂度**：`O(n)`  
  - 需要一个长度为 `n` 的 `heights` 数组来存每次尝试的结果。  
  - 这在题目限制下是可以接受的，但仍然不是最优的空间使用。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要从头遍历**左、右两段来计算高度。  
其实左侧的填充过程只依赖 **“从右往左的最小值”**，右侧则依赖 **“从左往右的最小值”**。如果我们能在一次遍历中把这些最小值对应的**累计和**算出来，那么每个峰的答案就可以 **O(1)** 直接得到。

下面把这个想法拆成两步：

1. **左侧贡献 `left[i]`**  
   设 `left[i]` 为“当 `i` 为峰时，区间 `[0, i]` 能得到的最大高度和”。  
   观察左侧填充规则：  
   ```
   height[i] = maxHeights[i]                (峰)
   height[i-1] = min(maxHeights[i-1], height[i])
   height[i-2] = min(maxHeights[i-2], height[i-1])
   …
   ```
   换句话说，从右往左我们不断取 **当前元素与右侧已经确定的最小值的较小者**。  
   这正好等价于：对每个位置 `j`，它的最终高度是 **在区间 `[j, i]` 中的最小值**（因为更左的塔不能超过更右的最小上限）。  
   因此 `left[i]` 可以用 **单调递增栈**一次性算出：

   * 栈中保存的是 **严格递增** 的 `maxHeights` 下标。  
   * 当处理位置 `i` 时，弹出所有 `maxHeights[stack[-1]] ≥ maxHeights[i]`（因为 `i` 更小，会限制左侧更远的元素）。  
   * 栈顶留下的下标 `prev` 是离 `i` 最近、且高度 **更小** 的位置。  
   * 区间 `(prev, i]`（长度 `i - prev`）内的所有塔高度都可以取到 `maxHeights[i]`，于是贡献 `maxHeights[i] * (i - prev)`。  
   * 再加上 `prev` 之前已经算好的 `left[prev]`（如果 `prev` 存在），得到 `left[i]`。

   公式化：
   ```
   left[i] = maxHeights[i] * (i - prev) + (left[prev] if prev != -1 else 0)
   ```
   这里 `prev = stack[-1]`（栈为空时设为 `-1`）。

2. **右侧贡献 `right[i]`**  
   同理，从右往左遍历一遍，使用 **单调递增栈**（这次看的是左侧更小的下标），得到 `right[i]`——区间 `[i, n-1]` 的最大和。

3. **合并**  
   对每个可能的峰 `i`，山形的总高度为
   ```
   total[i] = left[i] + right[i] - maxHeights[i]
   ```
   因为峰的高度在 `left[i]` 与 `right[i]` 中都算进来了，需要减掉一次。

4. **答案**  
   取 `max(total[i])` 即为所求。

> **单调栈直观图**（左侧计算示例）  
> ```
> maxHeights : 5 3 4 1 1
>            ^         当前 i = 2 (value=4)
> 栈中保存递增下标 → [1] (value=3)   (因为 5 >= 4 被弹出)
> prev = 1
> 区间 (1,2] 长度 1，全部可以取 4 → 4*1
> left[2] = 4*1 + left[1]
> ```
> 通过一次遍历，所有 `left[i]` 都能算出。

#### 代码（Python）

```python
from typing import List

def max_sum_optimal(maxHeights: List[int]) -> int:
    n = len(maxHeights)

    # ---------- 计算 left ----------
    left = [0] * n          # left[i] = best sum for prefix [0..i] with i as peak
    stack = []              # 单调递增栈，存下标

    for i in range(n):
        # 弹出所有高度 >= 当前高度的下标，因为它们会被 i 限制
        while stack and maxHeights[stack[-1]] >= maxHeights[i]:
            stack.pop()

        # prev 是左边最近且更小的下标，若栈空则视作 -1
        prev = stack[-1] if stack else -1

        # 区间 (prev, i] 长度为 i - prev，全部可以取 maxHeights[i]
        left[i] = maxHeights[i] * (i - prev) + (left[prev] if prev != -1 else 0)

        stack.append(i)     # 把当前下标压入栈，供后面的元素使用

    # ---------- 计算 right ----------
    right = [0] * n
    stack.clear()          # 重新使用同一个栈

    for i in range(n - 1, -1, -1):
        while stack and maxHeights[stack[-1]] >= maxHeights[i]:
            stack.pop()

        # next 是右边最近且更小的下标，若栈空则视作 n
        nxt = stack[-1] if stack else n

        # 区间 [i, nxt) 长度为 nxt - i，全部可以取 maxHeights[i]
        right[i] = maxHeights[i] * (nxt - i) + (right[nxt] if nxt != n else 0)

        stack.append(i)

    # ---------- 合并 ----------
    ans = 0
    for i in range(n):
        total = left[i] + right[i] - maxHeights[i]   # 峰被算了两次，减一次
        ans = max(ans, total)

    return ans
```

#### 复杂度  

* **时间复杂度**：`O(n)`  
  - 两次线性遍历（一次从左到右算 `left`，一次从右到左算 `right`），每个元素最多进出栈一次。  
  - 与 `n` 成正比，能够轻松处理 `10⁵` 规模的数据。  
  - 与暴力解的 `O(n²)` 相比，速度提升了 **近 `n` 倍**（比如 `10⁵` → `10⁵` 次操作）。

* **空间复杂度**：`O(n)`  
  - 需要存 `left`、`right` 两个长度为 `n` 的数组以及一个栈（最坏也只会保存 `n` 个下标）。  
  - 这已经是线性空间的下界，无法再进一步压缩。

---

## 心得

* **核心技巧**：**单调栈** + **前缀/后缀累计**  
  - 单调栈帮助我们在 **一次遍历** 内找出“左边最近更小的元素”或“右边最近更小的元素”。  
  - 结合前缀累计和后缀累计，就能在 `O(1)` 时间内得到以任意位置为峰的最大山形和。

* **适用的题型**  
  1. **最大山形/凹形**（如本题）  
  2. **每个元素作为最小值的子数组和**（LeetCode 907 – Sum of Subarray Minimums）  
  3. **柱状图中最大的矩形面积**（LeetCode 84 – Largest Rectangle in Histogram）

* **一句话总结解题钥匙**  
  > “把每个位置看成‘最小高度的屏障’，用单调栈一次性把它左右能支配的区间算出来，再累计得到整体最优。”

---

## 反思

* **第一反应**：看到“山形”“峰值”就想到“枚举峰、左右扩展”，于是写出了暴力方案。  
* **最容易踩的坑**  
  - **边界处理**：栈为空时要把左边视作 `-1`（或右边视作 `n`），否则会出现索引错误。  
  - **峰的重复计数**：`left[i]` 与 `right[i]` 都把 `maxHeights[i]` 加进来了，需要在合并时减一次。  
  - **大数溢出**：在 Python 不会溢出，但在某些语言要用 `long long`。  

* **下次遇到类似题**，第一步应该：  
  - **确认单调约束**（递增/递减），  
  - **思考“最近更小/更大”** 能否用单调栈一次性求出，  
  - 再把局部贡献累加得到全局答案。