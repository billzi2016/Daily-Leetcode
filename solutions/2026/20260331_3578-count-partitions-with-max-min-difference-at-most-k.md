# #3578. 计数最大最小差不超过 K 的划分 / Count Partitions With Max-Min Difference at Most K

> 难度：中等 · 标签：Array、Dynamic Programming、Queue、Sliding Window、Prefix Sum、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/count-partitions-with-max-min-difference-at-most-k/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k. Your task is to partition nums into one or more non-empty contiguous segments such that in each segment, the difference between its maximum and minimum elements is at most k.
Return the total number of ways to partition nums under this condition.
Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [9,4,1,3,7], k = 4
Output: 6
Explanation:
There are 6 valid partitions where the difference between the maximum and minimum elements in each segment is at most k = 4 :
```

**Example 2:**

```
Input: nums = [3,3,4], k = 0
Output: 2
Explanation:
There are 2 valid partitions that satisfy the given conditions:
```

**Constraints**

- 2 <= nums.length <= 5 * 104
- 1 <= nums[i] <= 109
- 0 <= k <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。请将 `nums` 划分为一个或多个非空的连续子段（contiguous segments），要求每个子段内的最大元素与最小元素的差值不超过 `k`。返回满足该条件的划分方式总数。由于答案可能非常大，请返回结果对 `10^9 + 7` 取模后的值。

**示例 1**  
**输入**: `nums = [9,4,1,3,7]`, `k = 4`  
**输出**: `6`  
**解释**:  
共有 6 种合法的划分，使得每个子段中最大值与最小值的差不超过 `k = 4`：

**示例 2**  
**输入**: `nums = [3,3,4]`, `k = 0`  
**输出**: `2`  
**解释**:  
共有 2 种合法的划分满足给定条件：

**约束条件**  
- `2 <= nums.length <= 5 * 10^4`  
- `1 <= nums[i] <= 10^9`  
- `0 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的切分方式**，判断每一段是否满足  
`max(segment) - min(segment) ≤ k`。  

我们可以用动态规划来把“枚举切分”写成代码：

- `dp[i]` 表示**前 i（0‑based）个元素**（即 `nums[0..i-1]`）的合法切分数目。  
- `dp[0] = 1`，因为空数组只有一种“切分”——什么也不切。  
- 对于 `i > 0`，我们尝试把最后一段的左端点放在 `j`（`0 ≤ j < i`），只要子数组 `nums[j..i-1]` 的最大值与最小值之差 ≤ `k`，就可以把 `dp[j]` 加到 `dp[i]` 上。

伪代码：

```
dp[0] = 1
for i = 1 .. n:
    dp[i] = 0
    for j = 0 .. i-1:
        if max(nums[j..i-1]) - min(nums[j..i-1]) ≤ k:
            dp[i] += dp[j]
```

> **数据结构类比**  
> - `max` / `min` 就像在字典里查“最高”和“最低”单词的页码，需要遍历整个子数组才能找到它们。  
> - `dp` 是一本记事本，`dp[i]` 记录到第 `i` 页为止有多少种合法写法。

这个办法一定能得到正确答案，因为我们把 **所有** 合法的最后一段都加进来了。

#### 代码（Python）

```python
MOD = 10 ** 9 + 7

def countPartitions_bruteforce(nums, k):
    n = len(nums)
    dp = [0] * (n + 1)          # dp[i]：前 i 个数的合法切分数
    dp[0] = 1                   # 空数组只有一种切法

    for i in range(1, n + 1):
        dp[i] = 0
        cur_max = cur_min = nums[i - 1]   # 维护子数组 nums[j..i-1] 的最大最小值
        # 从 i-1 往左遍历，逐步扩展子数组
        for j in range(i - 1, -1, -1):
            cur_max = max(cur_max, nums[j])
            cur_min = min(cur_min, nums[j])
            if cur_max - cur_min <= k:     # 当前子数组合法
                dp[i] = (dp[i] + dp[j]) % MOD
            else:                          # 已经不合法，左边继续往左也不可能合法
                break
    return dp[n]
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 外层循环 `n` 次，内层最坏也要遍历 `n` 次。  
  - “O(n²)” 可以想象成 **一张 n 行 n 列的表格**，我们把每个格子都看了一遍。

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n+1` 的 `dp` 数组，和常数级的临时变量。

> 对于 `n` 最高可达 `5·10⁴` 的数据，这个二次算法会超时，需要进一步优化。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次求 `max/min` 都要遍历子数组，导致 `O(n²)`。  
我们要把“随时知道窗口里的最大最小值”变成 **`O(1)`** 查询。  

**关键点**：

1. **滑动窗口**  
   - 维护一个左指针 `left` 和右指针 `right`（这里的 `right` 实际上就是 `i`，遍历到第 `i` 个元素时窗口为 `[left, i-1]`）。  
   - 当加入新元素 `nums[i-1]` 后，若窗口不满足 `max - min ≤ k`，就把 `left` 向右收缩，直到满足为止。  
   - 这样对于每个 `i`，`left` 正好是 **能让 `[left, i-1]` 成为合法子数组的最左位置**。

2. **单调队列（双端队列）**  
   - 用两个 `deque`（双端队列）分别维护**递减的最大值队列**和**递增的最小值队列**。  
   - 当我们把新元素 `x` 加入窗口时：
     - 对最大队列：弹出队尾所有 **小于 `x`** 的元素，再把 `x` 放进队尾。队首永远是窗口的最大值。  
     - 对最小队列：弹出队尾所有 **大于 `x`** 的元素，再把 `x` 放进队尾。队首永远是窗口的最小值。  
   - 当 `left` 移动时，如果队首对应的下标已经离开窗口，就把它弹出。这样 **随时 O(1) 能拿到窗口的 max 与 min**。

3. **前缀和 + DP**  
   - 记 `dp[i]` 为前 `i` 个元素的合法切分数（同暴力解），`dp[0]=1`。  
   - 对于固定的 `i`，合法的左端点 `j` 必须满足 `left ≤ j ≤ i-1`（因为 `[j, i-1]` 必须合法）。  
   - 所以 `dp[i] = sum_{j=left}^{i-1} dp[j]`。直接遍历求和仍是 `O(n²)`。  
   - 引入 **前缀和** `pre[i] = (pre[i-1] + dp[i]) % MOD`，则  
     `sum_{j=left}^{i-1} dp[j] = pre[i-1] - pre[left-1]`（注意取模）。  
   - 这样每个 `i` 只需要 **常数时间** 就能算出 `dp[i]`。

4. **整体流程**  

   ```
   pre[0] = dp[0] = 1
   left = 0
   for i = 1 .. n:
       把 nums[i-1] 加入单调队列，更新窗口的 max/min
       while max - min > k:
           left += 1
           把 left-1 对应的元素从单调队列中弹出（如果在队首）
       dp[i] = (pre[i-1] - pre[left-1]) % MOD
       pre[i] = (pre[i-1] + dp[i]) % MOD
   answer = dp[n]
   ```

> **类比**  
> - 单调队列像是 **“只保留最近的最高/最低的登山者”**，一直把比他矮/高的赶走，队首永远是最高/最低的。  
> - 前缀和就像 **“累计的存钱罐”**，想知道从第 `l` 天到第 `r` 天赚了多少钱，只需要 `sum[r] - sum[l-1]`。

#### 代码（Python）

```python
from collections import deque

MOD = 10 ** 9 + 7

def countPartitions(nums, k):
    n = len(nums)
    dp = [0] * (n + 1)          # dp[i]：前 i 个数的合法切分数
    pre = [0] * (n + 1)         # 前缀和，pre[i] = dp[0] + ... + dp[i]
    dp[0] = pre[0] = 1          # 空数组的唯一切法

    max_q = deque()             # 存放 (值, 下标)，递减队列，队首是最大值
    min_q = deque()             # 存放 (值, 下标)，递增队列，队首是最小值
    left = 0                     # 当前窗口的最左下标

    for i in range(1, n + 1):
        cur = nums[i - 1]        # 要加入窗口的元素

        # ---------- 更新单调队列 ----------
        while max_q and max_q[-1][0] < cur:
            max_q.pop()
        max_q.append((cur, i - 1))

        while min_q and min_q[-1][0] > cur:
            min_q.pop()
        min_q.append((cur, i - 1))

        # ---------- 收缩窗口，确保 max - min ≤ k ----------
        while max_q[0][0] - min_q[0][0] > k:
            # 左指针左移一格
            left += 1
            # 把已经离开窗口的元素从队首弹出
            if max_q[0][1] < left:
                max_q.popleft()
            if min_q[0][1] < left:
                min_q.popleft()

        # ---------- 计算 dp[i] ----------
        # 合法的左端点范围是 [left, i-1]，对应 dp[left] .. dp[i-1]
        # 使用前缀和快速求和
        dp_i = pre[i - 1] - pre[left - 1] if left > 0 else pre[i - 1]
        dp[i] = dp_i % MOD

        # ---------- 更新前缀和 ----------
        pre[i] = (pre[i - 1] + dp[i]) % MOD

    return dp[n]
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个元素至多进入、离开两个单调队列各一次，都是 `O(1)` 操作。  
  - `left` 指针只会单向移动，最多 `n` 步。  
  - 所以整体线性扫描一次即可完成。

- **空间复杂度**：`O(n)`  
  - `dp`、`pre` 各占 `O(n)`。  
  - 两个单调队列最多各保存 `n` 个元素的下标，整体仍是 `O(n)`。

> 与暴力解相比，时间从 **“看每个格子”** 降到 **“只走一遍路”**，大幅提升。

---

## 心得

- **核心技巧**：**滑动窗口 + 单调队列 + 前缀和** 的组合。  
  - 滑动窗口把“合法区间的左边界”快速定位。  
  - 单调队列让我们在 **O(1)** 时间得到窗口内的最大最小值。  
  - 前缀和把区间求和从线性降到常数。

- **适用的题型**（类似思路）  
  1. “子数组最大值最小值差 ≤ K 的最长子段” – 只需要窗口大小，不涉及计数。  
  2. “把数组分成若干段，每段和 ≤ K” – 使用前缀和 + 双指针。  
  3. “统计所有满足 max - min ≤ K 的子数组个数” – 也是滑动窗口 + 单调队列的经典做法。

- **一句话总结解题钥匙**：  
  “把‘合法区间’的左边界锁定，再用前缀和快速累计左边界左侧的 DP 值。”

---

## 反思

- **第一反应**：看到“分段”立即想到 DP，随后想到枚举左端点，导致 `O(n²)`。  
- **最容易踩的坑**  
  1. **下标偏移**：`dp` 与数组下标的对应关系（`dp[i]` 对应前 `i` 个元素）容易混淆。  
  2. **模运算**：`pre[i-1] - pre[left-1]` 可能为负数，记得加上 `MOD` 再取模。  
  3. **单调队列的弹出条件**：左指针移动时，需要检查队首的下标是否已经不在窗口，否则会出现“窗口最大值已经离开却仍被保留”的错误。  
- **下次类似题的第一步**：  
  “先判断能不能用滑动窗口把合法区间的左右边界实时维护”，如果能，再考虑 **单调队列**（最大/最小）和 **前缀和**（区间求和）来把 DP 推到线性。