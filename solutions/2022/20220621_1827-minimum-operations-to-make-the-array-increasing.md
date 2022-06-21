# #1827. 使数组递增的最少操作次数 / Minimum Operations to Make the Array Increasing

> 难度：简单 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-the-array-increasing/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums (0-indexed). In one operation, you can choose an element of the array and increment it by 1.
Return the minimum number of operations needed to make nums strictly increasing.
An array nums is strictly increasing if nums[i] < nums[i+1] for all 0 <= i < nums.length - 1. An array of length 1 is trivially strictly increasing.

**Examples**

**Example 1:**

```
Input: nums = [1,1,1]
Output: 3
Explanation: You can do the following operations:
1) Increment nums[2], so nums becomes [1,1,2].
2) Increment nums[1], so nums becomes [1,2,2].
3) Increment nums[2], so nums becomes [1,2,3].
```

**Example 2:**

```
Input: nums = [1,5,2,4,1]
Output: 14
```

**Example 3:**

```
Input: nums = [8]
Output: 0
```

**Constraints**

- 1 <= nums.length <= 5000
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`（0 起始下标）。一次操作中，你可以选择数组中的任意元素并将其增加 1。  
返回使 `nums` **严格递增**（strictly increasing）所需的最少操作次数。  

数组 `nums` 若满足 `nums[i] < nums[i+1]` 对所有 `0 ≤ i < nums.length - 1` 成立，则称其为严格递增。长度为 1 的数组天然满足严格递增。

**示例 1**  
``` 
Input: nums = [1,1,1]
Output: 3
Explanation: 你可以进行如下操作：
1) 将 nums[2] 加 1，数组变为 [1,1,2]。
2) 将 nums[1] 加 1，数组变为 [1,2,2]。
3) 将 nums[2] 加 1，数组变为 [1,2,3]。
```  

**示例 2**  
```
Input: nums = [1,5,2,4,1]
Output: 14
```  

**示例 3**  
```
Input: nums = [8]
Output: 0
```  

**约束条件**  
- `1 ≤ nums.length ≤ 5000`  
- `1 ≤ nums[i] ≤ 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步步模拟**题目里“把某个元素加 1”的操作：

1. 从左到右检查相邻两个数 `nums[i]` 与 `nums[i+1]`。  
2. 如果 `nums[i] >= nums[i+1]`，说明 `nums[i+1]` 不够大，需要把它 **一次一次** 加 1，直到满足 `nums[i] < nums[i+1]`。  
3. 每加一次就记一次操作数，然后继续往后检查。

可以把 “把元素加 1” 想象成 **在纸上写数字**，每次只能把纸上的数字向右移动一格（加 1），所以我们只能一步一步地“爬”到满足严格递增的状态。

> **为什么正确**  
> 只要我们把每个不满足 `nums[i] < nums[i+1]` 的位置都提升到恰好比左边大 1（即 `nums[i] + 1`），整个数组必然严格递增。因为我们从左到右一次只处理当前不合法的相邻对，后面的元素在处理完前面的元素后只会变得更大，不会破坏已经得到的递增关系。

> **时间/空间分析（大白话）**  
> - **时间复杂度**：每次发现不满足时，我们会把 `nums[i+1]` 加 1，可能要加很多次。最坏情况下（比如全是 `1` 的数组），第 `i` 位要加 `i` 次，累计大约是 `1 + 2 + … + (n‑1) = O(n²)` 次循环。  
> - **空间复杂度**：我们只用了几个计数变量，和输入大小无关，属于 `O(1)`（常数）空间。

#### 代码（Python）

```python
def minOperations_bruteforce(nums):
    """
    暴力模拟：每次发现相邻两个数不满足 nums[i] < nums[i+1]，
    就把后面的数一次一次加 1，直到满足为止。
    """
    ops = 0                     # 记录总共加了多少次 1
    n = len(nums)

    # 从左到右遍历相邻位置
    for i in range(n - 1):
        # 当左边的数已经不小于右边的数时，需要把右边的数提升
        while nums[i] >= nums[i + 1]:
            nums[i + 1] += 1    # 把右边的数加 1
            ops += 1            # 操作计数加一
        # 此时 nums[i] < nums[i+1] 已经成立，继续检查下一个相邻对
    return ops
```

> **关键行中文注释**  
> - `while nums[i] >= nums[i + 1]`：如果左边不小于右边，就进入循环。  
> - `nums[i + 1] += 1`：模拟一次“把元素加 1”的操作。  
> - `ops += 1`：累计一次操作。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：在最坏情况下（如 `[1,1,1,…]`），第 `i` 位需要加 `i` 次，总加次数约等于 `1+2+…+(n‑1)`，这就是平方级别的工作量。  
- **空间复杂度**：`O(1)`  
  解释：只用了常数个额外变量（`ops、i`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次只加 1，循环次数太多**。其实我们不需要一步步加 1，只要一次性把 `nums[i+1]` 提升到**最小合法值**就行——那就是 `nums[i] + 1`（左边元素再加 1）。

**贪心原则**  
- 处理位置 `i` 时，左边已经是严格递增的（因为我们从左到右逐步保证）。  
- 为了让 `nums[i]` 与左边保持递增，`nums[i]` 最小只能取 `prev + 1`（`prev` 为 `nums[i-1]` 的最终值）。  
- 如果原始的 `nums[i]` 已经大于等于 `prev + 1`，我们**不需要动它**；否则直接把它提升到 `prev + 1`，所需的操作次数就是差值 `prev + 1 - nums[i]`。

这一步一步地“把每个位置拉到前一个位置的下一个整数”，不需要多余的循环，也不需要把某个数提升得比必要的更大——**最小化每一步的增量**，整体操作数自然最小。

> **核心数据结构**：只用到 **整数变量**（`prev` 保存前一个位置的最终值），不需要额外的数组或哈希表。  
> **类比**：把数组想象成一排递增的楼层编号，左边的楼层已经确定。我们只需要把右边的楼层“升到比左边高 1 层”，不需要一次次爬楼梯，而是直接乘电梯到目标层。

#### 代码（Python）

```python
def minOperations(nums):
    """
    贪心单遍扫描：遍历数组，保持前一个元素的最终值 prev，
    若当前元素 nums[i] 已经大于 prev，则直接更新 prev；
    否则把 nums[i] 提升到 prev + 1，累计提升的差值即为操作次数。
    """
    ops = 0            # 总操作数
    prev = nums[0]     # 第一个元素不需要改动（单元素数组本身已递增）

    # 从第二个元素开始检查
    for i in range(1, len(nums)):
        # 目标值：必须比前一个最终值大 1
        target = prev + 1

        if nums[i] < target:
            # 需要把 nums[i] 提升到 target
            ops += target - nums[i]   # 累计需要的加 1 次数
            prev = target             # 更新 prev 为提升后的值
        else:
            # 已经足够大，直接把 prev 更新为当前值
            prev = nums[i]

    return ops
```

> **关键行中文注释**  
> - `target = prev + 1`：右边元素必须至少比左边大 1。  
> - `ops += target - nums[i]`：一次性算出需要加多少次 1。  
> - `prev = target` / `prev = nums[i]`：维护左边已确定的最大值，供下一轮使用。

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次数组，线性时间。  
  与暴力解 `O(n²)` 对比：从“每次加 1、可能循环多次”降到了“一次遍历一次算完”。  
- **空间复杂度**：`O(1)` — 只用了几个整数变量，不随 `n` 增长。

---

## 心得

- **核心技巧**：**贪心**——在每一步都让当前元素保持**最小合法值**（前一个元素 + 1），这样整体操作数最小。  
- **适用的题型**：  
  1. “使数组递增/递减”类题（如 *Increasing Triplet Subsequence* 的变形）。  
  2. 需要最少增量使序列满足单调约束的题（如 *Minimum Increment to Make Array Unique*）。  
- **解题钥匙**：**一次性把每个位置拉到左侧已确定值的下一个整数**，不要循环加 1。

---

## 反思

- **第一反应**：看到“只能把元素加 1”，立刻想到**模拟**每一次加法——这导致了暴力的 `O(n²)` 解。  
- **最容易踩的坑**：  
  - 忘记更新 `prev` 为 **提升后的值**，导致后面的比较仍使用旧的、未被提升的数。  
  - 边界情况：数组长度为 1 时直接返回 0（已经递增）。  
  - 可能误以为要把所有后面的元素都提升到同一个目标值，实际上每个位置的目标值是 **前一个位置的最终值 + 1**，是动态变化的。  
- **下次遇到同类题**：第一步先**思考“每个位置的最小合法值是多少”，如果能一次性确定，就可以用贪心单遍遍历完成。