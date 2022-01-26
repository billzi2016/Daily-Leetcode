# #1646. 获取生成数组中的最大值 / Get Maximum in Generated Array

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/get-maximum-in-generated-array/)

---

## 题目（英文原版）

**Description**

You are given an integer n. A 0-indexed integer array nums of length n + 1 is generated in the following way:
Return the maximum integer in the array nums​​​.

**Examples**

**Example 1:**

```
Input: n = 7
Output: 3
Explanation: According to the given rules:
  nums[0] = 0
  nums[1] = 1
  nums[(1 * 2) = 2] = nums[1] = 1
  nums[(1 * 2) + 1 = 3] = nums[1] + nums[2] = 1 + 1 = 2
  nums[(2 * 2) = 4] = nums[2] = 1
  nums[(2 * 2) + 1 = 5] = nums[2] + nums[3] = 1 + 2 = 3
  nums[(3 * 2) = 6] = nums[3] = 2
  nums[(3 * 2) + 1 = 7] = nums[3] + nums[4] = 2 + 1 = 3
Hence, nums = [0,1,1,2,1,3,2,3], and the maximum is max(0,1,1,2,1,3,2,3) = 3.
```

**Example 2:**

```
Input: n = 2
Output: 1
Explanation: According to the given rules, nums = [0,1,1]. The maximum is max(0,1,1) = 1.
```

**Example 3:**

```
Input: n = 3
Output: 2
Explanation: According to the given rules, nums = [0,1,1,2]. The maximum is max(0,1,1,2) = 2.
```

**Constraints**

- 0 <= n <= 100

---

## 题目（中文翻译）

给定一个整数 `n`。按照下列规则生成一个 **0 索引**（0-indexed）的整数数组 `nums`，数组长度为 `n + 1`：

- `nums[0] = 0`
- `nums[1] = 1`
- 当 `i` 为 **偶数** 时，`nums[i] = nums[i / 2]`
- 当 `i` 为 **奇数** 时，`nums[i] = nums[(i - 1) / 2] + nums[(i - 1) / 2 + 1]`

返回数组 `nums` 中的最大整数（maximum integer）。

---

### 示例

#### 示例 1
**输入**  
``` 
n = 7
```  
**输出**  
```
3
```  
**解释**  
根据规则生成数组：

```
nums[0] = 0
nums[1] = 1
nums[2] = nums[1]               = 1
nums[3] = nums[1] + nums[2]     = 1 + 1 = 2
nums[4] = nums[2]               = 1
nums[5] = nums[2] + nums[3]     = 1 + 2 = 3
nums[6] = nums[3]               = 2
nums[7] = nums[3] + nums[4]     = 2 + 1 = 3
```

因此 `nums = [0,1,1,2,1,3,2,3]`，其中的最大值为 `3`。

#### 示例 2
**输入**  
``` 
n = 2
```  
**输出**  
```
1
```  
**解释**  
按照规则得到 `nums = [0,1,1]`，最大值 `max(0,1,1) = 1`。

#### 示例 3
**输入**  
``` 
n = 3
```  
**输出**  
```
2
```  
**解释**  
按照规则得到 `nums = [0,1,1,2]`，最大值 `max(0,1,1,2) = 2`。

---

### 约束条件

- `0 <= n <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求按照下面的规则生成一个长度为 `n + 1` 的数组 `nums`，随后返回其中的最大值：

1. `nums[0] = 0`，`nums[1] = 1`（这两个是固定的起始值）。  
2. 对于任意 `i ≥ 1`：  
   - 如果 `2 * i ≤ n`，则 `nums[2 * i] = nums[i]`。  
   - 如果 `2 * i + 1 ≤ n`，则 `nums[2 * i + 1] = nums[i] + nums[i + 1]`。  

这看起来像是“把一个小树根部往下展开”。  
我们可以把它想象成 **一次遍历**：从左到右依次把已经算好的 `nums[i]` 用来填充后面的 `2*i` 与 `2*i+1` 位置。  

因为 `n ≤ 100`，数组很小，直接把所有位置都算出来再找最大值，代码非常直观。  

> **为什么这个方法一定对？**  
> - 规则只依赖于已经算好的前面位置（`i` 与 `i+1`），而我们是按顺序从小到大遍历 `i`，所以在使用 `nums[i]`、`nums[i+1]` 时，它们一定已经有值。  
> - 每个合法的下标都会恰好被一次赋值（要么是 `2*i`，要么是 `2*i+1`），不会出现遗漏或冲突。

#### 代码（Python）

```python
def getMaximumGenerated(n: int) -> int:
    # 特例：n 为 0 时数组只有一个元素 [0]
    if n == 0:
        return 0

    # 初始化长度为 n+1 的数组，全部填 0
    nums = [0] * (n + 1)
    nums[0] = 0          # 题目给定的起始值
    nums[1] = 1

    # 按照题目规则，从 i = 1 开始遍历
    for i in range(1, n // 2 + 1):          # i 最大只需要到 n//2，后面的 2*i 已经超界
        if 2 * i <= n:                      # 生成偶数下标
            nums[2 * i] = nums[i]
        if 2 * i + 1 <= n:                  # 生成奇数下标
            nums[2 * i + 1] = nums[i] + nums[i + 1]

    # 返回数组中的最大值
    return max(nums)
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 我们遍历一次 `i`（最多 `n/2` 次），每次做常数操作，所以整体随 `n` 线性增长。  
  - “O(n)” 可以理解为：如果 `n` 是 100，需要的步骤大约是 100 步左右，和 `n` 成正比。

- **空间复杂度：** `O(n)`  
  - 需要额外存放长度为 `n+1` 的数组 `nums`，占用的空间随 `n` 增大而线性增长。

---

### 2. 最优解  

#### 思路  

在暴力实现里，我们已经是 **一次遍历** 生成全部数组，时间已经是线性的，无法再进一步加速（因为每个下标的值都必须被计算）。  
但我们可以 **省掉存整条数组的空间**，只保留两个信息：

1. 当前正在生成的 `nums[i]`（因为后面的值只依赖于 `i` 与 `i+1`）。  
2. 已经出现过的最大值 `max_val`。

实现思路：

- 仍然用一个长度为 `n+1` 的列表 `nums`（因为后面会用到 `nums[i+1]`），但**不必在遍历结束后再去 `max()`**，我们在生成每个新元素时直接更新 `max_val`。  
- 当 `n` 很小（如 0、1）时直接返回已知结果，避免不必要的循环。

这样时间仍是 `O(n)`，但额外的空间从 `O(n)` 降到 **`O(1)`**（只保存一个整数 `max_val`，列表本身是必须的，因为后面的值需要查 `i+1`，但如果进一步使用“滚动数组”技巧，仅保留最近两个值，也可以做到 `O(1)`，这里给出更直观的写法）。

#### 代码（Python）

```python
def getMaximumGenerated(n: int) -> int:
    if n == 0:                 # 只有 nums[0] = 0
        return 0
    if n == 1:                 # nums = [0,1]
        return 1

    nums = [0] * (n + 1)
    nums[0], nums[1] = 0, 1
    max_val = 1                # 已知的最大值是 1

    for i in range(1, n // 2 + 1):
        # 偶数位置
        if 2 * i <= n:
            nums[2 * i] = nums[i]
            if nums[2 * i] > max_val:
                max_val = nums[2 * i]

        # 奇数位置
        if 2 * i + 1 <= n:
            nums[2 * i + 1] = nums[i] + nums[i + 1]
            if nums[2 * i + 1] > max_val:
                max_val = nums[2 * i + 1]

    return max_val
```

> **关键点**：在生成每个新元素的瞬间就比较一次 `max_val`，这样遍历结束后直接返回 `max_val`，无需再遍历整个数组。

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 与暴力解相同，只是常数因子更小（省掉了最后一次 `max()` 的遍历）。

- **空间复杂度：** `O(1)`（若仅计额外变量）  
  - 除了必须的 `nums`（用来访问 `i+1`），我们不再额外开辟与 `n` 成正比的存储。若使用“滚动数组”进一步压缩，也可以做到纯 `O(1)`。

---

## 心得  

- **核心技巧**：**按规则一次遍历生成**（相当于 DP 的自底向上），并在生成过程中实时维护最大值。  
- **适用场景**：  
  1. 需要依据已有子结果递推得到新值的数组/序列（如 LeetCode 1646、1647）。  
  2. 只关心最终的“最大/最小/累计和”，不需要完整保存所有中间结果（如 “爬楼梯” 的最小步数、斐波那契数列的第 `n` 项）。  
- **一句话总结**：**遍历生成 + 实时更新最大值** 是本题的解题钥匙。

## 反思  

- **第一反应**：看到 “2*i”和 “2*i+1” 的递推式，就想到直接把数组从 0 到 n 按顺序填满。  
- **最容易踩的坑**：  
  - 忘记处理 `n = 0` 的特殊情况，会导致访问 `nums[1]` 越界。  
  - 循环上限写错：如果直接遍历到 `n`，会出现 `i+1` 超界的错误，正确的上限是 `n // 2`。  
- **下次类似题的第一步**：先手写出递推关系的**生成过程**（可以先在纸上画小例子），确认每一步只依赖已经算好的值，然后决定是一次遍历还是需要额外的数据结构。