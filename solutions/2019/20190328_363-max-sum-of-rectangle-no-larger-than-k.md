# #363. 最大不超过 K 的矩形和 / Max Sum of Rectangle No Larger Than K

> 难度：困难 · 标签：Array、Binary Search、Matrix、Prefix Sum、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/max-sum-of-rectangle-no-larger-than-k/)

---

## 题目（英文原版）

**Description**

Given an m x n matrix matrix and an integer k, return the max sum of a rectangle in the matrix such that its sum is no larger than k.
It is guaranteed that there will be a rectangle with a sum no larger than k.
Follow up: What if the number of rows is much larger than the number of columns?

**Examples**

**Example 1:**

```
Input: matrix = [[1,0,1],[0,-2,3]], k = 2
Output: 2
Explanation: Because the sum of the blue rectangle [[0, 1], [-2, 3]] is 2, and 2 is the max number no larger than k (k = 2).
```

**Example 2:**

```
Input: matrix = [[2,2,-1]], k = 3
Output: 3
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -100 <= matrix[i][j] <= 100
- -105 <= k <= 105

---

## 题目（中文翻译）

给定一个 `m x n` 矩阵 `matrix` 和一个整数 `k`，返回矩阵中**矩形**（submatrix）的最大和，使其和**不大于** `k`。题目保证至少存在一个和不大于 `k` 的矩形。

**示例 1**  

**示例 2**  

**进阶**：如果行数远大于列数，该如何优化？

---

### 示例

#### 示例 1
**输入**  
```text
matrix = [[1,0,1],[0,-2,3]], k = 2
```
**输出**  
```text
2
```
**解释**  
因为蓝色矩形 `[[0, 1], [-2, 3]]` 的和为 `2`，且 `2` 是不大于 `k`（`k = 2`）的最大值。

#### 示例 2
**输入**  
```text
matrix = [[2,2,-1]], k = 3
```
**输出**  
```text
3
```

---

### 约束条件
- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 100`
- `-100 <= matrix[i][j] <= 100`
- `-10^5 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把矩阵里 **所有可能的矩形** 都枚举一遍，计算每个矩形的元素和，然后挑出不超过 `k` 的最大和。

- **矩形的表示**：先随便选左上角 `(r1, c1)`，再随便选右下角 `(r2, c2)`（要求 `r1 ≤ r2, c1 ≤ c2`），这四个坐标唯一确定一个子矩形。  
- **遍历方式**：四层循环，分别遍历 `r1, r2, c1, c2`。  
- **求和**：对每个矩形，用两层循环把它内部的每个元素加起来。

> **类比**：想象你在一本书里找连续的章节，暴力解就是把所有章节的起止页码全部写下来，然后一个个算总页数，看看哪段最接近但不超过目标页数 `k`。

这种方法一定能得到正确答案，因为它穷举了**所有**合法矩形，必然包含最优解。

#### 代码（Python）

```python
def maxSumSubmatrix_brute(matrix, k):
    m, n = len(matrix), len(matrix[0])
    ans = -float('inf')                     # 记录当前找到的最大和

    # 枚举左上角 (r1, c1)
    for r1 in range(m):
        for c1 in range(n):
            # 枚举右下角 (r2, c2)
            for r2 in range(r1, m):
                for c2 in range(c1, n):
                    # 计算子矩形的和
                    cur_sum = 0
                    for i in range(r1, r2 + 1):
                        for j in range(c1, c2 + 1):
                            cur_sum += matrix[i][j]
                    # 若满足条件，更新答案
                    if cur_sum <= k:
                        ans = max(ans, cur_sum)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(m² * n²)`  
  四层循环遍历所有矩形，再用两层循环求和。  
  用大白话说，就是如果矩阵是 10×10，最多要检查大约 `10⁴ = 10,000` 个矩形，每个矩形的求和又要遍历最多 `100` 个元素，整体会很慢。

- **空间复杂度**：`O(1)`  
  只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于两点：

1. **重复计算**：相邻矩形的求和很多元素是重复的，却每次都重新累加。  
2. **枚举次数过多**：四层循环直接遍历所有左上、右下坐标，组合数指数级增长。

我们可以**把矩形的求和拆成两步**：

1. **固定上下边界**（或左右边界），把二维问题压缩成“一维”——每列（或每行）累计成一个数组 `sums`，`sums[col]` 表示在当前上下边界之间，第 `col` 列所有元素的和。  
2. **在这个一维数组里找** **最长（或最大）子数组**，使得子数组的和 ≤ `k`，且尽可能接近 `k`。这一步等价于「**在前缀和序列中找最近但不超过 `k` 的差值**」。

> **类比**：把矩形看成一段连续的文字，先把每行的字符数累加成一句话（一步压缩），再在这句话里找最长且字数不超过 `k` 的子句（一步搜索）。

**关键工具**：有序集合（在 Python 中用 `bisect` 实现的「有序列表」），它可以在 `O(log n)` 时间内找到「大于等于某个值」的最小元素，正好对应「前缀和 ≥ current_sum - k」的查询。

具体步骤：

1. **遍历所有的行对**（`top` 到 `bottom`），对每一对行，更新 `sums`（累计每列的和）。  
2. 对当前的 `sums`，利用前缀和 + 有序集合求出在该行对范围内，满足条件的最大矩形和。  
   - 维护一个有序列表 `prefix`，初始包含 `0`（表示空前缀）。  
   - 逐列累加得到 `curr`（到当前列的前缀和）。  
   - 在 `prefix` 中查找最小的 `p`，满足 `p ≥ curr - k`，则 `curr - p` 就是一个合法矩形的和。  
   - 用 `bisect.insort` 把 `curr` 插回 `prefix`，保持有序。

**复杂度分析**：

- 行对的枚举是 `O(m²)`（如果 `m > n`，可以把矩阵转置，改为 `O(n²)`，这就是题目 Follow‑up 的思路）。  
- 对每个行对，遍历列一次 `O(n)`，在有序列表里查询/插入 `O(log n)`。  
- 故总时间 `O(min(m, n)² * max(m, n) * log max(m, n))`，在题目限制下足够快。

#### 代码（Python）

```python
import bisect

def maxSumSubmatrix(matrix, k):
    """
    最优解：行压缩 + 前缀和 + 有序集合（二分搜索）
    """
    m, n = len(matrix), len(matrix[0])
    # 为了让外层循环更少，始终让 rows <= cols
    if m > n:                         # 行多于列时转置矩阵
        matrix = [list(row) for row in zip(*matrix)]
        m, n = n, m

    ans = -float('inf')               # 记录全局最大合法和

    # top 为上边界，bottom 为下边界
    for top in range(m):
        # sums[c] 表示在 top~bottom 行之间，第 c 列的累计和
        sums = [0] * n
        for bottom in range(top, m):
            # 更新每列的累计和
            for c in range(n):
                sums[c] += matrix[bottom][c]

            # ---------- 在一维数组 sums 上求最大子数组和 ≤ k ----------
            # prefix 保存所有出现过的前缀和，保持有序
            prefix = [0]                 # 空前缀和
            cur = 0                      # 当前前缀和
            for val in sums:
                cur += val               # 累计到当前位置的前缀和
                # 我们希望找到最小的 p，使得 cur - p ≤ k  ⇔ p ≥ cur - k
                target = cur - k
                idx = bisect.bisect_left(prefix, target)
                if idx < len(prefix):
                    # 找到合法的前缀和 p，更新答案
                    ans = max(ans, cur - prefix[idx])
                # 将当前前缀和加入有序集合，供后续使用
                bisect.insort(prefix, cur)
            # ---------------------------------------------------------
            # 若已经找到了等于 k 的答案，直接返回（已经是最优）
            if ans == k:
                return k
    return ans
```

#### 复杂度

- **时间复杂度**：`O(min(m, n)² * max(m, n) * log max(m, n))`  
  - 大白话：先把行数（或列数）较小的维度两两配对（这一步是平方），每次配对再遍历另一维度的每个元素，并在一个“有序列表”里做二分查找（`log` 级别）。整体比暴力快了几个数量级。

- **空间复杂度**：`O(max(m, n))`  
  - 只需要额外的 `sums`（列数大小）和 `prefix`（同样大小），都是线性空间。

---

## 心得

- **核心技巧**：**行（列）压缩 + 前缀和 + 有序集合（利用二分搜索）**。  
- **适用题型**：  
  1. “**子数组和不超过 K 的最大值**” – LeetCode 560（子数组和最大不超过 K）。  
  2. “**二维子矩阵和不超过 K**” – 本题。  
  3. “**一维或二维范围求和的最优子结构**” – 如最大子矩形、最大子数组等变种。  
- **一句话总结**：**把二维问题降维成一维，再用有序前缀和快速定位“最接近但不超过 k 的和”。**

---

## 反思

- **第一反应**：直接把所有矩形枚举，写四层循环，虽然能通过小样例，却会超时。  
- **最容易踩的坑**：  
  - 忘记在 `prefix` 中先放 `0`（空前缀），会导致第一个子数组的和遗漏。  
  - 当 `k` 为负数时，仍然需要找 **最大但不超过** `k`，不能把 `ans` 初始化为 `0`。  
  - 行列不平衡时不转置会导致 `O(m² * n)` 过大，需要根据尺寸选取较小的维度做外层枚举。  
- **下次思路**：看到“矩形/子数组和 ≤ K”时，第一步想到 **前缀和 + 有序结构**（二分），第二步考虑 **降维**（行/列压缩），再决定是枚举行对还是列对。