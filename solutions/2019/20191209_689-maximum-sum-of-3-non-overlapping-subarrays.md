# #689. 最大和的三个不重叠子数组 / Maximum Sum of 3 Non-Overlapping Subarrays

> 难度：困难 · 标签：Array、Dynamic Programming、Sliding Window、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, find three non-overlapping subarrays of length k with maximum sum and return them.
Return the result as a list of indices representing the starting position of each interval (0-indexed). If there are multiple answers, return the lexicographically smallest one.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,2,6,7,5,1], k = 2
Output: [0,3,5]
Explanation: Subarrays [1, 2], [2, 6], [7, 5] correspond to the starting indices [0, 3, 5].
We could have also taken [2, 1], but an answer of [1, 3, 5] would be lexicographically larger.
```

**Example 2:**

```
Input: nums = [1,2,1,2,1,2,1,2,1], k = 2
Output: [0,2,4]
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 1 <= nums[i] < 216
- 1 <= k <= floor(nums.length / 3)

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`，请找出长度为 `k` 的 **三个不重叠子数组（subarray）**，使它们的和最大，并返回这三个子数组的起始下标。  
返回的结果应为一个下标列表，表示每个区间的起始位置（0 起始）。如果存在多个答案，返回字典序最小的那一个。

## 示例

### 示例 1
**Input:**  
`nums = [1,2,1,2,6,7,5,1]`, `k = 2`  

**Output:**  
`[0,3,5]`  

**Explanation:**  
子数组 `[1, 2]、[2, 6]、[7, 5]` 对应的起始下标分别为 `[0, 3, 5]`。  
我们也可以选择子数组 `[2, 1]`，但答案 `[1, 3, 5]` 在字典序上更大。

### 示例 2
**Input:**  
`nums = [1,2,1,2,1,2,1,2,1]`, `k = 2`  

**Output:**  
`[0,2,4]`  

## 约束条件
- `1 <= nums.length <= 2 * 10^4`
- `1 <= nums[i] < 2^16`
- `1 <= k <= floor(nums.length / 3)`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把所有可能的三段长度为 `k` 的子数组都枚举一遍，然后比较它们的和，选出最大的那组。  
具体步骤：

1. **枚举起始下标**  
   - 设第一个子数组的起始位置为 `i`，第二个为 `j`，第三个为 `l`。  
   - 必须满足 `i + k ≤ j` 且 `j + k ≤ l`（即三段不重叠），并且 `i < j < l`。  

2. **计算子数组和**  
   - 为了避免每次都循环 `k` 次求和，我们可以先把原数组的前缀和算出来。  
   - 前缀和就像一本字典，`pre[t]` 记录了数组前 `t` 个数的总和，求区间 `[a, b]` 的和只需要 `pre[b+1] - pre[a]`，相当于“一下子翻到对应页码”。  

3. **比较并记录**  
   - 对每一组三个下标，算出 `sum(i) + sum(j) + sum(l)`，如果比当前最大值大就更新答案。  

因为我们把所有合法的三元组都尝试了一遍，答案一定是对的——只要遍历完整个搜索空间，就不会漏掉最优解。

**时间复杂度**  
- 三层循环遍历所有 `(i, j, l)`，最坏情况下大约是 `O(n³)`（`n` 为数组长度），即使每次求和只用 `O(1)`（前缀和），整体仍是立方级别。  
- 对于 `n ≤ 2·10⁴` 的数据，这远远超出可接受的范围，会超时。

**空间复杂度**  
- 需要一个长度为 `n+1` 的前缀和数组，`O(n)` 的额外空间。

#### 代码（Python）

```python
def max_sum_of_three_subarrays_bruteforce(nums, k):
    n = len(nums)
    # ---------- 前缀和 ----------
    pre = [0] * (n + 1)               # pre[t] = nums[0] + ... + nums[t-1]
    for i in range(n):
        pre[i + 1] = pre[i] + nums[i]

    # ---------- 求区间和的快捷函数 ----------
    def window_sum(start):
        # 子数组 nums[start : start + k] 的和
        return pre[start + k] - pre[start]

    best_sum = -1
    best_idxs = None

    # ---------- 暴力枚举三段 ----------
    for i in range(n - 3 * k + 1):          # 第一个子数组的起点
        for j in range(i + k, n - 2 * k + 1):   # 第二个子数组的起点
            for l in range(j + k, n - k + 1):   # 第三个子数组的起点
                cur = window_sum(i) + window_sum(j) + window_sum(l)
                if cur > best_sum:
                    best_sum = cur
                    best_idxs = [i, j, l]

    return best_idxs
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  这里的 `n³` 可以想象成“把所有可能的三支队伍从 `n` 个人中挑选出来”，数量非常大，实际运行会非常慢。  

- **空间复杂度**：`O(n)`  
  只用了前缀和数组来加速区间求和，额外的空间随输入规模线性增长。  

---  

### 2. 最优解

#### 思路  
从暴力解可以看到，**枚举三次是瓶颈**。我们需要把搜索空间压缩到 **线性** 或 **准线性**。

关键观察：

1. **子数组长度固定为 `k`**  
   - 可以把每个长度为 `k` 的子数组的和预先算好，得到一个新数组 `w`，其中 `w[i]` 表示以 `i` 为起点的长度为 `k` 的子数组和。  
   - 这一步只需要一次滑动窗口：窗口右移时加进新元素、减去左边离开的元素，时间 `O(n)`。  

2. **把三段的选择拆成“左、 中、 右”三部分**  
   - 设中间子数组的起点为 `j`（`k ≤ j ≤ len(w)-k-1`），左边子数组只能在 `[0, j‑k]` 里，右边只能在 `[j+k, len(w)-1]` 里。  
   - 如果我们事先知道 **左侧最大和的起点** 和 **右侧最大和的起点**，那么只要遍历一次所有可能的 `j`，就能得到最优的三段组合。  

3. **动态规划记录最优子结构**  
   - `left_best[i]`：在区间 `[0, i]`（含 `i`）里，`w` 最大的下标。若出现相同的和，取**左侧更小的下标**，这样可以保证最终答案的字典序最小。  
   - `right_best[i]`：在区间 `[i, len(w)-1]`（含 `i`）里，`w` 最大的下标。同理，若相同则取**右侧更小的下标**（因为我们从右往左遍历）。  

   这两个数组本质上是“子问题的最优解”，是 DP 的经典做法。  

4. **遍历中间位置求最终答案**  
   - 对每个合法的 `j`，左边最佳起点是 `left_best[j - k]`，右边最佳起点是 `right_best[j + k]`。  
   - 计算总和 `w[left] + w[j] + w[right]`，如果更大就更新；如果相等则比较下标的字典序（因为 `left_best` 与 `right_best` 已经保证了最左/最右的选择，所以只需要比较整体的三元组即可）。  

5. **复杂度分析**  
   - 预处理 `w`、`left_best`、`right_best` 都是一次线性扫描，整体时间 `O(n)`，空间 `O(n)`。  

下面用类比帮助理解：

- **滑动窗口**：想象你在跑道上跑步，手里拿着一块长 `k` 的地毯。每跨一步，左边的地毯掉下来，你再把右边的新地面铺上，这样你随时知道自己正踩的 `k` 块地的总重量（即子数组和）。  
- **左侧最优记录**：在跑道的左边设了一个“最高分榜”，每跑到一个位置，就把当前子数组的分数和位置和榜单比较，若更高就更新。这样跑到任意位置时，你都能立刻知道左边的“最高分”。  
- **右侧最优记录**：同理，只是从右边往左跑，建立“右侧最高分榜”。  

把这三块信息（左、 中、 右）组合起来，就能一次得到全局最优。

#### 代码（Python）

```python
def max_sum_of_three_subarrays(nums, k):
    n = len(nums)
    # ---------- 第一步：计算所有长度为 k 的子数组和 ----------
    # w[i] = sum(nums[i:i+k])
    w = [0] * (n - k + 1)
    cur = sum(nums[:k])          # 初始窗口
    w[0] = cur
    for i in range(1, n - k + 1):
        cur += nums[i + k - 1] - nums[i - 1]   # 滑动窗口：加右边，减左边
        w[i] = cur

    m = len(w)   # m = n - k + 1

    # ---------- 第二步：左侧最大子数组的起点 ----------
    left_best = [0] * m
    best_idx = 0
    for i in range(m):
        # 如果当前 w[i] 更大，或者相等但下标更左，则更新 best_idx
        if w[i] > w[best_idx] or (w[i] == w[best_idx] and i < best_idx):
            best_idx = i
        left_best[i] = best_idx

    # ---------- 第三步：右侧最大子数组的起点 ----------
    right_best = [0] * m
    best_idx = m - 1
    for i in range(m - 1, -1, -1):
        # 同样的比较规则，只是遍历方向相反
        if w[i] >= w[best_idx]:   # 注意这里用 >=，保证字典序最小
            best_idx = i
        right_best[i] = best_idx

    # ---------- 第四步：遍历中间子数组 ----------
    max_total = -1
    ans = None
    # 中间子数组的起点必须保证左右各有足够空间放下 k 长度的子数组
    for mid in range(k, m - k):
        left = left_best[mid - k]      # 左侧最佳起点
        right = right_best[mid + k]    # 右侧最佳起点
        total = w[left] + w[mid] + w[right]

        if total > max_total:
            max_total = total
            ans = [left, mid, right]
        elif total == max_total:
            # 若总和相同，比较字典序（先比较 left，再 mid，再 right）
            if [left, mid, right] < ans:
                ans = [left, mid, right]

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 计算 `w`、`left_best`、`right_best` 各一次线性扫描，遍历中间位置再一次线性扫描。整个过程只跟数组长度成正比，远快于暴力的 `O(n³)`。  

- **空间复杂度**：`O(n)`  
  - 需要存 `w`、`left_best`、`right_best` 三个同等长度的辅助数组。若要求更省空间，可以把 `left_best` 与 `right_best` 用整数数组覆盖，但整体仍是线性级别。

---

## 心得

- **核心技巧**：前缀和/滑动窗口快速得到固定长度子数组的和 + 动态规划记录左/右侧的“局部最优”，从而把原本的三重枚举压缩到线性遍历。  
- **相似题型**  
  1. **689. Maximum Sum of 3 Non-Overlapping Subarrays**（本题）  
  2. **1031. Maximum Sum of Two Non-Overlapping Subarrays**（只需要两段，思路完全相同，只是去掉一层）  
  3. **560. Subarray Sum Equals K**（利用前缀和+哈希表快速查询子数组）  
- **一句话总结**：把“大搜索”拆成“左侧最优 + 中间 + 右侧最优”，记录子问题的最优解即可线性求解。  

## 反思

- **第一反应**：直接枚举三段子数组（暴力），因为最直观且易实现。  
- **最容易踩的坑**  
  - 忘记“非重叠”条件导致下标冲突（如 `j` 必须 ≥ `i + k`）。  
  - 当多个答案的总和相同，需要返回字典序最小的组合，容易遗漏比较细节。  
  - 边界处理：`mid` 的取值范围必须保证左侧和右侧都有足够空间放下长度为 `k` 的子数组。  
- **下次类似题目**：先问自己“子数组长度是否固定？”、“是否可以提前算出每段的和？”、“能否用前缀和/滑动窗口把子问题的最优记录下来？”这些思路会帮助快速定位到“左/右最优 + 中间遍历”的解法。