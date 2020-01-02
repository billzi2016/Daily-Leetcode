# #718. 最大重复子数组的最大长度 / Maximum Length of Repeated Subarray

> 难度：中等 · 标签：Array、Binary Search、Dynamic Programming、Sliding Window、Rolling Hash、Hash Function · [LeetCode 链接](https://leetcode.com/problems/maximum-length-of-repeated-subarray/)

---

## 题目（英文原版）

**Description**

Given two integer arrays nums1 and nums2, return the maximum length of a subarray that appears in both arrays.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
Output: 3
Explanation: The repeated subarray with maximum length is [3,2,1].
```

**Example 2:**

```
Input: nums1 = [0,0,0,0,0], nums2 = [0,0,0,0,0]
Output: 5
Explanation: The repeated subarray with maximum length is [0,0,0,0,0].
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 100

---

## 题目（中文翻译）

给定两个整数数组 `nums1` 和 `nums2`，返回同时出现在两个数组中的子数组（subarray）的最大长度。

**约束条件**

- `1 <= nums1.length, nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 10^9`

**示例**

**示例 1**

```
Input: nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
Output: 3
Explanation: 最大长度的重复子数组是 [3,2,1]。
```

**示例 2**

```
Input: nums1 = [0,0,0,0,0], nums2 = [0,0,0,0,0]
Output: 5
Explanation: 最大长度的重复子数组是 [0,0,0,0,0]。
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把 `nums1` 中的每一个子数组（连续片段）都拿出来，去 `nums2` 里找有没有完全一样的子数组，找到的最长长度就是答案。

- **数据结构**：这里我们只用普通的 **列表**（list），因为子数组本身就是列表的切片。  
- **生活化类比**：把 `nums1` 看成一本书的文字序列，`nums2` 是另一本书。我们把第一本书的每一段文字（子数组）抄下来，去第二本书里逐字逐句比对，看看能不能找到完全相同的段落。  
- **正确性**：只要遍历了所有可能的子数组，并且每个子数组都在另一数组里检查了一遍，就一定不会漏掉最长的公共子数组，所以答案一定会被找到。

#### 代码（Python）

```python
def findLength_brute(nums1, nums2):
    n, m = len(nums1), len(nums2)
    max_len = 0                     # 记录目前找到的最长公共子数组长度

    # i 为 nums1 的起始下标，j 为子数组的长度
    for i in range(n):
        for length in range(1, n - i + 1):   # 所有可能的子数组长度
            sub = nums1[i:i + length]       # 取出子数组，类似“抄下来”

            # 在 nums2 中逐个位置尝试匹配
            for k in range(m - length + 1):
                if sub == nums2[k:k + length]:
                    max_len = max(max_len, length)
                    break   # 已找到相同的子数组，后面更长的已经不可能在这里出现

    return max_len
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两层循环枚举 `i`（起点）和 `length`（长度），共 `≈ n²/2` 次。  
  - 内层再遍历 `nums2` 的所有可能起点，最坏情况是 `≈ m` 次。  
  - 所以总体是 `n² * m`，在最坏情况下 `n ≈ m`，即 `O(n³)`。  
  - **大白话**：如果数组长度是 1000，粗略想象就是 1000 × 1000 × 1000 ≈ 10⁹ 次比较，电脑跑不动。

- **空间复杂度**：`O(1)`（不计输入本身）  
  - 只用了常数个临时变量和一个切片 `sub`（Python 切片会创建新列表，但长度最多是 `n`，不随循环次数增长）。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **重复比较相同的前缀**。  
比如 `nums1[i:]` 和 `nums2[j:]` 的前 `k` 个元素相等，我们在后面再比较 `i+1` 与 `j+1` 时，又会重新把这 `k-1` 个元素一次遍历。

**动态规划** 正好可以把“已经算好的”信息保存下来，避免重复工作。

1. 定义 `dp[i][j]` 为 **从 `nums1[i]` 开始、从 `nums2[j]` 开始** 的最长公共前缀长度。  
   - 如果 `nums1[i] == nums2[j]`，那么 `dp[i][j] = 1 + dp[i+1][j+1]`（因为后面还能继续匹配）。  
   - 否则 `dp[i][j] = 0`（当前位置不相等，前缀长度为 0）。

2. 为了让 `dp[i+1][j+1]` 已经算好，我们从后往前遍历两个数组。  
   - 设 `i` 从 `n-1` 到 `0`，`j` 从 `m-1` 到 `0`。  
   - 这样在计算 `dp[i][j]` 时，`dp[i+1][j+1]` 已经是已知值。

3. 在遍历的过程中维护一个全局最大值 `ans`，即所有 `dp[i][j]` 中的最大者。

**为什么是最优**：每对 `(i, j)` 只算一次，时间是 `O(n·m)`，空间可以压缩到 `O(min(n,m))`（只保留上一行），满足题目给出的 1000 规模。

#### 代码（Python）

```python
def findLength(nums1, nums2):
    n, m = len(nums1), len(nums2)

    # 为了节省空间，只保留上一行 dp（即 i+1 那一行）
    # dp_next[j] 对应 dp[i+1][j]，dp_cur[j] 对应 dp[i][j]
    dp_next = [0] * (m + 1)   # 多开一个位置，防止越界
    ans = 0

    # 从后往前遍历 nums1
    for i in range(n - 1, -1, -1):
        dp_cur = [0] * (m + 1)   # 当前行的 dp 表
        # 从后往前遍历 nums2
        for j in range(m - 1, -1, -1):
            if nums1[i] == nums2[j]:
                dp_cur[j] = 1 + dp_next[j + 1]   # 对应 dp[i][j] = 1 + dp[i+1][j+1]
                ans = max(ans, dp_cur[j])        # 更新全局最大值
            # else: dp_cur[j] 本来就是 0，保持不变
        dp_next = dp_cur   # 当前行 becomes 下一轮的 “上一行”

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - 只遍历了 `n × m` 次双层循环，每次都是常数操作。  
  - **大白话**：如果两个数组都是 1000 长，只有约 1,000,000 次比较，电脑几毫秒就能完成。

- **空间复杂度**：`O(m)`（或 `O(min(n,m))`）  
  - 只用了两行长度为 `m+1` 的数组来存放 DP 值，远小于 `n·m` 的二维表。  
  - 如果把较短的数组设为 `m`，则空间是最小的。

---

## 心得

- **核心技巧**：利用 **动态规划** 把“公共前缀长度”递推下来，避免重复比较。  
- **适用题型**：  
  1. “最长公共子序列（LCS）”的变形（这里要求子数组/连续）  
  2. “编辑距离”中涉及前缀匹配的 DP  
  3. “最大正方形”或“最大矩形”这类二维 DP，思路相似：把局部最优扩展到全局。  
- **一句话总结**：把“从当前位置往后还能匹配多长”记下来，往前推时只加一。

---

## 反思

- **第一反应**：直接暴力枚举所有子数组，代码写得很快，但忽略了时间限制。  
- **最容易踩的坑**：  
  - **下标越界**：`dp[i+1][j+1]` 在最底层需要额外的 “哨兵” 行/列（上面代码里多开了一个位置）。  
  - **空间误用**：直接创建 `n×m` 的二维表会超出内存，尤其在语言默认二维数组占用大时。  
  - **忘记更新全局最大值**：只算 DP 表而不记录最大会得到错误答案。  
- **下次第一步**：先思考“有没有可以递推的子问题”，如果可以，用 DP 把子问题的答案保存下来，避免重复计算。