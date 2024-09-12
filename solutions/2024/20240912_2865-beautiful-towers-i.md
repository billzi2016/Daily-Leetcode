# #2865. **美丽塔 I** / Beautiful Towers I

> 难度：中等 · 标签：Array、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/beautiful-towers-i/)

---

## 题目（英文原版）

**Description**

You are given an array heights of n integers representing the number of bricks in n consecutive towers. Your task is to remove some bricks to form a mountain-shaped tower arrangement. In this arrangement, the tower heights are non-decreasing, reaching a maximum peak value with one or multiple consecutive towers and then non-increasing.
Return the maximum possible sum of heights of a mountain-shaped tower arrangement.

**Examples**

**Example 1:**

```
Input: heights = [5,3,4,1,1]
Output: 13
Explanation:
We remove some bricks to make heights = [5,3,3,1,1] , the peak is at index 0.
```

**Example 2:**

```
Input: heights = [6,5,3,9,2,7]
Output: 22
Explanation:
We remove some bricks to make heights = [3,3,3,9,2,2] , the peak is at index 3.
```

**Example 3:**

```
Input: heights = [3,2,5,5,2,3]
Output: 18
Explanation:
We remove some bricks to make heights = [2,2,5,5,2,2] , the peak is at index 2 or 3.
```

**Constraints**

- 1 <= n == heights.length <= 103
- 1 <= heights[i] <= 109

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `heights`，其中 `heights[i]` 表示第 `i` 座连续塔的砖块数量。你可以移除若干砖块，使塔的高度形成山形（mountain-shaped）排列：塔的高度先**非递减**（non-decreasing），达到一个或多个相邻塔的最高峰后，再**非递增**（non-increasing）。

返回能够形成山形排列的塔高度之和的最大可能值。

---

#### 示例

**示例 1**

```
Input: heights = [5,3,4,1,1]
Output: 13
Explanation:
我们移除一些砖块，使 heights 变为 [5,3,3,1,1]，峰位于下标 0。
```

**示例 2**

```
Input: heights = [6,5,3,9,2,7]
Output: 22
Explanation:
我们移除一些砖块，使 heights 变为 [3,3,3,9,2,2]，峰位于下标 3。
```

**示例 3**

```
Input: heights = [3,2,5,5,2,3]
Output: 18
Explanation:
我们移除一些砖块，使 heights 变为 [2,2,5,5,2,2]，峰位于下标 2 或 3。
```

---

#### 约束条件

- `1 <= n == heights.length <= 10^3`
- `1 <= heights[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求把每座塔的砖块 **只能削减**（即只能把高度变小），使得整体形成 “山形”：  
- 从左到峰 **不下降**（即每个位置的高度 ≤ 右边相邻位置的高度）  
- 从峰到右 **不上升**（即每个位置的高度 ≥ 右边相邻位置的高度）  

最直接的想法是：**把每一个下标 `i` 当成峰**，分别算出以 `i` 为峰时左侧和右侧需要削减多少砖，最后取最大和。

- **左侧**：从 `i‑1` 往左遍历，当前塔的高度只能 **不大于** 右边已经确定的高度。于是可以用  
  `left[j] = min(heights[j], left[j+1])`（从右往左递推）。  
- **右侧**：从 `i+1` 往右遍历，当前塔的高度只能 **不小于** 左边已经确定的高度。于是可以用  
  `right[j] = min(heights[j], right[j‑1])`（从左往右递推）。

把左侧、右侧以及峰本身的高度加起来，就是以 `i` 为峰的山形塔总高度。遍历所有 `i`，取最大值即为答案。

> **生活化类比**：  
> 把 `heights` 想象成一排装满水的瓶子，只能往下倒水，不能往上倒。要让水面先升后降（山形），我们从峰往两边“倒”，保证左边的水面不超过右边，右边的水面不低于左边。

#### 代码（Python）

```python
def max_sum_mountain_bruteforce(heights):
    n = len(heights)
    best = 0

    for peak in range(n):                     # 每个位置都尝试当峰
        # ---------- 处理左侧 ----------
        left = heights[:]                     # 复制一份，后面会在这里削减
        for j in range(peak - 1, -1, -1):     # 从峰左边往左走
            left[j] = min(left[j], left[j + 1])   # 只能让它不高于右边

        # ---------- 处理右侧 ----------
        right = heights[:]                    # 复制一份，后面会在这里削减
        for j in range(peak + 1, n):          # 从峰右边往右走
            right[j] = min(right[j], right[j - 1])  # 只能让它不低于左边

        # ---------- 计算总和 ----------
        total = sum(left[:peak + 1]) + sum(right[peak + 1:])
        best = max(best, total)

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：我们遍历 `n` 个可能的峰，每一次都要对左侧和右侧各走一遍最多 `n` 步，所以最坏情况是 `n × n`，也就是“平方级”。如果 `n = 1000`，大约会进行 1,000,000 次基本操作，算得过去但不够优雅。

- **空间复杂度**：`O(n)`  
  解释：每次循环里我们额外拷贝了两个长度为 `n` 的数组 `left`、`right`，因此需要 `n` 的额外空间。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都重新遍历左、右两侧**。事实上，左侧的“只能递增”过程只和**当前位置左边所有元素的最小值**有关，右侧同理。我们可以**一次遍历就把所有位置的左侧贡献算好**，再一次逆向遍历算右侧贡献，最后合并。

关键在于**单调栈（Monotonic Stack）**的使用。单调栈是一种“保持栈中元素单调递增（或递减）”的数据结构，常用于：

- 计算每个位置左侧最近的小于/大于元素  
- 统计区间长度时，能够把相同高度的连续块合并起来

这里我们需要的功能是：

> 对于每个下标 `i`，求 **从左边开始到 `i` 为止**，如果只能把高度向右“压低”使序列非递减，最终得到的 **总高度**（即左侧贡献）。

实现方式（从左到右遍历）：

1. 栈中存 `(height, cnt)`，`cnt` 表示该高度在栈里连续出现的长度（因为相同高度可以合并，省掉重复计算）。栈始终保持 **高度递增**（从栈底到栈顶）。
2. 处理新来的 `h = heights[i]` 时：  
   - 如果栈顶的高度 **大于** `h`，说明它们必须被压到 `h`，于是把栈顶弹出，并把对应的贡献 `height * cnt` 从当前累计和 `cur_sum` 中减掉，同时把 `cnt` 加到当前元素的计数里（因为这些被压低的块现在归属于 `h`）。
   - 重复弹出，直到栈顶高度 ≤ `h`。
3. 把 `(h, cnt)` 压入栈，`cur_sum += h * cnt`。此时 `cur_sum` 正好是 **左侧贡献** `left[i]`。
4. 把 `left[i] = cur_sum` 记录下来。

右侧贡献同理，只是从右往左遍历，得到数组 `right[i]`（表示从 `i` 到最右端的山形贡献）。

最后答案是：

```
ans = max( left[i] + right[i] - heights[i] )   # 峰的高度被左、右都算了一遍，减掉一次
```

> **类比**：想象你在排队买票，队伍里每个人只能比前面的人 **不低**（左侧）或 **不高**（右侧）。单调栈就像一个“裁判”，一旦发现后面的人比前面高（或低），就把前面的人“降级”到后面人的水平，保证整个队伍符合规则。统计时，只要把每个“裁判”处理过的总票数累加，就得到了左侧或右侧的最大可能总票数。

#### 代码（Python）

```python
def max_sum_mountain(heights):
    n = len(heights)
    # ---------- 左侧贡献 ----------
    left = [0] * n               # left[i] = 以 i 为右端点的非递减序列的最大总和
    stack = []                   # 栈中元素为 (height, count)
    cur_sum = 0                  # 当前栈对应的总和

    for i, h in enumerate(heights):
        cnt = 1                  # 当前高度在栈中出现的次数（初始为 1）

        # 如果栈顶高度比当前高度大，需要把栈顶“压低”
        while stack and stack[-1][0] > h:
            top_h, top_cnt = stack.pop()
            cur_sum -= top_h * top_cnt   # 把被弹出的高度贡献移除
            cnt += top_cnt               # 这些块现在合并到当前高度上

        stack.append((h, cnt))          # 把当前 (height, cnt) 放进栈
        cur_sum += h * cnt               # 加上新的贡献
        left[i] = cur_sum                # 记录以 i 为右端的最大和

    # ---------- 右侧贡献 ----------
    right = [0] * n
    stack.clear()
    cur_sum = 0

    for i in range(n - 1, -1, -1):
        h = heights[i]
        cnt = 1

        while stack and stack[-1][0] > h:
            top_h, top_cnt = stack.pop()
            cur_sum -= top_h * top_cnt
            cnt += top_cnt

        stack.append((h, cnt))
        cur_sum += h * cnt
        right[i] = cur_sum

    # ---------- 合并左、右，得到答案 ----------
    ans = 0
    for i in range(n):
        total = left[i] + right[i] - heights[i]   # 峰的高度重复计入一次，需要减掉
        ans = max(ans, total)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：每个元素最多被压入栈一次、弹出一次，整个过程线性扫描两遍（左→右、右→左），所以时间随 `n` 成正比。相较于 `O(n²)` 的暴力解，“一次遍历就搞定”——在实际运行中即使 `n=10⁵` 也毫无压力。

- **空间复杂度**：`O(n)`  
  解释：我们额外保存两个长度为 `n` 的数组 `left`、`right`，以及最多 `n` 大小的栈。整体仍是线性额外空间。

---

## 心得

- **核心技巧**：单调栈 + 前缀（后缀）累计求和，用一次遍历算出每个位置左侧/右侧的最大可能总和。  
- **适用的题型**  
  1. “把数组压低/抬高，使其满足单调约束，求最大/最小总和”——如 *Maximum Sum of Min-Heap after Decreasing Elements*。  
  2. “求每个位置左（右）侧最近的更小/更大元素并统计区间贡献”——如 *Largest Rectangle in Histogram*、*Sum of Subarray Minimums*。  
- **一句话总结**：**把“只能削减”转化为“把高的压到低的”，用单调栈一次遍历把所有压低的费用累计起来**。

---

## 反思

- **第一反应**：先枚举峰，然后分别向左、向右遍历压低高度，写出暴力实现。  
- **最容易踩的坑**  
  - **峰的高度算重了**：左侧 `left[i]` 已经包含了 `heights[i]`，右侧 `right[i]` 也包含了同一个峰，需要在合并时减去一次。  
  - **相同高度的合并**：如果不把相同高度的连续块合并，栈里会出现大量重复元素，导致时间仍是 `O(n²)`（每次弹出只处理一个元素）。  
  - **整数溢出**：虽然 Python 整数不溢出，但在其他语言（如 C++）要使用 `long long`。  
- **下次遇到同类题**：第一步先**思考“单调约束”能否用单调栈把“压低/抬高”过程一次性累计**，再决定是暴力枚举还是利用栈做线性优化。