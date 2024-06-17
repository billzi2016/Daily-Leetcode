# #2735. 收集巧克力 / Collecting Chocolates

> 难度：中等 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/collecting-chocolates/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of size n representing the cost of collecting different chocolates. The cost of collecting the chocolate at the index i is nums[i]. Each chocolate is of a different type, and initially, the chocolate at the index i is of ith type.
In one operation, you can do the following with an incurred cost of x:
Return the minimum cost to collect chocolates of all types, given that you can perform as many operations as you would like.

**Examples**

**Example 1:**

```
Input: nums = [20,1,15], x = 5
Output: 13
Explanation: Initially, the chocolate types are [0,1,2]. We will buy the 1st type of chocolate at a cost of 1.
Now, we will perform the operation at a cost of 5, and the types of chocolates will become [1,2,0]. We will buy the 2nd type of chocolate at a cost of 1.
Now, we will again perform the operation at a cost of 5, and the chocolate types will become [2,0,1]. We will buy the 0th type of chocolate at a cost of 1. 
Thus, the total cost will become (1 + 5 + 1 + 5 + 1) = 13. We can prove that this is optimal.
```

**Example 2:**

```
Input: nums = [1,2,3], x = 4
Output: 6
Explanation: We will collect all three types of chocolates at their own price without performing any operations. Therefore, the total cost is 1 + 2 + 3 = 6.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 109
- 1 <= x <= 109

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 `nums`（长度为 `n`），其中 `nums[i]` 表示收集下标 `i` 处巧克力的费用。每种巧克力的类型互不相同，初始时下标 `i` 位置的巧克力属于第 `i` 种类型。

在一次 **操作（operation）** 中，你可以以费用 `x` 执行以下行为：

（题目原文此处缺失具体操作描述）

返回在可以任意次数执行上述操作的前提下，收集所有类型巧克力的最小总费用。

---

### 示例

#### 示例 1
``` 
Input: nums = [20,1,15], x = 5
Output: 13
```
**解释**：最初巧克力的类型为 `[0,1,2]`。我们以费用 `1` 购买第 `1` 种巧克力。  
随后以费用 `5` 执行一次操作，巧克力的类型变为 `[1,2,0]`。我们再以费用 `1` 购买第 `2` 种巧克力。  
再次以费用 `5` 执行操作，巧克力的类型继续循环……（此处示例已截断），最终的最小总费用为 `13`。

#### 示例 2
``` 
Input: nums = [1,2,3], x = 4
Output: 6
```
**解释**：我们直接按各自的价格购买三种巧克力，无需进行任何操作。总费用为 `1 + 2 + 3 = 6`。

---

### 约束条件
- `1 <= nums.length <= 1000`
- `1 <= nums[i] <= 10^9`
- `1 <= x <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **把题目想成“转盘”**  
   - `nums` 是固定不动的费用表，像一本字典，`nums[i]` 就是第 *i* 页的价格。  
   - 初始时第 *i* 种巧克力对应第 *i* 页（下标 `i`）。  
   - **一次操作**相当于把整个转盘左转一格，所有巧克力的类型整体左移一位，转盘本身不动，仍然是同一本字典。左转一次要付 `x` 元。  

2. **什么时候买哪种巧克力**  
   - 假设我们已经左转了 `r` 次（`0 ≤ r ≤ n‑1`），第 `i` 种巧克力现在位于下标 `(i‑r) mod n`，买它的花费就是 `nums[(i‑r) mod n]`。  
   - 如果我们决定 **总共** 左转 `K` 次（`K` 次操作的费用是 `K·x`），那么在这 `K` 次转动期间，每种巧克力都可以在 **0、1、2 … K** 次转动后的任意时刻购买。  
   - 对第 `i` 种巧克力来说，最便宜的买入时机就是在这 `K+1` 个位置中取最小值：  

\[
\text{cost}_i(K)=\min_{0\le r\le K} \; nums[(i-r)\bmod n]
\]

   - 最终的总费用 = `K·x + Σ cost_i(K)`。

3. **为什么暴力能得到正确答案**  
   - 我们枚举 **所有可能的总转动次数 `K`**（最多转 `n‑1` 次就会回到原点，转更多只会额外付费没有任何好处），对每个 `K` 逐个检查每种巧克力在 `0…K` 次转动后的所有费用，取最小即可。  
   - 只要把所有 `K` 的结果取最小，就一定能得到全局最优解。

4. **时间/空间复杂度的大白话**  
   - 暴力实现会三层循环：外层遍历 `K`（最多 `n` 次），中层遍历每种巧克力 `i`（`n` 次），内层遍历所有可能的转动次数 `r`（最多 `n` 次）。  
   - 时间复杂度是 **O(n³)**，如果 `n = 1000`，大约会进行 `10⁹` 次比较，运行会很慢。  
   - 只用到原数组和几个计数变量，空间复杂度是 **O(1)**（常数级），也就是几乎不占额外内存。

#### 代码（Python）

```python
from typing import List

def minCost_bruteforce(nums: List[int], x: int) -> int:
    n = len(nums)
    ans = float('inf')                     # 最小答案，先设为无穷大

    # 枚举总共要转动多少次 K（0~n-1）
    for K in range(n):
        total = K * x                       # K 次操作的费用
        # 对每一种巧克力 i，找在 0~K 次转动后的最小购买费用
        for i in range(n):
            best = float('inf')
            for r in range(K + 1):          # r 表示已经转了 r 次再买
                idx = (i - r) % n           # 现在它在 nums 的哪个下标
                best = min(best, nums[idx])
            total += best
        ans = min(ans, total)               # 取所有 K 中的最小值
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)` —— 三层循环，每层最多 `n` 次。  
  - “O(n³)” 可以理解为：如果 `n` 是 10，程序会做大约 `10³ = 1000` 次基本操作；`n` 越大，次数会以立方方式快速增长。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

1. **从暴力找瓶颈**  
   - 暴力的 **内层循环**（遍历 `r = 0…K`）是最耗时的，因为对每个 `i` 都要重新比较 `K+1` 次。  
   - 只要能 **在 O(1) 时间内得到 `min_{0≤r≤K} nums[(i-r) mod n]`**，整体复杂度就会从 `O(n³)` 降到 `O(n²)`（外层 `K` + 中层 `i`）。

2. **利用“前缀最小”**  
   - 对固定的 `K`，我们要的其实是 **以 i 为中心、向左最多 K 步的最小值**。  
   - 想象把数组 `nums` 再复制一遍拼成 `nums2 = nums + nums`（长度 `2n`），这样左移 `K` 步后仍然可以在 `nums2` 中直接取到对应位置，且不需要手写模运算。  

3. **滚动维护最小值**  
   - 当我们从左到右遍历 `i = 0 … n‑1` 时，窗口 `[i‑K, i]`（在 `nums2` 中）正好是 “第 i 种巧克力可以出现的所有位置”。  
   - 用 **单调队列（Monotonic Queue）** 可以在 **O(1) 均摊时间** 内维护窗口的最小值：  
     - 队列里保存的是下标，保证对应的 `nums2` 值单调递增（队首永远是最小值）。  
     - 每移动一步，就把新进来的下标加入队列，弹出已经离开窗口的下标。  

4. **遍历所有可能的 K**  
   - `K` 的取值范围只有 `0 … n‑1`（转 `n` 次会回到原点，继续转只会额外付费），所以我们 **枚举 K**。  
   - 对每个 `K` 用单调队列一次遍历求出所有 `i` 的最小购买费用，累计得到 `total = K·x + Σ minCost_i`。  
   - 记录所有 `K` 中的最小 `total` 即为答案。

5. **时间复杂度从 O(n³) 降到 O(n²)**  
   - 外层 `K` 循环 `n` 次。  
   - 对每个 `K`，单调队列遍历 `2n`（实际上只需要 `n`）元素，摊销后是 **O(n)**。  
   - 所以总体是 `O(n·n) = O(n²)`，对 `n ≤ 1000` 完全绰绰有余。  

6. **空间复杂度**  
   - 需要额外的 `2n` 长度的数组 `nums2`（复制一次）和一个单调队列，都是 **O(n)** 级别。

> **类比**：单调队列就像排队买咖啡的人，只保留“更便宜的”在前面，排在后面更贵的会被“踢出队列”，这样队首永远是当前窗口里最便宜的那杯咖啡。

#### 代码（Python）

```python
from collections import deque
from typing import List

def minCost_optimal(nums: List[int], x: int) -> int:
    n = len(nums)
    # 为了处理循环，复制一遍
    nums2 = nums + nums          # 长度 2n
    ans = float('inf')

    # 枚举总共要转动多少次 K（0~n-1）
    for K in range(n):
        # 单调队列，存下标，保证对应的 nums2 值单调递增
        dq = deque()
        total = K * x            # K 次操作的费用

        # 先把第 0~K 的窗口放进队列（对应 i = 0 的可选位置）
        for idx in range(K + 1):
            while dq and nums2[dq[-1]] >= nums2[idx]:
                dq.pop()
            dq.append(idx)

        # 现在遍历每一种巧克力 i = 0 … n-1
        for i in range(n):
            # 队首就是窗口 [i-K, i]（在 nums2 中）的最小值
            total += nums2[dq[0]]

            # 窗口右边界往右移动一格：加入下标 i+K+1
            nxt = i + K + 1
            if nxt < 2 * n:                     # 防止越界（其实永远不会越界）
                while dq and nums2[dq[-1]] >= nums2[nxt]:
                    dq.pop()
                dq.append(nxt)

            # 窗口左边界离开：下标 i-K
            left = i - K
            if dq and dq[0] == left:
                dq.popleft()

        ans = min(ans, total)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “O(n²)” 可以理解为：如果 `n = 100`，程序大约会做 `100 × 100 = 10,000` 次核心操作；`n` 翻倍，次数会增长到原来的四倍。相较于 `O(n³)`（立方增长），这里的增长要慢得多。  
  - 与暴力解相比，我们把 **每种巧克力的最小费用** 的寻找从 `K` 次比较压缩到 **常数时间**（单调队列的摊销 O(1)），于是整体快了约 `n` 倍。  

- **空间复杂度**：`O(n)`  
  - 需要存 `2n` 长度的 `nums2`（相当于原数组的两倍）以及单调队列，都是线性空间，和 `n` 成正比。  

---

## 心得  

- **核心技巧**：把“转动”看成“循环左移”，并把**所有可能的转动次数**抽象为一个参数 `K`，再用 **单调队列** 在 O(1) 均摊时间内得到窗口最小值。  
- **适用的题型**：  
  1. 需要在 **循环数组** 中找 **固定长度窗口最小值**（如 “Maximum Sum Circular Subarray” 的变体）。  
  2. “一次操作会整体左移/右移” 的问题，尤其是 **费用随位置变化** 的情形（如 “Rotate Function”）。  
- **一句话总结解题钥匙**：**把所有可能的旋转次数枚举出来，然后用单调队列把每种巧克力在该旋转范围内的最小购买费用快速算出来**。

---

## 反思  

- **拿到题目第一反应**：先把转盘想成“每转一次，所有类型都左移一格”，于是想到 **枚举转多少次**，然后逐个计算每种巧克力的最小费用。  
- **最容易踩的坑**  
  1. **循环取模** 写错：`(i - r) % n` 必须放在正确的位置，否则会出现负下标错误。  
  2. **转动次数上界**：忽略了转 `n` 次会回到原点，导致不必要的循环。  
  3. **单调队列的窗口边界**：左边界离开时要记得弹出对应的下标，否则最小值会被“过期”。  
- **下次遇到同类题，第一步该想到**：把“整体移动”抽象为 **参数化的循环左/右移**，并考虑 **枚举移动次数 + 滑动窗口最小值**（单调队列或前缀最小）来降低复杂度。