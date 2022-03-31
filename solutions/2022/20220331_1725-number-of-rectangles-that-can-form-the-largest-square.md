# #1725. 能够构成最大正方形的矩形数量 / Number Of Rectangles That Can Form The Largest Square

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/number-of-rectangles-that-can-form-the-largest-square/)

---

## 题目（英文原版）

**Description**

You are given an array rectangles where rectangles[i] = [li, wi] represents the ith rectangle of length li and width wi.
You can cut the ith rectangle to form a square with a side length of k if both k <= li and k <= wi. For example, if you have a rectangle [4,6], you can cut it to get a square with a side length of at most 4.
Let maxLen be the side length of the largest square you can obtain from any of the given rectangles.
Return the number of rectangles that can make a square with a side length of maxLen.

**Examples**

**Example 1:**

```
Input: rectangles = [[5,8],[3,9],[5,12],[16,5]]
Output: 3
Explanation: The largest squares you can get from each rectangle are of lengths [5,3,5,5].
The largest possible square is of length 5, and you can get it out of 3 rectangles.
```

**Example 2:**

```
Input: rectangles = [[2,3],[3,7],[4,3],[3,7]]
Output: 3
```

**Constraints**

- 1 <= rectangles.length <= 1000
- rectangles[i].length == 2
- 1 <= li, wi <= 109
- li != wi

---

## 题目（中文翻译）

给定一个数组 `rectangles`，其中 `rectangles[i] = [li, wi]` 表示第 *i* 个矩形（rectangle）的长度 `li` 和宽度 `wi`。  
如果同时满足 `k <= li` 且 `k <= wi`，则可以将第 *i* 个矩形裁剪成边长为 `k` 的正方形（square）。例如，矩形 `[4,6]` 可以裁剪得到最大边长为 `4` 的正方形。  

设 `maxLen` 为你可以从任意给定矩形中得到的最大正方形的边长。返回能够裁剪出边长为 `maxLen` 的正方形的矩形数量。

**示例 1**  
Input: `rectangles = [[5,8],[3,9],[5,12],[16,5]]`  
Output: `3`  
Explanation: 每个矩形能够得到的最大正方形的边长分别为 `[5,3,5,5]`。最大的可能正方形的边长为 `5`，你可以从 `3` 个矩形中得到它。

**示例 2**  
Input: `rectangles = [[2,3],[3,7],[4,3],[3,7]]`  
Output: `3`

**约束条件**  
- `1 <= rectangles.length <= 1000`  
- `rectangles[i].length == 2`  
- `1 <= li, wi <= 10^9`  
- `li != wi`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**先把每个矩形能切出的最大正方形的边长算出来**，再找出这些边长中的最大值 `maxLen`，最后统计有多少个矩形的边长恰好等于 `maxLen`。

- **把矩形变成正方形的边长**  
  对于矩形 `[l, w]`，只能在它的短边以内切出正方形，所以能得到的最大正方形边长就是 `min(l, w)`。这一步可以想象成“把每个矩形压平”，只留下最短的那根棍子长度。

- **为什么这样就对了**  
  `min(l, w)` 正好是该矩形能够提供的最大正方形边长，所有矩形的候选值都已经算出来了，最大值 `maxLen` 必然在这些候选值里。随后统计等于 `maxLen` 的矩形数量即可得到答案。

- **时间/空间复杂度**  
  - 第一次遍历求每个矩形的 `min(l,w)` 并记录最大值 → O(n)  
  - 第二次遍历统计等于最大值的矩形数量 → O(n)  
  总共是两次线性扫描，时间复杂度是 **O(n)**（n 为矩形个数）。  
  空间上只用了常数几个变量，**O(1)**。

#### 代码（Python）

```python
from typing import List

def countGoodRectangles(rectangles: List[List[int]]) -> int:
    # 第一步：求每个矩形能切出的最大正方形边长，并找出最大的那个
    max_len = 0                     # 当前看到的最大正方形边长
    mins = []                       # 保存每个矩形对应的 min(l, w)
    for l, w in rectangles:
        side = min(l, w)             # 只能切到短边这么长
        mins.append(side)           # 记录下来，后面要统计
        if side > max_len:          # 更新最大值
            max_len = side

    # 第二步：统计有多少矩形的 min(l, w) 正好等于 max_len
    cnt = 0
    for side in mins:
        if side == max_len:
            cnt += 1
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n)` — 代码里遍历了两遍矩形列表，n 是矩形的数量。可以把 O(n) 想成“和矩形个数成正比”，如果有 1000 个矩形，就要跑大约 1000 次循环。
- **空间复杂度**：`O(n)` – 这里用了一个 `mins` 列表保存每个矩形的 `min(l,w)`，长度正好是 n。如果不想额外的列表，后面可以进一步优化。

---

### 2. 最优解

#### 思路  
在上面的直觉解里，我们用了两次遍历：第一次找最大值，第二次计数。**瓶颈**就在于第二次遍历其实可以省掉，只要在第一次遍历时同步维护「当前最大值」和「出现次数」就行。

**一步步的优化**：

1. **保持两个变量**  
   - `max_len`：当前看到的最大正方形边长  
   - `cnt`：`max_len` 出现的次数  

2. **遍历每个矩形**  
   - 计算 `side = min(l, w)`。  
   - 如果 `side > max_len`，说明出现了更大的正方形，更新 `max_len = side` 并把计数重置为 1（因为这是第一次出现这个更大的值）。  
   - 如果 `side == max_len`，说明又找到一个可以切出同样最大正方形的矩形，计数 `cnt += 1`。  
   - 其他情况（`side < max_len`）直接忽略。

这样一次遍历就同时完成了「求最大」和「计数」两件事，时间从两遍降到一遍，空间只用了常数。

**核心技巧**：**在一次遍历中同步维护最大值及其出现次数**。这在很多 “找最大/最小并计数” 的题目里都非常常见。

#### 代码（Python）

```python
from typing import List

def countGoodRectangles(rectangles: List[List[int]]) -> int:
    max_len = 0   # 当前最大的正方形边长
    cnt = 0       # 该边长出现的矩形个数

    for l, w in rectangles:
        side = min(l, w)          # 能切出的最大正方形边长

        if side > max_len:        # 发现更大的正方形
            max_len = side        # 更新最大值
            cnt = 1               # 计数重新从 1 开始
        elif side == max_len:     # 又找到一个相同大小的正方形
            cnt += 1              # 计数加一
        # side < max_len 的情况直接跳过

    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次矩形列表，和矩形个数成正比。相较于直觉解的两次遍历，省去了约 1/2 的循环次数，但在大 O 表记上仍是同一级别。
- **空间复杂度**：`O(1)` – 只用了几个整型变量，不随输入规模增长而增长。

---

## 心得

- **核心技巧**：一次遍历同步维护「最大值」和「出现次数」。
- **适用的题型**  
  1. 找数组中最大元素并统计出现次数（如 LeetCode 统计最高分学生）。  
  2. 找最长子序列长度并统计出现次数（如最长递增子序列的个数）。  
  3. 在矩形、线段等几何对象中求最大可容纳的尺寸并计数（本题）。
- **解题钥匙**：**“边走边记”**——遍历时把需要的统计信息即时更新，别等遍历完再回头去算。

---

## 反思

- **第一反应**：先把每个矩形能切出的正方形边长算出来，然后找最大值，再计数。也就是把题目拆成「求 max」+「计数」两个子任务。
- **最容易踩的坑**  
  - **忘记取最短边**：正方形的边长受限于矩形的短边，不能随意取长边。  
  - **计数重置忘写**：当出现更大的正方形时，要把计数重新置为 1，否则会把之前的计数误算进去。  
  - **边界条件**：矩形的长宽可能相等（虽然题目说 `li != wi`，但实际代码最好兼容），此时 `min(l,w)` 仍然有效。
- **下次类似题的第一步**：**先把每个元素映射成一个“候选值”（这里是 `min(l,w)`），再思考如何在一次遍历中同时得到最大值和它的出现次数**。这样可以避免不必要的二次遍历或额外空间。