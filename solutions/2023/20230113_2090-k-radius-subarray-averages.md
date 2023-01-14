# #2090. K 半径子数组平均值 / K Radius Subarray Averages

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/k-radius-subarray-averages/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums of n integers, and an integer k.
The k-radius average for a subarray of nums centered at some index i with the radius k is the average of all elements in nums between the indices i - k and i + k (inclusive). If there are less than k elements before or after the index i, then the k-radius average is -1.
Build and return an array avgs of length n where avgs[i] is the k-radius average for the subarray centered at index i.
The average of x elements is the sum of the x elements divided by x, using integer division. The integer division truncates toward zero, which means losing its fractional part.

**Examples**

**Example 1:**

```
Input: nums = [7,4,3,9,1,8,5,2,6], k = 3
Output: [-1,-1,-1,5,4,4,-1,-1,-1]
Explanation:
- avg[0], avg[1], and avg[2] are -1 because there are less than k elements before each index.
- The sum of the subarray centered at index 3 with radius 3 is: 7 + 4 + 3 + 9 + 1 + 8 + 5 = 37.
  Using integer division, avg[3] = 37 / 7 = 5.
- For the subarray centered at index 4, avg[4] = (4 + 3 + 9 + 1 + 8 + 5 + 2) / 7 = 4.
- For the subarray centered at index 5, avg[5] = (3 + 9 + 1 + 8 + 5 + 2 + 6) / 7 = 4.
- avg[6], avg[7], and avg[8] are -1 because there are less than k elements after each index.
```

**Example 2:**

```
Input: nums = [100000], k = 0
Output: [100000]
Explanation:
- The sum of the subarray centered at index 0 with radius 0 is: 100000.
  avg[0] = 100000 / 1 = 100000.
```

**Example 3:**

```
Input: nums = [8], k = 100000
Output: [-1]
Explanation: 
- avg[0] is -1 because there are less than k elements before and after index 0.
```

**Constraints**

- n == nums.length
- 1 <= n <= 105
- 0 <= nums[i], k <= 105

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`，以及一个整数 `k`。  
以索引 `i` 为中心、半径为 `k` 的子数组（subarray）指的是 `nums` 中从索引 `i - k` 到 `i + k`（含）之间的所有元素。该子数组的 **k 半径平均值** 是这些元素的平均值。  
如果在索引 `i` 的左侧或右侧的元素不足 `k` 个，则该位置的 k 半径平均值为 `-1`。  

构造并返回一个长度为 `n` 的数组 `avgs`，其中 `avgs[i]` 为以索引 `i` 为中心的子数组的 k 半径平均值。  

`x` 个元素的平均值定义为这 `x` 个元素之和除以 `x`，使用整数除法（integer division）。整数除法会向零方向截断，即舍去小数部分。

### 示例

#### 示例 1
```text
Input: nums = [7,4,3,9,1,8,5,2,6], k = 3
Output: [-1,-1,-1,5,4,4,-1,-1,-1]
```
**解释**  
- `avg[0]、avg[1]、avg[2]` 为 `-1`，因为这些位置左侧的元素不足 `k` 个。  
- 以索引 `3` 为中心、半径 `3` 的子数组的和为 `7 + 4 + 3 + 9 + 1 + 8 + 5 = 37`，使用整数除法得到 `avg[3] = 37 / 7 = 5`。  
- 对于以索引 `4` 为中心的子数组，`avg[4] = (4 + 3 + 9 + 1 + 8 + 5 + 2) / 7 = 4`（整数除法结果）。  
- 其余位置同理，超出数组边界的中心位置其平均值为 `-1`。

#### 示例 2
```text
Input: nums = [100000], k = 0
Output: [100000]
```
**解释**  
- 半径为 `0` 时，子数组仅包含自身一个元素。索引 `0` 处的子数组和为 `100000`，`avg[0] = 100000 / 1 = 100000`。

#### 示例 3
```text
Input: nums = [8], k = 100000
Output: [-1]
```
**解释**  
- 索引 `0` 左右均不存在足够的 `k` 个元素，故 `avg[0]` 为 `-1`。

### 约束

- `n == nums.length`
- `1 <= n <= 10^5`
- `0 <= nums[i], k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**对每一个位置 `i` 都去找它左右各 `k` 个元素，求和再取整除**。  
- **遍历**：从左到右依次处理下标 `i`（`0 ≤ i < n`）。  
- **取子数组**：对于当前的 `i`，检查它左边是否还有至少 `k` 个元素、右边是否还有至少 `k` 个元素。如果不满足，答案直接是 `-1`。  
- **求和**：把下标从 `i‑k` 到 `i+k`（共 `2k+1` 个）之间的所有数加起来，用 `sum // (2k+1)` 得到整数平均值。  

> 类比：想象你在图书馆查字典，字典的每一页记录了某个单词的解释。这里的 “子数组” 就像一次要翻阅连续的几页，手动把每页的字数相加再除以页数，就是我们要的平均字数。

**为什么正确**  
只要我们真的把 **所有** 在窗口 `[i‑k, i+k]` 里的元素都加进来，然后除以元素个数（`2k+1`），得到的就是题目定义的“k‑radius 平均”。只要边界检查做对了，答案一定正确。

**时间/空间复杂度**  
- 对每个 `i`（最多 `n` 次）都要遍历 `2k+1` 个元素求和。最坏情况下 `k` 接近 `n/2`，于是每次求和的工作量大约是 `O(n)`，总共是 `O(n·n) = O(n²)`。  
- 只用了几个额外的整型变量（比如 `total`、`ans`），空间是 `O(1)`（不计返回数组）。

> 大白话解释：  
> - `O(n²)` 就像你在一张 `n` 行的表格里，先选一行，再把整行的所有格子都数一遍。行数多，格子多，工作量会迅速“翻倍”。  
> - `O(1)` 表示无论数组多大，你只需要常量几个记事本来记临时数据。

#### 代码（Python）

```python
from typing import List

def getAverages_brute(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    ans = [-1] * n                     # 先全部填 -1，后面再改成真正的平均值
    window = 2 * k + 1                 # 每个合法子数组的长度

    # 遍历每一个中心位置 i
    for i in range(n):
        # 判断左、右是否都有足够的元素
        if i - k < 0 or i + k >= n:
            continue                   # 不满足条件，保持 -1
        total = 0
        # 手动累加 i-k 到 i+k 之间的所有数
        for j in range(i - k, i + k + 1):
            total += nums[j]
        ans[i] = total // window       # 整数除法，自动向 0 截断

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 对每个中心位置都要遍历 `2k+1` 个元素，最坏情况下相当于 `n` × `n` 次加法。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（不计输出数组）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于重复求和**：相邻的窗口大部分元素是相同的，只差进出一个元素。  
我们可以利用 **滑动窗口**（或前缀和）把求和的工作量降到 `O(1)`，从而整体降到 `O(n)`。

**关键观察**  
- 当我们已知窗口 `[i‑k, i+k]` 的和 `S`，下一个中心 `i+1` 对应的窗口是 `[i+1‑k, i+1+k]`。这两个窗口的区别只有左边多了 `nums[i‑k]` 被踢出，右边多了 `nums[i+k+1]` 被加入。  
- 因此 `S_next = S - nums[i‑k] + nums[i+k+1]`，只需要 **常数时间** 就能得到下一个窗口的和。

**实现方式**  
1. **先判断哪些位置合法**：只有当 `i‑k ≥ 0` 且 `i+k < n` 时才需要计算平均值，其余位置直接保留 `-1`。  
2. **初始化第一个合法窗口的和**：从下标 `0` 开始累加前 `2k+1` 个数，得到 `window_sum`。  
3. **遍历所有合法中心**：  
   - 把当前 `window_sum` 除以窗口长度得到平均值，写入答案。  
   - 若还有下一个合法中心，则更新 `window_sum = window_sum - nums[left] + nums[right]`，其中 `left = i‑k`，`right = i+k+1`。  
4. **返回答案数组**。

> 类比：想象你在超市排队结账，收银员每次只需要把前面离开的商品价格减掉、后面新来的商品价格加上，而不必重新把整篮子商品都数一遍。

**为什么使用 64 位整数**  
题目说明 `nums[i]` 和 `k` 都可能达到 `10⁵`，窗口长度最多 `2·10⁵+1`，单个窗口的和最坏可以是 `10⁵ * 10⁵ = 10¹⁰`，超过 32 位整数的范围（约 `2.1×10⁹`），所以要用 Python 的 `int`（本身是大整数）或显式地把累计值放在 `long` 类型（在 C/C++/Java 中需要注意）。

#### 代码（Python）

```python
from typing import List

def getAverages(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    ans = [-1] * n                         # 默认 -1
    window_len = 2 * k + 1                 # 每个合法子数组的长度

    # 如果窗口长度超过数组本身，直接返回全 -1（因为没有任何合法中心）
    if window_len > n:
        return ans

    # 1️⃣ 计算第一个合法窗口的和：下标 0 ~ window_len-1
    window_sum = sum(nums[:window_len])    # Python 的 sum 已经是 O(window_len)

    # 2️⃣ 从左到右遍历所有合法中心 i = k ... n-k-1
    for i in range(k, n - k):
        # 当前窗口的平均值（整数除法）
        ans[i] = window_sum // window_len

        # 若还有下一个窗口，更新窗口和
        if i + k + 1 < n:                  # 右边还有元素可以加入
            # 左边要踢出的元素下标是 i-k
            # 右边要加入的元素下标是 i+k+1
            window_sum = window_sum - nums[i - k] + nums[i + k + 1]

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` ——  
  - 初始求和 `O(window_len)`，但 `window_len ≤ n`。  
  - 之后每次移动窗口只做常数次加减，遍历 `n` 次，总体是线性时间。  
  与暴力解的 `O(n²)` 相比，提升了 **数量级**（从“每个位置都遍历整段”到“每个位置只看进出一个数”）。
- **空间复杂度**：`O(1)`（不计输出数组）——只用了几个整型变量 `window_sum`、`i` 等。

---

## 心得

- **核心技巧**：**滑动窗口**（或等价的前缀和）——通过维护一个“窗口的累计和”，在窗口向右滑动时只做 O(1) 的增删，避免重复计算。  
- **适用题型**  
  1. “固定长度子数组的最大/最小/平均值” 如 *Maximum Average Subarray I/II*。  
  2. “满足某种条件的最短/最长子数组” 如 *Longest Substring Without Repeating Characters*（使用滑动窗口）。  
  3. “子数组和等于目标值” 如 *Subarray Sum Equals K*（利用前缀和+哈希表的思路）。  
- **一句话总结**：**让窗口“只搬进搬出”一个元素，求和从 O(k) 降到 O(1)。**

---

## 反思

- **第一反应**：看到“子数组平均值”，立刻想到“遍历每个中心、把左右 k 个数全部相加”。这就是暴力解的出发点。  
- **最容易踩的坑**  
  - **边界判断**：中心两侧不足 `k` 个元素时必须返回 `-1`，容易忘记把左侧或右侧越界的情况过滤掉。  
  - **窗口长度为 0**（即 `k = 0`）时，窗口只有一个元素，代码仍需正常工作。  
  - **整数溢出**：在语言层面需要使用 64 位整数来保存窗口和，Python 自带大整数，但在 C/C++/Java 中必须显式使用 `long`/`long long`。  
- **下次思路**：看到“子数组的和/平均/最大/最小”这类描述，第一步就**检查是否可以用滑动窗口或前缀和**把重复计算削减到常数时间，再决定具体实现方式。