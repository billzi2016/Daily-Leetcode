# #3030. 求区域平均网格 / Find the Grid of Region Average

> 难度：中等 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-the-grid-of-region-average/)

---

## 题目（英文原版）

**Description**

You are given m x n grid image which represents a grayscale image, where image[i][j] represents a pixel with intensity in the range [0..255]. You are also given a non-negative integer threshold.
Two pixels are adjacent if they share an edge.
A region is a 3 x 3 subgrid where the absolute difference in intensity between any two adjacent pixels is less than or equal to threshold.
All pixels in a region belong to that region, note that a pixel can belong to multiple regions.
You need to calculate a m x n grid result, where result[i][j] is the average intensity of the regions to which image[i][j] belongs, rounded down to the nearest integer. If image[i][j] belongs to multiple regions, result[i][j] is the average of the rounded-down average intensities of these regions, rounded down to the nearest integer. If image[i][j] does not belong to any region, result[i][j] is equal to image[i][j].
Return the grid result.

**Examples**

**Example 1:**

```
Input: image = [[5,6,7,10],[8,9,10,10],[11,12,13,10]], threshold = 3
Output: [[9,9,9,9],[9,9,9,9],[9,9,9,9]]
Explanation:

There are two regions as illustrated above. The average intensity of the first region is 9, while the average intensity of the second region is 9.67 which is rounded down to 9. The average intensity of both of the regions is (9 + 9) / 2 = 9. As all the pixels belong to either region 1, region 2, or both of them, the intensity of every pixel in the result is 9.
Please note that the rounded-down values are used when calculating the average of multiple regions, hence the calculation is done using 9 as the average intensity of region 2, not 9.67.
```

**Example 2:**

```
Input: image = [[10,20,30],[15,25,35],[20,30,40],[25,35,45]], threshold = 12
Output: [[25,25,25],[27,27,27],[27,27,27],[30,30,30]]
Explanation:

There are two regions as illustrated above. The average intensity of the first region is 25, while the average intensity of the second region is 30. The average intensity of both of the regions is (25 + 30) / 2 = 27.5 which is rounded down to 27.
All the pixels in row 0 of the image belong to region 1, hence all the pixels in row 0 in the result are 25. Similarly, all the pixels in row 3 in the result are 30. The pixels in rows 1 and 2 of the image belong to region 1 and region 2, hence their assigned value is 27 in the result.
```

**Example 3:**

```
Input: image = [[5,6,7],[8,9,10],[11,12,13]], threshold = 1
Output: [[5,6,7],[8,9,10],[11,12,13]]
Explanation:
There is only one 3 x 3 subgrid, while it does not have the condition on difference of adjacent pixels, for example, the difference between image[0][0] and image[1][0] is |5 - 8| = 3 > threshold = 1 . None of them belong to any valid regions, so the result should be the same as image .
```

**Constraints**

- 3 <= n, m <= 500
- 0 <= image[i][j] <= 255
- 0 <= threshold <= 255

---

## 题目（中文翻译）

你得到一个 `m x n` 的二维网格 `image`，它表示一幅灰度图像，其中 `image[i][j]` 表示强度在 `[0..255]` 之间的像素。另给定一个非负整数 `threshold`。  

- 两个像素如果共享一条边，则称它们是 **相邻（adjacent）** 的。  
- **区域（region）** 是一个 `3 x 3` 的子网格（subgrid），并且该子网格内任意两个相邻像素的强度绝对差 `|image[a][b] - image[c][d]|` 必须 **小于等于** `threshold`。  
- 子网格中的所有像素都属于该区域。注意，同一个像素可以属于多个区域。  

现在需要计算一个 `m x n` 的结果网格 `result`，其中 `result[i][j]` 为像素 `image[i][j]` 所属所有区域的 **平均强度（average intensity）**，先对每个区域的平均强度向下取整，再对这些整数求平均，最后再向下取整得到 `result[i][j]`。  

- 如果 `image[i][j]` 属于多个区域，则 `result[i][j]` 为这些 **已向下取整的平均强度** 的平均值，再向下取整。  
- 如果 `image[i][j]` 不属于任何区域，则 `result[i][j] = image[i][j]`。  

返回结果网格 `result`。

### 示例

#### 示例 1
```text
Input: image = [[5,6,7,10],[8,9,10,10],[11,12,13,10]], threshold = 3
Output: [[9,9,9,9],[9,9,9,9],[9,9,9,9]]
Explanation:
如图所示存在两个区域。第一个区域的平均强度为 9，第二个区域的平均强度为 9.67，向下取整后为 9。两个区域的平均强度为 (9 + 9) / 2 = 9，向下取整后仍为 9。所有像素都属于其中一个或两个区域，最终结果全部为 9。
```

#### 示例 2
```text
Input: image = [[10,20,30],[15,25,35],[20,30,40],[25,35,45]], threshold = 12
Output: [[25,25,25],[27,27,27],[27,27,27],[30,30,30]]
Explanation:
如图所示存在两个区域。第一个区域的平均强度为 25，第二个区域的平均强度为 30。两个区域的平均强度为 (25 + 30) / 2 = 27.5，向下取整后为 27。不同像素属于的区域数量不同，最终得到的结果如上所示。
```

#### 示例 3
```text
Input: image = [[5,6,7],[8,9,10],[11,12,13]], threshold = 1
Output: [[5,6,7],[8,9,10],[11,12,13]]
Explanation:
唯一的 `3 x 3` 子网格不满足相邻像素差 ≤ threshold 的条件，例如 `|5 - 8| = 3 > 1`。因此没有像素属于任何有效区域，结果与原图相同。
```

### 约束条件
- `3 <= m, n <= 500`
- `0 <= image[i][j] <= 255`
- `0 <= threshold <= 255`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **遍历所有 3×3 子网格**  
   - 对于左上角坐标 `(i, j)`（`0 ≤ i ≤ m‑3, 0 ≤ j ≤ n‑3`），把以它为左上角的 3×3 区块取出来。  
   - 这相当于在一张大图片里，拿一块 3×3 的“拼图”逐个检查。  

2. **检查相邻像素的差值**  
   - 在 3×3 区块里，每两个相邻（上下或左右）像素的差值必须 ≤ `threshold`。  
   - 可以把 3×3 看成一个 3 行 3 列的格子，格子之间的“边”共有 12 条（3 行 × 2 横向 + 2 行 × 3 纵向）。  
   - 只要遍历这 12 条边，计算 `abs(a‑b) ≤ threshold`，全部满足则该子网格是一个 **region**。  

3. **统计每个 region 的平均强度**  
   - 先把 9 个像素求和 `s`，平均值向下取整 `avg = s // 9`（整数除法自动向下取整）。  
   - 把 `avg` 加到这 9 个像素对应位置的 **累计和** `sum[i][j]` 中，并把计数 `cnt[i][j]` 加 1，表示该像素属于了多少个 region。  

4. **得到最终答案**  
   - 对每个像素 `(i, j)`：  
     - 若 `cnt[i][j] == 0`，说明它不在任何 region，直接返回原图的值 `image[i][j]`。  
     - 否则，先把累计和除以计数得到 **所有 region 平均值的平均**，再向下取整：`result[i][j] = sum[i][j] // cnt[i][j]`。  

> **类比**：  
> - `sum` 像是给每个像素记账本，记录它“收了多少笔 region 的平均工资”。  
> - `cnt` 像是记账本的页数，记录它“被几笔工资打到”。最终的工资就是 “总工资 / 账本页数”。  

#### 代码（Python）

```python
from typing import List

def findGridOfRegionAverage(image: List[List[int]], threshold: int) -> List[List[int]]:
    m, n = len(image), len(image[0])

    # 累计每个像素所在 region 的平均值之和
    sum_grid = [[0] * n for _ in range(m)]
    # 记录每个像素属于了多少个 region
    cnt_grid = [[0] * n for _ in range(m)]

    # ----------- 1. 枚举所有左上角 (i, j) ----------
    for i in range(m - 2):          # 只到 m-3，因为要留出 3 行
        for j in range(n - 2):      # 同理，留出 3 列
            # ----------- 2. 检查 12 条相邻边 ----------
            ok = True
            # 横向相邻：3 行 × 2 条
            for r in range(3):
                for c in range(2):
                    a = image[i + r][j + c]
                    b = image[i + r][j + c + 1]
                    if abs(a - b) > threshold:
                        ok = False
                        break
                if not ok:
                    break
            # 纵向相邻：2 行 × 3 条
            if ok:
                for r in range(2):
                    for c in range(3):
                        a = image[i + r][j + c]
                        b = image[i + r + 1][j + c]
                        if abs(a - b) > threshold:
                            ok = False
                            break
                    if not ok:
                        break

            # ----------- 3. 如果是合法 region，统计平均 ----------
            if ok:
                total = 0
                for r in range(3):
                    for c in range(3):
                        total += image[i + r][j + c]
                avg = total // 9          # 向下取整的平均强度

                # 把 avg 加到子网格里每个像素的累计和与计数中
                for r in range(3):
                    for c in range(3):
                        x, y = i + r, j + c
                        sum_grid[x][y] += avg
                        cnt_grid[x][y] += 1

    # ----------- 4. 生成结果 ----------
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if cnt_grid[i][j] == 0:          # 没有属于任何 region
                result[i][j] = image[i][j]
            else:
                result[i][j] = sum_grid[i][j] // cnt_grid[i][j]
    return result
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 解释：左上角的遍历次数约为 `(m‑2)*(n‑2)`，每个子网格检查常数 12 条边、求和 9 个数、更新 9 次，都是 **常数时间**。所以整体随矩阵大小线性增长。  
- **空间复杂度**：`O(m * n)`  
  - 解释：我们额外用了两张和原图同尺寸的二维数组 `sum_grid`、`cnt_grid`，因此空间与输入规模成正比。  

---  

### 2. 最优解  

#### 思路  

暴力解已经是 **线性** 的，但是我们仍可以把实现细节再优化，让代码更简洁、常数因子更小：

1. **利用前缀和快速求子网格的像素和**  
   - 对整个 `image` 先算出二维前缀和 `pref`（`pref[i+1][j+1]` 为左上 `(0,0)` 到 `(i,j)` 的累计和）。  
   - 那么任意 3×3 区块的总和可以 **O(1)** 通过四个前缀和相减得到，省去每次遍历 9 个格子求和的开销。  

2. **一次性检查相邻差值**  
   - 对每个方向（右、下）预先算出 “相邻差值是否 ≤ threshold” 的布尔矩阵 `right_ok`、`down_ok`。  
   - 对于一个 3×3 区块，只要检查这 12 条对应的布尔值全为 `True` 即可，避免重复计算 `abs`。  

3. **整体流程**  
   - ① 计算前缀和 `pref`（`O(mn)`）。  
   - ② 计算 `right_ok`、`down_ok`（同样 `O(mn)`）。  
   - ③ 再遍历左上角 `(i,j)`：  
        - 用 `right_ok`、`down_ok` 检查 12 条边（常数）。  
        - 若合法，利用前缀和直接得到区块总和 `s`，算出 `avg = s // 9`。  
        - 用同样的 3×3 循环把 `avg` 加到 `sum_grid`、`cnt_grid`。  
   - ④ 最后一次遍历得到 `result`。  

> **类比**：  
> - 前缀和就像一本“累计账本”，记下了每一行每一列到当前位置的总收入。查询任意子矩形的收入，只要看账本的四个角就行，省时又省力。  

#### 代码（Python）

```python
from typing import List

def findGridOfRegionAverage_opt(image: List[List[int]], threshold: int) -> List[List[int]]:
    m, n = len(image), len(image[0])

    # ---------- 1. 计算二维前缀和 ----------
    pref = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        row_sum = 0
        for j in range(n):
            row_sum += image[i][j]
            pref[i + 1][j + 1] = pref[i][j + 1] + row_sum

    # ---------- 2. 预计算相邻差值是否满足阈值 ----------
    # right_ok[i][j] 表示 (i,j) 与 (i,j+1) 的差值 ≤ threshold
    right_ok = [[False] * (n - 1) for _ in range(m)]
    for i in range(m):
        for j in range(n - 1):
            right_ok[i][j] = abs(image[i][j] - image[i][j + 1]) <= threshold

    # down_ok[i][j] 表示 (i,j) 与 (i+1,j) 的差值 ≤ threshold
    down_ok = [[False] * n for _ in range(m - 1)]
    for i in range(m - 1):
        for j in range(n):
            down_ok[i][j] = abs(image[i][j] - image[i + 1][j]) <= threshold

    # ---------- 3. 累计每个像素所在 region 的平均 ----------
    sum_grid = [[0] * n for _ in range(m)]
    cnt_grid = [[0] * n for _ in range(m)]

    for i in range(m - 2):
        for j in range(n - 2):
            # 检查 12 条边：先横向再纵向
            ok = True
            # 横向：3 行 × 2 条
            for r in range(3):
                if not (right_ok[i + r][j] and right_ok[i + r][j + 1]):
                    ok = False
                    break
            # 纵向：2 行 × 3 条
            if ok:
                for r in range(2):
                    if not (down_ok[i + r][j] and down_ok[i + r][j + 1] and down_ok[i + r][j + 2]):
                        ok = False
                        break
            if not ok:
                continue

            # 该 3×3 区块合法，利用前缀和求总和
            # 区块左上 (i,j)，右下 (i+2, j+2)
            total = (
                pref[i + 3][j + 3] - pref[i][j + 3] -
                pref[i + 3][j] + pref[i][j]
            )
            avg = total // 9

            # 把 avg 加到子块里每个像素的累计信息中
            for r in range(3):
                for c in range(3):
                    x, y = i + r, j + c
                    sum_grid[x][y] += avg
                    cnt_grid[x][y] += 1

    # ---------- 4. 生成最终结果 ----------
    result = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if cnt_grid[i][j] == 0:
                result[i][j] = image[i][j]
            else:
                result[i][j] = sum_grid[i][j] // cnt_grid[i][j]
    return result
```

#### 复杂度  

- **时间复杂度**：`O(m * n)`  
  - 前缀和、`right_ok`、`down_ok` 各一次遍历 + 主循环仍然是线性。相比暴力版省去了每次子网格内部的 9 次求和和 12 次 `abs`，常数因子更小。  
- **空间复杂度**：`O(m * n)`  
  - 额外使用了前缀和、两个布尔矩阵以及累计数组，总共仍是若干个和原图同尺寸的二维数组。  

---  

## 心得  

- **核心技巧**：  
  1. **枚举固定大小子矩阵**（这里是 3×3）并利用**常数时间检查**相邻约束。  
  2. **二维前缀和**把子矩阵求和从 `O(k²)` 降到 `O(1)`（`k` 为子矩阵边长）。  
  3. **累计 + 计数**的思想，让每个像素可以“被多次引用”，最终再做一次除法得到平均。  

- **该技巧适用的题型**（举例）：  
  - “滑动窗口求子矩阵和”类题目，如 LeetCode 1695 “Maximum Erasure Value”。  
  - “子矩阵满足某种局部约束”类题目，如 LeetCode 1277 “Count Square Submatrices with All Ones”。  
  - “多次覆盖求最终值”类题目，如 LeetCode 2470 “Number of Subarrays With Median K”。  

- **一句话总结解题钥匙**：  
  > “把所有子矩阵的局部检查和整体求和都做成常数时间，再用累计/计数的方式把多重覆盖自然合并”。  

---  

## 反思  

- **第一反应**：直接把每个 3×3 子网格全部遍历、每次逐格检查相邻差值、求和、更新。  
- **最容易踩的坑**：  
  1. **边界遗漏**：子网格左上角只能取到 `m‑3`、`n‑3`，否则会越界。  
  2. **相邻检查不全**：必须检查 **所有 12 条边**，漏掉任意一条都会导致错误的 region 判定。  
  3. **整数取整规则**：先对每个 region 取整（`//9`），再对每个像素的平均再取整，顺序不能颠倒。  
  4. **计数为零时的处理**：`cnt[i][j]==0` 时要直接返回原像素值，防止除以零错误。  

- **下次类似题的第一步**：  
  > “先把固定大小的子结构（如 3×3）所有可能的左上角列举出来，利用前缀和或布尔预处理把局部约束和子结构求和都压缩到 O(1)”。这样可以在保证正确性的前提下，把整体时间控制在 `O(mn)`。