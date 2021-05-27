# #1343. 大小为 K 且平均值大于等于阈值的子数组个数 / Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/)

---

## 题目（英文原版）

**Description**

Given an array of integers arr and two integers k and threshold, return the number of sub-arrays of size k and average greater than or equal to threshold.

**Examples**

**Example 1:**

```
Input: arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4
Output: 3
Explanation: Sub-arrays [2,5,5],[5,5,5] and [5,5,8] have averages 4, 5 and 6 respectively. All other sub-arrays of size 3 have averages less than 4 (the threshold).
```

**Example 2:**

```
Input: arr = [11,13,17,23,29,31,7,5,2,3], k = 3, threshold = 5
Output: 6
Explanation: The first 6 sub-arrays of size 3 have averages greater than 5. Note that averages are not integers.
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= arr[i] <= 104
- 1 <= k <= arr.length
- 0 <= threshold <= 104

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `arr`，以及两个整数 `k` 和 `阈值（threshold）`，返回满足以下条件的子数组（sub-arrays）个数：子数组的大小恰好为 `k`，且其平均值大于或等于 `阈值（threshold）`。

**示例 1**  
```text
Input: arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4
Output: 3
Explanation: 子数组 [2,5,5]、[5,5,5] 和 [5,5,8] 的平均值分别为 4、5、6，均不小于阈值。其余所有大小为 3 的子数组的平均值均小于 4（阈值）。
```

**示例 2**  
```text
Input: arr = [11,13,17,23,29,31,7,5,2,3], k = 3, threshold = 5
Output: 6
Explanation: 前 6 个大小为 3 的子数组的平均值均大于 5。注意，平均值不一定是整数。
```

**约束条件**  
- `1 <= arr.length <= 10^5`  
- `1 <= arr[i] <= 10^4`  
- `1 <= k <= arr.length`  
- `0 <= threshold <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把数组里所有可能的长度为 `k` 的连续子数组都枚举出来，逐个计算它们的平均值，看看是否 ≥ `threshold`，满足的就计数。

- **数据结构**：只需要普通的 Python 列表 `arr`。遍历子数组时，用 `sum()` 把子数组里所有元素加起来，`sum / k` 就是平均值。  
  > 类比：把 `arr` 想成一本书的文字，`k` 就是一次要读的连续 `k` 页。我们把每一种连续 `k` 页的文字都读一遍，算出平均字数，看是否够多。

- **正确性**：因为我们把**所有**可能的长度为 `k` 的子数组都检查了一遍，凡是平均值 ≥ `threshold` 的子数组必然被计数，所以答案一定正确。

- **复杂度分析**：  
  - 外层循环要遍历 `n‑k+1` 次（`n` 为数组长度），每次都要对长度为 `k` 的子数组求和，求和本身是 `O(k)`。  
  - 所以总时间是 `O((n‑k+1)·k) ≈ O(n·k)`。在最坏情况下 `k≈n`，时间会退化到 `O(n²)`。  
  - 只用了常数级别的额外空间，`O(1)`。

> 大白话解释：如果数组有 10 万个元素，而我们每次都要把 5 万个数加一次，那就相当于要跑 5 0000 × 5 0000 = 2.5 × 10⁹ 次加法，明显太慢了。

#### 代码（Python）

```python
def numOfSubarrays_bruteforce(arr, k, threshold):
    """
    暴力解：枚举所有长度为 k 的子数组，逐个计算平均值
    """
    n = len(arr)
    count = 0                         # 记录满足条件的子数组个数
    for start in range(n - k + 1):    # 子数组的左端点
        window = arr[start:start + k]        # 取出长度为 k 的子数组（切片）
        avg = sum(window) / k                 # 计算平均值
        if avg >= threshold:                  # 与阈值比较
            count += 1
    return count
```

#### 复杂度

- **时间复杂度**：`O(n·k)`  
  - 意味着如果 `k` 很大，时间会接近 `n²`，在 10⁵ 规模的数据上会超时。
- **空间复杂度**：`O(1)`（不计返回值和输入数组本身）  
  - 只用了几个整数变量，额外占用的内存可以忽略不计。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都重新求和**。实际上，连续子数组的和有很强的**递推关系**：

> 当窗口从 `[i, i+k-1]` 移动到 `[i+1, i+k]` 时，只丢掉左边的 `arr[i]`，再加入右边的 `arr[i+k]`，其余 `k‑1` 个元素保持不变。

利用这个特性，我们可以用 **滑动窗口（Sliding Window）** 只维护当前窗口的**和**，而不是每次都重新遍历 `k` 个元素。

步骤如下：

1. 先计算第一个窗口（`arr[0:k]`）的总和 `window_sum`。  
2. 判断 `window_sum / k >= threshold`，若成立计数 `+1`。  
3. 然后把窗口右移一位：`window_sum = window_sum - arr[left] + arr[right]`（`left` 为左边即将离开的元素索引，`right` 为新加入的元素索引）。  
4. 重复第 2 步，直到窗口滑到数组末端。

**为什么可以用和来代替平均值比较？**  

比较 `average >= threshold` 等价于 `sum/k >= threshold`，两边同乘 `k`（`k` 为正数），得到 `sum >= threshold * k`。于是只要比较**窗口和**是否不小于 `threshold * k` 即可，无需做除法，避免了浮点数误差，也更快。

**核心数据结构**：  
- **滑动窗口**：实际上只用两个指针 `left`（窗口左端）和 `right`（窗口右端），以及一个整数 `window_sum` 保存当前窗口的元素和。  
  > 类比：把窗口想成一根可滑动的尺子，尺子上只放了 `k` 块砖头。每次往前移动时，只把左边最旧的砖头拿走，放进新的砖头，砖头的总重量我们随时记录下来。

#### 代码（Python）

```python
def numOfSubarrays(arr, k, threshold):
    """
    最优解：滑动窗口，只维护窗口的和
    """
    n = len(arr)
    need = threshold * k            # 预先把阈值乘以 k，转化为 “和的阈值”
    window_sum = sum(arr[:k])       # 第一个窗口的和
    count = 1 if window_sum >= need else 0

    # 从下标 k 开始遍历，right 为新加入元素的下标
    for right in range(k, n):
        left = right - k             # left 为即将移出的元素下标
        # 更新窗口和：减去左边元素，加上右边元素
        window_sum += arr[right] - arr[left]
        if window_sum >= need:       # 判断是否满足 “和 >= need”
            count += 1

    return count
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 只遍历数组一次，窗口每移动一步只做常数次加减操作。相较于暴力 `O(n·k)`，在 `n=10⁵`、`k≈n` 时快了近 `k` 倍。
- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（`window_sum`, `need`, `count`），不随 `n` 增长。

---

## 心得

- **核心技巧**：滑动窗口（Sliding Window）——在处理“连续子数组/子串的固定长度”问题时，维护一个可滚动的“窗口”并只在窗口两端做增删，能够把重复的计算消除掉。
- **适用的题型**  
  1. **固定长度子数组求和或均值**（如本题、LeetCode 1343 “Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold”）。  
  2. **固定长度子串中字符种类统计**（如 LeetCode 567 “Permutation in String” 的固定窗口版）。  
  3. **固定窗口内的最大/最小值**（如 LeetCode 239 “Sliding Window Maximum”）。
- **一句话总结**：**“把每一次完整的重新计算，换成‘把左边的踢出去、把右边的踢进来’”。**

---

## 反思

- **第一反应**：看到“子数组大小 k”和“平均值”这两个关键词，立刻想到枚举所有子数组并逐个计算平均值——也就是暴力解。
- **最容易踩的坑**  
  1. **浮点数比较**：直接比较 `sum/k >= threshold` 可能出现精度误差，最好转化为整数比较 `sum >= threshold * k`。  
  2. **边界条件**：`k` 可能等于 `len(arr)`，此时只能有一个窗口，需要确保循环不会越界。  
  3. **大数乘法**：`threshold * k` 可能超过 32 位整数范围，但在 Python 中整数不溢出，仍需注意语言差异。
- **下次遇到同类题**：第一步先问自己“窗口大小固定吗？如果是，能否用滑动窗口把‘每次重新求和’改成‘增删一步’？”这一步往往就能直接导向最优解。