# #2321. 拼接数组的最大得分 / Maximum Score Of Spliced Array

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximum-score-of-spliced-array/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2, both of length n.
You can choose two integers left and right where 0 <= left <= right < n and swap the subarray nums1[left...right] with the subarray nums2[left...right].
You may choose to apply the mentioned operation once or not do anything.
The score of the arrays is the maximum of sum(nums1) and sum(nums2), where sum(arr) is the sum of all the elements in the array arr.
Return the maximum possible score.
A subarray is a contiguous sequence of elements within an array. arr[left...right] denotes the subarray that contains the elements of nums between indices left and right (inclusive).

**Examples**

**Example 1:**

```
Input: nums1 = [60,60,60], nums2 = [10,90,10]
Output: 210
Explanation: Choosing left = 1 and right = 1, we have nums1 = [60,90,60] and nums2 = [10,60,10].
The score is max(sum(nums1), sum(nums2)) = max(210, 80) = 210.
```

**Example 2:**

```
Input: nums1 = [20,40,20,70,30], nums2 = [50,20,50,40,20]
Output: 220
Explanation: Choosing left = 3, right = 4, we have nums1 = [20,40,20,40,20] and nums2 = [50,20,50,70,30].
The score is max(sum(nums1), sum(nums2)) = max(140, 220) = 220.
```

**Example 3:**

```
Input: nums1 = [7,11,13], nums2 = [1,1,1]
Output: 31
Explanation: We choose not to swap any subarray.
The score is max(sum(nums1), sum(nums2)) = max(31, 3) = 31.
```

**Constraints**

- n == nums1.length == nums2.length
- 1 <= n <= 105
- 1 <= nums1[i], nums2[i] <= 104

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的整数数组 `nums1` 和 `nums2`，两者长度均为 `n`。  
你可以选择两个整数 `left` 和 `right`，满足 `0 <= left <= right < n`，将子数组 `nums1[left...right]` 与子数组 `nums2[left...right]` 互换。  
此操作可以执行 **一次**，也可以不执行。  

数组的得分定义为 `sum(nums1)` 与 `sum(nums2)` 的最大值，其中 `sum(arr)` 表示数组 `arr` 中所有元素的和。  
返回能够得到的 **最大可能得分**。  

子数组（subarray）是数组中连续的元素序列。`arr[left...right]` 表示包含下标 `left` 到 `right`（含）之间所有元素的子数组。

## 示例

### 示例 1
**输入**  
`nums1 = [60,60,60]`  
`nums2 = [10,90,10]`  

**输出**  
`210`

**解释**  
选择 `left = 1`、`right = 1`，则交换后得到 `nums1 = [60,90,60]`、`nums2 = [10,60,10]`。  
得分为 `max(sum(nums1), sum(nums2)) = max(210, 80) = 210`。

### 示例 2
**输入**  
`nums1 = [20,40,20,70,30]`  
`nums2 = [50,20,50,40,20]`  

**输出**  
`220`

**解释**  
选择 `left = 3`、`right = 4`，交换后得到 `nums1 = [20,40,20,40,20]`、`nums2 = [50,20,50,70,30]`。  
得分为 `max(sum(nums1), sum(nums2)) = max(140, 220) = 220`。

### 示例 3
**输入**  
`nums1 = [7,11,13]`  
`nums2 = [1,1,1]`  

**输出**  
`31`

**解释**  
不进行任何子数组交换。  
得分为 `max(sum(nums1), sum(nums2)) = max(31, 3) = 31`。

## 约束条件
- `n == nums1.length == nums2.length`
- `1 <= n <= 10^5`
- `1 <= nums1[i], nums2[i] <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **遍历所有可能的左端点 `left`**（从 `0` 到 `n‑1`）。  
2. 对每个 `left` 再**遍历所有可能的右端点 `right`**（`left ≤ right < n`）。  
3. 把 `nums1[left…right]` 与 `nums2[left…right]` 交换，**重新计算两数组的和**，取两者的最大值作为这一次操作的得分。  
4. 把所有得分取最大，即为答案。  

> **数据结构类比**：  
> - 我们把两个数组想象成两本笔记本，每页上有一个数字。  
> - “子数组”就像把连续的几页纸（左到右）一次性抽出来换到另一册里。  
> - 交换后我们只需要把两本笔记本里所有页数相加，看看哪本的总分更高。

**为什么能得到正确答案**：  
因为我们把**所有**合法的交换区间都尝试了一遍，必然会覆盖最优的那一次（或者根本不换）。

**时间/空间复杂度**  
- 外层 `left` 循环 `n` 次，内层 `right` 最多也是 `n` 次，**总共 O(n²)** 次尝试。  
- 每次交换后我们重新遍历数组求和，若直接累加会再是 O(n)；但我们可以在遍历 `right` 时**增量更新**子数组的和，使每次尝试只 O(1)。整体仍是 **O(n²)**。  
- 只用了几个整数变量保存临时和，**空间 O(1)**（常数级）。

> **大白话解释**：  
> O(n²) 就像在 1000 本书里找两本相邻的书，需要检查 1000×1000≈100 万次；如果 n=10⁵，次数就会变成 10⁰¹⁰，根本算不完。

#### 代码（Python）

```python
def maximumScoreBrute(nums1, nums2):
    n = len(nums1)
    sum1 = sum(nums1)            # 原始 sum(nums1)
    sum2 = sum(nums2)            # 原始 sum(nums2)
    best = max(sum1, sum2)       # 不交换时的得分

    # 为了增量更新子数组和，预先计算两数组的前缀和
    # pre1[i] = nums1[0] + ... + nums1[i-1]（长度为 i）
    pre1 = [0] * (n + 1)
    pre2 = [0] * (n + 1)
    for i in range(n):
        pre1[i + 1] = pre1[i] + nums1[i]
        pre2[i + 1] = pre2[i] + nums2[i]

    # 枚举所有子数组 [l, r]
    for l in range(n):
        for r in range(l, n):
            # 子数组在两个数组中的和
            seg1 = pre1[r + 1] - pre1[l]   # nums1[l..r] 的和
            seg2 = pre2[r + 1] - pre2[l]   # nums2[l..r] 的和

            # 交换后两数组的和
            new_sum1 = sum1 - seg1 + seg2
            new_sum2 = sum2 - seg2 + seg1

            # 记录当前得分的最大值
            best = max(best, new_sum1, new_sum2)

    return best
```

> 关键行解释  
> - `pre1` / `pre2`：前缀和相当于“累计字典”，让我们可以 **O(1)** 取任意子数组的总和。  
> - `seg1` / `seg2`：利用前缀和快速算出左、右端点之间的和。  
> - `new_sum1` / `new_sum2`：交换后两数组的新总分。  

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 需要检查每一对 `(left, right)`。  
- **空间复杂度**：`O(n)` —— 前缀和数组占用了线性空间（如果不使用前缀和，只用常数空间，则每次重新遍历子数组会导致 `O(n³)`，显然更慢）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**遍历所有区间**。  
观察交换后的总分公式：

```
new_sum1 = S1 - sum1[l..r] + sum2[l..r]
new_sum2 = S2 - sum2[l..r] + sum1[l..r]
```

其中 `S1 = sum(nums1)`，`S2 = sum(nums2)` 为原始总和。  
把两式分别改写：

```
new_sum1 = S1 + ( sum2[l..r] - sum1[l..r] )
new_sum2 = S2 + ( sum1[l..r] - sum2[l..r] )
```

> **核心发现**：  
> - 对于 `nums1`，我们只关心 **“在某段区间内，nums2 的和比 nums1 多多少”**。  
> - 这正是一个**差值数组**的子数组和：`diff[i] = nums2[i] - nums1[i]`。  
> - 如果我们能找到 `diff` 的**最大子数组和** `gain1`，那么把对应区间交换后，`nums1` 的总和最大能提升 `gain1`。  
> - 同理，把 `diff` 取负得到 `-diff[i] = nums1[i] - nums2[i]`，其最大子数组和 `gain2` 表示 `nums2` 能提升的幅度。

于是答案只需要比较四个可能：

```
ans = max( S1,                     # 不换，直接看 nums1
           S2,                     # 不换，直接看 nums2
           S1 + gain1,             # 把 nums1 提升到最大
           S2 + gain2 )            # 把 nums2 提升到最大
```

> **为什么只要最大子数组和**？  
> 因为我们只能交换 **一次** 连续子数组。把差值数组中和最大的那段选出来，正好让对应的原数组获得最大的“增益”。如果所有增益都是负的，说明交换只会让两边更差，此时我们**可以选择不交换**（对应 `gain = 0`）。

**如何求最大子数组和**  
这正是**Kadane 算法**的典型场景：一次遍历，维护当前子数组的和 `cur` 与历史最大值 `best`。  
伪代码：

```
cur = best = 0
for x in diff:
    cur = max(0, cur + x)   # 若累计变负，则从下一位重新开始
    best = max(best, cur)
```

这里把负数直接丢掉（相当于“不选任何子数组”），所以 `best` 永远 ≥ 0。

> **类比**：  
> 把 `diff` 看成一条山路，`x` 是每一步的高低起伏。我们想找 **最高的连续上坡段**，如果一路往下走（累计和为负），就直接回到山脚重新开始。最高的上坡段的海拔就是 `gain`。

#### 代码（Python）

```python
def maximumScore(nums1, nums2):
    """
    O(n) 时间、O(1) 额外空间的最优解
    """
    n = len(nums1)
    sum1 = sum(nums1)          # 原始 sum(nums1)
    sum2 = sum(nums2)          # 原始 sum(nums2)

    # 计算 diff = nums2 - nums1 以及它的最大子数组和 (gain1)
    cur = best1 = 0
    for i in range(n):
        diff = nums2[i] - nums1[i]
        cur = max(0, cur + diff)   # 若累计为负则重新开始
        best1 = max(best1, cur)    # 记录目前为止的最大增益

    # 计算 -diff = nums1 - nums2 的最大子数组和 (gain2)
    cur = best2 = 0
    for i in range(n):
        diff = nums1[i] - nums2[i]
        cur = max(0, cur + diff)
        best2 = max(best2, cur)

    # 四个候选答案取最大
    return max(sum1, sum2, sum1 + best1, sum2 + best2)
```

> 关键行中文注释  
> - `diff = nums2[i] - nums1[i]`：构造差值数组的当前元素。  
> - `cur = max(0, cur + diff)`：如果把当前元素加进去导致累计和变负，就把累计和清零（相当于“不选子数组”）。  
> - `best1 = max(best1, cur)`：保存迄今为止看到的最大增益。  
> - 同理第二遍循环求 `best2`（其实只需要一次循环求两者的最大值，但为保持思路清晰这里分开写）。

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历两次数组（实际上一次遍历就能算出两种增益），线性规模。  
  > 与暴力 `O(n²)` 对比：如果 `n = 10⁵`，暴力需要约 `10¹⁰` 次操作根本跑不完，最优解只需要 `10⁵` 次，几乎瞬间完成。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（累计和、最大值），不随 `n` 增长。

---

## 心得  

- **核心技巧**：把“交换子数组后得到的增益”转化为**差值数组的最大子数组和**，利用 Kadane 算法在线性时间求解。  
- **适用场景**  
  1. **最大子数组差值** 类似题目：  
     - *Maximum Subarray Sum After One Modification*（一次修改后最大子数组和）  
  2. **只能操作一次的区间问题**：  
     - *Maximum Subarray Sum with One Deletion*（一次删除后最大子数组和）  
  3. **两个数组的局部替换**：  
     - *Maximum Score From Removing Subarrays*（删除子数组后得分最大）  

- **一句话总结解题钥匙**：  
  “把一次区间交换的收益抽象成差值数组的子段和，最大收益即差值数组的最大子段和”。  

---

## 反思  

- **第一反应**：看到“交换子数组一次”，我第一时间想到“枚举所有区间”。这自然导致暴力 `O(n²)` 思路。  
- **最容易踩的坑**  
  1. **忘记“可以不交换”**：增益可能为负，需要把最大子数组和下限设为 0。  
  2. **边界条件**：当 `n = 1` 时，子数组只能是整个数组；Kadane 仍然适用。  
  3. **整数溢出**（在 Python 不会，但在 C/C++/Java 需要注意使用 `long`）。  
- **下次遇到同类题**，第一步应该：  
  “把‘一次区间操作的效果’写成原始总和 + 区间增益的形式，随后把增益抽象为差值数组的子段和”，再用 Kadane/单调栈等线性技巧求最优增益。