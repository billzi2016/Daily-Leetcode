# #1526. 子数组递增形成目标数组的最少操作次数 / Minimum Number of Increments on Subarrays to Form a Target Array

> 难度：困难 · 标签：Array、Dynamic Programming、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/)

---

## 题目（英文原版）

**Description**

You are given an integer array target. You have an integer array initial of the same size as target with all elements initially zeros.
In one operation you can choose any subarray from initial and increment each value by one.
Return the minimum number of operations to form a target array from initial.
The test cases are generated so that the answer fits in a 32-bit integer.

**Examples**

**Example 1:**

```
Input: target = [1,2,3,2,1]
Output: 3
Explanation: We need at least 3 operations to form the target array from the initial array.
[0,0,0,0,0] increment 1 from index 0 to 4 (inclusive).
[1,1,1,1,1] increment 1 from index 1 to 3 (inclusive).
[1,2,2,2,1] increment 1 at index 2.
[1,2,3,2,1] target array is formed.
```

**Example 2:**

```
Input: target = [3,1,1,2]
Output: 4
Explanation: [0,0,0,0] -> [1,1,1,1] -> [1,1,1,2] -> [2,1,1,2] -> [3,1,1,2]
```

**Example 3:**

```
Input: target = [3,1,5,4,2]
Output: 7
Explanation: [0,0,0,0,0] -> [1,1,1,1,1] -> [2,1,1,1,1] -> [3,1,1,1,1] -> [3,1,2,2,2] -> [3,1,3,3,2] -> [3,1,4,4,2] -> [3,1,5,4,2].
```

**Constraints**

- 1 <= target.length <= 105
- 1 <= target[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `target`。另有一个大小相同、初始全部为 `0` 的整数数组 `initial`。  
在一次操作中，你可以选择 `initial` 中的任意子数组（subarray），将该子数组内的每个元素都增加 `1`。  
返回将 `initial` 变为 `target` 所需的最少操作次数。  
题目保证答案能够放入 32 位整数。

**示例**

**示例 1**  
```
Input: target = [1,2,3,2,1]
Output: 3
Explanation: 至少需要 3 次操作才能从初始数组得到目标数组。
[0,0,0,0,0] → 在索引 0~4（含）区间递增 1 → [1,1,1,1,1]
[1,1,1,1,1] → 在索引 1~3（含）区间递增 1 → [1,2,2,2,1]
[1,2,2,2,1] → 在索引 2 处递增 1 → [1,2,3,2,1]
```

**示例 2**  
```
Input: target = [3,1,1,2]
Output: 4
Explanation: 操作过程如下：
[0,0,0,0] → [1,1,1,1] → [1,1,1,2] → [2,1,1,2] → [3,1,1,2]
```

**示例 3**  
```
Input: target = [3,1,5,4,2]
Output: 7
Explanation: 操作过程如下：
[0,0,0,0,0] → [1,1,1,1,1] → [2,1,1,1,1] → [3,1,1,1,1] → 
[3,1,2,2,2] → [3,1,3,3,2] → [3,1,4,4,2] → [3,1,5,4,2]
```

**约束条件**  
- `1 <= target.length <= 10^5`  
- `1 <= target[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**每次只选取一个位置**（子数组长度为 1），把它的值从 0 增加到目标值 `target[i]`。  
这相当于把每个格子单独“灌水”。  
- **数据结构**：只需要一个普通的列表 `target`，不需要额外的结构。  
- **为什么正确**：因为题目允许任意子数组，我们完全可以把子数组选成长度 1 的那种；这样每次增 1 只影响一个格子，最终每个格子都会恰好被增 `target[i]` 次，必然能得到目标数组。  
- **时间/空间复杂度**：  
  - 时间上我们要对每个格子执行 `target[i]` 次增操作，最坏情况是所有 `target[i]` 都是 `10⁵`，于是总操作次数是 `Σ target[i]`，在最坏情况下接近 `10⁵ × 10⁵ = 10¹⁰`，显然太慢。  
  - 空间上只用了原数组本身，额外空间是 **O(1)**。  

> **大白话**：`O(n²)` 中的 `n` 代表规模（这里是数组长度），`O(n²)` 就像两层循环每层走 `n` 步，整体要走 `n×n` 步。我们的暴力解相当于 **每个格子要走 `target[i]` 步**，如果 `target[i]` 也和 `n` 同阶，那就是 `O(n·target_max)`，和 `O(n²)` 差不多。

#### 代码（Python）

```python
def minNumberOperations_bruteforce(target):
    """
    暴力模拟：每次只增一个位置的子数组（长度为 1）。
    直接返回所需的操作次数——即所有元素的和。
    """
    ops = 0
    for v in target:          # 遍历每个格子
        ops += v              # 需要 v 次单独增 1 的操作
    return ops
```

#### 复杂度  

- **时间复杂度**：`O( Σ target[i] )`，在最坏情况下约等于 `O(n·target_max)`，会超时。  
- **空间复杂度**：`O(1)`，只用了常数级额外空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到：**每一次增 1 都是“在某个区间里把所有格子一起抬高”。**  
如果我们把区间抬高到 **该区间最小值**，则已经满足了该区间里所有格子至少需要的那一层。  
于是我们可以把整个过程想成 **层层堆叠**：  

1. 先把整个数组整体抬高到最小的那个值 `min(target)`（一次操作覆盖全数组）。  
2. 把数组划分成若干 **更高的子段**（因为某些位置比最小值高），在每个子段里继续重复上述过程。  

这是一种 **分治** 思路，时间会是 `O(n log n)`（因为每层都要找区间最小值）。  

不过还有更简洁的观察：  
- 看左到右的相邻两个位置 `target[i-1]` 与 `target[i]`。  
- 如果 `target[i]` **不低于** 前一个，则前面已经抬到 `target[i-1]`，要再让第 `i` 位达到 `target[i]`，只能 **额外** 再抬高 `target[i] - target[i-1]` 次，且这几次可以把从 `i` 开始的后面一段一起抬高（即选子数组 `[i, …]`）。  
- 如果 `target[i]` **低于** 前一个，则不需要额外操作——因为在抬高前面的过程中，已经把第 `i` 位抬到了至少 `target[i]`（因为子数组可以覆盖更宽的范围），甚至可能更高，随后在后面的子段里会把多余的层“削掉”。  

于是 **整个数组所需的最小操作数** 正好等于：

```
target[0]                     # 第一个格子必须被抬高 target[0] 次
+ Σ max(0, target[i] - target[i-1])   （i 从 1 到 n-1）
```

这就是 **贪心** + **单调递增** 的思路，时间只需一次遍历，空间只用常数。

> **从零解释核心概念**  
> - **贪心**：在每一步都做局部最优（只在需要的地方额外抬高），因为后面的操作不会影响已经满足的部分。  
> - **单调栈**（这里不需要显式使用）：如果把每次 “需要额外抬高的层数” 看成一条高度曲线，正好是 **非负的上升段**，这正是单调递增的特性。  

#### 代码（Python）

```python
def minNumberOperations(target):
    """
    贪心算法：只在相邻元素出现上升时增加操作次数。
    时间 O(n)，空间 O(1)。
    """
    if not target:
        return 0

    ops = target[0]                 # 第一个位置必须被抬高 target[0] 次
    # 从左到右检查每一对相邻元素
    for i in range(1, len(target)):
        if target[i] > target[i - 1]:
            # 只有在升高的情况下才需要额外操作
            ops += target[i] - target[i - 1]
        # 如果不升高，ops 不变
    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组。与暴力解相比，从“每个格子要走 target[i 步”降到了“每个格子只看一次相邻差”。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，不随 `n` 增长。

---

## 心得  

- **核心技巧**：把“子数组统一加 1”看成“在高度图上整体向上涂层”，于是只需要统计 **上升的那几层**。  
- **适用的题型**：  
  1. “把数组从全 0 变成目标数组”类问题（如 LeetCode 1526 `Minimum Number of Increments on Subarrays to Form a Target Array`）。  
  2. “从左到右累计增量”类问题，例如 “最小增量使数组非递减” (类似 945 `Minimum Increment to Make Array Unique`)。  
  3. “区间操作转化为差分”类题目，如 “区间加法” (LeetCode 370 `Range Addition`) 的逆向思考。  
- **一句话总结**：**只在出现向上跳跃的地方额外加一次，就是最少的子数组增操作**。

---

## 反思  

- **第一反应**：直接想到把每个元素单独增到目标值，结果是 `Σ target[i]`，显然太慢。  
- **最容易踩的坑**：忽略了相邻元素之间的**差值**可以共享同一次子数组操作；或者在实现时忘记把第一个元素的值单独计入。  
- **下次遇到同类题**：第一步先**思考“如果把整个数组一次性抬高多少层？”**，再检查**相邻位置的升高**，把问题转化为“累计正差”。这样可以迅速得到 O(n) 贪心解。