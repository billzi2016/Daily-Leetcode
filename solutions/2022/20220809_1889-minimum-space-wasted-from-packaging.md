# #1889. 最小包装空间浪费 / Minimum Space Wasted From Packaging

> 难度：困难 · 标签：Array、Binary Search、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-space-wasted-from-packaging/)

---

## 题目（英文原版）

**Description**

You have n packages that you are trying to place in boxes, one package in each box. There are m suppliers that each produce boxes of different sizes (with infinite supply). A package can be placed in a box if the size of the package is less than or equal to the size of the box.
The package sizes are given as an integer array packages, where packages[i] is the size of the ith package. The suppliers are given as a 2D integer array boxes, where boxes[j] is an array of box sizes that the jth supplier produces.
You want to choose a single supplier and use boxes from them such that the total wasted space is minimized. For each package in a box, we define the space wasted to be size of the box - size of the package. The total wasted space is the sum of the space wasted in all the boxes.
Return the minimum total wasted space by choosing the box supplier optimally, or -1 if it is impossible to fit all the packages inside boxes. Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: packages = [2,3,5], boxes = [[4,8],[2,8]]
Output: 6
Explanation: It is optimal to choose the first supplier, using two size-4 boxes and one size-8 box.
The total waste is (4-2) + (4-3) + (8-5) = 6.
```

**Example 2:**

```
Input: packages = [2,3,5], boxes = [[1,4],[2,3],[3,4]]
Output: -1
Explanation: There is no box that the package of size 5 can fit in.
```

**Example 3:**

```
Input: packages = [3,5,8,10,11,12], boxes = [[12],[11,9],[10,5,14]]
Output: 9
Explanation: It is optimal to choose the third supplier, using two size-5 boxes, two size-10 boxes, and two size-14 boxes.
The total waste is (5-3) + (5-5) + (10-8) + (10-10) + (14-11) + (14-12) = 9.
```

**Constraints**

- n == packages.length
- m == boxes.length
- 1 <= n <= 105
- 1 <= m <= 105
- 1 <= packages[i] <= 105
- 1 <= boxes[j].length <= 105
- 1 <= boxes[j][k] <= 105
- sum(boxes[j].length) <= 105
- The elements in boxes[j] are distinct.

---

## 题目（中文翻译）

你有 **n** 个包裹需要放入盒子中，每个盒子只能放一个包裹。共有 **m** 家供应商，每家供应商提供若干种不同尺寸的盒子（供应量无限）。如果包裹的尺寸小于等于盒子的尺寸，则该包裹可以放入该盒子。

- 包裹的尺寸由整数数组 `packages` 给出，`packages[i]` 表示第 *i* 个包裹的尺寸。  
- 供应商的信息由二维整数数组 `boxes` 给出，`boxes[j]` 是第 *j* 家供应商生产的所有盒子尺寸的数组。

你需要选择 **唯一** 的一家供应商，并只使用该供应商提供的盒子，使得 **总浪费空间** 最小。对于放入盒子中的每个包裹，浪费空间定义为 **盒子尺寸 - 包裹尺寸**。总浪费空间是所有盒子中浪费空间的和。

返回在最优选择供应商的情况下的最小总浪费空间；如果无法将所有包裹都装入盒子，返回 **-1**。由于答案可能很大，返回结果需取模 **10⁹ + 7**。

---

### 示例

**示例 1**

```text
Input: packages = [2,3,5], boxes = [[4,8],[2,8]]
Output: 6
Explanation: 选择第一家供应商，使用两个尺寸为 4 的盒子和一个尺寸为 8 的盒子。
总浪费空间为 (4-2) + (4-3) + (8-5) = 6。
```

**示例 2**

```text
Input: packages = [2,3,5], boxes = [[1,4],[2,3],[3,4]]
Output: -1
Explanation: 没有任何盒子能够容纳尺寸为 5 的包裹。
```

**示例 3**

```text
Input: packages = [3,5,8,10,11,12], boxes = [[12],[11,9],[10,5,14]]
Output: 9
Explanation: 选择第三家供应商，使用两个尺寸为 5 的盒子、两个尺寸为 10 的盒子和两个尺寸为 14 的盒子。
总浪费空间为 (5-3) + (5-5) + (10-8) + (10-10) + (14-11) + (14-12) = 9。
```

---

### 约束条件

- `n == packages.length`
- `m == boxes.length`
- `1 <= n <= 10⁵`
- `1 <= m <= 10⁵`
- `1 <= packages[i] <= 10⁵`
- `1 <= boxes[j].length <= 10⁵`
- `1 <= boxes[j][k] <= 10⁵`
- `sum(boxes[j].length) <= 10⁵`
- `boxes[j]` 中的元素互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**每一个供应商，然后**逐个包裹**每个包裹：

1. 对于当前供应商 `j`，取出它生产的所有箱子尺寸 `boxes[j]`。  
2. 对每一个包裹 `p`，在 `boxes[j]` 中找一个**最小的且不小于 `p`**的箱子（如果有多个同样大小的箱子，任选其一），把 `p` 放进去，浪费的空间就是 `箱子尺寸 - p`。  
3. 把所有包裹的浪费相加，得到该供应商的总浪费。  
4. 把所有供应商的结果取最小值，即为答案。

**使用的数据结构**  
- `list`（普通的 Python 列表）保存箱子尺寸。可以把它想象成**一本未排好序的词典**，我们要在里面逐个查找合适的“词条”。  
- `for` 循环遍历所有包裹和箱子。

**为什么正确**  
因为我们把每个包裹都放进了**满足条件的最小箱子**，这一步已经是对该供应商的**最优**分配（如果我们用了更大的箱子，浪费只会更大）。只要遍历完所有供应商，取最小值，就能得到全局最优。

**复杂度分析（大白话）**  
- 对每个供应商，我们要把 **所有** 包裹都遍历一次；每遍历一次，还要在该供应商的箱子列表里 **线性查找** 合适的箱子。  
- 假设有 `n` 个包裹，`m` 个供应商，平均每个供应商有 `k` 种箱子（`k` 可能和 `n` 差不多大），那么时间复杂度大约是 `O(m * n * k)`，最坏情况下会是 `O(10^5 * 10^5 * 10^5)`，根本不可接受。  
- 空间上我们只保存原始输入，额外的空间是 `O(1)`。

#### 代码（Python）

```python
def minWastedSpace_bruteforce(packages, boxes):
    MOD = 10**9 + 7
    n = len(packages)
    ans = float('inf')

    for supplier in boxes:                     # 遍历每个供应商
        # 为了能快速判断是否能装下所有包裹，先找出最大的箱子尺寸
        if max(supplier) < max(packages):      # 这个供应商根本装不下最大的包裹
            continue

        waste = 0
        for p in packages:                     # 对每个包裹
            # 在该供应商的箱子里线性寻找最小的、且 >= p 的箱子
            best = None
            for b in supplier:
                if b >= p:
                    if best is None or b < best:
                        best = b
            if best is None:                    # 没找到合适的箱子，说明此供应商不可行
                waste = float('inf')
                break
            waste += best - p                    # 累加浪费空间
        ans = min(ans, waste)

    return -1 if ans == float('inf') else ans % MOD
```

> 代码里每一行都写了中文注释，帮助你一步步跟上思路。

#### 复杂度

- **时间复杂度**：`O(m * n * k)`（极其低效），其中  
  - `m` 为供应商数量，  
  - `n` 为包裹数量，  
  - `k` 为单个供应商的箱子种类数。  
  用大白话说，就是“每找一次箱子都要翻遍一次所有箱子”，所以会很慢。  
- **空间复杂度**：`O(1)`（不额外使用额外的数据结构，只用了常数级的变量）。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次找箱子都要线性扫描。我们可以通过**排序 + 前缀和 + 二分查找**把这个过程降到 `O(log k)`，从而把整体复杂度降到 `O((n + total_boxes) log total_boxes)`。

核心步骤如下：

1. **对包裹排序**  
   把 `packages` 按从小到大排序。这样在后面处理箱子时，只需要一次遍历就能知道哪些包裹会被放进当前箱子。

2. **预处理包裹的前缀和**  
   设 `pre[i]` 为前 `i` 个（已排序）包裹尺寸之和，`pre[0] = 0`。  
   前缀和相当于**累计总和的记事本**，帮助我们在 O(1) 时间内算出任意区间的尺寸总和。

3. **遍历每个供应商**  
   - 先把该供应商的箱子尺寸 **去重并排序**（题目已经保证去重，这里只需要排序）。  
   - 如果该供应商最大的箱子尺寸 < 最大的包裹尺寸，直接跳过（装不下）。

4. **使用双指针 + 二分**  
   - 设 `i` 为已经处理好的包裹的下标（从 0 开始）。  
   - 对于当前箱子尺寸 `size`，我们需要把 **所有** 包裹 `packages[i … j-1]`（其中 `packages[j-1] ≤ size`）装进这种箱子。  
   - 用 `bisect_right(packages, size)` 找到第一个 **大于** `size` 的位置 `j`，即 `[i, j)` 区间的包裹可以放进此箱子。  
   - 这 `cnt = j - i` 个包裹如果使用 **size** 号箱子，浪费空间 = `cnt * size - (pre[j] - pre[i])`。  
   - 把这部分浪费累加到当前供应商的总浪费 `cur` 中，然后把指针 `i = j`，继续处理下一个更大的箱子。  
   - 当 `i` 已经等于 `n`（所有包裹都已分配）时，停止循环。

5. **取所有供应商中最小的 `cur`**，记为答案。若所有供应商均不可行，返回 `-1`。

**为什么这样是最优的**  
- 对每个箱子我们总是把**能够装进的最小包裹**（因为包裹已经排好序）放进去，这等价于把每个包裹分配给**满足条件的最小箱子**，浪费最小。  
- 使用二分查找把“找出可以放进当前箱子的最后一个包裹”从线性降到对数，整体遍历每个箱子只做一次 **指针移动**，所以时间非常快。

**关键算法/数据结构解释**  

- **排序**：把乱序的东西排成有序的队列，后面查找就能用二分。想象把散落的玩具按大小排成一排，找最合适的盒子时只需要从左到右顺序检查。  
- **前缀和**：把“前面所有玩具的总重量”记录下来，之后想要知道任意区间的总重量，只需要两次减法。  
- **二分查找 (`bisect_right`)**：在有序列表里找**第一个大于目标**的位置，时间是 `log` 级别。就像在一本排好序的字典里找词，翻页比逐行查找快很多。  
- **双指针**：`i` 指向当前未分配的包裹，`j` 是本次箱子可以容纳的最右边界，两者一起向右移动，保证每个包裹只被处理一次。

#### 代码（Python）

```python
from bisect import bisect_right

def minWastedSpace(packages, boxes):
    MOD = 10**9 + 7
    packages.sort()                     # 1. 包裹升序
    n = len(packages)

    # 2. 前缀和，pre[i] = 前 i 个包裹尺寸之和（0 <= i <= n）
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + packages[i]

    ans = float('inf')                  # 记录全局最小浪费

    for supplier in boxes:              # 逐个供应商
        supplier.sort()                 # 盒子尺寸升序
        if supplier[-1] < packages[-1]: # 最大盒子仍然装不下最大包裹 → 不可能
            continue

        cur = 0          # 当前供应商的总浪费
        i = 0            # 已经分配好的包裹下标（从 0 开始）

        for size in supplier:            # 按尺寸从小到大遍历盒子
            # 3. 用二分找出第一个 > size 的包裹位置 j
            j = bisect_right(packages, size, lo=i)   # 只在未处理的区间里查
            if j == i:                 # 没有任何包裹能放进这个盒子
                continue
            cnt = j - i                # 这次可以装进的包裹数量
            # 4. 计算浪费：cnt * size - (pre[j] - pre[i])
            waste = cnt * size - (pre[j] - pre[i])
            cur += waste
            i = j                      # 指针前移，已处理的包裹不再考虑

            if i == n:                 # 所有包裹都已分配完
                break

        # 若 i 已经走到 n，说明此供应商可行，更新答案
        if i == n:
            ans = min(ans, cur)

    return -1 if ans == float('inf') else ans % MOD
```

> 代码中每一步都配有中文注释，帮助你对应思路的每个关键点。

#### 复杂度

- **时间复杂度**：  
  - 包裹排序 `O(n log n)`。  
  - 前缀和 `O(n)`。  
  - 对每个供应商：盒子排序 `O(k log k)`（`k` 为该供应商的盒子数量），遍历盒子时每个盒子只做一次二分查找 `O(log n)`，但所有盒子合起来的二分查找次数不超过 `n`（因为指针 `i` 只前进），所以整体是 `O(k log k + n)`。  
  - 所有供应商的盒子总数 ≤ `10^5`（题目限制），记为 `B`，则总时间为 `O(n log n + B log B + n·m?)` 实际上是 `O((n + B) log (n + B))`，在 10⁵ 规模下完全可以跑完。  
  - 用大白话说：**先把东西排好序，然后每次只看一次，查找用二分，整个过程只需要几次“翻页”。**

- **空间复杂度**：  
  - 额外使用的前缀和数组 `pre` 大小 `O(n)`。  
  - 其余只是少量变量，故总体 `O(n)`。  
  - 这比暴力解多用了一个同等规模的数组，但仍然是线性空间，完全可以接受。

---

## 心得

- **核心技巧**：**排序 + 前缀和 + 二分查找**（或说“离线+区间求和”），把原本的“每个箱子都遍历所有包裹”转化为“每个包裹只被处理一次”。  
- **适用的题型**（类似思路）  
  1. “最小代价分配”类：如 LeetCode 1354 `Construct Target Array With Multiple Sums`（需要前缀和快速求区间和）。  
  2. “区间覆盖最小费用”类：如 LeetCode 1627 `Graph Connectivity With Threshold`（需要排序+二分）。  
  3. “装箱/分配”类：如 LeetCode 1011 `Capacity To Ship Packages Within D Days`（同样利用排序和前缀和做二分判定）。  
- **一句话总结解题钥匙**：  
  > “先把包裹排好序，用前缀和记住累计大小，随后对每个供应商的箱子用二分快速定位可装的包裹区间，累加浪费即可。”

---

## 反思

- **第一反应**：看到“每个包裹对应一个箱子”，本能想到**枚举**所有可能的配对，直接实现最朴素的暴力解。  
- **最容易踩的坑**  
  1. **边界条件**：如果某个供应商的最大箱子仍然小于最大的包裹，需要提前剪枝，否则会在循环里一直找不到合适箱子导致错误。  
  2. **前缀和溢出**：包裹尺寸和箱子尺寸均可能达到 `10^5`，累计和会超过 `int` 范围（在 Python 中不怕），但在取模前要注意使用 `% MOD` 防止超大数影响性能。  
  3. **二分搜索的起始位置**：必须在未处理的区间 `[i, n)` 里搜索，否则会重复计数已经分配好的包裹。`bisect_right(packages, size, lo=i)` 正是为此设计。  
- **下次遇到同类题**，第一步应该想到：  
  > “能否把原始数据排序后，用前缀和/二分把区间查询变成 O(1) / O(log)？”  
  这一步往往能把指数级的暴力转化为线性或对数级的高效解。