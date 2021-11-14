# #1551. 使数组相等的最小操作次数 / Minimum Operations to Make Array Equal

> 难度：中等 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-array-equal/)

---

## 题目（英文原版）

**Description**

You have an array arr of length n where arr[i] = (2 * i) + 1 for all valid values of i (i.e., 0 <= i < n).
In one operation, you can select two indices x and y where 0 <= x, y < n and subtract 1 from arr[x] and add 1 to arr[y] (i.e., perform arr[x] -=1 and arr[y] += 1). The goal is to make all the elements of the array equal. It is guaranteed that all the elements of the array can be made equal using some operations.
Given an integer n, the length of the array, return the minimum number of operations needed to make all the elements of arr equal.

**Examples**

**Example 1:**

```
Input: n = 3
Output: 2
Explanation: arr = [1, 3, 5]
First operation choose x = 2 and y = 0, this leads arr to be [2, 3, 4]
In the second operation choose x = 2 and y = 0 again, thus arr = [3, 3, 3].
```

**Example 2:**

```
Input: n = 6
Output: 9
```

**Constraints**

- 1 <= n <= 104

---

## 题目（中文翻译）

你有一个长度为 `n` 的数组 `arr`，其中 `arr[i] = (2 * i) + 1` 对所有满足 `0 <= i < n` 的下标 `i` 都成立。  
在一次操作中，你可以选择两个下标 `x` 和 `y`（满足 `0 <= x, y < n`），将 `arr[x]` 减 1 并将 `arr[y]` 加 1（即执行 `arr[x] -= 1` 与 `arr[y] += 1`）。目标是让数组中的所有元素相等。题目保证可以通过若干操作使数组所有元素相等。  

给定整数 `n`（数组的长度），返回使 `arr` 中所有元素相等所需的最小操作次数。

## 示例

### 示例 1
**输入**  
```
n = 3
```
**输出**  
```
2
```
**解释**  
初始 `arr = [1, 3, 5]`。  
- 第一次操作选择 `x = 2`、`y = 0`，得到 `arr = [2, 3, 4]`。  
- 第二次操作再次选择 `x = 2`、`y = 0`，得到 `arr = [3, 3, 3]`。

### 示例 2
**输入**  
```
n = 6
```
**输出**  
```
9
```

## 约束条件
- `1 <= n <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出的数组 `arr[i] = 2*i + 1`（即 1、3、5、…），我们可以把它想成一排 **装满球的盒子**：  
- 盒子里球的数量就是 `arr[i]`。  
- 一次操作相当于 **从一个盒子里拿走 1 球**，再 **放进另一个盒子**。  

最直观的做法是：  
1. 先算出目标值 `target = sum(arr) / n`（所有盒子最终要拥有的球数）。  
2. 每次遍历数组，找出一个**球多**的盒子 `x`（`arr[x] > target`）和一个**球少**的盒子 `y`（`arr[y] < target`），把球从 `x` 移到 `y`。  
3. 重复第 2 步，直到所有盒子里球数都等于 `target` 为止。

> **为什么能成功？**  
> 每一次操作都把「多余的」球转移到「缺少的」盒子，整体球数不变，且多余的球总量在逐步减小。只要目标 `target` 是整数（题目已保证），最终必能全部平衡。

> **时间/空间分析（大白话）**  
> - **时间复杂度**：每一次操作我们都要遍历整个数组去找 `x`、`y`，最坏情况下需要做 `O(totalDiff)` 次操作，而 `totalDiff` 可能和 `n` 同阶（比如 `n=10^4` 时需要几千次），于是整体是 **O(n²)**。可以把它想成「每搬一次球，都要重新检查所有盒子」。
> - **空间复杂度**：只用了几个临时变量，**O(1)**（常数级别的额外空间）。

#### 代码（Python）

```python
def min_operations_bruteforce(n: int) -> int:
    # 1. 生成原数组
    arr = [2 * i + 1 for i in range(n)]          # [1, 3, 5, ...]
    target = sum(arr) // n                        # 必然是整数

    ops = 0
    while True:
        # 2. 找到第一个大于 target 的位置 x
        x = next((i for i, v in enumerate(arr) if v > target), None)
        # 3. 找到第一个小于 target 的位置 y
        y = next((i for i, v in enumerate(arr) if v < target), None)

        # 4. 若不存在 x 或 y，说明已经全部相等，结束循环
        if x is None or y is None:
            break

        # 5. 执行一次转移操作
        arr[x] -= 1        # 从多的盒子拿走 1 球
        arr[y] += 1        # 把球放进少的盒子
        ops += 1           # 计数

    return ops
```

> **关键行中文注释** 已在代码中给出，直接复制运行即可看到答案（虽慢，但思路清晰）。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 想象每搬一球都要全表扫描，最坏会出现 `n` 次循环，每次遍历 `n` 项。
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈是每次都要遍历数组寻找 `x、y`**。其实我们不需要模拟搬球的过程，只要算出**总共要搬走多少球**就行，因为每搬走 1 球就对应一次操作。

1. **求目标值**  
   \[
   arr[i] = 2i + 1 \quad (0 \le i < n)
   \]
   求和：
   \[
   \sum_{i=0}^{n-1} (2i+1) = n^2
   \]
   所以平均值（目标值）是  
   \[
   target = \frac{n^2}{n} = n
   \]

2. **统计「多余的」球**  
   只要 `arr[i] > target`，这个盒子里有多余的球，需要把它们搬走。  
   把所有多余球的数量加起来，就是最少操作次数（因为每次只能搬走 1 球）。

3. **利用数组的规律化简**  
   `arr` 是严格递增的奇数列，`target = n`。  
   - 当 `n` 为 **偶数**（设 `n = 2k`）时，`target = 2k`。  
     第 `k` 个位置开始的元素都大于 `target`：  
     \[
     arr[k] = 2k+1,\; arr[k+1]=2k+3,\dots,arr[2k-1]=4k-1
     \]
     多余球总数：
     \[
     \sum_{i=k}^{2k-1} (arr[i] - 2k)
     = \sum_{j=0}^{k-1} (2j+1) = k^2
     \]
   - 当 `n` 为 **奇数**（设 `n = 2k+1`）时，`target = 2k+1`。  
     从第 `k+1` 个位置开始的元素都大于 `target`：  
     \[
     \sum_{i=k+1}^{2k} (arr[i] - (2k+1))
     = \sum_{j=1}^{k} (2j) = k(k+1)
     \]

4. **统一公式**  
   观察两种情况可以写成：
   \[
   \boxed{answer = \left\lfloor\frac{n}{2}\right\rfloor \times \left\lceil\frac{n}{2}\right\rceil}
   \]
   也就是 **“左边一半乘右边一半”**。  
   - `n//2` → 向下取整的半数  
   - `(n+1)//2` → 向上取整的半数  

   这一步只用了 **常数时间**，不需要遍历数组。

> **类比**：把所有盒子想成一条天平，两边球的数量差距就是需要搬走的球数。只要算出左边（或右边）缺少的总球数，就等于右边多余的总球数，也就是最少搬运次数。

#### 代码（Python）

```python
def min_operations(n: int) -> int:
    """
    返回使 arr[i] = 2*i+1 的数组全部相等所需的最少操作次数。
    关键公式： floor(n/2) * ceil(n/2)
    """
    left = n // 2               # 向下取整的“左半边”
    right = (n + 1) // 2        # 向上取整的“右半边”
    return left * right
```

> 代码只有两行，直接返回公式结果，时间 **O(1)**，空间 **O(1)**。

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做了几次整数运算，不随 `n` 增长。
- **空间复杂度**：`O(1)` —— 只用了几个整数变量。

相比暴力的 `O(n²)`，这里快了 **指数级**，在 `n = 10⁴` 时瞬间返回答案。

---

## 心得

- **核心技巧**：把“把所有元素变成同一个数”的过程抽象为“统计多余（或缺少）的总量”，利用**平均值**和**数组的数学特性**直接求和。
- **适用场景**  
  1. **均分/平衡类**问题（如把糖果均分、把石子搬到同一点）。  
  2. **单调序列的求和**（利用等差数列求和公式）。  
  3. **只需要计数不需要模拟**的题目（如“最小移动次数”“最少翻转次数”等）。
- **一句话总结**：**把“操作次数”等价为“多余元素的总和”，直接用等差数列求和即可得到 O(1) 解**。

---

## 反思

- **第一反应**：看到“把一个数减 1、另一个数加 1”，自然想到“模拟搬球”。这会让人陷入 O(n²) 的实现陷阱。
- **最容易踩的坑**  
  - 忘记先确认目标值 `target` 必须是整数（虽然题目保证，但在实际面试中要自行验证）。  
  - 直接遍历数组统计差值时，容易把“缺少的”也算进去，导致答案翻倍。正确做法是只统计 **大于 target 的差值**（或只统计小于的绝对值，二者相等）。  
  - 边界条件 `n=1`：此时数组已经相等，答案应为 0，公式 `floor(1/2)*ceil(1/2)=0*1=0` 正确。
- **下次类似题的第一步**：  
  1. 计算总和 → 平均值 → 目标值。  
  2. 判断是“搬运”还是“翻转”，只需要 **统计偏离目标的总量**，而不是一步步模拟。这样往往能直接得到 O(1) 或 O(n) 的简洁解。